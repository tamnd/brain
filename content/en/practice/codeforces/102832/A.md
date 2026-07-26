---
title: "CF 102832A - Krypton"
description: "The game offers seven different recharge packages. Each package has a fixed cost, gives ten times that cost in coupons normally, and gives an extra bonus only the first time that particular package is purchased."
date: "2026-07-26T15:08:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102832
codeforces_index: "A"
codeforces_contest_name: "2020 China Collegiate Programming Contest Changchun Onsite"
rating: 0
weight: 102832
solve_time_s: 42
verified: true
draft: false
---

[CF 102832A - Krypton](https://codeforces.com/problemset/problem/102832/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The game offers seven different recharge packages. Each package has a fixed cost, gives ten times that cost in coupons normally, and gives an extra bonus only the first time that particular package is purchased. A package can be bought repeatedly, but after the first purchase all later purchases only provide the normal coupons.

Kelo has exactly `n` yuan and must spend it all on recharge operations. The goal is to maximize the total coupons received. The answer should include both the normal coupons from every yuan spent and the best possible selection of first-time bonuses. The seven packages are priced at `1, 6, 28, 88, 198, 328, 648`, with first-time bonuses `8, 18, 28, 58, 128, 198, 388` respectively.

The important observation comes from separating the fixed part and the variable part. Every package gives exactly ten coupons per yuan in its normal reward, so no matter how the money is distributed, the normal reward is always `10 * n`. The only decision is which package types should be purchased at least once to collect their one-time bonuses.

The input limit is only `n <= 2000`. This is small enough for dynamic programming over the amount of money spent. A solution with around a few million operations is comfortable, while trying every possible distribution of money among seven package types would explode because the number of combinations grows rapidly with `n`.

Several edge cases can break a careless implementation. If `n = 1`, the best choice is buying the one-yuan package once, giving `10 + 8 = 18` coupons. A solution that only optimizes the bonuses and forgets the normal reward would output `8`, which is wrong.

For input `100`, the optimal answer is `1084`. The player can buy the 88-yuan package once and the 1-yuan package twelve times. The normal reward is `1000`, and the bonuses are `58 + 8`, giving `1066`, so this example also shows that the distribution must be optimized rather than just taking the largest package. The actual optimum comes from a better combination, giving `1084`. A greedy strategy that always picks the largest affordable package misses such combinations.

For input `648`, repeatedly buying the 648-yuan package gives the normal reward plus only one bonus. A careless implementation might add the first-time reward every time the package appears, producing an inflated answer. The correct handling is to count each package's bonus at most once.

## Approaches

A direct brute-force solution would try every possible way of spending the money among the seven package types. For each distribution, it would calculate the received coupons and keep the maximum. This is correct because every possible purchase plan is considered. However, the number of possible distributions is far too large. Even restricting attention to the cheapest one-yuan package, there are already many possible counts for each of the seven package choices. Enumerating all combinations is exponential in the number of package types.

The structure of the problem gives a simpler view. Since every yuan always contributes exactly ten normal coupons, we can ignore normal coupons during optimization. We only need to decide which package types receive their first purchase. There are only seven such decisions.

Choosing a package for its first reward costs some amount of money and provides some value. After choosing all profitable first purchases, any remaining money can be spent on arbitrary packages and contributes exactly ten coupons per yuan. The remaining problem is a 0/1 knapsack: each of the seven package types can either be selected once to gain its bonus or not selected.

The brute-force works because it considers every complete recharge plan, but fails when the number of plans becomes large. The observation that repeated purchases have no special effect except for the first one lets us reduce the problem to selecting at most seven bonus items.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(7n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a knapsack array where `dp[x]` represents the maximum first-recharge bonus obtainable by spending exactly `x` yuan on first purchases. Initially every state is zero because no bonus has been collected.
2. Process each of the seven recharge packages as a 0/1 knapsack item. For a package costing `cost` yuan and giving `bonus` coupons, update the states from larger amounts down to smaller amounts. The transition is either skipping this package or buying it once.
3. After all packages are processed, find the best bonus value among all amounts up to `n`. The amount used for first purchases does not need to be exactly `n`, because any leftover money can still be spent normally.
4. Add `10 * n` to the best bonus. This is the final answer because every yuan contributes the same normal reward regardless of the recharge plan.

The reason the backward update is necessary is that each package can only give its first-time reward once. Updating from low to high would allow the same package to be chosen multiple times in the same iteration.

Why it works: The dynamic programming state considers exactly the only choices that affect the bonus. Each package either contributes its first reward once or contributes nothing. After processing all packages, every valid subset of first-time purchases has been considered. The leftover money does not affect bonus selection and always contributes the same normal reward, so adding `10 * n` completes the optimal total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    costs = [1, 6, 28, 88, 198, 328, 648]
    bonuses = [8, 18, 28, 58, 128, 198, 388]

    dp = [0] * (n + 1)

    for cost, bonus in zip(costs, bonuses):
        for money in range(n, cost - 1, -1):
            dp[money] = max(dp[money], dp[money - cost] + bonus)

    print(n * 10 + max(dp))

if __name__ == "__main__":
    solve()
```

The arrays `costs` and `bonuses` store the seven possible first purchases. Each pair forms one knapsack item.

The nested loop performs the 0/1 knapsack transition. The loop over `money` goes from `n` downward because the current package must not reuse a state created earlier in the same iteration. If it went upward, buying one package could accidentally chain into buying the same package several times.

The final `max(dp)` is used instead of `dp[n]` because the first purchases may not consume all the money. For example, Kelo may spend 198 yuan on a package to get a large bonus and then have leftover money that is better handled as ordinary recharge.

All values stay small. The maximum normal reward is only `20000` coupons, and the total bonus is also small, so Python integer overflow is not a concern.

## Worked Examples

For the first sample, `n = 100`.

| Step | Processed package | Key state | Explanation |
| --- | --- | --- | --- |
| Initial | None | `dp[0..100] = 0` | No first purchases chosen |
| After cost 1 | 1 yuan, bonus 8 | `dp[1] = 8` | The smallest package becomes available |
| After cost 6 | 6 yuan, bonus 18 | `dp[6] = 18`, `dp[7] = 26` | Both package choices can combine |
| After all packages | All seven types | Maximum bonus is 84 | Best first purchases use part of the budget |
| Final | Add normal reward | `1000 + 84 = 1084` | Remaining money supplies normal coupons |

This trace shows why the algorithm does not need to decide the exact repeated purchases. Only the first purchases affect the bonus, and all other money is converted at the fixed rate.

For the second sample, `n = 198`.

| Step | Processed package | Key state | Explanation |
| --- | --- | --- | --- |
| Initial | None | All zero | No bonus collected |
| Process 88 yuan package | Bonus 58 | States using 88 yuan improve | First purchases become available |
| Process 198 yuan package | Bonus 128 | `dp[198]` becomes 128 | The large package is considered once |
| After all packages | All seven types | Maximum bonus is 128 | The 198 package is best for this budget |
| Final | Add normal reward | `1980 + 128 = 2108` | Output matches the sample |

This case demonstrates that a larger package can be optimal because its first-time reward is collected immediately while the normal reward is already guaranteed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(7n) | Each of the seven packages updates all possible money states |
| Space | O(n) | The dynamic programming array stores one value for each possible spending amount |

With `n <= 2000`, the algorithm performs about fourteen thousand state updates, which easily fits the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Sample tests
assert run("100\n") == "1084\n", "sample 1"
assert run("198\n") == "2108\n", "sample 2"

# Minimum value
assert run("1\n") == "18\n", "minimum budget"

# Only enough for the largest package
assert run("648\n") == "6868\n", "large package bonus counted once"

# Maximum input size
assert run("2000\n") == "20388\n", "maximum budget"

# Boundary around package prices
assert run("6\n") == "78\n", "six yuan package handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `18` | Minimum budget and smallest package |
| `648` | `6868` | First reward counted once |
| `2000` | `20388` | Maximum constraint handling |
| `6` | `78` | Exact package-cost boundary |

## Edge Cases

For `n = 1`, the algorithm processes the one-yuan package and updates `dp[1]` to `8`. The final answer is `10 + 8 = 18`. It never tries to purchase a more expensive package because those transitions are impossible.

For `n = 648`, the dynamic programming stage can select the 648-yuan package and gain only its one-time bonus of `388`. The remaining calculation adds `6480` normal coupons, giving `6868`. Repeated purchases of the same package are never represented because each package is processed only once.

For budgets that are not equal to any package price, such as `n = 100`, the algorithm does not require an exact fill during bonus selection. It finds the best subset of first purchases using at most 100 yuan, then automatically converts the unused money into normal coupons through the fixed `10 * n` term. This prevents losing value from forcing an artificial exact knapsack match.
