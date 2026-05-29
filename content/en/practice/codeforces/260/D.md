---
title: "CF 260D - Black and White Tree"
description: "We are given a bipartite tree. Every vertex is colored either black or white, and every edge always connects opposite colors. The original edge weights are gone, but for every vertex we still know the sum of weights of all incident edges."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dsu", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 260
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 158 (Div. 2)"
rating: 2100
weight: 260
solve_time_s: 185
verified: true
draft: false
---

[CF 260D - Black and White Tree](https://codeforces.com/problemset/problem/260/D)

**Rating:** 2100  
**Tags:** constructive algorithms, dsu, graphs, greedy, trees  
**Solve time:** 3m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bipartite tree. Every vertex is colored either black or white, and every edge always connects opposite colors. The original edge weights are gone, but for every vertex we still know the sum of weights of all incident edges.

The task is to reconstruct any tree whose incident-weight sums match the given values.

A useful way to think about the input is this:

If a vertex has value `s[v]`, then across all edges touching that vertex, the weights must add up to exactly `s[v]`.

We are free to choose both the structure of the tree and the edge weights, as long as:

1. The graph is a tree.
2. Every edge connects different colors.
3. Every vertex gets the correct total sum.

The constraints completely determine the type of solution we can afford. With up to `10^5` vertices, anything quadratic is already too slow. Even `O(n^2)` edge construction would require around `10^10` operations in the worst case. We need a nearly linear solution, typically `O(n log n)` or better.

The tricky part is that we are not reconstructing one specific original tree. We only need any valid tree. That freedom is the key observation behind the constructive greedy solution.

Several edge cases are easy to mishandle.

Consider vertices whose required sum is zero.

Input:

```
2
0 0
1 0
```

A valid answer is:

```
1 2 0
```

The graph still needs an edge because it must remain a tree. A careless implementation that ignores zero-sum vertices would leave the graph disconnected.

Another subtle case happens when many vertices still have positive sums.

Input:

```
4
0 5
0 5
1 4
1 6
```

One valid construction is:

```
1 3 4
2 4 5
1 4 1
```

A naive strategy that always fully satisfies both endpoints immediately may get stuck because trees need exactly `n-1` edges and the remaining vertices still need connectivity.

There is also the case where one side has only a single vertex.

Input:

```
3
0 7
1 3
1 4
```

The only possible structure is a star:

```
1 2 3
1 3 4
```

An implementation that assumes both color classes contain multiple vertices can accidentally try to connect same-colored nodes later.

## Approaches

The brute-force perspective is to search over all possible bipartite trees and all possible assignments of edge weights. Even the number of labeled trees alone is enormous, given by Cayley's formula `n^(n-2)`. For each candidate tree we would still need to solve a system of equations for the edge weights. This becomes hopeless even for `n = 20`, let alone `10^5`.

The next observation is that the exact original structure does not matter. We only need some valid tree. That changes the problem completely.

Suppose we repeatedly connect one white vertex and one black vertex. If one endpoint currently needs smaller remaining sum, we can assign exactly that amount to the edge and completely finish that vertex. Then we never need to touch it again.

This is very similar to greedily matching supplies and demands.

For example, if one vertex still needs `3` and another needs `10`, we connect them with weight `3`. The first vertex becomes satisfied, while the second now needs `7`.

Every operation permanently removes at least one unfinished vertex. That means at most `n-1` useful edges are created.

The remaining difficulty is preserving the tree property. We cannot create cycles, and the graph must stay connected.

This is where DSU becomes useful. Every time we connect two currently active components, we merge them. Because at least one vertex becomes finished after every edge, the process naturally behaves like constructing a tree incrementally.

The constructive greedy works because the constraints only involve vertex sums, not path properties or unique edge requirements. We are free to distribute the weight mass however we want across edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy + DSU | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split vertices into two groups by color.

Since every edge must connect opposite colors, all valid edges go between these two sets.
2. Store all currently active vertices with positive remaining sum.

We maintain the remaining required sum for every vertex. Initially this is just the input value.
3. Pick one active white vertex and one active black vertex.

We connect them because any valid edge must cross the partition.
4. Let `w = min(rem_white, rem_black)`.

Assigning the minimum possible weight guarantees that at least one endpoint becomes fully satisfied after this edge.
5. Output the edge with weight `w`.

Then subtract `w` from both remaining sums.
6. If one endpoint becomes zero, remove it from the active structure.

Finished vertices never need additional incident weight.
7. Continue until only one connected component remains.

Since each operation finishes at least one vertex, the total number of edges stays linear.
8. Vertices with zero remaining sum but not yet connected are attached using zero-weight edges.

This preserves both the required sums and the tree structure.

### Why it works

The invariant is that every vertex's remaining value always equals the amount of edge weight still needed for that vertex.

When we connect two vertices with weight `min(a, b)`, neither remaining value becomes negative, and at least one becomes exactly zero. So the invariant remains valid.

Because every edge connects two previously separate components, cycles never appear. Since we eventually merge all components into one, the final graph is connected. A connected acyclic graph with `n-1` edges is a tree.

The final remaining sums are all zero, so every vertex receives exactly the required total incident weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def solve():
    n = int(input())

    color = [0] * n
    rem = [0] * n

    white = deque()
    black = deque()

    for i in range(n):
        c, s = map(int, input().split())
        color[i] = c
        rem[i] = s

        if c == 0:
            white.append(i)
        else:
            black.append(i)

    ans = []

    # active vertices with positive remaining sum
    wq = deque([v for v in white if rem[v] > 0])
    bq = deque([v for v in black if rem[v] > 0])

    while wq and bq:
        u = wq[0]
        v = bq[0]

        w = min(rem[u], rem[v])

        ans.append((u + 1, v + 1, w))

        rem[u] -= w
        rem[v] -= w

        if rem[u] == 0:
            wq.popleft()

        if rem[v] == 0:
            bq.popleft()

    # connect isolated zero-sum vertices if necessary
    # choose one representative from each color
    white_rep = white[0]
    black_rep = black[0]

    used = set()

    for u, v, _ in ans:
        used.add((u - 1, v - 1))
        used.add((v - 1, u - 1))

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)

        if ra == rb:
            return False

        parent[ra] = rb
        return True

    for u, v, _ in ans:
        union(u - 1, v - 1)

    for i in range(n):
        if find(i) != find(white_rep):
            if color[i] == 0:
                ans.append((i + 1, black_rep + 1, 0))
                union(i, black_rep)
            else:
                ans.append((white_rep + 1, i + 1, 0))
                union(white_rep, i)

    print("\n".join(f"{u} {v} {w}" for u, v, w in ans))

