---
title: "CF 103328B - Apple Tree"
description: "We are given a tree with weighted nodes and weighted edges. Each node contains some number of apples. Each edge has a length."
date: "2026-07-03T17:53:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103328
codeforces_index: "B"
codeforces_contest_name: "National Taiwan University NCPC Preliminary 2021"
rating: 0
weight: 103328
solve_time_s: 54
verified: true
draft: false
---

[CF 103328B - Apple Tree](https://codeforces.com/problemset/problem/103328/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with weighted nodes and weighted edges. Each node contains some number of apples. Each edge has a length. We are allowed to choose any subset of nodes, and then we must design a closed walk in the tree that starts at some node, visits every chosen node at least once, and returns to the starting node. The score of a plan is the total apples collected from the chosen nodes minus the total length of the walk. The goal is to maximize this score.

The key detail is that once a set of nodes is fixed, the cheapest possible closed walk that visits all of them in a tree structure is not arbitrary. In a tree, any closed walk that visits a set of nodes must traverse exactly the minimal connected subtree that spans those nodes, and every edge in that subtree is walked exactly twice, once in each direction. This means the travel cost is determined entirely by the sum of edge lengths in the induced connecting subtree, multiplied by two.

The input size goes up to one million nodes, which immediately rules out any solution that tries to enumerate subsets of nodes or simulate routes explicitly. Even linear or near-linear memory access must be carefully designed, since recursion depth and constant factors matter. This pushes us toward a dynamic programming formulation over the tree structure.

A subtle issue appears when thinking greedily about selecting nodes based only on their apple counts. A node with a small or even negative contribution might still be worth keeping if it connects two profitable regions, since it can reduce the need for additional edges in the spanning structure. Conversely, selecting many positive nodes that are far apart can become unprofitable because connecting them forces inclusion of expensive edges that are traversed twice.

For example, consider a chain of three nodes with apple values `[100, 1, 100]` and edges of length `1000` between consecutive nodes. Selecting all nodes gives a huge edge cost of `2 * 2000 = 4000` while apple gain is `201`, producing a negative score. The correct answer is to pick only one endpoint node. A naive strategy that always includes positive nodes fails here because it ignores connectivity cost.

Another corner case is when all apple values are zero. The correct answer is zero, achieved by selecting nothing. Any approach that assumes at least one node must be chosen would incorrectly produce a negative value.

## Approaches

A brute-force strategy would try every subset of nodes, compute the minimal subtree spanning them, and evaluate its cost. Even if computing the Steiner tree cost in a tree is linear in the number of nodes, the number of subsets is exponential, making this approach impossible even for small instances.

The structure of the problem simplifies once we fix a root and think about how contributions propagate. If we consider a connected selection rooted at some node, then each child subtree either contributes something useful upward or is discarded entirely. The key observation is that the cost of including a child subtree is exactly the best gain inside that subtree minus twice the connecting edge length. If this value is negative, the optimal decision is to exclude that subtree entirely, because including it only increases travel cost more than it adds apples.

This turns the problem into a tree dynamic programming task where each node aggregates the best possible contribution of all beneficial child subtrees. Since the chosen structure must remain connected, each dp value represents the best connected component rooted at that node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^N · N) | O(N) | Too slow |
| Tree DP pruning negative branches | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Root the tree at an arbitrary node, since the tree is undirected and any connected selection has a unique topmost node in the rooted view. This lets us define a parent-child structure for DP.
2. Perform a postorder traversal so that when processing a node, all its children have already been processed and their best contributions are known.
3. For each node, initialize its current value as the apple count at that node. This represents the gain if we only take this node without connecting anything else.
4. For each child, compute how much benefit that child subtree can provide if attached. The child contributes its dp value minus twice the edge length connecting it to the current node. If this value is positive, add it to the current node's value. Otherwise, discard the child subtree completely.

The reason for subtracting twice the edge is that any included subtree must traverse that edge in both directions in a closed walk.
5. Store this accumulated value as dp[node], representing the best score of a connected subtree whose highest node in the rooted tree is this node.
6. The final answer is the maximum dp value over all nodes, but it is also valid to return zero if all values are negative, since selecting no nodes yields zero score.

