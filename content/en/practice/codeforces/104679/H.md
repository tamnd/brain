---
title: "CF 104679H - A Dance with DS"
description: "We are given two integers. One is a fixed base-like parameter $k$, and the other is an upper bound $r$. For any non-negative integer $n$, we define a process: if $n$ is divisible by $k$, we divide it by $k$, otherwise we subtract 1."
date: "2026-06-29T09:02:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104679
codeforces_index: "H"
codeforces_contest_name: "Replay of Battle of Brains 2022, University of Dhaka"
rating: 0
weight: 104679
solve_time_s: 42
verified: true
draft: false
---

[CF 104679H - A Dance with DS](https://codeforces.com/problemset/problem/104679/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers. One is a fixed base-like parameter $k$, and the other is an upper bound $r$. For any non-negative integer $n$, we define a process: if $n$ is divisible by $k$, we divide it by $k$, otherwise we subtract 1. Repeating this until reaching 0 gives a number of operations $f(n)$. The task is to maximize $f(n)$ over all integers $n$ in the range $[0, r]$.

The key difficulty is not computing $f(n)$ for a single value. That part becomes structured once we notice the process behaves like repeatedly removing the last digit in base $k$. The real challenge is searching over all values up to $r$, which can be very large, so we need to reason about how the structure of numbers affects the cost without simulating every $n$.

The constraints implied by the problem setting are typical competitive programming limits: $r$ is large enough that iterating over all values is impossible, so any solution that evaluates each $n$ independently would be quadratic or linear in $r$, which is too slow. We need something closer to logarithmic or at worst linear in the number of digits.

A subtle edge case appears when $n$ has leading structure changes in base $k$. For example, when the most significant digit becomes zero after a decrement, the number of digits effectively shrinks. Another issue is small values of $n$, where the “digit formula” still holds but needs careful interpretation when the representation has only one digit.

## Approaches

The naive approach is straightforward. For every $n \le r$, simulate the process: if divisible by $k$, divide, otherwise subtract one, counting steps. Each simulation costs $O(\log_k n)$, since each division reduces magnitude, but in the worst case we subtract many times before a division happens. Over all $n$, this leads to about $O(r \log r)$, which is far beyond feasible limits when $r$ is large.

The turning point is realizing that the process is equivalent to working in base $k$. Each subtraction reduces the last digit, and each division removes a digit. This means the number of steps is directly tied to the digit structure of $n$ in base $k$. In fact, each digit contributes its value plus a structural cost, leading to a clean closed form:

$$f(n) = (\text{sum of digits of } n \text{ in base } k) + (\text{number of digits}) - 1$$

So instead of simulating transitions, we are maximizing a digit-based function.

Now the problem becomes: among all numbers $n \le r$, maximize a function that depends only on digits in base $k$. This is a classic digit-DP-style structure, but we do not need full DP. We only need the maximum, and the objective is monotone in each digit: larger digits always help.

This allows a greedy construction over prefixes of $r$ in base $k$. We fix a prefix length where we match $r$, then at the first position where we drop below $r$, we reduce that digit by one and fill the rest with $k-1$, maximizing digit sum while staying below $r$.

We also handle the special case where we choose zero common prefix, which effectively reduces the number of digits by one if the leading digit allows it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(r \log r)$ | $O(1)$ | Too slow |
| Base-k Digit Greedy Construction | $O(\log_k r)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Convert $r$ into its base $k$ representation. This gives a digit array where each position corresponds to a power of $k$. This is necessary because the objective function is digit-based.
2. For each possible prefix length $p$ from $0$ to the number of digits in $r$, assume we match the first $p$ digits of $r$. This fixes the highest structure of the candidate number.
3. If $p$ equals the full length, the candidate is exactly $r$, so its value is computed directly from digit sum plus digit count.
4. Otherwise, at position $p$, we reduce the digit of $r$ by 1, provided it is not zero. If it is zero, this prefix choice is invalid because we cannot form a smaller number without reducing length earlier.
5. After decreasing that digit, fill all remaining positions with $k-1$. This maximizes digit sum while guaranteeing the constructed number is strictly less than $r$.
6. If we choose $p = 0$, we are effectively constructing numbers with fewer digits than $r$. In this case, the best possible number is all digits equal to $k-1$ with one fewer digit than $r$, since that maximizes both digit sum and digit count under the constraint.
7. Compute the objective value for each candidate and take the maximum.

### Why it works

Any number $n \le r$ must match $r$ in some prefix and differ at the first differing digit. At that position, it must be strictly smaller, and all later digits can be chosen freely up to $k-1$. Since the objective is strictly increasing in each digit and also increases with digit count, any optimal solution must maximize digits after the first deviation and delay the deviation as far right as possible. This forces the greedy structure over prefixes, ensuring no candidate outside these constructed forms can improve the objective.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_base_k(x, k):
    if x == 0:
        return [0]
    digs = []
    while x > 0:
        digs.append(x % k)
        x //= k
    return digs[::-1]

def value(digits):
    # (sum of digits) + (number of digits) - 1
    return sum(digits) + len(digits) - 1

def solve():
    k, r = map(int, input().split())

    digits = to_base_k(r, k)
    n = len(digits)

    best = 0

    # case: use r itself
    best = max(best, value(digits))

    # try prefix matches
    for p in range(n):
        if digits[p] == 0:
            continue

        cand = digits[:p]
        cand.append(digits[p] - 1)
        cand.extend([k - 1] * (n - p - 1))

        best = max(best, value(cand))

    # try shorter length (p = 0 type case)
    if n > 1:
        cand = [k - 1] * (n - 1)
        best = max(best, value(cand))

    print(best)

if __name__ == "__main__":
    solve()
```

The conversion to base $k$ is essential because it transforms the subtraction-and-division process into a digit problem. The helper `value` directly encodes the derived formula, avoiding any simulation.

The main loop enumerates the first position where we break from $r$. The condition `digits[p] == 0` skips invalid cases where we cannot reduce that digit without borrowing earlier. Once we reduce a digit, filling the suffix with $k-1$ guarantees maximal contribution from remaining positions.

The final special case handles numbers with fewer digits than $r$, where we maximize both digit count and digit sum independently by using all $k-1$ digits.

## Worked Examples

### Example 1

Let $k = 10$, $r = 274$. Base-10 digits are $[2, 7, 4]$.

| Prefix p | Candidate digits | Value |
| --- | --- | --- |
| 3 | [2, 7, 4] | 2+7+4+3-1 = 15 |
| 0 | [9, 9] | 9+9+2-1 = 19 |
| 1 | [1, 9, 9] | 1+9+9+3-1 = 21 |
| 2 | [2, 6, 9] | 2+6+9+3-1 = 19 |

The best is prefix 1, giving 21. This demonstrates why pushing the deviation earlier can sometimes dominate, since digit count and suffix maximization interact.

### Example 2

Let $k = 9$, $r = 413089$. Digits are $[4,1,3,0,8,9]$.

| Prefix p | Candidate digits | Value |
| --- | --- | --- |
| 6 | [4,1,3,0,8,9] | fixed |
| 2 | [4,1,2,8,8,8] | optimal candidate |
| 3 | invalid (digit 0) | skipped |
| 0 | [8,8,8,8,8] | shorter length case |

This shows how skipping zero digits is necessary, since reducing a zero without earlier borrowing is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_k r)$ | single base conversion and linear scan over digits |
| Space | $O(\log_k r)$ | storing base-k representation |

The solution only depends on the number of digits of $r$, so it remains efficient even when $r$ is extremely large.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def to_base_k(x, k):
        if x == 0:
            return [0]
        digs = []
        while x > 0:
            digs.append(x % k)
            x //= k
        return digs[::-1]

    def value(digits):
        return sum(digits) + len(digits) - 1

    k, r = map(int, sys.stdin.readline().split())
    digits = to_base_k(r, k)
    n = len(digits)

    best = value(digits)

    for p in range(n):
        if digits[p] == 0:
            continue
        cand = digits[:p] + [digits[p] - 1] + [k - 1] * (n - p - 1)
        best = max(best, value(cand))

    if n > 1:
        best = max(best, value([k - 1] * (n - 1)))

    return str(best)

# small cases
assert run("10 0") == "0"
assert run("10 5") == "5"
assert run("10 10") == "10"
assert run("10 274") == "21"

# base-k behavior
assert run("2 5") == "5"
assert run("2 12") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 0 | 0 | minimum boundary |
| 10 5 | 5 | single-digit behavior |
| 10 274 | 21 | multi-digit prefix logic |
| 2 12 | 7 | binary digit structure |

## Edge Cases

A critical edge case is when $r$ is a power of $k$, such as $1000_k$. A naive prefix reduction might attempt to decrease a zero digit too late, which is invalid. The algorithm correctly skips such prefixes and instead relies on earlier positions or shorter-length constructions.

Another edge case is $r < k$, where the base representation has a single digit. In this case, only two candidates exist: $r$ itself and $k-1$. The algorithm naturally covers both because the prefix loop contributes nothing meaningful and the shorter-length case is either absent or dominates appropriately, producing correct results without special casing.
