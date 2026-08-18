---
title: "CF 102201F - Fruit Tree"
description: "We have a tree with one fruit type assigned to every vertex. For each query, two vertices s and e define a unique path, and we have to determine whether some fruit type occurs on that path strictly more than all other vertices combined. If such a type exists, we print it."
date: "2026-08-18T10:25:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "F"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 331
verified: true
draft: false
---

[CF 102201F - Fruit Tree](https://codeforces.com/problemset/problem/102201/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with one fruit type assigned to every vertex. For each query, two vertices `s` and `e` define a unique path, and we have to determine whether some fruit type occurs on that path strictly more than all other vertices combined. If such a type exists, we print it. Otherwise we print `-1`. The official constraints allow both `N` and `Q` to reach `250000`, with a 3 second time limit and 1024 MB of memory.

The key difficulty is that the queried object is a tree path rather than a contiguous interval in an array. A path can contain `O(N)` vertices, and there can be `O(N)` queries, so explicitly walking every path can require `O(NQ)` operations. With `N = Q = 250000`, that is roughly `6.25 * 10^10` vertex visits, far beyond what can fit into a few seconds. We need both preprocessing close to `O(N log N)` and a query close to `O(log N)`.

Several boundary cases are easy to mishandle. First, a path consisting of one vertex always has a majority. For example,

```
1 1
7
1 1
```

has output

```
7
```

A solution that only checks paths of length at least two would incorrectly print `-1`.

Second, equality is not enough. For

```
3 1
1 2 1
1 2
2 3
1 3
```

the path contains `1, 2, 1`, so the answer is `1`. But for

```
4 1
1 2 1 2
1 2
2 3
3 4
1 4
```

the counts are `2` and `2`, so the answer is `-1`. A careless implementation using `>= half` would incorrectly report a majority.

Third, the lowest common ancestor belongs to the path and must be counted exactly once. For example,

```
3 1
1 2 1
1 2
1 3
2 3
```

has path `2 -> 1 -> 3`, whose fruit types are `2, 1, 1`, so the answer is `1`. A path formula that subtracts the LCA twice without adding it back would see only one occurrence of `1` and produce the wrong result.

## Approaches

The direct solution is straightforward. For every query, find the LCA of the two endpoints and walk upward from both endpoints until reaching the LCA. While walking, count the fruit types in a dictionary and then check whether one count is greater than half the path length. This is correct because every vertex on the path is visited exactly once.

The problem is the worst-case operation count. Consider a tree that is simply a chain and queries whose endpoints are the two ends of that chain. Every query visits `N` vertices. With `Q = 250000` and `N = 250000`, this can reach about `6.25 * 10^10` vertex operations, even before accounting for dictionary operations and LCA computation. The brute force works because it explicitly obtains the complete frequency distribution of a path, but it fails because the same long paths may be traversed again and again.

The useful observation is that the tree is static. Root the tree at vertex `1`. For every vertex `u`, imagine a frequency table containing all fruit types on the path from the root to `u`. If we could store that table for every `u`, the frequency of a fruit type on an arbitrary path could be obtained by combining four root-to-vertex tables.

A persistent segment tree gives exactly those tables without copying an entire frequency array. The version belonging to `u` is obtained from the version belonging to `parent[u]` by increasing the count of `color[u]`. One update creates only `O(log N)` new segment-tree nodes, so all root-to-vertex versions require `O(N log N)` memory and construction time.

Suppose `w = LCA(u, v)` and `p = parent[w]`. The frequency distribution of the path `u -> v` is

```
root[u] + root[v] - root[w] - root[p].
```

The subtraction of `root[w]` and `root[p]` removes every vertex above the LCA and keeps the LCA itself exactly once. This is the same persistent-tree idea used for tree path frequency queries, and the specific Fruit Tree problem is commonly categorized under persistent segment tree solutions.

There is one more observation that removes the need for a separate candidate-verification pass. Suppose the whole path has length `L`, and its majority type occurs `M > L/2` times. Split the color domain into two halves. The half containing the majority type must contain more than `L/2` vertices. Consequently, when descending the segment tree, if the left half contains more than half of the current path's vertices, the majority must be there. Otherwise, if the right half contains more than half, it must be there. If neither half contains more than half, no majority exists.

After choosing the half containing the majority, the same argument applies recursively. We reach one color after `O(log N)` levels. This gives an exact, deterministic query rather than a randomized candidate search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NQ)` worst case | `O(N)` | Too slow |
| Optimal | `O(N log N + Q log N)` | `O(N log N)` | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `1` and compute `parent[u]` and `depth[u]` for every vertex. The parent relation gives us the root-to-vertex paths needed by the persistent segment trees, while the depths are used to compute LCAs.
2. Build binary-lifting tables for the parents. `up[k][u]` stores the `2^k`-th ancestor of `u`. Binary lifting lets us find `LCA(u, v)` in `O(log N)` time instead of walking through the tree.
3. Build a persistent segment-tree version `root[u]` for every vertex. Version `root[u]` represents the frequency of every fruit type on the path from vertex `1` to `u`. Starting from `root[parent[u]]`, insert one occurrence of `color[u]`.
4. For a query `(u, v)`, compute `w = LCA(u, v)` and let `p = parent[w]`. The frequency of every fruit type on the queried path is represented by the four persistent roots `root[u]`, `root[v]`, `root[w]`, and `root[p]`.
5. Compute the total path length as `depth[u] + depth[v] - 2 * depth[w] + 1`. The `+1` accounts for the LCA itself.
6. Start at the root of the color segment tree, whose interval is `[1, N]`. Calculate how many vertices on the queried path have colors in the left half. This is obtained by adding the left-child counts of `root[u]` and `root[v]` and subtracting the corresponding counts from `root[w]` and `root[p]`.
7. If the left-half count is greater than half of the total path length, descend into the left child. Otherwise, calculate the right-half count. If the right-half count is greater than half, descend into the right child. If neither side exceeds half, the queried path has no majority, so return `-1`.
8. Repeat the descent until the segment contains a single color. That color is the only possible majority, and because every decision was based on the exact frequency in the queried path, it is safe to print it.

The invariant during the segment-tree descent is that whenever we continue into a child, that child contains more than half of all vertices represented by the current segment. A genuine majority must satisfy this property at every level because its entire count lies inside the child containing its color. If neither child has more than half, no individual color in either child can have more than half of the path. At the leaf, the surviving color is consequently a majority exactly when every previous decision was valid.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    input = sys.stdin.buffer.readline

    n, q = map(int, input().split())
    color = [0] + list(map(int, input().split()))

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    # Root the tree at 1.
    parent = array('i', [0]) * (n + 1)
    depth = array('i', [0]) * (n + 1)

    # root[u] is the persistent segment-tree root for root -> u.
    root = array('i', [0]) * (n + 1)

    # Every insertion creates at most bit_length(n) + 1 nodes.
    max_nodes = n * (n.bit_length() + 1) + 5

    left = array('i', [0]) * max_nodes
    right = array('i', [0]) * max_nodes
    count = array('i', [0]) * max_nodes

    nodes = 0

    def update(previous, pos):
        nonlocal nodes

        # Clone the root of the previous version.
        nodes += 1
        new_root = nodes
        left[new_root] = left[previous]
        right[new_root] = right[previous]
        count[new_root] = count[previous] + 1

        old = previous
        cur = new_root
        lo = 1
        hi = n

        while lo < hi:
            mid = (lo + hi) >> 1

            if pos <= mid:
                old_child = left[old]

                nodes += 1
                new_child = nodes

                left[new_child] = left[old_child]
                right[new_child] = right[old_child]
                count[new_child] = count[old_child] + 1

                left[cur] = new_child

                old = old_child
                cur = new_child
                hi = mid
            else:
                old_child = right[old]

                nodes += 1
                new_child = nodes

                left[new_child] = left[old_child]
                right[new_child] = right[old_child]
                count[new_child] = count[old_child] + 1

                right[cur] = new_child

                old = old_child
                cur = new_child
                lo = mid + 1

        return new_root

    # Build parent/depth and persistent roots in one DFS.
    stack = [1]

    while stack:
        u = stack.pop()

        root[u] = update(root[parent[u]], color[u])

        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)

    # Binary lifting table.
    log = n.bit_length()
    up = [parent]

    for k in range(1, log):
        prev = up[-1]
        cur = array('i', [0]) * (n + 1)

        for u in range(1, n + 1):
            cur[u] = prev[prev[u]]

        up.append(cur)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0

        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(log - 1, -1, -1):
            ua = up[k][a]
            ub = up[k][b]
            if ua != ub:
                a = ua
                b = ub

        return parent[a]

    output = []

    for _ in range(q):
        u, v = map(int, input().split())

        w = lca(u, v)
        pw = parent[w]

        total = depth[u] + depth[v] - 2 * depth[w] + 1

        ru = root[u]
        rv = root[v]
        rw = root[w]
        rp = root[pw]

        lo = 1
        hi = n

        while lo < hi:
            mid = (lo + hi) >> 1

            lu = left[ru]
            lv = left[rv]
            lw = left[rw]
            lp = left[rp]

            left_count = (
                count[lu] + count[lv]
                - count[lw] - count[lp]
            )

            if left_count * 2 > total:
                ru = lu
                rv = lv
                rw = lw
                rp = lp
                hi = mid
            else:
                ru = right[ru]
                rv = right[rv]
                rw = right[rw]
                rp = right[rp]
                lo = mid + 1

        # If neither side had a strict majority, the descent could
        # have followed an arbitrary right side. Verify the leaf.
        candidate = lo

        occurrences = (
            count[ru] + count[rv]
            - count[rw] - count[rp]
        )

        if occurrences * 2 > total:
            output.append(str(candidate))
        else:
            output.append("-1")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The graph is stored as ordinary adjacency lists because each edge is needed only while rooting the tree. The parent and depth arrays use compact integer arrays, which keeps Python memory usage under control at the largest input size.

The persistent segment tree uses three integer arrays. Each new version clones only the nodes along the root-to-leaf route corresponding to one fruit type. The update is written iteratively rather than recursively because there can be millions of persistent nodes, and avoiding millions of Python function calls makes a substantial difference.

The zeroth persistent node represents an empty frequency table. Consequently, when the LCA is the root, `parent[w]` is zero and `root[0]` is still the empty version. This removes a special case from the path-frequency formula.

The four-root formula is the central implementation detail. `root[u]` and `root[v]` contain the two root paths, while subtracting `root[w]` and `root[parent[w]]` removes every root-to-LCA contribution twice except for the LCA itself. The resulting count is exactly the frequency on `u -> v`.

The final leaf is checked once more. During the descent, if the left child contains more than half of the path, we must enter it. If it does not, the right child is the only possible location for a majority. The final check also makes the code robust against the case where the descent reaches a leaf after repeatedly taking a side that did not itself contain a strict majority.

All counts are at most `N`, so ordinary Python integers are already more than sufficient. There is no integer-overflow issue in Python.

## Worked Examples

The official sample has seven vertices. Its tree contains several occurrences of fruit type `1`, and the queries exercise both majority and non-majority paths.

For the first query, `1 -> 4`, the path is

```
1 -> 3 -> 5 -> 4
```

with colors

```
3, 1, 1, 2
```

No color occurs more than twice, so the answer is `-1`.

For the second query, `7 -> 2`, the path is

```
7 -> 5 -> 3 -> 2
```

with colors

```
2, 1, 1, 1
```

Color `1` occurs three times out of four, so it is the majority.

| Query | LCA | Path colors | Total | Majority candidate | Candidate count | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `1 4` | `1` | `3,1,1,2` | 4 | `1` | 2 | `-1` |
| `7 2` | `3` | `2,1,1,1` | 4 | `1` | 3 | `1` |
| `3 3` | `3` | `1` | 1 | `1` | 1 | `1` |
| `4 7` | `5` | `2,1,1,2` | 4 | `2` | 2 | `-1` |

The fourth row shows why equality is not sufficient. The actual official output has `2` for the fourth query because the path is `4 -> 5 -> 7`, not the four-vertex sequence shown by an incorrectly reconstructed path. Its colors are `2,1,2`, giving type `2` two occurrences out of three. This is exactly why the LCA and endpoint-inclusive path formula must be handled carefully. The official sample output is `-1, 1, 1, 2`.

A smaller example makes the persistent-tree descent easier to see:

```
5 2
1 2 2 3 2
1 2
2 3
3 4
4 5
1 5
2 4
```

The first path contains `1,2,2,3,2`. Its total size is `5`, and color `2` occurs `3` times. During the color-domain descent, the segment containing color `2` retains more than half of the path's frequency at every necessary level.

| Query | Path | Total | Candidate | Count | Result |
| --- | --- | --- | --- | --- | --- |
| `1 5` | `1,2,2,3,2` | 5 | 2 | 3 | `2` |
| `2 4` | `2,2,3` | 3 | 2 | 2 | `2` |

The second query is also useful because the LCA is an endpoint. When `w = 2`, the expression `root[u] + root[v] - root[w] - root[parent[w]]` still counts vertex `2` exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N log N + Q log N)` | Each vertex creates `O(log N)` persistent nodes, each LCA costs `O(log N)`, and each majority query descends `O(log N)` segment-tree levels |
| Space | `O(N log N)` | The persistent segment tree has `O(N log N)` nodes, while the graph and binary-lifting table use `O(N log N)` or less |

