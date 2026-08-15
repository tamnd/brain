---
title: "CF 102388A - Strange Base"
description: "We need to print the unique canonical representation of a positive integer (n) using powers of the golden ratio [ phi=frac{1+sqrt5}{2}. ] Each position contains either (0) or (1), and two neighboring positions can never both contain (1)."
date: "2026-08-15T08:21:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "A"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 617
verified: true
draft: false
---

[CF 102388A - Strange Base](https://codeforces.com/problemset/problem/102388/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to print the unique canonical representation of a positive integer (n) using powers of the golden ratio

[
\phi=\frac{1+\sqrt5}{2}.
]

Each position contains either (0) or (1), and two neighboring positions can never both contain (1). Unlike an ordinary positional system, useful positions can have negative exponents, so the output may contain a fractional part. For example,

[
2=\phi^1+\phi^{-2},
]

which is written as `10.01`.

The input contains at most ten independent integers, with every (n\le 100000). A solution that is quadratic in (n) would already perform up to (10^{10}) operations for one test case, far beyond the one second limit. Even an approach that explores exponentially many digit strings is completely infeasible. We need an algorithm whose work grows roughly with the number of base-(\phi) positions, which is only logarithmic in (n).

There are several edge cases that are easy to mishandle. The smallest input is (n=1), whose answer is simply `1`. A formatter that always prints a radix point could incorrectly produce `1.`.

The first number that needs negative powers is (n=2). Its answer is

```
2
10.01
```

A method that only searches powers (\phi^0,\phi^1,\phi^2,\ldots) can never finish, because (2) is not a sum of the required positive powers.

Floating point arithmetic is another dangerous case. For (n=2), the exact identity is (\phi+\phi^{-2}=2), but evaluating the two terms with ordinary floating point can leave a tiny residual instead of exactly zero. A loop that keeps generating negative powers until the residual becomes zero can then produce incorrect extra digits. The solution below never evaluates (\phi) numerically.

Finally, adjacent ones must be forbidden. For example, (4) is represented as `101.01`, not by an arbitrary combination of nearby powers. The greedy process automatically creates the required separation because of the identity

[
\phi^{k+1}-\phi^k=\phi^{k-1}.
]

The greedy characterization used here is the standard canonical, or Bergman, base-(\phi) representation.

## Approaches

A direct brute-force solution would choose a range of exponents and enumerate every possible binary digit string, rejecting strings containing adjacent ones and checking which remaining string evaluates to (n). This is correct in principle because the required representation is finite and unique, but the search space grows exponentially. For a 49-position range, there are (F_{51}=20,365,011,074) binary strings with no adjacent ones, so even testing one candidate in constant time would already be hopeless for the largest inputs.

A more natural but still unsuitable approach is to repeatedly add or subtract powers of (\phi) while maintaining a symbolic expression. It avoids enumerating all strings, but without the greedy observation there is no reason to know which power should be chosen next, so the algorithm still has to explore alternatives.

The key observation is that the canonical representation can be constructed greedily. At every point, let (r) be the positive remainder still to represent. Choose the largest power (\phi^k) satisfying

[
\phi^k\le r.
]

Put a (1) at position (k), then replace (r) with (r-\phi^k). Repeating this eventually reaches zero and produces the canonical representation. This is exactly the greedy characterization of the minimal base-(\phi) representation.

There is a second difficulty: comparisons involving (\phi) cannot safely use ordinary floating point. The useful algebraic fact is that every power of (\phi) can be written exactly as

[
a+b\phi
]

for integers (a,b). Since

[
\phi^2=\phi+1,
]

multiplying such a pair by (\phi) is just

[
(a+b\phi)\phi=b+(a+b)\phi.
]

Likewise, because (1/\phi=\phi-1), dividing by (\phi) is

[
(a+b\phi)/\phi=(b-a)+a\phi.
]

So we can generate every required power using integer arithmetic alone.

The comparison itself can also be exact. For

[
x=a+b\phi,
]

write

[
x=\frac{(2a+b)+b\sqrt5}{2}.
]

The sign of this expression can be determined using only integer multiplication and comparison. There is no numerical approximation anywhere in the algorithm.

The brute-force approach therefore fails because the number of valid digit strings is exponential, while the observation that the canonical representation is greedy reduces the problem to scanning the powers once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(F_L)), where (L) is the number of positions | (O(L)) | Too slow |
| Greedy with exact algebraic arithmetic | (O(L)) | (O(L)) | Accepted |

