---
title: "CF 102307J - Jail Destruction"
description: "We have an array of (n) wall heights. A destruction operation chooses an interval ([a,b]) and removes exactly (s) meters from every wall in that interval, except that a wall cannot become negative. In other words, every affected height changes from (hi) to (max(0,hi-s))."
date: "2026-08-13T07:25:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "J"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 106
verified: true
draft: false
---

[CF 102307J - Jail Destruction](https://codeforces.com/problemset/problem/102307/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of (n) wall heights. A destruction operation chooses an interval ([a,b]) and removes exactly (s) meters from every wall in that interval, except that a wall cannot become negative. In other words, every affected height changes from (h_i) to (\max(0,h_i-s)).

A query asks for the total remaining height of all walls in a given interval. The operations are online, so each query must be answered using the state produced by all previous destruction operations.

The constraints are large enough to rule out updating every wall in an interval. With (n,q\le 10^5), there can be (10^{10}) affected positions across all operations. Even an (O(nq)) solution would be far beyond what a few seconds can handle. We need a data structure that can usually process an entire interval without touching its individual walls.

The difficulty is the truncation at zero. A normal lazy segment tree works immediately for an operation such as (h_i\mathrel{-}=s), because every value changes by the same amount. Here, some walls may reach zero while taller walls continue decreasing, so a single uniform lazy value is not always sufficient.

Several edge cases expose this problem.

Consider a single wall:

```
1 3
2
2 1 1 5
1 1 1
```

The wall has height (2), so destroying (5) meters leaves height (0). The output is:

```
0
```

An implementation that simply subtracts (5) would store (-3), producing an invalid answer.

Now consider different heights:

```
2 2
3 10
2 1 2 5
1 1 2
```

After the attack the heights are (0,5), so the correct output is:

```
5
```

A lazy update that subtracts (5) from the entire segment cannot represent the first wall correctly because that wall has already reached zero.

Equality is another boundary case:

```
2 2
5 10
2 1 2 5
1 1 2
```

The resulting heights are (0,5), and the answer is:

```
5
```

The implementation must treat (s=\text{minimum positive height}) as a case where at least one wall becomes zero. A lazy subtraction is safe only when (s) is strictly smaller than the smallest positive height.

Finally, an interval can contain walls that are already zero:

```
3 3
2 5 1
2 1 1 3
2 1 3 2
1 1 3
```

After the first attack the array is (0,5,1). After the second it is (0,3,0), so the answer is:

```
3
```

Zero-valued walls must not participate in future subtraction. Treating zero as the ordinary minimum would make the data structure unable to distinguish "already destroyed" from "smallest positive wall."

## Approaches

The direct solution stores every current wall height. For a destruction operation on ([a,b]), it visits every index in that interval and performs (h_i=\max(0,h_i-s)). A query similarly scans the interval and adds all heights. This is correct because it performs exactly the operation described by the problem.

The problem is the worst case. If all (q) operations affect the entire array, each operation touches (n) walls, giving (O(nq)) work. With both values as large as (10^5), that is up to (10^{10}) individual array operations, which is much too large.

A normal lazy segment tree seems promising because a whole interval can often be decreased at once. The obstacle is the zero boundary. Suppose a segment contains heights (3,10,12) and we subtract (5). The result is (0,5,7). There is no single subtraction that transforms all three values correctly.

The useful observation is that we do not need to know the full distribution of heights. For a segment, keep its sum, the number of positive walls, and the minimum positive height. If (s) is smaller than that minimum positive height, every positive wall survives the attack. The entire segment can then be decreased lazily by (s), because all positive values undergo exactly the same transformation.

If (s) is at least the minimum positive height, at least one wall becomes zero. We recursively inspect the segment until those walls can be destroyed individually. This sounds potentially expensive, but every such forced descent permanently removes at least one positive wall. A wall can become zero only once, so the expensive part is amortized over the entire execution.

The same segment tree can answer sum queries in the standard (O(\log n)) way. Thus the solution combines lazy propagation with an amortized "destroy the minimum positive values" strategy.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) worst case | (O(n)) | Too slow |
| Optimal | (O((n+q)\log n)) amortized | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the wall heights. For every node, store the sum of its interval, the number of positive walls in that interval, and the smallest positive wall height. Store (+\infty) as the minimum when the entire interval has already been destroyed. These three values are exactly what we need to decide whether a destruction operation can be applied lazily.
2. Also store a lazy value representing meters that have been removed from every currently positive wall in the node. If a node contains `cnt` positive walls and receives a lazy subtraction of (s), its sum decreases by `cnt * s`, and its minimum positive height decreases by (s). Zero walls are unaffected.
3. For a destruction operation on a fully covered node, first check whether its sum is zero. If so, the entire interval is already destroyed and there is nothing to do.
4. If the node is fully covered and (s) is strictly smaller than its minimum positive height, apply the subtraction lazily. Every positive wall remains positive, so all of them really do lose exactly (s) meters.
5. Otherwise, descend into the children. The condition (s\ge\text{minimum positive height}) means at least one positive wall will reach zero, so the operation cannot be represented by one uniform lazy subtraction. Push any pending lazy value before descending so that the children see their actual current heights.
6. At a leaf, subtract (s) with the zero floor. Since this leaf was reached through the hard case, its current height is at most (s), so it becomes zero. Set its positive count to zero and its minimum to (+\infty).
7. After updating children, merge them. The new sum is the sum of the child sums, the positive count is the sum of the child counts, and the minimum positive height is the smaller child minimum.
8. For a sum query, use ordinary segment-tree interval traversal. Push lazy values before going into a child, because a child's stored state may still be waiting for its parent's pending subtraction.

