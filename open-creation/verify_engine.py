#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ScopeGuard Audit Studio — deterministic verification suite (pure Python stdlib).

Mirrors the JavaScript policy engine embedded in index.html exactly:
  Stage 1  parse the scope/policy DSL and the multi-agent action queue DSL
  Stage 2  evaluate 8 policy rules (POL-01..POL-08) under exclusion-overrides-inclusion
           precedence, CIDR subnet-containment math, destructive-verb blocking,
           rate-limit thresholds and time-window adherence
  Stage 3  integer-exact scoring: compliance score, risk exposure index, verdict,
           deterministic remediation plan

Runs CHK-01..CHK-10 and writes the certified output to verification/run_log.txt.

Usage:  python verify_engine.py        (exit code 0 iff 10/10 checks pass)
Requires: Python 3.8+ (standard library only).
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENGINE_VERSION = '1.0.0'

# ----------------------------------------------------------------------------------
# Shared engine constants — must stay in lockstep with index.html
# ----------------------------------------------------------------------------------
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DESTRUCTIVE_METHODS = {'DELETE', 'PUT', 'PATCH'}
DESTRUCTIVE_VERBS = ['stress-load', 'stress', 'wipe', 'purge', 'destroy', 'shutdown',
                     'truncate', 'flush', 'hammer', 'flood', 'bomb', 'overwrite',
                     'rm -rf', 'drop table', 'drop-table']
SENSITIVE_VERBS = ['harvest', 'credential', 'password', 'secret', 'bypass', 'privilege',
                   'dump', 'exfiltrate', 'keylog', 'brute-force', 'bruteforce', 'token']
READ_ONLY_METHODS = {'GET', 'HEAD', 'OPTIONS'}

RULES = {
    'POL-01': 'Scope Inclusion Match',
    'POL-02': 'Exclusion Override Precedence',
    'POL-03': 'CIDR Containment',
    'POL-04': 'Destructive Operation Gate',
    'POL-05': 'Rate-Limit Threshold',
    'POL-06': 'Time Window Adherence',
    'POL-07': 'Sensitive Data & Auth Boundary',
    'POL-08': 'Method Allowlist',
}
SEVWORD = {'ok': 'OK', 'warn': 'WARN', 'violated': 'VIOLATED', 'na': 'N/A'}

URL_RE = re.compile(r'^https?://([^/?#]+)', re.I)
IP_TOKEN_RE = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
IP_LITERAL_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
CIDR_RE = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})/(\d{1,2})$')
DOMAIN_TOKEN_RE = re.compile(r'^\*?[\w.\[\]-]+\.[\w.\[\]-]+$', re.I)
WINDOW_RE = re.compile(r'^([A-Za-z]{3}(?:-[A-Za-z]{3})?(?:,[A-Za-z]{3}(?:-[A-Za-z]{3})?)*)'
                       r'\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})(?:\s+(?:UTC|GMT))?$', re.I)
DIRECTIVE_RE = re.compile(r'^(INCLUSION|EXCLUSION|ALLOW|RATE-LIMIT|WINDOW|NOTES)\s+(.*)$', re.I)


# ----------------------------------------------------------------------------------
# Stage 0 — primitives (exact mirror of the JS engine)
# ----------------------------------------------------------------------------------
def is_ip_literal(s):
    return bool(IP_LITERAL_RE.match(s))


def is_cidr(s):
    m = CIDR_RE.match(s)
    if not m:
        return False
    p = int(m.group(2))
    return 0 <= p <= 32 and is_ip_literal(m.group(1))


def ip_to_int(ip):
    m = IP_LITERAL_RE.match(ip)
    if not m:
        return None
    octets = [int(x) for x in ip.split('.')]
    if any(x > 255 for x in octets):
        return None
    return ((octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]) & 0xFFFFFFFF


def cidr_contains(cidr, ip):
    parts = cidr.split('/')
    if len(parts) != 2:
        return False
    n = ip_to_int(parts[0])
    i = ip_to_int(ip)
    if n is None or i is None:
        return False
    try:
        p = int(parts[1])
    except ValueError:
        return False
    if not (0 <= p <= 32):
        return False
    if p == 0:
        return True
    mask = (0xFFFFFFFF << (32 - p)) & 0xFFFFFFFF
    return (n & mask) == (i & mask)


def host_matches_entry(host, entry):
    h = (host or '').lower()
    e = (entry or '').lower()
    if not h or not e:
        return False
    if e.startswith('*.'):
        suf = e[1:]
        return h.endswith(suf) and len(h) > len(suf)
    if is_cidr(e) or is_ip_literal(e):
        return False
    return h == e


def entry_matches_target(entry, na):
    e = (entry or '').lower()
    if is_cidr(e) or is_ip_literal(e):
        if not na['ip']:
            return False
        if is_cidr(e):
            return cidr_contains(e, na['ip'])
        return ip_to_int(e) == ip_to_int(na['ip'])
    return host_matches_entry(na['host'], e) if na['host'] else False


def parse_window_days(spec):
    out = []
    for tok in spec.split(','):
        m = re.match(r'^([A-Za-z]{3})(?:-([A-Za-z]{3}))?$', tok.strip())
        if not m:
            continue
        a = next((i for i, d in enumerate(DAYS) if d.lower() == m.group(1).lower()), -1)
        if a < 0:
            continue
        b = a
        if m.group(2):
            b = next((i for i, d in enumerate(DAYS) if d.lower() == m.group(2).lower()), -1)
            if b < 0:
                continue
        i = a
        while True:
            out.append(DAYS[i])
            if i == b:
                break
            i = (i + 1) % 7
    seen = []
    for d in out:
        if d not in seen:
            seen.append(d)
    return seen


