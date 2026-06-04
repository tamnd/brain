---
title: "CF 231E - Cactus"
description: "We are given a connected undirected graph that is guaranteed to be a vertex cactus. In a vertex cactus, every vertex belongs to at most one simple cycle. Cycles may touch the rest of the graph through articulation points, but two different cycles can never share a vertex."
date: "2026-06-04T09:14:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 2100
weight: 231
solve_time_s: 155
verified: false
draft: false
---

[CF 231E - Cactus](https://codeforces.com/problemset/problem/231/E)

**Rating:** 2100  
**Tags:** data structures, dfs and similar, dp, graphs, trees  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph that is guaranteed to be a vertex cactus. In a vertex cactus, every vertex belongs to at most one simple cycle. Cycles may touch the rest of the graph through articulation points, but two different cycles can never share a vertex.

For each query `(x, y)`, we must count how many distinct simple paths start at `x` and end at `y`. Two paths are considered different if their sets of edges differ. The answer is required modulo `10^9 + 7`.

The graph has up to `10^5` vertices, `10^5` edges, and `10^5` queries. Any solution that processes a query by exploring the graph directly is immediately ruled out. Even an `O(n)` computation per query would require around `10^10` operations in the worst case.

The cactus restriction is the entire point of the problem. In a general graph, counting simple paths is extremely difficult. In a cactus, every cycle behaves independently, and the graph can be compressed into a tree-like structure.

A subtle case occurs when both queried vertices lie inside the same cycle.

Example:

```
1-2
| |
4-3
```

Query `(1,3)` has two simple paths:

```
1-2-3
1-4-3
```

A tree-based approach that assumes uniqueness of paths would incorrectly return `1`.

Another important case is when the route between two vertices passes through several cycles.

Example:

```
cycle A -- bridge -- cycle B
```

Any simple path from one side to the other must choose one direction inside cycle A and one direction inside cycle B. The answer becomes `2 * 2 = 4`.

A careless implementation that only checks the endpoints' cycles would miss this multiplication effect.

A third edge case is when the path touches a cycle through its articulation vertex but does not need to traverse the cycle. Such a cycle contributes nothing. Only cycles lying on the compressed-tree path between the endpoints matter.

## Approaches

The brute force idea is to enumerate all simple paths between the queried vertices.

This is correct because the problem directly asks for the number of simple paths. Unfortunately, even a single query can have exponentially many simple paths in a graph with many cycles. With up to `10^5` queries, this is hopeless.

The cactus property changes the structure dramatically. Since every vertex belongs to at most one cycle, every biconnected component is either a single edge or a single cycle.

Think about what happens when we contract every cycle into one special node.

The resulting structure becomes a tree, often called the block-cut tree of the cactus.

Original vertices become one type of node.

Each cycle becomes another type of node.

Every vertex that belongs to a cycle is connected to that cycle-node.

Because cycles never overlap, this graph is a tree.

Now consider a query. Between two vertices in a tree there is exactly one route. Whenever that route passes through a cycle-node, there are exactly two ways to traverse the corresponding cycle. One may go around the cycle clockwise or counterclockwise.

Different cycle-nodes contribute independently. If the tree path contains `c` cycle-nodes, the answer is simply:

```
2^c
```

So the problem reduces to:

1. Build the cactus block tree.
2. For each query, count how many cycle-nodes lie on the tree path.
3. Return `2^(count)`.

Counting cycle-nodes on tree paths is a standard LCA problem with prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O((n+m) log n + k log n) | O(n+m) | Accepted |

## Algorithm Walkthrough

### 1. Find all cycle vertices

Run a DFS and compute standard discovery times and low-link values.

Whenever DFS encounters a back edge from a node `u` to an ancestor `v`, the vertices on the DFS stack from `u` back to `v` form one cycle of the cactus.

Because the graph is a vertex cactus, each vertex can belong to at most one such cycle.

We assign an identifier to every discovered cycle.

### 2. Build the block tree

Create nodes of two kinds.

The first `n` nodes correspond to original graph vertices.

Every discovered cycle receives one additional node.

For each vertex contained in a cycle, connect:

```
vertex node <-> cycle node
```

Vertices not belonging to any cycle remain isolated from cycle nodes.

The resulting graph is a tree.

The reason is that every block of a cactus is either an edge or a cycle, and the standard block-cut representation of such a graph is acyclic.

### 3. Mark cycle nodes

Assign weight:

```
0 for original vertices
1 for cycle nodes
```

Later, path sums will count how many cycle-nodes are encountered.

### 4. Preprocess LCA

Root the block tree anywhere, for example at node `1`.

Compute:

```
depth[u]
up[j][u]
pref[u]
```

where `pref[u]` is the number of cycle nodes on the root-to-`u` path.

Binary lifting gives `O(log n)` LCA queries.

### 5. Answer a query

Let `a` and `b` be the original vertex nodes.

Find:

```
l = LCA(a,b)
```

The number of cycle nodes on the tree path is:

```
cnt =
pref[a] + pref[b]
- 2 * pref[l]
+ weight[l]
```

Every such cycle contributes a factor of two.

The answer is:

```
2^cnt mod MOD
```

### Why it works

After replacing every cycle by a dedicated cycle-node, the cactus becomes a tree. Any route between two vertices in the original graph corresponds to the unique tree path between their corresponding nodes.

Whenever this tree path passes through a cycle-node, the original path enters the cycle through one cycle vertex and leaves through another. A simple cycle offers exactly two distinct simple routes between those vertices, one in each direction around the cycle.

Choices made inside different cycles are independent because different cycles share no vertices. Thus every encountered cycle doubles the number of valid simple paths.

The tree-path cycle count is exactly the number of independent binary choices, so the answer equals `2^(cycle count)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

n, m = map(int, input().split())

g = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

tin = [0] * (n + 1)
low = [0] * (n + 1)
parent = [0] * (n + 1)
timer = 0

cycles = []
stack = []

sys.setrecursionlimit(300000)

def dfs(u, p):
    global timer
    timer += 1
    tin[u] = low[u] = timer

    for v in g[u]:
        if v == p:
            continue

        if not tin[v]:
            parent[v] = u
            dfs(v, u)
            low[u] = min(low[u], low[v])
        elif tin[v] < tin[u]:
            low[u] = min(low[u], tin[v])

            cyc = [v]
            cur = u
            while cur != v:
                cyc.append(cur)
                cur = parent[cur]
            cycles.append(cyc)

dfs(1, 0)

tot = n + len(cycles)
tree = [[] for _ in range(tot + 1)]

for idx, cyc in enumerate(cycles, start=1):
    cid = n + idx
    for v in cyc:
        tree[cid].append(v)
        tree[v].append(cid)

LOG = (tot + 1).bit_length()

depth = [0] * (tot + 1)
pref = [0] * (tot + 1)
up = [[0] * (tot + 1) for _ in range(LOG)]
weight = [0] * (tot + 1)

for i in range(n + 1, tot + 1):
    weight[i] = 1

def dfs_tree(u, p):
    up[0][u] = p

    if p:
        pref[u] = pref[p] + weight[u]
        depth[u] = depth[p] + 1
    else:
        pref[u] = weight[u]

    for v in tree[u]:
        if v != p:
            dfs_tree(v, u)

dfs_tree(1, 0)

for j in range(1, LOG):
    prev = up[j - 1]
    cur = up[j]
    for v in range(1, tot + 1):
        cur[v] = prev[prev[v]]

pow2 = [1] * (len(cycles) + 1)
for i in range(1, len(pow2)):
    pow2[i] = (pow2[i - 1] * 2) % MOD

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

    for j in range(LOG - 1, -1, -1):
        if up[j][a] != up[j][b]:
            a = up[j][a]
            b = up[j][b]

    return up[0][a]

q = int(input())

ans = []

for _ in range(q):
    a, b = map(int, input().split())

    l = lca(a, b)

    cnt = (
        pref[a]
        + pref[b]
        - 2 * pref[l]
        + weight[l]
    )

    ans.append(str(pow2[cnt]))

sys.stdout.write("\n".join(ans))
```

After finding all cycles, the code creates one extra node for every cycle and connects that node to all vertices belonging to the cycle. This is the crucial compression step.

The DFS on the block tree computes both binary-lifting ancestors and the prefix count of cycle-nodes. The prefix count allows any path sum to be recovered with the standard LCA formula.

A subtle point is that cycle-nodes themselves carry weight `1`, while ordinary vertices carry weight `0`. This makes the path sum equal to the number of cycles encountered.

Another detail is precomputing powers of two. The maximum number of cycles is at most `m`, so a simple linear precomputation is sufficient.

## Worked Examples

### Sample 1

The graph contains two cycles:

```
1-2-3-4-1
6-7-8-6
```

The compressed tree contains two cycle-nodes.

Query `(9,2)`:

| Node on compressed path | Type | Contribution |
| --- | --- | --- |
| 9 | vertex | 0 |
| 7-cycle | cycle | 1 |
| 6 | vertex | 0 |
| 5 | vertex | 0 |
| 3 | vertex | 0 |
| 4-cycle | cycle | 1 |
| 2 | vertex | 0 |

Total cycle count = 2.

Answer:

```
2^2 = 4
```

which matches the sample.

This demonstrates that cycle contributions multiply independently.

### Custom Example

Input:

```
4 4
1 2
2 3
3 4
4 1
1
1 3
```

Compressed tree:

| Tree Node | Type |
| --- | --- |
| 1 | vertex |
| 2 | vertex |
| 3 | vertex |
| 4 | vertex |
| C | cycle |

Path:

```
1 -> C -> 3
```

Cycle count = 1.

Answer:

```
2^1 = 2
```

The two paths are:

```
1-2-3
1-4-3
```

This confirms the interpretation of a cycle-node as a binary choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) + (n + c) log n + k log n) | DFS, tree preprocessing, and LCA queries |
| Space | O((n + c) log n) | Block tree and binary lifting tables |

