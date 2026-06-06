---
title: "CF 433B - Kuriyama Mirai's Stones"
description: "We have a sequence of stones, each with a numeric cost. Kuriyama Mirai wants to ask two types of questions repeatedly: in the first type, she asks for the sum of the costs of stones in a contiguous segment of the original sequence; in the second type, she asks for the sum of the…"
date: "2026-06-07T02:42:48+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 433
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 248 (Div. 2)"
rating: 1200
weight: 433
solve_time_s: 66
verified: true
draft: false
---

[CF 433B - Kuriyama Mirai's Stones](https://codeforces.com/problemset/problem/433/B)

**Rating:** 1200  
**Tags:** dp, implementation, sortings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of stones, each with a numeric cost. Kuriyama Mirai wants to ask two types of questions repeatedly: in the first type, she asks for the sum of the costs of stones in a contiguous segment of the original sequence; in the second type, she asks for the sum of the costs of stones in the same segment but after sorting all the stones by cost in non-decreasing order.

The input first gives the number of stones, then their individual costs, followed by the number of questions and the questions themselves. Each question provides the type (1 or 2) and the segment boundaries. The output is the sum corresponding to that query.

Given that there can be up to 100,000 stones and 100,000 queries, a naive approach that sums a segment for each query directly would take O(n * m) operations in the worst case. This could be as high as 10^10 operations, far exceeding reasonable limits for a 2-second time limit. Thus, we need an approach that can handle multiple queries efficiently, ideally in O(1) per query after preprocessing.

Non-obvious edge cases include segments of length 1, where l equals r, segments that cover the entire array, and arrays with all stones of equal value. A careless solution might mix 1-based and 0-based indexing, or forget that sums can exceed 32-bit integers, leading to overflow. For example, an array `v = [10^9, 10^9, 10^9]` and query `1 1 3` should return 3*10^9, which does not fit in a 32-bit signed integer.

## Approaches

The brute-force approach is simple: for each query, iterate over the segment indices and sum the values. This is correct because it directly implements the problem statement. However, the worst-case scenario of 100,000 stones and 100,000 queries results in O(n*m) operations, which is far too slow.

The key insight is that both types of queries ask for sums of contiguous segments. For any array, if we precompute a prefix sum array, then the sum of any segment `[l, r]` can be computed in O(1) using the formula `prefix[r] - prefix[l-1]`. For type 2 queries, we first sort the original array and compute its prefix sums. This reduces the per-query time to O(1), while the preprocessing takes O(n log n) for sorting and O(n) for prefix sums.

The brute-force approach works because it directly sums the requested elements, but it fails for large inputs. The observation that segment sums can be reduced to prefix sums lets us answer each query in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Prefix Sum + Sorting | O(n log n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of stones `n` and the stone costs array `v`.
2. Construct a prefix sum array `prefix_original` for `v` where `prefix_original[i] = v[0] + ... + v[i]`. This allows O(1) sum queries on the original array.
3. Make a copy of `v` and sort it to get `v_sorted`. Construct a prefix sum array `prefix_sorted` for the sorted array.
4. Read the number of queries `m`.
5. For each query `(type, l, r)`:

- If `type` is 1, compute the sum as `prefix_original[r] - prefix_original[l-1]`.
- If `type` is 2, compute the sum as `prefix_sorted[r] - prefix_sorted[l-1]`.
6. Output the result for each query.

This works because the prefix sum array maintains the invariant that `prefix[i]` equals the sum of all elements from index 1 to i. Subtracting two prefix sums gives exactly the sum of the elements between those indices, making it impossible to miscalculate a segment sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
v = list(map(int, input().split()))

# prefix sum for the original array
prefix_original = [0] * (n + 1)
for i in range(1, n + 1):
    prefix_original[i] = prefix_original[i - 1] + v[i - 1]

# prefix sum for the sorted array
v_sorted = sorted(v)
prefix_sorted = [0] * (n + 1)
for i in range(1, n + 1):
    prefix_sorted[i] = prefix_sorted[i - 1] + v_sorted[i - 1]

m = int(input())
for _ in range(m):
    t, l, r = map(int, input().split())
    if t == 1:
        print(prefix_original[r] - prefix_original[l - 1])
    else:
        print(prefix_sorted[r] - prefix_sorted[l - 1])
```

The solution first constructs prefix sums to avoid repeated summation. Using `n+1` length arrays with a leading 0 simplifies boundary handling and ensures that sums for segments starting at index 1 are correct without special cases. Sorting creates the array for type 2 queries, and the same prefix sum trick applies. Care is taken to read input efficiently with `sys.stdin.readline`.

## Worked Examples

**Sample 1 Input:**

```
6
6 4 2 7 2 7
3
2 3 6
1 3 4
1 1 6
```

| Step | prefix_original | prefix_sorted | Query | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | [0,6,10,12,19,21,28] | [0,2,4,6,11,18,25] | 2 3 6 | prefix_sorted[6]-prefix_sorted[2] = 25-4 | 21 |
| Second |  |  | 1 3 4 | prefix_original[4]-prefix_original[2]=19-10 | 9 |
| Third |  |  | 1 1 6 | prefix_original[6]-prefix_original[0]=28-0 | 28 |

This demonstrates that prefix sums give constant-time answers for any segment.

**Custom Input:**

```
5
1 1 1 1 1
2
1 1 5
2 1 5
```

| Step | prefix_original | prefix_sorted | Query | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | [0,1,2,3,4,5] | [0,1,2,3,4,5] | 1 1 5 | 5-0 | 5 |
| Second |  |  | 2 1 5 | 5-0 | 5 |

This shows the algorithm correctly handles all-equal elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting takes O(n log n), computing prefix sums takes O(n), each of the m queries is O(1) |
| Space | O(n) | Two prefix sum arrays of size n+1, plus sorted copy |

Given n, m ≤ 10^5, this fits comfortably in 2 seconds and uses well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n = int(input())
    v = list(map(int, input().split()))
    prefix_original = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_original[i] = prefix_original[i - 1] + v[i - 1]
    v_sorted = sorted(v)
    prefix_sorted = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sorted[i] = prefix_sorted[i - 1] + v_sorted[i - 1]
    m = int(input())
    for _ in range(m):
        t, l, r = map(int, input().split())
        if t == 1:
            print(prefix_original[r] - prefix_original[l - 1])
        else:
            print(prefix_sorted[r] - prefix_sorted[l - 1])
    return output.getvalue().strip()

# provided sample
assert run("6\n6 4 2 7 2 7\n3\n2 3 6\n1 3 4\n1 1 6\n") == "24\n9\n28", "sample 1"

# all equal
assert run("5\n1 1 1 1 1\n2\n1 1 5\n2 1 5\n") == "5\n5", "all equal"

# single element
assert run("1\n42\n2\n1 1 1\n2 1 1\n") == "42\n42", "single element"

# large values
assert run("3\n1000000000 1000000000 1000000000\n1\n1 1 3\n") == "3000000000", "overflow test"

# segment of length 1
assert run("4\n3 1 4 1
```
