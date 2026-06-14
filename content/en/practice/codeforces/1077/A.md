---
title: "CF 1077A - Frog Jumping"
description: "A frog moves along a number line starting from position zero. Its movement is strictly alternating: it first jumps to the right by a fixed distance a, then to the left by b, then right again by a, and so on."
date: "2026-06-15T06:38:19+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1077
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 521 (Div. 3)"
rating: 800
weight: 1077
solve_time_s: 118
verified: true
draft: false
---

[CF 1077A - Frog Jumping](https://codeforces.com/problemset/problem/1077/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

A frog moves along a number line starting from position zero. Its movement is strictly alternating: it first jumps to the right by a fixed distance `a`, then to the left by `b`, then right again by `a`, and so on. Each query describes one such frog independently, and asks where it ends up after performing exactly `k` jumps.

The input consists of multiple independent scenarios. Each scenario provides the two step sizes and the number of jumps. The output for each scenario is the final coordinate after simulating this alternating movement.

The key observation about constraints is that `k` can be as large as 10^9, so simulating each jump directly is impossible. A naive simulation would take O(k) time per query, which in the worst case becomes 10^9 operations per query and immediately exceeds time limits. With up to 1000 queries, this is completely infeasible. The solution must compute the final position in constant time per query.

A subtle edge case arises when `k = 1`. Only a single right jump occurs, so the answer is exactly `a`. Another important case is when `k` is even and `a` equals `b`, since all motion cancels out and the frog returns to zero. These cancellations can mislead a step-by-step implementation if parity is not handled correctly.

## Approaches

A direct approach is to simulate each jump sequentially. Starting at zero, we alternate adding `a` and subtracting `b`. This is correct because it follows the definition exactly. However, for large `k`, this requires repeating the same two operations up to 10^9 times per query. Even with efficient arithmetic, this approach is too slow.

The structure of the movement is periodic with period two. Every pair of jumps consists of a net movement of `a - b`. This observation allows us to collapse the entire sequence into blocks of two jumps. Once we group jumps into pairs, we only need to handle whether there is an extra final jump when `k` is odd.

If `k` is even, there are exactly `k/2` full pairs, each contributing `a - b`, so the result is `(k/2) * (a - b)`. If `k` is odd, there are `(k//2)` full pairs plus one additional rightward jump of `a`.

This reduces the problem from linear simulation to constant-time arithmetic per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k) per query | O(1) | Too slow |
| Pair Compression | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. Read `a`, `b`, and `k`. These define the alternating step sizes and how many moves to apply.
2. Compute how many full `(right, left)` pairs exist using integer division `k // 2`. Each such pair contributes a net displacement of `a - b` because the frog first moves right by `a` and then left by `b`.
3. Multiply the number of full pairs by `(a - b)` to accumulate the contribution of all complete cycles. This captures all jumps except possibly the last one when `k` is odd.
4. If `k` is odd, add one extra rightward jump of size `a`, since the sequence always starts with a right jump and odd-length sequences end on a right move.
5. Output the computed position.

### Why it works

The sequence of movements decomposes into independent two-step blocks. Each block always starts from the same structural state: a right jump followed by a left jump. Because addition on a line is associative, the final position depends only on the sum of these blocks and the presence of a single leftover first-step jump when `k` is odd. No intermediate position affects future step sizes or directions, so collapsing into pairs preserves the total displacement exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, k = map(int, input().split())

    pairs = k // 2
    res = pairs * (a - b)

    if k % 2 == 1:
        res += a

    print(res)
```

The implementation directly mirrors the decomposition derived in the algorithm. The integer division isolates full two-step cycles, and the parity check handles the final unmatched right jump. The arithmetic uses Python integers, so overflow is not a concern even when values reach 10^18 scale.

## Worked Examples

We trace two queries to see how the decomposition behaves.

### Example 1

Input: `a = 5, b = 2, k = 3`

| Step | k status | pairs (k//2) | partial result | extra jump |
| --- | --- | --- | --- | --- |
| 1 | start | 1 | 1 × (5 - 2) = 3 |  |
| 2 | odd k | 1 | 3 | +5 |

Final result is 8.

This shows how one full cycle contributes a net +3, and the remaining single jump adds +5.

### Example 2

Input: `a = 1, b = 10, k = 5`

| Step | k status | pairs (k//2) | partial result | extra jump |
| --- | --- | --- | --- | --- |
| 1 | start | 2 | 2 × (1 - 10) = -18 |  |
| 2 | odd k | 2 | -18 | +1 |

Final result is -17.

This confirms that negative net movement from pairs is corrected by the final right jump.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is processed with constant arithmetic operations |
| Space | O(1) | Only a few variables are used per query |

The solution easily fits within limits since even 1000 queries involve only simple integer arithmetic operations.

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
        a, b, k = map(int, input().split())
        pairs = k // 2
        res = pairs * (a - b)
        if k % 2 == 1:
            res += a
        out.append(str(res))
    return "\n".join(out)

# provided samples
assert run("6\n5 2 3\n100 1 4\n1 10 5\n1000000000 1 6\n1 1 1000000000\n1 1 999999999\n") == "8\n198\n-17\n2999999997\n0\n1"

# custom cases
assert run("1\n1 1 1\n") == "1"
assert run("1\n10 10 2\n") == "0"
assert run("1\n3 5 1\n") == "3"
assert run("1\n3 5 2\n") == "-2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | 1 | Single right jump |
| `10 10 2` | 0 | Perfect cancellation in a pair |
| `3 5 1` | 3 | Only first jump is applied |
| `3 5 2` | -2 | One full pair with negative net movement |

## Edge Cases

When `k = 1`, the algorithm correctly computes `k//2 = 0` so no pair contribution is added, and the final odd-step adds `a`. This matches the definition since only one right jump occurs.

When `k = 2`, the algorithm produces exactly `a - b`, because there is one full pair and no leftover jump. This directly matches the movement `0 → a → a - b`.

When `a = b`, every pair contributes zero, so only an odd leftover jump can produce a non-zero result. For even `k`, the result is always zero, and for odd `k`, it is exactly `a`.
