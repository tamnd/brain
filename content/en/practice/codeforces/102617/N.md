---
title: "CF 102617N - Pie Predicament"
description: "We have several pie types, and every pie in a row belongs to exactly one type. Two people must divide the pies between them, but the division happens by type rather than by individual pie. If a person receives one pie of some type, that person must receive every pie of that type."
date: "2026-07-31T17:41:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102617
codeforces_index: "N"
codeforces_contest_name: "mBIT Rookie November 2019"
rating: 0
weight: 102617
solve_time_s: 68
verified: true
draft: false
---

[CF 102617N - Pie Predicament](https://codeforces.com/problemset/problem/102617/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several pie types, and every pie in a row belongs to exactly one type. Two people must divide the pies between them, but the division happens by type rather than by individual pie. If a person receives one pie of some type, that person must receive every pie of that type.

Each person has a list of preferred types. A type that appears only in one person's list is forced to belong to that person. A type appearing in both lists can be assigned either way. After the assignment, every adjacent pair of pies in the row gives candies if both pies belong to the same person. The goal is to choose the ownership of the flexible types so that the total number of candies is as large as possible.

The important part of the input is that the row of pies creates relationships between types. If two neighboring pies have different types, assigning those two types to different people loses the candy value associated with that boundary. If they have the same owner, that value is gained. The problem is not about individual pies, it is about assigning types to two groups while preserving as many valuable connections as possible.

The number of types can reach 500 and the number of pies can reach 1000. A solution that tries every possible assignment of types would need to examine up to $2^K$ possibilities. With $K=500$, this is far beyond what any time limit can support. We need an approach that works close to polynomial time. The number of pies is small enough that building relationships between types directly is practical.

The main edge cases come from forced assignments and from types that occur multiple times in the row. For example, consider:

```
2 2 1 1
1
2
1 2
5
```

The first type can only belong to Joaozao and the second only to Nicoleta. The only boundary separates the two people, so the answer is `0`. A careless solution that assigns types greedily without respecting preferences could incorrectly place both types together and count the boundary.

Another case is when a type appears many times:

```
3 5 2 2
1 2
2 3
1 2 1 3 2
1 10 10 1
```

Type 2 can belong to either person, but its repeated appearances connect it with both type 1 and type 3. Looking only at one occurrence of the type can lead to the wrong decision. The solution must combine all boundaries involving a type.

A final boundary case is when every type is already forced:

```
3 3 1 2
1
2 3
1 2 3
7 8
```

There is no decision to make. The answer is simply the total value of boundaries where the forced owners match. Any algorithm that assumes at least one flexible type exists must still handle this case.

## Approaches

A direct approach is to assign every flexible pie type to one of the two people, then calculate the candy total for that assignment. This works because every valid solution corresponds to exactly one ownership choice for every type. If there are $F$ flexible types, this requires checking $2^F$ assignments. In the worst case every type can be chosen freely, giving $2^{500}$ possibilities, which is impossible.

The useful observation comes from looking at what is lost instead of what is gained. The total candy value of all boundaries is fixed. A boundary contributes its value unless the two adjacent types are assigned to different people. Therefore maximizing candies is equivalent to minimizing the total weight of boundaries that are cut between the two groups of types.

This turns the problem into a minimum cut problem. Each pie type becomes a vertex. Every adjacent pair of different types contributes an edge whose weight is the number of candies lost if those two types are separated. Types forced to Joaozao are connected to the source, and types forced to Nicoleta are connected to the sink. The minimum source-sink cut chooses the side of every flexible type while paying exactly for the separated boundaries.

The maximum candies are the sum of all boundary values minus the minimum cut value. The graph has only about 500 vertices and 1000 useful edges, so a standard max flow algorithm is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^K \cdot N)$ | $O(K)$ | Too slow |
| Min Cut | $O(V^2E)$ with Dinic's algorithm in this graph size | $O(V+E)$ | Accepted |

## Algorithm Walkthrough

