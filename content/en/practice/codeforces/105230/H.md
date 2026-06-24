---
title: "CF 105230H - Mountains"
description: "We are given a one-dimensional path encoded as a string of + and -. We start at an implicit height of zero before processing the string. Each character moves the current height by exactly one unit: + increases height by one, - decreases it by one."
date: "2026-06-24T16:00:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105230
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC Bolivia Pre-National Contest"
rating: 0
weight: 105230
solve_time_s: 70
verified: true
draft: false
---

[CF 105230H - Mountains](https://codeforces.com/problemset/problem/105230/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional path encoded as a string of `+` and `-`. We start at an implicit height of zero before processing the string. Each character moves the current height by exactly one unit: `+` increases height by one, `-` decreases it by one. After processing each character, we obtain a sequence of heights along the path, one height per position in the string.

The task is to find the position in the string where the height reaches its maximum value for the entire walk. Positions are 1-indexed and refer to the character in the string that leads to that height.

So the problem is essentially: simulate a prefix sum over a ±1 array and report the earliest position where the maximum prefix sum occurs, with the guarantee that this maximum is unique.

The constraint `|s| ≤ 10^5` implies that any solution must be linear or near-linear. An O(n²) simulation, such as recomputing prefix sums or scanning from each position, would be far too slow because it would involve up to 10¹⁰ operations in the worst case.

A linear scan in O(n) is sufficient, since 10⁵ operations are trivial under a 1-second limit in Python.

A subtle edge case arises when the maximum height is achieved immediately. For example, input `+----` reaches height 1 at position 1 and never exceeds it again, so the answer is 1. Another case is when the maximum is achieved at the end, such as `++++`, where the answer is 4. A naive approach that only tracks the final height would fail here, because the peak is not necessarily at the end of the walk.

## Approaches

The straightforward idea is to simulate the walk and compute the height after each step. We maintain a running sum, starting at zero, and update it by +1 or -1 depending on the character. Along the way, we track the maximum value seen so far and the position where it first occurs.

This works because the height at each position depends only on the prefix of the string up to that position. However, a careless implementation might recompute the height from scratch for each index, which would cost O(n²) time since each position would scan all previous characters again.

The key observation is that prefix sums are incremental. Each new height can be derived from the previous one in constant time. This reduces the computation to a single pass over the string, making it optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute prefix each time) | O(n²) | O(1) | Too slow |
| Optimal (single prefix scan) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the string once while maintaining three values: current height, best height found so far, and the index where the best height occurs.

1. Initialize current height as 0, best height as 0, and best position as 0. We include position 0 conceptually to handle cases where the maximum is never improved beyond initial assumptions.
2. Iterate through the string from left to right using a 1-based index i.
3. Update current height: increase by 1 if the character is `+`, otherwise decrease by 1.
4. Compare current height with best height. If current height is strictly greater, update best height and record position i.
5. Continue until the end of the string.
6. Output the stored best position.

Each step relies on the fact that heights are built cumulatively, so no future or past segment needs to be reconsidered once processed.

### Why it works

The sequence of heights is fully determined by prefix sums, and each prefix sum depends only on the previous one. At every step i, the algorithm stores the maximum value among all prefix sums up to i. Because every prefix sum is evaluated exactly once and compared immediately, no higher value can be missed. The uniqueness guarantee ensures we never need to handle ties or multiple candidates, so a simple strict comparison is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    
    cur = 0
    best = 0
    best_pos = 0
    
    for i, ch in enumerate(s, 1):
        if ch == '+':
            cur += 1
        else:
            cur -= 1
        
        if cur > best:
            best = cur
            best_pos = i
    
    print(best_pos)

if __name__ == "__main__":
    solve()
