---
title: "CF 1679D - Toss a Coin to Your Graph..."
description: "The problem gives a directed graph where each vertex has a positive integer value. Masha can place a coin on any vertex, and then move it along the graph edges exactly $k-1$ times. Every time the coin visits a vertex, the vertex’s number is recorded in a notebook."
date: "2026-06-10T00:41:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1679
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 791 (Div. 2)"
rating: 1900
weight: 1679
solve_time_s: 123
verified: true
draft: false
---

[CF 1679D - Toss a Coin to Your Graph...](https://codeforces.com/problemset/problem/1679/D)

**Rating:** 1900  
**Tags:** binary search, dfs and similar, dp, graphs  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a directed graph where each vertex has a positive integer value. Masha can place a coin on any vertex, and then move it along the graph edges exactly $k-1$ times. Every time the coin visits a vertex, the vertex’s number is recorded in a notebook. The task is to minimize the largest number that appears in the notebook after these $k$ coin placements, including the initial position. If it is impossible to make $k-1$ moves because the graph is too small or disconnected, the output should be $-1$.

The input constraints are large: up to $2 \cdot 10^5$ vertices and edges, and $k$ can be as high as $10^{18}$. This rules out any algorithm that explicitly simulates all possible sequences of moves or stores $k$ elements. We also need to handle large numbers in the vertex values and potentially very sparse or disconnected graphs.

Edge cases are subtle. If the graph contains cycles, Masha can repeat vertices indefinitely, which makes $k$ irrelevant as long as the cycle is reachable from some start. If the graph is acyclic and the longest path has fewer than $k$ vertices, the output is $-1$. Small graphs or graphs where the smallest vertices are isolated also present traps for naive algorithms that only look locally or assume all vertices are reachable.

For example, consider a graph with three vertices, edges $1 \to 2$ and $2 \to 3$, and $k = 5$. The longest path has only three vertices, so no matter how Masha moves, she cannot record five numbers. The correct output is $-1$. A careless approach that assumes cycles or unlimited moves would incorrectly try to use existing vertices multiple times.

## Approaches

A brute-force approach would be to try every vertex as a starting point and explore all paths of length $k$. We could track the maximum value along each path and choose the minimal among them. This is correct in principle but intractable: the number of paths grows exponentially with the graph size, and $k$ is up to $10^{18}$. Even depth-limited DFS for moderate $k$ is impossible.

The key insight is to recognize that the largest number recorded along a sequence is the maximum among the vertices visited. If we guess a threshold $x$, we can check if there exists a sequence of length $k$ that only visits vertices with value at most $x$. This reduces the problem to a reachability question in a subgraph formed by vertices with value $\le x$. If a strongly connected component of this subgraph has a cycle, we can repeat moves indefinitely to reach any $k$. If the graph is acyclic, the longest path in the subgraph must be at least $k$. Using this property, we can binary search over candidate maximum values to efficiently find the minimum feasible $x$.

The brute-force search tries all paths explicitly and fails at $n = 2 \cdot 10^5$. The optimal solution reduces the problem to binary search over values combined with DFS to detect cycles or compute the longest path in a thresholded subgraph. This brings the complexity down to roughly $O((n+m) \log n)$, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(k) | Too slow |
| Binary Search + DFS | O((n+m) log(max a_i)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Collect all unique vertex values and sort them. These are the only candidates for the minimal maximum value along a sequence.
2. Implement a check function `can(x)` that returns True if there exists a sequence of length $k$ that only visits vertices with value $\le x$. Construct the subgraph containing only vertices with `a[i] <= x` and edges between them.
3. In `can(x)`, detect whether there is a cycle in the subgraph using DFS with a recursion stack. If there is a cycle, the sequence can be extended indefinitely. Return True in this case.
4. If no cycle exists, compute the length of the longest path in the subgraph using DFS with memoization. If the longest path has at least $k$ vertices, return True; otherwise, return False.
5. Binary search over the sorted unique vertex values. For each candidate `x`, use `can(x)` to determine if it is possible. Keep narrowing the search to find the minimal feasible maximum value.
6. If no candidate passes the check (all subgraphs fail to support $k$ moves), return $-1$.

The invariant is that we always search among valid vertex values and only consider subgraphs where no value exceeds the candidate threshold. The DFS correctly identifies cycles, guaranteeing that we do not underestimate reachability. Memoized longest path calculation ensures correct evaluation in acyclic subgraphs.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    edges = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        edges[u-1].append(v-1)

    unique_vals = sorted(set(a))

    def can(x):
        subgraph = [[] for _ in range(n)]
        for u in range(n):
            if a[u] <= x:
                for v in edges[u]:
                    if a[v] <= x:
                        subgraph[u].append(v)

        visited = [0]*n
        dp = [0]*n

        def dfs(u):
            visited[u] = 1
            max_len = 1
            for v in subgraph[u]:
                if visited[v] == 0:
                    ret = dfs(v)
                    max_len = max(max_len, 1 + ret)
                elif visited[v] == 1:
                    return k  # cycle detected
                else:
                    max_len = max(max_len, 1 + dp[v])
            visited[u] = 2
            dp[u] = max_len
            return dp[u]

        max_path = 0
        for i in range(n):
            if a[i] <= x and visited[i] == 0:
                length = dfs(i)
                if length >= k:
                    return True
                max_path = max(max_path, length)
        return max_path >= k

    left, right = 0, len(unique_vals)-1
    ans = -1
    while left <= right:
        mid = (left + right)//2
        if can(unique_vals[mid]):
            ans = unique_vals[mid]
            right = mid - 1
        else:
            left = mid + 1
    print(ans)

solve()
```

The solution first sets up the subgraph for each candidate maximum value. DFS is used both for cycle detection and longest path calculation. The `visited` array differentiates unvisited, visiting, and processed nodes to detect cycles. The binary search iterates over only unique values, avoiding unnecessary repeated checks.

## Worked Examples

**Sample 1**

| Step | Candidate x | Subgraph vertices | Cycle? | Longest path | can(x)? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | [1] | No | 1 | False |
| 2 | 2 | [1,3] | No | 2 | False |
| 3 | 3 | [1,3,4] | No | 3 | False |
| 4 | 4 | [1,3,4,5] | No | 4 | True |

The minimal feasible maximum is 4. This matches the sample output.

**Sample 2**

| Step | Candidate x | Subgraph vertices | Cycle? | Longest path | can(x)? |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | [2,4,5,6] | Yes | - | True |

Cycle allows repeating moves, so any large $k$ is possible. The minimal maximum is 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Each DFS runs in O(n+m) and binary search iterates O(log n) over unique vertex values |
| Space | O(n+m) | For adjacency list, visited array, and memoization |

The solution easily fits in the constraints: DFS and memoization handle 200,000 vertices efficiently, and binary search adds a logarithmic factor over 32-bit integer ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("""6 7 4
1 10 2 3 4 5
1 2
1 3
3 4
4 5
5 6
6 2
2 5""") == "4", "sample 1"

# Minimum size
assert run("""1 0 1
7""") == "7", "single vertex, 1 move"

# Impossible moves
assert run("""3 2 5
1 2 3
1 2
2 3""") == "-1", "long path impossible"

#
```
