---
title: "CF 2071C - Trapmigiano Reggiano"
description: "We are given a tree, a starting vertex st, and a target vertex en. A permutation of all vertices must be chosen. During the i-th step, a piece of cheese appears at vertex p[i]. If the mouse is already there, it stays."
date: "2026-06-08T06:51:52+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dfs-and-similar", "dp", "greedy", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2071
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1007 (Div. 2)"
rating: 1700
weight: 2071
solve_time_s: 134
verified: false
draft: false
---

[CF 2071C - Trapmigiano Reggiano](https://codeforces.com/problemset/problem/2071/C)

**Rating:** 1700  
**Tags:** constructive algorithms, data structures, dfs and similar, dp, greedy, sortings, trees  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree, a starting vertex `st`, and a target vertex `en`.

A permutation of all vertices must be chosen. During the `i`-th step, a piece of cheese appears at vertex `p[i]`. If the mouse is already there, it stays. Otherwise, it moves exactly one edge along the unique simple path toward that vertex.

The permutation determines a sequence of attractions. We must order all vertices exactly once so that after processing the entire permutation, the mouse ends up at vertex `en`.

The task is not to simulate a fixed process. We are free to choose the permutation itself.

The tree contains up to `10^5` vertices across all test cases. Since the total number of vertices is bounded by `10^5`, an `O(n log n)` or `O(n)` solution per test case is easily fast enough. Anything involving testing many permutations is impossible. Even checking all permutations of a tree with only 15 vertices would already require more than a trillion possibilities.

The most dangerous part of the problem is that the mouse only moves one edge per step. A naive strategy might try to make the mouse follow a complete path toward `en`, but later cheese placements can pull it away again.

Consider a simple chain:

```
1 - 2 - 3
st = 2
en = 2
```

If we choose permutation `[1,2,3]`, the mouse moves

```
2 -> 1 -> 2 -> 3
```

and ends at `3`, not at `2`.

Another subtle case is when the mouse passes through `en` before the last step.

```
1 - 2 - 3 - 4
st = 1
en = 4
```

The permutation `[4,1,2,3]` makes the mouse reach `4` immediately, but later attractions pull it away. Reaching `en` early is not enough. Only the final position matters.

A correct solution must guarantee the final position regardless of where the mouse currently is when the last vertices are processed.

## Approaches

A brute-force solution would generate every permutation of the vertices and simulate the mouse. For a permutation of length `n`, simulation takes `O(n)` steps. There are `n!` permutations, so the total complexity is `O(n·n!)`.

Even for `n = 15`, this is completely infeasible.

The key observation comes from looking at the tree relative to the trap vertex `en`.

Root the tree at `en`. Every vertex now has a depth equal to its distance from `en`.

Suppose we process vertices in decreasing depth order. Intuitively, we show the cheese first in the deepest parts of the tree and only later near the root.

Why is this useful?

Take any step where the cheese appears at some vertex `v`. If the mouse is not already there, it moves one edge toward `v`.

When vertices are processed from larger depth to smaller depth, every unprocessed vertex lies at depth no greater than the current one. In a rooted tree, moving toward a deeper vertex cannot move the mouse farther away from the set of already processed deeper vertices. The process gradually collapses toward the root.

The crucial fact is that the very last vertex in this ordering is `en` itself, because it is the unique vertex with depth `0`.

By the time we process the final vertex, the mouse is always located somewhere in the tree. The cheese appears at `en`, and the mouse moves one step toward `en`. The structure of the ordering guarantees that after all previous vertices have been consumed, the mouse's position coincides with the remaining active subtree containing `en`, forcing the final position to be `en`.

A more formal way to view it is through a potential function. Let `d(v)` denote depth from `en`. Processing vertices in decreasing depth ensures that after handling all vertices of depth greater than `k`, the mouse must lie inside the subtree induced by vertices of depth at most `k`. This invariant shrinks until only `en` remains.

To construct the permutation, we only need the depth of every vertex from `en`. Sorting vertices by decreasing depth immediately gives a valid answer.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|------|---|

| Brute Force | O(n·n!) | O(n) | Too slow |

| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `en`.
2. Run a DFS or BFS starting from `en` and compute the depth of every vertex.
3. Create a list containing all vertices.
4. Sort the vertices by decreasing depth.
5. Output the resulting order as the permutation.

The reason for sorting by decreasing depth is that vertices farther from the trap are processed first. Vertices closer to the trap are delayed until the end.

1. Since `en` has depth `0`, it becomes the last element of the permutation.

### Why it works

Root the tree at `en`.

For a vertex `x`, define its depth as its distance from `en`.

Consider the set of vertices that have not yet appeared in the permutation. Because we process depths from largest to smallest, this set is always connected and contains `en`.

Initially, all vertices are unprocessed.

When a vertex `v` is processed, it is one of the deepest remaining vertices. Any movement toward `v` cannot force the mouse outside the connected region formed by the remaining vertices. After removing `v` from consideration, the mouse still lies inside the remaining connected component containing `en`.

Repeating this argument after every step shows that after processing all but the last vertex, the mouse must lie inside the remaining set. The only remaining vertex is `en`, so the mouse must be at `en` when the process ends.

Thus the produced permutation always catches the mouse at the trap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, st, en = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * (n + 1)
        depth = [0] * (n + 1)

        stack = [en]
        parent[en] = 0

        while stack:
            u = stack.pop()

            for v in g[u]:
                if v == parent[u]:
                    continue

                parent[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)

        order = list(range(1, n + 1))
        order.sort(key=lambda x: depth[x], reverse=True)

        print(*order)

solve()
```

The DFS computes distances from `en`, which become the depths in the rooted tree.

The parent array prevents traversing edges back toward the parent. Since the graph is a tree, this is sufficient to visit every vertex exactly once.

After depths are known, the only remaining task is sorting. Vertices farther from `en` appear earlier in the permutation. Because `en` has depth `0`, it naturally becomes the last element.

No special handling is required for `st`. The construction works for every starting position.

An easy mistake is rooting the tree at `st` instead of `en`. The correctness argument depends entirely on distances from the trap vertex. Using any other root breaks the proof.

Another common mistake is sorting in increasing depth order. That places `en` first instead of last and generally fails.

## Worked Examples

### Example 1

```
n = 3
st = 2
en = 2

1 - 2 - 3
```

Depths from `en = 2`:

| Vertex | Depth |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |

Sorted by decreasing depth:

```
[1, 3, 2]
```

Mouse simulation:

| Step | Cheese | Mouse Before | Mouse After |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1 |
| 2 | 3 | 1 | 2 |
| 3 | 2 | 2 | 2 |

Final position is `2 = en`.

This example shows that the mouse may move away from the trap and return later.

### Example 2

```
n = 6
st = 1
en = 4

Edges:
1-2
1-3
1-4
4-5
5-6
```

Depths from `4`:

| Vertex | Depth |
| --- | --- |
| 4 | 0 |
| 1 | 1 |
| 5 | 1 |
| 2 | 2 |
| 3 | 2 |
| 6 | 2 |

One valid ordering:

```
[2, 3, 6, 1, 5, 4]
```

Simulation:

| Step | Cheese | Mouse Before | Mouse After |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 2 |
| 2 | 3 | 2 | 1 |
| 3 | 6 | 1 | 4 |
| 4 | 1 | 4 | 1 |
| 5 | 5 | 1 | 4 |
| 6 | 4 | 4 | 4 |

The mouse reaches the trap several times during the process, but only the final position matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | DFS is O(n), sorting dominates |
| Space | O(n) | Adjacency list, depth array, parent array |

The sum of all `n` values is at most `10^5`. Sorting `10^5` vertices and performing one DFS per test case easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    t = int(input())

    for _ in range(t):
        n, st, en = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * (n + 1)
        depth = [0] * (n + 1)

        stack = [en]
        parent[en] = 0

        while stack:
            u = stack.pop()

            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)

        order = list(range(1, n + 1))
        order.sort(key=lambda x: depth[x], reverse=True)

        out.append(" ".join(map(str, order)))

    return "\n".join(out)

# minimum tree
assert run("""1
1 1 1
""") == "1"

# single edge
assert run("""1
2 1 2
1 2
""") == "1 2"

# chain
assert run("""1
3 2 2
1 2
2 3
""") == "1 3 2"

# star centered at trap
assert run("""1
4 2 1
1 2
1 3
1 4
""").split()[-1] == "1"

# long chain, trap at one endpoint
assert run("""1
5 3 1
1 2
2 3
3 4
4 5
""") == "5 4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `1` | Smallest possible tree |
| Two vertices | `1 2` | Basic movement |
| Chain with trap in middle | `1 3 2` | Equal-depth vertices |
| Star centered at trap | Trap appears last | Root handling |
| Long chain | Reverse order | Maximum depth ordering |

## Edge Cases

### Tree with a single vertex

Input:

```
1
1 1 1
```

The DFS assigns depth `0` to vertex `1`.

The sorted order is simply:

```
[1]
```

The mouse starts and ends at the trap.

### Trap equals starting vertex

Input:

```
1
3 2 2
1 2
2 3
```

Depths are:

```
1 -> 1
3 -> 1
2 -> 0
```

The permutation ends with `2`.

Even though the mouse starts at the trap, earlier cheese appearances may move it away. The final appearance at `2` guarantees the process finishes correctly.

### Trap is a leaf

Input:

```
1
4 1 4
1 2
2 3
3 4
```

Depths from `4`:

```
1 -> 3
2 -> 2
3 -> 1
4 -> 0
```

The permutation becomes:

```
[1, 2, 3, 4]
```

The trap still appears last. The proof depends only on depths from `en`, not on the shape of the tree.

### Multiple vertices at the same depth

Input:

```
1
5 1 3
3 1
3 2
3 4
3 5
```

All leaves have depth `1`.

Any ordering among those leaves is valid because the correctness proof only requires non-increasing depth. Equal-depth vertices may appear in any order.
