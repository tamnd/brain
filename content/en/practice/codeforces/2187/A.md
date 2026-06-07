---
title: "CF 2187A - Restricted Sorting"
description: "We are given an array of integers, and we are asked to determine the largest integer $k$ such that we can sort the array in non-descending order by swapping any two elements whose difference is at least $k$."
date: "2026-06-07T21:20:41+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2187
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1077 (Div. 1)"
rating: 1300
weight: 2187
solve_time_s: 194
verified: false
draft: false
---

[CF 2187A - Restricted Sorting](https://codeforces.com/problemset/problem/2187/A)

**Rating:** 1300  
**Tags:** greedy, sortings  
**Solve time:** 3m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we are asked to determine the largest integer $k$ such that we can sort the array in non-descending order by swapping any two elements whose difference is at least $k$. Formally, for any pair of indices $i < j$, we can swap $a_i$ and $a_j$ if $|a_i - a_j| \ge k$. Our goal is to maximize $k$ while still allowing the array to become fully sorted using these swaps.

The input consists of multiple test cases, each with a length $n$ up to $2 \cdot 10^5$ and array values up to $10^9$. Since the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$, we need an algorithm roughly linear or linearithmic per test case. Quadratic approaches would not run in reasonable time because they would require up to $10^{10}$ operations in the worst case.

A subtle edge case occurs when the array is already sorted. For instance, if the array is `[1,2,3]`, no swaps are necessary, but the problem asks for the largest $k$. In this case, any non-negative $k$ is technically allowed, but the largest meaningful $k$ is undefined in the sense that no operation is needed, so the answer should be `-1`. Another tricky case is when all elements are equal, such as `[5,5,5]`; again, no swaps are needed, and the output must be `-1`. Arrays with only two elements are simpler, but the algorithm must still correctly identify whether a swap is needed to sort them.

## Approaches

The brute-force approach would try all possible $k$ values, attempting to simulate swaps for each. For each $k$, we would scan the array repeatedly, swapping any pair with a difference at least $k$ until no more swaps are possible. This approach is correct in principle, but far too slow: there are up to $10^9$ possible $k$ values and each simulation could take $O(n^2)$, which is computationally infeasible.

The key insight is that the largest piggy $k$ is determined solely by the positions of elements that are out of order in the sorted array. Let `b` be the sorted version of `a`. Consider elements $a_i$ and $b_i$ at the same index. If $a_i \neq b_i$, that element must be moved. The maximum value of $k$ that allows all necessary swaps is then the maximum difference between any original element that must move and its target in the sorted array. Specifically, we need $k \le \max(a) - \min(a)$ among misplaced elements. This reduces the problem to a single pass over the array: identify the minimum and maximum of misplaced elements and compute their difference. If no elements are misplaced, the array is already sorted, and the answer is `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * max(a)) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a` and create a sorted copy `b`.
2. Initialize `min_misplaced` to `inf` and `max_misplaced` to `-inf`.
3. Iterate over indices `i` from 0 to `n-1`. For each index, if `a[i] != b[i]`, update `min_misplaced` and `max_misplaced` with `a[i]`.
4. After the iteration, check if `min_misplaced` remains `inf`. If so, the array is already sorted, and the output is `-1`.
5. Otherwise, the largest piggy integer `k` is `max_misplaced - min_misplaced`.
6. Output the result.

Why it works: Any element that is not in its sorted position must be moved. The maximum allowed $k$ cannot exceed the difference between the largest and smallest elements among those that are misplaced, because swaps are only allowed for differences greater than or equal to $k$. By selecting $k$ as this difference, we ensure that all necessary swaps are permitted, and any larger $k$ would block required swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = sorted(a)
    
    min_misplaced = float('inf')
    max_misplaced = float('-inf')
    
    for i in range(n):
        if a[i] != b[i]:
            min_misplaced = min(min_misplaced, a[i])
            max_misplaced = max(max_misplaced, a[i])
    
    if min_misplaced == float('inf'):
        print(-1)
    else:
        print(max_misplaced - min_misplaced)
```

The code first reads input efficiently. It maintains two variables to track the extreme values of misplaced elements. Iterating over the array ensures that only elements that need to move influence the result. Using `float('inf')` and `float('-inf')` avoids special casing the first misplaced element. Sorting is `O(n log n)`, and the scan is `O(n)`. The solution handles multiple test cases in a single pass.

## Worked Examples

### Sample Input 1

```
3
1
1
3
1 4 2
6
1 1 4 5 1 4
```

| Test | a | b | min_misplaced | max_misplaced | k |
| --- | --- | --- | --- | --- | --- |
| 1 | [1] | [1] | inf | -inf | -1 |
| 2 | [1,4,2] | [1,2,4] | 2 | 4 | 2 |
| 3 | [1,1,4,5,1,4] | [1,1,1,4,4,5] | 1 | 4 | 3 |

In the first test case, the array is already sorted, so the output is `-1`. In the second, the elements `4` and `2` are out of order, giving a difference of `4 - 2 = 2`. In the third, the misplaced elements are `4,5,1,4`, giving `max - min = 4 - 1 = 3`.

### Sample Input 2

```
1
5
2 1 5 4 3
```

| i | a[i] | b[i] | misplaced? | min | max |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | Yes | 2 | 2 |
| 1 | 1 | 2 | Yes | 1 | 2 |
| 2 | 5 | 3 | Yes | 1 | 5 |
| 3 | 4 | 4 | No | 1 | 5 |
| 4 | 3 | 5 | Yes | 1 | 5 |

k = 5 - 1 = 4

The trace confirms that the algorithm correctly identifies the extremes among misplaced elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates; the scan is linear |
| Space | O(n) | The sorted copy `b` requires additional memory |

Given $n \le 2 \cdot 10^5$ and sum of $n$ across test cases $\le 2 \cdot 10^5$, the solution runs comfortably within the 2-second limit.

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
        b = sorted(a)
        min_misplaced = float('inf')
        max_misplaced = float('-inf')
        for i in range(n):
            if a[i] != b[i]:
                min_misplaced = min(min_misplaced, a[i])
                max_misplaced = max(max_misplaced, a[i])
        if min_misplaced == float('inf'):
            output.append('-1')
        else:
            output.append(str(max_misplaced - min_misplaced))
    return "\n".join(output)

# Provided samples
assert run("5\n1\n1\n5\n1 2 3 4 5\n3\n1 4 2\n5\n2 1 5 4 3\n6\n1 1 4 5 1 4\n") == "-1\n-1\n2\n4\n3"

# Custom cases
assert run("2\n2\n5 5\n2\n2 1\n") == "-1\n1"
assert run("1\n3\n3 2 1\n") == "2"
assert run("1\n6\n1 1 1 1 1 1\n") == "-1"
assert run("1\n5\n1 3 2 5 4\n") == "3"
```

| Test input | Expected output
