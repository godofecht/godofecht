#!/usr/bin/env python3
"""Render the repo constellation as two static SVGs (light and dark).

Nodes are public repos, sized by stars, coloured by the section they belong to
in spine.py. Edges join repos that share a topic. Layout is a small
force-directed simulation, stdlib only, seeded so the picture is stable.
"""
import json, math, os, random, subprocess, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
spine = load('spine', 'spine.py')

W, H = 1280, 360
PAD = 30

PALETTE = {
    "Flow":                                    ("#7c5cff", "#a08bff"),
    "Build systems":                           ("#0f9d58", "#3ddc84"),
    "Reproducible scientific tooling":         ("#d1495b", "#ff7b8c"),
    "Audio and real-time":                     ("#e08d1a", "#ffb545"),
    "Machine intelligence":                    ("#1b7fd4", "#57b0f5"),
    "Graphics and things that look like something": ("#00a3a3", "#2fd4d4"),
    "Tools and systems":                       ("#6e7b8b", "#93a1b3"),
    "_other":                                  ("#9aa4b2", "#5c6672"),
}
ORDER = [s[0] for s in spine.SECTIONS]

def fetch():
    out = []
    for owner in ("godofecht", "flooooooooooow"):
        r = subprocess.run(["gh","repo","list",owner,"--limit","300","--json",
                            "name,isPrivate,isFork,isArchived,stargazerCount,repositoryTopics,description"],
                           capture_output=True, text=True, check=True)
        for x in json.loads(r.stdout):
            if x["isPrivate"] or x["isFork"]: continue
            if x["name"] == "godofecht": continue
            out.append({"full": f'{owner}/{x["name"]}', "name": x["name"],
                        "stars": x["stargazerCount"],
                        "topics": {t["name"] for t in (x.get("repositoryTopics") or [])}})
    return out

TOPIC_MAP = [
    ("Flow", {"flow-language"}),
    ("Build systems", {"build-system","build-tool","azazel-parity","azazel","zaza","cmake",
                       "package-manager","cross-compilation","deterministic-builds","cue","build-cache"}),
    ("Reproducible scientific tooling", {"reproducibility","research","scientific-computing","peer-review",
                       "corpus-analysis","research-integrity","statistics","determinism","citations",
                       "bibliography","openalex","crossref","arxiv","computational-neuroscience","public-health"}),
    ("Audio and real-time", {"audio","dsp","vst3","audio-plugin","juce","juce-framework","maxmsp","max4live",
                       "audio-dev","audio-effect","music","midi","speech-synthesis","dafx","freesound",
                       "audioreactive","synthesizer","real-time","guitar-pedal","audio-ui","isobar",
                       "algorithmic-composition","captions","transcription"}),
    ("Machine intelligence", {"machine-learning","neural-network","nlp","agents","llm","genetic-algorithm",
                       "neuroevolution","neat","hyperneat","stance-detection","bert","roberta","ocr-recognition",
                       "cyclegan","timbre-transfer","generative-adversarial-networks","style-transfer",
                       "reinforcement-learning","perceptron","embeddings","tfidf","edge-computing",
                       "unsupervised-learning","slow-feature-analysis","stereo-vision","disparity",
                       "agent-based-simulation","backpropagation","memory","qwen","claude"}),
    ("Graphics and things that look like something", {"graphics","shaders","glsl","metal","slang","generative-art",
                       "game","gamedev","game-engine","godot","processing","visuals","livecoding","hydra",
                       "voxel","raylib","procedural-generation","noise","texture","dataviz","webgl",
                       "graph-visualization","terminal","animation","ascii-art","tui","album-art","mandala",
                       "creative-coding","watch-faces","2d","topdownshooter","dungeon-crawler","simulation"}),
    ("Tools and systems", {"cli","packaging","pypi","release-automation","automation","setup","dotfiles",
                       "ssh","git","browser","chromium","patch","tabs","printing","cups","printer","hardware",
                       "dymo-labelwriter","literate-programming","documentation","tooling","cache",
                       "computer-architecture","simulator","education","file-conversion","privacy","web",
                       "browser-extension","networking","diagnostics","homebrew","homebrew-tap","macos",
                       "awesome-list","resources","interview-questions","algorithms","api-client",
                       "discord-bot","spotify","finance","fintech","flask","streaming","video","video-processing",
                       "ffmpeg","unity","satellite","engineering","qtcreator","gui","imgui","example",
                       "monorepo","submodules","index","marketing","website","minecraft","computercraft"}),
]

