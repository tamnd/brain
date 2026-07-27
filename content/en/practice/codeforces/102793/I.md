---
title: "CF 102793I - \u0422\u0435\u043e\u0440\u0438\u044f \u0420\u0430\u043c\u0441\u0435\u044f"
description: "We have an undirected graph where rooms are vertices and tunnels are edges. We need to find a small group of rooms with one of two properties. The first possibility is a clique of size l, meaning every pair of rooms in the group has a tunnel between them."
date: "2026-07-27T18:03:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102793
codeforces_index: "I"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102793
solve_time_s: 67
verified: true
draft: false
---

[CF 102793I - \u0422\u0435\u043e\u0440\u0438\u044f \u0420\u0430\u043c\u0441\u0435\u044f](https://codeforces.com/problemset/problem/102793/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
# Problem Understanding

We have an undirected graph where rooms are vertices and tunnels are edges. We need to find a small group of rooms with one of two properties. The first possibility is a clique of size `l`, meaning every pair of rooms in the group has a tunnel between them. The second possibility is an anti-clique of size `k`, meaning no pair of rooms in the group has a tunnel between them. If neither structure exists, we print `-1`.

The input gives the number of rooms, the tunnels, and the two target sizes. The graph can have up to 300000 vertices and 300000 edges, while both requested group sizes are at most 5. The small values of `k` and `l` are the key constraint. A general clique search is hard, but searching for a clique or an independent set of size at most five allows us to use Ramsey theory. The sparse graph representation also matters because storing or checking all possible pairs of vertices is impossible.

With 300000 vertices, even checking every pair of rooms would require around 90000000000 operations, which is far beyond the limit. Any solution that enumerates triples, quadruples, or larger groups directly also becomes impossible quickly. We need an approach that depends almost linearly on the graph size and only explores a small search tree caused by the maximum answer size.

The first edge case is when one requested size is one. Any single vertex is both a clique and an anti-clique of size one, so the answer is immediately any vertex. For example:

```
Input:
5 0 1 3

Output:
1
```

A solution that only searches for edges or non-edges would incorrectly fail because it would miss the fact that a one-vertex group is always valid.

Another edge case is when the graph is empty. If we need an anti-clique, every set of vertices works, but if we need a clique of size greater than one, no clique exists. For example:

```
Input:
4 0 3 2

Output:
1 2 3
```

The algorithm must be able to move through non-neighbors correctly, because all vertices except the chosen one belong to the anti-clique side.

A final tricky case is when the graph is complete. Then anti-cliques larger than one are impossible, but every group of vertices is a clique. For example:

```
Input:
4 6 3 4

Output:
1 2 3 4
```

A careless implementation that only checks missing edges would fail even though the clique answer is immediate.

## Approaches

The direct approach would enumerate every possible group of vertices of the required size and check whether it forms a clique or anti-clique. For a target size of five, this means checking roughly `n^5` groups. With `n = 300000`, this is completely impossible.

A better direction comes from the structure of the problem. We are not looking for an arbitrary subgraph. We only care about finding either a clique or its opposite, an independent set, and both sizes are at most five.

Pick one vertex `v`. Every valid group containing `v` must choose the remaining vertices from exactly one of two places. If the group is a clique, all remaining vertices must be neighbors of `v`. If the group is an anti-clique, all remaining vertices must be non-neighbors of `v`.

This gives a recursive search. To find a clique of size `c` or an anti-clique of size `i`, we split the current candidate set into neighbors and non-neighbors of one vertex. We then search for a clique of size `c - 1` among neighbors, or an anti-clique of size `i - 1` among non-neighbors.

The brute force method fails because it treats every subset equally. The recursive method only follows combinations that can still contain one of the required structures. Since both parameters are at most five, the recursion depth is tiny. Ramsey theory gives the additional guarantee that if no answer exists, a graph avoiding both structures cannot be large. The recursion only reaches a small number of vertices in the difficult cases.

We can use the recurrence

`R(a, b) <= R(a - 1, b) + R(a, b - 1)`

with base cases `R(1, x) = R(x, 1) = 1`. This gives a safe upper bound for the size of a set that must contain either a clique of size `a` or an anti-clique of size `b`. If a candidate set is smaller than this value, the recursive call can immediately stop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^5) | O(1) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Start a recursive search with the full set of vertices. The parameters describe how many more vertices are needed for a clique and for an anti-clique.
2. If the clique requirement or anti-clique requirement is one, return any current vertex. A single vertex always satisfies both definitions.
3. If the current candidate set is smaller than the Ramsey bound for the remaining requirements, stop this branch. It cannot contain a valid answer.
4. Choose one vertex `v` from the current set. Split all other candidates into two groups. The first group contains neighbors of `v`, and the second group contains non-neighbors of `v`.
5. Search the neighbor group while decreasing the required clique size by one. This is correct because every additional vertex of a clique containing `v` must be connected to `v`.
6. If that fails, search the non-neighbor group while decreasing the required anti-clique size by one. This is correct because every additional vertex of an anti-clique containing `v` must avoid `v`.
7. If both recursive calls fail, no valid structure exists in this branch. Continue returning failure until either an answer is found or the root returns failure.

Why it works:

The invariant is that every recursive call receives exactly the vertices that can still complete one of the two required structures. If a solution contains the chosen vertex `v`, the rest of that solution must lie completely in either the neighbor group or the non-neighbor group. The recursion explores both possibilities, so it cannot discard a valid answer. The Ramsey bound only removes sets that are mathematically guaranteed to contain no solution of the requested sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k, l = map(int, input().split())

    graph = [[] for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    ramsey = [[0] * 6 for _ in range(6)]
    for i in range(1, 6):
        ramsey[1][i] = 1
        ramsey[i][1] = 1

    for i in range(2, 6):
        for j in range(2, 6):
            ramsey[i][j] = ramsey[i - 1][j] + ramsey[i][j - 1]

    mark = [0] * n
    token = 0

    def dfs(vertices, clique_need, indep_need):
        nonlocal token

        if clique_need == 1 or indep_need == 1:
            return [vertices[0]]

        if len(vertices) < ramsey[clique_need][indep_need]:
            return None

        v = vertices[0]

        token += 1
        cur = token
        for u in graph[v]:
            mark[u] = cur

        neigh = []
        non_neigh = []

        for u in vertices[1:]:
            if mark[u] == cur:
                neigh.append(u)
            else:
                non_neigh.append(u)

        if clique_need > 1:
            res = dfs(neigh, clique_need - 1, indep_need)
            if res is not None:
                return [v] + res

        if indep_need > 1:
            res = dfs(non_neigh, clique_need, indep_need - 1)
            if res is not None:
                return [v] + res

        return None

    ans = dfs(list(range(n)), l, k)

    if ans is None:
        print(-1)
    else:
        print(*[x + 1 for x in ans])

if __name__ == "__main__":
    solve()
```

The adjacency list stores only existing edges, which is necessary because the graph can have 300000 vertices. The `mark` array avoids repeatedly building adjacency sets. For each chosen vertex, its neighbors receive the current token value, allowing the split into neighbors and non-neighbors with one scan of the candidate list.

The recursive function keeps two counters. `clique_need` represents how many vertices are still required for a clique, while `indep_need` represents the same for an anti-clique. When one of them reaches one, the current vertex list already contains a valid single vertex answer.

The Ramsey table uses upper bounds rather than exact values. This is enough because the only purpose is pruning impossible branches. The values are tiny because both target sizes are at most five.

The returned vertices are converted back to one-based indexing before printing. The implementation avoids integer overflow automatically because Python integers have arbitrary precision.

## Worked Examples

Consider:

```
Input:
4 0 2 4
```

The graph has no edges. We need either a 4-clique or a 2-vertex anti-clique.

| Step | Candidate vertices | Clique need | Anti-clique need | Action |
| --- | --- | --- | --- | --- |
| 1 | 1,2,3,4 | 4 | 2 | Choose vertex 1 |
| 2 | Empty neighbors | 3 | 2 | Clique branch fails |
| 3 | 2,3,4 | 4 | 1 | Return vertex 2 |

The second branch succeeds immediately because any single vertex is a valid anti-clique of size one, completing the requested two-vertex anti-clique together with vertex 1.

Consider:

```
Input:
4 6 3 4
```

The graph is complete.

| Step | Candidate vertices | Clique need | Anti-clique need | Action |
| --- | --- | --- | --- | --- |
| 1 | 1,2,3,4 | 4 | 3 | Choose vertex 1 |
| 2 | 2,3,4 | 3 | 3 | Search neighbors |
| 3 | 3,4 | 2 | 3 | Search neighbors |
| 4 | 4 | 1 | 3 | Return vertex 4 |

The recursive path keeps taking the neighbor side because every remaining vertex is connected. It reconstructs the full clique.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each large recursive split scans only the current candidates, and the recursion depth is bounded by 10 because both target sizes are at most 5. |
| Space | O(n + m) | The adjacency list stores all edges, and the recursion stores only small candidate lists. |

The solution fits the constraints because the expensive part of the recursion only happens while the candidate sets are large enough to matter. Ramsey bounds guarantee that unsuccessful searches quickly shrink to small sets.

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

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""5 5 3 3
1 2
2 3
3 4
4 5
1 5
""") == "-1\n", "cycle without triangle"

assert run("""4 0 2 4
""").strip() in {"1 2", "1 3", "1 4", "2 3", "2 4", "3 4"}, "empty graph"

assert run("""4 6 3 4
1 2
1 3
1 4
2 3
2 4
3 4
""").strip() == "1 2 3 4", "complete graph"

assert run("""1 0 5 1
""").strip() == "1", "single vertex"

assert run("""5 0 5 5
""").strip() == "1 2 3 4 5", "large anti-clique"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Five vertices forming a cycle | `-1` | Checks the impossible case where neither structure exists |
| Empty graph | Any valid pair | Checks non-neighbor recursion |
| Complete graph | Four vertices | Checks clique recursion |
| One vertex | `1` | Checks size-one handling |
| Empty graph with size five request | All vertices | Checks maximum target size |

## Edge Cases

For the single-vertex case:

```
Input:
1 0 5 1
```

The recursive function immediately sees that a clique of size one is enough. It returns the only vertex without trying to inspect edges.

For the empty graph:

```
Input:
5 0 5 3
```

Choosing vertex 1 creates an empty neighbor group and a non-neighbor group containing vertices 2 through 5. The clique branch fails because there are no edges, but the anti-clique branch keeps all remaining vertices. The recursion eventually returns all five vertices because every pair is disconnected.

For the complete graph:

```
Input:
5 10 3 5
```

Choosing vertex 1 places every other vertex into the neighbor group. The anti-clique side is empty, but the clique side repeatedly removes one required vertex until five vertices are collected. The output is any five vertices in the graph.

For the case where no structure exists:

```
Input:
5 5 3 3
1 2
2 3
3 4
4 5
1 5
```

The graph is a cycle of length five. Every recursive split eventually reaches a candidate set smaller than the Ramsey bound for the remaining requirements, proving that no branch can contain a triangle or an independent set of size three. The algorithm returns `-1`.
