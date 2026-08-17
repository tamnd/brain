---
title: "CF 102253F - Function"
description: "We have two permutations, a on n positions and b on m values. We want to count functions f that assign every position of a a value from 0 through m - 1, subject to the rule [ f(i)=b(f(ai))."
date: "2026-08-17T21:34:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "F"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 350
verified: true
draft: false
---

[CF 102253F - Function](https://codeforces.com/problemset/problem/102253/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two permutations, `a` on `n` positions and `b` on `m` values. We want to count functions `f` that assign every position of `a` a value from `0` through `m - 1`, subject to the rule

[
f(i)=b(f(a_i)).
]

The useful way to read this equation is that moving once along a cycle of `a` forces the value of `f` to move along a cycle of `b` in the opposite direction. The task is to count all assignments that remain consistent when every cycle is closed. The answer is reported modulo (10^9+7). The original problem page and contest editorial confirm this cycle-based formulation.

Because `a` and `b` are permutations, their functional graphs consist entirely of disjoint directed cycles. This is the structural property that makes the problem much easier than a general function-composition problem.

The values of `n` and `m` can each reach (10^5), and the sums over all test cases reach (10^6). With a one-second limit, anything quadratic in `n` or `m` is already too expensive in the worst case. We need a solution close to linear in the total input size. Fortunately, after decomposing the permutations into cycles, the remaining divisor enumeration can also be bounded linearly.

There are several edge cases that can make an apparently reasonable implementation fail.

Consider

```
1 2
0
1 0
```

The only source position is a cycle of length `1`, while `b` is a cycle of length `2`. The equation requires the chosen target value to be fixed by `b`, but neither target is fixed. The correct answer is `0`. An implementation that simply counts all target values without checking cycle lengths would incorrectly return `2`.

Now consider

```
2 2
1 0
0 1
```

Here `a` is a cycle of length `2`, while `b` consists of two fixed points. Either fixed point can be used for the entire source cycle, so the answer is `2`. A careless implementation might look only for target cycles of exactly the same length and return `0`, but the required condition is that the target cycle length divides the source cycle length.

A boundary case involving a square divisor is

```
4 4
1 2 3 0
0 1 3 2
```

The source has one cycle of length `4`. The target has two cycles of length `1` and one cycle of length `2`. All three target cycles have lengths dividing `4`, contributing (1+1+2=4) possible starting values. The answer is `4`. When enumerating divisors by checking `d * d <= L`, the divisor `2` must be counted only once because it is the square root of `4`.

Finally, a permutation cannot literally have all entries equal unless its size is `1`. For example, `[0]` is the only permutation whose entries are all equal. For larger sizes, the meaningful version of this stress case is that all cycles have the same length. Six elements split into three 2-cycles is a useful example because it tests repeated cycle lengths and repeated multiplication of the same factor.

## Approaches

The direct brute-force approach is conceptually simple. For every one of the (m^n) possible functions, assign a target value to each of the `n` source positions and check all `n` equations. This is correct because every possible function is considered and only functions satisfying every equation are counted.

The problem is the number of candidates. In the worst case with (n=m=10^5), brute force considers

[
100000^{100000}
]

different functions, and checking each candidate can require (100000) equation evaluations. That is up to

[
100000\cdot100000^{100000}
]

basic checks, which is far beyond any feasible limit.

The key observation is that the constraints do not couple arbitrary source positions. They couple positions along cycles of `a`. Suppose one cycle of `a` has length `L`, starting at some position `x`:

[
x,\ a(x),\ a^2(x),\ldots,a^{L-1}(x).
]

Once `f(x)` is chosen, the equation determines the value of `f` at every other position in this cycle. The only question is whether the assignment is consistent when we return to `x`.

Applying the equation around the entire cycle gives

[
f(x)=b^L(f(x)).
]

Thus `f(x)` must be a target value that returns to itself after exactly `L` applications of `b`. If that target value lies in a cycle of `b` of length `d`, then (b^L) fixes it exactly when

[
d\mid L.
]

Suppose `b` contains (c_d) cycles of length `d`. Every such cycle contributes `d` possible choices for `f(x)`, because any of its `d` elements satisfies (b^L(y)=y). Therefore a source cycle of length `L` has

[
\sum_{d\mid L} d,c_d
]

valid assignments.

Different cycles of `a` are independent. Choosing a value for one source cycle does not affect any other source cycle, so the final answer is the product of these quantities over all cycles of `a`.

The remaining task is to calculate these divisor sums efficiently. We can count the cycle lengths of `b` once. Then, for every source cycle length `L`, enumerate its divisors in (O(\sqrt L)) time. Since the source cycle lengths sum to `n`, the total divisor-search work is bounded by

[
\sum_i O(\sqrt{L_i})
\le O\left(\sqrt{k\sum_i L_i}\right)
\le O(n),
]

where `k` is the number of cycles of `a`. Cycle decomposition itself takes (O(n+m)), so the complete algorithm is (O(n+m)). This is also the complexity given by the contest editorial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm^n)) | (O(n)) | Too slow |
| Optimal | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Decompose permutation `b` into disjoint cycles and count how many cycles have each possible length. Let `cnt[d]` be the number of cycles of length `d`.

We only need the number of cycles of each length, not the actual elements inside those cycles, because every element of a valid target cycle is an equally valid starting value.
2. Decompose permutation `a` into disjoint cycles and record their lengths.

For a source cycle, all function values are determined by choosing the image of just one position. This reduces the counting problem from assigning `n` independent values to assigning one starting value per source cycle.
3. For a source cycle of length `L`, calculate

[
ways(L)=\sum_{d\mid L}d\cdot cnt[d].
]

A target cycle of length `d` is usable precisely when `d` divides `L`. It contributes `d` choices because any of its elements can be the image of the chosen source position.
4. Enumerate the divisors of `L` by testing integers `d` from `1` through (\lfloor\sqrt L\rfloor).

When `d` divides `L`, both `d` and `L // d` are divisors. If they are different, add both contributions. If `d * d == L`, add only `d` once.
5. Multiply `ways(L)` into the answer for every source cycle and reduce modulo (10^9+7).

The multiplication is valid because source cycles are independent. Every global function corresponds uniquely to one valid choice for each source cycle.

### Why it works

Take any cycle of `a` with length `L` and choose one position `x` on it. The defining equation determines all other values on that source cycle from `f(x)`. After following the entire source cycle, consistency requires (b^L(f(x))=f(x)). A value in a target cycle of length `d` satisfies this exactly when `d` divides `L`. Hence the number of choices for this source cycle is exactly (\sum_{d\mid L}d,cnt[d]).

Every valid function is uniquely determined by its choices on the separate cycles of `a`, and choices made on different cycles never interact. Multiplying the number of choices for all source cycles consequently counts every valid function exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def cycle_lengths(p):
    n = len(p)
    seen = [False] * n
    lengths = []

    for start in range(n):
        if seen[star]()
```
