---
title: "CF 61D - Eternal Victory"
description: "We are asked to find the minimum distance Shapur must travel to visit all cities at least once. The cities are connected in a tree structure, meaning there are exactly $n-1$ bidirectional roads and a unique path between any two cities."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "greedy", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 61
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 57 (Div. 2)"
rating: 1800
weight: 61
solve_time_s: 89
verified: true
draft: false
---

[CF 61D - Eternal Victory](https://codeforces.com/problemset/problem/61/D)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, greedy, shortest paths, trees  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the minimum distance Shapur must travel to visit all cities at least once. The cities are connected in a tree structure, meaning there are exactly $n-1$ bidirectional roads and a unique path between any two cities. Shapur starts at city 1 and can finish in any city. Each road has a weight, representing its length. The input gives the number of cities $n$ and then $n-1$ triples describing the roads with their weights. The output is a single integer: the minimum total travel distance.

Because $n$ can be as large as $10^5$, any solution that is worse than linear or near-linear in the number of cities and roads will be too slow. A naive solution that tries all possible routes or permutations is clearly infeasible since the number of permutations grows factorially. We need to exploit the tree structure to reduce the number of computations.

A non-obvious edge case is a tree where the heaviest path is in a long chain from city 1 to a leaf. For instance, with three cities in a line: city 1 connected to 2 with weight 10, and 2 connected to 3 with weight 20. The optimal strategy is to walk 1 → 2 → 3 and stop at 3. A careless approach that assumes Shapur must return to city 1 would incorrectly double some edge weights, giving 60 instead of 30.

Another subtle case is when the tree is star-shaped, all cities directly connected to city 1. Here, the optimal path can traverse each edge only once without returning, so summing all edge weights gives the answer.

## Approaches

A brute-force approach would generate all paths starting at city 1 that visit every city exactly once, compute their distances, and take the minimum. While this is correct, the number of possible paths in a tree is factorial in the number of cities for non-trivial shapes, which becomes infeasible for $n$ as large as $10^5$.

The key observation is that the cities form a tree. To visit all cities, every edge must be traversed at least once, since omitting an edge would leave its connected cities unvisited. If we ignore the starting city, the naive method would traverse each edge twice: once to go deeper, once to backtrack. This counts each edge as double its weight. The only way to save distance is to avoid backtracking on the longest single path from city 1, which will be the path from city 1 to the furthest leaf. Traversing the longest path only once instead of twice gives the minimal total distance.

Therefore, the optimal approach is to sum all edge weights multiplied by two and then subtract the maximum distance from city 1 to any leaf. The DFS is used to compute this maximum distance efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input to read $n$ and the $n-1$ edges. Store the edges in an adjacency list with both the neighbor and the edge weight. This representation allows fast traversal from any city.
2. Compute the total sum of all edge weights. Since each edge must be traversed at least once in both directions except on the path where we avoid backtracking, this sum multiplied by two gives the naive total travel if we were to return to the start after visiting each branch.
3. Perform a depth-first search starting at city 1 to find the maximum distance from city 1 to any leaf. Initialize a distance accumulator to 0, then for each neighbor not yet visited, recursively compute the path length and keep track of the maximum.
4. Subtract the maximum distance obtained from the double total to get the minimal travel distance. This works because along the path from the root to the furthest leaf, we do not need to backtrack over the edges; all other edges are counted twice.

Why it works: Every edge must be traversed at least once to ensure all cities are visited. Counting each edge twice initially accounts for going out and returning. By identifying the longest single path from the starting city, we can avoid one traversal of those edges. DFS guarantees that we accurately find this path in linear time, and the subtraction of this maximum path length ensures minimal travel without missing any city.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

n = int(input())
adj = [[] for _ in range(n + 1)]
total_weight = 0

for _ in range(n - 1):
    u, v, w = map(int, input().split())
    adj[u].append((v, w))
    adj[v].append((u, w))
    total_weight += w

visited = [False] * (n + 1)
max_path = 0

def dfs(node, dist):
    global max_path
    visited[node] = True
    if dist > max_path:
        max_path = dist
    for neighbor, weight in adj[node]:
        if not visited[neighbor]:
            dfs(neighbor, dist + weight)

dfs(1, 0)

result = 2 * total_weight - max_path
print(result)
```

The adjacency list is chosen for efficient DFS traversal. The global variable `max_path` keeps track of the maximum distance. The DFS accumulates distances recursively and ensures each node is visited once. We multiply the total weight by two because we initially assume we go to each city and back. Subtracting `max_path` avoids double-counting the longest path from the root to a leaf.

## Worked Examples

### Sample 1

Input:

```
3
1 2 3
2 3 4
```

| Step | Node | Dist | max_path | Notes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | Start DFS |
| 2 | 2 | 3 | 3 | Visit neighbor 2 |
| 3 | 3 | 7 | 7 | Visit neighbor 3 |

Total weight = 3 + 4 = 7. Multiply by 2 → 14. Subtract max_path 7 → 7. Output is 7. Confirms minimal travel is achieved by walking 1→2→3 and stopping.

### Custom Input 2

```
5
1 2 1
1 3 2
3 4 3
3 5 4
```

| Step | Node | Dist | max_path | Notes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | Start DFS |
| 2 | 2 | 1 | 1 | Visit neighbor 2 |
| 3 | 3 | 2 | 2 | Visit neighbor 3 |
| 4 | 4 | 5 | 5 | Visit neighbor 4 |
| 5 | 5 | 6 | 6 | Visit neighbor 5 |

Total weight = 1+2+3+4=10 → doubled = 20. Subtract max_path 6 → 14. Optimal path 1→3→5, then back to 3→4→3→1→2. Confirms algorithm handles branching paths correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | DFS visits each node and edge exactly once |
| Space | O(n) | Adjacency list and visited array take linear space |

Given the constraints of $n \le 10^5$, a linear algorithm is efficient and fits comfortably within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    adj = [[] for _ in range(n + 1)]
    total_weight = 0
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
        adj[v].append((u, w))
        total_weight += w

    visited = [False] * (n + 1)
    max_path = 0

    def dfs(node, dist):
        nonlocal max_path
        visited[node] = True
        if dist > max_path:
            max_path = dist
        for neighbor, weight in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor, dist + weight)

    dfs(1, 0)
    return str(2 * total_weight - max_path)

# provided sample
assert run("3\n1 2 3\n2 3 4\n") == "7", "sample 1"

# custom tests
assert run("1\n") == "0", "single node"
assert run("2\n1 2 10\n") == "10", "two nodes only"
assert run("4\n1 2 1\n2 3 2\n3 4 3\n") == "6", "linear chain"
assert run("5\n1 2 1\n1 3 2\n3 4 3\n3 5 4\n") == "14", "branching tree"
assert run("3\n1 2 0\n2 3 0\n") == "0", "zero-weight edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
|  |  |  |
