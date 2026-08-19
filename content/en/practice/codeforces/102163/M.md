---
title: "CF 102163M - NCD Salary"
description: "For each test case, there are two salaries. The original salary is (B1^{P1}), while the amount actually received is (B2^{P2}). We have to determine whether the second value is larger, smaller, or exactly equal to the first."
date: "2026-08-19T07:58:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "M"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 244
verified: false
draft: false
---

[CF 102163M - NCD Salary](https://codeforces.com/problemset/problem/102163/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 4s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case, there are two salaries. The original salary is (B_1^{P_1}), while the amount actually received is (B_2^{P_2}). We have to determine whether the second value is larger, smaller, or exactly equal to the first. The required outputs are `Congrats`, `HaHa`, and `Lazy`, respectively. The original problem uses (0 \le B,P \le 10^6), with each power guaranteed not to have both its base and exponent equal to zero.

The bounds make direct construction of the powers unattractive. An exponent can be (10^6), so repeatedly multiplying to construct one value can take up to (10^6) multiplications, and doing this for both salaries takes up to (2\cdot10^6) multiplications per test case. The resulting integers are also enormous. For example, (2^{10^6}) has hundreds of thousands of decimal digits, so arithmetic on the complete values is much more expensive than the original input size suggests. Since the comparison itself only needs a single result, building those integers is unnecessary work.

There are several edge cases that can silently break a logarithm-based implementation. The first is a zero base. For example,

```
1
0 5 2 3
```

has salaries (0^5=0) and (2^3=8), so the answer is `Congrats`. Calling `log(0)` is invalid, so zero bases must be handled before taking logarithms.

A second case is an exponent of zero. For example,

```
1
7 0 3 5
```

gives (7^0=1) and (3^5=243), so the answer is `Congrats`. A careless implementation might treat exponent zero as making the whole expression zero, but for every positive base, (B^0=1).

A third case is a base of one. For example,

```
1
1 1000000 2 1
```

compares (1) with (2), so the answer is `Congrats`. Since (\log 1=0), the logarithmic expression correctly becomes zero, but code that assumes every base contributes a positive logarithm can mishandle it.

Finally, exact equality must be recognized. For example,

```
1
2 4 4 2
```

gives (2^4=16) and (4^2=16), so the answer is `Lazy`. The two input pairs are different even though their powers are equal, so comparing bases and exponents directly is not sufficient.

## Approaches

The most direct approach is to calculate both powers and compare the resulting integers. If we construct a power by repeated multiplication, (B^P) requires (P) multiplications. With (P=10^6), one test case can require (2\cdot10^6) such multiplications before the comparison even happens. Worse, the integers become hundreds of thousands of digits long, so the cost of each multiplication grows as the number becomes larger. This is unnecessary when all we need is the ordering of the two values.

The brute-force method works because integer arithmetic preserves the exact ordering of the two salaries. The problem is that the values themselves are much larger than the input numbers. The key observation is that logarithm is strictly increasing on positive numbers. For positive (B),

[
\log(B^P)=P\log B.
]

Consequently,

[
B_1^{P_1} < B_2^{P_2}
]

exactly when

[
P_1\log B_1 < P_2\log B_2.
]

The original powers never have to be constructed. Each test case becomes two logarithm evaluations, two multiplications, and one comparison.

The zero-base cases have to be separated first because (\log 0) does not exist. Under the given guarantee, a base of zero always has a positive exponent, so its value is exactly zero. If both bases are zero, both salaries are zero. If only one base is zero, the corresponding salary is zero, while the other salary is positive because its pair cannot be ((0,0)). Thus the zero cases can be resolved using ordinary integer comparisons before entering the logarithmic calculation.

For positive bases, the computed logarithmic values can differ from the mathematical values by tiny floating-point errors. A small tolerance around equality is enough for this problem, and is also useful for identities such as (2^4=4^2), where the two mathematically equal expressions are evaluated through separate calls to `log`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(P_1+P_2)) multiplications, with large-integer costs | (O(P_1+P_2)) bits for the constructed values | Too slow / unnecessarily expensive |
| Optimal | (O(1)) arithmetic operations per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (B_1,P_1,B_2,P_2). We only need the two bases and exponents for this test case, so no array or other data structure is necessary.
2. If either base is zero, handle this case directly. A zero base has a positive exponent because ((0,0)) is forbidden, so its salary is zero. If both bases are zero, both salaries are zero and the answer is `Lazy`. Otherwise, the salary with the zero base is smaller, so determine whether the new salary is zero and print the corresponding result.
3. If both bases are positive, compute

