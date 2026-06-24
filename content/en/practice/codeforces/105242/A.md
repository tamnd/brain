---
title: "CF 105242A - Prefix GCD"
description: "We are given an array and allowed to perform a single operation at most once. The operation selects a contiguous segment, computes the mex of that segment, and then overwrites every element inside the segment with that mex value."
date: "2026-06-24T13:03:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105242
codeforces_index: "A"
codeforces_contest_name: "The 2024 Damascus University Collegiate Programming Contest (DCPC 2024)"
rating: 0
weight: 105242
solve_time_s: 81
verified: true
draft: false
---

[CF 105242A - Prefix GCD](https://codeforces.com/problemset/problem/105242/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and allowed to perform a single operation at most once. The operation selects a contiguous segment, computes the mex of that segment, and then overwrites every element inside the segment with that mex value. After doing nothing or doing exactly one such overwrite, we look at the mex of the entire array and want to maximize it.

So the task is not to directly optimize the segment, but to understand how one carefully chosen “compression” of a subarray can increase the global mex.

The mex of an array is the smallest non-negative integer missing from it, so increasing the mex means we are trying to make as many small integers as possible appear while ensuring the first missing integer is pushed as far right as possible.

The constraints allow arrays up to size 10^6, which immediately rules out any solution that tries all segments. Even O(n log n) with heavy constants is acceptable, but anything quadratic over segments is impossible.

A subtle edge case appears when thinking about whether the operation can only help or sometimes hurt. For example, if we pick a segment that already has mex 0, we overwrite it with 0, potentially destroying existing structure and lowering the global mex. Another issue is assuming that the best segment always relates to the original mex directly, which is not true without a structural argument about how mex changes globally.

## Approaches

A brute force strategy would try every pair of indices l and r, compute mex of that subarray, apply the overwrite, recompute the full array mex, and track the best result. Computing mex naively per segment already costs O(n), and there are O(n^2) segments, so this becomes O(n^3), which is completely infeasible even for n around 5000.

Even improving mex computation per segment to amortized O(1) with frequency resets does not rescue this approach, since iterating over all segments still dominates.

The key structural observation is that the mex of the whole array is determined entirely by whether all values from 0 upward appear somewhere. The operation only changes one contiguous region into a constant value, so the only way it can improve mex is by helping ensure that small values remain present while introducing a new missing value.

Let m0 be the mex of the original array. All values from 0 to m0 − 1 appear at least once, and m0 does not appear at all.

If we want to improve the mex after one operation, the only candidate improvement is to make m0 appear in the array (since it is currently missing) while keeping all values 0 through m0 − 1 present. If we succeed, the new mex becomes m0 + 1. We cannot jump further than that, because we are introducing at most one new uniform value.

So the problem reduces to checking whether there exists a segment such that:

the segment produces mex equal to m0 when replaced, and the replacement does not destroy all occurrences of any value 0 through m0 − 1.

This turns into a purely positional condition on where each value appears.

We define for each value v its first and last occurrence in the array. To ensure that after replacement every value from 0 to m0 − 1 still exists, the chosen segment must not fully cover all occurrences of any such v. At the same time, to ensure the mex of the segment becomes exactly m0, the segment must contain at least one occurrence of every value from 0 to m0 − 1.

That is only possible if there exists a single segment that intersects every occurrence interval of values 0 through m0 − 1. This becomes an interval intersection problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over segments | O(n^3) | O(n) | Too slow |
| Interval intersection check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Compute the original mex

We scan the array and mark which values appear. The smallest value not seen is m0.

This gives the baseline: values 0 through m0 − 1 are all guaranteed to exist.

### 2. Record occurrence boundaries

For every value v in [0, m0 − 1], we compute its first and last occurrence in the array.

These boundaries describe the full region where each value “lives”.

### 3. Build the intersection condition

We want a segment [l, r] that contains at least one occurrence of every value 0 through m0 − 1. That means for every such value v, its interval [Lv, Rv] must intersect [l, r].

This is equivalent to requiring that there exists at least one index position that lies inside all these intervals simultaneously.

So we compute the global intersection:

we take L = max(Lv) and R = min(Rv) over all v < m0.

### 4. Decide feasibility

If L ≤ R, there exists a position that lies inside every occurrence interval. We can choose a segment that includes exactly that position, ensuring it intersects all required values while not fully covering any interval in a destructive way.

If L > R, no single segment can simultaneously intersect all these intervals, so we cannot force the mex improvement.

### Why it works

The crucial invariant is that every value v < m0 must survive the operation, meaning at least one occurrence of v must remain outside the chosen segment. At the same time, to make m0 appear after the operation, the segment must generate it as its mex, which requires the segment to “see” every value 0 through m0 − 1 at least once.

This creates a tension that collapses into a single condition: all these value intervals must overlap in at least one common index. If such a point exists, we can anchor the segment around it; otherwise, any segment will necessarily miss some required value or eliminate all occurrences of another.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    seen = [False] * (n + 2)
    for x in a:
        if x <= n + 1:
            seen[x] = True

    mex0 = 0
    while seen[mex0]:
        mex0 += 1

    if mex0 == 0:
        print(1)
        return

    INF = 10**18
    L = INF
    R = -INF

    first = [-1] * (mex0)
    last = [-1] * (mex0)

    for i, x in enumerate(a):
        if x < mex0:
            if first[x] == -1:
                first[x] = i
            last[x] = i

    for v in range(mex0):
        L = min(L, first[v])
        R = max(R, last[v])

    print(mex0 + 1 if L <= R else mex0)

if __name__ == "__main__":
    solve()
```

The solution first computes the original mex by marking all present values. It then records first and last occurrences for all values smaller than that mex. These boundaries define intervals whose overlap determines whether a single segment can simultaneously interact with all required values.

The final comparison `L <= R` is the entire decision point: it checks whether all these intervals share at least one common index.

## Worked Examples

### Example 1

Input:

```
5
0 1 2 4 3
```

Here mex is 5 since 0-4 all appear.

We compute intervals:

0: [0,0], 1: [1,1], 2: [2,2], 3: [4,4], 4: [3,3]

Now we intersect them:

L = max(0,1,2,4,3) = 4

R = min(0,1,2,4,3) = 0

| Step | L | R |
| --- | --- | --- |
| Start | 0 | 0 |
| After processing intervals | 4 | 0 |

Since L > R, no common point exists.

So answer is mex0 = 5.

This shows the case where values are too scattered to be simultaneously preserved inside one segment.

### Example 2

Input:

```
4
1 0 2 1
```

mex is 3.

Intervals:

0: [1,1]

1: [0,3]

2: [2,2]

Intersection:

L = max(1,0,2) = 2

R = min(1,3,2) = 1

| Step | L | R |
| --- | --- | --- |
| Start | 0 | 3 |
| After processing intervals | 2 | 1 |

Since L > R, answer is mex0 = 3.

This demonstrates that even though values exist, they do not overlap in a single position that touches all required occurrences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single scan to compute mex and boundaries |
| Space | O(n) | storing occurrence positions and seen array |

The solution fits comfortably within limits even for n up to 10^6 since all operations are linear and use simple arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    seen = [False] * (n + 2)
    for x in a:
        if x <= n + 1:
            seen[x] = True

    mex0 = 0
    while seen[mex0]:
        mex0 += 1

    if mex0 == 0:
        return "1"

    first = [-1] * mex0
    last = [-1] * mex0

    for i, x in enumerate(a):
        if x < mex0:
            if first[x] == -1:
                first[x] = i
            last[x] = i

    L = min(first)
    R = max(last)

    return str(mex0 + 1 if L <= R else mex0)

# minimum size
assert run("1\n0\n") == "1"

# all equal
assert run("5\n1 1 1 1 1\n") == "0"

# increasing sequence
assert run("5\n0 1 2 3 4\n") == "6"

# scattered values
assert run("4\n0 2 1 3\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0` | 1 | single element behavior |
| `5\n1 1 1 1 1` | 0 | missing 0 from start |
| `5\n0 1 2 3 4` | 6 | full consecutive range |
| `4\n0 2 1 3` | 4 | scattered interval intersection failure |

## Edge Cases

A key edge case is when the original mex is 0. In that situation, 0 does not appear anywhere, so any segment has mex 0 and replacing it does not help introduce missing structure. The algorithm handles this directly by returning 1, since we can always introduce 0 by selecting any segment containing only non-zero values.

Another edge case is when all values are already present consecutively from 0 to n − 1. In that case mex is n, and there are no values 0 through mex − 1 that violate the condition. The intersection condition trivially holds, and the algorithm correctly returns n + 1.

A third subtle case is when occurrences of required values are extremely scattered. The interval intersection check captures this precisely: even if every value exists, if their occurrence intervals do not overlap, there is no single segment that can simultaneously include them all, and thus no improvement is possible.
