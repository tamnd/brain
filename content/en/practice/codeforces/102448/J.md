---
title: "CF 102448J - Jingle Bells"
description: "We have a tree with (N) vertices and (N-1) edges. Every edge either already has one of five colors, numbered (1) through (5), or is still uncolored and marked by (0). A final painting assigns a color to every uncolored edge while keeping all existing colors unchanged."
date: "2026-08-08T12:28:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "J"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 504
verified: true
draft: false
---

[CF 102448J - Jingle Bells](https://codeforces.com/problemset/problem/102448/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with (N) vertices and (N-1) edges. Every edge either already has one of five colors, numbered (1) through (5), or is still uncolored and marked by (0). A final painting assigns a color to every uncolored edge while keeping all existing colors unchanged.

The final coloring is valid when, at every vertex, all incident edges have different colors. The same color can appear many times in the tree, but two edges sharing a vertex may never have the same color. The answer is the number of valid completions of the partially colored tree, taken modulo (10^9+7). The original constraints allow (N) up to (10^5), with exactly (N-1) edge descriptions.

The size of the tree rules out anything exponential in (N). There can be (5^{N-1}) assignments to the uncolored edges, so enumerating them is already impossible for a tree with only a few dozen edges. Even an (O(N^2)) algorithm is too large for (10^5) vertices under a 2 second limit. We need essentially linear time, with only a small constant factor depending on the five available colors.

The crucial structural fact is that a valid vertex can have at most five incident edges. Once we know the color of the edge connecting a vertex to its parent, the colors of all child edges only need to be distinct from each other and from that parent color. Since there are only five colors, the complete set of colors used by the child edges fits in a 5-bit mask.

Several edge cases are easy to mishandle.

Consider a single vertex:

```
1
```

There are no edges to color, so there is exactly one valid painting. A DP implementation that assumes every vertex has a parent edge can accidentally return zero here. The correct output is `1`.

Adjacent edges with the same preassigned color make the answer immediately zero:

```
3
1 2 1
2 3 1
```

At vertex (2), both incident edges already have color (1), so no completion is possible. The correct output is `0`. An implementation that only checks conflicts while choosing colors for uncolored edges would silently miss this contradiction.

A vertex with more than five incident edges is also impossible:

```
7
1 2 0
1 3 0
1 4 0
1 5 0
1 6 0
1 7 0
```

All six edges would have to receive pairwise distinct colors at vertex (1), but only five colors exist. The correct output is `0`. A mask implementation must not accidentally process only the first five children and ignore the sixth.

Finally, the same color is allowed on edges that do not meet at a vertex:

```
4
1 2 1
2 3 2
3 4 1
```

Every vertex still sees distinct incident colors, so this is a valid coloring and the answer is `1`. A careless implementation that treats each color as globally usable only once would incorrectly reject it.

## Approaches

The direct approach is to assign every uncolored edge one of the five colors, then check whether the resulting coloring is valid. If there are (K) uncolored edges, this produces (5^K) candidates. In the worst case (K=N-1), so there are (5^{N-1}) complete colorings. Checking one coloring takes (\Theta(N)) time because every edge or vertex may need to be inspected. The total work is therefore (\Theta(N5^{N-1})), which becomes hopeless almost immediately.

The brute force works because every complete assignment can be checked independently. It fails because it repeatedly solves the same subtrees. For example, once the color of the edge entering a subtree is fixed, everything below that edge can be counted independently of the rest of the tree. That is exactly the kind of repeated structure tree DP can exploit.

Root the tree at an arbitrary vertex. For each vertex (v), suppose the edge from its parent has color (p). The only information from the rest of the tree that matters to (v)'s subtree is this value (p). Define (dp[v][p]) as the number of valid colorings of the subtree of (v), assuming the parent edge has color (p).

The children of (v) cannot share a color, and none of their colors may equal (p). For an uncolored edge from (v) to a child (u), choosing color (c) contributes (dp[u][c]) ways from the child's subtree. For an already colored edge with color (c), there is only one possible choice, contributing (dp[u][c]), provided that (c) is not already used at (v).

The remaining challenge is combining the children without trying every (5^5) assignment explicitly. Since there are only five colors, represent the colors already used among the processed child edges with a 5-bit mask. There are only (2^5=32) masks. We can run a small subset DP over the children.

There is one useful optimization that makes the DP cleaner. The child-edge assignments themselves do not depend on the parent color (p). We can first count all distinct assignments of child-edge colors, storing their used-color mask. Afterward, (dp[v][p]) is simply the sum of masks that do not contain color (p). For the root there is no parent edge, represented by (p=0), so every mask is allowed.

The resulting complexity is linear in the number of vertices up to the constant factor from the five colors and 32 masks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(N5^{N-1})) | (O(N)) | Too slow |
| Optimal | (O(N\cdot 5\cdot 32)) | (O(N\cdot 5)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex (1). For every vertex, remember its parent so that the edge toward the parent is excluded when processing its children. An iterative traversal is preferable in Python because a tree can be a path of length (10^5), which would exceed the normal recursive call-stack limit.
2. Define (dp[v][p]) for (p\in{0,1,2,3,4,5}). For (p=1,\ldots,5), it counts valid colorings inside (v)'s subtree when the parent edge has color (p). State (p=0) is used only for the root, where there is no parent edge.
3. Process vertices in reverse traversal order so every child's DP values are already known when its parent is processed. For a vertex (v), start a subset DP with `ways[0] = 1`. The mask records exactly which colors have already been assigned to processed child edges.
4. For an already colored child edge with color (c), only that color may be used. If the current mask already contains (c), the transition is forbidden because two incident edges at (v) would share a color. Otherwise, add the child's (dp[u][c]) ways to the mask containing (c).
5. For an uncolored child edge, try every color (c) whose bit is not already present in the mask. Choosing (c) contributes (dp[u][c]) ways, because after fixing the edge color, the entire child subtree has exactly that many valid completions.
6. After all children have been processed, `ways[mask]` represents the number of valid assignments to all child edges that use exactly the colors in `mask`. For the root, sum every mask because there is no parent color. For a non-root vertex and parent color (p), sum only masks that do not contain (p). This is the local condition that the parent edge must have a different color from every child edge.
7. Store these six values as `dp[v]` and continue upward. When vertex (1) is processed, the required answer is `dp[1][0]`, because the root has no parent edge.

The invariant is that after processing a vertex (v), `dp[v][p]` counts every valid coloring of the entire subtree exactly once, under the single assumption that the parent edge has color (p). The subset DP enforces pairwise distinct colors among all child edges, while the final mask filtering enforces inequality with the parent edge. Since different child subtrees share only vertex (v), once their incident edge colors are fixed, their internal choices are independent. Thus every valid global coloring corresponds to exactly one DP path, and every DP path represents a valid coloring.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007
FULL = 31

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, c))
        graph[v].append((u, c))

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for v in order:
        for u, c in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    dp = [[0] * 6 for _ in range(n)]

    for v in reversed(order):
        ways = [0] * 32
        ways[0] = 1

        for u, edge_color in graph[v]:
            if u == parent[v]:
                continue

            new_ways = [0] * 32

            if edge_color != 0:
                bit = 1 << (edge_color - 1)
                child_ways = dp[u][edge_color]

                if child_ways:
                    for mask in range(32):
                        value = ways[mask]
                        if value and not (mask & bit):
                            new_ways[mask | bit] += value * child_ways

            else:
                child_dp = dp[u]

                for mask in range(32):
                    value = ways[mask]
                    if not value:
                        continue

                    for color in range(1, 6):
                        bit = 1 << (color - 1)
                        if not (mask & bit):
                            new_ways[mask | bit] += value * child_dp[color]

            for mask in range(32):
                new_ways[mask] %= MOD

            ways = new_ways

        total = sum(ways) % MOD
        dp[v][0] = total

        for color in range(1, 6):
            bit = 1 << (color - 1)
            count = 0

            for mask in range(32):
                if not (mask & bit):
                    count += ways[mask]

            dp[v][color] = count % MOD

    print(dp[0][0])

