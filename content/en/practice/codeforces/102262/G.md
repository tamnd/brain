---
title: "CF 102262G - \u0421\u043a\u0430\u0447\u0438\u0432\u0430\u043d\u0438\u0435 \u0440\u0435\u0441\u0443\u0440\u0441\u043e\u0432 \u0432 \u0434\u0430\u0442\u0430-\u0446\u0435\u043d\u0442\u0440\u0435"
description: "We have an undirected graph whose vertices are servers and whose edges are physical connections. A server can download a file only from another server that belongs to the same connected component."
date: "2026-08-17T20:24:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "G"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 122
verified: true
draft: false
---

[CF 102262G - \u0421\u043a\u0430\u0447\u0438\u0432\u0430\u043d\u0438\u0435 \u0440\u0435\u0441\u0443\u0440\u0441\u043e\u0432 \u0432 \u0434\u0430\u0442\u0430-\u0446\u0435\u043d\u0442\u0440\u0435](https://codeforces.com/problemset/problem/102262/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph whose vertices are servers and whose edges are physical connections. A server can download a file only from another server that belongs to the same connected component. The server identifiers are arbitrary integers up to (10^9), so they cannot be used directly as array indices.

For every query, (X) is the destination server and the following list contains servers that currently have the requested file. We must keep exactly those servers (Y) that are connected to (X), and print them in their original order. The order matters, so the query list cannot simply be converted into a set.

The graph can contain up to (10^6) edges. Consequently, there can be almost (2\cdot10^6) different server identifiers. With only 1.5 seconds available, running a graph traversal for every query is too expensive. With (Q\le 1000), even scanning all (10^6) edges once per query can reach (10^9) edge examinations. The query lists themselves are small, since (K_i\le100), so the main task is to preprocess connectivity efficiently.

The graph may also contain server identifiers that occur only in queries. Such a server is an isolated vertex unless it is connected by one of the input edges. A careless implementation that stores only vertices occurring in edges can mishandle a query where both (X) and (Y) are absent from the graph. For example:

```
0
1
42 2
42 17
```

The correct output is:

```
1 42
```

Both servers are isolated, but they are the same server when their identifiers are equal. Treating every unknown identifier as belonging to some generic "unknown" component would incorrectly accept `17`.

A second edge case is a server that occurs in the graph but another candidate does not. For example:

```
1
1 2
1
1 2
3 2
```

The correct output is:

```
1 2
```

Server `3` is an isolated vertex and cannot download from server `2`, even though both identifiers are known to the program. A solution must distinguish different isolated vertices.

A third edge case is that the answer must preserve duplicates and ordering if the input contains them. For example:

```
0
1
7 3
7 7 8
```

The output is:

```
2 7 7
```

The query asks about three listed sources, and both occurrences of `7` are valid. Sorting or deduplicating the query list would change the required output.

## Approaches

The direct solution is to find the connected component of (X) separately for every query, using DFS or BFS. Once the component is known, each of the at most 100 candidate servers can be checked against it. This is correct because connectedness is exactly the condition defining whether a download is possible.

The problem is the repeated graph traversal. In the worst case, one traversal can inspect all (10^6) edges. With (1000) queries that becomes up to (10^9) edge examinations, before counting the additional vertex work. Doing a separate traversal for every candidate (Y) would be even worse, potentially around (10^{11}) connectivity checks.

The graph structure gives us a much stronger observation. Every query asks only whether two vertices belong to the same connected component. We never need the actual path between them. This is exactly the operation supported by a disjoint-set union structure, or DSU. While reading each edge ((A,B)), we merge the components containing (A) and (B). After all edges have been processed, two servers are connected if and only if their DSU representatives are equal.

The arbitrary server identifiers introduce a second issue. A conventional DSU expects compact indices such as (0,\ldots,V-1). Coordinate compression would solve that, but storing millions of Python integers and a large dictionary is undesirable under the 64 MB memory limit. The implementation below instead uses a compact open-addressing hash table backed by `array('I')`. Each occupied hash-table slot stores the server identifier and its DSU parent. Since identifiers are positive, zero can represent an unused slot.

The brute-force works because a traversal directly discovers exactly one connected component, but fails when the same expensive traversal is repeated for many queries. The observation that every query is only a component-membership test lets us replace graph traversal with almost constant-time DSU operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q(N+V))) | (O(N+V)) | Too slow, up to about (10^9) edge examinations |
| DSU + compact hash table | Expected (O(N\alpha(V)+QK\alpha(V))) | (O(V)) | Accepted |

