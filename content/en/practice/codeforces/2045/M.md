---
title: "CF 2045M - Mirror Maze"
description: "Think of the laser beam as moving along the grid lines between cells. Whenever the beam enters a cell through one side, the content of that cell determines which side it leaves from. An empty cell does not change direction."
date: "2026-06-08T09:20:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2045
codeforces_index: "M"
codeforces_contest_name: "2024-2025 ICPC Asia Jakarta Regional Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1800
weight: 2045
solve_time_s: 94
verified: true
draft: false
---

[CF 2045M - Mirror Maze](https://codeforces.com/problemset/problem/2045/M)

**Rating:** 1800  
**Tags:** brute force, dfs and similar, graphs, implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the laser beam as moving along the grid lines between cells. Whenever the beam enters a cell through one side, the content of that cell determines which side it leaves from.

An empty cell does not change direction. A `/` mirror turns the beam by 90 degrees in one way, and a `\` mirror turns it by 90 degrees in the other way.

A laser is placed outside the grid on one of the boundary openings. After entering the grid, the beam follows a deterministic path until it eventually leaves the grid again.

We must find every boundary opening whose beam hits every mirror cell in the grid at least once.

The grid dimensions are at most 200 × 200. There are only `2(R + C)` possible laser positions, which is at most 800. A straightforward simulation from every boundary is possible, but we must be careful about how much work is done per simulation.

The subtle part is understanding what "hit every mirror" means. A mirror is hit whenever the beam enters that cell and reflects on that mirror. We do not care how many times it is hit.

A common mistake is to simulate from each boundary independently and count visited mirrors. That works, but it ignores a stronger structural property of the maze.

Another easy mistake is to assume that different entrances produce unrelated paths. In fact, every beam path is part of a fixed graph determined entirely by the grid. Once that graph is built, all answers can be extracted almost immediately.

Consider this small example:

```
1 1
/
```

The only mirror is touched by all four possible entrances, so the answer contains all four boundary positions.

A solution that only tracks cells instead of beam states can fail, because entering the same cell from different directions can lead to different continuations.

## Approaches

The brute-force idea is straightforward. For every boundary entrance, simulate the beam until it leaves the grid. During the simulation, mark every mirror touched. If all mirrors were touched, record that entrance.

A beam can visit at most `O(RC)` states because a state is determined by a cell and a direction. There are `O(R + C)` entrances. The total complexity becomes `O((R + C)RC)`.

With `R = C = 200`, this is roughly

```
800 × 40000 = 32,000,000
```

state transitions.

That is not absurdly large, but there is a cleaner observation.

The beam's movement is completely deterministic. Every side of every cell is connected to exactly one other side. This means the entire maze is really a collection of connected path components.

Instead of tracing every laser separately, we can build those components once.

Represent every cell side as a node.

Inside a cell, the content determines which sides are connected:

For an empty cell:

```
N <-> S
W <-> E
```

For `/`:

```
N <-> W
S <-> E
```

For `\`:

```
N <-> E
S <-> W
```

Adjacent cells also connect through their common border.

After all connections are added, every node belongs to some DSU component.

Now consider a mirror cell.

A beam hits that mirror iff its path enters one of the two component branches that pass through the mirror. We can count, for every component, how many mirrors are reachable from that component.

If a boundary opening belongs to a component that can reach all mirrors, then that opening is a valid answer.

This reduces the whole problem to one DSU construction plus a counting pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((R+C)RC) | O(RC) | Too slow conceptually, unnecessary |
| Optimal | O(RC α(RC)) | O(RC) | Accepted |

## Algorithm Walkthrough

1. Create a DSU node for every side of every cell.
2. Connect cell sides according to the cell content.

For an empty cell, connect north with south and west with east.

For a `/` mirror, connect north with west and south with east.

For a `\` mirror, connect north with east and south with west.
3. Use a numbering scheme where two neighboring cells automatically share the same border node.

This models movement across cell boundaries without adding extra edges later.
4. After all unions are performed, every DSU component represents one maximal beam trajectory component.
5. Let `tot` be the total number of mirrors.
6. For every mirror cell, determine the two DSU components corresponding to the two sides of that mirror.

For `/`, the mirror separates `(N,W)` from `(S,E)`.

For `\`, the mirror separates `(N,E)` from `(S,W)`.

A beam belonging to either side can hit that mirror.
7. For each mirror, add one count to both relevant DSU components.

If both sides belong to the same component, add only once.
8. For every boundary opening, find its DSU component.
9. If that component's count equals `tot`, then every mirror is reachable from that entrance, so record the corresponding answer string.

### Why it works

A DSU component represents all beam states connected by deterministic movement rules.

For a particular mirror, a beam can hit it only if the beam belongs to one of the two trajectory components touching that mirror. During the counting step, we register that mirror for exactly those components.

After processing all mirrors, `cnt[component]` equals the number of distinct mirrors that can be hit by any beam state inside that component.

A boundary entrance belongs to exactly one component. Its beam can hit every mirror iff that component is associated with every mirror. That is precisely the condition

```
cnt[component] = total number of mirrors.
```

So every reported entrance is valid, and every valid entrance is reported.

## Python Solution

```python
import sys
input = sys.stdin.readline

R, C = map(int, input().split())
grid = [input().strip() for _ in range(R)]

MAXN = 100000

parent = list(range(MAXN))
cnt = [0] * MAXN

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra = find(a)
    rb = find(b)
    if ra != rb:
        parent[ra] = rb

# directions:
# 1 = N, 2 = S, 3 = W, 4 = E
def node(i, j, d):
    if d == 1:
        return (i - 1) * C + j
    if d == 2:
        return i * C + j
    return (R + 1) * C + (i - 1) * (C + 1) + j + (1 if d == 4 else 0)

for i in range(1, R + 1):
    for j in range(1, C + 1):
        ch = grid[i - 1][j - 1]

        if ch == '.':
            union(node(i, j, 1), node(i, j, 2))
            union(node(i, j, 3), node(i, j, 4))
        elif ch == '/':
            union(node(i, j, 1), node(i, j, 3))
            union(node(i, j, 2), node(i, j, 4))
        else:  # '\'
            union(node(i, j, 1), node(i, j, 4))
            union(node(i, j, 2), node(i, j, 3))

total_mirrors = 0

for i in range(1, R + 1):
    for j in range(1, C + 1):
        ch = grid[i - 1][j - 1]

        if ch == '.':
            continue

        total_mirrors += 1

        if ch == '/':
            a = find(node(i, j, 1))
            b = find(node(i, j, 2))
        else:
            a = find(node(i, j, 1))
            b = find(node(i, j, 3))

        cnt[a] += 1
        if a != b:
            cnt[b] += 1

ans = []

for r in range(1, R + 1):
    if cnt[find(node(r, 1, 3))] == total_mirrors:
        ans.append(f"W{r}")

for r in range(1, R + 1):
    if cnt[find(node(r, C, 4))] == total_mirrors:
        ans.append(f"E{r}")

for c in range(1, C + 1):
    if cnt[find(node(1, c, 1))] == total_mirrors:
        ans.append(f"N{c}")

for c in range(1, C + 1):
    if cnt[find(node(R, c, 2))] == total_mirrors:
        ans.append(f"S{c}")

print(len(ans))
if ans:
    print(*ans)
```

The numbering function is the key implementation detail. Instead of creating separate nodes for every cell side and then explicitly connecting neighboring cells, the numbering scheme assigns the same ID to both sides of a shared border. That automatically models movement between adjacent cells.

The counting phase is also subtle. A mirror contributes to two trajectory components. If both sides happen to belong to the same DSU component, we must count the mirror only once for that component.

Boundary openings correspond directly to outer border segments. The four final loops simply test those border nodes.

## Worked Examples

### Example 1

```
1 1
/
```

There is one mirror.

| Mirror | Component A | Component B |
| --- | --- | --- |
| (1,1) '/' | N/W side | S/E side |

Both components receive count `1`.

| Entrance | Component Count | Valid |
| --- | --- | --- |
| N1 | 1 | Yes |
| S1 | 1 | Yes |
| W1 | 1 | Yes |
| E1 | 1 | Yes |

Output:

```
4
N1 S1 W1 E1
```

This demonstrates that a single mirror can be reachable from multiple independent boundary entrances.

### Example 2

```
2 2
..
./
```

Total mirrors = 1.

After DSU construction, some boundary openings belong to components that never reach the mirror. Their component count remains zero.

| Entrance | Component Count | Valid |
| --- | --- | --- |
| N1 | 0 | No |
| N2 | 1 | Yes |
| W2 | 1 | Yes |
| S1 | 0 | No |

Only entrances whose component sees the mirror are accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC α(RC)) | Each union/find operation is nearly constant |
| Space | O(RC) | DSU nodes and mirror counts |

The grid contains at most 40,000 cells. The number of DSU nodes is proportional to the number of grid borders, which is also `O(RC)`. This easily fits within both the 1 second time limit and the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    # paste solution into a solve() function and call it
    pass

# sample 1
# output order is not unique, so real judging should compare sets

# single mirror
inp = """\
1 1
/
"""

# every entrance hits the only mirror
# expected count = 4

# minimum size with backslash mirror
inp2 = """\
1 1
\\
"""

# all entrances valid again

# mirror isolated from some boundaries
inp3 = """\
2 2
..
./
"""

# no mirrors except one corner mirror

# large empty grid except one mirror
inp4 = "200 200\n" + ("." * 199 + "/\n") + ("." * 200 + "\n") * 199
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` with `/` | 4 answers | Minimum grid |
| `1×1` with `\` | 4 answers | Mirror orientation handling |
| Single corner mirror | Partial set of entrances | Boundary mapping |
| `200×200` grid | Finishes quickly | Maximum constraints |

## Edge Cases

Consider

```
1 1
/
```

The mirror's two sides belong to different DSU components. The algorithm increments both component counters. Every boundary opening belongs to one of those two components, so all four entrances are reported.

Consider

```
1 1
\
```

The mirror partition changes, but the counting logic is identical. The algorithm does not rely on geometric simulation, only on the component structure, so both mirror orientations are handled uniformly.

Consider

```
2 2
..
./
```

Several boundary openings belong to components that never touch the mirror. Their component count remains zero, while components touching the mirror receive count one. The final equality test against the total number of mirrors filters them out automatically.

The most subtle case is when both sides of a mirror belong to the same DSU component. The implementation checks `if a != b` before adding the second count. Without that condition, a mirror would be counted twice and some valid entrances would be rejected.
