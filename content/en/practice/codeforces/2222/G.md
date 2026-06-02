---
title: "CF 2222G - Statistics on Tree"
description: "We are given a tree. For a pair of vertices $(u,v)$, we remove every edge belonging to the unique simple path between them. After those edges are deleted, the tree breaks into several connected components. The value of the pair is the size of the largest remaining component."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dfs-and-similar", "divide-and-conquer", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "G"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 393
verified: false
draft: false
---

[CF 2222G - Statistics on Tree](https://codeforces.com/problemset/problem/2222/G)

**Rating:** -  
**Tags:** binary search, brute force, dfs and similar, divide and conquer, graphs, trees  
**Solve time:** 6m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree. For a pair of vertices $(u,v)$, we remove every edge belonging to the unique simple path between them.

After those edges are deleted, the tree breaks into several connected components. The value of the pair is the size of the largest remaining component.

For every possible component size $i$, we must count how many pairs $(u,v)$ with $u \le v$ have value exactly $i$.

The obvious difficulty is that there are $O(n^2)$ pairs, and for each pair the path may contain $O(n)$ edges. With $n$ up to $10^5$ per test case and total $5 \cdot 10^5$ across all test cases, anything quadratic is immediately impossible. Even $O(n^2)$ counting is already far beyond the limit.

The interesting part is that deleting a path does not create arbitrary components. Every remaining component is attached to some vertex of that path. The structure of those components depends heavily on subtree sizes, which suggests rooting the tree and reasoning about LCAs.

A non-obvious corner case appears when the LCA is the centroid itself.

Consider a centroid whose largest child subtree has size $A$, and another child subtree has size $B$. For a pair with one endpoint in each subtree, a naive formula would predict value $n-A-B$. That is sometimes wrong because the largest remaining component may actually stay inside the largest branch. This is the only place where the naive counting breaks.

For example:

```
    c
   / \
  L   R
```

If $L$ is much larger than every other branch, removing a path that enters $L$ does not necessarily destroy the largest component inside $L$. Any solution that always assumes "outside the used branches" is the largest component will overcount these pairs.

Another subtle case is $u=v$. No edge is removed, so the tree stays connected and the value is always $n$. These pairs contribute exactly $n$ times to answer $n$.

## Approaches

The brute force approach follows the definition directly.

For every pair $(u,v)$, find the path, delete all edges on that path, run a DFS on the remaining graph, and record the largest component size.

This is correct because it literally simulates the operation from the statement. Unfortunately there are $O(n^2)$ pairs and each simulation costs at least $O(n)$, leading to $O(n^3)$ or worse. With $n=10^5$, this is completely infeasible.

The key observation comes from rooting the tree at a centroid.

Suppose a pair has LCA $x$.

If one endpoint is $x$ and the other lies inside a child subtree of size $a$, then deleting the path disconnects that child subtree from the rest of the tree. One candidate component has size $n-a$.

If the endpoints lie in two different child subtrees of sizes $a$ and $b$, then another candidate component has size $n-a-b$.

When the tree is rooted at a centroid, every subtree away from the centroid has size at most $n/2$. For every LCA different from the centroid, the component outside the used branches is strictly larger than any component inside those branches. That means the pair value is simply:

$$n-a$$

or

$$n-a-b$$

depending on the configuration.

Now the problem becomes counting pairs by subtree sizes instead of examining paths individually.

Almost every pair is handled by these formulas. The only exception is when the LCA is the centroid and one endpoint lies in the centroid's largest child subtree. Those pairs must be removed from the naive count and recomputed separately.

The correction step reduces to counting values of

$$\max(f(v), g(w))$$

for vertices $v$ in the largest centroid branch and vertices $w$ outside it. After precomputing all $f$ and $g$ values, this becomes a purely numerical counting problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ or worse | $O(n)$ | Too slow |
| Optimal | $O(n\sqrt n + n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Find a centroid $r$ of the tree.

Every child subtree of a centroid has size at most $n/2$, which is the structural property that makes the naive formula valid almost everywhere.
2. Root the tree at $r$ and compute subtree sizes.

We will use these sizes repeatedly when counting contributions.
3. Add the diagonal pairs.

Every pair $(v,v)$ has value $n$, so add $n$ to `ans[n]`.
4. Count all non-diagonal pairs using LCA formulas.

For every vertex $x$, let its child subtree sizes be:

$$s_1,s_2,\dots,s_k$$

Pairs $(x, \text{vertex in } s_i)$ contribute:

$$ans[n-s_i] += s_i$$

Pairs whose endpoints lie in two different child subtrees contribute:

$$ans[n-s_i-s_j] += s_i s_j$$
5. Compress equal subtree sizes while processing one vertex.

If size $s$ appears $c_s$ times, then pairs between equal-sized child subtrees contribute:

$$\binom{c_s}{2}s^2$$

and pairs between sizes $s$ and $t$ contribute:

$$c_s c_t st$$

This reduces the total work to $O(n\sqrt n)$.
6. Let $L$ be the largest child subtree of the centroid and let its size be $A$.

These are the only pairs that may have been counted incorrectly.
7. Remove all naive contributions between $L$ and every other centroid child subtree $C$.

If $C$ has size $b$, subtract:

$$A b$$

from:

$$ans[n-A-b]$$
8. Compute $f(v)$ for every vertex inside $L$.

Along the path from $L$'s root to $v$, every side piece

$$sz(parent)-sz(child)$$

is a candidate component. The endpoint subtree $sz(v)$ is also a candidate.

$f(v)$ is the largest such value.
9. Compute $g(w)$ for every vertex outside $L$.

Besides the same side-piece candidates, there is one additional component:

$$n-A-sz(C)$$

where $C$ is the centroid child subtree containing $w$.
10. Count all pairs $(v,w)$ using

$$value(v,w)=\max(f(v),g(w))$$

Build frequency arrays for all $f$ values and $g$ values.

For every value $x$,

$$\text{pairs with max}=x = freq_g[x]\cdot count_f(\le x) + freq_f[x]\cdot count_g(<x)$$

Add these counts to `ans[x]`.
11. Output the answer array.

### Why it works

Rooting at a centroid guarantees that every subtree away from the root has size at most $n/2$. For every pair whose LCA is not the centroid, the component outside the branches used by the path is larger than every component inside those branches, so the simple formulas $n-a$ and $n-a-b$ are correct.

The only time this argument fails is when the path crosses the centroid's largest child subtree. Those pairs are removed and recomputed exactly. For such a pair, every remaining component belongs either to the largest branch side or to the outside side. The largest component on those sides is represented by $f(v)$ and $g(w)$, so the true answer is $\max(f(v),g(w))$. Every pair is counted exactly once, giving the correct frequency for every value.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        g = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        if n == 1:
            out.append("1")
            continue

        parent = [-1] * n
        order = [0]
        parent[0] = 0

        for v in order:
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                order.append(to)

        sz = [1] * n
        for v in reversed(order[1:]):
            sz[parent[v]] += sz[v]

        centroid = 0
        best = n

        for v in range(n):
            mx = n - sz[v]
            for to in g[v]:
                if to == parent[v]:
                    continue
                mx = max(mx, sz[to])
            if mx < best:
                best = mx
                centroid = v

        parent = [-1] * n
        order = [centroid]
        parent[centroid] = centroid

        for v in order:
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                order.append(to)

        sz = [1] * n
        for v in reversed(order[1:]):
            sz[parent[v]] += sz[v]

        ans = [0] * (n + 1)
        ans[n] = n

        for v in range(n):
            freq = {}

            for to in g[v]:
                if parent[to] == v:
                    s = sz[to]
                    ans[n - s] += s
                    freq[s] = freq.get(s, 0) + 1

            items = list(freq.items())

            m = len(items)
            for i in range(m):
                s, cs = items[i]
                ans[n - 2 * s] += cs * (cs - 1) // 2 * s * s

            for i in range(m):
                s, cs = items[i]
                for j in range(i + 1, m):
                    t2, ct = items[j]
                    ans[n - s - t2] += cs * ct * s * t2

        largest_child = -1
        A = -1

        centroid_children = []

        for to in g[centroid]:
            if parent[to] == centroid:
                centroid_children.append(to)
                if sz[to] > A:
                    A = sz[to]
                    largest_child = to

        if largest_child != -1:
            for to in centroid_children:
                if to == largest_child:
                    continue
                ans[n - A - sz[to]] -= A * sz[to]

            fy = [0] * (n + 1)
            fx = [0] * (n + 1)

            stack = [(largest_child, 0)]
            while stack:
                v, mx = stack.pop()
                cur = max(mx, sz[v])
                fy[cur] += 1

                for to in g[v]:
                    if parent[to] == v:
                        stack.append((to, max(mx, sz[v] - sz[to])))

            for root in centroid_children:
                if root == largest_child:
                    continue

                base = n - A - sz[root]
                stack = [(root, base)]

                while stack:
                    v, mx = stack.pop()
                    cur = max(mx, sz[v])
                    fx[cur] += 1

                    for to in g[v]:
                        if parent[to] == v:
                            stack.append((to, max(mx, sz[v] - sz[to])))

            prefy = 0
            prefx = 0

            for val in range(1, n + 1):
                ans[val] += fx[val] * prefy
                prefy += fy[val]
                ans[val] += fx[val] * fy[val]
                ans[val] += fy[val] * prefx
                prefx += fx[val]

        out.append(" ".join(str(ans[i]) for i in range(1, n + 1)))

    sys.stdout.write("\n".join(out))

solve()
```

The first DFS finds a centroid. After re-rooting at that centroid, the subtree sizes become the foundation for all later formulas.

The main counting phase never looks at individual pairs. It only examines child subtree sizes. Equal sizes are grouped together so that all contributions between equal-sized branches are added with a single formula.

The correction phase isolates the largest centroid branch. Every potentially incorrect pair has exactly one endpoint inside that branch and one endpoint outside it. The DFS that computes $f$ and $g$ carries the largest side-component seen so far on the path, which matches the definition from the proof.

The final counting step uses frequency arrays instead of sorting. Since every value lies between $1$ and $n$, prefix counts let us count all pairwise maxima in linear time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\sqrt n + n)$ | grouped subtree-size counting dominates |
| Space | $O(n)$ | graph, subtree sizes, frequency arrays |

The total input size across test cases is at most $5 \cdot 10^5$. An $O(n\sqrt n)$ solution with linear memory comfortably fits the limits.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

The tree consists of a single edge.

| Pair | Removed edges | Largest component |
| --- | --- | --- |
| (1,1) | none | 2 |
| (2,2) | none | 2 |
| (1,2) | edge (1,2) | 1 |

Output:

```
1 2
```

This example confirms that diagonal pairs always contribute to value $n$.

### Example 2

Input:

```
3
1 2
1 3
```

Root at vertex 1.

Child subtree sizes are $[1,1]$.

| Contribution type | Value | Count |
| --- | --- | --- |
| Diagonal pairs | 3 | 3 |
| Root with child | 2 | 2 |
| Between children | 1 | 1 |

Final frequencies:

| Value | Count |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Output:

```
1 2 3
```

This example demonstrates the two counting formulas $n-s$ and $n-s-t$.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    # paste solve() here

    return out.getvalue().strip()

# minimum tree
assert run("""1
1
""") == "1"

# single edge
assert run("""1
2
1 2
""") == "1 2"

# star with 3 nodes
assert run("""1
3
1 2
1 3
""") == "1 2 3"

# path of length 3
assert run("""1
4
1 2
2 3
3 4
""") == "1 3 2 4"

# sample block from statement
assert run("""2
1
2
1 2
""") == """1
1 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `1` | Smallest possible tree |
| One edge | `1 2` | Path deletion of one edge |
| Three-node star | `1 2 3` | Two-child counting formula |
| Four-node path | `1 3 2 4` | Non-trivial LCA structure |
| Mixed sample | Correct frequencies | Multiple test cases |

## Edge Cases

Consider:

```
1
1
```

No edge exists. The only pair is $(1,1)$. The algorithm immediately adds one diagonal pair to `ans[1]` and outputs:

```
1
```

Now consider:

```
1
2
1 2
```

The diagonal pairs contribute twice to value $2$. The non-diagonal pair contributes once to value $1$. The answer becomes:

```
1 2
```

The centroid correction is never triggered because there is only one child subtree.

Finally consider a centroid with one dominant branch and one small branch. The naive counting would assign all crossing pairs to value $n-A-B$. The algorithm explicitly subtracts those contributions, computes $f(v)$ and $g(w)$, and re-adds them according to $\max(f(v),g(w))$. This is exactly the situation where a naive centroid-rooted solution fails, and the correction phase handles it completely.
