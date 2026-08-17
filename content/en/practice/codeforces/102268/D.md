---
title: "CF 102268D - Dates"
description: "We have (t) days, where day (d) can host at most (ad) dates. Each girl is represented by an interval ([li,ri]) and a pleasure value (pi). If we choose her, we must assign her exactly one day inside that interval, and no day may receive more than its capacity."
date: "2026-08-17T18:40:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102268
codeforces_index: "D"
codeforces_contest_name: "300iq Contest 1"
rating: 0
weight: 102268
solve_time_s: 279
verified: false
draft: false
---

[CF 102268D - Dates](https://codeforces.com/problemset/problem/102268/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We have (t) days, where day (d) can host at most (a_d) dates. Each girl is represented by an interval ([l_i,r_i]) and a pleasure value (p_i). If we choose her, we must assign her exactly one day inside that interval, and no day may receive more than its capacity.

The task is to choose a subset of girls and assign every chosen girl to a legal day so that the total pleasure is as large as possible. The intervals are already ordered by both their left and right endpoints, although the solution below does not actually need that extra ordering property.

The bounds (n,t\le 300,000) immediately rule out anything that considers subsets of girls, or even anything quadratic in the number of girls. There can be (300,000) intervals, so the target is roughly (O((n+t)\log(n+t))). The pleasure values can reach (10^9), and there can be (300,000) selected girls, so the answer can be around (3\cdot10^{14}). Python integers handle this automatically, while a C++ implementation would need 64-bit integers.

The first edge case is zero capacity. Consider

```
1 2
0 0
1 2 10
```

The answer is (0), because the girl has an available interval but there is no usable day. An implementation that only checks whether every interval is nonempty would incorrectly select her.

The second edge case is several girls competing for the same single slot.

```
2 1
1
1 1 10
1 1 9
```

Only one girl can be selected, so the answer is (10). A careless algorithm that treats every girl independently, or only checks the total capacity against the number of girls without respecting their intervals, could incorrectly count both girls.

The third edge case concerns inclusive boundaries and intervals touching the ends of the schedule.

```
2 2
0 1
1 1 5
1 2 4
```

The answer is (4). The first girl can only use day (1), whose capacity is zero. The second girl can use day (2), so she is the only selectable girl. Treating ([l,r]) as a half-open interval, or accidentally shifting one endpoint in the feasibility check, can change this answer.

## Approaches

A direct solution would enumerate every subset of girls, then check whether that subset can be assigned to days. The check itself can be done greedily by processing days from left to right and assigning the available interval with the earliest deadline. That gives a correct brute-force method because every possible choice of girls is explicitly considered.

The problem is the number of subsets. There are (2^n) of them, so even an (O(n+t)) feasibility check would lead to (O(2^n(n+t))) work. With (n=300,000), this is not remotely feasible.

The key observation is that the feasible subsets have much more structure than an arbitrary collection of subsets. Think of every day as several identical slots, with (a_d) copies of day (d). A girl is connected to all slots belonging to days in her interval. A set of girls is feasible exactly when those girls can be matched to distinct slots.

The family of subsets that can be matched in a bipartite graph is a transversal matroid. Consequently, if we process girls in decreasing order of pleasure and add a girl whenever the resulting set remains feasible, the accepted set has maximum total weight. The exchange property behind this greedy rule is the reason we do not need dynamic programming over pleasure values. This matroid interpretation and the corresponding Hall-condition reduction are also the core of the known solution for this problem.

We are left with the real implementation problem: after accepting some high-value girls, how can we test whether another interval can be inserted in (O(\log t))?

Hall's theorem gives the answer. For any day interval ([L,R]), all selected girls whose entire availability interval is contained in ([L,R]) must fit into the capacity of those days. Thus a selected set (S) is feasible exactly when

[
#{[l_i,r_i]\in S\ge L,\ r_i\le R}
\le
\sum_{d=L}^{R}a_d
]

for every (1\le L\le R\le t).

Let

[
s_i=\sum_{d=1}^{i}a_d,\qquad s_0=0.
]

It is convenient to shift the left endpoint by one. Define, for (0\le i\le t),

[
p_i=s_i-#{[l,r]\in S\le i}
]

and

[
q_i=s_i-#{[l,r]\in S\le i}.
]

The Hall condition becomes

[
p_i\le q_j
]

for every (0\le i<j\le t). To see this, the difference (q_j-p_i) is exactly the capacity in days (i+1,\ldots,j), minus the number of selected intervals completely contained there.

Now suppose we want to insert ([l_0,r_0]). Adding it decreases every (p_i) with (i\ge l_0) by one and every (q_i) with (i\ge r_0) by one. The only potentially violated inequalities have (i<l_0) and (j\ge r_0). All other inequalities either remain unchanged or become easier to satisfy.

Therefore the insertion is feasible precisely when

[
\max_{0\le i<l_0}p_i
<
\min_{r_0\le j\le t}q_j.
]

A segment tree can maintain the maximum of (p), the minimum of (q), and lazy suffix additions. Every accepted interval performs two suffix decrements, one on (p) starting at (l_0), and one on (q) starting at (r_0).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n(n+t))) | (O(n+t)) | Too slow |
| Greedy + Hall condition + segment tree | (O(n\log n+n\log t+t)) | (O(n+t)) | Accepted |

