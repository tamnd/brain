---
title: "CF 154C - Double Profiles"
description: "We are working with an undirected graph where each vertex represents a social network profile. Two profiles are considered \"doubles\" if every other profile sees them identically. For any third vertex k, either both i and j are connected to k, or neither is connected to k."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "hashing", "sortings"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 2300
weight: 154
solve_time_s: 97
verified: true
draft: false
---

[CF 154C - Double Profiles](https://codeforces.com/problemset/problem/154/C)

**Rating:** 2300  
**Tags:** graphs, hashing, sortings  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with an undirected graph where each vertex represents a social network profile. Two profiles are considered "doubles" if every other profile sees them identically. For any third vertex `k`, either both `i` and `j` are connected to `k`, or neither is connected to `k`.

The relation between `i` and `j` themselves does not matter. They may be connected or disconnected.

Another way to phrase the condition is this:

Two vertices are doubles if their adjacency sets become equal after removing each other from consideration.

Suppose we have this graph:

```
1 -- 3
2 -- 3
```

Vertices `1` and `2` are doubles because every other vertex treats them the same. Vertex `3` is connected to both of them, and there are no other vertices.

The input gives up to one million vertices and one million edges. That scale immediately rules out any approach that compares neighborhoods vertex-by-vertex in quadratic time. Even storing a dense adjacency matrix would require around `10^12` cells, which is impossible.

An `O(n^2)` pair comparison is also hopeless. With `10^6` vertices, there are roughly `5 * 10^11` unordered pairs. Even touching each pair once is already too slow.

The graph is sparse because `m ≤ 10^6`. Sparse-graph techniques become the natural direction. We need something close to linear or `O(m log n)`.

There are several easy-to-miss edge cases.

Consider isolated vertices:

```
4 0
```

Every vertex has an empty neighborhood, so every pair is valid. The correct answer is `6`.

A careless implementation that only processes vertices appearing in edges would completely miss isolated vertices.

Another subtle case appears when the two vertices are directly connected:

```
3 1
1 2
```

Vertices `1` and `2` are doubles. The definition ignores the relationship between the pair itself. A naive comparison of full adjacency lists would fail because:

```
adj(1) = {2}
adj(2) = {1}
```

These sets are different, yet the pair is valid.

One more dangerous case:

```
4 2
1 3
2 3
```

Vertices `1` and `2` are doubles because both are connected only to `3`.

If we compare adjacency sets after inserting the vertex itself into the set, we get:

```
{1,3}
{2,3}
```

Still different.

The trick is that when two vertices are adjacent, we should compare closed neighborhoods. When they are not adjacent, we compare ordinary neighborhoods. Mixing these two situations incorrectly leads to wrong answers.

## Approaches

The brute-force solution is straightforward.

For every unordered pair `(i, j)`, inspect every third vertex `k`. Check whether `k` is connected to both or neither. If any `k` distinguishes the pair, reject it.

Using adjacency matrices, each check becomes `O(1)`, but we still examine all triples:

```
O(n^3)
```

With `n = 10^6`, this is completely impossible.

We can improve the brute force slightly by storing adjacency sets and directly comparing neighborhoods. For every pair `(i, j)`, we check whether:

```
adj(i) \ {j} == adj(j) \ {i}
```

This is logically correct, but still far too slow because the number of pairs is quadratic.

The key observation is that the problem only asks whether neighborhoods are equal. We do not actually care about the specific vertex labels once the neighborhoods are formed.

That suggests grouping vertices by some representation of their neighborhood.

Suppose two disconnected vertices are doubles. Then their adjacency lists are exactly equal.

Suppose two connected vertices are doubles. Then after adding themselves into their own adjacency sets, the resulting sets are equal.

Example:

```
1 -- 2
1 -- 3
2 -- 3
```

For vertices `1` and `2`:

```
adj(1) = {2,3}
adj(2) = {1,3}
```

Different.

But if we include each vertex itself:

```
{1,2,3}
{1,2,3}
```

Now they match.

This converts the problem into counting equal sets.

We need a compact representation for each neighborhood. Sorting entire vectors for every comparison would still be expensive, so we use hashing.

For every vertex:

```
hash_open(v)   = hash of adj(v)
hash_closed(v) = hash of adj(v) ∪ {v}
```

Vertices with equal `hash_open` form valid disconnected pairs.

Vertices with equal `hash_closed` form valid connected pairs.

We count both categories separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| Optimal | O(n + m) expected | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the graph.

Since the graph is undirected, every edge `(u, v)` is added to both lists.
2. Assign a random 64-bit value to every vertex.

These values are used for hashing neighborhoods. The probability of collision with 64-bit hashes is negligible for competitive programming.
3. Compute an open-neighborhood hash for every vertex.

For each edge `(u, v)`:

```
hash_open[u] += rnd[v]
hash_open[v] += rnd[u]
```

The resulting sum uniquely represents the multiset of neighbors with overwhelming probability.
4. Group vertices by `hash_open`.

Any two disconnected doubles must have identical ordinary neighborhoods, so they land in the same group.
5. For each group of size `k`, add:

```
k * (k - 1) / 2
```

to the answer.

This counts all unordered pairs with equal open neighborhoods.
6. Compute closed-neighborhood hashes.

For every vertex:

```
hash_closed[v] = hash_open[v] + rnd[v]
```

Adding the vertex itself transforms the neighborhood into:

```
adj(v) ∪ {v}
```
7. Group vertices by `hash_closed`.

Connected doubles have equal closed neighborhoods.
8. Count only actual edges inside these groups.

For every edge `(u, v)`, if:

```
hash_closed[u] == hash_closed[v]
```

then `(u, v)` is a valid doubles pair.

We only count existing edges because equal closed neighborhoods are relevant exclusively for connected pairs.

### Why it works

For disconnected vertices `u` and `v`, the doubles condition means every third vertex either connects to both or neither. That is exactly the statement:

```
adj(u) = adj(v)
```

So disconnected doubles are precisely the pairs with equal open neighborhoods.

For connected vertices `u` and `v`, each neighborhood differs only because one contains `v` and the other contains `u`. After inserting the vertex itself into the neighborhood, the sets become identical:

```
adj(u) ∪ {u} = adj(v) ∪ {v}
```

The algorithm counts both categories separately, and every valid pair belongs to exactly one category.

## Python Solution

```python
import sys
import random
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    rnd = [random.getrandbits(64) for _ in range(n + 1)]

    open_hash = [0] * (n + 1)
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())

        edges.append((u, v))

        open_hash[u] += rnd[v]
        open_hash[v] += rnd[u]

    groups = defaultdict(int)

    for v in range(1, n + 1):
        groups[open_hash[v]] += 1

    ans = 0

    for cnt in groups.values():
        ans += cnt * (cnt - 1) // 2

    closed_hash = [0] * (n + 1)

    for v in range(1, n + 1):
        closed_hash[v] = open_hash[v] + rnd[v]

    for u, v in edges:
        if closed_hash[u] == closed_hash[v]:
            ans += 1

    print(ans)

solve()
```

The solution never explicitly stores adjacency lists. That is an intentional optimization. The hash of a neighborhood can be accumulated directly while reading edges.

The array `rnd` assigns each vertex a random 64-bit fingerprint. A neighborhood hash becomes the sum of fingerprints of neighboring vertices.

Using addition instead of sorted tuples keeps the algorithm linear. Python integers automatically handle overflow safely, so we do not need modular arithmetic.

The first grouping counts disconnected doubles. Every vertex with the same `open_hash` belongs to the same neighborhood class.

The second phase handles connected pairs separately. We add the vertex's own random value to construct the closed neighborhood hash.

A subtle detail is that we do not group by `closed_hash` and count combinations. Doing so would incorrectly count disconnected vertices whose closed neighborhoods happen to match. We only inspect actual edges.

Another subtle point is collision probability. Hash collisions are theoretically possible, but with independent 64-bit random values, the probability is astronomically small and fully acceptable for this problem.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
1 3
```

Random values are symbolic here:

```
r1, r2, r3
```

Open neighborhood hashes:

| Vertex | Neighbors | Open Hash |
| --- | --- | --- |
| 1 | {2,3} | r2 + r3 |
| 2 | {1,3} | r1 + r3 |
| 3 | {1,2} | r1 + r2 |

No two open hashes match, so disconnected contribution is `0`.

Closed neighborhood hashes:

| Vertex | Closed Neighborhood | Closed Hash |
| --- | --- | --- |
| 1 | {1,2,3} | r1 + r2 + r3 |
| 2 | {1,2,3} | r1 + r2 + r3 |
| 3 | {1,2,3} | r1 + r2 + r3 |

Now every edge connects vertices with equal closed hashes.

| Edge | Equal Closed Hashes | Counted |
| --- | --- | --- |
| (1,2) | Yes | Yes |
| (2,3) | Yes | Yes |
| (1,3) | Yes | Yes |

Final answer:

```
3
```

This example demonstrates why open neighborhoods alone are insufficient for connected pairs.

### Example 2

Input:

```
4 2
1 3
2 3
```

Open neighborhood hashes:

| Vertex | Neighbors | Open Hash |
| --- | --- | --- |
| 1 | {3} | r3 |
| 2 | {3} | r3 |
| 3 | {1,2} | r1 + r2 |
| 4 | {} | 0 |

Vertices `1` and `2` share the same open hash.

Disconnected contribution:

```
1 pair
```

Closed neighborhood hashes:

| Vertex | Closed Hash |
| --- | --- |
| 1 | r1 + r3 |
| 2 | r2 + r3 |
| 3 | r1 + r2 + r3 |
| 4 | r4 |

No edge connects equal closed hashes.

Final answer:

```
1
```

This example shows the disconnected case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) expected | Each vertex and edge is processed a constant number of times |
| Space | O(n + m) | Arrays plus edge storage |

The constraints allow around a few million operations comfortably in Python. This solution stays linear in the graph size and fits both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
import random
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    rnd = [random.getrandbits(64) for _ in range(n + 1)]

    open_hash = [0] * (n + 1)
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())

        edges.append((u, v))

        open_hash[u] += rnd[v]
        open_hash[v] += rnd[u]

    groups = defaultdict(int)

    for v in range(1, n + 1):
        groups[open_hash[v]] += 1

    ans = 0

    for cnt in groups.values():
        ans += cnt * (cnt - 1) // 2

    closed_hash = [0] * (n + 1)

    for v in range(1, n + 1):
        closed_hash[v] = open_hash[v] + rnd[v]

    for u, v in edges:
        if closed_hash[u] == closed_hash[v]:
            ans += 1

    return str(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""3 3
1 2
2 3
1 3
"""
) == "3", "sample 1"

# isolated vertices
assert run(
"""4 0
"""
) == "6", "all isolated"

# simple disconnected doubles
assert run(
"""4 2
1 3
2 3
"""
) == "1", "vertices 1 and 2 are doubles"

# connected doubles
assert run(
"""2 1
1 2
"""
) == "1", "connected pair"

# no doubles
assert run(
"""4 3
1 2
2 3
3 4
"""
) == "0", "path graph"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 0` | `6` | All isolated vertices form doubles |
| `4 2 / 1 3 / 2 3` | `1` | Equal open neighborhoods |
| `2 1 / 1 2` | `1` | Connected doubles require closed neighborhoods |
| Path graph on 4 vertices | `0` | Prevents accidental false positives |

## Edge Cases

Consider the completely empty graph:

```
4 0
```

Every vertex has:

```
open_hash = 0
```

The grouping size becomes `4`, so the algorithm adds:

```
4 * 3 / 2 = 6
```

Every pair is correctly counted.

Now consider a graph with a single edge:

```
2 1
1 2
```

Open hashes differ:

```
1 -> r2
2 -> r1
```

So the disconnected counting phase contributes nothing.

Closed hashes become:

```
1 -> r1 + r2
2 -> r1 + r2
```

The edge `(1,2)` satisfies equality and gets counted once.

Finally, examine this tricky case:

```
4 4
1 3
1 4
2 3
2 4
```

Vertices `1` and `2` share neighbors `{3,4}`.

Vertices `3` and `4` share neighbors `{1,2}`.

Open-hash grouping creates two groups of size `2`, producing:

```
1 + 1 = 2
```

There are no edges inside either group, so the second phase contributes nothing.

The final answer is `2`, which is correct.
