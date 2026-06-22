---
title: "CF 105575I - \u5fc3\u610f\u65e0\u5411\uff0c\u524d\u7a0b\u6709\u5411"
description: "We are given a graph structure with directed constraints and undirected relationships over the same set of vertices."
date: "2026-06-22T17:43:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "I"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 57
verified: true
draft: false
---

[CF 105575I - \u5fc3\u610f\u65e0\u5411\uff0c\u524d\u7a0b\u6709\u5411](https://codeforces.com/problemset/problem/105575/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph structure with directed constraints and undirected relationships over the same set of vertices. The directed edges represent strict ordering rules that cannot be violated, while the undirected edges are flexible and must be assigned a direction in the final result.

The task is to decide whether it is possible to orient all undirected edges so that the entire graph becomes acyclic, while preserving the given directed edges. If it is possible, we must output a consistent orientation for every undirected edge; otherwise we output that no valid construction exists.

The key difficulty is that directed edges already impose partial order constraints. If those constraints contain a cycle, no assignment of directions to undirected edges can fix the contradiction, because directed edges are immutable. If the directed part is acyclic, then the undirected edges can always be oriented consistently with a global ordering derived from that acyclic structure.

The constraints imply a graph with up to 200000 vertices and edges. This forces any solution to run in linear or near-linear time. Any quadratic behavior over edges or vertices would fail immediately. This rules out approaches that try to test consistency by repeatedly simulating edge orientations or attempting backtracking assignments.

A subtle failure case appears when directed edges form a cycle even though undirected edges exist that might seem capable of “breaking” it intuitively. For example, if 1 → 2, 2 → 3, 3 → 1 are all directed edges, the answer is immediately impossible, even if there are many undirected edges. A naive approach that tries to orient undirected edges first might incorrectly believe it can avoid the cycle, but directed cycles are already fatal.

Another edge case is when there are no directed edges at all. In that case, any ordering of vertices works, so we can always produce a valid orientation for undirected edges.

## Approaches

A brute-force idea is to treat every undirected edge as a binary choice and try all possible orientations. After assigning directions, we would check whether the resulting directed graph is acyclic using a topological sort or DFS cycle detection. Since there can be up to O(m2) undirected edges in worst cases, this approach explodes into 2^m configurations, and even a single validity check costs O(n + m), making it completely infeasible.

The key observation is that directed edges define a partial order. If this partial order is consistent, meaning it has no cycle, then it can be extended into a full linear order of all vertices. Once we have such a linear order, every undirected edge can simply be oriented from earlier to later in that order. This automatically guarantees that no cycle is introduced, because every edge respects a single global ordering.

So the entire problem reduces to checking whether the directed subgraph is a DAG and, if so, constructing a topological ordering. Once that ordering exists, all undirected edges become trivial to orient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m · (n + m)) | O(n + m) | Too slow |
| Optimal (Topological Sort) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build a directed graph using only the directed edges. Compute indegrees for all vertices. This isolates the constraints that are mandatory and must be satisfied regardless of how undirected edges are handled.
2. Run a standard Kahn’s algorithm for topological sorting using a queue. Start with all vertices whose indegree is zero. These vertices have no prerequisites and can appear earliest in any valid ordering.
3. Repeatedly remove a vertex from the queue, assign it the next position in a global ordering, and decrease indegrees of its neighbors. Whenever a neighbor’s indegree becomes zero, push it into the queue.
4. If at the end fewer than n vertices are processed, a cycle exists in the directed graph. In this case, no valid orientation can exist because the directed constraints are inherently contradictory.
5. If a full ordering is obtained, use it to assign directions for all undirected edges. For each undirected edge (u, v), compare their positions in the topological order and direct the edge from the earlier vertex to the later vertex.

### Why it works