## Algorithm Walkthrough

1. Read the day capacities and compute their prefix sums (s_0,s_1,\ldots,s_t). The prefix sums let us express the capacity of any consecutive block as one subtraction.
2. Sort all girls by decreasing pleasure. We will consider the most valuable girl first because the feasible sets form a matroid. The weighted matroid greedy theorem says that accepting the highest-value feasible element at every step produces a maximum-weight feasible set.
3. Initially no girl is selected, so both arrays satisfy (p_i=q_i=s_i). Build a segment tree whose leaves represent indices (0,\ldots,t). Each node stores the maximum (p_i) and minimum (q_i) in its range, together with lazy values for pending additions to the two arrays.
4. For a girl with interval ([l,r]), query the maximum (p_i) over (0\le i<l), and the minimum (q_j) over (r\le j\le t). If the first value is strictly smaller than the second, the girl can be added. The strict inequality is necessary because adding the girl decreases the relevant (q) values by exactly one.
5. If the girl is accepted, decrease (p_i) by one for every (i\ge l), and decrease (q_i) by one for every (i\ge r). Both operations are suffix range additions, so the segment tree handles them in logarithmic time.
6. Add the girl's pleasure to the answer whenever the insertion succeeds. If the feasibility test fails, leave the segment tree unchanged and continue with the next girl.

The invariant is that after processing any prefix of the pleasure-sorted girls, the segment tree represents exactly the (p) and (q) values for the accepted girls, and those accepted girls form a feasible set. For an unselected interval ([l,r]), the only Hall inequalities that can become false after inserting it are the pairs with (i<l) and (j\ge r). The segment tree checks the strongest such inequality by comparing the largest possible (p_i) with the smallest possible (q_j). Hence every accepted girl preserves feasibility, while every rejected girl cannot be added to the current set. Since the candidates are processed in decreasing weight and feasible sets form a matroid, the resulting set has maximum total pleasure.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array

def solve():
    n, t = map(int, input().split())
    a = list(map(int, input().split()))

    girls = []
    for _ in range(n):
        l, r, p = map(int, input().split())
        girls.append((l, r, p))

    girls.sort(key=lambda x: x[2], reverse=True)

    # Prefix capacities s[0..t].
    pref = array('q', [0]) * (t + 1)
    cur = 0
    for i, x in enumerate(a, 1):
        cur += x
        pref[i] = cur

    # Segment tree over indices 0..t.
    size = 4 * (t + 1) + 5

    # Maximum p in a node.
    mxp = array('q', [0]) * size

    # Minimum q in a node.
    mnq = array('q', [0]) * size

    # Lazy suffix additions for p and q.
    lazy_p = array('i', [0]) * size
    lazy_q = array('i', [0]) * size

    def build(v, lo, hi):
        if lo == hi:
            x = pref[lo]
            mxp[v] = x
            mnq[v] = x
            return

        mid = (lo + hi) >> 1
        left = v << 1
        right = left | 1

        build(left, lo, mid)
        build(right, mid + 1, hi)

        mxp[v] = max(mxp[left], mxp[right])
        mnq[v] = min(mnq[left], mnq[right])

    def push(v):
        lp = lazy_p[v]
        lq = lazy_q[v]

        if lp:
            left = v << 1
            right = left | 1

            mxp[left] += lp
            mxp[right] += lp
            lazy_p[left] += lp
            lazy_p[right] += lp

            lazy_p[v] = 0

        if lq:
            left = v << 1
            right = left | 1

            mnq[left] += lq
            mnq[right] += lq
            lazy_q[left] += lq
            lazy_q[right] += lq

            lazy_q[v] = 0

    def max_prefix(v, lo, hi, qr):
        if hi <= qr:
            return mxp[v]

        push(v)
        mid = (lo + hi) >> 1
        left = v << 1
        right = left | 1

        if qr <= mid:
            return max_prefix(left, lo, mid, qr)

        x = maxp = mxp[left]
        y = max_prefix(right, mid + 1, hi, qr)
        return x if x > y else y

    def min_suffix(v, lo, hi, ql):
        if lo >= ql:
            return mnq[v]

        push(v)
        mid = (lo + hi) >> 1
        left = v << 1
        right = left | 1

        if ql > mid:
            return min_suffix(right, mid + 1, hi, ql)

        x = min_suffix(left, lo, mid, ql)
        y = mnq[right]
        return x if x < y else y

    def update(v, lo, hi, pl, ql):
        # No part of this segment belongs to either suffix.
        if hi < pl:
            return

        # Both suffixes fully cover this node.
        if lo >= ql:
            mxp[v] -= 1
            mnq[v] -= 1
            lazy_p[v] -= 1
            lazy_q[v] -= 1
            return

        # Only the p suffix fully covers this node.
        if lo >= pl and hi < ql:
            mxp[v] -= 1
            lazy_p[v] -= 1
            return

        if lo == hi:
            return

        # If p covers the whole node but q only covers part of it,
        # apply p here and descend for q.
        if lo >= pl:
            mxp[v] -= 1
            lazy_p[v] -= 1

        push(v)

        mid = (lo + hi) >> 1
        left = v << 1
        right = left | 1

        update(left, lo, mid, pl, ql)
        update(right, mid + 1, hi, pl, ql)

        mxp[v] = max(mxp[left], mxp[right])
        mnq[v] = min(mnq[left], mnq[right])

    build(1, 0, t)

    answer = 0

    for l, r, pleasure in girls:
        # The affected Hall inequalities have i < l and j >= r.
        left_max = max_prefix(1, 0, t, l - 1)
        right_min = min_suffix(1, 0, t, r)

        if left_max < right_min:
            answer += pleasure
            update(1, 0, t, l, r)

    return answer

