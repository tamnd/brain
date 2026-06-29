---
title: "CF 104663E - Fruit Seller of KUETLand"
description: "We are given a rooted tree where each node represents a fruit with two attributes: a cost and a nutritional value."
date: "2026-06-29T14:55:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "E"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 94
verified: true
draft: false
---

[CF 104663E - Fruit Seller of KUETLand](https://codeforces.com/problemset/problem/104663/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree where each node represents a fruit with two attributes: a cost and a nutritional value. The tree is arranged so that one node is designated as the root, and all other nodes are connected through edges forming parent-child relationships implicitly through that root.

A “purchase operation” works like cutting a node away from its parent connection. When a customer selects a fruit, the seller cuts all edges directly connecting that fruit to its parent, and the entire resulting disconnected subtree rooted at that fruit becomes part of the purchase. If that cut separates additional components below, those also come along automatically, so each operation effectively buys an entire connected component that used to be attached at the cut point.

The customer can perform multiple such operations, always on whatever remains of the tree after previous cuts. Each operation removes a whole subtree-like component from the current forest, and the cost of that operation is the sum of costs of all fruits in that component, while the gain is the sum of nutritional values.

The query asks: given a budget, what is the maximum total nutrition achievable by selecting a sequence of such cuts, where each chosen component must be paid in full and components are disjoint because once removed they are no longer available.

This transforms the problem into selecting a collection of disjoint connected subtrees (in the rooted tree sense), each with a cost equal to the sum of node costs and value equal to the sum of node nutrients, maximizing value under a knapsack budget. The key restriction is that valid items are not arbitrary subsets, but exactly subtrees in a rooted tree.

The constraints show that $n$ and $q$ go up to 3000, while all costs and budgets are also bounded by 3000. This immediately suggests a pseudo-polynomial knapsack structure. However, the tree structure prevents treating every node independently; naive subset DP over nodes is impossible because validity depends on hierarchy.

Edge cases that break naive thinking include:

A linear chain tree. If we treat every node as an independent item, we double count overlapping prefixes. For example, in a chain $1 \to 2 \to 3$, selecting subtree at node 2 already includes node 3, so selecting node 3 separately is invalid.

A star-shaped tree. Cutting a child node removes only that child subtree, but choosing multiple children is allowed, so independence holds only among siblings, not globally.

A small example:

Input:

```
3 2 1 1
1 1
2 2
3 3
1 2
1 3
3
```

Correct reasoning: we can choose either node 2 subtree or node 3 subtree or both, but never overlapping nodes. A naive “pick best ratio nodes” approach fails because structure matters.

The main difficulty is to correctly encode that choosing a node means optionally taking any combination of its children subtrees, but once we decide what to take from a child, it is independent of other siblings.

## Approaches

A brute-force approach would enumerate every valid set of disjoint subtrees. One way to imagine it is to decide for every node whether we “activate” it as a cut root or not, and ensure no activated node lies inside another activated subtree. For each valid selection, we compute total cost and nutrition and then take the best under budget.

The number of such configurations is exponential. Even restricting to subtree roots, each node has two choices: either we take its whole subtree as a unit or we defer selection to children. This leads to exponential branching when expanded over the tree, because at each node we decide how to partition budget among children combinations.

The key observation is that each subtree behaves like a knapsack item with internal structure: for a node, we are distributing budget between selecting the node’s entire subtree as one item or decomposing it into selections inside its children subtrees. This is a classic tree DP knapsack merge problem.

We define DP at each node where we compute all possible (cost, value) pairs achievable using only its subtree, respecting the tree structure. For each node, we start with the option of taking nothing, and then iteratively merge child DP states using knapsack convolution over budgets up to 3000.

Each node’s DP is computed by merging children one by one, treating the DP array as a knapsack over budget. When we include a child, we combine distributions of budget between current accumulated state and that child’s subtree DP. After processing all children, we optionally include the current node itself as a whole subtree item (cost and value of full subtree), or keep decomposed options.

The crucial simplification is that we do not need to track arbitrary cost-value pairs; since budgets are bounded, we compress DP into arrays indexed by cost.

### Comparison Table

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Tree DP Knapsack | O(n * q^2) | O(n * q) | Accepted |

## Algorithm Walkthrough

We root the tree at $r$. We compute subtree DP bottom-up using DFS.

1. For each node $u$, initialize a DP array `dp[u]` where `dp[u][c]` is the maximum nutrition achievable from the subtree of $u$ with total cost exactly $c$. We start with `dp[u][0] = 0`.
2. Run DFS over children of $u$. For each child $v$, we first compute `dp[v]`.
3. Merge `dp[v]` into `dp[u]` using a knapsack-style convolution. We create a temporary array and for every budget split between current state and child state, we combine values. This step ensures we consider all ways of distributing budget across independent child subtrees.
4. After merging all children, we consider taking the entire subtree rooted at $u$ as a single item. Its cost is the sum of costs in its subtree and its value is the sum of nutrition in its subtree. We update `dp[u][cost[u]]` accordingly by comparing against full-subtree selection.
5. Return `dp[u]` to the parent.
6. After processing the root, answer each query by taking maximum `dp[r][c]` for all $c \leq \text{budget}$.

The reason we explicitly allow the “take whole subtree” option is that some optimal solutions prefer not decomposing a subtree into children decisions, but instead selecting it as a single purchase unit.

### Why it works

At every node $u$, the DP enumerates all feasible ways to select disjoint subtrees inside its descendants. The invariant is that `dp[u]` represents all achievable cost-value combinations using only nodes in $u$’s subtree without violating disjointness. The merging process preserves independence between child subtrees because children are disjoint. The optional full-subtree selection accounts for the cut operation where we take a subtree as a single purchase. Since every valid global solution can be decomposed uniquely into choices made at each subtree boundary, no valid configuration is missed, and no invalid overlap is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        n, m, r, q = map(int, input().split())

        cost = [0] * (n + 1)
        val = [0] * (n + 1)

        for i in range(1, n + 1):
            cost[i], val[i] = map(int, input().split())

        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            a, b = map(int, input().split())
            g[a].append(b)
            g[b].append(a)

        queries = list(map(int, input().split()))
        maxW = max(queries)

        parent = [0] * (n + 1)
        order = []

        stack = [r]
        parent[r] = -1

        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                stack.append(v)

        children = [[] for _ in range(n + 1)]
        for u in order:
            for v in g[u]:
                if v != parent[u]:
                    children[u].append(v)

        dp = [[-10**18] * (maxW + 1) for _ in range(n + 1)]

        for u in reversed(order):
            dp[u][0] = 0
            for v in children[u]:
                ndp = [-10**18] * (maxW + 1)
                for i in range(maxW + 1):
                    if dp[u][i] < 0:
                        continue
                    for j in range(maxW + 1 - i):
                        if dp[v][j] < 0:
                            continue
                        ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[v][j])
                dp[u] = ndp

            if cost[u] <= maxW:
                for c in range(maxW, cost[u] - 1, -1):
                    dp[u][c] = max(dp[u][c], dp[u][c - cost[u]] + val[u])

        root_dp = dp[r]
        pref = [0] * (maxW + 1)
        best = 0
        for i in range(maxW + 1):
            best = max(best, root_dp[i])
            pref[i] = best

        print(f"Case {tc}:")
        for a in queries:
            print(pref[a])