The topological order defines a strict total ordering consistent with all directed edges. Every directed edge u → v guarantees that u appears before v in this order. Any edge oriented according to this ordering can never create a directed cycle, because following edges always strictly increases position in the order. Since every undirected edge is forced to follow this monotonic rule, the final graph inherits acyclicity directly from the linear order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m1, m2 = map(int, input().split())

    undirected = []
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)

    # undirected edges
    for _ in range(m1):
        u, v = map(int, input().split())
        undirected.append((u, v))

    # directed edges
    for _ in range(m2):
        u, v = map(int, input().split())
        adj[u].append(v)
        indeg[v] += 1

    from collections import deque
    q = deque([i for i in range(1, n + 1) if indeg[i] == 0])

    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(topo) != n:
        print(-1)
        return

    pos = [0] * (n + 1)
    for i, v in enumerate(topo):
        pos[v] = i

    for u, v in undirected:
        if pos[u] < pos[v]:
            print(u, v)
        else:
            print(v, u)

t = 1
for _ in range(t):
    solve()
```

The solution separates undirected and directed edges immediately, since only the directed ones influence feasibility. The adjacency list and indegree array are used purely for Kahn’s algorithm. The queue initially contains all vertices with no incoming directed edges, ensuring we always extend a valid partial order.

The critical step is verifying whether the topological sort covers all vertices. If not, the directed constraints already contradict themselves, so no further processing is meaningful.

Once the ordering is computed, we map each vertex to its position. This allows constant-time comparison for every undirected edge. Each undirected edge is oriented strictly according to this global order, guaranteeing consistency.

## Worked Examples

Consider a case with a small directed structure:

Input:

n = 4

directed edges: 1 → 2, 2 → 3

undirected edges: (1, 3), (4, 2)

Topological process:

| Step | Queue | Popped | topo | indegree changes |
| --- | --- | --- | --- | --- |
| 1 | [1,4] | 1 | [1] | 2→0 |
| 2 | [4,2] | 4 | [1,4] | none |
| 3 | [2] | 2 | [1,4,2] | 3→0 |
| 4 | [3] | 3 | [1,4,2,3] | done |

Final order is [1,4,2,3]. Now orient undirected edges:

Edge (1,3): 1 before 3, becomes 1 → 3

Edge (4,2): 4 before 2, becomes 4 → 2

This demonstrates that once a topological order exists, all undirected edges become consistent with it.

Now consider a failure case:

Input:

n = 3

directed edges: 1 → 2, 2 → 3, 3 → 1

undirected edges: none

The queue becomes empty immediately or finishes with fewer than 3 nodes processed. The algorithm detects that not all nodes are included in topo, so output is -1. This shows that directed cycles cannot be repaired.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m1 + m2) | Each vertex enters and leaves the queue once, each edge is processed once |
| Space | O(n + m1 + m2) | adjacency list, indegree array, and ordering storage |

The constraints allow up to 200000 elements, so linear complexity is sufficient. The algorithm processes each edge a constant number of times, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# Since full IO solver is embedded above, these are conceptual placeholders
# In a real setup, solve() would be imported and called directly

# sample-style cycle case
# assert run("3 0 3\n1 2\n2 3\n3 1\n") == "-1"

# minimal acyclic
# assert run("2 1 0\n1 2\n") in ["1 2\n"]

# mixed case
# assert run("4 2 2\n1 3\n2 4\n1 2\n3 4\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 nodes directed cycle | -1 | cycle detection correctness |
| 2 nodes single edge | valid orientation | base correctness |
| mixed graph | consistent orientation | integration of topo + undirected handling |

## Edge Cases

A key edge case is when there are no directed edges at all. In that situation, every vertex initially has indegree zero, so the queue starts with all nodes. Any topological ordering is valid, and the algorithm produces a full permutation immediately. All undirected edges are then oriented arbitrarily according to that permutation, which is always valid.

Another edge case is when directed edges form a chain plus isolated nodes. The topological order will place isolated nodes at arbitrary positions relative to the chain, but this does not affect correctness because isolated nodes impose no constraints.

A failure edge case is a directed cycle hidden among many nodes. For example, if only three nodes form a cycle inside a larger graph, Kahn’s algorithm will stall early. The final topo length check detects this without needing to explicitly search for cycles.
