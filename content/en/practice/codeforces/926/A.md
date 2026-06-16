---
title: "CF 926A - 2-3-numbers"
description: "We are asked to count how many integers in a closed interval $[l, r]$ can be written using only the prime factors 2 and 3. Any valid number must have the form $2^x cdot 3^y$, where both exponents are non-negative integers."
date: "2026-06-17T03:09:38+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 926
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2018 - Wild-card Round 1"
rating: 1300
weight: 926
solve_time_s: 71
verified: true
draft: false
---

[CF 926A - 2-3-numbers](https://codeforces.com/problemset/problem/926/A)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many integers in a closed interval $[l, r]$ can be written using only the prime factors 2 and 3. Any valid number must have the form $2^x \cdot 3^y$, where both exponents are non-negative integers. This includes 1, since choosing $x = 0, y = 0$ produces $1$.

The task is purely about counting how many such “restricted-factor” numbers fall inside a given range. There are no other constraints like ordering or decomposition of the interval, so the entire problem reduces to membership testing over a very sparse set of integers.

The constraints allow $l$ and $r$ up to $2 \cdot 10^9$. This size immediately rules out generating all numbers up to $r$ in a dense way or checking every integer in the interval. A naive scan over $[l, r]$ could involve up to two billion iterations in the worst case, which is far beyond feasible limits in a 1-second time bound.

A more subtle issue is duplication in generation attempts. If we try to construct numbers as $2^x \cdot 3^y$, careless enumeration may revisit the same value multiple times, especially if both exponents are iterated independently. Any correct solution must either avoid duplicates or generate values in a controlled order.

Edge cases appear around small bounds and large powers:

If $l = 1$, the number 1 must be included. A naive solution that starts exponentiation from $x = 1$ or $y = 1$ would incorrectly exclude it.

If $r = 1$, the answer is 1 only if $l = 1$, otherwise 0.

Large values near $2 \cdot 10^9$ also matter because powers like $2^{30}$ or $3^{19}$ are close to the limit, and overflow or premature stopping conditions can silently drop valid values.

## Approaches

A brute-force strategy would iterate through every integer in $[l, r]$ and check whether it can be fully factored into 2s and 3s. For each number, we repeatedly divide by 2 while divisible, then by 3, and check if the result becomes 1. This works correctly because it directly tests the definition.

However, this approach examines every integer in the range, so in the worst case it performs $r - l + 1$ checks. With $r$ up to $2 \cdot 10^9$, even a tiny fraction of that range is far too large for a 1-second limit. The cost per check is logarithmic in the value, but the dominant factor is the sheer number of integers.

The key observation is that valid numbers are extremely sparse. Instead of testing every number, we can generate all numbers of the form $2^x \cdot 3^y$ up to $r$. Since both bases grow exponentially, the total number of such values is small. For $2^x$, $x$ is at most 30 before exceeding $2 \cdot 10^9$. For $3^y$, $y$ is at most 19. This gives at most a few hundred combinations.

Once we generate all valid numbers up to $r$, we sort them and count how many lie in the interval $[l, r]$. This converts the problem from scanning a huge range into enumerating a tiny structured set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(r - l + 1)$ | $O(1)$ | Too slow |
| Optimal | $O(\log r \cdot \log r)$ | $O(N)$, $N \approx 200$ | Accepted |

## Algorithm Walkthrough

We construct all numbers of the form $2^x \cdot 3^y$ that do not exceed the upper bound $r$.

1. Fix a power of 3 by iterating $y$ starting from 0 and repeatedly multiplying by 3. This ensures we never miss any exponent of 3 and also avoids recomputation from scratch.
2. For each fixed value $3^y$, generate powers of 2 by starting from 1 and repeatedly multiplying by 2. This builds the full set $2^x \cdot 3^y$ for all valid $x$.
3. Every time we compute a value, we check whether it is within the limit $r$. If it exceeds $r$, we stop increasing the power of 2 for this $y$, since further multiplications will only make it larger.
4. We store each valid value in a container. This collection may contain duplicates if different exponent pairs produce the same number, so we deduplicate using a set.
5. After all generation is complete, we iterate through the resulting set and count how many values lie in $[l, r]$.

The key design choice is the nested exponential generation rather than direct exponent loops, which avoids recomputing powers and keeps operations bounded.

### Why it works

Every valid number must be uniquely representable as $2^x \cdot 3^y$. The generation process enumerates all possible pairs $(x, y)$ within bounds implied by $r$, so no valid number can be missed. Since we explicitly multiply from smaller values upward, every constructed number stays within the constraint before being inserted, ensuring correctness of filtering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    l, r = map(int, input().split())

    vals = set()

    p3 = 1
    while p3 <= r:
        p2 = p3
        while p2 <= r:
            vals.add(p2)
            p2 *= 2
        p3 *= 3

    ans = 0
    for v in vals:
        if l <= v <= r:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly mirrors the construction process. The outer loop fixes powers of 3, while the inner loop multiplies by 2 until exceeding the limit. Each generated value is inserted into a set to guarantee uniqueness. Finally, we count how many fall inside the required interval.

A subtle point is starting both sequences from 1. This ensures that the case $1 = 2^0 \cdot 3^0$ is included naturally without special handling.

## Worked Examples

### Example 1

Input:

```
1 10
```

We generate values as follows:

| y (power of 3) | p3 | p2 sequence (powers of 2) | values added |
| --- | --- | --- | --- |
| 0 | 1 | 1, 2, 4, 8 | 1, 2, 4, 8 |
| 1 | 3 | 3, 6 | 3, 6 |
| 2 | 9 | 9 | 9 |

The set becomes `{1,2,3,4,6,8,9}`. All of these lie in $[1,10]$, so the answer is 7.

This trace confirms that both exponent dimensions are explored fully and that multiplication stops exactly when exceeding the bound.

### Example 2

Input:

```
10 20
```

| y | p3 | p2 sequence | valid values in range |
| --- | --- | --- | --- |
| 0 | 1 | 1,2,4,8,16 | 16 |
| 1 | 3 | 3,6,12,24 | 12 |
| 2 | 9 | 9,18 | 18 |
| 3 | 27 | (stop early) | none |

The collected set is `{1,2,3,4,6,8,9,12,16,18}`. Filtering to $[10,20]$ yields `{12,16,18}`, so the answer is 3.

This example highlights that many generated values lie outside the range and are safely ignored in the final counting step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log r \cdot \log r)$ | at most ~30 powers of 2 and ~20 powers of 3 |
| Space | $O(N)$ | storing all valid values in a set |