if __name__ == "__main__":
    solve()
```

The adjacency list stores both endpoints of every edge together with its fixed color. A color of zero means that the transition may choose any of the five colors.

The `parent` and `order` arrays turn the undirected tree into a rooted tree without recursion. Because `order` is built from the root outward, reversing it guarantees that children are processed before parents.

The central part of the implementation is `ways`. Its index is a five-bit mask, where bit (c-1) means color (c) has already been used by one of the processed child edges. A fixed edge has exactly one possible color, while an uncolored edge tries all five colors that are not already represented in the mask.

The child DP value is multiplied into every transition. This is the product rule for independent subtrees: after deciding that the edge ((v,u)) has color (c), there are `dp[u][c]` possible ways to complete everything below (u).

The code delays the modulo operation until after each child has been incorporated. Every DP value entering a transition is already below (10^9+7), and each intermediate `new_ways` value remains small enough for Python's integer arithmetic. Reducing after each child keeps the values bounded without paying for a modulo operation on every individual transition.

The final loop computes `dp[v][color]` by excluding masks containing that color. This is equivalent to enforcing the parent-edge restriction after all child edges have been assigned. For the root, `dp[0][0]` sums every mask because color zero does not correspond to an actual edge color.

There is no integer overflow issue in Python, but the modulo operation is still necessary because the requested answer is modulo (10^9+7). More importantly, keeping DP values reduced prevents intermediate integers from growing unnecessarily.

## Worked Examples

### Sample 1

The tree is rooted at vertex (1). Edge (1-3) is fixed to color (1), while edges (1-2) and (3-4) are uncolored.

| Vertex | Child edge | Child DP values | Nonzero `ways` masks | Resulting DP |
| --- | --- | --- | --- | --- |
| 4 | none | all states (=1) | mask (0:1) | (dp[4][p]=1) |
| 3 | (3-4) uncolored | all states (=1) | five one-bit masks, each (1) | (dp[3][0]=5,\ dp[3][1..5]=4) |
| 2 | none | all states (=1) | mask (0:1) | (dp[2][p]=1) |
| 1 | (1-2) uncolored, (1-3) fixed (1) | (dp[2][c]=1,\ dp[3][1]=4) | masks containing color (1) and one other color, each (4) | (dp[1][0]=16) |

At vertex (3), the edge to vertex (4) can use any of the five colors. If the parent edge has color (1), only four of those choices remain, giving (dp[3][1]=4).

At vertex (1), the edge to vertex (3) must use color (1). The edge to vertex (2) can then use any of the other four colors. For every such choice, the subtree of vertex (3) has four completions. Thus the answer is (4\cdot4=16).

### Sample 2

This is a path with three uncolored edges.

| Vertex | Child edge | Child DP values | `ways` after child | Resulting DP |
| --- | --- | --- | --- | --- |
| 4 | none | all states (=1) | mask (0:1) | all states (1) |
| 3 | (3-4) uncolored | all (1) | five one-bit masks, each (1) | (dp[3][0]=5,\ dp[3][1..5]=4) |
| 2 | (2-3) uncolored | (dp[3][c]=4) | five one-bit masks, each (4) | (dp[2][0]=20,\ dp[2][1..5]=16) |
| 1 | (1-2) uncolored | (dp[2][c]=16) | five one-bit masks, each (16) | (dp[1][0]=80) |

The first edge has five choices. Once its color is fixed, the next edge has four choices, and the final edge also has four choices. The DP computes exactly (5\cdot4\cdot4=80), matching the sample output.

The example also demonstrates why the parent color must be part of the DP state. At vertex (3), there are five possibilities when no parent color is imposed, but only four possibilities after one of the five colors has already been used by the parent edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\cdot5\cdot32)) | Each child is processed with at most 32 masks and 5 possible colors |
| Space | (O(N\cdot5+N)) | The DP stores six states per vertex, alongside the tree and traversal arrays |

The color count is fixed at five, so the factors (5) and (32=2^5) are constants. The algorithm is consequently linear in the number of vertices for asymptotic purposes. With (N\le10^5), the number of tree edges is also (O(10^5)), so the solution fits comfortably within the intended memory bound and avoids the exponential (5^{N-1}) search.

## Test Cases

The test harness below uses the same `solve()` function as the submitted solution. The maximum-size case is generated as a star with (100000) vertices. Its center has (99999) incident edges, so the answer is immediately zero.

```python
import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n = int(input())
    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, c))
        graph[v].append((u, c))

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for v in order:
        for u, c in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    dp = [[0] * 6 for _ in range(n)]

    for v in reversed(order):
        ways = [0] * 32
        ways[0] = 1

        for u, edge_color in graph[v]:
            if u == parent[v]:
                continue

            new_ways = [0] * 32

            if edge_color != 0:
                bit = 1 << (edge_color - 1)
                child_ways = dp[u][edge_color]

                if child_ways:
                    for mask in range(32):
                        value = ways[mask]
                        if value and not (mask & bit):
                            new_ways[mask | bit] += value * child_ways
            else:
                child_dp = dp[u]

                for mask in range(32):
                    value = ways[mask]
                    if not value:
                        continue

                    for color in range(1, 6):
                        bit = 1 << (color - 1)
                        if not (mask & bit):
                            new_ways[mask | bit] += value * child_dp[color]

            for mask in range(32):
                new_ways[mask] %= MOD

            ways = new_ways

        dp[v][0] = sum(ways) % MOD

        for color in range(1, 6):
            bit = 1 << (color - 1)
            total = 0
            for mask in range(32):
                if not (mask & bit):
                    total += ways[mask]
            dp[v][color] = total % MOD

    print(dp[0][0])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """4
1 2 0
1 3 1
3 4 0
"""
) == "16", "sample 1"

