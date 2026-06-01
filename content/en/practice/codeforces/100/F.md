---
title: "CF 100F - Polynom"
description: "We are given a polynomial already factorized into linear terms: $$p(x) = (x + a1)(x + a2)dots(x + an)$$ The task is to expand this product and print the polynomial in the usual descending-power form: $$x^n + b1x^{n-1} + dots + bn$$ The tricky part is not the expansion itself."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "F"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1800
weight: 100
solve_time_s: 146
verified: true
draft: false
---

[CF 100F - Polynom](https://codeforces.com/problemset/problem/100/F)

**Rating:** 1800  
**Tags:** *special, implementation  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a polynomial already factorized into linear terms:

$$p(x) = (x + a_1)(x + a_2)\dots(x + a_n)$$

The task is to expand this product and print the polynomial in the usual descending-power form:

$$x^n + b_1x^{n-1} + \dots + b_n$$

The tricky part is not the expansion itself. The tricky part is formatting the result exactly as required.

Every term must appear in the form `C*X^K`, but shortened whenever possible. Coefficient `1` before non-constant terms must disappear, exponent `1` must be printed as just `X`, exponent `0` must omit `X` completely, and terms with coefficient `0` must not appear at all. Signs must also be printed compactly without extra spaces.

The degree is at most 9, which is extremely small. Even algorithms with exponential behavior would probably survive here, but there is no reason to use them. A straightforward polynomial multiplication approach runs in a few hundred operations.

The formatting rules are where most wrong answers happen. The polynomial itself is easy to compute.

One subtle edge case appears when intermediate coefficients become zero. For example:

```
2
-1
1
```

The polynomial is:

$$(x-1)(x+1)=x^2-1$$

The `x` term disappears completely. A careless implementation might print `X^2+0*X-1`, which is invalid.

Another dangerous case is coefficients equal to `1` or `-1`. Consider:

```
1
1
```

The polynomial is:

$$x+1$$

The correct output is:

```
X+1
```

Printing `1*X+1` is too verbose and rejected.

Exponent formatting also matters. For example:

```
2
0
0
```

gives:

$$x^2$$

The output must be:

```
X^2
```

not `X^2+0*X+0`.

Constant polynomials need special handling too. For example:

```
1
-3
```

produces:

$$x-3$$

The constant term has no `X`, while the linear term has no exponent.

## Approaches

The most direct brute-force idea is to literally multiply the factors one by one while storing every coefficient explicitly.

Suppose we currently know the coefficients of:

$$(x+a_1)(x+a_2)\dots(x+a_k)$$

Then multiplying by `(x + a_{k+1})` creates the next polynomial. Each old coefficient contributes to two new coefficients, one shifted by degree because of multiplication by `x`, and one unchanged because of multiplication by `a_{k+1}`.

This works because polynomial multiplication distributes naturally across terms.

A truly naive brute-force solution would enumerate every subset of factors contributing to every degree. Since the coefficient of $x^{n-k}$ is the sum of all products of `k` chosen `a_i`, that approach needs checking all subsets. With `n ≤ 9`, even $2^9 = 512$ subsets are acceptable, but the implementation becomes unnecessarily complicated.

The incremental multiplication approach is cleaner and scales much better conceptually. Each multiplication touches only the current polynomial degree, so the complexity becomes quadratic.

The key observation is that multiplying by a linear polynomial only changes neighboring coefficients. If:

$$P(x)=c_0+c_1x+\dots+c_dx^d$$

then:

$$P(x)(x+a)= ac_0+(c_0+ac_1)x+\dots+c_dx^{d+1}$$

This local transition makes dynamic polynomial construction natural.

After computing coefficients, the remaining challenge is deterministic formatting. Since the statement guarantees a unique valid output, we must exactly follow the shortest representation rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Subset Enumeration | O(2^n \cdot n) | O(2^n) | Accepted |
| Incremental Polynomial Multiplication | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all values `a_i`.
2. Start with the constant polynomial `1`.

We store coefficients in increasing degree order. Initially:

$$p(x)=1$$

so the coefficient array is:

```
[1]
```
3. For every factor `(x + a)` create a new coefficient array one degree larger.

If the current coefficient of $x^i$ is `c`, then:

Multiplying by `a` contributes `c * a` to degree `i`.

Multiplying by `x` contributes `c` to degree `i+1`.
4. Replace the old polynomial with the new one after processing each factor.

After all factors are processed, the array contains every coefficient of the expanded polynomial.
5. Traverse coefficients from highest degree to lowest degree and build the answer string.
6. Skip coefficients equal to zero.

Terms with coefficient `0` must not appear at all.
7. Handle signs carefully.

The first printed term should not begin with `+`.

Negative terms should start with `-`.
8. Format each term in the shortest legal form.

For degree `0`, print only the coefficient.

For degree `1`, print `X` instead of `X^1`.

For coefficients `1` and `-1` on non-constant terms, omit the numeric part.
9. Print the final string.

### Why it works

After processing the first `k` factors, the coefficient array exactly represents:

$$(x+a_1)(x+a_2)\dots(x+a_k)$$

This invariant is true initially because the polynomial is `1`.

When multiplying by `(x+a_{k+1})`, every term contributes correctly to the new polynomial through distributivity. Multiplication by `a_{k+1}` preserves degree, while multiplication by `x` increases degree by one. Since every contribution is added exactly once, the resulting coefficients are correct.

The formatting phase is correct because each coefficient is translated according to the statement's shortest-form rules, and zero terms are omitted entirely.

## Python Solution

```python
import sys
input = sys.stdin.readline

def format_term(coef, deg, first):
    if coef == 0:
        return ""

    sign = ""
    if coef < 0:
        sign = "-"
    elif not first:
        sign = "+"

    val = abs(coef)

    if deg == 0:
        body = str(val)
    else:
        if val == 1:
            coef_part = ""
        else:
            coef_part = str(val) + "*"

        if deg == 1:
            body = coef_part + "X"
        else:
            body = coef_part + f"X^{deg}"

    return sign + body

def solve():
    n = int(input())
    a = [int(input()) for _ in range(n)]

    # coefficients by increasing degree
    poly = [1]

    for x in a:
        nxt = [0] * (len(poly) + 1)

        for deg, coef in enumerate(poly):
            nxt[deg] += coef * x
            nxt[deg + 1] += coef

        poly = nxt

    parts = []
    first = True

    for deg in range(n, -1, -1):
        term = format_term(poly[deg], deg, first)

        if term:
            parts.append(term)
            first = False

    print("".join(parts))

solve()
```

The polynomial coefficients are stored in increasing degree order because it simplifies transitions during multiplication. When processing a factor `(x + a)`, each existing coefficient contributes to exactly two positions in the next array.

The update:

```
nxt[deg] += coef * x
nxt[deg + 1] += coef
```

comes directly from distributive multiplication.

The formatting function isolates all output rules in one place. This avoids scattered special cases and makes correctness easier to reason about.

The most error-prone detail is handling coefficients `1` and `-1`. For example:

```
1*X^2
```

is invalid because the shortest representation must omit the `1`.

Another subtle point is sign handling. The first positive term must not start with `+`, while every later positive term must.

The loop prints degrees from largest to smallest so the polynomial appears in standard form.

## Worked Examples

### Example 1

Input:

```
2
-1
1
```

We compute:

$$(x-1)(x+1)$$

| Step | Factor | Polynomial Coefficients |
| --- | --- | --- |
| Start | - | `[1]` |
| After `x-1` | `-1` | `[-1, 1]` |
| After `x+1` | `1` | `[-1, 0, 1]` |

The coefficient array means:

$$-1 + 0x + 1x^2$$

The `x` term disappears because its coefficient is zero.

Final output:

```
X^2-1
```

This trace demonstrates why skipping zero coefficients is mandatory.

### Example 2

Input:

```
3
1
1
1
```

We compute:

$$(x+1)^3$$

| Step | Factor | Polynomial Coefficients |
| --- | --- | --- |
| Start | - | `[1]` |
| After first | `1` | `[1, 1]` |
| After second | `1` | `[1, 2, 1]` |
| After third | `1` | `[1, 3, 3, 1]` |

The coefficients correspond to:

$$1 + 3x + 3x^2 + x^3$$

Printing from highest degree downward gives:

```
X^3+3*X^2+3*X+1
```

This example confirms that coefficients are accumulated correctly across repeated multiplications.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each multiplication touches all current coefficients |
| Space | O(n) | Only the current polynomial is stored |

With `n ≤ 9`, the algorithm performs only a few dozen arithmetic operations. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def format_term(coef, deg, first):
        if coef == 0:
            return ""

        sign = ""
        if coef < 0:
            sign = "-"
        elif not first:
            sign = "+"

        val = abs(coef)

        if deg == 0:
            body = str(val)
        else:
            if val == 1:
                coef_part = ""
            else:
                coef_part = str(val) + "*"

            if deg == 1:
                body = coef_part + "X"
            else:
                body = coef_part + f"X^{deg}"

        return sign + body

    n = int(input())
    a = [int(input()) for _ in range(n)]

    poly = [1]

    for x in a:
        nxt = [0] * (len(poly) + 1)

        for deg, coef in enumerate(poly):
            nxt[deg] += coef * x
            nxt[deg + 1] += coef

        poly = nxt

    parts = []
    first = True

    for deg in range(n, -1, -1):
        term = format_term(poly[deg], deg, first)

        if term:
            parts.append(term)
            first = False

    return "".join(parts)

# provided sample
assert run("2\n-1\n1\n") == "X^2-1", "sample 1"

# minimum size
assert run("1\n1\n") == "X+1", "single factor positive"

# zero coefficients in middle
assert run("2\n0\n0\n") == "X^2", "middle and constant zero"

# repeated values
assert run("3\n1\n1\n1\n") == "X^3+3*X^2+3*X+1", "binomial expansion"

# negative coefficient formatting
assert run("1\n-3\n") == "X-3", "constant negative"

# maximum degree style case
assert run("9\n0\n0\n0\n0\n0\n0\n0\n0\n0\n") == "X^9", "highest degree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `X+1` | Omitting coefficient `1` |
| `2 0 0` | `X^2` | Removing zero terms |
| `3 1 1 1` | `X^3+3*X^2+3*X+1` | Correct coefficient accumulation |
| `1 -3` | `X-3` | Constant formatting |
| Nine zeros | `X^9` | Maximum degree handling |

## Edge Cases

Consider:

```
2
-1
1
```

The polynomial becomes:

$$(x-1)(x+1)=x^2-1$$

During multiplication the coefficient array becomes:

```
[-1, 0, 1]
```

The algorithm skips the degree-1 term because its coefficient is zero. The final output is:

```
X^2-1
```

This avoids the invalid form `X^2+0*X-1`.

Now consider:

```
1
1
```

The coefficient array is:

```
[1, 1]
```

When formatting the degree-1 term, the algorithm detects coefficient `1` and suppresses the numeric prefix. The output becomes:

```
X+1
```

instead of `1*X+1`.

Finally, consider:

```
2
0
0
```

The polynomial is:

$$x^2$$

The coefficient array is:

```
[0, 0, 1]
```

Both lower-degree terms are skipped. The algorithm prints only:

```
X^2
```

which is the required shortest representation.
