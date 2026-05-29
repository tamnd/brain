---
title: "CF 245F - Log Stream Analysis"
description: "We receive a chronologically ordered stream of warning logs. Every line contains a timestamp and a message. The message itself is irrelevant for the computation, only the timestamp matters."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "F"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 2000
weight: 245
solve_time_s: 104
verified: true
draft: false
---

[CF 245F - Log Stream Analysis](https://codeforces.com/problemset/problem/245/F)

**Rating:** 2000  
**Tags:** binary search, brute force, implementation, strings  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We receive a chronologically ordered stream of warning logs. Every line contains a timestamp and a message. The message itself is irrelevant for the computation, only the timestamp matters.

For every moment when a warning appears, we want to know how many warnings happened during the last `n` seconds, including the current warning. The task is to find the earliest moment when that count becomes at least `m`.

A warning at time `T` belongs to the current window if its timestamp is inside the interval `[T - n + 1, T]`. The timestamps are precise to the second, and multiple warnings may happen during the same second.

The total input size can reach 5 MB, so the number of log entries can easily be in the hundreds of thousands. Any algorithm that repeatedly scans earlier logs for every new log entry becomes too slow. A quadratic solution would perform on the order of `10^10` operations in the worst case, which is far beyond the 2 second limit. We need a linear or near-linear approach.

The tricky part is handling the time window boundaries correctly. The phrase “last `n` seconds” is inclusive. If `n = 60` and the current warning happens at `16:16:43`, then warnings from `16:15:44` through `16:16:43` count, but warnings at `16:15:43` do not.

Another subtle issue is that multiple warnings can share the exact same timestamp. A careless implementation that treats timestamps as unique moments would undercount.

Consider this example:

```
2 2
2012-01-01 00:00:00: A
2012-01-01 00:00:00: B
```

The correct answer is:

```
2012-01-01 00:00:00
```

Both warnings belong to the same 2 second window ending at that timestamp.

Here is another boundary example:

```
3 2
2012-01-01 00:00:00: A
2012-01-01 00:00:03: B
```

The correct output is:

```
-1
```

The difference is exactly 3 seconds. For a window size of 3, the valid interval ending at `00:00:03` is `[00:00:01, 00:00:03]`, so the first warning is outside the window.

A common mistake is using `<= n` instead of `< n` when comparing timestamp differences.

## Approaches

The brute force solution is straightforward. For every warning, scan backward through earlier warnings and count how many timestamps fall into the last `n` seconds. As soon as the count reaches `m`, output the current timestamp.

This works because the logs are already sorted chronologically. For a fixed current warning, every earlier warning either belongs to the window or is too old.

The problem is performance. If there are `k` log entries, the brute force approach may compare every pair of entries. With hundreds of thousands of logs, this becomes quadratic. Even `200000^2` is completely infeasible.

The key observation is that the valid window only moves forward. Once an old warning becomes too old for the current window, it will never become valid again for any future window. That monotonic behavior makes a sliding window possible.

We maintain two pointers. The right pointer represents the current warning. The left pointer marks the earliest warning still inside the last `n` seconds. As we advance the right pointer, we move the left pointer forward whenever entries become too old.

At every step, the interval `[left, right]` contains exactly the warnings inside the current time window. The number of warnings is simply `right - left + 1`.

Because each pointer moves only forward, the total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k) | Too slow |
| Optimal Sliding Window | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Parse every log line and extract only the timestamp part. The message is irrelevant.
3. Convert each timestamp into an integer number of seconds from the start of the year.

Using integers makes time comparisons simple and fast. Instead of comparing date strings, we compare numeric differences.
4. Store both the original timestamp string and the numeric value.

We need the numeric form for calculations and the original form for output.
5. Initialize `left = 0`.

This pointer represents the earliest warning still inside the current window.
6. Iterate `right` from left to right over all warnings.
7. While the difference between the current warning and the warning at `left` is at least `n`, move `left` forward.

A warning exactly `n` seconds older is already outside the valid interval.
8. After adjusting the window, compute the number of warnings inside it as:

