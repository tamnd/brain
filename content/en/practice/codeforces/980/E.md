---
title: "CF 980E - The Number Games"
description: "We are given a tree with $n$ nodes. Each node represents a district, and the road system guarantees there is exactly one simple path between any two districts."
date: "2026-06-17T01:13:18+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 980
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 480 (Div. 2)"
rating: 2200
weight: 980
solve_time_s: 106
verified: true
draft: false
---

[CF 980E - The Number Games](https://codeforces.com/problemset/problem/980/E)

**Rating:** 2200  
**Tags:** data structures, greedy, trees  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ nodes. Each node represents a district, and the road system guarantees there is exactly one simple path between any two districts. Each district $i$ contributes a value equal to $2^i$, so higher numbered districts are exponentially more valuable than lower numbered ones.

We must remove exactly $k$ districts. After removal, the remaining districts must still form a connected graph under the original roads, meaning you can still travel between any two remaining nodes without passing through removed ones. Among all valid ways to remove $k$ nodes, we want to maximize the sum of $2^i$ over the remaining nodes, which is equivalent to minimizing the impact of removing high-index nodes.

The exponential weights matter because $2^i$ dominates any combination of smaller indices. This implies that the objective is lexicographic in nature: keeping a higher numbered node is always more important than any collection of lower numbered nodes.

The constraints allow $n$ up to $10^6$, so any solution must be close to linear or $O(n \log n)$. A quadratic strategy such as repeatedly recomputing connectivity or simulating deletions with full graph checks would be far too slow.

A subtle point is that not every subset of nodes is allowed. Even if a set of nodes has high total weight, it is invalid if it disconnects the remaining graph. For example, removing a central articulation node early may split the remaining nodes into multiple components, which is forbidden.

Another edge case is when the tree is a star. If node 1 is the center and we remove it too early, all remaining nodes become isolated. For instance, if $n = 4$ and edges are $1$ connected to $2,3,4$, removing node 1 first leaves three isolated nodes, which violates connectivity. So deletions must respect structural constraints, not just value ordering.

## Approaches

A brute-force approach would try all subsets of size $n-k$, check whether the induced subgraph is connected, and compute the sum of weights. Even ignoring connectivity checks, the number of subsets is $\binom{n}{k}$, which is infeasible even for small $n$. A single connectivity check per candidate already costs $O(n)$, making this approach exponential and unusable.

The key observation comes from understanding how connectivity is preserved under deletions in a tree. In a tree, removing a node can disconnect the remaining graph only if that node is an articulation point for the current remaining set. However, in a tree, every node becomes a potential articulation point unless it is a leaf of the current remaining graph.

This leads to a structural simplification: if we want the remaining graph to stay connected throughout deletions, we can only remove nodes that are leaves in the current remaining tree. Removing any internal node would split the remaining vertices into at least two components.

Once we accept that restriction, the problem becomes a greedy process. We repeatedly remove a leaf. Since we want to maximize remaining sum and higher indices are more valuable, we should prefer removing the smallest available leaf at each step. Removing smaller labels first preserves larger labels for as long as possible while maintaining connectivity.

The process can be maintained dynamically using a priority queue of current leaves. Each time we remove a leaf, its neighbor may become a new leaf, and we update accordingly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Leaf-pruning greedy with heap | $O(n \log n)$ | O(n) | Accepted |

## Algorithm Walkthrough

We maintain the current degrees of nodes in the remaining tree and a structure that always gives us the smallest-numbered removable leaf.

1. Compute the degree of every node from the adjacency list. This represents how many active connections each node currently has.
2. Initialize a min-heap containing all nodes whose degree is exactly 1. These are the current leaves, and only these nodes are safe to remove without breaking connectivity.
3. Repeat the following process exactly $k$ times. Each repetition corresponds to removing one node.
4. Extract the smallest indexed node from the heap. This ensures we remove the least valuable node among all currently safe choices, which aligns with minimizing loss of exponential weights.
5. Mark this node as removed. This means it will not appear in the final connected component.
6. For the unique neighbor of this node, reduce its degree by one because the edge to the removed node disappears. If this neighbor’s degree becomes 1 and it is not removed already, it becomes a new leaf and is inserted into the heap.
7. Continue until $k$ nodes have been removed.

After these steps, the remaining nodes form a connected subtree, and the removed nodes are exactly those recorded during the process.

The correctness rests on the invariant that the remaining graph is always connected, and every removal preserves this property because we only remove leaves. Additionally, among all valid sequences of leaf removals, always choosing the smallest label leaf ensures that higher labels are preserved as long as structurally possible, which is optimal due to the exponential weighting.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

n, k = map(int, input().split())
adj = [[] for _ in range(n + 1)]
deg = [0] * (n + 1)

for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)
    deg[a] += 1
    deg[b] += 1

