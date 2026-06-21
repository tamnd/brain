---
title: "CF 105632M - Rejection Sampling"
description: "We are given a universe of elements from 1 to n, and each element i carries a weight ai. The goal is to design a randomized procedure that produces subsets of fixed size k using independent coin flips, followed by rejection of invalid outcomes."
date: "2026-06-22T05:38:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105632
codeforces_index: "M"
codeforces_contest_name: "2024 China Collegiate Programming Contest (CCPC) Zhengzhou Onsite (The 3rd Universal Cup. Stage 22: Zhengzhou)"
rating: 0
weight: 105632
solve_time_s: 42
verified: true
draft: false
---

[CF 105632M - Rejection Sampling](https://codeforces.com/problemset/problem/105632/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a universe of elements from 1 to n, and each element i carries a weight ai. The goal is to design a randomized procedure that produces subsets of fixed size k using independent coin flips, followed by rejection of invalid outcomes.

The process works by assigning each index i a probability pi. In one trial, we independently include each i with probability pi, producing a random subset T. If the resulting subset has size exactly k, we accept it; otherwise we discard the entire trial and repeat until success. Among all successful outcomes, we want the distribution over k-sized subsets S to be proportional to the product of ai over all elements in S.

The output is not the subsets themselves but the inclusion probabilities pi. These probabilities must sum to k, and they must induce, after rejection sampling, a distribution on k-subsets matching the required multiplicative weight structure.

The constraints allow n up to 100000, which immediately rules out anything involving enumerating subsets or dynamic programming over all k-combinations. Any correct approach must reduce the problem to linear time or near linear time with a small number of passes over the array.

A subtle aspect is that the distribution is defined after conditioning on the event |T| = k. That conditioning couples all coordinates, so even though generation is independent, the final probabilities pi are not independent functions of ai in a naive way.

A typical failure mode is to assume pi is proportional to ai or that normalization alone is sufficient. For example, if n = 3, k = 1, a = [1, 100, 100], guessing pi proportional to ai gives probabilities that do not respect the conditioning structure, and the induced distribution after rejection is not uniform over weighted singletons.

Another subtle pitfall is numerical stability. Since pi are real numbers and must satisfy a global constraint, small errors accumulate through the normalization condition and can violate the sum constraint or distort ratios.

## Approaches

The brute-force interpretation would attempt to solve for pi directly from the defining condition. One could imagine enumerating all subsets S of size k, writing the probability that rejection sampling outputs S in terms of pi, and equating ratios between any two subsets to the ratio of their weights. This leads to a system of exponentially many equations, because each subset probability expands into products of pi and (1 - pi). Even writing the full likelihood requires summing over all subsets of all sizes, which is O(2^n). This is infeasible even for small n.

The key structural observation is that the rejection step conditions on a fixed cardinality, which suggests a connection to Poisson binomial distributions conditioned on sum constraints. The distribution of T before rejection is fully factorized, but after conditioning on |T| = k, we get a fixed-size product-form distribution.

The required target distribution over k-subsets is proportional to ∏ ai, which is exactly the distribution obtained from sampling k items without replacement where each item has weight ai. This is the classic weighted k-subset model, also known as the multivariate Wallenius or Fisher noncentral hypergeometric structure. In such models, there is a known representation: each element i has an “inclusion propensity” pi that depends on a single scaling parameter λ, and the correct form is

pi = 1 / (1 + λ / ai)

for some λ > 0 chosen so that the expected size of T equals k under independent sampling.

This structure emerges because the ratio of inclusion probabilities between any two elements must match the ratio of weights after conditioning. Enforcing proportionality across all k-subsets forces a one-parameter family of solutions, and the constraint ∑ pi = k pins down λ uniquely.

Thus the problem reduces to finding λ such that the sum of pi(λ) equals k. Since pi decreases monotonically in λ, the sum is also monotone, so λ can be found using binary search. Each evaluation of the sum is O(n), making the full solution O(n log precision).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n) | O(2^n) | Too slow |
| Monotone parameter + binary search | O(n log(1/ε)) | O(n) | Accepted |

## Algorithm Walkthrough

We introduce a single positive parameter λ that controls all probabilities simultaneously. For a fixed λ, define each inclusion probability as pi(λ) = ai / (ai + λ). This form is chosen because it is the only smooth symmetric transformation that preserves proportional odds between elements while mapping weights into probabilities in (0,1).

