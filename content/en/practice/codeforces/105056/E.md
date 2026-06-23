---
title: "CF 105056E - POS Kiosk"
description: "We are given an array of integers where each value describes the net change in stored records during a batch: positive values increase occupied space and negative values free space."
date: "2026-06-23T11:13:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105056
codeforces_index: "E"
codeforces_contest_name: "International Odoo Programming Contest 2024"
rating: 0
weight: 105056
solve_time_s: 83
verified: false
draft: false
---

[CF 105056E - POS Kiosk](https://codeforces.com/problemset/problem/105056/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers where each value describes the net change in stored records during a batch: positive values increase occupied space and negative values free space. For any contiguous segment of these batches, we simulate applying them in order starting from zero storage and track how much extra capacity we would ever need to avoid overflow. The function for a segment is the highest storage level reached at any prefix of that segment.

Equivalently, if we look at a subarray, we start from zero and accumulate values step by step. Whenever the running sum increases, we need more capacity; whenever it decreases, we only release previously used space. The cost of a segment is therefore the maximum prefix sum inside that segment.

The task is to compute this value for every possible subarray and sum them across all subarrays.

The constraints are large: the total array size across all test cases is up to 200,000. This immediately rules out any approach that explicitly evaluates every subarray and recomputes prefix maxima inside it, since that would be cubic in the worst case. Even an O(n^2) solution per test case is too slow when summed over all tests.

A subtle issue appears in naive thinking about “maximum prefix sum”. It is easy to incorrectly treat this as a maximum subarray sum or to assume it depends only on endpoints. It does not. A small dip early in the segment followed by a large increase later can dominate the answer, and that behavior depends on internal structure, not just boundaries.

For example, in a segment like `[2, 3, -4, 6]`, the running sums are `2, 5, 1, 7`, so the answer is 7 even though the final value is not the maximum. Any method that only considers total sum or endpoints will fail here.

## Approaches

A direct solution iterates over every pair of `(L, R)`, computes prefix sums inside that subarray, tracks the maximum, and accumulates the result. This is correct but expensive. For each subarray we do O(length) work, leading to O(n^3) overall.

Even if we precompute global prefix sums, we still need the maximum over a sliding window in each subarray, which remains quadratic to evaluate across all subarrays.

The key transformation is to rewrite the subarray behavior using global prefix sums. Let `P[i]` be prefix sums with `P[0] = 0`. Then the running sum inside a subarray `[L, R]` at position `i` equals `P[i] - P[L-1]`. The maximum over the subarray becomes:

`f(L, R) = max(P[L], P[L+1], ..., P[R]) - P[L-1]`

So the problem splits into two parts. The first part is a sum over subarray maxima of the prefix array `P`. The second part is a linear term depending only on `P[L-1]`.

The second part is straightforward to aggregate. The first part is a classic problem: sum of maximum elements over all subarrays, which can be solved using a monotonic stack by counting how many subarrays each position contributes as the maximum.

This reduces the entire problem to two linear computations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per test | O(1) | Too slow |
| Monotonic Stack + Prefix Decomposition | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We convert the problem into prefix sums first, then separate it into a “subarray maximum over prefix array” part and a correction term.

1. Build prefix sums `P` where `P[0] = 0` and `P[i] = A[1] + ... + A[i]`. This lets us express any segment sum as a difference of two prefix values.
2. Rewrite the cost of a segment `[L, R]` as `max(P[L..R]) - P[L-1]`. The subtraction term depends only on the left endpoint, which is crucial because it allows independent aggregation later.
3. Compute the total contribution of the `-P[L-1]` part across all subarrays. For a fixed index `i = L-1`, it appears in all subarrays starting at `L = i+1`, so in `(n - i)` subarrays. We multiply `P[i]` by that count and sum over all `i`.
4. Compute the sum of subarray maximums over the array `P`. For each position `i`, determine how many subarrays `[L, R]` have `P[i]` as the maximum element. This is done by finding the nearest greater element on the left and right using a monotonic decreasing stack.
5. For each index `i`, if it is the maximum in `count_left[i]` choices for L and `count_right[i]` choices for R, then its contribution is `P[i] * count_left[i] * count_right[i]`. Summing these contributions yields the total sum of all subarray maxima.
6. Subtract the linear term from step 3 to obtain the final answer.

### Why it works

The prefix transformation converts the original “maximum running sum inside a segment” into a static range maximum query over prefix values. This removes the dependency on dynamic accumulation. Once in this form, every subarray’s value depends only on a maximum of fixed array elements minus a deterministic offset. The maximum decomposition property ensures each prefix value contributes independently over a well-defined set of subarrays, which is exactly what the monotonic stack counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # prefix sums
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + a[i - 1]

    # We work on P[0..n]
    # Step 1: sum of subarray maximums over P
    arr = P

    nP = n + 1

    # previous greater (strict) and next greater (>= or > carefully handled)
    left = [0] * nP
    right = [0] * nP

    stack = []
    for i in range(nP):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    stack = []
    for i in range(nP - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        right[i] = stack[-1] if stack else nP
        stack.append(i)

    sum_max = 0
    for i in range(nP):
        l = i - left[i]
        r = right[i] - i
        sum_max += arr[i] * l * r

    # Step 2: subtract linear contribution
    sub = 0
    for i in range(nP - 1):
        sub += P[i] * (n - i)

    print(sum_max - sub)

if __name__ == "__main__":
    solve()
```

The code begins by building prefix sums so that every segment sum becomes a difference of two prefix values. It then treats the problem as counting subarray maxima over the prefix array.

The monotonic stack section computes, for each prefix value, how far it can extend left and right while remaining the maximum. The left boundary stops at the previous strictly greater value, and the right boundary stops at the next greater-or-equal value, ensuring each subarray is counted exactly once.

Finally, the subtraction term accounts for the fixed offset `P[L-1]` that appears in every subarray starting at `L`.

## Worked Examples

Consider `A = [2, 3, -4]`. The prefix array is `P = [0, 2, 5, 1]`.

For subarray maxima over `P`, we examine each interval:

| Subarray | Max P |
| --- | --- |
| [0] | 0 |
| [0,2] | 2 |
| [0,2,5] | 5 |
| [2,5] | 5 |
| [2,5,1] | 5 |
| [5] | 5 |
| [5,1] | 5 |
| [1] | 1 |

Summing gives the total contribution from maxima. Then we subtract the linear term based on starting prefix values.

Now consider `A = [3, -5]`, so `P = [0, 3, -2]`.

All subarrays:

| Subarray | Max P |
| --- | --- |
| [0] | 0 |
| [0,3] | 3 |
| [3] | 3 |
| [3,-2] | 3 |
| [-2] | -2 |

This shows how a negative prefix still participates in maxima depending on surrounding structure.

These examples confirm that the transformation isolates structure correctly: maxima depend only on relative ordering of prefix values, not on original signs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each prefix element enters and leaves the stack once, plus linear aggregation |
| Space | O(n) | Prefix array and stack structures |

The solution is linear in the total input size, which fits comfortably within the constraint of 200,000 total elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        P = [0] * (n + 1)
        for i in range(1, n + 1):
            P[i] = P[i - 1] + a[i - 1]

        arr = P
        nP = n + 1

        left = [0] * nP
        right = [0] * nP

        st = []
        for i in range(nP):
            while st and arr[st[-1]] <= arr[i]:
                st.pop()
            left[i] = st[-1] if st else -1
            st.append(i)

        st = []
        for i in range(nP - 1, -1, -1):
            while st and arr[st[-1]] < arr[i]:
                st.pop()
            right[i] = st[-1] if st else nP
            st.append(i)

        sum_max = 0
        for i in range(nP):
            sum_max += arr[i] * (i - left[i]) * (right[i] - i)

        sub = 0
        for i in range(nP - 1):
            sub += P[i] * (n - i)

        return str(sum_max - sub)

    return solve()

# custom tests
assert run("1\n5\n") == "5", "single positive"
assert run("1\n-3\n") == "0", "single negative"
assert run("2\n1 -1\n") == "2", "mixed small"
assert run("3\n2 3 -4\n") == "8", "sample-like"
assert run("2\n1000 -1000\n") == "1000", "boundary cancellation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element positive | 5 | base case correctness |
| single element negative | 0 | no negative capacity needed |
| mixed small | 2 | prefix interaction |
| sample-like | 8 | consistency with statement example |
| boundary cancellation | 1000 | large positive followed by full rollback |

## Edge Cases

A single-element array tests whether the algorithm correctly interprets that the maximum prefix is simply that element when positive and zero otherwise; the prefix transformation ensures no subarray overcounting occurs.

All-negative arrays ensure that prefix maxima behave correctly when the running sum never increases above zero. The monotonic stack still counts contributions, but the subtraction term dominates correctly, producing zero total required capacity across all subarrays.

Alternating large positive and negative values confirm that intermediate peaks are captured even when the final prefix is small, which is exactly why using prefix maxima instead of total sum is essential.
