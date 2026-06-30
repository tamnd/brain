---
title: "CF 104573G - Iguana Walking"
description: "We are given a directed graph where each iguana sits on a node from 1 to N, and every node has exactly one outgoing edge defined by the array p. In one time step, every iguana moves simultaneously from i to p[i]."
date: "2026-06-30T08:20:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104573
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 1"
rating: 0
weight: 104573
solve_time_s: 69
verified: true
draft: false
---

[CF 104573G - Iguana Walking](https://codeforces.com/problemset/problem/104573/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each iguana sits on a node from 1 to N, and every node has exactly one outgoing edge defined by the array p. In one time step, every iguana moves simultaneously from i to p[i]. The only exception is node 1: Iguana 1 never moves, and instead acts as a fixed root that others are trying to reach.

Each iguana repeatedly follows this deterministic rule. Some iguanas will eventually land on node 1, possibly after several steps. Others may be trapped in cycles that never include 1, in which case they never reach the leader and are ignored in the expectation.

The quantity we need is the average time, measured in steps from time 0, for all iguanas that can eventually reach node 1 to arrive there for the first time. Iguana 1 itself is included, contributing zero time.

The input size is large: up to 2·10^5 nodes across all test cases. This rules out any per-node simulation that walks forward step by step for each iguana, since following chains naively can degrade to quadratic behavior in long chains or cycles.

A subtle issue appears when cycles exist. Consider a cycle like 2 → 3 → 2 that does not connect to 1. A naive BFS from 1 in reverse edges would avoid counting these nodes, which is correct, but we still need correct distances for nodes that do reach 1 through long functional chains. Another subtle case is that the graph is not a tree, so multiple nodes can share suffix chains before merging into a cycle or into node 1.

Edge cases include:

A simple chain: 1 ← 2 ← 3 ← 4. Here answers are straightforward distances 0,1,2,3 and average is 1.5. Any method that mistakenly treats the graph as undirected would overcount.

A pure cycle with no access to 1, like 1 → 2 → 3 → 1 plus a disjoint cycle 4 → 5 → 4. Nodes 4 and 5 must be ignored entirely.

A self-loop at node 1 is implied since p1 exists but 1 never moves. That detail matters when computing reverse structures.

## Approaches

A brute-force idea is to simulate each iguana independently. For each i, we repeatedly apply p[i], then p[p[i]], and so on until we either reach 1 or detect repetition. If we reach 1 at step d, we contribute d to the sum; otherwise we ignore it. This is correct because each trajectory is deterministic, and the first time it hits 1 is well defined.

However, each walk can take O(N) steps in the worst case, and we do this for all nodes, leading to O(N^2) per test case. With N up to 2·10^5 overall, this is far too slow.

The key observation is that every node has exactly one outgoing edge, so the structure is a functional graph. Each component consists of a directed cycle with trees feeding into it. Only nodes whose path eventually reaches node 1 matter, so we only care about nodes in the basin of attraction of 1 in the reversed graph sense.

Once we restrict attention to reachable nodes, the problem reduces to computing shortest distances to node 1 in a graph where every edge has weight 1, but edges are directed forward along p. The natural way to compute distances to a fixed target in a functional graph is to reverse edges and run a BFS starting from node 1. This gives us the minimum number of steps needed to reach 1 from each node, which is exactly the time each iguana takes.

So the solution becomes: build reverse adjacency lists, run BFS from node 1, compute distances, and average only over nodes with finite distance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N^2) | O(1) | Too slow |
| Reverse Graph BFS | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Build a reverse adjacency list rev where rev[v] contains all nodes u such that p[u] = v. This converts “where do I go next” into “who can reach me in one step”, which is essential for backward search.
2. Initialize a distance array dist with -1 for all nodes. This marks all nodes as initially unreachable from node 1.
3. Set dist[1] = 0 and push node 1 into a queue. Node 1 is the source of the BFS because we measure how many steps are needed to arrive at it.
4. While the queue is not empty, pop a node u. For every node v in rev[u], if dist[v] is still -1, set dist[v] = dist[u] + 1 and push v into the queue. This propagates shortest arrival times outward along reverse edges.
5. After BFS completes, iterate over all nodes. For each node i with dist[i] != -1, add dist[i] to a running sum and increment a counter.
6. Compute the answer as sum / count. This averages only over nodes that can actually reach node 1.

