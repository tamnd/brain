---
title: "CF 104741H - \u73bb\u7483\u7403"
description: "We are given a rooted tree of size $N$, rooted at node 1. Each node represents a platform, and each platform initially contains exactly one glass ball."
date: "2026-06-28T23:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104741
codeforces_index: "H"
codeforces_contest_name: "The 10th Jimei University Programming Contest"
rating: 0
weight: 104741
solve_time_s: 86
verified: true
draft: false
---

[CF 104741H - \u73bb\u7483\u7403](https://codeforces.com/problemset/problem/104741/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree of size $N$, rooted at node 1. Each node represents a platform, and each platform initially contains exactly one glass ball. Every edge is directed from a node to its parent, so each ball will always move upward toward the root, traversing one edge per unit time.

When a ball reaches a node $v$, it may be collected there if a device at $v$ works. Each node $v$ has an independent probability $p_v$ of its device successfully working. If the device works, the ball stops permanently at $v$. If it fails, the ball continues moving upward toward the parent.

A ball keeps moving until it is collected by the first node on its path whose device works. Because $p_1 = 1$, every ball is guaranteed to be collected at the root if nothing earlier stops it.

The cost of a ball is defined as the number of edges it travels before being collected. We are asked to compute the expected total cost over all $N$ balls, one starting from each node.

The key subtlety is that multiple balls interact only through sharing the same tree structure, not directly. Each ball independently moves upward, but their expected contributions depend on shared probabilities along paths.

The constraints go up to $N = 5 \cdot 10^5$, which immediately rules out any quadratic or even $O(N \log^2 N)$ per-node recomputation. The solution must be linear or near-linear, since only about a few tens of millions of operations are safe in time.

A naive simulation would move every ball upward until it is collected, but that can degrade to $O(N^2)$ in a chain-shaped tree. For example, in a line $1 \leftarrow 2 \leftarrow 3 \leftarrow \dots \leftarrow N$, the ball at node $N$ traverses $N-1$ edges, the ball at $N-1$ traverses $N-2$, and so on, producing a quadratic total.

Another hidden difficulty is that naive probability enumeration over all subsets of working devices is exponential. Even small chains already produce $2^N$ configurations, so any approach that explicitly branches on working/failing devices is impossible.

The main difficulty is separating the randomness along a path from the deterministic tree aggregation of distances.

## Approaches

A direct way to think about the process is to simulate each ball independently. For a ball starting at node $u$, we walk upward until we encounter the first node $v$ whose device works, and we add the distance from $u$ to $v$. If no device worked, it would end at the root, but since $p_1 = 1$, this case is absorbed at node 1.

This view is correct but too slow because each ball may traverse up to $O(N)$ edges, giving $O(N^2)$ worst case.

The key observation is that instead of tracking where each ball ends, we reverse the perspective. Fix a node $v$. We ask: which balls get collected at $v$, and what is their total travel distance?

A ball from node $u$ is collected at $v$ exactly when two conditions hold. First, all devices on the path from $u$ up to but excluding $v$ fail. Second, the device at $v$ succeeds. This probability depends only on ancestors of $v$, not on the subtree structure below.

This allows us to factor the probability into a value attached to $v$, independent of individual $u$, multiplied by a purely structural sum over the subtree of $v$.

So the expectation becomes a sum over nodes $v$, where each node contributes its success-weighted probability times the total distance from all nodes in its subtree to $v$. This transforms randomness on paths into a single multiplier per node.

To compute subtree distance sums efficiently, we rewrite distances using depths. For any descendant $u$ of $v$, the distance is $\text{depth}[u] - \text{depth}[v]$. Thus, the subtree contribution reduces to maintaining subtree sums of depths and subtree sizes.

The final structure becomes a tree DP with one DFS for probability accumulation and one for subtree aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute simulation per ball | $O(N^2)$ | $O(N)$ | Too slow |
| Probability enumeration | $O(2^N)$ | $O(2^N)$ | Impossible |
| Tree DP factorization | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We root the tree at 1 and process it in DFS order.

1. Compute the probability that node $v$ is the first working device on a path from below. We define a value $g[v]$ as the probability that all ancestors of $v$ fail and $v$ succeeds. While traversing from parent to child, we maintain a running product of failure probabilities, so $g[v] = p_v \cdot \prod_{x \in \text{ancestors of } v} (1 - p_x)$. This ensures each node knows how likely it is to be the stopping point for any ball reaching its subtree.
2. Run a DFS from the root while maintaining subtree information. For each node $v$, compute two values over its subtree: the number of nodes $sz[v]$, and the sum of depths of nodes in its subtree, denoted $sumDepth[v]$.
3. For each node $v$, compute the total distance from all nodes in its subtree to $v$. Using the identity $\text{dist}(u,v) = \text{depth}[u] - \text{depth}[v]$, we derive:

$$\sum_{u \in subtree(v)} \text{dist}(u,v) = sumDepth[v] - depth[v] \cdot sz[v].$$
4. Multiply this structural sum by the probability weight $g[v]$. This gives the expected contribution of node $v$ to the final answer.
5. Sum contributions over all nodes and output the result modulo $998244353$.

### Why it works

Each ball’s expected cost can be decomposed by conditioning on the node where it is first collected. The event “ball from $u$ is collected at $v$” depends only on the states of nodes on the path from $u$ to $v$, and this dependency separates cleanly into a factor depending only on ancestors of $v$ and a deterministic count of how many $u$ lie in $v$’s subtree.

This separation ensures no double counting: every ball contributes exactly once, at its stopping node, and the DFS aggregation enumerates all such contributions exactly once per node.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    parent = [0] * n
    children = [[] for _ in range(n)]

    for i in range(1, n):
        fa = int(input().split()[0]) if False else None  # placeholder safe
```

We cannot use that incorrect input line; fix properly:
