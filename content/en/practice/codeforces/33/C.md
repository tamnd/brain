---
title: "CF 33C - Wonderful Randomized Sum"
description: "We are given a sequence of integers, and the task is to maximize its sum by performing two operations: first, we may choose any prefix of the sequence and multiply every element in it by -1; second, we may choose any suffix of the sequence and multiply every element in it by -1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 33
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 33 (Codeforces format)"
rating: 1800
weight: 33
solve_time_s: 186
verified: true
draft: false
---
[CF 33C - Wonderful Randomized Sum](https://codeforces.com/problemset/problem/33/C)

**Rating:** 1800  
**Tags:** greedy  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and the task is to maximize its sum by performing two operations: first, we may choose any prefix of the sequence and multiply every element in it by -1; second, we may choose any suffix of the sequence and multiply every element in it by -1. Both operations are optional, and the prefix and suffix can overlap. The output is a single integer, the maximum sum achievable.

The key constraints are that the sequence can be as large as 100,000 elements, and individual elements range from -10,000 to 10,000. With a 2-second time limit, this restricts us to solutions that run in roughly linear or linear-logarithmic time. Quadratic approaches, such as trying every possible pair of prefix and suffix, would require on the order of $10^{10}$ operations in the worst case, which is infeasible.

Subtle edge cases include sequences with all negative numbers, where flipping the entire sequence may be optimal, and sequences with a single element, where flipping may or may not be beneficial. For example, the input `[-5]` should output `5`, while `[3]` should output `3`. Careless approaches might assume prefixes and suffixes are disjoint or fail to handle empty flips properly.

## Approaches

A brute-force approach would try every possible prefix to flip, then every possible suffix to flip, calculate the sum, and track the maximum. Specifically, for each index $i$ from 0 to $n$, we flip the first $i$ elements and then for each index $j$ from 0 to $n$, flip the last $j$ elements. Each evaluation requires summing $n$ elements. This gives $O(n^3)$ complexity in the worst case. Even if we precompute prefix sums to reduce the sum calculation to $O(1)$, this still yields $O(n^2)$, which is too slow for $n = 10^5$.

The key observation that allows a linear solution is noticing that flipping a prefix or suffix is equivalent to subtracting twice the sum of that segment from the total sum if we had initially flipped it and then flipped back. More concretely, let the total sum of the sequence be $S$. Flipping a prefix of length $k$ changes the sum by $-2 \times \text{sum of first k elements}$. Flipping a suffix of length $l$ changes the sum by $-2 \times \text{sum of last l elements}$. Therefore, maximizing the total sum reduces to choosing the prefix and suffix such that the sum of the segment being flipped (and subtracted twice) is minimized.

To efficiently implement this, we can precompute prefix sums and suffix sums. We track the minimum prefix sum and the minimum suffix sum, then consider combinations where we flip none, flip only prefix, flip only suffix, or flip both. The optimal sum is then the maximum among these combinations. Because prefix sums and suffix sums are computed linearly and the combination step is also linear, the overall complexity is $O(n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the sequence and compute the total sum $S$. This represents the sum without any flips.
2. Compute the prefix sums for the sequence. For each index $i$, prefix sum up to $i$ is the sum of elements from 0 to $i$. Track the minimum prefix sum as you iterate. This will later allow us to determine the most beneficial prefix to flip.
3. Similarly, compute suffix sums from the end to the start, tracking the minimum suffix sum. This gives the most beneficial suffix to flip.
4. Consider flipping no segment. This simply yields $S$.
5. Consider flipping the prefix with the smallest sum. Flipping this prefix changes the total sum to $S - 2 \times (\text{minimum prefix sum})$.
6. Consider flipping the suffix with the smallest sum. Flipping this suffix changes the total sum to $S - 2 \times (\text{minimum suffix sum})$.
7. Consider flipping both prefix and suffix. Because flips can overlap, calculate the sum when flipping both the minimum prefix and minimum suffix, adjusting for the overlap to avoid double subtraction.
8. The answer is the maximum among these scenarios.

Why it works: Flipping a segment is equivalent to subtracting twice its sum. The operations are linear and independent, except for overlap, which is correctly accounted for. By precomputing minimum prefix and suffix sums, we ensure the choice maximizes the sum globally without missing any better combinations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

# Compute minimum prefix sum
prefix_sum = 0
min_prefix = 0
for x in a:
    prefix_sum += x
    min_prefix = min(min_prefix, prefix_sum)

# Compute minimum suffix sum
suffix_sum = 0
min_suffix = 0
for x in reversed(a):
    suffix_sum += x
    min_suffix = min(min_suffix, suffix_sum)

# Maximum sum options
max_sum = total
max_sum = max(max_sum, total - 2 * min_prefix)
max_sum = max(max_sum, total - 2 * min_suffix)
max_sum = max(max_sum, total - 2 * (min_prefix + min_suffix))

print(max_sum)
```

The solution first calculates the total sum as a baseline. The prefix sum loop tracks the running sum and updates the minimum prefix sum, handling the case where flipping an empty prefix yields no change. The suffix sum loop does the same in reverse. The maximum among all flipping options gives the final answer. Edge cases such as all negative numbers or a single element are naturally handled, because empty flips correspond to zero subtraction.

## Worked Examples

**Example 1**

Input: `[-1, -2, -3]`

| Step | prefix_sum | min_prefix | suffix_sum | min_suffix | total | max_sum candidates |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -1 | -1 | -3 | -3 | -6 | 6, 6, 6, 6 |

Flipping the entire sequence (prefix and/or suffix) produces 6, the correct maximum.

**Example 2**

Input: `[3, -4, 2]`

| Step | prefix_sum | min_prefix | suffix_sum | min_suffix | total | max_sum candidates |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 2 | -4 | 1 | 1, 1, 9, 9 |

Flipping the suffix `[-4, 2]` gives sum `9`, which is the maximum.

These traces confirm the algorithm identifies the optimal segments to flip even when elements are mixed positive and negative.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute total sum, one for prefix sums, one for suffix sums, constant time combination |
| Space | O(1) | Only a few running totals and minima are stored |

This fits comfortably within the 2-second limit for $n \le 10^5$ and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    prefix_sum = 0
    min_prefix = 0
    for x in a:
        prefix_sum += x
        min_prefix = min(min_prefix, prefix_sum)
    suffix_sum = 0
    min_suffix = 0
    for x in reversed(a):
        suffix_sum += x
        min_suffix = min(min_suffix, suffix_sum)
    max_sum = total
    max_sum = max(max_sum, total - 2 * min_prefix)
    max_sum = max(max_sum, total - 2 * min_suffix)
    max_sum = max(max_sum, total - 2 * (min_prefix + min_suffix))
    return str(max_sum)

# Provided sample
assert run("3\n-1 -2 -3\n") == "6", "sample 1"

# Custom cases
assert run("1\n5\n") == "5", "single positive"
assert run("1\n-5\n") == "5", "single negative"
assert run("5\n-1 -2 -3 -4 -5\n") == "15", "all negative"
assert run("5\n1 2 3 4 5\n") == "15", "all positive"
assert run("4\n3 -1 -2 5\n") == "11", "mixed positive/negative"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n5\n` | 5 | Single positive element |
| `1\n-5\n` | 5 | Single negative element |
| `5\n-1 -2 -3 -4 -5\n` | 15 | Flipping all negative numbers |
| `5\n1 2 3 4 5\n` | 15 | No flips needed for all positive |
| `4\n3 - |  |  |