def parse_window(s):
    m = WINDOW_RE.match(s)
    if not m:
        return None
    return {'days': parse_window_days(m.group(1)), 'start': m.group(2), 'end': m.group(3), 'tz': 'UTC'}


def in_window(win, iso):
    if not win or not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    except ValueError:
        return None
    dt = dt.astimezone(timezone.utc)
    day = DAYS[dt.weekday()]
    cur = dt.strftime('%H:%M')
    return day in win['days'] and win['start'] <= cur <= win['end']


# ----------------------------------------------------------------------------------
# Stage 1 — parsers
# ----------------------------------------------------------------------------------
def parse_policy(text):
    p = {'inclusions': [], 'exclusions': [], 'allowed_methods': [], 'rate_limit_rpm': 60,
         'window': None, 'notes': ''}
    for line0 in str(text or '').splitlines():
        line = line0.strip()
        if not line or line.startswith('#'):
            continue
        m = DIRECTIVE_RE.match(line)
        if not m:
            continue
        key = m.group(1).upper()
        val = m.group(2).strip()
        if key == 'INCLUSION':
            if not re.match(r'^\(none', val, re.I):
                p['inclusions'].append(val.lower())
        elif key == 'EXCLUSION':
            if not re.match(r'^\(none', val, re.I):
                p['exclusions'].append(val.lower())
        elif key == 'ALLOW':
            p['allowed_methods'] = [x for x in re.split(r'[\s,]+', val.upper()) if x]
        elif key == 'RATE-LIMIT':
            n = re.search(r'(\d+)', val)
            if n:
                p['rate_limit_rpm'] = int(n.group(1))
        elif key == 'WINDOW':
            p['window'] = parse_window(val)
        elif key == 'NOTES':
            p['notes'] = val
    return p


def parse_queue(text):
    out = []
    for line0 in str(text or '').splitlines():
        line = line0.strip()
        if not line or line.startswith('#'):
            continue
        parts = [x.strip() for x in line.split('|')]
        if len(parts) < 3:
            continue
        action = {'id': parts[0], 'method': parts[1].upper(), 'target': parts[2],
                  'rate_rpm': 1, 'at': None, 'agent': 'unknown', 'notes': ''}
        rest = parts[3:]
        notes = None
        kvs = []
        for i, it in enumerate(rest):
            if it.lower().startswith('notes='):
                notes = ' | '.join([it[6:]] + rest[i + 1:]).strip()
                break
            kvs.append(it)
        for kv in kvs:
            if '=' not in kv:
                continue
            k, v = kv.split('=', 1)
            k = k.strip().lower()
            v = v.strip()
            if k == 'rate':
                try:
                    n = int(v)
                    if n > 0:
                        action['rate_rpm'] = n
                except ValueError:
                    pass
            elif k == 'at':
                action['at'] = v
            elif k == 'agent':
                action['agent'] = v
        if notes is not None:
            action['notes'] = notes
        out.append(action)
    return out


def first_verb(raw, verbs):
    for v in verbs:
        if v in raw:
            return v
    return None


def normalize_action(a):
    raw = ((a.get('method') or '') + ' ' + (a.get('target') or '') + ' ' + (a.get('notes') or '')).lower()
    t = (a.get('target') or '').strip()
    host = None
    ip = None
    um = URL_RE.match(t)
    if um:
        auth = um.group(1)
        at_idx = auth.rfind('@')
        if at_idx >= 0:
            auth = auth[at_idx + 1:]
        host = auth.split(':')[0].lower()
    ipm = IP_TOKEN_RE.search(t)
    if ipm:
        ip = ipm.group(0)
    if host and is_ip_literal(host):
        if not ip:
            ip = host
        host = None
    if not host and not ip:
        for tok in t.split():
            c = tok.rstrip("',;")
            if IP_LITERAL_RE.match(c):
                ip = c
                break
            if DOMAIN_TOKEN_RE.match(c) and not c[0].isdigit():
                host = c.lower()
                break
    rate = a.get('rate_rpm')
    try:
        rate = int(rate) if rate is not None else 1
    except (TypeError, ValueError):
        rate = 1
    if not rate or rate < 1:
        rate = 1
    return {'id': a.get('id') or 'ACT', 'agent': a.get('agent') or 'unknown',
            'method': (a.get('method') or 'GET').upper(), 'target': t, 'host': host,
            'ip': ip, 'rate_rpm': rate, 'at': a.get('at') or None,
            'notes': a.get('notes') or '', 'raw': raw}


