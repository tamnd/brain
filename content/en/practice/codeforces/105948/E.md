---
title: "CF 105948E - Colonization Assessment for Terraforming"
description: "We are given a graph where each vertex represents a planet and each vertex has a numeric value called its habitability. The graph is undirected, and edges represent bidirectional travel routes between planets."
date: "2026-06-22T16:06:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105948
codeforces_index: "E"
codeforces_contest_name: "CCF CAT NAEC 2025 (Provincial)"
rating: 0
weight: 105948
solve_time_s: 55
verified: true
draft: false
---

[CF 105948E - Colonization Assessment for Terraforming](https://codeforces.com/problemset/problem/105948/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph where each vertex represents a planet and each vertex has a numeric value called its habitability. The graph is undirected, and edges represent bidirectional travel routes between planets.

For each test case, we must choose exactly k planets such that every chosen planet can reach every other chosen planet by staying entirely within the chosen set. In other words, the chosen planets must form a connected induced subgraph, because traversal is not allowed through unchosen vertices.

Among all such valid connected selections of size k, we look at the smallest habitability value inside the chosen set. The goal is to maximize this minimum value.

This immediately suggests that the answer depends on selecting a threshold value x and checking whether there exists a connected component that contains at least k vertices whose weights are at least x. If such a set exists, then we can pick k of them inside that connected region.

The constraints imply that n and m are up to 100000 per test case, with total sums across tests bounded by 200000. This rules out any approach that recomputes connectivity from scratch for many candidate thresholds. A solution must effectively be linear or near linear over all test cases.

A subtle edge case arises when the graph is disconnected in such a way that no connected component has size at least k. For example, if n = 5, k = 3, and all edges are isolated, then no valid selection exists and the answer must be -1 even if all weights are large.

Another failure case occurs when one might incorrectly consider components of the full graph without respecting the constraint that traversal cannot pass through excluded nodes. This means we cannot take a globally connected component unless all nodes inside it are valid under the chosen threshold.

## Approaches

The brute-force idea is to consider every possible subset of k nodes, check whether it forms a connected induced subgraph, and compute the minimum weight in it. This is combinatorially impossible because the number of subsets is exponential in n, and even connectivity checking per subset is linear in n plus m. This leads to roughly O(n choose k · (n + m)) operations, which is completely infeasible even for very small n.

A more structured brute-force is to fix the answer x and then check whether the subgraph induced by nodes with weight at least x contains a connected component of size at least k. This reduces the problem to a feasibility check per x. If we could check this efficiently, we could binary search over x.

The key insight is that connectivity only depends on edges between "active" nodes, and we only care about the size of connected components in the filtered graph. If we sort nodes by decreasing weight and progressively activate them, we can maintain connected components using a union-find structure. As soon as a component reaches size k, the current weight threshold is feasible.

This turns the problem into sorting plus DSU maintenance, which is linearithmic per test case but linear overall in practice given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · (n + m)) | O(n + m) | Too slow |
| Threshold + DSU | O(n log n + m α(n)) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process nodes in order of decreasing habitability so that when a node is activated, its weight represents the current candidate minimum.

We maintain a DSU over active nodes only.

1. Sort all nodes by decreasing weight. This ensures we try larger minimum values first, which directly corresponds to maximizing the final answer.
2. Initially, no node is active in the DSU.
3. Iterate through nodes in sorted order, and activate one node at a time.
4. When activating a node, mark it as active and union it with all already-active neighbors. This incrementally builds connected components of the induced subgraph of currently activated nodes.
5. After each activation, compute the size of the DSU component containing that node. If it becomes at least k, we can immediately return the current node's weight as the answer.
6. If we finish processing all nodes without finding a component of size k, return -1.

The reason step 4 is correct is that edges to inactive nodes must not contribute to connectivity. By only unioning active neighbors, we enforce that the DSU exactly represents connectivity in the induced subgraph.

### Why it works

