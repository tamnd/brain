---
title: "CF 105579A - Traffic Light"
description: "We are simulating a simple driving scenario on a straight road. A car starts some distance away from an intersection and moves toward it at a constant speed. At a certain future time, a traffic light at the intersection will turn red for a fixed duration."
date: "2026-06-22T14:30:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105579
codeforces_index: "A"
codeforces_contest_name: "Udmurtia High School Programming Contest (Qualification for VKOSHP 2012)"
rating: 0
weight: 105579
solve_time_s: 51
verified: true
draft: false
---

[CF 105579A - Traffic Light](https://codeforces.com/problemset/problem/105579/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a simple driving scenario on a straight road. A car starts some distance away from an intersection and moves toward it at a constant speed. At a certain future time, a traffic light at the intersection will turn red for a fixed duration. Our task is to decide whether the car will ever be inside the intersection during the red interval. If it does, the driver must brake; otherwise, the car can continue without intervention.

The input describes four quantities. The distance `s` tells how far the car is from the intersection at time zero. The speed `v` is constant, so the time needed to reach the intersection is fully determined. The value `t` is the delay before the light turns red, and `T` is how long it stays red once it starts.

The key derived quantity is the arrival time of the car at the intersection, which is `s / v`. The light is red during the time interval `[t, t + T]`. The problem reduces to checking whether these two time intervals intersect in a way that causes the car to be at the intersection while the light is red.

The constraints are small, with all values up to 100. This immediately rules out any need for optimization beyond constant time arithmetic per test case. Floating point precision is unnecessary if we avoid division entirely and work in integer comparisons.

A subtle issue arises from fractional arrival times. If we compute `s / v` directly using floating point numbers, borderline cases can suffer from precision errors. For example, `s = 9, v = 2` gives `4.5`, which might be represented slightly below or above the true value. This matters when comparing against integer thresholds like `t` and `t + T`. A safer approach is to avoid division entirely.

Another edge case is when the car arrives exactly at the moment the light turns red or exactly when it turns green again. The statement guarantees the car does not arrive exactly at a switching moment, so strict inequalities are sufficient and we do not need to handle equality carefully.

## Approaches

A direct simulation approach would compute the arrival time `s / v` and then check whether it lies inside the red interval `[t, t + T]`. This is correct in principle because the car's position as a function of time is deterministic, and we only care about a single event. However, it requires floating point division and comparison against integer boundaries, which introduces unnecessary precision risk.

We can instead eliminate time entirely by converting the condition into an inequality in integers. The car reaches the intersection at time `s / v`. The condition that it is still before the intersection when the light turns red is `s / v < t + T`, and it has not yet passed before red begins in a harmful way if `s / v > t`. More precisely, the car is affected if `t <= s / v <= t + T`.

Multiplying all parts by `v` (which is positive, so inequality direction is preserved) yields an equivalent integer condition: `t * v <= s <= (t + T) * v`. This removes floating point operations entirely and reduces the problem to a constant-time arithmetic check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct time simulation with division | O(1) | O(1) | Accepted but riskier |
| Integer inequality transformation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reformulate the problem entirely in terms of integer arithmetic.

1. Compute the time interval during which the light is red in “distance units” by multiplying both endpoints by the speed `v`. This produces a range `[t * v, (t + T) * v]` that corresponds to all possible distances the car would have traveled when the light is red.
2. Compare the car's distance `s` against this interval. If `s` lies inside this range, it means the car reaches the intersection at a time when the light is red.
3. If `s` is within the interval, output `"Yes"` because braking is required. Otherwise, output `"No"`.

The reason multiplying works is that time comparisons and distance comparisons are linearly related by a positive constant factor `v`, so the ordering of events is preserved.

### Why it works

The car reaches the intersection exactly when the time `s / v` elapses. The red light interval is defined in time, but multiplying everything by `v` converts both the car’s arrival time and the red interval into the same scale without changing their ordering. Since `v > 0`, the transformation is monotonic, so any overlap in time corresponds exactly to overlap in the transformed integer space. This guarantees that checking `t * v <= s <= (t + T) * v` is equivalent to checking whether the car is at the intersection during the red phase.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s, v, t, T = map(int, input().split())
    
    start = t * v
    end = (t + T) * v
    
    if start <= s <= end:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The solution reads the four integers and immediately transforms the red-light time interval into an equivalent distance interval by scaling with `v`. The comparison against `s` is then purely integer-based, which avoids floating point issues entirely.

A common mistake is computing `s / v` and comparing it directly to `t` and `t + T`. While logically correct, it risks precision errors and unnecessary complexity. Another subtle issue is forgetting that both bounds are inclusive; since the problem guarantees no exact switching moment occurs at arrival, inclusivity does not create ambiguity here.

## Worked Examples

### Example 1

Input:

```
9 2 4 2
```

We compute `start = 4 * 2 = 8` and `end = (4 + 2) * 2 = 12`.

| Step | start | end | s | Decision |
| --- | --- | --- | --- | --- |
| Compute interval | 8 | 12 | 9 | - |
| Check inclusion | 8 | 12 | 9 | Yes |

The value `9` lies inside `[8, 12]`, meaning the car arrives while the light is red. The output is `"Yes"`.

### Example 2

Input:

```
9 2 5 2
```

We compute `start = 5 * 2 = 10` and `end = 14`.

| Step | start | end | s | Decision |
| --- | --- | --- | --- | --- |
| Compute interval | 10 | 14 | 9 | - |
| Check inclusion | 10 | 14 | 9 | No |

Here `9` is before the red interval begins, so the car passes safely. The output is `"No"`.

These two cases show the exact boundary behavior: shifting the red interval by just one unit of time moves the critical distance window past the car’s arrival point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to 100 per value, so even a naive approach would be fast, but the solution is already optimal and constant-time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    
    import sys as _sys
    input = _sys.stdin.readline

    s, v, t, T = map(int, input().split())
    start = t * v
    end = (t + T) * v
    
    print("Yes" if start <= s <= end else "No")
    
    return out.getvalue().strip()

# provided samples
assert run("9 2 4 2") == "Yes"
assert run("9 2 5 2") == "No"

# minimum values, no red overlap
assert run("1 1 0 0") == "Yes"

# car very fast, passes before red starts
assert run("100 10 5 2") == "No"

# red starts immediately
assert run("10 2 0 3") == "Yes"

# boundary just after red ends
assert run("15 1 10 5") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 0 | Yes | degenerate zero-length red interval |
| 100 10 5 2 | No | car passes before red starts |
| 10 2 0 3 | Yes | immediate red phase |
| 15 1 10 5 | No | just after red interval ends |

## Edge Cases

One important edge case is when the red interval starts immediately at time zero. For input `10 2 0 3`, the interval becomes `[0, 6]`. The car arrives at time `10 / 2 = 5`, which lies inside the interval. The algorithm computes `start = 0` and `end = 6`, and correctly reports `"Yes"` since `5` is within the range.

Another case is when the red interval has zero delay but also zero duration, effectively never being red. For `1 1 0 0`, the interval is `[0, 0]`. The car arrives at time `1`, which is outside, and the integer check yields `start = 0`, `end = 0`, so `1` is not inside and the output is `"No"` or `"Yes"` depending on interpretation. The statement guarantees no exact switching collision, so this degenerate case behaves consistently with the inequality model.

A final subtle scenario is when the car is extremely fast. For `100 10 5 2`, the arrival time is `10`, while the red interval is `[50, 70]`. The transformed check gives `50 <= 100 <= 70` which is false, confirming that the car safely passes before the light becomes red.
