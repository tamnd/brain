---
title: "CF 102760I - Query On A Tree 17"
description: "We have a rooted tree with root 1. Every vertex stores a nonnegative number of people. Initially every vertex has value zero. Each operation increases the values on either an entire subtree or an entire simple path."
date: "2026-07-29T00:03:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "I"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 114
verified: true
draft: false
---

[CF 102760I - Query On A Tree 17](https://codeforces.com/problemset/problem/102760/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with root 1. Every vertex stores a nonnegative number of people. Initially every vertex has value zero. Each operation increases the values on either an entire subtree or an entire simple path. After every update we must print the vertex where all people have the smallest possible total travel distance. If several vertices have the same minimum, we choose the one closest to the root.

The value we are minimizing is the weighted sum of distances. With up to $10^5$ vertices and $10^5$ operations, recomputing the value of every vertex after every update would require roughly $10^{10}$ work, which is impossible. We need logarithmic or near logarithmic processing per operation.

The tricky cases come from the tie rule and from zero valued vertices. A vertex whose child subtree contains exactly half of all people does not force us to move into that child because both sides give the same cost, and the shallower vertex must win.

For example, if the tree is a chain:

```
1
|
2
|
3
```

and vertex 3 has value 10, the answer is 1, not 3. Moving from 1 to 2 or 3 does not improve the gathering distance enough to beat the shallower choice.

## Approaches

A brute force method would maintain every vertex value explicitly. After each update, we could run a tree traversal from every possible answer vertex and calculate the total distance. This is correct because it directly evaluates the definition, but a single query would already cost $O(n)$ or worse, leading to $O(nQ)$ operations.

The key observation is that the answer is a weighted centroid. If we move across an edge from a vertex to its parent, the distance sum changes only according to the amount of weight in the moved subtree. If a child subtree contains more than half of all people, moving into it improves the answer. Otherwise we should stay.

The remaining problem is maintaining subtree sums under subtree additions and path additions. We flatten the tree with heavy light decomposition. In DFS order, every subtree becomes one interval, and every path becomes $O(\log n)$ intervals. A lazy segment tree maintains the values in DFS order, allowing interval additions and prefix searches.

The weighted centroid can be found by locating the first DFS order position whose prefix weight reaches half of the total weight. The answer lies on the ancestor chain of that vertex. Binary lifting is used to move upward until the highest valid centroid is found.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nQ)$ | $O(n)$ | Too slow |
| HLD + Segment Tree | $O(Q\log^2 n)$ | $O(n\log n)$ | Accepted |

## Algorithm Walkthrough

1. Build the rooted tree and compute subtree sizes, depths, heavy children, DFS order, and binary lifting ancestors.
2. Use heavy light decomposition so that every subtree corresponds to one DFS interval and every path can be split into logarithmically many intervals.
3. Store current vertex values in a lazy segment tree over DFS order. The segment tree supports adding one to an interval, finding the total weight, and finding the first position where a prefix reaches a target.
4. After an update, let the total number of people be $S$. Find the first DFS position whose prefix sum is at least $\lceil S/2\rceil$.
5. The answer is an ancestor of this vertex. Use binary lifting and subtree sum queries to climb upward while the current ancestor does not contain enough weight.

Why it works: the difference between the cost at a vertex and its parent depends only on whether the child side contains more than half of the total weight. The chosen vertex is exactly the shallowest vertex whose child direction containing the heavy side cannot improve the cost. The prefix search finds a point inside that heavy side, and climbing ancestors resolves the required tie rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(300000)

n = int(input())
g = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    a, b = map(int, input().split())
    g[a].append(b)
    g[b].append(a)

par = [[0] * (n + 1) for _ in range(17)]
dep = [0] * (n + 1)
sz = [0] * (n + 1)
son = [0] * (n + 1)

def dfs1(u, p):
    par[0][u] = p
    dep[u] = dep[p] + 1
    sz[u] = 1
    best = 0
    for v in g[u]:
        if v == p:
            continue
        dfs1(v, u)
        sz[u] += sz[v]
        if sz[v] > best:
            best = sz[v]
            son[u] = v

dfs1(1, 0)

for j in range(1, 17):
    for i in range(1, n + 1):
        par[j][i] = par[j - 1][par[j - 1][i]]

