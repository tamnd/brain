---
title: "CF 102811A - \u0410\u0432\u0442\u043e\u0431\u0443\u0441\u043d\u044b\u0435 \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438"
description: "The street has bus stops placed at regular intervals. If the first stop is at position 0, then every following stop is exactly K meters farther, so their positions are multiples of K."
date: "2026-07-26T16:11:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102811
codeforces_index: "A"
codeforces_contest_name: "\u0428\u043a\u043e\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0432\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041c\u043e\u0441\u043a\u0432\u0430  (\u0432\u0435\u0440\u0441\u0438\u044f CF)"
rating: 0
weight: 102811
solve_time_s: 35
verified: true
draft: false
---

[CF 102811A - \u0410\u0432\u0442\u043e\u0431\u0443\u0441\u043d\u044b\u0435 \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/102811/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The street has bus stops placed at regular intervals. If the first stop is at position 0, then every following stop is exactly K meters farther, so their positions are multiples of K. Sveta has already walked N meters from the beginning of the street and wants to know the shortest distance she must walk to reach any bus stop.

The input contains the interval between stops K and Sveta's current distance from the start N. The output is the minimum distance from position N to a position that is a multiple of K.

The values of K and N can be as large as 2 * 10^9. This immediately rules out simulating the street or checking every stop one by one. In the worst case there could be billions of possible stops, and even an O(N) solution would require far too many operations. The solution must use only a constant number of arithmetic operations.

The main edge cases come from positions that are exactly on a stop or very close to the beginning of an interval. A careless solution that always moves forward to the next stop would fail on these cases.

For example, with input:

```
5
10
```

the stops are at positions 0, 5, 10, 15 and so on. Sveta is already at a stop, so the correct answer is 0. A solution that only calculates the distance to the next stop would incorrectly return 5.

Another boundary case is when the nearest stop is the previous one rather than the next one. For example:

```
10
14
```

The closest stops are 10 and 20. The distances are 4 and 6, so the answer is 4. A solution that always rounds upward would return 6.

A final case is when Sveta is before the first non-zero stop:

```
100
1
```

The closest stops are 0 and 100. The answer is 1. The beginning of the street must be treated as a valid bus stop.

## Approaches

A straightforward approach would be to generate every bus stop position and compare its distance from Sveta. Starting from position 0, we could check 0, K, 2K, 3K and continue until the distance becomes larger than the current best answer.

This approach is correct because every possible destination is examined. However, it is far too slow for the given limits. If K is 1 and N is 2 * 10^9, there are two billion stops before reaching Sveta's position. A loop with billions of iterations cannot finish within the time limit.

The useful observation is that Sveta's position only depends on the nearest multiples of K. The bus stop immediately before her is at distance N divided by K, rounded down, multiplied by K. The next stop is exactly K meters after that. There is no need to inspect any other stops because all other stops are farther away.

The problem becomes finding the remainder after division by K. If N = q * K + r, then r is the distance to the previous stop, while K - r is the distance to the next stop. We only need the smaller of these two values. When r is zero, Sveta is already at a stop and the answer is zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N / K) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the remainder of N divided by K. This remainder is the distance from Sveta's position back to the previous bus stop because every stop position is a multiple of K.
2. If the remainder is zero, output zero. Sveta is standing exactly on a bus stop, so no movement is required.
3. Otherwise, compare the remainder with K minus the remainder. The first value is the distance to the previous stop, and the second value is the distance to the next stop. The smaller one is the required walking distance.

The reason only two distances are checked is that consecutive bus stops surround Sveta's current position. Every other stop is even farther away than one of these two.

Why it works: Every bus stop has a position that is a multiple of K. For any position N, integer division separates N into a previous multiple of K and a remaining offset. The previous stop is exactly the remainder away, and the next stop is exactly the unused part of the interval away. Since these are the only two stops that can be closest to N, choosing the smaller distance always gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    K = int(input())
    N = int(input())

    remainder = N % K

    if remainder == 0:
        print(0)
    else:
        print(min(remainder, K - remainder))

if __name__ == "__main__":
    solve()
```

The input is read as two integers because the problem gives K and N on separate lines. The order matters, since K defines the spacing between stops while N defines Sveta's location.

The expression `N % K` gives the distance to the previous bus stop. Python integers do not overflow, so the maximum values from the constraints are handled safely.

The zero remainder check avoids an unnecessary comparison and directly handles the case where Sveta is already at a stop. For all other cases, the two possible directions are compared. The implementation does not use rounding or floating-point arithmetic, which avoids precision errors and off-by-one mistakes.

## Worked Examples

Since the statement formatting does not include a visible sample input, consider two valid examples.

For K = 600 and N = 2000:

| Step | K | N | Remainder | Distance to previous | Distance to next | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Initial calculation | 600 | 2000 | 200 | 200 | 400 | 200 |

The remainder is 200 because 2000 = 3 * 600 + 200. The previous stop is at 1800 and the next one is at 2400, so the shorter path is 200 meters.

For K = 10 and N = 14:

| Step | K | N | Remainder | Distance to previous | Distance to next | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Initial calculation | 10 | 14 | 4 | 4 | 6 | 4 |

This example shows why checking only the next stop is incorrect. The closest stop is behind Sveta, not ahead of her.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one division operation and a few comparisons are performed. |
| Space | O(1) | The algorithm stores only a few integer variables. |

The solution performs a fixed amount of work regardless of the size of K and N. This makes it suitable for values near the maximum limit of 2 * 10^9 and easily fits within the time and memory restrictions.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    K = int(input())
    N = int(input())

    remainder = N % K

    if remainder == 0:
        print(0)
    else:
        print(min(remainder, K - remainder))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("600\n2000\n") == "200\n", "sample style case"
assert run("10\n10\n") == "0\n", "already at a stop"
assert run("1\n2000000000\n") == "0\n", "minimum interval and maximum distance"
assert run("100\n1\n") == "1\n", "closest stop is the starting point"
assert run("10\n15\n") == "5\n", "exact middle of two stops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 600, 2000 | 200 | Regular case with a previous closer stop |
| 10, 10 | 0 | Position exactly on a bus stop |
| 1, 2000000000 | 0 | Maximum value handling |
| 100, 1 | 1 | The stop at position zero |
| 10, 15 | 5 | Equal distance from two stops |

## Edge Cases

For input:

```
5
10
```

the remainder is `10 % 5 = 0`. The algorithm immediately returns 0 because Sveta is exactly at a stop. This handles the case where moving in either direction would be unnecessary.

For input:

```
10
14
```

the remainder is `14 % 10 = 4`. The previous stop is 4 meters away and the next stop is 6 meters away. The algorithm selects 4, which is the correct shortest path.

For input:

```
100
1
```

the remainder is `1 % 100 = 1`. The previous stop is the beginning of the street at position 0, only 1 meter away. The next stop is 99 meters away, so the algorithm returns 1.

For input:

```
10
15
```

the remainder is `5`. Both neighboring stops are 5 meters away. The minimum operation returns 5, correctly handling the case where both directions have the same distance.

I can also adapt this editorial into a shorter Codeforces-style explanation or a more beginner-focused version if needed.
