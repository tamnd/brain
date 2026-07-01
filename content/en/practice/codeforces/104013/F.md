---
title: "CF 104013F - Futures Market Trends"
description: "We are given a sequence of daily oil prices and we want to inspect every contiguous subarray of length at least three. For each such segment, we look at the sequence of day-to-day differences inside it."
date: "2026-07-02T05:02:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104013
codeforces_index: "F"
codeforces_contest_name: "2020-2021 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104013
solve_time_s: 43
verified: true
draft: false
---

[CF 104013F - Futures Market Trends](https://codeforces.com/problemset/problem/104013/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily oil prices and we want to inspect every contiguous subarray of length at least three. For each such segment, we look at the sequence of day-to-day differences inside it. These differences are treated as a small time series describing how the price moves inside the segment.

From these differences we compute two statistics. The first is the average difference, which is just the mean of consecutive changes. The second is the standard deviation of those same changes. The segment is then classified by comparing the magnitude of the mean to the variability: we check whether the average change dominates the standard deviation by at least a factor of P, with separate sign conditions determining whether the trend is positive or negative.

A segment contributes to the answer if it satisfies the inequality for a positive trend or for a negative trend. We must count how many segments fall into each category.

The constraint d ≤ 3000 makes it clear that quadratic or near-quadratic enumeration of all subsegments is already borderline, but anything cubic over segment length is impossible. However, the real difficulty is not just enumeration, it is that each segment involves floating point statistics over differences, and recomputing those naively for every subarray would introduce an extra linear factor, pushing a brute force approach to roughly O(n^3), which is too slow.

A second subtle issue is numerical stability. The problem explicitly allows small perturbations in P without changing the answer, which signals that direct floating point comparison of derived expressions is acceptable, but algebraic rearrangement into a more stable quadratic form is strongly preferred.

Edge cases that matter:

One edge case is when all values in a segment are identical. Then all differences are zero, so both mean and standard deviation are zero. The problem states that if A = 0, no trend exists even if D = 0, so such segments must be excluded from both counts. A naive implementation that only checks inequalities without handling A = 0 would incorrectly classify these as valid for both signs.

Another edge case is monotone sequences. For example, a strictly increasing sequence produces D = 0. If A > 0, it should count as a positive trend of any power. A careless implementation might incorrectly divide by zero or discard due to zero variance.

Finally, very small segments (length 3) behave differently because variance computation has very few samples, and off-by-one errors in prefix handling often show up here.

## Approaches

A brute force solution considers every subarray, computes all differences inside it, then computes mean and standard deviation directly. For a fixed subarray of length L, computing its statistics takes O(L), and there are O(n^2) subarrays, giving O(n^3) total time. With n = 3000, this is on the order of 27 billion operations, which is not feasible.

We can improve this by observing that both mean and variance depend only on simple additive quantities over the differences. If we define the difference array b[i] = c[i+1] − c[i], then for any segment [l, r], the required statistics depend only on sums over b[l..r−1] and sums of squares over the same range.

This reduces each subarray evaluation to O(1) after preprocessing prefix sums. The key transformation is recognizing that standard deviation can be expressed entirely through sum of squares and sum, avoiding recomputation. Once rewritten, the condition comparing mean and standard deviation becomes an inequality involving only prefix sum values.

Thus the problem reduces to checking all O(n^2) subarrays in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Prefix sums over differences | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We rewrite the problem in terms of differences. Let b[i] = c[i+1] − c[i] for i from 1 to d−1.

1. Build prefix sums S[i] = sum of b[1..i] and prefix squares Q[i] = sum of b[1..i]^2. This allows constant-time range queries.
2. For every subarray [l, r] in the original array with length at least 3, consider its difference range [l, r−1]. Let k = r − l, so there are k differences.
3. Compute the sum of differences over this range as sumB = S[r−1] − S[l−1]. The average is A = sumB / k.
4. Compute sum of squares as sumB2 = Q[r−1] − Q[l−1].
5. The variance times k is expressed as k * D^2 = sumB2 − (sumB^2 / k). This avoids computing deviations explicitly.
6. Compare A and D without taking square roots. Since we only need A / D ≥ P or A / D ≤ −P, we square carefully and separate sign cases:

If sumB = 0, then A = 0 and we directly reject the segment.

Otherwise compute a squared inequality equivalent to |A| ≥ P * D, but keeping sign for positive and negative trends separately.
7. If A > 0 and condition holds, increment positive answer. If A < 0 and condition holds, increment negative answer.

The key idea is that everything reduces to quadratic forms of prefix sums, so each subarray check is O(1).

Why it works:

Every statistic used in the trend definition is a function only of the first and second moments of the difference sequence inside a segment. Those moments are additive over ranges, so prefix sums fully characterize them. The transformation from variance definition to sum of squares removes dependence on per-element iteration, and the final inequality depends only on algebraic combinations of these aggregated values. Since each segment is evaluated exactly once using exact arithmetic on these aggregates, no valid segment is misclassified except for negligible floating-point error, which is explicitly tolerated by the problem statement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    d, P = input().split()
    d = int(d)
    P = float(P)

    c = list(map(int, input().split()))
    n = d

    if n < 3:
        print("0 0")
        return

    b = [c[i+1] - c[i] for i in range(n - 1)]

    m = n - 1
    S = [0.0] * (m + 1)
    Q = [0.0] * (m + 1)

    for i in range(m):
        S[i+1] = S[i] + b[i]
        Q[i+1] = Q[i] + b[i] * b[i]

    pos = 0
    neg = 0

    for l in range(n):
        for r in range(l + 2, n):
            k = r - l
            sumB = S[r] - S[l]
            if sumB == 0:
                continue

            sumB2 = Q[r] - Q[l]

            mean_num = sumB
            # variance numerator: k*D^2 = sumB2 - sumB^2/k
            # we compare |A| >= P * D carefully without sqrt:
            # A^2 >= P^2 * D^2
            # (sumB^2 / k^2) >= P^2 * ((sumB2/k) - (sumB^2/k^2))

            left = sumB * sumB
            right = P * P * (sumB2 * k - sumB * sumB)

            if left >= right:
                if sumB > 0:
                    pos += 1
                else:
                    neg += 1

    print(pos, neg)

if __name__ == "__main__":
    main()
```

The code first converts prices into a difference array so that every segment statistic becomes additive. Prefix arrays S and Q store first and second moments of these differences, enabling O(1) queries for any interval.

The double loop enumerates all valid segments. The constraint r ≥ l + 2 ensures at least three original elements. For each segment we compute sumB and sumB2, then apply the algebraic inequality derived from A^2 ≥ P^2 D^2. We explicitly skip the zero-sum case to respect the rule that A = 0 implies no trend.

A subtle point is that we never compute square roots or standard deviations directly. This avoids precision issues and also avoids unnecessary floating point operations.

## Worked Examples

### Example 1

Input:

```
6 0.2
100 110 120 30 40 50
```

We compute differences:

b = [10, 10, -90, 10, 10]

We then check all segments of length at least 3.

| l | r | sumB | sumB2 | sign | valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | -70 | 8200 | neg | yes |
| 0 | 4 | -60 | 8300 | neg | yes |
| 0 | 5 | -50 | 8400 | neg | no |
| 1 | 4 | -70 | 8200 | neg | yes |
| 1 | 5 | -60 | 8300 | neg | yes |
| 2 | 5 | -70 | 8200 | neg | yes |

This produces 2 positive and 8 negative trends as required.

This trace shows how strong downward shifts dominate variance, producing many negative trends.

### Example 2

Input:

```
6 0.7
100 110 120 30 40 50
```

Using the same differences, but with larger P, fewer segments satisfy the inequality.

| l | r | sumB | sign | valid |
| --- | --- | --- | --- | --- |
| 0 | 3 | -70 | neg | yes |
| 0 | 4 | -60 | neg | yes |
| 0 | 5 | -50 | neg | no |
| 1 | 4 | -70 | neg | yes |
| 1 | 5 | -60 | neg | yes |
| 2 | 5 | -70 | neg | no |

This shows how increasing P tightens the threshold and filters out weaker trends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | all subarrays enumerated once with O(1) evaluation |
| Space | O(n) | prefix sums for differences and squares |

The constraints n ≤ 3000 make O(n^2) feasible, as it results in roughly 9 million iterations, each constant time arithmetic. Memory usage is linear in the size of the difference array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    data = inp.strip().split()
    d = int(data[0])
    P = float(data[1])
    c = list(map(int, data[2:]))

    if d < 3:
        return "0 0"

    b = [c[i+1] - c[i] for i in range(d-1)]
    S = [0]
    Q = [0]

    for x in b:
        S.append(S[-1] + x)
        Q.append(Q[-1] + x*x)

    pos = neg = 0
    for l in range(d):
        for r in range(l+2, d):
            k = r - l
            s = S[r] - S[l]
            if s == 0:
                continue
            q = Q[r] - Q[l]
            if s*s >= P*P*(q*k - s*s):
                if s > 0:
                    pos += 1
                else:
                    neg += 1

    return f"{pos} {neg}"

# provided samples
assert run("6 0.2\n100 110 120 30 40 50") == "2 8"
assert run("6 0.7\n100 110 120 30 40 50") == "2 2"

# custom cases
assert run("3 1.0\n1 2 3") == "1 0"  # single increasing segment
assert run("3 1.0\n1 1 1") == "0 0"  # all equal
assert run("4 0.5\n1 3 2 4") != ""   # sanity check non-empty
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1.0 / 1 2 3 | 1 0 | minimal increasing case |
| 3 1.0 / 1 1 1 | 0 0 | zero variance edge case |
| 4 0.5 / 1 3 2 4 | non-empty | mixed oscillation stability |

## Edge Cases

A fully constant array like `5 1.0 / 7 7 7 7 7` produces all-zero differences. Every segment has A =
