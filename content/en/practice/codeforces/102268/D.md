---
title: "CF 102268D - Dates"
description: "We have (t) calendar days, and day (x) can host at most (ax) dates. Each girl can be dated at most once, and girl (i) accepts any day from (li) through (ri). Dating her contributes (pi) to the answer."
date: "2026-08-19T04:18:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "D"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 1010
verified: false
draft: false
---

[CF 102268D - Dates](https://codeforces.com/problemset/problem/102268/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have (t) calendar days, and day (x) can host at most (a_x) dates. Each girl can be dated at most once, and girl (i) accepts any day from (l_i) through (r_i). Dating her contributes (p_i) to the answer. The task is to choose a subset of girls and assign every chosen girl a valid, capacity-respecting day so that the total pleasure is maximum.

The unusual structural condition is that both endpoints are sorted:

[
l_1\le l_2\le\cdots\le l_n,\qquad
r_1\le r_2\le\cdots\le r_n.
]

This condition is the key to making the matching constraints compressible. Without it, the natural formulation is a large weighted matching problem, which is far too expensive for (n,t\le 300000).

The bounds leave room for roughly (O((n+t)\log n)) operations, but not for quadratic work. A procedure that checks every pair of girls already has (O(n^2)) operations, around (9\cdot10^{10}) at the maximum size. Enumerating all subsets is obviously impossible, since there are (2^n) of them. The final solution uses sorting plus two lazy segment trees, giving (O((n+t)+n\log n)) time.

Several edge cases are easy to mishandle.

With no available capacity, the answer must be zero:

```
1 1
0
1 1 10
```

The answer is `0`. A careless solution that only checks whether each interval itself is nonempty would incorrectly select the girl.

Several girls can have exactly the same interval, but capacity is still shared. For example:

```
2 1
1
1 1 5
1 1 4
```

The answer is `5`, not `9`. Both girls can use only the single available slot.

Checking every selected interval independently is also insufficient. Consider:

```
2 2
1 0
1 1 100
1 2 99
```

Each girl individually has an interval containing at least one unit of capacity, but together they cannot be scheduled. The first girl consumes the only slot on day (1), while the second girl can only use day (1) because day (2) has capacity zero. The answer is `100`. This is exactly the kind of global condition captured by Hall's theorem.

Finally, boundaries must be handled inclusively. In

```
2 2
0 1
1 2 5
2 2 4
```

both girls can only use day (2), so only one can be selected and the answer is `5`. Treating an interval as half-open by accident would change the matching constraints.

The official statement confirms the endpoint ordering and the (300000) bounds that drive the (O(n\log n)) requirement.

## Approaches

The brute-force approach is to enumerate a subset of girls, determine whether those girls can be assigned to distinct available date slots, and keep the maximum pleasure among feasible subsets. It is correct because every possible choice of girls is considered. If the feasibility check itself greedily assigns the selected intervals to available slots, one subset can already require (O(n+t)) work, giving (O(2^n(n+t))) in the worst case. Even ignoring the feasibility cost, (2^{300000}) subsets cannot be processed.

The next natural idea is maximum-cost flow. Create capacity copies of every day and connect each girl to every day in her interval. That models the problem correctly, but the graph can contain (\Theta(nt)) edges, and a general matching or flow algorithm is much too slow.

The useful observation is that feasible sets of girls form a matroid. Think of every unit of daily capacity as a separate slot. A girl can be matched to any slot corresponding to a day in her interval. A set of girls is feasible exactly when these girls can be matched to distinct slots. Such matchable subsets form a transversal matroid. The weighted greedy theorem for matroids then says that we can process girls in decreasing order of pleasure and accept a girl precisely when adding her keeps the selected set feasible. This is the central optimization step.

The remaining problem is to test feasibility quickly.

Hall's theorem says that a selected set is schedulable exactly when every collection of girls has at least as many available day slots in its union of allowed days as there are selected girls. Because all allowed sets are intervals and both endpoint sequences are nondecreasing, it is sufficient to check contiguous blocks of girl indices. This turns a matching condition into inequalities over prefixes.

Let (b_i) be (1) if girl (i) has already been accepted and (0) otherwise. Let

[
A_x=\sum_{j=1}^{x}a_j
]

be the prefix capacity, and let

[
B_x=\sum_{j=1}^{x}b_j
]

be the prefix number of selected girls.

For a block of girls (L,\ldots,R), all of their possible days lie inside ([l_L,r_R]). Hall's condition becomes

[
B_R-B_{L-1}\le A_{r_R}-A_{l_L-1}.
]

Rearranging gives

[
B_R-A_{r_R}\le B_{L-1}-A_{l_L-1}.
]

Define

[
c_R=B_R-A_{r_R}
]

and

[
d_L=B_{L-1}-A_{l_L-1}.
]

The whole feasible set is characterized by

[
c_R\le d_L\qquad\text{for every }L\le R.
]

This is exactly the reduction used in the known solution for the problem.

Suppose we are considering girl (x). Before accepting her, (b_x=0). Adding her increases every (B_i) with (i\ge x), so every (c_i) with (i\ge x) increases by (1). It also increases (d_i) only when (i>x), because (d_i) contains (B_{i-1}). Thus the only new inequalities that can become harder are those with

[
L\le x\le R.
]

For those inequalities, (c_R) increases by (1), while (d_L) does not. Therefore girl (x) can be accepted exactly when

[
\max_{R\ge x}c_R < \min_{L\le x}d_L.
]

After accepting her, we add (1) to the suffix (c_x,\ldots,c_n), and add (1) to the suffix (d_{x+1},\ldots,d_n).

So we need one segment tree maintaining suffix maximums with range addition for (c), and another maintaining prefix minimums with range addition for (d).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n(n+t))) | (O(n+t)) | Too slow |
| Weighted matching / flow | At least superlinear in the full interval graph | Potentially (O(nt)) | Too slow |
| Greedy + two lazy segment trees | (O(t+n+n\log n)) | (O(t+n)) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix capacities (A_x), where (A_x) is the total number of date slots in days (1) through (x). This lets every capacity interval ([u,v]) be evaluated as (A_v-A_{u-1}) in constant time.
2. For every girl (i), initially no girl is selected, so (B_i=0). Store

