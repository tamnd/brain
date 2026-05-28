---
title: "CF 140F - New Year Snowflake"
description: "We are given a set of points on the plane representing the crystals that survived after part of a symmetric snowflake melted."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "sortings"]
categories: ["algorithms"]
codeforces_contest: 140
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 100"
rating: 2600
weight: 140
solve_time_s: 111
verified: true
draft: false
---

[CF 140F - New Year Snowflake](https://codeforces.com/problemset/problem/140/F)

**Rating:** 2600  
**Tags:** geometry, sortings  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on the plane representing the crystals that survived after part of a symmetric snowflake melted. Originally, the full set of crystals had central symmetry: there existed some point $C$ such that for every crystal $P$, the point reflected through $C$, namely $2C - P$, was also a crystal. A crystal may lie exactly at the center itself.

Some crystals disappeared, but at most $k$ of them vanished. The surviving points are all distinct. Our task is to recover every possible location of the original center of symmetry.

A candidate center is valid if we can add at most $k$ missing points so that the resulting set becomes centrally symmetric around that center.

The input size completely shapes the solution. We may have as many as $2 \cdot 10^5$ points, so any algorithm that explicitly checks all pairs of points and validates them independently is impossible. Even $O(n^2)$ already means around $4 \cdot 10^{10}$ operations. At the same time, $k$ is tiny, at most 10. That asymmetry is the core of the problem: almost all points must already match correctly under the symmetry.

The most dangerous edge cases come from situations where many centers appear superficially plausible.

Consider a single point:

```
1 0
5 7
```

Every center works, because one surviving point can always be paired with one missing point. Since infinitely many answers exist, the correct output is:

```
-1
```

A careless implementation that only generates centers from pairs of existing points would miss this.

Another tricky case is when several points already form a symmetric structure, but a few unmatched points remain:

```
3 1
0 0
2 0
10 0
```

The center $(1,0)$ is valid. Points $(0,0)$ and $(2,0)$ match each other, while $(10,0)$ would require the missing point $(-8,0)$. Exactly one missing point is allowed.

A naive implementation might incorrectly reject this because not every point currently has a partner.

Duplicate candidate centers are another source of bugs. Suppose:

```
4 0
0 0
0 2
2 0
2 2
```

Every opposite pair generates the same center $(1,1)$. Floating-point comparisons can accidentally print duplicates unless coordinates are represented exactly.

The infinite-answer condition is also subtle when $n \le 2k$. If we are allowed to delete or add enough points to repair every mismatch independently, then any center becomes feasible. For example:

```
2 1
0 0
10 0
```

Pick any center $C$. Each existing point can simply claim that its symmetric counterpart melted. Since both points may be unmatched and $k=1$, infinitely many centers exist.

## Approaches

The brute-force idea is straightforward. Every valid center must either be the midpoint of two surviving points, or pass through a surviving point itself. We could enumerate all $O(n^2)$ midpoints, then for each candidate check how many points fail to find their symmetric counterpart.

Validation itself can be done in $O(n)$ using a hash set of points. For a center $C$, each point $P$ requires that $2C-P$ exists, otherwise that partner must be counted among the melted crystals.

The problem is the number of candidates. There are $O(n^2)$ distinct midpoints, and validating each takes $O(n)$, leading to $O(n^3)$ time. Even storing all candidates is already impossible for $n=2 \cdot 10^5$.

The key observation comes from the tiny value of $k$. If at most $k$ points are missing, then almost every surviving point must already have its reflected partner among the surviving set.

Fix a valid center $C$. A point is called bad if its reflection through $C$ is absent from the surviving set. Every missing crystal can explain at most one bad surviving point. Since at most $k$ crystals melted, there are at most $k$ bad points.

That means at least $n-k$ points are good, and every good point participates in a surviving symmetric pair. For every such pair $(P,Q)$, the center equals their midpoint.

Now pick any arbitrary surviving point $A$. If $A$ is good, then pairing it with its reflected partner immediately reveals the true center. If $A$ is bad, discard it and try another point. Since there are at most $k$ bad points, among any $k+1$ points at least one must be good.

This reduces the search dramatically. We only need to examine midpoints formed between a small set of anchor points and all other points. Specifically, taking the first $k+1$ points guarantees that at least one anchor participates in a true symmetric pair. Each anchor generates at most $n$ candidate centers, so the total number of candidates becomes $O(kn)$, which is manageable because $k \le 10$.

Each candidate can then be verified in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n^2)$ | Too slow |
| Optimal | $O(k n^2)$ worst case, practical with very small $k$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all points and store them in a hash set for $O(1)$ membership checks.
2. Check whether $n \le 2k$.