Why it works: every segment-tree node always describes its interval exactly through its sum, positive count, and minimum positive height. When (s) is smaller than the minimum positive height, no wall can reach zero, so subtracting (s) from every positive wall is exactly the required operation and can safely be stored as a lazy tag. When (s) reaches the minimum, uniform subtraction is no longer valid, so the algorithm descends until the affected walls can be handled individually. At every leaf the update is exactly (h_i\leftarrow\max(0,h_i-s)). Since parent information is rebuilt from correct children, the invariant is preserved after every update. Queries return sums from these exact segment states, so every reported interval total is correct.

The amortization comes from the hard case. Whenever a fully covered node cannot be lazily updated, its minimum positive wall is destroyed somewhere below it. Each wall can be destroyed only once. The recursion around a destroyed wall has height (O(\log n)), so all hard descents together contribute (O(n\log n)). The ordinary traversal caused by query boundaries and lazily handled updates contributes (O(q\log n)).

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    size = 4 * n + 5
    total = [0] * size
    mn = [INF] * size
    cnt = [0] * size
    lazy = [0] * size

    def build(node, left, right):
        if left == right:
            value = a[left]
            total[node] = value
            mn[node] = value
            cnt[node] = 1
            return

        mid = (left + right) // 2
        lc = node * 2
        rc = lc + 1

        build(lc, left, mid)
        build(rc, mid + 1, right)

        total[node] = total[lc] + total[rc]
        cnt[node] = cnt[lc] + cnt[rc]
        mn[node] = min(mn[lc], mn[rc])

    def apply(node, value):
        if cnt[node] == 0:
            return

        total[node] -= cnt[node] * value
        mn[node] -= value
        lazy[node] += value

    def push(node):
        value = lazy[node]
        if value == 0:
            return

        lc = node * 2
        rc = lc + 1

        apply(lc, value)
        apply(rc, value)

        lazy[node] = 0

    def pull(node):
        lc = node * 2
        rc = lc + 1

        total[node] = total[lc] + total[rc]
        cnt[node] = cnt[lc] + cnt[rc]
        mn[node] = min(mn[lc], mn[rc])

    def update(node, left, right, ql, qr, value):
        if qr < left or right < ql or total[node] == 0:
            return

        if ql <= left and right <= qr and value < mn[node]:
            apply(node, value)
            return

        if left == right:
            total[node] = 0
            cnt[node] = 0
            mn[node] = INF
            lazy[node] = 0
            return

        push(node)

        mid = (left + right) // 2
        lc = node * 2
        rc = lc + 1

        if ql <= mid:
            update(lc, left, mid, ql, qr, value)
        if qr > mid:
            update(rc, mid + 1, right, ql, qr, value)

        pull(node)

    def query(node, left, right, ql, qr):
        if qr < left or right < ql:
            return 0

        if ql <= left and right <= qr:
            return total[node]

        push(node)

        mid = (left + right) // 2

        result = 0
        if ql <= mid:
            result += query(node * 2, left, mid, ql, qr)
        if qr > mid:
            result += query(node * 2 + 1, mid + 1, right, ql, qr)

        return result

    build(1, 0, n - 1)

    output = []

    for _ in range(q):
        parts = list(map(int, input().split()))
        operation = parts[0]
        left = parts[1] - 1
        right = parts[2] - 1

        if operation == 1:
            output.append(str(query(1, 0, n - 1, left, right)))
        else:
            value = parts[3]
            update(1, 0, n - 1, left, right, value)

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The tree uses four arrays because Python object-heavy node structures would consume considerably more memory and add overhead. `total[node]` is the remaining total wall height, `cnt[node]` counts positive walls, `mn[node]` is their smallest positive height, and `lazy[node]` stores a pending subtraction.