if __name__ == "__main__":
    print(solve())
```

The `pref` array stores (s_i), including (s_0=0). Using indices from (0) through (t) is what makes the Hall condition naturally become (p_i\le q_j) for (i<j). The query for a girl beginning at (l) is therefore exactly the prefix (0,\ldots,l-1), while the query for her ending at (r) is the suffix (r,\ldots,t).

The segment tree stores `mxp` because insertion needs the largest left-side (p), and `mnq` because insertion needs the smallest right-side (q). The two lazy arrays are separate because the two suffixes generally begin at different positions.

The `update` function handles both suffix decrements in one traversal. Since (l\le r), the two update boundaries occur in sorted order. A node can be completely outside both suffixes, completely inside both, completely inside only the (p) suffix, or straddle one of the boundaries. This keeps each insertion logarithmic rather than performing (O(t)) individual decrements.

The comparison uses `<`, not `<=`. Suppose before insertion the strongest affected inequality is (p_i=q_j). Adding the interval decreases (q_j) by one, so the new inequality becomes (p_i\le q_j-1), which fails. Thus equality before insertion means the candidate must be rejected.

Python integers would safely hold every prefix capacity and the final answer, but the segment tree uses `array('q')` for its large numeric fields to avoid the memory overhead of millions of Python integer objects. The lazy values only range between roughly (-n) and (0), so signed 32-bit storage is sufficient for them.

## Worked Examples

### Sample 1

The official sample is

```
3 5
0 1 0 1 0
1 2 2
2 4 1
3 5 5
```

The prefix capacities are

[
s=[0,0,1,1,2,2].
]

The girls are processed in pleasure order: ([3,5]) with pleasure (5), then ([1,2]) with pleasure (2), then ([2,4]) with pleasure (1).

| Girl | (l,r) | max (p_i), (i<l) | min (q_j), (j\ge r) | Decision | Answer |
| --- | --- | --- | --- | --- | --- |
| pleasure 5 | 3, 5 | 1 | 2 | accept | 5 |
| pleasure 2 | 1, 2 | 0 | 1 | accept | 7 |
| pleasure 1 | 2, 4 | 0 | 0 | reject | 7 |

After accepting ([3,5]), the (p) values at indices (3,4,5) decrease by one, while only (q_5) decreases. Accepting ([1,2]) then decreases (p_1,\ldots,p_5) and (q_2,\ldots,q_5). For the final interval ([2,4]), the best left-side (p) is already equal to the smallest right-side (q), so inserting it would violate Hall's condition.

The selected girls can be scheduled on day (2) and day (4), giving pleasure (2+5=7). This also demonstrates why the candidate with pleasure (1) must be rejected even though some capacity remains elsewhere.

### Custom contention example

Consider

```
2 1
1
1 1 10
1 1 9
```

There is only one available date slot.

| Girl | (l,r) | max (p_i), (i<l) | min (q_j), (j\ge r) | Decision | Answer |
| --- | --- | --- | --- | --- | --- |
| pleasure 10 | 1, 1 | 0 | 1 | accept | 10 |
| pleasure 9 | 1, 1 | 0 | 0 | reject | 10 |

After the first girl is accepted, both (p_1) and (q_1) become zero. The second insertion would require (0<0), which is false. The data structure therefore captures the exact one-slot capacity constraint without explicitly constructing a matching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t+n\log n+n\log t)) | Prefix sums take (O(t)), sorting takes (O(n\log n)), and every girl performs logarithmic segment-tree work |
| Space | (O(n+t)) | The girls, prefix sums, and segment-tree arrays are all linear in the input size |

With (n,t\le300,000), the solution performs only a logarithmic amount of data-structure work for each girl after sorting. The segment tree contains (O(t)) nodes, and the compact numeric arrays keep its memory usage within the 256 MiB limit stated by the official problem.

## Test Cases

The following harness assumes the `solve()` function from the previous section is in the same Python file. It temporarily replaces `stdin` and the global `input` function so every assertion exercises the actual solution.

```python
# Place this harness in the same file as solve().

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        return str(solve()).strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample.
assert run(
    """3 5
0 1 0 1 0
1 2 2
2 4 1
3 5 5
"""
) == "7", "sample 1"

