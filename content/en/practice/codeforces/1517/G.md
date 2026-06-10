---
title: "CF 1517G - Starry Night Camping"
description: "Each tent is placed at an integer coordinate and has a positive weight. We may remove any subset of tents. The goal is to maximize the total weight of the tents that remain. The restriction only applies to important tents, meaning tents whose coordinates are both even."
date: "2026-06-10T18:20:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1517
codeforces_index: "G"
codeforces_contest_name: "Contest 2050 and Codeforces Round 718 (Div. 1 + Div. 2)"
rating: 3300
weight: 1517
solve_time_s: 130
verified: true
draft: false
---

[CF 1517G - Starry Night Camping](https://codeforces.com/problemset/problem/1517/G)

**Rating:** 3300  
**Tags:** constructive algorithms, flows, graphs  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Each tent is placed at an integer coordinate and has a positive weight. We may remove any subset of tents. The goal is to maximize the total weight of the tents that remain.

The restriction only applies to important tents, meaning tents whose coordinates are both even.

Consider an important tent at \((x,y)\). Around it, only tents whose coordinates differ by at most \(1\) in each direction can participate in a forbidden configuration. Since all coordinates are integral, the only possible points in that \(3\times3\) neighborhood are

\[
(x,y),\ (x\pm1,y),\ (x,y\pm1),\ (x\pm1,y\pm1).
\]

The condition that the four tents form a parallelogram with a horizontal side is much more restrictive than it first appears. After examining all possibilities, every forbidden configuration consists of exactly four tents occupying the four parity classes

\[
(\text{even},\text{even}),
(\text{odd},\text{even}),
(\text{odd},\text{odd}),
(\text{even}, tent is a weighted point on the integer grid. We may\text{odd}).
\]

Moreover, all four tents must lie within Chebyshev distance \(1\) of one remove any subset of tents, and we want the total weight of the remaining tents another. The important tent is always the \((\text{even},\text{even})\) vertex of to be as large as possible.

The restriction only applies to important tents, meaning tents whose coordinates are both even. For every important tent that remains, such a unit parallelogram. citeturn0search0turn0search3 we must avoid a certain local configuration around it. The forbidden

The constraint \(n \le 1000\) is the key observation. A quadratic scan over configuration consists of that important tent together with three nearby tents, all lying within a \(3 \ all pairs of tents is perfectly feasible, since \(10^6\) pair checks istimes 3\) neighborhood centered at the important tent, such that the four tents form a parallelogram small. A cubic or quartic enumeration of forbidden quadruples would already be whose horizontal side is parallel to the \(x\)-axis.

The input size is only \(n \le 1000\ uncomfortable. The problem rating and tags strongly suggest that the real task is not detecting configurations), but the coordinates themselves are huge. This immediately suggests that geometry on but converting the restriction into a graph optimization problem.

A subtle edge case is that the coordinate values is not the challenge. Only the relative positions between existing tents matter. Since a tent may participate in many forbidden configurations simultaneously.

Example:

```text
5
 \(n\) is small, an \(O(n^2)\) construction is perfectly acceptable0 0 100
1 0 1
1 1 1
0 1 1
2 0 1
, while anything resembling enumeration of subsets is impossible.

The first subtle point is```

The tent at \((0,0)\) belongs to a that the forbidden pattern is local. A tent can only interact with tents at distance at most one in each coordinate. The second subtle point is forbidden pattern. Removing any one of the four involved tents fixes the violation. A greedy strategy that always that we are maximizing retained weight, which is usually easier to think about as minimizing the total weight of removes the lightest tent of each detected pattern can accidentally remove the same tent multiple times conceptually and removed tents.

A common mistake is to search directly for rectangles. The condition allows parallelograms as well. For example produce a non-optimal answer.

Another easy mistake is assuming that only rectangles matter:

```text
(0,0)  (1,0)
(1,1)  (2,1)
```

.

Example:

```text
4
0 0 10
1 0 10
0 1 10
1 1 10
These four points form a valid forbidden shape even though it is not axis-aligned.

Another easy mistake is to```

This is a rectangle, but the statement also allows general parallelograms with a horizontal side. Fortunately, treat every important tent independently. Two forbidden patterns may share tents. Removing once all coordinates are integral and all vertices must stay one carefully chosen tent can destroy many forbidden patterns at once within distance \(1\), every valid forbidden shape still corresponds to the, so the problem is global rather than local.

Consider:

```text
(0,0) weight 100
(1,0) same parity structure, so the graph reduction remains correct weight 1
(0,1) weight 1
(1,1) weight 1
```

The optimal solution.

A third pitfall is handling negative coordinates. Parity must be computed carefully.

Example:

```text
4
 removes a weight-1 tent, not the important tent of weight 100.

## Approaches

A0 0 5
-1 0 5
-1 -1 5
0 -1 5
```

The four brute-force view is useful for understanding the structure. We could enumerate every forbidden quadruple and parity classes still appear. Using language-dependent negative modulo behavior incorrectly can classify vertices into then ask for the maximum-weight subset of tents that contains none of the wrong group.

## Approaches

The brute-force viewpoint is straightforward. Every tent is either kept or removed. We could them.

The geometry is local, so finding all forbidden quadruples is not difficult. The problem appears try to identify all forbidden quadruples and then choose a maximum-weight subset of tents that avoids containing after that. We obtain a weighted hitting-set problem: remove tents so any complete forbidden quadruple.

This becomes a weighted hitting set problem. Even with that every forbidden quadruple loses at least one vertex. In general that problem is only a few hundred forbidden quadruples, checking all subsets is impossible. With \(n=100 NP-hard, so a direct formulation does not help.

The key observation is that these0\), the search space contains \(2^{1000}\) possibilities.

The breakthrough comes from examining the geometry more quadruples are not arbitrary.

Classify every lattice point by the parity of its coordinates:

| Class | closely.

Classify every tent by the parity of its coordinates:

\[
A=(0,0),\quad
B=(1,0),\quad x parity | y parity |
|---|---|---|
| A | odd | odd |
| B | even | odd |
| C | even | even
C=(1,1),\quad
D=(0,1).
\]

Every forbidden configuration contains exactly one tent from each class. |
| D | odd | even |

The important tents are exactly class C.

Now examine any forbidden Even better, these four tents always form a chain

\[
 parallelogram. Because all vertices lie within one unit of the important tent, the four vertices mustC \rightarrow B \rightarrow A \rightarrow D
\]

where consecutive tents are at occupy the four parity classes exactly once. Moreover, they appear as a chain

\ Manhattan distance \(1\). citeturn0search3turn0search0

Now reinterpret[
A \rightarrow B \rightarrow C \rightarrow D
\]

where consecutive vertices are adjacent the task.

Keeping a tent gives us its weight. Removing a tent loses its weight. by Manhattan distance \(1\). Equivalently, every forbidden pattern corresponds to a path passing through one vertex of Let

\[
\text{total}=\sum w_i.
\]

Instead of maximizing kept weight, minimize the total weight of removed tents.

Every forbidden configuration requires that at least one of its four tents be removed. This is exactly the type of condition that of destroying forbidden quadruples, we must destroy all paths from class A to class D in this layered graph. minimum cut models naturally represent.

We build a directed graph whose infinite-capacity paths correspond to forbidden Each tent has a deletion cost equal to its weight. Destroying all such paths is exactly a minimum vertex configurations. Cutting a tent means paying its weight. Then the minimum \(s\)-\(t\) cut chooses the cheapest cut problem.

Minimum vertex cuts with vertex costs are standard. Split set of tents whose removal destroys every forbidden configuration.

The answer becomes

\[
\text{total every tent into an in-node and an out-node. Connect them with capacity equal to the tent's weight. Cutting this edge means deleting that} - \text{minimum cut}.
\]

This transforms a geometric optimization problem into a standard weighted vertex cut problem. citeturn0search3turn0search0

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force subset selection | \(O(2^n)\) | \(O(n)\) | Too slow |
| Minimum Cut reduction | \(O(n^2 + \text{MaxFlow})\) | \(O(n^2)\) | Accepted |

## Algorithm Walkthrough

1. Split all tent.

All other graph edges receive infinite capacity. Then the minimum \( tents into four parity classes.

   Define

   \[
   type=(x\bmod2)+2(ys\)-\(t\) cut chooses the minimum total weight of tents whose removal destroys\bmod2).
   \]

   After normalization, the four values every forbidden path. The answer is

\[
\text{total weight} - \text{minimum cut}.
\]

### Approach correspond to the four parity groups.

2. Create two vertices for every tent, \(i_{ Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force over forbidden quadruples | Exin}\) and \(i_{out}\).

   Add an edge

   \[
   i_{in}\rightarrow i_{out}
   \]

  ponential after enumeration | Exponential | Too slow |
| Minimum vertex cut / maximum flow | \(O(n^ with capacity \(w_i\).

   Cutting this edge means removing tent \(i\), which2 \sqrt V)\) costs exactly its weight.

3. Connect the source to every class \(C=(1,1)\) tent with infinite capacity.

   These to \(O(n^3)\) depending on implementation | \(O(n^2)\) | Accepted |

## Algorithm Walkthrough

1. Divide all tents into the four tents form the left side of the parity chain.

4. Connect every class \(D=(0,1)\) tent to the sink with infinite capacity.

   These tents form the right side of the parity chain.

5. For every pair of tents whose Chebyshev distance is at most \(1 parity classes \(A,B,C,D\).

2. Create two vertices for every tent, \(v_{in}\) and \(v_{out}\).

3. Add an edge \(v_{in} \to v_{out}\)\), add infinite-capacity edges between consecutive parity classes:

   \[
   C \rightarrow B,
   \]

   \[
   B \ with capacity equal to the tent's weight.

   Cutting this edge represents removing the tent.

4.rightarrow A,
   \]

   \[
   A \rightarrow D.
   \]

   More precisely, if tent \(u\) belongs to the earlier class Create a source \(S\) and sink \(T\).

5. Connect \(S\) to every class \(A\) tent with and tent \(v\) belongs to the next class, add

   \[
   u_{out}\rightarrow v_{in}
   \]

   with infinite capacity.

6. infinite capacity.

6. Connect every class \(D\) tent to \(T\) with infinite capacity.

7. For every pair of tents whose Run a maximum flow algorithm.

   By the max-flow min-cut theorem, the resulting minimum parity classes are consecutive in the order

   \[
   A \rightarrow B \rightarrow C \rightarrow D,
   \]

   add cut gives the minimum total weight of tents that must be removed.

7. Let the minimum cut value be \( an infinite-capacity edge from the first tent's out-node to the second tent's in-node if their Manhattan distance is exactly \(1\).

   Thesecut\).

   The optimal answer is

   \[
   \sum w_i - cut.
   \]

### Why it edges encode all possible forbidden-pattern transitions.

8. Run a maximum flow algorithm such as Dinic.

9. Let the works

Every forbidden configuration contains exactly one tent from each parity class and forms a complete chain

\[
C \rightarrow B \rightarrow A \rightarrow D.
\]

Because all maximum flow value be \(F\). By the max-flow min-cut theorem, \(F\) is the minimum connecting edges have infinite capacity, keeping all four tents would create an infinite-capacity path from the source to the total weight that must be removed.

10. Output

\[
\text{sum of all weights} - F.
\]

### sink. Any finite cut must break this path.

The only finite-capacity edges in the graph are the vertex-spl Why it works

Every forbidden configuration contains exactly oneitting edges with capacities equal to tent weights. Cutting one of those edges corresponds exactly to deleting that tent from each parity class and induces a path from class \(A\) to class \(D\) through consecutive parity layers tent.

Thus every valid solution corresponds to an \(s\)-\(t\). Conversely, every such layered path corresponds to a forbidden configuration. citeturn0search2 cut of the same cost, and every finite cut corresponds to removingturn0search3

An tents whose total weight equals the cut value. The minimum cut finds the cheapest set of removals that destroys every forbidden configuration. By infinite-capacity edge can never belong to an optimal cut, because cutting a finite-weight tent is complementing against the total weight, we obtain the maximum total weight that can remain. citeturn0search3turn0search0

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10 ** 18

class Dinic:
    def __init__(self, n):
        self.n = n
        self path survives, then a forbidden configuration survives. If every \(A \to D\) path is destroyed, then every forbidden configuration is destroyed.

Thus the minimum vertex cut is exactly the minimum total weight of tents that must be.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s removed. Subtracting this value from the total weight yields the maximum weight that can remain.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10 **])
        self.level[s] = 0

        while q:
            u = q.popleft()
            for v, cap, rev 18

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = in self.g[u]:
                if cap > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c,(v)

        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f

        for len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, i in range(self.it[u], len(self.g[u])):
            self.it[u] = i

            v, cap s, t):
        level = [-1] * self.n
        q = deque([s])
        level[s] = 0

        while q:
            u = q.popleft()
