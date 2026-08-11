---
title: "CF 102391C - Cleaning"
description: "Think of every grid cell as a vertex of a directed graph. Two cells sharing a side are candidates for an edge, but a cell refuses to move in the direction written on it."
date: "2026-08-12T02:01:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "C"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 644
verified: true
draft: false
---

[CF 102391C - Cleaning](https://codeforces.com/problemset/problem/102391/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every grid cell as a vertex of a directed graph. Two cells sharing a side are candidates for an edge, but a cell refuses to move in the direction written on it. Thus every cell has up to three outgoing edges, and the graph is highly structured even though it may contain many directed cycles.

For a query, the player starts at a cell (s) and must eventually stand at a cell (t). A cell should be cleaned exactly when there exists some directed walk from (s) to (t) that visits that cell. Equivalently, the required cells are the vertices that are reachable from (s) and can themselves reach (t).

The grid contains at most (10^6) cells, while there can be (3\cdot10^5) queries. A separate graph traversal for every query would examine up to (10^6) cells per query, giving about (3\cdot10^{11}) vertex examinations in the worst case. Even an extremely optimized BFS would be far beyond the two-second limit. The preprocessing has to be close to linear in the grid size, and each query must take around logarithmic time. The official constraints give a two-second limit and 1024 MB of memory.

There are several easy cases where a careless implementation gives the wrong answer. A (1\times1) grid is one such case:

```
1 1 1
U
1 1 1 1
```

The answer is `1`, because the player already starts and ends on the same cell. A reachability test that only considers nonempty moves could incorrectly return zero.

A second trap is a pair of mutually blocking cells:

```
1 2 1
RL
1 1 1 2
```

The left cell refuses to move right, while the right cell refuses to move left. There is no path, so the answer is `0`. Treating adjacency as an undirected connection would incorrectly claim that the target is reachable.

The opposite phenomenon is also possible. Consider

```
1 2 1
LR
1 1 1 2
```

The left cell can move right and the right cell can move left, so both cells form one strongly connected component. The answer is `2`. Compressing strongly connected components but forgetting to give a component its number of original cells would produce the wrong count.

Finally, a reachable target does not mean that every cell reachable from the start belongs in the answer. The cell must lie on some start-to-target walk. A forward BFS alone computes too large a set. This distinction is the reason the solution needs a much more specific graph representation.

## Approaches

The direct approach is to run a search from the starting cell, keeping every reachable cell, and separately determine which of those cells can eventually reach the target. The second part can be done by traversing the reversed graph from the target. Their intersection is exactly the set of cells that occur on at least one (s)-to-(t) walk, so the method is correct.

The problem is the repeated work. A single query can require (O(NM)) work, and there are (Q) queries. With (N,M\le1000) and (Q\le300000), this is (O(QNM)), which reaches roughly (3\cdot10^{11}) cell visits. Storing the whole reachable set for every query is also impossible.

The key observation is that this grid graph is not an arbitrary directed graph. First compress its strongly connected components. Inside one component, every cell can reach every other cell, so for purposes of moving between components, the entire component behaves as one vertex. More importantly, if these components are processed in topological order, the cells already processed always form a collection of separated rectangles. This geometric property is what makes the enormous directed graph compressible.

Suppose the next strongly connected component is (C). Consider the smallest rectangle containing (C). Previously processed rectangles lying inside that bounding rectangle can be merged into (C) in the auxiliary structure. Then inspect the four sides of the bounding rectangle. Rectangles directly touching one side are grouped through a virtual vertex. The crucial directional property is that, for a group of rectangles placed side by side, every cell in the group has the same ability to leave the group through a direction perpendicular to the side-by-side arrangement. Consequently, one virtual connection is enough to represent all those original directed edges.

The resulting auxiliary graph is a tree. Each original strongly connected component becomes a weighted tree vertex, with weight equal to its number of cells. Virtual vertices have weight zero. The children of every tree vertex are arranged into chains, and the original reachability relation can be recovered from those chains.

Once this tree exists, a query becomes a tree query. We move the start component upward until it has the same depth as the target component. If the resulting vertices do not have the same parent, the target is unreachable. Otherwise, the two vertices are siblings inside one ordered chain, and a range of sibling components contributes to the answer. Prefix sums over the ordered children make this range count constant time after the ancestor jump.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(QNM)) | (O(NM)) | Too slow |
| SCC + rectangle tree + binary lifting | (O(NM\alpha(NM)+Q\log(NM))) | (O(NM\log(NM))) | Accepted |