## Algorithm Walkthrough

1. Represent every algebraic number in the form ((a,b)), meaning (a+b\phi). The input integer (n) starts as ((n,0)), and the current remainder is stored in the same form.
2. Find the largest exponent (k) for which (\phi^k\le n). Start with (\phi^0=1) and repeatedly multiply the current power by (\phi) while it does not exceed (n). Since (\phi>1), the process stops after (O(\log n)) iterations.
3. Starting from this largest exponent, process powers in decreasing order. At exponent (k), compare the current remainder with (\phi^k). If the power fits, put digit (1) at this position and subtract the power from the remainder. Otherwise put digit (0).
4. After each position, divide the current power by (\phi) using the exact pair transformation ((a,b)\mapsto(b-a,a)). This moves from exponent (k) to exponent (k-1).
5. Stop as soon as the remainder becomes exactly ((0,0)). The finite-representation property guarantees that the greedy process reaches zero.
6. The digits have been collected from the largest exponent down to the smallest exponent. Split them immediately after exponent (0), remove unnecessary leading zeroes from the integer part and trailing zeroes from the fractional part, and insert the decimal point only if a fractional digit remains.

The reason adjacent ones never appear follows directly from the greedy choice. Suppose (\phi^k) is selected. Before selecting it, the remainder was smaller than (\phi^{k+1}), because (k) was the largest possible exponent. After subtraction, the new remainder is therefore smaller than

[
\phi^{k+1}-\phi^k=\phi^{k-1}.
]

Consequently, the next position (k-1) cannot possibly be selected. The greedy process automatically satisfies the no-adjacent-ones rule.

**Why it works.** At every iteration, the remainder (r) is exactly the value represented by all digits that have not yet been chosen. The algorithm selects the largest power not exceeding (r), which is precisely the defining choice of the canonical greedy representation. Subtracting that power preserves the invariant, and the identity (\phi^{k+1}-\phi^k=\phi^{k-1}) proves that two consecutive selected positions are impossible. When the remainder reaches zero, the selected powers sum exactly to the original (n), and uniqueness of the canonical representation means the resulting digit sequence is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mul_phi(p):
    a, b = p
    return (b, a + b)

def div_phi(p):
    a, b = p
    return (b - a, a)

def nonnegative(a, b):
    """
    Return whether a + b*phi >= 0 exactly.

    a + b*phi = (2*a + b + b*sqrt(5)) / 2.
    """
    c = 2 * a + b

    if c == 0:
        return b >= 0

    if b > 0 and c > 0:
        return True

    if b < 0 and c < 0:
        return False

    if c > 0:
        return c * c >= 5 * b * b

    return 5 * b * b >= c * c

def geq(x, y):
    """
    Return whether x >= y for two numbers represented as
    (a, b) = a + b*phi.
    """
    a = x[0] - y[0]
    b = x[1] - y[1]
    return nonnegative(a, b)