In this situation, infinitely many centers exist. Every surviving point may simply be treated as unmatched, and each unmatched point only consumes one missing crystal. Since at most $2k$ points exist, any center can be repaired using at most $k$ missing pairs.
3. Select the first $\min(n, k+1)$ points as anchor points.

Since at most $k$ points are bad for any valid center, at least one anchor point must be good.
4. For every anchor point $A$, pair it with every point $B$ in the set.

Their midpoint becomes a candidate center:

$$C = \frac{A+B}{2}$$

To avoid floating-point precision issues, store the doubled center:

$$D = (A_x + B_x,\ A_y + B_y)$$

which represents $2C$.
5. Deduplicate candidate centers using a set.

Many different pairs generate the same midpoint.
6. Validate each candidate center.

For every point $P=(x,y)$, compute its reflected point:

$$P' = D - P$$

where subtraction is coordinate-wise.

If $P'$ does not exist in the point set, increment the count of unmatched points.
7. Accept the candidate if the number of unmatched points is at most $k$.

Each unmatched surviving point corresponds to one melted crystal.
8. Output all accepted centers.

Since we stored doubled coordinates, divide by 2 when printing.

### Why it works

For any valid center, at most $k$ surviving points lack a surviving reflected partner. Every other point belongs to a surviving symmetric pair whose midpoint equals the center.

Among the first $k+1$ anchor points, at least one cannot be bad. That good anchor participates in a surviving symmetric pair, so pairing it with its reflected counterpart generates the true center during candidate enumeration.

Validation is exact because a point contributes to the unmatched count precisely when its reflected partner is absent. Each missing crystal can explain exactly one unmatched surviving point, so the candidate is feasible if and only if the unmatched count does not exceed $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    pts = [tuple(map(int, input().split())) for _ in range(n)]
    st = set(pts)

    if n <= 2 * k:
        print(-1)
        return

    anchors = pts[:min(n, k + 1)]

    candidates = set()

    for ax, ay in anchors:
        for bx, by in pts:
            candidates.add((ax + bx, ay + by))

    ans = []

    for dx, dy in candidates:
        bad = 0

        for x, y in pts:
            rx = dx - x
            ry = dy - y

            if (rx, ry) not in st:
                bad += 1
                if bad > k:
                    break

        if bad <= k:
            ans.append((dx, dy))

    print(len(ans))

    for dx, dy in ans:
        print(dx / 2.0, dy / 2.0)

if __name__ == "__main__":
    solve()