```
right - left + 1
```
9. If this count becomes at least `m`, immediately output the current timestamp and terminate.

Since we process logs chronologically, the first valid timestamp we encounter is the required answer.
10. If the loop finishes without finding such a window, print `-1`.

### Why it works

At every iteration, the sliding window maintains this invariant:

```
All warnings between left and right belong to the last n seconds,
and every warning before left is too old.
```

The while loop guarantees the left boundary is always minimal. That means the window contains every valid warning and excludes every invalid one.

Since the logs are processed in chronological order, the first time the window size reaches `m` is exactly the earliest moment satisfying the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MONTH_DAYS = [31, 29, 31, 30, 31, 30,
              31, 31, 30, 31, 30, 31]

PREFIX_DAYS = [0]
for d in MONTH_DAYS:
    PREFIX_DAYS.append(PREFIX_DAYS[-1] + d)

def to_seconds(ts: str) -> int:
    month = int(ts[5:7])
    day = int(ts[8:10])
    hour = int(ts[11:13])
    minute = int(ts[14:16])
    second = int(ts[17:19])

    days_before = PREFIX_DAYS[month - 1] + (day - 1)

    return (
        days_before * 24 * 3600
        + hour * 3600
        + minute * 60
        + second
    )

def solve():
    first = input().split()
    if not first:
        return

    n, m = map(int, first)

    logs = []

    for line in sys.stdin:
        line = line.rstrip('\n')

        ts = line[:19]
        sec = to_seconds(ts)

        logs.append((ts, sec))

    left = 0

    for right in range(len(logs)):
        current_time = logs[right][1]

        while current_time - logs[left][1] >= n:
            left += 1

        if right - left + 1 >= m:
            print(logs[right][0])
            return

    print(-1)

