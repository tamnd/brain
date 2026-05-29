---
title: "CF 413B - Spyke Chatting"
description: "We are given a company where employees participate in several independent chat groups. Each chat has a fixed membership defined in advance. Over time, a log records messages: each event says that a particular employee posts in a particular chat."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 413
codeforces_index: "B"
codeforces_contest_name: "Coder-Strike 2014 - Round 2"
rating: 1300
weight: 413
solve_time_s: 108
verified: false
draft: false
---

[CF 413B - Spyke Chatting](https://codeforces.com/problemset/problem/413/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a company where employees participate in several independent chat groups. Each chat has a fixed membership defined in advance. Over time, a log records messages: each event says that a particular employee posts in a particular chat.

The key rule is simple but asymmetric: when someone sends a message in a chat, every other participant of that same chat receives exactly one notification. The sender does not receive a notification for their own message in that chat.

The task is to compute, for every employee, how many notifications they receive across all chats and all messages in the log.

The input structure describes a bipartite relationship between employees and chats using an n by m binary matrix, where m is very small (at most 10). Then follows a sequence of up to 200,000 message events. Each event is independent and contributes notifications to all other members of the relevant chat.

The constraints immediately suggest the important imbalance. The number of employees can be up to 20,000, but the number of chats is tiny. This asymmetry is what allows us to avoid simulating each message naively over all participants. A direct simulation per event would still work only if each chat were small or events were few, but here both can be large.

A naive implementation would, for each event, scan all n employees and check whether they belong to the chat, incrementing counters. This leads to 200,000 events times 20,000 employees, which is 4 billion checks in the worst case, clearly too slow.

A more subtle failure mode appears if one tries to precompute adjacency lists but still iterates per event over full chat membership without optimizing repeated work. That still degenerates to O(k · n) behavior.

Edge cases that break naive solutions include:

1. A single chat containing almost all employees, with many messages in it. Every event would require touching nearly all employees.
2. Many repeated messages in the same chat. Any per-event full scan repeats the same work unnecessarily.
3. Employees belonging to many chats (up to m = 10). A per-employee aggregation over chats per event still becomes heavy if done incorrectly.

## Approaches

The brute-force idea is straightforward. For each message event (x, y), we look at all employees i from 1 to n. If employee i is in chat y and i is not x, we increment their notification counter. This is correct because it directly simulates the definition of notification delivery.

However, each event costs O(n) time in this approach. With k up to 2·10^5 and n up to 2·10^4, this yields about 4·10^9 operations, which is far beyond limits.

The key observation is that we do not actually care about the sender’s identity during propagation, except to exclude them from receiving the notification. Instead of iterating over all participants per event, we can aggregate contributions per chat.

For each chat y, we maintain a total count of messages sent in it. Then, for any employee i who belongs to chat y, they receive one notification for every message in y, except those messages where i was the sender. That means we can separate the total messages in a chat from the number of times each employee was the sender in that chat.

So we maintain two pieces of information: total messages per chat, and per employee per chat how many messages they personally sent. Since m is at most 10, storing an n by m table is cheap enough.

Then the answer for each employee is the sum over all chats they belong to of (total_messages_in_chat − messages_sent_by_employee_in_that_chat).

This avoids iterating over all members per event and replaces it with O(1) updates per event.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per event scanning all employees | O(k · n) | O(1) | Too slow |
| Per-chat aggregation with counters | O(k + n·m) | O(n·m) | Accepted |

## Algorithm Walkthrough

We exploit the fact that chats are independent containers of messages and that notifications depend only on membership and message counts.

1. Read the membership matrix. For each employee i and chat y, we store whether i belongs to y. Since m ≤ 10, this is a compact boolean table.
2. Initialize an array total_chat of size m to store how many messages were sent in each chat.
3. Initialize an array sent[i][y] to store how many messages employee i personally sent in chat y.
4. Process each event (x, y). We increment total_chat[y]. We also increment sent[x][y]. This captures both the global activity in the chat and the sender’s contribution.
5. After processing all events, compute the answer for each employee i by iterating over all chats y. If employee i belongs to chat y, then add total_chat[y] − sent[i][y] to their answer.

The subtraction is crucial because total_chat[y] counts all messages, but an employee should not be notified of their own messages.

### Why it works

Fix any employee i and any chat y. Every message in chat y contributes exactly one notification to i unless i is the sender of that message. Over all messages in y, the total notifications received by i are therefore the total number of messages in y minus the number of messages i sent in y. Summing this independently across chats works because notifications from different chats are disjoint events and do not interact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    # membership[i][j] = 1 if employee i is in chat j
    membership = []
    for _ in range(n):
        membership.append(list(map(int, input().split())))

    total = [0] * m
    sent = [[0] * m for _ in range(n)]

    for _ in range(k):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        total[y] += 1
        sent[x][y] += 1

    ans = [0] * n

    for i in range(n):
        res = 0
        for j in range(m):
            if membership[i][j]:
                res += total[j] - sent[i][j]
        ans[i] = res

    print(*ans)

if __name__ == "__main__":
    solve()
```

The membership matrix is read directly into a list of lists so we can query chat participation in O(1). The `total` array tracks message volume per chat, while `sent` isolates how many of those messages belong to each employee.

The final accumulation step is where correctness emerges: for each chat an employee belongs to, we subtract their own contributions from the global count.

A subtle point is indexing. The input is 1-based, so both employee and chat indices are decremented immediately to avoid repeated off-by-one mistakes later.

## Worked Examples

### Example 1

Input:

```
3 4 5
1 1 1 1
1 0 1 1
1 1 0 0
1 1
3 1
1 3
2 4
3 2
```

We track total messages per chat and per employee contributions.

| Event | (x, y) | total[chat] | sent[x][chat] |
| --- | --- | --- | --- |
| 1 | (1,1) | [1,0,0,0] | sent[1][1]=1 |
| 2 | (3,1) | [2,0,0,0] | sent[3][1]=1 |
| 3 | (1,3) | [2,0,1,0] | sent[1][3]=1 |
| 4 | (2,4) | [2,0,1,1] | sent[2][4]=1 |
| 5 | (3,2) | [2,1,1,1] | sent[3][2]=1 |

Now compute per employee:

Employee 1: chats 1,2,3,4

Contribution = (2−1) + (1−0) + (1−1) + (1−0) = 1 + 1 + 0 + 1 = 3

Employee 2: chats 1,3,4

Contribution = (2−0) + (1−0) + (1−1) = 2 + 1 + 0 = 3

Employee 3: chats 1,2

Contribution = (2−1) + (1−1) = 1 + 0 = 1

Output matches:

```
3 3 1
```

This trace confirms that per-chat separation correctly avoids per-event expansion.

### Example 2

Consider a minimal case:

Input:

```
2 1 3
1
1
1 1
2 1
1 1
```

Here both employees are in a single chat.

| Event | total[1] | sent[1][1] | sent[2][1] |
| --- | --- | --- | --- |
| (1,1) | 1 | 1 | 0 |
| (2,1) | 2 | 1 | 1 |
| (1,1) | 3 | 2 | 1 |

Employee 1 receives (3−2)=1 notification, employee 2 receives (3−1)=2 notifications.

This highlights that repeated messages by the same sender only reduce their own received count, not others.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m + k + n·m) | Reading membership, processing events, final aggregation |
| Space | O(n·m) | Storage for membership and sent counters |

The solution is efficient because m is at most 10, so n·m is around 200,000 operations in the worst case, comparable to k. This fits comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    n, m, k = map(int, inp.splitlines()[0].split())
    membership = []
    idx = 1
    for _ in range(n):
        membership.append(list(map(int, inp.splitlines()[idx].split())))
        idx += 1

    total = [0] * m
    sent = [[0] * m for _ in range(n)]

    for line in inp.splitlines()[1+n:]:
        if not line.strip():
            continue
        x, y = map(int, line.split())
        total[y-1] += 1
        sent[x-1][y-1] += 1

    ans = [0] * n
    for i in range(n):
        res = 0
        for j in range(m):
            if membership[i][j]:
                res += total[j] - sent[i][j]
        ans[i] = res

    return " ".join(map(str, ans))

# provided sample
assert run("""3 4 5
1 1 1 1
1 0 1 1
1 1 0 0
1 1
3 1
1 3
2 4
3 2
""") == "3 3 1"

# single chat small
assert run("""2 1 3
1
1
1 1
2 1
1 1
""") == "1 2"

# minimum size
assert run("""2 1 1
1
1
1 1
""") == "0 1"

# all separate chats
assert run("""3 3 3
1 0 0
0 1 0
0 0 1
1 1
2 2
3 3
""") == "0 0 0"

# dense activity
assert run("""4 2 4
1 1
1 1
1 1
1 1
1 1
2 1
3 1
4 2
""") == "3 3 3 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single chat repeated sender | 1 2 | self-message exclusion handling |
| minimum size | 0 1 | base correctness |
| disjoint chats | 0 0 0 | independence across chats |
| dense activity | equal counts | large shared chat behavior |

## Edge Cases

A dense chat where almost every employee participates stresses the need to avoid per-event scanning. Suppose 20,000 employees all belong to one chat and there are 200,000 messages. A naive simulation would require 4 billion updates. The optimized method instead performs two increments per event and one final subtraction per employee.

Repeated self-posting is another subtle case. If one employee sends all messages in a chat, every other participant still receives all notifications, but that sender should receive zero. The formula total_chat − sent ensures this automatically: their sent count matches total, yielding zero contribution from that chat.

Sparse membership is handled naturally because the final loop only considers chats where membership is 1, so unnecessary subtraction is avoided.