The largest instance has `250000` vertices and `250000` queries. A linear scan of every queried path can reach tens of billions of operations, while the persistent construction performs only `O(N log N)` updates and every query performs only logarithmic work. The 1024 MB memory limit is also unusually generous for a persistent structure, which is appropriate because roughly several million persistent segment-tree nodes are required.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above. The maximum-size test is generated rather than written literally, because its input would contain hundreds of thousands of lines.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.TextIOWrapper(io.BytesIO(inp.encode()))
        sys.stdout = io.StringIO()
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official sample
sample1 = """\
7 4
3 1 1 2 1 1 2
1 3
7 5
2 3
5 3
5 6
4 5
1 4
7 2
3 3
4 7
"""

assert run(sample1) == " -1".strip() + "\n1\n1\n2", "official sample"

# Minimum-size input.
sample2 = """\
1 3
9
1 1
1 1
1 1
"""

assert run(sample2) == "9\n9\n9", "single vertex"

# All colors equal.
sample3 = """\
5 3
4 4 4 4 4
1 2
2 3
3 4
4 5
1 5
2 4
3 3
"""

assert run(sample3) == "4\n4\n4", "all equal"

# Exact half is not a majority.
sample4 = """\
4 3
1 2 1 2
1 2
2 3
3 4
1 4
1 3
2 4
"""

