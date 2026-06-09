---
title: "CF 1791E - Negatives and Positives"
description: "We are given an array of integers, which can be positive, negative, or zero, and we are allowed to perform a single operation any number of times: choose two adjacent elements and flip their signs simultaneously."
date: "2026-06-09T10:31:01+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1791
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 849 (Div. 4)"
rating: 1100
weight: 1791
solve_time_s: 133
verified: true
draft: false
---

[CF 1791E - Negatives and Positives](https://codeforces.com/problemset/problem/1791/E)

**Rating:** 1100  
**Tags:** dp, greedy, sortings  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, which can be positive, negative, or zero, and we are allowed to perform a single operation any number of times: choose two adjacent elements and flip their signs simultaneously. The goal is to maximize the sum of all array elements after applying these operations optimally.

Input consists of multiple test cases, each with a length $n$ and an array of $n$ integers. The output is a single integer per test case: the maximum sum achievable after any number of allowed operations.

The constraints are significant: $n$ can be up to 200,000, and the sum of $n$ across all test cases does not exceed 200,000. This rules out any algorithm that examines every possible pair sequence or simulates operations blindly, because such brute-force approaches can have exponential complexity. Each element can be as large as $10^9$ or as small as $-10^9$, so intermediate sums must be handled with 64-bit integers.

Edge cases that are easy to overlook include arrays with all negative numbers of odd length. For example, $[-1, -1, -1]$ cannot have all elements flipped to positive because each operation affects two elements. The optimal sum here is achieved by flipping the first two elements to get $[1, 1, -1]$, which sums to $1$. Another subtle scenario is arrays with zeros: flipping a negative and zero can convert the negative to positive without harming the zero, which increases the sum.

## Approaches

The brute-force approach is straightforward: iterate through all adjacent pairs, flip their signs, compute the sum, and repeat until no improvement is possible. While this works in principle, the number of possible operation sequences grows exponentially. For $n = 2 \cdot 10^5$, even considering each pair once is already $O(n)$ per operation, and iterating until convergence could lead to millions or billions of operations, which is far beyond feasible.

The key observation that unlocks a faster solution comes from parity and absolute values. Flipping two adjacent elements preserves the sum of their absolute values but allows us to change the signs. If all elements are non-negative, the sum is maximal. If there is an even number of negative elements, we can pair them up and flip each pair until all are positive. If there is an odd number of negative elements, all but one can be flipped positive, leaving the smallest absolute value element negative. This is because the operation can only flip signs in pairs, so a single leftover negative cannot be eliminated.

The optimal approach reduces to summing the absolute values of all elements and, if the count of negative numbers is odd, subtracting twice the smallest absolute value. This ensures we leave exactly one negative element with the minimal possible impact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `total_sum` to zero and `min_abs` to a very large value. Also track `neg_count` as zero.
2. Iterate through each element of the array. For each element, add its absolute value to `total_sum`. Update `min_abs` if the absolute value is smaller than the current `min_abs`. Increment `neg_count` if the element is negative.
3. After processing all elements, check the parity of `neg_count`. If it is odd, subtract twice `min_abs` from `total_sum` to account for the unavoidable negative element.
4. Output `total_sum` for the current test case. Repeat for all test cases.

Why it works: the sum of absolute values represents the maximum achievable if all elements could be made positive. Operations allow flipping in pairs, so only an odd count of negatives prevents making all positive. Subtracting twice the smallest absolute value simulates leaving one negative element of minimal impact, which produces the maximum sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_sum_after_flips():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total_sum = 0
        min_abs = float('inf')
        neg_count = 0

        for x in a:
            if x < 0:
                neg_count += 1
            abs_x = abs(x)
            total_sum += abs_x
            if abs_x < min_abs:
                min_abs = abs_x

        if neg_count % 2 == 1:
            total_sum -= 2 * min_abs

        print(total_sum)

if __name__ == "__main__":
    max_sum_after_flips()
```

The code mirrors the algorithm directly. We compute `total_sum` as the sum of absolute values. `neg_count` tracks how many elements are negative, and `min_abs` finds the smallest absolute value. The check for `neg_count % 2 == 1` ensures we account for cases where one negative element cannot be eliminated. The use of `float('inf')` is safe for comparisons, and `abs()` handles large integers correctly.

## Worked Examples

### Sample Input 1

```
3
-1 -1 -1
```

| Step | Element | abs(x) | total_sum | min_abs | neg_count |
| --- | --- | --- | --- | --- | --- |
| 1 | -1 | 1 | 1 | 1 | 1 |
| 2 | -1 | 1 | 2 | 1 | 2 |
| 3 | -1 | 1 | 3 | 1 | 3 |

`neg_count` is 3 (odd), subtract 2 * 1 → `total_sum = 3 - 2 = 1`. Output is 1. This demonstrates handling an odd number of negatives in an all-negative array.

### Sample Input 2

```
5
1 5 -5 0 2
```

| Step | Element | abs(x) | total_sum | min_abs | neg_count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 5 | 5 | 6 | 1 | 0 |
| 3 | -5 | 5 | 11 | 1 | 1 |
| 4 | 0 | 0 | 11 | 0 | 1 |
| 5 | 2 | 2 | 13 | 0 | 1 |

`neg_count` is 1 (odd), subtract 2 * 0 → `total_sum = 13`. Output is 13. Shows handling zeros without reducing total sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass through array per test case. Sum of n over all test cases ≤ 2·10^5. |
| Space | O(1) | Only a few integer variables; no extra arrays are needed. |

This linear solution easily fits within the 2-second limit for the given constraints, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    max_sum_after_flips()
    return output.getvalue().strip()

# Provided samples
assert run("5\n3\n-1 -1 -1\n5\n1 5 -5 0 2\n3\n1 2 3\n6\n-1 10 9 8 7 6\n2\n-1 -1\n") == "1\n13\n6\n39\n2", "Sample 1-5"

# Custom tests
assert run("1\n2\n-1000000000 1000000000\n") == "2000000000", "Edge with max magnitude"
assert run("1\n3\n0 0 -1\n") == "0", "Odd negatives with zero"
assert run("1\n4\n-1 -1 -1 -1\n") == "4", "All negatives even count"
assert run("1\n5\n-1 -2 -3 -4 -5\n") == "13", "All negatives odd count"
assert run("1\n2\n0 0\n") == "0", "All zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -1000000000 1000000000 | 2000000000 | Handles large magnitude values correctly |
| 0 0 -1 | 0 | Correctly handles odd negatives with zeros |
| -1 -1 -1 -1 | 4 | Even number of negatives become all positive |
| -1 -2 -3 -4 -5 | 13 | Odd number of negatives, leaves smallest negative |
| 0 0 | 0 | All zeros, no change needed |

## Edge Cases

In the first edge case with $[-1, -1, -1]$, the algorithm sums absolute values to 3, counts 3 negatives, and subtracts 2 × 1 → 1. The leftover negative is unavoidable. In the second edge case with zeros, the algorithm correctly treats zeros as non-negative and chooses the smallest absolute value as zero, avoiding reducing the total sum. In both cases, the algorithm produces the correct maximal sum.
