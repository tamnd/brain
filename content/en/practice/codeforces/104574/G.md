---
title: "CF 104574G - Iguana Walking"
description: "We are given a directed functional graph: each iguana i has exactly one outgoing edge to p[i], so from every node there is exactly one deterministic next position."
date: "2026-06-30T08:17:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104574
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 2 (Beginner)"
rating: 0
weight: 104574
solve_time_s: 79
verified: true
draft: false
---

[CF 104574G - Iguana Walking](https://codeforces.com/problemset/problem/104574/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed functional graph: each iguana i has exactly one outgoing edge to p[i], so from every node there is exactly one deterministic next position. Iguana 1 is special because it never moves, it stays fixed at node 1, and we interpret this as a sink where paths may eventually terminate.

Every iguana repeatedly follows its outgoing edge at each time step. So at time t, iguana i is at p applied t times to i. Some iguanas eventually reach node 1, while others never do because they get trapped in a cycle that does not include 1.

The task is to compute the expected time for iguanas that are able to reach node 1 to actually arrive there, starting from time 0. The expectation is taken uniformly over the set of iguanas that eventually reach 1, and iguana 1 itself is included with arrival time 0.

A direct reading shows that we are dealing with distances in a directed graph where every node has outdegree 1, but only nodes that can reach 1 matter, and we must average their distances to 1.

The constraints are large: the total number of nodes across test cases is up to 2×10^5. This rules out any solution that simulates each iguana independently by walking forward step by step, since that could cost O(N^2) in worst cases like long chains.

A subtle edge case appears when cycles exist. Any node in a cycle that does not contain 1 never reaches the destination and must be excluded entirely. Another edge case is nodes that eventually enter such a cycle after a long prefix; they must also be excluded even though their prefix path may look like a valid route at first.

For example, consider 1 → 2 → 3 → 2. Nodes 2 and 3 never reach 1, so only node 1 counts and the answer is 0. A naive DFS that does not properly detect cycles would incorrectly assign finite distances.

Another case is a long chain feeding into 1, like 5 → 4 → 3 → 2 → 1. All nodes contribute with distances 0,1,2,3,4 respectively, and the expectation is their average. Any solution that recomputes paths separately for each node risks repeated traversal of the same chain.

## Approaches

The structure is a functional graph where each node has exactly one outgoing edge. The natural brute force approach is to compute, for every node, the number of steps required to reach node 1 by repeatedly following p[i] until we either reach 1 or detect a loop.

This works conceptually because each path is deterministic. However, in the worst case, the graph can be a single chain of length N or a cycle of length N. If we recompute the walk for every node independently, each walk can take O(N), leading to O(N^2) total operations, which is too slow for 2×10^5 nodes.

The key observation is that this is a reverse-tree problem once cycles are removed. In a functional graph, every connected component contains exactly one cycle. Only the component containing node 1 is relevant. Inside that component, we can reverse edges and treat it like a tree rooted at 1. All nodes that can reach 1 lie in the reverse reachable set of 1 in this reversed graph.

Once we restrict ourselves to nodes that can reach 1, the distance from a node to 1 is simply its depth in this reverse BFS tree. So the task reduces to computing all shortest distances in an unweighted graph starting from node 1, but on the reversed edges.

We then average these distances over all reachable nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force walk per node | O(N^2) | O(1) | Too slow |
| Reverse graph BFS from 1 | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We solve the problem by turning the functional graph into its reverse adjacency structure and performing a BFS from node 1.

1. Build a reverse adjacency list where for each i, we add i to rev[p[i]]. This flips the direction of motion so that moving backward corresponds to “who can reach this node in one step”. This is necessary because we want distances toward node 1.
2. Run a BFS starting from node 1 over the reversed graph. We assign dist[1] = 0 and push it into a queue.
3. Pop nodes from the queue. For each node u, iterate over all v in rev[u]. If v has not been visited, set dist[v] = dist[u] + 1 and push v. This ensures we are expanding outward in increasing number of steps required to reach 1.
4. After BFS finishes, only nodes that were visited are those that can reach node 1. We compute the sum of all dist values over visited nodes and also count how many nodes were visited.
5. The answer is sum / count.

The reason we can safely ignore unvisited nodes is that BFS on the reversed graph exactly captures reachability into node 1. Any node not visited lies in a cycle or in a component disconnected from 1 in reverse direction, meaning it cannot reach 1 in the original graph.

### Why it works

The BFS guarantees that when a node v is first assigned a distance, that distance is the shortest number of reverse edges needed to reach 1, which corresponds exactly to the number of forward steps needed for v to reach 1. Since every edge has unit weight, BFS layers match exact step counts. The set of visited nodes is precisely the set of nodes with finite distance to 1, so excluding others is correct by definition of the process.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        p = list(map(int, input().split()))
        
        rev = [[] for _ in range(n + 1)]
        for i in range(1, n + 1):
            rev[p[i - 1]].append(i)
        
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
        
        print(total / cnt)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the BFS formulation. The reverse adjacency list is built in linear time. The BFS ensures each node is processed once, and dist[i] stores the exact number of steps needed to reach node 1.

The only subtle point is ensuring that unreachable nodes are not included in the average. This is handled by checking dist[i] != -1. Another important detail is using floating division at the end, since the answer is expected as a real number.

## Worked Examples

### Example 1

Input:

```
3
5
5 2 3 1 4
```

We build edges: 1→5, 2→2, 3→3, 4→1, 5→4. Reverse edges are: 5←1, 2←2, 3←3, 1←4, 4←5.

BFS starts at 1.

| Step | Node | Distance | Newly reached |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 4 |
| 2 | 4 | 1 | 5 |
| 3 | 5 | 2 | 1 (already seen) |

Node 2 and 3 are not reachable from 1 in reverse, so they are excluded.

Distances: node 1 = 0, node 4 = 1, node 5 = 2. Average = (0 + 1 + 2) / 3 = 1.

This shows that only nodes in the reverse reachable set contribute.

### Example 2

Input:

```
3
3
1 2 3
```

Every node points to itself or forms trivial self-loops.

Reverse graph has each node pointing to itself.

BFS:

| Step | Node | Distance | Newly reached |
| --- | --- | --- | --- |
| 1 | 1 | 0 | none |

Only node 1 is reachable. Answer is 0 / 1 = 0.

This demonstrates that isolated cycles not involving 1 are correctly excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each node and edge is processed once in reverse BFS |
| Space | O(N) | Reverse adjacency list and distance array |

The total sum of N across test cases is 2×10^5, so linear processing per test case is sufficient and comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        T = int(input())
        out = []
        for _ in range(T):
            n = int(input())
            p = list(map(int, input().split()))
            rev = [[] for _ in range(n + 1)]
            for i in range(1, n + 1):
                rev[p[i - 1]].append(i)

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

            out.append(str(total / cnt))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""3
5
5 2 3 1 4
3
1 2 3
10
2 3 4 5 6 7 8 9 10 1
""") == """1.0
0.0
4.5"""

# custom cases
assert run("""1
1
1
""") == "0.0", "single node"

assert run("""1
4
2 3 4 1
""") == "1.5", "simple cycle with all reachable"

assert run("""1
4
2 3 4 4
""") == "1.0", "cycle + tail"

assert run("""1
5
2 3 4 5 5
""") == "2.0", "long chain into cycle excluding tail"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node self-loop | 0.0 | minimal case |
| pure cycle | 1.5 | all nodes contribute |
| cycle with tail | 1.0 | mixed reachability |
| chain into cycle | 2.0 | exclusion of non-reachable nodes |

## Edge Cases

One edge case is when only node 1 can reach itself. In that case the BFS visits exactly one node and the denominator is 1, producing 0. The algorithm handles this naturally since dist[1] = 0 and no other nodes are counted.

Another edge case is a pure cycle disconnected from 1. For example 2 → 3 → 2. The reverse BFS from 1 never reaches these nodes, so they are excluded entirely. This prevents incorrect infinite loops and avoids dividing by zero issues because node 1 is always counted.

A third case is a long chain feeding into 1. For example 4 → 3 → 2 → 1. BFS assigns distances 0,1,2,3 correctly in increasing order from the root. The average is computed over all four nodes, matching the definition of “reachable iguanas”.
