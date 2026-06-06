---
title: "CF 402E - Strictly Positive Matrix"
description: "We are given a square matrix $a$ of size $n times n$ whose elements are all non-negative integers. The matrix can be thought of as a weighted adjacency matrix of a graph with $n$ nodes, where $a{ij} 0$ indicates a direct edge from node $i$ to node $j$."
date: "2026-06-07T01:23:32+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 402
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 236 (Div. 2)"
rating: 2200
weight: 402
solve_time_s: 248
verified: true
draft: false
---

[CF 402E - Strictly Positive Matrix](https://codeforces.com/problemset/problem/402/E)

**Rating:** 2200  
**Tags:** graphs, math  
**Solve time:** 4m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square matrix $a$ of size $n \times n$ whose elements are all non-negative integers. The matrix can be thought of as a weighted adjacency matrix of a graph with $n$ nodes, where $a_{ij} > 0$ indicates a direct edge from node $i$ to node $j$.

The task is to determine if there exists a positive integer $k$ such that raising the matrix to the power $k$, denoted $a^k$, results in a matrix where every entry is strictly positive. This corresponds to asking whether, in graph terms, every node can reach every other node in exactly $k$ steps along paths formed by the original edges.

The constraints are significant. $n$ can be as large as 2000, so any solution that tries to explicitly compute $a^k$ by multiplying matrices naively is immediately infeasible. A single matrix multiplication is $O(n^3)$, which is already 8 billion operations at the worst case-far too slow.

Subtle edge cases arise from disconnected nodes or blocks. For example, consider the identity matrix:

```
2
1 0
0 1
```

Here, no power of the matrix can connect the off-diagonal elements, so the answer is "NO". A naive approach that simply checks if $a$ has non-zero elements might falsely say "YES" if it ignores the reachability structure of the matrix.

Another non-obvious case is a cyclic permutation:

```
3
0 1 0
0 0 1
1 0 0
```

This matrix does eventually become strictly positive at $a^3$ because each node can reach every other node in three steps. A careless implementation that only checks $a$ or $a^2$ would fail.

Understanding this problem as a graph reachability problem is the key to efficiency.

## Approaches

The brute-force approach is straightforward: repeatedly multiply the matrix by itself and check if all elements are positive after each multiplication. Start with $a$, then $a^2$, then $a^3$, and so on. Stop when either all elements are positive or the matrix stabilizes. This is correct because matrix multiplication exactly models the combination of paths of increasing length. However, the worst-case complexity is $O(n^4)$ if we multiply up to $n$ times, since each multiplication is $O(n^3)$. For $n = 2000$, this is completely impractical.

The optimal approach leverages graph theory. Interpret the matrix as the adjacency matrix of a directed graph. Each non-zero entry indicates an edge. The matrix becomes strictly positive at some power if and only if the graph is **strongly connected**, meaning there is a path from every node to every other node. Checking strong connectivity can be done efficiently using a depth-first search (DFS) or breadth-first search (BFS) twice: once on the original graph, and once on the transposed graph. This reduces the complexity to $O(n^2)$, since we only need to traverse all edges, and each traversal of the adjacency matrix costs $O(n^2)$ in the worst case.

The brute-force works because it literally constructs the reachability matrix, but it fails due to the cubic cost per multiplication and the unknown number of multiplications needed. The graph approach works because strong connectivity guarantees the existence of a positive power, independent of the actual numerical values in the matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n^2) | Too slow |
| Graph Connectivity | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Construct the adjacency graph from the matrix $a$. For every $a_{ij} > 0$, add a directed edge from node $i$ to node $j$. This abstracts away the numeric values and focuses only on reachability.
2. Pick any node, for instance node 1, and perform a DFS to mark all nodes reachable from it in the original graph. If any node is unvisited, the graph is not strongly connected, and we can return "NO" immediately.
3. Construct the transpose of the graph by reversing all edges. This flips the direction of reachability.
4. Perform a DFS from the same node in the transposed graph. If any node is unvisited, the original graph is not strongly connected, and we return "NO".
5. If both DFS traversals visited all nodes, the graph is strongly connected. This guarantees that there exists some positive integer $k$ such that $a^k$ is strictly positive, so we return "YES".

**Why it works**: The DFS checks ensure that every node can reach every other node (original graph) and that every node can be reached from every other node (transposed graph). Together, these two conditions are exactly the definition of strong connectivity. The Perron-Frobenius theorem from linear algebra guarantees that a strongly connected non-negative matrix has a power that is strictly positive, which is exactly what we need.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(5000)

def main():
    n = int(input())
    adj = [[] for _ in range(n)]
    for i in range(n):
        row = list(map(int, input().split()))
        for j in range(n):
            if row[j] > 0:
                adj[i].append(j)

    visited = [False] * n

    def dfs(v, graph):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                dfs(u, graph)

    # Check reachability from node 0
    dfs(0, adj)
    if not all(visited):
        print("NO")
        return

    # Check reachability in the transposed graph
    adj_t = [[] for _ in range(n)]
    for i in range(n):
        for j in adj[i]:
            adj_t[j].append(i)

    visited = [False] * n
    dfs(0, adj_t)
    if not all(visited):
        print("NO")
    else:
        print("YES")

if __name__ == "__main__":
    main()
```

The code first converts the matrix into an adjacency list. The DFS ensures that every node is reachable from the starting node in both the original and transposed graphs. Using an adjacency list instead of repeatedly multiplying matrices is critical to stay within time limits. Increasing the recursion limit handles the maximum depth for DFS on the worst-case graph.

## Worked Examples

**Sample 1**

Input:

```
2
1 0
0 1
```

| Step | DFS Visited (Original) | DFS Visited (Transpose) |
| --- | --- | --- |
| Start node 0 | [True, False] | - |
| Transpose DFS | - | [True, False] |

Both DFS traversals leave node 1 unvisited, so the output is "NO". This demonstrates handling of disconnected blocks.

**Custom Sample 2**

Input:

```
3
0 1 0
0 0 1
1 0 0
```

| Step | DFS Visited (Original) | DFS Visited (Transpose) |
| --- | --- | --- |
| Start node 0 | [True, True, True] | - |
| Transpose DFS | - | [True, True, True] |

All nodes are reachable in both graphs, so the output is "YES". This shows that cycles ensure eventual positivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each DFS traverses all edges; there can be up to n^2 edges. |
| Space | O(n^2) | Adjacency list may store all edges in the worst case; visited array uses O(n). |

For $n \le 2000$, the algorithm executes at most 4 million operations, comfortably under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("2\n1 0\n0 1\n") == "NO", "sample 1"

# custom cases
assert run("3\n0 1 0\n0 0 1\n1 0 0\n") == "YES", "cyclic 3x3"
assert run("2\n1 1\n1 1\n") == "YES", "all ones"
assert run("2\n0 1\n0 0\n") == "NO", "single direction, not strongly connected"
assert run("4\n0 1 0 0\n0 0 1 0\n0 0 0 1\n1 0 0 0\n") == "YES", "4-cycle"
assert run("2\n0 0\n0 0\n") == "NO", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-cycle | YES | cyclic reachability leads to eventual positivity |
| all ones | YES | matrix already fully connected |
| single direction | NO | one-way connection, |
