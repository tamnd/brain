---
title: "CF 104599B - Birthday"
description: "We are given a range of years from $x$ to $y$, both inclusive. For every year in this interval, we must output the calendar date corresponding to March 7th in that year. Each output line represents one such date, formatted as a day number, then the month name, then the year."
date: "2026-06-30T02:58:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104599
codeforces_index: "B"
codeforces_contest_name: "GPL 2023 Novice"
rating: 0
weight: 104599
solve_time_s: 66
verified: true
draft: false
---

[CF 104599B - Birthday](https://codeforces.com/problemset/problem/104599/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a range of years from $x$ to $y$, both inclusive. For every year in this interval, we must output the calendar date corresponding to March 7th in that year. Each output line represents one such date, formatted as a day number, then the month name, then the year.

Conceptually, the task is to enumerate a simple deterministic mapping from each integer year to a fixed string representing a date. There is no filtering, no computation on the year other than iteration, and no dependency between years. The output order must follow chronological order, which in this context is equivalent to increasing year order since all dates are the same month and day.

The constraints allow $x, y \le 10^5$. This means the maximum number of years we may need to output is $10^5$. Any solution that performs constant work per year is sufficient, since about $10^5$ operations easily fits within a 1 second limit in Python. Anything involving nested loops over the range of years would also remain safe, but any approach with superlinear overhead per year is unnecessary.

There are no hidden corner cases related to calendar validity because the date is fixed as March 7th, which exists in every year in the standard Gregorian calendar, including leap years. The only edge cases come from formatting and ordering.

A naive mistake would be to recompute or re-parse dates using a date library or to construct strings inefficiently inside repeated concatenations. For example, building strings with repeated `+` operations in a loop over large ranges can introduce quadratic behavior in Python due to repeated allocations.

Another subtle issue is formatting consistency. The month must appear as the word “March”, not a number like 3, and spacing must match exactly. For instance:

Input:

```
2023 2024
```

Correct output:

```
7 March 2023
7 March 2024
```

A wrong approach might output `07 March 2023` or `March 7 2023`, both of which would be rejected due to formatting mismatch.

## Approaches

The brute-force idea is straightforward: iterate through every year from $x$ to $y$, construct the corresponding date string for March 7th, and print it immediately. Each iteration performs constant work: converting the year to string and concatenating fixed tokens.

This works because the mapping from year to output is independent and does not require precomputation or validation. However, one might still worry about efficiency if string construction is done inefficiently. If we repeatedly concatenate strings in a naive way inside a loop, Python may allocate new intermediate strings each time, but since each string is small and the total number of outputs is at most $10^5$, this remains acceptable.

The key observation is that the problem is not computationally complex at all. The structure is purely enumeration over a contiguous integer interval, and each element maps to a constant template. There is no optimization problem to solve, only careful iteration and formatting.

Thus the optimal solution is identical to the brute-force structure, but implemented carefully with direct formatting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ where $n = y-x+1$ | $O(1)$ | Accepted |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $x$ and $y$. These define the inclusive range of years we must process.
2. Iterate over all integers $i$ from $x$ to $y$. Each value of $i$ represents a single year.
3. For each year $i$, construct the output string exactly in the format: `7 March i`. The day and month are fixed constants, so only the year varies.
4. Print each constructed string immediately in the loop. This avoids storing all outputs and keeps memory usage constant.

### Why it works

Each year in the interval corresponds to exactly one valid occurrence of March 7th. There is no dependency between years and no missing cases. The iteration covers the full inclusive range, so every required date is produced exactly once. Since the output format is fixed and deterministic for each year, constructing the string directly yields the correct chronological sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, y = map(int, input().split())

for year in range(x, y + 1):
    sys.stdout.write(f"7 March {year}\n")
```

The solution reads the two endpoints and iterates inclusively over the range. The use of `sys.stdout.write` avoids the overhead of repeated `print` calls, though `print` would also pass comfortably under these constraints.

The formatting string is fixed, with only the year interpolated. A common mistake is to accidentally swap day and month or to use numeric month representations. Here the literal `"March"` is required.

The loop boundary is inclusive on both ends, so `range(x, y + 1)` is essential. Omitting the `+1` would silently drop the last year, which is a typical off-by-one error in such enumeration problems.

## Worked Examples

### Example 1

Input:

```
2023 2024
```

| Step | Year | Output |
| --- | --- | --- |
| 1 | 2023 | 7 March 2023 |
| 2 | 2024 | 7 March 2024 |

This trace shows that each year independently generates one formatted string. The order matches increasing year order, which satisfies chronological ordering.

### Example 2

Input:

```
2020 2022
```

| Step | Year | Output |
| --- | --- | --- |
| 1 | 2020 | 7 March 2020 |
| 2 | 2021 | 7 March 2021 |
| 3 | 2022 | 7 March 2022 |

This confirms that the loop includes both endpoints and produces exactly $y-x+1$ lines. No year is skipped and no extra output is produced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(y - x + 1)$ | One constant-time string construction and output per year |
| Space | $O(1)$ | No storage proportional to input size; output streamed directly |

The maximum number of iterations is $10^5$, which is well within limits for Python. Memory usage remains constant since no large data structures are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import PIPE, Popen
    p = Popen(["python3", "main.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    out, _ = p.communicate(inp)
    return out.strip()

# sample
# assert run("2023 2024") == "7 March 2023\n7 March 2024"

# minimum range
assert run("1 1") == "7 March 1"

# small range
assert run("2020 2022") == "7 March 2020\n7 March 2021\n7 March 2022"

# boundary formatting check
assert run("9 10") == "7 March 9\n7 March 10"

# larger consecutive block
assert run("1998 2002") == "\n".join([
    "7 March 1998",
    "7 March 1999",
    "7 March 2000",
    "7 March 2001",
    "7 March 2002"
])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 7 March 1 | single element range |
| 9 10 | 7 March 9\n7 March 10 | formatting and two-year range |
| 1998 2002 | sequential lines | multi-step iteration correctness |

## Edge Cases

The main edge case is when the range collapses to a single year, such as $x = y$. In this situation, the loop still runs exactly once due to inclusive bounds. For input:

```
5 5
```

The algorithm initializes `
