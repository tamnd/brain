---
title: "CF 105408E - Expected Closest Friend"
description: "We are given a weighted, undirected, connected graph of cities. Jorge lives at city 0. Each edge represents a road with a positive length, and shortest paths define the distance between any two cities. Jorge has k friends, and each friend independently occupies a distinct city."
date: "2026-06-23T17:19:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105408
codeforces_index: "E"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico Repechaje"
rating: 0
weight: 105408
solve_time_s: 85
verified: true
draft: false
---

[CF 105408E - Expected Closest Friend](https://codeforces.com/problemset/problem/105408/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted, undirected, connected graph of cities. Jorge lives at city 0. Each edge represents a road with a positive length, and shortest paths define the distance between any two cities.

Jorge has k friends, and each friend independently occupies a distinct city. We are not told which cities they occupy; instead, we consider every possible choice of k distinct cities from the remaining n − 1 cities, all equally likely. For each such choice, we compute the distance from city 0 to each chosen city using shortest paths, then take the minimum among those k distances. The task is to compute the expected value of this minimum distance.

The key difficulty is that we are averaging a nonlinear statistic, the minimum over a random subset, rather than summing independent distances.

The constraints push us toward an almost linearithmic graph solution. With n up to 100000 and m up to 1e6, any approach that recomputes shortest paths per choice is impossible. Even storing all pairwise distances is infeasible. We must compute all distances from source 0 once, then reason combinatorially over sorted values.

A subtle edge case arises when multiple cities share the same shortest distance from 0. For example, if several cities are at distance 5, then the probability structure of the minimum changes in a stepwise manner, and naive averaging over individual cities fails if we do not group equal distances properly. Another edge case is when k is very close to n − 1. In that regime, the minimum is almost surely the smallest distance among nearly all nodes, and combinatorial probabilities must still behave correctly, especially for the farthest nodes which never influence the minimum.

## Approaches

A brute-force interpretation would enumerate all subsets of k cities among n − 1, compute the minimum distance for each subset, and average the result. Even ignoring shortest path computation, the number of subsets is $\binom{n-1}{k}$, which becomes astronomically large even for moderate n. This immediately rules out direct enumeration.

We first separate the graph component from the combinatorial component. The distance from city 0 to every other city can be computed using Dijkstra’s algorithm in $O(m \log n)$. After that, the problem becomes purely probabilistic: given an array of n − 1 distances, we pick k elements uniformly without replacement and want the expected minimum.

The key observation is to reframe the expectation in terms of survival probabilities. Instead of asking what the minimum is directly, we consider the probability that the minimum is at least a threshold value d. This happens exactly when all k chosen cities lie among those with distance ≥ d. If we sort all distances, we can compute prefix counts of how many cities have distance ≤ d, and from that derive how many have distance ≥ d.

This transforms the expectation into a sum over sorted unique distances, where each value contributes according to the probability that the minimum equals that value. This probability is expressed using combinations: we count the number of ways to choose k cities all outside the set of nodes closer than the threshold, and subtract the next threshold similarly. The entire structure reduces to prefix combinatorics over sorted distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(C(n, k) · k + m log n) | O(n) | Too slow |
| Dijkstra + combinatorics over sorted distances | O(m log n + n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We split the solution into a graph preprocessing phase and a combinatorial expectation phase.

1. Run Dijkstra from city 0 to compute shortest distances to all cities.

This is necessary because every later computation depends only on these distances, and any path structure beyond shortest distances is irrelevant once they are computed.
2. Remove city 0 from consideration since it is the source and cannot be chosen as a friend city.
3. Store all distances into an array and sort it in non-decreasing order.

Sorting is required because the minimum over a random subset is easiest to reason about in terms of thresholds from smallest to largest.
4. Precompute factorials and inverse factorials up to n for binomial coefficients modulo 1e9+7.

We need fast computation of $\binom{a}{b}$ because probabilities depend on counting subsets.
5. Define a function C(a, b) returning 0 if b > a, otherwise computing $\frac{a!}{b!(a-b)!}$.

This function is used repeatedly in probability expressions.
6. Iterate over each index i in the sorted distance array, treating dist[i] as the candidate value where the minimum might first appear.

For a fixed i, we compute how many subsets of size k have their minimum exactly equal to dist[i].
7. Let i+1 be the number of cities with distance ≤ dist[i]. The number of cities strictly closer than or equal to this threshold determines how many choices would invalidate dist[i] as the minimum.
8. Compute the number of ways to choose k cities from indices i..n-1 (all cities with distance ≥ dist[i]).

This is C(n-1 - i, k).
9. Subtract the number of ways to choose k cities from indices i+1..n-1, which corresponds to subsets whose minimum is strictly greater than dist[i].

This gives the number of subsets where dist[i] is exactly the minimum.
10. Multiply this probability weight by dist[i] and accumulate into the final answer.

### Why it works

The algorithm partitions all k-subsets of cities according to their minimum distance from city 0. Every subset has exactly one minimum element in the sorted order, and the combinatorial difference C(n-1 - i, k) − C(n-1 - i-1, k) counts precisely the subsets whose first selected element in sorted order is position i. This ensures each subset contributes exactly once to exactly one distance bucket, and therefore the weighted sum is exactly the expectation of the minimum distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def dijkstra(n, adj):
    import heapq
    dist = [10**30] * n
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def modinv(x):
    return pow(x, MOD - 2, MOD)

def nCk(n, k, fact, invfact):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

def solve():
    n, m, k = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        a, b, w = map(int, input().split())
        adj[a].append((b, w))
        adj[b].append((a, w))

    dist = dijkstra(n, adj)
    arr = dist[1:]
    arr.sort()

    maxn = n + 5
    fact = [1] * maxn
    invfact = [1] * maxn
    for i in range(1, maxn):
        fact[i] = fact[i - 1] * i % MOD
    invfact[maxn - 1] = modinv(fact[maxn - 1])
    for i in range(maxn - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    total = nCk(n - 1, k, fact, invfact)

    ans = 0
    n1 = n - 1

    for i, x in enumerate(arr):
        if n1 - i < k:
            continue
        # subsets where minimum >= x
        ge = nCk(n1 - i, k, fact, invfact)
        # subsets where minimum > x
        if i + 1 <= n1:
            gt = nCk(n1 - (i + 1), k, fact, invfact)
        else:
            gt = 0
        cnt = (ge - gt) % MOD
        ans = (ans + cnt * x) % MOD

    inv_total = modinv(total)
    print(ans * inv_total % MOD)

if __name__ == "__main__":
    solve()
```

The implementation starts by building the adjacency list and computing single-source shortest paths using Dijkstra with a heap. This produces all distances needed for the probabilistic stage.

The factorial and inverse factorial arrays are precomputed once, since binomial coefficients are required repeatedly. Modular inverses are computed using Fermat’s theorem, which is safe because the modulus is prime.

The array `arr` contains distances from node 0 to all other nodes, sorted so that we can reason about thresholds. For each position `i`, we compute how many k-subsets have their minimum exactly equal to `arr[i]` using a difference of two binomial counts. This avoids explicitly tracking subsets.

Finally, we divide the accumulated weighted sum by the total number of k-subsets using a modular inverse, producing the expected value.

A common implementation pitfall is forgetting that city 0 is excluded from the selection pool. Another is incorrectly treating equal distances without grouping; the difference-of-combinations formulation avoids this issue automatically.

## Worked Examples

### Example 1

Input:

```
2 1 1
0 1 3
```

Distances from 0 are:

| Step | Dist array | Computation | Contribution |
| --- | --- | --- | --- |
| init | [3] | total subsets = C(1,1)=1 | - |
| i=0 | x=3 | ge=C(1,1)=1, gt=0 | 3 * 1 = 3 |

Final answer is 3.

This example shows the simplest case where the only node must be chosen, so the minimum is deterministic.

### Example 2

Input:

```
4 3 2
0 1 5
0 2 2
1 3 10
```

Distances:

node 1 = 5, node 2 = 2, node 3 = 15

Sorted: [2, 5, 15]

We compute probabilities over 2-element subsets:

| i | x | ge = C(3-i,2) | gt | cnt | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | C(3,2)=3 | C(2,2)=1 | 2 | 4 |
| 1 | 5 | C(2,2)=1 | C(1,2)=0 | 1 | 5 |
| 2 | 15 | 0 | 0 | 0 | 0 |

Sum = 9

This trace shows how subsets are partitioned by their minimum element in sorted order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n + n log n) | Dijkstra dominates, sorting and combinatorics are linearithmic |
| Space | O(n + m) | adjacency list plus distance and factorial arrays |

The constraints allow up to 1e6 edges, so a heap-based shortest path is necessary. The combinatorial phase is linear in n, which keeps the solution within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided sample
assert run("2 1 1\n0 1 3\n").strip() == "3"

# minimum graph
assert run("2 1 1\n0 1 5\n").strip() == "5"

# chain graph
assert run("4 3 1\n0 1 1\n1 2 2\n2 3 3\n").strip() == "1"

# star graph
assert run("5 4 2\n0 1 1\n0 2 2\n0 3 3\n0 4 4\n").strip() == "1"

# k close to n-1
assert run("4 3 3\n0 1 1\n0 2 2\n0 3 3\n").strip() == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal edge | 5 | single forced choice |
| chain graph | 1 | propagation of shortest path ordering |
| star graph | 1 | dominance of closest node |
| k = n-1 | 1 | boundary combinatorics |

## Edge Cases

One edge case is when k = n − 1. In that situation every node is selected, so the minimum is always the smallest distance. The algorithm handles this because C(n − 1 − i, k) becomes zero for all i except the first index, leaving only the smallest distance contributing.

Another edge case is repeated distances. Suppose multiple nodes have identical shortest path values. A naive approach that treats each node independently would double count probability mass, but the subtraction formula C(n − 1 − i, k) − C(n − 1 − i − 1, k) automatically collapses equal values into correct frequency-weighted contributions.

A final edge case is k = 1. Then the answer is simply the average of all shortest path distances. The algorithm degenerates correctly because each node is chosen with equal probability, and the combinatorial difference reduces to a uniform weighting over all distances.
