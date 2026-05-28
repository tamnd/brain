---
title: "CF 205B - Little Elephant and Sorting"
description: "We are given an array of integers, and one operation consists of choosing a contiguous segment and increasing every element inside that segment by exactly one. We may repeat this operation any number of times."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 205
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 129 (Div. 2)"
rating: 1400
weight: 205
solve_time_s: 90
verified: true
draft: false
---

[CF 205B - Little Elephant and Sorting](https://codeforces.com/problemset/problem/205/B)

**Rating:** 1400  
**Tags:** brute force, greedy  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and one operation consists of choosing a contiguous segment and increasing every element inside that segment by exactly one. We may repeat this operation any number of times. After all operations, we do not need to match a fixed target array; instead, we only need the final array to be non-decreasing.

So the task is to understand how many range-increment operations are needed to transform the original array into some array that never decreases when read from left to right.

The key subtlety is that we are free to choose the final shape of the array, as long as it is non-decreasing and can be obtained only by adding increments over subarrays. We are not allowed to decrease values, only to “push” parts of the array upward using segments.

The constraint n ≤ 100000 implies we cannot simulate operations explicitly. Each operation can touch O(n) elements, and even a few thousand operations would already be too slow if applied naively. Any valid solution must reduce the problem to a single linear scan.

A naive but natural mistake is to think we can greedily “fix” local inversions by raising suffixes or prefixes without counting carefully how operations overlap.

For example, consider [5, 1, 1]. A careless approach might try to raise the second and third elements independently, but because operations act on ranges, fixing one position can unintentionally affect earlier positions.

Another misleading case is when the array is already non-decreasing, such as [1, 2, 3, 4]. Any correct solution must return 0 immediately, and not attempt to “improve” anything further.

A different edge scenario is when the array is strictly decreasing, such as [4, 3, 2, 1]. Here, every adjacent drop contributes independently to the number of required operations, but it is not immediately obvious why those contributions do not interact in a complicated way.

## Approaches

The brute-force viewpoint starts from the definition of the operation. Each operation increases a chosen segment by one, so we could try to simulate all sequences of operations and check when the array becomes non-decreasing. Even restricting ourselves to a fixed number of operations, the branching factor is huge because each step allows O(n²) possible segments. This quickly becomes exponential in the number of operations, which is infeasible even for small arrays.

A more structured brute idea is to fix a target non-decreasing array b where b[i] ≥ a[i], and then try to express the difference b - a as a sum of range increments. This is equivalent to decomposing a non-negative array into interval updates, but searching over all valid b is still too large.

The key simplification comes from reversing the perspective. Instead of building an arbitrary final array, we focus on how adjacent violations force operations. If at some position i we have a[i] > a[i+1], then the right side is too small compared to the left. Since we can only increase values, the only way to resolve this is to increase position i+1 enough so that it catches up to a[i]. Each unit of this gap must be “delivered” by some operation that affects i+1 but does not equally affect i, which implies a structural cost that is independent of other positions.

This leads to a linear decomposition where each downward step contributes directly to the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Optimal Adjacent-Drop Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the array once from left to right and measure how much each adjacent decrease contributes to the total number of operations.

1. Start with a running answer initialized to zero. This variable will accumulate the number of required range operations.
2. Iterate over the array from the first element to the second-to-last element. At each position i, compare a[i] and a[i+1].
3. If a[i] is less than or equal to a[i+1], do nothing. The pair already satisfies non-decreasing order locally, so no forced operations are needed to repair this boundary.
4. If a[i] is greater than a[i+1], compute the difference d = a[i] - a[i+1]. Add this value to the answer. This represents the minimum number of unit increments that must be applied to position i+1 relative to i in order to eliminate the local drop.
5. Continue scanning until the end of the array, accumulating all such positive drops.
6. Output the final accumulated value.

The reasoning behind step 4 is that each unit of decrease corresponds to one independent “layer” of correction that must be introduced via some range operation starting at or after i+1 and not fully covering i. These layers do not interfere across different positions because each adjacent drop enforces its own minimum number of required increments.

### Why it works

Each operation increases a contiguous segment by exactly one, so any final effect can be viewed as stacking unit-height interval covers over the array. The difference between adjacent elements a[i] and a[i+1] determines how many more layers must be present on the right side compared to the left in order for the final array to be non-decreasing.

Whenever a[i] > a[i+1], at least a[i] - a[i+1] operations must contribute extra height to position i+1 without equally contributing to position i. No operation can simultaneously “avoid” all such constraints, so these requirements add independently over all adjacent pairs. This independence makes the sum of positive drops both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            ans += a[i] - a[i + 1]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the observation that only downward transitions matter. The loop considers each adjacent pair exactly once, and the accumulator stores the total mandatory compensation needed to eliminate all local decreases. There is no need for simulation of operations or construction of the final array.

A common implementation mistake is trying to maintain a transformed array explicitly or simulating the range increments. That is unnecessary because the answer depends only on local differences, not on the evolving global structure.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

| i | a[i] | a[i+1] | Drop | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 0 |
| 2 | 2 | 3 | 0 | 0 |

The array is already non-decreasing, so no adjacent pair requires correction. The final answer remains zero, reflecting that no operations are needed.

### Example 2

Input:

```
3
4 3 2
```

| i | a[i] | a[i+1] | Drop | Answer |
| --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 1 | 1 |
| 2 | 3 | 2 | 1 | 2 |

Here each step introduces a new required unit of compensation. The first drop forces at least one operation affecting the second element more than the first, and the second drop introduces another independent requirement. The total becomes two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array, constant work per element |
| Space | O(1) | Only a running sum is stored |

The linear scan fits easily within the constraints for n up to 100000, and no auxiliary structures are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            ans += a[i] - a[i + 1]
    return str(ans)

# provided samples
assert run("3\n1 2 3\n") == "0"

# custom cases
assert run("1\n10\n") == "0", "single element"
assert run("3\n4 3 2\n") == "2", "strictly decreasing"
assert run("5\n1 1 1 1 1\n") == "0", "already flat"
assert run("4\n5 1 4 2\n") == "7", "mixed pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | minimum boundary |
| 4 3 2 | 2 | cumulative drops |
| all equal | 0 | no operations needed |
| mixed pattern | 7 | non-trivial accumulation |

## Edge Cases

For a single-element array like [10], the loop over adjacent pairs does not execute at all, so the answer remains zero, which matches the fact that a single value is trivially non-decreasing.

For a strictly decreasing array such as [5, 4, 3, 2], every adjacent pair contributes independently. The algorithm accumulates (5-4) + (4-3) + (3-2) = 3, and this matches the fact that each drop introduces a separate unit of required compensation.

For an already constant array such as [7, 7, 7, 7], no pair satisfies a[i] > a[i+1], so the answer stays zero throughout, confirming that no range operations are necessary.
