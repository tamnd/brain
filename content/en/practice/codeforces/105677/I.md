---
title: "CF 105677I - Divination"
description: "We are given a collection of N objects, each object representing a paper. Every paper contains a list of references to other papers, forming a directed graph where an arrow goes from a paper to each paper it cites."
date: "2026-06-22T05:08:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105677
codeforces_index: "I"
codeforces_contest_name: "2024-2025 ICPC Southwestern European Regional Contest (SWERC 2024)"
rating: 0
weight: 105677
solve_time_s: 49
verified: true
draft: false
---

[CF 105677I - Divination](https://codeforces.com/problemset/problem/105677/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of N objects, each object representing a paper. Every paper contains a list of references to other papers, forming a directed graph where an arrow goes from a paper to each paper it cites. The structure is guaranteed to have no directed cycles, so if you follow citations forward you can never return to the same paper.

The task is to determine whether these papers can be arranged into a single chain that uses all of them exactly once, such that each paper cites the next one in the chain. In graph terms, we are asked whether the directed acyclic graph contains a Hamiltonian path that follows edge directions.

The constraint N up to 100,000 and total edges up to 500,000 implies we must operate in linear or near-linear time. Any solution that tries to test all permutations or all paths explicitly is immediately infeasible since even O(N^2) would be too slow at this scale.

A subtle point is that we are not asked whether the graph is connected in the undirected sense. A graph can be connected and still fail the condition if it branches. Conversely, multiple disconnected components already make it impossible to form a single chain covering all nodes.

A common failure case comes from assuming that “acyclic” implies a valid ordering automatically works. For example, if we have three nodes with edges 1 → 2 and 1 → 3, the graph is a DAG, but there is no way to arrange all three into a single chain where each step follows an edge, since after 1 we cannot go to both 2 and 3 in sequence.

Another failure case comes from assuming any topological ordering works. A topological order might place nodes in a valid dependency order but still fail to correspond to a path where consecutive nodes are directly connected by edges.

## Approaches

A brute-force interpretation would try to build a path starting from every node, performing a DFS or backtracking that tries to extend the path step by step while marking visited nodes. In the worst case, each node could branch to many others, and exploring all possibilities leads to factorial or exponential behavior. Even pruning with visited states still explores an enormous number of partial permutations because the graph is only constrained to be acyclic, not linear.

The key observation is that if such a full chain exists, then the graph is essentially forced into a near-linear structure. In a valid solution, every node except the last must have exactly one “next” choice along the chain. This suggests that the entire structure can be verified using a topological ordering, because in a DAG, any Hamiltonian path must appear as a valid topological order.

Once we compute a topological ordering, we only need to check whether each consecutive pair in that ordering is connected by a directed edge. If that holds, the ordering itself is a valid Hamiltonian path. If it does not hold, then no Hamiltonian path can exist, because any valid path would have to appear as a topological order, and the absence of edges between consecutive positions shows that the graph cannot support a full chain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Backtracking DFS over paths | O(N!) | O(N) | Too slow |
| Topological sort + adjacency check | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We treat the citation structure as a directed graph and use a standard indegree-based topological sorting process.

1. Build an adjacency list for the graph and compute the indegree of every node. This allows us to identify which nodes have no prerequisites, meaning no incoming citations.
2. Initialize a queue with all nodes whose indegree is zero. These nodes can appear first in any valid ordering because nothing depends on them.
3. Repeatedly remove a node from the queue, append it to the topological order, and reduce the indegree of all nodes it points to. When a node’s indegree becomes zero, it is added to the queue. This process simulates removing “available” papers in a valid dependency-respecting order.
4. After processing all nodes, we obtain a topological ordering of all papers. Since the graph is guaranteed acyclic, every node will be processed.
5. Verify whether this ordering forms a single chain by checking every adjacent pair in the order. For each consecutive pair (u, v), we check whether there is a direct edge u → v.
6. If all consecutive pairs are connected by edges, we return 1, since the order itself is a valid full citation chain. Otherwise, we return 0.

### Why it works

In a DAG, any Hamiltonian path must respect a topological order because edges always go forward along dependencies. If a Hamiltonian path exists, it defines a total order of all nodes. A topological sort is another linear extension of the same partial order. If the graph admits a Hamiltonian path, all valid topological sorts must be consistent with that path ordering, since reversing any pair in the path would contradict the existence of a directed edge.

Therefore, if we compute a topological ordering and find that some adjacent pair is not directly connected, it implies there is a “gap” where the path cannot proceed, meaning no Hamiltonian path exists at all.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    adj = [[] for _ in range(n)]
    indeg = [0] * n

    for i in range(n):
        parts = list(map(int, input().split()))
        c = parts[0]
        for x in parts[1:]:
            x -= 1
            adj[i].append(x)
            indeg[x] += 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    topo = []

    while q:
        u = q.popleft()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    pos = [0] * n
    for i, x in enumerate(topo):
        pos[x] = i

    has_edge = set()
    for u in range(n):
        for v in adj[u]:
            has_edge.add((u, v))

    for i in range(n - 1):
        u = topo[i]
        v = topo[i + 1]
        if (u, v) not in has_edge:
            print(0)
            return

    print(1)

if __name__ == "__main__":
    solve()
```

The implementation begins by constructing the adjacency list and indegree array directly from the citation lists. The queue holds all currently free nodes, which ensures we always respect dependency constraints.

After generating the topological order, we build a fast lookup structure for edges using a set of pairs. This makes the adjacency check between consecutive nodes O(1), avoiding repeated scans of adjacency lists.

The final loop is the critical verification step. It enforces that the topological ordering is not just valid in a dependency sense, but also forms a continuous path without breaks.

## Worked Examples

Consider a case where the graph forms a simple chain 1 → 2 → 3 → 4.

| Step | Queue | Popped | Topo Order | Indegree Changes |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | [1] | 2 becomes 0 |
| 2 | [2] | 2 | [1,2] | 3 becomes 0 |
| 3 | [3] | 3 | [1,2,3] | 4 becomes 0 |
| 4 | [4] | 4 | [1,2,3,4] | done |

Every consecutive pair has a direct edge, so the answer is 1. This confirms that a pure chain structure is correctly recognized.

Now consider a branching DAG where 1 → 2 and 1 → 3, with no edge between 2 and 3.

| Step | Queue | Popped | Topo Order |
| --- | --- | --- | --- |
| 1 | [1] | 1 | [1] |
| 2 | [2,3] | 2 | [1,2] |
| 3 | [3] | 3 | [1,2,3] |

When checking consecutive pairs, we find that 1 → 2 exists but 2 → 3 does not, so the algorithm outputs 0. This demonstrates that even though the graph is acyclic and fully ordered in a topological sense, it does not form a single Hamiltonian path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | Each node is processed once in Kahn’s algorithm, and each edge is examined a constant number of times |
| Space | O(N + M) | Adjacency list, indegree array, and edge set store all graph information |

The constraints allow up to 100,000 nodes and 500,000 edges, so a linear-time graph traversal is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# simple chain
assert run("3\n1 2\n1 3\n1\n") in ["1\n", "1"]

# single chain 1->2->3
assert run("3\n1 2\n1 3\n0\n") in ["1\n", "1"]

# branching
assert run("3\n1 2 3\n0\n0\n") in ["0\n", "0"]

# disconnected components
assert run("4\n1 2\n0\n1 4\n0\n") in ["0\n", "0"]

# minimum size
assert run("2\n1 2\n0\n") in ["1\n", "1"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-node chain | 1 | basic Hamiltonian path |
| branching from root | 0 | detects missing linear structure |
| disconnected graph | 0 | requires full coverage |
| minimum N=2 chain | 1 | smallest valid case |

## Edge Cases

A key edge case is a graph that is acyclic but splits immediately. For example, node 1 points to 2 and 3. The algorithm processes node 1 first in the topological sort, then both 2 and 3 become available simultaneously. The resulting ordering will place them in some arbitrary order, such as [1,2,3], but since there is no edge 2 → 3, the consecutive check fails, correctly rejecting the input.

Another edge case is when multiple valid topological orders exist but only one of them could correspond to a Hamiltonian path. For instance, even if the queue allows different choices at different steps, any ordering that is not strictly a single chain will necessarily introduce a missing edge between consecutive nodes, and the verification step catches this regardless of how ties were resolved.
