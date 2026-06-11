---
title: "CF 1372A - Omkar and Completion"
description: "We are asked to construct arrays of a given length such that each element is positive, no greater than 1000, and no element equals the sum of any two elements in the array, including sums where the same element is counted twice."
date: "2026-06-11T11:17:29+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1372
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 655 (Div. 2)"
rating: 800
weight: 1372
solve_time_s: 128
verified: false
draft: false
---

[CF 1372A - Omkar and Completion](https://codeforces.com/problemset/problem/1372/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct arrays of a given length such that each element is positive, no greater than 1000, and no element equals the sum of any two elements in the array, including sums where the same element is counted twice. In other words, for any indices x, y, z, the relation a[x] + a[y] ≠ a[z] must hold. The input gives multiple test cases, each with a single integer n, and for each test case we must output a valid array of length n.

The constraints are fairly small. n can go up to 1000, and the sum of n over all test cases is also at most 1000. This means we can afford an O(n) or even O(n log n) solution per test case without risking timeouts, because the total number of operations across all test cases will remain well below 10^6.

A subtle edge case is arrays with n = 1. In that case, any single positive integer less than or equal to 1000 works, because there is no pair of elements to sum. Another edge case is n = 1000. The naive approach of randomly selecting numbers and checking sums could fail here or exceed limits if we are not careful, so we need a deterministic approach. Finally, we need to avoid elements exceeding 1000, which rules out certain sequences like powers of two if n is large.

## Approaches

A brute-force approach would be to try all possible arrays of length n with elements in [1, 1000], and for each candidate, check whether every sum of two elements equals any array element. This is correct but infeasible: for n = 1000, we would have 1000^1000 possibilities, and even generating all pairs to check sums takes O(n^3) time, which is far too large.

The key insight comes from the structure of the condition: we only need to avoid any element being equal to the sum of two elements. One simple way is to choose an arithmetic progression with a sufficiently large common difference. For instance, if we pick consecutive odd numbers starting from 1 (1, 3, 5, 7,...), the sum of any two numbers is even, whereas all elements themselves are odd. Therefore, no element can equal the sum of any two elements. This observation lets us construct arrays of arbitrary length up to n = 1000 easily and ensures all elements are positive and below 1000. Choosing the first 1000 odd numbers works because the largest element, 1999, is beyond 1000. To fix this, we can use any sequence with a large enough step that keeps all elements ≤ 1000, for instance multiples of 1 (1, 2, 3...) works too, but we need a gap: the simplest is choosing all numbers equal to 1. Then the sum of any two elements is 2, which is different from any element. For any n, using an array of n ones works perfectly and is within bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t.
2. For each test case, read n, the desired length of the array.
3. Construct an array of length n, filling every element with 1. This guarantees that each element is positive, ≤ 1000, and no sum of two elements equals any element, because 1 + 1 = 2 ≠ 1.
4. Output the array on a single line.

Why it works: the invariant we maintain is that all elements are equal to 1. Therefore the sum of any two elements is always 2, which can never appear in the array. This directly satisfies the complete array condition. All elements are within the allowed bounds, and we can repeat this approach for any n ≤ 1000.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    print("1 " * n)
```

The code reads t test cases, then for each test case reads n and prints n ones separated by spaces. We multiply the string "1 " by n to generate the output efficiently. This method avoids loops in output construction and ensures no off-by-one errors. We rely on Python handling the trailing space correctly when printing; it does not affect the output validity.

## Worked Examples

### Example 1

Input:

```
2
5
4
```

| Step | n | Constructed array |
| --- | --- | --- |
| 1 | 5 | [1, 1, 1, 1, 1] |
| 2 | 4 | [1, 1, 1, 1] |

Both arrays satisfy the invariant: the sum of any two elements is 2, which does not appear in the array.

### Example 2

Input:

```
1
1
```

| Step | n | Constructed array |
| --- | --- | --- |
| 1 | 1 | [1] |

With a single element, the array trivially satisfies the condition since there is no pair to sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We generate n elements in linear time |
| Space | O(n) per test case | We store n elements to print |

Given the constraints n ≤ 1000 and total n across test cases ≤ 1000, this solution easily fits within the 1-second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        print("1 " * n)
    return output.getvalue().strip()

# provided samples
assert run("2\n5\n4\n") == "1 1 1 1 1\n1 1 1 1", "sample 1"
# custom cases
assert run("1\n1\n") == "1", "single element"
assert run("1\n1000\n") == "1 " * 1000, "maximum size input"
assert run("2\n2\n3\n") == "1 1\n1 1 1", "small arrays"
assert run("1\n10\n") == "1 1 1 1 1 1 1 1 1 1", "moderate size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single element edge case |
| 1000 | 1 repeated 1000 times | maximum size array |
| 2,3 | arrays of different small sizes | correctness across multiple test cases |
| 10 | array of 10 ones | correctness for arbitrary small n |

## Edge Cases

For n = 1, the algorithm returns [1]. The sum condition is vacuously satisfied since there are no two elements to sum.

For n = 1000, the algorithm returns an array of 1000 ones. The sum of any two elements is 2, which does not appear in the array. All elements are within the allowed range.

This approach handles the minimum, maximum, and any intermediate n without violating any constraints.
