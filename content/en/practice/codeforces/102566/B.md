---
title: "CF 102566B - BLAT"
description: "The tree contains a lowercase letter on every vertex. Every ordered pair of vertices defines one string: start at the first vertex, walk along the unique path to the second vertex, and concatenate the letters encountered."
date: "2026-08-07T21:26:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "B"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 61
verified: true
draft: false
---

[CF 102566B - BLAT](https://codeforces.com/problemset/problem/102566/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree contains a lowercase letter on every vertex. Every ordered pair of vertices defines one string: start at the first vertex, walk along the unique path to the second vertex, and concatenate the letters encountered. The task is to find the K-th smallest string among all such ordered paths in lexicographical order.

There are up to 100000 vertices, which means the number of possible paths can reach 10 billion. Enumerating every path or sorting them is impossible. We need to exploit the fact that K is only at most 100000. We only need the beginning of the lexicographical ordering, not the entire set.

A common mistake is to treat paths as undirected. The path from u to v and the path from v to u are different strings because their letters are read in different directions.

For example:

```
2 1
a b
1 2
```

The possible strings are `a`, `b`, `ab`, and `ba`. The answer is `a`, not `ab`, because shorter strings with the same prefix are smaller.

## Approaches

The direct solution is to generate all N² paths, convert each one to a string, sort them, and take the K-th element. A tree traversal can find one path in O(N), so this approach needs O(N³) work in the worst case, which is far beyond the limit.

The useful observation is that K is small. Instead of building the whole sorted list, we can generate paths in lexicographical order using a priority queue. Each queue element represents one already constructed path. Initially, every single vertex is a valid path of length one. When we remove the smallest path, we extend it by one adjacent vertex in every possible direction that does not immediately return to the previous vertex.

This is equivalent to exploring the implicit trie of all valid tree paths. The priority queue always contains the smallest unfinished prefixes, so repeatedly taking the minimum gives the next lexicographical path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N³) | O(N²) | Too slow |
| Priority Queue Enumeration | O((N+K) log(N+K) + S) | O(N+K) | Accepted for K ≤ 100000 |

## Algorithm Walkthrough

1. Insert every single vertex as an initial path in the priority queue. Each of these strings represents a path that starts and ends at the same vertex.
2. Remove the smallest string from the queue. This is the next path in lexicographical order, so count it as one of the answers.
3. If this is the K-th removed string, output it immediately. There is no need to generate the remaining paths.
4. Otherwise, extend the current path through every neighbor of its last vertex except the vertex we came from. Insert those new paths into the queue.

The reason this works is that every valid path has exactly one predecessor obtained by removing its last vertex. The priority queue keeps all possible continuations ordered, so no path can be skipped before a smaller one.

Why it works:

The queue invariant is that it contains every generated path that could become the next answer. When the minimum element is removed, every path not in the queue either has already been output or has a prefix that is still smaller and waiting in the queue. Therefore the removed element is always the next lexicographical path.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    letters = input().split()

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    heap = []

    for i in range(n):
        heapq.heappush(heap, (letters[i], i, -1))

    count = 0

    while heap:
        s, node, parent = heapq.heappop(heap)
        count += 1

        if count == k:
            print(s)
            return

        for nxt in graph[node]:
            if nxt != parent:
                heapq.heappush(heap, (s + letters[nxt], nxt, node))

if __name__ == "__main__":
    solve()
```

The queue stores the current string together with the last two vertices of the path. The previous vertex is necessary because a tree path cannot immediately go backwards, otherwise the same edge would be traversed twice.

The initialization inserts N paths of length one. After a path is removed, all possible one-step extensions are added. The algorithm stops as soon as K paths have been extracted, so it never tries to construct the entire set of paths.

The main implementation detail is keeping the previous vertex. Without it, the expansion would generate invalid walks such as `a b a b a`, which are not simple paths in the tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+K) log(N+K) + L) | Each extracted path creates expansions, and only K paths are removed |
| Space | O(N+K) | The heap stores active candidates |

The solution relies on K being bounded by 100000. Generating only the prefix of the ordering avoids the quadratic number of possible paths.

## Edge Cases

A single vertex tree:

```
1 1
a
```

The only path is `a`, so the answer is `a`. The initial queue already contains the complete answer.

Repeated letters:

```
3 3
a a a
1 2
2 3
```

Many strings compare equally for their first characters. The heap still handles this because the complete strings are compared, not only the first letter.

Directional paths:

```
2 4
a b
1 2
```

The ordered paths are:

```
a
ab
b
ba
```

The last answer is `ba`. Treating the tree as undirected would incorrectly merge `ab` and `ba`. The stored previous vertex keeps the direction of traversal.
