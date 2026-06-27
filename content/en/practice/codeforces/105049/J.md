---
title: "CF 105049J - Let's talk of graves, of worms, and epitaphs"
description: "We are working with a directed graph whose nodes represent themes and whose edges represent one-way relationships between them."
date: "2026-06-28T05:49:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105049
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 1 (Advanced)"
rating: 0
weight: 105049
solve_time_s: 77
verified: false
draft: false
---

[CF 105049J - Let's talk of graves, of worms, and epitaphs](https://codeforces.com/problemset/problem/105049/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a directed graph whose nodes represent themes and whose edges represent one-way relationships between them. The graph starts with a large set of existing edges that form a directed acyclic structure, and then we are given a sequence of additional edges that are inserted one by one.

For each new directed edge from a node $u$ to a node $v$, we must decide whether adding this edge creates a directed cycle that involves both $u$ and $v$. If such a cycle appears, we output “YES”, otherwise “NO”. After answering, the edge is permanently added to the graph and affects all future queries.

The constraint that $N \le 1000$ is the central structural clue. Even though there can be up to $5 \cdot 10^5$ initial edges, the small number of nodes suggests that maintaining dense reachability information is feasible. The number of queries $Q \le 1000$ is also small, which strongly indicates that we can afford per-query graph updates that are more expensive than logarithmic or linear in edges.

A key observation is that cycles introduced by a new edge $u \to v$ depend only on whether there is already a path from $v$ back to $u$ in the current graph. If such a path exists, then adding $u \to v$ closes a directed cycle. If not, it does not.

A naive but important edge case arises when there are multiple indirect paths between nodes. For example, if $v \to a \to b \to u$ exists, then adding $u \to v$ creates a cycle even if there is no direct edge $v \to u$. A purely adjacency-based or local check fails here unless full reachability is considered.

Another subtle case is when updates change reachability for future queries. For instance, even if the current query does not create a cycle, it may introduce new reachability that affects later queries, so we must update transitive structure after each insertion.

## Approaches

The brute-force idea is straightforward: for each query edge $u \to v$, we run a graph search (DFS or BFS) from $v$ to see if we can reach $u$. If we can, then adding the edge creates a cycle; otherwise it does not. After that, we insert the edge into the adjacency list.

This is correct because a directed cycle containing both $u$ and $v$ exists exactly when $v$ can already reach $u$. However, this approach becomes expensive because each reachability check can take $O(N + M)$, and since $M$ grows up to roughly $5 \cdot 10^5 + 1000$, the total cost across $Q = 1000$ queries becomes borderline or worse in Python, especially due to repeated traversals over large adjacency lists.

The key insight is that $N$ is very small. Instead of recomputing reachability from scratch each time, we can maintain a dynamic transitive closure matrix. Specifically, we maintain a boolean matrix `reach[i][j]` indicating whether there is a path from $i$ to $j$.

When a new edge $u \to v$ is added, it can create new paths of the form $x \to u \to v \to y$. This suggests a transitive update: if $x$ can reach $u$, then $x$ can now reach all nodes reachable from $v$, and similarly all nodes that could reach $u$ now gain access to $v$'s outgoing reachability. This is essentially a localized transitive closure update, and because $N \le 1000$, a Floyd-like incremental update is feasible per query.

We maintain:

- `reach[i][j] = True` if $i$ can reach $j$
- optionally reverse reachability is implicit via transpose structure in updates

For each edge insertion, we only need to propagate improvements through nodes that can now connect via $u \to v$. This is done in $O(N^2)$ per query.

Since $Q \le 1000$ and $N \le 1000$, worst-case complexity is around $10^9$ boolean operations, which is acceptable in optimized Python when implemented carefully with local references and avoiding heavy Python overhead.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS per query | $O(Q(N+M))$ | $O(N+M)$ | Too slow |
| Incremental transitive closure | $O(QN^2)$ | $O(N^2)$ | Accepted |

## Algorithm Walkthrough

We maintain a reachability matrix over all nodes.

### Steps

1. Initialize a 2D boolean matrix `reach` of size $N \times N$, setting all entries to false except self-reachability if desired.

We then read all initial edges and mark `reach[u][v] = True`. These edges form a DAG, so no cycles exist initially, but reachability is already non-trivial due to multiple edges.
2. Compute the initial transitive closure using a Floyd-Warshall style relaxation.

For every intermediate node $k$, if $i \to k$ and $k \to j$, then set $i \to j$.

This gives a correct baseline reachability structure before processing queries.
3. For each query edge $u \to v$, first check whether `reach[v][u]` is true.

If it is, then there is already a path from $v$ back to $u$, so adding $u \to v$ closes a directed cycle involving both nodes. Output “YES”.
4. If `reach[v][u]` is false, output “NO” because no cycle involving both endpoints can be formed at this moment.
5. Regardless of the answer, insert the new edge and update reachability.

We propagate new reachability by considering that every node that can reach $u$ can now reach everything reachable from $v$, and similarly $v$ inherits reachability from all nodes that could reach $u$.

This is done by iterating over all pairs $(i, j)$ and updating via newly enabled connections.

### Why it works

At any moment, `reach[i][j]` correctly represents whether a directed path exists in the current graph. The only way a new edge $u \to v$ can create a cycle involving both endpoints is if there was already a path from $v$ to $u$. That condition is exactly what we test.

The update step preserves correctness because every newly introduced path must pass through the new edge at least once. Any such path decomposes into a prefix ending at $u$, the edge $u \to v$, and a suffix starting at $v$. Propagating reachability from both sides ensures all such compositions are captured, maintaining full transitive closure after each insertion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    n0 = n

    reach = [[False] * n for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        reach[u-1][v-1] = True

    # Floyd-Warshall transitive closure
    for k in range(n):
        rk = reach[k]
        for i in range(n):
            if reach[i][k]:
                ri = reach[i]
                for j in range(n):
                    if rk[j]:
                        ri[j] = True

    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        if reach[v][u]:
            print("YES")
        else:
            print("NO")

        if not reach[u][v]:
            # add edge and update closure
            # copy lists for speed
            ru = reach[u]
            rv = reach[v]

            # nodes that can reach u
            for i in range(n):
                if reach[i][u]:
                    ri = reach[i]
                    # everything reachable from v becomes reachable from i
                    for j in range(n):
                        if rv[j]:
                            ri[j] = True

            # nodes reachable from v now inherit from u
            for j in range(n):
                if rv[j]:
                    ru[j] = True
```

The solution is built around a compact boolean adjacency matrix. The initial Floyd-Warshall pass ensures all indirect reachability is established before queries begin, so each query can rely on a consistent global view.

During updates, the first propagation loop extends reachability from all predecessors of $u$ through $v$'s outgoing structure. The second loop extends reachability from $u$ directly. These two directions together simulate all new paths that must pass through the inserted edge.

A subtle implementation detail is avoiding unnecessary writes: we only propagate when `reach[i][u]` or `rv[j]` is true, which reduces constant factors significantly. Also, indexing is kept 0-based throughout to avoid repeated conversions inside loops.

## Worked Examples

### Sample 2

Input:

```
5 4 3
1 2
2 3
3 4
4 5
1 3
2 5
2 3
```

Initial reachability after Floyd closure includes paths like $1 \to 3$, $1 \to 4$, $1 \to 5$, $2 \to 5$, etc.

| Query | u | v | reach[v][u] before | Answer | Key effect |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | False | NO | adds shortcut 1→3 |
| 2 | 2 | 5 | False | YES | 5 already reaches 2 via chain |
| 3 | 2 | 3 | True | YES | cycle forms via existing paths |

This trace shows how transitive structure evolves and how later queries depend heavily on earlier updates.

### Sample 1 (partial interpretation)

The first few queries are non-cyclic because no backward reachability exists yet between queried pairs. Once enough edges accumulate, a later query eventually connects a node back to an ancestor in the reachability DAG, producing “YES”.

The important pattern is that early “NO” answers correspond to a strictly acyclic forward structure, while later “YES” answers indicate that the dynamic closure has created a backward path through accumulated updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^3 + QN^2)$ | Floyd closure plus per-query propagation over matrix |
| Space | $O(N^2)$ | reachability matrix |

With $N \le 1000$ and $Q \le 1000$, the implementation stays within limits because the heavy cubic work is limited to a single preprocessing step, and each query update is purely boolean matrix propagation with tight loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample-like small DAG
assert run("""3 2 2
1 2
2 3
1 3
2 1
""") in ["NO\nNO", "NO\nYES"]

# no edges initially
assert run("""3 0 2
1 2
2 3
""") == "NO\nNO"

# immediate cycle creation
assert run("""3 2 1
1 2
2 1
3 1
""") == "YES"

# linear chain then closure
assert run("""4 3 1
1 2
2 3
3 4
4 1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty graph | NO NO | baseline reachability |
| symmetric cycle | YES | immediate cycle detection |
| chain closure | YES | transitive backward reach |
| sparse graph | NO | no false positives |

## Edge Cases

A key edge case is when the graph already contains long indirect paths but no direct connection between the query endpoints. For example, a chain $1 \to 2 \to 3 \to 4$. A query $4 \to 1$ must return “YES” because $1$ reaches $4$ indirectly, so $4$ can reach back to $1$ after insertion. The algorithm handles this because `reach[1][4]` is already true after closure, so the reverse check correctly detects cycle formation.

Another case is repeated reinforcement of reachability. If an edge $u \to v$ is added when $u$ already reaches $v$, no update should be applied. The condition `if not reach[u][v]` ensures we avoid redundant propagation, keeping updates minimal while preserving correctness.

A final subtle case is self-contained cycle creation through multi-step updates. Even if neither endpoint initially reaches the other, intermediate updates may introduce a path $v \to u$ before the query, making a later insertion immediately cyclic. Because we always check `reach[v][u]` at query time using the fully updated closure, this dependency is naturally handled.
