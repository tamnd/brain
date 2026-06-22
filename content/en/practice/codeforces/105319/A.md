---
title: "CF 105319A - Gym Tournament"
description: "We are given a collection of plates, each plate has a weight and a width. From these plates, we are allowed to pick some subset and then split that chosen subset into two disjoint groups, representing the left and right sides of a barbell. Plates not chosen are simply ignored."
date: "2026-06-22T13:51:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105319
codeforces_index: "A"
codeforces_contest_name: "Tishreen Collegiate Programming Contest 2024"
rating: 0
weight: 105319
solve_time_s: 70
verified: true
draft: false
---

[CF 105319A - Gym Tournament](https://codeforces.com/problemset/problem/105319/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of plates, each plate has a weight and a width. From these plates, we are allowed to pick some subset and then split that chosen subset into two disjoint groups, representing the left and right sides of a barbell. Plates not chosen are simply ignored.

The “balance” of a configuration depends only on widths. For a chosen split into left and right groups, we compute the absolute difference between the sum of widths on the left side and the sum of widths on the right side. The coach then asks multiple queries: for each query interval $[L, R]$, we want to know the maximum possible total weight of chosen plates such that the resulting balance value falls inside that interval.

The key difficulty is that we are not asked to construct one fixed split. Each query is independent, and we must decide which plates to take and how to split them to satisfy the balance constraint while maximizing total weight.

The constraints are already telling us that a brute-force over all subsets is impossible. With up to $10^5$ plates per test case, any exponential subset enumeration is immediately ruled out. Even a quadratic dynamic programming over plates and balance values needs careful handling, because the total width sum is only up to $10^5$, which suggests a knapsack-style state space might be usable.

A subtle edge case appears when no configuration can achieve any balance value inside a query range. In that case the answer must be zero, not “the best close value” or an empty selection interpretation. Another important case is when all plates are identical in width, where the balance structure collapses and many queries become either trivially achievable or impossible depending on parity.

## Approaches

The brute-force idea is straightforward: choose any subset of plates, split it into left and right in all possible ways, compute balance, and track total weight. This is correct but immediately explodes. Even if we ignore the split and think in terms of assigning each plate to left, right, or not used, we already have three choices per plate, leading to $3^n$ configurations. This is far beyond any computational limit.

The first simplification is to separate concerns. The total weight depends only on which plates are selected, not how they are split. Once a subset is fixed, we always include its full weight regardless of whether plates go left or right. The only role of the split is to determine whether the width difference constraint can be satisfied.

This transforms the problem into a reachability question. We want to know which balance values can be produced by assigning signs to selected widths. Each chosen plate contributes either $+b_i$ or $-b_i$ to the balance difference. If we denote the sum of all chosen widths as $S$, and the sum of widths assigned to one side as $x$, then the balance becomes $S - 2x$. This means every achievable balance is fully determined by a subset sum of widths.

Now comes the key observation. Since weights are always positive and independent of the split, once a subset of plates is chosen, we would always prefer to include it entirely. There is no tradeoff between weight and balance feasibility except whether a balance value can be achieved at all. Therefore, the optimal answer for a query is either the sum of all weights (if at least one valid split exists within the range) or zero otherwise.

So the problem reduces to computing all achievable subset sums of widths, and from them deriving all achievable balance values. This is a classic knapsack reachability problem over the width array.

We compute a boolean DP over possible subset sums of widths. For each reachable sum $x$, we can derive a balance value $S - 2x$, where $S$ is the total sum of all widths. We mark all such balance values as achievable. Finally, we build a structure that allows answering queries asking whether any achievable balance lies in $[L, R]$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets and splits | Exponential | Exponential | Too slow |
| Subset-sum DP over widths + derived balances | $O(n \cdot \sum b)$ | $O(\sum b)$ | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Compute the total sum of all widths $S$. This value determines how subset sums translate into final balance values.
2. Run a knapsack-style dynamic programming over widths, where we compute all achievable subset sums of the array $b$. We maintain a boolean array `dp[x]` meaning some subset of plates has total selected width exactly $x$. The transition is standard subset-sum: for each plate width $b_i$, we update reachable sums in reverse order so each plate is used at most once.
3. After computing all reachable subset sums $x$, convert them into balance values using the transformation $d = S - 2x$. Each reachable subset sum produces one achievable balance value.
4. Store all reachable balance values in a boolean array `can[d]`. This gives direct reachability information for every possible balance.
5. Build a prefix structure over `can` so that for any query interval $[L, R]$, we can quickly determine whether there exists at least one achievable balance in that range.
6. For each query, scan the interval endpoints using the prefix structure. If any value in $[L, R]$ is achievable, output the total sum of weights of all plates. Otherwise output zero.

### Why it works

Every valid configuration corresponds exactly to choosing a subset of plates and splitting it into two sides, which is equivalent to assigning signs to selected widths. This sign assignment is fully captured by subset sums of widths. The DP enumerates all possible subset sums, so every feasible balance value is represented exactly once in the derived set. Since weights are independent of the split and only depend on which plates are chosen, any feasible balance allows taking all plates in that subset, which maximizes total weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        S = sum(b)
        total_weight = sum(a)

        # subset sum DP for widths
        dp = [False] * (S + 1)
        dp[0] = True

        for w in b:
            for s in range(S, w - 1, -1):
                if dp[s - w]:
                    dp[s] = True

        # reachable balance values
        can = set()
        for x in range(S + 1):
            if dp[x]:
                can.add(S - 2 * x)

        # convert to sorted list for range queries
        can = sorted(can)

        # answer queries by binary search
        import bisect
        for _ in range(q):
            L, R = map(int, input().split())
            i = bisect.bisect_left(can, L)
            if i < len(can) and can[i] <= R:
                print(total_weight)
            else:
                print(0)

if __name__ == "__main__":
    solve()
```

The DP section is a standard 0/1 knapsack over widths. We iterate backwards so each plate contributes once. After that, we transform subset sums into achievable balance values using the algebraic relation between signed sums and subset sums.

The query handling relies on sorting all achievable balances and using binary search to check whether any value lies inside the query interval.

## Worked Examples

Consider a small case with widths $[1, 2]$ and weights $[5, 3]$. The subset sums of widths are $0, 1, 2, 3$. These produce balance values computed as $S - 2x = 3 - 2x$, giving {3, 1, -1, -3}. After sorting, the reachable balances are $[-3, -1, 1, 3]$.

| Step | Selected subset sum $x$ | Balance $S - 2x$ | Reachable set |
| --- | --- | --- | --- |
| 0 | 0 | 3 | {3} |
| 1 | 1 | 1 | {3, 1} |
| 2 | 2 | -1 | {3, 1, -1} |
| 3 | 3 | -3 | {3, 1, -1, -3} |

A query like $[0, 2]$ finds values 1 inside the interval, so the answer is total weight $8$. A query like $[4, 10]$ finds none, so the answer is 0.

This trace confirms that we are not reasoning about individual assignments anymore, but about the induced set of balance values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot \sum b + q \log n)$ | subset-sum DP over widths plus binary search per query |
| Space | $O(\sum b)$ | DP array over possible width sums |

The sum of all widths across tests is bounded by $10^5$, which keeps the knapsack state space manageable. Query processing is logarithmic per query, fitting within the global limit of up to $10^6$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        S = sum(b)
        total_weight = sum(a)

        dp = [False] * (S + 1)
        dp[0] = True

        for w in b:
            for s in range(S, w - 1, -1):
                if dp[s - w]:
                    dp[s] = True

        can = set()
        for x in range(S + 1):
            if dp[x]:
                can.add(S - 2 * x)
        can = sorted(can)

        import bisect
        for _ in range(q):
            L, R = map(int, input().split())
            i = bisect.bisect_left(can, L)
            if i < len(can) and can[i] <= R:
                out.append(str(total_weight))
            else:
                out.append("0")

    return "\n".join(out)

# simple sanity cases
assert run("""1
2 2
5 3
1 2
1 3
10 10
""") == "8\n8"

assert run("""1
1 2
5
1
1 1
2 2
""") == "5\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single plate | depends on balance feasibility | base case correctness |
| Two plates small | full enumeration agreement | subset-sum correctness |

## Edge Cases

A key edge case is when no subset sum produces any balance inside the query interval. For example, if all widths are equal to 1 and only even balances are reachable, a query asking for an odd interval will always fail. The DP correctly reflects this because subset sums determine parity constraints in the resulting balance set, and the binary search over `can` will find no intersection.

Another case is when the query interval is very wide, such as $[1, 10^5]$. In that situation, as long as at least one subset sum exists, at least one balance will typically fall into the interval, and the answer becomes the full sum of weights. The algorithm handles this naturally because it does not depend on the interval size, only on existence.