assert run(sample4) == "-1\n1\n2", "strict majority boundary"

# LCA is an endpoint, and the path is not rooted at either endpoint.
sample5 = """\
5 4
1 2 2 3 2
1 2
2 3
3 4
4 5
1 5
2 4
2 5
3 5
"""

assert run(sample5) == "2\n2\n2\n2", "LCA and endpoint cases"

# Maximum-size generated test.
# A chain makes the tree as deep as possible.
# All colors are distinct, so every path of length > 1 has no majority.
n = 250000
q = 250000

parts = [f"{n} {q}\n"]
parts.append(" ".join(map(str, range(1, n + 1))) + "\n")

for i in range(1, n):
    parts.append(f"{i} {i + 1}\n")

for i in range(q):
    if i & 1:
        parts.append(f"1 {n}\n")
    else:
        parts.append(f"{i + 1} {i + 1}\n")

large_input = "".join(parts)
large_output = run(large_input)

lines = large_output.splitlines()

assert len(lines) == q, "maximum-size query count"

for i, ans in enumerate(lines):
    if i & 1:
        assert ans == "-1", "maximum-size non-majority path"
    else:
        assert ans == str(i + 1), "maximum-size singleton path"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `-1, 1, 1, 2` | General tree paths and the official behavior |
| Single vertex | `9` for every query | Minimum size and endpoint-inclusive paths |
| All colors equal | `4` for every query | Persistent counts when one color dominates completely |
| `1,2,1,2` chain | `-1,1,2` | Strictly greater than half, not greater than or equal |
| LCA endpoint cases | `2` for every query | Correct four-root path formula |
| Generated maximum case | Singleton colors, otherwise `-1` | Maximum `N`, maximum `Q`, deep tree, and scalability |

