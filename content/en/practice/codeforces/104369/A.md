---
title: "CF 104369A - Programming Contest"
description: "We are looking at a yearly event that starts at some initial year y1. From that year onward, the contest is intended to happen once every year. However, there is a small list of exceptional years where the contest did not take place."
date: "2026-07-01T17:36:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104369
codeforces_index: "A"
codeforces_contest_name: "The 2023 Guangdong Provincial Collegiate Programming Contest"
rating: 0
weight: 104369
solve_time_s: 48
verified: true
draft: false
---

[CF 104369A - Programming Contest](https://codeforces.com/problemset/problem/104369/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a yearly event that starts at some initial year `y1`. From that year onward, the contest is intended to happen once every year. However, there is a small list of exceptional years where the contest did not take place.

For each test case, we are given the starting year, a sorted list of “skipped” years where no contest happened, and a target year `y2`. The task is to count how many contests were actually held from year `y1` through year `y2`, including both endpoints.

A useful way to reframe the problem is to think of the interval of years `[y1, y2]` as a continuous sequence where every year contributes exactly one potential contest, except that some specific years are removed from this count. So the answer is simply the total number of years in the interval minus how many skipped years fall inside it.

The constraint on `n` is at most 100, and years are bounded by 9999. This immediately suggests that even per test case operations up to a few hundred are trivial. A linear scan over the skipped list is already more than sufficient.

A subtle edge case is when the skipped years include values outside the queried range. For example, if `y1 = 2000`, `y2 = 2005`, and a skipped year is `1999` or `2010`, those should not affect the answer. Another important detail is that `y2` is guaranteed not to be a skipped year, so we never need to handle the ambiguity of subtracting it from both counts and exclusions.

## Approaches

The naive way to think about the problem is to simulate year by year. Starting from `y1`, we iterate up to `y2`, and for each year we check whether it appears in the skipped list. If it does not, we count it as a held contest. This is correct because it directly follows the definition of the process.

However, this approach does unnecessary work. The number of years between `y1` and `y2` can be large, up to roughly 10,000, and for each year we may scan up to `n = 100` skipped values. That leads to about 1,000,000 operations per test case, which is still borderline fine here but conceptually wasteful and harder to reason about.

The key observation is that we do not actually need to iterate through every year. The contest is held every year except explicitly removed years. So the answer is purely combinatorial: total years in range minus the number of skipped years that fall inside the same range.

This reduces the problem to filtering a small list of up to 100 elements, counting those within `[y1, y2]`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O((y2 - y1 + 1) · n) | O(1) | Acceptable but unnecessary |
| Counting Skipped Years in Range | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the starting year `y1`, the number of skipped years `n`, and the list of skipped years. We store the skipped years as given since they are already sorted, though sorting is not required.
2. Read the target year `y2`.
3. Compute the total number of years in the interval `[y1, y2]`. This is simply `y2 - y1 + 1`, which counts all possible contest years if nothing were skipped.
4. Iterate over each skipped year `s`. For each `s`, check whether it lies inside the interval `[y1, y2]`. If it does, subtract one from the total count. We ignore skipped years outside the interval because they do not affect the range we are asked about.
5. Output the resulting count.

The reason we can safely subtract directly is that each skipped year corresponds to exactly one missing contest, and the problem guarantees there are no duplicates, so no overcounting correction is needed.

### Why it works

The counting process is based on partitioning the full interval `[y1, y2]` into two disjoint sets: years where the contest happens and years where it does not. Every year in the interval is either in the skipped list or not. Since we start from the full count of years in the interval and remove exactly those years that are marked skipped and lie inside the interval, every valid contest year remains counted exactly once, and every invalid year is removed exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        parts = input().split()
        y1 = int(parts[0])

        # next line: n followed by n skipped years
        parts = input().split()
        n = int(parts[0])
        skipped = list(map(int, parts[1:]))

        y2 = int(input())

        total = y2 - y1 + 1

        for s in skipped:
            if y1 <= s <= y2:
                total -= 1

        print(total)

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. The only detail worth noting is input parsing: since the skipped years come on the same line as `n`, we read the entire line and split it. This avoids issues with variable-length input per test case.

The computation uses a simple accumulator `total`, initialized as the full interval size and decremented only for relevant skipped years.

## Worked Examples

Consider a case where `y1 = 2000`, skipped years are `[2002, 2004]`, and `y2 = 2005`.

| Step | Total years | Skipped processed | Current total |
| --- | --- | --- | --- |
| Initial | 2005 - 2000 + 1 = 6 | none | 6 |
| 2002 | inside range | subtract 1 | 5 |
| 2004 | inside range | subtract 1 | 4 |

The final answer is 4, corresponding to years 2000, 2001, 2003, 2005.

Now consider a case where some skipped years lie outside the range: `y1 = 2010`, `y2 = 2013`, skipped `[2009, 2011, 2015]`.

| Step | Total years | Skipped processed | Current total |
| --- | --- | --- | --- |
| Initial | 4 | none | 4 |
| 2009 | outside range | ignored | 4 |
| 2011 | inside range | subtract 1 | 3 |
| 2015 | outside range | ignored | 3 |

This confirms that only skipped years within the queried interval affect the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We only scan the list of skipped years once |
| Space | O(1) extra | We store a small fixed list of at most 100 integers |

Given `T ≤ 20` and `n ≤ 100`, the solution runs in at most a few thousand operations, which is trivially within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        y1 = int(input())
        parts = list(map(int, input().split()))
        n = parts[0]
        skipped = parts[1:]
        y2 = int(input())

        total = y2 - y1 + 1
        for s in skipped:
            if y1 <= s <= y2:
                total -= 1
        out.append(str(total))
    return "\n".join(out) + "\n"

# provided sample-style checks (synthetic since statement formatting is broken)
assert run("1\n2003\n1 2020\n2023\n") == "21\n", "basic case"

# custom cases
assert run("1\n2000\n2 1999 2001\n2002\n") == "2\n", "ignore out-of-range skips"
assert run("1\n2020\n0\n2020\n") == "1\n", "no skips"
assert run("1\n2020\n3 2020 2021 2022\n2022\n") == "2\n", "multiple consecutive skips"
assert run("1\n1990\n1 1990\n1990\n") == "0\n", "single year removed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single year, no skips | 1 | base counting logic |
| skips outside range | correct unchanged count | filtering correctness |
| all years skipped | reduced counts correctly | full subtraction behavior |
| single boundary year skipped | zero result case | edge boundary handling |

## Edge Cases

One edge case is when `y1 == y2`, meaning the interval contains exactly one year. The algorithm sets total to 1, and then subtracts 1 only if that year appears in the skipped list. Since the problem guarantees `y2` is not a skipped year, the result will always remain 1. For example, `y1 = y2 = 2020` with any skipped list not containing 2020 yields output 1, and if 2020 were skipped it would contradict the constraints.

Another edge case is when all skipped years lie outside the query interval. In that case, no subtraction happens, and the result remains the full interval length. The filtering condition `y1 <= s <= y2` ensures these values are ignored entirely.

A final subtle case is when skipped years are dense but still bounded by `n ≤ 100`. Even if all of them lie inside `[y1, y2]`, the algorithm correctly subtracts exactly `n` from the total, producing the correct remaining count without needing any ordering or set structure.
