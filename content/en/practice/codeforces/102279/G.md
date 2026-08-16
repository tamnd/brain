---
title: "CF 102279G - Get Higher and Higher"
description: "There are two trees. B21 chooses the root of his tree optimally, trying to make its height as large as possible. Lowie chooses the root of his tree adversarially from B21's perspective, so B21 only needs to know whether there exists some root for Lowie's tree that makes B21's…"
date: "2026-08-16T19:19:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "G"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 105
verified: true
draft: false
---

[CF 102279G - Get Higher and Higher](https://codeforces.com/problemset/problem/102279/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two trees. B21 chooses the root of his tree optimally, trying to make its height as large as possible. Lowie chooses the root of his tree adversarially from B21's perspective, so B21 only needs to know whether there exists some root for Lowie's tree that makes B21's resulting height strictly larger.

The height of a rooted tree is measured in vertices on the longest root-to-vertex path. It is convenient to work with distances measured in edges instead. If the longest distance from the root to any vertex is `h` edges, the tree height is `h + 1` vertices. The extra `1` appears in both trees, so it disappears when we compare their heights.

For B21, maximizing the height over all possible roots is exactly the same as finding the tree's diameter. If the diameter has `D` edges, choosing a diameter endpoint as the root gives a height of `D + 1`.

For Lowie, we need the opposite quantity. B21 wants to know whether there is some root that makes Lowie's height as small as possible. The minimum possible maximum distance from a root to every vertex is the tree's radius, which is `ceil(D / 2)` when the diameter is `D`. Thus Lowie's best possible height from B21's point of view is `ceil(D / 2) + 1`.

The input contains B21's tree followed by Lowie's tree. A tree with `N` vertices has `N - 1` edges, despite the archived statement text saying `N` edge lines. The examples use `N - 1` edges, which is the only format consistent with the definition of a tree, so the implementation reads `N - 1` and `M - 1` edges.

The limits are large enough that quadratic traversal is impossible. With up to `10^5` vertices in B21's tree and `2 * 10^5` vertices in Lowie's tree, an `O(N^2 + M^2)` method can require around `10^11` adjacency visits. The official limit is only 1 second with 256 MB of memory, so the intended solution must process each tree in linear time.

The first edge case is a single-vertex B21 tree.

```
1
2
1 2
```

B21's diameter is zero edges, so his maximum height is `1`. Lowie's tree has diameter one edge, so even its minimum possible height is `2`. B21 cannot win, and the answer is `FF`. A careless implementation that assumes every tree has at least one edge may fail when its DFS starts from a nonexistent neighbor or when it initializes the diameter to `1`.

The second edge case is a draw at exactly the boundary.

```
4
1 2
2 3
3 4
7
1 2
2 3
3 4
4 5
5 6
6 7
```

B21's diameter is `3`, while Lowie's diameter is `6`. Lowie's minimum radius is `ceil(6 / 2) = 3`, so both players can obtain height `4`. The correct answer is `FF`, because a draw does not count as a win. A careless implementation using `>=` instead of `>` would incorrectly print `GGEZ`.

The third edge case is an odd diameter.

```
4
1 2
2 3
3 4
6
1 2
2 3
3 4
4 5
5 6
```

The diameters are `3` and `5`. Lowie's minimum radius is `ceil(5 / 2) = 3`, so both maximum and minimum relevant heights are `4`. The answer is again `FF`. This catches implementations that accidentally use integer division `D / 2` instead of ceiling division `(D + 1) / 2`.

## Approaches

A direct solution would try every possible root. For each root, run a DFS or BFS and find the farthest vertex. Taking the maximum of these values gives B21's best height, while taking the minimum gives the best root Lowie could accidentally choose. This is correct because the definition of tree height is exactly the maximum distance from the selected root.

The problem is the repeated traversal. A traversal of an `N`-vertex tree examines `2(N - 1)` adjacency entries. Running it once for every root therefore takes `2N(N - 1)` adjacency visits. Doing the same for Lowie's tree gives another `2M(M - 1)`. At `N = 10^5` and `M = 2 * 10^5`, this is about `99,999,400,000` adjacency visits, far beyond the time limit.

The brute-force approach works because each root independently determines one tree height, but we do not actually need to inspect every root. The structure of a tree gives us two global quantities that summarize exactly what we need.

The maximum height obtainable by changing the root is the diameter. If the diameter endpoints are `a` and `b`, rooting at `a` reaches `b` at the maximum possible distance, so the resulting height is the diameter plus one.

The minimum height obtainable by changing the root is the radius. Every vertex must be close to the chosen root, and the best possible root is a center of the tree. A center lies halfway along a diameter, so for diameter `D` the minimum possible maximum distance is `ceil(D / 2)`.

This reduces the whole problem to computing two diameters. A tree diameter can be found with two graph traversals. Start from any vertex and find a farthest vertex `a`. Then start from `a` and find a farthest vertex `b`. The distance from `a` to `b` is the diameter.

Let `D_B` be B21's diameter in edges and `D_L` be Lowie's diameter in edges. B21 wins exactly when

`D_B + 1 > ceil(D_L / 2) + 1`

which simplifies to

`D_B > ceil(D_L / 2)`.

The resulting comparison is linear in the sizes of the two trees. This is also the approach described by the official contest editorial, which reduces the problem to the maximum and minimum possible tree heights and computes the required diameters with two traversals per tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N² + M²)` | `O(N + M)` | Too slow |
| Optimal | `O(N + M)` | `O(N + M)` | Accepted |

## Algorithm Walkthrough

1. Read B21's tree and build its adjacency list. A tree with `N` vertices has exactly `N - 1` edges, so those are the edges that belong to B21's graph.
2. Compute B21's diameter with two traversals. Start from any vertex, find a farthest vertex `a`, then start from `a` and find the farthest vertex `b`. The distance from `a` to `b` is `D_B`, the diameter in edges.
3. Read Lowie's tree and build its adjacency list. The same tree property means it contains `M - 1` edges.
4. Compute Lowie's diameter `D_L` using the same two-traversal method.
5. Convert Lowie's diameter into the smallest possible maximum distance from a root. A root at the center of a diameter minimizes its farthest distance, giving radius `ceil(D_L / 2)`. In integer arithmetic this is `(D_L + 1) // 2`.
6. Compare B21's maximum distance `D_B` with Lowie's minimum possible maximum distance. B21 wins exactly when `D_B > (D_L + 1) // 2`. The strict inequality is necessary because equality produces a draw.
7. Print `GGEZ` when the inequality holds and `FF` otherwise.

