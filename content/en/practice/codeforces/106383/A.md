---
title: "CF 106383A - Factorial Frenzy"
description: "The task asks for the number of zero bits at the end of the binary representation of a factorial. The input is a single integer n, and the output is how many times the binary value of n! can be divided by 2 before it becomes odd. The value of n!"
date: "2026-06-25T10:19:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106383
codeforces_index: "A"
codeforces_contest_name: "2026 Spring UT CS104c Midterm #1"
rating: 0
weight: 106383
solve_time_s: 31
verified: true
draft: false
---

[CF 106383A - Factorial Frenzy](https://codeforces.com/problemset/problem/106383/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks for the number of zero bits at the end of the binary representation of a factorial. The input is a single integer `n`, and the output is how many times the binary value of `n!` can be divided by 2 before it becomes odd. The value of `n!` itself becomes far too large to construct directly, even for the allowed maximum input.

The important shift is to stop thinking about the digits of the factorial and instead think about factors. A trailing zero in binary means the number has a factor of `2`. If a number is divisible by `2^k` but not by `2^(k+1)`, its binary representation ends with exactly `k` zeros. The problem is asking for the exponent of `2` inside `n!`.

The input limit reaches `10^6`. A loop over all numbers up to `n` is completely reasonable, but building the factorial is impossible because the number of digits of `n!` grows much faster than the input size. Any approach that stores or repeatedly manipulates the factorial itself will run out of time or memory.

The tricky cases are mostly about counting factors correctly. For `n = 1`, the factorial is `1`, whose binary representation is `1`, so the answer is zero. A solution that starts counting from the wrong point might incorrectly add a factor of two.

For example:

```
Input:
1

Output:
0
```

There are no even numbers in `1!`, so there are no trailing zero bits.

Another common mistake is counting only multiples of two and ignoring higher powers. For example:

```
Input:
8

Output:
7
```

The even numbers contribute factors of two as follows: `2` contributes one, `4` contributes two, `6` contributes one, and `8` contributes three. The total is `1 + 2 + 1 + 3 = 7`. A careless implementation that only counts even numbers would get `4` instead.

## Approaches

The direct approach is to compute the factorial and repeatedly divide it by two while it remains even. This is mathematically correct because every division removes one trailing zero from the binary representation. The problem is the size of the factorial. For `n = 10^6`, the factorial has millions of digits, so constructing it and dividing it would require manipulating an enormous integer.

A better way is to count how many factors of two appear in the multiplication `1 * 2 * 3 * ... * n`. Every even number contributes at least one factor of two. Numbers divisible by four contribute an additional factor, numbers divisible by eight contribute another, and this pattern continues.

The number of multiples of `2` among the first `n` integers is `floor(n / 2)`. The number of additional factors coming from multiples of `4` is `floor(n / 4)`. The number of additional factors from multiples of `8` is `floor(n / 8)`. Adding these values until the power of two becomes larger than `n` gives the exact number of trailing binary zeros.

The brute-force idea fails because it tries to represent the result of the multiplication. The optimized idea only counts the prime factors that matter, so it reduces the problem from manipulating a huge number to performing a small logarithmic number of divisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(size of n! × number of divisions) | O(size of n!) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and initialize the answer to zero. The answer will store the total number of factors of two contained in `n!`.
2. Start with the value `2` and repeatedly multiply it by `2`. For each power of two `p`, add `n // p` to the answer.
3. Stop when the current power of two becomes larger than `n`. No number from `1` to `n` can contain that many factors of two, so larger powers contribute nothing.
4. Print the accumulated answer.

The reason this works is that every occurrence of a factor of two in the numbers from `1` to `n` creates one trailing zero in binary. Counting multiples of `2` finds the first factors, counting multiples of `4` finds the extra factors those numbers contain, and continuing with higher powers captures every possible contribution.

Why it works:

The exponent of a prime number `p` in a factorial is given by adding the number of multiples of `p`, then the number of multiples of `p²`, then the number of multiples of `p³`, and so on. Here the prime is `2`, so the sum is exactly:

`floor(n/2) + floor(n/4) + floor(n/8) + ...`

This value is the largest `k` such that `2^k` divides `n!`. Since a binary trailing zero corresponds exactly to one factor of two, this value is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = 0
    power = 2

    while power <= n:
        ans += n // power
        power *= 2

    print(ans)

if __name__ == "__main__":
    solve()
```

The variable `ans` stores the total number of factors of two found so far. The loop starts from `2` because every factor counted must come from a multiple of two.

The multiplication `power *= 2` moves through the sequence `2, 4, 8, 16, ...`. Each iteration counts how many numbers contain this power of two as a divisor. Integer division gives exactly the number of multiples.

Python integers do not overflow, so there is no special handling needed for the answer. The largest possible answer is much smaller than the factorial itself, and the loop runs only about twenty times for `n = 10^6`.

## Worked Examples

For `n = 8`:

| power | n // power | answer |
| --- | --- | --- |
| 2 | 4 | 4 |
| 4 | 2 | 6 |
| 8 | 1 | 7 |

The next power would be `16`, which is larger than `8`, so the algorithm stops. The result confirms that all factors of two from `8!` have been counted.

For `n = 10`:

| power | n // power | answer |
| --- | --- | --- |
| 2 | 5 | 5 |
| 4 | 2 | 7 |
| 8 | 1 | 8 |

The value `10!` contains eight factors of two, so its binary representation ends with eight zero bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | The algorithm checks only powers of two up to `n`. |
| Space | O(1) | Only a few integer variables are stored. |

The maximum input is `10^6`, so the loop executes around twenty times. This is far below the available limits and avoids ever creating the enormous value of `n!`.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    ans = 0
    power = 2
    while power <= n:
        ans += n // power
        power *= 2

    sys.stdin = old_stdin
    return str(ans) + "\n"

# provided samples
assert solve_data("1\n") == "0\n", "sample 1"
assert solve_data("8\n") == "7\n", "sample 2"
assert solve_data("1000000\n") == "999993\n", "sample 3"

# custom cases
assert solve_data("2\n") == "1\n", "smallest even factorial"
assert solve_data("3\n") == "1\n", "boundary before power of two"
assert solve_data("16\n") == "15\n", "power of two boundary"
assert solve_data("32\n") == "31\n", "larger power of two boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `1` | Checks the first non-zero contribution. |
| `3` | `1` | Checks that a number just before a power of two is handled correctly. |
| `16` | `15` | Checks contributions from several levels of powers of two. |
| `32` | `31` | Checks a larger power-of-two boundary. |

## Edge Cases

For the input:

```
1
```

the loop never runs because `2 > 1`. The answer remains zero, which matches the fact that `1! = 1` has no trailing zero bits.

For the input:

```
8
```

the algorithm visits powers `2`, `4`, and `8`. It adds `8 // 2 = 4`, `8 // 4 = 2`, and `8 // 8 = 1`, producing `7`. This handles the case where numbers such as `8` contribute multiple factors of two and prevents the common mistake of counting only even numbers.

For the input:

```
1000000
```

the algorithm never attempts to build `1000000!`. It only checks powers of two up to `524288`, adding each contribution. The final answer is `999993`, which comes entirely from factor counting rather than factorial construction.
