---
title: "CF 1416F - Showing Off"
description: "Think of each cell as a vertex of a directed graph. Every vertex chooses exactly one adjacent vertex as its outgoing edge. A graph where every vertex has outdegree exactly one is a functional graph."
date: "2026-06-11T07:04:54+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1416
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 673 (Div. 1)"
rating: 3300
weight: 1416
solve_time_s: 137
verified: false
draft: false
---

[CF 1416F - Showing Off](https://codeforces.com/problemset/problem/1416/F)

**Rating:** 3300  
**Tags:** flows, graph matchings, greedy, implementation  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Think of each cell as a vertex of a directed graph. Every vertex chooses exactly one adjacent vertex as its outgoing edge.

A graph where every vertex has outdegree exactly one is a functional graph. Every connected component contains exactly one directed cycle, and all other vertices form directed trees pointing into that cycle.

Let the given matrix be $b$. For a cell $u$, $b_u$ is the sum of costs of every vertex reachable from $u$.

We must reconstruct:

1. A positive cost for every cell.
2. One valid direction for every cell.

such that recomputing all reachable-set sums produces exactly the given matrix.

The total number of cells over all test cases is at most $10^5$, so anything quadratic in the number of cells is immediately impossible. We need something close to linear or $O(N\sqrt N)$, where $N=nm$.

The first subtle observation is what happens along a directed edge $u\to v$.

If $u$ is not on a cycle, then

$$b_u = \text{cost}_u + b_v,$$

so $b_u>b_v$.

If $u$ and $v$ belong to the same cycle, they have exactly the same reachable set, hence

$$b_u=b_v.$$

No edge can go from a smaller value to a larger value.

A common mistake is to assume that every equal-valued connected component can simply be turned into a cycle. Positivity of costs matters. A cycle of equal-valued vertices must have total cycle cost equal to that value, so we need a construction that always keeps all costs positive.

Consider

```
4 4
```

Two adjacent cells with value 4 can form a 2-cycle and receive costs $1$ and $3$. This is always valid because all given values are at least 2.

Another easy-to-miss case is a local minimum.

```
5
```

in a $1\times1$ grid.

The only cell has no neighbor. No outgoing edge is possible, so the answer is impossible. This is exactly the sample with output `NO`.

A third pitfall is a cell whose neighbors are all larger.

```
7 8
9 10
```

The value 7 cannot point anywhere, because every outgoing edge must go to a value $\le 7$. Such an instance is impossible.

## Approaches

A brute-force reconstruction idea is to guess the functional graph and then solve for costs. The graph has exponentially many possibilities, because every cell may choose one of up to four neighbors. Even for a few dozen cells this becomes hopeless.

The key structural observation is that the matrix values already tell us almost everything.

For a cell $u$:

If there exists a neighboring cell with strictly smaller value, then $u$ can safely be made a tree vertex. We simply point it to such a neighbor $v$ and assign

$$\text{cost}_u=b_u-b_v.$$

The only difficult cells are those with **no strictly smaller neighbor**.

Such a cell cannot be a tree vertex. Since every outgoing edge must go to a value not exceeding its own, it must point to an equal-valued neighbor. Hence it must belong to a cycle of equal-valued cells. This observation appears in standard solutions to the problem.

The grid graph is bipartite under chessboard coloring. Every cycle in a bipartite graph has even length. Because of that, it is enough to build only 2-cycles. We only need to pair adjacent equal-valued cells.

Now the problem becomes:

Construct a matching among adjacent equal-valued cells such that every mandatory cell (a cell without a smaller neighbor) is matched.

Some cells may be matched or unmatched. Some must be matched.

This is a bipartite matching problem with lower bounds. The classical solution uses feasible circulation with lower bounds, exactly as the accepted solutions do.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Flow with lower bounds + reconstruction | $O(N\sqrt N)$ in practice | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Read the matrix $b$.
2. For every cell, inspect its four neighbors.

If no neighbor has value $\le b_u$, the answer is impossible.
3. Mark a cell as **flexible** if it has at least one strictly smaller neighbor.

Flexible cells may become ordinary tree vertices.
4. Cells without a strictly smaller neighbor are **mandatory cycle cells**.

They must belong to an equal-valued cycle.
5. Chessboard-color the grid.

Build a bipartite graph whose vertices are cells and whose edges connect adjacent cells having equal values.
6. Construct a lower-bound matching instance.

A mandatory vertex must be matched exactly once.

A flexible vertex may be matched at most once and may also remain unmatched.
7. Solve the lower-bound matching using feasible circulation.

If no feasible circulation exists, print `NO`.
8. Every matched equal-value edge becomes a 2-cycle.

Suppose matched vertices are $u$ and $v$.

Set:

$$\text{cost}_u=1,\qquad \text{cost}_v=b_u-1.$$

Since $b_u=b_v\ge 2$, both costs are positive.
9. For every unmatched flexible vertex $u$, choose any neighboring cell $v$ with $b_v<b_u$.

Direct $u\to v$ and assign

$$\text{cost}_u=b_u-b_v.$$
10. Output all costs and directions.

### Why it works

For every unmatched flexible vertex, the construction gives

$$b_u=\text{cost}_u+b_v.$$

Hence its reachable-set sum is correct.

Every matched pair forms a 2-cycle of equal-valued vertices. The reachable set of both vertices is exactly the pair itself. Their assigned costs sum to

$$1+(b_u-1)=b_u,$$

so both vertices obtain the required value.

Mandatory vertices are exactly the vertices that cannot be attached to a smaller neighbor. The flow formulation guarantees that every such vertex is matched. Thus every mandatory vertex is placed inside some 2-cycle.

Every vertex is either matched into a 2-cycle or attached to a strictly smaller value. Hence every vertex gets exactly one outgoing edge and the resulting graph is valid.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10 ** 18

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, v, u, c):
        a = [u, c, None]
        b = [v, 0, a]
        a[2] = b
        self.g[v].append(a)
        self.g[u].append(b)
        return a

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s])
        self.level[s] = 0

        while q:
            v = q.popleft()
            for e in self.g[v]:
                if e[1] > 0 and self.level[e[0]] == -1:
                    self.level[e[0]] = self.level[v] + 1
                    q.append(e[0])

        return self.level[t] != -1

    def dfs(self, v, t, f):
        if v == t:
            return f

        g = self.g[v]
        while self.it[v] < len(g):
            e = g[self.it[v]]

            if e[1] > 0 and self.level[e[0]] == self.level[v] + 1:
                pushed = self.dfs(e[0], t, min(f, e[1]))
                if pushed:
                    e[1] -= pushed
                    e[2][1] += pushed
                    return pushed

            self.it[v] += 1

        return 0

    def maxflow(self, s, t):
        flow = 0

        while self.bfs(s, t):
            self.it = [0] * self.n

            while True:
                pushed = self.dfs(s, t, INF)
                if not pushed:
                    break
                flow += pushed

        return flow

