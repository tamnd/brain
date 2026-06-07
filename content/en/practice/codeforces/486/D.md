---
title: "CF 486D - Valid Sets"
description: "We are given a tree where every vertex has an integer value. A set of vertices is considered valid if it is non-empty, forms a connected subgraph of the tree, and the difference between the largest and smallest value inside the set does not exceed d."
date: "2026-06-07T17:28:51+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "math", "trees"]
categories: ["algorithms"]
codeforces_contest: 486
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 277 (Div. 2)"
rating: 2100
weight: 486
solve_time_s: 118
verified: true
draft: false
---

[CF 486D - Valid Sets](https://codeforces.com/problemset/problem/486/D)

**Rating:** 2100  
**Tags:** dfs and similar, dp, math, trees  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where every vertex has an integer value. A set of vertices is considered valid if it is non-empty, forms a connected subgraph of the tree, and the difference between the largest and smallest value inside the set does not exceed `d`.

The task is to count how many such connected vertex sets exist.

The tree contains at most 2000 vertices, and every value is at most 2000. The limit of 2000 vertices is small enough that an `O(n²)` or `O(n² log n)` solution is realistic, but anything exponential in the number of vertices is impossible. Since a tree with 2000 vertices has 1999 edges, running a DFS from every vertex is completely feasible.

The difficult part is avoiding double counting. A connected set may contain many vertices having the same minimum value. If we simply enumerate connected subsets satisfying the value restriction, the same set can be discovered multiple times.

Consider a tiny example:

```
d = 0

1 -- 2
values: [5, 5]
```

The valid sets are `{1}`, `{2}`, and `{1,2}`.

If we try to count connected subsets rooted at every minimum-valued vertex, then `{1,2}` would be counted once from vertex 1 and again from vertex 2.

Another subtle case appears when several equal minima exist inside a larger connected component:

```
1 -- 2 -- 3
values: [1, 1, 2]
d = 1
```

The set `{1,2,3}` is valid. Any counting scheme that does not establish a unique representative minimum vertex will count this set multiple times.

A third edge case is `d = 0`. Then every valid set must consist entirely of vertices having the same value. The algorithm must naturally reduce to counting connected monochromatic subsets.

## Approaches

A brute-force solution would enumerate every subset of vertices, check whether it is connected, and verify that the maximum value minus the minimum value is at most `d`.

There are `2^n` subsets. Even for `n = 40`, this is already too large, while the actual limit is 2000. The brute-force approach is completely infeasible.

The tree structure suggests a different perspective. Instead of enumerating subsets directly, suppose we choose a vertex `r` that will serve as the minimum-valued vertex of the set.

Any valid set counted through `r` must satisfy two conditions.

First, every vertex in the set must have value between `a[r]` and `a[r] + d`.

Second, among vertices having value exactly `a[r]`, we need a tie-breaking rule so that each valid set is counted exactly once.

A very common technique on trees is to count connected subgraphs containing a distinguished root. Once the root is fixed, a tree DP can count all connected subsets containing that root.

For a chosen root `r`, let us only allow vertices whose values lie in the interval

```
[a[r], a[r] + d]
```

and additionally forbid any vertex with

```
a[v] = a[r] and v < r.
```

This tie-breaking rule makes `r` the smallest-index vertex among all vertices with the minimum value.

Now every valid set has exactly one representative root:

If a valid set has minimum value `m`, look at all vertices inside the set whose value equals `m`. Let `r` be the smallest index among them. The set will be counted when processing `r`, and it will be rejected for every other minimum-valued vertex because of the tie-breaking restriction.

Once the allowed vertices are fixed, we need to count connected subsets containing `r` inside the induced tree of allowed vertices.

This is a standard tree DP. For every vertex `u`, define `dp[u]` as the number of connected subsets inside the DFS subtree of `u` that contain `u`.

For every child `v`, we may either:

1. Take nothing from that child's side.
2. Attach any connected subset counted by `dp[v]`.

Hence the contribution of a child is `(dp[v] + 1)`, and

```
dp[u] = ∏ (dp[v] + 1).
```

The answer contributed by root `r` is `dp[r]`.

Repeating this DFS for every vertex gives the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and the values.
2. Iterate over every vertex `r` and treat it as the distinguished minimum vertex of a valid set.
3. While processing `r`, a vertex `v` is allowed if:

- `a[v] >= a[r]`
- `a[v] <= a[r] + d`
- if `a[v] == a[r]`, then `v >= r`

The last condition is the tie-breaking rule.
4. Run a DFS starting from `r`.
5. For each visited vertex `u`, compute the number of connected subsets containing `u` and lying completely inside the DFS subtree.
6. For every allowed child `v`, recursively compute `dp[v]`.
7. When combining a child, either ignore that branch or attach one of the connected subsets counted by `dp[v]`. Multiply the current result by `(dp[v] + 1)`.
8. Store the resulting product as `dp[u]`.
9. After the DFS finishes, add `dp[r]` to the global answer.
10. Repeat for all roots and output the sum modulo `10^9 + 7`.

### Why it works

Fix any valid connected set `S`.

Let `m` be its minimum value. Among vertices of `S` having value `m`, choose the smallest index `r`.

When processing root `r`, every vertex of `S` satisfies

```
m ≤ a[v] ≤ m + d,
```

and no vertex of value `m` has index smaller than `r`. Thus every vertex of `S` is allowed.

Since `S` is connected and contains `r`, the DFS DP has exactly one way to construct it.

Now consider any other root `x`.

If `a[x] > m`, then `x` cannot be the minimum value of `S`.

If `a[x] = m` and `x > r`, then `r` is forbidden by the tie-breaking rule while processing `x`, so `S` cannot be formed.

Thus every valid set is counted exactly once, and every counted set is valid. This establishes correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

d, n = map(int, input().split())
a = list(map(int, input().split()))

g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

sys.setrecursionlimit(10000)

answer = 0

for root in range(n):
    base = a[root]

    def dfs(u, parent):
        res = 1

        for v in g[u]:
            if v == parent:
                continue

            if a[v] < base or a[v] > base + d:
                continue

            if a[v] == base and v < root:
                continue

            res = (res * (dfs(v, u) + 1)) % MOD

        return res

    answer = (answer + dfs(root, -1)) % MOD

print(answer)
```

The outer loop chooses the representative minimum vertex. The variable `base` stores its value.

The DFS only traverses vertices that satisfy the value interval constraint. Vertices with the same value as the root but a smaller index are also excluded. This is the crucial tie-breaking condition that prevents duplicate counting.

The return value of `dfs(u, parent)` is the number of connected subsets that contain `u` and use only vertices from the DFS subtree below `u`.

For each child, there are exactly two choices. Either we ignore that entire branch, contributing `1`, or we connect one of the valid connected subsets containing the child, contributing `dp[child]`. Multiplying these choices across children gives the total count.

Since every multiplication is performed modulo `10^9 + 7`, overflow is avoided.

## Worked Examples

### Sample 1

Input:

```
1 4
2 1 3 2
1 2
1 3
3 4
```

Processing root 2 (value 1):

| Vertex | Allowed | dp |
| --- | --- | --- |
| 4 | Yes | 1 |
| 3 | No (value 3 > 2) | - |
| 1 | Yes | 1 |
| 2 | Yes | 2 |

The contribution is `2`, corresponding to:

```
{2}
{1,2}
```

Processing all roots produces total answer `8`.

This example demonstrates how the value window `[a[root], a[root]+d]` restricts which vertices may participate.

### Example 2

Input:

```
0 3
5 5 5
1 2
2 3
```

Processing root 1:

| Vertex | Allowed | dp |
| --- | --- | --- |
| 3 | Yes | 1 |
| 2 | Yes | 2 |
| 1 | Yes | 3 |

Contribution: `3`.

Processing root 2:

Vertex 1 is forbidden because it has the same value and a smaller index.

| Vertex | Allowed | dp |
| --- | --- | --- |
| 3 | Yes | 1 |
| 2 | Yes | 2 |

Contribution: `2`.

Processing root 3:

| Vertex | Allowed | dp |
| --- | --- | --- |
| 3 | Yes | 1 |

Contribution: `1`.

Total:

```
3 + 2 + 1 = 6
```

The six valid connected subsets are:

```
{1}
{2}
{3}
{1,2}
{2,3}
{1,2,3}
```

This trace shows how the tie-breaking rule distributes equal-minimum subsets among different roots without duplication.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | One DFS is executed for each root, and each DFS visits at most O(n) vertices |
| Space | O(n) | Adjacency list, recursion stack, and DFS state |

With `n ≤ 2000`, an `O(n²)` solution performs roughly four million edge traversals in the worst case, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    MOD = 1000000007

    input = sys.stdin.readline
    d, n = map(int, input().split())
    a = list(map(int, input().split())

    )
    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    sys.setrecursionlimit(10000)

    ans = 0

    for root in range(n):
        base = a[root]

        def dfs(u, p):
            res = 1

            for v in g[u]:
                if v == p:
                    continue
                if a[v] < base or a[v] > base + d:
                    continue
                if a[v] == base and v < root:
                    continue

                res = (res * (dfs(v, u) + 1)) % MOD

            return res

        ans = (ans + dfs(root, -1)) % MOD

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# sample 1
assert run(
"""1 4
2 1 3 2
1 2
1 3
3 4
"""
) == "8"

# minimum size
assert run(
"""0 1
7
"""
) == "1"

# all equal values on a chain
assert run(
"""0 3
5 5 5
1 2
2 3
"""
) == "6"

# no pair can coexist
assert run(
"""0 2
1 2
1 2
"""
) == "2"

# star, all values inside range
assert run(
"""10 3
1 2 3
1 2
1 3
"""
) == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 1 | Smallest possible tree |
| Chain with equal values | 6 | Tie-breaking among equal minima |
| Two vertices, d=0, different values | 2 | Value restriction filtering |
| Small star with large d | 6 | Counting all connected subsets |

## Edge Cases

Consider:

```
0 2
5 5
1 2
```

Valid sets are:

```
{1}
{2}
{1,2}
```

When root `1` is processed, both vertices are allowed and `{1,2}` is counted.

When root `2` is processed, vertex `1` is excluded because it has the same value and a smaller index. The set `{1,2}` cannot appear again. The final answer is correctly `3`.

Consider:

```
0 2
1 2
1 2
```

The only valid sets are `{1}` and `{2}` because the value difference inside `{1,2}` equals `1`, which exceeds `d=0`.

For root `1`, vertex `2` lies outside the allowed interval `[1,1]`.

For root `2`, vertex `1` lies outside the allowed interval `[2,2]`.

Each DFS contributes exactly one singleton set, producing answer `2`.

Consider:

```
1 3
1 2 2
1 2
2 3
```

The valid connected sets are:

```
{1}
{2}
{3}
{1,2}
{2,3}
{1,2,3}
```

The interval restriction allows all vertices when root `1` is chosen. The DP correctly generates every connected set containing that root. Roots `2` and `3` contribute only the sets whose minimum value is `2`. Every valid set appears exactly once because the representative minimum vertex is unique.
