---
title: "CF 4B - Before an Exam"
description: "We are given d days and a target total number of study hours, sumTime. For every day, Peter must study at least minTime["
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 4
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 4 (Div. 2 Only)"
rating: 1200
weight: 4
solve_time_s: 72
verified: true
draft: false
---

[CF 4B - Before an Exam](https://codeforces.com/problemset/problem/4/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `d` days and a target total number of study hours, `sumTime`. For every day, Peter must study at least `minTime[i]` hours and at most `maxTime[i]` hours. The task is to construct any valid schedule whose total sum is exactly `sumTime`.

This is not an optimization problem. We do not need the minimum or maximum schedule, only any schedule that satisfies all constraints.

The first thing to notice is that every day contributes an interval of possible values. Across all days, the smallest achievable total is:

```
sum(minTime[i])
```

and the largest achievable total is:

```
sum(maxTime[i])
```

If `sumTime` lies outside this range, no solution exists.

The constraints are tiny. `d` is at most 30, and each daily limit is at most 8. Even exponential solutions might look tempting at first because the search space is not enormous compared to typical Codeforces problems. But the number of possible schedules can still explode. If every day allows 9 choices from 0 to 8, then the total number of assignments becomes:

```
9^30 ≈ 4.2 × 10^28
```

which is completely impossible to brute force.

The small constraints instead hint that the intended solution is constructive. We are supposed to directly build a valid schedule rather than search for one.

A subtle edge case appears when the target sum is smaller than the sum of all minimum values. For example:

```
2 3
2 5
2 5
```

The minimum achievable total is already 4, so no schedule works. A careless greedy solution that starts from zeros and increases values might accidentally produce invalid daily values.

Another tricky case happens when the target equals the minimum total exactly:

```
3 6
1 4
2 5
3 7
```

Here the only necessary schedule is:

```
1 2 3
```

Some implementations continue distributing extra hours even though no extra hours remain, which can push a day beyond its maximum.

The opposite boundary also matters. Suppose:

```
2 10
3 5
4 5
```

The maximum achievable total is exactly 10, so the only valid schedule is:

```
5 5
```

If the algorithm distributes hours incorrectly or stops early, it may fail to reach the required sum.

There is also the single-day case:

```
1 6
5 7
```

The answer is simply `6`. But for:

```
1 48
5 7
```

the target lies outside the allowed interval, so the answer is `NO`.

## Approaches

A brute-force solution would try every possible study schedule. For each day, we choose some value between `minTime[i]` and `maxTime[i]`, then check whether the final sum equals `sumTime`.

This works logically because it explores the entire search space. If a valid schedule exists, brute force eventually finds it.

The problem is the number of combinations. In the worst case, each day has 9 possible values, from 0 to 8. With 30 days, that becomes:

```
9^30
```

which is astronomically large.

The key insight is that the problem only cares about the total sum, not about any special arrangement between days. Once we know the target lies between the global minimum and maximum possible sums, we can always construct a valid schedule greedily.

Start with the minimum valid schedule:

```
schedule[i] = minTime[i]
```

This guarantees every day already satisfies its lower bound.

Now compute how many extra hours are still needed:

```
remaining = sumTime - sum(minTime)
```

For each day, we can safely increase its value by at most:

```
maxTime[i] - minTime[i]
```

So we greedily add as many extra hours as possible to the current day without exceeding its maximum or overshooting the target.

This works because the only global condition is the final sum. Any unused extra capacity from one day can always be transferred to another day later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^d) | O(d) | Too slow |
| Optimal | O(d) | O(d) | Accepted |

## Algorithm Walkthrough

1. Read the number of days `d` and the target total `sumTime`.

We need both the daily constraints and the desired final sum before constructing anything.
2. Store all `(minTime, maxTime)` pairs and compute:

```
min_total = sum(minTime[i])
max_total = sum(maxTime[i])
```

These values define the entire achievable range of total study hours.
3. Check whether `sumTime` lies inside this range.

If:

```
sumTime < min_total
```

or

```
sumTime > max_total
```

then print `NO` and stop.

No schedule can possibly satisfy the constraints in those cases.
4. Initialize the schedule using all minimum values.

```
schedule[i] = minTime[i]
```

This already gives a valid schedule with total `min_total`.
5. Compute how many additional hours are still needed.

```
remaining = sumTime - min_total
```
6. Traverse the days one by one.

For each day, calculate how many extra hours can still be added:

```
extra = maxTime[i] - minTime[i]
```

Add:

```
add = min(remaining, extra)
```

to the current day.

This greedily pushes the schedule toward the target while always staying valid.
7. Decrease `remaining` by the amount added.

Eventually `remaining` becomes zero, meaning the total sum is correct.
8. Print `YES` and the constructed schedule.

