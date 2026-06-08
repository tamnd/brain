---
title: "CF 1872A - Two Vessels"
description: "We are given two containers holding real-valued amounts of water. One starts with a, the other with b. We also have a cup that can transfer at most c units of water in a single operation."
date: "2026-06-08T23:17:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1872
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 895 (Div. 3)"
rating: 800
weight: 1872
solve_time_s: 73
verified: true
draft: false
---

[CF 1872A - Two Vessels](https://codeforces.com/problemset/problem/1872/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two containers holding real-valued amounts of water. One starts with `a`, the other with `b`. We also have a cup that can transfer at most `c` units of water in a single operation. In one operation we choose a source vessel, take some amount of water up to `c`, and pour it into the other vessel.

The process changes the two values asymmetrically, but the total amount of water remains constant. After each move, one vessel decreases by some amount and the other increases by the same amount. The goal is to make both vessels contain exactly the same amount.

Since the total water is fixed, the only possible final state is that each vessel contains `(a + b) / 2`. If `a == b`, the answer is already zero moves. Otherwise we are effectively trying to transfer exactly `|a - b| / 2` units of water from the larger vessel to the smaller one, using transfers of size at most `c`.

The constraints are very small: `a, b, c ≤ 100`, and up to `1000` test cases. This immediately rules out any simulation over fine-grained fractional states or search over continuous choices. Any correct solution must reduce the process to a direct arithmetic computation per test case.

A subtle edge case is when `c` is large enough that the full difference can be transferred in one move. Another is when `c` is very small, where many partial transfers are required. A naive greedy that always transfers exactly `c` can still work here, but only if carefully handling the remainder of the required transfer.

## Approaches

A brute-force interpretation would simulate the process step by step. At each step, we choose the larger vessel, transfer some amount up to `c`, and try to greedily reduce the difference. If we always transfer `c` (or the remaining needed amount if smaller), we reduce the absolute difference between `a` and `b`.

This simulation is correct because every operation strictly reduces `|a - b|` unless they are already equal. However, its complexity is proportional to the number of moves, which in the worst case is about `|a - b| / c`. Since values are small here, this is technically feasible, but it hides the actual structure: each move reduces the difference by at most `c`, and we only care about reaching zero difference.

The key observation is that we never need to track individual states. We only track the absolute difference `d = |a - b|`. Each move can reduce this difference by at most `c`, and since we can always choose the direction optimally (from larger to smaller), the optimal strategy is to always reduce the difference as much as possible. That turns the problem into a simple ceiling division: how many chunks of size `c` are needed to cover `d / 2` units of transfer, but more cleanly we reason in terms of difference reduction per move.

Each move reduces the difference by at most `2c` in terms of imbalance resolution perspective, but more directly: transferring `x` from larger to smaller reduces the difference by `2x`, so the optimal move always takes `x = min(c, remaining_needed/2)` in effect. This collapses to a simple greedy count: repeatedly subtract up to `c` from the imbalance until it disappears.

Thus the answer is `ceil(|a - b| / (2c))` if we model reduction symmetrically, but more cleanly derived in the standard CF solution, it simplifies to repeatedly reducing the difference until zero, which equals `ceil(|a - b| / (2c))`. In practice, the accepted formulation is `ceil(|a - b| / (2c))` which matches the fact each move moves `c` from one side to the other.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step simulation | O( | a-b | /c) |
| Direct formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the absolute difference `d = |a - b|`. This represents the total imbalance that must be eliminated through transfers.
2. If `d == 0`, output `0` immediately because both vessels are already equal and no operation is needed.
3. Each operation can move at most `c` units from one vessel to the other, which reduces the imbalance in a single direction optimally.
4. Since each move reduces the imbalance by exactly `2 * x` where `x ≤ c`, the best possible reduction per move is `2c`.
5. Compute the number of moves as the smallest integer `k` such that `k * 2c ≥ d`.
6. Output `ceil(d / (2c))`.

### Why it works

The state of the system is fully described by the difference `d`. Every move preserves total mass and changes `d` by subtracting twice the transferred amount. Because we always choose the larger vessel as the source, we always reduce `d` rather than increasing it. No sequence of moves can do better than always using the maximum allowed transfer `c`, since any smaller transfer would reduce `d` more slowly and never create compensating future gains. This makes the process equivalent to repeatedly subtracting `2c` from `d` until it reaches zero, which yields the optimal number of steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    d = abs(a - b)
    if d == 0:
        print(0)
    else:
        # each move can reduce difference by at most 2c
        print((d + 2 * c - 1) // (2 * c))
```

The implementation begins by reading each test case and computing the absolute difference between the two vessels. The only non-trivial step is recognizing that we never need to simulate transfers explicitly; the entire process reduces to shrinking this difference.

The integer ceiling division `(d + 2*c - 1) // (2*c)` encodes the fact that we are grouping the imbalance into chunks of size `2c`. The edge case `d == 0` is handled separately to avoid unnecessary arithmetic, although the formula would also return zero.

## Worked Examples

### Example 1: `a = 3, b = 7, c = 2`

We compute `d = 4`.

| Step | Difference d | Action | Reduction | New d |
| --- | --- | --- | --- | --- |
| 0 | 4 | start | - | 4 |
| 1 | 4 | transfer 2 from b to a | 4 → 0 | 0 |

Only one move is required because one transfer of size `c` exactly eliminates the imbalance. This confirms that when `d ≤ 2c`, a single move suffices.

### Example 2: `a = 17, b = 4, c = 3`

We compute `d = 13`.

| Step | Difference d | Action | Reduction | New d |
| --- | --- | --- | --- | --- |
| 0 | 13 | start | - | 13 |
| 1 | 13 | transfer 3 | 13 → 7 | 7 |
| 2 | 7 | transfer 3 | 7 → 1 | 1 |
| 3 | 1 | transfer 1 | 1 → 0 | 0 |

This shows that repeated maximal transfers reduce the difference greedily until it vanishes. The final move is a partial transfer, which is why ceiling behavior is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within constraints since even 1000 test cases require only simple arithmetic evaluations.

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
        a, b, c = map(int, input().split())
        d = abs(a - b)
        if d == 0:
            out.append("0")
        else:
            out.append(str((d + 2*c - 1) // (2*c)))
    return "\n".join(out)

# provided samples
assert run("""6
3 7 2
17 4 3
17 17 1
17 21 100
1 100 1
97 4 3
""") == """1
3
0
1
50
16"""

# custom cases
assert run("1\n1 1 1\n") == "0", "already equal"
assert run("1\n1 3 10\n") == "1", "large c single move"
assert run("1\n1 100 1\n") == "50", "maximum chain transfers"
assert run("1\n10 1 2\n") == "3", "direction reversed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | already equal case |
| `1 3 10` | `1` | single move suffices |
| `1 100 1` | `50` | long sequence of minimal transfers |
| `10 1 2` | `3` | correctness under reversed roles |

## Edge Cases

One important edge case is when the difference is smaller than the cup capacity. For example `a = 1, b = 4, c = 10` gives `d = 3`. The algorithm computes `(3 + 19) // 20 = 1`, which matches the fact that we can transfer all required water in one move without needing to split it.

Another case is when `a == b`. Here the computed difference is zero, and the early exit returns zero moves immediately. Without this check, the formula still produces zero, but the explicit branch makes the logic consistent with the interpretation that no operation is required.

A third case is when `c = 1`, forcing unit transfers. For `a = 1, b = 100`, the difference is 99, and each move reduces it by at most 2. The formula yields `(99 + 1) // 2 = 50`, which matches the necessity of many small adjustments, alternating direction optimally to converge exactly to equality.
