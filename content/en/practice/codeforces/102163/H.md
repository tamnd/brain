---
title: "CF 102163H - Mr. Hamra and his quantum particles"
description: "Think of the particles as vertices of an undirected graph. Every known entanglement relation gives us an edge between two particles."
date: "2026-08-19T07:49:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "H"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 171
verified: false
draft: false
---

[CF 102163H - Mr. Hamra and his quantum particles](https://codeforces.com/problemset/problem/102163/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
## Problem Understanding

Think of the particles as vertices of an undirected graph. Every known entanglement relation gives us an edge between two particles. The transitive rule says that if we can move from particle A to B through a chain of known relations, then A and B are considered entangled even if there is no direct edge between them.

So each connected component of the graph represents one group of mutually entangled particles. For every query `(X, Y)`, we only need to determine whether X and Y belong to the same connected component. The required output is a binary string, with one character per query, where `1` means the two particles are connected and `0` means they are in different components.

With up to `10^5` particles, `10^5` known relations, and `10^5` queries in a single test case, an algorithm that scans a large part of the graph for every query is too expensive. A worst-case `O(NQ)` or `O((N+M)Q)` method can reach roughly `10^10` graph operations, far beyond what a two-second limit allows. We need preprocessing close to linear in the input size, followed by almost constant-time queries.

There are several small cases that can make a careless implementation fail. A query can ask about the same particle twice. For example,

```
1
1 1 1
1 1
1 1
```

has output `1`, because every vertex is connected to itself. An implementation that only checks whether a path contains at least one edge could incorrectly return `0`.

Duplicate relations are also allowed by the input as written. In Sample 1, the edge `1 2` appears twice. These duplicates must not change the component structure. For example,

```
1
3 2 2
1 2
1 2
2 3
```

would connect all three particles, so a query such as `(1, 3)` must return `1`. A solution that treats every input edge as a distinct relationship still gets the right connectivity if implemented normally, but any logic based on counting unique edges must handle duplicates correctly.

Another common mistake is checking only direct edges. Consider,

```
1
3 2 1
1 2
2 3
1 3
```

The answer is `1`, even though there is no direct `1 3` edge. The transitive rule makes the path `1 -> 2 -> 3` sufficient.

Finally, disconnected vertices must remain separate. For example,

```
1
4 2 2
1 2
3 4
1 3
2 2
```

produces `01`. The first query crosses two components, while the second asks about the same vertex.

## Approaches

The direct approach is to answer every query with a graph traversal. Starting from X, we run DFS or BFS and mark all particles reachable from X. If Y is reached, the answer is `1`; otherwise it is `0`. This is correct because reachability in an undirected graph is exactly the transitive closure of the given entanglement relation.

The problem is that the traversal can cost `O(N + M)` for one query. With `Q` queries, the worst-case complexity becomes `O(Q(N + M))`. When all three values are around `10^5`, this is about `2 * 10^10` operations in the worst case. Repeating essentially the same connectivity search for every query wastes the structure we have already discovered.

The key observation is that the answer to every query depends only on the connected component containing each endpoint. We do not need to know the actual path between two particles, and we do not need to explore the graph again after the components have been identified.

A Disjoint Set Union, also called Union-Find, is designed for exactly this situation. Initially every particle belongs to its own set. Whenever an edge `(u, v)` is read, we merge the sets containing u and v. After all M edges have been processed, two particles are entangled exactly when their DSU representatives are equal.

The brute-force method works because it reconstructs reachability from scratch. The observation that all queries ask about the same fixed collection of connected components lets us compute those components once and reduce each query to two representative lookups.

Path compression makes repeated `find` operations very cheap, while union by size keeps the trees shallow. The resulting amortized cost per DSU operation is `O(alpha(N))`, where `alpha` is the inverse Ackermann function and is effectively constant for every realistic input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(Q(N + M))` | `O(N + M)` | Too slow |
| Optimal | `O((N + M + Q) alpha(N))` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Create a DSU structure containing all N particles. Initially, every particle is its own component because no relationships have been processed yet.
2. Read each of the M relationships `(u, v)` and union the two particles. If they are already in the same component, the union operation does nothing. This naturally handles duplicate edges.
3. For every query `(x, y)`, find the representative of x and the representative of y. If the representatives are equal, both particles belong to the same connected component, so append `1` to the answer. Otherwise append `0`.
4. After all Q queries have been processed, print the accumulated characters as one binary string. Building the string once is preferable to printing each answer separately because it reduces output overhead.

### Why it works

The central invariant is that after processing any prefix of the edge list, two particles are in the same DSU set exactly when they are connected using only edges from that processed prefix. Initially this is true because no edges have been processed and every particle is isolated. When an edge `(u, v)` is processed, union merges exactly the two components connected by that edge, preserving the invariant. After all edges are processed, the DSU sets are precisely the connected components of the entire graph. Thus a query returns `1` exactly when its two particles are connected through a sequence of entanglement relations.

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
    outputs = []

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

        outputs.append(''.join(answer))

    sys.stdout.write('\n'.join(outputs))

if __name__ == "__main__":
    solve()
```

The DSU uses arrays indexed from `1` through `N`, matching the particle numbering in the input. Index `0` is simply unused, which avoids repeatedly subtracting one from every vertex number.

`parent[x]` stores the parent of x in the DSU forest. A root is identified by `parent[x] == x`. The `size` array stores the number of vertices in each root's set and allows union by size.

The `find` method uses iterative path halving. While walking toward the root, it makes each visited vertex point closer to its grandparent. Repeated queries then become extremely cheap because the trees flatten as they are accessed.

The `union` method first finds both roots. If they are equal, the edge connects particles already known to be connected, so there is nothing to merge. Otherwise, the smaller tree is attached to the larger tree. This keeps the forest shallow and is one half of the standard DSU optimization.

There is no integer overflow concern in Python, and the only potentially large structures are the `parent`, `size`, and output arrays. We also store the output of each test case as a string rather than accumulating one giant character structure unnecessarily.

## Worked Examples

### Sample 1

The input graph contains three particles and one distinct edge, `1 2`. The repeated `1 2` in the sample is not a second line of the graph, because the input has `M = 1`; it is the first query. The four queries are `(1, 2)`, `(2, 3)`, `(3, 1)`, and `(2, 2)`.

| Step | Operation | DSU components | Query result |
| --- | --- | --- | --- |
| 1 | Initialize | `{1}`, `{2}`, `{3}` |  |
| 2 | Union `1 2` | `{1,2}`, `{3}` |  |
| 3 | Query `1 2` | `{1,2}`, `{3}` | `1` |
| 4 | Query `2 3` | `{1,2}`, `{3}` | `0` |
| 5 | Query `3 1` | `{1,2}`, `{3}` | `0` |
| 6 | Query `2 2` | `{1,2}`, `{3}` | `1` |

The representatives of 1 and 2 are equal, while 3 has a different representative. A vertex always has the same representative as itself, so the final query produces `1`. The resulting string is `1001`.

### Constructed Example 2

Consider a graph where the relationships form a chain:

```
1
5 4 4
1 2
2 3
3 4
4 5
1 5
2 4
1 3
2 5
```

Each union extends the same connected component.

| Step | Operation | Main component | Query result |
| --- | --- | --- | --- |
| 1 | Initialize | `{1}`, `{2}`, `{3}`, `{4}`, `{5}` |  |
| 2 | Union `1 2` | `{1,2}`, `{3}`, `{4}`, `{5}` |  |
| 3 | Union `2 3` | `{1,2,3}`, `{4}`, `{5}` |  |
| 4 | Union `3 4` | `{1,2,3,4}`, `{5}` |  |
| 5 | Union `4 5` | `{1,2,3,4,5}` |  |
| 6 | Query `1 5` | `{1,2,3,4,5}` | `1` |
| 7 | Query `2 4` | `{1,2,3,4,5}` | `1` |
| 8 | Query `1 3` | `{1,2,3,4,5}` | `1` |
| 9 | Query `2 5` | `{1,2,3,4,5}` | `1` |

The example demonstrates why direct adjacency is not enough. There is no direct edge between most queried pairs, but every particle belongs to the same connected component after all four unions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((N + M + Q) alpha(N))` | M unions and Q queries each use DSU operations with amortized `O(alpha(N))` cost |
| Space | `O(N)` | The parent and size arrays each contain `N + 1` entries, and the answer contains Q characters |

For `N, M, Q <= 10^5`, the effective DSU factor `alpha(N)` is tiny, so the algorithm is essentially linear in the amount of input. This is comfortably within the intended two-second and 256 MB limits, while the repeated-search approach can require around `10^10` operations.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    t = next(it)
    outputs = []

    for _ in range(t):
        n = next(it)
        m = next(it)
        q = next(it)

        parent = list(range(n + 1))
        size = [1] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            a = find(a)
            b = find(b)

            if a == b:
                return

            if size[a] < size[b]:
                a, b = b, a

            parent[b] = a
            size[a] += size[b]

        for _ in range(m):
            u = next(it)
            v = next(it)
            union(u, v)

        answer = []

        for _ in range(q):
            x = next(it)
            y = next(it)
            answer.append('1' if find(x) == find(y) else '0')

        outputs.append(''.join(answer))

    return '\n'.join(outputs)

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
assert solve_data(sample1) == "1001", "sample 1"

# Minimum-size input, self-query
case2 = """\
1
1 1 1
1 1
1 1
"""
assert solve_data(case2) == "1", "minimum-size self query"

# Disconnected components and self query
case3 = """\
1
4 2 3
1 2
3 4
1 3
2 2
4 1
"""
assert solve_data(case3) == "010", "disconnected components"

# Transitive connectivity and duplicate edge
case4 = """\
1
5 4 4
1 2
2 3
2 3
4 5
1 3
1 5
4 5
3 3
"""
assert solve_data(case4) == "1011", "transitivity and duplicate edge"

# Maximum-size stress case
n = 100000
q = 100000

parts = ["1", f"{n} 1 {q}", "1 2"]
parts.extend(["1 100000"] * q)
case5 = "\n".join(parts) + "\n"

assert solve_data(case5) == "0" * q, "maximum-size boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 / 1 1 / 1 1` | `1` | Minimum size and self-connectivity |
| `4` vertices with edges `1 2` and `3 4` | `010` | Separate connected components and a self-query |
| Chain `1-2-3`, duplicate `2-3`, and edge `4-5` | `1011` | Transitive connectivity, duplicate edges, and component boundaries |
| `N=100000`, one edge, `Q=100000` | `0...0` | Large input size, vertex-number boundary `100000`, and output construction |

## Edge Cases

A self-query such as `(2, 2)` must always return `1`, even when particle 2 has no incident edge. For the input

```
1
3 1 2
1 2
2 2
2 3
```

the DSU after reading the only edge contains `{1,2}` and `{3}`. Both calls to `find(2)` return the same representative, so the first answer is `1`. The second query compares representatives of 2 and 3 and gets `0`, giving `10`.

A path can imply entanglement without a direct edge. For

```
1
3 2 1
1 2
2 3
1 3
```

the first union creates `{1,2}`, and the second union expands it to `{1,2,3}`. The query then sees identical representatives for 1 and 3 and returns `1`. Any solution that checks only whether `(1,3)` appears among the input edges would incorrectly produce `0`.

Duplicate edges do not create new components. With

```
1
3 2 2
1 2
1 2
1 3
2 3
```

the first `1 2` union creates `{1,2}`, while the second `1 2` finds the same representative for both endpoints and does nothing. The query `1 3` then returns `0`, and `2 3` also returns `0`, producing `00`. The DSU naturally ignores the duplicate without requiring any special duplicate-edge handling.

Disconnected components must not accidentally become connected through unrelated edges. For

```
1
4 2 2
1 2
3 4
1 3
2 2
```

the final sets are `{1,2}` and `{3,4}`. The query `1 3` compares different representatives and produces `0`, while `2 2` compares the same representative with itself and produces `1`. The final output is `01`.

The largest valid particle number is also a useful boundary check. With `N = 100000`, a query involving particle `100000` must access the final DSU entry rather than an out-of-range or incorrectly shifted index. The stress test above uses the edge `1 2` and repeatedly queries `1 100000`, so every answer is `0`. This catches implementations that accidentally allocate only `N` slots while using one-based vertex numbering.
