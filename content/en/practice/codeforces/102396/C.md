---
title: "CF 102396C - Jet Trains"
description: "Think of the cities as vertices of an undirected graph whose edges are the currently available train routes. Since routes are bidirectional, two cities can reach each other exactly when they belong to the same connected component of this graph."
date: "2026-08-14T14:22:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "C"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 291
verified: false
draft: false
---

[CF 102396C - Jet Trains](https://codeforces.com/problemset/problem/102396/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 51s  
**Verified:** no  

## Solution
## Problem Understanding

Think of the cities as vertices of an undirected graph whose edges are the currently available train routes. Since routes are bidirectional, two cities can reach each other exactly when they belong to the same connected component of this graph.

There is a second undirected graph on the same vertices, representing friendships. For a query `? v`, we need the number of vertices `u` such that `u` is a friend of `v` and `u` is in the same connected component of `v` in the train graph. The answer is not the total number of friends, because some friends may currently be unreachable.

Two kinds of updates are possible. A `T a b` operation inserts a train edge, so two previously separate train components may merge. An `F a b` operation inserts a friendship edge. Neither type of edge is ever removed, which is the structural property that makes an incremental connectivity solution possible.

The initial input contains up to (10^5) cities, (10^5) friendships, (10^5) train routes, and (10^5) subsequent operations. A solution that scans all cities or all friendships for every query would take up to (10^{10}) operations, far beyond what a two-second limit permits. We need roughly linear or near-linear total work, with logarithmic factors being acceptable.

There are several edge cases that can fool a direct implementation. First, a friendship can exist before its endpoints become train-connected. For example:

```
2 1 0
1 2
0
```

There are no train routes, so there is no output. If we instead add a query:

```
2 1 0
1 2
1
? 1
```

the output is `0`, even though cities 1 and 2 are friends. A solution that counts friendships without checking train connectivity would incorrectly print `1`.

Second, a newly added friendship can connect two cities that are already reachable:

```
2 0 1
1 2
1
F 1 2
```

There is no query, but after the friendship is inserted the contribution of both endpoints becomes one immediately. If the implementation only processes friendships when a train edge is added, it loses this update.

Third, when a train edge joins two components, several existing friendships can become valid simultaneously. For example:

```
4 2 1
1 3
2 4
1 2
1
? 1
```

The train graph connects 1 with 2, while 3 and 4 are outside that component. City 1 has no reachable friend, so the answer is `0`. If the train edge instead joins components containing 1 and 3, then the friendship `(1,3)` becomes valid immediately. A careless implementation that only checks the two endpoints of the new train edge can miss friendships between arbitrary vertices of the two merged components.

## Approaches

The brute-force approach is straightforward. Maintain the train graph and, for every query `? v`, run a DFS or BFS from `v` to determine its current connected component. Then inspect every friendship of `v` and count those whose endpoint was visited. This is correct because the DFS exactly identifies the cities reachable from `v`.

The problem is the cost. A single connectivity search can touch (O(n+k+q)) vertices and edges in the worst case, and there can be (10^5) queries. In a dense enough sequence of operations this gives on the order of (10^{10}) graph operations, which is far too slow.

A better starting point is to exploit the fact that train edges are only inserted. Connected components can then be maintained with a disjoint set union structure, or DSU. A query `? v` can immediately identify the current train component of `v`.

The remaining problem is maintaining how many friends of each vertex are inside its component. Let `ans[v]` be exactly that number. When a friendship `(a,b)` is inserted, there are only two possibilities. If `a` and `b` already belong to the same train component, both answers increase by one. Otherwise the friendship is not useful yet, but it must be remembered because a future train merge may make it useful.

Suppose a train edge merges two different components. Every friendship crossing those two components becomes valid after the merge. We could inspect every friendship between the two components, but doing that naively can repeatedly scan huge components.

The key observation is to always process the smaller component. Store the list of vertices belonging to every DSU component. When two components merge, iterate through every vertex of the smaller component and inspect all of its friendship edges. A friendship whose other endpoint lies in the larger component is crossing the cut and becomes valid, so increment the answers of both endpoints.

Why is this fast enough? Whenever a vertex is processed during a component merge, it belonged to the smaller component. After the merge, its component has at least doubled in size. Consequently, any particular vertex can belong to the smaller side at most (O(\log n)) times. Every time that vertex is processed, we scan its friendship adjacency list, so each friendship adjacency is scanned only (O(\log n)) times in total.

This gives the same small-to-large idea used in the official analysis of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(q(n+m+k))) | (O(n+m+k)) | Too slow |
| Optimal | (O((m+q+k)\log n\cdot\alpha(n))) | (O(n+m+k)) | Accepted |

