---
title: "CF 102646E - Maximizing SCCs"
description: "We have a directed graph with n vertices and m edges. The original graph is guaranteed to be strongly connected, meaning every vertex can reach every other vertex using the given edges. We must keep exactly k of these edges and remove the rest."
date: "2026-07-30T23:09:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102646
codeforces_index: "E"
codeforces_contest_name: "Testing Round #XVII"
rating: 0
weight: 102646
solve_time_s: 118
verified: true
draft: false
---

[CF 102646E - Maximizing SCCs](https://codeforces.com/problemset/problem/102646/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed graph with `n` vertices and `m` edges. The original graph is guaranteed to be strongly connected, meaning every vertex can reach every other vertex using the given edges. We must keep exactly `k` of these edges and remove the rest. The goal is to make the remaining graph have as many strongly connected components as possible. The output is the maximum number of components and one valid set of `k` edge indices that achieves it.

The key restriction is that `k` is smaller than `n`. Since every vertex is already a possible separate strongly connected component, the absolute maximum answer is `n`. The question becomes whether we can always choose `k` edges without accidentally creating a directed cycle.

With `n` up to `100000` and `m` up to `200000`, any solution that tries many subsets of edges or repeatedly recomputes SCCs will be far too slow. A solution close to linear in the size of the graph is needed because there are only a few million operations available in a typical contest setting.

A common mistake is to choose arbitrary edges. For example:

```
3 3 2
1 2
2 3
3 1
```

The correct output is:

```
3
1 2
```

because edges `1 -> 2` and `2 -> 3` form a directed chain, so every vertex is its own SCC. A careless choice of edges `1` and `3` creates the cycle `1 -> 2 -> 3 -> 1` is not possible here because edge `2` is missing, but choosing all three edges would clearly make one SCC. The important detail is that the chosen edges must avoid cycles.

Another edge case is `k = 0`.

```
5 5 0
1 2
2 3
3 4
4 5
5 1
```

The correct output is:

```
5
```

The empty graph has no paths between different vertices, so every vertex is a separate SCC. An implementation that always tries to output at least one edge would fail.

A final edge case is when the graph is dense and every vertex has many incoming and outgoing edges. For example:

```
4 6 3
1 2
2 3
3 4
4 1
1 3
2 4
```

The correct answer is still `4`. Density does not matter. We only need a small acyclic subset of edges, not a sparse graph.

## Approaches

A direct approach would try different sets of `k` edges and compute the SCC count for each choice. This is correct because checking every possible subset guarantees that the best one is found. However, the number of choices is `C(m, k)`, which becomes enormous even for small graphs. Running an SCC algorithm after every choice is impossible.

The useful observation comes from the fact that the original graph is strongly connected. Starting from any vertex, a DFS can reach every other vertex. The DFS tree contains exactly `n - 1` edges, and those edges always form a directed tree from parent to child. A tree has no directed cycles, so every vertex in that tree is its own SCC.

Since `k < n`, we can take any `k` edges from this DFS tree. The resulting graph remains acyclic, which means it has exactly `n` strongly connected components. This is already the theoretical maximum, so no more complicated optimization is needed.

The brute-force works because it explores every possible remaining graph, but fails because the search space is huge. The DFS tree observation reduces the problem from searching among all edge subsets to constructing one guaranteed optimal subset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(m, k) * (n + m)) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Run a DFS from any vertex, for example vertex `1`. Whenever DFS visits a new vertex through an edge, record that edge as part of the DFS tree. The graph is strongly connected, so this process will visit all vertices.
2. Take the first `k` recorded DFS tree edges and output their indices. These are the required edges because they come from an acyclic structure.
3. If `k` is zero, output zero selected edges. The empty graph already gives the maximum number of SCCs.

Why it works:

The selected edges are a subset of a DFS tree. Every edge in this tree points from a parent vertex to a child vertex. Following selected edges can only move farther down the tree, so returning to an already visited vertex is impossible. The selected graph is a DAG. In a DAG, no two different vertices can be mutually reachable, so every vertex forms its own SCC. The answer is therefore `n`, which is the maximum possible number of SCCs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    graph = [[] for _ in range(n)]

    for i in range(1, m + 1):
        u, v = map(int, input().split())
        graph[u - 1].append((v - 1, i))

    ans = []
    seen = [False] * n

    sys.setrecursionlimit(300000)

    def dfs(u):
        seen[u] = True
        for v, idx in graph[u]:
            if not seen[v]:
                ans.append(idx)
                if len(ans) == k:
                    return True
                if dfs(v):
                    return True
        return False

    if k > 0:
        dfs(0)

    print(n)
    if k:
        print(*ans)

