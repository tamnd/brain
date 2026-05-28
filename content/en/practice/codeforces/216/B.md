---
title: "CF 216B - Forming Teams"
description: "We can model the students as an undirected graph. Each student is a vertex, and every pair of enemies creates an edge. We want to split the remaining students into two teams of equal size such that no edge stays inside one team."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "implementation"]
categories: ["algorithms"]
codeforces_contest: 216
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 133 (Div. 2)"
rating: 1700
weight: 216
solve_time_s: 87
verified: true
draft: false
---

[CF 216B - Forming Teams](https://codeforces.com/problemset/problem/216/B)

**Rating:** 1700  
**Tags:** dfs and similar, implementation  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We can model the students as an undirected graph. Each student is a vertex, and every pair of enemies creates an edge. We want to split the remaining students into two teams of equal size such that no edge stays inside one team. In graph terms, we need a bipartite graph, because enemies must always end up on opposite sides.

If some connected component is not bipartite, then at least one student from that component must be removed. After removals, the total number of remaining students must also be even, because the two teams must have the same size.

The graph has at most 100 vertices and 100 edges, so even fairly slow graph algorithms would pass. A DFS or BFS over all vertices is trivial within the limits. The more interesting part is understanding exactly when removals are necessary.

The condition that every student has degree at most 2 heavily restricts the graph structure. Every connected component is either:

- a path,
- a cycle,
- or an isolated vertex.

A path is always bipartite. An even cycle is also bipartite. An odd cycle is not bipartite, and removing one vertex turns it into a path.

One subtle edge case is isolated students. Consider:

```
3 0
```

All students are independent, so the graph is bipartite. Still, we cannot split 3 students into two equal teams. One student must sit out, so the answer is `1`.

Another easy mistake is forgetting that every odd cycle requires one removal even if the total number of remaining students becomes even afterward.

Example:

```
3 3
1 2
2 3
3 1
```

This is a triangle. The graph is not bipartite. Removing one student leaves an edge between the other two students, which works. The correct answer is `1`.

A more subtle case combines both issues:

```
6 3
1 2
2 3
3 1
```

There is one odd cycle of size 3 and three isolated vertices. Removing one vertex from the cycle leaves 5 students total, which is still odd. One additional student must also sit out. The correct answer is `2`.

A careless implementation that only counts odd cycles would incorrectly print `1`.

## Approaches

A brute-force approach would try every subset of students to remove. For each subset, we would check whether the remaining graph is bipartite and whether the number of remaining students is even. Since there are `2^n` subsets, this becomes impossible very quickly. Even for `n = 100`, the search space is astronomically large.

The graph structure gives a much cleaner direction. Since every vertex has degree at most 2, connected components are extremely simple. The only problematic structure is an odd cycle.

A connected bipartite component can always be colored with two colors, meaning its vertices can be separated into two enemy-free groups. An odd cycle breaks this property because walking around the cycle forces a contradiction in coloring.

So the problem reduces to two observations:

First, every odd cycle forces exactly one removal.

Second, after fixing all odd cycles, the remaining graph is bipartite. If the number of remaining students is odd, we remove one more arbitrary student to make the total even.

DFS coloring detects odd cycles naturally. Whenever we try to color adjacent vertices with opposite colors and discover a conflict, that connected component is not bipartite.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * (n + m)) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph.

Every student stores the list of enemies connected to them.
2. Maintain a color array initialized with `-1`.

A value of `-1` means the vertex has not been visited yet. Colors `0` and `1` represent the two teams in bipartite coloring.
3. Iterate through all vertices.

Whenever an unvisited vertex is found, start a DFS from it.
4. During DFS, assign alternating colors to neighboring vertices.

If a neighbor is unvisited, give it the opposite color and continue DFS.
5. If we ever find an edge connecting two vertices with the same color, the connected component is not bipartite.

Because every component has maximum degree 2, this means the component contains an odd cycle.
6. For every non-bipartite component, increase the answer by 1.

Removing one student from an odd cycle always breaks the cycle and turns the component into a bipartite graph.
7. After processing all components, compute how many students remain.

If `n - answer` is odd, increase the answer by 1.

The remaining students must be split into two equal teams, so their count must be even.
8. Print the final answer.

### Why it works

DFS coloring correctly characterizes bipartite graphs. A graph is bipartite if and only if no edge connects vertices with the same color during two-coloring.

Since every connected component here has degree at most 2, the only non-bipartite structure possible is an odd cycle. Removing one vertex from such a cycle destroys the cycle and leaves a path, which is bipartite.

After fixing all odd cycles, the graph becomes bipartite. Any bipartite graph can be split into two enemy-free groups. The only remaining issue is parity. If the total number of remaining students is odd, equal teams are impossible, so one additional student must be removed.

Because each odd cycle requires at least one removal and parity may require one more, the algorithm produces the minimum possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

adj = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

color = [-1] * (n + 1)