## Edge Cases

The single-vertex case

```
1 1
7
1 1
```

has `w = 1`, `parent[w] = 0`, and `total = 1`. The four-root expression becomes `root[1] + root[1] - root[1] - root[0]`, leaving exactly one occurrence of color `7`. The segment-tree descent reaches color `7`, whose count is `1`, so the output is `7`.

The exact-half case

```
4 1
1 2 1 2
1 2
2 3
3 4
1 4
```

has path colors `1,2,1,2`. Both colors occur twice, while a majority requires a count strictly greater than `4/2 = 2`. During the segment-tree descent, neither color range can legitimately be declared dominant, and the final count check rejects the candidate. The answer is `-1`.

The LCA correction case

```
3 1
1 2 1
1 2
1 3
2 3
```

has `w = 1` and `parent[w] = 0`. The path frequency is computed as

```
root[2] + root[3] - root[1] - root[0].
```

The root-to-`2` version contains colors `1,2`, the root-to-`3` version contains `1,1`, and subtracting the root version removes one duplicate copy of the LCA while subtracting the empty version changes nothing. The resulting path is `2,1,1`, so color `1` has count `2` and the answer is `1`.

The endpoint-LCA case is handled by the same formula. For

```
5 1
1 2 2 3 2
1 2
2 3
3 4
4 5
2 4
```

the LCA is vertex `2`, which is also the first endpoint. The path is `2 -> 3 -> 4`, with colors `2,2,3`. The formula using `root[2]`, `root[4]`, `root[2]`, and `root[1]` leaves exactly those three vertices, so color `2` has frequency `2` and the answer is `2`.

The no-majority case can also occur on a long path even when one color looks frequent globally. The query only considers vertices on its particular path. The persistent segment tree avoids confusing global frequency with path frequency because every count is formed from the four versions corresponding to the two endpoints and their LCA.

Finally, the largest possible depth is handled iteratively. A recursive DFS can exceed Python's recursion limit on a chain with `250000` vertices, while the implementation uses an explicit stack. The persistent segment-tree update is also iterative, keeping the Python call stack independent of the tree depth.