[
L_1=P_1\log(B_1),\qquad L_2=P_2\log(B_2).
]

These are the logarithms of the two salaries, so comparing (L_1) and (L_2) is equivalent to comparing the original salaries.
4. If (|L_1-L_2|) is within a small tolerance, print `Lazy`. This handles mathematical equalities despite tiny floating-point rounding differences.
5. Otherwise, if (L_2>L_1), the new salary is larger, so print `Congrats`. If (L_2<L_1), print `HaHa`.

### Why it works

For positive bases, the logarithm function is strictly increasing, so it preserves the ordering of the salaries. Since

[
\log(B^P)=P\log B,
]

the algorithm compares exactly the logarithms of the two salaries instead of constructing the salaries themselves. Zero bases are handled separately because their values are known exactly to be zero. Thus every possible valid input is reduced either to an exact zero comparison or to an equivalent comparison of logarithms.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        b1, p1, b2, p2 = map(int, input().split())

        if b1 == 0 or b2 == 0:
            if b1 == 0 and b2 == 0:
                ans.append("Lazy")
            elif b1 == 0:
                ans.append("Congrats")
            else:
                ans.append("HaHa")
            continue

        x = p1 * math.log(b1)
        y = p2 * math.log(b2)

        if abs(x - y) <= 1e-7:
            ans.append("Lazy")
        elif x < y:
            ans.append("Congrats")
        else:
            ans.append("HaHa")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input loop processes each test case independently and stores only the resulting strings. This keeps the algorithm constant-space apart from the output buffer.

The zero-base branch appears before `math.log`, which is necessary because `math.log(0)` raises an error. The problem guarantees that a pair cannot be `(0, 0)`, so whenever a single base is zero its exponent is positive and the corresponding power is genuinely zero.

For positive bases, `p1 * math.log(b1)` represents (\log(B_1^{P_1})), and similarly for the second salary. Python integers have arbitrary precision, so the multiplication by the exponent itself cannot overflow. The logarithm is the only floating-point operation.

The `1e-7` tolerance is deliberately applied to the difference between the logarithms rather than to the salaries themselves. The salaries can be astronomically large, making an absolute tolerance on the original values meaningless. At the logarithmic scale, the relevant quantities are bounded by roughly (10^6\log(10^6)), so this tolerance is tiny compared with the scale of a genuinely different comparison.

## Worked Examples

The first sample contains three different relationships.

| (B_1) | (P_1) | (B_2) | (P_2) | First salary | New salary | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | 4 | 2 | (2^3=8) | (4^2=16) | `Congrats` |
| 2 | 2 | 3 | 1 | (2^2=4) | (3^1=3) | `HaHa` |
| 2 | 4 | 4 | 2 | (2^4=16) | (4^2=16) | `Lazy` |

For the first row, the logarithmic values are (3\log2) and (2\log4). Since (\log4=2\log2), these become approximately (2.0794) and (2.7726), so the second salary is larger. The second row gives approximately (1.3863) and (1.0986), so the new salary is smaller. In the last row, both logarithmic values represent (\log16), so their difference is within the equality tolerance.

A second example exercises zero bases and exponent zero.

```
4
0 7 5 0
3 0 2 1
1 100 1 1
2 10 4 5
```

| (B_1) | (P_1) | (B_2) | (P_2) | First salary | New salary | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 7 | 5 | 0 | (0) | (1) | `Congrats` |
| 3 | 0 | 2 | 1 | (1) | (2) | `Congrats` |
| 1 | 100 | 1 | 1 | (1) | (1) | `Lazy` |
| 2 | 10 | 4 | 5 | (1024) | (1024) | `Lazy` |

The first row never calls `log(0)`, because the zero-base branch immediately recognizes the first salary as zero. The second row confirms that a positive base raised to exponent zero produces one. The third row shows that a base of one remains one regardless of the exponent. The final row is another equality of different power representations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case performs a constant number of arithmetic and logarithm operations. |
| Space | (O(T)) for the output buffer, (O(1)) auxiliary space | The computation itself uses only a constant number of variables. |

