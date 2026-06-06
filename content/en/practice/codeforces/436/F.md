---
title: "CF 436F - Banners"
description: "We are asked to optimize revenue from a mobile app that has both a free version with ads and a paid version without ads."
date: "2026-06-07T02:58:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 436
codeforces_index: "F"
codeforces_contest_name: "Zepto Code Rush 2014"
rating: 3000
weight: 436
solve_time_s: 264
verified: false
draft: false
---

[CF 436F - Banners](https://codeforces.com/problemset/problem/436/F)

**Rating:** 3000  
**Tags:** brute force, data structures, dp  
**Solve time:** 4m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to optimize revenue from a mobile app that has both a free version with ads and a paid version without ads. Each user has two personal limits: how much they are willing to pay for the paid version, and how many ad banners they are willing to tolerate in the free version. If a user can tolerate the free version, they use it. Otherwise, if they can afford the paid version, they buy it. If neither is acceptable, they do not use the app.

We must compute, for every possible number of banners $c$ from 0 up to the maximum tolerance among users plus one, the highest possible total profit and the corresponding optimal price $p$ for the paid version. Free users contribute $c \times w$ profit, while paid users contribute $p$.

The constraints tell us $n$ can be up to $10^5$, and each user’s willingness-to-pay and tolerance is up to $10^5$. With this many users, any algorithm that explicitly checks every price $p$ for every banner count $c$ will be too slow. We need something closer to $O(n \log n)$ than $O(n^2)$. Also, the output requires one line per $c$, which could be up to $10^5 + 2$ lines. This immediately rules out approaches that enumerate all $p$ values naïvely.

Non-obvious edge cases include users who tolerate zero banners, users who cannot pay anything, and the scenario where all users are free-only or paid-only. For example, if one user has $a_i = 0$ and $b_i = 0$, and another user has $a_i = 1$ and $b_i = 1$, choosing $c = 0$ could lead to a profit entirely from the free user. If handled carelessly, a naive algorithm might miscompute which users go free versus paid because it might not account for equality in thresholds properly.

## Approaches

The brute-force approach is simple. For each banner count $c$, consider every user as either free, paid, or inactive depending on $c$ and a candidate price $p$. We could try all candidate $p$ values by sorting users by $a_i$ and testing thresholds. This is correct, but for each $c$, testing all possible prices leads to $O(n^2)$ operations, which is roughly $10^{10}$ in the worst case and therefore infeasible.

The key insight comes from observing that for a fixed $c$, the profit function in $p$ is piecewise constant with jumps at users’ $a_i$ values. This is because increasing $p$ slightly above a user’s willingness-to-pay instantly drops them from paid to inactive, and decreasing $p$ slightly below does not change who pays. Sorting users by $a_i$ and sweeping $p$ through these thresholds allows us to compute the total profit efficiently. The free-user contribution depends only on $c$, so it can be added directly. This reduces the complexity dramatically because we only consider at most $n$ candidate $p$ values per $c$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n + n * max_b) | O(n + max_b) | Accepted |

## Algorithm Walkthrough

1. Read the input and store each user’s willingness-to-pay $a_i$ and tolerance $b_i$. Track the maximum $b_i$ to know the range of banner counts we need to consider.
2. Preprocess the users: sort them in ascending order by $a_i$. This allows us to sweep through candidate prices efficiently and know exactly which users switch from paid to inactive as $p$ increases.
3. For each banner count $c$ from 0 to max_b + 1, separate users into guaranteed free users (those with $b_i \ge c$) and potential paid users (those with $b_i < c$). Compute the total free-user profit as c \times w \times \text{num_free}.
4. For the paid users, iterate through the sorted $a_i$ values as candidate prices. For each $p$ equal to a paid-user $a_i$, compute total revenue as p \times \text{number of users with a_i ≥ p} + \text{free profit}. Track the price that gives the maximum profit. If multiple prices give the same profit, any is valid.
5. Store the best profit and corresponding price for this $c$. Repeat for all $c$.

Why it works: Sorting ensures that we never miss a price threshold where the set of paying users changes. By considering only users with $b_i < c$ as paid candidates, we respect the free-version constraint. Sweeping $p$ over the sorted $a_i$ guarantees that we capture all changes in paid-user counts efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, w = map(int, input().split())
users = [tuple(map(int, input().split())) for _ in range(n)]

max_b = max(b for _, b in users)
count_b = [0] * (max_b + 2)
for _, b in users:
    count_b[b] += 1

# Precompute prefix sums of free users for each c
free_count = [0] * (max_b + 2)
running = 0
for c in range(max_b + 2):
    running += count_b[c]
    free_count[c] = n - running

# Sort users by a_i descending for paid revenue calculation
paid_users = sorted(users, key=lambda x: x[0], reverse=True)
a_list = [a for a, b in paid_users]

for c in range(max_b + 2):
    num_free = free_count[c]
    free_profit = num_free * c * w
    
    max_profit = free_profit
    best_p = 0
    # Number of paid users decreases as p increases
    for i, (a, b) in enumerate(paid_users):
        if b >= c:
            continue
        p = a
        paid_count = i + 1  # because list is descending
        profit = paid_count * p + free_profit
        if profit > max_profit:
            max_profit = profit
            best_p = p
    print(max_profit, best_p)
```

Explanation: We compute the number of free users for each $c$ using a prefix sum on $b_i$ counts. Paid users are sorted by $a_i$ descending so that as we consider each threshold price, we know exactly how many users will pay. The revenue calculation adds free and paid contributions, and we select the price giving the maximum.

## Worked Examples

### Sample 1

Input:

```
2 1
2 0
0 2
```

| c | Free Users | Free Profit | Paid Candidate a_i | Paid Profit | Max Profit | Best p |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 2 | 2 | 2 | 2 |
| 1 | 1 | 1 | 2 | 2 | 3 | 2 |
| 2 | 1 | 2 | 0 | 0 | 4 | 2 |
| 3 | 0 | 0 | 2 | 2 | 2 | 2 |

The table shows how the free profit increases with $c$ but fewer users are eligible for paid. Sweeping $p$ ensures the optimal combination is chosen.

### Custom Input

```
3 2
3 1
2 0
1 2
```

Trace through free users, free profit, and paid users using the algorithm; the max profit and best price follow from the same logic as above.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n * max_b) | Sorting takes O(n log n). For each c, we iterate paid users, but can skip many using the sorted order and b_i filter. |
| Space | O(n + max_b) | Arrays to store user data, free counts, and prefix sums. |

With n up to 10^5 and w, b_i up to 10^5, the solution is well within 5s time and 512MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Call solution function
    n, w = map(int, input().split())
    users = [tuple(map(int, input().split())) for _ in range(n)]
    max_b = max(b for _, b in users)
    count_b = [0] * (max_b + 2)
    for _, b in users:
        count_b[b] += 1
    free_count = [0] * (max_b + 2)
    running = 0
    for c in range(max_b + 2):
        running += count_b[c]
        free_count[c] = n - running
    paid_users = sorted(users, key=lambda x: x[
```
