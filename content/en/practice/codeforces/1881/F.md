---
title: "CF 1881F - Minimum Maximum Distance"
description: "We are given a tree and a subset of its vertices marked as special. For every vertex $v$, define $f(v)$ as the distance from $v$ to the farthest marked vertex. We want to choose a vertex whose farthest marked vertex is as close as possible."
date: "2026-06-08T22:42:23+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 1881
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 903 (Div. 3)"
rating: 1700
weight: 1881
solve_time_s: 140
verified: true
draft: false
---

[CF 1881F - Minimum Maximum Distance](https://codeforces.com/problemset/problem/1881/F)

**Rating:** 1700  
**Tags:** dfs and similar, dp, graphs, shortest paths, trees  
**Solve time:** 2m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree and a subset of its vertices marked as special.

For every vertex $v$, define $f(v)$ as the distance from $v$ to the farthest marked vertex. We want to choose a vertex whose farthest marked vertex is as close as possible. The answer is the minimum value of $f(v)$ over all vertices.

Viewed differently, imagine all marked vertices as important locations. For each candidate vertex, look at the worst distance to any marked vertex. We need the vertex that minimizes this worst-case distance.

The tree can contain up to $2 \cdot 10^5$ vertices across all test cases. Any algorithm that performs a traversal from every vertex would require $O(n^2)$ work in the worst case, which is far beyond what fits in two seconds. We need a solution close to linear time per test case.

Several edge cases are easy to mishandle.

Consider a tree with only one marked vertex:

```
1
5 1
3
1 2
2 3
3 4
4 5
```

The correct answer is `0`, because choosing vertex 3 gives distance 0 to the only marked vertex. A solution that assumes two endpoints always exist would fail here.

Consider a path where every vertex is marked:

```
1
4 4
1 2 3 4
1 2
2 3
3 4
```

The answer is `2`. The best vertices are 2 and 3, whose farthest marked vertex is at distance 2. Looking only at nearby marked vertices would miss the influence of the endpoints.

Another subtle case is when the marked vertices form a small cluster inside a large tree:

```
1
7 2
3 4
1 2
2 3
3 4
4 5
5 6
6 7
```

The answer is `1`. The optimal vertices are 3 and 4. A careless approach that tries to balance distances to all vertices instead of only marked vertices would produce a larger value.

## Approaches

A direct solution is to compute $f(v)$ for every vertex separately.

For a fixed vertex $v$, we could run BFS or DFS to obtain distances to all vertices, then take the maximum distance among marked vertices. Repeating this for every vertex gives $O(n^2)$ time on a tree. With $n = 2 \cdot 10^5$, this would require roughly $4 \cdot 10^{10}$ operations in the worst case.

The key observation is that we do not care about all marked vertices individually. We only care about the farthest one.

Suppose we look only at the marked vertices and find two marked vertices whose distance is maximum among all marked pairs. Call them $A$ and $B$. They form the diameter of the marked set.

Now consider any vertex $v$. Let

$$d_A(v)=\operatorname{dist}(v,A)$$

and

$$d_B(v)=\operatorname{dist}(v,B).$$

A crucial property of trees is that for every marked vertex $x$,

$$\operatorname{dist}(v,x)
\le
\max(d_A(v), d_B(v)).$$

This means the farthest marked vertex from $v$ is always one of the two diameter endpoints.

Therefore

$$f(v)=\max(d_A(v), d_B(v)).$$

Once the diameter endpoints are known, we only need distances from $A$ and from $B$. Then we evaluate the above expression for every vertex and take the minimum.

The remaining question is how to find the marked diameter. This is the standard double-DFS trick, slightly modified.

Start from any marked vertex and find the farthest marked vertex $A$. Then start from $A$ and find the farthest marked vertex $B$. The path between $A$ and $B$ is the diameter among marked vertices.

After that, one DFS from $A$ and one DFS from $B$ provide all required distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the tree and the list of marked vertices.
2. Pick any marked vertex as a starting point.
3. Run a DFS from this vertex and compute distances to every vertex.
4. Among all marked vertices, choose the one with maximum distance. Call it $A$.

This vertex must be an endpoint of the marked diameter.
5. Run another DFS from $A$.
6. Among all marked vertices, choose the one farthest from $A$. Call it $B$.

The pair $(A,B)$ forms a diameter of the marked vertices.
7. Store all distances from $A$. Call this array `distA`.
8. Run a third DFS from $B$ and store all distances in `distB`.
9. For every vertex $v$, compute

$$\max(\text{distA}[v], \text{distB}[v]).$$

This equals the distance from $v$ to its farthest marked vertex.
10. Take the minimum value among all vertices and output it.

### Why it works

Let $A$ and $B$ be endpoints of the diameter of the marked vertices.

For any marked vertex $x$, diameter maximality implies

$$\operatorname{dist}(A,x)\le \operatorname{dist}(A,B)$$

and

$$\operatorname{dist}(B,x)\le \operatorname{dist}(A,B).$$

A standard tree-diameter property states that for every vertex $v$, the farthest marked vertex from $v$ must be one of the diameter endpoints. Consequently,

$$\max_{x \text{ marked}} \operatorname{dist}(v,x)
=
\max(
\operatorname{dist}(v,A),
\operatorname{dist}(v,B)
).$$

The algorithm computes exactly these two distances for every vertex and minimizes their maximum. Since every candidate value is computed correctly, the minimum is also correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        marked = list(map(int, input().split()))

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        def distances(start):
            dist = [-1] * (n + 1)
            dist[start] = 0

            stack = [start]

            while stack:
                v = stack.pop()

                for to in g[v]:
                    if dist[to] == -1:
                        dist[to] = dist[v] + 1
                        stack.append(to)

            return dist

        start = marked[0]

        dist0 = distances(start)

        A = max(marked, key=lambda x: dist0[x])

        distA = distances(A)

        B = max(marked, key=lambda x: distA[x])

        distB = distances(B)

        ans = min(max(distA[v], distB[v]) for v in range(1, n + 1))

        print(ans)

solve()
```

The helper function `distances()` performs an iterative DFS and returns distances from one source to every vertex. Iterative traversal is safer than recursive DFS because the tree can contain up to $2 \cdot 10^5$ vertices, which would exceed Python's recursion depth.

The first traversal finds a marked vertex that lies at one end of the marked diameter. The second traversal identifies the opposite endpoint. These are exactly the same steps used to find a tree diameter, except that the farthest vertex is chosen only among marked vertices.

The third traversal is necessary because we need distances from both diameter endpoints simultaneously. Once `distA` and `distB` are available, the expression `max(distA[v], distB[v])` gives the farthest marked distance for vertex `v`.

A common mistake is to minimize `distA[v] + distB[v]` or some other combination. The problem asks for the worst marked distance, so the correct expression is the maximum of the two endpoint distances.

## Worked Examples

### Example 1

```
7 3
Marked: 2 6 7
```

The tree is:

```
    1
   / \
  2   3
 / \ / \
4  5 6  7
```

The marked diameter endpoints are 2 and 6.

| Vertex | distA (from 2) | distB (from 6) | max |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 2 |
| 2 | 0 | 3 | 3 |
| 3 | 2 | 1 | 2 |
| 4 | 1 | 4 | 4 |
| 5 | 1 | 4 | 4 |
| 6 | 3 | 0 | 3 |
| 7 | 3 | 2 | 3 |

The minimum value in the last column is `2`, achieved by vertices 1 and 3.

This example shows the central property of the solution. Once the diameter endpoints are known, every vertex's answer comes from those two distances alone.

### Example 2

```
4 4
Marked: 1 2 3 4
1-2-3-4
```

The marked diameter endpoints are 1 and 4.

| Vertex | distA | distB | max |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 3 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 1 | 2 |
| 4 | 3 | 0 | 3 |

The minimum value is `2`.

This demonstrates that when every vertex is marked, the problem reduces to finding the center of the diameter path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Three full tree traversals and linear scans |
| Space | $O(n)$ | Adjacency list and distance arrays |

The sum of all $n$ values across test cases is at most $2 \cdot 10^5$. Linear processing per test case means the total work is also linear in the overall input size, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        marked = list(map(int, input().split()))

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        def distances(start):
            dist = [-1] * (n + 1)
            dist[start] = 0
            stack = [start]

            while stack:
                v = stack.pop()
                for to in g[v]:
                    if dist[to] == -1:
                        dist[to] = dist[v] + 1
                        stack.append(to)

            return dist

        d0 = distances(marked[0])
        A = max(marked, key=lambda x: d0[x])

        dA = distances(A)
        B = max(marked, key=lambda x: dA[x])

        dB = distances(B)

        out.append(str(min(max(dA[i], dB[i]) for i in range(1, n + 1))))

    return "\n".join(out)

# provided sample
assert run(
"""6
7 3
2 6 7
1 2
1 3
2 4
2 5
3 6
3 7
4 4
1 2 3 4
1 2
2 3
3 4
5 1
1
1 2
1 3
1 4
1 5
5 2
4 5
1 2
2 3
1 4
4 5
10 8
1 2 3 4 5 8 9 10
2 10
10 5
5 3
3 1
1 7
7 4
4 9
8 9
6 1
10 9
1 2 4 5 6 7 8 9 10
1 3
3 9
9 4
4 10
10 6
6 7
7 2
2 5
5 8
"""
) == "2\n2\n0\n1\n4\n5"

# single vertex
assert run(
"""1
1 1
1
"""
) == "0"

# path with one marked endpoint
assert run(
"""1
5 1
5
1 2
2 3
3 4
4 5
"""
) == "0"

# two marked endpoints of a path
assert run(
"""1
5 2
1 5
1 2
2 3
3 4
4 5
"""
) == "2"

# star centered at marked vertex
assert run(
"""1
5 1
1
1 2
1 3
1 4
1 5
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex tree | 0 | Smallest possible input |
| One marked endpoint on path | 0 | Handling $k=1$ |
| Path with marked endpoints | 2 | Diameter-center behavior |
| Star with marked center | 0 | Distances from unique marked node |

## Edge Cases

Consider a single marked vertex.

```
1
5 1
3
1 2
2 3
3 4
4 5
```

The first diameter search finds vertex 3. The second search also finds vertex 3. Thus $A=B=3$. Every vertex uses `max(distA, distB)`, which is simply its distance to vertex 3. The minimum occurs at vertex 3 and equals 0.

Consider all vertices marked on a path.

```
1
4 4
1 2 3 4
1 2
2 3
3 4
```

The marked diameter is the whole path, with endpoints 1 and 4. Distances from those endpoints correctly identify vertices 2 and 3 as centers. The answer becomes 2.

Consider marked vertices concentrated in one region.

```
1
7 2
3 4
1 2
2 3
3 4
4 5
5 6
6 7
```

The diameter endpoints are 3 and 4. Distances from these endpoints give:

| Vertex | max(dist(3), dist(4)) |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 3 |
| 7 | 4 |

The minimum is 1, achieved at vertices 3 and 4. The algorithm focuses only on marked vertices, exactly as required by the problem definition.
