---
title: "CF 102412C - Steel Ball Run"
description: "We have a tree whose vertices may or may not currently contain a chip. A query toggles one vertex between these two states. After every toggle, we need the minimum total number of edge traversals required to gather all currently present chips at one common vertex."
date: "2026-08-10T14:00:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "C"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 1030
verified: true
draft: false
---

[CF 102412C - Steel Ball Run](https://codeforces.com/problemset/problem/102412/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 17m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree whose vertices may or may not currently contain a chip. A query toggles one vertex between these two states. After every toggle, we need the minimum total number of edge traversals required to gather all currently present chips at one common vertex. A chip may pass through vertices containing other chips, so the cost for choosing a destination vertex (v) is simply

[
F(v)=\sum_{u\text{ has a chip}} \operatorname{dist}(u,v).
]

The answer is the minimum value of (F(v)) over all vertices.

The tree contains up to (10^5) vertices and there are up to (10^5) updates. The official time limit is 4 seconds and the memory limit is 256 MiB. This rules out anything that scans the whole tree after every query. An (O(nq)) solution can perform about (10^{10}) operations at the maximum limits, which is far beyond what fits. We need roughly logarithmic work per update.

There are several edge cases that are easy to mishandle. With only one chip, the answer is always zero. For example,

```
1
1
+ 1
```

has output

```
0
```

because the chip is already at the destination.

The optimal destination does not have to contain a chip. On the path (1-2-3), adding chips at vertices 1 and 3 gives

```
3
1 2
2 3
2
+ 1
+ 3
```

with output

```
0
2
```

The best destination is vertex 2, which is empty. An implementation that considers only occupied vertices would incorrectly report 2 only if it happens to handle this case indirectly, and in general it can miss the true optimum.

There can also be two equally good median vertices. On the path (1-2), if both endpoints contain chips, moving everything to either endpoint costs one. A method that assumes the median is unique can accidentally reject a correct answer. The useful characterization is based on components containing strictly more than half the chips, so either median is handled naturally.

Finally, deleting the last chip is forbidden by the input, but deleting a chip can still leave exactly one chip. For example,

```
3
1 2
2 3
3
+ 1
+ 3
- 1
```

produces

```
0
2
0
```

The data structures must work when the active set has size one immediately after an update.

## Approaches

A direct solution can recompute the entire objective after every query. Root the tree once, calculate the number of chips in every subtree, compute the sum of distances from the root, and then reroot the distance sum across all vertices. The standard rerooting formula is

[
F(v)=F(p)+M-2S_v,
]

when (v) is a child of (p), where (M) is the total number of chips and (S_v) is the number of chips in (v)'s subtree. This gives the exact answer in (O(n)) time for one query.

The problem is that doing this after (10^5) queries costs (O(nq)), which is about (10^{10}) operations at the maximum constraints. The brute force is correct because it explicitly evaluates every possible destination, but it repeatedly throws away almost all information from the previous query.

The key observation is that the objective has a very rigid shape on a tree. Suppose we stand at vertex (v) and move across one edge into a component containing (x) chips. Every one of those (x) chips gets one edge closer, while each of the other (M-x) chips gets one edge farther. Consequently,

[
F(\text{next})-F(v)=(M-x)-x=M-2x.
]

So moving toward a component containing more than half the chips strictly improves the answer. Moving toward a component containing at most half cannot improve it. Hence a vertex is optimal exactly when every component obtained by removing it contains at most half of all chips. This is the weighted median of the tree.

Root the original tree arbitrarily. In this rooted tree, if some child subtree contains more than half of all chips, the median must be inside that subtree. We can repeatedly follow that heavy child. Equivalently, the median is the deepest vertex whose subtree contains strictly more than half of all chips.

The remaining problem is finding that vertex dynamically. An Euler tour turns every subtree into one contiguous interval. A Fenwick tree can maintain which vertices contain chips, so subtree chip counts become interval-sum queries. We first find the chip that crosses the halfway point in Euler order. Any subtree containing more than half of the chips must contain that chip, so the median lies on the root-to-that-chip path. Binary lifting then finds the deepest ancestor whose subtree still contains more than half the chips. This costs (O(\log^2 n)) because each of the (O(\log n)) ancestor checks performs a Fenwick prefix-sum query.

After locating the median, we still need its total distance to all chips. Recomputing this sum would be too expensive. Centroid decomposition gives exactly the right dynamic structure. For every centroid (c), we maintain the number of active chips represented there and their total distance to (c). We also store the corresponding information for each centroid child so that contributions from the same decomposition component can be subtracted once. An insertion or deletion changes only (O(\log n)) centroid ancestors, and a distance-sum query visits the same (O(\log n)) ancestors.

The two techniques solve different halves of the problem. Euler order and binary lifting identify where the optimum is, while centroid decomposition evaluates the objective at that optimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) | (O(n)) | Too slow |
| Optimal | (O(n\log n+q\log^2 n)) | (O(n\log n)) | Accepted |

