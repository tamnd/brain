---
title: "CF 102281L - \u041d\u0435\u043e\u0431\u044b\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "The function foo(a, b) repeatedly subtracts a from b until the current value becomes non-positive. The final value is zero exactly when a divides b. The function then recursively replaces a by 2a and 2a+1, so starting from a=1 it can eventually reach every positive integer."
date: "2026-08-13T09:34:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "L"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 110
verified: true
draft: false
---

[CF 102281L - \u041d\u0435\u043e\u0431\u044b\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The function `foo(a, b)` repeatedly subtracts `a` from `b` until the current value becomes non-positive. The final value is zero exactly when `a` divides `b`. The function then recursively replaces `a` by `2a` and `2a+1`, so starting from `a=1` it can eventually reach every positive integer.

The actual constant in the original statement is much larger than the final line shown in the prompt. It is the concatenation of the three parts

`33931086844518982011982560935885732032396635556994207701963662088123265`,
`31417633033625453597120718116969886858499194160778011107392823626119960`,
and
`4691797570505851011072000000000000000000000000000`.

Let this constant be `C`. For every integer `k` in the requested interval, we need to evaluate `foo(1, C+k)` and print `TRUE` or `FALSE`.

The crucial constraint is that `k` is only between 0 and 100, while `C` has hundreds of decimal digits. This makes any algorithm proportional to the value of `C` impossible. Even iterating through divisors up to `sqrt(C)` would require an astronomically large number of operations. The intended reduction is to a primality question, after which modular exponentiation gives a practical solution.

There are several easy cases where a careless implementation can go wrong. For input `0 0`, the answer is `TRUE`, because `C` ends in many zeroes and is certainly composite. A program that only checks whether the number is even would happen to work here, but would fail for an odd composite such as the value corresponding to `k=99`, whose correct result is also `TRUE`. For input `0 1`, the outputs are `TRUE` and `FALSE`, as in the sample. The second number is the exceptional prime in this pair, so treating every sufficiently large number as composite would fail. Finally, for input `100 100`, the answer is `TRUE`, because `C+100` is even. A loop written with an exclusive upper bound for `k` can silently omit this case.

## Approaches

A direct implementation follows the old program literally. For every recursive call `(a,b)`, we subtract `a` from `b` until the remainder is non-positive, then recursively visit `2a` and `2a+1` whenever the earlier conditions do not already decide the result.

This direct implementation is logically correct because the recursion exactly describes the original function. Starting at `a=1`, the pairs of recursive arguments enumerate all positive integers `a` below `b`: every integer appears once as a node of the binary tree whose children are `2a` and `2a+1`. If `b` is prime, none of those values divides `b`, so the recursion explores essentially every `a` from 1 through `b-1`.

The cost of the subtraction loops is then approximately

[
\sum_{a=1}^{b-1}\left\lfloor\frac ba\right\rfloor,
]

which is `Theta(b log b)`. Here `b` has hundreds of decimal digits, so the number of individual subtractions is on the order of `10^187`. The brute-force interpretation is not merely too slow, it is fundamentally impossible.

The observation that makes the problem manageable is that the recursion is not really computing an arbitrary Boolean function. For `a=1` and `b>1`, the first condition is false, and the condition `a<b` is true. Since `a==1`, the divisibility branch is disabled, leaving only the recursive calls. Consequently, `foo(1,b)` is true exactly when one of the reachable integers `a` with `1<a<b` divides `b`.

Every integer from 2 through `b-1` is reachable, so such an `a` exists exactly when `b` has a proper divisor. For `b>1`, that is equivalent to `b` being composite.

The entire problem is thus reduced to checking whether each of the at most 101 enormous integers `C+k` is composite. Miller-Rabin primality testing is a natural fit because it works with arbitrarily large integers using modular multiplication and exponentiation, without ever iterating up to the number itself.

For numbers of this size, a fixed collection of many Miller-Rabin bases makes the probability of accepting a composite number as prime negligible. Python's arbitrary-precision integers also remove the overflow issue explicitly mentioned in the statement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(B log B)` per value | `O(log B)` recursion depth | Too slow |
| Miller-Rabin | `O(R log B)` modular operations per value | `O(1)` besides big integers | Accepted |

Here `B` denotes the magnitude of `C+k`, and `R` is the fixed number of Miller-Rabin bases.

## Algorithm Walkthrough

1. Read `kmin` and `kmax`, and construct the complete constant `C` as an integer. The three pieces are written separately in the source code so that the long literal remains easy to verify against the original statement.
2. For every `k` from `kmin` through `kmax`, set `n = C + k`. The upper endpoint is included because the output must contain one line for every integer in the closed interval.
3. Handle the trivial cases before Miller-Rabin. If `n < 2`, it is not relevant for the official constraints, but treating it as non-prime makes the primality routine complete. If `n` is divisible by a small prime such as 2, 3, 5, or another small prime, it is immediately composite.
4. Run Miller-Rabin on `n`. Write `FALSE` if the test considers `n` prime and `TRUE` otherwise. The inversion is deliberate: the original recursive function returns true for composite numbers, not for primes.
5. Print all answers in the same order as the corresponding values of `k`. This preserves the required one-to-one correspondence between input values and output lines.

### Why it works

For `b>1`, `foo(1,b)` can only become true through a recursive call. The recursive transitions `a -> 2a` and `a -> 2a+1` generate every positive integer exactly once, so before reaching `a>=b` the function tests every possible proper divisor `a` of `b`. The subtraction loop makes the divisibility test exact, since its final value is zero precisely when `a` divides `b`. Thus `foo(1,b)` is true exactly when `b` has a proper divisor, which for `b>1` means exactly when `b` is composite. The algorithm tests that same property through primality testing, so the output is the required Boolean value.

## Python Solution

```python
import sys
input = sys.stdin.readline

C = int(
    "33931086844518982011982560935885732032396635556994207701963662088123265"
    "31417633033625453597120718116969886858499194160778011107392823626119960"
    "4691797570505851011072000000000000000000000000000"
)

# A sufficiently large fixed set of bases makes the probability of a
# composite number passing all tests negligible for this problem.
BASES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499
]

def is_prime(n: int) -> bool:
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # n - 1 = d * 2^s, with d odd.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in BASES:
        if a >= n:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def solve() -> None:
    kmin, kmax = map(int, input().split())

    ans = []

    for k in range(kmin, kmax + 1):
        n = C + k
        ans.append("FALSE" if is_prime(n) else "TRUE")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The constant is converted from a string instead of being written as one enormous integer token. Python's arbitrary-precision integer type can represent it directly, so no overflow handling is needed.

The `is_prime` function first removes small prime factors. This is useful for the many even values in the range and avoids spending dozens of modular exponentiations on an obviously composite number.

Miller-Rabin writes `n-1` in the form `d * 2^s`, with `d` odd. For a chosen base `a`, it computes `a^d mod n` using Python's built-in modular exponentiation. If the resulting sequence never reaches `n-1`, the number is definitely composite.

The output condition is the reverse of the primality result. A prime `C+k` corresponds to `FALSE`, while a composite `C+k` corresponds to `TRUE`.

The loop uses `range(kmin, kmax + 1)`, not `range(kmin, kmax)`, because `kmax` belongs to the requested interval. This is one of the easiest places to introduce an off-by-one error.

The official statement explicitly guarantees that integer overflow does not exist in the original language. Python has the same useful property for this task because its integers grow as necessary.

## Worked Examples

For the first sample, the two values are `C` and `C+1`.

| `k` | `C+k` property | `is_prime` | Function result |
| --- | --- | --- | --- |
| 0 | Composite | `False` | `TRUE` |
| 1 | Prime | `True` | `FALSE` |

The first number is composite because it ends with a long sequence of zeroes. The second number is prime, so there is no proper divisor for the recursive function to discover. The resulting output is exactly the sample output.

For the second sample, the values are `C+99` and `C+100`.

| `k` | `C+k` property | `is_prime` | Function result |
| --- | --- | --- | --- |
| 99 | Composite | `False` | `TRUE` |
| 100 | Even, hence composite | `False` | `TRUE` |

The second value is an especially simple composite case because adding 100 preserves evenness. The first value demonstrates why checking only the last digit is insufficient: it is odd but still composite. The primality test handles both cases uniformly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((kmax-kmin+1) R log C)` modular operations | At most 101 numbers are tested, each with a fixed number `R` of modular exponentiation bases |
| Space | `O(1)` auxiliary space | Only a constant number of big integers and Miller-Rabin variables are kept |

The important difference from the literal recursion is that the running time depends on the number of bits in `C`, not on the numerical value of `C`. With only 101 candidates and a fixed set of Miller-Rabin bases, the solution easily avoids the astronomical `Theta(C log C)` work of the direct simulation.

## Test Cases

```python
# helper: run the core solver on an input string
import sys
import io

C = int(
    "33931086844518982011982560935885732032396635556994207701963662088123265"
    "31417633033625453597120718116969886858499194160778011107392823626119960"
    "4691797570505851011072000000000000000000000000000"
)

BASES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499
]

def is_prime(n):
    if n < 2:
        return False

    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in BASES:
        if a >= n:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def run(inp: str) -> str:
    kmin, kmax = map(int, inp.split())
    out = []

    for k in range(kmin, kmax + 1):
        n = C + k
        out.append("FALSE" if is_prime(n) else "TRUE")

    return "\n".join(out) + "\n"

# Provided sample 1.
assert run("0 1") == "TRUE\nFALSE\n", "sample 1"

# Provided sample 2.
assert run("99 100") == "TRUE\nTRUE\n", "sample 2"

# Minimum-size interval and the first value.
assert run("0 0") == "TRUE\n", "minimum interval"

# All-equal bounds. C + 50 is even.
assert run("50 50") == "TRUE\n", "equal bounds"

# Boundary at k = 100. C + 100 is even.
assert run("100 100") == "TRUE\n", "upper boundary"

# Consecutive values crossing the upper endpoint.
assert run("98 100") == "TRUE\nTRUE\nTRUE\n", "inclusive upper bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `TRUE` | Minimum interval and the composite base value |
| `50 50` | `TRUE` | Equal `kmin` and `kmax`, with an even candidate |
| `100 100` | `TRUE` | Correct handling of the maximum allowed `k` |
| `98 100` | `TRUE`, `TRUE`, `TRUE` | Inclusive upper bound and consecutive processing |

## Edge Cases

For `0 0`, the algorithm constructs exactly one candidate, `C`. Its decimal representation ends in zero, so the small-prime filter immediately finds divisibility by 2. `is_prime(C)` returns `False`, which is inverted to `TRUE`. No recursive simulation is needed.

For `0 1`, the first candidate is again immediately recognized as composite. The second candidate survives all small-prime checks and the Miller-Rabin tests, so it is classified as prime. Since the recursive function is equivalent to a composite test, the two output lines are `TRUE` and `FALSE`.

For `99 100`, the loop executes twice because the upper endpoint is included. The value for `k=99` is classified as composite, producing `TRUE`. The value for `k=100` is even and is rejected by the first small-prime check, also producing `TRUE`. This case simultaneously checks an odd composite and the upper boundary.

For `50 50`, both bounds are identical, so the loop must execute exactly once. Since `C` is even and 50 is even, `C+50` is even as well. The result is a single `TRUE` line, confirming that the output count is one rather than zero or two.

The key invariant behind all these cases is unchanged: the original recursion asks whether the huge candidate has any proper divisor, while the optimized algorithm asks whether the candidate is composite. The two predicates are identical for every candidate in this problem.
