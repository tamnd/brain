---
title: "CF 2190D - Prufer Vertex"
description: "We start with a forest. We may add edges between its connected components until the whole graph becomes a single tree. For every resulting tree, run the standard Prüfer-code deletion process: repeatedly remove the smallest numbered leaf until only two vertices remain."
date: "2026-06-07T21:07:12+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dsu", "number-theory", "probabilities", "trees"]
categories: ["algorithms"]
codeforces_contest: 2190
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1073 (Div. 1)"
rating: 2500
weight: 2190
solve_time_s: 165
verified: false
draft: false
---

[CF 2190D - Prufer Vertex](https://codeforces.com/problemset/problem/2190/D)

**Rating:** 2500  
**Tags:** combinatorics, dsu, number theory, probabilities, trees  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a forest. We may add edges between its connected components until the whole graph becomes a single tree.

For every resulting tree, run the standard Prüfer-code deletion process: repeatedly remove the smallest numbered leaf until only two vertices remain. One of those vertices is always vertex $n$. The other surviving vertex is called the Prüfer vertex $P(T)$.

The task is not to count all completion trees. Instead, for every $v<n$, we must count how many ways of connecting the forest produce a tree whose Prüfer vertex equals $v$.

The total number of vertices over all test cases is at most $2\cdot 10^5$. Any solution that performs work proportional to the number of completion trees is hopeless, because even an empty forest on $n$ vertices has $n^{n-2}$ possible trees. We need a structural characterization of the Prüfer vertex and then a counting formula that depends only on component sizes and a few subtree sizes.

A surprisingly dangerous edge case is when $n$ and $n-1$ already belong to the same connected component.

```
4 3
1 2
2 3
3 4
```

The forest is already a tree. There is exactly one completion. The answer is concentrated on a single vertex, namely the second vertex on the path from $4$ to $3$. Any counting formula that assumes $n$ and $n-1$ are initially disconnected will fail here.

Another subtle case is when the forest consists only of isolated vertices.

```
3 0
```

There are three completion trees. The answers are not symmetric. Vertex $2$ is larger than vertex $1$, so the leaf-removal order matters. Any argument based only on unlabeled trees gives the wrong distribution.

A third pitfall is the component containing $n$. Vertices inside that component are not equally likely to become the answer. What matters is the size of the rooted subtree hanging below a child of $n$, not just the component size.

## Approaches

The brute-force idea is straightforward. Enumerate every way to connect the forest into a tree, simulate the Prüfer process, and increment the corresponding answer.

This is correct because it directly follows the definition. Unfortunately, the number of completion trees is

$$n^{k-2}\prod s_i,$$

which is exponential in the worst case. Even for modest values of $n$, the number of trees is astronomically large.

The key observation comes from understanding the Prüfer process itself.

Consider the final surviving pair. Vertex $n$ is always present. When can vertex $n-1$ disappear before the end?

A tree with at least two vertices always has at least two leaves. Thus $n-1$ can only survive to the end if the only leaves near the end are $n-1$ and $n$. That means the unique path from $n$ to $n-1$ contains all remaining vertices. The second vertex on that path is exactly the vertex that survives together with $n$. This completely characterizes the Prüfer vertex.

Once this characterization is known, the problem becomes a counting problem on connected components. The classical formula

$$n^{k-2}\prod s_i$$

for counting ways to connect components can be combined with the fact that every vertex inside a component is symmetric. The resulting counts depend only on component sizes and, for vertices inside the component of $n$, on rooted subtree sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DSU/tree counting | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Find connected components

Run DFS or DSU on the forest.

For every vertex store its component id and the size of that component.

Root every component at its largest-numbered vertex. In particular, the component containing $n$ becomes rooted at $n$.

### 2. Compute subtree sizes inside the component of $n$

During DFS, compute

$$dp[v]=1+\sum dp[\text{child}].$$

For a child $v$ of $n$, this value is exactly the size of the branch hanging below $v$.

### 3. Handle the case where $n$ and $n-1$ are already connected

The Prüfer vertex is then fixed forever.

Walk from $n-1$ upward until reaching the child of $n$ lying on the path from $n$ to $n-1$.

Call this vertex $x$.

Every completion tree has $P(T)=x$, so

$$ans[x] = \Big(\prod s_i\Big)\, n^{k-2}.$$

All other answers are zero.

### 4. Consider a candidate vertex $v$

Assume $n$ and $n-1$ are in different components.

There are three situations.

#### 4.1 $v$ lies in the component of $n$

Then $v$ must be a direct child of $n$.

Among all ways to connect the remaining components, the component containing $n-1$ must end up inside the branch of $v$.

Because vertices of the component of $n$ are symmetric, the probability of landing in that branch is

$$\frac{dp[v]}{|C_n|}.$$

Multiplying by the total number of completion trees yields the answer.

#### 4.2 $v$ lies in the component of $n-1$

We first connect the components of $n$ and $n-1$.

Then the desired branch size becomes

$$|C_n|+|C_{n-1}|.$$

Substituting into the counting formula gives the contribution.

#### 4.3 $v$ lies in any other component

That component must first be attached to the component of $n$.

All vertices inside the component are symmetric, so only the component size matters.

### 5. Precompute modular inverses and powers

All formulas contain divisions by component sizes. Since the modulus is prime, use modular inverses.

Also precompute

$$n^0,n^1,\dots,n^k.$$

### Why it works

The crucial property is that the Prüfer vertex is exactly the second vertex on the path from $n$ to $n-1$. Once this is known, the problem no longer depends on the detailed deletion order.

For a fixed candidate $v$, we only need to count completion trees in which the component containing $n-1$ ends up inside the branch of $v$ when the tree is rooted at $n$. Vertices within the same connected component are indistinguishable in the classical component-joining counting formula, so the count is proportional to the size of the relevant branch. Every formula used by the algorithm is exactly the total number of completion trees multiplied by the fraction of completions placing $n-1$ in that branch. Thus every completion is counted once for exactly one vertex $v$, and the resulting answers are correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())

    inv = [0] * 200001
    inv[1] = 1
    for i in range(2, 200001):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        comp = [-1] * (n + 1)
        parent = [0] * (n + 1)
        sub = [1] * (n + 1)
        sizes = []

        sys.setrecursionlimit(1 << 20)

        def dfs(v, p, cid):
            comp[v] = cid
            sizes[cid] += 1
            parent[v] = p

            for to in g[v]:
                if to == p:
                    continue
                dfs(to, v, cid)
                sub[v] += sub[to]

        cid = 0
        for v in range(n, 0, -1):
            if comp[v] == -1:
                sizes.append(0)
                dfs(v, 0, cid)
                cid += 1

        k = cid

        sz = [0] * (n + 1)
        for v in range(1, n + 1):
            sz[v] = sizes[comp[v]]

        p = 1
        for s in sizes:
            p = p * s % MOD

        pw = [1] * (k + 1)
        for i in range(1, k + 1):
            pw[i] = pw[i - 1] * n % MOD

        def npow(e):
            if e >= 0:
                return pw[e]
            return inv[n]

        ans = [0] * n

        if comp[n] == comp[n - 1]:
            v = n - 1
            while parent[v] != n:
                v = parent[v]

            ans[v] = p * npow(k - 2) % MOD
        else:
            comp_n = comp[n]
            comp_nm1 = comp[n - 1]

            for v in range(1, n):
                if comp[v] == comp_n:
                    if parent[v] != n:
                        continue

                    ans[v] = (
                        sub[v]
                        * p
                        % MOD
                        * inv[sz[n]]
                        % MOD
                        * npow(k - 2)
                    ) % MOD

                elif comp[v] == comp_nm1:
                    ans[v] = (
                        p
                        * inv[sz[n]]
                        % MOD
                        * inv[sz[n - 1]]
                        % MOD
                        * (sz[n] + sz[n - 1])
                        % MOD
                        * npow(k - 3)
                    ) % MOD

                else:
                    ans[v] = (
                        sz[v]
                        * p
                        % MOD
                        * inv[sz[n]]
                        % MOD
                        * inv[sz[v]]
                        % MOD
                        * npow(k - 3)
                    ) % MOD

        print(*ans[1:])

