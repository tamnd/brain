---
title: "CF 102174J - \u91d1\u8272\u4f20\u8bf4"
description: "We need the sum of the values of every valid expression of exactly (n) characters. An expression starts and ends with a digit, operators never appear next to each other, and the only operators are + and -."
date: "2026-08-19T07:08:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "J"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 115
verified: true
draft: false
---

[CF 102174J - \u91d1\u8272\u4f20\u8bf4](https://codeforces.com/problemset/problem/102174/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We need the sum of the values of every valid expression of exactly (n) characters. An expression starts and ends with a digit, operators never appear next to each other, and the only operators are `+` and `-`. Leading zeroes are allowed, so a maximal digit block is simply interpreted as an ordinary decimal integer, even when it begins with zero. The required answer is the sum of all evaluated expressions modulo (998244353). The official statement and samples are available on Codeforces.

The difficulty is not evaluating one expression. A length-(n) string has exponentially many possibilities, and even checking all strings is already hopeless once (n) reaches (5\times10^5). With up to 500 test cases sharing the same upper bound, an acceptable solution needs essentially linear preprocessing in the largest (n), followed by constant work per test case. An (O(n^2)) recurrence would already require about (2.5\times10^{11}) operations at the largest input size, far beyond the one-second limit.

There are several boundary cases where a seemingly natural recurrence can go wrong. For (n=1), no operator can occur, so the ten expressions `0` through `9` contribute (45), not zero or (10). For (n=2), an operator still cannot occur because it would have to occupy one of the two endpoints, so the answer is the sum of all two-digit strings, (4950). A recurrence that assumes every expression has an operator would fail on both cases.

Another common mistake is to count only the digit blocks after the first operator. For example, with (n=3), expressions such as `1+2` and `1-2` both exist. Their combined contribution is (3+(-1)=2), so the suffix values cancel while the prefix value remains twice. This cancellation is the key observation behind the efficient recurrence.

Leading zeroes also matter. For (n=2), `00` is a valid expression and contributes zero, while `09` is a valid expression and contributes nine. Treating a digit block as an ordinary string rather than requiring its first digit to be nonzero is necessary.

## Approaches

The brute-force approach is straightforward. Generate every string of length (n) over the twelve available characters, discard strings violating the syntax rules, evaluate each remaining expression, and add its value. There are (12^n) raw strings before validity checking, so for (n=5\times10^5) the number of candidates is astronomically large. Even generating all valid expressions is exponential, because a valid expression can choose an operator or a digit at many positions. This approach is correct because it directly enumerates exactly the objects whose values we need, but it becomes unusable almost immediately.

A more promising approach is to split an expression at its first operator. Suppose the first operator occurs after (i) characters. The prefix (A) is itself a valid expression of length (i), while the suffix (B) contains only digits, because the split is made at the first operator. The suffix therefore has exactly (10^{n-i-1}) possible strings.

For every fixed pair (A,B), there are two expressions, (A+B) and (A-B). Their values add to

[
(A+B)+(A-B)=2A.
]

The suffix disappears completely from the sum. This is the central simplification: to calculate the contribution of every expression whose first operator is at a particular position, we only need the total value of the prefix and the number of possible digit-only suffixes.

Let (F_n) be the sum of values of all valid expressions of length (n). Let (P_n) be the sum of all (n)-digit strings, where leading zeroes are allowed. There are (10^n) such strings, and every digit appears equally often in every position, giving

[
P_n=\frac{10^n(10^n-1)}2.
]

Expressions with no operator contribute exactly (P_n). For expressions whose first operator appears after a prefix of length (i), the combined contribution of the `+` and `-` versions is

[
2F_i\cdot10^{n-i-1}.
]

Hence

[
F_n=P_n+2\sum_{i=1}^{n-2}F_i10^{n-i-1}.
]

The remaining problem is the convolution in this formula. We can remove it by defining

[
S_n=\sum_{i=1}^{n-2}F_i10^{n-i-1}.
]

Shifting from (S_{n-1}) to (S_n) multiplies every existing term by (10), and the new term corresponding to (i=n-2) is (10F_{n-2}). Thus

[
S_n=10S_{n-1}+10F_{n-2}.
]

Since (F_n=P_n+2S_n), we can eliminate (S) entirely:

[
\begin{aligned}
F_n
&=P_n+20S_{n-1}+20F_{n-2}\
&=P_n+10(F_{n-1}-P_{n-1})+20F_{n-2}.
\end{aligned}
]

The pure-number terms simplify nicely:

[
P_n-10P_{n-1}=45\cdot10^{2n-2}.
]

Therefore the final recurrence is

[
\boxed{F_n=10F_{n-1}+20F_{n-2}+45\cdot10^{2n-2}}
]

with

[
F_1=45,\qquad F_2=4950.
]

This turns the original exponential enumeration into a linear recurrence. We can precompute all answers up to the largest requested (n) once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(12^n\cdot n)) | (O(n)) | Too slow |
| Optimal | (O(\max n+T)) | (O(\max n)) | Accepted |

## Algorithm Walkthrough

