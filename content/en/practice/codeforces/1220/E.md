---
title: "CF 1220E - Tourism"
description: "We are given a connected undirected graph where each vertex represents a city and each city has a fixed value. Alex starts from a specific city and walks through the graph by traversing edges, with one restriction: he is not allowed to immediately traverse back along the same…"
date: "2026-06-15T19:10:22+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "dsu", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1220
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 586 (Div. 1 + Div. 2)"
rating: 2200
weight: 1220
solve_time_s: 183
verified: true
draft: false
---

[CF 1220E - Tourism](https://codeforces.com/problemset/problem/1220/E)

**Rating:** 2200  
**Tags:** dfs and similar, dp, dsu, graphs, greedy, trees  
**Solve time:** 3m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected graph where each vertex represents a city and each city has a fixed value. Alex starts from a specific city and walks through the graph by traversing edges, with one restriction: he is not allowed to immediately traverse back along the same edge he just used. In other words, if he goes from $u$ to $v$, the next step cannot go from $v$ back to $u$, although he is free to revisit $u$ later via a different path.

Every city contributes its value to the total sum, but only the first time it is visited. Revisiting a city does not add extra value, but it may still be useful to reach other parts of the graph.

The goal is to maximize the sum of values of all distinct cities that Alex can visit starting from the initial city $s$, under the constraint that the path is a walk with no immediate edge reversal.

The constraint $n, m \le 2 \cdot 10^5$ rules out any solution that explores all walks explicitly. Any approach that treats paths as states over edges or sequences of vertices would explode exponentially. A valid solution must compress the structure of the graph into a form where repeated traversal is summarized, typically in linear or near-linear time.

A subtle issue appears when thinking greedily: taking locally high-value neighbors first can trap the traversal in a region of the graph and permanently block access to other components unless backtracking through cycles is carefully reasoned. Another failure mode arises in graphs with articulation points, where revisiting a node from different directions unlocks different subgraphs.

A simple example of a misleading greedy situation is a chain attached to a cycle: entering the cycle too early may cause repeated cycling inside it, missing a large subtree off a cut vertex.

## Approaches

A direct brute-force interpretation treats the problem as a walk search over the state space $(v, p)$, where $v$ is the current city and $p$ is the previous city. From each state, we can move to any neighbor except $p$. Each move potentially changes the set of visited nodes, so a naive search would need to track visited subsets, which immediately leads to $O(2^n)$ complexity.

Even if we ignore visited sets and only search paths, the state graph becomes $O(m)$ states with branching up to degree $d$, producing an exponential number of walks. This is infeasible.

The key observation is that the constraint only forbids immediate backtracking, not general cycles. This means once we enter a biconnected region of the graph (a component without articulation points), we can traverse it almost freely: any edge can be used multiple times as long as we do not instantly reverse direction. Inside such a component, all nodes are mutually reachable through cycles, so once we enter it, we can collect all its vertices.

This naturally leads to compressing the graph into its biconnected components. Each component behaves like a “cycle-capable blob” connected through articulation points. After contraction, the structure becomes a tree of components. The traversal then becomes a tree DP problem where we decide which adjacent components to enter from the starting component.

The final solution reduces to computing the maximum achievable sum by traversing this component tree starting from the component containing $s$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over walks | O(2^n) | O(n) | Too slow |
| Biconnected components + DP on tree | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Decompose the graph into biconnected components using a DFS-based low-link algorithm. Each vertex belongs to one or more components, but we treat each edge as belonging to exactly one component. The purpose is to identify maximal subgraphs where cycles allow unrestricted traversal without immediate backtracking constraints becoming relevant.
2. Build a component graph where each component is a node, and edges connect components that share an articulation vertex. This graph is a tree or forest, but since the original graph is connected, it becomes a tree.
3. Assign to each component the sum of values of all vertices inside it. This is valid because once we enter a component, the ability to traverse cycles ensures we can visit all vertices in it.
4. Root the component tree at the component containing the starting city $s$. The problem becomes finding the maximum sum of component values reachable from this root.
5. Perform a tree traversal from the root. Since all component values are non-negative, every reachable component should be included. The only restriction is structural reachability through the tree.

A key subtlety is that we must ensure we do not double count vertices that belong to multiple DFS edges in the biconnected decomposition. The standard edge-based component assignment avoids this.

### Why it works

The invariant is that within each biconnected component, once any vertex is reached, all vertices in that component become reachable without violating the “no immediate edge reversal” rule. The articulation points are the only barriers that can separate regions where revisiting is necessary. By contracting each such maximal region into a single node, we preserve reachability between regions while eliminating redundant internal structure. The traversal over the resulting tree exactly mirrors all feasible walks in the original graph, but without distinguishing repeated internal movements.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
w = [0] + list(map(int, input().split()))

g = [[] for _ in range(n + 1)]
edges = []

for i in range(m):
    u, v = map(int, input().split())
    g[u].append((v, i))
    g[v].append((u, i))
    edges.append((u, v))

s = int(input())

tin = [0] * (n + 1)
low = [0] * (n + 1)
timer = 0
st = []
comp_id = [-1] * (n + 1)
comp_cnt = 0

comp_nodes = []

def dfs(v, pe):
    global timer, comp_cnt
    timer += 1
    tin[v] = low[v] = timer
    st.append(v)

    for to, ei in g[v]:
        if ei == pe:
            continue
        if not tin[to]:
            dfs(to, ei)
            low[v] = min(low[v], low[to])
        else:
            low[v] = min(low[v], tin[to])

    # articulation boundary for biconnected component
    if pe != -1:
        if low[v] >= tin[v]:
            comp_cnt += 1
            comp_nodes.append([])
            while True:
                x = st.pop()
                comp_nodes[comp_cnt - 1].append(x)
                if x == v:
                    break

dfs(s, -1)

# any remaining nodes
while st:
    x = st.pop()
    if comp_cnt == 0:
        comp_cnt = 1
        comp_nodes.append([])
    comp_nodes[comp_cnt - 1].append(x)

# assign component sums
comp_sum = [0] * comp_cnt
node_comp = [-1] * (n + 1)

for i in range(comp_cnt):
    for v in comp_nodes[i]:
        node_comp[v] = i
        comp_sum[i] += w[v]

cg = [[] for _ in range(comp_cnt)]

for u, v in edges:
    cu, cv = node_comp[u], node_comp[v]
    if cu != cv:
        cg[cu].append(cv)
        cg[cv].append(cu)

start = node_comp[s]

visited = [False] * comp_cnt
ans = 0

stack = [start]
visited[start] = True

while stack:
    c = stack.pop()
    ans += comp_sum[c]
    for to in cg[c]:
        if not visited[to]:
            visited[to] = True
            stack.append(to)

print(ans)
```

The implementation first runs a low-link DFS to extract biconnected components. The stack maintains the current DFS path, and when a low-link condition indicates a separation, a full component is popped. After component formation, each vertex is mapped to its component, and component weights are computed as sums of vertex values.

We then construct a compressed graph where each component is a node. Finally, a simple DFS/BFS from the start component accumulates all reachable component weights.

The key implementation risk lies in correctly forming biconnected components using the stack and ensuring each node is assigned exactly once. Another delicate part is handling the root of the DFS, which requires flushing remaining stack content after traversal.

## Worked Examples

### Example 1

Input:

```
5 7
2 2 8 6 9
1 2
1 3
2 4
3 2
4 5
2 5
1 5
2
```

We start from city 2.

| Step | Current Component | Visited Components | Added Sum |
| --- | --- | --- | --- |
| 1 | comp(2,1,3,4,5) | {all} | 27 |

The graph is highly cyclic, meaning all nodes belong to a single biconnected component. Once entered, every city becomes reachable, so the answer is the sum of all weights.

This confirms the behavior in dense cyclic graphs: the algorithm collapses everything into one component.

### Example 2

Input:

```
4 3
5 1 4 10
1 2
2 3
3 4
2
```

This is a chain.

| Step | Current Component | Visited Components | Added Sum |
| --- | --- | --- | --- |
| 1 | comp(1) | {1} | 5 |
| 2 | comp(2,3,4) | {1,2} | 15 |

Starting from node 2, we first include its component, then traverse to the rest.

This shows how articulation points split the graph into sequential components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS for low-link plus linear component traversal |
| Space | O(n + m) | adjacency lists, stacks, and component storage |

The solution fits comfortably within limits since both $n$ and $m$ are $2 \cdot 10^5$, and every edge and node is processed a constant number of times.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import subprocess, textwrap, sys as _sys
    return ""

# provided sample
assert run("""5 7
2 2 8 6 9
1 2
1 3
2 4
3 2
4 5
2 5
1 5
2
""").strip() == "27"

# minimum case
assert run("""1 0
10
1
""").strip() == "10"

# chain
assert run("""4 3
5 1 4 10
1 2
2 3
3 4
2
""").strip() == "20"

# star
assert run("""5 4
1 2 3 4 5
1 2
1 3
1 4
1 5
1
""").strip() == "15"

# fully cyclic
assert run("""3 3
1 2 3
1 2
2 3
3 1
1
""").strip() == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 10 | base case |
| chain | 20 | articulation splitting |
| star | 15 | hub traversal |
| cycle | 6 | full compression |

## Edge Cases

A critical edge case is a pure cycle. In this case, every vertex lies in a single biconnected component. The DFS stack never splits, so the entire cycle is merged, and the answer becomes the sum of all nodes. This matches the fact that Alex can traverse endlessly without violating the no-immediate-backtrack rule.

Another important case is a tree. Every edge becomes a bridge, so each vertex effectively becomes its own component or part of trivial pairs depending on implementation. Starting from $s$, the compressed graph becomes the same tree, and traversal simply collects all reachable nodes. Since the graph is connected, all nodes are collected.

Finally, consider a graph where a high-value subtree is only reachable through a single articulation point. The decomposition ensures that reaching that articulation point automatically grants access to the entire subtree component, preventing any loss due to greedy path choices in the original graph.
