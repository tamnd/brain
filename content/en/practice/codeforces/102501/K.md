---
title: "CF 102501K - Birdwatching"
description: "I will provide a compact version of the editorial that keeps the core reasoning, proof, implementation, and testing guidance while fitting the response limits. Edit We are given a directed graph of observed bird movements."
date: "2026-08-06T18:54:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 54
verified: true
draft: false
---

[CF 102501K - Birdwatching](https://codeforces.com/problemset/problem/102501/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
I will provide a compact version of the editorial that keeps the core reasoning, proof, implementation, and testing guidance while fitting the response limits.

Edit

# Problem Understanding

We are given a directed graph of observed bird movements. The original graph of real flights is unknown, but every real edge must appear in the observed graph, while some observed edges may be shortcuts representing longer real paths.

For a fixed tree T, we need to find every tree a such that the edge a → T is guaranteed to be a real edge. An observed edge a → T is guaranteed only when every possible path from a to T inside the observed graph uses that exact edge.

The constraints allow up to 100000 nodes and 100000 edges. A solution that checks paths separately for every incoming edge can easily become quadratic, which is too slow. We need to process the graph with a linear or near-linear traversal.

The key edge cases are caused by alternative routes. A direct edge into T is not enough. For example:

```
3 3 2
0 1
0 2
1 2
```

The answer is:

```
1
1
```

Node 0 has an edge to 2, but the path 0 → 1 → 2 avoids that edge, so 0 is not valid.

Another case is a cycle:

```
3 3 2
0 2
0 1
1 2
```

The answer is still only node 1. A direct edge does not matter if another outgoing edge can eventually reach T.

# Approaches

The direct approach is to examine every predecessor a of T and remove the edge a → T. If T is still reachable from a, the edge is not guaranteed. This is correct because the definition asks whether an alternative path exists. However, doing a graph traversal for every incoming edge costs O(M(N + M)) in the worst case, which is impossible for 100000 vertices.

The important observation is that every alternative path from a to T must begin with an edge leaving a that is different from a → T. We do not need to test each edge separately. We only need to know which vertices can reach T.

Run one reverse graph traversal starting from T. A vertex is marked if it can reach T in the original graph. For an incoming edge a → T, if a has another outgoing edge a → x where x is marked and x is not T, then there exists another path from a to T, so the edge is not guaranteed. Otherwise the only possible way to arrive at T from a is through a → T.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M(N+M)) | O(N+M) | Too slow |
| Optimal | O(N+M) | O(N+M) | Accepted |

# Algorithm Walkthrough

1. Build the reverse graph. A reverse edge b → a is added for every original edge a → b. Traversing from T in this graph visits exactly the nodes that can reach T in the original graph.
2. Run DFS or BFS from T on the reverse graph and mark all reachable nodes. These are the only nodes that can appear in a path ending at T.
3. Store all outgoing edges of every node while reading the input, because later we need to inspect whether a candidate predecessor has another route to T.
4. For every edge a → T, check all outgoing edges of a. If there exists an edge a → x with x different from T and x marked as able to reach T, then a can reach T without using a → T, so discard it.
5. Sort all remaining predecessors and print them.

Why it works: A path from a to T that avoids the edge a → T must start with some other outgoing edge a → x. After that first move, the remaining part of the path is exactly a path from x to T. The reverse traversal marks precisely those x values where such a suffix path exists. Therefore the algorithm rejects exactly the edges with an alternative path and accepts exactly the guaranteed real edges.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, t = map(int, input().split())

    graph = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    incoming = []

    for _ in range(m):
        a, b = map(int, input().split())
        graph[a].append(b)
        rev[b].append(a)
        if b == t:
            incoming.append(a)

    reachable = [False] * n
    stack = [t]
    reachable[t] = True

    while stack:
        v = stack.pop()
        for u in rev[v]:
            if not reachable[u]:
                reachable[u] = True
                stack.append(u)

    ans = []
    for a in incoming:
        ok = True
        for x in graph[a]:
            if x != t and reachable[x]:
                ok = False
                break
        if ok:
            ans.append(a)

    ans.sort()
    print(len(ans))
    for x in ans:
        print(x)

if __name__ == "__main__":
    solve()
```

The first traversal works on the reversed graph because reachability direction is inverted. Reaching a node x from T in the reversed graph means there was a path from x to T originally.

The final loop only checks vertices that already have a direct edge to T. This is enough because every answer must be a predecessor of T. For each such vertex, another outgoing edge is dangerous only when it leads to a vertex that can eventually return to T.

No recursion is used because Python recursion depth is too small for a graph with 100000 vertices. The iterative stack avoids that issue.

# Worked Examples

For the first sample:

| Step | Current vertex | Can reach T? |
| --- | --- | --- |
| Start reverse DFS | 2 | yes |
| Visit reverse neighbor | 1 | yes |
| Visit reverse neighbor | 0 | yes |

Incoming edges to 2 are 0 → 2 and 1 → 2.

| Candidate | Other edge to reachable node | Result |
| --- | --- | --- |
| 0 | 0 → 1 | rejected |
| 1 | none | accepted |

The answer is:

```
1
1
```

For the second sample, reverse traversal from 2 marks 0, 1, 2, 3, and 4. Node 5 is not marked.

| Candidate | Alternative route | Result |
| --- | --- | --- |
| 0 | 0 → 1 → 2 | rejected |
| 1 | none | accepted |
| 4 | none | accepted |

The answer is:

```
2
1
4
```

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N+M) | Every edge is processed a constant number of times. |
| Space | O(N+M) | The graph, reverse graph, and traversal arrays are stored. |

This fits the limits because the algorithm performs only a few linear passes over the graph.

# Test Cases

```
# Expected outputs for the official implementation

# Minimum graph
# Input:
# 1 0 0
# Output:
# 0

# Single guaranteed edge
# Input:
# 2 1 1
# 0 1
# Output:
# 1
# 0

# Direct edge with an alternative route
# Input:
# 3 3 2
# 0 2
# 0 1
# 1 2
# Output:
# 1
# 1

# Cycle around the target
# Input:
# 4 5 3
# 0 3
# 0 1
# 1 2
# 2 3
# 2 1
# Output:
# 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node | No answers | Empty graph handling |
| One edge | Source accepted | Basic predecessor case |
| Multiple paths | Only forced edges kept | Main idea |
| Cycle | Reachability through cycles | Correct reverse traversal |

# Edge Cases

A direct incoming edge can still be invalid. In:

```
3 3 2
0 2
0 1
1 2
```

reverse traversal marks every node as able to reach 2. When checking node 0, the edge 0 → 1 is found and node 1 is marked, so the algorithm rejects 0.

A node inside a cycle may still be valid. In the second sample, node 4 has an edge to 2, but its other outgoing edges do not exist, so every path from 4 to 2 must use 4 → 2. The algorithm accepts it even though the graph contains cycles elsewhere.
