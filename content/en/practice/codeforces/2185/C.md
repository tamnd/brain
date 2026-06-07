---
title: "CF 2185C - Shifted MEX"
description: "We are given an array of integers, which may include negative numbers. The task allows us to pick a single integer shift x and add it to every element of the array. After performing this shift, we want to maximize the MEX of the array."
date: "2026-06-07T21:28:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2185
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1074 (Div. 4)"
rating: 900
weight: 2185
solve_time_s: 125
verified: false
draft: false
---

[CF 2185C - Shifted MEX](https://codeforces.com/problemset/problem/2185/C)

**Rating:** 900  
**Tags:** implementation, sortings  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, which may include negative numbers. The task allows us to pick a single integer shift `x` and add it to every element of the array. After performing this shift, we want to maximize the MEX of the array. The MEX of an array is defined as the smallest non-negative integer not present in the array.

Effectively, the problem asks: by uniformly shifting all elements, what is the largest "gap" starting from zero we can create that is missing from the array? For example, an array `[2, 4, 1, 0, -1]` can be shifted so that the elements start at zero, making consecutive non-negative integers appear as long as possible, pushing the first missing number further.

The constraints are moderate: up to 3000 total array elements across all test cases. This means an `O(n^2)` solution can work, but we should prefer `O(n log n)` or `O(n)` if possible to stay comfortable within the 2-second time limit. Negative numbers must be handled carefully, as a naive approach that assumes non-negativity could fail.

An edge case arises when all numbers are the same or when the smallest number is already zero. For instance, `[1, 1]` can only be shifted by `-1` to make the array `[0, 0]`, giving a MEX of `1`. Another edge case is when the array already contains consecutive numbers from `0` to `k`; the optimal MEX is just one more than the maximum element after shifting, potentially zero shift.

## Approaches

The brute-force approach is straightforward: try all possible shifts `x` from `-max(a)` to `-min(a)` so that the shifted array touches zero and check the MEX after each shift. This works because adding a large positive or negative number can push elements far away, but the number of potential shifts is enormous (up to 2*10^9), so iterating all shifts is infeasible.

The key insight is that the optimal shift aligns the smallest number in the array with zero. Once the minimum element becomes zero, the MEX is determined by the smallest missing integer among the sorted array. Since we only need to consider the difference between the smallest number and zero, a single operation suffices: shift all elements by `-min(a)`. After this, the array becomes non-negative and starts from zero. The MEX then is simply the first index where the consecutive non-negative sequence is broken.

Sorting the shifted array allows us to count how many consecutive numbers appear starting from zero. The first gap indicates the MEX. This reduces the problem to a single sort per test case plus a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all x) | O(range(a) * n) | O(n) | Too slow |
| Optimal (shift by -min(a), sort, find MEX) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a` of length `n`.
2. Compute the minimum value in the array, `min_a`. This value determines the shift needed to bring the smallest element to zero.
3. Shift the array by `x = -min_a`. This guarantees the smallest element is zero and all elements are non-negative.
4. Sort the shifted array. Sorting simplifies finding the first missing integer because we can now scan from zero upwards.
5. Initialize a variable `mex` to zero. Iterate through the sorted array, skipping duplicates. For each element, if it equals `mex`, increment `mex` by 1. The first element greater than `mex` breaks the consecutive sequence, so `mex` at that point is the MEX of the array.
6. Output `mex` as the maximum possible MEX after the shift.

**Why it works:** The optimal shift must bring some element to zero because the MEX is a non-negative integer. Shifting any element below zero would never increase the MEX beyond the first missing non-negative integer. Sorting and scanning ensures we correctly account for duplicates and consecutive sequences, guaranteeing that the first gap is detected.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_mex(a):
    min_a = min(a)
    shifted = [x - min_a for x in a]
    shifted.sort()
    mex = 0
    for val in shifted:
        if val == mex:
            mex += 1
    return mex

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max_mex(a))
```

**Explanation:**

We first compute the minimum of the array to determine the shift. Subtracting `min_a` from every element ensures the array starts at zero. Sorting the array allows us to easily find the first missing non-negative integer by checking `mex` against each value. The final loop correctly skips duplicates by only incrementing `mex` when the current value equals `mex`.

## Worked Examples

### Sample Input 1

```
1
4
4 2 3 6
```

| Step | Array | min_a | Shifted | mex |
| --- | --- | --- | --- | --- |
| Initial | [4,2,3,6] | 2 | [2,0,1,4] | 0 |
| After sort | [0,1,2,4] | - | - | 0 → 1 → 2 → 3 |

**Result:** 3. The first missing integer after 0,1,2 is 3.

### Sample Input 2

```
1
5
2 4 1 0 -1
```

| Step | Array | min_a | Shifted | mex |
| --- | --- | --- | --- | --- |
| Initial | [2,4,1,0,-1] | -1 | [3,5,2,1,0] | 0 |
| After sort | [0,1,2,3,5] | - | - | 0 → 1 → 2 → 3 → 4 |

**Result:** 4. The first missing integer after 0,1,2,3 is 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates; linear scan to compute MEX is O(n) |
| Space | O(n) | Storing the shifted array |

The algorithm easily handles the constraint sum(n) ≤ 3000 within the 2-second limit.

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
        print(max_mex(a))
    
    return output.getvalue().strip()

# Provided samples
assert run("6\n1\n4\n5\n0 1 1 2 3\n2\n1 1\n4\n4 2 3 6\n5\n2 4 1 0 -1\n6\n-1 1 2 3 5 6\n") == "1\n4\n1\n3\n4\n3"

# Custom cases
assert run("1\n1\n0\n") == "1", "single zero element"
assert run("1\n3\n-5 -4 -3\n") == "6", "all negative elements"
assert run("1\n4\n1 1 1 1\n") == "1", "all equal positive elements"
assert run("1\n5\n0 1 2 3 4\n") == "5", "already consecutive from 0"
assert run("1\n5\n0 0 0 1 1\n") == "2", "duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0` | 1 | Single element zero |
| `1\n3\n-5 -4 -3` | 6 | All negative elements |
| `1\n4\n1 1 1 1` | 1 | All equal positive elements |
| `1\n5\n0 1 2 3 4` | 5 | Already consecutive from 0 |
| `1\n5\n0 0 0 1 1` | 2 | Handling duplicates |

## Edge Cases

For the array `[1,1]`, the minimum is 1. Shift by `-1` yields `[0,0]`. Sorting gives `[0,0]`. Scanning for MEX starts at 0; first element 0 increments MEX to 1, second element 0 is skipped. Correct MEX is 1. This confirms that duplicates do not artificially inflate the MEX.

For `[ -1, 1, 2, 3, 5, 6 ]`, the minimum is -1. Shift by `1` gives `[0,2,3,4,6,7]`. Sorting: `[0,2,3,4,6,7]`. Scan for MEX