# ----------------------------------------------------------------------------------
# Stage 2 — rule matcher (POL-01..POL-08, fixed order, exclusion-overrides-inclusion)
# ----------------------------------------------------------------------------------
def evaluate_action(policy, na):
    checks = []
    label = na['host'] or na['ip'] or na['target'] or 'unknown target'

    def add(rule_id, result, detail):
        checks.append({'rule_id': rule_id, 'name': RULES[rule_id], 'result': result, 'detail': detail})

    # POL-01 — Scope Inclusion Match
    inc_hit = next((e for e in policy['inclusions'] if entry_matches_target(e, na)), None)
    add('POL-01', 'ok' if inc_hit else 'violated',
        ("Target " + label + " matched authorized inclusion entry '" + inc_hit + "'")
        if inc_hit else ("Target " + label + " matched no inclusion entry — outside authorized scope."))

    # POL-02 — Exclusion Override Precedence
    ex_hit = next((e for e in policy['exclusions'] if entry_matches_target(e, na)), None)
    if ex_hit:
        read_only = (na['method'] in READ_ONLY_METHODS
                     and first_verb(na['raw'], DESTRUCTIVE_VERBS) is None
                     and first_verb(na['raw'], SENSITIVE_VERBS) is None)
        add('POL-02', 'warn' if read_only else 'violated',
            ("Read-only action on explicitly excluded '" + ex_hit + "': exclusion overrides inclusion — human arbitration required.")
            if read_only else
            ("Non-read-only action (" + na['method'] + ") on explicitly excluded '" + ex_hit + "': exclusion overrides inclusion — hard violation."))
    else:
        add('POL-02', 'ok', 'Target matches no explicit exclusion.')

    # POL-03 — CIDR Containment
    if na['ip']:
        c_hit = next((e for e in policy['inclusions']
                      if (is_cidr(e) and cidr_contains(e, na['ip']))
                      or (is_ip_literal(e) and ip_to_int(e) == ip_to_int(na['ip']))), None)
        add('POL-03', 'ok' if c_hit else 'violated',
            ("IP " + na['ip'] + " is contained in authorized CIDR entry '" + c_hit + "'")
            if c_hit else
            ("IP " + na['ip'] + " is not contained in any authorized CIDR entry — unapproved infrastructure."))
    else:
        add('POL-03', 'na', 'Hostname target — deterministic engine performs no DNS resolution.')

    # POL-04 — Destructive Operation Gate
    dest_m = na['method'] in DESTRUCTIVE_METHODS
    dest_v = first_verb(na['raw'], DESTRUCTIVE_VERBS)
    if dest_m:
        add('POL-04', 'violated', 'State-mutating method ' + na['method'] + ' is destructive — blocked.')
    elif dest_v:
        add('POL-04', 'violated', "Destructive verb '" + dest_v + "' detected in action text — blocked.")
    else:
        add('POL-04', 'ok', 'No destructive method or destructive verb detected.')

    # POL-05 — Rate-Limit Threshold
    over_rate = na['rate_rpm'] > policy['rate_limit_rpm']
    add('POL-05', 'warn' if over_rate else 'ok',
        ("Planned " + str(na['rate_rpm']) + " rpm exceeds cap " + str(policy['rate_limit_rpm'])
         + " rpm on " + label + " — throttling decision requires human review.")
        if over_rate else
        ("Planned " + str(na['rate_rpm']) + " rpm vs cap " + str(policy['rate_limit_rpm']) + " rpm — within cap."))

    # POL-06 — Time Window Adherence
    if not policy['window']:
        add('POL-06', 'na', 'No time window declared in policy.')
    elif not na['at']:
        add('POL-06', 'na', 'Action carries no timestamp.')
    else:
        inw = in_window(policy['window'], na['at'])
        wtxt = ('authorized window (' + ','.join(policy['window']['days']) + ' '
                + policy['window']['start'] + '-' + policy['window']['end'] + ' UTC)')
        if inw is None:
            add('POL-06', 'na', 'Timestamp ' + na['at'] + ' could not be parsed.')
        elif inw:
            add('POL-06', 'ok', 'Timestamp ' + na['at'] + ' is inside ' + wtxt + '.')
        else:
            add('POL-06', 'warn', 'Timestamp ' + na['at'] + ' falls outside ' + wtxt + ' — reschedule or obtain approval.')

    # POL-07 — Sensitive Data & Auth Boundary
    sv = first_verb(na['raw'], SENSITIVE_VERBS)
    add('POL-07', 'violated' if sv else 'ok',
        ("Sensitive-intent keyword '" + sv + "' detected — credential/auth boundary hard violation.")
        if sv else 'No credential/token-harvesting or auth-bypass intent detected.')

    # POL-08 — Method Allowlist
    method_ok = na['method'] in policy['allowed_methods']
    add('POL-08', 'ok' if method_ok else 'violated',
        ('Method ' + na['method'] + ' is in allowed methods (' + ', '.join(policy['allowed_methods']) + ').')
        if method_ok else
        ('Method ' + na['method'] + ' is not in allowed methods (' + ', '.join(policy['allowed_methods']) + ') — blocked.'))

    if any(c['result'] == 'violated' for c in checks):
        status = 'BLOCK_VIOLATION'
    elif any(c['result'] == 'warn' for c in checks):
        status = 'WARN_HUMAN_REVIEW'
    else:
        status = 'PASS'
    return {'action': na, 'checks': checks, 'status': status}


# ----------------------------------------------------------------------------------
# Stage 3 — scoring, remediation, exports
# ----------------------------------------------------------------------------------
def compute_metrics(findings):
    npass = sum(1 for f in findings if f['status'] == 'PASS')
    nwarn = sum(1 for f in findings if f['status'] == 'WARN_HUMAN_REVIEW')
    nblock = sum(1 for f in findings if f['status'] == 'BLOCK_VIOLATION')
    total = len(findings)
    half_sum = 2 * npass + nwarn
    denom = 2 * max(total, 1)
    # Integer-exact round-half-up of 100 * half_sum / denom — identical to Math.round in JS.
    score = 100 if total == 0 else (200 * half_sum + denom) // (2 * denom)
    rei = min(100, 30 * nblock + 12 * nwarn)
    verdict = 'REJECTED' if nblock > 0 else ('ESCALATE_TO_HUMAN' if nwarn > 0 else 'APPROVED')
    return {'total_actions': total, 'pass': npass, 'warn': nwarn, 'block': nblock,
            'compliance_score': score, 'risk_exposure_index': rei, 'verdict': verdict}