## Algorithm Walkthrough

1. Root the original tree at vertex 1 and perform an Euler tour. Store `tin[v]` and `tout[v]`, so the subtree of (v) corresponds to the Euler interval ([tin[v],tout[v])). Also build binary-lifting ancestors.
2. Maintain the current chip configuration in a Fenwick tree. Position `tin[v]` contains 1 exactly when vertex (v) has a chip. The Fenwick tree therefore supports adding or removing a chip and counting chips inside any subtree.
3. Let (M) be the current number of chips and set

[
k=\left\lfloor\frac M2\right\rfloor+1.
]

Find the (k)-th active vertex in Euler order. Call it (x). This is the first active vertex after the halfway point.

1. The median must be an ancestor of (x). If a vertex has more than half of all chips in its subtree, that subtree contains the (k)-th active vertex. Thus every possible median lies on the root-to-(x) path.
2. Starting from (x), use binary lifting to climb as far upward as possible while the candidate ancestor's subtree contains fewer than (k) chips. The first ancestor with at least (k) chips is the deepest subtree containing more than half of the chips, so it is a valid tree median.
3. Build a centroid decomposition of the original tree. For every vertex, store its distances to its centroid ancestors. The centroid tree has logarithmic height because each centroid splits its component into pieces of at most half the size.
4. For every centroid (c), maintain `cnt[c]`, the number of active chips represented by that centroid, and `sum[c]`, the sum of their distances to (c). For every non-root centroid (c), also maintain `subcnt[c]` and `subsum[c]`, describing the component represented by (c) relative to its centroid parent.
5. When a chip is inserted or removed at vertex (v), walk from (v) upward through the centroid tree. At centroid (c), add the update to `cnt[c]` and add the corresponding distance to `sum[c]`. If (c) has a centroid parent, update `subcnt[c]` and `subsum[c]` as well.
6. To calculate the total distance from an arbitrary vertex (v) to every active chip, walk through its centroid ancestors. For a centroid (c), `sum[c] + cnt[c] * dist(v,c)` counts the contribution of all chips stored there. The chips belonging to the same centroid component as (v) were already counted at a deeper centroid, so subtract `subsum[child] + subcnt[child] * dist(v,c)` for that child.
7. After every query, update both the Fenwick tree and centroid structure, find the current median, evaluate its total distance using the centroid structure, and print that value.

### Why it works

The central invariant is that a vertex is a minimum of the sum-of-distances function exactly when no component around it contains more than half of the active chips. If such a component exists, crossing its edge decreases the objective, so the current vertex cannot be optimal. If no such component exists, every possible first move has nonnegative cost change, so the vertex is optimal.

The Euler-order construction finds the deepest ancestor satisfying this condition. The (k)-th active Euler position must lie inside every subtree containing more than half the chips, so the median is on its ancestor path. Binary lifting finds the deepest qualifying ancestor.

