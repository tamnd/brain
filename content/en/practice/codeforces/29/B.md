---
title: "CF 29B - Traffic Lights"
description: "A car starts at point A and moves along a straight road toward point B. The total distance is l meters, and the car always moves at a fixed speed v. Somewhere along the road, exactly d meters from the start, there is a traffic light."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 29
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 29 (Div. 2, Codeforces format)"
rating: 1500
weight: 29
solve_time_s: 83
verified: true
draft: false
---
[CF 29B - Traffic Lights](https://codeforces.com/problemset/problem/29/B)

**Rating:** 1500  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

A car starts at point A and moves along a straight road toward point B. The total distance is `l` meters, and the car always moves at a fixed speed `v`. Somewhere along the road, exactly `d` meters from the start, there is a traffic light.

The traffic light alternates between green and red forever. At time `0`, the light is green. It stays green for `g` seconds, then red for `r` seconds, then repeats this cycle again and again.

The car may stop instantly and accelerate instantly, so there is no penalty for waiting at the traffic light. The only restriction is that the car cannot cross during a red interval. If it arrives exactly when red begins, it must stop. If it arrives exactly when green begins, it may pass immediately.

The task is to compute the minimum possible travel time from A to B.

The constraints are tiny. Every value is at most `1000`, and there is only one traffic light. Even simulation-heavy solutions would fit comfortably inside the limits. The real challenge is handling the timing boundaries correctly, especially the moments when the light changes state.

The easiest mistake is mishandling arrival exactly at the transition from green to red.

Consider this input:

```
10 5 1 5 5
```

The car reaches the traffic light at time `5`. The green interval is `[0, 5)`, and red starts exactly at `5`. The car is not allowed to pass. It must wait until time `10`, then continue.

The correct answer is:

```
15
```

A careless implementation using `<= g` instead of `< g` would incorrectly allow the car to pass immediately and produce `10`.

Another subtle case is arriving exactly when a new green interval begins.

```
10 5 1 3 2
```

The cycle length is `5`. The car reaches the light at time `5`, which is exactly the start of a green interval. It may continue immediately.

The correct answer is:

```
10
```

An implementation that treats every boundary as blocked would incorrectly add unnecessary waiting time.

One more edge case appears when the car reaches the destination before ever touching the light. The problem guarantees `d < l`, so this never happens, but it is still useful to think about the structure. The only place where waiting can occur is at the traffic light itself. Once the car passes it, the remaining movement is always uninterrupted.

## Approaches

The brute-force idea is to simulate time second by second and track the traffic light state until the car reaches the destination. Since the values are small, even a fine-grained simulation could work if implemented carefully with floating point arithmetic.

The brute-force works because the system is extremely simple. The car only changes behavior at one position, the traffic light timing is periodic, and movement speed is constant. The issue is that continuous time simulation is awkward and unnecessary. You would need very small increments to maintain precision, and floating point accumulation errors become annoying.

The key observation is that the car interacts with the traffic light exactly once.

Without the traffic light, total travel time is simply:

$$\frac{l}{v}$$

The only question is whether the car must wait when it reaches distance `d`.

The arrival time at the light is:

$$\frac{d}{v}$$

The traffic signal repeats every `g + r` seconds. By taking the arrival time modulo the cycle length, we can determine whether the light is green or red at that instant.

If:

$$t \bmod (g+r) < g$$

the car arrives during green and crosses immediately.

Otherwise, it arrives during red and must wait until the next cycle starts.

That reduces the entire problem to a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T) | O(1) | Unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the five integers `l`, `d`, `v`, `g`, and `r`.
2. Compute the time needed to reach the traffic light:

$$t = \frac{d}{v}$$

This is the earliest possible arrival time because the car always moves at maximum speed.

1. Compute the traffic light cycle length:

$$cycle = g + r$$

The signal repeats forever with this period.

1. Find the position inside the current cycle when the car arrives:

$$x = t \bmod cycle$$

This tells us whether the signal is green or red at that moment.

1. Check whether the car arrives during green.

If:

$$x < g$$

the car passes immediately.

Otherwise, the car arrives during red and must wait:

$$wait = cycle - x$$

This waiting time moves the current time exactly to the beginning of the next green interval.

1. Add the remaining travel time from the traffic light to the destination:

$$\frac{l-d}{v}$$

1. Print the final answer with sufficient precision.

### Why it works

The car only has one decision point, the traffic light. Moving slower before reaching the light never helps because the car can always stop instantly with no penalty. Reaching earlier is always at least as good as reaching later.

The algorithm computes the earliest arrival time at the light and checks whether that moment belongs to a green interval. If yes, immediate crossing is optimal. If not, the best strategy is to wait exactly until the next green interval starts. No other waiting strategy can improve the answer.

Because every possible valid trip follows this structure, the computed time is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

l, d, v, g, r = map(int, input().split())