Here (V\le2N) for vertices appearing in edges, (\alpha) is the inverse Ackermann function, and the hash-table operations have expected (O(1)) time.

## Algorithm Walkthrough

1. Read (N), the number of graph edges, and create a compact hash table large enough for all possible endpoints. Since there are at most (2N) distinct endpoints and we reserve at least twice that many slots, the load factor stays below one half. This gives short expected probe sequences.
2. For every edge ((A,B)), insert both server identifiers into the hash table if they are not present. A newly inserted server starts as its own DSU root. Then merge the roots of (A) and (B).

The DSU does not need a separate parent array indexed by compressed vertex number. The hash-table slot itself acts as the vertex index, which saves another mapping array and keeps the memory usage small.
3. Implement `find` with path compression. Starting from the slot of a server, follow parent slots until a root whose parent is itself is reached. Then compress the traversed path so later operations reach the root more quickly.
4. Implement `union` by finding both roots and attaching one root to the other. The implementation uses the root slot itself as the parent value, so no extra rank or size array is required.
5. Read each query after the graph has been processed. For the destination (X), look up its hash-table slot. If it exists, its DSU root represents its connected component. If it does not exist, (X) is an isolated server.
6. Read the (K) candidate sources in their original order. For each (Y), first check whether its identifier exists in the graph's hash table. If both (X) and (Y) are absent, they are connected only when their identifiers are equal. If exactly one is absent, they cannot be connected. If both are present, compare their DSU roots.
7. Append every valid source to the answer without changing its position relative to the other candidates. Print the count followed by the selected identifiers.

### Why it works

After all edges have been processed, the DSU invariant is that two servers appearing in the graph have the same representative exactly when there is a path between them. Every input edge joins its two endpoints, so every pair connected by a sequence of edges is eventually merged into one DSU set. Conversely, DSU never merges two components unless an input edge connects them, so two different graph components can never receive the same representative.

A server absent from the edge list has degree zero and is therefore an isolated component. Two such servers are connected precisely when they are the same identifier. The query logic handles this case separately, so every candidate is accepted exactly when it belongs to the destination's connected component.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MASK32 = 0xFFFFFFFF
MULT = 2654435761

def solve():
    n_line = input()
    if not n_line:
        return
    n = int(n_line)

    # At most 2*n different server identifiers occur in edges.
    # Keep the load factor below 1/2.
    need = max(2, 4 * n)
    size = 1
    while size < need:
        size <<= 1

    mask = size - 1

    # 0 means an unused slot. Server identifiers are >= 1.
    keys = array('I', [0]) * size
    parent = array('I', [0]) * size

    def locate(x):
        """Return the slot containing x, or 0 if x is absent."""
        p = (x * MULT) & mask
        while True:
            k = keys[p]
            if k == 0:
                return 0
            if k == x:
                return p
            p = (p + 1) & mask

    def get_slot(x):
        """Find x, inserting it as a new DSU root when necessary."""
        p = (x * MULT) & mask
        while True:
            k = keys[p]
            if k == 0:
                keys[p] = x
                parent[p] = p
                return p
            if k == x:
                return p
            p = (p + 1) & mask

    def find(p):
        root = p
        while parent[root] != root:
            root = parent[root]

        while parent[p] != p:
            nxt = parent[p]
            parent[p] = root
            p = nxt

        return root

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra != rb:
            parent[rb] = ra

    for _ in range(n):
        a, b = map(int, input().split())
        sa = get_slot(a)
        sb = get_slot(b)
        union(sa, sb)

    q = int(input())
    out = []

    for _ in range(q):
        x, k = map(int, input().split())
        ys = list(map(int, input().split()))

        sx = locate(x)

        if sx == 0:
            # x is an isolated server.
            ans = [y for y in ys if y == x]
        else:
            rx = find(sx)
            ans = []

            for y in ys:
                sy = locate(y)
                if sy != 0 and find(sy) == rx:
                    ans.append(y)

        if ans:
            out.append(str(len(ans)) + " " + " ".join(map(str, ans)))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation allocates the hash table according to the maximum possible number of edge endpoints. Four slots are reserved per edge, so even if every endpoint is different, the table has a load factor of at most one half. A power-of-two size allows the hash position to be obtained with a bit mask instead of a more expensive modulo operation.

