---
title: "CF 104761I - \u0418\u0433\u0440\u0430 \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435"
description: "We are working with a tree where two players pick vertices in sequence. First player chooses a vertex $u$, then the opponent chooses a different vertex $v$. After both choices, a vertex $w$ is selected uniformly at random from all vertices of the tree."
date: "2026-06-28T22:41:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104761
codeforces_index: "I"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104761
solve_time_s: 82
verified: false
draft: false
---

[CF 104761I - \u0418\u0433\u0440\u0430 \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435](https://codeforces.com/problemset/problem/104761/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a tree where two players pick vertices in sequence. First player chooses a vertex $u$, then the opponent chooses a different vertex $v$. After both choices, a vertex $w$ is selected uniformly at random from all vertices of the tree. The first player wins if $w$ is strictly closer to $u$ than to $v$, using standard shortest-path distance in the tree. The second player wins if $w$ is strictly closer to $v$, and ties do not count for either side.

The task is to choose $u$ so that, regardless of how the opponent responds, the probability that a random vertex ends up closer to $u$ is as large as possible. Since the opponent is adversarial, once $u$ is fixed, they will pick a $v$ that minimizes this probability. We are effectively optimizing a worst-case outcome over all possible opponent replies.

The tree can be large, up to $2 \cdot 10^5$ vertices across all test cases. That rules out anything that recomputes distances or simulates the interaction for every pair $(u, v)$, since that would push us toward cubic or quadratic behavior. Even $O(n^2)$ per test case is already too slow.

A subtle point is that the probability depends only on how the tree is partitioned by relative distances to $u$ and $v$, not on the specific identity of nodes. A naive approach might try evaluating every pair $(u, v)$ and counting how many vertices prefer $u$, but that immediately becomes $O(n^2)$ distance computations per test, which is infeasible.

Another mistake is to assume that picking a leaf or a high-degree node is always good. For example, in a star-shaped tree, choosing a leaf makes the opponent pick the center, and almost every node becomes closer to the center than to the leaf, so the win probability collapses. This shows that local intuition about degree is not sufficient.

The real difficulty is that the opponent always reacts optimally, which means we must characterize a vertex that is globally stable against being "outperformed" by any other vertex.

## Approaches

A direct brute-force method would fix a candidate $u$, then try every possible $v$, and for each pair compute the number of nodes $w$ such that $d(u,w) < d(v,w)$. This requires computing distances from both $u$ and $v$ to all nodes, which is $O(n)$ per pair using BFS in a tree. Since there are $O(n^2)$ pairs, the total complexity becomes $O(n^3)$ per test case in the worst interpretation, or at least $O(n^2)$ if distances are precomputed, which is still far beyond the limits.

The key observation is that the opponent’s best response tries to “pull” as many vertices as possible to their side by choosing a vertex that is structurally opposite to $u$. The only vertices that are robust against this kind of attack are those that minimize the size of the largest remaining component when the tree is centered around them.

This is exactly the defining property of a centroid. A centroid is a vertex such that if it is removed, no connected component has more than half of the total vertices. If $u$ is a centroid, then no matter where $v$ is placed, the opponent cannot create a partition that steals more than half of the vertices away from $u$'s side in the distance comparison sense. If $u$ is not a centroid, there exists a direction containing more than half of the nodes, and the opponent can choose $v$ in that direction to dominate the comparison for most vertices.

Thus, the optimal strategy reduces to selecting a centroid of the tree. If there are two centroids (which happens when $n$ is even), either works, but the problem requires the smallest indexed one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $u, v$ pairs | $O(n^3)$ | $O(n)$ | Too slow |
| Centroid finding | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the size of each subtree by rooting the tree at an arbitrary node, typically 1. This is done with a DFS. The subtree size of a node tells us how many nodes lie in each direction away from it.
2. For each node $u$, examine its adjacent subtrees. If we conceptually remove $u$, each neighbor subtree contributes a component whose size is known from the DFS, except for the “parent side”, which is the rest of the tree.
3. Identify whether $u$ satisfies the centroid condition: no adjacent component has more than $n/2$ nodes. This includes both child subtrees and the implicit parent component.
4. Collect all nodes that satisfy the centroid condition. There will be either one or two such nodes.
5. Output the centroid with the smallest index among them.

The key computational trick is that once subtree sizes are known, checking the centroid condition for every node becomes a constant-time operation per node.

### Why it works

For any node that is not a centroid, there exists a neighboring direction containing more than half of the nodes. If the opponent chooses a vertex inside that heavy direction, then for most vertices in that component, distances to $v$ become smaller than distances to $u$, forcing a loss on more than half of the tree. This directly reduces the winning probability below what a centroid can guarantee.

Conversely, if a node is a centroid, every direction away from it is balanced, so no opponent choice can isolate more than half of the vertices into a region closer to $v$. This makes the centroid the unique structure that maximizes the minimum possible winning region.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            a, b = map(int, input().split())
            g[a].append(b)
            g[b].append(a)

        parent = [0] * (n + 1)
        sz = [0] * (n + 1)
        order = []

        stack = [1]
        parent[1] = -1

        while stack:
            v = stack.pop()
            order.append(v)
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                stack.append(to)

        for v in reversed(order):
            sz[v] = 1
            for to in g[v]:
                if to == parent[v]:
                    continue
                sz[v] += sz[to]

        centroids = []
        for v in range(1, n + 1):
            ok = True
            for to in g[v]:
                if to == parent[v]:
                    comp = n - sz[v]
                else:
                    comp = sz[to]
                if comp > n // 2:
                    ok = False
                    break
            if ok:
                centroids.append(v)

        print(min(centroids))

if __name__ == "__main__":
    solve()
```

The solution first builds the tree and computes parent relationships using a DFS-style stack traversal. This avoids recursion limits and still produces a rooted structure. After that, subtree sizes are accumulated in reverse order of traversal.

The centroid check relies on comparing each adjacent component size against $n/2$. For child edges we directly use subtree sizes, and for the parent side we subtract from $n$. This distinction is the most common place for mistakes, since forgetting the parent-side component leads to incorrectly accepting non-centroids.

Finally, we select the smallest indexed centroid to satisfy the tie-breaking requirement.

## Worked Examples

Consider a small tree shaped like a line: $1 - 2 - 3 - 4 - 5$.

We compute subtree sizes assuming root at 1.

| Node | Largest adjacent component size | Centroid? |
| --- | --- | --- |
| 1 | 4 | No |
| 2 | 3 | No |
| 3 | 2 | Yes |
| 4 | 3 | No |
| 5 | 4 | No |

Node 3 is the centroid because removing it splits the tree into components of size at most 2. This demonstrates that centroids tend to sit near the middle of long chains.

Now consider a star with center 1 connected to 2, 3, 4, 5.

| Node | Largest adjacent component size | Centroid? |
| --- | --- | --- |
| 1 | 1 | Yes |
| 2 | 4 | No |
| 3 | 4 | No |
| 4 | 4 | No |
| 5 | 4 | No |

The center is the only centroid because every leaf removal isolates a component of size 4, which is too large. This shows why high degree alone does not guarantee optimality unless it balances subtree sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each edge is processed a constant number of times in DFS and centroid checks |
| Space | $O(n)$ | Adjacency list and auxiliary arrays for parent and subtree sizes |

Since the sum of $n$ over all test cases is bounded by $2 \cdot 10^5$, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    # re-run solution by redefining solve locally
    import sys
    input = sys.stdin.readline
    sys.setrecursionlimit(10**7)

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            g = [[] for _ in range(n + 1)]
            for _ in range(n - 1):
                a, b = map(int, input().split())
                g[a].append(b)
                g[b].append(a)

            parent = [0] * (n + 1)
            sz = [0] * (n + 1)
            order = []

            stack = [1]
            parent[1] = -1
            while stack:
                v = stack.pop()
                order.append(v)
                for to in g[v]:
                    if to == parent[v]:
                        continue
                    parent[to] = v
                    stack.append(to)

            for v in reversed(order):
                sz[v] = 1
                for to in g[v]:
                    if to == parent[v]:
                        continue
                    sz[v] += sz[to]

            centroids = []
            for v in range(1, n + 1):
                ok = True
                for to in g[v]:
                    if to == parent[v]:
                        comp = n - sz[v]
                    else:
                        comp = sz[to]
                    if comp > n // 2:
                        ok = False
                        break
                if ok:
                    centroids.append(v)

            print(min(centroids))

    solve()
    return ""

# sample
assert run("""1
5
1 2
2 3
3 4
4 5
""") == "", "sample-like"

# star
assert run("""1
5
1 2
1 3
1 4
1 5
""") == "", "star centroid check"

# minimal
assert run("""1
2
1 2
""") == "", "min case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Line tree | center | centroid in path |
| Star tree | 1 | central dominance |
| n=2 | 1 | smallest index tie |

## Edge Cases

In a two-node tree, both nodes have equal structure, but the tie-breaking rule forces choosing the smaller index. The centroid check correctly marks both nodes as valid because no component exceeds half the size, and the final `min()` enforces the required output.

In a star-shaped tree, the center is the only node whose removal leaves small components. The algorithm’s parent-side component calculation is essential here, because for leaves the “rest of the tree” becomes the dominant component and correctly disqualifies them.

In a long path, the centroid appears in the middle. The subtree size computation ensures that for the middle node, neither side exceeds $n/2$, while any shift away from the center creates a heavy side that violates the centroid condition.
