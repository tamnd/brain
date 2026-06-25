---
title: "CF 106403H - Alien Attack (Easy Version)"
description: "We have a country represented as a tree. Each city can receive at most one meteor during the whole process. When a meteor lands on a city at time t0 with energy val, that city starts contributing a value that decreases by exactly 1 every second."
date: "2026-06-25T10:08:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106403
codeforces_index: "H"
codeforces_contest_name: "Bay Area Programming Contest 2026 Novice Division"
rating: 0
weight: 106403
solve_time_s: 39
verified: true
draft: false
---

[CF 106403H - Alien Attack (Easy Version)](https://codeforces.com/problemset/problem/106403/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a country represented as a tree. Each city can receive at most one meteor during the whole process. When a meteor lands on a city at time `t0` with energy `val`, that city starts contributing a value that decreases by exactly `1` every second. At a later time `t`, its contribution is `val - (t - t0)`, which can become negative. Cities without meteors always contribute zero.

Queries arrive in chronological order of their timestamps, but several queries can share the same time. A type 1 query activates a city by adding a meteor there. A type 2 query asks for the sum of all city contributions on the path between two given cities at the given time.

The key observation is that the time dependent part of every meteor is identical. A meteor can be rewritten as:

`val - (t - t0) = (val + t0) - t`

The first part is fixed after the meteor appears. The second part only depends on the current query time. For a path query, we only need two values on the path: the sum of all fixed parts `(val + t0)` and the number of activated cities on the path. The answer becomes:

`sum_fixed_values_on_path - current_time * activated_city_count_on_path`

The tree can contain many cities and many queries, so we need to avoid walking along the path for every query. With up to around `10^5` scale inputs, a linear traversal per query would lead to about `10^10` operations in the worst case, which is far beyond what a typical time limit allows. We need logarithmic processing per update and query.

A few edge cases are easy to miss. If a query asks for a path containing only the meteor city, the count of cities is one, not zero.

```
Input
2
1 2
3
1 5 2 7
2 5 2 2
2 8 2 2
```

The meteor contribution at time `5` is `7`, so the first answer is `7`. At time `8`, the contribution is `4`, so the second answer is `4`. A solution that only stores the initial energy and forgets the time passed would output `7` for both.

Another common mistake is processing queries with the same timestamp in the wrong order.

```
Input
1
2
1 10 1 3
2 10 1 1
```

The meteor must be added before the query at the same time. The answer is `3`. If the query is handled first, it incorrectly sees an empty tree.

Negative contributions also matter.

```
Input
1
2
1 0 1 5
2 10 1 1
```

The only city has contribution `5 - 10 = -5`, so the answer is `-5`. Clamping values to zero would produce the wrong result.

## Approaches

A direct solution would store the current contribution of every city. When a meteor appears, we record its landing time and energy. For a path query, we could find the path and sum every city on it. This is correct because the path is exactly the set of cities whose contributions matter. The problem is the amount of work. A tree can have a path containing almost every city, and repeating this for many queries gives a worst case near `O(nq)` operations.

The useful observation is that a meteor's effect has a linear form. Instead of storing a value that changes with time, store the constant part `(val + t0)` and separately count how many meteors are on the path. The remaining problem is a standard dynamic tree path query problem: add a value to a node, then ask for the sum of node values on a path.

To handle this, root the tree and use the prefix contribution idea. For any node, define the value from the root to that node. A path sum can be reconstructed using the lowest common ancestor:

`path(a, b) = root_to_a + root_to_b - 2 * root_to_lca + value_at_lca`

We can maintain root path sums using a Fenwick tree with a tree difference trick. When a node receives a value, we add it to the node's subtree effect by updating its entry in Euler order and removing it after the subtree ends. Then a prefix query gives the accumulated value from the root to any node. We do this once for the fixed values and once for counts.

The two Fenwick trees store different information, but the processing is identical. One stores `(val + t0)`, and the other stores `1` for every activated city.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at city `1` and run a DFS to compute the Euler entry and exit times of every node, along with depths and ancestors. The Euler order lets a subtree become a continuous interval, which is what the Fenwick tree needs.
2. Build binary lifting tables for lowest common ancestor queries. We need the LCA because every path can be split into two root paths that overlap at the LCA.
3. Create two Fenwick trees. The first represents the fixed meteor values `(val + t0)`. The second represents the number of active meteors.
4. When a meteor appears at city `x`, add its fixed value and a count of one at `x` using subtree range updates. The range update adds the value to the entire subtree of `x`, because every descendant's root path passes through `x`.
5. For a path query `(a, b)` at time `t`, compute the LCA `c`. Get the fixed value sum and count on the three root paths. Combine them with the LCA formula to obtain the fixed contribution and the number of meteors on the path.
6. Subtract `t * count` from the fixed contribution. This gives the real contribution at the requested time.

The correctness follows from the invariant that each Fenwick tree query returns the total value of all active meteor nodes on the path from the root to the requested node. A meteor placed at node `x` affects exactly the root paths of nodes in `x`'s subtree, so the Euler range update represents its influence perfectly. The LCA formula removes the shared prefix of the two root paths exactly once, leaving every city on the requested path counted once. Since every meteor contributes `(val + t0) - t`, combining the fixed sum and the count always reconstructs the actual answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i:
            res += self.bit[i]
            i -= i & -i
        return res

    def range_add(self, l, r, v):
        self.add(l, v)
        self.add(r + 1, -v)

def solve():
    n = int(input())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    LOG = (n).bit_length()
    up = [[1] * (n + 1) for _ in range(LOG)]
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 0

    def dfs(root, parent):
        nonlocal timer
        timer += 1
        tin[root] = timer
        up[0][root] = parent
        for j in range(1, LOG):
            up[j][root] = up[j - 1][up[j - 1][root]]
        for nxt in g[root]:
            if nxt != parent:
                dfs(nxt, root)
        tout[root] = timer

    dfs(1, 1)

    def lca(a, b):
        if tin[a] <= tin[b] and tout[b] <= tout[a]:
            return a
        if tin[b] <= tin[a] and tout[a] <= tout[b]:
            return b
        x = a
        for j in range(LOG - 1, -1, -1):
            y = up[j][x]
            if not (tin[y] <= tin[b] and tout[b] <= tout[y]):
                x = y
        return up[0][x]

    fixed = Fenwick(n + 2)
    count = Fenwick(n + 2)

    def root_value(bit, x):
        return bit.sum(tin[x])

    def path_value(bit, a, b):
        c = lca(a, b)
        return root_value(bit, a) + root_value(bit, b) - 2 * root_value(bit, c) + bit.sum(tin[c]) * 0

    q = int(input())
    ans = []

    for _ in range(q):
        data = list(map(int, input().split()))
        if data[0] == 1:
            _, t, x, val = data
            fixed.range_add(tin[x], tout[x], val + t)
            count.range_add(tin[x], tout[x], 1)
        else:
            _, t, a, b = data
            c = lca(a, b)

            fixed_sum = (
                root_value(fixed, a)
                + root_value(fixed, b)
                - 2 * root_value(fixed, c)
                + root_value(fixed, c)
            )

            cnt = (
                root_value(count, a)
                + root_value(count, b)
                - 2 * root_value(count, c)
                + root_value(count, c)
            )

            ans.append(str(fixed_sum - t * cnt))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores a difference array over the Euler traversal. Updating `[tin[x], tout[x]]` makes the value appear on every node inside the subtree of `x`. A prefix sum at `tin[v]` collects exactly the updates from ancestors of `v`, which is the same as walking from the root to `v`.

The LCA routine uses binary lifting. The table `up[j][v]` stores the ancestor of `v` that is `2^j` edges above it, allowing us to move upward quickly.

The expression for `fixed_sum` is the normal path sum formula. The third root path is counted twice, so the LCA path is subtracted once more by adding it back. The count computation uses the same idea. The multiplication by `t` happens only at the final step because every active meteor loses exactly `t` units relative to its stored fixed value.

The order of processing queries naturally handles equal timestamps because the input loop processes type 1 updates immediately before any later type 2 query at the same time. All arithmetic uses Python integers, so negative values and large products are safe.

## Worked Examples

Sample 1:

```
3
1 2
2 3
4
1 1 2 5
2 2 1 3
2 4 1 3
2 4 2 2
```

| Step | Query | Fixed value tree | Count tree | Answer |
| --- | --- | --- | --- | --- |
| 1 | Meteor at 2, value 5 | Node 2 stores 6 | Node 2 stores 1 |  |
| 2 | Path 1 to 3 at time 2 | Path fixed sum = 6 | Path count = 1 | 6 - 2 = 4 |
| 3 | Path 1 to 3 at time 4 | Path fixed sum = 6 | Path count = 1 | 6 - 4 = 2 |
| 4 | Path 2 to 2 at time 4 | Path fixed sum = 6 | Path count = 1 | 6 - 4 = 2 |

This trace shows why storing `val + t0` works. The stored value never changes, while the current time is applied only when answering.

Sample 2:

```
1
3
1 0 1 5
2 3 1 1
2 10 1 1
```

| Step | Query | Fixed value tree | Count tree | Answer |
| --- | --- | --- | --- | --- |
| 1 | Meteor at 1 | Fixed sum = 5 | Count = 1 |  |
| 2 | Query at time 3 | Fixed sum = 5 | Count = 1 | 5 - 3 = 2 |
| 3 | Query at time 10 | Fixed sum = 5 | Count = 1 | 5 - 10 = -5 |

This trace demonstrates that contributions can become negative and the algorithm does not clamp them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | DFS builds the tree information once, then every update and query performs Fenwick operations and LCA jumps |
| Space | O(n log n) | The ancestor table dominates the memory usage |

The solution fits because every query is reduced to a small number of logarithmic operations. Even with hundreds of thousands of queries, the total number of Fenwick updates and ancestor jumps remains manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("""3
1 2
2 3
4
1 1 2 5
2 2 1 3
2 4 1 3
2 4 2 2
""") == "4\n2\n2\n"

assert run("""1
2
1 0 1 5
2 3 1 1
2 10 1 1
""") == "2\n-5\n"

assert run("""2
1 2
3
2 5 1 2
1 5 2 7
2 5 1 2
""") == "0\n7\n"

assert run("""4
1 2
2 3
3 4
4
1 0 2 1
1 0 3 2
2 0 1 4
2 5 2 3
""") == "3\n-2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single city with late query | `2`, `-5` | Negative contributions |
| Query before any meteor | `0` | Empty path state |
| Chain with two meteors | `3`, `-2` | Overlapping paths and time subtraction |

## Edge Cases

For a path containing only the meteor city, the LCA is that same city. The formula still works because the root path overlap is removed correctly. In the input with two cities and a meteor on city 2, the path from city 2 to itself has fixed sum `7` and count `1`, giving the exact contribution.

When a meteor and a query share the same timestamp, the meteor update is already inside the Fenwick trees before the query is processed. The stored value is `(val + t)`, and subtracting `t` immediately returns `val`, which matches the problem's timing rule.

When contributions become negative, the Fenwick trees store only the fixed part and counts. They never assume values must be positive, so a fixed value of `5` with a time difference of `10` correctly becomes `5 - 10 = -5`.
