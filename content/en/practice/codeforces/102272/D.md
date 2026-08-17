---
title: "CF 102272D - C\u00e1nh \u0110\u1ed3ng Hoa"
description: "We have an array of (N) flower plots. Plot (i) initially contains (Ai) flowers, and the operations are processed in order. An update operation chooses an interval ([l,r]). At position (i) inside that interval, it adds exactly (i-l+1) flowers."
date: "2026-08-17T11:10:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "D"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 218
verified: false
draft: false
---

[CF 102272D - C\u00e1nh \u0110\u1ed3ng Hoa](https://codeforces.com/problemset/problem/102272/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of (N) flower plots. Plot (i) initially contains (A_i) flowers, and the operations are processed in order.

An update operation chooses an interval ([l,r]). At position (i) inside that interval, it adds exactly (i-l+1) flowers. Thus the added values form an arithmetic progression:

[
1,2,3,\ldots,r-l+1.
]

A query operation chooses ([u,v]) and asks for the current sum of flowers on that interval.

The difficult part is that an update is not a constant addition. For example, updating ([3,6]) adds (1,2,3,4), so the amount added depends linearly on the position:

[
i-l+1=i+(1-l).
]

That linear form is the key to the solution.

There are at most (10^5) plots and (10^5) operations in one test case, with up to four test cases. An (O(N)) operation would already lead to (10^{10}) work in the worst case, far beyond what a two-second limit allows. We need each update and query to take around (O(\log N)), giving roughly (10^5\log N) operations per test case.

The first boundary case is a one-element update. For example,

```
1
1
5
2
1 1 1
2 1 1
```

The update adds one flower, so the answer is

```
6
```

A careless implementation that treats the progression as starting with zero would produce (5).

The second boundary case is an update ending exactly at (N). For example,

```
1
5
0 0 0 0 0
2
1 2 5
2 1 5
```

The update adds (0,1,2,3,4) to positions (1,2,3,4,5), respectively, so the answer is

```
10
```

The third case is an update whose left endpoint is not (1). For

```
1
5
0 0 0 0 0
2
1 3 5
2 1 5
```

the additions are (0,0,1,2,3), giving

```
6
```

The expression must use the actual left endpoint (l). Replacing it with (i), or assuming every progression starts from position (1), gives a wrong result.

The fourth case is overlapping updates. For

```
1
4
0 0 0 0
3
1 1 3
1 2 4
2 1 4
```

the first update gives ([1,2,3,0]), the second gives ([1,3,5,3]), and the final answer is (12). Updates are additions, so they cannot overwrite the effects of earlier operations.

## Approaches

The direct approach stores the actual array. For an update ([l,r]), we simply loop from (l) to (r) and add (i-l+1) to every position. For a query ([u,v]), we loop over the interval and calculate its sum. This is correct because every operation is applied exactly to the positions it describes.

The problem is the amount of work. An update can touch all (N) positions, and a query can also inspect all (N) positions. With (Q=10^5) operations and (N=10^5), a sequence of full-range operations can require about

[
NQ=10^{10}
]

array accesses. That is several orders of magnitude too large.

The brute force works because it explicitly materializes every flower count. It fails because the updates have structure that we are throwing away.

The observation that unlocks the faster solution is that every update adds a linear function of the position. On ([l,r]),

[
i-l+1 = 1\cdot i +(1-l).
]

So instead of thinking about the update as (r-l+1) individual additions, we can think of it as adding the same linear function (ai+b) to an entire segment.

A segment tree with lazy propagation is a natural fit. For every tree node representing ([L,R]), we store the total flower count in that segment. Its lazy tag stores two numbers (a,b), meaning that every position (i) in this node still needs

[
ai+b
]

added to it.

Suppose the node covers ([L,R]). The total contribution of such a lazy update is

a\sum_{i=L}^{R}i+b(R-L+1).
]

The index sum has the closed form

\frac{(L+R)(R-L+1)}2.
]

So an entire segment can be updated in (O(1)) once the segment has been reached. Lazy propagation postpones pushing the linear function into its children until we actually need to inspect them.

For the original operation, we simply use

[
a=1,\qquad b=1-l.
]