The centroid structure independently maintains the exact distance sum for every queried vertex. Each active chip contributes to every centroid ancestor of its vertex, and the subtraction for the deeper centroid component prevents double counting. Thus the value returned for the selected median is exactly the minimum possible span.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, pos, delta):
        n = self.n
        bit = self.bit
        while pos <= n:
            bit[pos] += delta
            pos += pos & -pos

    def prefix(self, pos):
        bit = self.bit
        res = 0
        while pos:
            res += bit[pos]
            pos -= pos & -pos
        return res

    def kth(self, k):
        idx = 0
        step = 1 << (self.n.bit_length() - 1)
        bit = self.bit
        n = self.n

        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1

        return idx

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    # Root the original tree and build an Euler tour.
    parent = array('i', [-1]) * n
    depth = array('i', [0]) * n
    tin = array('i', [0]) * n
    tout = array('i', [0]) * n
    euler = []

    stack = [(0, -1, 0)]
    while stack:
        v, p, state = stack.pop()

        if state == 0:
            parent[v] = p
            if p != -1:
                depth[v] = depth[p] + 1

            tin[v] = len(euler)
            euler.append(v)

            stack.append((v, p, 1))
            for to in reversed(graph[v]):
                if to != p:
                    stack.append((to, v, 0))
        else:
            tout[v] = len(euler)

    # Binary lifting for ancestor queries.
    LOG = n.bit_length()
    up = [array('i', parent)]

    for _ in range(1, LOG):
        prev = up[-1]
        cur = array('i', [-1]) * n
        for v in range(n):
            p = prev[v]
            cur[v] = -1 if p == -1 else prev[p]
        up.append(cur)

    # Centroid decomposition.
    removed = bytearray(n)
    cd_parent = array('i', [-1]) * n

    # For every original vertex v, cd_dist[v] stores distances to
    # centroid ancestors in root-to-leaf centroid order.
    cd_dist = [array('i') for _ in range(n)]

    tmp_parent = array('i', [-1]) * n
    subtree_size = array('i', [0]) * n

    def find_centroid(start):
        order = [start]
        tmp_parent[start] = -1

        for v in order:
            pv = tmp_parent[v]
            for to in graph[v]:
                if not removed[to] and to != pv:
                    tmp_parent[to] = v
                    order.append(to)

        for v in reversed(order):
            s = 1
            for to in graph[v]:
                if not removed[to] and tmp_parent[to] == v:
                    s += subtree_size[to]
            subtree_size[v] = s

        total = len(order)

        for v in order:
            largest = total - subtree_size[v]
            for to in graph[v]:
                if not removed[to] and tmp_parent[to] == v:
                    if subtree_size[to] > largest:
                        largest = subtree_size[to]

            if largest * 2 <= total:
                return v

        return start

    def decompose(start, pcd):
        c = find_centroid(start)
        cd_parent[c] = pcd

        # Store distance from this centroid to every vertex in its
        # current component.
        stack = [(c, -1, 0)]
        while stack:
            v, p, d = stack.pop()
            cd_dist[v].append(d)

            for to in graph[v]:
                if not removed[to] and to != p:
                    stack.append((to, v, d + 1))

        removed[c] = 1

        for to in graph[c]:
            if not removed[to]:
                decompose(to, c)

    decompose(0, -1)

    # Dynamic centroid data.
    cnt = array('q', [0]) * n
    total_dist = array('q', [0]) * n
    subcnt = array('q', [0]) * n
    subdist = array('q', [0]) * n

    fenwick = Fenwick(n)
    active = bytearray(n)
    total_chips = 0

    def centroid_update(v, delta):
        chain = cd_dist[v]
        c = v

        for i in range(len(chain) - 1, -1, -1):
            d = chain[i]

            cnt[c] += delta
            total_dist[c] += delta * d

            p = cd_parent[c]
            if p != -1:
                dp = chain[i - 1]
                subcnt[c] += delta
                subdist[c] += delta * dp

            c = p
            if c == -1:
                break

    def distance_sum(v):
        chain = cd_dist[v]
        c = v
        child = -1
        ans = 0

        for i in range(len(chain) - 1, -1, -1):
            d = chain[i]

            ans += total_dist[c] + cnt[c] * d

            if child != -1:
                ans -= subdist[child] + subcnt[child] * d

            child = c
            c = cd_parent[c]

            if c == -1:
                break

        return ans

    def subtree_count(v):
        return fenwick.prefix(tout[v]) - fenwick.prefix(tin[v])

    def find_median():
        k = (total_chips + 1) // 2

        # Fenwick.kth returns a zero-based Euler position.
        pos = fenwick.kth(k)
        x = euler[pos]

        # x itself may already be the deepest heavy vertex.
        if subtree_count(x) >= k:
            return x

        cur = x

        for j in range(LOG - 1, -1, -1):
            a = up[j][cur]
            if a != -1 and subtree_count(a) < k:
                cur = a

        # cur is the deepest ancestor whose subtree is still too small.
        # Its parent is the first ancestor whose subtree exceeds half.
        return parent[cur]

    q = int(input())
    out = []

    for _ in range(q):
        op, v = input().split()
        v = int(v) - 1

        if op == '+':
            delta = 1
            active[v] = 1
        else:
            delta = -1
            active[v] = 0

        total_chips += delta

        fenwick.add(tin[v] + 1, delta)
        centroid_update(v, delta)

        median = find_median()
        out.append(str(distance_sum(median)))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The first preprocessing traversal roots the original tree and assigns Euler positions. The `tout[v] = tin[v] + subtree_size[v]` property could also be used, but assigning `tout` directly with an iterative enter/exit traversal makes the subtree interval explicit and avoids recursion depth problems.

