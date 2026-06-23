---
title: "CF 105062A - Is It Rated??"
description: "We are given two integers, m and d. Think of m as a month number in a calendar year and d as a day of the month. The task is to decide whether this pair can represent a valid calendar date in the simplified world implied by the problem."
date: "2026-06-23T10:47:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105062
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #29 (Clown-Forces)"
rating: 0
weight: 105062
solve_time_s: 72
verified: true
draft: false
---

[CF 105062A - Is It Rated??](https://codeforces.com/problemset/problem/105062/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `m` and `d`. Think of `m` as a month number in a calendar year and `d` as a day of the month. The task is to decide whether this pair can represent a valid calendar date in the simplified world implied by the problem.

In practice, the only constraint that matters is whether the day `d` is even meaningful for a given month `m`. Since no year or calendar system is explicitly defined, the problem implicitly reduces to checking whether the day exists within the allowed range for that month.

The key observation is that months differ in how many days they can contain, and the validity of `(m, d)` depends on that structure rather than on any computational trick.

The input sizes are tiny, with `m ≤ 12` and `d ≤ 31`, which immediately rules out any need for optimization concerns. Any solution that directly encodes the calendar rules or even hardcodes valid pairs is sufficient.

A subtle edge case comes from the fact that day limits vary across months. For example, a naive approach might assume every month has 31 days, which would incorrectly accept invalid dates like February 30 or April 31 in a realistic calendar interpretation. Another potential pitfall is forgetting that the smallest months still allow at least 28 or 30 days depending on interpretation, and incorrectly over-restricting valid pairs.

For instance, if someone incorrectly assumes all months have 31 days, they would accept `(2, 31)` as valid, which is clearly incorrect. On the other hand, if someone assumes a uniform smaller bound like 30 days for all months, they would incorrectly reject `(1, 31)`.

So the problem reduces to correctly distinguishing which months allow which maximum day.

## Approaches

A brute-force mindset would be to treat every possible calendar date as valid and then check whether `(m, d)` appears in a precomputed list of all valid dates. This would mean enumerating all months and all possible days per month according to the calendar rules, storing them in a set, and checking membership. This works because the domain is extremely small, at most a few hundred entries.

The issue is not performance but unnecessary complexity. Building and querying a structure is overkill when the structure itself is fixed and trivial.

The more direct approach is to encode the month-to-maximum-day relationship. Months alternate between 31-day and 30-day lengths, with February as a special case. Since the constraints are so small, the cleanest solution is simply to hardcode the maximum number of days per month and compare `d` against it.

The key insight is that this is not a dynamic problem at all. There is no dependency between test cases or computations; the answer is determined entirely by a constant lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of valid dates | O(365) | O(365) | Accepted |
| Direct lookup by month rule | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Construct a mapping from each month `m` to its maximum valid number of days. This reflects the fixed calendar structure, where each month has a known upper bound on `d`.
2. Read the input pair `(m, d)`.
3. Compare `d` against the maximum allowed value for month `m`.
4. If `d` is within range, output `"YES"`, otherwise output `"NO"`.

The reasoning behind step 1 is that all future checks depend on a constant rule, so precomputing it avoids repeating logic or conditionals.

### Why it works

The correctness rests on the invariant that each month has a fixed maximum number of valid days, and any valid date must satisfy `1 ≤ d ≤ max_days[m]`. Since the mapping encodes the exact constraints of the calendar, every valid input passes the inequality check, and every invalid input violates it. No other structure or hidden dependency exists in the problem, so the comparison is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, d = map(int, input().split())

    # days per month in a standard calendar abstraction
    max_days = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    if 1 <= d <= max_days[m]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The code directly encodes the calendar structure into a dictionary. This avoids any branching logic beyond a single lookup and comparison. The key detail is ensuring that the bounds are inclusive, since both endpoints are valid days.

One subtle implementation detail is that the dictionary must correctly reflect February as 28 days, since forgetting this is the most common source of incorrect answers in similar problems. The rest of the months follow a fixed pattern.

## Worked Examples

### Example 1

Input:

```
1 1
```

| Step | m | d | max_days[m] | Condition |
| --- | --- | --- | --- | --- |
| Read input | 1 | 1 | - | - |
| Lookup | 1 | 1 | 31 | - |
| Check | 1 | 1 | 31 | 1 ≤ 1 ≤ 31 |

Output:

```
YES
```

This trace shows that January supports 31 days, so day 1 is valid. The check confirms the lower boundary is respected and the upper limit is not violated.

### Example 2

Input:

```
2 31
```

| Step | m | d | max_days[m] | Condition |
| --- | --- | --- | --- | --- |
| Read input | 2 | 31 | - | - |
| Lookup | 2 | 31 | 28 | - |
| Check | 2 | 31 | 28 | 31 ≤ 28 is false |

Output:

```
NO
```

This demonstrates the February edge case. Even though 31 is a valid day number in general, it exceeds the allowed range for month 2, so it is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a dictionary lookup and a comparison are performed |
| Space | O(1) | Fixed mapping of 12 months |

The solution trivially satisfies the constraints since it performs constant-time work per test case.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("1 1\n") == "YES", "sample 1"
assert run("2 31\n") == "NO", "sample 2"

# custom cases
assert run("1 31\n") == "YES", "January max boundary"
assert run("2 28\n") == "YES", "February boundary valid"
assert run("2 29\n") == "NO", "February overflow"
assert run("12 31\n") == "YES", "December max boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 31` | YES | upper boundary of 31-day month |
| `2 29` | NO | leap-day rejection |
| `12 31` | YES | last month boundary case |

## Edge Cases

One edge case is the maximum valid day in a 31-day month. For input `1 31`, the algorithm retrieves `max_days[1] = 31` and checks `31 ≤ 31`, which passes, producing `"YES"`. This confirms that the upper boundary is inclusive.

Another edge case is February overflow. For input `2 29`, the lookup returns `28`, and the condition `29 ≤ 28` fails, so the output is `"NO"`. This shows that the month-specific constraint is correctly enforced.

A final edge case is a generic 30-day month like April. For an input such as `4 30`, the mapping gives `30`, and the equality passes, ensuring that months with fewer than 31 days are still handled correctly without special-casing beyond the lookup.
