---
title: "CF 102448D - Drinking to turn red"
description: "We have a fixed point ((x,y)) where the magic ring is placed. Every ordinary ring has a center ((Xi,Yi)) and radius (Ri). The magic ring starts with some radius (r), and whenever it absorbs an ordinary ring, its radius grows by that ring's radius."
date: "2026-08-08T12:07:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "D"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 589
verified: true
draft: false
---

[CF 102448D - Drinking to turn red](https://codeforces.com/problemset/problem/102448/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed point ((x,y)) where the magic ring is placed. Every ordinary ring has a center ((X_i,Y_i)) and radius (R_i). The magic ring starts with some radius (r), and whenever it absorbs an ordinary ring, its radius grows by that ring's radius.

Suppose the magic ring currently has radius (C). An ordinary ring (i) can be absorbed exactly when the two circles intersect or touch, which is equivalent to

[
\sqrt{(X_i-x)^2+(Y_i-y)^2} \le C+R_i.
]

After absorbing it, the current radius becomes (C+R_i). The task is to choose the smallest possible initial (r) that allows every ring to be absorbed in some order.

The key difficulty is that absorbing a ring changes the radius, so the rings cannot simply be treated independently. A ring that is initially unreachable may become reachable after absorbing several easier rings.

There are up to (10^5) rings, while the coordinates can have magnitude close to (10^9). This rules out anything quadratic in (N), because (10^{10}) operations are far beyond the two second limit. We need an (O(N\log N)) solution, or something comparably efficient. The coordinate bounds also mean squared distances can reach roughly (8\cdot10^{18}), so the distance calculation needs enough integer precision before taking the square root.

There are several edge cases that a careless implementation can mishandle. First, the required initial radius can actually be zero. For example,

```
1 0 0
0 0 2
```

has answer `0.0000000000`. The magic ring already intersects the ordinary ring even with zero radius, because the distance between their centers is zero. An implementation that initializes the answer to the first required radius without allowing zero can incorrectly print a positive value.

Tangency is another boundary case. Consider

```
1 0 0
3 0 2
```

The centers are exactly distance (3) apart and the radii sum to (3), so the rings touch and absorption is allowed. The answer is

```
1.0000000000
```

Using a strict `<` instead of `<=` would reject this valid absorption.

The order of absorption also matters. Consider

```
2 0 0
100 0 99
3 0 1
```

For the first ring, the required current radius is (100-99=1). For the second, it is (3-1=2). The first ring should be absorbed first. Starting with radius (1), the magic ring absorbs the radius-(99) ring and grows to radius (100), after which the second ring is easy. The correct answer is `1.0000000000`. Sorting by center distance instead would process the distance-(3) ring first and incorrectly conclude that radius (2) is needed.

## Approaches

A direct brute-force approach is to consider every possible absorption order. For a fixed order, the minimum required initial radius is easy to calculate. Before absorbing ring (i), we know the sum of the radii of all previously absorbed rings, so we can determine exactly how large the initial radius must have been for that step to be possible. Taking the maximum over the whole order gives the required starting radius for that order.

The problem is the number of orders. There are (N!) permutations, and evaluating one permutation takes (O(N)) time, giving (O(N\cdot N!)) work. Even (N=20) would already require roughly (20\cdot20!), about (4.9\cdot10^{19}), ring checks. With (N=10^5), exhaustive ordering is completely impossible.

The structure becomes much simpler if we rewrite the absorption condition. Let

[
d_i=\sqrt{(X_i-x)^2+(Y_i-y)^2}
]

be the distance from the magic ring's center to ring (i)'s center. Ring (i) is absorbable when

[
d_i\le C+R_i,
]

or equivalently,

[
d_i-R_i\le C.
]

Define

[
A_i=d_i-R_i.
]

Now each ring is simply an object that becomes available once the current magic radius reaches its threshold (A_i). Absorbing it adds (R_i) to the current radius.

All rewards (R_i) are positive. That changes the ordering problem completely. If two rings have thresholds (A_i\le A_j), and the ring with threshold (A_j) is currently available, then the ring with threshold (A_i) is also available. Absorbing the smaller-threshold ring first cannot hurt, because it only increases the current radius before the other ring is considered.

This means we can sort all rings by (A_i). Once sorted, there is no need to simulate complicated choices. Before the (i)-th ring in this order, the current radius has already gained the radii of all previous rings. If their total radius is (S), then we need

[
r+S\ge A_i,
]

so

[
r\ge A_i-S.
]

The minimum initial radius is consequently the maximum of these requirements, together with zero because a radius cannot be negative.

The brute-force works because a complete order lets us test every possible sequence. It fails because there are factorially many sequences. The observation that rings can be ordered by the amount of radius they need before becoming reachable reduces the entire problem to sorting and one prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N\cdot N!)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. For every ordinary ring, calculate its distance from the fixed magic-ring center:

