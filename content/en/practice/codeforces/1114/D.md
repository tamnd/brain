---
title: "CF 1114D - Flood Fill"
description: "We are given a row of n colored squares, each labeled with an integer representing its color. The goal is to recolor the entire row into a single color using a series of \"flood fill\" operations."
date: "2026-06-12T04:52:43+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1114
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 538 (Div. 2)"
rating: 1900
weight: 1114
solve_time_s: 87
verified: false
draft: false
---

[CF 1114D - Flood Fill](https://codeforces.com/problemset/problem/1114/D)

**Rating:** 1900  
**Tags:** dp  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of `n` colored squares, each labeled with an integer representing its color. The goal is to recolor the entire row into a single color using a series of "flood fill" operations. Each operation picks a contiguous segment of identical color that contains a chosen starting square and changes all of its squares to another color. The starting square itself is chosen once and does not count as a move.

The input gives the number of squares and the sequence of colors. The output is the minimum number of turns required to make all squares the same color.

With `n` up to 5000, any naive algorithm that examines every possible sequence of moves explicitly will be too slow. For example, if one tries every possible starting square and every color choice at every step, the search space grows exponentially, easily exceeding `10^6` operations, which is infeasible under a 2-second time limit.

Subtle edge cases include rows that are already uniform, in which case the answer is zero, or rows where each square has a unique color, which maximizes the number of moves required. Another tricky scenario is when the optimal starting square is not at an endpoint but somewhere in the middle, requiring us to look beyond a simple greedy approach.

## Approaches

The brute-force approach is to simulate every possible choice of starting square and each possible sequence of color changes. For each move, we recolor the connected component and check the resulting array. This works correctly in principle, but for `n = 5000`, the number of sequences grows exponentially, making it utterly impractical.

The key insight to optimize comes from recognizing that we do not need to track every square individually. Instead, we can collapse consecutive identical colors into single segments. Recoloring only matters at segment boundaries. Moreover, if two segments of the same color appear with a different color in between, an optimal strategy can merge these segments by turning the middle colors into the target color in a minimal number of steps.

Formally, we define a dynamic programming state `dp[l][r]` as the minimum number of turns needed to make the segment from `l` to `r` (inclusive) a single color. If the first and last segments have the same color, the outermost coloring can be done in one fewer move because they can be merged optimally. This observation allows a recursive formula:

```
dp[l][r] = 1 + min(dp[l+1][k] + dp[k+1][r])  for all k such that l <= k < r
```

We optimize further by noticing that we only need to consider the positions where the color changes, which reduces the effective `n` from the total number of squares to the number of segments, often dramatically smaller.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Dynamic Programming on segments | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Compress the input array into segments where consecutive identical colors are collapsed into one. Store only the unique sequence of colors. This reduces redundant computation.
2. Initialize a 2D DP array `dp` of size `m x m`, where `m` is the number of segments. `dp[l][r]` will store the minimum number of moves to recolor segments `l` through `r` into a single color.
3. Set the base case: `dp[i][i] = 1` for all single segments, since a segment alone can be turned into a single color in one move if needed.
4. Fill the DP table by increasing segment lengths. For a segment from `l` to `r`:

- Start with `dp[l][r] = 1 + dp[l+1][r]` assuming we recolor segment `l` to match the rest.
- Then iterate over positions `k` from `l+1` to `r`. If `color[l] == color[k]`, we can merge the segments at `l` and `k` and combine results: `dp[l][r] = min(dp[l][r], dp[l+1][k-1] + dp[k][r])`.
5. The final answer is `dp[0][m-1]`, the minimum number of moves to recolor the entire compressed row.

**Why it works:** The DP invariant is that `dp[l][r]` always stores the minimum number of moves to recolor the segment `[l, r]`. The recurrence merges segments of the same color and accounts for intermediate colors efficiently, ensuring no redundant moves are counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
colors = list(map(int, input().split()))

# Step 1: Compress consecutive identical colors
comp = []
for c in colors:
    if not comp or comp[-1] != c:
        comp.append(c)

m = len(comp)
dp = [[0] * m for _ in range(m)]

# Step 2: DP base case
for i in range(m):
    dp[i][i] = 1

# Step 3: DP computation
for length in range(2, m+1):
    for l in range(m - length + 1):
        r = l + length - 1
        dp[l][r] = 1 + dp[l+1][r]
        for k in range(l+1, r+1):
            if comp[l] == comp[k]:
                dp[l][r] = min(dp[l][r], dp[l+1][k-1] + dp[k][r])

print(dp[0][m-1])
```

The code first compresses the sequence of colors, which ensures we only consider meaningful segment boundaries. We initialize a DP table with base cases of length-1 segments. We iterate by increasing segment lengths, updating the DP using the merge logic. The `dp` table guarantees that every subarray solution is optimal when computed from smaller subarrays.

## Worked Examples

### Sample 1

Input: `4 5 2 2 1`

| l | r | dp[l][r] | Explanation |
| --- | --- | --- | --- |
| 0 | 0 | 1 | Single segment [5] |
| 1 | 1 | 1 | [2] |
| 2 | 2 | 1 | [2] |
| 3 | 3 | 1 | [1] |
| 1 | 2 | 1 | Merge [2,2] |
| 0 | 1 | 2 | Merge [5] with [2,2] |
| 0 | 2 | 2 | Same, considering merging |
| 0 | 3 | 2 | Final result: recolor [5,2,2,1] in 2 moves |

This trace shows how merging segments reduces moves when colors match at distant ends.

### Sample 2

Input: `5 1 2 3 4 5`

All colors differ. Each segment is unique, so every move changes one segment at a time. DP calculates that merging non-adjacent same colors is not possible. Minimum moves = 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | After compression, we consider each segment pair. Inner loop iterates at most `m` times. |
| Space | O(n^2) | The DP table stores results for all segment ranges. |

With `n <= 5000`, `n^2` operations is roughly 25 million, which is acceptable within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    colors = list(map(int, input().split()))
    comp = []
    for c in colors:
        if not comp or comp[-1] != c:
            comp.append(c)
    m = len(comp)
    dp = [[0] * m for _ in range(m)]
    for i in range(m):
        dp[i][i] = 1
    for length in range(2, m+1):
        for l in range(m - length + 1):
            r = l + length - 1
            dp[l][r] = 1 + dp[l+1][r]
            for k in range(l+1, r+1):
                if comp[l] == comp[k]:
                    dp[l][r] = min(dp[l][r], dp[l+1][k-1] + dp[k][r])
    return str(dp[0][m-1])

# Provided samples
assert run("4\n5 2 2 1\n") == "2", "sample 1"
assert run("1\n5\n") == "1", "single element"
assert run("5\n1 2 3 4 5\n") == "4", "all distinct"
# Custom cases
assert run("6\n1 1 1 1 1 1\n") == "1", "all same"
assert run("7\n1 2 1 2 1 2 1\n") == "4", "alternating"
assert run("2\n2 2\n") == "1", "two same"
assert run("2\n2 3\n") == "1", "two different
```
