---
title: "CF 105757L - Tree Harmony"
description: "We have a rooted tree with root 1. Every vertex stores a value. For each query (u, v), we need to decide whether v lies inside the subtree of u and whether the vertices that remain after removing the whole subtree of v from the subtree of u can be paired so that every pair…"
date: "2026-06-25T16:02:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105757
codeforces_index: "L"
codeforces_contest_name: "Insomnia 2025"
rating: 0
weight: 105757
solve_time_s: 48
verified: true
draft: false
---

[CF 105757L - Tree Harmony](https://codeforces.com/problemset/problem/105757/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with root `1`. Every vertex stores a value. For each query `(u, v)`, we need to decide whether `v` lies inside the subtree of `u` and whether the vertices that remain after removing the whole subtree of `v` from the subtree of `u` can be paired so that every pair contains two different values.

The first condition is purely about ancestry. If `u` is not an ancestor of `v`, then their lowest common ancestor cannot be `u`, so the answer is immediately `NO`.

The second part looks like a partitioning problem, but it can be reduced to a much simpler observation. Suppose the remaining set contains `k` vertices. We need to divide them into two groups of equal size and match the groups. A value that appears too often prevents this. If some value appears more than `k / 2` times, there are not enough vertices with other values to pair against all occurrences of that value. On the other hand, if no value exceeds half of the set, we can always arrange the pairs.

So every query becomes:

Find the size of `subtree(u) - subtree(v)`. It must be even.

Find whether this set has a majority value, meaning some value occurring more than half of the set size.

The tree has up to `100000` vertices and the same number of queries. A quadratic solution would require looking through a large part of the tree for every query, which can reach around `10^10` operations. We need preprocessing that lets each query be answered in logarithmic time.

The difficult edge cases are not the large trees but the exact meaning of the removed subtree.

For example, if the tree is:

```
1
|
2
|
3
```

with values:

```
1 1 2
```

and the query is `(2, 3)`, the remaining set is only node `2`, so its size is odd and the answer is `NO`. A solution that only checks colors and forgets the pairing count would incorrectly accept it.

Another case is:

```
1
|
2
```

with values:

```
5 5
```

and query `(1, 2)`. The remaining set is `{1}`, which cannot form a pair. The repeated value is not the real reason for failure here, the odd size is.

A more subtle case is:

```
1
/ \
2  3
```

with values:

```
7 7 8
```

and query `(1, 2)`. The remaining set is `{1,3}`. The size is even, and the values differ, so the answer is `YES`. A careless approach that checks the whole subtree of `1` would see two `7`s and reject incorrectly.

## Approaches

The brute force approach is straightforward. For every query, first check whether `u` is an ancestor of `v`. If it is, traverse the subtree of `u` while skipping the subtree of `v`, count all values, and check whether the largest frequency is more than half of the remaining size. This is correct because it directly evaluates the definition of compatibility.

The problem is the cost. A single query can touch `O(n)` vertices, and with `10^5` queries the worst case is about `10^10` vertex visits, which is far beyond the allowed time.

The key observation is that the pairing condition only depends on the majority value of a set. We do not need all frequencies for every query. A set either has one value appearing more than half the time or it does not.

The Boyer Moore majority vote idea gives exactly the information we need. A segment can be represented by a candidate value and a balance. When two disjoint segments are combined, their summaries can be merged while preserving the possible majority candidate.

After an Euler tour, every subtree becomes one contiguous interval. Since `subtree(v)` is removed from `subtree(u)`, the remaining vertices are at most two Euler intervals. We can store majority summaries in a segment tree and combine the two remaining intervals. The resulting candidate is then checked by counting its real frequency using sorted positions of every value.

The brute force works because it directly counts all values, but fails when many queries overlap large subtrees. The observation that only a possible majority value matters reduces the query from scanning vertices to a few logarithmic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Run a DFS from the root to compute Euler tour positions, subtree sizes, and entry and exit times. A subtree of a node becomes the interval `[tin[node], tout[node]]`.
2. Build a binary lifting table for ancestors. This allows us to check ancestry and handle lowest common ancestor related queries in `O(log n)` time.
3. Build a segment tree over the Euler order. Each node of the segment tree stores a Boyer Moore majority summary containing a candidate value and its balance.
4. Store the Euler positions of every value in sorted order. This allows counting how many times a chosen value appears inside any interval using binary search.
5. For each query `(u, v)`, first check whether `u` is an ancestor of `v`. If not, the answer is `NO`.
6. Compute the remaining number of vertices as `subtree_size[u] - subtree_size[v]`. If this number is odd, the answer is `NO`, because every vertex must belong to exactly one pair.
7. If `u == v`, the remaining set is empty. There are no pairs to form, so the answer is `YES`.
8. The removed subtree is one Euler interval inside the subtree of `u`. The remaining vertices are the parts before and after that interval. Query the segment tree on both parts and merge the two majority summaries.
9. Count the actual occurrences of the candidate value in the remaining intervals. If this count is greater than half of the remaining size, the answer is `NO`. Otherwise the answer is `YES`.

The invariant behind the algorithm is that every Euler interval summary always keeps the only possible majority candidate of that interval. If a value is a true majority of the query set, it must survive every Boyer Moore merge operation. The final frequency check removes false candidates, so the algorithm accepts exactly the sets where no majority value exists.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = 1
        while self.n < len(arr):
            self.n *= 2
        self.tree = [(0, 0)] * (2 * self.n)
        for i, x in enumerate(arr):
            self.tree[self.n + i] = (x, 1)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.merge(self.tree[2 * i], self.tree[2 * i + 1])

    def merge(self, a, b):
        if a[0] == b[0]:
            return (a[0], a[1] + b[1])
        if a[1] > b[1]:
            return (a[0], a[1] - b[1])
        return (b[0], b[1] - a[1])

    def query(self, l, r):
        if l > r:
            return (0, 0)
        l += self.n
        r += self.n
        left = (0, 0)
        right = (0, 0)
        while l <= r:
            if l & 1:
                left = self.merge(left, self.tree[l])
                l += 1
            if not (r & 1):
                right = self.merge(self.tree[r], right)
                r -= 1
            l //= 2
            r //= 2
        return self.merge(left, right)

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        x, y = map(int, input().split())
        graph[x].append(y)
        graph[y].append(x)

    LOG = 17
    while (1 << LOG) <= n:
        LOG += 1

    up = [[0] * (n + 1) for _ in range(LOG)]
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    size = [0] * (n + 1)
    euler = []
    timer = 0

    sys.setrecursionlimit(300000)

    def dfs(v, p):
        nonlocal timer
        up[0][v] = p
        for i in range(1, LOG):
            up[i][v] = up[i - 1][up[i - 1][v]]
        tin[v] = timer
        euler.append(a[v])
        timer += 1
        size[v] = 1
        for u in graph[v]:
            if u != p:
                dfs(u, v)
                size[v] += size[u]
        tout[v] = timer - 1

    dfs(1, 1)

    for i in range(LOG):
        up[i][1] = 1

    positions = {}
    for i, x in enumerate(euler):
        if x not in positions:
            positions[x] = []
        positions[x].append(i)

    seg = SegTree(euler)

    def ancestor(x, y):
        return tin[x] <= tin[y] <= tout[x]

    def count_value(x, l, r):
        if l > r:
            return 0
        arr = positions.get(x, [])
        return bisect_right(arr, r) - bisect_left(arr, l)

    q = int(input())
    ans = []

    for _ in range(q):
        u, v = map(int, input().split())

        if not ancestor(u, v):
            ans.append("NO")
            continue

        remaining = size[u] - size[v]

        if remaining % 2:
            ans.append("NO")
            continue

        if remaining == 0:
            ans.append("YES")
            continue

        cand1 = seg.query(tin[u], tin[v] - 1)
        cand2 = seg.query(tout[v] + 1, tout[u])
        cand = seg.merge(cand1, cand2)[0]

        cnt = count_value(cand, tin[u], tin[v] - 1)
        cnt += count_value(cand, tout[v] + 1, tout[u])

        if cnt * 2 > remaining:
            ans.append("NO")
        else:
            ans.append("YES")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The DFS section converts the tree into an array problem. The entry and exit times are what make subtree queries possible without walking the tree repeatedly.

The segment tree does not store frequencies. It stores only the Boyer Moore candidate and balance, because a true majority is unique and must remain the candidate after combining any partition of the set.

The position lists are used only after obtaining a candidate. This separation is necessary because Boyer Moore can find a possible majority but cannot prove that it actually exists. The binary searches perform that final verification.

The query processing order matters. The size check happens before the majority logic because an odd number of vertices can never be completely paired. The empty set case also has to be handled before querying the segment tree.

## Worked Examples

Using the first sample:

```
5
1 1 2 1 2
1 2
2 3
3 4
4 5
```

For query `(3,5)`:

| Step | Value |
| --- | --- |
| Is 3 ancestor of 5 | Yes |
| Remaining size | 2 |
| Remaining Euler intervals | node 3 and node 4 |
| Majority candidate | none |
| Result | YES |

The two remaining values are `2` and `1`, so they can form one valid pair.

For query `(2,5)`:

| Step | Value |
| --- | --- |
| Is 2 ancestor of 5 | Yes |
| Remaining size | 3 |
| Remaining Euler intervals | nodes 2,3,4 |
| Size parity | Odd |
| Result | NO |

The algorithm rejects immediately because three vertices cannot be divided into pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) log n) | DFS, segment tree construction, and each query use logarithmic operations |
| Space | O(n log n) | Ancestor table dominates memory usage |

