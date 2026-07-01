---
title: "CF 104313C - \u042f \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044c"
description: "We are given a single month where the weekday of one specific day is known. That known anchor consists of a day number between 1 and 31 and a weekday name such as Monday or Sunday. Using this anchor, we must determine the weekday of another day in the same month."
date: "2026-07-01T19:45:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104313
codeforces_index: "C"
codeforces_contest_name: "II \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104313
solve_time_s: 45
verified: true
draft: false
---

[CF 104313C - \u042f \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044c](https://codeforces.com/problemset/problem/104313/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single month where the weekday of one specific day is known. That known anchor consists of a day number between 1 and 31 and a weekday name such as Monday or Sunday. Using this anchor, we must determine the weekday of another day in the same month.

The structure of the problem is essentially a linear calendar: each day advances the weekday by one step in a cycle of seven. Moving forward or backward between two dates only depends on the difference in their day numbers, not on any month-specific quirks such as varying lengths or leap years. The only operation we need is translating a numeric offset into a shift in a cyclic sequence of length seven.

The constraints are extremely small, with day numbers bounded by 31. This immediately rules out any need for complex preprocessing, simulation over large ranges, or data structures. Any solution that computes the difference between two integers and applies modular arithmetic is already sufficient within constant time.

The main edge case arises from wraparound behavior in the weekday cycle. For example, if the known day is near the end of the week and the target day is earlier in the month, the shift becomes negative. A naive implementation that forgets to normalize modulo 7 can produce incorrect indexing or even negative array access. Another subtle issue is consistent weekday ordering. If the mapping between weekday names and indices is inconsistent between encoding and decoding, the result will be shifted incorrectly by a fixed offset.

## Approaches

A brute-force interpretation would simulate day by day starting from the known date. We would assign the known weekday to day a, then iterate forward or backward through all days up to b, incrementing or decrementing the weekday each time. This works because each step is deterministic, but in the worst case we move across the entire month length, up to 31 steps. While this is still trivial, it is conceptually unnecessary overhead and becomes fragile if the bounds were larger.

The key observation is that weekdays form a cycle of size seven. Instead of simulating each intermediate day, we only need the net displacement between b and a. That displacement is simply (b − a), and the weekday shift is that value modulo 7. Once we convert weekdays to integers, the answer becomes a single arithmetic expression.

This reduces the entire problem to constant-time mapping and modular arithmetic, eliminating any iteration entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | b − a | ) |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by converting weekdays into a cyclic numeric system and applying a shift.

1. Assign each weekday a number from 0 to 6 in chronological order starting from Monday. This creates a consistent cyclic representation of the week.
2. Read the known anchor day a and its weekday s, and convert s into its numeric form cur.
3. Read the target day b.
4. Compute the difference diff = b − a, which represents how many days we move forward (or backward if negative).
5. Convert this difference into a weekday shift using diff mod 7, ensuring it always lies in the range 0 to 6.
6. Add this shift to cur and again take modulo 7 to remain inside the weekday cycle.
7. Convert the resulting number back into a weekday string and output it.

### Why it works

The weekday system is a pure modular cycle of length seven. Every increment of one calendar day corresponds to adding one modulo 7 in weekday space. Therefore, moving from day a to day b corresponds exactly to applying (b − a) such increments. Reducing this displacement modulo 7 preserves equivalence classes of shifts, so any full cycles of seven days cancel out without affecting the final weekday. The mapping between strings and indices is bijective, so no ambiguity is introduced at any stage.

## Python Solution

```python
import sys
input = sys.stdin.readline

days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

rev = {v: k for k, v in days.items()}

def solve():
    parts = input().split()
    a = int(parts[0])
    s = parts[1].strip()

    b = int(input().strip())

    cur = days[s]
    shift = (b - a) % 7
    ans = (cur + shift) % 7

    print(rev[ans])

if __name__ == "__main__":
    solve()
```

The solution first builds a fixed bijection between weekday names and integers, which is essential for performing arithmetic. The input is parsed in two steps because the first line contains both a number and a string. The shift computation uses modulo 7 to ensure correctness for both forward and backward movement across the week cycle. The final conversion back to a string completes the mapping.

A common implementation mistake is forgetting to normalize negative differences. In Python, negative modulo still behaves correctly, but in other languages this can lead to incorrect indices unless explicitly adjusted.

## Worked Examples

### Example 1

Input:

```
3 Wednesday
5
```

We map weekdays as Monday = 0 through Sunday = 6.

| Step | Value |
| --- | --- |
| a | 3 |
| b | 5 |
| s | Wednesday = 2 |
| diff | 5 − 3 = 2 |
| shift | 2 mod 7 = 2 |
| result index | (2 + 2) mod 7 = 4 |
| output | Friday |

This confirms forward shifting behaves as expected, moving two days ahead from Wednesday.

### Example 2

Input:

```
1 Monday
7
```

| Step | Value |
| --- | --- |
| a | 1 |
| b | 7 |
| s | Monday = 0 |
| diff | 6 |
| shift | 6 mod 7 = 6 |
| result index | (0 + 6) mod 7 = 6 |
| output | Sunday |

This shows correct wraparound behavior when crossing the end of the week cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time dictionary lookups and arithmetic operations are performed |
| Space | O(1) | Fixed mapping of seven weekdays |

The solution trivially fits within constraints since all operations are constant time and memory usage is fixed regardless of input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip() if False else _run(inp)

def _run(inp: str) -> str:
    import sys
    from io import StringIO

    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = StringIO(inp)
    sys.stdout = StringIO()

    solve()

    out = sys.stdout.getvalue().strip()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

# provided sample
assert _run("3 Wednesday\n5\n") == "Friday"

# minimum distance
assert _run("1 Monday\n1\n") == "Monday"

# wrap forward across week
assert _run("7 Sunday\n8\n") == "Monday"

# wrap backward logic
assert _run("2 Tuesday\n1\n") == "Monday"

# large jump multiple cycles
assert _run("10 Friday\n100\n") == "Thursday"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 Monday / 1 | Monday | zero shift |
| 7 Sunday / 8 | Monday | forward wraparound |
| 2 Tuesday / 1 | Monday | backward movement |
| 10 Friday / 100 | Thursday | multiple full cycles |

## Edge Cases

One edge case is when b is smaller than a, producing a negative difference. For example:

Input:

```
10 Friday
8
```

Here, Friday corresponds to index 4. The difference is 8 − 10 = −2. Applying modulo 7 gives 5, so we move five steps forward from Friday:

Friday (4) → Saturday (5) → Sunday (6) → Monday (0) → Tuesday (1) → Wednesday (2)

The output is Wednesday, which matches direct backward counting.

Another case is when the difference is exactly a multiple of 7:

Input:

```
15 Sunday
29
```

Difference is 14, and 14 mod 7 = 0. The weekday remains unchanged. This confirms that full-week cycles cancel out completely, preserving the anchor weekday regardless of how many weeks are traversed.
