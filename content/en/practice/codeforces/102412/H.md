---
title: "CF 102412H - Mex on DAG"
description: "We have a directed acyclic graph with (n) vertices and exactly (2n) edges. The edges are numbered from (0) to (2n-1), and edge (i) has value (lfloor i/2rfloor). Thus every value from (0) through (n-1) occurs on exactly two edges."
date: "2026-08-10T14:03:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "H"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 141
verified: true
draft: false
---

[CF 102412H - Mex on DAG](https://codeforces.com/problemset/problem/102412/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed acyclic graph with (n) vertices and exactly (2n) edges. The edges are numbered from (0) to (2n-1), and edge (i) has value (\lfloor i/2\rfloor). Thus every value from (0) through (n-1) occurs on exactly two edges. For a directed path, we look only at the set of edge values appearing on it and take its MEX, the smallest non-negative value that does not occur. The task is to maximize this MEX over all simple directed paths. The original statement gives (2\le n\le2000), (2n) edges, a 5 second time limit, and 256 MiB of memory.

The vertices are already topologically ordered because every edge is given as (a_i<b_i). This matters a lot. A path can contain an edge (e=(a,b)) followed by an edge (f=(c,d)) exactly when there is a directed path from (b) to (c), where (b=c) is allowed. Since the graph is acyclic, every directed path is automatically simple.

The answer is at most (n-1). A path on (n) vertices contains at most (n-1) edges, while achieving MEX (k) requires the path to contain all (k) distinct values (0,1,\ldots,k-1). The lower bound is at least (1), because either of the two edges with value (0) is itself a valid path.

A first edge case is when both edges of a value have exactly the same endpoints. For example,

```
2
1 2
1 2
1 2
1 2
```

has two edges of value (0) and two of value (1), all going from vertex (1) to vertex (2). The answer is (1), because a path can contain only one edge between these two vertices. A careless solution that treats the two edges of the same value as separate requirements could incorrectly think that both choices somehow increase the MEX.

Another edge case is when the two required values exist but their edges cannot coexist on one path. Consider

```
3
1 3
1 3
1 2
1 2
```

The first two edges have value (0), and the last two have value (1). A path can take a value (0) edge or a value (1) edge, but cannot take both, because both types leave vertex (1) and then terminate. The correct answer is (1). Checking only the numerical order of endpoints is not enough in the general problem, because (b<c) does not imply that (b) can actually reach (c).

A third edge case is when two edges share an endpoint. For example, if one edge is (1\to3) and another is (3\to5), they are compatible and can occur consecutively. The reachability relation must include the zero-length case, so a vertex must be considered reachable from itself. Forgetting this causes paths with consecutive edges to be rejected.

## Approaches

The brute-force approach is to try every choice of one edge for every value we want to put into the path. Since every value has two edges, forcing values (0,\ldots,k-1) gives (2^k) possible choices. For each choice, we can check whether the selected edges form one directed path by sorting them according to their positions in the DAG and checking consecutive reachability. This is correct because a path with MEX at least (k) must contain every value below (k), and there are only two possible edges for each such value.

The problem is the exponential number of choices. In the worst case (k=\Theta(n)), giving (2^n) choices, and even an (O(n)) or (O(n^2)) validity check leaves (O(n2^n)) or (O(n^22^n)) work. With (n=2000), this is completely impossible. The official constraint is specifically large enough to rule out enumeration of the possible paths or the possible edge choices.

The key observation is that we do not need to construct a path directly. Instead, fix a candidate answer (k) and ask whether some path contains all values (0,\ldots,k-1). For each value there are exactly two edges, so we can introduce one Boolean variable. The variable decides which of the two edges of that value is selected.

Now consider two selected edges (e=(a,b)) and (f=(c,d)). They can both belong to one path if either (b) can reach (c), meaning (e) comes before (f), or (d) can reach (a), meaning (f) comes before (e). If neither relation holds, selecting both edges is impossible. Thus every incompatible pair gives a 2-SAT clause saying that at least one of the two edges must not be selected.

This is exactly the structure exploited by the standard solution: binary search the MEX, reduce each feasibility test to 2-SAT, and solve the resulting implication graph with SCCs.

There is one more useful optimization. We do not need to test reachability separately for every pair of edges. For every vertex (v), we can precompute the set of edges whose starting vertex is reachable from (v), and the set of edges whose ending vertex can reach (v). Then, for an edge (e=(a,b)), the compatible edges are exactly the union of the first set for (b) and the second set for (a). Python's arbitrary-size integers make these sets compact bitsets, which lets the implementation represent a dense (O(n^2)) relation without storing millions of Python integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2 2^n)) | (O(n)) | Too slow |
| Optimal | (O(n^2\log n)) | (O(n^2)) bits plus SCC state | Accepted |

## Algorithm Walkthrough

1. Read all (2n) edges. Edge (2x) and edge (2x+1) are the two choices for value (x). Store their endpoints and build the DAG adjacency lists.
2. Compute reachability between vertices. Because every edge satisfies (a<b), the vertex numbering itself is a topological ordering. Process vertices from (n) down to (1). For each vertex (v), start its reachability bitset with (v) itself and OR in the reachability bitset of every outgoing neighbor.
3. For every vertex (v), compute `succ[v]`, the bitset of all edges whose starting vertex can be reached from (v). Initialize it with all edges starting exactly at (v), then process the DAG backwards and merge the corresponding `succ` sets of outgoing neighbors.
4. Similarly compute `pred[v]`, the bitset of all edges whose ending vertex can reach (v). Initialize it with all edges ending at (v), then process the DAG forwards. When processing (u\to v), everything that can end at (u) can also precede (v).
5. For an edge (e_i=(a_i,b_i)), every edge compatible with (e_i) is contained in `succ[b_i] | pred[a_i]`. The first part represents edges after (e_i), while the second represents edges before it. All remaining edges are incompatible with (e_i).
6. Remove the other edge having the same value from the incompatibility set. The two edges of one value are never simultaneously required, because the Boolean variable chooses exactly one of them.
7. Fix a candidate MEX (k). Create one Boolean variable for every value (0,\ldots,k-1). Literal (2x) means choosing edge (2x), and literal (2x+1) means choosing edge (2x+1).
8. If edge (i) and edge (j) are incompatible, add the clause (\neg i\lor\neg j). In the implication graph this becomes (i\to\neg j) and (j\to\neg i). Since the graph is stored as bitsets, these implications can be generated by swapping every set bit (j) to (j\mathbin{\hat{}}!1).
9. Run Tarjan's SCC algorithm on the implication graph. A 2-SAT instance is satisfiable exactly when no variable and its negation belong to the same SCC. This is the standard SCC characterization of 2-SAT.
10. Binary-search the largest (k) for which the 2-SAT instance is satisfiable. Feasibility is monotone: if a path contains all values (0,\ldots,k-1), it also contains all values (0,\ldots,k-2).

### Why it works

For a fixed (k), every satisfying assignment chooses exactly one edge for every value below (k). The clauses forbid precisely those pairs of chosen edges that cannot coexist on a directed path. Hence every satisfying assignment gives a collection of pairwise compatible edges. Because reachability in a DAG is transitive, pairwise compatible selected edges can be ordered into one directed path. Conversely, every path containing all required values chooses one edge of each value and never contains an incompatible pair, so its choices satisfy every clause. The 2-SAT test is thus true exactly when a path with MEX at least (k) exists. Binary search then finds the maximum possible MEX.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

def solve():
    n = int(input())
    m = 2 * n

    u = [0] * m
    v = [0] * m
    graph = [[] for _ in range(n)]

    for i in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        u[i] = a
        v[i] = b
        graph[a].append(b)

    # Vertices are already in topological order because a < b.
    # reach[x] is a bitset of vertices reachable from x, including x.
    reach = [0] * n
    for x in range(n - 1, -1, -1):
        cur = 1 << x
        for y in graph[x]:
            cur |= reach[y]
        reach[x] = cur

    # starts[x] = edges whose starting vertex is x
    # ends[x]   = edges whose ending vertex is x
    starts = [0] * n
    ends = [0] * n
    for i in range(m):
        starts[u[i]] |= 1 << i
        ends[v[i]] |= 1 << i

    # succ[x] = edges whose starting vertex can be reached from x.
    succ = starts[:]
    for x in range(n - 1, -1, -1):
        cur = succ[x]
        for y in graph[x]:
            cur |= succ[y]
        succ[x] = cur

    # pred[x] = edges whose ending vertex can reach x.
    pred = ends[:]
    for x in range(n):
        for y in graph[x]:
            pred[y] |= pred[x]

    full_edges = (1 << m) - 1

    # bad[i] contains every edge incompatible with edge i.
    bad = [0] * m

    for i in range(m):
        compatible = succ[v[i]] | pred[u[i]]

        # Edges i and i^1 have the same value and are not both selected.
        same_value = (1 << i) | (1 << (i ^ 1))
        bad[i] = (full_edges ^ compatible) & ~same_value

    # If bit j is in bad[i], the implication is i -> (j^1).
    # Swap even and odd bit positions to obtain the implication rows.
    even_mask = sum(1 << i for i in range(0, m, 2))
    odd_mask = sum(1 << i for i in range(1, m, 2))

    implication = [0] * m
    reverse_implication = [0] * m

    for i in range(m):
        b = bad[i]
        implication[i] = ((b & even_mask) << 1) | ((b & odd_mask) >> 1)

        # Incoming edges to literal x correspond to bad[x^1].
        reverse_implication[i] = bad[i ^ 1]

    def possible(k):
        vertices = 2 * k
        mask = (1 << vertices) - 1

        disc = [-1] * vertices
        low = [0] * vertices
        on_stack = bytearray(vertices)
        stack = []
        component = [-1] * vertices
        timer = 0
        comp_id = 0

        def dfs(x):
            nonlocal timer, comp_id

            disc[x] = low[x] = timer
            timer += 1
            stack.append(x)
            on_stack[x] = 1

            bits = implication[x] & mask

            while bits:
                bit = bits & -bits
                bits -= bit
                y = bit.bit_length() - 1

                if disc[y] == -1:
                    dfs(y)
                    if low[y] < low[x]:
                        low[x] = low[y]
                elif on_stack[y] and disc[y] < low[x]:
                    low[x] = disc[y]

            if low[x] == disc[x]:
                while True:
                    y = stack.pop()
                    on_stack[y] = 0
                    component[y] = comp_id
                    if y == x:
                        break
                comp_id += 1

        for x in range(vertices):
            if disc[x] == -1:
                dfs(x)

        for x in range(0, vertices, 2):
            if component[x] == component[x ^ 1]:
                return False

        return True

    lo, hi = 1, n - 1
    answer = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if possible(mid):
            answer = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation reads the (2n) edges and builds the DAG. The fact that the endpoints satisfy (a<b) means there is no need to run a separate topological sort.

The `reach` array uses Python integers as bitsets. Bit (x) is set exactly when vertex (x) is reachable. Processing vertices backwards is valid because every outgoing edge goes to a larger-numbered vertex.

The `succ` and `pred` arrays compress the pairwise path compatibility relation. For an edge (u_i\to v_i), `succ[v_i]` contains every edge that can appear after it, while `pred[u_i]` contains every edge that can appear before it. Their union is exactly the set of edges compatible with (i).

The `bad` array is the complement of that union. The two edges with the same value are explicitly removed because a satisfying assignment chooses only one of them. This also explains why the code never needs clauses saying that the two choices of one variable cannot both be selected, that restriction is already built into the meaning of a Boolean variable.

The implication graph uses the standard encoding of a clause. If selecting edge (i) and selecting edge (j) is forbidden, the clause is (\neg i\lor\neg j), giving implications (i\to\neg j) and (j\to\neg i). Since negation is represented by XOR with (1), swapping every even and odd bit in a bitset constructs the implication row without iterating over all incompatible pairs.

Tarjan's algorithm is written recursively, so the recursion limit is raised substantially. The maximum depth is bounded by the number of literals, at most (4000), which is safe after changing the Python recursion limit.

The binary search uses `n - 1` as the upper bound because a simple path in an (n)-vertex DAG has at most (n-1) edges. The answer is initialized to (1), which is always feasible because at least one of the two value-(0) edges exists and a single edge is a valid path.

## Worked Examples

The original statement does not provide conventional sample input/output pairs in the text available with the problem statement, so the first trace below uses the test instance included with the reference solution, and the second is a small constructed instance.

### Sample 1

```
8
3 6
2 7
1 3
2 3
6 7
7 8
7 8
4 6
2 7
1 5
2 5
2 8
6 8
7 8
3 5
7 8
```

The edges have values (0,0,1,1,2,2,3,3,\ldots). The path

```
1 -> 3 -> 6 -> 7 -> 8
```

can choose values (1,0,2,3), respectively. Thus its set of values contains (0,1,2,3), giving MEX (4). No path can also contain value (4), so the answer is (4).

| Binary-search state | Candidate | Feasible? | Reason |
| --- | --- | --- | --- |
| Initial | 4 | Yes | The path (1\to3\to6\to7\to8) contains values (0,1,2,3) |
| Upper half | 6 | No | Values (0,\ldots,5) cannot all be placed on one path |
| Remaining | 5 | No | The value-4 edges cannot coexist with all values (0,\ldots,3) |
| Final | 4 | Yes | Maximum feasible candidate |

The invariant is that every feasible candidate corresponds to an actual satisfying assignment of the 2-SAT instance. The path above provides a concrete assignment for (k=4), while the unsatisfiable tests for larger candidates rule out larger MEX values.

### Sample 2

```
3
1 3
1 3
1 2
1 2
```

The two value-(0) edges are (1\to3), and the two value-(1) edges are (1\to2). Any path can contain one of these edge types, but cannot contain both.

| Candidate (k) | Required values | Result |
| --- | --- | --- |
| 1 | (0) | Feasible |
| 2 | (0,1) | Infeasible |
| Answer | (1) | (1) |

For (k=2), every choice of the value-(0) edge conflicts with every choice of the value-(1) edge. The resulting 2-SAT instance has no satisfying assignment, so the binary search correctly stops at (1).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2\log n)) | Reachability and compatibility preprocessing use bitset operations; each binary-search step solves a 2-SAT instance with (O(n)) literals and (O(n^2)) possible implications |
| Space | (O(n^2)) bits plus (O(n)) arrays | Dense graph relations are stored as Python integer bitsets rather than Python integer adjacency lists |

