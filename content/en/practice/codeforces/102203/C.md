---
title: "CF 102203C - \u0424\u0430\u0431\u0440\u0438\u043a\u0430"
description: "The factory is a tree. Every room is a vertex, every corridor is an edge, and because there are exactly (n-1) corridors and exactly one path between every pair of rooms, the path between two rooms is unique."
date: "2026-08-18T11:23:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "C"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 153
verified: true
draft: false
---

[CF 102203C - \u0424\u0430\u0431\u0440\u0438\u043a\u0430](https://codeforces.com/problemset/problem/102203/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The factory is a tree. Every room is a vertex, every corridor is an edge, and because there are exactly (n-1) corridors and exactly one path between every pair of rooms, the path between two rooms is unique.

For every request ((s_i,f_i)), people must be able to walk from (s_i) to (f_i) after every corridor has been made one-way. Since the underlying graph is a tree, there is only one possible route from (s_i) to (f_i). Consequently, every edge on that route has a forced direction. The task is to determine whether all these forced directions are mutually consistent, and if they are, output one orientation of every corridor satisfying all requests.

The constraints reach (2\cdot10^5) for both the number of rooms and the number of requests. A solution that examines every possible orientation is immediately impossible because a tree with (n-1) edges has (2^{n-1}) orientations. Even an approach that explicitly walks along every requested path can reach (O(nm)), which is about (4\cdot10^{10}) edge visits at the maximum size. The intended solution has to process the tree and all requests almost linearly.

There are several edge cases that easily break an implementation. The first is a request whose endpoints are equal. For example,

```
1 1
1 1
```

has no corridor at all and is obviously satisfiable, so the answer is `YES`. A path-difference implementation that assumes the two endpoints are distinct can accidentally introduce a fake constraint.

The second is two requests demanding opposite directions on the same edge:

```
2 2
1 2
1 2
2 1
```

The correct answer is `NO`. Both requests use the only edge, but one requires (1\to2) while the other requires (2\to1). Checking requests independently and orienting an edge when it is first encountered can silently accept this case.

The third is a request that travels through several ancestors. Consider

```
3 1
1 2
2 3
3 1
```

The only valid orientation is (3\to2\to1). An approach that simply orients every edge from the chosen root toward its children would produce (1\to2\to3), which satisfies the tree structure but violates the request.

## Approaches

The most direct approach is to enumerate every orientation of the (n-1) edges. For each orientation, inspect every request and check whether all edges on its unique path point from its start to its finish. This is correct because every possible answer is explicitly considered. With a straightforward path traversal, one orientation can require (O(mn)) work in the worst case, so the total is (O(2^{n-1}mn)). Even before reaching large values of (n), this becomes useless.

A better direction is to stop thinking about complete orientations and instead ask what each individual edge is required to do. Root the tree at room (1). Every non-root vertex (v) has an edge between (v) and its parent (p(v)). A request can cross this edge in exactly one of two ways. If it goes from the subtree of (v) toward the parent, the edge must be (v\to p(v)). If it goes from the parent side into the subtree, the edge must be (p(v)\to v).

For one request (s\to f), let (l) be the lowest common ancestor of (s) and (f). The path splits into an upward part from (s) to (l), followed by a downward part from (l) to (f). This is the key structural observation. We can record all upward requirements with one tree-difference array and all downward requirements with another.

For the upward part (s\to l), add (1) at (s) and subtract (1) at (l). After summing values from children toward parents, an edge ((p(v),v)) receives a positive upward count exactly when some request requires (v\to p(v)).

For the downward part (l\to f), add (1) at (f) and subtract (1) at (l). The same bottom-up accumulation then gives a positive downward count exactly when some request requires (p(v)\to v).

Thus an edge is impossible precisely when both counts are positive. If only the upward count is positive, orient the edge upward. If only the downward count is positive, orient it downward. If neither count is positive, the edge is unrestricted and can be oriented arbitrarily.

The remaining problem is finding all LCAs efficiently. Since all requests are known before processing begins, we can use Tarjan's offline LCA algorithm. It processes the tree in postorder while a DSU represents already completed subtrees. Every LCA request is answered when one endpoint becomes processed and the other endpoint has already been processed. With path compression and union by rank, this takes almost linear time.

The brute-force works because it explicitly tests every possible orientation, but fails because the number of orientations is exponential. The observation that every request only imposes independent directions on individual tree edges lets us aggregate all requests with tree differences, while offline LCA supplies the only structural information needed to split each path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{n-1}mn)) | (O(n+m)) | Too slow |
| Optimal | (O((n+m)\alpha(n))) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex (1), and compute the parent of every vertex together with a DFS order. The reverse of this order is a valid postorder, so it lets us process every child before its parent without recursion.
2. Store every request twice in a query adjacency structure. For request (i=(s_i,f_i)), attach (f_i) to (s_i) and (s_i) to (f_i). We need this structure because Tarjan's offline LCA algorithm answers a request when either endpoint is processed.
3. Run Tarjan's offline LCA algorithm. Every vertex initially forms its own DSU set. When a vertex has finished, its set is merged into its parent, and the DSU representative stores the current tree ancestor of that set. When both endpoints of a request have been processed, `ancestor[find(other)]` is their LCA.
4. For every request (s\to f), let (l=\operatorname{LCA}(s,f)). Increment `up[s]` and decrement `up[l]`. This represents the segment (s\to l), where every crossed edge must point toward the root.
5. For the same request, increment `down[f]` and decrement `down[l]`. This represents (l\to f), where every crossed edge must point away from the root.
6. Traverse the tree in reverse DFS order and add every vertex's `up` and `down` values to its parent. After this accumulation, for every non-root vertex (v), `up[v]` counts requests that require (v\to parent[v]), while `down[v]` counts requests that require (parent[v]\to v).
7. If both `up[v]` and `down[v]` are positive, output `NO`. The same corridor is required in both directions, so no orientation can satisfy all requests.
8. Otherwise orient the edge between (v) and `parent[v]` according to the available requirement. An upward requirement gives (v\to parent[v]), a downward requirement gives (parent[v]\to v), and an unconstrained edge can use (parent[v]\to v).

