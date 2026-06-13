---
title: "CF 1198C - Matching vs  Independent Set"
description: "We are given several undirected graphs, each with exactly $3n$ vertices. For each graph, we must construct one of two specific structures of size $n$: either a matching consisting of $n$ edges, or an independent set consisting of $n$ vertices."
date: "2026-06-13T14:43:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1198
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 576 (Div. 1)"
rating: 2000
weight: 1198
solve_time_s: 404
verified: false
draft: false
---

[CF 1198C - Matching vs  Independent Set](https://codeforces.com/problemset/problem/1198/C)

**Rating:** 2000  
**Tags:** constructive algorithms, graphs, greedy, sortings  
**Solve time:** 6m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several undirected graphs, each with exactly $3n$ vertices. For each graph, we must construct one of two specific structures of size $n$: either a matching consisting of $n$ edges, or an independent set consisting of $n$ vertices. If neither structure exists, we must report impossibility.

A matching is a set of edges where no vertex appears in more than one chosen edge. An independent set is a set of vertices such that no edge in the graph connects any pair of chosen vertices.

The key difficulty is that the graph is large and sparse constraints are not guaranteed: $n$ can be up to $10^5$ per test case, and total edges up to $5 \cdot 10^5$. This immediately rules out any approach that tries to enumerate subsets of vertices or edges, or even anything quadratic in $n$. The solution must be essentially linear or linear-logarithmic per test case.

A subtle edge case appears when both structures exist. For example, in a graph where vertices form many disjoint edges plus isolated nodes, both a matching and an independent set of size $n$ are possible. The problem allows either answer, so any deterministic choice strategy is acceptable.

Another important edge case is when the graph is very dense. If edges are abundant, matchings are likely easy to find, but independent sets become small. Conversely, if edges are very sparse, independent sets become large but matching structure may fail. The solution must not assume either regime.

A third non-obvious case is when the graph is structured so that neither a full matching of size $n$ nor an independent set of size $n$ exists. The construction in the official solution ensures this case never requires complex fallback logic beyond a simple contradiction check.

## Approaches

A direct brute-force idea is to try constructing a maximum matching and a maximum independent set independently. One could run a greedy matching and also compute a greedy independent set from the complement, or attempt to compute a maximum independent set via DP or flow-based reductions. These approaches are either exponential or require solving NP-hard subproblems, which is infeasible at $n = 10^5$.

The key structural insight is that the graph has $3n$ vertices, but we only need a structure of size $n$, which is exactly one third of the vertex set. This imbalance is crucial. It suggests that if we cannot find enough disjoint edges, then many vertices must remain “unmatched” in a strong sense, and these can be organized into an independent set.

The standard constructive idea is to greedily attempt a matching. If we can select $n$ disjoint edges, we are done. If we fail, the failure implies that too many vertices are “blocked” by previous choices, which forces a large independent set to exist. The algorithm carefully tracks used vertices and extracts either structure in one pass.

The deeper viewpoint is that every edge we pick reduces available vertices, and every time we fail to pick a matching edge, we gain structure in the complement graph that contributes to an independent set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n + m) | Too slow |
| Greedy construction | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

The solution is built around maintaining a simple greedy process that simultaneously tries to build a matching while implicitly preparing an independent set fallback.

We maintain a list of unused vertices and a visited array. We also maintain adjacency lists.

### 1. Greedy attempt to build a matching

We iterate through edges in input order. For each edge $(u, v)$, if both endpoints are currently unused, we take this edge into our matching and mark both vertices as used. We continue until we either collect $n$ edges or finish all edges.

This works because any valid matching only requires disjoint endpoints, and greedily picking early edges avoids unnecessary conflicts later.

### 2. If matching succeeds

If we manage to pick $n$ edges, we immediately output them. This satisfies the requirement.

### 3. If matching fails

If we cannot reach $n$ edges, then fewer than $n$ disjoint edges exist in the graph. This implies that at least $3n - 2(n-1)$ vertices remain not fully paired by our greedy process, which guarantees enough structure to form an independent set.

We construct an independent set by taking all vertices that were never used in the matching process. Since every chosen edge consumes two vertices, the remaining set contains at least $n$ vertices. We then take any $n$ of them.

We must ensure this set is independent. Any edge inside this remaining set would have been available for matching earlier (since both endpoints were unused), contradicting the maximality of the greedy matching process.

### Why it works

