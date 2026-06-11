---
title: "CF 1238F - The Maximum Subtree"
description: "We are given a tree and need to find the largest connected subgraph that can be represented as an intersection graph of line segments on a line."
date: "2026-06-11T22:11:05+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 1238
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 74 (Rated for Div. 2)"
rating: 2200
weight: 1238
solve_time_s: 116
verified: true
draft: false
---

[CF 1238F - The Maximum Subtree](https://codeforces.com/problemset/problem/1238/F)

**Rating:** 2200  
**Tags:** dfs and similar, dp, graphs, trees  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree and need to find the largest connected subgraph that can be represented as an intersection graph of line segments on a line.

A graph is built from segments by creating one vertex per segment and connecting two vertices whenever the corresponding segments intersect. Some trees can be represented this way and some cannot. Among all connected subgraphs of the given tree, we must find the one with the maximum number of vertices that is representable.

The input contains up to $1.5 \cdot 10^5$ test cases, but the total number of vertices across all trees is at most $3 \cdot 10^5$. This aggregate bound is the one that matters. Any solution substantially worse than linear per tree will fail. An $O(n^2)$ algorithm would require around $9 \cdot 10^{10}$ operations in the worst case, which is completely infeasible. Even $O(n \log n)$ is fine, but the intended solution is actually linear.

The difficult part is not the tree processing itself. The challenge is understanding which trees are representable as interval intersection graphs.

A classical result says that interval graphs are exactly the intersection graphs of intervals on a line. Trees that are interval graphs have a very restricted structure. Any cycle is impossible because interval graphs are chordal, and among trees the only interval graphs are caterpillars.

A caterpillar is a tree that becomes a simple path after removing all leaves.

That observation completely changes the problem. We are no longer searching for an arbitrary good subtree. We are searching for the largest connected subtree that is a caterpillar.

Several edge cases are easy to miss.

Consider a star:

```
1
5
1 2
1 3
1 4
1 5
```

The whole tree is a caterpillar. Removing the leaves leaves a single vertex. The answer is 5.

A naive diameter-based approach would incorrectly return only 2.

Consider a balanced binary tree of height 2:

```
      1
    / | \
   2  3  4
  / \ / \
 5 6 7 8
```

The answer is 8, not 7. The optimal caterpillar uses one central path and may keep leaves attached to vertices of that path.

Another subtle case is a simple path:

```
1-2-3-4-5
```

The entire tree is already a caterpillar. The answer is 5.

Any DP that only counts branching vertices and forgets path endpoints will underestimate this case.

## Approaches

The brute force viewpoint is straightforward. Enumerate every connected subtree and test whether it is a caterpillar.

Testing whether a tree is a caterpillar is easy. Remove all leaves and check whether the remaining graph is a path. The problem is the number of connected subtrees. Even a tree with a few hundred vertices already has an enormous number of connected subgraphs. This approach is hopeless.

The key observation is structural.

A tree is representable as an interval graph if and only if it is a caterpillar. A caterpillar consists of a backbone path, often called the spine, and arbitrary leaves attached to vertices of that path.

Instead of thinking about interval representations, we can think about choosing a path. Every vertex on that path may contribute all of its neighboring leaves. Any branch that extends further than one edge away from the path would violate the caterpillar property.

Suppose a vertex belongs to the spine. One incident edge is used to connect to its parent on the spine, another may continue the spine downward, and every remaining incident edge can contribute exactly one leaf vertex.

This naturally suggests a tree DP.

Let a rooted tree be fixed. We want a state describing the best caterpillar whose spine starts at the current vertex and goes downward. When the spine passes through a vertex, every unused child contributes one leaf. One child may be chosen to continue the spine.

This turns the problem into a longest-path style DP where each vertex contributes

```
(number of available leaves) + 1
```

and one child may continue the chain.

The final answer is obtained by combining the two best downward spine extensions through each vertex, exactly like diameter DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Tree DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

Let the tree be rooted at an arbitrary vertex, say vertex 1.

Define:

`dp[v]` = maximum size of a caterpillar subtree whose spine starts at `v` and continues only into descendants.

For a vertex `v`, let

```
base(v) = 1 + (deg(v) - 1)
```

for non-root vertices.

The `1` counts the vertex itself.

Among its incident edges, one edge goes toward its parent and cannot become a leaf. Every other unused incident edge may contribute a leaf.

For the root:

```
base(root) = 1 + deg(root)
```

because there is no parent edge.

Now process vertices bottom-up.

### 1. Compute the contribution of every vertex without extending the spine

If the spine ends at `v`, all child edges become leaves.

The value is simply `base(v)`.

### 2. Try extending the spine through one child

Suppose the spine continues through child `u`.

The edge to `u` is no longer available as a leaf, so we lose one leaf contribution.

The resulting value is

```
base(v) - 1 + dp[u]
```

Take the maximum over all children.

This gives `dp[v]`.

### 3. Compute the best caterpillar passing through each vertex

A global optimum may have its spine passing through `v` and continuing into two different child directions.

Let

```
gain(u) = dp[u]
```

for every child.

Take the two largest child gains.

The caterpillar centered at `v` has size

```
base(v) + best1 + best2 - 2
```

The subtraction by 2 comes from using two child edges as spine edges instead of leaf edges.

For the root, the formula is slightly different because there is no parent edge already excluded.

Using the unified implementation below is easier and avoids special-case reasoning.

### 4. Update the global answer

For every vertex, update the answer with the best caterpillar whose spine passes through that vertex.

### 5. Process all test cases

Because the total number of vertices is at most $3 \cdot 10^5$, a single DFS per tree is sufficient.

### Why it works

A caterpillar is completely determined by its spine path. Every vertex on the spine may use at most two incident edges to remain on the spine. All other incident edges can only contribute leaves.

The DP state represents the optimal caterpillar whose spine enters a vertex from above and continues downward through at most one child. When combining the two best child extensions at a vertex, we construct every possible spine path whose highest vertex is that vertex. Every caterpillar has exactly one such highest spine vertex in the rooted tree, so every valid caterpillar is considered. The DP always accounts for every vertex that can legally become a leaf and excludes every vertex that would create distance greater than one from the spine. Hence the computed maximum is exactly the largest caterpillar subtree.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    anss = []

    for _ in range(t):
        n = int(input())

        g = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * n
        order = [0]
        parent[0] = 0

        for v in order:
            for to in g[v]:
                if parent[to] == -1:
                    parent[to] = v
                    order.append(to)

        dp = [0] * n
        answer = 0

        for v in reversed(order):
            deg = len(g[v])

            if v == 0:
                base = deg + 1
            else:
                base = deg

            best1 = 0
            best2 = 0

            dp[v] = base

            for to in g[v]:
                if to == parent[v]:
                    continue

                cand = base - 1 + dp[to]
                if cand > dp[v]:
                    dp[v] = cand

                val = dp[to]
                if val > best1:
                    best2 = best1
                    best1 = val
                    best1_child = to
                elif val > best2:
                    best2 = val

            answer = max(answer, dp[v])

            cur = base

            if best1:
                cur += best1 - 1
            if best2:
                cur += best2 - 1

            answer = max(answer, cur)

        anss.append(str(answer))

    sys.stdout.write("\n".join(anss))

if __name__ == "__main__":
    solve()
```

The tree is rooted iteratively to avoid recursion depth issues. With up to $3 \cdot 10^5$ vertices, recursive DFS is risky in Python.

`base` represents the contribution of the current vertex if no child continues the spine. For a non-root vertex, one edge is already reserved for the parent direction, so only the remaining incident edges can become leaves.

`dp[v]` stores the best caterpillar whose spine enters `v` from above and may continue through one child. Extending through a child consumes one potential leaf edge, which is why the transition uses `base - 1 + dp[child]`.

The global answer must also consider caterpillars whose spine passes through a vertex and continues into two child directions. This is analogous to the standard tree diameter combination step, so we keep the two largest child DP values.

## Worked Examples

### Example 1

Input:

```
1
5
1 2
1 3
1 4
1 5
```

The tree is a star.

| Vertex | Degree | Base | Best Child DP | DP |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 1 |
| 4 | 1 | 1 | 1 | 1 |
| 5 | 1 | 1 | 0 | 1 |
| 1 | 4 | 5 | 1 | 5 |

The answer becomes 5.

This demonstrates that a star is itself a caterpillar. The center forms a spine of length one and every other vertex is a leaf.

### Example 2

Input:

```
1
5
1 2
2 3
3 4
4 5
```

A simple path.

| Vertex | Degree | Base | Child DP | DP |
| --- | --- | --- | --- | --- |
| 5 | 1 | 1 | 0 | 1 |
| 4 | 2 | 2 | 1 | 2 |
| 3 | 2 | 2 | 2 | 3 |
| 2 | 2 | 2 | 3 | 4 |
| 1 | 1 | 2 | 4 | 5 |

The answer is 5.

This trace shows how the spine extends through exactly one child at every step, reconstructing the whole path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is processed a constant number of times |
| Space | O(n) | Adjacency list, parent array, traversal order, DP array |

The sum of all vertices across test cases is at most $3 \cdot 10^5$. A linear solution processes only a few million primitive operations, comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        g = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * n
        order = [0]
        parent[0] = 0

        for v in order:
            for to in g[v]:
                if parent[to] == -1:
                    parent[to] = v
                    order.append(to)

        dp = [0] * n
        ans = 0

        for v in reversed(order):
            deg = len(g[v])

            base = deg + 1 if v == 0 else deg

            best1 = best2 = 0
            dp[v] = base

            for to in g[v]:
                if to == parent[v]:
                    continue

                dp[v] = max(dp[v], base - 1 + dp[to])

                val = dp[to]
                if val > best1:
                    best2 = best1
                    best1 = val
                elif val > best2:
                    best2 = val

            ans = max(ans, dp[v])

            cur = base
            if best1:
                cur += best1 - 1
            if best2:
                cur += best2 - 1

            ans = max(ans, cur)

        out.append(str(ans))

    return "\n".join(out)

# star
assert run("""1
5
1 2
1 3
1 4
1 5
""") == "5"

# path
assert run("""1
5
1 2
2 3
3 4
4 5
""") == "5"

# minimum tree
assert run("""1
2
1 2
""") == "2"

# balanced binary tree from statement style
assert run("""1
10
1 2
1 3
1 4
2 5
2 6
3 7
3 8
4 9
4 10
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | 2 | Minimum valid size |
| Star | 5 | Many leaves attached to one spine vertex |
| Path | 5 | Entire tree used as spine |
| Balanced branching tree | 8 | Combining two best spine extensions |

## Edge Cases

Consider the minimum tree:

```
1
2
1 2
```

Both vertices form a path, which is automatically a caterpillar. The root gets `base = 2`, the leaf gets `base = 1`, and the DP returns 2.

Consider a star:

```
1
5
1 2
1 3
1 4
1 5
```

The center contributes itself plus all four neighbors. No spine extension is needed. The algorithm evaluates this directly through the `base` value of the center and returns 5.

Consider a long path:

```
1
6
1 2
2 3
3 4
4 5
5 6
```

Every internal vertex extends the spine through exactly one child. The DP accumulates one extra vertex at each step and reaches 6. No leaf contributions are required.

Consider a highly branching tree where several children compete to continue the spine. The algorithm keeps the two largest child DP values. Every caterpillar spine passing through a vertex can use at most two directions, so retaining only the two best values is sufficient and no optimal solution is discarded.
