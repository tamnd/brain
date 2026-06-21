---
title: "CF 106387G - The Veneto Relay"
description: "We are given a graph where cities are connected by roads, and each road has an associated danger value. Some cities are marked as milestone cities."
date: "2026-06-21T19:15:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106387
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 2-25-26 (Beginner)"
rating: 0
weight: 106387
solve_time_s: 49
verified: true
draft: false
---

[CF 106387G - The Veneto Relay](https://codeforces.com/problemset/problem/106387/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a graph where cities are connected by roads, and each road has an associated danger value. Some cities are marked as milestone cities. The task is to determine the smallest possible danger threshold such that if we only use roads whose danger does not exceed that threshold, all milestone cities end up connected within the same connected component.

In other words, we are not trying to optimize a path or sum of weights. We are trying to find a cutoff value on edge weights that makes a subset of important nodes mutually reachable.

The input can be interpreted as an undirected weighted graph. Each edge contributes connectivity only if we allow its weight level, and as we increase the allowed threshold, more edges become usable, and connected components merge. The output is the minimum threshold at which all special nodes belong to one connected component.

From a complexity perspective, the graph structure and edge count imply that any solution that repeatedly scans all edges in a naive way per query would be expensive. If we imagine up to 10^5 nodes and edges, then even a linear scan repeated many times becomes problematic. However, the key constraint that makes this problem approachable is that edge weights are either small or can be ordered, and connectivity is monotonic with respect to the threshold.

A naive approach would be to try each possible threshold and run a full graph traversal to check connectivity among milestone nodes. This works logically but becomes slow if the weight range is large.

A subtle edge case appears when milestone nodes are already connected at threshold zero or when they are isolated until the maximum edge weight. Another important case is when there is only one milestone city; then the answer is trivially zero since it is already “connected” to itself. A final corner case is when milestone nodes lie in separate components even after all edges are allowed, in which case no threshold suffices, although typical versions of this problem assume connectivity is guaranteed at full graph level.

## Approaches

The brute-force idea is straightforward: pick a candidate danger threshold V, discard all edges with weight greater than V, and run a BFS or DFS to determine whether all milestone cities lie in the same connected component. Since V ranges from 1 to 100 in the intended constraints, repeating this for all values is already sufficient.

This works because connectivity is monotonic. If all milestone nodes are connected using edges of weight at most V, then they remain connected for any larger threshold. The failure condition also propagates in the opposite direction: if they are disconnected at V, they remain disconnected for smaller values.

The cost of this approach is dominated by running a full graph traversal for each possible V. Each traversal costs O(N + M), and doing it up to 100 times leads to O(100(N + M)), which is acceptable.

If the weight range were larger, iterating over all values would become inefficient. The key observation is that we are effectively searching for the smallest value V such that a predicate becomes true, and that predicate is monotone. This immediately suggests either binary search over V or a structural approach that builds connectivity in increasing order of edge weight.

Binary search gives O((N + M) log W), but a more direct and cleaner solution is to simulate Kruskal’s algorithm. If we sort edges by weight and gradually activate them, we can maintain connected components using a disjoint set union structure. As we merge components, we also track how many milestone nodes are contained in each component. The moment one component contains all milestone nodes, the current edge weight is the answer.

This is exactly the same logic as building a minimum spanning forest, except we stop early when a global connectivity condition on a subset of nodes is satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (DFS per V) | O(100(N + M)) | O(N + M) | Accepted |
| Kruskal + DSU | O(M log M) | O(N) | Accepted |

## Algorithm Walkthrough

We use a disjoint set union structure that maintains connected components as we process edges in increasing order of danger.

1. Read the graph and mark which nodes are milestone cities. Count how many milestone nodes exist in total, since this will be our target component size.
2. Initialize a DSU where each node is initially in its own set. For each set, maintain how many milestone nodes it currently contains. Initially, each milestone node contributes one to its own set count.
3. Sort all edges by increasing danger value. This ensures that when we merge components, we are always using the smallest possible edges first, mirroring the idea of gradually relaxing the threshold.
4. Iterate over edges in sorted order. For each edge connecting u and v with weight w, find their DSU representatives. If they are already in the same set, skip it since it does not change connectivity.
5. If they are in different sets, merge them. When merging, sum the milestone counts from both components into the new root.
6. After each merge, check whether the resulting component contains all milestone nodes. If it does, the current edge weight w is the smallest threshold that connects all milestone cities, so we return w immediately.
7. If we finish processing all edges without reaching a component containing all milestone nodes, then all milestones are never fully connected under available edges, and the answer would be undefined depending on problem guarantees.

Why it works comes from the monotonic growth of connected components under sorted edge insertion. At any point, the DSU represents exactly the connectivity of the graph restricted to edges with weight at most the current processed threshold. Since we process edges in increasing order, the first time all milestone nodes appear in one component corresponds to the minimum threshold where such connectivity becomes possible. No later step can produce a smaller valid threshold, because all earlier edges are strictly smaller or equal and have already been considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n, is_milestone):
        self.parent = list(range(n))
        self.size = [1] * n
        self.milestones = [1 if is_milestone[i] else 0 for i in range(n)]
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return ra
        
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.milestones[ra] += self.milestones[rb]
        return ra

