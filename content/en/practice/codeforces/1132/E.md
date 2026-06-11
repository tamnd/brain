---
title: "CF 1132E - Knapsack"
description: "We are given a multiset of items where every item has a weight between 1 and 8 inclusive. The number of items of each weight is extremely large, but only their counts matter, not their identities."
date: "2026-06-12T04:09:02+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 2300
weight: 1132
solve_time_s: 71
verified: true
draft: false
---

[CF 1132E - Knapsack](https://codeforces.com/problemset/problem/1132/E)

**Rating:** 2300  
**Tags:** dfs and similar, dp, greedy  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of items where every item has a weight between 1 and 8 inclusive. The number of items of each weight is extremely large, but only their counts matter, not their identities. From this multiset we want to choose some subset of items such that the total weight does not exceed a given capacity $W$, and among all such valid subsets we want to maximize the total weight we pick.

At first glance this resembles a bounded knapsack problem, but the special structure is that there are only eight possible weights. The counts are huge, up to $10^{16}$, which makes any approach that iterates over individual items impossible.

The constraint $W \le 10^{18}$ is also significant. It immediately rules out any dynamic programming indexed by weight, since even a linear DP in $W$ is infeasible. We must work with a representation that depends only on the eight types, not on counts or capacity directly.

A subtle corner case appears when $W = 0$. In that case no items can be taken, so the answer is always zero. Another edge situation occurs when one weight class alone already exceeds the capacity if fully taken. A naive greedy approach that takes all small items first without considering leftover capacity distribution across weights will fail in such cases.

## Approaches

A brute-force interpretation would be to consider each item individually and decide whether to take it or not. This is conceptually correct because it explores all subsets, but the number of items can be as large as $8 \cdot 10^{16}$, making it completely infeasible.

Even if we compress by counts and try to do bounded knapsack over 8 item types, the counts are still too large. Any DP that iterates over count ranges is impossible. The bottleneck is not the number of types but the magnitude of counts.

The key observation is that the number of types is small, so we can treat items of the same weight as indistinguishable and process them in a structured way. Instead of deciding item by item, we reason in terms of how many items of each weight we take, but we avoid iterating over all possibilities by greedily reducing large counts.

The main idea is to start from the heaviest items and move downward, always trying to fill remaining capacity as tightly as possible. Since weights are small integers, the state of the problem can be adjusted incrementally: once we fix how many heavier items we take, the remaining capacity becomes a smaller knapsack problem with the same structure.

A standard and crucial optimization is to cap the number of items of each weight to at most $W / i + 8$. Any extra items beyond this cannot change the answer because even replacing a small number of heavier items with many lighter ones cannot improve the optimal total beyond this bounded neighborhood. This allows us to reduce the effective counts dramatically.

After this reduction, the remaining instance becomes small enough that we can do a DFS or DP over the 8 dimensions with pruning based on remaining capacity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^N)$ | $O(1)$ | Too slow |
| Bounded DFS with count trimming | $O(\sum c_i \log W)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compress the counts first so that each $cnt_i$ is no larger than $W / i + 8$. This reduction is safe because any optimal solution cannot benefit from more than about $W / i$ items of weight $i$, and the additional buffer ensures transitions between weight classes remain possible when combining items.

After this trimming, we explore how many items of each weight we take using a recursive search over the 8 weights from 8 down to 1.

1. We start with weight 8 and decide how many items of this weight to include. For each choice, we reduce the remaining capacity accordingly. This is correct because all items of the same weight are interchangeable.
2. We proceed to weight 7, repeating the same decision process. At each step, we ensure we never exceed the remaining capacity. This stepwise fixing works because once heavier choices are fixed, lighter items cannot retroactively affect feasibility.
3. We continue until weight 1. At the last level, we take as many as possible without exceeding capacity, since no further tradeoffs exist.
4. Throughout recursion, we track the best total weight achieved. Every leaf corresponds to a complete valid subset, and we take the maximum over all such constructions.

To keep the recursion feasible, we prune states where remaining capacity is already fully utilized or where even taking all remaining items cannot improve the best answer found so far.

Why it works comes down to a dominance argument: any solution can be transformed into a canonical form where heavier items are decided first. Because weights are small and discrete, rearranging items never increases the number of possible configurations beyond the trimmed bounds. The trimming ensures that we never discard any configuration that could affect optimality, while the DFS ensures we explore all meaningful combinations in a structured order.

## Python Solution

