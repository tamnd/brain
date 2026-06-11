---
title: "CF 1117A - Best Subsegment"
description: "We are given an array of integers and may choose any contiguous subarray. For every chosen subarray, we can compute its arithmetic mean, which is the sum of its elements divided by its length. The task is to find the maximum possible mean among all subarrays."
date: "2026-06-12T04:42:16+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1117
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 60 (Rated for Div. 2)"
rating: 1100
weight: 1117
solve_time_s: 330
verified: false
draft: false
---

[CF 1117A - Best Subsegment](https://codeforces.com/problemset/problem/1117/A)

**Rating:** 1100  
**Tags:** implementation, math  
**Solve time:** 5m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and may choose any contiguous subarray. For every chosen subarray, we can compute its arithmetic mean, which is the sum of its elements divided by its length.

The task is to find the maximum possible mean among all subarrays. If several subarrays achieve that same maximum mean, we must output the length of the longest such subarray.

The array length is at most $10^5$, which immediately rules out any approach that examines all $O(n^2)$ subarrays. Even computing the mean of every subarray with prefix sums would still require around $5 \cdot 10^9$ subarrays in the worst case, which is far beyond what can be processed within one second.

The values themselves can be as large as $10^9$, so sums may become large. Python handles this automatically, but in languages with fixed-width integers we would need 64-bit arithmetic.

The tricky part is understanding what the maximum possible average can be.

Consider the array:

```
5
3 7 2 5 1
```

The maximum element is 7. No subarray can have average greater than 7 because every element contributing to the average is at most 7. The single-element subarray `[7]` achieves average 7, so the maximum possible average is exactly 7.

Another subtle case is when the maximum value appears consecutively:

```
5
4 9 9 9 2
```

The subarray `[9,9,9]` has average 9. Any shorter subarray consisting only of 9s also has average 9, but the problem asks for the longest one. The correct answer is 3.

A careless solution might only count how many times the maximum value appears in the whole array. That fails on:

```
5
9 1 9 1 9
```

The maximum value appears three times, but no contiguous segment of length 3 consists entirely of 9s. The longest valid segment has length 1.

## Approaches

A brute-force solution would enumerate every subarray, compute its average, keep track of the largest average found, and among those choose the longest length.

With prefix sums, each average can be computed in constant time, but there are still $O(n^2)$ subarrays. For $n=10^5$, this means roughly five billion candidates, which is completely infeasible.

The key observation comes from a simple property of averages.

Let $M$ be the maximum value in the array.

No subarray can have average greater than $M$, because every element inside that subarray is at most $M$. An average can never exceed the largest value being averaged.

At the same time, any subarray consisting entirely of elements equal to $M$ has average exactly $M$.

This immediately tells us that the maximum achievable average is always $M$.

Now the problem becomes much simpler. Which subarrays have average exactly $M$?

Suppose a subarray contains at least one element smaller than $M$. Since all elements are at most $M$, introducing even a single smaller value forces the average below $M$.

So a subarray achieves average $M$ if and only if every element in it equals $M$.

The answer is simply the length of the longest consecutive block of maximum elements.

We first find the maximum value in the array, then scan the array and compute the longest run consisting entirely of that value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ or $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the array.
2. Compute the maximum value $M$ in the array.
3. Scan the array from left to right while maintaining the length of the current consecutive run of values equal to $M$.
4. When the current element equals $M$, increase the current run length by one.
5. When the current element is smaller than $M$, end the current run and reset its length to zero.
6. Maintain the largest run length seen during the scan.
7. Output the largest run length.

### Why it works

The largest element in the array is $M$. Since every array element is at most $M$, no subarray can have average greater than $M$.

A subarray has average exactly $M$ only when every element inside it equals $M$. If even one element is smaller than $M$, the average becomes strictly less than $M$.

Thus every optimal subarray is precisely a contiguous block of maximum elements. Among all such blocks, the problem asks for the longest one. The scan computes exactly that quantity, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    best = 0
    cur = 0

    for x in a:
        if x == mx:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0

    print(best)

if __name__ == "__main__":
    solve()
```

The first step is finding the maximum element. This determines the highest possible average any subarray can achieve.

The scan that follows keeps two variables. `cur` stores the length of the current consecutive block of maximum elements, while `best` stores the largest such block encountered so far.

Whenever a maximum element is seen, the current block extends by one. Whenever a smaller element appears, the block must end because any segment crossing that position would contain a value below the maximum and could no longer achieve the optimal average.

The update order matters slightly. We first increase `cur`, then update `best`, ensuring runs ending at the current position are counted correctly.

No special handling is required for large values because we never compute sums or averages. We only compare elements to the maximum value.

## Worked Examples

### Example 1

Input:

```
5
6 1 6 6 0
```

The maximum value is 6.

| Position | Value | Current Run | Best |
| --- | --- | --- | --- |
| 1 | 6 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 6 | 1 | 1 |
| 4 | 6 | 2 | 2 |
| 5 | 0 | 0 | 2 |

Output:

```
2
```

The trace shows two separate blocks of maximum elements. The longest block is the segment `[6, 6]`, whose length is 2.

### Example 2

Input:

```
7
5 5 5 1 5 5 2
```

The maximum value is 5.

| Position | Value | Current Run | Best |
| --- | --- | --- | --- |
| 1 | 5 | 1 | 1 |
| 2 | 5 | 2 | 2 |
| 3 | 5 | 3 | 3 |
| 4 | 1 | 0 | 3 |
| 5 | 5 | 1 | 3 |
| 6 | 5 | 2 | 3 |
| 7 | 2 | 0 | 3 |

Output:

```
3
```

This example demonstrates that separate groups of maximum values cannot be merged. Any intervening smaller value would reduce the average below the optimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to find the maximum and one pass to find the longest run |
| Space | $O(1)$ | Only a few variables are used |

With $n \le 10^5$, a linear scan is easily fast enough. The memory usage is constant aside from storing the input array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    mx = max(a)

    best = 0
    cur = 0

    for x in a:
        if x == mx:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0

    return str(best)

# provided sample
assert run("5\n6 1 6 6 0\n") == "2", "sample 1"

# minimum size
assert run("1\n7\n") == "1", "single element"

# all equal values
assert run("4\n5 5 5 5\n") == "4", "whole array"

# separated maximum values
assert run("5\n9 1 9 1 9\n") == "1", "non-contiguous maxima"

# maximum block at the end
assert run("6\n1 2 8 8 8 8\n") == "4", "suffix block"

# maximum block at the beginning
assert run("6\n10 10 10 3 2 1\n") == "3", "prefix block"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1` | Minimum array size |
| `4 / 5 5 5 5` | `4` | Entire array is optimal |
| `5 / 9 1 9 1 9` | `1` | Maximum values separated by smaller values |
| `6 / 1 2 8 8 8 8` | `4` | Longest block appears at the end |
| `6 / 10 10 10 3 2 1` | `3` | Longest block appears at the beginning |

## Edge Cases

Consider:

```
1
42
```

The maximum value is 42. The scan encounters one maximum element, so `cur = 1` and `best = 1`. The answer is 1, which is the only possible subarray.

Consider:

```
5
9 1 9 1 9
```

The maximum value is 9. The scan repeatedly starts and ends runs:

| Value | cur | best |
| --- | --- | --- |
| 9 | 1 | 1 |
| 1 | 0 | 1 |
| 9 | 1 | 1 |
| 1 | 0 | 1 |
| 9 | 1 | 1 |

The answer is 1. Counting total occurrences of 9 would incorrectly give 3, but those occurrences are not contiguous.

Consider:

```
6
7 7 7 7 7 7
```

Every element equals the maximum. The run length grows from 1 to 6 without interruption. The answer is 6, corresponding to the entire array. Since every subarray has average 7, the longest optimal one is the whole array.

Consider:

```
6
1 2 8 8 8 8
```

The longest block of maximum elements occurs at the end. The scan correctly keeps extending the run until the array finishes, producing 4. This confirms there is no off-by-one error when the optimal segment reaches the last position.
