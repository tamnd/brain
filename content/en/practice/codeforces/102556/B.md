---
title: "CF 102556B - Riana and the Blind Date"
description: "The task is to count the total pencil cost of writing every calendar date from year A through year B. A date is represented without the year by joining the month number and the day number. For example, March 7 becomes 37, while December 24 becomes 1224."
date: "2026-08-04T09:16:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102556
codeforces_index: "B"
codeforces_contest_name: "2020 Ateneo de Manila University DISCS PrO HS Division"
rating: 0
weight: 102556
solve_time_s: 65
verified: true
draft: false
---

[CF 102556B - Riana and the Blind Date](https://codeforces.com/problemset/problem/102556/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
# Problem Understanding

The task is to count the total pencil cost of writing every calendar date from year `A` through year `B`. A date is represented without the year by joining the month number and the day number. For example, March 7 becomes `37`, while December 24 becomes `1224`. The cost of writing a date is the numeric value of that representation itself.

The only part of a year that affects the answer is whether February has 28 or 29 days. The input gives two years, possibly as large as `10^18`, and the output is the sum of all date values across all those years, reduced modulo `104206969`.

The size of the years immediately rules out iterating through years or dates. A range containing `10^18` years would require roughly `10^18 * 365` date calculations, which is far beyond what a program can do in a reasonable time. The solution must use the fact that most years are identical and only the leap year count matters.

There are several places where a direct implementation can fail. Year `0` is one of them. It satisfies the leap year rule because it is divisible by 400, so the input `0 0` must use February with 29 days and produces `180987`. A solution that starts counting leap years from `1` would incorrectly treat it as a normal year.

Another trap is the century rule. The input `1900 1900` is a normal year even though it is divisible by 4, because it is also divisible by 100 and not by 400. Its answer is `180758`. A solution using only divisibility by 4 would return the leap year value.

The opposite boundary appears at `2000 2000`. This year is divisible by 400, so it is a leap year and the answer is `180987`. Solutions that reject all century years as non-leap years fail here.

# Approaches

A brute force solution would process every year in the interval, determine whether it is a leap year, then loop through its twelve months and all days inside those months. For each day it would construct the date value and add it to the answer. This is correct because it follows the definition directly.

However, the largest possible interval contains about `10^18` years. Even one constant-time operation per year would already be too slow, and a full date simulation would require around `3.65 * 10^20` day operations. The repeated structure of the calendar is the key observation that removes this need.

Every normal year contributes exactly the same amount, because its month lengths never change. Every leap year also contributes exactly the same amount. Instead of summing individual years, we only need to count how many normal years and leap years appear in the range.

For a month `m` with `L` days, the first nine days contribute values of the form `10m + day`, and the remaining days contribute values of the form `100m + day`. Combining these two parts gives a direct formula:

`month_sum = m * (100L - 810) + L(L+1)/2`

Using this for all months gives the fixed contribution of a normal year and a leap year.

The remaining problem is counting leap years from `0` to a given year. The number of years divisible by `k` from `0` through `n` is `n//k + 1`, because year zero is included. Inclusion-exclusion gives the leap count:

`multiples of 4 - multiples of 100 + multiples of 400`

Using a prefix function for years `0..n` lets us answer any interval with subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of years * 365) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

# Algorithm Walkthrough

1. Precompute the contribution of one normal year and one leap year. For each month, apply the formula for the sum of all encoded dates in that month. This avoids recalculating the same calendar pattern repeatedly.
2. Create a prefix function `pref(x)` that returns the total contribution of all years from `0` through `x`. If `x` is negative, the prefix is zero because there are no years before zero.
3. Count leap years in the prefix range using divisibility by 4, 100, and 400. The remaining years are normal years, so multiply the two counts by their respective yearly contributions.
4. Compute the requested interval by subtracting prefixes: `pref(B) - pref(A-1)`. Apply the modulus after the subtraction to keep the result positive.

Why it works: every year belongs to exactly one of two categories, normal or leap. All normal years have the same twelve month lengths, so they contribute the same amount. The same is true for leap years. The prefix function counts exactly how many years of each type exist, which means the total sum is the exact combination of those two fixed contributions.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 104206969

def year_value(leap):
    days = [31, 29 if leap else 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31]

    total = 0
    for month, length in enumerate(days, 1):
        total += month * (100 * length - 810)
        total += length * (length + 1) // 2
    return total % MOD

