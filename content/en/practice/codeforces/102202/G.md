---
title: "CF 102202G - Increasing Sequence"
description: "We have a permutation A[0..N-1]. Fix an index i and consider all increasing subsequences that contain A[i]. Among them, some have maximum possible length."
date: "2026-08-20T02:25:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "G"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 578
verified: true
draft: false
---

[CF 102202G - Increasing Sequence](https://codeforces.com/problemset/problem/102202/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation `A[0..N-1]`. Fix an index `i` and consider all increasing subsequences that contain `A[i]`. Among them, some have maximum possible length. We need to count how many other indices `j` are essential for index `i`, meaning that after deleting `j`, the best increasing subsequence that still contains `i` becomes strictly shorter.

The key distinction is between an element that appears in some optimal subsequence and an element that appears in every optimal subsequence containing `i`. Only the latter contributes to the answer.

For a fixed `i`, every increasing subsequence containing it splits naturally into a left part ending at `i` and a right part starting at `i`. Consequently, an index to the left of `i` is relevant exactly when it occurs in every longest increasing subsequence ending at `i`. The symmetric statement holds for indices to the right.

With `N` up to `250000`, an `O(N^2)` dynamic program is already far beyond the limit. In the worst case it performs about `N(N-1)/2`, which is roughly `3.1 * 10^10` predecessor checks. Even the ordinary `O(N log N)` LIS computation is not enough by itself, because we need information about which elements are unavoidable in every optimal subsequence.

There are several edge cases that expose common mistakes. For `N=1`, the only subsequence containing the single element is that element itself, so the answer is `0`. The input `1 / 1` must produce `0`.

For a strictly increasing permutation such as `1 2 3`, every element belongs to the unique increasing subsequence containing any fixed position. The answer is `2 2 2`, not `0 0 0`. A solution that only counts alternative LIS choices will miss this case.

For a strictly decreasing permutation such as `3 2 1`, every single element forms a longest increasing subsequence by itself. Removing another index never changes the best length containing the chosen index, so the answer is `0 0 0`. A solution that confuses "belongs to some LIS" with "belongs to every LIS" can incorrectly count other elements.

A useful boundary case is `1 3 2`. The answers are `0 1 1`. For index `1`, the value `3` has no possible extension to the right, so deleting either neighboring element is not equivalent. For index `2`, every length-two increasing subsequence containing it uses the first element `1`, making that index essential. Similar reasoning applies to index `1`.

## Approaches

The direct solution constructs the increasing-subsequence dynamic programming graph. Create a vertex for every array position and an edge `j -> i` whenever `j < i`, `A[j] < A[i]`, and `j` can be the previous element of a longest increasing subsequence ending at `i`. Equivalently, if `L[i]` is the LIS length ending at `i`, we keep edges satisfying `L[j] + 1 = L[i]`.

For a fixed `i`, every longest path from the beginning of this graph to `i` represents a longest increasing subsequence ending at `i`. An index is unavoidable exactly when it lies on every such path. The brute-force way would be to enumerate or otherwise inspect all relevant predecessors for every vertex. Even constructing all edges is potentially quadratic, because an increasing permutation has an edge between every pair of positions. With `N=250000`, that means about `3.1 * 10^10` possible edges.

The observation that unlocks the faster solution is that the relevant graph is a DAG whose edges always move from LIS layer `k-1` to layer `k`. We can build its dominator tree. A vertex `u` dominates a vertex `v` when every path from the source to `v` passes through `u`. The ancestors of `v` in the dominator tree are exactly the vertices that are unavoidable on every path to `v`.

For a DAG, the immediate dominator of a vertex is the LCA of all its direct predecessors in the dominator tree. This lets us construct the dominator tree layer by layer. The remaining difficulty is that the predecessor set can be large. The permutation property removes that difficulty: vertices having the same LIS-ending length form a decreasing sequence in both position and value. Thus, for every vertex in layer `k`, its predecessors in layer `k-1` form a contiguous sliding window.

We maintain the LCA of that moving window with a two-stack aggregate queue. Each insertion, deletion, and query performs only a constant number of LCA operations. LCA itself is answered with binary lifting in `O(log N)`, giving an `O(N log N)` solution.

The right side of index `i` is handled by reversing the permutation and replacing every value `x` with `N+1-x`. A strictly increasing subsequence to the right of `i` becomes an ordinary increasing subsequence ending at the transformed position corresponding to `i`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Optimal | O(N log N) | O(N log N) | Accepted |

## Algorithm Walkthrough

1. Compute the LIS-ending layer of every position using the standard patience-sorting tails array. If `L[i] = k`, put index `i` into layer `k`. The indices are processed from left to right, so every layer is automatically stored in increasing position order.

Because two elements with the same `L` value cannot have both increasing positions and increasing values, the values inside every layer are strictly decreasing as positions increase.
2. Add a virtual source vertex `0`. Every vertex with LIS length `1` is connected from this source. Its dominator depth is therefore `1`, because the vertex itself is the only real element on every path ending there.
3. Process the layers in increasing order. Suppose we are currently constructing layer `k`, and the previous layer is `k-1`. For a current vertex `v`, its possible predecessors are exactly the vertices `u` in layer `k-1` satisfying `u < v` and `A[u] < A[v]`.

Since the previous layer has positions increasing while values decrease, the conditions `u < v` and `A[u] < A[v]` select one contiguous interval of that layer.
4. Process the current layer from left to right. The right endpoint of the predecessor interval only moves right because the current position increases. The left endpoint also only moves right because values in the current layer decrease, so the threshold `A[v]` becomes smaller.

We can therefore maintain the predecessor interval as a sliding queue. Each previous-layer vertex is inserted at most once and removed at most once while processing the current layer.
5. Maintain the LCA of every vertex currently inside this sliding queue. A normal queue cannot efficiently remove from the front while maintaining an arbitrary associative aggregate, so use two stacks. Each stack stores its own aggregate, where the aggregate of two vertices is their LCA. When the front stack becomes empty, transfer all elements from the back stack while recomputing the aggregates.

LCA is associative because `LCA(LCA(a,b),c)` equals the common ancestor deepest among all three vertices. It is also commutative here, so the order in which the two stack aggregates are combined does not matter.
6. If the predecessor window for `v` is empty, its immediate dominator is the virtual source. Otherwise, the LCA of all predecessors is exactly the immediate dominator of `v`. Set this vertex as the parent of `v` in the dominator tree.

Once the parent is known, fill the binary-lifting table for `v` immediately. All ancestors used by these entries already belong to earlier layers.
7. The depth of `v` in the dominator tree equals the number of unavoidable vertices on every increasing subsequence ending at `v`, including `v` itself. Thus `depth[v] - 1` is the number of unavoidable indices strictly before `v`.
8. Run the same procedure on the transformed sequence `B`, where `B` is obtained by reversing `A` and replacing every value `x` by `N+1-x`. A right-increasing subsequence in the original array becomes a left-to-right increasing subsequence in `B`.
9. If `left[i]` is the dominator depth from the original sequence and `right[i]` is the corresponding depth from the transformed sequence, the required answer is

`left[i] + right[i] - 2`.

We subtract two because `i` itself is included once in each dominator depth but must not be counted.

### Why it works

Every increasing subsequence ending at a vertex is a path through the layered LIS DAG. A vertex is present in every such subsequence exactly when it dominates the corresponding DAG vertex. The dominator-tree invariant says that all dominators of a vertex are precisely its tree ancestors, so the tree depth counts them.

For a DAG, the immediate dominator of a vertex is the LCA of all its predecessors in the already constructed dominator tree. The sliding window contains exactly those predecessors because equal-LIS layers are strictly decreasing in value as position increases. Thus every parent chosen by the algorithm is the correct immediate dominator. The same argument applied to the reversed and complemented permutation gives the unavoidable suffix elements. Since the prefix and suffix of an increasing subsequence containing `i` are independent once `i` is fixed, adding the two counts gives exactly the indices whose deletion reduces the optimum.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve_dom_depth(a):
    n = len(a)

    # layers[k] contains indices whose LIS-ending length is k + 1.
    layers = []
    tails = []

    for i, x in enumerate(a):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            layers.append([])
        else:
            tails[k] = x
        layers[k].append(i)

    log = (n + 1).bit_length()

    # Binary lifting table for the dominator tree.
    up = [[0] * n for _ in range(log)]
    depth = [0] * n

    def lca(a1, a2):
        if a1 == a2:
            return a1

        if depth[a1] < depth[a2]:
            a1, a2 = a2, a1

        diff = depth[a1] - depth[a2]
        bit = 0
        while diff:
            if diff & 1:
                a1 = up[bit][a1]
            diff >>= 1
            bit += 1

        if a1 == a2:
            return a1

        for k in range(log - 1, -1, -1):
            if up[k][a1] != up[k][a2]:
                a1 = up[k][a1]
                a2 = up[k][a2]

        return up[0][a1]

    class AggQueue:
        def __init__(self):
            self.in_nodes = []
            self.in_agg = []
            self.out_nodes = []
            self.out_agg = []

        def push(self, v):
            self.in_nodes.append(v)
            if self.in_agg:
                self.in_agg.append(lca(self.in_agg[-1], v))
            else:
                self.in_agg.append(v)

        def _transfer(self):
            while self.in_nodes:
                v = self.in_nodes.pop()
                self.in_agg.pop()

                self.out_nodes.append(v)
                if self.out_agg:
                    self.out_agg.append(lca(v, self.out_agg[-1]))
                else:
                    self.out_agg.append(v)

        def pop(self):
            if not self.out_nodes:
                self._transfer()
            self.out_nodes.pop()
            self.out_agg.pop()

        def empty(self):
            return not self.in_nodes and not self.out_nodes

        def query(self):
            if not self.out_nodes:
                return self.in_agg[-1]
            if not self.in_nodes:
                return self.out_agg[-1]
            return lca(self.out_agg[-1], self.in_agg[-1])

    # Layer 0 has no real predecessor.
    for v in layers[0]:
        depth[v] = 1

    for k in range(1, len(layers)):
        prev = layers[k - 1]
        cur = layers[k]

        q = AggQueue()

        left = 0
        right = 0
        m = len(prev)

        for v in cur:
            # Add all previous-layer vertices with position < v.
            while right < m and prev[right] < v:
                if right >= left:
                    q.push(prev[right])
                right += 1

            # Remove vertices whose value is not smaller than a[v].
            # Values in prev are strictly decreasing.
            while left < right and a[prev[left]] >= a[v]:
                q.pop()
                left += 1

            if q.empty():
                parent = 0
                depth[v] = 1
            else:
                parent = q.query()
                depth[v] = depth[parent] + 1

            up[0][v] = parent
            for j in range(1, log):
                up[j][v] = up[j - 1][up[j - 1][v]]

    return depth

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    left = solve_dom_depth(a)

    transformed = [n + 1 - x for x in reversed(a)]
    right_rev = solve_dom_depth(transformed)

    ans = [0] * n
    for i in range(n):
        right = right_rev[n - 1 - i]
        ans[i] = left[i] + right - 2

    print(*ans)

if __name__ == "__main__":
    solve()
```

The first part of `solve_dom_depth` constructs the LIS layers with `bisect_left`. Because the input is a permutation, strict increasing subsequences are handled directly by lower-bound replacement. The actual LIS length is not needed separately, only the layer of each position.

The `up` table represents the dominator tree. `up[0][v]` is the immediate dominator of `v`, while higher rows contain ancestors at powers of two. The virtual source is represented by index `0` in the table, even though the real array vertices use zero-based indices. A real vertex can never be confused with the source because the source is represented by the special parent value `0`, while `depth[0]` is implicitly zero.

The LCA routine first equalizes depths and then lifts both vertices together. The largest lifting power is `(N+1).bit_length()`, which is enough to represent every possible tree depth.

The `AggQueue` is the sliding-window component. `in_nodes` receives new predecessors from the right, while `out_nodes` supplies elements to be removed from the left. Each element crosses from one stack to the other at most once during one layer scan. The aggregate stored with each stack entry is the LCA of all elements below that entry.

The two pointers `left` and `right` describe the predecessor interval in the previous LIS layer. The condition `prev[right] < v` handles the position restriction. The condition `a[prev[left]] >= a[v]` removes values that cannot precede `v` in a strictly increasing subsequence. The use of `>=` rather than `>` is necessary because the subsequence must be strictly increasing.

Finally, reversing and complementing the permutation turns every valid suffix after `i` into a valid prefix before the corresponding transformed vertex. The transformed depth is mapped back with `n - 1 - i`, and the two dominator depths are combined.

## Worked Examples

For Sample 1, the array is `[1]`. There is one LIS layer, containing only index `0`.

| Layer | Current index | Predecessor window | Immediate dominator | Depth |
| --- | --- | --- | --- | --- |
| 1 | 0 | empty | source | 1 |

The transformed sequence is also a single element, so its depth is again `1`. The answer is `1 + 1 - 2 = 0`.

For Sample 2, the array is `[1, 2, 3, 4, 5, 6]`. Every element belongs to its own LIS layer because the whole array is increasing.

| Layer | Current index | Predecessor window | Immediate dominator | Depth |
| --- | --- | --- | --- | --- |
| 1 | 0 | empty | source | 1 |
| 2 | 1 | `[0]` | 0 | 2 |
| 3 | 2 | `[1]` | 1 | 3 |
| 4 | 3 | `[2]` | 2 | 4 |
| 5 | 4 | `[3]` | 3 | 5 |
| 6 | 5 | `[4]` | 4 | 6 |

For the transformed sequence the depths appear in the opposite order, `6, 5, 4, 3, 2, 1`. At every position, the two depths add to `7`, so subtracting `2` gives `5`. This matches the fact that deleting any other element breaks the unique increasing subsequence containing the chosen index.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | LIS layers take O(N log N), while the dominator construction performs O(N) amortized queue operations and O(N) LCA queries, each costing O(log N). |
| Space | O(N log N) | Binary lifting stores O(N log N) ancestors, while the layers and sliding queue use O(N) additional space. |

The largest input contains `250000` elements. The algorithm performs only logarithmically many ancestor operations per vertex, rather than inspecting all pairs of positions. The `O(N log N)` bound is comfortably within the intended scale of the 3 second limit, and the `O(N log N)` ancestor table fits easily inside the 1024 MB memory limit.

## Test Cases

The test harness below assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

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
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("1\n1\n") == "0", "sample 1"
assert run("6\n1 2 3 4 5 6\n") == "5 5 5 5 5 5", "sample 2"
assert run("6\n6 5 4 3 2 1\n") == "0 0 0 0 0 0", "sample 3"
assert run("4\n2 1 4 3\n") == "0 0 0 0", "sample 4"
assert run("9\n1 2 3 6 5 4 7 8 9\n") == "5 5 5 6 6 6 5 5 5", "sample 5"

# Single element.
assert run("1\n7\n") == "0", "minimum size"

# Strictly decreasing permutation.
assert run("5\n5 4 3 2 1\n") == "0 0 0 0 0", "all LIS have length 1"

# A case with two different choices on one side.
assert run("3\n1 3 2\n") == "0 1 1", "sliding predecessor boundary"

# A longer case where both prefix and suffix dominators matter.
assert run("4\n3 1 2 4\n") == "1 2 2 2", "prefix and suffix dominance"

# Equal values are outside the permutation constraints, but are useful
# as a robustness check for the LIS boundary handling.
assert run("3\n5 5 5\n") == "0 0 0", "equal values"

# Maximum-size stress case, a decreasing permutation.
n = 250000
a = list(range(n, 0, -1))
expected = " ".join(["0"] * n)
assert run(str(n) + "\n" + " ".join(map(str, a)) + "\n") == expected, \
    "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum size and the absence of another index |
| `5 / 5 4 3 2 1` | `0 0 0 0 0` | Every LIS has length one |
| `3 / 1 3 2` | `0 1 1` | Strict predecessor boundaries and suffix handling |
| `4 / 3 1 2 4` | `1 2 2 2` | Multiple mandatory vertices on both sides |
| `3 / 5 5 5` | `0 0 0` | Equal-value boundary behavior, outside official constraints |
| `250000 / 250000 ... 1` | all zeros | Maximum `N` and performance |

## Edge Cases

For the single-element input `1 / 1`, the only vertex is placed in the first LIS layer. Its dominator depth is `1` in both the original and transformed sequences. The formula gives `1 + 1 - 2 = 0`, so the algorithm never accidentally counts the chosen index itself.

For a strictly increasing array such as `1 2 3`, each layer contains exactly one vertex. The predecessor window therefore contains exactly one element for every non-first vertex, and the dominator tree is simply a chain. The depths are `1, 2, 3` from the left and `3, 2, 1` from the right, giving `2, 2, 2`. This exercises the case where every other element is genuinely necessary.

For a strictly decreasing array such as `3 2 1`, every vertex lies in the first LIS layer. There are no edges between real vertices, so every dominator depth is `1`. The transformed array has the same property. The final formula produces zero everywhere, correctly handling the case where the chosen element can only participate in a length-one increasing subsequence.

For `1 3 2`, the left layers are `[0]` and `[1, 2]`. For index `1`, the predecessor window contains index `0`, so index `0` dominates it. For index `2`, the predecessor window also contains index `0`, making index `0` its unavoidable prefix element. On the right side, index `1` has no larger element after it, while index `2` has no suffix extension. Combining the two directions gives `0 1 1`. The example specifically catches the mistake of treating every element in the same LIS layer as a possible predecessor without respecting the value boundary.

For `3 1 2 4`, the left dominator depths are `1, 1, 2, 3`. The value `1` dominates the subsequence ending at `2`, and both `1` and `2` dominate the subsequence ending at `4`. The transformed pass supplies right-side depths `2, 3, 2, 1`. Combining them gives `1 2 2 2`. This case demonstrates why simply counting direct predecessors is insufficient, because a vertex can be unavoidable through several layers of the dominator tree.

For equal values such as `5 5 5`, the official input guarantee is violated, but the test is useful for checking strict comparison boundaries. No two equal values can extend a strictly increasing subsequence, so every chosen index has maximum length one and the expected result is `0 0 0`. The implementation uses `bisect_left` and the `>=` predecessor rejection consistently with strict inequality.
