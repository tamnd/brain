---
title: "CF 102222K - Vertex Covers"
description: "We have an undirected simple graph with at most 36 vertices. Each vertex has a multiplicative weight. A chosen set of vertices is valid when every edge has at least one endpoint in the set."
date: "2026-08-17T22:15:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "K"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 193
verified: true
draft: false
---

[CF 102222K - Vertex Covers](https://codeforces.com/problemset/problem/102222/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected simple graph with at most 36 vertices. Each vertex has a multiplicative weight. A chosen set of vertices is valid when every edge has at least one endpoint in the set. For every valid set (S), its value is the product of the weights of its chosen vertices, with the empty product equal to 1. The task is to add these products over every valid vertex cover and report the result modulo the given prime (q).

The input contains several independent graphs. For each test case, (n) is the number of vertices, (m) is the number of edges, and (q) is the modulus. The next line contains the vertex weights, followed by the edges. The answer for each test case is printed with its case number.

The key constraint is (n\le 36). A direct enumeration has (2^{36}=68,719,476,736) possible subsets, which is already far beyond what a 10 second program can examine. The graph can also contain (\Theta(n^2)) edges, so checking every edge for every subset would be even worse. The guarantee that at most 36 test cases have (n>18) tells us that an exponential algorithm is intended, but its exponential part must depend on roughly half of (n), not on (n) itself.

The modulus is prime, but the solution does not need modular division. In particular, a vertex weight can be exactly (q), so its weight is zero modulo (q). Any approach that blindly divides by vertex weights or uses modular inverses would need additional special handling. The solution below only uses multiplication and addition modulo (q), so this case works automatically.

A graph with no edges is another easy place to make a silent mistake. Consider

```
1
3 0 998244353
2 3 5
```

Every subset is a vertex cover, including the empty subset. The answer is

[
(1+2)(1+3)(1+5)=72.
]

An implementation that starts enumerating only nonempty covers would miss the contribution 1 from the empty set.

A single vertex with no edges exercises the same boundary condition:

```
1
1 0 998244353
5
```

There are two covers, the empty set with value 1 and the set containing the vertex with value 5, so the answer is 6.

A weight equal to the modulus gives another subtle case:

```
1
1 0 998244353
998244353
```

The two covers have values 1 and (998244353), which become 1 and 0 modulo (q). The correct answer is 1. A solution based on modular inverses cannot invert this weight, while the meet-in-the-middle solution has no such problem.

Finally, for two vertices joined by one edge,

```
1
2 1 998244353
2 3
1 2
```

the valid covers are ({1}), ({2}), and ({1,2}), with values 2, 3, and 6. The answer is 11. This catches the common mistake of counting only minimal vertex covers, since the full set is also a vertex cover and contributes to the sum.

## Approaches

The brute-force solution follows the definition directly. Enumerate every subset (S) of the (n) vertices, test whether every edge has at least one endpoint in (S), and if it is a cover, multiply the weights of its selected vertices and add the result.

This is correct because every subset is examined exactly once, and the test is exactly the definition of a vertex cover. The problem is the number of subsets. For (n=36), there are (2^{36}=68,719,476,736) of them. Even if checking a subset were somehow reduced to a handful of machine operations, this would be too slow. A straightforward edge-by-edge check could require up to (2^{36}\cdot 630), which is more than (4\times10^{13}) edge checks.

The useful observation is that a vertex cover is precisely the complement of an independent set. However, we do not actually need to transform the weighted expression into an independent-set expression. Doing so algebraically would suggest dividing by vertex weights, which is unsafe when a weight is zero modulo (q). Instead, we split the vertices into two parts and keep the original cover weights.

Let the left side contain (L) vertices and the right side contain (R) vertices. Consider fixing the chosen vertices on the left. Edges entirely inside the left side can be checked immediately. Every cross edge whose left endpoint was not selected forces its right endpoint to be selected. Thus the left choice determines a mask called `need`, containing all right vertices that are mandatory.

What remains is a right-side query: among all right-side vertex covers, what is the total weight of those that contain every vertex in `need`? We can answer all such queries at once with a subset zeta transform. Initially, an array stores the contribution of each exact right-side cover. After the transform, `sum[need]` contains the sum over every right cover that is a superset of `need`.

The brute-force works because every possible cover can be checked independently, but fails because there are (2^n) choices. The observation that fixing one half only imposes a subset requirement on the other half lets us replace the full enumeration by two enumerations of roughly (2^{n/2}), followed by a subset transform.

For the implementation, we use the equivalent independent-set test to determine whether a half-mask is a valid cover. If `cover` is the selected mask, then `full ^ cover` must contain no internal edge. Independent masks can be recognized in (O(2^k)) using a one-bit recurrence.

We choose the split slightly asymmetrically when useful. The right side is the side on which the subset zeta transform runs, so its size should be chosen to minimize (R2^R+2^{n-R}). For (n=36), this gives (R=16) and (L=20), instead of the conventional 18 and 18 split. This reduces the amount of work in Python while keeping the same asymptotic complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n m)) | (O(n)) | Too slow |
| Meet in the Middle + SOS DP | (O(2^L + R2^R)), (L+R=n) | (O(2^L+2^R)) | Accepted |

