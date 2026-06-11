---
title: "CF 1209A - Paint the Numbers"
description: "We are given a list of integers, and we want to partition them into as few groups as possible. Each group has a structural constraint: if you look at the smallest number inside that group, every other number assigned to the same group must be divisible by that smallest number."
date: "2026-06-11T23:18:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1209
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 584 - Dasha Code Championship - Elimination Round (rated, open for everyone, Div. 1 + Div. 2)"
rating: 800
weight: 1209
solve_time_s: 101
verified: true
draft: false
---

[CF 1209A - Paint the Numbers](https://codeforces.com/problemset/problem/1209/A)

**Rating:** 800  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers, and we want to partition them into as few groups as possible. Each group has a structural constraint: if you look at the smallest number inside that group, every other number assigned to the same group must be divisible by that smallest number.

You can think of each group as being “anchored” by its minimum element. Once you pick that minimum, everything else in the group must be a multiple of it. The task is to assign every number to some group while minimizing how many groups are created.

The constraint that values are at most 100 changes the nature of the problem significantly. Instead of needing a complex graph or DP over large states, we can reason directly about frequencies and divisibility structure among small integers. Any solution that tries to explicitly enumerate partitions or greedily assign elements without a global view risks missing optimal groupings, especially because the same value can appear multiple times and must be handled consistently.

A subtle failure case for naive reasoning appears when numbers share divisors but not directly in a chain. For example, in `[6, 10, 15]`, a greedy approach might try to combine 6 and 10 or 10 and 15 based on partial compatibility, but none of them can share a group unless all elements are multiples of the chosen minimum. Since no pair shares a valid common minimum that divides both, the correct answer is 3 groups.

Another subtle case is duplicates and divisor reuse. In `[2, 4, 8, 3, 9]`, it is tempting to think we might “reuse” a group for multiple unrelated chains, but each group’s minimum forces strict divisibility, so we must carefully decide which numbers act as anchors.

## Approaches

A brute-force approach would attempt to assign each element into one of several groups and check validity. For each assignment, we would verify that in every group, all numbers are divisible by the minimum element of that group. This leads to an exponential search space because each element has multiple group choices and we do not know the optimal number of groups in advance. Even with pruning, the number of partitions of n elements grows too quickly for n up to 100.

The key structural observation is that group membership is determined entirely by the chosen minimum. If a number x is the minimum of a group, then every element in that group must be a multiple of x. This means that for each possible value x, we can consider whether it should act as a group representative, and then assign all its multiples to that group if they have not already been assigned elsewhere.

Once we interpret the problem this way, the goal becomes selecting a set of “anchors” such that every number belongs to exactly one anchor’s group, and each anchor can only cover numbers divisible by itself. The optimal strategy is to process numbers from smallest to largest, and whenever we encounter a number that has not yet been assigned to any earlier group, it must start a new group. Then we mark all multiples of it as covered by that group.

This works because smaller numbers are always better anchors: they divide more numbers and therefore create more flexible groups. Larger numbers cannot serve as useful anchors for smaller ones, so delaying decisions would only risk losing optimal grouping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitioning | Exponential | O(n) | Too slow |
| Greedy divisor anchoring | O(n + maxA log maxA) | O(maxA) | Accepted |

## Algorithm Walkthrough

We use an array or frequency structure to track which values are still unassigned.

1. Initialize a boolean array `used` over the value range. This tracks whether a number has already been assigned to some group.
2. Iterate over possible values from 1 to the maximum value in the input. This ordering ensures we always consider potential group anchors from smallest to largest.
3. When we encounter a value `x` that appears in the input and is not yet marked as used, we decide that `x` starts a new group. This choice is forced because no earlier smaller divisor exists that could validly anchor `x`.
4. Once `x` is chosen as a group minimum, we mark every multiple of `x` as used. This represents assigning all numbers divisible by `x` into this group. The reason this is safe is that every multiple of `x` satisfies the divisibility constraint with respect to `x`.
5. Continue scanning upward, repeating the process whenever we find an unused number that appears in the array.

The final answer is the number of times we start a new group.

The correctness hinges on the invariant that whenever we start a group at value x, every number less than x is already fully processed and assigned, and x is the smallest unassigned value. This guarantees x cannot be placed into any earlier group, because any earlier group would have a smaller minimum that does not divide x. Therefore starting a new group at x is unavoidable, and greedily covering all multiples maximizes coverage without invalid assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    maxv = max(a)
    freq = [0] * (maxv + 1)
    
    for x in a:
        freq[x] += 1

    used = [False] * (maxv + 1)
    groups = 0

    for x in range(1, maxv + 1):
        if freq[x] > 0 and not used[x]:
            groups += 1
            for multiple in range(x, maxv + 1, x):
                used[multiple] = True

    print(groups)

if __name__ == "__main__":
    solve()
```

The solution first compresses the input into a frequency array so we can quickly test whether a value exists. The `used` array tracks whether a value has already been absorbed into some earlier group.

The loop over `x` ensures we always process potential group leaders in increasing order. When we select a new leader, we immediately mark all its multiples, which prevents them from forming redundant groups later.

A common mistake is iterating over the input array directly instead of the value range. That breaks the divisor structure because grouping depends on numeric relationships, not input order.

## Worked Examples

### Example 1

Input: `[10, 2, 3, 5, 4, 2]`

| x | freq[x] | used[x] | Action | Groups |
| --- | --- | --- | --- | --- |
| 1 | 0 | - | skip | 0 |
| 2 | 2 | False | start group at 2, mark 2,4 | 1 |
| 3 | 1 | False | start group at 3, mark 3 | 2 |
| 4 | 1 | True | already used | 2 |
| 5 | 1 | False | start group at 5, mark 5,10 | 3 |
| 6.. | 0 | - | skip | 3 |

Final answer is 3 groups.

This trace shows how early small divisors absorb larger multiples, preventing them from forming additional groups later.

### Example 2

Input: `[6, 2, 3, 4, 12]`

| x | freq[x] | used[x] | Action | Groups |
| --- | --- | --- | --- | --- |
| 1 | 0 | - | skip | 0 |
| 2 | 1 | False | start group at 2, mark 2,4 | 1 |
| 3 | 1 | False | start group at 3, mark 3,6,12 | 2 |
| 4 | 1 | True | skip | 2 |
| 5 | 0 | - | skip | 2 |
| 6 | 1 | True | skip | 2 |

Final answer is 2 groups.

This demonstrates that once a divisor group is formed, it can absorb far-reaching multiples, including values that are not immediate multiples in the input order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(maxA log maxA) | each number marks multiples up to 100 |
| Space | O(maxA) | frequency and bookkeeping arrays |

The bounds are small enough that iterating over multiples is extremely fast. Even in the worst case, the number of operations stays well below limits because max value is only 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return io.StringIO()

# corrected run wrapper
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("6\n10 2 3 5 4 2\n") == "3"

# all equal
assert run("4\n2 2 2 2\n") == "1"

# primes only
assert run("3\n7 11 13\n") == "3"

# single chain
assert run("5\n2 4 8 16 32\n") == "1"

# mixed divisibility
assert run("5\n3 6 2 4 9\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 1 | single anchor dominates |
| primes only | n | no merges possible |
| powers of two | 1 | full divisor chain |
| mixed values | 2 | interaction of groups |

## Edge Cases

A key edge case is when all numbers are pairwise coprime, such as `[7, 11, 13]`. The algorithm starts a new group at each value because none divides another, producing three groups, which is optimal since no grouping is possible.

Another case is a fully nested divisor chain like `[2, 4, 8, 16]`. The algorithm starts at 2, marks all multiples, and finishes with one group. This shows that early anchoring correctly collapses long chains into a single group.

A third case involves repeated values like `[3, 3, 6, 6, 12]`. The first 3 becomes the anchor, and all others are absorbed immediately, confirming that duplicates do not increase group count.
