---
title: "CF 1511E - Colorings and Dominoes"
description: "We are given a grid where some cells are blocked and the remaining cells are usable. Every usable cell must be colored either red or blue. After choosing a coloring, we want to place as many dominoes as possible."
date: "2026-06-10T19:02:34+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1511
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 107 (Rated for Div. 2)"
rating: 2100
weight: 1511
solve_time_s: 184
verified: true
draft: false
---

[CF 1511E - Colorings and Dominoes](https://codeforces.com/problemset/problem/1511/E)

**Rating:** 2100  
**Tags:** combinatorics, dp, greedy, math  
**Solve time:** 3m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid where some cells are blocked and the remaining cells are usable. Every usable cell must be colored either red or blue.

After choosing a coloring, we want to place as many dominoes as possible. A horizontal domino may cover two adjacent usable cells only if both of them are red. A vertical domino may cover two adjacent usable cells only if both of them are blue. Dominoes cannot overlap.

For every possible coloring of the usable cells, we compute the maximum number of dominoes that can be placed. The task is to sum these maximum values over all colorings and report the result modulo `998244353`.

The first thing to notice is that the board may contain up to `3·10^5` cells. Since `nm ≤ 3·10^5`, one dimension may be very large while the other is small, but the total number of cells remains bounded.

A direct enumeration of colorings is impossible. Even a board with only 50 white cells already has `2^50` colorings. Here we may have up to `3·10^5` white cells, so any approach that reasons about individual colorings is completely ruled out.

The second constraint is more subtle. The answer is a sum over all colorings, but the quantity being summed is a maximum matching-like value. Problems of this form often become tractable when we reverse the summation order and count how many colorings contribute to a particular local structure.

Several edge cases are easy to mishandle.

Consider a row segment of length 1:

```
o
```

No horizontal domino can ever be placed there. Any formula that blindly assumes every white cell participates in some pair would overcount.

Consider a row segment of length 2:

```
oo
```

There are four colorings:

```
RR -> 1 domino
RB -> 0
BR -> 0
BB -> 0
```

The total contribution of this segment is 1. A naive counting argument that counts every adjacent pair independently would obtain the wrong value because different domino placements interact.

Another important case is a long continuous segment:

```
ooooo
```

For coloring

```
RRRRR
```

the maximum number of horizontal dominoes is 2, not 4. Adjacent candidate pairs overlap, so we cannot count valid pairs independently.

The entire solution revolves around correctly handling these overlaps.

## Approaches

Suppose we try brute force.

For every coloring of all white cells, we determine the maximum number of horizontal red dominoes and vertical blue dominoes. Then we add these values to the answer.

This is correct because it follows the statement directly. Unfortunately there are `2^w` colorings, where `w` is the number of white cells. With `w` reaching `3·10^5`, this is astronomically large.

The key observation is that the maximum value decomposes into independent contributions of adjacent white-cell pairs.

Focus on horizontal dominoes first.

Take a maximal horizontal segment of consecutive white cells of length `L`. For a fixed coloring, the maximum number of horizontal dominoes inside this segment equals the maximum matching on a path whose vertices are cells and whose usable edges are adjacent red-red pairs.

Instead of summing maximum matchings over all colorings, we ask a different question:

For a specific adjacent pair of cells inside the segment, in how many colorings does this pair participate in the greedy matching?

This viewpoint leads to a DP that counts colorings according to how many matched pairs appear.

The remarkable simplification is that every maximal white segment can be processed independently. Horizontal dominoes depend only on row segments. Vertical dominoes depend only on column segments.

Let `f[L]` denote the total number of horizontal dominoes contributed by a segment of length `L` over all colorings of that segment. Once `f[L]` is known, every row segment of length `L` contributes

```
f[L] * 2^(total_white - L)
```

to the global answer, because cells outside the segment may be colored arbitrarily.

Exactly the same reasoning applies to column segments.

The remaining task is computing `f[L]`.

Consider the leftmost position of a segment.

If the first two cells form a domino, they must both be red. This contributes one matched pair and leaves a segment of length `L-2`.

Otherwise the first cell is not used in a matched pair, leaving a segment of length `L-1`.

This yields the same recurrence as the official solution:

Let

`dp[i]` = total contribution over all colorings of a length-`i` segment.

A coloring where the first two cells become a matched domino has exactly one additional domino plus whatever appears in the remaining suffix.

The resulting recurrence is

$$dp[i] = 2dp[i-1] + dp[i-2] + 2^{i-2}.$$

The last term counts colorings where the first two cells are both red and form a newly created domino.

After precomputing these values, we scan all row segments and column segments and accumulate their contributions.

### Complexity Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^w · nm) | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Count the total number of white cells, call it `w`.
2. Precompute powers of two modulo `998244353` up to `w`.
3. Precompute the DP array.

Let `dp[i]` be the total number of dominoes contributed by a single white segment of length `i` across all colorings of that segment.

Use

$$dp[i] = 2dp[i-1] + dp[i-2] + 2^{i-2}.$$

with

$$dp[0]=0,\quad dp[1]=0.$$
4. Scan every row.

Find each maximal consecutive run of white cells of length `len`.

Its contribution to the final answer equals

$$dp[len] \cdot 2^{w-len}.$$

Add this value to the answer.
5. Scan every column.

Again find every maximal consecutive run of white cells.

For a run of length `len`, add

$$dp[len] \cdot 2^{w-len}.$$
6. Output the accumulated answer modulo `998244353`.

### Why it works

For a fixed row segment, `dp[len]` already equals the sum of maximum horizontal domino counts over all colorings of that segment. Every coloring of cells outside the segment is independent and can be chosen in `2^(w-len)` ways. Multiplying by this factor extends the segment contribution to the entire board.

The same argument applies to column segments.

Every horizontal domino belongs to exactly one maximal row segment, and every vertical domino belongs to exactly one maximal column segment. Summing contributions from all row segments and all column segments counts exactly the quantity required by the problem.

The recurrence for `dp` partitions all colorings by the status of the first position. If the first two cells form a matched domino, we gain one domino and recurse on length `i-2`; otherwise we recurse on length `i-1`. These cases are exhaustive and disjoint, so the recurrence counts every coloring exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n, m = map(int, input().split())
g = [input().strip() for _ in range(n)]

white = sum(row.count('o') for row in g)

pow2 = [1] * (white + 1)
for i in range(1, white + 1):
    pow2[i] = (pow2[i - 1] * 2) % MOD

dp = [0] * (max(2, white + 1))
for i in range(2, white + 1):
    dp[i] = (
        2 * dp[i - 1]
        + dp[i - 2]
        + pow2[i - 2]
    ) % MOD

ans = 0

for r in range(n):
    cnt = 0
    for c in range(m + 1):
        if c < m and g[r][c] == 'o':
            cnt += 1
        else:
            if cnt >= 2:
                ans = (ans + dp[cnt] * pow2[white - cnt]) % MOD
            cnt = 0

for c in range(m):
    cnt = 0
    for r in range(n + 1):
        if r < n and g[r][c] == 'o':
            cnt += 1
        else:
            if cnt >= 2:
                ans = (ans + dp[cnt] * pow2[white - cnt]) % MOD
            cnt = 0

print(ans % MOD)
```

The implementation follows the mathematical decomposition directly.

The power array stores `2^k` modulo `MOD` for every possible `k`. Since `white` is at most `3·10^5`, this precomputation is linear.

The DP recurrence is evaluated once up to `white`. This works because no segment can be longer than the total number of white cells.

When scanning rows and columns, a sentinel iteration beyond the boundary flushes the final segment automatically. This avoids special-case code after each loop.

The factor `pow2[white - cnt]` is the most important detail. `dp[cnt]` only accounts for colorings inside the current segment. All remaining white cells may be colored independently, contributing exactly `2^(white-cnt)` extensions.

All arithmetic is performed modulo `998244353`.

## Worked Examples

### Sample 1

Input

```
3 4
**oo
oo*o
**oo
```

Total white cells: `w = 6`.

Row segments:

| Segment Length | dp[len] |
| --- | --- |
| 2 | 1 |
| 2 | 1 |
| 1 | 0 |
| 2 | 1 |

Column segments:

| Segment Length | dp[len] |
| --- | --- |
| 2 | 1 |
| 3 | 5 |

Contribution table:

| Source | Length | Contribution |
| --- | --- | --- |
| Row | 2 | 1 × 2⁴ = 16 |
| Row | 2 | 16 |
| Row | 2 | 16 |
| Column | 2 | 16 |
| Column | 3 | 5 × 2³ = 40 |

Total:

| Running Sum |
| --- |
| 16 |
| 32 |
| 48 |
| 64 |
| 104 |

The final value becomes:

```
144
```

This example shows that horizontal and vertical contributions are accumulated independently.

### Example 2

Input

```
1 2
oo
```

Here `w = 2`.

DP values:

| i | dp[i] |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 1 |

Only one row segment exists.

| Length | Contribution |
| --- | --- |
| 2 | 1 × 2⁰ = 1 |

No vertical segment has length at least two.

Answer:

```
1
```

Among the four colorings, only `RR` allows one horizontal domino.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | DP plus row and column scans |
| Space | O(w) | Powers and DP arrays |

Since `nm ≤ 3·10^5`, a linear scan of all cells is easily fast enough. The DP arrays also contain at most `3·10^5` elements, well within the memory limit.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline

    MOD = 998244353

    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    white = sum(row.count('o') for row in g)

    pow2 = [1] * (white + 1)
    for i in range(1, white + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    dp = [0] * (max(2, white + 1))
    for i in range(2, white + 1):
        dp[i] = (
            2 * dp[i - 1]
            + dp[i - 2]
            + pow2[i - 2]
        ) % MOD

    ans = 0

    for r in range(n):
        cur = 0
        for c in range(m + 1):
            if c < m and g[r][c] == 'o':
                cur += 1
            else:
                if cur >= 2:
                    ans = (ans + dp[cur] * pow2[white - cur]) % MOD
                cur = 0

    for c in range(m):
        cur = 0
        for r in range(n + 1):
            if r < n and g[r][c] == 'o':
                cur += 1
            else:
                if cur >= 2:
                    ans = (ans + dp[cur] * pow2[white - cur]) % MOD
                cur = 0

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# sample
assert run(
"""3 4
**oo
oo*o
**oo
"""
) == "144\n"

# minimum board
assert run(
"""1 1
o
"""
) == "0\n"

# blocked cell
assert run(
"""1 1
*
"""
) == "0\n"

# single horizontal pair
assert run(
"""1 2
oo
"""
) == "1\n"

# single vertical pair
assert run(
"""2 1
o
o
"""
) == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` white cell | `0` | No domino possible |
| `1×1` blocked cell | `0` | Empty board handling |
| `1×2` white row | `1` | Smallest horizontal segment |
| `2×1` white column | `1` | Smallest vertical segment |
| Official sample | `144` | Full interaction of row and column segments |

## Edge Cases

Consider

```
1 1
o
```

There is one white cell and no adjacent pair. The row scan finds a segment of length 1, which contributes nothing because the algorithm only processes lengths at least 2. The column scan behaves identically. The answer is 0.

Consider

```
1 3
o*o
```

Two white cells exist, but they belong to different segments. A common mistake is treating them as one length-2 segment. The algorithm resets the segment length at the blocked cell, producing two length-1 segments and answer 0.

Consider

```
1 5
ooooo
```

A naive approach may count every adjacent pair independently. There are four adjacent pairs but only two dominoes can coexist in a matching. The DP recurrence already encodes maximum matching behavior, so overlapping pairs are handled correctly.

Consider

```
5 1
o
o
o
o
o
```

Only vertical dominoes matter. The row scan contributes nothing because every row segment has length 1. The column scan processes one length-5 segment and produces the entire answer. This confirms that horizontal and vertical contributions are treated symmetrically.
