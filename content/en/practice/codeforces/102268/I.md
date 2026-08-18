---
title: "CF 102268I - Interesting Graph"
description: "We are given a simple undirected graph with up to (10^5) vertices and (10^5) edges. For every possible number of available colors (k) from (1) through (n), we need the number of proper vertex colorings using those (k) labeled colors, modulo (998244353)."
date: "2026-08-19T04:33:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "I"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 860
verified: false
draft: false
---

[CF 102268I - Interesting Graph](https://codeforces.com/problemset/problem/102268/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple undirected graph with up to (10^5) vertices and (10^5) edges. For every possible number of available colors (k) from (1) through (n), we need the number of proper vertex colorings using those (k) labeled colors, modulo (998244353).

The unusual condition on the graph is what makes the problem tractable. Take any seven vertices. Among them, two must have some third vertex outside the seven that lies on every path between those two vertices. This condition forces every biconnected component, also called a block, to contain at most six vertices.

To see why, suppose a biconnected component contained at least seven vertices. Choose any seven of its vertices as (A). For any two distinct vertices (a,b\in A), and for any (c\notin A), the vertex (c) cannot separate (a) and (b). If (c) is outside the component, it is irrelevant to paths inside the component. If (c) is another vertex of the component, biconnectivity gives an (a)-(b) path avoiding (c). This contradicts the required property.

The bound (n,m\le 10^5) rules out anything that explores arbitrary vertex subsets, enumerates colorings, or performs a quadratic operation for every vertex. Even (O(n^2)) already means about (10^{10}) basic operations at the upper bound. The useful decomposition has to be essentially linear in the input size, with only a small constant amount of work for every block.

There are several boundary cases that are easy to mishandle. A graph with two vertices and one edge has coloring counts (0,2), because one color cannot separate the endpoints while two colors give two assignments. A graph with three vertices in a path has (0,2,12), since its chromatic polynomial is (k(k-1)^2). A disconnected graph must be handled component by component. For example, two disjoint edges on four vertices have polynomial (k^2(k-1)^2), giving (0,4,36,144). Finally, a complete graph on six vertices is a single allowed block, and its answer is (0,0,0,0,0,720). A careless implementation that assumes every block is a tree edge, or that divides by (k) at the wrong point, gets these cases wrong.

## Approaches

The direct approach is to enumerate every assignment of colors to the vertices. For a fixed (k), there are (k^n) assignments, and checking one assignment against all edges costs (O(m)). Doing this for every (k) gives (O(m\sum_{k=1}^n k^n)), which is already on the order of (m n^n). With (n=10^5), this is not merely too slow, it is completely infeasible.

The useful observation is that the graph can be split at articulation vertices. Once a connected graph is decomposed into its biconnected components, different blocks interact only through a single shared articulation vertex. A coloring of one block can be combined independently with a coloring of the next block once the color of their common articulation vertex has been fixed.

Suppose a connected graph has blocks (B_1,\ldots,B_t). If (P_B(k)) denotes the chromatic polynomial of block (B), then

[
P_G(k)=\frac{\prod_{i=1}^{t}P_{B_i}(k)}{k^{t-1}}.
]

Every block contains at least one edge, so (P_B(k)) is divisible by (k). Define

[
Q_B(k)=\frac{P_B(k)}{k}.
]

Then a connected component contributes

[
k\prod_B Q_B(k).
]

For a graph with (C) connected components, the full answer is

[
P_G(k)=k^C\prod_B Q_B(k).
]

The remaining difficulty is evaluating all these factors for every (k). Each block has at most six vertices, so we can enumerate all partitions of its vertices into independent sets. There are only (203) set partitions of six elements. If (c_t) is the number of valid partitions into exactly (t) independent sets, then

[
P_B(k)=\sum_{t=1}^{|B|}c_t(k)_t,
]

where

[
(k)_t=k(k-1)\cdots(k-t+1).
]

After dividing by (k),

[
Q_B(k)=\sum_{t=1}^{|B|}c_t(k-1)_{t-1}.
]

Thus every block is represented by a tuple of at most six tiny integers.

There are very few different chromatic polynomials for connected graphs on at most six vertices. The known counts are (1,1,2,5,14,50) for sizes (1) through (6), so there are only (72) different connected chromatic polynomials over sizes (2) through (6). We can consequently group blocks having the same coefficient tuple and process each type only once. The original contest discussion describes exactly this small-state classification approach, observing that the number of relevant local polynomials is below (100).

The brute-force computation inside a block is therefore tiny, while the large graph is handled by the block decomposition. This is the key transition from an arbitrary graph-coloring problem to a collection of constant-size problems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(mn^n)) | (O(n+m)) | Too slow |
| Block decomposition and local polynomial classification | (O(n+m+Un)), with (U<100) local types | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Run Tarjan's DFS for biconnected components. Maintain the discovery time and low-link value of every vertex and a stack of traversed edges. Whenever a DFS child (v) satisfies (\operatorname{low}[v]\ge\operatorname{tin}[u]), pop edges until the edge (uv) is removed. Those popped edges form one block. The given graph property guarantees that every resulting block contains at most six vertices.
2. Count the connected components while running the DFS. An isolated vertex has no edge block, but it still contributes a factor (k) to the chromatic polynomial. This is exactly why the final global factor is (k^C).
3. For every block, collect its vertices and translate them to local indices (0,\ldots,s-1), where (s\le6). Encode the block's edges as a bit mask. Since there are at most (\binom 62=15) possible local edges, the entire block fits into a 15-bit integer.
4. Enumerate every set partition of the (s) local vertices. A partition represents one way to decide which vertices receive the same color. The partition is usable exactly when no graph edge has both endpoints in the same part. Count how many valid partitions have (t) parts. These counts are the coefficients (c_t) in the falling-factorial expansion of the block's chromatic polynomial.
5. Store the coefficient tuple as the block's type and count how many blocks have each type. Blocks with the same tuple have exactly the same (Q_B(k)), so there is no reason to evaluate them separately.
6. For each distinct block type, evaluate

