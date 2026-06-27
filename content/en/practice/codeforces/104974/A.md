---
title: "CF 104974A - Happy Valentine's Day"
description: "We are given a short sequence of integer adjustments applied one after another to a running total. Each value can either increase or decrease the sum depending on whether it is positive or non-positive, but in practice they are simply added as-is."
date: "2026-06-28T06:09:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104974
codeforces_index: "A"
codeforces_contest_name: "Codentines Day"
rating: 0
weight: 104974
solve_time_s: 72
verified: false
draft: false
---

[CF 104974A - Happy Valentine's Day](https://codeforces.com/problemset/problem/104974/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a short sequence of integer adjustments applied one after another to a running total. Each value can either increase or decrease the sum depending on whether it is positive or non-positive, but in practice they are simply added as-is.

The question is not about the final full sequence only. We are allowed to choose any subset of these values, preserve their original values, and decide whether there exists at least one subset whose sum is exactly 14. If such a selection exists, the output is affirmative, otherwise it is negative.

The structure is essentially asking whether 14 can be formed as a subset sum from a small list of integers that may include negatives, zeros, and positives.

The constraint on the number of elements is very small, with n at most 19. This bound is the key signal in the problem. A list of this size allows exponential exploration over all subsets, since the total number of subsets is 2^19, which is slightly over half a million. This is small enough to evaluate directly within time limits in Python without needing advanced optimization techniques like meet-in-the-middle or dynamic programming bitsets.

The value range of each element, from -10 to 19, does not require special handling beyond normal integer arithmetic. It does, however, mean that intermediate sums can be negative or exceed 14, so pruning strategies must be used carefully if applied.

A few edge situations deserve attention. If all numbers are positive and greater than 14, no subset can ever reach 14, and the correct answer is immediately negative. For example, input `[20, 30]` clearly cannot form 14. Conversely, if there is a single element equal to 14, the answer is immediately positive. Another subtle case is when zeros exist. Zeros do not change sums but still count as distinct subset choices, so a subset that reaches 14 remains valid regardless of whether extra zeros are included.

## Approaches

The most direct approach is to try every possible subset of the given numbers and compute its sum. Since each element has two choices, either it is included or not included, this leads to 2^n possibilities. For each subset we compute a sum in O(n) or maintain an incremental sum during bitmask enumeration. The total work is therefore on the order of n times 2^n in a naive implementation.

With n = 19, this upper bound is roughly 19 × 524,288, which is about ten million primitive operations. In Python this is still acceptable, especially since addition and bit operations are cheap. So even the brute force is already sufficient.

An alternative view is dynamic programming over achievable sums, but because values include negatives, a classic knapsack DP with fixed offsets becomes slightly more cumbersome. We would need to shift the range or use a set to track reachable sums. That also works, but it does not improve asymptotic complexity compared to simple subset enumeration in this constraint regime.

The key insight is that we do not need to optimize beyond enumerating subsets. The constraint on n is explicitly chosen to make exhaustive search the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(n · 2^n) | O(1) or O(n) | Accepted |
| DP / Set of Sums | O(n · S) where S is sum range | O(S) | Accepted but unnecessary |

## Algorithm Walkthrough

We treat each subset as a binary mask of length n. Each bit indicates whether a corresponding element is included in the subset.

1. Read the array of integers and store it in a list. This gives us direct indexed access for subset construction.
2. Iterate over all integers from 0 to 2^n − 1. Each integer represents a subset of the array. The binary representation encodes inclusion or exclusion of each element.
3. For each subset mask, compute the sum of all elements whose corresponding bit is set. This is done by scanning all positions from 0 to n − 1 and checking whether the bit is active. The reason for recomputing rather than maintaining incremental sums is simplicity, and the cost is still acceptable given the constraints.
4. If at any point the computed sum equals 14, we can immediately return success because we only need existence of one valid subset.
5. If no subset produces sum 14 after exhausting all masks, we conclude it is impossible.

### Why it works

Every subset of the array corresponds to exactly one binary mask, and every binary mask corresponds to exactly one subset. This bijection guarantees that iterating over all masks enumerates all possible subsets without omission or duplication. Since we check the sum for each subset explicitly, any valid combination summing to 14 must be encountered during iteration. Therefore, if one exists, the algorithm will find it; if none exists, the full enumeration will complete without triggering success.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:]))

    # in case input is split across lines
    while len(arr) < n:
        arr.extend(map(int, input().split()))

    target = 14

    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if mask & (1 << i):
                s += arr[i]
        if s == target:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The parsing step accounts for slightly irregular input formatting where numbers might be split across lines or combined inconsistently. The core logic is the bitmask enumeration. Each mask is interpreted independently, and we accumulate a local sum variable `s`. The early exit on finding 14 prevents unnecessary exploration once a valid subset is found.

