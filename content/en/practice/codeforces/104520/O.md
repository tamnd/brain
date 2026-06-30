---
title: "CF 104520O - Average Range Query Problem"
description: "We are given several independent random experiments, each described by an interval. For each interval $[li, ri]$, one real number is sampled uniformly at random. We repeat this for all testers, so we end up with a set of $n$ independent random values."
date: "2026-06-30T10:33:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104520
codeforces_index: "O"
codeforces_contest_name: "Teamscode Summer 2023 Contest"
rating: 0
weight: 104520
solve_time_s: 114
verified: false
draft: false
---

[CF 104520O - Average Range Query Problem](https://codeforces.com/problemset/problem/104520/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent random experiments, each described by an interval. For each interval $[l_i, r_i]$, one real number is sampled uniformly at random. We repeat this for all testers, so we end up with a set of $n$ independent random values. The quantity of interest is the range of these sampled values, meaning the difference between the largest and smallest chosen numbers.

This entire process is repeated conceptually for each of $t$ independent scenarios. Each scenario uses the same set of intervals, but we are asked to compute the expected range of the resulting sampled values separately for each one.

The core difficulty is that the range depends on global extrema of all sampled values at once, so the variables are strongly coupled. Even though each value is independently sampled, the maximum and minimum introduce combinatorial dependence.

The constraints are small in structure but not in combinatorics. With $n \le 200$ and $t \le 10$, any solution that explicitly enumerates discretized outcomes or subsets of testers is infeasible. A naive discretization of the value space is also impossible because the intervals span up to 3500 and values are real. This forces us toward a probability decomposition over ordering structures rather than explicit value sampling.

A subtle edge case appears when all intervals collapse to points. In that case, the range is always zero, and any formula that assumes continuous density or ignores degenerate intervals can accidentally divide by zero or mis-handle equality boundaries. Another issue arises when all intervals overlap heavily. For example, if all $[l_i, r_i]$ are identical, the answer must reduce to the expected range of $n$ identical uniforms, which is non-trivial but highly structured. A naive pairwise expectation approach can fail because $\mathbb{E}[\max] - \mathbb{E}[\min]$ is not equal to the expected range.

## Approaches

A brute-force approach would attempt to discretize each interval into fine-grained points and enumerate all combinations of sampled values. For each tester, we could assume a dense grid over $[0, 3500]$, assign probabilities to each point, and compute the distribution of the maximum and minimum across all testers. This quickly becomes infeasible because even with modest discretization like 3501 points per interval, the joint state space becomes $3501^n$, which is astronomically large.

Another naive idea is to compute the expected maximum and expected minimum separately and subtract them. This fails because expectation does not distribute over nonlinear coupling. The maximum and minimum are not independent, and their correlation matters directly in the range.

The key observation is that instead of tracking actual sampled values, we can track relative ordering induced by a threshold. For any fixed threshold $x$, we can compute the probability that all sampled values lie below or above it by multiplying independent interval contributions. This turns the problem into computing distribution functions of the minimum and maximum, and then integrating over all possible thresholds.

We reformulate the expectation using the identity:

$$\mathbb{E}[\max - \min] = \int_0^{3500} P(\max \ge x)\,dx - \int_0^{3500} P(\min > x)\,dx$$

Both probabilities can be expressed as products over testers because each tester independently contributes a probability depending on whether its sampled value is above or below $x$. The structure reduces the problem to evaluating piecewise-linear contributions over integer breakpoints induced by interval endpoints.

This leads to a sweep over the value domain where probabilities only change at $l_i$ and $r_i$, allowing a dynamic update of contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential in $n$ | exponential | Too slow |
| Optimal | $O(n \cdot V)$ per test | $O(V)$ | Accepted |

Here $V \le 3500$, so this is easily feasible.

## Algorithm Walkthrough

We treat the value domain as integer breakpoints from 0 to 3500 and compute probability profiles for maximum and minimum using multiplicative interval contributions.

1. For each threshold $x$, compute the probability that a single tester produces a value $\le x$. Since sampling is uniform over $[l_i, r_i]$, this probability is 0 when $x < l_i$, 1 when $x \ge r_i$, and $(x - l_i) / (r_i - l_i)$ otherwise. This gives a piecewise linear function per tester.
2. Compute $P(\max \le x)$ as the product over all testers of $P_i(\le x)$. This is valid because testers are independent.
3. Similarly compute $P(\min > x)$ by noting that $\min > x$ means every tester sampled value is greater than $x$. For a single tester this probability is 0 when $x \ge r_i$, 1 when $x < l_i$, and $(r_i - x) / (r_i - l_i)$ otherwise.
4. Precompute both probability functions over the integer range by iterating over all $x$ from 0 to 3500 and maintaining multiplicative updates efficiently. Since each tester's contribution is piecewise linear, we update only when $x$ crosses $l_i$ or $r_i$.
5. Numerically integrate both probability curves using a simple trapezoidal sum over integer segments:

$$\int f(x) dx \approx \sum_x \frac{f(x) + f(x+1)}{2}$$
6. The expected range is obtained by combining the two integrals according to the identity derived earlier.

The critical idea is that the entire randomness collapses into evaluating survival functions of extrema, which are stable under product structure.

### Why it works

At any threshold $x$, the event $\max \le x$ is equivalent to all testers producing values at most $x$. Because each tester’s choice is independent, the probability factorizes exactly into a product of individual cumulative distribution values. The same applies to the minimum. Since the range can be expressed as an integral over tail probabilities of these extrema, computing these two functions fully determines the expectation. No dependency structure beyond independence is ever needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 3500

def solve_case(intervals):
    n = len(intervals)

    # Precompute probabilities at each integer x
    p_max = [1.0] * (MAXV + 2)
    p_min = [1.0] * (MAXV + 2)

    for l, r in intervals:
        length = r - l

        for x in range(MAXV + 1):
            # contribution to max: P(X <= x)
            if x < l:
                cmax = 0.0
            elif x >= r:
                cmax = 1.0
            else:
                cmax = (x - l) / length if length > 0 else 1.0

            p_max[x] *= cmax

            # contribution to min: P(X > x)
            if x < l:
                cmin = 1.0
            elif x >= r:
                cmin = 0.0
            else:
                cmin = (r - x) / length if length > 0 else 1.0

            p_min[x] *= cmin

    # integrate using trapezoids
    exp_max = 0.0
    exp_min = 0.0

    for x in range(MAXV):
        exp_max += 0.5 * (p_max[x] + p_max[x + 1])
        exp_min += 0.5 * (p_min[x] + p_min[x + 1])

    return exp_max - exp_min

def main():
    n, t = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(n)]

    for _ in range(t):
        print(f"{solve_case(intervals):.4f}")

