---
title: "CF 1139C - Edgy Trees"
description: "We have a tree whose edges are colored either red (0) or black (1). We must count how many sequences of length k consisting of tree vertices are \"good\". For a sequence [a₁, a₂, ..."
date: "2026-06-12T03:50:37+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 1139
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 548 (Div. 2)"
rating: 1500
weight: 1139
solve_time_s: 86
verified: true
draft: false
---

[CF 1139C - Edgy Trees](https://codeforces.com/problemset/problem/1139/C)

**Rating:** 1500  
**Tags:** dfs and similar, dsu, graphs, math, trees  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree whose edges are colored either red (`0`) or black (`1`). We must count how many sequences of length `k` consisting of tree vertices are "good".

For a sequence `[a₁, a₂, ..., aₖ]`, we repeatedly travel along the unique shortest path in the tree from `a₁` to `a₂`, then from `a₂` to `a₃`, and so on. The sequence is considered good if at least one black edge is traversed somewhere during this entire journey.

The tree has up to `10^5` vertices, while `k` is at most `100`. The total number of possible sequences is `n^k`, which is astronomically large. Even iterating over all sequences is impossible. Since the tree itself contains `10^5` vertices, any solution that repeatedly computes paths between vertices will also fail. We need something close to linear in `n`.

The key difficulty is that goodness is defined by the presence of at least one black edge on the collection of paths induced by the sequence. Directly checking every sequence is hopeless, so we need to count them indirectly.

A subtle edge case occurs when every edge is black.

```
4 2
1 2 1
2 3 1
3 4 1
```

The only sequences that are not good are `[1,1]`, `[2,2]`, `[3,3]`, and `[4,4]`. Any movement between distinct vertices uses at least one black edge. A solution that only looks at connected components of black edges would completely miss the structure.

Another important case is when every edge is red.

```
4 3
1 2 0
2 3 0
3 4 0
```

No path contains a black edge, so the answer is `0`. A careless implementation that counts sequences touching multiple vertices would incorrectly report a positive answer.

A more subtle example is:

```
5 2
1 2 0
2 3 0
3 4 1
4 5 0
```

Vertices `{1,2,3}` form a red-only connected component. Sequences such as `[1,3]` are not good because their path stays entirely inside red edges. The same is true for `[5,5]`. The answer depends on the sizes of red-only components, not on individual vertices.

## Approaches

The brute-force idea is straightforward. Generate every sequence of length `k`, simulate the walk, and determine whether at least one traversed edge is black.

There are `n^k` sequences. With `n = 10^5` and `k = 100`, this number is beyond any conceivable computation. Even for tiny values, repeatedly computing paths in a tree would already be expensive. The brute-force approach is correct because it directly applies the definition, but it becomes unusable immediately.

To find something faster, it helps to think about the opposite question.

Instead of counting good sequences, count sequences that are **not** good.

A sequence is not good exactly when every traversed path consists entirely of red edges.

Consider removing all black edges from the tree. The remaining graph is a collection of connected components formed only by red edges.

Suppose all vertices in the sequence belong to the same red component. Then every shortest path between consecutive vertices lies entirely inside that component, so every traversed edge is red. The sequence is not good.

Suppose the sequence contains vertices from two different red components. Any path between those components must cross at least one removed edge, which means at least one black edge. Then the sequence is good.

This completely characterizes bad sequences:

A sequence is bad if and only if all its vertices belong to the same connected component of the graph formed by red edges.

If a red component has size `s`, then it contributes `s^k` bad sequences, because every position in the sequence may independently choose any vertex from that component.

The total number of sequences is `n^k`.

Hence:

`answer = n^k - Σ s^k`

where the sum runs over all red connected components.

Finding these component sizes is easy with DFS, BFS, or DSU after ignoring black edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k · n) or worse | O(n) | Too slow |
| Optimal | O(n + log k · number of components) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a graph using only red edges (`x = 0`).

Black edges are ignored because they separate the red-only regions that determine bad sequences.
2. Find all connected components of this red-only graph using DFS or BFS.

Every component represents a maximal set of vertices connected without using any black edge.
3. Compute `total = n^k mod M`, where `M = 10^9 + 7`.

This is the number of all possible sequences.
4. For each red component of size `s`, compute `s^k mod M` and subtract it from `total`.

Every sequence whose vertices all lie inside this component is bad.
5. Perform all arithmetic modulo `10^9 + 7`.
6. Output the final result.

### Why it works

After removing black edges, vertices split into red connected components.

If every vertex of a sequence belongs to the same component, then every path between consecutive vertices stays entirely within that component and uses only red edges. Such a sequence is bad.

If a sequence contains vertices from different components, some path between consecutive chosen vertices must cross a black edge, because distinct red components are disconnected without black edges. Such a sequence is good.

The bad sequences are partitioned by the component in which all their vertices lie. A component of size `s` contributes exactly `s^k` bad sequences. Summing over all components counts every bad sequence exactly once.

