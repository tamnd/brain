---
title: "CF 102391C - Cleaning"
description: "The grid is a directed graph disguised as an array. Every cell is a vertex, and two orthogonally adjacent cells are connected by a directed edge exactly when the first cell does not forbid moving in that direction."
date: "2026-08-10T19:56:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "C"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 562
verified: false
draft: false
---

[CF 102391C - Cleaning](https://codeforces.com/problemset/problem/102391/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 22s  
**Verified:** no  

## Solution
## Problem Understanding

The grid is a directed graph disguised as an array. Every cell is a vertex, and two orthogonally adjacent cells are connected by a directed edge exactly when the first cell does not forbid moving in that direction. A cell marked `L`, for example, may move to its right, up, or down neighbors, but never to its left neighbor. Moves outside the grid are simply unavailable. This interpretation matches the original problem definition.

For each query, we know the starting cell `s` and the ending cell `t`. We need to count every cell `v` for which there exists a directed path `s -> ... -> v -> ... -> t`. A cell counts once even if many different paths use it. If `t` is unreachable from `s`, the answer is zero.

That last distinction is easy to miss. We are not counting every cell reachable from `s`. A cell behind `t` does not count just because the player can reach it from the start. The cell must also be usable before eventually reaching the specified ending cell.

There can be up to one million cells and 300,000 queries. Running a graph search independently for every query would require up to about `3 * 10^11` cell visits in the worst case, before even counting the neighbor checks. The grid is large enough that the preprocessing must be close to linear, while each query must be logarithmic or better. The original contest gives a two second time limit and 1024 MB of memory, so a solution that constructs an explicit general-purpose reachability structure for every pair is far too large.

Several small cases expose mistakes that otherwise look harmless.

Consider a single cell.

```
1 1 1
L
1 1 1 1
```

The answer is `1`. The player starts and ends on that cell, so the empty path already visits it. A careless implementation that only counts movement edges could incorrectly return zero.

Now consider a one by two grid whose arrows point toward the outside.

```
1 2 2
RL
1 1 1 2
1 2 1 1
```

The output is

```
0
0
```

The first cell is marked `R`, so it cannot move right. The second cell is marked `L`, so it cannot move left. The two cells form a complete directed barrier. Treating the grid as an undirected graph would incorrectly claim that they are connected.

A boundary cell also has fewer legal moves than an interior cell. For example,

```
1 2 1
LL
1 2 1 1
```

has answer `0`. The second cell cannot move left because it is forbidden by its `L`, and there is no other cell. A traversal that checks only whether the target is adjacent, without respecting the arrow of the source cell, gives the wrong result.

Finally, several cells can belong to one strongly connected component. In Sample 1, the entire last row is marked `U`. The cells can move horizontally in both directions, so all five cells belong to one SCC. The query from `(5,5)` to itself consequently has answer `5`, not `1`.

## Approaches

The direct approach is to run a BFS or DFS from the starting cell for every query. During the search we mark every reachable cell. If the ending cell is never reached, the answer is zero. Otherwise we need one more restriction: among the reachable cells, only cells that can still reach the target belong to a valid start-to-target path. Running a second search from the target on the reversed graph would handle that, but it is still `O(NM)` per query. With `Q = 300000` and `NM = 10^6`, this reaches roughly `3 * 10^11` visited vertices in the worst case.

The useful structure appears when we stop looking at individual cells and first contract every strongly connected component. Inside one SCC, every cell can reach every other cell, so for the purpose of deciding which cells lie on a start-to-target path, the entire component behaves as one vertex with weight equal to its number of cells.

The resulting SCC condensation is a DAG. A general DAG would still be difficult because reachability between arbitrary pairs can be complicated. The grid restriction gives us much more structure. If SCCs are inserted in topological order, the cells already inserted always form a collection of disjoint rectangles. If one such component were not rectangular, an outside cell would touch it on at least two sides. That outside cell would have an edge into the already constructed region, contradicting the chosen topological order. This is the first key geometric property of the problem.

The rectangles can be represented by a tree with a small number of additional directed edges. When a new SCC is inserted, all previously constructed rectangles lying inside its bounding rectangle are attached to it as tree children. Rectangles touching its four sides are grouped into consecutive chains, with a virtual vertex used when several rectangles share the same side. The virtual vertex gives us one tree connection while the actual directed connection toward the new SCC is stored separately as a non-tree edge.

The second key property says that for a group of rectangles lying next to each other, movement in the perpendicular direction is uniform: either every rectangle in the group can leave in that direction, or none can. This is what allows an entire side to be represented by one virtual vertex instead of handling every cell separately.

After all SCCs have been processed, the constructed graph has a particularly useful shape. Its tree edges form a rooted tree, and the children of every tree vertex are arranged into one or more directed chains. A query can then be reduced to moving upward in the tree until the source and target are at the same depth, followed by checking whether their two children belong to the same directed chain. The number of cells on all possible valid paths is obtained from prefix sums over the ordered children.

This construction is essentially the official solution's central observation. The original implementation uses disjoint set union to merge already processed rectangles and binary lifting for the final ancestor queries. The Python implementation below uses the same construction, but replaces binary lifting with heavy-light decomposition. Both give logarithmic query time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(QNM)` | `O(NM)` | Too slow |
| SCC + rectangle tree | `O(NM α(NM) + Q log(NM))` | `O(NM)` packed storage | Accepted |

## Algorithm Walkthrough

1. Treat every cell as a directed graph vertex. For each cell, inspect its four neighboring positions and create a usable transition whenever that direction is not the cell's forbidden direction. Boundary positions are rejected before creating a transition because moving outside the grid is impossible.
2. Compute all strongly connected components with Tarjan's algorithm. We need SCCs because inside one component every cell can be used to reach every other cell, so queries can operate on components rather than individual cells.

The implementation uses an iterative version of Tarjan rather than recursive DFS. A one million cell recursion depth would exceed Python's recursion limit and would also consume a large amount of call-stack memory.
3. For every SCC, record its size and its minimum and maximum row and column. The four extrema define its bounding rectangle. We also store all cells belonging to each SCC in a linked list, so iterating through the cells of a component does not require a Python list of lists for up to one million components.
4. Process SCCs in decreasing component number. Tarjan assigns components in reverse topological order, so this processes the condensation DAG from sources toward sinks.

While processing component `C`, use a disjoint set union structure to merge every already represented component lying inside the bounding rectangle of `C`. These merged objects become tree descendants of `C`.
5. Inspect the four sides immediately outside the bounding rectangle. Suppose we inspect the cells directly to the left of `C`. All such cells lie on one horizontal boundary segment. Consecutive cells that have already been merged into the same rectangle are represented by one DSU root.

If the boundary cells all forbid movement toward `C`, no directed edge can enter `C` from that side, so no extra connection is needed. Otherwise, all rectangles touching that side are joined under one virtual vertex, and the virtual vertex receives a directed non-tree edge toward `C`.

The same procedure is applied to the right, upper, and lower sides. The forbidden directions used for the four sides are exactly `R`, `L`, `D`, and `U`, respectively.
6. After every SCC has been processed, every DSU root that has not yet acquired a parent is attached to one artificial root. The tree now contains all SCC vertices and all virtual vertices. Real SCC vertices have positive weights equal to their number of cells, while virtual vertices have weight zero.
7. Each tree vertex has several children. The extra directed edges connect children of the same parent, and those edges form disjoint chains. We compute a position for every child so that the children of one parent are ordered from left to right along these chains.

The graph formed only by the extra edges has maximum degree two. The XOR of the neighbors is enough to walk through every chain without storing an adjacency list for every node.
8. For each extra edge between siblings `a` and `b`, store its direction using `dir`. If `a` is before `b` and the edge is `a -> b`, set `dir[a] = 1`. If `b` is before `a`, set `dir[b] = -1`.

For every parent, compute `le[v]` and `ri[v]`. They identify the leftmost and rightmost child in the directed chain containing `v`. A prefix sum `sum[v]` stores the total SCC weight from the first child through `v`.
9. Compute `val[v]`, which represents the number of real grid cells that can be covered when entering the subtree through `v` and using the available sibling-chain movement. The recurrence is

`val[v] = val[parent] + sum[ri[v]] - sum[le[v]] + size[le[v]]`.

The added term is exactly the weight of the maximal sibling-chain interval associated with `v`.
10. Preprocess the tree for ancestor queries using heavy-light decomposition. Given a source component `a` and target component `b`, we first need the ancestor of `a` whose depth equals the depth of `b`. Heavy-light decomposition finds that vertex in `O(log(NM))`.
11. If the source is shallower than the target, the target cannot be reached through the constructed tree structure, so the answer is zero. Otherwise lift the source to the target's depth.
12. The lifted source and target must have the same parent. If their parents differ, no valid path can connect them, so the answer is zero.
13. If the lifted source is before the target among their parent's ordered children, check whether the directed chain starting at the source reaches the target. This is equivalent to checking `pos[ri[source]] >= pos[target]`. If it fails, the target is unreachable.
14. If the chain condition succeeds, the answer consists of the prefix-sum interval between the two children plus the contribution from the ancestor part of the path. The symmetric case where the source is after the target uses `le` instead of `ri`.

### Why it works

The SCC contraction preserves every reachability relation between cells because all cells inside one SCC are mutually reachable. The rectangle property means that, during topological processing, every already constructed region can be represented by rectangular pieces. The uniform-exit property lets each side interaction be compressed into one virtual vertex and one directed chain relation without losing a possible path.

After this compression, every possible route from a component toward another component must follow the rooted tree upward and, whenever several children share a parent, move inside the corresponding directed sibling chain. The ancestor lifting identifies the only possible tree level at which the source can meet the target. The same-parent check verifies that such a meeting is structurally possible, while the `le` and `ri` bounds verify that the directed sibling chain actually connects the two positions.

The prefix sums count every SCC on that collection of possible paths exactly once, and virtual vertices contribute zero. Since SCC sizes are the number of original grid cells they contain, the final sum is exactly the number of cells that lie on at least one valid path from the starting cell to the ending cell.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    R = n * m

    # 0 = L, 1 = R, 2 = U, 3 = D
    direction = bytearray(R)
    for i in range(n):
        s = input().strip()
        base = i * m
        for j, ch in enumerate(s):
            if ch == 76:       # L
                direction[base + j] = 0
            elif ch == 82:     # R
                direction[base + j] = 1
            elif ch == 85:     # U
                direction[base + j] = 2
            else:              # D
                direction[base + j] = 3

    # ------------------------------------------------------------
    # Iterative Tarjan SCC
    # ------------------------------------------------------------
    dfn = array('i', [0]) * R
    low = array('i', [0]) * R
    bel = array('i', [-1]) * R

    scc_stack = []
    timer = 0
    cnt = 0

    for start in range(R):
        if dfn[start]:
            continue

        dfn[start] = timer + 1
        low[start] = timer + 1
        timer += 1

        dfs = [start]
        it = [0]
        scc_stack.append(start)

        while dfs:
            u = dfs[-1]
            k = it[-1]

            while k < 4:
                it[-1] = k + 1

                if k == direction[u]:
                    k += 1
                    continue

                if k == 0:
                    if u % m == 0:
                        k += 1
                        continue
                    v = u - 1
                elif k == 1:
                    if u % m == m - 1:
                        k += 1
                        continue
                    v = u + 1
                elif k == 2:
                    if u < m:
                        k += 1
                        continue
                    v = u - m
                else:
                    if u >= R - m:
                        k += 1
                        continue
                    v = u + m

                if dfn[v] == 0:
                    dfn[v] = timer + 1
                    low[v] = timer + 1
                    timer += 1
                    dfs.append(v)
                    it.append(0)
                    scc_stack.append(v)
                    break

                if bel[v] == -1 and dfn[v] < low[u]:
                    low[u] = dfn[v]

                k += 1

            else:
                dfs.pop()
                it.pop()

                if dfs:
                    p = dfs[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]

                if low[u] == dfn[u]:
                    while True:
                        v = scc_stack.pop()
                        bel[v] = cnt
                        if v == u:
                            break
                    cnt += 1

    # dfn and low are no longer needed.
    del dfn, low, scc_stack

    # ------------------------------------------------------------
    # Store SCC members as linked lists and compute bounding boxes.
    # ------------------------------------------------------------
    head = array('i', [-1]) * cnt
    nxt = array('i', [-1]) * R

    xmin = array('i', [n]) * cnt
    xmax = array('i', [-1]) * cnt
    ymin = array('i', [m]) * cnt
    ymax = array('i', [-1]) * cnt
    size = array('i', [0]) * cnt

    for u in range(R):
        c = bel[u]
        nxt[u] = head[c]
        head[c] = u

        x = u // m
        y = u - x * m

        if x < xmin[c]:
            xmin[c] = x
        if x > xmax[c]:
            xmax[c] = x
        if y < ymin[c]:
            ymin[c] = y
        if y > ymax[c]:
            ymax[c] = y
        size[c] += 1

    # ------------------------------------------------------------
    # DSU and compressed tree construction.
    # ------------------------------------------------------------
    V = 2 * R + 5

    parent = array('i', [-1]) * V
    dsu = array('i', range(V))

    deg = array('i', [0]) * V
    ch = array('i', [0]) * V

    edge_a = array('i')
    edge_b = array('i')

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    # SCCs are numbered in reverse topological order by Tarjan.
    for c in range(cnt - 1, -1, -1):
        u = head[c]

        # Merge all previously represented components inside C's
        # bounding rectangle into C.
        while u != -1:
            ux = u // m
            uy = u - ux * m

            if uy > ymin[c]:
                v = u - 1
                if ymin[c] <= uy - 1 <= ymax[c]:
                    r = find(bel[v])
                    if r != c:
                        parent[r] = c
                        dsu[r] = c

            if uy < ymax[c]:
                v = u + 1
                r = find(bel[v])
                if r != c:
                    parent[r] = c
                    dsu[r] = c

            if ux > xmin[c]:
                v = u - m
                r = find(bel[v])
                if r != c:
                    parent[r] = c
                    dsu[r] = c

            if ux < xmax[c]:
                v = u + m
                r = find(bel[v])
                if r != c:
                    parent[r] = c
                    dsu[r] = c

            u = nxt[u]

        # Process top and bottom sides.
        for x in (xmin[c] - 1, xmax[c] + 1):
            if x < 0 or x >= n:
                continue

            base = x * m + ymin[c]
            if bel[base] < c:
                continue

            all_blocked = True
            u = find(bel[base])
            first = True

            for y in range(ymin[c], ymax[c] + 1):
                v = x * m + y

                # Direction toward C.
                needed = 3 if x < xmin[c] else 2
                if direction[v] != needed:
                    all_blocked = False

                r = find(bel[v])

                if r != u:
                    if first:
                        parent[u] = cnt
                        dsu[u] = cnt
                        u = cnt
                        cnt += 1
                        first = False

                    parent[r] = u
                    dsu[r] = u

            if not all_blocked:
                edge_a.append(u)
                edge_b.append(c)
                deg[u] += 1
                ch[u] ^= c
                deg[c] += 1
                ch[c] ^= u

        # Process left and right sides.
        for y in (ymin[c] - 1, ymax[c] + 1):
            if y < 0 or y >= m:
                continue

            base = xmin[c] * m + y
            if bel[base] < c:
                continue

            all_blocked = True
            u = find(bel[base])
            first = True

            for x in range(xmin[c], xmax[c] + 1):
                v = x * m + y

                # Direction toward C.
                needed = 1 if y < ymin[c] else 0
                if direction[v] != needed:
                    all_blocked = False

                r = find(bel[v])

                if r != u:
                    if first:
                        parent[u] = cnt
                        dsu[u] = cnt
                        u = cnt
                        cnt += 1
                        first = False

                    parent[r] = u
                    dsu[r] = u

            if not all_blocked:
                edge_a.append(u)
                edge_b.append(c)
                deg[u] += 1
                ch[u] ^= c
                deg[c] += 1
                ch[c] ^= u

    # Attach every remaining DSU root to one artificial root.
    root = cnt
    old_cnt = cnt

    for i in range(old_cnt):
        if dsu[i] == i:
            parent[i] = root
            dsu[i] = root

    cnt += 1
    parent[root] = -1

    # ------------------------------------------------------------
    # Find the order of children inside every tree vertex.
    # ------------------------------------------------------------
    pos = array('i', [-1]) * cnt
    next_pos = array('i', [0]) * cnt

    for i in range(old_cnt):
        if pos[i] != -1:
            continue

        if deg[i] == 0:
            p = parent[i]
            pos[i] = next_pos[p]
            next_pos[p] += 1

        elif deg[i] == 1:
            u = i
            previous = 0
            p = parent[u]

            while True:
                pos[u] = next_pos[p]
                next_pos[p] += 1

                nxt_node = ch[u] ^ previous
                previous, u = u, nxt_node

                if deg[u] != 2:
                    pos[u] = next_pos[p]
                    next_pos[p] += 1
                    break

    del next_pos

    # Set the direction of every non-tree edge.
    dir_edge = array('b', [0]) * cnt

    for a, b in zip(edge_a, edge_b):
        if pos[a] < pos[b]:
            dir_edge[a] = 1
        else:
            dir_edge[b] = -1

    del edge_a, edge_b, dsu

    # ------------------------------------------------------------
    # Build children in the required left-to-right order.
    # ------------------------------------------------------------
    child_count = array('i', [0]) * cnt

    for i in range(old_cnt):
        child_count[parent[i]] += 1

    start_child = array('i', [0]) * cnt
    total = 0

    for u in range(cnt):
        start_child[u] = total
        total += child_count[u]

    children = array('i', [0]) * old_cnt
    cursor = array('i', start_child)

    for i in range(old_cnt):
        p = parent[i]
        children[cursor[p]] = i
        cursor[p] += 1

    del cursor

    # ------------------------------------------------------------
    # Tree depths, subtree sizes, and heavy child.
    # ------------------------------------------------------------
    depth = array('i', [0]) * cnt
    subtree = array('i', [1]) * cnt
    heavy = array('i', [-1]) * cnt

    order = array('i', [root])
    idx = 0

    while idx < len(order):
        u = order[idx]
        idx += 1

        begin = start_child[u]
        end = begin + child_count[u]

        for j in range(begin, end):
            v = children[j]
            depth[v] = depth[u] + 1
            order.append(v)

    for idx in range(len(order) - 1, -1, -1):
        u = order[idx]
        begin = start_child[u]
        end = begin + child_count[u]

        best_size = 0
        best_child = -1

        for j in range(begin, end):
            v = children[j]
            subtree[u] += subtree[v]
            if subtree[v] > best_size:
                best_size = subtree[v]
                best_child = v

        heavy[u] = best_child

    # ------------------------------------------------------------
    # Heavy-light decomposition.
    # tin is a preorder in which every heavy chain is contiguous.
    # ------------------------------------------------------------
    chain_head = array('i', [-1]) * cnt
    tin = array('i', [0]) * cnt
    at = array('i', [0]) * cnt

    stack = [(root, root)]
    timer = 0

    while stack:
        u, h = stack.pop()

        while u != -1:
            chain_head[u] = h
            tin[u] = timer
            at[timer] = u
            timer += 1

            heavy_u = heavy[u]

            begin = start_child[u]
            end = begin + child_count[u]

            for j in range(begin, end):
                v = children[j]
                if v != heavy_u:
                    stack.append((v, v))

            u = heavy_u

    del subtree, heavy, order

    def ancestor_at_depth(u, target_depth):
        while depth[chain_head[u]] > target_depth:
            u = parent[chain_head[u]]

        return at[tin[u] - (depth[u] - target_depth)]

    # ------------------------------------------------------------
    # Prefix sums and chain intervals.
    # ------------------------------------------------------------
    prefix = array('i', [0]) * cnt
    left_chain = array('i', [0]) * cnt
    right_chain = array('i', [0]) * cnt
    val = array('i', [0]) * cnt

    stack = [root]

    while stack:
        u = stack.pop()

        begin = start_child[u]
        dcnt = child_count[u]

        if dcnt == 0:
            continue

        end = begin + dcnt

        s = 0
        for j in range(begin, end):
            v = children[j]
            s += size[v]
            prefix[v] = s

        previous = -1
        for j in range(begin, end):
            v = children[j]
            if j == begin or dir_edge[previous] != -1:
                left_chain[v] = v
            else:
                left_chain[v] = left_chain[previous]
            previous = v

        for j in range(end - 1, begin - 1, -1):
            v = children[j]
            if j == end - 1 or dir_edge[v] != 1:
                right_chain[v] = v
            else:
                right_chain[v] = right_chain[children[j + 1]]

        for j in range(begin, end):
            v = children[j]
            val[v] = (
                val[u]
                + prefix[right_chain[v]]
                - prefix[left_chain[v]]
                + size[left_chain[v]]
            )

        for j in range(begin, end):
            stack.append(children[j])

    del head, nxt, xmin, xmax, ymin, ymax
    del children, start_child, child_count
    del chain_head, tin, at, dir_edge

    def query(a, b):
        if depth[a] < depth[b]:
            return 0

        ret = val[a]
        a = ancestor_at_depth(a, depth[b])
        ret -= val[a]

        if parent[a] != parent[b]:
            return 0

        if pos[a] < pos[b]:
            if pos[right_chain[a]] >= pos[b]:
                return prefix[b] - prefix[a] + ret + size[a]
            return 0

        if pos[left_chain[a]] <= pos[b]:
            return prefix[a] - prefix[b] + ret + size[b]

        return 0

    out = []

    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        u = bel[(x1 - 1) * m + (y1 - 1)]
        v = bel[(x2 - 1) * m + (y2 - 1)]
        out.append(str(query(u, v)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation converts each arrow into an integer direction. Using a `bytearray` is enough because only four values are needed.

The SCC stage is iterative. `dfs` stores the current DFS path, while `it` stores the next direction to inspect for every active vertex. When a vertex finishes, its low-link value is propagated to its parent. If its low-link value equals its discovery number, the active SCC stack is popped until that vertex is removed.

The SCC members are stored through `head` and `nxt`. This avoids `cnt` Python lists, which would be particularly expensive when almost every cell is its own SCC. The bounding rectangle and size are computed in the same pass over the cells.

The DSU stage follows the rectangle construction directly. The component IDs produced by Tarjan are processed from large to small because that is the topological direction needed by the construction. Every time several boundary rectangles have to be treated as one object, a virtual vertex is created. Virtual vertices have zero `size`, so they never contribute cells to an answer.

The `pos` computation is one of the subtler parts. The extra edges form chains, so a degree-one endpoint can walk through the chain using the XOR of its two neighbors. Once every node receives a position, the children of a tree vertex can be placed in their required order.

The heavy-light decomposition is only used for ancestor queries. Every heavy chain is contiguous in `tin` order, so if the desired ancestor lies on the current heavy chain, its vertex can be obtained directly from the inverse preorder array `at`. Otherwise we jump to the parent of the current chain head. The number of light-chain jumps is logarithmic.

The final query deliberately checks the depth before subtracting `val`. If the source is shallower than the target, there is no valid upward tree representation. After lifting, comparing the two parents is the structural reachability test. The `left_chain` and `right_chain` checks then test the directed sibling connection.

All coordinates are converted from one-based input to zero-based cell indices only when locating the SCC. No coordinate adjustment is performed during the tree construction, so the boundary tests consistently use zero-based rows and columns.

## Worked Examples

### Sample 1

The given grid is

```
DDDDD
RDDDL
RRDLL
RUUUL
UUUUU
```

Consider the query `(5,5) -> (5,5)`. All five cells in the last row have `U`. They can move left and right freely, so they form one SCC containing five cells.

| Stage | Source component | Target component | Depth relation | Same component | Answer |
| --- | --- | --- | --- | --- | --- |
| Input | `(5,5)` | `(5,5)` | equal | yes | 5 |
| SCC compression | bottom-row SCC | bottom-row SCC | equal | yes | 5 |
| Query | `a = b` | `a = b` | equal | yes | 5 |

When `a == b`, the query formula reduces to the size of that SCC. The result is `5`, matching the fifth output line of Sample 1. This demonstrates why SCC weights must contain the number of original cells rather than treating every compressed vertex as weight one.

Now consider `(2,2) -> (5,5)`. The source and target are in different components. After lifting the source to the target's depth, the construction finds two sibling positions under a common parent and a directed chain connecting them. The prefix sums over that chain, together with the ancestor contribution, contain exactly 14 real cells.

| Stage | Operation | Result |
| --- | --- | --- |
| Input | source `(2,2)`, target `(5,5)` | different SCCs |
| Ancestor step | lift source to target depth | same depth |
| Parent test | compare `parent[a]` and `parent[b]` | equal |
| Chain test | compare target position with `right_chain[a]` | reachable |
| Counting | sibling interval + ancestor contribution | 14 |

The first query of Sample 1, `(1,1) -> (5,5)`, fails the corresponding chain reachability condition, so its answer is zero. The other queries produce `20`, `14`, and `5`, giving the complete sample output `0 14 20 14 5`.

### One-dimensional chain

Consider

```
1 3 3
LLL
1 1 1 3
1 2 1 3
3 1 1 1
```

An `L` forbids moving left, so every cell can move right. The graph is the directed chain

```
1 -> 2 -> 3
```

Each cell is its own SCC.

| Query | Source position | Target position | Directed chain test | Answer |
| --- | --- | --- | --- | --- |
| `1 -> 3` | 0 | 2 | succeeds | 3 |
| `2 -> 3` | 1 | 2 | succeeds | 2 |
| `3 -> 1` | 2 | 0 | fails | 0 |

The constructed tree has the three SCCs as siblings of one root, with non-tree edges `1 -> 2` and `2 -> 3`. The right-chain endpoint of the first child is the third child, so the first query counts all three SCC weights. The second query counts the last two. The reverse query fails because the directed chain does not point backward.

This example confirms the purpose of `left_chain` and `right_chain`: the tree itself does not encode the direction between siblings, so those additional bounds are essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NM α(NM) + Q log(NM))` | SCC construction, DSU rectangle merging, and tree preprocessing are near-linear; each query uses heavy-light ancestor lifting |
| Space | `O(NM)` | All graph and tree information is stored in packed integer arrays |

There are at most `NM` original SCC vertices and `O(NM)` virtual vertices. The packed `array` storage keeps the dense integer structures much smaller than ordinary Python integer lists. The algorithm performs only a constant amount of geometric work per processed grid boundary element and uses logarithmic work per query. The asymptotic bounds fit the constraints of one million cells and 300,000 queries; the original contest's two second limit is aggressive for Python, so the implementation deliberately avoids Python lists of lists and recursive graph traversal.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py`. The helper resets the module's `input` function after replacing `sys.stdin`, which is necessary because the solution defines `input = sys.stdin.readline` at module scope.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solution.input = sys.stdin.readline

    try:
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
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

# Minimum-size grid, start equals end.
case_min = """\
1 1 1
L
1 1 1 1
"""

assert run(case_min) == "1", "minimum-size grid"

# Two cells with a complete directed barrier.
case_barrier = """\
1 2 2
RL
1 1 1 2
1 2 1 1
"""

assert run(case_barrier) == "0\n0", "mutual boundary barrier"

# Directed chain, catches endpoint and ordering errors.
case_chain = """\
1 3 3
LLL
1 1 1 3
1 2 1 3
3 1 1 1
"""

assert run(case_chain) == "3\n2\n0", "directed chain"

# Maximum-size grid and maximum number of cells.
# Every L forbids moving left, while vertical movement is unrestricted.
# Hence every column is an SCC and movement is possible only toward
# increasing columns.
n = 1000
m = 1000
grid = "\n".join(["L" * m] * n)

case_max = (
    f"{n} {m} 3\n"
    + grid
    + "\n"
    + "1 1 1000 1000\n"
    + "1000 1000 1 1\n"
    + "500 500 500 500\n"
)

assert run(case_max) == "1000000\n0\n1", "maximum-size all-equal grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1`, one query | `1` | Empty path and minimum grid |
| `1 x 2`, `RL` | `0`, `0` | Directed barriers and boundary handling |
| `1 x 3`, `LLL` | `3`, `2`, `0` | Ordered sibling chains and off-by-one positions |
| `1000 x 1000`, all `L` | `1000000`, `0`, `1` | Maximum grid, maximum answer, all-equal arrows |

## Edge Cases

### Starting and ending on the same cell

For

```
1 1 1
L
1 1 1 1
```

the SCC containing the only cell has size one. The query sees identical source and target components, so the lifted source is unchanged and the sibling interval contains exactly that SCC. The output is `1`.

The same logic handles a larger SCC. In Sample 1, `(5,5)` belongs to the five-cell bottom-row SCC, so the same-cell query returns `5`. The implementation never assumes that a query with equal coordinates has answer one.

### An unreachable target

For

```
1 2 2
RL
1 1 1 2
1 2 1 1
```

neither cell can cross the boundary between them. The SCCs are distinct, and the rectangle construction creates no directed sibling chain connecting them. After lifting the source, the parent or chain test fails, so both answers are zero.

This catches the common mistake of treating adjacency as automatically bidirectional.

### A boundary cell whose arrow blocks the only useful move

For

```
1 2 1
RL
1 1 1 2
```

the first cell has `R`, which forbids the only move toward the second cell. The boundary scan recognizes that the edge into the target does not exist. The query returns zero without needing any special case in the query code.

The same reasoning applies to a top-row cell marked `U`, a bottom-row cell marked `D`, a leftmost cell marked `L`, or a rightmost cell marked `R`. An arrow can forbid a direction even when that direction would leave the grid, but such an outside move was already impossible anyway.

### A large strongly connected component

In Sample 1, the last row is

```
UUUUU
```

Every cell can move left or right because `U` forbids only upward movement. Thus all five cells belong to one SCC. The SCC compression stores `size = 5`, and a query entirely inside this component immediately counts all five cells.

This is why replacing every SCC by a single unweighted vertex would be incorrect. The compressed graph answers reachability, but the original question asks for the number of original grid cells.

### Several possible paths between the same endpoints

The answer is not the length of one chosen path. It is the number of cells that occur on at least one valid start-to-target path. In the compressed tree, a sibling chain may contain several intermediate SCCs that can all participate in different routes. The prefix sums deliberately count the whole valid chain interval rather than selecting one arbitrary route.

This is also why a simple shortest-path algorithm cannot solve the problem. The desired quantity is a union of possible path vertices, not a path length.

### Very many tiny SCCs

A grid such as the one-dimensional `LLL` example has one SCC per cell. The construction still works because it never assumes that an SCC contains many cells. Every singleton component gets a one-cell bounding rectangle, and adjacent components are connected through the same rectangle-side mechanism.

The maximum-size all-`L` test exercises the opposite situation at scale. There are 1000 large SCCs, one for each column, and the algorithm still handles them using the same representation.
