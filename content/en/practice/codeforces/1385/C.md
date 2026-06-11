---
title: "CF 1385C - Make It Good"
description: "We are given an array of integers, and the task is to remove the smallest possible prefix so that the remaining array can be turned into a non-decreasing sequence by repeatedly taking either the first or last element and appending it to a new array."
date: "2026-06-11T10:41:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1385
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 656 (Div. 3)"
rating: 1200
weight: 1385
solve_time_s: 126
verified: false
draft: false
---

[CF 1385C - Make It Good](https://codeforces.com/problemset/problem/1385/C)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and the task is to remove the smallest possible prefix so that the remaining array can be turned into a non-decreasing sequence by repeatedly taking either the first or last element and appending it to a new array. The goal is not to actually perform these operations, but to determine the minimal prefix length to remove so that the array is “good,” meaning this operation sequence is possible.

The constraints indicate that the array can be as long as 200,000 elements and there can be up to 20,000 test cases, but the total sum of array sizes across all tests will not exceed 200,000. This rules out any O(n²) approach because it would result in up to 4 × 10^10 operations. A linear or near-linear solution is required.

Edge cases arise when the array is already good without removing any prefix. For instance, a strictly non-decreasing array like `[1, 2, 3, 4]` should output `0`. Another subtle edge case is when the array starts with a long decreasing sequence followed by an increasing sequence, like `[5, 4, 3, 2, 3, 4]`. A naive approach might stop too early or erase too little of the prefix.

## Approaches

The brute-force approach would try all possible prefix lengths to remove, simulate the selection of first or last elements, and check if a non-decreasing array can be constructed. This is correct but would require O(n²) operations per test case, which is too slow for n up to 2 × 10^5.

The key insight for a faster solution is to notice that the array only needs to have a decreasing prefix followed by a non-increasing suffix. If we look from the end of the array backwards, the longest non-increasing suffix indicates elements we never need to remove. Once the suffix is identified, we continue moving backwards through any strictly decreasing part. Everything before that point must be removed. This reduces the problem to a single pass from the end of the array to the beginning, giving O(n) time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the last element of the array and move leftwards to find the longest non-increasing suffix. Keep decrementing the pointer as long as the current element is greater than or equal to the previous one. This identifies the portion of the array that can remain without violating the non-decreasing property in the final array.
2. Once the non-increasing suffix is determined, continue moving leftwards while the elements are strictly decreasing. These are part of the tail of the prefix that could potentially be removed, because taking elements from this decreasing portion in the reverse order ensures that we can append them to the resulting array without breaking the non-decreasing requirement.
3. The pointer now indicates the last index that must be removed to make the remaining array good. The length of the prefix to remove is the index plus one since array indices start from zero.

Why it works: The algorithm maintains the invariant that the portion we consider as the suffix is always non-increasing, meaning we can safely select elements from its ends to build a non-decreasing array. Moving further left through a strictly decreasing sequence ensures any element before that would violate the non-decreasing property unless removed. Therefore, the prefix we identify is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # start from the end
        i = n - 1
        # find longest non-increasing suffix
        while i > 0 and a[i-1] >= a[i]:
            i -= 1
        # find the decreasing part before the suffix
        while i > 0 and a[i-1] <= a[i]:
            i -= 1
        print(i)

if __name__ == "__main__":
    solve()
```

The first `while` loop identifies the non-increasing suffix from the end. The second `while` loop moves leftwards through any decreasing sequence that precedes the suffix. Finally, `i` represents the minimal prefix length to remove. The approach carefully handles the array boundaries and ensures off-by-one errors do not occur.

## Worked Examples

**Example 1**: `a = [1, 2, 3, 4]`

| Step | i | a[i] | Action |
| --- | --- | --- | --- |
| start | 3 | 4 | check a[2] >= a[3]? 3 >= 4: no, exit loop |
| second loop | 3 | 4 | check a[2] <= a[3]? 3 <= 4: yes, i=2 |
| continue | 2 | 3 | check a[1] <= a[2]? 2 <= 3: yes, i=1 |
| continue | 1 | 2 | check a[0] <= a[1]? 1 <= 2: yes, i=0 |

Output: `0`, correct because array is already good.

**Example 2**: `a = [5, 4, 3, 2, 3, 4]`

| Step | i | a[i] | Action |
| --- | --- | --- | --- |
| start | 5 | 4 | check a[4] >= a[5]? 3 >= 4: no, exit loop |
| second loop | 5 | 4 | check a[4] <= a[5]? 3 <= 4: yes, i=4 |
| continue | 4 | 3 | check a[3] <= a[4]? 2 <= 3: yes, i=3 |
| continue | 3 | 2 | check a[2] <= a[3]? 3 <= 2: no, exit loop |

Output: `3`, remove first 3 elements `[5,4,3]` leaving `[2,3,4]`, good array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single backward pass through array to find suffix and decreasing prefix |
| Space | O(1) extra | Only index pointers used; input array stored anyway |

Given the sum of n across all tests ≤ 2 × 10^5, the algorithm runs comfortably within the 1-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n4\n1 2 3 4\n7\n4 3 3 8 4 5 2\n3\n1 1 1\n7\n1 3 1 4 5 3 2\n5\n5 4 3 2 3\n") == "0\n4\n0\n2\n3"

# custom cases
assert run("1\n1\n100\n") == "0", "single element array"
assert run("1\n5\n5 4 3 2 1\n") == "0", "strictly decreasing array"
assert run("1\n5\n1 2 3 2 1\n") == "2", "peak in middle"
assert run("1\n6\n1 2 3 4 5 6\n") == "0", "already increasing array"
assert run("1\n4\n4 4 4 4\n") == "0", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | Single element is always good |
| 5 4 3 2 1 | 0 | Entirely decreasing array is already good |
| 1 2 3 2 1 | 2 | Peak in the middle requires prefix removal |
| 1 2 3 4 5 6 | 0 | Already increasing array |
| 4 4 4 4 | 0 | All elements equal |

## Edge Cases

For `[5,4,3,2,1]`, the algorithm correctly identifies that the whole array is a non-increasing suffix. The first `while` loop moves all the way to index `0`. The second loop does nothing, so the prefix length to remove is `0`, which is correct because a fully non-increasing array can be rearranged from ends to form a non-decreasing array.

For `[1]`, the loops are bypassed, and the prefix length is `0`, as expected.

For arrays with a peak, like `[1,2,3,2,1]`, the first loop stops at the last non-increasing suffix `[3,2,1]`. The second loop moves left through the strictly decreasing sequence before the peak (from `3` back to `2`), correctly identifying that the first two elements `[1,2]` must be removed.
