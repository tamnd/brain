---
title: "CF 105900A - Ascending mountains"
description: "We are given a set of mountains labeled from 1 to N, where each label also represents its difficulty level. There are M precedence rules of the form A before B, meaning Isa cannot climb mountain B unless she has already climbed mountain A."
date: "2026-06-21T18:12:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105900
codeforces_index: "A"
codeforces_contest_name: "VI UnBalloon Contest Mirror"
rating: 0
weight: 105900
solve_time_s: 49
verified: true
draft: false
---

[CF 105900A - Ascending mountains](https://codeforces.com/problemset/problem/105900/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of mountains labeled from 1 to N, where each label also represents its difficulty level. There are M precedence rules of the form A before B, meaning Isa cannot climb mountain B unless she has already climbed mountain A. Since A < B is always guaranteed, every dependency only points from a lower-numbered mountain to a higher-numbered one.

The task is to construct an order in which Isa climbs all mountains exactly once while respecting all dependencies. Among all valid orders, we must output the lexicographically smallest one, meaning we always prefer to place smaller-numbered mountains as early as possible, provided we do not violate any prerequisite constraints. If no valid ordering exists, we must report impossibility.

The structure is a directed graph over vertices 1 through N, and each constraint is a directed edge A → B. The goal is a topological ordering, but not just any topological ordering, the smallest in lexicographic order.

The constraints go up to 2 · 10^5 vertices and edges. This immediately rules out any O(NM) or O(N^2) simulation strategy. Even O(NM) graph traversal is too slow. The only acceptable solutions are close to O((N + M) log N) or O(N + M).

A key structural constraint is that edges only go from smaller to larger labels. This guarantees the graph is acyclic by construction, since you can never return to a smaller index, so cycles cannot exist. However, we still need to respect the ordering constraints and optimize lexicographic output.

A naive but important pitfall is to think that simply sorting adjacency lists or greedily picking smallest available node without careful dependency tracking is enough. For example, if we always pick the smallest unvisited node globally, we might pick a node whose prerequisites are not yet satisfied.

Another subtle edge case is when multiple nodes become available at different times. If we do not maintain a global structure of currently valid nodes, we may miss the correct lexicographically smallest continuation.

## Approaches

A brute-force idea is to repeatedly scan all nodes and pick the smallest node that has not been used and whose prerequisites are already satisfied. After selecting it, we mark it as used and repeat. To check validity each time, we either recompute indegrees or scan all edges affecting it.

This works logically because at every step we ensure constraints are respected, but the cost is severe. For each of N steps, scanning all nodes costs O(N), and verifying prerequisites can add up to O(M). This leads to O(N^2 + M) behavior, which is far beyond limits when N is 2 · 10^5.

The key observation is that this is a classic topological ordering problem, and the only difference is that we must always choose the smallest available node among those whose indegree is zero. That suggests maintaining a dynamic set of currently valid candidates.

Once we maintain all nodes with zero incoming edges in a structure that always gives us the smallest element, the process becomes straightforward. We repeatedly extract the smallest available node, append it to the answer, and remove its outgoing edges, possibly activating new nodes. A min-heap or priority queue is the natural tool for this.

The condition A < B ensures the graph is already acyclic, so we do not need cycle detection logic beyond verifying whether we processed all nodes at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan each step | O(N^2 + M) | O(N + M) | Too slow |
| Min-heap lexicographic topological sort | O((N + M) log N) | O(N + M) | Accepted |

## Algorithm Walkthrough

We model the problem as a directed graph and compute indegrees for each node. Nodes with indegree zero are those whose prerequisites are already satisfied.

1. Build an adjacency list for all edges A → B, and compute indegree[B] for each edge. This encodes exactly how many prerequisites each mountain still needs.
2. Initialize a min-heap (priority queue) and insert every node i such that indegree[i] = 0. These are mountains that can be climbed immediately without violating constraints.
3. Repeatedly extract the smallest element from the heap. This ensures that among all currently available mountains, we always pick the lexicographically smallest option.
4. Append this chosen node to the answer sequence.
5. For each neighbor v of the chosen node u, decrement indegree[v] by 1. If indegree[v] becomes zero, push v into the heap. This represents that all prerequisites of v are now satisfied, so it becomes available for selection.
6. Continue until the heap is empty.
7. If the resulting sequence has length N, output it. Otherwise, output -1.

The correctness of always pushing newly unlocked nodes immediately into the heap ensures that we never delay a valid candidate that could be chosen earlier lexicographically.

### Why it works

At every step, the heap contains exactly the set of nodes whose prerequisites have all been satisfied by previously chosen nodes. Any node not in the heap has a remaining dependency, so it is invalid to choose it. Among valid candidates, choosing the smallest label is optimal because any larger choice would lexicographically worsen the sequence without enabling any advantage later. The dependency structure guarantees that once a node becomes available, delaying it can only push it further right in the ordering, never improving feasibility or lexicographic order.

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

    res = []

    while heap:
        u = heapq.heappop(heap)
        res.append(u)

        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    if len(res) != n:
        print(-1)
    else:
        print(*res)

if __name__ == "__main__":
    solve()
```

The adjacency list stores all dependency edges, while the indegree array tracks how many prerequisites each node still has unmet. The heap is the key structure that enforces lexicographic optimality by always selecting the smallest available node.

A subtle implementation detail is that nodes are pushed into the heap only when their indegree becomes exactly zero. Pushing earlier would violate correctness because the node would not yet be valid to use.

The final check ensures that all nodes were processed. Even though the input guarantees A < B, this check is still the standard safety condition for topological sorting problems.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 3
```

| Step | Heap | Chosen | Result | Indegrees |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | [1] | (2:1, 3:0) |
| 2 | [2] | 2 | [1,2] | (3:0) |
| 3 | [3] | 3 | [1,2,3] | all zero |

The heap always contains exactly one valid choice, so the ordering is forced. This confirms that the algorithm degenerates correctly into a simple chain traversal.

### Example 2

Input:

```
5 2
1 5
2 5
```

| Step | Heap | Chosen | Result | Indegrees |
| --- | --- | --- | --- | --- |
| 1 | [1,2,3,4] | 1 | [1] | 5:1 |
| 2 | [2,3,4] | 2 | [1,2] | 5:0 |
| 3 | [3,4,5] | 3 | [1,2,3] | 5:0 |
| 4 | [4,5] | 4 | [1,2,3,4] | 5:0 |
| 5 | [5] | 5 | [1,2,3,4,5] | done |

This shows how node 5 becomes available only after both prerequisites are processed, and how the heap naturally enforces lexicographic ordering among independent nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Each node is pushed and popped at most once, each edge is processed once, heap operations cost log N |
| Space | O(N + M) | adjacency list plus indegree array and heap storage |

The constraints allow up to 2 · 10^5 nodes and edges, so logarithmic overhead is acceptable. The solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

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

    res = []
    while heap:
        u = heapq.heappop(heap)
        res.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    if len(res) != n:
        return "-1"
    return " ".join(map(str, res))

# provided samples
assert run("3 2\n1 2\n2 3\n") == "1 2 3"
assert run("5 1\n1 5\n") == "1 2 3 4 5"

# custom cases
assert run("1 0\n") == "1"
assert run("3 0\n") == "1 2 3"
assert run("3 3\n1 2\n2 3\n1 3\n") == "1 2 3"
assert run("4 3\n1 2\n1 3\n1 4\n") == "1 2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node, no edges | 1 | minimal graph |
| no constraints | sorted order | all nodes initially available |
| chain + extra edge | 1 2 3 | redundant dependency handling |
| star from 1 | 1 2 3 4 | lexicographic priority among independent nodes |

## Edge Cases

One important edge case is when no dependencies exist. In that situation, every node has indegree zero initially, so the heap contains all nodes. The algorithm then simply outputs 1 through N in order because the heap enforces lexicographic selection at every step.

Another case is when dependencies form a strict chain. For example, 1 → 2 → 3 → 4. The heap always contains exactly one element, so the algorithm behaves like a simple traversal. There is no ambiguity in ordering, and the heap overhead does not change correctness.

A more subtle case is when a node becomes available late but is smaller than already available nodes. For example, if node 3 becomes available after node 5, the heap ensures node 3 is selected immediately upon insertion, preserving lexicographic minimality. This is exactly the scenario that a naive “scan all candidates each time” approach would mishandle or implement inefficiently.