## Python Solution

```python
import sys
input = sys.stdin.readline

d, sumTime = map(int, input().split())

days = []
min_total = 0
max_total = 0

for _ in range(d):
    mn, mx = map(int, input().split())
    days.append((mn, mx))
    min_total += mn
    max_total += mx

if sumTime < min_total or sumTime > max_total:
    print("NO")
    sys.exit()

schedule = [mn for mn, mx in days]
remaining = sumTime - min_total

for i in range(d):
    mn, mx = days[i]

    extra_capacity = mx - mn
    add = min(remaining, extra_capacity)

    schedule[i] += add
    remaining -= add

print("YES")
print(*schedule)
```

The first part reads all intervals and computes the minimum and maximum achievable totals. That immediately tells us whether a solution is possible.

The schedule starts with all minimum values because those are always safe. Every day already satisfies its lower bound, so we only need to distribute additional hours.

The greedy distribution works because each day has independent extra capacity. Adding more hours to one day never reduces the validity of another day.

The line:

```
add = min(remaining, extra_capacity)
```

is the critical detail. It prevents two common mistakes at once. We never exceed the target total, and we never exceed the day's maximum limit.

The algorithm does not need backtracking. Once a value is assigned, it never has to be reconsidered.

## Worked Examples

### Example 1

Input:

```
1 48
5 7
```

Initial totals:

| Value | Result |

|---|---|---|

| min_total | 5 |

| max_total | 7 |

| target | 48 |

Since:

```
48 > 7
```

the target is impossible.

Output:

```
NO
```

This example confirms the range check is sufficient to reject impossible cases immediately.

### Example 2

Input:

```
3 10
1 3
2 5
3 8
```

Initial state:

| Day | min | max |
| --- | --- | --- |
| 1 | 1 | 3 |
| 2 | 2 | 5 |
| 3 | 3 | 8 |

We compute:

```
min_total = 1 + 2 + 3 = 6
max_total = 3 + 5 + 8 = 16
```

Since `10` lies inside `[6, 16]`, a solution exists.

Initial schedule:

| Day | Current Value |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Remaining hours:

```
10 - 6 = 4
```

Greedy distribution:

| Day | Extra Capacity | Added | Remaining | Schedule |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | [3, 2, 3] |
| 2 | 3 | 2 | 0 | [3, 4, 3] |
| 3 | 5 | 0 | 0 | [3, 4, 3] |

Final output:

```
YES
3 4 3
```

This trace shows how the greedy method gradually reaches the target without violating any limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | One pass to read input and one pass to construct the schedule |
| Space | O(d) | Stores the intervals and resulting schedule |

With at most 30 days, this solution is easily fast enough. The algorithm performs only a few simple arithmetic operations per day, and memory usage is tiny.

## Test Cases

### Test Case 1

Input:

```
1 0
0 0
```

Expected output:

```
YES
0
```

This checks the smallest possible valid input.

### Test Case 2

Input:

```
2 3
2 5
2 5
```

Expected output:

```
NO
```

The minimum achievable total is already 4, so the target cannot be reached.

### Test Case 3

Input:

```
4 12
3 3
3 3
3 3
3 3
```

Expected output:

```
YES
3 3 3 3
```

Every value is fixed, so the algorithm must recognize the only possible schedule.

### Test Case 4

Input:

```
5 20
0 8
0 8
0 8
0 8
0 8
```

Expected output:

```
YES
8 8 4 0 0
```

Any valid distribution works. This case checks whether the greedy allocation handles large remaining values correctly.

## Edge Cases

Consider the impossible lower-bound case:

```
2 3
2 5
2 5
```

The algorithm computes:

```
min_total = 4
max_total = 10
```

Since the target `3` is smaller than `4`, it immediately prints:

```
NO
```

No schedule construction even begins, which avoids invalid negative adjustments later.

Now consider the exact minimum boundary:

```
3 6
1 4
2 5
3 7
```

The algorithm starts with:

```
schedule = [1, 2, 3]
remaining = 0
```

Since no additional hours are needed, the greedy loop adds nothing. The final answer remains:

```
1 2 3
```

This confirms the algorithm does not accidentally modify already-correct schedules.

For the exact maximum boundary:

```
2 10
3 5
4 5
```

We get:

```
min_total = 7
remaining = 3
```

The first day can accept 2 extra hours, producing:

```
5 4
remaining = 1
```

The second day accepts the final extra hour:

```
5 5
remaining = 0
```

The constructed schedule reaches the maximum total exactly.

Finally, the single-day case:

```
1 6
5 7
```

The initial schedule is `[5]` with:

```
remaining = 1
```

The only day has capacity for 2 more hours, so the algorithm adds 1 and produces:

```
6
```

This confirms the greedy logic also works when there is only one interval.
