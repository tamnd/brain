---
title: "CF 102163H - Mr. Hamra and his quantum particles"
description: "Treat the particles as vertices of an undirected graph. Every known entanglement relation gives an edge between two particles."
date: "2026-08-19T14:47:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "H"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 257
verified: false
draft: false
---

[CF 102163H - Mr. Hamra and his quantum particles](https://codeforces.com/problemset/problem/102163/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Treat the particles as vertices of an undirected graph. Every known entanglement relation gives an edge between two particles. The transitive property of entanglement means that if there is a path from particle (A) to particle (B), then (A) and (B) are considered entangled, even when no direct edge connects them.

For each test case, the input gives the number of particles (N), the number of known relations (M), and the number of queries (Q). The next (M) pairs describe graph edges. The following (Q) pairs ask whether the two named vertices belong to the same connected component. The required output is a binary string, with one character per query. A `1` means the two particles are connected through the given relations, while a `0` means they are in different connected components.

The bounds reach (10^5) for each of (N), (M), and (Q). With (10^5) vertices and edges, an algorithm that explores the graph separately for every query can perform around (10^{10}) graph operations in the worst case. That is far beyond what a 2 second limit permits. Even an (O(N^2)) preprocessing approach is too expensive at this scale, so the solution needs to process the graph and all queries essentially linearly.

There are several small cases that can make an incorrect implementation fail silently. A query can ask about a vertex and itself. For example,

```
1
1 1 1
1 1
1 1
```

has answer `1`. A vertex is always in the same connected component as itself, regardless of whether there are useful edges.

Duplicate edges also do not create additional components. For example,

```
1
3 2 2
1 2
1 2
2 3
1 3
```

has answer `11`. The two copies of the edge (1,2) represent the same connection, and the path (1\rightarrow2\rightarrow3) connects particles (1) and (3).

A query does not require a direct edge. For example,

```
1
3 2 2
1 2
2 3
1 3
1 2
```

has answer `11`. A solution that checks only whether the queried pair appeared among the input edges would incorrectly return `01`. The transitive property is exactly what turns ordinary graph reachability into the required relation.

Finally, vertices may remain completely isolated. With

```
1
3 1 2
1 2
1 3
3 3
```

the answer is `01`. Particle (3) has no connection to particle (1), but it is connected to itself. An implementation that assumes every vertex belongs to a nontrivial edge can mishandle this case.

## Approaches

The most direct approach is to run a graph traversal for every query. Build an adjacency list from the (M) known relations, then for a query ((X,Y)), run BFS or DFS starting at (X) and check whether (Y) is reached. This is correct because the query asks exactly whether a path exists between the two vertices.

The problem is repeated work. A single BFS can inspect (O(N+M)) vertices and edges. Doing that independently for all (Q) queries gives (O(Q(N+M))) time. With all three values around (10^5), the worst case is on the order of (10^{10}) operations. Even if many queries happen to concern the same component, the traversal keeps rediscovering the same information.

The graph has a stronger structure than arbitrary reachability queries. We do not need to know the actual path between two particles. We only need to know which connected component each particle belongs to. Once two particles have been assigned the same component identifier, every query involving them can be answered immediately.

This is exactly the situation handled by a Disjoint Set Union structure, also called Union-Find. Initially every particle forms its own component. For every known relation ((u,v)), we merge the components containing (u) and (v). After all (M) relations have been processed, two particles are entangled precisely when their DSU representatives are equal.

The useful insight is that the transitive property lets us replace an entire connected component with one representative. Instead of repeatedly searching paths, we maintain the equivalence classes directly. With path compression and union by size, each operation takes amortized (O(\alpha(N))), where (\alpha) is the inverse Ackermann function and is effectively constant for any input size encountered in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O((N+M+Q)\alpha(N))) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Create a DSU containing all (N) particles. Initially, every particle is its own component, so `parent[i] = i` and every component has size one.
2. Read each of the (M) known entanglement relations ((u,v)) and call `union(u, v)`. If the two particles already belong to the same component, nothing changes. Otherwise, merge their components.