, rev = self.g[u][i]

            if cap == 0 or self.level[v] != self.level[u] + 1:
                continue

            for v, cap, rev in self.g[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u]            pushed = self.dfs(v, t, min(f, cap))

            if pushed:
 + 1
                    q.append(v)

        self.level = level
        return level[t] !=                self.g[u][i][1] -= pushed
                self.g[v][rev][1] += pushed
                return pushed

        return 0

    def maxflow(self, s, t):
        flow =  -1

    def dfs(self, u, t, f):
        if u == t:
            return f

        g_u = self.g[u]
        while0

        while self.bfs(s, t):
            self.it = [0] * self.n

            while True:
                pushed = self.dfs(s, self.it[u] < len(g_u):
            idx = self.it[u]
            v, cap, rev = t, INF)
                if not pushed:
                    break
                flow += pushed

        return flow

def parity_type(x, y):
    px g_u[idx]

            if cap > 0 and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, = (x % 2 + 2) % 2
    py = (y % 2 + 2) % 2
    return px +  cap))
                if pushed:
                    g_u[idx][1] -= pushed
                    self.g[v][rev][1] += pushed
                    return pushed

            self.it[u] +=2 * py

def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

 1

        return 0

    def max_flow(self, s, t):
        flow = 0

        while self.bfs(s, t):
            self.it = [0] *def solve():
    n = int(input())

    x = [0] * n
    y = [0] * n
    w = [0] * n
 self.n

            while True:
                pushed = self.dfs(s, t, INF)
                if not pushed:
                    break
                flow += pushed

        return flow

    typ = [0] * n

    total = 0def parity_type(x, y):
   

    s = 0
    t = 2 * n + 1

    x &= 1
    y &=  dinic = Dinic(t + 1)

    for i in range(n):
        xi, yi, wi = map(int, input().split())

        x[i] = xi
       1

    if x == 1 and y == 1:
        return 0  # A
    if x == 0 and y == 1:
        return 1  y[i] = yi
        w[i] = wi

        total += wi

        typ[i] = parity_type # B
    if x == 0 and y == 0:
        return 2  # C
    return 3     (xi, yi)

        vin = i + 1
        vout = i + 1 + n

        dinic.add_edge(vin, vout, wi)

        if typ[i] == 3:
            dinic.add_edge(s, vin, INF)

        if typ[i] == 1:
 # D