# Minimum-size case, with zero capacity.
assert run(
    """1 1
0
1 1 9
"""
) == "0", "minimum size and zero capacity"

# Two girls need the same single day.
assert run(
    """2 1
1
1 1 10
1 1 9
"""
) == "10", "single-slot contention"

# All capacities, intervals, and pleasures are equal.
assert run(
    """3 3
1 1 1
1 3 7
1 3 7
1 3 7
"""
) == "21", "equal values and tie handling"

# Boundary-heavy case.
assert run(
    """3 3
0 1 0
1 1 5
2 2 7
1 3 6
"""
) == "7", "inclusive interval boundaries"

# Maximum-size structural test.
N = 300_000
lines = [
    f"{N} {N}",
    " ".join(["1"] * N),
]
lines.extend(["1 300000 1"] * N)

assert run("\n".join(lines) + "\n") == "300000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0 / 1 1 9` | 0 | Minimum input and zero capacity |
| `2 1 / 1 / 1 1 10 / 1 1 9` | 10 | Two intervals competing for one slot |
| `3 3 / 1 1 1 / 1 3 7` repeated | 21 | Equal capacities, intervals, pleasures, and sorting ties |
| `3 3 / 0 1 0 / 1 1 5 / 2 2 7 / 1 3 6` | 7 | Inclusive boundaries and unavailable endpoint days |
| Generated (300000)-girl instance | 300000 | Maximum (n,t), segment-tree performance, and large answer |

## Edge Cases

### Zero capacity

For

```
1 2
0 0
1 2 10
```

the initial prefix capacities are (s=[0,0,0]), so (p=q=[0,0,0]). For the only girl, the left query gives (p_0=0), while the right query gives (\min(q_2)=0). The required strict inequality (0<0) fails, so the girl is rejected and the answer remains (0).

The algorithm does not need a special case for zero-capacity days. They simply appear as equal prefix values, and the Hall inequality detects that no date can be assigned.

### Multiple girls competing for one day

For

```
2 1
1
1 1 10
1 1 9
```

the initial arrays are (p=q=[0,1]). The pleasure (10) girl is accepted because (p_0=0<q_1=1). The suffix update makes both values at index (1) equal to zero.

When the pleasure (9) girl is considered, the test becomes (p_0=0<q_1=0), which fails. The algorithm returns (10), exactly matching the fact that one day has only one slot.

### Inclusive endpoints and zero capacity at a boundary

For

```
3 3
0 1 0
1 1 5
2 2 7
1 3 6
```

the highest-value girl is ([2,2]), so she is accepted using the only usable day. The ([1,3]) girl is considered next, but she competes for that same remaining capacity and cannot be added. The ([1,1]) girl can only use day (1), whose capacity is zero, so she is also rejected.

The answer is (7). The segment-tree indices (0,\ldots,t) make the left boundary (l=1) correspond to the prefix containing only index (0), while the right boundary (r=3) starts the suffix at index (3). This is exactly the shift needed by the Hall formulation and avoids an off-by-one interpretation of the original day intervals.

### A candidate that is globally possible but locally impossible

Consider

```
3 3
1 0 1
1 1 100
2 3 60
1 3 70
```

The first girl has value (100) and can only use day (1), so she is accepted. The second girl has value (70) and can use days (1) through (3), but after the first acceptance she can still use day (3), so she is also accepted. The third girl has value (60) and can use days (2) or (3), but day (2) has no capacity and day (3) is already needed by the flexible (70)-value girl. The Hall test rejects her.

This illustrates why checking only the total remaining capacity is insufficient. Feasibility depends on where that capacity occurs, and the (p,q) transformation compresses all interval Hall constraints into the two extrema queried by the segment tree.
