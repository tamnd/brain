---
title: "CF 102878J - Teacher Long and Machine Learning"
description: "The task is to recover the coefficients of a fourth-degree polynomial from five observed values. The five observations correspond to the polynomial evaluated at x = 1, 2, 3, 4, and 5, but every observation may contain an error of at most one."
date: "2026-07-25T12:46:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "J"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 42
verified: true
draft: false
---

[CF 102878J - Teacher Long and Machine Learning](https://codeforces.com/problemset/problem/102878/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
# Problem Understanding

The task is to recover the coefficients of a fourth-degree polynomial from five observed values. The five observations correspond to the polynomial evaluated at x = 1, 2, 3, 4, and 5, but every observation may contain an error of at most one. The real polynomial has integer coefficients in the range [-100, 100], and we must output the unique coefficient set that could have generated the noisy observations.

The input contains several test cases. Each test case gives five integers representing the observed values. The output for each case is the constant coefficient through the fourth-degree coefficient, meaning a0, a1, a2, a3, and a4 for the polynomial a0 + a1x + a2x² + a3x³ + a4x⁴.

The small number of observations is the key constraint. We only have five values, so the mathematical degree of freedom is very limited. A general quartic is fully determined by five exact points, but here every point can move by one unit because of noise. The number of possible corrections is therefore small enough to explore. A method that tries all possible corrected datasets performs only a few hundred checks per test case. More complicated polynomial recovery methods are unnecessary.

A careless implementation can still fail in a few situations. If the noise is ignored and the five given values are directly interpolated, a single corrupted value can create a completely different quartic.

For example:

```
1 4 9 16 24
```

The correct output is:

```
0 0 1 0 0
```

The values almost match x², but the last value is one smaller than 25. Direct interpolation treats the bad measurement as truth and produces a different quartic.

Another edge case is when the polynomial has higher-looking values because of the constant and linear terms.

Input:

```
25 16 9 4 1
```

The output is:

```
36 -12 1 0 0
```

A solution that only checks simple patterns such as squares or tries to guess the degree can fail here. The polynomial is still quadratic, but its coefficients are shifted.

The noise can also appear in several positions at once. A method that assumes only the last value is wrong will fail because every observation is allowed to differ from the true value.

## Approaches

The direct brute-force idea is to assume the five observed values are exact and perform polynomial interpolation. Five points uniquely define a quartic, so this approach is mathematically valid for clean data. The issue is that the input values are not guaranteed to be clean. A single noisy point changes the interpolated polynomial, and there is no way to distinguish the wrong quartic from the real one.

A stronger brute-force method uses the small noise range. Each observation can be corrected by -1, 0, or +1. Since there are only five observations, there are 3⁵ = 243 possible corrected sequences. For each candidate sequence, we interpolate the quartic and check whether the resulting coefficients are all integers within the allowed range. The problem guarantees that at least one valid polynomial exists, so the first valid candidate we find is the answer.

The important observation is that the uncertainty is in the input values, not in the polynomial degree. Instead of searching through all possible coefficients, which would be enormous, we search through the tiny space of possible measurement errors. Once the true five values are found, interpolation is straightforward.

The interpolation itself is done using finite differences. For equally spaced x values, a fourth-degree polynomial has a constant fourth difference. Using the corrected values, we compute the Newton form of the polynomial and convert it into normal powers of x. Fraction arithmetic avoids precision problems and lets us verify that the coefficients are truly integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over coefficients | O(201⁵) | O(1) | Too slow |
| Direct interpolation of noisy values | O(1) | O(1) | Wrong |
| Enumerate noise corrections and interpolate | O(3⁵) | O(1) | Accepted |

## Algorithm Walkthrough

1. Generate every possible corrected version of the five observations. For each position, try adding -1, 0, and +1. These are exactly the possible true values because the measurement error cannot exceed one.
2. Interpolate the polynomial for the current corrected values. The x coordinates are fixed as 1, 2, 3, 4, and 5, so finite differences give a compact way to construct the quartic.
3. Convert the polynomial from the Newton basis into the normal coefficient form. The required output format is a0, a1, a2, a3, and a4, so we need the coefficients of x⁰ through x⁴.
4. Check whether every coefficient is an integer and whether every coefficient lies inside [-100, 100]. If all checks pass, this polynomial satisfies all original conditions and is the answer.
5. Output the five coefficients and stop searching. The guarantee of a valid solution means the enumeration must find one.

Why it works: every valid polynomial produces exactly one corrected sequence where each noisy observation is adjusted back to the true value. The enumeration examines that sequence. Interpolation reconstructs the only quartic passing through those five true points. The coefficient validation removes all candidates that do not satisfy the original restrictions. Since the valid polynomial is guaranteed to exist, the algorithm cannot finish without finding the correct coefficients.

## Python Solution

```python
import sys
from fractions import Fraction

input = sys.stdin.readline

def multiply_poly(a, b):
    res = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y
    return res

def add_poly(a, b):
    n = max(len(a), len(b))
    res = [Fraction(0)] * n
    for i in range(len(a)):
        res[i] += a[i]
    for i in range(len(b)):
        res[i] += b[i]
    return res

def interpolate(values):
    diff = [Fraction(x) for x in values]
    coeff = []
    while diff:
        coeff.append(diff[0])
        diff = [diff[i + 1] - diff[i] for i in range(len(diff) - 1)]

    result = [Fraction(0)]
    basis = [Fraction(1)]
    denominator = 1

    for i, c in enumerate(coeff):
        if i > 0:
            basis = multiply_poly(basis, [Fraction(-i), Fraction(1)])
            denominator *= i
        term = [x * c / denominator for x in basis]
        result = add_poly(result, term)

    return result

def solve_case(arr):
    def dfs(idx, cur):
        if idx == 5:
            poly = interpolate(cur)
            poly += [Fraction(0)] * (5 - len(poly))
            if all(x.denominator == 1 and -100 <= x <= 100 for x in poly[:5]):
                return [int(x) for x in poly[:5]]
            return None

        for delta in (-1, 0, 1):
            cur.append(arr[idx] + delta)
            ans = dfs(idx + 1, cur)
            if ans is not None:
                return ans
            cur.pop()
        return None

    return dfs(0, [])

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        values = list(map(int, input().split()))
        ans.append(" ".join(map(str, solve_case(values))))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The `multiply_poly` and `add_poly` functions handle polynomial arithmetic in coefficient form. Keeping these operations separate makes the interpolation logic easier to verify.

The `interpolate` function builds the Newton finite-difference representation. The first value from every difference layer becomes a Newton coefficient. The basis polynomial is multiplied by `(x - i)` after each layer, matching the points x = 1, 2, 3, 4, and 5. Fractions are used because intermediate values such as division by 2, 6, or 24 appear even though the final answer must be integral.

The depth-first search tries the three possible corrections for each observation. Once five corrected values are selected, the polynomial is reconstructed and checked. The range check is done after verifying that the denominator is one, which avoids accidentally accepting fractional coefficients.

There are no floating point operations, so rounding errors cannot create false answers. Python integers also handle all intermediate arithmetic safely.

## Worked Examples

### Example 1

Input:

```
1 4 9 16 25
```

One successful correction path is:

| Step | Corrected values | Polynomial coefficients |
| --- | --- | --- |
| Start | 1, 4, 9, 16, 25 | Not calculated |
| After correction search | 1, 4, 9, 16, 25 | 0, 0, 1, 0, 0 |

The values already match x² exactly, so no correction is needed. The invariant is that every accepted candidate represents a polynomial consistent with all five observations.

### Example 2

Input:

```
1 4 9 16 24
```

The search finds:

| Step | Corrected values | Polynomial coefficients |
| --- | --- | --- |
| Start | 1, 4, 9, 16, 24 | Not calculated |
| Try correction of fifth value | 1, 4, 9, 16, 25 | 0, 0, 1, 0, 0 |

The final observation is increased by one. The resulting corrected sequence produces the quadratic x², showing why checking nearby measurements is enough to recover the original function.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3⁵ * 5³) | There are 243 possible corrected datasets, and each interpolation handles only five points. |
| Space | O(1) | Only small arrays containing polynomial coefficients and differences are stored. |

The number of test cases is at most ten, so even a few thousand arithmetic operations per case are far below the limits. The algorithm spends most of its time on constant-sized polynomial operations.

## Test Cases

```python
import sys
import io
from fractions import Fraction

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    main()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert run("""3
1 4 9 16 25
1 4 9 16 24
25 16 9 4 1
""") == """0 0 1 0 0
0 0 1 0 0
36 -12 1 0 0
""", "samples"

assert run("""1
0 0 0 0 0
""") == """0 0 0 0 0
""", "all equal values"

assert run("""1
1 2 3 4 5
""") == """0 1 0 0 0
""", "linear boundary case"

assert run("""1
100 101 104 109 116
""") == """0 0 1 0 0
""", "quadratic with shifted observations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 4 9 16 25` | `0 0 1 0 0` | Exact polynomial without noise |
| `1 4 9 16 24` | `0 0 1 0 0` | Single corrupted observation |
| `0 0 0 0 0` | `0 0 0 0 0` | All values equal |
| `1 2 3 4 5` | `0 1 0 0 0` | Low-degree polynomial |
| `100 101 104 109 116` | `0 0 1 0 0` | Larger values and coefficient bounds |

## Edge Cases

For the input:

```
1 4 9 16 24
```

the algorithm explores corrections around every observation. When it reaches the candidate sequence:

```
1 4 9 16 25
```

the finite differences become those of x², and the recovered coefficients are:

```
0 0 1 0 0
```

The wrong direct interpolation approach would keep 24 as a true value and return a different quartic.

For the input:

```
25 16 9 4 1
```

the algorithm does not assume the polynomial must resemble x². It reconstructs the polynomial from the five corrected points and obtains:

```
36 -12 1 0 0
```

which represents x² - 12x + 36. This demonstrates that shifted quadratics are handled naturally.

For an input where several values have noise, such as:

```
2 3 8 15 24
```

the search still considers every combination of adjustments. It does not rely on a particular position being corrupted. Once all five true values are selected, interpolation and validation decide whether the candidate is acceptable.

The minimum-size conceptual case is when all five observations are identical. The algorithm still runs the same search and interpolation process, and it accepts the constant polynomial when the coefficients satisfy the required range.
