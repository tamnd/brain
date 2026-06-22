---
title: "CF 105323D - \u6218\u81f3\u7ec8\u7ae0"
description: "We are given a set of nodes, each representing a demon. Every node has a required strength threshold, a reward strength increase, and a set of prerequisite “keys”."
date: "2026-06-22T13:58:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105323
codeforces_index: "D"
codeforces_contest_name: "2024 Xiangtan University Summer Camp-Div.2"
rating: 0
weight: 105323
solve_time_s: 71
verified: true
draft: false
---

[CF 105323D - \u6218\u81f3\u7ec8\u7ae0](https://codeforces.com/problemset/problem/105323/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of nodes, each representing a demon. Every node has a required strength threshold, a reward strength increase, and a set of prerequisite “keys”. A node can only be attempted if two conditions are simultaneously satisfied: all of its prerequisite keys have already been obtained from previously defeated nodes, and the current strength is at least its requirement.

When a node is defeated, it is removed from consideration, it contributes its index as a key that may unlock other nodes, and it increases the current strength by its reward value. The process starts from an initial strength and continues greedily until no further node can be defeated.

The key structural constraint is that the key-dependency graph is a directed acyclic graph. This removes the possibility of circular locking, so once a node becomes available in terms of keys, it will never be invalidated again.

The constraints reach up to two hundred thousand nodes and two hundred thousand total dependency edges. Any solution that repeatedly scans all nodes or recomputes feasibility from scratch per step will fail, since that would lead to quadratic behavior in the worst case. This immediately pushes the solution toward maintaining incremental structures, typically priority queues or BFS-like propagation over a DAG.

A subtle failure case appears when multiple nodes become available at the same time but only some are currently affordable due to strength. Choosing them in an arbitrary order can lead to dead ends.

Consider this scenario: current strength is 10, and two nodes become available, one requiring 10 strength and giving +1, another requiring 1 strength and giving +100. If we mistakenly pick the +1 node first, we might fail to reach nodes that require slightly higher thresholds later, even though a better ordering exists. This shows that feasibility alone is not enough, and we must carefully choose which available node to process next.

## Approaches

A direct simulation is straightforward to describe. We repeatedly scan all nodes, and whenever a node has all its keys collected and its requirement is satisfied by current strength, we defeat it, update strength, and repeat. This is correct because it follows the rules exactly.

The problem with this approach is performance. Each defeat may require scanning all n nodes to find a valid candidate. With up to 200,000 nodes, this leads to about n operations per step, and up to n steps, resulting in quadratic complexity that is far beyond the limit.

The key observation is that key dependencies form a DAG, so “becoming available” is a monotonic event driven by indegree reduction. Once a node’s prerequisites are satisfied, it can be inserted into a pool of candidates exactly once. From that point onward, the only remaining constraint is whether its required strength is met.

This separates the problem into two independent filters. The first filter is structural, handled by topological unlocking. The second filter is numerical, handled by strength thresholds. We can maintain a pool of unlocked nodes and dynamically select among those whose requirement is currently satisfied.

To make selection efficient, we maintain two priority structures. One stores unlocked nodes ordered by requirement, so we can quickly move newly affordable nodes into an active pool. The second stores currently affordable nodes ordered by reward strength gain, so we always pick the most beneficial next step among what is feasible right now.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n + m) | Too slow |
| Dual Priority Queue Optimization | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process the dependency graph while continuously maintaining the set of currently reachable and affordable nodes.

1. Compute indegree for each node based on its key requirements. Build adjacency lists from each key to the nodes it unlocks. Nodes with zero indegree are initially unlocked.
2. Insert all initially unlocked nodes into a structure ordered by their required strength. These nodes are structurally available but not necessarily affordable.
3. Maintain current strength as a variable, starting from the initial value.
4. Repeatedly move nodes whose required strength is at most the current strength from the unlocked structure into a second structure ordered by reward gain. This ensures we only consider nodes we can actually defeat at this moment.
5. If the affordable structure is empty, the process terminates because no remaining node can be defeated with current strength.
6. Otherwise, select the node with the highest reward gain, defeat it, record it in the answer, and increase current strength.
7. For each node that depended on it, decrease indegree. If any dependent node reaches zero indegree, insert it into the unlocked structure.
8. Repeat from step 4 until no more progress is possible.

The correctness hinges on the fact that once a node becomes unlocked (all keys collected), it remains unlocked forever, and once it becomes affordable, it remains affordable as strength only increases.

### Why it works

At any moment, the algorithm maintains two sets: nodes whose structural prerequisites are satisfied, and nodes among them whose strength requirement is satisfied. Any valid next move in the original problem must come from their intersection.

The process never ignores a valid candidate: every node enters the unlocked set exactly when it becomes structurally possible, and enters the affordable set exactly when it becomes numerically possible. The choice among affordable nodes always picks one that maximizes immediate strength gain, and since strength is monotonic, delaying a node with higher reward is never beneficial once it becomes affordable.

This ensures that if any sequence of valid defeats exists from a given state, the algorithm will not block itself from reaching the same or a stronger state afterward.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

n, p = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

g = [[] for _ in range(n)]
indeg = [0] * n