def solve_one(n):
    # Find the largest non-negative exponent whose power does not exceed n.
    power = (1, 0)  # phi^0
    k = 0

    while True:
        nxt = mul_phi(power)
        if not geq((n, 0), nxt):
            break
        power = nxt
        k += 1

    max_k = k
    remainder = (n, 0)
    digits = []

    # Greedily process phi^k, phi^(k-1), ...
    while remainder != (0, 0):
        if geq(remainder, power):
            digits.append('1')
            remainder = (
                remainder[0] - power[0],
                remainder[1] - power[1]
            )
        else:
            digits.append('0')

        power = div_phi(power)
        k -= 1

    s = ''.join(digits)

    # The digit corresponding to phi^0 is at index max_k.
    split = max_k + 1
    left = s[:split].lstrip('0')
    right = s[split:].rstrip('0')

    if not left:
        left = '0'

    if right:
        return left + '.' + right

    return left

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        out.append(solve_one(n))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()
```

The `mul_phi` function implements

[
(a+b\phi)\phi=b+(a+b)\phi,
]

so it moves one exponent to the right. The `div_phi` function implements multiplication by (\phi^{-1}=\phi-1), which moves one exponent to the left.

The `nonnegative` function is the critical precision detail. It never converts (\phi) to a floating point number. For (a+b\phi), multiplying by (2) gives (2a+b+b\sqrt5). If the two irrational components have the same sign, the answer is immediate. If their signs differ, squaring the two positive quantities gives an exact comparison between (c^2) and (5b^2).

The first loop locates the largest usable non-negative exponent. The second loop then performs the greedy construction from that exponent downward. The loop is allowed to pass into negative exponents, which is necessary because integers such as (2) and (123) require fractional positions.

The output formatting uses `max_k + 1` as the split position because the digit at exponent (0) is exactly the last digit of the integer part. Leading zeroes before the most significant (1) and trailing zeroes after the least significant (1) are removed. The decimal point is printed only when there is a non-empty fractional part.

Python integers have arbitrary precision, so there is no integer overflow issue even though the coefficients of powers grow like Fibonacci numbers.

## Worked Examples

For the sample value (n=2), the largest power not exceeding (2) is (\phi^1). The greedy process then reaches the exact representation (\phi+\phi^{-2}).

| Exponent (k) | Current power | Remainder before step | Action | Remainder after step |
| --- | --- | --- | --- | --- |
| (1) | (\phi) | (2) | choose (1) | (2-\phi) |
| (0) | (1) | (2-\phi) | choose (0) | (2-\phi) |
| (-1) | (\phi^{-1}) | (2-\phi) | choose (0) | (2-\phi) |
| (-2) | (\phi^{-2}) | (2-\phi) | choose (1) | (0) |

Since (\phi^{-2}=2-\phi), the final digits are `10.01`. The trace also shows why the fractional part cannot simply be treated like an ordinary decimal fraction.

For the constructed second example (n=5), the largest usable power is (\phi^3). The exact remainder gradually becomes small enough that the final correction is made with negative powers.

| Exponent (k) | Current power | Remainder before step | Action | Remainder after step |
| --- | --- | --- | --- | --- |
| (3) | (1+2\phi) | (5) | choose (1) | (4-2\phi) |
| (2) | (1+\phi) | (4-2\phi) | choose (0) | (4-2\phi) |
| (1) | (\phi) | (4-2\phi) | choose (0) | (4-2\phi) |
| (0) | (1) | (4-2\phi) | choose (0) | (4-2\phi) |
| (-1) | (-1+\phi) | (4-2\phi) | choose (1) | (5-3\phi) |
| (-2) | (2-\phi) | (5-3\phi) | choose (0) | (5-3\phi) |
| (-3) | (-3+2\phi) | (5-3\phi) | choose (0) | (5-3\phi) |
| (-4) | (5-3\phi) | (5-3\phi) | choose (1) | (0) |

The resulting representation is `1000.1001`. The exact pair representation makes the final subtraction equal to zero rather than merely close to zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log n)) | The greedy scan processes a number of powers proportional to the representation length, which grows logarithmically with (n). |
| Space | (O(\log n)) | The output digits and the exact algebraic coefficients both require only one entry per processed exponent. |

For (n\le100000), the number of processed positions is only a few dozen. With at most ten test cases, the total amount of arithmetic is tiny compared with the one second time limit, and the memory usage is negligible compared with 256 MB.

## Test Cases

```python
# helper: run the solution on an input string
import sys
import io

def mul_phi(p):
    a, b = p
    return (b, a + b)

def div_phi(p):
    a, b = p
    return (b - a, a)

