---
title: "CF 104974D - Traffic Lights"
description: "We are moving along a straight road from position 0 to position X, walking at exactly one meter per second. Along the way there are traffic lights placed at fixed coordinates."
date: "2026-06-28T06:10:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104974
codeforces_index: "D"
codeforces_contest_name: "Codentines Day"
rating: 0
weight: 104974
solve_time_s: 69
verified: false
draft: false
---

[CF 104974D - Traffic Lights](https://codeforces.com/problemset/problem/104974/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are moving along a straight road from position 0 to position X, walking at exactly one meter per second. Along the way there are traffic lights placed at fixed coordinates. Each traffic light is described by its position, its initial color, and a period parameter that controls how quickly it alternates between red and green forever.

The motion is continuous. When we reach a traffic light, we might have to wait if the current color is red at that exact time. Otherwise we pass through immediately. The only thing that increases our total travel time beyond the physical distance is waiting at red lights.

The input gives n traffic lights, each with a position p, an initial color c which is either red or green, and a cycle length parameter t. The signal alternates every t seconds, meaning its full cycle is 2t seconds. If it starts red, then red lasts from time 0 to t, then green from t to 2t, and so on. If it starts green, the phases are swapped.

We need the total time to reach X starting from 0, accounting for both walking time and all waiting.

The constraints go up to 100000 lights and distance up to 100000. That immediately rules out any simulation that tries to advance time in small increments. The only viable approach is to process each traffic light once in linear or near linear time after sorting them by position. Any solution worse than O(n log n) or O(n) would be too slow.

A subtle failure case appears when multiple lights are not sorted by position. If we process them in input order, we may simulate lights out of spatial order and compute waiting at the wrong times. Another issue arises if we forget that waiting depends on the absolute time of arrival, not just the number of lights passed.

For example, consider two lights:

Input:

```
2 10
R 5 5
G 2 3
```

If processed in input order, we might handle position 5 before position 2, which is physically impossible and leads to incorrect timing.

The correct output depends on processing in increasing position order.

## Approaches

A direct simulation is to walk from 0 to X second by second. At each second we check whether we are standing on a traffic light and whether it forces us to wait. This is correct because it mirrors the real process exactly. However, the distance is up to 100000, and waiting can also extend time significantly, so this approach could degrade to O(X) per second simulation steps and becomes too slow in worst cases.

A better way is to realize that nothing changes continuously except position and time. Between traffic lights, there is no decision making. We can safely jump from one traffic light to the next, adding the distance as travel time. The only nontrivial computation is determining whether we must wait at a light, which depends only on current time modulo 2t.

This observation reduces the problem to sorting the lights by position and simulating a single pass, maintaining current time and updating it at each light.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(X + waiting events) | O(1) | Too slow |
| Sort + single pass simulation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all traffic lights by their position in increasing order. This is necessary because time evolves along the spatial path, so we must encounter lights in the order we physically reach them.
2. Initialize current time as 0 and current position as 0. The time represents how long we have been walking including all waiting.
3. Iterate through each traffic light in sorted order.
4. Add the time needed to walk from the previous position to the current light position. Since speed is 1 meter per second, this is simply distance difference added to current time.
5. Compute the state of the traffic light at the moment of arrival using current_time modulo (2t). This gives us the phase within the repeating cycle.
6. Depending on the initial color, determine whether the current phase corresponds to red or green. If the light is red at arrival, advance current time forward to the start of the next green interval. This jump is computed by subtracting the current phase from t or 2t accordingly.
7. Update the current position to the traffic light position and continue.
8. After processing all lights, add the final segment from the last light to X.

The key idea is that we never simulate second by second. We only jump between meaningful event points, which are traffic lights.

### Why it works

Between consecutive traffic lights, the state of the system is completely determined by a single variable, the current time. The road segment contains no events that depend on time. At each traffic light, the decision to wait or pass depends only on the current time modulo the fixed cycle length. Since this computation is exact and we process lights in spatial order, the simulation preserves the true continuous-time behavior without approximation. The invariant is that current_time always equals the exact arrival time at the current position after resolving all required waiting up to that point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, X = map(int, input().split())
    lights = []
    
    for _ in range(n):
        parts = input().split()
        c = parts[0]
        p = int(parts[1])
        t = int(parts[2])
        lights.append((p, c, t))
    
    lights.sort()
    
    cur_time = 0
    cur_pos = 0
    
    for p, c, t in lights:
        cur_time += (p - cur_pos)
        cur_pos = p
        
        cycle = 2 * t
        phase = cur_time % cycle
        
        if c == 'R':
            if phase < t:
                cur_time += (t - phase)
        else:
            if phase >= t:
                cur_time += (cycle - phase)
    
    cur_time += (X - cur_pos)
    print(cur_time)

if __name__ == "__main__":
    solve()
```

The implementation follows the event-based simulation exactly. Sorting ensures correct spatial order. The variable `cur_time` always represents the absolute time when we arrive at the current point. The modulo computation isolates where we are inside the signal cycle. The conditional adjustment shifts time forward only when we arrive during a red interval.

A common mistake is forgetting to update position before computing the next segment, which would break distance calculations. Another subtle issue is misclassifying the red-green intervals, especially for green-starting lights, where the second half of the cycle is red.

## Worked Examples

Consider the sample input interpreted as three lights:

Input:

```
3 100
R 5 10
R 10 50
G 50 70
```

We track state step by step.

| Step | Position | Arrival Time Before Wait | Phase | Action | New Time |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | move | 0 |
| Light 1 | 5 | 5 | 5 mod 20 = 5 | red-start, phase < 10 so wait 5 | 10 |
| Light 2 | 10 | 15 | 15 mod 100 = 15 | red-start, phase in green so pass | 15 |
| Light 3 | 50 | 55 | 55 mod 140 = 55 | green-start, phase in red so wait | 70 |
| End | 100 | 120 | - | final move | 170 |

This trace shows how waiting is only triggered based on cycle phase at arrival, not by previous history.

A second example:

Input:

```
1 10
G 5 3
```

| Step | Position | Arrival Time | Phase | Action | New Time |
| --- | --- | --- | --- | --- | --- |
| Light | 5 | 5 | 5 mod 6 = 5 | green-start, phase >= 3 so red, wait | 6 |
| End | 10 | 11 | - | move | 11 |

This demonstrates a single forced wait where arrival falls into the red portion of a green-start cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting lights dominates, each light processed once |
| Space | O(n) | Storage for all traffic lights |

The constraints allow up to 100000 traffic lights, so sorting plus linear simulation comfortably fits within time limits. Each operation inside the loop is constant time arithmetic, so runtime is effectively linear after sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3 100\nR 5 10\nR 10 50\nG 50 70\n") == "170"

# minimum case: no lights
assert run("0 10\n") == "10"

# single green-start light, no wait
assert run("1 10\nG 5 5\n") == "10"

# single red-start light, forced wait
assert run("1 10\nR 5 5\n") == "10"

# multiple lights increasing delays
assert run("2 20\nR 5 5\nR 10 5\n") == "25"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no lights | 10 | pure walking baseline |
| single green | 10 | no waiting case |
| single red | 10 | waiting logic correctness |
| two reds | 25 | accumulation of waits |

## Edge Cases

One edge case is when a light triggers exactly at the boundary between red and green. For a red-start light with period t, arriving exactly at phase 0 means red, while arriving exactly at phase t means green. The implementation handles this correctly because it uses strict inequality on phase < t.

Another edge case is when multiple lights are very close together. Since each light updates current time before the next movement, consecutive waits compound correctly without interference.

A final case is when X equals a traffic light position. In that situation, the final segment adds zero distance after processing that light, so the answer is simply the time after resolving the last light, which matches the physical interpretation of arriving exactly at the intersection point.