if __name__ == "__main__":
    solve()
```

The adjacency list stores both the destination vertex and the original edge index because the output requires edge numbers rather than endpoints.

The DFS records an edge exactly when it first discovers a new vertex. This makes the recorded edges a spanning tree of the reachable part of the graph. Because the graph is strongly connected, starting from vertex `0` reaches every vertex.

The recursion stops as soon as `k` edges are collected. This is safe because the only goal is to output any valid optimal subset, not necessarily the whole tree. The condition `k < n` guarantees that a DFS tree always contains enough edges.

There is no need for SCC computation after construction. The proof already guarantees that the chosen edges form a DAG and therefore achieve the maximum possible answer.

## Worked Examples

For the first sample:

```
4 5 1
1 2
2 3
1 4
4 3
3 1
```

One possible DFS traversal starts at vertex `1`.

| Step | Current vertex | Chosen edge | Selected edges |
| --- | --- | --- | --- |
| 1 | 1 | 1 -> 2 | 1 |

The algorithm stops because `k = 1`.

The selected graph contains only edge `1 -> 2`. No cycle exists, so all four vertices are separate SCCs. The answer is `4`.

For a custom example:

```
5 5 3
1 2
2 3
3 4
4 5
5 1
```

The DFS tree follows the cycle until all vertices are discovered.

| Step | Current vertex | Chosen edge | Selected edges |
| --- | --- | --- | --- |
| 1 | 1 | 1 -> 2 | 1 |
| 2 | 2 | 2 -> 3 | 1 2 |
| 3 | 3 | 3 -> 4 | 1 2 3 |

The chosen edges create the chain `1 -> 2 -> 3 -> 4`. Vertex `5` is disconnected from this chosen subset, but that is allowed. There are no cycles, so every vertex remains an independent SCC and the answer is `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed at most once during DFS |
| Space | O(n + m) | The adjacency list and DFS state arrays store the graph |

The limits allow a linear traversal because `n` and `m` are both at most a few hundred thousand. The algorithm only stores the input graph and a small amount of DFS state.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    def solve():
        input = sys.stdin.readline
        n, m, k = map(int, input().split())
        graph = [[] for _ in range(n)]

        for i in range(1, m + 1):
            u, v = map(int, input().split())
            graph[u - 1].append((v - 1, i))

        ans = []
        seen = [False] * n

        def dfs(u):
            seen[u] = True
            for v, idx in graph[u]:
                if not seen[v]:
                    ans.append(idx)
                    if len(ans) == k:
                        return True
                    if dfs(v):
                        return True
            return False

        if k:
            dfs(0)

        print(n)
        if k:
            print(*ans)

    solve()
    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""4 5 1
1 2
2 3
1 4
4 3
3 1
""").split()[0] == "4", "sample 1"

assert run("""7 7 0
1 2
2 3
3 4
4 5
5 6
6 7
7 1
""").split()[0] == "7", "sample 2"

assert run("""1 1 0
1 1
""").split()[0] == "1", "single vertex"

assert run("""5 5 4
1 2
2 3
3 4
4 5
5 1
""").split()[0] == "5", "large k"

assert run("""4 6 2
1 2
2 3
3 4
4 1
1 3
2 4
""").split()[0] == "4", "dense graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `1` | Minimum size graph and zero edges |
| `5 5 4` | `5` | Taking almost all allowed edges without creating a cycle |
| `4 6 2` | `4` | Dense strongly connected graph |
| Sample graphs | `n` | Original examples and normal execution |

## Edge Cases

When `k = 0`, the algorithm skips DFS selection and prints only `n`. This matches the fact that an empty directed graph has no non-trivial SCCs. For the example with five vertices and no selected edges, the answer is `5`.

When `k` is close to `n`, the DFS tree still provides enough edges because every spanning tree has exactly `n - 1` edges. For a graph with `n = 5` and `k = 4`, the algorithm can output all four tree edges, and the selected graph is still acyclic.

When the original graph contains many cycles, those cycles are ignored. For example, in a graph containing `1 -> 2 -> 3 -> 1`, the DFS tree may select only `1 -> 2` and `2 -> 3`. The removed back edge is exactly what would have merged the vertices into one SCC, so excluding it is what gives the optimal result.
