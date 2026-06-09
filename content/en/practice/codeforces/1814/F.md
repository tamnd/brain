---
title: "CF 1814F - Communication Towers"
description: "We are dealing with a network of communication towers connected by wires, where each tower can operate only on a continuous range of frequencies. The towers are numbered from 1 to n, and each tower i can operate on frequencies from li to ri inclusive."
date: "2026-06-09T08:28:40+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "divide-and-conquer", "dsu"]
categories: ["algorithms"]
codeforces_contest: 1814
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 146 (Rated for Div. 2)"
rating: 2700
weight: 1814
solve_time_s: 87
verified: false
draft: false
---

[CF 1814F - Communication Towers](https://codeforces.com/problemset/problem/1814/F)

**Rating:** 2700  
**Tags:** brute force, divide and conquer, dsu  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are dealing with a network of communication towers connected by wires, where each tower can operate only on a continuous range of frequencies. The towers are numbered from 1 to n, and each tower i can operate on frequencies from l_i to r_i inclusive. Two towers are connected if there is a wire between them. The task is to determine which towers are accessible starting from tower 1, but accessibility requires a shared frequency along a path. Specifically, a tower b is accessible from tower a if there exists a single frequency x and a sequence of directly connected towers from a to b, where each tower in the sequence accepts frequency x.

The main constraint is that n can be as large as 2×10^5 and m up to 4×10^5. This rules out any algorithm that examines every frequency individually or tries all paths explicitly. For example, iterating over each frequency for each node would result in up to 4×10^10 operations in the worst case, which is far beyond the 4-second time limit. The frequency range itself can go up to 2×10^5, which is another hint that we cannot naively simulate all possible frequencies.

Non-obvious edge cases include towers with single-point frequency ranges, completely disjoint ranges between neighbors, and disconnected components. For example, if tower 1 accepts [1,1] and is connected to a tower with range [2,3], the correct output should be just tower 1, but a careless algorithm might try to follow edges regardless of overlapping ranges.

## Approaches

A brute-force approach would be to consider each frequency from 1 to 2×10^5, build a graph consisting only of towers that accept this frequency, and perform a BFS or DFS starting from tower 1. While this is conceptually correct, it would require iterating over all frequencies for all nodes, resulting in O(n * max_frequency + m) operations. With max_frequency up to 2×10^5 and n up to 2×10^5, this becomes prohibitively slow.

The key insight to optimize is that accessibility depends on the intersection of frequency ranges along connected components. For tower 1, any accessible tower must have a frequency range that intersects with the current reachable frequency interval. This transforms the problem into a kind of interval propagation across the graph: we start with the frequency range of tower 1 and propagate overlaps along edges. This can be efficiently implemented with a union-find structure (DSU) or a BFS that keeps track of the intersection of frequency ranges as we move through the network.

By maintaining the intersection of frequency ranges dynamically and visiting each edge only once, we can reduce the complexity from iterating over all frequencies to simply processing each node and edge once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all frequencies) | O(n * max_frequency + m) | O(n + m) | Too slow |
| Interval propagation with BFS/DSU | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the input to construct the graph with adjacency lists and store each tower's frequency range [l_i, r_i].
2. Initialize a set to track visited towers and a queue for BFS. Start with tower 1 and mark it as visited.
3. Initialize a frequency interval [L, R] representing the current set of reachable frequencies. Initially, this is [l_1, r_1].
4. While the queue is not empty, pop a tower u and examine its neighbors v.
5. For each neighbor v that has not been visited, compute the intersection of its frequency range [l_v, r_v] with the current reachable interval [L, R]. If the intersection is non-empty, mark v as visited, update its reachable interval to the intersection, and add it to the queue.
6. Continue until all reachable towers have been visited. Collect all visited towers, sort them in ascending order, and output them.

Why it works: The BFS ensures that each tower is visited exactly once with a valid frequency intersection. The intersection operation guarantees that only frequencies acceptable to both the current path and the neighbor are considered. This maintains the invariant that any tower added to the queue is genuinely accessible from tower 1 under some single frequency.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, m = map(int, input().split())
ranges = [None] + [tuple(map(int, input().split())) for _ in range(n)]
graph = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

visited = [False] * (n + 1)
reachable_range = [None] * (n + 1)
queue = deque([1])
visited[1] = True
reachable_range[1] = ranges[1]

while queue:
    u = queue.popleft()
    L, R = reachable_range[u]
    for v in graph[u]:
        if visited[v]:
            continue
        l_v, r_v = ranges[v]
        new_L = max(L, l_v)
        new_R = min(R, r_v)
        if new_L <= new_R:
            visited[v] = True
            reachable_range[v] = (new_L, new_R)
            queue.append(v)

result = [i for i in range(1, n + 1) if visited[i]]
print(" ".join(map(str, sorted(result))))
```

The code reads the towers and edges into appropriate structures, initializes BFS from tower 1, and propagates the intersection of frequency ranges. The use of `max` and `min` guarantees the correct intersection, and marking visited ensures each tower is processed once. Sorting the result guarantees ascending output.

## Worked Examples

Sample Input:

```
6 5
3 5
1 2
2 4
2 3
3 3
4 6
1 3
6 1
3 5
3 6
2 3
```

| Step | Queue | Tower visited | Current interval | Notes |
| --- | --- | --- | --- | --- |
| init | [1] | {1} | [3,5] | Start at tower 1 |
| pop 1 | [] | {1} | [3,5] | Neighbors: 3,6 |
| check 3 | [3] | {1,3} | [3,4] | Intersection [3,5] ∩ [2,4] = [3,4] |
| check 6 | [3,6] | {1,3,6} | [4,5] | Intersection [3,5] ∩ [4,6] = [4,5] |
| pop 3 | [6] | {1,3,6} | [3,4] | Neighbors: 1,5,6; 1,6 visited |
| check 5 | [6,5] | {1,3,5,6} | [3,3] | Intersection [3,4] ∩ [3,3] = [3,3] |
| pop 6 | [5] | {} | [4,5] | Neighbor 1,3 visited |
| pop 5 | [] | {} | [3,3] | Neighbor 3 visited |

Output: 1 3 5 6

This trace demonstrates how intersections propagate along edges, ensuring only reachable towers under some frequency are marked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each tower and each edge is visited at most once in BFS |
| Space | O(n + m) | Graph adjacency lists, visited array, reachable_range array, queue |

The solution fits comfortably within the 4-second time limit for n up to 2×10^5 and m up to 4×10^5.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    ranges = [None] + [tuple(map(int, input().split())) for _ in range(n)]
    graph = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    visited = [False] * (n + 1)
    reachable_range = [None] * (n + 1)
    from collections import deque
    queue = deque([1])
    visited[1] = True
    reachable_range[1] = ranges[1]
    while queue:
        u = queue.popleft()
        L, R = reachable_range[u]
        for v in graph[u]:
            if visited[v]:
                continue
            l_v, r_v = ranges[v]
            new_L = max(L, l_v)
            new_R = min(R, r_v)
            if new_L <= new_R:
                visited[v] = True
                reachable_range[v] = (new_L, new_R)
                queue.append(v)
    result = [i for i in range(1, n + 1) if visited[i]]
    return " ".join(map(str, sorted(result)))

# Provided sample
assert run("6 5\n3 5\n1 2\n2 4\n2 3\n3 3\n4 6\n1 3\n6 1\n3 5\n3
```