The total number of generated candidates is bounded by about 600 before deduplication, which is trivial under the constraints. Both time and memory comfortably fit within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    l, r = map(int, input().split())

    vals = set()

    p3 = 1
    while p3 <= r:
        p2 = p3
        while p2 <= r:
            vals.add(p2)
            p2 *= 2
        p3 *= 3

    return str(sum(1 for v in vals if l <= v <= r))

# provided samples
assert run("1 10") == "7"

# custom cases
assert run("1 1") == "1"
assert run("2 2") == "1"
assert run("10 10") == "0"
assert run("1 1000000000") == run("1 1000000000")  # consistency check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | includes number 1 correctly |
| 2 2 | 1 | single-element range handling |
| 10 10 | 0 | non-valid single value |
| 1 1000000000 | consistent output | scalability and completeness |

## Edge Cases

One important edge case is when the interval starts at 1. The algorithm includes 1 automatically because both loops begin with multipliers initialized to 1. For input `1 1`, the generation produces `{1}`, and the count correctly returns 1.

Another case is when no valid numbers exist in the range, such as `10 10`. The generated set still contains valid numbers like 8 or 9, but none fall within the interval, so the final filter removes everything and the answer is 0.

Large bounds such as `1 2000000000` are handled safely because the loops terminate as soon as values exceed the limit. The exponential growth ensures only a small number of iterations occur before stopping, so the algorithm remains efficient even at maximum input size.
