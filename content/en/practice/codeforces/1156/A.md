---
title: "CF 1156A - Inscribed Figures"
description: "We are given a sequence of geometric figures. Each number represents one of three shapes: - 1 = circle - 2 = isosceles triangle whose height equals its base length - 3 = square Every figure is inscribed into the previous one and is chosen with the largest possible size."
date: "2026-06-12T02:37:36+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1156
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 64 (Rated for Div. 2)"
rating: 1400
weight: 1156
solve_time_s: 91
verified: true
draft: false
---

[CF 1156A - Inscribed Figures](https://codeforces.com/problemset/problem/1156/A)

**Rating:** 1400  
**Tags:** geometry  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of geometric figures. Each number represents one of three shapes:

- `1` = circle
- `2` = isosceles triangle whose height equals its base length
- `3` = square

Every figure is inscribed into the previous one and is chosen with the largest possible size. Because the orientation of every triangle and square is fixed, each pair of consecutive figures has a unique relative placement.

Our task is not to reconstruct coordinates. We only need to determine how many distinct contact points appear between all consecutive pairs of figures. Sometimes two figures touch along an entire segment rather than at isolated points. In that case the answer is infinite.

The number of figures is at most 100, which is tiny. Any algorithm that scans the sequence a few times is more than fast enough. The challenge is purely geometric: understanding how each pair of figure types interacts.

The first trap is that contact counts do not depend on the actual sizes. Because every figure is maximally inscribed, each pair of figure types always produces the same pattern of touching points.

A second trap is the infinite case. For example:

```
2
2 3
```

A square inscribed in the special triangle touches the triangle along its entire bottom side. That side contains infinitely many points, so the correct output is

```
Infinite
```

A third trap is that some triples require a correction. Consider

```
3
3 1 2
```

A square contains a circle, and the circle contains a triangle. Naively adding pair contributions gives `4 + 3 = 7`, but one touching point is counted twice geometrically. The correct answer is 6. This special configuration is the key observation of the problem.

## Approaches

A brute-force geometric approach would attempt to reconstruct exact coordinates of every figure, compute intersections between boundaries of consecutive figures, merge equal points, and detect whether an overlap segment exists.

Such a solution is unnecessarily complicated. Even though `n ≤ 100`, representing circles, triangles, and squares precisely leads to difficult geometric calculations involving irrational coordinates and duplicate-point detection.

The real structure is much simpler. Since every figure is maximally inscribed and orientations are fixed, the interaction of any consecutive pair depends only on their types.

We can analyze all possible pairs once.

For a circle and triangle, the triangle's three vertices lie on the circle, giving three touching points.

For a circle and square, the square's four vertices lie on the circle, giving four touching points.

For a triangle and circle, the circle touches the three sides of the triangle, giving three touching points.

For a square and circle, the circle touches the four sides of the square, giving four touching points.

For a triangle and square, or a square and triangle, the figures share an entire side segment. The number of touching points is infinite.

This immediately reduces the problem to processing adjacent pairs.

One detail remains. The sequence

```
3 1 2
```

creates a configuration where the point counted from `(3,1)` and the point counted from `(1,2)` coincide. The official geometric analysis shows that every occurrence of the consecutive triple `(3,1,2)` reduces the total by one.

The brute-force geometry disappears entirely. We only need a small lookup table and one special correction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Geometry Reconstruction | Very large implementation complexity | O(n) | Impractical |
| Pair Analysis + Special Triple Correction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the sequence of figure types.
2. Scan every adjacent pair.
3. If the pair is `(2,3)` or `(3,2)`, print `"Infinite"` and stop.

These two combinations produce a common side segment rather than isolated contact points.
4. Otherwise add the contribution of the pair to the answer.

The only possible finite pairs are:

- `(1,2)` or `(2,1)` contribute `3`
- `(1,3)` or `(3,1)` contribute `4`
5. After processing all pairs, scan every consecutive triple.
6. For each occurrence of `(3,1,2)`, subtract `1` from the answer.

This removes the unique double-counted touching point.
7. Print `"Finite"` and the resulting count.

### Why it works

Every maximal inscription between two allowed figure types produces a fixed contact pattern independent of scale. The total number of touching points is therefore the sum of pair contributions.

The only way infinitely many touching points arise is when a square and the special triangle share a whole side segment. Those are exactly the pairs `(2,3)` and `(3,2)`.

Among all finite configurations, the only overlap between touching points contributed by neighboring pairs occurs in the triple `(3,1,2)`. Subtracting one for each such triple removes the duplicated point. No other triple creates a repeated contact point. Hence the algorithm counts every distinct touching point exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ans = 0

for i in range(n - 1):
    x = a[i]
    y = a[i + 1]

    if (x == 2 and y == 3) or (x == 3 and y == 2):
        print("Infinite")
        sys.exit(0)

    if x + y == 3:
        ans += 3
    else:
        ans += 4

for i in range(n - 2):
    if a[i] == 3 and a[i + 1] == 1 and a[i + 2] == 2:
        ans -= 1

print("Finite")
print(ans)
```

The first loop processes adjacent pairs. Any triangle-square adjacency immediately makes the answer infinite, so the program terminates at once.

For finite pairs, there are only two possibilities. Circle-triangle pairs contribute three touching points, while circle-square pairs contribute four. Because adjacent figures are guaranteed to differ, checking `x + y == 3` is enough to recognize the circle-triangle combinations `(1,2)` and `(2,1)`.

The second loop applies the correction for every `(3,1,2)` triple. Missing this adjustment is the most common mistake in this problem.

No special handling for `(2,1,3)` is needed. Only `(3,1,2)` creates a duplicated touching point.

## Worked Examples

### Sample 1

Input:

```
3
2 1 3
```

Pair processing:

| Pair | Contribution | Running Total |
| --- | --- | --- |
| (2,1) | 3 | 3 |
| (1,3) | 4 | 7 |

Triple processing:

| Triple | Correction | Total |
| --- | --- | --- |
| (2,1,3) | 0 | 7 |

Final answer:

```
Finite
7
```

This example shows a completely finite configuration. No infinite pair appears and no special triple correction applies.

### Sample 2

Input:

```
2
2 3
```

Pair processing:

| Pair | Result |
| --- | --- |
| (2,3) | Infinite |

The algorithm stops immediately and prints:

```
Infinite
```

This demonstrates the geometric degeneracy where the triangle and square share an entire segment.

### Additional Example

Input:

```
3
3 1 2
```

Pair processing:

| Pair | Contribution | Running Total |
| --- | --- | --- |
| (3,1) | 4 | 4 |
| (1,2) | 3 | 7 |

Triple processing:

| Triple | Correction | Total |
| --- | --- | --- |
| (3,1,2) | -1 | 6 |

Final answer:

```
Finite
6
```

This example exercises the special correction and is the easiest way to verify that the implementation is complete.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over pairs and one pass over triples |
| Space | O(1) | Only a few integer variables are used |

With `n ≤ 100`, the running time is tiny. The solution performs only linear scans and uses constant extra memory, comfortably fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0

    for i in range(n - 1):
        x = a[i]
        y = a[i + 1]

        if (x == 2 and y == 3) or (x == 3 and y == 2):
            return "Infinite\n"

        if x + y == 3:
            ans += 3
        else:
            ans += 4

    for i in range(n - 2):
        if a[i] == 3 and a[i + 1] == 1 and a[i + 2] == 2:
            ans -= 1

    return f"Finite\n{ans}\n"

# sample-like finite case
assert run("3\n2 1 3\n") == "Finite\n7\n"

# infinite case
assert run("2\n2 3\n") == "Infinite\n"

# special correction
assert run("3\n3 1 2\n") == "Finite\n6\n"

# minimum size finite
assert run("2\n1 2\n") == "Finite\n3\n"

# minimum size finite, circle-square
assert run("2\n1 3\n") == "Finite\n4\n"

# multiple corrections
assert run("5\n3 1 2 1 2\n") == "Finite\n11\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 2 1 3` | `Finite 7` | Standard finite configuration |
| `2 / 2 3` | `Infinite` | Infinite segment contact |
| `3 / 3 1 2` | `Finite 6` | Special triple correction |
| `2 / 1 2` | `Finite 3` | Smallest finite circle-triangle case |
| `2 / 1 3` | `Finite 4` | Smallest finite circle-square case |
| `5 / 3 1 2 1 2` | `Finite 11` | Multiple pair contributions and one correction |

## Edge Cases

### Triangle Adjacent to Square

Input:

```
2
3 2
```

The first pair is `(3,2)`. The algorithm immediately detects one of the two forbidden adjacencies and prints:

```
Infinite
```

No further processing is needed because a shared segment already creates infinitely many touching points.

### Special Triple `(3,1,2)`

Input:

```
3
3 1 2
```

The pair contributions give `4 + 3 = 7`.

The triple scan finds exactly one occurrence of `(3,1,2)` and subtracts one.

The final answer becomes:

```
Finite
6
```

A solution that only sums pair contributions would incorrectly output 7.

### Longer Sequence Containing an Infinite Pair

Input:

```
5
1 3 2 1 3
```

The algorithm processes `(1,3)` successfully, then encounters `(3,2)`.

Because this pair already creates infinitely many touching points, the correct output is:

```
Infinite
```

The remaining figures are irrelevant. Any implementation that continues counting after discovering such a pair risks producing a finite answer for an infinite configuration.
