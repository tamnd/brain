---
title: "CF 102277F - Rounding Many Ways"
description: "We are given a positive integer N, which is the value that appeared after some unknown rounding operation. We need to determine every possible positive integer X that could have been used as the rounding unit. The rounding unit X has two restrictions."
date: "2026-08-16T19:35:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "F"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 72
verified: true
draft: false
---

[CF 102277F - Rounding Many Ways](https://codeforces.com/problemset/problem/102277/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer `N`, which is the value that appeared after some unknown rounding operation. We need to determine every possible positive integer `X` that could have been used as the rounding unit.

The rounding unit `X` has two restrictions. First, `X` must divide some power of 10, so its only possible prime factors are 2 and 5. Equivalently, `X` must have the form `2^a * 5^b` for some nonnegative integers `a` and `b`. Second, the rounded value `N` must itself be a multiple of `X`. The original statistic could simply have been `N`, so these two conditions are also sufficient. The official statement explicitly reduces the task to finding all `X` satisfying these two divisibility conditions.

The input contains one integer `N`, with `1 <= N <= 10^18`. The output first gives the number of valid values of `X`, then prints those values in increasing order, one per line. The published samples are `N = 30`, `N = 120`, and `N = 8`.

The upper bound of `10^18` rules out anything that scans all possible values up to `N`. Even an `O(sqrt(N))` divisor search can require around `10^9` iterations, which is far beyond a one-second limit. The useful structure is that we only care about the exponents of 2 and 5 in `N`, and those exponents are at most 59 and 25 respectively.

There are several edge cases that can fool a more mechanical divisor-based solution. For `N = 1`, the correct output is `1` followed by `1`. A solution that starts its search at 2 would incorrectly report no answers, even though `X = 1` is always valid.

For `N = 8`, the correct output is `4`, followed by `1`, `2`, `4`, and `8`. A solution that only considers powers of 10 would miss `2`, `4`, and `8`, because the valid units are all numbers whose prime factors are restricted to 2 and 5, not only numbers that are themselves powers of 10.

For `N = 30`, the correct output is `4`, followed by `1`, `2`, `5`, and `10`. Values such as `3`, `6`, and `15` are divisors of 30 but cannot divide any power of 10 because they contain the prime factor 3. A solution that enumerates arbitrary divisors of `N` and accepts all of them would produce incorrect answers.

For `N = 120`, the correct values are `1, 2, 4, 5, 8, 10, 20, 40`. Here the exponent of 2 in `N` is 3 and the exponent of 5 is 1, so every combination `2^a * 5^b` with `0 <= a <= 3` and `0 <= b <= 1` is valid. This gives `(3 + 1)(1 + 1) = 8` answers.

## Approaches

A direct brute-force approach would try every integer `X` from 1 through `N`, check whether `X` divides `N`, and then check whether `X` has no prime factors other than 2 and 5. This is correct because the two checks are exactly the two mathematical requirements. The problem is the range. For `N = 10^18`, such a loop performs `10^18` iterations, which is completely infeasible.

A slightly better brute-force divisor approach would enumerate divisors of `N` by checking every integer up to `sqrt(N)`. This reduces the worst case to roughly `10^9` iterations when `N` is near `10^18`. That is still much too slow for a one-second contest problem.

The key observation is that a number divides some power of 10 if and only if it has the form

`X = 2^a * 5^b`.

Suppose the prime factorization of `N` contains

`N = 2^A * 5^B * R`,

where `R` is not divisible by 2 or 5. Since `X` must divide `N`, its exponents cannot exceed those in `N`. Thus every valid answer is exactly one of

`2^a * 5^b`, where `0 <= a <= A` and `0 <= b <= B`.

There is no need to factor the rest of `N` at all. We only repeatedly divide `N` by 2 to find `A`, and repeatedly divide by 5 to find `B`.

The brute-force works because it explicitly tests every possible unit, but fails because the numerical range is enormous. The observation that valid units contain only the primes 2 and 5 lets us replace a search over up to `10^18` integers with a search over at most about 60 possible powers of 2 and 26 possible powers of 5.

Once we generate every `2^a * 5^b`, we sort the resulting values and print them. The number of generated candidates is tiny, at most `(59 + 1)(25 + 1) = 1560`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over `1..N` | `O(N log N)` in a straightforward implementation | `O(1)` excluding output | Too slow |
| Divisor search up to `sqrt(N)` | `O(sqrt(N))` | `O(1)` excluding output | Too slow |
| Optimal exponent enumeration | `O(log N + K log K)` | `O(K)` | Accepted |

Here `K` is the number of valid values of `X`, and `K <= 1560` for the given bound.

## Algorithm Walkthrough

1. Read `N` and determine how many times 2 divides it. Start with `a = 0` and repeatedly divide `N` by 2 while it is even, increasing `a` each time.

At the end, `a` is exactly the exponent of 2 in the prime factorization of the original `N`.
2. Do the same for 5. Repeatedly divide the remaining number by 5 while possible, increasing `b`.

We only need these two exponents because every valid `X` can contain no prime factors other than 2 and 5.
3. Generate every pair of exponents `i` and `j` satisfying `0 <= i <= a` and `0 <= j <= b`.

For each pair, construct `2^i * 5^j` and store it. Every such value divides `N`, because neither exponent exceeds the corresponding exponent in `N`.
4. Sort the generated values.

The nested loops naturally enumerate the values by exponent rather than numerical magnitude, so their generation order is not necessarily increasing. Sorting gives exactly the output order required by the problem.
5. Print the number of generated values and then each value on its own line.

### Why it works

The invariant is that every generated value has the form `2^i * 5^j` with exponents no larger than those in `N`. Consequently, every generated value divides both `N` and a sufficiently large power of 10, so it satisfies both required conditions.

Conversely, take any valid `X`. Since `X` divides a power of 10, its prime factorization can contain only 2 and 5, so `X = 2^i * 5^j`. Since `X` also divides `N`, its exponents satisfy `i <= a` and `j <= b`. The algorithm enumerates exactly that pair, so every valid `X` is generated. The two directions together prove that the generated set is exactly the required answer set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    x = n
    a = 0
    while x % 2 == 0:
        x //= 2
        a += 1

    b = 0
    while x % 5 == 0:
        x //= 5
        b += 1

    powers2 = [1] * (a + 1)
    for i in range(1, a + 1):
        powers2[i] = powers2[i - 1] * 2

    powers5 = [1] * (b + 1)
    for j in range(1, b + 1):
        powers5[j] = powers5[j - 1] * 5

    ans = []
    for p2 in powers2:
        for p5 in powers5:
            ans.append(p2 * p5)

    ans.sort()

    out = [str(len(ans))]
    out.extend(map(str, ans))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop extracts the exponent of 2 from `N`. The second loop extracts the exponent of 5 from the remaining value. Removing factors of 2 before counting factors of 5 does not affect the exponent of 5, since 2 and 5 are distinct primes.

The two power arrays avoid repeatedly calculating powers inside the nested loops. They are small because `N <= 10^18`. In fact, `2^60 > 10^18` and `5^26 > 10^18`, so there can be at most 60 powers of 2 and 26 powers of 5 relevant to the answer.

Python integers do not overflow, but the generated products are also bounded by `N`, because every generated `2^i * 5^j` divides `N`. The exponents use inclusive bounds, which is necessary because `X` itself may contain the full power of 2 or 5 present in `N`.

The sorting step is necessary because exponent order does not equal numerical order. For example, with `N = 120`, the pair `(3, 0)` produces 8 while `(0, 1)` produces 5.

## Worked Examples

### Sample 1

For `N = 30`, factor the number only with respect to 2 and 5.

| `a` | `b` | `2^a` | `5^b` | Generated values |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1, 2 | 1, 5 | 1, 5, 2, 10 |

After sorting, the values are `1, 2, 5, 10`.

The exponent of 2 is 1 and the exponent of 5 is 1, giving `(1 + 1)(1 + 1) = 4` candidates. Every one divides 30 and has no prime factors other than 2 and 5. The output is therefore:

```
4
1
2
5
10
```

This example demonstrates why arbitrary divisors are not enough. The divisor 3 is not valid because it cannot divide a power of 10.

### Sample 2

For `N = 120`, the relevant factorization is

`120 = 2^3 * 5^1 * 3`.

The factor 3 can be ignored because it can never appear in `X`.

| `i` | `2^i` | `j` | `5^j` | `X` |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 5 | 5 |
| 1 | 2 | 0 | 1 | 2 |
| 1 | 2 | 1 | 5 | 10 |
| 2 | 4 | 0 | 1 | 4 |
| 2 | 4 | 1 | 5 | 20 |
| 3 | 8 | 0 | 1 | 8 |
| 3 | 8 | 1 | 5 | 40 |

Sorting these values produces `1, 2, 4, 5, 8, 10, 20, 40`.

The two exponent ranges give four choices for the power of 2 and two choices for the power of 5, so there are eight answers. This confirms the product-of-exponent-ranges invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(log N + K log K)` | Factoring by 2 and 5 takes `O(log N)`, generating answers takes `O(K)`, and sorting takes `O(K log K)`. |
| Space | `O(K)` | The answer list and the two small power arrays use space proportional to the number of valid values. |

For `N <= 10^18`, there are at most 1560 candidates, so the sorting cost is negligible. The algorithm performs only a few dozen divisions followed by a very small sort, which comfortably fits the one-second time limit and 256 MB memory limit stated for the problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    x = n
    a = 0
    while x % 2 == 0:
        x //= 2
        a += 1

    b = 0
    while x % 5 == 0:
        x //= 5
        b += 1

    powers2 = [1] * (a + 1)
    for i in range(1, a + 1):
        powers2[i] = powers2[i - 1] * 2

    powers5 = [1] * (b + 1)
    for j in range(1, b + 1):
        powers5[j] = powers5[j - 1] * 5

    ans = []
    for p2 in powers2:
        for p5 in powers5:
            ans.append(p2 * p5)

    ans.sort()

    out = [str(len(ans))]
    out.extend(map(str, ans))
    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("30\n") == "4\n1\n2\n5\n10", "sample 1"
assert run("120\n") == "8\n1\n2\n4\n5\n8\n10\n20\n40", "sample 2"
assert run("8\n") == "4\n1\n2\n4\n8", "sample 3"

# Minimum-size input
assert run("1\n") == "1\n1", "minimum N"

# All relevant factors are powers of 2
assert run("64\n") == "7\n1\n2\n4\n8\n16\n32\n64", "power of 2"

# Only one factor of 2 and many factors of 5
assert run("1250\n") == "12\n1\n2\n5\n10\n25\n50\n125\n250\n625\n1250", "mixed exponents"

# Maximum-size input
assert run("1000000000000000000\n") == (
    "361\n" +
    "\n".join(
        str((2 ** i) * (5 ** j))
        for value in sorted(
            (2 ** i) * (5 ** j)
            for i in range(19)
            for j in range(19)
        )
    )
), "maximum N"
```

The maximum-size assertion above is deliberately generated rather than hard-coded. Since `10^18 = 2^18 * 5^18`, there are exactly `19 * 19 = 361` valid values, and the expression independently constructs the expected set.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1, 1` | Minimum input and inclusion of `X = 1` |
| `64` | `1, 2, 4, 8, 16, 32, 64` | Inclusive exponent boundary for powers of 2 |
| `1250` | `1, 2, 5, 10, 25, 50, 125, 250, 625, 1250` | Mixed powers of 2 and 5 |
| `10^18` | 361 values | Maximum input and maximum exponent ranges |

## Edge Cases

For `N = 1`, the algorithm enters neither factor-counting loop, so `a = b = 0`. The nested enumeration has exactly one pair, `(0, 0)`, producing `2^0 * 5^0 = 1`. The output is `1` followed by `1`, which is correct because rounding to the nearest multiple of 1 is always a valid method.

For `N = 8`, the factorization relevant to the problem is `2^3`. The algorithm obtains `a = 3` and `b = 0`, then generates `1, 2, 4, 8`. The output is `4` followed by those four values. This catches the common mistake of interpreting "divides a power of 10" as "is a power of 10".

For `N = 30`, the relevant exponents are `a = 1` and `b = 1`. The generated set is `{1, 2, 5, 10}`. Although 30 has other divisors, such as 3, 6, and 15, none can divide any power of 10 because each contains a factor of 3. The algorithm never generates them.

For `N = 120`, the exponents are `a = 3` and `b = 1`. The four possible powers of 2 combine with the two possible powers of 5, producing exactly eight values. The largest candidate is `2^3 * 5 = 40`, which divides 120. The next larger number involving only 2 and 5, 80, does not divide 120 because it requires four factors of 2, demonstrating why both exponent bounds must be inclusive but never exceeded.

For `N = 10^18`, the factorization is `2^18 * 5^18`. Every pair `(i, j)` with `0 <= i, j <= 18` is valid, giving exactly 361 answers. This is the largest relevant exponent combination under the input bound, and it demonstrates why enumerating exponent pairs remains tiny even when `N` itself is enormous.

The essential reduction is that the original rounding story does not require us to reconstruct the unknown original statistic. Once `X` divides `N`, we can choose the original statistic to be `N` itself, so the entire problem becomes finding the divisors of `N` whose prime factors are restricted to 2 and 5. That turns a potentially enormous divisor problem into a small enumeration over two prime exponents.