def nonnegative(a, b):
    c = 2 * a + b

    if c == 0:
        return b >= 0

    if b > 0 and c > 0:
        return True

    if b < 0 and c < 0:
        return False

    if c > 0:
        return c * c >= 5 * b * b

    return 5 * b * b >= c * c

def geq(x, y):
    a = x[0] - y[0]
    b = x[1] - y[1]
    return nonnegative(a, b)

def solve_one(n):
    power = (1, 0)
    k = 0

    while True:
        nxt = mul_phi(power)
        if not geq((n, 0), nxt):
            break
        power = nxt
        k += 1

    max_k = k
    remainder = (n, 0)
    digits = []

    while remainder != (0, 0):
        if geq(remainder, power):
            digits.append('1')
            remainder = (
                remainder[0] - power[0],
                remainder[1] - power[1]
            )
        else:
            digits.append('0')

        power = div_phi(power)
        k -= 1

    s = ''.join(digits)
    split = max_k + 1

    left = s[:split].lstrip('0')
    right = s[split:].rstrip('0')

    if not left:
        left = '0'

    return left + ('.' + right if right else '')

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    t = int(input())
    ans = [solve_one(int(input())) for _ in range(t)]

    sys.stdin = old_stdin
    return '\n'.join(ans)

# Provided sample
assert run(
    """5
1
2
3
100000
123
"""
) == (
    """1
10.01
100.01
101010001010100000100000.101000101000000010000001
10000000000.0000000001"""
), "sample 1"

# Minimum value and repeated equal values
assert run(
    """4
1
1
1
1
"""
) == (
    """1
1
1
1"""
), "minimum and repeated values"

# First values that require fractional powers
assert run(
    """2
2
3
"""
) == (
    """10.01
100.01"""
), "negative exponent boundary"

# Values with several separated one digits
assert run(
    """2
5
18
"""
) == (
    """1000.1001
1000000.000001"""
), "multiple separated digits"

# Maximum input value
assert run(
    """1
100000
"""
) == (
    """101010001010100000100000.101000101000000010000001"""
), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1, 1, 1, 1` | `1, 1, 1, 1` | Minimum value and repeated equal inputs |
| `2, 3` | `10.01, 100.01` | First cases requiring negative exponents |
| `5, 18` | `1000.1001, 1000000.000001` | Several separated selected powers |
| `100000` | `101010001010100000100000.101000101000000010000001` | Maximum allowed input and long fractional output |

## Edge Cases

For (n=1), the largest usable power is (\phi^0=1). The first greedy step subtracts exactly (1), leaving the pair ((0,0)). The digit sequence contains only `1`, so the formatter prints `1` without a decimal point.

For (n=2), the algorithm first chooses (\phi^1), leaving (2-\phi). The next two powers, (1) and (\phi^{-1}), are both too large. At exponent (-2), the power is exactly (2-\phi), so the remainder becomes zero. The output is `10.01`. This case demonstrates why negative exponents are essential.

For (n=3), the first selected power is (\phi^2=1+\phi). The remainder is (2-\phi=\phi^{-2}), so the output is `100.01`. The greedy choice also demonstrates the adjacency invariant, since selecting exponent (2) makes exponent (1) impossible.

For (n=5), the selected exponents are (3,-1,-4). The corresponding value is

[
\phi^3+\phi^{-1}+\phi^{-4}=5,
]

so the output is `1000.1001`. The two selected negative positions are separated by two zeroes, showing that the no-adjacent-ones rule applies across the radix point just as it does on the integer side.

For (n=123), the answer is `10000000000.0000000001`. This means

[
123=\phi^{10}+\phi^{-10}.
]

The two algebraic terms are individually irrational, but their (\phi)-coefficients cancel exactly. The integer-pair representation handles this cancellation without ever depending on floating point precision.

For (n=100000), the algorithm continues the same process for only a few dozen positions and reaches zero exactly. The long answer is not a sign of an expensive algorithm, because the work is proportional to the number of digits rather than to the numeric value (100000).
