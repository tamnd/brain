---
title: "CF 104603D - Assigning problems"
description: "We are given a fixed structure for a contest: each contest has $K$ difficulty levels, and level $i$ requires exactly $Ci$ problems. Problems are categorized by a minimum usable level: a problem of grade $d$ can only be assigned to levels $d, d+1, dots, K$."
date: "2026-06-30T02:53:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104603
codeforces_index: "D"
codeforces_contest_name: "2023 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 104603
solve_time_s: 35
verified: true
draft: false
---

[CF 104603D - Assigning problems](https://codeforces.com/problemset/problem/104603/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed structure for a contest: each contest has $K$ difficulty levels, and level $i$ requires exactly $C_i$ problems. Problems are categorized by a minimum usable level: a problem of grade $d$ can only be assigned to levels $d, d+1, \dots, K$. Each problem can be used at most once overall, and within a contest it can occupy only one level.

We also have a supply $P_i$ of problems of grade $i$. The task is to maximize how many complete contests can be formed, where each contest must be fully filled according to the $C_i$ requirements, using the available problems without reuse.

The core difficulty is that higher-grade problems are flexible and can serve higher levels, while low-grade problems are restricted. This creates a flow-like dependency across levels, where early decisions affect later feasibility.

The constraints reach up to $K \le 10^5$ and values up to $10^9$, which immediately rules out any per-contest simulation. Even trying to construct contests greedily one by one would be far too slow since the number of possible contests can also be large.

A subtle failure case for naive greedy assignment appears when we assign low-grade problems too eagerly.

Example:

```
K = 2
C = [1, 1]
P = [1, 1]
```

A careless strategy might assign the grade 1 problem to level 1 and the grade 2 problem to level 2, producing 1 contest, which is correct. But if we scale this:

```
K = 2
C = [1, 1]
P = [100, 1]
```

If we greedily consume grade-1 problems for level 1 and ignore their flexibility, we might still get the right answer, but in more complex distributions this leads to starvation at higher levels because low-grade problems should be conserved for the most restrictive levels that can use them.

The key difficulty is ensuring that flexible high-grade problems are always available to fill gaps created by shortages in lower grades.

## Approaches

A brute-force viewpoint is to attempt constructing contests one by one. For each contest, we try to fill level 1 through level $K$, always choosing a feasible available problem with the smallest grade that still allows assignment. This is correct because it respects constraints directly, but it is computationally infeasible.

Each contest requires scanning multiple levels, and each level may require searching for available usable problem grades. In the worst case, with up to $10^5$ levels and potentially $10^9$ contests, this approach becomes impossible.

The structural insight is to flip perspective: instead of constructing contests, we test feasibility for a given number $x$. If we want to build $x$ contests, then level $i$ requires $x \cdot C_i$ problems assigned to level $i$, and these must come from all problem grades $d \le i$.

This turns the problem into a feasibility check under cumulative constraints. We are effectively distributing supplies with lower bounds on usable positions, which naturally suggests processing levels in increasing order and maintaining a surplus of flexible higher-grade capacity.

The key observation is that higher-grade problems can always be “delayed” downward, but lower-grade ones cannot move upward. So we process from low to high, tracking how many usable problems remain after satisfying each level.

We then binary search the maximum feasible $x$, since feasibility is monotonic: if we can build $x$ contests, we can also build any $x' < x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy per contest simulation | $O(xK)$ | $O(K)$ | Too slow |
| Binary search + greedy feasibility | $O(K \log \max P)$ | $O(K)$ | Accepted |

## Algorithm Walkthrough

### Feasibility check for a fixed number of contests $x$

1. Scale requirements so each level $i$ needs $need_i = x \cdot C_i$ problems. This represents the total demand we must satisfy.
2. Traverse levels from $1$ to $K$, maintaining a running pool of available problems that can be used for the current or higher levels.
3. At level $i$, add all problems of grade $i$ into the pool, since they are now available for level $i$ and above.
4. Attempt to satisfy $need_i$ using the current pool. If the pool is insufficient, return false immediately since later levels cannot compensate for a shortage here.
5. After fulfilling level $i$, carry forward any unused pool to the next level.

This works because lower levels have stricter requirements: if we cannot satisfy level $i$, no redistribution from higher levels can fix it.

### Binary search over answer

1. Define a function `ok(x)` that checks feasibility using the process above.
2. Binary search $x$ from 0 to a large upper bound. A natural bound is $\sum P_i / \min C_i$, but in practice $10^9$ scaled bounds are safe with long long arithmetic.
3. Move the search range depending on feasibility.

### Why it works

The feasibility check enforces a prefix-consistency condition: at every level $i$, the total usable supply up to grade $i$ must be sufficient for total demand up to level $i$. Since higher-grade problems can only move downward, any valid assignment must satisfy these prefix constraints.

This makes the greedy accumulation from low to high both necessary and sufficient: it matches the only direction in which flexibility exists, so no future reassignment can repair a violated prefix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(x, K, C, P):
    # current available pool of usable problems
    pool = 0
    
    for i in range(K):
        pool += P[i]
        need = x * C[i]
        
        if pool < need:
            return False
        
        pool -= need
    
    return True

def main():
    K = int(input())
    C = list(map(int, input().split()))
    P = list(map(int, input().split()))
    
    lo, hi = 0, 10**18
    ans = 0
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, K, C, P):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    print(ans)

if __name__ == "__main__":
    main()
```

The solution is built around a single feasibility function that treats all problem grades cumulatively. The key implementation detail is the running `pool`, which represents all problems available up to the current grade boundary.

The subtraction step `pool -= need` is crucial: it enforces that each problem is used exactly once. If this step is omitted, we would incorrectly reuse capacity across levels.

Binary search is applied because feasibility is monotone in $x$. Once a certain number of contests cannot be formed, any larger number will also fail due to linear scaling of demand.

## Worked Examples

### Example 1

```
K = 2
C = [1, 1]
P = [2, 2]
```

| i | pool before | add P[i] | need | pool after |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | 1 |
| 2 | 1 | 4 | 1 | 3 |

For $x = 2$, each level needs 2 units, and the process still succeeds with leftover capacity. Trying $x = 3$ fails because demand exceeds prefix supply.

This demonstrates how prefix accumulation captures feasibility correctly.

### Example 2

```
K = 3
C = [2, 1, 1]
P = [2, 1, 3]
```

Check $x = 1$:

| i | pool before | ad
