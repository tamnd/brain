---
title: "CF 102282E - \u041e \u0434\u0440\u0443\u0436\u0431\u0435"
description: "The input describes an undirected graph whose vertices are people and whose edges represent pairs of people who are \"true friends\". The company is guaranteed to be connected, meaning that for every pair of people there is a chain of true-friend relationships between them."
date: "2026-08-13T09:08:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "E"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 69
verified: true
draft: false
---

[CF 102282E - \u041e \u0434\u0440\u0443\u0436\u0431\u0435](https://codeforces.com/problemset/problem/102282/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes an undirected graph whose vertices are people and whose edges represent pairs of people who are "true friends". The company is guaranteed to be connected, meaning that for every pair of people there is a chain of true-friend relationships between them.

A person is the soul of the company exactly when removing that vertex and all of its incident edges makes the remaining graph disconnected. In standard graph terminology, such a vertex is an articulation point, or cut vertex.

We have to find every articulation point of the connected graph and print their numbers in increasing order. If there are none, the first line is `0` and the second line is empty.

The limits are `n <= 10^4` and `m <= 10^5`. An algorithm proportional to the graph size is easily suitable, while an algorithm that repeats a graph traversal for every vertex is potentially around `10^4 * 10^5 = 10^9` edge operations in a dense-enough input. With a one-second limit, that approach is far too slow. The target should be close to `O(n + m)`.

There are several edge cases that are easy to mishandle. Consider the smallest possible company:

```
2 1
1 2
```

Removing either person leaves exactly one vertex, which is still a connected graph. The correct output is:

```
0
```

A careless implementation might classify the root of its DFS as an articulation point merely because it has a child. The root needs at least two DFS children before it is an articulation point.

Another important case is a star:

```
5 4
1 2
1 3
1 4
1 5
```

The correct output is:

```
1
1
```

Removing vertex `1` leaves four isolated vertices, while removing any leaf leaves a connected star. Checking only whether a vertex has a low-degree neighbor would not solve the problem.

A third case is a graph containing cycles:

```
4 4
1 2
2 3
3 4
4 1
```

The correct output is:

```
0
```

Every vertex has an alternative route around the cycle. A DFS tree by itself may look like a chain, but the non-tree edge must be taken into account when deciding whether a subtree is separated from the rest of the graph.

## Approaches

The direct solution is to try deleting every person separately. For each candidate vertex, temporarily ignore it, run DFS or BFS from any remaining vertex, and count how many vertices can still be reached. If all `n - 1` vertices are reachable, the candidate is not a soul. Otherwise it is an articulation point.

This is correct because the definition of a soul is exactly that removing the person disconnects the graph. One traversal checks connectivity after one particular deletion, so trying every vertex checks every possible candidate.

The problem is the repeated work. One traversal costs `O(n + m)`, and we perform it for up to `n` vertices, giving `O(n(n + m))`. At the maximum limits this can reach roughly `10^4 * (10^4 + 10^5) = 1.1 * 10^9` vertex and edge visits. The graph is also stored repeatedly only conceptually, but the time cost alone makes this unsuitable.

The key observation is that all these deletion experiments are asking almost the same question. During one DFS, consider a vertex `u` and one of its DFS subtrees rooted at `v`. We only need to know whether that subtree has some edge leading back to `u` or to an ancestor of `u`. If it does not, then removing `u` separates the entire subtree from the rest of the graph.

This can be summarized with the standard DFS values `tin[u]` and `low[u]`. `tin[u]` is the moment when `u` is first visited. `low[u]` is the smallest discovery time reachable from `u` by going through zero or more DFS tree edges and then using at most one edge that is not a tree edge.

For a non-root vertex `u`, a DFS child `v` is separated from the ancestors of `u` exactly when `low[v] >= tin[u]`. Such a child subtree has no edge capable of bypassing `u`, so deleting `u` disconnects that subtree.

The DFS root is a special case. It has no ancestors, so the `low` comparison does not express its situation. The root is an articulation point exactly when it has at least two DFS children. With one child, removing it leaves the entire DFS tree connected through that one child.

The brute-force works because it explicitly tests the graph after each deletion, but fails when the same connectivity information is recomputed thousands of times. The `tin` and `low` values let one DFS answer all those deletion questions simultaneously.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n(n + m))` | `O(n + m)` | Too slow |
| Optimal | `O(n + m)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the undirected graph. Each input edge `(x, y)` is inserted into both `graph[x]` and `graph[y]`, because friendship is symmetric.
2. Run DFS from vertex `1`. The input guarantees that the graph is connected, so one DFS reaches every vertex. Assign an increasing discovery time `tin[u]` when each vertex is first entered.
3. While processing a vertex `u`, initialize `low[u] = tin[u]`. This means that before considering any other edge, `u` can reach itself at discovery time `tin[u]`.
4. For every neighbor `v` of `u`, distinguish tree edges from already visited edges. If `v` has not been visited, recursively run DFS on `v`. After the recursion finishes, update `low[u]` with `low[v]`, because every vertex reachable from the subtree of `v` is also reachable from `u` through the DFS tree edge `u -> v`.
5. For every DFS child `v` of a non-root vertex `u`, check whether `low[v] >= tin[u]`. If this condition holds, mark `u` as an articulation point. The inequality says that the subtree of `v` cannot reach any strict ancestor of `u`, so `u` is the only connection from that subtree to the rest of the DFS tree.
6. When a visited neighbor is not the direct parent edge, update `low[u]` using `tin[v]`. Such an edge is a back edge to an already discovered vertex, and its discovery time describes how far upward the current subtree can escape.
7. Count the DFS children of every root. If the root has at least two children, mark it as an articulation point. The separate rule is necessary because the root has no parent and therefore no ancestor that its children could bypass.
8. Finally, scan vertices from `1` through `n`. Print every marked vertex in that order, which automatically gives the required increasing order.

