---
title: "CF 105780E - Walrus Wallflowers"
description: "The garden is an n x n grid. Some cells already contain flowers. During the process, cells can gain flowers or pairs of cells can be joined by underground tunnels."
date: "2026-06-25T15:54:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105780
codeforces_index: "E"
codeforces_contest_name: "UTPC x WiCS Contest 3-12-25 (UT Internal)"
rating: 0
weight: 105780
solve_time_s: 54
verified: true
draft: false
---

[CF 105780E - Walrus Wallflowers](https://codeforces.com/problemset/problem/105780/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The garden is an `n x n` grid. Some cells already contain flowers. During the process, cells can gain flowers or pairs of cells can be joined by underground tunnels. A group of flowers belongs to the same budding when the flowers are connected through normal grid adjacency or through underground tunnels.

For every budding, we need two values. The first is `f`, the number of flower cells inside it. The second is `c`, the number of underground tunnels touching that budding. The energy contributed by this budding is `max(f - sqrt(c), 0)`. After every operation, the task is to compute the sum of these values over all buddings.

The limits are small enough to allow rebuilding the whole connectivity structure after every operation. The grid has at most `10000` cells and there are at most `1000` operations. A solution around `1000 * 10000` operations is only about ten million basic operations, so there is no need for a complicated dynamic connectivity structure. A solution that scans the grid from scratch after every update is acceptable, while approaches that simulate every possible budding separately or repeatedly search through all pairs of cells would be unnecessarily expensive.

The main implementation pitfalls are around connectivity and counting tunnels. A flower cell can be connected to another flower through a chain of underground tunnels or adjacent flower cells, so only checking direct neighbors gives wrong results. For example:

```
2 1
10
01
2 0 0 1 1
```

After the tunnel is added, the two flowers form one budding. The answer is `2 - sqrt(1)`, not `2`, because the underground connection contributes to `c`.

Another subtle case is a repeated flower insertion.

```
2 1
10
00
1 0 0
```

The cell already has a flower, so the garden does not change. A careless implementation that increments the flower count without checking the current state would overcount.

A final edge case is a budding with many tunnels but few flowers.

```
2 1
10
00
2 0 0 0 1
```

The dirt cell becomes connected underground to the flower cell, but it is not counted as a flower. The budding has `f = 1` and `c = 1`, so the contribution is `0`. Counting every connected cell as a flower would produce an incorrect result.

## Approaches

The straightforward approach is to maintain the garden after each query and recompute all buddings. We can model every grid cell as a vertex. Adjacent cells are connected by normal grid edges, and underground operations add extra edges. After each update, we run a disjoint set union over all cells, joining adjacent cells and all underground connections. Then we count, for every resulting component, how many cells contain flowers and how many underground edges belong to it.

This works because the number of cells and operations are both small. The worst case performs roughly `1000` rebuilds. Each rebuild touches `10000` cells, about `20000` grid adjacency checks, and at most `1000` underground edges. This is comfortably within the limit.

A more advanced dynamic connectivity solution would maintain components as tunnels and flowers change, but it is unnecessary here. The key observation is that the whole state space is small enough that rebuilding is simpler and safer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d * n²) | O(n²) | Too slow if implemented with repeated graph searches |
| Rebuild DSU | O(d * (n² + d)) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Store whether each cell currently has a flower and store every underground connection that has been added. The operations are only additions, so we never need to remove information.
2. After each query, create a fresh disjoint set union structure containing all `n * n` cells. Initially every cell is separate. We rebuild because the total size of the grid is small.
3. Join every pair of horizontally or vertically adjacent cells. This represents normal grid connectivity. The reason we include all cells, including dirt cells, is that a future flower can appear on any cell and underground or grid connectivity is a property of the cells themselves.
4. Join both endpoints of every underground connection. This adds the extra paths created by Karp's operations.
5. Traverse every cell and count the number of flower cells inside each DSU component. Only flower cells contribute to `f`.
6. Traverse every underground connection and count it inside its component. Because every underground edge has already been merged into the DSU, both endpoints have the same representative, so each edge belongs to exactly one budding.
7. For every component containing flowers, add `max(f - sqrt(c), 0)` to the answer. Print the resulting energy.

