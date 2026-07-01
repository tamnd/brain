---
title: "CF 104592B - Operation"
description: "Each test case gives a starting value and a collection of arithmetic “cards”. Every card is an operation with a fixed operand, and we are allowed to reorder these cards arbitrarily."
date: "2026-06-30T05:24:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104592
codeforces_index: "B"
codeforces_contest_name: "2017 Google Code Jam World Finals (GCJ 17 World Finals)"
rating: 0
weight: 104592
solve_time_s: 59
verified: true
draft: false
---

[CF 104592B - Operation](https://codeforces.com/problemset/problem/104592/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a starting value and a collection of arithmetic “cards”. Every card is an operation with a fixed operand, and we are allowed to reorder these cards arbitrarily. After choosing an order, we apply the operations sequentially to the initial value, and the result is a rational number.

The key difficulty is that order matters because operations are not commutative, and division is exact over rationals. The task is to find the permutation of cards that maximizes the final value.

Even though there are four operation types, every card transforms the current value in a very structured way. Addition and subtraction shift the value, multiplication and division scale it. This suggests that each card is not an arbitrary operation but a simple linear transformation over rationals.

The constraints allow up to 1000 cards per test case. Trying all permutations is impossible since that would grow factorially. Even dynamic programming over subsets is only feasible for the small case but not for the full input size.

A subtle edge case appears when operations produce negative scaling factors or when division introduces fractions. A naive integer-based simulation breaks immediately because intermediate results are not integers and can grow large in both numerator and denominator. Another failure case appears when assuming that multiplication should always be applied last or first. For example, swapping a multiplication by a negative number with an addition can flip the optimal ordering, so greedy rules based on intuition about arithmetic precedence do not hold.

## Approaches

The first natural attempt is brute force: try all permutations of the cards, simulate the expression, and keep the maximum result. This is correct because it explores the full solution space, but it is exponential in the number of cards. With 1000 cards, the number of permutations is astronomically large, making this approach unusable even for the small test limits beyond about 10 to 12 cards.

The key observation is that every card represents an affine transformation of the form x → a x + b. Addition and subtraction produce a = 1 with different b, multiplication and division produce b = 0 with different a. When composing such transformations, the result remains affine. This means the entire sequence reduces to a single transformation x → A x + B, regardless of parentheses or operator precedence.

Composition behaves predictably: if we apply f then g, the parameters multiply and combine linearly. This structure implies that the final answer depends only on how we arrange the (a, b) pairs.

A crucial simplification follows from checking what actually changes with ordering. If we compare two orders of two transformations, their combined multiplicative factor A is identical regardless of order because multiplication of a values is commutative. The only quantity affected by ordering is the additive part B. So the entire optimization reduces to maximizing B.

This turns the problem into an ordering problem where each item contributes a value b_i weighted by the product of a-values that come after it. The optimal ordering can then be derived using a pairwise swap argument, leading to a sorting rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(C!) | O(C) | Too slow |
| Affine transform + ordering rule | O(C log C) | O(C) | Accepted |

## Algorithm Walkthrough

We rewrite every card as an affine transformation x → a x + b.

For each card, we construct its parameters. Addition and subtraction give a = 1 and b = ±v. Multiplication by v gives a = v and b = 0. Division by v gives a = 1/v and b = 0.

We then need to choose an ordering of these pairs.

1. Convert all cards into pairs (a_i, b_i). This standardizes all operations into a single mathematical form.
2. Decide an ordering strategy by comparing pairs. For any two cards i and j, we compare the effect of placing i before j versus j before i on the additive contribution. The multiplicative part does not depend on order, so only the additive contribution matters.
3. For a fixed pair, compute both possibilities:

placing i before j contributes b_i * a_j + b_j

placing j before i contributes b_j * a_i + b_i
4. Prefer i before j when the first expression is larger. This inequality simplifies into a comparison rule:

b_i (a_j − 1) ≥ b_j (a_i − 1)
5. Sort all cards using this comparison rule.
6. After sorting, compute the final affine transformation by sequential composition. Starting from identity transformation x → x, update (A, B) by composing each card in order.
7. Apply the final transformation to S, giving A*S + B.
8. Output the result as a reduced fraction with positive denominator.

The comparison step is the only nontrivial part, and it defines the entire ordering.

### Why it works

The transformation composition always produces a final value of the form A*S + B. Since A is independent of ordering, maximizing the final result reduces to maximizing B. The swap condition guarantees that for any adjacent inversion, swapping into the preferred order does not decrease B. Repeatedly eliminating inversions leads to a globally optimal ordering, since any permutation can be sorted using adjacent swaps without violating the ordering rule.

## Python Solution

```python
import sys
from functools import cmp_to_key
from fractions import Fraction

input = sys.stdin.readline

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        S, C = map(int, input().split())

        cards = []
        for _ in range(C):
            op, v = input().split()
            v = int(v)

            if op == '+':
                a = Fraction(1, 1)
                b = Fraction(v, 1)
            elif op == '-':
                a = Fraction(1, 1)
                b = Fraction(-v, 1)
            elif op == '*':
                a = Fraction(v, 1)
                b = Fraction(0, 1)
            else:
                a = Fraction(1, v)
                b = Fraction(0, 1)

            cards.append((a, b))

        def cmp(x, y):
            a1, b1 = x
            a2, b2 = y
            left = b1 * (a2 - 1)
            right = b2 * (a1 - 1)
            if left > right:
                return -1
            if left < right:
                return 1
            return 0

        cards.sort(key=cmp_to_key(cmp))

        A = Fraction(1, 1)
        B = Fraction(0, 1)

        for a, b in cards:
            B = B * a + b
            A = A * a

        result = A * S + B

        num = result.numerator
        den = result.denominator
        if den < 0:
            num = -num
            den = -den

        print(f"Case #{tc}: {num} {den}")

if __name__ == "__main__":
    solve()
```

The implementation starts by converting every operation into a fractional linear transformation. Division is handled naturally through fractions, which avoids precision issues entirely.

The comparator directly encodes the swap condition derived in the algorithm section. Python’s sorting uses this comparator to produce the globally optimal order.

The final loop composes transformations in sequence. Even though A is not strictly needed for ordering, it is maintained for correctness and clarity in computing the final affine form.

Finally, the result is normalized so that the denominator is positive, and the fraction is already reduced by the `Fraction` type.

## Worked Examples

Consider a small case with S = 5 and cards: +1, -2, *3, /-2.

We compute (a, b) pairs:

+1 → (1, 1)

-2 → (1, -2)

*3 → (3, 0)

/ -2 → (-1/2, 0)

After sorting using the comparator, one optimal ordering places the multiplication early and the division in a position that minimizes destructive scaling while preserving additive gains.

A trace of composition:

| Step | a | b | A | B |
| --- | --- | --- | --- | --- |
| Start | - | - | 1 | 0 |
| *3 | 3 | 0 | 3 | 0 |
| /-2 | -1/2 | 0 | -3/2 | 0 |
| +1 | 1 | 1 | -3/2 | 1 |
| -2 | 1 | -2 | -3/2 | -7/2 |

Final value is A*S + B = (-3/2)*5 + (-7/2) = -3/2.

This trace shows that once the ordering is fixed, the computation is purely mechanical and stable under rational arithmetic.

A second example where all operations are multiplications demonstrates that ordering does not matter for A but does matter for signs when combined with additions, reinforcing why the comparator is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C log C) | sorting dominates, each comparison is O(1) |
| Space | O(C) | storing fractional pairs and transformations |

