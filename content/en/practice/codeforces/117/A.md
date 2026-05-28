---
title: "CF 117A - Elevator"
description: "The elevator follows a completely deterministic cycle. It starts at floor 1 at time 0, climbs one floor per second until it reaches floor m, then immediately reverses direction and goes back down to floor 1, again moving one floor per second."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 117
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 88"
rating: 1300
weight: 117
solve_time_s: 151
verified: true
draft: false
---

[CF 117A - Elevator](https://codeforces.com/problemset/problem/117/A)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The elevator follows a completely deterministic cycle.

It starts at floor `1` at time `0`, climbs one floor per second until it reaches floor `m`, then immediately reverses direction and goes back down to floor `1`, again moving one floor per second. After reaching floor `1`, the same pattern repeats forever.

For each participant, we know three things. We know the floor where they start, the floor they want to reach, and the moment when they arrive at the starting floor. A participant enters instantly if the elevator is currently stopped on that floor. The task is to compute the earliest possible arrival time at the destination floor.

The key detail is that the elevator direction matters. A person going upward cannot simply enter the elevator whenever it reaches their floor. They must board during an upward pass. The same applies for downward movement.

The constraints completely rule out simulation. There can be up to `10^5` queries, and both floors and times can be as large as `10^8`. A second-by-second simulation would require up to billions of operations even for one query. We need an `O(1)` formula per participant.

Several edge cases are easy to mishandle.

Consider someone already standing on the destination floor.

Input:

```
1 10
5 5 100
```

Output:

```
100
```

The elevator is irrelevant here. A careless implementation may still compute waiting time and movement.

Another tricky case appears when the elevator reaches the floor exactly at time `t`.

Input:

```
1 4
1 2 0
```

Output:

```
1
```

At time `0`, the elevator is already on floor `1`, so the participant enters immediately. If we accidentally require strictly later arrival, we would incorrectly wait for the next cycle.

Direction mismatches also cause bugs.

Input:

```
1 4
2 4 3
```

Output:

```
9
```

At time `3`, the elevator is indeed at floor `2`, but it is moving downward because the sequence is:

`1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1`.

The participant wants to go upward, so boarding at time `3` is useless. They must wait until the next upward visit at time `7`.

The first and last floors behave differently because the elevator reverses direction there.

Input:

```
1 5
5 1 4
```

Output:

```
8
```

At time `4`, the elevator is exactly at floor `5` and immediately starts moving downward, so the participant can board immediately. Treating turning points incorrectly often introduces off-by-one mistakes.

## Approaches

A brute-force solution would literally simulate elevator movement over time. For every second, we would track the elevator floor and direction, and for every participant we would wait until the elevator reaches the correct floor while moving in the required direction.

This works logically because the elevator path is deterministic. Eventually every valid boarding moment appears during simulation.

The problem is scale. The elevator cycle length is `2 * (m - 1)`, which may reach almost `2 * 10^8`. Simulating even one full cycle for every participant is far too slow. With `10^5` participants, the operation count becomes completely infeasible.

The important observation is that the elevator movement is periodic.

For a floor `x`:

If the elevator is moving upward, it reaches floor `x` at times:

```
x - 1 + k * cycle
```

If the elevator is moving downward, it reaches floor `x` at times:

```
(m - x) + (m - 1) + k * cycle
```

where:

```
cycle = 2 * (m - 1)
```

Once we know the required direction, we can directly compute the first valid boarding time greater than or equal to `t`.

Suppose the participant wants to go upward. Then we need the first time:

```
x - 1 + k * cycle >= t
```

We can compute `k` with simple arithmetic instead of simulation.

After boarding, travel time is just:

```
abs(f - s)
```

The whole problem becomes constant-time arithmetic per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the elevator cycle length:

```
cycle = 2 * (m - 1)
```

After this many seconds, the elevator returns to floor `1` in the same state.
2. For each participant, first check whether `s == f`.

If the participant already starts at the destination, the answer is simply `t`.
3. Determine the required movement direction.

If `f > s`, the participant must board during an upward pass.

Otherwise, they must board during a downward pass.
4. Compute the first time when the elevator reaches floor `s` in the required direction.

For upward movement, the base visit time inside one cycle is:

```
base = s - 1
```

For downward movement:

```
base = (m - 1) + (m - s)
```
5. Find the smallest non-negative integer `k` such that:

```
base + k * cycle >= t
```

This is ceiling division:

```
k = max(0, (t - base + cycle - 1) // cycle)
```
6. The boarding time becomes:

```
board = base + k * cycle
```
7. Add the travel distance:

```
answer = board + abs(f - s)
```

### Why it works

The elevator trajectory repeats perfectly every `2 * (m - 1)` seconds. For every floor and direction pair, there is exactly one visit time inside each cycle. The algorithm computes that canonical visit time and jumps directly to the first cycle where the elevator arrives no earlier than `t`.

Because the elevator moves one floor per second without interruptions, the time from `s` to `f` after boarding is always exactly `abs(f - s)`. Since we always choose the earliest valid boarding moment, the resulting arrival time is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    cycle = 2 * (m - 1)

    ans = []

    for _ in range(n):
        s, f, t = map(int, input().split())

        if s == f:
            ans.append(str(t))
            continue

        if f > s:
            base = s - 1
        else:
            base = (m - 1) + (m - s)

        if t <= base:
            board = base
        else:
            k = (t - base + cycle - 1) // cycle
            board = base + k * cycle

        arrival = board + abs(f - s)
        ans.append(str(arrival))

    print("\n".join(ans))

solve()
```

The first part computes the cycle length. The elevator path from `1` up to `m` and back to `1` takes exactly `2 * (m - 1)` seconds.

For each query, the special case `s == f` is handled immediately. Forgetting this case often produces wrong answers because the general boarding logic assumes the participant must actually ride the elevator.

The variable `base` represents the first moment inside a cycle when the elevator visits floor `s` in the required direction.

For upward travel:

```
base = s - 1
```

because the elevator starts at floor `1` at time `0` and climbs one floor per second.

For downward travel:

```
base = (m - 1) + (m - s)
```

The elevator first spends `m - 1` seconds reaching the top floor, then another `m - s` seconds descending to floor `s`.

The ceiling-division step is the core arithmetic trick:

```
(t - base + cycle - 1) // cycle
```

This computes the smallest number of complete cycles needed so that the visit time is at least `t`.

The implementation carefully handles `t <= base` separately. Without that branch, negative values could appear in the division expression.

Python integers easily handle the largest values here, since answers remain well below `10^9`.

## Worked Examples

### Example 1

Input:

```
4 4
2 4 3
1 2 0
4 2 0
2 2 5
```

Cycle length:

```
2 * (4 - 1) = 6
```

| s | f | t | Direction | base | board | arrival |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 4 | 3 | up | 1 | 7 | 9 |
| 1 | 2 | 0 | up | 0 | 0 | 1 |
| 4 | 2 | 0 | down | 3 | 3 | 5 |
| 2 | 2 | 5 | none | - | - | 5 |

The first query demonstrates why direction matters. The elevator reaches floor `2` at time `1` while moving upward and again at time `5` while moving downward. Since the participant arrives at time `3`, both visits are unusable. The next upward visit happens at time `7`.

### Example 2

Input:

```
3 5
5 1 4
3 4 20
2 1 1
```

Cycle length:

```
2 * (5 - 1) = 8
```

| s | f | t | Direction | base | board | arrival |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 1 | 4 | down | 4 | 4 | 8 |
| 3 | 4 | 20 | up | 2 | 26 | 27 |
| 2 | 1 | 1 | down | 7 | 7 | 8 |

The second query shows how the cycle jump works. Upward visits to floor `3` happen at times:

```
2, 10, 18, 26, ...
```

Since the participant appears at time `20`, the first valid boarding time is `26`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each participant is processed with constant-time arithmetic |
| Space | O(1) | Only a few variables are stored besides the output |

With `10^5` participants, linear time is easily fast enough. The solution performs only several arithmetic operations per query and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    cycle = 2 * (m - 1)

    ans = []

    for _ in range(n):
        s, f, t = map(int, input().split())

        if s == f:
            ans.append(str(t))
            continue

        if f > s:
            base = s - 1
        else:
            base = (m - 1) + (m - s)

        if t <= base:
            board = base
        else:
            k = (t - base + cycle - 1) // cycle
            board = base + k * cycle

        ans.append(str(board + abs(f - s)))

    print("\n".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup

    return out.getvalue()

# provided sample
assert run(
"""7 4
2 4 3
1 2 0
2 2 0
1 2 1
4 3 5
1 2 2
4 2 0
"""
) == """9
1
0
7
10
7
5
"""

# minimum size
assert run(
"""1 2
1 2 0
"""
) == """1
"""

# already at destination
assert run(
"""1 10
5 5 100
"""
) == """100
"""

# exact turning point at top floor
assert run(
"""1 5
5 1 4
"""
) == """8
"""

# waits multiple cycles
assert run(
"""1 5
3 4 20
"""
) == """27
"""

# catches direction mistake
assert run(
"""1 4
2 4 3
"""
) == """9
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1 2 0` | `1` | Smallest valid instance |
| `5 5 100` | `100` | Starting floor equals destination |
| `5 1 4` | `8` | Correct handling at turning point |
| `3 4 20` | `27` | Multiple-cycle waiting logic |
| `2 4 3` | `9` | Elevator direction matters |

## Edge Cases

Consider the case where the participant already starts at the target floor.

Input:

```
1 10
5 5 100
```

The algorithm immediately detects `s == f` and returns `100`. No boarding logic runs at all. This avoids accidentally forcing the participant to ride the elevator unnecessarily.

Now consider exact elevator arrival time.

Input:

```
1 4
1 2 0
```

For upward movement:

```
base = 1 - 1 = 0
```

Since:

```
t = 0
```

the algorithm boards immediately:

```
board = 0
arrival = 0 + 1 = 1
```

The equality case is important. Using a strict comparison would incorrectly delay boarding by one entire cycle.

Direction mismatch is another subtle situation.

Input:

```
1 4
2 4 3
```

The cycle length is:

```
6
```

Upward visits to floor `2` occur at:

```
1, 7, 13, ...
```

Downward visits occur at:

```
5, 11, ...
```

The participant arrives at time `3`, so neither nearby visit works. The algorithm correctly chooses the next upward visit at time `7`, producing:

```
7 + 2 = 9
```

Finally, consider the top floor turning point.

Input:

```
1 5
5 1 4
```

For downward movement:

```
base = (5 - 1) + (5 - 5) = 4
```

Since `t == base`, boarding happens immediately at the top floor during the downward phase. Travel time is `4`, so arrival time becomes `8`.

This confirms the reversal behavior is handled correctly without any off-by-one errors.