This is the step where all direct relations are converted into connected components. Repeated unions automatically propagate transitivity, so a chain such as (1\leftrightarrow2\leftrightarrow3) eventually puts all three particles in one set.
3. For every query ((x,y)), call `find(x)` and `find(y)`. If the two returned representatives are equal, append `1` to the answer string. Otherwise append `0`.
4. After processing all (Q) queries, print the accumulated characters as one string. Building a list of characters and joining it once avoids repeated string concatenation.

### Why it works

The DSU invariant is that two particles have the same representative exactly when the relations processed so far connect them through some path. Initially this is true because no edges have been processed and every vertex is isolated. When an edge ((u,v)) is processed, if its endpoints are already in the same set, the invariant remains unchanged. If they are in different sets, the edge creates a connection between those two components, so merging them is exactly the required update. After all edges have been processed, two particles have the same representative exactly when they are in the same connected component of the original graph. Each query therefore returns `1` exactly for entangled pairs.

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

        ans = []

        for _ in range(q):
            x, y = map(int, input().split())
            ans.append('1' if dsu.find(x) == dsu.find(y) else '0')

        output.append(''.join(ans))

    sys.stdout.write('\n'.join(output))

if __name__ == "__main__":
    solve()
```

The `DSU` constructor creates one set for every particle. The arrays have size (N+1) because the vertices are numbered from (1) through (N), so index zero is unused.

The `find` function returns the representative of the component containing a vertex. The assignment `parent[x] = parent[parent[x]]` performs path halving, shortening paths while searching. Together with union by size, this gives the required near-constant amortized complexity.

The `union` function first finds the representatives rather than attaching arbitrary vertices. If both representatives are equal, the edge is redundant. Otherwise the smaller component is attached below the larger one. This keeps the DSU trees shallow.

The input edges are processed before any queries. This ordering matters because a query must see the complete set of known relations, not just the relations read before that query. The implementation never needs an adjacency list because only component membership matters.

The answer for each test case is stored as a list of characters and joined once. The list also naturally handles (Q=10^5) without the overhead of repeatedly constructing longer immutable strings.

Python integers do not have an overflow issue here. The only values manipulated are vertex indices and component sizes, both bounded by (10^5).

## Worked Examples

### Sample 1

The input graph has three particles and one initial edge, (1\leftrightarrow2). The four queries are processed after the DSU has incorporated that edge.

| Operation | Particle / Query | Parent state | Result |
| --- | --- | --- | --- |
| Initialize | (1,2,3) | `[1, 2, 3]` | Three components |
| Union | (1,2) | `parent[2] = 1` | Components `{1,2}`, `{3}` |
| Query | (1,2) | representatives `1,1` | `1` |
| Query | (2,3) | representatives `1,3` | `0` |
| Query | (3,1) | representatives `3,1` | `0` |
| Query | (2,2) | representatives `1,1` | `1` |

The resulting string is `1001`. The final query also demonstrates that a particle is always connected to itself.

### Constructed Example 2

Consider a chain of four particles:

```
1
4 3 4
1 2
2 3
3 4
1 4
1 3
2 4
2 2
```

After the three unions, all four particles belong to one component.

| Operation | Particle / Query | Representative state | Result |
| --- | --- | --- | --- |
| Initialize | (1,2,3,4) | `1,2,3,4` | Four components |
| Union | (1,2) | `1,1,3,4` | `{1,2}` |
| Union | (2,3) | `1,1,1,4` | `{1,2,3}` |
| Union | (3,4) | `1,1,1,1` | `{1,2,3,4}` |
| Query | (1,4) | `1,1` | `1` |
| Query | (1,3) | `1,1` | `1` |
| Query | (2,4) | `1,1` | `1` |
| Query | (2,2) | `1,1` | `1` |

The output is `1111`. This demonstrates why checking only direct edges would be insufficient. There is no direct (1,4) edge, but the DSU captures the entire connected chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+M+Q)\alpha(N))) | Each union and find operation has amortized inverse-Ackermann complexity |
| Space | (O(N)) | The DSU stores one parent and one size value per particle |

With (N,M,Q\le10^5), the number of DSU operations is at most a few hundred thousand per test case, and each is effectively constant time. The memory usage is linear in the number of particles, well within the 256 MB limit. The solution also avoids storing all (M) edges after they have been processed, which keeps the memory footprint smaller than a traversal-based solution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from contextlib import redirect_stdout

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
    input = sys.stdin.readline
    t = int(input())
    output = []

    for _ in range(t):
        n, m, q = map(int, input().split())
        dsu = DSU(n)

        for _ in range(m):
            u, v = map(int, input().split())
            dsu.union(u, v)

        ans = []
        for _ in range(q):
            x, y = map(int, input().split())
            ans.append('1' if dsu.find(x) == dsu.find(y) else '0')

        output.append(''.join(ans))

    sys.stdout.write('\n'.join(output))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin

    return out.getvalue()

# Provided sample
assert run("""\
1
3 1 4
1 2
1 2
2 3
3 1
2 2
""") == "1001", "sample 1"

# Minimum-size graph, self-query, duplicate self-edge
assert run("""\
1
1 1 3
1 1
1 1
1 1
1 1
""") == "111", "minimum size"

# Transitive chain, no direct edge between the queried endpoints
assert run("""\
1
4 2 4
1 2
2 3
1 3
1 4
2 3
4 4
""") == "1011", "transitivity and isolated vertex"

# Duplicate edges and separate components
assert run("""\
1
5 5 5
1 2
1 2
2 3
4 5
4 5
1 3
1 5
4 5
2 2
3 4
""") == "10110", "duplicate edges and component separation"

# Multiple test cases, boundary vertex labels
assert run("""\
2
2 1 2
1 2
1 2
2 1
3 1 3
2 3
1 1
1 3
2 3
""") == "11\n011", "multiple test cases and boundary labels"

# Large connected chain, exercises the implementation at scale
n = 100000
edges = '\n'.join(f"{i} {i + 1}" for i in range(1, n))
queries = '\n'.join([
    f"1 {n}",
    f"1 {n - 1}",
    f"{n} {n}",
    f"1 1",
    f"50000 50001",
])

large_input = f"1\n{n} {n - 1} 5\n{edges}\n{queries}\n"
assert run(large_input) == "11111", "large connected chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` with a self-edge and self-queries | `111` | Minimum size and self-connectivity |
| Four vertices with edges `1-2`, `2-3` | `1011` | Transitive connectivity and an isolated vertex |
| Five vertices with duplicate edges and two components | `10110` | Duplicate relations and component separation |
| Two independent test cases | `11` and `011` | Correct state reset between test cases and boundary labels |
| A chain containing 100000 vertices | `11111` | Large input size and DSU performance |

