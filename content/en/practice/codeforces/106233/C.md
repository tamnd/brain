---
title: "CF 106233C - \u0418\u043b\u043b\u044e\u0437\u0438\u044f \u0441\u0443\u043c\u043c\u044b"
description: "We have a baker with a limited amount of dough and several types of fillings. A bun of a particular filling consumes some amount of dough and some amount of that filling, and gives a certain profit. The baker can also make plain buns that only consume dough."
date: "2026-06-25T07:02:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106233
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106233
solve_time_s: 39
verified: true
draft: false
---

[CF 106233C - \u0418\u043b\u043b\u044e\u0437\u0438\u044f \u0441\u0443\u043c\u043c\u044b](https://codeforces.com/problemset/problem/106233/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a baker with a limited amount of dough and several types of fillings. A bun of a particular filling consumes some amount of dough and some amount of that filling, and gives a certain profit. The baker can also make plain buns that only consume dough. The task is to choose how many buns of each kind to bake so that the total profit is as large as possible.

The input describes the available dough, the number of filling types, the cost and profit of a plain bun, and for each filling type the available amount of filling, the amount of filling required per bun, the dough required per bun, and the profit. The output is the maximum possible amount of money earned.

The dough limit is at most 1000, which changes the way we should think about the problem. A state indexed by the amount of remaining dough is small enough to maintain. The number of filling types is also small, at most 10, so processing each type separately is feasible. A solution that tries every possible number of buns for every filling type would grow too quickly because the combinations multiply, while a solution close to O(m * n * something small) is comfortable.

A common mistake is to only choose the filling with the highest profit per gram of dough. This fails because fillings are also limited resources. For example, consider:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The best choice is not to use only the first filling, because it runs out. The correct answer is `241`, using two buns of the first type, four of the second type, and one plain bun. A greedy ratio choice could leave valuable dough unused.

Another edge case is when a filling exists but is not worth using compared to plain buns. For example:

```
100 1 25 50
15 5 20 10
```

The correct output is:

```
200
```

A careless solution might spend dough on the filling because it is available, but four plain buns give more profit.

A third edge case is when a filling amount is not divisible by the amount needed for one bun. For example:

```
5 1 3 10
4 3 2 100
```

Only one filled bun can be made, because the filling is the limiting resource. The remaining filling cannot be used. The correct output is `110`, one filled bun and one plain bun. A loop that only checks the dough restriction can overestimate the answer.

## Approaches

The direct brute force idea is to decide how many buns of every filling type to make. For each type, we try all possible counts from zero up to the number allowed by the filling and dough. After fixing all filling choices, the remaining dough is converted into plain buns. This is correct because every possible baking plan is considered.

The problem is the number of combinations. Even though each filling type alone has a limited number of choices, combining 10 types creates a large search space. If every type allowed around 100 choices, the brute force would explore around `100^10` combinations, which is impossible.

The useful observation is that the only resource shared between all bun types is dough. Filling resources only affect the current filling type. Since the dough limit is small, we can store the best profit achievable for every possible amount of used dough.

For one filling type, we can treat making a bun as a bounded knapsack item. We know the maximum number of buns of that type, and each bun has a fixed dough cost and profit. We update a dynamic programming array where `dp[x]` means the maximum profit after using exactly `x` grams of dough. After processing every filling type, the remaining dough is optimally filled with plain buns.

The brute force works because it enumerates all valid plans, but it fails because it ignores that many plans share the same amount of used dough. The dynamic programming approach merges all such plans into one state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(product of all choices) | O(1) | Too slow |
| Optimal | O(m * n * maxBunsPerType) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the available dough and all bun types. Store the plain bun information separately because it will be applied after all filled buns are considered.
2. Create a dynamic programming array of size `n + 1`. The value at position `i` represents the maximum profit after spending exactly `i` grams of dough. Initially, spending zero dough gives zero profit.
3. Process every filling type one by one. For this type, calculate the maximum number of buns possible from the available filling. The actual number is limited by both the filling amount and the dough limit.
4. Try every possible number of buns of the current filling type. For every possible previous dough usage, update the new state by adding the chosen number of buns. This works because the current filling is independent of the other fillings except through dough.
5. After all fillings are processed, iterate over every possible amount of dough already used. Add the profit from making plain buns with the remaining dough and keep the maximum answer.

The reason this is correct is that after processing some filling types, the dynamic programming state contains the best possible profit for every amount of dough spent. When adding a new filling type, every possible contribution of that type is considered, so the invariant remains true. After all fillings are handled, the only remaining decision is how to use leftover dough, and plain buns have no other limitation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())

    types = []
    for _ in range(m):
        a, b, c, d = map(int, input().split())
        types.append((a, b, c, d))

    dp = [0] * (n + 1)

    for a, b, c, d in types:
        limit = min(a // b, n // c)
        ndp = dp[:]

        for dough_used in range(n + 1):
            if dp[dough_used] < 0:
                continue
            for cnt in range(1, limit + 1):
                new_dough = dough_used + cnt * c
                if new_dough > n:
                    break
                value = dp[dough_used] + cnt * d
                if value > ndp[new_dough]:
                    ndp[new_dough] = value

        dp = ndp

    ans = 0
    for used in range(n + 1):
        plain = (n - used) // c0 * d0
        if dp[used] + plain > ans:
            ans = dp[used] + plain

    print(ans)

if __name__ == "__main__":
    solve()
```

The array `dp` stores the best result for each possible amount of dough already committed. It starts with only the empty baking plan available.

For each filling, the variable `limit` prevents impossible transitions. A bun can only be made if there is enough filling and enough dough. The copied array `ndp` is used because all new choices for the current filling should be based on the previous set of fillings, not on decisions that already used the same filling in the same iteration.

The final loop handles plain buns. The state already accounts for all filled buns, so the remaining dough can only be spent on plain buns. Python integers avoid overflow issues because the maximum answer is still small, but using integer arithmetic naturally handles all intermediate values.

## Worked Examples

For the first sample:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The important states after processing fillings can be traced as follows.

| Step | Processed filling | Dough used | Best profit |
| --- | --- | --- | --- |
| Initial | none | 0 | 0 |
| After filling 1 | type 1 | 2 | 100 |
| After filling 1 | type 1 | 4 | 200 |
| After filling 2 | type 2 | 6 | 240 |

The best state uses 6 grams of dough on filled buns. Four grams remain, so two plain buns can be made, adding one more profit. The final answer is `241`.

For the second sample:

```
100 1 25 50
15 5 20 10
```

The filling gives very little profit, so the optimal state is to use no filling.

| Step | Processed filling | Dough used | Best profit |
| --- | --- | --- | --- |
| Initial | none | 0 | 0 |
| After filling 1 | type 1 | 0 | 0 |
| Final | plain buns | 100 | 200 |

The trace shows that the dynamic programming stage does not force us to use every available resource. The remaining dough is used only where it gives the best return.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * average possible buns) | For each filling we try all dough states and possible counts |
| Space | O(n) | Only the current dough states are stored |

The maximum dough amount is only 1000 and there are at most 10 fillings, so the number of transitions is easily within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    n, m, c0, d0 = map(int, data().split())
    types = []
    for _ in range(m):
        a, b, c, d = map(int, data().split())
        types.append((a, b, c, d))

    dp = [0] * (n + 1)

    for a, b, c, d in types:
        limit = min(a // b, n // c)
        ndp = dp[:]
        for i in range(n + 1):
            for cnt in range(1, limit + 1):
                if i + cnt * c > n:
                    break
                ndp[i + cnt * c] = max(ndp[i + cnt * c], dp[i] + cnt * d)
        dp = ndp

    ans = 0
    for i in range(n + 1):
        ans = max(ans, dp[i] + (n - i) // c0 * d0)

    sys.stdin = old
    return str(ans) + "\n"

assert run("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241\n"

assert run("""100 1 25 50
15 5 20 10
""") == "200\n"

assert run("""5 1 3 10
4 3 2 100
""") == "110\n"

assert run("""1 1 1 5
1 1 1 7
""") == "7\n"

assert run("""20 1 5 10
100 1 5 10
""") == "40\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | 241 | Mixing multiple fillings |
| Second sample | 200 | Ignoring unprofitable fillings |
| `5 1 3 10 / 4 3 2 100` | 110 | Filling limit not matching dough limit |
| `1 1 1 5 / 1 1 1 7` | 7 | Minimum dough boundary |
| `20 1 5 10 / 100 1 5 10` | 40 | All-equal profit choices |

## Edge Cases

For the limited filling case:

```
5 1 3 10
4 3 2 100
```

The algorithm calculates that at most one filled bun can be produced because `4 // 3 = 1`. The transition creates a state with 2 grams of dough used and 100 profit. The remaining 3 grams produce one plain bun, giving the final result `110`.

For the case where plain buns are better:

```
100 1 25 50
15 5 20 10
```

The filling transition can create only one possible filled bun, but every such choice leaves too little value compared to using dough for plain buns. The final scan compares all states with the plain bun profit added, so the empty filling state wins with `200`.

For the mixed-resource case:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The dynamic programming states combine the two filling types without needing to remember how much filling remains from earlier types. Each filling is processed once with its own limit, so the final state represents every valid combination.
