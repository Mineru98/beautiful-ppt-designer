---
name: typst
description: >
  Use this skill whenever the user wants to create presentations, slide decks, or beautiful PPT files
  using Typst. Triggers include: any mention of 'Typst', '.typ', 'PPT', 'presentation', 'slide deck',
  'beautiful slides', or requests to create professional presentations. Also triggers when user has
  a PDF or document they want to turn into a presentation, or when they mention 'beautiful-ppt'.
  This skill handles the COMPLETE workflow: content analysis via NotebookLM, design style selection,
  Typst slide generation with visual verification, and final PPT export.
  Use this skill even if the user just says "make me a presentation" or "프레젠테이션 만들어줘".
  Do NOT use for simple document typesetting without slides - use a simpler typst workflow for that.
---

# Beautiful-PPT: Typst Presentation Creation Skill

Create stunning, professional presentations from any source material. This skill handles the complete
pipeline from content analysis to final PPT export, with built-in design system and visual quality verification.

## Prerequisites

### Typst Installation
```bash
# macOS
brew install typst

# Linux
cd /tmp && curl -sL "https://github.com/typst/typst/releases/download/v0.14.2/typst-x86_64-unknown-linux-musl.tar.xz" -o typst.tar.xz && tar -xf typst.tar.xz && cp typst-x86_64-unknown-linux-musl/typst /usr/local/bin/
```
If `which typst` succeeds, skip installation.

### Python Dependencies
```bash
pip install python-pptx
```

### NotebookLM CLI (Required for PDF source analysis)
```bash
npm install -g notebooklm-cli
# Binary is installed as 'nlm-cli'
# Verify: nlm-cli --version
```

## Complete Workflow

Follow these steps in order. The workflow is designed to produce high-quality results through
structured content analysis, thoughtful design selection, and rigorous visual verification.

### Phase 1: Content Analysis via NotebookLM

If the user provides a PDF or document as source material:

1. **Compile source to PDF** (if typst source):
   ```bash
   typst compile source.typ source.pdf
   ```

2. **Create NotebookLM notebook** from the source:
   - Use the notebooklm skill at `.claude/skills/notebooklm/`
   - All scripts MUST be run via: `python scripts/run.py [script]`
   - Check auth: `python scripts/run.py auth_manager.py status`
   - The user needs to manually upload the PDF to NotebookLM
   - Add notebook to library after upload

3. **Extract key content** by querying the notebook:
   ```bash
   python scripts/run.py ask_question.py --question "Summarize the main topics, key points, and structure of this document. List all major sections and their key takeaways." --notebook-url "[URL]"
   ```

4. **Follow-up queries** to fill gaps in understanding before proceeding to slide creation.

### Phase 2: User Configuration (AskUserQuestion)

Use the `AskUserQuestion` tool to gather user preferences BEFORE creating slides.

**Question 1: Page Count**
```
Ask the user how many slides they want:
- "10 슬라이드 (간결한 요약)" - Concise summary
- "15 슬라이드 (표준 발표)" - Standard presentation
- "20 슬라이드 (상세 발표)" - Detailed presentation
- Other (custom number input)
```

**Question 2: Design Style Selection**
Read the design vocabulary from `assets/design-vocabulary.json` and present styles to the user.
Each option should show:
- Style name (Korean + English)
- Brief mood description
- The style's visual characteristics

Present as selectable options with previews showing the color palette:
```
Available styles:
1. 미니멀 클린 / Minimal Clean - "Calm professionalism"
2. 코퍼레이트 모던 / Corporate Modern - "Balanced and authoritative"
3. 그라디언트 플로우 / Gradient Flow - "Energetic and contemporary"
4. 다크 엘레건트 / Dark Elegant - "Sophisticated and premium"
5. 네이처 오가닉 / Nature Organic - "Warm and approachable"
6. 테크 네온 / Tech Neon - "Futuristic and innovative"
7. 파스텔 소프트 / Pastel Soft - "Friendly and inviting"
8. 볼드 지오메트릭 / Bold Geometric - "Striking and memorable"
9. 클래식 아카데믹 / Classic Academic - "Authoritative and timeless"
10. 스칸디나비안 휘게 / Scandinavian Hygge - "Comfortable and refined"
```

Since AskUserQuestion supports max 4 options per question, group them into 2-3 category questions:
- Question: "어떤 분위기의 디자인을 원하시나요?" with categories like:
  - "전문적/비즈니스 (미니멀, 코퍼레이트, 클래식)"
  - "모던/트렌디 (그라디언트, 다크, 테크)"
  - "따뜻한/친근한 (네이처, 파스텔, 스칸디나비안)"
  - "강렬한/임팩트 (볼드 지오메트릭)"
- Then follow up with specific style within the chosen category

### Phase 3: Typst Slide Generation

1. **Load the selected color theme** from `assets/color-themes.json` by matching the selected style ID.

2. **Read slide templates** from `references/slide-templates.md` for the template functions.

3. **Generate the .typ file** using the templates and content:
   - Start with theme color variable declarations from the selected theme
   - Use 16:9 widescreen page setup (25.4cm × 14.29cm)
   - Apply the appropriate font based on content language:
     - Korean: `"Noto Sans CJK KR"`
     - English: `"Libertinus Serif"` or `"DejaVu Sans"`
     - Check available fonts with `typst fonts`
   - Structure slides as:
     1. Title slide (표지)
     2. Table of contents / Agenda (목차)
     3. Section dividers between major topics
     4. Content slides with appropriate layouts
     5. Closing slide (마무리)
   - Keep content concise - NO overflow allowed

