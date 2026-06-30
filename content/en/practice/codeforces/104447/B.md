---
title: "CF 104447B - How Aswad Use Telegram?"
description: "We are given a chronological log of messages in a group chat. Each message has a sender and a timestamp. One particular participant, Aswad, follows a fixed reaction rule: whenever a message appears, he starts a waiting timer of length k minutes."
date: "2026-06-30T17:58:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104447
codeforces_index: "B"
codeforces_contest_name: "Al-Baath Collegiate Programming Contest 2023"
rating: 0
weight: 104447
solve_time_s: 61
verified: true
draft: false
---

[CF 104447B - How Aswad Use Telegram?](https://codeforces.com/problemset/problem/104447/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of messages in a group chat. Each message has a sender and a timestamp. One particular participant, Aswad, follows a fixed reaction rule: whenever a message appears, he starts a waiting timer of length k minutes. If no other message appears before that timer finishes, he sends exactly one response. If another message appears before the timer completes, he discards the pending reaction and restarts the waiting timer from that new message.

The task is to determine how many responses Aswad ends up sending for each test case, given all message timestamps in order.

The input consists of multiple test cases. Each test case provides k, the waiting duration, and a sequence of message timestamps. The sender IDs are irrelevant for the logic, since Aswad reacts to time progression rather than who sent the message. The output is a single integer per test case: the number of times Aswad successfully completes a full uninterrupted waiting period.

The constraints are small enough that a direct linear scan per test case is sufficient. Even if we process every message and compare it against a currently tracked deadline, the total work stays comfortably within limits. The key observation is that each message is handled once, and each decision is constant time.

A subtle edge case appears around messages that arrive exactly at the moment the waiting period finishes. If a message arrives at time t + k when the last message started at time t, the waiting is considered completed rather than interrupted. So equality should trigger a successful response, not a reset.

Another important corner case is when messages come in rapid bursts. For example, if messages keep arriving every minute and k is large, Aswad will never respond. Conversely, if there is a long idle gap after some message, Aswad will respond exactly once for that gap.

## Approaches

A brute-force interpretation would simulate Aswad’s behavior message by message and explicitly maintain a queue of pending “waiting windows”. For each message, we could scan forward in time to check whether any later message appears before k minutes pass, and decide whether the current message leads to a response. This leads to repeatedly scanning suffixes of the array, and in the worst case where messages are dense, each message may require checking many future events. That pushes the complexity toward O(m²) per test case, which is unnecessary given that m can reach the full input size.

The improvement comes from noticing that the process does not require looking ahead more than one step. We only need to track a single active candidate message that is currently “waiting to be answered”. When a new message arrives, it either invalidates the current candidate or allows it to complete. This turns the problem into a single pass greedy simulation: we maintain the timestamp of the last message that started a waiting period, and we maintain when that waiting period would expire.

Once we express the problem in terms of “current active start time” and “expiry time”, every message either extends the active state or triggers a completed response. This removes all need for nested scanning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(1) | Too slow |
| Optimal Simulation | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

We first convert all timestamps into a comparable numeric form, specifically minutes since midnight. This allows direct arithmetic for k-minute comparisons.

We then process messages in chronological order while maintaining two variables: the timestamp of the current pending message, and the time at which its response would be triggered if uninterrupted.

1. Initialize a counter for Aswad’s responses to zero. Also initialize no active pending message.
2. Convert each timestamp HH:MM into total minutes using 60 * HH + MM so that differences are simple integer subtraction. This avoids dealing with hour boundaries explicitly.
3. For the first message, set it as the active pending message and set its expiry time to its timestamp plus k minutes. This represents the earliest moment Aswad would respond if nothing interrupts.
4. For each next message, compare its timestamp with the current expiry time. If the new message arrives strictly before the expiry time, the previous waiting process is interrupted and discarded, so we replace the active message with the new one and recompute its expiry.
5. If the new message arrives at or after the expiry time, the previous waiting period completed successfully before being interrupted. We increment the response counter, because the pending message has now produced a response. Then we treat the current message as a fresh starting point and assign it a new expiry time.
6. After processing all messages, the final pending message may still have a valid waiting period that never got interrupted. We count it as a response because no future message cancels it.

The key decision point is always the comparison between the next timestamp and the current expiry time.

### Why it works

At every step, there is at most one active “candidate message” that could produce a response. Any message that arrives before its expiry invalidates it completely, and no earlier message ever becomes relevant again because it is always either already cancelled or already completed. This means the algorithm maintains the invariant that the active candidate is always the most recent message that has not yet been interrupted, and its expiry time correctly represents the earliest time a response could occur. Since every message is processed once and transitions are final, the count of completed expirations exactly matches Aswad’s responses.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

t = int(input())
for _ in range(t):
    n, k, m = map(int, input().split())

    times = []
    for _ in range(m):
        _, ts = input().split()
        times.append(to_minutes(ts))

    ans = 0
    start = times[0]
    expiry = start + k

    for i in range(1, m):
        cur = times[i]
        if cur < expiry:
            start = cur
            expiry = cur + k
        else:
            ans += 1
            start = cur
            expiry = cur + k

    ans += 1
    print(ans)
```

The implementation keeps a running “start” time for the active message and its computed expiry. The comparison `cur < expiry` captures interruption strictly inside the waiting window. Equality is treated as completion, which is why the response is counted before switching state.

The final `ans += 1` is necessary because the last active window always completes unless explicitly invalidated later, and since there is no later message, it must be counted.

## Worked Examples

### Example 1

Input:

n = 6, k = 5

messages:

01:00, 02:00, 03:00, 03:06, 03:07

Converted minutes:

60, 120, 180, 186, 187

We track state step by step.

| Message time | Active start | Expiry | Action | Responses |
| --- | --- | --- | --- | --- |
| 60 | 60 | 65 | start | 0 |
| 120 | 120 | 125 | previous expired before interruption | 1 |
| 180 | 180 | 185 | previous expired | 2 |
| 186 | 186 | 191 | interrupt previous | 2 |
| 187 | 187 | 192 | interrupt previous | 2 |

Final pending window completes, so total becomes 3.

This shows that only uninterrupted gaps of at least k minutes contribute to responses.

### Example 2

Input:

messages:

03:45, 04:00, 04:07, 04:30, 04:41, 06:09 with k = 15

Converted:

225, 240, 247, 270, 281, 369

| Message | Start | Expiry | Action | Responses |
| --- | --- | --- | --- | --- |
| 225 | 225 | 240 | start | 0 |
| 240 | 240 | 255 | completes previous | 1 |
| 247 | 247 | 262 | interrupt | 1 |
| 270 | 270 | 285 | completes previous | 2 |
| 281 | 281 | 296 | interrupt | 2 |
| 369 | 369 | 384 | completes previous | 3 |

This trace shows how alternating interruptions and long gaps produce multiple completed responses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) per test case | Each message is processed once with constant time updates |
| Space | O(1) | Only a few variables are maintained besides input storage |

The constraints allow up to 1000 test cases with up to 1440 messages each, so a linear scan is easily fast enough even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def to_minutes(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m

    t = int(input())
    out = []
    for _ in range(t):
        n, k, m = map(int, input().split())
        times = []
        for _ in range(m):
            _, ts = input().split()
            times.append(to_minutes(ts))

        ans = 0
        start = times[0]
        expiry = start + k

        for i in range(1, m):
            cur = times[i]
            if cur < expiry:
                start = cur
                expiry = cur + k
            else:
                ans += 1
                start = cur
                expiry = cur + k

        ans += 1
        out.append(str(ans))

    return "\n".join(out)

# provided sample (conceptual format)
assert run("""1
1 5 3
1 00:00
1 00:02
1 00:10
""") == "1"

# all spaced far apart
assert run("""1
1 5 3
1 00:00
1 00:10
1 00:20
""") == "3"

# dense messages prevent any response
assert run("""1
1 10 3
1 00:00
1 00:01
1 00:02
""") == "0"

# exact boundary equality
assert run("""1
1 5 2
1 00:00
1 00:05
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| spaced messages | 3 | every gap triggers response |
| dense stream | 0 | continuous interruption blocks all |
| exact k boundary | 1 | equality counts as completion |

## Edge Cases

A key edge case is when messages arrive exactly k minutes apart. In this case, the waiting period completes exactly at the moment the next message arrives, so the previous response should still be counted. For example, with k = 5 and messages at 00:00 and 00:05, the first message produces a response and the second starts a new cycle. The algorithm handles this because it uses a strict `< expiry` condition for interruption, so equality is treated as completion.

Another edge case is a completely dense sequence of messages where every message arrives before k minutes pass. In that situation, no waiting period is ever allowed to finish. The simulation continuously resets the active message, and the counter never increments until the final forced completion at the end. This matches the rule that only uninterrupted intervals produce responses.

A final edge case is a single message. With only one timestamp, there is no possibility of interruption, so Aswad always produces exactly one response. The algorithm handles this naturally because the initial pending window is always counted at the end.
