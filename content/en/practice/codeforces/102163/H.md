---
title: "CF 102163H - Mr. Hamra and his quantum particles"
description: "Think of the particles as vertices of an undirected graph. Every known entanglement relation gives an edge between two vertices."
date: "2026-08-23T22:21:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "H"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 832
verified: true
draft: false
---

[CF 102163H - Mr. Hamra and his quantum particles](https://codeforces.com/problemset/problem/102163/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the particles as vertices of an undirected graph. Every known entanglement relation gives an edge between two vertices. The transitive property in the statement means that if there is a path from particle (x) to particle (y), then the two particles are considered entangled, even if no direct relation was given between them.

For every query ((x,y)), we therefore need to determine whether (x) and (y) belong to the same connected component of the graph. The output is a binary string in query order. The (i)-th character is `1` when the two queried particles are connected through the given relations, and `0` otherwise.

The values of (N), (M), and (Q) can each reach (10^5). With that scale and a 2 second limit, an algorithm that performs a graph traversal for every query is far too expensive. A single traversal can already inspect (O(N+M)) vertices and edges, so repeating it (10^5) times can reach roughly (10^{10}) graph operations. Quadratic work such as checking every pair of particles is even less viable. We need to process the graph once and make each query close to constant time.

There are a few cases where a careless implementation can give the wrong result. Duplicate relations must not change connectivity. For example,

```
1
3 2 3
1 2
1 2
1 2
2 3
3 1
```

has only one actual connection between particles 1 and 2, but particle 3 is isolated. The correct output is `110` because 1 and 2 are connected, 1 and 2 are connected again, and 1 and 3 are not. An implementation that treats the number of input edges as though every edge connected a new component could make incorrect assumptions about the graph structure.

A query can also contain the same particle twice. For example,

```
1
1 1 2
1 1
1 1
1 1
```

has output `11`. A particle is always connected to itself because a vertex belongs to the same connected component as itself. An implementation that only checks whether there is an explicit edge between the two queried vertices would fail on such a query.

Finally, connectivity can be indirect rather than direct. Consider

```
1
3 2 2
1 2
2 3
1 3
1 1
```

The output is `11`. There is no direct edge between 1 and 3, but the path (1 \rightarrow 2 \rightarrow 3) makes them part of the same connected component. Looking only for explicitly listed pairs would incorrectly answer `0` for the first query.

## Approaches

The direct approach is to build an adjacency list and run BFS or DFS for every query. Starting from (x), we explore all particles reachable from (x), then check whether (y) was reached. This is correct because graph reachability is exactly the definition of the transitive entanglement relation.

The problem is the repeated work. In the worst case, one BFS can visit all (N) vertices and inspect all (M) edges, giving (O(N+M)) time for one query. With (Q) queries, the total becomes (O(Q(N+M))). At the maximum values, this is about (10^5(10^5+10^5)=2\cdot10^{10}) operations, far beyond the time limit.

The useful observation is that the graph itself does not change between queries. Every query asks the same question about a fixed partition of the vertices into connected components. We do not need to rediscover those components separately for every pair.

A Disjoint Set Union structure, also called Union-Find, represents exactly this partition. While reading every edge ((u,v)), we merge the components containing (u) and (v). After all edges have been processed, two particles are connected precisely when their DSU representatives are equal. Each query can then be answered with two `find` operations.

The brute-force solution works because graph traversal correctly discovers reachability, but it fails because it repeatedly discovers the same components. The observation that all queries refer to one fixed graph lets us compute its connected components once and reduce each query to a component comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q(N+M))) | (O(N+M)) | Too slow |
| Optimal | (O((N+M+Q)\alpha(N))) | (O(N)) | Accepted |

Here (\alpha(N)) is the inverse Ackermann function, which grows so slowly that it is effectively constant for all practical input sizes.

## Algorithm Walkthrough

1. Create a DSU structure with one set for every particle. Initially every particle is its own component because no relations have been processed yet.
2. For each of the (M) known entanglement relations ((u,v)), call `union(u, v)`. If the two particles already belong to the same component, nothing needs to change. Otherwise, their components are merged because an edge between them makes every particle reachable from one side reachable from the other.
3. After all relations have been processed, read each query ((x,y)) and compute `find(x)` and `find(y)`. If the representatives are equal, append `1` to the answer. Otherwise append `0`.
4. Print the collected characters as one string. Building the answer in a list avoids repeatedly constructing a new long string while processing the queries.