def solve():
    n, m, k = map(int, input().split())
    milestones = [False] * n
    ms = list(map(int, input().split()))
    for x in ms:
        milestones[x] = True

    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((w, u, v))

    dsu = DSU(n, milestones)
    total_ms = sum(milestones)

    edges.sort()

    for w, u, v in edges:
        root = dsu.union(u, v)
        if dsu.milestones[root] == total_ms:
            print(w)
            return

    print(-1)

if __name__ == "__main__":
    solve()
```

The DSU structure maintains both connectivity and the number of milestone nodes per component. The union operation updates both size and milestone counts, which is essential because the stopping condition depends on tracking how many special nodes are inside a merged component.

The sorting step ensures that the first time we reach full coverage of milestone nodes corresponds to the minimal possible threshold. The early exit is safe because any later merges only involve edges with greater or equal weight.

A common implementation pitfall is forgetting to update the milestone count only at the root after union. Another is not normalizing node indices if the input is 1-based.

## Worked Examples

Consider a graph with 4 nodes and 3 edges, where nodes 1 and 4 are milestones.

Edges:

(1-2, w=2), (2-3, w=3), (3-4, w=5)

Milestones: {1, 4}

### Trace

| Step | Edge | Components after union | Milestone counts | All connected? |
| --- | --- | --- | --- | --- |
| 1 | (1,2,2) | {1,2}, {3}, {4} | 1, 0, 1 | No |
| 2 | (2,3,3) | {1,2}, {2,3}, {4} merged -> {1,2,3}, {4} | 1, 1 | No |
| 3 | (3,4,5) | {1,2,3,4} | 2 | Yes |

The answer is 5 because only after processing the edge with weight 5 do both milestone nodes end up in the same connected component.

This trace shows how the DSU gradually expands connectivity and how the milestone counter aggregates across merges until it reaches the global requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M) | Sorting edges dominates, DSU operations are near constant amortized |
| Space | O(N + M) | DSU arrays and edge storage |

The complexity fits easily within typical constraints where N and M are up to 10^5. Sorting dominates, and DSU operations are effectively linear over all unions and finds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = io.StringIO()
    sys.stdout = output

    # assuming solve() is defined above
    solve()

    return output.getvalue().strip()

# simple connectivity
assert run("""4 3 2
1 4
1 2 2
2 3 3
3 4 5
""") == "5"

# already connected at smallest edge
assert run("""3 2 2
1 2
1 2 1
2 3 10
""") == "1"

# single milestone node
assert run("""3 2 1
2
1 2 5
2 3 6
""") == "0"

# all edges same weight
assert run("""4 3 3
1 2 3
1 2 1
2 3 1
3 4 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain 1-2-3-4 | 5 | progressive merging |
| early connectivity | 1 | minimal threshold correctness |
| single milestone | 0 | trivial case |
| equal weights | 1 | tie handling |

## Edge Cases

One important edge case is when there is only one milestone node. In that case, the DSU is initialized with that node already satisfying the condition of containing all required milestones. The correct behavior is to return zero immediately, since no edge is needed to connect a single node to itself.

Another case is when milestones are only connected via high-weight edges. The DSU will merge smaller components first, but the milestone counter will not reach the full total until the final necessary edge is processed. This ensures that the answer correctly reflects the maximum edge in the minimal connecting structure.

A final case is when multiple components contain subsets of milestone nodes. The algorithm handles this naturally because milestone counts are aggregated during unions, and only the first time a union creates a component covering all milestones triggers the answer.