# Provided sample 2
assert run(
    """4
1 2 0
2 3 0
3 4 0
"""
) == "80", "sample 2"

# Minimum-size tree: no edges means exactly one empty coloring.
assert run(
    """1
"""
) == "1", "minimum-size tree"

# Two vertices and one uncolored edge: any of the five colors works.
assert run(
    """2
1 2 0
"""
) == "5", "single uncolored edge"

# Adjacent fixed edges with the same color are impossible.
assert run(
    """3
1 2 1
2 3 1
"""
) == "0", "adjacent equal fixed colors"

# A vertex with exactly five incident edges can use every color once.
assert run(
    """6
1 2 0
1 3 0
1 4 0
1 5 0
1 6 0
"""
) == "120", "degree five"

# Maximum-size input. The center has 99999 incident edges,
# so no proper edge coloring with five colors exists.
max_n = 100000
max_input = str(max_n) + "\n" + "".join(
    f"1 {v} 0\n" for v in range(2, max_n + 1)
)
assert run(max_input) == "0", "maximum-size impossible star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | The empty tree and root state |
| Two vertices, one uncolored edge | `5` | Basic five-color choice and boundary indexing |
| Three-vertex path with both fixed edges color `1` | `0` | Detection of an existing local conflict |
| Five-edge uncolored star | `120` | Exact degree-five boundary, giving (5!) |
| (100000)-vertex uncolored star | `0` | Maximum input size and degree greater than five |