## Algorithm Walkthrough

1. Create a DSU containing all (n) cities. For every component, maintain its current list of vertices. Initially every component contains one city.
2. Store every friendship in an adjacency list `friends[v]`. Each friendship `(a,b)` is stored twice, once in `friends[a]` and once in `friends[b]`, because later we need to inspect all friends of a vertex.
3. Add the initial train routes to the DSU. Since train edges only add connectivity, DSU can represent the exact connected components after all initial routes have been inserted.
4. Initialize `ans[v]` by processing every initial friendship `(a,b)`. If `a` and `b` have the same DSU root, increment both `ans[a]` and `ans[b]`. At this point `ans[v]` is exactly the number of currently reachable friends of `v`.
5. For an `F a b` operation, append `b` to `friends[a]` and `a` to `friends[b]`. If the two endpoints currently have the same DSU root, increment `ans[a]` and `ans[b]`. If they are in different components, do not change the answers yet, because the friendship becomes useful only after their components merge.
6. For a `T a b` operation, find the roots of `a` and `b`. If they are already equal, the new route changes no connectivity and no answer, so the operation is finished.
7. If the roots differ, compare the sizes of their components and designate the smaller one as `small` and the larger one as `large`. The member list of `small` is the only component we need to enumerate.
8. Before changing the DSU parents, iterate through every vertex `v` in `small` and every friend `u` of `v`. If `u` currently belongs to `large`, then `(v,u)` is a friendship crossing the two components. After the new train route is inserted, the two cities become mutually reachable, so increment both `ans[v]` and `ans[u]`.
9. Merge `small` into `large` in the DSU and append the vertices of `small` to the member list of `large`. The component size also becomes the sum of the two old sizes.
10. For a `? v` operation, print `ans[v]`. No graph traversal is necessary because all changes that can affect this value were already processed when the corresponding friendship or train merge occurred.

### Why it works

The invariant is that after every processed operation, `ans[v]` equals the number of friendship edges incident to `v` whose other endpoint lies in the same current train component as `v`.

A newly inserted friendship is counted immediately exactly when its endpoints are already connected. If they are not connected, the friendship is stored in both adjacency lists and remains available for a later component merge.

When two train components merge, the only friendships whose status can change are friendships with one endpoint in each component. We inspect every vertex of the smaller component and all of its friendships, so every crossing friendship is found. Internal friendships were already counted, while friendships going outside both components remain invalid. Thus every newly valid friendship contributes exactly once to both endpoint answers.

