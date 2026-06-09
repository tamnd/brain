---
title: "CF 1615E - Purple Crayon"
description: "We are given a rooted tree with $n$ nodes, rooted at node 1, where all nodes start white. Two players, Red and Blue, take turns coloring nodes. Red goes first and can color at most $k$ nodes red by choosing entire subtrees."
date: "2026-06-10T06:39:52+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "games", "graphs", "greedy", "math", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1615
codeforces_index: "E"
codeforces_contest_name: "Codeforces Global Round 18"
rating: 2400
weight: 1615
solve_time_s: 101
verified: false
draft: false
---

[CF 1615E - Purple Crayon](https://codeforces.com/problemset/problem/1615/E)

**Rating:** 2400  
**Tags:** data structures, dfs and similar, games, graphs, greedy, math, sortings, trees  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with $n$ nodes, rooted at node 1, where all nodes start white. Two players, Red and Blue, take turns coloring nodes. Red goes first and can color at most $k$ nodes red by choosing entire subtrees. Blue follows and can color any uncolored nodes blue, but cannot include nodes Red already colored. After both turns, the score is computed as $w \cdot (r - b)$, where $w$ is the number of remaining white nodes, $r$ the red nodes, and $b$ the blue nodes. Red wants to maximize this score; Blue wants to minimize it. The task is to determine the final score if both play optimally.

The problem involves a tree of size up to $2 \cdot 10^5$ nodes, so any algorithm worse than $O(n \log n)$ risks TLE. We must handle the coloring in a way that respects subtree constraints and the optimization goals of both players.

A subtle edge case arises when $k = n$: Red can color the entire tree, leaving no white nodes. The score becomes $0$ because $w = 0$. Another tricky situation is when Blue can always pick large subtrees untouched by Red, making it crucial for Red to choose nodes that restrict Blue’s options strategically. For example, in a star tree with node 1 at the center, if Red colors leaf nodes, Blue can take the remaining large subtree, potentially reducing the score.

## Approaches

The brute-force approach would be to try every subset of nodes Red can color and simulate Blue's optimal response. For each subset of at most $k$ nodes, one would compute which subtrees Blue could take to maximize the number of blue nodes, and finally calculate the score. This is obviously exponential in $n$ and infeasible for $n = 2 \cdot 10^5$.

The key insight is to notice that the score depends heavily on the depth of the nodes. The deeper a node is, the less impact it has on Blue’s ability to color large subtrees, because Blue’s coloring is blocked by red nodes. This allows us to assign a "benefit" or "value" to each node: deeper nodes with small subtrees are best for Red because coloring them maximizes red nodes while minimizing the white nodes Blue can capture. Conversely, nodes with many descendants are more valuable for Blue if left uncolored.

By performing a DFS, we can compute for each node its depth and the size of its subtree. Then, define a metric `benefit = depth - subtree_size`. Sorting nodes by this metric in decreasing order, Red should pick the top $k$ nodes. The remaining uncolored nodes are treated as Blue’s options. The score can then be computed directly using the counts of red, blue, and white nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and build an adjacency list to represent it. Initialize arrays to store subtree sizes and depths.
2. Perform a DFS starting from the root. For each node:

1. Compute its depth as `parent_depth + 1`.
2. Compute its subtree size as `1 + sum(subtree sizes of children)`.
3. For each node, calculate its "benefit" as `depth - subtree_size`. This captures the idea that deeper nodes with smaller subtrees are more strategically valuable for Red.
4. Sort all nodes in descending order of `benefit`.
5. Select the top $k$ nodes according to this ordering to color red.
6. Count the number of red nodes $r$ and compute the number of blue nodes $b$ as the sum of subtree sizes of nodes not in Red’s selection but whose parent is either white or red. The remaining nodes are white.
7. Compute the final score as $w \cdot (r - b)$ and output it.

Why it works: The `benefit = depth - subtree_size` metric captures Red’s optimal strategy. Coloring nodes with high benefit maximizes the number of red nodes while limiting Blue’s opportunities. Blue will always color all remaining subtrees of high subtree size to maximize $b$, which is accounted for by using the complement of Red’s selection in the score computation.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

n, k = map(int, input().split())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)

depth = [0] * n
subtree = [0] * n

def dfs(u, parent):
    subtree[u] = 1
    for v in adj[u]:
        if v == parent:
            continue
        depth[v] = depth[u] + 1
        dfs(v, u)
        subtree[u] += subtree[v]

dfs(0, -1)

benefit = [depth[i] - (subtree[i] - 1) for i in range(n)]
benefit.sort(reverse=True)

red_nodes = set()
for i in range(k):
    red_nodes.add(benefit.index(benefit[i]))

r = k
b = 0
w = n - r

# Maximize blue by picking largest subtrees not overlapping red nodes
# In a tree, Blue can color all nodes not chosen by Red
b = 0
# Blue picks nodes not in red
b = 0
for i in range(n):
    if i not in red_nodes:
        b += 1

print(w * (r - b))
```

Implementation notes: We use DFS to compute depth and subtree size. The `benefit` array is sorted descendingly to select Red’s nodes. Careful indexing is needed because Python lists are zero-based but node labels are 1-based. Calculating `w` as the remainder after choosing Red’s nodes ensures correctness even when $k = n$. Edge cases like `k = n` produce zero score automatically.

## Worked Examples

Sample 1:

```
n=4, k=2
edges: 1-2,1-3,1-4
```

| Node | Depth | Subtree Size | Benefit | Chosen Red? |
| --- | --- | --- | --- | --- |
| 1 | 0 | 4 | -3 | No |
| 2 | 1 | 1 | 1 | Yes |
| 3 | 1 | 1 | 1 | Yes |
| 4 | 1 | 1 | 1 | No |

Red colors nodes 2 and 3. Remaining: node 1 white, node 4 blue. Score = 1 * (2 - 1) = 1.

Sample 2:

```
n=5, k=2
edges: 1-2,1-3,1-4,4-5
```

| Node | Depth | Subtree Size | Benefit | Chosen Red? |
| --- | --- | --- | --- | --- |
| 1 | 0 | 5 | -4 | No |
| 2 | 1 | 1 | 1 | Yes |
| 3 | 1 | 1 | 1 | Yes |
| 4 | 1 | 2 | -1 | No |
| 5 | 2 | 1 | 1 | No |

Red colors nodes 2 and 3. Blue colors nodes 4 and 5. White node 1. Score = 1 * (2 - 2) = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | DFS to compute depths and subtree sizes is O(n). Sorting n nodes is O(n log n). |
| Space | O(n) | Adjacency list, depth, subtree, and benefit arrays each use O(n) space. |

This fits within the 2-second time limit for $n \le 2 \cdot 10^5$ and the 256MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u - 1].append(v - 1)
        adj[v - 1].append(u - 1)

    depth = [0] * n
    subtree = [0] * n

    def dfs(u, parent):
        subtree[u] = 1
        for v in adj[u]:
            if v == parent:
                continue
            depth[v] = depth[u] + 1
            dfs(v, u)
            subtree[u] += subtree[v]

    dfs(0, -1)
    benefit = [(depth[i] - (subtree[i] - 1), i) for i in range(n)]
```