def build_remediation(findings, policy):
    steps = []
    seen = set()

    def push(action_id, rule_id, step):
        if step and step not in seen:
            seen.add(step)
            steps.append({'action_id': action_id, 'rule_id': rule_id, 'step': step})

    for f in findings:
        na = f['action']
        label = na['host'] or na['ip'] or na['target']
        for c in f['checks']:
            if c['result'] not in ('violated', 'warn'):
                continue
            rid = c['rule_id']
            if rid == 'POL-01':
                push(na['id'], rid, 'Remove the action or amend the authorized scope to include ' + label + '.')
            elif rid == 'POL-02':
                if c['result'] == 'warn':
                    ex = next((e for e in policy['exclusions'] if entry_matches_target(e, na)), 'the excluded asset')
                    push(na['id'], rid, 'Human arbitration required: read-only action targets explicitly excluded '
                         + ex + ' — approve via written scope amendment or drop the action.')
                else:
                    push(na['id'], rid, 'Target ' + label + ' is explicitly excluded — drop the action or obtain a written scope amendment.')
            elif rid == 'POL-03':
                push(na['id'], rid, 'IP ' + label + ' is outside all authorized CIDR blocks — remove the action or request authorization for the range.')
            elif rid == 'POL-04':
                push(na['id'], rid, 'Replace the destructive operation on ' + label + ' with a read-safe equivalent (e.g., GET) or drop the action.')
            elif rid == 'POL-05':
                push(na['id'], rid, 'Throttle ' + label + ' to at most ' + str(policy['rate_limit_rpm'])
                     + ' rpm or split the workload across the authorized window.')
            elif rid == 'POL-06':
                wtxt = (','.join(policy['window']['days']) + ' ' + policy['window']['start'] + '-'
                        + policy['window']['end'] + ' UTC') if policy['window'] else ''
                push(na['id'], rid, 'Reschedule the action on ' + label + ' inside the authorized window '
                     + wtxt + ' or obtain an explicit exception.')
            elif rid == 'POL-07':
                push(na['id'], rid, 'Strip credential/token-harvesting or auth-bypass intent from the action on '
                     + label + '; it is out of bounds for this engagement.')
            elif rid == 'POL-08':
                push(na['id'], rid, 'Restrict interactions with ' + label + ' to the allowed methods ('
                     + ', '.join(policy['allowed_methods']) + ').')
    return steps


def run_pipeline(policy_text, queue_text):
    policy = parse_policy(policy_text)
    actions = [normalize_action(a) for a in parse_queue(queue_text)]
    findings = [evaluate_action(policy, a) for a in actions]
    metrics = compute_metrics(findings)
    remediation = build_remediation(findings, policy)
    return {'policy': policy, 'actions': actions, 'findings': findings,
            'metrics': metrics, 'remediation': remediation}


def window_text(p):
    if not p['window']:
        return 'none declared'
    return ','.join(p['window']['days']) + ' ' + p['window']['start'] + '-' + p['window']['end'] + ' UTC'


def to_markdown_report(res):
    L = []
    m = res['metrics']
    p = res['policy']
    L.append('# Compliance Audit Report — [REDACTED_ENTITY] Engagement')
    L.append('')
    L.append('Deterministic output of ScopeGuard Audit Studio (pipeline v' + ENGINE_VERSION
             + '). All identifiers are sanitized: organizations, personnel and hosts appear as '
             + '[REDACTED_ENTITY]; financial figures as [REDACTED_AMOUNT]; infrastructure uses RFC 5737 '
             + 'documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24).')
    L.append('')
    L.append('## 1. Executive Summary')
    L.append('')
    L.append('- Verdict: ' + m['verdict'])
    L.append('- Compliance Score: ' + str(m['compliance_score']) + '/100')
    L.append('- Risk Exposure Index: ' + str(m['risk_exposure_index']) + '/100')
    L.append('- Actions Audited: ' + str(m['total_actions']) + ' (PASS: ' + str(m['pass'])
             + ', WARN_HUMAN_REVIEW: ' + str(m['warn']) + ', BLOCK_VIOLATION: ' + str(m['block']) + ')')
    L.append('')
    L.append('## 2. Scope & Policy Snapshot')
    L.append('')
    L.append('- Inclusions: ' + (', '.join(p['inclusions']) or 'none declared'))
    L.append('- Explicit Exclusions: ' + (', '.join(p['exclusions']) or 'none declared'))
    L.append('- Allowed Methods: ' + (', '.join(p['allowed_methods']) or 'none'))
    L.append('- Rate-Limit Cap: ' + str(p['rate_limit_rpm']) + ' rpm per host')
    L.append('- Authorized Window: ' + window_text(p))
    L.append('')
    L.append('## 3. Findings Matrix')
    L.append('')
    L.append('| Action | Agent | Method | Target | Status | Citations |')
    L.append('|---|---|---|---|---|---|')
    for f in res['findings']:
        cites = ', '.join(c['rule_id'] for c in f['checks'] if c['result'] in ('violated', 'warn')) or '—'
        L.append('| ' + f['action']['id'] + ' | ' + f['action']['agent'] + ' | ' + f['action']['method']
                 + ' | ' + f['action']['target'] + ' | ' + f['status'] + ' | ' + cites + ' |')
    L.append('')
    L.append('## 4. Rule Evaluation Traces')
    L.append('')
    for f in res['findings']:
        L.append('### ' + f['action']['id'] + ' — ' + f['action']['method'] + ' ' + f['action']['target'])
        for c in f['checks']:
            L.append('- ' + c['rule_id'] + ' ' + c['name'] + ': ' + SEVWORD[c['result']] + ' — ' + c['detail'])
        L.append('')
    L.append('## 5. Remediation Plan')
    L.append('')
    if not res['remediation']:
        L.append('No remediation required — all queued actions satisfied the active policy.')
    else:
        for i, r in enumerate(res['remediation'], 1):
            L.append(str(i) + '. [' + r['action_id'] + '] ' + r['step'])
    L.append('')
    L.append('## 6. Method & Assumptions')
    L.append('')
    L.append('- Deterministic 3-stage pipeline: Parser -> Policy Matcher -> Risk/Report Generator.')
    L.append('- Exclusion-overrides-inclusion precedence is always enforced (POL-02).')
    L.append('- No DNS resolution: hostname targets are matched textually; CIDR checks use exact IPv4 subnet-containment math.')
    L.append('- Severity ladder: read-only actions on excluded assets escalate to human review; mutating, destructive, '
             'sensitive-intent or unapproved-infrastructure actions are hard-blocked.')
    L.append('- Redaction compliance: this report contains only [REDACTED_ENTITY] / [REDACTED_AMOUNT] placeholders '
             'and RFC 5737 documentation ranges.')
    return '\n'.join(L)


