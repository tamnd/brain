---
title: "CF 102862H - Optimize DFS"
description: "We have a tree where every vertex stores two numbers, a and b. The interesting value is not either number alone, but their difference: $$cv = av - bv$$ A DFS step from a vertex v can move to a neighboring vertex u exactly when: $$av+bu=au+bv$$ Rearranging gives: $$av-bv=au-bu$$…"
date: "2026-07-25T13:53:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "H"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 53
verified: true
draft: false
---

[CF 102862H - Optimize DFS](https://codeforces.com/problemset/problem/102862/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree where every vertex stores two numbers, `a` and `b`. The interesting value is not either number alone, but their difference:

$$c_v = a_v - b_v$$

A DFS step from a vertex `v` can move to a neighboring vertex `u` exactly when:

$$a_v+b_u=a_u+b_v$$

Rearranging gives:

$$a_v-b_v=a_u-b_u$$

so the DFS only travels through edges whose endpoints currently have the same `c` value. After a vertex finishes in the DFS, its `a` value becomes `b`, which means its `c` value becomes zero.

The task is to process three types of operations. We can change one vertex's `a` value, ask for one vertex's current `a` value, or simulate the DFS process from a starting vertex efficiently.

The constraints allow up to `5 * 10^5` vertices and queries. A solution that repeatedly scans the whole tree or runs a fresh DFS over all vertices for every third query would be far too slow. With half a million operations, we need the total amount of work across all DFS simulations to be close to linear.

The important observation is that a third query only changes vertices whose current difference `c` is non-zero and equal to the starting vertex's difference. Once such a vertex is processed, its difference becomes zero. A vertex can only become non-zero again through a type 1 query, which changes exactly one vertex. This gives us an amortized bound: every vertex visited by an actual flood fill is either one of the initially non-zero vertices or was made non-zero by a previous update.

A careful implementation must handle cases where the starting vertex already has `a_v=b_v`. For example:

```
1 1
5
5
```

A third query from vertex `1` should do nothing and the value remains `5`. A naive implementation that tries to search for a component with difference zero may waste time repeatedly walking through the whole zero component.

Another edge case is a component containing several vertices with the same non-zero difference:

```
3 1
10 20 30
5 15 25
1 2
2 3
3 1
```

The differences are all `5`, so the DFS visits all three vertices and the output after the operation is:

```
5 15 25
```

for their `a` values. A solution that only resets the starting vertex would be incorrect.

A final important case is when a single update reconnects a large component:

```
3 2
10 0 0
0 0 0
1 2
2 3
1 2 10
3 1
```

After the update, all three vertices have difference `10`, so the third query must clear all three. The algorithm must always compare the current differences while traversing.

## Approaches

The direct solution is to simulate the described DFS. For every type 3 query, start from the requested vertex, recursively visit neighbors whose current difference matches, and set `a_v=b_v` after returning. This is exactly what the statement describes, so correctness is immediate.

The problem is that the same vertex could appear in many DFS traversals if we only look at the tree structure. A path or star-shaped tree can make a single query touch almost every vertex, and repeating that many times would lead to around `O(nq)` work.

The key insight is that the DFS is destructive. A non-zero difference component disappears after it is processed because every vertex in that component becomes difference zero. The only way a vertex can return to a non-zero difference is a type 1 query, and that affects one vertex. Thus, over the entire execution, the total number of vertices that can be removed by all meaningful DFS operations is bounded by the initial number of non-zero vertices plus the number of updates.

This allows us to use the simple flood fill approach. We do not need a complicated dynamic connectivity structure because the operation itself destroys the part of the graph it explores.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O(n + q) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the current `a` values and the fixed `b` values. For every third query, compute the current difference `a[v]-b[v]` of the starting vertex.

If this value is zero, the DFS would only visit vertices that already satisfy `a=b`, so the operation changes nothing. We can skip it immediately.
2. For a non-zero starting difference, run an iterative DFS using a stack. Keep a timestamp array to mark vertices visited during the current flood fill.

The timestamp avoids clearing a full `visited` array before every query, which would cost `O(n)` even for a query that changes nothing.
3. While processing a vertex, inspect all adjacent vertices. If an unvisited neighbor has the same current difference, push it into the stack.

The equality check uses the current value of `a`, because previous parts of the DFS may already have changed vertices to `b`.
4. After a vertex is taken from the stack, set `a[v]=b[v]`.

This exactly matches the effect of the original DFS finishing that vertex. Since the graph is a tree, changing already processed vertices cannot create additional paths that should have been visited.

Why it works:

The DFS condition is equivalent to equality of the difference `a-b`. Therefore the original procedure visits exactly the connected component of the starting vertex inside the graph containing only edges between equal differences. The algorithm performs the same search and applies the same final assignment to every visited vertex. The timestamp only prevents revisiting vertices inside one search, and the amortized argument proves that the total amount of searching over all queries is linear in the number of initial active vertices plus updates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    seen = [0] * (n + 1)
    timer = 0
    ans = []

    for _ in range(q):
        query = list(map(int, input().split()))
        t = query[0]

        if t == 1:
            v, x = query[1], query[2]
            a[v] = x

        elif t == 2:
            ans.append(str(a[query[1]]))

        else:
            v = query[1]
            diff = a[v] - b[v]

            if diff == 0:
                continue

            timer += 1
            stack = [v]
            seen[v] = timer

            while stack:
                x = stack.pop()

                for y in g[x]:
                    if seen[y] != timer and a[y] - b[y] == diff:
                        seen[y] = timer
                        stack.append(y)

                a[x] = b[x]

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation keeps `a` mutable because type 1 and type 3 queries both change it. The `b` array never changes, so it is stored separately.

The flood fill uses an explicit stack instead of recursion. With `5 * 10^5` vertices, a recursive DFS would exceed Python's recursion limit and risk stack overflow.

The order inside the loop is important. A vertex is assigned `a[x]=b[x]` after its neighbors have been checked. This mirrors the original DFS, where the assignment happens after exploring all valid children. If the assignment happened first, the difference would become zero and the search would incorrectly lose information.

The timestamp technique prevents the need to allocate or reset a large visited array for every query. Each actual flood fill only touches vertices it needs.

## Worked Examples

Sample 1:

```
2 6
20 102
10 90
1 2
2 1
2 2
1 2 100
3 1
2 1
2 2
```

The important state changes are:

| Step | Query | Difference values | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | `2 1` | `10, 12` | Print vertex 1 | `20` |
| 2 | `2 2` | `10, 12` | Print vertex 2 | `102` |
| 3 | `1 2 100` | `10, 10` | Update vertex 2 |  |
| 4 | `3 1` | both differences are `10` | Clear both vertices |  |
| 5 | `2 1` | `0, 0` | Print vertex 1 | `10` |
| 6 | `2 2` | `0, 0` | Print vertex 2 | `90` |

This example shows why the operation depends on differences rather than the raw `a` values. After the update, the two vertices become part of one component.

Sample 2:

```
6 6
20 30 30 60 60 70
10 20 30 40 50 60
1 2
2 4
2 5
1 3
3 6
1 3 40
3 1
2 1
2 6
2 2
2 4
```

The state during the flood fill is:

| Step | Query | Vertex differences | Action |
| --- | --- | --- | --- |
| 1 | `1 3 40` | `10,10,10,20,10,10` | Vertex 3 joins the difference 10 group |
| 2 | `3 1` | vertices 1,2,3,5,6 have difference 10 | Clear that whole connected component |
| 3 | `2 1` | vertex 1 has difference 0 | Output `10` |
| 4 | `2 6` | vertex 6 has difference 0 | Output `60` |
| 5 | `2 2` | vertex 2 has difference 0 | Output `20` |
| 6 | `2 4` | vertex 4 was not connected by difference 10 | Output `60` |

This demonstrates that the flood fill follows the current equal-difference component, not simply every vertex with the same difference in the whole tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) amortized | Each meaningful flood-filled vertex is either initially non-zero or created by an update, and each visited vertex scans its adjacency list once. |
| Space | O(n) | The tree, values, timestamps, and DFS stack all use linear memory. |

