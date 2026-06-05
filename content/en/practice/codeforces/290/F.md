---
title: "CF 290F - Greedy Petya"
description: "We are given an undirected graph with up to 20 vertices and up to 400 edges, and we need to decide whether there exists a simple path that visits every vertex exactly once."
date: "2026-06-05T10:38:11+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "F"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 2800
weight: 290
solve_time_s: 68
verified: true
draft: false
---

[CF 290F - Greedy Petya](https://codeforces.com/problemset/problem/290/F)

**Rating:** 2800  
**Tags:** *special, dfs and similar, graphs, greedy  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph with up to 20 vertices and up to 400 edges, and we need to decide whether there exists a simple path that visits every vertex exactly once. This is the Hamiltonian path problem in its decision form: we are not asked to construct the path, only to say whether at least one such ordering of vertices exists where consecutive vertices are connected by edges.

The key detail is the scale of the graph. With at most 20 vertices, exponential methods become viable, but anything like enumerating all permutations of vertices directly would already be borderline because $20!$ is far too large. However, any solution with state compression over subsets of vertices, on the order of $2^n \cdot n^2$, is comfortably feasible.

One subtle point is that the graph may contain self-loops or multiple edges, and these do not affect the existence of a Hamiltonian path. A self-loop never helps in a path that must move between distinct vertices, and duplicate edges are redundant for connectivity.

A naive mistake that appears often is to interpret this as a connectivity problem. For example, checking that the graph is connected and all vertices have degree at least one is far from sufficient. A connected graph like a star with 20 vertices has a center connected to all leaves but no Hamiltonian path, since any path that enters the center can only leave it once, making it impossible to visit all leaves in a single chain.

Another failure case comes from greedy traversal. Starting from a random node and always going to an unvisited neighbor can get stuck early even when a valid Hamiltonian path exists. The local choice does not encode global constraints.

## Approaches

A brute-force approach would try all permutations of the vertices and check whether consecutive vertices are connected by edges. For each permutation, we verify adjacency in $O(n)$, and there are $n!$ permutations, giving an overall complexity of $O(n! \cdot n)$. Even at $n = 20$, this is completely infeasible.

The structure of the problem changes significantly once we observe that we only care about which subset of vertices has been visited and the last vertex in the path. Two different permutations that visit the same set of vertices and end at the same vertex are equivalent in terms of future extendability. This suggests a dynamic programming formulation over subsets.

We define a state that captures a subset of visited vertices and the endpoint of the path. From any state, we try extending the path to an unvisited neighbor. This reduces the search space from permutations to subset transitions, turning an intractable enumeration into a manageable $2^n \cdot n$ state space.

This is the standard Hamiltonian path DP, and here it fits perfectly because $n \le 20$, making $2^n \approx 10^6$, which is small enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (permutations) | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Bitmask DP over paths | $O(n^2 \cdot 2^n)$ | $O(n \cdot 2^n)$ | Accepted |

## Algorithm Walkthrough

We build a dynamic programming table where we track whether a certain subset of vertices can form a valid path ending at a particular vertex.

1. We represent each subset of vertices using a bitmask of length $n$. A bitmask encodes exactly which vertices are already included in the partial path. This representation is natural because transitions only add one vertex at a time.
2. We define a DP array where `dp[mask][v]` is true if there exists a path that visits exactly the vertices in `mask` and ends at vertex `v`. This state captures all information needed to extend the path further.
3. We initialize the DP by setting `dp[1 << v][v] = True` for every vertex `v`. Each vertex alone forms a trivial path of length one.
4. We iterate over all masks from small to large. For each mask, we try all possible endpoints `v`. If `dp[mask][v]` is true, we attempt to extend the path.
5. To extend a state `(mask, v)`, we try all neighbors `to` of `v`. If `to` is not in `mask`, we set `dp[mask | (1 << to)][to] = True`. This step corresponds exactly to appending a new vertex to the current path.
6. After processing all states, we check whether there exists any vertex `v` such that `dp[(1 << n) - 1][v]` is true. If so, a Hamiltonian path exists.

The correctness hinges on the fact that every valid Hamiltonian path has a last vertex, and the DP will eventually construct exactly that sequence of subsets leading to it.

### Why it works

The invariant is that `dp[mask][v]` is true if and only if there exists a simple path that visits exactly the vertices in `mask` and ends at `v`. Every transition preserves simplicity because we only move to unvisited vertices, and every possible extension of a valid path is considered. Since every Hamiltonian path corresponds to some ordering of subset additions, it must appear in this state space, and no invalid state is ever introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[False] * n for _ in range(n)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u][v] = True
        adj[v][u] = True

    if n == 1:
        print("Yes")
        return

    size = 1 << n
    dp = [[False] * n for _ in range(size)]

    for i in range(n):
        dp[1 << i][i] = True

    for mask in range(size):
        for v in range(n):
            if not dp[mask][v]:
                continue
            if mask == (1 << n) - 1:
                continue
            for to in range(n):
                if not adj[v][to]:
                    continue
                if mask & (1 << to):
                    continue
                dp[mask | (1 << to)][to] = True

    full = (1 << n) - 1
    for v in range(n):
        if dp[full][v]:
            print("Yes")
            return

    print("No")