def to_json_bundle(res):
    bundle = {
        'schema': 'scopeguard.audit-bundle/1.0',
        'generated_by': 'ScopeGuard Audit Studio',
        'engine_version': ENGINE_VERSION,
        'policy': {
            'inclusions': res['policy']['inclusions'],
            'exclusions': res['policy']['exclusions'],
            'allowed_methods': res['policy']['allowed_methods'],
            'rate_limit_rpm': res['policy']['rate_limit_rpm'],
            'window': res['policy']['window'],
        },
        'actions': [
            {'id': a['id'], 'agent': a['agent'], 'method': a['method'], 'target': a['target'],
             'host': a['host'], 'ip': a['ip'], 'rate_rpm': a['rate_rpm'], 'at': a['at'], 'notes': a['notes']}
            for a in res['actions']
        ],
        'findings': [
            {'action_id': f['action']['id'], 'status': f['status'],
             'citations': [{'rule_id': c['rule_id'], 'name': c['name'], 'result': c['result'],
                            'detail': c['detail']} for c in f['checks']]}
            for f in res['findings']
        ],
        'metrics': res['metrics'],
        'remediation': res['remediation'],
    }
    return json.dumps(bundle, indent=2, ensure_ascii=False)


# ----------------------------------------------------------------------------------
# Fixture loading
# ----------------------------------------------------------------------------------
FIXTURES = BASE / 'sample_scopes'
FIX1 = FIXTURES / '01_authorized_baseline.md'
FIX2 = FIXTURES / '02_out_of_scope_violation.md'
FIX3 = FIXTURES / '03_wildcard_conflict.md'


def load_fixture(path):
    text = path.read_text(encoding='utf-8')
    scope = re.search(r'```scope\s*\n(.*?)```', text, re.S)
    queue = re.search(r'```queue\s*\n(.*?)```', text, re.S)
    if not scope or not queue:
        raise AssertionError('missing fenced scope/queue blocks in ' + path.name)
    return scope.group(1), queue.group(1)


# ----------------------------------------------------------------------------------
# CHK-01..CHK-10
# ----------------------------------------------------------------------------------
def chk01():
    scope, queue = load_fixture(FIX1)
    rep = run_pipeline(scope, queue)
    m = rep['metrics']
    ok = (m['verdict'] == 'APPROVED' and m['compliance_score'] == 100
          and m['pass'] == 4 and m['warn'] == 0 and m['block'] == 0
          and m['risk_exposure_index'] == 0
          and all(f['status'] == 'PASS' for f in rep['findings']))
    detail = ('verdict=%s score=%d/100 REI=%d/100 findings: %d PASS / %d WARN / %d BLOCK '
              '(expected APPROVED / 100 / 4 PASS / 0 WARN / 0 BLOCK)'
              % (m['verdict'], m['compliance_score'], m['risk_exposure_index'],
                 m['pass'], m['warn'], m['block']))
    return ok, detail


def chk02():
    scope, queue = load_fixture(FIX2)
    rep = run_pipeline(scope, queue)
    m = rep['metrics']
    expected_cites = {
        'A1': {'POL-01', 'POL-02', 'POL-07', 'POL-08'},
        'A2': {'POL-01', 'POL-03'},
        'A3': {'POL-04', 'POL-08'},
        'A4': {'POL-04', 'POL-05', 'POL-08'},
        'A5': set(),
    }
    actual_cites = {}
    for f in rep['findings']:
        actual_cites[f['action']['id']] = set(
            c['rule_id'] for c in f['checks'] if c['result'] in ('violated', 'warn'))
    base_ok = (m['verdict'] == 'REJECTED' and m['compliance_score'] == 20
               and m['pass'] == 1 and m['block'] == 4 and m['risk_exposure_index'] == 100)
    cites_ok = actual_cites == expected_cites
    detail = ('verdict=%s score=%d/100 REI=%d/100 findings: %d PASS / %d WARN / %d BLOCK; citations exact-match: %s'
              % (m['verdict'], m['compliance_score'], m['risk_exposure_index'],
                 m['pass'], m['warn'], m['block'], cites_ok))
    return base_ok and cites_ok, detail


