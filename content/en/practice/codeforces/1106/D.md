---
title: "CF 1106D - Lunar New Year and a Wander"
description: "We are given an undirected connected graph with $n$ nodes. Bob starts at node 1 and performs a walk along edges. Every time he enters a node that has never been seen before, he writes it down."
date: "2026-06-13T08:10:50+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1106
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 536 (Div. 2)"
rating: 1500
weight: 1106
solve_time_s: 280
verified: true
draft: false
---

[CF 1106D - Lunar New Year and a Wander](https://codeforces.com/problemset/problem/1106/D)

**Rating:** 1500  
**Tags:** data structures, dfs and similar, graphs, greedy, shortest paths  
**Solve time:** 4m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected connected graph with $n$ nodes. Bob starts at node 1 and performs a walk along edges. Every time he enters a node that has never been seen before, he writes it down. The walk continues until all nodes have been visited at least once, and the written sequence contains every node exactly once.

The task is not to output a specific walk, but to determine the lexicographically smallest possible sequence of first-visits that Bob can obtain by choosing his traversal path freely.

So the real problem is about controlling the order in which nodes are discovered in a graph traversal, starting from node 1, under the constraint that movement is only along edges.

The constraints $n, m \le 10^5$ immediately rule out any approach that tries to simulate all possible walks or performs exponential exploration over paths. Even $O(n^2)$ is unsafe in dense graphs. We need something close to linear or linearithmic time, typically $O((n + m)\log n)$ or $O(n + m)$.

A naive approach would be to perform a DFS or BFS and always choose the smallest-numbered unvisited neighbor. However, this fails in graphs where locally optimal choices block access to smaller nodes later.

A concrete failure scenario is a cycle-like structure where greedy local decisions can isolate smaller nodes. For example:

Input:

```
4 4
1 4
4 3
3 2
2 4
```

If we always choose the smallest neighbor greedily without global ordering, we might go $1 \to 4 \to 3 \to 2$, but a different exploration strategy could allow a lexicographically smaller prefix by carefully delaying certain edges. The key difficulty is that once a node is visited in DFS order, its placement in the output sequence is fixed.

So we need a traversal strategy that enforces global lexicographic minimality, not just local greedy choices.

## Approaches

A brute-force interpretation is to consider all possible valid walks starting from node 1, track the resulting visitation order, and take the lexicographically smallest sequence. This is theoretically correct because it explores all feasible permutations induced by graph walks. However, the number of walks grows exponentially with cycles in the graph. Even a simple graph with branching factor 3 over depth 100 becomes astronomically large.

The key insight is that we only care about the order of first visits, not the full walk. Once a node is visited, it is never relevant again for ordering decisions. This suggests that we are constructing a DFS-like tree, but with a global preference for smallest available node at each expansion point.

If we attempt a standard DFS with adjacency lists sorted in ascending order, it still fails in cases where visiting a smaller neighbor too early prevents reaching an even smaller node through a different branch ordering. The correct idea is to simulate DFS but maintain a global set of currently reachable but not yet fully explored nodes, always choosing the smallest among them that can be reached from the current traversal frontier.

This leads to a modified DFS using a priority queue (min-heap). We push nodes as they become reachable, and always extract the smallest available node next. Once a node is visited, we expand it and insert its unvisited neighbors. This behaves like a lexicographically constrained exploration of the reachable frontier.

The important structural property is that at any moment, any node already discovered but not yet processed is a valid candidate for the next output position, and choosing the smallest preserves lexicographic minimality globally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all walks) | exponential | exponential | Too slow |
| Greedy DFS with min-heap frontier | $O((n + m)\log n)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph.

We need fast access to neighbors of each node, since expansion depends on graph structure.
2. Maintain a boolean array `visited` to track whether a node has already been recorded.

This ensures each node appears exactly once in the output.
3. Use a min-heap (priority queue) initialized with node 1.

This heap represents all nodes that are reachable from the traversal so far but not yet processed.
4. Repeatedly extract the smallest node `u` from the heap.

This guarantees that among all valid candidates, we always choose the smallest possible next element in the sequence.
5. If `u` is already visited, skip it.

This can happen because nodes may be inserted multiple times from different neighbors.
6. Otherwise, mark `u` as visited and append it to the answer sequence.
7. Push all unvisited neighbors of `u` into the heap.

These become newly reachable candidates for future steps.
8. Continue until the heap is empty.