[
d_i=\sqrt{(X_i-x)^2+(Y_i-y)^2}.
]

Then calculate its required current radius

[
A_i=d_i-R_i.
]

This value is the smallest magic-ring radius that would allow ring (i) to be absorbed immediately.

1. Store each ring as the pair ((A_i,R_i)), then sort all pairs by (A_i).

The sorted order is valid because a ring with a smaller threshold is never harder to absorb than a ring with a larger threshold. If a larger-threshold ring is available, every smaller-threshold ring is available too, and absorbing the smaller one only increases the radius.

1. Set `added = 0`, representing the total radius gained from rings already absorbed, and set `answer = 0`.

Before processing a ring, the magic ring's current radius is `answer + added` only conceptually. More directly, `answer` represents the initial radius we are trying to make sufficient, while `added` represents the radius gained after previous absorptions.

1. For each sorted pair ((A_i,R_i)), compute

[
A_i-added.
]

The initial radius must be at least this value, because the previous rings have already increased the magic ring's radius by `added`. Update the answer with the maximum of its current value and this requirement.

1. Add (R_i) to `added` and continue.

Every ring contributes its radius only after it has been successfully reached, which is exactly how the real absorption process behaves.

1. Print the resulting maximum with sufficient decimal precision.

The distance calculation uses integer differences before taking the square root, so the squared distance itself is computed exactly in Python.

### Why it works

The invariant is that after processing the first (i) rings in sorted threshold order, `added` is exactly the sum of their radii, and `answer` is the smallest initial radius that makes every processed absorption possible.

For the next ring, its threshold is (A_i). The previous rings have already increased the magic radius by `added`, so the next absorption is possible exactly when

[
answer+added\ge A_i.
]

Thus the algorithm must enforce (answer\ge A_i-added). Taking the maximum over all processed rings satisfies every such condition.

The remaining question is why sorted threshold order is sufficient. Suppose some feasible absorption order contains two consecutive rings with thresholds (A_j>A_i), where (j) is absorbed before (i). Since (j) was reachable, the current radius was at least (A_j), and therefore also at least (A_i). We can swap them, absorb (i) first, gain its positive radius, and still have enough radius to absorb (j). Repeatedly removing such inversions transforms any feasible order into nondecreasing threshold order without increasing the required initial radius. Hence the sorted order contains an optimal solution.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, x, y = map(int, input().split())

    rings = []

    for _ in range(n):
        X, Y, R = map(int, input().split())

        dx = X - x
        dy = Y - y

        distance = math.hypot(dx, dy)
        need = distance - R

        rings.append((need, R))

    rings.sort()

    answer = 0.0
    added = 0

    for need, radius in rings:
        answer = max(answer, need - added)
        added += radius

    print(f"{answer:.10f}")

if __name__ == "__main__":
    solve()
