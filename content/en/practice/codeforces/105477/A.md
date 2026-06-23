---
title: "CF 105477A - Coins"
description: "We are given several independent scenarios. In each scenario, Baq owns a collection of coins, each coin having a positive integer value. Using any number of these coins, he can form sums by choosing a subset and adding their values."
date: "2026-06-23T18:11:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105477
codeforces_index: "A"
codeforces_contest_name: "XXII Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105477
solve_time_s: 68
verified: true
draft: false
---

[CF 105477A - Coins](https://codeforces.com/problemset/problem/105477/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario, Baq owns a collection of coins, each coin having a positive integer value. Using any number of these coins, he can form sums by choosing a subset and adding their values. The question is not about how many sums he can form, but about the smallest positive integer amount that cannot be represented as such a sum.

So for each test case, we are effectively looking at all subset sums of a multiset of positive integers and asking for the first gap in the set of achievable sums.

The key constraint is that the number of coins can be large, up to 10,000 in the hardest cases, and coin values can be as large as 10^9. This immediately rules out any attempt to explicitly enumerate subset sums, since even for moderate n, the number of subset sums grows exponentially. Even dynamic programming over sums is infeasible because the sum range is unbounded and could be extremely large.

A subtle failure case for naive thinking is assuming we need to generate all reachable sums and then scan for the first missing one. For example, with coins [1, 3], the reachable sums are {1, 3, 4}, so 2 is missing. But if we try to brute force all combinations, we already exceed feasible computation for slightly larger inputs like 30 arbitrary coins.

Another misleading intuition is that sorting alone is enough. Sorting helps structure the reasoning, but without the correct greedy accumulation logic, it does not directly yield the answer.

## Approaches

The brute-force idea is straightforward: generate every subset sum and then check which positive integer is missing. This works conceptually because it directly models the definition of reachability. However, each coin doubles the number of subsets, so for n coins we get 2^n sums. At n = 40, this already becomes astronomically large, and the constraint allows up to 10,000 coins, making this approach fundamentally impossible.

The key observation comes from shifting perspective: instead of tracking all sums, we track the smallest prefix of positive integers we can already form continuously starting from 1. Suppose we have already determined that every value from 1 to x can be formed. Now consider a new coin value v. If v is greater than x + 1, then x + 1 is immediately unreachable, because all existing sums are at most x and adding v would overshoot the gap without filling it. If v is at most x + 1, then we can extend the reachable interval up to x + v, because every value up to x can be combined with v to fill the next segment.

This greedy interval expansion is the core idea. Instead of thinking in terms of combinations, we maintain a growing contiguous segment of representable sums. The first gap appears exactly when a coin arrives that cannot bridge the next missing value.

Sorting the coins is essential, because we want to process small values first to build the smallest continuous range as efficiently as possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subset sums) | O(2^n) | O(2^n) | Too slow |
| Greedy interval expansion | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Sort the coin values in non-decreasing order. This ensures we always try to extend the smallest reachable range first.
2. Initialize a variable `reach = 0`, meaning we can currently form all sums from 1 up to `reach` continuously.
3. Iterate through each coin value `v` in sorted order.
4. If `v > reach + 1`, stop immediately and output `reach + 1`. This is the first value that cannot be formed because we have a gap that cannot be bridged.
5. Otherwise, update `reach = reach + v`. This expands the continuous reachable range.
6. After processing all coins, output `reach + 1`, since we can form everything up to `reach` but nothing beyond.

The key reasoning in step 4 is that if there is a gap at `reach + 1`, no later coin can fix it because all later coins are at least as large as `v`, hence also too large to fill the missing value.

### Why it works

