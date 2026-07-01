---
title: "CF 104312B - Snack Time"
description: "We are given a tree of houses. Each house initially has a certain number of friends living there. Over time, two kinds of events happen."
date: "2026-07-01T19:51:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "B"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 82
verified: false
draft: false
---

[CF 104312B - Snack Time](https://codeforces.com/problemset/problem/104312/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree of houses. Each house initially has a certain number of friends living there. Over time, two kinds of events happen. Either Umaru performs a travel query between two houses, or she performs an update that increases the number of friends in a specific house by multiplying it by some factor.

For each travel query, Umaru walks along the unique simple path between two given nodes in the tree. Every house on that path contributes its current number of friends. She wants to bring a number of snacks that is divisible by every value on that path. In other words, she needs the least common multiple of the values on that path at that moment, and she outputs it modulo 10^9 + 7.

The tree structure ensures there is exactly one path between any two nodes, so each query reduces to processing a path over a dynamic array defined on a tree.

The constraints are small, with N and Q up to 1000. This is important because it allows solutions that recompute values over paths directly or rebuild information repeatedly. Anything involving N^2 per query is still borderline but acceptable, while anything cubic over all queries would still pass comfortably in Python given tight implementation.

A subtle aspect is that values grow over time due to multiplicative updates. Since we are working with LCMs, naive factorization per query could still work under these limits, but must be structured carefully to avoid recomputation overhead.

A typical edge case arises when updates affect nodes not on a queried path. For example, if we multiply node 5 by 10, but later query a path that does not include node 5, the result should remain unaffected. Another edge case is repeated updates on the same node, which can rapidly increase values. For instance, a node starting at 2 updated by factors 3, 5, and 7 becomes 210, and must be fully reflected in later path computations.

## Approaches

A direct brute force approach handles each query independently. For a travel query between u and v, we first find the unique path between them using a DFS or BFS parent reconstruction. Once we have the path, we iterate over all nodes on it and compute the least common multiple of their current values. For updates, we simply multiply the stored value at a node.

This is correct because the tree structure guarantees a single path, and LCM over a set is associative and can be computed incrementally. The issue is efficiency over repeated queries.

The worst case path length is O(N), and there can be O(Q) queries. Each query recomputes an LCM over up to O(N) nodes, so total complexity becomes O(NQ), which is about 10^6 operations, already fine. However, if implemented with naive factorization inside LCM computations, each number could be up to 10^7 times many multiplications, causing factor explosion and repeated gcd computations that degrade performance.

A cleaner observation is that we do not actually need full LCM recomputation from scratch each time. Since LCM depends on prime exponents, the problem reduces to maintaining, for each node value, its prime factorization and taking the maximum exponent along the path. Each update only affects one node, so we update its factorization incrementally. Each query becomes a "max over path" problem for prime exponents.

Since N is small, we can afford to precompute paths via LCA or parent pointers and simply walk the path per query, maintaining a map of prime exponents. Each query becomes linear in path length, and updates become O(log value) factorization.

Thus the solution is essentially: factorize values, maintain per-node prime exponent maps, and for each query walk the path and compute max exponent per prime.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force LCM recomputation per query | O(NQ + Q log A) | O(N) | Accepted |
| Factorized path aggregation | O(Q * N * sqrt(A)) | O(N log A) | Accepted |

## Algorithm Walkthrough

1. Build the tree and preprocess parent and depth arrays using a DFS from an arbitrary root. This allows reconstructing the path between any two nodes by lifting both nodes until their lowest common ancestor is reached.
2. Maintain an array `fact[i]` storing the prime factorization of the current value at node i as a dictionary or counter of primes to exponents. Initialize this by factorizing all a[i].
3. For each update query of the form multiply node w by f, factorize f and add its exponents into `fact[w]`. This ensures the node’s value remains correctly represented in prime-exponent form.
4. For each travel query between u and v, first reconstruct the full path nodes by climbing u and v to their LCA and concatenating the segments. This gives all nodes on the simple path in order.
5. Initialize an empty dictionary `res` to store maximum exponents across the path.
6. Traverse each node on the path, and for each prime in its factorization, update `res[p] = max(res[p], fact[node][p])`. This step aggregates the exponent structure needed for LCM.
7. After processing all nodes on the path, compute the answer by multiplying `p^res[p] mod MOD` for all primes in `res`.
8. Output this value and continue to the next query.

The key reason this is efficient is that factorization is only done on updates, and path traversal is linear in N. Since both N and Q are small, the total cost remains comfortably within limits.

### Why it works

The LCM of a set of numbers is determined by taking, for each prime, the maximum exponent of that prime across all numbers. Representing each node’s value by its prime factorization preserves all necessary information. Updates only increase exponents, never decrease them, so factorization remains consistent over time. When we traverse a path, collecting maximum exponents per prime exactly reconstructs the LCM of that path. No interaction between primes exists, so handling them independently is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

from collections import defaultdict

def factorize(x):
    res = defaultdict(int)
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] += 1
            x //= d
        d += 1
    if x > 1:
        res[x] += 1
    return res

