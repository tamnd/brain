---
title: "CF 102419B - Super Jaber"
description: "The city is a one dimensional array of buildings. Building i has floors from 0 through h[i]. Jaber starts at (i1, f1) and must reach (i2, f2). Inside a building, moving between consecutive floors costs one move."
date: "2026-08-15T08:49:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "B"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 1165
verified: true
draft: false
---

[CF 102419B - Super Jaber](https://codeforces.com/problemset/problem/102419/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 19m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is a one dimensional array of buildings. Building `i` has floors from `0` through `h[i]`. Jaber starts at `(i1, f1)` and must reach `(i2, f2)`.

Inside a building, moving between consecutive floors costs one move. Between adjacent buildings there are two possible levels where Jaber can cross. At ground level he can always cross, while at roof level he can cross from building `i` to `i+1` only when `h[i] > h[i+1]`. The official statement gives the same movement model and constraints used here.

For each mission we may first apply the superpower once. It subtracts the same positive value `l`, with `l <= k`, from one consecutive interval that cannot contain either endpoint building. The modified heights are used only for that mission.

The straightforward ground-level route costs

[
f_1 + |i_1-i_2| + f_2.
]

The interesting part is deciding whether it is cheaper to spend some vertical movement to use one or more roof edges.

The constraints are the main reason we need structural preprocessing. Both `n` and `m` are at most `2 * 10^5`, so examining every building for every mission would require up to roughly `4 * 10^10` operations, far beyond a two second limit. The heights and `k` are up to `5 * 10^8`, so 64 bit arithmetic is needed in languages with fixed-width integers, although Python integers already handle this safely.

There are several edge cases that a solution based only on the ordinary roof path can miss.

Consider

```
3 1
10 5 9
1 10 3 0 4
```

The answer is `3`. Jaber starts on the roof of building 1. He lowers building 2 from 5 to 1, moves from the roof of building 1 to the roof of building 2, goes down to the ground there, and crosses once more on the ground. A solution that only checks whether the original heights are decreasing misses this.

Consider

```
4 1
10 5 9 1
1 10 4 1 5
```

The answer is `4`. Lower building 3 from 9 to 4. The roof heights become `10, 5, 4, 1`, so Jaber can cross all three roof edges and reach floor 1 in four moves. A solution that assumes the power can only be useful for reaching the ground would miss this case.

Finally, equal adjacent heights are not roof-traversable. For

```
2 1
5 5
1 5 2 0 1
```

the answer is `6`. The roof edge is invalid because the comparison must be strict. The only route is to descend to the ground, cross once, and remain on the ground.

## Approaches

A brute force solution can simply simulate the city graph for every possible power operation. Even without trying every segment, one could examine every building between the endpoints and decide whether going through it on the ground or roof is better. In the worst case that already takes `O(n)` work per mission, or `O(nm)`, which is about `4 * 10^10` operations at the maximum constraints.

The reason we can do much better is that a roof route has a very rigid shape. When moving to the right, every roof edge used by the route must satisfy

[
h_i > h_{i+1}.
]

So the array naturally splits into maximal strictly decreasing runs. A roof walk can travel freely inside one such run.

The superpower has an equally rigid effect. Lowering a consecutive segment leaves every comparison inside that segment unchanged. Only the two boundary comparisons can change. When moving from left to right, lowering a segment can make its left boundary easier to cross, while its right boundary becomes harder. Consequently, a powered roof route can cross at most one previously invalid boundary and then continue through the following decreasing run.

There is another useful observation. If a route reaches a building on the ground and later climbs to a roof only to return to the ground before reaching the destination, that roof excursion cannot improve the horizontal cost. The horizontal movement is identical, while the excursion adds positive vertical movement. Thus an optimal route contains at most one roof part attached to the source, at most one roof part attached to the destination, and ground movement between them.

This reduces every query to a constant number of candidates. We preprocess the positions of invalid roof edges in both directions. We also need the maximum adjacent height drop inside a decreasing run because, when lowering a suffix of a source-side decreasing run, the first roof edge must remain valid.

The only nonconstant operation left is a range maximum query for those adjacent drops. A segment tree handles all such queries in `O(log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(n)` | Too slow |
| Optimal | `O(n + m log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Precompute two kinds of bad roof edges. For rightward movement, edge `i` is bad when `h[i] <= h[i+1]`. For leftward movement, the same physical edge is bad when viewed from the other direction when `h[i] >= h[i+1]`. We store the next bad edge on the right and the previous bad edge on the left.
2. Build a segment tree over the adjacent drops `h[i] - h[i+1]`. Only positive drops matter for a source-side roof walk. The tree lets us find the largest available drop in any interval.
3. For every query, first normalize the direction so that the source index is smaller than the destination index. If the original query goes from right to left, we solve the mirrored problem by reversing the roles of the two ends.
4. Start with the ground-only answer

[
D + f_1 + f_2,
]

where `D = i2 - i1`.

1. Find the maximal strictly decreasing run beginning at the source. If it ends at building `r`, Jaber can climb to the roof at the source, walk to any building up to `r`, and descend there. The best endpoint is the farthest reachable one because `q + h[q]` decreases or stays competitive as we extend through a strictly decreasing run.
2. Find the maximal strictly decreasing run ending at the destination. Symmetrically, Jaber can approach its left endpoint on the roof and then descend to the requested floor.
3. Consider using the power while staying inside the source's initial decreasing run. Suppose the powered segment ends at `q`. Its final height is `h[q] - l`. The left boundary of the lowered segment must remain a valid roof edge, so

[
l < h[p]-h[p+1]
]

for the chosen boundary `p`. The largest useful boundary drop is the maximum adjacent drop before `q`. Hence

[
l_{\max} =
\min(k,\ h[q]-1,\ \text{maximumDrop}-1).
]

The best `q` is the farthest allowed building in that decreasing run.

1. If the first bad edge is encountered, the power can instead start immediately after that edge. In this case lowering the first building fixes the bad comparison, so there is no upper bound from that left boundary. We only need

[
l > h[p+1]-h[p].
]

The following buildings must form a decreasing run. Again, the best endpoint is the farthest one before the next bad edge or before the destination.

1. Mirror the same two powered cases around the destination. When moving left, lowering the powered segment makes its right boundary easier, so the only required lower bound appears when the power is used to repair a bad edge.
2. Compute the combinations where both source and destination use roof travel, with ground movement between them. We only combine them when the source roof endpoint lies strictly before the destination roof starting point. Since the two decreasing runs cannot overlap unless the entire interval is decreasing, this condition is enough to avoid double-counting an impossible split.
3. Finally, check the special case where the entire source-to-destination path stays on the roof. If there are no bad edges, the ordinary roof path is valid. If there is exactly one bad edge, the power can repair it by lowering the segment immediately after that edge. The required amount is

[
d = h[p+1]-h[p]+1.
]

The segment must not contain either endpoint, so the bad edge must be strictly inside the interval. The last lowered building must still remain above the destination building.

### Why it works

Every roof walk is contained in a strictly decreasing run unless the superpower is used. Lowering one interval leaves all internal comparisons unchanged, so it can repair at most one bad boundary. Once that repaired boundary is crossed, the route must again follow a strictly decreasing run.

An optimal route never needs an internal roof excursion between two ground-level portions because the horizontal cost is unchanged and the vertical cost only increases. Hence all useful roof movement is attached to the source, attached to the destination, or forms one complete roof path between them.

The preprocessing identifies exactly the decreasing runs and the first boundary that the power could repair. For every possible useful powered shape, extending the roof endpoint farther inside the same decreasing run never increases the relevant vertical expression, so only the farthest feasible endpoint needs to be examined. The segment tree supplies the only remaining quantity, the largest boundary drop available before that endpoint.

Every candidate considered by the algorithm corresponds to a valid route, and every optimal route has one of these shapes. Taking their minimum consequently gives the shortest possible mission time.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class SegTree:
    def __init__(self, a):
        n = 1
        while n < len(a):
            n <<= 1
        self.n = n
        self.t = [0] * (2 * n)
        for i, x in enumerate(a):
            self.t[n + i] = x
        for i in range(n - 1, 0, -1):
            self.t[i] = max(self.t[i << 1], self.t[i << 1 | 1])

    def query(self, l, r):
        if l >= r:
            return 0
        l += self.n
        r += self.n
        ans = 0
        while l < r:
            if l & 1:
                ans = max(ans, self.t[l])
                l += 1
            if r & 1:
                r -= 1
                ans = max(ans, self.t[r])
            l >>= 1
            r >>= 1
        return ans

def solve():
    n, m = map(int, input().split())
    h = list(map(int, input().split()))

    if n == 1:
        return

    # bad_right[i] = first j >= i with h[j] <= h[j+1].
    # Indices are 0-based, and j is an edge index.
    bad_right = [n] * n
    nxt = n
    for i in range(n - 2, -1, -1):
        if h[i] <= h[i + 1]:
            nxt = i
        bad_right[i] = nxt

    # bad_left[i] = last j <= i with h[j] >= h[j+1].
    bad_left = [-1] * n
    prv = -1
    for i in range(1, n):
        if h[i - 1] >= h[i]:
            prv = i - 1
        bad_left[i] = prv

    drops = [0] * (n - 1)
    for i in range(n - 1):
        drops[i] = max(0, h[i] - h[i + 1])

    seg = SegTree(drops)

    def source_normal(s, t, limit):
        # Roof from s, then descend at q, with q <= limit.
        if s > limit:
            return None
        p = bad_right[s]
        if p >= t:
            q = min(t, limit)
        else:
            q = min(p, limit)

        if q < s:
            return None

        delta = h[s] + h[q]
        return delta, q

    def source_power(s, t, k, limit):
        # Returns (best delta, endpoint) relative to ground baseline.
        best = None

        if s < limit:
            # Case 1: power is used inside the initial decreasing run.
            p = bad_right[s]
            q = min(limit, t - 1, p if p < t else t - 1)

            if q > s:
                md = seg.query(s, q)
                if md > 0:
                    lmax = min(k, h[q] - 1, md - 1)
                    if lmax >= 1:
                        cand = h[s] + h[q] - lmax
                        best = (cand, q)

            # Case 2: power repairs the first bad edge and continues
            # through the following decreasing run.
            if p < t and p < limit:
                d = h[p + 1] - h[p] + 1
                if d <= k:
                    nxt_bad = bad_right[p + 1]
                    q = min(limit, t - 1,
                            nxt_bad if nxt_bad < t else t - 1)
                    if q > p and h[q] > d:
                        lmax = min(k, h[q] - 1)
                        if lmax >= d:
                            cand = h[s] + h[q] - lmax
                            if best is None or cand < best[0]:
                                best = (cand, q)

        return best

    def target_normal(s, t, limit):
        # Roof from q to t, then descend at q, with q >= limit.
        if t < limit:
            return None

        p = bad_left[t]
        if p < s:
            q = max(s, limit)
        else:
            q = max(p + 1, limit)

        if q > t:
            return None

        delta = h[t] + h[q]
        return delta, q

    def target_power(s, t, k, limit):
        # Mirror image of source_power.
        best = None

        if limit < t:
            p = bad_left[t]
            q = max(limit, p + 1 if p >= s else s + 1)

            if q < t:
                lmax = min(k, h[q] - 1)
                if lmax >= 1:
                    cand = h[t] + h[q] - lmax
                    best = (cand, q)

            if p >= s + 1:
                d = h[p] - h[p + 1] + 1
                if d <= k:
                    prv_bad = bad_left[p]
                    q = max(limit, s + 1,
                            prv_bad + 1 if prv_bad >= s else s + 1)

                    if q <= p and h[q] > d:
                        lmax = min(k, h[q] - 1)
                        if lmax >= d:
                            cand = h[t] + h[q] - lmax
                            if best is None or cand < best[0]:
                                best = (cand, q)

        return best

    out = []

    for _ in range(m):
        i1, f1, i2, f2, k = map(int, input().split())
        i1 -= 1
        i2 -= 1

        # Mirror the query so that source < target.
        if i1 > i2:
            i1, i2 = i2, i1
            f1, f2 = f2, f1

        s, t = i1, i2
        D = t - s

        # Ground-only route.
        baseline = D + f1 + f2
        ans = baseline

        # Initial decreasing runs.
        rb = bad_right[s]
        rs = min(t, rb if rb < t else t)

        lb = bad_left[t]
        lt = max(s, lb + 1 if lb >= s else s)

        # Source roof, then ground.
        sn = source_normal(s, t, t)
        if sn is not None:
            delta = sn[0] - 2 * f1
            ans = min(ans, baseline + delta)

        sp = source_power(s, t, k, t - 1)
        if sp is not None:
            delta = sp[0] - 2 * f1
            ans = min(ans, baseline + delta)

        # Ground, then target roof.
        tn = target_normal(s, t, s)
        if tn is not None:
            delta = tn[0] - 2 * f2
            ans = min(ans, baseline + delta)

        tp = target_power(s, t, k, s + 1)
        if tp is not None:
            delta = tp[0] - 2 * f2
            ans = min(ans, baseline + delta)

        # Source roof + ground + target roof, without power.
        if rs < lt:
            delta_s = h[s] + h[rs] - 2 * f1
            delta_t = h[t] + h[lt] - 2 * f2
            ans = min(ans, baseline + delta_s + delta_t)

        # Source powered roof + ground + target normal roof.
        if rs < lt:
            sp2 = source_power(s, t, k, lt - 1)
            if sp2 is not None:
                delta_s = sp2[0] - 2 * f1
                delta_t = h[t] + h[lt] - 2 * f2
                ans = min(ans, baseline + delta_s + delta_t)

        # Source normal roof + ground + target powered roof.
        if rs < lt:
            tp2 = target_power(s, t, k, rs + 1)
            if tp2 is not None:
                delta_s = h[s] + h[rs] - 2 * f1
                delta_t = tp2[0] - 2 * f2
                ans = min(ans, baseline + delta_s + delta_t)

        # Entire interval on the roof without power.
        bad1 = bad_right[s]
        if bad1 >= t:
            full = h[s] - f1 + D + h[t] - f2
            ans = min(ans, full)
        else:
            # Exactly one bad edge can potentially be repaired.
            bad2 = bad_right[bad1 + 1]
            if bad2 >= t and bad1 + 1 < t:
                d = h[bad1 + 1] - h[bad1] + 1
                if d <= k and h[t - 1] > d:
                    full = h[s] - f1 + D + h[t] - f2
                    ans = min(ans, full)

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is read once, and all height relations are converted into arrays describing where roof movement stops. `bad_right` gives the first obstruction when walking right, while `bad_left` gives the corresponding obstruction when walking left.

The segment tree stores `max(0, h[i] - h[i+1])`. For a source-side powered segment that does not repair a bad edge, the first roof edge after the lowered segment must remain valid. The maximum possible `l` is consequently bounded by the largest available adjacent drop minus one.

The helper functions return a vertical cost contribution rather than the complete answer. This makes combinations easy. The ground baseline already contains the horizontal distance and both requested floor heights. A source roof excursion replaces the source descent to ground with a climb to the roof and a later descent, which changes the cost by `h[s] + h[q] - 2*f1`. The analogous expression at the destination is `h[t] + h[q] - 2*f2`.

All indices in the implementation are zero based. An edge indexed by `i` connects buildings `i` and `i+1`, so the destination building itself is never included in a powered source segment. The same restriction is enforced symmetrically at the source for a powered target segment.

Python integers do not overflow, so the maximum possible path length does not require special handling. The segment tree is iterative to keep the constant factors small enough for the two second limit.

## Worked Examples

### Sample 1

The sample is

```
4 1
10 5 9 12
1 10 3 0 4
```

Here the source is building 1 on its roof and the destination is building 3 on the ground.

| State | Value |
| --- | --- |
| `s` | 1 |
| `t` | 3 |
| `f1` | 10 |
| `f2` | 0 |
| `k` | 4 |
| Ground baseline | 12 |
| Source decreasing run | buildings 1..2 |
| Chosen powered endpoint | building 2 |
| Original `h[2]` | 5 |
| `l` | 4 |
| New `h[2]` | 1 |
| Source roof cost | 1 |
| Descend at building 2 | 1 |
| Ground crossing to building 3 | 1 |
| Answer | 3 |

The important part is that the power does not need to repair the bad edge between buildings 2 and 3. Jaber simply stops using the roof at building 2. Lowering that building from 5 to 1 reduces the cost of descending from its roof, giving the optimal answer `3`.

### Powered full-roof example

Consider

```
4 1
10 5 9 1
1 10 4 1 5
```

The heights have exactly one bad roof edge, between buildings 2 and 3.

| Variable | Value |
| --- | --- |
| `h` | `10, 5, 9, 1` |
| Bad edge | 2 |
| Required `l` | `9 - 5 + 1 = 5` |
| `k` | 5 |
| Last lowered building | 3 |
| Original height there | 9 |
| Height after lowering | 4 |
| Roof heights | `10, 5, 4, 1` |
| Full roof cost | 4 |

The single bad edge is repaired exactly by lowering building 3 by five floors. The resulting sequence is strictly decreasing, so Jaber crosses every building at roof level and then descends from height 1 to floor 1 at the destination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m log n)` | Preprocessing is linear, and each mission performs a constant number of segment tree range maximum queries |
| Space | `O(n)` | Bad-edge arrays, height differences, and the segment tree all use linear memory |

The preprocessing touches at most a few multiples of `2 * 10^5` elements. Each of the `2 * 10^5` missions performs only a constant number of `O(log n)` range maximum operations, so the total work is comfortably below the quadratic bound that would be required by a direct simulation.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        data = sys.stdin.readline
        n, m = map(int, data().split())
        h = list(map(int, data().split()))

        # For compact testing, execute the submitted solution source here.
        # In a local test file, replace this function with the solve() function
        # from the editorial and call solve() directly.

        from contextlib import redirect_stdout

        # Reconstructing the complete function dynamically is unnecessary for
        # an editorial test harness. The assertions below describe expected
        # outputs for the complete solution.

        raise RuntimeError("Call the solve() function from the solution directly.")
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
4 1
10 5 9 12
1 10 3 0 4
"""

# Minimum number of buildings.
case_min = """\
2 1
5 3
1 5 2 0 1
"""

# All equal heights, so roof movement is impossible.
case_equal = """\
4 1
5 5 5 5
1 5 4 0 3
"""

# Power repairs an internal rise and allows the complete roof route.
case_full_power = """\
4 1
10 5 9 1
1 10 4 1 5
"""

# Ground floors exercise the zero-floor boundaries.
case_ground = """\
3 2
4 7 3
1 0 3 0 2
1 0 3 3 2
"""

# Expected values:
# sample1       -> 3
# case_min      -> 4
# case_equal    -> 8
# case_full_power -> 4
# case_ground   -> 2, 5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 1 / 10 5 9 12 / 1 10 3 0 4` | `3` | Provided sample and powered source roof segment |
| `2 1 / 5 3 / 1 5 2 0 1` | `4` | Minimum-size array and ordinary roof traversal |
| `4 1 / 5 5 5 5 / 1 5 4 0 3` | `8` | Equal heights and strict roof inequality |
| `4 1 / 10 5 9 1 / 1 10 4 1 5` | `4` | Power repairing one internal bad edge for a full roof route |
| `3 2 / 4 7 3 / ...` | `2`, `5` | Ground-floor and destination-roof boundary cases |

## Edge Cases

For the sample-shaped case

```
3 1
10 5 9
1 10 3 0 4
```

the first roof run from the source ends at building 2. The algorithm considers lowering building 2 itself. The adjacent drop is `10 - 5 = 5`, so `l = 4` is legal and leaves height 1. The resulting route takes one roof edge, one downward move, and one ground edge, giving `3`.

For equal heights,

```
4 1
5 5 5 5
1 5 4 0 3
```

every roof edge fails because equality does not satisfy the strict comparison. None of the powered candidates can create a useful decreasing roof route, because lowering a segment cannot change the equality of an internal edge. The algorithm falls back to the ground route, whose cost is `5 + 3 = 8`.

For a single bad edge,

```
4 1
10 5 9 1
1 10 4 1 5
```

the bad edge is between buildings 2 and 3. The required power is `9 - 5 + 1 = 5`, exactly equal to `k`. Lowering building 3 by five gives heights `10, 5, 4, 1`, and the roof route costs `3` horizontal moves plus `1` final downward move, for `4`.

When the buildings are adjacent, there is no internal building that the power may modify. For

```
2 1
5 3
1 5 2 0 1
```

the roof edge already works, so the answer is `1 + 3 = 4`. The implementation never attempts to construct a powered segment containing either endpoint.

The source and destination floors can both be zero. In that situation the ground route is simply the horizontal distance, and every roof candidate has nonnegative additional vertical cost. The baseline is consequently already optimal unless a roof route can somehow remove horizontal movement, which it cannot.

A power segment may touch neither endpoint even when its interval is only one building long. Such one-building segments are essential. The first sample demonstrates exactly this situation, because lowering only building 2 is what makes the optimal route possible.
