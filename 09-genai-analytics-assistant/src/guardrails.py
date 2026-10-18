"""SQL guardrails applied to every generated query, whichever generator produced it."""
import re

ALLOWED_TABLES = {"sales", "customers"}
PII_COLUMNS = {"email", "phone", "name"}
FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|merge|grant|attach|pragma)\b", re.I)
INJECTION = re.compile(r"ignore (all |previous |prior )?instructions|system prompt|you are now", re.I)


class GuardrailError(Exception):
    pass


def check_question(question: str):
    if INJECTION.search(question):
        raise GuardrailError("G-7: possible prompt injection")
    if re.search(r"\b(email|e-mail|phone|address(es)?)\b", question, re.I):
        raise GuardrailError("G-3: personal data is not available through the assistant")
    if FORBIDDEN.search(question) or re.search(r"\binsert\b", question, re.I):
        raise GuardrailError("G-1: the assistant is read-only")


def enforce(sql: str, row_filter: str | None = None, limit: int = 1000) -> str:
    s = sql.strip().rstrip(";")
    if ";" in s:
        raise GuardrailError("G-1: multiple statements")
    if not re.match(r"^\s*select\b", s, re.I) or FORBIDDEN.search(s):
        raise GuardrailError("G-1: only SELECT statements are allowed")
    tables = set(t.lower() for t in re.findall(r"\b(?:from|join)\s+([a-zA-Z_][\w.]*)", s, re.I))
    if not tables <= ALLOWED_TABLES:
        raise GuardrailError(f"G-2: table not allowed: {tables - ALLOWED_TABLES}")
    if any(re.search(rf"\b{c}\b", s, re.I) for c in PII_COLUMNS):
        raise GuardrailError("G-3: PII column requested")
    if row_filter:  # G-5: row-level security predicate
        if re.search(r"\bwhere\b", s, re.I):
            s = re.sub(r"\bwhere\b", f"WHERE ({row_filter}) AND", s, count=1, flags=re.I)
        else:
            s = re.sub(r"(\bgroup by\b|\border by\b|\blimit\b|$)", f" WHERE {row_filter} \\1", s, count=1, flags=re.I)
    if not re.search(r"\blimit\s+\d+", s, re.I):  # G-4
        s += f" LIMIT {limit}"
    return s