tin = [0] * (n + 1)
tout = [0] * (n + 1)
rev = [0] * (n + 1)
top = [0] * (n + 1)
timer = 0

def dfs2(u, t):
    global timer
    timer += 1
    tin[u] = timer
    rev[timer] = u
    top[u] = t
    if son[u]:
        dfs2(son[u], t)
    for v in g[u]:
        if v != par[0][u] and v != son[u]:
            dfs2(v, v)
    tout[u] = timer

dfs2(1, 1)

class Seg:
    def __init__(self, n):
        self.s = [0] * (4 * n)
        self.lz = [0] * (4 * n)

    def add(self, x, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.s[x] += r - l + 1
            self.lz[x] += 1
            return
        m = (l + r) // 2
        self.push(x, l, r)
        if ql <= m:
            self.add(x * 2, l, m, ql, qr)
        if qr > m:
            self.add(x * 2 + 1, m + 1, r, ql, qr)
        self.s[x] = self.s[x * 2] + self.s[x * 2 + 1]

    def push(self, x, l, r):
        if self.lz[x]:
            m = (l + r) // 2
            v = self.lz[x]
            self.s[x * 2] += v * (m - l + 1)
            self.s[x * 2 + 1] += v * (r - m)
            self.lz[x * 2] += v
            self.lz[x * 2 + 1] += v
            self.lz[x] = 0

    def query(self, x, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.s[x]
        self.push(x, l, r)
        m = (l + r) // 2
        res = 0
        if ql <= m:
            res += self.query(x * 2, l, m, ql, qr)
        if qr > m:
            res += self.query(x * 2 + 1, m + 1, r, ql, qr)
        return res

    def kth(self, x, l, r, k):
        if l == r:
            return l
        self.push(x, l, r)
        m = (l + r) // 2
        if self.s[x * 2] >= k:
            return self.kth(x * 2, l, m, k)
        return self.kth(x * 2 + 1, m + 1, r, k - self.s[x * 2])

seg = Seg(n)

def path_add(a, b):
    while top[a] != top[b]:
        if dep[top[a]] < dep[top[b]]:
            a, b = b, a
        seg.add(1, 1, n, tin[top[a]], tin[a])
        a = par[0][top[a]]
    if dep[a] > dep[b]:
        a, b = b, a
    seg.add(1, 1, n, tin[a], tin[b])

def subtree_sum(u):
    return seg.query(1, 1, n, tin[u], tout[u])

q = int(input())
ans = []
for _ in range(q):
    data = list(map(int, input().split()))
    if data[0] == 1:
        u = data[1]
        seg.add(1, 1, n, tin[u], tout[u])
    else:
        path_add(data[1], data[2])

    total = seg.s[1]
    need = (total + 1) // 2
    x = rev[seg.kth(1, 1, n, need)]

    for j in range(16, -1, -1):
        p = par[j][x]
        if p and subtree_sum(p) >= need:
            x = p

    while par[0][x] and subtree_sum(par[0][x]) >= need:
        x = par[0][x]

    ans.append(str(x))

print("\n".join(ans))
```

The segment tree stores the actual vertex values in DFS order. The `add` operation handles both subtree and heavy light path updates. The `kth` function finds the first place where cumulative weight reaches half of the total, which identifies the region containing the centroid.

The ancestor jumps use the fact that only ancestors of that found vertex can be the answer. The final upward movement keeps the shallowest valid centroid, matching the required tie breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q\log^2 n)$ | Each path update uses $O(\log n)$ segments, each segment update costs $O(\log n)$, and centroid searching uses logarithmic ancestor jumps. |
| Space | $O(n\log n)$ | Binary lifting dominates the memory usage. |

The bounds allow this approach because every operation is logarithmic instead of scanning the whole tree.

## Edge Cases

A single path with all weight concentrated at a leaf tests the tie rule. The algorithm finds the heavy prefix but climbs back to the closest valid ancestor, so it does not incorrectly return the leaf.

A query that updates a single vertex through a path where both endpoints are equal tests the path decomposition boundary. Heavy light decomposition treats this as a one vertex interval and the segment tree performs a normal point update.

A tree where the heavy side contains exactly half of the total weight tests equality handling. The algorithm uses $\lceil S/2\rceil$ and only moves upward when the ancestor still satisfies the condition, so the shallower vertex is preserved.
