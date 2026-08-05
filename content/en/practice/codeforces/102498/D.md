---
title: "CF 102498D - \u041f\u043e\u0431\u0435\u0433 \u0441 \u0433\u043e\u0440\u043d\u043e\u0439 \u0431\u0430\u0437\u044b"
description: "We have a rooted tree of mountain clearings. Clearing 1 is the root, and every other clearing has exactly one parent that is higher on the mountain."
date: "2026-08-06T04:22:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102498
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102498
solve_time_s: 79
verified: true
draft: false
---

[CF 102498D - \u041f\u043e\u0431\u0435\u0433 \u0441 \u0433\u043e\u0440\u043d\u043e\u0439 \u0431\u0430\u0437\u044b](https://codeforces.com/problemset/problem/102498/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree of mountain clearings. Clearing `1` is the root, and every other clearing has exactly one parent that is higher on the mountain. Movement is only from a node to one of its children, so a clearing can reach a helicopter exactly when some helicopter is placed in its subtree.

The task is to choose locations for `k` helicopters so that the number of clearings that have at least one chosen node below them is as large as possible. The input gives the parent of every node from `2` to `n`, and the output is the maximum possible number of clearings that can reach a helicopter.

The constraint `n <= 300000` completely changes the type of solution we can use. A dynamic programming solution that keeps information about many subtrees or many choices will usually be too large. Even `O(n log n)` is comfortable, while approaches close to `O(nk)` or `O(n^2)` are impossible because the tree can contain hundreds of thousands of vertices.

A few details make naive thinking dangerous. The first trap is choosing arbitrary internal vertices. A helicopter placed at an internal vertex can always be moved deeper into one of its descendant leaves without losing any covered clearing, because every ancestor that could reach the old position can also reach the deeper one. The second trap is assuming that the deepest `k` vertices by depth are enough by themselves. The score is not the sum of depths because different helicopters share paths to the root. For example, two helicopters placed in different branches may cover much more than two helicopters on the same long path.

Consider the input:

```
5 1
1 2 3 4
```

The tree is a chain of five nodes. With one helicopter, placing it at node `5` covers every clearing, so the answer is `5`. A method that only counts leaves incorrectly as one possible covered node would fail here.

Another important case is a star:

```
5 2
1 1 1 1
```

There are four leaves below the root. Two helicopters can cover the root and the two chosen leaves, giving answer `3`. A method that simply adds the depths of the two chosen leaves would count `2`, while the real answer is larger because the root is shared.

The last edge case is when there are fewer useful destinations than helicopters. In a chain, after placing one helicopter at the bottom, every additional helicopter contributes nothing. The algorithm must allow zero additional contribution instead of assuming every helicopter increases the answer.

## Approaches

A direct approach is to try every possible set of helicopter positions and calculate how many ancestors are covered. This is correct because it examines every valid placement. However, even choosing `k` positions among `n` nodes already gives an enormous search space. For a tree with `300000` vertices, this is far beyond what can be explored.

A more practical first improvement is to observe that helicopters should be placed in leaves. If a helicopter is in an internal node, moving it to any descendant leaf preserves all covered nodes and possibly covers more. This transforms the problem into selecting paths from leaves to the root.

A common next idea is dynamic programming over selected leaves. For small trees, we can store which leaves have already been chosen and how much overlap their paths have. The problem is that the number of leaves can also be large, so the state space becomes too expensive.

The key observation is that the best next helicopter location can always be found by looking at the deepest currently uncovered vertex. Imagine that the deepest vertex `v` is not selected. Follow the path from `v` toward the root until reaching the first vertex that is already covered by a chosen helicopter. Replacing that chosen helicopter with `v` cannot decrease the answer, because the replacement covers the same shared path above that meeting point and also covers the extra suffix ending at `v`. Thus there is always an optimal solution containing the deepest available vertex.

After selecting that vertex, every vertex on its path to the root becomes covered and can be ignored for future choices. The same argument applies again to the remaining uncovered parts of the tree. Repeating this process `k` times gives the optimal greedy construction.

The remaining challenge is implementing this process efficiently. Repeatedly walking from a deepest vertex to the root would cost `O(nk)`. Instead, process vertices once in decreasing depth order. When a vertex is considered, walk upward only through currently unmarked vertices and mark them immediately. Each vertex is marked at most once, so the total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Dynamic Programming over leaves | Too large for `n = 300000` | Large | Too slow |
| Greedy with disjoint set skipping | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the depth of every clearing while reading the tree. Store the parent of every vertex because later we need to move upward from a vertex toward the root.
2. Sort all vertices by decreasing depth. The first vertices considered are the ones that can give the largest possible new coverage. This order matches the greedy proof because the next helicopter should always be placed at the deepest remaining vertex.
3. Maintain a disjoint set structure over vertices. `find(v)` returns the first unmarked vertex on the path from `v` upward. When a vertex becomes covered, connect it directly to the next vertex above it. This allows already covered sections of the tree to be skipped.
4. For every vertex in the sorted order, repeatedly move upward through unmarked vertices. Count how many vertices are encountered and mark them as covered. This count is the additional number of clearings gained if we place the next helicopter there.
5. Keep all obtained gains. The greedy argument says the gains produced by this simulation are exactly the contributions of the optimal choices. The final answer is the sum of the largest `k` gains.

Why it works:

The invariant is that after several greedy choices, the marked vertices are exactly the clearings covered by the helicopters already placed. The deepest unmarked vertex is always an optimal next choice because any solution that does not use it can replace one of its chosen vertices on the path with this deeper vertex without losing any existing coverage. Therefore every greedy step can be transformed from an arbitrary optimal solution into one that chooses the same vertex. Repeating this exchange argument proves that the sequence of gains produced by the algorithm is optimal. The disjoint set structure only changes the implementation by skipping vertices that are already covered, so it does not affect the greedy choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]

    if n > 1:
        p = list(map(int, input().split()))
        for i, x in enumerate(p, start=2):
            parent[i] = x
            children[x].append(i)

    depth = [0] * (n + 1)
    order = [1]
    for v in order:
        for u in children[v]:
            depth[u] = depth[v] + 1
            order.append(u)

    vertices = list(range(1, n + 1))
    vertices.sort(key=lambda x: depth[x], reverse=True)

    dsu = list(range(n + 1))

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    gains = []

    for v in vertices:
        cur = find(v)
        cnt = 0
        while cur != 0:
            cnt += 1
            dsu[cur] = find(parent[cur])
            cur = find(cur)
        gains.append(cnt)

    gains.sort(reverse=True)
    print(sum(gains[:k]))

if __name__ == "__main__":
    solve()
```

The tree is stored using child lists because we need a traversal from the root to compute depths. The iterative traversal avoids recursion depth problems on a chain of length `300000`.

The sorting step arranges vertices in exactly the order required by the greedy proof. We do not need to explicitly know which vertices are leaves because the exchange argument allows the deepest remaining vertex to be selected directly.

The disjoint set array has a slightly different meaning from the usual connectivity DSU. It stores the next uncovered ancestor. When vertex `x` becomes covered, we set `dsu[x]` to the first uncovered vertex above its parent. Future searches skip `x` immediately.

The while loop counts every vertex exactly once over the whole execution. Although it looks like it can walk a path for every vertex, every successful iteration marks a previously unmarked clearing, so the total number of iterations is bounded by `n`.

The answer is obtained from the `k` largest gains. Additional helicopters after all useful paths are covered simply contribute zero, which is why the array of gains may contain many zeros.
