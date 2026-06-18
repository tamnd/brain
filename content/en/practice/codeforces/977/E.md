---
problem: 977E
contest_id: 977
problem_index: E
name: "Cyclic Components"
contest_name: "Codeforces Round 479 (Div. 3)"
rating: 1500
tags: ["dfs and similar", "dsu", "graphs"]
answer: passed_samples
verified: true
solve_time_s: 61
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a501-2120-83ec-ad40-57e2d61c49fa
---

# CF 977E - Cyclic Components

**Rating:** 1500  
**Tags:** dfs and similar, dsu, graphs  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 1s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a501-2120-83ec-ad40-57e2d61c49fa  

---

## Solution

## Problem Understanding

We are given an undirected graph, and the task is to count how many of its connected components form a simple cycle. A component is considered a cycle when all of its vertices can be arranged in a ring so that every vertex has exactly two neighbors inside the component, and there are no extra edges beyond those that form the ring.

In graph terms, this means we are looking for connected components where every vertex has degree exactly two within that component. A component with extra branches or internal chords is disqualified, even if it contains a cycle somewhere inside it. Isolated cycles like a triangle or a square are valid, but any “cycle plus tail” structure is not.

The constraints allow up to 200,000 vertices and edges. This immediately rules out anything that tries to check all subsets or recompute connectivity repeatedly. Any solution must run in linear or near-linear time, so a graph traversal such as DFS, BFS, or DSU-based grouping is necessary.

A few subtle edge cases appear naturally.

A single connected component with exactly one cycle but extra edges breaks the condition. For example, a triangle with an extra leaf node attached is connected and contains a cycle, but is not a cycle component. The correct answer contribution is zero.

A pure cycle must have at least three vertices. A component of size two with a single edge is not valid, even though both vertices have degree one, because it cannot form a closed loop.

Finally, isolated vertices or trees are always invalid since they do not contain cycles where every vertex has degree two.

## Approaches

A brute-force idea is to compute connected components and, for each one, explicitly verify whether it forms a cycle. We could do this by collecting all vertices in a component, then checking two conditions: every vertex has degree exactly two within the component, and the number of edges equals the number of vertices. This works because in any simple cycle, edges and vertices match one-to-one in a closed loop.

The problem with a naive approach appears only in implementation inefficiency, not correctness. If we repeatedly scan adjacency lists or recompute component membership inefficiently, we may drift toward quadratic behavior. However, even a straightforward DFS that gathers components once and checks degrees remains linear.

The key observation is that a connected component is a cycle if and only if every vertex in it has degree exactly two within the component. This removes the need for edge counting or structural reconstruction. During a traversal, we can compute component size and sum of internal degrees, or simply verify the degree condition for all nodes in the component.

We use DFS or BFS to explore each component once, marking visited nodes. For each component, we check whether all vertices satisfy degree equals two. If yes, the component is a cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (rechecking structure repeatedly) | O(n²) | O(n) | Too slow |
| DFS/BFS with degree validation | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list representation of the graph. This allows constant-time iteration over neighbors of each vertex during traversal.
2. Maintain a visited array initialized to false for all vertices. This ensures each node is processed exactly once across all components.
3. Iterate over every vertex from 1 to n. If a vertex is unvisited, it becomes the starting point of a new connected component.
4. Run a DFS or BFS from this vertex, marking all reachable nodes as part of the same component. During traversal, collect all vertices belonging to this component in a list.
5. After finishing traversal of a component, check every vertex in that component and verify that its adjacency list size is exactly 2. This condition enforces that each vertex participates in exactly two edges inside the component, which is necessary for a cycle.
6. If all vertices in the component satisfy this condition and the component has at least 3 vertices, increment the answer.
7. Continue until all vertices have been processed, then output the final count.

### Why it works

