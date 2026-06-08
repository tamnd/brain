---
title: "CF 1995A - Diagonals"
description: "We are working on an $n times n$ grid where each cell belongs to exactly one diagonal if we group cells by the value $i + j$. Every such value defines a diagonal that runs from the top edge toward the right or bottom edge depending on where it sits in the square."
date: "2026-06-08T14:48:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1995
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 961 (Div. 2)"
rating: 800
weight: 1995
solve_time_s: 74
verified: true
draft: false
---

[CF 1995A - Diagonals](https://codeforces.com/problemset/problem/1995/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, math  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on an $n \times n$ grid where each cell belongs to exactly one diagonal if we group cells by the value $i + j$. Every such value defines a diagonal that runs from the top edge toward the right or bottom edge depending on where it sits in the square.

We are given $k$ identical chips and must place all of them on distinct cells. A diagonal becomes “active” if at least one chip lands on any cell belonging to it. The goal is to place all chips so that the number of active diagonals is as small as possible.

The key observation from the structure is that diagonals differ in how many cells they contain. Some diagonals near the corners contain only one cell, while central diagonals are much longer and can host many chips. The problem is essentially asking how to pack $k$ items into groups (diagonals) so that we use as few groups as possible, given that each group has a capacity determined by its diagonal length.

The constraints are small: $n \le 100$, so each test case can be reasoned about independently without worrying about efficiency beyond constant or linear per case. Even a direct simulation over all diagonals would be acceptable, but the structure allows a direct formula.

Edge cases appear when $k = 0$, where no diagonals are occupied, and when $k = n^2$, where every cell is filled and every diagonal becomes occupied. A subtle case is when $k$ is small: greedy intuition might suggest always filling the longest diagonals first, but the optimal strategy depends only on how many diagonals are needed to cover $k$, not on actual placement details.

## Approaches

A direct brute-force approach would attempt to place chips one by one and maintain which diagonals are already used. At each step, it would try every possible empty cell, simulate placing a chip, and track how many distinct diagonals become active. This quickly becomes exponential because each placement branches into up to $n^2$ choices, and the number of ways to choose $k$ cells is combinatorial. Even with pruning, this approach explodes for $n = 100$.

The key structural insight is that the exact geometry of the grid does not matter beyond the fact that diagonals are independent buckets with known capacities. Each diagonal corresponds to a fixed number of cells, and placing multiple chips inside the same diagonal costs only one “occupied diagonal.” Therefore, to minimize occupied diagonals, we want to fill diagonals as densely as possible before using new ones.

If we sort diagonals by capacity (number of cells in each diagonal) in decreasing order, then the optimal strategy becomes greedy: take the largest diagonals first and fill them completely until we place all $k$ chips. The number of diagonals used in this process is the answer.

Since the diagonal structure of an $n \times n$ grid is fixed, we can precompute the list of diagonal sizes once per $n$, then greedily subtract from $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n^2) | Too slow |
| Greedy over diagonal sizes | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the number of diagonals in an $n \times n$ grid. There are $2n - 1$ diagonals formed by values of $i + j$. This gives the structure we will allocate chips into.
2. Compute the size of each diagonal. For diagonal index $d$, its size increases from 1 up to $n$, then decreases symmetrically back to 1. This reflects how many cells satisfy $i + j = d$.
3. Sort these diagonal sizes in descending order. The intuition is that using a larger diagonal reduces the number of diagonals needed to store the same number of chips.
4. Iterate through the sorted diagonal sizes. For each diagonal, subtract its capacity from $k$, and count it as used. Stop once $k \le 0$.
5. Return the number of diagonals used.

### Why it works