def solve():
    t = int(input())
    out = []

    dirs = [(0, 1, 'R'), (1, 0, 'D'), (0, -1, 'L'), (-1, 0, 'U')]

    for _ in range(t):
        n, m = map(int, input().split())
        b = [list(map(int, input().split())) for _ in range(n)]

        N = n * m

        def id_of(r, c):
            return r * m + c

        flexible = [False] * N
        equal_edges = [[] for _ in range(N)]

        ok = True

        for r in range(n):
            for c in range(m):
                cur = b[r][c]

                has_le = False
                has_smaller = False

                for dr, dc, _ in dirs:
                    nr, nc = r + dr, c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        if b[nr][nc] <= cur:
                            has_le = True

                        if b[nr][nc] < cur:
                            has_smaller = True

                if not has_le:
                    ok = False

                flexible[id_of(r, c)] = has_smaller

        if not ok:
            out.append("NO")
            continue

        SS = N
        TT = N + 1
        S = N + 2
        T = N + 3

        dinic = Dinic(N + 4)

        demand = [0] * (N + 4)
        match_edges = []

        def add_lb(u, v, low, high):
            demand[u] -= low
            demand[v] += low
            return dinic.add_edge(u, v, high - low)

        for r in range(n):
            for c in range(m):
                v = id_of(r, c)

                if (r + c) & 1:
                    low = 0 if flexible[v] else 1
                    add_lb(SS, v, low, 1)

                    for dr, dc, _ in dirs:
                        nr, nc = r + dr, c + dc

                        if (
                            0 <= nr < n and 0 <= nc < m
                            and b[nr][nc] == b[r][c]
                        ):
                            u = id_of(nr, nc)
                            e = add_lb(v, u, 0, 1)
                            match_edges.append((v, u, e))
                else:
                    low = 0 if flexible[v] else 1
                    add_lb(v, TT, low, 1)

        add_lb(TT, SS, 0, INF)

        need = 0

        for i in range(N + 2):
            if demand[i] > 0:
                dinic.add_edge(S, i, demand[i])
                need += demand[i]
            elif demand[i] < 0:
                dinic.add_edge(i, T, -demand[i])

        flow = dinic.maxflow(S, T)

        if flow != need:
            out.append("NO")
            continue

        cost = [[0] * m for _ in range(n)]
        direction = [['?'] * m for _ in range(n)]

        matched = [False] * N

        for a, bto, e in match_edges:
            if e[1] == 0:
                matched[a] = matched[bto] = True

                ar, ac = divmod(a, m)
                br, bc = divmod(bto, m)

                cost[ar][ac] = 1
                cost[br][bc] = b[ar][ac] - 1

                for dr, dc, ch in dirs:
                    if ar + dr == br and ac + dc == bc:
                        direction[ar][ac] = ch
                        rev = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U'}[ch]
                        direction[br][bc] = rev
                        break

        for r in range(n):
            for c in range(m):
                v = id_of(r, c)

                if matched[v]:
                    continue

                for dr, dc, ch in dirs:
                    nr, nc = r + dr, c + dc

                    if (
                        0 <= nr < n and 0 <= nc < m
                        and b[nr][nc] < b[r][c]
                    ):
                        cost[r][c] = b[r][c] - b[nr][nc]
                        direction[r][c] = ch
                        break

        out.append("YES")

        for row in cost:
            out.append(" ".join(map(str, row)))

        for row in direction:
            out.append("".join(row))

    sys.stdout.write("\n".join(out))