At any moment after processing some prefix of sorted coins, we maintain the invariant that every integer in the range `[1, reach]` is representable using some subset of processed coins. When we see a coin `v` such that `v <= reach + 1`, we can combine it with all previously achievable sums to extend the reachable range without creating gaps. If `v > reach + 1`, there is no way to construct `reach + 1`, since all combinations either stay within `[1, reach]` or jump beyond it. This invariant guarantees that the first violation exactly corresponds to the smallest unreachable sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    arr.sort()

    reach = 0
    for v in arr:
        if v > reach + 1:
            break
        reach += v

    print(reach + 1)
```

The solution starts by sorting the coins so that we always consider them in increasing order, which is necessary for maintaining a contiguous reachable interval. The variable `reach` tracks the maximum continuous sum we can currently form. Each coin either extends this interval or exposes a gap. The condition `v > reach + 1` captures exactly the first unreachable integer, since `reach + 1` is the smallest missing value at any stage.

A common implementation mistake is initializing `reach` incorrectly. It must start at 0 because before using any coins, only the empty sum is achievable, and the first positive sum we care about is 1. Another subtle point is the strict inequality: using `>=` instead of `>` breaks correctness, since a coin equal to `reach + 1` should still extend the reachable range.

## Worked Examples

### Example 1

Input: `[2, 4, 16, 8, 1]`

After sorting: `[1, 2, 4, 8, 16]`

| Step | Coin v | reach before | Condition | reach after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 ≤ 1 | 1 |
| 2 | 2 | 1 | 2 ≤ 2 | 3 |
| 3 | 4 | 3 | 4 ≤ 4 | 7 |
| 4 | 8 | 7 | 8 ≤ 8 | 15 |
| 5 | 16 | 15 | 16 ≤ 16 | 31 |

After processing all coins, reachable range is `[1, 31]`, so answer is 32.

This trace shows how powers of two-like growth keeps extending a fully continuous interval without gaps.

### Example 2

Input: `[3, 5, 7, 1]`

Sorted: `[1, 3, 5, 7]`

| Step | Coin v | reach before | Condition | reach after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 ≤ 1 | 1 |
| 2 | 3 | 1 | 3 > 2 | stop |

We stop immediately at the second coin because we cannot form 2. The answer is 2.

This demonstrates how a single missing bridge early in the sorted order immediately determines the result, regardless of later coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, linear scan afterward |
| Space | O(1) | aside from input storage, only a few variables are used |

The constraints allow up to 10,000 coins per test and up to 500 test cases, so at worst about 5 million elements are processed in sorting operations overall. This fits comfortably within limits in Python with efficient input handling.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        arr.sort()

        reach = 0
        for v in arr:
            if v > reach + 1:
                break
            reach += v

        out.append(str(reach + 1))

    return "\n".join(out)

# provided samples
assert run("""3
5
2 4 16 8 1
3
1 2 3
4
3 5 7 1
""") == """32
7
2"""

# minimum size
assert run("""1
1
1
""") == "2"

# gap immediately
assert run("""1
2
2 3
""") == "1"

# full continuous
assert run("""1
4
1 2 3 4
""") == "11"

# large powers of two behavior
assert run("""1
5
1 2 4 8 16
""") == "32"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single coin 1 | 2 | smallest boundary case |
| 2,3 | 1 | immediate gap at start |
| 1 2 3 4 | 11 | fully continuous expansion |
| powers of two | 32 | maximal contiguous growth pattern |

## Edge Cases

For a single coin with value 1, the sorted array is `[1]`. The algorithm sets `reach = 1`, and since no gap appears, it outputs `2`. This matches the fact that only 1 is constructible, and 2 is missing.

For coins like `[2, 3]`, sorting yields the same order. Initially `reach = 0`, and the first coin is 2. Since `2 > 1`, the algorithm stops immediately and returns `1`, correctly identifying that no positive sum can be formed.

For a fully dense set like `[1, 2, 3, 4]`, each coin satisfies `v <= reach + 1`, so the reachable interval grows continuously to 10, and the answer becomes 11. This confirms the invariant that no gaps appear when each new coin is small enough to bridge the next missing integer.