```

The code directly implements a prefix sum scan. The variable `cur` tracks the current height, updated in constant time per character. The variable `best` stores the highest height seen so far, and `best_pos` remembers where it occurred.

The loop uses 1-based indexing via `enumerate(s, 1)` to match the problem’s definition of positions. The strict comparison `cur > best` ensures we only record the first occurrence of the maximum height, which aligns with the uniqueness guarantee.

## Worked Examples

### Example 1: `+-+-+++--+--`

We track the evolution of height step by step.

| i | char | cur | best | best_pos |
| --- | --- | --- | --- | --- |
| 1 | + | 1 | 1 | 1 |
| 2 | - | 0 | 1 | 1 |
| 3 | + | 1 | 1 | 1 |
| 4 | - | 0 | 1 | 1 |
| 5 | + | 1 | 1 | 1 |
| 6 | + | 2 | 2 | 6 |
| 7 | + | 3 | 3 | 7 |
| 8 | - | 2 | 3 | 7 |
| 9 | - | 1 | 3 | 7 |
| 10 | + | 2 | 3 | 7 |
| 11 | - | 1 | 3 | 7 |
| 12 | - | 0 | 3 | 7 |

The highest value reached is 3 at position 7. The algorithm correctly captures the first time this maximum is achieved.

### Example 2: `+++-++-+--+++-+++--+`

| i | char | cur | best | best_pos |
| --- | --- | --- | --- | --- |
| 1 | + | 1 | 1 | 1 |
| 2 | + | 2 | 2 | 2 |
| 3 | + | 3 | 3 | 3 |
| 4 | - | 2 | 3 | 3 |
| 5 | + | 3 | 3 | 3 |
| 6 | + | 4 | 4 | 6 |
| 7 | - | 3 | 4 | 6 |
| 8 | + | 4 | 4 | 6 |
| 9 | - | 3 | 4 | 6 |
| 10 | - | 2 | 4 | 6 |
| 11 | + | 3 | 4 | 6 |
| 12 | + | 4 | 4 | 6 |
| 13 | + | 5 | 5 | 13 |
| 14 | - | 4 | 5 | 13 |
| 15 | + | 5 | 5 | 13 |
| 16 | + | 6 | 6 | 16 |
| 17 | + | 7 | 7 | 17 |
| 18 | - | 6 | 7 | 17 |
| 19 | - | 5 | 7 | 17 |
| 20 | + | 6 | 7 | 17 |

The maximum height is 7 at position 17, which matches the required output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with constant-time updates |
| Space | O(1) | Only a few integer variables are maintained |

The linear scan is well within limits for n up to 10⁵. Memory usage is constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    s = input().strip()
    cur = 0
    best = 0
    best_pos = 0
    
    for i, ch in enumerate(s, 1):
        if ch == '+':
            cur += 1
        else:
            cur -= 1
        
        if cur > best:
            best = cur
            best_pos = i
    
    return str(best_pos)

# provided samples
assert run("+-+-+++--+--\n") == "7", "sample 1"
assert run("+++-++-+--+++-+++--+\n") == "17", "sample 2"

# minimum size
assert run("+\n") == "1", "single plus"

# all decreasing
assert run("-----\n") == "0", "never above zero, max at start"

# peak at end
assert run("++++\n") == "4", "peak at end"

# alternating
assert run("+-+-+-+\n") == "1", "early peak"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+` | 1 | minimal input, immediate peak |
| `-----` | 0 | maximum remains at initial position |
| `++++` | 4 | peak at last position |
| `+-+-+-+` | 1 | repeated oscillation, early maximum |

## Edge Cases

One important edge case is when the maximum height is achieved immediately at the first step. For input `+----`, the prefix heights are `[1, 0, -1, -2, -3]`, so the answer must be 1. The algorithm handles this because `best` starts at 0 and is updated at i = 1 when `cur = 1`.

Another edge case is when the height never exceeds zero after starting. For input `-----`, the maximum prefix height is 0 at position 0 (before any move). The implementation naturally returns 0 because `best_pos` is initialized to 0 and never updated.

A third case is when the maximum occurs multiple times but only the first occurrence should be returned. For `++-++`, heights are `[1, 2, 1, 2, 3]`, and the maximum 3 appears only once at position 5. If there were multiple equal maxima, the strict `>` comparison ensures the first occurrence is preserved.
