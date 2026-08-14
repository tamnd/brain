---
title: "CF 102388E - Stables"
description: "We have an undirected graph with up to 50 cities and up to 2500 roads. A road can connect two different cities or connect a city to itself, so loops are allowed. Starting from a city, we must follow exactly (k) roads and finish at the same city."
date: "2026-08-14T13:55:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "E"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 313
verified: false
draft: false
---

[CF 102388E - Stables](https://codeforces.com/problemset/problem/102388/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph with up to 50 cities and up to 2500 roads. A road can connect two different cities or connect a city to itself, so loops are allowed. Starting from a city, we must follow exactly (k) roads and finish at the same city. A city is valid if such a closed walk of length exactly (k) exists.

The task is to count all valid starting cities independently. Different cities may use completely different walks, and a walk is allowed to repeat both cities and roads.

The small value of (n) is the main clue. With only 50 vertices, an (O(n^3)) or even an (O(n^3 \log k)) method would be reasonable in a compiled language, while the huge value (k \le 10^9) rules out anything that processes every day directly. We need to avoid doing work proportional to (k). The fact that there are at most 2500 roads also means that graph traversals and small dynamic programs are cheap.

There are several edge cases that can fool a solution based only on parity.

First, (k=0) means that the horse makes no moves, so every city is already back at itself. For example,

```
1
1 0 0
```

has output

```
1
```

A solution that requires at least one road traversal would incorrectly return zero.

Second, an isolated vertex cannot make any positive-length walk. For example,

```
1
2 0 2
```

has output

```
0
```

There is no road at either city, so even though 2 is even, the usual "every positive even length works" argument does not apply.

Third, a loop creates a closed walk of length one. For example,

```
1
1 1 1
0 0
```

has output

```
1
```

A bipartite check that treats the graph as a simple graph and ignores loops would incorrectly classify this component as bipartite.

Fourth, being in a non-bipartite component is not by itself enough for small odd (k). Consider

```
1
3 3 1
0 1
1 2
2 0
```

The triangle is non-bipartite, but there is no one-step closed walk because there is no loop. The correct output is

```
0
```

This is why the algorithm handles small (k) exactly before using the eventual parity property.

## Approaches

The direct approach is to simulate walks by dynamic programming. For every starting city (s), keep the set of cities reachable after exactly (t) steps. Initially only (s) is reachable. For every step, follow every incident road from every currently reachable city. After (k) steps, check whether (s) itself is reachable.

This is correct because the state after (t) steps contains exactly the possible endpoints of all walks of length (t). The problem is the value of (k). In the worst case, the dynamic program performs (O(k n m)) adjacency processing when it is run for every starting city. With (k=10^9), (n=50), and (m=2500), this is on the order of (1.25 \cdot 10^{14}) graph transitions. The large (k) makes this impossible.

The key observation is that undirected graphs have a very simple long-term pattern for closed walks. Every positive even length is possible at every non-isolated vertex, because we can traverse any incident edge and immediately traverse it back. Repeating that two-step walk gives every positive even length.

Odd lengths behave differently. A connected component is bipartite exactly when it contains no odd cycle. In a bipartite component, every closed walk has even length, so no odd value of (k) can work. In a non-bipartite component, every vertex eventually has closed walks of both parities. More specifically, every vertex has an odd closed walk of length at most (2n-1). Once one odd closed walk exists, we can add any number of two-step backtracks, so every sufficiently large odd length also exists.

This gives us a clean split. If (k) is at most (2n), we simply compute the answer exactly with a small bitset dynamic program. If (k) is larger than (2n), we no longer need the exact walk structure. For even (k), every non-isolated vertex works. For odd (k), exactly the vertices belonging to non-bipartite components work.

The bitset representation makes the exact part particularly cheap. A set of reachable cities is represented by one Python integer, where bit (j) is set when city (j) is reachable. To advance one step, for every reachable city (v), we OR its adjacency bitset into the new reachable set. Since (n\le50), all of this fits inside a few machine-sized Python integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP for all (k) steps | (O(k n m)) | (O(n^2)) | Too slow |
| Exact bitset DP up to (2n), then parity/component analysis | (O(n^2 \min(k,n) + n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build both an adjacency list and an adjacency bitset for the graph. The adjacency list is used to determine connected components and bipartiteness. The bitset lets the exact dynamic program update all possible endpoints using fast integer OR operations.
2. If (k=0), return (n). The empty walk starts and ends at the same city regardless of the graph.
3. If (k\le2n), compute the answer exactly. For each city (i), the initial reachable set is just ({i}), represented by the integer (1\ll i). After one step, replace the reachable set by the union of the adjacency sets of all currently reachable cities. Repeat this exactly (k) times.

After the (t)-th iteration, the bit at position (j) is set exactly when there exists a walk of length (t) from the original city (i) to city (j). Thus the diagonal bits after (k) iterations tell us exactly which cities have a closed walk of length (k).
4. If (k>2n), run a BFS or DFS over every connected component while assigning each vertex a binary color. Along every ordinary edge, its endpoints must have opposite colors in a bipartite graph. If an edge joins two vertices with the same color, the component contains an odd cycle and is non-bipartite. A loop immediately creates such a conflict because its two endpoints are the same vertex.
5. For large even (k), count every vertex whose degree is positive. From such a vertex, choose one incident edge and traverse it back and forth. Repeating this two-step walk produces any positive even length.
6. For large odd (k), count every vertex whose component was found to be non-bipartite. A non-bipartite component contains an odd cycle. From any vertex, walk to that cycle, traverse the cycle once, and return along the same path. This gives an odd closed walk. The construction has length at most (2n-1), and because (k>2n), the difference between (k) and that odd length is a positive even number. We can fill that difference with repeated two-step backtracks.

### Why it works

For the exact part, the invariant is that after (t) iterations, `reach[i]` contains precisely the vertices reachable from (i) by a walk of exactly (t) edges. The update takes every currently reachable vertex and follows one more edge, so it neither misses a possible walk nor introduces an impossible endpoint. Consequently, bit (i) after (k) iterations is set exactly when there is a length-(k) closed walk at (i).

For large (k), consider an even length first. Any non-isolated vertex has a two-edge closed walk, obtained by traversing an incident edge in both directions. Repeating it gives every positive even length. An isolated vertex has no positive walk at all.

For odd lengths, a bipartite component cannot contain an odd closed walk because every edge changes the bipartite side, so after an odd number of edges the walk must be on the opposite side. A non-bipartite component contains an odd cycle. For a vertex (v), take a shortest path of length (d) from (v) to that cycle and let the odd cycle have length (l). The path and cycle can be chosen to meet only at the endpoint, so (d+l\le n). The resulting closed walk has length (2d+l), which is at most (d+n\le2n-1). Adding any number of two-edge backtracks gives every larger odd length. Since the algorithm only uses this argument when (k>2n), the required large odd length is always reachable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, m, k, edges):
    graph = [[] for _ in range(n)]
    adj_bits = [0] * n
    degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

        adj_bits[u] |= 1 << v
        adj_bits[v] |= 1 << u

        degree[u] += 1
        degree[v] += 1

    if k == 0:
        return n

    # Small k: compute the exact set of endpoints after k steps.
    if k <= 2 * n:
        reach = [1 << i for i in range(n)]

        for _ in range(k):
            new_reach = [0] * n

            for start in range(n):
                bits = reach[start]
                result = 0

                while bits:
                    low = bits & -bits
                    v = low.bit_length() - 1
                    result |= adj_bits[v]
                    bits -= low

                new_reach[start] = result

            reach = new_reach

        answer = 0
        for i in range(n):
            if (reach[i] >> i) & 1:
                answer += 1

        return answer

    # Large k: only the parity structure of each component matters.
    color = [-1] * n
    component = [-1] * n
    component_bad = []

    for start in range(n):
        if color[start] != -1:
            continue

        cid = len(component_bad)
        component_bad.append(False)

        color[start] = 0
        component[start] = cid
        stack = [start]

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    component[v] = cid
                    stack.append(v)
                elif color[v] == color[u]:
                    component_bad[cid] = True

    if k % 2 == 0:
        return sum(degree[i] > 0 for i in range(n))

    return sum(component_bad[component[i]] for i in range(n))

def solve():
    t = int(input())

    for _ in range(t):
        n, m, k = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]

        print(solve_case(n, m, k, edges))

if __name__ == "__main__":
    solve()
```

The first part of `solve_case` constructs two graph representations. `graph` stores the edges for the later component and bipartiteness traversal. `adj_bits[u]` stores every neighbor of (u) in one integer, so taking one more graph step becomes a sequence of integer OR operations.

The exact dynamic program starts with `1 << i` for city (i), because before taking any edges the only reachable city is (i) itself. For every reachable vertex `v`, `adj_bits[v]` contains all possible destinations after one additional step. OR-ing all those masks gives exactly the next reachable set.

The loop is limited to `k <= 2 * n`. This boundary is deliberate. We do not need to know exact walk lengths beyond (2n), because the component structure completely determines the answer there.

The bipartite traversal assigns colors `0` and `1`. A loop appears in `graph[u]` as an edge from `u` to itself, so `color[v] == color[u]` immediately marks the component as non-bipartite. Parallel edges cause no problem because repeating the same adjacency check does not change the result.

For even large (k), `degree[i] > 0` is the complete condition. For odd large (k), the component identifier maps each vertex to its bipartite status, so `component_bad[component[i]]` directly tells whether city (i) belongs to a non-bipartite component.

There is no integer overflow issue in Python. The largest bitset has only 50 relevant bits, and (k) is stored as an ordinary Python integer.

## Worked Examples

### Sample 1, first testcase

The graph is a path of length two, with city 0 in the middle.

For (k=3), we are in the exact-DP range because (3\le2n=6).

| Step | City 0 reachable | City 1 reachable | City 2 reachable |
| --- | --- | --- | --- |
| 0 | {0} | {1} | {2} |
| 1 | {1,2} | {0} | {0} |
| 2 | {0} | {1,2} | {1,2} |
| 3 | {1,2} | {0} | {0} |

No row contains its starting city after three steps, so the answer is 0.

The graph is bipartite, which also explains why odd closed walks cannot exist at all. The exact DP is still used because the algorithm must handle all small values of (k), including cases where eventual parity alone is insufficient.

### Sample 1, third testcase

The graph contains a triangle (0,1,2), plus the path (3-4-0). Here (n=5) and (k=5), so again (k\le2n) and the exact DP is used.

| Step | City 0 | City 1 | City 2 | City 3 | City 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | {0} | {1} | {2} | {3} | {4} |
| 1 | {1,2,4} | {0,2} | {0,1} | {4} | {0,3} |
| 2 | {0,2,3,4} | {0,1,4} | {0,1,2,4} | {0,3} | {1,2,4} |
| 3 | {0,1,2,3,4} | {0,1,2,3} | {0,1,2,3,4} | {4} | {0,1,2,3} |
| 4 | {0,1,2,3,4} | {0,1,2,3,4} | {0,1,2,3,4} | {0,3} | {0,1,2,4} |
| 5 | {0,1,2,3,4} | {0,1,2,3,4} | {0,1,2,3,4} | {4} | {0,1,2,3,4} |

Cities 0, 1, 2, and 4 contain themselves after five steps. City 3 does not, so the answer is 4.

The example also shows why connectivity alone is not enough. City 3 is connected to the non-bipartite triangle, yet it has no odd closed walk of length five. The exact computation handles that short-distance restriction correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2\min(k,2n)+n+m)) | Each exact DP step processes at most (n) reachable sets, each containing at most (n) vertices. Large (k) requires only one graph traversal. |
| Space | (O(n+m)) | The adjacency list, bitsets, colors, component IDs, and DP arrays all use at most (O(n+m)) space. |

With (n\le50), the exact phase performs at most (2n=100) iterations. Even in a dense graph, each iteration handles only 50 small bitsets, so the amount of work is tiny. The large-(k) phase is just a linear graph traversal. The solution comfortably fits the 3 second and 256 MB limits.

## Test Cases

The following test harness reproduces the algorithm through `solve_case` and checks the samples together with several boundary cases.

```python
import io

def solve_case(n, m, k, edges):
    graph = [[] for _ in range(n)]
    adj_bits = [0] * n
    degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        adj_bits[u] |= 1 << v
        adj_bits[v] |= 1 << u
        degree[u] += 1
        degree[v] += 1

    if k == 0:
        return n

    if k <= 2 * n:
        reach = [1 << i for i in range(n)]

        for _ in range(k):
            new_reach = [0] * n

            for start in range(n):
                bits = reach[start]
                result = 0

                while bits:
                    low = bits & -bits
                    v = low.bit_length() - 1
                    result |= adj_bits[v]
                    bits -= low

                new_reach[start] = result

            reach = new_reach

        return sum((reach[i] >> i) & 1 for i in range(n))

    color = [-1] * n
    component = [-1] * n
    component_bad = []

    for start in range(n):
        if color[start] != -1:
            continue

        cid = len(component_bad)
        component_bad.append(False)

        color[start] = 0
        component[start] = cid
        stack = [start]

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    component[v] = cid
                    stack.append(v)
                elif color[v] == color[u]:
                    component_bad[cid] = True

    if k % 2 == 0:
        return sum(degree[i] > 0 for i in range(n))

    return sum(component_bad[component[i]] for i in range(n))

def run(inp):
    data = list(map(int, inp.split()))
    p = 0

    t = data[p]
    p += 1
    out = []

    for _ in range(t):
        n, m, k = data[p], data[p + 1], data[p + 2]
        p += 3

        edges = []
        for _ in range(m):
            u, v = data[p], data[p + 1]
            p += 2
            edges.append((u, v))

        out.append(str(solve_case(n, m, k, edges)))

    return "\n".join(out) + "\n"

# Provided sample.
sample = """\
3
3 2 3
0 1
0 2
3 2 4
0 1
0 2
5 5 5
0 1
1 2
2 0
3 4
4 0
"""
assert run(sample) == "0\n3\n4\n", "sample"

# Minimum-size graph, no edges, k = 0.
assert run("""\
1
1 0 0
""") == "1\n", "k = 0"

# One vertex with several loops, all endpoints equal.
# Every positive k is possible.
assert run("""\
1
1 5 1000000000
0 0
0 0
0 0
0 0
0 0
""") == "1\n", "all-equal loop edges"

# Boundary between the exact and large-k phases.
# A single edge is bipartite, so even lengths work and odd lengths do not.
assert run("""\
4
2 1 4
0 1
2 1 5
0 1
3 2 6
0 1
1 2
3 2 7
0 1
1 2
""") == "2\n0\n3\n0\n", "parity boundary"

# Large odd k in a non-bipartite component.
# Triangle plus a leaf. Every vertex belongs to the same non-bipartite component.
assert run("""\
1
4 4 1000000001
0 1
1 2
2 0
2 3
""") == "4\n", "large odd non-bipartite"

# Maximum-size graph: complete graph on 50 vertices.
# There are 50^2 = 2500 roads when loops are included.
# Every vertex has a loop, so every positive k works.
n = 50
edges = [(i, j) for i in range(n) for j in range(n)]
max_input = "1\n50 2500 1000000000\n"
max_input += "\n".join(f"{u} {v}" for u, v in edges) + "\n"

assert run(max_input) == "50\n", "maximum-size dense graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0 0` | `1` | Empty walk and minimum graph size |
| `1 / 1 5 1000000000 / 0 0 ...` | `1` | Loops and arbitrarily large odd lengths |
| Single-edge and path cases with (k=4,5,6,7) | `2,0,3,0` | Even versus odd closed walks and the small/large boundary |
| Triangle with a leaf and huge odd (k) | `4` | Non-bipartite component handling for large odd (k) |
| Complete graph on 50 vertices with 2500 roads | `50` | Maximum (n), maximum (m), and dense adjacency |

## Edge Cases

For (k=0), consider

```
1
1 0 0
```

The algorithm returns immediately with `n`, which is 1. No adjacency information is needed because the zero-length walk does not require a road. This avoids the common mistake of requiring the starting city to have positive degree.

For an isolated vertex with positive even (k), consider

```
1
2 0 2
```

The large-(k) shortcut is not used because (2\le2n), so the exact DP starts with `{0}` and `{1}`. After one step both sets become empty because there are no incident edges, and they remain empty. Neither diagonal bit is present, giving 0. If the same case had a much larger even (k), the large-(k) branch would explicitly check `degree[i] > 0`, preventing an isolated city from being accepted.

For a loop, consider

```
1
1 1 1
0 0
```

The exact DP starts with bit 0 set. After one step it ORs the adjacency mask of vertex 0, which contains bit 0 because of the loop. The diagonal bit remains set, so the answer is 1. In the large-(k) branch, the same loop makes the bipartite traversal encounter an edge whose endpoints have the same color, marking the component non-bipartite.

For a non-bipartite graph with a small odd (k), consider the triangle

```
1
3 3 1
0 1
1 2
2 0
```

The graph contains an odd cycle, but there is no loop. With (k=1), no vertex can return to itself in one edge. Since (1\le2n), the exact DP is used and correctly returns 0. This is the reason the large-(k) parity classification cannot simply be applied for every odd (k).

Finally, consider a bipartite graph with a very large odd (k):

```
1
3 2 1000000001
0 1
1 2
```

Here (k>2n), so the algorithm runs the bipartite check instead of iterating a billion times. The component is bipartite, so `component_bad` is false. Since (k) is odd, no city is counted and the answer is 0. The result follows from the fact that every closed walk in a bipartite graph has even length.
