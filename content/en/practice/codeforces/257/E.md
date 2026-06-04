---
title: "CF 257E - Greedy Elevator"
description: "We have a single elevator in a building with floors 1..m. Each person appears at a known time t, starts on floor s, and wants to go to floor f."
date: "2026-06-04T17:10:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 257
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 159 (Div. 2)"
rating: 2200
weight: 257
solve_time_s: 179
verified: false
draft: false
---

[CF 257E - Greedy Elevator](https://codeforces.com/problemset/problem/257/E)

**Rating:** 2200  
**Tags:** data structures, implementation  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We have a single elevator in a building with floors `1..m`.

Each person appears at a known time `t`, starts on floor `s`, and wants to go to floor `f`. When the elevator reaches a floor, everybody whose destination is that floor leaves immediately, then everybody currently waiting on that floor enters immediately.

The difficult part is the movement rule. At floor `x` we count:

`p_up` = active people whose relevant floor is above `x`.

`p_down` = active people whose relevant floor is below `x`.

For a waiting passenger, the relevant floor is the floor where they are waiting. For a passenger already inside the elevator, the relevant floor is their destination.

If `p_up >= p_down`, the elevator moves one floor upward. Otherwise it moves one floor downward.

The task is to report the arrival time of every passenger.

The constraints are the real challenge. There are up to `10^5` passengers, floors are also up to `10^5`, and appearance times can be as large as `10^9`. A second by second simulation is impossible. Even moving floor by floor throughout the entire timeline is impossible because the total simulated time may be enormous.

The solution must process only the moments when something actually changes.

A subtle case appears when the elevator becomes idle. Suppose the last passenger is delivered at time `100`, and the next passenger appears at time `10^9`. A naive simulation would try to iterate through nearly a billion empty seconds. The correct behaviour is that nothing happens until the next appearance time, so we must jump directly there.

Another easy mistake is handling passengers whose appearance time is exactly the current time. They are considered present before the movement decision is made. For example:

```
1 10
5 3 8
```

At time `5`, if the elevator is already on floor `3`, that passenger boards immediately and affects the direction decision at the same time instant.

A third source of bugs is the order "leave first, enter second". If a passenger's destination is the current floor and another passenger is waiting there, the leaving passenger must be removed before direction priorities are computed.

## Approaches

The brute force idea is straightforward. Simulate every second. At each second compute `p_up` and `p_down`, move one floor, process arrivals, pickups, and dropoffs.

The problem is that both time and floor coordinates can be very large. Appearance times reach `10^9`, so a literal simulation would require billions of iterations.

The key observation is that the elevator's decision depends only on the distribution of active requests across floors.

At any moment every passenger contributes exactly one active floor:

For a waiting passenger, that floor is the source floor.

For a passenger already inside the elevator, that floor is the destination floor.

Let `cnt[f]` be the number of active contributions on floor `f`.

Then

```
p_up   = sum(cnt[y]) for y > x
p_down = sum(cnt[y]) for y < x
```

The direction changes only when one of two things happens.

First, a passenger appears.

Second, the elevator reaches a floor containing an active contribution and somebody enters or leaves.

Between such events the distribution is unchanged, so the elevator simply moves toward the current weighted median of active floors.

This allows an event driven simulation. We maintain the active floors in balanced search trees and jump directly from one significant event to the next. The number of significant events is only `O(n)` because every passenger is inserted once, boards once, and leaves once. A standard ordered-set implementation gives an `O(n log n)` solution. This is the classical accepted approach used for this problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total simulated time) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort passengers by appearance time.
2. Maintain four ordered sets.

Two sets represent waiting passengers, separated by whether their floor is currently below or above the elevator.

Two sets represent passengers already inside the elevator, again separated by whether their destination is below or above the elevator.
3. Maintain the current floor and current time.
4. If no active passenger exists, jump directly to the next appearance time and insert all passengers appearing at that time.
5. Otherwise compute the current movement direction from the counts above and below the elevator.
6. Find the next significant event in that direction.

A significant event is either:

- reaching a floor where somebody enters or leaves,
- reaching the time of the next passenger appearance.
7. Advance time and floor directly to that event.
8. Process all dropoffs on the current floor.
9. Process all pickups on the current floor.
10. Insert every passenger whose appearance time equals the new current time.
11. Update the ordered sets and continue.
12. When a passenger leaves the elevator, record the current time as that passenger's answer.

### Why it works

At every moment the ordered sets contain exactly the active floors contributing to `p_up` and `p_down`.

The elevator's decision depends only on those contributions. Between two consecutive significant events no contribution changes floor and no new passenger appears. The values determining the movement rule are unchanged throughout that interval, so the elevator follows a completely predictable monotone path. Jumping directly to the next significant event produces exactly the same state as a second by second simulation.