### Why it works

The DSU invariant is that two particles have the same representative exactly when all processed edges connect them through one connected component. Initially this is true because every particle is alone. When an edge joins two different components, `union` merges exactly those two components, preserving the invariant. When the two endpoints are already in the same component, the edge adds no new connectivity and leaving the DSU unchanged is correct.

After every one of the (M) edges has been processed, the DSU components are exactly the connected components of the entire graph. A query asks whether (x) and (y) are connected, which is equivalent to asking whether they have the same representative. Thus every output character is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    output = []

    for _ in range(t):
        n, m, q = map(int, input().split())

        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)

            if ra == rb:
                return

            if size[ra] < size[rb]:
                ra, rb = rb, ra

            parent[rb] = ra
            size[ra] += size[rb]

        for _ in range(m):
            u, v = map(int, input().split())
            union(u, v)

        ans = []

        for _ in range(q):
            x, y = map(int, input().split())
            ans.append('1' if find(x) == find(y) else '0')

        output.append(''.join(ans))

    sys.stdout.write('\n'.join(output))

if __name__ == "__main__":
    solve()
```

The `parent` array stores the parent of every DSU node. A root is identified by `parent[x] == x`, so initializing `parent` with `range(n + 1)` creates (N) separate components. The extra position at index zero lets us use the particle numbers directly because the input vertices are numbered from 1 through (N).

The `size` array supports union by size. When two different roots are merged, the smaller tree is attached below the larger one. This keeps the DSU trees shallow. The `find` function also performs path compression by changing each visited node to point closer to the root. The combination of these two optimizations gives the near-constant amortized complexity represented by (\alpha(N)).

Duplicate edges are naturally handled by `union`. If both endpoints already have the same representative, the function returns immediately. Self-edges behave the same way, and they do not need any special case.

The code processes all edges before answering queries, which matches the fact that the entire graph is fixed before any questions are asked. No adjacency list is necessary, so the implementation uses only (O(N)) auxiliary memory.

There is no integer overflow concern in Python. The implementation uses iterative `find`, which also avoids recursion-depth issues that could arise from a recursive implementation in Python.

## Worked Examples

For Sample 1, the graph contains particles 1 and 2 connected by one edge. The second occurrence of `1 2` in the input is a duplicate relation, so it does not change the component structure.

| Operation | Pair | Representative state | Query result |
| --- | --- | --- | --- |
| Initialize | none | `{1}`, `{2}`, `{3}` |  |
| Union | `(1, 2)` | `{1,2}`, `{3}` |  |
| Query | `(1,2)` | `find(1) = 1`, `find(2) = 1` | `1` |
| Query | `(2,3)` | `find(2) = 1`, `find(3) = 3` | `0` |
| Query | `(3,1)` | `find(3) = 3`, `find(1) = 1` | `0` |
| Query | `(2,2)` | `find(2) = 1`, `find(2) = 1` | `1` |

The resulting string is `1001`. This trace demonstrates both duplicate-free component construction and the fact that a particle is always connected to itself.

For a second example, consider the following input:

```
1
5 3 4
1 2
2 3
4 5
1 3
1 5
4 5
2 2
```

The first three edges create two nontrivial components, ({1,2,3}) and ({4,5}), while particle 5 is not connected to the first component.

| Operation | Pair | Components / Representatives | Query result |
| --- | --- | --- | --- |
| Initialize | none | `{1}`, `{2}`, `{3}`, `{4}`, `{5}` |  |
| Union | `(1,2)` | `{1,2}`, `{3}`, `{4}`, `{5}` |  |
| Union | `(2,3)` | `{1,2,3}`, `{4}`, `{5}` |  |
| Union | `(4,5)` | `{1,2,3}`, `{4,5}` |  |
| Query | `(1,3)` | same representative | `1` |
| Query | `(1,5)` | different representatives | `0` |
| Query | `(4,5)` | same representative | `1` |
| Query | `(2,2)` | same representative | `1` |

The output is `1011`. The first query confirms that DSU captures indirect connectivity, while the second confirms that separate components remain separate. The final query exercises the self-connectivity property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((N+M+Q)\alpha(N))) | Each edge performs at most two near-constant amortized DSU operations, and each query performs two `find` operations |
| Space | (O(N)) | The `parent` and `size` arrays each contain (N+1) entries |

With (N,M,Q\le10^5), the algorithm performs only a linear number of DSU operations per test case, each with effectively constant amortized cost. The memory usage is also linear in (N), comfortably within 256 MB. The approach avoids storing the graph entirely, which keeps both implementation and memory usage small.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    t = int(next(it))
    output = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        q = int(next(it))

        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)

            if ra == rb:
                return

            if size[ra] < size[rb]:
                ra, rb = rb, ra

            parent[rb] = ra
            size[ra] += size[rb]

        for _ in range(m):
            union(int(next(it)), int(next(it)))

        ans = []

        for _ in range(q):
            x = int(next(it))
            y = int(next(it))
            ans.append('1' if find(x) == find(y) else '0')

        output.append(''.join(ans))

    return '\n'.join(output)

# Provided sample
assert solve_data(
    """1
3 1 4
1 2
1 2
2 3
3 1
2 2
"""
) == "1001", "sample 1"

# Minimum-size graph, self-query and duplicate self-edge
assert solve_data(
    """1
1 1 3
1 1
1 1
1 1
1 1
"""
) == "111", "minimum-size self queries"

# Indirect connectivity plus a disconnected vertex
assert solve_data(
    """1
4 2 4
1 2
2 3
1 3
1 4
2 3
4 4
"""
) == "1011", "indirect connectivity"

# Duplicate edges and a component containing the largest-numbered vertex
assert solve_data(
    """1
5 4 5
1 2
1 2
2 3
4 5
1 2
2 3
1 5
4 5
5 5
"""
) == "11011", "duplicate edges and boundary vertex"

# Multiple test cases
assert solve_data(
    """2
3 1 3
1 2
1 2
2 3
3 3
4 3 4
1 2
2 3
3 4
1 4
2 4
1 1
3 4
"""
) == "101\n1111", "multiple test cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 3 / 1 1 / ...` | `111` | Minimum (N), self-queries, and self-edges |
| `4 2 4 / 1 2 / 2 3 / ...` | `1011` | Indirect connectivity, disconnected vertices, and self-query |
| `5 4 5 / 1 2 / 1 2 / ...` | `11011` | Duplicate edges and the largest valid vertex number |
| Two test cases | `101` and `1111` | Correct reset of DSU state between test cases |