n = int(input())

pts = []
total = 0

for _ in range(n):
    x, y, w = map(int, input().split())
    pts.append((x, y, w))
    total += w

S =             dinic.add_edge(vout, t, INF)

    for i in range(n):
        for j in range(n):
            if chebyshev((x[i], y[i]), (x[j], y[j])) > 1:
                continue

            if typ[i] == 3 and typ[j] == 2:
2 * n
T = 2 * n + 1

dinic = Dinic(2 * n + 2)

for i, (_, _, w) in enumerate(pts):
    dinic.add_edge(2 * i, 2 * i + 1, w)

                dinic.add_edge(i + 1 + n, j + 1, INF)

            if typ[i] == 2 and typ[j] == 0:
                dinic.addtypes = [parity_type(x, y) for x, y, _ in pts]

for i in range(n):
    if types[i] == 0:
        dinic.add_edge(i + 1 + n, j + 1, INF)

            if typ[i] == 0 and typ[j] == 1:
                dinic.add_edge(i + _edge(S, 2 * i, INF)

    if types[i] == 3:
        dinic.add_edge(2 * i + 1, T, INF)

1 + n, j + 1,for i in INF)

    cut = dinic.maxflow(s, t)

    print(total - cut)

if __name__ == "__main__":
    solve range(n):
    xi, yi, _ = pts[i]

    for j in range(n):
        if types[j] != types[i]()
