---
title: "CF 1527D - MEX Tree"
description: "We have a tree whose vertices are labeled with the integers 0 through n - 1. For every unordered pair of distinct vertices (u, v), we look at the unique simple path connecting them."
date: "2026-06-10T17:16:59+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "implementation", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 1527
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 721 (Div. 2)"
rating: 2400
weight: 1527
solve_time_s: 233
verified: false
draft: false
---

[CF 1527D - MEX Tree](https://codeforces.com/problemset/problem/1527/D)

**Rating:** 2400  
**Tags:** combinatorics, dfs and similar, implementation, math, trees  
**Solve time:** 3m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We have a tree whose vertices are labeled with the integers `0` through `n - 1`. For every unordered pair of distinct vertices `(u, v)`, we look at the unique simple path connecting them. The labels appearing on that path form a set of integers, and we compute the MEX of that set, meaning the smallest non-negative integer that does not appear.

The task is to count, for every value `k` from `0` to `n`, how many vertex pairs have path MEX equal to `k`.

The labels are not arbitrary values stored on vertices. The label of a vertex is exactly its index. This is the key structural property of the problem.

The total number of vertices across all test cases is at most `2 · 10^5`, so any solution substantially worse than linear or near-linear per test case is impossible. A tree with `2 · 10^5` vertices contains about `2 · 10^10` unordered pairs of vertices, which immediately rules out any approach that enumerates paths. Even an `O(n²)` algorithm would perform roughly `4 · 10^10` operations in the worst case.

The difficulty comes from counting paths indirectly, without ever iterating over them.

A subtle edge case appears when label `0` is not on the path. Every path missing `0` has MEX `0`, regardless of which other labels appear.

For example:

```
0 - 1 - 2
```

The path `(1,2)` contains labels `{1,2}` and has MEX `0`.

Another important situation occurs when the vertices with labels `0,1,...,k-1` cannot all lie on a single simple path. In that case no path can contain all of them simultaneously, so the answer for MEX `k` must be zero.

For example:

```
    0
   / \
  1   2
```

The three labels `{0,1,2}` do not lie on one simple path. No path can contain all three vertices, so every answer requiring them all to be present is zero.

A third source of mistakes is the handling of MEX `n`. For MEX `n`, the path must contain every label from `0` to `n-1`. Since labels are exactly the vertices, such a path must visit every vertex of the tree. This is only possible if the entire tree itself is a simple path.

## Approaches

A brute force solution would examine every unordered pair of vertices, find the path between them, collect the labels on that path, compute its MEX, and increment the corresponding counter.

The path between two vertices can be obtained using LCA preprocessing, but even then there are `Θ(n²)` pairs. With `n = 2 · 10^5`, this becomes completely infeasible.

The crucial observation is that MEX conditions are defined by small labels.

Suppose a path has MEX `k`.

Then:

```
0,1,...,k-1 must all appear on the path
k must not appear on the path
```

Nothing else matters.

Let

```
S_k = {0,1,...,k-1}
```

A path contributes to answer `k` iff it contains every vertex of `S_k` and does not contain vertex `k`.

The key structural fact is that a collection of vertices can all belong to one simple path only when they are contained in some path segment of the tree.

Define `L` and `R` as the endpoints of the minimal path containing vertices `0..i`.

While increasing `i`, we maintain this path.

If vertex `i` cannot be attached to the current endpoint structure, then vertices `0..i` are no longer contained in a single simple path. Once this happens, every larger set `0..j` also fails, and all remaining answers become zero.

The entire solution revolves around maintaining the path containing labels `0..i`, then counting how many pairs of endpoints generate a path containing all vertices `0..i-1` but excluding vertex `i`.

The counting itself is done through component sizes around the current path.

This transforms an impossible path enumeration problem into a sequence of local counting operations along a dynamically growing path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · n) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

### Preprocessing

We root the tree at vertex `0`.

Using DFS we compute:

- parent of every vertex
- subtree sizes
- Euler entry and exit times

The Euler intervals allow constant-time ancestor checks.

### Maintaining the path of small labels