def chk03():
    scope, queue = load_fixture(FIX3)
    rep = run_pipeline(scope, queue)
    m = rep['metrics']
    a2 = next(f for f in rep['findings'] if f['action']['id'] == 'A2')
    res_of = lambda f, rid: next(c['result'] for c in f['checks'] if c['rule_id'] == rid)
    ok = (m['verdict'] == 'ESCALATE_TO_HUMAN' and m['compliance_score'] == 88
          and m['warn'] == 1 and m['block'] == 0 and m['risk_exposure_index'] == 12
          and a2['status'] == 'WARN_HUMAN_REVIEW'
          and res_of(a2, 'POL-01') == 'ok'
          and res_of(a2, 'POL-02') == 'warn'
          and res_of(a2, 'POL-06') == 'warn'
          and all(f['status'] == 'PASS' for f in rep['findings'] if f['action']['id'] != 'A2'))
    detail = ('verdict=%s score=%d/100 REI=%d/100 findings: %d PASS / %d WARN / %d BLOCK; '
              'A2=WARN_HUMAN_REVIEW with POL-01 ok (wildcard matched) but POL-02 warn + POL-06 warn '
              '(exclusion-overrides-inclusion precedence proven)'
              % (m['verdict'], m['compliance_score'], m['risk_exposure_index'],
                 m['pass'], m['warn'], m['block']))
    return ok, detail


def chk04():
    pairs = [
        ('192.0.2.0/24', '192.0.2.10', True),
        ('192.0.2.0/24', '192.0.3.10', False),
        ('192.0.2.0/24', '192.0.2.255', True),
        ('192.0.2.0/24', '192.0.1.255', False),
        ('198.51.100.0/24', '198.51.100.0', True),
        ('203.0.113.0/24', '203.0.114.1', False),
        ('192.0.2.7/32', '192.0.2.7', True),
        ('192.0.2.7/32', '192.0.2.8', False),
        ('0.0.0.0/0', '203.0.113.9', True),
    ]
    import ipaddress
    failures = []
    for net, ip, expected in pairs:
        got = cidr_contains(net, ip)
        ref = ipaddress.ip_address(ip) in ipaddress.ip_network(net, strict=False)
        if got != expected or got != ref:
            failures.append('%s vs %s: got %s, expected %s, ipaddress-ref %s' % (ip, net, got, expected, ref))
    ok = not failures
    detail = ('9/9 boundary assertions hold and match the ipaddress-module reference '
              '(192.0.2.10 inside 192.0.2.0/24 vs 192.0.3.10 outside; network/broadcast edges; '
              '/32 exactness; /0 supernet)') if ok else ('; '.join(failures))
    return ok, detail


def chk05():
    policy = parse_policy('INCLUSION *.[REDACTED_ENTITY]\n'
                          'EXCLUSION legacy-auth.[REDACTED_ENTITY]\n'
                          'ALLOW GET HEAD OPTIONS\nRATE-LIMIT 60 rpm per host\n'
                          'WINDOW Mon-Fri 09:00-17:00 UTC')
    queue = parse_queue(
        'B1 | GET | https://legacy-auth.[REDACTED_ENTITY]/v1/session/peek | rate=1 | '
        'at=2026-11-19T14:00:00Z | agent=probe | notes=Read-only probe of excluded legacy host\n'
        'B2 | GET | https://portal.[REDACTED_ENTITY]/v1/health | rate=1 | '
        'at=2026-11-19T14:05:00Z | agent=probe | notes=Wildcard health probe')
    f1 = evaluate_action(policy, normalize_action(queue[0]))
    f2 = evaluate_action(policy, normalize_action(queue[1]))

    def res_of(f, rid):
        return next(c['result'] for c in f['checks'] if c['rule_id'] == rid)

    wildcard_would_match = host_matches_entry('legacy-auth.[REDACTED_ENTITY]', '*.[REDACTED_ENTITY]')
    ok = (wildcard_would_match
          and f1['status'] == 'WARN_HUMAN_REVIEW'
          and res_of(f1, 'POL-01') == 'ok'
          and res_of(f1, 'POL-02') == 'warn'
          and f2['status'] == 'PASS'
          and res_of(f2, 'POL-02') == 'ok')
    detail = ('wildcard would match legacy host: %s; B1=%s (POL-01 %s yet POL-02 %s — exclusion overrides inclusion); '
              'B2=%s (no exclusion hit)'
              % (wildcard_would_match, f1['status'], res_of(f1, 'POL-01'), res_of(f1, 'POL-02'), f2['status']))
    return ok, detail


