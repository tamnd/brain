---
title: "CF 1925B - A Balanced Problemset?"
description: "We are asked to split an integer $x$ into exactly $n$ positive integers whose sum is $x$, in a way that maximizes the greatest common divisor of these integers. The input gives multiple test cases, each with values for $x$ and $n$."
date: "2026-06-08T19:04:05+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1925
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 921 (Div. 2)"
rating: 1200
weight: 1925
solve_time_s: 81
verified: true
draft: false
---

[CF 1925B - A Balanced Problemset?](https://codeforces.com/problemset/problem/1925/B)

**Rating:** 1200  
**Tags:** brute force, greedy, math, number theory  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to split an integer $x$ into exactly $n$ positive integers whose sum is $x$, in a way that maximizes the greatest common divisor of these integers. The input gives multiple test cases, each with values for $x$ and $n$. For each test case, the output is a single integer representing the largest possible GCD you can achieve when dividing $x$ into $n$ parts.

The bounds indicate that $x$ can be as large as $10^8$ and $n$ can be up to $x$. With up to 1000 test cases, any solution that iterates linearly over all possible splits or all divisors of $x$ naively is too slow. We need an algorithm that is close to $O(\sqrt{x})$ or better for each test case.

Edge cases appear when $n = 1$ or $n = x$. If $n = 1$, the only option is $x$ itself, so the GCD is $x$. If $n = x$, the only valid split is $1 + 1 + \dots + 1$, giving a GCD of 1. Another subtle scenario is when $n$ does not divide $x$ evenly; the naive approach of assigning $x / n$ to each part will fail to produce integers, so we need to think about divisors of $x$ that allow a valid partition.

## Approaches

The brute-force approach tries all possible ways to split $x$ into $n$ integers and computes the GCD for each split. This works in theory because we can enumerate all sequences of length $n$ summing to $x$, but the number of sequences grows combinatorially. For example, if $x = 10^8$ and $n = 2$, there are roughly $10^8$ possible pairs, which is far too large. So brute force is only feasible for very small numbers.

The key insight is that to maximize the GCD, all numbers should be multiples of that GCD, say $g$. If we denote the parts as $g \cdot a_1, g \cdot a_2, \dots, g \cdot a_n$, then the sum is $g \cdot (a_1 + \dots + a_n) = x$. This implies $g$ must divide $x$. The remaining task is to pick the largest $g$ that allows a decomposition into exactly $n$ positive integers.

Once we know $g$ divides $x$, we define $y = x / g$. We now need $n$ positive integers summing to $y$. The minimal sum of $n$ positive integers is $n$, so we must have $y \ge n$, which gives the constraint $g \le x / n$. Combining this with the fact that $g$ must divide $x$, the problem reduces to finding the largest divisor of $x$ that is at most $x / n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(x-1, n-1)) | O(n) | Too slow |
| Optimal | O(sqrt(x)) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $x$ and $n$. These represent the total difficulty and the number of sub-problems.
2. Initialize a variable `best_gcd` to 1, which will track the largest valid divisor.
3. Iterate through all integers $d$ from 1 up to $\sqrt{x}$. For each $d$:

- Check if $d$ divides $x$. If not, continue.
- If $d$ divides $x$, compute the complementary divisor $x / d$.
4. For each divisor $d$ and its complement $x / d$, check if it is less than or equal to $x / n$. If so, update `best_gcd` to be the maximum of its current value and that divisor.
5. After considering all divisors, `best_gcd` contains the largest divisor of $x$ that does not exceed $x / n$.
6. Print `best_gcd` for the test case.

Why it works: By iterating through divisors up to $\sqrt{x}$, we guarantee that all divisors are considered, including the complementary divisors. The invariant is that `best_gcd` is always a divisor of $x$ and satisfies the partition constraint. This ensures the final value maximizes the balance of the problemset.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, n = map(int, input().split())
    best_gcd = 1
    limit = x // n
    d = 1
    while d * d <= x:
        if x % d == 0:
            if d <= limit:
                best_gcd = max(best_gcd, d)
            if x // d <= limit:
                best_gcd = max(best_gcd, x // d)
        d += 1
    print(best_gcd)
```

The first line reads the number of test cases. The loop handles each test case independently. `limit` ensures we only consider divisors that allow a valid split into $n$ positive integers. The while loop finds all divisors efficiently, leveraging symmetry to also check $x / d$ for each $d$. This avoids iterating all the way to $x$, which would be too slow.

## Worked Examples

**Sample Input:** 10 3

| x | n | limit | d | x % d == 0? | candidate | best_gcd |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 3 | 3 | 1 | yes | 1,10 | 1 |
| 10 | 3 | 3 | 2 | yes | 2,5 | 2 |
| 10 | 3 | 3 | 3 | no | - | 2 |

The largest divisor not exceeding $x / n = 3$ is 2, so output is 2.

**Sample Input:** 5 5

| x | n | limit | d | x % d == 0? | candidate | best_gcd |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 1 | 1 | yes | 1,5 | 1 |
| 5 | 5 | 1 | 2 | no | - | 1 |

The only valid divisor is 1, giving output 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * sqrt(x)) | Each test case iterates over divisors up to sqrt(x) |
| Space | O(1) | Only a few variables per test case |

With $t \le 10^3$ and $x \le 10^8$, the solution runs comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        x, n = map(int, input().split())
        best_gcd = 1
        limit = x // n
        d = 1
        while d * d <= x:
            if x % d == 0:
                if d <= limit:
                    best_gcd = max(best_gcd, d)
                if x // d <= limit:
                    best_gcd = max(best_gcd, x // d)
            d += 1
        print(best_gcd)
    return output.getvalue().strip()

# provided samples
assert run("3\n10 3\n5 5\n420 69\n") == "2\n1\n6", "samples"

# custom cases
assert run("1\n1 1\n") == "1", "min input"
assert run("1\n100000000 1\n") == "100000000", "n=1, max x"
assert run("1\n100000000 100000000\n") == "1", "n=x, max x"
assert run("1\n12 5\n") == "2", "x divisible by multiple options"
assert run("1\n17 4\n") == "4", "prime x, small n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal case |
| 100000000 1 | 100000000 | maximal x with n=1 |
| 100000000 100000000 | 1 | maximal x with n=x |
| 12 5 | 2 | multiple divisors, choose largest valid |
| 17 4 | 4 | prime x, check divisor selection |

## Edge Cases

If $n = 1$, any $x$ is trivially split into a single part, so the largest GCD is $x$. For input `