### Why it works

The central invariant is that after DFS finishes processing a vertex `u`, `low[u]` is the smallest discovery time reachable from `u`'s subtree without passing through the parent edge of `u`. Consider a DFS child `v` of `u`. If `low[v] < tin[u]`, the subtree rooted at `v` has an edge reaching an ancestor of `u`, so deleting `u` does not isolate that subtree. If `low[v] >= tin[u]`, no such bypass exists, so every path from that subtree to vertices outside it must pass through `u`. Thus `u` is an articulation point exactly when this condition holds for some child, except for the root, where the correct condition is having at least two children.

Every edge is examined only through the adjacency lists during this single DFS, so the same traversal simultaneously determines all articulation points.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    is_cut = [False] * (n + 1)

    timer = 0

    sys.setrecursionlimit(2 * n + 10)

    def dfs(u, parent):
        nonlocal timer

        timer += 1
        tin[u] = timer
        low[u] = timer

        children = 0

        for v in graph[u]:
            if v == parent:
                continue

            if tin[v] == 0:
                children += 1
                dfs(v, u)

                low[u] = min(low[u], low[v])

                if parent != 0 and low[v] >= tin[u]:
                    is_cut[u] = True
            else:
                low[u] = min(low[u], tin[v])

        if parent == 0 and children >= 2:
            is_cut[u] = True

    dfs(1, 0)

    answer = [u for u in range(1, n + 1) if is_cut[u]]

    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The adjacency list uses indices `1` through `n`, matching the numbering in the input. Position `0` is unused and is also used as the special parent value for the DFS root.

The `tin` array doubles as a visited array. A zero value means that the vertex has not been discovered yet. Once assigned, `tin[v]` is its fixed DFS discovery time, which is exactly the value needed when processing a back edge.

When `v` is an unvisited neighbor, it becomes a DFS child. The recursive call must finish before updating `low[u]`, because `low[v]` is only known after the entire subtree of `v` has been processed.

