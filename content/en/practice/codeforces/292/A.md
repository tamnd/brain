---
title: "CF 292A - SMSC"
description: "We are given a sequence of tasks that arrive at a corporation's SMS center. Each task consists of a time ti when it arrives and a number ci of text messages to send. The SMS center can send at most one message per second, and messages are queued in the order they arrive."
date: "2026-06-05T17:17:06+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1100
weight: 292
solve_time_s: 95
verified: true
draft: false
---

[CF 292A - SMSC](https://codeforces.com/problemset/problem/292/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of tasks that arrive at a corporation's SMS center. Each task consists of a time `t_i` when it arrives and a number `c_i` of text messages to send. The SMS center can send at most one message per second, and messages are queued in the order they arrive. At any second, the center first sends one message if the queue is non-empty, then adds any new messages arriving at that second to the tail of the queue.

The goal is to compute two quantities: the time when the last message is sent and the maximum number of messages in the queue at any time.

The constraints are small: `n` is at most 1000 and times `t_i` and counts `c_i` are up to 10^6. Since `n` is small, we can iterate over the tasks linearly without worrying about time, but we must carefully handle the queue behavior because naive per-second simulation up to `10^6` seconds would be too slow.

Non-obvious edge cases include tasks that arrive far apart in time, which creates idle periods where the queue may empty completely, and tasks that arrive with many messages at once, which can spike the maximum queue size. For example, if a task arrives at second 1 with 5 messages and the next task arrives at second 10 with 1 message, the queue empties by second 6, then at second 10 a new message arrives, so the last message is sent at second 10. A careless implementation might forget to account for these idle gaps.

## Approaches

A brute-force approach is to simulate the queue second by second from the first arrival to the time when all messages are sent. At each second, send a message if the queue is non-empty, then add messages arriving at that second. While correct, this would require iterating up to 10^6 seconds in the worst case, which is unnecessary and inefficient.

The key observation is that the SMS center always processes at most one message per second and we know the arrival times of all tasks. Therefore, we do not need to iterate every second explicitly. Instead, we can track the queue size and the current time, advancing the time intelligently to the next task if the queue is empty, or sending messages continuously until the next task arrives. This allows a linear sweep over the tasks while updating the queue and the maximum queue size without simulating idle seconds individually. The final last message time is simply the time after all messages have been sent, considering the remaining queue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (per-second simulation) | O(max(t_i + sum(c_i))) | O(1) | Too slow for large gaps between tasks |
| Optimal (task-based simulation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `queue = 0` to represent the number of messages waiting to be sent, `max_queue = 0` to track the maximum queue size, and `current_time = 0` to represent the last second we processed.
2. Iterate over the tasks in chronological order. For each task `(t, c)`, advance time to the arrival `t`. Compute how many seconds have passed since the last processed time: `delta = t - current_time`. During this interval, the SMS center will send `sent = min(queue, delta)` messages. Reduce `queue` by `sent` and increment `current_time` by `delta`.
3. Add the new messages `c` to `queue` after sending messages for the elapsed interval. Update `max_queue` as `max(max_queue, queue)` to account for the new messages. Set `current_time = t` because we have processed up to the task arrival.
4. After all tasks are processed, there may still be messages in the queue. The last message will be sent after `queue` seconds. Increment `current_time` by `queue` to get the final time when the last message is sent.
5. Return `current_time` as the time of the last message and `max_queue` as the maximum queue size observed.

The invariant maintained throughout the algorithm is that `queue` always represents the number of messages waiting to be sent immediately after processing the current time. This ensures the calculation of maximum queue size and last message time is accurate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
tasks = [tuple(map(int, input().split())) for _ in range(n)]

queue = 0
max_queue = 0
current_time = 0

for t, c in tasks:
    # Time passed since last task
    delta = t - current_time
    # Send as many messages as possible in that interval
    sent = min(queue, delta)
    queue -= sent
    current_time += delta
    # Add new messages
    queue += c
    max_queue = max(max_queue, queue)

# Process remaining messages
current_time += queue

print(current_time, max_queue)
```

This solution first reads all tasks, then simulates the queue efficiently by handling only task arrivals and leftover messages. The `delta` computation ensures that idle seconds are implicitly considered without iterating through them. Updating `max_queue` after adding messages correctly tracks the largest queue size.

## Worked Examples

Sample 1:

```
Input:
2
1 1
2 1
```

| Task | current_time | delta | queue before | sent | queue after | max_queue |
| --- | --- | --- | --- | --- | --- | --- |
| 1 1 | 0 | 1 | 0 | 0 | 1 | 1 |
| 2 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| End | 2 | - | 1 | - | 0 | 1 |

Final output: `3 1`

Constructed case:

```
Input:
3
1 2
4 3
6 1
```

| Task | current_time | delta | queue before | sent | queue after | max_queue |
| --- | --- | --- | --- | --- | --- | --- |
| 1 2 | 0 | 1 | 0 | 0 | 2 | 2 |
| 4 3 | 1 | 3 | 2 | 2 | 3 | 3 |
| 6 1 | 4 | 2 | 3 | 2 | 2 | 3 |
| End | 6 | - | 2 | - | 0 | 3 |

Final output: `8 3`

This trace shows how the algorithm handles idle gaps and overlapping message sending.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through each task once, performing only constant-time operations per task |
| Space | O(n) | We store the list of tasks |

With `n ≤ 1000`, this algorithm runs efficiently well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    queue = 0
    max_queue = 0
    current_time = 0
    n = int(input())
    tasks = [tuple(map(int, input().split())) for _ in range(n)]
    for t, c in tasks:
        delta = t - current_time
        sent = min(queue, delta)
        queue -= sent
        current_time += delta
        queue += c
        max_queue = max(max_queue, queue)
    current_time += queue
    return f"{current_time} {max_queue}"

# provided samples
assert run("2\n1 1\n2 1\n") == "3 1", "sample 1"

# minimum input
assert run("1\n1 1\n") == "2 1", "single task"

# multiple messages arriving before queue empties
assert run("3\n1 2\n2 2\n3 1\n") == "6 3", "messages overlap"

# large gap between tasks
assert run("2\n1 1\n10 2\n") == "12 2", "idle period"

# all tasks have 1 message, consecutive seconds
assert run("5\n1 1\n2 1\n3 1\n4 1\n5 1\n") == "6 1", "consecutive single messages"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 2 1 | Single task edge case |
| 3\n1 2\n2 2\n3 1 | 6 3 | Queue overlapping across arrivals |
| 2\n1 1\n10 2 | 12 2 | Large idle gap handling |
| 5\n1 1\n2 1\n3 1\n4 1\n5 1 | 6 1 | Consecutive arrivals, no queue growth |

## Edge Cases

If a task arrives long after the previous messages have been sent, the `delta` ensures that the queue empties completely before the new task is added. For input `2\n1 1\n10 2\n`, the queue is `1` after the first task. `delta = 10 - 0 = 10