## Edge Cases

For the self-query case,

```
1
1 1 1
1 1
1 1
```

the DSU starts with `parent[1] = 1`. Processing the self-edge calls `union(1,1)`, and both `find` operations return the same representative, so the union does nothing. The query also obtains the same representative twice and produces `1`. The output is `1`.

For duplicate edges,

```
1
3 2 2
1 2
1 2
2 3
1 3
```

the first `1 2` union joins particles (1) and (2). The second `1 2` edge finds the same representative for both endpoints and is ignored. The edge `2 3` then joins particle (3) to that component. The query `1 3` consequently returns `1`. The output is `11`.

For transitive connectivity,

```
1
3 2 1
1 2
2 3
1 3
```

the first union creates component `{1,2}`, and the second expands it to `{1,2,3}`. The query has no direct edge between (1) and (3), but both calls to `find` return the same representative. The output is `1`.

For an isolated vertex,

```
1
3 1 2
1 2
1 3
3 3
```

the first union creates component `{1,2}`, while particle (3) remains in its own component. The query `1 3` compares different representatives and gives `0`. The query `3 3` compares the same representative with itself and gives `1`, producing `01`.

For multiple test cases, the DSU must be recreated for every test case. Suppose the first case connects particles (1) and (2), while the second case has completely different relations. If the same DSU were reused, information from the first graph would leak into the second graph and produce false connections. The implementation constructs a fresh `DSU(n)` inside the test-case loop, so every graph starts with all of its own particles separate.
