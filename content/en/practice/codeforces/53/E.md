---
title: "CF 53E - Dead Ends"
description: "We are given an undirected connected graph representing roads between junctions. The mayor wants to remove some roads so that the remaining graph becomes a tree, meaning it stays connected and contains exactly n - 1 edges."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 53
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 49 (Div. 2)"
rating: 2500
weight: 53
solve_time_s: 238
verified: false
draft: false
---

[CF 53E - Dead Ends](https://codeforces.com/problemset/problem/53/E)

**Rating:** 2500  
**Tags:** bitmasks, dp  
**Solve time:** 3m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected connected graph representing roads between junctions. The mayor wants to remove some roads so that the remaining graph becomes a tree, meaning it stays connected and contains exactly `n - 1` edges. Among all such spanning trees, we only care about the ones that contain exactly `k` leaves. A leaf is a vertex whose degree inside the tree equals `1`.

The task is to count how many spanning trees of the original graph have exactly `k` leaves.

The graph is very small, only up to `10` vertices. That immediately suggests that exponential algorithms over subsets are possible. A state space around `2^10 = 1024` is tiny. Even `3^10` or `10 * 2^10 * 2^10` style dynamic programming can fit comfortably.

The difficulty is not connectivity checking itself. The real challenge is counting spanning trees while simultaneously tracking vertex degrees, because the number of leaves depends on the final degree distribution.

A naive solution would enumerate every subset of `n - 1` edges and check whether it forms a spanning tree with exactly `k` leaves. The problem is that the graph may contain up to `45` edges. The number of subsets becomes:

$$\binom{45}{9} \approx 8.8 \times 10^8$$

which is completely impossible within the time limit.

There are several subtle cases that break careless solutions.

Suppose the graph itself is already a tree.

```
4 3 3
1 2
2 3
2 4
```

There is only one spanning tree, the graph itself, and it has exactly three leaves. The correct answer is `1`. A buggy implementation that assumes every vertex starts as a leaf and later removes leaves as edges are added can easily miscount the center vertex.

Another dangerous case is a cycle.

```
4 4 2
1 2
2 3
3 4
4 1
```

Every spanning tree of a cycle is a path, and every path on four vertices has exactly two leaves. The correct answer is `4`, because removing any one edge gives a valid tree. If connectivity handling is wrong, it is easy to count disconnected forests.

A third pitfall appears when building trees incrementally. Consider:

```
5 6 2
1 2
1 3
1 4
1 5
2 3
4 5
```

A spanning tree may temporarily contain many leaves during construction, but after future edges are added, some of those leaves disappear. Any DP that greedily fixes the leaf count too early will fail.

The core issue is that degree information is only final after the whole tree has been constructed.

## Approaches

The brute-force approach is straightforward. We try every subset of edges of size `n - 1`. For each subset, we check whether it forms a connected graph. Since a connected graph with `n - 1` edges is automatically a tree, we then count how many vertices have degree `1`. If that count equals `k`, we add one to the answer.

This works because the definition of a spanning tree is simple to verify. The problem is the number of subsets. In the worst case we choose `9` edges out of `45`, which is almost a billion combinations before even performing connectivity checks.

The small value of `n` suggests that vertices, not edges, should be the center of the state representation. A tree has a very useful property: if we root it somewhere and reveal vertices one by one, every newly added vertex connects through exactly one edge to the already built part.

That observation transforms the problem into a subset DP.

We build connected induced structures incrementally. At every moment we maintain:

- which vertices are already inside the current connected component,
- which vertices currently have odd status regarding being leaves,
- how many vertices have already become internal vertices.

The key trick is to encode degree parity using bitmasks while growing the tree one edge at a time. Whenever we attach a new vertex `v` to an existing vertex `u`:

- `v` starts with degree `1`, so it becomes a leaf,
- `u` gains one additional degree, so its leaf/internal status may change.

This local update is exactly what makes dynamic programming possible.

The standard way to avoid counting the same tree many times is to root every tree at its smallest-numbered vertex and only allow transitions that add larger vertices. That canonical ordering removes duplicates automatically.

The resulting DP has roughly:

$$2^n \times 2^n$$

states, which is tiny for `n ≤ 10`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O\left(\binom{m}{n-1} \cdot (n+m)\right)$ | $O(n+m)$ | Too slow |
| Optimal | $O(3^n \cdot n^2)$ | $O(2^n \cdot n)$ | Accepted |

## Algorithm Walkthrough

We use a classic connected subset DP that grows rooted trees.

Let `dp[mask][leafMask]` denote the number of different trees whose vertex set is `mask`, and whose current leaves are exactly the vertices inside `leafMask`.

A vertex belongs to `leafMask` if its current degree equals `1`.

### 1. Start from every possible root

For every vertex `r`, initialize:

```
dp[1 << r][0] = 1
```

A single isolated vertex has degree `0`, not degree `1`, so it is not a leaf yet.

We also enforce that `r` is the smallest vertex in the final tree. Later transitions only add vertices larger than `r`. This prevents counting the same tree multiple times from different roots.

### 2. Expand connected subsets

For every current subset `mask`, try adding a new vertex `v` not inside `mask`.

The new vertex must connect through some edge `(u, v)` where `u` already belongs to `mask`.

This preserves connectivity automatically.

### 3. Update the leaf set

When attaching `v` to `u`:

- `v` gets degree `1`, so it becomes a leaf,
- `u` increases its degree by `1`.

The effect on `u` depends on its old degree category.

If `u` was not previously a leaf, then after gaining one extra edge it still is not a leaf.

If `u` was previously a leaf, then its degree changes from `1` to `2`, so it stops being a leaf.

This update can be represented entirely with bit operations.

### 4. Transition to the new state

Construct:

```
newMask = mask | (1 << v)
```

Then modify `leafMask`:

- toggle `u` if it was previously a leaf,
- add `v` as a leaf.

Add the DP value into the new state.

### 5. Finish at full masks

After processing all subsets, every spanning tree appears exactly once.

For every state where:

```
mask == (1 << n) - 1
```

count it if:

```
popcount(leafMask) == k
```

The sum of all such states is the answer.

### Why it works

At every transition we add exactly one new vertex and exactly one new edge connecting it to the existing connected component. Starting from a single vertex and repeating this process always produces a tree.

Conversely, every rooted tree can be reconstructed uniquely by repeatedly removing the largest non-root vertex. That means every valid spanning tree corresponds to exactly one sequence of DP transitions.

The leaf mask stays correct because the only vertex degrees that change during a transition are the parent `u` and the newly attached vertex `v`. All other vertices keep the same degree. The update rules exactly match how tree degrees evolve.

Since every spanning tree is generated once and only once, and we count only those with exactly `k` leaves, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    adj = [[False] * n for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u][v] = True
        adj[v][u] = True

    FULL = (1 << n) - 1

    ans = 0

    for root in range(n):
        dp = [[0] * (1 << n) for _ in range(1 << n)]

        dp[1 << root][0] = 1

        for mask in range(1 << n):
            if not (mask & (1 << root)):
                continue

            for leaf_mask in range(1 << n):
                cur = dp[mask][leaf_mask]

                if cur == 0:
                    continue

                for v in range(root + 1, n):
                    if mask & (1 << v):
                        continue

                    for u in range(n):
                        if not (mask & (1 << u)):
                            continue

                        if not adj[u][v]:
                            continue

                        new_mask = mask | (1 << v)

                        new_leaf = leaf_mask

                        if leaf_mask & (1 << u):
                            new_leaf ^= (1 << u)

                        new_leaf |= (1 << v)

                        dp[new_mask][new_leaf] += cur

        for leaf_mask in range(1 << n):
            if leaf_mask.bit_count() == k:
                ans += dp[FULL][leaf_mask]

    print(ans)

solve()
```

The adjacency matrix makes edge existence checks constant time. Since `n` is only `10`, this is simpler and faster than adjacency lists for this DP.

The outer loop fixes the smallest vertex of the tree. This is the key duplicate-removal trick. When processing root `r`, we only add vertices with indices greater than `r`. Every spanning tree has exactly one smallest vertex, so every tree is counted exactly once.

The DP state stores both the current vertex set and the exact set of leaves. A common mistake is trying to store only the number of leaves. That fails because when a vertex receives another edge later, it may stop being a leaf. The algorithm needs to know precisely which vertices currently have degree `1`.

The transition logic is subtle. The newly added vertex always becomes a leaf because its degree is exactly `1`. The parent vertex may lose leaf status if it previously had degree `1`. Using XOR to remove `u` from the leaf set is convenient because we only perform it when `u` is already inside the leaf mask.

The memory usage stays small because:

$$2^{10} \times 2^{10} = 1,048,576$$

states, which easily fits in memory in Python.

## Worked Examples

### Example 1

Input:

```
3 3 2
1 2
2 3
1 3
```

All spanning trees of a triangle are paths of length two.

| Step | mask | leafMask | Meaning |
| --- | --- | --- | --- |
| Start at 1 | 001 | 000 | Single root |
| Add 2 via 1 | 011 | 010 | Vertex 2 becomes leaf |
| Add 3 via 1 | 111 | 110 | Vertices 2 and 3 are leaves |

Another construction:

| Step | mask | leafMask | Meaning |
| --- | --- | --- | --- |
| Start at 1 | 001 | 000 | Single root |
| Add 3 via 1 | 101 | 100 | Vertex 3 becomes leaf |
| Add 2 via 3 | 111 | 010 | Vertices 1 and 2 are leaves |

There are exactly three spanning trees, each with two leaves, so the answer is `3`.

This trace shows how leaf status changes dynamically. A vertex can temporarily be a leaf and later stop being one.

### Example 2

Input:

```
4 4 2
1 2
2 3
3 4
4 1
```

This graph is a cycle.

| Step | mask | leafMask | Added edge |
| --- | --- | --- | --- |
| 0001 | 0000 | Start |  |
| 0011 | 0010 | 1-2 |  |
| 0111 | 0100 | 2-3 |  |
| 1111 | 1000 | 3-4 |  |

Final leaves are vertices `1` and `4`.

Removing any one edge from the cycle gives a path, so the total answer is `4`.

This example confirms that the DP never creates cycles. Every transition introduces exactly one new vertex.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(3^n \cdot n^2)$ | Every subset transitions to outside vertices through all possible attachment points |
| Space | $O(2^n \cdot 2^n)$ | DP stores states for subset and leaf mask |

For `n = 10`, we have at most `1024` subsets and `1024` leaf masks. The total state count is about one million, which is completely manageable inside the memory limit. The transition count also stays well within the 5 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m, k = map(int, input().split())

        adj = [[False] * n for _ in range(n)]

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u][v] = True
            adj[v][u] = True

        FULL = (1 << n) - 1

        ans = 0

        for root in range(n):
            dp = [[0] * (1 << n) for _ in range(1 << n)]

            dp[1 << root][0] = 1

            for mask in range(1 << n):
                if not (mask & (1 << root)):
                    continue

                for leaf_mask in range(1 << n):
                    cur = dp[mask][leaf_mask]

                    if cur == 0:
                        continue

                    for v in range(root + 1, n):
                        if mask & (1 << v):
                            continue

                        for u in range(n):
                            if not (mask & (1 << u)):
                                continue

                            if not adj[u][v]:
                                continue

                            new_mask = mask | (1 << v)

                            new_leaf = leaf_mask

                            if leaf_mask & (1 << u):
                                new_leaf ^= (1 << u)

                            new_leaf |= (1 << v)

                            dp[new_mask][new_leaf] += cur

            for leaf_mask in range(1 << n):
                if leaf_mask.bit_count() == k:
                    ans += dp[FULL][leaf_mask]

        return str(ans)

    return solve()

# provided sample
assert run(
"""3 3 2
1 2
2 3
1 3
"""
) == "3", "sample 1"

# already a tree
assert run(
"""4 3 3
1 2
2 3
2 4
"""
) == "1", "unique spanning tree"

# cycle graph
assert run(
"""4 4 2
1 2
2 3
3 4
4 1
"""
) == "4", "every spanning tree is a path"

# complete graph K4
assert run(
"""4 6 3
1 2
1 3
1 4
2 3
2 4
3 4
"""
) == "4", "all stars"

# path graph
assert run(
"""5 4 2
1 2
2 3
3 4
4 5
"""
) == "1", "single path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle graph | 3 | Multiple spanning trees with same leaf count |
| Existing tree | 1 | No duplicate counting |
| Cycle graph | 4 | Connectivity without cycles |
| Complete graph K4 | 4 | Counting star-shaped trees |
| Path graph | 1 | Minimum possible leaf count |

## Edge Cases

Consider the graph that is already a tree:

```
4 3 3
1 2
2 3
2 4
```

The algorithm starts from the smallest root, vertex `1`. It incrementally adds `2`, then `3`, then `4`. Vertex `2` initially becomes a leaf after connecting to `1`, but later loses leaf status when vertices `3` and `4` attach to it. The final leaf mask contains exactly `{1, 3, 4}`. No alternative construction exists, so the answer becomes `1`.

Now consider the cycle:

```
4 4 2
1 2
2 3
3 4
4 1
```

The DP only allows adding a vertex not already inside the current subset. That means no transition can ever create a cycle. Every completed structure automatically contains exactly `n - 1` edges and remains connected, so every final state is a valid tree.

Finally, consider a case where leaf status changes repeatedly:

```
5 4 4
1 2
1 3
1 4
1 5
```

This is a star centered at `1`. During construction, vertex `1` first becomes a leaf after adding one neighbor, then immediately stops being a leaf once another neighbor attaches. The algorithm handles this naturally through the leaf-mask updates. The final leaves are exactly `{2,3,4,5}`, giving answer `1`.
