---
name: book-s2tw
description: Batch-converts book/ content (chapters, intro, afterword, and the .tex/.lua/.py generator scripts) from Simplified to Traditional Chinese using OpenCC's s2tw config. Use when new or edited text under book/ contains Simplified Chinese, or when asked to convert book content to Traditional Chinese.
---

Pure rule-based `s2tw` (Simplified → Traditional, Taiwan standard) conversion, no LLM rewriting — reproduces the conversion in PR #1 (`chore: 全書簡體轉繁體`), verified byte-for-byte by re-running `s2tw` on the pre-conversion source (commit `cad8657`) and diffing against the current `book/chapter1.md`, `chapter5.md`, `introduction.md`, `gen_ch3_figs.py` — zero diff on all four.

## Setup

```
pip install opencc-python-reimplemented
```

Use this Python binding, not the Homebrew `opencc` CLI. The CLI's bundled dictionary is newer and converts a few extra phrases (e.g. `想象`→`想像`) that the book's existing Traditional text still has in the older, uncorrected form — running the CLI on old files reintroduces a diff against established style. The pip package matches what's already in the repo.

## Steps

1. Identify targets: `book/*.md`, `book/*.tex`, `book/*.lua`, `book/*.py` files that are new or were just edited to add Simplified Chinese text. Skip files that are already fully Traditional — `s2tw` is one-directional; running it on Traditional input desyncs its phrase dictionary and spuriously flips ambiguous characters (了/瞭, 干/幹, 系/繫).
2. Convert each target in place:
   ```python
   from opencc import OpenCC
   cc = OpenCC('s2tw')
   path = "book/chapterX.md"
   text = open(path, encoding="utf-8").read()
   open(path, "w", encoding="utf-8").write(cc.convert(text))
   ```
   Pin `s2tw` exactly — not `s2twp` (adds PRC→Taiwan vocabulary substitution beyond character mapping, e.g. 软件→軟體) and not plain `s2t` (skips the Taiwan variant pass).
3. Verify per file: `git diff --numstat` — insertions must equal deletions (only characters swap, no lines added or removed). Then eyeball `git diff` — only CJK text should change; code identifiers, code-block contents, and URLs pass through untouched automatically since OpenCC only remaps CJK codepoints.
4. Done when every touched file has symmetric numstat and no non-CJK lines in the diff.

## Don't

- Don't write markdown/code-fence-aware skipping logic — OpenCC already leaves non-CJK text alone; that logic would duplicate what the tool does for free.
- Don't run `s2tw` on text that's already Traditional.
- Don't use an LLM for the character substitution — this step is mechanical and deterministic by design.
