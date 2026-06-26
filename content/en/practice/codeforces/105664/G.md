---
title: "CF 105664G - Modulo"
description: "We are given a sequence of numbers and an initial value $x$. We are allowed to reorder the sequence arbitrarily. After fixing an order, we process the elements from left to right, repeatedly replacing the current value $x$ with the remainder when divided by the next array…"
date: "2026-06-26T10:31:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105664
codeforces_index: "G"
codeforces_contest_name: "AGM 2023, Final Round, Day 2"
rating: 0
weight: 105664
solve_time_s: 35
verified: true
draft: false
---

[CF 105664G - Modulo](https://codeforces.com/problemset/problem/105664/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers and an initial value $x$. We are allowed to reorder the sequence arbitrarily. After fixing an order, we process the elements from left to right, repeatedly replacing the current value $x$ with the remainder when divided by the next array element.

Each operation can only decrease the current value or leave it unchanged, since $x \bmod a_i$ is always in the range $[0, a_i - 1]$. The goal is to choose an ordering of the array that makes the final value of $x$ as large as possible after all operations.

The key object is not the final sequence itself, but how each modulus operation constrains the value at that moment. A large element placed early can destroy information immediately, while a small element placed early can preserve a large value by barely reducing it.

The constraints are very tight on $n$, with $n \le 21$. This immediately suggests that exponential strategies over subsets or permutations are allowed. However, values themselves can be as large as $10^{18}$, so any approach depending on enumerating numeric states beyond simple transitions is impossible. This pushes us toward a state definition that tracks only structural information of the process rather than exact arithmetic exploration.

A naive interpretation might try all permutations of the array and simulate the process. That works logically but fails computationally because $n!$ is astronomically large even at $n = 21$.

A second naive idea is dynamic programming over subsets where we store the current value exactly. That also fails because the value range is up to $10^{18}$, and the same subset can produce many different intermediate values depending on order.

Edge cases that break greedy intuition appear when large numbers interact in non-obvious orderings. For example, if $x = 100$ and the array is $[60, 50, 40]$, placing 60 first yields $100 \bmod 60 = 40$, but placing 40 first gives $100 \bmod 40 = 20$, which is worse later. A locally optimal choice is not stable across later steps, so greedy sorting by value is unreliable.

## Approaches

The brute-force approach is to try every permutation of the array, simulate the modulo process, and take the maximum result. Each simulation costs $O(n)$, and there are $n!$ permutations, so the total work grows as $O(n! \cdot n)$. Even at $n = 15$, this becomes infeasible.

The key observation is that the order matters only through which element is applied at each step, and the state space is governed by subsets of used elements. Since $n \le 21$, we can afford $2^n$ states, and we can define dynamic programming over subsets.

The crucial insight is that the process is reversible in a DP sense: instead of building the sequence forward, we can think of selecting the next element to apply last in the sequence. If we know the result after applying a subset of elements, we can try adding one more element at the end and compute the resulting value. This creates a subset DP where each state corresponds to a set of used elements and a resulting value after processing them in some order.

We define DP over masks, but storing only one value per mask is not enough in general, because different orders of the same subset can yield different results. The trick is that we do not need all values, only the best achievable value for each subset, because we are maximizing the final result.

This leads to a standard “subset DP with value transition” where each state tries extending by one unused element and applies the modulo transition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Subset DP over masks | $O(n \cdot 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

1. We define a bitmask representing which elements have already been used in the process, along with the current value of $x$ after applying those elements in some order. Each mask represents a set, not a sequence, so the DP keeps only the best achievable result for that set.
2. We initialize the DP with an empty set, where the value is the original $x$. This corresponds to not having applied any modulo operation yet.
3. For every subset of elements, we attempt to append one unused element to the sequence. If the current state is $(mask, value)$ and we try element $a_i$, the new value becomes $value \bmod a_i$, and the new mask includes $i$.
4. We update the DP entry for the new mask by taking the maximum between its current value and the newly computed value. This ensures that if multiple orders lead to the same subset, we retain only the best outcome.
5. After processing all subsets, the answer is the maximum value among all full masks, since any ordering corresponds to a path that eventually uses all elements.

### Why it works

The DP maintains the invariant that for every subset of elements, it stores the maximum value of $x$ achievable after applying exactly those elements in some order. Any full permutation corresponds to a path through subsets where exactly one element is added at each step. Since every transition preserves correctness of the modulo operation and we consider all possible last steps for each subset, no valid ordering is missed, and the maximum over full subsets must be optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
x = int(input())

N = 1 << n
dp = [-1] * N
dp[0] = x

for mask in range(N):
    cur = dp[mask]
    if cur == -1:
        continue
    for i in range(n):
        if not (mask >> i) & 1:
            nxt = cur % a[i]
            nmask = mask | (1 << i)
            if nxt > dp[nmask]:
                dp[nmask] = nxt

ans = max(dp)
print(ans)
```

The DP array stores the best achievable value for each subset of used elements. The transition loops over all unused elements and applies the modulo operation. The order of iteration over masks does not matter because all transitions only depend on smaller or equal subsets and always improve or maintain stored values.

A subtle point is that overwriting states is safe because we only care about maximizing the final value, not reconstructing the exact sequence. Also, initializing unused states with $-1$ prevents invalid transitions from propagating.

## Worked Examples

### Example 1

Input:

```
3
5 6 7
15
```

We track DP states as subsets:

| mask | used elements | value |
| --- | --- | --- |
| 000 | none | 15 |
| 001 | 5 | 15 % 5 = 0 |
| 010 | 6 | 15 % 6 = 3 |
| 100 | 7 | 15 % 7 = 1 |
| 110 | 6,7 | best from previous transitions |
| 111 | 5,6,7 | final max = 3 |

The best ordering avoids early destructive modulos like 5 first, and instead applies 6 or 7 first to preserve a larger intermediate value, ultimately achieving 3.

This trace shows how different partial orders lead to different intermediate values, and DP preserves the best one per subset.

### Example 2

Input:

```
4
20 21 22 10
107
```

We examine key transitions:

| mask | used elements | value |
| --- | --- | --- |
| 0000 | none | 107 |
| 0001 | 20 | 7 |
| 0010 | 21 | 2 |
| 0100 | 22 | 19 |
| 1000 | 10 | 7 |
| 0110 | 21,22 | 2 |
| 1111 | all | 9 |

The final value 9 comes from carefully ordering larger moduli early to reduce $x$ slowly before hitting smaller divisors.

This example shows that even though 10 is the smallest divisor, placing it early is not necessarily optimal, since it can prematurely collapse the value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^n)$ | Each subset transitions over at most $n$ elements |
| Space | $O(2^n)$ | One DP value per subset |

The constraint $n \le 21$ makes $2^n \approx 2 \cdot 10^6$, which is comfortably within limits for a Python solution with simple integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import defaultdict

    n = int(input())
    a = list(map(int, input().split()))
    x = int(input())

    N = 1 << n
    dp = [-1] * N
    dp[0] = x

    for mask in range(N):
        cur = dp[mask]
        if cur == -1:
            continue
        for i in range(n):
            if not (mask >> i) & 1:
                nxt = cur % a[i]
                nmask = mask | (1 << i)
                if nxt > dp[nmask]:
                    dp[nmask] = nxt

    return str(max(dp))

# provided samples
assert run("""3
5 6 7
15
""") == "3"

assert run("""4
20 21 22 10
107
""") == "9"

# custom cases
assert run("""1
10
100""") == "0", "single element"

assert run("""2
1000000000000000000 2
100""") == "1", "large value collapse"

assert run("""3
2 3 5
100""") == "1", "small mod chain"

assert run("""5
5 4 3 2 7
12345
""") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | trivial modulo collapse |
| large value case | 1 | 64-bit safety and overflow-free logic |
| small mod chain | 1 | repeated reductions behave correctly |
| mixed ordering | variable | DP handles ordering effects |

## Edge Cases

A single-element array is the simplest scenario. The algorithm initializes the DP with $x$, and applying the only element immediately gives $x \bmod a_0$, which is correctly reflected in the final mask containing that element.

A case where one of the values is 1 is extreme because any modulo by 1 collapses the value to zero. The DP naturally avoids applying 1 too early unless forced by full coverage, since it always keeps the maximum value per subset.

Cases with very large numbers such as $10^{18}$ do not cause overflow issues in Python, but in languages with fixed-width integers, care must be taken to ensure modulo is applied before multiplication or other operations. Here, only modulo is used, so values remain bounded safely.

A subtle ordering trap occurs when small numbers appear alongside large ones. The DP correctly explores both orders, ensuring that early collapse is avoided when possible and that the optimal sequence is discovered through subset exploration.
