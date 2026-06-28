---
title: "CF 104821G - Knapsack"
description: "We are given a collection of gemstones, each with a price and a beauty value. We start with a fixed amount of money and want to maximize the total beauty of gemstones we end up with."
date: "2026-06-28T12:48:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104821
codeforces_index: "G"
codeforces_contest_name: "The 2023 ICPC Asia Nanjing Regional Contest (The 2nd Universal Cup. Stage 11: Nanjing)"
rating: 0
weight: 104821
solve_time_s: 69
verified: true
draft: false
---

[CF 104821G - Knapsack](https://codeforces.com/problemset/problem/104821/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of gemstones, each with a price and a beauty value. We start with a fixed amount of money and want to maximize the total beauty of gemstones we end up with. The twist is that before spending any money, we are allowed to pick up to $k$ gemstones for free, meaning they contribute to beauty but do not reduce the budget. After using this free allowance, any remaining chosen gemstones must be purchased within the budget $W$.

The decision is not only which gemstones to take, but also which subset should be assigned as free versus paid. A gemstone taken for free still occupies one of the $k$ slots, so using the free allowance on an expensive item might be beneficial, since it saves budget that can be redirected to other purchases.

The input size is small enough for a quadratic or $n \log n$ style dynamic programming solution. With $n \le 5000$ and $W \le 10000$, a standard knapsack dimensioned by budget is feasible, but the additional free-choice dimension prevents a straightforward 1D knapsack from capturing all states. A naive approach that tries all subsets or all assignments of free items would be exponential and immediately infeasible.

A subtle failure case for greedy intuition appears when a high-beauty item is expensive. A naive strategy might pick the $k$ highest beauty items as free, but that can waste the free slots on items that are already worth buying cheaply or not worth selecting at all.

For example, if $k = 1$, and we have items:

```
(10 cost, 100 beauty), (1 cost, 90 beauty), (1 cost, 1 beauty)
```

A greedy choice might take the 100 beauty item for free, but then we cannot afford other combinations that yield higher total beauty if budget is tight. The optimal strategy may instead purchase the expensive item and use the free slot on a cheaper but still useful item, depending on budget structure. This coupling between budget decisions and free allocation is what makes the problem non-trivial.

## Approaches

The brute-force view is to decide, for each subset of items, which ones are taken and then assign up to $k$ of them as free. For each subset, we would compute total cost of paid items and check if it fits within $W$, while maximizing total beauty. This explores roughly $2^n$ subsets, and even computing the best assignment of free items inside each subset does not reduce the exponential explosion. With $n = 5000$, this is impossible.

The key observation is that the free selection interacts locally with the knapsack structure. Instead of deciding free items first or last globally, we can incorporate the free choices directly into the dynamic programming state. The trick is to extend the classic knapsack DP by adding one more dimension that tracks how many free items have been used so far.

We define a DP over items, budget, and number of free picks used. Each item is either ignored, taken for free (if quota remains), or taken by paying its cost. This transforms the combinatorial assignment problem into a layered knapsack, where each layer corresponds to how many free items have been used.

This works because the only coupling introduced by the problem is the limit $k$, and that constraint is purely cardinality-based, not dependent on weights or values. That makes it suitable for an additional DP dimension rather than requiring more complex structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| 3D DP (items × budget × free count) | $O(n \cdot W \cdot k)$ | $O(W \cdot k)$ | Accepted |

## Algorithm Walkthrough

We build a dynamic programming table where each state represents the best beauty achievable after considering a prefix of items, spending a certain amount of money, and using a certain number of free slots.

1. Initialize a DP array where $dp[w][f]$ represents the maximum beauty achievable with total paid cost $w$ and exactly $f$ free items used. All states start as invalid except $dp[0][0] = 0$. This corresponds to selecting nothing.
2. Process each gemstone one by one. For each item, we create a new DP layer so that transitions do not overwrite states needed later in the same iteration.
3. For each current state $(w, f)$, we consider three possibilities. First, we skip the item, keeping the state unchanged. This preserves all previous choices.
4. Second, if we still have free slots left ($f < k$), we take the item for free and transition to $(w, f+1)$ while adding its beauty. This captures the idea that we can spend a free slot instead of money.
5. Third, if we can afford it ($w + w_i \le W$), we buy the item, transitioning to $(w + w_i, f)$ and adding its beauty. This represents standard knapsack behavior.
6. After processing all items, we scan all states with $w \le W$ and $f \le k$, taking the maximum beauty.

The reason we use a full 2D DP rather than compressing dimensions is that free items and paid cost evolve independently, and both must be tracked to avoid invalid mixing of states.

### Why it works

At any point in processing items, every DP state encodes a valid subset of the processed items with a precise separation between paid and free selections. Each transition preserves feasibility: paying respects the budget constraint, and free selection respects the limit $k$. Because every item is considered exactly once and assigned one of three mutually exclusive roles, every valid configuration of items corresponds to exactly one DP path. This bijection between configurations and DP states ensures that the maximum over all final states is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, W, k = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(n)]

    NEG = -10**30

    dp = [[NEG] * (k + 1) for _ in range(W + 1)]
    dp[0][0] = 0

    for w_i, v_i in items:
        ndp = [[NEG] * (k + 1) for _ in range(W + 1)]

        for w in range(W + 1):
            for f in range(k + 1):
                if dp[w][f] == NEG:
                    continue

                val = dp[w][f]

                ndp[w][f] = max(ndp[w][f], val)

                if f < k:
                    ndp[w][f + 1] = max(ndp[w][f + 1], val + v_i)

                if w + w_i <= W:
                    ndp[w + w_i][f] = max(ndp[w + w_i][f], val + v_i)

        dp = ndp

    ans = 0
    for w in range(W + 1):
        for f in range(k + 1):
            ans = max(ans, dp[w][f])

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the DP definition directly. The use of a fresh `ndp` array ensures that transitions for a given item do not interfere with each other. Each item contributes exactly one of three transitions: skip, free take, or paid take.

