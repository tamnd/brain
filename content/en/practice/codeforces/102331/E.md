---
title: "CF 102331E - Easy Win"
description: "For every inserted edge, we know its two endpoints, the number of stones on it, and a positive value representing how much we earn if that edge is included in our chosen graph."
date: "2026-08-13T03:37:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "E"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 226
verified: true
draft: false
---

[CF 102331E - Easy Win](https://codeforces.com/problemset/problem/102331/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

For every inserted edge, we know its two endpoints, the number of stones on it, and a positive value representing how much we earn if that edge is included in our chosen graph. After each insertion, we want the maximum total value of a subset of the available edges that forms a good graph.

The game-theoretic part is the first obstacle. Suppose we choose some edges that form edge-disjoint cycles. In an undirected graph, such a set of edges is exactly an Eulerian subgraph: every vertex has even degree. Nim is losing for the first player exactly when the XOR of all chosen pile sizes is zero. Thus LHiC wins precisely when there exists a nonempty edge subset whose vertex degrees are all even and whose pile sizes XOR to zero.

That condition can be written as linear algebra over the field with two elements. Represent an edge ((u,v)) by a binary vector having ones in positions (u) and (v). Add 60 more coordinates, one for each bit of its pile size (a). The resulting vector for edge (i) is

[
x_i = e_{u_i} \oplus e_{v_i} \oplus (a_i\text{ in the last 60 coordinates}).
]

For a subset of edges, XORing their vectors gives zero exactly when every vertex occurs an even number of times and every bit of the total pile XOR is zero. Consequently, a graph is good exactly when the vectors of all its selected edges are linearly independent over (\mathbb F_2). This reduction is the central observation behind the solution. The same linear-basis formulation is also the one used in published solutions of this problem.

So the original problem becomes an online maximum-weight independent-set problem for binary vectors. After every insertion, we need the maximum total weight of an independent subset of all vectors seen so far.

There are at most (n+60\le124) coordinates. This small dimension is the reason a linear-basis solution is possible. The number of edges, however, can be (200000), so rebuilding the basis from all previous edges after every query would be far too expensive. A quadratic or exponential algorithm in the number of edges is completely ruled out.

There are several edge cases that a direct implementation can mishandle. The first is a graph with no cycles. For example,

```
3 2
1 2 0 5
2 3 0 7
```

The graph is always a forest, so every available edge can be selected. The correct output is

```
5
12
```

A solution that insists on constructing a cycle before accepting an edge would incorrectly discard these edges. The definition of a good graph is about preventing a winning cyclic subset, so an acyclic graph is automatically good.

The second case is a cycle whose pile XOR is zero. Consider

```
3 3
1 2 0 1
2 3 0 2
3 1 0 10
```

After the third edge, selecting all three edges creates a cycle and the Nim XOR is (0). Hence the three-edge graph is not good, and the best good graph has weight (10+2=12). A solution that checks only whether the selected edges contain a cycle would incorrectly reject every cyclic graph, while a solution that checks only ordinary graph independence would miss the Nim condition.

The third case is parallel edges. Consider

```
2 2
1 2 0 5
1 2 0 9
```

The two edge vectors are equal, so they are linearly dependent. The best good graph contains only the second edge, giving

```
5
9
```

A careless implementation that treats each pair of endpoints as a single possible edge would fail on this case.

Finally, the pile value can be exactly (2^{60}-1). For example,

```
2 2
1 2 1152921504606846975 3
1 2 1152921504606846975 10
```

The vectors are equal, so the answers are

```
3
10
```

The stone value must be represented with all 60 bits, including bit 59. Using a signed 32-bit or 64-bit representation without care would lose information.

## Approaches

The brute-force approach starts from the characterization of a good graph. For each query, we could enumerate every subset of the edges seen so far, test whether its vectors are linearly independent, and keep the maximum total weight. This is correct because linear independence is exactly the definition of a good selected graph after the reduction above. With (i) available edges, however, there are (2^i) subsets, and testing one subset by Gaussian elimination costs (O(i(n+60))). At the final query the worst-case work is

[
\Theta(2^q q(n+60)),
]

which is already hopeless for even a few dozen edges, let alone (q=200000).

If all queries were known in advance and we only needed the answer for the final set, the standard weighted-matroid greedy algorithm would solve the problem. Sort all edges by decreasing weight and insert an edge whenever its vector is independent of the already selected vectors. Linear independence forms a matroid, so this produces a maximum-weight independent set. The difficulty is that queries ask for every prefix, while the weights arrive in arbitrary order. We cannot sort the current prefix again after every insertion.

The key observation is that the dimension is tiny. A selected independent set contains at most (n+60\le124) edges, regardless of how many edges have been inserted. When a new vector is dependent on the current basis, it creates one circuit. The new edge can improve the optimal basis only by replacing the minimum-weight selected edge in that circuit. This is the weighted basis-exchange property behind the online solution. The published solution stores, for every basis vector, which original selected vectors are XORed to obtain it, then uses the representation of a dependent incoming vector to find exactly the cheapest edge that can be exchanged.

The representation is what makes the online part manageable. Suppose the current selected edges are indexed from (0) to (r-1). Alongside every Gaussian basis vector we store a bitmask over these (r) selected edges. The mask tells us which selected original vectors XOR to the current basis vector. When a new vector is reduced to zero, its accumulated mask describes the unique circuit formed with the current basis. We find the smallest weight among the selected edges appearing in that mask. If the new edge is heavier, we replace that edge and update every basis representation containing it. Since there are at most 124 basis vectors, every query takes only (O(n+60)) such operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(2^q q(n+60))) | (O(q)) | Too slow |
| Optimal | (O(q(n+60))) | (O((n+60)^2)) bits | Accepted |