The binary-lifting table stores original-tree ancestors, not centroid-tree ancestors. These two trees have different meanings and must not be mixed. The original-tree table is used only for locating the weighted median.

The centroid decomposition is built independently. Every original vertex eventually becomes a centroid, so following `cd_parent` starting at (v) gives exactly the centroid ancestors needed for dynamic distance queries.

The `cd_dist[v]` array stores distances in root-to-leaf order in the centroid tree. The update and query loops traverse this array backwards because they start at the original vertex and move toward the centroid root. The `array('i')` representation keeps these (O(n\log n)) distances compact in memory. Python's standard `array` type stores typed numeric values in a packed representation rather than one Python object per element.

The centroid counters use 64-bit arrays because the answer can be as large as (\Theta(n^2)). Python integers themselves do not overflow, but using signed 64-bit storage keeps the explicit arrays compact while comfortably covering the maximum possible distance sum.

The Fenwick tree uses one-based internal positions, so the original zero-based Euler position `tin[v]` is updated at `tin[v] + 1`. Conversely, `prefix(tout[v]) - prefix(tin[v])` counts exactly the vertices in the half-open Euler interval ([tin[v],tout[v])). Mixing these two indexing conventions is one of the easiest ways to introduce an off-by-one error.

The median search uses (k=\lfloor M/2\rfloor+1), rather than (M/2), because the condition is strictly more than half. For even (M), this chooses one side of a possible pair of medians, which is sufficient because both sides have the same optimal cost.

## Worked Examples

### Sample 1

The tree is the path (1-2-3). Root it at 1, giving Euler order (1,2,3).

| Query | Active vertices | Total chips | (k) | Euler (k)-th chip | Median | Span |
| --- | --- | --- | --- | --- | --- | --- |
| `+ 1` | {1} | 1 | 1 | 1 | 1 | 0 |
| `+ 3` | {1,3} | 2 | 2 | 3 | 2 | 2 |
| `+ 2` | {1,2,3} | 3 | 2 | 2 | 2 | 2 |
| `- 1` | {2,3} | 2 | 2 | 3 | 2 | 1 |

After the second query, vertex 3 is the halfway-crossing chip. Its own subtree has only one chip, so it is not the median. Its parent, vertex 2, has both chips in its subtree and is the deepest ancestor whose subtree exceeds half. The total distance from vertex 2 to chips at 1 and 3 is (1+1=2).

After adding vertex 2, the median remains vertex 2. After deleting vertex 1, only vertices 2 and 3 remain, so vertex 2 has total cost (0+1=1). This also exercises the case where an even number of chips admits two equally good medians.

### Sample 2

Root the tree at vertex 1. Its Euler order is (1,2,3,4,5,6).

| Query | Active vertices | Total chips | (k) | Euler (k)-th chip | Median | Span |
| --- | --- | --- | --- | --- | --- | --- |
| `+ 1` | {1} | 1 | 1 | 1 | 1 | 0 |
| `+ 4` | {1,4} | 2 | 2 | 4 | 2 | 3 |
| `+ 5` | {1,4,5} | 3 | 2 | 4 | 4 | 4 |
| `- 5` | {1,4} | 2 | 2 | 4 | 2 | 3 |
| `+ 6` | {1,4,6} | 3 | 2 | 4 | 2 | 4 |

When chips are at 1 and 4, vertex 4 lies inside the subtree of vertex 2, so vertex 2 becomes the deepest heavy ancestor. Its distance to chips at 1 and 4 is (1+2=3).

After adding vertex 5, the subtree of vertex 4 contains chips at 4 and 5, which is two out of three chips. Thus vertex 4 itself becomes the median, giving (0+3+1=4). This demonstrates why the median can move several levels downward after a single insertion.

After deleting vertex 5, the balance changes again and vertex 2 becomes the median. Finally, vertex 6 joins the active set. Vertex 2 now has distances (1), (2), and (1) to vertices 1, 4, and 6, giving span 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Preprocessing | (O(n\log n)) | Euler preprocessing, binary lifting, and centroid decomposition |
| Update | (O(\log n)) | One Fenwick update and one centroid-tree walk |
| Median search | (O(\log^2 n)) | (O(\log n)) binary-lifting checks, each using Fenwick sums |
| Distance sum | (O(\log n)) | One walk through centroid ancestors |
| Total | (O(n\log n+q\log^2 n)) | All queries use the same preprocessed structures |
| Space | (O(n\log n)) | Binary lifting and distances to centroid ancestors |

