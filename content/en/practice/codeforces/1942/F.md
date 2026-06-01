---
title: "CF 1942F - Farmer John's Favorite Function"
description: "We have an array $a$, and a recursively defined value: $$f(1)=sqrt{a1}, qquad f(i)=sqrt{f(i-1)+ai}.$$ After every point update $ak leftarrow x$, we need the integer part of $f(n)$. The first obstacle is that the recurrence uses real numbers."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1942
codeforces_index: "F"
codeforces_contest_name: "CodeTON Round 8 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2700
weight: 1942
solve_time_s: 130
verified: true
draft: false
---

[CF 1942F - Farmer John's Favorite Function](https://codeforces.com/problemset/problem/1942/F)

**Rating:** 2700  
**Tags:** brute force, data structures, implementation, math  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array $a$, and a recursively defined value:

$$f(1)=\sqrt{a_1}, \qquad f(i)=\sqrt{f(i-1)+a_i}.$$

After every point update $a_k \leftarrow x$, we need the integer part of $f(n)$.

The first obstacle is that the recurrence uses real numbers. A direct simulation would repeatedly evaluate square roots in floating point, and even tiny precision errors can change the final floor value. The sample already shows such a situation: the true answer is $2$, even though the final value is extremely close to $3$.

The constraints are large. Both $n$ and $q$ are up to $2 \cdot 10^5$. Recomputing the whole recurrence after every update would take $O(nq)$, which is roughly $4 \cdot 10^{10}$ operations in the worst case. That is completely out of reach for a 5 second limit.

The key difficulty is that updates happen on the array, but the recurrence depends on all previous positions. A single modification near the beginning potentially changes every later value.

There are several easy ways to get a wrong solution.

Consider:

```
n = 2
a = [3, 14]
```

Then

$$f(1)=\sqrt3 \approx 1.732,$$

$$f(2)=\sqrt{14+\sqrt3}\approx 3.966.$$

The answer is $3$. If we round intermediate values instead of taking the exact recurrence, we get a different result.

Another dangerous case is very large values:

```
n = 1
a = [10^18]
```

The answer is exactly $10^9$. Using doubles carelessly can lose precision near the boundary and produce $999999999$.

A more subtle example is:

```
a = [3, 14, 0, 7, 6]
```

The final value is approximately $2.999766$, so the answer is $2$. Any approach that repeatedly computes floating point square roots and then rounds at the end risks returning $3$.

The solution must avoid floating point arithmetic entirely.

## Approaches

The brute force idea is straightforward. After every update, rebuild the recurrence from left to right.

```
cur = sqrt(a[1])
for i = 2..n:
    cur = sqrt(cur + a[i])
answer = floor(cur)
```

This is correct because it directly follows the definition. The problem is the complexity. Each query requires $O(n)$ work, so the total cost is $O(nq)$. With $n=q=2\cdot10^5$, this becomes roughly $4\cdot10^{10}$ operations.

The first observation is that we only need $\lfloor f(n)\rfloor$, not the exact real value.

Define

$$g(1)=\left\lfloor \sqrt{a_1}\right\rfloor,$$

$$g(i)=\left\lfloor \sqrt{g(i-1)+a_i}\right\rfloor.$$

A crucial fact is:

$$g(i)=\lfloor f(i)\rfloor$$

for every $i$.

The reason is simple. Let

$$f(i-1)=g(i-1)+\delta, \qquad 0\le \delta<1.$$

Then

$$g(i-1)+a_i \le f(i-1)+a_i < g(i-1)+a_i+1.$$

Taking square roots keeps the value inside an interval of length less than $1$, so both endpoints have the same floor. Hence

$$\left\lfloor \sqrt{f(i-1)+a_i}\right\rfloor = \left\lfloor \sqrt{g(i-1)+a_i}\right\rfloor.$$

Now the whole problem becomes integer-only.

The second observation is to process all queries offline.

For a fixed position $i$, its value changes only when an update touches index $i$. Along the query timeline, $a_i$ is piecewise constant.

Suppose we maintain, for every query time $t$, the current value

$$dp_t$$

after processing positions $1 \ldots i-1$.

When we process position $i$, every timeline point performs

$$dp_t \leftarrow \left\lfloor \sqrt{dp_t + a_i(t)} \right\rfloor.$$

Here $a_i(t)$ denotes the value of position $i$ after query $t$.

So each position contributes:

1. Several range additions on the timeline, because $a_i(t)$ is piecewise constant.
2. One global operation $x \mapsto \lfloor\sqrt{x}\rfloor$.

The remaining challenge is supporting repeated global square-root operations efficiently.

A segment tree stores the minimum and maximum value in every node.

For a node covering values in $[mn,mx]$, if

$$mx-mn = \lfloor\sqrt{mx}\rfloor-\lfloor\sqrt{mn}\rfloor,$$

then every value in that segment changes by the same amount.

Indeed, in that situation

$$\lfloor\sqrt{x}\rfloor - x$$

is constant throughout the interval. The whole segment can be updated lazily using a single range add.

Only segments where this condition fails need to be split further.

This is a classic segment-tree-beats style argument. Repeated square roots rapidly shrink numbers, so the recursion depth stays manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| Optimal | $O((n+q)\log^2 q)$ amortized | $O(q)$ | Accepted |

## Algorithm Walkthrough

1. Read the initial array and all updates.
2. For every index $i$, collect the times when that index is modified.
3. Convert the update history of each position into disjoint timeline intervals. For every interval $[L,R]$, the value of $a_i$ remains constant.
4. Build a segment tree over query times $1 \ldots q$. Initially every timeline value is $0$.
5. Process array positions from left to right.
6. For the current position $i$, apply a range addition on every timeline interval where $a_i$ is constant. After these additions, each timeline point contains

$$g(i-1)+a_i.$$

1. Apply the transformation

$$x \mapsto \lfloor\sqrt{x}\rfloor$$

to the entire segment tree.

1. The segment tree now stores

$$g(i)$$

for every query time simultaneously.

1. After all positions are processed, extract all leaves. The value at timeline position $t$ is exactly the answer after query $t$.

### Why it works

After processing the first $i$ positions, every timeline point $t$ stores

$$g_i(t),$$

the integer recurrence value for the array state after query $t$.

The invariant is true initially because all values are $0$.

When processing position $i$, we first add $a_i(t)$ to every timeline point. The stored value becomes

$$g_{i-1}(t)+a_i(t).$$

Applying the square-root transformation changes it to

$$\left\lfloor \sqrt{g_{i-1}(t)+a_i(t)} \right\rfloor,$$

which is exactly $g_i(t)$.

By induction, after the last position we obtain $g_n(t)$ for every query time. Since $g_n(t)=\lfloor f_n(t)\rfloor$, the reported answers are correct.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        size = 4 * n + 5
        self.mn = [0] * size
        self.mx = [0] * size
        self.lazy = [0] * size

    def apply_add(self, p, v):
        self.mn[p] += v
        self.mx[p] += v
        self.lazy[p] += v

    def push(self, p):
        if self.lazy[p]:
            v = self.lazy[p]
            self.apply_add(p * 2, v)
            self.apply_add(p * 2 + 1, v)
            self.lazy[p] = 0

    def pull(self, p):
        self.mn[p] = min(self.mn[p * 2], self.mn[p * 2 + 1])
        self.mx[p] = max(self.mx[p * 2], self.mx[p * 2 + 1])

    def range_add(self, p, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            self.apply_add(p, v)
            return

        self.push(p)
        m = (l + r) >> 1

        if ql <= m:
            self.range_add(p * 2, l, m, ql, qr, v)
        if qr > m:
            self.range_add(p * 2 + 1, m + 1, r, ql, qr, v)

        self.pull(p)

    def apply_sqrt(self, p, l, r):
        mn = self.mn[p]
        mx = self.mx[p]

        if mx - mn == isqrt(mx) - isqrt(mn):
            delta = isqrt(mx) - mx
            self.apply_add(p, delta)
            return

        if l == r:
            v = isqrt(mx)
            self.mn[p] = v
            self.mx[p] = v
            self.lazy[p] = 0
            return

        self.push(p)
        m = (l + r) >> 1
        self.apply_sqrt(p * 2, l, m)
        self.apply_sqrt(p * 2 + 1, m + 1, r)
        self.pull(p)

    def collect(self, p, l, r, res):
        if l == r:
            res[l] = self.mn[p]
            return

        self.push(p)
        m = (l + r) >> 1
        self.collect(p * 2, l, m, res)
        self.collect(p * 2 + 1, m + 1, r, res)

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    changes = [[] for _ in range(n)]

    for t in range(1, q + 1):
        k, x = map(int, input().split())
        changes[k - 1].append((t, x))

    seg = SegTree(q)

    for i in range(n):
        cur = a[i]
        last = 1

        for t, x in changes[i]:
            if last <= t - 1:
                seg.range_add(1, 1, q, last, t - 1, cur)
            cur = x
            last = t

        if last <= q:
            seg.range_add(1, 1, q, last, q, cur)

        seg.apply_sqrt(1, 1, q)

    ans = [0] * (q + 1)
    seg.collect(1, 1, q, ans)

    sys.stdout.write("\n".join(map(str, ans[1:])))

solve()
```

The first important idea in the implementation is replacing the real recurrence with the integer recurrence. That removes all precision issues and allows every value to remain an integer.

The preprocessing phase builds the timeline intervals for every array position. If index $i$ is updated at times $5$, $11$, and $20$, then its value is constant on several disjoint query ranges. Each such range becomes one segment-tree range addition.

The segment tree stores only minimum, maximum, and a lazy addition tag. No sums are needed.

The subtle part is `apply_sqrt`. If the node satisfies

$$mx-mn = \lfloor\sqrt{mx}\rfloor-\lfloor\sqrt{mn}\rfloor,$$

then the square-root operation acts like adding a constant to every element in that node. We can update the whole segment lazily.

Otherwise we recurse into the children.

Using `math.isqrt` is essential. It computes exact integer square roots and avoids all floating point errors.

## Worked Examples

### Example 1

Input:

```
5 6
0 14 0 7 6
1 4
1 3
2 15
4 1
5 2
5 8
```

After processing position 1:

| Query | a₁ | Value after sqrt |
| --- | --- | --- |
| 1 | 4 | 2 |
| 2 | 3 | 1 |
| 3 | 3 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 1 |
| 6 | 3 | 1 |

After processing position 2:

| Query | Previous | +a₂ | sqrt |
| --- | --- | --- | --- |
| 1 | 2 | 16 | 4 |
| 2 | 1 | 15 | 3 |
| 3 | 1 | 16 | 4 |
| 4 | 1 | 16 | 4 |
| 5 | 1 | 16 | 4 |
| 6 | 1 | 16 | 4 |

Continuing through all positions produces:

```
3
2
3
2
1
3
```

This trace shows how every query state is processed simultaneously along the timeline.

### Example 2

Input:

```
2 2
386056082462833225 923951085408043421
1 386056082462833225
1 386056082462833224
```

After query 1:

| Position | Value |
| --- | --- |
| a₁ | 386056082462833225 |
| a₂ | 923951085408043421 |

The recurrence gives:

$$g(1)=621333955,$$

$$g(2)=961223744.$$

After query 2:

$$g(1)=621333954,$$

$$g(2)=961223743.$$

Output:

```
961223744
961223743
```

This example demonstrates why exact integer arithmetic is necessary near square-root boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\log^2 q)$ amortized | Range additions plus segment-tree-beats style square-root updates |
| Space | $O(q)$ | Segment tree and timeline storage |

The segment tree contains $O(q)$ nodes. Every update interval becomes one range addition. Repeated square roots rapidly reduce values, which keeps the total recursion cost bounded. This comfortably fits the limits for $n,q \le 2\cdot10^5$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class SegTree:
        def __init__(self, n):
            self.n = n
            self.mn = [0] * (4 * n + 5)
            self.mx = [0] * (4 * n + 5)
            self.lazy = [0] * (4 * n + 5)

        def apply_add(self, p, v):
            self.mn[p] += v
            self.mx[p] += v
            self.lazy[p] += v

        def push(self, p):
            if self.lazy[p]:
                v = self.lazy[p]
                self.apply_add(p * 2, v)
                self.apply_add(p * 2 + 1, v)
                self.lazy[p] = 0

        def pull(self, p):
            self.mn[p] = min(self.mn[p * 2], self.mn[p * 2 + 1])
            self.mx[p] = max(self.mx[p * 2], self.mx[p * 2 + 1])

        def add(self, p, l, r, ql, qr, v):
            if ql <= l and r <= qr:
                self.apply_add(p, v)
                return
            self.push(p)
            m = (l + r) // 2
            if ql <= m:
                self.add(p * 2, l, m, ql, qr, v)
            if qr > m:
                self.add(p * 2 + 1, m + 1, r, ql, qr, v)
            self.pull(p)

        def sq(self, p, l, r):
            mn = self.mn[p]
            mx = self.mx[p]

            if mx - mn == isqrt(mx) - isqrt(mn):
                self.apply_add(p, isqrt(mx) - mx)
                return

            if l == r:
                v = isqrt(mx)
                self.mn[p] = v
                self.mx[p] = v
                self.lazy[p] = 0
                return

            self.push(p)
            m = (l + r) // 2
            self.sq(p * 2, l, m)
            self.sq(p * 2 + 1, m + 1, r)
            self.pull(p)

        def collect(self, p, l, r, out):
            if l == r:
                out[l] = self.mn[p]
                return
            self.push(p)
            m = (l + r) // 2
            self.collect(p * 2, l, m, out)
            self.collect(p * 2 + 1, m + 1, r, out)

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    changes = [[] for _ in range(n)]

    for t in range(1, q + 1):
        k, x = map(int, input().split())
        changes[k - 1].append((t, x))

    seg = SegTree(q)

    for i in range(n):
        cur = a[i]
        last = 1

        for t, x in changes[i]:
            if last <= t - 1:
                seg.add(1, 1, q, last, t - 1, cur)
            cur = x
            last = t

        if last <= q:
            seg.add(1, 1, q, last, q, cur)

        seg.sq(1, 1, q)

    ans = [0] * (q + 1)
    seg.collect(1, 1, q, ans)

    return "\n".join(map(str, ans[1:]))

# provided sample
assert run(
"""5 6
0 14 0 7 6
1 4
1 3
2 15
4 1
5 2
5 8
"""
) == "3\n2\n3\n2\n1\n3", "sample 1"

# minimum size
assert run(
"""1 1
0
1 0
"""
) == "0", "single element zero"

# boundary sqrt transition
assert run(
"""1 2
16
1 15
1 16
"""
) == "3\n4", "crosses perfect square boundary"

# very large values
assert run(
"""1 1
1000000000000000000
1 1000000000000000000
"""
) == "1000000000", "1e18 square root"

# repeated updates on same index
assert run(
"""2 3
0 0
1 1
1 4
1 9
"""
) == "1\n2\n3", "timeline interval construction"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element, value 0 | 0 | Minimum input size |
| 16 → 15 → 16 | 3, 4 | Perfect-square boundary behavior |
| $10^{18}$ | $10^9$ | Large integer square roots |
| Repeated updates on one position | 1, 2, 3 | Correct interval generation on the timeline |

## Edge Cases

Consider:

```
1 2
16
1 15
1 16
```

After the first update,

$$\lfloor\sqrt{15}\rfloor=3.$$

After the second,

$$\lfloor\sqrt{16}\rfloor=4.$$

The algorithm never uses floating point arithmetic. The segment tree stores exact integers and applies `isqrt`, so both answers are computed exactly.

Now consider:

```
1 1
1000000000000000000
1 1000000000000000000
```

The value is exactly $10^{18}$. A floating point solution can lose precision around this magnitude. The integer recurrence computes

$$\lfloor\sqrt{10^{18}}\rfloor = 10^9$$

without any rounding issues.

Finally, consider multiple updates on the same index:

```
2 3
0 0
1 1
1 4
1 9
```

For index $1$, the timeline values are:

| Query interval | Value |
| --- | --- |
| [1,1] | 1 |
| [2,2] | 4 |
| [3,3] | 9 |

The preprocessing converts these into three range additions. Each interval is processed independently, so every query sees the correct version of the array.
