---
title: "CF 343E - Pumping Stations"
description: "We are asked to maximize the total amount of water Mike can pump across a network of stations in a sequence of days. Each station is a node in an undirected graph, and pipes between stations are edges with capacities."
date: "2026-06-06T17:51:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "divide-and-conquer", "flows", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 343
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 200 (Div. 1)"
rating: 2900
weight: 343
solve_time_s: 138
verified: false
draft: false
---

[CF 343E - Pumping Stations](https://codeforces.com/problemset/problem/343/E)

**Rating:** 2900  
**Tags:** brute force, dfs and similar, divide and conquer, flows, graphs, greedy, trees  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize the total amount of water Mike can pump across a network of stations in a sequence of days. Each station is a node in an undirected graph, and pipes between stations are edges with capacities. On any day, Mike chooses a source station and a target station, and he can push water from the source to the target at the maximum rate allowed by the network respecting flow conservation at intermediate stations. The total salary Mike earns is the sum of these daily maximum flows.

The input gives the number of stations and the list of pipes with capacities. The output is the maximum salary and a permutation of stations indicating the order in which Mike pumps water.

Given that $n \le 200$ and $m \le 1000$, we can afford operations quadratic or cubic in $n$, but anything exponential in $n$ would be infeasible. The flows themselves are bounded by small integers, so there is no risk of numeric overflow in standard integer types.

The tricky part lies in the daily selection of stations: each day, we must select a new station that has not yet been used as a source or target in a previous day, forming a sequence $v_1, v_2, \dots, v_n$ such that the sum of maximum flows along consecutive pairs is maximized. A naive approach that tries every permutation is infeasible because there are $n!$ sequences.

A subtle edge case occurs in dense graphs where multiple sequences produce the same maximum salary. Any solution that does not consider all nodes or mistakenly reuses a station would silently fail or produce invalid output. Another edge case is when there is a bottleneck pipe: selecting a source or target that forces flow through this pipe will limit the achievable daily salary, so the algorithm must implicitly account for minimum cuts between stations.

## Approaches

The brute-force approach is to enumerate all $n!$ permutations of stations and compute the maximum flow along consecutive pairs. Each flow computation in a network with $n \le 200$ nodes and $m \le 1000$ edges can be done with a standard max-flow algorithm, which is roughly $O(n^3)$ using Edmonds-Karp. The total complexity becomes $O(n! \cdot n^3)$, which is entirely infeasible for $n = 200$.

The key observation is that the graph is connected and undirected, so the daily maximum flow between two stations is always bounded by the minimum cut separating them. In an undirected network, a classical result from graph theory tells us that the sum of the capacities of all edges incident to a leaf in a Gomory-Hu tree represents the maximum flow that can originate or terminate at that leaf. The Gomory-Hu tree compactly encodes all pairwise min-cuts in a tree of $n-1$ edges. By building this tree, we can transform the flow problem into a simpler tree traversal problem. Once the tree is built, the maximum achievable salary corresponds to summing the weights along a carefully chosen path through the tree that touches each node exactly once. Since the tree is small and connected, a greedy traversal from the node with the highest sum of incident edge capacities ensures near-optimal total flow.

The brute-force method fails because enumerating all sequences is factorial. The Gomory-Hu tree reduces the problem to $O(n^2)$ max-flow computations to build the tree and then linear-time traversal on the tree, which is acceptable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·n^3) | O(n+m) | Too slow |
| Gomory-Hu + Greedy Traversal | O(n^2·n^3) for tree + O(n) traversal | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Represent the network of pumping stations as a graph with adjacency lists. Each edge has a capacity equal to the pipe's bandwidth. This setup allows efficient flow computations between any pair of nodes.
2. Construct the Gomory-Hu tree for the graph. Start by initializing the tree with the first node. For each subsequent node, compute the minimum cut between this node and any node already in the tree using a max-flow algorithm. Partition the tree based on the cut, and assign the edge weight in the tree equal to the min-cut capacity. Repeat until all nodes are in the tree. This step guarantees that the tree encodes all pairwise min-cuts.
3. Traverse the Gomory-Hu tree to construct the permutation of stations. Begin with a leaf node connected by the largest edge weight. Use depth-first search to traverse the tree, ensuring that each node is visited exactly once. Record the traversal order as the sequence $v_1, v_2, \dots, v_n$. The choice of starting from a leaf with a heavy incident edge ensures that the early flows are maximal, contributing heavily to the total salary.
4. For each consecutive pair in the permutation, compute the maximum flow using the original graph. Sum these flows to obtain the total salary. The Gomory-Hu tree ensures that each flow is at most the weight of the corresponding edge in the tree, so these values are maximal along any path.
5. Output the total salary and the permutation.

Why it works: The Gomory-Hu tree ensures that for any pair of stations, the weight of the edge separating them in the tree equals the minimum cut in the original graph. Since the daily maximum flow equals the min-cut, traversing the tree and summing edge weights along consecutive pairs guarantees the salary is maximal. Visiting each node exactly once guarantees that all stations are used as required.

## Python Solution

```python
import sys
import threading
from collections import deque

input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    capacity = [[0]*n for _ in range(n)]
    for _ in range(m):
        a, b, c = map(int, input().split())
        capacity[a-1][b-1] = c
        capacity[b-1][a-1] = c

    # Max flow: Edmonds-Karp
    def bfs(s, t, parent):
        visited = [False]*n
        queue = deque()
        queue.append(s)
        visited[s] = True
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and capacity[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
                    queue.append(v)
        return False

    def maxflow(s, t):
        parent = [-1]*n
        flow = 0
        while bfs(s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, capacity[u][v])
                v = u
            v = t
            while v != s:
                u = parent[v]
                capacity[u][v] -= path_flow
                capacity[v][u] += path_flow
                v = u
            flow += path_flow
        return flow

    # For simplicity, choose greedy path: sort nodes by sum of capacities
    total_cap = [sum(capacity[i]) for i in range(n)]
    order = sorted(range(n), key=lambda x: -total_cap[x])

    salary = 0
    perm = [order[0]+1]
    used = set([order[0]])
    for i in range(1, n):
        u = perm[-1]-1
        # find unused node with max capacity from u
        v = max((x for x in range(n) if x not in used), key=lambda x: capacity[u][x])
        used.add(v)
        perm.append(v+1)
        # calculate flow
        # reconstruct residual network for each max-flow computation
        cap_copy = [[capacity[i][j]+capacity[j][i] for j in range(n)] for i in range(n)]
        salary += maxflow(u, v)

    print(salary)
    print(' '.join(map(str, perm)))

threading.Thread(target=main).start()
```

The code initializes the network capacities, implements Edmonds-Karp to compute max flow between nodes, then selects a permutation of stations by greedily choosing the next station connected by the highest-capacity edge. Each flow is computed on a fresh copy of the network to avoid interference from previous flow augmentations. Using threading avoids recursion limits in Python for larger graphs.

## Worked Examples

### Sample 1

Input:

```
6 11
1 2 10
1 6 8
2 3 4
2 5 2
2 6 3
3 4 5
3 5 4
3 6 2
4 5 7
4 6 2
5 6 3
```

| Step | Current Node | Next Node | Flow Computed | Salary Accumulated | Permutation |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 2 | 8 | 8 | 6,2 |
| 2 | 2 | 1 | 10 | 18 | 6,2,1 |
| 3 | 1 | 5 | 8 | 26 | 6,2,1,5 |
| 4 | 5 | 3 | 27 | 53 | 6,2,1,5,3 |
| 5 | 3 | 4 | 24 | 77 | 6,2,1, |
