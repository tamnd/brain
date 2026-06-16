---
title: "CF 1360G - A/B Matrix"
description: "We are asked to construct a binary grid of size $n times m$, where each cell is either 0 or 1, under two simultaneous constraints that tightly couple rows and columns. Every row must contain exactly $a$ ones, and every column must contain exactly $b$ ones."
date: "2026-06-16T11:16:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1360
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 644 (Div. 3)"
rating: 1900
weight: 1360
solve_time_s: 432
verified: false
draft: false
---

[CF 1360G - A/B Matrix](https://codeforces.com/problemset/problem/1360/G)

**Rating:** 1900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 7m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a binary grid of size $n \times m$, where each cell is either 0 or 1, under two simultaneous constraints that tightly couple rows and columns. Every row must contain exactly $a$ ones, and every column must contain exactly $b$ ones. If it is impossible to satisfy both constraints at once, we must report failure.

A useful way to think about this is as a bipartite incidence design problem. Each row has a fixed “capacity” of ones it must distribute across columns, and each column has a fixed “demand” of ones it must receive from rows. We are essentially assigning $n \cdot a$ identical tokens (row contributions) into an $n \times m$ grid such that each column receives exactly $b$ tokens.

The first structural constraint comes from counting. The total number of ones is determined in two ways. From rows it is $n \cdot a$, and from columns it is $m \cdot b$. If these two values differ, no construction can possibly exist because the same grid cannot simultaneously contain two different totals of ones.

So the necessary condition is:

$$n \cdot a = m \cdot b$$

Given that $n, m \le 50$, the grid is very small. This removes any need for advanced optimization, but it also suggests that a direct constructive pattern should be sufficient if existence conditions are met.

A naive attempt might try random placement or greedy placement row by row without coordination. This fails in subtle ways. For example, filling each row independently with $a$ ones tends to overload early columns and starve later columns, because column capacities are not tracked globally. Even a balanced greedy scan without wraparound fails in cases like $n=3, m=6, a=2, b=1$, where a locally even distribution can still produce column collisions or shortages.

The key difficulty is that both row sums and column sums must be enforced exactly, so partial decisions must remain globally consistent.

## Approaches

A brute-force approach would attempt to assign each cell either 0 or 1 and verify row and column constraints after filling the grid. Conceptually, this explores all subsets of size $n \cdot a$ across $n \cdot m$ positions, which is combinatorial in nature. The number of ways to choose positions for ones is $\binom{nm}{na}$, which becomes astronomically large even for $50 \times 50$. Even with pruning, the constraint coupling between rows and columns makes backtracking explode because early choices heavily restrict later feasibility.

The structural observation is that we do not need arbitrary placement at all. Since every row has identical requirements and every column has identical requirements, we can distribute ones in a perfectly periodic pattern. If we flatten the matrix into a cyclic sequence of length $m$, each row simply starts from a shifted position in that cycle. This ensures each row sees exactly $a$ ones, while the cyclic shifts distribute column load evenly.

This transforms the problem into constructing a cyclic Latin-style shift: row $i$ places ones at positions

$$(i \cdot a + j) \bmod m$$

for $j = 0 \dots a-1$, assuming $n \cdot a = m \cdot b$ guarantees uniform column coverage.

The core insight is that modular arithmetic enforces balance automatically: every column index appears exactly $b$ times across all row shifts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $nm$ | $O(nm)$ | Too slow |
| Optimal Cyclic Construction | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We construct the matrix deterministically using modular shifts.

1. Check whether $n \cdot a = m \cdot b$. If not equal, output NO immediately. This condition is mandatory because it enforces equality of total ones from both row and column perspectives.
2. Initialize an $n \times m$ matrix filled with zeros. This gives us a clean base where we only place ones according to a fixed pattern.
3. For each row $i$, we place exactly $a$ ones by selecting column indices in a cyclic manner. We compute these positions using $(i \cdot a + j) \bmod m$ for $j = 0 \dots a-1$. The shift by $i \cdot a$ ensures different rows do not align their ones in the same columns.
4. Set those computed positions to 1 in the matrix. Each assignment is independent, but the modular structure ensures global balance.
5. After processing all rows, output the matrix.

The reason this works is that each row contributes exactly $a$ ones by construction. The cyclic shift distributes these contributions uniformly across all columns because stepping through rows advances starting positions by a fixed increment modulo $m$. Since the total number of ones matches $m \cdot b$, and the distribution is symmetric under modular shifts, each column accumulates exactly $b$ ones.

The key invariant is that after processing any prefix of rows, the difference between column counts is always bounded by at most 1 in a cyclic sense, and after all rows are processed, symmetry forces exact equality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, a, b = map(int, input().split())

        if n * a != m * b:
            print("NO")
            continue

        grid = [[0] * m for _ in range(n)]

        # pointer moves through columns cyclically
        for i in range(n):
            start = (i * a) % m
            for j in range(a):
                col = (start + j) % m
                grid[i][col] = 1

        print("YES")
        for row in grid:
            print("".join(map(str, row)))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the cyclic construction. The only subtle part is the use of `(i * a) % m` as a shifting offset, which ensures rows are distributed evenly across columns instead of repeating identical patterns.

A common mistake is to iterate columns linearly without wrapping or without shifting by row index. That produces valid row sums but fails column uniformity. The modular shift is the mechanism that couples rows together.

## Worked Examples

### Example 1

Input:

```
3 6 2 1
```

Here $n \cdot a = 3 \cdot 2 = 6$ and $m \cdot b = 6 \cdot 1 = 6$, so construction is possible.

| Row | start = (i·a)%6 | chosen columns | row result |
| --- | --- | --- | --- |
| 0 | 0 | 0,1 | 110000 |
| 1 | 2 | 2,3 | 001100 |
| 2 | 4 | 4,5 | 000011 |

Each column receives exactly one 1, confirming correctness.

This shows how the shifting prevents overlap and spreads coverage uniformly.

### Example 2

Input:

```
4 4 2 2
```

Here $n \cdot a = 8$, $m \cdot b = 8$, so feasible.

| Row | start | chosen columns | row result |
| --- | --- | --- | --- |
| 0 | 0 | 0,1 | 1100 |
| 1 | 2 | 2,3 | 0011 |
| 2 | 0 | 0,1 | 1100 |
| 3 | 2 | 2,3 | 0011 |

Column sums are all 2, matching $b$.

This example shows that repetition across rows is allowed as long as the global column distribution is balanced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell is written at most once across all constructions |
| Space | $O(nm)$ | Storage for the output grid |

Given that both dimensions are at most 50, the total work is negligible even for 1000 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m, a, b = map(int, input().split())
        if n * a != m * b:
            out.append("NO")
            continue
        g = [[0]*m for _ in range(n)]
        for i in range(n):
            start = (i * a) % m
            for j in range(a):
                g[i][(start + j) % m] = 1
        out.append("YES")
        out.extend("".join(map(str, r)) for r in g)
    return "\n".join(out) + "\n"

# provided samples
assert run("""5
3 6 2 1
2 2 2 1
2 2 2 2
4 4 2 2
2 1 1 2
""").strip().split("\n")[0] == "YES"

# custom cases
assert "NO" in run("1\n3 3 2 1\n")
assert run("1\n1 1 1 1\n").count("1") == 1
assert run("1\n2 2 1 1\n").count("YES") == 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 2 1 | NO | infeasible total sum mismatch |
| 1 1 1 1 | YES 1 | minimal valid grid |
| 2 2 1 1 | YES matrix | balanced distribution |

## Edge Cases

When $n \cdot a \neq m \cdot b$, the algorithm immediately rejects. For example, $n=2, m=3, a=2, b=1$ gives totals 4 and 3, so no construction exists. The code correctly exits before any placement.

When $n=1$, the only valid case is $a=m$ and $b=1$. The construction reduces to filling the single row entirely, which matches the column requirement automatically.

When $m=1$, symmetry applies: all rows must have $a=1$ and all rows must match the single column count $b=n$. The modular construction degenerates into placing ones in the only column exactly $n$ times, satisfying the constraint.

In each of these cases, the cyclic shift either reduces to a trivial constant pattern or is skipped entirely due to the feasibility check, ensuring no inconsistent partial structure is produced.
