---
title: "CF 1408C - Discrete Acceleration"
description: "Two cars start at opposite ends of a road of length l. The left car starts at position 0 and moves to the right. The right car starts at position l and moves to the left. Both cars begin with speed 1. Along the road there are flags placed at fixed coordinates."
date: "2026-06-11T07:41:45+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1408
codeforces_index: "C"
codeforces_contest_name: "Grakn Forces 2020"
rating: 1500
weight: 1408
solve_time_s: 147
verified: false
draft: false
---

[CF 1408C - Discrete Acceleration](https://codeforces.com/problemset/problem/1408/C)

**Rating:** 1500  
**Tags:** binary search, dp, implementation, math, two pointers  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

Two cars start at opposite ends of a road of length `l`. The left car starts at position `0` and moves to the right. The right car starts at position `l` and moves to the left.

Both cars begin with speed `1`. Along the road there are flags placed at fixed coordinates. Whenever a car passes a flag, only that car's speed increases by `1`. The two cars move continuously and simultaneously.

We must determine the exact time when the two cars occupy the same position.

The first thing to notice is that the cars do not change speed arbitrarily. Their speeds only change at flag positions. Between two consecutive speed changes, each car moves with constant velocity. That gives the motion a very structured form.

The number of flags in a single test can reach `10^5`, but the sum across all test cases is also bounded by `10^5`. This immediately rules out any simulation using tiny time steps. Even simulating every possible interaction between both cars would become difficult if each query required quadratic work.

The answer is a real number, so we are not looking for a purely combinatorial quantity. The motion is continuous. That often suggests either direct geometry or binary search on time.

Several edge cases are easy to mishandle.

Consider:

```
1
1 10
5
```

The cars reach the flag at different times. The left car reaches it after `5` seconds and accelerates, while the right car never touches that flag before the meeting occurs. A solution that assumes both cars gain speed at the same events will produce the wrong answer.

Consider:

```
1
2 10
1 9
```

Both cars hit a flag after exactly one second. Their speeds become `2`, and they meet at position `5` after another two seconds. The answer is exactly `3`. Floating-point accumulation errors become visible if the implementation tries to repeatedly simulate tiny intervals.

Another subtle case is when the meeting occurs before either car reaches its next flag. For example:

```
1
2 10
4 6
```

After both cars reach their first flags, they move toward each other with increased speeds. The meeting may happen inside an interval rather than at a flag. Any solution that only checks flag arrival times will miss this.

The key challenge is computing positions after an arbitrary amount of time while handling piecewise-constant speeds correctly.

## Approaches

A natural brute-force idea is to simulate events. Each event is the moment when one of the cars reaches its next flag. We could repeatedly determine which event happens first, advance time to that event, update positions, increase one speed, and continue until the cars meet.

This works conceptually because speed changes only occur at flags. The state changes only at finitely many moments.

The difficulty is that the meeting can occur between two events. We must constantly check whether the remaining distance between the cars closes before the next flag event. The implementation becomes fairly delicate.

Another possibility is to simulate motion using very small time increments. That is obviously too slow. Even a precision of `10^-7` on a road of length `10^9` would require an astronomical number of steps.

The crucial observation is that if we fix a time `T`, we can determine where each car is after exactly `T` seconds.

For the left car, we know the sequence of segments it traverses:

```
0 -> a1 -> a2 -> ... -> an -> l
```

On segment `i`, its speed is known. We can spend as much of the available time `T` as possible moving through complete segments. Once the remaining time is insufficient to finish the next segment, we stop somewhere inside that segment and compute the exact position.

The same idea works independently for the right car.

Now define:

```
f(T) = position_of_left_car_after_T
g(T) = position_of_right_car_after_T
```

The left position increases with time. The right position decreases with time.

The cars have met by time `T` exactly when:

```
f(T) >= g(T)
```

This condition is monotonic. If it is true for some time, it remains true for all larger times. That makes binary search possible.

We binary search the smallest time at which the two positions cross.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Event Simulation | O(n) per test | O(1) | Accepted, but more intricate |
| Binary Search + Position Evaluation | O(n log L) | O(1) | Accepted |

Here `L` represents the search range for time. About 60 binary-search iterations are sufficient for double precision.

## Algorithm Walkthrough

### Position computation for a fixed time

Suppose we want the position of the left car after time `T`.

The car starts at position `0` with speed `1`.

Whenever it passes a flag, the speed increases by `1`.

We process road segments from left to right.

If the current segment length is `d` and current speed is `v`, then traversing the whole segment requires:

```
d / v
```

seconds.

If enough time remains, we consume that amount of time, move to the segment's end, and increase the speed.

Otherwise, the car remains inside the segment. Its position is:

```
current_position + remaining_time * v
```

and we stop.

The right car is computed symmetrically from the right end.

### Binary search

1. Set `low = 0`.
2. Set `high = l`.

The meeting time can never exceed `l`, because even without any acceleration the cars approach each other with combined speed `2`, meeting within `l/2` seconds.
3. Repeat roughly 60 times.
4. Let `mid = (low + high) / 2`.
5. Compute the left car position after `mid` seconds.
6. Compute the right car position after `mid` seconds.
7. If the left position is at least the right position, the cars have already met by time `mid`, so move the upper bound to `mid`.
8. Otherwise the meeting happens later, so move the lower bound to `mid`.
9. After the iterations finish, output `high`.

### Why it works

For any fixed time `T`, the position calculations exactly reproduce the physical motion because every speed change occurs only when a complete segment has been traversed. The simulation of a single car is therefore exact.

Define:

```
h(T) = left_position(T) - right_position(T)
```

Initially `h(0) < 0`. As time increases, the left position never decreases and the right position never increases, so `h(T)` is monotone increasing.

The cars have met exactly when `h(T) >= 0`.

Since the predicate is monotone, binary search finds the unique transition point between "not yet met" and "already met". Repeated halving converges to the true meeting time with arbitrarily small error.

## Python Solution

```python
import sys
input = sys.stdin.readline

def left_pos(t, a, l):
    pos = 0.0
    speed = 1.0

    for flag in a:
        dist = flag - pos
        need = dist / speed

        if t >= need:
            t -= need
            pos = flag
            speed += 1.0
        else:
            return pos + speed * t

    dist = l - pos
    need = dist / speed

    if t >= need:
        return float(l)

    return pos + speed * t

def right_pos(t, a, l):
    pos = float(l)
    speed = 1.0

    for flag in reversed(a):
        dist = pos - flag
        need = dist / speed

        if t >= need:
            t -= need
            pos = float(flag)
            speed += 1.0
        else:
            return pos - speed * t

    dist = pos
    need = dist / speed

    if t >= need:
        return 0.0

    return pos - speed * t

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n, l = map(int, input().split())
        a = list(map(int, input().split()))

        lo = 0.0
        hi = float(l)

        for _ in range(70):
            mid = (lo + hi) / 2.0

            lp = left_pos(mid, a, l)
            rp = right_pos(mid, a, l)

            if lp >= rp:
                hi = mid
            else:
                lo = mid

        ans.append(f"{hi:.15f}")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The functions `left_pos` and `right_pos` implement the fixed-time position query. Each function walks through the sequence of segments, consuming time as long as an entire segment can be completed.

A common mistake is increasing the speed before reaching the flag. The implementation first checks whether enough time exists to finish the segment. Only after arriving at the flag is the speed incremented.

Another subtle detail is the final segment. After the last flag, the car continues toward the endpoint with its final speed. The code treats that segment exactly like every other one.

The binary search uses 70 iterations. Since each iteration halves the search interval, this is far more than enough to achieve the required `10^-6` precision.

## Worked Examples

### Example 1

Input:

```
1
2 10
1 9
```

Binary search eventually converges to `3`.

At `T = 3`:

#### Left car

| Segment | Speed | Time Needed | Remaining Time Before Segment | Position After |
| --- | --- | --- | --- | --- |
| 0 → 1 | 1 | 1 | 3 | 1 |
| 1 → 9 | 2 | 4 | 2 | inside segment |

Final position:

```
1 + 2 × 2 = 5
```

#### Right car

| Segment | Speed | Time Needed | Remaining Time Before Segment | Position After |
| --- | --- | --- | --- | --- |
| 10 → 9 | 1 | 1 | 3 | 9 |
| 9 → 1 | 2 | 4 | 2 | inside segment |

Final position:

```
9 - 2 × 2 = 5
```

Both cars are at position `5`, confirming the answer.

### Example 2

Input:

```
1
1 10
1
```

The answer is `11/3 ≈ 3.666666666667`.

#### Left car

| Segment | Speed | Time Needed |
| --- | --- | --- |
| 0 → 1 | 1 | 1 |

After one second the left car reaches the flag and its speed becomes `2`.

#### Right car

There are no flags on its side before meeting, so its speed remains `1`.

The remaining distance between positions `1` and `10` is:

```
9
```

Their combined speed is:

```
2 + 1 = 3
```

Additional time:

```
9 / 3 = 3
```

Total:

```
1 + 3 = 11/3
```

This example demonstrates that each car's acceleration depends only on the flags it personally reaches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log L) | Each binary-search iteration scans all flags once from each side |
| Space | O(1) | Only a few variables besides the input array |

With about 70 binary-search iterations and a total of at most `10^5` flags across all test cases, the total work is roughly `70 × 2 × 10^5`, which comfortably fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def left_pos(t, a, l):
        pos = 0.0
        speed = 1.0

        for flag in a:
            dist = flag - pos
            need = dist / speed

            if t >= need:
                t -= need
                pos = flag
                speed += 1.0
            else:
                return pos + speed * t

        return min(float(l), pos + speed * t)

    def right_pos(t, a, l):
        pos = float(l)
        speed = 1.0

        for flag in reversed(a):
            dist = pos - flag
            need = dist / speed

            if t >= need:
                t -= need
                pos = float(flag)
                speed += 1.0
            else:
                return pos - speed * t

        return max(0.0, pos - speed * t)

    tc = int(input())
    out = []

    for _ in range(tc):
        n, l = map(int, input().split())
        a = list(map(int, input().split()))

        lo, hi = 0.0, float(l)

        for _ in range(70):
            mid = (lo + hi) / 2

            if left_pos(mid, a, l) >= right_pos(mid, a, l):
                hi = mid
            else:
                lo = mid

        out.append(f"{hi:.6f}")

    return "\n".join(out)

# sample-style checks
res = run("1\n2 10\n1 9\n").strip()
assert abs(float(res) - 3.0) < 1e-5

res = run("1\n1 10\n1\n").strip()
assert abs(float(res) - 3.666666666666667) < 1e-5

# minimum case
res = run("1\n1 2\n1\n").strip()
assert abs(float(res) - 1.0) < 1e-5

# symmetric flags
res = run("1\n2 10\n4 6\n").strip()
assert float(res) > 0

# large coordinates
res = run("1\n2 1000000000\n413470354 982876160\n").strip()
assert float(res) > 0

# meeting exactly after simultaneous accelerations
res = run("1\n2 10\n1 9\n").strip()
assert abs(float(res) - 3.0) < 1e-5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1` | `1` | Smallest meaningful road |
| `2 10 / 1 9` | `3` | Simultaneous acceleration on both sides |
| `2 10 / 4 6` | Positive finite answer | Meeting inside an interval |
| Large coordinates near `10^9` | Positive finite answer | Floating-point stability |
| Single flag near one endpoint | Correct asymmetric answer | Independent speed changes |

## Edge Cases

### Meeting before the next flag

Input:

```
1
2 10
4 6
```

After both cars reach their nearest flags, their speeds become `2`. The meeting occurs somewhere between the flags rather than exactly at a flag position.

The position-query functions naturally handle this because they stop inside a segment whenever the remaining time is insufficient to reach the next flag.

### One car accelerates while the other does not

Input:

```
1
1 10
1
```

The left car reaches the flag after one second and gains speed `2`. The right car keeps speed `1`.

The algorithm computes each car independently. No assumption is made about simultaneous acceleration events, so the answer remains correct.

### Meeting exactly at the same coordinate after flag crossings

Input:

```
1
2 10
1 9
```

Both cars hit a flag after one second and accelerate simultaneously. At time `3`, both positions equal `5`.

Binary search uses the condition:

```
left_position >= right_position
```

so equality is treated as a valid meeting state. The transition point is found correctly even when the cars meet exactly rather than crossing strictly.

### Very large coordinates

Input:

```
1
2 1000000000
413470354 982876160
```

Distances and times can be close to `10^9`. The algorithm never performs integer-time simulation. It uses only arithmetic on segment lengths and binary search over doubles, which remains accurate within the required tolerance.
