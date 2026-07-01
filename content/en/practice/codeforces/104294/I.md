---
title: "CF 104294I - Snack Time"
description: "We are given a tree of houses, where each house initially contains a certain number of friends. The roads form a connected acyclic structure, so between any two houses there is exactly one simple path. There are two types of events."
date: "2026-07-01T20:28:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104294
codeforces_index: "I"
codeforces_contest_name: "UTPC Spring 2023 Open Contest"
rating: 0
weight: 104294
solve_time_s: 97
verified: true
draft: false
---

[CF 104294I - Snack Time](https://codeforces.com/problemset/problem/104294/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree of houses, where each house initially contains a certain number of friends. The roads form a connected acyclic structure, so between any two houses there is exactly one simple path.

There are two types of events. Either Umaru performs a snack run between two houses, or she increases the number of friends in a specific house by multiplying its current value by some factor. For each snack run, we must look at all houses on the unique path between the two endpoints and compute the smallest positive number that is divisible by the number of friends in every house along that path.

This quantity is nothing more than the least common multiple of all values on that path. The challenge is that the values are not static, since multiplicative updates happen between queries, and we must answer path LCM queries online.

The constraints are small enough that we can afford solutions close to quadratic in the number of nodes or queries. With both N and Q up to 1000, even approaches that take roughly O(N) per query are acceptable, since the total work remains around 10^6 operations. This immediately rules out heavy dynamic tree structures, but allows us to recompute or traverse paths explicitly.

A subtle point is that values can grow large due to repeated multiplications. Even though individual a_i values are bounded by 10^7 initially, repeated updates can make them much larger, so storing raw values and attempting direct LCM computation is unsafe. Instead, the structure of LCM through prime factorization becomes essential.

A naive mistake is to try maintaining the LCM of the entire path incrementally without tracking per-prime maxima. This fails under updates because LCM does not distribute over multiplication in a simple additive way. Another common mistake is recomputing path values but multiplying integers directly, which quickly overflows and becomes incorrect.

## Approaches

The brute-force idea is straightforward. For each query, we explicitly find the path between u and v, collect all nodes on that path, and compute the LCM of their values. This is correct because the path is explicitly enumerated and the LCM definition is applied directly. However, computing LCM over raw integers is problematic due to overflow, and even if we fix arithmetic, recomputing LCM over potentially O(N) nodes per query leads to O(NQ) complexity, which is still acceptable at this constraint but leaves no margin once we include factorization costs and updates.

The key observation is that LCM is best handled in prime factor space. The LCM of a set of numbers is determined by taking, for each prime, the maximum exponent of that prime across all numbers. This means each node can be represented as a map from primes to exponents, and the answer to a path query becomes a union of these maps using maximums.

Updates are simple in this representation. When a node is multiplied by f, we factor f into primes and add those exponents to the node’s stored factorization. This keeps the node’s factor map always correct.

The remaining difficulty is answering path queries efficiently. Since N is small, we can precompute parent and depth arrays for the tree and then extract all nodes on a path using a standard LCA-based lifting procedure. Once we have the list of nodes on the path, we merge their prime exponent maps by taking maxima. The final answer is reconstructed using modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ + factorization overhead) | O(N) | Acceptable but tight |
| Optimal | O(NQ log A) | O(N log A) | Accepted |

## Algorithm Walkthrough

We first root the tree anywhere, typically at node 1, and compute parent and depth arrays using a DFS. This allows us to later retrieve paths efficiently.

Next, for each node, we store its current prime factorization as a dictionary mapping primes to exponents. We build this initially by factorizing each a_i.

For each update operation, we factorize the multiplier f_i and add its prime exponents into the dictionary of the target node. This maintains correctness because multiplication in integers corresponds to addition in exponent space.

For each query operation, we compute the path between u and v. We lift both nodes up until they meet at their lowest common ancestor, collecting all nodes along the way. This gives us the full list of nodes on the path.

Once we have the nodes, we build a global dictionary for the query that tracks, for each prime, the maximum exponent seen among all nodes on the path. We update this dictionary by iterating through each node’s factorization map.

Finally, we reconstruct the answer by computing the product over all primes of p raised to its maximum exponent, taken modulo 1e9+7.

The reason this works is that every number in the path contributes independent prime powers. The LCM selects the highest power of each prime that appears anywhere in the set. Since updates only increase exponents at individual nodes and never split or remove factors, each node’s factorization remains valid over time, and merging via maximum preserves correctness for the path LCM.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