[
c_i=-A_{r_i}
]

and

[
d_i=-A_{l_i-1}.
]

These are exactly the previous definitions with all (b_i=0).

1. Sort the girls by decreasing pleasure. The selected sets are independent in a transversal matroid, so accepting every feasible girl in this order produces a maximum-weight feasible set.
2. Consider the next girl (x). Query

[
C=\max_{i\ge x}c_i
]

from the first segment tree and

[
D=\min_{i\le x}d_i
]

from the second segment tree.

1. Accept girl (x) if (C<D). The strict inequality is necessary because accepting her increases every relevant (c_i) by exactly one. The old inequality must have at least one unit of slack.
2. If girl (x) is accepted, add (1) to (c_x,\ldots,c_n). This reflects that every (B_i) with (i\ge x) increases by one.
3. Also add (1) to (d_{x+1},\ldots,d_n). The value (d_i) contains (B_{i-1}), so it changes only when (i-1\ge x). There is deliberately no update to (d_x).
4. Add the girl's pleasure to the answer and continue with the next girl. If the girl fails the test, leave both trees unchanged and move on.

The invariant is that after processing any prefix of the pleasure-sorted order, the two trees represent exactly the values of (c_i) and (d_i) for the accepted girls. The condition for every pair (L\le R) is already satisfied. When a new girl is considered, only inequalities with (L\le x\le R) can become tighter. Those inequalities are valid after insertion exactly when the largest old (c_R) on the right is strictly smaller than the smallest old (d_L) on the left. Thus every accepted set is feasible, and every rejected girl would violate Hall's condition if added. Since the feasibility system is a matroid and girls are processed by decreasing weight, the resulting set has maximum total pleasure.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

INF = 10**30