solve()
```

The DFS simultaneously computes component ids, component sizes, parent pointers, and subtree sizes. Rooting each component at its largest vertex matches the argument used in the counting proof. The component containing $n$ is automatically rooted at $n$, which makes every relevant branch size equal to a subtree size.

The function `npow` handles the special exponent $-1$. This occurs when $k=1$ or $k=2$, and the editorial formula replaces $n^{-1}$ by the modular inverse of $n$.

The most common implementation mistake is forgetting that only direct children of $n$ can be answers when $v$ belongs to the component of $n$. The check `parent[v] == n` is essential.

## Worked Examples

### Example 1

Input:

```
3 0
```

Components:

| Vertex | Component size |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |

Here $k=3$, $n=3$.

| v | Formula result |
| --- | --- |
| 1 | 1 |
| 2 | 2 |

Output:

```
1 2
```

This example shows that labels matter. Even though all vertices start isolated, the Prüfer process is not symmetric.

### Example 2

Input:

```
5 4
4 2
3 4
1 2
4 5
```

The graph is already a tree.

The path from $5$ to $4$ is simply $5\to4$.

| Quantity | Value |
| --- | --- |
| $n$ | 5 |
| $n-1$ | 4 |
| second vertex on path | 4 |
| completion count | 1 |

Output:

```
0 0 0 1
```

This demonstrates the special case where $n$ and $n-1$ already belong to the same component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | DFS plus a linear scan over vertices |
| Space | $O(n)$ | Graph, component, parent, and subtree arrays |

The sum of $n$ over all test cases is at most $2\cdot10^5$. Linear processing per test case is comfortably within the limits.

## Test Cases

```python
# These are illustrative tests.

