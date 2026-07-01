---
title: "CF 104328B - John and AndMax"
description: "We are given a directed acyclic graph where every vertex carries a 20-bit integer value. The task is to choose a path that moves along directed edges, uses exactly $k$ vertices, and computes a score defined as the bitwise AND of all values along the path."
date: "2026-07-01T19:03:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104328
codeforces_index: "B"
codeforces_contest_name: "FIICode2023"
rating: 0
weight: 104328
solve_time_s: 78
verified: true
draft: false
---

[CF 104328B - John and AndMax](https://codeforces.com/problemset/problem/104328/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph where every vertex carries a 20-bit integer value. The task is to choose a path that moves along directed edges, uses exactly $k$ vertices, and computes a score defined as the bitwise AND of all values along the path. Among all valid paths of length $k$, we want the maximum possible result of this AND.

So the problem is not about finding a shortest or longest path in the classical sense, but about selecting a constrained-length path that preserves as many common set bits as possible across all chosen vertices.

The key difficulty comes from the interaction between structure and bitwise operations. The graph restricts transitions, while the AND operation strongly depends on which vertices appear together. A single zero bit in any chosen vertex permanently destroys that bit in the final result.

The constraints are large: up to $2 \cdot 10^5$ vertices and edges, and $k$ can also be as large as $n$. Any solution that tries to enumerate paths or maintain states per path will fail because even storing all partial paths is exponential in $k$, and even DP over all paths without compression leads to $O(nk)$ which is borderline but still too large given $m$ as well.

The structure being a DAG is crucial. It guarantees no cycles, so we can process vertices in topological order and ensures that any path has length at most $n$.

A subtle failure case for naive approaches is assuming greediness works locally. For example, picking at each step the neighbor with maximum value does not work because a locally optimal vertex might eliminate bits that are necessary for future continuation.

Another failure case is treating it like a longest path DP with scalar weights. Here the “weight” is not additive or monotonic, so merging subproblems using a single best value per node is insufficient. We must remember more information than just one best score per vertex.

## Approaches

A brute force idea is to define a DP over paths: for every vertex and every length, compute the best possible AND value of a path ending at that vertex with that length. Transitioning would consider all incoming edges. This leads to a recurrence of the form $dp[v][t] = \max_{u \to v}(dp[u][t-1] \& a_v)$.

This is correct but too slow. The state space is $O(nk)$, and each transition scans incoming edges, producing $O(mk)$, which in worst case reaches $2 \cdot 10^{10}$ operations.

The key observation is that the value space is not arbitrary. Each number is at most 20 bits, so there are at most $2^{20}$ possible masks, and AND operations only delete bits. This suggests a bit-level construction: instead of computing exact DP values, we try to construct the answer greedily from the highest possible mask downward.

We reverse the viewpoint: instead of asking “what is the best AND for each path”, we ask “can we achieve a given mask as the AND of a length-k path?”. If a mask is achievable, then all its submasks are also achievable. This monotonicity allows binary searching or greedy bit building.

We build the answer bit by bit from the most significant to the least significant. At each step, we tentatively force a bit to 1 and check whether there exists a path of length $k$ using only vertices whose values contain all currently fixed bits. The check reduces to a constrained reachability DP over the DAG, where we only propagate through allowed vertices.

Because each feasibility check is $O(n + m)$, and we do this for at most 20 bits, the total complexity becomes $O(20(n + m))$, which is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over paths | $O(mk)$ | $O(nk)$ | Too slow |
| Bitmask greedy feasibility over DAG | $O(20(n + m))$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as constructing the maximum bitmask that can appear as the AND of a valid length-k path.

### Steps

1. Compute a topological ordering of the DAG.

This ensures we can propagate path information in a single forward pass without revisiting nodes.
2. Initialize the answer mask as 0.

We will try to set bits from high to low.
3. For each bit from 19 down to 0, attempt to set it in the answer mask.

We temporarily define a candidate mask that includes all previously fixed bits plus this new bit.
4. Filter vertices that are compatible with the candidate mask, meaning all bits in the candidate are present in the vertex value.

Any vertex failing this cannot appear in a valid path under this mask.
5. Run a DP over the DAG in topological order to compute the maximum path length achievable starting from each valid node.

For each node, if it is valid, its best chain length is 1 plus the maximum over all outgoing neighbors that are also valid.
6. If any node achieves a path length at least $k$, then the candidate mask is feasible, so we keep the bit. Otherwise, we discard it.
7. After processing all bits, output the constructed mask.

The DP inside each feasibility check is the key computational step. It essentially asks: within the subgraph induced by allowed vertices, does there exist a path of length at least $k$? Because the graph is a DAG, this reduces to a longest path problem in a DAG restricted to valid nodes.

### Why it works

The algorithm maintains the invariant that at every step, the current mask represents a value achievable by at least one valid path of length $k$. Each feasibility check ensures that adding a new bit does not destroy this property. Since AND only removes bits and never introduces them, any extension of the mask only makes the vertex set smaller, never larger. Therefore feasibility is monotonic with respect to bit removal, which justifies greedy construction from high bits downward.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(mask, n, adj, topo, a, k):
    valid = [False] * n
    for i in range(n):
        if (a[i] & mask) == mask:
            valid[i] = True

    dp = [0] * n
    best = 0

    for u in topo:
        if not valid[u]:
            continue
        dp[u] = max(dp[u], 1)
        for v in adj[u]:
            if valid[v]:
                if dp[u] + 1 > dp[v]:
                    dp[v] = dp[u] + 1
        best = max(best, dp[u])

    return best >= k

def topo_sort(n, adj):
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1

    stack = [i for i in range(n) if indeg[i] == 0]
    topo = []

    while stack:
        u = stack.pop()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    return topo

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)

    topo = topo_sort(n, adj)

    ans = 0
    for b in range(19, -1, -1):
        cand = ans | (1 << b)
        if can(cand, n, adj, topo, a, k):
            ans = cand

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first constructs a topological ordering so that all transitions respect DAG direction. This is necessary because the feasibility DP relies on processing nodes in dependency order without revisiting states.

