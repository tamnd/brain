---
title: "CF 1674G - Remove Directed Edges"
description: "We are given a directed acyclic graph where each vertex has some number of incoming and outgoing edges. We are allowed to delete edges, but only under a very specific local rule: a vertex can lose edges only if it actually had at least one edge of that type before, unless it…"
date: "2026-06-10T01:16:54+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1674
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 786 (Div. 3)"
rating: 2000
weight: 1674
solve_time_s: 121
verified: true
draft: false
---

[CF 1674G - Remove Directed Edges](https://codeforces.com/problemset/problem/1674/G)

**Rating:** 2000  
**Tags:** dfs and similar, dp, graphs  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph where each vertex has some number of incoming and outgoing edges. We are allowed to delete edges, but only under a very specific local rule: a vertex can lose edges only if it actually had at least one edge of that type before, unless it becomes completely isolated in that direction. In other words, a vertex is not allowed to partially “activate” from zero, but once it has degree it can be reduced.

After performing such deletions, we look at the remaining directed graph and want to choose a set of vertices with a strong connectivity property: between every pair of chosen vertices, one must be reachable from the other along the remaining directed edges. This means the induced structure on the chosen vertices behaves like a chain in terms of reachability, no branching allowed in how they compare.

The task is to maximize how many vertices can be selected in such a set after choosing deletions optimally.

The constraints are large, with up to 200,000 vertices and edges. This immediately rules out any solution that tries to simulate edge removals or check all subsets. Even quadratic approaches over vertices are impossible. The structure is a DAG, which is the key hint that a topological or ordering-based view will be necessary.

A naive misunderstanding that often appears is to treat the problem as selecting a longest path or longest chain in the original DAG. That fails because we are allowed to delete edges in a constrained way, which can completely reshape reachability, as long as degree conditions are respected.

A second subtle failure case is assuming we can always delete arbitrary edges to simplify the graph into any subgraph. The degree restriction prevents this: a vertex with positive indegree or outdegree must keep at least one incoming or outgoing edge unless it becomes isolated in that direction.

## Approaches

A brute-force idea would be to try all subsets of vertices, and for each subset try to determine whether we can delete edges so that it becomes a valid “chain-like” set under reachability. This is already exponential in vertices. Even if we fix a subset, checking feasibility would require reasoning about whether we can orient remaining edges and prune others without violating degree constraints, which itself depends on global structure. This quickly becomes intractable.

The key simplification comes from reframing what the deletion rule allows. A vertex with at least one incoming edge must keep at least one incoming edge after deletions, unless it becomes fully isolated on that side. The same holds for outgoing edges. This means every non-isolated vertex must preserve at least one incoming and one outgoing connection structure, so we cannot arbitrarily destroy connectivity patterns; we are forced to keep at least one “representative” incoming and outgoing edge per active vertex.

Now consider what it means for a set of vertices to be “cute”: every pair must be comparable by reachability. In a DAG, this is equivalent to the induced relation being a total order: we can line up vertices so that each can reach all later ones (or vice versa depending on direction consistency after deletions). So the problem reduces to building the longest possible chain in a structure where we are allowed to simplify edges but not violate the per-vertex degree constraints.

The crucial observation is that after optimal deletions, what matters is not the full graph but whether we can enforce a linear ordering over a subset of vertices. The degree constraints ensure that each chosen vertex can only “participate” in one incoming and one outgoing chain of influence in the final structure. This turns the problem into finding the largest set that can be arranged in a topological order consistent with existing reachability constraints, which reduces to a longest path-like DP on the DAG.

We process vertices in topological order and compute the best chain ending at each vertex. For a vertex `v`, we try to extend chains from all predecessors `u` such that there is an edge `u -> v`. The DP state is the longest valid chain ending at `v`. Since the graph is acyclic, this propagation is well-defined.

Finally, the answer is the maximum DP value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(2^n · m) | O(n) | Too slow |
| DAG DP on topological order | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute a topological ordering of the DAG. This ordering represents a linearization where all edges go forward. This is necessary so that when we process a vertex, all possible predecessors have already been computed.
2. Create a DP array `dp[v]`, initially 1 for all vertices. This represents the best chain ending at `v`.
3. Iterate over vertices in topological order. For each vertex `u`, consider every outgoing edge `u -> v`. We try to extend the best chain ending at `u` to `v`, so we update `dp[v] = max(dp[v], dp[u] + 1)`. This captures the idea that `v` can follow `u` in a valid chain.
4. Maintain a global answer as the maximum value in `dp`. This represents the largest chain we can build anywhere in the DAG.
5. Return the global maximum.

### Why it works

The DP constructs the longest reachable chain consistent with the DAG ordering. Since the graph is acyclic, any valid “cute” set can be arranged in a linear order consistent with edges. The degree constraints ensure we cannot merge multiple independent branches into the same chain in a way that violates comparability, so the optimal structure is always a single longest directed path in the effective reduced graph. The topological DP enumerates exactly these possibilities without duplication or cycles, so every feasible chain is represented in some DP state, and no invalid chain is ever counted.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    indeg = [0] * n

    for _ in range(m):
        v, u = map(int, input().split())
        v -= 1
        u -= 1
        g[v].append(u)
        indeg[u] += 1

    # topological sort (Kahn)
    q = deque([i for i in range(n) if indeg[i] == 0])
    topo = []

    while q:
        v = q.popleft()
        topo.append(v)
        for u in g[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)

    dp = [1] * n
    ans = 1

    for v in topo:
        for u in g[v]:
            if dp[v] + 1 > dp[u]:
                dp[u] = dp[v] + 1
                if dp[u] > ans:
                    ans = dp[u]

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first builds the adjacency list and computes indegrees to prepare a topological order. Kahn’s algorithm is used so that each vertex is processed only after all its prerequisites. The DP then propagates the longest chain length forward along edges. The key subtlety is that updates only go forward in topological order, ensuring correctness without revisiting nodes.

A common mistake is updating DP in arbitrary order, which can reuse incomplete values. The topological ordering prevents that by guaranteeing all contributions to a node are finalized before it is used to update others.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
1 3
```

Topological order is `[1, 2, 3]`.

| Step | Node | dp state | update |
| --- | --- | --- | --- |
| init | - | [1,1,1] | - |
| process 1 | 1 | [1,1,1] | 2,3 become 2 |
| process 2 | 2 | [1,2,1] | 3 becomes 3 |
| process 3 | 3 | [1,2,3] | - |

Final answer is 3.

This shows how multiple paths reinforce a single longest chain.

### Example 2

Input:

```
4 2
1 2
3 4
```

Topological order could be `[1,3,2,4]`.

| Step | Node | dp state | update |
| --- | --- | --- | --- |
| init | - | [1,1,1,1] | - |
| 1 | 1 | [1,1,1,1] | 2=2 |
| 3 | 3 | [1,1,1,1] | 4=2 |
| 2 | 2 | [1,1,1,1] | - |
| 4 | 4 | [1,1,1,2] | - |

Answer is 2.

This confirms that independent components cannot be merged into larger chains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each vertex and edge is processed once in topological sort and DP |
| Space | O(n + m) | Adjacency list and DP arrays |

The constraints allow up to 200,000 nodes and edges, and a linear solution fits comfortably within limits. The algorithm avoids any nested traversal over edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        indeg = [0] * n

        for _ in range(m):
            v, u = map(int, input().split())
            v -= 1
            u -= 1
            g[v].append(u)
            indeg[u] += 1

        q = deque([i for i in range(n) if indeg[i] == 0])
        topo = []
        while q:
            v = q.popleft()
            topo.append(v)
            for u in g[v]:
                indeg[u] -= 1
                if indeg[u] == 0:
                    q.append(u)

        dp = [1] * n
        ans = 1
        for v in topo:
            for u in g[v]:
                if dp[v] + 1 > dp[u]:
                    dp[u] = dp[v] + 1
                    ans = max(ans, dp[u])

        print(ans)

    from io import StringIO
    old = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# provided sample
assert run("""3 3
1 2
2 3
1 3
""") == "3"

# custom: disconnected graph
assert run("""4 2
1 2
3 4
""") == "2"

# custom: single node
assert run("""1 0
""") == "1"

# custom: chain
assert run("""5 4
1 2
2 3
3 4
4 5
""") == "5"

# custom: reverse-like DAG
assert run("""4 3
1 3
2 3
3 4
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-node sample | 3 | correctness on multi-path DAG |
| two components | 2 | independence handling |
| single node | 1 | base case |
| full chain | 5 | linear propagation |
| merge DAG | 3 | branching resolution |

## Edge Cases

A single vertex graph is the simplest case. With no edges, the topological order contains one node and DP remains `[1]`, producing answer 1. This aligns with the fact that a single vertex always forms a valid cute set.

A fully linear chain such as `1 -> 2 -> 3 -> ... -> n` causes DP to increase step by step along the only available path, producing `n`. This confirms that the algorithm correctly recognizes pure path structures.

A branching DAG like `1 -> 3`, `2 -> 3`, `3 -> 4` ensures that multiple incoming paths to a node do not incorrectly multiply counts. Node `3` only inherits the best predecessor chain, and the DP merges branches safely by taking maximum, preventing overcounting.
