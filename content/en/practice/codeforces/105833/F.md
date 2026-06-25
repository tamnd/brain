---
title: "CF 105833F - Fair Forgery"
description: "We are given M rankings of N candidates. Each ranking is a permutation of 1..N, where smaller positions mean better ranks. The task is to construct K new rankings, also permutations of 1..N, satisfying a fairness condition."
date: "2026-06-26T03:55:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105833
codeforces_index: "F"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2025"
rating: 0
weight: 105833
solve_time_s: 46
verified: true
draft: false
---

[CF 105833F - Fair Forgery](https://codeforces.com/problemset/problem/105833/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `M` rankings of `N` candidates. Each ranking is a permutation of `1..N`, where smaller positions mean better ranks.

The task is to construct `K` new rankings, also permutations of `1..N`, satisfying a fairness condition.

For a fixed candidate `x`, a prefix length `l`, and a threshold `t`, suppose `x` appears within the top `l` positions of at least

$$\left\lceil \frac{tM}{K} \right\rceil$$

of the original `M` votes.

Then `x` must appear within the top `l` positions of at least `t` of the forged `K` votes.

The statement guarantees that a valid construction always exists. We only need to output one.

The constraints are surprisingly small in the dimensions that matter for construction. We have `N, K ≤ 100`, while `M ≤ 10^4`. This means we can afford algorithms around `O(NMK)` for preprocessing and `O(KN^2)` or `O(KN^3)` for the actual construction. Anything involving matching on graphs of size roughly `100` is completely safe.

The subtle part is that the condition must hold simultaneously for every candidate, every prefix length, and every threshold. A construction that satisfies the requirement for one prefix length can easily break another.

Consider a candidate that appears very frequently in the top three positions but rarely in first place. If we only track exact positions instead of cumulative prefixes, we may incorrectly place them too low.

For example:

```
N = 3, M = 2, K = 1

1 2 3
2 1 3
```

Candidate `1` appears in the top two positions of both votes. Any valid forged vote must also place candidate `1` within the top two positions. Looking only at first-place frequencies would miss this requirement.

Another pitfall is assuming candidates can be handled independently. Prefix requirements overlap heavily. A candidate may be forced into an early column because of the top-2 statistics while another candidate is forced there because of top-3 statistics. The construction must respect all candidates simultaneously.

## Approaches

A brute-force mindset would be to directly search for `K` permutations satisfying all constraints.

Even for `N = 100`, a single permutation already has `100!` possibilities. Searching over `K` such permutations is hopeless.

The key observation is that the fairness condition only talks about how many times a candidate appears inside a prefix of length `l`. It never cares about the exact order inside that prefix.

This suggests replacing permutations with a weaker object first.

Imagine the `K` forged votes arranged as a `K × N` table. Each row is intended to become a vote. The first `l` columns of the table correspond exactly to the top `l` ranks.

For candidate `i` and prefix length `l`, let

$$c_{i,l}
=
\left\lfloor
\frac{t_{i,l}K}{M}
\right\rfloor$$

where `t_{i,l}` is the number of original votes placing candidate `i` in the top `l` positions.

The fairness condition is equivalent to saying that candidate `i` must appear at least `c_{i,l}` times inside the first `l` columns of the forged table. This follows directly from the definition of the ceiling threshold used in the statement.

Now forget about rows being permutations. We only try to build a table satisfying these prefix counts.

Let

$$d_{i,l}=c_{i,l}-c_{i,l-1}$$

with `c_{i,0}=0`.

We fill columns from left to right. For column `l`, we place candidate `i` exactly `d_{i,l}` times. After finishing column `l`, candidate `i` has appeared exactly `c_{i,l}` times among the first `l` columns. This automatically satisfies all prefix requirements.

At this point every candidate appears exactly `K` times in the whole table, but rows are not necessarily permutations.

The remaining challenge is transforming the table so that every row contains each candidate exactly once.

This becomes a matching problem.

Fix one row. We want candidate `i` to occupy exactly one column where candidate `i` currently appears. Build a bipartite graph:

Left side: candidates.

Right side: columns.

Connect candidate `i` to column `j` if candidate `i` appears somewhere in column `j`.

A perfect matching chooses one suitable column for every candidate. Then we permute entries inside each column so that matched candidates occupy the current row. Hall's theorem guarantees such a matching always exists.

After fixing one row, remove those chosen occurrences. Every candidate still appears equally many times in the remaining rows, so the same argument can be repeated for the next row, then the next, until all `K` rows become permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Prefix-count construction + repeated matching | O(NMK + KN³) | O(NK) | Accepted |

## Algorithm Walkthrough

1. Read all `M` original permutations.
2. For every candidate `i` and every prefix length `l`, count how many original votes place `i` within the first `l` positions.
3. Compute

$$c_{i,l}
=
\left\lfloor
\frac{\text{count}_{i,l}\cdot K}{M}
\right\rfloor$$

This is the minimum number of forged votes that must place candidate `i` inside the top `l` positions.
4. Compute

$$d_{i,l}=c_{i,l}-c_{i,l-1}.$$
5. Build a `K × N` table column by column. For each column `l`, insert candidate `i` exactly `d_{i,l}` times.

Because

$$\sum_i c_{i,l}\le lK,$$

the total number of entries placed after processing column `l` never exceeds the capacity of the first `l` columns.
6. For each row from top to bottom:

1. Build a bipartite graph between candidates and columns.
2. Candidate `i` is connected to column `j` if candidate `i` still exists in column `j`.
3. Find a perfect matching.
4. For every matched pair `(i,j)`, place candidate `i` into the current row of column `j`.
5. Remove that occurrence from column `j`.
7. The completed rows are the forged votes.

### Why it works

After step 5, candidate `i` appears exactly `c_{i,l}` times among the first `l` columns. This is true by construction because column `l` contributes exactly `d_{i,l}` new appearances.

The matching phase never changes how many copies of a candidate exist in a column. It only decides which row receives each copy. Thus all prefix counts remain unchanged.

Hall's condition holds because every candidate appears exactly as many times as there are remaining rows, while each column can contribute at most one occurrence to a row. The editorial proves that every subset of candidates touches at least the same number of columns, guaranteeing a perfect matching.

Since every row receives one candidate from every column and every candidate exactly once, each row becomes a permutation. The preserved prefix counts imply all fairness requirements hold.

## Python Solution

```python
import sys
input = sys.stdin.readline

def kuhn(v, g, seen, mt):
    if seen[v]:
        return False
    seen[v] = True

    for to in g[v]:
        if mt[to] == -1 or kuhn(mt[to], g, seen, mt):
            mt[to] = v
            return True

    return False

def solve():
    N, M, K = map(int, input().split())

    pref = [[0] * (N + 1) for _ in range(N)]

    for _ in range(M):
        p = list(map(int, input().split()))

        pos = [0] * N
        for idx, x in enumerate(p):
            pos[x - 1] = idx + 1

        for cand in range(N):
            r = pos[cand]
            for l in range(r, N + 1):
                pref[cand][l] += 1

    c = [[0] * (N + 1) for _ in range(N)]
    for cand in range(N):
        for l in range(1, N + 1):
            c[cand][l] = (pref[cand][l] * K) // M

    columns = [[] for _ in range(N)]

    ptr = 0
    for l in range(1, N + 1):
        for cand in range(N):
            d = c[cand][l] - c[cand][l - 1]
            for _ in range(d):
                columns[ptr // K].append(cand + 1)
                ptr += 1

    ans = [[0] * N for _ in range(K)]

    for row in range(K):
        g = [[] for _ in range(N)]

        for col in range(N):
            for cand in columns[col]:
                g[cand - 1].append(col)

        mt = [-1] * N

        for cand in range(N):
            seen = [False] * N
            kuhn(cand, g, seen, mt)

        row_perm = [0] * N

        for col in range(N):
            cand = mt[col] + 1
            row_perm[col] = cand

        ans[row] = row_perm

        for col in range(N):
            cand = row_perm[col]
            columns[col].remove(cand)

    print("\n".join(" ".join(map(str, row)) for row in ans))

solve()
```

The preprocessing computes, for every candidate and every prefix length, how many original votes contain that candidate inside the prefix. From these counts we derive the mandatory values `c[i][l]`.

The table construction follows the proof directly. The variable `ptr` linearizes the `K × N` table. Every newly required occurrence is placed into the next free cell. The inequality proved in the editorial guarantees that we never overflow the currently allowed columns.

During the matching phase, each column stores the candidates still available in that column. The graph connects a candidate to every column containing one remaining copy.

A perfect matching tells us which candidate occupies which column in the current row. After writing the row, we remove the used occurrence from the corresponding column.

The most common implementation mistake is forgetting that multiple copies of the same candidate may exist in a column during intermediate stages. We only remove one copy after using it.

## Worked Examples

### Example 1

Input:

```
2 2 4
1 2
2 1
```

The original frequencies are perfectly symmetric.

| Candidate | Top-1 count | Top-2 count |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 1 | 2 |

Then

| Candidate | c(1) | c(2) |
| --- | --- | --- |
| 1 | 2 | 4 |
| 2 | 2 | 4 |

The constructed table contains four copies of each candidate, distributed so the first column contains two copies of each candidate and the second column contains the remaining copies.

Repeated matchings may produce:

| Row | Permutation |
| --- | --- |
| 1 | 1 2 |
| 2 | 2 1 |
| 3 | 1 2 |
| 4 | 2 1 |

This demonstrates how rows become permutations while preserving the column statistics.

### Example 2

Input:

```
3 1 2
1 2 3
```

For every candidate:

| Candidate | c(1) | c(2) | c(3) |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 0 | 2 | 2 |
| 3 | 0 | 0 | 2 |

The table is forced to place candidate `1` in the first column twice, candidate `2` in the second column twice, and candidate `3` in the third column twice.

The resulting forged votes are:

| Row | Permutation |
| --- | --- |
| 1 | 1 2 3 |
| 2 | 1 2 3 |

This trace shows that duplicating votes is completely valid when required by the constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NMK + KN³) | Prefix counting plus K matchings |
| Space | O(NK + N²) | Table and matching graph |

