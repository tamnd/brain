---
title: "CF 105183A - \u041e\u0447\u0435\u043d\u044c \u0441\u0435\u0440\u044c\u0435\u0437\u043d\u044b\u0439 \u0447\u0435\u043b\u043e\u0432\u0435\u043a"
description: "We are given a fixed number of training days and a target number of total training hours. Each day contributes either a normal amount of training time or a boosted amount of training time."
date: "2026-06-27T04:28:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105183
codeforces_index: "A"
codeforces_contest_name: "XX \u041d\u0438\u0436\u0435\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u0412. \u0414. \u041b\u0435\u043b\u044e\u0445\u0430"
rating: 0
weight: 105183
solve_time_s: 59
verified: true
draft: false
---

[CF 105183A - \u041e\u0447\u0435\u043d\u044c \u0441\u0435\u0440\u044c\u0435\u0437\u043d\u044b\u0439 \u0447\u0435\u043b\u043e\u0432\u0435\u043a](https://codeforces.com/problemset/problem/105183/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed number of training days and a target number of total training hours. Each day contributes either a normal amount of training time or a boosted amount of training time. A normal day always gives 24 hours of training, while a special “superday” gives 72 hours instead. The task is to choose how many of the available days should be turned into superdays so that the total accumulated training time over all days is at least the required target, while keeping the number of superdays as small as possible.

The input consists of two numbers, the number of available days and the required total training hours. The output is a single integer representing the smallest number of days that must be upgraded to superdays to meet or exceed the target total.

The constraint that the required hours never exceed 72 times the number of days guarantees feasibility. Even if every day is a superday, the target can always be reached.

From a complexity perspective, both values can be as large as 100,000. This rules out any approach that tries to simulate all possible choices of superdays per day using recursion or exhaustive search, since that would grow exponentially with the number of days. Even a quadratic loop over days would be safe in isolation, but unnecessary. The structure of the problem suggests that we are optimizing a single integer parameter, so a closed-form or greedy reasoning is expected.

A subtle case that can break naive reasoning appears when the target is already achievable without any superdays. For example, if there are 5 days and the target is 100 hours, the normal schedule already gives 120 hours. In this case, the correct answer is zero, and any formula that blindly computes a positive requirement would be wrong.

Another edge case occurs when the target is exactly equal to the normal total. For instance, with 3 days and target 72, no superdays are needed. These boundary conditions are important because the solution naturally involves subtraction that can go negative.

## Approaches

The brute-force idea is to try every possible number of superdays from 0 up to d, compute the total training time for each choice, and pick the smallest valid value. For each candidate x, the total time is computed as 24(d − x) + 72x. Checking all possibilities costs O(d) evaluations, and each evaluation is O(1), so the overall complexity is O(d). With d up to 100,000 this is still acceptable, but it is unnecessary and conceptually heavier than needed.

The key observation is that replacing a normal day with a superday does not change the structure of the schedule, it only adds a fixed extra amount of training. A normal day contributes 24 hours, while a superday contributes 72 hours, so the net gain of upgrading one day is 48 additional hours compared to leaving it normal. This transforms the problem into a simple incremental gain scenario: we start from all-normal days, compute the baseline total, and then ask how many 48-hour increments are needed to reach the target.

This reduces the problem to finding the smallest integer x such that 24d + 48x ≥ h. Solving this inequality directly gives a closed form expression using ceiling division, eliminating the need for any simulation over days.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d) | O(1) | Too slow conceptually |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total training time if all days are normal, which is 24 × d. This represents the baseline capacity without any upgrades.
2. If this baseline already meets or exceeds the target h, return 0 because no superdays are required.
3. Otherwise compute the remaining deficit, defined as h − 24 × d. This is the extra number of hours that must be supplied by upgrading some days.
4. Each superday contributes an additional 48 hours compared to a normal day, so determine how many such increments are needed to cover the deficit. This is computed as the smallest integer x such that 48 × x ≥ deficit.
5. Return x as the answer.

The correctness comes from the fact that every valid schedule can be transformed into one where all non-superdays are normal days and all superdays are identical upgrades. Since every upgrade has identical marginal benefit and there is no interaction between days, the problem becomes a simple linear coverage problem over a single variable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    d, h = map(int, input().split())
    
    base = 24 * d
    if base >= h:
        print(0)
        return
    
    deficit = h - base
    # each superday adds 48 extra hours compared to normal day
    x = (deficit + 48 - 1) // 48
    print(x)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the derived formula. The first step computes the baseline total. The early return handles the important boundary case where no upgrades are needed. The remaining computation performs a ceiling division, implemented using integer arithmetic to avoid floating point inaccuracies. The expression `(deficit + 47) // 48` ensures correct rounding up when the deficit is not divisible by 48.

## Worked Examples

### Example 1

Input:

```
3 147
```

We compute baseline values step by step.

| Step | Base (24d) | Deficit | Superdays (x) |
| --- | --- | --- | --- |
| Start | 72 | - | - |
| Compare | 72 | - | - |
| Compute deficit | - | 75 | - |
| Compute x | - | - | 2 |

The baseline 72 hours is insufficient. The remaining 75 hours must be covered by 48-hour increments. One superday is not enough, since it gives only 48 extra hours, while two superdays give 96 extra hours which is sufficient. This matches the output 2.

### Example 2

Input:

```
4 80
```

| Step | Base (24d) | Deficit | Superdays (x) |
| --- | --- | --- | --- |
| Start | 96 | - | - |
| Compare | 96 | - | - |
| Early exit | - | - | 0 |

The baseline already exceeds the requirement, so no upgrades are needed. This confirms that the algorithm correctly handles cases where the target is below the normal schedule capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within the constraints since it avoids any iteration over days and reduces the problem to direct arithmetic on the input values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    d, h = map(int, input().split())
    base = 24 * d
    if base >= h:
        return "0"
    deficit = h - base
    return str((deficit + 47) // 48)

# provided sample
assert run("3 147\n") == "2"

# minimum case, already satisfied
assert run("1 24\n") == "0"

# needs exactly one superday
assert run("1 25\n") == "1"

# large boundary where all days must be superdays
assert run("100000 7200000\n") == "100000"

# mixed case
assert run("10 300\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 24 | 0 | exact baseline equality |
| 1 25 | 1 | smallest positive deficit |
| 100000 7200000 | 100000 | full saturation case |
| 10 300 | 3 | typical mid-range computation |

## Edge Cases

One important boundary is when the requirement is already satisfied without upgrades. For input `d = 2, h = 40`, the baseline is 48 hours. The algorithm immediately returns zero after the comparison step, since no deficit is computed. This avoids any risk of negative arithmetic propagating into the ceiling formula.

Another case is when the deficit is smaller than a single superday contribution. For example `d = 1, h = 50`, the baseline is 24 and the deficit is 26. Since one superday adds 48 hours, the ceiling division produces 1, correctly selecting a single upgrade.

A final structural case occurs when every day must be upgraded. For `d = 3, h = 216`, the baseline is 72 and the deficit is 144. Each superday contributes 48, so exactly 3 superdays are required. The formula naturally saturates at `d` when the target approaches the maximum possible training total.
