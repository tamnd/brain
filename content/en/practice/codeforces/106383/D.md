---
title: "CF 106383D - Cubic Equation"
description: "The task is to find the real solution of a cubic equation of the special form $$f(x) = x^3 + ax + b$$ where the input gives the two coefficients a and b. Both values are non-negative, which guarantees that the equation has exactly one real root."
date: "2026-06-25T10:19:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106383
codeforces_index: "D"
codeforces_contest_name: "2026 Spring UT CS104c Midterm #1"
rating: 0
weight: 106383
solve_time_s: 28
verified: false
draft: false
---

[CF 106383D - Cubic Equation](https://codeforces.com/problemset/problem/106383/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to find the real solution of a cubic equation of the special form

$$f(x) = x^3 + ax + b$$

where the input gives the two coefficients `a` and `b`. Both values are non-negative, which guarantees that the equation has exactly one real root. The program must output that root with enough precision that the judge accepts the answer within the allowed floating point error.

At first glance this looks like a standard equation-solving problem, and there are mathematical formulas for cubic equations. However, directly implementing the cubic formula is usually not the best competitive programming approach here. The input values can be as large as $10^9$, and the judge only requires a numerical approximation, not an exact symbolic answer. This suggests looking for a numerical method rather than manipulating the equation algebraically.

The size of `a` and `b` rules out any approach that tries many candidate values. We cannot scan possible answers because the root can be around $-10^9$, and checking billions of values would be impossible. A solution needs to use the monotonic structure of the function and finish in a small fixed number of operations.

The important property comes from the derivative:

$$f'(x)=3x^2+a$$

Since `a` is non-negative, the derivative is always positive. That means the function is strictly increasing everywhere. A strictly increasing continuous function crosses zero at most once, and because the problem guarantees that a root exists, we can locate it using binary search.

There are a few floating point pitfalls that can break a seemingly correct implementation. A common mistake is choosing an interval that does not always contain the answer. For example, with input

```
1000000000 0
```

the equation is

$$x^3 + 10^9x = 0$$

and the answer is exactly `0`. If a solution searches only positive values because the cubic term dominates, it misses the negative side of possible roots in other cases.

Another mistake is using an interval that is too small for large `b`. For example:

```
0 1000000000
```

requires solving

$$x^3+10^9=0$$

which gives a root close to `-1000`. A search range like `[-100,100]` would never reach the answer.

The case where both coefficients are zero also needs care:

```
0 0
```

The equation becomes

$$x^3=0$$

and the answer is `0`. A binary search implementation must still converge correctly when the answer is exactly on the boundary or at the midpoint of the search interval.

## Approaches

The most direct idea is to try to guess the answer. Since the function is simple, we could pick many values of `x`, evaluate

$$x^3+ax+b$$

and look for where it becomes zero. This is correct because the function is continuous, so values close enough to the root will produce a small absolute value. The problem is that there is no useful discrete range to search. The root can be as small as `0` or around `-1000` for the given limits, and arbitrary precision scanning would require too many evaluations. Even if we tried millions of candidates, the precision requirement would not be guaranteed.

The key observation is that we are not searching an arbitrary function. The cubic function here is strictly increasing because its derivative is always positive. This means every value smaller than the root produces a negative result and every value larger than the root produces a positive result.

That is exactly the condition needed for binary search on a real number. We maintain an interval containing the root, repeatedly check the middle, and discard the half that cannot contain the answer. After enough iterations, the interval becomes extremely small, and either endpoint is a good approximation.

The only remaining question is how to choose the initial bounds. Because `b` is non-negative, the root cannot be positive. If `x` is positive, every term in

$$x^3+ax+b$$

is non-negative, so the function cannot equal zero except at `x = 0` when both coefficients are zero. The negative side needs to be large enough to contain the root. Since

$$(-100000)^3$$

is already much smaller than any possible positive `b`, using a range like `[-10^6, 10^6]` is safely large enough. Another common approach is to derive the bound from `b`, but a fixed large interval is simpler and easily fits the constraints.

The brute-force and optimal methods compare as follows:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of guesses) | O(1) | Too slow / unreliable |
| Binary Search | O(iterations) | O(1) | Accepted |

(continued in next message)