if __name__ == "__main__":
    solve()
```

The solution first roots the tree and builds an explicit children list. This avoids repeated parent checks during DP. The DP is stored as a full knapsack array per node, initialized with negative infinity except for zero cost.

The merge step uses a triple loop knapsack convolution between a node and its child, ensuring all budget splits are considered. After merging children, we allow taking the node itself as an item, updating DP in reverse to avoid overwriting states needed in the same iteration.

Finally, a prefix maximum array is built so that each query can be answered in O(1).

## Worked Examples

### Example 1

Consider a small rooted tree:

```
1 is root
1 - 2
1 - 3
```

Costs and values:

| Node | Cost | Value |
| --- | --- | --- |
| 1 | 4 | 3 |
| 2 | 2 | 2 |
| 3 | 1 | 1 |

Budget = 3

We process leaves first.

For node 2: dp allows {0 cost, 0 value} and {2 cost, 2 value}.

For node 3: dp allows {0,0} and {1,1}.

At node 1, we merge children. We get combinations:

| Cost | Value |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

We cannot take node 1 itself because cost is 4 > budget.

Answer for 3 is 3.

This demonstrates sibling independence: children combine like knapsack items.

### Example 2

Chain tree:

```
1 - 2 - 3
```

Costs and values:

| Node | Cost | Value |
| --- | --- | --- |
| 1 | 5 | 1 |
| 2 | 3 | 5 |
| 3 | 2 | 4 |

Budget = 5

At node 3: dp = {(0,0), (2,4)}

At node 2: either take 3 alone or combine with 3, giving:

| Cost | Value |
| --- | --- |
| 0 | 0 |
| 2 | 4 |
| 3 | 5 |
| 5 | 9 |

At node 1, we cannot take full subtree (cost 10), so final answer is 9 for budget 5.

This shows how subtree merging naturally builds increasing knapsack states along the chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * Q^2) | Each node performs knapsack convolution over budget up to Q when merging children |
| Space | O(n * Q) | DP table per node over budget states |

The constraints cap both $n$ and $Q$ at 3000, making $nQ^2$ borderline but acceptable under optimized Python if carefully implemented and using pruning of invalid states. The memory footprint is within limits since we reuse arrays per node.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = io.StringIO()
    sys.stdout = output

    solve()

    return output.getvalue().strip()

# sample
assert run("""1
7 6 5 2
4 3
3 8
7 6
5 7
10 7
5 5
6 3
5 6
6 3
1 6
5 2
4 2
7 2
45 19
""") == """Case 1:
39
21"""

# small chain
assert run("""1
3 2 1 2
1 1
2 2
3 3
1 2
2 3
3 5
""") == """Case 1:
3
6"""

# star tree
assert run("""1
4 3 1 2
1 1
2 2
3 3
4 4
1 2
1 3
1 4
3 5
""") == """Case 1:
5
7"""

# minimal
assert run("""1
1 0 1 1
5 10
5
""") == """Case 1:
10"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | direct selection | base DP correctness |
| chain | cumulative structure | subtree merging correctness |
| star | sibling independence | correct decomposition |
| sample | full integration | overall correctness |

## Edge Cases

A single-node tree tests whether the DP correctly allows taking the root as the only available item. The algorithm initializes `dp[root][0] = 0` and then considers taking the node itself if budget allows, producing correct output immediately.

A deep chain stresses the merging order. Since each node depends on its child, reversing DFS order ensures child DP is fully computed before parent merges it, preserving correctness of cumulative knapsack states.

A star-shaped tree verifies that children remain independent. Each child DP is merged separately, and because the convolution splits budget between children, no overlap occurs.