Subtracting the number of bad sequences from the total number of sequences leaves exactly the number of good sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n, k = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, x = map(int, input().split())
        u -= 1
        v -= 1

        if x == 0:
            g[u].append(v)
            g[v].append(u)

    visited = [False] * n

    ans = pow(n, k, MOD)

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        size = 0

        while stack:
            v = stack.pop()
            size += 1

            for to in g[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        ans = (ans - pow(size, k, MOD)) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The graph stores only red edges. This is the central observation of the solution. We are not interested in traversing black edges because they merely separate the regions that generate bad sequences.

The DFS computes the size of every red connected component. Since the original graph is a tree, the red-only graph contains at most `n - 1` edges, so traversing it remains linear.

The variable `ans` starts as `n^k`, the count of all sequences. Each component contributes `size^k` bad sequences, which are subtracted immediately.

Using Python's built-in `pow(base, exp, mod)` is important. The values `n^k` and `size^k` are enormous without modular exponentiation.

The subtraction is performed modulo `MOD`. Writing

```
(ans - value) % MOD
```

avoids negative intermediate values.

## Worked Examples

### Sample 1

Input:

```
4 4
1 2 1
2 3 1
3 4 1
```

All edges are black.

| Component | Size |
| --- | --- |
| {1} | 1 |
| {2} | 1 |
| {3} | 1 |
| {4} | 1 |

| Step | Value |
| --- | --- |
| Total sequences | 4⁴ = 256 |
| Subtract 1⁴ | 255 |
| Subtract 1⁴ | 254 |
| Subtract 1⁴ | 253 |
| Subtract 1⁴ | 252 |

Answer = `252`.

This demonstrates that only constant sequences remain bad. Any movement between distinct vertices crosses a black edge.

### Sample 2

```
4 3
1 2 0
2 3 0
3 4 0
```

All edges are red.

| Component | Size |
| --- | --- |
| {1,2,3,4} | 4 |

| Step | Value |
| --- | --- |
| Total sequences | 4³ = 64 |
| Subtract 4³ | 0 |

Answer = `0`.

This confirms that when every path is red-only, no sequence can be good.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + c log k) | DFS visits each vertex once, each component contributes one modular exponentiation |
| Space | O(n) | Adjacency list, visited array, DFS stack |

Here `c` is the number of red connected components, which is at most `n`. Since `k ≤ 100`, modular exponentiation is effectively constant time. The algorithm is linear in the size of the tree and easily fits within the limits for `n = 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, x = map(int, input().split())
        u -= 1
        v -= 1

        if x == 0:
            g[u].append(v)
            g[v].append(u)

    vis = [False] * n
    ans = pow(n, k, MOD)

    for i in range(n):
        if vis[i]:
            continue

        stack = [i]
        vis[i] = True
        sz = 0

        while stack:
            v = stack.pop()
            sz += 1

            for to in g[v]:
                if not vis[to]:
                    vis[to] = True
                    stack.append(to)

        ans = (ans - pow(sz, k, MOD)) % MOD

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue()

# sample 1
assert run(
"""4 4
1 2 1
2 3 1
3 4 1
"""
) == "252\n"

# all red
assert run(
"""4 3
1 2 0
2 3 0
3 4 0
"""
) == "0\n"

# minimum size, black edge
assert run(
"""2 2
1 2 1
"""
) == "2\n"

# minimum size, red edge
assert run(
"""2 2
1 2 0
"""
) == "0\n"

# two red components of size 2
assert run(
"""4 2
1 2 0
2 3 1
3 4 0
"""
) == "8\n"

# single vertex components
assert run(
"""3 2
1 2 1
2 3 1
"""
) == "6\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 vertices, black edge | 2 | Smallest non-trivial good case |
| 2 vertices, red edge | 0 | Entire tree is one red component |
| Two red components of size 2 | 8 | Correct counting of multiple components |
| All black edges on 3 vertices | 6 | Every singleton component contributes exactly one bad sequence |

## Edge Cases

Consider a tree consisting entirely of black edges.

```
4 2
1 2 1
2 3 1
3 4 1
```

Removing black edges leaves four isolated vertices. Component sizes are `1,1,1,1`.

The algorithm computes:

```
4² - 1² - 1² - 1² - 1²
= 16 - 4
= 12
```

The only bad sequences are `[1,1]`, `[2,2]`, `[3,3]`, and `[4,4]`. Every other sequence moves through at least one black edge.

Now consider a tree consisting entirely of red edges.

```
4 2
1 2 0
2 3 0
3 4 0
```

Removing black edges changes nothing. There is a single component of size `4`.

The algorithm computes:

```
4² - 4² = 0
```

Every path is red-only, so no sequence is good.

Finally, consider mixed colors.

```
5 2
1 2 0
2 3 0
3 4 1
4 5 0
```

The red components have sizes `3` and `2`.

The algorithm computes:

```
5² - 3² - 2²
= 25 - 9 - 4
= 12
```

The bad sequences are exactly those whose two vertices both belong to `{1,2,3}` or both belong to `{4,5}`. Any sequence connecting the two components must cross the black edge `(3,4)`, making it good. This is precisely the property the solution counts.