[
Q(k)=\sum_t c_t(k-1)_{t-1}
]

for all (k=1,\ldots,n). Because (Q) has degree at most five, its values can be generated using finite differences, avoiding a fresh polynomial evaluation involving five multiplications at every point.

1. Multiply the contribution of the type into the answer. If the type occurs (r) times, its contribution is (Q(k)^r). For one occurrence we multiply directly; for multiple occurrences we use modular exponentiation.
2. After all block types have been processed, multiply every answer by (k^C). The resulting value is the number of proper (k)-colorings of the entire graph.

Why it works: Tarjan's decomposition separates a graph into blocks that intersect only at articulation vertices. Once the color of such an articulation vertex is fixed, the colorings of the incident blocks are independent. A block coloring has (P_B(k)) possibilities, but the shared articulation color is counted once in every incident block, so each additional block contributes a division by (k). This gives (k^C\prod_B(P_B(k)/k)). The local falling-factorial expansion counts every proper coloring exactly once by first partitioning vertices into its nonempty color classes and then assigning distinct labeled colors to those classes. Since every block has at most six vertices, exhaustive enumeration of its independent partitions is exact and constant-sized.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def generate_partitions(n):
    """Return (number_of_parts, internal_pair_mask) for every set partition."""
    if n == 0:
        return [(0, 0)]

    pair_id = [[-1] * n for _ in range(n)]
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            pair_id[i][j] = pair_id[j][i] = bit
            bit += 1

    res = []

    # Restricted-growth strings describe set partitions uniquely.
    a = [0] * n

    def dfs(pos, mx):
        if pos == n:
            mask = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if a[i] == a[j]:
                        mask |= 1 << pair_id[i][j]
            res.append((mx + 1, mask))
            return

        for x in range(mx + 2):
            a[pos] = x
            dfs(pos + 1, max(mx, x))

    a[0] = 0
    dfs(1, 0)
    return res