class SegmentTree:
    def __init__(self, values, is_max):
        self.n = len(values)
        self.is_max = is_max
        size = 4 * self.n + 5
        self.val = array('q', [0]) * size
        self.tag = array('q', [0]) * size
        self.values = values
        self._build(1, 0, self.n - 1)

    def _merge(self, x, y):
        if self.is_max:
            return x if x > y else y
        return x if x < y else y

    def _build(self, v, l, r):
        if l == r:
            self.val[v] = self.values[l]
            return
        m = (l + r) >> 1
        self._build(v << 1, l, m)
        self._build(v << 1 | 1, m + 1, r)
        self.val[v] = self._merge(
            self.val[v << 1],
            self.val[v << 1 | 1]
        )

    def update_suffix(self, pos, delta=1):
        if pos >= self.n:
            return
        self._update(1, 0, self.n - 1, pos, delta)

    def _update(self, v, l, r, pos, delta):
        if pos <= l:
            self.val[v] += delta
            self.tag[v] += delta
            return

        m = (l + r) >> 1

        if pos <= m:
            self._update(v << 1, l, m, pos, delta)
        self._update(v << 1 | 1, m + 1, r, pos, delta)

        self.val[v] = self._merge(
            self.val[v << 1],
            self.val[v << 1 | 1]
        ) + self.tag[v]

    def query_suffix(self, pos):
        if pos >= self.n:
            return -INF if self.is_max else INF
        return self._query_suffix(1, 0, self.n - 1, pos)

    def _query_suffix(self, v, l, r, pos):
        if pos <= l:
            return self.val[v]

        m = (l + r) >> 1

        if pos <= m:
            left = self._query_suffix(v << 1, l, m, pos)
            right = self.val[v << 1 | 1]
            return self._merge(left, right) + self.tag[v]

        return self._query_suffix(v << 1 | 1, m + 1, r, pos) + self.tag[v]

    def query_prefix(self, pos):
        if pos < 0:
            return -INF if self.is_max else INF
        if pos >= self.n - 1:
            return self.val[1]
        return self._query_prefix(1, 0, self.n - 1, pos)

    def _query_prefix(self, v, l, r, pos):
        if r <= pos:
            return self.val[v]

        m = (l + r) >> 1

        if pos <= m:
            return self._query_prefix(v << 1, l, m, pos) + self.tag[v]

        left = self.val[v << 1]
        right = self._query_prefix(v << 1 | 1, m + 1, r, pos)
        return self._merge(left, right) + self.tag[v]

def solve():
    n, t = map(int, input().split())

    pref = [0] * (t + 1)
    cur = 0
    a = list(map(int, input().split()))

    for i, x in enumerate(a, 1):
        cur += x
        pref[i] = cur

    order = [None] * n
    c = [0] * n
    d = [0] * n

    for i in range(n):
        l, r, p = map(int, input().split())
        order[i] = (p, i)
        c[i] = -pref[r]
        d[i] = -pref[l - 1]

    order.sort(reverse=True)

    tree_c = SegmentTree(c, True)
    tree_d = SegmentTree(d, False)

    del c
    del d
    del pref
    del a

    ans = 0

    for p, x in order:
        right_c = tree_c.query_suffix(x)
        left_d = tree_d.query_prefix(x)

        if right_c < left_d:
            tree_c.update_suffix(x)
            tree_d.update_suffix(x + 1)
            ans += p

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix array is built first because every girl's initial (c_i) and (d_i) depends only on the total capacity up to her right or just before her left endpoint. Once these values have been initialized, the original (l_i) and (r_i) are no longer needed.

The `order` array stores only `(pleasure, index)`. Sorting it in reverse gives decreasing pleasure, which is exactly the order required by the matroid greedy algorithm. Python integers are arbitrary precision, so the total pleasure and prefix capacities do not risk 32-bit overflow.

The segment tree uses a slightly unusual lazy propagation style. `val[v]` already includes the lazy update belonging to node (v), while `tag[v]` records the amount that has not been incorporated into the children. When descending into a child, the parent's tag is added to the child's returned value. When rebuilding a parent, the merged child value is increased by the parent's tag. This avoids an explicit push operation and makes suffix updates particularly compact.

The first tree is a range-add, range-maximum structure for (c). The second is a range-add, range-minimum structure for (d). The candidate test queries exactly the two ranges appearing in

[
\max_{R\ge x}c_R < \min_{L\le x}d_L.
]

After acceptance, the suffix update on (c) starts at (x), while the suffix update on (d) starts at (x+1). That one-index difference is essential and is the most likely off-by-one mistake in the implementation.

## Worked Examples

### Sample 1

The actual sample input is:

```
3 5
0 1 0 1 0
1 2 2
2 4 1
3 5 5
```

The prefix capacities are

[
A=[0,0,1,1,2,2].
]

The initial (c_i=-A_{r_i}) and (d_i=-A_{l_i-1}) are:

[
c=[-1,-2,-2],
\qquad
d=[0,0,-1].
]

The girls are considered in pleasure order (3,1,2).

