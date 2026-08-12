---
title: "CF 102341A - Alakazam"
description: "We have an array of spoon counts, where position i initially contains a[i]. A shuffle l r operation takes every value currently located in the interval [l, r] and randomly permutes those values among the same positions."
date: "2026-08-13T03:02:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "A"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 643
verified: true
draft: false
---

[CF 102341A - Alakazam](https://codeforces.com/problemset/problem/102341/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of spoon counts, where position `i` initially contains `a[i]`. A `shuffle l r` operation takes every value currently located in the interval `[l, r]` and randomly permutes those values among the same positions. A `get i` operation asks for the expected value at position `i` after all previous shuffles.

The central difficulty is that the actual permutation is random, so we cannot maintain one concrete array. We need to maintain the expected value at every position. A shuffle does not preserve the expected value of an individual position, but it does preserve the total sum of the whole shuffled interval.

With `n, q <= 250000`, an approach that scans an entire interval for every operation can require roughly `nq`, which is about `6.25 * 10^10` element operations in the worst case. That is far beyond what a 2-second competitive programming limit can support. We need every operation to touch only logarithmically many data structure nodes.

There are several boundary cases where a direct implementation can silently go wrong. If the shuffled interval contains only one position, for example

```
1 2
7
shuffle 1 1
get 1
```

the answer is `7.000000000000`. A careless implementation that treats every shuffle as changing the value could introduce an unnecessary rounding or averaging operation, although mathematically the interval average is still exactly `7`.

A more revealing case is a shuffle of the entire array:

```
3 2
1 2 6
shuffle 1 3
get 2
```

The answer is `3.000000000000`, because every position is equally likely to receive each of the three values. Looking only at the value originally at position `2` would incorrectly produce `2`.

Another common boundary error is forgetting that the endpoints are inclusive:

```
3 2
1 2 9
shuffle 1 2
get 2
```

The expected value is `1.500000000000`. Position `3` is untouched, while positions `1` and `2` both become averages of `1` and `2`. An implementation that accidentally uses `[l, r)` would leave position `2` unchanged and return `2`.

Repeated overlapping shuffles are another case where storing only the original array is insufficient:

```
3 4
1 2 3
shuffle 1 2
shuffle 2 3
get 1
get 3
```

The answers are `1.500000000000` and `2.250000000000`. The second shuffle must use the expected values produced by the first shuffle, not the original values `2` and `3`.

## Approaches

The brute-force approach is straightforward. Maintain the current expected value of every position. For `shuffle l r`, compute the sum of the expected values from `l` through `r`, divide by `r-l+1`, and write that average into every position of the interval. For `get i`, simply print the current value at position `i`.

This is correct because after a uniform random permutation of the values in `[l,r]`, every position in that interval has the same probability of receiving every value. If the current expected values are `E_l, E_{l+1}, ..., E_r`, linearity of expectation gives the new expectation at every position as

[
\frac{E_l+E_{l+1}+\cdots+E_r}{r-l+1}.
]

The problem is the cost. A shuffle can contain `250000` positions, and in the worst case all `250000` operations can be shuffles of the entire array. Updating every position then takes about

[
250000 \times 250000 = 62,500,000,000
]

position updates, even before accounting for computing the sums.

The observation that removes this bottleneck is that after a shuffle, the entire interval has one common expected value. We do not need to remember the individual expected values inside that interval once the shuffle has happened. We only need the interval's sum before the shuffle, then we can lazily mark the whole interval as having one constant value.

This is exactly a range assignment combined with a range sum query. A lazy segment tree can represent both operations in `O(log n)`. Each tree node stores the sum of its interval and, when necessary, a lazy assignment saying that every position in the interval currently has the same expected value.

The brute-force method works because it explicitly performs the same range assignment that the mathematics requires, but it materializes every individual assignment. The segment tree keeps that assignment compressed inside tree nodes. A whole interval can be represented by one number instead of rewriting all of its positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nq)` | `O(n)` | Too slow |
| Optimal | `O((n+q) log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the initial array. Each node stores the sum of the expected values in its interval. Initially, these are just the original spoon counts.
2. Add a lazy assignment value to every segment tree node. If a node has a lazy value `x`, it means every position represented by that node currently has expected value `x`. We use `None` to mean that there is no pending uniform assignment.
3. For `shuffle l r`, first query the sum of the interval `[l,r]`. Let this sum be `S`, and let the interval length be `len = r-l+1`. The expected value after the random permutation is `S / len`.
4. Assign this average to the entire interval `[l,r]` using lazy propagation. For a fully covered tree node representing `k` positions, its sum becomes `average * k`, and its lazy assignment becomes `average`.
5. For `get i`, descend through the segment tree to the leaf representing position `i`. Whenever a node has a pending lazy assignment, propagate it to its children before descending. The leaf then contains the exact expected value requested.
6. Print every answer with enough decimal digits. Printing twelve digits after the decimal point is more than sufficient for the required `1e-9` absolute or relative error.

### Why it works

The invariant is that every segment tree node stores the exact sum of the expected values of all positions in its interval, while a lazy assignment records that every position in that interval has the same expected value.

Consider a shuffle of `[l,r]`. Before the shuffle, let the expected value at position `j` be `E_j`. Every permutation gives every original position in the interval the same probability of appearing at any target position. Consequently, the new expected value at every target position is

[
\frac{\sum_{j=l}^{r} E_j}{r-l+1}.
]

The segment tree computes exactly this sum, then assigns exactly this average to the whole interval. Thus the invariant remains true after every shuffle. A point query follows the assignments affecting its path and returns the expected value represented by the leaf, so every `get` answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(float, input().split()))

    size = 4 * n + 5
    tree = [0.0] * size
    lazy = [None] * size

    def build(node, left, right):
        if left == right:
            tree[node] = a[left]
            return

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1

        build(lc, left, mid)
        build(rc, mid + 1, right)
        tree[node] = tree[lc] + tree[rc]

    def apply(node, left, right, value):
        tree[node] = value * (right - left + 1)
        lazy[node] = value

    def push(node, left, right):
        value = lazy[node]
        if value is None or left == right:
            return

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1

        apply(lc, left, mid, value)
        apply(rc, mid + 1, right, value)
        lazy[node] = None

    def range_sum(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return tree[node]

        push(node, left, right)

        mid = (left + right) >> 1
        result = 0.0

        if ql <= mid:
            result += range_sum(node << 1, left, mid, ql, qr)

        if qr > mid:
            result += range_sum(node << 1 | 1, mid + 1, right, ql, qr)

        return result

    def range_assign(node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            apply(node, left, right, value)
            return

        push(node, left, right)

        mid = (left + right) >> 1

        if ql <= mid:
            range_assign(node << 1, left, mid, ql, qr, value)

        if qr > mid:
            range_assign(node << 1 | 1, mid + 1, right, ql, qr, value)

        tree[node] = tree[node << 1] + tree[node << 1 | 1]

    def point_query(node, left, right, pos):
        if left == right:
            return tree[node]

        push(node, left, right)

        mid = (left + right) >> 1

        if pos <= mid:
            return point_query(node << 1, left, mid, pos)

        return point_query(node << 1 | 1, mid + 1, right, pos)

    build(1, 0, n - 1)

    output = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == "shuffle":
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1

            total = range_sum(1, 0, n - 1, l, r)
            average = total / (r - l + 1)

            range_assign(1, 0, n - 1, l, r, average)

        else:
            pos = int(parts[1]) - 1
            answer = point_query(1, 0, n - 1, pos)
            output.append(f"{answer:.12f}")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The `tree` array contains interval sums. For a leaf, the sum is simply the expected value at that position. For an internal node, the sum is the sum of its two children.

The `lazy` array represents a pending range assignment. If `lazy[node]` is `x`, every position in that node's interval has expected value `x`. Its sum is consequently `x * interval_length`. A single assignment value can represent an entire subtree, which is the compression that makes the solution fast.

The `range_sum` function is used only to obtain the sum before a shuffle. It does not modify the values conceptually, although it may push a lazy assignment downward so that the recursive traversal sees the correct child sums.

The `range_assign` function performs the actual effect of a shuffle. On a fully covered node it does not visit the children at all. It changes the node's sum and records the assignment lazily. Partial overlap requires pushing the parent's assignment first, because the children must receive the parent's current value before one of them is modified further.

The `point_query` function only follows one root-to-leaf path. It pushes lazy assignments on that path, so the leaf always represents the latest expected value for the requested position.

All input indices are converted from one-based indexing to zero-based indexing exactly once when a query is read. The interval length is still computed as `r - l + 1`, because both endpoints are included.

Python integers would have no overflow issue for sums, but the tree stores floating-point expectations because division is required after every shuffle. The values are bounded by the initial range of values, since an average never leaves the minimum and maximum of the values being averaged. Printing twelve digits after the decimal point gives sufficient precision for the required tolerance.

## Worked Examples

The provided sample starts with `[1, 2, 3]`.

| Operation | Interval | Sum before shuffle | Average assigned | Expected values after operation |
| --- | --- | --- | --- | --- |
| `get 1` | `1` | `1` | `1` | `[1, 2, 3]` |
| `get 3` | `3` | `3` | `3` | `[1, 2, 3]` |
| `shuffle 1 2` | `[1,2]` | `3` | `1.5` | `[1.5, 1.5, 3]` |
| `shuffle 2 3` | `[2,3]` | `4.5` | `2.25` | `[1.5, 2.25, 2.25]` |
| `get 1` | `1` | `1.5` | `1.5` | `[1.5, 2.25, 2.25]` |
| `get 3` | `3` | `2.25` | `2.25` | `[1.5, 2.25, 2.25]` |

The first shuffle replaces the expectations at positions `1` and `2` by `(1+2)/2 = 1.5`. The second shuffle must use `1.5` as the expectation at position `2`, so its average is `(1.5+3)/2 = 2.25`. This demonstrates why updates must operate on the current expected values rather than the original array.

Consider a second example:

```
4 6
10 20 30 40
shuffle 1 4
get 1
get 4
shuffle 2 3
get 2
get 3
```

| Operation | Interval | Sum before shuffle | Average assigned | Expected values after operation |
| --- | --- | --- | --- | --- |
| `shuffle 1 4` | `[1,4]` | `100` | `25` | `[25,25,25,25]` |
| `get 1` | `1` | `25` | `25` | `[25,25,25,25]` |
| `get 4` | `4` | `25` | `25` | `[25,25,25,25]` |
| `shuffle 2 3` | `[2,3]` | `50` | `25` | `[25,25,25,25]` |
| `get 2` | `2` | `25` | `25` | `[25,25,25,25]` |
| `get 3` | `3` | `25` | `25` | `[25,25,25,25]` |

The first shuffle assigns the same expectation to the entire array. The second shuffle has no visible effect because the interval already has a uniform expected value. This exercises the case where lazy assignments cover large portions of the tree repeatedly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n+q) log n)` | Building the tree costs `O(n)`, and every shuffle performs one range sum and one range assignment, each `O(log n)`. Every `get` is a point query in `O(log n)`. |
| Space | `O(n)` | The segment tree stores a constant amount of information for each tree node, so its size is linear in `n`. |

With `n` and `q` both at most `250000`, the algorithm performs only logarithmically many segment tree operations per query. The tree height is about 18, so the total number of visited nodes remains manageable, unlike the `O(nq)` brute-force simulation.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(float, input().split()))

    size = 4 * n + 5
    tree = [0.0] * size
    lazy = [None] * size

    def build(node, left, right):
        if left == right:
            tree[node] = a[left]
            return

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1
        build(lc, left, mid)
        build(rc, mid + 1, right)
        tree[node] = tree[lc] + tree[rc]

    def apply(node, left, right, value):
        tree[node] = value * (right - left + 1)
        lazy[node] = value

    def push(node, left, right):
        value = lazy[node]
        if value is None or left == right:
            return

        mid = (left + right) >> 1
        lc = node << 1
        rc = lc | 1

        apply(lc, left, mid, value)
        apply(rc, mid + 1, right, value)
        lazy[node] = None

    def range_sum(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return tree[node]

        push(node, left, right)
        mid = (left + right) >> 1
        result = 0.0

        if ql <= mid:
            result += range_sum(node << 1, left, mid, ql, qr)

        if qr > mid:
            result += range_sum(node << 1 | 1, mid + 1, right, ql, qr)

        return result

    def range_assign(node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            apply(node, left, right, value)
            return

        push(node, left, right)
        mid = (left + right) >> 1

        if ql <= mid:
            range_assign(node << 1, left, mid, ql, qr, value)

        if qr > mid:
            range_assign(node << 1 | 1, mid + 1, right, ql, qr, value)

        tree[node] = tree[node << 1] + tree[node << 1 | 1]

    def point_query(node, left, right, pos):
        if left == right:
            return tree[node]

        push(node, left, right)
        mid = (left + right) >> 1

        if pos <= mid:
            return point_query(node << 1, left, mid, pos)

        return point_query(node << 1 | 1, mid + 1, right, pos)

    build(1, 0, n - 1)

    output = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == "shuffle":
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1
            total = range_sum(1, 0, n - 1, l, r)
            average = total / (r - l + 1)
            range_assign(1, 0, n - 1, l, r, average)
        else:
            pos = int(parts[1]) - 1
            output.append(f"{point_query(1, 0, n - 1, pos):.12f}")

    sys.stdout.write("\n".join(output))

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

def close_enough(actual: str, expected: str) -> bool:
    a = [float(x) for x in actual.split()]
    b = [float(x) for x in expected.split()]

    if len(a) != len(b):
        return False

    return all(abs(x - y) <= 1e-9 * max(1.0, abs(y)) for x, y in zip(a, b))

sample1 = """\
3 6
1 2 3
get 1
get 3
shuffle 1 2
shuffle 2 3
get 1
get 3
"""

assert close_enough(
    run(sample1),
    """\
1.000000000000
3.000000000000
1.500000000000
2.250000000000
"""
), "provided sample"

minimum = """\
1 3
7
get 1
shuffle 1 1
get 1
"""

assert close_enough(
    run(minimum),
    """\
7.000000000000
7.000000000000
"""
), "minimum size"

all_equal = """\
5 7
8 8 8 8 8
shuffle 1 5
shuffle 2 4
get 1
get 2
get 5
"""

assert close_enough(
    run(all_equal),
    """\
8.000000000000
8.000000000000
8.000000000000
"""
), "all equal values"

boundaries = """\
4 7
1 2 9 10
shuffle 1 2
get 1
get 2
shuffle 3 4
get 3
get 4
get 2
"""

assert close_enough(
    run(boundaries),
    """\
1.500000000000
1.500000000000
9.500000000000
9.500000000000
1.500000000000
"""
), "boundary intervals"

maximum_n = 250000
maximum_case = (
    f"{maximum_n} 3\n"
    + " ".join(["1000000"] * maximum_n)
    + "\n"
    + "shuffle 1 250000\n"
    + "get 125000\n"
    + "get 250000\n"
)

assert close_enough(
    run(maximum_case),
    """\
1000000.000000000000
1000000.000000000000
"""
), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 6` with the provided operations | `1`, `3`, `1.5`, `2.25` | Correct propagation across overlapping shuffles |
| `1 3` with value `7` | `7`, `7` | Single-position intervals and the smallest possible array |
| Five equal values with whole-array and subarray shuffles | Three answers equal to `8` | Uniform expectations and repeated lazy assignments |
| Four values with shuffles `[1,2]` and `[3,4]` | `1.5`, `1.5`, `9.5`, `9.5`, `1.5` | Inclusive boundaries and disjoint intervals |
| `n = 250000`, all values `1000000` | Two answers equal to `1000000` | Maximum array size and large range assignment |

