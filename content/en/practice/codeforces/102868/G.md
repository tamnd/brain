---
title: "CF 102868G - White"
description: "The task asks us to answer many range queries. For each interval of possible inputs, we need find the number x inside that interval whose generated id code is largest. The generated code is x phi(x), where phi(x) is obtained by replacing every digit of x with its complement to 9."
date: "2026-07-25T13:31:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102868
codeforces_index: "G"
codeforces_contest_name: "2020 UTPC Fall Puzzle Contest"
rating: 0
weight: 102868
solve_time_s: 57
verified: true
draft: false
---

[CF 102868G - White](https://codeforces.com/problemset/problem/102868/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
# Problem Understanding

The task asks us to answer many range queries. For each interval of possible inputs, we need find the number `x` inside that interval whose generated id code is largest. The generated code is `x * phi(x)`, where `phi(x)` is obtained by replacing every digit of `x` with its complement to 9. The leading zeroes created by this operation are ignored, but that does not change the numerical value.

The key simplification is hidden inside the digit operation. If `x` has exactly `k` digits, replacing every digit `d` by `9-d` creates the same value as subtracting `x` from the `k` digit number consisting only of nines. For example, for a three digit number, `phi(x) = 999 - x`. Removing leading zeroes does not affect this equality because leading zeroes do not contribute to the value.

The input contains up to 1000 intervals, and every endpoint is at most `10^9`. A solution that checks every number in every interval can require up to about `10^12` evaluations, which is far beyond what is possible. We need to use the mathematical shape of the function instead of iterating through the range.

The function for a fixed digit length is:

`f(x) = x * (10^k - 1 - x)`

Expanding it gives a downward opening parabola. Its maximum is at the middle of the interval from `0` to `10^k - 1`, so we only need to examine positions near that middle and the boundaries of the query interval.

The tricky cases are caused by digit length changes. A number like `99` belongs to the two digit group, where `phi(99)=0`, but `100` belongs to the three digit group, where `phi(100)=899`. A solution that assumes the whole query uses one value of `k` can fail.

For example:

```
Input
1
99 100

Output
89900
```

The answer comes from `x=100`, because `100 * 899 = 89900`. Looking only at two digit numbers would incorrectly return zero.

Another edge case is when the interval contains only one number.

```
Input
1
5 5

Output
20
```

A careless implementation that only checks the middle of a range might miss the answer because there is no room to move toward the midpoint.

## Approaches

A direct solution would try every possible `x` in `[l,r]`, compute `phi(x)` digit by digit, and keep the largest product. This is correct because every valid candidate is examined. However, an interval can contain close to one billion values, and there can be 1000 queries. The worst case would require around `10^12` product evaluations, which is impossible.

The useful observation is that numbers with the same digit count share the same complement base. If `x` has `k` digits, then `phi(x)=10^k-1-x`, so the product becomes:

`x * (10^k-1-x)`

This is a parabola. A parabola that opens downward reaches its maximum at the vertex. For a query interval, the best value inside a digit-length segment must be either the vertex if it lies inside the segment, or one of the segment endpoints.

Since `x` is at most `10^9`, there are only eleven possible digit-length groups to consider, from one digit to ten digits. For each group we intersect it with the query range and test the few possible candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r-l+1) per query | O(1) | Too slow |
| Optimal | O(10) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. For each query interval `[l,r]`, consider every possible digit length `k` from 1 to 10. The interval of numbers having exactly `k` digits is `[10^(k-1), 10^k-1]`, with the lower bound treated as 1 for `k=1`.
2. Intersect this digit-length interval with `[l,r]`. If the intersection is empty, there are no candidates of this digit length.
3. Compute `m = (10^k - 1) / 2`, which is the position where `x * (10^k - 1 - x)` is maximized. The best candidate inside the current segment is among the segment boundaries and the two integers closest to `m`.
4. Evaluate the product for every candidate that remains inside the segment and update the global maximum.

