---
title: "CF 103B - Cthulhu"
description: "We are given an undirected graph and need to decide whether it matches a very specific structure. The graph should contain exactly one simple cycle, and every other vertex must belong to a tree attached to some vertex on that cycle."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 103
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 80 (Div. 1 Only)"
rating: 1500
weight: 103
solve_time_s: 103
verified: true
draft: false
---

[CF 103B - Cthulhu](https://codeforces.com/problemset/problem/103/B)

**Rating:** 1500  
**Tags:** dfs and similar, dsu, graphs  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph and need to decide whether it matches a very specific structure.

The graph should contain exactly one simple cycle, and every other vertex must belong to a tree attached to some vertex on that cycle. Another way to describe it is that the graph is connected and has exactly one cycle.

The statement phrases this as several rooted trees whose roots lie on a simple cycle. Once the cycle is fixed, every extra edge branching away from it forms a tree attached to one of the cycle vertices.

The input describes an undirected graph with up to 100 vertices. Each edge connects two different vertices, and there are no duplicate edges or self-loops.

The constraints are small, so even an $O(n^2)$ or $O(n^3)$ solution would pass comfortably. Still, the graph structure gives a much cleaner characterization that leads to a simple linear solution.

The key observation is that a connected undirected graph contains exactly one cycle if and only if:

$$m = n$$

where $n$ is the number of vertices and $m$ is the number of edges.

A connected graph with $n$ vertices and $n-1$ edges is a tree. Adding one more edge creates exactly one cycle. That is precisely the structure required here.

Several edge cases can break careless implementations.

Consider a disconnected graph where one component is cyclic.

Input:

```
4 4
1 2
2 3
3 1
4 4
```

This example is actually invalid because self-loops are forbidden, but the important idea is a disconnected graph containing a cycle somewhere. A naive check of only `m == n` would incorrectly accept disconnected graphs.

A valid disconnected example is:

```
4 3
1 2
2 3
3 1
```

The correct output is:

```
NO
```

The graph has a cycle, but vertex 4 is isolated, so the graph is not connected.

Another tricky case is a connected graph with more than one cycle.

Input:

```
4 5
1 2
2 3
3 1
3 4
4 1
```

The correct output is:

```
NO
```

This graph is connected, but it contains two cycles. A DFS that only checks connectivity would fail here.

A third important case is a pure tree.

Input:

```
5 4
1 2
2 3
3 4
4 5
```

The correct output is:

```
NO
```

The graph is connected, but it has no cycle at all.

## Approaches

A brute-force approach would try to explicitly detect cycles and verify the structure after removing them. One possible method is to enumerate edges, temporarily remove each one, and check whether the graph becomes a tree. Since the constraints are tiny, this works.

For each edge, we could:

1. Remove the edge.
2. Run DFS or BFS to check connectivity.
3. Verify that the remaining graph is acyclic.

This costs roughly $O(m \cdot (n + m))$. With $n \le 100$, this is still fast enough.

The problem becomes much simpler once we remember a classical graph property.

For undirected graphs:

- A tree has exactly $n-1$ edges.
- Every extra edge introduces one additional cycle.

So a connected graph with exactly $n$ edges has exactly one cycle.

That matches the required "cycle with trees attached" structure perfectly. Every vertex not on the cycle must belong to a tree hanging from it, because a second cycle would require another extra edge.

This reduces the whole problem to two checks:

1. The graph must be connected.
2. The graph must satisfy $m = n$.

Connectivity is verified with a single DFS or BFS. The edge count is already given in the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m(n + m)) | O(n + m) | Accepted |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and build an adjacency list.

The adjacency list allows efficient DFS traversal in linear time.
2. Check whether the number of edges equals the number of vertices.

A connected undirected graph with exactly one cycle must satisfy $m = n$. If this condition fails, we can immediately print `"NO"`.
3. Run DFS from any vertex, for example vertex 1.

DFS marks every reachable vertex. Since the graph is undirected and connectedness matters globally, one traversal is enough.
4. Count how many vertices were visited.

If some vertices remain unvisited, the graph is disconnected and cannot match the required structure.
5. If both conditions hold, print `"FHTAGN!"`. Otherwise print `"NO"`.

### Why it works

The algorithm relies on a standard graph theorem.

A connected undirected graph with $n$ vertices and $n-1$ edges is a tree. Adding exactly one extra edge creates exactly one simple cycle.

So:

- If the graph is connected and $m = n$, it contains exactly one cycle.
- Every remaining edge belongs to trees attached to that cycle.
- This is exactly the definition required in the problem.

Conversely, every valid Cthulhu graph contains one cycle plus tree branches, so it must be connected and must contain exactly one more edge than a tree, meaning $m = n$.

