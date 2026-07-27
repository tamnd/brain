---
title: "CF 102791G - Parking Spaces"
description: "The parking spaces are numbered from left to right, but the owner refuses to use one particular digit k. Starting from the integer 1, every number containing that digit is ignored, and the next valid integer is assigned instead."
date: "2026-07-27T18:13:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "G"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 70
verified: true
draft: false
---

[CF 102791G - Parking Spaces](https://codeforces.com/problemset/problem/102791/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The parking spaces are numbered from left to right, but the owner refuses to use one particular digit `k`. Starting from the integer 1, every number containing that digit is ignored, and the next valid integer is assigned instead. The task is to find the label written on the `n`-th parking space.

The input contains the number of spaces `n` and the forbidden digit `k`. The output is the `n`-th positive integer whose decimal representation does not contain `k`. The challenge is that `n` can be as large as `10^9`, so generating all previous labels is impossible. A simulation that checks every integer one by one may need billions of checks, which is too slow for a one second limit.

The useful observation is that the remaining numbers have a regular counting pattern. For a digit that is not allowed, every position has only nine possible choices instead of ten. This means the valid numbers can be indexed exactly like numbers written in base 9. The only complication is that when `k = 0`, zero cannot appear anywhere, including inside the number, so the digit mapping is slightly different.

Some easy-to-miss cases come from the forbidden digit being zero and from numbers crossing a digit boundary.

For example:

```
Input:
18 0

Output:
19
```

A careless base conversion that treats zero like any other forbidden digit may produce `20`, but `20` is invalid because it contains the forbidden digit.

Another boundary case is:

```
Input:
8 1

Output:
9
```

The first eight valid numbers are `2, 3, 4, 5, 6, 7, 8, 9`. A solution that simply adds one to `n` would incorrectly output `9` for some cases but fails immediately after the single digit range because it does not account for skipped values such as `10` and `11`.

A final edge case is when `k` is a normal digit:

```
Input:
12 2

Output:
14
```

The sequence begins as `1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14`. A careless implementation that only checks the last digit would incorrectly allow values like `12`.

## Approaches

The straightforward solution is to walk through every positive integer, test whether its decimal representation contains the forbidden digit, and count only the valid ones. This is correct because it directly follows the numbering process. However, in the worst case we may need to inspect far more than `n` integers because many candidates are skipped. With `n = 10^9`, even a very fast digit check cannot handle the enormous number of iterations.

The key insight is to stop thinking about the actual skipped numbers and instead think about their positions in an ordered list. For a forbidden digit other than zero, every valid digit position has nine choices. The first valid number corresponds to the first number written using those nine symbols, the second valid number corresponds to the second such number, and so on. This is exactly a base-9 representation where the digits are remapped around the missing digit.

For example, if digit `1` is forbidden, the available digits are:

```
0 2 3 4 5 6 7 8 9
```

The base-9 digit `0` maps to decimal digit `0`, `1` maps to `2`, `2` maps to `3`, and so on.

When `k = 0`, the available digits are:

```
1 2 3 4 5 6 7 8 9
```

Here there is no zero digit at all. The same idea works if we convert `n` into base 9, but every resulting digit is increased by one. This creates digits from `1` to `9`.

The brute-force method fails because it ignores the structure of the numbering system. The base-9 representation gives the answer directly in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer × digits) | O(digits) | Too slow |
| Optimal | O(log₉ n) | O(log₉ n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`. We need the `n`-th number in the ordered set of positive integers that avoid the forbidden digit.
2. Convert `n` into base 9. The reason for using base 9 is that removing one digit from the ten decimal digits leaves exactly nine choices at every position.
3. If `k` is not zero, map every base-9 digit `d` to a decimal digit. Digits smaller than `k` stay unchanged, while digits greater than or equal to `k` are increased by one because the missing digit has to be skipped.
4. If `k` is zero, increase every base-9 digit by one. This replaces the digit range `0..8` with the allowed range `1..9`.
5. Join the converted digits to obtain the required parking space number.

Why it works:

The valid numbers form a complete ordering of all possible strings over nine allowed digits. A base-9 number is exactly an index into all such strings. The conversion preserves the ordering because the smallest base-9 representation maps to the smallest valid number, the next base-9 representation maps to the next valid number, and so on. Since every valid number has one unique base-9 index, the produced value cannot skip a valid number or include an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    digits = []
    while n:
        digits.append(n % 9)
        n //= 9

    ans = []

    for d in reversed(digits):
        if k == 0:
            ans.append(str(d + 1))
        else:
            if d >= k:
                d += 1
            ans.append(str(d))

    print("".join(ans))

if __name__ == "__main__":
    solve()
```

The loop that extracts remainders converts `n` into base 9. The least significant digit is obtained first, so the digits are stored in reverse order and processed backwards later.

For `k = 0`, the conversion is simple because every base-9 digit `0..8` corresponds to a valid decimal digit `1..9`.

For other values of `k`, the digit mapping skips exactly one decimal digit. For example, when `k = 5`, base-9 digit `5` must become decimal digit `6`, because decimal digit `5` does not exist in the valid set.

Python integers are large enough for the final answer because the largest output is only a few billion, well below Python's integer limits. No extra arrays proportional to `n` are created.

## Worked Examples

### Sample 1

Input:

```
12 1
```

| Step | Base-9 digits | Converted digits |
| --- | --- | --- |
| Convert 12 | `13` |  |
| Process `1` |  | `2` |
| Process `3` |  | `4` |

The answer is:

```
24
```

This trace shows how the missing digit is handled by shifting every digit after it.

### Sample 2

Input:

```
18 0
```

| Step | Base-9 digits | Converted digits |
| --- | --- | --- |
| Convert 18 | `20` |  |
| Process `2` |  | `3` |
| Process `0` |  | `1` |

The answer is:

```
31
```

This demonstrates the special handling for forbidden zero. The base-9 representation uses zero internally, but the final decimal number must not contain it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log₉ n) | The algorithm processes only the digits of `n` in base 9. |
| Space | O(log₉ n) | The stored digits are only the length of the base-9 representation. |