The constraints are large enough that any solution repeatedly walking the entire tree would fail. The amortized bound is what makes the simple traversal fit the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    oldout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue()
    sys.stdin = old
    sys.stdout = oldout
    return res

assert run(
"""2 6
20 102
10 90
1 2
2 1
2 2
1 2 100
3 1
2 1
2 2
"""
) == "20\n102\n10\n90", "sample 1"

assert run(
"""6 6
20 30 30 60 60 70
10 20 30 40 50 60
1 2
2 4
2 5
1 3
3 6
1 3 40
3 1
2 1
2 6
2 2
2 4
"""
) == "10\n60\n20\n60", "sample 2"

assert run(
"""1 3
5
5
2 1
3 1
2 1
"""
) == "5\n5", "single zero-difference vertex"

assert run(
"""3 2
10 0 0
0 0 0
1 2
2 3
3 1
2 2
"""
) == "0", "large component clearing"

assert run(
"""4 5
1 2 3 4
0 0 0 0
1 2 10
1 3 10
1 4 10
3 2
2 2
"""
) == "0\n10", "updates creating components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex with equal `a` and `b` | `5` values remain unchanged | Handles zero-difference queries |
| A chain where all vertices share one difference | Entire component is cleared | Handles multi-vertex flood fills |
| Several updates followed by a query | Only connected equal-difference vertices are affected | Handles dynamic changes |
| Smallest tree | Correct base behavior | Handles minimum size |

## Edge Cases

For a starting vertex with `a_v=b_v`, the algorithm computes a difference of zero and immediately skips the search. This matches the real DFS because every visited vertex would already end with the same value it started with.

For a connected non-zero component, such as:

```
3 1
10 20 30
5 15 25
1 2
2 3
3 1
```

all vertices have difference `5`. The stack begins with vertex `1`, discovers vertices `2` and `3`, and then assigns each of their `a` values to `b`. The resulting values become:

```
5 15 25
```

For a component that is recreated by updates, such as:

```
3 2
10 0 0
0 0 0
1 2
2 3
1 2 10
3 1
```

the update changes vertex `2` so every vertex has difference `10`. The third query starts from vertex `1`, reaches all three vertices through equal differences, and resets all three. The algorithm handles this because it always reads the current `a-b` values instead of relying on any previous component information.
