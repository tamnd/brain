---
title: "CF 102569M - Notifications"
description: "Each notification arrives at a specific moment and contains a video with a given duration. Vasya always watches videos in the order their notifications arrive. If he is idle when a notification appears, he immediately starts watching that video."
date: "2026-08-01T06:03:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "M"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 70
verified: true
draft: false
---

[CF 102569M - Notifications](https://codeforces.com/problemset/problem/102569/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Each notification arrives at a specific moment and contains a video with a given duration. Vasya always watches videos in the order their notifications arrive. If he is idle when a notification appears, he immediately starts watching that video. If he is already watching something, the new video waits in the queue until every earlier unfinished video has been watched.

The input already gives notifications in non-decreasing order of arrival time, so we never need to reorder them. The task is simply to determine the finishing time of the final video after processing every notification.

The number of notifications reaches 200000, while both arrival times and durations can be as large as (10^9). Any algorithm that repeatedly simulates time or scans previously processed notifications for every new notification would perform too many operations. A linear solution is easily fast enough, while quadratic approaches are ruled out. Since finish times may exceed (2 \times 10^9), the algorithm must also avoid assumptions that values fit into 32-bit integers, although Python integers naturally handle this.

One easy mistake is forgetting that Vasya can become idle before the next notification arrives.

Example:

```
2
1 2
10 3
```

The correct answer is `13`. Vasya finishes the first video at time `3`, waits until time `10`, then watches the second video until `13`. Simply adding durations to the previous finish time would incorrectly produce `6`.

Another subtle case occurs when several notifications arrive at exactly the same moment.

```
3
5 2
5 4
5 1
```

The correct answer is `12`. The first video starts immediately at time `5`, and the other two are appended behind it in arrival order. Treating notifications with the same timestamp as simultaneous independent events would lose that ordering.

A third case is when a notification arrives exactly as the previous video finishes.

```
2
1 4
5 3
```

The correct answer is `8`. At time `5` Vasya is no longer busy, so the second video starts immediately. Using a strict comparison such as `finish > arrival` instead of `finish >= arrival` can shift the schedule incorrectly.

## Approaches

A straightforward simulation keeps every waiting video in a queue. Whenever a notification arrives, the simulation advances time, removes every completed video, then either starts the arriving video immediately or appends it to the queue. This faithfully models the rules, but in the worst case each arrival may process many queued videos again. With (n) notifications, this can require (O(n^2)) work, roughly (4 \times 10^{10}) operations when (n = 200000).

The queue itself is actually unnecessary. At any moment, the only information that affects future notifications is the time when Vasya will become free. Suppose that after processing some notifications, he is guaranteed to stay busy until time `finish`. When a new notification arrives at time `t`, only two situations are possible.

If `finish <= t`, Vasya is idle when the notification appears. The new video starts at `t` and finishes at `t + d`.

If `finish > t`, Vasya is still busy. The new video starts exactly at `finish` and ends at `finish + d`.

Both situations can be expressed with one formula:

```
finish = max(finish, t) + d
```

This single variable completely captures the state of the entire watching queue, allowing every notification to be processed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `finish = 0`. Before any notifications arrive, Vasya is idle.
2. Read notifications one by one in their given order. The input is already sorted by arrival time, so no preprocessing is needed.
3. For each notification with arrival time `t` and duration `d`, compute `start = max(finish, t)`. If Vasya is still busy, the video waits until `finish`. Otherwise it starts immediately at `t`.
4. Update `finish = start + d`. This becomes the earliest moment when every processed notification has been completely watched.
5. After all notifications have been processed, output `finish`.

### Why it works

The key invariant is that after processing the first `i` notifications, `finish` equals the exact time when all of those videos have been watched. When the next notification arrives, no earlier video can start later than `finish`, because every previous notification has already been scheduled. If Vasya is idle, the new video begins immediately. If he is busy, every earlier video must finish before the new one can begin, so the earliest possible start is exactly `finish`. Updating `finish` with `max(finish, t) + d` preserves the invariant, and after the last notification it represents the completion time of the final video.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    finish = 0

    for _ in range(n):
        t, d = map(int, input().split())
        finish = max(finish, t) + d

    print(finish)

if __name__ == "__main__":
    solve()
```

The solution keeps only one variable, `finish`, which represents the end of the current schedule. Every notification updates this value using the formula derived in the algorithm.

The expression `max(finish, t)` handles both possible states without branching. If Vasya is already busy, the current schedule continues uninterrupted. If he has already finished everything, the schedule restarts from the notification's arrival time.

The comparison uses `max` rather than a strict inequality, which correctly handles notifications arriving exactly when the previous video finishes. Python integers automatically grow as needed, so even very large finish times remain safe.

## Worked Examples

### Example 1

Input:

```
5
1 4
3 3
6 1
10 2
10 3
```

| Notification | Arrival | Duration | Previous finish | Start | New finish |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 0 | 1 | 5 |
| 2 | 3 | 3 | 5 | 5 | 8 |
| 3 | 6 | 1 | 8 | 8 | 9 |
| 4 | 10 | 2 | 9 | 10 | 12 |
| 5 | 10 | 3 | 12 | 12 | 15 |

The schedule becomes empty after the third video, so the fourth starts immediately at time `10`. The fifth notification arrives while the fourth is playing, so it waits until time `12`.

### Example 2

Input:

```
3
5 2
5 4
5 1
```

| Notification | Arrival | Duration | Previous finish | Start | New finish |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 0 | 5 | 7 |
| 2 | 5 | 4 | 7 | 7 | 11 |
| 3 | 5 | 1 | 11 | 11 | 12 |

Every notification arrives together, but they are still processed in input order. The running finish time naturally preserves that ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every notification is processed exactly once. |
| Space | O(1) | Only the current finish time is stored. |

Processing 200000 notifications with constant work per notification easily fits within the time limit, and the constant memory usage is far below the available memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    finish = 0
    for _ in range(n):
        t, d = map(int, input().split())
        finish = max(finish, t) + d
    print(finish)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

assert run("5\n1 4\n3 3\n6 1\n10 2\n10 3\n") == "15", "sample 1"

assert run("1\n7 5\n") == "12", "single notification"

assert run("2\n1 2\n10 3\n") == "13", "idle period"

assert run("3\n5 2\n5 4\n5 1\n") == "12", "same arrival time"

assert run("2\n1 4\n5 3\n") == "8", "arrival at finish"

assert run("3\n1 1000000000\n1 1000000000\n1 1000000000\n") == "3000000001", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One notification | 12 | Minimum valid input |
| Idle gap | 13 | Schedule restarts after becoming idle |
| Equal arrival times | 12 | Input order is preserved |
| Arrival at finish | 8 | Boundary where a video ends exactly at notification time |
| Large durations | 3000000001 | Correct handling of very large finish times |

## Edge Cases

Consider an idle gap:

```
2
1 2
10 3
```

The algorithm starts with `finish = 0`. After the first notification, `finish = max(0, 1) + 2 = 3`. For the second notification, `finish = max(3, 10) + 3 = 13`. The schedule correctly restarts at time `10` instead of continuing from time `3`.

Now consider multiple notifications with the same timestamp.

```
3
5 2
5 4
5 1
```

The updates are `7`, then `11`, then `12`. Every notification is processed in input order because each new start time depends on the finish time produced by earlier notifications.

Finally, consider a notification arriving exactly when the previous video ends.

```
2
1 4
5 3
```

After the first notification, `finish = 5`. The second update becomes `max(5, 5) + 3 = 8`. Since `finish` and the arrival time are equal, the new video begins immediately without any unnecessary waiting, matching the required behavior.
