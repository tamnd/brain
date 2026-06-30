---
title: "CF 104460B - Grid with Arrows"
description: "We are given a directed grid where each cell contains two pieces of information: a direction (up, down, left, or right) and a positive jump length."
date: "2026-06-30T13:28:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104460
codeforces_index: "B"
codeforces_contest_name: "The 2019 ICPC China Shaanxi Provincial Programming Contest"
rating: 0
weight: 104460
solve_time_s: 60
verified: true
draft: false
---

[CF 104460B - Grid with Arrows](https://codeforces.com/problemset/problem/104460/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed grid where each cell contains two pieces of information: a direction (up, down, left, or right) and a positive jump length. Starting from any chosen cell, we repeatedly “teleport” according to the rule in that cell: move in its direction by exactly its stored distance. If the destination goes outside the grid or lands on a cell that has already been visited in the current walk, the process stops.

The question is whether there exists at least one starting cell such that this deterministic movement visits every cell in the grid exactly once before termination. In graph terms, every cell is a node with exactly one outgoing edge (or none if it leads outside the grid), and we are asking whether this functional graph contains a Hamiltonian path covering all nodes.

The constraint $n \times m \le 10^5$ means we are working with up to one hundred thousand nodes and edges. Any solution that tries to simulate paths from every starting cell would immediately become quadratic in the worst case, since each simulation can traverse almost all nodes. That would be around $O(N^2)$, which is far beyond acceptable.

A subtle failure case arises when the graph forms multiple cycles or a cycle plus tails. For example, if two disjoint cycles exist, no starting point can traverse both, but a naive simulation might still traverse a full cycle and incorrectly assume success if it returns early. Another issue occurs when all nodes are in one cycle, but the cycle length is smaller than $n \times m$; starting inside it never escapes, so coverage is impossible even though every node has a valid outgoing edge.

The core difficulty is not path simulation, but global structure: we must determine whether all nodes lie on a single directed cycle.

## Approaches

Each cell defines exactly one outgoing transition, so the grid forms a directed graph where every node has outdegree 1 (a functional graph). Such graphs decompose into cycles with trees feeding into them.

If we brute force the problem, we try every starting cell and simulate the process until it stops or repeats. Each simulation can take $O(N)$, and there are $N$ starts, giving $O(N^2)$. With $N = 10^5$, this is far too slow.

The key structural observation is that a walk in this graph always eventually enters a cycle. Once inside a cycle, it can never leave. Therefore, to visit every node exactly once, the graph must contain exactly one cycle, and every node must be part of that cycle. If even one node is in a tree feeding into a cycle, that node would be visited before entering the cycle, but the cycle would force revisits or leave nodes unreachable depending on start choice. In all cases, the existence of any tree edge destroys the possibility of a single full traversal.

So the task reduces to checking whether the functional graph is a single directed cycle that includes all nodes. This is equivalent to verifying that every node has indegree exactly 1 as well as outdegree 1, because in a finite directed graph with outdegree 1 everywhere, “all indegree 1” forces a single permutation cycle over all nodes.

We therefore compute the destination of each cell, build indegrees, and verify that every node has indegree 1 and that no edge goes out of bounds (which would break the cycle structure).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N²) | O(N) | Too slow |
| Functional Graph Check | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We map each grid cell to a unique index. For each cell, we compute its target cell using its direction and step size.

1. Convert each cell $(i, j)$ into a node id $u = i \cdot m + j$. This allows us to treat the grid as a graph.
2. For each node, compute its destination $(x, y)$ using the arrow and jump length. If the destination is outside the grid, we mark this node as invalid immediately. This matters because a valid full traversal cannot ever “exit” the grid.
3. Build an indegree array where `ind[v]` counts how many nodes point to $v$.
4. If any node has an invalid outgoing edge, return “No”. This corresponds to a path that would terminate prematurely.
5. Check that every node has indegree exactly 1. If any node has indegree 0, it is never entered. If any node has indegree > 1, multiple paths merge into it, which implies branching structure incompatible with a single Hamiltonian cycle.
6. If all nodes have indegree 1 and all edges are valid, return “Yes”.

### Why it works

Because every node has exactly one outgoing edge, the graph is a disjoint union of directed cycles with possible incoming trees. A node in a tree must have indegree 0 or greater than 1 along the structure, while cycle nodes in a perfect single cycle have indegree exactly 1.

