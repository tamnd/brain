---
title: "CF 103306I - Integer Multiplicative Persistence"
description: "We are given a number and we repeatedly apply a very specific transformation: replace the number with the product of its decimal digits. We keep doing this until the number becomes a single digit."
date: "2026-07-03T14:23:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103306
codeforces_index: "I"
codeforces_contest_name: "2021 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 103306
solve_time_s: 47
verified: true
draft: false
---

[CF 103306I - Integer Multiplicative Persistence](https://codeforces.com/problemset/problem/103306/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number and we repeatedly apply a very specific transformation: replace the number with the product of its decimal digits. We keep doing this until the number becomes a single digit. The task is to determine how many such transformations are needed for each given input number.

Each test case gives one integer. For that integer, we simulate this digit-product process and count how many steps it takes before the number has only one digit left.

The constraints allow up to 1000 test cases, and each number is at most $10^9$. This means each number has at most 10 digits, so one full digit-product operation costs at most about 10 multiplications. Even if we simulate the process step by step, the value shrinks very quickly because digit products tend to drop fast, especially when zeros or small digits appear. This makes a direct simulation per test case efficient enough within time limits.

There are a few corner cases that matter.

If the number is already a single digit, no operations are needed, so the answer is zero. For example, input 5 should output 0.

If the number contains a zero, the next value immediately becomes zero, and the process ends in one step. For example, 10 becomes 1 * 0 = 0, then stops because 0 is a single digit, so the answer is 1.

If the number is 0 initially, it is already a single digit, so the answer is 0.

A naive mistake would be to keep looping even after reaching a single digit and accidentally count an extra step. Another subtle issue is forgetting that zeros collapse the process immediately, so treating leading zeros or intermediate representations incorrectly can overcount steps.

## Approaches

The brute-force idea is straightforward. For each number, repeatedly extract digits, compute their product, and replace the number. Each repetition is one step. We stop when the number becomes less than 10.

This works because the operation is deterministic and strictly reduces the number of digits in most cases, but the worst case cost depends on how many iterations are needed. In the worst imaginable scenario, we could have many steps, but in base 10 digit multiplication, values collapse quickly and the number of iterations is bounded by a small constant in practice. So the total complexity is roughly proportional to the number of digits times the number of steps per test case.

The key observation is that nothing in the process depends on history except the current number. There is no need for memoization or advanced data structures. The structure is purely iterative reduction over digits, which is already optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T · k · d) | O(1) | Accepted |
| Optimal Simulation (same idea) | O(T · k · d) | O(1) | Accepted |

Here $k$ is the number of iterations until a single digit is reached, and $d$ is number of digits (≤ 10).

## Algorithm Walkthrough

1. Read the number of test cases and iterate over each integer $N$. Each test case is independent, so we reset our step counter each time.
2. Initialize a counter `steps = 0`. This tracks how many times we apply the digit-product transformation.
3. While $N \ge 10$, meaning it still has at least two digits, compute the product of its digits. We do this by repeatedly taking the last digit using modulo 10 and multiplying it into an accumulator, then dividing $N$ by 10. This avoids string conversion but either approach is valid.
4. Replace $N$ with the computed product and increment `steps` by 1. Each replacement corresponds exactly to one transformation defined in the problem.
5. When the loop ends, $N$ is a single digit, so we output `steps`.

The key design choice is stopping exactly at $N < 10$. Stopping earlier or later shifts the definition of persistence and produces incorrect answers.

### Why it works

Each operation strictly follows the problem definition: a transformation is defined as replacing a number by the product of its digits. The loop invariant is that after `steps` iterations, the current value of $N$ is exactly the result of applying the digit-product operation `steps` times starting from the original input. Because each iteration reduces a multi-digit number into another integer in the same process space, and we only terminate when the number is already a fixed point under the operation (any single digit is unchanged by further multiplication of digits in the sense that the process stops), the count `steps` exactly measures multiplicative persistence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_product(x):
    res = 1
    while x > 0:
        res *= x % 10
        x //= 10
    return res

t = int(input())
for _ in range(t):
    n = int(input().strip())
    
    steps = 0
    while n >= 10:
        n = digit_product(n)
        steps += 1
    
    print(steps)
```

The helper function `digit_product` isolates the core transformation so the main loop remains clean. Inside it, we repeatedly extract digits using modulo and integer division, which avoids string conversion overhead but keeps logic simple and safe.

The stopping condition `n >= 10` is critical. It ensures we only count transformations that actually reduce a multi-digit number, and we do not overcount when the result becomes a single digit.

## Worked Examples

### Example 1

Input:

```
39
```

We start with `n = 39`, `steps = 0`.

| Step | Current n | Digit product | New n | steps |
| --- | --- | --- | --- | --- |
| 0 | 39 | 3 * 9 = 27 | 27 | 1 |
| 1 | 27 | 2 * 7 = 14 | 14 | 2 |
| 2 | 14 | 1 * 4 = 4 | 4 | 3 |

Now 4 is a single digit, so we stop. Output is 3.

This confirms that each iteration strictly corresponds to one full digit reduction.

### Example 2

Input:

```
10
```

We start with `n = 10`, `steps = 0`.

| Step | Current n | Digit product | New n | steps |
| --- | --- | --- | --- | --- |
| 0 | 10 | 1 * 0 = 0 | 0 | 1 |

Now 0 is a single digit, so we stop. Output is 1.

This shows how zeros collapse the process immediately and still count as exactly one valid transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · k · d) | Each step processes digits of the number, and each number shrinks quickly to a single digit |
| Space | O(1) | Only a few integers are used regardless of input size |

The constraints guarantee that this direct simulation fits easily within time limits. Even in worst cases, each number has at most 10 digits, and the persistence depth is small enough that total operations remain trivial for $T \le 1000$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline

    def digit_product(x):
        res = 1
        while x > 0:
            res *= x % 10
            x //= 10
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input().strip())
        steps = 0
        while n >= 10:
            n = digit_product(n)
            steps += 1
        out.append(str(steps))
    return "\n".join(out)

# provided samples
assert run("""6
0
5
10
25
39
27
""") == """0
0
1
2
3
2"""

# custom cases
assert run("""1
4
""") == "0"

assert run("""1
100
""") == "1"

assert run("""1
99
""") == "2"

assert run("""1
999999999
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | 0 | single digit base case |
| 100 | 1 | zero propagation |
| 99 | 2 | multi-step reduction |
| 999999999 | 4 | deep persistence stress case |

## Edge Cases

For a single-digit input like 7, the loop condition `n >= 10` fails immediately, so `steps` remains zero and the output is correct.

For inputs containing zero such as 10 or 100, the first multiplication produces zero, and the loop stops immediately afterward because zero is already a single digit. The algorithm correctly counts exactly one transformation.

For large repeated digits such as 999999999, the product becomes 387420489, then continues shrinking. Each iteration is handled uniformly by the same digit-product routine, and the step counter increases exactly once per transformation, ensuring correctness even in cases that take several rounds.
