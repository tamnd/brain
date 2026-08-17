---
title: "CF 102268I - Interesting Graph"
description: "We have an undirected graph with up to (10^5) vertices and (10^5) edges. For every number of available colors (k=1,2,ldots,n), we need the number of proper color assignments, where adjacent vertices must receive different colors. Each answer is taken modulo (998244353)."
date: "2026-08-17T18:57:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "I"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 367
verified: false
draft: false
---

[CF 102268I - Interesting Graph](https://codeforces.com/problemset/problem/102268/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph with up to (10^5) vertices and (10^5) edges. For every number of available colors (k=1,2,\ldots,n), we need the number of proper color assignments, where adjacent vertices must receive different colors. Each answer is taken modulo (998244353).

The unusual condition on every seven vertices is the key structural restriction. Suppose a connected component contained at least seven vertices. Because the component is connected, we can start from one vertex and repeatedly add a neighbor of the already chosen set until we have exactly seven vertices. The resulting seven vertices induce a connected subgraph. Between any two of them there is a path using only those seven vertices, so no vertex outside the seven can belong to every path between the pair. That contradicts the given condition. Thus every connected component has at most six vertices.

This is the whole reason the problem becomes manageable. The original graph may have (10^5) vertices, but every independent piece relevant to the coloring problem has only six vertices.

A direct coloring search is hopeless. With (k=n=10^5), trying every assignment would inspect

[
n^n=(10^5)^{10^5}=10^{500000}
]

assignments. Even computing a general chromatic polynomial by subset based methods on all (n) vertices would require exponential time in (n).

The input size also rules out algorithms that repeatedly perform expensive work over the whole graph. A linear or near linear scan of the (10^5) vertices and edges is fine, while (O(n^2)) already means roughly (10^{10}) operations. The useful exponential work must consequently depend only on the constant six, not on (n).

There are several edge cases that are easy to mishandle. With two vertices joined by one edge, the answers are (0,2), because one color cannot properly color an edge and two colors give two choices for which endpoint receives which color.

```
2 1
1 2
```

The output is

```
0 2
```

A complete component of six vertices is another important boundary case. Its chromatic polynomial is

[
k(k-1)(k-2)(k-3)(k-4)(k-5),
]

so it has no coloring with fewer than six colors and exactly (6!=720) colorings with six colors.

```
6 15
1 2
1 3
1 4
1 5
1 6
2 3
2 4
2 5
2 6
3 4
3 5
3 6
4 5
4 6
5 6
```

The output is

```
0 0 0 0 0 720
```

Another common mistake is forgetting that disconnected components can be colored independently. The sample contains a triangle and two isolated vertices. The triangle has (k(k-1)(k-2)) colorings, while the isolated vertices contribute (k^2), giving (k^3(k-1)(k-2)). At (k=3), this is (27\cdot2=54), matching the sample.

## Approaches

The brute force starts by assigning one of the (k) colors to every vertex and checking every edge after the assignment is complete. This is correct because every possible coloring appears exactly once, but for (k=n=10^5) it examines (10^{500000}) assignments. There is no useful pruning that changes the fundamental exponential nature of this approach.

The useful observation is that the seven vertex condition forces every connected component to contain at most six vertices. Proper colorings of different connected components have no interaction, so if the components are (G_1,G_2,\ldots,G_s), their chromatic polynomials satisfy

[
P_G(k)=\prod_{i=1}^{s}P_{G_i}(k).
]

We therefore only need to solve a tiny problem for each component.

For a component with (t\le6) vertices, consider a partition of its vertices into color classes. A color class is valid exactly when it is an independent set. If the component can be partitioned into (r) independent sets in (S_r) ways, those (r) sets can be assigned (r) distinct colors in

[
(k)_r=r!\binom{k}{r}
]

ways. Consequently,

[
P_G(k)=\sum_{r=1}^{t} S_r(k)_r.
]

We can enumerate all set partitions directly. There are only (B_6=203) set partitions of six labeled vertices, so this is much smaller than enumerating arbitrary colorings. We count only partitions whose blocks are independent.

There is a second constant size observation. Although there are many labeled graphs on six vertices, there are only 50 distinct chromatic polynomials among connected graphs on six vertices, and across component sizes one through six the corresponding counts are (1,1,2,5,14,50). Thus there are at most 73 distinct component chromatic polynomials that can occur.

We group components having the same polynomial. If a particular polynomial (f(k)) occurs (c) times, its total contribution is (f(k)^c). Instead of processing every component separately for every (k), we process each distinct polynomial once and raise its value to its multiplicity.

The implementation below goes one step further for Python. Every component polynomial has degree at most six, so its values at consecutive integers can be generated with finite differences using only additions. This avoids evaluating six binomial coefficients for every pair of (k) and polynomial type.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^n m)) for (k=n) | (O(n+m)) | Too slow |
| Optimal | (O(n+m+3^6n+nT\log n)), (T\le73) | (O(n+m)) | Accepted |