### Why it works

The key invariant is that every rooted tree height can be expressed as one plus the maximum edge distance from its root. The largest such value over all roots is the diameter plus one, because a diameter endpoint can reach the opposite endpoint at the diameter distance. The smallest such value is the radius plus one, and every tree center has eccentricity `ceil(D / 2)`, where `D` is the diameter. Thus B21 has a winning root choice exactly when his diameter is strictly greater than Lowie's radius. The two-traversal procedure computes each diameter exactly, so the final comparison cannot miss a possible winning root or declare a win when only a draw is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def diameter(graph):
    n = len(graph)

    def farthest(start):
        dist = [-1] * n
        dist[start] = 0
        stack = [start]
        far = start

        while stack:
            u = stack.pop()
            if dist[u] > dist[far]:
                far = u

            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    stack.append(v)

        return far, dist[far]

    if n == 1:
        return 0

    a, _ = farthest(0)
    _, d = farthest(a)
    return d

def solve():
    n = int(input())
    b21 = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        b21[u].append(v)
        b21[v].append(u)

    m = int(input())
    lowie = [[] for _ in range(m)]

    for _ in range(m - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        lowie[u].append(v)
        lowie[v].append(u)

    db = diameter(b21)
    dl = diameter(lowie)

    lowie_radius = (dl + 1) // 2

    if db > lowie_radius:
        print("GGEZ")
    else:
        print("FF")

if __name__ == "__main__":
    solve()
```

The `diameter` function performs exactly the two traversals described in the walkthrough. The first traversal only needs to identify a farthest vertex, while the second traversal records the distance from that vertex to every reachable vertex and returns the largest one.

The graph is a tree, so a simple iterative DFS is enough. BFS is not required because every edge has the same unit cost and we only need the farthest distance in an unweighted tree. Using an explicit stack also avoids Python recursion-depth problems on a path containing `10^5` or `2 * 10^5` vertices.

The `n == 1` check is necessary because a one-vertex tree has diameter zero. The first traversal would still work, but handling this case explicitly makes the definition clear and avoids relying on the behavior of the generic farthest-node logic for an empty adjacency list.

The conversion from diameter to radius uses `(dl + 1) // 2`. For an even diameter such as `6`, this gives `3`. For an odd diameter such as `5`, it gives `3`, which is the required ceiling rather than the floor.

The final comparison is strict. If `db == lowie_radius`, the resulting heights are equal, so the output must be `FF`.

The vertex indices are converted from one-based input to zero-based Python indices. No integer overflow is possible in Python, and all distances are at most `2 * 10^5 - 1`.

## Worked Examples

### Sample 1

B21's tree has edges

```
1-2, 1-3, 2-4, 2-5
```

The first traversal can start at vertex `1`. One possible farthest vertex is `4`, at distance `2`. Starting from `4`, the farthest vertex is `3`, at distance `3`. Thus B21's diameter is `3`.

For Lowie's tree, start at `1`. A possible farthest vertex is `5`, at distance `2`. Starting from `5`, vertex `7` is at distance `4`, giving Lowie's diameter `4`. Its radius is `ceil(4 / 2) = 2`.

| Tree | First start | First farthest | Second start | Second farthest | Diameter | Radius |
| --- | --- | --- | --- | --- | --- | --- |
| B21 | 1 | 4 | 4 | 3 | 3 | not needed |
| Lowie | 1 | 5 | 5 | 7 | 4 | 2 |

The comparison is `3 > 2`, so B21 can choose a diameter endpoint as his root and obtain a height strictly larger than Lowie's height under the favorable root choice. The answer is `GGEZ`.

### Sample 2

B21's tree is unchanged, so its diameter remains `3`.

For Lowie's tree, starting from `1`, one farthest vertex can be `5`. Starting from `5`, vertex `7` is at distance `6`, so Lowie's diameter is `6`. Its radius is `ceil(6 / 2) = 3`.

| Tree | First start | First farthest | Second start | Second farthest | Diameter | Radius |
| --- | --- | --- | --- | --- | --- | --- |
| B21 | 1 | 4 | 4 | 3 | 3 | not needed |
| Lowie | 1 | 5 | 5 | 7 | 6 | 3 |

Now the comparison is `3 > 3`, which is false. Both players can obtain height `4`, so the result is a draw and the answer is `FF`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N + M)` | Each tree is traversed twice, and every traversal examines every vertex and edge a constant number of times. |
| Space | `O(N + M)` | The two adjacency lists and traversal distance arrays store a linear number of vertices and edges. |

The largest tree has `2 * 10^5` vertices, so the algorithm performs only a constant number of linear passes over roughly `3 * 10^5` vertices and their edges. This fits the intended 1 second and 256 MB limits far more comfortably than the quadratic brute-force method.

## Test Cases

The following test harness uses the same `solve` implementation and replaces standard input and output so each case can be checked with an assertion.

```python
import sys
import io
from contextlib import redirect_stdout

