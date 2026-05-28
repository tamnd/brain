---
title: "CF 131B - Opposites Attract"
description: "We are asked to count all pairs of clients whose assigned numbers are exact opposites. Each client has a number between -10 and 10, and a pair is valid if one client has number $x$ and the other has number $-x$."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 131
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 95 (Div. 2)"
rating: 1200
weight: 131
solve_time_s: 94
verified: true
draft: false
---

[CF 131B - Opposites Attract](https://codeforces.com/problemset/problem/131/B)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count all pairs of clients whose assigned numbers are exact opposites. Each client has a number between -10 and 10, and a pair is valid if one client has number $x$ and the other has number $-x$. Zero is considered its own opposite, so two clients with number 0 form a valid pair. The order of clients does not matter, so each pair should be counted only once, and a client cannot pair with themselves.

The input consists of the number of clients $n$ and a list of their assigned numbers $t_1, t_2, \dots, t_n$. The output is the total number of valid opposite pairs.

Since $n$ can be as large as $10^5$, a brute-force approach that checks all pairs explicitly would require roughly $n^2/2$ operations, which is $5 \cdot 10^9$ in the worst case. This is too slow for a 2-second limit, so we need a linear or near-linear solution. All numbers are within a small, fixed range, which hints at a counting-based approach. Edge cases include all zeros, repeated numbers, and negative-positive symmetry. For example, if the input is `0 0 0`, there are 3 pairs: `(1,2)`, `(1,3)`, `(2,3)`. A naive approach that checks pairs with two loops might either double-count pairs or miss the zero self-pairing.

## Approaches

The brute-force approach is simple: iterate over all pairs of clients, check if their numbers are opposites, and increment a counter. This works for correctness but runs in $O(n^2)$, which is infeasible for $n=10^5$ since it would perform around $5 \cdot 10^9$ comparisons. Memory is negligible, but the runtime makes this approach unacceptable.

The optimal approach uses a counting strategy. First, create a frequency map of all numbers in the list. For each number $x$, the number of valid pairs formed with its opposite $-x$ is the product of the count of $x$ and the count of $-x$. Special handling is required for zero: the number of pairs among zeros is $\binom{count_0}{2} = count_0 \cdot (count_0-1)/2$. To avoid double-counting, only consider positive numbers (including zero) when multiplying counts with their opposites.

The observation that the numbers are small and bounded makes it feasible to use either a fixed-size array of length 21 (for -10 to 10) or a dictionary to track counts. This reduces the runtime to $O(n)$ for counting and $O(1)$ for computing pairs using the fixed number of possible values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) (fixed array) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter array `freq` of size 21 to store the frequency of numbers from -10 to 10. The index for a number $x$ is `x + 10`.
2. Iterate through the input list and increment the corresponding index in `freq` for each number. This constructs a frequency map in linear time.
3. Initialize a variable `pairs` to 0 to store the total number of opposite pairs.
4. Iterate through numbers from 1 to 10. For each number `x`, multiply `freq[x + 10]` by `freq[-x + 10]` and add the result to `pairs`. This counts all pairs with opposite numbers once without double-counting.
5. Handle zero separately. If `freq[10]` is the count of zeros, add `freq[10] * (freq[10] - 1) // 2` to `pairs` to account for all zero-zero pairs.
6. Print the value of `pairs`.

Why it works: the algorithm correctly counts all pairs by using the invariant that for every number $x > 0$, we include all combinations with its negative exactly once. Zero is treated with the combination formula because it pairs with itself. This ensures no pair is counted twice, and no invalid self-pairing occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))

# frequency array for numbers -10 to 10
freq = [0] * 21
for num in nums:
    freq[num + 10] += 1

pairs = 0
# count positive-negative pairs
for i in range(1, 11):
    pairs += freq[i + 10] * freq[-i + 10]

# count zero pairs
pairs += freq[10] * (freq[10] - 1) // 2

print(pairs)
```

The first part reads input and constructs the frequency array. The loop over positive numbers calculates pairs with negatives without double-counting. The zero case uses the combination formula for selecting 2 elements from `freq[10]` zeros. We use integer division to get an exact integer count.

## Worked Examples

**Sample 1:**

Input: `-3 3 0 0 3`

| num | freq index | freq after counting |
| --- | --- | --- |
| -3 | 7 | 1 |
| 3 | 13 | 1 |
| 0 | 10 | 1 |
| 0 | 10 | 2 |
| 3 | 13 | 2 |

Pairs calculation:

| i | freq[i+10] | freq[-i+10] | product |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 2 | 1 | 2 |

Zero pairs: `freq[10] * (freq[10]-1)//2 = 2*1//2 = 1`

Total pairs = 2 + 1 = 3

**Sample 2:**

Input: `1 -1 1 -1`

| i | freq[i+10] | freq[-i+10] | product |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 4 |

Zero pairs: none

Total pairs = 4

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constructing frequency array is linear in the number of clients. Calculating pairs involves at most 10 iterations. |
| Space | O(1) | Frequency array has 21 fixed elements, independent of n. |

Since n ≤ 10^5, the linear pass through the list is fast enough. Memory usage is minimal, so the solution fits comfortably within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    nums = list(map(int, input().split()))
    freq = [0]*21
    for num in nums:
        freq[num+10] += 1
    pairs = 0
    for i in range(1, 11):
        pairs += freq[i+10]*freq[-i+10]
    pairs += freq[10]*(freq[10]-1)//2
    return str(pairs)

# provided samples
assert run("5\n-3 3 0 0 3\n") == "3", "sample 1"
assert run("4\n1 -1 1 -1\n") == "4", "sample 2"

# custom cases
assert run("1\n0\n") == "0", "single zero"
assert run("3\n0 0 0\n") == "3", "three zeros"
assert run("6\n-10 10 -10 10 -10 10\n") == "9", "max absolute value"
assert run("5\n1 1 1 1 1\n") == "0", "all equal positive"
assert run("5\n-1 -1 -1 -1 -1\n") == "0", "all equal negative"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 | 0 | minimum input, no pairs |
| 3\n0 0 0 | 3 | multiple zeros, zero pairing logic |
| 6\n-10 10 -10 10 -10 10 | 9 | large absolute values, repeated pairing |
| 5\n1 1 1 1 1 | 0 | all same positive numbers |
| 5\n-1 -1 -1 -1 -1 | 0 | all same negative numbers |

## Edge Cases

For the zero case, input `0 0 0` results in frequency `freq[10] = 3`. The pair count formula computes `3*2/2 = 3` pairs, correctly enumerating `(1,2)`, `(1,3)`, `(2,3)`. For all identical positive numbers, e.g., `1 1 1`, the count array has `freq[11] = 3`, but `freq[-1+10] = freq[9] = 0`, so no pairs are added.