A subtle implementation detail is ensuring that input parsing does not assume a strict line structure beyond the first token. In competitive programming environments, defensive parsing avoids runtime errors on malformed spacing.

## Worked Examples

### Example 1

Input corresponds to an array `[3, 11]`.

We enumerate subsets:

| mask | chosen elements | sum | check |
| --- | --- | --- | --- |
| 00 | [] | 0 | no |
| 01 | [3] | 3 | no |
| 10 | [11] | 11 | no |
| 11 | [3, 11] | 14 | yes |

At mask `11`, the sum becomes exactly 14, so the algorithm stops and outputs YES.

This demonstrates that the algorithm correctly identifies the full set as a valid subset without requiring any pruning or heuristics.

### Example 2

Input corresponds to `[6, -8, -4, -3, 0, 12, 17]`.

A partial trace:

| mask | chosen elements | sum | check |
| --- | --- | --- | --- |
| 0000001 | [6] | 6 | no |
| 0000010 | [-8] | -8 | no |
| 0001000 | [-3] | -3 | no |
| 0010000 | [0] | 0 | no |
| 0100000 | [12] | 12 | no |
| 1000000 | [17] | 17 | no |
| 0001010 | [-8, -3] | -11 | no |
| 0100101 | [6, 12] | 18 | no |
| 0100011 | [6, -8, 12] | 10 | no |
| 0100101 | [6, 12] again pattern | 18 | no |

Eventually, one of the masks produces sum 14, and the enumeration stops.

This example shows why we cannot rely on greedy selection. Positive numbers alone do not guarantee reaching 14, and negative values can be essential to adjust sums precisely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^n) | each subset mask is evaluated by scanning up to n elements |
| Space | O(1) | only fixed extra variables besides input array |

The constraint n ≤ 19 ensures that 2^n remains small enough for exhaustive enumeration. The worst case is well within typical Python limits, since the total number of operations stays around a few million.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (interpreted with standard formatting)
assert run("2\n3 11\n") == "YES", "sample 1"
assert run("6\n-8 -4 -3 0 12 17\n") == "YES", "sample 2"

# minimum size, single element equals target
assert run("1\n14\n") == "YES", "single element success"

# minimum size, single element not target
assert run("1\n5\n") == "NO", "single element failure"

# all negative values
assert run("3\n-1 -2 -3\n") == "NO", "all negative cannot reach 14"

# mixture requiring subset
assert run("4\n10 5 4 -5\n") == "YES", "needs combination 10+4"

# zero-heavy case
assert run("5\n0 0 0 14 1\n") == "YES", "direct presence and zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 14 | YES | direct match base case |
| single 5 | NO | impossible trivial case |
| all negatives | NO | unreachable positive target |
| mixed combo | YES | subset combination necessity |
| zeros included | YES | zeros do not affect feasibility |

## Edge Cases

A case with a single element equal to 14 is handled immediately by the subset mask where only that element is selected. During iteration, the mask with exactly one bit set corresponding to that element produces sum 14 and triggers early termination.

A case where all numbers are negative demonstrates that no subset can increase the sum to a positive target. The algorithm still enumerates all subsets, but every computed sum remains non-positive, so the equality check for 14 is never triggered, and the final output is NO.

A case containing zeros shows that extra elements that contribute nothing do not interfere with correctness. The subset containing only the element 14 still exists among masks, and additional zeros simply create duplicate sums but do not affect detection of the target subset.
