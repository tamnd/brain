---
title: "CF 102419I - Another Query Problem"
description: "We maintain an integer array (A) of length (n), initially filled with zeroes. A type 2 operation adds an arithmetic progression to one contiguous interval. For an operation ((l,r,a,b)), position (i) receives [ a+b(i-l)."
date: "2026-08-12T20:25:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "I"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 474
verified: true
draft: false
---

[CF 102419I - Another Query Problem](https://codeforces.com/problemset/problem/102419/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an integer array (A) of length (n), initially filled with zeroes. A type 2 operation adds an arithmetic progression to one contiguous interval. For an operation ((l,r,a,b)), position (i) receives

[
a+b(i-l).
]

A type 1 operation asks whether every value in (A_l,A_{l+1},\ldots,A_r) is identical. The required output is (1) when the interval is constant and (0) otherwise.

The bounds (n,q\le 2\cdot10^5) rule out scanning an entire interval for every query. In the worst case, there can be (2\cdot10^5) operations on intervals of length (2\cdot10^5), which gives roughly (4\cdot10^{10}) array accesses. We need each operation to take around (O(\log n)), or at least substantially less than linear time.

The tricky part is that an arithmetic progression update looks like it changes every element of an interval independently. Storing the actual values and modifying the whole interval is exactly what makes the brute-force solution too slow.

A useful edge case is a one-element query. For example,

```
1 1
1 1 1
```

has output

```
1
```

because a single element is always equal to itself. A solution that searches for a difference inside the interval might accidentally treat this as a non-constant range.

Another edge case occurs when the progression has (b=0). For example,

```
3 2
2 1 3 5 0
1 1 3
```

produces

```
1
```

because the update adds (5) to every position, giving ([5,5,5]). A careless solution may assume every type 2 operation necessarily creates different values because it is described as an arithmetic progression.

The interval boundaries also matter. Consider

```
4 3
2 2 4 1 1
1 2 4
1 1 4
```

After the update the array is ([0,1,2,3]), so the outputs are

```
0
0
```

The first query checks only positions 2 through 4. The second includes position 1, which was untouched. A difference-array implementation that forgets the right boundary or uses (l) instead of (l+1) when checking equality can silently include the wrong difference.

Negative updates are another source of mistakes. For example,

```
3 3
2 1 3 5 -2
1 1 3
2 2 2 -1 0
1 1 3
```

gives

```
0
0
```

The first update creates ([5,3,1]), and the second changes position 2 to (2), giving ([5,2,1]). The data structure must work with signed values, not just with whether values are increasing or decreasing.

## Approaches

The direct solution is to store (A) itself. For a type 2 operation, iterate from (l) to (r) and add the corresponding term of the progression. For a type 1 query, scan the interval and compare every value with the first one. This is correct because it explicitly performs exactly the operations described by the problem and directly checks the definition of a constant interval.

The problem is the worst case. One update can touch (O(n)) elements, and one query can inspect (O(n)) elements. With (2\cdot10^5) operations, this can require about (4\cdot10^{10}) elementary array operations, far beyond the time limit.

The key observation is to stop looking at the values themselves and instead look at their adjacent differences. Define

[
D_i=A_i-A_{i-1},
]

with (A_0=0). An interval (A_l,\ldots,A_r) is constant exactly when

[
D_{l+1}=D_{l+2}=\cdots=D_r=0.
]

So a potentially long equality query becomes a query asking whether a range of differences contains anything nonzero.

Now consider what an arithmetic progression update does to (D). Let

[
x=a+b(r-l)
]

be the last value added to the interval. At position (l), the difference changes by (a). Between (l+1) and (r), every adjacent difference changes by (b). At (r+1), the difference changes by (-x). Thus the entire update becomes

[
D_l\mathrel{+}=a,
]

[
D_{l+1},\ldots,D_r\mathrel{+}=b,
]

[
D_{r+1}\mathrel{-}=x.
]

The long arithmetic progression has been reduced to one range addition and two point changes.

We still need to determine whether every value in a range of (D) is zero. A convenient way to do that is to maintain the sum of squares of the differences. Since every (D_i^2) is nonnegative,

[
\sum D_i^2=0
]

holds exactly when every (D_i) is zero.

A lazy segment tree can maintain both

[
S=\sum D_i
]

and

[
Q=\sum D_i^2
]

for every segment. If we add (x) to every value in a segment of length (k), then

[
S' = S+kx
]

and

[
Q' = Q+2xS+kx^2.
]

This gives constant-time lazy propagation at every visited segment. Each arithmetic progression update needs (O(\log n)) segment-tree operations, and each equality query needs one (O(\log n)) range query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) | (O(n)) | Too slow |
| Difference array + lazy segment tree | (O(q\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Represent the current array through its difference array (D), where (D_i=A_i-A_{i-1}). Initially every (D_i) is zero because every (A_i) is zero.
2. Build a lazy segment tree over (D). Each node stores the sum of its differences, the sum of their squares, and a lazy value representing a pending addition to the whole segment. The sum is needed when updating the sum of squares.
3. For a type 2 update ((l,r,a,b)), calculate the last added value

[
x=a+b(r-l).
]

Add (a) to (D_l), add (b) to every (D_i) for (l+1\le i\le r), and subtract (x) from (D_{r+1}) when (r<n).

This exactly represents the effect of adding the arithmetic progression to (A_l,\ldots,A_r). The special case (r=n) has no (D_{n+1}) inside the maintained array, so that final correction is simply omitted.

1. For a type 1 query ((l,r)), query the segment tree over (D_{l+1},\ldots,D_r). If (l=r), the range contains no differences, so the answer is immediately (1).
2. Otherwise, inspect the returned sum of squares. If it is zero, every difference in the interval is zero, so all corresponding values of (A) are equal. If it is positive, at least one adjacent pair differs, so the interval is not constant.

### Why it works

The invariant is that the segment tree always represents the exact current difference array (D). An arithmetic progression update changes (D) only at the left boundary, uniformly across its interior, and at the position immediately after the right boundary, so the three corresponding segment-tree updates preserve that invariant. For any queried interval, (A_l,\ldots,A_r) are all equal if and only if every adjacent difference (D_{l+1},\ldots,D_r) is zero. Since the segment tree stores the sum of their squares and squares are nonnegative, that sum is zero exactly in the constant case. Thus every query answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = n
        size = 4 * n + 5
        self.s = [0] * size
        self.sq = [0] * size
        self.lazy = [0] * size

    def _apply(self, node, left, right, x):
        length = right - left + 1
        old_sum = self.s[node]

        self.sq[node] += 2 * x * old_sum + length * x * x
        self.s[node] = old_sum + length * x
        self.lazy[node] += x

    def _push(self, node, left, right):
        x = self.lazy[node]
        if x == 0 or left == right:
            return

        mid = (left + right) >> 1
        self._apply(node << 1, left, mid, x)
        self._apply(node << 1 | 1, mid + 1, right, x)
        self.lazy[node] = 0

    def add(self, ql, qr, x):
        if ql > qr:
            return
        self._add(1, 1, self.n, ql, qr, x)

    def _add(self, node, left, right, ql, qr, x):
        if ql <= left and right <= qr:
            self._apply(node, left, right, x)
            return

        self._push(node, left, right)
        mid = (left + right) >> 1

        if ql <= mid:
            self._add(node << 1, left, mid, ql, qr, x)
        if qr > mid:
            self._add(node << 1 | 1, mid + 1, right, ql, qr, x)

        lc = node << 1
        rc = lc | 1
        self.s[node] = self.s[lc] + self.s[rc]
        self.sq[node] = self.sq[lc] + self.sq[rc]

    def query_sq(self, ql, qr):
        if ql > qr:
            return 0
        return self._query_sq(1, 1, self.n, ql, qr)

    def _query_sq(self, node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return self.sq[node]

        self._push(node, left, right)
        mid = (left + right) >> 1
        result = 0

        if ql <= mid:
            result += self._query_sq(node << 1, left, mid, ql, qr)
        if qr > mid:
            result += self._query_sq(node << 1 | 1, mid + 1, right, ql, qr)

        return result

def solve():
    n, q = map(int, input().split())
    seg = SegmentTree(n)
    out = []

    for _ in range(q):
        query = list(map(int, input().split()))
        typ = query[0]

        if typ == 1:
            l, r = query[1], query[2]

            if l == r:
                out.append("1")
                continue

            # A[l..r] is constant iff
            # D[l+1], ..., D[r] are all zero.
            value = seg.query_sq(l + 1, r)
            out.append("1" if value == 0 else "0")

        else:
            l, r, a, b = query[1:]

            # D[l] += a
            seg.add(l, l, a)

            # D[l+1..r] += b
            if l + 1 <= r:
                seg.add(l + 1, r, b)

            # The value added at position r is the final term.
            last = a + b * (r - l)

            # D[r+1] -= last
            if r < n:
                seg.add(r + 1, r + 1, -last)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The segment tree is initialized with zeroes because the original array consists entirely of zeroes, so every initial difference is zero. There is no need for a separate build procedure.

The `_apply` function is the central lazy-propagation operation. Suppose a node represents values (D_1,\ldots,D_k), with current sum (S) and squared sum (Q). After adding (x) to every value, the new squared sum is

[
\sum(D_i+x)^2
=\sum D_i^2+2x\sum D_i+kx^2.
]

The code saves the old sum before modifying it because the formula requires the old value of (S).

For an update, `seg.add(l, l, a)` handles the left boundary of the difference array. The range update `seg.add(l + 1, r, b)` handles the common increment of all internal differences. Finally, `seg.add(r + 1, r + 1, -last)` accounts for the fact that the progression stops after position (r).

The `r < n` condition is essential. There is no maintained difference (D_{n+1}), because the original array ends at (n). Forgetting this check would create an invalid segment-tree index.

For a type 1 query, the relevant differences start at (l+1), not (l). (D_l=A_l-A_{l-1}) tells us how (A_l) differs from the element before the queried interval, which has no bearing on whether the queried interval itself is constant.

Python integers have arbitrary precision, so the potentially large squared values do not overflow. The largest array values can become much larger than the original (10^8) update parameters after many operations, making a fixed-width 32-bit representation unsafe in languages that use it.

## Worked Examples

### Sample 1

The input is

```
5 3
2 1 3 4 1
1 1 3
1 4 5
```

After the update, (A=[4,9,14,0,0]). Its difference array is

[
D=[4,5,5,-14,0].
]

The trace is:

| Operation | (A) conceptually | Relevant (D) range | Sum of squares | Answer |
| --- | --- | --- | --- | --- |
| Initial | ([0,0,0,0,0]) | all zero | 0 |  |
| `2 1 3 4 1` | ([4,9,14,0,0]) | (D_2,D_3=5,5) | 50 |  |
| `1 1 3` | unchanged | (D_2,D_3=5,5) | 50 | 0 |
| `1 4 5` | unchanged | (D_5=0) | 0 | 1 |

The first query sees nonzero differences inside positions 1 through 3, so those values cannot all be equal. The second query contains two zero-valued elements, so its only relevant difference is zero.

### Constructed Sample 2

Consider

```
4 5
1 1 4
2 1 4 2 0
1 2 3
2 2 3 -1 2
1 1 4
```

The trace is:

| Operation | (A) conceptually | Relevant (D) range | Sum of squares | Answer |
| --- | --- | --- | --- | --- |
| Initial | ([0,0,0,0]) | all zero | 0 |  |
| `1 1 4` | ([0,0,0,0]) | (D_2,D_3,D_4=0,0,0) | 0 | 1 |
| `2 1 4 2 0` | ([2,2,2,2]) | (D_2,D_3,D_4=0,0,0) | 0 |  |
| `1 2 3` | unchanged | (D_3=0) | 0 | 1 |
| `2 2 3 -1 2` | ([2,1,3,2]) | (D_2,D_3,D_4=-1,2,-1) | 6 |  |
| `1 1 4` | unchanged | (D_2,D_3,D_4=-1,2,-1) | 6 | 0 |

The first update has (b=0), so it changes the values but leaves every internal difference equal to zero. The second update introduces nonzero differences, and the sum of squares immediately detects them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(q\log n)) | Each update performs at most three range additions, and each query performs one segment-tree query. |
| Space | (O(n)) | The segment tree stores a constant amount of information for each node. |

With (n,q\le2\cdot10^5), the solution performs only logarithmically many tree operations per query instead of touching every array position in an interval. The segment tree uses (O(n)) memory, comfortably within the 512 MB limit.

## Test Cases

```python
import sys
import io

class SegmentTree:
    def __init__(self, n):
        size = 4 * n + 5
        self.n = n
        self.s = [0] * size
        self.sq = [0] * size
        self.lazy = [0] * size

    def apply(self, node, left, right, x):
        length = right - left + 1
        old_sum = self.s[node]
        self.sq[node] += 2 * x * old_sum + length * x * x
        self.s[node] = old_sum + length * x
        self.lazy[node] += x

    def push(self, node, left, right):
        x = self.lazy[node]
        if x == 0 or left == right:
            return
        mid = (left + right) // 2
        self.apply(node * 2, left, mid, x)
        self.apply(node * 2 + 1, mid + 1, right, x)
        self.lazy[node] = 0

    def add(self, ql, qr, x):
        if ql > qr:
            return
        self._add(1, 1, self.n, ql, qr, x)

    def _add(self, node, left, right, ql, qr, x):
        if ql <= left and right <= qr:
            self.apply(node, left, right, x)
            return

        self.push(node, left, right)
        mid = (left + right) // 2

        if ql <= mid:
            self._add(node * 2, left, mid, ql, qr, x)
        if qr > mid:
            self._add(node * 2 + 1, mid + 1, right, ql, qr, x)

        self.s[node] = self.s[node * 2] + self.s[node * 2 + 1]
        self.sq[node] = self.sq[node * 2] + self.sq[node * 2 + 1]

    def query_sq(self, ql, qr):
        if ql > qr:
            return 0
        return self._query_sq(1, 1, self.n, ql, qr)

    def _query_sq(self, node, left, right, ql, qr):
        if ql <= left and right <= qr:
            return self.sq[node]

        self.push(node, left, right)
        mid = (left + right) // 2
        ans = 0

        if ql <= mid:
            ans += self._query_sq(node * 2, left, mid, ql, qr)
        if qr > mid:
            ans += self._query_sq(node * 2 + 1, mid + 1, right, ql, qr)

        return ans

def solve(data):
    inp = io.StringIO(data)
    n, q = map(int, inp.readline().split())
    seg = SegmentTree(n)
    ans = []

    for _ in range(q):
        v = list(map(int, inp.readline().split()))

        if v[0] == 1:
            l, r = v[1], v[2]
            if l == r:
                ans.append("1")
            else:
                ans.append("1" if seg.query_sq(l + 1, r) == 0 else "0")
        else:
            _, l, r, a, b = v

            seg.add(l, l, a)

            if l + 1 <= r:
                seg.add(l + 1, r, b)

            last = a + b * (r - l)

            if r < n:
                seg.add(r + 1, r + 1, -last)

    return "\n".join(ans)

# Provided sample.
assert solve(
    """5 3
2 1 3 4 1
1 1 3
1 4 5
"""
) == "0\n1", "sample 1"

# Minimum-size input. A one-element interval is always constant.
assert solve(
    """1 4
1 1 1
2 1 1 100000000 100000000
1 1 1
1 1 1
"""
) == "1\n1\n1", "minimum-size case"

# All values remain equal after a constant update.
assert solve(
    """5 4
2 1 5 7 0
1 1 5
2 2 4 -7 0
1 2 4
"""
) == "1\n1", "all-equal values"

# Boundary-sensitive case. The update starts at 2 and ends at 4.
assert solve(
    """4 4
2 2 4 1 1
1 2 4
1 1 4
1 3 4
"""
) == "0\n0\n0", "boundary conditions"

# Cancellation and negative values.
assert solve(
    """4 6
2 1 4 5 -2
1 1 4
2 2 3 -3 0
1 2 3
2 2 3 1 0
1 1 4
"""
) == "0\n1\n0", "negative updates and cancellation"

# Large input size. The update makes the whole array equal,
# then the full-range query must still be answered efficiently.
n = 200000
large_input = f"{n} 2\n2 1 {n} 12345678 0\n1 1 {n}\n"
assert solve(large_input) == "1", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 4 ...` | `1 1 1` | Single-element intervals and (n=1) |
| Constant additions | `1 1` | (b=0) and preservation of equality |
| Update from 2 through 4 | `0 0 0` | Left and right boundaries, plus untouched elements |
| Negative updates | `0 1 0` | Signed values and cancellation |
| (n=200000) | `1` | Maximum-size input and logarithmic processing |

## Edge Cases

For a single-element interval, such as

```
1 2
1 1 1
```

the query has no adjacent pair to compare. The implementation handles this explicitly by returning (1). In difference-array terms, the required range (D_{l+1},\ldots,D_r) is empty.

For a constant progression, consider

```
3 2
2 1 3 5 0
1 1 3
```

The update adds ([5,5,5]), so (A=[5,5,5]). In the difference array, (D_1=5), while (D_2=D_3=0). The query checks only (D_2,D_3), obtains a sum of squares equal to zero, and returns (1).

For an update touching the last position, consider

```
3 2
2 2 3 4 2
1 2 3
```

The new array is ([0,4,6]). The update changes (D_2) by (4) and (D_3) by (2). There is no (D_4) in the maintained structure, so the right-boundary correction is skipped. The query examines (D_3=2), whose square is positive, and returns (0).

For a range starting at position 1, consider

```
3 2
2 1 3 7 3
1 1 3
```

The array becomes ([7,10,13]), with differences (D_2=3,D_3=3). The query correctly examines positions (2) through (3) of the difference array. It does not inspect (D_1=A_1-A_0=7), because (A_0) is outside the queried interval.

For negative values, consider

```
3 2
2 1 3 5 -2
1 1 3
```

The array becomes ([5,3,1]), so its relevant differences are (D_2=-2) and (D_3=-2). Their squares sum to (8), which is positive, and the answer is (0). The sum-of-squares method does not depend on whether the differences are positive or negative, which is exactly what we need for arbitrary signed updates.
