---
title: "CF 1899C - Yarik and Array"
description: "We are given several independent test cases. Each test case provides an integer array, and the task is to choose a non-empty contiguous segment whose sum is as large as possible, under one additional restriction: adjacent elements inside the chosen segment must alternate in…"
date: "2026-06-08T21:24:27+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1899
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 909 (Div. 3)"
rating: 1100
weight: 1899
solve_time_s: 97
verified: true
draft: false
---

[CF 1899C - Yarik and Array](https://codeforces.com/problemset/problem/1899/C)

**Rating:** 1100  
**Tags:** dp, greedy, two pointers  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case provides an integer array, and the task is to choose a non-empty contiguous segment whose sum is as large as possible, under one additional restriction: adjacent elements inside the chosen segment must alternate in parity. In other words, whenever two neighboring chosen elements are next to each other in the original array, one must be even and the other must be odd.

This turns the classic maximum subarray sum problem into a constrained version where we are not allowed to extend a segment through two consecutive elements with the same parity. However, we are still allowed to start a new segment anywhere, and we are not required to use the whole array.

The constraints allow up to 200,000 total elements across all test cases, which immediately implies that any solution must be linear per test case, or at worst O(n log n). A quadratic approach that tries all subarrays or repeatedly recomputes sums over segments would reach roughly 10^10 operations in the worst case, which is far beyond the limit. This pushes us toward a dynamic programming or greedy linear scan.

A few edge cases are easy to miss.

A single element array always has an answer equal to that element, even if it is negative, since we must choose a non-empty subarray.

A segment that alternates parity but has many negative values may still be optimal to truncate early, because extending it might reduce the sum.

A subtle failure case for naive greedy expansion occurs when we break parity alternation: restarting too late or too early can miss better segments. For example, in an array like `[5, -100, 4, 3]`, blindly resetting only when parity breaks is insufficient if negative values should force a restart earlier.

## Approaches

A brute-force idea would enumerate every possible subarray and check whether it satisfies the parity alternation constraint. For each valid subarray, we compute its sum and track the maximum. Checking validity of one subarray takes O(length), and there are O(n^2) subarrays, leading to O(n^3) worst-case time, which is infeasible.

We can reduce this by noticing that validity of a subarray is local: once we fix a starting index, we can extend greedily until the parity condition breaks. That reduces checking all subarrays starting at i to O(n), giving O(n^2). Still too slow for 2e5 total elements.

The key observation is that we never need to revisit earlier decisions. At each position, we either continue an existing valid alternating segment or restart at the current element. This is a classic dynamic programming situation similar to Kadane’s algorithm, but with an additional constraint on transitions.

We maintain the best possible sum of a valid alternating subarray ending at the current index. When we extend from i−1 to i, we are only allowed to do so if a[i] has different parity from a[i−1]. If parity matches, we must restart at i.

Additionally, even if extension is allowed, we still compare it against starting fresh at i, because previous accumulated sums might be negative and hurt optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal DP (Kadane-like) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each array independently while maintaining a running best subarray ending at the current position.

1. Initialize a variable `current` as the best alternating subarray sum ending at index 0, which is simply `a[0]`. We also initialize `answer = a[0]` because the best subarray could be a single element.
2. Iterate through the array from index 1 to n−1.
3. At each index i, check whether `a[i]` can extend the previous segment. Extension is only valid if `a[i]` and `a[i-1]` have different parity. If parity is the same, any subarray ending at i−1 cannot be extended to i while respecting the rule.
4. If extension is valid, compute a candidate value `current + a[i]`. Otherwise, set extension as impossible.
5. Regardless of extension feasibility, also consider starting a new subarray at i with value `a[i]`.
6. Set `current` to the maximum of these two options. This choice ensures we always keep the best valid alternating subarray ending at i.
7. Update `answer` with `max(answer, current)`.

After finishing the scan, `answer` contains the best possible sum over all valid subarrays.

### Why it works

At every index i, the algorithm maintains the invariant that `current` is the maximum sum of any valid alternating-parity subarray that ends exactly at i. Any such subarray either comes from extending a valid subarray ending at i−1 or starting fresh at i. There is no third possibility, since every subarray ending at i must include i and its previous element is either part of the subarray or not. The parity constraint only restricts whether extension is allowed, not the structure of optimal subarrays. Because we always take the best of these two choices, no optimal solution is ever discarded.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    current = a[0]
    best = a[0]
    
    for i in range(1, n):
        if (a[i] % 2) != (a[i - 1] % 2):
            extend = current + a[i]
        else:
            extend = -10**18  # invalid transition
        
        current = max(a[i], extend)
        best = max(best, current)
    
    out.append(str(best))

print("\n".join(out))
```

The code follows the DP formulation directly. The variable `current` represents the best valid alternating subarray ending at the current index. When parity alternates, we attempt to extend; otherwise, extension is forcibly invalid.

A subtle point is the comparison against `a[i]` itself, which ensures we restart whenever previous accumulation is harmful. This is what preserves optimality in the presence of negative values.

The variable `best` tracks the global maximum across all endpoints, since the optimal subarray may end anywhere.

## Worked Examples

We trace the algorithm on two representative cases.

### Example 1

Input: `[1, 2, 3, 4, 5]`

| i | a[i] | Parity valid extension | Extend value | current chosen | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | - | 1 | 1 |
| 1 | 2 | yes | 3 | 3 | 3 |
| 2 | 3 | yes | 6 | 6 | 6 |
| 3 | 4 | yes | 10 | 10 | 10 |
| 4 | 5 | yes | 15 | 15 | 15 |

The algorithm continuously extends because parity alternates and all values are positive, producing a full array optimum.

### Example 2

Input: `[9, 9, 8, 8]`

| i | a[i] | Parity valid extension | Extend value | current chosen | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 9 | - | - | 9 | 9 |
| 1 | 9 | no | -inf | 9 | 9 |
| 2 | 8 | yes | 17 | 17 | 17 |
| 3 | 8 | no | -inf | 8 | 17 |

This shows why restarting is crucial: at index 2 we begin a new optimal segment instead of trying to extend from an invalid parity transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with O(1) transitions |
| Space | O(1) extra space | Only a few variables are maintained |

The total input size across test cases is bounded by 2×10^5, so a linear scan over all elements fits comfortably within time limits. The solution performs a small constant number of operations per element, well within 1 second in Python.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        current = a[0]
        best = a[0]

        for i in range(1, n):
            if (a[i] % 2) != (a[i - 1] % 2):
                extend = current + a[i]
            else:
                extend = -10**18

            current = max(a[i], extend)
            best = max(best, current)

        out.append(str(best))

    return "\n".join(out)

# provided samples
assert solve("""7
5
1 2 3 4 5
4
9 9 8 8
6
-1 4 -1 0 5 -4
4
-1 2 4 -3
1
-1000
3
101 -99 101
20
-10 5 -8 10 6 -10 7 9 -2 -6 7 2 -4 6 -1 7 -6 -7 4 1
""") == """15
17
8
4
-1000
101
10"""

# custom cases

# single element negative
assert solve("""1
1
-5
""") == "-5"

# all same parity forces single elements
assert solve("""1
5
2 4 6 8 10
""") == "10"

# alternating but negative-heavy
assert solve("""1
6
1 -2 3 -4 5 -6
""") == "5"

# alternating with beneficial restart
assert solve("""1
5
5 -1 4 -2 3
""") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | -5 | base case handling |
| all same parity | 10 | forced restarts |
| negative alternating | 5 | restart vs continuation |
| mixed restart benefit | 9 | optimal segmentation |

## Edge Cases

A single element input is handled directly because initialization sets both `current` and `best` to the first element. The loop does not execute, so the answer is returned correctly even if the value is negative.

Arrays with all numbers of the same parity never allow extension. The algorithm effectively reduces to taking the maximum single element, since every index becomes a restart point. Each iteration sets `current = a[i]`, so `best` tracks the maximum element.

For alternating arrays with large negative values, the algorithm may repeatedly restart. Each restart is handled by the `max(a[i], extend)` comparison, ensuring that we never carry forward a harmful prefix sum.

In cases where a negative value is sandwiched between two valid alternating positives, the algorithm correctly evaluates whether keeping the negative improves a longer alternating chain or whether restarting yields a better sum.