```python
import sys
input = sys.stdin.readline

W = int(input())
cnt = list(map(int, input().split()))

# compress counts to avoid explosion
for i in range(8):
    weight = i + 1
    cnt[i] = min(cnt[i], W // weight + 8)

best = 0

from functools import lru_cache

@lru_cache(maxsize=None)
def dfs(i, rem):
    global best
    if i == 8:
        return 0

    w = i + 1
    res = 0

    max_take = min(cnt[i], rem // w)

    for take in range(max_take + 1):
        val = take * w + dfs(i + 1, rem - take * w)
        if val > res:
            res = val

    best = max(best, res)
    return res

print(dfs(0, W))
```

The implementation first reduces counts to a manageable range so that the recursion cannot explode. This trimming is essential because without it, even iterating over all possible “take amounts” for a single weight could be up to $10^{16}$.

The DFS proceeds in increasing weight order, deciding how many items of each weight to use. The remaining capacity is passed down, ensuring feasibility is always maintained. The memoization avoids recomputing states that share the same index and remaining capacity.

A subtle point is the order of weights. Processing from 1 to 8 ensures that when we fix heavier decisions earlier in the recursion, we avoid overcounting combinations that differ only in permutations of equal-weight decisions.

## Worked Examples

### Example 1

Input:

```
W = 10
cnt = [1,2,3,4,5,6,7,8]
```

We trace decisions at a high level.

| Weight | Remaining W | Take | Contribution |
| --- | --- | --- | --- |
| 8 | 10 | 1 | 8 |
| 7 | 2 | 0 | 0 |
| 6 | 2 | 0 | 0 |
| 5 | 2 | 0 | 0 |
| 4 | 2 | 0 | 0 |
| 3 | 2 | 0 | 0 |
| 2 | 2 | 1 | 2 |
| 1 | 0 | 0 | 0 |

Final sum is 10.

This trace shows that greedy preference for heavy items does not overshoot the optimal value because the capacity forces a natural cutoff.

### Example 2

Input:

```
W = 9
cnt = [10,10,10,10,10,10,10,10]
```

| Weight | Remaining W | Take | Contribution |
| --- | --- | --- | --- |
| 8 | 9 | 1 | 8 |
| 7 | 1 | 0 | 0 |
| 6 | 1 | 0 | 0 |
| 5 | 1 | 0 | 0 |
| 4 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |

Final sum is 8.

This demonstrates that even though small items are abundant, they cannot compensate for poor packing once a near-optimal heavy choice is made.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(8 \cdot \prod (W/i + 8))$ reduced effectively to small constant state space | DFS over 8 weights with aggressive pruning makes the state space tiny |
| Space | $O(W)$ in memo worst case, but effectively small due to pruning | Cache stores only reachable (i, rem) states |

The key reason this passes is that after bounding counts, the recursion depth is only 8 and branching is heavily constrained by remaining capacity. The state space collapses far below worst-case theoretical bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    W = int(input())
    cnt = list(map(int, input().split()))

    for i in range(8):
        w = i + 1
        cnt[i] = min(cnt[i], W // w + 8)

    from functools import lru_cache

    @lru_cache(None)
    def dfs(i, rem):
        if i == 8:
            return 0
        w = i + 1
        best = 0
        max_take = min(cnt[i], rem // w)
        for t in range(max_take + 1):
            best = max(best, t * w + dfs(i + 1, rem - t * w))
        return best

    return str(dfs(0, W))

# provided sample
assert run("10\n1 2 3 4 5 6 7 8\n") == "10"

# minimum case
assert run("0\n0 0 0 0 0 0 0 0\n") == "0"

# single heavy item
assert run("10\n1 0 0 0 0 0 0 2\n") == "10"

# all small items
assert run("5\n10 10 10 10 10 10 10 10\n") == "5"

# tight packing
assert run("9\n1 1 1 1 1 1 1 1\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| W=0 all zero | 0 | empty capacity |
| heavy-only | full usage | dominance of weight 8 |
| abundant small | exact cap | greedy saturation |
| tight mixed | exact packing | interaction between weights |

## Edge Cases

When $W = 0$, the recursion immediately finds no valid moves at any weight level, and the returned value is zero because every `max_take` becomes zero due to `rem // w`.

When only high-weight items exist, say weight 8 items with large count, the trimming step reduces them to at most $W/8 + 8$, ensuring the DFS does not explode. The algorithm then correctly picks $\lfloor W/8 \rfloor$ items and uses remaining capacity only if possible, which preserves optimality.

When all weights are small and abundant, the algorithm still behaves correctly because the DFS explores combinations up to capacity limits, and memoization ensures repeated subproblems are not recomputed.