## Algorithm Walkthrough

1. Give every graph vertex one binary coordinate and give every bit of every pile value one additional coordinate. For an edge ((u,v,a,w)), construct the integer bitmask

[
x=(1\ll u);|;(1\ll v);|;(a\ll n).
]

The first (n) bits encode vertex parity. The last 60 bits encode the Nim XOR.

1. Maintain a Gaussian XOR basis indexed by the highest set bit. For each basis position, store both the actual vector and a representation mask. The vector is the XOR of the original selected edge vectors described by that representation mask.

The representation mask is necessary because the vector stored in a Gaussian basis is usually not one original edge anymore. We need to know which original edges participate in a dependency when a new edge is inserted.

1. Give every selected edge a permanent slot from (0) to (r-1), where (r) is the current rank. Store its weight in `weights[slot]`. A representation mask uses these slots as its bits.
2. When a new edge arrives, initialize its representation with one bit corresponding to a new temporary slot. Then perform ordinary Gaussian elimination from the highest coordinate to the lowest. Whenever the current vector has the current pivot bit and that pivot already exists, XOR the stored basis vector into the current vector and also XOR its representation mask into the current representation.

Both operations must be performed together because they describe the same linear combination.

1. If elimination reaches an unused pivot, the new edge is independent. Add the current vector as the new basis vector, assign it a new selected-edge slot, add its weight to the answer, and store the corresponding one-bit representation.

No exchange is necessary because increasing the rank always improves the objective, and all weights are positive.

1. If elimination reduces the new vector to zero, the new edge is dependent on the current selected basis. The accumulated representation mask now describes a nonempty circuit containing the new edge and some selected edges.

Find the selected edge of minimum weight among the set bits of this representation. Call its slot `f`.

1. If the new edge has weight no larger than `weights[f]`, discard it. Replacing `f` by the new edge would not increase the answer, and keeping the existing edge preserves a maximum-weight basis.
2. If the new edge is heavier, replace slot `f` by the new edge and add `new_weight - weights[f]` to the answer.

The basis vectors themselves do not need to change. Their representations do need to change. The representation mask of the new edge is exactly the dependency mask found during elimination. Since it contains the old edge `f`, XORing this mask into every basis representation containing `f` removes the old edge and replaces it with the new edge while preserving the represented vector.

1. Print the maintained total weight after every insertion.

### Why it works