removed = [False] * (n + 1)
heap = []

for i in range(1, n + 1):
    if deg[i] == 1:
        heapq.heappush(heap, i)

ans = []

for _ in range(k):
    while heap:
        v = heapq.heappop(heap)
        if not removed[v]:
            break

    removed[v] = True
    ans.append(v)

    for to in adj[v]:
        if not removed[to]:
            deg[to] -= 1
            if deg[to] == 1:
                heapq.heappush(heap, to)

ans.sort()
print(*ans)
```

The adjacency list stores the tree efficiently, and the degree array tracks how many active edges each node still has as nodes are removed. The heap ensures we always pick the smallest valid leaf in $O(\log n)$ time.

A subtle implementation detail is the lazy deletion in the heap. Nodes may remain in the heap after they stop being valid leaves, so we skip already removed nodes when popping. This avoids expensive heap maintenance.

Sorting the final answer is necessary because removals are generated in process order, not necessarily increasing order.

## Worked Examples

Consider the sample input:

```
6 3
2 1
2 6
4 2
5 6
2 3
```

Initially, leaves are nodes with degree 1: nodes 1, 3, 4, 5. The heap always selects the smallest leaf.

| Step | Heap (conceptual) | Chosen | Removed | Degree changes |
| --- | --- | --- | --- | --- |
| 1 | 1,3,4,5 | 1 | {1} | node 2 degree decreases |
| 2 | 3,4,5 | 3 | {1,3} | node 2 degree decreases |
| 3 | 4,5 | 4 | {1,3,4} | node 2 becomes leaf if degree 1 condition met |

After processing, the removed nodes are $1, 3, 4$, matching the expected output.

This trace shows that the algorithm always deletes safe boundary nodes and never touches internal structure until it naturally becomes a leaf.

As a second example, consider a chain:

```
5 2
1 2
2 3
3 4
4 5
```

Leaves start as 1 and 5. The algorithm removes 1 first, then 5. The remaining graph stays connected because removing endpoints of a path preserves a shorter path.

| Step | Leaves | Chosen | Removed |
| --- | --- | --- | --- |
| 1 | 1,5 | 1 | {1} |
| 2 | 2,5 | 2 | {1,2} |

This demonstrates how internal nodes only become removable after repeated pruning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each node enters and leaves the heap at most once, and each heap operation costs logarithmic time |
| Space | $O(n)$ | adjacency list, degree array, heap, and bookkeeping arrays |

The linearithmic complexity is acceptable for $n \le 10^6$ because each operation is simple and dominated by heap updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    n, k = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)

    for _ in range(n - 1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1

    removed = [False] * (n + 1)
    heap = []

    for i in range(1, n + 1):
        if deg[i] == 1:
            heapq.heappush(heap, i)

    ans = []

    for _ in range(k):
        while heap:
            v = heapq.heappop(heap)
            if not removed[v]:
                break
        removed[v] = True
        ans.append(v)

        for to in adj[v]:
            if not removed[to]:
                deg[to] -= 1
                if deg[to] == 1:
                    heapq.heappush(heap, to)

    ans.sort()
    return " ".join(map(str, ans))

assert run("""6 3
2 1
2 6
4 2
5 6
2 3
""") == "1 3 4"

assert run("""5 2
1 2
2 3
3 4
4 5
""") == "1 2"

assert run("""4 1
1 2
1 3
1 4
""") == "2"

assert run("""7 3
1 2
2 3
3 4
4 5
5 6
6 7
""") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| star tree | 2 | center protection and leaf removal rule |
| path tree | 1 2 | dynamic leaf evolution |
| chain small removal | 2 | heap ordering correctness |
| long chain | 1 2 3 | repeated pruning stability |

## Edge Cases

In a star-shaped tree, only leaves are removable at the start. The algorithm correctly restricts deletions to leaf nodes, so the center is never removed prematurely. For example, with edges $1$ connected to $2,3,4$, the initial heap contains $2,3,4$, and node 1 never enters the heap until it becomes a leaf, which never happens unless all others are removed.

In a long chain, internal nodes gradually become leaves only after endpoints are removed. The algorithm naturally respects this transition because degree updates ensure nodes only enter the heap when structurally valid.

In cases where multiple leaves exist, always choosing the smallest index ensures deterministic removal of lower-value nodes first, which is consistent with the exponential weighting and prevents suboptimal retention of low-index nodes.
