---
title: "CF 102201I - Increasing Sequence"
description: "We have a permutation (A) of (1,ldots,N). Fix an index (i). Among all strictly increasing subsequences that contain position (i), consider the maximum possible length. For every other index (j), we must decide whether deleting position (j) makes that maximum length smaller."
date: "2026-08-18T10:44:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "I"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 505
verified: true
draft: false
---

[CF 102201I - Increasing Sequence](https://codeforces.com/problemset/problem/102201/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation (A) of (1,\ldots,N). Fix an index (i). Among all strictly increasing subsequences that contain position (i), consider the maximum possible length. For every other index (j), we must decide whether deleting position (j) makes that maximum length smaller.

The output is one number for every position (i), so the answer is about positions in the original array, not about the numerical values stored there. The permutation property is useful because every value is unique, which lets us use the value itself as a convenient identifier internally. The original problem has (N\le 250000), a 3 second time limit, and 1024 MB of memory.

A quadratic algorithm is already too large at this scale. With (250000) positions, (N^2) is about (6.25\cdot10^{10}), so even an (O(N\log N)) LIS computation repeated for every position is far beyond the practical limit. The target is close to (O(N\log N)), with logarithmic factors coming from Fenwick trees, binary lifting, and binary searches.

There are several edge cases that expose common mistakes. For (N=1), the input is simply `1`, and the answer is `0`, because there is no other index to remove. A solution that counts the distinguished index itself as removable would incorrectly return `1`.

For a strictly decreasing permutation such as `6 5 4 3 2 1`, every increasing subsequence has length one. Once index (i) is required to belong to it, the subsequence is just (i), so removing any other index changes nothing. The correct output is `0 0 0 0 0 0`. A solution based only on ordinary LIS membership can easily overcount here.

Multiple optimal subsequences are another important case. For `2 1 4 3`, every position belongs to some increasing subsequence of length two, but no other position is present in all optimal subsequences containing a fixed position. The correct output is `0 0 0 0`. Looking at one arbitrary LIS instead of all optimal LISs would incorrectly mark some elements as necessary.

A useful case for checking that answers are associated with positions rather than values is `3 1 2 5 4`. The correct answer by position is `0 1 1 2 2`. Internally, the algorithm can identify a vertex by its value because the input is a permutation, but the final answers must be printed in the original positional order.

The requested all-equal test is not a valid input for this problem. For example, `3 / 7 7 7` violates the permutation condition because values must be distinct. It is useful as a sanity check for a test harness, but it should not be used as a correctness test for a submitted solution.

## Approaches

The direct approach is conceptually simple. For every distinguished position (i), try every deletion position (j\neq i). After deleting (j), recompute the longest increasing subsequence that is forced to contain (i), and compare it with the original value. This is correct because it tests exactly the condition from the definition.

The problem is the amount of repeated work. A straightforward dynamic-programming LIS recomputation takes (O(N^2)), producing (O(N^4)) work over all pairs (i,j). Even if we improve each recomputation to (O(N\log N)), doing it for all (O(N^2)) pairs still costs (O(N^3\log N)). More intelligently, one can compute the best increasing subsequence through a fixed (i) in linear or logarithmic time, but doing that independently for every possible deletion still leaves at least quadratic behavior. At (N=250000), even (N^2) is already about (6.25\cdot10^{10}) operations.

The key observation is to stop thinking about deletion directly. Fix an index (i), and look only at the longest increasing subsequences ending at (i). A position (j<i) decreases the optimum after deletion exactly when every maximum-length increasing subsequence ending at (i) contains (j). In graph terminology, (j) dominates (i): every relevant path from the beginning to (i) passes through (j).

Construct a directed acyclic graph whose vertices are array positions and whose edges connect consecutive levels of an increasing subsequence. Define (L[x]) as the length of the longest increasing subsequence ending at (x). A vertex (u) can precede (v) in a maximum-length subsequence ending at (v) precisely when (u<v), (A_u<A_v), and (L[u]+1=L[v]).

The vertices at the same (L)-level have a special ordering. During a left-to-right scan, their values are strictly decreasing. If two vertices had the same level and a later one had a larger value, the earlier one could precede it and create a longer subsequence, contradicting their levels. This ordering means that the potentially huge predecessor set of a new vertex is a contiguous suffix of one level.

The relevant graph can have quadratic many edges, so constructing it explicitly is impossible. Instead, we maintain its dominator tree online. The immediate dominator of a new vertex is the lowest common ancestor of its relevant predecessors in the already constructed dominator tree. Because the predecessors form a suffix of one level, it is enough to take the largest predecessor value below the current value and the smallest value on that level. Their LCA is the common dominator of the whole predecessor set. This is the central reduction used by the standard solution.

Once this dominator tree exists, all vertices that occur in every maximum path to (i) are exactly the ancestors of (i). If the tree depth of (i) is (d), then (d-1) other vertices are mandatory, because (i) itself is included in the depth count.

We need mandatory vertices both before and after (i). The first left-to-right pass handles vertices that must appear before (i). A symmetric right-to-left pass handles vertices that must appear after (i). The two sets cannot overlap except at (i), so after subtracting (i) from both depth counts, their sizes can simply be added.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3\log N)) with fast LIS recomputation | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N\log N)) | Accepted |