| Girl | Pleasure | (x) | (\max c[x..]) | (\min d[..x]) | Decision | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 5 | 2 | (-2) | (-1) | Accept | 5 |
| 1 | 2 | 0 | (-1) | (0) | Accept | 7 |
| 2 | 1 | 1 | (0) | (0) | Reject | 7 |

For girl (3), (-2<-1), so there is enough slack to insert her. After accepting her, (c_3) increases by one. Girl (1) also fits. When girl (2) is considered, the two sides are equal, so inserting her would make some Hall inequality fail by one unit. The final answer is `7`. This demonstrates why the acceptance test is strict.

### Boundary-heavy example

Consider:

```
2 2
1 0
1 1 100
1 2 99
```

The prefix capacities are (A=[0,1,1]). Initially,

[
c=[-1,-1],\qquad d=[0,0].
]

| Girl | Pleasure | (x) | (\max c[x..]) | (\min d[..x]) | Decision | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 100 | 0 | (-1) | (0) | Accept | 100 |
| 2 | 99 | 1 | (0) | (0) | Reject | 100 |

After accepting girl (1), the only capacity slot is consumed. Girl (2) overlaps that same effective capacity because day (2) has zero capacity, so the second candidate fails with equality. The output is `100`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t+n+n\log n)) | Prefix sums take (O(t)), sorting takes (O(n\log n)), and each girl performs a constant number of (O(\log n)) segment-tree operations |
| Space | (O(t+n)) | Prefix capacities, sorted candidates, and two segment trees all use linear memory |

With (n,t\le300000), the dominant term is (O(n\log n)), which is appropriate for the two-second target. The segment trees use compact 64-bit arrays in the Python implementation rather than ordinary Python integer arrays, keeping memory usage controlled.

## Test Cases

```python
import sys
import io
from array import array

input = sys.stdin.readline

INF = 10**30

class SegmentTree:
    def __init__(self, values, is_max):
        self.n = len(values)
        self.is_max = is_max
        size = 4 * self.n + 5
        self.val = array('q', [0]) * size
        self.tag = array('q', [0]) * size
        self.values = values
        self._build(1, 0, self.n - 1)

    def _merge(self, x, y):
        if self.is_max:
            return x if x > y else y
        return x if x < y else y

    def _build(self, v, l, r):
        if l == r:
            self.val[v] = self.values[l]
            return
        m = (l + r) >> 1
        self._build(v << 1, l, m)
        self._build(v << 1 | 1, m + 1, r)
        self.val[v] = self._merge(
            self.val[v << 1],
            self.val[v << 1 | 1]
        )

    def update_suffix(self, pos):
        if pos >= self.n:
            return
        self._update(1, 0, self.n - 1, pos)

    def _update(self, v, l, r, pos):
        if pos <= l:
            self.val[v] += 1
            self.tag[v] += 1
            return

        m = (l + r) >> 1

        if pos <= m:
            self._update(v << 1, l, m, pos)
        self._update(v << 1 | 1, m + 1, r, pos)

        self.val[v] = self._merge(
            self.val[v << 1],
            self.val[v << 1 | 1]
        ) + self.tag[v]

    def query_suffix(self, pos):
        if pos >= self.n:
            return -INF if self.is_max else INF
        return self._query_suffix(1, 0, self.n - 1, pos)

    def _query_suffix(self, v, l, r, pos):
        if pos <= l:
            return self.val[v]

        m = (l + r) >> 1

        if pos <= m:
            left = self._query_suffix(v << 1, l, m, pos)
            right = self.val[v << 1 | 1]
            return self._merge(left, right) + self.tag[v]

        return self._query_suffix(v << 1 | 1, m + 1, r, pos) + self.tag[v]

    def query_prefix(self, pos):
        if pos < 0:
            return -INF if self.is_max else INF
        if pos >= self.n - 1:
            return self.val[1]
        return self._query_prefix(1, 0, self.n - 1, pos)

    def _query_prefix(self, v, l, r, pos):
        if r <= pos:
            return self.val[v]

        m = (l + r) >> 1

        if pos <= m:
            return self._query_prefix(v << 1, l, m, pos) + self.tag[v]

        left = self.val[v << 1]
        right = self._query_prefix(v << 1 | 1, m + 1, r, pos)
        return self._merge(left, right) + self.tag[v]

def solve_case(inp):
    data = iter(inp.split())
    n = int(next(data))
    t = int(next(data))

    pref = [0] * (t + 1)
    for i in range(1, t + 1):
        pref[i] = pref[i - 1] + int(next(data))

    order = [None] * n
    c = [0] * n
    d = [0] * n

    for i in range(n):
        l = int(next(data))
        r = int(next(data))
        p = int(next(data))
        order[i] = (p, i)
        c[i] = -pref[r]
        d[i] = -pref[l - 1]

    order.sort(reverse=True)

    tc = SegmentTree(c, True)
    td = SegmentTree(d, False)

    ans = 0

    for p, x in order:
        if tc.query_suffix(x) < td.query_prefix(x):
            tc.update_suffix(x)
            td.update_suffix(x + 1)
            ans += p

    return str(ans)

def run(inp: str) -> str:
    return solve_case(inp)

# Provided sample.
assert run("""\
3 5
0 1 0 1 0
1 2 2
2 4 1
3 5 5
""") == "7", "sample 1"

# Minimum-size case with zero capacity.
assert run("""\
1 1
0
1 1 5
""") == "0", "minimum size and zero capacity"

# All girls have the same interval and compete for one slot.
assert run("""\
2 1
1
1 1 5
1 1 4
""") == "5", "shared single capacity"

# Boundary case where day 2 has no capacity.
assert run("""\
2 2
1 0
1 1 100
1 2 99
""") == "100", "Hall constraint across a boundary"

# All values equal, with enough total capacity for every girl.
assert run("""\
4 2
2 2
1 2 10
1 2 10
1 2 10
1 2 10
""") == "40", "all equal values"

# Maximum-size construction.
n = 300000
parts = [f"{n} {n}\n", ("1 " * (n - 1)) + "1\n"]
for i in range(1, n + 1):
    parts.append(f"{i} {i} 1\n")

large_input = "".join(parts)
assert run(large_input) == "300000", "maximum-size instance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0 / 1 1 5` | `0` | Minimum size and zero capacity |
| `2 1 / 1 / 1 1 5 / 1 1 4` | `5` | Multiple girls competing for one slot |
| `2 2 / 1 0 / 1 1 100 / 1 2 99` | `100` | Global Hall constraint and endpoint handling |
| `4 2 / 2 2 / four [1,2] intervals` | `40` | Equal intervals, equal pleasures, sufficient capacity |
| (n=t=300000), unit capacity and ([i,i]) intervals | `300000` | Maximum input size and linear-memory behavior |

