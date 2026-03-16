# Typst Slide Templates

Templates for creating beautiful presentation slides. Each template uses color variables that should be set from the selected design theme.

## Color Variable Setup

Every presentation starts with these variable declarations (values come from color-themes.json):

```typst
// Theme colors - replace with values from selected theme
#let theme-primary = rgb("003366")
#let theme-secondary = rgb("005B9A")
#let theme-accent = rgb("FF6B00")
#let theme-bg = rgb("F4F6F9")
#let theme-surface = rgb("FFFFFF")
#let theme-text = rgb("1C2B3A")
#let theme-text-light = rgb("5A7A99")
#let theme-heading = rgb("003366")
#let theme-border = rgb("CBD8E5")
```

## Page Setup (16:9 Widescreen)

```typst
#set page(
  width: 25.4cm,
  height: 14.29cm,
  margin: (top: 1.5cm, bottom: 1.5cm, left: 2cm, right: 2cm),
  fill: theme-bg,
)
#set text(font: "Noto Sans CJK KR", size: 14pt, fill: theme-text)
#set par(leading: 0.8em)
```

## Slide Types

### 1. Title Slide (표지)

```typst
#let title-slide(title, subtitle: none, author: none, date: none) = {
  set page(fill: theme-primary)
  set text(fill: white)
  align(center + horizon)[
    #block(spacing: 0.8em)[
      #text(size: 36pt, weight: "bold", tracking: 0.05em)[#title]
    ]
    #if subtitle != none {
      block(spacing: 0.5em)[
        #text(size: 18pt, fill: theme-surface.lighten(20%))[#subtitle]
      ]
    }
    #v(2em)
    #if author != none {
      text(size: 14pt, fill: theme-surface.lighten(40%))[#author]
    }
    #if date != none {
      linebreak()
      text(size: 12pt, fill: theme-surface.lighten(50%))[#date]
    }
  ]
}
```

### 2. Section Divider Slide (섹션 구분)

```typst
#let section-slide(number, title) = {
  set page(fill: theme-primary)
  place(top + right, dx: -2cm, dy: 1.5cm)[
    #text(size: 72pt, fill: theme-accent.transparentize(50%), weight: "bold")[#number]
  ]
  align(left + horizon, pad(left: 2cm)[
    #block(spacing: 0.5em)[
      #rect(width: 60pt, height: 4pt, fill: theme-accent)
    ]
    #text(size: 32pt, weight: "bold", fill: white)[#title]
  ])
}
```

### 3. Content Slide - Text Only (텍스트 콘텐츠)

```typst
#let content-slide(title, body) = {
  // Header bar
  place(top, rect(width: 100%, height: 0.8cm, fill: theme-primary))

  v(1.5cm)
  text(size: 24pt, weight: "bold", fill: theme-heading)[#title]
  v(0.3cm)
  rect(width: 40pt, height: 3pt, fill: theme-accent)
  v(0.8cm)
  text(size: 14pt, fill: theme-text)[#body]
}
```

### 4. Two-Column Slide (2단 레이아웃)

```typst
#let two-column-slide(title, left-content, right-content) = {
  place(top, rect(width: 100%, height: 0.8cm, fill: theme-primary))

  v(1.5cm)
  text(size: 24pt, weight: "bold", fill: theme-heading)[#title]
  v(0.3cm)
  rect(width: 40pt, height: 3pt, fill: theme-accent)
  v(0.8cm)

  grid(
    columns: (1fr, 0.5cm, 1fr),
    align(left)[#left-content],
    [],
    align(left)[#right-content],
  )
}
```

### 5. Key Point / Quote Slide (핵심 포인트)

```typst
#let key-point-slide(quote, attribution: none) = {
  set page(fill: theme-surface)
  align(center + horizon)[
    #block(width: 80%)[
      #text(size: 48pt, fill: theme-accent, weight: "bold")[""]
      #v(-0.5em)
      #text(size: 22pt, fill: theme-heading, style: "italic")[#quote]
      #if attribution != none {
        v(1em)
        text(size: 14pt, fill: theme-text-light)[— #attribution]
      }
    ]
  ]
}
```

### 6. Bullet Points Slide (목록형)