The same segment tree can answer range sums in (O(\log N)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NQ)) | (O(N)) | Too slow |
| Optimal | (O((N+Q)\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the initial array. Each node stores the sum of flowers in its interval. The lazy information starts at zero because no deferred update exists initially.
2. Represent an update ([l,r]) as the linear function

[
f(i)=i-l+1=i+(1-l).
]

Thus its slope is (a=1), and its intercept is (b=1-l).

1. When a tree node ([L,R]) is completely covered by the update, increase its stored sum by

[
a\frac{(L+R)(R-L+1)}2+b(R-L+1).
]

At the same time, add (a) and (b) to the node's lazy tag. We do not visit its children because the whole interval has received the same linear function.

1. When an update partially intersects a node, first push the node's pending linear function to its children. Then recursively update the two children and recompute the current node's sum from their sums.

The push operation uses exactly the same formula as a normal update. A child covering ([L,R]) receives the pending function (ai+b), so its sum increases by the corresponding arithmetic-series sum.

1. For a range-sum query ([u,v]), return zero for a disjoint node and return the stored sum for a completely covered node. For a partial intersection, push the pending lazy function before querying the children, then add their results.
2. Process all (Q) operations in their original order. For type (1), apply the linear update. For type (2), query the required interval and print the result.

### Why it works

The invariant is that every segment-tree node's stored sum equals the true sum of the current array over that node's interval, including every update that has already reached the node. Its lazy pair ((a,b)) represents exactly the linear function that still has to be applied to every position in that node's interval and has already been included in the node's stored sum.

When a complete update reaches a node, the closed-form arithmetic sum adds precisely the contribution of the update to every position in that interval. When the lazy tag is pushed, the identical function is applied to both children, whose intervals partition the parent interval. Thus the invariant is preserved after every update.

A query either takes an already-correct complete node or recursively combines correct child sums. Since every queried position belongs to exactly the relevant disjoint tree nodes, the returned value is exactly the requested flower total.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        size = 4 * self.n + 5
        self.tree = [0] * size
        self.lazy_a = [0] * size
        self.lazy_b = [0] * size
        self.arr = arr
        self._build(1, 1, self.n)

    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left - 1]
            return

        mid = (left + right) // 2
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    @staticmethod
    def _index_sum(left, right):
        length = right - left + 1
        return (left + right) * length // 2

    def _apply(self, node, left, right, a, b):
        length = right - left + 1
        index_sum = self._index_sum(left, right)

        self.tree[node] += a * index_sum + b * length
        self.lazy_a[node] += a
        self.lazy_b[node] += b

    def _push(self, node, left, right):
        a = self.lazy_a[node]
        b = self.lazy_b[node]

        if a == 0 and b == 0:
            return

        if left != right:
            mid = (left + right) // 2
            self._apply(node * 2, left, mid, a, b)
            self._apply(node * 2 + 1, mid + 1, right, a, b)

        self.lazy_a[node] = 0
        self.lazy_b[node] = 0

    def update(self, ql, qr):
        self._update(1, 1, self.n, ql, qr)

    def _update(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return

        if ql <= left and right <= qr:
            # Add i - ql + 1 = i + (1 - ql).
            self._apply(node, left, right, 1, 1 - ql)
            return

        self._push(node, left, right)

        mid = (left + right) // 2
        self._update(node * 2, left, mid, ql, qr)
        self._update(node * 2 + 1, mid + 1, right, ql, qr)

        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, ql, qr):
        return self._query(1, 1, self.n, ql, qr)

    def _query(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0

        if ql <= left and right <= qr:
            return self.tree[node]

        self._push(node, left, right)

        mid = (left + right) // 2
        return (
            self._query(node * 2, left, mid, ql, qr)
            + self._query(node * 2 + 1, mid + 1, right, ql, qr)
        )

def solve():
    t = int(input())
    output = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        q = int(input())
        seg = SegmentTree(arr)

        for _ in range(q):
            typ, x, y = map(int, input().split())

            if typ == 1:
                seg.update(x, y)
            else:
                output.append(str(seg.query(x, y)))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The three main arrays in the tree have different roles. `tree[node]` stores the current flower sum for the node's interval. `lazy_a[node]` and `lazy_b[node]` store the deferred coefficients of a function (ai+b).

The `_apply` method is the central calculation. For a node covering ([L,R]), there are (R-L+1) positions and their indices sum to ((L+R)(R-L+1)/2). Hence adding (ai+b) changes the node sum by `a * index_sum + b * length`.

For a type (1) operation, the update is always slope (1) and intercept (1-l). The right endpoint (r) only determines which positions are covered. It does not appear in the function itself.

The lazy coefficients are added rather than replaced. If a node first receives (2i+3) and later receives (i-4), the combined pending operation is (3i-1). This is why `_apply` performs `+=` on both lazy arrays.

The query pushes pending updates before descending. Without that step, a child could still contain an old value even though its parent already includes the deferred update in its sum.

Python integers automatically grow beyond 64 bits, so there is no overflow issue. The maximum answers are large enough that fixed-width 32-bit arithmetic would be unsafe.

All positions in the implementation are one-based, matching the mathematical formulas. This makes the expression (i-l+1) directly usable and avoids an extra conversion inside every update.

The recursion depth is only (O(\log N)), but the recursion limit is raised anyway. The segment tree contains (O(N)) nodes, comfortably within the memory limit.

## Worked Examples

### Sample 1, first test case

The initial array is ([2,1,3,5,2]). The following table records the array after each update and the answer whenever a query occurs.

| Operation | Update added | Array after operation | Query answer |
| --- | --- | --- | --- |
| `1 1 3` | ([1,2,3,0,0]) | ([3,3,6,5,2]) |  |
| `2 3 5` | none | ([3,3,6,5,2]) | (6+5+2=13) |
| `1 4 5` | ([0,0,0,1,2]) | ([3,3,6,6,4]) |  |
| `1 2 5` | ([0,1,2,3,4]) | ([3,4,8,9,8]) |  |
| `1 1 1` | ([1,0,0,0,0]) | ([4,4,8,9,8]) |  |
| `2 1 4` | none | ([4,4,8,9,8]) | (4+4+8+9=25) |

For example, the update `[2,5]` is represented as (i-1). On a segment covering positions (2) through (5), its contribution is

[
(2-1)+(3-1)+(4-1)+(5-1)=1+2+3+4=10.
]

The tree does not need to visit those four positions individually.

### Sample 1, second test case

The second initial array is ([10,5,2,0,8,6,2]).

| Operation | Update added | Array after operation | Query answer |
| --- | --- | --- | --- |
| `1 2 5` | ([0,1,2,3,4,0,0]) | ([10,6,4,3,12,6,2]) |  |
| `1 1 6` | ([1,2,3,4,5,6,0]) | ([11,8,7,7,17,12,2]) |  |
| `2 4 7` | none | ([11,8,7,7,17,12,2]) | (7+17+12+2=38) |
| `1 1 3` | ([1,2,3,0,0,0,0]) | ([12,10,10,7,17,12,2]) |  |
| `1 5 5` | ([0,0,0,0,1,0,0]) | ([12,10,10,7,18,12,2]) |  |
| `1 1 5` | ([1,2,3,4,5,0,0]) | ([13,12,13,11,23,12,2]) |  |
| `2 1 7` | none | ([13,12,13,11,23,12,2]) | (86) |

The second trace exercises overlapping updates. The tree combines their lazy linear functions by addition, which is exactly what the array operation requires.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+Q\log N)) | Building the tree takes (O(N)), while every update and query visits (O(\log N)) tree levels. |
| Space | (O(N)) | The three segment-tree arrays each contain (O(N)) entries. |

