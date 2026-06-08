---
title: "CF 1878C - Vasilije in Cacak"
description: "The problem asks whether we can pick exactly k distinct integers from the set {1, 2, ..., n} such that their sum equals x. Each test case provides three integers: n, the upper bound of the numbers we can choose; k, the number of elements we must select; and x, the target sum."
date: "2026-06-08T22:50:18+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1878
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 900 (Div. 3)"
rating: 900
weight: 1878
solve_time_s: 87
verified: true
draft: false
---

[CF 1878C - Vasilije in Cacak](https://codeforces.com/problemset/problem/1878/C)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether we can pick exactly `k` distinct integers from the set `{1, 2, ..., n}` such that their sum equals `x`. Each test case provides three integers: `n`, the upper bound of the numbers we can choose; `k`, the number of elements we must select; and `x`, the target sum. The output should be "YES" if such a selection is possible and "NO" otherwise.

The constraints indicate that `n` can be as large as 200,000 and `x` can be up to 40 billion, with up to 10,000 test cases. A brute-force attempt to enumerate all combinations would be infeasible because the number of k-element subsets grows combinatorially with `n` and `k`. We therefore need a solution that works in constant or linear time per test case.

Edge cases that are easy to overlook include situations where the sum is smaller than the minimum possible sum for `k` elements, or larger than the maximum possible sum. For example, if `n = 5`, `k = 3`, and `x = 3`, the smallest sum of three distinct numbers is `1 + 2 + 3 = 6`, so the answer must be "NO". Similarly, if `x` exceeds the sum of the `k` largest numbers in `{1..n}`, it is impossible.

## Approaches

The brute-force approach would be to generate all combinations of `k` numbers between `1` and `n` and check whether any of them sum to `x`. This is correct but extremely slow: the number of combinations is `C(n, k)`, which for the maximum values of `n` and `k` can exceed 10^150, far beyond feasible computation.

The key insight is to recognize that the minimum sum of `k` distinct numbers is always the sum of the first `k` natural numbers, `1 + 2 + ... + k = k*(k+1)/2`. Similarly, the maximum sum is the sum of the largest `k` numbers, `n + (n-1) + ... + (n-k+1) = k*(2n - k + 1)/2`. If `x` is smaller than the minimum sum or larger than the maximum sum, the answer is immediately "NO". Otherwise, it is possible to pick numbers in the middle to exactly reach `x`. This gives a constant-time check for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k)) | O(k) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `k`, and `x`.
2. Compute the minimum possible sum of `k` distinct numbers as `min_sum = k*(k+1)//2`. This sum uses the first `k` positive integers.
3. Compute the maximum possible sum as `max_sum = k*(2*n - k + 1)//2`. This sum uses the largest `k` integers from `1` to `n`.
4. Compare `x` with `min_sum` and `max_sum`. If `x` lies outside the interval `[min_sum, max_sum]`, output "NO".
5. Otherwise, output "YES".

Why it works: Any sum outside `[min_sum, max_sum]` cannot be obtained because the elements are distinct and bounded by 1 and `n`. Any sum within the interval can be reached by starting with the first `k` numbers and incrementally increasing elements to approach `x` without exceeding `n`. The algorithm leverages this property without explicitly constructing the sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, k, x = map(int, input().split())
        min_sum = k * (k + 1) // 2
        max_sum = k * (2 * n - k + 1) // 2
        if x < min_sum or x > max_sum:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    main()
```

The code reads the number of test cases and then processes each by computing the minimum and maximum sums for `k` elements. The comparison checks are done with integers, avoiding overflow by using Python's arbitrary-precision arithmetic. This avoids any pitfalls with large `x` values up to 4*10^10. Edge cases with `k = 1` or `k = n` are handled automatically since the formulas still produce correct min and max sums.

## Worked Examples

Sample Input 1: `5 3 10`

| Step | min_sum | max_sum | x | Output |
| --- | --- | --- | --- | --- |
| Compute | 6 | 12 | 10 | YES |

Explanation: The sum 10 lies between 6 and 12, so it is possible.

Sample Input 2: `5 3 3`

| Step | min_sum | max_sum | x | Output |
| --- | --- | --- | --- | --- |
| Compute | 6 | 12 | 3 | NO |

Explanation: 3 is below the minimum sum of 3 elements, so it is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations and comparisons are performed per test case |
| Space | O(1) | No additional storage beyond the input values |

With up to 10^4 test cases, the total time complexity is O(t), which fits comfortably in 1 second even with Python. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# provided samples
assert run("""12
5 3 10
5 3 3
10 10 55
6 5 20
2 1 26
187856 87856 2609202300
200000 190000 19000000000
28 5 2004
2 2 2006
9 6 40
47202 32455 613407217
185977 145541 15770805980
""") == """YES
NO
YES
YES
NO
NO
YES
NO
NO
NO
YES
YES""", "sample 1"

# custom cases
assert run("1\n1 1 1\n") == "YES", "single element"
assert run("1\n1 1 2\n") == "NO", "single element too large"
assert run("1\n10 10 55\n") == "YES", "full sum of all elements"
assert run("1\n10 10 56\n") == "NO", "full sum exceeded"
assert run("1\n5 2 5\n") == "YES", "middle sum achievable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | YES | Minimum-size input |
| 1 1 2 | NO | Single element exceeding `n` |
| 10 10 55 | YES | Maximum-size selection sum |
| 10 10 56 | NO | Maximum-size selection exceeding sum |
| 5 2 5 | YES | Achievable sum inside range |

## Edge Cases

For `n = 1, k = 1, x = 1`, `min_sum` and `max_sum` both equal 1, so the algorithm outputs "YES" correctly. For `n = 1, k = 1, x = 2`, `x` exceeds `max_sum = 1`, so it outputs "NO". For `k = n`, the sums automatically check whether `x` equals the sum of all numbers. Large `n` and `k` with large `x` are correctly handled due to Python integers. This ensures all edge cases are treated uniformly.