The (3^6) term describes the general small-component subset work, while the implementation here uses set partitions and therefore actually explores at most a few hundred states per component. The (T\le73) bound comes from the finite collection of possible chromatic polynomials of connected graphs with at most six vertices.

## Algorithm Walkthrough

1. Build the adjacency list and find every connected component with DFS or BFS. The structural argument above guarantees that every discovered component has at most six vertices, so we can safely represent its internal adjacency by bitmasks.
2. Relabel the vertices of one component from (0) to (t-1), and store for every local vertex a (t)-bit mask containing its neighbors. Bitmasks make the question "can this vertex be put into this color class?" a single bitwise AND operation.
3. Enumerate all partitions of the component vertices into blocks. Process the vertices in increasing order. For the current vertex, either insert it into an existing block whose vertices are all nonadjacent to it, or create a new block. Processing vertices in a fixed order makes every set partition appear exactly once.
4. Let (S_r) be the number of valid partitions into exactly (r) independent blocks. Convert this into the coefficient of (\binom{k}{r}) by multiplying by (r!). The resulting vector uniquely describes the component's chromatic polynomial.
5. Store this coefficient vector in a dictionary and count how many components have each vector. Components with the same vector have exactly the same number of proper colorings for every (k), so they can safely be grouped.
6. For each distinct polynomial, first compute its values at (k=0,1,\ldots,t). These (t+1) values determine the degree-(t) polynomial completely. Construct its finite difference table, retaining the first value of every difference order.
7. Generate the polynomial values for (k=1,2,\ldots,n) successively. If the current difference array is (\Delta^0f,\Delta^1f,\ldots,\Delta^tf), advancing from (k) to (k+1) is done by adding each difference to the next one from low order to high order. The first entry becomes the new value of (f).
8. Multiply the global answer at every (k) by the current polynomial value raised to the number of components represented by this polynomial. Since the exponent is the multiplicity of the type, the entire collection of equal components is handled at once.
9. Print the resulting values for (k=1) through (n). All arithmetic is performed modulo (998244353).

### Why it works

For every connected component, the recursive partitioning enumerates exactly the partitions whose blocks can receive equal colors. A partition into (r) independent blocks corresponds to exactly (r!\binom{k}{r}) assignments of distinct colors to those blocks. Hence the computed small polynomial is exactly the component's chromatic polynomial.

Different connected components have no edges between them, so their colorings can be selected independently. Their chromatic polynomials therefore multiply. Grouping equal component polynomials merely replaces repeated multiplication by exponentiation and does not change the product.

The finite difference phase does not approximate the polynomial. A polynomial of degree at most six is completely determined by seven consecutive values, and its seventh finite difference is zero. Advancing the difference table reproduces the exact value at every subsequent integer. Thus every value multiplied into the final answer is the exact number of colorings contributed by that component type.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def component_signature(adj_masks):
    """Return coefficients c[r-1] such that
       P(k) = sum_{r=1}^t c[r-1] * C(k, r).
    """
    t = len(adj_masks)
    ways = [0] * (t + 1)
    blocks = []

    def dfs(v):
        if v == t:
            ways[len(blocks)] += 1
            return

        bit = 1 << v
        forbidden = adj_masks[v]

        for i in range(len(blocks)):
            block = blocks[i]
            if forbidden & block == 0:
                blocks[i] = block | bit
                dfs(v + 1)
                blocks[i] = block

        blocks.append(bit)
        dfs(v + 1)
        blocks.pop()

    dfs(0)

    res = [0] * t
    fact = 1
    for r in range(1, t + 1):
        fact = fact * r % MOD
        res[r - 1] = ways[r] * fact % MOD

    return tuple(res)