Why it works: for every request (s\to f), its unique tree path is exactly the concatenation of (s\to l) and (l\to f), where (l) is their LCA. The difference updates mark every edge of the first segment as requiring the upward direction and every edge of the second segment as requiring the downward direction. After accumulation, each edge therefore knows all directions demanded by all requests. If both directions occur, the instance is impossible. If at most one direction occurs, choosing that direction satisfies every request using the edge. Since every request consists entirely of such edges, the resulting orientation satisfies all requests.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    # Compact forward-star representation of the tree.
    head = array('i', [-1]) * n
    to = array('i')
    nxt = array('i')

    eu = array('i')
    ev = array('i')

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        eid = len(to)
        to.append(v)
        nxt.append(head[u])
        head[u] = eid

        eid += 1
        to.append(u)
        nxt.append(head[v])
        head[v] = eid

        eu.append(u)
        ev.append(v)

    # Store requests.
    qs = array('i')
    qf = array('i')

    # Query adjacency for Tarjan's offline LCA.
    qhead = array('i', [-1]) * n
    qto = array('i')
    qnext = array('i')
    qid = array('i')

    for i in range(m):
        s, f = map(int, input().split())
        s -= 1
        f -= 1

        qs.append(s)
        qf.append(f)

        idx = len(qto)
        qto.append(f)
        qid.append(i)
        qnext.append(qhead[s])
        qhead[s] = idx

        idx = len(qto)
        qto.append(s)
        qid.append(i)
        qnext.append(qhead[f])
        qhead[f] = idx

    # Root the tree at 0 and build a DFS order.
    parent = array('i', [-1]) * n
    parent[0] = 0
    order = []

    stack = [0]
    while stack:
        v = stack.pop()
        order.append(v)

        e = head[v]
        while e != -1:
            u = to[e]
            if u != parent[v]:
                parent[u] = v
                stack.append(u)
            e = nxt[e]

    # Tarjan offline LCA.
    dsu = array('i', range(n))
    rank = array('b', [0]) * n
    ancestor = array('i', range(n))
    visited = bytearray(n)
    lca = array('i', [-1]) * m

    def find(x):
        root = x
        while dsu[root] != root:
            root = dsu[root]

        while dsu[x] != x:
            y = dsu[x]
            dsu[x] = root
            x = y

        return root

    for pos in range(n - 1, -1, -1):
        v = order[pos]

        # All child subtrees have already been merged into v.
        rv = find(v)
        ancestor[rv] = v
        visited[v] = 1

        # Answer queries whose other endpoint is already processed.
        e = qhead[v]
        while e != -1:
            other = qto[e]
            idx = qid[e]

            if visited[other] and lca[idx] == -1:
                lca[idx] = ancestor[find(other)]

            e = qnext[e]

        # Merge v into its parent after processing queries at v.
        if v != 0:
            p = parent[v]
            rv = find(v)
            rp = find(p)

            if rv != rp:
                if rank[rv] < rank[rp]:
                    dsu[rv] = rp
                    ancestor[rp] = p
                elif rank[rv] > rank[rp]:
                    dsu[rp] = rv
                    ancestor[rv] = p
                else:
                    dsu[rp] = rv
                    rank[rv] += 1
                    ancestor[rv] = p

    # We no longer need the query graph or DSU.
    del qhead, qto, qnext, qid
    del dsu, rank, ancestor, visited

    # Difference arrays for upward and downward requirements.
    up = array('i', [0]) * n
    down = array('i', [0]) * n

    for i in range(m):
        s = qs[i]
        f = qf[i]
        l = lca[i]

        up[s] += 1
        up[l] -= 1

        down[f] += 1
        down[l] -= 1

    del qs, qf, lca

    # Accumulate subtree differences from children to parents.
    possible = True

    for pos in range(n - 1, 0, -1):
        v = order[pos]

        if up[v] > 0 and down[v] > 0:
            possible = False
            break

        p = parent[v]
        up[p] += up[v]
        down[p] += down[v]

    if not possible:
        print("NO")
        return

    # Orient every original edge.
    answer = ["YES"]

    for i in range(n - 1):
        a = eu[i]
        b = ev[i]

        if parent[a] == b:
            child = a
            par = b
        else:
            child = b
            par = a

        if up[child] > 0:
            answer.append(f"{child + 1} {par + 1}")
        else:
            # This covers both down[child] > 0 and the unconstrained case.
            answer.append(f"{par + 1} {child + 1}")

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The tree is stored with a compact forward-star representation instead of a Python list of lists. At (2\cdot10^5) vertices, this keeps the memory footprint predictable. The original endpoints are also retained because the required output can list the edges in any order, but the orientation has to be reconstructed for each original edge.

