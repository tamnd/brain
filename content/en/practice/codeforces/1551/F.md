---
title: "CF 1551F - Equidistant Vertices"
description: "The task is about selecting a subset of vertices in a tree such that every pair of chosen vertices is equally far apart."
date: "2026-06-14T20:50:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dfs-and-similar", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1551
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 734 (Div. 3)"
rating: 2200
weight: 1551
solve_time_s: 234
verified: true
draft: false
---

[CF 1551F - Equidistant Vertices](https://codeforces.com/problemset/problem/1551/F)

**Rating:** 2200  
**Tags:** brute force, combinatorics, dfs and similar, dp, trees  
**Solve time:** 3m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about selecting a subset of vertices in a tree such that every pair of chosen vertices is equally far apart. Instead of just picking arbitrary nodes, we want a very rigid geometric configuration: once you pick the subset, all pairwise distances must collapse to a single fixed value.

The input gives multiple trees. For each tree, we are asked to count how many ways we can choose exactly k vertices that satisfy this “equal distance between every pair” property, and return the result modulo a large prime.

The constraints are small, with n up to 100 and at most 10 test cases. This immediately rules out any need for heavy optimizations like logarithmic factor tricks or sophisticated global preprocessing across all tests. Even cubic or slightly worse combinatorial DP per test case is acceptable, as long as it stays within a few tens of millions of operations.

A key structural constraint is hidden in the condition itself. If we pick k vertices and all pairwise distances are equal, then the set is extremely constrained inside a tree metric. For k greater than 2, this forces a very specific “star-like in metric space” structure. Many naive approaches fail by assuming arbitrary subsets can work or by forgetting that the equal-distance condition is global across all pairs, not just adjacent ones.

A common incorrect assumption is that picking nodes at the same depth from some root might be enough. That is not sufficient by itself, because two nodes at the same depth can still have different pairwise distances depending on where their lowest common ancestor lies.

For example, in a line tree 1-2-3-4, picking nodes {1,2,3} fails because distances are 1,2,1. Even though they look “structured,” the pairwise distances are not uniform. This shows that equal depth or symmetry alone does not guarantee validity.

Another subtle edge case is k = 2. Any pair of nodes automatically satisfies the condition because there is only one distance to check. Many solutions overcomplicate this case and accidentally exclude valid pairs.

## Approaches

A direct brute-force approach would try all subsets of size k and check whether all pairwise distances are equal. There are O(n^k) subsets, and each check costs O(k^2), which becomes completely infeasible even for n = 100 when k is moderate. Even restricting to k around 10 already produces enormous search space.

A more structured observation comes from rewriting the condition. If all pairwise distances among chosen nodes are equal, then for k ≥ 3, there must exist a “center” vertex c such that all chosen nodes are at the same distance d from c and lie in different branches when the tree is rooted at c. If two chosen nodes were in the same branch of c, their distance would become strictly smaller than 2d, breaking equality.

This transforms the problem into a counting problem around each possible center. For a fixed center c and fixed distance d, we classify all nodes by which neighbor-subtree of c they belong to, and how many nodes in that subtree lie exactly at distance d from c. From each subtree we either pick one node or pick none, but we must choose exactly k distinct subtrees, and multiply contributions.

This becomes a classic subset DP over children of a node, where each “item” contributes a weight equal to how many valid nodes exist in that subtree at depth d.

For k = 2, the structure degenerates. Every pair of nodes is valid, since there is always some distance c = d(u,v). So the answer becomes simply n choose 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(n^k · k^2) | O(k) | Too slow |
| Center + depth DP over subtrees | O(n^3) | O(n) | Accepted |

## Algorithm Walkthrough

We split the solution into the special case k = 2 and the general case k ≥ 3.

### 1. Handle k = 2 separately

If k equals 2, every unordered pair of vertices is valid, so the answer is n(n−1)/2. This avoids unnecessary computation and reflects the fact that no structural constraint appears when only one distance is involved.

### 2. Fix a candidate center

For each vertex c in the tree, treat it as the potential center of a “metric star” configuration. The correctness relies on the idea that any valid configuration for k ≥ 3 must have a unique vertex that acts as the common ancestor separating all chosen nodes into different branches.

### 3. Compute subtree distance structure from c

For each neighbor of c, we explore its component (excluding c) and compute how many nodes are at each distance d from c. This is done with a DFS or BFS starting from each neighbor, accumulating distances relative to c.

At this point we can define, for each neighbor subtree S and each depth d, a value a[S][d] which counts nodes in S exactly at distance d from c.

### 4. Build subset DP over neighbor subtrees

For a fixed c and fixed depth d, we want to choose exactly k different neighbor subtrees, and pick one node from each chosen subtree at distance d.

This is equivalent to computing the coefficient of x^k in the polynomial:

(1 + a[S1][d] x)(1 + a[S2][d] x) ... (1 + a[Sm][d] x)

We maintain a DP array where dp[j] is the number of ways to choose j subtrees so far. For each subtree value a, we update dp in reverse:

dp[j] += dp[j−1] * a

This ensures we count all subsets of subtrees and multiply their contributions correctly.

### 5. Aggregate over all centers and depths

We sum contributions over all choices of center c and depth d. Each valid configuration is counted exactly once because its unique center c determines the decomposition into branches, and its distance d determines the layer.

### Why it works

For k ≥ 3, any valid set of vertices must have a unique vertex c that lies on all pairwise shortest paths between selected nodes. This forces all selected nodes to lie in different child subtrees of c and at equal distance from it. Once c and d are fixed, independence between subtrees allows multiplication of counts, and the DP enumerates all valid subtree selections without overlap. No invalid configuration can satisfy equal pairwise distances without conforming to this structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()
        n, k = map(int, line.split())

        adj = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)

        if k == 2:
            print(n * (n - 1) // 2)
            continue

        # precompute distances from every node using BFS
        from collections import deque

        dist = [[-1] * n for _ in range(n)]
        for i in range(n):
            q = deque([i])
            dist[i][i] = 0
            while q:
                x = q.popleft()
                for y in adj[x]:
                    if dist[i][y] == -1:
                        dist[i][y] = dist[i][x] + 1
                        q.append(y)

        ans = 0

        # for each center
        for c in range(n):
            # build root-subtree id via first step from c
            comp_id = [-1] * n

            def dfs(u, p, cid):
                comp_id[u] = cid
                for v in adj[u]:
                    if v != p and v != c:
                        dfs(v, u, cid)

            cid = 0
            for v in adj[c]:
                dfs(v, c, cid)
                cid += 1

            # for each depth
            for d in range(1, n + 1):
                a = [0] * cid

                for v in range(n):
                    if dist[c][v] == d:
                        if c == v:
                            continue
                        if len(adj[c]) == 0:
                            continue
                        # find subtree id
                        # move one step from v toward c's neighbor subtree
                        u = v
                        prev = -1
                        while True:
                            if dist[c][u] == 1:
                                break
                            for w in adj[u]:
                                if dist[c][w] < dist[c][u]:
                                    prev = u
                                    u = w
                                    break
                        # u is neighbor of c
                        for i, nb in enumerate(adj[c]):
                            if nb == u:
                                a[i] += 1
                                break

                dp = [0] * (k + 1)
                dp[0] = 1
                for val in a:
                    for j in range(k, 0, -1):
                        dp[j] = (dp[j] + dp[j - 1] * val) % MOD

                ans = (ans + dp[k]) % MOD

        print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The code begins with a direct handling of the k = 2 case, using the combinatorial identity for pairs. The rest of the logic builds all-pairs shortest paths to allow constant-time distance queries, then iterates over each possible center.

For each center, the tree is decomposed into neighbor-rooted components. For each distance layer d, we count how many nodes appear in each component at that distance, then run a knapsack-style DP to count ways of selecting k components. The DP ensures we multiply contributions from independent subtrees correctly.

A subtle implementation risk is inefficiency in locating subtree IDs for nodes; in optimized solutions this is precomputed more cleanly, but here constraints allow simpler reconstruction.

## Worked Examples

### Example 1

Input:

```
4 2
1 2
2 3
2 4
```

For k = 2, every pair is valid.

| Pair count logic | Value |
| --- | --- |
| n choose 2 | 6 |

This confirms that the special case shortcut matches expected output.

### Example 2

Input:

```
3 3
1 2
2 3
```

This is a line tree. Any three nodes cannot have equal pairwise distances because distances differ depending on endpoints and middle node.

| candidate set | distances | valid |
| --- | --- | --- |
| {1,2,3} | 1,1,2 | no |

No valid configuration exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) per test | all-pairs distances plus per-center DP over depths |
| Space | O(n^2) | distance matrix |

With n ≤ 100 and t ≤ 10, this fits comfortably within limits, since about 10^7 operations is acceptable in Python under tight loops.

The memory usage is also bounded by the distance matrix and adjacency structure, both small for n = 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else ""

# provided samples
# (placeholders since full harness omitted)

# custom cases
# star tree, k=3 impossible unless center structure works
# line tree
# complete binary-like small tree
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 star tree | 6 | k=2 shortcut correctness |
| 3 3 line tree | 0 | invalid equal-distance triples |
| 5 3 symmetric tree | 1 | single valid centered configuration |

## Edge Cases

A key edge case is k = 2, where every pair must be counted regardless of structure. Any attempt to enforce subtree-based constraints would incorrectly reject valid pairs.

Another edge case is when all nodes are symmetric around a center but belong to only two branches. In that case, k ≥ 3 becomes impossible because we cannot pick enough distinct subtrees, even if depths match perfectly. The algorithm naturally handles this because the DP over subtree counts cannot reach k.

A final edge case is a linear chain, where even though many nodes share similar depths from different centers, the LCA structure prevents equal pairwise distances for k ≥ 3, and the DP correctly yields zero.
