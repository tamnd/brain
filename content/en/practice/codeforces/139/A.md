---
title: "CF 139A - Petr and Book"
description: "Petr has a book with n pages. Starting from Monday, he reads a fixed number of pages each day of the week. The input gives those seven daily reading capacities in order from Monday to Sunday. We need to determine on which day Petr finishes the book."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 139
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 99 (Div. 2)"
rating: 1000
weight: 139
solve_time_s: 86
verified: true
draft: false
---

[CF 139A - Petr and Book](https://codeforces.com/problemset/problem/139/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Petr has a book with `n` pages. Starting from Monday, he reads a fixed number of pages each day of the week. The input gives those seven daily reading capacities in order from Monday to Sunday.

We need to determine on which day Petr finishes the book. The answer is not the total number of days, but the weekday number from `1` to `7`, where `1` means Monday and `7` means Sunday.

The constraints are very small. The number of pages is at most `1000`, and each daily value is also at most `1000`. Even a direct simulation day by day is completely fast enough. In the worst case, Petr reads only one page per week, so the simulation could run for around `1000` days. That is still trivial for a 2-second limit.

The tricky part is not performance, it is handling the stopping condition correctly.

One common mistake is checking whether the remaining pages become exactly zero only after finishing a full week. Consider this input:

```
1
1 0 0 0 0 0 0
```

The correct answer is `1` because Petr finishes on Monday immediately. A careless implementation that loops week by week might accidentally continue into the next week.

Another subtle case happens when some days have zero reading capacity.

```
2
1 0 0 0 0 0 0
```

The correct answer is still `1`. Petr reads page 1 on the first Monday, then page 2 on the second Monday. Days with zero pages must still be processed because Petr does not skip them.

A final off-by-one trap appears when Petr finishes exactly at the end of a day.

```
10
5 5 1 1 1 1 1
```

The answer is `2`, not `3`. After Tuesday, the remaining pages become zero, so Tuesday is the finishing day.

## Approaches

The most direct approach is to simulate Petr's reading process one day at a time. We repeatedly iterate through the seven weekdays, subtracting the number of pages Petr can read on that day from the remaining pages. As soon as the remaining number becomes zero or negative, we return the current weekday.

This works because the process described in the problem is itself sequential. Petr reads in chronological order and never skips days, so simulating exactly what happens naturally produces the correct result.

Since the book has at most `1000` pages, even the slowest possible reading schedule still finishes after a manageable number of iterations. For example, if Petr reads only one page every Monday and zero pages on all other days, the simulation performs about `7000` daily checks. That is tiny.

There is also a slightly cleaner observation. We do not need to count complete weeks explicitly. We only care about the first day where the cumulative number of read pages reaches or exceeds `n`. That means a single repeating traversal over the weekdays is enough.

The brute-force and optimal approaches end up looking very similar because the constraints are small. The optimal version is simply the cleanest simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of simulated days) | O(1) | Accepted |
| Optimal | O(number of simulated days) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the total number of pages `n`.
2. Read the array of seven integers representing how many pages Petr reads from Monday through Sunday.
3. Start an infinite loop over the weekdays because the schedule repeats every week.
4. For each weekday from index `0` to `6`, subtract that day's reading capacity from `n`.
5. After subtracting, check whether `n <= 0`.
6. If the condition is true, return the current weekday number using `index + 1` because the problem uses 1-based numbering.

The reason this works is that the moment `n` becomes non-positive is exactly the moment Petr finishes the final page. Every previous day still left some pages unread.

### Why it works

The algorithm maintains a simple invariant: before processing a day, `n` equals the number of unread pages remaining. After subtracting the current day's reading amount, `n` becomes the remaining unread pages after that day finishes.

The first day where `n <= 0` is precisely the day when the cumulative number of pages read reaches at least the original book size. Since days are processed in chronological order, no earlier day could have finished the book. That guarantees the returned weekday is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    days = list(map(int, input().split()))

    while True:
        for i in range(7):
            n -= days[i]

            if n <= 0:
                print(i + 1)
                return