The exponent and base can each be as large as (10^6), but the optimal algorithm never iterates up to either value and never constructs the corresponding huge powers. Its running time depends only on the number of test cases, so it comfortably avoids the large-integer work of direct exponentiation. The memory used by the calculation is constant, and even storing the output for all test cases requires only linear space in the amount of text printed.

## Test Cases

```python
import sys
import io
import math

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    t = int(sys.stdin.readline())
    ans = []

    for _ in range(t):
        b1, p1, b2, p2 = map(int, sys.stdin.readline().split())

        if b1 == 0 or b2 == 0:
            if b1 == 0 and b2 == 0:
                ans.append("Lazy")
            elif b1 == 0:
                ans.append("Congrats")
            else:
                ans.append("HaHa")
            continue

        x = p1 * math.log(b1)
        y = p2 * math.log(b2)

        if abs(x - y) <= 1e-7:
            ans.append("Lazy")
        elif x < y:
            ans.append("Congrats")
        else:
            ans.append("HaHa")

    sys.stdin = old_stdin
    return "\n".join(ans)

# Provided sample
assert solve_io(
    """3
2 3 4 2
2 2 3 1
2 4 4 2
"""
) == """Congrats
HaHa
Lazy""", "sample 1"

# Zero base versus a positive salary, and exponent zero
assert solve_io(
    """2
0 7 5 0
3 0 2 1
"""
) == """Congrats
Congrats""", "zero base and zero exponent"

# Both salaries are zero
assert solve_io(
    """1
0 5 0 8
"""
) == "Lazy", "both zero-base powers"

# Maximum-size values
assert solve_io(
    """2
1000000 1000000 999999 1000000
1000000 999999 1000000 1000000
"""
) == """Congrats
HaHa""", "maximum boundary values"

# Equality with different representations and base one
assert solve_io(
    """3
2 20 4 10
1 1000000 1 1
10 1 2 0
"""
) == """Lazy
Lazy
Congrats""", "equality and exponent-zero cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 7 5 0` | `Congrats` | A zero base produces zero, while a positive base with exponent zero produces one. |
| `0 5 0 8` | `Lazy` | Both powers are zero when both bases are zero and exponents are positive. |
| `1000000 1000000 999999 1000000` | `Congrats` | Large boundary values without constructing enormous powers. |
| `1000000 999999 1000000 1000000` | `HaHa` | A one-step exponent difference at the maximum base. |
| `2 20 4 10` | `Lazy` | Equal powers represented by different bases and exponents. |
| `1 1000000 1 1` | `Lazy` | Base one with very different exponents. |
| `10 1 2 0` | `Congrats` | The boundary case where the second exponent is zero. |

## Edge Cases

When the first base is zero, consider

```
1
0 5 2 3
```

The algorithm enters the zero-base branch immediately. Since only (B_1) is zero, the first salary is (0^5=0), while the second salary is (2^3=8). It prints `Congrats`. No logarithm of zero is evaluated.

When both bases are zero, consider

```
1
0 4 0 9
```

Both exponents are positive because `(0, 0)` is forbidden for each power. The two salaries are therefore (0) and (0). The algorithm sees both zero bases and prints `Lazy`.

When an exponent is zero, consider

```
1
7 0 3 5
```

Both bases are positive, so the logarithmic branch is used. The first logarithmic value is (0\log7=0), representing (\log1), while the second is (5\log3>0). The second salary is larger, so the result is `Congrats`.

When a base is one, consider

```
1
1 1000000 2 1
```

The first logarithmic value is (10^6\log1=0), while the second is (\log2>0). The algorithm prints `Congrats`, correctly reflecting (1^{1000000}=1<2).

For equal powers with different representations, consider

```
1
2 1000000 4 500000
```

Mathematically,

[
2^{1000000}=(2^2)^{500000}=4^{500000}.
]

The algorithm computes (1000000\log2) and (500000\log4). These represent the same mathematical logarithm, and their floating-point difference is within the equality tolerance, so the output is `Lazy`.

The final edge case is a comparison where the values are extremely large but clearly different. For example,

```
1
1000000 1000000 999999 1000000
```

The algorithm compares (10^6\log(10^6)) with (10^6\log(999999)). Since the first logarithm is larger, it prints `Congrats` without ever constructing either power. This is exactly where the logarithmic transformation provides its main advantage.
