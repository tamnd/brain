---
title: "CF 106390C - Bed Building"
description: "The problem is about maximizing profit while baking buns. There is a fixed amount of dough and several kinds of stuffing available. A bun of a certain stuffing consumes some dough and some amount of that stuffing, then gives a certain profit."
date: "2026-06-25T10:12:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106390
codeforces_index: "C"
codeforces_contest_name: "Purdue Spring 2026 In-House Contest #2"
rating: 0
weight: 106390
solve_time_s: 38
verified: true
draft: false
---

[CF 106390C - Bed Building](https://codeforces.com/problemset/problem/106390/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is about maximizing profit while baking buns. There is a fixed amount of dough and several kinds of stuffing available. A bun of a certain stuffing consumes some dough and some amount of that stuffing, then gives a certain profit. A plain bun consumes only dough and gives its own profit. The task is to decide how many buns of every possible type to make so the total earnings are as large as possible.

The input gives the total dough, the number of stuffing types, and the requirements for plain buns. Each stuffing type describes how much of that stuffing exists, how much stuffing one bun needs, how much dough the bun consumes, and how much money it earns. The output is the maximum amount of money that can be earned.

The bounds are small in the number of stuffing types but large in the amount of dough. Since the number of stuffing types is at most 10, we can afford an exponential or dynamic programming solution over the stuffing types. However, the dough amount can reach 1000, so a solution that tries every possible number of buns without a state limit would grow too much. We need to use the small number of stuffing categories to control the search and the dough amount as the DP dimension.

The main trap is handling the remaining dough after choosing stuffed buns. The plain bun acts as a filler for any unused dough, so the answer is not simply the best combination of stuffed buns. For example:

```
10 1 3 100
5 10 2 1
```

The correct answer is 300. We cannot make stuffed buns because one needs 10 units of stuffing while only 5 exist, so we should make three plain buns. A solution that only considers stuffing choices and forgets the plain bun would output zero.

Another tricky case is when a stuffing type has a worse profit per dough unit but becomes useful because it consumes limited stuffing efficiently. For example:

```
10 2 5 1
100 1 5 10
2 10 1 100
```

The correct answer is 10. We can make two buns of the first type. A greedy approach that always chooses the best value per dough would incorrectly pick the second type because it looks more profitable, but the stuffing limit prevents that.

## Approaches

A direct brute force solution would try every possible count for every stuffing type. For each type, we decide how many buns to bake, then check whether the total stuffing and dough usage are valid. The approach is correct because every possible combination is examined, so the best valid one must be found. The problem is that each stuffing type can have up to 1000 possible counts, and with up to 10 types this becomes far too many combinations. The worst case approaches 1000^10 possibilities, which is impossible.

The useful observation is that the number of stuffing types is tiny. Instead of tracking every possible distribution of buns, we can process stuffing types one by one and store only the best profit achievable for each amount of dough used. The state size is limited by the dough amount, which is only 1000.

When processing a stuffing type, we try all possible numbers of buns made with it. If we make k buns of this type, we know exactly how much stuffing and dough they consume and how much profit they add. This is a bounded knapsack transition. After all stuffing types are processed, the remaining dough can be converted into plain buns, so we simply add the best possible plain bun profit to every state.

The brute force works because it explores every combination, but fails because the combination count explodes. The DP works because different stuffing choices only matter through the amount of dough already spent and the profit earned, which is exactly what the state stores.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(product of possible counts) | O(1) | Too slow |
| Optimal | O(m * n * 100) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[j]` represents the maximum profit after using exactly `j` grams of dough with the stuffing types processed so far. Initially, using zero dough gives zero profit.
2. For every stuffing type, calculate the maximum number of buns that can be made from the available stuffing. We cannot exceed this number because stuffing is a limited resource.
3. For each possible previous dough usage and each possible count of buns of the current type, update the new state. Making `k` buns adds `k * d[i]` profit and consumes `k * c[i]` dough.
4. After all stuffed bun types are processed, consider every possible amount of dough already used. The remaining dough can only be used for plain buns, so add `(remaining dough / c0) * d0` to that state.
5. The maximum value among all final states is the answer because every valid way of using stuffing is represented, and the leftover dough is optimally filled with plain buns.

Why it works: the invariant is that after processing any prefix of stuffing types, `dp[j]` stores the best possible profit among all ways to spend exactly `j` grams of dough using only those processed types. Every transition considers adding the current stuffing type any possible number of times, so it covers every new valid combination. Since the plain bun has no limited resource except dough, handling it at the end completes every possible solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())
    items = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())
        items.append((a // b, c, d))

    dp = [-1] * (n + 1)
    dp[0] = 0

    for limit, cost, value in items:
        ndp = [-1] * (n + 1)
        for used in range(n + 1):
            if dp[used] == -1:
                continue
            for cnt in range(limit + 1):
                new_used = used + cnt * cost
                if new_used > n:
                    break
                profit = dp[used] + cnt * value
                if profit > ndp[new_used]:
                    ndp[new_used] = profit
        dp = ndp

    ans = 0
    for used in range(n + 1):
        if dp[used] != -1:
            total = dp[used] + ((n - used) // c0) * d0
            if total > ans:
                ans = total

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts each stuffing type into a usable limit. `a // b` is the maximum number of buns of that type because every bun consumes `b` units of stuffing and only `a` units exist.

The DP array is rebuilt for every stuffing type so that the transition does not accidentally use the same stuffing multiple times beyond its limit. For each reachable dough amount, the inner loop tries all possible counts of the current bun type.

The final loop is where plain buns are handled. The state already contains the profit from stuffed buns, and the remaining dough is converted into as many plain buns as possible. This avoids needing another DP dimension.

The boundary condition in the transition is `new_used > n`. Once the dough limit is exceeded, larger counts are impossible, so the loop can stop. Python integers are large enough for the maximum profit range, so no overflow handling is required.

## Worked Examples

For the first sample:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The DP evolves as follows.

| Processed type | Dough used | Best profit |
| --- | --- | --- |
| None | 0 | 0 |
| Type 1 | 0 | 0 |
| Type 1 | 2 | 100 |
| Type 1 | 4 | 200 |
| Type 2 | 4 | 200 |
| Type 2 | 8 | 240 |
| Final with plain buns | 10 | 241 |

The best result uses two buns of the first stuffing type, four of the second type, and one plain bun. The trace shows why keeping only the best profit for each dough amount is enough.

For the second sample:

```
100 1 25 50
15 5 20 10
```

| Processed type | Dough used | Best profit |
| --- | --- | --- |
| None | 0 | 0 |
| Stuffed type | 0 | 0 |
| Stuffed type | 20 | 10 |
| Final with plain buns | 100 | 200 |

The stuffed buns are not useful enough to beat plain buns. The final conversion step correctly fills the entire dough with four plain buns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n * 100) | For every stuffing type, every dough amount tries up to 100 possible bun counts because the stuffing amount is bounded by 100 |
| Space | O(n) | Only the previous DP layer and the current layer are stored |