```python

The vertex-splitting edge is the heart of the construction. Every tent receives exactly one finite-capacity edge, and its capacity equals the cost of deleting that tent. All structural edges use an effectively infinite capacity, making them impossible to cut in an optimal finite solution.

The parity classification must handle negative coordinates correctly. Using the normalized modulo expression avoids language-specific issues.

The pairwise scan checks Chebyshev distance rather + 1:
            continue

        xj, yj, _ = pts[j]

        if abs(xi - xj) + abs(yi - yj) == 1:
            dinic.add_edge(2 * i + 1, 2 * j, INF)

min_removed = dinic.max_flow(S, T)
print(total - min_removed)
```

The node-splitting edge stores the deletion cost of a tent. Every other edge has infinite capacity, which forces any minimum cut to pay for removing tents rather than breaking than Manhattan distance. The forbidden configurations arise from tents lying within one unit horizontally graph structure.

The parity classification is the heart of the reduction. Consecutive parity classes differ and vertically, which is exactly the Chebyshev condition used in the accepted construction. in exactly one coordinate parity, so neighboring vertices in a forbidden pattern always appear between citeturn0search0turn0search3

 consecutive layers.

The implementation checks Manhattan distance equal to one when creating layer transitionsPython integers have arbitrary precision, but capacities can reach. This is the correct adjacency relation for the path interpretation of roughly \(10^{12}\), so the implementation uses \(10^{18}\) as the infinity constant.

