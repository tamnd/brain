---
title: "CF 102163M - NCD Salary"
description: "For each test case, there are two salaries represented as powers. The original salary is (B1^{P1}), while the new salary is (B2^{P2}). We need to compare these two values without actually needing to print either salary."
date: "2026-08-20T00:28:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "M"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 1546
verified: false
draft: false
---

[CF 102163M - NCD Salary](https://codeforces.com/problemset/problem/102163/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 25m 46s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case, there are two salaries represented as powers. The original salary is (B_1^{P_1}), while the new salary is (B_2^{P_2}). We need to compare these two values without actually needing to print either salary. If the new salary is larger, the answer is `Congrats`; if it is smaller, the answer is `HaHa`; if both salaries are equal, the answer is `Lazy`. The official problem has (B) and (P) ranging from (0) to (10^6).

The first difficulty is that the exponents can be as large as one million. Even though the inputs themselves fit comfortably in ordinary integers, (10^6{}^{10^6}) has about six million decimal digits. Constructing such numbers just to compare them is wasteful. The input contains (T) independent comparisons, so the work per test case needs to remain very small. A solution based on explicitly constructing the powers can quickly become dominated by arbitrary-precision multiplication and memory usage, while a logarithmic comparison needs only a handful of floating-point operations per case.

There are several boundary cases that can silently break a straightforward implementation. A base of zero cannot be passed directly to `log`, because (\log(0)) is undefined. For example,

```
1
0 5 2 3
```

represents (0^5) versus (2^3), so the new salary is larger and the answer is `Congrats`. A direct logarithmic calculation would attempt to evaluate `log(0)`.

An exponent of zero is another special case. For a positive base, (B^0=1). For example,

```
1
7 0 3 2
```

compares (1) with (9), so the answer is `Congrats`. The logarithmic expression handles positive bases naturally because (0\cdot\log(B)=0).

Equality can also be deceptive. The bases do not have to be identical. For example,

```
1
2 4 4 2
```

compares (2^4) with (4^2), both equal to (16), so the answer is `Lazy`. Comparing only the bases would incorrectly report that the second salary is larger.

The contest's accepted approach treats a zero base as a zero salary, including the degenerate `0 0` representation, and handles it before taking logarithms. This convention is consistent with the accepted solutions for the problem.

## Approaches

The most direct approach is to calculate both powers and compare the resulting integers. Mathematically this is completely correct because it computes exactly the two quantities we care about. For example, we could calculate `pow(B1, P1)` and `pow(B2, P2)` and compare them.

The problem is the size of those integers. In the worst case, (B=10^6) and (P=10^6), so the result contains roughly (6\times10^6) decimal digits, or about (2\times10^7) bits. A single exponentiation consequently operates on multi-megabyte integers, and repeated arbitrary-precision multiplications make this approach far too expensive when there are many test cases. The exact number of elementary machine-word operations depends on the big-integer implementation, so the useful complexity statement is that the arithmetic cost grows with the number of bits in the enormous result rather than with the constant-size input.

The key observation is that the ordering of positive numbers is preserved by the logarithm. For positive (B),

[
B^P = e^{P\ln B}.
]

Since the exponential function is strictly increasing,

[
B_1^{P_1} < B_2^{P_2}
]

is equivalent to

[
P_1\ln B_1 < P_2\ln B_2.
]

The enormous powers have disappeared. We only calculate two products involving numbers at most (10^6). This is exactly why logarithms fit the structure of the problem: the exponent that would make the integer enormous becomes an ordinary multiplication.

The zero-base cases must be separated first because (\ln 0) does not exist. After that, the comparison uses floating-point logarithms with a small tolerance. This is also the approach used by published accepted solutions for this problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Depends on huge integer size, up to millions of decimal digits per power | Depends on huge integer size | Too slow |
| Logarithms | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (B_1,P_1,B_2,P_2). The first pair represents the old salary and the second pair represents the new salary.
2. Check whether either base is zero. If both bases are zero, both salaries are treated as zero under the problem's contest convention, so print `Lazy`. If only (B_1) is zero, the old salary is zero and the new salary is positive, so print `Congrats`. If only (B_2) is zero, the new salary is zero and the old salary is positive, so print `HaHa`. This check also prevents an invalid call to `log(0)`.
3. For positive bases, calculate

[
x_1=P_1\ln(B_1),\qquad x_2=P_2\ln(B_2).
]

We do not calculate either original salary. The values (x_1) and (x_2) are their natural logarithms.
4. Compare (x_1) and (x_2). If their difference is extremely small, print `Lazy`, because the floating-point calculations represent the two logarithms as equal within the intended numerical precision.
5. If (x_1<x_2), the new salary is larger, so print `Congrats`. Otherwise (x_1>x_2), meaning the new salary is smaller, so print `HaHa`.

### Why it works

For positive bases, the logarithm is strictly increasing, so applying it cannot change the ordering of the two salaries. We have

[
\ln(B_1^{P_1})=P_1\ln(B_1)
]

and

[
\ln(B_2^{P_2})=P_2\ln(B_2).
]

Thus comparing the two products is equivalent to comparing the original salaries. Zero bases are handled separately before this transformation, so the algorithm never evaluates an undefined logarithm. The only approximation comes from floating-point arithmetic, which is handled with a small tolerance as expected by the problem's intended solution. Published solutions use the same logarithmic transformation and an epsilon around (10^{-7}).

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        b1, p1, b2, p2 = map(int, input().split())

        if b1 == 0 or b2 == 0:
            if b1 == b2:
                out.append("Lazy")
            elif b1 < b2:
                out.append("Congrats")
            else:
                out.append("HaHa")
            continue

        x1 = p1 * math.log(b1)
        x2 = p2 * math.log(b2)

        if abs(x1 - x2) <= 1e-7:
            out.append("Lazy")
        elif x1 < x2:
            out.append("Congrats")
        else:
            out.append("HaHa")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The program first imports `math` because the entire optimization comes from replacing a huge power with its logarithm. The output is accumulated in `out` and written once at the end, which avoids repeated output calls when there are many test cases.

The zero-base branch comes before every call to `math.log`. This is both mathematically necessary and an implementation detail that is easy to overlook. A call such as `math.log(0)` raises an exception.

For positive bases, `p1 * math.log(b1)` is exactly the logarithmic form (P_1\ln B_1). Python's integer multiplication is safe here because `p1` is at most (10^6) and `math.log(b1)` is an ordinary floating-point value.

The `1e-7` tolerance follows the intended solution strategy used in published solutions. The comparison is performed on logarithms rather than on the original powers, so no huge integer is ever constructed.

## Worked Examples

For the first sample, consider the three test cases one at a time.

| (B_1) | (P_1) | (B_2) | (P_2) | (P_1\ln B_1) | (P_2\ln B_2) | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | 4 | 2 | (3\ln2) | (2\ln4=4\ln2) | Congrats |
| 2 | 2 | 3 | 1 | (2\ln2) | (\ln3) | HaHa |
| 2 | 4 | 4 | 2 | (4\ln2) | (2\ln4=4\ln2) | Lazy |

In the first case, (3\ln2<4\ln2), so (2^3<4^2) and the new salary is larger. In the second case, (2\ln2>\ln3), so (2^2>3). The third case demonstrates that different base and exponent pairs can produce exactly the same salary.

A useful additional trace is the zero-base case and an exponent-zero case.

| (B_1) | (P_1) | (B_2) | (P_2) | Branch | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 3 | Zero base, only old salary is zero | Congrats |
| 7 | 0 | 3 | 2 | Positive bases, logarithms give (0) and (2\ln3) | Congrats |
| 2 | 4 | 4 | 2 | Positive bases, logarithmic values are equal | Lazy |

The first row never calls `log(0)`. The second row shows that an exponent of zero naturally becomes a logarithmic value of zero because (7^0=1). The final row confirms the equality condition through the identity (2^4=4^2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs a constant number of arithmetic and logarithm operations |
| Space | (O(T)) | The output strings are stored before one final write |

The logarithm operation works on ordinary floating-point numbers, so its cost is constant for the purposes of competitive-programming complexity analysis. With input values capped at (10^6), the algorithm never creates the multi-million-digit salary values that make direct exponentiation unattractive. The 256 MB memory limit is easily sufficient for the constant-size per-test-case state and the output buffer.

## Test Cases

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        b1, p1, b2, p2 = map(int, input().split())

        if b1 == 0 or b2 == 0:
            if b1 == b2:
                out.append("Lazy")
            elif b1 < b2:
                out.append("Congrats")
            else:
                out.append("HaHa")
            continue

        x1 = p1 * math.log(b1)
        x2 = p2 * math.log(b2)

        if abs(x1 - x2) <= 1e-7:
            out.append("Lazy")
        elif x1 < x2:
            out.append("Congrats")
        else:
            out.append("HaHa")

    sys.stdout.write("\n".join(out))

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

assert run(
    """3
2 3 4 2
2 2 3 1
2 4 4 2
"""
) == """Congrats
HaHa
Lazy""", "sample 1"

assert run(
    """1
1 0 1 0
"""
) == "Lazy", "minimum positive-base equality"

assert run(
    """1
0 5 1000000 1000000
"""
) == "Congrats", "zero old salary"

assert run(
    """1
1000000 1000000 999999 1000000
"""
) == "HaHa", "maximum-size values"

assert run(
    """4
2 4 4 2
3 1 3 1
10 0 2 1
2 1 1 1000000
"""
) == """Lazy
Lazy
HaHa
HaHa""", "equality and exponent boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 4 2` | `Congrats` | Basic logarithmic comparison |
| `1 0 1 0` | `Lazy` | Both exponents are zero |
| `0 5 1000000 1000000` | `Congrats` | Zero-base handling |
| `1000000 1000000 999999 1000000` | `HaHa` | Maximum input magnitudes without constructing huge powers |
| `2 4 4 2` | `Lazy` | Equality with different bases |
| `10 0 2 1` | `HaHa` | (10^0=1<2) |
| `2 1 1 1000000` | `HaHa` | Large exponent on the second salary |

## Edge Cases

A zero base must be handled before logarithms. For

```
1
0 5 2 3
```

the first salary is (0^5=0), while the second is (2^3=8). The algorithm enters the zero-base branch, sees that only (B_1) is zero, and prints `Congrats`. No call to `log(0)` occurs.

Two zero bases produce equal salaries under the contest's intended zero-base convention. For

```
1
0 7 0 3
```

the algorithm sees `b1 == b2 == 0` and prints `Lazy`. The exponents do not matter once the base-zero branch is selected.

An exponent of zero does not require a separate branch when the base is positive. For

```
1
10 0 2 1
```

the logarithmic values are (0) and (\ln2). Since (0<\ln2), the algorithm prints `Congrats` for the new salary. For the reverse comparison,

```
1
2 1 1 1000000
```

the values are (\ln2) and (0), so the algorithm prints `HaHa`.

Finally, equality cannot be inferred from equal bases alone. With

```
1
2 4 4 2
```

the logarithmic values are (4\ln2) and (2\ln4). Since (\ln4=2\ln2), both expressions are exactly (4\ln2), so the difference falls within the equality tolerance and the answer is `Lazy`. This is the central reason the algorithm compares the complete (P\ln B) expressions rather than inspecting either input pair independently.