In any connected component, if every vertex has degree exactly two, the structure cannot branch or terminate. Starting from any vertex and following edges must eventually return to the starting point without repetition, forming a single simple cycle. Conversely, any simple cycle graph has every vertex of degree exactly two. Therefore, the degree condition is both necessary and sufficient for identifying cycle components in an undirected graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

visited = [False] * (n + 1)

def dfs(start):
    stack = [start]
    comp = []
    visited[start] = True

    while stack:
        u = stack.pop()
        comp.append(u)
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)

    return comp

ans = 0

for i in range(1, n + 1):
    if not visited[i]:
        comp = dfs(i)

        ok = True
        if len(comp) < 3:
            ok = False
        else:
            for u in comp:
                if len(g[u]) != 2:
                    ok = False
                    break

        if ok:
            ans += 1

print(ans)
```

The solution builds adjacency lists and runs a DFS from each unvisited node, ensuring each connected component is extracted exactly once. The DFS collects all nodes in the component.

After extracting a component, the code first checks its size. A cycle must contain at least three vertices, so smaller components are immediately rejected. Then it validates the defining property of cycle graphs: every vertex must have exactly two neighbors in the full graph, which in a simple connected component implies it lies on a single cycle.

A common mistake is trying to count edges inside the component and comparing to vertices without careful handling of duplicates or traversal state. Using the global adjacency list degree avoids recomputation and avoids subtle bookkeeping errors.

The DFS is iterative to avoid recursion depth issues given the upper bound of 200,000 nodes.

## Worked Examples

### Example 1

Input:

```
5 4
1 2
3 4
5 4
3 5
```

We process components step by step.

| Start node | Component found | Sizes | Degree check result |
| --- | --- | --- | --- |
| 1 | [1, 2] | 2 | fail |
| 3 | [3, 4, 5] | 3 | pass |
| 5 | already visited | - | - |

The first component is a single edge, which fails the size requirement. The second component forms a triangle where each node has degree 2, so it is counted.

The final answer is 1.

### Example 2

Input:

```
4 3
1 2
2 3
3 4
```

This graph is a simple path.

| Start node | Component found | Sizes | Degree check result |
| --- | --- | --- | --- |
| 1 | [1, 2, 3, 4] | 4 | fail |

Even though the graph is connected, nodes 1 and 4 have degree 1, so it is not a cycle component.

The output is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is visited once during DFS and adjacency checks |
| Space | O(n + m) | Adjacency list plus visited array and component storage |

The linear complexity fits comfortably within the constraints of 200,000 vertices and edges. Both memory and runtime remain proportional to the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    visited = [False] * (n + 1)

    def dfs(start):
        stack = [start]
        comp = []
        visited[start] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in g[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)
        return comp

    ans = 0
    for i in range(1, n + 1):
        if not visited[i]:
            comp = dfs(i)
            if len(comp) >= 3 and all(len(g[u]) == 2 for u in comp):
                ans += 1
    return str(ans)

# provided sample
assert run("""5 4
1 2
3 4
5 4
3 5
""") == "1"

# single edge
assert run("""2 1
1 2
""") == "0"

# simple cycle
assert run("""3 3
1 2
2 3
3 1
""") == "1"

# chain
assert run("""5 4
1 2
2 3
3 4
4 5
""") == "0"

# two disjoint cycles
assert run("""6 6
1 2
2 3
3 1
4 5
5 6
6 4
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | 0 | minimum invalid component |
| triangle cycle | 1 | smallest valid cycle |
| chain graph | 0 | tree structure rejection |
| two cycles | 2 | multiple component counting |

## Edge Cases

A single edge component like `1 - 2` is handled correctly because its size is 2, which fails the minimum size requirement for a cycle. The DFS collects both nodes, and the check immediately rejects it.

A triangle such as `1 - 2 - 3 - 1` passes because all nodes have adjacency list size 2. The DFS collects all three nodes in one component, and the condition holds for each node.

A star graph like `1 connected to all others` fails because the center node has degree greater than 2, violating the cycle condition even though the graph is connected.