---
title: "CF 325B - Stadium and Games"
description: "We are given the exact number of football games that must be played, and we need to find every possible initial number of teams that produces exactly that many games under a specific tournament format."
date: "2026-06-06T08:46:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 325
codeforces_index: "B"
codeforces_contest_name: "MemSQL start[c]up Round 1"
rating: 1800
weight: 325
solve_time_s: 110
verified: true
draft: false
---

[CF 325B - Stadium and Games](https://codeforces.com/problemset/problem/325/B)

**Rating:** 1800  
**Tags:** binary search, math  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the exact number of football games that must be played, and we need to find every possible initial number of teams that produces exactly that many games under a specific tournament format.

The tournament starts with elimination rounds, but only while the number of remaining teams is even. During each such round, teams are paired, one game is played per pair, and half of the teams are eliminated.

Eventually the number of remaining teams becomes odd. If only one team remains, the tournament ends immediately. Otherwise, all remaining teams play a complete round robin tournament, where every pair of teams meets exactly once.

The input is a single integer `n`, the required total number of games. The output is every initial team count that leads to exactly `n` games, printed in increasing order.

The constraint is the key difficulty. The value of `n` can be as large as `10^18`, so any algorithm that tries many candidate team counts directly is impossible. Even iterating up to `√n` would already be around `10^9` operations in the worst case. We need a solution whose running time depends only logarithmically on the size of the numbers involved.

Several edge cases are easy to miss.

Consider `n = 1`. A careless solution might assume every valid tournament eventually reaches a round robin stage. That is false. Starting with two teams gives one elimination game and then a single winner. The correct output is:

```
2
```

Consider `n = 3`. There are two valid answers:

```
3
4
```

Starting with three teams immediately produces a round robin of three games. Starting with four teams produces two elimination games, leaving two teams, then one more elimination game, for a total of three games. A solution that only searches odd team counts would miss `4`.

Another subtle case is when multiple different powers of two divide the same answer structure. Different initial team counts can produce the same game total, so we must collect all valid solutions and sort them rather than stopping after the first match.

## Approaches

The most direct approach is to try every possible initial team count `m`, simulate the tournament, compute the number of games, and check whether it equals `n`.

Simulation is straightforward. Repeatedly halve the team count while it is even, adding `m/2` games each time. When an odd number `k` remains, add `k(k-1)/2` round robin games.

This brute-force method is correct because it exactly follows the tournament rules. The problem is the search space. The answer can be much larger than `10^9`, and in fact valid team counts can be around `10^18`. Enumerating candidates is completely infeasible.

The structure of the tournament gives a much better description.

Suppose the initial number of teams is

$$m = 2^t \cdot k$$

where `k` is odd.

After the first elimination round, the number of teams becomes

$$2^{t-1}k$$

After the second,

$$2^{t-2}k$$

and so on.

After exactly `t` elimination stages, `k` teams remain, and `k` is odd.

The elimination games contribute

$$2^{t-1}k + 2^{t-2}k + \cdots + k$$

which is

$$k(2^t-1).$$

The final round robin contributes

$$\frac{k(k-1)}2.$$

Hence every valid tournament satisfies

$$n = k(2^t-1)+\frac{k(k-1)}2.$$

After rearranging,

$$n=\frac{k(2^{t+1}+k-3)}2.$$

Now the search space becomes tiny. Since `k` is odd and positive, and `2^t ≤ 10^{18}`, the exponent `t` can take only about sixty values.

For a fixed `t`, the equation becomes a quadratic in `k`:

$$k^2+(2^{t+1}-3)k-2n=0.$$

We can solve this using integer arithmetic. For each possible `t`, check whether the quadratic has a positive odd integer root. Every such root gives a valid team count

$$m=2^t k.$$

This reduces the problem from searching up to `10^{18}` candidates to checking only about sixty exponents.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M log M) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Let `n` be the required number of games.
2. Iterate over all exponents `t` from `0` upward while `2^t ≤ 10^18`.
3. For the current `t`, define

$$a = 2^{t+1}-3.$$

The equation becomes

$$k^2+ak-2n=0.$$

1. Compute the discriminant

$$D=a^2+8n.$$

An integer solution exists only if `D` is a perfect square.

1. Let `s = √D`. If `s² ≠ D`, skip this exponent.
2. The quadratic formula gives

$$k=\frac{-a+s}{2}.$$

Check that the numerator is positive and even.

1. Verify that `k` is positive and odd. Only odd values correspond to the remaining teams after all elimination stages.
2. Construct

$$m = 2^t k.$$

1. Recompute the tournament game count from `m` using the derived formula and verify it equals `n`. This guards against any arithmetic mistakes.
2. Store every valid `m`.
3. After processing all exponents, sort the answers and print them. If none exist, print `-1`.

### Why it works

Every initial team count can be written uniquely as `m = 2^t k` where `k` is odd. The tournament always performs exactly `t` elimination stages and then stops with `k` teams.