## Edge Cases

When every capacity is zero, every initial (c_i) and (d_i) is zero. For a girl at position (x), the test compares a suffix maximum of zero with a prefix minimum of zero. Since (0<0) is false, nobody is accepted. For

```
1 1
0
1 1 10
```

the algorithm returns `0`, exactly as required.

When several girls share one day, the first one can be accepted, but the next one must fail. For

```
2 1
1
1 1 5
1 1 4
```

the first candidate satisfies (-1<0). After accepting her, the relevant (c) value becomes zero. The second candidate then sees (0<0) as false and is rejected. The result is `5`.

The global Hall constraint appears in

```
2 2
1 0
1 1 100
1 2 99
```

After accepting the first girl, the second candidate has (x=2) in one-based indexing. The right-side maximum (c) and left-side minimum (d) become equal, so the candidate is rejected. The segment tree is detecting that the two girls collectively require more capacity than the days can provide, even though each girl individually looks feasible.

For equal intervals, the algorithm does not rely on distinct endpoints. Consider four girls with interval ([1,2]), capacities (2,2), and pleasure (10) each. Every candidate passes because there are exactly four available slots. The suffix updates correctly accumulate four accepted girls, and the answer becomes `40`.

At the right boundary, accepting the last girl must not update (d_n), because (d_n) contains (B_{n-1}), not (B_n). This is why the implementation performs `tree_d.update_suffix(x + 1)` rather than `tree_d.update_suffix(x)`. For a final-position girl, this update is skipped completely. That boundary is what makes the prefix expression (B_{L-1}-A_{l_L-1}) line up with the Hall inequality.

The maximum-size case has (300000) girls and (300000) days, with one unit of capacity on every day and girl (i) restricted to day (i). Every girl is independently schedulable, so all (300000) girls are accepted and the answer is `300000`. The algorithm handles this in (O(n\log n)) time while keeping the segment-tree storage linear.
