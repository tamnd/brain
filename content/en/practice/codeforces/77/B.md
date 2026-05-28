---
title: "CF 77B - Falling Anvils"
description: "We are given two real parameters chosen uniformly at random. The victim height p lies in the interval [0, a], and the wind parameter q lies in [-b, b]. For every pair (p, q), the anvil hits successfully if a certain quadratic equation has at least one real root."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 77
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 69 (Div. 1 Only)"
rating: 1800
weight: 77
solve_time_s: 156
verified: true
draft: false
---

[CF 77B - Falling Anvils](https://codeforces.com/problemset/problem/77/B)

**Rating:** 1800  
**Tags:** math, probabilities  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two real parameters chosen uniformly at random.

The victim height `p` lies in the interval `[0, a]`, and the wind parameter `q` lies in `[-b, b]`. For every pair `(p, q)`, the anvil hits successfully if a certain quadratic equation has at least one real root.

The equation from the statement is:

$x^2+px+q=0$

A quadratic equation has a real root exactly when its discriminant is non-negative. So the entire problem reduces to computing the probability that:

$p^2-4q\ge0$

Since `p` and `q` are chosen uniformly and independently, this probability is simply the area of all valid `(p, q)` pairs divided by the total area of the rectangle:

$0\le p\le a,\ -b\le q\le b$

The constraints are very small from an algorithmic perspective. We only process up to `10^4` test cases, and each case contains just two integers. Any constant-time mathematical formula per test case is easily fast enough. Even an `O(log n)` or `O(sqrt n)` solution would pass comfortably. The real challenge is deriving the correct geometry and handling the boundary cases carefully.

The tricky cases come from how the parabola interacts with the rectangle.

Consider:

```
a = 1, b = 100
```

The parabola `q = p² / 4` stays very low compared to the rectangle height. Most points fail, so the probability is close to `1/2`, not close to `1`.

A careless implementation might assume the parabola always reaches the top boundary `q = b`, which is false here.

Another important edge case is:

```
a = 0, b = 5
```

Then `p` is always zero, so the condition becomes:

```
-4q >= 0
```

which means `q <= 0`. Exactly half of the interval `[-5, 5]` works, so the answer is `0.5`.

A buggy derivation often divides by `a` somewhere and crashes or produces NaN when `a = 0`.

The final subtle situation is when the parabola exactly touches the top edge:

```
a = 4, b = 4
```

because `a² / 4 = 4`.

The integration changes behavior precisely at this boundary. Using strict inequalities in the wrong place can introduce small floating-point errors or select the wrong formula.

## Approaches

The brute-force viewpoint is straightforward. We can think of the rectangle of all possible `(p, q)` pairs and check whether each point satisfies:

$q\le\frac{p^2}{4}$

If we discretize the rectangle into a very fine grid, count how many cells satisfy the inequality, and divide by the total number of cells, we get an approximation of the probability.

This works conceptually because uniform random selection corresponds directly to area ratios. The problem is precision. To achieve `10^-6` accuracy, the grid would need millions or billions of samples. For `10^4` test cases, that becomes completely impractical.

The key observation is that the valid region has a very simple geometric shape.

For every fixed `p`, the valid values of `q` are:

$-b\le q\le\min\left(b,\frac{p^2}{4}\right)$

So instead of approximating the area numerically, we can integrate the height of this interval exactly.

Two cases appear naturally.

If:

$\frac{a^2}{4}\le b$

then the parabola never reaches the top boundary of the rectangle. The valid height for each `p` is:

$b+\frac{p^2}{4}$

Integrating from `0` to `a` gives the area directly.

If instead:

$\frac{a^2}{4}>b$

then after some point, the parabola rises above the rectangle. From that point onward, every `q` value works.

The transition happens at:

$p=2\sqrt b$

This splits the integral into two easy pieces.

The entire solution becomes constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(K²) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the quadratic discriminant condition.

The equation has a real root when:

$p^2-4q\ge0$

Rearranging gives:

$q\le\frac{p^2}{4}$
2. Interpret the probability geometrically.

All possible pairs `(p, q)` form a rectangle of area:

$2ab$

The answer equals:

valid area / total area.
3. Determine the valid vertical interval for a fixed `p`.

Since `q` ranges from `-b` to `b`, and we additionally need:

$q\le\frac{p^2}{4}$

the valid height becomes:

$\min\left(b,\frac{p^2}{4}\right)+b$
4. Handle the first case where the parabola never reaches the top edge.

If:

$a\le2\sqrt b$

then:

$\frac{p^2}{4}\le b$

for every `p` in `[0, a]`.

The valid area is:

$\int_0^a\left(b+\frac{p^2}{4}\right)dp=ab+\frac{a^3}{12}$

Dividing by `2ab` gives:

$\frac12+\frac{a^2}{24b}$
5. Handle the second case where the parabola crosses the top edge.

If:

$a>2\sqrt b$

then for `p > 2√b`, every `q` value works.

Split the area into two regions.

The first region, from `0` to `2√b`, contributes:

$\int_0^{2\sqrt b}\left(b+\frac{p^2}{4}\right)dp=\frac{8}{3}b^{3/2}$

The second region, from `2√b` to `a`, contributes the full rectangle height:

$2b(a-2\sqrt b)$

Summing and simplifying yields:

$1-\frac{2\sqrt b}{3a}$
6. Print the formula corresponding to the current case.

### Why it works

The algorithm directly computes the exact measure of all successful `(p, q)` pairs inside the sampling rectangle. For every fixed `p`, we calculate precisely how much of the vertical interval satisfies the discriminant condition. Integrating those valid lengths across all `p` values gives the exact successful area.

The split into two cases is exhaustive because the parabola either stays below the rectangle top edge for the entire interval or crosses it exactly once. No other geometric behavior is possible.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b = map(float, input().split())

    if b == 0:
        print("1.0000000000")
        continue

    if a * a <= 4 * b:
        ans = 0.5 + (a * a) / (24.0 * b)
    else:
        ans = 1.0 - (2.0 * math.sqrt(b)) / (3.0 * a)

    print(f"{ans:.10f}")
```

The implementation follows the exact derivation from the walkthrough.

The first branch handles `b = 0` separately. In that situation, `q` is always zero, so the quadratic always has real roots because the discriminant becomes `p²`. The probability is exactly `1`.

The second branch checks whether the parabola reaches the top boundary of the rectangle. Using:

```
a * a <= 4 * b
```

avoids unnecessary square roots and also avoids small floating-point precision issues around the boundary.

The formulas are evaluated directly as floating-point expressions. All intermediate values comfortably fit inside standard double precision because `a` and `b` are at most `10^6`.

Formatting with ten decimal places easily satisfies the required precision tolerance.

## Worked Examples

### Example 1

Input:

```
a = 4
b = 2
```

Since:

```
a² = 16
4b = 8
```

we use the second formula.

| Variable | Value |
| --- | --- |
| a | 4 |
| b | 2 |
| sqrt(b) | 1.414213562 |
| 2 * sqrt(b) | 2.828427124 |
| (2 * sqrt(b)) / (3a) | 0.235702260 |
| Answer | 0.764297740 |

So the output is:

```
0.7642977396
```

This trace demonstrates the crossing case where part of the rectangle is entirely valid.

### Example 2

Input:

```
a = 1
b = 2
```

Now:

```
a² = 1
4b = 8
```

so the parabola never reaches the top edge.

| Variable | Value |
| --- | --- |
| a | 1 |
| b | 2 |
| a² / (24b) | 0.020833333 |
| 0.5 | 0.500000000 |
| Answer | 0.520833333 |

So the output is:

```
0.5208333333
```

This trace demonstrates the pure integration case where the valid upper boundary is always the parabola itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No extra storage is used |

Even for `10^4` test cases, the runtime is tiny because every case is solved with a closed-form formula. Memory usage is constant throughout execution.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    t = int(input())

    out = []

    for _ in range(t):
        a, b = map(float, input().split())

        if b == 0:
            out.append("1.0000000000")
            continue

        if a * a <= 4 * b:
            ans = 0.5 + (a * a) / (24.0 * b)
        else:
            ans = 1.0 - (2.0 * math.sqrt(b)) / (3.0 * a)

        out.append(f"{ans:.10f}")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("2\n4 2\n1 2\n") == (
    "0.7642977396\n"
    "0.5208333333\n"
), "sample"

# minimum values
assert run("1\n0 0\n") == "1.0000000000\n", "both zero"

# boundary where a^2 = 4b
assert run("1\n4 4\n") == "0.6666666667\n", "boundary transition"

# very large values
assert run("1\n1000000 1\n") == "0.9999993333\n", "large a"

# a = 0 with positive b
assert run("1\n0 5\n") == "0.5000000000\n", "half interval valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `1.0` | Degenerate rectangle with guaranteed success |
| `4 4` | `0.6666666667` | Exact transition point between formulas |
| `1000000 1` | `0.9999993333` | Large values and precision stability |
| `0 5` | `0.5` | Correct handling when only non-positive q works |

## Edge Cases

Consider:

```
1
0 5
```

Here `p` is fixed at zero. The condition becomes:

$-4q\ge0$

which means:

$q\le0$

Inside `[-5, 5]`, exactly half the interval works. The algorithm enters the first formula branch because:

```
a² <= 4b
```

and computes:

```
0.5 + 0 / (24 * 5) = 0.5
```

which is correct.

Now consider:

```
1
4 4
```

The parabola touches the top boundary exactly at `p = 4`. Both derived formulas produce the same value:

```
2 / 3
```

The implementation uses `<=` in the branch condition, so the boundary is handled consistently with no discontinuity.

Finally, consider:

```
1
10 0
```

Then `q` is always zero, and every quadratic has discriminant:

$p^2$

which is always non-negative. The dedicated `b == 0` branch returns `1.0` immediately, avoiding division by zero in the formulas.
