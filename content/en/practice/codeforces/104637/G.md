---
title: "CF 104637G - Frog Jumping"
description: "A frog starts at position 0 on a number line and repeatedly jumps left and right in a fixed pattern. The first jump moves it to the right by a, the second jump moves it to the left by b, and this alternation continues for k total jumps."
date: "2026-06-29T17:01:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104637
codeforces_index: "G"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u0431\u0430\u0437\u043e\u0432\u0430\u044f \u043c\u0430\u0442\u0435\u043c\u0430\u0442\u0438\u043a\u0430, \u0443\u0441\u043b\u043e\u0432\u0438\u044f, \u0446\u0438\u043a\u043b\u044b"
rating: 0
weight: 104637
solve_time_s: 59
verified: true
draft: false
---

[CF 104637G - Frog Jumping](https://codeforces.com/problemset/problem/104637/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

A frog starts at position 0 on a number line and repeatedly jumps left and right in a fixed pattern. The first jump moves it to the right by `a`, the second jump moves it to the left by `b`, and this alternation continues for `k` total jumps. Each query gives different values of `a`, `b`, and `k`, and we must determine the frog’s final position after performing exactly those jumps.

What matters here is that the movement is completely deterministic and periodic with a cycle of two jumps. One cycle consists of a right move of size `a` followed by a left move of size `b`. The frog’s position evolves as a simple alternating sum, but the number of jumps can be as large as 10^9, so explicitly simulating each step is impossible.

The constraints imply that any per-jump simulation is immediately infeasible. With up to 1000 queries and up to 10^9 steps per query, an O(k) approach would require up to 10^12 operations in the worst case, which is far beyond the limit. We must compress the process into constant time per query.

A subtle edge case arises when `k` is odd or even, because the last partial cycle behaves differently. For example, if `a = 5`, `b = 2`, and `k = 3`, the sequence is `+5, -2, +5`, resulting in 8. If `k = 4`, the last step would be `-2`, changing the balance. Any solution that assumes full pairs without handling leftovers will fail.

Another common pitfall is assuming symmetry or cancellation beyond full pairs. When `a` equals `b`, full cycles cancel, but incomplete cycles still produce non-zero values. For instance, with `a = b = 1` and `k = 999999999`, the result is 1, not 0.

## Approaches

A direct simulation maintains the current position and alternates adding `a` and subtracting `b` for each jump. This is straightforward and correct because it follows the definition exactly. However, it performs one arithmetic operation per jump, so for large `k` it becomes too slow.

The key observation is that jumps come in repeating pairs. Every two jumps contribute a net displacement of `a - b`. If we group the process into full pairs, we only need to compute how many full cycles of two jumps exist, and whether there is an extra single jump at the end.

If `k` is even, the frog completes exactly `k/2` full cycles, each contributing `a - b`. If `k` is odd, there are `(k-1)/2` full cycles plus one final right jump of `+a`.

This reduces the problem from linear simulation to simple arithmetic based on parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k) | O(1) | Too slow |
| Arithmetic Pair Compression | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

For each query:

1. Read `a`, `b`, and `k`. These define a fixed alternating movement pattern and how many steps we execute.
2. Compute how many full pairs of jumps exist using `k // 2`. Each pair consists of a `+a` move followed by a `-b` move.
3. Multiply the number of full pairs by `(a - b)` to get the total contribution of all complete cycles. This works because each full cycle returns a net displacement equal to the difference between the forward and backward jumps.
4. If `k` is odd, add one extra `+a` for the final incomplete step. This is necessary because the sequence always starts with a forward jump and odd-length sequences end on a forward move.
5. Output the resulting position.

### Why it works

The sequence is strictly periodic with period 2, and each period contributes a fixed net change of `a - b`. The only deviation from perfect pairing happens when `k` is odd, where the last step is always a forward jump. Since the process is linear and additive, splitting into disjoint pairs plus a possible remainder preserves the exact total displacement.

## Python Solution

```python
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

print("\n".join(out))
```

The solution processes each query independently. The key computation is the integer division `k // 2`, which counts full (a, -b) cycles. Multiplying by `(a - b)` collapses all those cycles into one arithmetic expression.

The conditional `if k % 2 == 1` handles the remaining single forward jump when `k` is odd. Since the first jump is always forward, the leftover step is never a subtraction.

All arithmetic is done in Python integers, which naturally support large values up to 10^9 * 10^9 without overflow issues.

## Worked Examples

### Example 1

Input: `a = 5, b = 2, k = 3`

| Step | Jump Type | Position |
| --- | --- | --- |
| 0 | start | 0 |
| 1 | +5 | 5 |
| 2 | -2 | 3 |
| 3 | +5 | 8 |

The algorithm computes `pairs = 1`, giving `1 * (5 - 2) = 3`, then adds the extra `+5` because `k` is odd, resulting in 8. This confirms that the pair compression matches the explicit simulation.

### Example 2

Input: `a = 100, b = 1, k = 4`

| Step | Jump Type | Position |
| --- | --- | --- |
| 0 | start | 0 |
| 1 | +100 | 100 |
| 2 | -1 | 99 |
| 3 | +100 | 199 |
| 4 | -1 | 198 |

The algorithm computes `pairs = 2`, giving `2 * (100 - 1) = 198`, with no remainder since `k` is even. The result matches the step-by-step simulation exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is processed in constant time using arithmetic operations only |
| Space | O(1) | Only a few variables are used regardless of input size |

The solution easily fits within constraints since even 1000 queries are handled with a handful of operations each.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
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
assert run("""6
5 2 3
100 1 4
1 10 5
1000000000 1 6
1 1 1000000000
1 1 999999999
""") == """8
198
-17
2999999997
0
1"""

# custom cases
assert run("""1
1 1 1
""") == "1", "single jump"

assert run("""1
10 20 2
""") == "-10", "one full cycle negative net"

assert run("""1
7 3 1
""") == "7", "only first jump"

assert run("""1
100 100 5
""") == "100", "full cancellation with leftover"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1,1,1` | `1` | minimal case, odd k |
| `10,20,2` | `-10` | full cycle negative net |
| `7,3,1` | `7` | single jump only |
| `100,100,5` | `100` | cancellation with leftover |

## Edge Cases

When `k = 1`, the algorithm sets `pairs = 0` and adds `+a`. For input `a = 7, b = 3, k = 1`, the result becomes 7, matching the definition since only the first forward jump occurs.

When `a = b`, every full pair contributes zero. For `a = b = 10, k = 5`, we get `pairs = 2`, so contribution is 0, and the leftover odd step adds `+10`, producing 10. A naive cancellation assumption would incorrectly return 0.

When `k` is even, no leftover exists, and the result depends entirely on `(a - b)`. For `a = 5, b = 2, k = 4`, we get `2 * 3 = 6`, matching the explicit sequence `5 - 2 + 5 - 2`.