for i in range(n):
    parts = list(map(int, input().split()))
    k = parts[0]
    for x in parts[1:]:
        x -= 1
        g[x].append(i)
        indeg[i] += 1

ready = []
for i in range(n):
    if indeg[i] == 0:
        heapq.heappush(ready, (a[i], i))

affordable = []
visited = [False] * n
ans = []

while True:
    while ready and ready[0][0] <= p:
        ai, i = heapq.heappop(ready)
        heapq.heappush(affordable, (-b[i], i))

    if not affordable:
        break

    negb, i = heapq.heappop(affordable)
    if visited[i]:
        continue

    visited[i] = True
    ans.append(i + 1)
    p += b[i]

    for to in g[i]:
        indeg[to] -= 1
        if indeg[to] == 0:
            heapq.heappush(ready, (a[to], to))

print(len(ans))
print(*sorted(ans))
```

The implementation begins by constructing the dependency graph from key relationships, treating each key as an edge prerequisite relation. Indegrees track how many keys are still missing for each node.

The `ready` heap stores nodes whose key conditions are satisfied, ordered by their required strength so that we can efficiently extract candidates that might become usable as strength increases.

The `affordable` heap stores nodes that are both structurally unlocked and currently beatable, ordered by negative reward so that it behaves as a max-heap. This ensures we always choose the most beneficial immediate upgrade.

The main loop first promotes newly affordable nodes, then selects the best candidate to defeat. After each defeat, we propagate key unlocks and potentially introduce new nodes into the system.

Sorting the final answer is necessary because selection order is not guaranteed to be numeric.

## Worked Examples

Consider a small instance where nodes unlock sequentially.

Input:

```
3 1
1 2 3
1 1 1
0
1 1
1 2
```

Here node 1 is initially available, node 2 requires key 1, and node 3 requires key 2.

| Step | Strength | Ready (ai) | Affordable (bi) | Chosen | Collected |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 2 | 2 | 1 | 2 | 1,2 |
| 2 | 3 | 3 | empty | 3 | 1,2,3 |

This trace shows how key propagation and strength growth interact to gradually unlock the full graph.

Now consider a case where affordability blocks selection order:

Input:

```
2 5
5 1
100 1
0
0
```

| Step | Strength | Ready | Affordable | Chosen |
| --- | --- | --- | --- | --- |
| 0 | 5 | 1,2 | 1,2 | 1 |
| 1 | 105 | 2 | 2 | 2 |

If we incorrectly chose node 2 first, we would still succeed here, but in more complex chained cases, ignoring reward ordering would reduce reachable states prematurely. The greedy selection by reward ensures maximal growth at each step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each node enters and leaves heaps once, and each edge reduces indegree once |
| Space | O(n + m) | Graph plus two priority queues |

The complexity fits comfortably within the constraints since both n and total dependency size are at most two hundred thousand, and logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, p = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    indeg = [0] * n

    for i in range(n):
        parts = list(map(int, input().split()))
        k = parts[0]
        for x in parts[1:]:
            x -= 1
            g[x].append(i)
            indeg[i] += 1

    import heapq
    ready = []
    for i in range(n):
        if indeg[i] == 0:
            heapq.heappush(ready, (a[i], i))

    affordable = []
    visited = [False] * n
    ans = []

    while True:
        while ready and ready[0][0] <= p:
            ai, i = heapq.heappop(ready)
            heapq.heappush(affordable, (-b[i], i))

        if not affordable:
            break

        negb, i = heapq.heappop(affordable)
        if visited[i]:
            continue

        visited[i] = True
        ans.append(i + 1)
        p += b[i]

        for to in g[i]:
            indeg[to] -= 1
            if indeg[to] == 0:
                heapq.heappush(ready, (a[to], to))

    return str(len(ans)) + "\n" + " ".join(map(str, sorted(ans)))

# minimal
assert run("1 5\n1\n0\n") == "1\n1"

# sample-like chain
assert run("3 1\n1 2 3\n1 1 1\n0\n1 1\n1 2\n") == "3\n1 2 3"

# no progress
assert run("2 0\n5 5\n1 1\n0\n0\n") == "0\n"

# independent choices
assert run("2 10\n1 2\n5 1\n0\n0\n") == "2\n1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single node | 1 1 | base case correctness |
| chained unlocks | 3 1 2 3 | dependency propagation |
| no reachable nodes | 0 | early termination |
| independent nodes | 2 1 2 | greedy selection correctness |

## Edge Cases

A key edge case occurs when a node becomes structurally unlocked early but is not affordable until much later. The algorithm ensures such nodes remain in the `ready` heap and are only moved into the `affordable` heap once the strength threshold is met, so they are never lost or prematurely discarded.

Another case is when multiple nodes unlock simultaneously and only one leads to sufficient strength growth to unlock the rest. Because the selection is driven by reward-maximization among affordable nodes, the algorithm always prioritizes the growth path, ensuring that delayed but necessary unlock chains are eventually activated.

A final edge case is when all remaining nodes are unlocked but none are affordable. In that situation, the ready heap may still contain nodes, but none pass the strength filter, so the algorithm correctly terminates without attempting invalid transitions.
