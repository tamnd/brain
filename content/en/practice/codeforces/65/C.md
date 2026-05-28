---
title: "CF 65C - Harry Potter and the Golden Snitch"
description: "The snitch moves along a fixed polyline in 3D space. It starts at the first vertex and travels segment by segment at constant speed vs. Harry starts at another point and can move in any direction at constant speed vp, where vp = vs."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry"]
categories: ["algorithms"]
codeforces_contest: 65
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 60"
rating: 2100
weight: 65
solve_time_s: 131
verified: true
draft: false
---

[CF 65C - Harry Potter and the Golden Snitch](https://codeforces.com/problemset/problem/65/C)

**Rating:** 2100  
**Tags:** binary search, geometry  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The snitch moves along a fixed polyline in 3D space. It starts at the first vertex and travels segment by segment at constant speed `vs`. Harry starts at another point and can move in any direction at constant speed `vp`, where `vp >= vs`.

We need the earliest time when Harry and the snitch can occupy exactly the same point. If that never happens before the snitch finishes traversing the polyline, we print `"NO"`.

The geometry is continuous. The snitch is not jumping between vertices, it moves smoothly along each segment. Harry is also free to move continuously in space. The challenge is to find the first reachable point on the snitch trajectory.

The path contains at most `10000` segments, which immediately rules out any extremely fine-grained simulation. A naive time-stepping approach with tiny increments would either miss the answer because of floating-point precision, or require billions of iterations to achieve enough accuracy.

Each coordinate is at most `10^4`, so distances are manageable numerically. Double precision floating point arithmetic is sufficient.

The tricky part is that the snitch trajectory is piecewise linear. The earliest catch point may occur strictly inside a segment, not at a vertex. A solution that only checks vertices is wrong.

Consider this example:

```
1
0 0 0
10 0 0
2 1
5 0 0
```

The snitch moves from `(0,0,0)` to `(10,0,0)` with speed `1`. Harry starts at `(5,0,0)` with speed `2`.

Harry catches the snitch at time `5/3`, at point `(5/3,0,0)`. Checking only endpoints would completely miss this.

Another easy mistake is assuming Harry can always catch the snitch because `vp >= vs`.

Example:

```
1
0 0 0
10 0 0
1 1
100 0 0
```

The snitch finishes at time `10`. Harry needs `90` seconds just to reach the endpoint. Catching is impossible while the snitch is moving, so the correct answer is `"NO"`.

There is also a precision pitfall near segment boundaries. Suppose the catch moment happens exactly when the snitch reaches a vertex. Binary searching independently inside segments without careful interval handling can accidentally skip the exact endpoint.

## Approaches

The brute-force idea is straightforward. Parameterize the snitch position by time, then binary search globally on time to find the first moment when Harry can reach the snitch position.

For a given time `t`, we can compute the snitch position along the polyline. Harry can reach that point if

$$\text{distance}(P, S(t)) \le vp \cdot t$$

where `P` is Harry's start position and `S(t)` is the snitch position at time `t`.

This condition is monotonic. Once Harry becomes capable of reaching the snitch, he remains capable for all later times because he can simply wait.

So a global binary search over time works.

The difficulty is evaluating `S(t)`. The snitch moves across up to `10000` segments. If we scan all segments for every binary-search iteration, the complexity becomes roughly:

$$O(n \cdot \log(\text{precision}))$$

which is already acceptable here, but we can simplify the reasoning further by exploiting the structure of each segment.

Inside a single segment, the snitch position changes linearly with time. The feasibility condition is also monotonic within that interval. That means we can process segments one by one and binary search only inside the first segment where catching becomes possible.

The key observation is this:

If Harry cannot catch the snitch by the time it reaches the end of a segment, then the earliest catch time must lie later.

For segment `i`, let:

- `t0` be the time when the snitch enters the segment
- `t1` be the time when it leaves the segment

If Harry cannot reach the segment endpoint by time `t1`, then nothing earlier in future segments matters yet.

Once we find the first segment where the endpoint is reachable in time, the earliest catch moment must lie somewhere inside that segment. Then a binary search on time inside `[t0, t1]` gives the exact answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force global binary search with segment scan | O(n log precision) | O(n) | Accepted |
| Segment-wise binary search | O(n + log precision) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all polyline vertices and precompute the length of every segment.

The snitch moves at constant speed, so the traversal time of a segment is simply:

$$\frac{\text{segment length}}{vs}$$
2. Maintain the current accumulated time `cur_t`.

This represents when the snitch reaches the current segment start.
3. Process segments in order.

Suppose the current segment goes from `A` to `B`.
4. Compute the segment traversal time.

If the segment length is `d`, then:

$$\Delta t = \frac{d}{vs}$$

The snitch reaches `B` at time:

$$t_1 = cur_t + \Delta t$$
5. Check whether Harry can reach endpoint `B` by time `t1`.

Harry needs:

$$\frac{\text{distance}(P, B)}{vp}$$

seconds to get there.

If this exceeds `t1`, then Harry cannot catch the snitch anywhere up to this endpoint, so continue to the next segment.
6. Once an endpoint becomes reachable in time, the earliest catch lies inside this segment.

At the segment start, catching was impossible. At the segment end, it is possible. The condition changes monotonically, so there is exactly one transition point.
7. Binary search on time inside the current segment interval.

Let the search range be `[cur_t, t1]`.
8. For a candidate time `mid`, compute the snitch position on the segment.

If the segment parameter is:

$$r = \frac{mid - cur_t}{\Delta t}$$

then the position is linear interpolation:

$$S(mid) = A + r(B - A)$$
9. Check feasibility.

Harry can catch the snitch at time `mid` if:

$$\text{distance}(P, S(mid)) \le vp \cdot mid$$

If feasible, move the binary search left. Otherwise move right.
10. After enough iterations, output the final time and position.

### Why it works

The critical property is monotonicity.

Define:

$$f(t) = \text{distance}(P, S(t)) - vp \cdot t$$

Harry can catch the snitch exactly when `f(t) <= 0`.

As time increases, Harry's reachable radius grows linearly. The snitch moves continuously at speed at most equal to Harry's speed. Once the snitch enters Harry's reachable region, it can never permanently escape from it.

That means feasibility changes only once, from impossible to possible. Binary search is valid.

Processing segments in order guarantees we locate the earliest segment containing a valid time, and the binary search inside that segment recovers the earliest feasible moment.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)

