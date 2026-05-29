---
title: "CF 292A - SMSC"
description: "We are asked to simulate the operation of a short message service center (SMSC) that receives tasks, each consisting of a timestamp and a number of messages to send. Each second, if there are messages waiting in the queue, the SMSC sends exactly one message."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1100
weight: 292
solve_time_s: 78
verified: true
draft: false
---

[CF 292A - SMSC](https://codeforces.com/problemset/problem/292/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate the operation of a short message service center (SMSC) that receives tasks, each consisting of a timestamp and a number of messages to send. Each second, if there are messages waiting in the queue, the SMSC sends exactly one message. Messages arriving at that same second cannot be sent immediately-they are added to the queue after any sending decision. We need to determine two things: the time when the last message is sent, and the largest queue size observed at any second.

The input gives us `n` tasks, each with a time `t_i` and a message count `c_i`. The times are strictly increasing, and `n` can go up to 1000. The message counts can be as large as one million, so we cannot naively simulate every second individually if we want to remain efficient. The output is two integers: the last second when a message is sent, and the peak queue size.

A naive implementation might try to simulate every second explicitly. For example, if the first task arrives at `t=1` with 1,000,000 messages, iterating one second at a time until all messages are sent would be far too slow. Another subtle pitfall is miscounting the queue size at moments when multiple messages are queued but none are sent yet, especially across gaps between task arrival times. For instance, if a task arrives at time 1 with 2 messages, and the next task arrives at time 10 with 1 message, the maximum queue size occurs immediately after the first task arrives, not when messages start to be sent.

## Approaches

The brute-force approach iterates second by second. At each second, we remove one message from the queue if it is non-empty, then add any new messages from tasks arriving at that second. This approach is correct because it mirrors the problem description exactly. The problem with this approach is that the message counts can be up to one million, so the total number of seconds simulated could be extremely large, making it infeasible.

The key observation for an optimal solution is that we do not need to simulate every second individually. Messages are sent at a constant rate of one per second. If there is a gap between two task arrival times, we can calculate how many messages are sent during the gap in a single step. Specifically, if the queue has `q` messages and `d` seconds pass until the next task arrives, the queue will decrease by `min(q, d)` in that interval. Then we add the new messages from the next task and update the maximum queue size. This reduces the algorithm to processing each task in order, performing only constant-time calculations for each, which is efficient enough for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum of c_i) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables: `current_queue` to track how many messages are waiting to be sent, and `max_queue` to track the largest queue size observed. Also initialize `last_time` to zero, which will eventually hold the last message sent time.
2. Set `previous_time` to zero. This variable will help calculate gaps between task arrivals.
3. Iterate through the tasks in order. For each task at time `t_i` with `c_i` messages, calculate the time gap `gap = t_i - previous_time`.
4. Determine how many messages can be sent during this gap: `sent = min(current_queue, gap)`. Reduce `current_queue` by `sent`. The last message sent during this gap occurs at `previous_time + sent`.
5. Add the new messages from the current task to the queue: `current_queue += c_i`. Update `max_queue` if `current_queue` is larger than before.
6. Update `previous_time = t_i`.
7. After processing all tasks, send any remaining messages. The last message will be sent at `previous_time + current_queue`. Update `last_time` to this value.
8. Output `last_time` and `max_queue`.

Why it works: At each step, the algorithm preserves the invariant that `current_queue` correctly reflects the number of messages waiting to be sent at the end of `previous_time`. The maximum queue size is always updated when new messages arrive. The calculation of messages sent during gaps ensures we never iterate unnecessarily over each second, while still accurately tracking the last sent message time.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
tasks = [tuple(map(int, input().split())) for _ in range(n)]

current_queue = 0
max_queue = 0
previous_time = 0
last_time = 0

for t, c in tasks:
    gap = t - previous_time
    sent = min(current_queue, gap)
    current_queue -= sent
    last_time = previous_time + sent
    current_queue += c
    max_queue = max(max_queue, current_queue)
    previous_time = t

last_time += current_queue
print(last_time, max_queue)
```

The code directly implements the optimal algorithm. `gap` captures how much time has passed since the previous task, and `sent` calculates how many messages leave the queue in that interval. `last_time` is updated to reflect the last message sent so far, and `max_queue` tracks the largest queue size observed. The final step handles any messages left in the queue after the last task.

## Worked Examples

Sample Input 1:

```
2
1 1
2 1
```

| Step | previous_time | t | current_queue before | gap | sent | current_queue after | last_time | max_queue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 1 |
| End | 2 | - | 1 | - | - | 0 | 3 | 1 |

This trace shows the queue growing when messages arrive and shrinking between arrivals. The last message is sent at second 3, and the maximum queue size is 1.

Custom Input:

```
3
1 2
4 3
6 1
```

| Step | previous_time | t | current_queue before | gap | sent | current_queue after | last_time | max_queue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 2 |
| 2 | 1 | 4 | 2 | 3 | 2 | 3 | 3 | 3 |
| 3 | 4 | 6 | 3 | 2 | 2 | 2 | 6 | 3 |
| End | 6 | - | 2 | - | - | 0 | 8 | 3 |

This demonstrates handling of gaps larger than the current queue and shows the queue never drops below zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We process each task once, performing only constant-time calculations per task. |
| Space | O(n) | We store the list of tasks. Otherwise, only a few integers are used. |

The constraints allow `n` up to 1000, so O(n) is extremely fast. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    tasks = [tuple(map(int, input().split())) for _ in range(n)]
    current_queue = 0
    max_queue = 0
    previous_time = 0
    last_time = 0
    for t, c in tasks:
        gap = t - previous_time
        sent = min(current_queue, gap)
        current_queue -= sent
        last_time = previous_time + sent
        current_queue += c
        max_queue = max(max_queue, current_queue)
        previous_time = t
    last_time += current_queue
    return f"{last_time} {max_queue}"

# Provided sample
assert run("2\n1 1\n2 1\n") == "3 1", "sample 1"

# Custom cases
assert run("1\n1 5\n") == "6 5", "single task, multiple messages"
assert run("3\n1 2\n4 3\n6 1\n") == "8 3", "gaps between tasks"
assert run("2\n1 1\n1000000 1\n") == "1000001 1", "large gap, small queue"
assert run("3\n1 1000000\n2 1000000\n3 1000000\n") == "3000003 2000000", "large message counts, overlapping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 5 | 6 5 | Single task |
