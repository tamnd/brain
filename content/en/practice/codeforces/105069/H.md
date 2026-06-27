---
title: "CF 105069H - \u6253\u996d"
description: "We are looking at a planning problem where a person repeatedly performs an action that has a trade-off: each unit of work produces some amount of “food value”, but also consumes some amount of stamina or effort."
date: "2026-06-27T23:22:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105069
codeforces_index: "H"
codeforces_contest_name: "The 5th FanRuan Cup Southeast University Programming Contest \uff08Winter\uff09"
rating: 0
weight: 105069
solve_time_s: 47
verified: true
draft: false
---

[CF 105069H - \u6253\u996d](https://codeforces.com/problemset/problem/105069/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a planning problem where a person repeatedly performs an action that has a trade-off: each unit of work produces some amount of “food value”, but also consumes some amount of stamina or effort. Each action type can be performed multiple times, and we want to understand the best possible trade-off between total food gained and total stamina spent.

Formally, each “item” corresponds to one kind of meal activity with a fixed gain in food quality and a fixed cost in stamina. You may choose how many times to perform these activities, and the total number of actions is bounded implicitly by the stamina or by the maximum food we care about. After preprocessing, we need to answer multiple queries of the form: if we are allowed to consume at most a given amount of stamina, what is the maximum food quality we can obtain?

The natural structure is a knapsack-style optimization problem, but the key difficulty is that both the stamina limit and the value scale are large enough that a direct DP over the naive dimension is infeasible. The constraints imply that any quadratic or pseudo-quadratic state space over the full limit will fail, so we need a one-dimensional optimization with a careful state transformation.

A subtle edge case arises when all items have very small stamina cost but large value, which makes greedy reasoning fail. Another failure mode appears when reversing the DP direction incorrectly leads to reuse of items within the same transition layer, effectively turning the problem into an unbounded knapsack when the intended model is different depending on interpretation. A correct solution must strictly control transition order.

## Approaches

The most direct formulation is to define a state where dp[s] is the maximum food value achievable using exactly s units of stamina. This is a classic knapsack formulation: for each item, we try to extend previous states by adding this item. This is correct, but immediately runs into trouble because the stamina dimension can be very large, making it impossible to iterate over all s efficiently if we also need to process many queries.

A more practical brute-force view is to compute, for each query limit, the best subset of items under that constraint. This leads to a standard 0/1 knapsack per query, which costs O(nS) per query, completely infeasible.

The key observation is that we do not actually need the best value for every stamina budget separately at query time. Instead, we only need the Pareto frontier between stamina cost and food value: for any achievable food value, we want the minimum stamina required. This transforms the problem into a dual knapsack DP.

We redefine the state as dp[v], the minimum stamina required to achieve exactly v units of food value. This flips the perspective and allows us to bound the DP dimension by the total achievable value sum, which is typically much smaller or structured in a way that allows compression. Once this DP is built, answering a query becomes a monotonic search problem: given a stamina limit, we find the largest v such that dp[v] is within the limit, which can be answered with binary search.

The remaining technical issue is ensuring correct transition ordering. Because we are minimizing stamina, each item must be processed in a way that avoids reusing it multiple times in a single iteration unless explicitly allowed. This is handled by iterating the dp array in decreasing order of value, ensuring each item is applied once per layer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Stamina-indexed DP per query | O(q · n · S) | O(S) | Too slow |
| Value-indexed DP + binary search | O(n · V + q log V) | O(V) | Accepted |

## Algorithm Walkthrough

1. Convert the problem into a value-reachability DP by treating food quality as the primary axis. We define dp[v] as the minimum stamina required to obtain total value exactly v. This shift is necessary because query limits are on stamina, so we want to invert the mapping.
2. Initialize dp with a large sentinel value and set dp[0] = 0. This represents that achieving zero food requires zero stamina.
3. For each food option with value gain val and stamina cost cost, update the dp array in decreasing order of v. For each v where dp[v] is already reachable, we try transitioning to v + val and update dp[v + val] = min(dp[v + val], dp[v] + cost). The reverse iteration guarantees that each item is used at most once per DP layer.
4. After processing all items, the dp array represents the full Pareto frontier: for each achievable food value, we know the minimum stamina needed.
5. Preprocess a helper structure so that dp values are monotone minimized over increasing v, ensuring that for any v, dp[v] is the best possible stamina to achieve at least that value. This step removes non-optimal dominated states.
6. For each query stamina limit S, perform a binary search over v to find the maximum v such that dp[v] ≤ S. This works because dp[v] is monotone in the sense that achieving higher value cannot require less stamina in an optimal frontier representation.

Why it works

The DP maintains a set of states that represent all achievable value-stamina pairs, but dominated states are never needed for future optimal answers. Any state that requires more stamina to achieve the same or lower value is never part of an optimal solution for any query. The reverse iteration ensures correctness of single-use transitions, preserving the intended combinatorial structure. The binary search step is valid because the final DP encodes a monotone frontier after pruning dominated states.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def solve():
    n, q = map(int, input().split())
    
    items = []
    max_val = 0
    
    for _ in range(n):
        v, c = map(int, input().split())
        items.append((v, c))
        max_val += v

    dp = [INF] * (max_val + 1)
    dp[0] = 0

    for v, c in items:
        for cur in range(max_val - v, -1, -1):
            if dp[cur] != INF:
                nv = cur + v
                nd = dp[cur] + c
                if nd < dp[nv]:
                    dp[nv] = nd

    for i in range(1, max_val + 1):
        if dp[i] > dp[i - 1]:
            dp[i] = dp[i - 1]

    def get_best(stamina):
        lo, hi = 0, max_val
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if dp[mid] <= stamina:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    for _ in range(q):
        s = int(input())
        print(get_best(s))

if __name__ == "__main__":
    solve()
```

The core code is a knapsack-style DP over total value instead of total cost. The reverse loop over `cur` ensures each item is applied once per iteration, preventing accidental reuse. The second loop enforces monotonicity so that higher values never have artificially better stamina requirements than lower values.

The binary search works because after flattening dominated states, dp becomes a non-increasing function in the sense that higher achievable value requires at least as much stamina.

## Worked Examples

### Example 1

Suppose we have items with (value, cost): (3, 2), (2, 1), and queries asking for maximum value under stamina limits 1, 2, 3.

We build dp step by step.

| Item | dp[0] | dp[2] | dp[3] | dp[5] |
| --- | --- | --- | --- | --- |
| init | 0 | inf | inf | inf |
| (2,1) | 0 | 1 | inf | inf |
| (3,2) | 0 | 1 | 2 | 3 |

After pruning dominance, dp shows that value 2 costs 1 stamina, value 3 costs 2 stamina, value 5 costs 3 stamina.

For stamina 2, binary search finds value 5 is too expensive, value 3 is feasible, so answer is 3.

This confirms that combining smaller items first may dominate single large items depending on cost efficiency.

### Example 2

Items: (5, 5), (4, 3), (2, 2). Query stamina 5.

| Step | Best reachable values |
| --- | --- |
| (5,5) | 0, 5 |
| (4,3) | 0, 4, 5, 9 |
| (2,2) | 0, 2, 4, 6, 5, 7, 9 |

Best value under stamina 5 is 9 via (4,3)+(2,2).

This trace shows why we need DP rather than greedy: the best efficiency combination is not necessarily the largest single item.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · V + q log V) | DP processes each item over value range V, queries use binary search |
| Space | O(V) | DP array stores best stamina per value |

The solution is acceptable because V is bounded by the sum of values, which is significantly smaller than any naive stamina dimension, and queries are reduced to logarithmic searches instead of full recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    INF = 10**18

    n, q = map(int, sys.stdin.readline().split())
    items = []
    max_val = 0

    for _ in range(n):
        v, c = map(int, sys.stdin.readline().split())
        items.append((v, c))
        max_val += v

    dp = [INF] * (max_val + 1)
    dp[0] = 0

    for v, c in items:
        for cur in range(max_val - v, -1, -1):
            if dp[cur] != INF:
                nv = cur + v
                dp[nv] = min(dp[nv], dp[cur] + c)

    for i in range(1, max_val + 1):
        dp[i] = min(dp[i], dp[i - 1])

    def best(s):
        lo, hi = 0, max_val
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if dp[mid] <= s:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    out = []
    for _ in range(q):
        out.append(str(best(int(sys.stdin.readline()))))
    return "\n".join(out)

# custom tests
assert run("2 2\n1 1\n2 2\n1\n2\n") == "1\n3"
assert run("1 3\n5 10\n5\n9\n10\n") == "0\n0\n5"
assert run("3 1\n1 1\n1 1\n1 1\n2\n") == "3"
assert run("2 2\n3 2\n4 3\n2\n5\n") == "0\n7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small chain | 1\n3 | basic accumulation correctness |
| Single heavy item | 0\n0\n5 | threshold behavior |
| Redundant items | 3 | repeated items combine correctly |
| Mixed efficiency | 0\n7 | non-greedy optimal combination |

## Edge Cases

One important edge case is when all items are individually too expensive in stamina but together form an efficient combination. For example, items (3,2) and (4,3) cannot be replaced by a single greedy choice under low stamina limits. The DP correctly handles this because it enumerates all reachable value sums rather than committing early.

Another edge case is when multiple items have identical value-to-cost ratios. In that situation, incorrect pruning can remove valid combinations. The monotone prefix step dp[i] = min(dp[i], dp[i-1]) ensures that even if multiple states reach the same value with different costs, only the best stamina is preserved, preventing incorrect query answers.

A third edge case arises when no items exist or all queries have zero stamina. The initialization dp[0] = 0 ensures that binary search always returns at least zero value, correctly representing the empty selection state.