def solve():
    n = int(input())

    pts = [tuple(map(float, input().split())) for _ in range(n + 1)]

    vp, vs = map(float, input().split())
    P = tuple(map(float, input().split()))

    cur_t = 0.0

    for i in range(n):
        A = pts[i]
        B = pts[i + 1]

        seg_len = dist(A, B)
        seg_time = seg_len / vs

        end_t = cur_t + seg_time

        if dist(P, B) > vp * end_t + 1e-12:
            cur_t = end_t
            continue

        lo = cur_t
        hi = end_t

        for _ in range(100):
            mid = (lo + hi) / 2.0

            ratio = (mid - cur_t) / seg_time

            x = A[0] + (B[0] - A[0]) * ratio
            y = A[1] + (B[1] - A[1]) * ratio
            z = A[2] + (B[2] - A[2]) * ratio

            snitch = (x, y, z)

            if dist(P, snitch) <= vp * mid:
                hi = mid
            else:
                lo = mid

        t = hi
        ratio = (t - cur_t) / seg_time

        x = A[0] + (B[0] - A[0]) * ratio
        y = A[1] + (B[1] - A[1]) * ratio
        z = A[2] + (B[2] - A[2]) * ratio

        print("YES")
        print(f"{t:.10f}")
        print(f"{x:.10f} {y:.10f} {z:.10f}")
        return

    print("NO")

