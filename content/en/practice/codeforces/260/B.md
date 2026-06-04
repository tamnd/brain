---
title: "CF 260B - Ancient Prophesy"
description: "The input is a long string consisting only of digits and the character -. Somewhere inside this string there may be many substrings that look like dates written exactly as dd-mm-yyyy. Our task is to find the valid date that appears most often as such a substring."
date: "2026-06-04T17:41:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 260
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 158 (Div. 2)"
rating: 1600
weight: 260
solve_time_s: 130
verified: true
draft: false
---

[CF 260B - Ancient Prophesy](https://codeforces.com/problemset/problem/260/B)

**Rating:** 1600  
**Tags:** brute force, implementation, strings  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a long string consisting only of digits and the character `-`. Somewhere inside this string there may be many substrings that look like dates written exactly as `dd-mm-yyyy`.

Our task is to find the valid date that appears most often as such a substring. A valid date must satisfy three conditions:

First, the format must be exactly two digits for the day, two digits for the month, and four digits for the year, separated by hyphens.

Second, the year must be one of `2013`, `2014`, or `2015`.

Third, the day must be valid for the given month. Since none of these years are leap years, February has 28 days.

The answer is guaranteed to exist and to be unique.

The string length is at most `10^5`. A substring representing a date always has length `10`, so there are at most about `10^5` candidate positions to examine. This immediately suggests that scanning all possible length-10 substrings is feasible. Any solution that tries to compare every candidate against every other candidate would drift toward quadratic behavior and become too slow.

The subtle part is that a substring may look like a date syntactically while being invalid. For example:

```
31-02-2013
```

This matches the pattern `dd-mm-yyyy`, but February never has 31 days, so it must not be counted.

Another easy mistake is accepting dates that do not use exactly two digits for day and month. Consider:

```
1-01-2013
```

This is not a valid occurrence because the required format is exactly ten characters long. Only:

```
01-01-2013
```

counts.

A third pitfall is month-specific day limits. For example:

```
31-04-2014
```

April has only 30 days. A solution that merely checks `1 <= day <= 31` would incorrectly count it.

Finally, overlapping occurrences are allowed. In the string

```
0012-10-2012-10-2012
```

different starting positions can produce valid date substrings. We must examine every length-10 window independently.

## Approaches

A brute-force idea is to generate every valid date between 2013 and 2015 and search the entire prophecy for each one.

There are only about a thousand valid dates in that range, so correctness is straightforward. For each date, count how many times its string representation appears in the prophecy and keep the maximum.

The problem is the running time. The prophecy can contain `10^5` characters. Searching for roughly 1000 dates independently leads to around `10^8` character operations in the worst case, which is unnecessarily expensive.

The structure of the problem suggests turning the process around.

Instead of asking, "How many times does each valid date occur?", we can ask, "What date does each length-10 substring represent?"

Every valid occurrence must occupy exactly ten characters:

```
dd-mm-yyyy
```

There are only `n - 9` such windows in the entire string. For each window we can check whether it forms a valid date. If it does, we increment that date's frequency.

This transforms the problem into a single linear scan of the prophecy. Each position is processed once, validity checks take constant time, and a hash map stores frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000·n) | O(1) | Too slow |
| Optimal | O(n) | O(k) | Accepted |

Here `k` is the number of distinct valid dates encountered, which is at most the number of valid dates between 2013 and 2015.

## Algorithm Walkthrough

1. Read the prophecy string.
2. Prepare an array containing the number of days in each month:

```
[31,28,31,30,31,30,31,31,30,31,30,31]
```

Since years 2013 through 2015 are not leap years, February always has 28 days.
3. Iterate over every starting position `i` such that a length-10 substring exists.
4. Extract the substring `s[i:i+10]`.
5. Check whether positions 2 and 5 contain hyphens.

If they do not, the substring cannot match the required format.
6. Parse:

- day from characters `[0:2]`
- month from characters `[3:5]`
- year from characters `[6:10]`

If parsing fails, discard the substring.
7. Verify the date:

- year is between 2013 and 2015
- month is between 1 and 12
- day is at least 1
- day does not exceed the number of days in that month
8. If the date is valid, increment its count in a hash map using the original substring as the key.
9. Track the date with the highest frequency seen so far.
10. After processing all windows, output the date with the maximum count.

### Why it works

Every valid occurrence in the prophecy occupies exactly ten consecutive characters and must be represented by some length-10 window. The algorithm examines every such window exactly once.

A substring contributes to the frequency map only if it passes all validity checks, so every counted occurrence corresponds to a correct date. Conversely, every correct date occurrence appears as one of the examined windows and will be counted.

The frequency map therefore stores the exact number of occurrences of every valid date. Since the apocalypse date is defined as the unique valid date with maximum frequency, selecting the key with the largest count produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    days_in_month = [31, 28, 31, 30, 31, 30,
                     31, 31, 30, 31, 30, 31]

    freq = {}
    best_date = ""
    best_count = 0

    for i in range(len(s) - 9):
        cur = s[i:i + 10]

        if cur[2] != '-' or cur[5] != '-':
            continue

        try:
            day = int(cur[0:2])
            month = int(cur[3:5])
            year = int(cur[6:10])
        except ValueError:
            continue

        if not (2013 <= year <= 2015):
            continue

        if not (1 <= month <= 12):
            continue

        if not (1 <= day <= days_in_month[month - 1]):
            continue

        freq[cur] = freq.get(cur, 0) + 1

        if freq[cur] > best_count:
            best_count = freq[cur]
            best_date = cur

    print(best_date)