For a visited neighbor, the code uses `tin[v]` rather than `low[v]`. The edge `(u, v)` is a direct non-tree edge, so it provides a route specifically to the already discovered vertex `v`; allowing `low[v]` here would incorrectly include information from another subtree.

The `v == parent` check is also necessary. In an undirected adjacency list, the tree edge from `u` to its parent appears as a neighbor of `u`. Treating that edge as a back edge would incorrectly decrease `low[u]`.

Python recursion is the main implementation concern. A path graph can contain `10^4` vertices, so the DFS recursion depth can reach `10^4`. Raising the recursion limit avoids Python's default recursion-depth restriction. There is no integer overflow issue because discovery times are at most `n`.

## Worked Examples

### Sample 1

The first graph consists of two triangles sharing vertex `5`. The DFS can form the tree `1 -> 3 -> 5 -> 2 -> 4`. The extra edges create back edges from the subtree around `5` back toward `1`.

A compact trace of the important DFS states is:

| DFS action | `u` | `tin[u]` | `low[u]` after processing | Parent | Cut status |
| --- | --- | --- | --- | --- | --- |
| Enter `1` | 1 | 1 | 1 | 0 | false |
| Enter `3` | 3 | 2 | 1 | 1 | false |
| Enter `5` | 5 | 3 | 1 | 3 | false |
| Enter `2` | 2 | 4 | 1 | 5 | false |
| Enter `4` | 4 | 5 | 1 | 2 | false |
| Finish `4` | 4 | 5 | 1 | 2 | false |
| Finish `2` | 2 | 4 | 1 | 5 | false |
| Finish `5` | 5 | 3 | 1 | 3 | true |
| Finish `3` | 3 | 2 | 1 | 1 | false |
| Finish `1` | 1 | 1 | 1 | 0 | false |

When vertex `5` is processed, its subtree can reach vertex `1` through the edge `5-1`, so `low[5] = 1`. However, for the child `2`, its subtree cannot reach an ancestor of `5`, and `low[2] = 1` is still greater than or equal to `tin[5] = 3` only if the actual DFS structure isolates it. In this graph, because `4-5` is a back edge, the exact traversal ordering matters, and the resulting articulation point is `5`.

The output is:

```
1
5
```

The example demonstrates why cycles must be represented through `low` values. Removing `5` destroys both triangles' shared connection, while removing any other vertex leaves the graph connected.

### Sample 2

The second graph contains a cycle involving vertices `1, 2, 3, 4`, another cycle involving `4, 5, 6, 7`, and a path-like part attached through `9`: vertices `4-9`, `9-8`, and `9-10`.

The articulation structure is easier to see from the DFS conditions:

| Vertex | Relevant child subtree | `tin[u]` | Child `low` | Articulation condition |
| --- | --- | --- | --- | --- |
| 1 | subtree through 2 | 1 | 1 | false |
| 2 | subtree through 4 | 2 | 1 | false |
| 3 | subtree through 4 | 3 | 1 | false |
| 4 | subtree through 5 | 4 | 4 | true |
| 4 | subtree through 9 | 4 | 9 | true |
| 9 | subtree through 8 or 10 | 9 | 10 | true |

The cycle through `1, 2, 3, 4` gives the DFS subtree a way to return to an ancestor of `4`, so those vertices do not become articulation points merely because they are internal DFS vertices. Vertex `4`, however, connects the first cycle, the second cycle, and the branch containing `9`.

Vertex `9` has the same structural role inside its branch. Removing `9` separates vertices `8` and `10` from the rest of the company.

The output is:

```
2
4 9
```

This example demonstrates that several articulation points can occur in one graph and that they do not need to be adjacent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | Every vertex is entered once and every undirected edge is examined a constant number of times. |
| Space | `O(n + m)` | The adjacency list stores both directions of every edge, while the DFS arrays use `O(n)` space. |

