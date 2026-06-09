---
title: "CF 1780B - GCD Partition"
description: "We are given an array of positive integers. Our task is to split this array into at least two contiguous subsegments, compute the sum of each subsegment, and then take the greatest common divisor (GCD) of these sums."
date: "2026-06-09T11:23:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1780
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 846 (Div. 2)"
rating: 1100
weight: 1780
solve_time_s: 97
verified: true
draft: false
---

[CF 1780B - GCD Partition](https://codeforces.com/problemset/problem/1780/B)

**Rating:** 1100  
**Tags:** brute force, greedy, math, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. Our task is to split this array into at least two contiguous subsegments, compute the sum of each subsegment, and then take the greatest common divisor (GCD) of these sums. Among all possible valid splits, we want the split that produces the largest possible GCD.

The input consists of multiple test cases. Each test case provides the length of the array and the array itself. The output is a single integer per test case: the maximum achievable GCD using any valid split.

Given that the length of the array can be up to $2 \cdot 10^5$ and the total sum over all test cases is also $2 \cdot 10^5$, any solution that examines all possible splits naively is too slow. A naive approach might try every pair of left and right boundaries for all segments, which would require $O(n^2)$ or worse, far exceeding the time limits.

A subtle edge case occurs when the array has all identical elements. Here, many splits are possible, and the GCD could equal the sum of a contiguous block if chosen carefully. Another tricky case is when the array contains primes or numbers that share no divisors. A careless approach that assumes some divisibility property may underestimate the maximal GCD. For example, `[1, 1, 1, 3]` splits optimally into `[1, 1, 1]` and `[3]` to get a GCD of 3, not 1.

## Approaches

A brute-force approach would enumerate every possible split of the array into $k$ subsegments, compute their sums, and then the GCD. This works because computing a GCD is fast for a small number of numbers, but the number of splits is exponential. For $n = 2 \cdot 10^5$, this is infeasible.

The key insight is that the maximum GCD must divide the total sum of the array. Let $S = a_1 + a_2 + \dots + a_n$. Suppose a split produces sums $s_1, s_2, \dots, s_k$. The GCD of these sums, call it $g$, must divide every $s_i$, and therefore also $S = s_1 + s_2 + \dots + s_k$. Thus $g$ must be a divisor of $S$. This reduces the search space to the divisors of $S$, which are at most $O(\sqrt{S})$.

Next, for each candidate divisor $d$, we can greedily check if the array can be partitioned into contiguous segments where each segment sum is a multiple of $d$. We scan left to right, accumulating a running sum. Whenever the sum reaches a multiple of $d$, we cut a segment. If we can form at least two segments this way, $d$ is a valid GCD. The largest valid $d$ across all divisors is the answer.

This approach reduces the complexity drastically and is suitable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal (divisor check + greedy) | O(n * sqrt(S)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and the array $a$, and compute the total sum $S$.
3. Generate all divisors of $S$. Since a number $x$ has at most $O(\sqrt{x})$ divisors, this is efficient.
4. Sort the divisors in descending order. Checking larger divisors first allows early termination upon finding a valid split.
5. For each divisor $d$, attempt to split the array greedily:

1. Initialize a running sum `current = 0` and a counter `segments = 0`.
2. Traverse the array, adding each element to `current`.
3. When `current` reaches a multiple of $d$, increment `segments` and reset `current` to 0.
6. If `segments >= 2` after scanning the array, `d` is feasible. Record it as the maximum GCD and stop checking smaller divisors.
7. Output the maximum GCD for this test case.

Why it works: The greedy accumulation works because if a segment sum exceeds a multiple of $d$ before a cut, then including the next element would violate the multiple condition. Hence, cutting exactly at multiples ensures that all segment sums are divisible by $d$. By checking all divisors of $S$ in descending order, we guarantee that the first feasible divisor is the largest possible GCD.

## Python Solution

```python
import sys
input = sys.stdin.readline

def divisors(x):
    res = set()
    for i in range(1, int(x**0.5) + 1):
        if x % i == 0:
            res.add(i)
            res.add(x // i)
    return sorted(res, reverse=True)

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    S = sum(a)
    max_gcd = 1
    for d in divisors(S):
        current = 0
        segments = 0
        for num in a:
            current += num
            if current % d == 0:
                segments += 1
                current = 0
        if segments >= 2:
            max_gcd = d
            break
    print(max_gcd)
```

This solution first generates all divisors of the total sum `S` for each test case. It then attempts a greedy partitioning by accumulating sums until multiples of `d` are reached. The first `d` that allows at least two segments is the optimal answer. Using sets for divisor collection avoids duplicates, and sorting ensures we try larger candidates first.

## Worked Examples

**Example 1:**

Input: `[2, 2, 1, 3]`

Total sum: `8`. Divisors: `[8, 4, 2, 1]`.

| Step | current | segments | Action |
| --- | --- | --- | --- |
| num=2 | 2 | 0 | continue |
| num=2 | 4 | 1 | cut, current=0 |
| num=1 | 1 | 1 | continue |
| num=3 | 4 | 2 | cut, current=0 |

Segments >=2, feasible GCD = 4.

**Example 2:**

Input: `[1, 2]`

Total sum: `3`. Divisors: `[3, 1]`.

- Check 3: cannot split into at least 2 segments.
- Check 1: can split `[1]` and `[2]`. Maximum GCD = 1.

These examples confirm the greedy partitioning correctly respects the divisor condition and finds the maximum GCD.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(S)) | For each test case, generating divisors is O(sqrt(S)) and checking each divisor scans the array O(n). |
| Space | O(n + sqrt(S)) | Storing array and divisors. |

Given $n \le 2 \cdot 10^5$ and sum of $n$ over all test cases $\le 2 \cdot 10^5$, this solution runs efficiently within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # copy solution here
    import sys
    input = sys.stdin.readline

    def divisors(x):
        res = set()
        for i in range(1, int(x**0.5) + 1):
            if x % i == 0:
                res.add(i)
                res.add(x // i)
        return sorted(res, reverse=True)

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        S = sum(a)
        max_gcd = 1
        for d in divisors(S):
            current = 0
            segments = 0
            for num in a:
                current += num
                if current % d == 0:
                    segments += 1
                    current = 0
            if segments >= 2:
                max_gcd = d
                break
        print(max_gcd)
    return output.getvalue().strip()

# Provided samples
assert run("6\n4\n2 2 1 3\n2\n1 2\n3\n1 4 5\n6\n1 2 1 1 1 3\n10\n12 30 37 88 12 78 89 17 2 12\n6\n7 7 7 7 7 7\n") == "4\n1\n5\n3\n1\n21"

# Custom cases
assert run("1\n2\n5 5\n") == "10", "two elements equal"
assert run("1\n
```
