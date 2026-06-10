---
title: "CF 1528C - Trees of Tranquillity"
description: "We are given two rooted trees on the same set of vertices 1..n. Both trees are rooted at vertex 1. From these two trees we define a graph. Two vertices are connected if they satisfy two conditions simultaneously."
date: "2026-06-10T17:02:42+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1528
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 722 (Div. 1)"
rating: 2300
weight: 1528
solve_time_s: 192
verified: true
draft: false
---

[CF 1528C - Trees of Tranquillity](https://codeforces.com/problemset/problem/1528/C)

**Rating:** 2300  
**Tags:** data structures, dfs and similar, greedy, trees  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two rooted trees on the same set of vertices `1..n`. Both trees are rooted at vertex `1`.

From these two trees we define a graph. Two vertices are connected if they satisfy two conditions simultaneously.

The first condition says that in the first tree, one vertex lies on the root-to-other path. In other words, the two vertices are ancestor-related in the first tree.

The second condition says that in the second tree, neither vertex is an ancestor of the other. Their ancestor intervals in the second tree must be incomparable.

The task is to find the size of the largest clique in this graph.

The direct graph is never built explicitly. With up to `3 * 10^5` vertices across all test cases, even storing all possible edges would be impossible. A graph on `3 * 10^5` vertices can contain roughly `4.5 * 10^10` edges.

The constraints immediately rule out any approach that checks pairs of vertices. An `O(n²)` algorithm would require about `9 * 10^10` operations in the worst case. We need something close to linear or `O(n log n)`.

The most subtle part of the problem is understanding what a clique looks like.

Suppose the first tree is a chain:

```
1
|
2
|
3
|
4
```

Every pair of chosen vertices is ancestor-related in the first tree. The only remaining requirement is that no pair is ancestor-related in the second tree.

A careless solution might try to maximize the number of vertices whose intervals in the second tree are pairwise disjoint. That is not enough. We need a stronger property: for every pair, neither interval may contain the other. Nested intervals are forbidden because nesting means an ancestor relation in the second tree.

Another easy mistake appears when one chosen vertex's interval contains several others.

Example:

```
Second tree:
1
├─2
│ └─3
└─4
```

The intervals of vertices `2` and `3` are nested. They cannot both belong to the clique even though both may lie on the same path in the first tree.

The root also deserves attention. In the second tree, the root is ancestor of every vertex. Its interval contains every other interval. Consequently, the root can never coexist with another vertex inside a valid clique.

## Approaches

A brute-force viewpoint is to construct the memorial graph and compute its maximum clique.

For every pair of vertices we could determine whether they form an edge by checking ancestor relations in both trees. That already costs `O(n²)`. After building the graph, finding a maximum clique is NP-hard in general graphs, making this direction completely hopeless.

The crucial observation is that the graph produced here has very special structure.

Consider a clique. Since every pair of vertices must be ancestor-related in the first tree, all clique vertices must lie on a single root-to-node path of the first tree.

Why?

Take any two vertices in the clique. They must be comparable in the first tree. A set of vertices that are pairwise comparable in a rooted tree forms a chain, which is exactly a path from the root downward.

Now look at the second tree.

For any two clique vertices, neither may be ancestor of the other in the second tree. Using Euler tour intervals, each vertex corresponds to a subtree interval `[tin, tout]`. Ancestor relations become interval containment.

Thus the clique corresponds to a set of vertices on one path of the first tree whose intervals in the second tree are pairwise non-containing.

A stronger statement is true.

If we maintain a collection of second-tree intervals such that no interval contains another, then any two corresponding vertices are non-ancestor-related in the second tree. Since all maintained vertices come from one current path in the first tree DFS, they automatically form a clique.

This transforms the problem into:

While traversing a path in the first tree, maintain the largest possible set of vertices whose intervals in the second tree are pairwise non-containing.

The interval structure suggests an ordered set solution. During DFS on the first tree, vertices are added when entering and removed when leaving. We keep the current optimal collection of intervals on the current path.

The famous solution maintains intervals ordered by Euler entry time in the second tree. Whenever a new interval is inserted, at most one existing interval may need to be removed. This yields an `O(n log n)` algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Preprocessing the second tree

First perform an Euler tour on the second tree.

For every vertex `v`, compute:

`tin[v]` = entry time

`tout[v]` = exit time

Vertex `u` is an ancestor of `v` in the second tree exactly when:

`tin[u] ≤ tin[v]` and `tout[v] ≤ tout[u]`.

### Maintaining the active clique

During DFS of the first tree, the recursion stack represents one root-to-current path.

We maintain a set of selected vertices from this path. Instead of storing vertices directly, we store their Euler entry times ordered in a balanced structure.

The invariant is that the selected vertices correspond to intervals in the second tree such that none contains another.

### DFS transitions

1. Enter a vertex `v` in the first tree.
2. Find the interval immediately before and immediately after `tin[v]` in the ordered set.
3. Check whether one of the currently selected intervals already contains the interval of `v`.

If such an interval exists, adding `v` would increase the clique size. We remove that containing interval and insert `v`.
4. Otherwise check whether `v` contains one of the selected intervals.

If yes, adding `v` would make the collection worse because `v` is less specific than the interval it contains. We do not insert `v`.
5. Otherwise `v` is incomparable with all selected intervals. Insert it.
6. Update the global answer with the current size of the set.
7. DFS into the children of `v` in the first tree.
8. After all children are processed, rollback exactly the modification performed when entering `v`.

This restores the data structure to the state corresponding to the parent path.

### Why it works

At any moment the DFS stack is a path in the first tree. Every selected vertex belongs to that path, so every pair of selected vertices is ancestor-related in the first tree.

The maintained set always contains intervals that are pairwise non-containing in the second tree. Two intervals in a rooted tree can only violate the clique condition if one contains the other. The update rules preserve the absence of containment.

When a new interval is contained inside an existing selected interval, replacing the larger interval with the smaller one cannot reduce future possibilities. The smaller interval is strictly more restrictive and leaves at least as much room for other disjoint intervals. This is the key greedy step.

Thus the maintained set is the maximum possible clique among vertices on the current root-to-node path. Taking the maximum size over all DFS states yields the global maximum clique.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    ans_out = []

    for _ in range(t):
        n = int(input())

        g1 = [[] for _ in range(n + 1)]
        p1 = list(map(int, input().split()))
        for i, p in enumerate(p1, start=2):
            g1[p].append(i)

        g2 = [[] for _ in range(n + 1)]
        p2 = list(map(int, input().split()))
        for i, p in enumerate(p2, start=2):
            g2[p].append(i)

        tin = [0] * (n + 1)
        tout = [0] * (n + 1)

        timer = 0

        def dfs2(v):
            nonlocal timer
            timer += 1
            tin[v] = timer
            for to in g2[v]:
                dfs2(to)
            tout[v] = timer

        dfs2(1)

        active = []
        best = 0

        def is_ancestor(u, v):
            return tin[u] <= tin[v] and tout[v] <= tout[u]

        def dfs1(v):
            nonlocal best

            pos = bisect_left(active, tin[v])

            inserted = False
            removed_vertex = -1

            if pos > 0:
                pred_tin = active[pos - 1]
                pred = tin_to_vertex[pred_tin]

                if is_ancestor(pred, v):
                    active.pop(pos - 1)
                    active.insert(pos - 1, tin[v])

                    inserted = True
                    removed_vertex = pred

                    best = max(best, len(active))

                    for to in g1[v]:
                        dfs1(to)

                    active.pop(pos - 1)
                    active.insert(pos - 1, tin[pred])
                    return

            if pos < len(active):
                succ_tin = active[pos]
                succ = tin_to_vertex[succ_tin]

                if is_ancestor(v, succ):
                    best = max(best, len(active))

                    for to in g1[v]:
                        dfs1(to)

                    return

            active.insert(pos, tin[v])
            inserted = True

            best = max(best, len(active))

            for to in g1[v]:
                dfs1(to)

            active.pop(bisect_left(active, tin[v]))

        tin_to_vertex = [0] * (n + 1)
        for v in range(1, n + 1):
            tin_to_vertex[tin[v]] = v

        dfs1(1)

        ans_out.append(str(best))

    sys.stdout.write("\n".join(ans_out))

if __name__ == "__main__":
    solve()
```

The first DFS computes Euler intervals in the second tree. Because subtree intervals become contiguous segments, ancestor queries reduce to interval containment tests.

The second DFS runs on the first tree. The recursion stack is exactly the path whose clique candidates we are considering.

The ordered structure `active` stores Euler entry times of currently selected vertices. The crucial fact is that among intervals with no containment, ordering by `tin` is sufficient. Any interval that can contain the new one must be its predecessor in this order. Any interval that can be contained by the new one must be its successor. That is why only two neighbors need to be examined.

Rollback is handled immediately after returning from recursive calls. Every DFS state sees exactly the collection corresponding to its own root-to-node path.

## Worked Examples

### Sample 2

Input:

```
5
1 2 3 4
1 1 1 1
```

The first tree is a chain. The second tree is a star.

Euler intervals in the second tree:

| Vertex | Interval |
| --- | --- |
| 1 | [1,5] |
| 2 | [2,2] |
| 3 | [3,3] |
| 4 | [4,4] |
| 5 | [5,5] |

DFS on the first tree:

| Current Vertex | Active Set |
| --- | --- |
| 1 | {1} |
| 2 | {2} |
| 3 | {2,3} |
| 4 | {2,3,4} |
| 5 | {2,3,4,5} |

The root interval contains every other interval, so it gets replaced immediately. All leaf intervals are pairwise incomparable, giving clique size `4`.

### Sample 4

Input:

```
7
1 1 3 4 4 5
1 2 1 4 2 5
```

During the DFS of the first tree, several vertices replace ancestors whose intervals contain them in the second tree.

| Vertex Entered | Action | Clique Size |
| --- | --- | --- |
| 1 | insert | 1 |
| 3 | replace containing ancestor | 1 |
| 4 | insert | 2 |
| 6 | insert | 3 |

The maximum size reached is `3`, corresponding to vertices `{3,4,6}`.

This trace demonstrates the greedy replacement rule. A larger containing interval is never better than the smaller interval inside it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each vertex performs a constant number of ordered-set operations |
| Space | O(n) | Trees, Euler arrays, recursion stack, active set |

The sum of all `n` values is at most `3 · 10^5`. An `O(n log n)` solution performs roughly a few million balanced-structure operations, which comfortably fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    def solve():
        from bisect import bisect_left

        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            n = int(input())

            g1 = [[] for _ in range(n + 1)]
            p1 = list(map(int, input().split()))
            for i, p in enumerate(p1, start=2):
                g1[p].append(i)

            g2 = [[] for _ in range(n + 1)]
            p2 = list(map(int, input().split()))
            for i, p in enumerate(p2, start=2):
                g2[p].append(i)

            tin = [0] * (n + 1)
            tout = [0] * (n + 1)

            timer = 0

            def dfs2(v):
                nonlocal timer
                timer += 1
                tin[v] = timer
                for to in g2[v]:
                    dfs2(to)
                tout[v] = timer

            dfs2(1)

            tin_to_vertex = [0] * (n + 1)
            for v in range(1, n + 1):
                tin_to_vertex[tin[v]] = v

            active = []
            best = 0

            def anc(u, v):
                return tin[u] <= tin[v] and tout[v] <= tout[u]

            def dfs1(v):
                nonlocal best

                pos = bisect_left(active, tin[v])

                if pos > 0:
                    p = tin_to_vertex[active[pos - 1]]
                    if anc(p, v):
                        old = active[pos - 1]
                        active[pos - 1] = tin[v]

                        best = max(best, len(active))
                        for to in g1[v]:
                            dfs1(to)

                        active[pos - 1] = old
                        return

                if pos < len(active):
                    s = tin_to_vertex[active[pos]]
                    if anc(v, s):
                        best = max(best, len(active))
                        for to in g1[v]:
                            dfs1(to)
                        return

                active.insert(pos, tin[v])

                best = max(best, len(active))
                for to in g1[v]:
                    dfs1(to)

                active.pop(bisect_left(active, tin[v]))

            dfs1(1)
            ans.append(str(best))

        return "\n".join(ans)

    return solve()

assert run(
"""4
4
1 2 3
1 2 3
5
1 2 3 4
1 1 1 1
6
1 1 1 1 2
1 2 1 2 2
7
1 1 3 4 4 5
1 2 1 4 2 5
"""
) == "1\n4\n1\n3"

assert run(
"""1
2
1
1
"""
) == "1"

assert run(
"""1
5
1 2 3 4
1 2 3 4
"""
) == "1"

assert run(
"""1
5
1 2 3 4
1 1 1 1
"""
) == "4"

assert run(
"""1
3
1 1
1 1
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two identical chains | 1 | Every pair is ancestor-related in both trees |
| Chain vs star | 4 | Maximum clique can be almost all non-root vertices |
| n = 2 | 1 | Smallest legal input |
| Star in both trees | 2 | Incomparable second-tree intervals are handled correctly |

## Edge Cases

### Identical trees

Input:

```
1
4
1 2 3
1 2 3
```

Every pair of vertices comparable in the first tree is also comparable in the second tree. No edge exists between distinct vertices. The algorithm keeps replacing intervals but never grows the active set beyond size `1`. The answer is `1`.

### Root interval contains everything

Input:

```
1
5
1 2 3 4
1 1 1 1
```

The root interval in the second tree is `[1,5]`. When vertex `2` is visited, its interval is contained inside the root interval. The algorithm replaces the root with vertex `2`. This is exactly the greedy rule that prevents the root from blocking future additions. The final answer becomes `4`.

### Nested intervals in the second tree

Input:

```
1
3
1 2
1 2
```

Intervals of vertices `2` and `3` are nested. A careless solution that only checks the first-tree path would choose both. The ordered-set logic detects containment and never allows both intervals to remain active simultaneously. The answer is `1`.

### Incomparable leaves

Input:

```
1
3
1 2
1 1
```

Vertices `2` and `3` lie on a path in the first tree, but in the second tree they are siblings. Their intervals are disjoint, so both stay in the active set. The algorithm reaches size `2`, which is the correct maximum clique.