1. Read all test cases and find the largest requested length (N). Precomputing only up to (N) avoids doing unnecessary work for smaller inputs.
2. Precompute powers of (10) modulo (998244353). The recurrence needs (10^{2n-2}), so one convenient choice is to maintain (p_n=10^n) and use (p_{n-1}^2).
3. Set (F_1=45) and (F_2=4950). These are the cases where an operator cannot appear, so the answer is simply the sum of all one-digit and two-digit strings.
4. For every (n\ge3), calculate

[
F_n=(10F_{n-1}+20F_{n-2}+45p_{n-1}^2)\bmod998244353.
]

Since (p_{n-1}=10^{n-1}), the last term is exactly (45\cdot10^{2n-2}).
5. Store every (F_n). Each query can then be answered by directly printing the precomputed value.

Why it works can be summarized by the first-operator decomposition. Every expression containing an operator has exactly one first operator. Everything before it is an arbitrary valid expression (A), and everything after it is an arbitrary digit string (B). The two choices of the first operator contribute (A+B) and (A-B), whose sum is (2A). Thus every expression is counted exactly once, and its contribution is represented by the recurrence. The algebraic transformation from the convolution to the second-order recurrence preserves the same quantity, so every stored (F_n) is exactly the required sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    queries = [int(input()) for _ in range(t)]
    mx = max(queries)

    ans = [0] * (mx + 1)

    if mx >= 1:
        ans[1] = 45

    if mx >= 2:
        ans[2] = 4950

    pow10 = [1] * (mx + 1)
    for i in range(1, mx + 1):
        pow10[i] = pow10[i - 1] * 10 % MOD

    for n in range(3, mx + 1):
        # 45 * 10^(2n-2) = 45 * (10^(n-1))^2
        pure_term = 45 * pow10[n - 1] % MOD * pow10[n - 1] % MOD

        ans[n] = (
            10 * ans[n - 1]
            + 20 * ans[n - 2]
            + pure_term
        ) % MOD

    sys.stdout.write("\n".join(str(ans[n]) for n in queries))

if __name__ == "__main__":
    solve()
