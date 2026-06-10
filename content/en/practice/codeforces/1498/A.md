---
title: "CF 1498A - GCD Sum"
description: "The problem asks us to find, for a given integer $n$, the smallest integer $x$ greater than or equal to $n$ such that the greatest common divisor of $x$ and the sum of its digits is greater than one."
date: "2026-06-10T21:35:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1498
codeforces_index: "A"
codeforces_contest_name: "CodeCraft-21 and Codeforces Round 711 (Div. 2)"
rating: 800
weight: 1498
solve_time_s: 123
verified: true
draft: false
---

[CF 1498A - GCD Sum](https://codeforces.com/problemset/problem/1498/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to find, for a given integer $n$, the smallest integer $x$ greater than or equal to $n$ such that the greatest common divisor of $x$ and the sum of its digits is greater than one. In other words, we want $x \ge n$ with $gcd(x, s(x)) > 1$, where $s(x)$ is the sum of digits of $x$. The input consists of multiple test cases, each giving a single number $n$, and the output is one integer per test case satisfying this condition.

The constraints allow $n$ up to $10^{18}$ and up to $10^4$ test cases. A naive approach that iterates from $n$ upward and computes $gcd(x, s(x))$ for each candidate could be feasible if each check is extremely fast. Since $10^{18}$ is massive, we cannot afford any solution that scans linearly over a large range of numbers in the worst case. Each check involves computing the sum of digits and then a gcd, both of which are fast for a single number.

Edge cases include numbers where $n$ itself already satisfies the condition, numbers where the sum of digits is a prime, or numbers just below a "good" candidate. For example, if $n = 75$, the gcd of 75 and 12 is 3, so the answer is 75 itself. If $n = 11$, $gcd(11,2) = 1$, so we need to move to 12, where $gcd(12,3) = 3$. Careless implementation might skip the check for $n$ itself and always increment first, producing the wrong answer.

## Approaches

A brute-force approach is straightforward: starting from $n$, compute the sum of digits, calculate the gcd with the number, and check if it is greater than 1. If not, increment the number and repeat. This works because each number is independent, and gcd computation is very fast. However, in the worst case, we may need to check many consecutive numbers before finding a valid $x$. Given the constraints, we could be unlucky with a few numbers, but practically the sum of digits is at most 162 (for 18-digit numbers), so a number almost always has a gcd greater than 1 with its digit sum within a few steps. This allows a simple linear scan in practice.

The key insight that makes the problem tractable is that the gcd condition is rarely violated for consecutive numbers. The sum of digits changes slowly, and many numbers share common divisors with their digit sum. Therefore, simply incrementing $n$ until the condition is satisfied is both correct and efficient given the problem limits. There is no need for a complicated mathematical formula or precomputation because the linear scan requires only a few iterations for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Linear Scan | O(18 * t) per test case | O(1) | Accepted |
| Optimal | O(18 * t) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the integer $n$.
3. Initialize $x = n$ as the candidate number.
4. Repeat the following steps until a valid $x$ is found:

1. Compute the sum of digits of $x$. This is done by converting $x$ to a string and summing the integer values of each character.
2. Compute $gcd(x, \text{sum of digits})$. Python's built-in `math.gcd` function handles this efficiently.
3. If the gcd is greater than 1, output $x$ and stop the loop for this test case.
4. Otherwise, increment $x$ by 1 and continue the loop.
5. Move to the next test case.

Why it works: The loop invariant is that for each number checked, either it satisfies the gcd condition or we increment to the next integer. Because integers are discrete and strictly increasing, the first number where `gcd(x, s(x)) > 1` is guaranteed to be minimal. The algorithm always considers the input $n$ itself, so it does not skip valid solutions.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    x = n
    while True:
        s = sum(int(d) for d in str(x))
        if math.gcd(x, s) > 1:
            print(x)
            break
        x += 1
```

The code first reads the number of test cases. For each test case, it reads $n$ and starts checking from $x = n$. The sum of digits is computed using a generator expression iterating over the string representation of the number. The `math.gcd` function efficiently computes the gcd of two numbers. If the condition is met, we print $x$ and stop. Otherwise, we increment $x$ and continue. The loop is guaranteed to terminate because a valid $x$ always exists and is quickly found.

## Worked Examples

### Sample 1 Trace

Input: 11

| x | sum_digits(x) | gcd(x, sum_digits) | Action |
| --- | --- | --- | --- |
| 11 | 2 | 1 | increment |
| 12 | 3 | 3 | print 12 |

Input: 31

| x | sum_digits(x) | gcd(x, sum_digits) | Action |
| --- | --- | --- | --- |
| 31 | 4 | 1 | increment |
| 32 | 5 | 1 | increment |
| 33 | 6 | 3 | print 33 |

These traces show that the loop quickly finds the minimal $x$ satisfying the gcd condition, often in 1 to 3 iterations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * L) | Each test case increments at most a few times; L is the number of digits in n (≤18), because sum of digits computation is O(L) and gcd computation is negligible. |
| Space | O(1) | Only a few integer variables and loop counters are used, independent of input size. |

Given the constraints $t \le 10^4$ and $n \le 10^{18}$, the solution fits comfortably within the 1-second limit. Python handles large integers efficiently for these operations.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        x = n
        while True:
            s = sum(int(d) for d in str(x))
            if math.gcd(x, s) > 1:
                print(x)
                break
            x += 1
    return output.getvalue().strip()

# provided samples
assert run("3\n11\n31\n75\n") == "12\n33\n75", "sample 1"

# custom cases
assert run("2\n1\n2\n") == "2\n2", "minimum values"
assert run("1\n10\n") == "12", "edge just below solution"
assert run("1\n99\n") == "99", "sum of digits gcd already >1"
assert run("1\n1000000000000000000\n") == "1000000000000000002", "large n case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 2 | 2, 2 | Minimum inputs |
| 10 | 12 | Off-by-one increment handling |
| 99 | 99 | Input itself satisfies gcd condition |
| 10^18 | 10^18 + 2 | Very large input, performance |

## Edge Cases

For the input `n = 1`, the algorithm checks `gcd(1,1) = 1`, increments to 2, and finds `gcd(2,2) = 2 > 1`. The output is correctly 2. For `n = 10^18`, the sum of digits is 1, `gcd(10^18,1) = 1`, increments to 10^18 + 1 (`gcd(10^18 + 1,1) = 1`), then 10^18 + 2, `gcd(10^18 + 2,2) = 2`, correctly producing 10^18 + 2. The algorithm handles boundaries and large values without overflow because Python integers are arbitrary precision. It also correctly identifies cases where the input itself satisfies the gcd condition, such as `n = 75`, immediately printing the input.