The `can` function enforces the current bitmask constraint by filtering vertices. Any node that lacks a required bit is excluded entirely. Then a longest-path-like DP runs over the DAG, but only among valid nodes. If any node reaches a chain length of at least $k$, we accept the mask.

The outer loop greedily builds the answer from the highest bit to the lowest, ensuring lexicographically maximum bitmask.

A subtle point is that we do not need to track exact paths, only the longest valid chain. Since we only care whether a length-$k$ path exists, DP values beyond $k$ are irrelevant.

## Worked Examples

### Sample 1

We start with mask 0 and try to activate bits from 19 down.

At each candidate mask, we check whether a valid length-4 path exists using only compatible nodes.

| Step | Mask Attempted | Valid nodes exist | Longest path found | Decision |
| --- | --- | --- | --- | --- |
| b=19..high | 0 | all nodes | ≥4 | keep |
| higher bits | various | restricted | <4 or ≥4 | selective |
| final | 10 | valid chain exists | 4 | accept |

The final constructed mask is 10.

This trace shows that intermediate restrictions may remove many nodes, but still preserve a long enough chain.

### Sample 2

We repeat the same greedy construction.

| Step | Mask Attempted | Valid nodes exist | Longest path found | Decision |
| --- | --- | --- | --- | --- |
| start | 0 | all nodes | ≥4 | keep |
| high bits | progressively restricted | varying | sometimes <4 | discard |
| final | 32 | valid chain exists | 4 | accept |

This demonstrates that higher bits may survive even under strong filtering, as long as a compatible DAG path remains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(20(n + m))$ | Each of 20 bits triggers one DAG DP over all nodes and edges |
| Space | $O(n + m)$ | adjacency list, topo order, and DP arrays |

The complexity fits comfortably within limits since $n, m \le 2 \cdot 10^5$. Even in worst case, we perform about 4 million edge relaxations, which is well within 1 second in optimized Python with adjacency lists.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def topo_sort(n, adj):
        indeg = [0]*n
        for u in range(n):
            for v in adj[u]:
                indeg[v]+=1
        stack = [i for i in range(n) if indeg[i]==0]
        topo=[]
        while stack:
            u=stack.pop()
            topo.append(u)
            for v in adj[u]:
                indeg[v]-=1
                if indeg[v]==0:
                    stack.append(v)
        return topo

    def can(mask, n, adj, topo, a, k):
        valid=[False]*n
        for i in range(n):
            if (a[i]&mask)==mask:
                valid[i]=True
        dp=[0]*n
        best=0
        for u in topo:
            if not valid[u]: continue
            dp[u]=max(dp[u],1)
            best=max(best,dp[u])
            for v in adj[u]:
                if valid[v]:
                    dp[v]=max(dp[v], dp[u]+1)
        return best>=k

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u,v = map(int, input().split())
        adj[u-1].append(v-1)

    topo = topo_sort(n, adj)
    ans=0
    for b in range(19,-1,-1):
        if can(ans|(1<<b), n, adj, topo, a, k):
            ans|=(1<<b)
    return str(ans).strip()

# provided samples
assert run("""5 8 4
11 26 15 3 26
1 5
2 3
2 5
3 1
3 5
4 1
4 3
4 5
""") == "10"

assert run("""7 12 4
36 47 47 31 33 15 34
1 6
1 7
2 4
2 5
3 2
3 7
4 1
4 5
4 6
5 7
6 5
6 7
""") == "32"

# custom cases
assert run("""2 1 2
3 3
1 2
""") == "3", "minimum chain"

assert run("""3 2 3
7 7 7
1 2
2 3
""") == "7", "all equal values"

assert run("""4 3 2
8 4 2 1
1 2
2 3
3 4
""") == "0", "no common bit survives"

assert run("""5 4 3
31 31 31 31 31
1 2
2 3
3 4
4 5
""") == "31", "full preservation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain of length 2 | 3 | minimum-length feasibility |
| all equal values | 7 | full propagation correctness |
| strictly decreasing bits | 0 | complete bit elimination |
| fully uniform DAG | 31 | maximal mask retention |

## Edge Cases

A key edge case is when only one path of length $k$ exists, and all other nodes are incompatible with higher bits. The algorithm handles this correctly because feasibility depends on existence of any valid chain, not global density.

For example:

```
4 3 3
7 6 7 7
1 2
2 3
3 4
```

When testing a high bit that is missing in node 2, that node is excluded, and the chain breaks, causing the DP to fail for that mask. The algorithm then correctly discards that bit and continues downward.

Another edge case is when multiple paths exist but only one preserves a rare bit. Since the DP computes maximum path length over all valid nodes, it naturally picks that rare path if it reaches length $k$, ensuring correctness without explicitly tracking paths.
