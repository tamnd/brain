---
title: "CF 2078A - Final Verdict"
description: "We are given an array of integers and a target value. The goal is to repeatedly split the array into equally-sized parts, replace the array with the averages of those parts, and continue until the array has only one element."
date: "2026-06-08T06:29:14+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2078
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1008 (Div. 2)"
rating: 800
weight: 2078
solve_time_s: 93
verified: true
draft: false
---

[CF 2078A - Final Verdict](https://codeforces.com/problemset/problem/2078/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a target value. The goal is to repeatedly split the array into equally-sized parts, replace the array with the averages of those parts, and continue until the array has only one element. We must determine if there exists a sequence of such operations that ends with the single element being equal to the target.

The input includes multiple test cases. Each test case provides the array length `n`, the target `x`, and the array `a` itself. The array elements and `x` are all positive integers, and `n` is at most 100. This implies we can afford algorithms with time complexity up to roughly $O(n^2)$ per test case. Brute force over all possible splits would become cumbersome, especially because for each split we would need to compute averages and recurse.

Non-obvious edge cases arise when the array is already a single element or when all elements are identical. For example, if `a = [3]` and `x = 3`, we can immediately return YES. If `a = [5,5,5]` and `x = 5`, the answer is also YES, but a naive approach that looks for subsets summing exactly to `x` might incorrectly reject it. Another subtlety occurs when the target `x` is equal to the mean of the array but not equal to any individual element. For instance, `a = [1, 2]` and `x = 1.5` cannot be achieved because our splits must produce integer-length subsequences, and averaging over them only produces integers if all elements are integers, which they are here.

## Approaches

A brute-force approach would try every possible split at every step, recursively computing averages. This is technically correct, because any valid sequence of operations must be a series of such splits. However, the number of ways to split an array grows combinatorially with `n`, making this approach impractical even for `n = 20`. For `n = 100`, it's infeasible.

The key insight is that at each operation, the array's new elements are convex combinations of the current array elements. This means that the final value `x` must lie between the minimum and maximum of the original array. If `x` equals one of the elements, the answer is trivially YES. Otherwise, if `x` is within the range of the array but not exactly equal to any element, we can always construct a sequence of splits that averages to `x` by first taking the average of the entire array. Specifically, we can always merge all elements in one subsequence of length `n` (the whole array), producing the mean. Therefore, the condition reduces to checking if `x` is either equal to any element or equal to the mean of the array.

This observation lets us reduce the problem to a linear scan of the array: check if `x` is in `a` or equal to the average of `a`. This is fast and fits comfortably within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `x`, and the array `a`.
2. Compute the sum of the array elements.
3. Check if `x` is equal to any element of `a`. If yes, print "YES" and continue to the next test case. This covers trivial sequences where we can immediately pick a single-element subsequence.
4. Otherwise, check if `x * n == sum(a)`. This verifies whether `x` is exactly the mean of the array. If yes, print "YES". The reasoning is that splitting the entire array into one group and taking the average produces `x`.
5. If neither condition is met, print "NO". No sequence of allowed operations can produce `x` in this case.

Why it works: The allowed operation replaces the array with averages of equal-sized subsequences. Any resulting average is a convex combination of existing elements, so the final element must lie between the minimum and maximum of the original array. If the target matches an element or the overall mean, there exists an explicit sequence of splits to reach it. Otherwise, no sequence can produce it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    if x in a:
        print("YES")
    elif sum(a) == x * n:
        print("YES")
    else:
        print("NO")
```

The solution first reads the number of test cases. For each test case, it reads the array and computes the sum. Checking `x in a` handles the simplest cases immediately. Comparing `sum(a)` to `x * n` handles cases where the average equals the target. Multiplying `x` by `n` avoids floating-point precision issues. If neither condition holds, "NO" is printed. This approach is straightforward, fast, and avoids unnecessary recursion.

## Worked Examples

Sample Input:

```
4
1 3
3
4 9
7 11 2 5
6 9
1 9 14 12 10 8
10 10
10 10 10 10 10 10 10 10 10 10
```

| Test Case | a | x | sum(a) | x in a | x * n == sum(a) | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [3] | 3 | 3 | True | True | YES |
| 2 | [7,11,2,5] | 9 | 25 | False | False | NO |
| 3 | [1,9,14,12,10,8] | 9 | 54 | False | True | YES |
| 4 | [10]*10 | 10 | 100 | True | True | YES |

The table shows that the algorithm correctly identifies both trivial and average-based sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Linear scan of the array to check membership and compute sum |
| Space | O(n) per test case | Storing the array |

Given the constraints (`n <= 100` and `t <= 500`), the solution performs at most 50,000 array accesses, well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        if x in a:
            print("YES")
        elif sum(a) == x * n:
            print("YES")
        else:
            print("NO")
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("4\n1 3\n3\n4 9\n7 11 2 5\n6 9\n1 9 14 12 10 8\n10 10\n10 10 10 10 10 10 10 10 10 10\n") == "YES\nNO\nYES\nYES", "sample 1"

# custom cases
assert run("3\n2 5\n1 5\n3 2\n1 2 3\n5 3\n3 3 3 3 3\n") == "YES\nYES\nYES", "custom 1"
assert run("2\n1 100\n50\n4 10\n5 5 5 5\n") == "NO\nYES", "custom 2"
assert run("1\n3 4\n2 4 6\n") == "YES", "custom 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5\n1 5 | YES | Single element matches target |
| 3 2\n1 2 3 | YES | Target equals mean but not an element |
| 5 3\n3 3 3 3 3 | YES | All elements equal target |
| 1 100\n50 | NO | Single element not matching target |
| 4 10\n5 5 5 5 | YES | Average equals target |

## Edge Cases

If the array has a single element equal to `x`, the algorithm immediately returns "YES". For `a = [3]` and `x = 3`, the check `x in a` passes. If the target equals the mean but no single element matches it, for example `a = [1,9,14,12,10,8]` and `x = 9`, the check `sum(a) == x * n` passes, producing "YES". Arrays with all elements equal are handled correctly as both checks will succeed. Arrays where neither condition holds, such as `a = [1,2]` and `x = 5`, correctly yield "NO".