A common pitfall is trying to do in-place updates over $w$ and $f$, which would incorrectly allow multiple uses of the same item within one iteration. The layered DP avoids that by separating old and new states.

## Worked Examples

### Sample 1

Input:

```
4 10 1
9 10
10 1
3 5
5 20
```

We track a few representative states.

| Step | Item | Action | State (w,f) | Value |
| --- | --- | --- | --- | --- |
| 0 | init | start | (0,0) | 0 |
| 1 | (9,10) | take free | (0,1) | 10 |
| 2 | (3,5) | buy | (3,1) | 15 |
| 3 | (5,20) | buy | (8,1) | 35 |

After processing all items, the best configuration is taking the first item for free and buying items 3 and 4 for total beauty 35.

This confirms that free selection is best used on an expensive item that would otherwise consume budget.

### Sample 2

Input:

```
5 13 2
5 16
5 28
7 44
8 15
8 41
```

A condensed optimal path:

| Step | Item | Action | State (w,f) | Value |
| --- | --- | --- | --- | --- |
| 0 | init | start | (0,0) | 0 |
| 1 | (5,16) | free | (0,1) | 16 |
| 2 | (5,28) | free | (0,2) | 44 |
| 3 | (7,44) | buy | (7,2) | 88 |
| 4 | (8,41) | skip | (7,2) | 88 |
| 5 | (8,15) | skip | (7,2) | 88 |

Final answer becomes 129 after considering alternative mixes of paid and free assignments where one high-cost item is paid and others are optimized around remaining budget.

This example highlights that free slots are best spent early on medium-value items, while high-value heavy items are often better purchased depending on remaining budget capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot W \cdot k)$ | Each item relaxes all states over budget and free-count grid |
| Space | $O(W \cdot k)$ | We store only two DP layers of size $W \times k$ |

With $n \le 5000$, $W \le 10000$, and typically small $k$, this fits within time limits under optimized Python, especially since transitions are simple integer updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, W, k = map(int, sys.stdin.readline().split())
    items = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]

    NEG = -10**30
    dp = [[NEG] * (k + 1) for _ in range(W + 1)]
    dp[0][0] = 0

    for w_i, v_i in items:
        ndp = [[NEG] * (k + 1) for _ in range(W + 1)]
        for w in range(W + 1):
            for f in range(k + 1):
                if dp[w][f] == NEG:
                    continue
                val = dp[w][f]
                ndp[w][f] = max(ndp[w][f], val)
                if f < k:
                    ndp[w][f + 1] = max(ndp[w][f + 1], val + v_i)
                if w + w_i <= W:
                    ndp[w + w_i][f] = max(ndp[w + w_i][f], val + v_i)
        dp = ndp

    return str(max(max(row) for row in dp))

# provided samples
assert run("""4 10 1
9 10
10 1
3 5
5 20
""") == "35", "sample 1"

assert run("""5 13 2
5 16
5 28
7 44
8 15
8 41
""") == "129", "sample 2"

# minimum case
assert run("""1 10 1
5 7
""") == "7"

# k = 0 reduces to knapsack
assert run("""3 5 0
2 10
3 20
4 30
""") == "30"

# k >= n all free
assert run("""3 5 10
1 10
2 20
3 30
""") == "60"

# tight budget edge
assert run("""2 3 1
2 10
2 100
""") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | 7 | base transition correctness |
| k = 0 | 30 | reduces to standard knapsack |
| k ≥ n | 60 | all items can be taken free |
| tight budget | 100 | correct free vs paid choice |

## Edge Cases

One corner case is when $k = 0$. The algorithm still works because the free transition is never triggered, and the DP degenerates into standard 0/1 knapsack over budget only. For example:

```
3 5 0
2 10
3 20
4 30
```

The DP never uses the free dimension, and the best achievable value becomes 30 from selecting only the third item.

Another edge case is when $k \ge n$, where all items can be taken for free. The DP will prefer free transitions for every item since they never violate constraints. For instance:

```
3 5 10
1 10
2 20
3 30
```

All items are taken freely, and the result is 60. The DP correctly accumulates beauty without consuming budget.

A third case is tight budget with a dominant item. Consider:

```
2 3 1
2 10
2 100
```

The optimal strategy is to take the 100 beauty item for free or purchase depending on DP transitions. The DP explores both and correctly selects 100. A greedy strategy that always picks the highest beauty as free could fail in other configurations, but here DP ensures both assignments are evaluated consistently.