## Algorithm Walkthrough

1. Split the vertices into a left part of size (L) and a right part of size (R). The implementation chooses the split that minimizes (R2^R+2^{n-R}), so the expensive subset-transform side is kept small.
2. Store three kinds of bitmasks. For every left vertex, store its neighbors inside the left part and its neighbors inside the right part. For every right vertex, store its neighbors inside the right part. Bitmasks make all adjacency checks constant-time at the scale of these small halves.
3. Enumerate every subset of the right vertices and compute whether its complement is an independent set. If the complement is independent, the subset itself is a valid right-side vertex cover. At the same time, compute the product of the selected right-side weights.
4. Put the product of every valid exact right-side cover into `sum[mask]`. Invalid masks receive zero. This array initially describes exact covers, so `sum[mask]` means only the cover equal to `mask`.
5. Apply a superset subset-zeta transform to `sum`. After processing every right-side bit, `sum[mask]` becomes the sum of the weights of all valid right-side covers containing `mask`. The transform is exactly what we need because the left half only tells us which right vertices are mandatory.
6. Precompute `need[mask]` for every left-side mask. `need[mask]` is the union of right-side neighbors of every left vertex that is not selected in `mask`. Such right vertices must be selected, otherwise their cross edge would have neither endpoint in the cover.
7. Enumerate every left-side cover mask. Its internal validity is checked by looking at the complement of the mask and testing whether that complement is an independent set. Its selected vertex product is computed independently.
8. For a valid left mask, multiply its weight product by `sum[need[mask]]`. The latter sums exactly all right-side covers that satisfy the cross-edge requirements. Add this value to the answer modulo (q).
9. Print the accumulated answer for the test case.

