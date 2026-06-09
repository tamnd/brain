---
title: "CF 1859C - Another Permutation Problem"
description: "We are given a permutation of the numbers from 1 to n. For a permutation p, define $$text{cost}(p)=sum{i=1}^{n} pi cdot i-max{i=1}^{n}(picdot i).$$ The task is to find the largest possible value of this expression among all permutations of length n."
date: "2026-06-09T00:27:42+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1859
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 892 (Div. 2)"
rating: 1200
weight: 1859
solve_time_s: 168
verified: true
draft: false
---

[CF 1859C - Another Permutation Problem](https://codeforces.com/problemset/problem/1859/C)

**Rating:** 1200  
**Tags:** brute force, dp, greedy, math  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`. For a permutation `p`, define

$$\text{cost}(p)=\sum_{i=1}^{n} p_i \cdot i-\max_{i=1}^{n}(p_i\cdot i).$$

The task is to find the largest possible value of this expression among all permutations of length `n`.

The first term rewards placing large numbers at large indices because it is a weighted sum. The second term subtracts the single largest contribution. These two objectives compete with each other. We would like the total weighted sum to be large, but we would also like the largest individual product not to become too dominant.

The constraint `n ≤ 250` is unusually small for a permutation problem. A brute force search over all permutations is impossible because there are `n!` permutations. Even for `n = 10`, there are already more than three million permutations. On the other hand, the small value of `n` suggests that an `O(n²)` or even `O(n³)` solution per test case is completely acceptable.

A subtle point is that maximizing the weighted sum alone is easy. By the rearrangement inequality, the maximum value of

$$\sum p_i i$$

is obtained by the sorted permutation `[1,2,...,n]`. However, that arrangement also creates the largest possible product `n²`, which is then subtracted. The optimal answer comes from balancing these two effects.

Consider `n = 4`.

The identity permutation gives

$$1\cdot1+2\cdot2+3\cdot3+4\cdot4=30$$

and the maximum product is `16`, so the cost is `14`.

The optimal permutation is `[1,2,4,3]`, whose cost is `17`.

A solution that only maximizes the weighted sum would miss the optimum.

Another easy mistake is assuming the largest product must occur at position `n`. For example, in `[1,4,2,3]`, the largest product is `4·2 = 8`, not necessarily the last position. Any correct solution must compute the maximum product explicitly.

## Approaches

The most direct idea is to enumerate every permutation, compute its weighted sum and largest product, then keep the best answer.

This works because the definition of the cost is straightforward. For a fixed permutation, evaluating the expression takes `O(n)` time.

The problem is the number of permutations. The worst case would require examining `250!` permutations, a number so large that it is completely infeasible.

The key observation is that the official solution relies on a very small search space of specially structured permutations.

Suppose we start from the increasing permutation

$$[1,2,3,\dots,n].$$

This arrangement maximizes the weighted sum. To reduce the penalty from the largest product, we can move some large values away from the largest indices.

A remarkable fact is that an optimal permutation can always be obtained by choosing a split position `k` and constructing

$$[1,2,\dots,k-1,n,n-1,\dots,k].$$

The prefix remains increasing, while the suffix is reversed.

Since `n ≤ 250`, we can simply try every possible split position. For each candidate permutation we compute its cost directly and take the maximum.

There are only `n` candidate permutations, each requiring `O(n)` work to evaluate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all permutations | O(n·n!) | O(n) | Too slow |
| Enumerate split positions | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, initialize the answer to zero.
2. For every split position `k` from `1` to `n`, construct the permutation:

$$[1,2,\dots,k-1,n,n-1,\dots,k].$$
3. Compute the weighted sum

$$\sum p_i\cdot i.$$
4. Compute the largest value among all products `p_i · i`.
5. The cost of this permutation is the weighted sum minus the largest product.
6. Update the answer with the maximum cost seen so far.
7. After checking all split positions, print the answer.

### Why it works

The increasing permutation maximizes the weighted sum. Any optimal solution must stay close to that arrangement because losing too much weighted sum is expensive.

The only significant freedom is deciding which large values should be moved away from the largest indices to reduce the maximum product. Reversing a suffix achieves exactly that tradeoff. The editorial observation for this problem is that every optimal solution belongs to this family of suffix-reversed permutations.

Since we explicitly evaluate every member of that family, the maximum cost found is the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans_list = []

    for _ in range(t):
        n = int(input())
        best = 0

        for k in range(1, n + 1):
            p = list(range(1, k))
            p.extend(range(n, k - 1, -1))

            total = 0
            mx = 0

            for i, x in enumerate(p, start=1):
                prod = i * x
                total += prod
                if prod > mx:
                    mx = prod

            best = max(best, total - mx)

        ans_list.append(str(best))

    sys.stdout.write("\n".join(ans_list))

solve()
```

The outer loop iterates over test cases. For each split position `k`, we generate the candidate permutation described above.

The computation of the cost is done in a single scan. We accumulate the weighted sum and simultaneously track the largest product.

The maximum answer across all candidates is reported.

The implementation uses 1-based indexing through `enumerate(..., start=1)` because the formula uses positions numbered from one.

Integer overflow is not a concern in Python. The largest weighted sum is on the order of

$$250 \cdot 250^2 = 15{,}625{,}000,$$

which is tiny compared to Python's integer limits.

## Worked Examples

### Example 1

Input:

```
2
```

There are two candidate permutations.

| k | Permutation | Weighted Sum | Max Product | Cost |
| --- | --- | --- | --- | --- |
| 1 | [2,1] | 4 | 2 | 2 |
| 2 | [1,2] | 5 | 4 | 1 |

The best cost is `2`.

Output:

```
2
```

This example shows that the identity permutation is not always optimal.

### Example 2

Input:

```
4
```

| k | Permutation | Weighted Sum | Max Product | Cost |
| --- | --- | --- | --- | --- |
| 1 | [4,3,2,1] | 20 | 6 | 14 |
| 2 | [1,4,3,2] | 25 | 9 | 16 |
| 3 | [1,2,4,3] | 29 | 12 | 17 |
| 4 | [1,2,3,4] | 30 | 16 | 14 |

The maximum value is `17`.

Output:

```
17
```

This demonstrates the central tradeoff. The identity permutation maximizes the weighted sum, but a slightly modified arrangement reduces the penalty enough to produce a larger final answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test case | `n` split positions, each evaluated in `O(n)` |
| Space | O(n) | Storage of one candidate permutation |

The maximum value of `n` is only `250`, and the sum of all `n` values is at most `500`. An `O(n²)` solution performs at most about `125,000` operations across all candidates, which is easily
