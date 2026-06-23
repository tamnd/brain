---
title: "CF 105064E - Color Conundrum"
description: "We are working with a rooted tree where each vertex carries a color label. The root is fixed at vertex 1. On this tree, we must support two operations over time: recoloring a single vertex, and querying how many vertices of a given color exist inside a particular subtree."
date: "2026-06-23T10:01:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105064
codeforces_index: "E"
codeforces_contest_name: "ICPC-de-Tryst 2024"
rating: 0
weight: 105064
solve_time_s: 83
verified: false
draft: false
---

[CF 105064E - Color Conundrum](https://codeforces.com/problemset/problem/105064/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a rooted tree where each vertex carries a color label. The root is fixed at vertex 1. On this tree, we must support two operations over time: recoloring a single vertex, and querying how many vertices of a given color exist inside a particular subtree.

A subtree here means all vertices whose path to the root passes through a given vertex. So every query is essentially asking: if we look at the connected “descendant region” of a node, how many nodes currently have color x?

The input is dynamic because colors change between queries. That immediately rules out any solution that recomputes subtree statistics from scratch per query, since updates break any precomputed static answers.

The constraints are tight in aggregate: across all test cases, the total number of vertices and queries is up to 2×10^5. This means any solution should behave close to linear or log-linear per operation. Anything like recomputing DFS results per query or scanning subtrees directly will exceed limits.

A subtle edge case appears when many nodes share the same color and updates repeatedly flip colors in a dense region. For example, consider a chain of 200000 nodes all initially color 1. If we query subtree counts naively for each node, every query degenerates into scanning O(n), which becomes catastrophic.

Another subtle failure case is forgetting that subtree membership is structural, not value-based. Two nodes with identical colors are not interchangeable unless they are inside the same subtree; mixing these notions leads to incorrect counting.

## Approaches

A direct way to answer a query is to traverse the subtree of the given node using DFS or BFS and count how many nodes match the queried color. This is correct because it explicitly examines exactly the required vertices. However, each query may touch O(n) nodes, and with up to 2×10^5 queries, this leads to O(nq) behavior in the worst case, which is far beyond feasible limits.

The key observation is that subtree queries become much simpler if we flatten the tree into an array using an Euler tour. Every subtree corresponds to a contiguous segment in this traversal order. This transforms the problem into maintaining a dynamic array where we need to support point updates and frequency queries over a range.

At this point, we need a data structure that can answer: how many times does a value appear in a segment, with updates changing a single position’s value. A natural structure for this is a map from color to a sorted set or a Fenwick tree per color, but maintaining a Fenwick tree per color is too expensive in memory.

Instead, we reverse the perspective: instead of tracking positions per color, we track colors per position using a structure that can aggregate counts efficiently. The standard solution is to maintain, for each color, an ordered set of Euler positions. Then each query reduces to counting how many positions of that color lie inside a given interval, which can be answered using binary search.

Updates become removal from one set and insertion into another. Both operations are O(log n), and queries are also O(log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | O(nq) | O(n) | Too slow |
| Euler tour + per-color ordered sets | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the tree and root it at node 1. We need a deterministic traversal order so that every subtree becomes a contiguous interval.
2. Run a DFS to assign each node an entry time tin[v] and optionally a subtree range [tin[v], tout[v]]. The DFS order ensures that all descendants of v lie in a continuous segment. This is the core transformation that replaces tree structure with an array structure.
3. Maintain a dictionary mapping each color to a sorted container of Euler positions where that color currently appears. Initially, insert tin[v] into the set corresponding to c[v].
4. For a type 2 query (v, x), interpret the subtree of v as the interval [tin[v], tout[v]]. The answer is the number of elements in the set of color x that fall inside this interval. This is computed using binary search: upper_bound(tout[v]) minus lower_bound(tin[v]).
5. For a type 1 update (v, x), we must reflect the color change. Remove tin[v] from the set of the old color and insert it into the set of the new color. Then update the stored color of v.

The correctness depends on always keeping the sets synchronized with the current coloring.

### Why it works

The DFS ordering guarantees that subtree(v) corresponds exactly to a contiguous interval in Euler time. Each node appears exactly once in this ordering, so storing nodes by their tin index is equivalent to storing them in a linearized representation of the tree. Each color set therefore represents the exact set of positions where that color occurs in the array, and every subtree query becomes a range counting problem over that array. Since updates only move a single element between sets, the structure remains consistent at all times.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    c = [0] + list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 0

    stack = [(1, 0, 0)]  # node, parent, state (0 enter, 1 exit)
    while stack:
        v, p, state = stack.pop()
        if state == 0:
            timer += 1
            tin[v] = timer
            stack.append((v, p, 1))
            for to in g[v]:
                if to != p:
                    stack.append((to, v, 0))
        else:
            tout[v] = timer

    from collections import defaultdict
    import bisect

    pos = defaultdict(list)

    for i in range(1, n + 1):
        pos[c[i]].append(tin[i])

    for k in pos:
        pos[k].sort()

    def count(color, l, r):
        arr = pos.get(color, [])
        return bisect.bisect_right(arr, r) - bisect.bisect_left(arr, l)

    for _ in range(q):
        t, v, x = map(int, input().split())
        if t == 1:
            old = c[v]
            if old == x:
                continue
            old_arr = pos[old]
            idx = bisect.bisect_left(old_arr, tin[v])
            if idx < len(old_arr) and old_arr[idx] == tin[v]:
                old_arr.pop(idx)

            bisect.insort(pos[x], tin[v])
            c[v] = x
        else:
            print(count(x, tin[v], tout[v]))

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The DFS-to-Euler conversion is implemented iteratively to avoid recursion depth issues. Each node receives a unique entry time, and subtree boundaries are derived from these times.

The color-to-positions map is implemented using lists kept sorted. Queries use binary search to compute range counts efficiently.

The update step carefully removes the old position before inserting the new one, ensuring consistency. A common mistake is forgetting to update the color array `c[v]`, which would desynchronize future updates.

## Worked Examples

Consider a small tree:

Input:

```
1
5 4
1 2 1 2 3
1 2
1 3
3 4
3 5
2 1 1
1 5 1
2 1 1
2 3 2
```

After Euler traversal, suppose tin order is:

1→1, 2→2, 3→3, 4→4, 5→5.

Initial color positions:

Color 1: [1, 3]

Color 2: [2, 4]

Color 3: [5]

First query asks subtree of 1 for color 1.

| Step | Operation | Color sets | Answer |
| --- | --- | --- | --- |
| 1 | query (1,1) | {1:[1,3],2:[2,4],3:[5]} | 2 |

Second operation changes node 5 from 3 to 1.

| Step | Operation | Color sets |
| --- | --- | --- |
| 1 | move 5: 3→1 | 1:[1,3,5], 3:[], 2:[2,4] |

Third query asks subtree of 1 for color 1.

| Step | Operation | Answer |
| --- | --- | --- |
| 1 | query (1,1) | 3 |

Final query asks subtree of 3 for color 2, which corresponds to nodes 3,4,5 depending on structure.

This demonstrates how updates propagate only locally in the color sets while subtree queries remain range checks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update performs one removal and one insertion in sorted lists, each O(log n), and each query performs two binary searches |
| Space | O(n) | Each node contributes exactly one entry in a color list |

The complexity fits comfortably within limits since the total number of operations across all test cases is bounded by 2×10^5, and logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue().strip()

# minimum case
assert run("""1
1 2
5
1 1 1
2 1 5
""") == "1"

# small tree, no updates
assert run("""1
3 2
1 2 3
1 2
1 3
2 1 1
2 2 2
""") == "1\n0"

# update flips same color back and forth
assert run("""1
3 4
1 2 3
1 2
1 3
2 1 2
1 2 3
2 1 2
2 1 3
""") == "1\n0\n1"

# star tree heavy subtree query
assert run("""1
5 2
1 1 1 2 2
1 2
1 3
1 4
1 5
2 1 1
2 1 2
""") == "3\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | base correctness |
| small static tree | 1,0 | subtree range mapping |
| flip updates | mixed | dynamic consistency |
| star tree | 3,2 | large subtree aggregation |

## Edge Cases

A subtle case arises when an update assigns the same color that the node already has. In that situation, removing and reinserting would corrupt the structure if not guarded. The implementation explicitly skips work when old and new colors match, preserving set integrity.

Another case is deep chains where subtree ranges are large contiguous segments. Without Euler flattening, these queries would degenerate into full scans; here they reduce to a simple interval count, so even a path of 200000 nodes remains efficient.

Finally, repeated updates on the same node stress the correctness of removal logic. Since positions are stored uniquely in each color list, failing to delete the exact tin index would accumulate duplicates and inflate answers. The binary search removal ensures the list always reflects the true current state of the tree.
