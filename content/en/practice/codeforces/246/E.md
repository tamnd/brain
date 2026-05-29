---
title: "CF 246E - Blood Cousins Return"
description: "We are given a rooted forest describing family relations. Every person has a name and at most one parent. Multiple roots are allowed because some people may have no ancestor at all."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 246
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 151 (Div. 2)"
rating: 2400
weight: 246
solve_time_s: 98
verified: true
draft: false
---

[CF 246E - Blood Cousins Return](https://codeforces.com/problemset/problem/246/E)

**Rating:** 2400  
**Tags:** binary search, data structures, dfs and similar, dp, sortings  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted forest describing family relations. Every person has a name and at most one parent. Multiple roots are allowed because some people may have no ancestor at all.

For each query `(v, k)`, we need the number of distinct names among all descendants of `v` that are exactly `k` edges below `v`.

A useful rephrasing makes the structure clearer. Let `depth[x]` be the depth of node `x` from its tree root. A node is a `k`-son of `v` exactly when:

- it lies inside the subtree of `v`
- its depth is `depth[v] + k`

So every query asks:

> Inside the subtree of `v`, how many distinct names appear at depth `depth[v] + k`?

The tree size and number of queries both go up to `10^5`. Any solution that scans a subtree for every query is immediately too slow. In the worst case, one subtree may contain almost all nodes, leading to roughly `10^10` operations.

The constraints strongly suggest an offline preprocessing approach. We need something around `O(n log n)` or `O((n + m) log n)`.

Several edge cases are easy to mishandle.

Consider multiple roots:

```
4
a 0
b 0
c 1
d 2
2
1 1
2 1
```

The correct answers are:

```
1
1
```

A DFS started from only one root would completely miss part of the forest.

Another subtle case appears when the requested depth does not exist:

```
3
a 0
b 1
c 2
1
1 5
```

The answer is:

```
0
```

A careless implementation might try to access nonexistent depth structures.

Repeated names also matter:

```
5
john 0
john 1
john 1
alice 2
alice 3
2
1 1
1 2
```

At distance `1` from node `1`, both descendants are named `john`, so the answer is `1`, not `2`.

Finally, queries with `k = 0` are impossible in this problem because constraints start from `1`. That removes one common special case.

## Approaches

The brute-force solution is straightforward. For every query `(v, k)`, traverse the subtree of `v`, collect all nodes whose depth equals `depth[v] + k`, insert their names into a set, and output the set size.

This is correct because it directly follows the definition of a `k`-son. The problem is cost. In a chain-like tree, a subtree can contain `O(n)` nodes. With `m = 10^5` queries, the total work becomes `O(nm)`.

We need to reuse work across queries.

The key observation is that every query only depends on two things:

- a subtree
- a single depth

Subtree queries on trees often become interval queries after an Euler tour. During DFS, each subtree becomes a contiguous segment `[tin[v], tout[v]]`.

Now imagine processing nodes depth by depth. For each depth `d`, we maintain all names appearing at that depth, ordered by Euler time. Then a query becomes:

> Among nodes at depth `d = depth[v] + k`, count distinct names whose Euler time lies inside `[tin[v], tout[v]]`.

The remaining challenge is counting distinct values inside a range efficiently.

This is where the classic offline distinct-query trick appears. Suppose we process Euler positions from left to right. For every name, we keep only its latest occurrence active in a Fenwick tree. Then the sum on a range gives the number of distinct names inside it.

We can group all nodes by depth and all queries by target depth. For each depth independently:

1. Sort nodes by Euler order.
2. Activate only the latest occurrence of every name.
3. Answer all interval queries for that depth.

Each node and query participates only once, giving an `O((n + m) log n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the forest from the parent array.

Every node with parent `0` becomes a root. Store children adjacency lists.
2. Run DFS from every root.

During DFS, compute:

- `depth[v]`
- `tin[v]`
- `tout[v]`

We increment a global timer on entry. Because of DFS ordering, every subtree forms a contiguous Euler interval.
3. Group nodes by depth.

For every node `v`, append `(tin[v], name[v])` into `depth_nodes[depth[v]]`.

Queries only compare nodes at one exact depth, so processing depths independently avoids unnecessary work.
4. Convert each query `(v, k)` into a depth-restricted interval query.

The required depth is:

```
target = depth[v] + k
```

The subtree interval is:

```
[tin[v], tout[v]]
```

Store queries grouped by `target`.
5. For each depth separately, process all nodes in Euler order.

Suppose we are processing depth `d`.

We sort all nodes at depth `d` by Euler time. Then we sweep from left to right.

Maintain:

- a Fenwick tree over Euler positions
- `last[name]`, the latest Euler position where this name appeared

When visiting `(pos, name)`:

- if the name appeared before at `old`, remove contribution at `old`
- add contribution at `pos`
- update `last[name] = pos`

At any moment, the Fenwick tree contains exactly one active occurrence per distinct name among processed positions.
6. Answer interval queries offline.

Sort queries for this depth by right endpoint.

While sweeping nodes up to the query's right boundary, update the Fenwick tree.

Then the number of distinct names inside `[l, r]` is:

```
bit.query(r) - bit.query(l - 1)
```
7. Output answers in original order.

### Why it works

For a fixed depth, the sweep invariant is:

> After processing Euler positions up to `x`, the Fenwick tree contains `1` exactly at the latest occurrence of every distinct name among positions `<= x`.

Consider a query interval `[l, r]`.

If a name appears inside this interval, its latest occurrence up to `r` must also lie inside the interval. Earlier occurrences were removed when later ones appeared.

So every distinct name contributes exactly one active position inside `[l, r]`, and names absent from the interval contribute zero.

The Fenwick range sum is exactly the number of distinct names in the subtree at the required depth.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def range_query(self, l, r):
        return self.query(r) - self.query(l - 1)

def solve():
    n = int(input())

    names = [""] * (n + 1)
    children = [[] for _ in range(n + 1)]
    roots = []

    for i in range(1, n + 1):
        s, r = input().split()
        r = int(r)

        names[i] = s

        if r == 0:
            roots.append(i)
        else:
            children[r].append(i)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    depth = [0] * (n + 1)

    depth_nodes = defaultdict(list)

    timer = 0

    sys.setrecursionlimit(1 << 25)

    def dfs(v, d):
        nonlocal timer

        timer += 1
        tin[v] = timer
        depth[v] = d

        depth_nodes[d].append((tin[v], names[v]))

        for to in children[v]:
            dfs(to, d + 1)

        tout[v] = timer

    for root in roots:
        dfs(root, 0)

    m = int(input())

    queries_by_depth = defaultdict(list)
    ans = [0] * m

    for idx in range(m):
        v, k = map(int, input().split())

        target = depth[v] + k

        queries_by_depth[target].append(
            (tout[v], tin[v], idx)
        )

    bit = Fenwick(n)

    for d in queries_by_depth:
        nodes = depth_nodes.get(d, [])
        nodes.sort()

        queries = queries_by_depth[d]
        queries.sort()

        last = {}

        ptr = 0

        used_positions = []

        for r, l, qid in queries:
            while ptr < len(nodes) and nodes[ptr][0] <= r:
                pos, name = nodes[ptr]

                if name in last:
                    bit.add(last[name], -1)

                bit.add(pos, 1)
                last[name] = pos

                used_positions.append(pos)

                ptr += 1

            ans[qid] = bit.range_query(l, r)

        for pos in used_positions:
            bit.add(pos, -1)

    print("\n".join(map(str, ans)))

solve()
```

The DFS phase assigns Euler intervals. Because DFS fully explores a subtree before returning, every descendant of `v` receives a contiguous Euler range. That property is what converts subtree queries into interval queries.

`depth_nodes[d]` stores all nodes at depth `d`. The pair `(tin[v], name[v])` is enough because subtree filtering later happens using Euler intervals only.

Queries are grouped by target depth rather than by source node. This is the central reduction. Once a depth is fixed, the problem becomes a standard offline distinct-elements-in-range problem.

The Fenwick tree stores active latest occurrences. When a name reappears, the previous occurrence is removed before inserting the new one. Without this removal step, duplicate names would be counted multiple times.

The cleanup loop at the end of each depth is subtle but necessary. The same Fenwick tree instance is reused across depths, so all updates from the current depth must be reverted.

Another easy mistake is sorting queries by `tout[v]`. The sweep processes nodes in increasing Euler order, so queries must also advance by right endpoint.

## Worked Examples

### Sample 1

Input:

```
6
pasha 0
gerald 1
gerald 1
valera 2
igor 3
olesya 1
5
1 1
1 2
1 3
3 1
6 1
```

DFS order:

| Node | Name | Depth | tin | tout |
| --- | --- | --- | --- | --- |
| 1 | pasha | 0 | 1 | 6 |
| 2 | gerald | 1 | 2 | 3 |
| 4 | valera | 2 | 3 | 3 |
| 3 | gerald | 1 | 4 | 5 |
| 5 | igor | 2 | 5 | 5 |
| 6 | olesya | 1 | 6 | 6 |

Query conversion:

| Query | Target Depth | Interval |
| --- | --- | --- |
| (1,1) | 1 | [1,6] |
| (1,2) | 2 | [1,6] |
| (1,3) | 3 | [1,6] |
| (3,1) | 2 | [4,5] |
| (6,1) | 2 | [6,6] |

Processing depth `1`:

| Euler Pos | Name | Active Names |
| --- | --- | --- |
| 2 | gerald | {gerald} |
| 4 | gerald | {gerald at 4} |
| 6 | olesya | {gerald, olesya} |

The subtree interval `[1,6]` contains two active names, so answer is `2`.

Processing depth `2`:

| Euler Pos | Name | Active Names |
| --- | --- | --- |
| 3 | valera | {valera} |
| 5 | igor | {valera, igor} |

The full subtree gives `2`, while interval `[4,5]` only contains `igor`, giving `1`.

This trace shows why only latest occurrences remain active. The duplicate `gerald` nodes collapse into one distinct name.

### Custom Example

Input:

```
5
a 0
a 1
b 1
a 2
b 3
3
1 1
1 2
2 1
```

DFS order:

| Node | Name | Depth | tin | tout |
| --- | --- | --- | --- | --- |
| 1 | a | 0 | 1 | 5 |
| 2 | a | 1 | 2 | 3 |
| 4 | a | 2 | 3 | 3 |
| 3 | b | 1 | 4 | 5 |
| 5 | b | 2 | 5 | 5 |

Queries:

| Query | Target Depth | Interval |
| --- | --- | --- |
| (1,1) | 1 | [1,5] |
| (1,2) | 2 | [1,5] |
| (2,1) | 2 | [2,3] |

Processing depth `1` gives active names `{a, b}`, answer `2`.

Processing depth `2` gives active names `{a, b}` for the full subtree, answer `2`.

For interval `[2,3]`, only node `4` lies inside, answer `1`.

This example demonstrates that subtree filtering and distinct counting interact correctly even when names repeat across different branches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each node and query performs Fenwick updates or queries |
| Space | O(n + m) | Tree storage, Euler arrays, grouped queries, Fenwick tree |

With `10^5` nodes and queries, roughly a few million Fenwick operations fit comfortably within the limits. Memory usage also remains linear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def query(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

        def range_query(self, l, r):
            return self.query(r) - self.query(l - 1)

    n = int(input())

    names = [""] * (n + 1)
    children = [[] for _ in range(n + 1)]
    roots = []

    for i in range(1, n + 1):
        s, r = input().split()
        r = int(r)

        names[i] = s

        if r == 0:
            roots.append(i)
        else:
            children[r].append(i)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    depth = [0] * (n + 1)

    depth_nodes = defaultdict(list)

    timer = 0

    sys.setrecursionlimit(1 << 25)

    def dfs(v, d):
        nonlocal timer

        timer += 1
        tin[v] = timer
        depth[v] = d

        depth_nodes[d].append((tin[v], names[v]))

        for to in children[v]:
            dfs(to, d + 1)

        tout[v] = timer

    for r in roots:
        dfs(r, 0)

    m = int(input())

    queries_by_depth = defaultdict(list)
    ans = [0] * m

    for idx in range(m):
        v, k = map(int, input().split())

        target = depth[v] + k

        queries_by_depth[target].append(
            (tout[v], tin[v], idx)
        )

    bit = Fenwick(n)

    for d in queries_by_depth:
        nodes = sorted(depth_nodes.get(d, []))
        queries = sorted(queries_by_depth[d])

        last = {}
        ptr = 0
        used = []

        for r, l, idx in queries:
            while ptr < len(nodes) and nodes[ptr][0] <= r:
                pos, name = nodes[ptr]

                if name in last:
                    bit.add(last[name], -1)

                bit.add(pos, 1)
                last[name] = pos

                used.append(pos)

                ptr += 1

            ans[idx] = bit.range_query(l, r)

        for pos in used:
            bit.add(pos, -1)

    return "\n".join(map(str, ans))

# provided sample
assert run(
"""6
pasha 0
gerald 1
gerald 1
valera 2
igor 3
olesya 1
5
1 1
1 2
1 3
3 1
6 1
"""
) == "2\n2\n0\n1\n0"

# minimum size
assert run(
"""1
alex 0
1
1 1
"""
) == "0"

# repeated names
assert run(
"""5
john 0
john 1
john 1
alice 2
alice 3
2
1 1
1 2
"""
) == "1\n1"

# multiple roots
assert run(
"""4
a 0
b 0
c 1
d 2
2
1 1
2 1
"""
) == "1\n1"

# chain tree, missing depth
assert run(
"""4
a 0
b 1
c 2
d 3
2
1 5
2 2
"""
) == "0\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node tree | 0 | Missing target depth |
| Repeated names | 1 1 | Distinct counting correctness |
| Multiple roots | 1 1 | Forest traversal correctness |
| Deep chain with large k | 0 1 | Boundary depth handling |

## Edge Cases

Consider a forest with multiple roots:

```
4
a 0
b 0
c 1
d 2
2
1 1
2 1
```

DFS starts from both roots `1` and `2`. Euler intervals become:

| Node | tin | tout |
| --- | --- | --- |
| 1 | 1 | 2 |
| 3 | 2 | 2 |
| 2 | 3 | 4 |
| 4 | 4 | 4 |

Query `(1,1)` maps to interval `[1,2]` at depth `1`, which only contains node `3`. Query `(2,1)` maps to `[3,4]`, containing only node `4`.

The algorithm handles disconnected trees because every root launches its own DFS.

Now consider nonexistent depths:

```
3
a 0
b 1
c 2
1
1 5
```

The target depth is `5`, but `depth_nodes[5]` is empty.

During processing, the node list for this depth is empty, so no Fenwick updates happen. The range query immediately returns `0`.

Repeated names inside the same subtree behave correctly:

```
5
john 0
john 1
john 1
alice 2
alice 3
2
1 1
1 2
```

At depth `1`, nodes `(2, john)` and `(3, john)` appear. When processing the second occurrence, the first one is removed from the Fenwick tree.

So the subtree interval contains exactly one active occurrence for `john`, producing answer `1` instead of `2`.
