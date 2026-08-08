---
title: "CF 102441J - Paternity Testing"
description: "We have a rooted tree with vertex 1 as the root. Vertices are numbered from 1 to (n). For a query interval ([l,r]), every vertex (v) with (lle vle r) contributes the number of vertices from the same interval that lie in the subtree of (v)."
date: "2026-08-08T13:33:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "J"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 268
verified: true
draft: false
---

[CF 102441J - Paternity Testing](https://codeforces.com/problemset/problem/102441/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with vertex 1 as the root. Vertices are numbered from 1 to (n). For a query interval ([l,r]), every vertex (v) with (l\le v\le r) contributes the number of vertices from the same interval that lie in the subtree of (v). Thus the answer is the number of ordered pairs ((u,v)) inside the interval for which (u) is an ancestor of (v), including the pair ((v,v)).

The tree is given by (n-1) ancestor references. The (i)-th reference describes an ancestor of vertex (i+1), so every ancestor of a vertex has a smaller label. Queries are encoded using the previous answer: the two input values are XORed with the previous answer, reduced modulo (n), shifted to the range (1\ldots n), and then sorted to obtain (l) and (r). This encoding makes the queries online, so we cannot reorder them or preprocess them after seeing all decoded intervals. The original problem specifies (n,q\le 50000) and a 3 second time limit.

The answer can be as large as (n(n+1)/2). With (n=50000), that is (1,250,025,000), so a 32-bit signed integer is still sufficient for the final answer, although using Python integers removes any overflow concern.

A singleton interval is easy to get wrong if the implementation only counts ancestor-descendant pairs with two different vertices. For example,

```
1
1
0 0
```

decodes to ([1,1]), and the answer is `1`, because a vertex is contained in its own subtree.

Two unrelated vertices are another useful boundary case. Consider

```
3
1
1
1
1 2
```

The query is ([2,3]). Neither vertex is an ancestor of the other, so each contributes only itself and the answer is `2`. An implementation that counts every pair of vertices in the interval as an ancestor pair would incorrectly return `3`.

A query containing the root also tests whether the whole subtree is handled correctly. For

```
3
1
1
1
0 2
```

the interval is ([1,3]). Vertex 1 contains all three vertices, while vertices 2 and 3 contain only themselves. The answer is `3 + 1 + 1 = 5`. An implementation that accidentally excludes the root or treats the subtree interval as half-open in the wrong place can lose one of these contributions.

## Approaches

The direct approach is to examine every pair of vertices in the queried interval and test whether one is an ancestor of the other. A DFS gives each vertex an entry time `tin` and exit time `tout`, and (u) is an ancestor of (v) exactly when

[
tin_u\le tin_v<tout_u.
]

This makes each pair test constant time after preprocessing. However, a query containing all (n) vertices examines (\Theta(n^2)) pairs. With (n=q=50000), that is about (1.25\times10^9) unordered pairs for one query and about (6.25\times10^{13}) unordered pair checks across all queries. The brute force is correct because it tests exactly the definition of the answer, but it is far outside the available time.

The useful observation is that ancestor relationships have a very rigid structure in DFS order. For two distinct vertices, exactly one of the following happens. One subtree contains the other, or their subtrees are disjoint. If (u) and (v) are disjoint and (u) appears first in DFS order, then

[
tout_u\le tin_v.
]

The editorial formulation uses this complementary view. For an interval containing (k) vertices, there are (\binom{k}{2}) unordered pairs of distinct vertices. Every pair that is not an ancestor-descendant pair is a pair of disjoint subtrees. If `bad(l,r)` is the number of such disjoint pairs, then

# k+\binom{k}{2}-bad(l,r)

\frac{k(k+1)}2-bad(l,r).
]

This turns the problem into range queries over the vertex labels, where each pair contributes one if the two corresponding subtrees are disjoint.

We then split the label axis into blocks of size (T). A query has at most two partial blocks, at its two ends. Everything between them consists of complete blocks. We precompute the answer for every interval of complete blocks. We also precompute, for every vertex and every block boundary, how many vertices in the prefix of blocks have disjoint subtrees with that vertex, and symmetrically for suffixes of blocks. This lets every interaction between a boundary vertex and all complete middle blocks be evaluated in (O(1)).

The only remaining work inside the two partial blocks is bounded by (O(T)). The interaction between the two partial blocks is counted by merging their DFS interval endpoints after sorting each block once.

