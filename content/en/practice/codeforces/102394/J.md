---
title: "CF 102394J - Justifying the Conjecture"
description: "For each test case, we need to split the integer n into two positive integers x and y such that x is prime, y is composite, and x + y = n. The two numbers must both be strictly smaller than n. If no such split exists, we print -1."
date: "2026-08-10T19:11:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "J"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 87
verified: true
draft: false
---

[CF 102394J - Justifying the Conjecture](https://codeforces.com/problemset/problem/102394/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we need to split the integer `n` into two positive integers `x` and `y` such that `x` is prime, `y` is composite, and `x + y = n`. The two numbers must both be strictly smaller than `n`. If no such split exists, we print `-1`.

There can be up to `10^5` test cases, while each `n` can be as large as `10^9`. That rules out algorithms that perform work proportional to `n` for every test case. Even a linear scan over all possible values of `x` would require up to about `10^14` iterations across the full input. We need to exploit a mathematical property of the required prime and composite numbers instead of searching through candidates.

The smallest useful composite number is `4`. The parity of `n` gives us an even simpler construction. If `n` is even and sufficiently large, choosing `x = 2` makes `y = n - 2`, which is also even. Every even number greater than `2` is composite, so this immediately works whenever `n - 2 >= 4`, meaning `n >= 6`.

If `n` is odd and sufficiently large, choosing `x = 3` makes `y = n - 3`, which is even. For odd `n >= 7`, we have `y >= 4`, so `y` is composite. Thus every odd `n >= 7` also has an immediate construction.

The small values `1` through `5` need to be handled separately. For `n = 1, 2, 3`, there is not enough room for a prime plus a composite. For `n = 4`, the only possible split using a prime is `2 + 2`, but `2` is prime rather than composite. For `n = 5`, the possible prime-first decompositions are `2 + 3` and `3 + 2`, and neither second number is composite. Hence all five values produce `-1`.

For example, input `1` must produce `-1`. A careless implementation that treats `1` as composite could incorrectly accept `1 + 0` or another invalid decomposition. For input `5`, simply finding two numbers whose sum is `5` is also insufficient, because `2 + 3` consists entirely of primes. The distinction between prime and composite must be checked correctly.

## Approaches

A direct brute-force solution can try every possible prime candidate `x` from `2` through `n - 2`, set `y = n - x`, and test whether `x` is prime and `y` is composite. The method is correct because every valid answer must appear among those candidates. If primality is tested by trial division, checking one number can take `O(sqrt(n))` operations, so scanning all candidates has worst-case complexity `O(n sqrt(n))` for one test case. With `n` as large as `10^9`, that means up to roughly `10^9` candidate values and about `31623` trial divisors per candidate, on the order of `3 * 10^13` divisibility checks in the worst case. Repeating such work for up to `10^5` cases is completely infeasible.

The brute-force approach works because the answer, when it exists, must be somewhere among the possible splits, but the problem gives us much stronger structure than an arbitrary search problem. We do not actually need to find a prime near `n`, because the fixed primes `2` and `3` interact perfectly with parity.

For an even `n`, subtracting the prime `2` leaves an even number. Once that remainder is at least `4`, it is automatically composite. For an odd `n`, subtracting the prime `3` also leaves an even number, and for `n >= 7` that remainder is at least `4`. The search consequently collapses to one parity check and one subtraction.

The resulting algorithm performs only constant work per test case. No primality test, sieve, factorization, or search is required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n sqrt(n))` per case with trial-division primality checks | `O(1)` | Too slow |
| Optimal | `O(1)` per case | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read the value `n`. Values below `6` cannot be represented as a prime plus a composite, so immediately print `-1` for `n < 6`.
2. If `n` is even, print `2` and `n - 2`. The number `2` is prime, while `n - 2` is even and at least `4`, so the second number is composite.
3. If `n` is odd, print `3` and `n - 3`. The number `3` is prime, while `n - 3` is even and at least `4`, so the second number is composite.

The construction always produces positive numbers smaller than `n`. For `n >= 6`, the chosen prime is at most `3`, and the composite part is `n - 2` or `n - 3`, so both are strictly between `0` and `n`.

### Why it works

The invariant behind the construction is that the second number is always an even integer greater than `2`. Every even integer greater than `2` is composite. For even `n`, subtracting prime `2` gives such a number because `n >= 6` implies `n - 2 >= 4`. For odd `n`, subtracting prime `3` gives such a number because `n >= 7` implies `n - 3 >= 4`. The only remaining values are `1` through `5`, and none can contain both a prime and a composite positive integer, so returning `-1` for them is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        if n < 6:
            print(-1)
        elif n % 2 == 0:
            print(2, n - 2)
        else:
            print(3, n - 3)

if __name__ == "__main__":
    solve()
```

The first branch handles every impossible small value. The threshold is `6` rather than `4` because `n = 4` and `n = 5` still cannot contain both a prime and a composite summand.

For an even `n`, the code chooses `2`. The resulting `n - 2` is even and at least `4`, so there is no need to test whether it is composite explicitly.

