---
title: "CF 167A - Wizards and Trolleybuses"
description: "Each trolleybus starts from the depot at a fixed departure time. It begins with speed 0, can accelerate at most a, and can never exceed its own speed limit v[i]. The destination is d meters away."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 167
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 114 (Div. 1)"
rating: 1600
weight: 167
solve_time_s: 100
verified: true
draft: false
---

[CF 167A - Wizards and Trolleybuses](https://codeforces.com/problemset/problem/167/A)

**Rating:** 1600  
**Tags:** implementation, math  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

Each trolleybus starts from the depot at a fixed departure time. It begins with speed `0`, can accelerate at most `a`, and can never exceed its own speed limit `v[i]`. The destination is `d` meters away. Braking is unrestricted, so a trolleybus can instantly reduce its speed whenever needed.

If trolleybus `i` catches trolleybus `i-1`, overtaking is impossible. From that moment onward, both move together and trolleybus `i` cannot arrive earlier than trolleybus `i-1`.

For every trolleybus, we must compute the earliest possible arrival time at the final station while respecting acceleration limits, speed limits, and the no-overtaking rule.

The constraints completely determine the intended complexity. There are up to `10^5` trolleybuses, so any solution that simulates motion continuously or compares every pair of trolleybuses is too slow. An `O(n^2)` solution would require roughly `10^10` operations in the worst case, which is far beyond the limit. We need a linear or near-linear approach.

The physics part also matters. A trolleybus does not always spend time cruising at maximum speed. Sometimes the distance is too short to ever reach `v[i]`. A careless implementation that assumes every trolleybus accelerates to `v[i]` first will produce incorrect times.

Consider this input:

```
1 10 5
0 100
```

The trolleybus only needs to travel `5` meters. Reaching speed `100` is impossible within that distance. The correct motion is pure acceleration:

```
distance = 1/2 * a * t^2
5 = 5 * t^2
t = 1
```

So the answer is:

```
1.0000000000
```

Another easy mistake is forgetting that later trolleybuses cannot arrive earlier than previous ones.

Example:

```
2 1 10
0 1
1 100
```

The first trolleybus needs:

```
10 seconds
```

The second trolleybus could physically arrive earlier if the track were empty, but overtaking is forbidden. The correct answers are:

```
10.0000000000
10.0000000000
```

A naive implementation that computes each trolley independently would incorrectly print something close to `5.47` for the second trolleybus.

A third subtle case happens when a trolleybus catches another one exactly at the destination. That still counts as arriving simultaneously.

Example:

```
2 1 1
0 1
1 100
```

The first trolleybus arrives at time `1.5`. The second trolleybus also reaches the station exactly at `1.5`. The correct output is:

```
1.5000000000
1.5000000000
```

Using strict inequalities in the comparison logic can fail on this boundary.

## Approaches

The brute-force idea is straightforward. For each trolleybus, compute its unrestricted earliest arrival time from the physics constraints. Then compare it against all previous trolleybuses to determine whether it would catch any of them before the destination.

This works because trolleybuses move in order and cannot overtake. If trolleybus `i` would arrive earlier than trolleybus `j`, then at some point it must catch up.

The problem is scale. Checking interactions between every pair requires `O(n^2)` comparisons. With `10^5` trolleybuses, that becomes hopelessly slow.

The key observation is that we do not actually need to simulate where the catch-up happens.

Suppose trolleybus `i` could independently arrive at time `T[i]`. If `T[i]` is smaller than the previous trolleybus's actual arrival time, then trolleybus `i` must eventually catch it before the destination. Since overtaking is impossible, trolleybus `i` is forced to arrive at exactly the same time.

That means the true arrival times are simply:

```
answer[i] = max(answer[i-1], independent_time[i])
```

Everything reduces to computing the earliest physically possible arrival time for a single trolleybus.

There are only two motion patterns.

If the trolleybus reaches its maximum speed before the destination, then:

1. It accelerates from `0` to `v`.
2. It continues at constant speed.

If the destination is too close, then it only accelerates the whole way.

The transition point comes from the acceleration distance formula:

```
v^2 = 2ad
```

If `v^2 <= 2ad`, the trolleybus reaches maximum speed before the destination.

Otherwise it never reaches `v`.

This gives a complete `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `a`, and `d`.
2. For each trolleybus, compute its fastest possible arrival time assuming the track is empty.
3. Determine whether the trolleybus can reach its speed limit before traveling distance `d`.

The distance needed to accelerate from `0` to `v` is:

$s = \frac{v^2}{2a}$

If this value is at most `d`, then the trolleybus reaches full speed.
4. If the trolleybus reaches full speed:

1. Compute acceleration time:

$t = \frac{v}{a}$
2. Compute acceleration distance:

$s = \frac{v^2}{2a}$
3. Travel the remaining distance at constant speed.
4. Add departure time `t[i]`.
5. Otherwise, the trolleybus accelerates for the entire trip.

Use:

$d = \frac{1}{2}at^2$

which gives:

$t = \sqrt{\frac{2d}{a}}$
6. Let this computed value be `independent`.
7. The actual arrival time cannot be earlier than the previous trolleybus's arrival time.

Set:

```
answer[i] = max(answer[i-1], independent)
```
8. Output all answers.

### Why it works

The invariant is simple: after processing trolleybus `i`, `answer[i]` equals the earliest physically achievable arrival time while respecting all no-overtaking constraints.

The independent motion computation is optimal because each trolleybus always accelerates as aggressively as allowed and never slows unless forced.

If `independent[i] >= answer[i-1]`, then trolleybus `i` never catches the previous trolleybus, so it can keep its optimal schedule.

If `independent[i] < answer[i-1]`, then trolleybus `i` would reach the destination earlier than trolleybus `i-1`. Since overtaking is impossible, a catch-up must occur before or exactly at the destination. From that moment onward they move together, forcing trolleybus `i` to arrive at `answer[i-1]`.

Thus taking the running maximum exactly models the physical restriction.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, a, d = map(int, input().split())

    ans = []

    for _ in range(n):
        t, v = map(int, input().split())

        accel_dist = v * v / (2.0 * a)

        if accel_dist >= d:
            travel_time = math.sqrt(2.0 * d / a)
        else:
            accel_time = v / a
            remaining = d - accel_dist
            travel_time = accel_time + remaining / v

        arrival = t + travel_time

        if ans:
            arrival = max(arrival, ans[-1])

        ans.append(arrival)

    print("\n".join(f"{x:.10f}" for x in ans))

solve()
```

The first part computes the unrestricted optimal travel time for one trolleybus.

The expression:

```
accel_dist = v * v / (2.0 * a)
```

represents the distance required to accelerate from `0` to `v`.

If this distance is larger than or equal to `d`, then the trolleybus never reaches maximum speed before the destination. The entire trip is accelerated motion, so we solve:

```
d = 1/2 * a * t^2
```

using the square root formula.

Otherwise, the trolleybus first accelerates to `v`, then moves at constant speed. The travel time becomes:

```
time_to_accelerate + time_at_constant_speed
```

The most important implementation detail is the final line:

```
arrival = max(arrival, ans[-1])
```

Without this, later trolleybuses could illegally overtake earlier ones in the output.

Another subtle point is using floating point arithmetic everywhere. The formulas involve square roots and division, so integer arithmetic would truncate values and destroy precision.

The condition:

```
if accel_dist >= d:
```

must include equality. If the trolleybus reaches maximum speed exactly at the destination, there is no cruising phase.

## Worked Examples

### Example 1

Input:

```
3 10 10000
0 10
5 11
1000 1
```

| Bus | Departure | Max Speed | Independent Arrival | Previous Answer | Final Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 10 | 1000.5 | none | 1000.5 |
| 2 | 5 | 11 | 914.595... | 1000.5 | 1000.5 |
| 3 | 1000 | 1 | 11000.05 | 1000.5 | 11000.05 |

The second trolleybus is physically faster, but it cannot overtake the first one. Its computed arrival time becomes clamped to `1000.5`.

The third trolleybus is much slower and never catches the others.

### Example 2

Input:

```
2 1 10
0 1
1 100
```

| Bus | Departure | Max Speed | Independent Arrival | Previous Answer | Final Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 10.5 | none | 10.5 |
| 2 | 1 | 100 | 5.4721... | 10.5 | 10.5 |

The second trolleybus could independently arrive much earlier, but that would require overtaking the first trolleybus. The running maximum rule prevents this.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each trolleybus is processed once |
| Space | O(n) | The answers are stored for output |

With `10^5` trolleybuses, a linear solution easily fits within the time limit. The memory usage is also small, since only the result array is stored.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    n, a, d = map(int, input().split())

    ans = []

    for _ in range(n):
        t, v = map(int, input().split())

        accel_dist = v * v / (2.0 * a)

        if accel_dist >= d:
            travel_time = math.sqrt(2.0 * d / a)
        else:
            accel_time = v / a
            remaining = d - accel_dist
            travel_time = accel_time + remaining / v

        arrival = t + travel_time

        if ans:
            arrival = max(arrival, ans[-1])

        ans.append(arrival)

    print("\n".join(f"{x:.10f}" for x in ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
out = run(
"""3 10 10000
0 10
5 11
1000 1
"""
).strip().splitlines()

assert abs(float(out[0]) - 1000.5) < 1e-6
assert abs(float(out[1]) - 1000.5) < 1e-6
assert abs(float(out[2]) - 11000.05) < 1e-6

# minimum size
out = run(
"""1 1 1
0 1
"""
).strip()

assert abs(float(out) - 1.5) < 1e-6

# cannot reach max speed
out = run(
"""1 10 5
0 100
"""
).strip()

assert abs(float(out) - 1.0) < 1e-6

# overtaking prevention
out = run(
"""2 1 10
0 1
1 100
"""
).strip().splitlines()

assert abs(float(out[0]) - 10.5) < 1e-6
assert abs(float(out[1]) - 10.5) < 1e-6

# catch exactly at destination
out = run(
"""2 1 1
0 1
1 100
"""
).strip().splitlines()

assert abs(float(out[0]) - 1.5) < 1e-6
assert abs(float(out[1]) - 1.5) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single trolleybus | Direct physics computation | Minimum constraints |
| Very high speed, short distance | Pure acceleration phase | Never reaching max speed |
| Fast trolley behind slow trolley | Equalized arrival times | No overtaking |
| Catch exactly at destination | Equal boundary handling | Correct comparison logic |

## Edge Cases

### A trolleybus never reaches maximum speed

Input:

```
1 10 5
0 100
```

The acceleration distance needed to reach speed `100` is:

```
100^2 / (2 * 10) = 500
```

but the destination is only `5` meters away.

The algorithm enters the square root branch:

```
t = sqrt(2 * 5 / 10) = 1
```

Output:

```
1.0000000000
```

A buggy implementation that always accelerates to `v` first would produce a wildly incorrect answer.

### A faster trolleybus starts later

Input:

```
2 1 10
0 1
1 100
```

The second trolleybus independently arrives around `5.47`, but the first trolleybus arrives at `10.5`.

The algorithm computes:

```
answer[1] = max(5.47, 10.5) = 10.5
```

This correctly models the catch-up event.

### Catching exactly at the destination

Input:

```
2 1 1
0 1
1 100
```

The first trolleybus arrives at `1.5`.

The second trolleybus independently also reaches the destination at `1.5`.

The algorithm keeps:

```
answer[1] = max(1.5, 1.5) = 1.5
```

Using a strict inequality instead of `max` logic could incorrectly separate the answers due to floating point comparisons.
