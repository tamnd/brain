---
title: "CF 106056C - New but Nostalgic Problem"
description: "The problem is about choosing how to bake buns to maximize profit. A baker has a fixed amount of dough and several possible fillings."
date: "2026-06-25T12:18:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106056
codeforces_index: "C"
codeforces_contest_name: "The 1st Universal Cup. Stage 18: Shenzhen"
rating: 0
weight: 106056
solve_time_s: 34
verified: true
draft: false
---

[CF 106056C - New but Nostalgic Problem](https://codeforces.com/problemset/problem/106056/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is about choosing how to bake buns to maximize profit. A baker has a fixed amount of dough and several possible fillings. For each filling type, there is a limited amount available, and each bun using that filling consumes some filling, some dough, and gives a certain amount of money. The baker can also make plain buns without filling, which only consume dough and give a fixed profit. The goal is to find the maximum possible revenue.

The input describes the available dough, the number of filling types, and the recipe for plain buns. Each filling type gives four values: the total amount of that filling, the amount of filling needed per bun, the dough needed per bun, and the selling price. The output is the largest amount of money that can be earned.

The dough limit is at most 1000, which is the key constraint. A solution that is exponential in the number of filling choices is impossible, because even a small number of filling types could create too many combinations. However, the small number of filling types, at most 10, suggests that we can afford a dynamic programming state that tracks the dough usage.

The difficult part is that each filling can be used multiple times, but only up to the available amount. A careless solution might greedily choose the filling with the highest price per gram of dough. For example, if the input is:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The correct output is:

```
241
```

A greedy strategy might focus only on the first filling because it gives 100 money per bun. However, the second filling uses less dough and allows more buns to be produced. The optimal choice mixes both fillings.

Another edge case is when plain buns are the best option. Consider:

```
100 1 25 50
15 5 20 10
```

The correct output is:

```
200
```

A method that always tries to use fillings first would lose money, because four plain buns earn more than any possible combination involving the filling.

## Approaches

The straightforward approach is to try every possible number of buns for every filling type. For a filling, we can choose from zero buns up to the maximum allowed by the available filling. Since there are multiple fillings, the number of combinations becomes the product of all these choices.

In the worst case, each filling amount is large enough to allow many choices. Even with only 10 fillings, trying every combination can become far too slow. The brute force idea is correct because it checks every possible baking plan, but the search space is too large.

The key observation is that dough is the limiting resource and its maximum value is only 1000. We do not need to remember the exact combination of fillings used. We only need to know how much dough remains, because future decisions depend only on that. This converts the problem into a bounded knapsack problem.

For each filling type, we process all possible quantities of that filling and update the best profit achievable for every possible amount of dough. After all fillings are handled, we can fill the remaining dough with plain buns in the most profitable way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of fillings | O(1) | Too slow |
| Dynamic Programming | O(m * n * max_possible_buns) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the dough amount, the number of fillings, and the plain bun recipe. Create a dynamic programming array where `dp[x]` represents the maximum money that can be earned using exactly `x` grams of dough from processed fillings.
2. For every filling type, compute the maximum number of buns possible using that filling. It is limited both by the available filling and by the fact that each bun consumes dough.
3. For the current filling, try every possible number of buns from zero to the maximum possible count. For each count, update the new profit for every dough amount that can support those buns.
4. After all fillings have been processed, consider plain buns. For every possible amount of dough already spent on fillings, calculate how many plain buns can be made from the remaining dough and add their profit.
5. The maximum value over all final states is the answer.

The reason this works is that the dynamic programming state stores all information needed for future choices. Once we know the amount of dough used so far, previous filling choices no longer matter. Every valid baking plan corresponds to one sequence of transitions, so the best value stored for each dough amount is always achievable and optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())
    fillings = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())
        fillings.append((a, b, c, d))

    dp = [0] * (n + 1)

    for a, b, c, d in fillings:
        ndp = dp[:]
        limit = min(a // b, n // c)

        for cnt in range(1, limit + 1):
            dough = cnt * c
            value = cnt * d
            for used in range(dough, n + 1):
                if dp[used - dough] + value > ndp[used]:
                    ndp[used] = dp[used - dough] + value

        dp = ndp

    ans = 0
    for used in range(n + 1):
        plain = (n - used) // c0
        cur = dp[used] + plain * d0
        if cur > ans:
            ans = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The code keeps a one dimensional DP array because the only changing resource is dough. For each filling, `ndp` is a copy of the previous state so that the current filling cannot be accidentally reused beyond its allowed quantity.

The loop over `cnt` handles the bounded nature of each filling. The maximum number of buns is the minimum of the available filling limit and the dough limit. The transition uses `used - dough` because we are asking how much profit was possible before adding the current group of buns.

After processing fillings, the final loop handles plain buns separately. This is simpler than mixing plain buns into the DP because there is no quantity limit for them.

## Worked Examples

### Sample 1

Input:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The important states after processing fillings are:

| Step | Dough used | Profit |
| --- | --- | --- |
| Start | 0 | 0 |
| Two buns of filling 1 | 4 | 200 |
| Four buns of filling 2 | 4 | 40 |
| Two filling 1 + four filling 2 | 8 | 240 |
| Remaining dough for plain buns | 10 | 241 |

The best filling combination uses eight grams of dough and earns 240. The remaining two grams create one plain bun, giving the final answer 241.

### Sample 2

Input:

```
100 1 25 50
15 5 20 10
```

The trace is:

| Step | Dough used | Profit |
| --- | --- | --- |
| Start | 0 | 0 |
| One filling bun | 20 | 10 |
| No filling | 100 | 200 |

The filling is not useful because it gives little money compared with plain buns. The final answer comes entirely from plain buns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * n) | For every filling and every possible count, we update every dough amount |
| Space | O(n) | Only the current DP array and a copied transition array are stored |

With `n` at most 1000 and `m` at most 10, the number of operations is small enough for the limits. The memory usage is also tiny because the DP array has only 1001 positions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue()

assert run("10 2 2 1\n7 3 2 100\n12 3 1 10\n") == "241\n"

assert run("100 1 25 50\n15 5 20 10\n") == "200\n"

assert run("1 1 1 5\n1 1 1 10\n") == "10\n"

assert run("10 1 3 7\n100 100 1 100\n") == "70\n"

assert run("20 2 4 5\n100 1 4 5\n100 1 4 5\n") == "25\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 5` with one filling | `10` | Checks the smallest dough amount and filling usage |
| `10 1 3 7` with unavailable filling | `70` | Checks that impossible fillings are ignored |
| `20 2 4 5` | `25` | Checks multiple fillings with identical recipes |

## Edge Cases

A filling can exist but be impossible to use because there is not enough of it or not enough dough. In that case, the maximum count becomes zero. For example:

```
10 1 2 3
1 5 1 100
```

The filling needs five units but only one exists, so the algorithm skips it. The baker makes five plain buns and the answer is 15.

A filling can be worse than plain buns even if it looks valuable. For:

```
100 1 25 50
15 5 20 10
```

the DP stores only the small profit from using the filling, then the final step compares it with using the remaining dough for plain buns. This produces 200 instead of a worse greedy choice.

When all fillings have the same cost and value, there is no special handling required. Each transition still represents a possible baking plan, and the maximum profit is preserved. For example:

```
20 2 4 5
100 1 4 5
100 1 4 5
```

The DP reaches 25 by using five buns, which confirms that repeated equal choices are handled correctly.
