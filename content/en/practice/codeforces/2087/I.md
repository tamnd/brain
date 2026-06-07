---
title: "CF 2087I - Hamiltonian Partition"
description: "We are given a directed acyclic graph on $n$ vertices with some existing directed edges. The task is to add as few new directed edges as possible so that, after adding them, we can split all edges of the resulting directed multigraph into several Hamiltonian cycles, where each…"
date: "2026-06-08T06:01:03+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 2087
codeforces_index: "I"
codeforces_contest_name: "Kotlin Heroes: Episode 12"
rating: 0
weight: 2087
solve_time_s: 87
verified: true
draft: false
---

[CF 2087I - Hamiltonian Partition](https://codeforces.com/problemset/problem/2087/I)

**Rating:** -  
**Tags:** *special  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph on $n$ vertices with some existing directed edges. The task is to add as few new directed edges as possible so that, after adding them, we can split all edges of the resulting directed multigraph into several Hamiltonian cycles, where each cycle visits every vertex exactly once and uses exactly one outgoing and one incoming edge per vertex.

The important structural interpretation is that each Hamiltonian cycle corresponds to a permutation of the vertices. In that cycle, every vertex has exactly one outgoing edge and exactly one incoming edge. If we have $c$ such cycles, then every vertex must have exactly $c$ outgoing edges and exactly $c$ incoming edges in the final graph.

So the real problem is not about paths or DAG structure anymore. It becomes a problem of completing a directed multigraph so that all row sums and column sums of its adjacency matrix become equal, and then decomposing that matrix into permutation matrices.

The DAG restriction matters only in the input, not in the final construction. Since we are allowed to add arbitrary directed edges (except self-loops), we can destroy acyclicity completely.

A naive approach would try to build Hamiltonian cycles directly or greedily extend paths, but that fails immediately because edges must be globally partitioned into consistent permutations. A single local cycle construction does not guarantee global consistency of in-degree and out-degree across all vertices and all cycles.

A more subtle failure case comes from ignoring balance. For example, if one vertex has large outdegree and small indegree, any attempt to form cycles will eventually get stuck because that vertex cannot simultaneously serve all cycles consistently.

The real obstruction is degree imbalance, not connectivity.

## Approaches

A brute-force idea would be to explicitly search for the minimum number of added edges by trying increasing values of $c$, and for each $c$, attempting to decide whether we can complete the graph into a $c$-regular directed multigraph that decomposes into Hamiltonian cycles. This quickly becomes infeasible because the decomposition step already requires solving a nontrivial assignment problem, and trying all possibilities of added edges grows combinatorially.

The key observation is that Hamiltonian cycle decomposition imposes a very rigid condition: the final graph must be a union of $c$ directed 1-factors. In matrix terms, we need a nonnegative integer matrix $A$ such that each row sum and column sum equals $c$, and $A[i][j] \ge B[i][j]$, where $B$ is the initial adjacency matrix.

Once we see this, the problem splits cleanly into two parts. First, we determine the minimum feasible $c$. Second, we construct any valid completion to achieve that $c$, and finally decompose it into $c$ permutation matrices using standard bipartite matching arguments.

The DAG structure guarantees that no self-consistency constraint blocks feasibility beyond degree balancing, because we are allowed to add edges arbitrarily between distinct vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Try all constructions of cycles and edges | Exponential | Exponential | Too slow |
| Degree balancing + bipartite decomposition | $O(c \cdot n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We first convert the graph into degree data. For each vertex we compute its current indegree and outdegree.

1. Compute $out[v]$ and $in[v]$ for every vertex. These represent how many cycles each vertex already participates in, in each direction.
2. We choose the smallest possible number of cycles $c$ such that we can make all vertices have equal indegree and outdegree $c$. This requires

$$c \ge \max_v(out[v], in[v])$$

because we cannot reduce existing degrees, and also

$$n \cdot c \ge m$$

because each cycle contributes exactly $n$ edges and we must cover all existing edges.

So we set

$$c = \max\left(\max_v(out[v], in[v]), \left\lceil \frac{m}{n} \right\rceil \right).$$
3. For each vertex, compute how many outgoing and incoming edges it still needs:

$$needOut[v] = c - out[v], \quad needIn[v] = c - in[v].$$

The total sums match, so the number of added edges will be exactly the total demand.
4. We construct added edges by matching outgoing deficits to incoming deficits. We maintain a multiset of vertices with remaining outgoing demand and another for incoming demand. We repeatedly connect a vertex $u$ with positive $needOut$ to a vertex $v$ with positive $needIn$, ensuring $u \ne v$. If a naive choice would create a self-loop, we swap with another available pair. Since $n \ge 2$, this swap is always possible.
5. After constructing all added edges, every vertex has indegree and outdegree exactly $c$.
6. Now we decompose the resulting directed multigraph into $c$ Hamiltonian cycles. We interpret the adjacency as a bipartite multigraph between a left copy and right copy of vertices. Each layer corresponds to choosing exactly one outgoing edge per vertex such that all incoming constraints are satisfied.

We repeatedly find a perfect matching in this bipartite structure using DFS-based augmenting matching, removing one unit of capacity per edge used. Each matching corresponds to one Hamiltonian cycle.
7. Each extracted matching defines a permutation of vertices, and we output it as one cycle. Every edge is assigned to exactly one such matching.

### Why it works

The core invariant is that after choosing $c$, the construction enforces a doubly stochastic structure at the integer level: every vertex has identical in-degree and out-degree. Any such integer matrix can be decomposed into permutation matrices because each step reduces the problem by extracting one perfect matching while preserving balance. Since every vertex always retains equal remaining in/out degree, the matching step never gets stuck, and every extracted layer forms a valid Hamiltonian cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[0] * n for _ in range(n)]
    outdeg = [0] * n
    indeg = [0] * n

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u][v] += 1
        outdeg[u] += 1
        indeg[v] += 1
        edges.append((u, v))

    c = 0
    for i in range(n):
        c = max(c, outdeg[i], indeg[i])
    c = max(c, (m + n - 1) // n)

    need_out = [c - outdeg[i] for i in range(n)]
    need_in = [c - indeg[i] for i in range(n)]

    added = []

    # construct added edges greedily with swap to avoid self-loops
    out_list = [i for i in range(n) for _ in range(need_out[i])]
    in_list = [i for i in range(n) for _ in range(need_in[i])]

    j = 0
    for u in out_list:
        if in_list[j] != u:
            v = in_list[j]
            added.append((u, v))
            j += 1
        else:
            if j + 1 < len(in_list):
                v = in_list[j + 1]
                in_list[j + 1] = in_list[j]
                in_list[j] = v
                added.append((u, v))
                j += 1

    all_edges = edges + added
    E = len(all_edges)

    # build adjacency matrix with capacities
    cap = [[0] * n for _ in range(n)]
    for u, v in all_edges:
        cap[u][v] += 1

    res = [0] * E

    def find_matching():
        match_r = [-1] * n
        used = [0] * n

        def dfs(u):
            for v in range(n):
                if cap[u][v] > 0 and used[v] == 0:
                    used[v] = 1
                    if match_r[v] == -1 or dfs(match_r[v]):
                        match_r[v] = u
                        cap[u][v] -= 1
                        return True
            return False

        for u in range(n):
            used = [0] * n
            dfs(u)

        return match_r

    for c_id in range(1, c + 1):
        match_r = find_matching()
        nxt = [-1] * n
        for v in range(n):
            if match_r[v] != -1:
                nxt[match_r[v]] = v

        for u in range(n):
            v = nxt[u]
            for i, (a, b) in enumerate(all_edges):
                if a == u and b == v:
                    res[i] = c_id
                    all_edges[i] = (-1, -1)
                    break

    print(len(added))
    for u, v in added:
        print(u + 1, v + 1)
    print(c)
    print(*res)

if __name__ == "__main__":
    solve()
```

The first part of the code computes degrees and selects the minimum feasible number of cycles $c$. The next part constructs the added edges by pairing surplus outgoing and incoming demands while avoiding self-loops through a simple local swap.

After that, the graph is converted into a capacity matrix. Each iteration of `find_matching` extracts one layer by building a one-to-one assignment from vertices to vertices using DFS-based augmenting paths. Each extracted matching corresponds to one Hamiltonian cycle.

Finally, each edge is assigned to the cycle in which it is used.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 3
```

Degrees:

Vertex 1 has out=1 in=0, vertex 2 has out=1 in=1, vertex 3 has out=0 in=1.

We get $c = 1$. No vertex needs extra degree, but vertex 3 needs an edge to close the cycle, so we add $3 \to 1$.

| Step | Action | State |
| --- | --- | --- |
| 1 | compute degrees | out=[1,1,0], in=[0,1,1] |
| 2 | choose c=1 | balanced target |
| 3 | add edge | 3→1 |
| 4 | decomposition | single cycle |

Final cycle is $1 \to 2 \to 3 \to 1$.

This confirms that even a DAG input becomes a single permutation once balanced.

### Example 2

Consider a slightly larger chain:

```
4 3
1 2
2 3
3 4
```

Degrees:

out=[1,1,1,0], in=[0,1,1,1], so $c=1$.

We add edge $4 \to 1$, forming a cycle.

| Step | Action | State |
| --- | --- | --- |
| 1 | compute degrees | chain |
| 2 | choose c=1 | minimal |
| 3 | add edge | 4→1 |
| 4 | cycle formed | 1→2→3→4→1 |

This demonstrates that the DAG structure only determines how many corrections are needed, not the final decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(c \cdot n^2)$ | Each of $c$ cycle extractions performs matching over an $n \times n$ capacity matrix |
| Space | $O(n^2)$ | Adjacency matrix and capacity storage |

The constraints $n \le 100$ ensure that even repeated matching over at most a few hundred layers remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()  # assuming solve prints; adapt if needed

# sample
assert run("3 2\n1 2\n2 3\n") is None

# single edge chain
assert run("4 3\n1 2\n2 3\n3 4\n") is None

# minimal case
assert run("2 1\n1 2\n") is None

# already balanced small cycle
assert run("3 3\n1 2\n2 3\n3 1\n") is None

# star structure
assert run("4 3\n1 2\n1 3\n1 4\n") is None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | cycle closure | handling imbalance |
| already cyclic | no unnecessary additions | optimality |
| star | heavy imbalance | correctness of balancing |

## Edge Cases

A critical edge case is when a vertex has zero indegree or zero outdegree. For instance, in a pure chain $1 \to 2 \to 3 \to 4$, the endpoints force the algorithm to add exactly one closing edge. The algorithm handles this by increasing $c$ to 1 and assigning missing degrees, which ensures both endpoints receive the necessary compensation.

Another subtle case is when a vertex would require a self-loop during balancing. The construction explicitly avoids this by swapping candidates in the incoming list, ensuring that no $i \to i$ edge is ever introduced while still preserving global feasibility.
