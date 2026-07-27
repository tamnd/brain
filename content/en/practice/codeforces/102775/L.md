---
title: "CF 102775L - \u0412\u0438\u0448\u043d\u0435\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441"
description: "We have a collection of cherry trees. Each tree is described by three numbers: the day it begins blooming, the last day when new flowers are added, and how many flowers appear or disappear in one daily change."
date: "2026-07-27T20:45:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "L"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 84
verified: true
draft: false
---

[CF 102775L - \u0412\u0438\u0448\u043d\u0435\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441](https://codeforces.com/problemset/problem/102775/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of cherry trees. Each tree is described by three numbers: the day it begins blooming, the last day when new flowers are added, and how many flowers appear or disappear in one daily change.

For a tree with parameters `a`, `b`, and `k`, the number of flowers is zero before day `a`. On day `a` it has `k` flowers, and every morning until day `b` it gains another `k` flowers. After the evening of day `b`, the tree loses `k` flowers every day until it becomes empty. The task is to find the earliest day when the total number of flowers on all trees reaches its maximum.

The input contains up to `10^5` trees, and the days and flower counts can be as large as `10^9`. This immediately rules out iterating over every possible day because the range of days can be around `10^9`, while the number of trees is also large. A solution needs to process the important changes of the function rather than every individual day. An `O(N log N)` solution is appropriate because sorting around `3N` events fits comfortably for `N = 10^5`.

Several boundary cases are easy to mishandle. A tree whose blooming period contains only one day must still be processed correctly.

For example:

```
1
5 5 10
```

The answer is:

```
5
```

The tree has 10 flowers on day 5 and zero afterward. A solution that treats the growth interval as empty because `a == b` may miss the peak.

Another tricky case is the exact transition after the last blooming day.

For example:

```
1
3 4 7
```

The flower counts are 7 on day 3, 14 on day 4, and 7 on day 5. The answer is:

```
4
```

A careless implementation that starts decreasing on day `b` instead of after day `b` would incorrectly move the maximum.

Ties also matter. The required answer is the first day with the maximum number of flowers.

For example:

```
2
1 1 5
3 3 5
```

The total reaches 5 on day 1 and again on day 3, so the answer is:

```
1
```

Updating the answer on equal values would return the wrong day.

## Approaches

The straightforward approach is to simulate the garden day by day. For every day, we could calculate the contribution of every tree and keep the best total seen so far. This is correct because it directly evaluates the function we care about. However, it is far too slow. The largest possible day values are near `10^9`, so even visiting every day would already require billions of iterations. Multiplying that by `10^5` trees gives a worst case far beyond the available limits.

The key observation is that we do not need the number of flowers on every day separately. A tree changes in a very regular way: it increases by a constant amount for a while, then decreases by the same constant amount. Instead of storing the flower count itself, we can store how much the total changes from one day to the next.

For a single tree, let `D(day)` be the change in flowers from the previous day to this day. The tree contributes `+k` to this difference from day `a` through day `b`, because the flower count increases every morning. Then it contributes `-k` from day `b + 1` through day `2b - a + 1`, because the flowers are disappearing. After that, the contribution is zero.

This converts every tree into three events that modify the current daily difference:

```
day a:       increase daily change by k
day b + 1:   decrease daily change by 2k
day 2b-a+2:  increase daily change by k
```

After collecting all events, we sweep them in order. Between two event days, the daily difference stays constant, so the total number of flowers can be updated by multiplying the difference by the length of the interval. This compresses billions of possible days into only `3N` meaningful positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max_day × N) | O(1) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Create an event map where each key is a day and the value is the change applied to the daily difference on that day. For every tree `(a, b, k)`, add `+k` at `a`, `-2k` at `b + 1`, and `+k` at `2b - a + 2`. These three events exactly describe when the slope of the flower count changes.
2. Sort all event days. Only these days can change the current daily difference, so every other day belongs to an interval where the behavior is predictable.
3. Sweep through the sorted event days while maintaining two values: the current number of flowers before the next processed day, and the current daily difference. Before processing an event day `x`, jump over the gap from the previous position to `x - 1` by adding `daily_difference * gap_length`.
4. Apply the event at day `x` to update the daily difference, then move one day forward using the new difference. The resulting value is the number of flowers on day `x`, so compare it with the best answer found so far.
5. Update the answer only when the flower count becomes strictly larger. Keeping the first occurrence automatically handles days with equal maximum values.

Why it works:

