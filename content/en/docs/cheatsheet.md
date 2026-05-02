---
title: "Cheatsheet"
weight: 1
description: "Quick reference for Markdown, shortcodes, front matter, and Hugo Book features."
---

# Cheatsheet

Quick reference for writing notes in this repo.

---

## Front matter

```yaml
---
title: "Note title"
date: 2026-05-02
description: "One line summary."
weight: 10          # lower = higher in sidebar
tags: ["go", "db"]
draft: false

# Hugo Book extras
bookHidden: true         # hide from sidebar, still accessible by URL
bookCollapseSection: true  # section starts collapsed
bookFlatSection: true    # list children flat, no nesting
bookToC: false           # disable table of contents on this page
bookSearchExclude: true  # exclude from search index
---
```

---

## Markdown

### Text

```
**bold**    *italic*    ~~strikethrough~~    `inline code`
```

### Links

```markdown
[text](https://example.com)
[relative](../other-note.md)
[safe internal]({{</* relref "code/go-interfaces.md" */>}})
```

### Images

```markdown
![alt](./image.png)
![alt](./image.png "title")
```

### Tables

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| a    |   b    |     c |
```

### Code blocks

````markdown
```go
fmt.Println("hello")
```
````

### Task list

```markdown
- [x] done
- [ ] pending
```

### Footnote

```markdown
Claim.[^1]

[^1]: Source.
```

---

## Alerts (callout boxes)

```markdown
> [!NOTE]
> General info.

> [!TIP]
> Helpful suggestion.

> [!IMPORTANT]
> Must-know info.

> [!WARNING]
> Could cause problems.

> [!CAUTION]
> Risk of harm or data loss.
```

---

## Shortcodes

### details

```
{{</* details title="Click to expand" */>}}
Hidden content.
{{</* /details */>}}

{{</* details title="Open by default" open=true */>}}
Visible on load.
{{</* /details */>}}
```

### tabs

```
{{</* tabs */>}}
{{</* tab "macOS" */>}}
brew install something
{{</* /tab */>}}
{{</* tab "Linux" */>}}
apt install something
{{</* /tab */>}}
{{</* /tabs */>}}
```

### columns

```
{{</* columns */>}}
Left side.
<--->
Right side.
{{</* /columns */>}}

{{</* columns ratio="2:1" */>}}
Wider left.
<--->
Narrow right.
{{</* /columns */>}}
```

### button

```
{{</* button href="https://github.com/tamnd/brain" */>}}
View on GitHub
{{</* /button */>}}
```

### card

```
{{</* card header="Title" */>}}
Card body.
{{</* /card */>}}

{{</* card href="/brain/maths/" image="./cover.png" */>}}
Caption text.
{{</* /card */>}}
```

### steps

```
{{</* steps */>}}

1. **First step**

   Details here.

2. **Second step**

   More details.

{{</* /steps */>}}
```

### badge

```
{{</* badge style="info" title="Status" value="stable" */>}}
{{</* badge style="warning" title="Version" value="beta" */>}}
{{</* badge style="danger" title="Deprecated" */>}}
```

Styles: `default` `info` `warning` `danger`

### image (zoomable)

```
{{</* image src="./diagram.png" alt="Description" */>}}
```

### mermaid

```
{{</* mermaid */>}}
graph TD
    A[Start] --> B{Branch}
    B -->|yes| C[Done]
    B -->|no| D[Skip]
{{</* /mermaid */>}}
```

```
{{</* mermaid */>}}
sequenceDiagram
    Client->>Server: request
    Server-->>Client: response
{{</* /mermaid */>}}
```

### katex (math)

```
{{</* katex */>}}x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}{{</* /katex */>}}
```

Block (centered):

```
{{</* katex display=true */>}}
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
{{</* /katex */>}}
```

---

## Sidebar order and visibility

| Want | How |
|------|-----|
| Pin page to top | `weight: 1` in front matter |
| Hide from nav | `bookHidden: true` |
| Collapse section | `bookCollapseSection: true` on `_index.md` |
| Flat section | `bookFlatSection: true` on `_index.md` |
| External link in nav | `bookHref: "https://..."` |

---

## Running locally

```bash
cd ~/github/tamnd/brain
hugo server                   # live reload at localhost:1313/brain/
hugo server --buildDrafts     # include draft: true pages
hugo server --buildFuture     # include future-dated pages
```