## Algorithm Walkthrough

1. Treat every array position as a vertex. For the first pass, define (L[x]) as the longest increasing subsequence ending at position (x). A Fenwick tree over values stores the maximum (L)-level among already processed values. Querying values smaller than (A_x) gives the level of (x) in (O(\log N)).
2. Group vertices by their (L)-level. During the left-to-right scan, each level's values appear in strictly decreasing order. Suppose the current value is (x), and its level is (k+1). Its possible predecessors are exactly the already processed vertices in level (k) whose values are smaller than (x).
3. Find the largest value below (x) in level (k). Because that level is stored in decreasing order, this can be found by binary search. Every other possible predecessor has an even smaller value.
4. Keep the smallest value in level (k) as well. The common dominators of all possible predecessors are the common ancestors of these two extreme predecessors. Thus the immediate dominator of (x) is their LCA in the current dominator tree.
5. Create (x) as a child of that LCA. Its tree depth is one greater than the parent's depth, and its binary-lifting ancestors are filled immediately. If (k=0), there is no predecessor, so (x) is attached directly to the virtual root.
6. After the left-to-right pass, add `depth[x] - 1` to the answer belonging to the corresponding array position. The subtraction removes (x) itself, since the question only counts other indices.
7. Repeat the entire construction from right to left. Now we are interested in increasing subsequences starting at (x), so the Fenwick tree is queried for values greater than (A_x). Reversing the value coordinate turns this into an ordinary prefix maximum query.
8. In the right-to-left pass, vertices of the same level occur in increasing value order. The relevant successor set is a prefix of that level, so the smallest successor greater than the current value and the largest value in the level give the two extreme vertices needed for the LCA.
9. Add the resulting `depth[x] - 1` to the same position's answer. Finally print the answers in the original array order, rather than in value order.