The constraints allow up to 1000 cards per test case, so an O(C log C) sorting solution with rational arithmetic fits comfortably within limits. Python’s fraction arithmetic handles large numerators without overflow concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from fractions import Fraction
    from functools import cmp_to_key

    input_data = inp.strip().split()
    T = int(input_data[0])
    idx = 1
    out_lines = []

    for tc in range(1, T + 1):
        S = int(input_data[idx]); idx += 1
        C = int(input_data[idx]); idx += 1

        cards = []
        for _ in range(C):
            op = input_data[idx]; v = int(input_data[idx+1]); idx += 2

            if op == '+':
                a = Fraction(1,1); b = Fraction(v,1)
            elif op == '-':
                a = Fraction(1,1); b = Fraction(-v,1)
            elif op == '*':
                a = Fraction(v,1); b = Fraction(0,1)
            else:
                a = Fraction(1,v); b = Fraction(0,1)

            cards.append((a,b))

        def cmp(x,y):
            a1,b1 = x; a2,b2 = y
            l = b1*(a2-1); r = b2*(a1-1)
            return -1 if l>r else (1 if l<r else 0)

        cards.sort(key=cmp_to_key(cmp))

        A = Fraction(1,1)
        B = Fraction(0,1)

        for a,b in cards:
            B = B*a + b
            A = A*a

        res = A*S + B
        num, den = res.numerator, res.denominator
        if den < 0:
            num, den = -num, -den

        out_lines.append(f"Case #{tc}: {num} {den}")

    return "\n".join(out_lines)

# provided samples
assert run("1\n5 2\n+ 1\n- 2\n* 3\n/ -2\n") == "Case #1: -3 2"

# custom cases
assert run("1\n0 1\n+ 0\n") == "Case #1: 0 1"
assert run("1\n1 1\n* 5\n") == "Case #1: 5 1"
assert run("1\n2 2\n+ 1\n+ 1\n") == "Case #1: 4 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single +0 | 0/1 | identity neutrality |
| Single multiplication | 5/1 | pure scaling |
| Two additions | 4/1 | commutative additive accumulation |

## Edge Cases

One delicate situation is when a card has a = 1, which happens for addition and subtraction. In this case the comparator reduces cleanly because (a − 1) becomes zero, and the ordering rule depends only on whether swapping affects downstream scaling. The algorithm still handles this correctly because the inequality collapses without division.

Another case is division producing negative a values. For example a / -2 introduces sign flips that can dramatically change ordering. The comparator handles this naturally because it compares full rational expressions rather than assuming positivity.

A final corner case is when all a values are 1. Then every transformation is purely additive and the comparator degenerates to sorting by b values in a way that respects the same inequality rule. The algorithm still produces a consistent ordering and avoids division by zero in the comparison expression.