The invariant behind the combination step is that every complete vertex cover has exactly one left mask. Once that left mask is fixed, all internal left edges are either covered or the mask is discarded. Every cross edge with an unselected left endpoint forces its right endpoint into the cover, and `need` records exactly those forced vertices. The zeta-transformed right array then sums precisely all valid right masks containing those forced vertices. Hence every complete cover contributes once, and no invalid cover contributes.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve_case(n, m, q, weights, edges):
    # Choose R to minimize the dominant subset work:
    # R * 2^R for the SOS transform plus 2^(n-R) for the other half.
    best_r = 0
    best_cost = 1 << (n + 1)

    for r in range(n + 1):
        cost = r * (1 << r) + (1 << (n - r))
        if cost < best_cost:
            best_cost = cost
            best_r = r

    R = best_r
    L = n - R

    adj_l = [0] * L
    adj_r = [0] * R
    cross = [0] * L

    for u, v in edges:
        if u < L and v < L:
            adj_l[u] |= 1 << v
            adj_l[v] |= 1 << u
        elif u >= L and v >= L:
            u -= L
            v -= L
            adj_r[u] |= 1 << v
            adj_r[v] |= 1 << u
        else:
            if u < L:
                cross[u] |= 1 << (v - L)
            else:
                cross[v] |= 1 << (u - L)

    wl = [x % q for x in weights[:L]]
    wr = [x % q for x in weights[L:]]

    # Compute independent-set flags and cover products for the right half.
    nr = 1 << R
    full_r = nr - 1

    ind_r = bytearray(nr)
    ind_r[0] = 1

    prod_r = [0] * nr
    prod_r[0] = 1

    for mask in range(1, nr):
        bit = mask & -mask
        v = bit.bit_length() - 1
        rest = mask ^ bit

        prod_r[mask] = prod_r[rest] * wr[v] % q

        if ind_r[rest] and (adj_r[v] & rest) == 0:
            ind_r[mask] = 1

    # sum[cover] is the exact contribution of this right-side cover.
    # A cover is valid exactly when its complement is independent.
    sum_r = [0] * nr

    for cover in range(nr):
        if ind_r[full_r ^ cover]:
            sum_r[cover] = prod_r[cover]

    # Superset zeta transform.
    for bit_index in range(R):
        bit = 1 << bit_index
        step = bit << 1

        for base in range(0, nr, step):
            end = base + bit
            other = end

            for mask in range(base, end):
                x = sum_r[mask] + sum_r[other]
                if x >= q:
                    x -= q
                sum_r[mask] = x
                other += 1

    # need[mask] = right vertices forced by unselected left vertices.
    nl = 1 << L
    need = array('I', [0]) * nl

    # Compute from supersets. For a mask that is not full, choose a zero bit v.
    # need[mask] = need[mask | bit] | cross[v].
    for mask in range(nl - 2, -1, -1):
        zero_bit = (~mask) & (mask + 1)
        v = zero_bit.bit_length() - 1
        need[mask] = need[mask | zero_bit] | cross[v]

    # Compute independent-set flags and selected-weight products on the left.
    ind_l = bytearray(nl)
    ind_l[0] = 1

    prod_l = [0] * nl
    prod_l[0] = 1

    for mask in range(1, nl):
        bit = mask & -mask
        v = bit.bit_length() - 1
        rest = mask ^ bit

        prod_l[mask] = prod_l[rest] * wl[v] % q

        if ind_l[rest] and (adj_l[v] & rest) == 0:
            ind_l[mask] = 1

    full_l = nl - 1
    ans = 0

    for cover in range(nl):
        if ind_l[full_l ^ cover]:
            ans += prod_l[cover] * sum_r[need[cover]] % q
            if ans >= q:
                ans -= q

    return ans

def solve_data(data):
    tokens = list(map(int, data.split()))
    p = 0
    t = tokens[p]
    p += 1

    out = []

    for case_id in range(1, t + 1):
        n = tokens[p]
        m = tokens[p + 1]
        q = tokens[p + 2]
        p += 3

        weights = tokens[p:p + n]
        p += n

        edges = []
        for _ in range(m):
            u = tokens[p] - 1
            v = tokens[p + 1] - 1
            p += 2
            edges.append((u, v))

        ans = solve_case(n, m, q, weights, edges)
        out.append(f"Case #{case_id}: {ans}")

    return "\n".join(out)

def main():
    data = sys.stdin.buffer.read()
    sys.stdout.write(solve_data(data))

if __name__ == "__main__":
    main()
