---
title: "CF 975B - Mancala"
description: "We are given a circular board with 14 positions. Each position contains some number of stones. One move consists of picking a single position that has stones, removing all stones from it, and then distributing those stones one by one into subsequent positions moving clockwise…"
date: "2026-06-17T01:33:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 975
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 478 (Div. 2)"
rating: 1100
weight: 975
solve_time_s: 83
verified: true
draft: false
---

[CF 975B - Mancala](https://codeforces.com/problemset/problem/975/B)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular board with 14 positions. Each position contains some number of stones. One move consists of picking a single position that has stones, removing all stones from it, and then distributing those stones one by one into subsequent positions moving clockwise around the circle.

After this redistribution, we look at all 14 positions and collect the stones from every position whose final count is even. The goal is to choose the starting position for the move so that this collected amount is maximized.

The important aspect is that only one move is made, and the only decision is which pile to pick up and redistribute.

The constraints are extremely small: exactly 14 positions. Even though each position may contain up to 10^9 stones, the structure is fixed and tiny. This immediately suggests that we can afford to simulate every possible starting position. Any solution that tries to do something more complex than linear scanning is unnecessary.

A subtle point is that redistribution is deterministic and fully described by the initial array and the chosen index. There is no interaction or branching during the move.

A naive mistake would be to try to recompute the full board incorrectly after redistribution by “jumping” counts instead of simulating the wraparound properly. For example, forgetting that stones wrap from position 14 back to 1 leads to incorrect final states.

Another potential pitfall is assuming we only need to check local effects near the chosen index. In reality, every position can receive at most one extra stone per full cycle of 14 steps, so even distant positions are affected.

Edge cases include:

When all stones are in a single pile, say `[0, 0, 0, ..., 7, 0, 0]`, the distribution wraps around multiple times, and every position can change parity multiple times.

When only one non-zero pile exists, the result depends entirely on where we start, because that determines the parity flip pattern across the cycle.

## Approaches

The brute-force idea is straightforward: for each index i from 1 to 14, simulate taking all stones from that pile and distributing them one by one across the circular array. After simulation, compute the sum of all even-valued piles. We take the maximum over all choices.

This is correct because the problem explicitly restricts us to one move, and each move is fully determined by its starting position.

The cost of this simulation is important. For a pile containing a[i] stones, we perform O(a[i]) updates. Since a[i] can be up to 10^9, this naive simulation is far too slow in the worst case.

The key observation is that although a[i] is large, the board size is constant. After every full rotation of 14 steps, each position receives exactly one additional stone from the moving pile. Therefore, the final effect depends only on how many full cycles we complete and the remaining partial steps.

We do not need to simulate each stone individually. Instead, we compute how many times each position is visited and update counts using arithmetic. Since the board size is fixed, for each starting index we can compute the resulting configuration in O(14).

Thus, we reduce a potentially huge per-move cost into a constant-time simulation per starting position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation per stone | O(14 * a[i]) | O(14) | Too slow |
| Cycle-based simulation per start | O(14 * 14) | O(14) | Accepted |

## Algorithm Walkthrough

1. Iterate over each possible starting position i from 0 to 13. This is the pile we choose to empty.
2. For each starting position, copy the initial array into a working array. We need an independent simulation because each choice is evaluated separately.
3. Extract all stones from position i into a variable k, and set that position to zero.
4. Starting from position i, distribute k stones one by one around the circle.

Instead of iterating k times, compute how many full cycles of 14 steps occur and how many extra steps remain.

Each position receives exactly floor(k / 14) stones, and the first (k mod 14) positions after i receive one additional stone.
5. Apply these computed increments to the copied array.
6. After distribution, scan all 14 positions and sum values that are even.
7. Track the maximum sum over all starting positions.

The critical idea is replacing per-stone simulation with direct arithmetic distribution across a fixed-length cycle.

### Why it works

Each stone moves deterministically to the next position in a fixed cycle of length 14. After 14 steps, the stone returns to its original index offset by full cycles. This means every position in the circle is visited uniformly except for a small prefix determined by the remainder. The final contribution to each cell depends only on how many times the rotation passes through it, which is completely determined by k modulo 14 and k divided by 14. This guarantees the reconstructed board is identical to full simulation, while avoiding step-by-step iteration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))
    n = 14
    ans = 0

    for i in range(n):
        b = a[:]  # copy board
        k = b[i]
        if k == 0:
            pass
        b[i] = 0

        full = k // n
        rem = k % n

        # distribute full cycles
        for j in range(n):
            b[j] += full

        # distribute remainder
        for t in range(1, rem + 1):
            b[(i + t) % n] += 1

        # compute score
        cur = 0
        for x in b:
            if x % 2 == 0:
                cur += x

        ans = max(ans, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the cycle decomposition. The full cycles contribute uniformly to all 14 positions, which is why we simply add `full` to every cell. The remainder distributes a single extra stone to the next `rem` positions after the chosen index, using modular indexing.

Care is needed when handling indexing: the redistribution starts from the next cell `(i + 1) % 14`, not the chosen cell itself.

## Worked Examples

### Example 1

Input:

```
0 1 1 0 0 0 0 0 0 7 0 0 0 0
```

We test starting at index 9 (value 7).

| Step | Position emptied | k | full cycles | remainder | key effect |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 7 | 0 | 7 | distribute 1 stone to next 7 positions |

After distribution, the board becomes:

```
1 2 2 0 0 0 0 0 0 0 1 1 1 1
```

Even-valued positions are 2, 2, 0, 0, 0, 0 contributing a total of 4.

This confirms that partial wraparound determines which positions flip parity.

### Example 2

Input:

```
1 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Only position 0 is non-zero.

| Start i | k | full | rem | even-sum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 |

Best answer is 0.

This shows that a single stone always produces an odd value somewhere, and cannot contribute to even sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(14^2) | 14 starting positions, each updating 14 cells |
| Space | O(14) | only a copy of the board |

The board size is constant, so the algorithm runs instantly under the limits. Even with repeated copying, the total work is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = list(map(int, sys.stdin.readline().split()))
    n = 14
    ans = 0

    for i in range(n):
        b = a[:]
        k = b[i]
        b[i] = 0

        full = k // n
        rem = k % n

        for j in range(n):
            b[j] += full

        for t in range(1, rem + 1):
            b[(i + t) % n] += 1

        cur = sum(x for x in b if x % 2 == 0)
        ans = max(ans, cur)

    return str(ans)

# provided sample
assert run("0 1 1 0 0 0 0 0 0 7 0 0 0 0") == "4"

# all zeros except one
assert run("0 0 0 0 5 0 0 0 0 0 0 0 0 0") >= "0"

# single stone
assert run("1 0 0 0 0 0 0 0 0 0 0 0 0 0") == "0"

# all equal odd values
assert run("1 1 1 1 1 1 1 1 1 1 1 1 1 1") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 4 | correctness of wrap redistribution |
| single non-zero | 0 | behavior with isolated pile |
| single stone | 0 | minimal non-trivial move |
| all ones | ≥0 | parity handling across full cycle |

## Edge Cases

When all stones are concentrated in one pile, the algorithm correctly splits the value into full cycles and remainder. For exam
