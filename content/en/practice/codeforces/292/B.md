---
title: "CF 292B - Network Topology"
description: "We are given a connected undirected graph representing a computer network. The task is not to analyze arbitrary graph structure, but to determine whether the graph exactly matches one of three specific topologies. A bus topology is simply a path."
date: "2026-06-05T17:19:26+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1200
weight: 292
solve_time_s: 111
verified: true
draft: false
---

[CF 292B - Network Topology](https://codeforces.com/problemset/problem/292/B)

**Rating:** 1200  
**Tags:** graphs, implementation  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected graph representing a computer network. The task is not to analyze arbitrary graph structure, but to determine whether the graph exactly matches one of three specific topologies.

A bus topology is simply a path. Exactly two vertices are endpoints with degree 1, and every other vertex has degree 2.

A ring topology is a cycle. Every vertex has degree 2.

A star topology has one central vertex connected to all others. The center has degree $n-1$, and every remaining vertex has degree 1.

The graph is guaranteed to be connected, so we do not need to verify connectivity ourselves. We only need to inspect the degree pattern of the vertices and decide which topology matches.

The constraints allow up to $10^5$ vertices and $10^5$ edges. Any algorithm that repeatedly traverses the graph or performs expensive pairwise checks would be unnecessary. Since the entire input contains only $O(m)$ edge information, a linear scan over the edges and vertices is the natural target. An $O(n+m)$ solution easily fits within the limits, while anything quadratic would be far too large for $10^5$ vertices.

Several edge cases can cause incorrect classifications if we only look at the number of edges.

Consider:

```
4 3
1 2
1 3
1 4
```

The graph has $n-1$ edges, just like a path, but its degree sequence is $[3,1,1,1]$. The correct answer is:

```
star topology
```

A solution that only checks whether $m=n-1$ would incorrectly call this a bus.

Another example is:

```
4 4
1 2
2 3
3 4
4 1
```

Every vertex has degree 2, so this is:

```
ring topology
```

Looking only at connectivity and edge count is not enough. We must inspect vertex degrees.

A final example:

```
5 5
1 2
2 3
3 4
4 5
2 5
```

The degrees are $[1,3,2,2,2]$. This graph is connected but matches none of the required structures.

The correct answer is:

```
unknown topology
```

## Approaches

A brute-force approach would attempt to recognize each topology by explicitly reconstructing its shape. For example, we could start from every vertex, walk through neighbors, verify whether the graph forms a single path, a cycle, or a star. Since the graph is connected, such traversals are correct, but they involve more graph logic than necessary.

In the worst case, repeatedly performing graph walks or topology checks could approach $O(n(n+m))$, which is far larger than needed when $n$ reaches $10^5$.

The key observation is that all three topologies are completely characterized by vertex degrees.

For a ring, every vertex has degree 2.

For a bus, exactly two vertices have degree 1 and every remaining vertex has degree 2.

For a star, exactly one vertex has degree $n-1$ and every remaining vertex has degree 1.

Because the graph is guaranteed to be connected, these degree conditions are sufficient. We do not need any additional structural verification.

This reduces the entire problem to counting vertex degrees while reading edges and then checking a few simple patterns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n+m)) | O(n+m) | Too slow |
| Optimal | O(n+m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $m$.
2. Create an array `deg` of size $n$ initialized to zero.
3. For every edge $(u,v)$, increment `deg[u]` and `deg[v]`.

The degree of a vertex is exactly the number of incident edges, so after processing all edges the array contains the complete degree sequence.
4. Check whether every vertex has degree 2.

If true, the graph is a ring topology.
5. Count how many vertices have degree 1 and how many have degree 2.

If there are exactly two degree-1 vertices and exactly $n-2$ degree-2 vertices, the graph is a bus topology.
6. Count how many vertices have degree $n-1$.

If there is exactly one such vertex and the remaining $n-1$ vertices have degree 1, the graph is a star topology.
7. If none of the above conditions hold, output `"unknown topology"`.

### Why it works

The graph is connected, which is the crucial guarantee.

A connected graph in which every vertex has degree 2 must be a single cycle, so it is a ring.

A connected graph with exactly two degree-1 vertices and all remaining vertices degree 2 must be a single path, so it is a bus.

A connected graph with one vertex of degree $n-1$ and all others degree 1 can only be a star centered at that high-degree vertex.

Since these conditions are mutually exclusive and completely characterize the three required topologies, the algorithm always returns the correct classification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    deg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        deg[u - 1] += 1
        deg[v - 1] += 1

    if all(d == 2 for d in deg):
        print("ring topology")
        return

    cnt1 = sum(d == 1 for d in deg)
    cnt2 = sum(d == 2 for d in deg)

    if cnt1 == 2 and cnt2 == n - 2:
        print("bus topology")
        return

    cnt_center = sum(d == n - 1 for d in deg)

    if cnt_center == 1 and cnt1 == n - 1:
        print("star topology")
        return

    print("unknown topology")

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly.

The degree array is the only information we need from the graph. Every edge contributes one degree to each endpoint, so processing all edges once is enough.

The order of checks is not particularly important because the three valid topologies are mutually exclusive for the given constraints. The code first checks for a ring, then a bus, then a star.

A subtle point is that we use the already computed count of degree-1 vertices when checking the star condition. A valid star must have exactly one center of degree $n-1$ and every other vertex must have degree 1.

Another detail is the conversion from 1-based vertex numbering in the input to 0-based indexing in the Python array.

## Worked Examples

### Example 1

Input:

```
4 3
1 2
2 3
3 4
```

Degree sequence becomes:

| Vertex | Degree |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |

Counts:

| cnt1 | cnt2 | cnt_center |
| --- | --- | --- |
| 2 | 2 | 0 |

The bus condition matches exactly, so the answer is:

```
bus topology
```

This demonstrates the characteristic path pattern: two endpoints and all internal vertices of degree 2.

### Example 2

Input:

```
5 4
1 2
1 3
1 4
1 5
```

Degree sequence:

| Vertex | Degree |
| --- | --- |
| 1 | 4 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |

Counts:

| cnt1 | cnt2 | cnt_center |
| --- | --- | --- |
| 4 | 0 | 1 |

Since one vertex has degree $n-1=4$ and all others have degree 1, the answer is:

```
star topology
```

This example shows why degree information alone is enough to identify a star.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass over all edges and a few scans of the degree array |
| Space | O(n) | Stores the degree of each vertex |

With at most $10^5$ vertices and $10^5$ edges, a linear solution performs only a few hundred thousand operations and comfortably fits within the time limit. The degree array requires only $O(n)$ memory, well below the available limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    deg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        deg[u - 1] += 1
        deg[v - 1] += 1

    if all(d == 2 for d in deg):
        return "ring topology"

    cnt1 = sum(d == 1 for d in deg)
    cnt2 = sum(d == 2 for d in deg)

    if cnt1 == 2 and cnt2 == n - 2:
        return "bus topology"

    cnt_center = sum(d == n - 1 for d in deg)

    if cnt_center == 1 and cnt1 == n - 1:
        return "star topology"

    return "unknown topology"

# provided sample
assert run(
"""4 3
1 2
2 3
3 4
"""
) == "bus topology", "sample 1"

# ring
assert run(
"""4 4
1 2
2 3
3 4
4 1
"""
) == "ring topology", "simple ring"

# star
assert run(
"""5 4
1 2
1 3
1 4
1 5
"""
) == "star topology", "simple star"

# unknown
assert run(
"""5 5
1 2
2 3
3 4
4 5
2 5
"""
) == "unknown topology", "extra edge"

# minimum valid ring
assert run(
"""4 4
1 2
2 3
3 4
4 1
"""
) == "ring topology", "minimum size ring"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Path on 4 vertices | bus topology | Standard bus detection |
| 4-cycle | ring topology | All vertices degree 2 |
| Star with 5 vertices | star topology | Single high-degree center |
| Path plus extra edge | unknown topology | Rejects almost-valid structures |
| Minimum-size ring | ring topology | Boundary value for n |

## Edge Cases

Consider the star graph:

```
4 3
1 2
1 3
1 4
```

The degree sequence is $[3,1,1,1]$. During the scan, `cnt1 = 3`, `cnt2 = 0`, and one vertex has degree `n - 1 = 3`. The bus test fails because there are not exactly two degree-1 vertices. The star test succeeds, producing:

```
star topology
```

Now consider a ring:

```
4 4
1 2
2 3
3 4
4 1
```

Every vertex has degree 2. The first check immediately succeeds and outputs:

```
ring topology
```

No further analysis is required.

Finally, consider a connected graph that matches none of the patterns:

```
5 5
1 2
2 3
3 4
4 5
2 5
```

The degree sequence is $[1,3,2,2,2]$. The ring condition fails because not every degree is 2. The bus condition fails because there is only one degree-1 vertex. The star condition fails because no vertex has degree $n-1=4$. The algorithm correctly returns:

```
unknown topology
```

These examples cover the situations where relying only on edge counts would produce incorrect classifications, while the degree-based approach handles them exactly.
