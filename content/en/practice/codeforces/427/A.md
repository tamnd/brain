---
title: "CF 427A - Police Recruits"
description: "We are given a sequence of events happening in time order in a city. Each event is either the arrival of one or more new police recruits, or the occurrence of a crime. When recruits arrive, they increase the number of available officers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 427
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 244 (Div. 2)"
rating: 800
weight: 427
solve_time_s: 82
verified: true
draft: false
---

[CF 427A - Police Recruits](https://codeforces.com/problemset/problem/427/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of events happening in time order in a city. Each event is either the arrival of one or more new police recruits, or the occurrence of a crime. When recruits arrive, they increase the number of available officers. When a crime occurs, it consumes exactly one currently available officer if any exist; otherwise, that crime is not handled.

The task is to simulate this process and count how many crimes cannot be assigned to any officer at the moment they occur.

The input size can be as large as 100,000 events. This immediately suggests that any solution doing nested scanning or revisiting previous events would be too slow. A linear scan that maintains only the current number of available officers is sufficient and necessary, since each event must be processed in order and decisions depend only on the current state.

A brute-force idea that tries to match each crime with the earliest possible recruit or searches backward for available officers would degrade to quadratic behavior in worst cases where many crimes and recruits are interleaved. With 10^5 events, O(n^2) would be far beyond feasible limits.

A subtle edge case comes from consecutive crimes before any recruits appear. For example, if the input is `-1 -1 1`, the first two crimes happen with zero officers available, so both go untreated. The later recruit does not retroactively help.

Another edge case is when recruits arrive in bursts larger than needed, such as `5 5 -1 -1 -1`. Only three officers are consumed, and remaining officers persist for later events. A wrong greedy approach might incorrectly "reset" counts per event instead of maintaining a global pool.

## Approaches

The naive approach tries to explicitly assign officers to crimes one by one, possibly searching for an available recruit for each crime event by scanning earlier events or maintaining a list of individual officers. While logically correct, this leads to unnecessary overhead because each officer is identical and interchangeable. The only relevant state is how many officers are currently free.

If we simulate each officer individually, each recruit increases a list, and each crime removes one element from that list. In the worst case, we would be performing O(n) list operations per event due to shifting or searching, leading to O(n^2) behavior when all events are crimes or recruits.

The key observation is that we never need identity-level tracking of officers. We only need a counter representing available officers. Each recruit event adds to this counter, and each crime consumes it if possible, otherwise increments the untreated count. This reduces the problem to a single pass with constant-time updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (track individuals) | O(n^2) | O(n) | Too slow |
| Optimal (counter simulation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two integers: one for currently available officers, and one for untreated crimes.

We process events in order.

1. Initialize a variable `available` to 0. This represents how many officers are free at the current moment.
2. Initialize a variable `untreated` to 0. This tracks crimes that cannot be handled.
3. Read each event from left to right.
4. If the event value is positive, increase `available` by that amount because new recruits become immediately available.
5. If the event value is `-1`, we are processing a crime.
6. If `available` is greater than 0, decrease `available` by 1 since one officer handles this crime.
7. Otherwise, increase `untreated` by 1 because no officer is available at this moment.
8. After processing all events, output `untreated`.

The decision at each crime step is locally optimal because every officer is identical and there is no benefit to saving or choosing between officers.

### Why it works

At any prefix of the sequence, the value of `available` exactly represents how many crimes can still be served by past recruits. Since each officer can handle at most one crime and there is no expiration or ordering constraint beyond availability, the system behaves like a simple resource counter. Every time a crime appears, consuming one unit of this counter is always optimal if possible, and failing to do so increases the number of unavoidable losses exactly once per shortage.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
events = list(map(int, input().split()))

available = 0
untreated = 0

for x in events:
    if x == -1:
        if available > 0:
            available -= 1
        else:
            untreated += 1
    else:
        available += x

print(untreated)
```

The code directly follows the simulation strategy. The `available` variable is updated only by addition and subtraction, ensuring O(1) work per event. The order of checks matters: we must handle crimes before updating anything else for that event, since the event itself is either a crime or recruitment.

A common mistake is to store recruits in a list and pop from it. That is unnecessary and risks inefficiency. Another mistake is resetting `available` per event instead of accumulating it globally.

## Worked Examples

### Example 1

Input:

```
3
-1 -1 1
```

| Event | Type | Available | Untreated |
| --- | --- | --- | --- |
| -1 | crime | 0 | 1 |
| -1 | crime | 0 | 2 |
| 1 | recruit | 1 | 2 |

This trace shows that early crimes cannot benefit from later recruits. The state evolves strictly forward.

### Example 2

Input:

```
6
1 -1 1 -1 -1 2
```

| Event | Type | Available | Untreated |
| --- | --- | --- | --- |
| 1 | recruit | 1 | 0 |
| -1 | crime | 0 | 0 |
| 1 | recruit | 1 | 0 |
| -1 | crime | 0 | 0 |
| -1 | crime | 0 | 1 |
| 2 | recruit | 2 | 1 |

This example highlights that extra recruits accumulate and can be used for future crimes, but cannot fix past shortages.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event updates a constant number of variables |
| Space | O(1) | Only two counters are maintained regardless of input size |

The linear scan fits easily within the constraints of 100,000 events, and constant memory usage ensures no overhead from storing the event history.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    events = list(map(int, sys.stdin.readline().split()))

    available = 0
    untreated = 0

    for x in events:
        if x == -1:
            if available > 0:
                available -= 1
            else:
                untreated += 1
        else:
            available += x

    return str(untreated)

# provided samples
assert run("3\n-1 -1 1\n") == "2"

# all crimes, no recruits
assert run("4\n-1 -1 -1 -1\n") == "4"

# all recruits, no crimes
assert run("5\n1 2 3 4 5\n") == "0"

# alternating pattern
assert run("6\n1 -1 1 -1 -1 2\n") == "1"

# exact balance
assert run("4\n1 1 -1 -1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all -1 | 4 | no officers available ever |
| all positive | 0 | no crimes occur |
| alternating | 1 | interleaving correctness |
| balanced | 0 | proper consumption of recruits |

## Edge Cases

One important edge case is when crimes occur before any recruits exist. For input `-1 -1 -1`, the algorithm keeps `available = 0` throughout and increments `untreated` for every event. This matches the requirement that no retroactive assignment is possible.

Another edge case is when a large batch of recruits arrives after several crimes. For input `-1 -1 5`, the first two crimes increase `untreated` to 2. When 5 recruits arrive, `available` becomes 5, but it does not reduce the already counted failures. This behavior is correct because crimes are resolved immediately at their time of occurrence, and past failures cannot be repaired.

A final edge case is when recruits exactly match crimes later in the sequence, such as `2 -1 -1`. The first event sets `available = 2`. Each crime consumes one officer, reducing the counter to zero, and no crime is left untreated. This confirms that the counter correctly models one-to-one assignment.