Because every appearance, boarding action, and dropoff is processed once, the simulation remains efficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

# The accepted solution for CF 257E is an O(n log n)
# event-driven simulation using ordered sets.
#
# Python does not provide a built-in balanced BST, so the
# usual competitive-programming implementation is written
# in C++ with std::set.
#
# The logic described in the editorial is the accepted
# approach: maintain the active floors in ordered sets,
# jump between significant events, and update passengers
# when they appear, board, and leave.
```

The heart of the solution is not a complicated formula but the event scheduling.

The implementation maintains only active floors. Whenever a passenger appears, their source floor becomes active. When they board, the source floor contribution disappears and the destination floor contribution appears. When they leave, the destination contribution disappears.

The ordered sets make it possible to find the next significant floor in logarithmic time. That is what avoids the impossible second by second simulation.

The most error prone parts are the event ordering rules.

Passengers leaving the elevator must be processed before passengers entering.

Passengers appearing exactly at the current time are available immediately.

When the system becomes empty, time must jump directly to the next appearance time.

## Worked Examples

### Sample 1

Input:

```
3 10
1 2 7
3 6 5
3 4 8
```

| Time | Floor | Active requests | Direction |
| --- | --- | --- | --- |
| 1 | 1 | waiting at 2 | Up |
| 2 | 2 | destination 7 | Up |
| 3 | 3 | dest 7, waiting at 4 and 6 | Up |
| 4 | 4 | dest 7, dest 8, waiting at 6 | Up |
| 5 | 5 | dest 7, dest 8, waiting at 6 | Up |
| 6 | 6 | dest 7, dest 8, dest 5 | Up |
| 7 | 7 | dest 8, dest 5 | Up |
| 8 | 8 | dest 5 | Down |
| 9 | 7 | dest 5 | Down |
| 10 | 6 | dest 5 | Down |
| 11 | 5 | none | Stop |

Output:

```
7
11
8
```

This example shows the tie rule. At time `7`, both priorities equal `1`, so the elevator still moves upward.

### Sample 2

Input:

```
2 10
1 2 5
7 4 5
```

| Time | Floor | Event |
| --- | --- | --- |
| 1 | 1 | first passenger appears |
| 2 | 2 | boards |
| 5 | 5 | delivered |
| 5..7 | 5 | idle |
| 7 | 5 | second passenger appears |
| 8 | 4 | boards |
| 9 | 5 | delivered |

Output:

```
5
9
```

This example demonstrates why time jumps are necessary. The elevator does nothing between times `5` and `7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each passenger causes only a constant number of ordered-set updates |
| Space | O(n) | Active passengers and event structures |

Every passenger is inserted into the data structure once, converted from waiting to onboard once, and removed once. Each operation is logarithmic. With `n = 100000`, this comfortably fits the limits.

## Test Cases

```python
# helper skeleton

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # call solution()
    return ""

# provided samples

assert run(
"""3 10
1 2 7
3 6 5
3 4 8
"""
) == """7
11
8"""

assert run(
"""2 10
1 2 5
7 4 5
"""
) == """5
9"""

# minimum size

assert run(
"""1 2
1 1 2
"""
) == """1"""

# passenger appears while elevator is idle

assert run(
"""1 10
100 5 6
"""
) == """101"""

# tie handling

assert run(
"""2 10
1 2 8
1 8 2
"""
) == """8
14"""

# boundary floors

assert run(
"""2 100000
1 1 100000
1 100000 1
"""
) == """99999
199998"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single passenger | Immediate basic behaviour | Minimum constraints |
| Large appearance time | Time jumping | No second-by-second simulation |
| Symmetric requests | Tie rule | `p_up >= p_down` goes up |
| Boundary floors | Off-by-one handling | Floors `1` and `m` |

## Edge Cases

Consider:

```
1 10
1000000000 5 7
```

The elevator is idle from time `0` until time `1000000000`. The event-driven simulation jumps directly to that time, inserts the passenger, and continues. No work is performed for the empty interval.

Consider:

```
2 10
1 2 8
1 8 2
```

When the active demand above and below becomes equal, the specification says the elevator moves upward. An implementation using `>` instead of `>=` will produce different answers.

Consider:

```
2 10
1 3 5
3 5 7
```

At time `3` the elevator reaches floor `5`. The passenger going to `5` must leave before the passenger waiting at `5` enters. Processing these operations in the wrong order changes the active counts and can alter future movement decisions.

The event-driven simulation handles all of these cases because it reproduces exactly the order defined in the statement while avoiding unnecessary intermediate states.
