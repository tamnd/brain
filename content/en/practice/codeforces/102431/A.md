---
title: "CF 102431A - Kick Start"
description: "For each test case, we have the 2019 schedule of Kick Start rounds and a date representing today. The scheduled dates can appear in any order. We need to find the scheduled date that comes strictly after today and is as early as possible."
date: "2026-08-08T17:14:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102431
codeforces_index: "A"
codeforces_contest_name: "2019 China Collegiate Programming Contest Final (CCPC-Final 2019)"
rating: 0
weight: 102431
solve_time_s: 194
verified: true
draft: false
---

[CF 102431A - Kick Start](https://codeforces.com/problemset/problem/102431/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we have the 2019 schedule of Kick Start rounds and a date representing today. The scheduled dates can appear in any order. We need to find the scheduled date that comes strictly after today and is as early as possible. If every scheduled round is today or earlier, there is no remaining round in 2019, so the required answer is `See you next year`.

The dates use month names such as `Jan`, `Feb`, and `Sept`, followed by ordinal day numbers such as `1st`, `22nd`, or `31st`. Since every date belongs to 2019, comparing two dates only requires comparing their month and day. We can convert each date into a pair `(month_number, day)` and use ordinary lexicographic comparison.

There are at most 20 scheduled rounds in one test case and at most 100 test cases. This is a very small input size, so even an approach that performs several hundred or a few thousand simple operations per test case is comfortably fast. In particular, there is no need for advanced data structures or a sophisticated sorting algorithm. A direct scan through the scheduled dates takes only `O(n)` time, where `n <= 20`.

The main boundary condition is that today itself must not be considered the next round. For example, if the schedule contains `Jan 2nd` and today is `Jan 2nd`, the answer is not `Jan 2nd`. If there is no later date, the correct result is `See you next year`.

A second edge case occurs when the next round is in a later month. For example:

```
1
2
Jan 31st
Feb 1st
Jan 31st
```

The correct output is:

```
Case #1: Feb 1st
```

A comparison based only on the day number would incorrectly prefer `Jan 31st` or fail to order the dates properly. The month must be part of the comparison.

A third edge case occurs when today is after every scheduled round. For example:

```
1
2
Jan 10th
Mar 20th
Dec 31st
```

The correct output is:

```
Case #1: See you next year
```

A careless implementation might return the last date it examined instead of explicitly checking whether a later round exists.

The input statement guarantees that scheduled dates are distinct, so two scheduled rounds cannot occupy the same date. The date representing today, however, may equal one of the scheduled dates, and that equality must be excluded because the problem asks for a strictly later round.

## Approaches

The most direct brute-force approach is to inspect every calendar date after today, starting with tomorrow, until the end of 2019. For each candidate date, we can scan all scheduled rounds and check whether that candidate is present. The first matching date is the answer. This works because dates are naturally ordered and the first scheduled date encountered after today must be the earliest possible one.

With at most 365 days in a year and at most 20 scheduled rounds, this performs at most about `365 * 20 = 7300` date comparisons per test case. Across 100 test cases, that is at most roughly 730,000 comparisons, which is easily fast enough. So despite being less elegant, this brute-force method is accepted under the given constraints.

A cleaner approach comes from observing that we do not actually need to enumerate the calendar. For every scheduled date, we can ask one question: is this date strictly later than today? If it is, it is a candidate. Among all candidates, we keep the smallest one. This immediately reduces the problem to a single scan of the `n` scheduled dates.

The comparison becomes simple after converting a date into `(month, day)`. For example, `Mar 24th` becomes `(3, 24)`, while `Apr 20th` becomes `(4, 20)`. Python compares tuples lexicographically, so `(4, 20)` is correctly considered later than `(3, 24)`.

The brute-force method works because the calendar has a tiny fixed number of days, but it performs work on dates that are not even scheduled. The direct scan avoids that unnecessary work entirely. Since `n` is only 20, the optimal solution is simply to examine each scheduled round once and maintain the earliest valid candidate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(365n)` | `O(n)` | Accepted, but unnecessary work |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Store the month names in chronological order by assigning `Jan` to 1, `Feb` to 2, and so on. The input uses `Sept`, so that exact spelling must be included in the mapping.
2. Convert today's date into a pair `(month, day)`. A date represented this way can be compared directly with another date because the month is the first component and the day is the second.
3. Read each of the `n` scheduled dates and convert it into the same `(month, day)` representation. Keep the original text as well, because the output must use the original ordinal formatting such as `Feb 2nd`.
4. For every scheduled date, check whether its `(month, day)` pair is strictly greater than today's pair. Strict comparison is required because a round occurring today is not a future round.
5. Among all dates that are strictly later than today, keep the one with the smallest date pair. This is exactly the next scheduled round, because every earlier candidate has already been rejected or replaced by a later one, while the smallest remaining candidate is the first scheduled date after today.
6. If no scheduled date was strictly later than today, print `See you next year`. Otherwise, print the original text of the selected scheduled date.

### Why it works

Maintain the invariant that after processing any prefix of the schedule, `best` is the earliest scheduled date in that prefix that occurs strictly after today. When a new date is not later than today, it cannot be the answer and is ignored. When it is later than today, it becomes `best` if no earlier candidate exists, or replaces `best` if it occurs before the current candidate. After all scheduled dates have been processed, the invariant says that `best` is the earliest scheduled round after today. If no candidate was ever found, no scheduled round occurs after today, so `See you next year` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MONTH = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sept": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

def parse_date(s):
    month, day = s.split()
    day = int(day.rstrip("stndrh"))
    return MONTH[month], day

def solve():
    t = int(input())

    for case in range(1, t + 1):
        n = int(input())

        schedule = []
        for _ in range(n):
            s = input().strip()
            schedule.append((parse_date(s), s))

        today_text = input().strip()
        today = parse_date(today_text)

        best_date = None
        best_text = None

        for date, text in schedule:
            if date > today:
                if best_date is None or date < best_date:
                    best_date = date
                    best_text = text

        if best_text is None:
            answer = "See you next year"
        else:
            answer = best_text

        print(f"Case #{case}: {answer}")

if __name__ == "__main__":
    solve()
```

The `MONTH` dictionary converts the textual month abbreviation into its chronological position. This avoids trying to compare strings such as `Apr` and `Feb`, whose alphabetical order is unrelated to calendar order.

`parse_date` separates the month and ordinal day. Removing the ordinal suffix leaves an integer day, so `2nd` becomes `2` and `24th` becomes `24`. The suffix is not semantically relevant to date comparison.

Each schedule entry stores both its normalized date pair and its original text. The normalized pair is used for comparisons, while the original string is returned directly so that the output preserves the required spelling and ordinal suffix.

The condition `date > today` is the critical boundary check. Using `>=` would incorrectly select today's round when today is itself a scheduled date. The second condition compares candidates and keeps the smallest one, which implements the definition of the next round.

There is no integer overflow issue because the largest values involved are a month number of 12 and a day number of 31. The input is also tiny, so standard `sys.stdin.readline` is already more than sufficient for the required I/O volume.

## Worked Examples

For the first sample, the schedule is `Jan 1st`, `Feb 2nd`, and `Mar 3rd`, while today is `Jan 2nd`.

| Scheduled date | Parsed date | Later than today? | Current best |
| --- | --- | --- | --- |
| `Jan 1st` | `(1, 1)` | No | None |
| `Feb 2nd` | `(2, 2)` | Yes | `Feb 2nd` |
| `Mar 3rd` | `(3, 3)` | Yes | `Feb 2nd` |

The first date is before today and is discarded. `Feb 2nd` is the first valid candidate. `Mar 3rd` is also in the future, but it is later than the current candidate, so the answer remains `Feb 2nd`.

For the second sample, the scheduled dates are `Mar 24th`, `Apr 20th`, `May 26th`, `Jul 28th`, `Aug 25th`, `Sept 29th`, `Oct 19th`, and `Nov 17th`. Today is `Nov 17th`.

| Scheduled date | Parsed date | Later than today? | Current best |
| --- | --- | --- | --- |
| `Mar 24th` | `(3, 24)` | No | None |
| `Apr 20th` | `(4, 20)` | No | None |
| `May 26th` | `(5, 26)` | No | None |
| `Jul 28th` | `(7, 28)` | No | None |
| `Aug 25th` | `(8, 25)` | No | None |
| `Sept 29th` | `(9, 29)` | No | None |
| `Oct 19th` | `(10, 19)` | No | None |
| `Nov 17th` | `(11, 17)` | No | None |

Every scheduled date is today or earlier. The candidate therefore remains empty, producing `See you next year`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` per test case | Each scheduled round is parsed and examined once |
| Space | `O(n)` | The schedule is stored together with its original text |

With `n <= 20` and at most 100 test cases, the algorithm performs only a few thousand date comparisons in total. The memory usage is also tiny because each test case stores at most 20 schedule entries.

## Test Cases

```python
import sys
import io

MONTH = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sept": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

def parse_date(s):
    month, day = s.split()
    day = int(day.rstrip("stndrh"))
    return MONTH[month], day

def solve():
    input = sys.stdin.readline
    t = int(input())

    out = []

    for case in range(1, t + 1):
        n = int(input())

        schedule = []
        for _ in range(n):
            s = input().strip()
            schedule.append((parse_date(s), s))

        today = parse_date(input().strip())

        best_date = None
        best_text = None

        for date, text in schedule:
            if date > today:
                if best_date is None or date < best_date:
                    best_date = date
                    best_text = text

        if best_text is None:
            answer = "See you next year"
        else:
            answer = best_text

        out.append(f"Case #{case}: {answer}")

    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Sample 1
assert run(
    """1
3
Jan 1st
Feb 2nd
Mar 3rd
Jan 2nd
"""
) == "Case #1: Feb 2nd\n"

# Sample 2
assert run(
    """1
8
Mar 24th
Apr 20th
May 26th
Jul 28th
Aug 25th
Sept 29th
Oct 19th
Nov 17th
Nov 17th
"""
) == "Case #1: See you next year\n"

# Minimum-size input, with today equal to the only scheduled round
assert run(
    """1
1
Jan 1st
Jan 1st
"""
) == "Case #1: See you next year\n"

# Boundary between months, catches day-only comparison mistakes
assert run(
    """1
2
Jan 31st
Feb 1st
Jan 31st
"""
) == "Case #1: Feb 1st\n"

# Today is the earliest date, so the next round is the minimum
# scheduled date strictly after today
assert run(
    """1
4
Dec 31st
Feb 1st
Jan 2nd
Jun 15th
Jan 1st
"""
) == "Case #1: Jan 2nd\n"

# Maximum-size schedule with all 20 scheduled dates distinct
assert run(
    """1
20
Jan 1st
Jan 2nd
Jan 3rd
Jan 4th
Jan 5th
Jan 6th
Jan 7th
Jan 8th
Jan 9th
Jan 10th
Jan 11th
Jan 12th
Jan 13th
Jan 14th
Jan 15th
Jan 16th
Jan 17th
Jan 18th
Jan 19th
Jan 20th
Jan 10th
"""
) == "Case #1: Jan 11th\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1`, scheduled `Jan 1st`, today `Jan 1st` | `See you next year` | Minimum size and strict inequality |
| `Jan 31st`, `Feb 1st`, today `Jan 31st` | `Feb 1st` | Correct month ordering at a month boundary |
| Four unsorted dates, today `Jan 1st` | `Jan 2nd` | Selecting the smallest future date rather than the first input date |
| Twenty distinct January dates, today `Jan 10th` | `Jan 11th` | Maximum `n` and correct linear scan |
| Multiple tests in one input | Corresponding `Case #x` lines | Independent processing and case numbering |

The phrase "all-equal values" requires a small qualification for this problem. Scheduled dates are guaranteed to be distinct, so a test case cannot legally contain several identical scheduled dates. The closest valid equality case is when today's date equals a scheduled date, as in the minimum-size test above. That case is more useful here because it directly tests the strict `>` condition.

## Edge Cases

When today is itself a scheduled date, the algorithm rejects it because the condition requires `date > today`. For example:

```
1
2
Jan 2nd
Feb 2nd
Jan 2nd
```

`Jan 2nd` compares equal to today, so it is ignored. `Feb 2nd` is later and becomes the candidate. The output is:

```
Case #1: Feb 2nd
```

When a future date crosses a month boundary, both components of the normalized pair matter. For:

```
1
2
Jan 31st
Feb 1st
Jan 31st
```

the dates become `(1, 31)` and `(2, 1)`. Since the month is compared first, `(2, 1)` is later. The answer is `Feb 1st`, even though its day number is smaller.

When every scheduled date is earlier than today, no candidate is ever stored. For:

```
1
3
Jan 10th
Jun 20th
Nov 30th
Dec 31st
```

all three dates fail the `date > today` test. `best_text` remains `None`, so the algorithm prints:

```
Case #1: See you next year
```

When the schedule is not sorted, the algorithm does not rely on input order. Consider:

```
1
4
Dec 31st
Feb 1st
Jan 2nd
Jun 15th
Jan 1st
```

The candidates appear in the order `Dec 31st`, `Feb 1st`, `Jan 2nd`, and `Jun 15th`. After seeing `Dec 31st`, it becomes the current best. `Feb 1st` replaces it, and `Jan 2nd` replaces it again. The final answer is `Jan 2nd`. This is exactly why maintaining the minimum future date is preferable to returning the first future date encountered.

When today is the final day of the year, there cannot be a later date in 2019. For example:

```
1
1
Dec 31st
Dec 31st
```

the only scheduled date is equal to today, so it is excluded and the output is:

```
Case #1: See you next year
```

The same logic also handles a schedule containing dates from many months without requiring any special case for December. The normalized `(month, day)` representation gives every 2019 date a total chronological ordering, so one comparison rule handles the entire calendar.