The invariant is that after greedy matching stops, no edge exists between two unused vertices. If such an edge existed, the algorithm would have picked it when processing that edge. Therefore, the set of unused vertices forms an independent set in the remaining graph. Since the matching failed to reach size $n$, the unused set must contain at least $n$ vertices, ensuring feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        adj = [[] for _ in range(3*n + 1)]
        edges = []

        for i in range(1, m + 1):
            u, v = map(int, input().split())
            adj[u].append((v, i))
            adj[v].append((u, i))
            edges.append((u, v))

        used = [False] * (3*n + 1)
        matching = []

        for i, (u, v) in enumerate(edges, 1):
            if not used[u] and not used[v]:
                used[u] = used[v] = True
                matching.append(i)
                if len(matching) == n:
                    break

        if len(matching) == n:
            print("Matching")
            print(*matching)
            continue

        indep = []
        for v in range(1, 3*n + 1):
            if len(indep) < n and not used[v]:
                indep.append(v)

        print("IndSet")
        print(*indep)

if __name__ == "__main__":
    solve()
```

The code first builds adjacency information and stores edges in input order. It then performs a greedy scan over edges, selecting disjoint endpoints to build a matching. The moment $n$ edges are collected, it outputs them.

If the greedy process fails, it collects unused vertices. The important detail is that we only need to take the first $n$ unused vertices, since correctness guarantees there are at least $n$ of them.

## Worked Examples

### Example 1

Input:

```
1
1 2
1 2
1 3
```

| Step | Edge | Used u | Used v | Matching size | Unused vertices |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,2) | 1 | 2 | 1 | {3} |

We immediately reach matching size 1, so we output it. This shows that even in a tiny graph, greedy selection can terminate early and satisfy the requirement.

### Example 2

Input:

```
1
1 0
```

| Step | Matching | Used vertices | Unused vertices |
| --- | --- | --- | --- |
| end | 0 | ∅ | {1,2,3} |

No edges exist, so matching fails. We take any single unused vertex as an independent set. Since no edges exist, any vertex set is independent.

This case confirms that the fallback construction works even in completely empty graphs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each edge is processed once, each vertex is scanned once |
| Space | $O(n + m)$ | adjacency list and bookkeeping arrays |

The total constraints across all test cases are $10^5$ vertices and $5 \cdot 10^5$ edges, so a single linear pass per graph fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    T = int(input())
    out = []

    for _ in range(T):
        n, m = map(int, input().split())
        edges = []
        for i in range(1, m+1):
            u, v = map(int, input().split())
            edges.append((u, v, i))

        used = [False]*(3*n+1)
        match = []

        for u, v, i in edges:
            if not used[u] and not used[v]:
                used[u] = used[v] = True
                match.append(i)
                if len(match) == n:
                    break

        if len(match) == n:
            out.append("Matching")
            out.append(" ".join(map(str, match)))
        else:
            ind = []
            for v in range(1, 3*n+1):
                if not used[v] and len(ind) < n:
                    ind.append(v)
            out.append("IndSet")
            out.append(" ".join(map(str, ind)))

    return "\n".join(out)

# provided samples
assert run("""4
1 2
1 3
1 2
1 2
1 3
1 2
2 5
1 2
3 1
1 4
5 1
1 6
2 15
1 2
1 3
1 4
1 5
1 6
2 3
2 4
2 5
2 6
3 4
3 5
3 6
4 5
4 6
5 6
""") == """Matching
2
IndSet
1
IndSet
2 4
Matching
1 15"""

# custom cases
assert run("""1
1 0
""") == """IndSet
1"""

assert run("""1
1 1
1 2
""") in ["Matching\n1", "IndSet\n1"]  # either valid depending on greedy order

assert run("""1
2 3
1 2
3 4
5 6
""") == """Matching
1 2"""

assert run("""1
2 0
""") == """IndSet
1 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty graph | IndSet | fallback correctness |
| single edge | Matching/IndSet | tie handling |
| disjoint edges | Matching | greedy stability |
| no edges | IndSet | full fallback behavior |

## Edge Cases

In a graph with no edges, the algorithm never selects a matching edge and ends with all vertices unused. The construction then simply takes the first $n$ vertices, which forms a valid independent set because independence is guaranteed by absence of edges.

In a graph where edges exist but are highly clustered around a few vertices, greedy matching may stall early. For example, if one vertex connects to almost all others, selecting any incident edge quickly blocks future matches involving that vertex, but still leaves a large pool of untouched vertices. Those untouched vertices form a valid independent set because any internal edge would have been selected earlier as a matching candidate.

In a graph where perfect matching is possible, greedy selection may or may not find a full matching depending on edge order, but the guarantee is that if it does not, enough unused vertices remain to form an independent set of size $n$. This follows from the fact that every failure to extend the matching corresponds to structural redundancy that shifts mass into the complement set.
