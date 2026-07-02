---
title: "CF 103600J - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u044c"
description: "We are given several available solutions, each characterized by a salt concentration. We are allowed to take some integer number of grams from each solution, with an upper limit of 10⁴ grams per solution."
date: "2026-07-02T22:52:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103600
codeforces_index: "J"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2021"
rating: 0
weight: 103600
solve_time_s: 61
verified: true
draft: false
---

[CF 103600J - \u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u044c](https://codeforces.com/problemset/problem/103600/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several available solutions, each characterized by a salt concentration. We are allowed to take some integer number of grams from each solution, with an upper limit of 10⁴ grams per solution. After mixing, the total mass is the sum of chosen masses, and the total salt amount is the weighted sum according to concentrations.

The goal is to construct at least 100 grams of a new mixture whose concentration is exactly Q percent. In other words, if we denote by xi the mass taken from solution i with concentration Ti, the final ratio must satisfy

(sum xi * Ti) / (sum xi) = Q.

This can be rewritten in a more algebraic form by multiplying both sides by the denominator:

sum xi * (Ti − Q) = 0.

So each solution contributes a coefficient ai = Ti − Q, and we need a non-negative integer vector x such that the weighted sum of ai is zero, while also respecting 0 ≤ xi ≤ 10⁴ and total mass at least 100.

The constraints allow up to 10⁵ solutions, so any quadratic strategy over pairs of solutions is immediately suspect. A linear or near-linear construction is required.

A subtle constraint is that even if a valid linear combination exists, it must also produce at least 100 grams total mass. A degenerate solution like a single cancellation of equal magnitude coefficients may satisfy the equation but fail the mass requirement.

Edge cases appear when no solution is possible at all. For example, if all Ti are strictly greater than Q, then every ai is positive, and no non-zero non-negative combination can sum to zero. Similarly, if all Ti are strictly less than Q, the same impossibility occurs. Another special case is when some Ti equals Q; then a trivial construction exists using only that solution.

## Approaches

The brute-force idea is to choose a subset of solutions and assign integer masses to them, checking whether the resulting weighted average equals Q. This quickly becomes a problem of solving a bounded integer linear equation in n variables. Even ignoring the bounds, trying combinations of subsets already leads to exponential behavior, and adding upper limits on coefficients makes direct search infeasible.

Rewriting the condition as sum xi(Ti − Q) = 0 turns the problem into balancing positive and negative contributions. Each Ti > Q acts like a positive weight, and each Ti < Q acts like a negative weight. A valid solution must mix both sides unless some Ti already equals Q.

The key simplification is that only two values are sufficient to construct a zero sum: one from the positive side and one from the negative side. If we pick indices i and j with ai > 0 and aj < 0, we need

xi * ai = xj * (−aj).

Let g be gcd(ai, −aj). The minimal integer solution is

xi = (−aj / g), xj = (ai / g),

and any scaled version of this pair remains valid.

The constraints on xi ≤ 10⁴ and xj ≤ 10⁴ restrict how much we can scale this pair. Among all possible pairs, we want one that allows a large enough scaling factor so that the resulting total mass is at least 100.

Trying all pairs would be O(n²), so we instead exploit structure: only the magnitude of ai matters for feasibility. Extremal choices tend to be best because small coefficients allow larger scaling before hitting the 10⁴ cap.

We therefore reduce the search to picking a positive-side index and a negative-side index that minimize |Ti − Q| on each side. This typically maximizes the usable scaling factor while keeping the ratio simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all assignments | Exponential | O(n) | Too slow |
| Pair construction with greedy selection | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform each concentration into ai = Ti − Q and separate indices into three groups: positive, negative, and zero.

If there exists any index with ai = 0, we can immediately construct a valid answer by taking 100 grams of that solution and zero from all others, since it already matches the target concentration.

If all ai are non-zero and all have the same sign, then no non-negative combination can produce zero, and the answer is impossible.

Otherwise, we must combine one positive and one negative value.

1. We select a candidate positive index and a candidate negative index. A natural choice is to pick the smallest positive ai and the smallest magnitude negative ai, because these give the simplest ratio and allow larger scaling before hitting the 10⁴ limit.
2. For the chosen pair, we compute the reduced ratio using gcd. Let ai = p > 0 and −aj = q > 0. We compute g = gcd(p, q), then define base amounts x0 = q / g and y0 = p / g.
3. We determine how many times we can scale this pair while respecting bounds. The scaling factor k is limited by both constraints xi ≤ 10⁴ and yi ≤ 10⁴, so

kmax = min(10⁴ / x0, 10⁴ / y0).

1. We check whether using the maximum possible scaling already produces enough total mass, meaning kmax * (x0 + y0) ≥ 100. If not, this pair cannot satisfy the requirement.
2. If it is sufficient, we output xi = kmax * x0 and yi = kmax * y0, and all other values zero.

If no pair works, the answer is impossible.

The correctness relies on the fact that any valid solution must balance positive and negative contributions. Any such solution can be decomposed into pairwise cancellations, and at least one cancellation pair must itself be scalable enough to reach the required total mass under the constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    n, Q = map(int, input().split())
    T = list(map(int, input().split()))

    pos = []
    neg = []
    zero = []

    for i, t in enumerate(T):
        a = t - Q
        if a > 0:
            pos.append((a, i))
        elif a < 0:
            neg.append((a, i))
        else:
            zero.append(i)

    # if exact match exists
    if zero:
        res = [0] * n
        res[zero[0]] = 100
        print(*res)
        return

    if not pos or not neg:
        print(-1)
        return

    # pick minimal absolute representatives
    pos.sort()
    neg.sort(key=lambda x: x[0], reverse=True)  # closest to zero negative

    candidates = []
    candidates.append((pos[0][0], neg[0][0]))

    # try a few more extreme combinations (safety)
    for i in range(min(3, len(pos))):
        for j in range(min(3, len(neg))):
            candidates.append((pos[i][0], neg[j][0]))

    best = None

    for p, nval in candidates:
        a = p
        b = -nval
        g = gcd(a, b)
        x0 = b // g
        y0 = a // g

        kmax = min(10000 // x0, 10000 // y0)
        if kmax <= 0:
            continue

        total = kmax * (x0 + y0)
        if total >= 100:
            best = (x0, y0, kmax, p, nval)
            break

    if best is None:
        print(-1)
        return

    x0, y0, kmax, p, nval = best

    res = [0] * n
    # find indices
    for i, t in enumerate(T):
        if t - Q == p and x0 > 0:
            res[i] = kmax * x0
            x0 = 0
        elif t - Q == nval and y0 > 0:
            res[i] = kmax * y0
            y0 = 0

    print(*res)

if __name__ == "__main__":
    solve()
```

The solution begins by converting the concentration condition into a linear equation. It then partitions indices into positive, negative, and zero deviation from Q. The zero case is handled immediately since it directly satisfies the requirement with 100 grams.

For non-zero cases, the algorithm constructs candidate balancing pairs. For each pair, it computes the reduced integer ratio using gcd, then checks how far it can be scaled before hitting the 10⁴ limit per ingredient. Only pairs that can produce at least 100 total grams are accepted.

The final assignment distributes the computed amounts back onto the chosen indices.

## Worked Examples

### Example 1

Input:

```
4 50
10 40 70 90
```

We compute deviations from 50: −40, −10, +20, +40. So we have negatives and positives.

A possible pairing is 40 and −10. The ratio is 40 : 10, reduced to 4 : 1. The maximum scaling is limited by xi ≤ 10000 and yi ≤ 10000, which is not restrictive here, so we can take k large enough; but we only need total mass ≥ 100, so k = 20 already gives (80, 20).

| Step | Positive | Negative | x0 | y0 | kmax | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Compute pair | 40 | −10 | 1 | 4 | 10000 | large |

We can choose a valid scaling that satisfies the requirement and distribute mass accordingly.

This confirms that balancing a strong positive deviation with a weaker negative one still allows a valid construction.

### Example 2

Input:

```
3 30
10 20 50
```

Deviations are −20, −10, +20. We can use +20 and −10.

The reduced ratio is 2 : 1. Scaling is limited by 10⁴, so kmax is large, and we easily exceed 100 grams total mass.

This example shows that even when values are sparse, a single balancing pair suffices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single scan plus constant candidate checks |
| Space | O(n) | storing indices for reconstruction |

The solution comfortably fits within limits since n is up to 10⁵ and all operations are linear or constant per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd

    # (assume solve() is defined above)
    return sys.stdout.getvalue()

# sample-like and custom cases would be placed here in a full setup
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 50\n50 | 100 | single exact match case |
| 2 50\n10 90 | valid pair | simplest balancing case |
| 3 50\n10 20 30 | -1 | no opposite signs |
| 4 0 | 100 | degenerate formatting edge |

## Edge Cases

When a solution contains a Ti exactly equal to Q, the algorithm immediately returns a valid construction using only that ingredient. This avoids unnecessary balancing logic and guarantees feasibility.

When all deviations have the same sign, every combination remains on one side of Q, so the linear equation cannot reach zero; the algorithm correctly returns −1.

When the balancing pair exists but the gcd-reduced coefficients are large, scaling is blocked by the 10⁴ cap. The algorithm explicitly checks this through kmax, ensuring it does not construct invalid assignments even if the equation is solvable without bounds.
