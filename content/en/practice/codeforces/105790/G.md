---
title: "CF 105790G - Gargantua"
description: "The situation describes two astronauts and a relativistic time difference caused by a black hole system. One astronaut, Leo, remains on Earth while the other, Ema, travels to a distant planet where time flows more slowly."
date: "2026-06-25T23:32:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "G"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 44
verified: true
draft: false
---

[CF 105790G - Gargantua](https://codeforces.com/problemset/problem/105790/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The situation describes two astronauts and a relativistic time difference caused by a black hole system. One astronaut, Leo, remains on Earth while the other, Ema, travels to a distant planet where time flows more slowly. The key detail is that time on the planet does not match Earth time linearly one-to-one, but is stretched by a fixed factor.

We are given three integers. The first is Leo’s initial age at the moment Ema leaves Earth. The second is a time dilation factor indicating how much slower time passes on the planet compared to Earth. The third is how many years Ema spends on the planet according to the planet’s own clock.

The task is to determine Leo’s age when Ema returns to Earth, which depends entirely on how much Earth time passes during Ema’s trip.

The key interpretation step is converting the time spent on the planet into Earth time. If one year on the planet corresponds to X years on Earth, then a duration of Y planetary years corresponds to X × Y Earth years. Leo ages normally during this entire Earth interval.

The input limits are extremely small, with all values bounded by 100. This immediately rules out any need for optimization or advanced data structures. Even a direct arithmetic computation is sufficient in constant time.

A subtle failure case appears when the multiplication step is mishandled. For example, if X and Y are treated as floating-point or if integer overflow were possible in larger constraints, the result could be incorrect. Here, however, values are small enough that standard integer arithmetic is safe.

Another potential mistake is misinterpreting the time dilation direction. The phrase “time passes X times slower” can be incorrectly read as division instead of multiplication. If someone computes Y / X instead of X × Y, they would get smaller and incorrect results even on simple inputs like A = 20, X = 3, Y = 4, where the correct Earth time contribution is 12, not 1.

## Approaches

The naive interpretation of the process would simulate time year by year. One could imagine advancing Ema’s stay one planetary year at a time and converting each to Earth time by multiplying by X, then incrementing Leo’s age accordingly. This works logically but introduces unnecessary iteration over Y steps. Each step performs constant work, so the total complexity is O(Y), which is still trivial here but becomes conceptually inefficient.

The key observation is that the transformation from planetary time to Earth time is linear and uniform. Every single unit of time on the planet expands into exactly X units on Earth. Because of this fixed ratio, the entire duration can be converted in one multiplication instead of repeated accumulation.

This reduces the problem to a direct arithmetic expression: Leo’s final age equals initial age plus total Earth time elapsed during Ema’s mission, which is X × Y.

There is no dependency between intermediate states, so no simulation or state tracking is required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(Y) | O(1) | Accepted but unnecessary |
| Direct computation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the initial age A, the time dilation factor X, and the planetary duration Y. These are independent scalar values describing the system state.
2. Compute the total Earth time that passes during Ema’s mission by multiplying X and Y. This conversion reflects the physical relationship between the two time scales.
3. Add this Earth time to Leo’s initial age A. Leo ages at the same rate as Earth time, so every Earth year increases his age by one.
4. Output the resulting value as Leo’s age at the moment Ema returns.

## Why it works

The correctness relies on the fact that the time dilation is constant across the entire interval. Each planetary year contributes exactly X Earth years, so the mapping from planetary duration to Earth duration is a linear scaling. Since Leo’s aging depends only on Earth time and not on Ema’s local time, the result is fully determined by A + X × Y. No intermediate interactions or state changes affect the outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input().strip())
    x = int(input().strip())
    y = int(input().strip())
    print(a + x * y)

if __name__ == "__main__":
    solve()
```

The solution reads three integers from separate lines, as specified. The multiplication `x * y` is performed directly without any loop or conversion. The result is added to `a`, which already represents Leo’s initial age.

A common implementation mistake is trying to read all values from a single line, but the input format explicitly places each value on its own line, so each call to `input()` must be handled separately.

Another detail is ensuring the multiplication happens before addition, although operator precedence makes the expression `a + x * y` naturally correct.

## Worked Examples

### Example 1

Input:

```
20
3
4
```

We track the computation:

| Step | A | X | Y | Earth Time (X×Y) | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 20 | 3 | 4 | - | - |
| Compute Earth time | 20 | 3 | 4 | 12 | - |
| Add to age | 20 | 3 | 4 | 12 | 32 |

This demonstrates that Leo experiences 12 additional Earth years during Ema’s mission, leading to a final age of 32.

### Example 2

Input:

```
31
17
3
```

| Step | A | X | Y | Earth Time (X×Y) | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 31 | 17 | 3 | - | - |
| Compute Earth time | 31 | 17 | 3 | 51 | - |
| Add to age | 31 | 17 | 3 | 51 | 82 |

Here, the mission corresponds to 51 Earth years, so Leo’s age increases accordingly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed regardless of input values |
| Space | O(1) | No additional data structures are used |

The constraints ensure all values are small integers, so the computation is instantaneous and well within limits for any standard runtime environment.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = int(sys.stdin.readline().strip())
    x = int(sys.stdin.readline().strip())
    y = int(sys.stdin.readline().strip())
    return str(a + x * y)

# provided samples
assert run("20\n3\n4\n") == "32", "sample 1"
assert run("31\n17\n3\n") == "82", "sample 2"

# custom cases
assert run("0\n0\n10\n") == "0", "zero factor eliminates time growth"
assert run("10\n1\n0\n") == "10", "no travel time means no change"
assert run("5\n2\n10\n") == "25", "basic scaling check"
assert run("100\n100\n1\n") == "200", "boundary multiplication case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0,0,10 | 0 | Zero dilation factor |
| 10,1,0 | 10 | Zero duration |
| 5,2,10 | 25 | Standard linear scaling |
| 100,100,1 | 200 | Upper-bound multiplication |

## Edge Cases

A direct corner case is when the time dilation factor is zero. In that case, no Earth time passes regardless of how long Ema stays on the planet. For input `A=10, X=0, Y=100`, the computation yields `10 + 0 = 10`, meaning Leo does not age during the mission interval.

Another case is when Ema does not spend any time on the planet. For `A=10, X=5, Y=0`, the Earth time contribution becomes zero, and Leo’s age remains unchanged at 10.

A final boundary case is when all values are maximal within constraints, such as `A=100, X=100, Y=100`. The multiplication yields 10000 Earth years, resulting in a final age of 10100, which still fits easily within integer limits and demonstrates that no overflow precautions are required in this problem setting.