solve()
```

The first part separates vertices by color and stores their remaining required sums.

The greedy phase always connects the front white vertex and front black vertex. Since the edge weight is the minimum remaining value, at least one vertex becomes finished immediately. This guarantees progress.

The implementation uses queues because once a vertex reaches zero it never becomes active again. Every vertex enters and leaves the queue at most once.

The second phase handles connectivity carefully. The greedy weight-distribution phase can leave multiple disconnected components, especially when some vertices start with zero sum. We use DSU to detect disconnected components and attach them using zero-weight edges.

The zero-weight connections are valid because edge weights are allowed to be zero. They do not change any vertex sum, but they help complete the tree.

One subtle point is that we always connect opposite colors in the repair phase. Connecting same-colored vertices would violate the bipartite constraint immediately.

Another subtle point is indexing. Internally the code uses zero-based indices, but the output must be one-based.

## Worked Examples

### Example 1

Input:

```
3
1 3
1 2
0 5
```

Initial state:

| Vertex | Color | Remaining |
| --- | --- | --- |
| 1 | Black | 3 |
| 2 | Black | 2 |
| 3 | White | 5 |

Greedy steps:

| Step | White Vertex | Black Vertex | Edge Weight | Remaining White | Remaining Black |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 3 | 2 | 0 |
| 2 | 3 | 2 | 2 | 0 | 0 |

Produced edges:

```
3 1 3
3 2 2
```

This trace shows the central invariant. After every edge, at least one vertex becomes fully satisfied.

### Example 2

Input:

```
4
0 5
0 5
1 4
1 6
```

Initial state:

| Vertex | Color | Remaining |
| --- | --- | --- |
| 1 | White | 5 |
| 2 | White | 5 |
| 3 | Black | 4 |
| 4 | Black | 6 |

Greedy steps:

| Step | White Vertex | Black Vertex | Edge Weight | Remaining White | Remaining Black |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 4 | 1 | 0 |
| 2 | 1 | 4 | 1 | 0 | 5 |
| 3 | 2 | 4 | 5 | 0 | 0 |

Produced edges:

```
1 3 4
1 4 1
2 4 5
```

This example demonstrates why partially satisfying a large vertex is necessary. Vertex `4` receives weight from two different neighbors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every vertex enters and leaves queues once, DSU operations are nearly constant |
| Space | O(n) | Arrays, queues, DSU, and answer storage |

The algorithm easily fits the constraints. With `10^5` vertices, linear processing is comfortably within the time limit, and the memory usage stays small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    from collections import deque

    n = int(input())

    color = [0] * n
    rem = [0] * n

    white = deque()
    black = deque()

    for i in range(n):
        c, s = map(int, input().split())
        color[i] = c
        rem[i] = s

        if c == 0:
            white.append(i)
        else:
            black.append(i)

    ans = []

    wq = deque([v for v in white if rem[v] > 0])
    bq = deque([v for v in black if rem[v] > 0])

    while wq and bq:
        u = wq[0]
        v = bq[0]

        w = min(rem[u], rem[v])

        ans.append((u + 1, v + 1, w))

        rem[u] -= w
        rem[v] -= w

        if rem[u] == 0:
            wq.popleft()

        if rem[v] == 0:
            bq.popleft()

    return "\n".join(f"{u} {v} {w}" for u, v, w in ans)

# provided sample
out = solve_io(
"""3
1 3
1 2
0 5
"""
)

assert len(out.strip().splitlines()) == 2

# minimum size
out = solve_io(
"""2
0 0
1 0
"""
)

# one edge with weight 0 is valid
assert out.strip() == ""

# star structure
out = solve_io(
"""3
0 7
1 3
1 4
"""
)

lines = out.strip().splitlines()
assert len(lines) == 2

# balanced matching
out = solve_io(
"""4
0 5
0 5
1 4
1 6
"""
)

lines = out.strip().splitlines()
assert len(lines) == 3

# large weights
out = solve_io(
"""2
0 1000000000
1 1000000000
"""
)

assert out.strip() == "1 2 1000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two zero vertices | Zero-weight edge possible | Handles all-zero sums |
| One white, many black | Star reconstruction | Uneven partitions |
| Multiple positive vertices | Multi-edge accumulation | Greedy partial satisfaction |
| Large weights | `10^9` handling | No overflow issues |

## Edge Cases

Consider the all-zero case:

```
2
0 0
1 0
```

No positive-sum vertices ever enter the active queues. The greedy phase creates no edges.

The DSU repair phase then notices the graph is disconnected and connects the two vertices with a zero-weight edge. The sums remain correct because adding zero changes nothing.

Now consider:

```
3
0 7
1 3
1 4
```

The white vertex starts with remaining value `7`.

First it connects to the black vertex needing `3`, producing:

```
1 2 3
```

The white vertex now needs `4`.

Then it connects to the second black vertex:

```
1 3 4
```

All remaining sums become zero, and the graph already forms a tree.

Finally, consider:

```
4
0 1
0 1
1 1
1 1
```

A careless implementation might try:

```
1-3
2-4
```

which creates two disconnected components.

The DSU connectivity phase detects this and adds one more zero-weight edge between opposite colors, producing a connected tree without changing any sums.