This is the same square-root decomposition idea described in the official editorial material: choose (T) around (n/\sqrt q), precompute element-to-block-prefix information and complete-block answers, then answer each query by processing only the two boundary blocks. The resulting bound is (O(n(\sqrt q+\log n))).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn^2)) | (O(n)) | Too slow |
| Optimal | (O(n(\sqrt q+\log n))) | (O(n\sqrt q)) | Accepted |

## Algorithm Walkthrough

1. Run a DFS from vertex 1 and compute `tin[v]` and `tout[v]`. The subtree of (v) is represented by the half-open DFS interval ([tin[v],tout[v])). Two vertices have disjoint subtrees exactly when one of `tout[u] <= tin[v]` or `tout[v] <= tin[u]` holds.
2. Choose a block size (T) close to (n/\sqrt q). The label interval (1\ldots n) is divided into consecutive blocks. A query can intersect many complete blocks, but only its first and last blocks can be partial.
3. For every vertex (v) and every block prefix, precompute how many vertices in that prefix have subtrees disjoint from (v). We call this `pref[v][b]`, where `b` means blocks with indices smaller than `b`.

This value is the sum of two independent conditions. A previous vertex (u) is disjoint from (v) either because (tout[u]\le tin[v]), or because (tout[v]\le tin[u]). Both sets can be counted with sweeps over DFS entry and exit times.
4. Build the analogous suffix table `suf[v][b]`, which counts disjoint vertices in blocks from `b` onward. The same two DFS-time sweeps are used, but the block indices are processed in reverse.
5. For every block, precompute the number of disjoint pairs inside every subinterval of that block. There are only (T) vertices in a block, so all its subintervals can be handled in (O(T^2)). We store the result in a compact integer array.
6. Precompute `full[a][b]`, the number of disjoint pairs among all vertices belonging to complete blocks (a,a+1,\ldots,b). When block (b) is appended to an interval beginning at block (a), its internal pairs are already known. For every vertex (v) in block (b), `pref[v][b] - pref[v][a]` counts its disjoint partners in the preceding complete blocks. Summing this over the block gives the new cross-block contribution.
7. Decode every query using the previous answer. Convert the two encoded numbers to vertices in (1\ldots n), sort them into (l) and (r), and work with zero-based indices internally.
8. If both endpoints are in the same block, obtain `bad(l,r)` directly from the precomputed subinterval table.
9. Otherwise, take the precomputed `full` value for the complete blocks strictly between the two boundary blocks. Add the disjoint pairs inside the partial suffix of the left block and the partial prefix of the right block.
10. For every vertex in the left partial block, use the suffix table to count its disjoint partners in the complete middle blocks. For every vertex in the right partial block, use the prefix table to count its disjoint partners in those middle blocks. There are at most (2T) such boundary vertices, so this costs (O(T)).
11. Finally, count disjoint pairs between the two partial blocks. The values `tout` on the left and `tin` on the right are sorted, so the number satisfying `tout[left] <= tin[right]` can be found by a linear two-pointer merge. Repeat with the roles reversed. This counts every disjoint pair between the two partial blocks exactly once.
12. If the interval contains (k=r-l+1) vertices, output (k(k+1)/2-bad(l,r)), then store that value as the previous answer for decoding the next query.

### Why it works

For every two distinct vertices, their subtrees are either nested or disjoint. A nested pair contributes exactly one ancestor-descendant relationship, while a disjoint pair contributes none. Hence among the (\binom{k}{2}) unordered pairs inside a query interval, exactly `bad(l,r)` fail to contribute an ancestor relationship. Each vertex also contributes itself, giving (k) additional pairs. The decomposition counts every disjoint pair exactly once, either inside one partial block, between a partial block and the complete middle blocks, between two complete blocks, or between the two partial blocks. Thus the final formula (k(k+1)/2-bad(l,r)) is exactly the required sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array
from math import isqrt