```

The input loop first converts every circle into the pair that matters to the greedy algorithm. The original center coordinates are no longer needed after computing the distance.

`math.hypot(dx, dy)` calculates (\sqrt{dx^2+dy^2}). The coordinate differences are integers, and Python integers have arbitrary precision, so there is no integer overflow when the squared distance is internally formed.

The subtraction `distance - R` is deliberately done before sorting. Sorting by `distance` alone is incorrect because a large ring can be easier to absorb than a smaller ring when its radius is large. The relevant quantity is always `distance - radius`.

The loop keeps `added` as an integer. This is useful because the sum of up to (10^5) radii is at most (10^{10}), which is exact in Python. Only the geometric threshold contains a square root and needs floating-point arithmetic.

The update happens before adding the current ring's radius. This ordering matches the physical process: the current ring cannot contribute its radius until after it has been absorbed. Adding first would introduce an off-by-one-step error and could make an initially unreachable ring appear reachable.

The comparison in the mathematical condition is non-strict. A tangent ring can be absorbed, so the threshold is satisfied when the current radius is exactly equal to `need`. The formula naturally handles equality without requiring a special case.

Finally, `answer` starts at zero because the required radius can be non-positive. If every ring already intersects a zero-radius magic ring after accounting for its own radius, no positive starting radius is necessary.

## Worked Examples

For Sample 1, the magic center is ((1,1)). The two ordinary rings are at ((1,7)) with radius (3), and ((5,1)) with radius (3).

Their distances and thresholds are:

| Ring | Distance | Radius | (A_i=d_i-R_i) | `added` before | Required initial radius |
| --- | --- | --- | --- | --- | --- |
| ((5,1)) | 4 | 3 | 1 | 0 | 1 |
| ((1,7)) | 6 | 3 | 3 | 3 | 0 |

The sorted order starts with the second input ring because its threshold is only (1). Starting with radius (1), the magic ring can absorb it and grows to radius (4). The other ring then requires only radius (3), so it is absorbed immediately.

The maximum required initial radius is (1), producing the sample output.

For Sample 2, the four thresholds are approximately:

| Ring | Distance | Radius | (A_i=d_i-R_i) | `added` before | Required initial radius |
| --- | --- | --- | --- | --- | --- |
| 3 | 160.015625 | 41 | 119.015625 | 0 | 119.015625 |
| 4 | 245.943083 | 78 | 167.943083 | 41 | 126.943083 |
| 1 | 836.244584 | 6 | 830.244584 | 119 | 711.244584 |
| 2 | 1025.353110 | 30 | 995.353110 | 125 | 870.353110 |

The third input ring is easiest to reach, so it is absorbed first and increases the magic radius by (41). The fourth ring then becomes reachable, adding another (78). After these two absorptions, the magic ring has gained (119) radius.

The first ring requires an initial contribution of only about (711.245) after accounting for those (119) units. The last ring is the real bottleneck. By the time it is considered, (125) radius has already been gained, but its threshold is about (995.353110), so the initial radius must be at least

[
995.353110-125=870.353110.
]

That gives the sample output `870.3531099090`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Computing all distances takes (O(N)), and sorting (N) thresholds takes (O(N\log N)). |
| Space | (O(N)) | The threshold and radius pair for every ring is stored before sorting. |

With (N\le10^5), sorting (10^5) elements is easily practical within the two second limit. The algorithm performs only one linear pass after sorting, and its memory usage is proportional to the number of rings, well within 256 MB.

## Test Cases

```python
import sys
import io
import math

