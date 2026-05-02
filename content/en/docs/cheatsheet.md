---
title: "Cheatsheet"
weight: 1
description: "Quick reference with live previews for Markdown, shortcodes, and front matter."
---

# Cheatsheet

Each section shows the syntax followed by a live preview.

---

## Alerts

````markdown
> [!NOTE]
> General info the reader should not miss.
````

> [!NOTE]
> General info the reader should not miss.

````markdown
> [!TIP]
> Helpful suggestion.
````

> [!TIP]
> Helpful suggestion.

````markdown
> [!IMPORTANT]
> Must-know info.
````

> [!IMPORTANT]
> Must-know info.

````markdown
> [!WARNING]
> Could cause problems.
````

> [!WARNING]
> Could cause problems.

````markdown
> [!CAUTION]
> Risk of harm or data loss.
````

> [!CAUTION]
> Risk of harm or data loss.

---

## Details

````markdown
{{</* details title="Click to expand" */>}}
Hidden content revealed on click.
{{</* /details */>}}
````

{{< details title="Click to expand" >}}
Hidden content revealed on click.
{{< /details >}}

````markdown
{{</* details title="Open by default" open=true */>}}
Visible immediately.
{{</* /details */>}}
````

{{< details title="Open by default" open=true >}}
Visible immediately.
{{< /details >}}

---

## Tabs

````markdown
{{</* tabs */>}}
{{</* tab "Go" */>}}
```go
fmt.Println("hello")
```
{{</* /tab */>}}
{{</* tab "Python" */>}}
```python
print("hello")
```
{{</* /tab */>}}
{{</* tab "Rust" */>}}
```rust
println!("hello");
```
{{</* /tab */>}}
{{</* /tabs */>}}
````

{{< tabs >}}
{{< tab "Go" >}}
```go
fmt.Println("hello")
```
{{< /tab >}}
{{< tab "Python" >}}
```python
print("hello")
```
{{< /tab >}}
{{< tab "Rust" >}}
```rust
println!("hello");
```
{{< /tab >}}
{{< /tabs >}}

---

## Steps

````markdown
{{</* steps */>}}

1. **Install Hugo**

   Download the extended binary from gohugo.io.

2. **Clone the repo**

   `git clone git@github.com:tamnd/brain.git`

3. **Run locally**

   `hugo server`

{{</* /steps */>}}
````

{{< steps >}}

1. **Install Hugo**

   Download the extended binary from gohugo.io.

2. **Clone the repo**

   `git clone git@github.com:tamnd/brain.git`

3. **Run locally**

   `hugo server`

{{< /steps >}}

---

## Badge

````markdown
{{</* badge content="stable" type="info" */>}}
{{</* badge content="beta" type="warning" */>}}
{{</* badge content="deprecated" type="error" */>}}
{{</* badge content="tag" */>}}
````

{{< badge content="stable" type="info" >}}
{{< badge content="beta" type="warning" >}}
{{< badge content="deprecated" type="error" >}}
{{< badge content="tag" >}}

---

## Mermaid diagrams

````markdown
```mermaid
graph LR
    A[Write note] --> B[brain_on.sh detects change]
    B --> C[git commit + push]
    C --> D[GitHub Actions builds]
    D --> E[Live on GitHub Pages]
```
````

```mermaid
graph LR
    A[Write note] --> B[brain_on.sh detects change]
    B --> C[git commit + push]
    C --> D[GitHub Actions builds]
    D --> E[Live on GitHub Pages]
```

````markdown
```mermaid
sequenceDiagram
    Client->>Server: GET /api/notes
    Server-->>Client: 200 OK + JSON
```
````

```mermaid
sequenceDiagram
    Client->>Server: GET /api/notes
    Server-->>Client: 200 OK + JSON
```

---

## KaTeX math

Inline:

```markdown
$E = mc^2$
```

$E = mc^2$

Block (centered):

```markdown
$$
\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}
$$
```

$$
\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}
$$

---

## Code blocks

````markdown
```go
package main

import "fmt"

func main() {
    fmt.Println("hello, brain")
}
```
````

```go
package main

import "fmt"

func main() {
    fmt.Println("hello, brain")
}
```

```python
def greet(name: str) -> str:
    return f"hello, {name}"
```

```sql
SELECT title, date
FROM notes
WHERE tags @> ARRAY['go']
ORDER BY date DESC;
```

```bash
hugo server --buildDrafts --buildFuture
```

---

## Markdown quick reference

### Text

| Syntax | Result |
|--------|--------|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `` `code` `` | `code` |
| `~~strike~~` | ~~strike~~ |

### Links

```markdown
[external](https://gohugo.io)
[internal]({{</* relref "cheatsheet.md" */>}})
```

[external](https://gohugo.io)

### Task list

```markdown
- [x] Published cheatsheet
- [x] Added dark mode toggle
- [ ] Write more notes
```

- [x] Published cheatsheet
- [x] Added dark mode toggle
- [ ] Write more notes

### Table

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| a    |   b    |     c |
| 1    |   2    |     3 |
```

| Left | Center | Right |
|:-----|:------:|------:|
| a    |   b    |     c |
| 1    |   2    |     3 |

### Footnote

```markdown
This is a claim.[^source]

[^source]: The source for this claim.
```

This is a claim.[^source]

[^source]: The source for this claim.

---

## Front matter reference

```yaml
---
title: "Note title"
date: 2026-05-02
weight: 1                    # sidebar order, lower = higher
tags: ["go", "db"]
draft: false

math: true                   # enable KaTeX on this page
---
```