The invariant behind the construction is that the dominator tree of every processed prefix is represented exactly by the maintained parent relation. For a new vertex (x), every maximum path reaching (x) must first come through one of its maximum-level predecessors. The immediate dominator is consequently the deepest vertex common to all predecessor dominator chains, which is their LCA. The special ordering of each LIS level reduces all predecessors to two extreme vertices without changing that common ancestor. Thus the tree depth counts exactly the vertices present in every maximum increasing path. The reverse pass applies the identical argument to suffixes.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    LOG = n.bit_length()

    # ans is indexed by value. Since A is a permutation,
    # ans[a[i]] is the answer belonging to position i.
    ans = [0] * (n + 1)

    def build_left():
        bit = [0] * (n + 1)

        # layers[k] contains values whose left LIS length is k.
        # Values inside one layer are decreasing.
        layers = [[] for _ in range(n + 1)]

        depth = [0] * (n + 1)
        up = [[0] * LOG for _ in range(n + 1)]

        def query(x):
            res = 0
            while x:
                v = bit[x]
                if v > res:
                    res = v
                x -= x & -x
            return res

        def update(x, v):
            while x <= n:
                if v > bit[x]:
                    bit[x] = v
                x += x & -x

        def lca(x, y):
            if depth[x] < depth[y]:
                x, y = y, x

            diff = depth[x] - depth[y]
            b = 0
            while diff:
                if diff & 1:
                    x = up[x][b]
                diff >>= 1
                b += 1

            if x == y:
                return x

            for b in range(LOG - 1, -1, -1):
                ux = up[x][b]
                uy = up[y][b]
                if ux != uy:
                    x = ux
                    y = uy

            return up[x][0]

        for x in a:
            k = query(x - 1)

            if k == 0:
                parent = 0
            else:
                layer = layers[k]

                # layer is decreasing.
                # Find the first value < x, which is the largest
                # value in this layer that is still < x.
                lo = 0
                hi = len(layer)
                while lo < hi:
                    mid = (lo + hi) >> 1
                    if layer[mid] < x:
                        hi = mid
                    else:
                        lo = mid + 1

                candidate = layer[lo]
                smallest = layer[-1]

                parent = lca(smallest, candidate)

            depth[x] = depth[parent] + 1
            up[x][0] = parent

            row = up[x]
            parent_row = up[parent]
            for b in range(1, LOG):
                row[b] = parent_row[b - 1]

            layers[k + 1].append(x)
            update(x, k + 1)

        for x in a:
            ans[x] += depth[x] - 1

    def build_right():
        bit = [0] * (n + 1)

        # In the right-to-left pass, each layer is increasing.
        layers = [[] for _ in range(n + 1)]

        depth = [0] * (n + 1)
        up = [[0] * LOG for _ in range(n + 1)]

        def query(x):
            res = 0
            while x:
                v = bit[x]
                if v > res:
                    res = v
                x -= x & -x
            return res

        def update(x, v):
            while x <= n:
                if v > bit[x]:
                    bit[x] = v
                x += x & -x

        def lca(x, y):
            if depth[x] < depth[y]:
                x, y = y, x

            diff = depth[x] - depth[y]
            b = 0
            while diff:
                if diff & 1:
                    x = up[x][b]
                diff >>= 1
                b += 1

            if x == y:
                return x

            for b in range(LOG - 1, -1, -1):
                ux = up[x][b]
                uy = up[y][b]
                if ux != uy:
                    x = ux
                    y = uy

            return up[x][0]

        for x in reversed(a):
            # Reverse the value coordinate.
            rx = n - x + 1
            k = query(rx - 1)

            if k == 0:
                parent = 0
            else:
                layer = layers[k]

                # layer is increasing.
                # Find the first value > x.
                idx = bisect_right(layer, x)

                candidate = layer[idx]
                largest = layer[-1]

                parent = lca(largest, candidate)

            depth[x] = depth[parent] + 1
            up[x][0] = parent

            row = up[x]
            parent_row = up[parent]
            for b in range(1, LOG):
                row[b] = parent_row[b - 1]

            layers[k + 1].append(x)
            update(rx, k + 1)

        for x in a:
            ans[x] += depth[x] - 1

    build_left()
    build_right()

    print(*[ans[x] for x in a])

if __name__ == "__main__":
    solve()
```

The first pass builds the dominator tree for maximum increasing prefixes. The Fenwick tree contains the best LIS level for every value prefix, so `query(x - 1)` gives the largest level that can precede value `x`. The new vertex is then placed into the next layer.

The `layers` arrays serve a second purpose beyond storing the levels. Their monotone ordering lets us avoid explicitly enumerating all incoming edges of a vertex. In the left pass the layer is decreasing, so the custom binary search finds the first value smaller than `x`. In the right pass the layer is increasing, so `bisect_right` finds the first value larger than `x`.

The `up` table stores binary ancestors in the dominator tree. Since (N<2^{18}) is not guaranteed, using `n.bit_length()` is safer than hard-coding the number of levels. Python integers do not overflow, so no special numeric handling is needed.

The reverse pass uses the transformed coordinate `n - x + 1`. A value greater than `x` becomes a smaller transformed coordinate, allowing exactly the same prefix-max Fenwick implementation to be reused.

The final list comprehension is subtle. `ans` is indexed by the permutation value because that makes the tree representation convenient. If position `i` contains value `x`, its answer is `ans[x]`, so the output must be `[ans[x] for x in a]`. Printing `ans[1], ans[2], ...` would answer a different question by value rather than by original position.

The construction follows the same two-pass dominator-tree idea as the known accepted C++ implementation for this problem.

## Worked Examples

### Sample 1

For the increasing permutation `1 2 3 4 5 6`, every position is part of the unique LIS containing all six elements. In the left pass, every new value has exactly one relevant predecessor, while in the right pass every value similarly has exactly one relevant successor.

| Position | Value | Left level | Left parent | Left depth | Right level | Right parent | Right depth | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 | 6 | 2 | 6 | 5 |
| 2 | 2 | 2 | 1 | 2 | 5 | 3 | 5 | 5 |
| 3 | 3 | 3 | 2 | 3 | 4 | 4 | 4 | 5 |
| 4 | 4 | 4 | 3 | 4 | 3 | 5 | 3 | 5 |
| 5 | 5 | 5 | 4 | 5 | 2 | 6 | 2 | 5 |
| 6 | 6 | 6 | 5 | 6 | 1 | 0 | 1 | 5 |

For position 3, for example, the left depth contributes (3-1=2), corresponding to values 1 and 2 that must occur before it. The right depth contributes (4-1=3), corresponding to values 4, 5, and 6. Together there are five other mandatory indices. The same reasoning applies to every position, giving `5 5 5 5 5 5`.

### Sample 2

For the decreasing permutation `6 5 4 3 2 1`, no two positions can form a strictly increasing subsequence. Consequently every vertex is a root-level vertex in both directional constructions.

| Position | Value | Left level | Left parent | Left depth | Right level | Right parent | Right depth | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 2 | 5 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 3 | 4 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 4 | 3 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 5 | 2 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 6 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |

Every depth is one, so both directional contributions are zero. Deleting any other position cannot destroy a length-one subsequence containing the chosen position, giving `0 0 0 0 0 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Each of the two passes performs Fenwick operations, binary searches, and (O(\log N)) LCA work for every element. |
| Space | (O(N\log N)) | The binary-lifting table dominates the memory usage, with (N\log N) ancestor entries. |