if __name__ == "__main__":
    solve()
```

The adjacency matrix is used so that edge checks are constant time. This is important because the DP already runs over all subsets and endpoints, and any logarithmic overhead per transition would be too expensive.

The DP table is indexed by bitmask first because subset iteration is the natural outer loop. Each state expands only along actual edges, and we explicitly skip transitions to already visited vertices to ensure path validity.

The final scan over `dp[full]` checks whether any endpoint is reachable after visiting all vertices.

## Worked Examples

### Example 1

Input graph:

```
3 2
1 2
2 3
```

We expect a Hamiltonian path like 1 → 2 → 3.

| mask | endpoint v | dp state | transition |
| --- | --- | --- | --- |
| 001 | 1 | true | start |
| 010 | 2 | true | start |
| 100 | 3 | true | start |
| 011 | 2 | true | 1→2 |
| 110 | 3 | true | 2→3 |
| 111 | 3 | true | 1→2→3 |

At the final mask, at least one endpoint is reachable, so the answer is “Yes”.

This trace shows how partial paths merge naturally as subsets grow.

### Example 2

Input:

```
4 2
1 2
3 4
```

The graph is disconnected, so no Hamiltonian path exists.

All DP states remain confined within their components, and no transition can move from {1,2} to {3,4}. Therefore no state reaches mask 1111.

The DP never produces a full-mask state, confirming that connectivity alone inside subsets is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot 2^n)$ | Each subset-state tries up to $n$ endpoints and up to $n$ neighbors |
| Space | $O(n \cdot 2^n)$ | DP table storing states for each mask and endpoint |

With $n \le 20$, $2^n \approx 10^6$, and the constant factor around $n^2$, the solution comfortably fits within limits in Python with adjacency matrix optimizations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    output = []
    def fake_print(*args):
        output.append(" ".join(map(str, args)))

    global print
    old_print = print
    print = fake_print
    try:
        solve()
    finally:
        print = old_print

    return "\n".join(output) + ("\n" if output else "")

# provided sample
assert run("2 3\n1 2\n2 1\n1 1\n") == "Yes\n", "sample 1"

# simple path
assert run("3 2\n1 2\n2 3\n") == "Yes\n"

# disconnected graph
assert run("4 2\n1 2\n3 4\n") == "No\n"

# single node
assert run("1 0\n") == "Yes\n"

# star graph (no Hamiltonian path)
assert run("5 4\n1 2\n1 3\n1 4\n1 5\n") == "No\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | Yes | trivial base case |
| linear chain | Yes | normal DP propagation |
| disconnected pairs | No | component isolation |
| star graph | No | greedy pitfall case |

## Edge Cases

One edge case is the single vertex graph. The DP initializes `dp[1<<0][0] = true`, and since this already corresponds to the full mask, the algorithm immediately succeeds, correctly outputting “Yes”.

Another case is graphs with isolated vertices. For example, if vertex 5 has no edges, it can only appear as a standalone path. The DP correctly handles this because states starting at 5 cannot expand, and no full-mask state becomes reachable.

A more subtle case is dense graphs with missing critical edges that block a full ordering. Even if most vertices are highly connected, the DP still respects exact adjacency constraints, so it never falsely combines incompatible partial paths.