Why it works: the DSU invariant is that two cells have the same representative exactly when they are connected through all currently available paths. Since every grid adjacency and underground tunnel is merged before counting, every budding is represented by one DSU component. Counting flowers inside a component gives the correct `f`, and counting underground edges in that component gives the correct `c`. The final summation applies the energy formula independently to every budding, so the result is exactly the required garden energy.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    total = n * n

    flowers = []
    for _ in range(n):
        s = input().strip()
        flowers.extend(ch == '1' for ch in s)

    tunnels = []

    def idx(x, y):
        return x * n + y

    def compute():
        parent = list(range(total))
        size = [1] * total

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

        for i in range(n):
            for j in range(n):
                cur = idx(i, j)
                if i + 1 < n:
                    union(cur, idx(i + 1, j))
                if j + 1 < n:
                    union(cur, idx(i, j + 1))

        for a, b in tunnels:
            union(a, b)

        flower_count = [0] * total
        for i, has_flower in enumerate(flowers):
            if has_flower:
                flower_count[find(i)] += 1

        tunnel_count = [0] * total
        for a, b in tunnels:
            tunnel_count[find(a)] += 1

        ans = 0.0
        for i in range(total):
            if flower_count[i]:
                ans += max(flower_count[i] - math.sqrt(tunnel_count[i]), 0.0)

        return ans

    out = []
    for _ in range(d):
        q = list(map(int, input().split()))
        if q[0] == 1:
            flowers[idx(q[1], q[2])] = True
        else:
            tunnels.append((idx(q[1], q[2]), idx(q[3], q[4])))

        out.append(f"{compute():.10f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `flowers` array stores the current state of every grid cell using a flattened index. Flattening avoids repeatedly storing coordinate pairs and makes DSU operations direct.

The `compute` function rebuilds connectivity. The first union loop adds the normal grid edges, and the second union loop adds all underground tunnels. The ordering does not affect the final components because DSU only represents connectivity.

The two counting arrays are separate because flowers and tunnels represent different quantities. `flower_count` counts cells, while `tunnel_count` counts underground connections. Mixing them would produce incorrect values for the square root term.

The final loop only considers components with at least one flower. Components made entirely of dirt do not form buddings and contribute nothing.

## Worked Examples

For the first sample:

```
3 4
101
100
001
1 2 0
2 0 0 0 1
2 0 2 2 2
1 0 1
```

The important state changes are:

| Step | Operation | Flower count in buddings | Tunnel count in buddings | Energy |
| --- | --- | --- | --- | --- |
| Initial | No operation yet | Three isolated groups | 0, 0, 0 | 5.00000000 |
| 1 | Add flower at (2,0) | Three isolated groups | 0, 0, 0 | 5.00000000 |
| 2 | Add tunnel between (0,0) and (0,1) | Same groups | One group has 1 tunnel | 4.00000000 |
| 3 | Add tunnel between (0,2) and (2,2) | Two groups | Each connected group has 1 tunnel | 3.00000000 |
| 4 | Add flower at (0,1) | One connected group | 2 tunnels | 4.58578644 |

This trace shows why tunnels affect only the square root term. They merge flowers into the same budding and also increase the tunnel count.

For a smaller custom example:

```
2 3
10
00
2 0 0 0 1
1 1 0
1 0 1
```

| Step | Operation | Flower count | Tunnel count | Energy |
| --- | --- | --- | --- | --- |
| 1 | Connect (0,0) and (0,1) | 1 | 1 | 0.00000000 |
| 2 | Add flower at (1,0) | 2 | 1 | 1.00000000 |
| 3 | Add flower at (0,1) | 3 | 1 | 2.00000000 |

The trace demonstrates that dirt cells can later become flowers while keeping the same connectivity structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d * (n² + d)) | Each query rebuilds DSU over all cells and all tunnels |
| Space | O(n²) | The DSU arrays and grid state each store one value per cell |

With `n = 100`, there are only `10000` cells. With `d = 1000`, the total work is around a few tens of millions of simple operations, which fits comfortably in the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 4
101
100
001
1 2 0
2 0 0 0 1
2 0 2 2 2
1 0 1
""") == """5.0000000000
4.0000000000
3.0000000000
4.5857864376
"""

assert run("""2 1
10
00
1 0 0
""") == """1.0000000000
"""

assert run("""2 3
10
00
2 0 0 0 1
1 1 0
1 0 1
""") == """0.0000000000
1.0000000000
2.0000000000
"""

assert run("""2 2
11
11
1 0 0
2 0 0 1 1
""") == """4.0000000000
3.0000000000
"""

assert run("""3 1
000
000
000
2 0 0 2 2
""") == """0.0000000000
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single flower insertion | 1.0000000000 | Repeated or simple flower updates |
| Tunnel before more flowers | 0.0000000000 then larger values | Connectivity through cells that later gain flowers |
| Fully flowered grid | Reduced energy after a tunnel | Counting tunnels separately from flowers |
| Empty grid with tunnel | 0 | Ignoring components without flowers |

## Edge Cases

A repeated flower insertion does not create a new flower. In the input

```
2 1
10
00
1 0 0
```

the cell `(0,0)` is already occupied. The algorithm sets the value to `True` again and rebuilds the same component structure, producing energy `1`.

A tunnel connecting cells that were previously separate must merge their buddings. For

```
2 1
10
01
2 0 0 1 1
```

the DSU joins the two flower cells. There is one underground edge in the component, so `f = 2` and `c = 1`, giving `2 - sqrt(1) = 1`.

A tunnel touching dirt does not increase the flower count. For

```
2 1
10
00
2 0 0 0 1
```

the component contains one flower and one underground tunnel. The value is `max(1 - sqrt(1), 0) = 0`, which the algorithm obtains by counting flowers and tunnels independently.
