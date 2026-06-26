---
title: "CF 105790L - Lango Mocos"
description: "We have N types of rocks. Some pairs of types are incompatible, meaning the two types cannot be stored in the same bag. Dudu has exactly two bags, and every rock type must be assigned to one of them."
date: "2026-06-26T08:54:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "L"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 36
verified: true
draft: false
---

[CF 105790L - Lango Mocos](https://codeforces.com/problemset/problem/105790/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `N` types of rocks. Some pairs of types are incompatible, meaning the two types cannot be stored in the same bag. Dudu has exactly two bags, and every rock type must be assigned to one of them. A valid assignment is one where every toxic pair is split between different bags.

The input describes an undirected graph. Each rock type is a vertex, and every toxic relationship is an edge. The question becomes whether the vertices can be divided into two groups such that no edge has both endpoints inside the same group. If possible, we must output the two groups. Otherwise, we report that the separation cannot be done.

The limits are large enough that the solution must be linear. With up to `100000` vertices and `100000` edges, an algorithm that repeatedly checks all pairs would perform around `10^10` operations in the worst case, which is far beyond what a one second limit allows. We need a solution close to `O(N + M)`, where every vertex and edge is processed only a constant number of times.

The main edge cases come from graph structure rather than input size. A graph with no toxic relationships is valid because every rock can go into either bag. For example:

```
Input:
3 0

Output:
POSSIVEL
3 0
1 2 3
```

A careless implementation that only starts searching from vertex `1` would miss isolated vertices in other components.

A single vertex is another special case:

```
Input:
1 0

Output:
POSSIVEL
1 0
1
```

There is no conflict to resolve, so placing the only type in one bag is valid. Code that assumes both bags must be non-empty would fail here.

A triangle is the smallest impossible case:

```
Input:
3 3
1 2
2 3
3 1

Output:
IMPOSSIVEL
```

Trying to alternate colors around the cycle forces the first and last vertices to receive the same color even though they are connected. Any approach that only checks local neighbors without detecting this contradiction would incorrectly accept it.

## Approaches

The straightforward approach is to try every possible division of the rocks into two bags. Since each rock has two choices, this creates `2^N` possible assignments. For each assignment, we can inspect every toxic pair and check whether both endpoints landed in the same bag. This method is correct because it directly tests the definition of a valid separation, but it is unusable when `N` reaches `100000`. The worst case requires checking about `2^100000` assignments.

The graph structure gives a much better way to think about the problem. A valid two-bag separation is exactly a bipartition of the graph. In graph theory terms, each bag is an independent set, and an undirected graph can be split into two independent sets if and only if it is bipartite.

A bipartite graph can be recognized by assigning one of two colors to every vertex so that every edge connects different colors. Starting from any unvisited vertex, we can color it and use a graph traversal to force alternating colors through its connected component. If we ever find an edge connecting two vertices with the same color, the required separation is impossible.

The brute-force solution works because it explores every possible coloring. The observation that only two colors matter lets us construct the coloring directly instead of searching through all possibilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N * M) | O(N) | Too slow |
| Optimal | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph. Each toxic pair creates an undirected edge because the incompatibility works in both directions.
2. Keep an array storing the color of every vertex. Use `-1` for unvisited vertices, and use `0` and `1` for the two possible bags.
3. Iterate through every vertex. If a vertex has not been colored yet, start a traversal from it and assign it color `0`. This step is needed because the graph can have multiple disconnected components.
4. During the traversal, assign every neighbor of a vertex the opposite color. If a neighbor already has the same color as the current vertex, the graph contains a contradiction and the answer is impossible.
5. After all components have been processed, collect vertices with color `0` into the first bag and vertices with color `1` into the second bag. The coloring guarantees that every toxic pair is split between these two groups.

Why it works: the invariant maintained during traversal is that every processed edge connects vertices with different colors. When we assign an uncolored neighbor the opposite color, we preserve this property for that edge. If an already colored neighbor has the wrong color, no valid two-color assignment can exist because that edge requires both equal and different colors at the same time. If the traversal finishes without contradictions, every edge crosses between the two color groups, so the two bags are valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n
    bag0 = []
    bag1 = []

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    stack.append(v)
                elif color[v] == color[u]:
                    print("IMPOSSIVEL")
                    return

    for i in range(n):
        if color[i] == 0:
            bag0.append(i + 1)
        else:
            bag1.append(i + 1)

    print("POSSIVEL")
    print(len(bag0), len(bag1))
    print(*bag0)
    print(*bag1)

