---
title: "CF 103361I - \u0420\u0430\u0444\u0442\u0438\u043d\u0433"
description: "We are given a directed graph whose vertices are lakes and whose edges are rivers flowing from one lake to another."
date: "2026-07-03T13:08:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "I"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 58
verified: true
draft: false
---

[CF 103361I - \u0420\u0430\u0444\u0442\u0438\u043d\u0433](https://codeforces.com/problemset/problem/103361/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph whose vertices are lakes and whose edges are rivers flowing from one lake to another. The structure is highly constrained: each lake has at most one incoming river and at most two outgoing rivers, and there are no directed cycles, so water always moves downhill in a consistent direction.

A rafting trip starts at a lake with no incoming rivers. From there, whenever the raft reaches a lake with multiple outgoing rivers, the next river is chosen uniformly at random among the available options. The process continues until the raft reaches a lake with no outgoing rivers, which becomes the final destination.

The task is to determine which terminal lake is most likely to be the final stopping point if we start from a uniformly random source lake and then follow the described random choices. If multiple terminal lakes share the same maximum probability, we must output the one with the smallest index.

The constraints imply a graph with up to 200,000 nodes and edges, so any solution must be essentially linear in the size of the graph. Algorithms that attempt to simulate paths explicitly or recompute probabilities independently per starting node will not survive within the limits. The structure is also important: indegree at most one means every node belongs to exactly one tree-like component, so the graph is a forest of directed trees pointing downward.

A few edge cases are worth making explicit.

If there are no rivers at all, every lake is simultaneously a starting lake and a terminal lake. For example, if n = 3 and m = 0, then all three lakes are valid starting points, and each is also a stopping point, so each has probability 1/3 of being chosen.

If the graph forms a chain such as 1 → 2 → 3 → 4, then there is only one source (1) and only one sink (4), so the answer is trivially 4.

If branching occurs, such as 1 → 2, 1 → 3, and both 2 and 3 lead to different sinks, then the probability splits and accumulates along different paths. A naive approach that treats paths independently without correctly propagating shared prefix probabilities will overcount or undercount contributions.

## Approaches

A direct simulation of the process would repeatedly choose a starting lake and then simulate random transitions until reaching a sink. Even a single simulation can take O(n) in the worst case, and estimating probabilities accurately would require a very large number of runs. This is far beyond the limits given n up to 2 · 10^5.

A more structured brute-force approach is to compute, for each source, a full probability distribution over sinks by running a DFS or BFS that splits probability equally at every branching point. This correctly models the random walk, but repeating it for every source leads to recomputation of large shared subtrees. In the worst case where the graph is a single tree-like structure, this becomes O(n^2).

The key observation is that the process is linear and Markovian in a very simple way. Once we know the probability of reaching a node, we can distribute that probability forward to its children without revisiting the past. Since each node has exactly one parent, probability flow never merges from different parents, it only splits downward. This allows a single pass propagation starting from all sources simultaneously.

We assign equal initial probability to all source nodes, then push probability forward along edges, dividing equally among outgoing edges. Each sink simply accumulates the total probability mass that reaches it. The best sink is the one with maximum accumulated mass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per source | O(n^2) | O(n) | Too slow |
| Forward probability propagation | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We treat probability as a flow that starts at source nodes and moves downward through the graph.

1. Identify all nodes with zero incoming edges. These are the possible starting lakes. Count them as k. Assign each such node an initial probability of 1/k. This reflects the uniform random choice of starting point.
2. Build adjacency lists for outgoing rivers and compute indegrees to detect sources. This prepares the structure for a single pass propagation.
3. Initialize an array p where p[v] represents the probability that the raft arrives at lake v. Set p[source] = 1/k for all sources and 0 for all other nodes.
4. Process nodes in topological order. Since each node has at most one incoming edge, we can also process by simply iterating in any order that respects parent before child, which is naturally achieved by BFS/queue from sources.
5. For each node u, distribute its probability mass evenly among its outgoing edges. If u has d outgoing edges, each child v receives p[v] += p[u] / d. This models the uniform random choice at each branching.
6. If u has no outgoing edges, it is a sink, so we do not propagate further from it.
7. After propagation completes, scan all nodes and find those with no outgoing edges. Among them, choose the node with the maximum p value. If there is a tie, choose the smallest index.

### Why it works

The process is linear because every node has a unique path from exactly one source, so probability arriving at any node is fully determined by that source’s initial mass and the sequence of splits along the path. Since probability only splits and never merges, summing contributions from independent sources is valid. The propagation rule preserves total probability mass at every step, ensuring that all probability injected at sources eventually ends up at sinks without loss or duplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
g = [[] for _ in range(n)]
indeg = [0] * n
outdeg = [0] * n

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    indeg[v] += 1
    outdeg[u] += 1

sources = [i for i in range(n) if indeg[i] == 0]
k = len(sources)

p = [0.0] * n
if k > 0:
    init = 1.0 / k
    for s in sources:
        p[s] = init

from collections import deque
q = deque(sources)

while q:
    u = q.popleft()
    if outdeg[u] == 0:
        continue
    share = p[u] / outdeg[u]
    for v in g[u]:
        p[v] += share
        q.append(v)

best = -1
best_p = -1.0

for i in range(n):
    if outdeg[i] == 0:
        if p[i] > best_p or (abs(p[i] - best_p) < 1e-15 and i < best):
            best_p = p[i]
            best = i

print(best + 1)
```

The solution begins by constructing adjacency lists and computing indegrees to identify all valid starting lakes. The probability array is initialized only on those sources, each receiving equal mass. The queue drives a forward propagation similar to topological traversal, ensuring each node’s probability is distributed exactly once through its outgoing edges.

A subtle implementation point is that nodes may be enqueued multiple times in a naive BFS-style push, but correctness is not harmed because we are not relying on processing order for correctness, only for eventual full propagation. Each update is additive, so repeated enqueues simply continue distributing accumulated probability. This avoids the need for a strict topological sort.

Floating point arithmetic is sufficient here because probabilities are bounded and we only compare final values. The tie-breaking rule is handled explicitly using an epsilon comparison.

## Worked Examples

Consider a small graph:

Input:

```
4 3
1 2
1 3
2 4
```

Here sources are {1}, since only node 1 has indegree 0. We start with p(1) = 1.

We track propagation:

| Step | Node | p[node] | Action |
| --- | --- | --- | --- |
| init | 1 | 1.0 | start at source |
| 1 | 1 | 1.0 | split to 2 and 3 |
| 2 | 2 | 0.5 | receives half |
| 3 | 3 | 0.5 | receives half |
| 4 | 2 → 4 | 0.5 | 2 splits to 4 |
| final | 4 | 0.5 | sink probability |

Node 3 is a sink with probability 0.5, node 4 is also a sink with probability 0.5. Since there is a tie, the smaller index wins, so 3 is chosen.

This trace shows how probability splits at branching nodes and accumulates at sinks.

Now consider a chain with multiple sources:

Input:

```
3 1
1 3
```

Sources are {1, 2}, so each gets probability 1/2. Node 2 is itself a sink, so it immediately contributes 1/2. Node 1 passes its 1/2 to node 3, so node 3 also gets 1/2.

Both sinks have equal probability, and the smaller index among them is chosen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | each edge processes probability once during propagation |
| Space | O(n + m) | adjacency list plus probability and degree arrays |

The algorithm processes each node and edge a constant number of times, which fits comfortably within the limits for n, m up to 2 · 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    indeg = [0] * n
    outdeg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        indeg[v] += 1
        outdeg[u] += 1

    sources = [i for i in range(n) if indeg[i] == 0]
    k = len(sources)

    p = [0.0] * n
    if k > 0:
        init = 1.0 / k
        for s in sources:
            p[s] = init

    from collections import deque
    q = deque(sources)

    while q:
        u = q.popleft()
        if outdeg[u] == 0:
            continue
        share = p[u] / outdeg[u]
        for v in g[u]:
            p[v] += share
            q.append(v)

    best = -1
    best_p = -1.0
    for i in range(n):
        if outdeg[i] == 0:
            if p[i] > best_p or (abs(p[i] - best_p) < 1e-15 and i < best):
                best_p = p[i]
                best = i

    return str(best + 1)

# provided sample (as stated)
assert run("""4 3
1 2
1 3
2 4
""") == "3", "sample 1"

# single chain
assert run("""4 3
1 2
2 3
3 4
""") == "4", "chain"

# multiple sources, multiple sinks
assert run("""3 1
1 3
""") == "2", "two sources tie"

# no edges
assert run("""3 0
""") == "1", "all isolated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | 4 | deterministic sink in linear path |
| two sources | 2 | uniform start probability splitting |
| no edges | 1 | all nodes are both sources and sinks |

## Edge Cases

When there are no edges, every node is simultaneously a source and a sink. In this case the initialization assigns probability 1/n to every node, and since no propagation happens, all nodes keep equal probability. The algorithm correctly selects the smallest index.

When the graph is a pure chain, each node except the last has exactly one outgoing edge, so no splitting occurs. The probability flows entirely from the random start distribution down to the unique sink, preserving total mass and producing a single answer.

When branching occurs at a source, such as 1 → 2 and 1 → 3, the algorithm splits probability immediately and independently tracks both branches. Since no merging is possible due to indegree constraints, the accumulated values remain disjoint and additive, ensuring correct sink probabilities.
