---
title: "CF 168A - Wizards and Demonstration"
description: "The city has n total citizens. Among them, exactly x are wizards, and all of those wizards will attend the demonstration. Nobody else from the city will come."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 168
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 114 (Div. 2)"
rating: 900
weight: 168
solve_time_s: 83
verified: true
draft: false
---

[CF 168A - Wizards and Demonstration](https://codeforces.com/problemset/problem/168/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The city has `n` total citizens. Among them, exactly `x` are wizards, and all of those wizards will attend the demonstration. Nobody else from the city will come. To make the crowd look larger, the wizards can create clone puppets, and the administration cannot distinguish them from real people.

The administration reacts only if at least `y` percent of the city's population appears at the demonstration. The percentage is always measured against the original population size `n`, not including clones. The task is to compute the minimum number of clones needed so that the total number of attendees reaches the required threshold.

The constraints are tiny, all values are at most `10^4`. Even a linear simulation would easily fit inside the time limit. This means the problem is not about optimization pressure, it is about handling percentage calculations correctly. The main difficulty comes from rounding and integer arithmetic.

A common mistake is to compute the required attendance using floor division. Consider this input:

```
10 1 14
```

Fourteen percent of 10 is `1.4`, so at least 2 people must attend. A careless implementation might compute:

```
required = 10 * 14 // 100
```

which gives `1`, incorrectly concluding that no clone is needed.

Another subtle case appears when `y` exceeds 100:

```
10 10 150
```

The administration wants attendance equal to 150% of the population, meaning at least 15 attendees are needed. Since only 10 wizards exist, the answer is 5 clones. Any solution that assumes the required attendance never exceeds `n` will fail here.

One more edge case happens when the current number of wizards already satisfies the requirement exactly:

```
20 5 25
```

Twenty five percent of 20 is exactly 5. The answer must be 0. Off by one errors often appear when using incorrect ceiling logic.

## Approaches

The most direct approach is brute force simulation. Start with the existing `x` wizards attending the demonstration. Then repeatedly add one clone until the total attendance satisfies the percentage requirement. At each step, check whether:

$$\frac{x + \text{clones}}{n} \times 100 \ge y$$

Since the constraints are only `10^4`, even adding clones one by one would finish quickly. In the worst case, the answer is around `10^4`, so the loop performs only a few thousand iterations.

The brute force method works because the attendance increases monotonically. Once the condition becomes true, it stays true forever. The weakness is that it treats the problem as a search process even though the target can be computed directly.

The key observation is that the administration requires a minimum number of attendees equal to:

$$\left\lceil \frac{n \cdot y}{100} \right\rceil$$

This is the smallest integer not less than `n * y / 100`. Once we know this required attendance, the answer is simply:

$$\max(0, \text{required} - x)$$

The only real challenge is computing the ceiling correctly using integers. A standard trick for ceiling division is:

$$\left\lceil \frac{a}{b} \right\rceil = \frac{a + b - 1}{b}$$

using integer division.

That gives:

$$\text{required} = \frac{n \cdot y + 99}{100}$$

with floor division.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n`, `x`, and `y`.
2. Compute the minimum required attendance using ceiling division:

$$\text{required} = \left\lceil \frac{n \cdot y}{100} \right\rceil$$

In code, this becomes:

```
required = (n * y + 99) // 100
```

Adding 99 before integer division simulates taking the ceiling when dividing by 100.

1. Compute how many additional attendees are needed beyond the existing wizards:

```
answer = required - x
```

1. If this value is negative, print 0 instead. Negative means the wizards already satisfy the requirement without clones.

### Why it works

The administration requires at least `y%` of the original population `n`. The smallest integer satisfying that threshold is exactly:

$$\left\lceil \frac{n \cdot y}{100} \right\rceil$$

The demonstration already has `x` guaranteed attendees. Any missing attendees must come from clones, and each clone increases attendance by exactly one. Since every added clone contributes directly toward the target, the minimum number of clones is simply the gap between the required attendance and the current attendance.

The ceiling division guarantees that fractional attendance requirements are rounded upward correctly. Without that rounding, cases like 14% of 10 would incorrectly accept only one attendee.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, x, y = map(int, input().split())

required = (n * y + 99) // 100

print(max(0, required - x))
```

The program begins by reading the three integers. No loops or extra data structures are needed because the entire problem reduces to one arithmetic computation.

The expression:

```
(n * y + 99) // 100
```

implements ceiling division by 100. This is the most important part of the solution. Using ordinary floor division would fail whenever `n * y` is not divisible by 100.

For example:

```
10 * 14 = 140
```

Then:

```
(140 + 99) // 100 = 239 // 100 = 2
```

which correctly rounds upward.

Finally, `max(0, required - x)` prevents negative answers. If enough wizards already exist, no clones are needed.

Python integers easily handle the arithmetic here because the maximum product is only:

```
10^4 * 10^4 = 10^8
```

which is far below any overflow limit.

## Worked Examples

### Example 1

Input:

```
10 1 14
```

| Step | Value |
| --- | --- |
| n | 10 |
| x | 1 |
| y | 14 |
| n * y | 140 |
| required | (140 + 99) // 100 = 2 |
| clones needed | 2 - 1 = 1 |
| final answer | 1 |

The required attendance is 2 because 14% of 10 equals 1.4, and attendance must be an integer. One wizard already attends, so exactly one clone is needed.

### Example 2

Input:

```
10 10 100
```

| Step | Value |
| --- | --- |
| n | 10 |
| x | 10 |
| y | 100 |
| n * y | 1000 |
| required | (1000 + 99) // 100 = 10 |
| clones needed | 10 - 10 = 0 |
| final answer | 0 |

This trace shows the exact boundary where the current attendance already matches the required threshold. The algorithm correctly returns zero instead of a negative value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No additional memory proportional to input size is used |

The constraints are extremely small, so this constant time solution easily fits within the limits. Even a brute force simulation would pass, but the direct formula is cleaner and mathematically precise.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, x, y = map(int, input().split())

    required = (n * y + 99) // 100

    print(max(0, required - x))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("10 1 14\n") == "1\n", "sample 1"

# exact percentage already satisfied
assert run("20 5 25\n") == "0\n", "exact threshold"

# percentage greater than 100
assert run("10 10 150\n") == "5\n", "more than full population needed"

# minimum input size
assert run("1 1 1\n") == "0\n", "minimum values"

# off by one ceiling case
assert run("10 1 11\n") == "1\n", "11 percent of 10 requires 2 attendees"

# large values
assert run("10000 1 10000\n") == "999999\n", "large percentage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `20 5 25` | `0` | Exact threshold equality |
| `10 10 150` | `5` | Percentages larger than 100 |
| `1 1 1` | `0` | Minimum constraint values |
| `10 1 11` | `1` | Correct ceiling division |
| `10000 1 10000` | `999999` | Very large required attendance |

## Edge Cases

Consider the rounding case:

```
10 1 14
```

The algorithm computes:

```
required = (10 * 14 + 99) // 100
         = 239 // 100
         = 2
```

Then:

```
answer = 2 - 1 = 1
```

This correctly handles fractional percentages. A floor division approach would incorrectly produce only 1 required attendee.

Now consider a percentage above 100:

```
10 10 150
```

The computation becomes:

```
required = (10 * 150 + 99) // 100
         = 1599 // 100
         = 15
```

Since only 10 wizards exist:

```
answer = 15 - 10 = 5
```

The algorithm never assumes the target attendance is bounded by the population size.

Finally, examine the exact equality boundary:

```
20 5 25
```

The required attendance is:

```
required = (20 * 25 + 99) // 100
         = 599 // 100
         = 5
```

Then:

```
answer = 5 - 5 = 0
```

The `max(0, ...)` call guarantees that already sufficient attendance never produces a negative answer.