The augmented vector of an edge records exactly the two conditions that matter for a winning cyclic subset: even degree at every graph vertex and zero Nim XOR. Thus a nonempty subset of selected edges on which LHiC can win exists exactly when the corresponding vectors are linearly dependent. A good graph is consequently exactly a linearly independent set of these vectors.

For the current prefix, the selected edges maintained by the algorithm are independent. If a new vector is independent, adding it increases the rank and is always beneficial because its weight is positive. If it is dependent, its representation gives the unique circuit created by adding it to the current basis. The matroid exchange property says that replacing any minimum-weight edge of this circuit by the new edge preserves independence. Choosing the minimum-weight one gives the largest possible improvement from this new edge.

The representation masks maintain this circuit information even though Gaussian elimination transforms the stored basis vectors. After an exchange, XORing the dependency mask into every affected representation changes the identity of the selected edge while leaving every represented vector unchanged. Hence the stored basis continues to span exactly the selected edge vectors, and the selected set remains a maximum-weight independent set after every query.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    D = n + 60

    # basis[p] is a vector whose highest set bit is p.
    # rep[p] tells which selected original edges XOR to basis[p].
    basis = [0] * D
    rep = [0] * D

    # weights[k] is the weight of the selected edge occupying slot k.
    weights = []

    rank = 0
    answer = 0

    def add_vector(v, w):
        nonlocal rank, answer

        # Temporary representation for the new edge.
        d = 1 << rank

        # Gaussian elimination.
        for p in range(D - 1, -1, -1):
            if not (v >> p) & 1:
                continue

            if basis[p] == 0:
                basis[p] = v
                rep[p] = d
                weights.append(w)
                rank += 1
                answer += w
                return

            v ^= basis[p]
            d ^= rep[p]

        # v == 0, so the new edge is dependent.
        # d describes the circuit in terms of selected edges.
        min_slot = -1
        min_weight = 10**30

        x = d
        while x:
            low = x & -x
            slot = low.bit_length() - 1

            if weights[slot] < min_weight:
                min_weight = weights[slot]
                min_slot = slot

            x ^= low

        # Keeping the old minimum-weight edge is at least as good.
        if w <= min_weight:
            return

        # Replace the minimum-weight edge by the new edge.
        answer += w - min_weight
        weights[min_slot] = w

        bit = 1 << min_slot

        # Every basis representation containing the old edge must
        # exchange it for the new edge. XOR with d performs exactly
        # that substitution.
        for p in range(D):
            if rep[p] & bit:
                rep[p] ^= d

    out = []

    for _ in range(q):
        u, v, a, w = map(int, input().split())
        u -= 1
        v -= 1

        vector = (1 << u) | (1 << v) | (a << n)

        add_vector(vector, w)
        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of `solve` fixes the vector dimension at `n + 60`. The vertex coordinates occupy positions `0` through `n - 1`, while the pile bits begin at position `n`. Shifting `a` by `n` places all 60 pile bits in the correct independent coordinate block.

`basis[p]` is the Gaussian basis vector whose highest set bit is `p`. This is the standard XOR-basis representation, so an insertion needs at most `D` elimination steps.

The subtle part is `rep[p]`. It is not a numerical value in the graph. It is a bitset whose bit `k` means that selected edge slot `k` participates in the XOR expression for `basis[p]`. Whenever a basis vector is XORed into the current vector, its representation must be XORed as well.

When a new vector is independent, `d` is a single bit because the new basis vector is represented only by the newly inserted edge. The edge gets a new slot, and the answer increases by its weight.

When `v` becomes zero, `d` is the dependency relation. The loop using `low = x & -x` extracts its set bits efficiently without scanning all possible edge indices. Since there are at most 124 selected edges, this loop is tiny.

The replacement step is easy to get wrong. Suppose slot `f` is the old minimum-weight edge and `d` is the dependency mask of the incoming edge. Since `f` belongs to `d`, XORing `d` into a basis representation containing `f` removes the old edge and introduces the new edge. The represented vector does not change, but the selected original edge associated with that representation does.

The comparison is strictly `w <= min_weight` for rejection. With equal weights, either edge gives the same objective value, so keeping the existing basis is sufficient and avoids unnecessary representation changes.

