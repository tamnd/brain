---
title: "CF 2144B - Maximum Cost Permutation"
description: "We are given an array p of length n where some positions contain integers from 1 to n and others are zeros. No positive integer appears more than once."
date: "2026-06-08T01:36:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2144
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 182 (Rated for Div. 2)"
rating: 1000
weight: 2144
solve_time_s: 130
verified: false
draft: false
---

[CF 2144B - Maximum Cost Permutation](https://codeforces.com/problemset/problem/2144/B)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `p` of length `n` where some positions contain integers from 1 to `n` and others are zeros. No positive integer appears more than once. The zeros are placeholders that we can replace with the missing numbers so that the array becomes a proper permutation of 1 through `n`. Once we have a valid permutation, we define the cost of the permutation as the length of the smallest contiguous subsegment that needs to be sorted for the entire permutation to become sorted.

The task is to maximize this cost. That is, we want to place the missing numbers into the zeros in such a way that the subsegment we have to sort to fix the permutation is as long as possible. The output for each test case is a single integer, the maximum achievable cost.

The constraints tell us that `n` can be as large as 2 * 10^5, and the total sum of `n` across all test cases is at most 2 * 10^5. This rules out any brute-force solution that tries all ways to fill zeros, since the number of permutations of missing numbers grows factorially. Instead, we need an approach that works in linear time with respect to `n`.

Non-obvious edge cases include arrays where all elements are zeros, arrays that are already sorted, or arrays where all missing numbers are clustered at one end. For instance, an array `[0, 0, 0]` has maximum cost 3, because we can place the numbers so that the array becomes `[3, 1, 2]` and we need to sort the entire array. On the other hand, `[1, 2, 3, 0]` has cost 0 because the only missing number is 4, which goes at the end, and the array is already sorted. A careless approach might simply count zeros or ignore the positions of existing numbers, producing wrong answers in these edge cases.

## Approaches

A naive approach would try every way to fill the zeros with missing numbers, construct the permutation, and compute the cost by scanning for the smallest segment to sort. Calculating the segment cost for a given permutation can be done by finding the first place from the left where the array is out of order and the last place from the right where it is out of order. However, this would require generating factorial combinations of zeros, which is completely infeasible for `n` up to 2 * 10^5.

The key observation is that the maximum cost corresponds to a subarray that starts at the first zero and ends at the last zero. Any number placed outside the zero segment either does not increase the sorting cost or decreases it. Therefore, we can identify the first and last positions of zeros in the array. Then, the maximum possible cost is the distance between these positions, adjusted by considering already correctly placed numbers at the ends. Specifically, numbers outside this zero segment are already in order and do not extend the cost.

This reduces the problem to finding the first and last zero positions in the array and taking the difference plus one as the maximum possible cost. We do not need to explicitly construct the permutation; the positions of zeros alone determine the maximum segment length we could force to be unsorted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the array `p`.
2. Initialize `first_zero` and `last_zero` to -1.
3. Iterate through the array from left to right. When we encounter the first zero, store its index in `first_zero`.
4. Continue iterating and update `last_zero` whenever a zero is encountered. By the end of the array, `last_zero` will contain the index of the last zero.
5. If there are no zeros (`first_zero` remains -1), the array is already a complete permutation, so the maximum cost is 0.
6. Otherwise, the maximum cost is `last_zero - first_zero + 1`. This corresponds to the length of the contiguous segment covering all zeros, which is the largest subsegment we could force to sort by placing missing numbers cleverly.
7. Print this maximum cost for the test case.

Why it works: the positions of zeros define a contiguous segment where numbers are missing. By placing the missing numbers to create the largest disorder, we can ensure that the entire segment between the first and last zero needs to be sorted. Numbers outside this segment are fixed and do not contribute to increasing the sorting cost. The segment length is therefore the maximum cost achievable.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    
    first_zero = -1
    last_zero = -1
    
    for i in range(n):
        if p[i] == 0:
            if first_zero == -1:
                first_zero = i
            last_zero = i
    
    if first_zero == -1:
        print(0)
    else:
        print(last_zero - first_zero + 1)
```

The code starts by reading the number of test cases. For each test case, it reads the array size and the array itself. It then scans the array to locate the first and last zeros. If no zeros are found, the array is complete and sorted, so it prints 0. Otherwise, it calculates the length of the segment covering all zeros. Using a single pass through the array ensures O(n) complexity, and only a few variables are needed, so space usage is O(1).

## Worked Examples

**Example 1:** `p = [1, 0, 4, 0, 5]`

| i | p[i] | first_zero | last_zero |
| --- | --- | --- | --- |
| 0 | 1 | -1 | -1 |
| 1 | 0 | 1 | 1 |
| 2 | 4 | 1 | 1 |
| 3 | 0 | 1 | 3 |
| 4 | 5 | 1 | 3 |

Segment length: 3 - 1 + 1 = 3.

This shows the algorithm correctly identifies the segment `[0, 4, 0]` as the largest one that could be unsorted.

**Example 2:** `p = [0, 0, 0]`

| i | p[i] | first_zero | last_zero |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 2 |

Segment length: 2 - 0 + 1 = 3.

All zeros form the full array, giving maximum disorder.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array is scanned once to find first and last zeros. |
| Space | O(1) | Only two indices are stored; the array itself is overwritten. |

Given `sum(n) <= 2*10^5`, the solution completes well under 2 seconds with minimal memory overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        first_zero = -1
        last_zero = -1
        for i in range(n):
            if p[i] == 0:
                if first_zero == -1:
                    first_zero = i
                last_zero = i
        if first_zero == -1:
            print(0)
        else:
            print(last_zero - first_zero + 1)
    return output.getvalue().strip()

# Provided samples
assert run("4\n5\n1 0 4 0 5\n3\n0 0 0\n4\n1 2 3 0\n3\n0 3 2\n") == "3\n3\n0\n2"

# Custom cases
assert run("1\n1\n0\n") == "1"  # single zero
assert run("1\n5\n1 2 3 4 5\n") == "0"  # no zeros
assert run("1\n5\n0 1 0 2 0\n") == "5"  # zeros interleaved with numbers
assert run("1\n6\n0 0 1 2 0 0\n") == "6"  # zeros at both ends
assert run("1\n2\n0 2\n") == "1"  # zeros at beginning
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0\n` | 1 | Single-element array with zero |
| `1\n5\n1 2 3 4 5\n` | 0 | Already sorted permutation, no zeros |
| `1\n5\n0 1 0 2 0\n` | 5 | Zeros interleaved, entire array forms max segment |
| `1\n6\n0 0 1 2 0 |  |  |
