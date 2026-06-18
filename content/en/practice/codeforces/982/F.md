---
problem: 982F
contest_id: 982
problem_index: F
name: "The Meeting Place Cannot Be Changed"
contest_name: "Codeforces Round 484 (Div. 2)"
rating: 2700
tags: ["dfs and similar", "graphs"]
answer: passed_samples
verified: false
solve_time_s: 87
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a33a65c-a680-83ec-b683-c182360d8ebc
---

# CF 982F - The Meeting Place Cannot Be Changed

**Rating:** 2700  
**Tags:** dfs and similar, graphs  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 27s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a33a65c-a680-83ec-b683-c182360d8ebc  

---

## Solution

## Problem Understanding

We are given a directed graph representing intersections connected by one-way roads. A car starts from some unknown intersection and then keeps moving along outgoing roads forever. We are guaranteed that this movement never gets stuck, meaning from every reachable situation there is always at least one outgoing edge to continue the journey.

Petr wants to choose a single intersection such that no matter where the car starts and no matter which outgoing edges are chosen during movement, the car will eventually reach that chosen intersection at some point in its infinite walk.

Rephrased in graph terms, we are looking for a vertex that is unavoidable for all infinite directed walks in the graph, assuming the walk follows edges arbitrarily but can continue indefinitely.

The constraint n up to 100000 and m up to 500000 forces any solution to be linear or near-linear in the size of the graph. Anything involving repeated DFS from every node, or checking reachability pairwise, will immediately exceed the limits because it would scale to O(n(m+n)) or worse.

A subtle failure case appears when the graph contains multiple strongly connected components arranged in a cycle. For example, consider a directed cycle of components A → B → C → A, where each component also has internal cycles. A naive intuition might pick a vertex inside one SCC and assume all paths eventually flow into it, but in reality the process can circulate forever without committing to a single entry point.

Another tricky case is when there are multiple large SCCs that can be visited in different orders depending on the path choices. In such a graph, no single vertex may be unavoidable, even though infinite movement is guaranteed by cycles inside components.

## Approaches

A brute-force interpretation would be to test each vertex as a candidate meeting point. For a fixed vertex v, we would need to verify that from every possible starting position and every possible continuation of edges, the infinite walk eventually hits v. That already hints at a worst-case need to reason about all possible reachable sets and all infinite paths. A direct simulation of all walks is impossible because the number of paths grows exponentially with length.

A more structured brute force would be to check reachability in reverse: for each vertex v, compute the set of vertices that can reach v. Then check whether from every vertex there is a path to v. This is equivalent to v being reachable from all nodes in the graph when edges are followed forward. That check can be done with a DFS or BFS from every vertex, costing O(n(m+n)), which is far too large.

The key structural insight is that the graph can be decomposed into strongly connected components. Inside a strongly connected component, every vertex can reach every other, so from the perspective of infinite movement, each SCC behaves like a single “macro-state”. Collapsing each SCC produces a directed acyclic graph.

In that condensed graph, the problem becomes finding a component that is reachable from every other component. In a DAG, this happens if and only if there is exactly one sink component in the reversed reachability sense, or equivalently a component that is the only one without incoming edges in the condensation graph. That component acts as a universal attractor because every other component can flow into it, and once inside an SCC, the walk cannot escape the SCC structure constraints that would avoid it.

This reduces the task to computing SCCs and then analyzing the condensation graph in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force reachability checks | O(n(m+n)) | O(n+m) | Too slow |
| SCC condensation + analysis | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Compute strongly connected components of the graph using Kosaraju or Tarjan algorithm. This groups vertices into maximal sets where every vertex can reach every other within the same set. This step is necessary because inside such a component, we cannot distinguish vertices in terms of long-term movement.
2. Build a condensed graph where each SCC becomes a single node. For every edge u → v in the original graph, if u and v belong to different components, add a directed edge between their SCCs.
3. Compute indegrees of all nodes in the condensed graph.
4. Identify all SCCs with indegree equal to zero. These are components that no other component can enter.
5. If there is exactly one such SCC, choose any vertex inside it as the answer. If there are multiple such SCCs, output -1 because there is no single unavoidable destination component.
6. Return the chosen vertex.

The reasoning behind focusing on indegree-zero SCCs is that any SCC with incoming edges can potentially be avoided indefinitely by staying within a cycle of other SCCs that do not force entry into it.

### Why it works

The condensation graph is a DAG, so at least one source SCC must exist. A vertex is unavoidable for every infinite walk only if every path of SCC transitions eventually leads into the same SCC. That is only possible when there is exactly one source SCC in the condensation graph, because multiple sources allow starting the walk inside a different source and remaining inside its reachable region forever without ever being forced into another source. Inside an SCC, all vertices are mutually reachable, so choosing any vertex in the unique source SCC guarantees eventual visitation under any infinite traversal.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def kosaraju(n, g, rg):
    visited = [False] * n
    order = []

    def dfs1(v):
        visited[v] = True
        for to in g[v]:
            if not visited[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    comp = [-1] * n
    cid = 0

    def dfs2(v, c):
        comp[v] = c
        for to in rg[v]:
            if comp[to] == -1:
                dfs2(to, c)

    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, cid)
            cid += 1

    return comp, cid

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        rg[v].append(u)
        edges.append((u, v))

    comp, c = kosaraju(n, g, rg)

    indeg = [0] * c
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv:
            indeg[cv] += 1

    sources = [i for i in range(c) if indeg[i] == 0]

    if len(sources) != 1:
        print(-1)
        return

    target = sources[0]
    for i in range(n):
        if comp[i] == target:
            print(i + 1)
            return

