---
title: "CF 1213A - Chips Moving"
description: "We are given several chips placed on integer positions on a line. Our goal is to move all chips so that they end up on a single shared coordinate, using the cheapest possible sequence of moves. Each chip can move in two different ways."
date: "2026-06-15T18:30:41+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1213
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 582 (Div. 3)"
rating: 900
weight: 1213
solve_time_s: 114
verified: true
draft: false
---

[CF 1213A - Chips Moving](https://codeforces.com/problemset/problem/1213/A)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several chips placed on integer positions on a line. Our goal is to move all chips so that they end up on a single shared coordinate, using the cheapest possible sequence of moves.

Each chip can move in two different ways. A chip can jump by 2 units left or right at no cost, or it can move by 1 unit left or right at a cost of one coin. The key difficulty is that zero-cost moves let us change position parity freely within the same parity class, while odd shifts are what actually create cost.

The task is to compute the minimum total number of coins required so that all chips can be relocated onto the same integer position.

The constraints are small, with at most 100 chips. That means any solution that tries all candidate target positions is already feasible since checking a single target is linear in n, and even scanning all coordinates in the input range would still be acceptable in O(n^2). However, the structure of the moves suggests that a more mathematical simplification should exist, and the optimal solution should reduce the problem to something independent of large coordinate values up to 10^9.

A naive approach would consider choosing every possible target coordinate between the minimum and maximum chip positions and compute the cost of moving all chips there. The issue is not correctness but redundancy, since many targets behave identically due to parity.

A subtle edge case appears when all chips are already at the same position. In that case the answer is zero, and any reasoning based on movement cost must preserve this. Another edge case is when all positions share the same parity, for example all even numbers. In this case, zero-cost moves can align everything, which leads to a zero answer, even though distances between points might be large. A naive approach that incorrectly assumes cost equals distance would fail here.

## Approaches

The crucial observation is that moving by 2 is free, so any chip can move freely among all positions with the same parity without paying anything. This means that the only time we pay coins is when we need to change parity, since a ±1 move flips parity and costs one coin.

This turns the problem into a parity balancing problem rather than a distance minimization problem.

For any chosen target coordinate T, a chip at position x has two possibilities. If x and T have the same parity, we can move it entirely using ±2 steps, paying zero coins. If their parity differs, we must pay at least one coin to adjust parity, and then the rest can again be handled by free ±2 moves. Importantly, once a chip pays for a ±1 move, it can effectively align its parity with T and finish the rest for free.

So the cost for a fixed target T is simply the number of chips whose parity differs from T.

There are only two meaningful choices for T’s parity: even or odd. If T is even, then every even-position chip costs zero and every odd-position chip costs one coin. If T is odd, the roles reverse. Therefore, the answer is the minimum between the number of even positions and the number of odd positions.

The brute-force approach would try every possible target coordinate, compute parity mismatches for all chips, and take the minimum. Since parity fully determines cost, this reduces to just two cases instead of up to 10^9 candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over coordinates | O(n * range) | O(1) | Too slow / unnecessary |
| Parity counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many chip positions are even and how many are odd. This directly captures how many chips will match a chosen target parity.
2. Compute the number of coins required if we choose an even target position. In that case, every odd-position chip must pay exactly one coin to flip parity, so the cost is the number of odd positions.
3. Compute the number of coins required if we choose an odd target position. Symmetrically, this cost equals the number of even positions.
4. Return the minimum of the two values. This corresponds to choosing the target parity that minimizes the number of parity flips required.

### Why it works

The invariant is that after at most one ±1 move per chip, every chip can be aligned to the target parity class, and from that point all remaining movement can be done using free ±2 steps. Since ±2 moves preserve parity and allow unrestricted movement within a parity class, distance no longer contributes to cost. The only irreducible cost is whether a chip starts in the correct parity class relative to the chosen target.

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

The implementation only tracks parity counts. The loop separates numbers into even and odd buckets, which directly correspond to the two possible target parity choices. The final answer is the smaller bucket size.

No sorting or coordinate compression is needed because absolute positions beyond parity are irrelevant.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

| Step | Even count | Odd count | Cost if even target | Cost if odd target | Answer |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 3 | 3 | 0 | 0 |

If we choose an even target, all three chips must flip parity, costing 3 coins. If we choose an odd target, no chip needs a parity flip after alignment, since all are already odd, so cost is 0. The optimal choice is odd.

### Example 2

Input:

```
4
1 2 3 4
```

| Step | Even count | Odd count | Cost if even target | Cost if odd target | Answer |
| --- | --- | --- | --- | --- | --- |
| Start | 2 | 2 | 2 | 2 | 2 |

Both parities are balanced, so either choice produces the same cost. The answer is 2.

These examples show that only parity distribution matters, not actual distances or ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each chip is processed once to determine parity |
| Space | O(1) | Only two counters are maintained |

The constraints allow up to 100 chips, so a linear scan is trivially efficient. Even for much larger n, this solution remains optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    x = list(map(int, sys.stdin.readline().split()))

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

# all same parity (already optimal)
assert run("5\n2 4 6 8 10\n") == "0"

# all odd
assert run("4\n1 3 5 7\n") == "0"

# mixed balanced
assert run("4\n1 2 3 4\n") == "2"

# single element
assert run("1\n100\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all even | 0 | zero-cost alignment case |
| all odd | 0 | symmetry with even case |
| balanced mix | 2 | equal parity split |
| single chip | 0 | minimal edge case |

## Edge Cases

When all chips are already at identical positions, such as `5, 5, 5`, both even and odd counts collapse into a single group and the answer becomes zero immediately. The algorithm handles this naturally since one of the parity counts is zero.

When all chips share the same parity but have large coordinate differences, such as `2, 100, 100000`, the solution still returns zero because parity alignment removes all cost, regardless of distance.

When the distribution is mixed, such as alternating even and odd positions, every chip contributes to exactly one of the parity buckets. The algorithm still correctly selects the smaller bucket, ensuring minimal parity flips.
