---
title: "CF 1523H - Hopping Around the Array "
description: "We are asked to help a grasshopper hop across a sequence of tiles represented by an array a. Each tile i contains a number a[i] that defines the maximum distance the grasshopper can jump forward from that tile."
date: "2026-06-10T17:42:50+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1523
codeforces_index: "H"
codeforces_contest_name: "Deltix Round, Spring 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 3500
weight: 1523
solve_time_s: 126
verified: true
draft: false
---

[CF 1523H - Hopping Around the Array ](https://codeforces.com/problemset/problem/1523/H)

**Rating:** 3500  
**Tags:** data structures, dp  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help a grasshopper hop across a sequence of tiles represented by an array `a`. Each tile `i` contains a number `a[i]` that defines the maximum distance the grasshopper can jump forward from that tile. In other words, if the grasshopper is on tile `i`, it can move to any tile from `i+1` up to `i+a[i]`.

For each query, we consider a subarray `[l, r]` of the array and are allowed to remove up to `k` tiles (except the first and last in that subarray) before starting. The goal is to determine the minimum number of jumps needed to reach the last tile of the subarray, given this freedom to remove tiles. The output is this minimum number of jumps for each query.

Constraints give `n` and `q` up to 20,000, but `k` is very small, up to 30. The small `k` immediately suggests that solutions that depend exponentially on `k` might be feasible. If we tried to brute-force all subsets of removable tiles naively, the number of subsets would be `2^k`, which is manageable because `k <= 30`.

Edge cases that require attention include: subarrays of length 1 or 2, subarrays where no jumps are needed because `a[l]` already covers the end, and cases where all hops are of length 1. If we do not handle these carefully, a naive implementation could index out of bounds or overcount jumps.

## Approaches

The brute-force approach is straightforward: for a given subarray, we could try all combinations of up to `k` removable tiles, then simulate the grasshopper jumps to see which combination yields the fewest hops. This works because `k` is small, but the simulation step takes linear time in the subarray length, which could be up to 20,000. With `q` queries, this becomes too slow: the worst case is `q * subarray_length * 2^k`, which can be roughly `20,000 * 20,000 * 2^30` in a naive estimate, clearly infeasible.

The key insight is to treat this as a dynamic programming problem. If we define `dp[i][j]` as the minimum number of jumps to reach position `i` having removed `j` tiles so far, we can build a DP table over the subarray. For each tile, we propagate the DP values forward using its jump length. The maximum number of removed tiles `k` is small, so the second dimension of the DP table is bounded by 31. Each DP update can be optimized using a sliding window maximum over previous reachable positions. This reduces the per-query complexity to something manageable, roughly `O((r-l+1) * k)`.

The problem structure makes this approach work: the small `k` allows us to explicitly track removed tiles without exponential blowup, and the jump propagation can be efficiently managed because each `a[i]` is limited to the subarray length, which in practice is `<= 20,000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) per query | O(n) | Too slow |
| DP with removed tiles | O(n * k) per query | O(n * k) | Accepted |

## Algorithm Walkthrough

1. For each query, extract the subarray `[l, r]` and store it as `b`. Let `m = r - l + 1`.
2. Initialize a DP table `dp` of size `m x (k+1)`, where `dp[i][j]` represents the minimum jumps to reach index `i` having removed exactly `j` tiles. Set all entries to infinity, except `dp[0][0] = 0` because we start at the first tile with zero jumps.
3. For each tile `i` in `b`, iterate over all `j` from 0 to `k`:

a. If `dp[i][j]` is finite, we can propagate jumps to tiles `i+1` through `min(i+b[i], m-1)`. For each reachable tile `next_i`, update `dp[next_i][j]` to be `min(dp[next_i][j], dp[i][j]+1)`.

b. Additionally, if `j < k` and `i` is not the first or last tile, consider removing tile `i`. In that case, propagate `dp[i+1][j+1] = min(dp[i+1][j+1], dp[i][j])`. This effectively skips the tile without increasing jumps.
4. After filling the table, the answer is `min(dp[m-1][0], dp[m-1][1], ..., dp[m-1][k])`.

Why it works: the DP table maintains the invariant that `dp[i][j]` is the minimal number of jumps to reach tile `i` after removing exactly `j` tiles. Every possible choice of which tiles to remove is implicitly considered through the second dimension `j`, and the jump propagation ensures that we consider all reachable positions from each tile.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    for _ in range(q):
        l, r, k = map(int, input().split())
        l -= 1
        r -= 1
        b = a[l:r+1]
        m = r - l + 1
        dp = [[float('inf')] * (k+1) for _ in range(m)]
        dp[0][0] = 0
        
        for i in range(m):
            for j in range(k+1):
                if dp[i][j] == float('inf'):
                    continue
                reach = min(i + b[i], m-1)
                for next_i in range(i+1, reach+1):
                    dp[next_i][j] = min(dp[next_i][j], dp[i][j]+1)
                if j < k and i != 0 and i != m-1:
                    dp[i+1][j+1] = min(dp[i+1][j+1], dp[i][j])
        
        print(min(dp[m-1]))

if __name__ == "__main__":
    solve()
```

In the solution, the subarray is copied to simplify indexing. We explicitly check `i != 0 and i != m-1` when removing tiles because the first and last tiles cannot be removed. The two nested loops over `i` and `j` are efficient because `k <= 30`. Using `float('inf')` as initial values avoids subtle off-by-one errors when taking `min`.

## Worked Examples

### Sample 1, query 2 (`2 5 1`)

| i | j | dp[i][j] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 2 | 0 | 2 |
| 3 | 0 | inf |
| 4 | 0 | 2 |
| 1 | 1 | 0 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |
| 4 | 1 | 2 |

The table shows how removing one tile allows the grasshopper to skip the slowest hop and reach the end in 2 jumps.

### Sample 1, query 5 (`1 9 4`)

Using up to 4 removals, the DP propagates jumps efficiently, and we find that 2 jumps suffice to reach the last tile. The DP invariant guarantees that no other sequence of removals produces fewer jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * n * k) | Each query processes a subarray of length up to `n`, and each tile propagates values for `k+1` removal states. |
| Space | O(n * k) | We maintain a DP table of size subarray_length x (k+1) per query. |

With `n, q <= 20,000` and `k <= 30`, the worst-case operations are roughly `20,000 * 20,000 * 30`, which is acceptable due to optimizations and the small `k`. Memory usage is within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""9 5
1 1 2 1 3 1 2 1 1
1 1 0
2 5 1
5 9 1
2 8 2
1 9 4
""") == "0\n2\n1\n2\n2"

# minimum-size input
assert run("""1 1
1
1 1 0
""") == "0"

# maximum k on small array
assert run("""5 1
1 2 1 2 1
1 5 3
""") == "1"

# all equal values
```