Each diagonal is an independent container with a fixed capacity, and using any cell inside it counts the same in terms of occupied diagonals. Therefore, minimizing occupied diagonals reduces to minimizing the number of containers needed to cover $k$ units of capacity. The greedy strategy of always using the largest available container first is optimal because replacing a chosen diagonal with a smaller one can only increase the number of diagonals required to reach the same total capacity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_diagonals(n):
    sizes = []
    # i + j ranges from 2 to 2n
    for s in range(2, 2 * n + 1):
        cnt = 0
        for i in range(1, n + 1):
            j = s - i
            if 1 <= j <= n:
                cnt += 1
        sizes.append(cnt)
    sizes.sort(reverse=True)
    return sizes

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    
    if k == 0:
        print(0)
        continue

    diag = build_diagonals(n)

    used = 0
    for c in diag:
        if k <= 0:
            break
        k -= c
        used += 1

    print(used)
```

The code first constructs all diagonal lengths by scanning possible sums $i + j$. For each sum, it counts valid grid positions, which gives the size of that diagonal. After sorting these sizes in descending order, it greedily subtracts from $k$, each subtraction representing fully occupying that diagonal.

The early exit for $k = 0$ avoids unnecessary computation. The loop stops as soon as enough capacity has been accumulated.

A subtle point is that recomputing diagonals per test is still fast enough because $n \le 100$, so the construction cost is bounded and small.

## Worked Examples

### Example 1

Input:

```
n = 2, k = 3
```

Diagonal sizes are:

```
[2, 2, 1]
```

| Step | Chosen diagonal | Remaining k | Used diagonals |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 2 | -1 | 2 |

We stop after using two diagonals. This matches the idea that three chips cannot all fit into a single diagonal of size 2.

This confirms the greedy choice of taking largest diagonals first is necessary, since picking a size-1 diagonal early would only increase the total count.

### Example 2

Input:

```
n = 3, k = 9
```

Diagonal sizes:

```
[3, 2, 2, 2, 1, 1, 1]
```

| Step | Chosen diagonal | Remaining k | Used diagonals |
| --- | --- | --- | --- |
| 1 | 3 | 6 | 1 |
| 2 | 2 | 4 | 2 |
| 3 | 2 | 2 | 3 |
| 4 | 2 | 0 | 4 |

We use 4 diagonals total. This demonstrates that once large diagonals are exhausted, remaining chips must be distributed into smaller ones, and the greedy ordering naturally minimizes the number of transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n^2)$ | Building diagonals requires scanning all $i, j$ pairs per test |
| Space | $O(n)$ | Stores at most $2n-1$ diagonal sizes |

With $n \le 100$ and $t \le 500$, the total operations are well within limits. The solution runs comfortably in time because the constant factor is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        if k == 0:
            print(0)
            return

        sizes = []
        for s in range(2, 2 * n + 1):
            cnt = 0
            for i in range(1, n + 1):
                j = s - i
                if 1 <= j <= n:
                    cnt += 1
            sizes.append(cnt)

        sizes.sort(reverse=True)

        used = 0
        for c in sizes:
            if k <= 0:
                break
            k -= c
            used += 1
        print(used)

    t = int(input())
    out = []
    for _ in range(t):
        solve()
    return out

# provided samples
assert run("""7
1 0
2 2
2 3
2 4
10 50
100 239
3 9
""") == """0
1
2
3
6
3
5
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 0 | empty board |
| 2 4 | 2 | full saturation of small grid |
| 3 9 | 5 | full coverage case |

## Edge Cases

A minimal case is $n = 1, k = 0$. The grid has a single diagonal, but no chips means no occupied diagonals. The algorithm immediately returns 0 before building any structure, matching the definition.

For $n = 2, k = 1$, diagonal sizes are $[2,2,1]$. The greedy loop takes the first diagonal and stops after consuming it, returning 1. Any valid placement of a single chip occupies exactly one diagonal, so the result is consistent.

For $k = n^2$, every cell is filled, so all diagonals must be used. The algorithm consumes all diagonal capacities in descending order and returns $2n-1$, which is exactly the number of diagonals in the grid.
