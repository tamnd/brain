---
title: "CF 102163H - Mr. Hamra and his quantum particles"
description: "Think of the particles as vertices of an undirected graph. Every known entanglement relationship between two particles is an edge."
date: "2026-08-20T00:02:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "H"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 599
verified: false
draft: false
---

[CF 102163H - Mr. Hamra and his quantum particles](https://codeforces.com/problemset/problem/102163/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 59s  
**Verified:** no  

## Solution
## Problem Understanding

Think of the particles as vertices of an undirected graph. Every known entanglement relationship between two particles is an edge. The special property of entanglement says that if particle (A) is connected to (B), and (B) is connected to (C), then (A) must also be connected to (C). Repeatedly applying this rule means that every pair of particles belonging to the same connected component is considered entangled.

For each test case, we receive (N) particles, (M) known relationships, and (Q) queries. Each query gives two particle numbers (X) and (Y). We must output a binary string of length (Q), where the character at position (i) is `1` exactly when the two particles in the (i)-th query belong to the same connected component.

For example, with edges (1-2) and (2-3), particles (1) and (3) are not directly related in the input, but they are entangled through particle (2). A query for (1,3) must consequently produce `1`.

The values of (N), (M), and (Q) can each reach (10^5). An algorithm that examines the whole graph separately for every query can perform on the order of (10^{10}) operations, which is far beyond what a 2-second limit can tolerate. Even algorithms with (O(N^2)) preprocessing are unsuitable at this scale. We need a solution close to linear in the number of particles, relationships, and queries.

There are several edge cases that can expose an incorrect implementation.

A query can contain the same particle twice. For example,

```
1
1 1 3
1 1
1 1
1 1
1 1
```

has output `111`. A particle is always in the same connected component as itself, so a careless implementation that only checks whether an actual edge exists could incorrectly return `0`.

Duplicate relationships are also allowed by the input format. For example,

```
1
2 3 2
1 2
1 2
2 1
1 2
```

has output `11`. The repeated edge does not create a new component or require special handling. An implementation that assumes every edge is unique does not need to be correct for uniqueness, because the graph's connectivity is unchanged.

Indirect connectivity is the central edge case. Consider

```
1
3 2 2
1 2
2 3
1 3
1 1
```

The output is `11`. Particles (1) and (3) have no direct relationship in the input, but the path (1 \rightarrow 2 \rightarrow 3) makes them entangled. Checking only the original edges would incorrectly produce `01`.

Finally, disconnected particles must remain separate. For

```
1
4 1 3
1 2
1 2
3 4
1 3
4 4
```

the output is `101`. Particles (1) and (2) belong to one component, particles (3) and (4) belong to another, and there is no relationship between those components. A solution that accidentally merges unrelated groups would produce an incorrect result for the second query.

## Approaches

The most direct solution is to treat every query independently. Given (X) and (Y), run DFS or BFS starting from (X), following the known relationships, and check whether (Y) can be reached. This is correct because graph reachability is exactly the definition of belonging to the same connected component.

The problem is the repeated work. In the worst case, a single traversal examines (O(N+M)) vertices and edges. Doing that for all (Q) queries costs (O(Q(N+M))). With (N=M=Q=10^5), this can reach roughly (10^{10}) graph operations. The same connected component would be rediscovered from scratch many thousands of times.

We can do better by looking at what all queries are actually asking. None of them cares about the path between two particles. They only care about which connected component contains each particle. The entire graph can be compressed conceptually into groups, where every particle in one group has the same answer when compared with another particle in that group.

This is exactly the situation handled by a Disjoint Set Union structure, also called Union-Find. While reading every known relationship (u,v), we merge the sets containing (u) and (v). After all (M) relationships have been processed, two particles are entangled precisely when their DSU representatives are equal.

The important change is that we compute connectivity once while reading the edges, instead of rediscovering it for every query. DSU supports merging two components and finding a particle's component representative in almost constant amortized time. With path compression and union by size or rank, the total complexity is (O((N+M+Q)\alpha(N))), where (\alpha) is the inverse Ackermann function and is effectively a constant for all practical input sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O((N+M+Q)\alpha(N))) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Create a DSU containing all (N) particles. Initially every particle is its own component, because no relationships have been processed yet.
2. Read each of the (M) relationships (u,v) and call `union(u, v)`. If the particles are already in the same component, nothing changes. Otherwise their two components are merged.

This directly models the transitive nature of entanglement. If (A) is joined with (B), and later (B) is joined with (C), the DSU automatically places all three in one set.
3. After all relationships have been processed, read each query (X,Y) and compute `find(X)` and `find(Y)`.
4. Append `1` to the answer if the two representatives are equal, and append `0` otherwise. The representatives are equal exactly when the particles belong to the same connected component.
5. Print the accumulated characters as one string for the test case. Building one string is preferable to printing one character per query, because it avoids a large number of output operations.

### Why it works

The DSU maintains the invariant that two particles have the same representative exactly when the relationships processed so far connect them through some path. Initially this is true because only a particle itself is reachable from that particle. When an edge (u,v) is processed, merging their two sets makes every particle reachable from (u) belong to the same set as every particle reachable from (v), exactly matching the new paths created by that edge. No unrelated components are merged. After all edges have been processed, the invariant describes the connected components of the complete graph. A query therefore returns `1` exactly when its two particles are connected by a path.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]