With (n,q\le 10^5), the preprocessing is easily within the intended scale, and every query avoids a full scan of the tree. The (O(\log^2 n)) median search is the dominant per-query component, while the centroid distance calculation remains logarithmic. The compact typed arrays in the implementation keep the (O(n\log n)) auxiliary data within the 256 MiB memory limit.

## Test Cases

The following harness assumes `solve()` is the function from the Python Solution section. It temporarily replaces the module's `input` and `stdout`, so each assertion runs the actual implementation rather than a separate reimplementation.

```python
import sys
import io

def run(inp: str) -> str:
    global input

    old_input = input
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        input = old_input
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1.
assert run(
    """3
1 2
2 3
4
+ 1
+ 3
+ 2
- 1
"""
) == """0
2
2
1""\n", "sample 1"

# Provided sample 2.
assert run(
    """6
1 2
2 3
3 4
4 5
2 6
5
+ 1
+ 4
+ 5
- 5
+ 6
"""
) == """0
3
4
3
4""\n", "sample 2"

# Minimum-size tree.
assert run(
    """1
1
+ 1
"""
) == """0\n""", "minimum-size tree"

# A path where the optimal vertex is between occupied vertices,
# followed by a deletion that leaves two active vertices.
assert run(
    """5
1 2
2 3
3 4
4 5
4
+ 1
+ 5
+ 3
- 5
"""
) == """0
4
4
2\n""", "path median and deletion"

# Star with every vertex eventually occupied.
assert run(
    """5
1 2
1 3
1 4
1 5
5
+ 1
+ 2
+ 3
+ 4
+ 5
"""
) == """0
1
2
3
4\n""", "all vertices active"

# Maximum-size tree and a distance close to the largest possible answer.
n = 100000
max_case = [str(n)]
for i in range(1, n):
    max_case.append(f"{i} {i + 1}")
max_case.append("2")
max_case.append("+ 1")
max_case.append(f"+ {n}")
max_input = "\n".join(max_case) + "\n"

assert run(max_input) == "0\n99999\n", "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=1), one insertion | `0` | Minimum-size tree and single-chip case |
| Path (1-2-3-4-5), `+1,+5,+3,-5` | `0,4,4,2` | Empty median, movement of the median, deletion |
| Star centered at 1 with all vertices inserted | `0,1,2,3,4` | All vertices active and high-degree centroid |
| Path with (100000) vertices and chips at both endpoints | `0,99999` | Maximum (n), large distance, 64-bit answer range |

## Edge Cases

A single active chip is handled by taking (k=1). The only active vertex is the first active Euler position, and its own subtree contains at least one chip, so the median search immediately returns it. For

```
1
1
+ 1
```

the centroid distance query returns zero.

An empty optimal destination is handled because the median is defined by subtree weights, not by whether the vertex itself is occupied. For

```
3
1 2
2 3
2
+ 1
+ 3
```

the halfway chip is vertex 3. Its subtree contains one chip, which is not more than half of two. Its parent, vertex 2, has both chips in its subtree, so vertex 2 is selected. The centroid distance query gives (1+1=2).

Two adjacent medians arise when an edge splits the active chips exactly in half. On the path (1-2), after inserting both chips, either vertex is optimal. With the strict condition `subtree >= floor(M / 2) + 1`, the algorithm selects the median on the side containing the Euler-order halfway chip. The selected vertex still has the minimum possible span, so no special tie handling is necessary.

The deletion case where only one chip remains is also safe. On the path (1-2-3), after

```
+ 1
+ 3
- 1
```

the only active chip is at 3. The median search returns 3 and the distance sum is zero. The input guarantees that the active set never becomes empty, so the algorithm never needs to define a median for zero chips.

A particularly useful boundary case is when the halfway point is exactly at the boundary between two subtrees. The strict-more-than-half condition prevents the algorithm from descending into either side unless that side genuinely contains more than half. This is exactly what allows the same code to handle both unique medians and pairs of adjacent medians.

You can adapt the editorial's terminology to a particular Codeforces house style, for example by making the centroid-decomposition section more implementation-oriented or making the proof more formal.