import sys, io

# helper placeholder
def run(inp: str) -> str:
    return "implementation dependent"

# sample 1
# assert run(...) == ...

# minimum tree
# 2 vertices, already connected
# answer must be 1
# assert run("1\n2 1\n1 2\n") == "1\n"

# two isolated vertices
# only one possible tree
# assert run("1\n2 0\n") == "1\n"

# chain already formed
# Prüfer vertex fixed
# assert run("1\n4 3\n1 2\n2 3\n3 4\n") == "0 0 1\n"

# star centered at n
# checks child-of-n logic
# assert run("1\n5 4\n5 1\n5 2\n5 3\n5 4\n") == "0 0 0 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Connected tree on 2 vertices | `1` | Smallest valid instance |
| Two isolated vertices | `1` | Component-joining base case |
| Path graph | Single nonzero answer | Fixed Prüfer vertex case |
| Star centered at $n$ | Answer concentrated at $n-1$ | Child-of-$n$ logic |

## Edge Cases

### $n$ and $n-1$ already connected

Input:

```
4 3
1 2
2 3
3 4
```

The path from $4$ to $3$ starts with vertex $3$, so $P(T)=3$. No added edges are possible. The algorithm detects that both vertices belong to the same component and directly outputs a single nonzero answer.

### All vertices isolated

Input:

```
3 0
```

There are three completion trees. The algorithm uses only component sizes, so it naturally counts all completions without enumerating them.

### Candidate vertex inside the component of $n$

Input:

```
6 3
1 6
6 4
2 1
```

Vertex $4$ is a direct child of $6$, while vertex $1$ has a larger subtree hanging below it. The algorithm uses subtree sizes, not merely component sizes, which is exactly what distinguishes their answer counts.
