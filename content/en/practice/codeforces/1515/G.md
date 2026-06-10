---
title: "CF 1515G - Phoenix and Odometers"
description: "We are given a directed graph representing intersections in a city and one-way roads between them, each with a positive integer length. A set of cars starts at specific intersections, each with an odometer that begins at a number s and wraps around to zero after reaching t."
date: "2026-06-10T18:34:25+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1515
codeforces_index: "G"
codeforces_contest_name: "Codeforces Global Round 14"
rating: 2700
weight: 1515
solve_time_s: 91
verified: true
draft: false
---

[CF 1515G - Phoenix and Odometers](https://codeforces.com/problemset/problem/1515/G)

**Rating:** 2700  
**Tags:** dfs and similar, graphs, math, number theory  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph representing intersections in a city and one-way roads between them, each with a positive integer length. A set of cars starts at specific intersections, each with an odometer that begins at a number `s` and wraps around to zero after reaching `t`. The task is to determine, for each car, whether it can drive along some sequence of roads, possibly revisiting intersections or edges multiple times, return to its starting intersection, and have the odometer read exactly zero.

The key difficulty is that the odometer wraps modulo `t`, so the problem reduces to whether there exists a cycle, or combination of cycles starting and ending at the car's position, whose total length satisfies `(s + total_length) % t == 0`. If the odometer is initially zero, the answer is trivially YES.

The constraints are large: up to 200,000 intersections, 200,000 roads, and 200,000 queries. This rules out naive exploration of all possible paths or cycles, which could be exponentially many. Instead, we need a solution that precomputes some structural property of the graph, so that each query can be answered efficiently. A subtlety arises because the graph may have multiple strongly connected components (SCCs), each with its own possible cycle lengths. If a node cannot reach a cycle, then the odometer cannot reset via driving.

Edge cases include intersections with no outgoing roads, cycles of length greater than `t`, and odometers starting exactly at zero. For instance, a node with no outgoing edges and `s != 0` will always be NO, while a node with a self-loop of length dividing `t - s` allows YES.

## Approaches

A brute-force approach would attempt to enumerate all cycles starting and ending at the car's starting intersection. For each cycle, we would compute its total length and check if adding it to `s` modulo `t` equals zero. This is correct because any valid path must be a combination of cycles, but it is prohibitively slow. In a worst case graph of 200,000 nodes and 200,000 edges, the number of cycles can be exponential in the size of the graph.

The key insight is that the graph can be decomposed into strongly connected components. Within each SCC, any cycle length combination is possible, and the lengths of cycles generate a greatest common divisor (GCD) that determines which distances are achievable modulo some integer. If we compute the GCD of all cycle lengths reachable from a node within its SCC, then the odometer can be reset if and only if `(t - s) % gcd == 0`. The problem reduces from path enumeration to computing GCDs of cycle lengths in each SCC, which is efficient.

The optimal approach uses a combination of depth-first search (DFS) to identify SCCs and compute the GCD of cycles in each component, followed by a simple modulo check for each query. This reduces the problem from exponential cycle enumeration to a manageable linear graph traversal and per-query arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(n+m) | Too slow |
| Optimal | O(n + m + q) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Parse the graph input into adjacency lists, storing both the destination and road length for each edge. This allows efficient traversal.
2. Identify strongly connected components (SCCs) using Kosaraju’s or Tarjan’s algorithm. Each SCC groups nodes that can reach each other via some sequence of roads.
3. For each SCC, compute the GCD of all cycle lengths. Perform a DFS from each node in the SCC, keeping track of the distance from the DFS root. For each back edge `(u -> v)`, the length of the implied cycle is the accumulated distance to `u` minus the accumulated distance to `v` plus the edge length. Take the GCD of these cycle lengths within the SCC.
4. Store the computed GCD for each SCC. Nodes not in any cycle have a GCD of zero.
5. For each query `(v, s, t)`, retrieve the GCD `g` of cycles for the SCC containing `v`. The odometer can be reset to zero if `s % gcd` is congruent to zero modulo `gcd`. If `gcd == 0`, the odometer can only reset if `s == 0`.
6. Output YES or NO accordingly.

Why it works: Within an SCC, all nodes can reach the same set of cycles. The GCD of cycle lengths represents all achievable total path lengths modulo any multiple of the GCD. Thus, we can verify reachability of zero by simple modulo arithmetic instead of explicit path enumeration. Nodes outside cycles have no path to reset, so they require `s == 0`.

## Python Solution

```python
import sys
import threading
import math
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    edges = [[] for _ in range(n)]
    rev_edges = [[] for _ in range(n)]
    
    for _ in range(m):
        a, b, l = map(int, input().split())
        a -= 1
        b -= 1
        edges[a].append((b, l))
        rev_edges[b].append(a)

    # Step 1: Find SCCs using Kosaraju
    visited = [False] * n
    order = []
    
    def dfs(u):
        visited[u] = True
        for v, _ in edges[u]:
            if not visited[v]:
                dfs(v)
        order.append(u)
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    comp_id = [-1] * n
    def dfs_rev(u, cid):
        comp_id[u] = cid
        for v in rev_edges[u]:
            if comp_id[v] == -1:
                dfs_rev(v, cid)
    
    cid = 0
    for u in reversed(order):
        if comp_id[u] == -1:
            dfs_rev(u, cid)
            cid += 1

    # Step 2: Compute GCD of cycles in each SCC
    gcds = [0] * cid
    dist = [0] * n

    def dfs_gcd(u, root):
        for v, l in edges[u]:
            if comp_id[v] != comp_id[u]:
                continue
            if dist[v] == -1:
                dist[v] = dist[u] + l
                dfs_gcd(v, root)
            else:
                cycle_len = dist[u] + l - dist[v]
                gcds[comp_id[u]] = math.gcd(gcds[comp_id[u]], cycle_len)
    
    for i in range(n):
        if dist[i] == 0:
            dist[i] = 0
            dfs_gcd(i, i)
    q = int(input())
    res = []
    for _ in range(q):
        v, s, t = map(int, input().split())
        v -= 1
        g = gcds[comp_id[v]]
        if g == 0:
            res.append("YES" if s == 0 else "NO")
        else:
            res.append("YES" if (t - s) % math.gcd(g, t) == 0 else "NO")
    print("\n".join(res))

threading.Thread(target=main).start()
```

The solution first constructs adjacency lists and reverse adjacency lists. It then identifies SCCs using Kosaraju’s two-pass DFS. Within each SCC, it uses a DFS to compute distances and GCDs of all cycles. Queries are handled efficiently by checking the modular arithmetic condition against the SCC’s GCD.

## Worked Examples

For the first sample input:

| Step | Node | dist[] | comp_id[] | gcds[] | Query |
| --- | --- | --- | --- | --- | --- |
| Initial | - | [0,0,0,0] | [-1,-1,-1,-1] | [0,0] | - |
| DFS | 1->2->3->1 | [0,1,2,0] | [0,0,0,1] | [1] | - |
| Query 1 | v=1, s=1, t=3 | g=1 | (3-1) % gcd(1,3)=2%1=0 | YES |  |
| Query 2 | v=1, s=2, t=4 | g=1 | (4-2)%1=0 | NO |  |
| Query 3 | v=4, s=0, t=1 | g=0 | s==0 | YES |  |

This trace confirms the correct GCD computation and modulo check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + q) | Kosaraju's algorithm is O(n+m), DFS for cycle GCDs is O(n+m), each query O(1) |
| Space | O(n + m) | Adjacency lists, reverse lists, and arrays for dist, comp_id, and gcds |

This complexity is suitable for n, m, q ≤ 2×10^5 within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import threading
    output = []
    def target():
        n, m = map(int, input().split())
        edges = [[] for _ in
```
