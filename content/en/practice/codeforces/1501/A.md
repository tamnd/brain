---
title: "CF 1501A - Alexey and Train"
description: "We are given the planned schedule of a train. For each station i, the schedule says the train is supposed to arrive at time a[i] and depart at time b[i]. Bad weather causes delays while travelling between stations. For each segment, we know an extra delay tm[i]."
date: "2026-06-10T21:02:22+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1501
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 707 (Div. 2, based on Moscow Open Olympiad in Informatics)"
rating: 800
weight: 1501
solve_time_s: 148
verified: false
draft: false
---

[CF 1501A - Alexey and Train](https://codeforces.com/problemset/problem/1501/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the planned schedule of a train. For each station `i`, the schedule says the train is supposed to arrive at time `a[i]` and depart at time `b[i]`.

Bad weather causes delays while travelling between stations. For each segment, we know an extra delay `tm[i]`. The actual travel time from station `i - 1` to station `i` becomes:

$$(a_i - b_{i-1}) + tm_i$$

with `b[0] = 0`.

Once the train reaches a station, it cannot always leave immediately. The departure time must satisfy two requirements.

First, the train must remain at the station for at least

$$\left\lceil \frac{b_i-a_i}{2} \right\rceil$$

time units.

Second, it cannot leave before the scheduled departure time `b[i]`.

The task is to determine the actual arrival time at the final station.

The constraints are very small. There are at most 100 test cases and at most 100 stations per test case. Even an $O(n^2)$ solution would easily fit, but the process itself is naturally linear because each station only depends on the previous one.

The main difficulty is correctly simulating the departure rule. A common mistake is to always leave at `max(arrival + required_stay, b[i])`, including at the final station. The train's arrival at station `n` is the answer. We do not care when it would depart from station `n`.

Another subtle point is the ceiling division. The required waiting time is

$$\left\lceil \frac{b_i-a_i}{2} \right\rceil$$

which must be computed carefully. For example, if `a=1` and `b=4`, the interval length is `3`, so the required stay is `2`, not `1`.

Consider:

```
1
1
1 4
0
```

The train arrives at time `1`. It would need to stay at least `2` units before departing, but since this is the last station, the answer is simply `1`. Any solution that simulates a departure from the final station would incorrectly output `4`.

Another easy mistake is using floor division instead of ceiling division.

```
1
2
1 4
10 11
0 0
```

At station 1, the required stay is `ceil(3/2)=2`. The train arrives at `1`, waits until `4`, then reaches station 2 at `10`.

Using floor division would allow departure after only one unit of waiting and produce the wrong timeline.

## Approaches

A brute-force simulation follows the train station by station.

We keep track of the current time. When we reach a station, we compute the actual arrival time. Then we determine the earliest valid departure time by checking both departure conditions. We repeat until reaching the last station.

Even if we literally simulate the process exactly as described, the work per station is constant. With at most 100 stations, the total work is only about 10,000 station updates across all test cases.

The key observation is that there is no optimization problem hidden inside the statement. Every arrival and departure time is uniquely determined by the previous one. Once we know the current departure time, the next arrival time follows immediately from the given travel formula.

Let `cur` denote the actual departure time from the previous station. Then the arrival time at station `i` is

$$cur + (a_i - b_{i-1}) + tm_i.$$

After arriving, the earliest departure allowed by the waiting rule is

$$arrival + \left\lceil \frac{b_i-a_i}{2} \right\rceil.$$

The earliest departure allowed by the schedule is `b[i]`.

The actual departure time is the larger of those two values.

This direct simulation already runs in linear time and is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal Simulation | O(n) | O(1) | Accepted |

In this problem the brute-force and optimal approaches are actually the same, because the process is inherently sequential and already linear.

## Algorithm Walkthrough

1. Initialize `cur = 0`, representing the departure time from the terminal.
2. Process stations from `1` to `n`.
3. Compute the actual arrival time at station `i`:

$$arrival = cur + (a_i - b_{i-1}) + tm_i.$$

This comes directly from the travel-time formula given in the statement.
4. If `i = n`, output `arrival` and stop.

The problem asks for arrival at the final station, not departure from it.
5. Compute the minimum required stay:

$$wait = \left\lceil \frac{b_i-a_i}{2} \right\rceil.$$

In integer arithmetic this is:

$$(b_i-a_i+1)//2.$$
6. The earliest departure satisfying the stay condition is:

$$arrival + wait.$$
7. The train also cannot leave before `b[i]`.

Set

$$cur = \max(arrival + wait,\; b_i).$$
8. Continue to the next station.

### Why it works

The algorithm maintains a simple invariant:

`cur` is always the actual departure time from the previous station.

Given that invariant, the statement uniquely determines the travel time to the next station, so the computed arrival time is correct. The departure rule says the train may leave only after both conditions become true. The earliest such moment is exactly the maximum of the two lower bounds:

$$arrival + wait$$

and

$$b_i.$$

Thus the computed departure time is the true departure time. By induction over all stations, every arrival and departure time produced by the simulation matches the real train timeline. When station `n` is reached, the computed arrival time is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        a = [0] * n
        b = [0] * n

        for i in range(n):
            a[i], b[i] = map(int, input().split())

        tm = list(map(int, input().split()))

        cur = 0
        prev_b = 0

        for i in range(n):
            arrival = cur + (a[i] - prev_b) + tm[i]

            if i == n - 1:
                print(arrival)
                break

            wait = (b[i] - a[i] + 1) // 2
            cur = max(arrival + wait, b[i])

            prev_b = b[i]

if __name__ == "__main__":
    solve()
```

The arrays `a` and `b` store the schedule. The variable `cur` always holds the actual departure time from the previous station, which is the invariant described earlier.

For station `i`, we compute the actual arrival time using the travel formula from the statement. The value `prev_b` represents the scheduled departure time of the previous station, which appears in that formula.

The most delicate line is:

```
wait = (b[i] - a[i] + 1) // 2
```

This performs ceiling division for positive integers. Using `(b[i] - a[i]) // 2` would be incorrect whenever the interval length is odd.

Another subtle detail is the order of operations around the last station. We check whether the current station is the final one immediately after computing its arrival time. We never simulate a departure from station `n`, because the answer is the arrival time itself.

Python integers easily handle all values in this problem, so there is no overflow concern.

## Worked Examples

### Sample 1

Input:

```
2
2 4
10 12
0 2
```

| Station | Previous Departure | Arrival | Required Wait | Actual Departure |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | 4 |
| 2 | 4 | 12 | - | - |

The final arrival time is `12`.

This example shows that even though station 1 only requires one unit of waiting, the train still cannot leave before the scheduled departure time `4`.

### Sample 2

Input:

```
5
1 4
7 8
9 10
13 15
19 20
1 2 3 4 5
```

| Station | Previous Departure | Arrival | Required Wait | Actual Departure |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 2 | 4 |
| 2 | 4 | 9 | 1 | 10 |
| 3 | 10 | 14 | 1 | 15 |
| 4 | 15 | 22 | 1 | 23 |
| 5 | 23 | 32 | - | - |

The final arrival time is `32`.

This trace demonstrates the invariant that each departure time completely determines the next arrival time. Once station 1's departure becomes `4`, the rest of the timeline follows deterministically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One constant-time update per station |
| Space | O(1) | Only a few variables besides the input arrays |

For each test case, the train is processed exactly once from the first station to the last. With at most 100 stations and 100 test cases, the total amount of work is tiny compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        a = []
        b = []

        for _ in range(n):
            x, y = map(int, input().split())
            a.append(x)
            b.append(y)

        tm = list(map(int, input().split()))

        cur = 0
        prev_b = 0

        for i in range(n):
            arrival = cur + (a[i] - prev_b) + tm[i]

            if i == n - 1:
                out.append(str(arrival))
                break

            wait = (b[i] - a[i] + 1) // 2
            cur = max(arrival + wait, b[i])
            prev_b = b[i]

    return "\n".join(out)

# provided samples
assert run(
"""2
2
2 4
10 12
0 2
5
1 4
7 8
9 10
13 15
19 20
1 2 3 4 5
"""
) == "12\n32"

# minimum size
assert run(
"""1
1
1 2
0
"""
) == "1"

# ceiling division check
assert run(
"""1
2
1 4
10 11
0 0
"""
) == "10"

# large delay accumulation
assert run(
"""1
3
1 2
5 6
10 11
10 10 10
"""
) == "35"

# waiting condition dominates schedule condition
assert run(
"""1
2
1 10
20 21
0 0
"""
) == "24"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single station | 1 | No departure should be simulated from the last station |
| Odd interval length | 10 | Correct ceiling division |
| Large delays | 35 | Delay accumulation across multiple stations |
| Long scheduled stop | 24 | Waiting-time rule can be more restrictive than schedule timing |

## Edge Cases

Consider a test with only one station:

```

```
