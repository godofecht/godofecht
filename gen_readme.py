#!/usr/bin/env python3
"""Rebuild README.md for the profile repo from spine.py plus live repo data.

Nothing here is hand-edited after the fact. Edit spine.py, run this, commit.
"""
import json, os, subprocess, sys, importlib.util, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('spine', os.path.join(HERE, 'spine.py'))
spine = importlib.util.module_from_spec(spec); spec.loader.exec_module(spine)

REPO_DIR = os.environ.get("PROFILE_REPO", os.path.join(HERE, "profile"))

def live():
    d = {}
    for owner in ("godofecht", "flooooooooooow"):
        r = subprocess.run(["gh","repo","list",owner,"--limit","300","--json",
                            "name,isPrivate,isFork,stargazerCount,description,primaryLanguage,homepageUrl"],
                           capture_output=True, text=True, check=True)
        for x in json.loads(r.stdout):
            if x["isPrivate"] or x["isFork"]: continue
            d[f'{owner}/{x["name"]}'] = x
    return d

def badge(label, url, right):
    lab = label.replace("-", "--").replace(" ", "%20")
    return f'[![{label}](https://img.shields.io/badge/{lab}-{right}-0d1117?style=flat-square)]({url})'

def main():
    L = live()
    missing = [f for _t,_b,rs in spine.SECTIONS for f,_ in rs if f not in L]
    if missing:
        print("WARNING: featured repo not public:", missing, file=sys.stderr)

    o = []
    o.append('<div align="center">')
    o.append('  <picture>')
    o.append('    <source media="(prefers-color-scheme: dark)" srcset="assets/graph-dark.svg">')
    o.append('    <img src="assets/graph-light.svg" alt="Every public repository in this account, joined where they share a topic" width="100%">')
    o.append('  </picture>')
    o.append('</div>')
    o.append('')
    o.append('# Abhishek Shivakumar')
    o.append('')
    o.append(spine.INTRO)
    o.append('')
    o.append(' '.join(badge(l, u, r) for l, u, r in spine.LINKS))
    o.append('')

    for title, blurb, repos in spine.SECTIONS:
        o.append(f'## {title}')
        o.append('')
        if blurb:
            o.append(blurb)
            o.append('')
        for full, fact in repos:
            x = L.get(full)
            if not x:
                continue
            name = full.split("/")[1]
            stars = x["stargazerCount"]
            star = f' `{stars}★`' if stars >= 3 else ''
            line = fact or x["description"] or ""
            o.append(f'- **[{name}](https://github.com/{full})**{star} {line}')
        o.append('')
        if title == "Build systems":
            o.append(spine.PARITY_NOTE)
            o.append('')

    o.append('---')
    o.append('')
    o.append(spine.CLOSER)
    o.append('')
    featured = {f for _t,_b,rs in spine.SECTIONS for f,_ in rs}
    o.append(f'There are {len(L)} public repositories here in total. '
             f'The {len(L)-len(featured)} not listed above are mostly older. '
             f'[All of them](https://github.com/godofecht?tab=repositories).')
    o.append('')
    o.append(f'<sub>Page rebuilt from live repository data on {datetime.date.today().isoformat()}.</sub>')

    text = "\n".join(o) + "\n"
    for bad, why in (("—","em dash"), ("–","en dash"), ("’","curly apostrophe"), ("“","curly quote")):
        if bad in text:
            print(f"REFUSING: output contains a {why}", file=sys.stderr); sys.exit(1)

    out = os.path.join(REPO_DIR, "README.md")
    os.makedirs(REPO_DIR, exist_ok=True)
    open(out, "w").write(text)
    print(f"wrote {out}  ({len(text)} bytes, {len(text.splitlines())} lines)")

if __name__ == "__main__":
    main()