4. **Compile to PDF**:
   ```bash
   typst compile presentation.typ presentation.pdf
   ```

### Phase 4: Visual Verification Loop (MANDATORY - 3 iterations)

This is a MANDATORY 3-iteration ralph verification loop. Each iteration MUST:

#### Iteration N (repeat 3 times):

**Step 1: Export each slide to PNG**
```bash
# Export all pages as individual PNGs
typst compile presentation.typ slide-{n}.png --format png

# This creates slide-1.png, slide-2.png, etc.
```

**Step 2: Read each PNG and verify**
Use the Read tool on each PNG file to visually inspect:
- [ ] No text overflow beyond slide boundaries
- [ ] No text cut off at edges
- [ ] Adequate spacing between elements
- [ ] Headings fit within single lines
- [ ] Bullet points don't exceed slide area
- [ ] Images (if any) are properly contained
- [ ] Font sizes are readable
- [ ] Color contrast is sufficient

**Step 3: Fix any issues found**
For each issue:
- If text overflows → reduce content, split across slides, or decrease font size
- If spacing is tight → increase margins or reduce content
- If heading is too long → shorten or use smaller font
- If too many bullet points → split into multiple slides

**Step 4: Recompile and verify fix**
```bash
typst compile presentation.typ presentation.pdf
typst compile presentation.typ slide-{n}.png --format png
```

After fixing, re-check ALL slides, not just the fixed ones.

**IMPORTANT**: All 3 iterations MUST run even if no issues are found in earlier iterations.
The purpose is to catch subtle issues that may be missed on first pass.

Log each iteration's findings:
```
Iteration 1: Found [N] issues → Fixed [M]
Iteration 2: Found [N] issues → Fixed [M]
Iteration 3: Found [N] issues → Fixed [M] (should be 0 if quality is high)
```

### Phase 5: PPT Export

After all 3 verification iterations pass:

1. **Ensure PNG slides are up to date**:
   ```bash
   mkdir -p slides/
   typst compile presentation.typ slides/slide-{n}.png --format png
   ```

2. **Convert to PowerPoint**:
   ```bash
   mkdir -p output/
   python .claude/skills/typst/scripts/export-ppt.py \
     --input-dir slides/ \
     --output output/presentation.pptx \
     --title "Presentation Title"
   ```

3. **Report to user**:
   - Show the output path: `output/presentation.pptx`
   - Report slide count
   - Report any issues found and fixed during verification
   - Provide the .typ source file path for future editing

## Asset Files

- `assets/design-vocabulary.json` — 10 design styles with descriptions and mood
- `assets/color-themes.json` — Color palettes for each design style
- `references/slide-templates.md` — Typst template functions for various slide types
- `scripts/export-ppt.py` — PNG-to-PPTX conversion script

## Typst Syntax Quick Reference

Typst has three modes: **markup**, **math**, and **code**. In markup, `#` enters code mode.

### Essential Syntax for Slides

```typst
// Page setup for 16:9 slides
#set page(width: 25.4cm, height: 14.29cm, margin: 1.5cm, fill: rgb("F4F6F9"))

// Typography
#set text(font: "Noto Sans CJK KR", size: 14pt)
*bold* _italic_ `code`

// Layout
#align(center + horizon)[Centered content]
#grid(columns: (1fr, 1fr), [Left], [Right])
#v(1em)  // vertical space
#h(1em)  // horizontal space

// Shapes and decoration
#rect(width: 100%, height: 3pt, fill: rgb("FF6B00"))
#circle(radius: 4pt, fill: rgb("FF6B00"))
#line(length: 100%, stroke: 0.5pt + rgb("CBD8E5"))

// Colors
#text(fill: rgb("003366"))[Colored text]
#block(fill: rgb("F4F6F9"), inset: 12pt, radius: 6pt)[Card content]

// Images
#image("photo.jpg", width: 80%)
#figure(image("chart.png", width: 100%), caption: [Caption])

// Page breaks (= slide breaks)
#pagebreak()
```

### Compilation Commands

```bash
# PDF output
typst compile presentation.typ presentation.pdf

# PNG output (all pages)
typst compile presentation.typ slide-{n}.png --format png

# Single page PNG
typst compile presentation.typ slide.png --format png --pages 1

# SVG output
typst compile presentation.typ slide-{n}.svg --format svg

# Custom font path
typst compile --font-path ./fonts presentation.typ
```

## Available Fonts

Check with `typst fonts`. Common options:
- Korean: `Noto Sans CJK KR`, `Noto Serif CJK KR`
- Sans: `DejaVu Sans`, `Liberation Sans`
- Serif: `Libertinus Serif`, `Liberation Serif`
- Mono: `DejaVu Sans Mono`
- Math: `DejaVu Math TeX Gyre`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Text overflow | Reduce content, split slides, decrease font size |
| Unknown font | Run `typst fonts` to check available fonts |
| CJK not rendering | Use `Noto Sans CJK KR` font |
| PNG export fails | Ensure typst v0.10+ for `--format png` |
| PPT export fails | Run `pip install python-pptx` |
| NotebookLM auth | Run auth setup with visible browser |

## Tips for Professional Results

1. **Less is more** — Max 5-6 bullet points per slide, max 40 chars per heading
2. **Visual hierarchy** — Use font size difference of at least 6pt between heading and body
3. **Consistent spacing** — Use `v(0.8cm)` consistently between sections
4. **Color restraint** — Use accent color sparingly for emphasis only
5. **Slide count** — Plan for ~1 minute per slide for typical presentations
6. **CJK content** — Always set appropriate CJK font before any Korean/Japanese/Chinese text
