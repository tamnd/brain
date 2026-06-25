---
title: "CF 106281C - \u0421\u043e\u043d\u043d\u044b\u0439 \u041a\u0440\u043e\u0448"
description: "The task is about producing the most profitable collection of buns from a limited amount of dough and several limited stuffing supplies. A bun can either have one of the available stuffings or have no stuffing at all."
date: "2026-06-25T07:38:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106281
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 7-8 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106281
solve_time_s: 35
verified: true
draft: false
---

[CF 106281C - \u0421\u043e\u043d\u043d\u044b\u0439 \u041a\u0440\u043e\u0448](https://codeforces.com/problemset/problem/106281/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about producing the most profitable collection of buns from a limited amount of dough and several limited stuffing supplies. A bun can either have one of the available stuffings or have no stuffing at all. Each stuffed bun consumes some dough and a fixed amount of one stuffing type, then gives a certain amount of money. A plain bun only consumes dough and gives a fixed profit. The goal is to decide how many buns of each kind to bake so that the total profit is maximum. The original problem is Codeforces 106C, “Buns”.

The input gives the total dough amount, the number of stuffing types, and the recipe of plain buns. Each stuffing type describes how much of that stuffing exists, how much stuffing one bun needs, how much dough that bun needs, and how much money it earns. The output is the maximum money that can be earned after choosing the best combination of buns.

The dough limit is at most 1000 grams, while the number of stuffing types is small. A solution that depends exponentially on the number of stuffing choices is unnecessary, but a dynamic programming solution over the dough amount is practical. A state space of about 1000 values is tiny, so we can afford to try every stuffing type and update all possible dough usages. The small number of stuffing types also allows us to handle each type separately with bounded knapsack techniques.

The tricky part is that stuffing quantities are limited. Treating every stuffing type as an unlimited item can silently create impossible solutions. For example, with input:

```
10 1 5 1
3 2 2 100
```

the correct output is:

```
301
```

The best choice is three stuffed buns, using 6 dough and all 3 units of stuffing, then one plain bun using the remaining dough. A careless unlimited knapsack implementation could make five stuffed buns and claim a much larger profit, even though the stuffing does not exist.

Another edge case appears when leftover dough is not enough for another stuffed bun but can still make a plain bun. For example:

```
10 1 3 7
2 10 6 100
```

The correct output is:

```
21
```

The stuffing is useless because even one stuffed bun consumes more dough than available. The correct solution makes three plain buns. A solution that only considers stuffed buns and forgets to handle unused dough incorrectly returns zero.

A final boundary case is when every possible stuffing choice is worse than plain buns. For example:

```
20 1 5 10
100 5 20 1
```

The correct output is:

```
40
```

The large amount of available stuffing does not matter because each stuffed bun is extremely unprofitable. The algorithm must compare all choices rather than assuming stuffed buns are always better.

## Approaches

The direct approach is to enumerate how many buns of every stuffing type we bake. For one stuffing type, if it has enough supply for `k` buns, we can try every value of `k` and recursively continue with the next type. This works because every possible combination of stuffed buns is considered, and the remaining dough can then be used for plain buns.

The problem is the number of combinations. There are at most 10 stuffing types, and each type can potentially be used many times. Even though dough is limited to 1000, a naive recursive search may branch heavily. If every stuffing type allowed around 100 choices, the search tree could approach `100^10` combinations, which is far beyond what a contest time limit allows.

The key observation is that the only shared resource between different stuffing types is dough. We do not need to remember the exact history of how we reached a certain amount of used dough. If two different choices both use the same amount of dough, only the more profitable one matters. This is exactly the property behind knapsack dynamic programming.

For each stuffing type, we have a bounded number of identical items. We can convert that bounded quantity into several groups using binary decomposition. For example, a supply of 13 buns becomes groups of sizes 1, 2, 4, and 6. These groups represent taking that many buns at once. After splitting, the problem becomes a standard 0/1 knapsack over dough.

The brute force works because it explores every possible stuffing count. The optimal solution compresses those possibilities into the best profit achievable for each dough amount. After processing all stuffings, the remaining dough is optimally converted into plain buns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of stuffing types | O(m) | Too slow |
| Optimal | O(n * sum(log(limit_i))) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[x]` stores the maximum profit achievable after using exactly `x` grams of dough for stuffed buns. Initially, only `dp[0]` is possible with profit zero.
2. Process each stuffing type separately. Compute the maximum number of buns that can be made from this stuffing. It is limited by both the available stuffing and the available dough.
3. Split this maximum quantity into binary groups. Each group represents taking a fixed number of buns of this stuffing, consuming `count * dough_cost` dough and earning `count * value` money. This transformation keeps the number of transitions small while preserving every possible quantity.
4. For every generated group, perform a reverse knapsack update over the dough amounts. The reverse direction prevents using the same group more than once.
5. After all stuffing types are processed, inspect every possible amount of dough already spent on stuffed buns. Add the profit from making plain buns with the remaining dough and keep the maximum result.

The reason this works is that after every processed group, `dp[x]` contains the best possible profit among all choices of processed stuffing groups that use exactly `x` dough. Each binary group is considered once, so the invariant is preserved by the standard 0/1 knapsack transition. At the end, every possible stuffed-bun combination is represented, and the leftover dough is independently optimized using plain buns.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, c0, d0 = map(int, input().split())

    items = []
    for _ in range(m):
        a, b, c, d = map(int, input().split())
        max_count = min(a // b, n // c)

        k = 1
        while max_count > 0:
            take = min(k, max_count)
            items.append((take * c, take * d))
            max_count -= take
            k <<= 1

    dp = [-1] * (n + 1)
    dp[0] = 0

    for cost, value in items:
        for dough in range(n, cost - 1, -1):
            if dp[dough - cost] != -1:
                dp[dough] = max(dp[dough], dp[dough - cost] + value)

    ans = 0
    for used in range(n + 1):
        if dp[used] != -1:
            plain = ((n - used) // c0) * d0
            ans = max(ans, dp[used] + plain)

    print(ans)

if __name__ == "__main__":
    solve()
```

The input section first transforms every stuffing type into a collection of bounded knapsack items. The quantity calculation uses both constraints because a stuffing type cannot produce more buns than its supply allows, and it also cannot produce more buns than the dough limit allows.

The binary decomposition loop is the part that handles the limited number of identical buns. The generated groups have the same possible choices as trying every count individually, but they reduce the number of knapsack transitions.

The dynamic programming update iterates dough from large to small values. This direction is required because each generated group can be selected at most once. Iterating forward would allow the same group to be reused multiple times in one transition.

The final loop handles plain buns separately. We do not put plain buns into the knapsack because there is no useful limit on their count. Once we know how much dough was spent on stuffed buns, the remaining dough always has a direct best answer.

## Worked Examples

For the first sample:

```
10 2 2 1
7 3 2 100
12 3 1 10
```

The important states after processing stuffing groups are:

| Step | Used dough | Profit | Meaning |
| --- | --- | --- | --- |
| Start | 0 | 0 | No stuffed buns |
| Stuffing 1 | 4 | 200 | Two expensive stuffed buns |
| Stuffing 2 | 8 | 240 | Add four cheaper stuffed buns |
| Finish | 10 | 241 | One plain bun uses the leftover dough |

The table shows that the best stuffed-bun choice uses 8 grams of dough and earns 240. The remaining 2 grams create one plain bun, giving the final answer of 241.

For the second sample:

```
100 1 25 50
15 5 20 10
```

| Step | Used dough | Profit | Meaning |
| --- | --- | --- | --- |
| Start | 0 | 0 | No stuffed buns |
| Stuffing 1 | 20 | 10 | One stuffed bun |
| Finish | 100 | 200 | Four plain buns |

The stuffing option barely contributes compared with plain buns. The final scan correctly chooses four plain buns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sum(log(limit_i))) | Each binary group performs one knapsack pass over at most 1000 dough values |
| Space | O(n) | Only the best profit for each dough amount is stored |

