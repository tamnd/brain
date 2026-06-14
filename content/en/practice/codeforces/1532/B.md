---
title: "CF 1532B - Frog Jumping"
description: "The frog moves along a straight number line starting from position 0. Its motion is fully deterministic: it alternates between two fixed step sizes."
date: "2026-06-14T18:21:48+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math"]
categories: ["algorithms"]
codeforces_contest: 1532
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Practice 7"
rating: 0
weight: 1532
solve_time_s: 167
verified: true
draft: false
---

[CF 1532B - Frog Jumping](https://codeforces.com/problemset/problem/1532/B)

**Rating:** -  
**Tags:** *special, math  
**Solve time:** 2m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The frog moves along a straight number line starting from position 0. Its motion is fully deterministic: it alternates between two fixed step sizes. On the first move it goes right by distance `a`, on the second move it goes left by `b`, then right by `a` again, then left by `b`, and so on until it performs `k` jumps.

Each query is independent, and for each one we need the final coordinate after exactly `k` such alternating jumps.

The constraint `k ≤ 10^9` immediately rules out simulating each jump step-by-step. Even though each operation is simple addition or subtraction, performing up to a billion operations per query would exceed any realistic time limit. With up to 1000 queries, a naive simulation would reach up to 10^12 operations in the worst case, which is infeasible.

The key difficulty is not computational complexity alone but recognizing that the movement pattern is periodic with a period of 2, so the process can be compressed into counting full pairs of moves.

A common mistake comes from mishandling the last incomplete pair of moves. For example, when `k = 1`, only the initial `+a` should be applied, and no subtraction occurs. When `k = 2`, the net movement is `a - b`. When `k = 3`, it becomes `a - b + a`, and so on. Any approach that assumes full pairs only (i.e., `k // 2 * (a - b)`) will fail for odd `k` if it does not account for the extra forward jump.

Another subtle issue is integer overflow in languages with fixed-width integers. Since `a, b, k` can be up to `10^9`, intermediate values like `k * a` can reach `10^18`, which requires 64-bit or Python’s arbitrary precision integers.

## Approaches

The brute-force approach directly simulates the frog’s jumps. Starting from position 0, we iterate from 1 to `k`, adding `a` on odd steps and subtracting `b` on even steps. This is correct because it follows the definition exactly. However, its cost is linear in `k`, so across all queries it could require up to 10^12 operations, which is far beyond feasible limits.

The key observation is that jumps come in repeating pairs: `( +a, -b )`. Each full pair contributes a net movement of `a - b`. If we group the sequence into complete pairs, we get `k // 2` such pairs. What remains is a possible extra first move if `k` is odd. That extra move is always a `+a`.

So the entire process reduces to computing how many full pairs exist and whether one extra forward jump is needed. This eliminates all iteration and reduces each query to constant time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per query | O(1) | Too slow |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `a`, `b`, and `k` for each query. These define the step sizes and the number of moves to simulate.
2. Compute how many complete two-step cycles exist using `k // 2`. Each cycle contains one `+a` and one `-b`, so it contributes a net displacement of `a - b`.
3. Multiply the number of full cycles by `(a - b)` to obtain the contribution from all paired moves. This compresses all even-indexed behavior into one arithmetic expression.
4. If `k` is odd, add one additional `+a` to account for the last unpaired forward jump. This is necessary because the sequence always starts with a forward step.
5. Output the resulting sum.

### Why it works

The sequence of moves is strictly periodic with length 2 after the first move is considered. Every pair `( +a, -b )` has a fixed net effect independent of position or history. Because addition is associative, grouping operations into disjoint pairs does not change the final result. The only exception is when the sequence length is odd, in which case the final unpaired operation is always the initial `+a` step. This guarantees the formula exactly reconstructs the full prefix sum of the infinite alternating sequence truncated at `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
out = []

for _ in range(t):
    a, b, k = map(int, input().split())
    
    pairs = k // 2
    ans = pairs * (a - b)
    
    if k % 2 == 1:
        ans += a
    
    out.append(str(ans))

print("\n".join(out))
```

The solution directly implements the derived decomposition. The expression `pairs * (a - b)` encodes all complete cycles, while the conditional `if k % 2 == 1` handles the leftover first jump. The result is accumulated as strings to avoid repeated I/O overhead inside the loop.

Care is needed in maintaining correct order of operations: computing `k // 2` first avoids repeated division, and grouping `(a - b)` ensures we do not accidentally mix contributions from different steps.

## Worked Examples

We trace two representative queries.

### Example 1

Input: `a = 5, b = 2, k = 3`

| Step | Action | Contribution | Position |
| --- | --- | --- | --- |
| 1 | +5 | +5 | 5 |
| 2 | -2 | -2 | 3 |
| 3 | +5 | +5 | 8 |

This shows one full pair plus an extra forward jump. The formula gives `k // 2 = 1`, so `1 * (5 - 2) = 3`, plus extra `5`, giving `8`.

This confirms the decomposition handles odd `k` correctly.

### Example 2

Input: `a = 100, b = 1, k = 4`

| Step | Action | Contribution | Position |
| --- | --- | --- | --- |
| 1 | +100 | +100 | 100 |
| 2 | -1 | -1 | 99 |
| 3 | +100 | +100 | 199 |
| 4 | -1 | -1 | 198 |

There are two full pairs, each contributing `99`, so total is `198`. No leftover jump exists since `k` is even.

This confirms the pairing logic fully captures repeated structure without explicit simulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is processed in constant arithmetic time |
| Space | O(1) | Only a few integer variables are used regardless of input size |

The solution easily fits within limits since even `t = 1000` results in only 1000 constant-time computations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b, k = map(int, input().split())
        pairs = k // 2
        ans = pairs * (a - b)
        if k % 2 == 1:
            ans += a
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("6\n5 2 3\n100 1 4\n1 10 5\n1000000000 1 6\n1 1 1000000000\n1 1 999999999\n") == "8\n198\n-17\n2999999997\n0\n1"

# minimum k
assert run("1\n10 5 1\n") == "10"

# even k simple cancellation
assert run("1\n3 3 10\n") == "0"

# large imbalance
assert run("1\n1 1000000000 2\n") == "-999999999"

# odd k boundary
assert run("1\n7 2 7\n") == "21"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `k = 1` | single `a` | minimal edge case |
| equal `a, b` | 0 or `a` if odd | cancellation behavior |
| large `b` | large negative | overflow-safe arithmetic |
| odd `k` | extra `a` included | parity handling |

## Edge Cases

When `k = 1`, the algorithm computes `k // 2 = 0`, so the pair contribution is 0 and since `k` is odd it adds `a`. For example `a = 7, b = 2, k = 1` produces `7`, matching the single jump definition.

When `a = b`, every full pair contributes zero net movement. For `a = 3, b = 3, k = 5`, we get two full pairs giving 0 and one extra `+3`, resulting in `3`, which matches the explicit sequence `3 - 3 + 3 - 3 + 3`.

When `k` is even and large, such as `k = 10^9`, all movement is captured by `k // 2` pairs. No special handling is needed beyond integer multiplication, since Python naturally supports large integers and the formula remains stable.
