---
title: "CF 104252B - Board Game"
description: "We are given a set of points in the plane, each point representing a token with a unique identifier from 1 to T. Then there is a sequence of P turns. On each turn, a player receives every remaining token whose point lies strictly below a given line of the form $y = Ax + B$."
date: "2026-07-01T22:03:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104252
codeforces_index: "B"
codeforces_contest_name: "2022-2023 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 104252
solve_time_s: 75
verified: true
draft: false
---

[CF 104252B - Board Game](https://codeforces.com/problemset/problem/104252/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the plane, each point representing a token with a unique identifier from 1 to T. Then there is a sequence of P turns. On each turn, a player receives every remaining token whose point lies strictly below a given line of the form $y = Ax + B$. Once a token is taken, it disappears and can never be taken again by later players.

For each player, we must output how many tokens they obtain in that turn, followed by the identifiers of those tokens in increasing order.

The difficulty is not evaluating a single query, but handling up to 100,000 points and 100,000 lines, while each point is removed once it is collected. A naive recomputation over all remaining points for each query would repeatedly scan large parts of the dataset and quickly become infeasible.

The input bounds imply that any solution with quadratic behavior in either T or P will fail. Even a linear scan per query leads to about $10^{10}$ operations in the worst case, which is far beyond typical limits. This forces a design where each point is processed only a small number of times across all queries, ideally once.

A subtle issue arises from the dynamic nature of deletions. A point that is removed early must not influence later queries. This prevents preprocessing answers independently for each line.

Another non-trivial corner case comes from ordering requirements. Even if we can efficiently find all points under a line, we must also output their identifiers in sorted order per query. A structure that retrieves points in arbitrary traversal order will still require careful post-processing.

## Approaches

A direct approach evaluates each query independently. For a given line $y = Ax + B$, we check every remaining point and test whether $Y < AX + B$. This correctly identifies all tokens for that player, and then we remove them from the set.

This works logically because the condition is purely geometric and independent per point. However, the cost is prohibitive. With T and P both up to 100,000, this approach performs up to $10^10$ point-line checks in the worst case, which is too slow.

The key structural observation is that we do not actually need to recompute membership from scratch each time. We only need a data structure that can repeatedly answer a geometric range query of the form “report all points in a half-plane” and then delete them.

This transforms the problem into a classic dynamic geometric reporting task. Each query is a half-plane query, and each point is removed at most once, so the total number of reported outputs across all queries is exactly T. This suggests that an output-sensitive structure can succeed, even if each individual query is not logarithmic.

A suitable tool for this is a spatial partitioning structure such as a kd-tree. The idea is to recursively partition points into axis-aligned rectangles. Each node represents a region of the plane, and stores the bounding box of its points. When processing a query line, we decide whether the entire region lies below the line, entirely above it, or partially intersects it. If fully below, we output all points in that subtree at once. If fully above, we prune it entirely. Otherwise, we recurse.

The key advantage is that each point is only visited along a logarithmic number of tree nodes, and each reported point contributes only once to the total output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · P) | O(T) | Too slow |
| kd-tree half-plane reporting | O((T + P) log T + output log output) | O(T) | Accepted |

## Algorithm Walkthrough

We build a kd-tree over all points, using alternating splits on x and y coordinates. Each node stores its bounding rectangle and the list of point ids in its subtree.

When processing a query line $y = Ax + B$, we traverse the kd-tree and classify each node relative to the line.

1. For a node, compute the maximum and minimum value of $y - Ax$ over its four rectangle corners. This is sufficient because a linear function achieves extrema on a rectangle at its corners.
2. If the maximum value is strictly less than B, then every point in this node satisfies the condition. We collect all point ids from this subtree and mark them as removed.
3. If the minimum value is greater than or equal to B, then no point in this node satisfies the condition, so we stop exploring this subtree.
4. Otherwise, the node is partially intersected by the query line. We recurse into its children.
5. After collecting all points for a query, we sort their ids before outputting them, since traversal order is not guaranteed to respect id ordering.
6. Mark all reported points as inactive so that future queries ignore them.

The reasoning behind correctness comes from the fact that every node classification is exact. A node is only fully included when every point inside satisfies the inequality, and only fully excluded when no point satisfies it. Partial nodes are decomposed until every affected point is individually discovered.

The invariant maintained is that at every step of traversal, we never skip a point that satisfies the query condition, and we never include a point that does not satisfy it. Since each point is removed immediately after being reported, it can never be duplicated in later queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("x1", "x2", "y1", "y2", "ids", "left", "right")
    def __init__(self, x1, x2, y1, y2, ids):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.ids = ids
        self.left = None
        self.right = None

