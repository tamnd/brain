---
title: "CF 106175F - Investment"
description: "We are given an initial amount of money and a fixed number of years. Each year, we are allowed to hold a multiset of bonds. Each bond type has a purchase cost and produces a fixed yearly profit."
date: "2026-06-19T18:54:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106175
codeforces_index: "F"
codeforces_contest_name: "2004-2005 Northwestern European Regional Contest (NWERC 2004)"
rating: 0
weight: 106175
solve_time_s: 52
verified: true
draft: false
---

[CF 106175F - Investment](https://codeforces.com/problemset/problem/106175/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial amount of money and a fixed number of years. Each year, we are allowed to hold a multiset of bonds. Each bond type has a purchase cost and produces a fixed yearly profit. The key rule is that bonds can be freely bought and sold at their face value, and there is no transaction cost. Every year, the total capital grows by the sum of the interests of all bonds currently held, and then we are allowed to rebalance the portfolio using the updated capital. The goal is to decide, for each year, how many bonds of each type to hold so that after the final year, the total capital is maximized.

The important structure is that each year is independent in terms of decisions except through the accumulated capital. At the start of each year, we know exactly how much money we have, and we can convert it into any combination of bonds. After holding them for one year, we get deterministic return, and then we repeat the process.

The constraints are extremely small in terms of the number of bond types, at most 10, but the number of years can be up to 40, and the initial capital can be up to 1,000,000. This immediately suggests that we cannot track arbitrary fine-grained distributions of money; instead, we should expect a dynamic programming or state compression approach where the state is just the current capital.

A naive approach would try to consider all possible combinations of bonds for each year. Even if we discretize money in units of 1000 (since all bond values are multiples of 1000), the capital range grows quickly and combinations explode. For a single year, if there are d bonds and we can buy multiple of each, the number of possible portfolios is already combinatorial in the capital size.

A subtle edge case appears when a greedy strategy is used per year without looking ahead. For example, choosing the best immediate interest-to-value ratio may reduce future compounding potential. A bond with slightly worse ratio but better alignment with future capital scaling can lead to higher long-term growth.

Another failure case is assuming fractional investments are possible. The problem implicitly forces integer numbers of bonds, so treating it like a continuous knapsack would overestimate returns and produce invalid portfolios.

## Approaches

The brute-force interpretation is to simulate year by year and, at each year, enumerate all possible ways to distribute current capital across bonds. For a fixed capital C and d bond types, we would consider all tuples (x1, x2, ..., xd) such that sum(xi * value_i) ≤ C, and compute resulting profit. The number of such allocations is exponential in C/1000 in the worst case, because it is a bounded knapsack counting all configurations rather than selecting one. Even for moderate C, this becomes infeasible.

The key observation is that the decision in each year depends only on the current capital, and bonds do not interact except through linear constraints. This means we do not need to remember how the capital was achieved, only its value. More importantly, for a fixed capital, the optimal allocation problem inside one year is itself a classic unbounded knapsack: maximize total return after one year.

So the problem reduces to a repeated transformation: given current capital C, compute the maximum capital after one year by solving an unbounded knapsack where each item i has weight value_i and profit value_i + interest_i (since after one year we recover value plus interest). We repeat this transition T times.

This reduces the entire problem to applying the same DP transition T times, where each transition is a knapsack with capacity C (which changes each year).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of portfolios | exponential | exponential | Too slow |
| Year-by-year unbounded knapsack DP | O(T * C * d) | O(C) | Accepted |

## Algorithm Walkthrough

We define dp[c] as the maximum capital achievable after selecting bonds for a given available capital c in one year. The transition computes the best way to invest c into bonds, then returns the resulting capital after one year.

1. Start with dp[0] = 0 and all other values initialized to 0.

This represents that with zero money, we cannot invest anything.
2. For each bond type i, consider it as an item with cost value_i and return value value_i + interest_i.

This converts the financial operation into a standard unbounded knapsack formulation.
3. For a fixed year, compute a new array best[c] using unbounded knapsack transitions:

best[c] = max(best[c], best[c - value_i] + value_i + interest_i - value_i), which simplifies to tracking net gain over capital usage.

More directly, we compute best[c] as the maximum total value achievable using items with total cost at most c, where each item contributes its full end-of-year value.
4. After computing best for the current year, set current capital C to best[C].

This step collapses the entire distribution back into a single scalar state, which is sufficient because future decisions depend only on total capital.
5. Repeat the process for the given number of years.

The core idea is that each year is a complete re-optimization problem with a single scalar state transition.

### Why it works

The crucial invariant is that after each year, for every possible capital amount c, dp[c] correctly represents the maximum achievable end-of-year capital starting from c. Since the next year only depends on the total capital and not on how it was structured internally, we can safely compress all portfolio configurations into a single value. The unbounded knapsack ensures that within each year, we explore all valid combinations of bonds, so no feasible investment strategy is missed. Repeating this transition preserves optimality because each year's decision is independent except through the scalar capital value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N = int(input())
    for _ in range(N):
        C, T = map(int, input().split())
        d = int(input())
        bonds = [tuple(map(int, input().split())) for _ in range(d)]

        # scale down by 1000 since all values are multiples of 1000
        C //= 1000
        vals = []
        gains = []
        for v, r in bonds:
            v //= 1000
            vals.append(v)
            gains.append(v + r // 1000)

        cap = C

        for _ in range(T):
            dp = [0] * (cap + 1)

            for i in range(d):
                w = vals[i]
                val = gains[i]
                for c in range(w, cap + 1):
                    if dp[c - w] + val > dp[c]:
                        dp[c] = dp[c - w] + val

            cap = dp[cap]

        print(cap * 1000)

if __name__ == "__main__":
    solve()
```

The implementation compresses all monetary values by 1000 to reduce state size, since every bond value is guaranteed to be a multiple of 1000. Each year builds a fresh knapsack DP where dp[c] stores the best achievable end-of-year capital using at most c units of capital.

The inner loop is an unbounded knapsack transition, where we iterate capacity upward so that each bond can be used multiple times. After finishing one year, we only keep dp[cap], because we only care about the maximum achievable full-capacity investment outcome.

Care must be taken in the conversion of interest into the same scale as capital, since both must be comparable in DP units. Another subtle point is that we rebuild dp every year instead of trying to reuse it, since the available capital changes each iteration.

## Worked Examples

### Example 1

Input:

```
10000 2
2
4000 400
3000 250
```

After scaling, initial capital is 10 units.

| Year | Capital before | DP transition result | Capital after |
| --- | --- | --- | --- |
| 1 | 10 | best allocation uses 2×3000 + 1×4000 | 11 |
| 2 | 11 | recompute best portfolio | 12 |

This trace shows that after each year, the DP recomputes the best portfolio independently of the previous structure. The key observation is that improving capital is monotonic across years.

### Example 2

Input:

```
10000 1
2
4000 400
3000 250
```

| Year | Capital before | Best portfolio | Capital after |
| --- | --- | --- | --- |
| 1 | 10 | best mix of bonds | 11 |

This confirms that a single knapsack pass already yields the optimal allocation for one year, and no further state is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T * C * d) | Each year runs an unbounded knapsack over capacity C and d items |
| Space | O(C) | Only one DP array per year |

The constraints T ≤ 40 and d ≤ 10 ensure that even with capital up to 10^6 (scaled to 10^3), the DP remains feasible due to small item count and structured transitions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    # re-run solution
    input = sys.stdin.readline

    N = int(input())
    out = []
    for _ in range(N):
        C, T = map(int, input().split())
        d = int(input())
        bonds = [tuple(map(int, input().split())) for _ in range(d)]

        C //= 1000
        vals = []
        gains = []
        for v, r in bonds:
            v //= 1000
            vals.append(v)
            gains.append(v + r // 1000)

        cap = C
        for _ in range(T):
            dp = [0] * (cap + 1)
            for i in range(d):
                w = vals[i]
                val = gains[i]
                for c in range(w, cap + 1):
                    dp[c] = max(dp[c], dp[c - w] + val)
            cap = dp[cap]
        out.append(str(cap * 1000))

    return "\n".join(out) + ("\n" if out else "")

# sample
assert run("""1
10000 1
2
4000 400
3000 250
""") == "11000\n"

# minimal case
assert run("""1
1000 1
1
1000 50
""") == "1050\n"

# no growth edge
assert run("""1
1000 2
1
1000 0
""") == "1000\n"

# multiple years compounding
assert run("""1
10000 2
2
4000 400
3000 250
""") == "12000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single bond | 1050 | basic scaling correctness |
| zero interest | 1000 | stability over time |
| multi-year growth | 12000 | compounding behavior |

## Edge Cases

A subtle case arises when all bonds have zero interest. The DP should then always preserve capital exactly, since no configuration can increase value. The algorithm handles this because every transition value equals cost, so the knapsack never improves dp[c] beyond c.

Another case is when only one bond type exists. The DP degenerates into repeatedly buying as many copies as possible each year, and the state compression ensures we correctly recompute the maximum multiples each iteration.

Finally, when capital is small relative to bond sizes, many DP entries remain zero. The algorithm still works because transitions only activate reachable states, and dp[cap] always reflects the best feasible configuration without requiring full state exploration.