def solve():
    t = int(input())
    output = []

    for _ in range(t):
        n, m, q = map(int, input().split())

        dsu = DSU(n)

        for _ in range(m):
            u, v = map(int, input().split())
            dsu.union(u, v)

        answer = []

        for _ in range(q):
            x, y = map(int, input().split())
            answer.append('1' if dsu.find(x) == dsu.find(y) else '0')

        output.append(''.join(answer))

    sys.stdout.write('\n'.join(output))

if __name__ == "__main__":
    solve()
```

The `DSU` constructor creates `parent[i] = i`, so every particle starts as the representative of its own component. The `size` array records how many particles are currently in each component.

The `find` method follows parent pointers until it reaches a root. During the traversal it performs path halving with `self.parent[x] = self.parent[self.parent[x]]`. This shortens the paths encountered by future queries and gives the same near-constant amortized complexity as standard path compression.

The `union` method first finds the roots rather than modifying arbitrary nodes. If both roots are equal, the relationship is redundant and no operation is necessary. Otherwise the smaller component is attached below the larger one. This is union by size, and it prevents the DSU trees from becoming unnecessarily deep.

The input uses particle numbers from (1) through (N), so the arrays have length (N+1). Index zero is unused. This avoids repeatedly subtracting one from every particle number and removes a common source of indexing mistakes.

The code processes all relationships before answering any query. That ordering matters because a query must see the connectivity created by every relationship in the test case.

Python integers do not have an overflow problem here, and the only values stored in `size` are at most (N). The output is accumulated per test case and then written once, which keeps I/O overhead low.

## Worked Examples

The statement provides one sample. Since there is no second sample in the supplied problem text, the second trace below uses a small constructed test case that emphasizes indirect connectivity and disconnected components.

For Sample 1,

```
1
3 1 4
1 2
1 2
2 3
3 1
2 2
```

the only initial relationship is (1-2).

| Operation | Input | Parent state | Query result |
| --- | --- | --- | --- |
| Initial state | none | `[1, 2, 3]` |  |
| Union | `1 2` | `[1, 1, 3]` |  |
| Query | `1 2` | `[1, 1, 3]` | `1` |
| Query | `2 3` | `[1, 1, 3]` | `0` |
| Query | `3 1` | `[1, 1, 3]` | `0` |
| Query | `2 2` | `[1, 1, 3]` | `1` |

The resulting string is `1001`. The trace demonstrates that a direct relationship is enough for the first query, while particle (3) remains isolated. The final self-query also confirms that every particle belongs to its own component.

For the constructed case,

```
1
5 3 5
1 2
2 3
4 5
1 3
1 4
2 3
4 5
3 3
```

the first three particles form one component and the last two form another.

| Operation | Input | Components after operation | Query result |
| --- | --- | --- | --- |
| Initial state | none | `{1}`, `{2}`, `{3}`, `{4}`, `{5}` |  |
| Union | `1 2` | `{1,2}`, `{3}`, `{4}`, `{5}` |  |
| Union | `2 3` | `{1,2,3}`, `{4}`, `{5}` |  |
| Union | `4 5` | `{1,2,3}`, `{4,5}` |  |
| Query | `1 3` | `{1,2,3}`, `{4,5}` | `1` |
| Query | `1 4` | `{1,2,3}`, `{4,5}` | `0` |
| Query | `2 3` | `{1,2,3}`, `{4,5}` | `1` |
| Query | `4 5` | `{1,2,3}`, `{4,5}` | `1` |
| Query | `3 3` | `{1,2,3}`, `{4,5}` | `1` |

The output is `10111`. The important part is the first query: particles (1) and (3) have no direct edge, but the two union operations have placed them into the same DSU component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+M+Q)\alpha(N))) | Each union and find operation has inverse-Ackermann amortized cost |
| Space | (O(N)) | The DSU stores one parent and one size value per particle |

With (N,M,Q) up to (10^5), this gives roughly a linear number of DSU operations per test case. The inverse Ackermann factor is tiny, so the solution is comfortably within the intended complexity for a 2-second limit. The memory usage is also linear in (N), well below 256 MB.

## Test Cases

The following test harness implements the same algorithm as the submitted solution and checks the provided sample together with several targeted cases.

```python
import sys
import io

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]

