---
title: "CF 102741J - E-Sports Tournament"
description: "The system maintains a social network of users. A friendship connection joins two users into the same friend group, where groups are connected components of the graph. For every tournament query, we are asked how many teams of exactly size s can be formed."
date: "2026-07-29T00:49:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102741
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 1"
rating: 0
weight: 102741
solve_time_s: 57
verified: true
draft: false
---

[CF 102741J - E-Sports Tournament](https://codeforces.com/problemset/problem/102741/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
# Problem Understanding

The system maintains a social network of users. A friendship connection joins two users into the same friend group, where groups are connected components of the graph. For every tournament query, we are asked how many teams of exactly size `s` can be formed. A team must come entirely from one friend group, and one group may contribute several teams as long as they do not share users. The answer is thus the sum of `floor(size_of_group / s)` over all current friend groups.

The input contains up to `10^5` users and `10^5` operations. Friendship operations only add edges, so the connected components can be maintained with a disjoint set union structure. However, a query can ask for any team size from `1` to `n`, which means recomputing all components for every query is impossible. With `10^5` operations, even an `O(n)` answer per query would approach `10^10` operations and cannot fit in typical contest limits.

The difficult part is not maintaining the connected components. The difficult part is keeping the values `sum floor(component_size / s)` for every possible `s` while component sizes change.

A common mistake is to update every possible team size after a merge. For example, if a component grows from size `1` to size `50000`, directly changing every `s` up to `50000` works for one merge, but thousands of merges would make the solution too slow.

Another edge case is handling size `1` components. Initially every user is alone, so a query for team size `1` must return `n`, while a query for any larger size must return `0`.

Example:

```
5 3
2 1
2 2
1 1 2
```

The first query asks for teams of size `1`, so the answer is `5`. After users `1` and `2` become friends, the groups have sizes `2,1,1,1`, so a size `2` team query returns `1`, not `2`, because the group of two users can only provide one complete team.

Another edge case is merging already connected users. The friendship graph does not change when two users in the same group become friends again. A careless implementation might remove the component twice and corrupt the stored counts.

Example:

```
3 3
1 1 2
1 2 1
2 2
```

The final component sizes are `2,1`, so the answer is `1`. The second union operation must be ignored.

## Approaches

A straightforward solution uses disjoint set union to maintain components. For every query of type `2`, we could iterate over all current component sizes and calculate how many teams each component contributes. This is correct because each group independently contributes `size // s` teams.

The problem is the query cost. There can be `10^5` queries, and there can also be `10^5` components. In the worst case this approach performs around `10^10` operations, which is too slow.

The key observation is that a component of size `x` contributes `floor(x / s)` to the answer of every team size `s`. We do not need to update all `s` individually. The value of `floor(x / s)` changes only about `2 * sqrt(x)` times. For example, all `s` values in a certain interval may produce the same quotient.

This allows us to represent the effect of adding or removing a component as a small number of range additions. Since queries ask for one particular `s`, a Fenwick tree over a difference array can support range additions and point queries.

When two components of sizes `a` and `b` merge into size `a+b`, we remove the contributions of `a` and `b` and add the contribution of `a+b`. The DSU handles the connectivity, while the Fenwick tree maintains the answers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nq)` | `O(n)` | Too slow |
| Optimal | `O((n+q) * sqrt(n) * log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Initialize every user as its own DSU component. A single user contributes `floor(1/s)` teams, so the initial contribution can be added using the same component update routine.
2. Maintain a Fenwick tree that stores range additions. The value at position `s` represents the current number of valid teams of size `s`.
3. When adding a component of size `x`, find every interval of team sizes where `floor(x/s)` has the same value. For every such interval `[l,r]`, add that quotient to the Fenwick tree over that range.
4. When removing a component, perform the same process with the opposite sign. This keeps every possible team size answer synchronized with the current component sizes.
5. For a friendship operation, find the two DSU roots. If they are already equal, nothing changes. Otherwise remove both old component contributions, merge the DSU sets, and add the contribution of the new component size.
6. For a tournament query with team size `s`, ask the Fenwick tree for the value at position `s`.

The reason the quotient intervals are small is that `floor(x/s)` decreases slowly at first and then changes rapidly near the end. The number of distinct values is bounded by `O(sqrt(x))`, so each component update is efficient.

Why it works:

The maintained invariant is that the Fenwick tree value at every position `s` equals the sum of `floor(size/s)` over all current connected components. Initially this is true because every component is inserted. A merge removes exactly the two old components and inserts exactly the new one, so the invariant remains true after every friendship operation. A query simply reads the maintained value for the requested team size, which is exactly the required number of teams.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def range_add(self, l, r, val):
        if l > r:
            return
        self.add(l, val)
        self.add(r + 1, -val)

    def query(self, idx):
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    n, q = map(int, input().split())

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    fw = Fenwick(n)

    def update_component(x, delta):
        l = 1
        while l <= x:
            val = x // l
            r = x // val
            fw.range_add(l, r, val * delta)
            l = r + 1

    update_component(1, n)

    ans = []

    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 1:
            a, b = query[1], query[2]
            ra, rb = find(a), find(b)
            if ra != rb:
                update_component(size[ra], -1)
                update_component(size[rb], -1)
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
                update_component(size[ra], 1)
        else:
            ans.append(str(fw.query(query[1])))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The Fenwick tree stores a difference array rather than the answers directly. A range update adds at the left boundary and subtracts after the right boundary, and a prefix sum reconstructs the current answer for a specific team size.

The `update_component` function is the core optimization. It walks through intervals where `x // s` is constant. The line `r = x // val` jumps directly to the end of the current interval, avoiding a loop over every possible team size.

The DSU uses path compression and union by size. The merge order is handled carefully because the stored component size belongs to the root after the merge. If both users already have the same root, no contribution changes are made.

## Worked Examples

For the first sample:

```
5 6
2 2
1 1 2
2 2
2 3
1 1 3
2 3
```

| Step | Operation | Component sizes | Query answer |
| --- | --- | --- | --- |
| 0 | Initial state | `1,1,1,1,1` |  |
| 1 | Ask size `2` | `1,1,1,1,1` | `0` |
| 2 | Merge `1,2` | `2,1,1,1` |  |
| 3 | Ask size `2` | `2,1,1,1` | `1` |
| 4 | Ask size `3` | `2,1,1,1` | `0` |
| 5 | Merge `1,3` | `3,1,1` |  |
| 6 | Ask size `3` | `3,1,1` | `1` |

This trace shows that only complete teams count. A component of size `3` can provide one team of size `3`, while smaller components contribute nothing.

For the second sample:

```
7 9
2 1
2 2
1 1 2
1 2 3
1 4 5
1 5 6
1 6 7
2 3
2 4
```

| Step | Operation | Component sizes | Query answer |
| --- | --- | --- | --- |
| 0 | Initial state | `1,1,1,1,1,1,1` |  |
| 1 | Ask size `1` | `1,1,1,1,1,1,1` | `7` |
| 2 | Ask size `2` | `1,1,1,1,1,1,1` | `0` |
| 3 | Merge `1,2` | `2,1,1,1,1,1` |  |
| 4 | Merge `2,3` | `3,1,1,1,1` |  |
| 5 | Merge `4,5` | `3,2,1,1` |  |
| 6 | Merge `5,6` | `3,3,1` |  |
| 7 | Merge `6,7` | `3,4` |  |
| 8 | Ask size `3` | `3,4` | `2` |
| 9 | Ask size `4` | `3,4` | `1` |

The trace confirms that the answer depends only on component sizes, not on the internal arrangement of friendships.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n+q) sqrt(n) log n)` | Each merge changes three components, and each component update uses `O(sqrt(n))` quotient intervals with Fenwick operations. |
| Space | `O(n)` | DSU arrays and Fenwick tree each store linear-sized data. |

The constraints allow about `10^5` operations. The optimized quotient decomposition avoids the linear update cost that would make every merge too expensive, keeping the total work within the required limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = []
    n, q = map(int, input().split())

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 2)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def ra(self, l, r, v):
            self.add(l, v)
            self.add(r + 1, -v)
        def get(self, i):
            s = 0
            while i:
                s += self.bit[i]
                i -= i & -i
            return s

    fw = Fenwick(n)

    def add_comp(x, d):
        l = 1
        while l <= x:
            v = x // l
            r = x // v
            fw.ra(l, r, v * d)
            l = r + 1

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    add_comp(1, n)

    for _ in range(q):
        a = list(map(int, input().split()))
        if a[0] == 1:
            x, y = find(a[1]), find(a[2])
            if x != y:
                add_comp(size[x], -1)
                add_comp(size[y], -1)
                parent[y] = x
                size[x] += size[y]
                add_comp(size[x], 1)
        else:
            out.append(str(fw.get(a[1])))

    sys.stdin = old
    return "\n".join(out)

assert run("""5 6
2 2
1 1 2
2 2
2 3
1 1 3
2 3
""") == "0\n1\n0\n1"

assert run("""3 3
1 1 2
1 2 1
2 2
""") == "1"

assert run("""1 3
2 1
2 2
2 1
""") == "1\n0\n1"

assert run("""6 5
1 1 2
1 2 3
1 4 5
1 5 6
2 3
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single user queries | `1,0,1` | Minimum size and team size larger than population |
| Repeated friendship | `1` | Ignoring unions inside one component |
| Two components of sizes `3` and `3` | `2` | Multiple groups contributing teams |

## Edge Cases

When every user is alone, the algorithm inserts `n` copies of a size `1` component. The update routine handles this by adding `1` only to team size `1`, so larger team sizes remain zero.

For repeated friendships, DSU finds that both users have the same root. Since no component size changes, the Fenwick tree is untouched and the stored answers remain valid.

For a large component, such as one of size `100000`, the algorithm does not loop over all possible team sizes. Instead it jumps between equal quotient ranges. This keeps the update cost small even when a single friend group contains every user.
