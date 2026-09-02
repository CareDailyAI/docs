# -*- coding: utf-8 -*-
"""Tag every unlabelled code fence with a language so GitHub highlights it.

Around 150 fenced blocks across the repository carry no language, so every JSON payload in the
documentation renders as flat grey text. Tagging them is the single largest readability win
available and it changes no prose.

Language is inferred from the content rather than guessed:
  * starts with { or [            -> json   (pseudo-JSON with Python True/None still highlights
                                             usefully, and GitHub does not error on it)
  * an HTTP verb and a path       -> http
  * key: value shaped lines only  -> yaml
  * otherwise                     -> text   (never left bare, so the intent is explicit)

Fences inside a block already tagged are left alone, and so is anything already labelled.
"""
import glob
import io
import json
import re

VERB = re.compile(r"^\s*(GET|POST|PUT|PATCH|DELETE|HEAD)\s+\S", re.M)
KV = re.compile(r"^[A-Za-z_][A-Za-z0-9_.\-]*\s*:\s*\S")


def sniff(body):
    s = body.strip()
    if not s:
        return "text"
    if s[0] in "{[":
        return "json"
    if VERB.search(s):
        return "http"
    try:
        json.loads(s)
        return "json"
    except Exception:
        pass
    lines = [l for l in s.split("\n") if l.strip()]
    if lines and sum(1 for l in lines if KV.match(l)) >= max(2, len(lines) * 0.6):
        return "yaml"
    return "text"


def main():
    total = 0
    per = {}
    for f in sorted(glob.glob("**/*.md", recursive=True)):
        src = io.open(f, encoding="utf-8").read()
        out = []
        i = 0
        n = 0
        parts = src.split("```")
        # even indices are outside fences, odd indices are fence bodies (with their info string)
        for k, part in enumerate(parts):
            if k % 2 == 0:
                out.append(part)
                continue
            nl = part.find("\n")
            info = part[:nl] if nl != -1 else ""
            if info.strip():                      # already labelled
                out.append(part)
                continue
            body = part[nl + 1:] if nl != -1 else ""
            lang = sniff(body)
            out.append(lang + part)
            n += 1
        if n:
            io.open(f, "w", encoding="utf-8").write("```".join(out))
            per[f] = n
            total += n
    for f in sorted(per):
        print("  %-56s %3d" % (f, per[f]))
    print("\ntagged %d fences across %d files" % (total, len(per)))


if __name__ == "__main__":
    main()
