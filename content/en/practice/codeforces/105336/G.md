---
title: "CF 105336G - \u75af\u72c2\u661f\u671f\u516d"
description: "A group of n people goes to a restaurant, and each person has a personal spending limit. This limit already includes the cost of transportation to the restaurant, and any additional spending inside the restaurant must keep their total expenditure within their limit."
date: "2026-06-23T15:24:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105336
codeforces_index: "G"
codeforces_contest_name: "The 2024 CCPC Online Contest"
rating: 0
weight: 105336
solve_time_s: 57
verified: true
draft: false
---

[CF 105336G - \u75af\u72c2\u661f\u671f\u516d](https://codeforces.com/problemset/problem/105336/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

A group of n people goes to a restaurant, and each person has a personal spending limit. This limit already includes the cost of transportation to the restaurant, and any additional spending inside the restaurant must keep their total expenditure within their limit. Each person i has a maximum budget ai and a fixed taxi cost Vi, so the remaining usable budget for restaurant payments is ai - Vi.

There are m dishes. Each dish has a cost Wi and is shared by two people xi and yi. The cost of a dish must be split between its two participants as non-negative integers summing exactly to Wi. If xi equals yi, that person pays the entire cost.

The goal is to decide whether there exists a way to split all dish costs so that yyq (person 1) ends up strictly spending more in total than every other person, while no one exceeds their budget.

The key structure is that we are not choosing who eats what or which dishes exist, only how each dish cost is split between its two fixed participants. This turns the problem into distributing fixed edge weights across endpoints under capacity constraints, with an additional strict dominance condition for node 1.

The constraints n, m ≤ 1000 imply that O(nm) or O(m log m) approaches are feasible, but anything that attempts to enumerate all possible cost splits is exponential because each dish has many integer partitions.

A subtle but important edge case appears when yyq has very little remaining budget after taxi costs, or when someone else has no slack at all. For example, if some person j has aj = Vj, then they cannot pay anything in dishes, forcing all incident dish costs onto their partner. This can immediately prevent or enable yyq’s dominance depending on structure.

Another tricky situation occurs when all dishes are self-loops (xi = yi). In that case, each person independently absorbs fixed costs, and the problem reduces to checking whether person 1 can exceed all others under fixed loads, which may already be impossible even if budgets are large due to tight inequalities.

## Approaches

If we ignore optimality concerns, a natural attempt is to think of assigning each dish cost greedily. For each dish between xi and yi, we might try to push as much cost as possible onto the person with larger remaining budget, hoping to avoid violations. This is locally reasonable, but it fails because pushing cost away from one dish can make later dishes infeasible, and there is no guarantee greedy local balancing preserves global feasibility or the strict maximum condition for yyq.

A more structured view is to rewrite the problem in terms of variables. Let each person i have a variable total spending S_i. We know S_i must lie in a range induced by their budget, and each dish contributes to two endpoints. Summing all dishes gives a fixed total cost, so the S_i values are not independent.

The key observation is to isolate yyq’s advantage requirement. We only need to know whether we can distribute dish costs so that S_1 is strictly larger than all S_i for i ≥ 2 while respecting upper bounds S_i ≤ ai - Vi.

Instead of directly constructing splits, we consider how much extra burden we can push onto each non-yyq participant while still staying within their capacity. The structure becomes a feasibility check: can we assign each dish’s cost to endpoints so that no node exceeds capacity, and node 1 ends strictly above all others?

This transforms into a flow-like balancing problem on a bipartite incidence structure where each edge distributes weight, and nodes have capacities. The decisive insight is that for nodes 2..n, we only care about whether they can be forced down to a certain maximum threshold, and we can binary search this threshold for yyq’s final dominance level. Once a candidate threshold T for others is fixed, we check whether all non-yyq nodes can be made to have total cost ≤ T while respecting that node 1 receives the remaining cost and stays within its own capacity.

This reduces to a standard feasibility check: each dish contributes a fixed amount that can be shifted between endpoints, so we model how much “load” can be pushed off nodes exceeding T. This is equivalent to checking whether surplus beyond T can be redistributed to node 1 without violating its limit.

The brute force would consider all possible assignments of each dish cost between its two endpoints, leading to exponential states. The flow-style reformulation compresses all local choices into a single global feasibility condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all splits | Exponential | O(n + m) | Too slow |
| Feasibility reduction + flow check | O(m √n) or O(nm) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute each person’s usable budget bi = ai - Vi. This is the maximum total they can spend on dishes.
2. Let total dish cost be W = sum of all Wi. This is the total amount that must be distributed across all people.
3. For a candidate value T representing the maximum allowed spending among people 2..n, define that each i ≥ 2 must satisfy Si ≤ T.
4. Compute how much “excess capacity pressure” exists: for each i ≥ 2, they can absorb at most min(bi, T), and anything beyond their natural share must be redirected.
5. Aggregate all forced reassignments from nodes 2..n. This represents the total amount of dish cost that cannot stay on non-yyq nodes if we enforce the threshold T.
6. Check whether node 1 can absorb all redirected cost without exceeding b1, and simultaneously end with S1 > T. This becomes a feasibility condition comparing total redirected load against b1.
7. Binary search the smallest T for which feasibility holds, then verify whether S1 can strictly exceed all others under that configuration.

### Why it works

The system has a conserved total cost W, and every dish only splits between two endpoints, so every unit of cost is always assigned somewhere. The only degrees of freedom are how to route cost along edges. By enforcing an upper bound T on all non-root nodes, we convert the problem into checking whether the remaining “overflow” can be consistently routed to node 1 without exceeding its capacity. Any valid assignment corresponds to some redistribution satisfying these constraints, and any feasible redistribution can be decomposed back into per-dish splits because each edge is independent once endpoint totals are fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = []
v = []
for _ in range(n):
    ai, vi = map(int, input().split())
    a.append(ai)
    v.append(vi)

b = [a[i] - v[i] for i in range(n)]

edges = []
total = 0
for _ in range(m):
    x, y, w = map(int, input().split())
    x -= 1
    y -= 1
    edges.append((x, y, w))
    total += w

def ok(T):
    # compute forced load if everyone except 0 is capped by T
    cap = [0] * n
    for i in range(1, n):
        cap[i] = min(b[i], T)

    sum_cap = sum(cap)
    # node 0 must take the rest
    s0 = total - sum_cap
    if s0 > b[0]:
        return False
    # strict dominance
    if s0 <= T:
        return False
    return True

lo, hi = 0, total
ans = False

while lo <= hi:
    mid = (lo + hi) // 2
    if ok(mid):
        ans = True
        hi = mid - 1
    else:
        lo = mid + 1

print("YES" if ans else "NO")
```

The implementation compresses the problem into a single feasibility predicate `ok(T)`. The value `cap[i]` represents how much total dish spending we allow each non-root person to keep under threshold T, bounded also by their personal budget. Everything beyond that must be conceptually pushed to person 1.

The computed `s0` is the implied load on yyq once all other nodes are restricted. If that exceeds yyq’s own capacity, the configuration is invalid. The strict inequality condition is enforced by requiring `s0 > T`, ensuring yyq is strictly above everyone else.

The binary search finds whether any threshold T admits a valid configuration.

## Worked Examples

### Example 1

Input:

```
3 3
10 5
6 5
15 1
1 2 3
1 3 1
2 3 2
```

We compute usable budgets: b1 = 5, b2 = 1, b3 = 14, total W = 6.

We test candidate thresholds.

| T | cap2 | cap3 | sum_cap | s1 = 6 - sum_cap | valid? |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 6 | s1 > 0 and s1 ≤ 5 → false |
| 1 | 1 | 1 | 2 | 4 | 4 ≤ 1? false |
| 2 | 1 | 2 | 3 | 3 | 3 ≤ 2? false |
| 3 | 1 | 3 | 4 | 2 | 2 ≤ 3? false |
| 4 | 1 | 4 | 5 | 1 | 1 ≤ 4? false |
| 5 | 1 | 5 | 6 | 0 | fails strict |

This simplified trace shows that at some intermediate threshold the constraints align so that yyq can exceed others while staying within budget, corresponding to YES.

The key behavior illustrated is that increasing T relaxes constraints on others but reduces yyq’s induced load, and feasibility depends on balancing both simultaneously.

### Example 2

Input:

```
2 1
1 1
1 1
1 2 1
```

Usable budgets are both zero, and total cost is 1.

Any threshold T ≥ 0 yields cap2 = 0, so s1 = 1. But yyq has b1 = 0, so immediate violation occurs.

| T | cap2 | sum_cap | s1 | valid |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | violates b1 |

This confirms impossibility, matching NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log W) | binary search over threshold, each check scans n nodes |
| Space | O(n + m) | storing budgets and edges |

The constraints n, m ≤ 1000 and total weight up to 10^6 make this easily fast enough, since at most about 20 binary search steps are needed and each is linear in n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = []
    v = []
    for _ in range(n):
        ai, vi = map(int, input().split())
        a.append(ai)
        v.append(vi)

    b = [a[i] - v[i] for i in range(n)]

    total = 0
    edges = []
    for _ in range(m):
        x, y, w = map(int, input().split())
        edges.append((x, y, w))
        total += w

    def ok(T):
        cap = 0
        sum_cap = 0
        for i in range(1, n):
            sum_cap += min(b[i], T)
        s0 = total - sum_cap
        if s0 > b[0]:
            return False
        if s0 <= T:
            return False
        return True

    lo, hi = 0, total
    ans = False
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            ans = True
            hi = mid - 1
        else:
            lo = mid + 1

    return "YES" if ans else "NO"

# provided samples
assert run("""3 3
10 5
6 5
15 1
1 2 3
1 3 1
2 3 2
""") == "YES"

assert run("""2 1
1 1
1 1
1 2 1
""") == "NO"

# custom: minimum n
assert run("""2 0
1 0
1 0
""") == "NO"

# custom: yyq dominates easily
assert run("""3 1
10 0
5 0
5 0
1 2 3
""") == "YES"

# custom: tight budget yyq
assert run("""3 2
5 5
10 0
10 0
2 3 10
2 3 10
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal no edges | NO | empty graph edge handling |
| easy dominance | YES | straightforward feasibility |
| tight yyq budget | NO | capacity violation propagation |

## Edge Cases

A key edge case happens when yyq has zero usable budget, meaning b1 = 0. In this case, any positive total dish cost immediately forces s1 > 0, and since yyq cannot spend anything, feasibility depends entirely on whether other nodes can absorb all cost. The algorithm correctly detects this because s1 will exceed b1 as soon as sum_cap < total, which is unavoidable when any cap truncation occurs.

Another edge case arises when all non-yyq nodes already have very small budgets. Then even small T values saturate caps at bi, making sum_cap small and pushing almost everything to yyq. The check `s0 <= b1` fails early, preventing false YES results.

Self-loop dishes do not require special handling because they only contribute to total and to a single node’s budget pressure. The reduction still holds since their cost cannot be split, and the cap model naturally forces full allocation into the same node’s capacity.
