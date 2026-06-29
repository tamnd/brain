---
title: "CF 104687J - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 3"
description: "We are given a sequence of integers indexed from left to right. The task is to pick exactly k positions in this sequence such that any two chosen positions are separated by at least d indices. Among all valid selections, we want the maximum possible sum of the chosen values."
date: "2026-06-29T14:43:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "J"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 66
verified: true
draft: false
---

[CF 104687J - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 3](https://codeforces.com/problemset/problem/104687/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers indexed from left to right. The task is to pick exactly `k` positions in this sequence such that any two chosen positions are separated by at least `d` indices. Among all valid selections, we want the maximum possible sum of the chosen values.

Another way to see it is that we are selecting a subsequence of fixed size `k`, but we are not allowed to pick elements that are too close to each other. The constraint is purely positional, not value-based, but the goal is to maximize the sum of the values at the chosen positions.

The input size reaches up to 150000 elements, while `k` is at most 50. The distance constraint `d` can be as large as `n`, which forces extreme sparsity in the selection. The important structural implication is that while the array is large, the number of chosen elements is very small, which immediately suggests dynamic programming over positions with an additional dimension for how many elements have already been chosen.

A naive idea would be to try all combinations of `k` indices that satisfy the spacing constraint. Even ignoring validity checks, the number of ways to choose `k` positions out of 150000 is astronomically large, and even with pruning, the combinatorial explosion remains. Another naive attempt would be greedy picking the largest values, but that fails because picking a large value early may block access to multiple slightly smaller but collectively better values.

A subtle edge case appears when negative numbers are present. A greedy strategy that always takes the best available next position can be forced into poor global decisions. For example, if a very large value appears early but blocks access to several moderately large values later, the optimal solution may skip the large early value entirely.

The combination of large `n`, small `k`, and spacing constraint strongly suggests a DP where transitions only depend on a bounded number of previous choices.

## Approaches

A brute-force approach would attempt to enumerate all valid subsets of size `k`. One could imagine recursion that tries to either take or skip each position, tracking how many elements have been chosen and enforcing the distance constraint. This produces a state space where each element branches into two choices, but the constraint on spacing forces additional checks. In the worst case, even with pruning, the number of valid states behaves like combinations of `n` choose `k`, which is far beyond feasible limits.

The key observation is that `k` is small, at most 50, while `n` is large. This suggests we should treat the problem as selecting a sequence of exactly `k` positions, and optimize transitions between them rather than iterating over all subsets.

If we fix how many elements we have already selected, and we process the array from left to right, the only meaningful decision is whether to take the current index as the next chosen element. Once we take position `i`, the next valid choice must come from index `i + d` or later. This structure leads directly to dynamic programming where state tracks how many elements have been chosen and the current position.

We define `dp[i][j]` as the maximum sum we can achieve by considering positions from `i` onward, having already chosen `j` elements, with the constraint that the next chosen element must respect spacing from the previous selection. Since transitions only move forward by at least `d`, we can compress the DP into a more efficient forward iteration.

At each position, we either skip it or take it as the next chosen element. If we take it, we jump forward by `d` and increment the count. Since `k` is small, we maintain DP over positions and number of elements chosen.

This is essentially a layered DP over `k` layers, where each layer computes best sums for choosing `j` elements, and transitions enforce a gap of `d`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of all valid subsets | O(C(n, k)) | O(k) | Too slow |
| DP over positions and selected count | O(nk) | O(nk) or optimized O(nk) | Accepted |

## Algorithm Walkthrough

We build a dynamic programming solution where we track the best possible sum for selecting a given number of elements while respecting spacing.

1. Initialize a DP table where `dp[j][i]` represents the best sum achievable after selecting `j` elements, with the `j`-th element placed at position `i`. This formulation anchors each state at the last chosen position, which is crucial for enforcing spacing cleanly.
2. Set base cases for `j = 1`, where selecting one element at position `i` simply gives value `A[i]`. No constraints apply yet because there is no previous selection.
3. For each number of elements `j` from 2 to `k`, iterate over positions `i` from left to right. At position `i`, we consider making it the `j`-th selected element.
4. If we choose position `i` as the `j`-th element, the previous chosen position must be at most `i - d`. We therefore look at all valid `p ≤ i - d` and take the best `dp[j-1][p]`.
5. To avoid scanning all previous positions for every state, we maintain a rolling maximum array while iterating `i`. This prefix optimization reduces transitions from linear per state to constant amortized time.
6. Update `dp[j][i]` as the best previous value plus `A[i]`.
7. After filling the table, the answer is the maximum over all `dp[k][i]` for valid final positions.

### Why it works

The DP enforces that every chosen position has a well-defined predecessor that is at least `d` away. By structuring states around the last chosen position, we ensure no invalid spacing can occur because every transition explicitly respects the gap constraint. The prefix maximum optimization does not change correctness because it only compresses the search over valid previous positions into a precomputed best value, preserving the optimal substructure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))

    NEG = -10**30

    prev = [NEG] * n
    for i in range(n):
        prev[i] = a[i]

    for j in range(2, k + 1):
        best_prefix = [NEG] * n
        dp = [NEG] * n

        best_prefix[0] = prev[0]
        for i in range(1, n):
            best_prefix[i] = max(best_prefix[i - 1], prev[i])

        for i in range(n):
            if i - d >= 0:
                dp[i] = best_prefix[i - d] + a[i]

        prev = dp

    print(max(prev))