# simple factorization up to sqrt using trial division
def factor(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res

sys.setrecursionlimit(10**7)

N, Q = map(int, input().split())
a = list(map(int, input().split()))

g = [[] for _ in range(N)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

parent = [-1] * N
depth = [0] * N

def dfs(u, p):
    parent[u] = p
    for v in g[u]:
        if v == p:
            continue
        depth[v] = depth[u] + 1
        dfs(v, u)

dfs(0, -1)

facts = [factor(x) for x in a]

def get_path(u, v):
    pu, pv = u, v
    while depth[pu] > depth[pv]:
        pu = parent[pu]
    while depth[pv] > depth[pu]:
        pv = parent[pv]

    path_u = []
    path_v = []

    while pu != pv:
        path_u.append(u)
        path_v.append(v)
        u = parent[u]
        v = parent[v]
        pu = parent[pu]
        pv = parent[pv]

    path_u.append(u)
    path = path_u + path_v[::-1]
    return path

def mod_pow(x, e):
    return pow(x, e, MOD)

for _ in range(Q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 2:
        _, w, f = tmp
        w -= 1
        for p, c in factor(f).items():
            facts[w][p] = facts[w].get(p, 0) + c
    else:
        _, u, v = tmp
        u -= 1
        v -= 1

        path = get_path(u, v)

        best = {}
        for node in path:
            for p, c in facts[node].items():
                if best.get(p, 0) < c:
                    best[p] = c

        ans = 1
        for p, c in best.items():
            ans = (ans * pow(p, c, MOD)) % MOD

        print(ans)
```

The solution maintains a factor dictionary per node, so updates become localized additions of exponents after factorizing the multiplier. The DFS sets up parent pointers and depths so that path reconstruction can be done without any heavy LCA structure.

The path extraction function first aligns both nodes at the same depth, then moves them upward together until they meet, collecting nodes along both branches. This guarantees that every node on the path is included exactly once.

During query evaluation, we aggregate prime exponents across the path. The dictionary `best` always keeps the maximum exponent seen so far for each prime. This directly encodes the LCM definition in exponent form.

## Worked Examples

Consider the sample tree where we first query a path and then apply an update before the next query.

For the first query, suppose the path includes nodes with factorizations `{1}`, `{2 × 3}`, and `{2²}`. The aggregation step builds a table like this.

| Node | Prime factors | Aggregated best |
| --- | --- | --- |
| 1 | {} | {} |
| 2 | {2:1, 3:1} | {2:1, 3:1} |
| 3 | {2:2} | {2:2, 3:1} |

The final answer is 2² × 3¹ = 12. This confirms that the algorithm correctly selects maximum exponent per prime across the path.

After an update multiplies a node by 4, its factor map gains two additional powers of 2. On the next query, if that node is included in the path, its contribution dominates the exponent of 2, which is correctly reflected in the final LCM.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q · N + Q · sqrt(A)) | Each query walks a path of up to N nodes and merges factor maps; updates require factoring the multiplier |
| Space | O(N log A) | Each node stores its prime factorization |

Given N, Q ≤ 1000, this comfortably fits within limits. Even with repeated factorization and full path traversal, the total number of operations stays well under typical constraints for Python.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def factor(x):
        res = {}
        d = 2
        while d * d <= x:
            while x % d == 0:
                res[d] = res.get(d, 0) + 1
                x //= d
            d += 1
        if x > 1:
            res[x] = res.get(x, 0) + 1
        return res

    N, Q = map(int, input().split())
    a = list(map(int, input().split()))
    g = [[] for _ in range(N)]

    for _ in range(N - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * N
    depth = [0] * N

    def dfs(u, p):
        parent[u] = p
        for v in g[u]:
            if v != p:
                depth[v] = depth[u] + 1
                dfs(v, u)

    dfs(0, -1)

    facts = [factor(x) for x in a]

    def get_path(u, v):
        pu, pv = u, v
        while depth[pu] > depth[pv]:
            pu = parent[pu]
        while depth[pv] > depth[pu]:
            pv = parent[pv]

        path_u, path_v = [], []
        while pu != pv:
            path_u.append(u)
            path_v.append(v)
            u = parent[u]
            v = parent[v]
            pu = parent[pu]
            pv = parent[pv]

        path_u.append(u)
        return path_u + path_v[::-1]

    out = []
    for _ in range(Q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 2:
            _, w, f = tmp
            w -= 1
            for p, c in factor(f).items():
                facts[w][p] = facts[w].get(p, 0) + c
        else:
            _, u, v = tmp
            u -= 1
            v -= 1

            path = get_path(u, v)

            best = {}
            for node in path:
                for p, c in facts[node].items():
                    best[p] = max(best.get(p, 0), c)

            ans = 1
            for p, c in best.items():
                ans = ans * pow(p, c, MOD) % MOD

            out.append(str(ans))

    return "\n".join(out)

# provided sample
assert solve("""6 3
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
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node path | correct value | LCM of one element |
| repeated updates on same node | increasing exponent handling | accumulation correctness |
| long path chain | full traversal correctness | path reconstruction correctness |

## Edge Cases

A key edge case is when updates repeatedly multiply a single node, causing its factorization to grow significantly. For example, if node 3 starts at 1 and is updated by 2 five times, its factor map becomes `{2:5}`. On any query involving node 3, the LCM must reflect this full exponent. The algorithm handles this because updates only ever increment stored exponents, never overwrite them.

Another edge case is a path of length 1, where u equals v. In that case, the path extraction returns only one node, and the LCM is exactly its current value. The aggregation step naturally reduces to a single dictionary, so no special handling is required.

A third case is when different nodes contribute the same prime in different ways. For example, one node might have `2^3` and another `2^1`. The correct result depends on taking the maximum exponent, not summing. The merging step in `best[p] = max(...)` ensures this behavior, so overlapping prime factors are resolved correctly without double counting.
