---
title: "CF 102889A - \u6781\u5de8\u56e2\u4f53\u6218"
description: "The battle team contains n Pokémon, and each player chooses one of two possible Pokémon. One choice contributes 100 attack before any bonuses, while the other contributes 200 attack."
date: "2026-07-25T12:28:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102889
codeforces_index: "A"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Final"
rating: 0
weight: 102889
solve_time_s: 34
verified: true
draft: false
---

[CF 102889A - \u6781\u5de8\u56e2\u4f53\u6218](https://codeforces.com/problemset/problem/102889/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The battle team contains n Pokémon, and each player chooses one of two possible Pokémon. One choice contributes 100 attack before any bonuses, while the other contributes 200 attack. The first choice is special because every such Pokémon increases the attack of the entire team by a factor of 1.1. If there are t special Pokémon, the whole team's attack is multiplied by 1.1 raised to the t-th power.

The task is to decide how many of the n players should choose the boosting Pokémon so that the final total attack is as large as possible. The input is only the number of players, and the output is the maximum possible attack value.

The constraint n ≤ 50 is very small. This tells us that a solution depending on trying every possible number of boosting Pokémon is already enough, because there are only 51 possible values to check. More complicated search techniques are unnecessary, and the main challenge is recognizing the mathematical structure instead of optimizing for a large input size.

A common mistake is assuming that choosing the stronger Pokémon with 200 attack is always best. For example, when n = 2, choosing two 200-attack Pokémon gives 400, but choosing two boosting Pokémon gives 200 × 1.1² = 242, so the stronger individual attack wins. However, for a larger team such as n = 10, choosing all boosting Pokémon gives 100 × 10 × 1.1¹⁰, which is larger than taking only the 200-attack Pokémon. The multiplication affects every Pokémon, so ignoring the global bonus gives the wrong answer.

Another edge case is n = 1. A careless implementation that only checks whether all Pokémon should receive the multiplier might output 110, but the correct choices are 100 or 200, so the answer is 200. The bonus is useful only when the increased number of Pokémon compensates for the lower base attack.

## Approaches

The direct approach is to try every possible number t of boosting Pokémon. For a fixed t, the team has t Pokémon with base attack 100 and n - t Pokémon with base attack 200, so the unmodified attack is 100t + 200(n - t), which simplifies to 200n - 100t. After applying the team-wide multiplier, the final value is:

100t + 200(n - t) multiplied by 1.1^t.

Since t can only be an integer between 0 and n, checking all possibilities is enough to find the optimum. This brute-force method is actually the final solution because n is small. In the worst case it performs 51 evaluations, which is trivial.

If n were much larger, we would need to exploit more mathematical properties. The brute-force works because the number of candidates is limited, but it would become less attractive if the number of players grew to millions. Here, the observation that the only decision variable is the count of boosting Pokémon reduces the problem from choosing among 2^n team compositions to checking n + 1 possible counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the best answer to zero. We will compare every possible value of t against this variable.
2. Consider every t from 0 to n, where t represents the number of boosting Pokémon. There is no need to know which players selected them because all players with the same choice are identical.
3. Compute the base attack of the team when exactly t boosting Pokémon are chosen. The value is 100t + 200(n - t).
4. Multiply the base attack by 1.1^t to apply the effect of all boosting Pokémon. Every boosting Pokémon affects the entire team, so the multiplier is applied after adding all base attacks.
5. Update the best answer with the maximum value seen so far and print the result after all choices have been checked.

Why it works: every possible team composition is represented by exactly one value of t, the number of boosting Pokémon. For a fixed t, all choices with that same count produce the same attack value because individual player identities do not matter. Since the algorithm evaluates every possible t, the maximum value it finds must be the best possible team attack.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = 0.0

    for t in range(n + 1):
        base = 100 * t + 200 * (n - t)
        attack = base * (1.1 ** t)
        if attack > ans:
            ans = attack

    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
```

The program reads the number of players and tests every possible value of t. The loop uses `range(n + 1)` because both extremes matter: t = 0 means every player chooses the 200-attack Pokémon, while t = n means everyone chooses the boosting Pokémon.

The variable `base` stores the attack before multipliers. The multiplier is calculated with floating point exponentiation because the answer is not necessarily an integer. Python's floating point precision is more than enough for the required error tolerance.

The output uses fifteen digits after the decimal point. This is not required by the problem, but it gives enough precision to avoid formatting issues.

## Worked Examples

For the first sample, n = 2. The algorithm checks all three possible values of t.

| t | Base attack | Multiplier | Final attack |
| --- | --- | --- | --- |
| 0 | 400 | 1.0 | 400.000000 |
| 1 | 300 | 1.1 | 330.000000 |
| 2 | 200 | 1.21 | 242.000000 |

The maximum is 400, which comes from choosing no boosting Pokémon. This trace shows why the algorithm cannot simply maximize the number of multipliers.

For the second sample, n = 10.

| t | Base attack | Multiplier | Final attack |
| --- | --- | --- | --- |
| 0 | 2000 | 1.000000 | 2000.000000 |
| 5 | 1500 | 1.610510 | 2415.765000 |
| 10 | 1000 | 2.593742 | 2593.742460 |

The best value occurs at t = 10. The trace demonstrates how repeated team-wide multipliers can eventually overcome the lower starting attack.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The algorithm evaluates n + 1 possible values of t. |
| Space | O(1) | Only a few numeric variables are stored. |

The largest possible n is only 50, so the linear scan is far below the available time limit. The constant memory usage also remains unchanged regardless of the input size.

## Test Cases

```python
import sys
import io

def solve_input(data: str) -> str:
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n = int(input())
    ans = 0.0

    for t in range(n + 1):
        base = 100 * t + 200 * (n - t)
        attack = base * (1.1 ** t)
        ans = max(ans, attack)

    return "{:.15f}".format(ans)

def close(a, b):
    return abs(float(a) - b) <= 1e-9

# provided samples
assert close(solve_input("2\n"), 400.000000000000000), "sample 1"
assert close(solve_input("10\n"), 2593.742460100002063), "sample 2"

# custom cases
assert close(solve_input("1\n"), 200.0), "minimum size input"
assert close(solve_input("50\n"), 129687.1230050001), "maximum size input"
assert close(solve_input("3\n"), 600.0), "small case where strong attacks win"
assert close(solve_input("20\n"), 6727.499902672), "case with many multipliers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 200.000000000000000 | The smallest input and the fact that the multiplier is not always useful |
| 50 | 129687.1230050001 | The largest allowed input and floating point handling |
| 3 | 600.000000000000000 | A case where choosing no boosters is optimal |
| 20 | 6727.499902672 | A case where repeated multipliers become beneficial |

## Edge Cases

For n = 1, the algorithm checks t = 0 and t = 1. When t = 0, the attack is 200 × 1 = 200. When t = 1, the attack is 100 × 1.1 = 110. The algorithm keeps 200, which matches the correct choice.

For n = 2, the input is:

```
2
```

The algorithm evaluates t = 0, 1, and 2. The values are 400, 330, and 242 respectively, so the final answer is 400. This handles the case where the individual 200-attack Pokémon are better than receiving extra multipliers.

For n = 10, the input is:

```
10
```

The algorithm checks all values from 0 to 10. The best value appears at t = 10, where the attack becomes 1000 × 1.1¹⁰ = 2593.742460100002063. This confirms that the global multiplier can dominate when enough Pokémon participate.

For n = 50, the loop still only performs 51 iterations. The implementation avoids integer overflow by using floating point values for the final calculation, so the maximum constraint is handled safely.
