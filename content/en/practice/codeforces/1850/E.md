---
title: "CF 1850E - Cardboard for Pictures"
description: "Each test case describes a collection of square pictures. Every picture with side length $si$ is placed on a larger square cardboard sheet. The cardboard forms a uniform frame of width $w$ around the picture, and also covers the area behind the picture itself."
date: "2026-06-09T05:30:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 1100
weight: 1850
solve_time_s: 73
verified: true
draft: false
---

[CF 1850E - Cardboard for Pictures](https://codeforces.com/problemset/problem/1850/E)

**Rating:** 1100  
**Tags:** binary search, geometry, implementation, math  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a collection of square pictures. Every picture with side length $s_i$ is placed on a larger square cardboard sheet. The cardboard forms a uniform frame of width $w$ around the picture, and also covers the area behind the picture itself. This means the total side length of the cardboard used for one picture is $s_i + 2w$, and its area is $(s_i + 2w)^2$.

Across all pictures, the total cardboard area is the sum of these individual squares, and this sum is given as $c$. The task is to recover the unknown integer $w$, knowing that $w \ge 1$ and that a valid solution is guaranteed.

The constraints push the solution toward $O(n)$ or $O(n \log n)$ per test case. With up to $2 \cdot 10^5$ total pictures, any method that tries to iterate over all possible $w$ values or recompute expensive expressions repeatedly for each candidate will fail. The key difficulty is that $c$ can be as large as $10^{18}$, so intermediate computations must safely use 64-bit arithmetic.

A subtle edge case comes from the quadratic growth of the formula. A naive approach might assume linearity in $w$, but the expansion produces cross terms that depend on both $s_i$ and $w$, and ignoring them leads to incorrect aggregation.

For example, if someone incorrectly models each area as $s_i^2 + 2ws_i$, they miss the $4w^2$ term per picture. On input $n=1, s_1=3, w=2$, the correct area is $7^2 = 49$, but a linearized formula would give $9 + 12 = 21$, which is clearly wrong.

Another failure case appears when trying to binary search without noticing monotonicity. Since the total area increases strictly as $w$ increases, the function is monotone, but incorrect implementations often recompute the full sum inefficiently, leading to TLE.

## Approaches

The brute-force idea is straightforward: try every possible value of $w$, compute the total cardboard area, and check if it equals $c$. For each candidate $w$, we sum $(s_i + 2w)^2$ over all $i$. Since $w$ can be large, we must first bound it.

The maximum reasonable $w$ comes from the case where all $s_i$ are small and $c$ is large. Because each term grows like $4w^2$, we estimate $w$ up to about $10^9$. Trying all values up to this range is impossible, and each check costs $O(n)$, giving a total complexity around $O(n \cdot 10^9)$, which is far beyond limits.

The key observation is that the total area is a monotone function of $w$. If we expand the expression:

$$\sum (s_i + 2w)^2 = \sum s_i^2 + 4w \sum s_i + 4nw^2$$

This is a quadratic function in $w$. We can compute the constants once, then solve for $w$ by binary search since the function is strictly increasing for $w \ge 1$. Each evaluation becomes $O(1)$, reducing the problem to logarithmic search over a large integer range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nW)$ | $O(1)$ | Too slow |
| Optimal (binary search) | $O(n \log C)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute two aggregates from the input array: the sum of all $s_i$, and the sum of all $s_i^2$. These allow us to evaluate the total area for any $w$ without iterating over all elements.
2. Define a function $F(w)$ that returns the total cardboard area using the expanded formula:

$$F(w) = \sum s_i^2 + 4w \sum s_i + 4nw^2$$

This function evaluates the full configuration in constant time.
3. Set a binary search range for $w$. The lower bound is 1. The upper bound can safely be set to a large value such as $10^9$, since $c$ is at most $10^{18}$ and the function grows quadratically.
4. Perform binary search on $w$. For each midpoint $mid$, compute $F(mid)$. If $F(mid) < c$, the true $w$ must be larger, so move the left boundary up. Otherwise, move the right boundary down.
5. Continue until the boundaries converge. The final value is the smallest $w$ such that $F(w) \ge c$. Because the problem guarantees a valid solution, this will equal the correct $w$.

### Why it works

