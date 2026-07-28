---
title: "CF 102747A - \u041b\u0435\u0442\u043e\u0438\u0441\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0435"
description: "The problem uses a historical year numbering system where there is no year zero. Years after the beginning of the era are written as positive integers, while years before it are written as negative integers. The sequence of years is therefore: ..., -3, -2, -1, 1, 2, 3, ..."
date: "2026-07-29T00:42:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102747
codeforces_index: "A"
codeforces_contest_name: "\u041f\u0440\u0438\u0433\u043b\u0430\u0441\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f. \u0421\u0438\u0440\u0438\u0443\u0441-2020"
rating: 0
weight: 102747
solve_time_s: 90
verified: true
draft: false
---

[CF 102747A - \u041b\u0435\u0442\u043e\u0438\u0441\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/102747/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem uses a historical year numbering system where there is no year zero. Years after the beginning of the era are written as positive integers, while years before it are written as negative integers. The sequence of years is therefore:

`..., -3, -2, -1, 1, 2, 3, ...`

We are given the year in which one event happened and the number of years separating it from another event. A positive separation means moving forward in time, while a negative separation means moving backward. The task is to find the year of the second event using this unusual numbering system.

The values can be as large as $10^9$ in absolute value. This immediately rules out simulating the movement year by year, because a loop of that size would require up to two billion iterations. The solution must use direct arithmetic with constant time operations.

The tricky part is that ordinary integer addition does not work because the calendar jumps from year `-1` directly to year `1`. For example, moving one year after `-1` gives `1`, not `0`. Any solution that simply calculates `A + n` will fail around this transition.

Consider the input:

```
-1
1
```

The correct output is:

```
1
```

A careless implementation using normal arithmetic would produce `0`, which is not a valid year.

Another boundary case is moving backward from the first positive year:

```
1
-1
```

The correct output is:

```
-1
```

Normal subtraction gives `0`, again producing a nonexistent year.

## Approaches

The direct approach is to repeatedly move from the current year toward the target. If the distance is positive, we increment the year one step at a time. If the distance is negative, we decrement it one step at a time. This is easy to understand because every operation represents exactly one year of movement. However, if the distance has absolute value $10^9$, this performs one billion iterations, which is far beyond what a program can finish within the time limit.

The key observation is that the only unusual part of the calendar is the missing year zero. We can temporarily convert the historical year numbering into a normal continuous integer line.

For this conversion, map every positive year to itself. Negative years are shifted by one because the missing zero creates a gap. The transformation is:

```
year > 0  -> year
year < 0  -> year + 1
```

Now the sequence becomes continuous:

```
-3 -> -2
-2 -> -1
-1 -> 0
 1 -> 1
 2 -> 2
 3 -> 3
```

In this transformed space, moving by `n` years is just adding `n`. After that, we convert the result back. Values greater than zero are already positive years, while zero and negative values correspond to years before the era and need to be shifted back by one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | n | ) |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the starting year into a continuous representation. If the year is positive, keep it unchanged. If it is negative, add one to it so that year `-1` becomes zero.
2. Add the given number of years to the transformed value. This works because the transformed timeline has no gaps.
3. Convert the transformed year back into the original calendar format. Positive transformed values remain unchanged, while zero and negative transformed values are decreased by one.

Why it works: the transformation creates a one-to-one mapping between real historical years and ordinary integers. Every adjacent year in history becomes an adjacent integer, including the transition between `-1` and `1`. Since the distance between events is preserved by this mapping, adding `n` in the transformed space gives exactly the correct destination year. The reverse transformation restores the required historical notation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_linear(year):
    if year > 0:
        return year
    return year + 1

def from_linear(value):
    if value > 0:
        return value
    return value - 1

def solve():
    a = int(input())
    n = int(input())

    current = to_linear(a)
    answer = from_linear(current + n)

    print(answer)

if __name__ == "__main__":
    solve()
```

The function `to_linear` removes the missing-year gap. The important boundary is `-1`, which becomes `0`, making it directly adjacent to year `1`, represented as `1`.

The addition is done only after the conversion, so the program never creates the invalid year zero as a final answer. The function `from_linear` handles the reverse conversion by moving all non-positive transformed values back into negative historical years.

No loops or large arrays are used, so the implementation remains constant time even for the largest allowed values.

## Worked Examples

### Sample 1

Input:

```
5
-3
```

| Step | Original year | Linear value | Operation |
| --- | --- | --- | --- |
| Start | 5 | 5 | Convert positive year directly |
| Move | 5 | 2 | Add -3 |
| Restore | 2 | 2 | Positive linear value stays positive |

The output is:

```
2
```

The example shows that ordinary addition becomes valid after removing the year zero gap.

### Sample 2

Input:

```
-3
1
```

| Step | Original year | Linear value | Operation |
| --- | --- | --- | --- |
| Start | -3 | -2 | Add one because the year is negative |
| Move | -3 | -1 | Add 1 |
| Restore | -1 | -2 | Convert back to historical notation |

The output is:

```
-2
```

This example crosses the negative-year region and confirms that the reverse transformation correctly restores the original numbering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs only a few arithmetic operations |
| Space | O(1) | It stores only several integer variables |

The maximum input size only affects the magnitude of the integers, not the amount of work. Python integers can handle these values directly, so the solution fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def to_linear(year):
        return year if year > 0 else year + 1

    def from_linear(value):
        return value if value > 0 else value - 1

    a = int(sys.stdin.readline())
    n = int(sys.stdin.readline())
    ans = from_linear(to_linear(a) + n)

    sys.stdin = old_stdin
    return str(ans) + "\n"

# provided samples
assert run("5\n-3\n") == "2\n", "sample 1"
assert run("-3\n1\n") == "-2\n", "sample 2"

# custom cases
assert run("-1\n1\n") == "1\n", "crossing from last BCE year"
assert run("1\n-1\n") == "-1\n", "crossing from first CE year"
assert run("-1000000000\n2000000000\n") == "1000000000\n", "large values"
assert run("100\n0\n") == "100\n", "zero distance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `-1` and `1` | `1` | Crossing the missing year zero forward |
| `1` and `-1` | `-1` | Crossing the missing year zero backward |
| `-1000000000` and `2000000000` | `1000000000` | Handling extreme values without simulation |
| `100` and `0` | `100` | No movement case |

## Edge Cases

For the input:

```
-1
1
```

the algorithm converts `-1` into linear value `0`. After adding one year, the value becomes `1`. Since it is positive, the reverse conversion returns `1`. This avoids ever outputting the invalid year zero.

For the input:

```
1
-1
```

the algorithm converts `1` into linear value `1`. Subtracting one gives `0`. The reverse conversion changes zero into `-1`, correctly returning the year immediately before the era.

For the input:

```
-1000000000
2000000000
```

the conversion changes the starting value to `-999999999`. Adding the distance gives `1000000001`, which converts back to `1000000001`. The calculation remains constant time because it never walks through individual years.
