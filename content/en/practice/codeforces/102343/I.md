---
title: "CF 102343I - Floating-Point Unrounding"
description: "We are given consecutive values from a positive geometric sequence, but every value has already been rounded to exactly (D) significant digits. The original sequence has the form [ ai=a0r^i, ] where both (a0) and (r) are unknown."
date: "2026-08-16T18:40:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "I"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 1030
verified: false
draft: false
---

[CF 102343I - Floating-Point Unrounding](https://codeforces.com/problemset/problem/102343/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 17m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given consecutive values from a positive geometric sequence, but every value has already been rounded to exactly (D) significant digits. The original sequence has the form

[
a_i=a_0r^i,
]

where both (a_0) and (r) are unknown. Because rounding destroys information, there can be many possible pairs ((a_0,r)) that produce the given displayed sequence. The task is to find the tight lower and upper bounds for (a_0), and independently the tight lower and upper bounds for (r). The four answers must be printed with more significant digits than the input, specifically (D+3) digits for (a_0) and (D+5) digits for (r). These are the exact quantities requested by the original contest statement.

The constraints are deliberately small in (N), with (N<200), but the problem is primarily about finding the right mathematical representation rather than avoiding an enormous input size. An (O(N^2)) algorithm performs only about forty thousand pair operations at the maximum input size, which is trivial. Even an (O(N^3)) method would perform roughly eight million checks for (N=200), so it is still potentially workable here, but it obscures the structure of the problem and would scale poorly.

The first edge case is when there are only two terms. For example,

```
1 2
10 20
```

The value 10 represents the interval ([9.5,10.5]), while 20 represents ([19.5,20.5]). The tight bounds are (a_0\in[9.5,10.5]), (r\in[19.5/10.5,20.5/9.5]), so the output is

```
9.500 10.50 1.85714 2.15789
```

A careless implementation that propagates one rounded value forward using an arbitrary representative, such as the displayed center, would lose the possible combinations at the endpoints.

Another edge case occurs when the displayed values have trailing zeroes. For example, `180.0` and `180` have the same numerical value but not the same significant-digit precision. In this problem, `180.0` has four significant digits, so its rounding unit is (0.1), giving a half-width of (0.05). Treating the input as an ordinary floating-point number and counting decimal places after converting it would lose this information. The original statement explicitly makes the formatting significant, including mandatory trailing zeroes.

A third edge case is that the tight bound for (a_0) need not come directly from the first term's rounding interval. For the sample

```
3 6
12.9 13.0 13.2 13.3 13.4 13.5
```

the first term alone permits (a_0) up to (12.95), but the other terms restrict the geometric progression enough that the requested upper bound is (12.949). The same phenomenon occurs for (r), where the most restrictive pair of terms can be non-adjacent. The official sample output demonstrates both effects.

## Approaches

A direct approach is to turn every rounded value into an interval, enumerate candidate intersections of the corresponding constraints, and check every candidate against all (N) terms. This works because after taking logarithms, every geometric-sequence constraint becomes a strip bounded by two straight lines. An endpoint of the feasible region is determined by intersections of those lines. There are (O(N^2)) possible pairs of lines, and checking every candidate against all constraints gives (O(N^3)) work, about eight million constraint checks when (N) is near 200. That is still feasible for the official bounds, but it is more computation than necessary and makes the correctness argument harder.

The key observation is that the logarithm removes the exponential part of the geometric sequence. Let

[
x=\log a_0,\qquad y=\log r.
]

Then

[
\log a_i=x+iy.
]

Suppose the original value corresponding to the (i)-th rounded input must lie between (L_i) and (U_i). The condition becomes

[
L'_i\le x+iy\le U'_i,
]

where (L'_i=\log L_i) and (U'_i=\log U_i).

We now have only linear inequalities in two variables. The entire problem is a two-dimensional linear-feasibility problem.

The bounds for (x) and (y) can be obtained by eliminating the other variable pairwise. Since there are only two variables, Fourier-Motzkin elimination becomes especially simple. For every pair of indices (i>j), combining one lower constraint with one upper constraint gives a direct bound on (y), while combining the opposite pair gives a direct bound on (x). Taking the maximum of all lower bounds and the minimum of all upper bounds gives the exact projection of the feasible region onto each axis.

The brute-force and optimal approaches are thus solving the same geometric problem. The brute-force method explicitly searches the polygon formed by the constraints. The optimal method observes that we only need its projections onto the (x) and (y) axes, so the other variable can be eliminated algebraically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Boundary enumeration and verification | (O(N^3)) | (O(N)) | Accepted for (N<200), but unnecessarily expensive |
| Pairwise elimination | (O(N^2)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Convert every displayed decimal into the interval of real numbers that could have produced it after rounding to (D) significant digits. If
