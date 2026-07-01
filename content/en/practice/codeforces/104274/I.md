---
title: "CF 104274I - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0434\u043d\u0438 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u0432\u0435\u043b\u0438\u043a\u0438\u0445"
description: "We are given a person’s birth date and an upper bound year. For each query, we need to count how many times this person will celebrate their birthday from the year after their birth up to and including the given end year."
date: "2026-07-01T21:20:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104274
codeforces_index: "I"
codeforces_contest_name: "2023 VIII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e"
rating: 0
weight: 104274
solve_time_s: 61
verified: true
draft: false
---

[CF 104274I - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0434\u043d\u0438 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u0432\u0435\u043b\u0438\u043a\u0438\u0445](https://codeforces.com/problemset/problem/104274/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a person’s birth date and an upper bound year. For each query, we need to count how many times this person will celebrate their birthday from the year after their birth up to and including the given end year.

The key complication is that birthdays only occur on the same calendar date each year, except when the birthday is February 29. In that special case, the birthday only happens in leap years. A year is considered leap if it is divisible by 400, or divisible by 4 but not by 100.

So the task reduces to counting how many years in a range contain the date “D/M” as a valid calendar date. For normal dates, every year contributes one birthday. For February 29, only leap years contribute.

The constraints are large: up to 100000 queries and years up to 2,000,000. This rules out any per-year simulation. Even a naive approach that iterates year by year for each query would require up to 2e11 operations in the worst case, which is infeasible.

A subtle edge case is handling February 29 correctly with the correct leap year rules. Another is ensuring we exclude the birth year itself, even if the birthday occurs later in that same year, since the problem explicitly starts counting from the next year.

For example, if the person is born on 1 January 2000 and YE is 2000, the answer is 0. If born on 29 February 2020 and YE is 2020, the answer is also 0.

## Approaches

A direct approach is to iterate over every year from Y+1 to YE and check whether the birthday exists in that year. For most dates, this is trivial since every year contains that day and month. For February 29, we additionally check the leap condition.

This works conceptually, but in worst cases the range length can be up to 2 million per test, and with up to 100000 tests this becomes far too slow. The bottleneck is the repeated per-year checking.

The key observation is that for all dates except February 29, the answer is purely the count of integers in a range, since the birthday always exists once per year. For February 29, we only need to count how many leap years exist in a range. This reduces each query to either a constant-time subtraction or a prefix count of leap years.

To support leap year counting efficiently, we derive a formula for how many leap years are in [1, N]. This can be computed using inclusion-exclusion on multiples of 4, 100, and 400. Once we have this function, each query becomes O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · (YE − Y)) | O(1) | Too slow |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. First, we set the effective counting range as all years strictly after the birth year up to the end year, i.e. from Y+1 to YE. This ensures we correctly exclude the birth year.
2. If the birthday is not 29 February, then every year in this interval contributes exactly one birthday. We compute the answer as (YE − Y). This is because every year in the range is valid for that date.
3. If the birthday is 29 February, we instead need to count how many leap years lie in the interval [Y+1, YE].
4. To compute how many leap years are ≤ X, we use the formula:

floor(X/4) − floor(X/100) + floor(X/400).

This counts multiples of 4, removes invalid century years, and adds back centuries divisible by 400.
5. The number of leap years in [L, R] is computed as F(R) − F(L−1), where F(X) is the prefix leap count.
6. We apply this formula with L = Y+1 and R = YE, producing the final answer.

Why it works

For non-leap-special birthdays, the event “birthday occurs” is independent of the year and always true, so counting reduces to counting integers in a range. For February 29, the event reduces exactly to membership of the year in the leap-year set, which is fully characterized by the standard divisibility rules. The prefix function F(X) precisely counts that set up to X, and subtraction isolates any interval without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def leap_count(x):
    if x <= 0:
        return 0
    return x // 4 - x // 100 + x // 400

def solve():
    T = int(input())
    out = []
    for _ in range(T):
        d, m, y, ye = map(int, input().split())
        l = y + 1
        r = ye

        if m == 2 and d == 29:
            if l > r:
                out.append("0")
                continue
            ans = leap_count(r) - leap_count(l - 1)
            out.append(str(ans))
        else:
            if l > r:
                out.append("0")
            else:
                out.append(str(r - l + 1))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution separates the leap-year case from all other dates. The helper function `leap_count` implements the inclusion-exclusion formula for counting leap years up to a threshold.

For normal dates, we compute the number of integers in the range [Y+1, YE], which is simply `r - l + 1`. For February 29, we transform the problem into counting how many valid leap years exist in that same interval using prefix differences.

The boundary condition `l > r` handles cases where YE equals Y, ensuring no negative counts appear.

## Worked Examples

### Example 1

Input:

```
15 1 1975 2020
```

| Step | L | R | Type | Result |
| --- | --- | --- | --- | --- |
| init | 1976 | 2020 | normal |  |
| count |  |  | range size | 2020 − 1976 + 1 = 45 |

This confirms that every year contributes exactly one birthday, since the date is not February 29.

### Example 2

Input:

```
29 2 2020 2035
```

| Step | L | R | leap(R) | leap(L−1) | Result |
| --- | --- | --- | --- | --- | --- |
| init | 2021 | 2035 |  |  |  |
| compute |  |  | F(2035)=? | F(2020)=? | difference |

We evaluate:

F(2035) = 2035//4 − 2035//100 + 2035//400 = 508 − 20 + 5 = 493

F(2020) = 505 − 20 + 5 = 490

Result = 3

This matches the idea that only leap years 2024, 2028, 2032 fall in the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each query is handled with a constant number of arithmetic operations |
| Space | O(1) | Only a few integers and output storage |

The solution comfortably fits the constraints since even 100000 queries only require simple integer arithmetic, with no iteration over years.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def leap_count(x):
        if x <= 0:
            return 0
        return x // 4 - x // 100 + x // 400

    T = int(input())
    out = []
    for _ in range(T):
        d, m, y, ye = map(int, input().split())
        l, r = y + 1, ye
        if m == 2 and d == 29:
            if l > r:
                out.append("0")
            else:
                out.append(str(leap_count(r) - leap_count(l - 1)))
        else:
            out.append(str(max(0, r - l + 1)))
    return "\n".join(out)

# provided samples
assert run("""5
15 1 1975 1976
15 1 1975 2020
7 10 2002 3001
29 2 2024 2140
29 2 2020 2035
""") == """1
45
999
28
3"""

# custom cases
assert run("""1
1 1 2000 2000
""") == "0", "same year excluded"

assert run("""1
29 2 2000 2000
""") == "0", "no leap in range"

assert run("""1
29 2 1996 2005
""") == "3", "1996, 2000, 2004"

assert run("""1
1 3 1999 2003
""") == "4", "normal range count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 Jan same year | 0 | exclusion of birth year |
| 29 Feb same year | 0 | leap case boundary |
| 1996-2005 Feb 29 | 3 | correct leap counting |
| normal range | 4 | general counting correctness |

## Edge Cases

One edge case is when the birth year is equal to the end year. For a normal date like 10/5/2000 with YE = 2000, the interval becomes empty since we start from 2001. The algorithm sets L = Y+1, so L > R and returns 0 directly.

Another edge case is February 29 in a range that contains no leap years. For example, 29/2/2021 to 2023 produces L = 2022 and R = 2023. The leap prefix difference returns zero because neither endpoint contains a leap year.

A final edge case is very large year values close to 2e6. The prefix formula still works safely because all operations are simple integer divisions, and no overflow or iteration occurs.