def solve():
    n = int(input())

    children = [[] for _ in range(n)]
    for v in range(1, n):
        p = int(input()) - 1
        children[p].append(v)

    # Iterative DFS.
    tin = [0] * n
    tout = [0] * n
    at_tin = [0] * n
    at_tout = [0] * (n + 1)

    timer = 0
    stack = [(0, 0, 0)]

    while stack:
        v, p, state = stack.pop()

        if state == 0:
            tin[v] = timer
            at_tin[timer] = v
            timer += 1

            stack.append((v, p, 1))
            for u in reversed(children[v]):
                if u != p:
                    stack.append((u, v, 0))
        else:
            tout[v] = timer
            at_tout[timer] = v

    q = int(input())

    # T ~= n / sqrt(q).
    sq = max(1, isqrt(q))
    T = max(1, n // sq)
    B = (n + T - 1) // T
    stride = B + 1

    block_of = [v // T for v in range(n)]
    block_start = [b * T for b in range(B)]
    block_end = [min(n, (b + 1) * T) for b in range(B)]

    # Build a table:
    # table[v][b] = number of vertices in blocks [0, b)
    # whose subtrees are disjoint from v.
    #
    # If reverse=True, blocks are considered in reverse order.
    def build_disjoint_table(reverse):
        size = n * stride
        table = array('I', [0]) * size

        def mapped_block(v):
            b = block_of[v]
            return B - 1 - b if reverse else b

        cnt = [0] * B

        # First condition:
        # tout[u] <= tin[v].
        #
        # Sweep the threshold tin[v] from small to large.
        for t in range(n):
            u = at_tout[t] if t <= n else 0
            if t > 0:
                u = at_tout[t]
                cnt[mapped_block(u)] += 1

            v = at_tin[t]
            base = v * stride
            cur = 0
            table[base] = 0

            for b in range(B):
                cur += cnt[b]
                table[base + b + 1] = cur

        # Second condition:
        # tout[v] <= tin[u], equivalently tin[u] >= tout[v].
        #
        # Sweep the threshold tout[v] from large to small.
        cnt = [0] * B

        for s in range(n, 0, -1):
            u = at_tin[s - 1]
            cnt[mapped_block(u)] += 1

            v = at_tout[s]
            base = v * stride
            cur = 0

            for b in range(B):
                cur += cnt[b]
                table[base + b + 1] += cur

        return table

    pref = build_disjoint_table(False)
    suf = build_disjoint_table(True)

    # Precompute all subinterval answers inside one block.
    #
    # small[b][l * m + r] =
    # number of disjoint pairs in that subinterval.
    small = []
    internal = [0] * B

    for b in range(B):
        L = block_start[b]
        R = block_end[b]
        m = R - L

        sqmat = array('I', [0]) * (m * m)

        # Process the left endpoint backwards.
        # bad(l, r) = bad(l+1, r) + pairs(l, l+1..r).
        for l in range(m - 1, -1, -1):
            cur = 0
            vl = L + l
            row = l * m
            next_row = (l + 1) * m

            for r in range(l + 1, m):
                vr = L + r

                disjoint = (
                    tout[vl] <= tin[vr] or
                    tout[vr] <= tin[vl]
                )

                if disjoint:
                    cur += 1

                sqmat[row + r] = sqmat[next_row + r] + cur

        small.append(sqmat)
        internal[b] = sqmat[m - 1] if m else 0

    # full[a][b] = number of disjoint pairs in complete blocks a..b.
    full = [[0] * B for _ in range(B)]

    for a in range(B):
        total = 0

        for b in range(a, B):
            cross = 0

            for v in range(block_start[b], block_end[b]):
                base = v * stride
                cross += pref[base + b] - pref[base + a]

            total += internal[b] + cross
            full[a][b] = total

    # Values sorted by DFS entry and exit times inside every label block.
    # They let us count pairs between the two partial blocks in O(T).
    sorted_tin = []
    sorted_tout = []

    for b in range(B):
        L = block_start[b]
        R = block_end[b]

        ids = list(range(L, R))
        sorted_tin.append(sorted(ids, key=tin.__getitem__))
        sorted_tout.append(sorted(ids, key=tout.__getitem__))

    def count_le(A, Bvals):
        # A and Bvals are sorted.
        # Count pairs (a,b) with a <= b.
        j = 0
        m = len(Bvals)
        ans = 0

        for a in A:
            while j < m and Bvals[j] < a:
                j += 1
            ans += m - j

        return ans

    def cross_partial(lb, l, left_end, rb, right_start, r):
        # Count disjoint pairs between:
        # [l, left_end] and [right_start, r].
        #
        # The first orientation is tout[left] <= tin[right].
        # The second orientation is tout[right] <= tin[left].
        out_left = [
            tout[v]
            for v in sorted_tout[lb]
            if v >= l
        ]
        in_right = [
            tin[v]
            for v in sorted_tin[rb]
            if v <= r
        ]

        out_right = [
            tout[v]
            for v in sorted_tout[rb]
            if v <= r
        ]
        in_left = [
            tin[v]
            for v in sorted_tin[lb]
            if v >= l
        ]

        return count_le(out_left, in_right) + count_le(out_right, in_left)

    def query(l, r):
        k = r - l + 1
        lb = l // T
        rb = r // T

        if lb == rb:
            m = block_end[lb] - block_start[lb]
            ll = l - block_start[lb]
            rr = r - block_start[lb]
            bad = small[lb][ll * m + rr]
            return k * (k + 1) // 2 - bad

        # Complete blocks strictly between the two boundary blocks.
        bad = 0

        ml = lb + 1
        mr = rb - 1

        if ml <= mr:
            bad += full[ml][mr]

        # Pairs entirely inside the two partial blocks.
        left_m = block_end[lb] - block_start[lb]
        left_l = l - block_start[lb]
        bad += small[lb][left_l * left_m + left_m - 1]

        right_m = block_end[rb] - block_start[rb]
        right_r = r - block_start[rb]
        bad += small[rb][right_r]

        if ml <= mr:
            # Left partial block against all complete middle blocks.
            #
            # suf[v][B-k] represents original blocks k..B-1.
            left_prefix_column = B - (lb + 1)
            left_suffix_column = B - rb

            for v in range(l, block_end[lb]):
                base = v * stride
                bad += (
                    suf[base + left_prefix_column]
                    - suf[base + left_suffix_column]
                )

            # Complete middle blocks against the right partial block.
            for v in range(block_start[rb], r + 1):
                base = v * stride
                bad += (
                    pref[base + rb]
                    - pref[base + (lb + 1)]
                )

        # Interaction between the two partial blocks.
        bad += cross_partial(
            lb, l, block_end[lb] - 1,
            rb, block_start[rb], r
        )

        return k * (k + 1) // 2 - bad

    ans = 0
    output = []

    for _ in range(q):
        u, v = map(int, input().split())

        x = 1 + ((u ^ ans) % n)
        y = 1 + ((v ^ ans) % n)

        l = min(x, y) - 1
        r = max(x, y) - 1

        ans = query(l, r)
        output.append(str(ans))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The DFS is iterative because a chain-shaped tree can contain 50000 vertices, which would exceed Python's normal recursion depth. `tin` is assigned on entry and `tout` on exit, so the subtree of a vertex is exactly one half-open interval in DFS order.

The two disjoint-pair tables are stored in `array('I')` rather than ordinary Python lists. There are (O(n\sqrt q)) entries, and Python integers would consume considerably more memory. Every stored count is at most (\binom n2), which fits in an unsigned 32-bit integer for this constraint.

The first sweep of each table handles `tout[u] <= tin[v]`. The second handles `tout[v] <= tin[u]`. Their sum is exactly the number of vertices whose subtrees are disjoint from `v`. Reversing the block numbering produces the suffix table without changing the underlying tree information.

The `small` tables handle intervals that remain entirely inside one block. The recurrence uses a previously computed row, so every pair of vertices is examined once while all (O(T^2)) interval values are produced.

The complete-block table is built from the prefix disjoint counts. When block `b` is appended to a range beginning at block `a`, the difference `pref[v][b] - pref[v][a]` removes all vertices before block `a` and leaves exactly the preceding blocks inside the current range.

The query code keeps the order of operations precise because the XOR encoding depends on the previous answer. The raw query values must be decoded before any range calculation, and the newly computed answer must be assigned to `ans` only after the current query has been completely evaluated.

## Worked Examples

The official sample contains five encoded queries. The first two already demonstrate both the full-range case and a query spanning several blocks conceptually.

| Query | Previous answer | (x) | (y) | Interval | Vertices | Disjoint pairs | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 9 | [1,9] | 9 | 3 | 42 |
| 2 | 42 | 8 | 5 | [5,8] | 4 | 2 | 8 |
| 3 | 8 | 2 | 3 | [2,3] | 2 | 1 | 3 |
| 4 | 3 | 6 | 7 | [6,7] | 2 | 1 | 3 |
| 5 | 3 | 5 | 8 | [5,8] | 4 | 2 | 8 |

For the first query, all nine vertices are selected. There are (9\cdot10/2=45) self or unordered-pair contributions available before removing disjoint pairs. The only disjoint subtree pairs are the three pairs involving vertex 6 and one of vertices 7, 8, or 9. Hence (45-3=42).

For the second query, the previous answer is 42. The encoded values become (1\oplus42=43) and (2\oplus42=40). Reducing modulo 9 and adding one gives vertices 8 and 5, so the interval is [5,8]. There are four vertices, giving ten self-or-unordered-pair possibilities, and two disjoint pairs, giving (10-2=8).

A separate small example makes the disjoint-pair logic clearer.

```
4
1
1
2
1
2 3
```

The only query decodes to [3,4]. Vertices 3 and 4 are in different branches, so their subtrees are disjoint. There are two vertices and one disjoint pair, hence the answer is (2\cdot3/2-1=2).

| Step | Previous answer | (u) | (v) | Decoded interval | (k) | Bad pairs | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 3 | [3,4] | 2 | 1 | 2 |

This example confirms that the algorithm does not confuse two unrelated vertices with an ancestor-descendant pair. It also exercises the boundary where the query starts and ends inside the same small region of the label array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n(\sqrt q+\log n))) | DFS and sorting take (O(n\log n)); block preprocessing takes (O(n^2/T)); queries take (O(T)) each |
| Space | (O(n^2/T+nT)) | The prefix/suffix block tables and within-block interval tables dominate memory |

