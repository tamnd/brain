---
title: "CF 1244E - Minimizing Difference"
description: "We are given a list of integers and a limited budget of unit operations. Each operation lets us pick a single element and move it by exactly one step, either up or down."
date: "2026-06-15T21:29:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "sortings", "ternary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1244
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 592 (Div. 2)"
rating: 2000
weight: 1244
solve_time_s: 451
verified: false
draft: false
---

[CF 1244E - Minimizing Difference](https://codeforces.com/problemset/problem/1244/E)

**Rating:** 2000  
**Tags:** binary search, constructive algorithms, greedy, sortings, ternary search, two pointers  
**Solve time:** 7m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers and a limited budget of unit operations. Each operation lets us pick a single element and move it by exactly one step, either up or down. The goal is not to make all numbers equal, but to reduce the gap between the largest and smallest value in the final array as much as possible.

The key constraint is that every adjustment costs one unit, and we have a total budget of at most $k$ operations. We are allowed to distribute these operations arbitrarily across elements.

The output is the smallest achievable value of $\max(a) - \min(a)$ after spending no more than $k$ total increments or decrements.

The constraints are large: up to $10^5$ elements and $k$ up to $10^{14}$. This immediately rules out any approach that simulates operations step by step. Even $O(nk)$ style greedy simulation is impossible because $k$ is far too large. Sorting is allowed, and anything $O(n \log n)$ is safe.

A naive but tempting idea is to repeatedly adjust the global minimum upward or the global maximum downward. This fails because changing one extreme can expose a new extreme immediately, and greedily moving one side without global accounting can waste operations.

For example, if the array is $[1, 1, 100]$ with a small $k$, always pushing the maximum down first might consume too much budget while a better strategy would partially raise the minimums first.

Another subtle issue is assuming that you should always make values equal as much as possible. That is not always optimal because sometimes it is cheaper to “compress” both ends instead of fully equalizing everything.

## Approaches

A brute-force view would try to simulate all possible final configurations where each element is shifted by some integer amount whose total absolute sum is at most $k$. This is equivalent to searching over a huge state space of integer vectors, which grows exponentially with $n$ and is completely infeasible.

The structural insight is that only the extremes matter. Since we care only about the difference between maximum and minimum, we can ignore internal ordering once the array is sorted. The optimal strategy always consists of repeatedly adjusting either the current minimum upward or the current maximum downward, because any operation applied inside the array does not affect the current range as efficiently as targeting an endpoint.

After sorting, we can think in terms of how many elements we fully “lift” from the left and how many we fully “push” from the right. Instead of simulating operations, we track cumulative costs to raise a prefix or lower a suffix to some boundary level.

This leads to a two-pointer greedy structure. We maintain pointers at both ends and also track how many times the current minimum value appears on the left and how many times the maximum value appears on the right. At each step, we choose the cheaper side to adjust, based on how many elements share that extreme value.

The algorithm effectively compresses layers of equal values from both ends until we either run out of budget or the interval collapses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force state search | Exponential | Exponential | Too slow |
| Sorting + two pointers greedy compression | $O(n \log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This allows us to reason about removing or adjusting extremes as contiguous blocks instead of scattered elements.
2. Initialize two pointers, one at the start and one at the end of the array. These represent the current minimum and maximum candidates.
3. Maintain two counters: how many times the current minimum value appears at the left side and how many times the current maximum value appears at the right side. These multiplicities determine the cost of moving the boundary inward.
4. While the left pointer is strictly less than the right pointer and we still have remaining budget $k$, compare the cost of fully increasing the current minimum block versus fully decreasing the current maximum block.

The cost of raising the minimum block by one is equal to the size of the block of equal minimum values. Similarly, the cost of lowering the maximum block is the size of the block of equal maximum values.
5. Choose the side with the smaller cost. If we can afford it within $k$, we subtract that cost and move the corresponding pointer inward, merging with the next distinct value. If we cannot fully afford it, we distribute remaining budget within that block and stop.
6. Once we stop, compute the final difference as the distance between the current right and left values, possibly reduced further by partially spending remaining budget inside the last active block.

### Why it works

The invariant is that at every step, the remaining problem is equivalent to shrinking a contiguous segment of the sorted array, and all optimal solutions must operate only on the current extreme value blocks. Any operation on a non-extreme element can be simulated more efficiently by applying it to the boundary instead without worsening cost. This ensures that greedily consuming the cheaper boundary block never blocks a globally optimal solution, because any optimal sequence can be rearranged so that extreme adjustments happen first without increasing total cost.

## Python Solution

```
PythonRun
```

The sorting step ensures all decisions are made on contiguous value blocks. The two pointers shrink the active range. The block counting logic identifies how many identical elements are currently at each boundary, which determines how expensive it is to move that boundary inward.

A subtle implementation risk is recomputing block sizes repeatedly in a naive way. While this solution does so, it still remains linear overall because each element is absorbed into a pointer once.

The final answer is computed directly from the remaining boundary values once no further affordable full compression is possible.

## Worked Examples

### Example 1

Input:

```

```

Sorted array: $[1, 3, 5, 7]$

| Step | l | r | k | Left value | Right value | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 5 | 1 | 7 | Compare ends |
| 2 | 0 | 3 | 5 | 1 | 7 | Reduce left side first |
| 3 | 1 | 3 | remaining | 3 | 7 | Continue |
| 4 | 1 | 2 | remaining | 3 | 5 | Stop when budget insufficient |

Final range is $5 - 3 = 2$.

This trace shows that compressing both ends gradually leads to a balanced middle segment instead of focusing on one side only.

### Example 2

Input:

```

```

Sorted array: $[1, 1, 1, 10, 10]$

| Step | l | r | k | Left | Right | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 10 | 1 | 10 | Compare blocks |
| 2 | 0 | 4 | 10 | 1 | 10 | Raise left block or lower right |
| 3 | 1 | 3 | remaining | 1 | 10 | Continue compression |
| 4 | 1 | 3 | remaining | 1 | 10 | Possibly equalize |

Eventually the array can be fully equalized or nearly equalized depending on budget.

This demonstrates that large uniform blocks are absorbed in bulk, not element by element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; pointer movement is linear |
| Space | $O(1)$ extra | Only indices and counters are used beyond input storage |

The constraints allow up to $10^5$ elements, so an $O(n \log n)$ solution fits comfortably within time limits, and linear memory usage is trivial for 256 MB.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | no-op case |
| k = 0 | original range | no operations allowed |
| large k | 0 | full compression possible |

## Edge Cases

A key edge case is when all elements are identical. The sorted array has equal endpoints, so the algorithm immediately terminates with zero difference because no compression is needed.

Another edge case occurs when $k = 0$. The pointers never move, and the answer is simply the initial max minus min, which the algorithm preserves correctly since no operation branch is entered.

A third case is when the array has two extreme clusters like $[1, 1, 1, 100, 100]$. The algorithm processes the entire left or right block in bulk, ensuring that cost is computed in aggregated form rather than per element, which is essential to avoid underestimating or overestimating the number of required operations.
