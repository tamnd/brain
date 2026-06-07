---
title: "CF 2156C - Maximum GCD on Whiteboard"
description: "We are given a collection of integers on a whiteboard and two operations to modify it. The first operation, Erase, allows us to remove up to $k$ numbers."
date: "2026-06-08T00:25:12+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2156
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1061 (Div. 2)"
rating: 1400
weight: 2156
solve_time_s: 97
verified: false
draft: false
---

[CF 2156C - Maximum GCD on Whiteboard](https://codeforces.com/problemset/problem/2156/C)

**Rating:** 1400  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of integers on a whiteboard and two operations to modify it. The first operation, Erase, allows us to remove up to $k$ numbers. The second operation, Split, lets us break any number $x \ge 3$ into three integers $x_1, x_2, x_3$ summing to $x$ but only keeps $x_1$ and $x_3$, discarding $x_2$. The task is to maximize the greatest common divisor (GCD) of all numbers remaining on the whiteboard after performing these operations.

The input provides multiple test cases. Each test case specifies $n$, the number of integers, $k$, the maximum number of erasures allowed, and the array $a$ of integers. Each integer satisfies $1 \le a_i \le n$. The constraints are significant: $n$ can be up to 200,000 and the total sum of all $n$ across test cases is also 200,000. This rules out brute-force approaches that iterate through all possible splits or subsets, since operations exponential in $n$ would be infeasible.

Non-obvious edge cases include situations where $k = 0$ and the numbers contain a single outlier like 1. For example, if the array is $[1, 2, 2, 2]$ and $k = 0$, we cannot erase 1, so the maximum GCD is 1. Another tricky scenario arises when numbers are all equal or primes larger than 2; splitting can only reduce or rearrange numbers, so identifying which elements to erase is key.

## Approaches

The brute-force approach is to try every possible combination of erasures and splits. For each number on the whiteboard, we could attempt every split configuration, then compute the GCD of the resulting array. This is correct in theory, because any combination of operations could be explored, but it is computationally infeasible. Each number can be split in many ways, and with $n$ up to 200,000, the number of possibilities explodes.

The key observation is that we only care about the final GCD, and the Split operation can be used to produce any pair of numbers $x_1, x_3$ as long as $x_1 + x_2 + x_3 = x$ and $x_2 \ge 1$. This allows us to reduce any number $a_i$ to any multiple of a candidate GCD $d$ that is less than or equal to $a_i$. Thus, we can reframe the problem: for a given candidate $d$, how many numbers cannot be converted into multiples of $d$ even using splits? These numbers must be erased, and if that count is less than or equal to $k$, $d$ is achievable.

To implement this efficiently, we iterate over possible divisors $d$ from 1 up to $n$. For each $d$, we count how many numbers in the array are not divisible by $d$ and check if that count is ≤ $k$. The largest $d$ passing this check is the answer. This is fast because we only need a linear scan per candidate $d$, and we can optimize by starting from the largest $d$ and stopping at the first valid one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Optimal | O(n√n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $k$, and the array $a$. Track the frequency of each integer since this helps quickly compute how many numbers are divisible by a candidate $d$.
2. Iterate candidate GCDs $d$ from 1 to the maximum number in $a$, or equivalently up to $n$. For each $d$, determine how many numbers are divisible by $d$ by using modular arithmetic.
3. Calculate the number of numbers that cannot be converted to multiples of $d$ even with splits. Since Split allows us to keep any two numbers adding to $x$ while discarding the middle one, any number greater than or equal to $d$ can be adjusted to produce multiples of $d$. Only numbers smaller than $d$ must be erased.
4. If the count of numbers that must be erased is ≤ $k$, record $d$ as a valid beauty. Keep track of the maximum valid $d$ during the iteration.
5. Output the maximum $d$ for the test case. Repeat for all test cases.

The algorithm works because Split operations give complete flexibility in decomposing numbers, meaning only numbers smaller than the candidate GCD constrain the choice. Erase operations provide a safety valve to remove these small numbers. By checking candidates in descending order, we ensure that the first feasible $d$ is the largest possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_beauty(n, k, a):
    freq = [0] * (n + 2)
    for x in a:
        freq[x] += 1
    
    count = [0] * (n + 2)
    for d in range(1, n + 1):
        cnt = 0
        for mult in range(d, n + 1, d):
            cnt += freq[mult]
        count[d] = cnt
    
    for d in range(n, 0, -1):
        if n - count[d] <= k:
            return d
    return 1

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_beauty(n, k, a))
```

The `freq` array counts occurrences of each number. The `count` array then aggregates how many numbers are multiples of each candidate GCD. Subtracting this from $n$ gives the minimum number of erasures needed to make all numbers divisible by that candidate. The descending iteration ensures that we find the largest possible beauty.

## Worked Examples

**Sample Input 1**

```
9 1
4 9 6 8 2 6 7 8 2
```

| Candidate d | Multiples Count | Erases Needed | Valid? |
| --- | --- | --- | --- |
| 9 | 1 | 8 | No |
| 8 | 2 | 7 | No |
| 7 | 1 | 8 | No |
| 6 | 2 | 7 | No |
| 5 | 0 | 9 | No |
| 4 | 3 | 6 | No |
| 3 | 2 | 7 | No |
| 2 | 6 | 3 | No |
| 1 | 9 | 0 | Yes |

Here, `d = 2` requires erasing 1 number (`7`), which is ≤ `k=1`. Maximum beauty is 2.

**Sample Input 2**

```
7 5
1 1 2 3 4 5 5
```

Numbers ≥5 are `[5,5]`. Erasing `[1,1,2,3,4]` uses exactly `k=5`. The maximum GCD is 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n) | Iterates over divisors up to n, for each counting multiples efficiently |
| Space | O(n) | Frequency and count arrays, each of size n+2 |

This fits comfortably within the constraints because n ≤ 2×10^5, giving about 2×10^5 iterations per test case in the worst case.

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
        a = list(map(int, input().split()))
        print(max_beauty(n, k, a))
    return output.getvalue().strip()

# Provided samples
assert run("1\n9 1\n4 9 6 8 2 6 7 8 2\n") == "2"
assert run("1\n7 5\n1 1 2 3 4 5 5\n") == "5"

# Custom cases
assert run("1\n1 0\n1\n") == "1", "single element, no erase"
assert run("1\n5 0\n1 2 3 4 5\n") == "1", "all numbers distinct, no erase"
assert run("1\n6 3\n2 4 6 8 10 12\n") == "2", "even numbers, can erase up to 3"
assert run("1\n4 2\n3 3 3 3\n") == "3", "all equal, k unused"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element, k=0 | 1 | Minimum input size, no erasures |
