---
title: "CF 104261B - Pluto Discovery!"
description: "We are given a single integer $n$, and we need to evaluate a specific summation built from division remainders. For every integer $i$ from 1 to $n$, we divide $n$ by $i$ and take the remainder, then add all those remainders together. The task is to compute this total efficiently."
date: "2026-07-01T21:40:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104261
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 2 (Beginner)"
rating: 0
weight: 104261
solve_time_s: 71
verified: true
draft: false
---

[CF 104261B - Pluto Discovery!](https://codeforces.com/problemset/problem/104261/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we need to evaluate a specific summation built from division remainders. For every integer $i$ from 1 to $n$, we divide $n$ by $i$ and take the remainder, then add all those remainders together. The task is to compute this total efficiently.

Formally, the required result is

$$\sum_{i=1}^{n} (n \bmod i)$$

The input size constraint $n \le 10^5$ already rules out any solution that recomputes a modulus inside a nested loop over large ranges per test case. A direct evaluation performs $n$ modulo operations, which is $O(n)$, and that is already acceptable here. Anything worse than linear, such as trying to simulate division behavior or recomputing remainders through repeated subtraction, would fail under time limits if scaled beyond this single loop structure.

The main subtlety is that although the formula looks like a straightforward loop, many naive interpretations try to expand or simplify it incorrectly, especially by attempting to group terms without understanding how $n \bmod i$ behaves for different ranges of $i$.

Edge cases are minimal but still worth checking.

For $n = 1$, the expression becomes $1 \bmod 1 = 0$, so the answer is 0. A common mistake is assuming the remainder is always positive or mistakenly starting the loop from 2, which would incorrectly produce no output.

For larger $n$, the remainder values vary significantly: for small divisors $i$, the remainder is $n - i \cdot \lfloor n/i \rfloor$, while for $i > n/2$, the quotient is 1 and the remainder simplifies to $n - i$. A careless attempt to optimize without respecting this structure may double-count or mis-handle transitions.

## Approaches

The brute-force approach directly follows the definition. For each $i$ from 1 to $n$, compute $n \bmod i$ and accumulate the result. This is correct because it evaluates the definition literally without transformation. The runtime is linear in $n$, with exactly $n$ modulo operations and additions.

Since $n \le 10^5$, this brute-force solution already fits comfortably within time limits. There is no need for advanced optimization techniques such as divisor grouping or harmonic series tricks, because the problem does not require processing multiple test cases or larger constraints.

The key insight is simply recognizing that the problem is already in its simplest computational form. The expression does not hide repeated structure that needs compression, and the modulus operation itself is constant time in Python.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input. This is the upper bound of the summation range.
2. Initialize an accumulator variable `ans` to 0. This will store the running total of all remainders.
3. Iterate $i$ from 1 to $n$, inclusive. Each value of $i$ represents a divisor candidate in the expression $n \bmod i$.
4. For each $i$, compute the remainder of dividing $n$ by $i$, then add it to `ans`. This directly matches the mathematical definition of the problem.
5. After the loop completes, output `ans`.

### Why it works

Each term in the sum is independent and defined purely by the pair $(n, i)$. The algorithm evaluates every valid $i$ exactly once, and each contribution $n \bmod i$ is computed exactly as defined. Since addition is associative and commutative over integers, accumulating these values in any order produces the same result as the mathematical sum. No approximation or transformation is introduced, so correctness follows directly from term-by-term evaluation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
ans = 0

for i in range(1, n + 1):
    ans += n % i

print(ans)
```

The solution reads the input once and maintains a single accumulator. The loop runs from 1 through $n$, ensuring all required divisors are included. The expression `n % i` is computed directly for each iteration, matching the definition exactly.

There are no tricky boundary cases in implementation, but care must be taken to include $i = n$, since $n \bmod n = 0$, and excluding it would slightly reduce the sum incorrectly.

## Worked Examples

### Example 1

Input:

```
5
```

We compute each term:

| i | 5 % i | Running Sum |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 3 |
| 4 | 1 | 4 |
| 5 | 0 | 4 |

Output is 4.

This trace shows how remainders fluctuate depending on how $i$ divides $n$. The contributions are non-monotonic, and only direct evaluation captures the correct structure.

### Example 2

Input:

```
6
```

| i | 6 % i | Running Sum |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |
| 4 | 2 | 2 |
| 5 | 1 | 3 |
| 6 | 0 | 3 |

Output is 3.

This example highlights that many early terms contribute zero because they divide $n$ exactly. The non-zero contributions come only from non-divisors, which explains why the sum tends to be relatively small compared to $n^2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate once over all integers from 1 to n, performing constant-time modulo and addition each time |
| Space | O(1) | Only a single accumulator variable is used |

Given $n \le 10^5$, an $O(n)$ loop is easily fast enough in Python, with at most $10^5$ iterations and simple arithmetic per iteration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    ans = 0
    for i in range(1, n + 1):
        ans += n % i
    return str(ans)

# provided sample
assert run("5\n") == "4"

# minimum input
assert run("1\n") == "0"

# small case with full divisibility structure
assert run("6\n") == "3"

# all primes behavior check
assert run("7\n") == str(sum(7 % i for i in range(1, 8)))

# larger boundary
assert run("100000\n") == str(sum(100000 % i for i in range(1, 100001)))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | smallest edge case |
| 6 | 3 | multiple exact divisors |
| 100000 | computed sum | upper bound performance sanity |

## Edge Cases

For $n = 1$, the loop runs only once with $i = 1$. The computation is $1 \bmod 1 = 0$, so the accumulator stays 0 and the output is correct.

For values where $n$ is prime, all terms except $i = 1$ and $i = n$ contribute non-zero values. For example, $n = 7$ produces remainders $0,1,2,3,2,1,0$, and the algorithm accumulates them directly without relying on any special-case logic.

For large $n$, such as $100000$, the loop still executes within limits because it performs only simple arithmetic per iteration. No intermediate state grows beyond a single integer, so memory usage remains constant and stable.