The first DFS only establishes `parent` and `order`. Because the graph is guaranteed to be a tree, checking `u != parent[v]` is enough to avoid walking back toward the parent. No recursive DFS is used, since a tree can be a chain of (2\cdot10^5) vertices and would exceed Python's recursion limit.

Tarjan's part uses a separate DSU parent array. This is deliberately different from the tree's `parent` array. The tree parent describes the actual rooted tree, while the DSU parent describes temporary sets of already processed subtrees. The `ancestor` array connects a DSU representative back to the tree vertex that currently acts as the ancestor of that set.

The order inside the Tarjan loop matters. A vertex is marked as processed and its queries are answered before it is merged into its own parent. If the merge happened first, a query whose LCA is the current vertex could observe a higher ancestor and receive an incorrect answer.

The two difference arrays use signed 32-bit integers. Every value is bounded by the number of requests, so it comfortably fits in this range. Python itself also has arbitrary-precision integers, but compact arrays substantially reduce memory consumption.

The final orientation uses the child endpoint of every rooted edge. `up[child] > 0` means that at least one request requires the edge to point from the child toward its parent. If this is not the case, the edge can safely point from parent to child because either a downward request requires it or nobody cares about it.

## Worked Examples

For Sample 1, root the tree at vertex (1). The rooted edges are (1-2), (1-4), (4-3), and (3-5). The LCAs and the two path segments are:

| Request | LCA | Upward segment | Downward segment |
| --- | --- | --- | --- |
| (1\to2) | 1 | empty | (1\to2) |
| (5\to3) | 3 | (5\to3) | empty |
| (5\to4) | 4 | (5\to3\to4) | empty |
| (1\to4) | 1 | empty | (1\to4) |
| (3\to4) | 4 | empty | empty relative to the rooted split |

