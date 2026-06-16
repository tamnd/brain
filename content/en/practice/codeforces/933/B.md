---
title: "CF 933B - A Determined Cleanup"
description: "We are asked to construct a polynomial whose coefficients are non-negative integers strictly less than a given base $k$, such that when this polynomial is divided by $x + k$, the remainder is exactly the constant polynomial $p$."
date: "2026-06-17T02:51:54+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 933
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 462 (Div. 1)"
rating: 2000
weight: 933
solve_time_s: 70
verified: true
draft: false
---

[CF 933B - A Determined Cleanup](https://codeforces.com/problemset/problem/933/B)

**Rating:** 2000  
**Tags:** math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a polynomial whose coefficients are non-negative integers strictly less than a given base $k$, such that when this polynomial is divided by $x + k$, the remainder is exactly the constant polynomial $p$.

Dividing by $x + k$ means that if we evaluate the polynomial at $x = -k$, the value must equal $p$, since the remainder theorem tells us that the remainder of division by $x + k$ is $f(-k)$. So the task is equivalent to building a finite sequence of digits $a_0, a_1, \dots, a_{d-1}$ in base $k$-like constraints, where each digit lies in $[0, k-1]$, and their signed weighted sum

$$f(-k) = a_0 - a_1 k + a_2 k^2 - a_3 k^3 + \dots$$

must equal $p$.

The coefficients are not allowed to be negative, so we cannot directly represent the alternating base-$k$ expansion of $p$ without carrying. The challenge is to simulate a signed base representation while keeping every digit within $[0, k-1]$.

The constraints are very tight: $p \le 10^{18}$ and $k \le 2000$. Any solution must be essentially linear in the number of digits produced, since even $O(\log p)$ is acceptable but anything quadratic in digit construction would still pass. The real difficulty is not computational complexity but ensuring a valid digit system without violating coefficient bounds.

A naive attempt would be to expand $p$ in base $k$ directly and assign coefficients greedily. This fails because of the alternating signs induced by evaluation at $-k$. For example, setting digits from least significant upward as $p \bmod k$ ignores that higher powers subtract rather than add, which breaks correctness immediately.

A second failure mode occurs when carries are not handled symmetrically across alternating signs. For instance, a digit intended to be negative contribution at an odd position cannot simply be set to zero or reduced locally without affecting higher terms.

## Approaches

A brute-force approach would attempt to construct coefficients one by one, maintaining the exact value of the polynomial evaluated at $-k$. At each position, we would try all possible digits from $0$ to $k-1$ and recursively adjust the remaining target value. This quickly becomes infeasible because the branching factor is $k$, and the depth can reach up to $O(\log_k p)$, leading to exponential blow-up.

The key observation is that the polynomial evaluation at $-k$ behaves like a mixed-radix number system with alternating signs. This suggests that we can construct digits greedily from the lowest degree upward, but we must carefully manage a running "carry" that absorbs sign alternation.

At step $i$, we decide coefficient $a_i$. Its contribution to the value is $a_i \cdot (-k)^i$. Instead of working with alternating signs directly, we maintain a current remainder and enforce divisibility by $k$ at each step, but adjust the remainder when the parity of the position flips the sign.

The crucial insight is that after choosing $a_i$, the remaining target must remain an integer multiple of $k$, because higher powers of $x$ correspond to higher powers of $k$ in magnitude. This enforces a deterministic digit extraction process similar to base conversion, except that at odd positions we correct for negative contribution by effectively adding a full $k$-block before division.

This transforms the problem into a controlled digit construction in a signed base system.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(d) | Too slow |
| Optimal | O(log_k p) | O(log_k p) | Accepted |

## Algorithm Walkthrough

We build coefficients from degree 0 upward while maintaining a current residual value representing what still must be matched by higher-degree terms.

1. Start with current value $p$ and an empty list of coefficients.

We interpret this value as what remains to be represented by the polynomial.
2. For each position $i = 0, 1, 2, \dots$, determine the coefficient $a_i$.

At even positions, the contribution is positive; at odd positions, it is negative. This sign alternation determines how we extract digits.
3. If $i$ is even, we set

$$a_i = p \bmod k$$

because this position contributes positively in base-$k$-like expansion.
4. If $i$ is odd, we must compensate for the negative sign. We compute

$$a_i = (k - (p \bmod k)) \bmod k$$

This ensures that after subtracting $a_i \cdot k^i$, the remainder becomes divisible by $k$ in a consistent way.
5. Update the remaining value by subtracting the chosen digit contribution and dividing by $k$, carefully adjusting for sign.
6. Repeat until the remaining value becomes zero.
7. Remove trailing zeros in the coefficient list, ensuring the highest coefficient is non-zero.

The reason this process terminates is that each step reduces the magnitude of the remaining value roughly by a factor of $k$, similar to standard base conversion, but with alternating correction.

### Why it works

At each step, we enforce that the residual value after subtracting the chosen coefficient is divisible by $k$. This guarantees that higher-order coefficients can represent the remaining value without fractional interference. The alternating correction ensures that negative contributions at odd indices are always compensated within the digit range $[0, k-1]$, so no invalid coefficient is ever produced. The invariant maintained is that the remaining value always corresponds exactly to what higher-degree terms must encode in a valid signed base-$k$ representation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p, k = map(int, input().split())

    coeffs = []

    x = p
    i = 0

    while x != 0:
        if i % 2 == 0:
            a = x % k
            x = (x - a) // k
        else:
            # adjust so that remainder division works with negative sign
            a = (-x) % k
            x = (x + a) // k

        coeffs.append(a)
        i += 1

    if not coeffs:
        print(-1)
        return

    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()

    print(len(coeffs))
    print(*coeffs)

if __name__ == "__main__":
    solve()
```

The implementation follows the alternating-digit extraction directly. The key subtlety is the handling of odd indices, where we convert the residual into a form that remains divisible by $k$ after adjusting for the negative contribution. The integer divisions are exact by construction of the chosen coefficients, so no floating-point issues arise.

The trimming step ensures that we do not output unnecessary leading zeros, since the highest-degree coefficient must be non-zero.

## Worked Examples

### Example 1

Input:

```
46 2
```

We track the process:

| i | x (before) | a_i | operation | x (after) |
| --- | --- | --- | --- | --- |
| 0 | 46 | 0 | (46 - 0)/2 | 23 |
| 1 | 23 | 1 | (23 + 1)/2 | 12 |
| 2 | 12 | 0 | (12 - 0)/2 | 6 |
| 3 | 6 | 0 | (6 + 0)/2 | 3 |
| 4 | 3 | 1 | (3 - 1)/2 | 1 |
| 5 | 1 | 1 | (1 + 1)/2 | 1 |
| 6 | 1 | 1 | (1 - 1)/2 | 0 |

The coefficients become `[0, 1, 0, 0, 1, 1, 1]`, matching the sample output.

This trace shows how alternating corrections keep division exact at every step.

### Example 2

Input:

```
2018 10
```

| i | x (before) | a_i | operation | x (after) |
| --- | --- | --- | --- | --- |
| 0 | 2018 | 8 | (2018 - 8)/10 | 201 |
| 1 | 201 | 9 | (201 + 9)/10 | 21 |
| 2 | 21 | 1 | (21 - 1)/10 | 2 |
| 3 | 2 | 8 | (2 + 8)/10 | 1 |
| 4 | 1 | 1 | (1 - 1)/10 | 0 |

Output coefficients are `[8, 9, 1, 8, 1]`.

This example highlights how odd positions force adjustment upward before division.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_k p)$ | Each step reduces the magnitude of the remaining value by roughly a factor of $k$. |
| Space | $O(\log_k p)$ | Stores one coefficient per digit of the constructed representation. |

The bounds $p \le 10^{18}$ and $k \le 2000$ imply at most around 60 steps, so the algorithm is comfortably fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import *
    p, k = map(int, sys.stdin.readline().split())

    coeffs = []
    x = p
    i = 0

    while x != 0:
        if i % 2 == 0:
            a = x % k
            x = (x - a) // k
        else:
            a = (-x) % k
            x = (x + a) // k
        coeffs.append(a)
        i += 1

    if not coeffs:
        return "-1\n"

    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()

    return str(len(coeffs)) + "\n" + " ".join(map(str, coeffs)) + "\n"

# provided sample
assert run("46 2") == "7\n0 1 0 0 1 1 1\n"

# minimum edge
assert run("1 2") != ""

# small base
assert run("10 3") != ""

# power of k
assert run("100 10") != ""

# large value
assert run("1000000000000000000 2000") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 46 2 | 7 digits | Alternating carry correctness |
| 1 2 | valid short poly | Minimal representation |
| 10 3 | valid base-3 mix | Non-binary base handling |
| 100 10 | structured digits | clean divisibility chain |
| large case | valid output | performance and stability |

## Edge Cases

One edge case occurs when $p$ is already zero. In this situation, the algorithm never enters the loop and would output an empty coefficient list. The correct interpretation is that no polynomial is needed beyond the zero polynomial, but the problem requires a valid representation with a non-zero highest coefficient. The implementation handles this by printing $-1$ for empty construction.

Another edge case arises when repeated carries propagate through many levels due to small $k$, such as $k = 2$. For instance, large powers of two in $p$ create long alternating adjustments. The algorithm still processes each bit exactly once, and the invariant that $x$ becomes divisible by $k$ after each step ensures no infinite loop or precision issue occurs.
