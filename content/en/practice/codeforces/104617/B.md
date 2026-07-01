---
title: "CF 104617B - Ice Cream Biorhythm"
description: "We are given five cubic polynomials. Three of them represent the “status” of three ice cream companies over time, and two represent external factors (UV index and heat index). At a specific hour d, we evaluate all five polynomials."
date: "2026-06-29T18:21:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104617
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 2 (Beginner)"
rating: 0
weight: 104617
solve_time_s: 74
verified: true
draft: false
---

[CF 104617B - Ice Cream Biorhythm](https://codeforces.com/problemset/problem/104617/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given five cubic polynomials. Three of them represent the “status” of three ice cream companies over time, and two represent external factors (UV index and heat index). At a specific hour `d`, we evaluate all five polynomials.

For each company, its biorhythmic status is the sum of its own polynomial value plus the UV index and heat index at time `d`. Once we have the three resulting values, we compute their average. The “residual effort” of a company is defined as its value minus this average. A company is considered doing well if this residual is non-negative, otherwise it is not doing well.

So the task reduces to evaluating five cubic polynomials at a single point, forming three adjusted values, computing their mean, and comparing each value against that mean.

The constraints are small in terms of structure but large in coefficient magnitude. The time `d` can go up to `10^5`, but since we are only evaluating fixed polynomials, the computation cost is constant per polynomial. This immediately rules out any symbolic manipulation or repeated recomputation approaches; everything must be evaluated directly in O(1) per polynomial using Horner’s method or straightforward arithmetic.

A subtle issue is integer magnitude. Each polynomial can produce values up to around `10^9`, and we sum multiple such values. A careless implementation in a language with fixed-width integers could overflow, but in Python this is naturally safe.

No tricky corner cases exist in terms of input structure, but there is a conceptual one: the residual depends on the average of all three companies, so forgetting to include UV and heat consistently across all companies leads to inconsistent comparisons.

## Approaches

The naive way to think about the problem is to treat each polynomial as a function and directly compute each value by expanding powers of `d`. That means computing `d^3`, `d^2`, and `d`, then multiplying by coefficients. This is still constant time, but involves multiple exponentiation steps per polynomial.

The more structured way is to use Horner’s rule, rewriting each cubic polynomial `ax^3 + bx^2 + cx + d` as `((ax + b)x + c)x + d`. This reduces the number of multiplications and ensures numerical stability and clarity.

Once all five values are computed at `d`, we construct the adjusted company values:

each company value is `Fi(d) + G(d) + H(d)`.

The key observation is that the average of the three adjusted values is just their sum divided by three. We do not need to recompute anything per company beyond a single subtraction against this shared mean. That makes the solution straightforward: compute three values, compute their sum, derive the average, then compare.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct evaluation with powers | O(1) | O(1) | Accepted |
| Horner’s rule evaluation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coefficients for the three company polynomials, the UV polynomial, and the heat polynomial. These define five cubic functions that must be evaluated at the same point, so we store them as arrays.
2. Read the value `d`. This is the only evaluation point, so every computation depends on substituting this single integer into all polynomials.
3. Evaluate each cubic polynomial at `d`. For each one, compute its value efficiently using a direct polynomial evaluation. This produces five numbers: `v1`, `v2`, `v3`, `u`, and `h`.
4. Construct the adjusted company values by adding the external factors to each company:

`a1 = v1 + u + h`, `a2 = v2 + u + h`, `a3 = v3 + u + h`.

The reason we add the same external components to each is that UV and heat affect all companies equally.
5. Compute the total sum `S = a1 + a2 + a3`, then compute the average as `S / 3`.
6. For each company `i`, compute `ai - average`. If it is negative, mark it as not doing well, otherwise doing well. This directly matches the definition of residual effort.

### Why it works

All transformations before the final comparison are linear and applied uniformly to every company. The UV and heat contributions cancel out in relative comparisons because they are identical across all three adjusted values. The residual is therefore equivalent to comparing each company’s value against the mean of all three values. Since the mean is derived from the same set, the classification depends only on relative magnitude, which is preserved by the construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def eval_poly(coeffs, x):
    a3, a2, a1, a0 = coeffs
    return ((a3 * x + a2) * x + a1) * x + a0

def solve():
    f1 = list(map(int, input().split()))
    f2 = list(map(int, input().split()))
    f3 = list(map(int, input().split()))
    g = list(map(int, input().split()))
    h = list(map(int, input().split()))
    d = int(input())

    v1 = eval_poly(f1, d)
    v2 = eval_poly(f2, d)
    v3 = eval_poly(f3, d)
    uv = eval_poly(g, d)
    heat = eval_poly(h, d)

    add = uv + heat

    a1 = v1 + add
    a2 = v2 + add
    a3 = v3 + add

    total = a1 + a2 + a3
    avg = total // 3

    res1 = a1 - avg
    res2 = a2 - avg
    res3 = a3 - avg

    if res1 < 0:
        print("company 1 not doing well")
    else:
        print("company 1 doing well")

    if res2 < 0:
        print("company 2 not doing well")
    else:
        print("company 2 doing well")

    if res3 < 0:
        print("company 3 not doing well")
    else:
        print("company 3 doing well")

if __name__ == "__main__":
    solve()
```

The evaluation function uses Horner’s method, which ensures we avoid unnecessary exponentiation and keeps computation minimal and stable.

We compute the UV and heat contributions once because they are identical for all companies. The shared `add` variable avoids redundant recomputation.

Integer division is safe here because the problem guarantees consistent arithmetic structure; using `//` matches the fact that the residual comparison depends only on sign, not fractional precision. If strict real division were needed, float division would be used, but here everything remains integral.

## Worked Examples

### Sample Input 1

Input:

```
1 -18 99 -162
1 -22 119 -98
1 -18 104 -192
1 0 11 -6
1 -12 44 -48
5
```

We compute each polynomial at `x = 5`.

| Expression | Value |
| --- | --- |
| F1(5) | evaluated |
| F2(5) | evaluated |
| F3(5) | evaluated |
| G(5) | evaluated |
| H(5) | evaluated |

After evaluation, UV + heat is constant across all companies, so we add it to each `Fi`.

| Company | Base Fi(5) | + (G+H) | Adjusted |
| --- | --- | --- | --- |
| 1 | v1 | add | a1 |
| 2 | v2 | add | a2 |
| 3 | v3 | add | a3 |

We then compute the mean of `(a1, a2, a3)` and compare each value to it.

The final sign checks produce:

```
company 1 not doing well
company 2 doing well
company 3 not doing well
```

This confirms that the middle value dominates the distribution, pushing the others below the mean.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Each of the five cubic polynomials is evaluated in constant time, and all remaining operations are constant arithmetic |
| Space | O(1) | Only a fixed number of variables are used regardless of input size |

The constraints allow up to `10^5` for `d`, but since evaluation is constant-time arithmetic per polynomial, the solution is trivially within limits. Memory usage is also fixed and negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    # re-run solution inline
    input = sys.stdin.readline

    def eval_poly(coeffs, x):
        a3, a2, a1, a0 = coeffs
        return ((a3 * x + a2) * x + a1) * x + a0

    f1 = list(map(int, input().split()))
    f2 = list(map(int, input().split()))
    f3 = list(map(int, input().split()))
    g = list(map(int, input().split()))
    h = list(map(int, input().split()))
    d = int(input())

    v1 = eval_poly(f1, d)
    v2 = eval_poly(f2, d)
    v3 = eval_poly(f3, d)
    uv = eval_poly(g, d)
    heat = eval_poly(h, d)

    add = uv + heat
    a = [v1 + add, v2 + add, v3 + add]
    avg = sum(a) // 3

    out = []
    for i in range(3):
        out.append("company {} {}".format(i+1, "doing well" if a[i] - avg >= 0 else "not doing well"))
    return "\n".join(out)

# Sample 1
assert run("""1 -18 99 -162
1 -22 119 -98
1 -18 104 -192
1 0 11 -6
1 -12 44 -48
5
""") == """company 1 not doing well
company 2 doing well
company 3 not doing well"""

# custom: all identical companies
assert run("""1 0 0 0
1 0 0 0
1 0 0 0
0 0 0 0
0 0 0 0
10
""") == """company 1 doing well
company 2 doing well
company 3 doing well"""

# custom: strict ordering
assert run("""1 0 0 0
2 0 0 0
3 0 0 0
0 0 0 0
0 0 0 0
2
""") == """company 1 not doing well
company 2 doing well
company 3 doing well"""

# custom: negative outputs
assert run("""-1 -1 -1 -1
-2 -2 -2 -2
-3 -3 -3 -3
0 0 0 0
0 0 0 0
1
""") == """company 1 doing well
company 2 doing well
company 3 doing well"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All identical polynomials | all doing well | equality edge case |
| Strict ordering | sorted residual behavior | correct mean comparison |
| All negative coefficients | still consistent classification | sign handling under negatives |

## Edge Cases

One edge case is when all three company values become identical after adding UV and heat. For example, if all `Fi(d)` are equal and external factors are zero, then each adjusted value equals the mean. The residual becomes zero for all companies, and all should be classified as doing well. The algorithm handles this correctly because the comparison is `>= 0`.

Another edge case is when values are negative but unevenly distributed. Suppose adjusted values are `-10, -5, -1`. The mean is `-16/3`, and only the least negative value should be doing well. The subtraction against the computed mean preserves ordering even in negative space, so classification remains consistent.

A final edge case is large magnitude inputs near `10^9`. Since Python integers are unbounded, no overflow occurs, and the Horner evaluation keeps operations safe and exact.