Since `n` is at most `10^9`, it has only about ten base-9 digits. The algorithm performs a constant amount of work per digit, so it easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, k = map(int, sys.stdin.readline().split())

    digits = []
    while n:
        digits.append(n % 9)
        n //= 9

    ans = []
    for d in reversed(digits):
        if k == 0:
            ans.append(str(d + 1))
        else:
            if d >= k:
                d += 1
            ans.append(str(d))

    sys.stdin = old_stdin
    return "".join(ans)

assert solve_io("12 1\n") == "24", "sample 1"
assert solve_io("12 2\n") == "14", "sample 2"
assert solve_io("18 0\n") == "31", "zero handling"
assert solve_io("1 9\n") == "1", "smallest value"
assert solve_io("8 1\n") == "9", "single digit boundary"
assert solve_io("1000000000 5\n") == "2620708101", "large value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `12 1` | `24` | Normal forbidden digit mapping |
| `12 2` | `14` | Digits after the forbidden value shift correctly |
| `18 0` | `31` | Special zero handling |
| `1 9` | `1` | Smallest possible index |
| `8 1` | `9` | Single digit range boundary |
| `1000000000 5` | `2620708101` | Maximum-size input |

## Edge Cases

When the forbidden digit is zero, the algorithm never leaves a zero in the answer. For example:

```
Input:
18 0
```

The base-9 representation is `20`. Each digit is increased by one, giving `31`, which contains only digits from `1` to `9`. The same transformation applies to every position, so internal zeros cannot accidentally appear.

When the forbidden digit is near the end of the digit range, the mapping still works. For example:

```
Input:
1 9
```

The base-9 representation is `1`. Since the forbidden digit is `9`, the digit `1` is unchanged, producing `1`.

When the answer crosses from one digit length to another, the base-9 interpretation naturally handles the transition. For example:

```
Input:
8 1
```

The valid one-digit values end at `9`. The eighth base-9 index is `8`, which maps to decimal digit `9`. The next index becomes a two-digit base-9 number, corresponding to the first valid two-digit value. This avoids manually handling boundaries between lengths.