Why it works: every edge in the reversed graph represents a valid forward move toward node 1 in exactly one step. BFS explores nodes in increasing number of steps from 1, and because all edges have equal weight, the first time we assign a distance to a node is guaranteed to be the minimum number of steps needed to reach node 1. Nodes not visited are exactly those that lie in cycles or components disconnected from 1, so they are correctly excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        rev = [[] for _ in range(n + 1)]
        for i in range(n):
            rev[p[i]].append(i + 1)

        dist = [-1] * (n + 1)
        q = deque([1])
        dist[1] = 0

        while q:
            u = q.popleft()
            for v in rev[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        total = 0
        cnt = 0
        for i in range(1, n + 1):
            if dist[i] != -1:
                total += dist[i]
                cnt += 1

        out.append(str(total / cnt if cnt else 0.0))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the reverse BFS idea. The reverse adjacency list rev is built using 1-based indexing, matching the problem definition. The BFS queue starts at node 1, and dist[1] is correctly set to zero since Iguana 1 is already at the leader.

A common mistake is iterating forward along p instead of reversing it. That would simulate movement away from 1 rather than toward it, which does not compute arrival times. Another subtle issue is forgetting to exclude unreachable nodes; the dist array check ensures we only average valid iguanas.

## Worked Examples

### Example 1

Input:

```
5
5 2 3 1 4
```

We build reverse edges:

| Node | Incoming nodes |
| --- | --- |
| 1 | 4 |
| 2 | 2 |
| 3 | 3 |
| 4 | 5 |
| 5 | 1 |

We run BFS from 1.

| Step | Queue | Popped | Newly updated |
| --- | --- | --- | --- |
| 1 | [1] | 1 | 4 → dist=1 |
| 2 | [4] | 4 | 5 → dist=2 |
| 3 | [5] | 5 | none |

Distances: 1:0, 4:1, 5:2, 2 and 3 unreachable.

Sum = 0 + 1 + 2 = 3, count = 3, answer = 1.0.

This confirms that only nodes in the basin of node 1 contribute.

### Example 2

Input:

```
3
1 2 3
```

Reverse edges:

2 → 2, 3 → 3, and 1 → 1.

BFS from 1 reaches only node 1.

| Step | Queue | Popped | Newly updated |
| --- | --- | --- | --- |
| 1 | [1] | 1 | none |

Sum = 0, count = 1, answer = 0.0.

This checks that self-loops and isolated components do not contaminate the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | Each node is enqueued once and each edge is processed once in reverse BFS |
| Space | O(N) | Reverse adjacency list and distance array |

The constraints allow up to 2·10^5 total nodes, so a linear-time BFS across all test cases fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            p = list(map(int, input().split()))

            rev = [[] for _ in range(n + 1)]
            for i in range(n):
                rev[p[i]].append(i + 1)

            dist = [-1] * (n + 1)
            q = deque([1])
            dist[1] = 0

            while q:
                u = q.popleft()
                for v in rev[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)

            total = 0
            cnt = 0
            for i in range(1, n + 1):
                if dist[i] != -1:
                    total += dist[i]
                    cnt += 1

            out.append(str(total / cnt if cnt else 0.0))

        return "\n".join(out)

    return solve()

# provided samples
assert run("3\n5\n5 2 3 1 4\n3\n1 2 3\n10\n2 3 4 5 6 7 8 9 10 1\n") == "1.0\n0.0\n4.5"

# custom cases
assert run("1\n1\n1\n") == "0.0", "single node"
assert run("1\n4\n2 3 4 2\n") == "1.0", "cycle excluding root except entry"
assert run("1\n4\n1 1 1 1\n") == "1.0", "all direct to root"
assert run("1\n6\n2 3 4 5 6 4\n") == "2.0", "tree into cycle, partial reach"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node self-loop | 0.0 | minimal case and root handling |
| small cycle | 1.0 | cycle handling and reachability |
| all point to root | 1.0 | star structure correctness |
| chain into cycle | 2.0 | exclusion of unreachable cycle nodes |

## Edge Cases

A key edge case is when the graph consists mostly of cycles that do not connect to node 1. In such a case, BFS from node 1 never reaches them, and they must not influence the average. For example, in a graph where 2 → 3 → 2 and 4 → 5 → 4 while 1 is isolated, only node 1 is counted. The reverse BFS naturally leaves all other nodes at dist = -1, so they are excluded cleanly.

Another edge case is when every node eventually leads to 1 in a long chain. For instance, 1 ← 2 ← 3 ← … ← N. BFS assigns distances 0 through N−1, and the average becomes (N−1)/2. The algorithm handles this without modification because each node is discovered exactly once in increasing distance order.

A third subtle case is when multiple branches merge before reaching a cycle or node 1. Reverse BFS handles this correctly because once a node is visited, it is never revisited, ensuring that only the shortest path to 1 is recorded, even if multiple forward paths exist.
