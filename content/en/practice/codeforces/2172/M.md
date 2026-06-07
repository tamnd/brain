---
title: "CF 2172M - Maximum Distance To Port"
description: "We have a network of cities connected by roads, where each road is exactly one kilometer long. Each city produces one type of agricultural product, and city 1 is a central port."
date: "2026-06-07T22:59:57+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2172
codeforces_index: "M"
codeforces_contest_name: "2025 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1300
weight: 2172
solve_time_s: 77
verified: true
draft: false
---

[CF 2172M - Maximum Distance To Port](https://codeforces.com/problemset/problem/2172/M)

**Rating:** 1300  
**Tags:** graphs, shortest paths  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a network of cities connected by roads, where each road is exactly one kilometer long. Each city produces one type of agricultural product, and city 1 is a central port. The goal is to find, for each product type, the worst-case distance that a city producing that product has to travel to reach the port. In other words, for product type $i$, we need the maximum among the shortest distances from all cities producing $i$ to city 1.

The input gives the number of cities $n$, roads $m$, and product types $k$, followed by a list of length $n$ indicating the product of each city. The next $m$ lines describe bidirectional edges. The graph is guaranteed to be connected, so every city can reach city 1. The output is a single line of $k$ integers where the $i$-th integer is the maximum distance for product $i$.

The constraints indicate we can have up to $2 \times 10^5$ cities and edges. A naive approach that computes shortest paths from each city to the port individually would take $O(n + m)$ per city, resulting in $O(n(n + m))$, which is too slow. This implies we need a single pass over the graph to compute distances efficiently. Because all edges have equal length, breadth-first search (BFS) is ideal, as it produces shortest paths in unweighted graphs in linear time.

A subtle edge case arises when multiple cities produce the same product, especially when one of them is city 1. For example, if city 1 produces product 3, the maximum distance for that product should be 0, even if other cities also produce it. Another edge case occurs when a product type is produced by only one city; our algorithm must still correctly compute its distance.

## Approaches

The brute-force approach computes the shortest path from each city producing a product to city 1 using BFS or Dijkstra. We would then take the maximum distance for each product. This works because BFS guarantees the shortest paths in an unweighted graph. However, in the worst case where all $n$ cities produce the same product, we would perform $n$ BFS traversals, each taking $O(n + m)$, leading to $O(n(n + m))$, which is far beyond the acceptable limit for $n = 2 \times 10^5$.

The optimal approach exploits the symmetry of shortest paths in an unweighted graph. Instead of starting a BFS from every city, we start a single BFS from the port city 1. BFS computes the shortest distance from city 1 to all other cities in $O(n + m)$. After this, we can simply iterate over all cities and, for each product type, track the maximum distance seen among the cities producing that product. This reduces the work from $O(n(n + m))$ to a single $O(n + m)$ BFS plus a linear scan over the cities, which fits comfortably within the time constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n(n + m)) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m + k) | Accepted |

## Algorithm Walkthrough

1. Parse the input to read the number of cities $n$, roads $m$, and product types $k$. Also read the list of products produced by each city.
2. Construct an adjacency list for the graph using the road information. This representation allows efficient traversal of neighbors during BFS.
3. Initialize a distance array of size $n + 1$ with a sentinel value (e.g., $-1$) to indicate unvisited cities. Set the distance for city 1 to 0.
4. Perform BFS starting from city 1. Use a queue to process cities layer by layer. For each city dequeued, check all neighbors; if a neighbor is unvisited, set its distance to the current city’s distance plus one and enqueue it.
5. After BFS, the distance array contains the shortest distance from city 1 to every other city.
6. Initialize a result array of size $k + 1$ with zeros. Iterate over all cities; for the product type of the city, update the corresponding result entry to the maximum of its current value and the city's distance.
7. Print the results for product types $1$ to $k$.

Why it works: BFS guarantees that when a city is visited for the first time, we have found the shortest path to it from the starting city. Tracking the maximum distance for each product type correctly identifies the farthest city producing that product. Since all edges have equal weight, BFS correctly computes the shortest distances, ensuring the result is accurate.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

n, m, k = map(int, input().split())
products = list(map(int, input().split()))

# Build adjacency list
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

# BFS from city 1
dist = [-1] * (n + 1)
dist[1] = 0
queue = deque([1])

while queue:
    u = queue.popleft()
    for v in graph[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            queue.append(v)

# Track maximum distances per product type
res = [0] * (k + 1)
for i in range(n):
    p = products[i]
    res[p] = max(res[p], dist[i + 1])

print(" ".join(str(res[i]) for i in range(1, k + 1)))
```

The adjacency list allows $O(1)$ neighbor lookups. BFS uses a queue to guarantee that cities are visited in order of increasing distance from the port. The final loop correctly maps cities to their product type and updates the maximum distance seen. The `i + 1` indexing converts zero-based array positions to one-based city numbers.

## Worked Examples

**Sample 1**

Input:

```
3 3 2
2 1 1
1 2
3 1
3 2
```

| City | Product | Distance from 1 | Max per Product |
| --- | --- | --- | --- |
| 1 | 2 | 0 | 2 → max(0,0)=0 |
| 2 | 1 | 1 | 1 → max(0,1)=1 |
| 3 | 1 | 1 | 1 → max(1,1)=1 |

Output:

```
1 0
```

Explanation: Product 1 is produced by cities 2 and 3, both at distance 1, so max is 1. Product 2 is only city 1, distance 0.

**Sample 2 (constructed)**

Input:

```
5 4 3
1 2 3 1 2
1 2
2 3
3 4
4 5
```

| City | Product | Distance | Max per Product |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 → 0 |
| 2 | 2 | 1 | 2 → 1 |
| 3 | 3 | 2 | 3 → 2 |
| 4 | 1 | 3 | 1 → 3 |
| 5 | 2 | 4 | 2 → 4 |

Output:

```
3 4 2
```

This trace confirms that the algorithm correctly computes maximum distances for multiple cities per product type and handles non-consecutive city numbering in the BFS.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | BFS visits each city once and iterates over each edge once. Final loop over cities is O(n). |
| Space | O(n + m + k) | Adjacency list takes O(n + m). Distance array O(n). Result array O(k). Queue at most O(n). |

With $n, m \le 2 \times 10^5$, this is comfortably under 1-second runtime and uses less than 256 MB memory.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    products = list(map(int, input().split()))
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    dist = [-1] * (n + 1)
    dist[1] = 0
    queue = deque([1])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    res = [0] * (k + 1)
    for i in range(n):
        p = products[i]
        res[p] = max(res[p], dist[i + 1])
    return " ".join(str(res[i]) for i in range(1, k + 1))

# Provided
```