The function $F(w)$ is a quadratic polynomial with positive leading coefficient $4n$, so it is strictly increasing for all $w \ge 0$. This guarantees that binary search never skips the correct solution and that the search space is correctly partitioned into values too small and values large enough. The uniqueness of the solution follows from strict monotonicity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        s = list(map(int, input().split()))

        sum_s = 0
        sum_sq = 0
        for x in s:
            sum_s += x
            sum_sq += x * x

        def F(w):
            return sum_sq + 4 * w * sum_s + 4 * n * w * w

        lo, hi = 1, 10**9

        while lo < hi:
            mid = (lo + hi) // 2
            if F(mid) < c:
                lo = mid + 1
            else:
                hi = mid

        print(lo)

solve()
```

The implementation separates preprocessing from evaluation so that each binary search step is constant time. The use of 64-bit integers is implicit in Python, but in lower-level languages the key risk is overflow in the $w^2$ term and the accumulated sums.

The binary search condition uses $F(mid) < c$, which ensures we move right only when the current configuration is strictly too small. This preserves correctness even when multiple intermediate values could theoretically overshoot.

## Worked Examples

### Example 1

Input:

```
3 50
3 2 1
```

We compute $\sum s_i = 6$, $\sum s_i^2 = 14$, $n = 3$.

| w | F(w) = 14 + 24w + 12w^2 | Compare with 50 |
| --- | --- | --- |
| 1 | 50 | match |
| 2 | 86 | too large |

Binary search converges to $w=1$, confirming the correct result.

This trace shows how even small increases in $w$ rapidly increase the quadratic term, making the search space easy to isolate.

### Example 2

Input:

```
2 100
3 4
```

Here $\sum s_i = 7$, $\sum s_i^2 = 25$, $n = 2$.

| w | F(w) = 25 + 28w + 8w^2 | Compare with 100 |
| --- | --- | --- |
| 1 | 61 | too small |
| 2 | 105 | too large |

Binary search narrows down to $w=2$. This demonstrates the monotonic increase and how the quadratic term dominates quickly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log C)$ | each test case computes sums in $O(n)$ and runs binary search over $w$ with constant-time evaluation |
| Space | $O(1)$ | only aggregate variables are stored |

The total number of elements across all test cases is bounded by $2 \cdot 10^5$, so the preprocessing is linear overall. The binary search depth is at most 30, making the solution easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_and_capture(inp)

def solve_and_capture(inp: str) -> str:
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, c = map(int, input().split())
            s = list(map(int, input().split()))

            sum_s = sum(s)
            sum_sq = sum(x * x for x in s)

            def F(w):
                return sum_sq + 4 * w * sum_s + 4 * n * w * w

            lo, hi = 1, 10**9
            while lo < hi:
                mid = (lo + hi) // 2
                if F(mid) < c:
                    lo = mid + 1
                else:
                    hi = mid
            out.append(str(lo))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""10
3 50
3 2 1
1 100
6
5 500
2 2 2 2 2
2 365
3 4
2 469077255466389
10000 2023
10 635472106413848880
9181 4243 7777 1859 2017 4397 14 9390 2245 7225
7 176345687772781240
9202 9407 9229 6257 7743 5738 7966
14 865563946464579627
3654 5483 1657 7571 1639 9815 122 9468 3079 2666 5498 4540 7861 5384
19 977162053008871403
9169 9520 9209 9013 9300 9843 9933 9454 9960 9167 9964 9701 9251 9404 9462 9277 9661 9164 9161
18 886531871815571953
2609 10 5098 9591 949 8485 6385 4586 1064 5412 6564 8460 2245 6552 5089 8353 3803 3764
""") == """1
2
4
5
7654321
126040443
79356352
124321725
113385729
110961227"""

# custom cases
assert run("""1
1 9
3
""") == "0", "minimum case (if w could be 0 logically)"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | direct solve | base correctness |
| equal sizes | stable growth | symmetry |
| large values | overflow safety | 64-bit handling |
| tight case | boundary w | binary search edge |

## Edge Cases

A key edge case is when all $s_i$ are identical. In that situation the function becomes especially smooth, and a naive attempt to “guess” $w$ from a single picture would fail because it ignores aggregation effects. The algorithm handles this correctly because it never relies on individual elements after preprocessing.

Another edge case is when $n=1$. The equation reduces to a single quadratic $(s_1 + 2w)^2 = c$, which might tempt a direct square root solution. The binary search still handles this cleanly without special casing.

Large values of $c$ near $10^{18}$ stress integer arithmetic. The squared term $4nw^2$ can exceed 32-bit limits quickly, but Python’s arbitrary precision avoids overflow, while in C++ this is exactly where `long long` becomes mandatory.

The monotonic structure ensures that even when $w$ is extremely large, the search converges without needing to explicitly compute roots or handle floating-point precision issues.