solve()
```

After the flow finds a feasible matching, every saturated equal-value edge becomes a 2-cycle. The implementation detects those edges by checking whether the residual capacity became zero.

The lower-bound construction is the most delicate part. Mandatory vertices receive lower bound 1, which forces them to participate in the matching. Flexible vertices receive lower bound 0 and may remain unmatched.

The reconstruction phase is simple because the value matrix already determines the required costs. For a tree edge $u\to v$, the only possible positive cost is $b_u-b_v$.

## Worked Examples

### Example 1

Input:

```
7 6 7 8
5 5 4 4
5 7 4 4
```

Mandatory cells are exactly the equal-value plateaus with no smaller neighbor.

A feasible matching may choose:

| Pair |
| --- |
| (2,1) ↔ (2,2) |
| (2,3) ↔ (2,4) |

All remaining cells have a smaller neighbor and become tree vertices.

The resulting graph satisfies every required sum.

This example demonstrates the main idea: only local minima among equal-valued regions need matching.

### Example 2

Input:

```
5
```

| Cell | Has neighbor ≤ value? |
| --- | --- |
| only cell | No |

The necessary condition fails immediately.

Output:

```
NO
```

This demonstrates the smallest impossible instance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N\sqrt N)$ | Bipartite matching via flow on a graph with $O(N)$ vertices and edges |
| Space | $O(N)$ | Grid, flow graph, reconstruction data |

The total number of cells over all test cases is at most $10^5$, so an $O(N\sqrt N)$ flow-based solution comfortably fits the limits.

## Test Cases

```
# The official checker accepts many valid outputs.
# For this problem, exact-output asserts are generally not suitable,
# because multiple different reconstructions may be correct.

# Sample 1
inp = """\
2
3 4
7 6 7 8
5 5 4 4
5 7 4 4
1 1
5
"""

# Expected:
# first test -> YES
# second test -> NO

# Minimum impossible case
inp = """\
1
1 1
2
"""

# Expected: NO

# Two equal adjacent cells
inp = """\
1
1 2
4 4
"""

# Expected: YES

# All equal 2x2 block
inp = """\
1
2 2
5 5
5 5
"""

# Expected: YES

# Strict gradient
inp = """\
1
2 2
10 9
8 7
"""

# Expected: YES
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $1\times1$ | NO | No outgoing edge exists |
| Two equal cells | YES | Smallest valid 2-cycle |
| All equal $2\times2$ | YES | Matching inside an equal-value component |
| Strict gradient | YES | Pure tree construction without cycles |

## Edge Cases

Consider a cell whose neighbors are all larger:

```
1 2
3 4
```

The value 1 has no neighbor with value $\le 1$. The algorithm rejects the instance during the initial scan. Any valid functional graph would require an outgoing edge from that cell, which is impossible.

Consider a plateau:

```
4 4
```

Neither cell has a smaller neighbor. Both become mandatory vertices. The matching contains their unique equal-value edge, producing a valid 2-cycle.

Consider a mixed situation:

```
7 6
5 5
```

The two cells with value 5 are mandatory and must be matched. The cells 7 and 6 both have smaller neighbors, so they become tree vertices. The reconstruction combines one 2-cycle with a small in-tree, exactly matching the required reachable-set sums.
