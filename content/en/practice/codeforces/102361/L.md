---
title: "CF 102361L - MUV LUV ALTERNATIVE"
description: "The cabin is a rectangular grid, but most cells are not equally useful. There are two vertical corridors, each one cell wide. The first corridor is immediately after the left seated zone, and the second corridor is immediately after the middle seated zone."
date: "2026-08-13T00:22:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "L"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 284
verified: true
draft: false
---

[CF 102361L - MUV LUV ALTERNATIVE](https://codeforces.com/problemset/problem/102361/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The cabin is a rectangular grid, but most cells are not equally useful. There are two vertical corridors, each one cell wide. The first corridor is immediately after the left seated zone, and the second corridor is immediately after the middle seated zone. Only corridor cells allow vertical movement. Every soldier starts inside one of the three seated zones, where movement is initially horizontal.

A soldier from the left zone must eventually use the left corridor and leave through its exit. A soldier from the right zone must use the right corridor. A soldier from the middle zone may choose either corridor. Once a soldier reaches a corridor, it can move downward one row per unit of time and eventually reach the corresponding exit.

The input gives the number of rows, the widths of the three seated zones, and the number of soldiers. Each soldier is described by its zone and its initial row and column. The required output is the minimum integer time by which every soldier can be outside the cabin.

The largest parameter values are around (10^9), while the number of soldiers can reach (10^5). We cannot construct the grid, simulate every cell, or simulate every movement step. Even a simulation that processes every soldier once per moment can require around (10^{14}) soldier updates on a large instance. The solution has to depend on the (10^5) input records rather than on the (10^9)-sized geometry.

There are several boundary cases that expose mistakes in the model. With one soldier in the smallest possible cabin, the answer is not one because a soldier starts in a seated cell and must first enter a corridor. For example, with `1 1 1 1 1` and the soldier at `(1,1)`, the left corridor is column 2, so the soldier needs one horizontal move and one downward move. The answer is `2`. A solution that treats the corridor exit as if it were horizontally adjacent to the starting cell would incorrectly return `1`.

Another subtle case is when several soldiers have the same earliest exit time. For example, with `1 1 1 1 3`, put soldiers at `(1,1)`, `(1,3)`, and `(1,5)`, belonging to the left, middle, and right zones respectively. Every soldier can reach its chosen corridor and exit in two steps individually, but three soldiers cannot all use their corridors with exit time two when the middle soldier chooses one side. Two soldiers must share a corridor, so one of them needs a later exit time. The correct answer is `3`. Treating every soldier's shortest path independently would give the wrong answer `2`.

A third common mistake is forgetting that a soldier can wait. Two soldiers approaching the same corridor from opposite sides can avoid a collision by delaying one of them before entering the corridor. The relevant constraint is not that their entry times must be distinct, but that their eventual exit times through that corridor must be distinct.

## Approaches

The most direct brute force is to decide which exit every middle-zone soldier uses, then solve the movement problem for the resulting two groups. If there are (s) middle-zone soldiers, there are (2^s) assignments. With (s=100000), this means (2^{100000}) different assignments before considering the cost of checking even one assignment. A more literal simulation is also hopeless. If every moment scans all (10^5) soldiers and the evacuation takes on the order of (10^9) moments, the simulation performs around (10^{14}) soldier updates.

The key observation is to stop thinking about the entire corridor and instead describe a soldier by the time at which it leaves through the exit. Suppose a soldier enters a corridor at time (s), starting at row (x). Its exit time is (s+x). If we prescribe its exit time as (e), its path inside the corridor is completely determined: at time (t), its row is (e-t). Two soldiers using the same corridor collide exactly when they have the same exit time. Thus the only requirement inside one corridor is that all assigned soldiers receive distinct integer exit times.

For a soldier, let (p_L) be its earliest possible exit time through the left exit, and (p_R) its earliest possible exit time through the right exit. A soldier assigned to the left corridor may use any integer exit time in the interval ([p_L,T]), where (T) is a proposed final time. The same holds for the right corridor.

This turns the geometric problem into a matching problem. There are (T) possible exit-time slots on each corridor. A soldier is connected to a suffix of the left slots and a suffix of the right slots. Reversing the order of time turns those suffixes into prefixes, which gives a particularly convenient form of Hall's condition.

For a fixed (T), define

[
d_L=\max(0,T-p_L+1), \qquad d_R=\max(0,T-p_R+1).
]

The value (d_L) is the number of reversed-time slots available to the soldier on the left corridor. A value of zero means that the soldier cannot use that corridor by time (T).

Consider taking the first (a) reversed-time slots on the left and the first (b) on the right. A soldier is forced into this set precisely when (d_L\le a) and (d_R\le b). Such soldiers must all fit into the (a+b) slots. Hence the feasibility condition is

[
#{i:d_{L,i}\le a,\ d_{R,i}\le b}\le a+b
]

for every (a,b).

Because every soldier's available slots are prefixes, checking these pairs of prefixes is sufficient by Hall's theorem. We can sweep (a) from small to large. When a soldier becomes active, it contributes one to every (b) satisfying (b\ge d_R). Thus the quantity

[
#{d_R\le b}-b
]

receives a range addition on a suffix. A segment tree can maintain its maximum.

There is a useful transformation that avoids explicitly constructing all (d_R) values for every binary-search iteration. Put

[
q=T+1-b.
]

Then (d_R\le b) is equivalent to (p_R\ge q), including the case where the soldier cannot use the right corridor by treating its right-side earliest time as infinity. The Hall condition becomes

[
q+#{p_R\ge q}\le T+1+a.
]

For every active soldier, its insertion adds one to every threshold (q\le p_R). We maintain the maximum value of (q+\text{count}(p_R\ge q)) with a segment tree supporting prefix range additions.

The resulting algorithm performs a binary search on (T). Each feasibility check takes (O(k\log k)), so the complete complexity is (O(k\log k\log C)), where (C) is the numerical range of the answer. With (C) around (10^9), the extra logarithmic factor is only about 31.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over middle assignments | (O(2^k\cdot k\log k)) | (O(k)) | Too slow |
| Time-step simulation | (O(kT)) | (O(k)) | Too slow |
| Optimal Hall-condition check with binary search | (O(k\log k\log C)) | (O(k)) | Accepted |

## Algorithm Walkthrough

1. Convert every soldier into its earliest possible exit time for each corridor. Let the left corridor be column (c_1=l_1+1), and the right corridor be column (c_2=l_1+l_2+2).

A left-zone soldier has only the left value

[
p_L=x+c_1-y.
]

A right-zone soldier has only the right value

[
p_R=x+y-c_2.
]

A middle-zone soldier has both

[
p_L=x+y-c_1,
\qquad
p_R=x+c_2-y.
]

For a corridor that the soldier is forbidden to use, store a very large sentinel value.
2. Given a candidate evacuation time (T), convert each earliest exit time into a deadline in reversed time.

For a finite earliest time (p), the number of usable reversed-time slots is

[
d=\max(0,T-p+1).
]

A soldier can use the corridor if and only if (d>0).
3. Use Hall's theorem to characterize feasibility. For any (a) left slots and (b) right slots at the beginning of reversed time, every soldier satisfying (d_L\le a) and (d_R\le b) has its complete neighborhood inside those (a+b) slots. Therefore such soldiers must be no more than (a+b).

Since the neighborhoods are prefixes, these prefix pairs are enough to test the complete bipartite matching.
4. Sweep the value (a) from small to large. When (a) reaches a soldier's (d_L), that soldier becomes active. For the current active set, we need

[
\max_b\left(#{d_R\le b}-b\right)\le a.
]

Every newly active soldier with right deadline (d_R) increases the count for every (b\ge d_R). This is exactly a suffix range addition.
5. Rewrite the right-side expression using (q=T+1-b). The condition becomes

[
\max_q\left(q+#{p_R\ge q}\right)\le T+1+a.
]

A newly active soldier with right earliest time (p_R) increases the maintained value for every (q\le p_R), so we need a prefix range addition and a global maximum query.

Only thresholds equal to an existing finite (p_R), together with (T+1), can be relevant. Between two consecutive thresholds the count is constant while (q) increases, so the largest endpoint is always sufficient.
6. Sort soldiers by decreasing (p_L). As (T) is fixed, this is the same as processing increasing (d_L). Soldiers with (p_L>T), including soldiers forbidden from the left corridor, all have (d_L=0) and are inserted first. Then equal finite (p_L) values are processed as one group.
7. For every active group, update the segment tree for its right-side threshold. If (p_R>T), the soldier cannot use the right corridor, so it contributes to every valid threshold up to (T+1). Otherwise it contributes to all thresholds (q\le p_R).
8. After each group, compare the segment tree maximum with (T+1+a). If the maximum is larger, Hall's condition is violated and (T) is impossible.
9. Obtain an upper bound by assigning every middle-zone soldier to the left corridor, scheduling all left-zone and middle-zone soldiers together, and scheduling the right-zone soldiers independently. For one corridor, sort all earliest exit times and assign the earliest possible distinct exit times. Binary-search between zero and this guaranteed feasible upper bound.

### Why it works

The central invariant is that a corridor schedule is completely characterized by distinct integer exit times. A soldier with earliest possible exit time (p) can receive exactly any exit time at least (p), so for a fixed (T) its possible slots form a suffix. Reversing time turns every possible slot set into a prefix.

Hall's theorem says that a matching exists exactly when every set of slots contains enough capacity for all soldiers whose entire neighborhood lies inside it. Because every neighborhood is a union of two prefixes, the potentially tight slot sets can be represented by taking a prefix of the left corridor and a prefix of the right corridor. The segment tree checks all such pairs simultaneously.

The binary search is valid because if evacuation is possible in (T) moments, it remains possible in any larger number of moments. Thus the feasibility predicate is monotone, and the smallest feasible (T) is exactly the required answer.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

INF = 10**30
NEG = -10**30

class SegTree:
    def __init__(self, values):
        n = len(values)
        size = 1
        while size < n:
            size <<= 1

        self.size = size
        self.mx = [NEG] * (size << 1)
        self.lazy = [0] * (size << 1)

        base = size
        for i, v in enumerate(values):
            self.mx[base + i] = v

        for i in range(size - 1, 0, -1):
            self.mx[i] = max(self.mx[i << 1], self.mx[i << 1 | 1])

    def _add(self, node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            self.mx[node] += value
            self.lazy[node] += value
            return

        mid = (left + right) >> 1

        if ql <= mid:
            self._add(node << 1, left, mid, ql, qr, value)
        if mid < qr:
            self._add(node << 1 | 1, mid + 1, right, ql, qr, value)

        self.mx[node] = (
            self.lazy[node]
            + max(self.mx[node << 1], self.mx[node << 1 | 1])
        )

    def add_prefix(self, right, value):
        if right < 0:
            return
        if right >= self.size:
            right = self.size - 1
        self._add(1, 0, self.size - 1, 0, right, value)

    @property
    def maximum(self):
        return self.mx[1]

def corridor_cost(values):
    if not values:
        return 0

    values.sort()

    current = 0
    for p in values:
        current = max(p, current + 1)

    return current

def solve():
    n, l1, l2, l3, k = map(int, input().split())

    c1 = l1 + 1
    c2 = l1 + l2 + 2

    jobs = []
    left_fixed = []
    right_fixed = []
    middle = []

    for _ in range(k):
        a, x, y = map(int, input().split())

        if a == 1:
            p_l = x + c1 - y
            p_r = INF
            left_fixed.append(p_l)
        elif a == 2:
            p_l = x + y - c1
            p_r = x + c2 - y
            middle.append((p_l, p_r))
        else:
            p_l = INF
            p_r = x + y - c2
            right_fixed.append(p_r)

        jobs.append((p_l, p_r))

    # A guaranteed feasible solution:
    # send every middle-zone soldier to the left corridor.
    upper = max(
        corridor_cost(left_fixed + [p_l for p_l, _ in middle]),
        corridor_cost(right_fixed[:])
    )

    finite_right = sorted({p_r for _, p_r in jobs if p_r < INF})
    right_rank = {v: i for i, v in enumerate(finite_right)}

    jobs_by_left = sorted(jobs, key=lambda z: z[0], reverse=True)

    def feasible(T):
        # Only p_R values <= T are useful coordinates.
        m = bisect_right(finite_right, T)

        # q values are all useful p_R thresholds plus q = T + 1.
        coords = finite_right[:m]
        coords.append(T + 1)

        seg = SegTree(coords)

        idx = 0
        total = len(jobs_by_left)

        # All jobs with p_L > T, and all jobs forbidden from the
        # left corridor, have d_L = 0.
        while idx < total and jobs_by_left[idx][0] > T:
            p_r = jobs_by_left[idx][1]

            if p_r >= INF or p_r > T:
                seg.add_prefix(m, 1)
            else:
                seg.add_prefix(right_rank[p_r], 1)

            idx += 1

        # At a = 0, all d_L = 0 jobs are active.
        if seg.maximum > T + 1:
            return False

        # For finite p_L <= T, equal p_L values have the same d_L.
        while idx < total:
            p_l = jobs_by_left[idx][0]
            a = T - p_l + 1

            j = idx
            while j < total and jobs_by_left[j][0] == p_l:
                p_r = jobs_by_left[j][1]

                if p_r >= INF or p_r > T:
                    seg.add_prefix(m, 1)
                else:
                    seg.add_prefix(right_rank[p_r], 1)

                j += 1

            if seg.maximum > T + 1 + a:
                return False

            idx = j

        return True

    lo = 0
    hi = upper

    while lo < hi:
        mid = (lo + hi) >> 1
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The first part of the implementation converts the geometric coordinates into the two earliest exit times. The corridor columns are `c1 = l1 + 1` and `c2 = l1 + l2 + 2`, so the horizontal distance is obtained directly from the column difference.

`INF` represents an exit that a soldier is not allowed to use. It is deliberately much larger than every possible real time, so in a feasibility check such a soldier receives zero available slots on that corridor.

The `corridor_cost` function is used only for the initial upper bound. If the earliest exit times on one corridor are sorted as (p_1\le p_2\le\cdots), the earliest distinct exit times are obtained by repeatedly taking `max(p_i, previous + 1)`. This also demonstrates why collisions inside a corridor reduce to distinct exit times.

The segment tree stores values of the form

[
q+#{p_R\ge q}.
]

Its leaves start with the threshold `q`. Activating a soldier adds one to every threshold not larger than its `p_R`, which is exactly a prefix range addition. The root stores the maximum over all thresholds.

The special threshold `T + 1` represents (b=0), meaning that no right-corridor reversed-time slot is available. It is needed for soldiers that are forced onto the left corridor. Values of `p_R` greater than `T` have the same effect, so they update the entire valid threshold range.

The sweep order is decreasing `p_L`. Since

[
d_L=\max(0,T-p_L+1),
]

decreasing `p_L` is exactly increasing `d_L`. All values with `p_L>T` are processed together at (a=0). Equal finite `p_L` values are also processed together because they have the same Hall parameter (a).

Python integers have arbitrary precision, so the (10^9)-sized coordinates and all accumulated scheduling times are safe. The large `INF` and `NEG` values are far outside the possible answer range and only serve as sentinels.

## Worked Examples

For the provided sample, the two corridor columns are (3) and (6).

The two left-zone soldiers have earliest left exit times (4) and (3). The middle soldier has earliest left exit time (3) and earliest right exit time (4).

| Soldier | Zone | (p_L) | (p_R) |
| --- | --- | --- | --- |
| A | 1 | 4 | INF |
| B | 1 | 3 | INF |
| C | 2 | 3 | 4 |

For (T=3), the reversed deadlines are

| Soldier | (d_L) | (d_R) |
| --- | --- | --- |
| A | 0 | 0 |
| B | 1 | 0 |
| C | 1 | 0 |

Taking (a=1,b=0), all three soldiers satisfy (d_L\le1) and (d_R\le0), so they would all have to fit into only one left slot. The Hall inequality becomes (3\le1), which fails.

For (T=4), the deadlines become

| Soldier | (d_L) | (d_R) |
| --- | --- | --- |
| A | 1 | 0 |
| B | 2 | 0 |
| C | 2 | 1 |

The tight conditions are now satisfied. For example, (a=2,b=1) contains all three soldiers and has three available slots, giving (3\le3). Hence (T=4) is feasible, while (T=3) is not, so the answer is `4`.

This matches the actual movement schedule. The two left soldiers can leave at times (3) and (4), while the middle soldier uses the right corridor and leaves at time (4).

For a second example, consider

```
1 1 1 1 3
1 1 1
2 1 3
3 1 5
```

The corridors are columns (2) and (4). Every soldier has an earliest possible exit time of (2).

| Soldier | Zone | (p_L) | (p_R) |
| --- | --- | --- | --- |
| A | 1 | 2 | INF |
| B | 2 | 2 | 2 |
| C | 3 | INF | 2 |

Trying (T=2) gives

| Soldier | (d_L) | (d_R) |
| --- | --- | --- |
| A | 1 | 0 |
| B | 1 | 1 |
| C | 0 | 1 |

For (a=1,b=1), all three soldiers satisfy the two deadline conditions, but there are only two slots. The inequality (3\le2) fails.

At (T=3), the deadlines become

| Soldier | (d_L) | (d_R) |
| --- | --- | --- |
| A | 2 | 0 |
| B | 2 | 2 |
| C | 0 | 2 |

Every Hall condition is satisfied. One possible assignment sends A and B through the left corridor and C through the right corridor. The left corridor uses exit times (2) and (3), while the right corridor uses exit time (2). The answer is `3`.

This example catches duplicate earliest exit times. Individual shortest paths are all length two, but two soldiers using the same corridor need different exit times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(k\log k\log C)) | Sorting takes (O(k\log k)), each feasibility check uses (O(k\log k)), and binary search performs (O(\log C)) checks |
| Space | (O(k)) | The soldiers, compressed right-side thresholds, and segment tree all use linear space |

With (k\le100000), the algorithm never depends on the grid dimensions themselves. Values such as (n,l_1,l_2,l_3) can be (10^9) without increasing the data structure size. The only numerical factor is the binary search over the answer, which needs roughly 31 iterations when the answer is below a few billion.

## Test Cases

```python
# The solve() function from the previous section is assumed to be defined.

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()

        # solve() writes directly to stdout, so this helper is intended
        # to be adapted with an output capture in an actual test harness.
        # A convenient contest-style version is shown below instead.
    finally:
        sys.stdin = old_stdin
        input = old_input

    return ""

# For a fully executable harness, redirect stdout as well.

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided sample
assert run(
    """4 2 2 2 3
1 2 1
1 2 2
2 2 4
"""
) == "4", "provided sample"

# Minimum-size cabin, one soldier in the left zone.
assert run(
    """1 1 1 1 1
1 1 1
"""
) == "2", "minimum cabin"

# One soldier on each side. Both can leave at time 2.
assert run(
    """1 1 1 1 2
1 1 1
3 1 5
"""
) == "2", "independent corridors"

# Three soldiers with identical earliest exit time.
# Two of them must share one corridor, so the answer is 3.
assert run(
    """1 1 1 1 3
1 1 1
2 1 3
3 1 5
"""
) == "3", "duplicate earliest exit times"

# Boundary case around both corridor columns.
assert run(
    """1 2 1 2 2
1 1 2
2 1 4
"""
) == "3", "corridor boundary"

# Large coordinates and maximum number of soldiers.
# All soldiers are in the left zone at row 1.
# Their earliest times are consecutive and the largest is 1000000001.
parts = ["1000000000 1000000000 1 1 100000"]
for y in range(1, 100001):
    parts.append(f"1 1 {y}")

assert run("\n".join(parts) + "\n") == "1000000001", "large k and coordinates"
```

The first custom case validates the minimum possible dimensions and the one-horizontal-move plus one-vertical-move boundary.

The second case confirms that the two corridors are independent when soldiers do not compete for the same corridor.

The third case checks that equal earliest exit times cannot be assigned to the same corridor simultaneously.

The fourth case puts soldiers directly next to both corridor boundaries and catches mistakes in the definitions of (c_1) and (c_2).

The final case uses (100000) soldiers and coordinates near (10^9). It validates both the asymptotic behavior and the use of arbitrary-size integer arithmetic.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1` with one left soldier | `2` | Minimum dimensions and off-by-one handling |
| `1 1 1 1 2` with one left and one right soldier | `2` | Independent corridor schedules |
| `1 1 1 1 3` with left, middle, and right soldiers | `3` | Duplicate exit times and corridor capacity |
| `1 2 1 2 2` with boundary-adjacent soldiers | `3` | Exact corridor-column formulas |
| `1000000000 1000000000 1 1 100000` with 100000 left soldiers | `1000000001` | Maximum (k), large coordinates, and integer arithmetic |

## Edge Cases

For the minimum cabin

```
1 1 1 1 1
1 1 1
```

the left corridor is column (2). The soldier starts at column (1), so (p_L=1+(2-1)=2). There is only one soldier, so no corridor collision is possible. The binary search finds that (T=1) is infeasible and (T=2) is feasible.

For duplicate earliest exit times,

```
1 1 1 1 3
1 1 1
2 1 3
3 1 5
```

all three soldiers have earliest exit time (2). At (T=2), the left soldier has only the left slot at reversed time (1), the middle soldier can use either corridor's slot, and the right soldier has only the right slot. Hall's condition for one prefix slot on each corridor sees all three soldiers but only two slots, so (T=2) fails. At (T=3), each corridor has enough distinct exit times and the answer becomes (3).

For a soldier close to the left corridor,

```
1 2 1 2 2
1 1 2
2 1 4
```

the left corridor is column (3), while the right corridor is column (6). The left soldier has (p_L=2), and the middle soldier at column (4) has (p_L=2) and (p_R=3). Both could individually leave through the left side at time (2), but they would need distinct corridor exit times if both used that corridor. Sending the middle soldier to the right gives exit times (2) and (3), so the answer is `3`. This catches the common mistake of treating the two corridor columns as if their positions were (l_1) and (l_1+l_2+1) rather than (l_1+1) and (l_1+l_2+2).

For a very large instance,

```
1000000000 1000000000 1 1 100000
```

with all (100000) soldiers in row (1) of the left zone, the earliest exit times form the consecutive range from (999900002) through (1000000001). Because consecutive earliest times already give distinct exit slots, the last soldier leaves at time (1000000001). The algorithm handles this without ever constructing the (10^9)-wide grid.