The two conditions are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dfs(node, graph, visited):
    visited[node] = True

    for nei in graph[node]:
        if not visited[nei]:
            dfs(nei, graph, visited)

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    if m != n:
        print("NO")
        return

    visited = [False] * (n + 1)

    dfs(1, graph, visited)

    for node in range(1, n + 1):
        if not visited[node]:
            print("NO")
            return

    print("FHTAGN!")

solve()
```

The first part builds the adjacency list. Since the graph is undirected, every edge is inserted in both directions.

The condition `m != n` is checked before DFS because it immediately eliminates impossible cases. This avoids unnecessary traversal work.

The DFS marks all vertices reachable from vertex 1. If the graph is connected, every vertex must eventually become visited.

The loop over all vertices verifies connectivity explicitly. Missing this step is a common mistake because detecting a cycle alone is not enough.

The graph size is tiny, so recursion depth is completely safe here.

## Worked Examples

### Example 1

Input:

```
6 6
6 3
6 4
5 1
2 5
1 4
5 4
```

The graph has:

- $n = 6$
- $m = 6$

So the edge-count condition already matches.

DFS traversal:

| Step | Current Node | Newly Visited | Visited Set |
| --- | --- | --- | --- |
| 1 | 1 | 1 | {1} |
| 2 | 5 | 5 | {1,5} |
| 3 | 2 | 2 | {1,2,5} |
| 4 | 4 | 4 | {1,2,4,5} |
| 5 | 6 | 6 | {1,2,4,5,6} |
| 6 | 3 | 3 | {1,2,3,4,5,6} |

All vertices become reachable.

Output:

```
FHTAGN!
```

This trace demonstrates the central invariant: connectedness plus $m=n$ guarantees exactly one cycle.

### Example 2

Input:

```
5 4
1 2
2 3
3 4
4 5
```

Here:

- $n = 5$
- $m = 4$

The algorithm stops immediately because `m != n`.

| Variable | Value |
| --- | --- |
| n | 5 |
| m | 4 |
| Condition m == n | False |

Output:

```
NO
```

This example shows why a plain connectivity check is insufficient. The graph is connected, but it is only a tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS visits every vertex and edge once |
| Space | O(n + m) | Adjacency list and visited array |

With at most 100 vertices, this solution is far below the limits. Even much slower algorithms would pass, but the linear approach is both simpler and mathematically cleaner.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def dfs(node, graph, visited):
        visited[node] = True

        for nei in graph[node]:
            if not visited[nei]:
                dfs(nei, graph, visited)

    def solve():
        n, m = map(int, input().split())

        graph = [[] for _ in range(n + 1)]

        for _ in range(m):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)

        if m != n:
            return "NO"

        visited = [False] * (n + 1)

        dfs(1, graph, visited)

        for node in range(1, n + 1):
            if not visited[node]:
                return "NO"

        return "FHTAGN!"

    return solve()

# provided sample
assert run(
"""6 6
6 3
6 4
5 1
2 5
1 4
5 4
""") == "FHTAGN!", "sample 1"

# tree, connected but no cycle
assert run(
"""5 4
1 2
2 3
3 4
4 5
""") == "NO", "tree should fail"

# disconnected graph with one cycle
assert run(
"""4 3
1 2
2 3
3 1
""") == "NO", "disconnected graph should fail"

# connected graph with multiple cycles
assert run(
"""4 5
1 2
2 3
3 1
3 4
4 1
""") == "NO", "multiple cycles should fail"

# smallest valid cycle
assert run(
"""3 3
1 2
2 3
3 1
""") == "FHTAGN!", "simple cycle should pass"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Tree with 5 vertices | NO | Connected graphs without cycles fail |
| Disconnected triangle | NO | Connectivity is required |
| Two-cycle graph | NO | More than one cycle is invalid |
| Triangle | FHTAGN! | Smallest valid structure |

## Edge Cases

A disconnected graph with exactly one cycle can fool solutions that only check `m == n`.

Input:

```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
```

The graph has two disconnected components. DFS starting from vertex 1 only visits vertices `{1,2,3}`.

The visited check fails because vertices 4, 5, and 6 remain unvisited.

The algorithm correctly prints:

```
NO
```

A connected graph with multiple cycles can fool solutions that only check connectivity.

Input:

```
4 5
1 2
2 3
3 1
3 4
4 1
```

The graph is connected, but:

$$m = 5,\quad n = 4$$

Since `m != n`, the algorithm immediately rejects it.

The output is:

```
NO
```

A tree can fool solutions that only check connectivity.

Input:

```
4 3
1 2
2 3
3 4
```

DFS visits every node, so the graph is connected. But:

$$m = 3,\quad n = 4$$

The missing extra edge means there is no cycle.

The algorithm correctly outputs:

```
NO
```