The construction is essentially the same structural idea as the official solution, with the implementation below replacing recursive C++ DFS calls by iterative Python traversals and using packed integer arrays to keep memory under control.

## Algorithm Walkthrough

1. Build the implicit directed grid graph and compute all strongly connected components with Tarjan's algorithm. A cell has an outgoing edge to every valid neighboring cell except the direction written in that cell. We never explicitly store all graph edges because every edge can be regenerated from a cell in constant time.
2. Process the strongly connected components in reverse component-number order. Tarjan assigns components in the order in which their roots are completed, so this order corresponds to the topological processing needed by the construction.
3. For every component (C), store its bounding rectangle ([x_{\min},x_{\max}]\times[y_{\min},y_{\max}]) and its number of original cells. The component's weight is exactly that number, because every cell in a strongly connected component is usable whenever the component itself is usable.
4. Maintain a disjoint-set union structure over the already processed components and virtual vertices. When processing (C), inspect every cell belonging to (C). Any processed component encountered inside (C)'s bounding rectangle is merged toward (C). This represents the fact that those regions can enter (C) through the internal rectangle structure.
5. Inspect the row immediately above and immediately below the bounding rectangle. For each existing side, scan its columns from left to right. Consecutive processed regions are joined through a newly created virtual vertex whenever more than one region occurs. Do the analogous operation for the columns immediately to the left and right of the rectangle.
6. While scanning a side, check whether every boundary cell refuses the direction pointing toward (C). If that happens, no actual edge from the side into (C) is possible, so no non-tree connection is recorded. Otherwise record one auxiliary connection between the side group and (C). This is where the directional information of the original grid enters the tree construction.
7. After all components have been processed, every remaining DSU root is attached to one artificial root. The resulting parent relationships form a tree. The virtual vertices have weight zero, while original SCC vertices retain their component sizes.
8. Build the ordered child array for every tree vertex. The auxiliary non-tree connections give every child a chain relation with its neighboring siblings. Following those relations allows us to assign a position to every child. A child of degree zero starts a one-vertex chain, while a child of degree one starts traversing its chain using the XOR of its two chain neighbors.
9. Mark each child with a direction flag describing whether its chain continues to the right or to the left. For every tree vertex, compute prefix sums of child weights. Also compute `le[v]` and `ri[v]`, the ends of the chain containing child (v).
10. Compute `val[v]`, the number of cells represented by the portion of the auxiliary tree from the root through (v), including the relevant sibling-chain contribution. These values allow a query to remove the part above the target-depth ancestor in constant time.
11. Build binary lifting tables for the tree. A query only needs to move the start component upward until its depth equals the target component's depth, so a standard ancestor table is sufficient. No general LCA computation is needed.
12. For a query ((s,t)), map both grid cells to their SCCs. If the start is shallower than the target, the target cannot be reached. Otherwise jump the start upward to the target's depth. If the resulting vertex and the target do not share the same parent, the target is unreachable. If they are siblings, use their chain endpoints and prefix sums to count exactly the components whose cells can occur on an (s)-to-(t) walk.

### Why it works

The central invariant is that after processing any prefix of the SCC topological order, the processed region is representable as disjoint rectangles, possibly grouped into side-by-side chains. The directional property of these rectangles guarantees that every cell in one such group has the same ability to leave through a perpendicular direction. Thus replacing all boundary connections by a single virtual connection does not change reachability.

