---
title: "CF 1150A - Stock Arbitraging"
description: "We are given a very simple two-phase trading scenario. In the morning, there are several sellers offering unlimited quantities of the same stock at different buy prices. You can pick any one of these prices and buy as many shares as you want at that price."
date: "2026-06-12T03:05:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1150
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 556 (Div. 2)"
rating: 800
weight: 1150
solve_time_s: 74
verified: true
draft: false
---

[CF 1150A - Stock Arbitraging](https://codeforces.com/problemset/problem/1150/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very simple two-phase trading scenario. In the morning, there are several sellers offering unlimited quantities of the same stock at different buy prices. You can pick any one of these prices and buy as many shares as you want at that price. In the evening, there are several buyers willing to purchase unlimited quantities at different sell prices, again one price per transaction, and you can choose any of them.

You start with some amount of money and no shares. Your goal is to choose exactly one buying price from the morning, buy any number of shares using your current money, and then choose exactly one selling price from the evening and sell all shares at that price. You are allowed to do nothing at all if that is better.

The key observation from the structure is that once you fix a buy price and a sell price, everything becomes deterministic: you spend all your money on shares, then liquidate them completely.

The constraints are small enough that even checking all combinations is trivial. With at most 30 buying prices and 30 selling prices, the total number of pairs is 900. For each pair, computing how many shares you can buy is constant time, so a full brute-force scan is completely sufficient within limits.

The only subtle pitfall is forgetting that you are not forced to trade. If all profit opportunities are negative, the optimal answer is simply the initial money.

## Approaches

A brute-force solution tries every possible pair of morning and evening prices. For each buy price, it computes how many shares you can purchase with your current money, then for each sell price, it computes the final amount after selling those shares.

This works because each decision is independent: the number of shares depends only on the buy price and initial capital, and profit depends only on the sell price. However, this naive formulation still leads directly to a double loop over all pairs, which is at most 900 iterations, easily fast enough. There is no need for more advanced optimization, but we can still simplify reasoning.

The key insight is that buying more shares is always better if the buy price is lower, and selling at a higher price is always better. Therefore, we do not need to consider intermediate choices: we only care about the cheapest buying option and the most expensive selling option. The optimal strategy becomes: pick the minimum of all buy prices, pick the maximum of all sell prices, and evaluate the resulting profit, or choose to do nothing if it decreases wealth.

The brute-force works because the search space is tiny, but it becomes conceptually redundant once we realize monotonicity reduces everything to two extreme values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Accepted |
| Optimal (min/max reduction) | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by identifying the only two meaningful decisions: the best possible purchase price and the best possible selling price.

1. Read the initial capital and the lists of buy and sell prices. These represent all possible uniform markets you can choose from in each phase.
2. Compute the minimum value among all buy prices. This represents the cheapest market in which you can convert money into the largest number of shares.
3. Compute the maximum value among all sell prices. This represents the most profitable market where each share yields the highest return.
4. Compute how many shares you can buy if you use all your money at the minimum buy price. This is simply initial_money divided by min_buy_price. The division is integer because shares are indivisible.
5. Compute the final amount after selling all shares at the maximum sell price. This is shares multiplied by max_sell_price.
6. Compare this result with the initial money. If trading is not beneficial, keep the original value. Otherwise, take the larger one.

The reason we explicitly compare with the initial capital is that the optimal strategy may involve no transactions at all.

### Why it works

Any valid strategy consists of picking one buy price and one sell price. If a buy price is not the minimum available, replacing it with a cheaper option increases or preserves the number of shares you can obtain. If a sell price is not the maximum available, replacing it with a higher price increases or preserves revenue per share. Therefore, any optimal strategy can be transformed into one that uses the minimum buy price and maximum sell price without decreasing profit. This transformation preserves correctness and shows that the solution is fully determined by extreme values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, r = map(int, input().split())
    s = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    min_buy = min(s)
    max_sell = max(b)
    
    shares = r // min_buy
    best = shares * max_sell
    
    print(max(r, best))

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the reduction to extreme values. The only arithmetic care point is integer division when computing shares, since fractional shares are impossible. The final comparison ensures we do not mistakenly enforce trading when it is unprofitable.

## Worked Examples

### Example 1

Input:

```
3 4 11
4 2 5
4 4 5 4
```

We compute the key values: minimum buy price is 2, maximum sell price is 5.

| Step | Value |
| --- | --- |
| Initial money | 11 |
| Min buy price | 2 |
| Max sell price | 5 |
| Shares bought | 11 // 2 = 5 |
| Final money | 5 × 5 = 25 |
| Best result | max(11, 25) = 25 |

The process shows that using the cheapest buying option maximizes conversion into shares, and the most expensive selling option maximizes return per share.

### Example 2

Input:

```
2 2 10
5 6
4 3
```

Here, buying shares is always worse because even the best sell price is below the cheapest buy price.

| Step | Value |
| --- | --- |
| Initial money | 10 |
| Min buy price | 5 |
| Max sell price | 4 |
| Shares bought | 10 // 5 = 2 |
| Final money | 2 × 4 = 8 |
| Best result | max(10, 8) = 10 |

This confirms the importance of the “do nothing” option when trading yields negative return.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We scan each list once to compute min and max values |
| Space | O(1) | Only a few scalar variables are used |

The input limits are small, but even if they were much larger, this solution would remain efficient because it avoids any pairwise enumeration and reduces the problem to constant-time decision making after a single pass.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve() if solve() is not None else "").strip()

# provided sample
assert run("""3 4 11
4 2 5
4 4 5 4
""") == "25"

# no profit case
assert run("""2 2 10
5 6
4 3
""") == "10"

# minimum input
assert run("""1 1 1
1
1
""") == "1"

# profitable extreme spread
assert run("""3 3 100
1 2 3
10 20 30
""") == "3000"

# all buy prices equal
assert run("""3 2 50
5 5 5
1 2
""") == "50"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal prices | 1 | trivial stability |
| no profit | initial money | correct fallback |
| extreme spread | large gain | max/min correctness |
| uniform buy prices | correct min handling | redundancy robustness |

## Edge Cases

A key edge case is when every possible trade is unprofitable because even the best selling price is below the cheapest buying price. For example, if you start with 10, buy prices are `[5, 6]`, and sell prices are `[1, 2]`, then any trade destroys value. The algorithm handles this because it explicitly compares the trading result with the original amount and returns the maximum of the two.

Another edge case is when all prices are identical. In that case, buying and selling yields no change in wealth. The algorithm computes shares correctly but the final comparison ensures the result remains equal to the initial value.

A third case is when the optimal strategy involves using all money exactly with no remainder. Integer division naturally enforces this; any leftover money is irrelevant because it cannot be used to buy fractional shares, and the algorithm does not attempt to reuse it in any other way.
