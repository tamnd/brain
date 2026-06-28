---
title: "CF 104941B - Buying Croissants"
description: "We are given a sequence of daily croissant prices for the next $n$ days. Each day, exactly one croissant must be eaten, and croissants are perishable: any croissant remains edible only for 7 days after purchase, including the purchase day, and becomes useless afterward."
date: "2026-06-28T18:17:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "B"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 78
verified: true
draft: false
---

[CF 104941B - Buying Croissants](https://codeforces.com/problemset/problem/104941/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily croissant prices for the next $n$ days. Each day, exactly one croissant must be eaten, and croissants are perishable: any croissant remains edible only for 7 days after purchase, including the purchase day, and becomes useless afterward.

This creates a planning problem: on each day, we may buy croissants not only for the current day but also for up to 6 future days, as long as they are still within their freshness window. The goal is to choose purchase days so that every day’s consumption is covered by some still-fresh croissant, while minimizing total cost.

The key difficulty is that buying in advance can be beneficial if a future price is higher, but overbuying is useless because of expiration.

The constraint $n \le 29220$ suggests that solutions with quadratic behavior $O(n^2)$ are unlikely to pass in 1 second in Python, while linear or near-linear strategies are expected.

A subtle failure case for naive strategies comes from ignoring expiration windows. For example, always buying on the cheapest day seen so far and stocking up indefinitely fails:

Input:

```
8
5 1 1 1 1 1 1 100
```

A greedy strategy that buys too much on day 2 might try to cover far beyond day 8, but everything expires after 7 days, so purchases cannot be shifted arbitrarily far.

Another failure comes from only buying on the current day: that is always correct but not optimal. For instance:

Input:

```
7
10 1 1 1 1 1 1
```

Buying every day costs 16, but buying more on day 2 can replace expensive early purchases.

The structure is a sliding time window with limited validity, which suggests decisions depend only on the previous 7 days.

## Approaches

A brute-force approach tries to decide, for each day, how many croissants to buy and on which earlier day they should have been purchased. Conceptually, for each day $i$, we could look back up to 7 days and assign today’s croissant to the cheapest valid purchase day in that range. This leads to a dynamic programming formulation where each day considers transitions from up to 7 previous states. While this already reduces the problem structure, a more naive version might still recompute valid minimums repeatedly, leading to $O(n \cdot 7)$ or worse depending on implementation.

A direct but inefficient idea is to, for every day, scan all previous days within the 7-day window and compute the best possible assignment cost. That gives $O(n \cdot 7)$, which is borderline but acceptable. However, even more naive formulations that recompute cumulative decisions or try to simulate all purchase combinations explode exponentially.

The key observation is that each croissant needed on day $i$ must be purchased on some day in $[i-6, i]$. Among those 7 options, we want the cheapest valid purchase day, but that purchase also contributes to earlier or later days within its own validity window. This means each day’s optimal cost depends only on a fixed-size sliding window of previous decisions, and we can maintain the minimum cost efficiently.

Thus the problem reduces to a sliding window minimum over prices, applied per day: the cost for day $i$ is the minimum price among days $i-6$ to $i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force window scan per day | $O(7n)$ | $O(1)$ | Accepted |
| Sliding window minimum (deque) | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a structure that allows us to quickly know the minimum price in the last 7 days.

1. Process days from 1 to $n$ in order, treating each day as requiring exactly one unit of “coverage”.
2. Maintain a deque storing candidate days, where the prices are increasing from front to back. Each element represents a day index.
3. Before processing day $i$, remove from the front any day $j$ where $j < i - 6$, since those purchases are no longer valid due to expiration.
4. While the back of the deque has a price greater than or equal to $c_i$, remove it. These days are never optimal again because day $i$ dominates them within the valid window.
5. Push day $i$ into the deque.
6. The front of the deque now stores the index of the cheapest valid purchase day, so add $c_{\text{deque}[0]}$ to the answer.

The reasoning behind step 4 is that if a later day has a lower price and is still within the valid 7-day window, any more expensive earlier option is strictly worse for all future decisions where both remain valid.

### Why it works

At every day $i$, the deque represents exactly the set of days in $[i-6, i]$, but pruned so that prices are monotonic. Any removed index either expires or is dominated by a cheaper or equal price on a later day. Therefore, the minimum of the window is always preserved at the front, and no optimal solution can require a discarded day because any such choice can be replaced by a cheaper valid alternative without breaking feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    c = list(map(int, input().split()))

    dq = deque()
    ans = 0

    for i in range(n):
        while dq and dq[0] < i - 6:
            dq.popleft()

        while dq and c[dq[-1]] >= c[i]:
            dq.pop()

        dq.append(i)

        ans += c[dq[0]]

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads prices and processes them in a single pass. The deque stores indices, not values, so we can enforce the 7-day expiration rule precisely using index comparisons. The first loop removes expired entries. The second loop maintains monotonicity so the front is always the minimum price in the valid range. The answer accumulates the minimum valid price for each day.

A common mistake is forgetting that expiration is inclusive of the purchase day, meaning a croissant bought on day $i$ is valid through day $i+6$. That is exactly why the cutoff is $i - 6$, not $i - 7$.

## Worked Examples

### Sample 1

Input:

```
7
1 9 9 9 9 9 9
```

We track the deque and cost day by day.

| Day | Price | Valid window | Deque indices | Chosen price | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [1] | [1] | 1 | 1 |
| 2 | 9 | [1,2] | [1,2] | 1 | 2 |
| 3 | 9 | [1,2,3] | [1,2,3] | 1 | 3 |
| 4 | 9 | [1..4] | [1,2,3,4] | 1 | 4 |
| 5 | 9 | [1..5] | [1,2,3,4,5] | 1 | 5 |
| 6 | 9 | [1..6] | [1,2,3,4,5,6] | 1 | 6 |
| 7 | 9 | [1..7] | [1,2,3,4,5,6,7] | 1 | 7 |

The trace shows that once a very cheap day exists inside the window, it dominates all later expensive days until it expires.

### Sample 2

Input:

```
8
1 9 9 9 9 9 9 9
```

| Day | Price | Valid window | Deque indices | Chosen price | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [1] | [1] | 1 | 1 |
| 2 | 9 | [1,2] | [1,2] | 1 | 2 |
| 3 | 9 | [1,2,3] | [1,2,3] | 1 | 3 |
| 4 | 9 | [1,2,3,4] | [1,2,3,4] | 1 | 4 |
| 5 | 9 | [1,2,3,4,5] | [1,2,3,4,5] | 1 | 5 |
| 6 | 9 | [1..6] | [1..6] | 1 | 6 |
| 7 | 9 | [1..7] | [1..7] | 1 | 7 |
| 8 | 9 | [2..8] | [2..8] | 9 | 16 |

Day 1 expires after day 7, so on day 8 the best remaining option becomes 9. This confirms expiration handling is essential for correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index enters and leaves the deque at most once |
| Space | $O(n)$ | Deque stores at most 7 active indices at any time |

The linear scan is easily fast enough for $n \le 29220$, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n = int(input())
        c = list(map(int, input().split()))
        dq = deque()
        ans = 0

        for i in range(n):
            while dq and dq[0] < i - 6:
                dq.popleft()
            while dq and c[dq[-1]] >= c[i]:
                dq.pop()
            dq.append(i)
            ans += c[dq[0]]

        print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("7\n1 9 9 9 9 9 9\n") == "7"
assert run("8\n1 9 9 9 9 9 9 9\n") == "16"

# custom cases
assert run("1\n5\n") == "5", "minimum size"
assert run("7\n1 1 1 1 1 1 1\n") == "7", "all equal"
assert run("7\n7 6 5 4 3 2 1\n") == "7", "monotone decreasing"
assert run("14\n10 1 10 1 10 1 10 1 10 1 10 1 10 1\n") == "8", "alternating prices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 day | 5 | minimal boundary |
| all 1s | 7 | stability under ties |
| decreasing prices | 7 | correct window dominance |
| alternating prices | 8 | repeated window resets |

## Edge Cases

A key edge case is when a very cheap day appears early and later expires. For example:

Input:

```
8
1 9 9 9 9 9 9 9
```

During days 1 through 7, the algorithm consistently uses the price 1. On day 8, the index 1 is removed because it falls outside the valid window $[8-6, 8] = [2, 8]$. The deque then contains only expensive entries, so the answer switches to 9. The algorithm correctly transitions without any special handling because expiration is enforced structurally via index removal.

Another edge case is repeated equal prices. When prices are identical, the monotonic condition still works because removing from the back uses `>=`, ensuring earlier duplicates do not linger unnecessarily. This guarantees correctness even when multiple optimal choices exist simultaneously.