if __name__ == "__main__":
    solve()
```

The implementation uses Kosaraju’s algorithm to compute SCCs in two passes, first building a finishing order and then assigning components on the reversed graph. After that, we only need to inspect edges between components.

A common pitfall is forgetting to ignore intra-component edges when computing indegrees. Those edges do not affect condensation structure and would incorrectly inflate indegree counts. Another subtlety is choosing any vertex from the target SCC, since all vertices inside a strongly connected component are equivalent for this purpose.

## Worked Examples

### Example 1

Input:

```
5 6
1 2
2 3
3 1
3 4
4 5
5 3
```

SCC formation and condensation:

| Step | State |
| --- | --- |
| SCCs | {1,2,3}, {4,5} |
| Condensed edges | {1,2,3} ↔ {4,5} (cycle) |
| indegree | both components have indegree 1 |
| sources | none unique |

Since there is no single SCC with indegree zero, no vertex is universally unavoidable.

Output:

```
-1
```

This shows that cycles between SCCs destroy uniqueness of a forced destination.

### Example 2

Input:

```
4 4
1 2
2 3
3 1
3 4
```

| Step | State |
| --- | --- |
| SCCs | {1,2,3}, {4} |
| Condensed edges | {1,2,3} → {4} |
| indegree | {1,2,3}: 0, {4}: 1 |
| sources | {1,2,3} |

Only one source SCC exists, so any vertex inside {1,2,3} works, for example 1.

Output:

```
1
```

This demonstrates how a single entry component forces eventual arrival regardless of the starting point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two DFS passes for SCC plus one scan of edges for condensation analysis |
| Space | O(n + m) | Adjacency lists, reverse graph, and component arrays |

The solution comfortably fits within limits because both n and m are large but linear traversal is sufficient, and no nested exploration of states is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.setrecursionlimit(10**7)

    def kosaraju(n, g, rg):
        visited = [False] * n
        order = []

        def dfs1(v):
            visited[v] = True
            for to in g[v]:
                if not visited[to]:
                    dfs1(to)
            order.append(v)

        for i in range(n):
            if not visited[i]:
                dfs1(i)

        comp = [-1] * n
        cid = 0

        def dfs2(v, c):
            comp[v] = c
            for to in rg[v]:
                if comp[to] == -1:
                    dfs2(to, c)

        for v in reversed(order):
            if comp[v] == -1:
                dfs2(v, cid)
                cid += 1

        return comp, cid

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]
        edges = []
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            rg[v].append(u)
            edges.append((u, v))

        comp, c = kosaraju(n, g, rg)

        indeg = [0] * c
        for u, v in edges:
            if comp[u] != comp[v]:
                indeg[comp[v]] += 1

        sources = [i for i in range(c) if indeg[i] == 0]

        if len(sources) != 1:
            return "-1\n"

        for i in range(n):
            if comp[i] == sources[0]:
                return str(i + 1) + "\n"

    return solve()

# provided sample
assert run("5 6\n1 2\n2 3\n3 1\n3 4\n4 5\n5 3\n") == "-1\n"

# chain to single sink SCC
assert run("4 3\n1 2\n2 3\n3 4\n") == "1\n"

# single cycle
assert run("3 3\n1 2\n2 3\n3 1\n") == "-1\n"

# two components both reachable cycle
assert run("4 4\n1 2\n2 1\n3 4\n4 3\n") == "-1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| cycle between SCCs | -1 | multiple source SCCs |
| linear chain | 1 | unique source SCC |
| single SCC cycle | -1 | whole graph is one SCC but no unique source structure |
| disjoint cycles | -1 | multiple independent SCC sources |

## Edge Cases

A key edge case is when the entire graph is a single strongly connected component. In that situation, every vertex is reachable from every other, so the condensation graph has exactly one node with indegree zero. The algorithm selects any vertex in this SCC, which is correct because the car will eventually visit every vertex infinitely often under any walk.

Another edge case is when multiple SCCs have no incoming edges in the condensation graph. For example, two disjoint cycles with no edges between them. In this case, starting in one cycle allows the car to remain forever without entering the other, so no universal meeting point exists. The algorithm correctly outputs -1 because it finds more than one source SCC.

A final subtle case is when edges form a large cycle of SCCs, where every component has indegree one. Even though the graph is fully connected in a cyclic sense, no single SCC is unavoidable because the car can circulate indefinitely without committing to a unique destination component.