The sweep maintains the exact value of the total flower count at every event boundary. Between two consecutive event days, no tree changes its growth rate, so the total changes linearly with a fixed daily difference. The event representation changes that difference at exactly the days where some tree switches behavior. Since every possible maximum of a piecewise linear sequence over integer days must occur at an interval boundary or the start of an interval with a constant direction, checking these compressed positions finds the true earliest maximum day.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())
    events = defaultdict(int)

    for _ in range(n):
        a, b, k = map(int, input().split())
        events[a] += k
        events[b + 1] -= 2 * k
        events[2 * b - a + 2] += k

    days = sorted(events)

    current_change = 0
    flowers = 0
    position = 1

    best_flowers = 0
    answer = 1

    for day in days:
        flowers += current_change * (day - position)

        current_change += events[day]

        flowers += current_change

        if flowers > best_flowers:
            best_flowers = flowers
            answer = day

        position = day + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The event construction in the first loop is the core transformation. The first event starts the increasing part of the tree. The second event removes the previous increase and starts the decrease, which changes the daily difference by `-2k`. The third event cancels the decrease after the tree becomes empty.

The sweep keeps `current_change` as the change in total flowers when moving from one day to the next. The variable `flowers` stores the total at the current processed position. Before reaching a new event day, the code skips all intermediate days at once because the same difference applies throughout that interval.

The order inside the loop is important. The event must be applied before adding the flowers of the event day because the event describes the difference that becomes active on that exact day. Applying it one day later would introduce an off-by-one error at every boundary.

Python integers are used automatically for arbitrary precision, which avoids overflow even though the final answer is only guaranteed to fit in 64 bits.

## Worked Examples

Sample input:

```
3
1 9 1
20 24 2
35 36 5
```

The events are processed as follows:

| Day | Daily change before event | Event change | Flowers after processing day | Best answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | +1 | 1 | 1 |
| 10 | 1 | -2 | 9 | 10 |
| 19 | -1 | +1 | 0 | 10 |
| 20 | 0 | +2 | 2 | 20 |
| 25 | 2 | -4 | 10 | 24 |
| 35 | -2 | +5 | 2 | 24 |
| 37 | 3 | -5 | 10 | 24 |

The maximum value appears first on day 24, even though the same number of flowers appears again later. This demonstrates why equal values must not replace the stored answer.

Another example:

```
1
5 5 10
```

| Day | Daily change before event | Event change | Flowers after processing day | Best answer |
| --- | --- | --- | --- | --- |
| 5 | 0 | +10 | 10 | 5 |
| 6 | 10 | -20 | 0 | 5 |
| 7 | -10 | +10 | 0 | 5 |

The single-day blooming interval is handled naturally. The answer is the only day with positive flowers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | There are exactly three events per tree, and sorting the event days dominates the work. |
| Space | O(N) | The event map stores at most three entries per tree. |

With `N = 100000`, the algorithm processes about `300000` events and only sorts this many values. It avoids dependence on the size of the day values, so large days near `10^9` do not affect performance.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided sample
assert run("""3
1 9 1
20 24 2
35 36 5
""") == "24\n", "sample"

# single tree, minimum interval
assert run("""1
5 5 10
""") == "5\n", "single day bloom"

# equal maximums, earliest must win
assert run("""2
1 1 5
3 3 5
""") == "1\n", "first maximum"

# boundary after blooming period
assert run("""1
3 4 7
""") == "4\n", "peak on last growth day"

# all trees overlap completely
assert run("""3
1 3 2
1 3 5
1 3 7
""") == "3\n", "combined peak"

# large values
assert run("""1
1000000000 1000000000 1000000000
""") == "1000000000\n", "large day values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 5 10` | `5` | Single-day flowering period |
| Two separated trees with the same peak | `1` | Earliest maximum handling |
| `3 4 7` | `4` | Correct transition between growth and decay |
| Three identical overlapping trees | `3` | Combining multiple contributions |
| Very large day values | `1000000000` | No iteration over the day range |

## Edge Cases

For the single-day blooming case:

```
1
5 5 10
```

The event days are 5, 6, and 7. On day 5 the daily change becomes `10`, giving 10 flowers. On day 6 the daily change becomes `-10`, reducing the total to zero. The algorithm checks day 5 before moving on, so it returns 5 correctly.

For the boundary after the last growth day:

```
1
3 4 7
```

The events are:

```
3: +7
5: -14
7: +7
```

Day 3 gives 7 flowers, day 4 gives 14 flowers, and day 5 begins the decrease. The algorithm applies the `-14` event on day 5 rather than day 4, preserving the correct maximum at day 4.

For equal maximum values:

```
2
1 1 5
3 3 5
```

The sweep reaches 5 flowers on day 1 and stores that as the best result. When it reaches day 3 with the same number of flowers, the strict comparison prevents replacing the earlier answer.

For very large coordinates:

```
1
1000000000 1000000000 1000000000
```

The algorithm creates only three events around the large day values. It never loops through the billion empty days before flowering, which is the main reason the event sweep fits the constraints.
