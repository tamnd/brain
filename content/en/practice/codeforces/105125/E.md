---
title: "CF 105125E - Irrational Path"
description: "We are given a directed graph whose edges are labeled with decimal digits. Starting from vertex 1, we may walk forever by following directed edges. The sequence of edge labels becomes the decimal expansion of a number between 0 and 1."
date: "2026-06-27T19:30:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105125
codeforces_index: "E"
codeforces_contest_name: "MITIT 2024 Spring Invitational Qualification"
rating: 0
weight: 105125
solve_time_s: 95
verified: false
draft: false
---

[CF 105125E - Irrational Path](https://codeforces.com/problemset/problem/105125/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph whose edges are labeled with decimal digits. Starting from vertex 1, we may walk forever by following directed edges. The sequence of edge labels becomes the decimal expansion of a number between 0 and 1.

The question is whether there exists an infinite walk whose decimal expansion is irrational. A decimal expansion is irrational exactly when its digits are **not eventually periodic**, so the task is really asking whether the graph can generate a non eventually periodic digit sequence.

The graph is large, but the total number of vertices and edges across all test cases is at most $2 \cdot 10^5$. Any algorithm that repeatedly explores the same graph or performs work proportional to $N^2$ or $M^2$ is immediately ruled out. A linear or near linear graph algorithm is required.

Several situations are easy to overlook.

Suppose there is no reachable cycle.

```
1 -> 2 -> 3
```

There is no infinite walk at all, so the answer is `No`. A solution that only checks for different edge labels would incorrectly answer `Yes`.

Suppose the reachable part is a single directed cycle.

```
1 -> 2 (digit 1)
2 -> 3 (digit 2)
3 -> 1 (digit 3)
```

Every infinite walk repeats `123123123...`, so every decimal is rational. The correct answer is `No`.

The most subtle case is when an SCC contains branching, but every outgoing edge from the same "position in the cycle" always carries the same digit. Such branching changes the visited vertices, but never changes the produced digit sequence. Looking only at the graph structure is not enough, the edge labels also matter.

## Approaches

A brute force idea is to enumerate longer and longer walks while checking whether the produced digit sequence eventually becomes periodic. This is correct in principle because irrationality is exactly the absence of eventual periodicity. Unfortunately, the number of walks grows exponentially with the walk length, so even exploring all walks of length 50 is already impossible.

The key observation is that every infinite walk eventually stays inside one strongly connected component. Once it leaves an SCC, it can never return. This allows us to analyze each reachable SCC independently.

Inside one SCC, every cycle length has some greatest common divisor $g$. A classical graph property shows that this value can be computed in linear time by taking the gcd of all values

$$\text{depth}[u] + 1 - \text{depth}[v]$$

over every directed edge $(u,v)$ in a DFS tree.

After computing $g$, every vertex naturally belongs to one of $g$ residue classes according to its DFS depth modulo $g$. Every edge always goes from residue $c$ to residue $c+1 \pmod g$.

Now comes the crucial characterization. If every edge leaving vertices of the same residue class always carries the same digit, then every infinite walk must emit exactly the same digit whenever it visits that residue class. The produced decimal is forced to repeat every $g$ positions, so every walk is eventually periodic.

Conversely, if some residue class contains two outgoing edges with different digits, we can repeatedly choose between them while remaining inside the SCC. This allows constructing a digit sequence that is not eventually periodic, giving an irrational decimal. This characterization is proved in the official analysis.

The entire algorithm becomes a sequence of SCC decomposition, DFS, gcd computation, and one pass over the edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(N+M)$ | $O(N+M)$ | Accepted |

## Algorithm Walkthrough

1. Run a DFS or BFS from vertex 1 and ignore every unreachable vertex.
2. Compute the strongly connected components of the reachable subgraph.
3. Process every reachable SCC separately. Ignore SCCs that cannot contain an infinite walk, namely single vertices without self loops.
4. Pick any vertex of the SCC as the root and build a DFS tree inside the SCC. Record the tree depth of every vertex.
5. Compute the gcd

$$g=\gcd(\text{depth}[u]+1-\text{depth}[v])$$

over every edge of the SCC.
6. Color every vertex by `depth % g`. When `g = 0`, replace it by 1 since an SCC always has at least one cycle.
7. For every residue class, examine every outgoing edge of every vertex in that class. All these edges must carry the same digit. If some residue class contains two different digits, immediately answer `Yes`.
8. If every reachable SCC satisfies the previous condition, answer `No`.

### Why it works

Every infinite walk eventually remains inside one reachable SCC. Inside an SCC, the gcd of all cycle lengths determines a canonical cyclic ordering of the positions in every infinite walk. Vertices with the same depth modulo $g$ always occupy the same position in that ordering.

If every residue class always emits the same digit, then the digit at position $i$ depends only on $i \bmod g$. Every infinite walk is eventually periodic, hence every decimal is rational.

If one residue class can emit two different digits, we can repeatedly revisit that residue class and independently choose which digit to output each time. Choosing according to any non eventually periodic binary sequence produces a non eventually periodic decimal expansion, which is irrational.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    edges = []

    for _ in range(m):
        u, v, d = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, d))
        rg[v].append(u)
        edges.append((u, v, d))

    # reachable
    vis = [False] * n
    stack = [0]
    vis[0] = True
    while stack:
        v = stack.pop()
        for to, _ in g[v]:
            if not vis[to]:
                vis[to] = True
                stack.append(to)

    order = []
    used = [False] * n

    def dfs1(v):
        used[v] = True
        for to, _ in g[v]:
            if vis[to] and not used[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if vis[i] and not used[i]:
            dfs1(i)

    comp = [-1] * n

    def dfs2(v, c):
        comp[v] = c
        comps[-1].append(v)
        for to in rg[v]:
            if vis[to] and comp[to] == -1:
                dfs2(to, c)

    comps = []
    cid = 0
    for v in reversed(order):
        if comp[v] == -1:
            comps.append([])
            dfs2(v, cid)
            cid += 1

    ok = False

    for idx, verts in enumerate(comps):
        if ok:
            break

        if len(verts) == 1:
            u = verts[0]
            self_loop = False
            for to, _ in g[u]:
                if to == u:
                    self_loop = True
            if not self_loop:
                continue

        depth = {}
        root = verts[0]

        def dfs(v):
            for to, _ in g[v]:
                if comp[to] != idx:
                    continue
                if to not in depth:
                    depth[to] = depth[v] + 1
                    dfs(to)

        depth[root] = 0
        dfs(root)

        cyc = 0
        for u in verts:
            for v, _ in g[u]:
                if comp[v] == idx:
                    cyc = gcd(cyc, abs(depth[u] + 1 - depth[v]))
        if cyc == 0:
            cyc = 1

        digit = {}
        for u in verts:
            c = depth[u] % cyc
            for v, d in g[u]:
                if comp[v] != idx:
                    continue
                if c in digit:
                    if digit[c] != d:
                        ok = True
                        break
                else:
                    digit[c] = d
            if ok:
                break

    print("Yes" if ok else "No")
```

The first part removes every unreachable vertex because no valid walk can ever enter those vertices.

Kosaraju's algorithm decomposes the remaining graph into SCCs. Since every infinite walk eventually stays inside one SCC, each component can be checked independently.

For every relevant SCC, a DFS assigns depths. These depths are only one possible spanning tree, but the gcd computation removes the dependence on the particular tree. The value

`depth[u] + 1 - depth[v]`

captures how much each non tree edge changes the cycle length, and taking the gcd over all such values recovers the gcd of every cycle length in the SCC.

Finally, vertices are grouped by `depth % cyc`. Every outgoing edge from one residue class must carry the same digit. The moment two different digits appear, we have found an irrational path and can stop immediately.

## Worked Examples

### Sample 1

The reachable SCC is a single directed cycle.

| Step | Value |
| --- | --- |
| SCC | {1,2,3} |
| gcd | 3 |
| Residues | 0,1,2 |
| Digits by residue | 1,2,3 |
| Conflict | No |

Every residue always emits the same digit, so every walk repeats `123`.

### Second example

```
1 -> 1 (0)
1 -> 2 (1)
2 -> 1 (1)
2 -> 2 (0)
```

| Step | Value |
| --- | --- |
| SCC | {1,2} |
| gcd | 1 |
| Residues | both vertices in residue 0 |
| Digits leaving residue 0 | 0 and 1 |
| Conflict | Yes |

Since one residue can emit either digit, we can build arbitrary binary sequences, including non eventually periodic ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N+M)$ | SCC decomposition, DFS, gcd computation, and edge scan are all linear |
| Space | $O(N+M)$ | Graph storage and auxiliary arrays |

Because the total number of vertices and edges over all test cases is at most $2 \cdot 10^5$, a linear algorithm easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    # paste solution here
    ...

# sample
assert run("""3
4 4
1 2 1
1 2 1
2 3 2
3 1 3
2 4
1 1 0
1 2 1
2 1 1
2 2 0
6 6
1 2 4
1 3 5
2 4 6
2 5 7
6 6 8
6 6 9
""") == "No\nYes\nNo\n"

assert run("""1
1 1
1 1 7
""") == "No\n"

assert run("""1
2 2
1 2 0
2 1 1
""") == "No\n"

assert run("""1
2 4
1 1 0
1 2 1
2 1 1
2 2 0
""") == "Yes\n"

assert run("""1
3 2
1 2 5
2 3 6
""") == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single self loop | No | Purely periodic decimal |
| One directed cycle | No | Every walk repeats |
| SCC with conflicting digits | Yes | Irrational sequence exists |
| No reachable cycle | No | Infinite walk is impossible |

## Edge Cases

Consider a graph with no reachable cycle.

```
1 2
1 2 5
2 3 6
```

The reachable subgraph contains no SCC with a cycle, so every SCC is skipped. The algorithm correctly prints `No`.

Consider a single reachable directed cycle.

```
3 3
1 2 1
2 3 2
3 1 3
```

The gcd is 3, each residue class emits exactly one digit, and no conflict is found. The output is `No`.

Finally, consider

```
2 4
1 1 0
1 2 1
2 1 1
2 2 0
```

The whole graph is one SCC. The gcd equals 1, so every vertex belongs to the same residue class. That residue has outgoing edges labeled both 0 and 1, so the algorithm immediately reports `Yes`, exactly matching the existence of non eventually periodic binary digit sequences.
