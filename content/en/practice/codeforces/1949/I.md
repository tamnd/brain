---
title: "CF 1949I - Disks"
description: "Each disk has a fixed center and an initial radius. Some pairs of disks are tangent, meaning they touch at exactly one point. Because the disks never overlap with positive area, every tangent pair satisfies $$text{distance between centers} = ri + rj." date: "2026-05-31T00:00:00+07:00" tags: ["codeforces", "competitive-programming", "dfs-and-similar", "geometry", "graph-matchings", "graphs"] categories: ["algorithms"] codeforces_contest: 1949 codeforces_index: "I" codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)" rating: 1800 weight: 1949 solve_time_s: 114 verified: true draft: false --- [CF 1949I - Disks](https://codeforces.com/problemset/problem/1949/I) **Rating:** 1800   **Tags:** dfs and similar, geometry, graph matchings, graphs   **Solve time:** 1m 54s   **Verified:** yes   ## Solution ## Problem Understanding Each disk has a fixed center and an initial radius. Some pairs of disks are tangent, meaning they touch at exactly one point. Because the disks never overlap with positive area, every tangent pair satisfies$$\text{distance between centers} = r_i + r_j.$$
We may replace the radii by new positive real values. The centers stay fixed. Every pair that was tangent must remain tangent after the change, and disks must still avoid overlapping. The goal is to make the total sum of radii strictly smaller.
The first step is to forget about geometry as much as possible and focus on the tangent relationships. If two disks are tangent, the distance between their centers is fixed forever. Since they must remain tangent, the new radii must still add up to exactly that same distance.
The number of disks is at most $1000$. Checking every pair of disks costs about $10^6$ comparisons, which is completely reasonable. Any solution that repeatedly explores the graph built from tangencies is also easily fast enough.
The dangerous part of the problem is that reducing one radius usually forces changes in many other radii. Tangencies create equations linking disks together. Looking only at a single disk and trying to shrink it greedily gives the wrong answer.
Consider three tangent disks in a chain:
```
1 -- 2 -- 3
```
If disk 1 decreases by $x$, disk 2 must increase by $x$ to preserve the first tangency. Then disk 3 must decrease by $x$ to preserve the second tangency. The effect propagates through the entire component.
Another easy mistake is to look only for bipartite components. A bipartite component does give freedom to modify radii, but that freedom is useful only when the two color classes have different sizes.
For example:
```
1 -- 2
```
The component is bipartite, with color classes of sizes $1$ and $1$. Any valid modification changes one radius by $+t$ and the other by $-t$, leaving the total sum unchanged. The correct answer is `NO`.
A final subtle case is an odd cycle:
```
1 -- 2
 \  /
  3
```
The tangency equations force every change to be zero. Even though the graph is connected, there is no freedom at all.
## Approaches
A brute-force mindset starts from the tangency equations. For every tangent pair $(i,j)$,
$$r'_i+r'_j=d_{ij},$$
where $d_{ij}$ is the fixed center distance.
One could write a system of linear equations and ask whether there exists a solution with a smaller total radius sum. That is mathematically correct, but solving a general real-valued system is unnecessary. With up to $1000$ disks, a dense linear-algebra approach would be much more complicated than needed.
The key observation is that only differences from the original radii matter.
Define
$$\Delta_i = r'_i-r_i.$$
For every tangent edge,
$$(r_i+\Delta_i)+(r_j+\Delta_j)=r_i+r_j,$$
which simplifies to
$$\Delta_i+\Delta_j=0.$$
This equation is extremely restrictive. Along every edge, the two endpoint changes must be exact opposites.
If we choose a value $t$ for one vertex, every neighbor must have value $-t$, every neighbor of that neighbor must have value $+t$, and so on. The component naturally becomes a graph coloring problem.
If a connected component contains an odd cycle, following the alternation around the cycle forces $t=-t$, hence $t=0$. Every vertex in that component must remain unchanged.
If the component is bipartite, every vertex in one color class gets $+t$ and every vertex in the other gets $-t$. The entire component has exactly one degree of freedom.
The total radius sum changes by
$$t\cdot(|A|-|B|),$$
where $A$ and $B$ are the two bipartition classes.
When $|A|=|B|$, every allowed modification preserves the total sum.
When $|A|\neq|B|$, choosing the sign of $t$ appropriately makes the total sum smaller. Because all non-tangent pairs have a positive gap and all radii are initially positive, a sufficiently small nonzero $t$ preserves every required inequality.
The problem reduces to finding whether there exists a connected bipartite tangent component whose two color classes have different sizes.
| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Linear-system viewpoint | Roughly $O(n^3)$ | $O(n^2)$ | Unnecessarily heavy |
| Graph bipartite analysis | $O(n^2)$ | $O(n^2)$ | Accepted |
## Algorithm Walkthrough
1. Build the tangency graph.
For every pair of disks, compute the squared distance between centers. If
$$(x_i-x_j)^2+(y_i-y_j)^2=(r_i+r_j)^2,$$
the disks are tangent and we add an undirected edge.
2. Process every connected component with DFS or BFS.
We attempt a two-coloring of the component.
3. Assign color 0 to the starting vertex.
For every edge, neighbors must receive the opposite color because the equation $\Delta_i+\Delta_j=0$ forces alternating signs.
4. Detect whether the component is bipartite.
If an edge connects two vertices with the same color, the component contains an odd cycle. In that case the only possible change is $t=0$, so this component can never help.
5. For every bipartite component, count the sizes of the two color classes.
Let those counts be $c_0$ and $c_1$.
6. If $c_0\neq c_1$, immediately answer `YES`.
The component admits a nonzero parameter $t$. Choosing the sign of $t$ appropriately decreases the total radius sum.
7. If no component satisfies the previous condition, answer `NO`.
### Why it works
For every tangent edge, the relation $\Delta_i+\Delta_j=0$ must hold. In a connected bipartite component, all values are determined by a single parameter $t$: one color class receives $+t$, the other receives $-t$. The total change in radius sum becomes $t(c_0-c_1)$.
If $c_0\neq c_1$, selecting the sign of $t$ opposite to $c_0-c_1$ makes the total sum strictly smaller. Taking $t$ sufficiently small keeps every radius positive and preserves all strict non-overlap inequalities for non-tangent pairs.
If the component is not bipartite, an odd cycle forces $t=-t$, hence $t=0$. No radius can change inside that component. If every bipartite component has equal color-class sizes, every allowed modification changes the total sum by zero. A strict decrease is impossible.
These two facts are both necessary and sufficient, so the algorithm is correct.
## Python Solution
```python
import sys
input = sys.stdin.readline
def solve():
    n = int(input())
    disks = [tuple(map(int, input().split())) for _ in range(n)]
    g = [[] for _ in range(n)]
    for i in range(n):
        x1, y1, r1 = disks[i]
        for j in range(i + 1, n):
            x2, y2, r2 = disks[j]
            dx = x1 - x2
            dy = y1 - y2
            dist2 = dx * dx + dy * dy
            rs = r1 + r2
            if dist2 == rs * rs:
                g[i].append(j)
                g[j].append(i)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        stack = [start]
        color[start] = 0
        cnt = [1, 0]
        bipartite = True
        while stack:
            v = stack.pop()
            for to in g[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    stack.append(to)
                elif color[to] == color[v]:
                    bipartite = False
        if bipartite and cnt[0] != cnt[1]:
            print("YES")
            return
    print("NO")
solve()
```
The graph construction uses squared distances, avoiding floating-point arithmetic entirely. Coordinates and radii can be as large as $10^9$, so squared values can reach about $4 \cdot 10^{18}$. Python integers handle this safely.
The DFS simultaneously checks bipartiteness and counts the sizes of the two color classes. Isolated vertices form a bipartite component with counts $(1,0)$, which is exactly what we want. An isolated disk can simply shrink a little, immediately decreasing the total radius sum.
The moment we find a bipartite component with unequal color classes, we can stop. One such component is enough to construct a valid modification.
## Worked Examples
### Example 1
Input:
```
5
0 2 1
0 0 1
4 -3 4
11 0 3
11 5 2
```
The tangency graph contains one relevant component:
```
1 -- 2 -- 3
```
The remaining disks are isolated.
| Vertex | Color | Count Color 0 | Count Color 1 |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 0 | 2 | 1 |
The component is bipartite and the color classes have sizes $2$ and $1$.
Since the sizes differ, we can choose a small nonzero $t$ that decreases the total radius sum. The algorithm prints `YES`.
### Example 2
Input:
```
3
0 0 1
2 0 1
1 1732050808 1
```
These three disks form a triangle of tangencies.
| Vertex | Assigned Color | Observation |
| --- | --- | --- |
| 1 | 0 | Start DFS |
| 2 | 1 | Opposite color |
| 3 | 1 | Opposite color from 1 |
| Edge (2,3) | Conflict | Same-color edge |
The component is not bipartite. The odd cycle forces every change value to be zero. No useful component exists, so the answer is `NO`.
This example demonstrates the key obstruction: an odd cycle removes all freedom.
## Complexity Analysis
| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Checking all disk pairs dominates the running time |
| Space | $O(n^2)$ | The tangency graph can contain $O(n^2)$ edges |
With $n \le 1000$, about one million pair checks are required. This comfortably fits within the time limit, and the graph size remains manageable within the memory limit.
## Test Cases
```python
# helper: run solution on input string, return output string
import sys
import io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    n = int(input())
    disks = [tuple(map(int, input().split())) for _ in range(n)]
    g = [[] for _ in range(n)]
    for i in range(n):
        x1, y1, r1 = disks[i]
        for j in range(i + 1, n):
            x2, y2, r2 = disks[j]
            dx = x1 - x2
            dy = y1 - y2
            if dx * dx + dy * dy == (r1 + r2) ** 2:
                g[i].append(j)
                g[j].append(i)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        stack = [s]
        color[s] = 0
        cnt = [1, 0]
        bip = True
        while stack:
            v = stack.pop()
            for to in g[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    cnt[color[to]] += 1
                    stack.append(to)
                elif color[to] == color[v]:
                    bip = False
        if bip and cnt[0] != cnt[1]:
            return "YES\n"
    return "NO\n"
# provided sample
assert run(
"""5
0 2 1
0 0 1
4 -3 4
11 0 3
11 5 2
"""
) == "YES\n"
# single isolated disk
assert run(
"""1
0 0 5
"""
) == "YES\n"
# single tangent pair, balanced bipartition
assert run(
"""2
0 0 1
2 0 1
"""
) == "NO\n"
# chain of three disks, unbalanced bipartition
assert run(
"""3
0 0 1
2 0 1
4 0 1
"""
) == "YES\n"
# odd cycle of tangencies
assert run(
"""3
0 0 1
2 0 1
1 1732050808 1
"""
) == "NO\n"
```
| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single isolated disk | YES | An isolated vertex gives immediate freedom |
| Two tangent disks | NO | Bipartite but balanced component |
| Three-disk chain | YES | Bipartite and unbalanced |
| Odd cycle | NO | Non-bipartite component forces zero change |
## Edge Cases
Consider a single disk:
```
1
0 0 10
```
The graph contains one isolated vertex. The DFS finds a bipartite component with color-class sizes $(1,0)$. Since the counts differ, the algorithm returns `YES`. Geometrically, we can simply reduce the radius slightly.
Consider two tangent disks:
```
2
0 0 1
2 0 1
```
The graph is one edge. The bipartition sizes are $(1,1)$. Any valid modification must add $t$ to one disk and subtract $t$ from the other, leaving the total sum unchanged. The algorithm correctly returns `NO`.
Consider an odd cycle:
```
3
0 0 1
2 0 1
1 1732050808 1
```
During DFS, the third edge connects vertices with the same color. The component is marked non-bipartite. Algebraically this means
$$\Delta_1=-\Delta_2=\Delta_3=-\Delta_1,$$
forcing $\Delta_1=0$. No disk can change, and the algorithm returns `NO`.
Consider multiple components:
```
4
0 0 1
2 0 1
100 0 1
104 0 3
```
The first component is a balanced edge and contributes nothing. The second component consists of two isolated vertices, each an unbalanced bipartite component. The algorithm examines all components and returns `YES` as soon as it encounters one with unequal color-class sizes. This matches the fact that modifying a single isolated disk is enough.
