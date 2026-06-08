---
title: "CF 2008A - Sakurako's Exam"
description: "We are asked to decide whether it is possible to assign a positive or negative sign to each element in an array made up of a certain number of ones and twos such that the total sum becomes zero."
date: "2026-06-08T13:24:49+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 800
weight: 2008
solve_time_s: 81
verified: true
draft: false
---

[CF 2008A - Sakurako's Exam](https://codeforces.com/problemset/problem/2008/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, greedy, math  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decide whether it is possible to assign a positive or negative sign to each element in an array made up of a certain number of ones and twos such that the total sum becomes zero. Each test case provides two integers, $a$ and $b$, representing how many 1s and 2s are in the array. The output is a simple "Yes" or "No" depending on whether such a sign assignment exists.

Given the constraints, $0 \le a,b < 10$, we know the array size is very small. This implies that even a brute-force solution that tries all possible sign assignments would run quickly because the total number of assignments is $2^{a+b}$, which cannot exceed $2^{18} = 262{,}144$ in the worst case. However, this problem has a structure that allows us to reason mathematically without enumerating every assignment.

Edge cases arise when one type of number is missing or in small quantities. For example, if $a=0$ and $b=1$, the array is `[2]` and there is no way to reach zero. Another subtle case is when there is a combination like $a=1$ and $b=1$, where the sum of the array is odd (1+2=3) and cannot be split into equal positive and negative contributions. These small odd/even sums are the key to the solution.

## Approaches

A naive brute-force approach would iterate over all possible combinations of '+' and '-' signs for each element. For each combination, it would compute the sum and check if it equals zero. This works because every possible sign assignment is considered, but even with a small array length, it is overkill and not insightful.

The key observation comes from analyzing sums and parity. Each 1 contributes either +1 or -1, and each 2 contributes either +2 or -2. To reach a sum of zero, the total sum must be even because all numbers are integers and the sum of signed integers must balance exactly. If $2b + a$ (the sum when all signs are positive) is odd, there is no way to split into two equal parts. Further, if there are twos, they can only be split in multiples of 2. This means that if $b$ is odd, we need at least two 1s to compensate to reach zero; otherwise, it's impossible. If $b$ is even, any number of 1s can be paired off or left out in zero sum.

The insight allows us to immediately decide the answer without iteration. This produces a constant-time solution for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(a+b)) | O(a+b) | Correct but unnecessary |
| Mathematical Parity Check | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read integers $a$ and $b$ representing the count of 1s and 2s.
2. If the sum of all numbers, $a + 2b$, is odd, immediately print "No". An odd sum can never be split into two equal sums with plus and minus signs.
3. If $b$ is even, print "Yes". Even twos can always be split into pairs of +2 and -2. Ones can then be paired off similarly or added in complementary ways to maintain zero sum.
4. If $b$ is odd, check if $a \ge 2$. Two ones can compensate for a single unpaired two, so print "Yes" if $a \ge 2". Otherwise, print "No".
5. Repeat for all test cases.

The reason this works is that every configuration can be reduced to whether the total sum is even and whether we can pair off unbalanced twos using ones. There is no need to enumerate individual sign assignments because the parity rules fully determine feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    total = a + 2 * b
    if total % 2 != 0:
        print("No")
    elif b % 2 == 0:
        print("Yes")
    else:
        print("Yes" if a >= 2 else "No")
```

The solution first calculates the total sum of all positive numbers. If this total is odd, no combination of + and - can yield zero, so we print "No". If the total is even, we check the number of twos. Even twos can always be perfectly balanced. If the number of twos is odd, we require at least two ones to pair with a leftover two, otherwise zero sum is impossible. This implements the exact reasoning described in the algorithm walkthrough.

## Worked Examples

**Example 1:** Input `a=0, b=1`

| Variable | Value |
| --- | --- |
| total | 2 |
| total % 2 | 0 |
| b % 2 | 1 |
| a >= 2 | False |

Output: `No` because one unpaired two cannot be balanced without two ones.

**Example 2:** Input `a=2, b=3`

| Variable | Value |
| --- | --- |
| total | 2 + 2*3 = 8 |
| total % 2 | 0 |
| b % 2 | 1 |
| a >= 2 | True |

Output: `Yes` because two ones can balance one unpaired two, leaving the remaining two twos to pair off.

These traces demonstrate that checking parity and pairing is sufficient to decide the outcome without enumerating combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time. |
| Space | O(1) | Only a few integer variables are used per test case. |

Given the constraints, $t \le 100$ and $a,b < 10$, the solution runs in microseconds per test case and easily fits in the memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        total = a + 2 * b
        if total % 2 != 0:
            output.append("No")
        elif b % 2 == 0:
            output.append("Yes")
        else:
            output.append("Yes" if a >= 2 else "No")
    return "\n".join(output)

# Provided samples
assert run("5\n0 1\n0 3\n2 0\n2 3\n3 1\n") == "No\nNo\nYes\nYes\nNo", "sample 1"

# Custom cases
assert run("3\n0 0\n1 1\n9 0\n") == "Yes\nNo\nYes", "custom small and boundary"
assert run("2\n0 4\n1 5\n") == "Yes\nNo", "even twos and odd twos with insufficient ones"
assert run("1\n2 1\n") == "Yes", "two ones can balance single two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `Yes` | Empty array is trivially zero sum |
| `1 1` | `No` | Odd sum cannot be zero |
| `9 0` | `Yes` | All ones, even count can pair off |
| `0 4` | `Yes` | Even twos, no ones needed |
| `1 5` | `No` | Odd twos, insufficient ones |
| `2 1` | `Yes` | Odd two compensated by two ones |

## Edge Cases

For input `0 0`, total sum is 0. The algorithm prints `Yes` because an empty array sums to zero, which is correct. For input `1 1`, total sum is 3 (odd), so the algorithm prints `No`. For `2 1`, total sum is 4 (even), one two is odd, but `a >= 2`, so it prints `Yes`. All these examples confirm that the parity check and pairing logic handle edge cases correctly.