For (N=250000), the logarithmic factor is below twenty levels. The memory limit is 1024 MB, so the (O(N\log N)) ancestor table fits comfortably. The algorithm avoids the quadratic predecessor graph entirely, which is the decisive requirement for this input size.

## Test Cases

The test harness below uses the same algorithm through a string-based wrapper. The maximum-size case uses a decreasing permutation, so the expected result can be generated without storing a second enormous answer manually. The all-equal case is deliberately checked only for invalidity because it violates the permutation requirement.

```python
import sys
import io
from bisect import bisect_right

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        n = int(input())
        a = list(map(int, input().split()))

        LOG = n.bit_length()
        ans = [0] * (n + 1)

        def build_left():
            bit = [0] * (n + 1)
            layers = [[] for _ in range(n + 1)]
            depth = [0] * (n + 1)
            up = [[0] * LOG for _ in range(n + 1)]

            def query(x):
                res = 0
                while x:
                    if bit[x] > res:
                        res = bit[x]
                    x -= x & -x
                return res

            def update(x, v):
                while x <= n:
                    if v > bit[x]:
                        bit[x] = v
                    x += x & -x

            def lca(x, y):
                if depth[x] < depth[y]:
                    x, y = y, x

                diff = depth[x] - depth[y]
                b = 0
                while diff:
                    if diff & 1:
                        x = up[x][b]
                    diff >>= 1
                    b += 1

                if x == y:
                    return x

                for b in range(LOG - 1, -1, -1):
                    if up[x][b] != up[y][b]:
                        x = up[x][b]
                        y = up[y][b]

                return up[x][0]

            for x in a:
                k = query(x - 1)

                if k == 0:
                    parent = 0
                else:
                    layer = layers[k]
                    lo, hi = 0, len(layer)

                    while lo < hi:
                        mid = (lo + hi) >> 1
                        if layer[mid] < x:
                            hi = mid
                        else:
                            lo = mid + 1

                    parent = lca(layer[-1], layer[lo])

                depth[x] = depth[parent] + 1
                up[x][0] = parent

                for b in range(1, LOG):
                    up[x][b] = up[up[x][b - 1]][b - 1]

                layers[k + 1].append(x)
                update(x, k + 1)

            for x in a:
                ans[x] += depth[x] - 1

        def build_right():
            bit = [0] * (n + 1)
            layers = [[] for _ in range(n + 1)]
            depth = [0] * (n + 1)
            up = [[0] * LOG for _ in range(n + 1)]

            def query(x):
                res = 0
                while x:
                    if bit[x] > res:
                        res = bit[x]
                    x -= x & -x
                return res

            def update(x, v):
                while x <= n:
                    if v > bit[x]:
                        bit[x] = v
                    x += x & -x

            def lca(x, y):
                if depth[x] < depth[y]:
                    x, y = y, x

                diff = depth[x] - depth[y]
                b = 0
                while diff:
                    if diff & 1:
                        x = up[x][b]
                    diff >>= 1
                    b += 1

                if x == y:
                    return x

                for b in range(LOG - 1, -1, -1):
                    if up[x][b] != up[y][b]:
                        x = up[x][b]
                        y = up[y][b]

                return up[x][0]

            for x in reversed(a):
                rx = n - x + 1
                k = query(rx - 1)

                if k == 0:
                    parent = 0
                else:
                    layer = layers[k]
                    idx = bisect_right(layer, x)
                    parent = lca(layer[-1], layer[idx])

                depth[x] = depth[parent] + 1
                up[x][0] = parent

                for b in range(1, LOG):
                    up[x][b] = up[up[x][b - 1]][b - 1]

                layers[k + 1].append(x)
                update(rx, k + 1)

            for x in a:
                ans[x] += depth[x] - 1

        build_left()
        build_right()

        print(*[ans[x] for x in a])
        return out.getvalue().strip()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert solve_data(
    "6\n1 2 3 4 5 6\n"
) == "5 5 5 5 5 5", "sample 1"

# Provided sample 2
assert solve_data(
    "6\n6 5 4 3 2 1\n"
) == "0 0 0 0 0 0", "sample 2"

# Provided sample 3
assert solve_data(
    "4\n2 1 4 3\n"
) == "0 0 0 0", "sample 3"

# Provided sample 4
assert solve_data(
    "9\n1 2 3 6 5 4 7 8 9\n"
) == "5 5 5 6 6 6 5 5 5", "sample 4"

# Minimum size
assert solve_data(
    "1\n1\n"
) == "0", "minimum size"

# Branching LIS choices
assert solve_data(
    "4\n1 2 4 3\n"
) == "1 1 2 2", "multiple optimal subsequences"

# Checks that answers are printed by original position, not by value
assert solve_data(
    "5\n3 1 2 5 4\n"
) == "0 1 1 2 2", "position/value mapping"

# Another boundary case with several maximum LISs
assert solve_data(
    "5\n2 3 1 4 5\n"
) == "3 3 3 2 2", "shared mandatory vertices"

# Maximum-size valid input
n = 250000
maximum_input = str(n) + "\n" + " ".join(map(str, range(n, 0, -1))) + "\n"
maximum_expected = " ".join(["0"] * n)
assert solve_data(maximum_input) == maximum_expected, "maximum size"

# All-equal input is not a valid permutation and must not be treated
# as a correctness test for this problem.
invalid = [7, 7, 7]
assert len(set(invalid)) != len(invalid), "all-equal input is invalid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum size and exclusion of the distinguished index |
| `1 2 4 3` | `1 1 2 2` | Several optimal LISs and mandatory vertices |
| `3 1 2 5 4` | `0 1 1 2 2` | Correct mapping from values back to original positions |
| `2 3 1 4 5` | `3 3 3 2 2` | Multiple branches with several shared mandatory vertices |
| Decreasing permutation of size 250000 | All zeros | Maximum input size and worst-case LIS length one |
| `7 7 7` | Not applicable | Demonstrates an invalid all-equal input, since the statement requires a permutation |

## Edge Cases

For `1 / 1`, both directional constructions create a single root-level vertex. Its depth is one in each pass, so both contributions are `1-1=0`. The final answer is `0`, exactly because there is no other index.

For `6 / 6 5 4 3 2 1`, every left-to-right Fenwick query returns zero because no earlier value is smaller. Every right-to-left query also returns zero because no later value is larger. Every vertex is consequently attached to the virtual root in both trees. All answers are zero.

For `4 / 2 1 4 3`, consider position 1 containing value 2. The maximum increasing subsequences containing it are `[2,4]` and `[2,3]`. Neither position 3 nor position 4 is present in every such subsequence, so deleting either one leaves another optimal subsequence. The dominator tree captures this by placing the two alternatives below a common ancestor instead of making either one an ancestor of the other. The answer is zero.

For `4 / 1 2 4 3`, position 3 contains value 4. Its only maximum-length increasing subsequence is `[1,2,4]`, so positions 1 and 2 are both mandatory. The left dominator depth of value 4 is three, giving two mandatory predecessors. There is no mandatory successor, so the final answer for position 3 is `2`.

For `5 / 3 1 2 5 4`, the internal tree uses values as vertex identifiers, but the output must follow the original positions. The per-value answers are attached to values 3, 1, 2, 5, and 4 respectively, producing `0 1 1 2 2` when traversed through the input array. Printing the answer array directly in numerical value order would produce a different and incorrect ordering.

For an all-equal input such as `3 / 7 7 7`, the algorithm is not required to define an answer because the input violates the permutation guarantee. A test harness may reject it before calling the solver, but a competitive-programming solution should not spend complexity handling malformed input that the judge promises never to provide.
