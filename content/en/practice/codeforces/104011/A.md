---
title: "CF 104011A - Anno Domini 2022"
description: "We are given two points on a simplified timeline where every year is labeled either in the AD system or in the BC system. Each input line describes a year like “AD 2022” or “5508 BC”."
date: "2026-07-02T05:12:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104011
codeforces_index: "A"
codeforces_contest_name: "2021-2022 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104011
solve_time_s: 48
verified: true
draft: false
---

[CF 104011A - Anno Domini 2022](https://codeforces.com/problemset/problem/104011/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two points on a simplified timeline where every year is labeled either in the AD system or in the BC system. Each input line describes a year like “AD 2022” or “5508 BC”. The task is to compute how many whole years lie strictly between the first day of the first given year and the first day of the second given year.

The key subtlety is the historical convention that there is no year 0. The sequence of years around the transition is … 2 BC, 1 BC, AD 1, AD 2 …. This makes direct subtraction on signed integers slightly tricky if we do not encode the mapping carefully.

The constraints are small, with years bounded by 1 to 9999. This immediately tells us that any solution running in constant time per test case is sufficient, and even repeated parsing or simple arithmetic is negligible.

The main edge case is crossing the BC to AD boundary. For example, between “1 BC” and “AD 1”, the answer is not 2, but 1, because there is exactly one year boundary step between them. A naive mapping that treats BC years as negative numbers including zero will fail here.

Another edge case is ordering. The earlier date is not guaranteed to come first, so any solution must normalize by taking absolute difference in a consistent numeric mapping.

## Approaches

A brute force way to think about the problem is to simulate year by year starting from the earlier date and incrementing or decrementing until reaching the later date, counting steps. This is conceptually simple and always correct, but it is unnecessary work. Even though the range is small, the difference between endpoints could be up to roughly 20000 years in worst BC to AD transitions, which is still small but not elegant, and it becomes awkward if extended.

The real insight is that this is just a linear ordering problem with a discontinuity at zero. If we can map each year to a single integer line where adjacency corresponds exactly to time adjacency, then the answer becomes a simple absolute difference.

The natural construction is to assign AD years as positive integers and BC years as negative integers, but with a correction: since there is no year 0, we must ensure that 1 BC maps to -1 and AD 1 maps to +1, making the transition gap exactly 2 units in raw integers but only 1 year in reality. To fix this, we shift BC years by one when converting, effectively skipping zero in the number line.

Once both years are mapped into this corrected integer axis, the number of years between them is simply the absolute difference.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(difference) | O(1) | Too slow and unnecessary |
| Integer mapping with shift | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We convert each input year into an integer on a unified timeline where consecutive integers correspond to consecutive years in history.

1. Parse each line into a pair consisting of a numeric year value and a direction marker, either AD or BC.
2. Convert the year into a signed integer representation. If the year is AD, we map it directly to +year. If the year is BC, we map it to -year. At this stage, 1 BC becomes -1 and AD 1 becomes +1.
3. Compute the raw difference between these two integers. However, this raw difference double counts the missing year zero transition.
4. Adjust the mapping by treating the BC side as shifted forward by 1 unit. This can be implemented equivalently by mapping BC year y to -(y - 1), which ensures that -1 corresponds to 1 BC and 0 corresponds to AD 1's predecessor slot, effectively removing the nonexistent year gap.
5. After conversion, take the absolute difference between the two mapped values. This gives the exact number of year-to-year transitions between the two January 1st boundaries.

### Why it works

The integer mapping constructs a bijection between real historical years and integers with unit spacing. Every increment of 1 in the mapped value corresponds to moving forward exactly one calendar year, including across the BC to AD boundary. Since the mapping preserves adjacency and removes the artificial zero point, the distance in integer space is identical to the number of years passed in real time. The absolute difference therefore counts exactly the number of year transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse(line: str) -> int:
    parts = line.strip().split()
    if parts[0] == "AD":
        return int(parts[1])
    else:
        y = int(parts[0])
        return -(y - 1)

a = parse(input())
b = parse(input())

print(abs(a - b))
```

The solution reads two lines and converts each into a unified integer timeline value. The helper function handles the asymmetry between BC and AD by shifting BC years so that there is no artificial zero point.

The final answer is computed as an absolute difference, which is valid because the mapping guarantees linear adjacency.

A common mistake is mapping BC years directly to negative integers without shifting. That causes “1 BC” to be -1 and “AD 1” to be +1, which incorrectly implies a distance of 2. The corrected shift fixes exactly this issue.

## Worked Examples

### Example 1

Input:

AD 1

1 BC

Mapped values:

| Step | Value 1 | Value 2 | Difference |
| --- | --- | --- | --- |
| Parse | 1 | 1 BC | - |
| Map | 1 | 0 | - |
| Compute | 1 | 0 | 1 |

Output is 1, matching the fact that only the transition from 1 BC to AD 1 is a single year step.

This confirms that the mapping correctly collapses the missing year zero gap.

### Example 2

Input:

AD 2001

AD 1

Mapped values:

| Step | Value 1 | Value 2 | Difference |
| --- | --- | --- | --- |
| Parse | 2001 | 1 | - |
| Map | 2001 | 1 | - |
| Compute | 2001 | 1 | 2000 |

Output is 2000, which corresponds to the number of yearly transitions between the two AD dates.

This verifies that within a single era the mapping reduces to normal subtraction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time parsing and arithmetic |
| Space | O(1) | No additional data structures used |

The constraints are small enough that even less optimal solutions would pass, but this direct mapping avoids any unnecessary simulation and works uniformly across BC and AD ranges.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def parse(line: str) -> int:
        parts = line.strip().split()
        if parts[0] == "AD":
            return int(parts[1])
        else:
            y = int(parts[0])
            return -(y - 1)

    a = parse(input())
    b = parse(input())
    return str(abs(a - b))

def run(inp: str) -> str:
    return solve(inp)

# provided samples
assert run("1 BC\nAD 1\n") == "1"
assert run("AD 1\nAD 2001\n") == "2000"

# custom cases
assert run("AD 2022\n5508 BC\n") == str(abs(2022 - (-(5508 - 1)))), "cross era large gap"
assert run("1 BC\n2 BC\n") == "1", "within BC consecutive years"
assert run("AD 1\nAD 1\n") == "0", "same year"
assert run("9999 BC\nAD 9999\n") == str(abs(-(9999 - 1) - 9999)), "max boundary cross"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| AD 1 / 1 BC | 1 | BC-AD boundary correctness |
| AD 1 / AD 2001 | 2000 | normal AD subtraction |
| AD 2022 / 5508 BC | computed | large cross-era gap |
| 1 BC / 2 BC | 1 | BC ordering correctness |
| AD 1 / AD 1 | 0 | identical input handling |

## Edge Cases

For the BC to AD transition, consider input “1 BC” and “AD 1”. The parser maps them to 0 and 1 respectively after shifting BC by one. The difference is 1, which matches the single year transition across the boundary.

For purely BC input like “2 BC” and “1 BC”, the mapping gives -1 and 0. The difference is 1, correctly reflecting consecutive years in reverse chronological order.

For identical years such as “AD 2022” and “AD 2022”, both map to 2022, producing 0 as expected.

The shifting logic ensures all discontinuities are absorbed into a continuous integer line, so every possible ordering reduces to a single absolute difference computation.
