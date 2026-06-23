---
title: "CF 105363D - Connecting Villages"
description: "We are given a network of villages connected by roads, where each road is initially unusable and becomes usable only after a certain number of hours. All roads “unlock” in parallel according to their own schedules. Once a road is unlocked, it can be used permanently."
date: "2026-06-23T15:54:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105363
codeforces_index: "D"
codeforces_contest_name: "XXV Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105363
solve_time_s: 69
verified: true
draft: false
---

[CF 105363D - Connecting Villages](https://codeforces.com/problemset/problem/105363/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a network of villages connected by roads, where each road is initially unusable and becomes usable only after a certain number of hours. All roads “unlock” in parallel according to their own schedules. Once a road is unlocked, it can be used permanently.

The question is to determine the earliest time when the villages become fully reachable from one another using only roads that have already finished unlocking. In graph terms, we want the smallest time $T$ such that if we only keep edges with $h_i \le T$, the resulting graph is connected.

Each test case gives a weighted undirected graph, where weights represent activation times. We are effectively asked to find the minimum threshold on edge weights that makes the graph connected.

The constraints are large: up to $10^5$ vertices and $5 \cdot 10^5$ edges per test case, with a total sum of $10^6$. This immediately rules out anything that recomputes connectivity from scratch for each candidate time, such as repeatedly running a BFS/DFS over all edges for every distinct $h_i$. Even sorting all edges and simulating multiple full graph rebuilds per threshold would be too slow if done naively.

We also need to be careful about a subtle failure case: connectivity is not monotonic in the sense of partial processing if we do not handle edges in increasing order properly.

For example, consider a triangle:

```
0 - 1 (10)
1 - 2 (10)
0 - 2 (100)
```

A naive approach might incorrectly think we need to wait for edge (0,2), but in reality nodes are already connected at time 10 using the first two edges.

The correct answer depends on the structure of the minimum way to connect all nodes, not on any specific path between a fixed pair.

## Approaches

A brute-force strategy would be to simulate time increasing from 1 upward, and at each step check whether the graph formed by all edges with $h_i \le T$ is connected. Each connectivity check costs $O(n + m)$ using DFS or BFS. In the worst case, we may scan up to $10^6$ different time values if weights are dense and large, giving a prohibitive $O(m \cdot \max h)$ or even $O(m^2)$-style behavior depending on implementation. This is far beyond limits.

The key observation is that we do not actually need to check every time. We only care about the moment when enough edges exist to connect all vertices. That is exactly the moment when we have selected a spanning tree using the smallest possible maximum edge weight.

This transforms the problem into a classic minimum bottleneck spanning tree question: among all spanning trees, we want the one that minimizes the maximum edge weight used. The answer is the maximum edge weight in a minimum spanning tree.

Once we recognize this, the solution becomes straightforward. We sort edges by weight and build a spanning tree using a Disjoint Set Union (DSU). As soon as we have connected all vertices, the current edge weight is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m \cdot (n + m))$ | $O(n + m)$ | Too slow |
| Kruskal + DSU | $O(m \log m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We use Kruskal’s idea, but we stop early once connectivity is achieved.

1. Sort all roads by their opening time $h_i$. This ensures we always consider the earliest possible connections first, which is necessary because we want to minimize the time when the graph becomes connected.
2. Initialize a DSU structure where each village starts in its own component. Initially, no villages are connected.
3. Iterate through the sorted edges in increasing order of $h_i$. For each edge $(u, v, h_i)$, attempt to merge the components containing $u$ and $v$. If they are already in the same component, the edge does not change connectivity.
4. After each successful merge, track how many connected components remain. Every successful union reduces this count by one. When the number of components becomes one, all villages are connected.
5. The answer is the current edge’s weight $h_i$, because this is the first moment when the graph becomes fully connected using only edges up to this time.

The key idea is that we are effectively building a spanning forest in order of increasing edge weight, and the moment it becomes a single tree is exactly when connectivity is achieved.

### Why it works

At any time $T$, the set of usable edges is exactly all edges with weight at most $T$. Kruskal’s algorithm processes edges in increasing order and maintains the minimum spanning forest for that prefix. The moment the DSU merges everything into one component, we have found the smallest prefix of edges that connects all vertices.

If connectivity were possible earlier than the current edge weight, that would imply a spanning tree exists using only smaller edges, contradicting the fact that Kruskal always constructs a minimum bottleneck spanning tree. Thus the first time we reach a single component must be the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        n, m = map(int, input().split())
        edges = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            edges.append((w, u, v))

        edges.sort()

        dsu = DSU(n)

        ans = 0
        for w, u, v in edges:
            if dsu.union(u, v):
                ans = w
                if dsu.components == 1:
                    break

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DSU maintains dynamic connectivity as we process edges in increasing order. The `components` counter is critical because it avoids needing a full graph traversal to test connectivity. Each successful union reduces the number of connected components, and once it reaches one, we know the graph is fully connected.

A subtle implementation detail is that we store the last used edge weight as `ans`. This works because edges are processed in non-decreasing order, so the last successful union that completes connectivity gives the correct threshold.

## Worked Examples

### Example 1

Input:

```
3 3
0 1 10
0 2 20
1 2 30
```

| Step | Edge (w,u,v) | Components | Union? | Answer |
| --- | --- | --- | --- | --- |
| Init | - | 3 | - | 0 |
| 1 | (10,0,1) | 2 | Yes | 10 |
| 2 | (20,0,2) | 1 | Yes | 20 |

At weight 10, only edge (0,1) exists, so the graph is not fully connected. At weight 20, edges (0,1) and (0,2) are available and connect all nodes. The DSU reflects this by reaching a single component at the second edge.

### Example 2

Input:

```
4 3
0 1 10
0 2 20
0 3 30
```

| Step | Edge (w,u,v) | Components | Union? | Answer |
| --- | --- | --- | --- | --- |
| Init | - | 4 | - | 0 |
| 1 | (10,0,1) | 3 | Yes | 10 |
| 2 | (20,0,2) | 2 | Yes | 20 |
| 3 | (30,0,3) | 1 | Yes | 30 |

This case shows a star structure where connectivity grows linearly. The answer is the last edge because each node connects through vertex 0 only after its corresponding edge is available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | Sorting edges dominates; DSU operations are near constant amortized |
| Space | $O(n + m)$ | Storage for DSU arrays and edge list |

This complexity fits comfortably within the limits since the total number of edges across all test cases is at most $5 \cdot 10^5$, making sorting and DSU operations efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    backup_stdout = sys.stdout
    sys.stdout = StringIO()

    # assume solve() is defined above in the same module
    solve()

    out = sys.stdout.getvalue()
    sys.stdout = backup_stdout
    return out.strip()

# provided samples
assert run("""2
3 3
0 1 10
0 2 20
1 2 30
4 3
0 1 10
0 2 20
0 3 30
""") == "20\n30"

# minimum case
assert run("""1
2 1
0 1 5
""") == "5"

# chain
assert run("""1
5 4
0 1 1
1 2 2
2 3 3
3 4 4
""") == "4"

# star
assert run("""1
5 4
0 1 10
0 2 10
0 3 10
0 4 10
""") == "10"

# already connected early
assert run("""1
3 3
0 1 100
1 2 1
0 2 50
""") == "50"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes single edge | 5 | minimal connectivity |
| chain graph | 4 | longest path dependency |
| star graph | 10 | simultaneous joins |
| mixed weights triangle | 50 | ordering correctness |

## Edge Cases

One edge case is when the graph is already almost connected and only one edge is missing to complete connectivity. For example:

```
3 3
0 1 100
1 2 1
0 2 50
```

The DSU first connects (1,2) at time 1, then connects (0,2) at time 50, and stops there. The answer is 50 because before that moment node 0 is isolated.

Another case is when all edges have identical weights. The algorithm still processes all edges at that weight, but connectivity is achieved as soon as enough unions happen. For:

```
4 3
0 1 5
1 2 5
2 3 5
```

each union happens at weight 5, and the final merge completes connectivity at 5. The algorithm correctly outputs the common weight since sorting preserves all equal edges together and DSU merges until a single component remains.