## Edge Cases

A duplicate relation is handled by the same `union` operation as every other edge. For the input

```
1
3 2 3
1 2
1 2
1 2
2 3
3 1
```

the first `1 2` creates the component ({1,2}), while the second is ignored because both endpoints already have the same representative. The queries produce `110`, as expected. The DSU never assumes that every input edge must merge two different components.

For a self-query, consider

```
1
1 1 1
1 1
1 1
```

Particle 1 starts as its own component. The edge `1 1` leaves that component unchanged, and the query compares `find(1)` with itself. Both calls return the same root, so the output is `1`. No special branch for (x=y) is needed because the DSU definition already handles it correctly.

Indirect connectivity is covered by

```
1
3 2 1
1 2
2 3
1 3
```

After processing the first edge, particles 1 and 2 share a representative. After processing the second, particle 3 is merged into that same component. The query then finds the same representative for 1 and 3 and outputs `1`, even though the pair `1 3` never appeared as an input edge.

A disconnected query behaves oppositely. With

```
1
4 2 1
1 2
2 3
1 4
```

the components are ({1,2,3}) and ({4}). The query compares the representative of 1 with the representative of 4, which are different, so the answer is `0`. This is exactly the distinction between direct reachability inside a component and unrelated particles.

Finally, multiple test cases require a fresh DSU for each graph. The `parent` and `size` arrays are allocated inside the test-case loop, so no component information can leak from one test case into the next.
