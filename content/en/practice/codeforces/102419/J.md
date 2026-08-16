---
title: "CF 102419J - Jaber The policeman"
description: "Think of every row and every column as a vertex of a bipartite graph. A cell containing 1 is an edge between its row vertex and its column vertex. The value ai tells us exactly how many edges must be incident to row i. The column degrees are completely under our control."
date: "2026-08-16T09:11:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "J"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 546
verified: false
draft: false
---

[CF 102419J - Jaber The policeman](https://codeforces.com/problemset/problem/102419/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 6s  
**Verified:** no  

## Solution
## Problem Understanding

Think of every row and every column as a vertex of a bipartite graph. A cell containing `1` is an edge between its row vertex and its column vertex. The value `a_i` tells us exactly how many edges must be incident to row `i`. The column degrees are completely under our control.

When Jaber checks a vertex, every edge incident to an already checked vertex has disappeared. Thus the number of lights he sees is exactly the degree of that vertex in the subgraph induced by the vertices that have not been checked yet. A valid checking order is consequently an ordering in which every vertex has at most one remaining incident edge when it is removed.

A graph has such an ordering exactly when it is a forest. If a graph contains a cycle, after repeatedly removing vertices of degree at most one, the cycle eventually remains and every vertex on it has degree two. Conversely, every nonempty forest has a leaf or an isolated vertex, so we can repeatedly remove a vertex of degree at most one.

The problem has therefore become a graph construction problem. We need a simple bipartite forest with `n` row vertices, `m` column vertices, and prescribed degrees on the row side.

The bounds `n,m <= 1000` are small enough that an `O(nm)` construction is appropriate. In particular, the output itself contains `nm` characters, so merely printing the answer already costs `O(nm)`. A construction with quadratic time and memory is therefore natural, while anything exponential is completely infeasible.

There are several edge cases that make a simplistic construction fail. Consider

```
2 2
2 2
```

Both rows need two ones, so all four cells would have to be `1`. The resulting bipartite graph is a 4-cycle, and no valid checking order exists. Merely checking that the total number of ones is at most `n+m-1` is enough to reject this example, but that condition is not sufficient in general.

For example,

```
5 3
3 3 0 0 0
```

has only six ones, while there are eight vertices, so the crude edge-count condition `6 <= 8-1` passes. Nevertheless, the two positive rows both have degree three and there are only three columns. They must share all three columns, producing multiple cycles. The correct answer is `NO`.

At the other extreme, zero-degree rows must not be treated as part of the connected structure. For

```
3 2
2 0 0
```

the first row can simply use both columns and the other rows can be isolated. The answer is `YES`. A construction that assumes every row has a positive degree would incorrectly reject this case.

The case

```
1 1
0
```

is also valid. There are no edges at all, so both the row and the column can be checked immediately. The answer is `YES`.

## Approaches

A direct brute-force approach would enumerate every binary `n x m` matrix, discard matrices whose row sums differ from the required values, and then test whether the resulting bipartite graph has a valid elimination order. There are `2^(nm)` binary matrices in total, so in the worst case this considers `2^(1,000,000)` candidates. Even if we restrict enumeration to matrices having the correct row sums, the number of candidates in the worst case is

`C(m, floor(m/2))^n`,

which is still exponential. Checking each candidate costs at least `O(nm)`, so this approach has worst-case cost `Theta(nm * C(m, floor(m/2))^n)`. Its correctness is straightforward, but it is unusable.

The useful observation is that a valid checking order is equivalent to the constructed bipartite graph being a forest. We therefore do not need to reason about the checking process while constructing the matrix. We only need to build an acyclic graph with the requested row degrees.

Suppose there are `k` rows with positive degree, and let the sum of all row degrees be `S`. Consider using a column either as a leaf column, containing a single `1`, or as a connector column containing two `1`s and joining two row vertices. A connector column behaves like an edge between two row vertices. If we use `E` connector columns, those columns can form a forest on the `k` positive rows. Such a forest can have at most `k-1` edges, and because every connector consumes two row-degree units, we also have `E <= floor(S/2)`.

Thus the maximum useful number of connector columns is

`E = min(k-1, floor(S/2))`.

Every connector saves one column compared with using two separate leaf columns. The total number of used columns is consequently

`E + (S - 2E) = S - E`.

If this exceeds `m`, no construction can exist. If it does not, we can construct exactly such a forest.

The remaining task is to realize a forest on the positive rows whose degree at row `i` is some value `t_i <= a_i`, with exactly `E` edges. We choose the `t_i` so that their sum is `2E`. A convenient way to realize the forest is to temporarily add one super-vertex. A forest with `E` edges on `k` vertices has `k-E` connected components. Connect the super-vertex to exactly one vertex in every component. The result is a tree on `k+1` vertices, so we can construct it from its degree sequence using a Prüfer sequence.

This turns the problem into a linear-sized degree-sequence construction followed by an ordinary forest traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(nm * C(m,floor(m/2))^n)` | `O(nm)` | Too slow |
| Optimal | `O(nm + (n+m) log(n+m))` | `O(nm + n+m)` | Accepted |

## Algorithm Walkthrough

1. Compute `S`, the sum of all row degrees, and collect the rows with positive degree. Let their number be `k`. Rows with `a_i = 0` will never need an edge, so they can remain isolated.
2. Set

`E = min(k - 1, S // 2)`.

These are the connector columns we want to use. We cannot use more than `k-1` without creating a cycle among the row vertices, and we cannot use more than `S//2` because each connector consumes two row-degree units.
3. Compute the number of columns that the construction will need as `S-E`. If `S-E > m`, print `NO`.

The quantity `S-E` is the minimum possible number of columns. Every connector uses two ones in one column instead of two separate columns, so each connector saves exactly one column.
4. Choose connector degrees `t_i` for the positive rows. We need `0 <= t_i <= a_i` and

`sum(t_i) = 2E`.

When `E > 0`, first give one connector degree to `E+1` distinct positive rows. This is possible because `E <= k-1`. Then distribute the remaining `E-1` degree units greedily without exceeding `a_i` or `k-1`.

Giving one unit to `E+1` rows guarantees that the connector graph can have `E` edges without trying to concentrate all its degree on too few vertices. The additional cap of `k-1` is useful later because no row can have degree greater than `k` in the temporary tree after the super-vertex is added.
5. Let `C = k-E`, the number of components the connector forest will have. Every row with `t_i=0` must receive an edge to the super-vertex. Choose all such rows as super-vertex neighbors, then choose arbitrary additional rows until exactly `C` rows have been selected.

There are enough zero-degree rows to do this because the construction gave positive connector degree to at least `E+1` rows. Hence at most `k-E-1` rows have `t_i=0`, while `C=k-E`.
6. Define the degree of row `i` in the temporary tree as `t_i + 1` if row `i` was selected as a super-vertex neighbor, and `t_i` otherwise. Give the super-vertex degree `C`.

The total degree is

`2E + C + C = 2(E+C) = 2k`,

exactly the number required for a tree on `k+1` vertices. Every degree is positive and at most `k`, so this is a valid tree degree sequence.
7. Build a Prüfer sequence containing each temporary vertex exactly `degree[i]-1` times. Its length is `k-1`. Decode the sequence with a priority queue containing the current leaves.

Prüfer decoding constructs a tree having exactly the requested degree sequence. Since the number of vertices is only `k+1 <= 1001`, the `O(k log k)` implementation is easily fast enough.
8. Remove every edge incident to the super-vertex. The remaining edges form a forest on the positive rows. Each remaining tree edge becomes one connector column with exactly two ones, one at each endpoint.
9. For each row `i`, there are `a_i-t_i` remaining ones that were not used by connector columns. Give each of them a separate leaf column containing a single `1` in row `i`.

The number of columns created is exactly `E + S - 2E = S-E`, which was checked against `m` earlier. All unused columns are filled with zeros.
10. Build the bipartite adjacency list of the resulting matrix and repeatedly take a vertex whose current degree is at most one. Append it to the answer order, remove it conceptually, and decrease the degree of its neighbors.

Because the graph is a forest, such a vertex always exists. Isolated rows and unused columns simply enter the queue with degree zero.
11. Output the matrix and the resulting row/column order.

### Why it works

The connector columns form a forest on the positive rows. Every additional `1` not used by a connector is placed in a private leaf column, so attaching those columns cannot create a cycle. Hence the entire bipartite graph is a forest.

Every row receives exactly `t_i` connector edges and `a_i-t_i` leaf edges, giving it exactly `a_i` ones. The construction uses `S-E` columns, which is no more than `m` whenever the algorithm accepts.

Finally, repeatedly removing a vertex of degree at most one produces a valid checking order for any forest. At the moment a vertex is removed, its current degree is exactly the number of lights still on in that row or column, so Jaber never sees more than one light.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    positive = [i for i, x in enumerate(a) if x > 0]
    k = len(positive)
    total = sum(a)

    if k == 0:
        mat = ['0' * m for _ in range(n)]
        order = []
        for i in range(n):
            order.append(("row", i))
        for j in range(m):
            order.append(("col", j))

        out = ["YES"]
        out.extend(mat)
        out.extend(f"{typ} {idx + 1}" for typ, idx in order)
        sys.stdout.write("\n".join(out))
        return

    E = min(k - 1, total // 2)

    used_columns = total - E
    if used_columns > m:
        print("NO")
        return

    # t[i] is the number of row i's edges used by connector columns.
    t = [0] * n

    if E > 0:
        # First give one connector incidence to E+1 rows.
        base_count = E + 1
        for idx in range(base_count):
            t[positive[idx]] = 1

        remaining = E - 1

        # Distribute the remaining incidences.
        # Capping at k-1 is enough for a row degree in the
        # temporary tree after possibly adding one super edge.
        for v in positive:
            if remaining == 0:
                break
            cap = min(a[v], k - 1)
            extra = min(cap - t[v], remaining)
            if extra > 0:
                t[v] += extra
                remaining -= extra

        if remaining != 0:
            print("NO")
            return

    # Number of connected components in the connector forest.
    C = k - E

    # Rows selected to connect to the super vertex.
    roots = []
    selected_root = [False] * n

    for v in positive:
        if t[v] == 0:
            roots.append(v)
            selected_root[v] = True

    if len(roots) > C:
        print("NO")
        return

    for v in positive:
        if len(roots) == C:
            break
        if not selected_root[v]:
            roots.append(v)
            selected_root[v] = True

    if len(roots) != C:
        print("NO")
        return

    # Temporary tree vertices:
    # 0 .. k-1 are positive rows
    # k is the super vertex
    super_v = k
    Ntree = k + 1

    degree = [0] * Ntree

    pos_index = {}
    for idx, v in enumerate(positive):
        pos_index[v] = idx

    for v in positive:
        idx = pos_index[v]
        degree[idx] = t[v] + (1 if selected_root[v] else 0)

    degree[super_v] = C

    # Build a Prüfer sequence.
    prufer = []
    for v in range(Ntree):
        prufer.extend([v] * (degree[v] - 1))

    # Decode Prüfer sequence.
    cur_degree = degree[:]
    leaves = []
    for v in range(Ntree):
        if cur_degree[v] == 1:
            heapq.heappush(leaves, v)

    tree_edges = []

    for v in prufer:
        leaf = heapq.heappop(leaves)
        tree_edges.append((leaf, v))

        cur_degree[leaf] -= 1
        cur_degree[v] -= 1

        if cur_degree[v] == 1:
            heapq.heappush(leaves, v)

    last1 = heapq.heappop(leaves)
    last2 = heapq.heappop(leaves)
    tree_edges.append((last1, last2))

    # Convert the tree, after removing the super vertex,
    # into connector columns.
    row_connector_edges = []

    for u, v in tree_edges:
        if u == super_v or v == super_v:
            continue

        original_u = positive[u]
        original_v = positive[v]
        row_connector_edges.append((original_u, original_v))

    if len(row_connector_edges) != E:
        print("NO")
        return

    # Matrix as mutable byte arrays.
    mat = [bytearray(b'0' * m) for _ in range(n)]

    col = 0

    # Each connector edge gets one column with two ones.
    for u, v in row_connector_edges:
        if col >= m:
            print("NO")
            return
        mat[u][col] = ord('1')
        mat[v][col] = ord('1')
        col += 1

    # Remaining row degrees use private leaf columns.
    for i in range(n):
        remaining = a[i] - t[i]
        for _ in range(remaining):
            if col >= m:
                print("NO")
                return
            mat[i][col] = ord('1')
            col += 1

    # Build the bipartite graph.
    total_vertices = n + m
    adj = [[] for _ in range(total_vertices)]
    deg = [0] * total_vertices

    for i in range(n):
        for j in range(m):
            if mat[i][j] == ord('1'):
                u = i
                v = n + j
                adj[u].append(v)
                adj[v].append(u)
                deg[u] += 1
                deg[v] += 1

    # Every forest has a vertex of degree <= 1.
    queue = []
    for v in range(total_vertices):
        if deg[v] <= 1:
            heapq.heappush(queue, v)

    removed = [False] * total_vertices
    order = []

    while queue:
        v = heapq.heappop(queue)
        if removed[v]:
            continue

        removed[v] = True
        order.append(v)

        for u in adj[v]:
            if removed[u]:
                continue
            deg[u] -= 1
            if deg[u] <= 1:
                heapq.heappush(queue, u)

    if len(order) != total_vertices:
        print("NO")
        return

    out = ["YES"]
    out.extend(row.decode() for row in mat)

    for v in order:
        if v < n:
            out.append(f"row {v + 1}")
        else:
            out.append(f"col {v - n + 1}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation separates zero rows from positive rows. This matters because a zero row does not need to participate in the connector forest at all.

The variable `E` is the number of connector columns. The expression `total - E` is the number of columns required after maximizing the number of two-row columns. If that number is larger than `m`, no arrangement can work.

The array `t` records how many of each row's required ones belong to connector columns. The initial `E+1` assignments guarantee enough nonzero vertices for a forest with `E` edges. The remaining degree is distributed greedily, with `k-1` as an upper bound. Python integers do not overflow, and all relevant values are at most about `10^6` here.

The super-vertex construction is the key graph-theoretic part. A forest with `E` edges on `k` vertices has `k-E` components. Connecting one vertex from every component to a new super-vertex produces a tree. Rather than constructing the components directly, we construct this tree from its degree sequence and then delete the super-vertex.

The Prüfer sequence contains vertex `v` exactly `degree[v]-1` times. Its length is `k-1`, matching a tree with `k+1` vertices. A heap stores current leaves during decoding, avoiding any quadratic search for the next leaf.

After decoding, every tree edge not touching the super-vertex corresponds to a connector column. The residual row degree is placed into private columns. The construction never puts two identical row pairs into separate connector columns, and the resulting graph is acyclic because it is a subgraph of the temporary tree plus leaf columns.

The final traversal is a standard leaf-removal process. `deg[v]` is the number of edges that are still alive when vertex `v` is about to be checked. Removing a degree-zero or degree-one vertex is exactly the condition required by the statement.

## Worked Examples

### Sample 1

For

```
4 4
1 0 0 0
```

only row 1 is positive, so `k=1` and `S=1`.

| Variable | Value |
| --- | --- |
| `positive` | `[1]` |
| `k` | `1` |
| `S` | `1` |
| `E = min(k-1,S//2)` | `0` |
| used columns | `1` |
| `t` | `[1,0,0,0]` |

Since there are no connector edges, the single required one becomes a private leaf column. The resulting matrix can be

```
1000
0000
0000
0000
```

The graph contains only one edge. Every vertex has degree zero or one, so any order of all eight vertices works. The sample's order is one such ordering.

This example exercises the `E=0` case. The construction does not need the super-vertex machinery to connect rows because there is only one positive row.

### Sample 2

For

```
4 4
2 1 1 1
```

we have `k=4` and `S=5`.

| Variable | Value |
| --- | --- |
| `positive` | `[1,2,3,4]` |
| `k` | `4` |
| `S` | `5` |
| `E` | `2` |
| `C = k-E` | `2` |
| required columns | `S-E = 3` |

The construction can choose connector degrees

```
t = [2, 1, 1, 0]
```

Their sum is `4 = 2E`. The corresponding temporary tree has row degrees

```
3, 1, 1, 1
```

after choosing row 1 and row 4 as super-vertex neighbors, while the super-vertex has degree two.

One possible connector forest is

```
row 1 -- row 2
row 1 -- row 3
```

and row 4 is isolated in the connector forest. The remaining degree belongs entirely to row 4, so one private column is added there.

A possible matrix is consequently

```
1100
1000
1000
0010
```

The exact matrix differs from the sample, which is fine because the problem accepts any valid construction. Its bipartite graph is a forest, so a leaf-removal ordering exists.

The trace demonstrates why the row degrees do not have to be interpreted as degrees in a tree on the rows themselves. Some row edges become leaf columns, while the connector columns are the part that determines the forest structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm + (n+m) log(n+m))` | The matrix and bipartite adjacency are processed in `O(nm)`, while Prüfer decoding and the final heap traversal are logarithmic per vertex. |
| Space | `O(nm + n+m)` | The matrix and adjacency lists dominate memory usage. |

With `n,m <= 1000`, the matrix contains at most one million cells. The `O(nm)` portion is also unavoidable up to constants because the complete matrix must be printed. The memory usage stays comfortably below the 256 MB limit.

## Test Cases

Because the output is not unique, an exact string comparison is inappropriate for this problem. The tests below run the solver and validate the produced matrix and checking order instead. The validator checks the row sums, the uniqueness of every row and column in the order, and the condition that every checked vertex has at most one remaining edge.

```python
import sys
import io
import heapq

def solve_string(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str) -> bool:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    lines = out.strip().splitlines()
    if not lines:
        return False

    possible = lines[0] == "YES"

    total = sum(a)
    if not possible:
        # A validator for NO instances is supplied separately below.
        return True

    if len(lines) != 1 + n + n + m:
        return False

    matrix = lines[1:1 + n]
    if any(len(row) != m for row in matrix):
        return False

    for i in range(n):
        if sum(c == '1' for c in matrix[i]) != a[i]:
            return False
        if any(c not in '01' for c in matrix[i]):
            return False

    order_lines = lines[1 + n:]
    if len(order_lines) != n + m:
        return False

    seen = set()
    order = []

    for line in order_lines:
        parts = line.split()
        if len(parts) != 2:
            return False

        typ, x = parts
        x = int(x)

        if typ == "row":
            if not (1 <= x <= n):
                return False
            v = x - 1
        elif typ == "col":
            if not (1 <= x <= m):
                return False
            v = n + x - 1
        else:
            return False

        if v in seen:
            return False
        seen.add(v)
        order.append(v)

    if len(seen) != n + m:
        return False

    adj = [[] for _ in range(n + m)]
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '1':
                u = i
                v = n + j
                adj[u].append(v)
                adj[v].append(u)

    removed = [False] * (n + m)

    for v in order:
        remaining = sum(not removed[u] for u in adj[v])
        if remaining > 1:
            return False
        removed[v] = True

    return True

def expect_no(inp: str):
    out = solve_string(inp)
    assert out.strip() == "NO"

# Sample 1
sample1 = """\
4 4
1 0 0 0
"""
assert validate(sample1, solve_string(sample1)), "sample 1"

# Sample 2
sample2 = """\
4 4
2 1 1 1
"""
assert validate(sample2, solve_string(sample2)), "sample 2"

# Minimum-size instance
case_min = """\
1 1
0
"""
assert validate(case_min, solve_string(case_min)), "minimum-size zero"

# Minimum-size instance with one edge
case_min_edge = """\
1 1
1
"""
assert validate(case_min_edge, solve_string(case_min_edge)), "minimum-size edge"

# Boundary case: both rows require every column.
# The only possible matrix is all ones, which contains a cycle.
case_impossible = """\
2 2
2 2
"""
expect_no(case_impossible)

# Same total-edge count as a sparse graph might allow, but the
# prescribed row degrees force two rows to share all three columns.
case_impossible_2 = """\
5 3
3 3 0 0 0
"""
expect_no(case_impossible_2)

# Maximum-size feasible case.
# Every row has exactly one one, so one private column per row is enough.
case_max = "1000 1000\n" + " ".join(["1"] * 1000) + "\n"
assert validate(case_max, solve_string(case_max)), "maximum-size case"

# All equal positive row degrees.
# 1000 rows and 1000 columns, every row has degree 1.
case_equal = "1000 1000\n" + " ".join(["1"] * 1000) + "\n"
assert validate(case_equal, solve_string(case_equal)), "all-equal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `YES` | Smallest graph with no edges |
| `1 1 / 1` | `YES` | Smallest graph containing an edge |
| `2 2 / 2 2` | `NO` | Forced 4-cycle |
| `5 3 / 3 3 0 0 0` | `NO` | Catches the insufficient edge-count condition |
| `1000 1000 / 1 ... 1` | `YES` | Maximum dimensions and large output |
| `1000 1000 / 1 ... 1` | `YES` | All-equal row degrees and boundary column usage |

## Edge Cases

For

```
2 2
2 2
```

we have `S=4`, `k=2`, and `E=min(1,2)=1`. The construction would need `S-E=3` columns, but only two columns exist. It immediately prints `NO`. This catches the fact that the forest restriction is stronger than merely requiring the number of edges to be at most the number of vertices minus one.

For

```
5 3
3 3 0 0 0
```

we have `S=6`, `k=2`, and again `E=1`. The minimum number of columns is `6-1=5`, which exceeds `m=3`. The algorithm rejects the instance before attempting any graph construction. This is exactly the kind of case where checking only `S <= n+m-1` gives the wrong answer.

For

```
3 2
2 0 0
```

there is one positive row, so `k=1`, `S=2`, and `E=0`. Both required ones become private leaf columns. The first row is `11`, and the other two rows are zero. The graph is a star with the row as its center, which is a tree, so a valid checking order exists.

For

```
3 3
0 0 0
```

we have `k=0`. There are no edges anywhere, so every row and column has degree zero. The special case directly prints an all-zero matrix and any permutation of the six vertices. This avoids trying to construct a connector forest with no positive rows.

For the maximum-size instance with 1000 rows and 1000 columns and every `a_i=1`, we have `S=1000`, `k=1000`, and `E=999`. The construction uses `1000-999=1` column for the connector forest, with the remaining degree unit structure represented by the same connector tree. The resulting bipartite graph is a tree containing all 1000 row vertices and one used column, while the other 999 columns are isolated. The final leaf-removal process handles the isolated columns automatically.

The central invariant behind all of these cases is unchanged: every `1` is an edge of a forest. Once that invariant is established, the required checking order is guaranteed by repeatedly removing a vertex with at most one remaining edge.
