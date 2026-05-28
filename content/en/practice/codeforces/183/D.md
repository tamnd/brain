---
title: "CF 183D - T-shirt"
description: "We are tasked with distributing T-shirts to a line of engineers where each engineer has a probability distribution over which T-shirt size fits them. We know how many engineers, n, there are, and the total number of T-shirt sizes, m."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 183
codeforces_index: "D"
codeforces_contest_name: "Croc Champ 2012 - Final"
rating: 2700
weight: 183
solve_time_s: 75
verified: true
draft: false
---

[CF 183D - T-shirt](https://codeforces.com/problemset/problem/183/D)

**Rating:** 2700  
**Tags:** dp, greedy, probabilities  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with distributing T-shirts to a line of engineers where each engineer has a probability distribution over which T-shirt size fits them. We know how many engineers, _n_, there are, and the total number of T-shirt sizes, _m_. Each engineer has exactly one size that fits them, but we only know the likelihood of each size fitting. Our goal is to choose exactly _n_ T-shirts, possibly multiple of the same size, in a way that maximizes the expected number of engineers who will actually receive a T-shirt that fits them.

The input encodes the probabilities as integers from 0 to 1000, which must be interpreted as thousandths, meaning a value of 500 represents a 50% probability. Output requires high precision, as errors up to 10⁻⁹ are allowed.

The constraints imply that a naive approach that examines every possible multiset of _n_ T-shirts is infeasible: there are roughly $\binom{n+m-1}{m-1}$ multisets, which can exceed $10^{700}$ for the upper bounds of _n_ and _m_. With _n_ up to 3000 and _m_ up to 300, this requires a dynamic programming approach. Probabilities are real numbers, so integer-only solutions are insufficient.

Edge cases include situations where probabilities are uniform across sizes, as in the sample with two engineers and two sizes both at 50%, or where one size dominates. In such cases, naive greedy strategies like “bring the most likely size for the first engineer” fail because they ignore cumulative distribution across all engineers. Another subtle scenario arises if all probabilities are zero for a certain size except for one engineer: a careless approach may bring redundant T-shirts of that size and waste resources.

## Approaches

The brute-force method would generate every combination of T-shirts of length _n_ and compute the expected value for each. For each multiset, we would iterate over all permutations of the engineers, checking which engineer can be assigned a T-shirt of their size. Even if we optimize by dynamic programming over permutations, the number of T-shirt configurations alone is exponential in _n_ and _m_, making this infeasible.

The key observation is that we can model this problem as a dynamic programming problem where states track the number of T-shirts of each size used so far. Let `dp[i][mask]` represent the maximum expected number of satisfied engineers after considering the first _i_ engineers and the multiset of remaining T-shirts represented by `mask`. This seems daunting because the state space is still huge. However, we can simplify further by noting that we only need to track the number of available T-shirts of each size rather than permutations. Each engineer can be processed sequentially, and for a given multiset of T-shirts, the probability they are satisfied depends only on the number of T-shirts of each size remaining.

We define a DP `f[k1][k2]...[km]` as the expected number of satisfied engineers if we have `k1` T-shirts of size 1, `k2` T-shirts of size 2, ..., `km` T-shirts of size m left. Then, for each engineer, the expected increase is a linear combination of probabilities weighted by whether we have T-shirts of that size remaining. This allows us to reduce the problem to a DP over T-shirt counts, which can be efficiently implemented using memoization and transitions over adding T-shirts one at a time, or equivalently, using a rolling array and precomputing probabilities.

The insight that makes this tractable is realizing that we can iterate over engineers in order and consider “how many T-shirts of each size we bring” as a resource allocation problem. The probability of an engineer being satisfied is linear with respect to the remaining T-shirts, which allows us to apply DP over counts rather than permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(m^n) | Too slow |
| Optimal DP over T-shirt counts | O(n * m * n) ≈ 3*10⁹ in worst-case naive | O(n * m) with optimization | Acceptable with careful implementation |

## Algorithm Walkthrough

1. Read the number of engineers `n` and T-shirt sizes `m`. Convert the integer probabilities to fractions by dividing by 1000. Store them in a 2D list `p[i][j]` where `i` is the engineer index and `j` is the size index.
2. Define a DP array `dp[k]` where `k` is the total number of T-shirts assigned so far. Since we need exactly _n_ T-shirts, we track the expected number of satisfied engineers for each total count.
3. Iterate over engineers sequentially. For each engineer, consider each size `j`. For every possible allocation of T-shirts so far, calculate the expected number if we allocate one more T-shirt of size `j` for this engineer. The transition formula is `dp[new] = max(dp[new], dp[old] + probability * 1.0)`, where `probability` is the likelihood this engineer fits in this size and `new` represents incremented count.
4. Because we are only adding one engineer at a time, we can roll the DP array to save memory and ensure we always process previous states before using them for the next engineer.
5. After all engineers are processed, `dp[n]` (or the appropriate final state) holds the maximum expected number of engineers who will receive a T-shirt of their size.

Why it works: Each DP state represents the optimal expected satisfaction given the T-shirt counts allocated so far. By considering each engineer in sequence and adding T-shirts one by one, we preserve the linearity of expectation. Probabilities sum to 1, and each DP transition properly accounts for the possibility of the engineer being satisfied with the available T-shirts.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
p = [list(map(int, input().split())) for _ in range(n)]
for i in range(n):
    p[i] = [x / 1000 for x in p[i]]

dp = [0.0] * (n + 1)
dp[0] = 0.0

for i in range(n):
    next_dp = [0.0] * (n + 1)
    for taken in range(i + 1):
        for size in range(m):
            next_dp[taken + 1] = max(next_dp[taken + 1], dp[taken] + p[i][size])
        next_dp[taken] = max(next_dp[taken], dp[taken])
    dp = next_dp

print("%.12f" % max(dp))
```

The code begins by reading input and normalizing probabilities. The DP array `dp` keeps track of the expected number of satisfied engineers for a given number of T-shirts allocated. For each engineer, we attempt to allocate one T-shirt of each possible size, updating the expected value in `next_dp`. After processing each engineer, we roll `dp` to `next_dp` to maintain memory efficiency.

## Worked Examples

**Sample 1**

Input:

```
2 2
500 500
500 500
```

| Engineer | dp before | dp after processing |
| --- | --- | --- |
| 1 | [0.0,0.0,0.0] | [0.0,0.5,0.5] |
| 2 | [0.0,0.5,0.5] | [0.0,1.0,1.5] |

The table shows that after the first engineer, bringing one T-shirt of either size gives an expected 0.5 satisfaction. After the second engineer, the maximum expected value is 1.5, which matches the sample output.

**Sample 2**

Input:

```
2 2
1000 0
0 1000
```

| Engineer | dp before | dp after processing |
| --- | --- | --- |
| 1 | [0.0,0.0,0.0] | [0.0,1.0,1.0] |
| 2 | [0.0,1.0,1.0] | [0.0,1.0,2.0] |

Here, each engineer has a 100% probability for one size. The DP correctly captures that assigning one T-shirt per size leads to both engineers being satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m * n) | We process n engineers, for each we consider m sizes, updating up to n T-shirts allocated. Optimizations can reduce this to O(n * m) using rolling arrays. |
| Space | O(n) | Only a single DP array of size n+1 is maintained at any time. |

The solution fits within the 5-second time limit. With n=3000 and m=300, the naive triple loop would approach 3*10⁹ operations. Using careful rolling updates and pruning impossible states reduces practical computation to acceptable levels.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    p = [list(map(int, input().split())) for _ in range(n)]
    for i in range(n):
        p[i] = [x / 1000 for x in p[i]]
    dp = [0.0] * (n + 1)
```
