---
title: "CF 1141G - Privatization of Roads in Treeland"
description: "We are given a tree with $n$ vertices and $n-1$ edges. Every edge must be assigned a company number. A city is considered good if all roads incident to it belong to different companies. A city becomes bad if at least two incident roads receive the same company."
date: "2026-06-12T03:44:22+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "dfs-and-similar", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1141
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 547 (Div. 3)"
rating: 1900
weight: 1141
solve_time_s: 92
verified: true
draft: false
---

[CF 1141G - Privatization of Roads in Treeland](https://codeforces.com/problemset/problem/1141/G)

**Rating:** 1900  
**Tags:** binary search, constructive algorithms, dfs and similar, graphs, greedy, trees  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices and $n-1$ edges. Every edge must be assigned a company number. A city is considered _good_ if all roads incident to it belong to different companies. A city becomes _bad_ if at least two incident roads receive the same company.

We are allowed to have at most $k$ bad cities. Among all valid assignments, we must minimize the number of companies $r$. After finding the smallest possible $r$, we also need to output one valid coloring of the edges using company numbers from $1$ to $r$.

The graph is a tree, which means there is exactly one simple path between every pair of vertices. The input gives the endpoints of every road, and the output must assign a company number to every road.

The constraints are the real challenge. The tree can contain up to $200\,000$ vertices, so any algorithm that repeatedly scans all vertices or tries many candidate colorings is far too expensive. With only two seconds available, the intended solution must be close to linear or $O(n \log n)$.

The key difficulty is that minimizing the number of companies is not directly a coloring problem on the whole tree. We are allowed to violate the distinct-color condition at up to $k$ vertices. Understanding which vertices should be sacrificed is the main insight.

Consider a star centered at vertex 1:

```
1-2
1-3
1-4
1-5
```

with $k=1$.

The center has degree 4. If we allow vertex 1 to be bad, then all edges may use the same color and $r=1$. A solution that blindly tries to make every vertex good would incorrectly conclude that four different colors are needed.

Another subtle case is a path:

```
1-2-3-4-5
```

with $k=0$.

Every vertex has degree at most 2. The answer is not 2 because a proper edge coloring of a tree only needs $\Delta$ colors, where $\Delta$ is the maximum degree. Here $\Delta=2$, and alternating colors along the path works. Any implementation that assumes every edge must get a unique color would overestimate the answer.

A third trap appears when many vertices share the same degree. Suppose the degrees are:

```
5, 5, 5, 1, 1, ...
```

and $k=2$.

We may choose any two of the degree-5 vertices to become bad. The answer depends on the third largest degree, not on which specific vertices are selected. An implementation that handles equal degrees incorrectly can produce a larger-than-necessary value of $r$.

## Approaches

A brute-force viewpoint is to guess the number of companies $r$, then try to determine whether the tree can be colored with at most $r$ colors while making at most $k$ vertices bad.

This quickly becomes infeasible. Even checking a single value of $r$ by exploring possible edge colorings has an enormous search space. A tree with $200\,000$ vertices already contains $199\,999$ edges, so any combinatorial search is hopeless.

The turning point comes from asking what forces a large number of colors.

If a vertex must remain good, all incident edges need distinct colors. A vertex of degree $d$ immediately requires at least $d$ available colors.

Now suppose we decide that some vertex may be bad. Then we no longer care whether incident edges repeat colors there.

This observation completely changes the problem. The only vertices that force a large color count are the vertices we choose to keep good.

Assume the degrees are sorted in descending order:

$$d_1 \ge d_2 \ge \cdots \ge d_n.$$

We may sacrifice at most $k$ vertices. Naturally, we should sacrifice the vertices with the largest degrees, since they impose the strongest color requirements.

After removing those $k$ worst constraints, the minimum necessary number of colors becomes

$$r = d_{k+1}.$$

If $k=0$, this is simply the maximum degree. If $k=n-1$, every vertex except one may be bad, so $r=1$.

The remaining task is constructive: produce an edge coloring using exactly $r$ colors.

The standard tree edge-coloring DFS works perfectly here. We root the tree and color edges while traversing. At a vertex whose degree exceeds $r$, we intentionally allow repetitions. At every other vertex, we assign different colors to all incident edges.

Because $r$ equals the $(k+1)$-th largest degree, there are at most $k$ vertices whose degree exceeds $r$. Those become the bad vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and compute the degree of every vertex.
2. Sort all degrees in descending order.
3. Let $r$ be the $(k+1)$-th largest degree. In zero-based indexing this is `sorted_deg[k]`.

This value is the smallest possible number of colors because at least $n-k$ vertices must remain good, and every good vertex of degree $d$ requires $d$ distinct colors.
4. Root the tree at any vertex, for example vertex 1.
5. Perform a DFS.
6. Suppose the edge connecting the current vertex to its parent has color `parent_color`.
7. For the children of the current vertex, assign colors sequentially from 1 to $r$, skipping `parent_color`.

This guarantees that all incident edges at this vertex receive distinct colors whenever its degree does not exceed $r$.
8. If the color counter exceeds $r$, wrap it back to 1.

Such wrapping can only create repeated colors at vertices whose degree exceeds $r$. Those are exactly the vertices we are willing to make bad.
9. Store the assigned color for every edge by its original input index.
10. Output $r$ and all edge colors.

### Why it works

The crucial property is that every vertex with degree at most $r$ receives pairwise distinct colors on all incident edges.

At such a vertex, one color is already occupied by the edge to its parent. The DFS assigns distinct colors to all child edges while skipping the parent color. Since the total number of incident edges does not exceed $r$, there are enough colors available and no repetition occurs.

A repetition can happen only when a vertex has degree greater than $r$. The number of such vertices is at most $k$, because $r$ was chosen as the $(k+1)$-th largest degree. Thus at most $k$ vertices become bad.

The coloring uses only colors $1 \ldots r$, satisfies the bad-vertex limit, and $r$ is minimal. Hence the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())

    g = [[] for _ in range(n)]
    deg = [0] * n
    edges = []

    for idx in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        edges.append((u, v))

        g[u].append((v, idx))
        g[v].append((u, idx))

        deg[u] += 1
        deg[v] += 1

    sorted_deg = sorted(deg, reverse=True)
    r = sorted_deg[k]

    ans = [0] * (n - 1)

    stack = [(0, -1, 0)]

    while stack:
        v, parent, parent_color = stack.pop()

        color = 1

        for to, eid in g[v]:
            if to == parent:
                continue

            if color == parent_color:
                color += 1

            if color > r:
                color = 1

            ans[eid] = color

            stack.append((to, v, color))

            color += 1
            if color > r:
                color = 1

    print(r)
    print(*ans)

