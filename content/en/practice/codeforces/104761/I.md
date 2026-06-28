---
title: "CF 104761I - \u0418\u0433\u0440\u0430 \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435"
description: "We are given a tree with $n$ vertices. One player first selects a vertex $u$, then an adversary selects a different vertex $v$. After that, a vertex $w$ is chosen uniformly at random from all $n$ vertices."
date: "2026-06-29T02:27:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104761
codeforces_index: "I"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104761
solve_time_s: 108
verified: false
draft: false
---

[CF 104761I - \u0418\u0433\u0440\u0430 \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435](https://codeforces.com/problemset/problem/104761/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices. One player first selects a vertex $u$, then an adversary selects a different vertex $v$. After that, a vertex $w$ is chosen uniformly at random from all $n$ vertices.

The outcome is decided by comparing distances in the tree: if $w$ is closer to $u$ than to $v$, the first player wins; if it is closer to $v$, the second player wins; otherwise it is a tie.

The first player wants to choose $u$ so that even after the second player responds optimally with $v$, the probability that a random vertex is closer to $u$ is as large as possible. The second player is adversarial and will always choose $v$ to minimize this probability. If multiple vertices $u$ achieve the same best guaranteed probability, we output the smallest index.

The tree size across all test cases can be up to $2 \cdot 10^5$, so any solution must be essentially linear per test case. This rules out any strategy that tries all pairs $(u, v)$ and evaluates probabilities explicitly, since that would lead to quadratic or worse behavior per tree.

A subtle difficulty is that the probability depends on global geometry: changing $v$ affects distances to all vertices in a non-local way. A naive approach that recomputes distances from both $u$ and $v$ for every pair would repeatedly traverse the entire tree and fail immediately on large inputs.

Another potential pitfall is assuming the second player only considers neighbors of $u$. That is not correct, since a far vertex $v$ can shift large portions of the tree into being closer to $v$ than to $u$, especially along long paths.

## Approaches

A direct approach fixes $u$, then tries all $v \neq u$, computes for each pair how many vertices satisfy $d(u,w) < d(v,w)$, and takes the worst case. Computing this value for a single pair requires reasoning about all vertices, so even with BFS from both endpoints, each evaluation costs $O(n)$. This leads to $O(n^3)$ over all choices of $u$, which is far beyond limits.

The key structural observation is that for a fixed $u$, the adversary does not need to carefully balance distances across the tree. Instead, it is always beneficial for them to pick $v$ inside a region of the tree that is already “far” from $u$. Intuitively, once $v$ is placed in a large subtree away from $u$, most vertices in that subtree become closer to $v$ than to $u$, and moving $v$ deeper into that subtree only strengthens this effect.

This turns the problem into a structural balance condition on the tree. The quality of a vertex $u$ is governed by how evenly it splits the tree into components when removed. If one component is large, the adversary can choose $v$ inside it and force most vertices to favor $v$. If all components are small, no matter where $v$ is placed, it cannot dominate the majority of vertices. This is exactly the notion of a centroid.

So the problem reduces to finding a centroid of the tree, with the additional requirement of choosing the smallest-index centroid if there are two.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all $(u,v)$ pairs | $O(n^3)$ | $O(n)$ | Too slow |
| Centroid of the tree | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Root the tree arbitrarily, for convenience vertex $1$. Compute subtree sizes using a DFS. This gives, for each node, the size of the component “below” it in the rooted tree.
2. For each vertex $u$, compute the size of the largest connected component that remains if $u$ is removed. This consists of each child subtree of $u$, plus the “parent side” which has size $n - \text{subtree}(u)$.
3. Identify the minimum possible value of this maximum component size across all vertices. A vertex achieving this minimum is a centroid.
4. If multiple vertices achieve the same minimum, choose the one with the smallest index.

The reason this works is that the adversary’s optimal strategy effectively concentrates mass in one component of the tree relative to $u$. The worst component size determines how much of the tree can be “captured” against $u$, so minimizing that maximum component size directly maximizes the first player’s guaranteed share of favorable vertices.

### Why it works

For a fixed $u$, consider any choice of $v$. The vertices that prefer $v$ form a region that always contains the entire component of $v$ when the tree is split at $u$, except for vertices near the boundary of the path between $u$ and $v$. This boundary effect cannot outweigh the fact that one entire component is biased toward $v$.

Thus the adversary’s best move is to select $v$ inside the largest component created by removing $u$, because that maximizes the number of vertices whose shortest path structure favors $v$. The guaranteed performance of $u$ is therefore controlled by its largest component size, and maximizing the minimum-case win probability is equivalent to minimizing this quantity, which defines the centroid.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            g[a].append(b)
            g[b].append(a)

        parent = [-1] * n
        order = []
        stack = [0]
        parent[0] = -2

        while stack:
            v = stack.pop()
            order.append(v)
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                stack.append(to)

        sz = [1] * n
        for v in reversed(order):
            for to in g[v]:
                if to == parent[v]:
                    continue
                sz[v] += sz[to]

        best = n + 1
        ans = 0

        for v in range(n):
            mx = n - sz[v]
            for to in g[v]:
                if to == parent[v]:
                    continue
                mx = max(mx, sz[to])
            if mx < best or (mx == best and v < ans):
                best = mx
                ans = v

        print(ans + 1)

if __name__ == "__main__":
    solve()
```

The solution first constructs the tree and runs a DFS-style traversal to establish a parent relationship and compute subtree sizes. The iterative stack is used instead of recursion to avoid recursion depth issues on long chains.

After that, each vertex is evaluated as a potential centroid candidate. The value $n - \text{subtree}(v)$ represents the size of the component above $v$, while each child subtree contributes a potential component if $v$ is removed. The maximum among these is computed and minimized.

A common implementation mistake is forgetting the parent-side component, which leads to underestimating the true maximum component size and incorrectly selecting nodes deep in a large branch.

## Worked Examples

### Example 1

Consider a small tree shaped like a line: $1 - 2 - 3 - 4 - 5$.

| node | parent-side | max child subtree | max component |
| --- | --- | --- | --- |
| 1 | 4 | 0 | 4 |
| 2 | 3 | 1 | 3 |
| 3 | 2 | 2 | 2 |
| 4 | 3 | 1 | 3 |
| 5 | 4 | 0 | 4 |

The minimum maximum component size is $2$, achieved at node $3$. This node splits the tree most evenly, so it is the best starting choice for the first player.

### Example 2

Consider a star centered at $1$ with leaves $2,3,4,5$.

| node | parent-side | max child subtree | max component |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 4 | 0 | 4 |
| 3 | 4 | 0 | 4 |
| 4 | 4 | 0 | 4 |
| 5 | 4 | 0 | 4 |

Node $1$ is clearly optimal, since removing it produces only singleton components. Any other choice allows the adversary to capture almost the entire tree by choosing $v=1$.

These examples show that the optimal vertex is determined purely by how balanced its removal makes the tree, not by local degree or position in a traversal order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each edge is processed a constant number of times during DFS and centroid evaluation |
| Space | $O(n)$ | Adjacency list, parent array, subtree sizes |

The sum of $n$ across test cases is at most $2 \cdot 10^5$, so a linear solution over all tests is sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    import builtins
    output = io.StringIO()
    sys.stdout = output

    # assume solution is in solve()
    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# sample
assert run("1\n2\n1 2\n") in ["1", "2"]

# star
assert run("1\n5\n1 2\n1 3\n1 4\n1 5\n") == "1"

# line
assert run("1\n4\n1 2\n2 3\n3 4\n") == "2"

# balanced tree
assert run("1\n7\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| star | 1 | centroid at hub in highly unbalanced structure |
| line | 2 | correct handling of path-shaped trees |
| balanced tree | 1 | tie-breaking and centroid correctness |

## Edge Cases

A key edge case is a long chain where the centroid is not unique. For a path of even length, two central vertices both minimize the maximum component size. The algorithm handles this correctly by selecting the smallest index among them.

Another case is a star graph where all leaves look symmetric except for index ordering. The computation ensures all leaves have large maximum components, while the center has minimal value, so the center is always selected regardless of indexing.

Finally, skewed trees with one deep chain attached to a dense subtree still behave correctly because the parent-side component size captures the full weight of the heavy branch, preventing incorrectly chosen deep nodes from being selected.
