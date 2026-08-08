---
title: "CF 102436A - Cool Water"
description: "We have a water cooler with two buttons. Pressing the red button gives exactly a milliliters of water at 100°C, while pressing the blue button gives exactly b milliliters at 0°C."
date: "2026-08-08T15:59:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102436
codeforces_index: "A"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 1"
rating: 0
weight: 102436
solve_time_s: 123
verified: true
draft: false
---

[CF 102436A - Cool Water](https://codeforces.com/problemset/problem/102436/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a water cooler with two buttons. Pressing the red button gives exactly `a` milliliters of water at `100°C`, while pressing the blue button gives exactly `b` milliliters at `0°C`. Tintin wants to collect water at exactly `x°C` in a 1000 milliliter bottle, without throwing any water away. The task is to find the largest amount of correctly tempered water that can fit in the bottle.

Suppose Tintin presses the red button `i` times and the blue button `j` times. The hot-water volume is `a * i`, the cold-water volume is `b * j`, and the total volume is `a * i + b * j`. The resulting temperature is

[
\frac{100ai}{ai+bj}.
]

For an intermediate temperature, this equation imposes an exact ratio between the amount of hot and cold water. The whole problem is consequently an integer divisibility problem rather than a simulation problem.

The constraints are tiny, with `a` and `b` at most 1000 and `x` between 0 and 100. The bottle capacity is fixed at 1000 milliliters, so even a direct search over possible button presses is feasible in principle, but the intended solution is much simpler and runs in constant time. The original problem has a 1 second time limit and 512 MB memory limit.

There are several boundary cases that can make a careless implementation fail. If `x = 0`, only cold water can be used. For example, with

```
10
20
0
```

the answer is `1000`, because fifty presses of the blue button produce exactly 1000 milliliters. A formula that blindly divides by `x` would fail here.

Similarly, if `x = 100`, only hot water can be used. For

```
300
200
100
```

the answer is `900`, because three red-button presses give 900 milliliters. The general ratio formula must therefore handle a zero coefficient correctly.

An intermediate temperature can also be impossible to obtain at all. For

```
100
101
10
```

the answer is `0`. The required ratio between hot and cold water cannot be formed from these two fixed button volumes, so pretending that some fractional number of button presses is possible would produce an invalid positive answer.

Finally, obtaining one valid mixture does not mean we should stop there. If the smallest valid mixture has volume `250`, for example, we can make `250`, `500`, `750`, or `1000` milliliters using repeated copies of that same mixture. The answer is the largest such multiple that does not exceed the bottle capacity.

## Approaches

A straightforward brute-force approach is to try every possible number of red-button and blue-button presses, compute the resulting temperature, and remember the largest valid volume. Since the bottle holds only 1000 milliliters, there are only bounded numbers of useful presses. One implementation can inspect every pair `(i, j)` with `1 <= i, j <= 1000`, giving up to one million candidate pairs. For every pair we evaluate

[
\frac{100ai}{ai+bj}
]

and check whether it equals `x`.

This works because every candidate pair is tested directly, so any feasible mixture will eventually be found. The problem is that the search is doing far more work than the structure requires. It also encourages floating-point comparisons, which are unnecessary and potentially dangerous when an exact integer equality is available.

The key observation is that the target temperature determines the ratio of hot water to cold water. Let the hot volume be `H` and the cold volume be `C`. For `0 < x < 100`,

[
\frac{100H}{H+C}=x.
]

Multiplying through gives

[
(100-x)H=xC.
]

Since `H = ai` and `C = bj`, we obtain

[
a(100-x)i = bxj.
]

Now the problem has become a standard equation of the form `A*i = B*j`. Let

[
A=a(100-x), \qquad B=bx.
]

If `g = gcd(A, B)`, the smallest positive solution is

[
i=\frac{B}{g}, \qquad j=\frac{A}{g}.
]

The corresponding smallest valid amount of water is

[
M=a\frac{B}{g}+b\frac{A}{g}
=\frac{100ab}{g}.
]

Every other valid solution is just an integer multiple of this smallest one. So once `M` is known, the largest amount that fits in the 1000 milliliter bottle is simply

[
\left\lfloor\frac{1000}{M}\right\rfloor M.
]

Interestingly, the same formula also handles `x = 0` and `x = 100`. For `x = 0`, the gcd becomes `gcd(0, 100a) = 100a`, giving `M = b`. For `x = 100`, it gives `M = a`. Thus no special cases are required in the implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^6) | O(1) | Accepted in principle, unnecessarily large |
| Optimal | O(log(max(a, b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a`, `b`, and `x`. Define `A = a * (100 - x)` and `B = b * x`. These are the two coefficients in the exact equation `A * i = B * j`.
2. Compute `g = gcd(A, B)`. Dividing both coefficients by their gcd gives the smallest integer ratio that can satisfy the temperature equation.
3. Compute the smallest valid mixture volume as

[
M=\frac{100ab}{g}.
]

The cancellation here follows directly from the smallest solution `i = B/g`, `j = A/g`. Their total water volume is exactly `100ab/g`.
4. Compute

[
\left\lfloor\frac{1000}{M}\right\rfloor M.
]

Every feasible mixture has volume equal to `kM` for some positive integer `k`, so this is exactly the largest feasible amount that fits in the bottle.
5. Print that amount. If `M > 1000`, the quotient is zero, correctly indicating that no valid mixture can be poured into the bottle.

The key invariant is that `M` is the smallest positive volume whose hot and cold components have exactly the required temperature ratio. Because every integer solution of `A*i = B*j` is a multiple of the reduced solution, every feasible total volume is a multiple of `M`. The final floor operation consequently considers every possible feasible volume and selects the largest one below the bottle capacity.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

a = int(input())
b = int(input())
x = int(input())

g = gcd(a * (100 - x), b * x)
minimum = 100 * a * b // g

answer = (1000 // minimum) * minimum
print(answer)
```

The two expressions `a * (100 - x)` and `b * x` come directly from rearranging the temperature equation. Keeping the computation entirely integral avoids floating-point precision issues.

`math.gcd` also handles zero correctly. When `x = 0`, the second argument is zero, and when `x = 100`, the first argument is zero. This is why the implementation does not need separate branches for the two extreme temperatures.

The expression `100 * a * b // g` calculates the smallest valid total volume. Python integers do not overflow, and the largest intermediate value is tiny anyway, since `a` and `b` are at most 1000.

Finally, `1000 // minimum` gives the number of complete copies of the smallest mixture that fit in the bottle. Multiplying back by `minimum` gives the actual volume rather than merely the number of copies.

## Worked Examples

For the first sample,

```
10
20
30
```

we have `a = 10`, `b = 20`, and `x = 30`.

| Step | `A = a(100-x)` | `B = bx` | `gcd(A,B)` | Minimum volume | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | 700 | 600 | 100 | 300 | 900 |
| Final | 700 | 600 | 100 | 300 | 900 |

The formula gives a smallest valid mixture of 300 milliliters. Three such mixtures fill the bottle with 900 milliliters, but the sample answer is actually 1000 milliliters. This exposes an issue with interpreting the buttons as independent fixed-volume pours when the target equation is reduced incorrectly: the actual primitive press counts are `i = 6`, `j = 7`, producing `60 + 140 = 200` milliliters at 30°C, so the smallest mixture is 200 milliliters. Recomputing the algebra gives

[
A=10\cdot70=700,\quad B=20\cdot30=600,\quad g=100,
]

and

[
i=B/g=6,\quad j=A/g=7.
]

The total is `10*6 + 20*7 = 200`, not 300. The correct closed form is consequently obtained by simplifying the total as

# \frac{abx+ab(100-x)}{g}

\frac{100ab}{g}.
]

Here that is `100*10*20/100 = 200`, giving `5 * 200 = 1000`.

For the third sample,

```
15
25
40
```

the coefficients are `A = 15 * 60 = 900` and `B = 25 * 40 = 1000`.

| Step | `A` | `B` | `gcd(A,B)` | `i = B/g` | `j = A/g` | Minimum volume | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 900 | 1000 | 100 | 10 | 9 | 375 | 750 |

The smallest valid mixture uses 10 red presses and 9 blue presses, giving `150 + 225 = 375` milliliters at exactly 40°C. Two copies fit in the bottle, giving 750 milliliters. A third copy would require 1125 milliliters, so 750 is maximal. This matches the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(max(a, b))) | The only non-constant operation is computing a gcd. |
| Space | O(1) | Only a fixed number of integer variables are stored. |

The constraints are far smaller than what this complexity can handle. The solution performs one gcd computation and a handful of integer arithmetic operations, so it is comfortably within the 1 second time limit and uses negligible memory compared with the 512 MB limit.

## Test Cases

```python
import sys
import io
from math import gcd

def solve():
    input = sys.stdin.readline

    a = int(input())
    b = int(input())
    x = int(input())

    g = gcd(a * (100 - x), b * x)
    minimum = 100 * a * b // g

    print((1000 // minimum) * minimum)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("10\n20\n30\n") == "1000\n", "sample 1"
assert run("100\n101\n10\n") == "0\n", "sample 2"
assert run("15\n25\n40\n") == "750\n", "sample 3"

# Minimum-size values
assert run("1\n1\n0\n") == "1000\n", "minimum values, 0 degrees"
assert run("1\n1\n100\n") == "1000\n", "minimum values, 100 degrees"

# All-equal button volumes
assert run("10\n10\n50\n") == "1000\n", "equal volumes and midpoint temperature"

# Boundary temperature with a volume that does not divide 1000
assert run("333\n7\n100\n") == "999\n", "hot-only boundary"

# No possible intermediate mixture
assert run("1000\n999\n1\n") == "0\n", "small target temperature impossible"

# Large valid mixture with exact bottle fill
assert run("1000\n1000\n50\n") == "1000\n", "maximum button volumes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0` | `1000` | Minimum values and the `x = 0` boundary |
| `1 / 1 / 100` | `1000` | The `x = 100` boundary |
| `10 / 10 / 50` | `1000` | Equal hot and cold button volumes |
| `333 / 7 / 100` | `999` | Maximum whole number of hot-only pours |
| `1000 / 999 / 1` | `0` | A valid temperature ratio that cannot be formed |
| `1000 / 1000 / 50` | `1000` | Large button volumes and exact bottle capacity |

## Edge Cases

When `x = 0`, the required water must contain no hot component. For

```
10
20
0
```

we get `A = 1000` and `B = 0`, so `gcd(A, B) = 1000`. The minimum valid volume is `100 * 10 * 20 / 1000 = 20`. The bottle can contain `50` such portions, giving `1000`. The algorithm naturally reduces to using only blue-button water.

When `x = 100`, the symmetric situation occurs. For

```
333
7
100
```

we get `A = 0` and `B = 700`. The gcd is `700`, so the minimum valid volume is `333`. Three red-button pours give `999`, while a fourth would exceed the bottle. The output is therefore `999`.

When no positive intermediate mixture exists, the minimum valid volume can exceed the bottle capacity. For

```
1000
999
1
```

we have `A = 99000` and `B = 999`, whose gcd is `9`. The smallest valid mixture has volume

[
\frac{100\cdot1000\cdot999}{9}=1{,}110{,}000,
]

far above 1000. Thus `1000 // minimum` is zero, and the algorithm correctly prints `0`.

The all-equal case is useful because it tests the simplest possible ratio. With

```
10
10
50
```

the required temperature is exactly the midpoint, so equal quantities of hot and cold water are required. One red and one blue press produce 20 milliliters at 50°C, and 50 copies fill the bottle exactly. The gcd reduction finds this primitive mixture directly.

The main off-by-one trap is the bottle boundary. We need the largest multiple of the smallest valid mixture that is at most 1000, not the smallest multiple strictly below 1000. The expression `(1000 // minimum) * minimum` handles an exact fit correctly. If `minimum = 250`, for example, it returns 1000 rather than 750.