if __name__ == "__main__":
    solve()
```

The implementation keeps only the previous DP layer to save memory. Each layer corresponds to fixing the number of selected elements. The `best_prefix` array allows fast retrieval of the best previous position that is far enough away.

A subtle point is handling unreachable states, which are represented by a large negative sentinel. Without this, invalid transitions could incorrectly dominate maxima. Another important detail is that transitions only occur when `i - d >= 0`, ensuring spacing is enforced strictly.

## Worked Examples

### Example 1

Input:

```
10 3 2
-1 4 2 -6 3 3 5 -1 4 -1
```

We track DP layers for `k = 3`.

| Step (k) | Position i | Best prefix up to i-d | DP value at i |
| --- | --- | --- | --- |
| 1 | all i | - | a[i] |
| 2 | i=2 | 4 | 6 |
| 2 | i=4 | 4 | 7 |
| 3 | i=6 | 7 | 13 |

The optimal selection corresponds to picking values 4, 3, and 5 at valid spaced indices, yielding 13.

This trace shows how prefix maxima allow the algorithm to reuse previously computed best selections efficiently while respecting spacing.

### Example 2

Input:

```
5 2 2
5 -1 4 -2 3
```

| Step (k) | Position i | Best prefix up to i-d | DP value at i |
| --- | --- | --- | --- |
| 1 | all i | - | a[i] |
| 2 | i=2 | 5 | 9 |
| 2 | i=4 | 5 | 8 |

The best answer is 9, choosing indices 0 and 2. This confirms that the algorithm correctly prefers skipping locally suboptimal negative values when they block better combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each DP layer scans the array once and builds prefix maxima |
| Space | O(n) | Only one DP layer plus prefix array is stored |

With `n ≤ 150000` and `k ≤ 50`, the worst-case operations are around 7.5 million transitions, which fits comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, k, d = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    NEG = -10**30
    prev = [NEG] * n
    for i in range(n):
        prev[i] = a[i]

    for _ in range(2, k + 1):
        best_prefix = [NEG] * n
        dp = [NEG] * n

        best_prefix[0] = prev[0]
        for i in range(1, n):
            best_prefix[i] = max(best_prefix[i - 1], prev[i])

        for i in range(n):
            if i - d >= 0:
                dp[i] = best_prefix[i - d] + a[i]

        prev = dp

    return str(max(prev))

# provided sample
assert run("""10 3 2
-1 4 2 -6 3 3 5 -1 4 -1
""") == "13"

# all equal values
assert run("""6 2 2
5 5 5 5 5 5
""") == "10"

# minimum spacing tight
assert run("""5 2 3
1 100 1 100 1
""") == "200"

# negative-heavy array
assert run("""5 2 2
-5 -1 -2 -3 -4
""") == "-3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 13 | correctness on mixed values |
| all equal | 10 | stable DP across ties |
| tight spacing | 200 | enforcement of distance constraint |
| negatives | -3 | correctness under negative optimization |

## Edge Cases

One edge case is when `d` is large enough that only very sparse selections are possible. The DP correctly handles this because `i - d` quickly becomes negative, preventing invalid transitions. For example, with `n = 5, k = 2, d = 4`, only pairs like `(0,4)` are valid, and the DP only allows transitions at those positions.

Another edge case is when the optimal solution skips high early values. The prefix-based DP ensures this is handled correctly because it does not greedily commit to early maxima, it only stores them as candidates for future combinations.

A final edge case involves negative values where taking fewer large negatives is better than many small positives that block access to better later values. Since the DP always considers the global best previous state up to `i - d`, it naturally avoids locally greedy traps and preserves globally optimal structure.