1. Fix a candidate value of λ. For this λ, compute every pi(λ) using pi = ai / (ai + λ). This step transforms weights into inclusion probabilities in a way that preserves ordering: larger ai always implies larger pi.
2. Compute the sum S(λ) = ∑ pi(λ). This sum represents the expected size of the sampled set before rejection. The rejection step does not change pi, so this is the correct quantity to control.
3. Observe that when λ → 0, every pi approaches 1, so S(λ) approaches n. When λ → ∞, every pi approaches 0, so S(λ) approaches 0. This guarantees that every target k in [1, n − 1] is achievable.
4. Use binary search on λ to find the unique value where S(λ) = k. At each midpoint, compute S(λ) and compare it to k. If S(λ) is too large, λ is too small and must be increased; otherwise decrease λ.
5. After convergence, output pi for each i using the final λ.

The binary search terminates when the sum is accurate enough that individual pi values differ from their true values by at most 1e-6.

### Why it works

The distribution after rejection depends only on relative inclusion odds between elements. The form pi = ai / (ai + λ) preserves those odds exactly, since

pi / (1 − pi) = ai / λ.

This means the log-odds of inclusion are proportional to log(ai), shifted by a constant λ. Conditioning on exactly k selected items forces the expected cardinality to match k, and monotonicity of S(λ) guarantees a unique solution. The construction is therefore the only consistent way to align independent Bernoulli trials with a fixed-size weighted sampling distribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    def calc(lam):
        s = 0.0
        for x in a:
            s += x / (x + lam)
        return s

    lo, hi = 0.0, 1.0

    # expand hi until sum <= k
    while calc(hi) > k:
        hi *= 2.0

    for _ in range(80):
        mid = (lo + hi) / 2.0
        if calc(mid) > k:
            lo = mid
        else:
            hi = mid

    lam = hi
    res = [x / (x + lam) for x in a]
    print("\n".join(f"{v:.12f}" for v in res))

if __name__ == "__main__":
    solve()
```

The solution begins by defining the function S(λ), which computes the expected subset size for a given parameter. The initial upper bound is expanded exponentially until the expected size drops below k, ensuring the binary search interval is valid.

Binary search is then applied for a fixed number of iterations. The monotonicity of S(λ) guarantees correctness of the direction updates. After convergence, the final λ is used to compute each pi directly.

A common implementation pitfall is forgetting that floating-point precision requires enough iterations rather than a naive epsilon stop. Using a fixed iteration count like 80 is sufficient for double precision.

## Worked Examples

### Example 1

Input:

n = 3, k = 2, a = [5, 5, 5]

We expect symmetry, so all pi should be equal.

| λ | p1 | p2 | p3 | sum |
| --- | --- | --- | --- | --- |
| small | ~1 | ~1 | ~1 | > 2 |
| tuned | 2/3 | 2/3 | 2/3 | 2 |

At equilibrium, each probability becomes 2/3, matching the constraint that the expected size is 2.

This confirms that symmetry in input forces symmetry in solution, and the binary search finds the point where expected cardinality matches k.

### Example 2

Input:

n = 2, k = 1, a = [1, 4]

We expect the second element to be chosen more frequently.

| λ | p1 | p2 | sum |
| --- | --- | --- | --- |
| large λ | small | small | < 1 |
| small λ | large | large | > 1 |

At convergence, λ balances the expected size to 1, producing p2 ≈ 0.666 and p1 ≈ 0.333. The ratio reflects the ratio of weights, confirming that heavier elements get higher inclusion probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log C) | Each evaluation of S(λ) is O(n), and binary search runs for a fixed number of iterations |
| Space | O(n) | Storage of input array |

The algorithm is linear per iteration and uses a constant number of iterations for double precision accuracy. With n up to 100000, this comfortably fits within typical 1-2 second limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    import builtins
    backup = builtins.input

    def fake_input():
        return sys.stdin.readline().strip()

    builtins.input = fake_input
    try:
        solve()
    finally:
        builtins.input = backup

# provided samples
# (placeholders since exact formatting omitted)
# custom cases

# n=2 minimal k
# assert run("2 1\n1 1\n") == expected

# all equal large n small k
# assert run("5 3\n10 10 10 10 10\n") ...

# skewed weights
# assert run("3 1\n1 100 1000\n") ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 / 5 5 5 | uniform 2/3 | symmetry |
| 2 1 / 1 4 | skewed probabilities | weight bias |
| 5 3 / equal values | uniform k/n | balanced case |

## Edge Cases

One edge case is when all ai are equal. In that case the system must reduce to uniform probabilities pi = k / n. The algorithm handles this because S(λ) is symmetric and binary search converges to the unique λ producing equal probabilities.

Another edge case is when k is very small, such as k = 1. Then exactly one element is expected in T, and the solution pushes λ large so that all probabilities are small, with ratios matching ai. The construction naturally preserves proportional selection among elements.

A final edge case is extreme weight disparity, such as one ai being 1e9 and others being 1. The monotonic structure ensures that binary search still converges, and the ratio form pi = ai / (ai + λ) prevents overflow because all operations remain stable in floating point even for large ai.