Here `c` is the number of cycles, and `c ≤ m`. With all limits around `10^5`, the complexity easily fits within the 2-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from solution import solve
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

# sample 1
assert run(
"""10 11
1 2
2 3
3 4
1 4
3 5
5 6
8 6
8 7
7 6
7 9
9 10
6
1 2
3 5
6 9
9 2
9 3
9 10
"""
) == "\n".join(["2","2","2","4","4","1"])

# tree
assert run(
"""2 1
1 2
1
1 2
"""
) == "1"

# single cycle
assert run(
"""4 4
1 2
2 3
3 4
4 1
1
1 3
"""
) == "2"

# two cycles in chain
assert run(
"""7 8
1 2
2 3
3 1
3 4
4 5
5 6
6 4
6 7
1
1 7
"""
) == "4"

# cycle queried at articulation
assert run(
"""5 5
1 2
2 3
3 1
3 4
4 5
1
5 3
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | 1 | Unique path in a tree |
| Single cycle | 2 | One cycle doubles count |
| Two cycles chained | 4 | Independent multiplication |
| Query ending at articulation | 1 | Cycle not necessarily used |
| Sample 1 | Sample output | Full cactus structure |

## Edge Cases

Consider a graph that is just one cycle:

```
4 4
1 2
2 3
3 4
4 1
1
1 3
```

The compressed path contains exactly one cycle-node. The algorithm returns `2^1 = 2`, corresponding to the two directions around the cycle.

Now consider:

```
5 5
1 2
2 3
3 1
3 4
4 5
1
5 3
```

The path in the block tree is simply:

```
5 -> 4 -> 3
```

The cycle-node is not traversed. The cycle count is zero, so the answer is `1`. This prevents overcounting cycles that merely touch the route.

Finally, consider two cycles connected by a bridge:

```
cycle A -- bridge -- cycle B
```

Any path crossing the graph must choose a direction in cycle A and independently choose a direction in cycle B. The block-tree path contains two cycle-nodes, giving `2^2 = 4`. The multiplicative structure follows directly from the cactus property that cycles never overlap.