```

The first part of `solve_case` chooses the split. The conventional choice would be (L=\lceil n/2\rceil) and (R=\lfloor n/2\rfloor), but Python benefits from making the SOS side a little smaller. The small loop over all possible (R) values finds the best split without affecting the algorithm itself.

The three adjacency arrays encode the graph in the form needed by the two halves. `adj_l[v]` and `adj_r[v]` are local adjacency masks. `cross[v]` contains right vertices adjacent to left vertex (v). The distinction between these masks prevents cross edges from accidentally being treated as internal edges.

The independent-set arrays are the cleanest way to validate a cover. For a mask containing vertex `v`, remove its lowest set bit to obtain `rest`. The larger mask is independent exactly when `rest` is independent and `v` has no neighbor in `rest`. Since a cover and its complement are equivalent to an independent set, testing `ind[full ^ cover]` gives the validity of a cover without checking every edge.

The product arrays are computed using the same lowest-bit recurrence. If `mask = rest | {v}`, then the product for `mask` is the product for `rest` multiplied by the weight of `v`. Every multiplication is reduced modulo (q), so Python never constructs enormous exact products.

The right-side `sum_r` initially contains contributions for exact covers. The zeta transform changes its meaning from exact equality to containment. For every bit, a mask without that bit receives the contribution of the corresponding mask with that bit set. After all bits are processed, `sum_r[need]` contains every valid cover that contains `need`.

The `need` array deserves particular attention because it depends on unselected left vertices, not selected ones. For every mask, choose one vertex absent from it. If that vertex were selected, we would have the larger mask `mask | bit`. The unselected vertex contributes its entire cross-neighbor mask, giving the recurrence

[
need[mask]=need[mask\cup{v}]\mathbin{|}cross[v].
]

The loop runs backwards so the larger mask has already been computed.

The final loop only accepts left covers whose complements are independent. For each such cover, `prod_l[cover]` is its exact weight, while `sum_r[need[cover]]` accounts for every compatible right cover. Their product is exactly the total contribution of all complete covers extending that left choice.

There is no integer overflow issue in Python. In a language with fixed-width integers, every product should be evaluated in a sufficiently wide type before taking the modulus. The bit masks also fit comfortably inside a normal integer because there are at most 36 vertices.

## Worked Examples

### Sample 1

The graph is the path (1-2-3-4), and every weight is 1. With the natural two-and-two split, the left vertices are 1 and 2 and the right vertices are 3 and 4.

For the right half, the exact valid covers are `01`, `10`, and `11`. The right-side edge is between vertices 3 and 4, so the empty right cover is invalid.

| Right mask | Exact contribution | After superset transform |
| --- | --- | --- |
| `00` | 0 | 3 |
| `01` | 1 | 2 |
| `10` | 1 | 2 |
| `11` | 1 | 1 |

The left edge is between vertices 1 and 2. The valid left covers are `01`, `10`, and `11`. For `01`, vertex 2 is unselected, and its cross edge to vertex 3 forces right bit `01`. For the other two left covers, no right vertex is forced.

| Left mask | Valid cover | `need` | Left product | Right sum | Contribution |
| --- | --- | --- | --- | --- | --- |
| `00` | No | `11` | 1 | 1 | 0 |
| `01` | Yes | `01` | 1 | 2 | 2 |
| `10` | Yes | `00` | 1 | 3 | 3 |
| `11` | Yes | `00` | 1 | 3 | 3 |

The total is (2+3+3=8), matching `Case #1: 8`. The trace demonstrates the central invariant: once the left cover is fixed, the cross edges become only mandatory-vertex constraints on the right.

### Sample 2

The graph is (K_4), again with all weights equal to 1. A vertex cover of a complete graph must contain at least three vertices. With the same two-and-two split, the right half has an internal edge, and every left vertex is connected to both right vertices.

The right-side transformed values are again

| Right mask | Exact contribution | After superset transform |
| --- | --- | --- |
| `00` | 0 | 3 |
| `01` | 1 | 2 |
| `10` | 1 | 2 |
| `11` | 1 | 1 |

The valid left covers are `01`, `10`, and `11`. If exactly one left vertex is selected, the other left vertex is unselected and forces both right vertices, giving `need = 11`. If both left vertices are selected, `need = 00`.

| Left mask | Valid cover | `need` | Left product | Right sum | Contribution |
| --- | --- | --- | --- | --- | --- |
| `00` | No | `11` | 1 | 1 | 0 |
| `01` | Yes | `11` | 1 | 1 | 1 |
| `10` | Yes | `11` | 1 | 1 | 1 |
| `11` | Yes | `00` | 1 | 3 | 3 |

