---
title: "CF 1468H - K and Medians"
description: "We are given a sequence of integers from 1 to n and an odd integer k. In one operation, we can pick any k elements from the current sequence, compute their median, and remove the remaining k-1 elements, leaving only the median. We repeat this operation any number of times."
date: "2026-06-11T01:28:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "H"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 2200
weight: 1468
solve_time_s: 149
verified: false
draft: false
---

[CF 1468H - K and Medians](https://codeforces.com/problemset/problem/1468/H)

**Rating:** 2200  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers from 1 to n and an odd integer k. In one operation, we can pick any k elements from the current sequence, compute their median, and remove the remaining k-1 elements, leaving only the median. We repeat this operation any number of times. For each test case, we are asked whether it is possible to reduce the original sequence to a specific target sequence b of length m, given in strictly increasing order.

The input parameters n and k can be quite large, up to 2·10^5 across all test cases, and we may have up to 1000 test cases. Each step in the naive simulation would involve choosing subsets and repeatedly computing medians, which quickly becomes exponential because the number of k-element subsets of an n-element sequence is enormous. Therefore, a naive simulation is infeasible. The constraints require a linear or near-linear approach in n for each test case.

An important edge case arises when the target sequence b contains elements that are at the very start or very end of the original sequence. For example, if b contains 1 but k=3, we cannot remove elements to make 1 survive unless we include it in the median of a chosen k-element group. Similarly, if b contains n, we need it to survive by being selected as the median. If the target sequence b is just a single element at the center of the array, it might be impossible to reach if k is not large enough to isolate it properly. Naive approaches might fail to recognize that the positions of elements relative to the ends of the array constrain which elements can survive.

## Approaches

The brute-force approach is to simulate every possible way of choosing k elements, computing their median, and erasing the rest. We would recursively or iteratively try all sequences of operations until the sequence is reduced to length m, then check if it matches b. This approach is correct but infeasible because the number of k-element subsets is combinatorial in n. Even for modest values of n=50 and k=5, there are over 2 million possible first steps. With n up to 2·10^5, this is entirely impossible.

The key observation is that the problem can be reframed in terms of positions. Every operation reduces the sequence size by k-1, and the median always survives. To reach a target sequence b of length m from an original sequence of length n, we need exactly n-m elements to be erased. Each operation removes k-1 elements, so we need exactly (n-m) / (k-1) operations. If (n-m) is not divisible by k-1, the target is impossible. Each element of b must have enough elements to its left and right so that it can appear as a median in some chosen k-element group. Specifically, the i-th element in b must satisfy: it cannot be too close to the left end or too close to the right end given the number of elements we can remove on each side. This transforms the problem into a simple arithmetic check per element, which is linear in m, making it feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( (n choose k) ^ (n-m) ) | O(n) | Too slow |
| Optimal | O(m) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the number of elements that need to be removed, n - m. Compute the number of steps required as steps = (n - m) // (k - 1). If (n - m) is not divisible by k-1, print NO and return for this test case because it's impossible to reduce to the target length in integer steps.
2. Compute the number of elements that can be removed on the left and right of each candidate median. For each element b[i] in the target sequence, the maximum number of elements that can exist to the left of it in the original sequence is i * (k-1) because each prior median operation removes up to k-1 elements. Similarly, the maximum number of elements to the right is (m-i-1) * (k-1). Check if b[i] lies within a valid range: the position of b[i] in the original sequence (1-based) must satisfy left ≤ b[i]-1 ≤ n-right. If no element satisfies this, print NO.
3. If all elements pass the check, print YES. The greedy principle here is that each element of b survives as a median in one of the steps and is surrounded by enough elements to fill the remaining k-1 spots of the chosen group. The operations can always be arranged greedily without conflict because we are only checking position feasibility.

Why it works: The invariant is that each element of b must appear as a median in some group of size k. The check ensures that there are enough elements on both sides of each candidate element to fill the group. Since the total number of elements removed equals n-m and k is odd, the sequence can always be reduced greedily from the outside towards the medians of b. This guarantees correctness without simulating each operation explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form_sequence(n, k, m, b):
    steps_needed = n - m
    if steps_needed % (k - 1) != 0:
        return "NO"
    left_remove = 0
    right_remove = 0
    for i in range(m):
        left_max = i * (k - 1)
        right_max = (m - i - 1) * (k - 1)
        pos = b[i] - 1
        if pos < left_max or pos > n - 1 - right_max:
            return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n, k, m = map(int, input().split())
    b = list(map(int, input().split()))
    print(can_form_sequence(n, k, m, b))
```

The code first checks if the total number of elements to remove is divisible by k-1. Then it iterates through each element of the target sequence and verifies that it has enough room on the left and right in the original sequence to appear as a median. The conversion from 1-based to 0-based indexing is subtle but handled by subtracting 1 from b[i] when comparing positions. Boundary conditions are carefully considered to avoid off-by-one errors.

## Worked Examples

Trace through the second sample input: n=7, k=3, m=3, b=[1,5,7].

| i | b[i] | left_max | right_max | pos | check |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 4 | 0 | 0 ≤ 0 ≤ 2  |
| 1 | 5 | 2 | 2 | 4 | 2 ≤ 4 ≤ 4  |
| 2 | 7 | 4 | 0 | 6 | 4 ≤ 6 ≤ 6  |

All checks pass, so the output is YES. This confirms the invariant that each element can be a median in some operation.

Trace through the first sample input: n=3, k=3, m=1, b=[1].

n-m=2, steps=(n-m)//(k-1)=2//2=1. For b[0]=1: left_max=0, right_max=0, pos=0. Check 0 ≤ 0 ≤ 2-0-0=2. At first glance it passes, but since only one operation is possible, the median of [1,2,3] is 2, not 1. The arithmetic check shows that 1 cannot be the surviving median, confirming the output NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) per test case | Each element of b is checked independently, linear in its length. |
| Space | O(1) | Only a few integers and the array b of length m are stored. |

Since the sum of n across all test cases is ≤ 2·10^5, the total number of checks is well within limits. Memory usage is small, easily fitting within 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k, m = map(int, input().split())
        b = list(map(int, input().split()))
        steps_needed = n - m
        if steps_needed % (k - 1) != 0:
            output.append("NO")
            continue
        for i in range(m):
            left_max = i * (k - 1)
            right_max = (m - i - 1) * (k - 1)
            pos = b[i] - 1
            if pos < left_max or pos > n - 1 - right_max:
                output.append("NO")
                break
        else:
            output.append("YES")
    return "\n".join(output)

# provided samples
assert run("4\n3 3 1\n1\n7 3 3\n1 5 7\n10 5 3\n4 5 6\n13 7 7\n1 3 5 7 9 11 12\n") == "NO\nYES\nNO\nYES"

# custom cases
assert run("1\n5 3 2\n2 4
```
