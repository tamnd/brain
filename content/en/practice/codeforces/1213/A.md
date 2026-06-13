---
title: "CF 1213A - Chips Moving"
description: "We are given several chips placed on integer points along a line. Each chip can be moved independently, and the goal is to bring all chips to exactly the same coordinate using the least number of coins. The movement rules create two different costs."
date: "2026-06-13T17:16:43+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1213
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 582 (Div. 3)"
rating: 900
weight: 1213
solve_time_s: 355
verified: false
draft: false
---

[CF 1213A - Chips Moving](https://codeforces.com/problemset/problem/1213/A)

**Rating:** 900  
**Tags:** math  
**Solve time:** 5m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several chips placed on integer points along a line. Each chip can be moved independently, and the goal is to bring all chips to exactly the same coordinate using the least number of coins.

The movement rules create two different costs. Moving a chip by two units in either direction costs nothing, while moving it by one unit costs one coin. Because we are free to apply operations any number of times, each chip can be repositioned arbitrarily, but with a cost structure that depends on how many odd-length adjustments we use.

The task is to choose a single final coordinate and compute the minimum total cost required to move every chip there.

The constraints are small enough that a direct quadratic check over all possible target positions is feasible. With at most 100 chips, even trying each position as a candidate and summing costs yields at most 10,000 evaluations, each involving up to 100 computations. This is comfortably within limits.

A subtle point is that chips that start far apart might still interact in terms of parity. Since moving by two is free, only parity changes incur cost. Any solution that ignores parity will fail.

A typical incorrect idea is to assume the optimal position is always the median or mean of coordinates. For example, if chips are at positions 1 and 3, choosing 2 as target seems natural, but both chips must spend coins to adjust parity, and that cost is unavoidable regardless of proximity. Another mistake is to assume cost depends on distance; in fact, distance in steps of 2 is irrelevant.

Edge cases arise when all chips already have the same parity. For example, input `2 4 6` requires zero cost since all can be moved freely by steps of two to meet. In contrast, `1 2` forces at least one coin because their parities differ.

## Approaches

A brute-force approach is straightforward. We try every possible integer coordinate between the minimum and maximum chip positions as the final meeting point. For each candidate target, we compute the cost to move each chip to that target and sum it up. The best result among all candidates is the answer. This works because we directly simulate all possibilities.

However, the range of coordinates can be up to 1e9, so iterating over every integer position is impossible. Even restricting to the given coordinates still leaves O(n^2) checks, and for each check we might simulate moves costing O(1), giving O(n^2) total. That is acceptable for n = 100, but we can simplify further.

The key observation is that moving by 2 is free, so only parity matters. A chip can freely switch between positions of the same parity without cost. Therefore, all even positions are equivalent to each other, and all odd positions are equivalent to each other, except for the cost of changing parity.

This reduces the problem to deciding whether we align everything to an even coordinate or to an odd coordinate. If we pick an even target, every odd chip must spend 1 coin to flip parity once. Similarly, if we pick an odd target, every even chip must pay 1 coin. So the answer is simply the minimum between the number of odd chips and the number of even chips.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · R) or O(n²) | O(1) | Too slow for full range |
| Parity Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all chip positions and count how many are even and how many are odd. This classification is enough because only parity determines cost behavior.
2. Compute the number of even positions and the number of odd positions separately.
3. Consider choosing an even final coordinate. Every odd chip must pay exactly one coin to adjust parity, so the cost equals the number of odd chips.
4. Consider choosing an odd final coordinate. Every even chip must pay exactly one coin, so the cost equals the number of even chips.
5. Return the minimum of these two values, since we are free to pick either parity for the final meeting point.

### Why it works

The key invariant is that any chip can move between any two integers of the same parity with zero cost using repeated ±2 moves. This partitions the integer line into two independent equivalence classes: even and odd. Within each class, movement is free, so the only irreversible operation is switching parity, which always costs exactly one coin per chip. Because of this, the entire optimization collapses to choosing which parity class becomes the target, and minimizing the number of chips that must switch classes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
x = list(map(int, input().split()))

even = 0
odd = 0

for v in x:
    if v % 2 == 0:
        even += 1
    else:
        odd += 1

print(min(even, odd))
```

The solution reads all coordinates and counts parity groups. The logic relies on the fact that parity is the only invariant under free moves. The final answer is the smaller group because we choose that parity as the target class.

No sorting or simulation is required. The code avoids floating-point or distance reasoning entirely.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We track parity counts step by step.

| Step | Even count | Odd count | Action |
| --- | --- | --- | --- |
| Read 1 | 0 | 1 | 1 is odd |
| Read 2 | 1 | 1 | 2 is even |
| Read 3 | 1 | 2 | 3 is odd |

If we choose even target, cost is 2 (both odd chips must flip). If we choose odd target, cost is 1 (only one even chip must flip). Minimum is 1.

This confirms that the optimal strategy depends only on parity distribution, not spatial distance.

### Example 2

Input:

```
4
2 4 6 7
```

| Step | Even count | Odd count | Action |
| --- | --- | --- | --- |
| Read 2 | 1 | 0 | even |
| Read 4 | 2 | 0 | even |
| Read 6 | 3 | 0 | even |
| Read 7 | 3 | 1 | odd |

Choosing even target costs 1 (only chip 7). Choosing odd target costs 3 (all evens). Minimum is 1.

This shows how a single opposite-parity chip dominates the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass counting parity |
| Space | O(1) | Only two counters used |

The input size is at most 100, so linear processing is instantaneous. Even under multiple test scenarios, the solution remains trivially fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    even = 0
    odd = 0
    for v in x:
        if v % 2 == 0:
            even += 1
        else:
            odd += 1

    return str(min(even, odd))

# provided sample
assert run("3\n1 2 3\n") == "1"

# all equal
assert run("3\n4 4 4\n") == "0"

# all odd
assert run("5\n1 3 5 7 9\n") == "0"

# alternating parity
assert run("4\n1 2 3 4\n") == "2"

# single chip
assert run("1\n10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal evens | 0 | no cost when already aligned |
| all odd | 0 | parity-consistent group needs no flips |
| mixed parity | min(even, odd) | correct parity decision |
| single element | 0 | trivial base case |

## Edge Cases

For an input where all chips already share the same parity, such as `6 10 14`, the algorithm counts all as even and returns zero. Since there is no need to switch parity, no chip pays any coin, matching the computed result.

For an input with one chip of opposite parity like `2 4 6 7`, the algorithm identifies one odd and three evens. Choosing even as target makes only the odd chip pay one coin, which matches the minimum.

For a fully alternating small case like `1 2`, the counts are equal, so either parity choice yields cost 1. The algorithm correctly returns `1`, reflecting that exactly one chip must switch parity.
