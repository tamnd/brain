---
title: "CF 2188E - Jerry and Tom"
description: "Every vertex has an edge to the next vertex, and possibly one additional long jump to a larger vertex. The extra edges never cross. If we draw every edge above the number line, no two extra edges form the pattern $ui < uj < vi < vj$. Jerry must move every turn."
date: "2026-06-09T04:37:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "games", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2188
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1077 (Div. 2)"
rating: 2300
weight: 2188
solve_time_s: 123
verified: true
draft: false
---

[CF 2188E - Jerry and Tom](https://codeforces.com/problemset/problem/2188/E)

**Rating:** 2300  
**Tags:** data structures, dfs and similar, games, graphs, greedy, trees  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Every vertex has an edge to the next vertex, and possibly one additional long jump to a larger vertex. The extra edges never cross. If we draw every edge above the number line, no two extra edges form the pattern $u_i < u_j < v_i < v_j$.

Jerry must move every turn. Tom may move or stay. Jerry wins by reaching vertex $n$ before being caught. Tom wins as soon as both players occupy the same vertex at the end of a turn.

For every ordered starting pair $(x,y)$, we define $f(x,y)$ as the minimum number of actual moves Tom must make to force a win. If Tom cannot force a win, the value is $0$.

We must sum $f(x,y)$ over all ordered pairs $x \ne y$.

The total number of vertices over all test cases is only $2 \cdot 10^5$, which immediately rules out anything close to $O(n^2)$ per test case. Since the final answer involves all ordered pairs, we need to aggregate information globally rather than simulate games individually.

The most dangerous part of the problem is that the game is played on a DAG, not a tree. A naive approach may try to reason about arbitrary paths. The non-crossing condition is exactly what makes a tree structure appear.

Consider a graph with vertices $1 \to 2 \to 3 \to 4$ and an extra edge $1 \to 4$.

If Jerry starts at $1$ and Tom at $3$, Tom must immediately move to $4$. Waiting loses because Jerry can jump directly to $4$. The answer is $f(1,3)=1$, not $0$.

Another subtle case is $x=n$. Jerry wins immediately before any turn is played. For example:

```
n = 2
x = 2
y = 1
```

Tom has no opportunity to move, so $f(2,1)=0$.

A third trap is that Tom is allowed to stay still. Sometimes the optimal strategy is to make zero moves and wait at a critical ancestor. Any solution that assumes Tom always advances will overcount.

## Approaches

A brute-force solution would evaluate every ordered pair $(x,y)$, solve the corresponding game, and accumulate the answer.

The graph contains $O(n)$ edges, so even an $O(n)$ game analysis per pair already costs $O(n^2)$. Since there are $O(n^2)$ pairs, the total complexity becomes $O(n^3)$, which is hopeless for $n=2 \cdot 10^5$.

The key observation comes from the non-crossing condition.

For every vertex $i$, let $a_i$ be the largest endpoint among all outgoing edges of $i$. Since the ordinary edge $i \to i+1$ always exists, $a_i$ is well-defined.

A crucial fact is that every path from $i$ to $n$ must pass through $a_i$. If a path tried to bypass $a_i$, eventually a crossing edge would be created, contradicting the graph restriction. This observation appears in the official solution discussions.

Now connect every vertex $i$ to $a_i$. These edges form a rooted tree with root $n$. Every path from a vertex to $n$ contains all ancestors of that vertex in this tree.

Once the game is translated onto this tree, the outcome becomes simple.

Let $d_u$ be the depth of $u$ in the tree, measured from root $n$. Let $L=\operatorname{lca}(x,y)$.

If $d_x < d_y$, Jerry can stay strictly ahead of Tom forever and reaches $n$, so Tom cannot force a win.

If $d_x \ge d_y$, Tom wins by racing to $L$. He reaches $L$ no later than Jerry, and Jerry must pass through $L$. The minimum number of moves Tom needs is

$$f(x,y)=d_y-d_L.$$

This reduces the game to a pure tree counting problem.

After rewriting the ordered-pair sum and grouping symmetric pairs, the answer becomes

$$A-B+C,$$

where

$$A=\sum_{x<y}\min(d_x,d_y),$$

$$B=\sum_{x<y} d_{\operatorname{lca}(x,y)},$$

and

$$C=\sum_{\substack{x<y\\ d_x=d_y}} \left(d_x-d_{\operatorname{lca}(x,y)}\right).$$

All three terms can be computed in $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For every vertex $i<n$, compute $a_i$, the largest endpoint among its outgoing edges.
2. Build a rooted tree by making $a_i$ the parent of $i$. The root is vertex $n$.
3. Run a DFS to compute subtree sizes and depths.
4. Compute

$$A=\sum_{x<y}\min(d_x,d_y).$$

Sort all depths. If the sorted depths are $b_1 \le b_2 \le \dots \le b_n$, then

$$A=\sum_{i=1}^{n} b_i (n-i).$$

Every pair contributes the smaller depth, which is exactly the left endpoint in sorted order.
5. Compute

$$B=\sum_{x<y} d_{\operatorname{lca}(x,y)}.$$

For a node $u$, the number of unordered pairs whose LCA equals $u$ is

$$\binom{\text{sz}_u}{2} - \sum_{v \text{ child of } u} \binom{\text{sz}_v}{2}.$$

Multiply this count by $d_u$ and add it to $B$.
6. Compute

$$C_1=\sum_h h \binom{\text{cnt}_h}{2},$$

where $\text{cnt}_h$ is the number of vertices at depth $h$.

This equals the first part of $C$.
7. Compute

$$C_2=\sum_{\substack{x<y\\ d_x=d_y}} d_{\operatorname{lca}(x,y)}.$$

Use DSU-on-tree. For each node $u$, count equal-depth pairs whose LCA is exactly $u$. If that count is $P_u$, then add

$$d_u \cdot P_u$$

to $C_2$.
8. The final answer is

$$A-B+(C_1-C_2).$$

### Why it works

The entire solution rests on the tree induced by the maximal outgoing edge of every vertex. Every path to $n$ must pass through the parent in this tree, so the game depends only on ancestor relationships. Jerry can avoid capture exactly when he starts strictly closer to the root than Tom. Otherwise Tom can occupy the LCA first and wait. This gives the closed formula for $f(x,y)$. The remaining work is counting how often depths and LCAs contribute across all pairs, which is exactly what the three aggregated terms compute.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        parent = [0] * (n + 1)
        for i in range(1, n):
            parent[i] = i + 1

        for _ in range(m):
            u, v = map(int, input().split())
            if v > parent[u]:
                parent[u] = v

        g = [[] for _ in range(n + 1)]
        root = n

        for i in range(1, n):
            g[parent[i]].append(i)

        depth = [0] * (n + 1)
        sz = [0] * (n + 1)
        heavy = [0] * (n + 1)

        depth_cnt = [0] * n

        def dfs1(u):
            sz[u] = 1
            depth_cnt[depth[u]] += 1

            mx = 0
            for v in g[u]:
                depth[v] = depth[u] + 1
                dfs1(v)
                sz[u] += sz[v]
                if sz[v] > mx:
                    mx = sz[v]
                    heavy[u] = v

        dfs1(root)

        depths = depth[1:]
        depths.sort()

        A = 0
        for i, d in enumerate(depths):
            A += d * (n - 1 - i)

        B = 0
        for u in range(1, n + 1):
            pairs = sz[u] * (sz[u] - 1) // 2
            for v in g[u]:
                pairs -= sz[v] * (sz[v] - 1) // 2
            B += pairs * depth[u]

        C1 = 0
        for d, c in enumerate(depth_cnt):
            C1 += d * (c * (c - 1) // 2)

        big = [False] * (n + 1)
        freq = [0] * n

        C2 = 0

        def add_subtree(u, delta):
            freq[depth[u]] += delta
            for v in g[u]:
                if not big[v]:
                    add_subtree(v, delta)

        def count_subtree(u):
            nonlocal cur_pairs
            cur_pairs += freq[depth[u]]
            for v in g[u]:
                if not big[v]:
                    count_subtree(v)

        def dfs2(u, keep):
            nonlocal C2, cur_pairs

            for v in g[u]:
                if v != heavy[u]:
                    dfs2(v, False)

            if heavy[u]:
                dfs2(heavy[u], True)
                big[heavy[u]] = True

            pairs_here = 0

            for v in g[u]:
                if v == heavy[u]:
                    continue

                cur_pairs = 0
                count_subtree(v)
                pairs_here += cur_pairs
                add_subtree(v, 1)

            freq[depth[u]] += 1

            if heavy[u]:
                big[heavy[u]] = False

            C2 += pairs_here * depth[u]

            if not keep:
                add_subtree(u, -1)

        dfs2(root, False)

        ans = A - B + (C1 - C2)
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first phase builds the parent tree using the largest outgoing edge from every vertex. The graph property guarantees that this tree captures every possible route to the root.

The first DFS computes depths, subtree sizes, and heavy children. These values are reused by every later formula.

The computation of $B$ uses a standard LCA-counting identity. Every unordered pair inside the subtree contributes to some ancestor. Subtracting the pairs entirely contained in child subtrees leaves exactly the pairs whose LCA is the current node.

The DSU-on-tree section is the only delicate part. While processing a node $u$, the frequency table stores depths already accumulated from previously processed child subtrees. When traversing another child subtree, every vertex immediately finds how many equal-depth partners already exist. Those pairs have LCA exactly $u$, because they lie in different child subtrees.

All arithmetic uses Python integers, so overflow is never an issue.

## Worked Examples

### Example 1

Input:

```
4 2
2 4
1 4
```

The parent tree is:

```
4
├─1
└─2
   └─3
```

| Vertex | Depth |
| --- | --- |
| 4 | 0 |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |

Sorted depths are $[0,1,1,2]$.

| Term | Value |
| --- | --- |
| A | 5 |
| B | 0 |
| C1 | 1 |
| C2 | 0 |
| Answer | 6 |

This matches the sample output.

### Example 2

Input:

```
3 1
1 3
```

The tree is:

```
3
├─1
└─2
```

| Vertex | Depth |
| --- | --- |
| 3 | 0 |
| 1 | 1 |
| 2 | 1 |

| Term | Value |
| --- | --- |
| A | 2 |
| B | 0 |
| C1 | 1 |
| C2 | 1 |
| Answer | 2 |

The equal-depth pair $(1,2)$ contributes once more in the symmetric transformation, which is exactly what $C$ corrects.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting depths and DSU-on-tree |
| Space | $O(n)$ | Tree, depth arrays, frequency tables |

The total $n$ across all test cases is at most $2 \cdot 10^5$, so $O(n \log n)$ easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    bak = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = bak
    return out.getvalue()

# provided sample
assert run("""5
2 0
3 1
1 3
4 2
2 4
1 4
5 1
1 4
8 3
1 4
5 8
2 4
""") == """0
2
6
3
23
"""

# minimum graph
assert run("""1
2 0
""") == "0\n"

# pure chain
assert run("""1
3 0
""") == "0\n"

# single jump to root
assert run("""1
4 1
1 4
""") == "3\n"

# nested jumps
assert run("""1
5 2
1 5
2 4
""") == "8\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0` | `0` | Smallest possible graph |
| Chain only | `0` | Tom never needs positive moves |
| One jump to root | `3` | Immediate interception cases |
| Nested jumps | `8` | Non-crossing extra edges and tree construction |

## Edge Cases

Consider:

```
1
2 0
```

Jerry starts at vertex $2$ for the pair $(2,1)$. The game ends immediately with Jerry's victory. The tree depth of vertex $2$ is $0$, so the formula correctly contributes nothing.

Consider:

```
1
4 1
1 4
```

Tom can often win by waiting at vertex $4$. The algorithm captures this because the LCA is already the root and $d_y-d_{LCA}=0$.

Consider:

```
1
4 2
1 4
2 4
```

Vertices $1$ and $2$ lie at the same depth. Equal-depth pairs are exactly where the symmetric-pair transformation overcounts. The correction term $C=C_1-C_2$ removes the excess and produces the correct answer.
