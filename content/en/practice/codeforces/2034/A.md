---
title: "CF 2034A - King Keykhosrow's Mystery"
description: "The problem asks us to find a number that satisfies two properties relative to two given numbers, $a$ and $b$. Specifically, we want the smallest integer $m$ such that $m$ is at least as large as one of the two numbers and the remainder of $m$ when divided by $a$ equals the…"
date: "2026-06-08T11:32:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2034
codeforces_index: "A"
codeforces_contest_name: "Rayan Programming Contest 2024 - Selection (Codeforces Round 989, Div. 1 + Div. 2)"
rating: 800
weight: 2034
solve_time_s: 80
verified: true
draft: false
---

[CF 2034A - King Keykhosrow's Mystery](https://codeforces.com/problemset/problem/2034/A)

**Rating:** 800  
**Tags:** brute force, chinese remainder theorem, math, number theory  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to find a number that satisfies two properties relative to two given numbers, $a$ and $b$. Specifically, we want the smallest integer $m$ such that $m$ is at least as large as one of the two numbers and the remainder of $m$ when divided by $a$ equals the remainder when divided by $b$. In other words, if you imagine counting in steps of $a$ and $b$ starting from zero, $m$ is the first number where the two sequences "align" in their remainders.

The input consists of several test cases, each providing $a$ and $b$. Both values are bounded up to 1000, and the number of test cases is at most 100. Because $a$ and $b$ are relatively small, we can consider approaches that involve iterating or computing multiples without exceeding time limits.

A subtle edge case occurs when $a = b$. Any number greater than or equal to $a$ automatically satisfies the remainder condition, so the minimal $m$ is simply $a$ (or $b$). Another scenario is when $a$ and $b$ are coprime. The remainders will only match after their least common multiple, so the algorithm must handle numbers that are substantially larger than either input. A careless brute-force check might iterate unnecessarily over every integer and could miss that the first valid number is exactly the least common multiple (LCM).

## Approaches

A brute-force approach would start at $\max(a, b)$ and increment $m$ until $m \bmod a = m \bmod b$. This works because it directly implements the problem's condition, but its performance degrades for large inputs. For instance, if $a = 999$ and $b = 1000$, the first number that satisfies the remainder condition is $999 \cdot 1000 = 999000$. Iterating through nearly a million numbers for each test case is feasible here but inefficient and would be slow in larger bounds.

The key insight comes from rewriting the condition $m \bmod a = m \bmod b$. This is equivalent to saying $m$ leaves the same remainder modulo the greatest common divisor of $a$ and $b$. More concretely, if we let $d = \gcd(a, b)$, then the numbers $m$ that satisfy the remainder equality are precisely those of the form $m = k \cdot \mathrm{lcm}(a, b)$ for some integer $k \ge 1$. The smallest such $m$ that is at least $\max(a, b)$ is exactly the least common multiple of $a$ and $b$.

Thus, the optimal approach is to compute the LCM of $a$ and $b$ for each test case and return it. This uses standard number theory: $\mathrm{lcm}(a, b) = \frac{a \cdot b}{\gcd(a, b)}$. This completely avoids iteration and works efficiently for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a*b) worst case | O(1) | Correct but slower in edge cases |
| Optimal (LCM via GCD) | O(log(min(a,b))) | O(1) | Fast and accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. This determines how many pairs of numbers we will process.
2. For each test case, read integers $a$ and $b$.
3. Compute the greatest common divisor $d = \gcd(a, b)$. This uses the Euclidean algorithm, which is efficient and takes $O(\log \min(a, b))$ steps.
4. Calculate the least common multiple using $\mathrm{lcm}(a, b) = a \cdot b // d$. This guarantees the smallest number that is divisible by both $a$ and $b$, which also satisfies $m \bmod a = m \bmod b$.
5. Print the computed LCM. This is the minimal $m$ that satisfies both conditions for the test case.

Why it works: any number $m$ with $m \bmod a = m \bmod b$ must be a multiple of $\mathrm{lcm}(a, b)$ because the remainders repeat every multiple of the LCM. Taking the first multiple ensures minimality, and since LCM is always greater than or equal to both $a$ and $b$, it meets the "at least one of $a, b$" condition. The Euclidean algorithm ensures the LCM is computed correctly and efficiently.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    lcm = a * b // math.gcd(a, b)
    print(lcm)
```

The code begins with fast input reading. For each test case, it parses the two numbers, computes their GCD using Python's built-in `math.gcd`, then computes the LCM via integer division to avoid floating point errors. Finally, it prints the result immediately. Handling of multiple test cases is straightforward and there are no off-by-one errors because LCM inherently satisfies the minimum condition.

## Worked Examples

Sample input:

```
4 6
472 896
```

| a | b | gcd(a,b) | lcm(a,b) | m (output) |
| --- | --- | --- | --- | --- |
| 4 | 6 | 2 | 12 | 12 |
| 472 | 896 | 16 | 52864 | 52864 |

In the first case, LCM(4,6) = 12, which is the first number where 12 % 4 = 12 % 6 = 0. For the second case, LCM(472, 896) = 52864, which satisfies the same remainder condition. This confirms that computing the LCM directly finds the minimal $m$ efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * log(min(a,b))) | Each GCD computation via Euclidean algorithm is logarithmic in the smaller of the two numbers. |
| Space | O(1) | Only a few variables are needed per test case; no large data structures. |

Given $t \le 100$ and $a, b \le 1000$, this algorithm executes at most a few thousand GCD steps, well within a 1-second time limit.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        lcm = a * b // math.gcd(a, b)
        output.append(str(lcm))
    return "\n".join(output)

# Provided samples
assert run("2\n4 6\n472 896\n") == "12\n52864", "Sample test cases"

# Custom cases
assert run("1\n1 1\n") == "1", "Minimum equal values"
assert run("1\n1000 1000\n") == "1000", "Maximum equal values"
assert run("1\n2 3\n") == "6", "Small coprime numbers"
assert run("1\n5 7\n") == "35", "Another coprime example"
assert run("1\n8 12\n") == "24", "Shared divisors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Minimal input, a = b |
| 1000 1000 | 1000 | Maximal equal inputs |
| 2 3 | 6 | Small coprime numbers |
| 5 7 | 35 | Coprime numbers |
| 8 12 | 24 | Numbers with shared divisors |

## Edge Cases

For the input `1 1`, GCD is 1, and LCM is 1. The algorithm correctly returns 1, which satisfies the remainder condition immediately.

For `1000 1000`, GCD = 1000, so LCM = 1000. This output is the first number satisfying both the minimality condition and the remainder equality.

For coprime numbers like `2 3`, the first alignment of remainders happens at 6, confirming that the LCM approach handles coprime numbers correctly.

For numbers with a common divisor, `8 12`, LCM = 24, which is indeed the smallest number greater than either input where the remainders are equal. Each of these traces demonstrates that the algorithm handles minimal, maximal, coprime, and shared-divisor inputs accurately.