PARTITIONS = {s: generate_partitions(s) for s in range(2, 7)}

def block_signature(vertices, edge_ids, edges):
    """Return the falling-factorial coefficient tuple of one block."""
    s = len(vertices)

    where = {v: i for i, v in enumerate(vertices)}

    edge_mask = 0
    for eid in edge_ids:
        u, v = edges[eid]
        a = where[u]
        b = where[v]
        if a > b:
            a, b = b, a

        # Pair (a,b) among the s vertices.
        bit = 0
        for i in range(a):
            bit += s - 1 - i
        bit += b - a - 1
        edge_mask |= 1 << bit

    cnt = [0] * s

    for parts, inside in PARTITIONS[s]:
        if edge_mask & inside == 0:
            cnt[parts - 1] += 1

    return tuple(cnt)

def solve():
    n, m = map(int, input().split())

    edges = []
    graph = [[] for _ in range(n)]

    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        graph[u].append((v, eid))
        graph[v].append((u, eid))

    sys.setrecursionlimit(max(1_000_000, 2 * n + 100))

    tin = [0] * n
    low = [0] * n
    timer = 0

    edge_stack = []
    type_count = {}
    components = 0

    def process_component(edge_ids):
        verts = set()
        for eid in edge_ids:
            u, v = edges[eid]
            verts.add(u)
            verts.add(v)

        vertices = list(verts)
        sig = block_signature(vertices, edge_ids, edges)
        type_count[sig] = type_count.get(sig, 0) + 1

    def dfs(u, parent_edge):
        nonlocal timer

        timer += 1
        tin[u] = low[u] = timer

        for v, eid in graph[u]:
            if eid == parent_edge:
                continue

            if tin[v] == 0:
                edge_stack.append(eid)

                dfs(v, eid)

                low[u] = min(low[u], low[v])

                if low[v] >= tin[u]:
                    comp_edges = []

                    while True:
                        x = edge_stack.pop()
                        comp_edges.append(x)
                        if x == eid:
                            break

                    process_component(comp_edges)

            elif tin[v] < tin[u]:
                edge_stack.append(eid)
                low[u] = min(low[u], tin[v])

    for root in range(n):
        if tin[root] == 0:
            components += 1
            dfs(root, -1)

    # ans[k] is the contribution accumulated from all Q_B(k).
    ans = [1] * (n + 1)

    for sig, multiplicity in type_count.items():
        # Q(k) = sum_{t=1}^s c_t * (k-1)_(t-1)
        #
        # Q is degree at most 5. Build its first six values and
        # turn them into forward differences.
        s = len(sig)

        vals = []
        for k in range(1, s + 2):
            x = k - 1
            falling = 1
            value = 0

            for j in range(s):
                if j > 0:
                    falling *= x - (j - 1)
                value += sig[j] * falling

            vals.append(value % MOD)

        # Forward differences.
        diff = vals[:]

        for level in range(s):
            for i in range(s - level):
                diff[i] = (diff[i + 1] - diff[i]) % MOD

        # The current value at k=1 is diff[0].
        cur = diff[:]
        q = diff[0]

        # Apply k=1 first.
        if multiplicity == 1:
            ans[1] = ans[1] * q % MOD
        else:
            ans[1] = ans[1] * pow(q, multiplicity, MOD) % MOD

        # Advance from k to k+1 using finite differences.
        for k in range(2, n + 1):
            for level in range(s - 1):
                cur[level] = (cur[level] + cur[level + 1]) % MOD

            q = cur[0]

            if multiplicity == 1:
                ans[k] = ans[k] * q % MOD
            else:
                ans[k] = ans[k] * pow(q, multiplicity, MOD) % MOD

    # Each connected component contributes one free root color.
    for k in range(1, n + 1):
        ans[k] = ans[k] * pow(k, components, MOD) % MOD

    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The adjacency list stores edge IDs rather than only neighboring vertices. This is necessary because two DFS endpoints can have the same parent vertex only in graphs with parallel edges, which are forbidden here, but using edge IDs makes the parent-edge test precise and avoids special cases.