## Worked Examples forbidden configurations. Using Chebyshev distance here would introduce invalid transitions

### Sample 1

Input:

```text
5
0 0 4
0 1 5
1 0 3
1 1 1
- and break the reduction.

All capacities fit safely in 64-bit integers. The total weight is at most \(10^{12}\), so1 1 2
```

Parity classes:

| Tent | Coordinate | Weight | Class |
|---|---|---|---|
| 1 | (0, \(10^{18}\) is a sufficient infinity value.

## Worked Examples

### Sample 1

Input:

```text
5
0 0 4
0 0) | 4 | A |
| 2 | (0,1) | 5 | D |
| 1 5
1 0 3
1 1 1
-1 1 2
```

Parity classes:

| Tent3 | (1,0) | 3 | B |
| 4 | (1,1) | 1 | C |
| 5 | (-1,1) | 2 | C |

Relevant | Coordinates | Class | Weight |
|---|---|---|---|
| 1 | (0,0) | C | 4 |
| 2 | (0,1) | B | 5 |
| 3 | (1, chain:

| C | B | A | D |
|---|---|---|---|
| (1,1) | (1,0) | (0,0) | (0,1) |

The cheapest tent on0) | D | 3 |
| 4 | (1,1) | A | 1 |
| 5 | (-1,1) | A | 2 |

Relevant path:

| Layer | Vertex this chain has weight \(1\), so the minimum cut removes tent 4.

| Total Weight | Minimum Cut | Answer |
|---|---|---|
| 15 | 3 | 12 |

Output:

```text
12
```

This demonstrates that removing a non-important tent may be cheaper than removing the important |
|---|---|
| A | (1,1) |
| B | (0,1) |
| C | (0,0) |
| D | (1,0) |

The minimum cut removes the weight-1 tent \((1,1)\).

| Total weight | Min tent itself.

### Constructed Example

```text
4
0 0 10
1  cut | Answer |
|---|---|---|
| 15 | 10 1
1 1 1
0 1 100
```

The unique forbidden chain is:

| C | B | | 12 |

This demonstrates that removing a single cheap tent can destroy the entire forbidden pattern.

### Sample 2

All weights are \(1\).

The A | D |
|---|---|---|---|
| 1 | 1 | 10 | 100 |

The minimum cut removes construction produces eight independent forbidden paths, either the \(C\) or \(B\) vertex.

| exactly matching the eight patterns shown in the statement illustration Removed Tent Cost | Feasible |
|---|---|
| 1 | Yes |
| 10 | Yes |
| 100 | Yes |

. citeturn0search0

| Total tents | TotalOptimal cut value is \(1\).

| Total Weight | Minimum Cut | Answer |
|---|---|---|
| 112 | 1 | 111 |

The trace shows that weight |
|---|---|
| 32 | 32 |

The minimum cut value is \(8\).

| Total weight | Min cut | Answer |
|---|---|---|
| the flow formulation naturally chooses the cheapest vertex in the forbidden structure.

## Complexity Analysis

| Measure | Complexity 32 | 8 | 24 |

This demonstrates that the graph | Explanation |
|---|---|---|
| Time | \(O(n^2 + V^ formulation correctly handles many overlapping forbidden patterns simultaneously.

## Complexity Analysis

| Measure | Complexity |2E)\) worst case Explanation |
|---|---|---|
| Time | \(O(n^ for Dinic, much smaller in practice | \(n^2\) pair generation plus max flow |
| Space | \(O(n^2)\2 + \text{Dinic})\) | Graph construction) | Graph may contain \(O(n^2)\) edges |

With \(n \le 1000\), the graph contains only checks all pairs of tents |
| Space | \(O(n^2)\) | a few thousand vertices and at most about Worst-case number of edges is quadratic |

With \(n \le 1000 one million candidate pair checks. This\), the graph contains at most a few million comfortably fits within the limits and is the intended solution. citeturn0search0 adjacency entries in the absolute worst case,turn0search3

## Test Cases

```python and the layered structure.stdin = io.StringIO(inp)

    # is extremely friendly to Dinic. This paste solve() and supporting classes here

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue()

# sample
assert run(
 comfortably fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return"""5
0 0 4
0 1 5
1 0  output string
import io
import sys

def run(inp: str) -> str:
    #3
1 1 1
-1 1 2
"""
) == "12\n"

# single tent
assert run(
"""1
0 0  paste solution7
"""
) == "7\n"

# complete forbidden pattern
assert run(
"""4
0 0 10
1 0 1
 into a solve() function when testing1 1 1
0 1 100
"""
) == "111\n"

# negative coordinates
assert run
    pass

# sample 1
assert run(
"""(
"""4
0 0 5
-1 0 5
-1 -1 5
0 -1 5
"""
) == "155
0 0 4
0 1 5
\n"

# no forbidden structure
assert run(
"""3
0 0 10
1 0 3
1 1 1
-1 1 2
"""
) == "12\n"

# single tent
assert run(
"""1
0 10 10 20
20 20 30
"""
) == "60\n"
```

| Test input | Expected output |0 7
"""
) == "7\n"

# one complete forbidden pattern
assert run(
"""4
0 0 100
0 1 1
1 0  What it validates |
|---|---|---|
| Single tent | 7 | Minimum size instance |
| One forbidden quadruple | 111 | Minimum1
1 1 1
"""
) == "102\n"

# no forbidden pattern exists
assert run(
"""3
0 0 5
10 10 6
20 20 7
"""
) == "18\n"

-cut chooses cheapest vertex |
| Negative coordinates | 15 | Correct parity handling |
| Widely separated tents | 60 | No unnecessary removals |

## Edge Cases

Consider the negative-coordinate example:

# choose cheapest tent to remove
assert run(
"""4
0 0 1
0 1 100
1 0 100
1 1 100
"""
) == "300\n"
```

| Test input | Expected output | What it validates```text
4
0 0 5
-1 0 5
-1 -1 5
0 -1 5
```

The four |
|---|---|---|
| Single tent | 7 | Minimum size |
| One forbidden pattern | 102 | Basic cut construction |
| Isolated tents | 18 | No path means no removal |
| Expensive neighbors | 300 | Minimum tents still occupy the four parity classes. The graph contains one source-to-sink chain. Any-weight vertex cut valid solution must remove one tent. The minimum cut value is \(5\), producing answer, not greedy geometry |

## Edge Cases

Consider:

```text
4
0 0 100
0 1 1
1 0 1
1 1 1
```

There is exactly one forbidden configuration. The graph contains one \(A \to B \to C \to D\) path. The minimum cut \(20-5=15\). Incorrect parity computation would miss removes any weight-1 tent. The answer is \(103 - 1 = 102\). A greedy strategy that always deletes the important tent would the chain entirely and return \(20\).

Consider a tent participating in multiple forbidden structures:

```text
5
0  lose weight 100 and be far from optimal.

Now consider:

```text
0 100
1 0 1
1 1 1
0 1 1
2 0 1
```

The important tent \((0,0)\3
0 0 5
10 10 6
20 20 7
```

No pair of tents is adjacent,) appears in more than one potential interaction. The cut model does not process configurations independently. It globally chooses the cheapest set of removed tents, avoiding the double-counting mistakes that so the flow graph contains no \(A \to D\) path. The maximum flow is zero, the minimum cut is zero, and all tents remain. The answer is 18.

Finally, greedy local fixes can make.

Consider a configuration where the important tent is very heavy:

```text
4
 consider negative coordinates:

```text
4
0 0 1000
1 0 1
1 1 1
0 1 0 0 5
0 1 2
-1
```

A naive strategy might1 0 2
-1 1 2
```

Parity classification must focus on removing important tents. The minimum cut instead removes one of the weight-\(1\) tents. The answer becomes \(1002\), which is optimal because only be computed correctly for negative values. Using `x & 1` and `y & 1` works for both positive and negative integers in Python. The graph still forms one forbidden path, and the algorithm removes one weight-2 tent, producing the correct answer 9.