## Edge Cases

For a single-position shuffle, the segment tree computes the interval sum and divides by an interval length of `1`. With

```
1 3
7
get 1
shuffle 1 1
get 1
```

the sum is `7`, the average is `7 / 1 = 7`, and the range assignment leaves the value unchanged. The two queries both return `7.000000000000`.

For a full-array shuffle, every position receives the same expected value because every original element is equally likely to reach every position. For

```
3 2
1 2 6
shuffle 1 3
get 2
```

the root node already stores the complete sum `9`. The shuffle calculates `9 / 3 = 3` and assigns `3` to the root lazily. The point query then pushes that value down its path and returns `3.000000000000`.

For inclusive boundaries, consider

```
3 2
1 2 9
shuffle 1 2
get 2
```

the requested interval has sum `3` and length `2`, so its new expected value is `1.5`. The assignment covers exactly positions `1` and `2`. Position `3` remains `9`, and `get 2` returns `1.500000000000`.

For overlapping shuffles, consider the provided sequence

```
3 4
1 2 3
shuffle 1 2
shuffle 2 3
get 1
get 3
```

After the first operation, positions `1` and `2` both have expectation `1.5`. The second operation queries the current sum of positions `2` and `3`, which is `1.5 + 3 = 4.5`, not `2 + 3 = 5`. Its new average is `2.25`. The final expectations are `[1.5, 2.25, 2.25]`, so the answers are `1.500000000000` and `2.250000000000`.

For repeated assignment of an already uniform interval, consider

```
4 3
5 5 5 5
shuffle 1 4
shuffle 2 3
get 2
```

The first shuffle assigns `5` to every position. The second shuffle calculates an interval average of `(5+5)/2 = 5`, so the state does not change. The lazy segment tree handles both operations without expanding the first whole-array assignment into individual elements.

For the largest allowed array, every node can be assigned the same expectation without needing to materialize individual changes. With `250000` positions all containing `1000000`, a full-range shuffle still has average `1000000`. A later point query follows only one tree path, so the size of the array does not turn the query into a linear scan.
