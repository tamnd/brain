---
title: "CF 2127E - Ancient Tree"
description: "We are given a rooted tree. Some vertices already have fixed colors, while others are uncolored and may be assigned any color from 1..k."
date: "2026-06-08T03:17:40+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dfs-and-similar", "dsu", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2127
codeforces_index: "E"
codeforces_contest_name: "Atto Round 1 (Codeforces Round 1041, Div. 1 + Div. 2)"
rating: 2100
weight: 2127
solve_time_s: 125
verified: false
draft: false
---

[CF 2127E - Ancient Tree](https://codeforces.com/problemset/problem/2127/E)

**Rating:** 2100  
**Tags:** constructive algorithms, data structures, dfs and similar, dsu, greedy, trees  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree. Some vertices already have fixed colors, while others are uncolored and may be assigned any color from `1..k`.

A vertex `v` becomes cutie if there exists a color different from `c[v]` that appears in at least two branches of the subtree of `v`, so that two vertices of that color have LCA equal to `v`.

The cost of a coloring is the sum of weights of all cutie vertices. We must minimize that cost and output one optimal coloring.

The first difficulty is that the number of possible colorings is enormous. Even if only `10^5` vertices are uncolored, each may choose among up to `10^5` colors. Exhaustive search is impossible.

The second difficulty is that the tree size over all test cases reaches `2·10^5`. Any algorithm that examines all pairs of vertices, all pairs of colors, or repeatedly recomputes subtree information is far beyond the limit. The target complexity is roughly `O(n log n)`.

A common mistake is to focus on the final colors of all vertices. The key observation is that only the originally fixed colors matter.

Consider:

```
1(0)
├─ 2(1)
└─ 3(2)
```

No matter how vertex `1` is colored, the subtree of `1` already contains two different fixed colors. That conflict cannot be removed.

Now consider:

```
1(0)
├─ 2(1)
└─ 3(0)
```

The entire tree can be colored with color `1`, producing cost `0`.

The difference between these examples is not the uncolored vertices. It is the set of fixed colors present in the subtree.

## Approaches

A brute force solution would try every assignment of missing colors and evaluate the resulting tree.

If there are `m` uncolored vertices, this requires `k^m` colorings. Even for `m = 20`, this is already infeasible.

The next idea is to ask what information really matters.

Suppose we process a subtree rooted at `u`.

If every fixed-colored vertex inside that subtree has the same color `x`, then we may safely color every missing vertex there with `x`. No conflict is created inside the subtree or above it.

If the subtree contains no fixed-colored vertex at all, we can postpone the choice and later paint the whole region with whatever color is convenient.

The only problematic situation is when the subtree already contains at least two distinct fixed colors. Then no recoloring of the missing vertices can make those fixed colors agree.

Let

`S(u) = { fixed colors appearing in the subtree of u }`.

A crucial fact is:

A vertex contributes to the minimum possible answer exactly when `|S(u)| ≥ 2`.

If a subtree contains at least two distinct fixed colors, the conflict is unavoidable. If it contains at most one fixed color, we can paint all missing vertices consistently and avoid creating a cutie vertex there.

So the optimization problem becomes much simpler:

For every vertex, determine how many distinct fixed colors occur in its subtree.

That is a classic small-to-large merging problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Small-to-Large Merging | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the rooted tree at vertex `1`.
2. Run a DFS.
3. For each vertex, maintain a set containing all distinct fixed colors appearing in its subtree.
4. Process children first.
5. Merge child sets using the small-to-large technique. Always merge the smaller set into the larger one.
6. If the current vertex already has a fixed color, insert that color into the set.
7. After all merges, if the set size is at least `2`, add `w[u]` to the answer.
8. Store one representative color from the set. If the set is empty, store `0`.
9. Run a second DFS to construct an optimal coloring.

1. Fixed-colored vertices keep their color.
2. An uncolored vertex whose subtree contains a fixed color receives the representative color.
3. An uncolored vertex whose subtree contains no fixed color inherits its parent's color.
4. If even the root has no available color, assign color `1`.

### Why it works

The invariant is that every subtree with at most one distinct fixed color can be made monochromatic.

When `|S(u)| = 0`, the subtree contains no constraints.

When `|S(u)| = 1`, every missing vertex may be painted with that unique fixed color.

Neither case forces `u` to become cutie.

When `|S(u)| ≥ 2`, at least two different fixed colors already exist in the subtree. No assignment of missing vertices can remove that disagreement. The contribution of `u` is unavoidable.

Thus the minimum cost is exactly the sum of weights of vertices whose subtree contains at least two distinct fixed colors.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    w = [0] + list(map(int, input().split()))
    c = [0] + list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    ans = 0
    rep = [0] * (n + 1)

    def dfs(u, p):
        nonlocal ans

        cur = set()

        for v in g[u]:
            if v == p:
                continue

            child = dfs(v, u)

            if len(cur) < len(child):
                cur, child = child, cur

            cur |= child

        if c[u] != 0:
            cur.add(c[u])

        if len(cur) >= 2:
            ans += w[u]

        if cur:
            rep[u] = next(iter(cur))

        return cur

    dfs(1, 0)

    res = c[:]

    root_color = rep[1]
    if root_color == 0:
        root_color = 1

    def paint(u, p, inherited):
        if res[u] == 0:
            if rep[u]:
                res[u] = rep[u]
            else:
                res[u] = inherited

        for v in g[u]:
            if v != p:
                paint(v, u, res[u])

    paint(1, 0, root_color)

    print(ans)
    print(*res[1:])
```

The first DFS computes the set of fixed colors present in every subtree. Small-to-large merging guarantees that every color is moved only `O(log n)` times.

The second DFS constructs an explicit optimal coloring. Whenever a subtree already contains a fixed color, we reuse that color. Entire regions containing no fixed colors inherit a color from above.

The subtle point is that we never need to remember all colors during reconstruction. One representative color is enough.

## Worked Examples

### Example 1

```
1(0)
├─ 2(1)
└─ 3(2)
```

| Vertex | Fixed colors in subtree | Size | Adds cost |
| --- | --- | --- | --- |
| 2 | {1} | 1 | No |
| 3 | {2} | 1 | No |
| 1 | {1,2} | 2 | Yes |

The answer contains `w[1]`.

This example shows an unavoidable conflict.

### Example 2

```
1(0)
├─ 2(1)
└─ 3(0)
```

| Vertex | Fixed colors in subtree | Size | Adds cost |
| --- | --- | --- | --- |
| 2 | {1} | 1 | No |
| 3 | {} | 0 | No |
| 1 | {1} | 1 | No |

The entire tree can be painted color `1`.

The answer is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Small-to-large set merging |
| Space | O(n) | Tree, recursion, and stored sets |

Since the sum of `n` over all test cases is at most `2·10^5`, `O(n log n)` easily fits within the limits.

## Test Cases

```
# Minimum nontrivial tree
1
3 3
1 1 1
0 1 2
1 2
1 3

# All vertices uncolored
1
3 2
5 5 5
0 0 0
1 2
1 3

# Single fixed color everywhere
1
5 3
1 1 1 1 1
1 0 0 1 0
1 2
1 3
3 4
3 5

# Two conflicting fixed colors deep inside
1
5 3
1 2 3 4 5
0 1 2 0 0
1 2
1 3
3 4
3 5
```

| Test input | Expected output property | What it validates |
| --- | --- | --- |
| Minimum tree | Cost equals root weight | Smallest valid structure |
| All uncolored | Cost 0 | Empty color sets |
| One fixed color | Cost 0 | Monochromatic propagation |
| Two fixed colors | Conflict detected | ` |

## Edge Cases

A subtree containing no fixed-colored vertex at all is easy to mishandle. Such a subtree should not introduce a new color. The reconstruction DFS assigns it the inherited color, making the whole region monochromatic.

A subtree containing exactly one fixed color is another common source of mistakes. Every missing vertex there should be painted with that color. Creating a different color only increases the chance of generating additional cutie vertices.

The root may have no fixed color anywhere in the tree. In that case every vertex can be painted with color `1`, producing cost `0`. The reconstruction explicitly handles this case by choosing `1` as the fallback root color.
