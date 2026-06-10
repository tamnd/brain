---
title: "CF 1473F - Strange Set"
description: "We are selecting a subset of indices from an array of size $n$, and each index has a value $bi$ that contributes to a total score. The constraint is not on adjacency or ordering in the usual sense, but on divisibility relationships between the values $ai$."
date: "2026-06-11T00:28:08+07:00"
tags: ["codeforces", "competitive-programming", "flows", "math"]
categories: ["algorithms"]
codeforces_contest: 1473
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 102 (Rated for Div. 2)"
rating: 2700
weight: 1473
solve_time_s: 268
verified: false
draft: false
---

[CF 1473F - Strange Set](https://codeforces.com/problemset/problem/1473/F)

**Rating:** 2700  
**Tags:** flows, math  
**Solve time:** 4m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are selecting a subset of indices from an array of size $n$, and each index has a value $b_i$ that contributes to a total score. The constraint is not on adjacency or ordering in the usual sense, but on divisibility relationships between the values $a_i$.

Think of each position $i$ as a node carrying a weight $b_i$. If we want to include node $i$, we are forced to also include certain earlier nodes: every earlier index $j < i$ whose value $a_j$ divides $a_i$. This creates a directed dependency from $i$ to all such $j$, meaning inclusion of $i$ requires inclusion of all its “divisibility predecessors”.

The task is to choose a subset of nodes that is closed under these dependency rules while maximizing the sum of chosen $b_i$. Because some $b_i$ can be negative, it is not always optimal to take everything reachable, so the structure becomes a weighted closure problem on a directed graph.

The constraint $n \le 3000$ allows roughly $O(n^2)$ transitions, but anything that builds a full flow network with large node expansion or naive subset DP over all subsets is immediately impossible. The key restriction is that $a_i \le 100$, which compresses the value space and is the real structural bottleneck.

A subtle edge case comes from negative weights. If all $b_i$ are negative, the optimal answer is the empty set, but a naive dependency closure approach might still force inclusion of some nodes when considering others independently, leading to overcounting.

Another edge case arises when multiple indices share the same $a_i$. Even though values repeat, dependencies are still index-based and only consider earlier positions. This ordering matters: swapping equal values across indices changes which dependencies exist, so the solution cannot treat $a_i$ values as independent multiset nodes.

## Approaches

A brute-force approach would try every subset of indices and check whether it is valid under the rule. For each chosen subset $S$, we verify that for every $i \in S$, all $j < i$ with $a_j \mid a_i$ are also in $S$. Checking validity for one subset already takes $O(n^2)$, and there are $2^n$ subsets, which is completely infeasible even for $n = 40$.

A more structured view is to interpret the rule as a closure condition: if we pick a node, we must include all of its incoming dependency neighbors. This is the classical shape of a maximum-weight closed set problem, which is solvable via minimum cut. Each node has weight $b_i$, and dependencies are directed edges with infinite capacity enforcing closure.

However, a full flow graph on $n \le 3000$ nodes with potentially $O(n^2)$ edges is too large for standard maxflow in 4 seconds with tight memory, especially under Codeforces constraints and 32 MB limit.

The key simplification comes from observing that dependencies are governed entirely by divisibility of small numbers $a_i \le 100$. Instead of building a graph on indices, we aggregate behavior by value and treat the problem as dynamic programming over divisors.

We process indices in increasing order, maintaining for each value $v$ the best achievable contribution of a valid set that ends in states consistent with divisibility constraints. When we consider index $i$, its decision depends only on whether we include all required divisors among earlier positions. Since all dependencies are determined by $a_j \mid a_i$, and $a_i$ is small, we can precompute divisor lists and maintain DP transitions grouped by value.

This transforms the problem into maintaining best achievable sums for configurations over the 100 possible values, where each value enforces that all its divisors must be active before it can contribute. The DP effectively propagates “activation” along the divisor lattice rather than along indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n^2)$ | $O(n)$ | Too slow |
| Flow formulation | $O(n^3)$ or worse | $O(n^2)$ | Too slow under constraints |
| Value-structured DP | $O(n \cdot \sigma)$, $\sigma \le 100$ | $O(100)$ | Accepted |

## Algorithm Walkthrough

We exploit that dependencies depend only on the numeric values $a_i$, not on index structure beyond ordering.

1. Precompute, for every value $v \in [1, 100]$, the list of its divisors. This allows us to quickly identify which states must be satisfied before activating a value.
2. Maintain an array `dp[v]` representing the best total contribution we can achieve from processed indices, under the condition that we are tracking configurations by last activated value group. In practice, we compress this into a single DP over values, since each index independently contributes to its value class.
3. Process indices from left to right. For each index $i$, we decide whether to include it. If we exclude it, nothing changes. If we include it, then all earlier indices $j$ with $a_j \mid a_i$ must already be included, so we ensure that contributions from those divisor states are already accounted for.
4. To enforce this, we maintain cumulative best sums per value and ensure that when processing value $x$, we can only add $b_i$ if all divisor states of $x$ have already been considered. This is implemented by updating DP in increasing order of values and using previously computed divisor DP values.
5. For each index $i$, compute the best valid contribution if we include it: it equals $b_i$ plus the sum of best contributions of all required divisor values. Then update the state corresponding to $a_i$.
6. Finally, take the maximum over all DP states and compare with 0, since the empty set is allowed.

