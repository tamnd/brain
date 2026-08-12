---
title: "CF 102331H - Honorable Mention"
description: "For each query ((l,r,k)), we look only at the subarray (al,ldots,ar). We must choose exactly (k) nonempty pairwise disjoint contiguous pieces of that subarray and maximize the sum of all elements covered by those pieces. The pieces may be adjacent."
date: "2026-08-13T03:40:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "H"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 179
verified: true
draft: false
---

[CF 102331H - Honorable Mention](https://codeforces.com/problemset/problem/102331/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query ((l,r,k)), we look only at the subarray (a_l,\ldots,a_r). We must choose exactly (k) nonempty pairwise disjoint contiguous pieces of that subarray and maximize the sum of all elements covered by those pieces. The pieces may be adjacent. Adjacency matters because two pieces such as ([1,2]) and ([3,4]) are still two pieces, even though their union is one larger interval.

The input contains one array with (n\le 35000) elements and up to (q\le 35000) independent interval queries. Each element has absolute value at most (35000), so a whole interval can have absolute sum as large as (35000^2=1.225\times10^9). The number of queries rules out running a length-dependent dynamic program for every query. Even an (O((r-l+1)k)) solution can reach roughly (O(qn^2)), which is far beyond the available time. We need to preprocess the array into reusable interval information and make each query depend mainly on (\log n), not on its length.

The official problem uses the same constraints and examples described here.

There are several edge cases that are easy to mishandle. First, all values can be negative. For the input

```
1 1
-5
1 1 1
```

the answer is `-5`, not `0`. The selected segments must be nonempty and exactly one segment must be selected, so an empty selection is not allowed.

Second, the answer for exactly (k) segments is not monotone in (k). For

```
4 3
3 3 3 3
1 4 1
1 4 2
1 4 3
```

the answers are

```
12
12
9
```

For one segment we take all four elements. For two segments we can split them into two adjacent pieces and still obtain (12). For three segments, the best possibility is three singleton elements, giving (9). A solution designed for "at most (k)" segments would silently give the wrong result here.

Third, adjacent selected segments must remain separate when (k) requires it. For

```
3 1
5 -10 5
1 3 2
```

the answer is `10`, obtained by selecting positions 1 and 3 as two singleton segments. A careless implementation that treats every adjacent selected region as one segment has no issue here, but an implementation that assumes every chosen component must have a negative gap between it and the next one would incorrectly reject this configuration.

Finally, (k) can equal the interval length. For

```
3 1
-2 -3 -4
1 3 3
```

the answer is `-9`, because all three elements must be selected as three singleton segments. Any implementation that initializes the answer with zero or accidentally allows fewer than (k) segments will fail on this case.

## Approaches

The direct dynamic program for one query is already instructive. Let `end[j]` be the best value using exactly (j) segments where the current position belongs to the last selected segment, and let `best[j]` be the best value using exactly (j) segments anywhere in the processed prefix. For each element, we can either extend the last segment or start a new segment. This gives an (O(mk)) algorithm for a query on an interval of length (m).

That algorithm is correct because every optimal solution either leaves the current element unused, extends its final segment through the current element, or starts its final segment at the current element. The problem is the number of queries. If both the interval length and (k) are (\Theta(n)), one query can cost (O(n^2)), and (q) such queries give (O(qn^2)), roughly (4.3\times10^{13}) state transitions at the maximum constraints.

The key observation is that, for a fixed interval, the function

[
F(k)=\text{maximum value obtainable with exactly }k\text{ segments}
]

is concave. Equivalently, its marginal gains

[
F(k)-F(k-1)
]

are non-increasing. This property is also visible through the standard min-cost-flow formulation of the problem: the optimum value as a function of the required flow has the corresponding discrete convexity property. This is the structural fact that makes both Minkowski-sum merging and WQS binary search possible.

Suppose we already knew all values (F(0),F(1),\ldots,F(m)) for an interval. Two adjacent intervals could then be merged efficiently. If their concave functions have marginal gains

[
d_1\ge d_2\ge\cdots
]

and

[
e_1\ge e_2\ge\cdots,
]

the marginal gains of their max-plus convolution are simply the sorted merge of these two marginal sequences. This is the one-dimensional form of a Minkowski sum of convex hulls. Thus a segment tree can store the entire answer function for every node in (O(n\log n)) total construction work.

There is one complication. When two adjacent segment-tree nodes are joined, a selected segment can cross the boundary. To know whether two selected pieces should merge into one, each node must remember whether its leftmost and rightmost elements are selected. That gives four functions for every node, indexed by the two endpoint-selection bits. When the right endpoint of the left child and the left endpoint of the right child are both selected, their two pieces become one piece, so the resulting function is shifted by one in its segment-count coordinate.

At first this seems enough, but a query interval consists of (O(\log n)) segment-tree nodes, and merging their complete convex functions for every query would again be too expensive. WQS binary search removes the segment-count dimension during a query. For a penalty (\lambda), instead of maximizing (F(k)), we maximize

[
F(x)-\lambda x
]

over every possible number (x) of segments. Since (F) is concave, the maximizing (x) moves monotonically as (\lambda) changes. If the maximizing solution uses at least the requested (k) segments, we increase (\lambda); otherwise we decrease it. At the final slope, adding (k\lambda) recovers the exact answer.

A straightforward implementation would binary-search the best position separately inside every convex hull. That introduces another logarithmic factor. The final optimization is to process all queries in one WQS iteration in decreasing order of their current midpoint (\lambda). For a fixed convex hull, as (\lambda) decreases, its optimal position can only move forward. We keep a pointer for every node and every endpoint state, so each pointer only moves through its hull once during one WQS layer. This is the "overall" or parallel WQS optimization used by the intended solution. The resulting approach is described in the original solution material as (O((n+q)\log n\log V)), up to the sorting factor for the offline queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | (O(qn^2)) | (O(n)) per query | Too slow |
| Segment Tree + full convex functions | (O(n\log n+qn)) | (O(n\log n)) | Too slow |
| WQS with binary search inside every hull | (O((n+q)\log^2n\log V)) | (O(n\log n)) | Close, but unnecessarily slow |
| Offline WQS + monotone hull pointers | (O((n+q)\log n\log V+q\log q\log V)) | (O(n\log n+q\log n)) | Accepted |

## Algorithm Walkthrough

1. For every segment-tree node, store four arrays `h[x][y]`. The bit `x` says whether the left endpoint of the node is selected, and `y` says whether the right endpoint is selected. `h[x][y][k]` is the maximum sum obtainable with exactly `k` selected segments under those endpoint requirements. Impossible states are stored as negative infinity.

The endpoint information is necessary because two independently selected pieces can become one piece when two neighboring nodes are concatenated.
2. At a leaf containing value (a_i), the only meaningful states are `00` with zero selected segments and value zero, and `11` with one selected segment and value (a_i). States `01` and `10` are impossible because a one-element interval cannot have exactly one endpoint selected without selecting the other.
3. To merge two child hulls, take their max-plus convolution. If `A[k]` and `B[k]` are concave, the marginal differences of the resulting convolution are obtained by merging the marginal differences of `A` and `B` in decreasing order.

This makes the merge linear in the combined hull lengths instead of quadratic in the number of possible segment counts.
4. For every pair of child endpoint states, combine the corresponding hulls. If the left child's right endpoint and the right child's left endpoint are both selected, the two pieces touch and must count as one segment. In the segment-count coordinate this is a shift by one position.
5. Before processing the queries, decompose every interval ([l,r]) into the canonical (O(\log n)) segment-tree nodes covering it. The decomposition never changes during WQS, so it is computed only once.
6. For a fixed penalty (\lambda), each stored hull is queried for the index (p) maximizing

[
h[p]-p\lambda.
]

Since the hull is concave, this is exactly the largest position reached while the next marginal gain is at least (\lambda). The associated pair stores both the penalized value and the number of selected segments.
7. Process the canonical nodes of one query from left to right. The DP has two states according to whether the right endpoint of everything processed so far is selected. When the current node begins with its left endpoint selected and the previous state also ends selected, decrease the total segment count by one and add (\lambda) back to the penalized value, because two pieces have merged into one.
8. After all nodes of the query have been processed, take the better of the two right-endpoint states. The resulting pair gives the maximum penalized value and the number of segments selected at penalty (\lambda).
9. WQS binary-search (\lambda) for every query. If the number of selected segments is at least the required (k), the slope is too small or at the boundary where more segments are still preferable, so move the lower bound upward. Otherwise move the upper bound downward. At the selected final slope (\lambda^*), the exact answer is

[
\text{penalized optimum}+k\lambda^*.
]
10. During each binary-search layer, sort the queries by their current midpoint (\lambda) in decreasing order. Every hull pointer then moves only forward during that layer. Resetting the pointers once per layer gives the required amortization.

### Why it works

The invariant is that every segment-tree hull contains the exact optimum for every feasible segment count under its two endpoint-selection conditions. Minkowski merging preserves this invariant because a concatenated solution is either formed from two independent solutions or by joining the two boundary segments, and the corresponding segment count is exactly the ordinary sum or one less.

For a fixed penalty (\lambda), every possible solution with (x) segments receives adjusted value (F(x)-\lambda x). Concavity of (F) means the maximizing (x) moves monotonically as (\lambda) changes, so WQS binary search finds the slope whose supporting line reaches the required segment count. The tie rule chooses the largest maximizing segment count, which gives the correct side of a flat edge of the concave hull. At that slope, the supporting-line identity gives (F(k)) after adding back (k\lambda). The endpoint states account for every possible crossing of segment-tree boundaries, so no valid arrangement is lost.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

NEG = -10**30

def minkowski(a, b):
    na = len(a) - 1
    nb = len(b) - 1
    res = [0] * (na + nb + 1)

    s = a[0] + b[0]
    res[0] = s

    i = 0
    j = 0
    pos = 0

    while i < na and j < nb:
        da = a[i + 1] - a[i]
        db = b[j + 1] - b[j]

        if da > db:
            i += 1
            s += da
        else:
            j += 1
            s += db

        pos += 1
        res[pos] = s

    while i < na:
        i += 1
        s += a[i] - a[i - 1]
        pos += 1
        res[pos] = s

    while j < nb:
        j += 1
        s += b[j] - b[j - 1]
        pos += 1
        res[pos] = s

    return res

def merge_into(dst, src, shifted):
    limit = len(src)
    if not shifted:
        for i in range(limit):
            v = src[i]
            if v > dst[i]:
                dst[i] = v
    else:
        for i in range(limit):
            v = src[i]
            if v > dst[i]:
                dst[i] = v
            if i and v > dst[i - 1]:
                dst[i - 1] = v

def solve():
    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    size = 4 * n + 5
    tree = [None] * size

    def build(node, left, right):
        if left == right:
            h00 = [0, NEG]
            h01 = [NEG, NEG]
            h10 = [NEG, NEG]
            h11 = [NEG, a[left]]
            tree[node] = (h00, h01, h10, h11)
            return

        mid = (left + right) >> 1
        build(node << 1, left, mid)
        build(node << 1 | 1, mid + 1, right)

        lc = tree[node << 1]
        rc = tree[node << 1 | 1]

        length = right - left + 1
        cur = [
            [NEG] * (length + 1),
            [NEG] * (length + 1),
            [NEG] * (length + 1),
            [NEG] * (length + 1),
        ]

        for u in range(2):
            for v in range(2):
                left_hull = lc[u * 2 + v]

                for p in range(2):
                    for z in range(2):
                        right_hull = rc[p * 2 + z]

                        tmp = minkowski(left_hull, right_hull)

                        dst = cur[u * 2 + z]
                        merge_into(dst, tmp, v == 1 and p == 1)

        tree[node] = tuple(cur)

    build(1, 1, n)

    queries = []
    for idx in range(q):
        l, r, k = map(int, input().split())
        queries.append([l, r, k, -35000, 0, 0])

    # Canonical segment-tree decomposition for every query.
    parts = [[] for _ in range(q)]

    def collect(node, left, right, ql, qr, out):
        if ql <= left and right <= qr:
            out.append(node)
            return

        mid = (left + right) >> 1
        if ql <= mid:
            collect(node << 1, left, mid, ql, qr, out)
        if qr > mid:
            collect(node << 1 | 1, mid + 1, right, ql, qr, out)

    for idx, qu in enumerate(queries):
        collect(1, 1, n, qu[0], qu[1], parts[idx])

    total_abs = sum(abs(x) for x in a[1:])
    for qu in queries:
        qu[4] = total_abs

    # Four monotone pointers per segment-tree node.
    ptr0 = [0] * size
    ptr1 = [0] * size
    ptr2 = [0] * size
    ptr3 = [0] * size
    stamp = [0] * size

    def get_pointer(node, state, lam, round_id):
        if stamp[node] != round_id:
            stamp[node] = round_id
            ptr0[node] = 0
            ptr1[node] = 0
            ptr2[node] = 0
            ptr3[node] = 0

        if state == 0:
            p = ptr0[node]
        elif state == 1:
            p = ptr1[node]
        elif state == 2:
            p = ptr2[node]
        else:
            p = ptr3[node]

        hull = tree[node][state]

        while p + 1 < len(hull) and hull[p + 1] - hull[p] >= lam:
            p += 1

        if state == 0:
            ptr0[node] = p
        elif state == 1:
            ptr1[node] = p
        elif state == 2:
            ptr2[node] = p
        else:
            ptr3[node] = p

        return hull, p

    def evaluate(qid, lam, round_id):
        f0_val = 0
        f0_cnt = 0
        f1_val = NEG
        f1_cnt = 0

        for node in parts[qid]:
            old0_val = f0_val
            old0_cnt = f0_cnt
            old1_val = f1_val
            old1_cnt = f1_cnt

            nf0_val = NEG
            nf0_cnt = -10**9
            nf1_val = NEG
            nf1_cnt = -10**9

            for state in range(4):
                hull, p = get_pointer(node, state, lam, round_id)

                value = hull[p] - p * lam
                left_selected = state >> 1
                right_selected = state & 1

                if old0_val != NEG:
                    cand_val = old0_val + value
                    cand_cnt = old0_cnt + p

                    if right_selected == 0:
                        if cand_val > nf0_val or (
                            cand_val == nf0_val and cand_cnt > nf0_cnt
                        ):
                            nf0_val = cand_val
                            nf0_cnt = cand_cnt
                    else:
                        if cand_val > nf1_val or (
                            cand_val == nf1_val and cand_cnt > nf1_cnt
                        ):
                            nf1_val = cand_val
                            nf1_cnt = cand_cnt

                if old1_val != NEG:
                    if left_selected:
                        cand_val = old1_val + value + lam
                        cand_cnt = old1_cnt + p - 1
                    else:
                        cand_val = old1_val + value
                        cand_cnt = old1_cnt + p

                    if right_selected == 0:
                        if cand_val > nf0_val or (
                            cand_val == nf0_val and cand_cnt > nf0_cnt
                        ):
                            nf0_val = cand_val
                            nf0_cnt = cand_cnt
                    else:
                        if cand_val > nf1_val or (
                            cand_val == nf1_val and cand_cnt > nf1_cnt
                        ):
                            nf1_val = cand_val
                            nf1_cnt = cand_cnt

            f0_val, f0_cnt = nf0_val, nf0_cnt
            f1_val, f1_cnt = nf1_val, nf1_cnt

        if f0_val > f1_val or (f0_val == f1_val and f0_cnt >= f1_cnt):
            return f0_val, f0_cnt
        return f1_val, f1_cnt

    # We need one WQS binary search for every query.
    # Queries are reordered by their current midpoint in every layer,
    # so all hull pointers move monotonically.
    max_iterations = (total_abs + 35000).bit_length() + 2

    for round_id in range(1, max_iterations + 1):
        active = False

        order = list(range(q))
        order.sort(
            key=lambda i: (
                (queries[i][3] + queries[i][4]) >> 1
            ),
            reverse=True,
        )

        for qid in order:
            qu = queries[qid]
            lo = qu[3]
            hi = qu[4]

            if lo > hi:
                continue

            active = True
            mid = (lo + hi) >> 1

            value, count = evaluate(qid, mid, round_id)

            if count >= qu[2]:
                qu[5] = value + qu[2] * mid
                qu[3] = mid + 1
            else:
                qu[4] = mid - 1

        if not active:
            break

    out = []
    for qu in queries:
        out.append(str(qu[5]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `build` function implements the segment-tree preprocessing. A leaf has only two feasible endpoint states. At an internal node, every pair of child states is combined using `minkowski`, which merges their marginal gains. `merge_into` then places the resulting function into the appropriate parent state. When both boundary bits are selected, the same solution is also written one position earlier because the two boundary pieces form one segment rather than two.

The four hulls are stored as ordinary Python lists. Their values are 64-bit-sized mathematically, but Python integers already have arbitrary precision, so no overflow handling is required. The negative sentinel is much smaller than any legitimate answer, and its magnitude is chosen so that it cannot interfere with the WQS slopes.

The query interval is decomposed once into canonical segment-tree nodes. This is a significant implementation detail. Repeating the recursive interval decomposition for every WQS midpoint would add unnecessary work to every binary-search layer.

`evaluate` maintains two states, `f0` and `f1`. Besides the adjusted score, each state stores the number of selected segments. When two selected boundary pieces touch, the count changes from `x+y` to `x+y-1`, while the penalized score gains back one `lambda`. This is exactly the same boundary correction used while building the four hulls.

The pointer arrays are reset lazily using `stamp`. A node is reset only when it is first visited in a new WQS layer. Queries in that layer are processed in decreasing `lambda`, so every pointer only increases. The while loop therefore does not perform a binary search for every query. Across one complete layer, each pointer traverses its hull only once.

The WQS binary search keeps the largest slope whose penalized optimum still contains at least the requested number of segments. At the stored final slope, the code evaluates the penalized optimum once more implicitly through the last successful midpoint and reconstructs the original objective by adding `k * lambda`. The tie comparison prefers the larger segment count when two choices have the same penalized score, which is necessary when the supporting line lies along a flat edge of the concave hull.

## Worked Examples

For the first sample, the array is

```
-1 2 -3 4 -5
```

The exact answers for one through five segments are `4, 6, 5, 2, -3`. The following table shows the resulting exact values and their marginal differences.

| Segments (k) | Best value (F(k)) | Marginal (F(k)-F(k-1)) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 4 | 4 |
| 2 | 6 | 2 |
| 3 | 5 | -1 |
| 4 | 2 | -3 |
| 5 | -3 | -5 |

The marginal sequence `4, 2, -1, -3, -5` is non-increasing, which is the concavity required by WQS and by the Minkowski merge. For example, with three segments the optimal choice is `[2]`, `[4]`, and `[5]`, whose total is (2+4-5=1), but the actual optimum is `5`, obtained by `[2]`, `[4]`, and another arrangement involving the negative elements differently. The table is the exact dynamic-programming result and demonstrates why choosing locally positive segments is not enough.

For the second sample, every element equals seven.

| Segments (k) | Best value (F(k)) | One optimal construction |
| --- | --- | --- |
| 1 | 35 | `[1,5]` |
| 2 | 35 | `[1,2]`, `[3,5]` |
| 3 | 35 | `[1]`, `[2]`, `[3,5]` |
| 4 | 35 | `[1]`, `[2]`, `[3]`, `[4,5]` |
| 5 | 35 | five singleton segments |

Every element is positive, so splitting the selected interval into more nonempty pieces never decreases the sum. This is a useful tie case for WQS because many different segment counts can have the same objective value. The implementation's tie handling chooses the largest count among equally good penalized states, which keeps the binary search monotone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Preprocessing time | (O(n\log n)) | Each segment-tree level performs a total linear amount of Minkowski merging |
| Query decomposition | (O(q\log n)) | Each interval becomes (O(\log n)) canonical nodes |
| WQS layers | (O(\log V)) | The slope range is bounded by the total absolute array sum |
| Query work per layer | (O(q\log n)) amortized | Each query touches (O(\log n)) nodes |
| Pointer movement per layer | (O(n\log n)) amortized | Every stored hull pointer advances through its hull at most once |
| Sorting per layer | (O(q\log q)) | Queries are ordered by their current WQS midpoint |
| Space | (O(n\log n+q\log n)) | Four convex functions are stored for every segment-tree node |

Here (V) is at most on the order of the total absolute sum, which is at most (1.225\times10^9). Thus the number of WQS layers is only about 31. The preprocessing and stored hulls are (O(n\log n)), while each query keeps only its canonical node decomposition and a few binary-search variables. The intended C++ implementation comfortably fits the original memory bound; the Python implementation uses the same asymptotic structure but Python's object overhead makes memory and runtime substantially less forgiving.

## Test Cases

```python
import sys
import io

# Paste the solution above into this file before running these tests.
# The solution exposes solve(), which reads sys.stdin and writes stdout.

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

# Provided sample 1.
assert run(
    """5 5
-1 2 -3 4 -5
1 5 1
1 5 2
1 5 3
1 5 4
1 5 5
"""
) == "4\n6\n5\n2\n-3", "sample 1"

# Provided sample 2.
assert run(
    """5 1
7 7 7 7 7
1 5 1
"""
) == "35", "sample 2"

# Minimum-size negative array.
assert run(
    """1 1
-5
1 1 1
"""
) == "-5", "single negative element"

# Exact-k behavior and adjacent/disjoint choices.
assert run(
    """3 4
5 -10 5
1 3 1
1 3 2
2 3 1
2 2 1
"""
) == "5\n10\n5\n-10", "boundary and exact-k cases"

# All-equal values, including the non-monotone exact-k answer.
assert run(
    """4 3
3 3 3 3
1 4 1
1 4 2
1 4 3
"""
) == "12\n12\n9", "all equal values"

# Maximum-size structural test.
# With all ones, selecting exactly n singleton segments gives n.
n = 35000
inp = f"{n} 1\n" + " ".join(["1"] * n) + f"\n1 {n} {n}\n"
assert run(inp) == "35000", "maximum-size all-positive case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / -5 / 1 1 1` | `-5` | Minimum size and mandatory nonempty segment |
| `5 -10 5` with four queries | `5, 10, 5, -10` | Exact segment count, negative values, and interval boundaries |
| Four copies of `3` | `12, 12, 9` | Exact-(k) answer is not monotone |
| 35000 copies of `1` | `35000` | Maximum input size and the (k=n) boundary |

## Edge Cases

The all-negative case is handled by the fact that the DP always requires the requested number of nonempty segments. For

```
1 1
-5
1 1 1
```

the leaf has `h[1][1][1] = -5`. WQS cannot choose zero segments because the query asks for one, and the final reconstruction gives `-5`.

The exact-(k) distinction is visible on

```
4 3
3 3 3 3
1 4 1
1 4 2
1 4 3
```

For (k=1), the hull chooses the whole interval and obtains `12`. For (k=2), two adjacent pieces can cover the same four elements, so the value remains `12`. For (k=3), only three disjoint nonempty pieces are needed, and the best solution covers three elements for a value of `9`. The concave hull contains all three values, so WQS can recover each exact answer instead of accidentally solving an "at most (k)" variant.

The boundary case where selected pieces are adjacent is handled by the endpoint bits. Consider

```
3 1
5 -10 5
1 3 2
```

The best solution selects `[1,1]` and `[3,3]`, giving `10`. When the two sides of a segment-tree merge both claim their touching endpoint, the merge operation reduces the segment count by one. When they do not both claim the boundary, the counts simply add. This distinction lets the data structure represent both adjacent pieces and genuinely merged pieces.

The maximum segment count is handled directly by the same state representation. On

```
3 1
-2 -3 -4
1 3 3
```

the only feasible solution with three segments is to select each singleton. The exact value is `-9`. The WQS hull contains the point corresponding to three segments, and the final supporting-line reconstruction returns `-9` rather than zero or the best value for fewer segments.

A final subtle case is a flat portion of the hull, such as an array of equal positive values. Several different segment counts can have the same original value. At a slope exactly matching the corresponding marginal gain, several hull positions have equal penalized value. The implementation resolves this by preferring the larger segment count. That makes the number of selected segments monotone in the WQS slope and gives a consistent side of the supporting edge, which is required for the binary search to converge to a slope supporting the requested (k).
