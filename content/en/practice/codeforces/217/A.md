---
title: "CF 217A - Ice Skating"
description: "We are given a set of snow drifts on a 2D grid. Bajtek can move from one snow drift to another by sliding along the rows or columns until he reaches another snow drift, moving strictly in the north, south, east, or west directions."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 217
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 134 (Div. 1)"
rating: 1200
weight: 217
solve_time_s: 75
verified: true
draft: false
---

[CF 217A - Ice Skating](https://codeforces.com/problemset/problem/217/A)

**Rating:** 1200  
**Tags:** brute force, dfs and similar, dsu, graphs  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of snow drifts on a 2D grid. Bajtek can move from one snow drift to another by sliding along the rows or columns until he reaches another snow drift, moving strictly in the north, south, east, or west directions. The goal is to determine the minimal number of additional snow drifts we must place so that it is possible to travel between any two snow drifts using this sliding rule.

Each snow drift is defined by integer coordinates, and there are up to 100 of them. Since `n` is small, we can afford algorithms that are quadratic in `n` or involve exploring connectivity explicitly. The maximum coordinates are 1000, which means storing a full 2D grid of presence flags is not practical, but we do not need to, since the problem can be treated as a graph problem where nodes are snow drifts and edges exist if two drifts share either `x` or `y`.

A key edge case arises when all snow drifts are aligned along a single row or a single column. In that case, the snow drifts are already connected, so no additional snow drifts are needed. Another subtle scenario is when no two drifts share an `x` or `y` coordinate, for instance:

```
3
1 1
2 2
3 3
```

Here, every drift is isolated, so connecting them requires additional drifts to form bridges along rows or columns.

## Approaches

A brute-force approach would attempt to simulate all possible placements of new snow drifts and test connectivity, but this quickly becomes infeasible. With 100 drifts and 1000 possible positions in each dimension, the combinatorial explosion makes this approach impossible.

The key insight is to model the drifts as nodes in a graph where edges exist if two drifts share an `x` or `y` coordinate. In this graph, connected components correspond to groups of snow drifts that are reachable from one another. Each additional snow drift can reduce the number of disconnected components by at most one because it can connect two previously disconnected components. Therefore, the minimal number of new drifts required is equal to the number of connected components minus one.

We can find the connected components efficiently using depth-first search (DFS). Construct a list of adjacency relations by checking pairs of drifts sharing an `x` or `y` coordinate, then traverse the graph with DFS to count components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n^2)) | O(n^2) | Too slow |
| DFS on drift graph | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input to get the list of snow drifts as `(x, y)` pairs. Each drift becomes a node in our graph.
2. Build a graph where each drift is connected to every other drift that shares either its `x` or `y` coordinate. This ensures edges represent legal sliding moves.
3. Initialize a `visited` array to track which drifts have been explored.
4. For each drift, if it is not yet visited, start a DFS from that drift. Mark all reachable drifts as visited.
5. Each time a new DFS starts, increment a `component_count` variable. This counts how many disconnected groups exist.
6. The answer is `component_count - 1`, because each additional snow drift can connect two components, so connecting all components requires one fewer drift than the number of components.

Why it works: DFS correctly identifies all nodes reachable from any starting drift via valid moves, which corresponds exactly to the connected components in our drift graph. The subtraction by one is valid because one snow drift can connect two separate components into one, so connecting `k` components requires `k-1` connections.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    drifts = [tuple(map(int, input().split())) for _ in range(n)]
    
    adj = [[] for _ in range(n)]
    
    # Build graph: connect drifts sharing x or y
    for i in range(n):
        for j in range(i + 1, n):
            if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
                adj[i].append(j)
                adj[j].append(i)
    
    visited = [False] * n
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
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

The code reads the drifts, builds a graph where edges correspond to reachable moves along rows or columns, and uses DFS to count connected components. The subtle parts are ensuring that edges are bidirectional and that each drift is checked exactly once in the DFS to avoid double-counting components.

## Worked Examples

### Example 1

Input:

```
2
2 1
1 2
```

| Step | visited | DFS stack | components |
| --- | --- | --- | --- |
| Start | [F, F] | [] | 0 |
| DFS 0 | [T, F] | 0 | 1 |
| DFS 0 neighbors | [T, T] | 1 | 1 |

Output: `1`

Adding one drift connecting the two components makes them reachable.

### Example 2

Input:

```
4
1 1
1 2
3 1
4 5
```

| Step | visited | DFS stack | components |
| --- | --- | --- | --- |
| Start | [F,F,F,F] | [] | 0 |
| DFS 0 | [T,T,F,F] | 0 | 1 |
| DFS 2 | [T,T,T,F] | 2 | 2 |
| DFS 3 | [T,T,T,T] | 3 | 3 |

Output: `2`

Two additional drifts are needed to connect the three components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Building adjacency requires checking all pairs of drifts. DFS traversal is O(n) since each edge is traversed at most twice. |
| Space | O(n^2) | Storing adjacency lists for up to n^2 edges. |

With n ≤ 100, n^2 ≤ 10,000, which fits comfortably in the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided sample
assert run("2\n2 1\n1 2\n") == "1", "sample 1"

# Single drift, no extra needed
assert run("1\n10 10\n") == "0", "single drift"

# All drifts in same row
assert run("3\n1 1\n2 1\n3 1\n") == "0", "same row"

# All drifts in same column
assert run("3\n2 1\n2 2\n2 3\n") == "0", "same column"

# Isolated drifts, diagonal
assert run("3\n1 1\n2 2\n3 3\n") == "2", "isolated diagonal"

# Multiple components
assert run("4\n1 1\n1 2\n3 1\n4 5\n") == "2", "three components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 drift | 0 | Minimal input, no new drifts |
| 3 drifts same row | 0 | Already connected horizontally |
| 3 drifts same column | 0 | Already connected vertically |
| 3 diagonal drifts | 2 | Isolated, need two new drifts |
| 4 mixed drifts | 2 | Multiple connected components, general case |

## Edge Cases

A single snow drift is trivially connected, so output is `0`. When all drifts align along a single row or column, the DFS will visit all drifts starting from any node, so `components` will be `1`, and output `0`. For disjoint diagonal drifts, DFS discovers each component separately, correctly counting `n` components for `n` isolated drifts, and the output formula subtracts one to give the minimal number of connecting drifts.
