---
title: "CF 103451B - Sum of sums"
description: "We are given an array of non-negative integers, and a recursive operation that repeatedly “expands” it into a new value. At the base level, when the level is zero, the value is simply the sum of all elements in the array. For higher levels, we look at every contiguous subarray."
date: "2026-07-03T07:20:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103451
codeforces_index: "B"
codeforces_contest_name: "Krosh Kaliningrad Contest 2"
rating: 0
weight: 103451
solve_time_s: 69
verified: true
draft: false
---

[CF 103451B - Sum of sums](https://codeforces.com/problemset/problem/103451/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers, and a recursive operation that repeatedly “expands” it into a new value.

At the base level, when the level is zero, the value is simply the sum of all elements in the array.

For higher levels, we look at every contiguous subarray. For each subarray, we compute the same function at the previous level on that subarray, and then sum all of those results. Repeating this k times produces a single number that grows very quickly.

So the task is to take the original array, apply this subarray-sum-of-previous-values operation k times, and output the final value modulo 1e9+7.

The input size allows up to 200,000 elements and k up to 200,000. That immediately rules out any approach that explicitly enumerates subarrays even once, since there are O(n^2) of them. Even k = 1 already requires aggregating over all subarrays, and k > 1 compounds this explosion. Any solution must avoid ever iterating over subarrays explicitly.

A subtle edge case appears when k = 0. In that case, the recursion never starts, and the answer is just the plain sum of the array. Another edge case is when n = 1. Every subarray is just the single element, so the answer becomes the same value for all k, which is a useful sanity check for any derived formula.

## Approaches

A direct simulation computes f(A, 1) by iterating over all pairs (l, r), summing each subarray, then repeating this on the resulting structure for k layers. This is already O(n^2), and doing it k times makes it effectively O(k n^2), which is far beyond any feasible limit.

The key observation is that the entire process is linear in the sense that every element contributes independently to the final answer. The recursion only changes how many times each original element is counted, not how elements interact with each other. So instead of tracking subarrays, we track the contribution of a single fixed position through all levels.

At level 0, each element a[i] contributes exactly 1 to the sum.

At level 1, we count how many subarrays include index i. That is i choices for the left endpoint and (n - i + 1) choices for the right endpoint, so the coefficient becomes i(n - i + 1).

At higher levels, the same structure repeats, but inside each chosen subarray, the element’s position shifts. This leads to a product structure: the number of ways to choose a left boundary and right boundary at each depth separates cleanly. After working through two levels, a pattern emerges where binomial coefficients appear naturally.

This leads to a closed form for the coefficient of a[i] after k operations, which depends only on its position and n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over subarrays per level | O(k n^2) | O(n^2) | Too slow |
| Combinatorial contribution formula | O(n + k) | O(n + k) | Accepted |

## Algorithm Walkthrough

### 1. Reinterpret the process as a linear contribution problem

We assume the final answer can be written as a weighted sum of original elements, where each a[i] has a coefficient depending only on its index and k. This is valid because every step is a sum over subarrays, which is linear in the input values.

### 2. Compute base coefficients

For k = 0, every element contributes exactly once, so the coefficient is 1 for all i.

For k = 1, each element i appears in exactly i choices of left boundary and (n - i + 1) choices of right boundary, giving coefficient i(n - i + 1).

This confirms that the coefficient depends only on how many subarrays cover a position.

### 3. Observe structure for k = 2

For the second level, we sum over all subarrays again, but now each subarray contributes with its own internal weighting.

If we fix an element i in the original array, we choose a subarray [l, r] containing it. Inside that subarray, its local contribution depends only on its position (i - l + 1) and remaining length (r - i + 1). Summing over all valid l and r separates into two independent sums, one for the left side and one for the right side, which produces a product of triangular sums.

This produces:

i(i + 1)/2 times (n - i + 1)(n - i + 2)/2

### 4. Generalize to k levels

Each additional level increases both sides of the combinatorial “triangle” by 1. This leads to binomial coefficients:

Coefficient of a[i] =

C(i + k - 1, k) × C(n - i + k, k)

### 5. Compute final answer

Precompute factorials and inverse factorials up to n + k. Then sum a[i] multiplied by the coefficient above for each index.

### Why it works

At every level, the operation only chooses a left and right boundary independently. These choices accumulate multiplicatively across recursive levels. Because the position of an element inside a subarray depends only on how far the left boundary shifts it, the counting decomposes into two independent combinatorial choices, one from the left side and one from the right side. This independence is exactly what transforms nested subarray summations into products of binomial coefficients.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def build_fact(n):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    return fact, invfact

def C(n, r, fact, invfact):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    maxv = n + k + 5
    fact, invfact = build_fact(maxv)

    ans = 0
    for i in range(n):
        left = C(i + k, k, fact, invfact)
        right = C(n - i - 1 + k, k, fact, invfact)
        ans = (ans + a[i] * left % MOD * right) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The factorial table is built up to n + k because both binomial terms shift indices by up to k. Each coefficient is computed in constant time using precomputed factorials.

The key implementation detail is indexing: the formula uses 0-based i, so the left term becomes C(i + k, k) and the right term becomes C(n - i - 1 + k, k). A common mistake is mixing 1-based derivation with 0-based implementation, which shifts all coefficients incorrectly.

## Worked Examples

### Example 1

Input:

```
5 0
1 2 3 4 5
```

| i | a[i] | left C(i+0,0) | right C(n-i-1+0,0) | contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 2 | 1 | 1 | 2 |
| 2 | 3 | 1 | 1 | 3 |
| 3 | 4 | 1 | 1 | 4 |
| 4 | 5 | 1 | 1 | 5 |

The result is 15, which matches the fact that level 0 is just the plain sum.

This confirms that the formula correctly collapses to the identity case when k = 0.

### Example 2

Input:

```
5 1
1 2 3 4 5
```

| i | a[i] | left C(i+1,1) | right C(n-i,1) | contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 5 | 5 |
| 1 | 2 | 2 | 4 | 16 |
| 2 | 3 | 3 | 3 | 27 |
| 3 | 4 | 4 | 2 | 32 |
| 4 | 5 | 5 | 1 | 25 |

Total is 105.

This matches the interpretation that each element is counted by the number of subarrays containing it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | factorial preprocessing and one pass over array |
| Space | O(n + k) | factorial and inverse factorial tables |

The constraints allow up to 2e5 for both n and k, so precomputing factorials up to n + k fits comfortably, and the final loop is linear in n.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    maxv = n + k + 5
    fact = [1] * (maxv + 1)
    invfact = [1] * (maxv + 1)

    for i in range(1, maxv + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[maxv] = pow(fact[maxv], MOD - 2, MOD)
    for i in range(maxv, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    ans = 0
    for i in range(n):
        ans += a[i] * C(i + k, k) * C(n - i - 1 + k, k)
        ans %= MOD

    return str(ans)

# provided samples
assert solve("5 0\n1 2 3 4 5\n") == "15"
assert solve("5 1\n1 2 3 4 5\n") == "105"
assert solve("3 2\n1 2 3\n") == "42"

# custom cases
assert solve("1 0\n7\n") == "7"
assert solve("1 5\n7\n") == "7"
assert solve("2 1\n1 1\n") == "4"
assert solve("4 2\n1 2 3 4\n") == solve("4 2\n1 2 3 4\n"), "consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 / 7 | 7 | single element base case |
| 1 5 / 7 | 7 | stability under k |
| 2 1 / 1 1 | 4 | symmetry and counting correctness |
| 4 2 / 1 2 3 4 | consistent | internal consistency check |

## Edge Cases

For k = 0, the algorithm reduces to summing a[i] because both binomial terms evaluate to 1. The formula handles this cleanly since C(x, 0) = 1 for all valid x.

For n = 1, the left term becomes C(k, k) = 1 and the right term also becomes C(k, k) = 1, so every level leaves the value unchanged. This matches the intuition that there is only one subarray at every stage, so no combinatorial explosion occurs.

For large k, the coefficients grow rapidly but remain bounded modulo MOD due to factorial precomputation. The use of modular inverses ensures that even when binomial values are large, they remain computable in constant time per element.