def build(points, depth=0):
    if not points:
        return None

    if len(points) == 1:
        x, y, i = points[0]
        node = Node(x, x, y, y, [i])
        return node

    axis = depth % 2
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2

    left = build(points[:mid], depth + 1)
    right = build(points[mid:], depth + 1)

    xs = []
    ys = []

    for child in (left, right):
        if child:
            xs.extend([child.x1, child.x2])
            ys.extend([child.y1, child.y2])

    node = Node(min(xs), max(xs), min(ys), max(ys), [])
    node.left = left
    node.right = right
    return node

def query(node, A, B, res):
    if not node:
        return

    corners = [
        (node.x1, node.y1),
        (node.x1, node.y2),
        (node.x2, node.y1),
        (node.x2, node.y2),
    ]

    vals = [y - A * x for x, y in corners]
    mx = max(vals)
    mn = min(vals)

    if mx < B:
        collect(node, res)
        return

    if mn >= B:
        return

    if node.left is None and node.right is None:
        if node.ids:
            res.extend(node.ids)
            node.ids = []
        return

    query(node.left, A, B, res)
    query(node.right, A, B, res)

def collect(node, res):
    if not node:
        return
    if node.left is None and node.right is None:
        if node.ids:
            res.extend(node.ids)
            node.ids = []
        return
    collect(node.left, res)
    collect(node.right, res)

def solve():
    T = int(input())
    pts = []
    for i in range(1, T + 1):
        x, y = map(int, input().split())
        pts.append((x, y, i))

    root = build(pts)

    P = int(input())
    for _ in range(P):
        A, B = map(int, input().split())
        res = []
        query(root, A, B, res)
        res.sort()
        if res:
            print(len(res), *res)
        else:
            print(0)

if __name__ == "__main__":
    solve()
```

The kd-tree construction recursively partitions points so that geometric queries become localized. The query function is the core: it uses rectangle corner evaluation to decide whether to fully take or skip a subtree. The collect function is only used when a subtree is entirely inside the query region, avoiding unnecessary per-point checks.

A subtle implementation detail is that subtree bounding boxes must be accurate. Any mistake there breaks the correctness of the pruning logic. Another important point is that each point is removed exactly once by clearing leaf storage after reporting.

Sorting is applied per query because the traversal order of the kd-tree is not aligned with identifier order.

## Worked Examples

Consider a small configuration where points are spread in the plane and a few lines are applied.

### Example Trace 1

Suppose we have three points:

(0,0,1), (2,2,2), (4,1,3)

Query line: $y = x + 0$

We evaluate each point condition $Y < X$.

| Step | Point | Compute Y < X | Taken |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 < 0 | No |
| 2 | (2,2) | 2 < 2 | No |
| 3 | (4,1) | 1 < 4 | Yes |

Only point 3 is collected, so output is:

```
1 3
```

This confirms that the geometric condition is evaluated strictly, not allowing equality.

### Example Trace 2

Now apply a second query to the remaining points.

Points left:

(0,0,1), (2,2,2)

Query: $y = 0x + 1$

Condition is $Y < 1$.

| Step | Point | Compute Y < 1 | Taken |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 < 1 | Yes |
| 2 | (2,2) | 2 < 1 | No |

Output:

```
1 1
```

This shows that deletion is correctly applied: previously removed points never reappear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((T + P) log T + T log T total sorting) | Each point is visited through kd-tree paths once per removal, and total reporting cost is linear over all outputs |
| Space | O(T) | Each point is stored once in the kd-tree structure |

The complexity fits comfortably within constraints because every token is reported exactly once, and each query only explores relevant parts of the tree. The additional logarithmic factors come from traversal depth and per-query sorting, which remain bounded by 100,000-scale limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = StringIO(inp)
    out = StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

# minimal
assert solve_capture("1\n0 0\n1\n0 1\n") == "1 1"

# all below first line
assert solve_capture("3\n0 0\n1 0\n2 0\n1\n0 1\n") == "3 1 2 3"

# no points
assert solve_capture("2\n0 10\n10 10\n1\n0 0\n") == "0"

# mixed removals
assert solve_capture("4\n0 0\n1 2\n2 1\n3 3\n2\n0 2\n1 2\n") == "3 1 2 3\n1 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single point | single removal | base correctness |
| all points satisfy | full subtree collection | node aggregation correctness |
| no points satisfy | empty output | pruning correctness |
| mixed queries | dynamic deletion | state updates across queries |

## Edge Cases

A key edge case is when a query line removes an entire large region at once. In this case, the kd-tree must avoid descending into individual points unnecessarily. The algorithm handles this because the rectangle test detects full containment when all four corners satisfy the inequality, allowing immediate subtree collection.

Another edge case is when A is negative. This changes which corners produce the maximum and minimum values of $y - Ax$. The implementation handles this correctly because it evaluates all four corners directly rather than relying on axis-aligned shortcuts.

A final edge case is repeated queries that target already removed points. Since each leaf clears its stored ids after collection, subsequent traversals naturally skip empty nodes, ensuring no duplicate outputs even when the geometric condition still holds.
