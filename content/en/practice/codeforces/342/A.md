---
title: "CF 342A - Xenia and Divisors"
description: "We are given a sequence of positive integers, all between 1 and 7, whose length is divisible by three. The task is to split this sequence into triplets so that within each triplet the numbers are strictly increasing and each number divides the next."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 342
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 199 (Div. 2)"
rating: 1200
weight: 342
solve_time_s: 362
verified: false
draft: false
---

[CF 342A - Xenia and Divisors](https://codeforces.com/problemset/problem/342/A)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 6m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of positive integers, all between 1 and 7, whose length is divisible by three. The task is to split this sequence into triplets so that within each triplet the numbers are strictly increasing and each number divides the next. Each integer must appear in exactly one triplet, so the number of triplets will be one-third of the sequence length. If no such partition exists, the output should be -1.

The constraints make this problem manageable with simple counting. Since the largest number is 7, we can reason about valid triplets directly, rather than searching through all permutations. Because n can be up to 100,000 and we have a one-second time limit, an algorithm that examines every element a constant number of times, O(n), is acceptable. A naive brute-force search over all possible groupings, which would have complexity O(n³) or worse, is infeasible.

A non-obvious edge case occurs when the sequence contains elements that could form valid divisibility chains individually but cannot be grouped without leaving leftover numbers. For example, the sequence `[1, 1, 1, 2, 2, 2]` seems promising, but no combination of strictly increasing divisible triplets exists, so the correct output is -1. Another edge case is when numbers 5, 6, or 7 appear, as these cannot form valid triplets with 1, 2, 3, 4 under the given divisibility rules.

## Approaches

The brute-force approach would attempt to generate all possible triplets from the sequence, check if they satisfy the conditions, and then attempt to combine them into a partition covering all elements. This is correct in theory but requires O(n³) operations just to generate candidates and much more to verify partitions, which is prohibitive for n up to 100,000.

The key insight is to exploit the small number of distinct values (1 through 7) and the divisibility rules. Valid triplets must follow specific patterns that satisfy a < b < c and a divides b and b divides c. By enumerating possibilities, we find only three feasible triplets: (1, 2, 4), (1, 2, 6), and (1, 3, 6). No other combinations of numbers 1 through 7 meet both the divisibility and strict ordering requirements. This observation reduces the problem to counting occurrences of each number and greedily forming as many of these triplets as possible. If at any point the counts do not allow a valid formation, the answer is -1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n³) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each number from 1 to 7. This will allow us to determine how many triplets of each type we can form. Since numbers are at most 7, we only need an array of length 8.
2. Check for numbers 5 and 7. They cannot appear in any valid triplet, so if they exist, output -1.
3. Determine the maximum number of triplets (1, 2, 4) we can form by taking the minimum count among 1, 2, and 4.
4. Subtract the numbers used for these triplets from their counts.
5. Determine the maximum number of triplets (1, 2, 6) we can form using the remaining counts of 1, 2, and 6.
6. Subtract the numbers used for these triplets.
7. Determine the maximum number of triplets (1, 3, 6) we can form using the remaining counts of 1, 3, and 6.
8. Subtract the numbers used for these triplets.
9. If any counts remain non-zero, output -1 because leftover numbers cannot form valid triplets. Otherwise, print all triplets in any order, as long as each triplet is printed in increasing order.

Why it works: The invariant is that we only form triplets that satisfy both the divisibility and strict ordering conditions. Because the numbers are limited to 1 through 7, any sequence that can be partitioned must be fully composed of these three triplet types. Attempting to form any other triplet would violate the constraints, so greedily forming as many as possible and verifying that no numbers remain guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))

count = [0] * 8
for x in arr:
    count[x] += 1

# Numbers 5 and 7 cannot be part of any valid triplet
if count[5] > 0 or count[7] > 0:
    print(-1)
    sys.exit()

triplets = []

# Form (1, 2, 4)
t124 = min(count[1], count[2], count[4])
for _ in range(t124):
    triplets.append((1, 2, 4))
count[1] -= t124
count[2] -= t124
count[4] -= t124

# Form (1, 2, 6)
t126 = min(count[1], count[2], count[6])
for _ in range(t126):
    triplets.append((1, 2, 6))
count[1] -= t126
count[2] -= t126
count[6] -= t126

# Form (1, 3, 6)
t136 = min(count[1], count[3], count[6])
for _ in range(t136):
    triplets.append((1, 3, 6))
count[1] -= t136
count[3] -= t136
count[6] -= t136

# Check if any numbers remain
if any(count[1:7]):
    print(-1)
else:
    for trip in triplets:
        print(*trip)
```

The solution first counts each number to efficiently track availability. It then checks for impossible numbers and proceeds to greedily form valid triplets, always consuming the smallest numbers first to satisfy the strict ordering. Finally, it verifies that no numbers remain ungrouped.

## Worked Examples

Sample 1:

Input: `6\n1 1 1 2 2 2`

| Count of numbers | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| After (1,2,4) | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| After (1,2,6) | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| After (1,3,6) | 3 | 3 | 0 | 0 | 0 | 0 | 0 |

Triplets cannot be formed, counts remain, output is -1. This trace confirms the algorithm correctly identifies impossible partitions.

Sample 2:

Input: `6\n1 2 4 1 3 6`

| Count of numbers | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 2 | 1 | 1 | 1 | 0 | 1 | 0 |
| After (1,2,4) | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| After (1,2,6) | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| After (1,3,6) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

All counts consumed, output:

```
1 2 4
1 3 6
```

This trace demonstrates correct greedy triplet formation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting elements and forming triplets require scanning the array and iterating up to n/3 times |
| Space | O(1) | Only an array of size 8 is needed plus output storage proportional to n |

Given n ≤ 100,000, these operations are comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Paste the solution here
    n = int(input())
    arr = list(map(int, input().split()))
    count = [0] * 8
    for x in arr:
        count[x] += 1
    if count[5] > 0 or count[7] > 0:
        print(-1)
        return output.getvalue().strip()
    triplets = []
    t124 = min(count[1], count[2], count[4])
    for _ in range(t124):
        triplets.append((1, 2, 4))
    count[1] -= t124
    count[2] -= t124
    count[4]()
```
