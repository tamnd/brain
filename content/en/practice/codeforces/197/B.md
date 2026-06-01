---
title: "CF 197B - Limit"
description: "We are given two polynomials, $P(x)$ and $Q(x)$, written in descending powers of $x$. The task is to compute: $$lim{x to infty} frac{P(x)}{Q(x)}$$ The input gives the degrees of the two polynomials and all coefficients from the highest-degree term down to the constant term."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 197
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 124 (Div. 2)"
rating: 1400
weight: 197
solve_time_s: 93
verified: true
draft: false
---

[CF 197B - Limit](https://codeforces.com/problemset/problem/197/B)

**Rating:** 1400  
**Tags:** math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two polynomials, $P(x)$ and $Q(x)$, written in descending powers of $x$. The task is to compute:

$$\lim_{x \to \infty} \frac{P(x)}{Q(x)}$$

The input gives the degrees of the two polynomials and all coefficients from the highest-degree term down to the constant term.

The key observation is that when $x$ becomes extremely large, the highest-degree terms dominate everything else. Lower powers become insignificant compared to the leading term.

For example:

$$\frac{3x^5 + 2x + 1}{7x^5 - 9}$$

behaves almost exactly like:

$$\frac{3x^5}{7x^5} = \frac{3}{7}$$

for very large $x$.

The constraints are tiny, degrees are at most 100, so performance is not really the challenge here. Even evaluating the polynomials numerically would fit comfortably inside the limits. The real challenge is mathematical correctness. Floating point evaluation would introduce precision issues and can even produce completely wrong answers for large inputs.

Several edge cases are easy to mishandle.

Consider:

```
2 1
1 1 1
2 5
```

This is:

$$\frac{x^2 + x + 1}{2x + 5}$$

The numerator has larger degree, so the ratio grows without bound. Since both leading coefficients are positive, the answer is:

```
Infinity
```

A careless implementation that evaluates at some large finite value might still produce a finite number.

Now consider:

```
2 1
-1 0 0
2 1
```

This is:

$$\frac{-x^2}{2x+1}$$

The numerator still dominates, but the leading coefficient is negative. The limit becomes:

```
-Infinity
```

The sign matters whenever the numerator degree is larger.

Another important case happens when the denominator has larger degree:

```
1 2
5 1
1 0 0
```

This is:

$$\frac{5x+1}{x^2}$$

As $x \to \infty$, the denominator grows faster, so the result approaches zero:

```
0/1
```

Finally, when both degrees are equal, we must reduce the fraction correctly:

```
1 1
6 0
8 1
```

The limit is:

$$\frac{6x}{8x} = \frac{6}{8} = \frac{3}{4}$$

Printing `6/8` would be wrong because the problem requires an irreducible fraction.

## Approaches

A brute-force approach would directly evaluate both polynomials for a very large value such as $x = 10^9$, then divide the results and try to infer the limit.

This works in many ordinary cases because dominant terms overwhelm smaller ones. For equal degrees, the ratio approaches the ratio of leading coefficients. For different degrees, the magnitude becomes extremely large or extremely small.

The problem is reliability. Large powers overflow quickly in many languages, and floating point arithmetic loses precision. Even Python's arbitrary-size integers would produce astronomically large values unnecessarily. More importantly, numerical approximation is fundamentally the wrong tool here because the answer is exact and purely determined by polynomial degrees and leading coefficients.

The structure of polynomial growth gives a much cleaner solution.

Suppose:

$$P(x)=a_0x^n+\dots$$

and

$$Q(x)=b_0x^m+\dots$$

As $x \to \infty$:

$$\frac{P(x)}{Q(x)} \sim \frac{a_0x^n}{b_0x^m} = \frac{a_0}{b_0}x^{n-m}$$

Now everything depends only on $n-m$.

If $n>m$, the factor $x^{n-m}$ grows infinitely large. The sign comes from $\frac{a_0}{b_0}$.

If $n<m$, the factor tends to zero.

If $n=m$, the powers cancel completely and only the ratio of leading coefficients remains.

This reduces the entire problem to a few comparisons and one gcd computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force polynomial evaluation | O(n + m) | O(1) | Numerically unsafe |
| Optimal mathematical observation | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the degrees $n$ and $m$.
2. Read the coefficient arrays for both polynomials.
3. Extract the leading coefficients.

Since coefficients are given from highest degree to lowest degree, the leading coefficients are simply:

$$a_0 = A[0], \quad b_0 = B[0]$$
4. Compare the degrees $n$ and $m$.
5. If $n > m$, the numerator grows faster than the denominator.

The limit becomes either positive or negative infinity depending on the sign of:

$$a_0 \times b_0$$

If the product is positive, print `"Infinity"`.

Otherwise print `"-Infinity"`.
6. If $n < m$, the denominator grows faster.

The limit approaches zero, so print:

```
0/1
```
7. If $n = m$, compute the reduced fraction:

$$\frac{a_0}{b_0}$$

Compute:

$$g = \gcd(|a_0|, |b_0|)$$

Divide both numbers by $g$.
8. Ensure the denominator is positive.

If the denominator is negative, multiply both numerator and denominator by $-1$.
9. Print the fraction in the format:

```
p/q
```

### Why it works

For very large $x$, lower-degree polynomial terms become negligible compared to the leading term. The quotient:

$$\frac{P(x)}{Q(x)}$$

has the same asymptotic behavior as:

$$\frac{a_0x^n}{b_0x^m} = \frac{a_0}{b_0}x^{n-m}$$

The exponent $n-m$ completely determines whether the expression grows infinitely, shrinks to zero, or stabilizes at a constant value. Since every step of the algorithm follows directly from this asymptotic form, the produced answer is mathematically exact.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

n, m = map(int, input().split())

A = list(map(int, input().split()))
B = list(map(int, input().split()))

a0 = A[0]
b0 = B[0]

if n > m:
    if a0 * b0 > 0:
        print("Infinity")
    else:
        print("-Infinity")

elif n < m:
    print("0/1")

else:
    g = gcd(abs(a0), abs(b0))

    p = a0 // g
    q = b0 // g

    if q < 0:
        p *= -1
        q *= -1

    print(f"{p}/{q}")
```

The first part reads the degrees and coefficient arrays. Since the input order already starts with the highest-degree coefficient, the leading coefficients are immediately available at index `0`.

The degree comparison drives the entire solution. When the numerator degree is larger, only the sign matters. Multiplying the leading coefficients gives the sign of the limit.

The equal-degree branch is the only place where arithmetic beyond comparisons is required. We reduce the fraction using `gcd`, then normalize the sign so the denominator remains positive, exactly as required by the statement.

One subtle point is using absolute values inside `gcd`. Python's `math.gcd` handles negatives safely, but taking absolute values keeps the intent explicit and avoids portability issues across languages.

Another subtle detail is denominator normalization. A result like `1/-2` is mathematically correct but violates the required output format because the denominator must be positive.

## Worked Examples

### Example 1

Input:

```
2 1
1 1 1
2 5
```

This represents:

$$\frac{x^2+x+1}{2x+5}$$

| Variable | Value |
| --- | --- |
| n | 2 |
| m | 1 |
| a0 | 1 |
| b0 | 2 |
| Degree comparison | n > m |
| Sign of a0 × b0 | Positive |

Output:

```
Infinity
```

The numerator grows like $x^2$, while the denominator grows like $x$. Since $x^2$ dominates $x$, the ratio grows without bound.

### Example 2

Input:

```
1 1
6 0
8 1
```

This represents:

$$\frac{6x}{8x+1}$$

| Variable | Value |
| --- | --- |
| n | 1 |
| m | 1 |
| a0 | 6 |
| b0 | 8 |
| gcd(6, 8) | 2 |
| Reduced numerator | 3 |
| Reduced denominator | 4 |

Output:

```
3/4
```

Both polynomials grow at the same rate because their degrees match. The limit equals the ratio of leading coefficients.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Reading the input arrays dominates the runtime |
| Space | O(1) | Only a few variables besides the input arrays are used |

The constraints are extremely small, so this solution runs instantly. Even for the maximum degree of 100, the work is trivial compared to the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    a0 = A[0]
    b0 = B[0]

    if n > m:
        if a0 * b0 > 0:
            print("Infinity")
        else:
            print("-Infinity")

    elif n < m:
        print("0/1")

    else:
        g = gcd(abs(a0), abs(b0))

        p = a0 // g
        q = b0 // g

        if q < 0:
            p *= -1
            q *= -1

        print(f"{p}/{q}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run(
"""2 1
1 1 1
2 5
"""
) == "Infinity", "sample 1"

# equal degrees, reducible fraction
assert run(
"""1 1
6 0
8 1
"""
) == "3/4", "fraction reduction"

# denominator degree larger
assert run(
"""1 2
5 1
1 0 0
"""
) == "0/1", "approaches zero"

# negative infinity
assert run(
"""2 1
-1 0 0
2 1
"""
) == "-Infinity", "negative sign handling"

# minimum size polynomials
assert run(
"""0 0
5
-10
"""
) == "-1/2", "constant polynomials"

# denominator normalization
assert run(
"""1 1
1 0
-2 3
"""
) == "-1/2", "positive denominator requirement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Equal degrees with reducible coefficients | 3/4 | Proper gcd reduction |
| Numerator degree smaller | 0/1 | Correct zero handling |
| Negative leading sign | -Infinity | Infinity sign correctness |
| Degree 0 polynomials | -1/2 | Smallest valid input |
| Negative denominator | -1/2 | Denominator normalization |

## Edge Cases

Consider:

```
2 1
-1 0 0
2 1
```

The leading terms are:

$$\frac{-x^2}{2x} = -\frac{x}{2}$$

The algorithm compares degrees and finds $2 > 1$. It then checks the sign of:

$$(-1) \times 2 = -2$$

Since the sign is negative, it prints:

```
-Infinity
```

This correctly captures the direction of divergence.

Now consider:

```
1 2
5 1
1 0 0
```

The dominant behavior is:

$$\frac{5x}{x^2} = \frac{5}{x}$$

As $x$ grows, the value shrinks toward zero.

The algorithm sees $1 < 2$ and immediately prints:

```
0/1
```

No fraction reduction is needed because the exact limit is zero.

Finally, consider denominator sign normalization:

```
1 1
1 0
-2 3
```

The raw leading coefficient ratio is:

$$\frac{1}{-2}$$

The gcd is $1$, so the unreduced fraction remains `1/-2`.

The algorithm detects the negative denominator and flips both signs:

$$\frac{1}{-2} = \frac{-1}{2}$$

It prints:

```
-1/2
```

which satisfies the required output format.