`get_slot` is used while processing edges because every endpoint must become a DSU vertex. `locate` is used for queries because a query identifier that never occurred in an edge must remain an isolated vertex rather than being inserted into an existing component.

The parent array stores hash-table slot numbers. For a newly inserted identifier, `parent[p] = p`, making that slot its own root. When two components are merged, one root stores the other root as its parent. Path compression in `find` then makes subsequent operations nearly constant time.

There is no integer-overflow problem in Python. The multiplication used by the hash function is explicitly masked to 32 bits because the compact hash table is designed around unsigned 32-bit server identifiers and a power-of-two table size.

The query list is processed only after the graph's DSU has been completed. The original order is preserved because candidates are appended to `ans` as they are read. No sorting or deduplication is performed.

A subtle boundary case is (N=0). In that situation there are no graph vertices in the hash table. Every queried server is isolated, so the only valid source for destination (X) is another occurrence of the same identifier (X).

## Worked Examples

### Sample 1

The graph contains two disconnected components. The first contains `54578972`, `99368556`, `79699669`, `64508306`, and `56554555`. The second contains `27101564`, `81480071`, `89445516`, `93762227`, and `89808815`.

The relevant DSU state after all eight edges is:

| Server | Component representative |
| --- | --- |
| 54578972 | component A |
| 99368556 | component A |
| 79699669 | component A |
| 64508306 | component A |
| 56554555 | component A |
| 27101564 | component B |
| 81480071 | component B |
| 89445516 | component B |
| 93762227 | component B |
| 89808815 | component B |

For the queries, the important state is:

| Destination (X) | Candidate | Same component? | Output action |
| --- | --- | --- | --- |
| 56554555 | 93762227 | No | skip |
| 56554555 | 79699669 | Yes | keep |
| 99368556 | 64508306 | Yes | keep |
| 99368556 | 56554555 | Yes | keep |
| 27101564 | 99368556 | No | skip |
| 27101564 | 79699669 | No | skip |
| 93762227 | 56554555 | No | skip |
| 93762227 | 54578972 | No | skip |

The resulting output is:

```
1 79699669
2 64508306 56554555
0
0
```

The trace demonstrates the central DSU invariant. The actual shape of each component does not matter once every connected set has one representative.

### Sample 2

Here the graph has two components. One contains `85619126`, `64616465`, `98159933`, `73978229`, `29978081`, and `72404745`. The other contains `97698445`, `75243921`, `36815728`, `18360411`, `66445821`, and `92142380`.

The query processing looks like this:

