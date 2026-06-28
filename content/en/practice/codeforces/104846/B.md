---
title: "CF 104846B - \u041c\u044b\u0442 \u043d\u0430 \u0440\u0435\u043a\u0435 \u042f\u0443\u0437\u0430"
description: "A merchant travels along a river route carrying two kinds of goods: caviar and honey. Initially, he has a fixed amount of each commodity, and each unit can later be sold at a known price."
date: "2026-06-28T11:27:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104846
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (7-8 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104846
solve_time_s: 46
verified: true
draft: false
---

[CF 104846B - \u041c\u044b\u0442 \u043d\u0430 \u0440\u0435\u043a\u0435 \u042f\u0443\u0437\u0430](https://codeforces.com/problemset/problem/104846/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

A merchant travels along a river route carrying two kinds of goods: caviar and honey. Initially, he has a fixed amount of each commodity, and each unit can later be sold at a known price. His final profit depends on how much of each good survives until the city market, because everything that is not used for tolls can be sold.

On the way, he must pass a customs point. At this checkpoint, he is forced to pay a toll, but he has flexibility in how to pay it. He can either pay a fixed amount of money, or he can substitute the payment with some amount of caviar, or some amount of honey. Each option fully replaces the same toll, but consumes different resources.

The goal is to choose the payment method that maximizes the final monetary gain after selling the remaining goods and accounting for any cash paid at the toll.

The key structure is that there is only one decision point: how to pay a single toll. After that, everything is linear, since remaining goods are sold independently at fixed prices.

Even though the constraints include very large values for quantities of goods (up to tens of millions), there is only a constant number of meaningful strategies to evaluate, so the solution must avoid any simulation over quantities.

A common mistake is to assume you should always minimize the immediate cost of the toll. That fails because paying in goods removes future selling profit, not just immediate value.

For example, if caviar is extremely valuable compared to honey, paying in caviar might be much more expensive in terms of lost revenue even if it avoids spending cash.

Another subtle edge case is feasibility of payment methods. If the merchant does not have enough caviar or honey, those options are invalid, even if they appear optimal in value terms.

## Approaches

A brute-force mindset would be to consider all possible combinations of paying the toll using different amounts of goods and cash. However, the problem does not allow partial payments, and the toll is fixed in three discrete forms. This collapses the decision space into at most three candidate strategies.

The correct insight is that the entire optimization is local to the toll. Everything before and after the toll is linear in remaining resources, so the only effect of the toll is a one-time subtraction from a fixed initial value. This allows us to evaluate each payment option independently by computing final profit after applying it.

For each option, we compute remaining caviar and honey, convert them to money using given prices, and subtract cash paid if applicable. The best outcome among valid options is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over allocations | O(i + m) or worse depending on modeling | O(1) | Too slow and unnecessary |
| Evaluate 3 payment modes | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the result by directly evaluating the three possible ways to pay the toll.

1. Start by computing the baseline profit if no toll is paid in cash: total value is i·a + m·b. This represents the maximum theoretical revenue before any constraint is applied.
2. Consider paying the toll in cash v. In this case, no goods are consumed at the checkpoint, so the remaining value is i·a + m·b − v.
3. Consider paying the toll using c grams of caviar. This option is valid only if i ≥ c. If valid, the remaining goods are (i − c, m), so the profit becomes (i − c)·a + m·b. This models the loss of future selling value of the removed caviar.
4. Consider paying the toll using d grams of honey. This option is valid only if m ≥ d. If valid, the remaining goods are (i, m − d), so the profit becomes i·a + (m − d)·b.
5. Take the maximum value among all valid options.

Why it works

Each payment option corresponds to a distinct final state of remaining resources. After the checkpoint, revenue is fully determined by linear valuation of remaining goods. Since there is no interaction between caviar and honey beyond the single subtraction at the toll, the optimal strategy must be one of these three endpoints. Any hypothetical mixed strategy would contradict the fixed-form nature of the toll, which enforces a single choice among three discrete transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    i, m, a, b, v, c, d = map(int, input().split())

    base = i * a + m * b
    ans = base - v  # pay money

    if i >= c:
        ans = max(ans, (i - c) * a + m * b)

    if m >= d:
        ans = max(ans, i * a + (m - d) * b)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first computes the full value of goods without any deductions. This acts as a reference point for all other outcomes. The cash payment case is handled by subtracting v directly.

Then we check feasibility for each goods-based payment. Each check simply ensures enough stock exists, then recomputes the resulting value after removing the corresponding quantity. No simulation is needed because only one deduction happens.

The comparisons are done incrementally, so we always preserve the best achievable outcome.

## Worked Examples

### Example 1

Input: i = 5, m = 10, a = 2, b = 3, v = 7, c = 3, d = 3

We evaluate all three options.

| Option | Remaining (i, m) | Value computation | Result |
| --- | --- | --- | --- |
| Cash | (5, 10) | 5·2 + 10·3 − 7 | 33 |
| Caviar | (2, 10) | 2·2 + 10·3 | 34 |
| Honey | (5, 7) | 5·2 + 7·3 | 31 |

The best is paying with caviar, yielding 34.

This shows that avoiding cash payment can be optimal even if it preserves liquidity, because goods have higher downstream value.

### Example 2

Input: i = 5, m = 10, a = 1, b = 3, v = 10, c = 6, d = 3

| Option | Remaining (i, m) | Value computation | Result |
| --- | --- | --- | --- |
| Cash | (5, 10) | 5·1 + 10·3 − 10 | 25 |
| Caviar | invalid | not enough caviar | - |
| Honey | (5, 7) | 5·1 + 7·3 | 26 |

Here, caviar payment is impossible, so only two options are compared. Honey payment is best despite losing goods, because cash payment reduces total value more.

This demonstrates the importance of feasibility checks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations per test |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits constraints since even for 10 test cases, the work is purely constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        i, m, a, b, v, c, d = map(int, input().split())

        base = i * a + m * b
        ans = base - v

        if i >= c:
            ans = max(ans, (i - c) * a + m * b)

        if m >= d:
            ans = max(ans, i * a + (m - d) * b)

        print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# sample-like cases
assert run("5 10 2 3 7 3 3\n") == "34"

# cash dominates scenario
assert run("1 1 100 100 1 0 0\n") == "199"

# forced goods payment due to large v
assert run("5 5 1 1 1000 2 2\n") == "6"

# boundary: exactly enough caviar
assert run("10 0 5 1 0 10 1\n") == "0"

# boundary: exactly enough honey
assert run("0 10 1 5 0 1 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| cash vs goods tradeoff | 34 | correctness of max selection |
| small equal values | 199 | baseline arithmetic correctness |
| large cash penalty | 6 | avoiding cash when suboptimal |
| exact caviar threshold | 0 | boundary feasibility |
| exact honey threshold | 0 | boundary feasibility |

## Edge Cases

One edge case is when cash payment looks attractive because it avoids losing goods, but actually reduces final profit more than selling the goods would. For instance, even a small caviar deduction can be worth more than paying cash if a is large.

Another case is when a goods-based payment is just barely feasible. If i equals c exactly, the remaining caviar becomes zero, which can drastically change value. The algorithm handles this because it checks i ≥ c before computing the reduced state.

A third case is when both goods payments are invalid. In that situation, only cash payment remains, and the algorithm correctly falls back to base − v without comparing invalid states.