The last request actually has (4) as its LCA because (4) is an ancestor of (3), so its upward segment is (3\to4). After accumulation, the constrained edges have these directions:

| Edge | Up count | Down count | Chosen direction |
| --- | --- | --- | --- |
| (1-2) | 0 | 1 | (1\to2) |
| (1-4) | 0 | 1 | (1\to4) |
| (4-3) | 2 | 0 | (3\to4) |
| (3-5) | 2 | 0 | (5\to3) |

No edge has positive counts in both directions, so the instance is feasible. The output shown in the statement is one valid orientation, and the algorithm may produce a different one because unconstrained edges can be oriented arbitrarily.

For Sample 2, the important intermediate state is the set of LCAs:

| Request | LCA | Up update | Down update |
| --- | --- | --- | --- |
| (6\to10) | 1 | (up[6]++, up[1]--) | (down[10]++, down[1]--) |
| (13\to1) | 1 | (up[13]++, up[1]--) | no net change |
| (5\to14) | 1 | (up[5]++, up[1]--) | (down[14]++, down[1]--) |
| (15\to12) | 12 | (up[15]++, up[12]--) | no net change |
| (2\to8) | 2 | no net change | (down[8]++, down[2]--) |

After the bottom-up accumulation, every edge gets at most one positive direction count. For example, edge (1-2) receives an upward requirement from (6\to10), so it must be (2\to1). Edge (1-3) receives a downward requirement from (6\to10), so it must be (1\to3). Edge (2-8) receives a downward requirement from (2\to8), so it must be (2\to8).

The resulting directions include the paths

```
6 -> 2 -> 1 -> 3 -> 10
13 -> 11 -> 4 -> 1
5 -> 1 -> 3 -> 9 -> 12 -> 14
15 -> 12
2 -> 8
```

which demonstrates the central invariant: every requested path is assembled entirely from edges whose direction was independently fixed by the corresponding difference count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+m)\alpha(n))) | Tree traversal, Tarjan's DSU operations, and difference accumulation are all almost linear |
| Space | (O(n+m)) | The tree, query lists, DSU state, requests, and two difference arrays are stored |

The largest input has (2\cdot10^5) vertices and (2\cdot10^5) requests. The algorithm performs only a constant number of passes over the tree and the requests, with DSU operations having inverse-Ackermann amortized cost. This fits the required asymptotic bounds and avoids both exponential enumeration and explicit traversal of every requested path.

## Test Cases

The output of this problem is not unique, so the tests should not compare a successful orientation with one fixed string. The test harness below checks that `NO` is reported when necessary and, for `YES`, verifies that every produced edge is a valid original edge and that every requested route is actually directed from its source to its destination.

For the large test, checking every request by a full graph search would itself be unnecessarily expensive, so that case checks the structural properties of the output instead.

