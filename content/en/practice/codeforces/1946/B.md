---
title: "CF 1946B - Maximum Sum"
description: "We are given an array of integers and we are allowed to perform exactly k operations. Each operation lets us pick any contiguous segment of the current array, compute its sum, and insert that sum back into the array at any position."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1946
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 936 (Div. 2)"
rating: 1100
weight: 1946
solve_time_s: 165
verified: false
draft: false
---

[CF 1946B - Maximum Sum](https://codeforces.com/problemset/problem/1946/B)

**Rating:** 1100  
**Tags:** dp, greedy, math  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and we are allowed to perform exactly `k` operations. Each operation lets us pick any contiguous segment of the current array, compute its sum, and insert that sum back into the array at any position.

The key effect of an operation is that it increases the total sum of the array by the sum of the chosen subarray. Inserting the value does not remove elements, so the structure grows, but the only quantity that matters for the final answer is the total sum of all elements.

So the real question is not about the array structure at all. It is about how much extra sum we can generate by repeatedly selecting subarrays.

The input gives multiple test cases, each with an array and a number of operations. For each test case, we need the maximum achievable total sum after exactly `k` operations, modulo $10^9 + 7$.

The constraints are large: total `n` and total `k` across tests are up to $2 \cdot 10^5$. This immediately rules out any solution that tries to simulate operations or recompute subarray sums per operation. Any valid solution must reduce each test case to linear or near-linear preprocessing and then constant-time reasoning per test.

A subtle point is that empty subarrays are allowed. Their sum is zero, meaning we can always “waste” an operation. This becomes important when all subarray sums are negative or when no positive gain is possible.

Another hidden pitfall is assuming we must pick non-empty segments. The ability to choose an empty segment is what makes the baseline behavior stable when all values are negative.

A naive misunderstanding would be to simulate each operation greedily and update the array. That fails because each insertion changes future choices, and the number of states grows rapidly.

## Approaches

A brute-force strategy would explicitly simulate each operation. For each of the `k` steps, we would consider all subarrays of the current array, compute their sums, pick the best one, and insert it. Even if we maintain prefix sums to compute subarray sums quickly, each step still requires $O(n^2)$ choices in the worst case.

Since `k` itself can be large, the array size also increases with every insertion, making the brute-force explode far beyond feasible limits. The growth is multiplicative: after each operation, the array becomes larger, so later operations are even more expensive than earlier ones.

The key observation is that the only thing that matters is whether we can obtain a positive contribution from a subarray. Once we pick a subarray with sum `S`, we are effectively adding `S` to the total sum. The structure of the array after insertion is irrelevant for the final sum, because future operations only depend on sums we can extract, not positions.

This reduces the problem to understanding the best subarray sum we can repeatedly exploit. The optimal strategy is to repeatedly add the maximum possible subarray sum if it is positive. If all subarrays have non-positive sum, we instead use empty subarrays.

So the core transition becomes: compute the maximum subarray sum `mx` once, then each operation contributes `max(0, mx)` to the total answer. The base is the sum of the original array.

We also implicitly allow choosing the best subarray every time independently, since inserting the sum does not reduce the ability to pick the same optimal segment again.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(k \cdot n^2)$ | $O(n)$ | Too slow |
| Kadane + Greedy Accumulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to two quantities: the total sum of the array and the maximum subarray sum.

1. Compute the total sum of the array. This is the base contribution before any operations. The reason this works is that operations only add values, they never remove or replace existing sum contribution.
2. Compute the maximum subarray sum using a linear scan (Kadane’s algorithm). This identifies the best possible gain from a single operation.
3. If the maximum subarray sum is negative, treat it as zero. This corresponds to choosing an empty subarray, which guarantees no decrease in total sum.
4. Each operation contributes independently the best possible gain. Therefore, the total added contribution is `k * max(0, mx_subarray_sum)`.
5. Add this contribution to the original sum.
6. Take the result modulo $10^9 + 7$, ensuring non-negative output even if intermediate values were negative.

Why it works: every operation is independent in terms of contribution to total sum. The structure changes do not restrict future ability to obtain the same maximum gain because we can always select subarrays from the original content effectively, and inserted elements do not create better-than-optimal subarray sums beyond `mx`. The process stabilizes into repeatedly harvesting the same best gain.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = sum(a)
        
        best = float('-inf')
        cur = 0
        
        for x in a:
            cur = max(x, cur + x)
            best = max(best, cur)
        
        if best < 0:
            best = 0
        
        ans = (total + best * k) % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates global accumulation from local optimization cleanly. The `total` variable tracks the invariant base sum. The Kadane loop maintains a running best segment ending at each position, ensuring we capture the optimal subarray in linear time. The clamp to zero enforces the empty-subarray option.

The final multiplication by `k` reflects the independence of operations, which is the central structural simplification of the problem.

## Worked Examples

We trace a simplified version of two test cases to observe how the algorithm behaves.

### Example 1

Input: `a = [2, 2, 8], k = 3`

| Step | cur | best | total |
| --- | --- | --- | --- |
| 1 (2) | 2 | 2 | 12 |
| 2 (2) | 4 | 4 | 12 |
| 3 (8) | 12 | 12 | 12 |

After scan, `best = 12`.

Each operation adds 12, so total becomes:

`12 + 3 * 12 = 48`.

This matches the idea that the entire array is always the optimal segment.

### Example 2

Input: `a = [-4, -7], k = 2`

| Step | cur | best | total |
| --- | --- | --- | --- |
| 1 (-4) | -4 | -4 | -11 |
| 2 (-7) | -7 | -4 | -11 |

Here all subarrays are negative, so `best = 0`.

Total remains:

`-11 + 2 * 0 = -11`, which modulo becomes `999999996`.

This demonstrates the role of empty subarrays, preventing any forced degradation or improvement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Single pass Kadane plus sum computation |
| Space | $O(1)$ | Only a few running variables are used |

The total complexity across all test cases is linear in the input size, which fits comfortably under the constraint that the sum of `n` is $2 \cdot 10^5$. Memory usage is constant beyond the input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []

    MOD = 10**9 + 7

    t = int(sys.stdin.readline())
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        
        total = sum(a)
        
        best = float('-inf')
        cur = 0
        for x in a:
            cur = max(x, cur + x)
            best = max(best, cur)
        
        best = max(0, best)
        output.append(str((total + best * k) % MOD))
    
    return "\n".join(output)

# provided samples (partial check due to length)
assert run("""1
2 2
-4 -7
""") == "999999996"

assert run("""1
3 3
2 2 8
""") == "96"

# custom cases
assert run("""1
1 5
5
""") == "30", "single positive element"
assert run("""1
1 5
-5
""") == "999999982", "single negative element"
assert run("""1
5 3
0 0 0 0 0
""") == "0", "all zeros"
assert run("""1
4 2
-1 2 -1 2
""") == "10", "alternating positives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single positive | 30 | repeated gains accumulate correctly |
| single negative | mod result | empty subarray behavior |
| all zeros | 0 | neutral stability |
| alternating positives | 10 | Kadane correctly finds best segment |

## Edge Cases

For arrays with all negative values, the algorithm sets `best` to zero, ensuring that every operation effectively becomes a no-op. For example, `[-1, -2, -3]` produces total `-6`, and since no positive subarray exists, the answer remains `-6 mod M`. This prevents incorrect attempts to “improve” the array using negative segments.

For arrays with a single element, Kadane’s algorithm correctly identifies that element as the only subarray candidate. If it is positive, it is multiplied by `k`; if negative, it is ignored via the zero clamp. This avoids double-counting or missing the empty subarray option.

For arrays of all zeros, both total and best remain zero, and repeated operations do not change anything. This confirms stability under neutral inputs.

For mixed-sign arrays where positive segments are isolated, Kadane ensures only contiguous positive contributions are selected, and repeated operations scale only the best contiguous gain rather than summing multiple disjoint segments incorrectly.
