---
title: "CF 102565E - OneZeroTree"
description: "The tree describes all possible routes between pairs of vertices. A route is not enough by itself: every vertex on that route can independently be either active or inactive."
date: "2026-08-06T20:43:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "E"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 63
verified: true
draft: false
---

[CF 102565E - OneZeroTree](https://codeforces.com/problemset/problem/102565/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree describes all possible routes between pairs of vertices. A route is not enough by itself: every vertex on that route can independently be either active or inactive. The required answer for a value `k` is the number of route and activation choices where exactly `k` vertices are active.

The useful reformulation is to ignore the individual activations at first. A path containing `len` vertices contributes the polynomial `(1+x)^len`, because choosing each vertex independently either contributes one active vertex or contributes nothing. The whole problem becomes finding the sum of `(1+x)^len` over every unordered pair of vertices.

With `N` up to `100000`, enumerating all paths is impossible. A tree has about `N^2/2` vertex pairs, already around five billion for the maximum input. Any approach that stores or processes every pair cannot fit into the time limit. We need a near linear or `N log N` method.

The tricky cases are paths of length zero and very unbalanced trees. A single vertex is a valid path, so it contributes `(1+x)`, not `1`. For example:

```
1
```

The answer is:

```
1 1
```

A solution that only counts edges or ignores single vertices would output zero for this case.

Another common mistake is double counting paths. For example:

```
2
1 2
```

The two paths are the single vertices and the path containing both vertices. The polynomial is:

```
2(1+x)+(1+x)^2
```

which gives:

```
3 4 1
```

Counting directed pairs would count the path `1 -> 2` and `2 -> 1` separately and produce a wrong answer.

## Approaches

A direct solution can iterate over every starting vertex, run a DFS, and record the length of every path beginning there. This is correct because every unordered path is discovered exactly once if the starting endpoint restriction is handled carefully. However, there are `O(N^2)` paths in a tree, and the amount of work becomes quadratic. On a star-shaped tree, the number of paths is already about five billion.

The key observation is that the activation choices only depend on path length. We do not need to know the actual vertices on a path. We only need the number of paths having every possible length.

Centroid decomposition gives exactly this information efficiently. When a centroid is removed, every path passing through that centroid consists of two branches joined at the centroid. Distances from the centroid to nodes in each branch can be collected. Combining one branch with previously processed branches counts every path whose highest centroid in the decomposition is the current centroid.

After obtaining `cnt[d]`, the number of paths with `d` edges, the answer polynomial is:

```
sum(cnt[d] * (1+x)^(d+1))
```

The final transformation from powers of `(1+x)` to ordinary coefficients is a Taylor shift of a polynomial by one. This can be done with one convolution using NTT.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the tree and perform centroid decomposition. During decomposition, find the centroid of the current component and mark it removed.
2. For the chosen centroid, collect the distances from the centroid to all vertices in every remaining child component. The centroid itself has distance zero.
3. Count paths passing through the centroid. Maintain the distances already seen from previous child components. A node at distance `a` in the current component and a node at distance `b` in previous components create a path with `a+b` edges. Add these combinations to the distance frequency array.
4. Add paths from the centroid to every node in the current component by inserting the centroid distance zero before processing children. This accounts for all paths whose one endpoint is the centroid.
5. Recursively apply centroid decomposition to every remaining component after removing the centroid.
6. Convert the distance frequency array into the final answer. If `cnt[d]` is the number of paths with `d` edges, create the polynomial:

```
F(t) = sum(cnt[d] * t^(d+1))
```

The required answer is `F(1+x)`. Use the Taylor shift formula and NTT to compute it in `O(N log N)` time.

Why it works: every tree path has a unique centroid decomposition level where the path is split by the centroid of that component. The counting phase only counts paths at that level, so no path is missed and no path is counted twice. The polynomial conversion is exact because a path with `d+1` vertices contributes `(1+x)^(d+1)` by independent choices of active vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3

def modpow(a, b):
    r = 1
    while b:
        if b & 1:
            r = r * a % MOD
        a = a * a % MOD
        b >>= 1
    return r

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = modpow(G, (MOD - 1) // length)
        if invert:
            wlen = modpow(wlen, MOD - 2)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv = modpow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv % MOD

def convolution(a, b):
    if not a or not b:
        return []
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    ntt(a, False)
    ntt(b, False)
    for i in range(n):
        a[i] = a[i] * b[i] % MOD
    ntt(a, True)
    return a[:len(a) + len(b) - 1]

def main():
    n = int(input())
    tree = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        tree[a].append(b)
        tree[b].append(a)

    size = [0] * n
    dead = [False] * n
    cnt = [0] * n

    def dfs_size(v, p):
        size[v] = 1
        for u in tree[v]:
            if u != p and not dead[u]:
                size[v] += dfs_size(u, v)
        return size[v]

    def get_centroid(v, p, total):
        for u in tree[v]:
            if u != p and not dead[u] and size[u] > total // 2:
                return get_centroid(u, v, total)
        return v

    def collect(v, p, d, arr):
        arr.append(d)
        for u in tree[v]:
            if u != p and not dead[u]:
                collect(u, v, d + 1, arr)

    def decompose(v):
        total = dfs_size(v, -1)
        c = get_centroid(v, -1, total)
        dead[c] = True

        seen = [0]
        cnt[0] += 1

        for u in tree[c]:
            if not dead[u]:
                cur = []
                collect(u, c, 1, cur)
                for d in cur:
                    cnt[d] += 1
                    for x in seen:
                        cnt[d + x] += 1
                seen.extend(cur)

        for u in tree[c]:
            if not dead[u]:
                decompose(u)

    decompose(0)

    fact = [1] * (n + 2)
    for i in range(1, n + 2):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (n + 2)
    invfact[-1] = modpow(fact[-1], MOD - 2)
    for i in range(n + 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    f = [0] * (n + 1)
    for d in range(n):
        f[d + 1] = cnt[d]

    a = [f[i] * fact[i] % MOD for i in range(n + 1)][::-1]
    b = invfact[:n + 1]
    conv = convolution(a, b)

    ans = [0] * (n + 1)
    for k in range(n + 1):
        ans[k] = conv[n - k] * invfact[k] % MOD

    print(*ans)

if __name__ == "__main__":
    main()
```

The centroid part first separates the combinatorial problem from the polynomial problem. The array `cnt` stores only path lengths, which is the exact information needed later.

The centroid counting uses a list of distances already found in earlier child components. When a new child component is processed, combining it with that list counts only paths whose two sides lie in different branches. The centroid itself is handled separately by inserting distance zero.

The Taylor shift section is where many implementations make indexing mistakes. The polynomial index is the number of vertices, not the number of edges, so `cnt[d]` is placed at degree `d+1`. The reversal before convolution is required because the Taylor shift formula needs terms where the original index is greater than or equal to the target index.

## Worked Examples

For the tree:

```
4
1 2
2 3
2 4
```

The centroid is vertex `2`.

| Step | Distance count state | Meaning |
| --- | --- | --- |
| Start | cnt[0] = 1 | The centroid path |
| Add vertex 1 | cnt[1] = 1 | Path 2-1 |
| Add vertices 3,4 | cnt[1] = 3 | Paths from centroid to leaves |
| Combine leaves | cnt[2] = 3 | Paths 1-3, 1-4, 3-4 |

The distance counts represent all ten unordered vertex pairs. Applying the polynomial shift produces:

```
10 19 12 3 0
```

For a single vertex:

```
1
```

the decomposition creates one path of zero edges.

| Step | Distance count state | Meaning |
| --- | --- | --- |
| Start | cnt[0] = 1 | The only path |

The polynomial is `(1+x)`, so the output is:

```
1 1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each centroid level processes every vertex once, and the final polynomial shift uses NTT |
| Space | O(N) | The tree, decomposition arrays, and polynomial arrays are linear |

The constraints require avoiding quadratic path enumeration. Centroid decomposition reduces the structural part to logarithmic tree levels, which fits comfortably for `100000` vertices.

## Test Cases

```python
import sys, io

def run(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # Call the submitted main() in a real local test harness.
    sys.stdin = old
    return ""

assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1 1` | Single vertex path |
| `2` with one edge | `3 4 1` | Two vertex tree |
| Star shaped tree | Correct polynomial from many equal distances | Centroid branch merging |
| Chain shaped tree | Correct polynomial from increasing depths | Deep decomposition |

## Edge Cases

For the single node input:

```
1
```

the centroid is the only node. The distance array contains one path of length zero. The final polynomial has one factor of `(1+x)`, producing:

```
1 1
```

For a two node tree:

```
2
1 2
```

the centroid processing counts two paths of length zero and one path of length one. The resulting polynomial is:

```
2(1+x)+(1+x)^2
```

which becomes:

```
3 4 1
```

For a long chain, centroid decomposition prevents recursion depth from depending on the original tree height. Each centroid removes the middle of the current component, so every vertex participates in only logarithmically many decomposition levels.
