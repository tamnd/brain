---
title: "CF 36B - Fractal"
description: "We start with an n × n pattern consisting of black cells () and white cells (.). This pattern acts like a template. The"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 36
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 36"
rating: 1600
weight: 36
solve_time_s: 112
verified: true
draft: false
---

[CF 36B - Fractal](https://codeforces.com/problemset/problem/36/B)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an `n × n` pattern consisting of black cells (`*`) and white cells (`.`). This pattern acts like a template.

The fractal is built recursively. At the first level, the whole canvas is divided into `n × n` blocks, and every block corresponding to a black cell in the template becomes fully black. White template cells stay undecided for now.

At the next level, every still-white block is again divided into `n × n` smaller blocks, and the same template is applied inside it. Black cells stop expanding forever, while white cells continue recursively.

After performing this process exactly `k` times, we must print the final picture. Its size is `n^k × n^k`.

The limits are very small numerically, but the final output itself can become large. Since `n ≤ 3` and `k ≤ 5`, the largest possible grid has size `3^5 = 243`, so the output contains at most about sixty thousand cells. That means even algorithms touching every final cell multiple times are perfectly safe.

The real challenge is understanding how the recursion determines whether a particular cell ends up black or white.

A common mistake is to think that every level overwrites previous colors. That is not how the process works. Once a region becomes black, recursion stops there permanently.

Consider this input:

```
2 2
*.
..
```

At the first level, the top-left quadrant becomes entirely black. Nothing inside it is subdivided again. A careless implementation might continue recursing into that quadrant and incorrectly create white cells inside a region that should stay fully black.

Another subtle case appears when the template contains only one white cell.

```
2 3
**
*.
```

Only the bottom-right branch keeps subdividing. Every other region becomes black immediately. If an implementation blindly expands all cells every step, it wastes work and can accidentally overwrite fixed black regions.

The smallest possible case is also worth checking:

```
2 1
..
.*
```

Here the answer is exactly the original template. No recursive expansion happens because we only perform one level.

## Approaches

The most direct simulation mirrors the statement literally.

We begin with a single white square. At each step, every currently white square is replaced by an `n × n` copy of the template. Black squares remain solid black forever.

One way to implement this is recursive subdivision. Every region either becomes fully black immediately, or gets subdivided again. Since the final image contains at most `243 × 243` cells, this approach is already fast enough.

The issue is that explicitly managing recursive regions becomes awkward. We need coordinates, sizes, stopping conditions, and careful handling of already-black regions.

The key observation is that every final cell can be analyzed independently.

Take a cell `(x, y)` in the final grid. At every recursion level, the template decides whether that position falls into a black subcell or a white subcell. The coordinates at each level are simply the digits of `x` and `y` in base `n`.

Suppose at some level we examine:

```
template[x % n][y % n]
```

If this position is black, then the entire ancestor region became black at that recursion depth, so the final cell must also be black. We can stop immediately.

If it is white, recursion continues upward:

```
x //= n
y //= n
```

We repeat this for all `k` levels. If no level ever lands on a black template cell, the final cell stays white.

This transforms the problem from recursive region construction into a simple per-cell digit inspection problem.

The brute-force recursive construction works because the output size is small, but the coordinate-based interpretation is cleaner and much easier to reason about.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursive construction | O(n^(2k) * k) | O(n^(2k)) | Accepted |
| Optimal coordinate inspection | O(n^(2k) * k) | O(1) extra | Accepted |

The asymptotic complexity looks the same because the output itself already has `n^(2k)` cells. The improvement comes from simplicity and lower constant factors.

## Algorithm Walkthrough

1. Read the template grid and compute the final size `size = n^k`.
2. Iterate over every final cell `(i, j)` in the `size × size` output grid.
3. For the current cell, copy its coordinates into temporary variables:

```
x = i
y = j
```
4. Repeat exactly `k` times.

At each step, inspect:

```
template[x % n][y % n]
```

These remainders tell us which template cell controls the current recursion level.
5. If that template cell is black (`*`), mark the final cell black immediately and stop checking deeper levels.

This works because black regions never subdivide further.
6. Otherwise divide the coordinates:

```
x //= n
y //= n
```

This moves to the parent recursion level.
7. If all `k` levels stay white, the final cell is white.
8. Print the constructed rows.

### Why it works

Every coordinate in the final image corresponds to a path through the recursive subdivision tree.

The least significant base-`n` digits determine the deepest subdivision level, the next digits determine the parent level, and so on.

A cell becomes black if any level of this path lands on a black template position. Once that happens, recursion stops and the entire descendant region stays black forever.

If every level lands on a white template cell, the recursion survives all `k` steps and the cell remains white.

The algorithm checks exactly these conditions, so every output cell receives the correct color.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
pattern = [input().strip() for _ in range(n)]

size = n ** k
answer = []

for i in range(size):
    row = []

    for j in range(size):
        x = i
        y = j
        black = False

        for _ in range(k):
            if pattern[x % n][y % n] == '*':
                black = True
                break

            x //= n
            y //= n

        row.append('*' if black else '.')

    answer.append(''.join(row))

sys.stdout.write('\n'.join(answer))
```

The outer two loops generate every position in the final image.

For each cell, the variables `x` and `y` are repeatedly reduced using integer division. This effectively walks upward through recursion levels.

The expression:

```
pattern[x % n][y % n]
```

extracts the current base-`n` digit pair. Those digits identify which template block controls the current level.

The early `break` is important. Once a black template cell appears, deeper levels no longer matter because recursion stops there permanently.

A subtle implementation detail is the order of operations. We must check the current remainder before dividing by `n`. Reversing the order would skip the deepest recursion level and produce shifted patterns.

Another detail is iterating exactly `k` times. Even if `x` and `y` become zero early, higher recursion levels still correspond to template position `(0, 0)`.

## Worked Examples

### Example 1

Input:

```
2 3
.*
..
```

The template says only the top-right block becomes black.

Final size:

```
2^3 = 8
```

Consider several cells:

| Cell `(i,j)` | Level 1 `(x%n,y%n)` | Level 2 | Level 3 | Result |
| --- | --- | --- | --- | --- |
| `(0,0)` | `(0,0)=.` | `(0,0)=.` | `(0,0)=.` | `.` |
| `(0,1)` | `(0,1)=*` | stop | stop | `*` |
| `(2,2)` | `(0,0)=.` | `(1,1)=.` | `(0,0)=.` | `.` |
| `(3,4)` | `(1,0)=.` | `(1,0)=.` | `(0,1)=*` | `*` |

This demonstrates that a black decision can occur at any recursion depth. The algorithm keeps checking levels until either black appears or all levels remain white.

### Example 2

Input:

```
2 2
*.
..
```

Final size:

```
4
```

Trace several cells:

| Cell `(i,j)` | Level 1 | Level 2 | Result |
| --- | --- | --- | --- |
| `(0,0)` | `(0,0)=*` | stop | `*` |
| `(1,1)` | `(1,1)=.` | `(0,0)=*` | `*` |
| `(2,2)` | `(0,0)=*` | stop | `*` |
| `(3,3)` | `(1,1)=.` | `(1,1)=.` | `.` |

The important observation here is that black regions stop recursion immediately. Even though `(0,0)` would map to deeper levels, the first level already fixes it as black forever.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^(2k) * k) | We inspect every output cell and check at most `k` recursion levels |
| Space | O(n^(2k)) | The output grid itself dominates memory usage |

The largest grid contains `243 × 243 = 59049` cells. For each cell we perform at most five checks. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    pattern = [input().strip() for _ in range(n)]

    size = n ** k
    ans = []

    for i in range(size):
        row = []

        for j in range(size):
            x = i
            y = j
            black = False

            for _ in range(k):
                if pattern[x % n][y % n] == '*':
                    black = True
                    break

                x //= n
                y //= n

            row.append('*' if black else '.')

        ans.append(''.join(row))

    return '\n'.join(ans)

# provided sample
assert run(
"""2 3
.*
..
"""
) == (
""".*******
..******
.*.*****
....****
.***.***
..**..**
.*.*.*.*
........"""
), "sample 1"

# minimum size with k = 1
assert run(
"""2 1
..
.*
"""
) == (
"""..
.*"""
), "k = 1 should reproduce template"

# only one recursive white branch
assert run(
"""2 2
**
*.
"""
) == (
"""****
****
****
***."""
), "single surviving white path"

# all white template
assert run(
"""2 3
..
..
"""
) == (
"""........
........
........
........
........
........
........
........"""
), "everything stays white"

# off-by-one coordinate checks
assert run(
"""2 2
.*
..
"""
) == (
""".***
..**
.*.*
...."""
), "base-n digit traversal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `k = 1` case | Original template | No unnecessary recursion |
| Single white branch | Mostly black grid | Black regions stop recursion |
| All white template | Fully white output | No accidental black propagation |
| Mixed 2-level case | Structured fractal | Correct base-`n` coordinate handling |

## Edge Cases

Consider the case where recursion survives through only one path:

```
2 3
**
*.
```

At every level, three quadrants become permanently black immediately. Only the bottom-right quadrant continues subdividing.

Take cell `(7,7)`.

At each level:

```
(7 % 2, 7 % 2) = (1,1) -> white
(3 % 2, 3 % 2) = (1,1) -> white
(1 % 2, 1 % 2) = (1,1) -> white
```

No black level appears, so the cell stays white.

Now take `(6,7)`:

```
(0,1) -> black
```

The algorithm stops instantly and marks the cell black.

This confirms the rule that a single black ancestor dominates all deeper levels.

Now consider the smallest recursion depth:

```
2 1
..
.*
```

The algorithm checks exactly one level for each cell.

For `(1,1)`:

```
(1 % 2, 1 % 2) = (1,1) -> black
```

For `(0,1)`:

```
(0,1) -> white
```

The output exactly matches the template, confirming that the implementation handles `k = 1` correctly without extra subdivision.

Finally, consider an all-white template:

```
2 2
..
..
```

Every level check always lands on a white template cell. Since no recursion level ever produces black, the entire final image stays white.

This catches implementations that accidentally initialize cells as black or fail to reset state between iterations.