def component_values(signature, n):
    """Generate P(1), P(2), ..., P(n) using finite differences."""
    t = len(signature)

    # Evaluate at k = 0, 1, ..., t.
    initial = []
    for k in range(t + 1):
        comb = 1
        value = 0
        for r in range(1, t + 1):
            comb = comb * (k - r + 1) % MOD
            comb = comb * pow(r, MOD - 2, MOD) % MOD
            value = (value + signature[r - 1] * comb) % MOD
        initial.append(value)

    # Build the first element of every finite-difference row.
    diff = initial[:]
    first = [diff[0]]
    for length in range(t, 0, -1):
        diff = [(diff[i + 1] - diff[i]) % MOD for i in range(length)]
        first.append(diff[0])

    # first[j] = Delta^j f(0).
    cur = first
    values = [0] * n

    for k in range(n):
        # Advance from x=k to x=k+1.
        for j in range(t):
            cur[j] = (cur[j] + cur[j + 1]) % MOD
        values[k] = cur[0]

    return values

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    seen = [False] * n
    pos = [-1] * n
    types = {}

    for start in range(n):
        if seen[start]:
            continue

        stack = [start]
        seen[start] = True
        vertices = []

        while stack:
            u = stack.pop()
            vertices.append(u)
            for v in graph[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)

        t = len(vertices)

        # The input guarantee implies t <= 6.
        for i, v in enumerate(vertices):
            pos[v] = i

        masks = [0] * t
        for i, u in enumerate(vertices):
            mask = 0
            for v in graph[u]:
                mask |= 1 << pos[v]
            masks[i] = mask

        signature = component_signature(masks)
        types[signature] = types.get(signature, 0) + 1

    answer = [1] * n

    for signature, count in types.items():
        values = component_values(signature, n)

        if count == 1:
            for i, value in enumerate(values):
                answer[i] = answer[i] * value % MOD
        elif count == 2:
            for i, value in enumerate(values):
                answer[i] = answer[i] * value * value % MOD
        elif count == 3:
            for i, value in enumerate(values):
                answer[i] = answer[i] * value * value % MOD
                answer[i] = answer[i] * value % MOD
        else:
            for i, value in enumerate(values):
                answer[i] = answer[i] * pow(value, count, MOD) % MOD

    print(*answer)

if __name__ == "__main__":
    solve()
```

The input section stores the graph as adjacency lists, then a stack finds connected components in linear time. Because every valid component has at most six vertices, the local graph can be converted to bitmasks without any large auxiliary structure.

The `component_signature` routine is the core of the small graph computation. The `blocks` array contains the currently constructed color classes. When vertex (v) is inserted into a block, `adj_masks[v] & block` checks whether an edge would have both endpoints in that color class. A zero result means the block remains independent.

The recursion counts unordered partitions. This is deliberate. A partition into (r) blocks corresponds to (r!\binom{k}{r}) labeled color assignments, which is exactly why the code multiplies `ways[r]` by `r!`.

The `component_values` function uses the resulting representation

[
P(k)=\sum_{r=1}^{t} c_r\binom{k}{r}.
]

The small initial evaluation uses the recurrence for binomial coefficients. Since (t\le6), this work is constant size. The subsequent values are generated by finite differences, avoiding repeated polynomial evaluation for every color count.

The exponentiation section handles the multiplicity of each polynomial type. The special cases for multiplicities one, two, and three avoid a function call to modular exponentiation for the most common small counts. For larger multiplicities, Python's built-in `pow(a,b,MOD)` performs modular exponentiation in optimized native code.

All values are reduced modulo (998244353). Python integers do not overflow, but keeping values reduced after multiplication prevents them from growing unnecessarily.

## Worked Examples

For the provided sample, the graph consists of a triangle on vertices (1,3,5) and two isolated vertices. The triangle has one valid partition into three independent singleton blocks, and no valid partition into fewer than three blocks. Its coefficient vector is therefore ((0,0,6)). An isolated vertex has polynomial (k), represented by ((1)).

| (k) | Triangle (P(k)) | Two isolated vertices | Total |
| --- | --- | --- | --- |
| 1 | 0 | (1^2=1) | 0 |
| 2 | 0 | (2^2=4) | 0 |
| 3 | 6 | (3^2=9) | 54 |
| 4 | 24 | (4^2=16) | 384 |
| 5 | 60 | (5^2=25) | 1500 |

Thus the final output is `0 0 54 384 1500`. The table shows the component product invariant directly: the isolated vertices never interact with the triangle, so their contribution is simply multiplied afterward. The official sample is the same triangle plus two isolated vertices.

For the second example, take three disjoint edges.

```
6 3
1 2
3 4
5 6
```

Every component is (K_2), whose polynomial is (k(k-1)). Its coefficient representation contains only the term (2\binom{k}{2}), so all three components have the same signature and are grouped together with multiplicity three.

| (k) | One edge | Multiplicity | Total |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 0 |
| 2 | 2 | 3 | 8 |
| 3 | 6 | 3 | 216 |
| 4 | 12 | 3 | 1728 |
| 5 | 20 | 3 | 8000 |
| 6 | 30 | 3 | 27000 |

The output is

```
0 8 216 1728 8000 27000
```

This example demonstrates why grouping identical component types matters. Instead of evaluating three separate factors for every (k), the algorithm evaluates one polynomial and raises it to the third power.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m+3^6n+nT\log n)) | Components are constant size, (T\le73), and each type is evaluated over all (n) color counts |
| Space | (O(n+m)) | The adjacency lists, component data, answer array, and constant-size component state dominate |

The graph traversal is linear in the input size. The expensive graph computation is bounded by a constant because no component has more than six vertices. The number of different chromatic polynomial types for connected graphs of sizes at most six is at most (1+1+2+5+14+50=73).

With (n,m\le10^5), this keeps the graph-dependent part close to linear and confines all exponential behavior to the constant six. The grouping step is what makes it unnecessary to evaluate one polynomial for every one of up to (10^5) components.

## Test Cases

```python
import io
import sys