Python integers have arbitrary precision, so both the 124-bit graph vectors and the 124-bit representation masks are handled directly. No overflow occurs in the vector construction or in the answer, whose maximum is at most (200000\cdot10^9=2\cdot10^{14}).

## Worked Examples

### Sample 1

The input is

```
3 3
1 2 0 1
2 3 0 1
3 1 0 2
```

All pile values are zero, so the extra 60 coordinates are zero. The problem is consequently just maximum-weight forest selection.

| Query | Edge | Weight | Result of insertion | Rank | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1-2 | 1 | Independent, add | 1 | 1 |
| 2 | 2-3 | 1 | Independent, add | 2 | 2 |
| 3 | 3-1 | 2 | Dependent, circuit contains edges 1 and 2 | 2 | 3 |

At the third query, the new edge completes the triangle. Its dependency representation contains the first two selected edges. Their weights are both 1, so one of them is replaced by the new edge of weight 2. The selected graph still has two independent edges and now has total weight 3.

The outputs are therefore

```
1
2
3
```

This example demonstrates why a dependent edge cannot simply be discarded. A heavier dependent edge can replace a lighter edge in the circuit and improve the optimal basis.

### Sample 2

The input is

```
6 6
1 2 1 1
2 3 1 2
3 4 1 3
4 1 1 4
5 6 1 2
6 5 1 1
```

The first four edges form a four-cycle, and every one of them has pile value 1. The XOR of all four pile values is zero, so the four cycle vectors are dependent.

| Query | Edge | Weight | Result of insertion | Rank | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1-2, a=1 | 1 | Independent, add | 1 | 1 |
| 2 | 2-3, a=1 | 2 | Independent, add | 2 | 3 |
| 3 | 3-4, a=1 | 3 | Independent, add | 3 | 6 |
| 4 | 4-1, a=1 | 4 | Dependent, circuit contains all four | 3 | 9 |
| 5 | 5-6, a=1 | 2 | Independent, add | 4 | 11 |
| 6 | 6-5, a=1 | 1 | Dependent, same vector as edge 5 | 4 | 11 |

At query 4, the circuit contains all four edges. The minimum weight is 1, so the edge of weight 1 is replaced by the new edge of weight 4. The best total becomes (2+3+4=9).

The fifth edge is independent because it introduces vertices 5 and 6, so its weight 2 is added. The sixth edge has exactly the same augmented vector as the fifth edge, but its weight is only 1, so it cannot improve the basis.

The outputs are

```
1
3
6
9
11
11
```

This example exercises both kinds of dependence: a genuine cycle with a zero Nim XOR and two parallel edges carrying the same pile value.

## Complexity Analysis

Let

[
D=n+60\le124.
]

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(qD)) | Each insertion performs at most (D) Gaussian steps, at most (D) steps to find the minimum-weight edge in a dependency, and at most (D) representation updates. |
| Space | (O(D^2)) bits | There are at most (D) basis vectors and each representation is a (D)-bit integer. |

The dimension is bounded by only 124, so the algorithm performs a small constant amount of work per query. With (q\le200000), the total number of basis-coordinate iterations is proportional to roughly (25) million, rather than depending on the number of possible edge subsets. The state itself contains only a constant number of 124-bit objects.

The original problem has a 1.5 second limit and the intended implementation uses fixed-size 128-bit bitsets, which is why the same (O(qD)) structure is particularly fast in C++. The Python implementation uses arbitrary-precision integers for the same bitset operations and keeps all state bounded by the 124-dimensional basis.

## Test Cases

The following test harness assumes the solution above has been saved as `solution.py` and exposes the `solve()` function.

