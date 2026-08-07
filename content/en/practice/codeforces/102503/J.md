---
title: "CF 102503J - Mildly Irritated Gandhi"
description: "The islands and bridges form a connected undirected multigraph. Gandhi wants to remove as many bridges as possible while keeping the graph connected."
date: "2026-08-07T20:41:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "J"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 69
verified: true
draft: false
---

[CF 102503J - Mildly Irritated Gandhi](https://codeforces.com/problemset/problem/102503/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The islands and bridges form a connected undirected multigraph. Gandhi wants to remove as many bridges as possible while keeping the graph connected. Removing the maximum number of bridges means the remaining graph must contain exactly the minimum number of edges needed for connectivity, so the remaining bridges form a spanning tree.

Among all possible spanning trees, only those with the maximum possible sum of culture values are valid. For each query, we are given a set of bridge indices and must count how many of those bridges appear in at least one optimal spanning tree.

The input size rules out trying to build spanning trees explicitly. The graph can contain around 133000 bridges, so even an algorithm close to quadratic is impossible. We need a solution based on sorting and near-linear graph processing.

The tricky cases come from equal culture values. If all values were different, a maximum spanning tree would be unique, but equal values can create many valid trees. Another common mistake is treating every edge chosen by one run of Kruskal as the only possible answer. The query asks whether an edge can appear in any maximum spanning tree.

For example:

```
1
3 3
1 2 5
2 3 5
1 3 5
1
3 1 2 3
```

The answer is:

```
3
```

A careless implementation using one Kruskal run would keep only two edges and incorrectly answer 2. Since all edges have equal value, any two form a maximum spanning tree, so every edge is possible.

## Approaches

A brute force solution could enumerate all spanning trees, compute their culture values, keep the maximum value, and then test every query edge against all optimal trees. This is correct because it directly checks the definition, but the number of spanning trees can be exponential. Even generating only subsets of edges gives about (2^b) possibilities, which is already impossible for the largest graphs.

The useful observation is that maximum spanning trees have a greedy structure. Kruskal's algorithm processes edges from larger culture values to smaller ones. For one culture value, edges with larger values have already been fixed. After contracting the components formed by larger edges, every edge of the current value that connects two different components can be included in some optimal spanning tree. Edges whose endpoints are already connected can never appear because a better cycle connection already exists.

So the problem becomes finding every edge that is allowed by Kruskal's algorithm, then answering queries by counting allowed indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(b log b) | O(n + b) | Accepted |

## Algorithm Walkthrough

1. Sort all bridges by decreasing culture value. Maximum spanning trees use the same greedy ordering as Kruskal, but with the largest weights first.
2. Maintain a disjoint set union structure containing the connected components created by all previously processed larger culture values.
3. Process bridges in groups with the same culture value. For each bridge in the group, check whether its two endpoints currently belong to different DSU components. If they do, mark the bridge as possible. The reason is that inside this equal-value layer, any non-loop edge can be chosen as part of a spanning forest.
4. After checking the whole group, merge all endpoints of bridges in that group that connect different current components. These merges represent adding this culture value to the structure before moving to smaller values.
5. For every query, count how many listed bridge indices were marked as possible.

Why it works: The DSU always represents the components that are already connected by strictly larger culture values. An edge that joins two different components at its own weight can replace another edge of the same weight in some maximum spanning tree, so it belongs to at least one optimal solution. An edge inside one DSU component would create a cycle using edges that are no worse, so including it cannot improve the spanning tree and it cannot be required by any optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            self.p[b] = a

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, b = map(int, input().split())
        edges = []

        for i in range(1, b + 1):
            x, y, c = map(int, input().split())
            edges.append((c, x, y, i))

        edges.sort(reverse=True)

        possible = [False] * (b + 1)
        dsu = DSU(n)

        i = 0
        while i < b:
            j = i
            while j < b and edges[j][0] == edges[i][0]:
                j += 1

            for k in range(i, j):
                _, x, y, idx = edges[k]
                if dsu.find(x) != dsu.find(y):
                    possible[idx] = True

            for k in range(i, j):
                _, x, y, _ = edges[k]
                dsu.union(x, y)

            i = j

        q = int(input())
        for _ in range(q):
            data = list(map(int, input().split()))
            cnt = 0
            for idx in data[1:]:
                if possible[idx]:
                    cnt += 1
            ans.append(str(cnt))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sorting step groups equal culture values together because processing one edge at a time would incorrectly allow an equal-weight edge to influence another edge in the same group.

The DSU merge happens after marking the entire group. This ordering is the main implementation detail. If merges were done immediately, later edges with the same culture value could incorrectly appear blocked.

The array `possible` stores the answer to the graph part of the problem. Since the total size of all queries is bounded by the number of bridges, every query can simply scan its listed edges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(b log b) | Sorting dominates, while DSU operations are almost constant amortized time |
| Space | O(n + b) | Stores edges, DSU parents, and possible flags |

The constraints allow about 133000 bridges, so sorting plus DSU processing easily fits the time limit.

## Worked Example

For the sample:

```
4 4
1 3 40
3 4 20
1 2 30
2 4 10
```

The bridges are already ordered by culture.

| Step | Current edge | DSU state | Possible |
| --- | --- | --- | --- |
| 40 | 1-3 | {1,3} merged | edge 1 |
| 30 | 1-2 | {1,2,3} merged | edge 3 |
| 20 | 3-4 | {1,2,3,4} merged | edge 2 |
| 10 | 2-4 | same component | no |

The valid bridges are 1, 2, and 3. The first query contains edges 2 and 4, so only edge 2 is possible and the answer is 1. The second query contains edges 2 and 3, both possible, so the answer is 2.

## Edge Cases

Self-loops are automatically rejected because both endpoints always have the same DSU representative.

Parallel bridges are handled correctly because bridges are identified by their indices, not by their endpoints. Two bridges connecting the same islands can have different answers if their culture values differ.

A graph where every bridge has the same culture value is also handled correctly. The first DSU pass sees every edge between different components as possible, which matches the fact that every edge can belong to some spanning tree.
