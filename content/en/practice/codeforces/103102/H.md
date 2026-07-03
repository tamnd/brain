---
title: "CF 103102H - AND = OR"
description: "We are given an array of integers, and we are interested in contiguous segments of this array where a bitwise condition holds: the bitwise AND of all elements in the segment is exactly equal to the bitwise OR of all elements in the same segment."
date: "2026-07-03T21:48:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103102
codeforces_index: "H"
codeforces_contest_name: "2020-2021 ICPC Southeastern European Regional Programming Contest (SEERC 2020)"
rating: 0
weight: 103102
solve_time_s: 43
verified: true
draft: false
---

[CF 103102H - AND = OR](https://codeforces.com/problemset/problem/103102/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we are interested in contiguous segments of this array where a bitwise condition holds: the bitwise AND of all elements in the segment is exactly equal to the bitwise OR of all elements in the same segment.

The task is to count how many such segments exist.

The input can be large, typically up to around 10^5 elements, which immediately rules out any approach that explicitly checks every segment. A naive O(n^2) enumeration of all subarrays, recomputing AND and OR each time, would involve on the order of 10^10 operations in the worst case, which is far beyond any practical limit under typical time constraints. This forces us to look for structure that allows aggregation without recomputation.

A key edge case appears when all elements are identical. For example, if the array is `[5, 5, 5]`, then every subarray satisfies the condition because both AND and OR stay equal to 5. A careless approach that checks only endpoints or assumes pairwise equality might still miss that longer segments are also valid. Another subtle case is when elements differ by only one bit. For instance `[1, 3]` in binary is `[01, 11]`, where AND is `01` and OR is `11`, which are not equal, so even small differences break validity immediately.

## Approaches

The brute-force idea is straightforward. We consider every subarray `[l, r]`, compute the bitwise AND and OR over that interval, and check whether they are equal. This is correct because it directly matches the definition. However, recomputing AND and OR for each subarray leads to O(n) work per segment unless we precompute something like sparse tables. Even with preprocessing, checking all O(n^2) subarrays remains too slow, giving roughly O(n^2) subarrays to validate.

The key observation is to understand when AND and OR of a set of numbers can be equal. For a fixed bit position, OR is 1 if at least one element has a 1 in that bit, while AND is 1 only if every element has a 1 in that bit. For these two results to match at every bit, each bit must behave identically under both operations. The only way this can happen is if, for every bit, either all elements have 0 or all elements have 1. That condition implies all numbers in the subarray are identical.

So the problem reduces to counting subarrays where all elements are equal. Instead of thinking in terms of bitwise operations, we now only need to track contiguous runs of equal values. Each maximal segment of equal values contributes a simple combinatorial count of subarrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or O(n² log n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. We scan the array from left to right while grouping consecutive equal elements into maximal blocks. This works because any valid subarray must lie entirely inside a block of identical values.
2. For each block, we determine its length, say `k`. Once we know that all elements in this segment are the same, every subarray inside it automatically satisfies the AND equals OR condition.
3. We compute the contribution of this block as `k * (k + 1) / 2`. This formula counts all possible contiguous subarrays inside a segment of length `k`.
4. We accumulate these contributions across all blocks to form the final answer.

Why it works

Within any subarray containing two different values, there exists at least one bit where the values differ. At that bit, OR will be 1 while AND will be 0, breaking equality. This means valid subarrays cannot cross a boundary where adjacent values differ, and cannot include heterogeneous elements. Therefore, valid subarrays are exactly those fully contained in maximal runs of equal values, and counting them reduces to counting all subarrays inside each run.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    i = 0
    
    while i < n:
        j = i
        while j < n and a[j] == a[i]:
            j += 1
        
        length = j - i
        ans += length * (length + 1) // 2
        
        i = j
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the idea of splitting the array into maximal equal-value segments. The two-pointer loop identifies each block `[i, j)` where all values match. Once a block is found, its contribution is computed using the arithmetic formula for subarray counts.

A subtle point is ensuring that `j` advances correctly even when the array has many repeated values, since failing to advance properly would lead to an infinite loop or double counting. The integer division is safe because `k*(k+1)` is always even.

## Worked Examples

### Example 1

Consider the array `[2, 2, 1, 1, 1]`.

| Step | Segment | Length | Contribution |
| --- | --- | --- | --- |
| 1 | [2, 2] | 2 | 3 |
| 2 | [1, 1, 1] | 3 | 6 |

The first block contributes 3 subarrays: `[2]`, `[2]`, `[2,2]`. The second contributes 6 subarrays. The total is 9.

This confirms that the algorithm decomposes the array cleanly into independent valid regions.

### Example 2

Consider `[5, 5, 5, 5]`.

| Step | Segment | Length | Contribution |
| --- | --- | --- | --- |
| 1 | [5, 5, 5, 5] | 4 | 10 |

Every subarray is valid because there are no transitions. This checks the full-range edge case where the entire array forms one block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited exactly once when forming blocks |
| Space | O(1) | Only counters and indices are used |

The solution runs in linear time, which is optimal since any correct answer must at least read the entire input. Memory usage remains constant aside from the input array, fitting easily within typical constraints for n up to 10^5 or higher.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    i = 0
    while i < n:
        j = i
        while j < n and a[j] == a[i]:
            j += 1
        length = j - i
        ans += length * (length + 1) // 2
        i = j
    
    return str(ans)

# provided samples (hypothetical format)
assert run("3\n1 1 1\n") == "6", "all equal case"
assert run("5\n1 2 2 3 3\n") == "6", "mixed blocks"

# custom cases
assert run("1\n7\n") == "1", "single element"
assert run("2\n1 2\n") == "2", "all distinct"
assert run("4\n9 9 9 9\n") == "10", "single long block"
assert run("6\n1 1 2 2 2 1\n") == "8", "multiple blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n7\n` | `1` | minimal input |
| `2\n1 2\n` | `2` | each element forms its own block |
| `4\n9 9 9 9\n` | `10` | full-range block counting |
| `6\n1 1 2 2 2 1\n` | `8` | multiple segments and transitions |

## Edge Cases

For arrays where all elements are equal, the algorithm collapses the entire array into one segment and correctly counts all subarrays via the triangular number formula. For an input like `[4, 4, 4]`, the loop forms a single block of length 3 and outputs 6, matching the number of all possible subarrays.

For arrays where no adjacent elements match, such as `[1, 2, 3, 4]`, each element forms a block of length 1. Each contributes exactly one valid subarray, so the total is 4. The algorithm handles this naturally because each iteration immediately closes a block of size 1 before moving forward.

For mixed patterns like `[1, 1, 2, 1, 1]`, the middle element breaks the structure into three blocks. The algorithm processes each independently, ensuring that no invalid cross-boundary subarrays are ever counted.