def lca(u, v, parent, depth):
    visited = set()
    while u != v:
        if depth[u] > depth[v]:
            visited.add(u)
            u = parent[u]
        else:
            visited.add(v)
            v = parent[v]
    visited.add(u)
    return visited

def build_path(u, v, parent, depth):
    path_u = []
    path_v = []
    a, b = u, v
    while depth[a] > depth[b]:
        path_u.append(a)
        a = parent[a]
    while depth[b] > depth[a]:
        path_v.append(b)
        b = parent[b]
    while a != b:
        path_u.append(a)
        path_v.append(b)
        a = parent[a]
        b = parent[b]
    path_u.append(a)
    return path_u + path_v[::-1]

def dfs(root, g, parent, depth):
    stack = [(root, -1)]
    parent[root] = -1
    depth[root] = 0
    order = []
    while stack:
        u, p = stack.pop()
        for v in g[u]:
            if v == p:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append((v, u))
    return

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    depth = [0] * n
    dfs(0, g, parent, depth)

    fact = [factorize(x) for x in a]

    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            u, v = tmp[1] - 1, tmp[2] - 1
            path = build_path(u, v, parent, depth)
            cur = defaultdict(int)
            for node in path:
                for p, e in fact[node].items():
                    if e > cur[p]:
                        cur[p] = e
            ans = 1
            for p, e in cur.items():
                ans = (ans * pow(p, e, MOD)) % MOD
            print(ans)
        else:
            w, f = tmp[1] - 1, tmp[2]
            add = factorize(f)
            for p, e in add.items():
                fact[w][p] += e

if __name__ == "__main__":
    solve()
```

The DFS establishes parent and depth information so that any path can be reconstructed in linear time. The factorization table `fact` is always kept updated under multiplicative updates, so it remains a faithful representation of each node value at all times.

The `build_path` function reconstructs the simple path by lifting both endpoints until they meet, which is safe because the structure is a tree. This avoids any need for LCA preprocessing beyond parent pointers.

Each query then reduces to a sweep over the path with a dictionary accumulating maximum prime exponents, which directly corresponds to computing the LCM.

## Worked Examples

Consider the sample input. The first query computes the LCM along a path in the initial tree. The traversal collects values from all nodes on that path and merges their prime factors, producing 12.

| Step | Node | Current value factorization | Aggregated max exponents |
| --- | --- | --- | --- |
| Start | - | - | {} |
| Visit 1 | 1 | {1} | {1:1} |
| Visit 2 | 2 | {2,3} | {1:1,2:1,3:1} |
| Visit 5 | 5 | {2,2} | {1:1,2:2,3:1} |

The resulting product is 2^2 * 3 = 12, confirming correctness.

After the update, node 2 becomes multiplied by 4, increasing its exponent of 2 by 2. This changes its factorization from 6 to 24.

| Step | Node | Factorization | Max update |
| --- | --- | --- | --- |
| Update node 2 | - | {2:2,3:1} -> {2:4,3:1} | applied |

The second query now includes node 2 in the path, so the LCM must reflect the increased power of 2. The result becomes 24.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q * N * sqrt(A)) | Each query may traverse O(N) nodes and factorization cost is O(sqrt(A)) only on updates |
| Space | O(N log A) | Each node stores prime factorization of its current value |

The constraints keep N and Q at most 1000, so even a full traversal per query combined with factorization overhead remains well within time limits. The solution fits comfortably under both 2 seconds and 512 MB.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("""6 3
1 6 5 3 4 3
1 2
1 3
1 4
2 5
4 6
1 1 5
2 2 4
1 1 2
""") == """12
24"""

# small chain
assert run("""3 2
2 3 5
1 2
2 3
1 1 3
1 2 3
""") == """30
15"""

# all equal
assert run("""4 1
7 7 7 7
1 2
2 3
3 4
1 1 4
""") == """7"""

# single edge updates
assert run("""2 3
2 2
1 2
2 1 3
1 1 2
1 1 2
""") == """6
6"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small chain | 30, 15 | correctness of path merging |
| all equal | 7 | stability under uniform values |
| repeated updates | 6, 6 | update persistence |

## Edge Cases

A key edge case is repeated updates on a single node. If a node is multiplied many times, its factorization must accumulate correctly rather than overwrite previous values. For example, starting with 2 and applying multipliers 3 and 5 should result in factorization {2:1,3:1,5:1}. The update logic directly adds exponents, so earlier contributions are preserved.

Another edge case is queries where u equals v. The path contains a single node, so the answer is simply the current value of that node. The path-building logic returns a single-element list in this case, and the LCM accumulation reduces correctly to that node’s factorization.

A final edge case is updates on nodes that are never queried. These do not affect any output, but must still be applied correctly because future queries may include those nodes later in the sequence. The factorization storage ensures updates are global and persistent, independent of query order.