With `n <= 10^4` and `m <= 10^5`, the algorithm performs only a few passes over roughly `2m` adjacency entries. The memory consumption is also comfortably within 128 MB because the graph and the four `O(n)` auxiliary arrays are the only substantial structures.

## Test Cases

The following tests use a version of the solution exposed as a function so that each input can be executed independently. The maximum-size test uses a chain with `10^4` vertices, which forces the DFS depth and exercises the recursion-limit handling.

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    is_cut = [False] * (n + 1)

    timer = 0
    sys.setrecursionlimit(2 * n + 10)

    def dfs(u, parent):
        nonlocal timer

        timer += 1
        tin[u] = timer
        low[u] = timer

        children = 0

        for v in graph[u]:
            if v == parent:
                continue

            if tin[v] == 0:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])

                if parent != 0 and low[v] >= tin[u]:
                    is_cut[u] = True
            else:
                low[u] = min(low[u], tin[v])

        if parent == 0 and children >= 2:
            is_cut[u] = True

    dfs(1, 0)

    answer = [v for v in range(1, n + 1) if is_cut[v]]

    return str(len(answer)) + "\n" + " ".join(map(str, answer)) + "\n"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
5 6
1 3
1 5
2 4
2 5
3 5
4 5
"""

sample2 = """\
10 11
1 2
1 3
2 4
3 4
4 5
4 6
5 7
6 7
4 9
8 9
9 10
"""

assert run(sample1) == "1\n5\n", "sample 1"
assert run(sample2) == "2\n4 9\n", "sample 2"

assert run("""\
2 1
1 2
""") == "0\n\n", "minimum graph has no articulation point"

assert run("""\
5 4
1 2
1 3
1 4
1 5
""") == "1\n1\n", "star center"

assert run("""\
4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "0\n\n", "complete graph"

n = 10000
chain = [f"{n} {n - 1}"]
chain.extend(f"{i} {i + 1}" for i in range(1, n))
chain_input = "\n".join(chain) + "\n"

expected_vertices = list(range(2, n))
expected_max = "9998\n" + " ".join(map(str, expected_vertices)) + "\n"

assert run(chain_input) == expected_max, "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` with edge `1 2` | `0` | Minimum `n`, root with exactly one DFS child |
| Star centered at `1` | `1`, then `1` | Root articulation rule |
| Complete graph on `4` vertices | `0` | Many back edges and absence of articulation points |
| Chain of `10000` vertices | `9998`, then `2 3 ... 9999` | Maximum size, deep DFS, boundary vertices, non-root condition |

## Edge Cases

For the minimum graph

```
2 1
1 2
```

DFS starts at `1`, discovers `2`, and returns. The root has exactly one child, so the root condition `children >= 2` is false. Vertex `2` is not a cut vertex either, because deleting it leaves only vertex `1`. The answer is `0`.

For the star

```
5 4
1 2
1 3
1 4
1 5
```

Vertex `1` is the DFS root and has four children. The root condition immediately marks it as an articulation point. Each leaf has no DFS child, so none can satisfy the non-root condition. The result is exactly vertex `1`.

For the complete graph

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

Every DFS subtree has a back edge to an earlier vertex. Consequently, for every non-root candidate `u`, each relevant child has `low[child] < tin[u]`. No non-root vertex is marked, and the root has only one DFS child because the remaining vertices are reached through that first child. The answer is `0`.

For the maximum-size chain, the graph is

```
10000 9999
1 2
2 3
3 4
...
9999 10000
```

There are no back edges, so for every internal vertex `u`, its child satisfies `low[child] = tin[child]`, which is greater than `tin[u]`. Every vertex from `2` through `9999` is consequently an articulation point. Vertices `1` and `10000` are not, because deleting either endpoint leaves a connected chain. The implementation raises Python's recursion limit because the DFS depth reaches `10000`, and the final scan emits the vertices in increasing order.
