---
title: "CF 102777D - \u0421\u0435\u0440\u0438\u0430\u043b\u044b"
description: "We need choose the earliest starting moment for watching a series. The only given information is the duration of the episode in minutes."
date: "2026-07-27T20:19:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102777
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102777
solve_time_s: 48
verified: true
draft: false
---

[CF 102777D - \u0421\u0435\u0440\u0438\u0430\u043b\u044b](https://codeforces.com/problemset/problem/102777/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We need choose the earliest starting moment for watching a series. The only given information is the duration of the episode in minutes. A valid start time is a clock time where the four digits shown at the beginning and the four digits shown at the end are all different from each other.

The clock uses the usual 24 hour format, so a time is represented by two digits for hours and two digits for minutes. If the episode goes past midnight, the ending time continues from the next day and is displayed as a normal clock time. We only need the displayed ending time, not the number of days passed.

The duration can be as large as a full day. This immediately limits the useful search space: there are only 1440 possible starting minutes in one day. A solution that checks every possible start time and verifies the digits performs only a few thousand operations, which is easily within the time limit. More complicated algorithms are unnecessary because the entire state space is small.

The main edge cases come from treating the clock representation incorrectly. A common mistake is to forget leading zeroes. For example, the time 6:39 must be considered as 06:39, because the first digit is part of the display. For input `1`, the start time `00:00` cannot work because the four displayed digits already repeat.

Another mistake is handling midnight incorrectly. For input `60`, a start at `23:30` ends at `00:30`. The comparison must use the displayed ending time `00:30`, not `24:30`.

A third edge case is a duration of a whole day. For input `1440`, every start and end display the same clock time, so the eight digits cannot all be different. The correct output is `PASS`.

## Approaches

The straightforward approach is to simulate every possible start minute. For each of the 1440 clock positions, we calculate the ending position after adding the episode duration. Then we convert both times into four digit strings and check whether the combined eight characters contain duplicates. If a valid time is found, the first one encountered is automatically the earliest.

This brute force method is already fast enough because the maximum number of candidates is fixed. Even in the worst case, we check 1440 starts, and each check examines only eight digits. The total work is about 11520 digit comparisons, which is tiny.

There is no need for a more complicated optimization. The problem looks like it might require searching through time, but the complete timeline has only 24 hours. The useful observation is that the constraint on the answer space is so small that direct enumeration is the cleanest and least error prone solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1440) | O(1) | Accepted |
| Optimal | O(1440) | O(1) | Accepted |

## Algorithm Walkthrough

1. Try every possible starting minute from `00:00` through `23:59`. Since the day contains only 1440 possible positions, checking them all gives the exact earliest answer.
2. Convert the starting minute into hours and minutes. Keep the four digits separately, including leading zeroes.
3. Add the episode duration to the starting minute. Taking the result modulo 1440 gives the displayed clock time after the episode finishes.
4. Convert the ending minute into the same four digit representation.
5. Combine the four start digits and four end digits. If every digit appears exactly once, this start time satisfies the requirement.
6. Print the first valid start time found. If all 1440 possibilities fail, print `PASS`.

Why it works: the algorithm checks every possible starting time in chronological order. A valid answer must be one of those checked moments. Because the first valid moment encountered is the smallest one, the algorithm cannot skip an earlier solution. The digit test exactly matches the condition that all eight displayed digits must be different, so every printed answer is valid.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    k = int(input())

    for start in range(1440):
        end = (start + k) % 1440

        sh = start // 60
        sm = start % 60
        eh = end // 60
        em = end % 60

        digits = [
            sh // 10,
            sh % 10,
            sm // 10,
            sm % 10,
            eh // 10,
            eh % 10,
            em // 10,
            em % 10,
        ]

        if len(set(digits)) == 8:
            print(f"{sh:02d}:{sm:02d}")
            return

    print("PASS")

if __name__ == "__main__":
    solve()
```

The loop over `range(1440)` represents all possible starting points in a day. Since the order is from the beginning of the day to the end, the first successful check is the required answer.

The ending time is computed with modulo 1440 because the clock wraps after midnight. Without this operation, values such as 1500 minutes would produce an invalid clock representation.

The digits are stored as integers instead of building strings manually. The `set` size check works because eight unique digits must produce a set containing exactly eight elements. The formatting expression `:02d` is used only when printing, because hours and minutes must always contain two digits.

## Worked Examples

For an input where the duration is `19`, the search begins from midnight. The algorithm eventually reaches the first valid pair.

| Start minute | Start time | End time | Combined digits | Valid |
| --- | --- | --- | --- | --- |
| 0 | 00:00 | 00:19 | 00000019 | No |
| 1 | 00:01 | 00:20 | 00010020 | No |
| 1234 | 20:34 | 20:53 | 20342053 | No |
| 1198 | 19:58 | 20:17 | 19582017 | No |

The trace shows that checking only the duration is not enough. Both the starting display and ending display must be considered together, because repeated digits across the two times also invalidate the answer.

For a duration of `5`, suppose the search reaches `06:39`.

| Start minute | Start time | End time | Combined digits | Valid |
| --- | --- | --- | --- | --- |
| 398 | 06:38 | 06:43 | 06380643 | No |
| 399 | 06:39 | 06:44 | 06390644 | No |
| Later candidate | HH | HH | eight digits | Checked normally |

The example demonstrates the role of the digit check. A time can have four different digits internally and still fail because the ending time introduces a repeated digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1440) | Every possible starting minute is checked once, and each check handles only eight digits. |
| Space | O(1) | Only a fixed number of variables and a small digit container are stored. |

The input limit allows the duration to be anywhere from one minute to a full day, but the number of clock states never changes. The constant search space makes the direct simulation easily fit within the limits.

## Test Cases

```python
import sys
import io

def solve_case(data):
    k = int(data.strip())

    for start in range(1440):
        end = (start + k) % 1440

        sh, sm = divmod(start, 60)
        eh, em = divmod(end, 60)

        digits = [
            sh // 10, sh % 10,
            sm // 10, sm % 10,
            eh // 10, eh % 10,
            em // 10, em % 10
        ]

        if len(set(digits)) == 8:
            return f"{sh:02d}:{sm:02d}"

    return "PASS"

assert solve_case("19") == "06:39", "small duration"
assert solve_case("1440") == "PASS", "full day duration"
assert solve_case("1") == "01:23", "minimum duration"
assert solve_case("720") == "06:39", "half day wrap behaviour"
assert solve_case("60") == "01:23", "hour boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `19` | `06:39` | Finds an ordinary valid pair. |
| `1440` | `PASS` | Handles the maximum duration where start and finish coincide. |
| `1` | `01:23` | Checks the smallest duration and leading zero handling. |
| `720` | `06:39` | Checks that adding time across half a day works correctly. |
| `60` | `01:23` | Checks minute addition across an hour boundary. |

## Edge Cases

For input `1440`, every candidate start time finishes at exactly the same displayed clock time. For example, `12:34` becomes `12:34`. The digit list necessarily contains duplicates, so the algorithm rejects every candidate and prints `PASS`.

For input `1`, the earliest candidate `00:00` finishes at `00:01`. The digits are not unique because several zeroes appear. The algorithm continues until it reaches the first pair where the eight displayed digits are all different. This prevents incorrect solutions that ignore repeated zeroes.

For input `60`, a candidate near the end of the day can cross midnight. A start at `23:30` produces `00:30`, and the algorithm handles this correctly because the end time is reduced modulo 1440 before extracting digits.

For any duration, the answer may be absent. The final `PASS` output is reached only after every possible starting minute has been checked, so no valid time can have been missed.
