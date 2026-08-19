---
title: "CF 102168K - \u041e\u0431\u0445\u043e\u0434 \u0434\u0435\u0440\u0435\u0432\u0430"
description: "We have a tree with (n) vertices and (n-1) edges. We need to traverse every edge exactly once. The walk may start at any vertex, and whenever the current walk cannot continue along an unused edge, we may teleport to any other vertex and continue from there."
date: "2026-08-19T07:29:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "K"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 107
verified: true
draft: false
---

[CF 102168K - \u041e\u0431\u0445\u043e\u0434 \u0434\u0435\u0440\u0435\u0432\u0430](https://codeforces.com/problemset/problem/102168/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with (n) vertices and (n-1) edges. We need to traverse every edge exactly once. The walk may start at any vertex, and whenever the current walk cannot continue along an unused edge, we may teleport to any other vertex and continue from there. The goal is to minimize the number of teleports.

A single uninterrupted part of the traversal is a trail: it uses every edge in that part exactly once, although vertices may be visited several times. Thus the problem can be viewed as partitioning all tree edges into as few trails as possible. If the edges can be covered by (k) trails, we need exactly (k-1) teleports because the first trail can be started freely.

The input contains (n), followed by (n-1) pairs of vertex numbers describing the tree edges. The output is the minimum number of teleports.

The constraint (n \le 200000) rules out anything that examines exponentially many edge subsets, and even many quadratic algorithms are too slow under a two-second limit. A linear or (O(n\log n)) solution is the natural target. Since the graph is a tree, its number of edges is already (O(n)), so an adjacency-list representation gives linear memory.

The first boundary case is a tree with one vertex and no edges:

```
1
```

The correct answer is `0`. There is nothing to traverse, so no teleport is necessary. A formula that blindly assumes at least one trail and subtracts one could produce a negative answer.

The second important case is a simple path:

```
4
1 2
2 3
3 4
```

The correct answer is `0`, because we can simply walk from vertex 1 through 2 and 3 to 4. A careless approach might count every vertex of degree different from two as requiring a teleport, but only the number of odd-degree vertices matters.

A branching tree gives a different result:

```
4
1 2
1 3
1 4
```

The correct answer is `1`. Vertex 1 and all three leaves have odd degree, so there are four odd-degree vertices. One continuous trail can have only two odd endpoints, so at least two trails are necessary, which means one teleport.

## Approaches

A direct brute-force approach can treat the edges as objects that have to be divided into trails. One could enumerate every subset of edges, determine whether that subset can be traversed as one trail, and then use dynamic programming over subsets to find the minimum number of trails covering all edges. This is correct because every possible decomposition into trails appears among those subsets. However, a tree with (n) vertices has (n-1) edges, giving (2^{n-1}) possible edge subsets. Even ignoring the additional work required to validate each subset, that is already about (2^{199999}) states at the maximum constraint, so this approach becomes impossible almost immediately.

The brute-force works because it explicitly searches through all possible ways of splitting the traversal. The key observation is that a tree has a very rigid degree structure. For any graph, a trail has either zero or two vertices of odd degree within the edges belonging to that trail. When several trails are combined, every odd-degree vertex of the original graph must be an endpoint of one of those trails. In a tree there are no cycles that could change this accounting, and every set of odd-degree vertices can be paired to construct the required trails.

Let the tree contain (O) vertices of odd degree. Each trail contributes at most two odd endpoints, so at least (O/2) trails are necessary. This lower bound is attainable: pair the odd-degree vertices and decompose the tree's edges into trails with those endpoints. Hence the minimum number of trails is (O/2), provided there is at least one edge.

The required number of teleports is one less than the number of trails. Thus, for a nonempty tree,

[
\text{answer}=\frac{O}{2}-1.
]

For (n=1), there are no edges and the answer is zero.

There is an even simpler way to write the result for every tree with at least two vertices. A tree always has at least two leaves, so it always has at least two odd-degree vertices. We only need to count how many vertices have odd degree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(2^n)) | Too slow |
| Count odd degrees | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the tree and maintain the degree of every vertex. Every input edge increases the degree of both of its endpoints because the edge contributes one incident edge to each vertex.
2. Count the vertices whose degree is odd. Call this number (odd). The handshaking lemma guarantees that (odd) is even.
3. If (n=1), output `0`. The graph has no edges, so there is no traversal to perform.
4. Otherwise, the minimum number of continuous trails is (odd/2). Every trail can account for at most two odd endpoints, which gives the lower bound, and the structure of an undirected graph allows this bound to be achieved.
5. Since the first trail needs no teleport before it starts, joining (odd/2) trails requires exactly (odd/2-1) teleports. Output that value.

