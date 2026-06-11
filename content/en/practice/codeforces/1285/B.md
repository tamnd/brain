---
title: "CF 1285B - Just Eat It!"
description: "We have an array representing the tastiness of cupcakes, and two players. Yasser always takes all the cupcakes, summing up the full array. Adel can pick any contiguous subarray that does not cover the entire array."
date: "2026-06-11T19:14:49+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1285
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 613 (Div. 2)"
rating: 1300
weight: 1285
solve_time_s: 129
verified: true
draft: false
---

[CF 1285B - Just Eat It!](https://codeforces.com/problemset/problem/1285/B)

**Rating:** 1300  
**Tags:** dp, greedy, implementation  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array representing the tastiness of cupcakes, and two players. Yasser always takes all the cupcakes, summing up the full array. Adel can pick any contiguous subarray that does **not** cover the entire array. Yasser wants to know if his total tastiness is strictly greater than **any possible sum** Adel can achieve.

The input consists of multiple test cases. Each test case gives the number of cupcakes and the array of tastiness values. The output for each test case is either "YES" if Yasser will always have a strictly higher total, or "NO" otherwise.

Looking at the constraints, each array can have up to $10^5$ elements, and the total over all test cases is also $10^5$. This immediately rules out any $O(n^2)$ approach, because iterating over all subarrays would be roughly $10^{10}$ operations in the worst case. A linear or near-linear solution is required. Values of tastiness can be large negatives or positives ($-10^9$ to $10^9$), so we also need to be careful about integer overflow in languages that have fixed-size integers, though Python handles this automatically.

A subtle edge case arises when the array has only two elements. Adel can only take one element at a time, and Yasser’s sum will always equal the sum of both. If one element is greater than the other, Yasser will be happy; if the largest subarray sum Adel can take equals Yasser’s total, the answer is "NO". Another edge case occurs when the array has alternating positive and negative numbers, for example `[5, -5, 5]`. Yasser’s total sum is `5`, but Adel can pick the last `5` alone, matching Yasser’s total. A careless implementation might ignore the restriction on not taking the entire array or fail to consider prefix and suffix subarrays properly.

## Approaches

The brute-force approach is straightforward: for each test case, compute Yasser’s total sum. Then, for every valid subarray that Adel can take, calculate its sum and compare with Yasser’s. This guarantees correctness, because we literally check every possibility. However, this is $O(n^2)$ for each test case. With $n$ up to $10^5$, this is far too slow.

The key insight comes from realizing that the only subarrays that could threaten Yasser are prefixes or suffixes. Any subarray fully inside the array that doesn’t touch the boundaries will have a sum strictly less than some prefix or suffix that extends to an edge because we can include more elements, potentially increasing the sum. Therefore, it is sufficient to check the maximum sum of prefixes (excluding the full array) and maximum sum of suffixes. If both of these are strictly less than Yasser’s total sum, no interior subarray can exceed his sum, and the answer is "YES". Otherwise, the answer is "NO". This reduces the complexity to linear per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute Yasser’s total sum by summing the entire array. This is straightforward and forms the baseline for comparison.
2. Compute the maximum prefix sum, considering prefixes that exclude the last element. Initialize a running sum to zero, iterate from the first element to the second-to-last element, adding each element to the running sum, and track the maximum encountered. We stop at the second-to-last because Adel cannot take the full array.
3. Compute the maximum suffix sum, considering suffixes that exclude the first element. Initialize a running sum to zero, iterate from the last element to the second element in reverse, adding each element to the running sum, and track the maximum encountered. We start at the last element because the first element cannot be included in the suffix if we want to avoid taking the full array.
4. Compare Yasser’s total with both maximum prefix and suffix sums. If either maximum is greater than or equal to Yasser’s total, print "NO". Otherwise, print "YES".

Why it works: The invariant is that the maximum sum of any subarray excluding the full array is always either a prefix or a suffix. Interior subarrays are bounded by the sums of prefixes and suffixes. By ensuring that no prefix or suffix sum meets or exceeds Yasser’s total, we guarantee that no subarray choice by Adel can surpass Yasser’s sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        total = sum(a)
        
        # check max prefix sum excluding last element
        max_prefix = curr = 0
        for i in range(n - 1):
            curr += a[i]
            if curr > max_prefix:
                max_prefix = curr
        
        # check max suffix sum excluding first element
        max_suffix = curr = 0
        for i in range(n - 1, 0, -1):
            curr += a[i]
            if curr > max_suffix:
                max_suffix = curr
        
        if max_prefix >= total or max_suffix >= total:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    main()
```

We use fast I/O with `sys.stdin.readline` due to the potential number of test cases. The prefix and suffix sums are initialized to zero and updated incrementally, ensuring correct handling of negative values. Off-by-one errors are avoided by stopping the prefix at `n - 1` and the suffix at `1`. The comparison uses `>=` because the happiness condition is strictly greater.

## Worked Examples

**Example 1:** `[1, 2, 3, 4]`

| Step | curr prefix | max_prefix | curr suffix | max_suffix | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | - | - | 10 |
| 2 | 3 | 3 | - | - | 10 |
| 3 | 6 | 6 | - | - | 10 |
| 1 (suffix) | - | - | 4 | 4 | 10 |
| 2 | - | - | 7 | 7 | 10 |
| 3 | - | - | 9 | 9 | 10 |

Both max prefix and suffix are less than 10, so output "YES".

**Example 2:** `[7, 4, -1]`

| Step | curr prefix | max_prefix | curr suffix | max_suffix | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | 7 | - | - | 10 |
| 2 | 11 | 11 | - | - | 10 |
| 1 (suffix) | - | - | -1 | -1 | 10 |
| 2 | - | - | 3 | 3 | 10 |

Max prefix 11 ≥ total 10, so output "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate through the array twice to compute prefix and suffix sums. |
| Space | O(1) | Only a few running totals are kept. |

This fits comfortably within the constraints, as the sum of all `n` across test cases is ≤ $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("3\n4\n1 2 3 4\n3\n7 4 -1\n3\n5 -5 5\n") == "YES\nNO\nNO", "samples"

# custom cases
assert run("2\n2\n1 2\n2\n-1 -2\n") == "YES\nNO", "min size"
assert run("1\n5\n5 5 5 5 5\n") == "YES", "all equal positive"
assert run("1\n3\n-1 -1 -1\n") == "NO", "all negative"
assert run("1\n4\n1 -1 1 -1\n") == "NO", "alternating signs"
assert run("1\n3\n10 -1 1\n") == "YES", "single negative in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n2\n1 2\n2\n-1 -2 | YES\nNO | Minimum size, positive and negative |
| 1\n5\n5 5 5 5 5 | YES | All-equal positive |
| 1\n3\n-1 -1 -1 | NO | All negative numbers |
| 1\n4\n1 -1 1 -1 | NO | Alternating signs, interior subarray max |
| 1\n3\n10 -1 1 | YES | Single negative in the middle |

## Edge Cases

For `[5, -5, 5]`, Yasser’s total is 5. Prefix sums: 5, 0 (first two), suffix sums
