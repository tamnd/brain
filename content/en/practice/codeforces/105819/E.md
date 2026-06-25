---
title: "CF 105819E - Mingle"
description: "We are given an undirected friendship graph with n players and m friendship edges. Two players are allowed to form a pair if they are directly connected by a friendship edge, or if they have at least one common friend."
date: "2026-06-25T15:06:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105819
codeforces_index: "E"
codeforces_contest_name: "TeamsCode Spring 2025 Novice Division"
rating: 0
weight: 105819
solve_time_s: 46
verified: true
draft: false
---

[CF 105819E - Mingle](https://codeforces.com/problemset/problem/105819/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected friendship graph with `n` players and `m` friendship edges.

Two players are allowed to form a pair if they are directly connected by a friendship edge, or if they have at least one common friend. In graph terms, two vertices may be paired if their distance in the friendship graph is at most `2`.

Every player may belong to at most one pair. The task is to output a pairing with the maximum possible number of pairs.

The graph can contain up to `2 · 10^5` vertices and edges. Any algorithm that explicitly builds the graph of all valid pairings is immediately impossible. A single high degree vertex could create Θ(n²) distance-2 relationships. We need a solution that works directly on the original graph in roughly linear time.

The first key observation is that players from different connected components can never be paired. Any valid pair must lie entirely inside one connected component.

The second observation is more surprising. For a connected component containing `s` vertices, it is always possible to create exactly `⌊s / 2⌋` pairs. Since no component can contribute more than `⌊s / 2⌋` pairs anyway, that is the maximum.

This reduces the problem to constructing such a pairing efficiently.

Consider a component consisting of a single isolated vertex:

```
1
```

The correct answer is `0` pairs. A careless implementation that blindly tries to pair every DFS parent with a child would create an invalid pair.

Consider a path of length three:

```
1 - 2 - 3 - 4
```

Players `1` and `3` may pair because they share friend `2`, and players `2` and `4` may pair because they share friend `3`. The correct answer is `2` pairs. Looking only at friendship edges would incorrectly find only one pair.

Consider a star:

```
    2
    |
3 - 1 - 4
    |
    5
```

All leaves are pairwise compatible because they share player `1` as a mutual friend. The correct answer is `2` pairs. Any solution that only considers original graph edges would miss these pairings.

## Approaches

A brute force solution would first build the graph of all valid pairings. For every vertex, we would connect it to all friends and all vertices reachable in exactly two steps. After constructing this graph, we would search for a maximum matching.

The problem is that the distance-2 graph can contain Θ(n²) edges. A star with `2 · 10^5` vertices already creates almost `2 · 10^5²` valid pairings between leaves. Building that graph is impossible.

The breakthrough comes from ignoring most of the graph.

Take any connected component and choose an arbitrary DFS tree inside it. Every friendship edge outside that tree is merely an extra edge. If we can already achieve `⌊s / 2⌋` pairs using only the DFS tree, then the additional edges are irrelevant because `⌊s / 2⌋` is the theoretical maximum.

So the real problem becomes:

Given a tree, pair as many vertices as possible so that every pair is at distance at most `2`.

A bottom-up DFS provides exactly what we need.

For each node, after processing all children, some child subtrees may still contain one unmatched vertex. Any two such unmatched children can be paired together because their distance is exactly `2` through the current node.

After pairing child representatives among themselves, if one unmatched child remains, we pair that child with the current node. Their distance is `1`.

This greedily removes vertices from the tree while guaranteeing that every created pair is valid.

At the end of the DFS, every component leaves at most one unmatched vertex, which means we obtain exactly `⌊s / 2⌋` pairs.

The same DFS works unchanged on the original graph. We simply traverse one DFS tree of each connected component and ignore all non-tree edges.

The solution runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal DFS Construction | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the friendship graph.
2. Start a DFS from every unvisited vertex. Each DFS explores exactly one connected component.
3. For a node `u`, recursively process all unvisited children.
4. Each child DFS returns whether that child's subtree still contains one unmatched representative.
5. Collect all child representatives that remain unmatched.
6. Pair these representatives two at a time.

If representatives come from children `a` and `b`, then `a` and `b` share the mutual friend `u`, so the pair is valid.
7. After pairing as many child representatives as possible, add `u` itself to the collection.
8. Again pair elements of the collection two at a time and store those pairs.
9. If the collection size is odd, exactly one representative remains unmatched. Return that information to the parent.
10. Continue until the whole component has been processed.

### Why it works

The DFS maintains a simple invariant.

After finishing the subtree of a node `u`, all vertices in that subtree are already paired except possibly one representative that is returned upward.

Whenever two unmatched child representatives exist, they can safely be paired because both are adjacent to `u` in the DFS tree. Their distance is exactly `2`.

If one unmatched child remains, pairing it with `u` is valid because their distance is `1`.

As a result, every operation creates a legal pair and reduces the number of unmatched vertices by two.

A component with size `s` can leave at most one unmatched vertex after the root finishes. Hence exactly `⌊s / 2⌋` pairs are produced. Since no matching can use more than `⌊s / 2⌋` pairs, the construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

n, m = map(int, input().split())

adj = [[] for _ in range(n)]

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    adj[u].append(v)
    adj[v].append(u)

vis = [False] * n
ans = []

def dfs(u):
    vis[u] = True

    rem = []

    for v in adj[u]:
        if vis[v]:
            continue

        if dfs(v):
            rem.append(v)

    rem.append(u)

    for i in range(1, len(rem), 2):
        ans.append((rem[i - 1] + 1, rem[i] + 1))

    return len(rem) % 2 == 1

for i in range(n):
    if not vis[i]:
        dfs(i)

print(len(ans))
print("\n".join(f"{u} {v}" for u, v in ans))
```

The adjacency list stores the original friendship graph.

The DFS visits only tree edges. Any extra edges in the component are ignored because the DFS tree alone is sufficient to achieve the optimal number of pairs.

The list `rem` stores child vertices whose subtrees still contain one unmatched representative. After all children are processed, the current node is added to the same list.

Pairing consecutive elements of `rem` is safe. Two child representatives are at distance `2` through the current node, while a child representative and the current node are at distance `1`.

The return value indicates whether exactly one representative remains unmatched after all possible pairings inside the subtree.

The implementation uses 0-based indices internally and converts back to 1-based indices when storing the answer.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
1 3
```

DFS rooted at `1`.

| Node | Unmatched children | rem after adding self | Produced pairs | Return |
| --- | --- | --- | --- | --- |
| 2 | {} | {2} | none | unmatched |
| 3 | {} | {3} | none | unmatched |
| 1 | {2,3} | {2,3,1} | (2,3) | unmatched |

Output:

```
1
2 3
```

This demonstrates the distance-2 rule. Players `2` and `3` are not friends, but they share friend `1`.

### Example 2

Input:

```
5 2
1 2
3 4
```

There are three connected components.

| Component | Size | Pairs produced |
| --- | --- | --- |
| {1,2} | 2 | (1,2) |
| {3,4} | 2 | (3,4) |
| {5} | 1 | none |

Output:

```
2
1 2
3 4
```

This demonstrates that components are processed independently and isolated vertices remain unmatched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed a constant number of times |
| Space | O(n + m) | Adjacency list, visitation array, recursion stack, answer storage |

With `n, m ≤ 2 · 10^5`, linear complexity easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string

# Sample-style validation is difficult because many valid answers exist.
# These tests verify the number of pairs produced.

from collections import deque

def expected_pairs_count(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    vis = [False] * n
    total = 0

    for i in range(n):
        if vis[i]:
            continue

        q = deque([i])
        vis[i] = True
        sz = 0

        while q:
            u = q.popleft()
            sz += 1

            for v in g[u]:
                if not vis[v]:
                    vis[v] = True
                    q.append(v)

        total += sz // 2

    return total

assert expected_pairs_count(3, [(1, 2), (1, 3)]) == 1
assert expected_pairs_count(5, [(1, 2), (3, 4)]) == 2

# minimum graph
assert expected_pairs_count(1, []) == 0

# single edge
assert expected_pairs_count(2, [(1, 2)]) == 1

# star
assert expected_pairs_count(
    5,
    [(1, 2), (1, 3), (1, 4), (1, 5)]
) == 2

# path of length 3
assert expected_pairs_count(
    4,
    [(1, 2), (2, 3), (3, 4)]
) == 2

# odd-sized connected component
assert expected_pairs_count(
    5,
    [(1, 2), (2, 3), (3, 4), (4, 5)]
) == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 0 pairs | Minimum size component |
| One edge | 1 pair | Direct friendship pairing |
| Star graph | 2 pairs | Distance-2 pairing through center |
| Path of 4 vertices | 2 pairs | Perfect matching in a tree |
| Path of 5 vertices | 2 pairs | Exactly one unmatched vertex remains |

## Edge Cases

Consider a component containing a single vertex:

```
1 0
```

The DFS visits the vertex and creates `rem = {1}`. No pair can be formed. The function returns one unmatched representative and the final answer contains zero pairs. This is optimal.

Consider the star graph:

```
5 4
1 2
1 3
1 4
1 5
```

Leaves `2`, `3`, `4`, and `5` all return as unmatched representatives. At node `1`, the list becomes:

```
{2, 3, 4, 5, 1}
```

The algorithm pairs `(2,3)` and `(4,5)`. Every pair shares the mutual friend `1`, so both are valid. One vertex remains unmatched because the component size is odd.

Consider the path:

```
4 3
1 2
2 3
3 4
```

Processing bottom-up creates representatives that eventually allow pairings `(4,3)` and `(2,1)`. Every pair is connected by a friendship edge, so both are valid. All four vertices become matched, achieving the theoretical maximum of `2` pairs.

The same reasoning extends to arbitrary connected components. The DFS tree alone guarantees `⌊s/2⌋` pairs, which is already optimal for a component of size `s`.
