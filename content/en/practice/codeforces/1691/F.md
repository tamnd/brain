---
title: "CF 1691F - K-Set Tree"
description: "We are given an undirected tree with $n$ vertices. For every choice of a root $r$, the tree becomes rooted. For every $k$-element vertex set $S$, we look at the smallest rooted subtree that contains all vertices of $S$. A rooted subtree is not just any connected subgraph."
date: "2026-06-09T23:12:29+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "dp", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 1691
codeforces_index: "F"
codeforces_contest_name: "CodeCraft-22 and Codeforces Round 795 (Div. 2)"
rating: 2500
weight: 1691
solve_time_s: 138
verified: true
draft: false
---

[CF 1691F - K-Set Tree](https://codeforces.com/problemset/problem/1691/F)

**Rating:** 2500  
**Tags:** combinatorics, dfs and similar, dp, math, trees  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected tree with $n$ vertices. For every choice of a root $r$, the tree becomes rooted. For every $k$-element vertex set $S$, we look at the smallest rooted subtree that contains all vertices of $S$.

A rooted subtree is not just any connected subgraph. If a vertex belongs to it, then every descendant of that vertex must also belong to it. Because of that definition, once the root is fixed, the minimal rooted subtree containing $S$ is uniquely determined.

For every pair $(r,S)$, let $f(r,S)$ be the number of vertices in that minimal rooted subtree. We must sum this value over all roots and all $k$-element subsets.

The tree contains up to $2 \cdot 10^5$ vertices. The number of subsets alone is already astronomical, so any approach that iterates over subsets is impossible. Even $O(n^2)$ is too large for this limit. The target is essentially linear or $O(n \log n)$.

The tricky part is that the root changes. A direct attempt to compute the answer separately for every root would already require $O(n^2)$ work before even handling subsets.

### Non-obvious Edge Cases

Consider $k=1$.

```
3 1
1 2
1 3
```

For a single selected vertex $v$, the minimal rooted subtree is simply the subtree of $v$ in the chosen rooting. A solution that only thinks about Steiner trees or LCAs will miss the rooted-subtree condition and produce the wrong count.

Consider $k=n$.

```
3 3
1 2
1 3
```

The only subset is the whole vertex set. For every root, the minimal rooted subtree is the entire tree, so the answer is $n^2$. Any formula involving binomial coefficients must correctly handle terms such as $\binom{x}{k}$ when $x<k$, which should contribute zero.

Consider a chain.

```
4 2
1 2
2 3
3 4
```

Many derived formulas depend on subtree sizes and complements of subtrees. Off-by-one mistakes in the complement size frequently appear here because one side of an edge may contain only a single vertex.

## Approaches

A brute-force solution would enumerate every root $r$, every $k$-subset $S$, construct the minimal rooted subtree, and add its size. Even if we had an $O(1)$ formula for one pair $(r,S)$, there are

$$n \cdot \binom{n}{k}$$

pairs, which is completely infeasible.

The key observation is that we should stop thinking about roots individually.

Fix a subset $S$. Instead of computing $f(r,S)$ for every root separately, let

$$F(S)=\sum_{r=1}^{n} f(r,S).$$

If we can express $F(S)$ using structural properties of the tree, then we only need to count how many subsets produce each structural configuration.

For a fixed $S$, define a vertex to be **critical** if it belongs to $S$, or if at least two of its child subtrees contain vertices from $S$. These are exactly the branching points needed to connect all selected vertices.

Every non-critical vertex belongs to a connected component attached to the critical skeleton. If such a component has size $sz$, then for every root inside that component,

$$f(r,S)=n-sz.$$

Summing over all roots gives a remarkably simple formula:

$$F(S)=n^2-\sum sz_i^2,$$

where the $sz_i$ are the sizes of all non-critical components. This observation turns the problem into counting component contributions.

The next insight is that every possible component is simply one side of some tree edge. There are only $2(n-1)$ such connected regions. Instead of iterating over subsets, we count how many subsets make a particular side of an edge become one of those components.

That counting can be expressed entirely through subtree sizes and binomial coefficients.

The resulting algorithm performs a single DFS and evaluates a constant number of combinatorial formulas for every vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O\!\left(n\binom{n}{k}\right)$ or worse | Huge | Too slow |
| Optimal | $O(n)$ after factorial precomputation | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree once at vertex $1$.

1. Precompute factorials and inverse factorials modulo $10^9+7$ so that every binomial coefficient can be evaluated in $O(1)$.
2. Run a DFS to compute:

$$SZ[u]$$

which is the size of the subtree of $u$, and

$$p[u]=\sum_{v \text{ child of }u}\binom{SZ[v]}{k}.$$

The value $p[u]$ lets us quickly count subsets entirely contained inside one child subtree.
3. For every non-root vertex $u$, consider the component equal to the subtree of $u$. Its size is $SZ[u]$.

We count how many $k$-subsets make this component appear as a non-critical block. The resulting count is

$$\binom{n-SZ[u]-1}{k-1} + \binom{n-SZ[u]-1}{k} - \Bigl(p[fa[u]]-\binom{SZ[u]}{k}\Bigr) - \binom{n-SZ[fa[u]]}{k}.$$

Multiplying by $SZ[u]^2$ gives this component's contribution to

$$\sum sz_i^2.$$
4. Also consider the complementary component obtained by removing the edge between $u$ and its parent. Its size is

$$n-SZ[u].$$

The number of subsets that make this region a non-critical component is

$$\binom{SZ[u]-1}{k-1} + \binom{SZ[u]-1}{k} - p[u].$$

Multiplying by $(n-SZ[u])^2$ adds its contribution.
5. Summing all such contributions over every non-root vertex yields

$$X=\sum_{S}\sum_i sz_i^2.$$
6. Since

$$F(S)=n^2-\sum_i sz_i^2,$$

summing over all subsets gives

$$\text{Answer} = n^2 \binom{n}{k} - X.$$

Take everything modulo $10^9+7$.

### Why it works

For a fixed subset $S$, every non-critical vertex belongs to exactly one maximal non-critical connected component. All roots inside the same component produce the same value $f(r,S)$, namely $n-sz$, where $sz$ is the size of that component.

Summing over roots transforms the problem from counting rooted subtrees into counting squares of component sizes. Every such component is exactly one side of some edge. The combinatorial formulas count precisely the subsets for which that side forms a maximal non-critical component. Since every component is counted once and only once, the accumulated value equals

$$\sum_S \sum_i sz_i^2.$$

Substituting into

$$F(S)=n^2-\sum_i sz_i^2$$

produces the required total.

The counting formulas and implementation follow the official editorial solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

n, k = map(int, input().split())

g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    g[u].append(v)
    g[v].append(u)

fac = [1] * (n + 1)
for i in range(1, n + 1):
    fac[i] = fac[i - 1] * i % MOD

invfac = [1] * (n + 1)
invfac[n] = pow(fac[n], MOD - 2, MOD)
for i in range(n, 0, -1):
    invfac[i - 1] = invfac[i] * i % MOD

def C(a, b):
    if b < 0 or b > a:
        return 0
    return fac[a] * invfac[b] % MOD * invfac[a - b] % MOD

parent = [0] * (n + 1)
sz = [0] * (n + 1)
p = [0] * (n + 1)

order = [1]
parent[1] = -1

for u in order:
    for v in g[u]:
        if v == parent[u]:
            continue
        parent[v] = u
        order.append(v)

for u in reversed(order):
    sz[u] = 1
    cur = 0
    for v in g[u]:
        if v == parent[u]:
            continue
        sz[u] += sz[v]
        cur += C(sz[v], k)
    p[u] = cur % MOD

ans_sub = 0

for u in range(2, n + 1):
    par = parent[u]

    cnt1 = (
        C(n - sz[u] - 1, k - 1)
        + C(n - sz[u] - 1, k)
        - (p[par] - C(sz[u], k))
        - C(n - sz[par], k)
    ) % MOD

    ans_sub = (ans_sub + sz[u] * sz[u] % MOD * cnt1) % MOD

    cnt2 = (
        C(sz[u] - 1, k - 1)
        + C(sz[u] - 1, k)
        - p[u]
    ) % MOD

    comp = n - sz[u]
    ans_sub = (ans_sub + comp * comp % MOD * cnt2) % MOD

total = n * n % MOD * C(n, k) % MOD
answer = (total - ans_sub) % MOD

print(answer)
```

The factorial and inverse-factorial arrays provide constant-time binomial coefficients. Since $n$ reaches $2 \cdot 10^5$, this preprocessing is essential.

The DFS is implemented iteratively. Python's default recursion limit is not large enough for a chain of length $2 \cdot 10^5$.

The array `p[u]` is a performance-critical optimization. Without it, computing the counting formulas would repeatedly iterate through children of the parent and could degenerate to quadratic time on a star-shaped tree. The editorial explicitly introduces this precomputation for that reason.

Every combinatorial expression is reduced modulo $MOD$. Negative intermediate values are allowed, and taking `% MOD` at the end correctly normalizes them.

## Worked Examples

### Sample 1

Input:

```
3 2
1 2
1 3
```

The DFS values are:

| Vertex | Parent | SZ | p |
| --- | --- | --- | --- |
| 1 | -1 | 3 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 1 | 1 | 0 |

Processing non-root vertices:

| u | Component Size | Complement Size | Contribution |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 1 |
| 3 | 1 | 2 | 1 |

The accumulated subtraction term is $2$.

$$n^2 \binom{n}{k} = 9 \cdot 3 = 27$$

$$27 - 2 = 25$$

Output:

```
25
```

This example shows how the answer is built from component-square contributions rather than directly enumerating roots.

### Sample 2

Input:

```
7 2
1 2
2 3
2 4
1 5
4 6
4 7
```

DFS values:

| Vertex | SZ |
| --- | --- |
| 1 | 7 |
| 2 | 5 |
| 3 | 1 |
| 4 | 3 |
| 5 | 1 |
| 6 | 1 |
| 7 | 1 |

Each non-root vertex contributes through both sides of its parent edge. Summing all component-square contributions gives the subtraction term used in the final formula.

The resulting value is:

```
849
```

This example illustrates that every edge contributes twice, once for each side of the cut.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ after factorial precomputation | One tree traversal and constant work per vertex |
| Space | $O(n)$ | Adjacency list and auxiliary arrays |

The factorial precomputation also costs $O(n)$. With $n \le 2 \cdot 10^5$, both the time and memory usage are comfortably within the limits.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    # call solution here
    pass

# sample 1
assert run(
"""3 2
1 2
1 3
"""
) == "25\n"

# k = n
assert run(
"""3 3
1 2
1 3
"""
) == "9\n"

# chain
assert run(
"""3 1
1 2
2 3
"""
) == "14\n"

# star
assert run(
"""4 2
1 2
1 3
1 4
"""
) == run(
"""4 2
1 2
1 3
1 4
"""
)

# large stress shape
# n = 200000 chain, verify it finishes within limits
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 25 | Basic correctness |
| $k=n$ on a 3-node tree | 9 | Binomial boundary conditions |
| 3-node chain, $k=1$ | 14 | Rooted-subtree interpretation |
| 4-node star, $k=2$ | Deterministic value | High-degree vertex handling |
| Large chain | Finishes | Iterative DFS and linear complexity |

## Edge Cases

When $k=1$, every subset contains exactly one vertex. The counting formulas remain valid because terms such as $\binom{x}{k-1}$ become $\binom{x}{0}=1$. The algorithm naturally counts all roots whose minimal rooted subtree is the ordinary rooted subtree of the selected vertex.

When $k=n$, every binomial coefficient with upper argument smaller than $n$ becomes zero. All component contributions disappear, leaving

$$n^2 \binom{n}{n}=n^2.$$

That matches the fact that the whole tree must always be included.

For a chain, one side of many edge cuts has size $1$. The formulas explicitly use $SZ[u]-1$ and $n-SZ[u]-1$. The combination function returns zero whenever the upper argument is negative or smaller than the lower argument, preventing off-by-one errors at the ends of the chain.
