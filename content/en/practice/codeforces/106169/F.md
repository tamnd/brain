---
title: "CF 106169F - Sign Entanglement"
description: "The problem asks us to count pairs of events where the two events happened close enough in time and have opposite signs. Each record gives a timestamp and a sign, where + and - represent the two different sides."
date: "2026-06-25T11:08:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106169
codeforces_index: "F"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 106169
solve_time_s: 38
verified: true
draft: false
---

[CF 106169F - Sign Entanglement](https://codeforces.com/problemset/problem/106169/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count pairs of events where the two events happened close enough in time and have opposite signs. Each record gives a timestamp and a sign, where `+` and `-` represent the two different sides. A pair is valid if the timestamps differ by at most `d` and the two signs are different. The events are already sorted by time, so the task is to count all such cross-sign pairs efficiently.

The input size can reach `3 * 10^5`, which immediately rules out checking every pair of events. A direct comparison would perform around `n * (n - 1) / 2` checks, which is about `4.5 * 10^10` operations at the maximum size. Even a very optimized implementation cannot finish that in a typical contest time limit. We need to exploit the fact that the timestamps are sorted.

A few details cause incorrect answers in otherwise reasonable solutions. Equal timestamps are a common trap because the difference can be zero, and the condition allows pairs with the same time. For example:

```
3 0
5 5 5
+-+
```

The answer is `2` because the two `+` events pair with the `-` event at the same timestamp. A solution that only looks for strictly smaller or larger times would miss them.

Another mistake is forgetting that multiple events at the same timestamp are separate events. For example:

```
4 1
1 1 2 2
++--
```

The answer is `4`. Every `+` at time `1` matches every `-` at time `2`. Counting only distinct timestamps would produce `1`, which is wrong.

The final tricky case is the boundary of distance `d`. For example:

```
2 3
10 13
+-
```

The answer is `1` because the distance is exactly `3`. Using a strict comparison instead of `<= d` loses valid pairs.

## Approaches

The straightforward approach is to compare every positive event with every negative event. For each pair, we compute the absolute difference between their times and add one if it is at most `d`. This is easy to reason about because it directly follows the definition of a valid pair.

The problem is that the number of comparisons grows quadratically. With `n = 300000`, the number of possible pairs is roughly `45000000000`, which is far beyond what we can process.

The useful observation comes from the sorted timestamps. Instead of checking whether every earlier event matches a later event, we can maintain the set of previous events that are still close enough to the current one. When we move from left to right, every previous event either remains inside the allowed time window or becomes too old and can never match again.

For every current event, we need to know how many previous events have the opposite sign and a timestamp at least `current_time - d`. Since the input is sorted, we can remove expired events with a moving pointer. We only need the counts of active `+` and `-` events, not their individual positions.

When the current event is `+`, it forms a valid pair with all active `-` events. When it is `-`, it forms a valid pair with all active `+` events. After counting, we insert the current event into the active window so that future events can use it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sliding Window Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store all events as `(time, sign)` pairs. The events are already sorted, so we can process them in the given order without sorting again. Keep a left pointer representing the first event that is still inside the valid time window.
2. Maintain counts of active events separated by sign. The active window contains exactly the previous events whose timestamps are at least `current_time - d`.
3. Before processing the current event, move the left pointer forward while the event at the left side is too old. Remove its sign from the active counts because it can no longer form a valid pair with any future event.
4. Look at the current event's sign. If it is `+`, add the number of active `-` events to the answer. If it is `-`, add the number of active `+` events instead. These are exactly the previous events with the opposite sign and valid distance.
5. Insert the current event into the active window by increasing the corresponding sign count. It may match later events, so it must stay available.

Why it works: at every point in the scan, the active window contains all and only the previous events that can still create a valid pair with the current and future events. Every pair is counted exactly once, when the later event in the pair is processed. Since we only add opposite-sign events from the active window, every counted pair satisfies the sign condition and the time condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    t = list(map(int, input().split()))
    s = input().strip()

    ans = 0
    left = 0
    plus = 0
    minus = 0

    for i in range(n):
        while left < i and t[left] < t[i] - d:
            if s[left] == '+':
                plus -= 1
            else:
                minus -= 1
            left += 1

        if s[i] == '+':
            ans += minus
            plus += 1
        else:
            ans += plus
            minus += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The main loop implements the sliding window from the walkthrough. The pointer `left` never moves backwards, so every event is removed at most once. This is what keeps the total work linear.

The removal condition uses `t[left] < t[i] - d` rather than `<=` because timestamps with difference exactly `d` are still valid. The current event is counted before being added to the stored counts, preventing an event from pairing with itself.

Python integers are sufficient here because the answer can be as large as the number of all pairs, which is around `4.5 * 10^10`.

## Worked Examples

For the first example:

```
5 2
1 2 3 4 5
+-++-
```

| Current event | Active `+` | Active `-` | Added to answer | Answer |
| --- | --- | --- | --- | --- |
| `1 +` | 0 | 0 | 0 | 0 |
| `2 -` | 1 | 0 | 1 | 1 |
| `3 +` | 1 | 1 | 1 | 2 |
| `4 +` | 1 | 1 | 1 | 3 |
| `5 -` | 2 | 1 | 2 | 5 |

The final answer is `5`. This trace shows that events at the boundary distance are still kept, because time differences of exactly `2` remain valid.

For the second example:

```
4 0
7 7 8 8
++--
```

| Current event | Active `+` | Active `-` | Added to answer | Answer |
| --- | --- | --- | --- | --- |
| `7 +` | 0 | 0 | 0 | 0 |
| `7 +` | 1 | 0 | 0 | 0 |
| `8 -` | 0 | 0 | 0 | 0 |
| `8 -` | 0 | 1 | 0 | 0 |

The answer is `0` because only equal timestamps can match when `d = 0`, and all equal timestamps have the same sign in this case. The trace confirms that the window removes events with different timestamps when the allowed distance is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each event enters the window once and leaves the window once |
| Space | O(n) | The timestamp and sign arrays are stored |

The solution easily fits the constraints because the total number of operations is proportional to the number of events. The memory usage is linear and remains well within typical contest limits.

## Test Cases

```python
import sys
import io

def solve(data):
    inp = io.StringIO(data)
    n, d = map(int, inp.readline().split())
    t = list(map(int, inp.readline().split()))
    s = inp.readline().strip()

    ans = 0
    left = 0
    plus = 0
    minus = 0

    for i in range(n):
        while left < i and t[left] < t[i] - d:
            if s[left] == '+':
                plus -= 1
            else:
                minus -= 1
            left += 1

        if s[i] == '+':
            ans += minus
            plus += 1
        else:
            ans += plus
            minus += 1

    return str(ans)

# sample
assert solve("""14 3
1 1 3 3 3 3 5 5 6 6 6 8 9 11
+--+++--+++++-
""") == "23"

# minimum size
assert solve("""1 10
5
+
""") == "0"

# all equal values
assert solve("""5 0
7 7 7 7 7
+-+-+
""") == "6"

# boundary distance
assert solve("""2 3
10 13
+-
""") == "1"

# all pairs valid
assert solve("""4 100
1 2 3 4
++++
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single event | 0 | No pair can be formed |
| Equal timestamps with mixed signs | 6 | Handles zero distance and duplicates |
| Distance exactly equal to `d` | 1 | Checks inclusive boundary |
| Same sign everywhere | 0 | Confirms sign filtering |

## Edge Cases

For the equal timestamp case:

```
3 0
5 5 5
+-+
```

The first event is added to the active `+` count. The second event sees one active `+`, so it adds one valid `-` pair and is added to the `-` count. The third event sees one active `-`, adding another pair. The result is `2`, which matches the fact that only events at the exact same time can pair.

For duplicate timestamps with many events:

```
4 1
1 1 2 2
++--
```

Both events at time `1` remain active when processing the two events at time `2`, because their difference is exactly `1`. Each negative event counts two positive events, giving `4` total pairs. The algorithm handles multiplicities because it stores counts of events, not unique timestamps.

For the boundary condition:

```
2 3
10 13
+-
```

The first event remains in the window because `10 < 13 - 3` is false. The second event sees one opposite-sign event and adds it to the answer. The result is `1`, proving the inclusive comparison is handled correctly.
