---
title: "CF 154C - Double Profiles"
description: "We are given an undirected graph representing a social network. Each vertex is a profile and each edge is a friendship. Two distinct profiles i and j are considered doubles if every other profile sees them in exactly the same way."
date: "2026-06-02T16:54:31+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "hashing", "sortings"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 2300
weight: 154
solve_time_s: 63
verified: true
draft: false
---

[CF 154C - Double Profiles](https://codeforces.com/problemset/problem/154/C)

**Rating:** 2300  
**Tags:** graphs, hashing, sortings  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph representing a social network. Each vertex is a profile and each edge is a friendship.

Two distinct profiles `i` and `j` are considered doubles if every other profile sees them in exactly the same way. For every vertex `k ≠ i, j`, either both edges `(i, k)` and `(j, k)` exist, or neither exists. The friendship status between `i` and `j` themselves does not matter for this definition.

In graph terms, if we ignore the vertices themselves, then `i` and `j` must have identical neighborhoods. The only subtlety is that the presence or absence of the edge `(i, j)` should not affect the comparison.

We must count how many unordered pairs of vertices satisfy this property.

The constraints are extremely large. Both `n` and `m` can reach `10^6`. A graph with one million vertices immediately rules out any algorithm that compares adjacency lists pairwise. Even storing an `n × n` structure is impossible. With a 3 second time limit, we need something close to linear or `O(m log n)`.

The graph is sparse because `m ≤ 10^6`, while a complete graph on `10^6` vertices would contain roughly `5·10^11` edges. This suggests that adjacency-list based processing is the right direction.

Several edge cases are easy to mishandle.

Consider isolated vertices:

```
4 0
```

Every vertex has the same neighborhood, namely the empty set. Every pair is a double, so the answer is:

```
6
```

A solution that only processes vertices appearing in edges might forget the isolated ones entirely.

Another subtle case is when two vertices differ only because they are connected to each other.

```
2 1
1 2
```

The answer is:

```
1
```

There are no third vertices, so the condition is vacuously true. If we compare ordinary adjacency lists, we get `{2}` versus `{1}`, which are different. A direct neighborhood comparison would incorrectly reject this pair.

A slightly larger example shows the same phenomenon:

```
3 2
1 3
2 3
```

Vertices `1` and `2` are doubles because both are connected only to vertex `3`.

Now add the edge `(1,2)`:

```
3 3
1 2
1 3
2 3
```

Vertices `1` and `2` are still doubles. The only difference in their adjacency lists is each other. Any approach that compares full neighborhoods without accounting for this will fail.

The core difficulty is handling the phrase "all other vertices" efficiently.

## Approaches

The most direct solution is to examine every pair of vertices `(i,j)`. For each pair, compare their relationships with all remaining vertices. If every third vertex sees `i` and `j` identically, count the pair.

This is correct because it follows the definition literally. Unfortunately there are `O(n²)` pairs, and each comparison may require examining `O(n)` vertices. The worst case is `O(n³)`, which is completely impossible for `n = 10^6`.

We need to reformulate the condition.

Suppose `N(v)` denotes the set of neighbors of vertex `v`.

If vertices `u` and `v` are not adjacent, then the definition simply says:

```
N(u) = N(v)
```

because neither neighborhood contains the other vertex.

If vertices `u` and `v` are adjacent, then each neighborhood contains the other vertex. After removing each other, the remaining neighbors must match:

```
N(u) \ {v} = N(v) \ {u}
```

This observation transforms the problem into grouping vertices by neighborhood signatures.

The challenge is that adjacency lists may contain up to one million vertices, so comparing sets directly is too expensive. Instead, we assign each vertex a hash value and represent a neighborhood by the sum of hashes of its members.

Let `rnd[x]` be a random 64-bit number assigned to vertex `x`.

For every vertex:

```
H(v) = Σ rnd[x]   over all x in N(v)
```

With overwhelming probability, equal neighborhood sets produce equal sums and different sets produce different sums.

Now consider the two cases.

For non-adjacent doubles, we need equal ordinary neighborhoods. We can simply group vertices by `H(v)`.

For adjacent doubles, we need:

```
N(u) \ {v} = N(v) \ {u}
```

Equivalently:

```
H(u) - rnd[v] = H(v) - rnd[u]
```

Define:

```
G(u,v) = H(u) + rnd[u]
```

Then adjacent vertices form a valid pair exactly when:

```
H(u) + rnd[u] = H(v) + rnd[v]
```

This leads to a very efficient strategy.

First count all pairs of vertices with identical `H(v)`. These are the non-adjacent doubles.

Then count all pairs of vertices with identical `H(v)+rnd[v]`. This includes both adjacent and non-adjacent pairs, so we cannot add all of them. Instead, we only examine actual edges `(u,v)` and check whether:

```
H(u)+rnd[u] = H(v)+rnd[v]
```

Every such edge contributes one additional double pair.

The graph has only `m ≤ 10^6` edges, so this final check is cheap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n + m) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Assign every vertex a random 64-bit integer `rnd[i]`.
2. Create an array `H` initialized to zero.
3. For every edge `(u,v)`, add `rnd[v]` to `H[u]` and add `rnd[u]` to `H[v]`.

After this step, `H[v]` is the hash of the neighborhood of vertex `v`.
4. Group all vertices by `H[v]`.

If a group contains `k` vertices, add:

```
k(k-1)/2
```

to the answer.

These are pairs with identical ordinary neighborhoods.
5. For every vertex compute:

```
T[v] = H[v] + rnd[v]
```
6. For every edge `(u,v)`, check whether:

```
T[u] = T[v]
```

If true, add one to the answer.

This corresponds exactly to:

```
H(u)-rnd[v] = H(v)-rnd[u]
```

which means the neighborhoods become identical after removing each other.
7. Output the final count.

### Why it works

For non-adjacent vertices, the double condition is equivalent to equality of their entire neighborhood sets. The hash `H(v)` is constructed from all neighbors of `v`, so equal neighborhoods produce equal hashes. Grouping equal hashes counts exactly those pairs.

For adjacent vertices, each neighborhood differs by the presence of the other endpoint. Removing that endpoint from both sides gives the condition:

```
N(u)\{v} = N(v)\{u}
```

The hash representation transforms this into:

```
H(u)-rnd[v] = H(v)-rnd[u]
```

which is algebraically equivalent to:

```
H(u)+rnd[u] = H(v)+rnd[v]
```

Checking this equality only on existing edges counts exactly the adjacent double pairs.

Every double pair falls into one of these two categories, and no pair is counted twice. Hence the algorithm is correct.

## Python Solution

```python
import sys
import random
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    rnd = [0] * (n + 1)
    rng = random.Random(154154)

    for i in range(1, n + 1):
        rnd[i] = rng.getrandbits(64)

    h = [0] * (n + 1)
    edges = []

    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))

        h[u] += rnd[v]
        h[v] += rnd[u]

    groups = defaultdict(int)

    for i in range(1, n + 1):
        groups[h[i]] += 1

    ans = 0

    for cnt in groups.values():
        ans += cnt * (cnt - 1) // 2

    t = [0] * (n + 1)
    for i in range(1, n + 1):
        t[i] = h[i] + rnd[i]

    for u, v in edges:
        if t[u] == t[v]:
            ans += 1

    print(ans)

solve()
```

The first phase assigns a random 64-bit value to every vertex. These values act as fingerprints for neighborhood construction.

While reading edges, the code updates the neighborhood hash of both endpoints. After processing all edges, `h[v]` contains the sum of fingerprints of all neighbors of `v`.

The dictionary `groups` counts how many vertices share the same neighborhood hash. If a hash appears `
