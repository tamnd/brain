---
title: "CF 131D - Subway"
description: "We are given a subway system of n stations connected by exactly n passages, each passage connecting two distinct stations. The system forms a connected graph where each station can reach every other station."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 131
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 95 (Div. 2)"
rating: 1600
weight: 131
solve_time_s: 74
verified: true
draft: false
---

[CF 131D - Subway](https://codeforces.com/problemset/problem/131/D)

**Rating:** 1600  
**Tags:** dfs and similar, graphs  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a subway system of _n_ stations connected by exactly _n_ passages, each passage connecting two distinct stations. The system forms a connected graph where each station can reach every other station. By graph theory, a connected graph with _n_ nodes and _n_ edges contains exactly one cycle. This cycle corresponds to the "ringroad" in the problem. The goal is to compute the distance from each station to the ringroad, which is the minimal number of passages to traverse to reach any station on the cycle. Stations that are part of the cycle have distance zero.

The input consists of _n_ lines after the first, each describing a bidirectional connection between two stations. The output is a sequence of _n_ numbers, where the i-th number is the distance of station _i_ to the ringroad.

The constraint _n ≤ 3000_ means that solutions with time complexity up to roughly O(n²) will run comfortably within the 2-second limit. A naive approach that repeatedly searches for distances without exploiting the graph structure could still be too slow if it visits nodes unnecessarily.

Edge cases to be careful about include small cycles, where almost all stations are on the ringroad, and linear chains attached to the cycle, where distances need to propagate correctly along branches. For example, a graph shaped like a triangle with a long tail attached at one node requires that the tail’s nodes are assigned correct incremental distances.

## Approaches

A brute-force approach would first attempt to find the ringroad by checking all possible cycles. This involves enumerating cycles and verifying their uniqueness, which becomes combinatorially expensive, roughly O(n³) for adjacency checks. Once the cycle is known, a BFS from each station to the cycle could compute distances in O(n²). While correct, this is unnecessary work because the graph’s properties allow a more direct approach.

The key observation is that the graph is connected and has exactly one cycle. This implies that any station not in the cycle is part of a tree rooted at some cycle node. Therefore, the problem reduces to two steps: first identify the nodes in the cycle, and then propagate distances to the cycle along the tree branches.

Cycle detection can be performed efficiently with a modified depth-first search. When a back edge is detected during DFS, it marks the presence of the cycle. Tracking the path during DFS allows us to identify exactly which nodes are in the cycle. Once the cycle is identified, a breadth-first search starting from all cycle nodes simultaneously propagates distances outward. Each station will be reached along the shortest path to the cycle, ensuring correct distance assignment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all cycles + BFS per node) | O(n³) | O(n²) | Too slow |
| DFS for cycle + BFS for distances | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent the subway as an adjacency list where each station maps to the list of stations it connects to. This structure allows O(1) iteration over neighbors.
2. Run a depth-first search to detect the unique cycle. Track the parent of each node during DFS. If a visited node is encountered that is not the parent, a cycle is found. Record all nodes along the DFS path between the current node and the visited node to identify the cycle.
3. Initialize a distance array with -1 for all stations, meaning "unvisited." Set distance 0 for all stations identified in the cycle.
4. Use a queue to perform breadth-first search starting from all cycle nodes simultaneously. For each node dequeued, iterate over its neighbors. If a neighbor’s distance is -1, set it to the current node’s distance plus one and enqueue it.
5. Continue BFS until all nodes have a distance assigned. At the end, the distance array contains the minimal distance from each station to the ringroad.

Why it works: The DFS guarantees identification of the unique cycle because the graph has exactly one cycle. BFS propagates distances from the cycle outward in layers, and since all edges are equal weight, the first time a node is visited is via the shortest path to the cycle.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline
sys.setrecursionlimit(10000)

n = int(input())
adj = [[] for _ in range(n)]
for _ in range(n):
    u, v = map(int, input().split())
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)

visited = [False] * n
parent = [-1] * n
cycle_nodes = []

def dfs(u, p):
    visited[u] = True
    for v in adj[u]:
        if v == p:
            continue
        if visited[v]:
            # cycle detected, reconstruct path
            cycle_nodes.append(v)
            node = u
            while node != v:
                cycle_nodes.append(node)
                node = parent[node]
            return True
        parent[v] = u
        if dfs(v, u):
            return True
    return False

dfs(0, -1)

dist = [-1] * n
q = deque()
for node in cycle_nodes:
    dist[node] = 0
    q.append(node)

while q:
    u = q.popleft()
    for v in adj[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            q.append(v)

print(' '.join(map(str, dist)))
```

The adjacency list represents the subway efficiently. The DFS function tracks parent nodes to reconstruct the cycle when a back edge is encountered. BFS ensures all distances propagate correctly, with the initial cycle nodes at distance zero. Care is taken to avoid revisiting nodes and to handle 1-based input by converting to 0-based indices.

## Worked Examples

### Sample Input 1

```
4
1 3
4 3
4 2
1 2
```

| Node | DFS parent | Cycle nodes | BFS queue | Distance array |
| --- | --- | --- | --- | --- |
| 1 | - | 1,2,3,4 | 1,2,3,4 | 0,0,0,0 |

All nodes are part of the cycle, so BFS does not expand further. Each distance is 0, as expected.

### Custom Input 2

```
6
1 2
2 3
3 1
3 4
4 5
5 6
```

| Node | DFS parent | Cycle nodes | BFS queue | Distance array |
| --- | --- | --- | --- | --- |
| 1 | - | 1,2,3 | 1,2,3 | 0,0,0,-1,-1,-1 |
| 4 | 3 |  | 4 | 1 |
| 5 | 4 |  | 5 | 2 |
| 6 | 5 |  | 6 | 3 |

This shows that BFS propagates distances along the tree attached to the cycle. Node 4 is 1 passage away, node 5 is 2, and node 6 is 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once in DFS and once in BFS. Each edge is traversed at most twice. |
| Space | O(n) | Adjacency list, parent array, visited array, and BFS queue all scale linearly. |

With _n ≤ 3000_, this runs comfortably within the time and memory limits.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline
    sys.setrecursionlimit(10000)

    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n):
        u, v = map(int, input().split())
        adj[u - 1].append(v - 1)
        adj[v - 1].append(u - 1)

    visited = [False] * n
    parent = [-1] * n
    cycle_nodes = []

    def dfs(u, p):
        visited[u] = True
        for v in adj[u]:
            if v == p:
                continue
            if visited[v]:
                cycle_nodes.append(v)
                node = u
                while node != v:
                    cycle_nodes.append(node)
                    node = parent[node]
                return True
            parent[v] = u
            if dfs(v, u):
                return True
        return False

    dfs(0, -1)

    dist = [-1] * n
    q = deque()
    for node in cycle_nodes:
        dist[node] = 0
        q.append(node)

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    return ' '.join(map(str, dist))

# Provided sample
assert run("4\n1 3\n4 3\n4 2\n1 2\n") == "0 0 0 0", "sample 1"

# Custom tests
assert run("6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 6\n") == "0 0 0 1 2 3", "triangle with tail"
assert run("3\n1 2\n2 3\n3 1\n") == "
```