def solve(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    input = sys.stdin.readline

    n, x, y = map(int, input().split())
    rings = []

    for _ in range(n):
        X, Y, R = map(int, input().split())

        dx = X - x
        dy = Y - y

        distance = math.hypot(dx, dy)
        need = distance - R

        rings.append((need, R))

    rings.sort()

    answer = 0.0
    added = 0

    for need, radius in rings:
        answer = max(answer, need - added)
        added += radius

    sys.stdin = old_stdin
    return f"{answer:.10f}"

def run(inp: str) -> str:
    return solve(inp)

# Provided sample 1
out = float(run("""\
2 1 1
1 7 3
5 1 3
"""))
assert abs(out - 1.0) < 1e-9, "sample 1"

# Provided sample 2
out = float(run("""\
4 211 -458
335 369 6
-771 -753 30
193 -617 41
-27 -396 78
"""))
assert abs(out - 870.3531099090) < 1e-6, "sample 2"

# Minimum-size input, zero initial radius
out = float(run("""\
1 0 0
0 0 2
"""))
assert abs(out - 0.0) < 1e-9, "zero-radius answer"

# Tangency must be accepted
out = float(run("""\
1 0 0
3 0 2
"""))
assert abs(out - 1.0) < 1e-9, "tangency"

# Sorting must use distance - radius, not distance
out = float(run("""\
2 0 0
100 0 99
3 0 1
"""))
assert abs(out - 1.0) < 1e-9, "threshold ordering"

# Boundary coordinates and a large distance
out = float(run("""\
1 -999999999 1000000000
1000000000 -999999999 2
"""))
assert abs(out - (1999999999 * math.sqrt(2) - 2)) < 1e-6, "coordinate boundary"

# Maximum-size input, all equal values
n = 100000
lines = [f"{n} 0 0"]
lines.extend(["0 0 2"] * n)
out = float(run("\n".join(lines) + "\n"))
assert abs(out - 0.0) < 1e-9, "maximum-size equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0 / 0 0 2` | `0.0000000000` | Minimum-size case and the possibility of zero initial radius |
| `1 0 0 / 3 0 2` | `1.0000000000` | Tangency and the non-strict absorption condition |
| `2 0 0 / 100 0 99 / 3 0 1` | `1.0000000000` | Sorting by `distance - radius` rather than distance |
| Boundary-coordinate case | approximately `2828427123.746...` | Large coordinate differences and numerical precision |
| 100000 identical rings at the center | `0.0000000000` | Maximum (N), repeated values, sorting and linear scan performance |

## Edge Cases

The zero-radius case is handled because the answer starts at `0.0` and every requirement is considered relative to that value. For

```
1 0 0
0 0 2
```

the distance is (0), so the threshold is (0-2=-2). The required initial radius is therefore (-2), but a physical radius cannot be negative, so the maximum with zero remains (0). The ring can be absorbed immediately, and the algorithm prints `0.0000000000`.

The tangency case uses equality directly. For

```
1 0 0
3 0 2
```

the threshold is (3-2=1). With initial radius exactly (1), the two circles have center distance (3) and combined radii (1+2=3), so they touch. The condition is satisfied exactly, and the answer is `1.0000000000`. No epsilon adjustment or strict comparison is needed.

The ordering edge case demonstrates why the threshold includes the ring's own radius. For

```
2 0 0
100 0 99
3 0 1
```

the thresholds are (1) and (2), respectively. The sorted order takes the radius-(99) ring first. Starting with radius (1), the magic ring reaches it exactly, absorbs it, and grows to radius (100). The second ring is then trivially reachable. The algorithm records requirements (1) and (2-99=-97), so the final answer remains (1). Sorting by center distance would reverse the order and produce the wrong answer.

Large coordinates do not cause integer overflow in Python. For example, the boundary case uses a center near ((-10^9,10^9)) and a ring near ((10^9,-10^9)). The coordinate differences are close to (2\cdot10^9), so the squared distance is around (8\cdot10^{18}). Python computes that integer exactly before `math.hypot` converts the geometry to floating point. The resulting floating-point error is far below the required (10^{-6}) tolerance for the final answer.

Finally, many rings can have exactly the same threshold. The sort keeps them adjacent, and their relative order does not matter because all have already become reachable at the same current radius. Since every radius is positive, absorbing any one of them can only make the remaining rings easier to reach. The maximum-size test with (10^5) identical rings exercises this case while also confirming that the (O(N\log N)) implementation scales to the input limit.

If you want, I can also turn this into a more compact Codeforces-style editorial suitable for publication directly after the problem statement.