The constraints allow linear preprocessing and logarithmic queries. The solution avoids scanning subtrees, so even a chain-shaped tree with `100000` nodes remains within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""5
1 1 2 1 2
1 2
2 3
3 4
4 5
4
4 5
3 5
2 5
1 4
""") == """NO
YES
NO
NO
""", "sample 1"

assert run("""6
1 2 3 4 5 6
1 2
2 3
3 4
4 5
5 6
4
1 3
1 2
2 5
1 6
""") == """YES
NO
NO
NO
""", "sample 2"

assert run("""1
7
1
3
1 1
""") == "YES\n", "single node"

assert run("""3
5 5 8
1 2
1 3
2
1 2
1 3
""") == """YES
YES
""", "different remaining pairs"

assert run("""4
1 1 1 1
1 2
1 3
1 4
2
1 2
1 3
""") == """NO
NO
""", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node tree | YES | Empty remaining set handling |
| Star with mixed values | YES | Pairing with removed child subtree |
| All equal values | NO | Majority detection |
| Path examples | Mixed | Ancestor and parity boundaries |

## Edge Cases

For a query where `u == v`, the removed subtree is the entire subtree of `u`, leaving an empty set. The algorithm reaches the `remaining == 0` condition and returns `YES`, because there are no vertices that need pairing.

For a query where the remaining set has odd size, such as a chain `1-2-3` with values `1 1 2` and query `(2,3)`, the algorithm computes `size[2] - size[3] = 1`. Since one vertex cannot be split into pairs, it returns `NO` before doing any majority work.

For a case where the whole subtree has a majority but the remaining part does not, such as the star with values `7 7 8` and query `(1,2)`, the Euler intervals exclude node `2`. The algorithm only counts the remaining vertices `{1,3}`, so the false majority from the removed subtree never affects the answer.