```python
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run(
    """3 3
1 2 0 1
2 3 0 1
3 1 0 2
"""
) == "1\n2\n3", "sample 1"

# Sample 2
assert run(
    """6 6
1 2 1 1
2 3 1 2
3 4 1 3
4 1 1 4
5 6 1 2
6 5 1 1
"""
) == "1\n3\n6\n9\n11\n11", "sample 2"

# Sample 3
assert run(
    """5 5
1 2 0 1
2 3 1 1
3 4 2 3
4 5 4 9
5 1 7 29
"""
) == "1\n2\n5\n14\n42", "sample 3"

# Sample 4
assert run(
    """5 1
3 5 35 35
"""
) == "35", "sample 4"

# Minimum-size input.
assert run(
    """2 1
1 2 0 7
"""
) == "7", "minimum size"

# All equal vectors and equal weights.
assert run(
    """3 3
1 2 0 5
2 3 0 5
3 1 0 5
"""
) == "5\n10\n10", "equal values and equal weights"

# Parallel edges with different weights.
assert run(
    """2 3
1 2 0 4
1 2 0 9
1 2 0 6
"""
) == "4\n9\n9", "parallel edges"

# Maximum 60-bit pile value.
MAX_A = (1 << 60) - 1
assert run(
    f"""2 2
1 2 {MAX_A} 3
1 2 {MAX_A} 10
"""
) == "3\n10", "60-bit boundary"

# Maximum q and n, with all vectors identical.
# Every prefix has rank one, so the answer is always 1.
q = 200000
lines = [f"64 {q}"]
lines.extend(["1 2 0 1"] * q)
maximum_case = "\n".join(lines) + "\n"

out = run(maximum_case)
maximum_lines = out.splitlines()

assert len(maximum_lines) == q, "maximum q"
assert maximum_lines[0] == "1", "maximum q first answer"
assert maximum_lines[-1] == "1", "maximum q last answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, one edge | `7` | Minimum number of vertices and queries, plus an acyclic graph |
| Three-edge triangle with all `a=0` and all weights `5` | `5, 10, 10` | Equal weights and strict replacement condition |
| Three parallel edges with weights `4,9,6` | `4, 9, 9` | Equal vectors and keeping the best representative |
| Two identical edges with (a=2^{60}-1) | `3, 10` | Highest allowed pile bits and 64-bit boundary handling |
| `n=64`, `q=200000`, identical edges | `1` for every prefix | Maximum dimensions and query count |

## Edge Cases

An acyclic graph is handled naturally because an independent set of edge vectors corresponds to a good graph regardless of whether it contains a cycle. For

```
3 2
1 2 0 5
2 3 0 7
```

the first vector creates rank 1 and contributes 5. The second creates rank 2 and contributes 7. No dependency is encountered, so the output is `5` followed by `12`.

A zero-Nim-XOR cycle is handled by the extra pile coordinates. For

```
3 3
1 2 0 1
2 3 0 2
3 1 0 10
```

the first two vectors are independent. The third reduces to zero because the XOR of all three edge vectors is zero. Its dependency contains the first two selected edges, with minimum weight 1. Since the incoming edge has weight 10, that edge replaces the weight-1 edge. The resulting rank remains 2 and the answer becomes 12. The output is `1`, `3`, `12`.

Parallel edges are handled as ordinary vectors rather than by endpoint pairs. For

```
2 2
1 2 0 5
1 2 0 9
```

both augmented vectors are equal. The second insertion reduces to zero, and its dependency contains the first edge. Since 9 is larger than 5, the first selected edge is replaced. The output is `5`, `9`.

Equal weights require no exchange. For

```
2 3
1 2 0 5
1 2 0 5
1 2 0 5
```

the first edge is selected. Each later edge is dependent on it, but the minimum weight in the dependency is also 5. Since the new weight is not greater, the basis stays unchanged and every answer remains 5.

The largest pile value uses all 60 available pile coordinates. For

```
2 2
1 2 1152921504606846975 3
1 2 1152921504606846975 10
```

both vectors are identical, because their endpoint bits and all 60 pile bits coincide. The second edge replaces the first because its weight is larger. The outputs are `3` and `10`.

Finally, when (q=200000), the number of inserted edges is far larger than the maximum possible rank. This is exactly the situation where storing every previous edge would be unnecessary for the core algorithm. After at most 124 successful independent insertions, the rank can never grow again. Later edges only create dependency circuits and can exchange selected edges. The maximum-size test with identical vectors exercises this behavior for the full query limit without increasing the basis size beyond one.