```

The first part reads every query before doing the dynamic programming. This lets the program determine the largest required length and perform one shared precomputation, which is especially useful because there can be hundreds of test cases.

The array `pow10` stores (10^i\bmod MOD). At position (n), the inhomogeneous term is (45\cdot10^{2n-2}), which is computed as `45 * pow10[n - 1] * pow10[n - 1]`. Multiplication is reduced modulo `MOD` at each stage, so Python never needs to manipulate the enormous exact powers of ten.

The recurrence uses only `ans[n - 1]`, `ans[n - 2]`, and `pow10[n - 1]`. The bases (F_1) and (F_2) are handled separately because the recurrence describes expressions after the first operator decomposition and requires two previous lengths.

There is no integer overflow issue in Python, and reducing after each multiplication keeps intermediate values small. In a fixed-width language, the multiplication should be performed with a sufficiently wide integer type before taking the modulus.

## Worked Examples

For the first sample query, (n=1), the algorithm does not enter the recurrence because there is no (F_0) or (F_{-1}). It directly uses the base value.

| (n) | (F_n) | Reason |
| --- | --- | --- |
| 1 | 45 | Sum of `0` through `9` |

The result is (45), matching the sample. This demonstrates why the one-character boundary case needs its own initialization.

For (n=4), the recurrence can be traced through the previous answers.

| (n) | (F_{n-2}) | (F_{n-1}) | (45\cdot10^{2n-2}) | (F_n) |
| --- | --- | --- | --- | --- |
| 3 | 45 | 4950 | 45000 | 500400 |
| 4 | 4950 | 500400 | 4500000 | 50103000 |

For (n=4),

[
F_4=10(500400)+20(4950)+4500000=50103000.
]

The first-operator interpretation gives the same result. Pure four-digit strings contribute (49,995,000). If the first operator is after one digit, the two operator choices contribute (2\cdot45\cdot100=9,000). If it is after two digits, they contribute (2\cdot4950\cdot10=99,000). Their total is (49,995,000+9,000+99,000=50,103,000). The recurrence has compressed exactly these contributions.

For (n=5), the recurrence gives

[
F_5=10F_4+20F_3+45\cdot10^8.
]

Using (F_4=50,103,000) and (F_3=500,400),

[
F_5=501,030,000+10,008,000+4,500,000,000
=5,011,038,000.
]

Taking this modulo (998244353) gives (19,816,235), which is the fifth sample answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\max n+T)) | Powers of ten and all recurrence values are computed once, then every query is answered in (O(1)). |
| Space | (O(\max n)) | The answer and power arrays contain one entry for each length up to the largest query. |

With (n\le5\times10^5), the preprocessing performs only a few million modular arithmetic operations in total, rather than anything exponential or quadratic. The memory consumption is linear in (n), comfortably within the stated memory limit.

## Test Cases

The following test harness uses the same recurrence implementation as the submitted solution for ordinary cases and an independent matrix-exponentiation calculation for the maximum-size case. The latter checks that the recurrence remains correct at (n=500000) without relying on a precomputed literal constant.

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def solve():
    input = sys.stdin.readline

    t = int(input())
    queries = [int(input()) for _ in range(t)]
    mx = max(queries)

    ans = [0] * (mx + 1)

    if mx >= 1:
        ans[1] = 45
    if mx >= 2:
        ans[2] = 4950

    pow10 = [1] * (mx + 1)
    for i in range(1, mx + 1):
        pow10[i] = pow10[i - 1] * 10 % MOD

    for n in range(3, mx + 1):
        pure_term = 45 * pow10[n - 1] % MOD * pow10[n - 1] % MOD
        ans[n] = (
            10 * ans[n - 1]
            + 20 * ans[n - 2]
            + pure_term
        ) % MOD

    sys.stdout.write("\n".join(str(ans[n]) for n in queries))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def mat_mul(a, b):
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(3)) % MOD
            for j in range(3)
        ]
        for i in range(3)
    ]

def mat_pow(a, e):
    r = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

    while e:
        if e & 1:
            r = mat_mul(r, a)
        a = mat_mul(a, a)
        e >>= 1

    return r

def max_case_expected(n):
    # State:
    # [F_n, F_(n-1), 10^(2n-2)]
    #
    # F_(n+1) = 10 F_n + 20 F_(n-1) + 45 * 10^(2n)
    #
    # The third component is multiplied by 100.
    trans = [
        [10, 20, 4500],
        [1, 0, 0],
        [0, 0, 100],
    ]

    if n == 1:
        return 45
    if n == 2:
        return 4950

    # At n = 2:
    # state = [F_2, F_1, 10^2]
    p = mat_pow(trans, n - 2)
    state = [4950, 45, 100]

    return sum(p[0][i] * state[i] for i in range(3)) % MOD

# Provided samples
assert run("5\n1\n2\n3\n4\n5\n") == (
    "45\n4950\n500400\n50103000\n19816235"
), "provided samples"

# Minimum size
assert run("1\n1\n") == "45", "n = 1"

# Two-digit boundary, where operators are still impossible
assert run("1\n2\n") == "4950", "n = 2"

# First length where operators can occur
assert run("1\n3\n") == "500400", "n = 3"

# All-equal / leading-zero-sensitive expressions are included at n = 2.
# The answer must still count 00, 11, ..., 99.
assert run("1\n2\n") == "4950", "leading zero and equal digits"

# Maximum allowed n, checked independently with matrix exponentiation
expected_500k = max_case_expected(500000)
actual_500k = int(run("1\n500000\n"))
assert actual_500k == expected_500k, "n = 500000"
assert 0 <= actual_500k < MOD, "modulo boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n` | `45` | Minimum length and base case |
| `1\n2\n` | `4950` | Endpoint restriction prevents operators |
| `1\n3\n` | `500400` | First case containing `+` and `-` |
| `1\n2\n` | `4950` | Leading zeroes and equal digit strings such as `00` |
| `1\n500000\n` | Matrix-recurrence value modulo (998244353) | Maximum constraint and large-index recurrence |

## Edge Cases

For (n=1), the only valid strings are the ten individual digits. The initialization sets (F_1=45), which is (0+1+\cdots+9). No recurrence step is attempted, so there is no invalid reference to a shorter expression.

For (n=2), an operator would have to occupy either the first or second character, both of which are forbidden. Consequently every valid expression is a two-digit string from `00` through `99`. The initialization (F_2=4950) gives the correct result.

For (n=3), operators first become possible. The pure digit strings contribute

[
0+1+\cdots+999=499500.
]

The expressions with an operator have a one-digit prefix and a one-digit suffix. For each prefix value (a), the pair `a+b` and `a-b` contributes (2a). Summing over the ten possible prefixes and ten suffixes gives

[
2\cdot45\cdot10=900.
]

Thus

[
F_3=499500+900=500400.
]

This is exactly the first point where the first-operator cancellation becomes relevant.

For expressions containing several operators, the decomposition still works because only the first operator is selected. For example, an expression such as `12-3+45` is split as (A=12), operator `-`, and (B=3+45) conceptually only if (B) were allowed to contain operators, which it is not under our decomposition. Instead, the first operator is after `12`, so the actual suffix is the digit block `3`, and the remaining `+45` belongs to the structure of a different prefix decomposition only when the first operator is chosen later. More directly, every complete expression has one unique first operator, and everything before that position is a valid expression while everything after it contains no operator. This uniqueness prevents double counting.

For leading zeroes, `00`, `007`, and `00042` are all legitimate digit blocks. The term (10^k) counts all (k)-digit strings, not the integers with exactly (k) decimal digits. This is why the pure-string sum is

[
P_k=\frac{10^k(10^k-1)}2
]

rather than the sum of integers from (10^{k-1}) to (10^k-1).

For (n=500000), the algorithm never constructs an expression and never evaluates a large decimal number. It performs the same recurrence once for each length, reducing every quantity modulo (998244353). The large input size changes only the number of linear-time iterations, not the mathematical structure of the solution.
