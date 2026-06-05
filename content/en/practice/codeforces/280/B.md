---
title: "CF 280B - Maximum Xor Secondary"
description: "We are given an array of distinct positive integers, and our task is to find the largest possible \"lucky number\" obtainable from any contiguous subarray of length at least two. A \"lucky number\" is defined as the bitwise XOR of the largest and second largest element in a subarray."
date: "2026-06-05T09:03:41+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 280
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 172 (Div. 1)"
rating: 1800
weight: 280
solve_time_s: 99
verified: true
draft: false
---

[CF 280B - Maximum Xor Secondary](https://codeforces.com/problemset/problem/280/B)

**Rating:** 1800  
**Tags:** data structures, implementation, two pointers  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct positive integers, and our task is to find the largest possible "lucky number" obtainable from any contiguous subarray of length at least two. A "lucky number" is defined as the bitwise XOR of the largest and second largest element in a subarray.

The input consists of the array length $n$ and the $n$ integers themselves. The output is a single integer: the maximum lucky number among all subarrays.

With $n$ up to $10^5$ and each number up to $10^9$, a naive approach that examines all subarrays is infeasible. There are roughly $n^2/2$ subarrays, and for each, finding the two largest numbers takes $O(r-l)$, leading to an $O(n^3)$ algorithm. This is clearly far too slow for the time limit.

A non-obvious edge case arises when the array is sorted in ascending or descending order. For example, for `s = [1, 2, 3, 4]`, the maximum lucky number is `4 XOR 3 = 7`. A careless approach that only checks adjacent pairs or tries to maintain the "current max" without considering the second largest can miss the correct answer.

Another subtlety is that only contiguous subarrays matter. The largest overall number XORed with the second largest anywhere in the array is not always the answer. For example, in `s = [1, 100, 2]`, the global maximum is 100, but the second maximum in some subarrays might be 2 or 1, producing different XOR values.

## Approaches

The brute-force approach works by iterating over all subarrays, finding the two largest numbers in each, computing their XOR, and keeping track of the maximum. This is correct because it checks every possible candidate, but it requires roughly $O(n^3)$ operations: there are $O(n^2)$ subarrays, and computing the two largest numbers in each takes $O(n)$. For $n = 10^5$, this is completely impractical.

The key insight is that in any subarray, the maximum lucky number is produced by one of the two largest numbers that are **adjacent in value when considered from left to right in the array**. This is because if you look at the XOR operation, a smaller number further away from the maximum never contributes a larger XOR than the immediate neighbors in the array.

This reduces the problem to checking only **consecutive pairs** of numbers in the array and their running maximums. A stack-based approach can be used: iterate left-to-right, maintain a decreasing stack of numbers, and for each new number, compute XORs with elements popped from the stack. This efficiently captures all candidate subarrays that could produce the maximum lucky number.

The observation that the maximum XOR in a subarray is always achieved by either the current number and the previous larger neighbor on the left, or the current number and the previous larger neighbor on the right, lets us reduce the problem from $O(n^2)$ to $O(n)$ in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Stack-based Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty stack and a variable `ans = 0` to track the maximum lucky number.
2. Iterate through each element `x` in the array.
3. While the stack is non-empty:

1. Compute the XOR of `x` with the top element of the stack.
2. Update `ans` if this XOR is larger than the current `ans`.
3. If the top of the stack is larger than `x`, break. Otherwise, pop the top element.
4. Push `x` onto the stack.
5. Repeat until all elements have been processed.
6. Print `ans`.

The stack maintains a decreasing sequence of numbers from left to right. Each XOR computed is a candidate for the maximum lucky number. We do not need to check all subarrays explicitly because any other element would produce a smaller XOR than one of these pairs.

**Why it works:** Every pair of adjacent numbers in the decreasing stack represents a subarray where one of them is the maximum and the other is the second maximum. By checking each number against elements popped from the stack, we are effectively checking all subarrays that can produce a larger XOR. No candidate is missed because any number smaller than the current top will not produce a larger XOR with previous elements than the immediate neighbors.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = list(map(int, input().split()))

stack = []
ans = 0

for x in s:
    while stack:
        ans = max(ans, stack[-1] ^ x)
        if stack[-1] > x:
            break
        stack.pop()
    stack.append(x)

print(ans)
```

This solution directly implements the stack-based approach. We iterate through each number, compare it with the decreasing stack, and compute XORs. The break condition ensures we only keep numbers in decreasing order, and popping smaller numbers guarantees we do not miss potential second maxima in contiguous subarrays. Using fast input with `sys.stdin.readline` ensures the program runs within the 1-second time limit for $n \le 10^5$.

## Worked Examples

**Sample 1:**

Input: `5`

Array: `[5, 2, 1, 4, 3]`

| Step | Stack | XOR Computed | ans |
| --- | --- | --- | --- |
| 5 | [5] | - | 0 |
| 2 | [5,2] | 5^2=7 | 7 |
| 1 | [5,2,1] | 2^1=3 | 7 |
| 4 | [5,4] | 1^4=5, 2^4=6 | 7 |
| 3 | [5,4,3] | 4^3=7 | 7 |

The maximum lucky number is 7, produced by subarrays `[5,2]` and `[4,3]`.

**Sample 2:**

Input: `4`

Array: `[8, 3, 5, 7]`

| Step | Stack | XOR Computed | ans |
| --- | --- | --- | --- |
| 8 | [8] | - | 0 |
| 3 | [8,3] | 8^3=11 | 11 |
| 5 | [8,5] | 3^5=6, 8^5=13 | 13 |
| 7 | [8,7] | 5^7=2, 8^7=15 | 15 |

The maximum lucky number is 15, produced by `[8,7]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is pushed and popped at most once from the stack |
| Space | O(n) | The stack may hold up to n elements in the worst case |

This is efficient for $n \le 10^5$ and fits comfortably within the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    s = list(map(int, input().split()))
    stack = []
    ans = 0
    for x in s:
        while stack:
            ans = max(ans, stack[-1] ^ x)
            if stack[-1] > x:
                break
            stack.pop()
        stack.append(x)
    return str(ans)

# Provided samples
assert run("5\n5 2 1 4 3\n") == "7", "sample 1"
assert run("4\n8 3 5 7\n") == "15", "sample 2"

# Custom cases
assert run("2\n1 2\n") == "3", "minimum-size input"
assert run("3\n1 2 3\n") == "3", "ascending sequence"
assert run("3\n3 2 1\n") == "3", "descending sequence"
assert run("5\n10 1 5 8 3\n") == "15", "mix of large and small numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 2 | 3 | Minimum-size input |
| 3 1 2 3 | 3 | Ascending sequence |
| 3 3 2 1 | 3 | Descending sequence |
| 5 10 1 5 8 3 | 15 | Mix of large and small numbers |

## Edge Cases

For a strictly ascending array like `[1, 2]`, the algorithm correctly computes `1 XOR 2 = 3`. The stack initially has 1, then 2 is compared with 1, producing the correct lucky number before being pushed.

For a strictly descending array `[3, 2, 1]`, the stack ensures each number is compared with its immediate left neighbor. `3 XOR 2 = 1 XOR`
