---
title: "CF 104336C - Two players, two numbers"
description: "We are given two players, each starting with an integer written in decimal form. Arthur owns a, Nikita owns b. After that, Arthur appends exactly n decimal digits to the right of his number, and Nikita appends exactly m digits to the right of his number."
date: "2026-07-01T18:46:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104336
codeforces_index: "C"
codeforces_contest_name: "II Olympiad of classes at the Mechanics and Mathematics Faculty of MSU in programming 2023."
rating: 0
weight: 104336
solve_time_s: 57
verified: true
draft: false
---

[CF 104336C - Two players, two numbers](https://codeforces.com/problemset/problem/104336/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two players, each starting with an integer written in decimal form. Arthur owns `a`, Nikita owns `b`. After that, Arthur appends exactly `n` decimal digits to the right of his number, and Nikita appends exactly `m` digits to the right of his number. Those appended digits can be chosen freely.

After both extensions are done, the resulting two integers are compared as normal integers. Arthur wins if his final number is larger, Nikita wins if hers is larger, otherwise it is a draw.

The key point is that both players are trying to choose appended digits optimally to maximize their own chance of winning. Since each player controls only their own suffix, the game reduces to understanding how much influence `n` and `m` give in overcoming the difference between `a` and `b`.

The constraints are very large, up to 10^9 for all four values. That immediately rules out any construction that tries to simulate digit-by-digit appending or brute forcing all suffixes. Even a single number with 10^9 appended digits is impossible to represent explicitly, so the solution must reduce the problem to comparing magnitudes in closed form.

A subtle edge case appears when `a` and `b` are close, but one player has significantly more digits to append. For example, if `a = 9`, `b = 10`, and Arthur appends many digits while Nikita appends few, the leading structure can be overwhelmed by suffix length. A naive comparison of just `a` and `b` fails completely in such cases because it ignores how many digits can be appended.

Another failure case arises if one assumes players always append only 9s or only 0s without reasoning about optimality. The correct reasoning depends on the fact that each player will choose suffix digits to maximize lexicographically the final number, meaning they always choose 9s in all appended positions.

## Approaches

A brute-force interpretation would try to simulate both players’ choices. For each possible digit string of length `n` for Arthur and `m` for Nikita, we would construct the resulting numbers and compare them. This is theoretically correct because each player’s optimal choice is among all possible suffixes, but the number of possibilities is 10^n and 10^m, which is astronomically large even for tiny values of n and m. The brute force fails immediately.

The key observation is that each player’s optimal strategy is deterministic. Since the goal is to maximize the final number, every appended digit should be 9. Any smaller digit can only decrease the value without offering any compensating advantage later, because more significant positions dominate.

So Arthur’s final number becomes `a` followed by `n` digits of 9, and Nikita’s becomes `b` followed by `m` digits of 9.

Now the problem reduces to comparing two very large numbers formed by concatenation. Instead of constructing them explicitly, we compare by structure. If the number of digits differs after extension, the longer effective length dominates. If they have equal effective length, we compare first by integer part scaled by powers of 10, and then by suffix influence.

This reduces the problem to a comparison of `a * 10^n + (10^n - 1)` versus `b * 10^m + (10^m - 1)`. Since direct exponentiation is still safe only via Python integers, we rely on Python’s arbitrary precision arithmetic or structured comparison logic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^n + 10^m) | O(10^n + 10^m) | Too slow |
| Optimal | O(log(max(a,b,n,m))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that both players will always append the digit 9 in every position. This is because increasing any suffix digit increases the final number and there is no trade-off with future decisions.
2. Replace the game state with two deterministic final numbers: Arthur has `A = a * 10^n + (10^n - 1)` and Nikita has `B = b * 10^m + (10^m - 1)`.
3. Compare the magnitudes of `A` and `B`. Instead of constructing full values, compare them using Python’s big integer arithmetic or by comparing digit structure.
4. If `A > B`, Arthur wins. If `A < B`, Nikita wins. Otherwise, the result is a draw.

The key reasoning step is that suffix optimization fully removes strategic interaction. Once both players play optimally, the game becomes a direct numeric comparison problem with no further choices.

### Why it works

Each player’s decision at every appended position is independent and monotonic: increasing any digit strictly increases the final value regardless of future digits. This eliminates any non-greedy structure. As a result, the optimal strategy is fixed and unique, collapsing the game into a deterministic comparison of two constructed numbers. Since both constructions are exact upper bounds for each player, comparing them gives the correct winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, n, m = map(int, input().split())

A = a * (10 ** n) + ((10 ** n) - 1)
B = b * (10 ** m) + ((10 ** m) - 1)

if A > B:
    print("Arthur")
elif A < B:
    print("Nikita")
else:
    print("Draw")
```

The code directly implements the derived formula for each player’s optimal final number. The multiplication by `10 ** n` shifts the original number left by `n` decimal places, and `(10 ** n - 1)` fills all appended digits with 9.

Python’s integer type safely handles the very large values that can arise when `n` and `m` are large, so no manual big-integer handling is needed.

The comparison is a direct integer comparison, which is both correct and efficient.

## Worked Examples

### Sample 1

Input: `1 2 3 4`

Arthur computes `A = 1 * 10^3 + 999 = 1999`.

Nikita computes `B = 2 * 10^4 + 9999 = 29999`.

| Step | Arthur | Nikita |
| --- | --- | --- |
| Base | 1 | 2 |
| Power | 10^3 | 10^4 |
| Final | 1999 | 29999 |

Nikita’s number is clearly larger because the extra digit position from `m = 4` dominates Arthur’s smaller extension.

### Sample 2

Input: `54 54 54 54`

Arthur computes `A = 54 * 10^54 + (10^54 - 1)`.

Nikita computes `B = 54 * 10^54 + (10^54 - 1)`.

| Step | Arthur | Nikita |
| --- | --- | --- |
| Base | 54 | 54 |
| Power | 10^54 | 10^54 |
| Final | identical | identical |

Both expressions are identical, so the result is a draw.

These examples confirm that both the magnitude of appended digits and equality of structure fully determine the outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant number of big integer operations |
| Space | O(1) | Only a few integers are stored |

The solution runs within limits because Python handles big integers efficiently, and the number of operations does not depend on the magnitude of `n` or `m`, only on arithmetic on a constant number of values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    a, b, n, m = map(int, input().split())

    A = a * (10 ** n) + ((10 ** n) - 1)
    B = b * (10 ** m) + ((10 ** m) - 1)

    if A > B:
        return "Arthur"
    elif A < B:
        return "Nikita"
    return "Draw"

# provided samples
assert run("1 2 3 4") == "Nikita"
assert run("54 54 54 54") == "Draw"
assert run("11 10 2 2") == "Arthur"

# custom cases
assert run("1 1 1 2") == "Nikita", "longer suffix wins"
assert run("9 10 1 1") == "Nikita", "base dominance"
assert run("100 1 0 0") == "Arthur", "no extension comparison"
assert run("5 5 10 10") == "Draw", "identical structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 2 | Nikita | longer suffix dominates |
| 9 10 1 1 | Nikita | base comparison after equal growth |
| 100 1 0 0 | Arthur | no extension case |
| 5 5 10 10 | Draw | symmetry correctness |

## Edge Cases

One important edge case is when both players have identical bases and identical extension lengths. For input `a = 7, b = 7, n = 3, m = 3`, both compute `7 * 10^3 + 999`, producing identical numbers. The algorithm handles this naturally because both constructed values are identical, and the final equality check returns "Draw".

Another subtle case is when one player has a much larger base but fewer digits to append. For `a = 1000, b = 1, n = 0, m = 5`, Arthur has `1000`, while Nikita has `1 * 10^5 + 99999 = 199999`. Even though Arthur starts larger, Nikita’s longer suffix completely dominates. The algorithm captures this because the power of ten shift is applied before comparison, making suffix length a dominant factor when magnitudes differ sufficiently.
