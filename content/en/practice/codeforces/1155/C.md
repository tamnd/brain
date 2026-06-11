---
title: "CF 1155C - Alarm Clocks Everywhere"
description: "We are given several event times, already sorted in increasing order. Ivan wants to configure an alarm clock that rings periodically. Once the first ring happens at minute y, the clock continues ringing at times: y, y + p, y + 2p, y + 3p, ..."
date: "2026-06-12T02:42:10+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1155
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 63 (Rated for Div. 2)"
rating: 1300
weight: 1155
solve_time_s: 91
verified: true
draft: false
---

[CF 1155C - Alarm Clocks Everywhere](https://codeforces.com/problemset/problem/1155/C)

**Rating:** 1300  
**Tags:** math, number theory  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several event times, already sorted in increasing order. Ivan wants to configure an alarm clock that rings periodically. Once the first ring happens at minute `y`, the clock continues ringing at times:

`y, y + p, y + 2p, y + 3p, ...`

The starting time `y` can be any integer, but the period `p` must be chosen from a given list of allowed periods.

Our task is to determine whether there exists some allowed period such that every event time belongs to the ringing sequence. If such a period exists, we must output a valid starting minute and the index of the chosen period.

The constraints immediately suggest that the solution must be close to linear. Both `n` and `m` can reach `3·10^5`, so any algorithm that checks every event against every period would require about `9·10^10` operations in the worst case, which is completely infeasible.

The event times and periods can be as large as `10^18`. This rules out any approach that relies on arrays indexed by values or any simulation of the ringing process. We must work purely with arithmetic properties.

A subtle point is that the alarm may ring at additional times that are not event times. We only require every event time to be among the ringing moments. This distinction is crucial.

Consider:

```
x = [3, 12, 18]
p = 3
```

The ringing sequence starting at `3` is:

```
3, 6, 9, 12, 15, 18, ...
```

The extra rings at `6`, `9`, and `15` are completely acceptable.

Another easy mistake is to focus only on consecutive differences.

Example:

```
x = [1, 7, 13]
```

The differences are:

```
6, 6
```

A period of `6` works.

But for:

```
x = [1, 7, 19]
```

The differences are:

```
6, 12
```

A period of `6` still works because all event times are congruent modulo `6`.

The key object is not the individual differences but their greatest common divisor.

A final edge case occurs when no allowed period divides the required structure.

Example:

```
x = [1, 7, 13]
allowed periods = [4, 5]
```

All event times are congruent modulo `6`, but neither `4` nor `5` can generate them all, so the answer is `NO`.

## Approaches

The most direct idea is to try every allowed period. For a chosen period `p`, we could check whether all event times belong to the same residue class modulo `p`.

If every event satisfies:

```
xi ≡ x1 (mod p)
```

then choosing `y = x1` works.

This test is correct because every ringing time generated from `x1` with period `p` has the same remainder modulo `p`.

The problem is the cost. There are up to `3·10^5` candidate periods and up to `3·10^5` event times. Testing every pair requires:

```
O(nm)
```

operations, which is far too large.

The crucial observation comes from rewriting the congruence condition.

If all event times must satisfy:

```
xi ≡ x1 (mod p)
```

then:

```
p | (xi - x1)
```

for every `i`.

A number that divides every value in a collection must divide their greatest common divisor. Let

```
g = gcd(x2 - x1, x3 - x1, ..., xn - x1)
```

Then any valid period must divide `g`.

This completely changes the problem.

Instead of testing every event against every period, we first compute the single number `g`. Then we only need to check whether some allowed period divides `g`.

If an allowed period `pj` satisfies:

```
g % pj == 0
```

then every difference `(xi - x1)` is divisible by `pj`, meaning all event times are congruent modulo `pj`. Choosing:

```
y = x1
```

works immediately.

This reduces the problem to a linear scan after one gcd computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the event times and allowed periods.
2. Compute:

```
g = gcd(x2 - x1, x3 - x1, ..., xn - x1)
```

This captures every divisibility constraint imposed by the event times.
3. Iterate through the allowed periods in their input order.
4. For each period `pj`, check whether:

```
g % pj == 0
```

If this holds, then `pj` divides every difference `(xi - x1)`.
5. As soon as such a period is found, output:

```
YES
x1 j
```

where `j` is the 1-based index of the period.
6. If no allowed period divides `g`, output:

```
NO
```

### Why it works

Let

```
g = gcd(x2 - x1, ..., xn - x1).
```

If a period `p` is valid, then every event time must satisfy:

```
xi ≡ x1 (mod p).
```

Equivalently,

```
p | (xi - x1)
```

for every `i`.

Since `p` divides every difference, it must divide their gcd `g`.

Conversely, if an allowed period `p` divides `g`, then it divides every difference `(xi - x1)`. Hence:

```
xi ≡ x1 (mod p)
```

for all `i`.

Choosing `y = x1` produces a ringing sequence containing every event time. Thus the condition `p | g` is both necessary and sufficient.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    x = list(map(int, input().split()))
    p = list(map(int, input().split()))

    g = 0
    for i in range(1, n):
        g = gcd(g, x[i] - x[0])

    for idx, period in enumerate(p, start=1):
        if g % period == 0:
            print("YES")
            print(x[0], idx)
            return

    print("NO")

solve()
```

The first part computes the gcd of all differences relative to the first event. Initializing `g` with zero is convenient because:

```
gcd(0, a) = a
```

so the first difference automatically becomes the starting value.

The second loop scans the allowed periods. The moment a divisor of `g` is found, the answer is known and we can terminate immediately.

Using `x[0]` as the starting time is sufficient because every event time has the same remainder modulo the chosen period. No search for `y` is necessary.

Python integers handle values up to `10^18` without overflow concerns.

## Worked Examples

### Example 1

Input:

```
3 5
3 12 18
2 6 5 3 3
```

Differences relative to `3`:

```
9, 15
```

| Step | Value |
| --- | --- |
| Initial g | 0 |
| gcd(0, 9) | 9 |
| gcd(9, 15) | 3 |

Now scan periods:

| Index | Period | g % Period |
| --- | --- | --- |
| 1 | 2 | 1 |
| 2 | 6 | 3 |
| 3 | 5 | 3 |
| 4 | 3 | 0 |

The first valid period appears at index 4.

Output:

```
YES
3 4
```

This trace demonstrates the central theorem. Once `g = 3`, any valid period must divide `3`.

### Example 2

Input:

```
3 2
1 7 13
4 5
```

Differences relative to `1`:

```
6, 12
```

| Step | Value |
| --- | --- |
| Initial g | 0 |
| gcd(0, 6) | 6 |
| gcd(6, 12) | 6 |

Scan periods:

| Index | Period | g % Period |
| --- | --- | --- |
| 1 | 4 | 2 |
| 2 | 5 | 1 |

No period divides `6`.

Output:

```
NO
```

This example shows that having a consistent arithmetic progression structure is not enough. One of the allowed periods must actually divide the gcd.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass for gcd computation and one pass through periods |
| Space | O(1) | Only a few variables besides the input arrays |

The algorithm performs a linear amount of work and uses constant extra memory. With `n, m ≤ 3·10^5`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    x = list(map(int, input().split()))
    p = list(map(int, input().split()))

    g = 0
    for i in range(1, n):
        g = gcd(g, x[i] - x[0])

    for idx, period in enumerate(p, start=1):
        if g % period == 0:
            return f"YES\n{x[0]} {idx}\n"

    return "NO\n"

# provided sample
assert run(
    "3 5\n"
    "3 12 18\n"
    "2 6 5 3 3\n"
) == "YES\n3 4\n"

# minimum size
assert run(
    "2 1\n"
    "1 2\n"
    "1\n"
) == "YES\n1 1\n"

# no valid period
assert run(
    "3 2\n"
    "1 7 13\n"
    "4 5\n"
) == "NO\n"

# gcd has several divisors, first valid index should be returned
assert run(
    "3 3\n"
    "5 17 29\n"
    "4 6 12\n"
) == "YES\n5 1\n"

# large values
assert run(
    "2 1\n"
    "1 1000000000000000000\n"
    "1\n"
) == "YES\n1 1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2 / 1` | YES | Minimum valid instance |
| `1 7 13` with periods `4 5` | NO | No divisor of gcd exists |
| `5 17 29` with periods `4 6 12` | YES, index 1 | Multiple valid divisors, first one found |
| Large `10^18` values | YES | Correct handling of 64-bit sized integers |

## Edge Cases

Consider:

```
3 2
1 7 19
6 12
```

The differences are `6` and `18`, giving:

```
g = 6
```

The algorithm checks period `6` and accepts it. A common mistake is to require all consecutive differences to equal the chosen period. Here the differences are not equal, yet a period of `6` is perfectly valid because all event times share the same residue modulo `6`.

Consider:

```
3 2
1 7 13
4 5
```

We obtain:

```
g = 6
```

Neither `4` nor `5` divides `6`, so the algorithm outputs `NO`. This handles the situation where the event structure admits a valid period, but none of the allowed options provide it.

Consider:

```
2 3
10 25
3 5 15
```

The gcd is:

```
g = 15
```

The algorithm finds that `3` divides `15` and outputs:

```
YES
10 1
```

Some solutions mistakenly search for an exact difference match and would only accept `15`. Any divisor of the gcd is valid, because all event times remain congruent modulo that divisor.
