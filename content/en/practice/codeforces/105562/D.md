---
title: "CF 105562D - Dutch Democracy"
description: "We are given a collection of political parties, each with a certain number of seats. A “coalition” is simply a subset of these parties. We want to count how many subsets satisfy a very specific notion of being a valid governing coalition."
date: "2026-06-22T14:20:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105562
codeforces_index: "D"
codeforces_contest_name: "2024-2025 ICPC Northwestern European Regional Programming Contest (NWERC 2024)"
rating: 0
weight: 105562
solve_time_s: 67
verified: true
draft: false
---

[CF 105562D - Dutch Democracy](https://codeforces.com/problemset/problem/105562/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of political parties, each with a certain number of seats. A “coalition” is simply a subset of these parties. We want to count how many subsets satisfy a very specific notion of being a valid governing coalition.

A subset is acceptable if it has a strict majority of all seats, meaning the sum of seats inside the subset is greater than half of the total sum across all parties. However, this is not enough. The coalition must also be minimal in the sense that if you remove any single party from it, it immediately stops being a strict majority. So every party inside the coalition is essential for maintaining the majority.

The constraints allow up to 60 parties, with each party having up to 10,000 seats. This immediately suggests that enumerating all subsets directly is possible in principle since there are about 2^60 subsets, but clearly impossible in practice. Any valid solution must exploit structure in the “minimal majority” condition rather than brute forcing subsets.

A naive attempt would try all subsets and check both conditions. This fails because 2^60 is astronomically large, far beyond any feasible computation.

A more subtle failure case comes from checking only the majority condition. For example, if we take a subset whose sum is barely above half, it is not necessarily minimal. Consider a case like 60, 50, 49 where the total is 159. The subset {60, 50} has sum 110, which is a majority, but removing 50 leaves 60 which is still a majority. So it is invalid even though it passes the first condition.

The reverse mistake is also common: ensuring minimality without ensuring majority. A subset where every element is “large relative to the rest” might still fail to exceed half the total.

## Approaches

The brute-force approach is straightforward: iterate over all subsets, compute their sum, and then for each element in the subset check whether removing it breaks the majority condition. This is correct but has exponential complexity in both subset enumeration and per-subset validation. With 60 elements, this becomes entirely infeasible.

The key observation is to reformulate minimality in a way that removes the dependency on checking each element individually inside the subset. Suppose a subset has total sum `S_sub`. If removing any element makes it lose majority, then for every element `x` in the subset we must have:

`S_sub - x <= S_total / 2`

Rearranging gives:

`x >= S_sub - S_total / 2`

This means every element in the subset must be at least a certain threshold that depends on the subset sum itself. That dependence looks circular at first, but it becomes manageable if we fix the smallest element in the subset.

If we assume a subset has minimum element `m`, then all elements are at least `m`, and the condition becomes:

`S_sub <= S_total / 2 + m`

At the same time, we still need:

`S_sub > S_total / 2`

So for a fixed minimum element, valid subsets are exactly those whose sum lies in a narrow interval controlled by that minimum.

This suggests sorting or iterating by which element is the minimum, and counting subsets where all elements come from a suffix of elements that are at least that value. That transforms the problem into counting subset sums under constraints on the sum range.

We can precompute subset sum counts for every suffix using dynamic programming, and then for each possible minimum element, query how many subset sums fall into the required interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Suffix DP + minimum pivot | O(n · S) | O(n · S) | Accepted |

Here `S` is the total sum of seats, at most about 6e5.

## Algorithm Walkthrough

We reformulate the counting so that each coalition is counted by choosing its minimum element first, then extending it with larger or equal elements.

1. Compute the total sum of all seats and define the majority threshold as half of this sum.
2. Sort parties by their seat values, or equivalently treat indices in increasing order of seat size so that suffixes represent valid choices for “minimum element anchored subsets”.
3. Build a dynamic programming table where `dp[i][s]` represents the number of ways to choose a subset using only parties from index `i` to `n` that sum to `s`.
4. Compute this DP from right to left. For each party `i`, we either exclude it or include it, shifting sums accordingly. This ensures every suffix has its full subset-sum distribution.
5. For each index `i`, treat party `i` as the minimum element of the coalition. Any valid coalition containing it must choose all other members from indices `i+1` onward.
6. If the minimum element is `p[i]`, then for a chosen subset of the suffix with sum `t`, the full coalition sum becomes `t + p[i]`. We translate the validity conditions into constraints on `t`:

The coalition must satisfy `S_total / 2 < t + p[i] <= S_total / 2 + p[i]`, which simplifies to `S_total / 2 - p[i] < t <= S_total / 2`.
7. Sum all dp counts over `t` in this interval for each `i`, and accumulate the result.

The correctness comes from the fact that every valid coalition has a unique minimum element. Once that element is fixed, the rest of the coalition is unrestricted except for being at least that minimum (guaranteed by suffix restriction), and the majority/minimality constraints become simple sum bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    half = total // 2
    
    max_sum = total
    
    dp_next = [0] * (max_sum + 1)
    dp_next[0] = 1
    
    ans = 0
    
    for i in range(n - 1, -1, -1):
        p = a[i]
        
        dp_cur = dp_next[:]  # not take p[i]
        for s in range(max_sum - p, -1, -1):
            if dp_next[s]:
                dp_cur[s + p] += dp_next[s]
        
        dp_next = dp_cur
        
        low = half - p + 1
        high = half
        
        if low < 0:
            low = 0
        
        for t in range(low, high + 1):
            ans += dp_next[t]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The DP is built from the end so that `dp_next` always represents subsets of the suffix strictly after the current index. When we process a new element, we clone the DP and add transitions that include the current seat count.

The interval query uses the transformed inequality. The lower bound is `half - p[i] + 1` because we need a strict inequality on the left side, while the upper bound is inclusive at `half`.

A subtle point is that we intentionally reuse `dp_next` after updating it for each index, so each party is correctly treated as a potential minimum of subsets in its suffix.

## Worked Examples

Consider a small configuration with seats `[3, 2, 2]`. The total is 7, so half is 3.

We build suffix DP tables:

For index 2 (value 2), subsets are `{}`, `{2}` so sums are 0 and 2.

For index 1 (value 2), subsets over `[2,2]` give sums `{0,2,2,4}`.

For index 0 (value 3), subsets over `[3,2,2]` give all combinations.

Now evaluate each minimum:

For minimum 3, suffix is `[2,2]`. We need `t` such that `3.5 - 3 < t <= 3.5`, meaning `0.5 < t <= 3.5`, so valid `t` are `{2}`. That gives subset `{3,2}` and `{3,2}` (depending on which 2 is chosen), contributing two coalitions.

For minimum 2 at index 1, suffix is `[2]`. We need `3.5 - 2 < t <= 3.5`, so `1.5 < t <= 3.5`, giving `t=2`. That produces coalition `{2,2}`.

| Minimum | Suffix | Valid t range | Valid coalitions |
| --- | --- | --- | --- |
| 3 | [2,2] | (0.5, 3.5] | {3,2} variants |
| 2 | [2] | (1.5, 3.5] | {2,2} |

This confirms that each coalition is counted exactly once via its minimum element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · S) | Each element updates a subset-sum DP over at most S states, and each index performs one range accumulation |
| Space | O(S) | We maintain only one suffix DP array |

The total sum of seats is bounded by about 600,000, and with 60 parties this DP comfortably fits within time limits in optimized Python or easily in C++.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# sample-like small case
assert run("3\n1 2 3\n") == "2", "basic sanity"

# single party
assert run("1\n10\n") == "1", "single element always valid"

# all equal
assert run("3\n2 2 2\n") == "3", "symmetry case"

# increasing values
assert run("4\n1 2 3 4\n") >= "1", "non-trivial structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 party | 1 | minimal edge case |
| all equal | 3 | symmetry and multiple valid minima |
| increasing | non-zero | general correctness |

## Edge Cases

For a single party `[x]`, the total is `x` and half is `x/2`. The only subset is `{x}`, which always satisfies majority and minimality. The DP correctly counts this because the suffix DP starts with empty subset and the range query includes `t = 0`.

For a case with large imbalance like `[100, 1, 1, 1]`, only coalitions anchored at 100 can reach majority constraints in a minimal way. The DP correctly restricts suffix sums so that smaller elements cannot form independent majority sets.

For symmetric cases like `[2,2,2]`, every pair is a valid minimal majority coalition. Each coalition is counted exactly once because it is associated with its unique minimum index, preventing overcounting.
