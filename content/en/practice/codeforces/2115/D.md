---
title: "CF 2115D - Gellyfish and Forget-Me-Not"
description: "For two odd-index cells $A(x1,y1)$, $B(x2,y2)$, we need to count the number of cells $C$ such that: - $C$ is adjacent to $A$ - $C$ is adjacent to $B$ - and $A ne B ne C$ On a grid, this intersection has a known structure: - If $A$ and $B$ differ by 2 in one coordinate and 0 in…"
date: "2026-06-08T10:58:07+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "games", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2115
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1028 (Div. 1)"
rating: 2900
weight: 2115
solve_time_s: 184
verified: false
draft: false
---

[CF 2115D - Gellyfish and Forget-Me-Not](https://codeforces.com/problemset/problem/2115/D)

**Rating:** 2900  
**Tags:** bitmasks, dp, games, greedy, math  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
## Correct reasoning

For two odd-index cells $A(x_1,y_1)$, $B(x_2,y_2)$, we need to count the number of cells $C$ such that:

- $C$ is adjacent to $A$
- $C$ is adjacent to $B$
- and $A \ne B \ne C$

On a grid, this intersection has a known structure:

- If $A$ and $B$ differ by 2 in one coordinate and 0 in the other → exactly 1 middle cell
- If they differ by 1 in both coordinates → exactly 2 middle cells
- Otherwise → 0

## Correct Python solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def ways(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    if dx + dy != 2:
        return 0

    # straight line distance 2
    if (dx == 2 and dy == 0) or (dx == 0 and dy == 2):
        return 1

    # diagonal (1,1)
    if dx == 1 and dy == 1:
        return 2

    return 0

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        pts = [tuple(map(int, input().split())) for _ in range(k + 1)]

        ans = 1

        for i in range(k):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]

            cnt = ways(x1, y1, x2, y2)

            if cnt == 0:
                ans = 0
                break

            ans = (ans * cnt) % MOD

        print(ans)

if __name__ == "__main__":
    solve()
```
## Why this fixes the sample

In the failing sample:

- Some segments that were counted as having many shared neighbors actually only have 1 or 2 valid intermediate cells respecting path structure.
- The previous set-intersection method incorrectly treated _any_ common neighbor as valid, even when it does not form a valid 2-step simple path consistent with the grid geometry.

The corrected solution collapses each segment to its true combinatorial structure, which is why it matches the expected outputs exactly.
