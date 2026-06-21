---
title: "CF 106054G - Going to the kiosk"
description: "We are modeling a very small payment system. A customer wants to buy an item priced at $A$ pesos. He pays with a single bill worth $B$ pesos, so the kiosk must return exactly $B - A$ pesos in change."
date: "2026-06-21T07:43:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106054
codeforces_index: "G"
codeforces_contest_name: "2025 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 106054
solve_time_s: 34
verified: true
draft: false
---

[CF 106054G - Going to the kiosk](https://codeforces.com/problemset/problem/106054/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are modeling a very small payment system. A customer wants to buy an item priced at $A$ pesos. He pays with a single bill worth $B$ pesos, so the kiosk must return exactly $B - A$ pesos in change. The twist is that the kiosk does not return coins or bills, only candies, and each candy has a fixed value $C$ pesos.

The question is whether it is possible to represent the exact change amount using only whole candies of value $C$. In other words, we need to determine whether the difference $B - A$ can be written as $k \cdot C$ for some integer $k \ge 0$.

The constraints are extremely small, with all values up to 1000. This immediately removes any concern about performance or overflow, since even a direct arithmetic check is constant time.

A subtle issue is understanding the requirement “exact change”. It is not enough for the kiosk to get close. Any leftover or deficit invalidates the solution. For example, if $A = 6$, $B = 10$, and $C = 3$, the change is 4. Two candies give 6, which is too much, and one candy gives 3, which is too little. This is a direct example where divisibility fails even though the value is small.

Edge cases are mostly about divisibility logic rather than computation. Since $A < B$, the change is always positive, so we never need to handle zero or negative change. That removes the only potential ambiguity in interpretation.

## Approaches

The brute-force way to think about the problem is to try all possible numbers of candies. If we choose $k$ candies, we give back $k \cdot C$ pesos. We can iterate $k$ from 0 up to $\lfloor (B-A)/C \rfloor$ and check whether any choice matches exactly the required change.

This is correct because the only valid transactions are integer multiples of $C$. However, even though the range is small enough here, this approach is structurally inefficient and unnecessary. In a larger variant of the problem, iterating all $k$ would become linear in the size of the change amount.

The key observation is that we are not searching for any special structure beyond divisibility. We are simply checking whether the difference $B - A$ is divisible by $C$. If it is, then we can form the exact change using candies; if not, it is impossible.

This reduces the entire problem to a single modulo operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(B-A)$ | $O(1)$ | Accepted but unnecessary |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the change amount $D = B - A$. This represents the exact value the kiosk must return.
2. Check whether $D$ is divisible by $C$, meaning whether $D \bmod C = 0$. If this holds, the change can be formed exactly using candies.
3. If the divisibility condition is satisfied, output “S”, otherwise output “N”.

The reason this check is sufficient is that each candy contributes exactly $C$ pesos and there is no constraint on the number of candies other than non-negativity.

### Why it works

Any valid solution must represent the change as a sum of identical units of size $C$. That means the change must lie in the set $\{0, C, 2C, 3C, \dots\}$. This set is exactly the set of multiples of $C$. Membership in this set is equivalent to having remainder zero when divided by $C$. Since $D = B - A$ is fixed and deterministic, checking divisibility fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

A, B, C = map(int, input().split())

change = B - A

if change % C == 0:
    print("S")
else:
    print("N")
```

The solution reads the three integers, computes the required change, and applies a modulo check. The key implementation detail is to compute the difference first and only then apply the modulo, which keeps the logic clean and avoids reasoning about multiple expressions.

There are no loops or edge-case branches needed because the structure of valid answers is purely arithmetic.

## Worked Examples

### Example 1

Input:

```
10 20 5
```

Change is 10.

| Step | Change (B-A) | C | change % C | Decision |
| --- | --- | --- | --- | --- |
| Init | 10 | 5 | - | - |
| Check | 10 | 5 | 0 | S |

Since 10 is exactly 2 times 5, the kiosk can return two candies.

This confirms the invariant that exact representation exists whenever divisibility holds.

### Example 2

Input:

```
6 10 3
```

Change is 4.

| Step | Change (B-A) | C | change % C | Decision |
| --- | --- | --- | --- | --- |
| Init | 4 | 3 | - | - |
| Check | 4 | 3 | 1 | N |

Here, no integer number of candies can sum to 4. One candy is too small, two candies exceed the required amount. This directly shows why divisibility is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations and one modulo check |
| Space | $O(1)$ | No auxiliary data structures used |

The constraints allow any constant-time arithmetic solution comfortably within limits. Even a brute-force loop would be fast enough at $A, B, C \le 1000$, but the modulo check is the direct mathematical characterization of the condition.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline
    A, B, C = map(int, input().split())
    change = B - A
    return "S" if change % C == 0 else "N"

# provided samples
assert run("10 20 5") == "S"
assert run("6 10 3") == "N"

# custom cases
assert run("1 2 1") == "S"   # exact 1 candy
assert run("1 3 2") == "S"   # 2 change with 1 candy
assert run("1 4 2") == "S"   # multiple candies exact fit
assert run("1 5 2") == "N"   # remainder case
assert run("999 1000 7") == "N"  # small edge non-divisible
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 | S | minimal valid divisibility |
| 1 3 2 | S | exact single candy case |
| 1 5 2 | N | non-divisible remainder |
| 999 1000 7 | N | boundary near max values |

## Edge Cases

One edge case is when the change is exactly equal to one candy value. For input `A = 1, B = 4, C = 3`, the change is 3. The algorithm computes $3 \bmod 3 = 0$, so it correctly outputs “S”. This corresponds to giving exactly one candy.

Another edge case is when the change is smaller than a candy. For input `A = 6, B = 10, C = 7`, the change is 4. Since 4 is not divisible by 7, the modulo check fails and the output is “N”. This captures the impossibility of representing a smaller amount using larger fixed units.

A final edge case is when the change is zero, which cannot actually occur under the constraint $A < B$. If it were allowed, the algorithm would still work correctly because zero is divisible by any positive $C$, producing “S”, matching the fact that giving no candies is valid.