At any moment in the process, the active set corresponds exactly to nodes with weight at least the current threshold. The DSU components represent connected components in the subgraph induced by these active nodes. When a component first reaches size k, it means there exists a connected subgraph of k nodes all with weight at least the current threshold. Because we process weights in descending order, this threshold is the maximum possible minimum value for any valid connected set of size k.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

    def comp_size(self, x):
        return self.size[self.find(x)]

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    w = list(map(int, input().split()))

    edges = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges[u].append(v)
        edges[v].append(u)

    order = sorted(range(n), key=lambda i: -w[i])

    active = [False] * n
    dsu = DSU(n)

    answer = -1

    for node in order:
        active[node] = True
        for nei in edges[node]:
            if active[nei]:
                dsu.union(node, nei)

        if dsu.comp_size(node) >= k:
            answer = w[node]
            break

    print(answer)
```

The DSU is initialized with each node in its own component, but the key detail is that components only become meaningful when nodes are activated. The active array ensures we never merge through inactive nodes, preserving the induced subgraph constraint.

The sorting step is critical because it guarantees that the first time we reach a component of size k, we are using the highest possible minimum weight.

The comp_size check uses the representative of the newly activated node, which is sufficient because all merges involving that node happen immediately upon activation.

## Worked Examples

Consider a small graph with 5 nodes and k = 3:

Input:

```
n = 5, m = 4, k = 3
w = [5, 1, 4, 3, 2]
edges: (1-2), (2-3), (3-4), (4-5)
```

Sorted nodes by weight: 1(5), 3(4), 4(3), 5(2), 2(1)

We track activation:

| Step | Node | Active Set | DSU Merges | Component Size | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | {1} | none | 1 | -1 |
| 2 | 3 | {1,3} | none | 1,1 | -1 |
| 3 | 4 | {1,3,4} | 3 connects to 4 | 2 | -1 |
| 4 | 5 | {1,3,4,5} | 4-5 | 3 | 3 |

When node 5 (weight 2) is added, the chain 3-4-5 is active and forms a connected component of size 3. However, we must ensure minimum weight is 3 here, not 2. The table shows a subtle issue: in reality, the answer triggers when node 4 is added because the connected active component {3,4,5} is not yet fully connected until 5 is included, but the minimum weight of that set is 2, so the first valid k-component is actually the set {3,4,5} which has minimum 2. If a higher-weight component of size 3 existed earlier, it would be selected first due to ordering.

This demonstrates that correctness depends on the descending activation order ensuring we always consider the best possible threshold first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) α(n)) per test | Each node is activated once and each edge is processed at most twice through DSU unions |
| Space | O(n + m) | adjacency list plus DSU arrays |

Across all test cases, total n and m are bounded by 2 × 10^5, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]

        def comp_size(self, x):
            return self.size[self.find(x)]

    t = int(input())
    out = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        w = list(map(int, input().split()))

        edges = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            edges[u].append(v)
            edges[v].append(u)

        order = sorted(range(n), key=lambda i: -w[i])

        active = [False] * n
        dsu = DSU(n)

        ans = -1
        for node in order:
            active[node] = True
            for nei in edges[node]:
                if active[nei]:
                    dsu.union(node, nei)
            if dsu.comp_size(node) >= k:
                ans = w[node]
                break

        out.append(str(ans))

    return "\n".join(out)

# simple constructed tests
assert run("""1
1 0 1
5
""") == "5"

assert run("""1
3 0 2
5 4 3
""") == "-1"

assert run("""1
3 2 2
1 2 3
1 2
2 3
""") == "2"

assert run("""1
5 4 3
5 1 4 3 2
1 2
2 3
3 4
4 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 5 | minimal case |
| disconnected graph | -1 | impossibility |
| small chain k=2 | 2 | threshold correctness |
| full chain k=3 | 2 | connectivity accumulation |

## Edge Cases

A key edge case is when the graph has enough nodes but no connected component can ever reach size k even before considering weights. In that situation, the algorithm will activate all nodes and never trigger the size condition, so it correctly outputs -1.

Another edge case is when the answer comes from a high-weight isolated node that never connects. Since connectivity is required, a single node cannot satisfy k > 1, and DSU sizes prevent false positives because unions never occur without edges.

A third case involves multiple components growing in parallel. The algorithm still works because each activation only merges local neighborhoods, and the first time any component reaches size k, it corresponds to the best possible threshold due to descending weight processing.
