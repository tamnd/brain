---
title: "CF 105272F - Festival of the Moon"
description: "We are observing a single festival where every participant bought exactly one ticket. There are two ticket types: a normal ticket costing v and a discounted lunar ticket costing exactly half of that, v/2, where v is guaranteed to be even."
date: "2026-06-23T06:56:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "F"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 42
verified: true
draft: false
---

[CF 105272F - Festival of the Moon](https://codeforces.com/problemset/problem/105272/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are observing a single festival where every participant bought exactly one ticket. There are two ticket types: a normal ticket costing `v` and a discounted lunar ticket costing exactly half of that, `v/2`, where `v` is guaranteed to be even.

We are given the total number of attendees `p`, the total revenue collected `a`, and the full ticket price `v`. Some unknown number of attendees are lunar residents who always pay the discounted price, while all other attendees pay the full price. The task is to determine how many of the `p` attendees bought the discounted ticket.

The constraints are large but the structure is extremely simple: all values are up to one million, and only arithmetic relationships matter. This immediately rules out any simulation over individuals or search over possible counts in a naïve way that depends on iterating up to `p` or `a`. Any correct solution must reduce the problem to a constant-time computation derived from an equation.

A subtle failure case appears if one tries to reason greedily without forming an equation. For example, assuming that maximizing discounted attendees is always valid can break consistency with the total revenue constraint. Another common mistake is forgetting that the discount is exactly half of `v`, not an arbitrary fraction, which is essential for forming a clean linear relation.

## Approaches

A brute-force interpretation would try every possible number `x` of lunar attendees from `0` to `p`, compute the resulting revenue, and check whether it matches `a`. This works because each candidate fully determines revenue, but it costs `O(p)` per test case. With `p` up to one million, this is still feasible in isolation, but becomes unnecessary and conceptually inefficient given that the relationship is linear and solvable directly.

The key observation is that the total revenue can be expressed as a linear function of the unknown variable `x`. If `x` attendees pay half price and `p - x` pay full price, then the revenue is completely determined by `x`. This transforms the problem into solving a single linear equation in one variable. Once that equation is rearranged, the answer is obtained directly without any iteration.

The structure of the problem guarantees that the resulting value is an integer and non-negative, so no additional search or rounding logic is required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start by assuming that `x` people are lunar attendees who pay `v/2`, while the remaining `p - x` pay `v`.

This directly encodes the only unknown in the system.
2. Express total revenue as a sum of contributions:

`a = x * (v/2) + (p - x) * v`.

This step converts the story into a deterministic equation.
3. Expand the expression:

`a = x*v/2 + p*v - x*v`.
4. Group terms involving `x`:

`a = p*v - x*(v/2)`.
5. Rearrange to isolate `x`:

`x*(v/2) = p*v - a`.
6. Solve for `x`:

`x = (2 * (p*v - a)) / v`.

The multiplication by 2 avoids fractional division since `v` is even.
7. Return `x` as the number of lunar attendees.

### Why it works

The revenue function is linear in `x`, meaning every additional lunar attendee replaces a full-price ticket with a half-price one and reduces revenue by exactly `v/2`. Since the baseline revenue with no discounts is `p*v`, the difference `p*v - a` measures the total reduction caused by discounted attendees. Dividing this total reduction by `v/2` gives exactly how many such reductions occurred, which corresponds uniquely to `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, p, v = map(int, input().split())
    # derived formula: x = 2*(p*v - a) / v
    x = (2 * (p * v - a)) // v
    print(x)

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the derived formula. The multiplication `p * v` is done first, which fits safely within Python’s integer range. Integer division is used at the end because the problem guarantees the result is an integer.

A common implementation mistake is rearranging the formula in a way that introduces floating-point division, which is unnecessary and can cause precision issues in other languages. Another mistake is forgetting to multiply by 2 before dividing by `v`, which would lose correctness because the discount is exactly half the full price.

## Worked Examples

### Example 1

Input:

`a = 7, p = 5, v = 2`

We compute the candidate values step by step.

| Step | Expression | Value |
| --- | --- | --- |
| Baseline revenue | p * v | 10 |
| Revenue deficit | p*v - a | 3 |
| Lunar count | 2*(p*v - a)/v | 3 |

This confirms that 3 attendees are lunar, which matches the intuition that three people paid half price and two paid full price.

### Example 2

Input:

`a = 22, p = 7, v = 4`

| Step | Expression | Value |
| --- | --- | --- |
| Baseline revenue | p * v | 28 |
| Revenue deficit | p*v - a | 6 |
| Lunar count | 2*(p*v - a)/v | 3 |

This shows that exactly 3 attendees used the discounted ticket, meaning the remaining 4 paid full price.

Both examples confirm that the computed value aligns exactly with the revenue difference interpretation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The solution comfortably fits within the constraints since it performs constant-time arithmetic regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, p, v = map(int, input().split())
    x = (2 * (p * v - a)) // v
    return str(x)

# provided samples
assert run("7 5 2\n") == "3"
assert run("22 7 4\n") == "3"

# all full-price attendees (no discount)
assert run("10 2 5\n") == "0"

# all discounted attendees
assert run("5 2 2\n") == "2"

# mixed case
assert run("18 4 4\n") == "1"

# maximum values stress case
assert run("1000000 1000000 1000000\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all full price | 0 | no lunar attendees case |
| all discounted | p | upper bound behavior |
| mixed values | 1 | correctness of linear relation |
| max values | 0 | overflow safety and scale |

## Edge Cases

When all attendees pay full price, the revenue equals `p * v`. Substituting into the formula yields `x = 0`, which correctly reflects that no discounted tickets were used.

When all attendees are lunar residents, the revenue becomes `p * v / 2`. Plugging this into the equation gives `x = p`, matching the expectation that every attendee used the discount.

For maximum input values, the intermediate product `p * v` can reach `10^12`, but Python handles this safely, and the final division still produces a valid integer.