def diameter(graph):
    n = len(graph)

    def farthest(start):
        dist = [-1] * n
        dist[start] = 0
        stack = [start]
        far = start

        while stack:
            u = stack.pop()

            if dist[u] > dist[far]:
                far = u

            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    stack.append(v)

        return far, dist[far]

    if n == 1:
        return 0

    a, _ = farthest(0)
    _, d = farthest(a)
    return d

def solve():
    input = sys.stdin.readline

    n = int(input())
    b21 = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        b21[u].append(v)
        b21[v].append(u)

    m = int(input())
    lowie = [[] for _ in range(m)]

    for _ in range(m - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        lowie[u].append(v)
        lowie[v].append(u)

    db = diameter(b21)
    dl = diameter(lowie)

    if db > (dl + 1) // 2:
        print("GGEZ")
    else:
        print("FF")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    output = io.StringIO()
    try:
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin

    return output.getvalue().strip()

# Provided sample 1
sample1 = """\
5
1 2
1 3
2 4
2 5
7
1 2
2 5
3 6
2 4
1 3
3 7
"""
assert run(sample1) == "GGEZ", "sample 1"

# Provided sample 2
sample2 = """\
5
1 2
1 3
2 4
2 5
7
1 2
1 3
3 4
4 5
2 6
6 7
"""
assert run(sample2) == "FF", "sample 2"

# Minimum-size B21 tree
case_min = """\
1
2
1 2
"""
assert run(case_min) == "FF", "single vertex B21 tree"

# Exact draw boundary
case_draw = """\
4
1 2
2 3
3 4
7
1 2
2 3
3 4
4 5
5 6
6 7
"""
assert run(case_draw) == "FF", "equal B21 diameter and Lowie radius"

# Odd Lowie diameter
case_odd = """\
4
1 2
2 3
3 4
6
1 2
2 3
3 4
4 5
5 6
"""
assert run(case_odd) == "FF", "odd diameter requires ceiling"

# Branching tree with a very small diameter
case_star = """\
3
1 2
1 3
4
1 2
1 3
1 4
"""
assert run(case_star) == "GGEZ", "star-shaped trees"

# Maximum-size generated case
def make_max_case():
    n = 100000
    m = 200000

    parts = [str(n)]
    for i in range(1, n):
        parts.append(f"{i} {i + 1}")

    parts.append(str(m))
    for i in range(1, m):
        parts.append(f"{i} {i + 1}")

    return "\n".join(parts) + "\n"

max_case = make_max_case()
assert run(max_case) == "FF", "maximum-size paths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` vertex versus a 2-vertex tree | `FF` | Minimum-size tree and zero diameter |
| B21 path of 4 versus Lowie path of 7 | `FF` | Exact equality between B21 diameter and Lowie radius |
| B21 path of 4 versus Lowie path of 6 | `FF` | Ceiling division for an odd diameter |
| Two stars | `GGEZ` | Branching trees and small diameter |
| Paths with `100000` and `200000` vertices | `FF` | Maximum constraints and linear-time behavior |

## Edge Cases

For the single-vertex case, B21's tree has no edges, so `D_B = 0`. Lowie's two-vertex tree has `D_L = 1`, giving radius `(1 + 1) // 2 = 1`. The comparison becomes `0 > 1`, which is false, so the algorithm prints `FF`. The explicit `n == 1` branch in `diameter` returns zero directly.

For the exact draw boundary, consider

```
4
1 2
2 3
3 4
7
1 2
2 3
3 4
4 5
5 6
6 7
```

The first tree has diameter `3`. The second has diameter `6`, so its radius is `(6 + 1) // 2 = 3`. The final test is `3 > 3`, which is false. The strict comparison correctly rejects a draw.

For an odd Lowie diameter, consider

```
4
1 2
2 3
3 4
6
1 2
2 3
3 4
4 5
5 6
```

B21's diameter is `3`. Lowie's diameter is `5`, and the best root is one of the two central vertices, giving radius `3`. The expression `(5 + 1) // 2` produces `3`, so the algorithm correctly handles the ceiling operation. Since `3 > 3` is false, it prints `FF`.

For a branching tree, consider

```
3
1 2
1 3
4
1 2
1 3
1 4
```

Both trees are stars. Their diameters are `2`, so Lowie's radius is `1`. B21's diameter `2` is strictly larger than `1`, and the algorithm prints `GGEZ`. This demonstrates why the solution depends only on the diameter, not on whether the tree is a path or has many branches.

For the maximum-size case, both trees are paths, with `100000` and `200000` vertices respectively. Their diameters are `99999` and `199999`. Lowie's radius is `(199999 + 1) // 2 = 100000`, while B21's diameter is only `99999`, so the answer is `FF`. The implementation processes the entire input with four linear traversals and never constructs a quadratic distance matrix, which is exactly the behavior required by the constraints.
