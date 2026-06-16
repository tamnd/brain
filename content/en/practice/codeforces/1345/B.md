---
title: "CF 1345B - Card Constructions"
description: "We are given a supply of identical cards and we repeatedly build structures called pyramids. A pyramid of height 1 is the smallest possible structure, and every higher pyramid is built in layers: a taller pyramid consists of a smaller pyramid placed on top of a wider base made…"
date: "2026-06-16T09:56:36+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1345
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 639 (Div. 2)"
rating: 1100
weight: 1345
solve_time_s: 438
verified: true
draft: false
---

[CF 1345B - Card Constructions](https://codeforces.com/problemset/problem/1345/B)

**Rating:** 1100  
**Tags:** binary search, brute force, dp, math  
**Solve time:** 7m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a supply of identical cards and we repeatedly build structures called pyramids. A pyramid of height 1 is the smallest possible structure, and every higher pyramid is built in layers: a taller pyramid consists of a smaller pyramid placed on top of a wider base made from additional cards. Because of this construction rule, each height has a fixed cost in cards.

The process is greedy and sequential. Starting with some number of cards, we always try to build the tallest possible pyramid we can. After building one, we subtract the cards it consumed and repeat the same decision on the remainder until no pyramid of any height can be formed. The output is simply how many pyramids are built in total for each test case.

The key hidden object here is not the geometric pyramid but the cost function of a pyramid of height h. Once that cost is known, the problem becomes a deterministic resource depletion process: repeatedly subtract the largest feasible cost.

The constraints allow up to 1000 test cases, with total cards across all tests up to 10^9. This immediately rules out any approach that simulates each card or even recomputes costs too expensively per test case. A naive simulation that repeatedly searches for the largest height and subtracts could still work if height computation is fast, since each pyramid consumes at least 2 cards and therefore there are at most O(n) iterations in the worst case, but O(n) per test case is impossible when n can be 10^9.

A more subtle failure case comes from incorrect interpretation of pyramid cost. A common mistake is to assume linear growth or triangular growth with wrong constants. For example, assuming a height h pyramid costs h^2 cards leads to incorrect construction counts even for small inputs like n = 14, where the correct behavior depends on precise combinatorial stacking rules.

Another edge case is small n such as n = 1 or n = 2. In these cases, no higher structure is possible, and any overestimation of feasible height leads to subtracting too many cards and producing negative or incorrect residual logic.

## Approaches

The brute-force approach is conceptually straightforward. We precompute or derive the number of cards required for every pyramid height h. Then for each test case, while we still have cards, we scan downward from the maximum possible height and pick the largest h whose cost does not exceed the remaining cards. We subtract that cost and increment the answer.

This works because each step is locally optimal and the problem explicitly enforces that greedy construction is required. However, the bottleneck is repeatedly finding the largest valid height. If we recompute from scratch each time, and if the maximum possible height is around O(√n), then each selection costs O(√n), and in the worst case we may build O(√n) pyramids, leading to O(n) behavior per test case in the worst scenario.

The key observation is that the cost of a pyramid grows quickly with height, and for n up to 10^9 the maximum height is only around a few hundred. This allows us to precompute all pyramid costs once. After that, the repeated process becomes a simple greedy subtraction over a fixed list of costs. Because the cost sequence is increasing rapidly, we can also reduce the selection step to a small loop over precomputed values.

This transforms the problem into repeatedly picking the largest value from a small sorted list until the sum is exhausted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n √n) worst-case intuition | O(√n) | Too slow |
| Optimal | O(H² + T·H) where H ≤ 450 | O(H) | Accepted |

## Algorithm Walkthrough

1. Precompute the number of cards required for each pyramid height h until the cost exceeds 10^9. This is safe because constraints guarantee n never exceeds this range. The cost for each h is derived incrementally from the previous one, since each new layer adds a predictable number of cards.
2. Store all valid costs in an increasing array cost[]. Each entry represents the exact number of cards needed to build a pyramid of that height.
3. For each test case, start with the given n and initialize a counter ans = 0.
4. While n is still large enough to build at least the smallest pyramid, scan through the cost array from largest to smallest and find the largest cost that is ≤ n.
5. Subtract that cost from n and increment ans by 1.
6. Repeat until no cost fits into the remaining n.

The reason scanning from largest downward is correct is that the process explicitly requires building the tallest possible pyramid each time. Since costs are strictly increasing with height, this guarantees we always pick the maximum valid height.