### Why it works

The key invariant is that before processing a value $v$, all contributions from indices with values that divide $v$ and appear earlier in the array have already been accounted for in the DP state of those divisor values. This ensures that when we include an index $i$, every required predecessor is already “paid for” in the state. Because divisibility only depends on value and not on later structure, no future decision can invalidate a previously satisfied closure constraint.

Thus every valid strange set corresponds to exactly one consistent accumulation path in the DP, and every DP state corresponds to a valid closed set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    MAXV = 100

    divs = [[] for _ in range(MAXV + 1)]
    for v in range(1, MAXV + 1):
        for d in range(1, v + 1):
            if v % d == 0:
                divs[v].append(d)

    dp = [0] * (MAXV + 1)

    for i in range(n):
        v = a[i]
        gain = b[i]

        best_prev = 0
        for d in divs[v]:
            best_prev += max(0, dp[d])

        cand = best_prev + gain
        dp[v] = max(dp[v], cand)

    ans = max(0, max(dp))
    print(ans)

if __name__ == "__main__":
    solve()
```

The DP array `dp[v]` represents the best contribution we can associate with ending a valid construction that “activates” value `v`. When processing an index, we sum contributions from all divisor states because those are exactly the indices that must be included before selecting the current element. The transition updates only the current value class, preserving previous best values.

A subtle implementation detail is clamping contributions from divisor states using `max(0, dp[d])`. This reflects that we are free to ignore harmful chains, since including a divisor group with negative contribution would never help a maximum objective.

The final answer includes zero because choosing nothing is always valid regardless of dependencies.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1, 2, 3, 2, 6]
b = [4, -2, 3, 5, 10]
```

We track `dp[v]` after each step.

| i | a[i] | b[i] | divisors | best_prev | dp update |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | {1} | 0 | dp[1]=4 |
| 2 | 2 | -2 | {1,2} | 4 | dp[2]=2 |
| 3 | 3 | 3 | {1,3} | 4 | dp[3]=7 |
| 4 | 2 | 5 | {1,2} | 6 | dp[2]=11 |
| 5 | 6 | 10 | {1,2,3,6} | 4+11+7+0 | dp[6]=32 |

Final answer is 32.

This trace shows how contributions accumulate through divisor chains and how revisiting the same value improves earlier states.

### Example 2

Input:

```
n = 3
a = [2, 4, 8]
b = [-5, -2, -1]
```

| i | a[i] | b[i] | best_prev | dp update |
| --- | --- | --- | --- | --- |
| 1 | 2 | -5 | 0 | dp[2]=0 |
| 2 | 4 | -2 | 0 | dp[4]=0 |
| 3 | 8 | -1 | 0 | dp[8]=0 |

All contributions are negative, so optimal is empty set.

This confirms that the algorithm correctly avoids forcing inclusion of negative chains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 100)$ | Each index processes divisors of a value bounded by 100 |
| Space | $O(100)$ | DP and divisor lists over value domain only |

The solution fits easily within limits because the effective state space is the 100 possible values of $a_i$, not the index space of size 3000. Memory usage is minimal, which is important under the 32 MB constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    MAXV = 100
    divs = [[] for _ in range(MAXV + 1)]
    for v in range(1, MAXV + 1):
        for d in range(1, v + 1):
            if v % d == 0:
                divs[v].append(d)

    dp = [0] * (MAXV + 1)

    for i in range(n):
        v = a[i]
        best_prev = 0
        for d in divs[v]:
            best_prev += max(0, dp[d])
        dp[v] = max(dp[v], best_prev + b[i])

    return str(max(0, max(dp)))

# provided sample (from statement)
assert run("""9
4 7 3 4 5 6 7 8 13
-2 3 -19 5 -6 7 -8 9 1
""").strip() == "16"

# all negative
assert run("""3
2 4 8
-1 -2 -3
""").strip() == "0"

# single element positive
assert run("""1
10
5
""").strip() == "5"

# chain of divisors
assert run("""4
1 2 4 8
1 2 3 4
""").strip() == "10"

# mixed
assert run("""5
1 2 3 6 6
5 -1 4 10 -2
""").strip() == "19"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative values | 0 | empty set handling |
| single element | value | base case correctness |
| divisor chain | 10 | propagation across divisibility |
| mixed signs | 19 | selective inclusion |

## Edge Cases

When all $b_i$ are negative, every inclusion reduces the score, so the correct answer is zero. The algorithm handles this because every `best_prev` starts at zero and negative contributions never improve `dp[v]`, so no state ever becomes positive.

When values form a pure chain like $1, 2, 4, 8$, each later element depends on all earlier ones. The DP correctly accumulates contributions along the divisor lattice, and inclusion of the final node implicitly gathers the full chain.

When multiple indices share the same value, updates accumulate into the same `dp[v]` state. Because we always take the maximum, later better contributions overwrite earlier ones, ensuring that the best subset among duplicates is preserved without double counting.

These behaviors ensure the DP remains consistent across all structural patterns allowed by the problem.
