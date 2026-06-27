---
title: "CF 104974I - Collin-Count"
description: "We are given a set of distinct points on a 2D plane. The task is to count how many ways we can choose four different points such that all four lie on the same straight line."
date: "2026-06-28T06:13:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104974
codeforces_index: "I"
codeforces_contest_name: "Codentines Day"
rating: 0
weight: 104974
solve_time_s: 87
verified: false
draft: false
---

[CF 104974I - Collin-Count](https://codeforces.com/problemset/problem/104974/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct points on a 2D plane. The task is to count how many ways we can choose four different points such that all four lie on the same straight line.

In other words, we want to count quadruples of indices $i < j < k < l$ where the corresponding points are collinear. Collinearity here means that all four points share a single line, not just that every pair forms some arbitrary alignment.

The input size is small enough that we can consider quadratic or cubic reasoning per point. With $n \le 400$, an $O(n^3)$ approach is already borderline but sometimes acceptable in C++ and tight in Python. An $O(n^2)$ or $O(n^2 \log n)$ solution is ideal.

A naive direction is to try all quadruples directly, which would be $O(n^4)$, but $400^4$ is already too large and would time out. The structure of collinearity suggests we should instead group points by direction or line identity rather than enumerating all quadruples.

A subtle edge case appears when many points lie on the same line. For example, if all points are on a single line, the answer is $\binom{n}{4}$. Any approach that only counts triples or pairs without properly aggregating all points per line will undercount or overcount in such configurations.

Another tricky case is vertical lines, where slope computations can break due to division by zero. For example:

```
4
0 0
0 1
0 2
0 3
```

The correct answer is 1, but slope-based floating point grouping would often fail unless carefully normalized.

## Approaches

The brute-force idea is straightforward: enumerate every 4-tuple of points and check whether they are collinear. Checking collinearity can be done via cross product. For four points, we can verify that points $A, B, C$ are collinear and $A, B, D$ are collinear. This gives an $O(1)$ check per quadruple, but there are $\binom{n}{4}$ such quadruples, which is about $10^9$ when $n = 400$. That is far too slow.

A better perspective is to fix a point $i$ and look at all other points relative to it. Every line passing through $i$ corresponds to a direction vector. If we group all other points by their normalized direction from $i$, then any group of size $k$ corresponds to a set of points collinear with $i$. However, quadruples are not centered on a single pivot; a valid quadruple might not include a chosen reference point.

This leads to the key observation: every set of $k$ collinear points contributes $\binom{k}{4}$ valid quadruples, regardless of how the line is found. So the problem reduces to identifying all maximal collinear groups and summing their contributions.

To do this efficiently, we consider all pairs of points. Each pair defines a unique line. If we can count how many points lie on that line, then we can compute how many quadruples that line contributes. The challenge is to avoid counting the same line multiple times.

We solve this by encoding each line in a normalized canonical form. A line can be represented as $Ax + By + C = 0$, where $A, B, C$ are integers derived from two points. We normalize this representation so that all equivalent lines map to the same key. Then we count how many points lie on each line representation by checking all pairs and incrementing.

This gives us a map from line → set of points, implicitly constructed via pair processing. Finally, for each line with $k$ supporting points, we add $\binom{k}{4}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over quadruples | $O(n^4)$ | $O(1)$ | Too slow |
| Pair-based line grouping | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. For every unordered pair of points $(i, j)$, compute the line passing through them in a normalized integer representation. This ensures all pairs on the same geometric line produce identical keys.
2. Maintain a dictionary from line representation to a set of points (or an incremental counter structure). For each pair $(i, j)$, add both endpoints to the set associated with that line. This ensures we eventually recover all points lying on each line.
3. After processing all pairs, iterate over all stored lines and compute the number of distinct points on each line. Let this be $k$.
4. For each line, add $\binom{k}{4} = \frac{k(k-1)(k-2)(k-3)}{24}$ to the answer.
5. Output the accumulated sum.

The reason step 2 uses sets rather than just counting pairs is that a line with many points generates many pairs, and we need to deduplicate points to recover the true cardinality of the line.

### Why it works

Every collinear quadruple lies on exactly one geometric line. When we group points by their unique line representation, each valid quadruple is counted exactly once because it belongs to exactly one line group. Within a line containing $k$ points, all subsets of size 4 are valid and independent of ordering, so summing $\binom{k}{4}$ over all lines correctly enumerates all valid quadruples without overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd
from collections import defaultdict

def norm_line(x1, y1, x2, y2):
    A = y2 - y1
    B = x1 - x2
    C = A * x1 + B * y1

    g = gcd(gcd(abs(A), abs(B)), abs(C))
    if g:
        A //= g
        B //= g
        C //= g

    if A < 0 or (A == 0 and B < 0):
        A, B, C = -A, -B, -C

    return (A, B, C)

def comb4(k):
    if k < 4:
        return 0
    return k * (k - 1) * (k - 2) * (k - 3) // 24

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    lines = defaultdict(set)

    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            key = norm_line(x1, y1, x2, y2)
            lines[key].add(i)
            lines[key].add(j)

    ans = 0
    for s in lines.values():
        k = len(s)
        ans += comb4(k)

    print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation detail is the normalization of the line representation. The coefficients $A, B, C$ are reduced by their greatest common divisor so that identical geometric lines collapse into the same dictionary key. The sign normalization ensures that the same line is not represented twice with opposite signs.

We use a set per line to avoid double counting points coming from multiple pairs on the same line. This is essential because each line with $k$ points produces $\binom{k}{2}$ pairs, but we only want the final distinct count of points, not the pair multiplicity.

## Worked Examples

### Example 1

Input:

```
5
1 1
2 2
3 3
4 4
5 5
```

All points lie on one diagonal line.

| Pair processed | Line key | Set size update |
| --- | --- | --- |
| (1,2) | same line | {1,2} |
| (1,3) | same line | {1,2,3} |
| (1,4) | same line | {1,2,3,4} |
| (1,5) | same line | {1,2,3,4,5} |

Final set size is 5.

Contribution is $\binom{5}{4} = 5$.

This confirms that once all points are aggregated under a single normalized line, counting reduces correctly to a combinatorial selection.

### Example 2

Input:

```
4
1 1
1 2
2 1
2 2
```

No three points are collinear, so no line contains 4 points.

| Pair processed | Line key | Set size |
| --- | --- | --- |
| (1,2) | vertical | 2 |
| (1,3) | horizontal-ish | 2 |
| (2,4) | diagonal | 2 |

All line groups have size 2, so every $\binom{2}{4} = 0$.

Final answer is 0.

This shows that incidental pair groupings do not affect the result unless a line accumulates at least 4 distinct points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Every pair of points is processed once, and set insertions are amortized constant |
| Space | $O(n^2)$ | In worst case, every pair contributes to a line entry |

With $n \le 400$, the total pair count is at most 160,000, which fits comfortably within time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd
    from collections import defaultdict

    def norm_line(x1, y1, x2, y2):
        A = y2 - y1
        B = x1 - x2
        C = A * x1 + B * y1
        g = gcd(gcd(abs(A), abs(B)), abs(C))
        if g:
            A //= g
            B //= g
            C //= g
        if A < 0 or (A == 0 and B < 0):
            A, B, C = -A, -B, -C
        return (A, B, C)

    def comb4(k):
        return k * (k - 1) * (k - 2) * (k - 3) // 24 if k >= 4 else 0

    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    lines = defaultdict(set)

    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            key = norm_line(x1, y1, x2, y2)
            lines[key].add(i)
            lines[key].add(j)

    return str(sum(comb4(len(s)) for s in lines.values()))

assert run("5\n1 1\n2 2\n3 3\n4 4\n5 5\n") == "5", "all collinear"
assert run("4\n1 1\n1 2\n2 1\n2 2\n") == "0", "grid no collinearity"
assert run("4\n0 0\n1 1\n2 2\n3 3\n") == "1", "single quadruple"
assert run("5\n0 0\n1 0\n2 0\n3 0\n0 1\n") == "1", "one line of 4 points"
assert run("3\n0 0\n1 1\n2 3\n") == "0", "insufficient points"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all points on a line | 5 | full combinatorial explosion |
| grid points | 0 | no accidental collinearity |
| 4 collinear points | 1 | minimal valid case |
| 5 points with one line of 4 | 1 | mixed structure |
| 3 points | 0 | boundary below threshold |

## Edge Cases

A critical edge case is when many points lie on the same vertical line. For example:

```
4
0 0
0 1
0 2
0 3
```

Every pair produces a vertical line with identical normalized representation. The set accumulates all four points, and the algorithm computes $\binom{4}{4} = 1$, which matches the correct answer. A slope-based approach without normalization would fail here due to division by zero.

Another case is when points form multiple overlapping lines sharing points but not all collinear together. The set-based grouping ensures each geometric line is treated independently, and overlapping contributions do not interfere because quadruples are counted only within each distinct line group.
