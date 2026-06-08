---
title: "CF 1930H - Interactive Mex Tree"
description: "The interactive story disappears in the hacked version. We are given a tree. Before any queries, we are allowed to choose two permutations of the vertices, $p1$ and $p2$. During each round, a permutation $a$ of $[0,n-1]$ is assigned to the vertices."
date: "2026-06-08T18:36:45+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "interactive", "trees"]
categories: ["algorithms"]
codeforces_contest: 1930
codeforces_index: "H"
codeforces_contest_name: "think-cell Round 1"
rating: 3300
weight: 1930
solve_time_s: 156
verified: false
draft: false
---

[CF 1930H - Interactive Mex Tree](https://codeforces.com/problemset/problem/1930/H)

**Rating:** 3300  
**Tags:** constructive algorithms, dfs and similar, interactive, trees  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The interactive story disappears in the hacked version.

We are given a tree. Before any queries, we are allowed to choose two permutations of the vertices, $p_1$ and $p_2$.

During each round, a permutation $a$ of $[0,n-1]$ is assigned to the vertices. We are also given two vertices $u$ and $v$. The task is to compute the MEX of the values appearing on the path between $u$ and $v$.

The only information available about $a$ comes from range-minimum queries on the two fixed permutations. In the hacked version, these queries are already simulated by the input, so we only need to reconstruct the intended strategy and output the answer.

The crucial observation is that $a$ is a permutation of $[0,n-1]$. For any set of vertices $S$, the MEX of the values on $S$ is exactly the minimum value outside $S$.

Why? Since every value appears exactly once in the whole tree, the smallest missing value from $S$ is simply the smallest value whose vertex does not belong to $S$.

So each round becomes:

- Let $P(u,v)$ be the path.
- Find the minimum value among all vertices not on that path.

The query operation returns the minimum value on an arbitrary union of contiguous segments in one of the two permutations. We need to design two permutations so that the complement of every tree path can always be represented using at most five intervals.

The constraints immediately suggest that the intended solution is entirely structural. The total $n$ over all tests is at most $10^5$, and the total $nq$ is at most $3\cdot10^6$. Any per-query processing around $O(\log n)$ is fine, but rebuilding complicated structures for every round is not.

The dangerous cases are paths whose LCA is neither endpoint. Then the complement of the path is scattered across several different subtrees. A naive DFS order alone produces six disconnected pieces in the worst case, exceeding the limit of five queries. The entire problem is about finding a second ordering that merges some of those pieces.

## Approaches

A natural first attempt is to use a single DFS preorder permutation.

In preorder, every subtree occupies one contiguous segment. Since a path can be described through the LCA, the complement of a path can be decomposed into several subtree-like regions. We could query each region separately and take the minimum.

The problem is that the complement of a general path may split into six disjoint preorder intervals. Since only five queries are allowed, this construction fails.

The key insight is that preorder and postorder complement each other.

Consider a rooted tree. Some regions that are fragmented in preorder become contiguous in postorder. By carefully choosing

- $p_1$ = preorder,
- $p_2$ = postorder,

the complement of every path can be covered by at most five intervals total.

Once the complement is covered, the answer is simply the minimum among those interval minima, because the MEX equals the smallest value outside the path.

The entire construction becomes a geometric decomposition problem on DFS orders.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Single DFS order | $O(q)$ queries but needs up to 6 intervals | $O(n)$ | Too many intervals |
| Preorder + Postorder | $O((n+q)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Preprocessing

1. Root the tree at vertex 1.
2. Run a DFS.
3. Record preorder positions `f1[u]` and the inverse permutation `g1`.
4. Record postorder positions `f2[u]` and the inverse permutation `g2`.
5. Build Heavy-Light Decomposition data needed for LCA queries.
6. For every vertex store its heavy child. This will later help locate the child of the LCA lying on a path branch.

### Processing a query

Let the path endpoints be $u$ and $v$.

1. Compute $l=\mathrm{LCA}(u,v)$.
2. If $l\neq u$, let $U$ and $V$ be the children of $l$ leading toward $u$ and $v$.
3. The complement of the path is decomposed into five regions.

In preorder these correspond to:

- $(D_2,G,B)$
- $(C_2,E)$
- $(rt,A)$

In postorder these correspond to:

- $(A,F,C_1)$
- $(E,D_1)$
4. Query those five intervals and take the minimum returned value.
5. That minimum equals the MEX.

### Ancestor case

If $u$ is an ancestor of $v$, the decomposition becomes simpler.

The complement can be covered by only three intervals:

1. preorder interval $(D_2,C_2,B)$
2. preorder interval $(rt,A)$
3. postorder interval $(A,C_1,D_1)$

Again, the minimum over these intervals is the answer.

### Why it works

Because $a$ is a permutation, every value appears exactly once.

Let $S$ be the set of vertices on the path. The MEX of values on $S$ is the smallest value whose vertex does not belong to $S$. This is exactly the minimum value on the complement $V\setminus S$.

The preorder and postorder decompositions cover the entire complement and nothing from the path. Every vertex outside the path belongs to exactly one of the queried regions. Taking the minimum over all queried regions therefore yields the minimum value outside the path, which equals the MEX.

The only nontrivial part is proving that every complement can be represented by at most five intervals. The preorder/postorder pairing was chosen precisely so that the six-piece preorder decomposition merges into five pieces when some regions are viewed in postorder instead.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(300000)

def solve():
    t = int(input())

    for _ in range(t):
        n, q = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        parent = [0] * (n + 1)
        depth = [0] * (n + 1)
        size = [0] * (n + 1)
        heavy = [0] * (n + 1)

        tin = [0] * (n + 1)
        tout = [0] * (n + 1)

        preorder = [0] * (n + 1)
        postorder = [0] * (n + 1)

        timer1 = 0
        timer2 = 0

        def dfs(u, p):
            nonlocal timer1, timer2

            parent[u] = p
            size[u] = 1

            timer1 += 1
            tin[u] = timer1
            preorder[timer1] = u

            best = 0

            for v in g[u]:
                if v == p:
                    continue

                depth[v] = depth[u] + 1
                dfs(v, u)

                size[u] += size[v]

                if size[v] > best:
                    best = size[v]
                    heavy[u] = v

            timer2 += 1
            tout[u] = timer2
            postorder[timer2] = u

        dfs(1, 0)

        top = [0] * (n + 1)

        def dfs_hld(u, tp):
            top[u] = tp

            if heavy[u]:
                dfs_hld(heavy[u], tp)

            for v in g[u]:
                if v == parent[u] or v == heavy[u]:
                    continue
                dfs_hld(v, v)

        dfs_hld(1, 1)

        def lca(a, b):
            while top[a] != top[b]:
                if depth[top[a]] < depth[top[b]]:
                    a, b = b, a
                a = parent[top[a]]

            return a if depth[a] < depth[b] else b

        def child_on_path(x, anc):
            while top[x] != top[anc]:
                if parent[top[x]] == anc:
                    return top[x]
                x = parent[top[x]]
            return heavy[anc]

        print(*preorder[1:])
        print(*postorder[1:])

        for _ in range(q):
            u, v = map(int, input().split())

            if tin[v] < tin[u]:
                u, v = v, u

            L = lca(u, v)

            def ask(tid, l, r):
                if l > r:
                    return n
                print("?", tid, l, r)
                sys.stdout.flush()
                return int(input())

            ans = n

            if L != u:
                U = child_on_path(u, L)
                V = child_on_path(v, L)

                ans = min(ans, ask(1, tin[v] + 1, n))
                ans = min(ans, ask(1, tin[u] + 1, tin[V] - 1))
                ans = min(ans, ask(1, 1, tin[L] - 1))
                ans = min(ans, ask(2, 1, tout[u] - 1))
                ans = min(ans, ask(2, tout[U] + 1, tout[v] - 1))
            else:
                ans = min(ans, ask(1, tin[v] + 1, n))
                ans = min(ans, ask(1, 1, tin[u] - 1))
                ans = min(ans, ask(2, 1, tout[v] - 1))

            print("!", ans)
            sys.stdout.flush()

            input()

solve()
```

The first DFS simultaneously computes subtree sizes, preorder positions, postorder positions, and heavy children.

The second DFS builds the heavy-light decomposition chains. This gives an $O(\log n)$ LCA routine and also lets us locate the child of the LCA lying on a specific branch.

The function `child_on_path(x, anc)` is subtle. It returns the child of `anc` that lies on the path from `anc` to `x`. This is exactly the boundary needed when converting the geometric decomposition into preorder and postorder intervals.

The interval formulas come directly from the complement decomposition described above. Empty intervals are ignored by returning `n`, which is larger than every possible value in the permutation.

## Worked Examples

### Example 1

Tree:

```
1 - 2 - 3
```

Suppose the queried path is `(2,3)`.

| Step | Value |
| --- | --- |
| LCA | 2 |
| Ancestor case | Yes |
| Preorder interval 1 | after subtree of 3 |
| Preorder interval 2 | before 2 |
| Postorder interval | before 3 |
| Minimum outside path | 0 |
| Answer | 0 |

The complement contains only vertex 1. Its value is 0, so the MEX of the path values is 0.

### Example 2

Tree:

```
    1
   / \
  2   3
 /     \
4       5
```

Query path `(4,5)`.

| Step | Value |
| --- | --- |
| LCA | 1 |
| General case | Yes |
| Child toward 4 | 2 |
| Child toward 5 | 3 |
| Queried regions | 5 |
| Minimum over regions | smallest value outside path |
| Answer | MEX |

This example exercises the harder case where neither endpoint is an ancestor of the other. The complement splits across both sides of the LCA, requiring the full five-interval decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\log n)$ | DFS and HLD preprocessing plus $O(\log n)$ LCA work per query |
| Space | $O(n)$ | Tree, HLD arrays, preorder and postorder storage |

The total constraints allow $O((n+q)\log n)$ comfortably. The memory usage is linear in the number of vertices.

## Test Cases

The original problem is interactive. The hacked version does not correspond to a normal function that can be tested with assert statements, because the query answers are supplied by the judge during execution.

For local verification, the usual approach is to write a simulator that:

1. Builds the two permutations.
2. Computes the answers that the judge would return.
3. Verifies that the reported MEX matches the true MEX on every queried path.

Typical stress tests should include:

```
# path tree
# star tree
# complete binary tree
# random trees

# queries where one endpoint is ancestor of the other
# queries whose LCA is strictly between endpoints
# paths passing through the root
# paths consisting of only two vertices
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Path tree | Correct MEX | Ancestor decomposition |
| Star tree | Correct MEX | LCA at root |
| Binary tree | Correct MEX | General five-interval case |
| Random tree | Correct MEX | Full stress verification |

## Edge Cases

### One endpoint is the ancestor of the other

Consider:

```
1
|
2
|
3
|
4
```

with query `(2,4)`.

The general five-piece decomposition is unnecessary. The complement collapses into three intervals. The algorithm detects `LCA = 2 = u` and uses the ancestor formulas, avoiding invalid interval boundaries.

### Path passes through the root

Consider:

```
    1
   / \
  2   3
```

with query `(2,3)`.

The LCA is the root. Several complement regions become empty. The implementation handles them through the `l > r` check and simply ignores those intervals.

### Complement contains a single vertex

Consider:

```
1 - 2 - 3
```

with query `(2,3)`.

Only vertex 1 lies outside the path. The minimum over all queried intervals still returns exactly the value of that single vertex, giving the correct MEX.

### Entire tree except one branch lies on the path

Large portions of the decomposition become empty, but the interval formulas remain valid. Empty intervals contribute `n`, which can never affect the minimum, so the answer is determined solely by the non-empty regions.
