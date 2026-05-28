---
title: "CF 141E - Clearing Up"
description: "We are given an undirected graph where every edge already belongs to one of two categories. Roads marked \"S\" are narrow roads that the Elf clears, and roads marked \"M\" are wide roads that Santa clears. We must choose a subset of roads satisfying two conditions at the same time."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 141
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 101 (Div. 2)"
rating: 2300
weight: 141
solve_time_s: 171
verified: true
draft: false
---

[CF 141E - Clearing Up](https://codeforces.com/problemset/problem/141/E)

**Rating:** 2300  
**Tags:** constructive algorithms, dp, dsu, graphs  
**Solve time:** 2m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph where every edge already belongs to one of two categories. Roads marked `"S"` are narrow roads that the Elf clears, and roads marked `"M"` are wide roads that Santa clears.

We must choose a subset of roads satisfying two conditions at the same time.

First, the chosen roads must form a tree over all huts. Between every pair of huts there must be exactly one simple path, which is the defining property of a spanning tree. A spanning tree on `n` vertices always contains exactly `n - 1` edges.

Second, the number of `"S"` edges and `"M"` edges inside that spanning tree must be equal.

That immediately gives an important observation. Since the tree has `n - 1` edges total, this number must be even. Otherwise it is impossible to split the edges evenly between the two types.

The graph is small in terms of vertices, only up to `1000`, but the number of edges can reach `100000`. This changes the shape of the solution completely. Algorithms that try many subsets of edges are hopeless, but algorithms based on repeated DSU operations are fast enough because DSU runs almost in constant amortized time. An `O(m α(n))` or `O(m log n)` solution is easily acceptable.

There are several easy-to-miss edge cases.

A graph may already be disconnected even if we ignore edge types.

```
4 2
1 2 S
3 4 M
```

No spanning tree exists here, so the correct answer is `-1`.

Another subtle case appears when one edge type cannot appear enough times in any spanning tree.

```
3 2
1 2 S
2 3 S
```

A spanning tree exists, but it contains only `"S"` edges. Since a valid answer needs one `"S"` and one `"M"` edge, the answer is still `-1`.

Self-loops are another trap.

```
2 2
1 1 S
1 2 M
```

The self-loop never helps connect components, so a careless implementation that blindly counts edges by type could incorrectly accept it.

Parallel edges also matter.

```
2 3
1 2 S
1 2 S
1 2 M
```

Only one edge can appear in a spanning tree. The algorithm must treat every edge independently and avoid adding cycle-forming duplicates.

## Approaches

The brute-force idea is straightforward. A spanning tree on `n` vertices contains exactly `n - 1` edges, so we could try every subset of that size, check whether it forms a tree, and verify that the number of `"S"` and `"M"` edges are equal.

This works logically because the constraints defining a valid answer are easy to test. Connectivity and acyclicity can both be checked with DSU or DFS.

The problem is the number of subsets. In the worst case we would examine

$$\binom{100000}{999}$$

subsets, which is completely impossible.

The key observation is that the only difficult part is balancing the number of edge types. The spanning-tree structure itself is easy to manage with DSU.

Suppose `k = (n - 1) / 2`. Any valid tree must contain exactly `k` `"S"` edges and exactly `k` `"M"` edges.

Instead of constructing the whole tree at once, we can think in terms of feasibility ranges.

First, what is the minimum number of `"S"` edges that any spanning tree must contain? If we greedily connect components using only `"M"` edges first, then every remaining forced connection must use `"S"` edges. This gives the minimum possible number of `"S"` edges.

Similarly, if we greedily use `"S"` edges first, we get the maximum possible number of `"S"` edges.

If `k` is outside this interval, no answer exists.

Even better, once feasibility is confirmed, we can explicitly construct such a tree. We first force exactly `k` `"S"` edges while preserving extendability to a spanning tree. Then we finish the remaining connections using `"M"` edges.

The entire solution becomes a sequence of DSU passes over the edge list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(m α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all edges and split them into two lists, `"S"` edges and `"M"` edges.
2. If `n - 1` is odd, immediately print `-1`.

A valid spanning tree would need equal counts of both edge types, so the total number of edges must be divisible by two.
3. Let `k = (n - 1) / 2`.
4. Compute the minimum possible number of `"S"` edges in any spanning tree.

Start a DSU and greedily add all possible `"M"` edges first. After that, try adding `"S"` edges. Every `"S"` edge that actually merges two components is unavoidable, so count it.
5. If this minimum exceeds `k`, print `-1`.

Every spanning tree would contain too many `"S"` edges.
6. Compute the maximum possible number of `"S"` edges.

Start another DSU and greedily add all possible `"S"` edges first. Count how many were added.
7. If this maximum is smaller than `k`, print `-1`.

No spanning tree can contain enough `"S"` edges.
8. Construct exactly `k` `"S"` edges.

Start with a fresh DSU. First greedily add `"S"` edges whenever they connect different components. Store these edges temporarily.

This creates a maximal forest using `"S"` edges.
9. Some of those `"S"` edges may be unnecessary. We only need exactly `k`.

Rebuild the DSU from scratch. Iterate over the stored `"S"` edges and add them one by one until exactly `k` have been chosen.
10. Continue scanning all `"S"` edges again.

If we still have fewer than `k` selected `"S"` edges, add more whenever they connect different components.

At this point we have exactly `k` `"S"` edges forming a forest.
11. Finish the spanning tree using `"M"` edges.

Iterate over all `"M"` edges and add any edge whose endpoints belong to different components.
12. If the total number of selected edges is not `n - 1`, print `-1`.

Otherwise output the chosen edge indices.

### Why it works

The minimum and maximum feasibility checks are based on a standard spanning-tree exchange argument. Greedily taking all possible `"M"` edges minimizes the number of required `"S"` edges because every avoided merge using `"M"` would only force another `"S"` merge later. The symmetric argument gives the maximum.

During construction, the selected `"S"` edges always form an acyclic forest. Every time we add one, it merges two previously disconnected components. Since the feasibility interval already proved that exactly `k` `"S"` edges are achievable, we can safely stop after selecting `k` such edges and complete the remaining connections using `"M"` edges.

The final DSU state guarantees both acyclicity and connectivity. We only add edges connecting different components, so cycles never appear. A spanning tree on `n` vertices with `n - 1` edges is automatically connected and acyclic.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def solve():
    n, m = map(int, input().split())

    edges_s = []
    edges_m = []

    all_edges = []

    for idx in range(1, m + 1):
        u, v, t = input().split()
        u = int(u)
        v = int(v)

        edge = (u, v, idx)

        all_edges.append((u, v, t, idx))

        if t == 'S':
            edges_s.append(edge)
        else:
            edges_m.append(edge)

    if (n - 1) % 2:
        print(-1)
        return

    k = (n - 1) // 2

    # minimum possible number of S edges
    dsu = DSU(n)

    for u, v, _ in edges_m:
        dsu.union(u, v)

    min_s = 0

    for u, v, _ in edges_s:
        if dsu.union(u, v):
            min_s += 1

    if min_s > k:
        print(-1)
        return

    # maximum possible number of S edges
    dsu = DSU(n)

    max_s = 0

    for u, v, _ in edges_s:
        if dsu.union(u, v):
            max_s += 1

    if max_s < k:
        print(-1)
        return

    # build exactly k S edges
    dsu = DSU(n)

    useful_s = []

    for u, v, idx in edges_s:
        if dsu.union(u, v):
            useful_s.append((u, v, idx))

    dsu = DSU(n)

    answer = []
    used_s = 0

    for u, v, idx in useful_s:
        if used_s == k:
            break

        if dsu.union(u, v):
            answer.append(idx)
            used_s += 1

    for u, v, idx in edges_s:
        if used_s == k:
            break

        if dsu.union(u, v):
            answer.append(idx)
            used_s += 1

    # finish with M edges
    for u, v, idx in edges_m:
        if dsu.union(u, v):
            answer.append(idx)

    if len(answer) != n - 1:
        print(-1)
        return

    print(len(answer))
    print(*answer)

solve()
```

The first important detail is separating `"S"` and `"M"` edges. The entire construction depends on processing the two types independently.

The minimum and maximum feasibility checks reuse the same DSU structure but in opposite orders. The ordering is the whole argument. Adding all `"M"` edges first leaves only forced `"S"` merges, while adding all `"S"` edges first maximizes how many such edges can participate.

The construction phase has a subtle two-stage structure. The first pass over `"S"` edges computes a maximal forest of potentially useful `"S"` edges. The second pass carefully selects only `k` of them.

Without rebuilding the DSU before that second phase, we would accidentally keep too many `"S"` edges already merged into the structure.

Another easy mistake is assuming that reaching exactly `k` `"S"` edges automatically guarantees connectivity. It does not. The final pass over `"M"` edges is still necessary to connect all remaining components.

The final check `len(answer) != n - 1` catches disconnected cases cleanly.

## Worked Examples

### Example 1

Input:

```
1 2
1 1 S
1 1 M
```

Here `n - 1 = 0`, so `k = 0`.

| Step | Action | Selected edges | Components |
| --- | --- | --- | --- |
| Initial | No edges needed | {} | 1 |
| Final | Tree already complete | {} | 1 |

Output:

```
0
```

This example confirms that a graph with one vertex requires no edges at all. Self-loops are ignored because they never merge components.

### Example 2

Input:

```
3 3
1 2 S
2 3 M
1 3 S
```

We need exactly one `"S"` edge and one `"M"` edge.

| Step | Edge considered | Accepted | Used S | DSU components |
| --- | --- | --- | --- | --- |
| 1 | 1-2 S | Yes | 1 | {1,2}, {3} |
| 2 | 1-3 S | Skipped temporarily | 1 | {1,2}, {3} |
| 3 | 2-3 M | Yes | 1 | {1,2,3} |

Chosen edges are `{1, 2}`.

This trace demonstrates the key invariant. The `"S"` edges are chosen only while they expand the forest, and the `"M"` edge finishes connectivity without creating a cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m α(n)) | Each edge participates in a constant number of DSU operations |
| Space | O(n) | DSU arrays and answer storage |

The graph contains at most `100000` edges, so linear passes over the edge list are completely fine. DSU operations are effectively constant time because inverse Ackermann growth is tiny in practice. The solution easily fits inside both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.size = [1] * (n + 1)

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)

            if a == b:
                return False

            if self.size[a] < self.size[b]:
                a, b = b, a

            self.parent[b] = a
            self.size[a] += self.size[b]
            return True

    n, m = map(int, input().split())

    edges_s = []
    edges_m = []

    for idx in range(1, m + 1):
        u, v, t = input().split()
        u = int(u)
        v = int(v)

        if t == 'S':
            edges_s.append((u, v, idx))
        else:
            edges_m.append((u, v, idx))

    if (n - 1) % 2:
        return "-1"

    k = (n - 1) // 2

    dsu = DSU(n)

    for u, v, _ in edges_m:
        dsu.union(u, v)

    min_s = 0

    for u, v, _ in edges_s:
        if dsu.union(u, v):
            min_s += 1

    if min_s > k:
        return "-1"

    dsu = DSU(n)

    max_s = 0

    for u, v, _ in edges_s:
        if dsu.union(u, v):
            max_s += 1

    if max_s < k:
        return "-1"

    dsu = DSU(n)

    useful_s = []

    for u, v, idx in edges_s:
        if dsu.union(u, v):
            useful_s.append((u, v, idx))

    dsu = DSU(n)

    ans = []
    used_s = 0

    for u, v, idx in useful_s:
        if used_s == k:
            break

        if dsu.union(u, v):
            ans.append(idx)
            used_s += 1

    for u, v, idx in edges_s:
        if used_s == k:
            break

        if dsu.union(u, v):
            ans.append(idx)
            used_s += 1

    for u, v, idx in edges_m:
        if dsu.union(u, v):
            ans.append(idx)

    if len(ans) != n - 1:
        return "-1"

    return str(len(ans))

# provided sample
assert run(
"""1 2
1 1 S
1 1 M
"""
) == "0", "sample 1"

# impossible because n-1 is odd
assert run(
"""2 1
1 2 S
"""
) == "-1", "odd tree size"

# disconnected graph
assert run(
"""4 2
1 2 S
3 4 M
"""
) == "-1", "disconnected"

# only one edge type available
assert run(
"""3 2
1 2 S
2 3 S
"""
) == "-1", "cannot balance types"

# simple valid case
assert run(
"""3 3
1 2 S
2 3 M
1 3 S
"""
) == "2", "balanced spanning tree exists"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node with loops | 0 | Self-loops are ignored correctly |
| `n - 1` odd | -1 | Equal split impossible |
| Disconnected graph | -1 | Connectivity requirement enforced |
| Only one edge type | -1 | Feasibility interval check |
| Small balanced graph | 2 | Successful construction |

## Edge Cases

Consider the disconnected graph:

```
4 2
1 2 S
3 4 M
```

The minimum `"S"` computation starts by adding the `"M"` edge, producing components `{1}`, `{2}`, `{3,4}`. The `"S"` edge merges `{1}` and `{2}`, leaving two connected components overall. Since the final graph can never become connected, the construction phase ends with fewer than `n - 1` edges and correctly prints `-1`.

Now consider the graph with only `"S"` edges:

```
3 2
1 2 S
2 3 S
```

Here `k = 1`. The maximum possible number of `"S"` edges is `2`, but the minimum possible number of `"S"` edges is also `2` because there are no `"M"` edges at all. Since `min_s > k`, the algorithm immediately rejects the instance.

Finally, consider parallel edges:

```
2 3
1 2 S
1 2 S
1 2 M
```

The DSU accepts only the first edge that merges the two vertices. Every later parallel edge is rejected because both endpoints already belong to the same component. This guarantees the final answer remains acyclic.