def dfs(start):
    stack = [start]
    color[start] = 0

    while stack:
        u = stack.pop()

        for v in adj[u]:
            if color[v] == -1:
                color[v] = color[u] ^ 1
                stack.append(v)
            elif color[v] == color[u]:
                return False

    return True

removed = 0

for i in range(1, n + 1):
    if color[i] == -1:
        if not dfs(i):
            removed += 1

remaining = n - removed

if remaining % 2 == 1:
    removed += 1

print(removed)
```

The adjacency list stores the graph compactly and supports efficient traversal. Since `n` and `m` are small, either recursive or iterative DFS would work, but iterative DFS avoids recursion depth concerns entirely.

The `color` array handles both visitation state and bipartite coloring. Unvisited vertices stay at `-1`. During traversal, neighbors always receive the opposite color using XOR with `1`.

The DFS returns `False` as soon as it finds a conflict edge. That immediately tells us the component contains an odd cycle.

One subtle detail is that we count exactly one removal per non-bipartite component. Because every vertex has degree at most 2, a connected component cannot contain multiple independent odd cycles. In a general graph this shortcut would fail.

The parity adjustment happens only after all odd cycles are fixed. Removing vertices from odd cycles changes the total number of remaining students, so parity must be checked afterward.

## Worked Examples

### Example 1

Input:

```
5 4
1 2
2 4
5 3
1 4
```

The graph contains a triangle among vertices `1, 2, 4` and one separate edge `3, 5`.

| Step | Current Vertex | DFS Result | Removed |
| --- | --- | --- | --- |
| 1 | 1 | Non-bipartite | 1 |
| 2 | 3 | Bipartite | 1 |

After removing one student from the triangle, `4` students remain, which is already even.

Final answer: `1`

This trace shows the core observation of the problem. A single odd cycle requires exactly one removal.

### Example 2

Input:

```
6 3
1 2
2 3
3 1
```

Vertices `4, 5, 6` are isolated.

| Step | Current Vertex | DFS Result | Removed |
| --- | --- | --- | --- |
| 1 | 1 | Non-bipartite | 1 |
| 2 | 4 | Bipartite | 1 |
| 3 | 5 | Bipartite | 1 |
| 4 | 6 | Bipartite | 1 |

After fixing the triangle, `5` students remain.

| Remaining Students | Even? | Final Removed |
| --- | --- | --- |
| 5 | No | 2 |

Final answer: `2`

This example demonstrates why the parity adjustment is necessary even after all odd cycles are handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex and edge is processed once during DFS |
| Space | O(n + m) | Adjacency list and color array |

With at most 100 vertices and 100 edges, this solution runs comfortably within the limits. Even a much slower graph traversal would pass, but the linear approach is both clean and optimal.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (n + 1)

    def dfs(start):
        stack = [start]
        color[start] = 0

        while stack:
            u = stack.pop()

            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    stack.append(v)
                elif color[v] == color[u]:
                    return False

        return True

    removed = 0

    for i in range(1, n + 1):
        if color[i] == -1:
            if not dfs(i):
                removed += 1

    if (n - removed) % 2 == 1:
        removed += 1

    print(removed)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(
"""5 4
1 2
2 4
5 3
1 4
"""
) == "1", "sample 1"

# minimum graph, already balanced
assert run(
"""2 0
"""
) == "0", "two isolated students"

# odd cycle
assert run(
"""3 3
1 2
2 3
3 1
"""
) == "1", "triangle requires one removal"

# odd cycle plus parity issue
assert run(
"""6 3
1 2
2 3
3 1
"""
) == "2", "triangle fixed but remaining count still odd"

# even cycle
assert run(
"""4 4
1 2
2 3
3 4
4 1
"""
) == "0", "even cycle is bipartite"

# isolated vertices causing parity problem
assert run(
"""5 0
"""
) == "1", "odd number of isolated students"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0` | `0` | Smallest valid balanced case |
| Triangle graph | `1` | Detecting odd cycles |
| Triangle plus isolated nodes | `2` | Extra parity removal |
| Even cycle | `0` | Correct bipartite handling |
| `5 0` | `1` | Odd total with no edges |

## Edge Cases

Consider the completely disconnected case:

```
3 0
```

DFS visits each vertex independently and never finds a coloring conflict. `removed = 0` after graph processing. Since `3` students remain, parity is odd, so one more student is removed. The algorithm prints `1`.

Now consider a single triangle:

```
3 3
1 2
2 3
3 1
```

DFS colors `1` with `0`, `2` with `1`, and `3` with `0`. When processing edge `(3,1)`, both endpoints have color `0`, so the component is non-bipartite. `removed` becomes `1`. Remaining students equal `2`, which is already even. Final answer is `1`.

Finally, consider multiple components:

```
8 5
1 2
2 3
3 1
4 5
6 7
```

The component `{1,2,3}` is an odd cycle, so one student must be removed. Components `{4,5}` and `{6,7}` are bipartite, and vertex `8` is isolated. After one removal, `7` students remain, still odd. The algorithm removes one more student and outputs `2`.

This confirms the two independent sources of removals: fixing odd cycles and fixing parity.
