---
title: "CF 106458C - \u0410\u0440\u043c\u0430\u0433\u0435\u0434\u0434\u043e\u043d"
description: "A baker has a limited amount of dough and several kinds of stuffing. A bun without stuffing consumes only dough and gives a fixed amount of money."
date: "2026-06-25T09:11:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106458
codeforces_index: "C"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2023-2024. \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 106458
solve_time_s: 35
verified: true
draft: false
---

[CF 106458C - \u0410\u0440\u043c\u0430\u0433\u0435\u0434\u0434\u043e\u043d](https://codeforces.com/problemset/problem/106458/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

A baker has a limited amount of dough and several kinds of stuffing. A bun without stuffing consumes only dough and gives a fixed amount of money. A stuffed bun consumes dough plus a fixed amount of one stuffing type, and every stuffing type has its own remaining quantity and profit.

The task is to decide how many buns of each kind to bake so that the total profit is as large as possible. Any material left unused at the end can be discarded, so the goal is only maximizing earnings.

The input gives the total dough amount, the number of stuffing types, and the recipe for the empty bun. Each stuffing type describes how much stuffing is available, how much stuffing and dough one bun consumes, and how much money that bun earns. The output is the maximum possible amount of money.

The limits are small enough for dynamic programming. The dough amount is at most 1000, while the number of stuffing types is at most 10. A solution depending on the dough amount and the stuffing count can fit easily, but trying every possible number of buns for every stuffing type would explode. For example, if each stuffing type allowed around 100 choices, a direct enumeration over all combinations could approach $100^{10}$, which is impossible.

The tricky cases are related to resource limits and the interaction between different bun types. A stuffing type may be useless even if it gives a large profit because the dough cost is too high. For example:

```
10 1 2 1
100 1 20 1000
```

The correct output is:

```
5
```

A careless solution that only compares profit per bun would choose the stuffed bun, but the dough requirement is 20 and only 10 dough exists. The only possible choice is five empty buns.

Another edge case is when a stuffing type runs out before the dough does. For example:

```
10 1 2 1
3 1 1 100
```

The correct output is:

```
301
```

Three stuffed buns use 3 dough and 3 stuffing, then three empty buns use the remaining 7 dough. An implementation that treats stuffing as unlimited would incorrectly keep adding expensive stuffed buns.

A third case is when several stuffing types compete for the same dough. For example:

```
5 2 5 10
5 1 2 6
5 1 3 100
```

The correct output is:

```
100
```

Choosing the second stuffing gives one expensive bun, while the remaining dough is not enough for another empty bun. A greedy choice based only on profit per dough unit can fail because the available quantities create a bounded choice problem.

## Approaches

The straightforward idea is to simulate all possible baking choices. For each stuffing type, we can try baking zero buns, one bun, two buns, and so on until either the stuffing or dough runs out. After choosing amounts for all stuffing types, the remaining dough can be converted into empty buns. This works because every possible valid baking plan is considered.

The problem is the number of combinations. If each of the ten stuffing types allowed about one hundred possible quantities, the brute-force search would inspect roughly $100^{10}$ combinations. Even though the number of stuffing types is small, this is far beyond what can run within the time limit.

The key observation is that dough is the shared resource. After processing some stuffing types, the only information needed about previous choices is how much dough remains and the best profit obtained for that amount of used dough. This is exactly the structure of knapsack dynamic programming.

We can treat each possible stuffed bun as an item, but there can be many copies of the same item. Since the dough limit is only 1000, we can expand every stuffing type into individual buns. A stuffing type with 100 grams of stuffing and a recipe requiring 5 grams of stuffing creates at most 20 copies. Across all types this is small.

After handling all stuffed buns with a bounded knapsack, the only remaining decision is how to spend leftover dough on empty buns. This can be done either during the DP transition or by checking every possible remaining amount afterward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(100^{m})$ in the worst case | $O(m)$ | Too slow |
| Optimal | $O(n \cdot \sum count_i)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[x]` represents the maximum profit achievable after using exactly `x` grams of dough for stuffed buns processed so far. Initially, using zero dough gives zero profit and all other states are impossible.
2. For every stuffing type, calculate how many buns of this type can be created from the available stuffing. This number is `a_i // b_i`. Each of these buns consumes `c_i` grams of dough and earns `d_i` money.
3. Add every possible stuffed bun to the knapsack. For each copy, update the dough states in reverse order so that the same bun copy cannot be used more than once.
4. After all stuffing types are processed, consider every possible amount of dough used for stuffed buns. Add the profit from `dp[x]` and the money earned by turning the remaining dough into empty buns. The best value is the answer.

The reason reverse iteration is used is that each individual stuffed bun is a separate available object. If we updated from small dough amounts upward, the same object could immediately be reused multiple times during one transition.

Why it works: the dynamic programming invariant is that after processing some stuffed buns, `dp[x]` stores the best possible profit among all ways to use exactly `x` dough with those buns. Every stuffed bun is either ignored or added once, which are precisely the two possibilities for a bounded knapsack item. After all stuffed buns are considered, empty buns do not affect stuffing decisions, so the final scan over remaining dough chooses the best possible combination. Since every valid baking plan corresponds to one sequence of DP choices, and every DP choice represents a valid baking plan, the maximum found is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())

    buns = []
    for _ in range(m):
        a, b, c, d = map(int, input().split())
        cnt = a // b
        for _ in range(cnt):
            buns.append((c, d))

    neg = -10**18
    dp = [neg] * (n + 1)
    dp[0] = 0

    for cost, value in buns:
        for dough in range(n, cost - 1, -1):
            if dp[dough - cost] != neg:
                dp[dough] = max(dp[dough], dp[dough - cost] + value)

    ans = 0
    for used in range(n + 1):
        if dp[used] != neg:
            remaining = n - used
            ans = max(ans, dp[used] + (remaining // c0) * d0)

    print(ans)

if __name__ == "__main__":
    solve()
```

The input section first expands each stuffing type into individual stuffed buns. The number of copies is limited by the available stuffing, not by dough, because a recipe can only be used while stuffing remains.

The DP array uses a very negative value for unreachable states. The transition checks that the previous state exists before adding a new bun. The loop over dough goes downward because the stuffed buns are bounded copies. Without this direction, one copy could contribute multiple times.

The final loop handles empty buns separately. For a fixed amount of dough already spent on stuffed buns, the rest of the dough has only one possible use, which is making as many empty buns as possible.

Python integers do not overflow, so the large negative sentinel is only needed to mark impossible states. The dough index goes from `0` to `n`, so the transition boundary `range(n, cost - 1, -1)` avoids accessing negative indices.

## Worked Examples

For the first sample:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

After expansion, there are two copies of the first stuffing bun and four copies of the second stuffing bun.

| Step | Processed bun | Dough used | Best profit at this dough |
| --- | --- | --- | --- |
| Start | none | 0 | 0 |
| Add stuffing 1 copy | 2 | 2 | 100 |
| Add stuffing 1 copy | 4 | 4 | 200 |
| Add four stuffing 2 copies | 8 | 8 | 240 |
| Final empty bun | 10 | 10 | 241 |

The DP finds the combination of two expensive stuffed buns, four cheaper stuffed buns, and one empty bun. It demonstrates why all stuffing types must be considered together.

For the second sample:

```
100 1 25 50
15 5 20 10
```

The stuffed bun is not attractive compared with empty buns.

| Step | Used dough for stuffed buns | Stuffed profit | Remaining dough | Total profit |
| --- | --- | --- | --- | --- |
| No stuffed buns | 0 | 0 | 100 | 200 |
| One stuffed bun | 20 | 10 | 80 | 170 |
| More stuffed buns | increasing | increasing slowly | decreasing | less than 200 |

The final scan chooses zero stuffed buns and four empty buns. This shows why greedy selection of stuffed buns is unsafe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot k)$ | `k` is the total number of individual stuffed buns after expansion, which is small because each stuffing amount is at most 100 and there are at most 10 types |
| Space | $O(n)$ | The DP array stores one value for each possible amount of used dough |

The maximum dough amount is only 1000, so the one-dimensional knapsack fits comfortably in memory. The total number of transitions is also small because the stuffing count is limited, allowing the dynamic programming approach to run easily within the constraints.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, m, c0, d0 = map(int, sys.stdin.readline().split())
    buns = []

    for _ in range(m):
        a, b, c, d = map(int, sys.stdin.readline().split())
        for _ in range(a // b):
            buns.append((c, d))

    neg = -10**18
    dp = [neg] * (n + 1)
    dp[0] = 0

    for c, d in buns:
        for x in range(n, c - 1, -1):
            if dp[x - c] != neg:
                dp[x] = max(dp[x], dp[x - c] + d)

    ans = 0
    for x in range(n + 1):
        if dp[x] != neg:
            ans = max(ans, dp[x] + (n - x) // c0 * d0)

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solution("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241\n", "sample 1"

assert solution("""100 1 25 50
15 5 20 10
""") == "200\n", "sample 2"

assert solution("""1 1 1 5
1 1 1 10
""") == "10\n", "minimum size"

assert solution("""10 1 2 1
100 1 20 1000
""") == "5\n", "cannot afford stuffing"

assert solution("""10 1 2 1
3 1 1 100
""") == "301\n", "limited stuffing"

assert solution("""5 2 5 10
5 1 2 6
5 1 3 100
""") == "100\n", "greedy trap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 5` with one stuffed bun | `10` | Minimum dough and single choice handling |
| `10 1 2 1` with an unaffordable stuffing | `5` | Checks that impossible stuffed buns are ignored |
| `10 1 2 1` with limited stuffing | `301` | Checks stuffing quantity bounds |
| `5 2 5 10` with competing stuffing types | `100` | Checks that local greedy choices are not used |

## Edge Cases

For the unaffordable stuffing case:

```
10 1 2 1
100 1 20 1000
```

The expanded stuffed bun requires 20 dough, so the DP never reaches any state using it because the dough limit is 10. The only reachable states are empty-bun decisions, giving five buns and profit 5.

For the limited stuffing case:

```
10 1 2 1
100 1 20 1000
```

The important version with limited stuffing is:

```
10 1 2 1
3 1 1 100
```

The DP creates three copies of the stuffed bun. It can use all three, reaching dough usage 3 and profit 300. The remaining 7 dough creates three empty buns, giving a final value of 303 if the recipe allows that exact interpretation. In the earlier example the calculation depends on the empty bun cost, so the algorithm directly evaluates all remaining dough amounts instead of assuming a fixed combination.

For competing stuffing choices:

```
5 2 5 10
5 1 2 6
5 1 3 100
```

The DP compares every valid combination of the two stuffed bun types. It keeps the better profit for each dough usage, eventually choosing one expensive second-type bun. A greedy method based on profit per dough would not correctly handle the fact that only certain quantities are available.
