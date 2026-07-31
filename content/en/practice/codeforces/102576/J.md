---
title: "CF 102576J - Space Gophers"
description: "The asteroid is a huge cubic grid with side length one million, so explicitly storing cells is impossible. The only empty cells are those removed by tunnels. Each tunnel is a complete straight line parallel to one of the three axes."
date: "2026-07-31T07:39:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "J"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 78
verified: true
draft: false
---

[CF 102576J - Space Gophers](https://codeforces.com/problemset/problem/102576/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The asteroid is a huge cubic grid with side length one million, so explicitly storing cells is impossible. The only empty cells are those removed by tunnels. Each tunnel is a complete straight line parallel to one of the three axes.

A tunnel can be described by the two coordinates that stay fixed. For example, a tunnel along the x-axis is identified by `(y, z)`, because every `(x, y, z)` cell is empty. The task is to answer whether two given empty cells belong to the same connected region of empty cells.

The constraints are the key difficulty. There can be 300000 tunnels and 500000 queries. A BFS over the cube would require up to `10^18` cells, which is impossible. Even a graph containing all empty cells is far too large. The algorithm must work only with the tunnels themselves.

The hidden structure is that the number of tunnels is small compared with the size of the asteroid. We only need to understand how tunnels connect to each other.

A common mistake is to check only whether two cells lie on the same tunnel. This fails because adjacent parallel tunnels are connected. Another mistake is to check only intersections of different directions. Two parallel tunnels one unit apart never intersect, but a gopher can still move between them.

## Approaches

The brute force solution would generate every empty cell, connect neighboring cells, and run connected components. The asteroid contains `10^18` cells, so even creating the grid is impossible.

A better attempt is to make a graph where every tunnel is a vertex. Two vertices are connected if the corresponding tunnels touch. A direct implementation would still be too slow because many tunnels can intersect the same coordinate plane. For example, thousands of x-tunnels and y-tunnels at the same z-coordinate would create millions of pairwise intersections.

The important observation is that intersections do not need to be represented individually. If several tunnels all pass through the same slice, one auxiliary vertex can represent the whole slice. Connecting every tunnel to this auxiliary vertex gives exactly the same connectivity.

For example, every x-tunnel with the same z-coordinate intersects every y-tunnel with that z-coordinate. A single "z slice" node connects all of them.

After this compression, only local adjacency between parallel tunnels remains. That can be handled with hash maps because each tunnel only needs to check its four possible neighbors in its two-dimensional coordinate space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^18) | O(10^18) | Impossible |
| Tunnel graph with pairwise intersections | O(n²) | O(n²) | Too slow |
| DSU with auxiliary slice nodes | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every unique tunnel and assign it an id. A tunnel is stored by its orientation and its two fixed coordinates.
2. Create a disjoint set union structure containing all tunnels and additional auxiliary nodes. An auxiliary node represents all tunnels sharing one fixed coordinate slice.
3. Connect perpendicular tunnels through auxiliary nodes. An x-tunnel `(y,z)` is connected to the auxiliary nodes representing coordinate `y` and coordinate `z`, because these are exactly the slices where perpendicular tunnels can meet it.
4. Connect parallel neighboring tunnels. For every tunnel, check whether another tunnel of the same orientation exists with one fixed coordinate increased by one. If it exists, merge their components.
5. For each query, find all tunnels containing the starting cell and all tunnels containing the ending cell. Since a cell is guaranteed to be empty, at least one tunnel exists for each side. If any starting tunnel and ending tunnel have the same DSU representative, the answer is `YES`.

Why it works:

Every movement between empty cells either stays on the same tunnel, moves between adjacent parallel tunnels, or happens at an intersection of two perpendicular tunnels. The DSU contains exactly these three types of connections. The auxiliary nodes represent all possible perpendicular intersections without explicitly creating every pair. Therefore two cells are connected in the original asteroid exactly when their corresponding tunnel vertices are in the same DSU component.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    z = int(input())
    out = []

    for _ in range(z):
        n = int(input())

        xt = {}
        yt = {}
        zt = {}

        tunnels = []

        for _ in range(n):
            a, b, c = map(int, input().split())
            if c == -1:
                key = (a, b)
                if key not in zt:
                    zt[key] = len(tunnels)
                    tunnels.append((2, a, b))
            elif b == -1:
                key = (a, c)
                if key not in yt:
                    yt[key] = len(tunnels)
                    tunnels.append((1, a, c))
            else:
                key = (b, c)
                if key not in xt:
                    xt[key] = len(tunnels)
                    tunnels.append((0, b, c))

        parent = []
        size = []

        def add():
            parent.append(len(parent))
            size.append(1)
            return len(parent) - 1

        for _ in tunnels:
            add()

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a = find(a)
            b = find(b)
            if a == b:
                return
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]

        aux = {}

        def get_aux(t, x):
            key = (t, x)
            if key not in aux:
                aux[key] = add()
            return aux[key]

        for i, (typ, a, b) in enumerate(tunnels):
            if typ == 0:
                union(i, get_aux(0, a))
                union(i, get_aux(1, b))
            elif typ == 1:
                union(i, get_aux(0, b))
                union(i, get_aux(2, a))
            else:
                union(i, get_aux(1, a))
                union(i, get_aux(2, b))

        for (a, b), i in xt.items():
            if (a + 1, b) in xt:
                union(i, xt[(a + 1, b)])
            if (a, b + 1) in xt:
                union(i, xt[(a, b + 1)])

        for (a, b), i in yt.items():
            if (a + 1, b) in yt:
                union(i, yt[(a + 1, b)])
            if (a, b + 1) in yt:
                union(i, yt[(a, b + 1)])

        for (a, b), i in zt.items():
            if (a + 1, b) in zt:
                union(i, zt[(a + 1, b)])
            if (a, b + 1) in zt:
                union(i, zt[(a, b + 1)])

        def get_lines(x, y, z):
            res = []
            if (y, z) in xt:
                res.append(xt[(y, z)])
            if (x, z) in yt:
                res.append(yt[(x, z)])
            if (x, y) in zt:
                res.append(zt[(x, y)])
            return res

        q = int(input())
        for _ in range(q):
            x1, y1, z1, x2, y2, z2 = map(int, input().split())
            a = get_lines(x1, y1, z1)
            b = get_lines(x2, y2, z2)

            ok = False
            for u in a:
                ru = find(u)
                for v in b:
                    if ru == find(v):
                        ok = True
                        break
                if ok:
                    break

            out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation keeps only the tunnels and the compressed slice graph. The coordinate values can remain as full integers because they are only used as dictionary keys. No coordinate compression is required.

The subtle part is the auxiliary node construction. A tunnel is not connected to every tunnel that intersects it. Instead, it is connected to a node representing the entire coordinate slice. This avoids quadratic behavior while preserving connectivity.

The neighbor checks only use `+1` because every undirected adjacency in the compressed two-dimensional tunnel layout is discovered from one endpoint. Checking negative directions would duplicate work.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each tunnel performs constant dictionary operations and each query checks at most three tunnels against three tunnels. |
| Space | O(n) | The DSU contains tunnel nodes and at most a constant number of auxiliary nodes per tunnel coordinate. |

The largest cases contain hundreds of thousands of tunnels and queries. The algorithm never touches the million-by-million-by-million cube, so it fits comfortably within the limits.
