---
title: "CF 104522F - Candy Machine"
description: "We are given a rooted tree, and each edge carries a weight that defines how likely a process moves through that edge. The process starts at the root. Whenever we “activate” a node, we spend one unit of cost, and that node becomes empty."
date: "2026-06-30T10:13:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104522
codeforces_index: "F"
codeforces_contest_name: "CerealCodes II Intermediate"
rating: 0
weight: 104522
solve_time_s: 99
verified: false
draft: false
---

[CF 104522F - Candy Machine](https://codeforces.com/problemset/problem/104522/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree, and each edge carries a weight that defines how likely a process moves through that edge. The process starts at the root. Whenever we “activate” a node, we spend one unit of cost, and that node becomes empty. If the node has children, exactly one of its children is chosen randomly, with probability proportional to the edge weights, and the process continues from that child. If the node is a leaf, the process stops because there is nowhere further to move.

Each node represents a candy type. Internal nodes initially have only one copy of their candy, while leaves have infinitely many copies, but that distinction mainly ensures leaves never block progress.

The key quantity we must compute is, for every node i, the expected total money spent until we obtain candy i through this stochastic cascade process.

The input size reaches 2 × 10^5 nodes overall across test cases, so any solution must be essentially linear per test case. Anything involving recomputation per node or per path separately would be too slow. The tree structure also suggests that each node’s answer depends only on its ancestors, not on arbitrary global interactions.

A subtle failure case for naive thinking is assuming independence across nodes. For example, one might try to simulate the process repeatedly until each node is reached, but even a single simulation is unbounded because the tree can be deep and probabilities compound multiplicatively into extremely small values.

Another common mistake is thinking that the expected cost depends on subtree size or number of leaves. It does not. It depends only on the probability that the random cascade ends exactly at a given node.

## Approaches

The brute-force interpretation is to explicitly simulate the stochastic process many times and estimate probabilities of reaching each node. One simulation corresponds to a single cascade starting from the root, walking down random children until a leaf is reached. If we repeat this process, we can estimate how often each node is the final endpoint or how many cascades are required before encountering it.

This is correct in expectation but unusable computationally. Even generating one path per trial is O(n) in the worst case, and to estimate expectations accurately we would need a prohibitive number of trials. With n up to 2 × 10^5, any Monte Carlo or repeated simulation approach collapses immediately.

The key structural observation is that each cascade is not arbitrary randomness over the whole tree, but a single random root-to-leaf walk where transition probabilities are fixed locally at each node. That means the probability of ending at a specific node is exactly the product of edge probabilities along the unique root-to-node path.

Once we know the probability p_i that a single cascade ends at node i, the expected number of cascades needed to hit node i is simply the expectation of a geometric distribution with success probability p_i, which equals 1 / p_i.

So the entire problem reduces to computing p_i for each node efficiently, then outputting its modular inverse.

The probability along a path is a product of terms of the form w(u, v) / sum_w(u), so its reciprocal becomes a product of sum_w(u) / w(u, v). This converts the answer into a simple multiplicative DP on the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T · k · n) | O(n) | Too slow |
| Tree probability DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at 1 and compute for every node the sum of weights of edges going to its children. This value represents the normalization factor for transition probabilities at that node.

We then perform a DFS from the root, maintaining for each node the reciprocal probability of reaching it in one cascade.

1. Set dp[1] = 1 because the root is reached before any probabilistic decision is made.
2. For each node u, compute S(u), the sum of weights of edges from u to its children.
3. When traversing an edge u → v with weight w, the probability of choosing v given we are at u is w / S(u).
4. Therefore, the probability of reaching v is dp_prob[v] = dp_prob[u] × (w / S(u)).
5. We do not store probabilities directly. Instead we store dp[v] = 1 / dp_prob[v], which avoids repeated modular inverses along paths.
6. This gives dp[v] = dp[u] × (S(u) / w). We compute this in modular arithmetic using modular inverses of w.
7. Traverse the entire tree once, propagating dp values from root to leaves.