```python
# Save the editorial solution as solution.py before running these tests.

import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate_orientation(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)

    edges = set()
    for _ in range(n - 1):
        u = next(it)
        v = next(it)
        edges.add((u, v))
        edges.add((v, u))

    queries = []
    for _ in range(m):
        s = next(it)
        f = next(it)
        queries.append((s, f))

    lines = out.splitlines()
    if not lines:
        return False

    if lines[0] == "NO":
        return False

    if lines[0] != "YES":
        return False

    if len(lines) != n:
        return False

    directed = [[] for _ in range(n + 1)]

    for line in lines[1:]:
        a, b = map(int, line.split())
        if (a, b) not in edges:
            return False
        directed[a].append(b)

    # This validator is intended for small tests.
    for s, f in queries:
        seen = [False] * (n + 1)
        stack = [s]
        seen[s] = True

        while stack:
            v = stack.pop()
            if v == f:
                break

            for u in directed[v]:
                if not seen[u]:
                    seen[u] = True
                    stack.append(u)

        if not seen[f]:
            return False

    return True

# Sample 1
sample1 = """\
5 5
2 1
4 1
5 3
3 4
1 2
5 3
5 4
1 4
3 4
"""

out = run(sample1)
assert validate_orientation(sample1, out), "sample 1"

# Sample 2
sample2 = """\
15 5
1 2
1 3
1 4
1 5
2 6
2 7
2 8
3 9
3 10
4 11
9 12
11 13
12 14
12 15
6 10
13 1
5 14
15 12
2 8
"""

out = run(sample2)
assert validate_orientation(sample2, out), "sample 2"

# Sample 3
sample3 = """\
5 5
1 3
5 1
4 2
3 4
4 3
4 3
3 2
1 2
5 4
"""

assert run(sample3) == "NO", "sample 3"

# Minimum-size tree, equal endpoints, no edges to orient.
case_min = """\
1 1
1 1
"""

out = run(case_min)
assert out == "YES", "minimum-size case"

# Two opposite requirements on the only edge.
case_conflict = """\
2 2
1 2
1 2
2 1
"""

assert run(case_conflict) == "NO", "opposite directions"

# A request from a deep leaf to the root.
case_reverse_chain = """\
3 1
1 2
2 3
3 1
"""

out = run(case_reverse_chain)
assert validate_orientation(case_reverse_chain, out), "reverse chain"

# All requests have equal endpoints, so every edge is unconstrained.
case_equal = """\
4 4
1 2
2 3
3 4
2 2
2 2
2 2
2 2
"""

out = run(case_equal)
assert validate_orientation(case_equal, out), "equal endpoints"

# Maximum-size stress shape: a chain and many identical requests.
n = 200000
m = 200000

parts = [f"{n} {m}"]
for v in range(1, n):
    parts.append(f"{v} {v + 1}")
for _ in range(m):
    parts.append(f"1 {n}")

large_case = "\n".join(parts) + "\n"
out = run(large_case)

large_lines = out.splitlines()
assert large_lines[0] == "YES", "maximum-size case must be feasible"
assert len(large_lines) == n, "wrong number of output edges"

print("all tests passed")
```

The first custom case validates the (n=1) boundary, where the answer contains only `YES` and no edge descriptions. The second creates the smallest possible contradiction and catches implementations that only remember one direction per edge.

The reverse-chain case catches incorrect assumptions about the root orientation. The equal-endpoint case confirms that a request (s\to s) imposes no edge constraints at all. The maximum-size chain stresses the iterative traversal, compact storage, offline LCA processing, and output construction at the actual upper bound.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `YES` | Minimum-size tree and empty path |
| `2 2 / 1 2 / 1 2 / 2 1` | `NO` | Direct contradiction on one edge |
| `3 1 / 1 2 / 2 3 / 3 1` | `YES` with (3\to2\to1) | Leaf-to-root direction and path boundaries |
| `4 4 / 1 2 / 2 3 / 3 4 / 2 2 ...` | `YES` | All requests have zero-length paths |
| (n=m=200000), chain with requests (1\to n) | `YES` with all edges (v\to v+1) | Maximum input size and iterative implementation |

## Edge Cases

For the equal-endpoint case

```
1 1
1 1
```

the LCA is also vertex (1). Both difference updates cancel immediately: `up[1] += 1` followed by `up[1] -= 1`, and the same happens for `down`. There are no edges to inspect, so the algorithm prints `YES`.

For the direct contradiction

```
2 2
1 2
1 2
2 1
```

root vertex (1). The first request produces a downward requirement on edge (1-2), while the second produces an upward requirement on exactly the same edge. After accumulation, `down[2] = 1` and `up[2] = 1`. The conflict condition fires and the algorithm prints `NO`.

For the reverse chain

```
3 1
1 2
2 3
3 1
```

the LCA of (3) and (1) is (1). The upward difference updates are `up[3] += 1` and `up[1] -= 1`. Bottom-up accumulation transfers the value from vertex (3) to vertex (2), and then to vertex (1). Both edges consequently have a positive upward count and no downward count. They are oriented (3\to2) and (2\to1), exactly matching the requested path.

For the unconstrained-edge situation

```
4 4
1 2
2 3
3 4
2 2
2 2
2 2
2 2
```

every request has identical endpoints. Every LCA equals that endpoint, so every difference update cancels at the same vertex. All edges have zero counts in both directions. The algorithm chooses the default parent-to-child orientation, producing (1\to2), (2\to3), (3\to4), which is valid because no request needs to traverse an edge.