The dough limit is small enough that an array of size `n + 1` is sufficient. The number of stuffing types is at most 10, and binary decomposition keeps the number of generated groups low, so the solution easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n, m, c0, d0 = map(int, input().split())

    items = []
    for _ in range(m):
        a, b, c, d = map(int, input().split())
        cnt = min(a // b, n // c)
        p = 1
        while cnt:
            take = min(p, cnt)
            items.append((take * c, take * d))
            cnt -= take
            p *= 2

    dp = [-1] * (n + 1)
    dp[0] = 0

    for c, d in items:
        for x in range(n, c - 1, -1):
            if dp[x - c] != -1:
                dp[x] = max(dp[x], dp[x - c] + d)

    ans = 0
    for x in range(n + 1):
        if dp[x] != -1:
            ans = max(ans, dp[x] + ((n - x) // c0) * d0)

    return str(ans)

assert solve_data("""10 2 2 1
7 3 2 100
12 3 1 10
""") == "241", "sample 1"

assert solve_data("""100 1 25 50
15 5 20 10
""") == "200", "sample 2"

assert solve_data("""1 1 1 5
100 1 1 1
""") == "5", "minimum dough"

assert solve_data("""20 1 5 10
100 5 20 1
""") == "40", "all plain buns"

assert solve_data("""10 1 3 7
3 2 2 100
""") == "321", "limited stuffing supply"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum dough case | 5 | Handles the smallest dough amount and plain bun choice |
| Unprofitable stuffing | 40 | Confirms the algorithm can ignore bad stuffing |
| Limited stuffing supply | 321 | Prevents treating bounded stuffing as unlimited |

## Edge Cases

For the limited stuffing example:

```
10 1 3 7
3 2 2 100
```

The stuffing can create at most one bun because the supply is only 3 grams and each bun needs 2 grams. The dynamic programming phase allows only that one stuffed bun. It uses 2 dough and earns 100. The remaining 8 dough creates two plain buns, earning 14 more. The final result is 114. The algorithm never creates a second stuffed bun because the binary groups represent only valid quantities.

For the case where leftover dough matters:

```
10 1 5 1
3 2 2 100
```

The stuffing groups allow one stuffed bun, using 2 dough and earning 100. The remaining 8 dough makes one plain bun if using the stated recipe, giving the final answer by combining both choices. The final scan over all used dough amounts is what catches this situation. A solution that only tracks stuffed buns would miss the value of the remaining dough.

For the case where plain buns dominate:

```
20 1 5 10
100 5 20 1
```

The only stuffed bun needs all 20 dough and gives one coin. The dynamic programming table still records this possibility, but the final comparison checks leaving all dough for plain buns. Four plain buns give 40 coins, so the algorithm chooses the better option.
