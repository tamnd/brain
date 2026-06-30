---
title: "CF 104511B - Bessie's Money"
description: "We are trying to assign coins to six distinct cows so that each cow receives exactly one coin and the total value of all assigned coins equals a target sum $n$."
date: "2026-06-30T10:42:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104511
codeforces_index: "B"
codeforces_contest_name: "Lexington Informatics Tournament (LIT) 2023"
rating: 0
weight: 104511
solve_time_s: 77
verified: true
draft: false
---

[CF 104511B - Bessie's Money](https://codeforces.com/problemset/problem/104511/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are trying to assign coins to six distinct cows so that each cow receives exactly one coin and the total value of all assigned coins equals a target sum $n$. The available coins are limited by denomination: for each value from 1 to 5, Farmer John has a fixed number $a_x$ of coins of value $x$. The task is not to decide feasibility alone, but to count how many distinct assignments exist, where two assignments are different if at least one cow receives a coin of a different value.

The structure is essentially a constrained distribution problem: we are selecting exactly six coins from a multiset of limited resources, with ordering mattering because cows are distinct. Even if two assignments use the same multiset of coin values, swapping which cow gets which coin creates a different valid configuration.

The constraints are small: $n \le 30$, and each $a_x \le 6$. This immediately signals that brute force over all allocations is plausible because both the number of cows and coin counts are tiny. Any approach that enumerates assignments over six positions with bounded branching will terminate quickly. A solution involving exponential combinations or dynamic programming over a small state space is expected.

A few subtle edge situations matter:

If there are too few coins in total, even ignoring values, it is impossible to assign six coins. For example, if all $a_x = 0$, then no assignment exists regardless of $n$, and the answer must be zero.

If there are enough coins but their values are too small or too large, the sum constraint can still fail. For instance, if all coins are of value 1, then the only achievable total is 6, so any $n \ne 6$ yields zero ways.

Finally, multiplicity constraints matter. Even if a valid multiset of six values exists that sums to $n$, we must ensure we do not overcount beyond available coin counts. A naive combinatorial count that ignores limited supplies would be incorrect.

## Approaches

The most direct idea is to assign a coin to each cow one by one. At each cow, we choose any available coin type, decrease its availability, and continue recursively. This correctly models the problem because it respects both the sum constraint and the limited supply constraints. The result is simply the number of valid leaf assignments whose total equals $n$.

However, the branching factor is up to five choices per cow, and we have six cows. In the worst case this leads to $5^6 = 15625$ assignments, which is already small, but we must also consider pruning by coin availability. Even if we ignore pruning, this is trivial computationally.

We can make the structure cleaner by noticing that the problem is equivalent to filling six labeled slots with values in $[1,5]$, subject to global constraints on how many times each value can be used and a sum condition. This is naturally a bounded depth search over a very small state space.

A slightly more structured view is dynamic programming over cows and remaining sum, while tracking remaining coin counts. But since each $a_x \le 6$, a direct DFS with memoization or even without memoization is sufficient.

The key insight is that the state space is tiny because there are only six decisions and five choices per decision, so brute force with validity checks is already optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS over 6 cows | $O(5^6)$ | $O(1)$ or $O(6)$ recursion | Accepted |
| DP with coin counts | $O(6 \cdot n \cdot \prod a_x)$ | $O(n \cdot \prod a_x)$ | Accepted but unnecessary |

## Algorithm Walkthrough

We process cows one by one, maintaining how many coins of each value are still available and the remaining sum we need to reach.

1. Start with all coin counts $a_1 \ldots a_5$, and target sum $n$, and we are at cow index 0. The remaining sum is initially $n$. This defines the initial state of the search.
2. For the current cow, try assigning each coin value from 1 to 5, provided we still have at least one coin of that value available. This step enforces the supply constraint locally.
3. If we assign a coin of value $v$, we decrement $a_v$ and reduce the remaining sum by $v$, then recurse to the next cow. This ensures that partial assignments always reflect the true remaining resources.
4. If at any point the remaining sum becomes negative, we immediately stop exploring that branch. There is no way to recover since all remaining coins are positive.
5. When we reach the sixth cow, we check whether the remaining sum is exactly zero. If it is, we count this as one valid assignment.

The correctness relies on the fact that every assignment of coins to cows corresponds to exactly one path in this search tree. Each level chooses one cow’s coin, and each choice is uniquely determined by both coin value and availability. Therefore, we neither miss valid assignments nor double-count the same assignment under identical state evolution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    cows = 6
    values = [1, 2, 3, 4, 5]
    
    sys.setrecursionlimit(10000)
    
    from functools import lru_cache
    
    @lru_cache(None)
    def dfs(i, c1, c2, c3, c4, c5, rem):
        if rem < 0:
            return 0
        if i == cows:
            return 1 if rem == 0 else 0
        
        res = 0
        counts = [c1, c2, c3, c4, c5]
        
        for v in range(5):
            if counts[v] > 0:
                nxt = counts[:]
                nxt[v] -= 1
                res += dfs(i + 1, nxt[0], nxt[1], nxt[2], nxt[3], nxt[4], rem - (v + 1))
        
        return res
    
    print(dfs(0, a[0], a[1], a[2], a[3], a[4], n))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the recursive construction described earlier. The state includes both the cow index and remaining coin counts, because coin availability affects future choices. The remaining sum is carried as a parameter to enforce the target constraint early.

The memoization ensures that repeated states, which can occur when different sequences of choices lead to the same remaining multiset and cow index, are not recomputed. This keeps execution fast even though the raw recursion is already small.

A common pitfall is forgetting that cows are distinct, which would lead to dividing by factorials or using combinatorial counts incorrectly. Here we explicitly treat each cow position as ordered, so no normalization is needed.

## Worked Examples

### Example 1

Input:

```
8
6 2 3 4 1
```

We trace a small portion of the DFS behavior.

| Step | Cow index | Remaining sum | Coin choice | Remaining counts |
| --- | --- | --- | --- | --- |
| 0 | 0 | 8 | start | (6,2,3,4,1) |
| 1 | 0 | 8 | take 1 | (5,2,3,4,1) |
| 2 | 1 | 7 | take 1 | (4,2,3,4,1) |
| 3 | 2 | 6 | take 3 | (4,2,2,4,1) |
| 4 | 3 | 3 | take 1 | (3,2,2,4,1) |
| 5 | 4 | 2 | take 1 | (2,2,2,4,1) |
| 6 | 5 | 1 | take 1 | (1,2,2,4,1) |

This branch ends unsuccessfully because we still have remaining sum 1 after all six cows. Other branches that place higher-value coins earlier succeed, and the recursion accumulates exactly 21 valid assignments.

This trace shows how the remaining sum constraint progressively filters invalid partial assignments before reaching depth six.

### Example 2

Input:

```
6
6 0 0 0 0
```

Here only value 1 coins exist.

| Step | Cow index | Remaining sum | Coin choice | Remaining counts |
| --- | --- | --- | --- | --- |
| 0 | 0 | 6 | take 1 | (5,0,0,0,0) |
| 1 | 1 | 5 | take 1 | (4,0,0,0,0) |
| 2 | 2 | 4 | take 1 | (3,0,0,0,0) |
| 3 | 3 | 3 | take 1 | (2,0,0,0,0) |
| 4 | 4 | 2 | take 1 | (1,0,0,0,0) |
| 5 | 5 | 1 | take 1 | (0,0,0,0,0) |

This is the only successful path, confirming the answer is 1. Any deviation immediately leads to negative remaining coins or leftover sum mismatch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(5^6)$ | Six cows, each tries up to five coin types, heavily pruned by availability |
| Space | $O(5^5)$ states | Memoization over cow index, remaining counts, and sum |

The total number of states is tiny because both the depth and coin limits are bounded by small constants. Even in the worst case, the recursion explores only a few tens of thousands of states, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    # --- solution ---
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input().strip())
        a = list(map(int, input().split()))
        cows = 6

        from functools import lru_cache

        @lru_cache(None)
        def dfs(i, c1, c2, c3, c4, c5, rem):
            if rem < 0:
                return 0
            if i == cows:
                return 1 if rem == 0 else 0

            res = 0
            counts = [c1, c2, c3, c4, c5]
            for v in range(5):
                if counts[v] > 0:
                    nxt = counts[:]
                    nxt[v] -= 1
                    res += dfs(i+1, nxt[0], nxt[1], nxt[2], nxt[3], nxt[4], rem-(v+1))
            return res

        return dfs(0, a[0], a[1], a[2], a[3], a[4], n)

    return str(solve())

# provided sample
assert run("8\n6 2 3 4 1\n") == "21"

# minimum edge: impossible
assert run("10\n0 0 0 0 0\n") == "0"

# exact fill with ones only
assert run("6\n6 0 0 0 0\n") == "1"

# boundary mix
assert run("7\n6 6 6 6 6\n") > "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zero coins | 0 | no available resources |
| all ones, sum 6 | 1 | exact forced assignment |
| rich coins, small sum | positive | combinatorial explosion correctness |

## Edge Cases

One edge case is when the total number of coins is insufficient. For input `n = 6, a = (0,0,0,0,0)`, the DFS immediately finds that at cow 0 no move is possible, so the recursion returns 0. This confirms that absence of resources correctly blocks all paths.

Another case is when coins exist but cannot match the required sum. For example, `n = 7, a = (6,0,0,0,0)` forces all cows to take value 1 coins, producing sum 6 at leaf level, never reaching 7. The algorithm reaches depth six with remaining sum 1 and rejects all paths.

A final subtle case is overabundant coins where many combinations exist. Since each assignment is treated as a distinct ordered sequence over cows, the DFS naturally counts each permutation without additional combinatorial corrections, matching the intended definition of distinctness.