NORMAL_YEAR = year_value(False)
LEAP_YEAR = year_value(True)

def leap_count(x):
    if x < 0:
        return 0
    return (x // 4 + 1) - (x // 100 + 1) + (x // 400 + 1)

def prefix(x):
    if x < 0:
        return 0

    leaps = leap_count(x)
    years = x + 1
    normal = years - leaps

    return (normal * NORMAL_YEAR + leaps * LEAP_YEAR) % MOD

def solve():
    A, B = map(int, input().split())
    print((prefix(B) - prefix(A - 1)) % MOD)

solve()
```

`year_value` compresses all twelve months into a single calculation. The formula handles one-digit and two-digit days together, which avoids looping over individual dates.

`leap_count` deliberately uses `x//k + 1` instead of only `x//k`. The extra one represents year zero, which follows the same divisibility rules as every other year.

The prefix calculation uses `x + 1` years because the interval starts at zero and includes both endpoints. The final subtraction uses `A - 1`, so the year `A` itself remains included.

Python integers do not overflow, but intermediate values can become large. The modulus is applied when returning the prefix value, and the final answer is also normalized with `% MOD` because the subtraction may be negative.

# Worked Examples

For input `1 3`, all three years are normal years.

| Year range | Leap years | Normal years | Contribution |
| --- | --- | --- | --- |
| 0..3 | 1 | 3 | prefix value |
| 0..0 | 1 | 0 | prefix value |
| 1..3 | 0 | 3 | 542274 |

The result is `3 * 180758 = 542274`, matching the sample. This trace confirms that the interval subtraction correctly removes years before `A`.

For input `2000 2000`, the only year is a leap year.

| Year range | Leap years | Normal years | Contribution |
| --- | --- | --- | --- |
| 0..2000 | 486 | 1515 | prefix value |
| 0..1999 | 485 | 1515 | prefix value |
| 2000..2000 | 1 | 0 | 180987 |

The difference leaves exactly one leap year contribution, confirming that the century rule is handled correctly.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and twelve-month calculations are performed |
| Space | O(1) | The algorithm stores only constant-sized values |

The solution does not depend on the size of the year interval. Even the maximum input values near `10^18` require the same amount of work as a one-year interval.

# Test Cases

```python
import sys
import io

MOD = 104206969

def year_value(leap):
    days = [31, 29 if leap else 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31]
    total = 0
    for month, length in enumerate(days, 1):
        total += month * (100 * length - 810)
        total += length * (length + 1) // 2
    return total % MOD

NORMAL_YEAR = year_value(False)
LEAP_YEAR = year_value(True)

def leap_count(x):
    if x < 0:
        return 0
    return (x // 4 + 1) - (x // 100 + 1) + (x // 400 + 1)

def prefix(x):
    if x < 0:
        return 0
    l = leap_count(x)
    return ((x + 1 - l) * NORMAL_YEAR + l * LEAP_YEAR) % MOD

def solve_case(inp):
    a, b = map(int, inp.split())
    return str((prefix(b) - prefix(a - 1)) % MOD)

assert solve_case("1 3") == "542274", "sample"
assert solve_case("0 0") == "180987", "year zero leap"
assert solve_case("1 1") == "180758", "single normal year"
assert solve_case("1900 1900") == "180758", "century non leap"
assert solve_case("2000 2000") == "180987", "century leap"
assert solve_case("1000000000000000000 1000000000000000000") == "180987", "maximum year"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `180987` | Year zero handling |
| `1 1` | `180758` | Single normal year |
| `1900 1900` | `180758` | Century exception |
| `2000 2000` | `180987` | Divisible by 400 leap year |
| `1000000000000000000 1000000000000000000` | `180987` | Maximum boundary |

# Edge Cases

For input `0 0`, the algorithm computes `leap_count(0)` as `1//?` through the formula `(0//4+1) - (0//100+1) + (0//400+1)`, which gives `1`. The year is classified as leap and contributes `180987`.

For input `1900 1900`, the divisibility by 4 count includes the year, but the divisibility by 100 count removes it. Since 1900 is not divisible by 400, it is not added back. The result uses the normal year contribution.

For input `2000 2000`, the year is removed by the divisible-by-100 rule and restored by the divisible-by-400 rule. It receives the leap year contribution.

For a huge range such as `1 10^18`, the algorithm never loops through the years. It only evaluates the number of leap and normal years with integer division, so the running time remains constant even at the maximum constraint.
