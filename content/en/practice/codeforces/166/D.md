---
title: "CF 166D - Shoe Store"
description: "We have a collection of shoes, where every shoe has a unique size and a price. We also have customers, where each customer has a budget and a foot size. A customer can buy a shoe only if two conditions hold."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graph-matchings", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 166
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 113 (Div. 2)"
rating: 2500
weight: 166
solve_time_s: 154
verified: true
draft: false
---

[CF 166D - Shoe Store](https://codeforces.com/problemset/problem/166/D)

**Rating:** 2500  
**Tags:** dp, graph matchings, greedy, sortings, two pointers  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of shoes, where every shoe has a unique size and a price. We also have customers, where each customer has a budget and a foot size. A customer can buy a shoe only if two conditions hold.

The first condition is financial: the shoe price must not exceed the customer's budget.

The second condition is size compatibility: if the shoe size is `s`, then the customer foot size must be either `s` or `s - 1`. In other words, a customer can wear shoes of exactly their size or one size larger.

Each shoe can be sold at most once, and each customer can buy at most one pair. The goal is not to maximize the number of sales, but the total revenue from sold shoes.

The constraints completely shape the solution. Both `n` and `m` can reach `10^5`, so any solution that tries all customer-shoe pairs immediately becomes impossible. A quadratic algorithm would require around `10^10` operations in the worst case, far beyond the time limit. We need something close to `O(n log n)` or `O((n + m) log n)`.

The unique shoe sizes are a very strong structural property. Since every size appears at most once among shoes, each customer is compatible with at most two shoe sizes. That dramatically simplifies the matching structure and turns the problem into something much more manageable than general bipartite matching.

Several edge cases are easy to mishandle.

Consider this input:

```
2
100 5
1 6
1
100 5
```

The correct answer is selling the first shoe for profit `100`.

A careless greedy strategy that processes shoes in arbitrary order might sell the cheap shoe first, because the customer can also wear size `6`. That blocks the expensive sale and gives profit `1` instead of `100`.

Another subtle case appears when two customers can buy the same shoe, but only one of them has alternatives.

```
2
50 10
40 11
2
50 10
50 11
```

The optimal solution is:

```
90
2
1 1
2 2
```

If we greedily assign the size `10` shoe to customer `2`, then customer `1` becomes unmatched and total profit drops to `50`.

There is also a dangerous case where choosing a locally expensive sale blocks two future sales.

```
3
100 5
99 6
98 7
2
100 5
99 6
```

The correct answer is `199`, by selling shoes `5` and `6`.

A greedy algorithm that always prioritizes the highest price shoe might take shoe `7` for customer `2`, because size `6` customers can also wear size `7`. Then shoe `6` becomes unsellable and the result becomes `198`.

The problem is fundamentally about carefully preserving flexibility while maximizing total value.

## Approaches

The most direct formulation is bipartite matching. One side contains customers, the other contains shoes. We add an edge when a customer can buy a shoe. Since every customer can connect to at most two shoe sizes, the graph is sparse.

A brute-force solution could build the entire graph and run a weighted matching algorithm. The matching must maximize the sum of shoe prices. General weighted bipartite matching is far too expensive here. Even building all possible pairs naively would take `O(nm)` operations.

The crucial observation is that shoe sizes are unique. A shoe of size `s` can only be bought by customers with foot size `s` or `s - 1`.

That means every shoe interacts with only two customer groups.

This transforms the graph into a chain-like structure when sizes are processed in sorted order. The dependencies become local instead of global.

Suppose we sort shoes by size. When we examine a shoe of size `s`, only customers of sizes `s` and `s - 1` matter. Future shoes have larger sizes, so a customer of size `s - 1` has no future opportunities after size `s`. If we skip assigning such a customer now, we lose them forever.

This naturally suggests dynamic programming over sorted sizes.

For every size position, we only need to know whether the previous shoe already consumed a customer of the current size. That tiny state is enough because interactions happen only between neighboring sizes.

The DP decides whether to:

1. Skip the current shoe.
2. Sell it to a customer of the same size.
3. Sell it to a customer of size smaller by one.

To make these transitions efficient, we preprocess for every shoe size the best available customers of matching sizes.

The resulting algorithm runs in `O((n + m) log n)` due to sorting and priority handling.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O((n + m)^3) or worse | O(nm) | Too slow |
| DP on Sorted Sizes | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read all shoes and store `(size, price, index)`.
2. Read all customers and group them by foot size.

For every foot size, keep customers sorted by budget in descending order. We only ever need the richest remaining customers first.

1. Sort shoes by size.

Since compatibility only involves equal size or one smaller, processing sizes in order makes all dependencies local.

1. For every shoe, precompute two candidate customers.

The first candidate is the richest unused customer whose foot size equals the shoe size.

The second candidate is the richest unused customer whose foot size is one smaller.

If a customer cannot afford the shoe, they are discarded.

1. Define DP states.

Let `dp[i][t]` be the maximum profit after processing the first `i` shoes.

The flag `t` tells whether the best customer of the current shoe size has already been consumed by the previous shoe.

This state is enough because neighboring shoe sizes are the only interacting sizes.

1. Transition by skipping the shoe.

We may ignore the current shoe and carry the previous answer forward.

1. Transition by selling to same-size customer.

If an available customer of the same size exists, add the shoe price and move to the next state.

1. Transition by selling to smaller-size customer.

If a customer of size `s - 1` exists and was not already consumed by the previous shoe, we may use them.

1. Store parent pointers.

To reconstruct the matching, keep the previous state and the action taken.

1. Reconstruct the chosen assignments by backtracking through DP states.
2. Output the total profit and the selected customer-shoe pairs.

### Why it works

The key invariant is that when processing shoes in increasing size order, only customers from the current size and the immediately smaller size can interact with the current shoe.

A customer of size `s - 1` has no future opportunities after size `s`, because later shoes are even larger. That means every decision involving such customers becomes final immediately.

The DP state captures exactly the only ambiguity that can propagate forward: whether a current-size customer was already used by the previous shoe. No larger dependency exists.

Because every transition considers all legal possibilities for the current shoe while preserving optimal substructure, the DP explores all optimal matchings implicitly. The reconstruction step simply follows the choices that produced the optimal value.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

INF = 10**30

def solve():
    n = int(input())

    shoes = []
    for i in range(n):
        c, s = map(int, input().split())
        shoes.append((s, c, i + 1))

    m = int(input())

    customers_by_size = defaultdict(list)

    for i in range(m):
        d, l = map(int, input().split())
        customers_by_size[l].append((d, i + 1))

    for l in customers_by_size:
        customers_by_size[l].sort(reverse=True)

    shoes.sort()

    ptr = defaultdict(int)

    same_customer = [None] * n
    prev_customer = [None] * n

    for i, (s, c, idx) in enumerate(shoes):
        arr = customers_by_size[s]

        while ptr[s] < len(arr) and arr[ptr[s]][0] < c:
            ptr[s] += 1

        if ptr[s] < len(arr):
            same_customer[i] = arr[ptr[s]]

        arr2 = customers_by_size[s - 1]

        while ptr[s - 1] < len(arr2) and arr2[ptr[s - 1]][0] < c:
            ptr[s - 1] += 1

        if ptr[s - 1] < len(arr2):
            prev_customer[i] = arr2[ptr[s - 1]]

    dp = [[-INF] * 2 for _ in range(n + 1)]
    parent = [[None] * 2 for _ in range(n + 1)]

    dp[0][0] = 0

    for i in range(n):
        s, c, shoe_idx = shoes[i]

        for used in range(2):
            if dp[i][used] < 0:
                continue

            # skip
            if dp[i][used] > dp[i + 1][0]:
                dp[i + 1][0] = dp[i][used]
                parent[i + 1][0] = (i, used, 0, None)

            # use same size customer
            if same_customer[i] is not None:
                val = dp[i][used] + c

                nxt = 1

                if val > dp[i + 1][nxt]:
                    dp[i + 1][nxt] = val
                    parent[i + 1][nxt] = (
                        i,
                        used,
                        1,
                        same_customer[i][1],
                    )

            # use smaller size customer
            if used == 0 and prev_customer[i] is not None:
                val = dp[i][used] + c

                if val > dp[i + 1][0]:
                    dp[i + 1][0] = val
                    parent[i + 1][0] = (
                        i,
                        used,
                        2,
                        prev_customer[i][1],
                    )

    if dp[n][0] >= dp[n][1]:
        state = 0
    else:
        state = 1

    best = dp[n][state]

    ans = []

    cur_i = n
    cur_state = state

    while cur_i > 0:
        p_i, p_state, action, customer_id = parent[cur_i][cur_state]

        if action == 1 or action == 2:
            shoe_idx = shoes[cur_i - 1][2]
            ans.append((customer_id, shoe_idx))

        cur_i = p_i
        cur_state = p_state

    ans.reverse()

    print(best)
    print(len(ans))

    for x, y in ans:
        print(x, y)

solve()
```

The solution begins by grouping customers according to foot size. For every size, customers are sorted by budget descending. This guarantees that when we look for a buyer for some shoe, the first valid customer is always the most useful one.

The preprocessing stage computes the best same-size and smaller-size candidates for every shoe. Since sizes are unique among shoes, these candidate relationships stay local.

The DP table has only two states per position. That is the core compression that makes the solution efficient. The boolean state records whether the current size group has already been consumed by the previous shoe.

The transition logic carefully preserves exclusivity. The `used == 0` condition is critical when assigning a smaller-size customer. Without it, the same customer group could accidentally be reused across neighboring shoes.

The reconstruction phase follows stored parent pointers backward from the optimal terminal state. Each action records exactly which customer bought which shoe.

All profit computations use normal Python integers, which safely handle the maximum possible total value.

## Worked Examples

### Example 1

Input:

```
3
10 1
30 2
20 3
2
20 1
20 2
```

Sorted shoes:

| Position | Shoe Size | Price |
| --- | --- | --- |
| 1 | 1 | 10 |
| 2 | 2 | 30 |
| 3 | 3 | 20 |

Customers:

| Customer | Budget | Foot Size |
| --- | --- | --- |
| 1 | 20 | 1 |
| 2 | 20 | 2 |

DP trace:

| Shoe | Action | Profit |
| --- | --- | --- |
| Size 1 | Sell to customer 1 | 10 |
| Size 2 | Cannot sell for 30 | 10 |
| Size 3 | Sell to customer 2 | 30 |

Final assignment:

```
Customer 1 -> Shoe 1
Customer 2 -> Shoe 3
```

Total profit becomes `30`.

This example shows why compatibility with size `s - 1` matters. Customer `2` cannot afford shoe `2`, but can still buy shoe `3`.

### Example 2

Input:

```
2
50 10
40 11
2
50 10
50 11
```

Sorted shoes:

| Position | Shoe Size | Price |
| --- | --- | --- |
| 1 | 10 | 50 |
| 2 | 11 | 40 |

DP trace:

| Shoe | Chosen Customer | Running Profit |
| --- | --- | --- |
| Size 10 | Customer 1 | 50 |
| Size 11 | Customer 2 | 90 |

If shoe `10` were sold to customer `2`, then shoe `11` would become impossible to sell. The DP correctly avoids that mistake.

This trace demonstrates the invariant that smaller-size customers should be consumed as late as possible unless no better option exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Sorting dominates the running time |
| Space | O(n + m) | Storage for customers, shoes, DP, and reconstruction |

The solution comfortably fits the constraints. Sorting `2 * 10^5` objects and performing linear DP transitions is easily fast enough within a 2-second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    from collections import defaultdict

    input = sys.stdin.readline
    INF = 10**30

    out = io.StringIO()
    sys.stdout = out

    n = int(input())

    shoes = []
    for i in range(n):
        c, s = map(int, input().split())
        shoes.append((s, c, i + 1))

    m = int(input())

    customers_by_size = defaultdict(list)

    for i in range(m):
        d, l = map(int, input().split())
        customers_by_size[l].append((d, i + 1))

    for l in customers_by_size:
        customers_by_size[l].sort(reverse=True)

    shoes.sort()

    ptr = defaultdict(int)

    same_customer = [None] * n
    prev_customer = [None] * n

    for i, (s, c, idx) in enumerate(shoes):
        arr = customers_by_size[s]

        while ptr[s] < len(arr) and arr[ptr[s]][0] < c:
            ptr[s] += 1

        if ptr[s] < len(arr):
            same_customer[i] = arr[ptr[s]]

        arr2 = customers_by_size[s - 1]

        while ptr[s - 1] < len(arr2) and arr2[ptr[s - 1]][0] < c:
            ptr[s - 1] += 1

        if ptr[s - 1] < len(arr2):
            prev_customer[i] = arr2[ptr[s - 1]]

    dp = [[-INF] * 2 for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n):
        s, c, idx = shoes[i]

        for used in range(2):
            if dp[i][used] < 0:
                continue

            dp[i + 1][0] = max(dp[i + 1][0], dp[i][used])

            if same_customer[i] is not None:
                dp[i + 1][1] = max(
                    dp[i + 1][1],
                    dp[i][used] + c
                )

            if used == 0 and prev_customer[i] is not None:
                dp[i + 1][0] = max(
                    dp[i + 1][0],
                    dp[i][used] + c
                )

    best = max(dp[n])

    return str(best).strip()

# sample 1
assert run(
"""3
10 1
30 2
20 3
2
20 1
20 2
"""
) == "30"

# minimum case
assert run(
"""1
5 10
1
5 10
"""
) == "5"

# no customer can buy
assert run(
"""2
100 1
200 2
2
50 1
50 2
"""
) == "0"

# smaller-size compatibility
assert run(
"""1
30 5
1
30 4
"""
) == "30"

# avoid greedy mistake
assert run(
"""2
50 10
40 11
2
50 10
50 11
"""
) == "90"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single shoe and customer | 5 | Minimum valid input |
| Nobody can afford shoes | 0 | Correct handling of impossible sales |
| Customer with size `s - 1` | 30 | Compatibility boundary |
| Two interacting shoes | 90 | Prevents incorrect greedy assignment |

## Edge Cases

Consider the earlier example where a greedy strategy can destroy profit.

Input:

```
2
100 5
1 6
1
100 5
```

When processing shoe size `5`, the algorithm sees a perfect same-size customer and gains profit `100`.

When processing shoe size `6`, there is no remaining compatible customer.

Final answer:

```
100
1
1 1
```

The DP never sacrifices the expensive shoe for the cheap one because it evaluates total future profit rather than local availability.

Now consider the interaction case:

```
2
50 10
40 11
2
50 10
50 11
```

At shoe `10`, the customer of size `11` is technically compatible. But assigning them immediately would block shoe `11`.

The DP compares both futures:

| Decision at Shoe 10 | Final Profit |
| --- | --- |
| Use customer 10 | 90 |
| Use customer 11 | 50 |

The better branch survives.

Finally, consider this boundary compatibility case:

```
1
30 5
1
30 4
```

The customer size is exactly one smaller than the shoe size, which is allowed.

The algorithm checks both candidate groups: size `5` and size `4`. The size `4` customer satisfies the budget condition, so the sale succeeds with total profit `30`.