For an odd `n`, the code chooses `3`. The resulting `n - 3` is again even and at least `4`. Using `3` rather than `2` is necessary because an odd number minus `2` is odd, and an odd number is not automatically composite.

There is no integer overflow issue in Python. In languages with fixed-width integers, the largest value printed here is below `10^9`, so a standard 32-bit signed integer is also sufficient.

The order of the conditions matters conceptually. We first remove the small impossible values, then apply the parity construction. Without the `n < 6` check, values such as `n = 5` would incorrectly enter the odd branch and produce `3 2`, where `2` is prime rather than composite.

## Worked Examples

The sample can be viewed as three test cases, `n = 1`, `n = 6`, and `n = 7`.

| `n` | `n < 6` | Parity | Output |
| --- | --- | --- | --- |
| 1 | true | not reached | `-1` |
| 6 | false | even | `2 4` |
| 7 | false | odd | `3 4` |

For `n = 1`, the small-value condition immediately identifies that no valid decomposition exists. For `n = 6`, the number is even, so `2 + 4` is constructed, with `2` prime and `4` composite. For `n = 7`, the number is odd, so `3 + 4` is constructed. These traces cover the impossible region, the even construction, and the odd construction.

A larger even example, `n = 10`, follows the same rule.

| `n` | `n < 6` | Parity | Prime `x` | Composite `y` | Check |
| --- | --- | --- | --- | --- | --- |
| 10 | false | even | 2 | 8 | `2 + 8 = 10` |

The remainder `8` is even and greater than `2`, so it is automatically composite. No factorization is needed.

A larger odd example, `n = 11`, demonstrates why the odd case uses `3`.

| `n` | `n < 6` | Parity | Prime `x` | Composite `y` | Check |
| --- | --- | --- | --- | --- | --- |
| 11 | false | odd | 3 | 8 | `3 + 8 = 11` |

Choosing `2` here would leave `9`, which happens to be composite, but that is not guaranteed for every odd `n`. Choosing `3` always leaves an even number, giving a uniform construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(T)` | Each test case requires one comparison and at most one parity check. |
| Space | `O(1)` auxiliary | The algorithm stores only the current input value and uses no data structure dependent on `n` or `T`. |

With at most `10^5` test cases, the algorithm performs only a constant number of integer operations per case. Even though `n` can reach `10^9`, its magnitude does not increase the amount of computation. The solution therefore fits comfortably within the stated constraints.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n = int(input())

        if n < 6:
            print(-1)
        elif n % 2 == 0:
            print(2, n - 2)
        else:
            print(3, n - 3)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""3
1
6
7
""") == """-1
2 4
3 4
""", "provided sample"

# Minimum-size input
assert run("""1
1
""") == """-1
""", "minimum n"

# Boundary between impossible and possible values
assert run("""4
4
5
6
7
""") == """-1
-1
2 4
3 4
""", "boundary values"

# Repeated equal values
assert run("""4
6
6
6
6
""") == """2 4
2 4
2 4
2 4
""", "repeated values"

# Maximum-size input
assert run("""1
1000000000
""") == """2 999999998
""", "maximum n"

# Large odd value
assert run("""1
999999999
""") == """3 999999996
""", "large odd n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `-1` | Smallest possible input |
| `4, 5, 6, 7` | `-1, -1, 2 4, 3 4` | Exact transition from impossible to possible |
| `6, 6, 6, 6` | Four copies of `2 4` | Repeated identical test cases |
| `1000000000` | `2 999999998` | Maximum `n` and even construction |
| `999999999` | `3 999999996` | Large odd `n` and odd construction |

The test suite deliberately checks `n = 5` and `n = 6` together because this is the most likely boundary mistake. An implementation using `n <= 5` for the impossible range is correct, while one using `n < 5` would incorrectly accept `5`.

## Edge Cases

For `n = 1`, the algorithm enters the `n < 6` branch and prints `-1`. There is no positive composite number available at all, so this is necessarily impossible.

For `n = 4`, the algorithm also prints `-1`. The only way to use a prime as the first summand is `2 + 2`, but the second `2` is prime, not composite. The distinction matters because merely finding two valid positive summands is not enough.

For `n = 5`, the result is again `-1`. The possible decompositions involving a prime are `2 + 3` and `3 + 2`, and both second summands are prime. This catches implementations that forget that `2` and `3` are not composite.

For `n = 6`, the algorithm takes the first valid even case and outputs `2 4`. Here `2` is prime and `4` is composite, and the sum is exactly `6`. This is the first integer for which the conjectured decomposition exists.

For `n = 7`, the algorithm uses the odd construction and outputs `3 4`. The value `4` is the smallest composite number, making this the first test of the odd branch.

For the maximum value `n = 10^9`, the algorithm outputs `2 999999998`. The second value is even and greater than `2`, so it is composite. The size of `n` has no effect on the number of operations, which is exactly why the constant-time construction handles the upper bound comfortably.