The Tarjan stack contains each edge exactly once. A tree edge is pushed when its child is first discovered, while a back edge is pushed only when it points toward an already discovered ancestor. When (\operatorname{low}[v]\ge\operatorname{tin}[u]), the stack segment ending at (uv) is exactly one biconnected component.

The local block encoding uses at most fifteen edge bits. The slightly unusual calculation of the bit position is just an indexing scheme for the unordered pairs of the local vertices. Since a block has at most six vertices, the dictionary used to translate global vertex IDs to local IDs stays tiny.

The partition generator uses restricted-growth strings. For example, a partition of four vertices into three groups can be represented by a sequence such as (0,1,2,0). Every set partition has exactly one such representation, so there is neither duplication nor a missing partition. Six vertices give only (203) possibilities.

The signature contains the number of independent partitions with each possible number of parts. The falling-factorial identity

[
P_B(k)=\sum_t c_t(k)_t
]

is exactly why this signature is sufficient. The actual labels of the block's vertices disappear after this computation.

The finite-difference evaluation deserves attention. A degree-(d) polynomial can be evaluated at consecutive integer arguments by maintaining its forward-difference table. Advancing by one argument changes the first difference by the second difference, the second by the third, and so on. Since the degree is at most five, each new value needs only a handful of additions.

Finally, Python's `pow(a,b,MOD)` performs modular exponentiation without constructing the enormous integer (a^b). Every multiplication is reduced modulo (998244353), so there is no integer-growth problem.

## Worked Examples

### Sample 1

The graph has five vertices, with a triangle on vertices (1,3,5) and two isolated vertices. The triangle is one block, while each isolated vertex is its own connected component.

The triangle has chromatic polynomial

[
P_B(k)=k(k-1)(k-2),
]

so its reduced factor is

[
Q_B(k)=(k-1)(k-2).
]

There are three connected components, giving the global factor (k^3).

| (k) | (Q_B(k)) | (k^3) | Answer |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 0 | 8 | 0 |
| 3 | 2 | 27 | 54 |
| 4 | 6 | 64 | 384 |
| 5 | 12 | 125 | 1500 |

The resulting output is `0 0 54 384 1500`. The trace demonstrates why isolated vertices are handled by the connected-component factor rather than by artificial blocks.

### Two triangles sharing one vertex

Consider

```
5 6
1 2
2 3
3 1
3 4
4 5
5 3
```

There are two triangular blocks, sharing vertex (3). The graph is connected, so there is one global factor (k). Each triangle contributes ((k-1)(k-2)).

| (k) | Triangle factor | Product of two factors | Global (k) | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 |
| 2 | 0 | 0 | 2 | 0 |
| 3 | 2 | 4 | 3 | 12 |
| 4 | 6 | 36 | 4 | 144 |
| 5 | 12 | 144 | 5 | 720 |

This example exercises the articulation-vertex multiplication rule. The shared vertex has one color, not two independently chosen colors, which is exactly why the product of block polynomials has to be divided by (k).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m+Un)) | Tarjan is linear, each block has at most six vertices, and there are fewer than (100) relevant local polynomial types |
| Space | (O(n+m)) | Graph storage, DFS arrays, edge stack, and block information are all linear |

The crucial structural fact is that the seven-vertex condition bounds every block by six vertices. The local enumeration is consequently constant-sized, while the number of distinct connected chromatic polynomials on at most six vertices is tiny. With (n,m\le10^5), the resulting computation stays within the intended complexity range and comfortably avoids any dependence on (k^n).

