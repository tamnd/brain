---
title: "CF 168A - Wizards and Demonstration"
description: "The city has n real residents. Among them, exactly x are wizards, and all of those wizards will attend a demonstration. Nobody else will attend. The administration measures attendance as a percentage of the real city population, which remains n even if the wizards create clones."
date: "2026-06-02T08:31:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 168
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 114 (Div. 2)"
rating: 900
weight: 168
solve_time_s: 121
verified: true
draft: false
---

[CF 168A - Wizards and Demonstration](https://codeforces.com/problemset/problem/168/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

The city has `n` real residents. Among them, exactly `x` are wizards, and all of those wizards will attend a demonstration. Nobody else will attend.

The administration measures attendance as a percentage of the real city population, which remains `n` even if the wizards create clones. A clone counts as an attendee but does not increase the population size used in the percentage calculation.

We must find the smallest number of clones so that the total attendance, which is `x + clones`, is at least `y%` of `n`.

The constraints are tiny. Every value is at most `10^4`, so even a simple simulation would run comfortably within the time limit. Still, the problem has a direct mathematical solution that computes the answer in constant time.

The main subtlety is that attendance is an integer count of people. If the required percentage corresponds to a non-integer number of attendees, we must round up.

Consider `n = 10`, `x = 1`, `y = 14`.

Fourteen percent of ten people is `1.4`. Since attendance must be an integer, at least `2` attendees are required. One wizard already attends, so one clone is needed.

A common mistake is to compute `(n * y) // 100`, which rounds down. Here it gives `1`, incorrectly suggesting that no clone is required.

Another edge case appears when the existing wizards already satisfy the requirement.

For example:

```
10 10 100
```

The required attendance is `10`, and all ten wizards already attend. The correct answer is `0`. A careless implementation that always computes `required - x` without taking a maximum with zero could produce a negative answer in other cases.

The statement also allows percentages greater than 100.

For example:

```
10 10 150
```

The required attendance is `15`, even though the city has only 10 residents. Since clones are allowed, the answer is `5`. Any solution that assumes percentages never exceed 100 would fail here.

## Approaches

A straightforward approach is to try clone counts starting from zero. For each candidate value `c`, check whether `x + c` attendees are enough to reach at least `y%` of the city's population. The first valid `c` is the answer.

This works because clone counts are examined in increasing order, so the first successful value is minimal. With the given constraints, the answer can never exceed roughly `10^4`, making even this brute-force simulation fast enough.

The reason the problem becomes simpler is that the requirement can be expressed directly as a minimum attendance count.

We need:

$$x + c \ge \frac{n \cdot y}{100}$$

Since attendance must be an integer, the true requirement is:

$$x + c \ge \left\lceil \frac{n \cdot y}{100} \right\rceil$$

Let

$$required = \left\lceil \frac{n \cdot y}{100} \right\rceil$$

Then the smallest clone count is simply:

$$required - x$$

unless that value is negative, in which case the answer is zero.

The only remaining task is computing the ceiling of an integer division. A standard formula is:

$$\left\lceil \frac{a}{b} \right\rceil = \frac{a+b-1}{b}$$

using integer division.

So:

```
required = (n * y + 99) // 100
answer = max(0, required - x)
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `x`, and `y`.
2. Compute the minimum attendance needed to satisfy the percentage requirement:

$$required = \left\lceil \frac{n \cdot y}{100} \right\rceil$$

Since all values are integers, use:

```
required = (n * y + 99) // 100
```
3. Compute how many additional attendees are needed beyond the existing `x` wizards:

```
required - x
```
4. If this value is negative, no clones are necessary. Return:

```
max(0, required - x)
```

### Why it works

The administration only cares about the final attendee count relative to the fixed population size `n`. The smallest valid attendance is exactly the ceiling of `n * y / 100`, because attendance must be an integer.

Any attendance smaller than `required` fails the percentage condition, while any attendance at least `required` succeeds. Since `x` wizards already attend, the minimum number of clones is precisely the deficit between `required` and `x`, with zero used when no deficit exists. This directly yields the unique minimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x, y = map(int, input().split())

required = (n * y + 99) // 100
print(max(0, required - x))
```

The first line reads the three input values.

The key computation is:

```
required = (n * y + 99) // 100
```

This performs ceiling division by 100. For example, if `n * y = 140`, then:

```
(140 + 99) // 100 = 239 // 100 = 2
```

which correctly computes `ceil(1.4)`.

The final answer is:

```
max(0, required - x)
```

This handles both situations. If more attendees are needed, the difference gives the required clone count. If the existing wizards already satisfy the target, the result becomes negative and is replaced by zero.

No overflow concerns exist because `n * y ≤ 10^8`, which is easily handled by Python integers.

## Worked Examples

### Sample 1

Input:

```
10 1 14
```

| Variable | Value |
| --- | --- |
| n | 10 |
| x | 1 |
| y | 14 |
| n × y | 140 |
| required | (140 + 99) // 100 = 2 |
| required - x | 1 |
| answer | 1 |

The required attendance is 2 people because 14% of 10 equals 1.4 and must be rounded up. One wizard already attends, so one clone is needed.

### Sample 2

Input:

```
10 10 100
```

| Variable | Value |
| --- | --- |
| n | 10 |
| x | 10 |
| y | 100 |
| n × y | 1000 |
| required | (1000 + 99) // 100 = 10 |
| required - x | 0 |
| answer | 0 |

All ten wizards already attend, exactly meeting the required attendance. No clones are necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The algorithm uses constant time and constant memory regardless of the input values. This is far below the limits and easily fits within the allowed resources.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    n, x, y = map(int, input().split())
    required = (n * y + 99) // 100
    print(max(0, required - x))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("10 1 14\n") == "1\n", "sample 1"

# equivalent to the statement's second example
assert run("10 10 100\n") == "0\n", "sample 2"

# minimum-size input
assert run("1 1 1\n") == "0\n", "minimum values"

# off-by-one ceiling case
assert run("10 1 11\n") == "1\n", "11% of 10 requires 2 attendees"

# percentage above 100
assert run("10 10 150\n") == "5\n", "clones beyond population"

# maximum values
assert run("10000 10000 10000\n") == "990000\n", "largest inputs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Smallest legal input |
| `10 1 11` | `1` | Correct ceiling rounding |
| `10 10 150` | `5` | Percentages greater than 100 |
| `10000 10000 10000` | `990000` | Largest values and large answer |

## Edge Cases

Consider:

```
10 1 14
```

The algorithm computes:

```
required = (10 * 14 + 99) // 100
         = 239 // 100
         = 2
```

The answer becomes:

```
max(0, 2 - 1) = 1
```

This correctly handles non-integer percentages. A floor division approach would incorrectly require only one attendee.

Now consider:

```
10 10 100
```

We obtain:

```
required = 10
answer = max(0, 10 - 10) = 0
```

The existing wizards already satisfy the requirement, so no clones are created.

Finally, consider:

```
10 10 150
```

The computation gives:

```
required = (1500 + 99) // 100
         = 15
answer = max(0, 15 - 10)
         = 5
```

The algorithm does not assume the percentage is at most 100. It correctly determines that five additional clones are needed to reach fifteen attendees.
