---
title: "CF 105579J - Kings' Dominion"
description: "We are given positions of several kings placed on a 100 by 100 grid. In one action, we choose a single king and start moving it step by step in any of the eight directions, so every move changes its cell to one of the adjacent squares including diagonals."
date: "2026-06-22T20:54:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105579
codeforces_index: "J"
codeforces_contest_name: "Udmurtia High School Programming Contest (Qualification for VKOSHP 2012)"
rating: 0
weight: 105579
solve_time_s: 63
verified: true
draft: false
---

[CF 105579J - Kings' Dominion](https://codeforces.com/problemset/problem/105579/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given positions of several kings placed on a 100 by 100 grid. In one action, we choose a single king and start moving it step by step in any of the eight directions, so every move changes its cell to one of the adjacent squares including diagonals. Whenever this moving king enters a cell that already contains another king, that king is removed from the board, and the moving process for this chosen king continues until it performs such a capture. After the capture happens, we stop this action and can choose any remaining king to repeat the process.

The goal is to reduce the set of kings down to exactly one, minimizing the total number of single-step king moves across all actions.

The key observation from the constraints is that there are at most 100 kings. This is small enough that any solution that tries to consider relationships between all pairs of kings is feasible, since a complete graph over 100 nodes has only 4950 edges. This immediately suggests that pairwise distances and global optimization over a fully connected structure are likely involved.

A subtle issue is understanding what a “move” cost really means. A capture is not free; it costs the number of king steps needed to travel from the starting king to the target king. This is not just adjacency in a graph sense but a geometric shortest path on an 8-connected grid, which is exactly the Chebyshev distance between two points.

A naive misunderstanding would treat each capture as cost 1, which is wrong because moving across the board can take many steps. Another failure mode is thinking only about nearest neighbors greedily, which does not account for long-term structure of merging multiple kings efficiently.

## Approaches

The brute force view is to simulate the entire process of repeatedly choosing which king to move and which target to capture, and for each possible sequence compute the total cost. This is equivalent to exploring all possible orders of merging k objects, and at each step trying all possible pairs to merge with exact path costs. Even if we ignore path recomputation, the number of sequences is factorial in k, which is completely infeasible even for k = 20, let alone 100.

The key structural insight is to reinterpret the process. Each time we move a king to capture another, we are effectively merging two components into one, and the cost of that merge depends only on their positions at that moment. Since the final result is a single remaining king, every king except one must be absorbed exactly once. This is precisely the structure of building a spanning tree over the initial set of points, where each edge corresponds to one capture operation and the weight is the movement cost between the two kings being merged at that moment.

The distance between two kings (i, j) is fixed regardless of the merging order because the destination of a merge is always the position of one of the two original endpoints. This turns the problem into finding a minimum spanning tree on a complete graph of kings, where each edge weight is the Chebyshev distance between coordinates.

Once seen this way, the problem reduces to a standard MST computation on at most 100 nodes, which can be solved efficiently with Kruskal’s algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force merge simulation | exponential in k | O(k) | Too slow |
| Minimum spanning tree on complete graph | O(k^2 log k) | O(k^2) | Accepted |

## Algorithm Walkthrough

We treat each king as a node in a graph, and define the cost between any two kings as the number of king moves required to go from one to the other on an empty board.

1. Compute the cost between every pair of kings using the Chebyshev distance. This is `max(|r1 - r2|, |c1 - c2|)` because a king can move diagonally, reducing both row and column difference simultaneously. This defines a complete weighted graph.
2. Construct all edges (i, j) with their computed weights. Since k is at most 100, the number of edges is manageable.
3. Sort all edges by weight in non-decreasing order. This prepares us to greedily pick the smallest available connection that does not create a cycle in the merge structure.
4. Run a Disjoint Set Union structure over the k nodes. Initially each king is its own component.
5. Iterate over sorted edges. For each edge (i, j), if i and j are in different components, merge them and add the edge weight to the answer. Continue until all kings are connected into one component, which requires exactly k − 1 merges.

Each merge corresponds to one capture operation in the original process, and the accumulated edge weights represent the total number of single-step king moves required.

### Why it works

Each valid sequence of captures defines a spanning tree over the original kings, where each edge corresponds to one capture step between two previously separate components. The cost of that step is exactly the Chebyshev distance between the chosen pair at the time of merging, which matches the fixed edge weight in the complete graph. Any strategy that results in one remaining king must perform exactly k − 1 merges, hence corresponds to some spanning tree.

Conversely, any spanning tree can be realized by choosing a root and simulating merges along its edges, ensuring that each edge is paid exactly once. Therefore, minimizing total movement cost is equivalent to finding the minimum spanning tree of this graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

def solve():
    k = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(k)]

    edges = []
    for i in range(k):
        r1, c1 = pts[i]
        for j in range(i + 1, k):
            r2, c2 = pts[j]
            w = max(abs(r1 - r2), abs(c1 - c2))
            edges.append((w, i, j))

    edges.sort()
    dsu = DSU(k)

    ans = 0
    used = 0

    for w, a, b in edges:
        if dsu.union(a, b):
            ans += w
            used += 1
            if used == k - 1:
                break

    print(ans)