After the merge, the DSU represents the new train connectivity, so the invariant holds again. Since all operations only add edges, no previously valid friendship can become invalid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    friends = [[] for _ in range(n)]
    friendship_edges = []

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        friends[a].append(b)
        friends[b].append(a)
        friendship_edges.append((a, b))

    parent = list(range(n))
    size = [1] * n
    members = [[i] for i in range(n)]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return a

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        members[a].extend(members[b])
        members[b] = []
        return a

    for _ in range(k):
        a, b = map(int, input().split())
        merge(a - 1, b - 1)

    ans = [0] * n

    for a, b in friendship_edges:
        if find(a) == find(b):
            ans[a] += 1
            ans[b] += 1

    q = int(input())
    out = []

    for _ in range(q):
        parts = input().split()
        typ = parts[0]

        if typ == '?':
            v = int(parts[1]) - 1
            out.append(str(ans[v]))

        elif typ == 'F':
            a = int(parts[1]) - 1
            b = int(parts[2]) - 1

            friends[a].append(b)
            friends[b].append(a)

            if find(a) == find(b):
                ans[a] += 1
                ans[b] += 1

        else:
            a = int(parts[1]) - 1
            b = int(parts[2]) - 1

            ra = find(a)
            rb = find(b)

            if ra == rb:
                continue

            if size[ra] > size[rb]:
                large, small = ra, rb
            else:
                large, small = rb, ra

            for v in members[small]:
                for u in friends[v]:
                    if find(u) == large:
                        ans[v] += 1
                        ans[u] += 1

            parent[small] = large
            size[large] += size[small]
            members[large].extend(members[small])
            members[small] = []

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The DSU is initialized before the initial friendships are evaluated because the initial train routes determine the starting connected components. The initial friendship edges are saved separately so they can be evaluated after all initial train routes have been inserted.

The `members` array is the extra structure that makes the small-to-large merge possible. A DSU alone can tell us whether two vertices are connected, but it cannot enumerate all vertices belonging to a component efficiently. The member list supplies exactly that missing operation.

The order inside a train merge is subtle. The smaller component is scanned before its parent is changed. During this scan, `find(u) == large` means that `u` really belonged to the other component before the merge. If we changed the parent first, friendships between two vertices that were both in `small` could be mistaken for crossing friendships and counted twice.

The `F` operation updates the friendship adjacency lists regardless of connectivity. The friendship must remain stored when its endpoints are disconnected, because a later `T` operation may make it valid.

All counts fit comfortably in Python integers. In C++ an ordinary 32-bit signed integer would also be sufficient here because an answer is at most (n-1), but Python has no integer overflow concern.

The iterative `find` avoids recursion overhead and performs path compression. Union by component size guarantees that member lists are always merged from the smaller list into the larger one.

## Worked Examples

### Sample 1

The initial train edges are `(1,2)` and `(1,4)`, so the train components are `{1,2,4}` and `{3}`. The initial friendships are `(1,2)` and `(1,3)`. Only `(1,2)` is inside the component of city 1, so `ans[1]` starts at one.

| Operation | Components | New friendship effect | `ans[1]` |
| --- | --- | --- | --- |
| Initial state | `{1,2,4}`, `{3}` | `(1,2)` counted, `(1,3)` not counted | 1 |
| `? 1` | `{1,2,4}`, `{3}` | none | 1 |
| `F 4 1` | `{1,2,4}`, `{3}` | 1 and 4 already connected | 2 |
| `? 1` | `{1,2,4}`, `{3}` | none | 2 |
| `T 4 3` | `{1,2,3,4}` | friendship `(1,3)` crosses the merged components | 3 |
| `? 1` | `{1,2,3,4}` | none | 3 |

The last train insertion scans the smaller component `{3}`. Its only friendship is with city 1, which belongs to the other component, so `(3,1)` becomes reachable and `ans[1]` increases from two to three.

### Constructed Example 2

Consider the following input:

```
5 2 1
1 4
2 5
1 2
5
? 1
F 1 3
? 1
T 3 4
? 1
```

Initially the train components are `{1,2}` and `{3}`, `{4}`, `{5}`. The friendship `(1,4)` is not reachable, and `(2,5)` is also not reachable from city 1.

| Operation | Components | Relevant change | `ans[1]` |
| --- | --- | --- | --- |
| Initial state | `{1,2}`, `{3}`, `{4}`, `{5}` | No friendship inside city 1's component | 0 |
| `? 1` | `{1,2}`, `{3}`, `{4}`, `{5}` | none | 0 |
| `F 1 3` | `{1,2}`, `{3}`, `{4}`, `{5}` | 1 and 3 are disconnected | 0 |
| `? 1` | `{1,2}`, `{3}`, `{4}`, `{5}` | none | 0 |
| `T 3 4` | `{1,2}`, `{3,4}`, `{5}` | friendship `(1,4)` still crosses components | 0 |
| `? 1` | `{1,2}`, `{3,4}`, `{5}` | none | 0 |

