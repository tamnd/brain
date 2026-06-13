---
title: "CF 1250F - Data Center"
description: "We are given a target area $n$, and we want to build a rectangle whose sides are integers and whose area is exactly $n$. Every valid rectangle corresponds to choosing two integers $a$ and $b$ such that $a cdot b = n$."
date: "2026-06-13T21:14:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1250
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 800
weight: 1250
solve_time_s: 146
verified: true
draft: false
---

[CF 1250F - Data Center](https://codeforces.com/problemset/problem/1250/F)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target area $n$, and we want to build a rectangle whose sides are integers and whose area is exactly $n$. Every valid rectangle corresponds to choosing two integers $a$ and $b$ such that $a \cdot b = n$. Among all such factor pairs, we want the rectangle with the smallest perimeter, which is $2(a + b)$.

So the task is purely about factorization: among all integer pairs whose product is fixed, we want the pair that minimizes their sum. Geometrically, this corresponds to making the rectangle as close to a square as possible, since balanced sides reduce perimeter for a fixed area.

The constraint $n \le 10^5$ is small enough that iterating up to $\sqrt{n}$ is feasible in constant time per test. A brute force over all possible factors up to $n$ would still pass, but it is unnecessary.

A subtle failure case for careless solutions is assuming $a = \lfloor \sqrt{n} \rfloor$ always gives a valid rectangle. That only works when $n$ is a perfect square. For example, if $n = 13$, $\lfloor \sqrt{13} \rfloor = 3$, but $13$ is not divisible by $3$, so $3 \times 3$ is invalid. The correct answer comes from $1 \times 13$.

Another edge case is $n = 1$. The only rectangle is $1 \times 1$, so perimeter is $4$. Any logic relying on factor search must still handle this cleanly.

## Approaches

A straightforward approach is to enumerate every possible pair $(a, b)$ such that $a \cdot b = n$, compute $2(a+b)$, and take the minimum. The correctness is immediate because it checks all valid rectangles. The problem is efficiency: scanning all values of $a$ from $1$ to $n$ leads to $O(n)$ checks, which is unnecessary and wasteful even though $n$ is only $10^5$.

The key observation is that factors come in pairs around $\sqrt{n}$. If $a \cdot b = n$, then at least one of $a, b$ is less than or equal to $\sqrt{n}$. This means we only need to iterate $a$ up to $\sqrt{n}$, and whenever $a$ divides $n$, we evaluate the corresponding pair $(a, n/a)$.

This reduces the search space from linear to square root size while still guaranteeing we examine every valid factor pair.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Too slow |
| Optimal (factor scan) | $O(\sqrt{n})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `best` with a very large value to store the minimum perimeter found so far. This ensures any valid rectangle will improve it.
2. Iterate $a$ from $1$ to $\lfloor \sqrt{n} \rfloor$. We only search up to the square root because every factor pair must have at least one element in this range.
3. For each $a$, check if $n \bmod a = 0$. If not, skip it since it cannot form a valid rectangle side.
4. If it divides evenly, compute $b = n / a$. This gives a valid rectangle $a \times b$.
5. Compute perimeter $p = 2(a + b)$ and update `best = min(best, p)`. Each valid factor pair is a candidate shape.
6. After finishing the loop, output `best`.

### Why it works

Every valid rectangle corresponds to exactly one factor pair $(a, b)$ with $a \le \sqrt{n}$ or $b \le \sqrt{n}$. The loop guarantees we encounter all such pairs exactly once through the smaller factor. Since perimeter depends only on the sum $a + b$, checking all valid pairs ensures the minimum is found without missing any candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

best = 10**18
i = 1

while i * i <= n:
    if n % i == 0:
        j = n // i
        best = min(best, 2 * (i + j))
    i += 1

print(best)
```

The solution maintains a running minimum over all valid factor pairs. The loop condition `i * i <= n` avoids floating-point square roots and guarantees integer-safe iteration. Each time we find a divisor, we immediately form the paired factor using integer division, ensuring no precision issues arise.

## Worked Examples

### Example 1: $n = 36$

| i | Divides? | j = 36/i | Perimeter $2(i+j)$ | Best |
| --- | --- | --- | --- | --- |
| 1 | yes | 36 | 74 | 74 |
| 2 | yes | 18 | 40 | 40 |
| 3 | yes | 12 | 30 | 30 |
| 4 | yes | 9 | 26 | 26 |
| 5 | no | - | - | 26 |
| 6 | yes | 6 | 24 | 24 |

The trace shows the perimeter shrinking as the factor pair becomes more balanced, reaching the minimum at the square $6 \times 6$.

### Example 2: $n = 13$

| i | Divides? | j = 13/i | Perimeter | Best |
| --- | --- | --- | --- | --- |
| 1 | yes | 13 | 28 | 28 |
| 2 | no | - | - | 28 |
| 3 | no | - | - | 28 |

Only one valid factor pair exists, so the algorithm correctly falls back to the rectangle $1 \times 13$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{n})$ | We test each integer up to $\sqrt{n}$ once |
| Space | $O(1)$ | Only a few integer variables are stored |

The upper bound $n \le 10^5$ makes $\sqrt{n} \le 316$, so the loop runs a negligible number of iterations under the time limit.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input())

    best = 10**18
    i = 1
    while i * i <= n:
        if n % i == 0:
            j = n // i
            best = min(best, 2 * (i + j))
        i += 1

    print(best)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    out = StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert run("36\n") == "24"
assert run("13\n") == "28"

# custom cases
assert run("1\n") == "4"
assert run("2\n") == "6"
assert run("49\n") == "28"
assert run("100000\n") == str(min(2*(i + 100000//i) for i in range(1, 100000+1) if 100000 % i == 0))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 4 | smallest boundary case |
| 2 | 6 | smallest non-square prime-like behavior |
| 49 | 28 | perfect square case |

## Edge Cases

For $n = 1$, the only valid rectangle is $1 \times 1$. The loop still executes once with $i = 1$, detects divisibility, and computes perimeter $2(1+1) = 4$, which matches the correct answer.

For a prime number like $n = 13$, no divisor exists except $1$, so the algorithm naturally falls back to $1 \times 13$, producing perimeter $28$. The absence of internal divisors does not require special handling.

For perfect squares like $n = 36$, multiple factor pairs are discovered, and the minimum occurs at the central pair $6 \times 6$. The iteration ensures this pair is explicitly evaluated, so the optimal structure is never missed.