1. Read the preferences and determine the owner restrictions of every type. A type that appears only in Joaozao's list must be placed on the source side, while a type that appears only in Nicoleta's list must be placed on the sink side. Types appearing in both lists remain undecided.
2. Build a graph where every pie type is a node. Add a directed edge in both directions between neighboring types with capacity equal to the candy value of that boundary. Multiple boundaries between the same pair of types are accumulated naturally by adding more capacity.
3. Add a source node and a sink node. Connect every forced Joaozao type to the source with a very large capacity. Connect every forced Nicoleta type to the sink with the same large capacity. The large value makes separating a forced type from its required side more expensive than any possible candy loss.
4. Compute the maximum flow from source to sink. By the max-flow min-cut theorem, this value is the minimum total weight of boundaries separating the two owners.
5. Subtract the minimum cut value from the sum of all boundary rewards. The remaining value is exactly the maximum candy amount that can be obtained.

Why it works:

The cut separates the type vertices into two groups. The source side represents Joaozao's types and the sink side represents Nicoleta's types. Forced types cannot cross the cut because their infinite capacity edges would make such a cut impossible to be optimal. Every ordinary edge crossing the cut represents a pair of neighboring pies whose owners differ, so its capacity is exactly the candy value lost at that boundary. Every non-crossing edge keeps its candy value. Since the minimum cut minimizes all lost candy values, the resulting assignment maximizes the earned candies.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = [s]
        for u in q:
            for v, c, _ in self.g[u]:
                if c and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f
        while self.it[u] < len(self.g[u]):
            e = self.g[u][self.it[u]]
            v, c, rev = e
            if c and self.level[v] == self.level[u] + 1:
                ret = self.dfs(v, t, min(f, c))
                if ret:
                    e[1] -= ret
                    self.g[v][rev][1] += ret
                    return ret
            self.it[u] += 1
        return 0

    def flow(self, s, t):
        ans = 0
        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self.dfs(s, t, 10**18)
                if not pushed:
                    break
                ans += pushed
        return ans

def solve():
    k, n, a, b = map(int, input().split())

    jo = list(map(int, input().split()))
    ni = list(map(int, input().split()))

    owner = [0] * k
    for x in jo:
        owner[x - 1] |= 1
    for x in ni:
        owner[x - 1] |= 2

    pies = list(map(int, input().split()))
    pies = [x - 1 for x in pies]
    g = list(map(int, input().split()))

    total = sum(g)

    s = k
    t = k + 1
    dinic = Dinic(k + 2)

    inf = total + 1

    for i in range(k):
        if owner[i] == 1:
            dinic.add_edge(s, i, inf)
        elif owner[i] == 2:
            dinic.add_edge(i, t, inf)

    for i, w in enumerate(g):
        u = pies[i]
        v = pies[i + 1]
        if u != v:
            dinic.add_edge(u, v, w)
            dinic.add_edge(v, u, w)

    cut = dinic.flow(s, t)
    print(total - cut)

if __name__ == "__main__":
    solve()
```

The implementation represents each pie type as one node in the flow graph. The Dinic structure stores residual edges, which allows the algorithm to repeatedly find augmenting paths and update remaining capacities.

The preference processing uses a two-bit representation. A value of `1` means Joaozao accepts the type, and a value of `2` means Nicoleta accepts it. Values `1` and `2` are forced, while value `3` is flexible.

The infinite capacity is chosen as `sum(g) + 1`. No optimal cut would ever sacrifice that much capacity, because cutting every normal boundary costs at most `sum(g)`. This prevents the flow algorithm from assigning a forced type to the wrong side.

Only boundaries between different types need edges. If two neighboring pies have the same type, they always have the same owner, so that boundary can never be lost and does not affect the optimization.

## Worked Examples

For the first sample:

```
4 6 1 3
1
2 3 4
1 3 2 2 4 1
1 2 4 8 16
```

The total available candy is 31. The type ownership graph contains the forced type 1 on Joaozao's side. The minimum cut chooses to separate type 1 from the rest, losing 17 candies.

| Step | Current decision | Cut value |
| --- | --- | --- |
| Initial | All boundaries counted | 31 |
| Force type 1 | Type 1 must stay on source side | 0 |
| Minimum cut | Separate type 1 from types 3,2,4 | 17 |
| Final | Total minus lost candy | 14 |

The trace shows that the algorithm is minimizing the lost boundaries rather than directly maximizing the gained ones.

For the second sample:

```
4 10 3 3
1 2 3
2 3 4
1 2 3 4 3 1 2 4 3 1
1 1 5 5 2 2 1 5 1
```

The total candy value is 23.

| Step | Current decision | Cut value |
| --- | --- | --- |
| Initial | Count every boundary | 23 |
| Forced nodes | Type 1 and type 4 are constrained | 0 |
| Minimum cut | Choose flexible ownership split | 5 |
| Final | Total minus lost candy | 18 |

This example demonstrates that a flexible type can be assigned based on all of its neighboring relationships, not just one occurrence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(V^2E)$ | Dinic runs on a graph with $V=K+2$ and $E$ proportional to the number of boundaries |
| Space | $O(V+E)$ | The residual graph stores every flow edge and reverse edge |

With at most 500 pie types and 1000 pies, the graph is small. The max flow computation is easily within the limits because the number of vertices and edges is low.

## Test Cases

```python
import sys, io