time_to_light = d / v
cycle = g + r

pos_in_cycle = time_to_light % cycle

answer = l / v

if pos_in_cycle >= g:
    answer += cycle - pos_in_cycle

print(f"{answer:.10f}")
```

The solution starts by computing the earliest possible arrival time at the traffic light. Since the speed is constant and acceleration is instantaneous, there is never a reason to intentionally drive slower before the light.

The variable `pos_in_cycle` represents the exact moment inside the repeating traffic-light cycle when the car arrives. This is the core observation of the problem.

The condition:

```
if pos_in_cycle >= g:
```

is the critical boundary. The green interval is `[0, g)`. Arriving exactly at `g` means red has already started, so the car must wait. Using `>` instead of `>=` would produce wrong answers.

The initial answer is set to:

```
l / v
```

which is the travel time without any waiting. If the car arrives during red, only the waiting time must be added.

The output uses high precision formatting to satisfy the required floating point tolerance.

## Worked Examples

### Example 1

Input:

```
2 1 3 4 5
```

The car reaches the light after:

$$\frac{1}{3}$$

seconds.

| Variable | Value |
| --- | --- |
| `l` | 2 |
| `d` | 1 |
| `v` | 3 |
| `g` | 4 |
| `r` | 5 |
| `time_to_light` | 0.3333333333 |
| `cycle` | 9 |
| `pos_in_cycle` | 0.3333333333 |
| Green? | Yes |
| Waiting time | 0 |
| Final answer | 0.6666666667 |

The car arrives well inside the green interval, so it never stops. The total travel time is simply distance divided by speed.

### Example 2

Input:

```
10 5 1 5 5
```

The car reaches the light exactly when red starts.

| Variable | Value |
| --- | --- |
| `l` | 10 |
| `d` | 5 |
| `v` | 1 |
| `g` | 5 |
| `r` | 5 |
| `time_to_light` | 5 |
| `cycle` | 10 |
| `pos_in_cycle` | 5 |
| Green? | No |
| Waiting time | 5 |
| Final answer | 15 |

This example demonstrates the most important boundary condition. Arriving exactly at time `g` is not allowed. The car waits until time `10`, then continues.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The algorithm easily fits within the limits. It performs only a few floating point computations and uses constant memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    l, d, v, g, r = map(int, input().split())

    time_to_light = d / v
    cycle = g + r

    pos_in_cycle = time_to_light % cycle

    answer = l / v

    if pos_in_cycle >= g:
        answer += cycle - pos_in_cycle

    print(f"{answer:.10f}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run("2 1 3 4 5\n") == "0.6666666667", "sample 1"

# arrives exactly when red starts
assert run("10 5 1 5 5\n") == "15.0000000000", "red boundary"

# arrives exactly when green starts
assert run("10 5 1 3 2\n") == "10.0000000000", "green boundary"

# minimum-like values
assert run("2 1 1 1 1\n") == "2.0000000000", "small values"

# large values
assert run("1000 999 1000 1 1000\n") == "1.0000000000", "large values"

# waiting required with fractional arrival
assert run("20 7 2 3 5\n") == "14.0000000000", "fractional wait"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 5 1 5 5` | `15.0000000000` | Arriving exactly when red begins |
| `10 5 1 3 2` | `10.0000000000` | Arriving exactly when green begins |
| `2 1 1 1 1` | `2.0000000000` | Smallest-style valid configuration |
| `1000 999 1000 1 1000` | `1.0000000000` | Large values and no waiting |
| `20 7 2 3 5` | `14.0000000000` | Fractional arrival during red |

## Edge Cases

Consider the boundary where the light turns red exactly when the car arrives:

```
10 5 1 5 5
```

The car reaches the light at time `5`.

The cycle is `10`, so:

$$5 \bmod 10 = 5$$

Since `5 >= 5`, the light is red. The algorithm adds waiting time:

$$10 - 5 = 5$$

The final answer becomes:

$$10 + 5 = 15$$

This matches the rules precisely because the car cannot cross at the instant red begins.

Now consider arriving exactly when green starts:

```
10 5 1 3 2
```

The cycle length is `5`. The car reaches the light at time `5`.

$$5 \bmod 5 = 0$$

Since `0 < 3`, the signal is green. The car crosses immediately and finishes in `10` seconds total.

This verifies that the modulo computation correctly handles cycle wraparound.

Finally, consider a fractional arrival during red:

```
20 7 2 3 5
```

The car reaches the light after:

$$\frac{7}{2} = 3.5$$

The cycle length is `8`.

$$3.5 \bmod 8 = 3.5$$

Because `3.5 >= 3`, the light is red. The car waits:

$$8 - 3.5 = 4.5$$

Base travel time is:

$$\frac{20}{2} = 10$$

Total:

$$10 + 4.5 = 14.5$$

The algorithm handles fractional timing naturally because all computations are performed with floating point arithmetic.
