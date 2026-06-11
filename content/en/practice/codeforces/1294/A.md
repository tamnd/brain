---
title: "CF 1294A - Collecting Coins"
description: "We are asked to decide whether a given number of coins can be distributed among three sisters so that they all end up with the same total number of coins. Each sister already has some coins: Alice has a, Barbara has b, and Cerene has c."
date: "2026-06-11T18:40:03+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1294
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 615 (Div. 3)"
rating: 800
weight: 1294
solve_time_s: 109
verified: true
draft: false
---

[CF 1294A - Collecting Coins](https://codeforces.com/problemset/problem/1294/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decide whether a given number of coins can be distributed among three sisters so that they all end up with the same total number of coins. Each sister already has some coins: Alice has `a`, Barbara has `b`, and Cerene has `c`. Polycarp brings `n` extra coins, and he can give each sister any non-negative number of these coins. The question is whether there exists a way to distribute all `n` coins so that `a + A = b + B = c + C`, where `A + B + C = n` and `A, B, C ≥ 0`.

Each test case is independent, and the numbers can be as large as 10^8, with up to 10^4 test cases. This tells us that any solution that loops over all possible distributions of coins is far too slow. We need an approach that is O(1) per test case.

Edge cases to watch for include scenarios where one sister already has far more coins than the others, or where the total number of coins needed to balance them exactly does not divide evenly. For instance, if the sisters have 1, 2, 3 coins and `n = 3`, a naive approach that simply adds coins one by one might incorrectly assume it is possible, but careful calculation shows that you cannot distribute 3 coins to make all totals equal because the largest gap is 2 and you cannot split the remainder evenly.

## Approaches

A brute-force method would try every combination of `(A, B, C)` such that `A + B + C = n`. This would work in principle because we only need to check integer solutions, but the number of possibilities grows cubically with `n`. Given that `n` can be 10^8, this is obviously infeasible.

The key insight is that we do not need to try all distributions. Let `max_coins` be the largest number of coins any sister currently has. To equalize them, we must at least bring the other two sisters up to `max_coins`. Let the total number of coins needed to reach that level be `(max_coins - a) + (max_coins - b) + (max_coins - c)`. If this number exceeds `n`, it is impossible.

If we have enough coins, the remaining coins after equalizing to `max_coins` must be divisible by 3. This is because any extra coins beyond the baseline must be distributed equally to maintain equality among all three sisters. This two-step check - first ensuring we have enough coins to reach `max_coins`, then checking divisibility by 3 - reduces the problem to a simple constant-time calculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, identify the maximum number of coins any sister currently has: `max_coins = max(a, b, c)`. This represents the minimum target we must reach for all sisters.
2. Compute the total number of coins required to bring each sister up to `max_coins`: `needed = (max_coins - a) + (max_coins - b) + (max_coins - c)`. This accounts for the baseline to equalize all three.
3. Check if the coins Polycarp brings (`n`) are sufficient: if `needed > n`, output "NO". The distribution is impossible.
4. If there are enough coins, calculate the remaining coins: `extra = n - needed`. These must be divisible by 3 to split evenly among three sisters. If `extra % 3 == 0`, output "YES"; otherwise, output "NO".

**Why it works:** The invariant is that after step 2, all sisters have been brought to at least `max_coins`. Any leftover coins must be divisible by three to maintain equality. There are no other constraints, so this check guarantees correctness. There is no need for further iterations or complicated distributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, n = map(int, input().split())
    max_coins = max(a, b, c)
    needed = (max_coins - a) + (max_coins - b) + (max_coins - c)
    if n < needed:
        print("NO")
    else:
        extra = n - needed
        print("YES" if extra % 3 == 0 else "NO")
```

The code reads multiple test cases efficiently using `sys.stdin.readline`. The `max` function quickly finds the highest starting coin count. We compute the coins required to balance everyone and check for feasibility and divisibility in two simple conditions. Using integer arithmetic ensures no rounding errors, and there are no off-by-one issues because all calculations are exact.

## Worked Examples

**Sample Input 1:** `5 3 2 8`

| a | b | c | n | max_coins | needed | extra | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 3 | 2 | 8 | 5 | 5 | 3 | YES |

Explanation: Bring Barbara from 3→5 and Cerene from 2→5. `needed = 5`. Remaining `n - needed = 3` can be split equally to give each sister one more coin, achieving equality.

**Sample Input 2:** `3 2 1 100000000`

| a | b | c | n | max_coins | needed | extra | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 2 | 1 | 100000000 | 3 | 3 | 99999997 | NO |

Explanation: We bring everyone to 3. `needed = 3`. `extra = 99999997` is not divisible by 3, so we cannot split it evenly among three sisters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations per case, no loops over `n` |
| Space | O(1) | Only a few integer variables used |

Given `t ≤ 10^4`, this algorithm easily runs within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b, c, n = map(int, input().split())
        max_coins = max(a, b, c)
        needed = (max_coins - a) + (max_coins - b) + (max_coins - c)
        if n < needed:
            print("NO")
        else:
            extra = n - needed
            print("YES" if extra % 3 == 0 else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("5\n5 3 2 8\n100 101 102 105\n3 2 1 100000000\n10 20 15 14\n101 101 101 3\n") == \
"YES\nYES\nNO\nNO\nYES", "sample 1"

# Custom cases
assert run("1\n1 1 1 0\n") == "YES", "all equal, no extra coins"
assert run("1\n1 2 3 3\n") == "YES", "small numbers, divisible extra"
assert run("1\n1 2 3 2\n") == "NO", "small numbers, insufficient extra"
assert run("1\n100000000 100000000 100000000 3\n") == "YES", "max input, small extra divisible"
assert run("1\n1 1 1 2\n") == "NO", "all equal, extra not divisible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 0 | YES | No extra coins, already equal |
| 1 2 3 3 | YES | Enough coins to equalize and divisible |
| 1 2 3 2 | NO | Insufficient coins to equalize |
| 100000000 100000000 100000000 3 | YES | Handles maximum input values |
| 1 1 1 2 | NO | Extra coins not divisible by 3 |

## Edge Cases

When all sisters already have equal coins, such as `a = b = c = 1` and `n = 0`, `needed = 0` and `extra = 0`. The divisibility check passes, so output is "YES". If `n = 2` instead, `extra = 2` is not divisible by 3, so output is "NO". This demonstrates the algorithm correctly handles cases with no distribution required or non-divisible leftover coins.

When the coins are extremely unbalanced, such as `a = 1, b = 2, c = 100000000` and `n