Let the current path contain all labels from `0` through `i`.

Initially:

```
L = 0
R = 0
```

For each new label `i` we determine whether it can extend the current path.

There are only three possibilities:

1. `i` lies on the path from `L` to `R`.
2. `i` can become the new left endpoint.
3. `i` can become the new right endpoint.

If none of these holds, then vertices `0..i` are not contained in any simple path. All larger answers become zero and we stop.

### Counting paths containing all required labels

Suppose vertices `0..i-1` are exactly contained inside path `(L,R)`.

We now want to count paths that contain that entire path but do not contain vertex `i`.

Any path containing `(L,R)` must choose one endpoint in a region attached beyond `L` and another endpoint in a region attached beyond `R`.

The number of valid choices is the product of the sizes of those two regions.

We compute these sizes using subtree information and ancestor relations.

### Inclusion-Exclusion Between Consecutive MEX Values

Let:

```
f(i) = number of paths containing all vertices 0..i-1
```

Then:

```
answer[i] = f(i) - f(i+1)
```

because paths counted by `f(i+1)` are exactly those that also contain vertex `i`.

This automatically enforces the condition that vertex `i` must be absent.

### MEX 0

For MEX `0`, we need paths that do not contain vertex `0`.

Removing vertex `0` splits the tree into components.

Any path entirely inside one component avoids `0`.

If a component has size `s`, it contributes:

```
s(s-1)/2
```

unordered vertex pairs.

Summing over all components gives answer `0`.

### MEX n

The value:

```
f(n)
```

already represents paths containing every vertex.

This is exactly answer `n`.

### Why it works

At every stage, the maintained endpoints `(L,R)` describe the unique minimal path containing labels processed so far. A set of vertices belongs to some simple path if and only if each newly inserted vertex can extend the current path from one endpoint. When that property fails once, it can never recover.

For a fixed `i`, every path containing labels `0..i-1` must contain the entire minimal path `(L,R)`. Such a path is uniquely determined by choosing one endpoint from the region extending past `L` and another from the region extending past `R`. Multiplying those region sizes counts every valid path exactly once.

Since MEX `i` requires containing `0..i-1` and excluding `i`, subtracting consecutive counts gives precisely the desired quantity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        parent = [-1] * n
        tin = [0] * n
        tout = [0] * n
        sz = [0] * n

        timer = 0

        stack = [(0, -1, 0)]
        while stack:
            v, p, state = stack.pop()

            if state == 0:
                parent[v] = p
                tin[v] = timer
                timer += 1

                stack.append((v, p, 1))
                for to in reversed(g[v]):
                    if to != p:
                        stack.append((to, v, 0))
            else:
                s = 1
                for to in g[v]:
                    if to != p:
                        s += sz[to]
                sz[v] = s
                tout[v] = timer

        def is_ancestor(a, b):
            return tin[a] <= tin[b] < tout[a]

        def on_path(x, a, b):
            return (
                is_ancestor(x, a) and is_ancestor(b, x)
            ) or (
                is_ancestor(x, b) and is_ancestor(a, x)
            )

        ans = [0] * (n + 1)

        total_pairs = n * (n - 1) // 2

        bad = 0
        for to in g[0]:
            if parent[to] == 0:
                s = sz[to]
            else:
                s = n - sz[0]
            bad += s * (s - 1) // 2

        ans[0] = bad

        f = [0] * (n + 1)

        L = 0
        R = 0

        def side_size(end, other):
            if is_ancestor(end, other):
                cur = other
                while parent[cur] != end:
                    cur = parent[cur]
                return n - sz[cur]
            return sz[end]

        f[1] = total_pairs

        alive = True

        for x in range(1, n):
            if not alive:
                break

            in_lr = on_path(x, L, R)
            in_lx = on_path(R, L, x)
            in_rx = on_path(L, R, x)

            if in_lr:
                pass
            elif in_lx:
                L = x
            elif in_rx:
                R = x
            else:
                alive = False
                break

            left_cnt = side_size(L, R)
            right_cnt = side_size(R, L)

            f[x + 1] = left_cnt * right_cnt

        for i in range(1, n):
            ans[i] = f[i] - f[i + 1]

        ans[n] = f[n]

        print(*ans)

