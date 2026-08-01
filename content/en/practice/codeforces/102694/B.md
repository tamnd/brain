---
title: "CF 102694B - Dynamic Diameter"
description: "The problem starts with a tree containing n vertices. A new isolated vertex exists outside this tree. For every original vertex i, we imagine connecting that new vertex to i with one extra edge and ask what the diameter of the resulting tree would be."
date: "2026-08-01T23:28:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102694
codeforces_index: "B"
codeforces_contest_name: "AlgorithmsThread Tree Basics Contest"
rating: 0
weight: 102694
solve_time_s: 57
verified: true
draft: false
---

[CF 102694B - Dynamic Diameter](https://codeforces.com/problemset/problem/102694/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem starts with a tree containing `n` vertices. A new isolated vertex exists outside this tree. For every original vertex `i`, we imagine connecting that new vertex to `i` with one extra edge and ask what the diameter of the resulting tree would be. The task is to output this value for every possible attachment point. The input gives only the original tree edges, and the output contains `n` answers, one for each possible connection.

The number of vertices can reach `300000`, so an approach that explores the tree from every vertex is too slow. A single traversal of a tree takes linear time, which is acceptable at this scale, but repeating it `n` times would require about `n²` operations, roughly ninety billion visits in the largest case. The solution must stay close to `O(n)`.

The tricky cases are mostly related to misunderstanding how the new leaf changes the diameter. If the new leaf is attached to a vertex already near the middle of the tree, the original diameter can remain the answer. For example:

```
3
1 2
2 3
```

The original diameter is `2`. Attaching the new vertex to node `2` creates a path of length `2` from the new leaf to either end, so the answer is `2`. A careless solution that always adds one to the old diameter would output `3`.

Another edge case is a single vertex:

```
1
```

There are no edges in the input. After adding the new vertex and connecting it to the only node, the tree has two vertices connected by one edge, so the answer is `1`. Code that assumes there are always two diameter endpoints can fail here.

A final case is when the attached vertex is an endpoint of the original diameter:

```
3
1 2
2 3
```

Attaching the new vertex to node `1` gives the path `new - 1 - 2 - 3`, whose length is `3`. The answer is larger than the old diameter, so solutions that only print the original diameter are incorrect.

## Approaches

A direct solution is to try every possible attachment vertex. For one chosen vertex `v`, we could run a traversal from `v`, find its farthest vertex, and compute the new diameter as the maximum of the old diameter and the distance from the new leaf to that farthest vertex. This works because every longest path involving the new vertex must start with the new edge and then continue to the farthest original vertex from `v`.

The problem is that this repeats almost the same work many times. Running a traversal from every one of `n` vertices costs `O(n²)` time. With `n = 300000`, this is far beyond what is possible.

The key observation is that a tree has a very special relationship between its diameter and its farthest vertices. If `a` and `b` are the two endpoints of any diameter, then for every vertex `v`, the farthest vertex from `v` is always one of `a` or `b`. This means we do not need to search from every vertex. We only need the distances to these two endpoints.

Let the original diameter length be `D`. When the new leaf is attached to `v`, any diameter in the new tree is either the old diameter or a path starting from the new leaf. The longest path starting from the new leaf has length `ecc(v) + 1`, where `ecc(v)` is the maximum distance from `v` to any old vertex. Because `ecc(v) = max(dist(v, a), dist(v, b))`, every answer becomes:

```
max(D, max(dist(v, a), dist(v, b)) + 1)
```

The entire problem reduces to finding two diameter endpoints and two distance arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start a traversal from any vertex, for example vertex `1`, and find the farthest vertex from it. Call this vertex `a`.

The farthest vertex from an arbitrary starting point in a tree is always an endpoint of a diameter.

1. Start another traversal from `a` and find the farthest vertex from `a`. Call it `b`. The distance from `a` to `b` is the original diameter length `D`.
2. Traverse the tree once from `a` and store the distance from `a` to every vertex.

These distances represent one possible side of the eccentricity calculation.

1. Traverse the tree once from `b` and store the distance from `b` to every vertex.

Now every vertex knows its distance to both diameter endpoints.

1. For every vertex `v`, compute:

```
max(D, max(dist_a[v], dist_b[v]) + 1)
```

The first value handles diameters that do not use the new leaf. The second value handles paths that start at the new leaf.

Why it works:

The only new paths introduced after adding the extra vertex are paths that begin with the new edge. Such a path has length one plus the distance from the chosen attachment vertex to some original vertex. The longest such path uses the farthest original vertex from the attachment point. In a tree, every vertex's farthest vertex is one of the two endpoints of the diameter, so the two stored distance arrays contain exactly the information needed to compute every eccentricity. Taking the maximum with the old diameter covers both possible types of longest paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_dist(start, graph):
    n = len(graph) - 1
    dist = [-1] * (n + 1)
    stack = [start]
    dist[start] = 0

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                stack.append(u)

    return dist

def solve():
    n = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    dist0 = get_dist(1, graph)
    a = max(range(1, n + 1), key=lambda x: dist0[x])

    dist_a = get_dist(a, graph)
    b = max(range(1, n + 1), key=lambda x: dist_a[x])

    dist_b = get_dist(b, graph)
    diameter = dist_a[b]

    ans = []
    for i in range(1, n + 1):
        ans.append(str(max(diameter, max(dist_a[i], dist_b[i]) + 1)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `get_dist` function performs an iterative DFS. Using an explicit stack avoids Python recursion depth problems because a tree can be a chain with `300000` vertices.

The first traversal finds one diameter endpoint. The second traversal both finds the other endpoint and gives all distances from the first endpoint. The third traversal gives the distances from the other endpoint. These two arrays are the complete information needed for all answers.

The diameter length is stored before computing the answers. The final loop checks both possibilities for each vertex: keeping the old diameter, or creating a longer path through the newly attached vertex.

There are no integer overflow concerns in Python because integers grow automatically. The main implementation detail to avoid is accidentally using recursion, which can exceed the default recursion limit on a path shaped tree.

## Worked Examples

For the input:

```
3
3 2
2 1
```

the diameter endpoints are nodes `1` and `3`.

| Vertex | Distance to 1 | Distance to 3 | Original Diameter | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 2 | 3 |
| 2 | 1 | 1 | 2 | 2 |
| 3 | 2 | 0 | 2 | 3 |

This demonstrates that the new leaf can increase the diameter when attached to an endpoint, but not when attached near the center.

For the input:

```
5
4 2
1 4
5 4
3 4
```

the tree has center `4` and diameter endpoints among the leaves.

| Vertex | Distance to endpoint A | Distance to endpoint B | Original Diameter | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 2 | 3 |
| 2 | 2 | 0 | 2 | 3 |
| 3 | 1 | 1 | 2 | 3 |
| 4 | 1 | 1 | 2 | 2 |
| 5 | 2 | 0 | 2 | 3 |

The center vertex keeps the original diameter because connecting the new leaf there does not create a path longer than the existing leaf-to-leaf path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Three tree traversals and one final pass over all vertices |
| Space | O(n) | Adjacency lists and distance arrays store linear information |

The algorithm performs only a constant number of operations per vertex and edge. This fits the `300000` vertex limit because the total work grows linearly with the tree size.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    n = int(data())
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a, b = map(int, data().split())
        graph[a].append(b)
        graph[b].append(a)

    def dist(start):
        d = [-1] * (n + 1)
        d[start] = 0
        stack = [start]
        while stack:
            v = stack.pop()
            for u in graph[v]:
                if d[u] == -1:
                    d[u] = d[v] + 1
                    stack.append(u)
        return d

    d = dist(1)
    a = max(range(1, n + 1), key=lambda x: d[x])
    da = dist(a)
    b = max(range(1, n + 1), key=lambda x: da[x])
    db = dist(b)
    dia = da[b]

    result = "\n".join(
        str(max(dia, max(da[i], db[i]) + 1))
        for i in range(1, n + 1)
    )

    sys.stdin = old_stdin
    return result

assert solve_io("1\n") == "1", "single vertex"
assert solve_io("3\n3 2\n2 1\n") == "3\n2\n3", "path tree"
assert solve_io("5\n4 2\n1 4\n5 4\n3 4\n") == "3\n3\n3\n2\n3", "sample tree"
assert solve_io("4\n1 2\n2 3\n3 4\n") == "4\n3\n3\n4", "long chain"
assert solve_io("4\n1 2\n1 3\n1 4\n") == "3\n3\n3\n3", "star tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Handles the smallest possible tree |
| A chain of four vertices | `4 3 3 4` | Checks diameter endpoints |
| A star centered at one vertex | `3 3 3 3` | Checks center behavior |
| The provided samples | Matching samples | Confirms the formula |

## Edge Cases

For a single vertex:

```
1
```

The traversal finds the only vertex as both diameter endpoints. Its eccentricity is zero, so the formula becomes `max(0, 0 + 1)`, producing `1`. The algorithm does not need special handling because the diameter endpoint logic still works.

For a middle attachment point:

```
3
1 2
2 3
```

The diameter is `2`. For vertex `2`, both endpoint distances are `1`, so the new path through the added leaf has length `2`. The maximum remains `2`, which avoids incorrectly increasing every answer.

For an endpoint attachment point:

```
3
1 2
2 3
```

For vertex `1`, the maximum endpoint distance is `2`. Adding the new edge creates a path of length `3`, and the formula returns `max(2, 2 + 1) = 3`. The same reasoning applies to the opposite endpoint.
