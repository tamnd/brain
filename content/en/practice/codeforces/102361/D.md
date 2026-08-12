---
title: "CF 102361D - Decimal"
description: "For each test case, we are given a positive integer (n), and we need to decide whether the decimal representation of the fraction (1/n) eventually ends."
date: "2026-08-13T00:07:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "D"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 49
verified: true
draft: false
---

[CF 102361D - Decimal](https://codeforces.com/problemset/problem/102361/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given a positive integer (n), and we need to decide whether the decimal representation of the fraction (1/n) eventually ends. If it can be written using a finite number of digits after the decimal point, we print `No`, because the problem asks whether the decimal is infinite. If the decimal expansion continues forever, we print `Yes`.

For example, (1/5=0.2), so its decimal expansion terminates and the answer is `No`. On the other hand, (1/3=0.333\ldots), so the answer is `Yes`.

There are at most 100 test cases, and every (n) is at most 100. These constraints are extremely small. Even an (O(Tn)) solution performs at most about 10,000 basic iterations, so there is no realistic performance concern. We can still derive the number-theoretic condition that solves each test case in logarithmic time.

The key edge cases are denominators such as (1), (2), (4), (5), (8), (10), (20), and (25). For example, the input

```
1
1
```

must produce

```
No
```

because (1/1=1), which has no infinite fractional part. A careless implementation that assumes every fraction must have digits after the decimal point could incorrectly classify it as infinite.

Another boundary case is

```
1
10
```

whose answer is also `No`, because (1/10=0.1). The denominator contains both a factor of 2 and a factor of 5, and both are allowed.

The opposite case is

```
1
6
```

whose answer is `Yes`, because (1/6=0.1666\ldots). The factor 3 remains in the denominator after removing all factors of 2 and 5. An implementation that only checks whether (n) is even or odd would miss this case.

## Approaches

A direct way to solve the problem is to simulate long division. When computing (1/n), the current remainder is multiplied by 10 before producing the next decimal digit. If the remainder ever becomes zero, the decimal terminates. If a remainder repeats, the same sequence of digits starts repeating, so the decimal is infinite. There are at most (n) possible remainders, so one test case takes (O(n)) time. With (T\le100) and (n\le100), the worst case is fewer than 10,000 remainder transitions, so this approach is easily fast enough for the given constraints.

The more useful observation comes from the structure of terminating decimal fractions. A finite decimal always has the form (a/10^k) for some integers (a) and (k). Since (10^k=2^k5^k), the only prime factors that can appear in a reduced denominator of a terminating decimal are 2 and 5.

Because the numerator here is exactly 1, the fraction (1/n) is already reduced. Consequently, its decimal representation terminates exactly when (n) contains no prime factor other than 2 and 5.

We can test this by repeatedly dividing (n) by 2 while possible, then repeatedly dividing it by 5 while possible. If the remaining value is 1, every prime factor was 2 or 5, so the decimal terminates and the answer is `No`. If some other factor remains, the decimal is infinite and the answer is `Yes`.

The brute-force method works because long division eventually either reaches remainder zero or repeats a remainder. The factorization observation replaces potentially many simulated decimal digits with a handful of divisions. For this problem both methods are fast enough, but the factor-based solution captures the mathematical condition directly and generalizes cleanly to the standard question of whether a rational number has a terminating decimal expansion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Tn)) | (O(n)) | Accepted |
| Optimal | (O(T\log n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) for the current test case. We only need to inspect its prime factors, so there is no need to construct the decimal representation.
2. Repeatedly divide (n) by 2 while it is divisible by 2. Every factor of 2 is allowed in the denominator of a terminating decimal.
3. Repeatedly divide the remaining value by 5 while it is divisible by 5. Factors of 5 are the other allowed prime factors.
4. Check the remaining value. If it is exactly 1, the original denominator consisted only of factors 2 and 5, so (1/n) terminates and we print `No`.
5. If the remaining value is greater than 1, it contains some prime factor other than 2 or 5. Such a factor cannot divide any power of 10, so the decimal expansion cannot terminate and we print `Yes`.

### Why it works

Suppose (1/n) has a finite decimal expansion. Then there is some (k) such that

[
\frac{1}{n}=\frac{m}{10^k}
]

for an integer (m). Rearranging gives (10^k=mn), so (n) must divide (10^k). Since (10^k=2^k5^k), every prime factor of (n) must be either 2 or 5.

Conversely, if (n=2^a5^b), choose (k=\max(a,b)). Then (n) divides (10^k), so (1/n) can be expressed with denominator (10^k), giving a finite decimal expansion.

The algorithm removes exactly all factors 2 and 5. Thus the remaining value is 1 exactly when the decimal terminates. This makes the printed answer correct for every possible input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        while n % 2 == 0:
            n //= 2

        while n % 5 == 0:
            n //= 5

        if n == 1:
            print("No")
        else:
            print("Yes")

if __name__ == "__main__":
    solve()
```

The first loop removes every factor of 2 from the denominator. The condition uses `n % 2 == 0` before the division, so the loop stops precisely when no factor of 2 remains.

The second loop performs the same operation for 5. The order of these two loops does not affect the result because multiplication of prime factors is commutative.

After both loops, `n == 1` means that nothing except factors of 2 and 5 was present originally. In that case the decimal is finite, so the required answer is `No`. If `n` is greater than 1, some other prime factor remains, so the answer is `Yes`.

Python integers do not have an overflow issue here, and the algorithm only decreases `n`. The largest input is just 100, so the implementation is also comfortably within the stated input bounds.

## Worked Examples

The sample consists of the two test cases (n=5) and (n=3).

For (n=5), the algorithm removes the factor 5 and reaches 1.

| Step | Current (n) | Action |
| --- | --- | --- |
| Start | 5 | Check factors |
| Remove 2 | 5 | Not divisible by 2 |
| Remove 5 | 1 | Divide by 5 |
| Final | 1 | Print `No` |

This matches (1/5=0.2). Once the denominator becomes 1, every original prime factor has been shown to be compatible with a power of 10.

For (n=3), neither factor-removal loop changes the value.

| Step | Current (n) | Action |
| --- | --- | --- |
| Start | 3 | Check factors |
| Remove 2 | 3 | Not divisible by 2 |
| Remove 5 | 3 | Not divisible by 5 |
| Final | 3 | Print `Yes` |

The remaining factor 3 proves that no power of 10 can be divisible by the original denominator. Consequently, the decimal cannot terminate, matching (1/3=0.333\ldots).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T\log n)) | Each division by 2 or 5 reduces (n) by a constant factor. |
| Space | (O(1)) | Only the current denominator and loop variables are stored. |

With (T\le100) and (n\le100), each test case requires only a few integer divisions. The total work is tiny, and the constant memory usage is independent of the number of test cases.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n = int(input())

        while n % 2 == 0:
            n //= 2

        while n % 5 == 0:
            n //= 5

        print("No" if n == 1 else "Yes")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# Provided sample
assert run("""2
5
3
""") == """No
Yes
""", "provided sample"

# Minimum-size input
assert run("""1
1
""") == """No
""", "n = 1 terminates immediately"

# Maximum-size input
assert run("""1
100
""") == """No
""", "100 = 2^2 * 5^2"

# Several powers of 2 and 5
assert run("""6
2
4
5
8
20
25
""") == """No
No
No
No
No
No
""", "all denominators contain only 2 and 5"

# Values containing another prime factor
assert run("""5
3
6
7
12
99
""") == """Yes
Yes
Yes
Yes
Yes
""", "each denominator has a prime factor other than 2 or 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `No` | Minimum value and the special case where the denominator is already 1 |
| `1 / 100` | `No` | Maximum value and repeated removal of both 2 and 5 |
| `2, 4, 5, 8, 20, 25` | All `No` | Pure powers and products of the two allowed primes |
| `3, 6, 7, 12, 99` | All `Yes` | Presence of a forbidden prime factor |

## Edge Cases

For (n=1), the input is

```
1
1
```

The algorithm enters both factor-removal loops, but neither loop executes because 1 is divisible by neither 2 nor 5. The final value is already 1, so the answer is `No`. This correctly handles the fact that (1/1) is an integer and has a finite decimal representation.

For (n=10), the input is

```
1
10
```

The first loop does nothing because 10 is odd. The second loop divides 10 by 5 and leaves 2, then divides 2 by 5 no further. At first this might appear to leave a non-one value, but the factor 2 still has to be removed. This is why the loops in the actual algorithm process both primes independently. Starting from 10, the 2-loop removes 2 first, leaving 5, and the 5-loop then removes 5, reaching 1. The output is `No`.

For (n=6), the input is

```
1
6
```

The 2-loop changes 6 to 3. The 5-loop cannot change 3. The remaining value is 3, so the answer is `Yes`. This is the characteristic case where removing all allowed factors exposes a forbidden factor.

For (n=100), the input is

```
1
100
```

The denominator factors as (100=2^2\cdot5^2). The algorithm repeatedly removes factors 2 until reaching 25, then repeatedly removes factors 5 until reaching 1. The answer is `No`, confirming that the boundary value behaves exactly like the smaller terminating denominators.
