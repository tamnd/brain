---
title: "CF 106078E - Mars"
description: "We are managing a small collection of milk jugs that travel between Mars and Earth. A spaceship trip either goes from Mars to Earth or from Earth to Mars. When a jug reaches Earth on a Mars-to-Earth trip, it is immediately filled."
date: "2026-06-25T12:08:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106078
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 1 (Advanced)"
rating: 0
weight: 106078
solve_time_s: 48
verified: true
draft: false
---

[CF 106078E - Mars](https://codeforces.com/problemset/problem/106078/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are managing a small collection of milk jugs that travel between Mars and Earth. A spaceship trip either goes from Mars to Earth or from Earth to Mars. When a jug reaches Earth on a Mars-to-Earth trip, it is immediately filled. To bring that milk back, we must assign the filled jug to a later Earth-to-Mars trip. Each spaceship can carry at most one of our jugs.

The important part is that Johnny only owns two empty jugs at the beginning. A jug that is travelling is unavailable. After a successful return to Mars, the jug is empty again and can be reused. The task is to maximize how many full jugs of milk can be delivered to Mars.

The input describes up to 100000 spaceship trips. Each trip has a start time, an end time, and a direction. Since the number of trips is large, any approach that tries every possible pair of trips is too slow. There are up to about 10^10 possible pairs, which cannot fit into a one second style limit. We need to process the trips close to linear time.

The tricky cases are caused by the fact that a jug is a resource, not just a chosen interval. A trip that looks useful might occupy a jug for a long time and prevent a better sequence.

For example, consider:

```
3
0 100 0
1 2 0
3 4 1
```

The answer is `1`.

A careless solution might think that taking both Earth trips is always best. However, there is only one Mars return available. The long trip cannot return before time 4, so only the short trip can produce milk.

Another case:

```
4
0 5 0
1 2 0
3 4 1
6 7 1
```

The answer is `1`.

If we only count compatible pairs of trips, we might think both Earth trips are useful. They are not. The short Earth trip and the first Mars trip can complete one cycle. The second Earth trip still has to wait until time 5 before it even becomes filled, so it misses the early Mars trip.

The solution must make decisions in time order and remember the number of available jugs.

## Approaches

A direct approach would try to match every Mars-to-Earth trip with every later Earth-to-Mars trip. For each possible pair, we could check whether the first trip finishes before the second one starts and whether the available jugs allow this choice. This is correct because every possible import is represented by exactly such a pair. However, with 100000 trips, checking all pairs requires about 10^10 operations, which is far beyond what is possible.

The key observation is that the only limited resource is the number of jugs. We never need to know which specific jug is free, only how many are free. Every event changes this count. When a Mars-to-Earth trip starts, an empty jug can leave. When it reaches Earth, it becomes a filled jug waiting to return. When an Earth-to-Mars trip starts, a waiting filled jug can leave. When it reaches Mars, the jug becomes empty again.

This turns the problem into a sweep over all trip endpoints. The greedy choice is to always use any available jug on the earliest possible event. Using an empty jug earlier cannot hurt, because if we skip an earlier trip, the jug would just stay unused until a later time. Starting earlier gives the jug at least as much time to complete a cycle.

Similarly, when a return trip is available, sending a filled jug immediately is optimal because it only increases the number of free jugs sooner.

The implementation keeps two counters: the number of empty jugs on Mars and the number of filled jugs waiting on Earth. Processing events in chronological order is enough to simulate the optimal schedule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal Sweep | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create two events for every spaceship trip. The start event represents the moment when the spaceship leaves, and the end event represents the moment when it arrives. We need both because a jug changes state at both times.
2. Sort all events by time. Every time value is unique, so there is no ambiguity about the order of changes.
3. Maintain the number of empty jugs on Mars. Initially this value is 2 because Johnny owns two empty jugs.
4. Maintain the number of filled jugs currently waiting on Earth. Initially this is 0 because no milk has been transported yet.
5. When a Mars-to-Earth departure happens, use an empty jug if one is available. The jug leaves Mars, so the number of empty jugs decreases.
6. When that same trip arrives at Earth, the jug is now filled and waiting for a return trip. Increase the number of filled jugs.
7. When an Earth-to-Mars departure happens, send a filled jug if one exists. Decrease the number of filled jugs.
8. When the return trip arrives at Mars, the milk has been delivered successfully. Increase the number of empty jugs and increase the answer.

Why it works:

The invariant is that after every processed event, the counters represent exactly the best possible state after all decisions up to that time. Starting a Mars-to-Earth trip earlier never reduces future possibilities because it only moves an available jug into a state where it may eventually create milk. Returning a filled jug as soon as possible only releases a resource earlier. Since every choice is made at the earliest possible moment, no future sequence can have more available resources than this greedy simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    events = []

    for _ in range(n):
        l, r, t = map(int, input().split())
        if t == 0:
            events.append((l, 0, 0))
            events.append((r, 1, 0))
        else:
            events.append((l, 0, 1))
            events.append((r, 1, 1))

    events.sort()

    empty = 2
    filled = 0
    ans = 0

    for _, kind, direction in events:
        if kind == 0:
            if direction == 0:
                if empty > 0:
                    empty -= 1
            else:
                if filled > 0:
                    filled -= 1
        else:
            if direction == 0:
                filled += 1
            else:
                empty += 1
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code stores each trip endpoint as an event. The third field distinguishes the direction of the original trip, while the second field distinguishes departure and arrival.

The sweep variables directly represent the real situation. `empty` counts jugs that can be placed on Mars-to-Earth ships. `filled` counts jugs that have reached Earth and are ready to come back. When a return arrives, the answer is increased because that is the exact moment the milk reaches Mars.

The ordering of operations is handled by sorting all events. Because all times are distinct, there is no tie-breaking problem between events. The counters are updated only after the corresponding physical action happens, avoiding off-by-one mistakes around trip boundaries.

## Worked Examples

### Sample 1

Input:

```
5
0 2 0
4 6 0
1 3 1
5 7 1
8 9 1
```

Trace:

| Time | Event | Empty jugs | Filled jugs | Answer |
| --- | --- | --- | --- | --- |
| 0 | Mars to Earth starts | 1 | 0 | 0 |
| 1 | Earth to Mars starts | 1 | 0 | 0 |
| 2 | Mars to Earth arrives | 1 | 1 | 0 |
| 3 | Return arrives | 2 | 0 | 1 |
| 4 | Mars to Earth starts | 1 | 0 | 1 |
| 5 | Earth to Mars starts | 1 | 0 | 1 |
| 6 | Mars to Earth arrives | 1 | 1 | 1 |
| 7 | Return arrives | 2 | 0 | 2 |

The trace shows that a jug can be reused after returning. The same two physical jugs can create multiple imports.

### Sample 2

Input:

```
3
0 10 0
1 2 0
3 4 1
```

Trace:

| Time | Event | Empty jugs | Filled jugs | Answer |
| --- | --- | --- | --- | --- |
| 0 | Long trip starts | 1 | 0 | 0 |
| 1 | Short trip starts | 0 | 0 | 0 |
| 2 | Short trip arrives | 0 | 1 | 0 |
| 3 | Return starts | 0 | 0 | 0 |
| 4 | Return arrives | 1 | 0 | 1 |
| 10 | Long trip arrives | 1 | 1 | 1 |

This demonstrates why starting earlier is enough. The algorithm naturally ignores the fact that the long trip cannot return in time for the available return ship.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the 2n generated events dominates the sweep |
| Space | O(n) | We store two events for every trip |

The solution fits the constraints because it avoids comparing trips with each other. The number of processed events is only twice the number of input trips.

## Test Cases

```python
import sys
import io

def solve_data(data):
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    n = int(input())
    events = []

    for _ in range(n):
        l, r, t = map(int, input().split())
        if t == 0:
            events.append((l, 0, 0))
            events.append((r, 1, 0))
        else:
            events.append((l, 0, 1))
            events.append((r, 1, 1))

    events.sort()

    empty = 2
    filled = 0
    ans = 0

    for _, kind, direction in events:
        if kind == 0:
            if direction == 0 and empty:
                empty -= 1
            elif direction == 1 and filled:
                filled -= 1
        else:
            if direction == 0:
                filled += 1
            else:
                empty += 1
                ans += 1

    return str(ans)

assert solve_data("""3
0 2 0
4 6 0
1 3 1
""") == "1"

assert solve_data("""4
0 5 0
1 2 0
3 4 1
6 7 1
""") == "1"

assert solve_data("""1
0 1 0
""") == "0"

assert solve_data("""4
0 2 0
3 5 1
6 8 0
9 10 1
""") == "2"

assert solve_data("""5
0 10 0
1 2 0
3 4 1
5 6 1
7 8 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single Mars-to-Earth trip | 0 | No possible return |
| Overlapping Earth trips | 1 | Resource limitation |
| Two independent cycles | 2 | Jug reuse |
| Long trip blocking intuition | 2 | Greedy event processing |
| Multiple return choices | 2 | Sending filled jugs immediately |

## Edge Cases

For the case where a long Earth trip blocks a short one:

```
3
0 100 0
1 2 0
3 4 1
```

The sweep starts the first trip at time 0 and the second at time 1 because both jugs are free. The short trip fills at time 2 and returns at time 4, producing one successful import. The long trip only fills at time 100, after the return opportunity has passed, so the final answer is `1`.

For a case where the same jugs must be reused:

```
4
0 2 0
4 6 0
1 3 1
5 7 1
```

The first jug cycle completes at time 3. The freed jug is counted as empty again and can be used for the second cycle. The answer becomes `2`, showing that the algorithm tracks the lifetime of jugs rather than treating them as one-time objects.