def section_of(full, topics=frozenset()):
    for title, _blurb, repos in spine.SECTIONS:
        if any(r[0] == full for r in repos): return title
    if full.startswith("godofecht/azazel-parity"): return "Build systems"
    if full.startswith("flooooooooooow/"): return "Flow"
    best, score = "_other", 0
    for title, keys in TOPIC_MAP:
        n = len(topics & keys)
        if n > score: best, score = title, n
    return best

def layout(nodes, edges, seed=11):
    """Force layout with an explicit per-section band, so the picture reads as groups."""
    rnd = random.Random(seed)
    bands = {t: i for i, t in enumerate(ORDER)}
    NB = len(ORDER) + 1
    def band_x(sec):
        b = bands.get(sec, len(ORDER))
        return PAD + 40 + (b + 0.5) * (W - 2*PAD - 80) / NB
    for nd in nodes:
        nd["bx"] = band_x(nd["section"])
        nd["x"] = nd["bx"] + rnd.uniform(-30, 30)
        nd["y"] = H/2 + rnd.uniform(-60, 60)
        nd["vx"] = nd["vy"] = 0.0
    idx = {nd["full"]: i for i, nd in enumerate(nodes)}
    E = [(idx[a], idx[b]) for a, b in edges if a in idx and b in idx]
    TOP, BOT = PAD + 12, H - PAD - 18
    for step in range(900):
        k = 1.0 - 0.85 * step/900
        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                dx, dy = a["x"]-b["x"], a["y"]-b["y"]
                d2 = dx*dx + dy*dy + 0.01
                if d2 > 30000: continue
                d = math.sqrt(d2)
                f = 1100.0 / d2
                a["vx"] += f*dx/d; a["vy"] += f*dy/d
                b["vx"] -= f*dx/d; b["vy"] -= f*dy/d
        for i, j in E:
            a, b = nodes[i], nodes[j]
            dx, dy = b["x"]-a["x"], b["y"]-a["y"]
            d = math.hypot(dx, dy) + 0.01
            f = (d - 54) * 0.016
            a["vx"] += f*dx/d; a["vy"] += f*dy/d
            b["vx"] -= f*dx/d; b["vy"] -= f*dy/d
        for nd in nodes:
            nd["vx"] -= (nd["x"] - nd["bx"]) * 0.010      # hold the section band
            nd["vy"] -= (nd["y"] - H/2) * 0.0085           # hold the vertical centre
            nd["x"] += max(-7, min(7, nd["vx"] * k))
            nd["y"] += max(-7, min(7, nd["vy"] * k))
            nd["vx"] *= 0.80; nd["vy"] *= 0.80
            nd["x"] = max(PAD, min(W-PAD, nd["x"]))
            nd["y"] = max(TOP, min(BOT, nd["y"]))
    place_labels(nodes)
    return nodes

def place_labels(nodes):
    """Put each label above its node, flipping below when that box is taken."""
    taken = []
    def clash(box):
        x0,y0,x1,y1 = box
        return any(not (x1 < b[0] or x0 > b[2] or y1 < b[1] or y0 > b[3]) for b in taken)
    for nd in sorted((n for n in nodes if n["label"]), key=lambda n: -n["stars"]):
        w = len(nd["name"]) * 6.7
        r = radius(nd["stars"])
        for dy in (-r-8, r+15, -r-21, r+28):
            cy = nd["y"] + dy
            box = (nd["x"]-w/2-3, cy-10, nd["x"]+w/2+3, cy+3)
            if not clash(box) and 10 < cy < H-24:
                nd["ly"] = cy; taken.append(box); break
        else:
            nd["ly"] = nd["y"] - r - 8
            taken.append((nd["x"]-w/2-3, nd["ly"]-10, nd["x"]+w/2+3, nd["ly"]+3))