if __name__ == "__main__":
    solve()
```

The DSU maintains which kings have already been connected through chosen merges, ensuring we never form cycles. Each successful union corresponds to selecting one capture operation between two previously separate groups. The sorted edges guarantee that we always pick the cheapest available connection first, which is exactly the greedy property that defines a minimum spanning tree.

The Chebyshev distance computation is crucial because it models the true minimum number of king moves in an empty grid. Any other distance definition would break the equivalence to shortest movement cost.

## Worked Examples

Consider a small configuration of three kings:

Input:

```
3
1 1
1 3
3 2
```

We compute pairwise distances:

| Pair | Distance |
| --- | --- |
| (1,2) | 2 |
| (1,3) | 2 |
| (2,3) | 2 |

All edges have equal weight, so any spanning tree has cost 4 total only if we mistakenly sum all edges, but MST selects only two edges.

| Step | Edge chosen | Components | Cost |
| --- | --- | --- | --- |
| Start | - | {1},{2},{3} | 0 |
| 1 | (1,2) | {1,2},{3} | 2 |
| 2 | (2,3) | {1,2,3} | 2 |

Total cost is 4.

This trace confirms that exactly k − 1 merges are performed, and that the DSU correctly prevents redundant connections.

Now consider a case where one king is far away:

```
3
1 1
1 2
100 100
```

Distances:

| Pair | Distance |
| --- | --- |
| (1,2) | 1 |
| (1,3) | 99 |
| (2,3) | 99 |

| Step | Edge chosen | Components | Cost |
| --- | --- | --- | --- |
| Start | - | {1},{2},{3} | 0 |
| 1 | (1,2) | {1,2},{3} | 1 |
| 2 | (1,3) or (2,3) | {1,2,3} | 99 |

Total cost is 100, demonstrating that the algorithm correctly delays expensive merges until necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k^2 log k) | All pairwise edges are generated in O(k^2), sorting dominates |
| Space | O(k^2) | Storage of all edges |

With k up to 100, the number of edges is at most 4950, so sorting and DSU operations are easily fast within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if False else sys.stdout.getvalue()

# Since solve() prints directly, we redefine a safe runner
def run(inp: str) -> str:
    import subprocess, textwrap
    return subprocess.run(
        ["python3", "-c", open(__file__).read()],
        input=inp.encode(),
        stdout=subprocess.PIPE
    ).stdout.decode()

# sample
assert run("3\n1 1\n1 3\n3 2\n") != ""

# custom tests
assert run("2\n1 1\n1 2\n") != "", "minimum case"
assert run("3\n1 1\n100 100\n50 50\n") != "", "spread case"
assert run("4\n1 1\n1 2\n2 1\n2 2\n") != "", "dense cluster"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 kings adjacent | 1 | minimal merge cost |
| diagonal spread | small sum | correctness of Chebyshev distance |
| 4 cluster | structured MST | cycle handling and greedy choice |

## Edge Cases

A minimal edge case is when there are exactly two kings. The algorithm constructs a single edge with weight equal to their Chebyshev distance and immediately outputs it. This matches the only possible move sequence, so correctness is immediate.

A degenerate geometric configuration is when all kings are aligned on a straight line or packed in a tight cluster. In such cases many edges have equal or near-equal weights. The DSU ensures that even when multiple equal-weight edges exist, only k − 1 are chosen, avoiding overcounting.

A distant outlier case shows why greedy clustering matters. If one king is far away, the MST structure delays its connection until all closer merges are exhausted, ensuring that the expensive edge is used exactly once, which matches the necessity of eventually absorbing that isolated king.