def chk06():
    policy = parse_policy('INCLUSION api.[REDACTED_ENTITY]\nINCLUSION 192.0.2.0/24\n'
                          'ALLOW GET HEAD OPTIONS\nRATE-LIMIT 60 rpm per host\n'
                          'WINDOW Mon-Fri 09:00-17:00 UTC')
    queue = parse_queue(
        'C1 | DELETE | https://api.[REDACTED_ENTITY]/v1/users/9 | rate=1 | '
        'at=2026-11-19T14:00:00Z | agent=t | notes=destructive probe\n'
        'C2 | GET | https://api.[REDACTED_ENTITY]/v1/list | rate=500 | '
        'at=2026-11-19T14:01:00Z | agent=t | notes=high volume sweep\n'
        'C3 | EXEC | stress-load --target 192.0.2.10 --rps 900 | rate=10 | '
        'at=2026-11-19T14:02:00Z | agent=t | notes=load burst')
    f1 = evaluate_action(policy, normalize_action(queue[0]))
    f2 = evaluate_action(policy, normalize_action(queue[1]))
    f3 = evaluate_action(policy, normalize_action(queue[2]))

    def res_of(f, rid):
        return next((c['result'] for c in f['checks'] if c['rule_id'] == rid), 'missing')

    ok = (f1['status'] == 'BLOCK_VIOLATION' and res_of(f1, 'POL-04') == 'violated'
          and f2['status'] == 'WARN_HUMAN_REVIEW' and res_of(f2, 'POL-05') == 'warn'
          and res_of(f2, 'POL-04') == 'ok'
          and f3['status'] == 'BLOCK_VIOLATION' and res_of(f3, 'POL-04') == 'violated')
    detail = ('C1 DELETE in-scope: %s (POL-04 %s); C2 GET at 500 rpm vs cap 60: %s (POL-05 %s, POL-04 %s); '
              'C3 stress-load tool run: %s (POL-04 %s)'
              % (f1['status'], res_of(f1, 'POL-04'), f2['status'], res_of(f2, 'POL-05'),
                 res_of(f2, 'POL-04'), f3['status'], res_of(f3, 'POL-04')))
    return ok, detail


def chk07():
    scope, queue = load_fixture(FIX2)
    md = to_markdown_report(run_pipeline(scope, queue))
    required = [
        '# Compliance Audit Report',
        '## 1. Executive Summary',
        '- Verdict: REJECTED',
        '- Compliance Score: 20/100',
        '- Risk Exposure Index: 100/100',
        '## 2. Scope & Policy Snapshot',
        '## 3. Findings Matrix',
        '## 4. Rule Evaluation Traces',
        '## 5. Remediation Plan',
        '## 6. Method & Assumptions',
        'POL-04',
        'POL-02',
        'POL-07',
        '[REDACTED_ENTITY]',
        'billing.[REDACTED_ENTITY]',
        '- Deterministic 3-stage pipeline',
    ]
    missing = [r for r in required if r not in md]
    rows = len(re.findall(r'^\| A\d ', md, re.M))
    ok = not missing and rows == 5
    detail = ('all 16 required sections/tokens present and 5 finding rows found'
              if ok else ('missing: %s; finding rows=%d' % (', '.join(missing), rows)))
    return ok, detail


def chk08():
    scope, queue = load_fixture(FIX2)
    bundle = json.loads(to_json_bundle(run_pipeline(scope, queue)))
    expected_keys = {'schema', 'generated_by', 'engine_version', 'policy', 'actions',
                     'findings', 'metrics', 'remediation'}
    m = bundle.get('metrics', {})
    consistent = (m.get('total_actions') == 5
                  and m.get('total_actions') == m.get('pass', -1) + m.get('warn', -1) + m.get('block', -1)
                  and m.get('compliance_score') == 20
                  and m.get('verdict') == 'REJECTED')
    findings_ok = (len(bundle.get('findings', [])) == 5
                   and all(len(f['citations']) == 8 and all(c['rule_id'] in RULES for c in f['citations'])
                           for f in bundle['findings'])
                   and all(f['status'] in ('PASS', 'WARN_HUMAN_REVIEW', 'BLOCK_VIOLATION')
                           for f in bundle['findings']))
    actions_ok = len(bundle.get('actions', [])) == 5
    remediation_ok = (len(bundle.get('remediation', [])) >= 4
                      and all(set(r) == {'action_id', 'rule_id', 'step'} for r in bundle['remediation']))
    ok = (set(bundle) == expected_keys
          and bundle['schema'] == 'scopeguard.audit-bundle/1.0'
          and consistent and findings_ok and actions_ok and remediation_ok)
    detail = ('bundle schema/keys complete; 5 actions, 5 findings x 8 citations, metrics consistent '
              '(score 20, verdict REJECTED), %d remediation steps'
              % len(bundle.get('remediation', []))) if ok else \
             ('keys=%s consistent=%s findings_ok=%s actions_ok=%s remediation_ok=%s'
              % (sorted(set(bundle)), consistent, findings_ok, actions_ok, remediation_ok))
    return ok, detail


SELF_CONTAINMENT_PATTERNS = [
    (r'<script\b[^>]*\bsrc\s*=', 'script with src attribute'),
    (r'<link\b[^>]*\bhref\s*=', 'link element with href'),
    (r'<iframe\b', 'iframe element'),
    (r'<embed\b', 'embed element'),
    (r'<object\b', 'object element'),
    (r'<img\b[^>]*\bsrc\s*=', 'img element with src'),
    (r'@import', 'CSS @import'),
    (r'url\(\s*[\'"]?\s*https?:', 'CSS url() referencing http(s)'),
]


def chk09():
    html = (BASE / 'index.html').read_text(encoding='utf-8')
    hits = []
    for pat, label in SELF_CONTAINMENT_PATTERNS:
        if re.search(pat, html, re.I):
            hits.append(label)
    has_doctype = html.lstrip().lower().startswith('<!doctype html')
    has_title = 'ScopeGuard Audit Studio' in html
    ok = not hits and has_doctype and has_title
    detail = ('0 external-resource patterns found (script src / link href / iframe / embed / object / img src / '
              '@import / css url(http)); DOCTYPE and title present') if ok else \
             ('violations: %s; doctype=%s title=%s' % (', '.join(hits), has_doctype, has_title))
    return ok, detail


# RFC 5737 documentation ranges plus loopback/private/link-local/unspecified space.
ALLOWED_NETS = [
    ('192.0.2.0', 24), ('198.51.100.0', 24), ('203.0.113.0', 24),
    ('127.0.0.0', 8), ('10.0.0.0', 8), ('172.16.0.0', 12),
    ('192.168.0.0', 16), ('169.254.0.0', 16), ('0.0.0.0', 8),
]
# Boundary-probe literals mandated by CHK-04 (they sit just OUTSIDE a TEST-NET block on
# purpose, to prove containment math rejects them). They appear only in engine
# self-test code and its log, never as fixture targets.
ALLOWED_IP_LITERALS = {'192.0.3.10', '192.0.1.255', '203.0.114.1'}


def ip_allowed(ip):
    if ip in ALLOWED_IP_LITERALS:
        return True
    for net, prefix in ALLOWED_NETS:
        if cidr_contains(net + '/' + str(prefix), ip):
            return True
    return False


def chk10():
    email_re = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    ip_re = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    dom_re = re.compile(r'(?<![\w.\-])(?:[A-Za-z0-9\-]+\.)+'
                        r'(?:com|net|org|io|dev|app|ai|co|uk|us|eu|info|biz|me|gov|edu)\b', re.I)
    cur_re = re.compile(r'[$€£¥]\s*\d')
    amt_re = re.compile(r'\b(?:USD|EUR|GBP|CHF)\s*\d', re.I)
    problems = []
    files = [p for p in sorted(BASE.rglob('*')) if p.is_file()]
    ent_count = 0
    amt_count = 0
    scanned = 0
    for p in files:
        rel = p.relative_to(BASE)
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, ValueError):
            problems.append('%s: not decodable as UTF-8 text' % rel)
            continue
        scanned += 1
        for m in email_re.finditer(text):
            problems.append('%s: email-like token found' % rel)
            break
        for m in ip_re.finditer(text):
            if not ip_allowed(m.group(0)):
                problems.append('%s: non-allowlisted IPv4 literal %s' % (rel, m.group(0)))
        for m in dom_re.finditer(text):
            problems.append('%s: bare registrable-domain-like token %s' % (rel, m.group(0)))
        for m in cur_re.finditer(text):
            problems.append('%s: raw currency amount found' % rel)
        for m in amt_re.finditer(text):
            problems.append('%s: raw currency-code amount found' % rel)
        ent_count += text.count('[REDACTED_ENTITY]')
        amt_count += text.count('[REDACTED_AMOUNT]')
    for f in (FIX1, FIX2, FIX3):
        t = f.read_text(encoding='utf-8')
        if '[REDACTED_ENTITY]' not in t:
            problems.append('%s: missing [REDACTED_ENTITY] placeholder' % f.name)
    if amt_count < 3:
        problems.append('too few [REDACTED_AMOUNT] occurrences across the project: %d' % amt_count)
    ok = not problems
    if ok:
        detail = ('scanned %d files: 0 email tokens, 0 non-allowlisted IPv4 literals '
                  '(RFC 5737 + loopback/private/link-local + 3 CHK-04 boundary probes), '
                  '0 bare registrable domains, 0 raw currency amounts; placeholders present '
                  '([REDACTED_ENTITY] x%d, [REDACTED_AMOUNT] x%d)'
                  % (scanned, ent_count, amt_count))
    else:
        detail = '%d problem(s): %s' % (len(problems), '; '.join(problems[:12]))
    return ok, detail


CHECKS = [
    ('CHK-01', 'Preset 1 Authorized Baseline: exact verdict, score and finding mix', chk01),
    ('CHK-02', 'Preset 2 Out-of-Scope and Destructive Trap: exact verdict, score, citations', chk02),
    ('CHK-03', 'Preset 3 Wildcard vs Exclusion Conflict: exact verdict, score, precedence proof', chk03),
    ('CHK-04', 'CIDR boundary precision vs ipaddress reference', chk04),
    ('CHK-05', 'Exclusion-overrides-wildcard precedence', chk05),
    ('CHK-06', 'Destructive method and rate-limit breach detection', chk06),
    ('CHK-07', 'Markdown export schema and completeness', chk07),
    ('CHK-08', 'JSON export schema, keys and metric consistency', chk08),
    ('CHK-09', 'index.html self-containment audit (zero external dependencies)', chk09),
    ('CHK-10', 'Redaction audit across all project files', chk10),
]


def main():
    results = []
    for cid, desc, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as e:  # noqa: BLE001 — report any failure honestly
            ok, detail = False, 'unexpected exception: %s: %s' % (type(e).__name__, e)
        results.append((cid, desc, bool(ok), detail))
    passed = sum(1 for r in results if r[2])
    total = len(results)
    lines = []
    lines.append('ScopeGuard Audit Studio — Deterministic Verification Run')
    lines.append('Engine: verify_engine.py v%s (pure Python stdlib mirror of the index.html engine)' % ENGINE_VERSION)
    lines.append('Run at: ' + datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    lines.append('=' * 78)
    for cid, desc, ok, detail in results:
        lines.append('%s  [%s]' % (cid, 'PASS' if ok else 'FAIL'))
        lines.append('  claim : %s' % desc)
        lines.append('  result: %s' % detail)
    lines.append('=' * 78)
    lines.append('SUMMARY: %d/%d checks passed%s' % (passed, total, ' — CERTIFIED' if passed == total else ' — NOT CERTIFIED'))
    text = '\n'.join(lines) + '\n'
    outdir = BASE / 'verification'
    outdir.mkdir(exist_ok=True)
    (outdir / 'run_log.txt').write_text(text, encoding='utf-8')
    print(text)
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
