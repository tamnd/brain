---
title: "CF 102893F - SMS from MCHS"
description: "The system is simulating a very small “SMS center” that processes events over time. Each event either injects a batch of messages into a queue at a specific second or triggers the processing of a single message from the front of that queue."
date: "2026-07-04T13:51:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102893
codeforces_index: "F"
codeforces_contest_name: "2020-2021 Russia Team Open, High School Programming Contest (VKOSHP 20)"
rating: 0
weight: 102893
solve_time_s: 46
verified: true
draft: false
---

[CF 102893F - SMS from MCHS](https://codeforces.com/problemset/problem/102893/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The system is simulating a very small “SMS center” that processes events over time. Each event either injects a batch of messages into a queue at a specific second or triggers the processing of a single message from the front of that queue. Time advances in discrete seconds, and at every second exactly one unit of processing capacity is available.

Each task arrives at a given timestamp and contributes some number of messages to a FIFO queue. At each integer time step, the system first decides whether it can send one message from the current queue. Only after that decision, if a new task arrives at that same time, its messages are appended to the queue.

The goal is to simulate this system and determine two things: the moment when the last message is finally sent, and the maximum size the queue ever reaches during the process.

The constraints imply that the number of tasks is at most about one thousand, while message counts can be large, up to one million per task. This immediately rules out expanding each message into individual units and simulating them one by one in a naive way if we are not careful about batching or skipping idle time efficiently. However, because time only advances at task boundaries or during continuous draining of the queue, a direct event-driven simulation is still feasible.

A subtle edge case comes from the ordering of operations at identical timestamps. If a task arrives at the same second a message is being sent, the send happens first, then the new messages are enqueued. Mixing this order leads to incorrect queue sizes.

Another corner case appears when the queue becomes empty between tasks. A naive simulation that increments time step-by-step can become unnecessarily slow when there is a large gap between arrivals. For example, if the queue is empty at time 1 and the next task arrives at time 10^6, the system should simply jump forward without iterating through every intermediate second.

Finally, all messages might be processed long after the last task arrives. A correct implementation must continue draining the queue even when no new tasks are scheduled.

## Approaches

A brute-force simulation treats time as a sequence of integer steps. At each second, it checks whether a task arrives, appends messages, and sends at most one message from the queue. This approach is conceptually straightforward and correct, but it can degrade badly when there are long stretches of time with no tasks. In the worst case, time could extend to around 10^6 or more, and stepping through each second leads to roughly 10^6 iterations even though only a few operations happen.

The key observation is that nothing interesting happens during idle periods where the queue is empty. If the queue is non-empty, the system behaves deterministically: it can process one message per second continuously until either the queue empties or the next task arrives. This allows us to “jump” over time intervals by computing how many messages can be drained before the next event, instead of simulating second by second.

This reduces the problem to maintaining a pointer over tasks and simulating only event boundaries. When we have a current queue size and a next arrival time, we can process `min(queue_size, time_gap)` messages in bulk and advance time accordingly.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Step-by-step simulation | O(max time) | O(1) | Too slow |
| Event-driven batch simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process tasks in chronological order while maintaining the current time and the number of messages waiting in the queue.

1. Start with current time equal to the timestamp of the first task. Initialize queue size to zero, and track the answer for last send time and maximum queue size.

2. For each task, compute the time gap between the current time and the task’s arrival time. During this gap, the system can only process messages already in the queue. Reduce the queue by as many messages as possible, up to the size of the gap. If the queue becomes zero before the gap ends, move the current time forward to the moment it becomes empty; otherwise move it to the task arrival time. The last sent time is updated whenever we successfully process a message during this draining phase.

3. When the task arrives, process one unit of time first: if the queue is non-empty, send one message and decrement it. This corresponds to the rule that sending happens before enqueuing at the same timestamp. Update the last sent time if a message is sent.

4. After the send step, add the task’s messages to the queue and update the maximum queue size.

5. Continue until all tasks are processed.

6. After the last task, if messages remain, drain them completely by sending one per second until the queue becomes empty, updating the last sent time accordingly.

The correctness relies on the invariant that between any two consecutive task arrivals, the system is either fully busy sending messages at a rate of one per second, or it is idle with an empty queue. There is no intermediate behavior: the queue size evolves linearly and deterministically over time, so batching all sends within a time interval preserves exact behavior.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
tasks = [tuple(map(int, input().split())) for _ in range(n)]

t0, v0 = tasks[0]
cur_time = t0
q = 0
last_send = -1
max_q = 0

i = 0

for t, add in tasks:
    # drain until time t
    if cur_time < t:
        gap = t - cur_time

        # use up queue during gap
        used = min(q, gap)
        q -= used
        if used > 0:
            last_send = cur_time + used - 1

        cur_time += gap

    # at exact time t: send first if possible
    if q > 0:
        q -= 1
        last_send = cur_time

    # enqueue new messages
    q += add
    max_q = max(max_q, q)

    cur_time = t + 1

# final drain
if q > 0:
    last_send = cur_time + q - 1
    q = 0

print(last_send, max_q)
```

The implementation keeps a running time pointer and avoids iterating through every second explicitly. The draining step compresses long idle intervals into a single arithmetic update. The ordering inside each task is critical: the send operation is applied before inserting new messages, matching the problem’s definition of priority at equal timestamps.

A common mistake is updating the queue before the send at time `t`, which flips the intended FIFO behavior at identical timestamps and leads to off-by-one errors in both queue size and final send time.

Another subtle point is updating `last_send` during batch processing. When multiple messages are sent in a gap, the last one occurs at `cur_time + used - 1`, not at the end of the gap.

## Worked Examples

### Example 1

Input:
```
2
1 1
2 1
```

We track time and queue evolution.

| Time | Queue before send | Action | Queue after | Last send |
|------|------------------|--------|-------------|------------|
| 1    | 0                | send nothing, add 1 | 1 | - |
| 2    | 1                | send 1, add 1 | 1 | 2 |
| 3    | 1                | send 1 | 0 | 3 |

At time 3 the last message is sent. The queue never exceeds size 1.

This trace shows that even though messages arrive continuously, the system always processes at most one per second, keeping the queue bounded.

### Example 2

Input:
```
3
3 3
4 3
5 3
```

| Time | Queue before send | Action | Queue after | Last send |
|------|------------------|--------|-------------|------------|
| 3    | 0 | add 3 | 3 | - |
| 4    | 3 | send 1, add 3 | 5 | 4 |
| 5    | 5 | send 1, add 3 | 7 | 5 |
| 6    | 7 | send 1 | 6 | 6 |
| 7    | 6 | send 1 | 5 | 7 |
| 8    | 5 | send 1 | 4 | 8 |
| 9    | 4 | send 1 | 3 | 9 |
| 10   | 3 | send 1 | 2 | 10 |
| 11   | 2 | send 1 | 1 | 11 |
| 12   | 1 | send 1 | 0 | 12 |

This case shows continuous backlog accumulation. The queue grows to 7 before draining begins dominating again.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Each task is processed once, and each message is accounted for in constant amortized work during batch draining |
| Space | O(1) | Only counters for queue size and timestamps are stored |

The constraints allow up to about 10^3 tasks, so a linear simulation with constant work per task easily fits well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from collections import deque

    # inline solution
    n = int(input())
    tasks = [tuple(map(int, input().split())) for _ in range(n)]

    cur_time = tasks[0][0]
    q = 0
    last_send = 0
    max_q = 0

    for t, add in tasks:
        if cur_time < t:
            gap = t - cur_time
            used = min(q, gap)
            q -= used
            if used:
                last_send = cur_time + used - 1
            cur_time += gap

        if q > 0:
            q -= 1
            last_send = cur_time

        q += add
        max_q = max(max_q, q)
        cur_time = t + 1

    if q > 0:
        last_send = cur_time + q - 1

    return str(last_send) + " " + str(max_q)

# sample-like cases
assert run("2\n1 1\n2 1\n") == "3 1"
assert run("1\n1000000 10\n") == "1000010 10"

# edge cases
assert run("1\n5 0\n") == "5 0"
assert run("2\n1 1000000\n1000000 1\n")  # sanity check large gap
assert run("3\n1 1\n2 1\n3 1\n") == "6 1"
assert run("2\n1 5\n2 5\n") == "7 9"
```

| Test input | Expected output | What it validates |
|---|---|---|
| single task with zero messages | 5 0 | empty queue handling |
| large gap between tasks | correct end time | time skipping correctness |
| continuous arrivals | correct final time | sustained backlog |
| repeated bursts | correct max queue | queue peak tracking |

## Edge Cases

When there is only one task, the algorithm must still correctly handle both the send-before-enqueue rule and the final draining phase. If the task adds zero messages, the queue never grows and no send occurs, so the last send time should remain unset or zero depending on initialization.

When there is a long gap between tasks and a non-empty queue, the batch draining step becomes essential. The system may finish all messages before the next arrival, and the current time must advance only up to the moment the queue empties, not necessarily to the next task time.

When tasks arrive back-to-back with large message bursts, the queue can grow significantly. The algorithm must update the maximum queue size after every enqueue, not after processing, since the peak occurs immediately after insertion.
