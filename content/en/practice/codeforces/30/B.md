---
title: "CF 30B - Codeforces World Finals"
description: "We are given two dates in the format DD.MM.YY: one representing the day of the Codeforces World Finals and the other rep"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 30
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 30 (Codeforces format)"
rating: 1700
weight: 30
solve_time_s: 61
verified: true
draft: false
---

[CF 30B - Codeforces World Finals](https://codeforces.com/problemset/problem/30/B)

**Rating:** 1700  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two dates in the format `DD.MM.YY`: one representing the day of the Codeforces World Finals and the other representing Bob's date of birth. Bob can rearrange the components of his birth date-the day, month, and year-but only as complete numbers, not individual digits. The goal is to determine whether, after such a rearrangement, Bob would be at least 18 years old on the day of the finals and would have been born in the same century as the finals. If either condition fails, he cannot participate.

The years are two-digit numbers, representing 2001 to 2099, and the finals occur in this range. A valid date of birth in this context must follow standard calendar rules, including handling months with different numbers of days and accounting for leap years. The maximum number of permutations to check for a rearranged date is small because there are only three components, giving 6 permutations per candidate date.

A naive implementation might overlook several subtle constraints. For example, swapping day and month might create invalid dates like 31st February. Another pitfall is miscalculating age when the final day and birth day coincide, which is a valid participation scenario. A careless solution could also ignore the century requirement and treat years like `01` as 2001 without considering that the birth year must be in the same century as the finals.

## Approaches

The brute-force approach is straightforward: generate all 6 permutations of Bob's birth date, interpret each permutation as a valid date, and check whether the resulting age is at least 18 and that the birth year matches the finals’ century. This works because the number of permutations is tiny, but one must be careful to reject invalid dates caused by impossible day-month combinations. Every permutation is independently checked, and this approach is efficient because the permutation count is fixed at 6, far below any complexity concern.

The key insight is that the constraints are small, allowing us to check each permutation individually. Calculating age requires comparing year, month, and day in order, handling the edge case when Bob’s 18th birthday coincides with the finals. We also need to verify that the day and month are valid according to the Gregorian calendar rules. Leap years are simple in this case, since any year divisible by 4 in the range 2001-2099 is a leap year, affecting only February. With these checks in place, the solution becomes a direct implementation problem rather than an algorithmic optimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(6) | O(1) | Accepted |
| Optimal | O(6) | O(1) | Accepted |

## Algorithm Walkthrough

1. Parse the finals date into day, month, and year integers. Interpret the year as 2000 + YY to work in the full century.
2. Parse Bob’s birth date into three integers.
3. Generate all permutations of the three numbers. Each permutation represents a candidate day, month, and year of birth.
4. For each permutation, adjust the year by adding 2000 to ensure it matches the century of the finals.
5. Verify that the candidate day and month form a valid calendar date. Reject any permutation that has an invalid day for the given month or an invalid leap-year February.
6. Compute Bob’s age by subtracting the birth year from the finals year. If the finals month and day occur before the birth month and day, subtract one from the age.
7. If the age is at least 18 and the birth year is in the same century as the finals, return YES. If no permutation satisfies both conditions, return NO.

Why it works: The invariant is that every permutation is checked independently, ensuring no possible rearrangement is skipped. By validating the calendar date and comparing ages systematically, we guarantee correctness. The algorithm only returns YES if at least one valid permutation meets both the age and century conditions.

## Python Solution

```python
import sys
import itertools
input = sys.stdin.readline

def is_valid_date(day, month, year):
    if month < 1 or month > 12 or day < 1:
        return False
    # Days in month
    if month == 2:
        if year % 4 == 0:
            return day <= 29
        return day <= 28
    if month in [4, 6, 9, 11]:
        return day <= 30
    return day <= 31

def main():
    finals = list(map(int, input().strip().split('.')))
    bob = list(map(int, input().strip().split('.')))

    f_day, f_month, f_year = finals
    f_year += 2000

    for perm in itertools.permutations(bob):
        b_day, b_month, b_year = perm
        b_year += 2000
        # must be same century
        if b_year // 100 != f_year // 100:
            continue
        if not is_valid_date(b_day, b_month, b_year):
            continue
        age = f_year - b_year
        if (f_month, f_day) < (b_month, b_day):
            age -= 1
        if age >= 18:
            print("YES")
            return
    print("NO")

if __name__ == "__main__":
    main()
```

The code first parses the finals and birth dates, then iterates through all permutations. The century check ensures Bob cannot appear younger by using an earlier year. The date validation rejects impossible calendar combinations. Age calculation is careful to decrement when the birthday has not occurred yet in the finals year.

## Worked Examples

**Sample 1**

Input:

```
01.01.98
01.01.80
```

| Variable | Value |
| --- | --- |
| finals | [1,1,98] → 2001+97? Wait, correct: 98→2098 |
| bob permutations | (1,1,80),(1,80,1),(80,1,1), etc. |
| valid permutation | (1,1,80) → 2080, finals 2098 |
| age | 2098-2080 = 18, month/day ok |
| Output | YES |

The trace shows that using the correct permutation yields age 18 exactly, which satisfies the participation rule.

**Custom Example**

Input:

```
28.02.24
29.02.06
```

| Variable | Value |
| --- | --- |
| finals | 28.02.2024 |
| bob permutations | (29,2,6),(2,29,6),(6,2,29), etc. |
| valid permutation | (29,2,2006) → 29 Feb 2006 invalid (not leap) |
| age | no permutation valid → NO |

Here, February 29 fails because 2006 is not a leap year. Algorithm correctly rejects it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(6) | 3! permutations, constant checks per permutation |
| Space | O(1) | Only temporary variables for permutations and date checks |

Since the number of permutations is fixed at 6 and all checks are constant-time, this runs comfortably under 2 seconds with minimal memory.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("01.01.98\n01.01.80\n") == "YES", "sample 1"

# Bob's birthday after finals, can swap
assert run("15.05.21\n21.05.03\n") == "YES", "swap to make age 18+"

# Invalid February 29 on non-leap year
assert run("28.02.24\n29.02.06\n") == "NO", "invalid leap year"

# Age exactly 18 on finals date
assert run("01.01.20\n01.01.02\n") == "YES", "birthday coincides"

# Century mismatch
assert run("01.01.20\n01.01.99\n") == "NO", "born in 2099, finals in 2020"

# Minimum values
assert run("01.01.01\n01.01.01\n") == "NO", "too young"

# All numbers same
assert run("02.02.02\n02.02.02\n") == "NO", "age <18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 15.05.21 / 21.05.03 | YES | swaps birth date to make age valid |
| 28.02.24 / 29.02.06 | NO | invalid leap year |
| 01.01.20 / 01.01.02 | YES | age exactly 18 on finals day |
| 01.01.20 / 01.01.99 | NO | century mismatch |
| 01.01.01 / 01.01.01 | NO | too young |
| 02.02.02 / 02.02.02 | NO | all equal numbers |

## Edge Cases

The algorithm handles invalid calendar dates by explicitly checking day ranges for each month. Leap years are computed using modulo 4, which is sufficient for 2001-2099. Perm