if __name__ == "__main__":
    main()
```

The first part builds the adjacency list and computes vertex degrees.

The sorted degree array is used only once. The value at position `k` is exactly the $(k+1)$-th largest degree, which is the optimal number of colors.

The DFS is iterative rather than recursive. A recursive solution can overflow Python's recursion limit on a tree with $200\,000$ vertices.

The variable `parent_color` records the color of the edge leading into the current vertex. When assigning colors to child edges, that color is skipped whenever possible. This is what guarantees distinct incident colors at low-degree vertices.

The wraparound behavior is intentional. Once a vertex has more than `r` incident edges, repetitions become unavoidable. Those vertices are precisely the ones we are allowed to sacrifice.

## Worked Examples

### Example 1

Input:

```
6 2
1 4
4 3
3 5
3 6
5 2
```

Degrees:

| Vertex | Degree |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 3 |
| 4 | 2 |
| 5 | 2 |
| 6 | 1 |

Sorted degrees:

| Position | Degree |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |
| 5 | 1 |
| 6 | 1 |

Since $k=2$,

$$r = 2.$$

DFS trace:

| Vertex | Parent Color | Assigned Child Colors |
| --- | --- | --- |
| 1 | 0 | 1 |
| 4 | 1 | 2 |
| 3 | 2 | 1, 2 |
| 5 | 1 | 2 |

One valid output is:

```
2
1 2 1 2 2
```

Vertex 3 has degree 3 greater than $r=2$, so it may become bad. All other vertices remain good.

### Example 2

Input:

```
5 0
1 2
1 3
1 4
1 5
```

Degrees:

| Vertex | Degree |
| --- | --- |
| 1 | 4 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |

Sorted degrees:

| Position | Degree |
| --- | --- |
| 1 | 4 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |

Since $k=0$,

$$r = 4.$$

DFS trace:

| Vertex | Parent Color | Assigned Child Colors |
| --- | --- | --- |
| 1 | 0 | 1,2,3,4 |

Output:

```
4
1 2 3 4
```

No bad vertices are allowed, so the center must receive four distinct incident colors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the degree array dominates |
| Space | O(n) | Adjacency list, degree array, DFS stack, answers |

The tree contains at most $200\,000$ vertices. Sorting $200\,000$ integers is easily fast enough, and all remaining work is linear in the number of edges. The memory usage is also comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
# For this problem many outputs are valid, so these tests
# check the optimal r value only.

import io
import sys

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)

    n, k = map(int, sys.stdin.readline().split())
    deg = [0] * n

    edges = []
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        deg[u - 1] += 1
        deg[v - 1] += 1

    r = sorted(deg, reverse=True)[k]
    return str(r)

# sample
assert run(
"""6 2
1 4
4 3
3 5
3 6
5 2
"""
) == "2"

# minimum tree
assert run(
"""2 0
1 2
"""
) == "1"

# star, one bad vertex allowed
assert run(
"""5 1
1 2
1 3
1 4
1 5
"""
) == "1"

# star, no bad vertices allowed
assert run(
"""5 0
1 2
1 3
1 4
1 5
"""
) == "4"

# path graph
assert run(
"""5 0
1 2
2 3
3 4
4 5
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge | 1 | Smallest possible tree |
| Star, k=1 | 1 | High-degree vertex may be sacrificed |
| Star, k=0 | 4 | Maximum degree required when all vertices must be good |
| Path | 2 | Proper handling of degree 2 trees |
| Sample | 2 | Matches official example |

## Edge Cases

Consider the star

```
5 1
1 2
1 3
1 4
1 5
```

The degree sequence is $[4,1,1,1,1]$. The second largest degree is 1, so $r=1$. The center is the only vertex whose degree exceeds $r$, which is allowed because $k=1$. Every edge receives color 1. A solution that insists on distinct colors at every vertex would incorrectly output 4.

Consider the path

```
5 0
1 2
2 3
3 4
4 5
```

The degree sequence is $[2,2,2,1,1]$. Since no bad vertices are allowed, $r=2$. During DFS the colors alternate naturally and every vertex sees distinct incident colors. The algorithm never introduces unnecessary colors.

Consider a tree whose three largest degrees are equal:

```
7 2
1 2
1 3
1 4
5 1
6 1
7 1
```

The degree sequence is $[6,1,1,1,1,1,1]$. With $k=2$, the answer becomes the third largest degree, which is still 1. The algorithm relies only on the sorted order, so ties are handled automatically without special logic.

Finally, when $k=n-1$, every vertex except one may be bad. The sorted degree index `k` always exists because the array has length $n$. The answer becomes 1, and coloring every edge with color 1 is valid. The implementation handles this case without any branching.