### Why it works

Consider any valid traversal and split it at every teleport. Each resulting piece is a trail using a disjoint set of edges. In a trail, all internal vertices have even degree within that trail, while its endpoints have odd degree. Consequently, a trail can account for at most two odd-degree vertices of the original tree, so (odd/2) trails are unavoidable.

For a tree, this lower bound is achievable. More generally, every connected graph with (O>0) odd-degree vertices can have its edges decomposed into (O/2) trails by pairing odd vertices and applying Euler-trail decomposition. A tree is connected and has no complications from cycles, so the same bound applies directly. Thus the minimum number of trails is exactly (odd/2), and the minimum number of teleports is exactly (odd/2-1). The (n=1) case is handled separately because it contains no trail at all.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    degree = [0] * n

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        degree[u] += 1
        degree[v] += 1

    if n == 1:
        print(0)
        return

    odd = sum(d & 1 for d in degree)
    print(odd // 2 - 1)

if __name__ == "__main__":
    solve()
```

The degree array is enough to solve the problem, so there is no need to store the adjacency list. For every edge ((u,v)), the code increments `degree[u]` and `degree[v]`. After all (n-1) edges have been processed, the parity of each degree is known.

The expression `d & 1` is one when `d` is odd and zero when it is even, so summing it counts exactly the odd-degree vertices. Because the number of odd-degree vertices in any undirected graph is even, `odd // 2` is an integer.

The special case `n == 1` must be handled before applying the formula. In that case `odd` would be zero, and `odd // 2 - 1` would incorrectly produce `-1`.

There is no recursion in the implementation, which avoids Python's recursion-depth limitations on trees shaped as a long path. The only arithmetic involves values at most (n), so integer overflow is not an issue in Python or in typical fixed-width implementations either.

## Worked Examples

### Sample 1

The input is the path

```
4
1 2
2 3
3 4
```

The degree state after processing each edge is:

| Processed edge | degree[1] | degree[2] | degree[3] | degree[4] | Odd vertices |
| --- | --- | --- | --- | --- | --- |
| none | 0 | 0 | 0 | 0 | 0 |
| 1-2 | 1 | 1 | 0 | 0 | 2 |
| 2-3 | 1 | 2 | 1 | 0 | 2 |
| 3-4 | 1 | 2 | 2 | 1 | 2 |

There are two odd vertices, 1 and 4. Therefore the tree needs (2/2=1) trail and (1-1=0) teleports. The traversal can simply be `1 -> 2 -> 3 -> 4`.

### Sample 2

The input is the three-edge star:

```
4
1 2
1 3
1 4
```

The degree state is:

| Processed edge | degree[1] | degree[2] | degree[3] | degree[4] | Odd vertices |
| --- | --- | --- | --- | --- | --- |
| none | 0 | 0 | 0 | 0 | 0 |
| 1-2 | 1 | 1 | 0 | 0 | 2 |
| 1-3 | 2 | 1 | 1 | 0 | 2 |
| 1-4 | 3 | 1 | 1 | 1 | 4 |

All four vertices have odd degree. One trail can cover at most two of these odd endpoints, so two trails are necessary. For example, one trail can traverse `2 -> 1 -> 3`, after which we teleport to vertex 4 and traverse the remaining edge `4 -> 1`. Hence the answer is `2 - 1 = 1`.

This example demonstrates why simply looking for a single Euler trail is insufficient. The whole tree does not have exactly zero or two odd-degree vertices, but it can be split into the minimum possible number of trails.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | There are (n-1) edges to process and (n) degrees to inspect. |
| Space | (O(n)) | The degree array contains one integer per vertex. |

With (n\le 200000), the algorithm performs only a constant amount of work per edge and vertex. It avoids both graph traversal overhead and exponential state enumeration, so it comfortably fits the two-second and 256 MB limits.

## Test Cases

```python
# helper: run the solution on an input string and return its output
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    degree = [0] * n

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        degree[u] += 1
        degree[v] += 1

    if n == 1:
        print(0)
        return

    odd = sum(d & 1 for d in degree)
    print(odd // 2 - 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """4
1 2
2 3
3 4
"""
) == "0", "sample 1"

# Provided sample 2
assert run(
    """4
1 2
1 3
1 4
"""
) == "1", "sample 2"

# Minimum-size tree
assert run(
    """1
"""
) == "0", "single vertex"

# Three-vertex path
assert run(
    """3
1 2
2 3
"""
) == "0", "path has one continuous trail"

# Five-vertex star
assert run(
    """5
1 2
1 3
1 4
1 5
"""
) == "1", "four leaves give two trails"

# Larger branching tree
assert run(
    """7
1 2
1 3
2 4
2 5
3 6
3 7
"""
) == "2", "six odd-degree vertices require three trails"

# Maximum-size path
n = 200000
path = [str(n)]
for i in range(1, n):
    path.append(f"{i} {i + 1}")
assert run("\n".join(path) + "\n") == "0", "maximum-size path"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Empty edge set and the special minimum-size case |
| Three-vertex path | `0` | Exactly two odd-degree endpoints |
| Five-vertex star | `1` | Several odd-degree leaves and the trail-to-teleport conversion |
| Seven-vertex balanced branching tree | `2` | Six odd-degree vertices and the general formula |
| Path with 200000 vertices | `0` | Maximum input size and linear-time performance |

## Edge Cases

For a single vertex,

```
1
```

the degree of the only vertex is zero, which is even, so `odd = 0`. The algorithm takes the explicit `n == 1` branch and returns `0`. This avoids interpreting the absence of edges as a trail that would require subtracting one from the number of trails.

For a path,

```
4
1 2
2 3
3 4
```

the degrees are (1,2,2,1). Only vertices 1 and 4 are odd, giving `odd = 2`. The formula produces `2 // 2 - 1 = 0`. The entire edge set is already one trail, so no teleport is required.

For a star,

```
4
1 2
1 3
1 4
```

the degrees are (3,1,1,1), so all four vertices are odd. The algorithm gets `odd = 4`, computes two required trails, and returns `4 // 2 - 1 = 1`. One possible decomposition is `2 -> 1 -> 3` and `4 -> 1`, with one teleport between them.

A tree can have many leaves, and this is where approaches based only on finding a longest path can fail. For example,

```
7
1 2
1 3
2 4
2 5
3 6
3 7
```

has degree sequence (2,3,3,1,1,1,1). Vertices 2, 3, 4, 5, 6, and 7 are odd, so `odd = 6`. Three trails are necessary and sufficient, giving `3 - 1 = 2` teleports. The answer depends on all odd-degree vertices, not just on the diameter or the number of leaves.

Finally, a path containing 200000 vertices stresses the implementation shape rather than the mathematical formula. Every internal vertex has degree two, while the two endpoints have degree one. The algorithm performs (199999) edge updates and one pass over 200000 degree values, producing `0`. Since it uses no recursive DFS and stores only the degree array, it remains safe even for this maximally deep tree.