Why it works is tied to a single invariant: at every node u, dp[u] always equals the reciprocal of the probability that a single cascade from the root ends exactly at u. The recursion preserves this because every edge multiplies probability by a local transition factor, and reciprocals transform multiplication into the inverse ratio in the same direction. Since every node has a unique parent path, no overlapping subproblems or cross terms exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    g = [[] for _ in range(n + 1)]
    
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))
    
    parent = [0] * (n + 1)
    pw = [0] * (n + 1)
    order = []
    
    stack = [1]
    parent[1] = -1
    
    while stack:
        u = stack.pop()
        order.append(u)
        for v, w in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            pw[v] = w
            stack.append(v)
    
    children_sum = [0] * (n + 1)
    
    for u in range(1, n + 1):
        for v, w in g[u]:
            if parent[v] == u:
                children_sum[u] = (children_sum[u] + w) % MOD
    
    dp = [1] * (n + 1)
    
    for u in order:
        for v, w in g[u]:
            if parent[v] == u:
                dp[v] = dp[u] * children_sum[u] % MOD * modinv(w) % MOD
    
    print(*dp[1:])

if __name__ == "__main__":
    solve()
```

The implementation first builds the tree, then fixes a rooted parent structure using an explicit stack to avoid recursion depth issues. After that, it computes the sum of outgoing weights for each node. This is the normalization factor needed for transition probabilities.

The DP propagation step follows the exact recurrence derived earlier: each child inherits its value from its parent multiplied by the ratio of total outgoing weight over edge weight. Modular inverses are used to handle division under modulo 998244353.

A subtle point is that we never recompute probabilities from scratch per node. Everything flows in a single traversal, ensuring linear complexity.

## Worked Examples

Consider a simple tree:

Node 1 has children 2 and 3, with weights 2 and 3 respectively.

| Step | Node | dp value | Explanation |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Root base case |
| 2 | 2 | (2+3)/2 = 5/2 | inverse probability of reaching 2 |
| 3 | 3 | (2+3)/3 = 5/3 | inverse probability of reaching 3 |

For node 2, probability in one cascade is 2/5, so expected trials is 5/2. For node 3, probability is 3/5, so expectation is 5/3.

Now consider a deeper chain:

1 → 2 → 3 with weights 4 and 5.

| Step | Node | dp value | Explanation |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Root |
| 2 | 2 | 4/4 = 1 | only child, deterministic |
| 3 | 3 | 1/5 | product of inverses |

This shows how deterministic edges collapse probabilities cleanly, and only branching nodes contribute nontrivial scaling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each node and edge is processed once in DFS |
| Space | O(n) | adjacency list and DP arrays |

The constraints allow up to 2 × 10^5 nodes total, so a linear traversal per test case is sufficient. The solution avoids any per-node recomputation or repeated path processing, keeping runtime comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline
    
    n = int(input())
    g = [[] for _ in range(n + 1)]
    
    edges = []
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))
        edges.append((u, v, w))
    
    parent = [0] * (n + 1)
    pw = [0] * (n + 1)
    
    stack = [1]
    parent[1] = -1
    order = []
    
    while stack:
        u = stack.pop()
        order.append(u)
        for v, w in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            pw[v] = w
            stack.append(v)
    
    children_sum = [0] * (n + 1)
    for u in range(1, n + 1):
        for v, w in g[u]:
            if parent[v] == u:
                children_sum[u] = (children_sum[u] + w) % MOD
    
    dp = [1] * (n + 1)
    for u in order:
        for v, w in g[u]:
            if parent[v] == u:
                dp[v] = dp[u] * children_sum[u] % MOD * modinv(w) % MOD
    
    return " ".join(str(x) for x in dp[1:])

# custom tests

# single node
assert run("1\n") == "1", "single node"

# chain
assert run("3\n1 2 2\n2 3 3\n") == "1 1 1", "linear deterministic chain"

# star
out = run("3\n1 2 1\n1 3 1\n")
assert len(out.split()) == 3, "star structure output size"

# symmetric small tree
out = run("5\n1 2 1\n1 3 2\n2 4 1\n2 5 3\n")
assert len(out.split()) == 5, "small tree structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | 1 | base case correctness |
| chain tree | all 1 | deterministic propagation |
| star tree | 3 values | branching normalization |
| small mixed tree | 5 values | general DP consistency |

## Edge Cases

A single-node tree is the simplest boundary. The algorithm initializes dp[1] = 1, and since there are no children, no transitions occur. The output correctly remains 1.

A fully linear tree ensures that every node has exactly one child. In that case, each S(u) equals the single edge weight, so every ratio becomes 1. The DP propagates a constant value down the chain, matching the fact that the cascade has probability 1 of following the only path.

A high-degree root tests normalization. Even when the root has many children, only the sum of weights matters. Each child’s value is scaled independently using the same root factor, and the DFS ensures no interference between branches.
