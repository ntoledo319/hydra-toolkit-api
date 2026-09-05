#!/usr/bin/env python3
"""project_history.py -- deterministic, dependency-free history tooling.

Commands (run from the project root):
  assess [range] [paths...]      flag potentially material surfaces in new work (advisory)
  context [paths|component]      smallest relevant history for an area of the tree
  validate                       schemas, ids, dates, links, anchors, secrets, render drift
  render [--check]               rebuild TIMELINE, decision index, PROJECT_HISTORY.md
  audit --full | --since <sha>   compare git evidence with recorded history
  declaration --text T|--file F  check a history-impact declaration (CI helper)

The ledgers under .project-history/ use a strict YAML subset parsed here
(block mappings, block sequences, flow lists of scalars, quoted strings,
literal/folded block scalars). Nothing here injects timestamps into rendered
output; the only dated artifact is an audit report written on explicit request.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import json
import os
import re
import subprocess
import sys

HEX40 = re.compile(r"\b[0-9a-f]{40}\b")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GEN_BEGIN = "<!-- BEGIN GENERATED: {name} -->"
GEN_END = "<!-- END GENERATED: {name} -->"

CLAIM_EVIDENCE = {"direct", "contemporaneous", "retrospective", "behavioral", "inferred"}
CLAIM_STATUS = {"verified", "reported", "inferred", "disputed", "unknown"}
CONFIDENCE = {"confirmed", "strongly_supported", "plausible", "speculative", "unknown"}
EVENT_REQUIRED = [
    "id", "title", "kind", "scope", "significance", "occurred_at", "decided_at", "merged_at",
    "released_at", "recorded_at", "last_verified_at", "claim_ids", "source_ids", "status",
    "confidence", "secrets_reviewed",
]
EVENT_SECTIONS = [
    "Before-state and pressure", "Intended beneficiaries", "Goal, non-goal and definition of success",
    "Principles affected", "Alternatives and rejected paths", "Decision and rationale",
    "Implementation and evidence", "Expected versus observed outcome",
    "Tradeoffs, debt and consequences", "Related events", "Unresolved questions",
]
GOAL_STATUS = {"proposed", "active", "narrowed", "expanded", "blocked", "achieved", "abandoned", "superseded"}
PRINCIPLE_STATUS = {"active", "weakened", "challenged", "superseded", "retired"}
DECLARATION_RE = re.compile(
    r"history:(recorded|none|defer)\s*(?:[-—:]\s*)?(.*)", re.IGNORECASE)

SECRET_PATTERNS = [
    re.compile(p) for p in [
        r"AKIA[0-9A-Z]{16}", r"ASIA[0-9A-Z]{16}",
        r"\b(?:sk|rk|pk)_(?:live|test)_[0-9A-Za-z]{16,}", r"\bwhsec_[0-9A-Za-z]{16,}",
        r"\bghp_[0-9A-Za-z]{30,}", r"\bgithub_pat_[0-9A-Za-z_]{20,}", r"\bgho_[0-9A-Za-z]{30,}",
        r"\bxox[abprs]-[0-9A-Za-z-]{10,}", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY",
        r"\bAIza[0-9A-Za-z_-]{35}\b", r"\bsk-[A-Za-z0-9]{20,}\b", r"\bsk-ant-[A-Za-z0-9_-]{20,}",
        r"\bre_[A-Za-z0-9]{8}_[A-Za-z0-9]{20,}",
        r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}",
        r"(?i)(?:postgres|postgresql|mysql|mongodb(?:\+srv)?|redis|amqp)://[^:\s/]+:[^@\s/]{4,}@",
        r"\b[A-Za-z_]*(?:SECRET|TOKEN|PASSWORD|API_KEY)[A-Za-z_]*\s*[=:]\s*[\"']?(?!\$\{|\$[A-Z]|<|\[|\(|\{|null|none|redacted|changeme|xxx|your[-_])[A-Za-z0-9+/=_\-]{24,}[\"']?",
    ]
]
# Positive control for the scanner, assembled at runtime so this source file never contains a matching literal.
SECRET_CONTROL = " ".join(["AKIA" + "IOSFODNN7EXAMPLE", "sk_live_" + "4eC39HqLyjWDarjtT1zdp7dc", "-----BEGIN " + "PRIVATE KEY-----"])


# --------------------------------------------------------------------------- YAML subset
class YamlError(ValueError):
    pass


class _Parser:
    def __init__(self, text: str):
        self.lines = text.split("\n")
        self.i = 0

    def _is_skippable(self, line: str) -> bool:
        s = line.strip()
        return s == "" or s.startswith("#")

    def _peek(self):
        while self.i < len(self.lines) and self._is_skippable(self.lines[self.i]):
            self.i += 1
        if self.i >= len(self.lines):
            return None
        line = self.lines[self.i]
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent + 1]:
            raise YamlError(f"line {self.i + 1}: tabs are not allowed for indentation")
        return indent, line[indent:].rstrip(), self.i

    def parse(self):
        tok = self._peek()
        if tok is None:
            return {}
        value = self._block(tok[0])
        rest = self._peek()
        if rest is not None:
            raise YamlError(f"line {rest[2] + 1}: unexpected content after document")
        return value

    def _block(self, indent: int):
        tok = self._peek()
        if tok is None:
            return None
        if tok[0] != indent:
            raise YamlError(f"line {tok[2] + 1}: expected indent {indent}, found {tok[0]}")
        if tok[1] == "-" or tok[1].startswith("- "):
            return self._sequence(indent)
        return self._mapping(indent)

    def _mapping(self, indent: int):
        out = {}
        while True:
            tok = self._peek()
            if tok is None or tok[0] < indent:
                return out
            if tok[0] > indent:
                raise YamlError(f"line {tok[2] + 1}: unexpected deeper indent")
            if tok[1] == "-" or tok[1].startswith("- "):
                return out
            key, rest = self._split_key(tok[1], tok[2])
            if key in out:
                raise YamlError(f"line {tok[2] + 1}: duplicate key {key!r}")
            self.i += 1
            out[key] = self._value_after_key(indent, rest, tok[2])

    def _sequence(self, indent: int):
        out = []
        while True:
            tok = self._peek()
            if tok is None or tok[0] < indent:
                return out
            if tok[0] > indent:
                raise YamlError(f"line {tok[2] + 1}: unexpected deeper indent in sequence")
            if not (tok[1] == "-" or tok[1].startswith("- ")):
                return out
            item = tok[1][1:].lstrip() if tok[1] != "-" else ""
            if item == "":
                self.i += 1
                nxt = self._peek()
                if nxt is None or nxt[0] <= indent:
                    out.append(None)
                else:
                    out.append(self._block(nxt[0]))
            elif self._looks_like_key(item):
                # rewrite the line so the mapping starts at a virtual indent
                virtual = indent + 2
                self.lines[tok[2]] = " " * virtual + item
                out.append(self._mapping(virtual))
            else:
                self.i += 1
                out.append(self._scalar(item, tok[2]))

    KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.\-/ ]*?):(?:\s+(.*))?$")

    def _looks_like_key(self, s: str) -> bool:
        if s.startswith(("\"", "'", "[")):
            return False
        return bool(self.KEY_RE.match(s))

    def _split_key(self, content: str, lineno: int):
        m = self.KEY_RE.match(content)
        if not m:
            raise YamlError(f"line {lineno + 1}: expected 'key: value', got {content!r}")
        return m.group(1).strip(), (m.group(2) or "").strip()

    def _value_after_key(self, indent: int, rest: str, lineno: int):
        if rest == "":
            nxt = self._peek()
            if nxt is None or nxt[0] <= indent:
                return None
            return self._block(nxt[0])
        if rest in ("|", "|-", ">", ">-"):
            return self._block_scalar(indent, rest, lineno)
        return self._scalar(rest, lineno)

    def _block_scalar(self, indent: int, style: str, lineno: int):
        collected = []
        block_indent = None
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if line.strip() == "":
                collected.append("")
                self.i += 1
                continue
            cur = len(line) - len(line.lstrip(" "))
            if cur <= indent:
                break
            if block_indent is None:
                block_indent = cur
            collected.append(line[block_indent:] if cur >= block_indent else line.strip())
            self.i += 1
        while collected and collected[-1] == "":
            collected.pop()
        if style.startswith("|"):
            text = "\n".join(collected)
        else:
            paras, buf = [], []
            for ln in collected:
                if ln == "":
                    paras.append(" ".join(buf))
                    buf = []
                else:
                    buf.append(ln.strip())
            paras.append(" ".join(buf))
            text = "\n".join(paras)
        return text if style.endswith("-") else text + "\n"

    def _scalar(self, s: str, lineno: int):
        s = s.strip()
        if s.startswith("\""):
            try:
                return json.loads(s)
            except json.JSONDecodeError as exc:
                raise YamlError(f"line {lineno + 1}: bad double-quoted string: {exc}")
        if s.startswith("'"):
            if not s.endswith("'") or len(s) < 2:
                raise YamlError(f"line {lineno + 1}: bad single-quoted string")
            return s[1:-1].replace("''", "'")
        if s.startswith("["):
            if not s.endswith("]"):
                raise YamlError(f"line {lineno + 1}: unterminated flow list")
            return [self._scalar(p, lineno) for p in self._split_flow(s[1:-1], lineno)]
        if s.startswith("{"):
            raise YamlError(f"line {lineno + 1}: flow mappings are not supported")
        if s in ("null", "~"):
            return None
        if s == "true":
            return True
        if s == "false":
            return False
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+\.\d+", s):
            return float(s)
        return s

    @staticmethod
    def _split_flow(body: str, lineno: int):
        parts, buf, quote = [], [], None
        for ch in body:
            if quote:
                buf.append(ch)
                if ch == quote:
                    quote = None
            elif ch in ("\"", "'"):
                quote = ch
                buf.append(ch)
            elif ch == ",":
                parts.append("".join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        tail = "".join(buf).strip()
        if tail:
            parts.append(tail)
        return [p for p in parts if p != ""]


def parse_yaml(text: str):
    return _Parser(text).parse()


def split_front_matter(text: str):
    if not text.startswith("---\n"):
        raise YamlError("event capsule must start with '---' front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise YamlError("front matter is not terminated by '---'")
    return parse_yaml(text[4:end + 1]), text[end + 5:]


# --------------------------------------------------------------------------- repository access
class Repo:
    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        self.policy = self._load_yaml(os.path.join(root, ".project-history", "policy.yml"))
        self.docs_dir = os.path.join(root, self.policy.get("docs_dir", "docs/history"))
        self.ph_dir = os.path.join(root, self.policy.get("history_dir", ".project-history"))

    # ---- files
    def _load_yaml(self, path: str):
        with open(path, encoding="utf-8") as fh:
            return parse_yaml(fh.read())

    def read(self, rel: str) -> str:
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def exists(self, rel: str) -> bool:
        return os.path.exists(os.path.join(self.root, rel))

    def ledger(self, name: str):
        return self._load_yaml(os.path.join(self.ph_dir, name))

    def events(self):
        out = []
        base = os.path.join(self.ph_dir, "events")
        for dirpath, _dirs, files in os.walk(base):
            for fn in sorted(files):
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dirpath, fn)
                with open(path, encoding="utf-8") as fh:
                    meta, body = split_front_matter(fh.read())
                out.append({"path": os.path.relpath(path, self.root), "meta": meta, "body": body})
        out.sort(key=lambda e: (str(e["meta"].get("occurred_at") or ""), str(e["meta"].get("id"))))
        return out

    # ---- git
    def git(self, *args, check=True) -> str:
        proc = subprocess.run(["git", "-C", self.root, *args], capture_output=True, text=True)
        if check and proc.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
        return proc.stdout

    def commit_exists(self, sha: str, extra_repos=()) -> bool:
        for repo in (self.root, *extra_repos):
            proc = subprocess.run(["git", "-C", repo, "cat-file", "-e", f"{sha}^{{commit}}"],
                                  capture_output=True)
            if proc.returncode == 0:
                return True
        return False

    def related_repo_paths(self):
        paths = []
        try:
            sources = self.ledger("sources.yml")
        except FileNotFoundError:
            return paths
        for src in sources.get("sources", []) or []:
            for key in ("local_path", "path"):
                p = src.get(key) if isinstance(src, dict) else None
                if isinstance(p, str) and os.path.isdir(os.path.join(p, ".git")) and os.path.abspath(p) != self.root:
                    paths.append(os.path.abspath(p))
        return sorted(set(paths))


# --------------------------------------------------------------------------- helpers
def _as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def _globs_match(path: str, patterns) -> bool:
    for pat in patterns or []:
        pat = str(pat)
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(os.path.basename(path), pat):
            return True
        if pat.endswith("/**") and (path == pat[:-3] or path.startswith(pat[:-3] + "/")):
            return True
        if pat.endswith("/*") and os.path.dirname(path) == pat[:-2]:
            return True
    return False


def _date_ok(v) -> bool:
    return v is None or (isinstance(v, str) and bool(DATE_RE.match(v)))


def _scan_secrets(text: str):
    hits = []
    for n, line in enumerate(text.split("\n"), 1):
        for pat in SECRET_PATTERNS:
            if pat.search(line):
                hits.append((n, pat.pattern[:28]))
                break
    return hits


def parse_declaration(text: str):
    """Return {'kind','detail'} for a well-formed declaration, else raise ValueError."""
    found = [m for m in DECLARATION_RE.finditer(text or "")]
    if not found:
        raise ValueError("no history declaration found (expected history:recorded|none|defer)")
    if len(found) > 1:
        raise ValueError("more than one history declaration found; declare exactly one")
    kind = found[0].group(1).lower()
    detail = found[0].group(2).strip().strip("`*_ ").strip()
    if kind == "recorded":
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]{3,}", detail):
            raise ValueError("history:recorded must name an event id")
    elif kind == "none":
        if len(detail) < 8:
            raise ValueError("history:none must give a specific reason")
    else:
        if len(detail) < 12 or not re.search(r"\d{4}-\d{2}-\d{2}", detail):
            raise ValueError("history:defer must name a tracking item, an owner and a YYYY-MM-DD deadline")
    return {"kind": kind, "detail": detail}


# --------------------------------------------------------------------------- validate
class Validator:
    def __init__(self, repo: Repo, today: str | None = None):
        self.repo = repo
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.today = today or _dt.date.today().isoformat()

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def run(self, check_render=True):
        r = self.repo
        pol = r.policy
        for key in ("docs_dir", "commands", "repository", "materiality"):
            if key not in pol:
                self.err(f"policy.yml missing top-level '{key}'")
        for cmd in ("assess", "context", "validate", "render", "audit_full", "audit_incremental", "test"):
            if cmd not in (pol.get("commands") or {}):
                self.err(f"policy.yml commands.{cmd} missing")
        required = [
            "PROJECT_HISTORY.md", "AGENTS.md",
            *(os.path.join(pol.get("docs_dir", "docs/history"), f) for f in
              ("ORIENTATION.md", "NARRATIVE.md", "IDEOLOGY.md", "GOALS.md", "DECISION_MAP.md",
               "TIMELINE.md", "OPEN_QUESTIONS.md")),
            *(os.path.join(".project-history", f) for f in
              ("policy.yml", "sources.yml", "claims.yml", "contradictions.yml", "state.yml",
               "doctrine/principles.yml", "doctrine/goals.yml", "schemas/event.schema.json",
               "templates/event.md")),
        ]
        for rel in required:
            if not r.exists(rel):
                self.err(f"required file missing: {rel}")
        if self.errors:
            return self
        sources = r.ledger("sources.yml")
        claims = r.ledger("claims.yml")
        contradictions = r.ledger("contradictions.yml")
        state = r.ledger("state.yml")
        principles = r.ledger("doctrine/principles.yml")
        goals = r.ledger("doctrine/goals.yml")
        try:
            schema = json.loads(r.read(".project-history/schemas/event.schema.json"))
        except json.JSONDecodeError as exc:
            self.err(f"event.schema.json is not valid JSON: {exc}")
            schema = {}
        events = r.events()
        related = r.related_repo_paths()

        source_ids = self._check_sources(sources)
        claim_ids = self._check_claims(claims, source_ids, related)
        self._check_contradictions(contradictions, claim_ids, source_ids)
        event_ids = self._check_events(events, schema, claim_ids, source_ids, related)
        self._check_doctrine(principles, "principle", PRINCIPLE_STATUS, claim_ids, event_ids)
        self._check_doctrine(goals, "goal", GOAL_STATUS, claim_ids, event_ids)
        self._check_state(state, related)
        self._check_deferrals(pol)
        self._check_agent_contract()
        self._check_links()
        self._check_secrets()
        self._check_cited_shas(related)
        if check_render:
            drift = Renderer(r).render(write=False)
            for rel in drift:
                self.err(f"rendered output drifted: {rel} (run render)")
        return self

    # -- pieces
    def _check_sources(self, sources):
        ids = set()
        for s in sources.get("sources", []) or []:
            sid = s.get("id")
            if not sid:
                self.err("source without id")
                continue
            if sid in ids:
                self.err(f"duplicate source id {sid}")
            ids.add(sid)
            for key in ("kind", "class", "access"):
                if key not in s:
                    self.err(f"source {sid} missing '{key}'")
            if s.get("class") not in {"direct", "contemporaneous", "retrospective", "behavioral", "inferred", "external"}:
                self.err(f"source {sid} has unknown class {s.get('class')!r}")
            if s.get("access") not in {"accessible", "inaccessible", "partial"}:
                self.err(f"source {sid} has unknown access {s.get('access')!r}")
            if s.get("retrieved_at") is not None and not _date_ok(s.get("retrieved_at")):
                self.err(f"source {sid} retrieved_at is not YYYY-MM-DD")
        if not ids:
            self.err("sources.yml lists no sources")
        return ids

    def _check_claims(self, claims, source_ids, related):
        ids = set()
        for c in claims.get("claims", []) or []:
            cid = c.get("claim_id")
            if not cid:
                self.err("claim without claim_id")
                continue
            if cid in ids:
                self.err(f"duplicate claim_id {cid}")
            ids.add(cid)
            for key in ("claim", "source_ids", "locator", "evidence_type", "status", "confidence", "rationale", "caveats"):
                if key not in c:
                    self.err(f"claim {cid} missing '{key}'")
            if "date" not in c and "date_range" not in c:
                self.err(f"claim {cid} needs date or date_range")
            if c.get("evidence_type") not in CLAIM_EVIDENCE:
                self.err(f"claim {cid} evidence_type {c.get('evidence_type')!r} invalid")
            if c.get("status") not in CLAIM_STATUS:
                self.err(f"claim {cid} status {c.get('status')!r} invalid")
            if c.get("confidence") not in CONFIDENCE:
                self.err(f"claim {cid} confidence {c.get('confidence')!r} invalid")
            if c.get("status") == "verified" and c.get("evidence_type") == "inferred":
                self.err(f"claim {cid} cannot be both 'verified' and 'inferred'")
            for sid in _as_list(c.get("source_ids")):
                if sid not in source_ids:
                    self.err(f"claim {cid} cites unknown source {sid}")
            if not _as_list(c.get("source_ids")):
                self.err(f"claim {cid} cites no sources")
            if c.get("date") is not None and not _date_ok(c.get("date")):
                self.err(f"claim {cid} date must be YYYY-MM-DD")
        return ids

    def _check_contradictions(self, contradictions, claim_ids, source_ids):
        seen = set()
        for x in contradictions.get("contradictions", []) or []:
            xid = x.get("id")
            if not xid:
                self.err("contradiction without id")
                continue
            if xid in seen:
                self.err(f"duplicate contradiction id {xid}")
            seen.add(xid)
            for key in ("disputed_claim", "accounts", "disagreement_kind", "best_supported_reading", "confidence", "resolving_evidence"):
                if key not in x:
                    self.err(f"contradiction {xid} missing '{key}'")
            if x.get("confidence") not in CONFIDENCE:
                self.err(f"contradiction {xid} confidence invalid")
            if len(_as_list(x.get("accounts"))) < 2:
                self.err(f"contradiction {xid} needs at least two accounts")
            for acc in _as_list(x.get("accounts")):
                for sid in _as_list(acc.get("source_ids") if isinstance(acc, dict) else None):
                    if sid not in source_ids:
                        self.err(f"contradiction {xid} account cites unknown source {sid}")
            for cid in _as_list(x.get("claim_ids")):
                if cid not in claim_ids:
                    self.err(f"contradiction {xid} cites unknown claim {cid}")

    def _check_events(self, events, schema, claim_ids, source_ids, related):
        ids = {}
        req = schema.get("required", EVENT_REQUIRED) if isinstance(schema, dict) else EVENT_REQUIRED
        kinds = set((schema.get("properties", {}).get("kind", {}).get("enum") or [])) if isinstance(schema, dict) else set()
        for ev in events:
            m, body = ev["meta"], ev["body"]
            eid = m.get("id")
            if not eid:
                self.err(f"{ev['path']}: event without id")
                continue
            if eid in ids:
                self.err(f"duplicate event id {eid} ({ev['path']} and {ids[eid]})")
            ids[eid] = ev["path"]
            if os.path.splitext(os.path.basename(ev["path"]))[0] != eid:
                self.err(f"{ev['path']}: file name must equal event id {eid}")
            for key in req:
                if key not in m:
                    self.err(f"event {eid} missing front-matter key '{key}'")
            for key in ("occurred_at", "decided_at", "merged_at", "released_at", "recorded_at", "last_verified_at"):
                if not _date_ok(m.get(key)):
                    self.err(f"event {eid} {key} must be YYYY-MM-DD or null")
            if m.get("occurred_at") and m.get("recorded_at") and m["recorded_at"] < m["occurred_at"]:
                self.err(f"event {eid} recorded_at earlier than occurred_at")
            if m.get("backfilled") is True and m.get("occurred_at") and m.get("recorded_at") and m["recorded_at"] <= m["occurred_at"]:
                self.err(f"event {eid} is backfilled but recorded_at is not later than occurred_at")
            if kinds and m.get("kind") not in kinds:
                self.err(f"event {eid} kind {m.get('kind')!r} not in schema enum")
            if m.get("significance") not in {"high", "medium", "low"}:
                self.err(f"event {eid} significance invalid")
            if m.get("status") not in {"open", "closed", "amended", "superseded"}:
                self.err(f"event {eid} status invalid")
            if m.get("confidence") not in CONFIDENCE:
                self.err(f"event {eid} confidence invalid")
            if m.get("secrets_reviewed") is not True:
                self.err(f"event {eid} secrets_reviewed must be true")
            if not _as_list(m.get("claim_ids")):
                self.err(f"event {eid} cites no claims")
            for cid in _as_list(m.get("claim_ids")):
                if cid not in claim_ids:
                    self.err(f"event {eid} cites unknown claim {cid}")
            for sid in _as_list(m.get("source_ids")):
                if sid not in source_ids:
                    self.err(f"event {eid} cites unknown source {sid}")
            for sha in _as_list(m.get("anchors")):
                if not re.fullmatch(r"[0-9a-f]{40}", str(sha)):
                    self.err(f"event {eid} anchor {sha!r} is not a 40-hex sha")
                elif not self.repo.commit_exists(str(sha), related):
                    self.err(f"event {eid} anchor {sha} is unreachable (rewritten or foreign history?)")
            for section in EVENT_SECTIONS:
                if f"## {section}" not in body:
                    self.err(f"event {eid} lacks section '## {section}'")
            if m.get("amendments"):
                for am in _as_list(m.get("amendments")):
                    if not isinstance(am, dict) or not am.get("date") or not am.get("reason") or not am.get("confidence_moved"):
                        self.err(f"event {eid} amendment must carry date, reason and confidence_moved")
        # link resolution (second pass)
        for ev in events:
            m = ev["meta"]
            for key in ("related_events", "amends", "supersedes", "reverses"):
                for other in _as_list(m.get(key)):
                    if other not in ids:
                        self.err(f"event {m.get('id')} {key} -> unknown event {other}")
        if not any(m["meta"].get("kind") == "bootstrap" for m in events):
            self.err("no bootstrap event for the history system itself")
        return set(ids)

    def _check_doctrine(self, doc, label, statuses, claim_ids, event_ids):
        items = doc.get(label + "s", []) or []
        ids = {}
        for it in items:
            iid = it.get("id")
            if not iid:
                self.err(f"{label} without id")
                continue
            key = (iid, it.get("version"))
            if key in ids:
                self.err(f"duplicate {label} {iid} v{it.get('version')}")
            ids[key] = it
            if it.get("status") not in statuses:
                self.err(f"{label} {iid} status {it.get('status')!r} invalid")
            if not isinstance(it.get("version"), int):
                self.err(f"{label} {iid} version must be an integer")
            if not _date_ok(it.get("introduced_at")):
                self.err(f"{label} {iid} introduced_at must be YYYY-MM-DD")
            for cid in _as_list(it.get("claim_ids")):
                if cid not in claim_ids:
                    self.err(f"{label} {iid} cites unknown claim {cid}")
            for eid in _as_list(it.get("event_ids")):
                if eid not in event_ids:
                    self.err(f"{label} {iid} cites unknown event {eid}")
            if label == "goal" and it.get("status") == "active" and it.get("review_by") and str(it["review_by"]) < self.today:
                self.warn(f"goal {iid} is active but review_by {it['review_by']} has passed (stale goal)")
        for (iid, ver), it in ids.items():
            sup = it.get("supersedes")
            if sup:
                if isinstance(sup, dict):
                    target = (sup.get("id"), sup.get("version"))
                else:
                    target = (str(sup), None)
                if target[1] is None:
                    if not any(k[0] == target[0] for k in ids):
                        self.err(f"{label} {iid} v{ver} supersedes unknown {target[0]}")
                elif target not in ids:
                    self.err(f"{label} {iid} v{ver} supersedes unknown {target[0]} v{target[1]}")
                elif ids[target].get("status") not in {"superseded", "retired", "abandoned", "achieved", "narrowed", "expanded", "weakened"}:
                    self.err(f"{label} {target[0]} v{target[1]} is superseded by {iid} v{ver} but not marked superseded")

    def _check_state(self, state, related):
        for key in ("repository", "audit_date", "full_audit_anchor", "incremental_anchor", "reachable_commit_count",
                    "refs_examined", "exclusion_counts", "source_classes", "inaccessible_sources", "evidence_gaps", "rewritten_history"):
            if key not in state:
                self.err(f"state.yml missing '{key}'")
        for key in ("full_audit_anchor", "incremental_anchor"):
            v = str(state.get(key) or "")
            if not re.fullmatch(r"[0-9a-f]{40}", v):
                self.err(f"state.yml {key} is not a 40-hex sha")
            elif not self.repo.commit_exists(v):
                self.err(f"state.yml {key} {v} is unreachable in this repository")
        try:
            actual = int(self.repo.git("rev-list", "--all", "--count").strip())
        except RuntimeError as exc:
            self.err(str(exc))
            return
        if state.get("reachable_commit_count") != actual:
            self.err(f"state.yml reachable_commit_count={state.get('reachable_commit_count')} but git reports {actual}")

    def _check_deferrals(self, pol):
        for d in pol.get("deferrals", []) or []:
            for key in ("id", "owner", "deadline", "tracking"):
                if not d.get(key):
                    self.err(f"deferral {d.get('id', '?')} missing '{key}' (naked deferrals are not allowed)")
            if d.get("deadline") and str(d["deadline"]) < self.today and d.get("status", "open") == "open":
                self.err(f"deferral {d.get('id')} expired on {d['deadline']} (owner {d.get('owner')})")

    def _check_agent_contract(self):
        text = ""
        for fn in ("AGENTS.md", "CLAUDE.md"):
            if self.repo.exists(fn):
                text += self.repo.read(fn)
        for tok in ("history:recorded", "history:none", "history:defer"):
            if tok not in text:
                self.err(f"AGENTS.md lacks the declaration token {tok}")
        if "ORIENTATION.md" not in text:
            self.err("AGENTS.md does not direct agents to docs/history/ORIENTATION.md")
        pr = ""
        for fn in (".github/PULL_REQUEST_TEMPLATE.md", ".github/pull_request_template.md", "docs/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md"):
            if self.repo.exists(fn):
                pr += self.repo.read(fn)
        if not pr:
            self.err("no pull-request template found")
        for tok in ("history:recorded", "history:none", "history:defer"):
            if tok not in pr:
                self.err(f"PR template lacks {tok}")

    def _check_links(self):
        files = [os.path.join(self.repo.root, "PROJECT_HISTORY.md")]
        for dirpath, _d, fns in os.walk(self.repo.docs_dir):
            files += [os.path.join(dirpath, f) for f in fns if f.endswith(".md")]
        for f in files:
            if not os.path.exists(f):
                continue
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
            for m in re.finditer(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", text):
                target = m.group(1)
                if re.match(r"^[a-z]+:", target, re.I):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), target))):
                    self.err(f"broken link in {os.path.relpath(f, self.repo.root)} -> {target}")

    def _artifact_files(self):
        files = [os.path.join(self.repo.root, "PROJECT_HISTORY.md")]
        for base in (self.repo.docs_dir, self.repo.ph_dir):
            for dirpath, _d, fns in os.walk(base):
                files += [os.path.join(dirpath, f) for f in fns]
        return [f for f in files if os.path.exists(f)]

    def _check_secrets(self):
        if not any(p.search(SECRET_CONTROL) for p in SECRET_PATTERNS):
            self.err("secret-scan positive control failed; scanner is broken")
        for f in self._artifact_files():
            with open(f, encoding="utf-8", errors="replace") as fh:
                for n, pat in _scan_secrets(fh.read()):
                    self.err(f"possible secret in {os.path.relpath(f, self.repo.root)}:{n} ({pat}...)")

    def _check_cited_shas(self, related):
        shas = set()
        for f in self._artifact_files():
            if not f.endswith((".md", ".yml", ".yaml", ".json")):
                continue
            with open(f, encoding="utf-8", errors="replace") as fh:
                shas.update(HEX40.findall(fh.read()))
        bad = sorted(s for s in shas if not self.repo.commit_exists(s, related))
        for s in bad:
            self.err(f"cited sha {s} does not resolve in this repository or any related repository listed in sources.yml")
        self.cited_shas = shas


# --------------------------------------------------------------------------- render
class Renderer:
    def __init__(self, repo: Repo):
        self.repo = repo

    def _replace_generated(self, text: str, name: str, generated: str) -> str:
        b, e = GEN_BEGIN.format(name=name), GEN_END.format(name=name)
        if b not in text or e not in text:
            raise RuntimeError(f"markers for generated block '{name}' not found")
        pre = text[: text.index(b) + len(b)]
        post = text[text.index(e):]
        return pre + "\n" + generated.rstrip("\n") + "\n" + post

    def timeline(self, events, claims) -> str:
        rows = []
        for ev in events:
            m = ev["meta"]
            for key in ("occurred_at", "decided_at", "merged_at", "released_at"):
                if m.get(key):
                    rows.append((m[key], key.replace("_at", ""), m["id"], m.get("title", ""), ev["path"]))
        for c in claims.get("claims", []) or []:
            d = c.get("date") or (c.get("date_range") or {}).get("start") if isinstance(c.get("date_range"), dict) else c.get("date")
            if isinstance(c.get("date_range"), str) and not d:
                d = c["date_range"].split("..")[0].strip()
            if d:
                rows.append((str(d), "claim", c["claim_id"], c.get("claim", "")[:110], ".project-history/claims.yml"))
        rows.sort(key=lambda r: (r[0], r[1], r[2]))
        out = ["| Date | Kind | Id | Summary | Record |", "|---|---|---|---|---|"]
        for d, kind, ident, title, path in rows:
            out.append(f"| {d} | {kind} | `{ident}` | {title.replace('|', '/').strip()} | `{path}` |")
        anchors = sorted({str(s) for ev in events for s in _as_list(ev["meta"].get("anchors"))})
        out += ["", "### Git anchors cited by events", ""]
        out += [f"- `{s}`" for s in anchors] or ["- (none)"]
        return "\n".join(out)

    def decision_index(self, events, principles, goals) -> str:
        out = ["| Event | Kind | Significance | Occurred | Status | Related | Amends / supersedes |", "|---|---|---|---|---|---|---|"]
        for ev in events:
            m = ev["meta"]
            rel = ", ".join(f"`{x}`" for x in _as_list(m.get("related_events"))) or "—"
            am = ", ".join(f"`{x}`" for x in (_as_list(m.get("amends")) + _as_list(m.get("supersedes")) + _as_list(m.get("reverses")))) or "—"
            out.append(f"| `{m['id']}` | {m.get('kind')} | {m.get('significance')} | {m.get('occurred_at')} | {m.get('status')} | {rel} | {am} |")
        out += ["", "#### Principles (versioned)", "", "| Id | v | Status | Introduced | Supersedes | Statement |", "|---|---|---|---|---|---|"]
        for p in principles.get("principles", []) or []:
            sup = p.get("supersedes")
            sup_s = f"`{sup.get('id')}` v{sup.get('version')}" if isinstance(sup, dict) else (f"`{sup}`" if sup else "—")
            out.append(f"| `{p['id']}` | {p.get('version')} | {p.get('status')} | {p.get('introduced_at')} | {sup_s} | {str(p.get('statement', '')).strip().replace('|', '/')} |")
        out += ["", "#### Goals (lifecycle)", "", "| Id | v | Status | Introduced | Review by | Supersedes | Statement |", "|---|---|---|---|---|---|---|"]
        for g in goals.get("goals", []) or []:
            sup = g.get("supersedes")
            sup_s = f"`{sup.get('id')}` v{sup.get('version')}" if isinstance(sup, dict) else (f"`{sup}`" if sup else "—")
            out.append(f"| `{g['id']}` | {g.get('version')} | {g.get('status')} | {g.get('introduced_at')} | {g.get('review_by') or '—'} | {sup_s} | {str(g.get('statement', '')).strip().replace('|', '/')} |")
        return "\n".join(out)

    def project_history(self, events, claims, contradictions, sources, state) -> str:
        pol = self.repo.policy
        order = pol.get("render_order") or ["ORIENTATION.md", "NARRATIVE.md", "IDEOLOGY.md", "GOALS.md", "DECISION_MAP.md", "TIMELINE.md", "OPEN_QUESTIONS.md"]
        title = pol.get("project", pol.get("repository"))
        parts = [f"# {title} — Project History", "",
                 "_Canonical, unabridged reading path. Assembled deterministically by `scripts/project_history` "
                 "`render` from the curated chapters in `docs/history/` and the evidence ledgers in `.project-history/`. "
                 "Edit the chapters, not this file._", "", "## Contents", ""]
        chapters = []
        for name in order:
            if name.endswith("/*"):
                d = os.path.join(self.repo.docs_dir, name[:-2])
                if os.path.isdir(d):
                    chapters += [os.path.join(name[:-2], f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
            else:
                chapters.append(name)
        for ch in chapters:
            parts.append(f"- [{ch}](#{self._anchor('Chapter: ' + ch)})")
        for extra in ("Appendix A — Claims ledger", "Appendix B — Contradiction register", "Appendix C — Source inventory", "Appendix D — Coverage and reproducibility"):
            parts.append(f"- [{extra}](#{self._anchor(extra)})")
        parts.append("")
        for ch in chapters:
            path = os.path.join(self.repo.docs_dir, ch)
            if not os.path.exists(path):
                raise RuntimeError(f"render_order names missing chapter {ch}")
            with open(path, encoding="utf-8") as fh:
                body = fh.read().rstrip("\n")
            parts += [f"## Chapter: {ch}", "", self._shift_headings(body), ""]
        parts += ["## Appendix A — Claims ledger", "", "| Claim | Date | Type | Status | Confidence | Statement |", "|---|---|---|---|---|---|"]
        for c in claims.get("claims", []) or []:
            d = c.get("date") or c.get("date_range")
            if isinstance(d, dict):
                d = f"{d.get('start')}..{d.get('end')}"
            parts.append(f"| `{c['claim_id']}` | {d} | {c.get('evidence_type')} | {c.get('status')} | {c.get('confidence')} | {str(c.get('claim', '')).strip().replace('|', '/')} |")
        parts += ["", "## Appendix B — Contradiction register", ""]
        for x in contradictions.get("contradictions", []) or []:
            parts += [f"### `{x['id']}` — {x.get('disputed_claim', '').strip()}", "", f"- Disagreement kind: {x.get('disagreement_kind')}"]
            for acc in _as_list(x.get("accounts")):
                if isinstance(acc, dict):
                    parts.append(f"- Account ({', '.join(_as_list(acc.get('source_ids'))) or 'unsourced'}; {acc.get('date', 'undated')}; {acc.get('proximity', 'proximity unknown')}): {str(acc.get('says', '')).strip()}")
            parts += [f"- Best-supported reading ({x.get('confidence')}): {str(x.get('best_supported_reading', '')).strip()}",
                      f"- Resolving evidence: {str(x.get('resolving_evidence', '')).strip()}", ""]
        parts += ["## Appendix C — Source inventory", "", "| Source | Kind | Class | Access | Retrieved | Locator |", "|---|---|---|---|---|---|"]
        for s in sources.get("sources", []) or []:
            loc = s.get("locator") or s.get("local_path") or s.get("url") or ""
            parts.append(f"| `{s['id']}` | {s.get('kind')} | {s.get('class')} | {s.get('access')} | {s.get('retrieved_at') or '—'} | {str(loc).replace('|', '/')} |")
        parts += ["", "## Appendix D — Coverage and reproducibility", ""]
        for key in ("repository", "audit_date", "full_audit_anchor", "incremental_anchor", "reachable_commit_count", "refs_examined",
                    "exclusion_counts", "source_classes", "inaccessible_sources", "evidence_gaps", "rewritten_history", "coverage_matrix", "completeness_statement"):
            val = state.get(key)
            if val is None:
                continue
            if isinstance(val, (dict, list)):
                parts.append(f"- **{key}:**")
                parts += self._bullets(val, 2)
            else:
                parts.append(f"- **{key}:** {str(val).strip()}")
        parts.append("")
        return "\n".join(parts)

    def _bullets(self, val, depth):
        out = []
        pad = " " * depth
        if isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, (dict, list)):
                    out.append(f"{pad}- {k}:")
                    out += self._bullets(v, depth + 2)
                else:
                    out.append(f"{pad}- {k}: {str(v).strip()}")
        else:
            for v in val:
                if isinstance(v, (dict, list)):
                    out += self._bullets(v, depth)
                else:
                    out.append(f"{pad}- {str(v).strip()}")
        return out

    @staticmethod
    def _anchor(text: str) -> str:
        s = text.lower()
        s = re.sub(r"[^\w\s-]", "", s)
        return re.sub(r"\s+", "-", s.strip())

    @staticmethod
    def _shift_headings(body: str) -> str:
        out, in_code = [], False
        for line in body.split("\n"):
            if line.startswith("```"):
                in_code = not in_code
            if not in_code and re.match(r"^#{1,5} ", line):
                line = "#" + line
            out.append(line)
        return "\n".join(out)

    def render(self, write=True):
        r = self.repo
        events = r.events()
        claims = r.ledger("claims.yml")
        contradictions = r.ledger("contradictions.yml")
        sources = r.ledger("sources.yml")
        state = r.ledger("state.yml")
        principles = r.ledger("doctrine/principles.yml")
        goals = r.ledger("doctrine/goals.yml")
        changed = []
        tl_path = os.path.join(r.docs_dir, "TIMELINE.md")
        tl = self._replace_generated(self._read_or_seed(tl_path, "timeline"), "timeline", self.timeline(events, claims))
        changed += self._write(tl_path, tl, write)
        dm_path = os.path.join(r.docs_dir, "DECISION_MAP.md")
        dm = self._replace_generated(self._read_or_seed(dm_path, "decision-index"), "decision-index", self.decision_index(events, principles, goals))
        changed += self._write(dm_path, dm, write)
        # PROJECT_HISTORY.md reads the (possibly just-updated) chapters
        if write:
            ph = self.project_history(events, claims, contradictions, sources, state)
        else:
            # compute against in-memory chapter content so --check is exact
            ph = self._project_history_with_overrides(events, claims, contradictions, sources, state, {tl_path: tl, dm_path: dm})
        changed += self._write(os.path.join(r.root, "PROJECT_HISTORY.md"), ph, write)
        return changed

    def _project_history_with_overrides(self, events, claims, contradictions, sources, state, overrides):
        original = {}
        try:
            for p, content in overrides.items():
                if os.path.exists(p):
                    with open(p, encoding="utf-8") as fh:
                        original[p] = fh.read()
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(content)
            return self.project_history(events, claims, contradictions, sources, state)
        finally:
            for p, content in original.items():
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(content)

    @staticmethod
    def _read_or_seed(path, name):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return fh.read()
        return f"# {os.path.basename(path)}\n\n{GEN_BEGIN.format(name=name)}\n{GEN_END.format(name=name)}\n"

    @staticmethod
    def _write(path, content, write):
        if not content.endswith("\n"):
            content += "\n"
        old = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                old = fh.read()
        if old == content:
            return []
        if write:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
        return [path]


# --------------------------------------------------------------------------- assess / context / audit
def _material_classification(repo: Repo, path: str):
    mat = repo.policy.get("materiality", {}) or {}
    if _globs_match(path, mat.get("noise_paths")):
        return "noise", "history/tooling/generated path (policy.materiality.noise_paths)"
    for rule in mat.get("material_paths", []) or []:
        if isinstance(rule, dict):
            if _globs_match(path, [rule.get("glob")]):
                return "material", rule.get("why", "material surface")
        elif _globs_match(path, [rule]):
            return "material", "material surface (policy.materiality.material_paths)"
    return "review", "not classified by policy; judge by the materiality tests in policy.yml"


def cmd_assess(repo: Repo, args):
    state = repo.ledger("state.yml")
    rng = args.range
    if not rng:
        anchor = str(state.get("incremental_anchor") or "")
        if anchor and repo.commit_exists(anchor):
            rng = f"{anchor}..HEAD"
        else:
            rng = "HEAD~1..HEAD" if repo.git("rev-list", "--count", "HEAD").strip() != "1" else "HEAD"
    print(f"history assess — range: {rng}")
    subjects = repo.git("log", "--format=%H %s", rng, check=False).strip().split("\n") if rng != "HEAD" else [repo.git("log", "-1", "--format=%H %s").strip()]
    subjects = [s for s in subjects if s]
    pats = [re.compile(p) for p in (repo.policy.get("materiality", {}).get("history_only_commit_patterns") or [])]
    files = set()
    if rng == "HEAD":
        files.update(repo.git("show", "--name-only", "--format=", "HEAD").split())
    elif subjects:
        files.update(repo.git("diff", "--name-only", rng, check=False).split())
    status = repo.git("status", "--porcelain", "-uall", check=False)
    uncommitted = [l[3:].strip('"') for l in status.split("\n") if l.strip()]
    if args.paths:
        files = set(args.paths)
    print(f"commits in range: {len(subjects)}")
    for s in subjects:
        sha, _, subj = s.partition(" ")
        tag = "history-only" if any(p.search(subj) for p in pats) else "review"
        print(f"  {sha[:12]} [{tag}] {subj}")
    material = []
    for f in sorted(files):
        cls, why = _material_classification(repo, f)
        print(f"  {cls:8} {f} — {why}")
        if cls == "material":
            material.append(f)
    if uncommitted:
        print("uncommitted work (present-tense, not history):")
        for f in uncommitted:
            cls, why = _material_classification(repo, f)
            print(f"  {cls:8} {f}")
    print()
    if material:
        print("assessment: candidate material surfaces touched — check the materiality tests in .project-history/policy.yml.")
        print("  if a purpose, promise, interface, architecture, deployment, licence or governance choice changed,")
        print("  add or amend an event capsule and declare `history:recorded <event-id>`;")
        print("  otherwise declare `history:none — <specific reason>`; emergencies may `history:defer — <item, owner, YYYY-MM-DD>`.")
    else:
        print("assessment: no policy-material surface touched; `history:none — <reason>` is probably right (heuristic only).")
    return 0


def cmd_context(repo: Repo, args):
    paths = args.paths or []
    print("# History context\n")
    orient = os.path.join(repo.docs_dir, "ORIENTATION.md")
    with open(orient, encoding="utf-8") as fh:
        text = fh.read()
    print(text.strip()[: args.max_chars] + ("\n…(truncated; read docs/history/ORIENTATION.md)" if len(text) > args.max_chars else ""))
    goals = repo.ledger("doctrine/goals.yml").get("goals", []) or []
    principles = repo.ledger("doctrine/principles.yml").get("principles", []) or []
    print("\n## Active goals")
    for g in goals:
        if g.get("status") in {"active", "proposed", "blocked", "narrowed", "expanded"}:
            print(f"- `{g['id']}` v{g.get('version')} [{g.get('status')}]: {str(g.get('statement', '')).strip()}")
    print("\n## Active principles")
    for p in principles:
        if p.get("status") in {"active", "weakened", "challenged"}:
            print(f"- `{p['id']}` v{p.get('version')} [{p.get('status')}]: {str(p.get('statement', '')).strip()}")
    print("\n## Relevant events")
    shown = 0
    for ev in repo.events():
        m = ev["meta"]
        scope = [str(s) for s in _as_list(m.get("scope"))] + [str(s) for s in _as_list(m.get("paths"))]
        if paths and not any(_globs_match(p, scope) or any(p.startswith(s.rstrip("*/")) for s in scope) or s in {"project", "*"} for p in paths for s in scope):
            continue
        shown += 1
        print(f"- `{m['id']}` ({m.get('kind')}, {m.get('significance')}, {m.get('occurred_at')}): {m.get('title')}")
        summary = m.get("summary")
        if summary:
            print(f"  {str(summary).strip()}")
    if not shown:
        print("- (no event matches these paths; read NARRATIVE.md)")
    contr = repo.ledger("contradictions.yml").get("contradictions", []) or []
    open_items = [x for x in contr if x.get("confidence") in {"plausible", "speculative", "unknown"}]
    if open_items:
        print("\n## Open disputes to keep in mind")
        for x in open_items:
            print(f"- `{x['id']}`: {str(x.get('disputed_claim', '')).strip()}")
    print("\nDeclare exactly one of `history:recorded <event-id>`, `history:none — <reason>`, `history:defer — <item, owner, deadline>` when done.")
    return 0


def cmd_audit(repo: Repo, args):
    state = repo.ledger("state.yml")
    related = repo.related_repo_paths()
    events = repo.events()
    claims = repo.ledger("claims.yml").get("claims", []) or []
    goals = repo.ledger("doctrine/goals.yml").get("goals", []) or []
    today = args.date or _dt.date.today().isoformat()
    hard, advisories, lines = [], [], []
    lines.append(f"# History audit report — {repo.policy.get('repository')}")
    lines.append("")
    lines.append(f"- Mode: {'full' if args.full else 'incremental since ' + args.since}")
    lines.append(f"- Audit date: {today}")
    head = repo.git("rev-parse", "HEAD").strip()
    lines.append(f"- HEAD: `{head}`")
    # anchors
    for key in ("full_audit_anchor", "incremental_anchor"):
        v = str(state.get(key) or "")
        if not repo.commit_exists(v):
            hard.append(f"state.yml {key} {v} is unreachable — ancestry rewritten or object missing; re-audit the affected range")
    cited = set()
    for ev in events:
        for s in _as_list(ev["meta"].get("anchors")):
            cited.add(str(s))
            if not repo.commit_exists(str(s), related):
                hard.append(f"event {ev['meta']['id']} anchor {s} unreachable")
    for c in claims:
        for s in HEX40.findall(str(c.get("locator", ""))):
            cited.add(s)
            if not repo.commit_exists(s, related):
                hard.append(f"claim {c['claim_id']} locator sha {s} unreachable")
    # refs drift
    refs_now = sorted(l.split()[0] for l in repo.git("for-each-ref", "--format=%(refname)").split("\n") if l.strip())
    refs_then = sorted(str(x) for x in _as_list(state.get("refs_examined")))
    new_refs = [r for r in refs_now if r not in refs_then]
    gone_refs = [r for r in refs_then if r not in refs_now]
    if new_refs:
        advisories.append("refs not present at last full audit: " + ", ".join(new_refs))
    if gone_refs:
        advisories.append("refs examined at last full audit that no longer exist: " + ", ".join(gone_refs))
    # divergence of tracking refs
    for r in refs_now:
        if r.startswith("refs/remotes/") and not r.endswith("/HEAD"):
            proc = subprocess.run(["git", "-C", repo.root, "merge-base", "--is-ancestor", r, "HEAD"], capture_output=True)
            proc2 = subprocess.run(["git", "-C", repo.root, "merge-base", "--is-ancestor", "HEAD", r], capture_output=True)
            if proc.returncode != 0 and proc2.returncode != 0:
                advisories.append(f"{r} and HEAD have diverged (possible rewritten remote history)")
            elif proc.returncode == 0 and repo.git("rev-parse", r).strip() != head:
                advisories.append(f"{r} is behind HEAD (local commits not on the remote-tracking ref)")
    # commit coverage
    if args.full:
        rng_commits = [l for l in repo.git("rev-list", "--all", "--format=%H%x1f%s", "--no-commit-header").split("\n") if l.strip()]
    else:
        if not repo.commit_exists(args.since):
            hard.append(f"--since anchor {args.since} is unreachable; cannot compute an incremental range (rewritten history?)")
            rng_commits = []
        else:
            rng_commits = [l for l in repo.git("rev-list", f"{args.since}..HEAD", "--format=%H%x1f%s", "--no-commit-header").split("\n") if l.strip()]
    pats = [re.compile(p) for p in (repo.policy.get("materiality", {}).get("history_only_commit_patterns") or [])]
    uncovered_material, covered, noise = [], 0, 0
    lines.append("")
    lines.append("## Commit coverage")
    lines.append("")
    lines.append("| Commit | Subject | Touches material surface | Cited by history | Classification |")
    lines.append("|---|---|---|---|---|")
    for entry in rng_commits:
        sha, _, subj = entry.partition("\x1f")
        files = repo.git("show", "--name-only", "--format=", sha).split()
        mat = [f for f in files if _material_classification(repo, f)[0] == "material"]
        is_hist = any(p.search(subj) for p in pats)
        is_cited = sha in cited
        if is_hist:
            cls = "history-only (ignored)"
            noise += 1
        elif is_cited:
            cls = "covered"
            covered += 1
        elif mat:
            cls = "UNCOVERED material — likely unrecorded change"
            uncovered_material.append((sha, subj))
        else:
            cls = "uncited, no material surface"
        lines.append(f"| `{sha[:12]}` | {subj.replace('|', '/')} | {', '.join(mat[:4]) or '—'} | {'yes' if is_cited else 'no'} | {cls} |")
    if uncovered_material:
        advisories.append(f"{len(uncovered_material)} commit(s) touch material surfaces but are cited by no event or claim")
    # stale goals / missing outcomes / deferrals
    for g in goals:
        if g.get("status") in {"active", "proposed"} and g.get("review_by") and str(g["review_by"]) < today:
            advisories.append(f"goal {g['id']} v{g.get('version')} is {g['status']} but its review_by {g['review_by']} has passed")
    for ev in events:
        m = ev["meta"]
        if m.get("status") == "open":
            advisories.append(f"event {m['id']} is still open — outcome not yet recorded")
        if "unknown" in str(m.get("observed_outcome", "")).lower():
            advisories.append(f"event {m['id']} records an unknown observed outcome")
    for d in repo.policy.get("deferrals", []) or []:
        if d.get("status", "open") == "open" and d.get("deadline") and str(d["deadline"]) < today:
            hard.append(f"deferral {d.get('id')} expired {d['deadline']} (owner {d.get('owner')})")
    lines.append("")
    lines.append(f"- Commits in range: {len(rng_commits)} · covered by history: {covered} · history-only: {noise} · uncovered material: {len(uncovered_material)}")
    lines.append("")
    lines.append("## Hard failures")
    lines.append("")
    lines += [f"- {h}" for h in hard] or ["- none"]
    lines.append("")
    lines.append("## Advisories")
    lines.append("")
    lines += [f"- {a}" for a in advisories] or ["- none"]
    lines.append("")
    report = "\n".join(lines)
    print(report)
    if args.report:
        with open(os.path.join(repo.root, args.report), "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"(report written to {args.report})")
    return 1 if hard else 0


# --------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="project_history", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="project root (default: parent of the scripts directory)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("assess")
    a.add_argument("range", nargs="?")
    a.add_argument("paths", nargs="*")
    c = sub.add_parser("context")
    c.add_argument("paths", nargs="*")
    c.add_argument("--max-chars", type=int, default=6000)
    v = sub.add_parser("validate")
    v.add_argument("--no-render-check", action="store_true")
    v.add_argument("--today", default=None)
    r = sub.add_parser("render")
    r.add_argument("--check", action="store_true", help="exit 1 if rendering would change anything")
    au = sub.add_parser("audit")
    g = au.add_mutually_exclusive_group(required=True)
    g.add_argument("--full", action="store_true")
    g.add_argument("--since", metavar="ANCHOR")
    au.add_argument("--report", default=None, help="write the report to this path (relative to root)")
    au.add_argument("--date", default=None, help="audit date YYYY-MM-DD (default: today)")
    d = sub.add_parser("declaration")
    d.add_argument("--text", default=None)
    d.add_argument("--file", default=None)
    args = ap.parse_args(argv)
    if args.cmd == "declaration":
        text = args.text if args.text is not None else (open(args.file, encoding="utf-8").read() if args.file else "")
        try:
            res = parse_declaration(text)
        except ValueError as exc:
            print(f"declaration INVALID: {exc}")
            return 1
        print(f"declaration OK: history:{res['kind']} — {res['detail']}")
        return 0
    root = args.root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        repo = Repo(root)
    except YamlError as exc:
        print(f"error: policy.yml is not valid: {exc}")
        return 1
    if args.cmd == "validate":
        try:
            val = Validator(repo, today=args.today).run(check_render=not args.no_render_check)
        except YamlError as exc:
            print(f"error: ledger is not valid YAML subset: {exc}")
            print("validate: 1 error(s), 0 warning(s)")
            return 1
        for w in val.warnings:
            print(f"warning: {w}")
        for e in val.errors:
            print(f"error: {e}")
        print(f"validate: {len(val.errors)} error(s), {len(val.warnings)} warning(s)")
        return 1 if val.errors else 0
    if args.cmd == "render":
        changed = Renderer(repo).render(write=not args.check)
        rel = [os.path.relpath(p, repo.root) for p in changed]
        if args.check:
            print("render --check: " + ("clean" if not rel else "DRIFT in " + ", ".join(rel)))
            return 1 if rel else 0
        print("render: " + ("no changes" if not rel else "updated " + ", ".join(rel)))
        return 0
    if args.cmd == "assess":
        return cmd_assess(repo, args)
    if args.cmd == "context":
        return cmd_context(repo, args)
    if args.cmd == "audit":
        return cmd_audit(repo, args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