```typst
#let bullet-slide(title, items) = {
  place(top, rect(width: 100%, height: 0.8cm, fill: theme-primary))

  v(1.5cm)
  text(size: 24pt, weight: "bold", fill: theme-heading)[#title]
  v(0.3cm)
  rect(width: 40pt, height: 3pt, fill: theme-accent)
  v(0.8cm)

  for item in items {
    block(spacing: 0.6em)[
      #grid(
        columns: (20pt, 1fr),
        align(center)[#circle(radius: 4pt, fill: theme-accent)],
        text(size: 14pt, fill: theme-text)[#item],
      )
    ]
  }
}
```

### 7. Image + Text Slide (이미지 + 텍스트)

```typst
#let image-text-slide(title, img-path, description, image-left: true) = {
  place(top, rect(width: 100%, height: 0.8cm, fill: theme-primary))

  v(1.5cm)
  text(size: 24pt, weight: "bold", fill: theme-heading)[#title]
  v(0.3cm)
  rect(width: 40pt, height: 3pt, fill: theme-accent)
  v(0.8cm)

  let img-block = block(clip: true, radius: 8pt)[
    #image(img-path, width: 100%)
  ]
  let text-block = align(left + horizon)[
    #text(size: 14pt, fill: theme-text)[#description]
  ]

  if image-left {
    grid(columns: (1fr, 1cm, 1fr), img-block, [], text-block)
  } else {
    grid(columns: (1fr, 1cm, 1fr), text-block, [], img-block)
  }
}
```

### 8. Data/Stats Slide (통계/숫자)

```typst
#let stats-slide(title, stats) = {
  place(top, rect(width: 100%, height: 0.8cm, fill: theme-primary))

  v(1.5cm)
  text(size: 24pt, weight: "bold", fill: theme-heading)[#title]
  v(0.3cm)
  rect(width: 40pt, height: 3pt, fill: theme-accent)
  v(1.5cm)

  let cols = stats.len()
  grid(
    columns: (1fr,) * cols,
    column-gutter: 1cm,
    ..stats.map(stat => align(center)[
      #text(size: 36pt, weight: "bold", fill: theme-accent)[#stat.value]
      #v(0.3em)
      #text(size: 14pt, fill: theme-text)[#stat.label]
      #if "detail" in stat {
        v(0.2em)
        text(size: 11pt, fill: theme-text-light)[#stat.detail]
      }
    ])
  )
}
```

### 9. Thank You / Closing Slide (마무리)

```typst
#let closing-slide(title: "감사합니다", subtitle: none, contact: none) = {
  set page(fill: theme-primary)
  set text(fill: white)
  align(center + horizon)[
    text(size: 36pt, weight: "bold")[#title]
    #if subtitle != none {
      v(0.5em)
      text(size: 16pt, fill: theme-surface.lighten(30%))[#subtitle]
    }
    #if contact != none {
      v(2em)
      text(size: 12pt, fill: theme-surface.lighten(50%))[#contact]
    }
  ]
}
```

## Complete Presentation Skeleton

```typst
// === Theme Setup ===
#let theme-primary = rgb("003366")
#let theme-secondary = rgb("005B9A")
#let theme-accent = rgb("FF6B00")
#let theme-bg = rgb("F4F6F9")
#let theme-surface = rgb("FFFFFF")
#let theme-text = rgb("1C2B3A")
#let theme-text-light = rgb("5A7A99")
#let theme-heading = rgb("003366")
#let theme-border = rgb("CBD8E5")

// === Page Setup ===
#set page(
  width: 25.4cm, height: 14.29cm,
  margin: (top: 1.5cm, bottom: 1.5cm, left: 2cm, right: 2cm),
  fill: theme-bg,
)
#set text(font: "Noto Sans CJK KR", size: 14pt, fill: theme-text)

// === Import Template Functions ===
// (paste the #let definitions above)

// === Slides ===
#title-slide("프레젠테이션 제목", subtitle: "부제목", author: "발표자", date: "2025년")
#pagebreak()

#section-slide("01", "첫 번째 섹션")
#pagebreak()

#bullet-slide("핵심 요점", (
  "첫 번째 포인트 설명",
  "두 번째 포인트 설명",
  "세 번째 포인트 설명",
))
#pagebreak()

#two-column-slide("비교 분석",
  [왼쪽 내용],
  [오른쪽 내용],
)
#pagebreak()

#closing-slide(subtitle: "질문이 있으신가요?", contact: "email@example.com")
```

## Tips for Overflow Prevention

- Keep title text under 40 characters for single-line display
- Limit bullet points to 5-6 per slide
- Use `#text(size: 12pt)` for dense content slides
- Always test with `typst compile --format png` and visually verify
- If content overflows, split into multiple slides rather than shrinking font