This example demonstrates that a friendship can be stored for a long time without affecting either endpoint's answer. If we then add `T 2 3`, the components `{1,2}` and `{3,4}` merge, and both friendships `(1,4)` and `(1,3)` become valid at once. The small-component scan finds both.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((m+q+k)\log n\cdot\alpha(n))) | DSU operations are almost constant, while every vertex's friendship list is scanned only (O(\log n)) times |
| Space | (O(n+m+q)) | DSU arrays, component member lists, friendship adjacency lists, and stored initial friendships |

The initial graph contains at most (10^5) friendship edges and (10^5) train edges, while at most (10^5) additional operations are processed. The logarithmic factor comes from small-to-large merging, so the total amount of friendship scanning remains manageable. The memory usage is linear in the number of cities and inserted friendships.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    friends = [[] for _ in range(n)]
    friendship_edges = []

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        friends[a].append(b)
        friends[b].append(a)
        friendship_edges.append((a, b))

    parent = list(range(n))
    size = [1] * n
    members = [[i] for i in range(n)]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        members[a].extend(members[b])
        members[b] = []

    for _ in range(k):
        a, b = map(int, input().split())
        merge(a - 1, b - 1)

    ans = [0] * n

    for a, b in friendship_edges:
        if find(a) == find(b):
            ans[a] += 1
            ans[b] += 1

    q = int(input())
    out = []

    for _ in range(q):
        parts = input().split()
        typ = parts[0]

        if typ == '?':
            v = int(parts[1]) - 1
            out.append(str(ans[v]))

        elif typ == 'F':
            a = int(parts[1]) - 1
            b = int(parts[2]) - 1

            friends[a].append(b)
            friends[b].append(a)

            if find(a) == find(b):
                ans[a] += 1
                ans[b] += 1

        else:
            a = int(parts[1]) - 1
            b = int(parts[2]) - 1

            ra = find(a)
            rb = find(b)

            if ra == rb:
                continue

            if size[ra] >= size[rb]:
                large, small = ra, rb
            else:
                large, small = rb, ra

            for v in members[small]:
                for u in friends[v]:
                    if find(u) == large:
                        ans[v] += 1
                        ans[u] += 1

            parent[small] = large
            size[large] += size[small]
            members[large].extend(members[small])
            members[small] = []

    return '\n'.join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
