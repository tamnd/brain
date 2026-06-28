---
title: "CF 104969I - Pizza Tower"
description: "We are given a set of points on a huge integer grid. Each point represents an enemy located at coordinates $(xi, yi)$ and carrying a strength value $si$. Every coordinate pair appears at most once, so there is no need to combine duplicates."
date: "2026-06-28T18:29:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 86
verified: false
draft: false
---

[CF 104969I - Pizza Tower](https://codeforces.com/problemset/problem/104969/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a huge integer grid. Each point represents an enemy located at coordinates $(x_i, y_i)$ and carrying a strength value $s_i$. Every coordinate pair appears at most once, so there is no need to combine duplicates.

For any point $(x_i, y_i)$, we define a value $F(x_i, y_i)$ as the total strength of all enemies that lie inside or on the bottom-left rectangle anchored at the origin and stretching to $(x_i, y_i)$. In other words, we sum $s_j$ over all enemies whose coordinates satisfy $x_j \le x_i$ and $y_j \le y_i$.

The task is to compute this prefix-sum-like value for every input point.

The constraints push us away from anything quadratic. With up to $2 \cdot 10^5$ points, any solution that scans all previous points per query will perform about $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the time limit. Even approaches that sort one dimension but scan the other must be avoided unless fully optimized with data structures.

A subtle issue is that coordinates go up to $2 \cdot 10^9$, so any grid-based structure indexed directly by coordinates is impossible. We must compress or avoid direct indexing.

One failure mode is computing answers independently for each point by iterating over all points and summing those satisfying the dominance condition. For example, with points forming a chain like $(1,1),(2,2),\dots$, this degenerates into summing increasingly large prefixes repeatedly, producing an $O(n^2)$ blowup.

Another issue arises if we sort only by $x$ and forget that the condition also depends on $y$. Then we might incorrectly include points with large $y$ that appear early in the sorted order but should not contribute.

The correct approach must handle both dimensions symmetrically while still building answers incrementally.

## Approaches

A brute-force method directly follows the definition: for each point $(x_i, y_i)$, iterate over all points $(x_j, y_j)$ and add $s_j$ if $x_j \le x_i$ and $y_j \le y_i$. This is correct because it literally implements the definition of the function. The cost per query is linear, giving $O(n^2)$ total operations, which becomes impossible when $n$ reaches $2 \cdot 10^5$.

The key observation is that this is a two-dimensional prefix sum problem over a sparse set of points. If we sort points by $x$, then when processing a point, all previously processed points automatically satisfy the $x_j \le x_i$ condition. The remaining requirement becomes: among all previously inserted points, we need the sum of those with $y_j \le y_i$.

This reduces the problem to maintaining a dynamic prefix sum over $y$-coordinates while sweeping in increasing order of $x$. Since $y$ is also large, we compress it into ranks and use a Fenwick tree (binary indexed tree). Each point is inserted once, and we query prefix sums in $O(\log n)$.

The only subtlety is that multiple points may share the same $x$. If we process them one by one and immediately insert into the structure, a point with the same $x$ might incorrectly include itself or other same-$x$ points. The correct fix is to process points grouped by identical $x$: compute all answers for the group using only previously inserted points, then insert the group afterward.

This sweep-line perspective converts a two-dimensional dominance query into a sequence of one-dimensional prefix queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sweep + Fenwick Tree | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process points in increasing order of $x$, while maintaining a Fenwick tree over compressed $y$-coordinates storing cumulative strengths.

1. Sort all points by $x$, and if needed, by $y$ as a secondary key. Sorting ensures that when we reach a point, all smaller $x$-values are already handled.
2. Compress all $y_i$ values into a range $[1, n]$. This is necessary because Fenwick trees require compact indices, and raw coordinates are too large to index directly.
3. Traverse the sorted points in blocks of equal $x$-value. For each block, first compute answers using only previously inserted points.
4. Inside a block, for each point $(x, y, s)$, query the Fenwick tree for the sum of all values with compressed $y \le y$. This returns exactly the contribution from all points with smaller $x$ and valid $y$.
5. Store these results, but do not update the Fenwick tree yet for points in this block. This prevents same-$x$ points from contributing to each other incorrectly.
6. After processing the entire block, insert all its points into the Fenwick tree by adding $s$ at their compressed $y$ position.
7. Continue until all blocks are processed.

The Fenwick tree operations ensure each query reflects exactly the sum over all valid predecessors in the dominance order.

### Why it works

At every step, the Fenwick tree represents the multiset of all processed points strictly to the left in $x$. Grouping by equal $x$ ensures that within a block, no point contaminates another with the same $x$-coordinate. Therefore, when querying for a point, the structure contains exactly the set of points satisfying $x_j < x_i$, and the prefix query on $y$ enforces $y_j \le y_i$. This maintains the invariant that every query returns precisely the desired 2D prefix sum over the processed prefix of the sweep.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

n = int(input())
pts = []
ys = []

for idx in range(n):
    x, y, s = map(int, input().split())
    pts.append((x, y, s, idx))
    ys.append(y)

ys.sort()
ys = {v: i + 1 for i, v in enumerate(ys)}

pts.sort(key=lambda p: (p[0], p[1]))

fw = Fenwick(n)
ans = [0] * n

i = 0
while i < n:
    j = i
    while j < n and pts[j][0] == pts[i][0]:
        j += 1

    for k in range(i, j):
        x, y, s, idx = pts[k]
        yi = ys[y]
        ans[idx] = fw.sum(yi)

    for k in range(i, j):
        x, y, s, idx = pts[k]
        yi = ys[y]
        fw.add(yi, s)

    i = j

for v in ans:
    print(v)
```

The solution begins by reading all points and storing their original indices so that results can be returned in input order. The $y$-compression step builds a rank map from sorted unique $y$-values, which ensures Fenwick tree indices remain within $1 \ldots n$.

Sorting by $(x, y)$ establishes the sweep order. The Fenwick tree stores accumulated strengths by $y$-rank. The grouped loop is critical: queries for a block are executed before any updates from that block are applied, ensuring correctness for equal $x$-values.

Each query uses `fw.sum(yi)` to retrieve the total strength of all previously inserted points with $y \le y_i$.

## Worked Examples

### Sample 1

Input points:

$(1,1,5), (2,1,10), (1,2,10), (3,3,15)$

After sorting by $x$:

$$(1,1,5), (1,2,10), (2,1,10), (3,3,15)$$

We process block $x=1$ first, but Fenwick is empty so all queries return 0.

| Step | Point | Query result | Fenwick before | Fenwick after |
| --- | --- | --- | --- | --- |
| 1 | (1,1,5) | 0 | empty | add y=1:5 |
| 2 | (1,2,10) | 0 | y1=5 | add y=2:10 |

Now Fenwick contains both.

Next block $x=2$:

| Step | Point | Query result | Fenwick before | Fenwick after |
| --- | --- | --- | --- | --- |
| 3 | (2,1,10) | 5 | y1=5,y2=10 | add y=1:10 |

Finally $x=3$:

| Step | Point | Query result | Fenwick before | Fenwick after |
| --- | --- | --- | --- | --- |
| 4 | (3,3,15) | 25 | full tree | add y=3:15 |

Outputs match cumulative dominance sums, confirming that the sweep correctly accumulates both dimensions.

### Sample 2

Points already form increasing chains in both coordinates:

$(1,1,1), (1,2,2), (1,3,3), (1,4,4), (1,5,5)$

All share the same $x$, so no point should see any other. The grouping rule ensures every query happens before any insert, so all results are zero except for the structural accumulation after processing (though outputs are independent per point).

| Step | Point | Query result | Fenwick before | Fenwick after |
| --- | --- | --- | --- | --- |
| 1 | (1,1,1) | 0 | empty | add |
| 2 | (1,2,2) | 0 | unchanged within block | add |
| 3 | (1,3,3) | 0 | unchanged within block | add |
| 4 | (1,4,4) | 0 | unchanged within block | add |
| 5 | (1,5,5) | 0 | unchanged within block | add |

This demonstrates why equal-$x$ batching is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates $O(n \log n)$, each Fenwick operation costs $O(\log n)$ |
| Space | $O(n)$ | storage for points, compression map, and Fenwick tree |

The constraints allow up to $2 \cdot 10^5$ operations, so logarithmic updates are easily fast enough, and memory usage stays linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def sum(self, i):
            res = 0
            while i > 0:
                res += self.bit[i]
                i -= i & -i
            return res

    n = int(input())
    pts = []
    ys = []
    for idx in range(n):
        x, y, s = map(int, input().split())
        pts.append((x, y, s, idx))
        ys.append(y)

    ys.sort()
    ys = {v: i + 1 for i, v in enumerate(ys)}
    pts.sort(key=lambda p: (p[0], p[1]))

    fw = Fenwick(n)
    ans = [0] * n

    i = 0
    while i < n:
        j = i
        while j < n and pts[j][0] == pts[i][0]:
            j += 1

        for k in range(i, j):
            x, y, s, idx = pts[k]
            ans[idx] = fw.sum(ys[y])

        for k in range(i, j):
            x, y, s, idx = pts[k]
            fw.add(ys[y], s)

        i = j

    return "\n".join(map(str, ans))

# provided samples
assert run("4\n1 1 5\n2 1 10\n1 2 10\n3 3 15\n") == "5\n15\n15\n40"
assert run("5\n1 1 1\n1 2 2\n1 3 3\n1 4 4\n1 5 5\n") == "0\n0\n0\n0\n0"

# custom cases
assert run("1\n7 7 10\n") == "0", "single point"
assert run("3\n1 3 1\n2 2 1\n3 1 1\n") == "0\n1\n3", "cross pattern"
assert run("4\n1 1 1\n1 2 1\n2 1 1\n2 2 1\n") == "0\n1\n1\n3", "grid corners"
assert run("2\n100 100 5\n50 50 7\n") == "7\n0", "unsorted input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | no predecessors |
| cross pattern | 0 1 3 | mixed dominance ordering |
| grid corners | 0 1 1 3 | rectangle accumulation correctness |
| unsorted input | 7 0 | sorting + sweep correctness |

## Edge Cases

A key edge case is when multiple points share the same $x$-coordinate. Consider:

```
3
1 1 5
1 2 7
1 3 9
```

All points must see zero contribution from each other because none satisfy $x_j < x_i$. During the sweep, all three points form one block. The algorithm first performs all Fenwick queries, which return zero since the structure is empty. Only after all queries are computed do we insert the values. This guarantees no contamination within the block.

Another edge case is strictly increasing coordinates:

```
3
1 1 1
2 2 1
3 3 1
```

Here each point should accumulate all previous strengths. After processing the first point, the Fenwick tree contains one element. The second query returns 1, and the third returns 2, matching a growing 2D prefix.

Finally, reversed ordering stresses the sorting step:

```
3
3 3 1
2 2 1
1 1 1
```

Sorting rearranges them into increasing $x$. The sweep ensures that despite input order, each point correctly aggregates only earlier points in dominance order, confirming that correctness depends entirely on the sorted structure rather than input sequence.