solve()
```

The first helper function computes Euclidean distance in 3D space. Everything in the problem is geometric, so this operation appears repeatedly.

The main loop processes one segment at a time. `cur_t` stores when the snitch arrives at the segment start. From the segment length and snitch speed we compute how long traversal takes.

The endpoint reachability check is the key pruning step. If Harry still cannot reach the segment endpoint by the moment the snitch gets there, then no earlier point in that segment can work either. That lets us skip the whole segment.

Once a feasible endpoint is found, the answer must lie inside that segment. The binary search uses time as the search variable. Converting time into a point on the segment requires linear interpolation with parameter `ratio`.

The binary search runs for `100` iterations. That is far more than enough for `1e-6` precision because each iteration halves the interval.

The small epsilon in:

```
dist(P, B) > vp * end_t + 1e-12
```

avoids floating-point instability when the values are extremely close.

A subtle detail is using `hi` as the final answer after binary search. `hi` always stores a feasible time, while `lo` stores an infeasible one.

## Worked Examples

### Sample 1

Input:

```
4
0 0 0
0 10 0
10 10 0
10 0 0
0 0 0
1 1
5 5 25
```

The snitch moves along a square in the plane `z = 0`, while Harry starts above the center.

| Segment | Start Time | End Time | Endpoint Reachable? |
| --- | --- | --- | --- |
| (0,0,0) → (0,10,0) | 0 | 10 | No |
| (0,10,0) → (10,10,0) | 10 | 20 | No |
| (10,10,0) → (10,0,0) | 20 | 30 | Yes |

The earliest feasible segment is the third one.

Binary search inside `[20, 30]` converges to:

| Iteration | Mid Time | Feasible? |
| --- | --- | --- |
| 1 | 25.0 | No |
| 2 | 27.5 | Yes |
| 3 | 26.25 | Yes |
| ... | ... | ... |
| Final | 25.5 | Yes |

The catch point becomes:

| x | y | z |
| --- | --- | --- |
| 10 | 4.5 | 0 |

This example demonstrates that the answer may occur strictly inside a segment rather than at a vertex.

### Custom Example

Input:

```
1
0 0 0
10 0 0
1 1
100 0 0
```

| Segment | Start Time | End Time | Endpoint Reachable? |
| --- | --- | --- | --- |
| (0,0,0) → (10,0,0) | 0 | 10 | No |

Harry needs `90` seconds just to reach `(10,0,0)`, but the snitch stops moving at time `10`.

No segment becomes feasible, so the algorithm outputs:

```
NO
```

This confirms that equal speeds do not guarantee success.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + log precision) | Each segment is processed once, and exactly one binary search is performed |
| Space | O(n) | Stores all polyline vertices |

With `n <= 10000`, this easily fits inside the limits. The binary search performs a constant number of iterations, so the runtime is dominated by the linear scan through the segments.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isclose

def run(inp: str) -> str:
    import math

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def dist(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    out = io.StringIO()
    sys.stdout = out

    n = int(input())

    pts = [tuple(map(float, input().split())) for _ in range(n + 1)]

    vp, vs = map(float, input().split())
    P = tuple(map(float, input().split()))

    cur_t = 0.0

    for i in range(n):
        A = pts[i]
        B = pts[i + 1]

        seg_len = dist(A, B)
        seg_time = seg_len / vs

        end_t = cur_t + seg_time

        if dist(P, B) > vp * end_t + 1e-12:
            cur_t = end_t
            continue

        lo = cur_t
        hi = end_t

        for _ in range(100):
            mid = (lo + hi) / 2.0

            ratio = (mid - cur_t) / seg_time

            x = A[0] + (B[0] - A[0]) * ratio
            y = A[1] + (B[1] - A[1]) * ratio
            z = A[2] + (B[2] - A[2]) * ratio

            if dist(P, (x, y, z)) <= vp * mid:
                hi = mid
            else:
                lo = mid

        t = hi
        ratio = (t - cur_t) / seg_time

        x = A[0] + (B[0] - A[0]) * ratio
        y = A[1] + (B[1] - A[1]) * ratio
        z = A[2] + (B[2] - A[2]) * ratio

        print("YES")
        print(f"{t:.10f}")
        print(f"{x:.10f} {y:.10f} {z:.10f}")
        return out.getvalue()

    print("NO")
    return out.getvalue()

# sample 1
res = run("""4
0 0 0
0 10 0
10 10 0
10 0 0
0 0 0
1 1
5 5 25
""")
assert res.startswith("YES")

# minimum size, immediate catch
res = run("""1
0 0 0
10 0 0
2 1
0 0 0
""")
assert res.startswith("YES")

# impossible case
assert run("""1
0 0 0
10 0 0
1 1
100 0 0
""").strip() == "NO"

# catch exactly at endpoint
res = run("""1
0 0 0
10 0 0
2 1
20 0 0
""")
assert res.startswith("YES")

# 3D diagonal movement
res = run("""1
0 0 0
10 10 10
3 1
5 5 20
""")
assert res.startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Immediate catch at start | YES | Correct handling of time `0` |
| Far away Harry | NO | Catching may be impossible |
| Catch at endpoint | YES | Segment boundary handling |
| 3D diagonal segment | YES | Correct 3D geometry |
| Sample 1 | YES | Interior catch point |

## Edge Cases

Consider the case where the catch happens exactly at a vertex.

Input:

```
1
0 0 0
10 0 0
2 1
20 0 0
```

The snitch reaches `(10,0,0)` at time `10`. Harry also needs exactly `10` seconds to reach that point.

The algorithm processes the segment and checks endpoint feasibility:

$$\text{distance} = 10,\quad vp \cdot t = 20$$

so the segment is feasible.

Binary search converges to the endpoint itself. Since feasibility is checked with `<=`, the exact equality case is accepted correctly.

Now consider an interior catch.

Input:

```
1
0 0 0
10 0 0
2 1
5 0 0
```

At time `0`, the snitch is too far left. At time `10`, Harry can certainly reach the endpoint.

The binary search progressively shrinks toward the first feasible time:

| Time | Snitch Position | Harry Reachable Radius | Feasible |
| --- | --- | --- | --- |
| 1 | 1 | 2 | No |
| 2 | 2 | 4 | Yes |

The exact transition occurs at:

$$t = \frac{5}{3}$$

This confirms that the algorithm correctly handles answers strictly inside segments.

Finally, consider a completely impossible case.

Input:

```
1
0 0 0
10 0 0
1 1
100 0 0
```

The segment endpoint is reached at time `10`, but Harry needs `90` seconds to get there.

The endpoint feasibility check fails, so the algorithm never enters binary search and prints `"NO"`.

This prevents false positives caused by assuming equal speeds imply eventual interception.