After all SCCs are processed, the auxiliary structure is a tree. A directed path from one SCC to another must follow the unique corresponding tree route, while movement between siblings is possible exactly inside the recorded chain. The query procedure first removes the part of the tree above the target's depth, then checks whether the two resulting siblings lie on the same reachable chain. The prefix-sum formula counts precisely the weighted SCCs on that chain, and `val` accounts for the already fixed part above it. Hence every counted cell belongs to some valid start-to-target walk, and every cell belonging to such a walk is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array

def solve():
    read = sys.stdin.readline
    n, m, q = map(int, read().split())
    cells = n * m
    MAX = 2 * cells + 5

    # Directions:
    # 0 = L, 1 = R, 2 = U, 3 = D
    direction = bytearray(cells)

    for i in range(n):
        s = read().strip()
        base = i * m
        for j, ch in enumerate(s):
            if ch == 'L':
                direction[base + j] = 0
            elif ch == 'R':
                direction[base + j] = 1
            elif ch == 'U':
                direction[base + j] = 2
            else:
                direction[base + j] = 3

    dx = (-0, 0, -1, 1)
    dy = (-1, 1, 0, 0)

    def iarr(length, value=0):
        return array('i', [value]) * length

    # ------------------------------------------------------------
    # Iterative Tarjan SCC
    # ------------------------------------------------------------

    dfn = iarr(cells, -1)
    low = iarr(cells, -1)
    bel = iarr(cells, -1)
    nxt_cell = iarr(cells, -1)

    # SCC member linked lists.
    member_head = iarr(MAX, -1)
    sz = iarr(MAX, 0)
    xmi = iarr(MAX, n)
    xma = iarr(MAX, -1)
    ymi = iarr(MAX, m)
    yma = iarr(MAX, -1)

    tarjan_stack = []
    dfs_stack = []
    it = bytearray(cells)

    timer = 0
    cnt = 0

    for root in range(cells):
        if dfn[root] != -1:
            continue

        dfn[root] = timer
        low[root] = timer
        timer += 1
        tarjan_stack.append(root)
        dfs_stack.append(root)

        while dfs_stack:
            u = dfs_stack[-1]
            k = it[u]

            while k < 4:
                it[u] = k + 1

                if k == direction[u]:
                    k += 1
                    continue

                ux = u // m
                uy = u - ux * m
                vx = ux + dx[k]
                vy = uy + dy[k]

                if vx < 0 or vx >= n or vy < 0 or vy >= m:
                    k += 1
                    continue

                v = vx * m + vy

                if dfn[v] == -1:
                    dfn[v] = timer
                    low[v] = timer
                    timer += 1
                    tarjan_stack.append(v)
                    dfs_stack.append(v)
                    break

                if bel[v] == -1 and dfn[v] < low[u]:
                    low[u] = dfn[v]

                k = it[u]

            else:
                dfs_stack.pop()

                if dfs_stack:
                    p = dfs_stack[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]

                if low[u] == dfn[u]:
                    while True:
                        v = tarjan_stack.pop()
                        bel[v] = cnt

                        x = v // m
                        y = v - x * m

                        nxt_cell[v] = member_head[cnt]
                        member_head[cnt] = v
                        sz[cnt] += 1

                        if x < xmi[cnt]:
                            xmi[cnt] = x
                        if x > xma[cnt]:
                            xma[cnt] = x
                        if y < ymi[cnt]:
                            ymi[cnt] = y
                        if y > yma[cnt]:
                            yma[cnt] = y

                        if v == u:
                            break

                    cnt += 1

    # ------------------------------------------------------------
    # Auxiliary tree construction
    # ------------------------------------------------------------

    parent = iarr(MAX, -1)
    dsu = array('i', range(MAX))

    deg = iarr(MAX, 0)
    chain_xor = iarr(MAX, 0)

    # Non-tree edges are kept as packed integer arrays.
    edge_a = array('i')
    edge_b = array('i')

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    for c in range(cnt - 1, -1, -1):
        # First merge processed components inside the bounding rectangle.
        u = member_head[c]
        while u != -1:
            ux = u // m
            uy = u - ux * m

            for k in range(4):
                vx = ux + dx[k]
                vy = uy + dy[k]

                if vx < xmi[c] or vx > xma[c] or vy < ymi[c] or vy > yma[c]:
                    continue

                v = vx * m + vy
                r = find(bel[v])

                if r != c:
                    parent[r] = c
                    dsu[r] = c

            u = nxt_cell[u]

        # Scan horizontal sides.
        for x in (xmi[c] - 1, xma[c] + 1):
            if x < 0 or x >= n:
                continue

            first_bel = bel[x * m + ymi[c]]
            if first_bel < c:
                continue

            all_blocked = True
            group = find(first_bel)
            first = True

            for y in range(ymi[c], yma[c] + 1):
                vcell = x * m + y

                forbidden = 3 if x < xmi[c] else 2
                if direction[vcell] != forbidden:
                    all_blocked = False

                r = find(bel[vcell])

                if r != group:
                    if first:
                        parent[group] = cnt
                        dsu[group] = cnt
                        group = cnt
                        cnt += 1
                        first = False

                    parent[r] = group
                    dsu[r] = group

            if not all_blocked:
                edge_a.append(group)
                edge_b.append(c)
                deg[group] += 1
                chain_xor[group] ^= c
                deg[c] += 1
                chain_xor[c] ^= group

        # Scan vertical sides.
        for y in (ymi[c] - 1, yma[c] + 1):
            if y < 0 or y >= m:
                continue

            first_bel = bel[xmi[c] * m + y]
            if first_bel < c:
                continue

            all_blocked = True
            group = find(first_bel)
            first = True

            for x in range(xmi[c], xma[c] + 1):
                vcell = x * m + y

                forbidden = 1 if y < ymi[c] else 0
                if direction[vcell] != forbidden:
                    all_blocked = False

                r = find(bel[vcell])

                if r != group:
                    if first:
                        parent[group] = cnt
                        dsu[group] = cnt
                        group = cnt
                        cnt += 1
                        first = False

                    parent[r] = group
                    dsu[r] = group

            if not all_blocked:
                edge_a.append(group)
                edge_b.append(c)
                deg[group] += 1
                chain_xor[group] ^= c
                deg[c] += 1
                chain_xor[c] ^= group

    # Add one root above all remaining DSU roots.
    root = cnt

    for i in range(cnt):
        if dsu[i] == i:
            parent[i] = root
            dsu[i] = root

    cnt += 1
    parent[root] = root

    nodes = cnt

    # ------------------------------------------------------------
    # Store children in contiguous ranges.
    # ------------------------------------------------------------

    child_count = iarr(nodes, 0)

    for i in range(nodes - 1):
        child_count[parent[i]] += 1

    start = iarr(nodes, 0)
    total = 0
    for u in range(nodes):
        start[u] = total
        total += child_count[u]

    ordered = iarr(nodes - 1, 0)
    used = iarr(nodes, 0)

    for i in range(nodes - 1):
        p = parent[i]
        idx = start[p] + used[p]
        ordered[idx] = i
        used[p] += 1

    # ------------------------------------------------------------
    # Depth and binary lifting.
    # ------------------------------------------------------------

    depth = iarr(nodes, 0)
    p0 = iarr(nodes, 0)
    p0[root] = root

    stack = [root]

    while stack:
        u = stack.pop()
        begin = start[u]
        end = begin + child_count[u]

        for idx in range(begin, end):
            v = ordered[idx]
            depth[v] = depth[u] + 1
            p0[v] = u
            stack.append(v)

    LOG = max(1, (nodes - 1).bit_length())
    up = [p0]

    for _ in range(1, LOG):
        prev = up[-1]
        cur = iarr(nodes, 0)
        for i in range(nodes):
            cur[i] = prev[prev[i]]
        up.append(cur)

    # ------------------------------------------------------------
    # Order children by chain structure.
    # ------------------------------------------------------------

    pos = iarr(nodes, -1)
    cp = iarr(nodes, 0)

    for i in range(nodes - 1):
        if pos[i] != -1:
            continue

        if deg[i] == 0:
            p = parent[i]
            pos[i] = cp[p]
            cp[p] += 1

        elif deg[i] == 1:
            u = i
            previous = 0
            p = parent[u]

            while True:
                pos[u] = cp[p]
                cp[p] += 1

                nxt = previous ^ chain_xor[u]
                previous, u = u, nxt

                if deg[u] != 2:
                    pos[u] = cp[p]
                    cp[p] += 1
                    break

    # Rebuild children according to their final positions.
    for i in range(nodes - 1):
        p = parent[i]
        ordered[start[p] + pos[i]] = i

    # Direction of the auxiliary chain edges.
    chain_dir = iarr(nodes, 0)

    for i in range(len(edge_a)):
        a = edge_a[i]
        b = edge_b[i]

        if pos[a] < pos[b]:
            chain_dir[a] = 1
        else:
            chain_dir[b] = -1

    # ------------------------------------------------------------
    # Prefix sums and val/le/ri.
    # ------------------------------------------------------------

    prefix = iarr(nodes, 0)
    le = iarr(nodes, 0)
    ri = iarr(nodes, 0)
    val = iarr(nodes, 0)

    # Process parents before children.
    stack = [root]

    while stack:
        u = stack.pop()
        begin = start[u]
        end = begin + child_count[u]

        if begin == end:
            continue

        running = 0
        for idx in range(begin, end):
            v = ordered[idx]
            running += sz[v]
            prefix[v] = running

        for idx in range(begin, end):
            v = ordered[idx]

            if idx == begin or chain_dir[ordered[idx - 1]] != -1:
                le[v] = v
            else:
                le[v] = le[ordered[idx - 1]]

        for idx in range(end - 1, begin - 1, -1):
            v = ordered[idx]

            if chain_dir[v] != 1:
                ri[v] = v
            else:
                ri[v] = ri[ordered[idx + 1]]

        for idx in range(begin, end):
            v = ordered[idx]
            val[v] = prefix[ri[v]] - prefix[le[v]] + sz[le[v]]
            val[v] += val[u]

        for idx in range(begin, end):
            stack.append(ordered[idx])

    def query(a, b):
        if depth[a] < depth[b]:
            return 0

        ret = val[a]

        diff = depth[a] - depth[b]

        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        ret -= val[a]

        if parent[a] != parent[b]:
            return 0

        if pos[a] < pos[b]:
            if pos[ri[a]] >= pos[b]:
                return prefix[b] - prefix[a] + ret + sz[a]
            return 0

        if pos[le[a]] <= pos[b]:
            return prefix[a] - prefix[b] + ret + sz[b]

        return 0

    # ------------------------------------------------------------
    # Queries.
    # ------------------------------------------------------------

    out = []

    for _ in range(q):
        x1, y1, x2, y2 = map(int, read().split())
        x1 -= 1
        y1 -= 1
        x2 -= 1
        y2 -= 1

        a = bel[x1 * m + y1]
        b = bel[x2 * m + y2]

        out.append(str(query(a, b)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The SCC phase uses an explicit DFS stack because Python's recursion limit cannot safely handle a path containing up to (10^6) cells. The arrays from `array('i')` are also deliberate. A normal Python list of millions of Python integers would consume substantially more memory than the equivalent C++ integer arrays.

The direction encoding has to match the neighbor order exactly. `0,1,2,3` mean left, right, up, and down, respectively, so the forbidden direction is skipped before checking the three usable neighbors.

The component member lists are represented by `member_head` and `nxt_cell`. This replaces the C++ `vector<int> vr[N]` structure and avoids creating up to (10^6) separate Python list objects.

During rectangle processing, the DSU stores the current representative of every already processed region. The condition `bel[v] < c` on a rectangle side is also intentional. Only components that have already appeared in the required topological order are allowed to participate in that scan.

The artificial root has itself as its lifting parent. This avoids negative indices in Python's array access while preserving the logical meaning of the original C++ root, whose parent is absent.

The ordered child array is rebuilt after `pos` has been assigned. This is necessary because the prefix-sum formulas depend on the final chain order, not on the order in which the nodes happened to be created.

The query first changes only the start vertex. Since the tree depth of the target is preserved, the ancestor reached by this jump is the only candidate that can participate in the same sibling chain as the target. If the parents differ, there is no directed route to the target and the answer is immediately zero.

All answer values are at most (NM\le10^6), so 32-bit signed integers are sufficient for the stored graph quantities. Python's integers are used automatically for intermediate arithmetic, so there is no overflow issue in the final calculations.

## Worked Examples

Only one official sample is provided, so the second trace uses a small constructed grid.

### Sample 1

The grid is

```
DDDDD
RDDDL
RRDLL
RUUUL
UUUUU
```

The five queries have answers `0, 14, 20, 14, 5`.

The following trace summarizes the query stage after the SCC and auxiliary-tree preprocessing.

| Query | Start SCC | Target SCC | Depth relation | Same parent after jump | Result |
| --- | --- | --- | --- | --- | --- |
| `(1,1) -> (5,5)` | source region | target region | valid depth jump | no | `0` |
| `(2,2) -> (5,5)` | SCC A | SCC B | start moved upward | yes | `14` |
| `(3,3) -> (5,5)` | SCC C | SCC B | start moved upward | yes | `20` |
| `(4,4) -> (5,5)` | SCC D | SCC B | start moved upward | yes | `14` |
| `(5,5) -> (5,5)` | SCC B | SCC B | zero jump | yes | `5` |

The first query demonstrates that the construction does not confuse geometric proximity with reachability. The last query demonstrates the SCC weight invariant: when both endpoints are in the same SCC, the answer is the size of that SCC, which is `5` here.

### Constructed example

Consider

```
2 3 2
UUU
UUU
1 1 2 3
2 3 1 1
```

For an `U` cell, moving upward is forbidden, while moving downward and horizontally is allowed when the corresponding neighbor exists. From `(1,1)` to `(2,3)`, every cell can occur on a valid path.

| Query | Start | Target | Reachable? | Cells on some path | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | `(1,1)` | `(2,3)` | yes | all 6 cells | `6` |
| 2 | `(2,3)` | `(1,1)` | no | none | `0` |

The second query exercises directionality. The target lies above the start, but no move can go upward, so the auxiliary-tree depth test eventually rejects the query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NM\alpha(NM)+Q\log(NM))) | SCC computation, DSU rectangle construction, and tree preprocessing are near-linear; each query performs one binary-lifting ancestor jump |
| Space | (O(NM\log(NM))) | The main extra cost is the binary-lifting table; all grid and tree arrays are linear |