if __name__ == "__main__":
    solve()
```

The adjacency list stores only existing toxic relationships, which keeps memory usage proportional to the actual graph size. The traversal uses an explicit stack instead of recursion because Python's default recursion limit is too small for a chain of `100000` vertices.

The outer loop over all vertices handles disconnected graphs. A common mistake is to run DFS or BFS only from vertex `1`, which leaves other components unchecked.

The expression `color[u] ^ 1` flips between `0` and `1`. It avoids extra condition checks and makes the two-bag assignment direct.

The final collection step converts internal zero-based indexes back into the one-based numbering used by the problem.

## Worked Examples

### Example 1

Input:

```
2 1
1 2
```

The traversal starts from vertex `1`.

| Current vertex | Current color | Neighbor checked | Neighbor color | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | uncolored | Assign color 1 |
| 2 | 1 | 1 | 0 | Valid edge |

The final groups are:

| Bag 0 | Bag 1 |
| --- | --- |
| 1 | 2 |

The edge connects different colors, so the separation is possible.

### Example 2

Input:

```
6 5
1 2
2 3
3 1
4 5
5 6
```

The first component already creates a contradiction.

| Current vertex | Current color | Neighbor | Neighbor color | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | uncolored | Assign color 1 |
| 1 | 0 | 3 | uncolored | Assign color 1 |
| 2 | 1 | 3 | 1 | Conflict |

Vertices `1`, `2`, and `3` form a triangle. The traversal detects that vertices `2` and `3` would need different colors because they are adjacent, but both were forced to color `1`. The correct answer is `IMPOSSIVEL`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Every vertex enters the traversal once and every edge is examined from both endpoints. |
| Space | O(N + M) | The adjacency list stores all edges and the arrays store colors and traversal data. |

The constraints allow `100000` vertices and edges, so a linear graph traversal comfortably fits within the required limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("""2 1
1 2
""") == """POSSIVEL
1 1
1
2
""", "sample 1"

assert run("""1 0
""") == """POSSIVEL
1 0
1

""", "sample 2"

assert run("""3 3
1 2
2 3
3 1
""") == """IMPOSSIVEL
""", "odd cycle"

assert run("""5 4
1 2
1 3
1 4
3 5
""") == """POSSIVEL
2 3
1 5
2 3 4
""", "tree shaped bipartite graph"

assert run("""4 0
""") == """POSSIVEL
4 0
1 2 3 4

""", "empty graph"

assert run("""4 4
1 2
2 3
3 4
4 1
""") == """POSSIVEL
2 2
1 3
2 4
""", "even cycle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | One bag with the only vertex | Minimum size handling |
| `4 0` | All vertices can share one bag | Empty graph handling |
| Triangle graph | `IMPOSSIVEL` | Odd cycle detection |
| Four-cycle graph | Two alternating groups | Correct bipartite coloring |
| Sample graph with branches | Valid partition | General traversal behavior |

## Edge Cases

For the isolated vertex case:

```
Input:
1 0
```

The algorithm visits vertex `1`, assigns color `0`, and finishes immediately because there are no neighbors. The final collection places vertex `1` into the first bag and leaves the second bag empty. The output remains valid because there are no toxic pairs.

For disconnected graphs:

```
Input:
4 1
1 2
```

The first traversal colors vertices `1` and `2`. Vertices `3` and `4` are never reached from that component, so the outer loop starts new traversals for them. They receive colors independently, and the final partition includes every vertex.

For an impossible odd cycle:

```
Input:
3 3
1 2
2 3
3 1
```

The algorithm colors vertex `1` as `0`, forcing vertices `2` and `3` to become `1`. When it checks the edge between `2` and `3`, both endpoints have the same color. Since every edge must connect opposite bags, no valid assignment exists and the algorithm correctly prints `IMPOSSIVEL`.