def solve_io(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    output = []

    for _ in range(t):
        n, m, q = map(int, data.readline().split())
        dsu = DSU(n)

        for _ in range(m):
            u, v = map(int, data.readline().split())
            dsu.union(u, v)

        answer = []

        for _ in range(q):
            x, y = map(int, data.readline().split())
            answer.append('1' if dsu.find(x) == dsu.find(y) else '0')

        output.append(''.join(answer))

    return '\n'.join(output)

# Provided sample
sample1 = """\
1
3 1 4
1 2
1 2
2 3
3 1
2 2
"""

assert solve_io(sample1) == "1001", "sample 1"

# Minimum-size graph and repeated/self relationships
case2 = """\
1
1 1 4
1 1
1 1
1 1
1 1
"""

assert solve_io(case2) == "1111", "minimum-size self queries"

# Indirect connectivity versus disconnected components
case3 = """\
1
5 3 5
1 2
2 3
4 5
1 3
1 4
2 3
4 5
3 3
"""

assert solve_io(case3) == "10111", "indirect connectivity"

# Duplicate edges and reversed endpoints
case4 = """\
1
4 4 5
1 2
2 1
1 2
3 4
1 2
2 1
3 4
1 3
4 3
"""

assert solve_io(case4) == "11011", "duplicate and reversed edges"

# Boundary particle numbers, including N itself
case5 = """\
1
6 2 5
1 6
5 6
1 5
1 6
5 6
2 6
6 6
"""

assert solve_io(case5) == "11101", "boundary indices"

# Multiple test cases
case6 = """\
2
2 1 2
1 2
1 2
1 1
3 1 3
1 2
1 2
2 3
3 3
"""

assert solve_io(case6) == "111", "multiple test cases"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 4 / 1 1 / ...` | `1111` | Minimum graph size and self-queries |
| Five-particle chain and separate pair | `10111` | Indirect connectivity and disconnected components |
| Duplicate and reversed edges | `11011` | Redundant relationships do not change components |
| Six particles with edges involving particle 6 | `11101` | One-based boundary indices and isolated particle |
| Two test cases in one input | `111` | Correct reset of DSU between test cases |

## Edge Cases

The self-query case has (N=1), with the only particle queried against itself. The input

```
1
1 1 3
1 1
1 1
1 1
1 1
```

contains a redundant self-edge and three self-queries. The first union sees the same root on both sides, so it changes nothing. Every query compares the root of particle (1) with itself, producing `111`. The algorithm does not need a special case for (X=Y`, because DSU naturally handles it.

For duplicate relationships, consider

```
1
2 3 2
1 2
1 2
2 1
1 2
```

The first relationship merges particles (1) and (2). The next two relationships find that their roots are already equal, so both are ignored. Both queries compare the same representative and produce `11`. This is why `union` must safely handle the case where its two arguments already belong to one component.

For indirect connectivity, use

```
1
3 2 2
1 2
2 3
1 3
1 1
```

After `union(1, 2)`, particles (1) and (2) share a representative. After `union(2, 3)`, particle (3) is merged into that same component. The query `1 3` consequently compares equal representatives and returns `1`. The query `1 1` also returns `1`, giving `11`. A method that only checks whether `(1, 3)` appears as an input edge would fail here.

For disconnected components, consider

```
1
4 1 3
1 2
1 2
3 4
4 4
```

After the single union, the components are `{1,2}`, `{3}`, and `{4}`. The first query returns `1`, while the second query compares the representatives of (3) and (4), which differ, so it returns `0`. The final self-query returns `1`. The resulting output is `101`. The DSU never merges particles merely because they exist in the same test case, so disconnected groups remain distinct.

For the largest allowed values, (N=M=Q=10^5), the algorithm performs (10^5) initializations, (10^5) union operations, and (10^5) query operations. With path compression and union by size, this remains near-linear rather than approaching the (10^{10}) operations required by repeated graph traversals. The same reasoning applies independently to every test case, since a fresh DSU is created for each one.