## Test Cases

The following harness assumes the `solve()` function from the solution above is available in the same Python process.

```python
import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin
    return out.getvalue().strip()

# Sample 1: triangle plus two isolated vertices.
assert run(
    """5 3
3 5
5 1
1 3
"""
) == "0 0 54 384 1500", "sample 1"

# Custom 1: minimum valid n with one edge.
assert run(
    """2 1
1 2
"""
) == "0 2", "single edge"

# Custom 2: a path on three vertices.
assert run(
    """3 2
1 2
2 3
"""
) == "0 2 12", "path"

# Custom 3: disconnected graph with two independent edges.
assert run(
    """4 2
1 2
3 4
"""
) == "0 4 36 144", "disconnected components"

# Custom 4: maximum-size block, K6.
assert run(
    """6 15
1 2
1 3
1 4
1 5
1 6
2 3
2 4
2 5
2 6
3 4
3 5
3 6
4 5
4 6
5 6
"""
) == "0 0 0 0 0 720", "K6 boundary"

# Large-size structural test.
# A path is useful for stress-testing the implementation of the block
# decomposition, although it does not satisfy the original seven-vertex
# promise once it becomes long.
n = 100000
edges = "\n".join(f"{i} {i+1}" for i in range(1, n))
large_input = f"{n} {n-1}\n{edges}\n"
large_output = run(large_input).split()

assert len(large_output) == n, "large output length"
assert large_output[0] == "0", "one-color boundary"
assert large_output[1] == str(2), "two-color path boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | `0 2` | Minimum graph and one-edge block |
| `3 2 / 1 2, 2 3` | `0 2 12` | Tree blocks and repeated articulation vertices |
| `4 2 / 1 2, 3 4` | `0 4 36 144` | Multiple connected components |
| (K_6) | `0 0 0 0 0 720` | Maximum allowed block size and falling-factorial enumeration |
| Path with (10^5) vertices | (10^5) values | Large-input Tarjan traversal and output boundaries |

The large stress test deliberately checks the implementation on a graph with the maximum number of vertices. It is not presented as a valid instance of the original promise because a long path contains seven consecutive vertices with no outside separator. Its purpose is to catch stack, traversal, and performance bugs independently of the structural guarantee.

## Edge Cases

For a graph containing a single edge, the only block is (K_2). Its valid independent-set partitions are the partition into two singleton sets, so

[
P_{K_2}(k)=(k)_2=k(k-1).
]

The reduced block factor is (k-1), and one connected component supplies the additional factor (k). For input

```
2 1
1 2
```

the algorithm obtains (0,2).

For a path on three vertices, Tarjan produces two (K_2) blocks. Each contributes (k-1), and the connected component contributes (k). The product is

[
k(k-1)^2.
]

At (k=1,2,3), this gives (0,2,12). The case catches errors where an articulation vertex is accidentally counted twice.

For disconnected graphs, every connected component gets its own free choice of the color of one root vertex. With two disjoint edges, there are two blocks and two connected components, so the formula is

[
k^2(k-1)^2.
]

At (k=2), this gives (4), corresponding to two independent binary choices for the orientations of the two edges.

For (K_6), there is one block containing all six vertices. Every proper coloring needs six distinct colors, so its chromatic polynomial is

[
(k)_6.
]

The block signature has exactly one valid partition for every number of parts from (1) through (6) only where the corresponding partition is compatible with the complete graph. In fact, only the six-singleton partition survives, giving (P(k)=(k)_6). Consequently all values for (k<6) are zero and the value at (k=6) is (6!=720). This catches off-by-one errors in both the partition enumeration and the local falling-factorial evaluation.

The most dangerous implementation mistake is treating a block of size six as if it could have seven local colors or forgetting that (Q_B(k)=P_B(k)/k) uses ((k-1)_{t-1}), not ((k)_t). The (K_6) test exposes both errors immediately.