def radius(stars): return 3.0 + min(7.0, math.sqrt(stars) * 2.4)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def render(nodes, edges, dark):
    bg   = "#0d1117" if dark else "#ffffff"
    edge = "#2b3440" if dark else "#d5dbe4"
    text = "#c9d1d9" if dark else "#3a4149"
    idx  = {nd["full"]: nd for nd in nodes}
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Repository constellation">',
         f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         '<g stroke-linecap="round">']
    for a, b in edges:
        if a not in idx or b not in idx: continue
        A, B = idx[a], idx[b]
        p.append(f'<line x1="{A["x"]:.1f}" y1="{A["y"]:.1f}" x2="{B["x"]:.1f}" y2="{B["y"]:.1f}" stroke="{edge}" stroke-width="0.9"/>')
    p.append('</g>')
    for nd in nodes:
        c = PALETTE.get(nd["section"], PALETTE["_other"])[0 if not dark else 1]
        p.append(f'<circle cx="{nd["x"]:.1f}" cy="{nd["y"]:.1f}" r="{radius(nd["stars"]):.1f}" fill="{c}" fill-opacity="{0.95 if nd["label"] else 0.72:.2f}"/>')
    fam = "ui-monospace,SFMono-Regular,Menlo,monospace"
    for nd in nodes:
        if not nd["label"]: continue
        c = PALETTE.get(nd["section"], PALETTE["_other"])[0 if not dark else 1]
        p.append(f'<text x="{nd["x"]:.1f}" y="{nd.get('ly', nd["y"]):.1f}" font-family="{fam}" '
                 f'font-size="11" fill="{text}" text-anchor="middle" '
                 f'stroke="{bg}" stroke-width="3.5" paint-order="stroke">{esc(nd["name"])}</text>')
    lx = PAD
    for t in ORDER:
        c = PALETTE[t][0 if not dark else 1]
        short = {"Reproducible scientific tooling":"research tooling",
                 "Graphics and things that look like something":"graphics",
                 "Audio and real-time":"audio","Machine intelligence":"ML",
                 "Build systems":"build systems","Flow":"flow",
                 "Tools and systems":"tools"}[t]
        p.append(f'<circle cx="{lx+4}" cy="{H-16}" r="4" fill="{c}"/>')
        p.append(f'<text x="{lx+14}" y="{H-12}" font-family="{fam}" font-size="10.5" fill="{text}" fill-opacity="0.8">{short}</text>')
        lx += 22 + len(short) * 6.4
    p.append('</svg>')
    return "\n".join(p)

def main():
    repos = fetch()
    featured = {r[0] for _t, _b, rs in spine.SECTIONS for r in rs}
    nodes = []
    for r in repos:
        r["section"] = section_of(r["full"], r["topics"])
        r["label"] = r["full"] in featured and r["stars"] >= 0 and r["full"] in featured
        nodes.append(r)
    # label only the six pins plus flowrat and wfdl-gallery, or the picture turns to soup
    LABEL = {"flooooooooooow/flow","godofecht/flow-scikit","godofecht/azazel",
             "godofecht/perturbation-kernel","godofecht/danzig","godofecht/tinyML",
             "godofecht/zaza","godofecht/flowrat","godofecht/citeverify","godofecht/wfdl-gallery"}
    for nd in nodes: nd["label"] = nd["full"] in LABEL
    edges = []
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            shared = a["topics"] & b["topics"]
            if len(shared) >= 2 or (a["section"] == b["section"] and len(shared) >= 1):
                edges.append((a["full"], b["full"]))
    layout(nodes, edges)
    out = os.path.join(HERE, "assets"); os.makedirs(out, exist_ok=True)
    for dark in (False, True):
        f = os.path.join(out, f'graph-{"dark" if dark else "light"}.svg')
        open(f, "w").write(render(nodes, edges, dark))
        print("wrote", f, os.path.getsize(f), "bytes")
    print(f"{len(nodes)} nodes, {len(edges)} edges")

if __name__ == "__main__":
    main()
