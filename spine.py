# The hand-written part of the profile. Everything else is pulled live.
# Rules: no em dashes, no "X, not Y", no rhetorical triples. One hard fact per line.

INTRO = """Compilers, build systems, real-time audio and computational neuroscience.
Cambridge, UK. Founder of [Quilio](https://www.quilio.dev).
Neuroscience at the University of Cambridge, music technology at Birmingham Conservatoire."""

# section title, blurb, [(owner/repo, one-line fact or None to use the live description)]
SECTIONS = [
("Flow",
 "Flow is a statically typed, compiled systems language for programs that evolve through time. "
 "Version 1.0 freezes a small production core around the self-hosted `flowc` compiler and a portable C "
 "backend. `brew tap flooooooooooow/flow && brew install flow`. Most of what I am building now runs through it.",
 [("flooooooooooow/flow",        "The language, the self-hosted `flowc` compiler and the standard library. MIT, at 1.0.2."),
  ("godofecht/flow-scikit",      "scikit-learn rebuilt in Flow. A 1.4 MB native binary with no Python runtime."),
  ("godofecht/flowrat",          "Rat navigation and hippocampal dynamics in real time. The arena is editable while the simulation runs."),
  ("godofecht/doom-flow",        "The Doom engine, ported."),
  ("godofecht/flow-euler",       "Project Euler used as a compiler test suite."),
  ("flooooooooooow/flow-kernel", "Flow on a Tiny Core Linux base, with cgroups, perf and eBPF underneath.")]),

("Build systems",
 "Two build systems that answer the same question differently. `azazel` states a build as a CUE model and "
 "generates Zig from it. `zaza` drives the graph from Zig directly.",
 [("godofecht/azazel", "CUE model in, deterministic Zig build out. No JSON runtime, no flags."),
  ("godofecht/zaza",   "C, C++, Zig, CMake interop and WebAssembly, driven from Zig."),
  ("godofecht/azazel-cache", "Content-addressed artifact cache, using GitHub Releases as the store.")]),

("Reproducible scientific tooling",
 "Tools for making a result checkable by someone who is not you.",
 [("godofecht/perturbation-kernel", "Scalar, SIMD and GPU backends that agree bit for bit. Rust core, five language bindings, on PyPI and crates.io."),
  ("godofecht/citeverify",          "Checks every reference in a bibliography against eight bibliographic indexes. Reads BibTeX, RIS, CSL-JSON, .bbl, .docx and PDF."),
  ("godofecht/refereed",            "A reviewer panel for a manuscript, running on your own model key."),
  ("godofecht/corpus-lens",         "TF-IDF keywords, rhetorical fingerprints and embeddings across a whole corpus."),
  ("godofecht/tilekiln",            "Procedural texture synthesis with measured parameter stability.")]),

("Audio and real-time",
 "Audio has been the continuous thread. Product work runs through [Quilio](https://www.quilio.dev).",
 [("godofecht/danzig", "The VST3 C ABI implemented directly in Zig, as extern structs of callconv(.c) function pointers. No JUCE, no Steinberg SDK."),
  ("godofecht/tinyML", "A C++ machine-learning and statistics library for embedded and real-time workloads."),
  ("godofecht/isobarcpp", "Daniel Jones' isobar algorithmic music library, in C++."),
  ("godofecht/Analog-Fattener", "An analog fattener effect in JUCE."),
  ("godofecht/Wobblefet", "Pink Trombone, the interactive vocal tract synthesizer, modified.")]),

("Machine intelligence",
 "Learning systems and agent infrastructure, going back to networks written from scratch.",
 [("godofecht/Fractal-Memory-Network", "Recursive memory structure for long-running agents."),
  ("godofecht/safe-yolo-agent",        "Allowlist permissions for an autonomous coding agent, so destructive calls cannot run unreviewed."),
  ("godofecht/CycleGAN-Timbre-Transfer", "Timbre transfer through a modified cycle-consistent adversarial network."),
  ("godofecht/Eye-Evolution",          "Predator-prey eye evolution, using perceptrons and a genetic algorithm."),
  ("godofecht/Disparity-Network",      "Depth from binocular image pairs."),
  ("godofecht/Slow-Feature-Analysis",  "Stone and Bray's Slow Feature Analysis, implemented.")]),

("Graphics and things that look like something",
 None,
 [("godofecht/wfdl-gallery",   "A watch dial written as text. 58 faces across seven families, compiled from a small description language."),
  ("godofecht/Shadow",         "A 2D game engine kept small enough to read."),
  ("godofecht/ShaderLibrary",  "GLSL, Metal and Slang fragment shaders."),
  ("godofecht/cosmographs",    "The graph at the top of this page. Every repo here, rendered on the GPU."),
  ("godofecht/terminal-eye-candy", "Zero-dependency terminal animations in Python."),
  ("godofecht/Hydra-Sketches", "Audio-reactive livecoding for the Hydra video synth.")]),

("Tools and systems",
 "Smaller things that exist because something was annoying.",
 [("godofecht/chromium-tabscroll", "Horizontal tab scrolling for Chromium, rewritten against HEAD after Google removed it in M144."),
  ("godofecht/lpmd",               "LitPro: executable literate programming for any language."),
  ("godofecht/l1-cache-simulator", "An L1 cache simulator that shows hits, misses and eviction policy as they happen."),
  ("godofecht/pypi-toolkit",       "Builds, tests and uploads Python packages."),
  ("godofecht/PrintingCPP",        "Talking to CUPS printers from C++."),
  ("godofecht/DYMO-Labelwriter-App", "Old DYMO label printers brought back into use.")]),
]

# Rendered as one line rather than twelve cards.
PARITY_NOTE = (
"Twelve real third-party projects, each built twice, once with `azazel` and once with `zaza`: "
"SQLite, ghostty, libxev, libvaxis, tigerbeetle, zls, river, mach, microzig, capy, zig-gamedev, "
"and the Zig compiler's own tokenizer. "
"[All twelve](https://github.com/search?q=owner%3Agodofecht+topic%3Aazazel-parity&type=repositories)")

LINKS = [
 ("Portfolio",  "https://godofecht.github.io",     "godofecht.github.io"),
 ("Site",       "https://abhishek-shivakumar.com", "abhishek--shivakumar.com"),
 ("Flow",       "https://flooooooooooow.github.io/flow/", "Language"),
 ("Quilio",     "https://www.quilio.dev",          "Audio%20software"),
 ("LinkedIn",   "https://www.linkedin.com/in/abhishek-shivakumar-899182a6/", "Abhishek%20Shivakumar"),
]

CLOSER = "The through line is asking how much of a stack stays necessary once you are willing to change the abstraction underneath it."
