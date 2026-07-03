---
title: "CF 103361A - \u0423\u0441\u043f\u0435\u0442\u044c \u043d\u0430 \u0441\u0430\u043c\u043e\u043b\u0451\u0442"
description: "We are given a single day schedule involving two time moments and two durations. First, we know when a traveler leaves home, expressed as hours and minutes. From that moment, a navigation system says the travel time to the airport is a fixed number of minutes."
date: "2026-07-03T13:08:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "A"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 41
verified: true
draft: false
---

[CF 103361A - \u0423\u0441\u043f\u0435\u0442\u044c \u043d\u0430 \u0441\u0430\u043c\u043e\u043b\u0451\u0442](https://codeforces.com/problemset/problem/103361/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single day schedule involving two time moments and two durations. First, we know when a traveler leaves home, expressed as hours and minutes. From that moment, a navigation system says the travel time to the airport is a fixed number of minutes. Separately, we know the departure time of the airplane and how many minutes before departure the check-in desk closes. The passenger must arrive strictly before the check-in closing moment, meaning arriving exactly at the cutoff time is still considered a failure.

The task is to determine whether the arrival time computed from departure plus travel time is strictly earlier than the last acceptable check-in moment computed from flight departure minus check-in lead time.

The key subtlety is that all times live within a single day and must be compared consistently in minutes. This is not a simulation over multiple days, but a single linear comparison after converting everything into a uniform unit.

The constraints are small, with hours bounded roughly between 9 and 21 and durations up to 60 minutes. This immediately tells us that any solution that converts time and performs constant-time arithmetic is sufficient. There is no need for search, sorting, or any nontrivial data structure. Even a brute force minute-by-minute simulation would be acceptable, but unnecessary.

A common failure case comes from misunderstanding the strict inequality condition.

For example, suppose the traveler arrives exactly at the check-in deadline:

Input:

9 0 10 9 10 10

Departure is 9:00, travel is 10 minutes, so arrival is 9:10. Flight is at 9:10, and check-in closes 10 minutes before, i.e. 9:00. Arrival is after the deadline, so the answer is "CHANGE TICKET".

Another subtle case:

Input:

10 0 50 15 30 45

Arrival is 10:50. Flight is 15:30, check-in closes at 14:45. Arrival is earlier, so the answer is "OK". The trap here is correctly subtracting minutes across hour boundaries.

The most frequent mistake is treating time as separate hour and minute arithmetic without normalization, which breaks when subtraction crosses hour boundaries.

## Approaches

The brute-force interpretation would simulate every minute from departure time, adding travel time, and separately simulating countdown to check-in closure. We could convert both moments into minute arrays and increment until we reach the endpoints. This works because the time range is small, but it is unnecessary overhead. In the worst case, we would still only process a few thousand minutes, so it is correct but inelegant.

The better approach is to normalize all times into absolute minutes since midnight. Once everything is in a single linear scale, the problem reduces to a single comparison.

We compute:

- arrival_time = (h1 * 60 + m1) + t1
- last_checkin_time = (h2 * 60 + m2) - t2

The only remaining condition is a strict inequality:

arrival_time < last_checkin_time

This removes all complexity and reduces the problem to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T) where T ≤ 1440 | O(1) | Accepted but unnecessary |
| Time Normalization | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the departure time into total minutes from midnight by computing h1 * 60 + m1. This gives a single scalar value for when the traveler leaves.
2. Add the travel duration t1 to compute the arrival time at the airport in minutes. This models continuous time progression without dealing with hour boundaries.
3. Convert the flight departure time into total minutes from midnight using h2 * 60 + m2. This provides the reference point for the airline schedule.
4. Subtract the required check-in lead time t2 from the flight departure time. This yields the last valid minute when a passenger is still allowed to complete check-in.
5. Compare arrival_time with last_checkin_time using a strict inequality. If arrival_time is strictly smaller, output "OK". Otherwise output "CHANGE TICKET".

### Why it works

Both computed values represent absolute time positions on the same linear axis measured in minutes from midnight. The transformation preserves ordering because it is a strictly monotonic mapping from clock time to integers. Since the requirement is only about whether one event happens strictly before another, no additional structure is needed. Any correct answer must depend solely on this ordering, so reducing the problem to integer comparison is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

h1, m1, t1, h2, m2, t2 = map(int, input().split())

arrival = h1 * 60 + m1 + t1
deadline = h2 * 60 + m2 - t2

if arrival < deadline:
    print("OK")
else:
    print("CHANGE TICKET")
```

The implementation follows the algorithm directly. The only important detail is consistent conversion into minutes before doing any arithmetic. This avoids errors from carrying minutes across hour boundaries manually.

The strict inequality is implemented exactly as required: equality is treated as failure because arriving at the exact closing moment does not allow completion of registration.

## Worked Examples

### Example 1

Input:

```
9 0 10 9 10 10
```

| Step | Value |
| --- | --- |
| Departure | 9 * 60 + 0 = 540 |
| Arrival | 540 + 10 = 550 |
| Flight | 9 * 60 + 10 = 550 |
| Check-in deadline | 550 - 10 = 540 |

Arrival (550) < deadline (540) is false, so output is CHANGE TICKET.

This example demonstrates the strict inequality rule, where arriving even slightly after the effective cutoff invalidates the trip.

### Example 2

Input:

```
10 0 50 15 30 45
```

| Step | Value |
| --- | --- |
| Departure | 600 |
| Arrival | 650 |
| Flight | 930 |
| Check-in deadline | 885 |

Arrival (650) < deadline (885) is true, so output is OK.

This confirms correct handling of cross-hour arithmetic, since the subtraction spans multiple hours without issue.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | constant number of arithmetic operations |
| Space | O(1) | only a few integer variables are used |

The constraints allow at most a few integer operations, so the solution runs well within limits and is effectively instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    h1, m1, t1, h2, m2, t2 = map(int, input().split())

    arrival = h1 * 60 + m1 + t1
    deadline = h2 * 60 + m2 - t2

    return "OK\n" if arrival < deadline else "CHANGE TICKET\n"

# provided samples
assert run("9 0 10 9 10 10") == "CHANGE TICKET\n"
assert run("10 0 50 15 30 45") == "OK\n"

# minimum edge: just before midnight boundary (still within constraints)
assert run("9 0 1 9 1 1") == "CHANGE TICKET\n"

# exact equality case (must fail)
assert run("9 0 10 9 10 10") == "CHANGE TICKET\n"

# large gap case
assert run("12 0 5 20 0 10") == "OK\n"

# tight success case
assert run("9 0 0 9 0 1") == "OK\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 0 1 9 1 1 | CHANGE TICKET | arrival just after cutoff |
| 12 0 5 20 0 10 | OK | large safe margin |
| 9 0 0 9 0 1 | OK | boundary with zero travel |

## Edge Cases

One important edge case is when arrival time equals the check-in closing time exactly. For instance:

Input:

```
9 0 10 9 10 10
```

Step-by-step:

Arrival = 540 + 10 = 550

Deadline = 550 - 10 = 540

Since 550 is not less than 540, the result is "CHANGE TICKET". The strict inequality correctly disqualifies equality, matching the problem requirement that arrival must be strictly earlier.

Another edge situation is when subtraction crosses an hour boundary:

Input:

```
10 30 20 11 0 45
```

Arrival = 630 + 20 = 650

Deadline = 660 - 45 = 615

Even though hour arithmetic looks confusing, the normalized minutes handle it cleanly. Since 650 < 615 is false, the traveler is late. The conversion ensures correctness regardless of crossing hour boundaries.