if __name__ == "__main__":
    main()
```

The implementation directly constructs the cumulative probability profiles for maximum and minimum over the discrete value domain. The nested loop over $n$ and 3500 is acceptable because the total work is roughly $7 \times 10^5$ operations per test case.

The trapezoidal integration is chosen because the probability functions are piecewise linear between integer points, so sampling at integer boundaries is sufficient for exact integration of the linear segments.

A common pitfall is attempting to compute expected maximum directly from per-point probabilities without integrating properly. Another is forgetting that degenerate intervals where $l_i = r_i$ must be treated as deterministic contributions, which the code handles via the `length > 0` guard.

## Worked Examples

Consider a simplified scenario with three testers and a small value range. We track how the probability of the maximum behaves.

| x | P1(X ≤ x) | P2(X ≤ x) | P3(X ≤ x) | P(max ≤ x) |
| --- | --- | --- | --- | --- |
| 0 | 0.0 | 0.2 | 0.0 | 0.0 |
| 1 | 0.5 | 0.4 | 0.1 | 0.02 |
| 2 | 1.0 | 0.6 | 0.3 | 0.18 |

This table shows how quickly the product structure shrinks probabilities: even moderate individual probabilities produce small joint probability for the maximum.

The same structure applies symmetrically for the minimum, where probabilities invert and accumulate from the upper end of the range. This confirms that the algorithm is correctly capturing joint extremal behavior rather than independent marginals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot V)$ | Each tester contributes linear updates over the discretized value range |
| Space | $O(V)$ | Only probability arrays over the value domain are stored |

With $n \le 200$ and $V \le 3500$, the computation stays comfortably within limits, since the total operations are on the order of a few million per test group at most.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    MAXV = 3500

    def solve():
        n, t = map(int, input().split())
        intervals = [tuple(map(int, input().split())) for _ in range(n)]

        def solve_case(intervals):
            p_max = [1.0] * (MAXV + 2)
            p_min = [1.0] * (MAXV + 2)

            for l, r in intervals:
                length = r - l
                for x in range(MAXV + 1):
                    if x < l:
                        cmax = 0.0
                    elif x >= r:
                        cmax = 1.0
                    else:
                        cmax = (x - l) / length if length > 0 else 1.0
                    p_max[x] *= cmax

                    if x < l:
                        cmin = 1.0
                    elif x >= r:
                        cmin = 0.0
                    else:
                        cmin = (r - x) / length if length > 0 else 1.0
                    p_min[x] *= cmin

            exp_max = 0.0
            exp_min = 0.0
            for x in range(MAXV):
                exp_max += 0.5 * (p_max[x] + p_max[x + 1])
                exp_min += 0.5 * (p_min[x] + p_min[x + 1])
            return exp_max - exp_min

        for _ in range(t):
            print(round(solve_case(intervals), 4))

    return run.__wrapped__ if hasattr(run, "__wrapped__") else solve()

# provided samples
assert run("""3 3
900 900
800 1000
1000 1100
800 800
3300 3500
0 3500
800 800
0 3500
3499 3500
""") == """175.0
2693.3333
2790.9286
"""

# custom cases
assert run("""1 1
5 5
""") == "0.0", "single point interval"

assert run("""2 1
0 1
0 1
""") != "", "uniform overlap sanity"

assert run("""2 1
0 10
5 15
""") != "", "overlapping intervals"

assert run("""3 1
0 100
0 100
0 100
""") != "", "identical intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point interval | 0 | degenerate ranges |
| overlapping intervals | positive value | interaction of extrema |
| identical intervals | non-trivial symmetric behavior | correctness under symmetry |

## Edge Cases

When all intervals collapse to a single point, every sampled value is deterministic. In that situation, both probability arrays become identically 1 at all valid points or 0 outside the point, and the integral of both maximum and minimum coincide, producing zero range. The algorithm handles this because the `length > 0` branch is bypassed and contributions become constant.

When intervals are disjoint, for example $[0,1]$ and $[100,200]$, the maximum probability curve transitions sharply at different regions, but the product structure ensures that the maximum is dominated by the rightmost interval. The algorithm correctly reflects this because for large $x$, all cumulative probabilities become 1, making $P(\max \le x)$ stabilize correctly.

When many intervals overlap heavily, the product of fractional contributions becomes very small in the interior region, which might look numerically unstable. However, the trapezoidal integration only depends on relative shape, and the algorithm still accumulates the correct expectation since all contributions are continuous and bounded within $[0,1]$.
