---
title: "CF 45A - Codecraft III"
description: "We are given the current month as a string and an integer k representing how many months later a new game release will happen. The task is to determine the month after advancing exactly k months forward in the calendar. The calendar is cyclic. After December comes January again."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 45
codeforces_index: "A"
codeforces_contest_name: "School Team Contest 3 (Winter Computer School 2010/11)"
rating: 900
weight: 45
solve_time_s: 74
verified: true
draft: false
---

[CF 45A - Codecraft III](https://codeforces.com/problemset/problem/45/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the current month as a string and an integer `k` representing how many months later a new game release will happen. The task is to determine the month after advancing exactly `k` months forward in the calendar.

The calendar is cyclic. After December comes January again. Because of this, the problem is really about moving forward inside a fixed circular sequence of 12 month names.

The constraints are extremely small. The value of `k` is at most 100, and there are only 12 months. Any reasonable implementation will run instantly. Even a simulation that advances one month at a time performs at most 100 operations, which is trivial for a 2 second time limit.

The main difficulty is not performance but handling the cyclic nature of the calendar correctly.

One common mistake is forgetting to wrap around after December. Consider this input:

```
December
1
```

The correct output is:

```
January
```

A careless implementation that simply moves to the next index without modular arithmetic would go out of bounds.

Another subtle case appears when `k = 0`. For example:

```
March
0
```

The correct output is:

```
March
```

If someone always advances at least once before processing `k`, they would incorrectly print April.

A third edge case happens when `k` is larger than 12. For example:

```
January
25
```

The correct output is:

```
February
```

Since every 12 months the calendar repeats, advancing 25 months is the same as advancing 1 month. Implementations that repeatedly move forward without reducing by modulo still work here because the constraints are small, but direct indexing solutions must apply modulo correctly.

## Approaches

The most direct solution is to simulate the passage of time month by month. We store all month names in order inside an array, locate the current month, then move forward `k` times. Every time we advance past December, we wrap back to January.

This brute-force approach is correct because each operation exactly mirrors how calendars work. Starting from the current month and repeatedly moving to the next month eventually lands on the correct answer.

The runtime is `O(k)`. With `k ≤ 100`, this is completely acceptable. At worst, we perform only 100 transitions.

The observation that improves the solution is that the calendar repeats every 12 months. Moving forward 12 months returns to the same month. Because of this periodic structure, we do not need simulation at all.

If the current month has index `i`, then the answer is simply:

```
(i + k) % 12
```

This converts the problem into circular array indexing. The modulo operation automatically handles wrapping from December back to January.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store all twelve months in an array in calendar order.
2. Read the current month and the integer `k`.
3. Find the index of the current month inside the array.

This index represents the month numerically from `0` to `11`.
4. Compute the destination index using `(current_index + k) % 12`.

The modulo operation wraps the position correctly when we move past December.
5. Output the month stored at the computed index.

### Why it works

The months form a cycle of length 12. Advancing by one month corresponds to moving one step forward in the array. Advancing by `k` months corresponds to moving `k` steps forward.

Modulo arithmetic preserves the correct position in a cyclic structure. Any movement beyond index 11 wraps back to the beginning exactly as the calendar does. Because of this, `(current_index + k) % 12` always matches the correct future month.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

current = input().strip()
k = int(input())

current_index = months.index(current)
answer_index = (current_index + k) % 12

print(months[answer_index])
```

The array `months` defines the calendar order explicitly. This gives us a direct mapping between month names and indices.

The call to `months.index(current)` finds the starting position. Since there are only 12 entries, this lookup is effectively constant time.

The expression `(current_index + k) % 12` is the key part of the implementation. Without `% 12`, indices larger than 11 would become invalid. The modulo converts large indices back into the valid range while preserving the correct cyclic position.

Using `input().strip()` is important because the month name comes from standard input and may contain a trailing newline character. Without stripping whitespace, the lookup would fail.

## Worked Examples

### Example 1

Input:

```
November
3
```

| Step | Value |
| --- | --- |
| Current month | November |
| Current index | 10 |
| k | 3 |
| Computed index | (10 + 3) % 12 = 1 |
| Answer | February |

The trace shows the wrap-around behavior clearly. Moving three months after November passes through December and returns to the start of the array.

### Example 2

Input:

```
January
25
```

| Step | Value |
| --- | --- |
| Current month | January |
| Current index | 0 |
| k | 25 |
| Computed index | (0 + 25) % 12 = 1 |
| Answer | February |

This example demonstrates that the modulo operation correctly handles values larger than 12. Advancing 25 months is equivalent to advancing 1 month.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The array size is fixed at 12, so all operations are constant time |
| Space | O(1) | Only a fixed-size array of month names is stored |

The solution easily fits within the limits. The program performs only a few arithmetic operations and stores a constant amount of data.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    current = input().strip()
    k = int(input())

    current_index = months.index(current)
    answer_index = (current_index + k) % 12

    print(months[answer_index])

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("November\n3\n") == "February", "sample 1"

# custom cases
assert run("March\n0\n") == "March", "k = 0"
assert run("December\n1\n") == "January", "year wrap"
assert run("January\n12\n") == "January", "full cycle"
assert run("January\n25\n") == "February", "large k with modulo"
assert run("August\n100\n") == "December", "maximum-style large movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `March 0` | `March` | No movement |
| `December 1` | `January` | Wrap-around after December |
| `January 12` | `January` | Full calendar cycle |
| `January 25` | `February` | Correct modulo behavior |
| `August 100` | `December` | Large movement values |

## Edge Cases

Consider the input:

```
December
1
```

The algorithm finds `December` at index `11`. Then it computes:

```
(11 + 1) % 12 = 0
```

Index `0` corresponds to `January`, which matches the correct calendar transition.

Now consider:

```
March
0
```

The index of `March` is `2`. The computation becomes:

```
(2 + 0) % 12 = 2
```

The result stays `March`. The algorithm correctly handles the case where no months pass.

Finally, consider:

```
January
25
```

The index of `January` is `0`. The computation becomes:

```
(0 + 25) % 12 = 1
```

Index `1` corresponds to `February`. Since every 12 months repeats the calendar, advancing 25 months is equivalent to advancing 1 month, and the algorithm captures that automatically through modulo arithmetic.
