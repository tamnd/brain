---
title: "CF 2160A - MEX Partition"
description: "We are given a multiset of integers, and we are allowed to split it into several smaller multisets such that every original element is used exactly the same number of times overall. In other words, we are partitioning occurrences of numbers into groups."
date: "2026-06-08T00:05:02+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2160
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1058 (Div. 2)"
rating: 800
weight: 2160
solve_time_s: 177
verified: true
draft: false
---

[CF 2160A - MEX Partition](https://codeforces.com/problemset/problem/2160/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of integers, and we are allowed to split it into several smaller multisets such that every original element is used exactly the same number of times overall. In other words, we are partitioning occurrences of numbers into groups.

For each group, we can compute its MEX, the smallest non-negative integer missing from that group. A partition is called valid when every group has exactly the same MEX value. That shared value becomes the score of the partition. The task is to choose a partition that makes this score as small as possible.

What makes this problem subtle is that we are not choosing one set and computing its MEX directly. We are distributing copies of numbers into multiple groups, and forcing all groups to “fail” at the same first missing number.

The constraints are small: each test has at most 100 elements, and values are also bounded by 100. This immediately rules out anything exponential over distributions or partitions. Even quadratic reasoning over value frequencies is safe, but anything enumerating partitions explicitly is unnecessary and would be overkill.

A naive mistake is to assume we should just compute the MEX of the whole array or something close to it. That fails because splitting can reduce or increase the achievable score. Another mistake is thinking the best strategy is always to maximize group sizes, but MEX depends on the presence of every number from 0 upward, not total sum or size.

A concrete edge case is when only a single number exists. For example, `[0, 0, 0]`. If we put everything in one group, MEX is 1. But if we split into three groups `{0},{0},{0}`, each group still has MEX 1, so score is 1. A careless solution might think splitting changes the MEX unpredictably, but here it preserves structure.

Another edge case is when 0 is missing entirely. For example `[1,2]`. Any group immediately has MEX 0, so the answer is forced to 0 regardless of partitioning. This is easy to miss if one assumes MEX depends on higher values.

## Approaches

The brute-force approach would try all ways of distributing occurrences into multiple groups and compute whether all groups share the same MEX. This involves partitioning `n` elements into arbitrary subsets, which grows faster than exponentially. Even for `n = 100`, this is completely infeasible.

The key observation is that the score is determined entirely by how many complete copies of the set `{0, 1, 2, ..., x-1}` we can form across groups. If we want a group to have MEX `x`, then every number from `0` to `x-1` must appear in that group at least once, while `x` must be missing.

To achieve a valid partition where all groups have the same MEX `x`, each group consumes at least one occurrence of every number `0..x-1`. Therefore, if we denote `freq[i]` as the frequency of value `i`, the number of such groups we can form is limited by the smallest frequency among `0..x-1`.

Let that minimum be `k`. We can form at most `k` groups each containing one copy of each number `0..x-1`. All remaining elements (including extra copies) can be placed anywhere without affecting MEX as long as we ensure `x` does not appear in any group.

For a valid construction, we need at least `k` groups, and we also need to ensure that `x` does not accidentally appear in all groups. The crucial constraint becomes that we must ensure that for some `x`, the structure is feasible and yields the smallest possible such value.

This reduces to checking, for each candidate MEX `x`, whether all numbers `0..x-1` exist at least once. If any is missing, we cannot form even one valid group with MEX ≥ x. Thus, the smallest `x` where this fails or becomes constrained determines the answer.

Instead of constructing partitions, we directly reason about when it becomes impossible to maintain a higher MEX across all groups. The answer ends up being the first index where frequency drops too low to support repeated coverage across groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over partitions | Exponential | Exponential | Too slow |
| Frequency-based scan | O(max A) | O(max A) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value in the array.

This gives us immediate access to how many copies of each number we can distribute across groups.
2. Start checking candidate MEX values from 0 upward.

We are effectively asking: can we force all groups to have MEX at least `x`?
3. For a fixed `x`, verify whether every number from `0` to `x-1` appears at least once.

If any is missing, no group can contain all required elements, so MEX cannot reach `x`.
4. Track the largest `x` such that all numbers `0..x-1` exist.

This is the point where the consecutive prefix of integers breaks.
5. The answer is exactly this largest achievable prefix length.

Beyond this point, MEX cannot be increased consistently across all groups.

### Why it works

Each group having the same MEX forces a shared structural requirement: every group must contain all numbers below that MEX. This reduces the problem to checking how far the set of numbers is “prefix-complete” starting from 0. The partitioning freedom does not change this requirement, since missing a number globally means it is impossible to satisfy the condition in any group. Thus the answer depends only on the longest consecutive prefix starting from 0 that exists in the multiset.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = [0] * 105
        for x in a:
            freq[x] += 1
        
        mex = 0
        while freq[mex] > 0:
            mex += 1
        
        print(mex)

if __name__ == "__main__":
    solve()
```

The frequency array is used only to detect the first missing integer starting from 0. The loop increments `mex` until it finds a value with zero frequency, which is exactly the definition of MEX for the multiset.

The important implementation detail is that we do not attempt to simulate partitions at all. The solution relies entirely on the observation that partitioning does not change whether a value exists in the multiset, and therefore does not affect the prefix condition that determines feasibility.

## Worked Examples

### Example 1

Input:

```
3
0 0 0
```

| mex | freq[0] | decision |
| --- | --- | --- |
| 0 | 3 | continue |
| 1 | 0 | stop |

The loop stops at 1 because 1 is missing entirely. This shows that even though we can split into many groups, every group would contain only zeros, so MEX is forced to be 1.

### Example 2

Input:

```
1 2
```

| mex | freq[mex] | decision |
| --- | --- | --- |
| 0 | 0 | stop |

Since 0 is missing, no group can ever contain 0, so every group immediately has MEX 0. The algorithm correctly returns 0.

These examples highlight that the answer depends only on the presence of the smallest missing integer, not on how elements are arranged into groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | We scan the array once to build frequencies and then scan a bounded range up to 100 |
| Space | O(1) | Frequency array size is fixed (≤ 101) |

The constraints are small enough that even a simple linear scan per test case is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        freq = [0]*105
        for x in a:
            freq[x] += 1
        mex = 0
        while freq[mex] > 0:
            mex += 1
        out.append(str(mex))
    return "\n".join(out)

# provided samples
assert run("""2
3
0 0 0
2
1 2
""") == """1
0"""

# custom cases
assert run("""1
1
0
""") == "1", "single zero"

assert run("""1
1
5
""") == "0", "missing zero"

assert run("""1
5
0 1 2 3 4
""") == "5", "full prefix"

assert run("""1
6
0 0 1 1 2 2
""") == "3", "balanced duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 1 | minimal valid MEX when 0 exists |
| single 5 | 0 | missing 0 forces MEX 0 |
| 0..4 present | 5 | full consecutive prefix |
| paired duplicates | 3 | duplicates do not affect MEX |

## Edge Cases

For an input like `[0]`, the frequency check sees `freq[0] > 0` and moves to `1`, where `freq[1] = 0`. The algorithm outputs `1`, matching the fact that any partition (only one group possible) has MEX 1.

For an input like `[2,3,4]`, the loop immediately fails at `mex = 0`, since `0` is absent. This produces output `0`, and any partition must also have MEX 0 because no group can contain 0.

For `[0,1,1,2,2]`, the loop proceeds through `0,1,2` but stops at `3`. This confirms that duplicates do not matter, only whether each integer appears at least once.
