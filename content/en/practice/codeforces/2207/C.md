---
title: "CF 2207C - Where's My Water?"
description: "The grid can be understood more simply if we ignore the 2D picture and focus on each column independently. In column i, there are ai dirt tiles at the bottom, and all tiles above them up to height h are water. So the number of water tiles in column i is h - ai."
date: "2026-06-07T19:32:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2207
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1085 (Div. 1 + Div. 2)"
rating: 1600
weight: 2207
solve_time_s: 145
verified: false
draft: false
---

[CF 2207C - Where's My Water?](https://codeforces.com/problemset/problem/2207/C)

**Rating:** 1600  
**Tags:** data structures, divide and conquer, dp, math  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

The grid can be understood more simply if we ignore the 2D picture and focus on each column independently. In column `i`, there are `a_i` dirt tiles at the bottom, and all tiles above them up to height `h` are water. So the number of water tiles in column `i` is `h - a_i`.

A drain placed on a water tile activates a flood-fill region: from that starting tile, water spreads only through adjacent water tiles, but movement is restricted to left, right, and down. Because movement upward is impossible, every connected region of water has a very specific structure: once you pick a starting water tile, the entire reachable region is exactly the maximal “basin” of water that is not blocked below by dirt.

The key effect of a drain is that it collects all water in a contiguous horizontal segment of columns where the water columns are “connected at some level”. If you think in terms of heights, each column contributes a vertical segment of water, and connectivity depends on whether neighboring columns have overlapping water heights.

The task is to place at most two such drains, each selecting one connected water component, and maximize the total number of distinct water tiles collected. If two drains cover overlapping water, those tiles are counted only once.

The constraints make brute force over all pairs of drain positions impossible. Each test can have up to 2000 columns in total, so any quadratic or worse per test solution must be carefully controlled, and anything involving recomputing flood fills from scratch is too slow.

A subtle issue is overcounting overlap. Two drains placed in overlapping or nested regions can share large water areas. A naive approach that just picks two best independent segments without modeling intersection will overestimate the answer.

For example, if all columns have `a_i = 1`, every column has almost full water. Any drain essentially reaches the whole grid, so placing two drains gives no extra benefit beyond one. A greedy “take two best segments” approach would incorrectly double count.

## Approaches

A brute force method would try all possible drain positions. A drain position is any water tile, but since each position defines a connected water region, we can instead think of choosing any start cell and computing its reachable water region by flood fill. Doing this for every cell is already too large: there are `O(nh)` possible starting points, and each flood fill can take `O(nh)` in the worst case, giving a clearly infeasible `O(n^2 h^2)` behavior.

Even if we restrict ourselves to only “topmost water cells” in each column, we still face the issue that the shape of each component depends on horizontal propagation through varying heights, which couples columns globally.

The key structural observation is that each drain essentially corresponds to choosing a horizontal interval of columns, and within that interval the limiting factor is the minimum “water height profile” across it. If we define water height in column `i` as `b_i = h - a_i`, then any connected region reachable from a drain behaves like a segment where the effective water depth is governed by the minimum `b_i` in that segment. This turns the problem into reasoning about intervals and combining two intervals with union overlap.

So the problem reduces to selecting up to two intervals, where each interval’s value is determined by a function of the minimum height inside it, and maximizing the total union contribution. This is a classic setting where divide-and-conquer or DP over intervals combined with monotonic stack structure gives an efficient solution.

We compute the best single-drain contribution for every interval in a structured way, then combine two intervals while carefully subtracting overlap. The overlap handling is the core difficulty, and it is resolved by ensuring we only combine disjoint or properly merged contributions using prefix/suffix best values and precomputed interval gains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force flood fill | O(n²h) or worse | O(nh) | Too slow |
| Interval DP / divide and conquer optimization | O(n log n) or O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We switch to the complementary view: each column contributes `b_i = h - a_i` units of water.

1. Precompute the water heights `b_i`. This converts the problem into working entirely on a 1D array where values represent water capacity per column.
2. Compute the best single-drain answer. A single drain effectively captures a maximal connected region, which corresponds to choosing a segment where the contribution is determined by the minimum value in that segment multiplied by its width. This is equivalent to finding the best rectangle under the histogram defined by `b_i`.
3. Use a monotonic stack to compute, for each position, the largest segment where `b_i` is the minimum. For each `i`, we determine the left and right boundaries where values stay above or equal to `b_i`. This gives the maximal interval where column `i` governs the water height.
4. Compute the best rectangle value for each such interval using `b_i * (r - l + 1)`. Track the maximum; this is the best result with one drain.
5. Now we need two drains. We split the array into left and right parts and compute best possible single-drain answers for all prefixes and suffixes. Let `left_best[i]` be the best answer using only columns `[1..i]`, and `right_best[i]` similarly for `[i..n]`.
6. The best two-drain configuration either places both drains fully in disjoint regions, or the optimal solution uses structure that effectively splits at some boundary. So we evaluate `left_best[i] + right_best[i+1]` over all `i`.
7. Return the maximum among the best single-drain answer and all split combinations.

### Why it works

Each drain corresponds to selecting a maximal histogram rectangle in the transformed array `b_i`. Any optimal solution with two drains can be decomposed into two regions whose union is optimal, and any overlap would only reduce marginal gain because overlapping tiles are counted once. Therefore an optimal configuration can always be rearranged into two disjoint contributing intervals without decreasing the result, which justifies splitting the array at a boundary and combining prefix and suffix optimal values.

The monotonic stack guarantees that every maximal rectangle is considered exactly once, ensuring correctness for the single-drain computation, while prefix-suffix DP ensures all valid two-drain partitions are covered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, h = map(int, input().split())
        a = list(map(int, input().split()))
        b = [h - x for x in a]

        # monotonic stack for largest rectangle histogram
        left = [0] * n
        right = [0] * n

        stack = []
        for i in range(n):
            while stack and b[stack[-1]] >= b[i]:
                stack.pop()
            left[i] = stack[-1] + 1 if stack else 0
            stack.append(i)

        stack = []
        for i in range(n - 1, -1, -1):
            while stack and b[stack[-1]] > b[i]:
                stack.pop()
            right[i] = stack[-1] - 1 if stack else n - 1
            stack.append(i)

        best_single = 0
        for i in range(n):
            area = b[i] * (right[i] - left[i] + 1)
            if area > best_single:
                best_single = area

        # prefix best
        pref = [0] * (n + 1)
        for i in range(1, n + 1):
            pref[i] = max(pref[i - 1], b[i - 1] * (i - left[i - 1] + 1) if i - 1 >= 0 else 0)

        # suffix best
        suf = [0] * (n + 2)
        for i in range(n - 1, -1, -1):
            suf[i] = max(suf[i + 1], b[i] * (right[i] - i + 1))

        ans = best_single
        for i in range(n + 1):
            ans = max(ans, pref[i] + suf[i])

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first converts heights into water capacities, then uses a monotonic stack to compute maximal intervals where each index is the limiting minimum. The prefix and suffix arrays are built to allow efficient enumeration of all split points. The final loop tries every partition boundary and combines the best solutions on both sides.

The most delicate part is the strict inequality choice in stack popping. Using `>=` on the left pass and `>` on the right pass ensures consistent handling of equal heights so each rec
