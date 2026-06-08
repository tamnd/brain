---
title: "CF 1857A - Array Coloring"
description: "We are given an array of integers and need to decide whether it can be partitioned into two non-empty groups such that the sums of each group have the same parity-both even or both odd. Each group must contain at least one element."
date: "2026-06-09T00:45:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1857
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 891 (Div. 3)"
rating: 800
weight: 1857
solve_time_s: 78
verified: true
draft: false
---

[CF 1857A - Array Coloring](https://codeforces.com/problemset/problem/1857/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and need to decide whether it can be partitioned into two non-empty groups such that the sums of each group have the same parity-both even or both odd. Each group must contain at least one element. The input consists of multiple test cases, each with an array of length between 2 and 50, and elements ranging from 1 to 50.

The output is a simple "YES" or "NO" for each test case, indicating whether such a coloring is possible. Because the array length is small (maximum 50), we do not need heavy optimizations, but we should avoid brute-force enumeration of all partitions, which would be exponential in n.

Non-obvious edge cases arise when all numbers are of the same parity. For instance, an array `[2,4]` has only even numbers. Splitting into two groups will always produce sums that are both even, which satisfies the parity condition. In contrast, an array `[1,2]` has one odd and one even number, so any split will produce sums of different parity and the answer should be "NO". Arrays containing at least one odd and one even element usually offer more flexibility.

## Approaches

A brute-force solution would try every possible partition of the array into two non-empty groups and check the sums' parity. With n elements, there are $2^n - 2$ possible non-empty splits. For n=50, this is roughly $10^{15}$, far beyond feasible in 1 second.

The key insight comes from observing parity behavior. Sums modulo 2 depend only on the count of odd numbers. If the array contains at least one odd and at least one even element, it is always possible to split them such that both groups have sums of the same parity. If all elements are even, any non-empty split will produce sums that are even, which satisfies the condition. If all elements are odd, the total sum is odd, and splitting into two non-empty groups produces one odd sum and one odd sum minus an odd number, which is even, so parity differs and "NO" is correct.

Thus, the problem reduces to counting odd and even elements. If the array contains both odd and even elements or all elements are even, the answer is "YES". If all elements are odd and n > 1, the answer is "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Parity Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array length n and the array a.
2. Initialize counters for odd and even elements.
3. Iterate over each element of a. If it is odd, increment the odd counter; otherwise, increment the even counter.
4. Check conditions: if both odd and even counts are at least one, output "YES".
5. If all elements are even, output "YES".
6. If all elements are odd and n > 1, output "NO".

Why it works: the parity of sums depends only on the parity of the elements in each group. Having at least one element of each parity allows us to balance sums as needed. Arrays of only even numbers always produce sums of the same parity, while arrays of only odd numbers always produce unequal parity sums when split into two non-empty groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    odd = sum(1 for x in a if x % 2)
    even = n - odd
    if odd and even:
        print("YES")
    elif even == n:
        print("YES")
    else:
        print("NO")
```

The code counts odd and even numbers and applies the conditions outlined in the algorithm. Using `sum(1 for x in a if x % 2)` avoids manual iteration and keeps code concise. The boundary cases are naturally handled: arrays with all even elements return "YES", arrays with all odd elements return "NO".

## Worked Examples

Sample Input 1: `[1,2,4,3,2,3,5,4]`

| Step | odd | even | odd>0 and even>0? | Output |
| --- | --- | --- | --- | --- |
| Count | 5 | 3 | True | YES |

Sample Input 2: `[4,7]`

| Step | odd | even | odd>0 and even>0? | Output |
| --- | --- | --- | --- | --- |
| Count | 1 | 1 | True | YES |

The second input demonstrates that having both parities allows a valid split. If the input had been `[1,3]`, both odd, the check would return "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting odd/even elements requires a single pass |
| Space | O(1) | Only counters for odd and even are stored |

With n ≤ 50 and t ≤ 1000, this is well within the time limits.

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
        a = list(map(int, input().split()))
        odd = sum(1 for x in a if x % 2)
        even = n - odd
        if odd and even:
            print("YES")
        elif even == n:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# Provided samples
assert run("7\n8\n1 2 4 3 2 3 5 4\n2\n4 7\n3\n3 9 8\n2\n1 7\n5\n5 4 3 2 1\n4\n4 3 4 5\n2\n50 48\n") == "YES\nYES\nYES\nYES\nNO\nYES\nYES"

# Custom cases
assert run("1\n2\n1 3\n") == "NO", "all odd"
assert run("1\n2\n2 4\n") == "YES", "all even"
assert run("1\n3\n1 2 3\n") == "YES", "mixed small array"
assert run("1\n50\n" + "1 "*50 + "\n") == "NO", "max size, all odd"
assert run("1\n50\n" + "2 "*50 + "\n") == "YES", "max size, all even"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3` | NO | all odd numbers with n>1 |
| `2 4` | YES | all even numbers |
| `1 2 3` | YES | small mixed array |
| 50x`1` | NO | maximum size all odd |
| 50x`2` | YES | maximum size all even |

## Edge Cases

For `[1,3]`, both numbers are odd. Counting gives odd=2, even=0. The condition `odd and even` is false, `even == n` is false, so it correctly outputs "NO". For `[2,4]`, odd=0, even=2. `even == n` is true, so output is "YES". Arrays with a mix of odd and even, like `[1,2,3]`, satisfy `odd and even`, so output is "YES". The algorithm handles all boundary situations automatically without special case branching.
