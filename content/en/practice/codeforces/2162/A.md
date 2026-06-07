---
title: "CF 2162A - Beautiful Average"
description: "We are given an array of integers, each between 1 and 10, and we are asked to find the maximum average of any contiguous subarray. A subarray is simply a consecutive segment of the array, which can be as short as a single element or as long as the entire array."
date: "2026-06-07T23:53:22+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2162
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1059 (Div. 3)"
rating: 800
weight: 2162
solve_time_s: 97
verified: true
draft: false
---

[CF 2162A - Beautiful Average](https://codeforces.com/problemset/problem/2162/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, each between 1 and 10, and we are asked to find the maximum average of any contiguous subarray. A subarray is simply a consecutive segment of the array, which can be as short as a single element or as long as the entire array. The output must be an integer, which in this problem is guaranteed because all elements are integers and the maximum average occurs on one of the integers themselves.

The first constraint is that the length of the array, $n$, is at most 10. This is small enough that any solution with complexity exponential in $n$ is feasible. Each test case is independent, and there can be up to 10,000 test cases. Even if we perform $O(n^2)$ operations per test case, this would be around $10^4 \times 100 = 10^6$ operations, which is well within the 1-second limit.

A non-obvious edge case arises when all elements are equal. For instance, with the array [3, 3, 3, 3], the maximum average is 3, and any attempt to look at sums of multiple elements does not increase the result. Another subtle point is when the array has a mix of low and high values, like [1, 9, 2]; the maximum average is simply the largest element, because any combination with smaller elements would reduce the average. A careless brute-force approach that computes all subarray averages without recognizing this property may still produce the correct answer due to small constraints, but it obscures the simpler insight.

## Approaches

The naive approach is straightforward: consider every possible subarray, compute its sum, divide by its length, and track the maximum. This works because there are only $n(n+1)/2$ subarrays, which is at most 55 for $n = 10$. However, this approach does redundant work: for each subarray, it recomputes the sum from scratch, which is unnecessary for such small arrays but scales poorly for larger ones.

The key insight is that because all elements are positive integers, the subarray that maximizes the average is always the single largest element. Adding smaller elements to the subarray only decreases the average, while adding equal elements does not improve it. Therefore, we can ignore all combinations and simply take the maximum element of the array as the answer. This reduces the computation from $O(n^2)$ to $O(n)$ per test case, which is more than sufficient given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Acceptable due to small n |
| Optimal (max element) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. We process each test case independently, so we can loop over them one by one.
2. For each test case, read the length of the array $n$ and the array elements $a_1, \dots, a_n$.
3. Find the maximum element of the array using a simple linear scan. This represents the largest possible average of any subarray.
4. Print the maximum element. Since the maximum subarray average is always an integer, no rounding is needed.

Why it works: the invariant is that any subarray average is bounded by its largest element. Including smaller elements in a subarray lowers the average, and including equal elements does not increase it. Therefore, the maximum element of the array is always the maximum subarray average, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max(a))
```

The solution reads the number of test cases, then iterates through each case. We convert the line of integers into a list and use Python's built-in `max` function to find the largest element efficiently. Using `sys.stdin.readline` ensures fast input for a large number of test cases. Since `n` is very small, the overhead of the list conversion is negligible. The solution avoids unnecessary computation of sums or averages for subarrays beyond the maximum element.

## Worked Examples

Consider the input:

```
4
3 3 3 3
7 1 6 9 9
3 4 4 4 3
1 2 3
```

| Test Case | Array | Maximum Element | Output |
| --- | --- | --- | --- |
| 1 | [3, 3, 3, 3] | 3 | 3 |
| 2 | [7, 1, 6, 9, 9] | 9 | 9 |
| 3 | [3, 4, 4, 4, 3] | 4 | 4 |
| 4 | [1, 2, 3] | 3 | 3 |

This trace demonstrates that regardless of subarray length or element combination, the maximum average is achieved by the largest individual element. The table confirms that the linear scan correctly identifies it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case performs a single scan of length n, repeated for t cases |
| Space | O(n) | Storing the array of length n per test case |

Given $n \le 10$ and $t \le 10^4$, the total operations are at most 10^5, fitting comfortably in the 1-second time limit. Memory usage is minimal because we only store one array at a time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        output.append(str(max(a)))
    return "\n".join(output)

# provided samples
assert run("3\n4\n3 3 3 3\n5\n7 1 6 9 9\n5\n3 4 4 4 3\n") == "3\n9\n4"

# custom test cases
assert run("1\n1\n10\n") == "10", "single element array"
assert run("1\n10\n1 2 3 4 5 6 7 8 9 10\n") == "10", "maximum-size array"
assert run("1\n5\n5 5 5 5 5\n") == "5", "all-equal values"
assert run("2\n3\n1 10 2\n4\n2 2 9 3\n") == "10\n9", "mixed small arrays"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n10 | 10 | Single-element array edge case |
| 1\n10\n1..10 | 10 | Maximum-size array |
| 1\n5\n5 5 5 5 5 | 5 | All-equal elements |
| 2\n3\n1 10 2\n4\n2 2 9 3 | 10\n9 | Mixed values, multiple test cases |

## Edge Cases

If the array contains only one element, like [10], the algorithm outputs 10. This is correct because the only subarray is the array itself. If all elements are equal, like [5, 5, 5, 5], the algorithm outputs 5, consistent with the maximum average among any subarray. For arrays with mixed low and high values, such as [1, 10, 2], the algorithm correctly selects the largest element, 10, as the maximum subarray average, without being distracted by sums of smaller numbers.
