---
title: "CF 106157C - Colourful Captcha"
description: "We are given two different rainbow colour names. The first colour, C1, is the word that the simplified \"human vision\" system must recognize from the ASCII art."
date: "2026-06-25T11:18:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "C"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 73
verified: true
draft: false
---

[CF 106157C - Colourful Captcha](https://codeforces.com/problemset/problem/106157/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two different rainbow colour names.

The first colour, `C1`, is the word that the simplified "human vision" system must recognize from the ASCII art. The second colour, `C2`, is the word that should appear in the raw text so that a language model reading the image as ordinary strings sees that colour and no other rainbow colour.

The recognition model is extremely weak. It does not care about the actual shape of letters. Every four-connected component of capital letters is treated as a single large letter, and the only feature it uses is the number of holes inside that component.

A component with two holes is interpreted as `B`.

A component with one hole is interpreted as one of `A`, `D`, `O`, `P`, `Q`, `R`.

A component with zero holes is interpreted as any other letter.

Because the six rainbow colour names have different hole-count sequences, recognizing a colour reduces to recognizing a sequence of hole counts.

This is a pure constructive problem. The input size is tiny, there is only one pair of colour names, and the output only needs to satisfy a collection of geometric constraints. The challenge is not efficiency, it is finding a construction that always works.

The main pitfall is that any accidental occurrence of another colour name inside the printed strings immediately violates the statement. Another easy mistake is allowing two neighbouring components to touch, which would merge them into one larger component and completely change the hole-count sequence seen by the recognizer.

## Approaches

A brute-force mindset would try to draw actual block letters for every colour and then somehow hide the language-model colour inside the picture. That works conceptually, but it creates a large number of geometric cases and makes correctness difficult to reason about.

The key observation is that the recognizer only counts holes. It never checks whether a component resembles a real alphabet letter.

Once we realize that, every character of `C1` can be replaced by a tiny template whose only purpose is to create a component with exactly 0, 1, or 2 holes.

We can precompute the hole count associated with every letter appearing in the rainbow colours.

Then we build one connected component per letter of `C1`, separating neighbouring components by at least one column of dots. The recognizer will read exactly the intended hole-count sequence.

For the language-model part, we simply place `C2` as ordinary text on the final row. Since every other row uses only a harmless filler letter, no other rainbow colour name can appear as a substring.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Draw real letters manually | O(1) | O(1) | Unnecessarily complicated |
| Encode only hole counts | O( | C1 | ) |

## Algorithm Walkthrough

1. Create a mapping from each capital letter appearing in rainbow colours to its hole count.
2. Prepare three fixed templates.

A zero-hole component:

```
XXX
X..
X..
X..
XXX
```

A one-hole component:

```
XXX
X.X
X.X
X.X
XXX
```

A two-hole component:

```
XXX
X.X
XXX
X.X
XXX
```
3. For every character of `C1`, look up its hole count and append the corresponding template to the picture.
4. Insert a column of dots between consecutive components so that they remain separate letters.
5. Add one final row containing `C2`, followed by dots until its length matches the other rows.
6. Print the resulting rectangle.

### Why it works

Each template forms a single four-connected component. The first template contains no enclosed regions, the second contains exactly one enclosed region, and the third contains exactly two enclosed regions.

Because adjacent templates are separated by a full column of dots, components never touch. The recognizer therefore sees one component per character.

The sequence of hole counts seen by the recognizer is exactly the sequence corresponding to the letters of `C1`, so the picture is interpreted as `C1`.

The final row explicitly contains `C2` as a standalone substring, satisfying the language-model requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

c1 = input().strip()
c2 = input().strip()

holes = {
    'A': 1, 'B': 2, 'C': 0, 'D': 1, 'E': 0, 'F': 0, 'G': 0,
    'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
    'O': 1, 'P': 1, 'Q': 1, 'R': 1, 'S': 0, 'T': 0, 'U': 0,
    'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0
}

templates = {
    0: [
        "XXX",
        "X..",
        "X..",
        "X..",
        "XXX",
    ],
    1: [
        "XXX",
        "X.X",
        "X.X",
        "X.X",
        "XXX",
    ],
    2: [
        "XXX",
        "X.X",
        "XXX",
        "X.X",
        "XXX",
    ]
}

rows = [""] * 5

for i, ch in enumerate(c1):
    pat = templates[holes[ch]]
    for r in range(5):
        rows[r] += pat[r]
        if i + 1 != len(c1):
            rows[r] += "."

width = max(len(rows[0]), len(c2))

for i in range(5):
    rows[i] += "." * (width - len(rows[i]))

rows.append(c2 + "." * (width - len(c2)))

print("\n".join(rows))
```

The first part builds the hole-count mapping. Only three values matter: 0, 1, and 2.

The three templates are carefully chosen so that each is connected and has the required number of holes.

The construction loop converts every character of `C1` into its template and inserts a separator column of dots between neighbouring components. Without that separator, two components could merge into one larger connected region.

After the five drawing rows are finished, we compute the required rectangle width. Every row must have the same length, so shorter rows are padded with dots.

Finally, the last row contains `C2` and is padded to the same width.

## Worked Examples

### Example 1

Input:

```
BLUE
RED
```

Hole counts for `BLUE` are:

| Letter | Holes |
| --- | --- |
| B | 2 |
| L | 0 |
| U | 0 |
| E | 0 |

The generated component sequence is:

| Position | Hole count |
| --- | --- |
| 1 | 2 |
| 2 | 0 |
| 3 | 0 |
| 4 | 0 |

The recognizer reads `BLUE`.

The last row contains `RED`, so the language-model target is also satisfied.

### Example 2

Input:

```
ORANGE
VIOLET
```

Hole counts for `ORANGE` are:

| Letter | Holes |
| --- | --- |
| O | 1 |
| R | 1 |
| A | 1 |
| N | 0 |
| G | 0 |
| E | 0 |

The recognizer sees:

| Component | Holes |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 0 |
| 5 | 0 |
| 6 | 0 |

That uniquely identifies `ORANGE`.

The last row contains `VIOLET`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | C1 |
| Space | O( | C1 |

The longest rainbow colour has only six letters, so the produced picture is far below the limits of 10 rows and 100 columns.

## Test Cases

```
# helper sketch

# BLUE -> RED
inp = """BLUE
RED
"""

# RED -> BLUE
inp = """RED
BLUE
"""

# ORANGE -> GREEN
inp = """ORANGE
GREEN
"""

# VIOLET -> YELLOW
inp = """VIOLET
YELLOW
"""

# GREEN -> ORANGE
inp = """GREEN
ORANGE
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| BLUE / RED | Any valid construction | Contains a two-hole component |
| RED / BLUE | Any valid construction | Mix of one-hole and zero-hole components |
| ORANGE / GREEN | Any valid construction | Longest one-hole prefix |
| VIOLET / YELLOW | Any valid construction | Alternating hole counts |
| GREEN / ORANGE | Any valid construction | Five-letter colour |

## Edge Cases

A colour such as `BLUE` starts with the only two-hole letter among all rainbow colours. The construction handles this by selecting the dedicated two-hole template. The recognizer sees a component with exactly two enclosed regions and correctly interprets it as `B`.

A colour such as `ORANGE` begins with several consecutive one-hole letters. Since every component is separated by a dot column, these one-hole components never merge. The recognizer still sees three distinct letters rather than one large component.

A colour such as `GREEN` contains both zero-hole and one-hole letters. Because the hole count is encoded independently for each component, mixed sequences are handled automatically without any special logic.
