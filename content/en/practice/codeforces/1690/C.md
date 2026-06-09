---
title: "CF 1690C - Restoring the Duration of Tasks"
description: "We are given two increasing arrays. The array s contains the arrival time of each task. Task i becomes available at time s[i]. The array f contains the completion time of each task. Task i finishes exactly at time f[i]. Polycarp processes tasks in FIFO order."
date: "2026-06-09T23:20:25+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1690
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 797 (Div. 3)"
rating: 800
weight: 1690
solve_time_s: 352
verified: false
draft: false
---

[CF 1690C - Restoring the Duration of Tasks](https://codeforces.com/problemset/problem/1690/C)

**Rating:** 800  
**Tags:** data structures, greedy, implementation  
**Solve time:** 5m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two increasing arrays.

The array `s` contains the arrival time of each task. Task `i` becomes available at time `s[i]`.

The array `f` contains the completion time of each task. Task `i` finishes exactly at time `f[i]`.

Polycarp processes tasks in FIFO order. If he is busy when a task arrives, the task waits in the queue. If he finishes a task and the queue is non-empty, he immediately starts the next waiting task. If the queue is empty, he waits until another task arrives.

The unknown values are the actual execution durations `d[i]` of the tasks. We must reconstruct every duration.

The total number of tasks across all test cases is at most `2 · 10^5`. This immediately suggests that we need a linear or near-linear solution. Anything quadratic would require roughly `4 · 10^10` operations in the worst case, which is far beyond the time limit.

The tricky part is that a task does not necessarily start when it arrives. If previous tasks are still being processed, it must wait in the queue. A naive implementation that assumes

`duration = finish - arrival`

will often be wrong.

Consider:

```
s = [0, 3]
f = [10, 12]
```

The second task arrives at time `3`, but the first task finishes only at time `10`. The second task actually starts at time `10`, so its duration is

```
12 - 10 = 2
```

not

```
12 - 3 = 9
```

Another easy mistake is forgetting that the processor may become idle.

Example:

```
s = [0, 10]
f = [2, 15]
```

The first task finishes at time `2`. Nothing is waiting, so Polycarp sits idle until time `10`. The second task starts immediately at its arrival time and has duration

```
15 - 10 = 5
```

Using the previous finish time unconditionally would incorrectly produce

```
15 - 2 = 13
```

The solution must correctly distinguish between these two situations.

## Approaches

A direct simulation is possible.

For each task, we could explicitly determine when it starts. The start time is either its arrival time or the moment the previous task finishes, whichever is later. Once the start time is known, the duration is simply the completion time minus the start time.

This simulation is already efficient because tasks are processed strictly in order. We never need an actual queue structure or any search operation. The only information needed for task `i` is when task `i - 1` finished.

The key observation is that the start time of task `i` is completely determined by two values:

```
start[i] = max(s[i], f[i-1])
```

for `i > 0`.

If the previous task finishes before the new task arrives, Polycarp waits and starts at `s[i]`.

If the previous task finishes after the new task arrives, the task has been waiting in the queue and starts immediately at `f[i-1]`.

Once the start time is known,

```
d[i] = f[i] - start[i]
```

This gives a simple linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation with explicit queue tracking | O(n) | O(n) | Accepted |
| Optimal direct reconstruction | O(n) | O(1) extra | Accepted |

Although both are linear, the second approach is cleaner because it derives the start time directly instead of maintaining queue state.

## Algorithm Walkthrough

1. Read `n`, the arrival array `s`, and the completion array `f`.
2. For the first task, it starts immediately when it arrives.

```
start = s[0]
d[0] = f[0] - s[0]
```
3. For every task `i > 0`, compute its actual start time.

```
start = max(s[i], f[i-1])
```

If the processor was idle before task `i` arrived, the task starts at `s[i]`. Otherwise it was waiting in the queue and starts at the previous completion time.
4. Compute the duration.

```
d[i] = f[i] - start
```
5. Output all durations.

### Why it works

The completion times are strictly increasing, and tasks are completed in the same order they arrive. Because of that, task `i` cannot begin before task `i - 1` finishes.

There are only two possibilities.

If task `i` arrives after task `i - 1` has already finished, Polycarp is idle and starts immediately at `s[i]`.

If task `i` arrives before task `i - 1` finishes, it waits in the queue and starts exactly when task `i - 1` completes, namely at `f[i-1]`.

Thus the start time is always

```
max(s[i], f[i-1])
```

and the duration is the completion time minus this start time. Since every task's start time is reconstructed exactly, every duration is reconstructed exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    s = list(map(int, input().split()))
    f = list(map(int, input().split()))

    ans = [0] * n

    ans[0] = f[0] - s[0]

    for i in range(1, n):
        start = max(s[i], f[i - 1])
        ans[i] = f[i] - start

    print(*ans)
```

The first task is handled separately because there is no previous completion time.

For every later task, the only subtle point is computing the start time correctly. Using `max(s[i], f[i - 1])` captures both possible situations: waiting in the queue or starting immediately after arrival.

All values fit comfortably inside Python integers. The largest timestamps are only `10^9`, so overflow is not a concern.

The implementation stores only the answer array and performs one pass through the tasks.

## Worked Examples

### Example 1

Input:

```
s = [0, 3, 7]
f = [2, 10, 11]
```

| i | s[i] | f[i-1] | start | f[i] | duration |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | - | 0 | 2 | 2 |
| 1 | 3 | 2 | 3 | 10 | 7 |
| 2 | 7 | 10 | 10 | 11 | 1 |

Output:

```
2 7 1
```

The third task arrives at time `7` but cannot start until the second task finishes at time `10`. This demonstrates why arrival time alone is insufficient.

### Example 2

Input:

```
s = [10, 15]
f = [11, 16]
```

| i | s[i] | f[i-1] | start | f[i] | duration |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | - | 10 | 11 | 1 |
| 1 | 15 | 11 | 15 | 16 | 1 |

Output:

```
1 1
```

After finishing the first task at time `11`, Polycarp waits until time `15`. The second task starts immediately when it arrives.

This example exercises the idle-processor case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the tasks |
| Space | O(n) | Output array of size `n` |

The sum of all `n` values over the test cases is at most `2 · 10^5`, so the algorithm performs only a few hundred thousand operations. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = list(map(int, input().split()))
        f = list(map(int, input().split()))

        ans = [0] * n
        ans[0] = f[0] - s[0]

        for i in range(1, n):
            ans[i] = f[i] - max(s[i], f[i - 1])

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided sample
assert run(
"""4
3
0 3 7
2 10 11
2
10 15
11 16
9
12 16 90 195 1456 1569 3001 5237 19275
13 199 200 260 9100 10000 10914 91066 5735533
1
0
1000000000
"""
) == (
"""2 7 1
1 1
1 183 1 60 7644 900 914 80152 5644467
1000000000"""
)

# minimum size
assert run(
"""1
1
5
8
"""
) == "3"

# waiting in queue
assert run(
"""1
2
0 3
10 12
"""
) == "10 2"

# idle processor
assert run(
"""1
2
0 10
2 15
"""
) == "2 5"

# boundary transition
assert run(
"""1
3
0 5 6
5 8 20
"""
) == "5 3 12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `3` | Single-task boundary case |
| `s=[0,3], f=[10,12]` | `10 2` | Task waits in queue |
| `s=[0,10], f=[2,15]` | `2 5` | Processor becomes idle |
| `s=[0,5,6], f=[5,8,20]` | `5 3 12` | Exact transition between idle and queued states |

## Edge Cases

### Task arrives while previous task is still running

Input:

```
1
2
0 3
10 12
```

For the second task:

```
start = max(3, 10) = 10
duration = 12 - 10 = 2
```

Output:

```
10 2
```

A solution using `f[i] - s[i]` would incorrectly return `10 9`.

### Processor becomes idle

Input:

```
1
2
0 10
2 15
```

For the second task:

```
start = max(10, 2) = 10
duration = 15 - 10 = 5
```

Output:

```
2 5
```

The algorithm correctly ignores the old completion time once the machine has become idle.

### Single task

Input:

```
1
1
100
150
```

The first task starts immediately:

```
duration = 150 - 100 = 50
```

Output:

```
50
```

Handling the first task separately avoids accessing a nonexistent previous completion time.

### Arrival exactly after previous completion

Input:

```
1
2
0 5
5 9
```

For the second task:

```
start = max(5, 5) = 5
duration = 9 - 5 = 4
```

Output:

```
5 4
```

The formula naturally handles equality without any special case.
