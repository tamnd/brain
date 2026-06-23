---
title: "CF 105383K - Kingdom's Development Plan"
description: "We are given a set of projects, each labeled from 1 to n, together with a list of dependency rules of the form “project a must be finished before project b can start."
date: "2026-06-23T16:12:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105383
codeforces_index: "K"
codeforces_contest_name: "2024 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 105383
solve_time_s: 54
verified: true
draft: false
---

[CF 105383K - Kingdom's Development Plan](https://codeforces.com/problemset/problem/105383/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of projects, each labeled from 1 to n, together with a list of dependency rules of the form “project a must be finished before project b can start.” These rules define a directed relationship between projects, and the task is to decide whether all projects can be completed in some order that respects every dependency. If such an order exists, we must output one valid ordering of all projects. If multiple valid orders exist, we are required to choose the lexicographically smallest one.

From a graph perspective, each project is a node and each dependency a directed edge from a to b. The output is therefore a topological ordering of a directed graph, with the additional constraint that among all valid topological orders, we must pick the smallest in lexicographic order.

The constraints go up to n = 100000 and m = 200000. Any solution that is quadratic in n, such as repeatedly scanning all nodes to find the next valid project, will not work. We are restricted to essentially linear or near linear time, meaning O(n log n) or O(n + m) is the target range. This already strongly suggests a graph traversal method rather than any combinational search.

A few edge cases matter here. First, if there is a cycle, for example 1 depends on 2, 2 depends on 3, and 3 depends on 1, then no ordering is possible and we must output IMPOSSIBLE. Second, when multiple valid next projects exist, the lexicographically smallest requirement forces us to always prefer the smallest indexed project available at each step, otherwise a greedy but unordered topological sort would produce a valid but not minimal sequence. Third, when there are no dependencies at all, the answer must simply be 1 2 3 ... n.

## Approaches

The naive approach is to repeatedly scan all projects and pick any project whose prerequisites are satisfied. At each step, we would check all edges or recompute indegrees from scratch to determine which nodes are currently available. This works conceptually because we are always respecting dependencies, but each selection step may cost O(n + m) in a straightforward implementation. Since we do this n times, the worst case becomes O(n(n + m)), which is far too large for the input limits.

The key observation is that we never need to recompute dependency satisfaction from scratch. What we actually need is a dynamic set of all currently available projects, meaning those whose indegree is zero. Once a project is taken, only its outgoing neighbors are affected. This naturally suggests maintaining indegrees and updating them incrementally.

To enforce lexicographically smallest ordering, we must always choose the smallest available project at each step. This turns the problem into a standard topological sorting task with a priority mechanism. Instead of an arbitrary queue, we use a min heap so that we always extract the smallest indexed node with indegree zero.

Each time we remove a node from the heap, we simulate completing that project and decrement the indegree of its neighbors. Any neighbor whose indegree becomes zero is added to the heap. This guarantees we always maintain the correct frontier of available nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n + m)) | O(n + m) | Too slow |
| Optimal (min-heap topological sort) | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We convert the problem into a directed graph and track indegrees.

1. Build an adjacency list for the graph and compute indegree for every node. This tells us how many prerequisites each project still has.
2. Initialize a min heap and push all nodes whose indegree is zero. These are projects that can be started immediately because they depend on nothing.
3. Repeatedly extract the smallest node from the heap. This choice ensures lexicographic minimality at every step among all currently valid candidates.
4. Append the extracted node to the answer sequence, since we are now committing to completing that project at this position.
5. For every neighbor of this node, decrement its indegree. This represents satisfying one prerequisite for those dependent projects.
6. If any neighbor’s indegree becomes zero, push it into the heap, because it has become eligible for execution.
7. Continue until the heap becomes empty. At that point, either all nodes have been processed or a cycle exists.
8. Finally, check whether the resulting ordering contains all n nodes. If not, some nodes were never freed from dependencies, meaning a cycle exists, so output IMPOSSIBLE.

The crucial detail is that the heap always reflects exactly the set of nodes that are currently valid to take, and we always choose the smallest among them.

### Why it works

At every step, the algorithm maintains the invariant that all nodes already output have indegree zero with respect to the remaining graph, and all nodes currently in the heap are exactly those nodes whose prerequisites have all been satisfied. Because edges are only removed implicitly through indegree updates, no node is ever inserted into the ordering before all its dependencies appear earlier in the sequence. The heap ordering ensures that among all valid next choices, the smallest index is chosen, so no lexicographically smaller valid sequence can exist that diverges earlier from the constructed one.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        indeg[b] += 1

    heap = []
    for i in range(1, n + 1):
        if indeg[i] == 0:
            heapq.heappush(heap, i)

    order = []

    while heap:
        u = heapq.heappop(heap)
        order.append(u)

        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    if len(order) != n:
        print("IMPOSSIBLE")
    else:
        print(*order)