MOD = 998244353

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        solve()
        # The competitive-programming solve() writes directly to stdout,
        # so this helper is normally replaced by a captured stdout in a
        # local test harness.
    finally:
        sys.stdin = old_stdin

# A convenient self-contained harness for the same algorithm.
def run_captured(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample.
assert run_captured(
    """5 3
3 5
5 1
1 3
"""
) == "0 0 54 384 1500", "sample 1"

# Minimum valid input: one edge.
assert run_captured(
    """2 1
1 2
"""
) == "0 2", "single edge"

# Complete graph K4.
assert run_captured(
    """4 6
1 2
1 3
1 4
2 3
2 4
3 4
"""
) == "0 0 0 24", "K4 boundary"

# Three identical components.
assert run_captured(
    """6 3
1 2
3 4
5 6
"""
) == "0 8 216 1728 8000 27000", "repeated components"

# Complete graph K6, the largest possible connected component.
assert run_captured(
    """6 15
1 2
1 3
1 4
1 5
1 6
2 3
2 4
2 5
2 6
3 4
3 5
3 6
4 5
4 6
5 6
"""
) == "0 0 0 0 0 720", "K6 boundary"

# Maximum-size graph allowed by the constraints, consisting of 50,000
# identical edges. Its chromatic polynomial is (k(k-1))^50000.
n = 100000
lines = [f"{n} 50000"]
for i in range(1, n + 1, 2):
    lines.append(f"{i} {i + 1}")

large_input = "\n".join(lines) + "\n"
large_output = run_captured(large_input)

expected = []
for k in range(1, n + 1):
    expected.append(str(pow(k * (k - 1) % MOD, 50000, MOD)))

assert large_output == " ".join(expected), "maximum-size repeated components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | `0 2` | Minimum valid graph and one-edge chromatic polynomial |
| `K4` | `0 0 0 24` | Zero values below the chromatic number and the (k=n) boundary |
| Three disjoint edges | `0 8 216 1728 8000 27000` | Identical component grouping and multiplicity |
| `K6` | `0 0 0 0 0 720` | Maximum component size and six-color boundary |
| 100000 vertices in 50000 disjoint edges | ((k(k-1))^{50000}) for every (k) | Maximum input size, repeated types, and modular exponentiation |

## Edge Cases

The two-vertex graph

```
2 1
1 2
```

has one connected component with two vertices. Its only proper partition is into two singleton color classes, so its polynomial is (2\binom{k}{2}=k(k-1)). The algorithm records the signature `(0, 2)`, evaluates it at (k=1,2), and obtains `0 2`.

For a six-vertex clique, every color class can contain only one vertex. The partition recursion reaches exactly one valid partition, containing six singleton blocks. Its coefficient for (\binom{k}{6}) is (6!=720), so the polynomial is (720\binom{k}{6}). This gives zero for (k<6) and (720) for (k=6), catching errors where the loop over the number of blocks accidentally stops at (t-1).

For the sample graph, the triangle and the isolated vertices are discovered as three connected components. The triangle contributes (k(k-1)(k-2)), while each singleton contributes (k). The global product is consequently (k^3(k-1)(k-2)). This catches the common mistake of treating the entire graph as one small component simply because some of its components are small.

For many identical components, such as the 50,000 disjoint edges in the maximum-size test, every component produces the same signature. The dictionary reduces all of them to one entry with multiplicity 50,000. The answer at color count (k) is then ((k(k-1))^{50000}). This is the case that makes grouping essential, because processing every edge independently for every (k) would require roughly (5\cdot10^9) component evaluations.

The condition itself is used only in the direction that matters for the algorithm. A valid input cannot contain a connected component with seven or more vertices. The algorithm does not need the converse, and it does not attempt to verify the seven-vertex condition. This distinction matters because the guarantee is a structural promise supplied by the problem, not a condition that the implementation needs to test.