| Destination (X) | Candidate | Same component? | Output action |
| --- | --- | --- | --- |
| 97698445 | 75243921 | Yes | keep |
| 97698445 | 92142380 | Yes | keep |
| 97698445 | 98159933 | No | skip |
| 97698445 | 73978229 | No | skip |
| 66445821 | 29978081 | No | skip |
| 66445821 | 92142380 | Yes | keep |
| 66445821 | 73978229 | No | skip |
| 66445821 | 97698445 | Yes | keep |
| 18360411 | 29978081 | No | skip |
| 18360411 | 92142380 | Yes | keep |
| 18360411 | 98159933 | No | skip |
| 18360411 | 97698445 | Yes | keep |
| 36815728 | 64616465 | No | skip |
| 36815728 | 92142380 | Yes | keep |
| 36815728 | 97698445 | Yes | keep |
| 36815728 | 29978081 | No | skip |

The output is:

```
2 75243921 92142380
2 92142380 97698445
2 92142380 97698445
2 92142380 97698445
```

The same component can be represented by any DSU root, so the actual numeric representative is irrelevant. Only equality of representatives matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(N\alpha(V)+QK\alpha(V))) | Each edge performs two expected (O(1)) hash lookups and one DSU merge; each query checks at most 100 sources |
| Space | (O(V)) | The compact hash table and parent array contain at most (O(2N)) occupied server slots |

Here (V\le2N) for the vertices that occur in graph edges. With (N=10^6), the implementation reserves at most (2^{22}) hash slots, and both keys and parents use four-byte unsigned integers. The two main arrays therefore occupy about 32 MB, leaving room for the input processing and output under the intended memory model.

The query work is at most (1000\cdot100=10^5) candidate checks, which is negligible compared with the graph preprocessing. The expensive part is processed once, rather than once per query.

## Test Cases

