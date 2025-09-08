\
    import re, hashlib
    HEADING_RE = re.compile(r"(?m)^\s*(?:>\s*)*(?:\\)?#{1,6}\s+(?:\d+\.\s*)?(?P<title>.+?)\s*$")
    GLOBAL_TITLES = [
        "Router — Query-Pattern Matrix","Query-Pattern Matrix","Unified Risk","Unified Risk & Control Model",
        "Standard Development Environment","Agent Query Index","High-Level Risk",
    ]
    def normalize_text(txt: str) -> str:
        t = txt.lower()
        t = re.sub(r"[\s\|`*_:>\-]+", "", t)
        return t
    def paragraph_iter(md: str):
        lines = md.splitlines()
        buf, start = [], 1
        line_no = 1
        for line in lines + [""]:
            if line.strip() == "":
                if buf:
                    yield "\n".join(buf), start, line_no-1
                    buf = []
                start = line_no + 1
            else:
                buf.append(line)
            line_no += 1
    def heading_iter(md: str):
        for m in HEADING_RE.finditer(md):
            yield m.group("title"), md[:m.start()].count("\n")+1
    def sha256_norm(txt: str) -> str:
        return hashlib.sha256(normalize_text(txt).encode("utf-8")).hexdigest()
    def looks_like_aqi_table(para: str) -> bool:
        pn = normalize_text(para)
        if "agentqueryindex" in pn:
            if "|" in para or "Route" in para or "Ch." in para or "Positive" in para:
                return True
        return False
