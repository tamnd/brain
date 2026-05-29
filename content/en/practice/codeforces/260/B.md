---
title: "CF 260B - Ancient Prophesy"
description: "The input is a long string made only of digits and hyphens. Somewhere inside this string, there may be many substrings that look like dates written in the exact format dd-mm-yyyy. We must find which valid date appears most often as a substring."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 260
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 158 (Div. 2)"
rating: 1600
weight: 260
solve_time_s: 132
verified: true
draft: false
---

[CF 260B - Ancient Prophesy](https://codeforces.com/problemset/problem/260/B)

**Rating:** 1600  
**Tags:** brute force, implementation, strings  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a long string made only of digits and hyphens. Somewhere inside this string, there may be many substrings that look like dates written in the exact format `dd-mm-yyyy`.

We must find which valid date appears most often as a substring. A valid date must satisfy three conditions. The year must be between 2013 and 2015 inclusive. The month must be between 01 and 12. The day must exist inside that month. Since none of these years are leap years, February always has 28 days.

The string length can reach `10^5`, which immediately rules out any algorithm that tries all possible substrings. A string of length `10^5` contains about `5 * 10^9` substrings, far beyond what fits into a 1 second time limit.

The key observation is that every valid date has fixed length 10 because the format is always exactly `dd-mm-yyyy`. That means we only need to inspect substrings of length 10. There are only about `10^5` of them, which is completely manageable.

Several edge cases are easy to mishandle.

A common mistake is accepting malformed dates that only look close to the required format. Consider:

```
1-01-2013
```

This is not valid because the day must use two digits. The correct format requires length exactly 10.

Another subtle case is invalid calendar dates:

```
31-02-2013
```

A naive check that only verifies `1 <= day <= 31` would incorrectly accept this. February 2013 only has 28 days.

Overlapping occurrences also matter. For example:

```
12-12-201312-12-2013
```

The valid date appears twice, and both occurrences must be counted even though the substrings overlap in the original string.

A careless implementation may also forget to validate separators. This input:

```
12/12/2013
```

must not count because the required separators are hyphens.

## Approaches

The brute-force idea is straightforward. Generate every substring, check whether it matches the date format, validate the date, and count occurrences. This works logically because every possible occurrence is examined.

The problem is the number of substrings. A string of length `n` has `O(n^2)` substrings. With `n = 10^5`, that becomes roughly `10^10` checks in the worst case, which is impossible within the time limit.

The structure of the date format changes everything. Every candidate date always has exactly 10 characters. We never need to look at any other substring length.

So instead of checking all substrings, we slide a window of size 10 across the string. For each position, we test whether the current substring has the form:

```
dd-mm-yyyy
```

and whether the numbers describe a real date.

This reduces the problem to about `10^5` checks, each taking constant time. We can store counts in a hash map and keep track of the most frequent valid date.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Prepare an array containing the number of days in each month.
3. Create a hash map `cnt` that stores how many times each valid date appears.
4. Iterate through every substring of length 10.
5. For the current substring, first check the format itself.

The third and sixth characters must be `'-'`. Every other position must contain digits. Reject immediately if this fails.
6. Extract day, month, and year as integers.

Since the format is fixed, slicing is simple:

`day = s[0:2]`

`month = s[3:5]`

`year = s[6:10]`
7. Validate the year.

It must be between 2013 and 2015 inclusive.
8. Validate the month.

It must be between 1 and 12.
9. Validate the day.

The day must be at least 1 and at most the number of days in that month.
10. If the date is valid, increment its frequency in the hash map.
11. Track the date with maximum frequency while processing.
12. Print the most frequent valid date.

### Why it works

Every valid occurrence in the string must occupy exactly 10 consecutive characters because the format is fixed. The algorithm checks every such substring exactly once, so no valid occurrence can be missed.

The validation rules exactly match the definition of a correct date. Invalid formats, impossible calendar dates, and years outside the allowed range are all rejected.

Since every valid occurrence increments its counter once, the stored frequencies are correct. The date with maximum frequency at the end is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid_date(t):
    if t[2] != '-' or t[5] != '-':
        return False

    for i in range(10):
        if i in (2, 5):
            continue
        if not t[i].isdigit():
            return False

    day = int(t[0:2])
    month = int(t[3:5])
    year = int(t[6:10])

    if year < 2013 or year > 2015:
        return False

    if month < 1 or month > 12:
        return False

    days_in_month = [
        31, 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ]

    if day < 1 or day > days_in_month[month - 1]:
        return False

    return True

def solve():
    s = input().strip()

    cnt = {}
    best_date = ""
    best_freq = 0

    for i in range(len(s) - 9):
        cur = s[i:i + 10]

        if valid_date(cur):
            cnt[cur] = cnt.get(cur, 0) + 1

            if cnt[cur] > best_freq:
                best_freq = cnt[cur]
                best_date = cur

    print(best_date)

solve()
```

The solution is built around the fixed length of the date format. The loop only examines substrings of size 10, which keeps the runtime linear.

The `valid_date` function separates formatting checks from calendar checks. First it verifies that positions 2 and 5 contain hyphens. Then it confirms every remaining character is a digit. This prevents conversion errors and rejects malformed strings early.

The month lengths are stored in a simple array indexed by `month - 1`. Since the problem guarantees no leap years, February always contains 28 days.

The loop condition uses `range(len(s) - 9)` because a substring of length 10 starting at index `i` ends at `i + 9`. Using `len(s) - 10` would miss the final candidate substring.

The frequency update happens before comparing against the current maximum. This matters because the first occurrence should count as frequency 1 immediately.

## Worked Examples

### Example 1

Input:

```
777-444---21-12-2013-12-2013-12-2013---444-777
```

| Position | Substring | Valid | Count After Update |
| --- | --- | --- | --- |
| 10 | 21-12-2013 | Yes | 1 |
| 16 | 2013-12-2 | No | - |
| 19 | 3-12-2013 | No | - |
| 20 | -12-2013- | No | - |
| 21 | 12-12-2013 | Yes | 1 |
| 24 | 12-2013-12 | No | - |
| 32 | 12-12-2013 | Yes | 2 |

The date `12-12-2013` appears twice, while every other valid date appears fewer times. The algorithm correctly tracks frequencies even when invalid substrings appear nearby.

### Example 2

Input:

```
01-01-201331-02-201301-01-2013
```

| Position | Substring | Valid | Reason |
| --- | --- | --- | --- |
| 0 | 01-01-2013 | Yes | Real calendar date |
| 10 | 31-02-2013 | No | February has only 28 days |
| 20 | 01-01-2013 | Yes | Real calendar date |

The invalid February date is rejected even though it matches the textual format. The valid date appears twice and becomes the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each length-10 substring is checked once |
| Space | O(n) | Hash map may store many distinct valid dates |

The algorithm performs constant work for every starting position in the string. With at most `10^5` positions, the runtime easily fits within the limit. The memory usage is also small because the number of distinct valid dates is bounded.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()

    def valid_date(t):
        if t[2] != '-' or t[5] != '-':
            return False

        for i in range(10):
            if i in (2, 5):
                continue
            if not t[i].isdigit():
                return False

        day = int(t[0:2])
        month = int(t[3:5])
        year = int(t[6:10])

        if year < 2013 or year > 2015:
            return False

        if month < 1 or month > 12:
            return False

        days = [31, 28, 31, 30, 31, 30,
                31, 31, 30, 31, 30, 31]

        return 1 <= day <= days[month - 1]

    cnt = {}
    ans = ""
    best = 0

    for i in range(len(s) - 9):
        cur = s[i:i + 10]

        if valid_date(cur):
            cnt[cur] = cnt.get(cur, 0) + 1

            if cnt[cur] > best:
                best = cnt[cur]
                ans = cur

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    global input
    input = sys.stdin.readline

    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run(
    "777-444---21-12-2013-12-2013-12-2013---444-777\n"
) == "13-12-2013", "sample 1"

# minimum valid input
assert run(
    "01-01-2013\n"
) == "01-01-2013", "single valid date"

# invalid date mixed with valid ones
assert run(
    "31-02-201301-03-2013\n"
) == "01-03-2013", "reject impossible February date"

# overlapping occurrences
assert run(
    "01-01-201301-01-2013\n"
) == "01-01-2013", "count overlapping occurrences"

# boundary year checks
assert run(
    "31-12-201231-12-201501-01-2016\n"
) == "31-12-2015", "only years 2013-2015 allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `01-01-2013` | `01-01-2013` | Smallest meaningful valid case |
| `31-02-201301-03-2013` | `01-03-2013` | Invalid calendar dates are rejected |
| `01-01-201301-01-2013` | `01-01-2013` | Overlapping occurrences are counted |
| `31-12-201231-12-201501-01-2016` | `31-12-2015` | Year bounds are enforced correctly |

## Edge Cases

Consider the input:

```
1-01-2013
```

The algorithm never even checks this as a candidate because its length is only 9. Every examined substring must have length exactly 10. This correctly rejects dates without leading zeroes.

Now consider:

```
31-02-2013
```

The substring passes the formatting test because the hyphens are in the right positions and all remaining characters are digits. Then the algorithm extracts `day = 31` and `month = 2`. Since February has 28 days, the condition:

```
day > days_in_month[month - 1]
```

becomes true, so the substring is rejected.

Another tricky input is:

```
01-01-201301-01-2013
```

The second occurrence starts before the first occurrence is completely separated from the string. The sliding window still visits every starting position independently, so both occurrences are counted correctly.

Finally, consider:

```
12/12/2013
```

The substring fails immediately because positions 2 and 5 are not hyphens. The algorithm never attempts integer conversion on malformed formats.
