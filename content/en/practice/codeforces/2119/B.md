---
title: "CF 2119B - Line Segments"
description: "We are given two fixed points on a plane: a starting location and a destination. We also receive a sequence of movement lengths. At step i, we must move from our current position to any point whose Euclidean distance from the current position is exactly ai."
date: "2026-06-08T03:56:23+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2119
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1035 (Div. 2)"
rating: 1200
weight: 2119
solve_time_s: 71
verified: true
draft: false
---

[CF 2119B - Line Segments](https://codeforces.com/problemset/problem/2119/B)

**Rating:** 1200  
**Tags:** geometry, greedy, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two fixed points on a plane: a starting location and a destination. We also receive a sequence of movement lengths. At step `i`, we must move from our current position to any point whose Euclidean distance from the current position is exactly `a_i`. The direction is completely free, but the distance is fixed.

After performing all moves, we want to know whether it is possible to land exactly on the target point.

The key difficulty is that each move introduces continuous freedom in direction, so the set of reachable points after each step is a disk boundary, not a single point. After multiple steps, the reachable region becomes a growing geometric shape defined by all possible vector sums of fixed-length segments.

The constraints matter in a very specific way. The total number of operations across all test cases is up to 2 · 10^5, so any approach that simulates geometry explicitly or stores sets of points is impossible. Even maintaining a polygon or sampling directions would be far too slow.

The natural failure mode comes from thinking greedily about direction choices. For example, always trying to aim toward the target can fail because early choices may force later moves to overshoot or undershoot the final distance. Another failure is assuming only total sum matters, which ignores cancellation effects.

For instance, if we only compare the distance between start and end with the sum of all `a_i`, we might say:

- if distance ≤ sum, then yes

This is incorrect. Consider:

```
start = (0,0), end = (1,0)
a = [2, 2]
```

Total sum is 4, so naive logic says reachable, but in fact we cannot end at distance 1 because two segments of length 2 can only reach distances in [0,4] but with parity-like constraints on vector composition.

The correct solution depends not only on total length but also on how much cancellation between segments is possible.

## Approaches

The brute-force interpretation is to track the full set of all reachable positions after each move. After step `i`, every reachable point expands to a circle centered at each previous point with radius `a_i`. This quickly becomes a continuous region whose boundary is increasingly complex. In fact, the reachable region after `i` steps is a disk whose radius depends only on the total structure of segment lengths, but deriving this geometrically still requires understanding Minkowski sums. Explicit simulation is impossible.

The key observation is that the only invariant that matters is the possible range of final distances from the start. After each segment, we are effectively adding a vector of fixed length but arbitrary direction. This reduces the problem to tracking the minimum and maximum possible distance from the origin after all moves.

If we think in reverse, after all segments, the endpoint relative to the start is a sum of vectors with fixed magnitudes. The set of all such sums forms an annulus: all distances between a minimum value and a maximum value.

The maximum distance is trivial: we align all segments in the same direction, giving:

```
max_dist = sum(a_i)
```

The minimum distance depends on cancellation. If one segment is too large compared to the rest, it cannot be fully canceled. If we sort nothing and reason directly, the minimum achievable distance is:

```
min_dist = max(0, 2 * max(a_i) - sum(a_i))
```

This comes from the idea that all segments except the largest can try to oppose it. If the largest segment is larger than the sum of all others, the excess remains.

Once we know the reachable interval `[min_dist, max_dist]`, the problem reduces to checking whether the actual distance between start and end lies inside it.

Let:

```
D = distance between start and end
```

We answer "Yes" iff:

```
min_dist ≤ D ≤ max_dist
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Geometry | Exponential / Continuous | Large | Too slow |
| Interval of distances | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We now translate the reasoning into a concrete procedure.

1. Compute the squared Euclidean distance between the start and end points. We avoid square roots by comparing squared values later.
2. Compute the sum of all segment lengths. This represents the farthest possible distance reachable if every move is aligned in the same direction.
3. Identify the largest segment length. This determines whether other segments can fully cancel it or not.
4. Compute the minimum possible final distance using:

```
min_dist = max(0, 2 * max_a - sum_a)
```

This captures the leftover “unbalanced” length after optimal cancellation.
5. Compare the target distance with the interval `[min_dist, sum_a]`. If it lies inside, output "Yes", otherwise output "No".

The reason this works is that the reachable endpoints form a continuous range of distances. Any value between the minimum and maximum is achievable because we can continuously rotate segment directions to interpolate between extreme configurations. The geometry of vector sums guarantees no gaps inside this interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        px, py, qx, qy = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = sum(a)
        mx = max(a)
        
        dx = px - qx
        dy = py - qy
        dist_sq = dx * dx + dy * dy
        
        min_dist = max(0, 2 * mx - total)
        
        # compare squared distances to avoid sqrt
        if min_dist * min_dist <= dist_sq <= total * total:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived interval check. The only subtlety is using squared distances to avoid floating-point error. The minimum and maximum distances are computed in linear time.

The expression `2 * mx - total` is clamped at zero because cancellation can fully eliminate displacement when no single segment dominates. The final check is purely an interval membership test.

## Worked Examples

### Example 1

Input:

```
n = 2
start = (1,1), end = (5,1)
a = [3,3]
```

| Step | total | max_a | min_dist | D^2 |
| --- | --- | --- | --- | --- |
| init | 6 | 3 | 0 | 16 |

We compute:

- total = 6
- max_a = 3
- min_dist = max(0, 2*3 - 6) = 0
- D = 4

Check:

```
0 ≤ 4 ≤ 6 → Yes
```

This shows full cancellation is possible in principle, so any intermediate distance up to 6 is achievable.

### Example 2

Input:

```
n = 2
start = (100,100), end = (100,100)
a = [4,5]
```

| Step | total | max_a | min_dist | D^2 |
| --- | --- | --- | --- | --- |
| init | 9 | 5 | 1 | 0 |

We compute:

- total = 9
- max_a = 5
- min_dist = max(0, 10 - 9) = 1
- D = 0

Check:

```
1 ≤ 0 is false → No
```

Even though we return to the same point geometrically, the imbalance forces at least distance 1 displacement, making exact return impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | single pass to compute sum and maximum |
| Space | O(1) | only aggregates stored |

The total complexity over all test cases is linear in the input size, which fits comfortably within limits up to 2 · 10^5 operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    out = []
    def fake_print(*args):
        out.append(" ".join(map(str, args)))
    builtins.print = fake_print

    solve()
    return "\n".join(out)

# provided samples
assert run("""5
2
1 1 5 1
3 3
3
1 1 3 3
2 3 4
2
100 100 100 100
4 5
1
5 1 1 4
5
2
10000000 10000000 10000000 10000000
10000 10000
""") == """Yes
Yes
No
Yes
Yes"""

# all equal, return to origin possible
assert run("""1
2
0 0 0 0
3 3
""") == "Yes"

# dominant segment prevents cancellation
assert run("""1
1
0 0 10 0
1
""") == "No"

# exact boundary case
assert run("""1
1
0 0 1 0
1
""") == "Yes"

# large symmetric case
assert run("""1
3
0 0 0 0
5 5 5
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal zero distance | Yes | full cancellation possible |
| single small segment vs far target | No | impossibility under min constraint |
| exact reachability | Yes | boundary inclusion |
| symmetric large segments | Yes | interval correctness |

## Edge Cases

When all segment lengths are identical and the target is the same point, cancellation allows full return to origin. The algorithm computes `max_a = total / n`, giving `min_dist = 0`, so any zero-distance target is accepted.

When there is only one segment, the reachable set is exactly a circle of radius `a1`. The formula yields `min_dist = max_dist = a1`, so only points at exact distance `a1` are accepted, matching geometry precisely.

When one segment dominates all others, such as `[10,1,1]`, the minimum distance becomes positive. The algorithm captures this as `2 * 10 - 12 = 8`, meaning the final position cannot get closer than distance 8 from the start, reflecting the irreducible excess of the longest move.