The key reasoning step is that we never revisit a node in output order, but we may reinsert it into the heap multiple times; duplicates do not matter because `visited` filters them.

### Why it works

At every step, the heap contains exactly the set of nodes that are reachable from already visited nodes through at least one edge, but not yet included in the output. Any valid walk must eventually visit one of these nodes next. Choosing the smallest among them ensures that no alternative valid traversal can produce a smaller prefix, because any smaller node is either already taken or unreachable without passing through already fixed nodes. This creates a greedy invariant: after producing the first $k$ nodes, the algorithm has produced the lexicographically smallest prefix achievable by any valid walk.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    visited = [False] * (n + 1)
    heap = []

    heapq.heappush(heap, 1)

    res = []

    while heap:
        u = heapq.heappop(heap)
        if visited[u]:
            continue

        visited[u] = True
        res.append(u)

        for v in g[u]:
            if not visited[v]:
                heapq.heappush(heap, v)

    print(*res)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the full graph structure so we can expand each visited node efficiently. The heap ensures that among all frontier nodes, we always pick the smallest available candidate. The visited array ensures correctness despite duplicates in the heap, since a node may be discovered from multiple parents.

A subtle point is that we do not sort adjacency lists. Sorting is unnecessary because global ordering is enforced by the heap, and sorting would only add overhead without improving correctness.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
1 3
```

| Step | Heap | Visited | Output |
| --- | --- | --- | --- |
| 1 | [1] | {} | [] |
| 2 | [] | {1} | [1] |
| 3 | [2, 3] | {1} | [1] |
| 4 | [3] | {1,2} | [1,2] |
| 5 | [] | {1,2,3} | [1,2,3] |

This shows that after expanding node 1, both neighbors become candidates, and the heap ensures 2 is chosen before 3, producing the lexicographically smallest sequence.

### Example 2

Input:

```
5 5
1 4
4 3
3 2
2 4
4 5
```

| Step | Heap | Visited | Output |
| --- | --- | --- | --- |
| 1 | [1] | {} | [] |
| 2 | [] | {1} | [1] |
| 3 | [4] | {1} | [1] |
| 4 | [3,5] | {1,4} | [1,4] |
| 5 | [2,5] | {1,3,4} | [1,4,3] |
| 6 | [5] | {1,2,3,4} | [1,4,3,2] |
| 7 | [] | {1,2,3,4,5} | [1,4,3,2,5] |

The trace shows how the heap dynamically maintains the frontier and always selects the smallest reachable unvisited node.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | each edge insertion and node extraction uses a heap operation |
| Space | $O(n + m)$ | adjacency list plus heap and visited array |

The graph size up to $10^5$ nodes and edges fits comfortably within these bounds since heap operations are logarithmic and the total number of operations scales linearly with edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        visited = [False] * (n + 1)
        heap = [1]
        res = []

        while heap:
            u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            res.append(u)
            for v in g[u]:
                if not visited[v]:
                    heapq.heappush(heap, v)

        return " ".join(map(str, res))

    return solve()

# provided sample
assert run("""3 2
1 2
1 3
""") == "1 2 3"

# all connected line
assert run("""4 3
1 2
2 3
3 4
""") == "1 2 3 4"

# star graph
assert run("""5 4
1 2
1 3
1 4
1 5
""") == "1 2 3 4 5"

# cycle
assert run("""4 4
1 2
2 3
3 4
4 1
""") == "1 2 3 4"

# duplicated edges
assert run("""3 4
1 2
1 2
2 3
1 3
""") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| line graph | 1 2 3 4 | simple chain traversal |
| star graph | 1 2 3 4 5 | priority among neighbors |
| cycle graph | 1 2 3 4 | handling cycles |
| duplicate edges | 1 2 3 | multiedge robustness |

## Edge Cases

One subtle case is duplicate edges and self-loops. For example:

```
3 3
1 1
1 2
2 3
```

The self-loop on 1 causes node 1 to be pushed into the heap multiple times, but the visited check ensures it is only processed once. The algorithm still proceeds as:

heap starts as [1], process 1, push 1,2,2,3, then repeatedly skip visited 1 and duplicate 2 entries, finally producing 1 2 3.

Another edge case is when the smallest-numbered node is not immediately reachable without passing through larger nodes. The heap approach resolves this naturally because reachability expands only through already visited nodes, ensuring we never consider truly unreachable nodes, and among reachable ones we always pick the smallest available candidate.
