---
title: "CF 105434B - \u5168\u6982\u7387\u516c\u5f0f"
description: "We are given several independent data sources, each representing a platform that might contribute to a mixed dataset. Each platform contributes a known fraction of the total data, and each platform also has its own probability of being “AI contaminated”."
date: "2026-06-23T03:51:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105434
codeforces_index: "B"
codeforces_contest_name: "2024\u5e74\u201c\u6838\u6843\u676f\u201d\u6b66\u6c49\u5730\u533aACM\u840c\u65b0\u8d5b"
rating: 0
weight: 105434
solve_time_s: 56
verified: true
draft: false
---

[CF 105434B - \u5168\u6982\u7387\u516c\u5f0f](https://codeforces.com/problemset/problem/105434/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent data sources, each representing a platform that might contribute to a mixed dataset. Each platform contributes a known fraction of the total data, and each platform also has its own probability of being “AI contaminated”.

In more concrete terms, imagine you pick a random piece of data from a huge combined pool. First, a platform is chosen according to its weight in the mixture. Then, within that platform, the data is either clean or AI-generated noise according to a known probability. The task is to compute the overall probability that the randomly chosen piece of data is contaminated.

The input provides two aligned probability distributions. The first describes how likely each platform is to be selected. These probabilities already sum to one, so they form a valid mixture distribution. The second describes, for each platform, the conditional probability that data from that platform is contaminated.

The output is the marginal probability of contamination across the entire mixture.

The constraints are small: at most 100 platforms, so even an O(n) or O(n log n) solution is trivial. The only subtlety is numerical stability, since the answer is a floating-point weighted sum and the required error tolerance is relative, not absolute. This means values close to zero require care, but standard double precision is sufficient.

A common mistake is to treat the probabilities as independent and multiply all values together, or to average the conditional probabilities without weighting. For example, if one platform contributes 99% of the data and another contributes 1%, simply averaging their contamination rates would severely distort the result. The weighting is essential.

A second mistake is forgetting that the platform probabilities already form a complete distribution. Adding normalization steps or re-normalizing can introduce unnecessary floating-point error.

## Approaches

A brute-force interpretation would simulate the two-stage process. One could repeatedly sample a platform according to its probability distribution, then sample whether it is contaminated, and estimate the result via Monte Carlo. While conceptually correct, this approach is unnecessary and imprecise, and even with large numbers of simulations it would only approximate the answer. The variance would also depend on how skewed the probabilities are, and there is no guarantee of meeting the strict relative error requirement.

The key observation is that the probability of contamination is a direct application of the law of total probability. Each platform contributes independently to the final expectation, weighted by how often it is chosen. Instead of simulating, we can compute the exact expectation in one pass by summing contributions of the form “probability of choosing platform i multiplied by probability of contamination given platform i”.

This collapses the entire problem into a single linear aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Monte Carlo Simulation | O(k) for large k samples | O(1) | Too slow / imprecise |
| Weighted Sum (Optimal) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of platforms n. Each platform represents a mutually exclusive source of data, so exactly one will be chosen in the probability model.
2. Read the array f, where f[i] is the probability that a randomly selected data item originates from platform i. These values already sum to 1, so they form a valid mixture distribution.
3. Read the array a, where a[i] is the conditional probability that a data item from platform i is AI contaminated.
4. Initialize an accumulator ans = 0. This will store the total probability of contamination across all platforms.
5. For each platform i from 1 to n, add f[i] * a[i] to ans. This term represents the contribution of platform i to the total probability: first selecting the platform, then observing contamination within it.
6. Output ans as a floating-point number.

The multiplication inside the sum is the crucial modeling step. Each platform contributes proportionally to how often it is chosen, so its contamination rate must be scaled by its selection probability before aggregation.

### Why it works

Let A be the event that a randomly selected data item is contaminated, and Fi be the event that the item comes from platform i. The Fi events form a partition of the sample space. By the law of total probability, P(A) equals the sum over all i of P(Fi) multiplied by P(A | Fi). The algorithm computes exactly this decomposition, with no approximation or hidden assumptions. Since all Fi are disjoint and exhaustive, no probability mass is double-counted or omitted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    f = list(map(float, input().split()))
    a = list(map(float, input().split()))

    ans = 0.0
    for i in range(n):
        ans += f[i] * a[i]

    print(ans)

if __name__ == "__main__":
    main()
```

The solution is a direct implementation of the weighted sum. The only detail worth attention is using floating-point arithmetic throughout. Since n is small, there is no need for optimization beyond a simple loop.

The multiplication is performed before accumulation, which is the numerically stable ordering for this size of input. There is no need for normalization or scaling because inputs already define a valid probability distribution.

## Worked Examples

Consider the sample input where two platforms contribute 0.4 and 0.6 of the data, and their contamination probabilities are 0.6 and 0.3 respectively.

| i | f[i] | a[i] | contribution |
| --- | --- | --- | --- |
| 1 | 0.4 | 0.6 | 0.24 |
| 2 | 0.6 | 0.3 | 0.18 |

The sum becomes 0.42.

This trace shows how heavily the second platform influences the result despite its lower contamination rate, purely because it dominates the data distribution.

Now consider a skewed case: one platform dominates almost completely.

Input:

f = [0.99, 0.01]

a = [0.0, 1.0]

| i | f[i] | a[i] | contribution |
| --- | --- | --- | --- |
| 1 | 0.99 | 0.0 | 0.0 |
| 2 | 0.01 | 1.0 | 0.01 |

The result is 0.01, showing that a rare but heavily contaminated source contributes only proportionally to its frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over n platforms computing a weighted sum |
| Space | O(1) | Only constant extra storage beyond input arrays |

The constraints allow up to 100 platforms, so the linear scan is effectively instantaneous. Floating-point operations dominate, but even these are negligible at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    f = list(map(float, input().split()))
    a = list(map(float, input().split()))

    ans = 0.0
    for i in range(n):
        ans += f[i] * a[i]

    return str(ans)

# provided sample
assert abs(float(run("2\n0.4 0.6\n0.6 0.3\n")) - 0.42) < 1e-9

# all clean
assert abs(float(run("3\n0.2 0.3 0.5\n0.0 0.0 0.0\n")) - 0.0) < 1e-9

# all contaminated
assert abs(float(run("3\n0.2 0.3 0.5\n1.0 1.0 1.0\n")) - 1.0) < 1e-9

# single platform
assert abs(float(run("1\n1.0\n0.37\n")) - 0.37) < 1e-9

# skewed distribution
assert abs(float(run("2\n0.999 0.001\n0.2 0.9\n")) - (0.999*0.2 + 0.001*0.9)) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 0.42 | basic correctness |
| all zeros | 0 | degenerate contamination |
| all ones | 1 | full contamination boundary |
| single platform | 0.37 | minimal structure |
| skewed | weighted sum | precision under imbalance |

## Edge Cases

A key edge case is when one platform has probability 1 and all others are 0. In that situation, the answer should exactly match that platform’s contamination probability. The algorithm handles this naturally because all zero-weight terms vanish, leaving only one contribution.

Another case is when contamination probabilities are all zero. The computation becomes a sum of zeros regardless of platform weights, producing zero as expected.

A third case is when all contamination probabilities are one. The result collapses to the sum of f[i], which is guaranteed to be 1 because the input distribution is normalized. The algorithm therefore produces exactly 1 without special handling.

Finally, when probabilities are extremely close to zero or one, floating-point rounding might introduce tiny errors, but the required relative error tolerance allows standard double precision accumulation to pass safely.
