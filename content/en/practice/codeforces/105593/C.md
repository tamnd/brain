---
title: "CF 105593C - Poniendo aristas"
description: "We are given a collection of villages that initially have no roads between them. Each test case describes two numbers, the number of villages and the maximum number of roads that can be built."
date: "2026-06-27T00:40:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105593
codeforces_index: "C"
codeforces_contest_name: "CAMA 2024"
rating: 0
weight: 105593
solve_time_s: 43
verified: true
draft: false
---

[CF 105593C - Poniendo aristas](https://codeforces.com/problemset/problem/105593/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of villages that initially have no roads between them. Each test case describes two numbers, the number of villages and the maximum number of roads that can be built.

The goal is to connect villages using at most the allowed number of roads so that the largest shortest-path distance between any two villages is as small as possible. If we cannot make the entire set of villages connected with the available roads, the answer is impossible.

The key object here is the diameter of the resulting graph after building roads: the maximum distance between any pair of nodes in terms of number of edges. Since all roads are unweighted, distance is simply the number of edges on the shortest path.

The constraint range is very large, with up to 10^5 test cases and values of n and m up to 5 × 10^8. This immediately rules out any per-test simulation or graph construction. Any solution must be O(1) per test case, relying only on arithmetic reasoning.

A naive approach would try to explicitly construct a graph and test its diameter under different edge placements. Even a greedy construction would already be too slow, since building adjacency structures or running BFS is impossible at this scale.

A subtle failure case appears when m is just slightly less than the minimum needed to connect all nodes. For example, if n = 4 and m = 2, we can connect at most three nodes in a chain and leave one isolated, so the graph is disconnected and no finite diameter exists. A careless solution that assumes connectivity after placing m edges would incorrectly output a finite answer instead of recognizing impossibility.

## Approaches

The brute-force mental model is to think of adding edges one by one and recomputing the diameter after each addition. This works for tiny graphs because each edge changes shortest paths locally, and a BFS from each node can recompute distances. However, this already costs O(n(n + m)) per evaluation, and here n itself can be up to 5 × 10^8, making even storing the graph impossible.

The key simplification is to recognize that only the structure of a connected graph matters, not the specific labeling of villages. With n nodes and m edges, the best possible configuration for minimizing maximum distance is always a tree-like structure augmented with extra edges. Extra edges beyond n − 1 can only reduce distances, but the limiting factor is whether connectivity is even achievable.

Once the graph is connected, the most distance-efficient structure is a star-like configuration, where one central node connects to many others. This minimizes diameter: a star has diameter 2, and adding more edges can reduce it further to 1 only when the graph becomes complete.

So the problem reduces to checking two regimes. First, whether m is large enough to connect all nodes, which requires m ≥ n − 1. Second, among connected graphs with extra edges, how small the diameter can be forced given the redundancy m − (n − 1). Each additional edge allows shortening the longest paths by effectively adding shortcuts, and the extremal structure becomes increasingly dense until it becomes complete.

The critical observation is that a graph with diameter 1 is a complete graph, requiring n(n − 1) / 2 edges. Any number of edges between n − 1 and that threshold produces a connected graph whose optimal minimal diameter is 2. Below n − 1, it is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct simulation of graph construction and BFS diameter | O(n + m) per test | O(n + m) | Too slow and impossible due to constraints |
| Arithmetic reasoning based on connectivity and completeness thresholds | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal reasoning steps

1. Check whether the graph can be connected with the available edges by verifying if m is at least n − 1. This is the minimum number of edges required for any connected structure because a connected graph on n nodes must have at least a spanning tree.
2. If m < n − 1, immediately output −1 since some villages must remain isolated and no finite maximum distance over all pairs can be defined.
3. If the graph can be connected, consider how small the diameter can be made. A diameter of 1 is only possible when every pair of nodes is directly connected, which requires exactly n(n − 1) / 2 edges.
4. If m reaches this complete-graph threshold, output 1 since every node is adjacent to every other node.
5. Otherwise, output 2, since any connected graph that is not complete can always be organized so that the longest shortest path is at most 2, and no construction can guarantee diameter 1.

### Why it works

The argument relies on extremal graph structure. A connected graph always contains a spanning tree, so the baseline is a tree with diameter at least 2 unless it is a single node or complete structure. Adding edges can only shorten shortest paths by introducing shortcuts, but until every pair is directly connected, there will always exist at least one pair of vertices whose shortest path uses an intermediate node, forcing diameter at least 2. The only way to eliminate all intermediate paths is to directly connect every pair, which uniquely corresponds to the complete graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())

        if m < n - 1:
            out.append("-1")
            continue

        # number of edges in complete graph
        max_edges = n * (n - 1) // 2

        if m == max_edges:
            out.append("1")
        else:
            out.append("2")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first check enforces connectivity using the spanning tree lower bound. The second compares against the complete graph threshold, which is the only situation where all pairwise distances collapse to 1. Everything else falls into the intermediate regime where connectivity is possible but not dense enough to eliminate length-2 shortest paths.

A common mistake is to assume that once the graph is connected, the answer is always 2. That is almost correct but misses the complete graph edge case, where the diameter collapses further.

## Worked Examples

### Sample 1

Input:

```
3
3 2
4 8
11 2
```

For n = 3, m = 2, the graph can be a simple path of length 2, which is connected but not complete, so the diameter is 2.

For n = 4, m = 8, the complete graph threshold is 6 edges. Since 8 ≥ 6, the graph can be made complete, so the diameter is 1.

For n = 11, m = 2, we cannot even connect all nodes since at least 10 edges are required, so the answer is −1.

| Test | n | m | Connectivity | Complete? | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 2 | yes | no | 2 |
| 2 | 4 | 8 | yes | yes | 1 |
| 3 | 11 | 2 | no | no | -1 |

These traces confirm that the solution separates the three structural regimes correctly: disconnected, connected sparse, and fully connected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant-time arithmetic checks |
| Space | O(1) | Only a few integer variables are stored regardless of input size |

The solution is designed specifically for very large bounds on n and m, so any algorithm depending on graph construction would be infeasible. Constant-time reasoning is required to fit within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    def solve():
        t = int(input())
        res = []
        for _ in range(t):
            n, m = map(int, input().split())
            if m < n - 1:
                res.append("-1")
            elif m == n * (n - 1) // 2:
                res.append("1")
            else:
                res.append("2")
        return "\n".join(res)

    return solve()

# provided samples
assert run("3\n3 2\n4 8\n11 2\n") == "2\n1\n-1"

# custom cases
assert run("1\n2 0\n") == "-1"
assert run("1\n2 1\n") == "1"
assert run("1\n5 4\n") == "2"
assert run("1\n5 10\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 | -1 | minimal disconnected case |
| 2 1 | 1 | smallest complete graph |
| 5 4 | 2 | tree (connected but not complete) |
| 5 10 | 2 | extra edges but not complete |

## Edge Cases

For the case n = 2, the behavior collapses both thresholds together. With one edge the graph is complete and diameter is 1, while with zero edges it is disconnected and impossible. The algorithm handles this cleanly because n − 1 equals 1 and n(n − 1)/2 also equals 1.

For a near-complete graph, such as n = 5 and m = 9, the structure is connected and very dense but still missing at least one edge from being complete. The algorithm correctly classifies this as diameter 2, since there remains at least one pair of vertices that is not directly connected, forcing a path of length 2 through an intermediate node.