The solution fits because the dough dimension is only 1000 and the number of stuffing types is at most 10. The total number of operations stays small enough for the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    n, m, c0, d0 = map(int, data().split())
    items = []
    for _ in range(m):
        a, b, c, d = map(int, data().split())
        items.append((a // b, c, d))

    dp = [-1] * (n + 1)
    dp[0] = 0

    for limit, cost, value in items:
        ndp = [-1] * (n + 1)
        for used in range(n + 1):
            if dp[used] == -1:
                continue
            for cnt in range(limit + 1):
                nxt = used + cnt * cost
                if nxt > n:
                    break
                ndp[nxt] = max(ndp[nxt], dp[used] + cnt * value)
        dp = ndp

    ans = 0
    for i in range(n + 1):
        if dp[i] != -1:
            ans = max(ans, dp[i] + ((n - i) // c0) * d0)

    sys.stdin = old
    return str(ans)

assert run("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241"

assert run("""100 1 25 50
15 5 20 10
""") == "200"

assert run("""1 1 1 5
1 1 1 100
""") == "100"

assert run("""10 1 3 100
5 10 2 1
""") == "300"

assert run("""20 2 10 1
100 2 5 10
4 10 10 100
""") == "40"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | 241 | Normal mixed stuffing and plain buns |
| Second sample | 200 | Plain buns are better than stuffing |
| `1 1 1 5 / 1 1 1 100` | 100 | Minimum dough boundary |
| `10 1 3 100 / 5 10 2 1` | 300 | Cannot use unavailable stuffing |
| `20 2 10 1 / 100 2 5 10 / 4 10 10 100` | 40 | Stuffing limit handling |

## Edge Cases

When there is not enough stuffing to make even one stuffed bun, the algorithm leaves those transitions unavailable. For the case:

```
10 1 3 100
5 10 2 1
```

the stuffing limit becomes zero because `5 // 10 = 0`. The DP keeps only the empty stuffing choice, and the final step creates three plain buns for a profit of 300.

When the most profitable looking stuffing is not the best overall choice, the DP still works because it compares complete combinations. In:

```
10 2 5 1
100 1 5 10
2 10 1 100
```

the second type cannot be used enough because its stuffing is limited. The transitions include the first type choices, and the final answer becomes 10.

When all dough should be used by plain buns, the final pass over states handles it naturally. The DP state with zero dough spent is still valid, and the remaining dough calculation produces the maximum plain bun count. This avoids needing a special case.
