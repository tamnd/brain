---
title: "CF 1097B - Petr and a Combination Lock"
description: "We are given a circular lock that behaves like a 360-degree dial. Starting from zero, we perform a sequence of rotations, each rotation having a fixed magnitude, but we are free to choose its direction: clockwise or counterclockwise."
date: "2026-06-13T05:55:32+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 1097
codeforces_index: "B"
codeforces_contest_name: "Hello 2019"
rating: 1200
weight: 1097
solve_time_s: 237
verified: true
draft: false
---

[CF 1097B - Petr and a Combination Lock](https://codeforces.com/problemset/problem/1097/B)

**Rating:** 1200  
**Tags:** bitmasks, brute force, dp  
**Solve time:** 3m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular lock that behaves like a 360-degree dial. Starting from zero, we perform a sequence of rotations, each rotation having a fixed magnitude, but we are free to choose its direction: clockwise or counterclockwise. Clockwise can be thought of as adding the angle, while counterclockwise subtracts it.

After applying all rotations in order, the pointer ends at some final angle modulo 360. The task is to determine whether there exists a choice of directions for all rotations such that the final position returns exactly to zero.

The input size is very small, with at most 15 rotations and each rotation bounded by 180 degrees. This immediately suggests that exponential search over all direction choices is feasible because the total number of sign assignments is at most 2^15, which is about 32 thousand configurations. Even with straightforward evaluation per configuration, this is well within limits.

A subtle point is that the problem is purely about net sum modulo 360. There is no intermediate constraint, so the order is fixed and only signs matter.

Edge cases are mostly about small n. If n = 1, only one rotation exists, and the only way to end at zero is if that single rotation is either 0 or 360, but since values are at least 1, the answer is always NO. A naive misunderstanding might try to reduce modulo 360 immediately per step, but that does not affect correctness because we only care about the final sum.

Another edge situation is when the sum exceeds 360 multiple times. For example, rotations like 180, 180, 180 can still work because directions can cancel out to form a multiple of 360.

## Approaches

The most direct way to think about this problem is to try every possible way of assigning directions to each rotation. For each angle, we either add it or subtract it, then check if the resulting sum is divisible by 360. This brute-force approach tries all 2^n sign assignments. It is correct because it explicitly enumerates every valid configuration.

The cost of this approach grows exponentially. With n = 15, we evaluate up to 32768 configurations, and for each configuration we compute a sum in O(n), giving about 5×10^5 operations. This is already fine in Python, but we can simplify further.

The key observation is that we do not need any optimization beyond brute force, because the constraint is small enough. The problem is essentially a subset sum variant where each element can be positive or negative. This directly maps to bitmask enumeration.

So the optimal solution is simply to iterate over all masks from 0 to (1 << n) - 1, interpret each bit as a sign choice, compute the resulting sum, and check if it equals a multiple of 360.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (bitmask) | O(n · 2^n) | O(1) | Accepted |
| Optimal (same) | O(n · 2^n) | O(1) | Accepted |

In this problem, brute force is already optimal due to constraints.

## Algorithm Walkthrough

1. Read the list of angles. Each angle represents a fixed contribution whose direction is undecided.
2. Iterate over all possible subsets of sign assignments using bitmasks from 0 to (2^n - 1). Each bit indicates whether we rotate clockwise or counterclockwise for that step. This encodes all possible valid decision paths.
3. For each bitmask, initialize a running sum to zero. This sum represents the net angular displacement after applying chosen directions.
4. For each index i in the rotation list, check the i-th bit of the mask. If it is set, add a_i to the sum, otherwise subtract a_i. This models the two possible directions for each rotation.
5. After processing all rotations for a given mask, compute sum modulo 360. If it equals zero, a valid configuration exists and we can stop immediately.
6. If no mask produces a zero modulo result, conclude that no sequence of directions returns the pointer to the starting position.

### Why it works

Every valid sequence of directions corresponds uniquely to one bitmask. The transformation from direction choice to +a_i or -a_i preserves the exact final angle. Because we enumerate all 2^n possibilities, we cover every possible net result. The modulo condition captures the circular nature of the lock, ensuring that any multiple of 360 degrees is equivalent to zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = [int(input()) for _ in range(n)]
    
    for mask in range(1 << n):
        total = 0
        for i in range(n):
            if mask & (1 << i):
                total += a[i]
            else:
                total -= a[i]
        if total % 360 == 0:
            print("YES")
            return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the bitmask enumeration described earlier. Each mask represents a full assignment of clockwise or counterclockwise directions. The inner loop computes the resulting displacement. The modulo check handles wrap-around on the circular dial.

A common mistake is to forget that subtraction is equally valid as addition; both must be considered symmetrically. Another potential pitfall is trying to reduce intermediate values modulo 360 too early, which is safe mathematically but unnecessary and can obscure reasoning.

## Worked Examples

### Example 1

Input:

```
3
10
20
30
```

We test different sign assignments.

| Mask | Expression | Sum |
| --- | --- | --- |
| 000 | -10 -20 -30 | -60 |
| 001 | -10 -20 +30 | 0 |
| 010 | -10 +20 -30 | -20 |
| 011 | -10 +20 +30 | 40 |
| 100 | +10 -20 -30 | -40 |
| 101 | +10 -20 +30 | 20 |
| 110 | +10 +20 -30 | 0 |
| 111 | +10 +20 +30 | 60 |

We observe valid masks like 001 and 110 that produce sums divisible by 360 (in fact zero). This confirms feasibility.

### Example 2

Input:

```
1
1
```

| Mask | Expression | Sum |
| --- | --- | --- |
| 0 | -1 | -1 |
| 1 | +1 | 1 |

No configuration yields a multiple of 360, so the answer is NO.

This shows the edge case where a single non-zero rotation cannot be balanced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^n) | Each of 2^n masks evaluates n rotations |
| Space | O(1) | Only input storage and counters are used |

With n ≤ 15, the maximum operations are about 15 × 32768, which is comfortably fast in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3\n10\n20\n30\n") == "YES"

# single element impossible
assert run("1\n1\n") == "NO"

# already multiple of 360 via cancellation
assert run("2\n180\n180\n") == "YES"

# mixed case
assert run("3\n90\n90\n180\n") == "YES"

# all same small values
assert run("4\n10\n10\n10\n10\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | NO | single-step impossibility |
| 2 180 180 | YES | cancellation to 360 |
| 4 identical 10s | YES | combinational balancing |

## Edge Cases

For n = 1, the algorithm checks both +a and -a. Since a is between 1 and 180, neither equals a multiple of 360, so no mask satisfies the condition, correctly producing NO.

For cases where all angles are 180, such as 180 180, the enumeration includes (+180, -180) and (-180, +180), both summing to zero, correctly returning YES.

For larger mixed inputs like 90, 90, 90, 90, multiple masks exist that sum to 360 or 0, and the exhaustive search guarantees at least one is found if valid.
