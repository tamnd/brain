---
title: "CF 102599B - \u041b\u0438\u043f\u0435\u0446\u043a\u043e\u0435 \u043c\u0435\u0442\u0440\u043e"
description: "We are given a metro map with N stations. Each station can specify at most one other station it is connected to. If p[i] is not -1, there is an undirected tunnel between station i and station p[i]."
date: "2026-07-31T16:38:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "B"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 122
verified: true
draft: false
---

[CF 102599B - \u041b\u0438\u043f\u0435\u0446\u043a\u043e\u0435 \u043c\u0435\u0442\u0440\u043e](https://codeforces.com/problemset/problem/102599/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a metro map with `N` stations. Each station can specify at most one other station it is connected to. If `p[i]` is not `-1`, there is an undirected tunnel between station `i` and station `p[i]`. The task is to determine whether there exists a route that visits every station exactly once, moving only through tunnels. If such a route exists, we must output the station order.

The graph has a special structure. Each station contributes at most one edge, so the total number of tunnels is at most `N`. A general Hamiltonian path problem is difficult, but a graph with at most `N` edges is either a tree or a graph consisting of a tree with one extra edge. This restriction is what makes a linear solution possible.

With `N` up to `2 * 10^5`, any solution that tries different starting points, permutations, or exponential backtracking is impossible. We need an algorithm close to `O(N)`, because only a few million operations fit comfortably in the time limit.

The dangerous cases are not just disconnected graphs. A connected graph may still fail because a branching tree cannot be walked through without revisiting a station. For example:

```
4
2 1 1 -1
```

The graph is `3-1-2` with an additional leaf `4` attached to `1`. A route visiting all stations would need to enter station `1` three times, which is impossible. The correct answer is:

```
NO
```

Another tricky case is a cycle with several branches. A cycle alone works, but once too many branches are attached there are not enough free ends in the Hamiltonian path.

## Approaches

A brute-force approach would try to build the route station by station, choosing every possible next station. This is correct because it enumerates every possible Hamiltonian path, but the number of possibilities grows factorially. Even a graph with only a few dozen vertices makes this approach unusable.

The useful observation is that the graph is extremely sparse. A connected graph with at most `N` edges is either a tree or a unicyclic graph. A Hamiltonian path in a tree is only possible when the tree itself is a simple path. In a unicyclic graph, the cycle provides flexibility, but attached trees must also be simple paths, and there can only be enough branches for the route endpoints.

The solution is to classify the graph, extract the cycle if it exists, and then construct the only possible shapes of a Hamiltonian path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph from the given connections and count edges. First check that all stations belong to one connected component, because a single route cannot cross between disconnected parts.
2. If the graph has `N - 1` edges, it is a tree. A tree has a Hamiltonian path only when every vertex has degree at most two. In that case, start from a leaf and walk along the only unused edge each time.
3. If the graph has `N` edges, find the cycle by repeatedly removing leaves. The vertices left after this process form the unique cycle.
4. For every cycle vertex, inspect the trees hanging from it. Each hanging part must itself be a single path. Store that path from its leaf towards the cycle.
5. If there are no hanging paths, the cycle itself is the answer.
6. If there is exactly one hanging path, start from its leaf, reach the cycle vertex, and then continue around the cycle.
7. If there are two hanging paths, they must be attached to adjacent cycle vertices. Start from one leaf, travel through the first branch, go around the cycle without using the edge between those two cycle vertices, and finish through the second branch.
8. Any other structure cannot contain a Hamiltonian path.

The invariant behind the construction is that every internal station of the final route must have exactly two used incident edges, while the two endpoints may have only one. The algorithm rejects every structure where a station would need to be visited from three different directions.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    if n == 1:
        print("YES")
        print(1)
        return

    g = [[] for _ in range(n)]
    edges = 0

    for i, x in enumerate(p):
        if x != -1:
            x -= 1
            g[i].append(x)
            g[x].append(i)
            edges += 1

    seen = [False] * n
    stack = [0]
    seen[0] = True
    while stack:
        v = stack.pop()
        for u in g[v]:
            if not seen[u]:
                seen[u] = True
                stack.append(u)

    if not all(seen):
        print("NO")
        return

    def tree_path():
        for i in range(n):
            if len(g[i]) <= 1:
                start = i
                break
        ans = []
        prev = -1
        cur = start
        while cur != -1:
            ans.append(cur)
            nxt = -1
            for u in g[cur]:
                if u != prev:
                    nxt = u
                    break
            prev, cur = cur, nxt
        return ans

    if edges == n - 1:
        if max(map(len, g)) > 2:
            print("NO")
        else:
            print("YES")
            print(*[x + 1 for x in tree_path()])
        return

    if edges != n:
        print("NO")
        return

    deg = [len(x) for x in g]
    q = deque(i for i in range(n) if deg[i] == 1)
    removed = [False] * n

    while q:
        v = q.popleft()
        removed[v] = True
        for u in g[v]:
            if not removed[u]:
                deg[u] -= 1
                if deg[u] == 1:
                    q.append(u)

    cycle = [i for i in range(n) if not removed[i]]
    cycle_set = set(cycle)

    order = []
    start = cycle[0]
    prev = -1
    cur = start
    while True:
        order.append(cur)
        nxt = -1
        for u in g[cur]:
            if u != prev and u in cycle_set:
                nxt = u
                break
        prev, cur = cur, nxt
        if cur == start:
            break

    def get_branch(c, nxt):
        res = [c]
        prev = c
        cur = nxt
        while True:
            res.append(cur)
            candidates = [u for u in g[cur] if u != prev and u not in cycle_set]
            if len(candidates) > 1:
                return None
            if not candidates:
                break
            prev, cur = cur, candidates[0]
        return res[::-1]

    branches = {}
    bad = False
    for c in cycle:
        arr = []
        for u in g[c]:
            if u not in cycle_set:
                b = get_branch(c, u)
                if b is None:
                    bad = True
                else:
                    arr.append(b)
        if len(arr) > 1:
            bad = True
        if arr:
            branches[c] = arr[0]

    if bad or len(branches) > 2:
        print("NO")
        return

    def rotate_after(x):
        k = order.index(x)
        return order[k + 1:] + order[:k]

    if not branches:
        ans = order
    elif len(branches) == 1:
        c, b = next(iter(branches.items()))
        ans = b + rotate_after(c)
    else:
        c1, c2 = list(branches.keys())
        if c2 not in g[c1]:
            print("NO")
            return
        i = order.index(c1)
        if order[(i + 1) % len(order)] == c2:
            middle = order[i + 2:] + order[:i + 1]
        else:
            middle = order[i - 1:i - len(order):-1]
        ans = branches[c1] + middle + branches[c2][::-1][1:]

    if len(ans) != n:
        print("NO")
    else:
        print("YES")
        print(*[x + 1 for x in ans])

if __name__ == "__main__":
    solve()
```

The implementation first separates the three structural cases: disconnected graphs, trees, and unicyclic graphs. The leaf-removal process is used because repeatedly deleting degree-one vertices removes every tree hanging from the cycle and leaves exactly the cycle vertices.

The branch validation is the subtle part. A branch can only be a chain. If a non-cycle vertex has two unused children, the route would need to split, which is impossible for a single path.

The construction never revisits a station because every part is appended exactly once: first a possible branch, then a section of the cycle, then a possible second branch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every vertex and edge is processed a constant number of times |
| Space | O(N) | The adjacency list, queues, and helper arrays store the graph |

The linear complexity is required for `N = 2 * 10^5`. The algorithm only performs graph traversals and local checks, so it fits easily within the limits.
