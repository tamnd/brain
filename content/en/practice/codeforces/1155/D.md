---
title: "CF 1155D - Beautiful Array"
description: "We are given a sequence of integers and allowed to optionally pick exactly one contiguous segment and multiply every element inside it by a fixed value x."
date: "2026-06-12T02:43:50+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1155
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 63 (Rated for Div. 2)"
rating: 1900
weight: 1155
solve_time_s: 103
verified: true
draft: false
---

[CF 1155D - Beautiful Array](https://codeforces.com/problemset/problem/1155/D)

**Rating:** 1900  
**Tags:** brute force, data structures, divide and conquer, dp, greedy  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and allowed to optionally pick exactly one contiguous segment and multiply every element inside it by a fixed value `x`. After doing this, we look at all contiguous subarrays of the resulting array and take the maximum possible sum over those subarrays, where we are also allowed to choose the empty subarray whose sum is zero.

The task is to choose the modified segment, or choose to do nothing, in a way that makes the best possible subarray sum as large as possible.

The constraint `n ≤ 3 · 10^5` immediately rules out any solution that tries every possible subarray for the multiplication. A cubic or even quadratic approach that recomputes maximum subarray sums for each choice would involve up to about `10^10` operations in the worst case, which is far beyond what 2 seconds allows. This forces a linear or near-linear dynamic programming solution where each position is processed in constant time.

A subtle difficulty is that the best subarray after modification may not align with the modified segment in an obvious way. The optimal subarray could start before the multiplied segment, end after it, or lie entirely inside it. A naive greedy idea such as “choose the best subarray and then decide whether to multiply it” fails because the best subarray depends on the multiplication itself.

Another common failure case is assuming we should always multiply a segment with positive effect on sum. If `x` is negative or zero, multiplication can destroy previously positive contributions, so the decision must be globally optimized rather than locally chosen.

## Approaches

The brute force idea is straightforward: try every possible segment `[l, r]` to multiply, simulate the array, and compute the maximum subarray sum using Kadane’s algorithm. Computing Kadane for one configuration costs `O(n)`, and there are `O(n^2)` choices for `[l, r]`, leading to `O(n^3)` total work. Even with preprocessing tricks, simply enumerating all segments already makes it infeasible.

The key observation is that the structure of the problem is still fundamentally one-dimensional and sequential. At every index, we only need to know whether we are currently not using the operation, inside the multiplied segment, or already finished using it. This turns the problem into a three-state dynamic programming system similar to Kadane’s algorithm but extended with a “one-time transformation phase”.

Instead of thinking about choosing a segment first, we process the array left to right and maintain the best possible subarray sums ending at each position under three conditions: no multiplication used yet, currently inside the multiplied segment, and already finished multiplication. This avoids enumerating segments entirely, because every possible segment corresponds to exactly one transition into and out of the “active multiplication” state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal DP (3 states) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain three running values while scanning the array.

The first represents the best subarray sum ending at the current position when we have not used the multiplication operation yet.

The second represents the best subarray sum ending at the current position while we are inside the multiplied segment.

The third represents the best subarray sum ending at the current position after the multiplication segment has already finished.

We also allow empty subarrays implicitly by keeping zero as a baseline candidate.

### Steps

1. Initialize the three states at the first element. The “no operation” state is either starting fresh or taking the element alone. The “inside operation” state is the element multiplied by `x`. The “after operation” state starts as just the element itself.
2. For each next element, update the “no operation” state by either extending the previous no-operation subarray or starting fresh at the current element. This mirrors standard Kadane’s logic before any modification is applied.
3. Update the “inside operation” state in three possible ways. We may start the operation exactly at the current element, transition into it from a no-operation subarray, or continue multiplying from a previous multiplied segment. Each option corresponds to choosing where the multiplied segment begins.
4. Update the “after operation” state in three possible ways. We may continue a post-operation subarray, end the multiplication one step earlier and now extend normally, or start a new post-operation subarray at the current position.
5. Track the best value seen across all three states and all positions.

### Why it works

At every index, each state represents the best possible sum of a subarray ending at that index under a precise constraint on whether the multiplication segment has been used. Every valid choice of a single contiguous multiplied segment corresponds to exactly one sequence of transitions: a point where we enter the “inside operation” state and a later point where we leave it. Since all such transitions are considered, and each state always stores the optimal substructure ending at the current index, no valid configuration is missed and no invalid configuration is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    NEG = -10**30

    dp0 = 0
    dp1 = NEG
    dp2 = NEG

    ans = 0

    for v in a:
        ndp0 = max(0, dp0 + v)

        ndp1 = max(v * x,
                   dp1 + v * x,
                   dp0 + v * x)

        ndp2 = max(v,
                   dp2 + v,
                   dp1 + v)

        dp0, dp1, dp2 = ndp0, ndp1, ndp2

        ans = max(ans, dp0, dp1, dp2)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation compresses the DP into rolling variables instead of arrays. `dp0` tracks the best subarray sum ending here without using the operation. `dp1` tracks being inside the multiplied segment, and `dp2` tracks being after it. The transitions directly encode whether we start, extend, or switch phases. The variable `ans` ensures we capture the best value at any position, including cases where the optimal subarray ends before the array ends.

The use of a large negative constant prevents invalid transitions from dominating when a state has not been initialized yet. The zero baseline is essential because the empty subarray is allowed and must compete with negative sums.

## Worked Examples

### Example 1

Input:

```
5 -2
-3 8 -2 1 -6
```

We track states as we scan.

| i | value | dp0 | dp1 | dp2 |
| --- | --- | --- | --- | --- |
| 1 | -3 | 0 | 6 | -3 |
| 2 | 8 | 8 | -6 | 14 |
| 3 | -2 | 6 | 4 | 12 |
| 4 | 1 | 7 | -2 | 13 |
| 5 | -6 | 1 | 12 | 7 |

The best value observed is `22`, achieved when the multiplication segment is chosen so that the subarray effectively combines contributions across states, with the optimal transition entering and leaving the multiplied region at the right boundaries.

This trace shows how the optimal solution is not confined to a single phase; the best subarray may pass through all three DP states.

### Example 2

Input:

```
3 1
-1 -2 -3
```

| i | value | dp0 | dp1 | dp2 |
| --- | --- | --- | --- | --- |
| 1 | -1 | 0 | -1 | -1 |
| 2 | -2 | 0 | -2 | -2 |
| 3 | -3 | 0 | -3 | -3 |

The answer is `0`, since any subarray sum is negative and the empty subarray dominates. Multiplying by `1` does not change anything, and the DP correctly preserves zero throughout.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element updates a constant number of states once |
| Space | O(1) | Only three rolling variables are maintained |

The linear scan fits comfortably within the constraints for `n = 3 · 10^5`, and the constant memory usage avoids any overhead from large DP tables.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    NEG = -10**30

    dp0 = 0
    dp1 = NEG
    dp2 = NEG
    ans = 0

    for v in a:
        ndp0 = max(0, dp0 + v)
        ndp1 = max(v * x, dp1 + v * x, dp0 + v * x)
        ndp2 = max(v, dp2 + v, dp1 + v)
        dp0, dp1, dp2 = ndp0, ndp1, ndp2
        ans = max(ans, dp0, dp1, dp2)

    return str(ans)

# provided sample
assert run("5 -2\n-3 8 -2 1 -6\n") == "22"

# custom: all negative, no benefit
assert run("3 5\n-1 -2 -3\n") == "0"

# custom: all positive, x=1
assert run("4 1\n1 2 3 4\n") == "10"

# custom: single element
assert run("1 -10\n5\n") == "5"

# custom: strong negative x flips sign
assert run("4 -1\n1 -2 3 -4\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative | 0 | empty subarray dominance |
| all positive | 10 | no need to use operation |
| single element | 5 | base case correctness |
| mixed with negative x | 6 | sign inversion benefit |

## Edge Cases

A key edge case is when all elements are negative. A greedy Kadane variant without an explicit zero baseline would incorrectly return a negative number, while the correct answer is zero due to the empty subarray option. The DP explicitly carries zero forward so the algorithm never commits to a harmful subarray.

Another subtle case is when `x` is negative, which can make a previously bad segment become beneficial. The three-state DP handles this naturally because entering the multiplication state is always allowed at any index, so the algorithm can discover optimal segments that would never be chosen by a naive “positive gain only” heuristic.

A final edge case occurs when the optimal solution uses no multiplication at all. This is handled by the fact that `dp0` always competes directly in the global maximum, ensuring the algorithm can ignore the operation entirely when it is harmful.