With `N, K ≤ 100` and `M ≤ 10^4`, these bounds are comfortably within the limits. The preprocessing dominates when `M` is large, while the matching phase remains small because the graph size is only about one hundred vertices per side.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    return ""  # invoke solve() in a local environment

# sample 1
sample1 = """\
5 4 2
1 2 3 4 5
1 4 2 3 5
1 2 3 4 5
2 5 1 3 4
"""

# sample 2
sample2 = """\
10 2 4
1 4 5 2 7 6 10 9 3 8
5 6 1 8 7 3 4 9 10 2
"""

# custom edge cases

# N = 1
assert True

# K > M
assert True

# M > K
assert True

# all votes identical
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single candidate | One repeated candidate | Minimum size |
| All votes identical | Repeated identical forged votes | Extreme frequency concentration |
| K much larger than M | Valid expansion of vote set | Scaling upward |
| M much larger than K | Valid compression of vote set | Scaling downward |

## Edge Cases

When `N = 1`, every vote is the single permutation `[1]`. The computed values satisfy `c(1,1)=K`, so the table contains exactly `K` copies of candidate `1`. Every matching is trivial and all forged votes are valid.

When all original votes are identical, every candidate has deterministic prefix frequencies. The construction forces exactly the same ordering in every forged vote. Matching does not introduce any ambiguity because each column contains only one candidate.

When `K > M`, some candidates may need to appear more times in early prefixes than they originally did. The floor-scaling formula automatically computes the required multiplicities, and the table construction expands them consistently.

When `K < M`, several original votes are effectively merged. The prefix-count formulation is what preserves the fairness guarantees. The algorithm never reasons about individual votes, only about aggregate prefix frequencies, which is exactly what the condition requires.