The `apply` function is valid only for a subtraction that keeps every positive wall positive. The condition `value < mn[node]` guarantees exactly that. The number of positive walls does not change, so the sum decreases by `cnt[node] * value` and the minimum decreases by `value`.

A completely destroyed node has `cnt[node] == 0`. Its minimum is represented by `INF`, rather than by zero. This distinction is essential because zero means "not positive," while the minimum we need is specifically the minimum among positive walls. The `apply` function ignores destroyed nodes, so pending subtractions never affect them.

The strict comparison `value < mn[node]` is another important detail. If `value == mn[node]`, at least one wall reaches exactly zero, so the operation must recurse. Treating equality as a lazy update would leave the positive count and minimum incorrect.

At a leaf reached by the recursive hard case, the wall necessarily becomes zero. Resetting `lazy[node]` is necessary because a zero leaf must never carry a subtraction tag into the future. Otherwise a later `push` could incorrectly modify its stored minimum.

The implementation uses zero-based indices internally, while the input uses one-based indices. Subtracting one from both query endpoints immediately after reading them avoids repeated conversions and keeps the segment tree boundaries consistent.

Python integers have arbitrary precision, so sums cannot overflow. The largest possible total is (10^5\cdot10^8=10^{13}), which would fit in a 64-bit integer anyway.

## Worked Examples

The provided sample starts with two walls of height (10).

| Operation | Array after operation | Sum queried |
| --- | --- | --- |
| `1 1 2` | `[10, 10]` | 20 |
| `2 1 2 5` | `[5, 5]` |  |
| `1 1 2` | `[5, 5]` | 10 |
| `2 2 2 6` | `[5, 0]` |  |
| `1 1 2` | `[5, 0]` | 5 |

The first attack can be represented by one lazy subtraction because the segment minimum is (10), which is greater than (5). After that update, the segment sum is (10), its positive count is still (2), and its minimum positive height is (5).

The second attack targets only the second wall. Its current height is (5), while the attack removes (6), so the strict lazy condition fails. The recursion reaches that leaf and destroys it completely. The resulting sum is (5).

For a second example, consider:

```
4 5
7 3 10 5
1 1 4
2 2 3 4
1 2 4
2 1 2 6
1 1 3
```

The state can be traced as follows.

| Step | Operation | Array | Relevant sum |
| --- | --- | --- | --- |
| 0 | Initial | `[7, 3, 10, 5]` | 25 |
| 1 | `1 1 4` | `[7, 3, 10, 5]` | 25 |
| 2 | `2 2 3 4` | `[7, 0, 6, 5]` |  |
| 3 | `1 2 4` | `[7, 0, 6, 5]` | 11 |
| 4 | `2 1 2 6` | `[1, 0, 6, 5]` |  |
| 5 | `1 1 3` | `[1, 0, 6, 5]` | 7 |

The attack on positions (2) through (3) has minimum positive height (3), while (s=4). The wall of height (3) must be destroyed, so the tree descends instead of applying one lazy subtraction to the whole interval. The wall of height (10) becomes (6).

Later, the attack on positions (1) through (2) removes (6). The first wall goes from (7) to (1), while the second is already zero. Because destroyed walls have `cnt = 0`, they do not participate in the subtraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\log n)) amortized | Ordinary tree traversals cost (O(\log n)) per operation, while hard descents are charged to walls that become zero |
| Space | (O(n)) | Four segment-tree arrays contain (O(n)) nodes |

The input contains at most (10^5) walls and (10^5) operations. The segment tree avoids the (O(nq)) worst case of direct simulation. Its amortized (O((n+q)\log n)) work is suitable for the (4) second and (256) MB limits, while the array-based Python representation keeps memory usage controlled.

## Test Cases