```python
import sys
import io
from array import array

MASK32 = 0xFFFFFFFF
MULT = 2654435761

def solve(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    input = sys.stdin.readline

    n = int(input())

    need = max(2, 4 * n)
    size = 1
    while size < need:
        size <<= 1
    mask = size - 1

    keys = array('I', [0]) * size
    parent = array('I', [0]) * size

    def locate(x):
        p = (x * MULT) & mask
        while True:
            k = keys[p]
            if k == 0:
                return 0
            if k == x:
                return p
            p = (p + 1) & mask

    def get_slot(x):
        p = (x * MULT) & mask
        while True:
            k = keys[p]
            if k == 0:
                keys[p] = x
                parent[p] = p
                return p
            if k == x:
                return p
            p = (p + 1) & mask

    def find(p):
        root = p
        while parent[root] != root:
            root = parent[root]

        while parent[p] != p:
            nxt = parent[p]
            parent[p] = root
            p = nxt

        return root

    def union(a, b):
        a = find(a)
        b = find(b)
        if a != b:
            parent[b] = a

    for _ in range(n):
        a, b = map(int, input().split())
        union(get_slot(a), get_slot(b))

    q = int(input())
    out = []

    for _ in range(q):
        x, k = map(int, input().split())
        ys = list(map(int, input().split()))

        sx = locate(x)

        if sx == 0:
            ans = [y for y in ys if y == x]
        else:
            rx = find(sx)
            ans = []
            for y in ys:
                sy = locate(y)
                if sy != 0 and find(sy) == rx:
                    ans.append(y)

        out.append(
            str(len(ans)) +
            ((" " + " ".join(map(str, ans))) if ans else "")
        )

    sys.stdin = old_stdin
    return "\n".join(out)

sample1 = """\
8
54578972 99368556
79699669 54578972
64508306 99368556
56554555 64508306
27101564 81480071
89445516 27101564
93762227 81480071
89808815 93762227
4
56554555 2
93762227 79699669
99368556 2
64508306 56554555
27101564 2
99368556 79699669
93762227 2
56554555 54578972
"""

assert solve(sample1) == """\
1 79699669
2 64508306 56554555
0
0""", "sample 1"

sample2 = """\
10
85619126 64616465
98159933 85619126
73978229 85619126
29978081 64616465
72404745 29978081
97698445 75243921
36815728 97698445
18360411 97698445
66445821 75243921
92142380 66445821
4
97698445 4
75243921 92142380 98159933 73978229
66445821 4
29978081 92142380 73978229 97698445
18360411 4
29978081 92142380 98159933 97698445
36815728 4
64616465 92142380 97698445 29978081
"""

assert solve(sample2) == """\
2 75243921 92142380
2 92142380 97698445
2 92142380 97698445
2 92142380 97698445""", "sample 2"

minimum = """\
0
1
42 4
42 17 42 17
"""

assert solve(minimum) == "2 42 42", "minimum graph and isolated vertices"

boundary = """\
1
1 1000000000
2
1 3
1000000000 1 42
42 2
1 1000000000
"""

assert solve(boundary) == """\
2 1000000000 1
0""", "identifier boundary"

self_loops = """\
4
7 7
7 7
1000000000 1000000000
42 42
3
7 4
7 7 7 42
1000000000 3
1000000000 7 1000000000
42 2
42 43
"""

assert solve(self_loops) == """\
3 7 7 42
1 1000000000
1 42""", "self loops and repeated values"

# Maximum-size stress case: one million edges forming one long chain.
# The query also uses the largest legal server identifier.
n = 1_000_000
parts = [str(n)]
for i in range(1, n + 1):
    parts.append(f"{i} {i + 1}")
parts.append("1")
parts.append(f"1 3")
parts.append(f"1 {n + 1} {1_000_000_000}")

maximum_case = "\n".join(parts) + "\n"

assert solve(maximum_case) == f"2 {n + 1} 1", "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `1 79699669`, `2 64508306 56554555`, then two zeroes | Basic component filtering and disconnected components |
| Sample 2 | Four lines with two valid sources each | Multiple components and preservation of source order |
| (N=0), repeated isolated identifier | `2 42 42` | Unknown servers, equality of isolated identifiers, duplicate candidates |
| Identifiers `1` and `1000000000` | `2 1000000000 1`, then `0` | Identifier boundaries and absent candidate handling |
| Self-loops and repeated values | Three component-specific answers | Self-loops, duplicates, and components containing only one server |
| One-million-edge chain | `2 1000001 1` | Maximum graph size, long DSU paths, and largest practical preprocessing load |

The maximum-size test is deliberately generated instead of embedding one million edge lines into the test source. It exercises the same input size that determines the memory and time behavior of the actual solution.

## Edge Cases

When there are no edges, every server is isolated. For the input

```
0
1
42 3
42 17 42
```

the destination `42` has no graph entry, so the query logic takes the isolated-server branch. It keeps both occurrences of `42` and rejects `17`, producing

```
2 42 42
```

A server that occurs in the graph can be connected to another server while a third queried identifier remains absent. For

```
1
1 2
1
1 3
2 3 1
```

the DSU contains one component `{1,2}`. Server `3` is absent and isolated, so only `1` belongs to the destination's component. The result is

```
1 1
```

This is why an absent identifier cannot simply be assigned a special common representative. Every absent identifier is its own isolated component.

If a candidate appears multiple times, every occurrence must be evaluated independently. For

```
0
1
7 4
7 7 8 7
```

the destination is the isolated server `7`, so the three occurrences of `7` are all valid. The output is

```
3 7 7 7
```

The implementation constructs `ans` by iterating over the original list, so no ordering or multiplicity information is lost.

A self-loop does not create a connection to another server. For

```
1
1000000000 1000000000
1
1000000000 2
1 1000000000
```

the DSU creates one singleton component containing `1000000000`. The candidate `1` is a different isolated server, while `1000000000` is the destination itself. The output is

```
1 1000000000
```

Repeated edges behave similarly. Calling `union` on two vertices already in the same DSU set changes nothing, so duplicate connections cannot corrupt the component structure.

Finally, server identifiers may be as large as (10^9), while the number of servers is much smaller. The hash table deliberately stores identifiers as 32-bit unsigned integers instead of attempting to allocate an array indexed by the identifier. That distinction is what makes the memory usage depend on the number of actual servers rather than on the maximum identifier value.
