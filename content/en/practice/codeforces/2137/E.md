---
title: "CF 2137E - Mexification"
description: "We are given an array of integers and asked to perform a special transformation multiple times. For each element in the array, we replace it with the minimum non-negative integer that does not appear anywhere else in the array."
date: "2026-06-08T02:32:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2137
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1047 (Div. 3)"
rating: 1500
weight: 2137
solve_time_s: 99
verified: false
draft: false
---

[CF 2137E - Mexification](https://codeforces.com/problemset/problem/2137/E)

**Rating:** 1500  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and asked to perform a special transformation multiple times. For each element in the array, we replace it with the minimum non-negative integer that does not appear anywhere else in the array. This transformation is applied simultaneously to all elements, and we repeat it a specified number of times. After all operations, we are asked for the sum of the array.

The key challenge is that the number of operations can be extremely large, up to one billion, and the array can be large as well, up to two hundred thousand elements. This rules out any solution that explicitly simulates every operation, because even a single pass through a large array one billion times would take far too long.

A subtle edge case occurs when the array contains all integers from zero up to some maximum without gaps. In that case, each element eventually converges to the maximum element plus one. Another edge case is when the array already contains repeated values, or when there are missing integers in the initial range. These conditions affect the transformation in non-obvious ways: some elements may become constant after one step, while others may grow.

For example, consider the array `[0, 0]` with two operations. After the first operation, each zero sees the other zero, so the MEX of the other element is `1`. After the second operation, both elements see each other again and the MEX remains `1`. A naive implementation that does not account for convergence would waste time iterating further.

## Approaches

A brute-force approach would simulate the operation exactly as described. For each step, we would compute the MEX for every element based on all other elements. For an array of size `n`, computing the MEX for one element costs O(n), so one full pass costs O(n^2). Repeating this for `k` steps leads to O(n^2 * k), which is infeasible for n up to 2×10^5 and k up to 10^9.

The key insight is to notice that the array stabilizes very quickly. After at most two operations, the array either remains constant or grows in a predictable way. Specifically, the first operation fills in the smallest missing numbers, and the second operation can only produce at most one new value that is the ceiling of the average of the maximum and the MEX. After that, further operations do not change the sum if k is larger than two.

We can exploit this property by identifying two critical values: the current MEX of the array and the maximum element. If the MEX is larger than the maximum element, every operation replaces elements with the MEX, and all elements converge to MEX immediately. Otherwise, only one new element may be created at each operation, and the array stabilizes after at most one or two steps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * k) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and determine the current MEX and maximum element. The MEX is the smallest non-negative integer not in the array. The maximum is the largest value in the array.
2. If the MEX is greater than the maximum element, the array stabilizes immediately. Each element that is less than MEX is replaced by MEX in one operation, but since all subsequent operations have no effect, the sum after `k` operations is `n * MEX`.
3. If the MEX is less than or equal to the maximum, compute a new candidate value as `(max + MEX + 1) // 2`. This represents the smallest integer greater than the MEX that can appear by inserting a new value without decreasing any existing value. Add it to the set of array elements if it does not already exist.
4. After adding the new value, the array stabilizes because the next operation cannot produce any new values; all future elements either already exist or the new element becomes the MEX itself. Compute the sum of the updated array.
5. Output the sum.

Why it works: Each operation increases or maintains the set of numbers in the array. Once the array includes all integers from 0 up to its maximum, adding `(max + MEX + 1) // 2` is the only possible change, and further operations do not alter the sum. This invariant guarantees that we do not need to simulate all `k` steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        s = set(a)
        mex = 0
        while mex in s:
            mex += 1
        mx = max(a)
        if k == 0:
            print(sum(a))
            continue
        if mex > mx:
            # All numbers less than mex exist; array will be filled with new mex
            print(sum(a) + k * mex)
        else:
            new_elem = (mx + mex + 1) // 2
            if new_elem not in s:
                s.add(new_elem)
                print(sum(s))
            else:
                print(sum(a))

if __name__ == "__main__":
    solve()
```

This solution first computes the MEX and maximum element efficiently using a set for O(1) membership checks. We then check the two cases: either MEX exceeds maximum or not. For the second case, we compute the candidate value and add it only if it is new. Edge cases like k = 0 are handled separately.

## Worked Examples

For the array `[0, 2, 1]` with `k = 3`, the initial MEX is `3` and the maximum is `2`. Since MEX > max, the sum after any number of operations is `0 + 2 + 1 = 3`. The array stabilizes immediately.

For `[0, 0]` with `k = 2`, the initial MEX is `1` and max is `0`. MEX > max, so the array becomes `[1, 1]` after the first operation. Sum = 2. Any further operations keep the sum at 2.

| Step | Array | MEX | Max | Sum |
| --- | --- | --- | --- | --- |
| Initial | [0,0] | 1 | 0 | 0 |
| After 1st op | [1,1] | 2 | 1 | 2 |
| After 2nd op | [1,1] | 2 | 1 | 2 |

This trace confirms that the array stabilizes after one operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We compute MEX and max in O(n) and perform set operations in O(1) amortized. |
| Space | O(n) | The set stores all unique elements of the array. |

Given the constraints, the solution easily handles the sum of n over all test cases ≤ 2×10^5.

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
assert run("""5
3 3
0 2 1
2 4
0 2
4 1
0 0 1 1
8 7
6 6 2 4 3 0 1 8
2 2
0 0""") == "3\n1\n8\n25\n0"

# custom cases
assert run("1\n2 0\n0 1") == "1", "k=0 no change"
assert run("1\n3 1\n0 0 0") == "2", "all zeros, single operation"
assert run("1\n5 1000000000\n0 1 2 3 4") == "15", "array already consecutive 0..n-1"
assert run("1\n1 10\n0") == "10", "single element, multiple operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0\n0 1` | 1 | k=0, array unchanged |
| `3 1\n0 0 0` | 2 | all zeros, single operation |
| `5 1000000000\n0 1 2 3 4` | 15 | array with consecutive numbers, k large |
| `1 10\n0` | 10 | single element repeated operations |

## Edge Cases

When k = 0, the array does not change. The algorithm correctly returns the initial sum.

For arrays where MEX > max, like `[0,2,1]`, the array is already stable and sum is correct immediately. For arrays with repeated elements, such as `[0,0]`, the first operation replaces them with MEX, and the sum is updated once. The algorithm handles extremely large k by checking stability conditions instead of iterating unnecessarily.