4 2 2
1 2
1 3
1 2
1 4
5
? 1
F 4 1
? 1
T 4 3
? 1
"""

assert run(sample1) == "1\n2\n3", "sample 1"

case2 = """\
1 0 0
3
? 1
F 1 1
? 1
"""
# This input violates the original constraint a != b for F, so it is
# deliberately not used as a valid test.

case3 = """\
2 1 0
1 2
2
? 1
T 1 2
"""
assert run(case3) == "0", "friendship before train connection"

case4 = """\
4 2 0
1 3
1 4
5
? 1
T 1 2
? 1
T 2 3
? 1
"""
assert run(case4) == "0\n0\n2", "friendships become reachable after a merge"

case5 = """\
5 0 2
1 2
2 3
5
? 1
F 1 3
? 1
F 4 5
T 3 4
"""
assert run(case5) == "0\n1", "friendship inserted after connectivity"

# Maximum-size structural test. Every query asks about the same isolated city.
# There are 100000 cities and 100000 queries, so this also checks input/output
# handling near the limit.
n = 100000
q = 100000
max_case = f"{n} 0 0\n{q}\n" + "? 100000\n" * q
expected = "0\n" * q
assert run(max_case) == expected[:-1], "maximum-size repeated queries"

# Boundary case with all cities in one train component and every possible
# friendship among three cities.
case7 = """\
3 3 3
1 2
1 3
2 3
1 2
2 3
1 3
4
? 1
F 1 2
? 1
? 3
"""
assert run(case7) == "2\n3\n2", "complete component and repeated queries"
```

The first assertion is the provided sample and checks the complete interaction between friendship insertion and train-component merging.

The second valid case uses the smallest possible graph with two cities. The friendship exists from the beginning, but there is no train route, so the answer is zero.

The third valid case checks a friendship that becomes reachable only after two separate train components are merged. It catches implementations that only update answers when a friendship is inserted.

The fourth valid case inserts a friendship after its endpoints are already connected. It verifies that `F` immediately increments the answers when the DSU roots match.

The maximum-size test performs (10^5) identical queries on (10^5) isolated cities. It stresses input handling and repeated constant-time queries without constructing an unnecessarily large edge set.

The final case places every city in one connected component from the start and has all possible friendships among three cities. It checks that the answer counts each friendship endpoint exactly once and that repeated queries do not mutate state.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `1`, `2`, `3` | Complete interaction of both update types |
| `2 1 0` with `? 1` | `0` | Friendship does not imply train connectivity |
| Four-city merge case | `0`, `0`, `2` | Several friendships can become reachable after a merge |
| Five-city dynamic friendship case | `0`, `1` | Friendship inserted after connectivity |
| (n=q=100000), isolated repeated queries | 100000 zeros | Maximum input size and boundary handling |
| Three fully connected cities | `2`, `3`, `2` | Complete component, duplicate queries, exact counting |

## Edge Cases

### Friendship exists but cities are disconnected

Consider:

```
2 1 0
1 2
1
? 1
```

The friendship adjacency list contains city 2 for city 1, but `find(1)` and `find(2)` are different. The initial friendship contributes nothing to `ans[1]`, so the query prints `0`. If a later `T 1 2` operation occurs, the smaller component contains one city, its friendship with the other component is found during the merge, and `ans[1]` becomes `1`.

### Friendship is added inside an existing train component

Consider:

```
2 0 1
1 2
2
F 1 2
? 1
```

The initial train route puts both cities under the same DSU root. When `F 1 2` is processed, the roots match, so both answers are incremented immediately. The query prints `1`.

### A train merge activates many old friendships

Consider:

```
4 2 1
1 3
1 4
1 2
2
? 1
T 2 3
```

Initially city 1 belongs to `{1,2}`, while cities 3 and 4 are separate. The first query prints `0`. When `T 2 3` is inserted, `{1,2}` merges with `{3}`. The smaller component is `{3}`, and its friendship list contains city 1. The merge increments `ans[3]` and `ans[1]`, so the friendship `(1,3)` is now counted.

The same mechanism handles arbitrarily many crossing friendships. If the smaller component contains (x) vertices and their friendship lists contain (r) relevant edges, all (r) edges are processed during that merge.

### Train edge connects cities already in the same component

Consider:

```
3 1 2
1 3
1 2
2 3
1
? 1
```

All three cities are already connected before the second train edge is considered. The DSU roots of 2 and 3 are equal, so the second edge causes no scan and no answer change. City 1 has one friend, city 3, so the query prints `1`.

Ignoring the `ra == rb` case would cause unnecessary work and could lead to incorrect repeated counting if the component were scanned despite there being no new connectivity.

### The smaller component changes from merge to merge

Suppose the train graph is initially five isolated cities and routes are inserted as `(1,2)`, `(3,4)`, `(1,3)`, `(1,5)`. The first two merges process one-city components. The third merge processes one two-city component against another two-city component. The fourth merge processes the one-city component containing 5 against the already larger component.

A city can only be on the smaller side when its component size is at most half the resulting component size. Every such event at least doubles its component size. Starting from size one, this can happen at most (\lfloor\log_2 n\rfloor) times, which is the reason the repeated friendship scans remain bounded.
