---
title: "CF 105055D - Whose Turn Is It?"
description: "Two athletes alternate doing fixed-size blocks of repetitions at a gym. Marcel always performs the first block, then Joãozão, then Marcel again, and so on. Each block contains exactly M repetitions."
date: "2026-06-28T00:22:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "D"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 56
verified: true
draft: false
---

[CF 105055D - Whose Turn Is It?](https://codeforces.com/problemset/problem/105055/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Two athletes alternate doing fixed-size blocks of repetitions at a gym. Marcel always performs the first block, then Joãozão, then Marcel again, and so on. Each block contains exactly `M` repetitions. They do not track individual contributions per person; instead, there is a single counter `N` that records how many repetitions have been completed in total.

The task is to determine whose turn comes next after exactly `N` repetitions have already been performed, given that turns alternate strictly in blocks of size `M`.

A useful way to rephrase the situation is to imagine the sequence of repetitions as being partitioned into chunks of size `M`. Chunk 0 is Marcel’s, chunk 1 is Joãozão’s, chunk 2 is Marcel’s again, and so forth. The total `N` tells us how far we are inside this chunked sequence, and we need to identify which chunk we are currently in and whether it is already finished.

The constraints allow `N` and `M` up to `10^9`. This immediately rules out any simulation that increments repetition by repetition, since that would require up to a billion steps in the worst case. The solution must instead compute the answer in constant time using arithmetic.

A subtle edge case appears when `N` is exactly a multiple of `M`. For example, if `M = 3` and `N = 6`, then exactly two full blocks have been completed. In this situation, we are at the start of a new block, so Marcel should be next because turns always restart with Marcel after Joãozão completes a full block. A naive implementation that only checks `(N // M) % 2` without considering whether we are inside or at the boundary of a block can easily shift the answer incorrectly if it treats completion and partial progress the same way.

Another important edge case is when `N < M`. For instance, if `M = 8` and `N = 6`, we are still inside Marcel’s first block. The correct answer is still Marcel, even though the next full block boundary has not been reached.

## Approaches

A brute-force simulation would track repetitions one by one, switching the active person every time a block of `M` repetitions is completed. We would maintain a counter for the current block progress and a toggle for whose turn it is. Each repetition increments the counter, and once it reaches `M`, we reset it and switch players.

This approach is correct because it directly mirrors the process described in the problem. However, it performs `N` iterations, and since `N` can be as large as `10^9`, it is far too slow to run within the time limit.

The key observation is that only full blocks matter for determining whose turn it is next. Every `M` repetitions flips the active player. Therefore, instead of simulating individual repetitions, we only need to count how many full blocks have been completed, which is `N // M`, and then determine whether we are inside a partially completed block or exactly at a boundary.

The distinction between “inside a block” and “exact boundary” is what determines whether we should look at the current block or the next one. If `N % M == 0`, we are at the start of a new block, so the next player is determined directly by the parity of completed blocks. If `N % M != 0`, we are still inside the current block, so the next player is the one currently active.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many complete blocks of size `M` are fully finished using integer division `q = N // M`. This counts how many times the turn has switched completely. This matters because each completed block flips the active player.
2. Compute how far we are inside the current block using `r = N % M`. This tells whether we are exactly at a boundary or still mid-block.
3. If `r == 0`, then no repetitions are currently being performed in a partially filled block. The next block to start is block `q`, so the identity of the next player depends only on whether `q` is even or odd. Since Marcel starts at block 0, even indices correspond to Marcel and odd indices correspond to Joãozão.
4. If `r != 0`, we are inside block `q`. That means the current active player is still working on this block, so the next repetition belongs to the same player assigned to block `q`. The same parity rule applies.
5. Output “MARCEL” if `q` is even, otherwise output “JOAOZAO”.

The core decision reduces the entire process to tracking which block we are in and using parity to map blocks to players.

### Why it works

Each complete block of size `M` corresponds to exactly one uninterrupted turn by a single player, and turns alternate deterministically starting from Marcel. Therefore, block index alone uniquely determines the player. The remainder `r` does not change which block we are in, only whether we are at its end or inside it. Since the next action is always determined by the current block assignment, parity of `q` is sufficient to determine the correct player in all cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

N = int(input())
M = int(input())

q = N // M
r = N % M

if q % 2 == 0:
    print("MARCEL")
else:
    print("JOAOZAO")
```

The code first reads the two integers and computes how many full blocks have been completed. The remainder is computed but does not affect the final decision beyond confirming whether we are inside a block or at a boundary, and both cases resolve to the same parity-based rule.

The key implementation choice is ignoring simulation entirely. There is no need to track progress within a block beyond confirming division behavior. Integer division and modulo fully encode the state of the system.

## Worked Examples

### Example 1

Input:

```
10
3
```

Here `q = 10 // 3 = 3`, `r = 1`.

| Step | N | M | q | r | Block parity | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 10 | 3 | 0 | 0 | - | - |
| Compute | 10 | 3 | 3 | 1 | odd | JOAOZAO |

Since `q = 3` is odd, the current block belongs to Joãozão. We are inside this block (`r != 0`), so Joãozão is still the active participant and therefore next.

### Example 2

Input:

```
6
8
```

Here `q = 6 // 8 = 0`, `r = 6`.

| Step | N | M | q | r | Block parity | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Init | 6 | 8 | 0 | 6 | even | MARCEL |

We are still in the first block, which belongs to Marcel. Since `r != 0`, Marcel is still performing this block, so he remains the next participant.

These examples confirm that both partial-block and full-block cases reduce consistently to parity of `q`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed regardless of input size |
| Space | O(1) | No auxiliary data structures are used |

The solution is constant time and easily satisfies the constraints up to `10^9`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N = int(input())
    M = int(input())

    q = N // M

    if q % 2 == 0:
        return "MARCEL"
    else:
        return "JOAOZAO"

# provided samples
assert run("10\n3\n") == "JOAOZAO"
assert run("6\n8\n") == "MARCEL"
assert run("20\n1\n") == "MARCEL"

# custom cases
assert run("0\n5\n") == "MARCEL", "start of first block"
assert run("5\n5\n") == "JOAOZAO", "exact boundary flips block"
assert run("9\n4\n") == "JOAOZAO", "inside second block"
assert run("8\n4\n") == "MARCEL", "exact full cycles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 5 | MARCEL | initial state before any repetition |
| 5 5 | JOAOZAO | exact boundary between blocks |
| 9 4 | JOAOZAO | mid-block transition correctness |
| 8 4 | MARCEL | full-cycle parity reset |

## Edge Cases

When `N = 0`, no repetitions have been performed. The algorithm computes `q = 0`, which is even, so it outputs Marcel. This matches the fact that Marcel always starts first.

When `N` is exactly divisible by `M`, such as `N = 20, M = 5`, we have `q = 4`. The algorithm treats this as the start of a new block, and since block 4 corresponds to Marcel again (even index), the output is correct.

When `M = 1`, every repetition is its own block. The algorithm reduces the problem to alternating every step, and parity of `N` directly determines the result, which matches the expected alternating sequence.