The answer is (1+1+3=5). The three contributions correspond exactly to the four-vertex covers of sizes three and four, with four covers of size three and one cover of size four.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2^L + R2^R + m)) | Half-mask DP costs (O(2^L+2^R)), the superset transform costs (O(R2^R)), and reading/building the graph costs (O(m)). |
| Space | (O(2^L+2^R+n+m)) | The dominant storage consists of the subset arrays for the two halves. |

Here (L+R=n), and the implementation chooses (R) to minimize the actual expression (R2^R+2^{n-R}). For (n=36), the chosen split is 20 and 16, so the largest subset space is about (2^{20}), and the transform touches about (16\cdot2^{16}) states. This is substantially smaller than enumerating (2^{36}) full-graph subsets and fits the intended exponential scale of the problem.

The guarantee that only at most 36 test cases have (n>18) is especially helpful because those are the cases responsible for the large subset arrays. Smaller test cases have dramatically smaller state spaces.

## Test Cases

The test harness below assumes the editorial solution is saved as `solution.py`, where `solve_data` is the function defined above.

```
import io
from solution import solve_data

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples.
sample = """\
2
4 3 998244353
1 1 1 1
1 2
2 3
3 4
4 6 998244353
1 1 1 1
1 2
1 3
1 4
2 3
2 4
3 4
"""

assert run(sample) == """\
Case #1: 8
Case #2: 5
""", "provided samples"

# Minimum-size graph: one isolated vertex.
assert run("""\
1
1 0 998244353
5
""") == "Case #1: 6", "empty graph and empty cover"

# A weight equal to q becomes zero modulo q.
assert run("""\
1
1 0 998244353
998244353
""") == "Case #1: 1", "weight equal to modulus"

# Smallest graph with an edge, including the full cover.
assert run("""\
1
2 1 998244353
2 3
1 2
""") == "Case #1: 11", "single edge"

# Maximum n, all equal weights, no edges.
# Every subset is a cover, so the answer is 2^36 modulo 998244353.
assert run("""\
1
36 0 998244353
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
""") == "Case #1: 838860732", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 998244353 / 5` | `Case #1: 6` | Minimum size, empty graph, empty cover |
| `1 0 998244353 / 998244353` | `Case #1: 1` | Weight equal to the modulus |
| `2 1 998244353 / 2 3 / 1 2` | `Case #1: 11` | Edge constraint and inclusion of the full cover |
| `36 0 998244353 / 36 ones` | `Case #1: 838860732` | Maximum vertex count, all equal weights, exponential-state boundary |

## Edge Cases

For an empty graph, every subset is a vertex cover because there are no edges that need to be covered. For the input

```
1
1 0 998244353
5
```

the right side of the split is empty. The only right mask has contribution 1. The two left masks represent the empty cover and the selected vertex, with products 1 and 5. Both complements are independent because the graph has no edges, so the answer is (1+5=6).

When a vertex weight is equal to the modulus, its contribution is zero modulo (q), but the vertex is still an ordinary graph vertex. For

```
1
1 0 998244353
998244353
```

the empty cover contributes 1 and the selected cover contributes 0 modulo (q). The subset products are computed with ordinary modular multiplication, so no inverse is ever required. The result is 1.

For the single-edge case

```
1
2 1 998244353
2 3
1 2
```

the valid masks are `01`, `10`, and `11`. Their products are 2, 3, and 6, giving 11. In the meet-in-the-middle view, whichever endpoint is placed on the left, an unselected left endpoint forces the right endpoint to be selected. The zeta query includes the forced right cover as well as any larger valid cover, so the full cover is counted rather than being mistaken for a minimal cover.

The maximum-size empty graph

```
1
36 0 998244353
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```

has all (2^{36}) subsets as vertex covers, because there are no edges. Every subset has product 1, so the answer is (2^{36}\bmod998244353=838860732). The algorithm never constructs those (2^{36}) complete subsets. It processes two halves independently and combines them through the subset transform, which is exactly why the maximum case remains feasible.