if __name__ == "__main__":
    solve()
```

The scan examines every possible length-10 window because any valid date occurrence must occupy exactly ten characters.

The hyphen check is performed before parsing integers. This quickly rejects most invalid windows and avoids unnecessary conversions.

The month validity check comes before indexing `days_in_month[month - 1]`. Reversing this order would risk accessing an invalid index when the month is outside the range `1..12`.

The original substring is used as the dictionary key. Since dates are always stored in canonical `dd-mm-yyyy` format, identical dates always produce identical keys.

The running maximum is updated during the scan, avoiding a second pass over the frequency map.

## Worked Examples

### Example 1

Input:

```
777-444---21-12-2013-12-2013-12-2013---444-777
```

Relevant valid windows:

| Window | Valid? | Count After Update |
| --- | --- | --- |
| 21-12-2013 | Yes | 1 |
| 13-12-2013 | Yes | 1 |
| 12-20-1312 | No | - |
| 13-12-2013 | Yes | 2 |
| 13-12-2013 | Yes | 3 |

Final frequencies:

| Date | Frequency |
| --- | --- |
| 21-12-2013 | 1 |
| 13-12-2013 | 3 |

Output:

```
13-12-2013
```

This example shows why every length-10 window must be checked. The winning date appears multiple times due to overlapping positions inside the larger string.

### Example 2

Input:

```
01-01-201331-02-201301-01-2013
```

Trace:

| Window | Valid? | Frequency |
| --- | --- | --- |
| 01-01-2013 | Yes | 1 |
| 31-02-2013 | No | - |
| 01-01-2013 | Yes | 2 |

Output:

```
01-01-2013
```

This example demonstrates the importance of validating month-specific day limits. The middle substring has the correct shape but is not a real calendar date.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each length-10 window is processed once |
| Space | O(k) | Frequency map stores distinct valid dates |

The string length is at most `10^5`, so roughly `10^5` windows are examined. Each window requires only constant-time parsing and validation. The solution comfortably fits within the time limit and uses very little memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    def solve():
        input = sys.stdin.readline
        s = input().strip()

        days = [31, 28, 31, 30, 31, 30,
                31, 31, 30, 31, 30, 31]

        freq = {}
        best_date = ""
        best_count = 0

        for i in range(len(s) - 9):
            cur = s[i:i + 10]

            if cur[2] != '-' or cur[5] != '-':
                continue

            try:
                d = int(cur[:2])
                m = int(cur[3:5])
                y = int(cur[6:])
            except ValueError:
                continue

            if not (2013 <= y <= 2015):
                continue
            if not (1 <= m <= 12):
                continue
            if not (1 <= d <= days[m - 1]):
                continue

            freq[cur] = freq.get(cur, 0) + 1

            if freq[cur] > best_count:
                best_count = freq[cur]
                best_date = cur

        print(best_date)

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue().strip()

# provided sample
assert run(
    "777-444---21-12-2013-12-2013-12-2013---444-777\n"
) == "13-12-2013", "sample"

# single valid date
assert run("01-01-2013\n") == "01-01-2013", "minimum valid case"

# invalid date between two valid occurrences
assert run(
    "01-01-201331-02-201301-01-2013\n"
) == "01-01-2013", "reject invalid February date"

# month boundary
assert run(
    "30-04-201431-04-201430-04-2014\n"
) == "30-04-2014", "April has only 30 days"

# year boundary
assert run(
    "31-12-201231-12-201331-12-2013\n"
) == "31-12-2013", "reject year outside range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `01-01-2013` | `01-01-2013` | Smallest meaningful valid input |
| `01-01-201331-02-201301-01-2013` | `01-01-2013` | Invalid February date is ignored |
| `30-04-201431-04-201430-04-2014` | `30-04-2014` | Month-specific day limits |
| `31-12-201231-12-201331-12-2013` | `31-12-2013` | Year range validation |

## Edge Cases

Consider:

```
31-02-2013
```

The substring has the correct `dd-mm-yyyy` structure. The algorithm parses day `31`, month `2`, and year `2013`. The month is valid, but February allows only `28` days. The condition

```
day <= days_in_month[month - 1]
```

fails, so the substring is discarded and never counted.

Consider:

```
31-04-2014
```

April has `30` days. The algorithm computes `days_in_month[3] = 30`, detects that `31 > 30`, and rejects the date. This prevents counting syntactically correct but impossible calendar dates.

Consider:

```
1-01-2013
```

This string is only nine characters long. Since the algorithm only examines length-10 windows, it never treats this as a candidate date. The required format demands exactly two digits for both day and month.

Consider:

```
13-12-2013-12-2013
```

The substring `13-12-2013` appears at the beginning, and another occurrence begins later due to overlap. Because the algorithm checks every starting position independently, both occurrences are counted correctly. Overlapping matches require no special handling.