solve()
```

The program directly follows the simulation described in the algorithm.

The `while True` loop represents repeating weeks. Inside it, the `for` loop iterates through Monday to Sunday in order.

After subtracting the current day's reading amount, we immediately check whether the book is finished. The order matters. If we checked before subtraction, we would incorrectly delay the answer by one day.

The condition uses `n <= 0` instead of `n == 0`. Petr may read more pages than remain in the book on the final day. For example, if `3` pages remain and today's capacity is `10`, the remaining value becomes `-7`, but the finishing day is still today.

The output uses `i + 1` because Python arrays are 0-indexed while the weekdays in the problem are numbered from `1` to `7`.

## Worked Examples

### Sample 1

Input:

```
100
15 20 20 15 10 30 45
```

| Day | Pages Read | Remaining Pages |
| --- | --- | --- |
| Monday | 15 | 85 |
| Tuesday | 20 | 65 |
| Wednesday | 20 | 45 |
| Thursday | 15 | 30 |
| Friday | 10 | 20 |
| Saturday | 30 | -10 |

The remaining pages become non-positive on Saturday, so the answer is `6`.

This trace shows why the algorithm checks `n <= 0` immediately after subtraction. Petr can finish in the middle of a day's reading capacity.

### Sample 2

Input:

```
2
1 0 0 0 0 0 0
```

| Day | Pages Read | Remaining Pages |
| --- | --- | --- |
| Monday | 1 | 1 |
| Tuesday | 0 | 1 |
| Wednesday | 0 | 1 |
| Thursday | 0 | 1 |
| Friday | 0 | 1 |
| Saturday | 0 | 1 |
| Sunday | 0 | 1 |
| Monday | 1 | 0 |

The answer is `1`.

This example demonstrates that the schedule repeats every week and that zero-reading days still count as calendar days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | `k` is the number of simulated days until the book finishes |
| Space | O(1) | Only a few variables are stored |

Even in the worst case, the simulation performs only a few thousand iterations, which is trivial within the given limits. The memory usage is constant because the algorithm stores only the seven weekday values and a few counters.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    days = list(map(int, input().split()))

    while True:
        for i in range(7):
            n -= days[i]

            if n <= 0:
                print(i + 1)
                return

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
    "100\n15 20 20 15 10 30 45\n"
) == "6\n", "sample 1"

# custom cases
assert run(
    "1\n1 0 0 0 0 0 0\n"
) == "1\n", "minimum input"

assert run(
    "10\n5 5 1 1 1 1 1\n"
) == "2\n", "exact finish on Tuesday"

assert run(
    "7\n1 1 1 1 1 1 1\n"
) == "7\n", "all equal values"

assert run(
    "1000\n1000 0 0 0 0 0 0\n"
) == "1\n", "maximum pages finished immediately"

assert run(
    "2\n0 0 0 0 0 0 2\n"
) == "7\n", "finish on Sunday"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0 0 0 0 0 0` | `1` | Minimum-size input |
| `10 / 5 5 1 1 1 1 1` | `2` | Exact finish at end of a day |
| `7 / 1 1 1 1 1 1 1` | `7` | Uniform reading schedule |
| `1000 / 1000 0 0 0 0 0 0` | `1` | Large value handled correctly |
| `2 / 0 0 0 0 0 0 2` | `7` | Correct Sunday indexing |

## Edge Cases

Consider the case where Petr finishes immediately on the first day.

Input:

```
1
1 0 0 0 0 0 0
```

The algorithm subtracts Monday's value from `n`, making `n = 0`. Since `n <= 0`, it immediately returns `1`. This avoids the common mistake of continuing into another day or week.

Now consider a schedule with many zero-reading days.

Input:

```
2
1 0 0 0 0 0 0
```

After the first Monday, one page remains. The algorithm still processes Tuesday through Sunday even though they subtract zero. On the next Monday, the remaining value becomes zero and the algorithm correctly returns `1`.

Finally, consider a case where Petr reads more pages than remain.

Input:

```
3
10 0 0 0 0 0 0
```

After Monday, the remaining pages become `-7`. The algorithm still accepts this because it checks `n <= 0` rather than `n == 0`. The correct answer is `1` because Petr finished during Monday's reading session.
