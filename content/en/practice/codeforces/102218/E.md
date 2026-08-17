---
title: "CF 102218E - Environmental Contingency"
description: "We have an array of N AQI predictions, one value for each consecutive day. We also know the weekday corresponding to the first array element and a threshold X. A school day is suspended exactly when its AQI is at least X."
date: "2026-08-17T23:18:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "E"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 176
verified: false
draft: false
---

[CF 102218E - Environmental Contingency](https://codeforces.com/problemset/problem/102218/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of `N` AQI predictions, one value for each consecutive day. We also know the weekday corresponding to the first array element and a threshold `X`. A school day is suspended exactly when its AQI is at least `X`. Saturdays and Sundays are never counted, even when their AQI reaches the threshold.

The task is to count array positions whose AQI is at least `X` and whose corresponding weekday is Monday through Friday.

The first line can contain as many as `10^6` days. That immediately rules out algorithms that repeatedly scan the array or perform work proportional to the distance from the first day for every position. An `O(N)` scan is the natural target because every AQI value has to be inspected at least once. With `N = 10^6`, an `O(N log N)` solution would still be mathematically reasonable, but it provides no benefit here, while `O(N^2)` can require roughly `5 * 10^11` iterations and is far beyond the one-second limit.

The AQI values and threshold are bounded between `0` and `500`, so there is no integer-overflow concern in the answer. At most `10^6` days can be counted.

The first non-obvious case is when the first day is a weekend. For example:

```
1 Saturday 100
100
```

The correct answer is `0`. A careless implementation that only checks `AQI >= X` would return `1`, forgetting that Saturday has no classes.

The second case is that the threshold comparison is inclusive. For example:

```
1 Monday 100
100
```

The correct answer is `1`, because an AQI exactly equal to `X` suspends classes. Using `>` instead of `>=` would incorrectly return `0`.

The third case is crossing Sunday while scanning. For example:

```
3 Friday 100
100 100 100
```

The days are Friday, Saturday, Sunday, so the answer is `1`. An implementation that checks only the first weekday and forgets to advance the weekday for every array position could incorrectly count all three values.

## Approaches

A direct brute-force approach could determine the weekday of each array position independently. For position `i`, start from the given first weekday and advance through the calendar one day at a time until reaching position `i`. Then check whether that weekday is a weekday and whether `a[i] >= X`.

This approach is correct because it reconstructs the exact weekday of every array element. The problem is that it repeats the same calendar work. For position `0` no advancement is needed, for position `1` one advancement is needed, and for position `N - 1`, `N - 1` advancements are needed. The total number of weekday advances is

`0 + 1 + 2 + ... + (N - 1) = N(N - 1)/2`.

At `N = 10^6`, that is `499,999,500,000` weekday advances, before even accounting for the AQI checks. That cannot fit within the time limit.

The key observation is that consecutive array positions represent consecutive calendar days. Once we know the weekday of position `i`, the weekday of position `i + 1` is simply the next weekday in the seven-day cycle. There is no reason to recompute the calendar from the beginning.

We can represent Monday through Sunday by integers `0` through `6`. For every AQI value, we check two conditions: the AQI must be at least `X`, and the current weekday must be one of `0, 1, 2, 3, 4`. After processing the value, we advance the weekday with `(weekday + 1) % 7`.

The brute-force method and the optimal method both inspect the AQI values, but the optimal method performs only constant work per day instead of repeatedly reconstructing the same prefix of the calendar.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Map the seven weekday names to integers in calendar order, with Monday as `0` and Sunday as `6`. This gives us a compact representation where moving to the next day is just an increment modulo `7`.
2. Read `N`, the name of the first weekday, and the threshold `X`. Convert the starting weekday name into its integer representation.
3. Read the `N` AQI values and process them from left to right. At position `i`, the variable `weekday` represents the actual weekday of `a[i]`.
4. If `weekday < 5` and `a[i] >= X`, increment the answer. The first condition excludes Saturday and Sunday, while the second applies the suspension threshold exactly as specified.
5. Advance `weekday` using `(weekday + 1) % 7`. This moves from Monday to Tuesday, Tuesday to Wednesday, and so on, with Sunday wrapping back to Monday.
6. Print the final count after all `N` days have been processed.

### Why it works

The invariant is that immediately before processing `a[i]`, `weekday` is exactly the weekday corresponding to the `i`-th array element. It is true initially because `weekday` is initialized from the stated first day. If it is true for position `i`, advancing it once gives the weekday of the next calendar day, which is exactly the weekday corresponding to position `i + 1`. Thus the invariant holds for every position.

For each position, the algorithm increments the answer exactly when the AQI is at least `X` and the day is Monday through Friday. Those are precisely the conditions for classes to be suspended, so every counted day is valid and every valid day is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    day_to_num = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    n, day_name, x = input().split()
    n = int(n)
    x = int(x)

    weekday = day_to_num[day_name]
    answer = 0

    remaining = n
    while remaining:
        values = map(int, input().split())
        for aqi in values:
            if weekday < 5 and aqi >= x:
                answer += 1

            weekday = (weekday + 1) % 7
            remaining -= 1

            if remaining == 0:
                break

    print(answer)

if __name__ == "__main__":
    solve()
```

The dictionary converts the textual starting weekday into the integer cycle used by the algorithm. Monday is `0` and Friday is `4`, so the condition `weekday < 5` identifies exactly the five school days.

The input-reading loop deserves some attention. Although the problem places all `N` AQI values on the second line, processing the line with `split()` is sufficient for the official input. The loop also handles the values incrementally and avoids storing the entire AQI array, which keeps the algorithm's additional space at `O(1)`.

The counter `remaining` makes the processing robust even if the input were split across multiple lines. Each consumed AQI decreases it by one, and processing stops exactly after `N` values.

The comparison uses `>=`, not `>`, because an AQI equal to the threshold is enough to suspend classes. The weekday is advanced after the current AQI is checked, so the first AQI is evaluated against the supplied starting day rather than the following day. This ordering prevents the most common off-by-one error.

Python integers do not overflow for this problem, and the answer is at most `10^6`.

## Worked Examples

### Sample 1

The first day is Wednesday, represented by `2`. The threshold is `6`. The weekdays progress through the normal seven-day cycle.

| AQI | Weekday number | Weekday | AQI >= 6 | School day | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | Wednesday | No | Yes | 0 |
| 2 | 3 | Thursday | No | Yes | 0 |
| 3 | 4 | Friday | No | Yes | 0 |
| 4 | 5 | Saturday | No | No | 0 |
| 5 | 6 | Sunday | No | No | 0 |
| 6 | 0 | Monday | Yes | Yes | 1 |
| 7 | 1 | Tuesday | Yes | Yes | 2 |
| 8 | 2 | Wednesday | Yes | Yes | 3 |
| 9 | 3 | Thursday | Yes | Yes | 4 |
| 10 | 4 | Friday | Yes | Yes | 5 |

The first five values do not contribute. The last five all reach the threshold and occur on Monday through Friday, producing the answer `5`. The trace also shows why the weekday must be advanced after every value, including weekend values.

### Sample 2

The first day is Saturday, represented by `5`, and the threshold is `223`.

| AQI | Weekday number | Weekday | AQI >= 223 | School day | Answer |
| --- | --- | --- | --- | --- | --- |
| 90 | 5 | Saturday | No | No | 0 |
| 372 | 6 | Sunday | Yes | No | 0 |
| 191 | 0 | Monday | No | Yes | 0 |
| 282 | 1 | Tuesday | Yes | Yes | 1 |
| 223 | 2 | Wednesday | Yes | Yes | 2 |

Three AQI values reach the threshold, but the `372` occurs on Sunday and is excluded. The final answer is `2`. This confirms that AQI qualification alone is insufficient, and the weekday condition must be checked independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every AQI value is processed exactly once, with constant work per value. |
| Space | O(1) | Only the current weekday, threshold, remaining count, and answer are maintained apart from the small weekday dictionary. |

With `N` as large as `10^6`, a single linear scan is appropriate for the one-second limit. The algorithm performs only a few integer operations per day and does not allocate an array containing all AQI values, so its additional memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    day_to_num = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    n, day_name, x = input().split()
    n = int(n)
    x = int(x)

    weekday = day_to_num[day_name]
    answer = 0

    remaining = n
    while remaining:
        values = map(int, input().split())
        for aqi in values:
            if weekday < 5 and aqi >= x:
                answer += 1

            weekday = (weekday + 1) % 7
            remaining -= 1

            if remaining == 0:
                break

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    """10 Wednesday 6
1 2 3 4 5 6 7 8 9 10
"""
) == "5", "sample 1"

assert run(
    """5 Saturday 223
90 372 191 282 223
"""
) == "2", "sample 2"

assert run(
    """5 Sunday 269
90 372 191 282 223
"""
) == "2", "sample 3"

# Minimum-size input, weekend day
assert run(
    """1 Saturday 0
500
"""
) == "0", "single weekend day"

# Exact threshold must count
assert run(
    """1 Monday 100
100
"""
) == "1", "threshold is inclusive"

# Weekend crossing and threshold boundary
assert run(
    """7 Friday 200
200 200 200 199 201 200 200
"""
) == "2", "Friday through Thursday with weekend excluded"

# All values equal to the threshold, full week
assert run(
    """7 Monday 500
500 500 500 500 500 500 500
"""
) == "5", "all weekdays at exact threshold"

# Maximum-size input, all values equal and all days qualifying on weekdays
n = 1_000_000
values = "500 " * (n - 1) + "500"
large_input = f"{n} Monday 500\n{values}\n"
assert run(large_input) == "714286", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 Saturday 0` with AQI `500` | `0` | Minimum size and weekend exclusion |
| `1 Monday 100` with AQI `100` | `1` | Inclusive `>= X` boundary |
| `7 Friday 200` with mixed AQI values | `2` | Correct weekday progression across Saturday and Sunday |
| `7 Monday 500` with every AQI equal to `500` | `5` | All-equal values and exact threshold |
| `1,000,000` Monday values of `500` | `714286` | Maximum input size and linear-time behavior |

## Edge Cases

For a single weekend day, consider:

```
1 Saturday 0
500
```

The initial weekday is `5`, so `weekday < 5` is false. Although `500 >= 0`, the answer remains `0`. The algorithm then advances to Sunday, but there are no more values to process.

For the exact-threshold boundary:

```
1 Monday 100
100
```

The weekday is Monday and `100 >= 100` is true, so the answer becomes `1`. This catches implementations that accidentally use a strict `>` comparison.

For a calendar transition across the weekend:

```
3 Friday 100
100 100 100
```

The first value is Friday and is counted. The second is Saturday and is rejected because schools are closed. The third is Sunday and is also rejected. The final answer is `1`. The weekday state changes from `4` to `5` to `6`, demonstrating that the update must happen after processing each AQI.

For the complete weekly cycle:

```
7 Monday 500
500 500 500 500 500 500 500
```

The first five values correspond to Monday through Friday and are all counted. The sixth and seventh correspond to Saturday and Sunday and are ignored. The result is `5`. This confirms both the weekday boundary and the modulo-7 wraparound.

The maximum-size case contains `10^6` AQI values. Since each value causes one comparison and one weekday update, the running time grows linearly rather than quadratically. The algorithm never needs to retain the AQI array, so its working state remains constant even at the largest input size.