solve()
```

The first important implementation detail is timestamp parsing. Every timestamp has a fixed format, so substring slicing is faster and simpler than using a date library. Converting timestamps into absolute seconds removes all complexity from time comparisons.

The conversion uses cumulative month lengths because all dates belong to 2012, which is a leap year. February has 29 days.

The sliding window logic depends on one critical inequality:

```
while current_time - logs[left][1] >= n:
```

The `>= n` condition is correct because a warning exactly `n` seconds older lies outside the last `n` seconds window.

Another subtle point is that the algorithm never moves the `left` pointer backward. Each log enters the window once and leaves once, which guarantees linear complexity.

The original timestamp string is stored separately because reconstructing formatted timestamps from seconds would add unnecessary work.

## Worked Examples

### Sample 1

Input:

```
60 3
2012-03-16 16:15:25: Disk size is
2012-03-16 16:15:25: Network failute
2012-03-16 16:16:29: Cant write varlog
2012-03-16 16:16:42: Unable to start process
2012-03-16 16:16:43: Disk size is too small
2012-03-16 16:16:53: Timeout detected
```

| right | Current Timestamp | left after shrinking | Window Size | Valid |
| --- | --- | --- | --- | --- |
| 0 | 16:15:25 | 0 | 1 | No |
| 1 | 16:15:25 | 0 | 2 | No |
| 2 | 16:16:29 | 2 | 1 | No |
| 3 | 16:16:42 | 2 | 2 | No |
| 4 | 16:16:43 | 2 | 3 | Yes |

The first two warnings share the same second, so they both belong to the same window. When we reach `16:16:29`, the earlier warnings become too old because the difference is 64 seconds. The window resets. At `16:16:43`, the last three warnings fit inside 60 seconds, so this is the answer.

### Custom Example

Input:

```
3 2
2012-01-01 00:00:00: A
2012-01-01 00:00:02: B
2012-01-01 00:00:03: C
```

| right | Current Timestamp | left after shrinking | Window Size | Valid |
| --- | --- | --- | --- | --- |
| 0 | 00:00:00 | 0 | 1 | No |
| 1 | 00:00:02 | 0 | 2 | Yes |

The algorithm stops immediately at the second warning. The interval `[00:00:00, 00:00:02]` spans exactly 3 seconds inclusively, so both warnings count.

This trace confirms the boundary handling is correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each pointer moves forward at most once |
| Space | O(k) | Stores all parsed timestamps |

Here `k` is the number of log records.

This complexity easily fits the limits. Even with hundreds of thousands of logs, the sliding window performs only a linear number of operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MONTH_DAYS = [31, 29, 31, 30, 31, 30,
              31, 31, 30, 31, 30, 31]

PREFIX_DAYS = [0]
for d in MONTH_DAYS:
    PREFIX_DAYS.append(PREFIX_DAYS[-1] + d)

def to_seconds(ts: str) -> int:
    month = int(ts[5:7])
    day = int(ts[8:10])
    hour = int(ts[11:13])
    minute = int(ts[14:16])
    second = int(ts[17:19])

    days_before = PREFIX_DAYS[month - 1] + (day - 1)

    return (
        days_before * 24 * 3600
        + hour * 3600
        + minute * 60
        + second
    )

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    logs = []

    for line in sys.stdin:
        ts = line[:19]
        logs.append((ts, to_seconds(ts)))

    left = 0

    for right in range(len(logs)):
        while logs[right][1] - logs[left][1] >= n:
            left += 1

        if right - left + 1 >= m:
            return logs[right][0]

    return "-1"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""60 3
2012-03-16 16:15:25: Disk size is
2012-03-16 16:15:25: Network failute
2012-03-16 16:16:29: Cant write varlog
2012-03-16 16:16:42: Unable to start process
2012-03-16 16:16:43: Disk size is too small
2012-03-16 16:16:53: Timeout detected
"""
) == "2012-03-16 16:16:43"

# minimum case
assert run(
"""1 1
2012-01-01 00:00:00: A
"""
) == "2012-01-01 00:00:00"

# identical timestamps
assert run(
"""2 2
2012-01-01 00:00:00: A
2012-01-01 00:00:00: B
"""
) == "2012-01-01 00:00:00"

# exact boundary exclusion
assert run(
"""3 2
2012-01-01 00:00:00: A
2012-01-01 00:00:03: B
"""
) == "-1"

# sliding window shrink
assert run(
"""5 3
2012-01-01 00:00:00: A
2012-01-01 00:00:02: B
2012-01-01 00:00:04: C
2012-01-01 00:00:10: D
"""
) == "2012-01-01 00:00:04"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single log entry | Same timestamp | Minimum valid input |
| Two identical timestamps | Same timestamp | Multiple warnings in one second |
| Difference exactly `n` | `-1` | Correct inclusive window handling |
| Window shrink example | Third timestamp | Proper left pointer movement |

## Edge Cases

### Multiple warnings at the same second

Input:

```
2 2
2012-01-01 00:00:00: A
2012-01-01 00:00:00: B
```

The algorithm processes the second warning with:

```
current_time - oldest_time = 0
```

Since `0 < 2`, both warnings stay inside the window. The window size becomes 2, so the answer is:

```
2012-01-01 00:00:00
```

This case confirms the solution correctly handles duplicate timestamps.

### Timestamp exactly `n` seconds apart

Input:

```
3 2
2012-01-01 00:00:00: A
2012-01-01 00:00:03: B
```

When processing the second warning:

```
3 - 0 = 3
```

The condition:

```
while diff >= n
```

removes the first warning from the window. The remaining window size is 1, so the answer is `-1`.

This prevents the classic off-by-one bug.

### Earliest valid answer must be returned

Input:

```
10 2
2012-01-01 00:00:01: A
2012-01-01 00:00:05: B
2012-01-01 00:00:06: C
```

At the second warning, the window already contains two warnings, so the algorithm immediately outputs:

```
2012-01-01 00:00:05
```

Even though later timestamps also satisfy the condition, the problem asks for the first such moment.

### No valid window exists

Input:

```
2 3
2012-01-01 00:00:00: A
2012-01-01 00:00:10: B
2012-01-01 00:00:20: C
```

Every warning is isolated from the others by more than 2 seconds. The window size never exceeds 1, so the algorithm finishes the scan and prints:

```
-1
```

This confirms the solution correctly handles impossible cases.