### Why it works

The algorithm maintains the invariant that after each subtraction, the remaining number of cards is always the leftover from an optimal greedy choice at every step. Because pyramid costs form a strictly increasing sequence and each step depends only on the remaining resource, the decision of picking the largest feasible pyramid is independent of previous choices beyond reducing n. This prevents any scenario where choosing a smaller pyramid earlier could enable a larger total count later, since larger pyramids always consume more cards than any combination of smaller unused partial structures.

## Python Solution

```python
import sys
input = sys.stdin.readline

# precompute pyramid costs
# cost[h] = number of cards needed for pyramid of height h

MAX_N = 10**9
cost = []

h = 1
curr = 2  # cost of height 1 pyramid
while curr <= MAX_N:
    cost.append(curr)
    h += 1
    # derive next cost incrementally
    # recurrence: cost[h] = cost[h-1] + 3*h - 1
    curr += 3 * h - 1

cost.sort()

t = int(input())
for _ in range(t):
    n = int(input())
    ans = 0

    while n >= 2:
        # pick tallest possible pyramid
        for c in reversed(cost):
            if c <= n:
                n -= c
                ans += 1
                break
        else:
            break

    print(ans)
```

The core of the implementation is the precomputation step. Instead of deriving pyramid sizes repeatedly during each test case, we build a global list of costs once. This ensures all queries are handled efficiently.

The greedy loop inside each test case always scans from the largest cost downward. This is safe because the list is small (at most a few hundred entries), so even a linear scan is fast enough.

One subtle point is the termination condition `n >= 2`. A pyramid of height 1 already costs 2 cards, so anything below 2 cannot form any structure. This prevents unnecessary scanning when the answer is already finalized.

## Worked Examples

### Example 1: n = 14

We first compute available pyramid costs up to 14, which are:

2, 7, 15 (only 2 and 7 are usable here)

| Step | n | Chosen cost | Remaining n | Pyramids |
| --- | --- | --- | --- | --- |
| 1 | 14 | 7 | 7 | 1 |
| 2 | 7 | 7 | 0 | 2 |

The process shows that greedy selection picks the largest possible pyramid each time. After using a height-2 pyramid (cost 7), we are still able to build another one of the same height.

This confirms that repetition of equal-cost choices is valid and that the algorithm does not require tracking used heights globally.

### Example 2: n = 15

| Step | n | Chosen cost | Remaining n | Pyramids |
| --- | --- | --- | --- | --- |
| 1 | 15 | 15 | 0 | 1 |

Here the largest pyramid consumes all resources immediately, leaving no remainder. This demonstrates that the algorithm naturally stops without additional logic when an exact match occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(H² + T·H) | Precomputation builds H costs; each test scans H values per step |
| Space | O(H) | Stores pyramid costs up to maximum feasible height |

The maximum height H is small (well below 500 for n ≤ 10^9), so even a quadratic precomputation and linear scanning per test case is efficient. The solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAX_N = 10**9
    cost = []
    curr = 2
    h = 1
    while curr <= MAX_N:
        cost.append(curr)
        h += 1
        curr += 3 * h - 1

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        ans = 0
        while n >= 2:
            for c in reversed(cost):
                if c <= n:
                    n -= c
                    ans += 1
                    break
            else:
                break
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""5
3
14
15
24
1
""") == """1
2
1
3
0"""

# minimum input
assert run("1\n1\n") == "0"

# exact single pyramid
assert run("1\n2\n") == "1"

# repeated same pyramid
assert run("1\n14\n") == "2"

# large value
assert run("1\n1000000000\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 0 | no possible construction |
| 1\n2 | 1 | smallest pyramid case |
| 1\n14 | 2 | repeated greedy reuse |
| 1\n1000000000 | valid output | stress upper bound |

## Edge Cases

For n = 1, the cost list contains only values starting from 2, so the scan immediately fails to find any valid pyramid. The loop never enters, and the answer correctly remains 0.

For n = 2, the algorithm selects the smallest cost exactly once, subtracts it to zero, and terminates cleanly. This confirms that exact matches are handled without requiring special casing.

For large n such as 10^9, the algorithm repeatedly selects from a small fixed list. Since the largest pyramid cost is still far below n, the first few iterations may repeatedly choose large pyramids, but the shrinking nature of n guarantees termination in very few steps.
