---
title: "CF 217A - Ice Skating"
description: "We are given a set of snow drifts on a 2D grid with integer coordinates. Bajtek can move only in straight lines along the x or y axis, sliding from one drift until he hits another."
date: "2026-06-05T00:53:21+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 217
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 134 (Div. 1)"
rating: 1200
weight: 217
solve_time_s: 87
verified: false
draft: false
---

[CF 217A - Ice Skating](https://codeforces.com/problemset/problem/217/A)

**Rating:** 1200  
**Tags:** brute force, dfs and similar, dsu, graphs  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of snow drifts on a 2D grid with integer coordinates. Bajtek can move only in straight lines along the x or y axis, sliding from one drift until he hits another. In other words, two snow drifts are connected if they share either the same x-coordinate or the same y-coordinate. Bajtek wants to be able to travel between any two snow drifts, directly or indirectly, so we need to add the minimum number of new snow drifts to make the set fully connected under these movement rules.

The input gives the number of existing drifts $n$ (up to 100) and their coordinates. The output is a single integer: the fewest additional drifts required to connect all existing drifts. The small value of $n$ indicates that an $O(n^2)$ solution is acceptable, which allows us to consider all pairs of drifts when determining connectivity.

A subtle point arises when drifts are in isolated clusters. For example, if there are two drifts at (1,1) and (2,2), they cannot reach each other directly. Adding one drift at (1,2) or (2,1) will connect them. A careless approach might try to consider only direct pairwise moves or assume diagonal adjacency works, which would produce an incorrect answer of zero for this case.

Another edge case is when all drifts lie on the same row or column. For instance, three drifts at (1,1), (1,2), (1,3) already form a single connected component, so no new drift is needed. Misunderstanding this could lead to adding unnecessary drifts.

## Approaches

A brute-force method would be to attempt placing new drifts at every integer coordinate from 1 to 1000 in both x and y directions until the grid becomes connected. This is impractical because even for $n = 100$, the number of possible placements is on the order of $10^6$, and checking connectivity repeatedly is expensive.

The key insight comes from viewing the snow drifts as a graph: each drift is a node, and an edge exists between nodes if they share the same x or y coordinate. The problem then reduces to finding the number of connected components in this graph. Each connected component is already internally reachable. To connect $k$ components into a single connected network, we need exactly $k-1$ additional drifts, because each new drift can bridge two components. This is analogous to connecting separate islands in a network: to reduce $k$ islands to one, $k-1$ bridges are sufficient and necessary.

Once we understand this, the solution becomes straightforward: construct the graph, count connected components, and subtract one to get the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((1000*1000)^n) | O(1000*1000) | Too slow |
| Graph + DFS/BFS | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Represent each snow drift as a node in a graph. Two nodes are connected if their x or y coordinate matches. This models the sliding movement constraints exactly.
2. Initialize a visited array to keep track of which drifts have been explored.
3. Iterate through each drift. If a drift has not been visited, start a depth-first search (DFS) from that drift to mark all reachable drifts. Each DFS call identifies a single connected component.
4. Count the total number of connected components discovered in step 3.
5. The minimum number of additional drifts required is the number of connected components minus one. Each new drift can connect two components, so $k-1$ drifts connect $k$ components into one.

Why it works: DFS correctly discovers all drifts reachable from a given starting drift along valid moves. By definition, each DFS traversal marks exactly one connected component. Since each new drift can bridge exactly two components, connecting $k$ components requires $k-1$ additional drifts, guaranteeing minimality.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10000)

def main():
    n = int(input())
    drifts = [tuple(map(int, input().split())) for _ in range(n)]
    
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
                graph[i].append(j)
                graph[j].append(i)
    
    visited = [False] * n
    
    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
    
    components = 0
    for i in range(n):
        if not visited[i]:
            dfs(i)
            components += 1
    
    print(components - 1)

if __name__ == "__main__":
    main()
```

The adjacency list construction ensures each drift is connected to all others that share x or y, directly modeling legal moves. The DFS marks every drift reachable from a starting drift, guaranteeing that each component is counted once. `components - 1` gives the minimal number of additional drifts to connect all components. We increase the recursion limit to handle worst-case depth in DFS when all drifts form a single linear chain.

## Worked Examples

**Sample 1**

Input:

```
2
2 1
1 2
```

| Step | visited | components |
| --- | --- | --- |
| start | [False, False] | 0 |
| DFS from 0 | [True, False] | 1 |
| DFS from 1 | [True, True] | 2 |

Output: `2 - 1 = 1`

Explanation: Two isolated drifts require one new drift to connect.

**Custom Example**

Input:

```
4
1 1
1 2
3 4
4 4
```

| Step | visited | components |
| --- | --- | --- |
| start | [F,F,F,F] | 0 |
| DFS from 0 | [T,T,F,F] | 1 |
| DFS from 2 | [T,T,T,T] | 2 |

Output: `2 - 1 = 1`

Explanation: Two components [(1,1),(1,2)] and [(3,4),(4,4)] need one drift to connect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Constructing the adjacency list compares each pair of drifts once; DFS is O(n+n^2) = O(n^2). |
| Space | O(n^2) | Adjacency list stores edges for each pair of drifts sharing x or y. |

Given $n \le 100$, $n^2 = 10000$ operations is comfortably within a 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("2\n2 1\n1 2\n") == "1", "sample 1"

# Custom cases
assert run("1\n5 5\n") == "0", "single drift needs no connection"
assert run("3\n1 1\n1 2\n1 3\n") == "0", "all drifts in same column"
assert run("4\n1 1\n1 2\n3 4\n4 4\n") == "1", "two separate components"
assert run("5\n1 1\n2 1\n3 1\n1 2\n2 2\n") == "0", "all drifts connected via x or y"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 drift at (5,5) | 0 | Single node, no connection needed |
| 3 drifts same column | 0 | Connected by vertical moves |
| Two separate components | 1 | Correct counting of disconnected clusters |
| Complex connected cluster | 0 | DFS captures all reachable drifts |

## Edge Cases

For a single drift `(5,5)`, DFS visits that node and finds no neighbors. Components = 1, output = 0. For drifts aligned along one row or column, DFS correctly marks all nodes, so components = 1, output = 0. When multiple isolated clusters exist, DFS discovers each independently, ensuring `components - 1` counts the exact number of connecting drifts needed. For overlapping x or y coordinates, adjacency list construction guarantees every possible legal move is represented.