## Edge Cases

For the single-vertex case, the input is simply:

```
1
```

The traversal contains only vertex (1). Its child subset DP starts with `ways[0] = 1` and processes no edges, so the only mask remains valid. The root uses state `p=0`, which sums all masks and gives `1`. No special case is required in the implementation.

For adjacent precolored edges with the same color, consider:

```
3
1 2 1
2 3 1
```

When vertex (2) is processed, both child and parent edge information eventually require color (1) at the same vertex. In the subset DP, the first fixed color occupies bit (0), while the second fixed color tries to occupy that same bit. Since the bit is already present, the transition produces no states. The DP value becomes zero and the final answer is `0`.

For a vertex with more than five incident edges, consider the six-edge star:

```
7
1 2 0
1 3 0
1 4 0
1 5 0
1 6 0
1 7 0
```

After five children have been processed, every possible mask has at most five bits set. The sixth child cannot choose any color whose bit is absent, so every transition produces zero. The final `ways` array is all zero, giving answer `0`. The implementation does not need a separate degree check because the five-bit state space naturally detects the impossibility.

For the case where a color repeats in different parts of the tree, consider:

```
4
1 2 1
2 3 2
3 4 1
```

The two color-1 edges are not adjacent, so there is no conflict. Every edge is already fixed, and every vertex sees distinct incident colors. The DP follows exactly one transition at every vertex and returns `1`. This confirms that the mask tracks colors only among edges incident to the current vertex, rather than incorrectly treating colors as globally unique.