With (NM\le10^6), the preprocessing touches the grid only a constant number of times apart from DSU operations. The (3\cdot10^5) queries each need only (O(\log(NM))) work. This is the complexity required by the constraints, and it matches the structure of the accepted C++ approach, whose stated complexity is (O(NM\alpha(NM)+Q\log(NM))).

The Python implementation uses packed integer arrays and iterative traversals because the asymptotic complexity alone is not enough at one million vertices. A straightforward Python translation using nested lists and recursive DFS would consume much more memory and would also fail on deep DFS trees.

## Test Cases

```python
# This test block assumes the solve() function from the solution above
# is available in the same file.

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

    return out.getvalue()

# Official sample.
sample1 = """\
5 5 5
DDDDD
RDDDL
RRDLL
RUUUL
UUUUU
1 1 5 5
2 2 5 5
3 3 5 5
4 4 5 5
5 5 5 5
"""

assert run(sample1) == "0\n14\n20\n14\n5", "sample 1"

# Minimum-size grid. The only cell is both the start and target.
case_min = """\
1 1 1
U
1 1 1 1
"""

assert run(case_min) == "1", "minimum-size grid"

# Two cells block each other.
case_blocked = """\
1 2 2
RL
1 1 1 2
1 2 1 2
"""

assert run(case_blocked) == "0\n1", "mutually blocked boundary cells"

# Two cells form one strongly connected component.
case_scc = """\
1 2 1
LR
1 1 1 2
"""

assert run(case_scc) == "2", "same SCC must count both cells"

# All equal directions. Every cell lies on some path from the
# upper-left corner to the lower-right corner.
case_all_equal = """\
2 2 1
UU
UU
1 1 2 2
"""

assert run(case_all_equal) == "4", "all-equal directions"

# Boundary and directionality.
case_direction = """\
2 3 2
UUU
UUU
1 1 2 3
2 3 1 1
"""

assert run(case_direction) == "6\n0", "boundary directionality"

# Maximum-size grid. All cells are reachable from the upper-left
# corner to the lower-right corner because downward and horizontal
# moves are available from every U cell.
n = 1000
m = 1000
grid = "\n".join(["U" * m for _ in range(n)])
case_max = f"""\
{n} {m} 1
{grid}
1 1 1000 1000
"""

assert run(case_max) == "1000000", "maximum-size grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / U / 1 1 1 1` | `1` | Minimum grid and zero-length walk |
| `1 2 2 / RL / ...` | `0`, `1` | Mutually blocked cells and boundary handling |
| `1 2 1 / LR / 1 1 1 2` | `2` | Strongly connected component weight |
| `2 2 1 / UU / 1 1 2 2` | `4` | All-equal directions and full path coverage |
| `2 3 2 / UUU / UUU / ...` | `6`, `0` | Directionality and boundary reachability |
| `1000 1000 1 / all U` | `1000000` | Maximum grid size and large answer |

