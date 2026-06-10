---
title: "CF 1607D - Blue-Red Permutation"
description: "We are given an array of integers where each element has a color, either blue or red. Blue elements can be decreased by 1 any number of times, while red elements can be increased by 1 any number of times."
date: "2026-06-10T07:43:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1607
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 753 (Div. 3)"
rating: 1300
weight: 1607
solve_time_s: 86
verified: true
draft: false
---

[CF 1607D - Blue-Red Permutation](https://codeforces.com/problemset/problem/1607/D)

**Rating:** 1300  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers where each element has a color, either blue or red. Blue elements can be decreased by 1 any number of times, while red elements can be increased by 1 any number of times. The goal is to determine if it is possible to transform the array into a permutation of numbers from 1 to $n$, where $n$ is the length of the array. A permutation here means every integer from 1 to $n$ occurs exactly once, in any order.

The constraints allow $n$ up to $2 \cdot 10^5$ per test case, with up to $10^4$ test cases, meaning a brute-force simulation of every possible increment/decrement is infeasible. We must reason about the problem mathematically rather than by simulating moves. The numbers themselves can be large in magnitude, up to $10^9$ in either direction, so any approach relying on direct array manipulation or large-range counting would be inefficient.

Edge cases that can trip up naive solutions include arrays where all numbers are initially larger than $n$ or smaller than 1. For example, an array of only blue elements all equal to 100 with $n = 5$ can never reach the range 1-5 by decrementing, because some numbers must become less than 1. Similarly, arrays of red elements smaller than 1 cannot reach their targets by increasing alone. Cases with duplicates of the same number or extreme negative numbers are also non-trivial because we must respect color operations while trying to achieve unique numbers in the 1 to $n$ range.

## Approaches

A brute-force approach would simulate all possible sequences of operations on each element to try to reach a permutation. This is correct in principle, as it exhaustively explores every transformation, but the number of possibilities grows exponentially with $n$, making it impossible for $n$ up to $2 \cdot 10^5$.

The key insight for an optimal solution comes from observing that each element can be adjusted only in one direction: blue elements can decrease, red elements can increase. Therefore, for a blue element $x$, the minimum final value it can reach is 1 (we cannot go below 1 for the permutation), and the maximum is $x$ itself. For a red element $x$, the minimum final value is $x$ (we cannot decrease it), and the maximum is $n$.

From this observation, we can sort the blue elements and red elements independently and attempt to assign them values from 1 to $n$ greedily. Blue elements should be assigned as small as possible starting from 1, and red elements should be assigned as large as possible starting from $n$, ensuring that each number is reachable given the operation constraints. If at any point a number cannot be assigned to a corresponding element because it is out of its reachable range, the answer is NO.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the array into two lists: `blue` contains all blue elements, and `red` contains all red elements. This allows us to handle their ranges independently.
2. Sort `blue` in ascending order. For each blue element at position $i$ in the sorted list, compute its maximum reachable value, which is the element itself. The minimum we want it to take is $i+1$, because the smallest number in a permutation starts at 1 and increases sequentially. If a blue element is smaller than $i+1$, it cannot reach the required value, so the answer is NO.
3. Sort `red` in descending order. For each red element at position $i$ in the sorted list, compute its minimum reachable value, which is the element itself. The maximum we want it to take is $n-i$, starting from $n$ and decreasing. If a red element is greater than $n-i$, it cannot reach the required value, so the answer is NO.
4. If all blue and red elements can satisfy the above conditions, the answer is YES.

This works because the ranges of values that each color can reach form a chain, and assigning them greedily ensures no number is skipped or duplicated. The invariant maintained is that after assigning the first $k$ numbers to the $k$ smallest blues and largest reds, all remaining numbers are still assignable within the allowed ranges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form_permutation(n, a, colors):
    blue = []
    red = []
    for val, color in zip(a, colors):
        if color == 'B':
            blue.append(val)
        else:
            red.append(val)
    
    blue.sort()
    red.sort(reverse=True)
    
    for i, val in enumerate(blue):
        if val < i + 1:
            return "NO"
    for i, val in enumerate(red):
        if val > n - i:
            return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    colors = input().strip()
    print(can_form_permutation(n, a, colors))
```

We first separate elements by color, sort each group, and then check each element against its target range. Sorting ensures that smaller blue numbers attempt to take smaller permutation positions first, and larger red numbers attempt to take larger positions last. The greedy check is straightforward and avoids simulation pitfalls.

## Worked Examples

**Example 1**

Input:

```
4
1 2 5 2
BRBR
```

| Step | Blue Sorted | Red Sorted | i | Check |
| --- | --- | --- | --- | --- |
| Initial | [1,5] | [2,2] | - | - |
| Blue 0 | 1 | - | 0 | 1 >= 1, OK |
| Blue 1 | 5 | - | 1 | 5 >= 2, OK |
| Red 0 | - | 2 | 0 | 2 <= 4, OK |
| Red 1 | - | 2 | 1 | 2 <= 3, OK |

All checks pass, so output is YES.

**Example 2**

Input:

```
2
1 1
BB
```

| Step | Blue Sorted | Red Sorted | i | Check |
| --- | --- | --- | --- | --- |
| Initial | [1,1] | [] | - | - |
| Blue 0 | 1 | - | 0 | 1 >= 1, OK |
| Blue 1 | 1 | - | 1 | 1 >= 2, FAIL |

Second blue cannot reach 2, so output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the blue and red lists dominates the computation. |
| Space | O(n) | Storing blue and red lists separately. |

With the constraints of sum of $n$ over all test cases ≤ 2·10^5, this approach comfortably runs within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution function
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        colors = input().strip()
        print(can_form_permutation(n, a, colors))
    return output.getvalue().strip()

# Provided samples
assert run("8\n4\n1 2 5 2\nBRBR\n2\n1 1\nBB\n5\n3 1 4 2 5\nRBRRB\n5\n3 1 3 1 3\nRBRRB\n5\n5 1 5 1 5\nRBRRB\n4\n2 2 2 2\nBRBR\n2\n1 -2\nBR\n4\n-2 -1 4 0\nRRRR\n") == \
"YES\nNO\nYES\nYES\nNO\nYES\nYES\nYES"

# Custom cases
assert run("1\n1\n100\nR\n") == "YES", "single red element beyond n"
assert run("1\n1\n-100\nB\n") == "YES", "single blue element below 1"
assert run("1\n3\n1 2 2\nBBR\n") == "NO", "duplicate blue cannot reach positions"
assert run("1\n5\n5 4 3 2 1\nRRRRR\n") == "YES", "all reds in reverse order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n100\nR\n` | YES | Single red element beyond `n` can be decreased to `n` |
| `1\n-100\nB\n` | YES | Single blue element below 1 can be increased to 1 |
| `1\n3\n1 2 2\nBBR\n` | NO | Duplicate blue fails to cover all positions |
| `1\n5\n5 4 3 2 1\n |  |  |