Why it works: For every fixed digit length, the product function is a concave quadratic. A concave quadratic cannot have an interior point better than its vertex, and if the vertex is outside the allowed interval, the best point must be the closest endpoint. We test exactly those possibilities for every digit length, so every possible optimal number is covered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_query(l, r):
    ans = 0
    pow10 = 1

    for k in range(1, 11):
        low = 1 if k == 1 else pow10
        high = pow10 * 10 - 1

        left = max(l, low)
        right = min(r, high)

        if left <= right:
            limit = high
            middle_floor = limit // 2
            middle_ceil = middle_floor + (limit % 2)

            candidates = [
                left,
                right,
                middle_floor,
                middle_ceil
            ]

            for x in candidates:
                if left <= x <= right:
                    ans = max(ans, x * (limit - x))

        pow10 *= 10

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        l, r = map(int, input().split())
        out.append(str(solve_query(l, r)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The loop over `k` handles every possible digit length. The variable `pow10` stores `10^(k-1)` before it is updated for the next iteration, so the current digit range can be constructed without repeated exponentiation.

For each digit length, `limit` is `10^k-1`, the all-nine number used in the formula for `phi(x)`. The candidate list contains the two ends of the valid interval and the two middle values. Testing both middle values avoids issues caused by integer division when the vertex is between two integers.

The multiplication is done using Python integers, so the largest possible product, which is around `9 * 10^18`, is handled safely. The order of operations also avoids any floating point rounding.

## Worked Examples

### Sample 1

Input interval: `[1,7]`

| k | Valid range | Candidate checked | Best product |
| --- | --- | --- | --- |
| 1 | [1,7] | 1, 7, 4, 5 | 20 |

The middle of the one digit range is around 4.5, so checking 4 and 5 finds the optimum. The answer is `4 * 5 = 20`.

### Sample 2

Input interval: `[8,14]`

| k | Valid range | Candidate checked | Best product |
| --- | --- | --- | --- |
| 1 | [8,9] | 8, 9, 4, 5 | 8 |
| 2 | [10,14] | 10, 14, 49, 50 | 1190 |

The one digit part cannot beat the two digit part. In the two digit segment, the closest available value to 49.5 is not inside the query, so the best point is the upper boundary `14`, giving `14 * 85 = 1190`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10t) | Each query checks ten possible digit lengths and a constant number of candidates. |
| Space | O(1) | Only a few integer variables are stored. |

The maximum number of operations is around a few tens of thousands because there are only 1000 queries. This easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_query(l, r):
    ans = 0
    pow10 = 1

    for k in range(1, 11):
        low = 1 if k == 1 else pow10
        high = pow10 * 10 - 1
        left = max(l, low)
        right = min(r, high)

        if left <= right:
            middle_floor = high // 2
            middle_ceil = middle_floor + (high % 2)

            for x in (left, right, middle_floor, middle_ceil):
                if left <= x <= right:
                    ans = max(ans, x * (high - x))

        pow10 *= 10

    return ans

def run(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""
    t = int(data[0])
    idx = 1
    res = []
    for _ in range(t):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        res.append(str(solve_query(l, r)))
    return "\n".join(res)

assert run("""3
1 7
7 10
8 14
""") == """20
890
1190""", "samples"

assert run("""1
1 1
""") == "8", "minimum input"

assert run("""1
5 5
""") == "20", "single value interval"

assert run("""1
99 100
""") == "89900", "digit boundary"

assert run("""1
1000000000 1000000000
""") == "8999999999000000000", "maximum value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,7]` | `20` | Middle point inside a small interval |
| `[1,1]` | `8` | Smallest possible value |
| `[5,5]` | `20` | Single-element query |
| `[99,100]` | `89900` | Crossing a digit-length boundary |
| `[1000000000,1000000000]` | `8999999999000000000` | Largest allowed input and large multiplication |

## Edge Cases

For the interval `[99,100]`, the algorithm checks both digit groups. The two digit group uses `99 - x`, giving only zero at `x=99`. The three digit group uses `999 - x`, and `x=100` gives `899`, producing `89900`. Since both groups are considered independently, the digit transition cannot be missed.

For the interval `[5,5]`, the intersection for the one digit group is a single point. The candidate list contains both boundaries, so `x=5` is tested directly. The computed value is `5 * (9-5) = 20`.

For the largest input value `1000000000`, the algorithm places it in the ten digit group. The all-nine number is `9999999999`, so `phi(1000000000)=8999999999`. The product fits in Python's integer type and is evaluated without overflow.