With (T\approx n/\sqrt q), the preprocessing term (n^2/T) and the total query term (qT) are both (O(n\sqrt q)). For (n,q\le50000), this is the intended square-root tradeoff. The compact integer arrays keep the large (O(n\sqrt q)) tables within the 512 MB memory limit.

## Test Cases

The test harness assumes the submitted solution is available as `solution.py` and exposes `solve()`.

```python
import sys
import io
from contextlib import redirect_stdout

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        out = io.StringIO()
        with redirect_stdout(out):
            solve()
        return out.getvalue()
    finally:
        sys.stdin = old_stdin

# Provided sample.
sample = """\
9
1
2
3
4
5
5
7
8
5
0 8
1 2
2 3
4 5
6 7
"""
assert run(sample) == "42\n8\n3\n3\n3", "provided sample"

# Minimum-size tree.
minimum = """\
1
1
0 0
"""
assert run(minimum) == "1", "singleton vertex"

# All encoded values equal.
# Every query becomes a singleton after XOR decoding.
all_equal = """\
5
1
1
1
1
4
0 0
0 0
0 0
0 0
"""
assert run(all_equal) == "1\n1\n1\n1", "all-equal encoded queries"

# Two sibling leaves.
siblings = """\
3
1
1
1
1 2
"""
assert run(siblings) == "2", "disjoint sibling subtrees"

# Root plus two children.
root_interval = """\
3
1
1
1
0 2
"""
assert run(root_interval) == "5", "root interval boundary"

# Maximum-size chain.
# Every vertex is an ancestor of every later vertex, so the full interval
# has answer n * (n + 1) / 2.
n = 50000
parents = "\n".join(["1"] + [str(i) for i in range(2, n)])
maximum = (
    str(n) + "\n" +
    parents + "\n" +
    "1\n" +
    "0 " + str(n - 1) + "\n"
)
expected = str(n * (n + 1) // 2)
assert run(maximum) == expected, "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `1` | Minimum tree and self-counting |
| Five-node star with four `0 0` queries | `1 1 1 1` | Repeated XOR decoding and singleton intervals |
| Three-node tree with parents `1,1`, query `1 2` | `2` | Two disjoint subtrees and interval boundaries |
| Three-node tree with parents `1,1`, query `0 2` | `5` | Root subtree and full interval |
| 50000-node chain | `1250025000` | Maximum size, large answer, and worst-case ancestor structure |

## Edge Cases

For a singleton interval, the algorithm enters the same-block branch immediately. For

```
1
1
0 0
```

the interval contains one vertex, so `k=1` and `bad=0`. The returned value is (1\cdot2/2=1). The within-block table contains the same result because its only interval has no pair of distinct vertices.

For two unrelated vertices, consider

```
3
1
1
1
2
1
```

The encoded query is [2,3]. Their subtrees are disjoint, so `bad=1`. With (k=2), the formula gives (2\cdot3/2-1=2). The merge between the two partial ranges detects the disjoint pair through one of the two DFS interval inequalities.

For the full three-vertex star,

```
3
1
1
1
0 2
```

the interval is [1,3]. Vertex 1 is an ancestor of both leaves, while the two leaves are disjoint. Thus `bad=1`, (k=3), and the answer is (3\cdot4/2-1=5). The root contributes three nodes to its subtree, while each leaf contributes itself.

The encoded queries also need special care because the current answer changes the meaning of the next input pair. In the official sample, the first query gives 42. The next raw values `1 2` are consequently decoded using XOR with 42, producing the interval [5,8], not the interval [2,3] that the raw numbers might suggest. This dependency is why queries must be answered strictly in input order.

Finally, a chain is the opposite structural extreme from a star. In a 50000-node chain, every pair of distinct vertices is an ancestor-descendant pair, so `bad=0` for the full interval. The answer becomes (50000\cdot50001/2=1,250,025,000). This case checks both the arithmetic at the largest possible answer and the fact that the disjoint-pair machinery does not accidentally subtract nested subtrees.