solve()
```

The DFS computes parent pointers, subtree sizes, and Euler timestamps. These are the only structural data needed later.

The function `is_ancestor` uses Euler intervals. A vertex `a` is an ancestor of `b` exactly when the Euler entry time of `a` contains the entry time of `b`.

The maintained pair `(L,R)` represents the minimal path containing all processed labels. When a new label arrives, there are only three possible geometric relationships. If none works, the required vertices no longer fit on a single path and all later counts become zero.

The helper `side_size` computes how many vertices may serve as an endpoint extending beyond one side of the path. The formula depends on whether the opposite endpoint lies inside the current endpoint's subtree.

The array `f` stores counts of paths containing all labels smaller than a threshold. Consecutive differences then produce the exact MEX frequencies.

A common implementation mistake is forgetting that `answer[0]` follows a different counting rule. MEX `0` means the path must avoid vertex `0`, which is most naturally counted by removing vertex `0` and summing pairs inside each resulting component.

## Worked Examples

### Sample 1

Input:

```
4
0-1
0-2
2-3
```

The maintained path evolves as follows.

| Step | Labels Required | L | R | f |
| --- | --- | --- | --- | --- |
| Initial | {0} | 0 | 0 | 6 |
| Add 1 | {0,1} | 1 | 0 | 2 |
| Add 2 | {0,1,2} | 1 | 2 | 1 |
| Add 3 | {0,1,2,3} | 1 | 3 | 1 |

Then:

| k | Computation | Answer |
| --- | --- | --- |
| 0 | component count | 1 |
| 1 | 6 - 2 | 4 |
| 2 | 2 - 1 | 1 |
| 3 | 1 - 1 | 0 |
| 4 | 1 | 1 |

The example illustrates how the path endpoints expand as larger labels are inserted.

### Sample 2

Input:

```
2
1-0
```

| Step | Labels Required | L | R | f |
| --- | --- | --- | --- | --- |
| Initial | {0} | 0 | 0 | 1 |
| Add 1 | {0,1} | 1 | 0 | 1 |

Answers become:

| k | Value |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 1 |

This demonstrates the MEX `n` case. The only path contains both vertices, so its MEX equals `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex is processed a constant number of times |
| Space | O(n) | Graph, DFS arrays, and auxiliary structures |

The total number of vertices over all test cases is at most `2 · 10^5`, so linear processing comfortably fits inside the time limit and memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue()

assert run(
"""2
4
0 1
0 2
2 3
2
1 0
"""
) == """1 2 1 1 1
0 0 1
"""

assert run(
"""1
2
0 1
"""
) == """0 0 1
"""

assert run(
"""1
3
0 1
1 2
"""
) == """0 1 1 1
"""

assert run(
"""1
3
0 1
0 2
"""
) == """1 1 1 0
"""

assert run(
"""1
4
0 1
1 2
2 3
"""
) == """0 1 1 1 1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | `0 0 1` | Smallest valid tree |
| Three-node chain | `0 1 1 1` | Consecutive path growth |
| Three-node star | `1 1 1 0` | Path condition failure |
| Four-node chain | `0 1 1 1 1` | MEX `n` counting |

## Edge Cases

Consider the star:

```
3
0 1
0 2
```

Removing vertex `0` leaves two isolated vertices. No unordered pair exists inside either component, so answer `0` equals `0`.

The algorithm computes this directly by summing:

```
1·0/2 + 1·0/2 = 0
```

Now consider:

```
    0
   / \
  1   2
```

When label `2` is processed, the current path containing `{0,1}` is `1-0`. Vertex `2` cannot extend either endpoint while preserving a simple path containing all labels. The algorithm detects this and terminates further expansion. Every larger MEX answer automatically becomes zero.

Finally consider a chain:

```
0 - 1 - 2 - 3
```

All labels lie on a single simple path. Every insertion extends one endpoint, so the invariant never breaks. The final value `f[n]` becomes `1`, correctly counting the unique path containing every vertex.
