---
title: "CF 1612D - X-Magic Pair"
description: "We are given a pair of integers $a$ and $b$, and another integer $x$. We are allowed to repeatedly replace either $a$ or $b$ with the absolute difference $ The constraints allow $a, b, x$ to go up to $10^{18}$, and there can be up to $10^4$ test cases."
date: "2026-06-10T06:58:23+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1612
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 117 (Rated for Div. 2)"
rating: 1600
weight: 1612
solve_time_s: 67
verified: true
draft: false
---

[CF 1612D - X-Magic Pair](https://codeforces.com/problemset/problem/1612/D)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pair of integers $a$ and $b$, and another integer $x$. We are allowed to repeatedly replace either $a$ or $b$ with the absolute difference $|a - b|$. The task is to determine whether it is possible, after some number of these operations, for either $a$ or $b$ to equal $x$. We have multiple independent test cases, each with their own $a, b, x$.

The constraints allow $a, b, x$ to go up to $10^{18}$, and there can be up to $10^4$ test cases. This makes any approach that simulates all operations explicitly infeasible, because the number of steps could be extremely large. We need an approach that works directly with the numeric properties of $a$ and $b$, rather than generating all possible sequences of operations.

A key non-obvious edge case arises when $a = b$. Here, $|a-b| = 0$, so any subsequent operations will never produce a number other than the current pair and zero. For example, if $a = b = 30$ and $x = 30$, the answer is YES, but if $x = 15$, it would be NO, because the pair can only reach 0, not 15.

Another subtle case is when $x$ is larger than either $a$ or $b$. For example, $a = 40, b = 50, x = 90$. The operations can only reduce numbers, so if $x > \max(a, b)$, the answer is immediately NO. Recognizing these constraints early prevents unnecessary computation.

## Approaches

The brute-force solution is straightforward: repeatedly apply both operations in all possible ways, tracking every new pair generated until either $x$ is found or the sequence stabilizes. This is correct because the problem allows arbitrary sequences of the two operations. The problem with this approach is that for large $a, b$ the number of distinct pairs that can be generated is enormous, potentially up to $10^{18}$, which is completely infeasible.

The key insight for an optimal solution comes from observing that the operations mimic the Euclidean algorithm for computing the greatest common divisor. Every time we replace one number with $|a-b|$, we are moving toward a smaller pair whose difference is a linear combination of the original $a$ and $b$. Concretely, any number reachable through these operations must satisfy $x \le \max(a, b)$ and $x \equiv a \pmod{\gcd(a, b)}$. This is because the Euclidean algorithm guarantees that the sequence of numbers produced by repeatedly applying $|a-b|$ will eventually produce all multiples of $\gcd(a, b)$ that are less than or equal to $\max(a, b)$.

So instead of simulating operations, we can directly check two conditions: $x \le \max(a, b)$ and $x \% \gcd(a, b) == a \% \gcd(a, b)$. If both hold, the pair is $x$-magic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(large, potentially exponential) | O(large) | Too slow |
| Optimal | O(log(max(a,b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read integers $a, b, x$.
3. Compute $g = \gcd(a, b)$. This captures the step size of all numbers reachable through the operations. Any reachable number must be congruent to $a$ modulo $g$.
4. Check if $x \le \max(a, b)$. If not, the operations cannot reach a larger number, so print NO and continue.
5. Check if $x \equiv a \pmod{g}$. If true, $x$ is reachable; otherwise, it is not. Print YES or NO accordingly.

Why it works: The Euclidean-like operations preserve the greatest common divisor of the pair, and the maximum never increases. Therefore, any number $x$ that is reachable must be less than or equal to the current maximum and must be congruent to the original numbers modulo the GCD. These two simple checks completely capture the set of reachable numbers.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, x = map(int, input().split())
    g = math.gcd(a, b)
    if x <= max(a, b) and (x % g == a % g):
        print("YES")
    else:
        print("NO")
```

The code first reads all test cases. The key computation is the `math.gcd(a, b)`, which allows us to directly check the modular condition instead of simulating operations. Checking `x <= max(a, b)` ensures we never attempt to reach a number larger than the current pair, and `x % g == a % g` guarantees reachability via the Euclidean pattern.

## Worked Examples

**Example 1:** $a=6, b=9, x=3$

| a | b | g | max(a,b) | x <= max | x % g | a % g | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 9 | 3 | 9 | True | 0 | 0 | YES |

The GCD is 3. 3 ≤ 9 and 3 ≡ 6 mod 3, so YES.

**Example 2:** $a=40, b=50, x=90$

| a | b | g | max(a,b) | x <= max | x % g | a % g | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 40 | 50 | 10 | 50 | False | 0 | 0 | NO |

x > max(a,b), so the pair cannot reach x.

These examples demonstrate that the algorithm correctly identifies reachable numbers by the two conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log(max(a,b))) | Each GCD computation takes O(log(max(a,b))), repeated for t test cases. |
| Space | O(1) | Only a few variables are stored per test case. |

Given $t \le 10^4$ and $a, b \le 10^{18}$, this approach is well within the 2-second time limit.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b, x = map(int, input().split())
        g = gcd(a, b)
        if x <= max(a, b) and (x % g == a % g):
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("8\n6 9 3\n15 38 7\n18 8 8\n30 30 30\n40 50 90\n24 28 20\n365 216 52\n537037812705867558 338887693834423551 3199921013340") == "YES\nYES\nYES\nYES\nNO\nYES\nYES\nYES"

# custom cases
assert run("3\n1 1 1\n1 1 2\n1000000000000000000 1000000000000000000 0") == "YES\nNO\nYES", "edge cases"
assert run("2\n10 6 4\n10 6 5") == "YES\nNO", "mod gcd test"
assert run("1\n7 14 7") == "YES", "simple gcd multiple"
assert run("1\n7 14 8") == "NO", "simple gcd failure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1; 1 1 2; 10^18 10^18 0 | YES; NO; YES | minimum size, unreachable x, max edge |
| 10 6 4; 10 6 5 | YES; NO | reachable by gcd pattern, fails modulo check |
| 7 14 7 | YES | simple gcd divisible case |
| 7 14 8 | NO | simple gcd not divisible case |

## Edge Cases

If $a = b = x$, the algorithm correctly returns YES because `x <= max(a,b)` and `x % g == a % g` trivially hold. For $x > \max(a, b)$, it correctly returns NO immediately. When the numbers are extremely large, GCD computations handle them efficiently, and modular arithmetic guarantees correctness without overflow.
