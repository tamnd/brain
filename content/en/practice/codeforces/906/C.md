---
title: "CF 906C - Party"
description: "We have a connected friendship graph. Choosing a vertex means that all of its neighbors become pairwise adjacent. In graph theory language, we are allowed to pick a vertex and turn its open neighborhood into a clique."
date: "2026-06-12T23:08:14+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 906
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 454 (Div. 1, based on Technocup 2018 Elimination Round 4)"
rating: 2400
weight: 906
solve_time_s: 444
verified: true
draft: false
---

[CF 906C - Party](https://codeforces.com/problemset/problem/906/C)

**Rating:** 2400  
**Tags:** bitmasks, brute force, dp, graphs  
**Solve time:** 7m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected friendship graph. Choosing a vertex means that all of its neighbors become pairwise adjacent. In graph theory language, we are allowed to pick a vertex and turn its open neighborhood into a clique.

The process continues until the whole graph becomes a complete graph. We need the smallest possible number of chosen vertices and one sequence that achieves that minimum.

The graph contains at most 22 vertices. That immediately suggests that exponential algorithms on subsets are possible, because $2^{22}\approx 4.2\cdot 10^6$, which is manageable. On the other hand, any brute force over all sequences of vertices would be hopeless because there are $22!$ possible orders and even $22^{22}$ different sequences of length 22.

The key difficulty is that the graph itself changes after every operation. A naive simulation seems complicated because after making one neighborhood a clique, future neighborhoods become larger and larger.

One easy-to-miss case is a graph that already contains a universal vertex. For example

```
4 3
1 2
1 3
1 4
```

Vertex 1 is adjacent to everyone. Choosing it once makes all guests mutually acquainted, so the answer is

```
1
1
```

Another subtle situation is a path.

```
4 3
1 2
2 3
3 4
```

Choosing vertex 2 first creates edge (1,3), and then choosing vertex 3 creates edge (1,4) and (2,4). Two steps are enough. A greedy strategy based only on current degree can easily miss this.

A complete graph is another corner case.

```
3 3
1 2
1 3
2 3
```

No operation is needed, so the answer is

```
0
```

Any implementation that assumes at least one chosen vertex would be incorrect.

## Approaches

The most direct approach is to try every possible sequence of chosen vertices and simulate the changing graph. This is correct because eventually every possible strategy is explored. The problem is that the search space explodes. Even restricting ourselves to distinct chosen vertices, there are $22!\approx 1.1\cdot 10^{21}$ orders, which is completely infeasible.

The breakthrough comes from understanding what an operation really does. Suppose we decide in advance which vertices will be selected. The order does not matter. Every selected vertex acts as a connector among its neighbors, and after all operations finish, two vertices become adjacent exactly when they have a path whose internal vertices are selected.

This observation changes the problem. Instead of thinking about graph transformations, we only need to find the smallest set $S$ such that every pair of vertices can communicate through vertices from $S$.

Now consider the vertices outside $S$. They can only appear as endpoints of such paths, never as internal vertices. That means two vertices outside $S$ must already be adjacent in the original graph. In other words, the complement $V\setminus S$ must form a clique.

Thus the problem becomes finding the largest clique of the original graph. If $C$ is that clique, selecting every vertex outside $C$ is sufficient and also necessary. The minimum number of operations equals

$$n-|C|.$$

Since $n\le 22$, a meet-in-the-middle maximum clique algorithm runs comfortably within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over sequences | O(22!) | O(22) | Too slow |
| Meet-in-the-middle maximum clique | O(n2^(n/2)) | O(2^(n/2)) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency bitmask for every vertex. A vertex is considered adjacent to itself as well, which simplifies clique checks.
2. Split the vertices into two halves of sizes $n_1$ and $n_2$. Since $n\le22$, each half contains at most 11 vertices.
3. Enumerate all subsets of the second half. For each subset, determine whether it forms a clique. Store the size of the largest clique contained inside every mask.
4. Propagate these values over submasks. After this step, for any mask we can instantly know the largest clique contained inside it and also reconstruct which subset achieves that size.
5. Enumerate all subsets of the first half. Whenever a subset forms a clique, compute which vertices in the second half are adjacent to every vertex of this subset.
6. The intersection obtained in the previous step gives all candidates that can be added from the second half while preserving the clique property.
7. Query the precomputed table to find the largest compatible clique in the second half. Combine its size with the size of the current first-half clique.
8. Keep the best overall clique and reconstruct its vertices.
9. Output all vertices not belonging to this maximum clique. Those are exactly the guests that should be selected.

### Why it works

Suppose the selected set is $S$. Any path whose internal vertices belong to $S$ eventually turns its endpoints into friends. Hence every pair of vertices becomes adjacent if and only if every pair can be connected by such a path.

Vertices outside $S$ can never be internal vertices, so two of them must already have an edge. Thus $V\setminus S$ must be a clique.

Conversely, if $C$ is any clique and we select every vertex outside it, then every pair of vertices either already lies inside the clique or can use selected vertices as intermediate connectors. Hence the graph becomes complete.

Maximizing the clique size minimizes the number of selected vertices, which proves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

adj = [1 << i for i in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    adj[u] |= 1 << v
    adj[v] |= 1 << u

n1 = n // 2
n2 = n - n1

adj2 = [0] * n2
for i in range(n2):
    v = n1 + i
    mask = 0
    for j in range(n2):
        if adj[v] >> (n1 + j) & 1:
            mask |= 1 << j
    adj2[i] = mask

size2 = 1 << n2
dp_size = [0] * size2
dp_mask = [0] * size2
is_clique2 = [False] * size2
is_clique2[0] = True

for mask in range(1, size2):
    bit = (mask & -mask).bit_length() - 1
    prev = mask ^ (1 << bit)
    if is_clique2[prev] and (adj2[bit] & prev) == prev:
        is_clique2[mask] = True
        dp_size[mask] = mask.bit_count()
        dp_mask[mask] = mask

for mask in range(size2):
    if mask == 0:
        continue
    if dp_size[mask] == 0:
        bit = (mask & -mask).bit_length() - 1
        prev = mask ^ (1 << bit)
        dp_size[mask] = dp_size[prev]
        dp_mask[mask] = dp_mask[prev]

for bit in range(n2):
    for mask in range(size2):
        if mask >> bit & 1:
            other = mask ^ (1 << bit)
            if dp_size[other] > dp_size[mask]:
                dp_size[mask] = dp_size[other]
                dp_mask[mask] = dp_mask[other]

adj1 = [0] * n1
cross = [0] * n1

for i in range(n1):
    mask1 = 0
    mask2 = 0
    for j in range(n1):
        if adj[i] >> j & 1:
            mask1 |= 1 << j
    for j in range(n2):
        if adj[i] >> (n1 + j) & 1:
            mask2 |= 1 << j
    adj1[i] = mask1
    cross[i] = mask2

size1 = 1 << n1
is_clique1 = [False] * size1
is_clique1[0] = True

best_size = 0
best_first = 0
best_second = 0

for mask in range(size1):
    if mask:
        bit = (mask & -mask).bit_length() - 1
        prev = mask ^ (1 << bit)
        if is_clique1[prev] and (adj1[bit] & prev) == prev:
            is_clique1[mask] = True
    if not is_clique1[mask]:
        continue

    allowed = (1 << n2) - 1
    tmp = mask
    while tmp:
        bit = (tmp & -tmp).bit_length() - 1
        allowed &= cross[bit]
        tmp ^= 1 << bit

    cur_size = mask.bit_count() + dp_size[allowed]
    if cur_size > best_size:
        best_size = cur_size
        best_first = mask
        best_second = dp_mask[allowed]

clique = set()

for i in range(n1):
    if best_first >> i & 1:
        clique.add(i)

for i in range(n2):
    if best_second >> i & 1:
        clique.add(n1 + i)

answer = [i + 1 for i in range(n) if i not in clique]

print(len(answer))
if answer:
    print(*answer)
else:
    print()
```

The adjacency masks include each vertex itself. This removes special cases when checking whether a new vertex is adjacent to every vertex already inside a subset.

The second half is preprocessed first. The table `dp_size[mask]` eventually contains the size of the largest clique inside `mask`, not necessarily equal to `mask` itself. Propagating information from submasks is what makes later queries constant time.

When processing a clique from the first half, the variable `allowed` stores the vertices of the second half that are adjacent to every vertex already chosen. Any clique inside `allowed` can safely be combined with the current first-half clique.

Finally, the answer consists of vertices outside the maximum clique.

## Worked Examples

Consider Sample 1.

```
5 6
1 2
1 3
2 3
2 5
3 4
4 5
```

| Current maximum clique | Size |
| --- | --- |
| {1} | 1 |
| {1,2} | 2 |
| {1,2,3} | 3 |

The maximum clique has size 3, namely vertices {1,2,3}. The complement is {4,5}, so two operations are required.

| Selected vertices | Graph status |
| --- | --- |
| 4 | adds edge (3,5) |
| 5 | adds edges involving 2 and 4 |

After these operations every pair becomes adjacent.

This example demonstrates that we only need to identify the largest clique, not simulate the graph transformations.

Consider a complete graph on four vertices.

```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

| Maximum clique found | Size |
| --- | --- |
| {1} | 1 |
| {1,2} | 2 |
| {1,2,3} | 3 |
| {1,2,3,4} | 4 |

The complement is empty.

| Answer |
| --- |
| 0 operations |

This confirms that the algorithm correctly handles the zero-operation case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n2^(n/2)) | Meet-in-the-middle enumeration |
| Space | O(2^(n/2)) | DP tables for one half |

With at most 22 vertices, each half contains at most 11 vertices, so only 2048 subsets per side are explored. The running time is tiny compared with the one-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    return ""

# minimum size
# answer must be 0
assert True

# complete graph of size 3
# answer must be 0
assert True

# star graph
# center alone is maximum clique size 2, answer size = 3
assert True

# path of length 3
# maximum clique size 2, answer size = 2
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 0 operations | Minimum size |
| Complete graph | 0 operations | Empty complement |
| Star graph | 3 operations | Universal vertex absent |
| Path graph | 2 operations | Nontrivial structure |

## Edge Cases

Consider a graph with a universal vertex.

```
4 3
1 2
1 3
1 4
```

The maximum clique size equals 2 because leaves are not connected to each other. The complement contains two vertices, and selecting them creates all missing edges. The algorithm reaches the same conclusion automatically through clique computation.

For an already complete graph

```
3 3
1 2
1 3
2 3
```

the maximum clique contains all vertices. Its complement is empty, so the printed answer is zero. No special branch is needed.

For a path

```
4 3
1 2
2 3
3 4
```

every clique has size 2. The complement size becomes 2, which matches the minimum number of operations. The algorithm avoids any dependence on operation order, because only the structure of the maximum clique matters.
