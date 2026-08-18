---
title: "CF 102192G - Card Game"
description: "Each card has two numbers, say (x) on the current front and (y) on the back. Flipping the card changes which of these two numbers is visible. We need every visible number to be different, while flipping as few cards as possible."
date: "2026-08-18T20:27:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "G"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 242
verified: true
draft: false
---

[CF 102192G - Card Game](https://codeforces.com/problemset/problem/102192/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

Each card has two numbers, say (x) on the current front and (y) on the back. Flipping the card changes which of these two numbers is visible. We need every visible number to be different, while flipping as few cards as possible. Among all minimum-flip solutions, we also need to count how many different sets of cards can be flipped. Two solutions are considered the same only when they flip exactly the same card indices.

The useful representation is a graph. Treat every distinct number as a vertex and every card ((x,y)) as an undirected edge between (x) and (y). The currently visible number tells us which endpoint of the edge is selected. Thus every card initially points toward its visible number. After flipping a card, its edge points toward the other endpoint.

A number appears on the front of more than one card exactly when several edges point toward the same vertex. Consequently, the requirement that all visible numbers be unique is exactly the requirement that every vertex have indegree at most one in the final orientation.

The input allows (n) to reach (10^5), and the total (n) over all test cases reaches (10^6). An (O(n^2)) solution is already too slow for the largest tests, while an exponential search is completely infeasible. The intended solution must process every card and every number only a constant number of times, giving an (O(n)) solution per test case.

Several cases are easy to mishandle.

Consider

```
1
1
1 1
```

The answer is

```
0 1
```

The card is a self-loop, but both sides contain the same number, so flipping it changes nothing. A careless graph implementation that treats a loop as an ordinary reversible edge may count a fake second orientation.

Consider

```
1
2
1 2
1 3
```

The answer is

```
1 2
```

The graph is a tree. Choosing vertex 2 as the root requires flipping the second card, while choosing vertex 3 as the root requires flipping the first card. Both solutions use one flip. Looking only at the currently duplicated number and greedily fixing it can miss one of these two globally optimal choices.

Consider

```
1
3
1 2
2 3
1 3
```

The graph is a single cycle. There are exactly two possible valid orientations of the cycle. In this example both require one flip, so the answer is

```
1 2
```

A solution that assumes every cycle has only one optimal orientation would get the count wrong.

Finally, consider

```
1
2
1 1
1 1
```

The answer is

```
-1 -1
```

There are two cards but only one usable number. More generally, a connected component containing more edges than vertices cannot be oriented so that every vertex receives at most one incoming edge. Merely checking whether each individual duplicated number can be locally repaired is not enough.

## Approaches

The direct approach is to decide independently for every card whether it is flipped. There are (2^n) possible flip sets. For each set, we can inspect all (n) visible numbers, check whether they are distinct, and keep the minimum number of flips and its frequency. This is correct because it explicitly considers every possible final state. Its worst-case work is (O(n2^n)), which for (n=10^5) is roughly (10^5\cdot2^{100000}) operations and is far beyond feasible.

The graph formulation reveals why the search space has much more structure than (2^n). Every card becomes an edge whose chosen endpoint is its visible number. The final condition is simply indegree at most one.

For a connected component containing (v) vertices and (e) edges, the sum of all indegrees is exactly (e). Since every vertex can have indegree at most one, we must have (e\le v). A connected undirected graph with (e<v) is a tree, while a connected graph with (e=v) is unicyclic. If (e>v), the component is impossible.

This reduces the problem to two very structured cases.

For a tree, every valid orientation has exactly one vertex with indegree zero, because there are (v-1) edges and (v) vertices. Once that vertex is chosen as the root, every edge is forced to point away from the root. We only need to find which root minimizes the number of edges whose initial direction disagrees with this forced orientation. This is a standard rerooting dynamic programming problem.

For a unicyclic component, every vertex must have indegree exactly one. All edges in the trees attached to the cycle are forced to point away from the cycle. The cycle itself has only two possible orientations, clockwise or counterclockwise. We calculate the flip cost for both and keep the better one, counting both when they tie. A self-loop is a one-vertex cycle, but its two sides are identical, so it contributes only one possible flip set.

The key structural observation is thus that every solvable component is either a tree or a unicyclic graph. We can find the cycles by repeatedly removing degree-one vertices. The removed edges form the attached trees, while the edges left behind form the cycles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Build an undirected multigraph. Vertex (x) represents number (x), and card (i=(x,y)) becomes edge (i). Store (x) as the endpoint selected by the initial front side. Self-loops are allowed.
2. Regard the initial state as an orientation of every edge toward its current front number. A valid final state is exactly an orientation in which every vertex has indegree at most one. For every connected component, count its vertices and edges conceptually. If some component has more edges than vertices, output (-1\ -1), because its total indegree is too large to fit into its vertices.
3. Repeatedly remove vertices of degree one. When a leaf (v) is connected to its remaining neighbor (u) by edge (e), remove that edge and record (u) as the parent of (v). In every valid orientation where the surviving part contains the root or cycle, this tree edge must point from (u) to (v). Its contribution to the flip count is one exactly when the initial selected endpoint is (u).

The peeling process simultaneously identifies the graph structure. In a valid component that is a tree, every edge is eventually removed. In a valid unicyclic component, exactly the cycle edges remain.
4. After peeling, inspect the remaining degree of every vertex. A remaining vertex in a valid component must have degree exactly two, counting a self-loop twice. If some remaining vertex has a different positive degree, the component contains more than one cycle and is impossible.
5. Process every connected component. The vertices and edges are traversed once to collect its vertices and the total cost already contributed by its peeled tree edges. If no edge remains in the component, it is a tree. Otherwise, it is unicyclic.
6. For a tree component, the peeling process leaves exactly one vertex without a parent. That vertex is a natural root. Let `base` be the sum of the costs of all peeled edges. This is the cost when that last remaining vertex is the root, because every recorded parent-child edge is oriented from the parent to the child.
7. Reroot the tree from this root. Suppose an edge connects the current root-side vertex (v) to its child (u), and the initial front endpoint is (x). With root at (v), the desired direction is (v\to u), so this edge costs ([x=v]). After moving the root to (u), the desired direction becomes (u\to v), so the cost becomes ([x=u]). Therefore

[
cost[u]=cost[v]+[x=u]-[x=v].
]

Each edge changes the root exactly once during this traversal, so all possible root costs are obtained in linear time. Keep the minimum and count how many roots attain it.
8. For a unicyclic component, all peeled tree edges already have their forced orientations. Find the remaining cycle by following the unremoved edges from any remaining vertex.
9. Traverse the cycle in one direction. If a cycle edge goes from (u) to (v), its clockwise orientation selects (v), while the opposite orientation selects (u). Add one to the corresponding cost whenever the initial front endpoint is the opposite endpoint. For a cycle with more than one vertex, the two orientations produce different sets of flipped cards. If their costs are equal, both count.
10. For a self-loop, there is only one effective orientation because both endpoints are the same number. Its contribution is zero, and it contributes one way rather than two.
11. Add the minimum flip counts of all components. Since choices in different connected components are independent, multiply their numbers of optimal flip sets modulo (998244353).

The invariant behind the whole algorithm is that every peeled tree edge has only one possible direction in any valid solution once the surviving side is fixed. In a tree, the only remaining freedom is the choice of the root. In a unicyclic component, the attached trees have no freedom and the only remaining choice is the direction of the cycle. Thus the algorithm enumerates every possible valid orientation in a compressed form, without ever enumerating the (2^n) original flip sets.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        m = 2 * n
        V = m + 1

        # Forward-star adjacency.
        head = array('i', [-1]) * V
        to = array('i', [0]) * (2 * n)
        nxt = array('i', [0]) * (2 * n)

        # For edge i, x[i] is the initially visible endpoint.
        x = array('i', [0]) * n
        y = array('i', [0]) * n

        degree = array('i', [0]) * V

        for i in range(n):
            a, b = map(int, input().split())
            x[i] = a
            y[i] = b

            p = 2 * i
            to[p] = b
            nxt[p] = head[a]
            head[a] = p

            to[p + 1] = a
            nxt[p + 1] = head[b]
            head[b] = p + 1

            if a == b:
                degree[a] += 2
            else:
                degree[a] += 1
                degree[b] += 1

        # parent[v] is the vertex that survived when v was peeled.
        parent = array('i', [-1]) * V

        # child_cost[v] is the cost of edge parent[v] -> v
        # in the orientation forced by the surviving side.
        child_cost = bytearray(V)

        removed = bytearray(n)

        # Peel all trees from the outside toward their roots/cycles.
        queue = []
        for v in range(1, V):
            if head[v] != -1 and degree[v] == 1:
                queue.append(v)

        qpos = 0
        while qpos < len(queue):
            v = queue[qpos]
            qpos += 1

            if degree[v] != 1:
                continue

            arc = head[v]
            while arc != -1:
                e = arc >> 1
                if not removed[e]:
                    break
                arc = nxt[arc]

            if arc == -1:
                continue

            removed[e] = 1

            a = x[e]
            b = y[e]
            u = b if a == v else a

            parent[v] = u
            child_cost[v] = 1 if x[e] == u else 0

            degree[v] -= 1
            degree[u] -= 1

            if degree[u] == 1:
                queue.append(u)

        # After peeling, every surviving vertex must have degree 2.
        possible = True
        for v in range(1, V):
            if degree[v] != 0 and degree[v] != 2:
                possible = False
                break

        if not possible:
            out.append("-1 -1")
            continue

        seen = bytearray(V)
        root_cost = array('i', [0]) * V

        answer_cost = 0
        answer_ways = 1

        # Process one connected component at a time.
        for start in range(1, V):
            if head[start] == -1 or seen[start]:
                continue

            stack = [start]
            seen[start] = 1
            vertices = array('i')

            base = 0
            cycle_start = -1

            while stack:
                v = stack.pop()
                vertices.append(v)

                base += child_cost[v]
                if degree[v] > 0:
                    cycle_start = v

                arc = head[v]
                while arc != -1:
                    u = to[arc]
                    if not seen[u]:
                        seen[u] = 1
                        stack.append(u)
                    arc = nxt[arc]

            if cycle_start == -1:
                # The component is a tree.
                root = -1
                for v in vertices:
                    if parent[v] == -1:
                        root = v
                        break

                root_cost[root] = base

                best = base
                ways = 1

                stack = [root]

                while stack:
                    v = stack.pop()
                    cv = root_cost[v]

                    if cv < best:
                        best = cv
                        ways = 1
                    elif cv == best and v != root:
                        ways += 1

                    arc = head[v]
                    while arc != -1:
                        u = to[arc]
                        e = arc >> 1

                        # In a peeled tree, parent[u] == v means u
                        # is a child of v.
                        if parent[u] == v:
                            delta = (1 if x[e] == u else 0) - \
                                    (1 if x[e] == v else 0)
                            root_cost[u] = cv + delta
                            stack.append(u)

                        arc = nxt[arc]

                answer_cost += best
                answer_ways = answer_ways * ways % MOD

            else:
                # The component is unicyclic.
                # Find the remaining cycle.
                cycle_vertices = [cycle_start]
                cycle_edges = []

                cur = cycle_start
                prev_edge = -1

                while True:
                    arc = head[cur]
                    chosen = -1

                    while arc != -1:
                        e = arc >> 1
                        if not removed[e] and e != prev_edge:
                            chosen = e
                            break
                        arc = nxt[arc]

                    if chosen == -1:
                        break

                    cycle_edges.append(chosen)

                    a = x[chosen]
                    b = y[chosen]
                    nxt_vertex = b if a == cur else a

                    if nxt_vertex == cycle_start:
                        break

                    cycle_vertices.append(nxt_vertex)
                    prev_edge = chosen
                    cur = nxt_vertex

                k = len(cycle_vertices)

                if k == 1:
                    # The only possible cycle is a self-loop.
                    cycle_cost = 0
                    cycle_ways = 1
                else:
                    clockwise = 0
                    counterclockwise = 0

                    for i in range(k):
                        u = cycle_vertices[i]
                        v = cycle_vertices[(i + 1) % k]
                        e = cycle_edges[i]

                        # Clockwise wants u -> v, so v is visible.
                        if x[e] == u:
                            clockwise += 1

                        # Counterclockwise wants v -> u, so u is visible.
                        if x[e] == v:
                            counterclockwise += 1

                    if clockwise < counterclockwise:
                        cycle_cost = clockwise
                        cycle_ways = 1
                    elif clockwise > counterclockwise:
                        cycle_cost = counterclockwise
                        cycle_ways = 1
                    else:
                        cycle_cost = clockwise
                        cycle_ways = 2

                answer_cost += base + cycle_cost
                answer_ways = answer_ways * cycle_ways % MOD

        out.append(f"{answer_cost} {answer_ways}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The adjacency structure uses a forward-star representation rather than a Python list of lists. This matters because there can be (2n) endpoint incidences and the memory limit is only 128 MB. The `array('i')` containers keep vertex and edge indices compact, while `bytearray` is enough for Boolean state such as removed edges and visited vertices.

The edge index is recovered from an adjacency index with `arc >> 1`. Every card contributes two consecutive adjacency records, so no separate edge-id array is needed.

During peeling, `parent[v]` records the unique neighbor that survives when (v) is removed. The corresponding `child_cost[v]` records whether that edge has to be flipped when oriented from the surviving vertex toward (v). Summing these values gives the cost of the forced tree orientation.

The tree rerooting uses the relation

[
cost[u]-cost[v]=[x_e=u]-[x_e=v].
]

The implementation stores the current root cost in `root_cost`, so the DFS stack contains only vertex indices rather than large tuples. This keeps the memory usage small even for a path with (10^5) vertices.

The cycle traversal deliberately checks `e != prev_edge`. Without this condition, the traversal would immediately walk back along the edge it just used. A self-loop is handled separately because both cycle directions represent exactly the same visible number and hence the same flip set.

All arithmetic involving the number of ways is reduced modulo (998244353). Flip counts are at most (n), so ordinary Python integers are more than sufficient and there is no overflow issue.

## Worked Examples

For Sample 1, the graph consists of two independent tree components.

The first component contains cards ((1,2)) and ((1,3)). Its peeling process eventually chooses one vertex as the root. The relevant rerooting states are:

| Root | Edge (1-2) cost | Edge (1-3) cost | Total |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 2 |
| 2 | 0 | 1 | 1 |
| 3 | 1 | 0 | 1 |

Thus its minimum is 1 and there are 2 optimal roots.

The second component has exactly the same shape, with vertices (4,5,6), so its minimum is also 1 with 2 optimal roots.

The components are independent, giving a total minimum of (1+1=2), and (2\cdot2=4) minimum flip sets.

| Component | Base tree cost | Minimum cycle cost | Local minimum | Local ways |
| --- | --- | --- | --- | --- |
| (1,2,3) | 1 | 0 | 1 | 2 |
| (4,5,6) | 1 | 0 | 1 | 2 |
| Total | 2 | 0 | 2 | 4 |

So the output is `2 4`, matching the sample.

For Sample 2, the two cards are both self-loops at vertex 1. Each loop contributes degree two, so vertex 1 has degree four. No leaf can be removed, and the remaining degree is neither zero nor two.

| Vertex | Initial degree | After peeling | Valid core degree? |
| --- | --- | --- | --- |
| 1 | 4 | 4 | No |

The component contains two edges but only one vertex. Its total indegree would have to be two, while the single vertex can accept at most one. The algorithm rejects the test case and prints `-1 -1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each card contributes two adjacency records, and peeling, component traversal, rerooting, and cycle traversal each inspect every record only a constant number of times. |
| Space | (O(n)) | There are (O(n)) vertices relevant to the graph and (O(n)) edges, stored in compact arrays. |

The largest test case has (n=10^5), and the total across all test cases is (10^6). The algorithm performs a constant number of linear graph passes, so the total work is (O(\sum n)). The compact adjacency representation also keeps memory proportional to (n), which is suitable for the 128 MB limit.

## Test Cases

```python
import sys
import io
from array import array

MOD = 998244353
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        V = 2 * n + 1

        head = array('i', [-1]) * V
        to = array('i', [0]) * (2 * n)
        nxt = array('i', [0]) * (2 * n)
        x = array('i', [0]) * n
        y = array('i', [0]) * n
        degree = array('i', [0]) * V

        for i in range(n):
            a, b = map(int, input().split())
            x[i] = a
            y[i] = b

            p = 2 * i
            to[p] = b
            nxt[p] = head[a]
            head[a] = p

            to[p + 1] = a
            nxt[p + 1] = head[b]
            head[b] = p + 1

            if a == b:
                degree[a] += 2
            else:
                degree[a] += 1
                degree[b] += 1

        parent = array('i', [-1]) * V
        child_cost = bytearray(V)
        removed = bytearray(n)

        queue = []
        for v in range(1, V):
            if head[v] != -1 and degree[v] == 1:
                queue.append(v)

        q = 0
        while q < len(queue):
            v = queue[q]
            q += 1

            if degree[v] != 1:
                continue

            arc = head[v]
            while arc != -1:
                e = arc >> 1
                if not removed[e]:
                    break
                arc = nxt[arc]

            if arc == -1:
                continue

            removed[e] = 1

            a = x[e]
            b = y[e]
            u = b if a == v else a

            parent[v] = u
            child_cost[v] = 1 if x[e] == u else 0

            degree[v] -= 1
            degree[u] -= 1

            if degree[u] == 1:
                queue.append(u)

        if any(degree[v] not in (0, 2) for v in range(1, V)):
            out.append("-1 -1")
            continue

        seen = bytearray(V)
        root_cost = array('i', [0]) * V

        total_cost = 0
        total_ways = 1

        for start in range(1, V):
            if head[start] == -1 or seen[start]:
                continue

            stack = [start]
            seen[start] = 1
            vertices = []
            base = 0
            cycle_start = -1

            while stack:
                v = stack.pop()
                vertices.append(v)
                base += child_cost[v]

                if degree[v] > 0:
                    cycle_start = v

                arc = head[v]
                while arc != -1:
                    u = to[arc]
                    if not seen[u]:
                        seen[u] = 1
                        stack.append(u)
                    arc = nxt[arc]

            if cycle_start == -1:
                root = next(v for v in vertices if parent[v] == -1)

                root_cost[root] = base
                best = base
                ways = 0

                stack = [root]
                while stack:
                    v = stack.pop()
                    cv = root_cost[v]

                    if cv < best:
                        best = cv
                        ways = 1
                    elif cv == best:
                        ways += 1

                    arc = head[v]
                    while arc != -1:
                        u = to[arc]
                        e = arc >> 1

                        if parent[u] == v:
                            delta = (x[e] == u) - (x[e] == v)
                            root_cost[u] = cv + delta
                            stack.append(u)

                        arc = nxt[arc]

                total_cost += best
                total_ways = total_ways * ways % MOD

            else:
                cv = [cycle_start]
                ce = []

                cur = cycle_start
                prev = -1

                while True:
                    arc = head[cur]
                    e = -1

                    while arc != -1:
                        z = arc >> 1
                        if not removed[z] and z != prev:
                            e = z
                            break
                        arc = nxt[arc]

                    if e == -1:
                        break

                    ce.append(e)

                    a = x[e]
                    b = y[e]
                    nxt_v = b if a == cur else a

                    if nxt_v == cycle_start:
                        break

                    cv.append(nxt_v)
                    prev = e
                    cur = nxt_v

                k = len(cv)

                if k == 1:
                    cycle_cost = 0
                    ways = 1
                else:
                    a = 0
                    b = 0

                    for i in range(k):
                        u = cv[i]
                        v = cv[(i + 1) % k]
                        e = ce[i]

                        if x[e] == u:
                            a += 1
                        if x[e] == v:
                            b += 1

                    if a < b:
                        cycle_cost = a
                        ways = 1
                    elif b < a:
                        cycle_cost = b
                        ways = 1
                    else:
                        cycle_cost = a
                        ways = 2

                total_cost += base + cycle_cost
                total_ways = total_ways * ways % MOD

        out.append(f"{total_cost} {total_ways}")

    return "\n".join(out)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline
        sys.stdout = io.StringIO()

        ans = solve()
        if ans is None:
            ans = sys.stdout.getvalue()

        return ans.strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

sample = """\
3
4
1 2
1 3
4 5
4 6
2
1 1
1 1
3
1 2
3 4
5 6
"""

assert run(sample) == "2 4\n-1 -1\n0 1", "provided samples"

assert run("""\
1
1
1 2
""") == "0 1", "minimum-size ordinary card"

assert run("""\
1
1
1 1
""") == "0 1", "minimum-size self-loop"

assert run("""\
1
2
1 2
1 3
""") == "1 2", "tree with two optimal roots"

assert run("""\
1
2
1 1
1 1
""") == "-1 -1", "all-equal values are impossible"

assert run("""\
1
2
1 4
2 3
""") == "0 1", "maximum endpoint value 2n"

# Maximum-size linear case.
n = 100000
lines = ["1", str(n)]
for i in range(1, n + 1):
    lines.append(f"{i} {i + 1}")

assert run("\n".join(lines) + "\n") == "0 1", "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1 2` | `0 1` | Minimum ordinary case and no unnecessary flip |
| `1 / 1 / 1 1` | `0 1` | Self-loop handling |
| `1 / 2 / 1 2 / 1 3` | `1 2` | Tree rerooting and counting multiple optimal roots |
| `1 / 2 / 1 1 / 1 1` | `-1 -1` | Impossible component with too many edges for its vertices |
| `1 / 2 / 1 4 / 2 3` | `0 1` | Boundary value (2n) and already valid orientation |
| Path of (100000) cards | `0 1` | Maximum-size input and linear complexity |

## Edge Cases

A self-loop such as

```
1
1
1 1
```

has degree two in the graph, because one loop contributes two to the degree. It is not removed during leaf peeling, so it is recognized as a one-vertex cycle. The cycle handler treats this case separately and assigns zero flip cost and one orientation. The output is `0 1`.

For an impossible all-equal component such as

```
1
2
1 1
1 1
```

vertex 1 has degree four. No leaf is available, and the remaining degree is not two. The algorithm rejects the component before attempting any orientation calculation, producing `-1 -1`.

For the tree

```
1
2
1 2
1 3
```

the peeled leaves are 2 and 3, with 1 as the last surviving root. The base orientation rooted at 1 requires two flips. Rerooting at 2 changes the cost by (-1), giving cost 1. Rerooting at 3 also gives cost 1. Both roots attain the optimum, so the component contributes `1 2`.

For the cycle

```
1
3
1 2
2 3
1 3
```

there are no tree edges to peel. The remaining cycle can be oriented in two directions. One direction flips one card and the other direction also flips one card. Since the two orientations reverse every cycle edge in opposite ways, they correspond to different flip sets, so the component contributes `1 2`.

For an already valid input such as

```
1
3
1 2
3 4
5 6
```

every component is a single edge whose initial orientation can already satisfy the unique-number condition. Each tree has an optimal root at the endpoint opposite the initially selected direction, giving zero flips. There is exactly one minimum flip set, the empty set, so the result is `0 1`.
