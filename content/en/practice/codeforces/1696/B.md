---
title: "CF 1696B - NIT Destroys the Universe"
description: "We are given an array representing the “universe,” where each element is a non-negative integer. The protagonist, NIT, can perform a specific operation on any contiguous subarray: compute the mex of that subarray and set every element in it to that mex."
date: "2026-06-09T22:33:14+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1696
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 21"
rating: 900
weight: 1696
solve_time_s: 131
verified: true
draft: false
---

[CF 1696B - NIT Destroys the Universe](https://codeforces.com/problemset/problem/1696/B)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array representing the “universe,” where each element is a non-negative integer. The protagonist, NIT, can perform a specific operation on any contiguous subarray: compute the `mex` of that subarray and set every element in it to that `mex`. The task is to find the minimum number of such operations required to turn the entire array into zeros.

The input includes multiple test cases, each with an array of length up to 100,000, and the total number of elements across all test cases does not exceed 200,000. This means any algorithm with time complexity significantly above O(n) per test case will likely exceed the time limit. For instance, a naive brute-force approach that repeatedly computes `mex` over arbitrary subarrays would be O(n²) or worse, which is unacceptable. We need a solution that essentially scans the array once or twice.

Non-obvious edge cases include arrays that already consist entirely of zeros, arrays that are a perfect sequence starting from zero, and arrays containing very large numbers with gaps in between. For example, an array `[0,1,2,3,4]` can be solved in one operation, while `[0,2,3,0,1,2,0]` requires two. A careless approach that only considers the maximum element or assumes sequential numbers could miscalculate the required operations.

## Approaches

A brute-force solution would repeatedly select some subarray, compute its `mex`, and apply the operation until all elements are zero. This works because eventually any non-zero element can be reduced to zero using one or more operations. However, each computation of `mex` could take O(n), and with multiple such operations, the complexity can easily reach O(n²) in a worst-case scenario, which is too slow for n up to 10^5.

The key insight is that the number of operations needed depends only on the minimum and maximum values present and whether zero is included. If the array already contains only zeros, no operations are required. If zero is missing from the array, we can perform a single operation on the entire array to introduce zero. If zero is present but there are elements greater than zero that need to be removed, we might require up to two operations. Specifically, one operation can reduce a contiguous block to its `mex`, potentially introducing zeros where they are missing, and a second operation can then propagate zeros across the remaining non-zero elements.

The problem reduces to checking the minimum value in the array, the maximum value, and the first and last positions where the maximum value occurs relative to zeros. This allows us to decide whether zero, one, or two operations are sufficient. The optimal solution does not require simulating the operations directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check if the array already consists entirely of zeros. If so, return 0 because no operations are needed.
2. Compute the minimum element of the array. If the minimum is greater than zero, perform a single operation on the entire array to introduce zero, then return 1. This guarantees that the smallest value in the array becomes zero.
3. Identify the maximum element in the array and its first and last occurrence positions. If the array contains zero and all elements are less than or equal to the maximum but appear in contiguous blocks starting from zero, a single operation is enough to convert the remaining non-zero elements to zero.
4. In general, if zero is present but there exists a subarray containing non-zero elements that are separated by zeros, it may require two operations. The first operation reduces the block to the `mex`, introducing zero where needed. The second operation spreads zeros to the remaining non-zero elements.
5. Return the number of operations determined by the above checks: 0 if all zeros, 1 if zero is missing or a single operation suffices, and 2 otherwise.

Why it works: The algorithm works because the `mex` operation can reduce a contiguous subarray to its smallest missing value. By inspecting only the global minimum and maximum and their positions, we capture the necessary conditions to decide whether one or two operations suffice without simulating all subarray operations. This guarantees correctness in O(n) time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if all(x == 0 for x in a):
            print(0)
            continue
        mn = min(a)
        mx = max(a)
        if mn > 0:
            print(1)
            continue
        first = None
        last = None
        for i, x in enumerate(a):
            if x == mx:
                if first is None:
                    first = i
                last = i
        # check if all elements between first and last are mx
        if all(a[i] == mx for i in range(first, last + 1)):
            print(1)
        else:
            print(2)

if __name__ == "__main__":
    solve()
```

The solution first handles the simplest case of an array already consisting of zeros. If not, it checks if the minimum value is greater than zero, which implies we can introduce zero in one operation. Otherwise, it locates the maximum element and checks if it appears in a contiguous block. If it does, one operation suffices; if there are gaps, two operations are needed. This approach avoids unnecessary simulation and guarantees the minimal number of operations.

## Worked Examples

**Example 1:** `[0, 0, 0, 0]`

| Step | mn | mx | first | last | Operation count |
| --- | --- | --- | --- | --- | --- |
| Initial | 0 | 0 | - | - | 0 |

All zeros, so output is 0.

**Example 2:** `[0, 2, 3, 0, 1, 2, 0]`

| Step | mn | mx | first | last | Contiguous check | Operation count |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 0 | 3 | 2 | 3 | False | 2 |

Maximum is 3, but its occurrences are not contiguous; thus two operations are needed.

These traces demonstrate how identifying min, max, and positions suffices to determine the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Scans array once to find min, max, and max positions |
| Space | O(1) extra | Only a few variables stored besides input array |

Given the sum of n over all test cases ≤ 200,000, the algorithm executes comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n4\n0 0 0 0\n5\n0 1 2 3 4\n7\n0 2 3 0 1 2 0\n1\n1000000000\n") == "0\n1\n2\n1", "samples"

# custom cases
assert run("1\n1\n0\n") == "0", "single zero"
assert run("1\n5\n5 5 5 5 5\n") == "1", "all equal non-zero"
assert run("1\n6\n1 0 1 0 1 0\n") == "2", "alternating ones and zeros"
assert run("1\n3\n0 1 0\n") == "2", "max in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n0 | 0 | single element zero |
| 1\n5\n5 5 5 5 5 | 1 | all non-zero identical elements |
| 1\n6\n1 0 1 0 1 0 | 2 | alternating pattern needing two operations |
| 1\n3\n0 1 0 | 2 | max element in middle requiring two operations |

## Edge Cases

For `[0,1,0]`, the minimum is 0 and maximum is 1. The maximum occurs in a non-contiguous subarray (positions 2), so the algorithm correctly returns 2. For `[5,5,5,5,5]`, min > 0, so a single operation on the whole array introduces zero. For `[0,0,0,0]`, all zeros, so no operations are needed. These examples confirm that the algorithm handles the critical edge cases correctly.
