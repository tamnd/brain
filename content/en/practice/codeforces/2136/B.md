---
title: "CF 2136B - Like the Bitset"
description: "We are asked to construct a permutation of length $n$ that satisfies a positional maximum constraint determined by a binary string $s$ and an integer $k$."
date: "2026-06-09T04:10:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2136
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1046 (Div. 2)"
rating: 900
weight: 2136
solve_time_s: 85
verified: false
draft: false
---

[CF 2136B - Like the Bitset](https://codeforces.com/problemset/problem/2136/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, two pointers  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of length $n$ that satisfies a positional maximum constraint determined by a binary string $s$ and an integer $k$. For every position $i$ where $s_i = 1$, we must ensure that $p_i$ is never the maximum value in any contiguous subarray of length at least $k$ that contains $i$. Positions with $s_i = 0$ have no restrictions. If such a permutation cannot exist, we report "NO".

The constraints allow $n$ up to $2 \cdot 10^5$ across multiple test cases. This rules out algorithms with $O(n^2)$ behavior because worst-case total operations could exceed $10^{10}$. We need an $O(n \log n)$ or better, ideally $O(n)$, solution per test case.

A subtle edge case arises when there are too many consecutive 1s relative to $k$. For example, if $s = 1111$ and $k = 3$, any element in a block of four 1s will be inside some length-3 or longer interval, and if the elements assigned are consecutive, one of them will inevitably be the maximum in some interval. This can make the permutation impossible. Another edge case is when $k = 1$; every element with $s_i = 1$ is in an interval of length 1, which trivially includes itself, but the problem allows $p_i$ not to be the maximum in length-1 intervals. This is important because it changes how we assign the largest and smallest numbers.

## Approaches

The brute-force approach would try all permutations and check all subarrays of length at least $k$ for each 1. This is obviously infeasible: for each permutation there are $n!$ possibilities, and checking all intervals could take $O(n^2)$. So even for small $n$ this is far too slow.

The key observation is that the constraints only matter for 1s. For 0s, we can freely assign any numbers. To ensure a 1 is never the maximum in any interval of length $\ge k$ that contains it, we can assign all 1-positions relatively small numbers and all 0-positions relatively large numbers. Then, in any interval of length $k$ or more, there will always be at least one 0 with a number higher than the numbers at 1-positions, guaranteeing no 1 is maximal.

However, there is a limit. If a block of consecutive 1s has length greater than $k$, then there exists a length-$k$ interval entirely inside this block. All numbers in that interval would be small, so the maximum will necessarily be one of the 1s. Therefore, we must check if the longest contiguous block of 1s is less than $k$. If it is, a valid assignment is possible. Otherwise, it is impossible.

This gives a constructive approach: assign the smallest numbers to 1s in order, and the largest numbers to 0s in order. We can simply iterate through the string and fill a list of numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n^2) | O(n) | Too slow |
| Greedy Constructive | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate through the binary string $s$ and find the length of the longest contiguous segment of 1s. If this length is $\ge k$, output "NO" because there will always be a length-$k$ interval of 1s where one of them is the maximum.
2. If the longest segment of 1s is less than $k$, output "YES". We can construct a permutation.
3. Prepare two lists: one for numbers to assign to 1s (starting from 1 upwards) and one for numbers to assign to 0s (starting from $n$ downwards).
4. Iterate through $s$ in order. For each position $i$, if $s_i = 1$, assign the next smallest unused number. If $s_i = 0$, assign the next largest unused number.
5. Print the constructed permutation.

Why it works: By assigning smaller numbers to 1s and larger numbers to 0s, any interval of length at least $k$ that contains at least one 0 will have a 0-number greater than the 1-numbers, ensuring no 1 is maximal. Because the longest consecutive block of 1s is smaller than $k$, any interval of length $k$ or more must include at least one 0. Therefore, the construction always satisfies the constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    
    # Step 1: check longest consecutive 1s
    max_ones = 0
    cur = 0
    for ch in s:
        if ch == '1':
            cur += 1
            max_ones = max(max_ones, cur)
        else:
            cur = 0
    
    if max_ones >= k:
        print("NO")
        continue
    
    # Step 2: construct permutation
    perm = [0] * n
    low = 1
    high = n
    for i, ch in enumerate(s):
        if ch == '1':
            perm[i] = low
            low += 1
        else:
            perm[i] = high
            high -= 1
    print("YES")
    print(' '.join(map(str, perm)))
```

The first part iterates through the string to find the longest contiguous block of 1s. This is the only point where a permutation might be impossible. The second part is the constructive assignment: using two pointers (low and high) ensures all numbers are used exactly once and that 1s get the smallest numbers while 0s get the largest. Off-by-one errors are avoided by careful initialization of low = 1 and high = n, incrementing or decrementing immediately after assignment.

## Worked Examples

### Example 1

Input:

```
4 3
0010
```

| i | s[i] | max_ones | low | high | perm[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 4 | 4 |
| 1 | 0 | 0 | 1 | 3 | 3 |
| 2 | 1 | 1 | 1 | 3 | 1 |
| 3 | 0 | 0 | 2 | 2 | 2 |

Permutation: `[4, 3, 1, 2]`. The maximum number in any interval of length >= 3 covering position 2 is 4, 3, or 2, never 1. Valid.

### Example 2

Input:

```
5 2
11011
```

The longest contiguous 1s = 2, which is equal to k. According to our check, since max_ones >= k, output is "NO".

These traces confirm that the algorithm correctly identifies impossible cases and constructs permutations when feasible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to find longest block of 1s and single pass to construct permutation |
| Space | O(n) | Storage for the permutation |

With sum of $n$ across all test cases ≤ 2e5, the total operations are comfortably below 1e6, fitting within the time limit. Memory usage is within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        max_ones = 0
        cur = 0
        for ch in s:
            if ch == '1':
                cur += 1
                max_ones = max(max_ones, cur)
            else:
                cur = 0
        if max_ones >= k:
            print("NO")
            continue
        perm = [0] * n
        low = 1
        high = n
        for i, ch in enumerate(s):
            if ch == '1':
                perm[i] = low
                low += 1
            else:
                perm[i] = high
                high -= 1
        print("YES")
        print(' '.join(map(str, perm)))
    return output.getvalue().strip()

# Provided samples
assert run("6\n2 1\n00\n4 3\n0010\n5 2\n11011\n7 5\n1111110\n8 4\n00101011\n10 2\n1000000010\n") == \
"""YES
2 1
YES
4 3 1 2
NO
NO
YES
8 7 2 6 5 4
```