The original limits are (n\le2000), 5 seconds, and 256 MiB. The dense relation is the main memory concern in a Python implementation, which is why the code deliberately stores it as bitsets. A conventional Python adjacency list containing every implication can consume far more memory because each stored integer is a Python object. The reference implementation is written in C++, where the same (O(n^2\log n)) method comfortably fits the intended limits; Python should be regarded as more implementation-sensitive on the original judge.

## Test Cases

The following tests include the reference sample, the small minimum-size case, an all-equal-endpoint case, a disconnected-choice case, and a maximum-size generated case.

```python
import io
import sys

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# Reference sample included with the published solution.
sample1 = """\
8
3 6
2 7
1 3
2 3
6 7
7 8
7 8
4 6
2 7
1 5
2 5
2 8
6 8
7 8
3 5
7 8
"""

assert run(sample1) == "4\n", "reference sample"

# Minimum-size graph.
sample2 = """\
2
1 2
1 2
1 2
1 2
"""

assert run(sample2) == "1\n", "minimum-size graph"

# Values 0 and 1 exist, but no path can contain both.
case3 = """\
3
1 3
1 3
1 2
1 2
"""

assert run(case3) == "1\n", "incompatible value choices"

# A single chain can contain both values.
case4 = """\
3
1 2
1 2
2 3
2 3
3 4
3 4
"""

assert run(case4) == "3\n", "three consecutive values"

# Maximum-size instance: every edge has the same endpoints.
# Every path contains only one edge, so the answer is 1.
n = 2000
lines = [str(n)]
lines.extend(["1 2000"] * (2 * n))
case5 = "\n".join(lines) + "\n"

assert run(case5) == "1\n", "maximum-size dense parallel-edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Reference 8-vertex case | `4` | Full interaction between reachability and 2-SAT |
| `n=2`, four copies of `1 2` | `1` | Minimum size and same-endpoint parallel edges |
| Two incompatible edge types from vertex 1 | `1` | Pairwise incompatibility constraints |
| Chain containing values 0, 1, and 2 | `3` | Consecutive reachability and the self-reachability boundary |
| (n=2000), all edges `1 2000` | `1` | Maximum input size and dense compatibility representation |

## Edge Cases

For the minimum-size case,

```
2
1 2
1 2
1 2
1 2
```

the path can contain only one edge because there are only two vertices. It can choose a value-(0) edge, giving MEX (1), but it cannot contain both value (0) and value (1). The compatibility preprocessing sees that no edge can follow another edge because every edge ends at vertex (2). The answer is consequently (1).

For equal parallel edges,

```
3
1 2
1 2
2 3
2 3
3 4
3 4
```

there are two choices for each of values (0,1,2), and either choice of each value can be placed consecutively on the path (1\to2\to3\to4). The selected edges therefore contain all values (0,1,2), giving MEX (3). The algorithm does not confuse the two copies of a value with two separate requirements because one Boolean variable represents both copies.

For incompatible choices,

```
3
1 3
1 3
1 2
1 2
```

the selected value-(0) edge and selected value-(1) edge always share the same starting vertex and then diverge. Neither can follow the other. Consequently every pair of choices generates a forbidden pair, making the (k=2) 2-SAT instance unsatisfiable. The algorithm returns (1).

For consecutive edges,

```
4
1 2
1 2
2 3
2 3
3 4
3 4
4 4
4 4
```

the final two lines are not valid under the original constraint (a<b), so they must not be used as an actual test. A valid boundary example is instead

```
4
1 2
1 2
2 3
2 3
3 4
3 4
1 4
1 4
```

Here values (0,1,2) can occur along (1\to2\to3\to4), while value (3) uses an edge (1\to4) that conflicts with those edges. The answer is (3). The reachability representation treats a shared endpoint as reachable from itself, so (1\to2) followed by (2\to3) is correctly accepted.

For the largest input size, (n=2000), there are (4000) edges and potentially millions of pairwise compatibility relationships. Storing each relationship as a Python list would introduce substantial object overhead. The bitset representation stores the same dense information in machine-sized chunks inside Python integers, which is the reason the implementation remains within a reasonable memory footprint.
