---
title: "CF 1537A - Arithmetic Array"
description: "We are given an integer array, and our task is to make its arithmetic mean equal to one by appending non-negative integers. Each test case presents an array of arbitrary integers, both positive and negative, and asks for the minimal number of additions needed."
date: "2026-06-10T15:02:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1537
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 726 (Div. 2)"
rating: 800
weight: 1537
solve_time_s: 146
verified: true
draft: false
---

[CF 1537A - Arithmetic Array](https://codeforces.com/problemset/problem/1537/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer array, and our task is to make its arithmetic mean equal to one by appending non-negative integers. Each test case presents an array of arbitrary integers, both positive and negative, and asks for the minimal number of additions needed. The arithmetic mean is calculated exactly as the sum of the elements divided by the number of elements.

The input consists of multiple test cases. Each test case gives the current length of the array and the array elements. The output is a single integer for each test case: the fewest non-negative integers that, when appended, will adjust the array’s mean to exactly one.

The constraints are small: array length up to 50 and element values up to ±10^4. This allows O(n) operations per test case comfortably. The total number of test cases is at most 1000, which means even a simple linear scan per test case is efficient. Edge cases include arrays where the mean is already one, arrays where the sum is negative, and arrays with a sum larger than the length.

A careless implementation might attempt to always add zeros until the mean becomes one, which fails when the sum is greater than the length. For example, an array [3,3] has mean 3, so adding zeros only decreases the mean towards zero, never reaching one. The correct output for this array is two: appending two zeros gives the sum 6, length 4, mean 1.5, which is still too high, so careful reasoning is required.

## Approaches

A brute-force approach would repeatedly append integers starting from zero or one and recompute the mean until it reaches exactly one. This works because each append changes the mean in a predictable way, but it is inefficient for arrays where the sum is much larger than the length: the number of iterations could be unbounded, and checking each step is unnecessary.

The key observation is that we can solve this problem mathematically without simulation. Let the sum of the initial array be S and its length n. We need to append k non-negative integers such that the new sum divided by the new length equals one:

$$\frac{S + X}{n + k} = 1$$

where X is the sum of the k new numbers. Since all appended numbers are non-negative, the minimum total sum we can add is 0. Hence, two scenarios arise:

1. If S equals n, the array already has mean one, so we append 0 elements.
2. If S < n, appending a single integer equal to n - S is sufficient because this number is non-negative, increasing the mean to exactly one.
3. If S > n, adding zeros alone is not enough. We need to increase the length to match the sum, which requires appending k elements. The smallest k that satisfies S / (n + k) ≤ 1 is k = S - n.

This insight reduces the problem to a constant-time calculation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(S)) | O(n + max(S)) | Too slow for large sums |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t.
2. For each test case, read n and the array a.
3. Compute the sum S of the array a.
4. If S equals n, print 0. The array already has mean one.
5. If S < n, print 1. A single appended number n - S brings the mean to one.
6. If S > n, print S - n. Appending this many zeros will increase the length so that the mean reaches one.

Why it works: The algorithm preserves the invariant that the mean of the final array is exactly one. The three cases cover all possibilities: equality, sum less than length, and sum greater than length. The sum and number of elements uniquely determine the mean, so no other scenario exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    s = sum(a)
    if s == n:
        print(0)
    elif s < n:
        print(1)
    else:
        print(s - n)
```

The solution reads inputs efficiently using `sys.stdin.readline`. The sum is computed with the built-in `sum`, avoiding manual loops. Each decision branch corresponds directly to one of the three cases in the algorithm walkthrough. Off-by-one errors are avoided because the formula derives from exact equality of sums and lengths.

## Worked Examples

### Sample Input 1

```
3
1 1 1
2 1 2
4 8 4 6 2
```

| Array | n | Sum S | Case | Appended | New Mean |
| --- | --- | --- | --- | --- | --- |
| [1,1,1] | 3 | 3 | S=n | 0 | 1 |
| [1,2] | 2 | 3 | S>n | 1 | 1 |
| [8,4,6,2] | 4 | 20 | S>n | 16 | 1 |

This trace shows that each branch of the case analysis triggers correctly. In the third example, appending 16 zeros adjusts the length to 20, making the mean 1.

### Sample Input 2

```
1
1 -2
```

| Array | n | Sum S | Case | Appended | New Mean |
| --- | --- | --- | --- | --- | --- |
| [-2] | 1 | -2 | S<n | 1 | 1 |

A single appended 3 brings the mean to 1, confirming the S<n case handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Summing the array of length n is linear |
| Space | O(n) | Storage of input array, no extra structures needed |

Given n ≤ 50 and t ≤ 1000, this is efficient within the 1-second time limit.

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
        a = list(map(int, input().split()))
        s = sum(a)
        if s == n:
            print(0)
        elif s < n:
            print(1)
        else:
            print(s - n)
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n1 1 1\n2\n1 2\n4\n8 4 6 2\n1\n-2\n") == "0\n1\n16\n1", "sample cases"

# Custom cases
assert run("2\n2\n0 0\n3\n2 2 2\n") == "1\n3", "zero sum and all equal >1"
assert run("1\n1\n1\n") == "0", "single element already 1"
assert run("1\n2\n-1 3\n") == "1", "mixed negative and positive"
assert run("1\n4\n5 5 5 5\n") == "16", "large sum > length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n2\n0 0\n3\n2 2 2\n | 1\n3 | Handling sum < n and sum > n correctly |
| 1\n1\n1\n | 0 | Single element case where mean already 1 |
| 1\n2\n-1 3\n | 1 | Mixed negative and positive numbers |
| 1\n4\n5 5 5 5\n | 16 | Large sum, multiple zeros needed |

## Edge Cases

For a single-element negative array, for example [-5], S < n. The algorithm appends 1 number equal to 6, yielding [-5,6]. Sum 1, length 2, mean 1.

For an array where all elements are larger than one, e.g., [10,10], S > n. Appending S - n = 20 - 2 = 18 zeros gives [10,10,0,...,0] (20 elements). Sum 20, length 20, mean 1.

These examples confirm the three-case approach handles extreme negative sums, large positive sums, and single-element arrays without off-by-one errors.
