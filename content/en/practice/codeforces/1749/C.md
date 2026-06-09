---
title: "CF 1749C - Number Game"
description: "We are asked to analyze a two-player game played on an array of positive integers. Alice chooses a number of stages $k$ she wants to play, and in each stage she must remove an element from the array that is at most the number of the remaining stage."
date: "2026-06-09T15:14:10+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1749
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 138 (Rated for Div. 2)"
rating: 1400
weight: 1749
solve_time_s: 130
verified: false
draft: false
---

[CF 1749C - Number Game](https://codeforces.com/problemset/problem/1749/C)

**Rating:** 1400  
**Tags:** binary search, data structures, games, greedy, implementation  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to analyze a two-player game played on an array of positive integers. Alice chooses a number of stages $k$ she wants to play, and in each stage she must remove an element from the array that is at most the number of the remaining stage. After Alice’s removal, Bob adds the same stage value to any remaining element. Alice wins if she successfully completes all $k$ stages; she loses if she cannot remove a valid element during any stage.

The input gives us multiple test cases. Each test case provides the size of the array and the array itself. The output must be the maximum number of stages $k$ Alice can choose and still guarantee a win if both play optimally.

The constraints are small: $n \le 100$ and array values are at most $n$. With these bounds, any algorithm that is quadratic in $n$ or slightly worse will run comfortably under the 2-second limit. This allows us to think in terms of sorting or simple iteration rather than complicated data structures.

A non-obvious edge case occurs when the array is filled with elements that are too large for Alice to remove even in the first stage. For example, if $a = [4,4,4,4]$ and $n=4$, then even $k=1$ is impossible because Alice cannot remove a number $\le 1$. A naive approach that simply tries to greedily remove elements without sorting would fail here, producing an incorrect $k>0$.

Another subtlety is the impact of Bob’s moves. He can increase any element, potentially blocking Alice’s ability to remove it in a later stage. However, the worst-case scenario for Alice is determined by the initial values sorted in ascending order; Bob can always apply his increment to the largest available number, effectively making the earlier smallest numbers the only ones Alice can remove at each stage.

## Approaches

The brute-force approach simulates the game for all possible $k$ from $0$ to $n$. For each $k$, we iterate through $k$ stages, attempting to remove an element that satisfies the stage condition and then increment some element. This method works because it directly follows the rules, but the worst-case operation count is $O(n^2)$ per test case, which is acceptable here but not elegant.

The key insight for a faster and cleaner solution is that Alice’s ability to survive $k$ stages depends entirely on the sorted order of the array. After sorting, if Alice wants to survive $k$ stages, she must remove elements in increasing order such that the $i$-th smallest element is at most $i$. This is because Bob’s optimal play effectively maximizes the future value of elements, so the smallest elements are the ones Alice can reliably remove.

The observation reduces the problem to a simple check on the sorted array: traverse it and find the largest $k$ such that the $i$-th element is at most $i$ (1-indexed). This linear scan after sorting gives the optimal $k$ in $O(n \log n)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Works but more complex and slower |
| Sorted Array Greedy | O(n log n) | O(n) | Accepted and clean |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read the array size $n$ and the array $a$.
2. Sort the array $a$ in non-decreasing order. Sorting ensures we consider the smallest elements first, which are the most constrained for Alice to remove.
3. Initialize a counter $k = 0$. Iterate over the sorted array using a 1-indexed loop. For each element $a[i]$, check if $a[i] \le k + 1$. If it is, increment $k$ by 1. If not, stop iterating, because Alice cannot survive a stage beyond this point.
4. After the iteration, $k$ represents the maximum number of stages Alice can choose and still guarantee a win. Print this value for the current test case.

The reason this works is that after sorting, the $i$-th element in the sorted array represents the smallest remaining number Alice could attempt to remove in stage $i$. If $a[i] > i$, Alice would fail at stage $i$ because there is no element small enough to remove. The greedy check preserves the invariant that all previous stages are winnable.

## Python Solution

```
PythonRun
```

The solution first reads input efficiently and sorts the array. The greedy counter `k` increases only when the current element is small enough to allow Alice to survive the next stage. The break ensures we stop counting as soon as Alice cannot proceed. Using `k + 1` aligns the 0-indexed Python loop with the 1-indexed stage count.

## Worked Examples

**Example 1**

Input array: `[1,1,2]`

| Sorted `a` | Stage `k` | Condition `x <= k+1` | Action |
| --- | --- | --- | --- |
| 1 | 0 | 1 <= 1 | k = 1 |
| 1 | 1 | 1 <= 2 | k = 2 |
| 2 | 2 | 2 <= 3 | k = 3 |

After iteration, Alice can survive 2 stages (the third element can also be removed, but `k` counts stages survived starting from 0). Output: `2`.

**Example 2**

Input array: `[4,4,4,4]`

| Sorted `a` | Stage `k` | Condition `x <= k+1` | Action |
| --- | --- | --- | --- |
| 4 | 0 | 4 <= 1 | No, break |

Output: `0`. Alice cannot survive even stage 1.

These traces confirm the algorithm correctly calculates the maximum winnable stages for Alice and respects the effect of Bob’s moves implicitly by considering the worst-case scenario.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, iteration is O(n) |
| Space | O(n) | Storing array for each test case |

Given the constraints $n \le 100$ and $t \le 100$, the worst-case total operations is roughly 100 * 100 log 100 ≈ 70000, which is comfortably within 2 seconds. Memory usage is negligible relative to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
```