With (N,Q\le 10^5), the dominant term is approximately (10^5\log_2(10^5)), which is around (1.7) million tree levels per test case. Even with several arithmetic operations at each visited node, this is far below the (10^{10}) operations required by the direct solution. The memory usage is linear and fits comfortably inside 256 MB.

## Test Cases

```python
import sys
import io

sys.setrecursionlimit(1_000_000)

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        size = 4 * self.n + 5
        self.tree = [0] * size
        self.lazy_a = [0] * size
        self.lazy_b = [0] * size
        self.arr = arr
        self._build(1, 1, self.n)

    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left - 1]
            return

        mid = (left + right) // 2
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    @staticmethod
    def _index_sum(left, right):
        length = right - left + 1
        return (left + right) * length // 2

    def _apply(self, node, left, right, a, b):
        length = right - left + 1
        index_sum = self._index_sum(left, right)
        self.tree[node] += a * index_sum + b * length
        self.lazy_a[node] += a
        self.lazy_b[node] += b

    def _push(self, node, left, right):
        a = self.lazy_a[node]
        b = self.lazy_b[node]

        if a == 0 and b == 0:
            return

        if left != right:
            mid = (left + right) // 2
            self._apply(node * 2, left, mid, a, b)
            self._apply(node * 2 + 1, mid + 1, right, a, b)

        self.lazy_a[node] = 0
        self.lazy_b[node] = 0

    def update(self, ql, qr):
        self._update(1, 1, self.n, ql, qr)

    def _update(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return

        if ql <= left and right <= qr:
            self._apply(node, left, right, 1, 1 - ql)
            return

        self._push(node, left, right)

        mid = (left + right) // 2
        self._update(node * 2, left, mid, ql, qr)
        self._update(node * 2 + 1, mid + 1, right, ql, qr)

        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, ql, qr):
        return self._query(1, 1, self.n, ql, qr)

    def _query(self, node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0

        if ql <= left and right <= qr:
            return self.tree[node]

        self._push(node, left, right)

        mid = (left + right) // 2
        return (
            self._query(node * 2, left, mid, ql, qr)
            + self._query(node * 2 + 1, mid + 1, right, ql, qr)
        )

def solve():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        q = int(input())

        seg = SegmentTree(arr)

        for _ in range(q):
            typ, x, y = map(int, input().split())
            if typ == 1:
                seg.update(x, y)
            else:
                ans.append(str(seg.query(x, y)))

    return "\n".join(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        result = solve()
        sys.stdout.write(result)

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
2
5
2 1 3 5 2
6
1 1 3
2 3 5
1 4 5
1 2 5
1 1 1
2 1 4
7
10 5 2 0 8 6 2
7
1 2 5
1 1 6
2 4 7
1 1 3
1 5 5
1 1 5
2 1 7
"""

assert run(sample) == "13\n25\n38\n86", "provided sample"

assert run("""\
1
1
5
2
1 1 1
2 1 1
""") == "6", "minimum size"

assert run("""\
1
5
0 0 0 0 0
3
1 2 5
2 1 5
2 5 5
""") == "10\n4", "right boundary"

assert run("""\
1
5
0 0 0 0 0
4
1 3 5
2 1 5
2 3 5
2 4 4
""") == "6\n6\n2", "left boundary"

assert run("""\
1
4
0 0 0 0
3
1 1 3
1 2 4
2 1 4
""") == "12", "overlapping updates"

# Maximum-size test. Every initial value is equal and the update covers N.
n = 100000
maximum_test = (
    "1\n"
    + str(n) + "\n"
    + ("1 " * n).strip() + "\n"
    + "3\n"
    + f"1 1 {n}\n"
    + f"2 1 {n}\n"
    + f"2 {n} {n}\n"
)

expected_total = n + n * (n + 1) // 2
expected_last = 2

assert run(maximum_test) == f"{expected_total}\n{expected_last}", \
    "maximum size and all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `N=1`, one update and one query | `6` | Minimum size and the first term of the progression |
| Zero array, update `[2,5]` | `10`, `4` | Right endpoint and exact progression values |
| Zero array, update `[3,5]` | `6`, `6`, `2` | Nonzero left endpoint and subrange queries |
| Two overlapping updates | `12` | Additive composition of updates |
| (N=100000), all values equal | `5000150000`, `2` | Maximum size, large sums, full-range update |

## Edge Cases

For the one-element case

```
1
1
5
2
1 1 1
2 1 1
```

the update has (a=1) and (b=0), because (1-l=0). The segment tree contains only the root, so the complete-cover case immediately adds (1). Its sum changes from (5) to (6), and the query returns (6). There is no child to push to, so the leaf condition is handled naturally.

For an update ending at the final position,

```
1
5
0 0 0 0 0
2
1 2 5
2 1 5
```

the lazy function is (i-1). The root is only partially covered, so the update descends until the covered nodes are found. The contribution over positions (2) through (5) is

[
1+2+3+4=10.
]

The final query returns (10). The right endpoint is handled only by the interval boundaries, so there is no special case for (r=N).

For a left endpoint other than one,

```
1
5
0 0 0 0 0
4
1 3 5
2 1 5
2 3 5
2 4 4
```

the update function is

[
i-3+1=i-2.
]

Thus positions (3,4,5) receive (1,2,3), giving a total of (6). The query `[3,5]` returns (6), while `[4,4]` returns (2). The intercept (1-l) is what makes the formula depend on the actual starting position.

For overlapping updates,

```
1
4
0 0 0 0
3
1 1 3
1 2 4
2 1 4
```

the first update is (i) on `[1,3]`, producing `[1,2,3,0]`. The second is (i-1) on `[2,4]`, producing an additional `[0,1,2,3]`. The final array is `[1,3,5,3]`, whose sum is (12). In the tree, overlapping lazy tags are added coefficient by coefficient, so the data structure represents exactly the combined effect of both operations.

The maximum-size test also checks arithmetic safety. With (N=100000), an all-one array followed by an update `[1,N]` produces a total of

5000150000.
]

This exceeds the signed 32-bit range, but Python integers represent it exactly. The segment tree therefore returns the correct value without any special overflow handling.