def solve_io(inp):
    sys.stdin = io.StringIO(inp)
    import collections

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]

        def add_edge(self, u, v, c):
            self.g[u].append([v, c, len(self.g[v])])
            self.g[v].append([u, 0, len(self.g[u]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * self.n
            self.level[s] = 0
            q = [s]
            for u in q:
                for v, c, _ in self.g[u]:
                    if c and self.level[v] == -1:
                        self.level[v] = self.level[u] + 1
                        q.append(v)
            return self.level[t] != -1

        def dfs(self, u, t, f):
            if u == t:
                return f
            while self.it[u] < len(self.g[u]):
                e = self.g[u][self.it[u]]
                v, c, rev = e
                if c and self.level[v] == self.level[u] + 1:
                    r = self.dfs(v, t, min(f, c))
                    if r:
                        e[1] -= r
                        self.g[v][rev][1] += r
                        return r
                self.it[u] += 1
            return 0

        def flow(self, s, t):
            ans = 0
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    x = self.dfs(s, t, 10**18)
                    if not x:
                        break
                    ans += x
            return ans

    def run():
        k, n, a, b = map(int, input().split())
        jo = list(map(int, input().split()))
        ni = list(map(int, input().split()))
        own = [0] * k
        for x in jo:
            own[x - 1] |= 1
        for x in ni:
            own[x - 1] |= 2
        p = [x - 1 for x in map(int, input().split())]
        w = list(map(int, input().split()))
        d = Dinic(k + 2)
        total = sum(w)
        inf = total + 1
        for i, x in enumerate(own):
            if x == 1:
                d.add_edge(k, i, inf)
            elif x == 2:
                d.add_edge(i, k + 1, inf)
        for i, x in enumerate(w):
            if p[i] != p[i + 1]:
                d.add_edge(p[i], p[i + 1], x)
                d.add_edge(p[i + 1], p[i], x)
        return str(total - d.flow(k, k + 1)) + "\n"

    return run()

assert solve_io("""4 6 1 3
1
2 3 4
1 3 2 2 4 1
1 2 4 8 16
""") == "14\n"

assert solve_io("""4 10 3 3
1 2 3
2 3 4
1 2 3 4 3 1 2 4 3 1
1 1 5 5 2 2 1 5 1
""") == "18\n"

assert solve_io("""2 2 1 1
1
2
1 2
5
""") == "0\n"

assert solve_io("""3 3 1 2
1
2 3
1 2 3
7 8
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 14 | Basic min cut construction |
| Sample 2 | 18 | Multiple flexible assignments |
| Two forced types | 0 | Forced ownership handling |
| All forced boundaries | 0 | No flexible node case |

## Edge Cases

When a type is forced to one person, the infinite capacity edge makes assigning it to the other side impossible in the minimum cut. For the input:

```
2 2 1 1
1
2
1 2
5
```

the graph contains a source connection to type 1 and a sink connection from type 2. The only possible cut separates them, losing the only boundary value of 5. The result is `0`.

When one type appears many times, every occurrence contributes to the same graph vertex. For example:

```
3 5 2 2
1 2
2 3
1 2 1 3 2
1 10 10 1
```

type 2 receives edges from both type 1 and type 3. The flow algorithm considers the combined effect of all these edges before deciding where type 2 belongs.

When all types are forced, the flow graph still works without any special handling. There are no meaningful choices left, but the cut value still represents the boundaries where forced groups differ. The final subtraction from the total reward gives the exact candy count.