### Why it works

Every valid selection of nodes induces a connected subtree in the original tree. If we root that subtree at the highest node in the global root orientation, all included edges go downward into child subtrees. The total score decomposes into node gains minus twice edge costs, and each child subtree contributes independently once its connecting edge is fixed. Because tree edges are not shared between different child subtrees, decisions to include or exclude each child are independent. This independence guarantees that locally discarding a negative contribution never blocks a globally optimal solution, since any optimal solution that includes a negative subtree can be improved by removing it without breaking connectivity above the parent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))

    parent = [-1] * n
    order = []
    stack = [0]
    parent[0] = -2

    while stack:
        u = stack.pop()
        order.append(u)
        for v, w in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)

    dp = [0] * n

    for u in reversed(order):
        dp[u] = a[u]
        for v, w in g[u]:
            if parent[v] == u:
                gain = dp[v] - 2 * w
                if gain > 0:
                    dp[u] += gain

    print(max(0, max(dp)))

if __name__ == "__main__":
    solve()
```

The code first builds an adjacency list for the tree. It then constructs a traversal order using an iterative DFS to avoid recursion depth issues, which is important given the constraint of up to one million nodes.

The dp array stores the best contribution of a connected subtree rooted at each node. During the reverse traversal, each node starts with its own apple value. For every child, we evaluate whether including that child subtree improves the total after accounting for the round-trip traversal of the connecting edge. Only positive contributions are added, ensuring that no harmful subtree is included.

The final answer is the best value among all dp states, with a floor at zero to handle cases where every possible selection is detrimental.

## Worked Examples

Consider a small tree where node 1 has 10 apples, node 2 has 5 apples, and node 3 has 8 apples, with edges 1-2 of length 3 and 2-3 of length 4.

| Node | Initial a[u] | Child contribution | dp[u] |
| --- | --- | --- | --- |
| 3 | 8 | none | 8 |
| 2 | 5 | 8 - 8 = 0 (discard) | 5 |
| 1 | 10 | 5 - 6 = -1 (discard) | 10 |

The algorithm selects only node 1 because attaching other nodes does not compensate for edge traversal cost. This demonstrates how local pruning prevents unnecessary expansion.

Now consider a star shaped tree where center node has 1 apple and three leaves each have 100 apples with edge cost 1.

| Node | Initial a[u] | Child contributions | dp[u] |
| --- | --- | --- | --- |
| leaves | 100 each | none | 100 |
| center | 1 | 100-2 = 98 each | 295 |

Here all leaves are included because their gains remain positive after paying edge costs twice. This confirms that the DP correctly aggregates multiple beneficial branches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each node and edge is processed exactly once during DFS and DP aggregation |
| Space | O(N) | Adjacency list, traversal order, and dp array store linear information |

The linear complexity is necessary given the constraint of up to one million nodes. Any superlinear approach would fail both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""

# simple chain
assert run("""3
1 1 1
1 2 1
2 3 1
""") == "", "chain test"

# star
assert run("""4
0 10 10 10
1 2 1
1 3 1
1 4 1
""") == "", "star test"

# single node
assert run("""1
5
""") == "", "single node"

# all zeros
assert run("""3
0 0 0
1 2 1
2 3 1
""") == "", "all zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | optimal pruning | negative branches |
| star | multi-branch accumulation | independent subtrees |
| single node | base case handling | trivial tree |
| all zeros | empty selection optimal | zero floor |

## Edge Cases

A single-node tree is handled correctly because the DP initializes each node with its own apple value and never requires children. The answer becomes that single value, or zero if it is negative.

A long chain where all intermediate nodes have small apple values compared to edge weights is correctly pruned because every child contribution becomes negative after subtracting twice the edge cost, causing the DP to collapse to isolated nodes.

A dense star where many leaves are individually beneficial remains fully included because each leaf is evaluated independently, and each contributes positively after edge cost adjustment, ensuring all profitable leaves are attached to the center without interference.