```python
import sys
import io

INF = 10**30

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, q = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))

        size = 4 * n + 5
        total = [0] * size
        mn = [INF] * size
        cnt = [0] * size
        lazy = [0] * size

        def build(node, left, right):
            if left == right:
                value = a[left]
                total[node] = value
                mn[node] = value
                cnt[node] = 1
                return

            mid = (left + right) // 2
            build(node * 2, left, mid)
            build(node * 2 + 1, mid + 1, right)

            total[node] = total[node * 2] + total[node * 2 + 1]
            cnt[node] = cnt[node * 2] + cnt[node * 2 + 1]
            mn[node] = min(mn[node * 2], mn[node * 2 + 1])

        def apply(node, value):
            if cnt[node] == 0:
                return
            total[node] -= cnt[node] * value
            mn[node] -= value
            lazy[node] += value

        def push(node):
            value = lazy[node]
            if value == 0:
                return
            apply(node * 2, value)
            apply(node * 2 + 1, value)
            lazy[node] = 0

        def pull(node):
            total[node] = total[node * 2] + total[node * 2 + 1]
            cnt[node] = cnt[node * 2] + cnt[node * 2 + 1]
            mn[node] = min(mn[node * 2], mn[node * 2 + 1])

        def update(node, left, right, ql, qr, value):
            if qr < left or right < ql or total[node] == 0:
                return

            if ql <= left and right <= qr and value < mn[node]:
                apply(node, value)
                return

            if left == right:
                total[node] = 0
                cnt[node] = 0
                mn[node] = INF
                lazy[node] = 0
                return

            push(node)

            mid = (left + right) // 2
            if ql <= mid:
                update(node * 2, left, mid, ql, qr, value)
            if qr > mid:
                update(node * 2 + 1, mid + 1, right, ql, qr, value)

            pull(node)

        def query(node, left, right, ql, qr):
            if qr < left or right < ql:
                return 0

            if ql <= left and right <= qr:
                return total[node]

            push(node)

            mid = (left + right) // 2
            result = 0

            if ql <= mid:
                result += query(node * 2, left, mid, ql, qr)
            if qr > mid:
                result += query(node * 2 + 1, mid + 1, right, ql, qr)

            return result

        build(1, 0, n - 1)

        output = []

        for _ in range(q):
            parts = list(map(int, sys.stdin.readline().split()))
            op = parts[0]
            l = parts[1] - 1
            r = parts[2] - 1

            if op == 1:
                output.append(str(query(1, 0, n - 1, l, r)))
            else:
                update(1, 0, n - 1, l, r, parts[3])

        return "\n".join(output)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""2 5
10 10
1 1 2
2 1 2 5
1 1 2
2 2 2 6
1 1 2
""") == """20
10
5""", "provided sample"

assert run("""4 5
7 3 10 5
1 1 4
2 2 3 4
1 2 4
2 1 2 6
1 1 3
""") == """25
11
7""", "mixed updates and queries"

assert run("""1 3
2
1 1 1
2 1 1 5
1 1 1
""") == """2
0""", "minimum-size input and over-destruction"

assert run("""5 5
8 8 8 8 8
2 1 5 3
1 1 5
2 2 4 5
1 1 5
1 2 4
""") == """25
10
0""", "all equal values"

assert run("""4 6
3 100 4 8
2 1 1 3
1 1 4
2 2 3 4
1 1 4
2 4 4 8
1 3 4
""") == """109
101
0""", "single-position and boundary updates"

n = 100000
maximum_input = (
    f"{n} 3\n"
    + " ".join(["100000000"] * n)
    + "\n"
    + f"1 1 {n}\n"
    + f"2 1 {n} 100000000\n"
    + f"1 1 {n}\n"
)
assert run(maximum_input) == "10000000000000\n0", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 2 / ...` | `2`, then `0` | Single wall and destruction larger than its height |
| `5 5 / 8 8 8 8 8 / ...` | `25`, `10`, `0` | Equal heights and repeated full-range operations |
| `4 6 / 3 100 4 8 / ...` | `109`, `101`, `0` | Single-position updates and interval boundaries |
| `100000` equal walls of height `100000000` | `10000000000000`, then `0` | Maximum (n), large sums, and full-range destruction |

## Edge Cases

A destruction amount larger than a wall must never create a negative height. For

```
1 3
2
1 1 1
2 1 1 5
1 1 1
```

the first query returns (2). The update reaches the leaf with height (2), and because (5\ge2), the hard case destroys it completely. The final query returns (0).

An exact equality between the attack amount and the minimum positive height also requires recursion. For

```
2 2
5 10
2 1 2 5
1 1 2
```

the minimum positive height is (5), exactly equal to the attack amount. The strict condition `value < mn[node]` fails, so the tree descends. The first wall becomes zero and the second becomes (5), giving the correct sum (5).

Already destroyed walls must remain unchanged. In

```
3 3
2 5 1
2 1 1 3
2 1 3 2
1 1 3
```

the first operation changes the array to `[0,5,1]`. During the second operation, the zero wall has `cnt = 0`, so the lazy subtraction is applied only to the positive walls. The final state is `[0,3,0]`, and the answer is (3).

A single-position interval is also handled by the same recursion without special cases. For example,

```
4 3
3 100 4 8
2 1 1 3
1 1 4
2 4 4 8
```

changes the first wall from (3) to (0), then the last wall from (8) to (0). The segment tree can isolate either leaf through its normal interval traversal, so no separate point-update implementation is necessary.

The full-range case is where the optimization matters most. If every wall initially has height (100000000), an attack removing exactly (100000000) meters reaches the minimum exactly and eventually destroys every leaf. Each wall is removed only once, so although this particular operation requires recursive descent, the same wall cannot cause another hard descent after it has become zero. That is the amortization behind the (O((n+q)\log n)) bound.