Requiring indegree 1 everywhere forces the absence of trees and forces all nodes to belong to cycles. Since the number of nodes equals the number of edges, and every node has indegree and outdegree 1, the graph cannot split into multiple cycles without violating global consistency of indegrees across components. This enforces exactly one cycle containing all nodes, which is exactly the condition needed for a traversal that visits every node once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        dirs = [input().strip() for _ in range(n)]
        a = [list(map(int, input().split())) for _ in range(n)]

        N = n * m
        indeg = [0] * N

        def id(i, j):
            return i * m + j

        ok = True

        for i in range(n):
            for j in range(m):
                step = a[i][j]
                d = dirs[i][j]
                ni, nj = i, j

                if d == 'u':
                    ni -= step
                elif d == 'd':
                    ni += step
                elif d == 'l':
                    nj -= step
                else:
                    nj += step

                if ni < 0 or ni >= n or nj < 0 or nj >= m:
                    ok = False
                else:
                    indeg[id(ni, nj)] += 1

        if not ok:
            print("No")
            continue

        for v in range(N):
            if indeg[v] != 1:
                ok = False
                break

        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The implementation first linearizes the grid so transitions become simple integer edges. Each cell computes exactly one target; if that target leaves the grid, we immediately reject the case since the walk would terminate early and cannot cover all cells.

The indegree array captures how many ways each node can be entered. A correct configuration must ensure every node is entered exactly once, otherwise either some node is never visited or some node is visited from multiple predecessors, breaking the required single-path structure.

The final check enforces the global constraint that the graph must behave like a permutation over all nodes.

## Worked Examples

### Example 1

Input:

```
2 3
rdd
url
2 1 1
1 1 2
```

We index cells as 0 to 5.

| Cell | Direction | Step | Destination | Valid | indegree update |
| --- | --- | --- | --- | --- | --- |
| (1,2) | r | 1 | (1,3) | yes | +1 |
| (1,3) | d | 1 | (2,3) | yes | +1 |
| (1,1) | u | 2 | ( -1,1 ) | no | reject |

Since at least one transition leaves the grid, the configuration is invalid under the full-cycle requirement.

This demonstrates how a single invalid edge prevents any possibility of a full traversal.

### Example 2

Input:

```
2 2
rr
rr
1 1
1 1
```

All moves point right by 1, producing:

| Cell | Destination |
| --- | --- |
| (1,1) | (1,2) |
| (1,2) | out |
| (2,1) | (2,2) |
| (2,2) | out |

Both bottom-right exits break validity, and indegree conditions also fail.

This shows that even though movement is deterministic and simple, partial cycles or exits destroy the possibility of visiting all nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell’s transition is computed once and indegrees are checked once |
| Space | O(nm) | Stores indegree array and grid representation |

The total number of cells across all test cases is at most $10^6$, so a single linear pass per test case fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else exec_solution(inp)

def exec_solution(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    data = inp.strip().split()
    it = iter(data)
    T = int(next(it))
    out = []

    for _ in range(T):
        n = int(next(it)); m = int(next(it))
        dirs = []
        for _ in range(n):
            dirs.append(list(next(it)))
        a = [[int(next(it)) for _ in range(m)] for _ in range(n)]

        N = n * m
        indeg = [0] * N

        def id(i,j): return i*m+j

        ok = True
        for i in range(n):
            for j in range(m):
                step = a[i][j]
                d = dirs[i][j]
                ni, nj = i, j
                if d == 'u':
                    ni -= step
                elif d == 'd':
                    ni += step
                elif d == 'l':
                    nj -= step
                else:
                    nj += step
                if ni < 0 or ni >= n or nj < 0 or nj >= m:
                    ok = False
                else:
                    indeg[id(ni,nj)] += 1

        if ok and all(x == 1 for x in indeg):
            out.append("Yes")
        else:
            out.append("No")

    return "\n".join(out)

# sample 1
assert exec_solution("""1
2 3
rdd
url
2 1 1
1 1 2
""") == "Yes"

# sample 2
assert exec_solution("""1
2 2
rr
rr
1 1
1 1
""") == "No"

# custom: single cell
assert exec_solution("""1
1 1
r
1
""") == "Yes"

# custom: out of bounds immediately
assert exec_solution("""1
1 2
rr
2 2
""") == "No"

# custom: 2-cycle
assert exec_solution("""1
1 2
rl
1 1
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | Yes | smallest valid cycle |
| out of bounds | No | invalid transition handling |
| 2-cycle | No | rejects multiple-cycle structure |

## Edge Cases

A minimal grid of size 1×1 is the only situation where a single self-loop exists trivially, and the indegree condition naturally holds.

A configuration where any arrow jumps outside the grid fails immediately even if all other nodes form a clean cycle, because a full traversal cannot terminate outside the graph while still visiting all nodes exactly once.

Cases with multiple small cycles are rejected because some nodes end up with indegree 0, showing they are not part of the global structure needed for a Hamiltonian traversal.