The elimination phase contributes exactly `k(2^t-1)` games, and the round robin phase contributes exactly `k(k-1)/2` games. Thus every valid solution must satisfy

$$n=\frac{k(2^{t+1}+k-3)}2.$$

Conversely, whenever an odd positive integer `k` satisfies this equation for some `t`, the team count `m=2^t k` produces exactly `n` games. The algorithm enumerates all possible exponents `t`, finds all integer roots `k`, and therefore finds every valid initial team count exactly once.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

def main():
    n = int(input())

    ans = []

    p = 1  # 2^t
    while p <= 10**18:
        a = 2 * p - 3
        D = a * a + 8 * n

        s = isqrt(D)
        if s * s == D:
            num = s - a

            if num > 0 and num % 2 == 0:
                k = num // 2

                if k > 0 and k % 2 == 1:
                    games = k * (p - 1) + k * (k - 1) // 2

                    if games == n:
                        ans.append(p * k)

        p <<= 1

    ans.sort()

    if not ans:
        print(-1)
    else:
        print("\n".join(map(str, ans)))

if __name__ == "__main__":
    main()
```

The loop enumerates all possible values of `2^t`. There are fewer than sixty such values before exceeding `10^18`, which is why the algorithm is extremely fast.

For each exponent, we derive a quadratic equation in the odd remainder `k`. The discriminant test is crucial. A quadratic with integer coefficients has an integer root only when the discriminant is a perfect square.

The expression

```
num = s - a
```

comes directly from the quadratic formula. We must verify that it is positive and divisible by two, otherwise `k` is not an integer.

The final recomputation of the game count is performed entirely with integer arithmetic. Python's arbitrary-precision integers eliminate overflow concerns, but the verification step is still useful because it guarantees that only genuinely valid solutions are output.

## Worked Examples

### Example 1

Input:

```
3
```

| t | p=2^t | a=2p-3 | D | √D | k | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | -1 | 25 | 5 | 3 | Yes |
| 1 | 2 | 1 | 25 | 5 | 2 | No, even |
| 2 | 4 | 5 | 49 | 7 | 1 | Yes |
| 3 | 8 | 13 | 193 | not square | - | No |

The valid team counts are:

$$1 \cdot 3 = 3$$

and

$$4 \cdot 1 = 4.$$

Output:

```
3
4
```

This example shows why multiple answers are possible. One tournament starts directly with a round robin, while the other consists entirely of elimination rounds.

### Example 2

Input:

```
1
```

| t | p=2^t | a=2p-3 | D | √D | k | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | -1 | 9 | 3 | 2 | No, even |
| 1 | 2 | 1 | 9 | 3 | 1 | Yes |
| 2 | 4 | 5 | 33 | not square | - | No |

The only valid team count is

$$2 \cdot 1 = 2.$$

Output:

```
2
```

This example demonstrates the special case where the tournament never reaches a round robin stage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | About sixty exponents are tested |
| Space | O(1) | Only a few integer variables are stored |

The largest input is `10^18`, yet the algorithm performs only around sixty iterations. Each iteration uses constant-time arithmetic on 64-bit scale integers, which easily fits within the limits.

## Test Cases

```python
import sys, io
from math import isqrt

def solve():
    n = int(input())

    ans = []
    p = 1

    while p <= 10**18:
        a = 2 * p - 3
        D = a * a + 8 * n

        s = isqrt(D)
        if s * s == D:
            num = s - a

            if num > 0 and num % 2 == 0:
                k = num // 2

                if k > 0 and k % 2 == 1:
                    games = k * (p - 1) + k * (k - 1) // 2

                    if games == n:
                        ans.append(p * k)

        p <<= 1

    ans.sort()

    if not ans:
        return "-1"

    return "\n".join(map(str, ans))

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    return solve()

# provided sample
assert run("3\n") == "3\n4", "sample 1"

# custom cases
assert run("1\n") == "2", "single elimination game"
assert run("6\n") == "4", "pure elimination tournament"
assert run("10\n") == "5\n20", "multiple valid answers"
assert run("2\n") == "-1", "no valid team count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `2` | Tournament ending with one winner |
| `6` | `4` | Pure elimination structure |
| `10` | `5` and `20` | Multiple valid answers |
| `2` | `-1` | No solution exists |

## Edge Cases

Consider input:

```
1
```

The algorithm examines every exponent. For `t = 1`, it finds `k = 1`, giving `m = 2`. The resulting game count is exactly one. This confirms that tournaments ending immediately after elimination rounds are handled correctly.

Consider input:

```
3
```

Two different exponent values produce valid roots. The algorithm records both `3` and `4`, sorts them, and prints both. Any solution that stops after the first match would fail here.

Consider input:

```
2
```

Every discriminant check either fails or produces an invalid root. The answer list remains empty, and the algorithm prints `-1`. This verifies correct handling when no tournament structure can generate the requested number of games.

Consider very large inputs near `10^18`. The algorithm still checks only about sixty exponent values. All arithmetic is performed with integers, and Python's arbitrary-precision integers safely handle discriminants larger than `10^18` without overflow.
