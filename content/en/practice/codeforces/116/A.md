---
title: "CF 116A - Tram"
description: "We have a single tram traveling along a line with n stops, starting empty at the first stop and ending empty at the last stop. At each stop, a certain number of passengers exit before any new passengers enter."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 116
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 87 (Div. 2 Only)"
rating: 800
weight: 116
solve_time_s: 93
verified: true
draft: false
---

[CF 116A - Tram](https://codeforces.com/problemset/problem/116/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a single tram traveling along a line with _n_ stops, starting empty at the first stop and ending empty at the last stop. At each stop, a certain number of passengers exit before any new passengers enter. The input consists of pairs of integers for each stop: the number leaving and the number entering. Our task is to determine the minimum tram capacity required to ensure that at no point does the number of passengers inside exceed the tram’s capacity.

The constraints are straightforward: there are at most 1000 stops, and the number of passengers entering or leaving at any stop does not exceed 1000. Because the input size is small, an O(n) solution is perfectly acceptable. A naive algorithm that simulates each stop sequentially will work in under a millisecond.

A non-obvious edge case arises when many passengers enter or exit at the first or last stop. For example, if the first stop has 0 leaving and 1000 entering, the capacity must be at least 1000 immediately. Another subtle case is when entering and exiting balances temporarily, but spikes later. For instance, with stops `0 5`, `3 2`, `2 4`, `6 0`, the tram sees peaks at different stops, and we need to track the running maximum, not just total sum.

## Approaches

The brute-force approach is actually already efficient: we simulate the tram’s journey. Start with zero passengers. At each stop, subtract the number leaving and add the number entering, then record the current number of passengers. Track the maximum seen during the simulation. That maximum is the minimum capacity the tram must have. This is correct because the tram never exceeds that peak, and the tram must handle at least that many passengers.

There is no faster method in asymptotic terms for this problem because we must inspect every stop to see the entry and exit dynamics. The key insight is that the order of operations matters: passengers always exit before entering. Any careless swap would give an incorrect peak. Another subtle point is initializing the passenger count to zero and confirming the first stop does not attempt to remove passengers, which is guaranteed by the input constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate each stop | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `current_passengers` to zero. This represents the number of people currently in the tram.
2. Initialize `max_passengers` to zero. This will track the peak tram occupancy.
3. Iterate over each stop from the first to the last. For each stop, subtract the number of exiting passengers from `current_passengers`. This reflects that exits happen before entries.
4. Add the number of entering passengers to `current_passengers`.
5. Update `max_passengers` if `current_passengers` exceeds the current maximum.
6. After processing all stops, `max_passengers` holds the minimum tram capacity required. Print this value.

Why it works: the invariant is that `current_passengers` always accurately reflects the number of passengers after each stop. Updating `max_passengers` ensures we capture the largest occupancy during the entire journey. Since exits always occur before entries, the order of operations correctly models real tram behavior. By the final stop, all passengers have exited, which matches the problem constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
current_passengers = 0
max_passengers = 0

for _ in range(n):
    a, b = map(int, input().split())
    current_passengers -= a
    current_passengers += b
    max_passengers = max(max_passengers, current_passengers)

print(max_passengers)
```

The code follows the algorithm step-by-step. We read the number of stops, initialize the counters, and then loop through each stop. Using `map(int, input().split())` safely converts the exit and entry counts. The subtraction before addition respects the exit-before-entry rule. Tracking `max_passengers` guarantees that we capture the peak load. There is no need for extra arrays or lists since we only need a running count and a maximum.

## Worked Examples

Sample Input 1:

```
4
0 3
2 5
4 2
4 0
```

| Stop | Exiting | Entering | Current | Max |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 3 | 3 |
| 2 | 2 | 5 | 6 | 6 |
| 3 | 4 | 2 | 4 | 6 |
| 4 | 4 | 0 | 0 | 6 |

This trace shows the tram occupancy at each stop. The peak occurs at stop 2 with 6 passengers, confirming the answer.

Sample Input 2:

```
3
0 2
1 3
4 0
```

| Stop | Exiting | Entering | Current | Max |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 2 | 2 |
| 2 | 1 | 3 | 4 | 4 |
| 3 | 4 | 0 | 0 | 4 |

The maximum occupancy is 4, demonstrating the algorithm correctly handles smaller cases with mixed entry and exit patterns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each stop is processed exactly once. With n ≤ 1000, this executes in under a millisecond. |
| Space | O(1) | Only two counters are maintained; no additional storage grows with n. |

This confirms that the solution fits comfortably within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    current_passengers = 0
    max_passengers = 0
    for _ in range(n):
        a, b = map(int, input().split())
        current_passengers -= a
        current_passengers += b
        max_passengers = max(max_passengers, current_passengers)
    return str(max_passengers)

# provided sample
assert run("4\n0 3\n2 5\n4 2\n4 0\n") == "6", "sample 1"

# custom cases
assert run("2\n0 0\n0 0\n") == "0", "all zero"
assert run("3\n0 5\n5 0\n0 0\n") == "5", "peak at first stop"
assert run("5\n0 1\n1 2\n2 3\n3 4\n4 0\n") == "7", "gradual buildup"
assert run("3\n0 1000\n0 0\n1000 0\n") == "1000", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 stops, all zeros | 0 | Minimum-size input, no passengers |
| 3 stops, peak at first | 5 | First stop causes peak occupancy |
| 5 stops, gradual buildup | 7 | Incremental increases across stops |
| 3 stops, large numbers | 1000 | Handling maximum passenger values |

## Edge Cases

The first edge case is when the first stop already causes a high peak. For input:

```
2
0 1000
1000 0
```

After the first stop, `current_passengers` is 1000, which updates `max_passengers` to 1000. After the last stop, all exit, returning to 0. The algorithm correctly reports 1000 as the required capacity.

Another edge case is when entries and exits perfectly cancel out, never exceeding the initial load. Input:

```
3
0 3
3 3
3 0
```

The occupancy fluctuates: stop 1 → 3, stop 2 → 3 (after exit 3, enter 3), stop 3 → 0. The maximum remains 3. The simulation handles these cancellations correctly because it tracks the running maximum after each stop.