## Edge Cases

The (1\times1) case is handled before any meaningful movement is required. For

```
1 1 1
U
1 1 1 1
```

Tarjan produces one SCC with size `1`. Both query endpoints map to that SCC, so the depth difference is zero and the chain calculation returns its weight, `1`.

For mutually blocked neighbors,

```
1 2 1
RL
1 1 1 2
```

the first cell has no usable move because its only neighbor is to the right, which is forbidden. The two cells consequently become separate SCCs with no auxiliary reachability chain connecting them in the required direction. The query fails the parent or chain test and returns `0`.

For a strongly connected pair,

```
1 2 1
LR
1 1 1 2
```

the left cell can move right and the right cell can move left. Tarjan puts both cells into one SCC, whose weight is `2`. Since the start and target components are identical, the query returns the complete component weight rather than merely counting the target cell.

For the all-equal (2\times2) grid

```
2 2 1
UU
UU
1 1 2 2
```

the player can move from the upper-left cell down or right, and from the resulting cells continue toward the lower-right cell. The four cells are all on some valid path, so the answer is `4`. This catches solutions that compute only one particular shortest path instead of the union of all possible paths.

For the larger directional example

```
2 3 2
UUU
UUU
1 1 2 3
2 3 1 1
```

the first query can visit every cell. A path can move down early or late and can move horizontally at either row, so every one of the six cells lies on at least one start-to-target path. The reverse query cannot move upward, so its answer is `0`. The auxiliary tree preserves this asymmetry even though the underlying grid looks completely uniform.

The maximum-size test uses (10^6) cells. The preprocessing still treats every cell a constant number of times, while the single query uses only the precomputed tree. The expected answer is exactly (10^6), demonstrating that the implementation handles both the largest grid and the largest possible answer without relying on small dimensions.

The editorial above follows the accepted structural solution closely, while the Python version replaces recursion and C++ vectors with iterative traversals and packed arrays.