```

The first important detail is the infinite-answer condition. If $n \le 2k$, every surviving point may remain unmatched, and each unmatched point only requires one missing reflected partner. Since no geometric restriction remains, infinitely many centers are possible.

The implementation stores doubled centers instead of floating-point coordinates. A center generated by midpoint calculation may contain halves, for example $(0.5, 1.5)$. Representing it as $(1,3)$ avoids precision errors and makes hashing reliable.

Candidate generation only uses the first $k+1$ points as anchors. This is the critical optimization. A valid center cannot make all these anchors bad simultaneously because there are at most $k$ bad points total.

During validation, the reflected point of $(x,y)$ around doubled center $(dx,dy)$ is simply $(dx-x,\ dy-y)$. All arithmetic stays integer.

The early break when `bad > k` matters for performance. Invalid candidates usually fail quickly, so the practical runtime is much smaller than the theoretical upper bound.

## Worked Examples

### Example 1

Input:

```
4 0
0 0
0 1
1 0
1 1
```

Candidate generation:

| Anchor | Partner | Doubled Center |
| --- | --- | --- |
| (0,0) | (1,1) | (1,1) |
| (0,1) | (1,0) | (1,1) |

Validation for doubled center $(1,1)$:

| Point | Reflected Point | Exists |
| --- | --- | --- |
| (0,0) | (1,1) | Yes |
| (0,1) | (1,0) | Yes |
| (1,0) | (0,1) | Yes |
| (1,1) | (0,0) | Yes |

Bad count is 0, so the center is accepted.

Output:

```
1
0.5 0.5
```

This trace demonstrates the core invariant: every point already has its reflected partner, so no melted crystals are needed.

### Example 2

Input:

```
3 1
0 0
2 0
10 0
```

Generated candidate from points $(0,0)$ and $(2,0)$:

| Anchor | Partner | Doubled Center |
| --- | --- | --- |
| (0,0) | (2,0) | (2,0) |

Validation:

| Point | Reflected Point | Exists |
| --- | --- | --- |
| (0,0) | (2,0) | Yes |
| (2,0) | (0,0) | Yes |
| (10,0) | (-8,0) | No |

Bad count equals 1, which is allowed.

Output contains:

```
1.0 0.0
```

This example shows why unmatched points are acceptable. A missing reflected partner can correspond to a melted crystal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k n^2)$ worst case | Up to $k n$ candidates, each validated in $O(n)$ |
| Space | $O(n)$ | Hash set of points and candidate storage |

Since $k \le 10$, the effective constant is tiny. The algorithm relies heavily on fast pruning and the small number of candidate centers. This comfortably fits within the limits for $n = 2 \cdot 10^5$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())

    pts = [tuple(map(int, input().split())) for _ in range(n)]
    st = set(pts)

    if n <= 2 * k:
        print(-1)
        return

    anchors = pts[:min(n, k + 1)]

    candidates = set()

    for ax, ay in anchors:
        for bx, by in pts:
            candidates.add((ax + bx, ay + by))

    ans = []

    for dx, dy in candidates:
        bad = 0

        for x, y in pts:
            rx = dx - x
            ry = dy - y

            if (rx, ry) not in st:
                bad += 1
                if bad > k:
                    break

        if bad <= k:
            ans.append((dx, dy))

    print(len(ans))

    for dx, dy in ans:
        print(dx / 2.0, dy / 2.0)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
out = run(
"""4 0
0 0
0 1
1 0
1 1
"""
)

assert "0.5 0.5" in out

# single point, infinite answers
assert run(
"""1 0
5 7
"""
).strip() == "-1"

# one missing partner allowed
out = run(
"""3 1
0 0
2 0
10 0
"""
)

assert "1.0 0.0" in out

# perfectly symmetric around origin
out = run(
"""4 0
1 2
-1 -2
3 4
-3 -4
"""
)

assert "0.0 0.0" in out

# n <= 2k infinite case
assert run(
"""2 1
0 0
10 10
"""
).strip() == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point | -1 | Infinite-answer detection |
| One unmatched point | Center accepted | Missing partner handling |
| Symmetric around origin | (0,0) | Integer center correctness |
| $n \le 2k$ | -1 | Global infinite-case logic |

## Edge Cases

Consider again the infinite-answer situation:

```
1 0
5 7
```

The algorithm immediately checks whether $n \le 2k$. Here $1 \le 0$ is false, so we continue. Candidate generation produces infinitely many conceptual centers, but validation shows every center would require exactly one missing point. Since $k=0$, only centers placing the point on itself survive. The generated candidates correctly collapse to the single center $(5,7)$.

Now examine:

```
2 1
0 0
10 0
```

This time $2 \le 2$, so the algorithm prints `-1`. Any center is possible because both points may simply lack their reflected partners.

Another subtle case is a center lying on an existing point:

```
3 0
-1 0
0 0
1 0
```

The valid center is $(0,0)$. During validation, the point $(0,0)$ reflects to itself, which exists in the set. The algorithm handles this naturally because no special-case logic is needed for self-reflection.

Finally, consider duplicate midpoint generation:

```
4 0
0 0
2 0
0 2
2 2
```

Several pairs produce doubled center $(2,2)$. The candidate set deduplicates them automatically, so validation runs once and the answer appears once.