if __name__ == "__main__":
    solve()
```

The implementation begins by constructing the adjacency list and computing indegrees, which is the structural representation of all prerequisite constraints. The heap is then seeded with all zero-indegree nodes, which form the initial valid set of starting projects.

The main loop repeatedly pops the smallest available node. Using a heap instead of a queue is what enforces lexicographic minimality; replacing it with a normal queue would still produce a valid topological order but not necessarily the smallest one.

Each time we remove a node, we propagate its effect through outgoing edges by decrementing indegrees. A neighbor is only pushed when its indegree becomes exactly zero, ensuring it becomes eligible exactly when all prerequisites are satisfied.

The final check compares the constructed order size with n. If they differ, at least one node was never reachable through indegree reduction, which can only happen in the presence of a cycle.

## Worked Examples

### Example 1

Input:

```
5 5
1 2
2 3
2 4
2 5
3 4
```

Initial indegrees:

| Step | Heap | Chosen | Order | Indegree changes |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | [1] | 2 becomes 0 |
| 2 | [2] | 2 | [1,2] | 3,4,5 updated |
| 3 | [3,4,5] | 3 | [1,2,3] | 4 updated |
| 4 | [4,5] | 4 | [1,2,3,4] | none |
| 5 | [5] | 5 | [1,2,3,4,5] | done |

The heap ensures that when multiple nodes become available, the smallest index is always selected first, producing the lexicographically smallest valid order.

### Example 2

Input:

```
5 4
1 2
2 3
3 1
5 4
```

| Step | Heap | Chosen | Order |
| --- | --- | --- | --- |
| start | [4,5] | - | [] |
| 1 | [4,5] | 4 | [4] |
| 2 | [5] | 5 | [4,5] |
| stop | [] | - | [4,5] |

Nodes 1, 2, 3 never enter the heap because their cycle keeps their indegrees non-zero forever. Only nodes in the acyclic component are processed, and the final length is less than n, triggering IMPOSSIBLE.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each node enters and leaves the heap at most once, and each edge causes one indegree update |
| Space | O(n + m) | adjacency list plus indegree array plus heap |

The complexity fits comfortably within limits since m is up to 200000 and each heap operation is logarithmic in n, making the total operations manageable under a 2-second constraint.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        n, m = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        indeg = [0] * (n + 1)

        for _ in range(m):
            a, b = map(int, input().split())
            adj[a].append(b)
            indeg[b] += 1

        heap = []
        for i in range(1, n + 1):
            if indeg[i] == 0:
                heapq.heappush(heap, i)

        order = []
        while heap:
            u = heapq.heappop(heap)
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    heapq.heappush(heap, v)

        if len(order) != n:
            return "IMPOSSIBLE"
        return " ".join(map(str, order))

    return solve()

# provided samples
assert run("5 5\n1 2\n2 3\n2 4\n2 5\n3 4\n") == "1 2 3 4 5"
assert run("5 4\n1 2\n2 3\n3 1\n5 4\n") == "IMPOSSIBLE"

# custom cases
assert run("1 0\n") == "1", "single node"
assert run("3 0\n") == "1 2 3", "no edges lexicographically smallest"
assert run("3 3\n1 2\n2 3\n1 3\n") == "1 2 3", "chain with extra edge"
assert run("4 2\n2 1\n3 1\n") == "2 3 1 4", "multiple sources ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | minimal base case |
| no edges | 1 2 3 | lexicographically smallest trivial DAG |
| extra edge | 1 2 3 | redundant constraint handling |
| multiple sources | 2 3 1 4 | correct heap prioritization |

## Edge Cases

A key edge case is when multiple nodes have indegree zero at the start. For example, with edges 2 → 3 and 4 → 5 in a 5-node graph, both 1, 2, and 4 might initially be available. The algorithm places all of them into the heap and always selects the smallest, ensuring deterministic lexicographic behavior.

Another edge case is a fully cyclic graph such as 1 → 2 → 3 → 1. Here no node ever reaches indegree zero, so the heap starts empty or becomes empty immediately after initialization. The output list remains incomplete, and the algorithm correctly outputs IMPOSSIBLE.

A final edge case is a graph with disconnected components. Each component is processed independently through indegree propagation, and the heap naturally merges them into a single global ordering by always selecting the smallest available node across components.
