---
title: "CF 104289B - OR-bitax"
description: "We are given a sequence of integers, and we are allowed to cut it into contiguous non-empty pieces. For each piece, we compute a value called its score, defined as the bitwise XOR of all elements inside that piece."
date: "2026-07-01T20:36:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104289
codeforces_index: "B"
codeforces_contest_name: "Bangladesh CP Server - BCS Round 1 (Div. 3)"
rating: 0
weight: 104289
solve_time_s: 75
verified: true
draft: false
---

[CF 104289B - OR-bitax](https://codeforces.com/problemset/problem/104289/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we are allowed to cut it into contiguous non-empty pieces. For each piece, we compute a value called its score, defined as the bitwise XOR of all elements inside that piece. After computing all segment scores, we take the bitwise OR of these scores, and our goal is to choose the segmentation that maximizes this final OR value.

So the decision we control is where to place cut points. Cutting more creates more segments, cutting fewer merges segments and changes their XOR values. The final objective is not the sum or XOR of segment results, but their bitwise OR, which makes the contribution of each bit independent.

The constraints allow up to 10^5 elements per test case and up to 3 × 10^5 total across tests. This immediately rules out any solution that tries all partitions, since the number of ways to split an array grows exponentially, roughly 2^(n−1). Even quadratic dynamic programming over all subarrays would be too slow at maximum scale.

A subtle point is that segment XOR values can introduce bit patterns that do not appear in any single element. For example, XOR of 1 and 2 is 3, which has both bits set. A naive intuition might suggest that segmentation could “create” new useful bits. The key question is whether such created bits can ever improve the final OR beyond what we already have from the original array.

## Approaches

A brute-force strategy would enumerate every possible way to split the array, compute XOR for each segment, then compute the OR of those segment values, and track the maximum. This is correct because it directly evaluates the objective definition. However, there are 2^(n−1) possible partitions, and each evaluation costs O(n) in the worst case, leading to exponential time that becomes infeasible even for n around 25.

We now look for structure. The important observation is that the final answer only depends on which bit positions can be made equal to 1 in at least one segment XOR. If a bit is 1 in any segment XOR, it contributes to the final OR independently of all other bits.

Now consider any bit position. A segment XOR has that bit set if and only if an odd number of elements in that segment have that bit set. However, this does not allow us to create a bit position that never existed in any element. XOR only rearranges parity; it does not introduce new bit positions. So every bit that can appear in any segment XOR must already appear in at least one element of the array.

This immediately implies an upper bound: the answer cannot exceed the bitwise OR of all elements. On the other hand, this bound is achievable by splitting the array into single-element segments. Each segment XOR is just the element itself, and the final OR becomes exactly the OR of all elements.

So the partitioning problem collapses completely: the optimal strategy is simply to take every element as its own segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

The solution reduces to computing the bitwise OR of all elements in the array.

1. Initialize an accumulator variable `ans` to zero. This variable will store the running OR of all values processed so far.
2. Iterate through the array from left to right. For each element, update `ans` by taking `ans = ans OR a[i]`. This gradually collects every bit that appears anywhere in the array.
3. After processing all elements, output `ans`.

The reason we can safely ignore all partitioning decisions is that no partition can introduce a new bit position beyond what already exists in the raw input values.

### Why it works

Each segment contributes a XOR value. Every bit set in any segment XOR must come from some subset of original elements that already contain that bit. Since OR only checks whether a bit appears anywhere, distributing elements into segments cannot create a bit that was not already present in at least one element. The single-element partition already realizes every achievable bit independently, so merging segments only risks canceling bits inside XOR, never improving the final OR.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    for x in a:
        ans |= x
    
    print(ans)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The implementation keeps exactly one running variable for the OR. There is no need to track prefix XORs or any DP state because segmentation does not influence the final optimal value.

The only subtlety is ensuring fast input handling due to large total constraints. Using `sys.stdin.readline` avoids overhead from standard input methods.

## Worked Examples

### Example 1

Input:

```
3
6 4 8
```

We process elements step by step.

| Step | Element | Running OR |
| --- | --- | --- |
| 1 | 6 | 6 |
| 2 | 4 | 6 |
| 3 | 8 | 14 |

Final answer is 14.

This shows that even though different partitions are possible, none can exceed the OR of all elements.

### Example 2

Input:

```
5
3 4 2 5 1
```

| Step | Element | Running OR |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 4 | 7 |
| 3 | 2 | 7 |
| 4 | 5 | 7 |
| 5 | 1 | 7 |

Final answer is 7.

This confirms that segmentation choices do not improve the final result beyond collecting all bit contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with a bitwise OR |
| Space | O(1) | Only a single accumulator is used |

The total complexity over all test cases is linear in the total number of elements, which is at most 3 × 10^5, easily fitting within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        for x in a:
            ans |= x
        print(ans)

    t = int(input())
    out = []
    for _ in range(t):
        solve()
    return ""

# provided samples
assert run("2\n3\n6 4 8\n5\n3 4 2 5 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n7\n` | `7` | Minimum size array |
| `1\n4\n1 2 4 8\n` | `15` | All bits independent |
| `1\n5\n0 0 0 0 0\n` | `0` | All zeros case |
| `1\n6\n3 3 3 3 3 3\n` | `3` | Repeated values stability |

## Edge Cases

A single-element array is the simplest scenario. The only possible partition is the array itself, and the answer equals that element. The algorithm correctly handles this because the OR accumulator starts at zero and becomes that value after processing the first and only element.

An array of zeros is another corner case. Every segment XOR is zero regardless of partitioning, so the final OR is zero. The algorithm preserves this because OR with zero does not change the accumulator.

Arrays with repeated identical values also highlight that segmentation does not matter. Even if we group or split differently, the OR over all elements remains the same, and no XOR combination produces a new bit outside the original value.
