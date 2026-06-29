---
title: "CF 104665G - Spaghetti Game"
description: "Two players are playing a turn-based game that changes a single integer, the current number of spaghetti strands in a shared pile. The game always starts from zero. Lario moves first, then Muigi, and they alternate for up to 100 moves each."
date: "2026-06-29T09:59:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104665
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 1 (Advanced)"
rating: 0
weight: 104665
solve_time_s: 74
verified: false
draft: false
---

[CF 104665G - Spaghetti Game](https://codeforces.com/problemset/problem/104665/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

Two players are playing a turn-based game that changes a single integer, the current number of spaghetti strands in a shared pile. The game always starts from zero. Lario moves first, then Muigi, and they alternate for up to 100 moves each.

On Lario’s turn, he can increase the pile by choosing one of his allowed bundle sizes. On Muigi’s turn, he can decrease the pile by choosing one of his removal sizes, as long as the pile does not go negative. Both players are allowed to do nothing, but since both have positive options available, optimal play will never rely on skipping unless forced.

The only way to win is for Lario to make the pile reach at least a threshold value at the moment immediately after his move. If that ever happens within 100 rounds, the game ends instantly. Otherwise Muigi is considered the winner.

The interaction matters because Muigi always responds right after Lario, meaning any gain Lario achieves can potentially be partially undone before his next move. This makes it tempting to think the problem requires simulating the full game. However, the structure is simple enough that the entire process can be reduced to reasoning about extreme choices.

The constraints are small: all bundle sizes and the threshold are at most 100, and the number of rounds is fixed at 100. This strongly suggests that any solution must run in constant time per test and that we should avoid any simulation or search over strategies.

A subtle point is that victory is checked immediately after each Lario move, not only at the end. This creates a “peak value” problem rather than a final-value problem.

Edge cases that matter:

If Lario has a bundle large enough to reach the target immediately, for example `a = [20]` and `t = 15`, then Muigi never gets a chance to respond and Lario wins instantly. A solution that only reasons about final state after 100 rounds would miss this.

If Muigi’s best removal is larger than Lario’s best addition, for example `a = [3]` and `b = [10]`, then any gain Lario makes is immediately erased more than he can compensate, and the pile never grows in a meaningful way. A naive “sum over time” idea would incorrectly suggest possible growth.

Finally, even if Lario’s best move is smaller than the threshold, repeated accumulation might still reach the target before 100 rounds, so we must consider intermediate states, not just per-move maxima.

## Approaches

A brute-force interpretation would simulate every possible sequence of moves for both players. At each turn, Lario chooses one of n actions and Muigi chooses one of m actions, leading to a branching process. Even though the depth is bounded by 200 moves total, branching creates an exponential number of possible games. This is unnecessary because both players are clearly adversarial and deterministic in objective: Lario maximizes the pile, Muigi minimizes it.

The key observation is that both players have no state-dependent restrictions except the pile size, and their actions are independent additive constants. Therefore, optimal play collapses to always choosing extremal values: Lario always picks the maximum `a_i`, Muigi always picks the maximum `b_j`.

Once we reduce the game to these two constants, the entire process becomes a deterministic sequence. The remaining question is whether there exists a moment during the first 100 Lario moves when the pile reaches at least `t`.

The structure of the timeline reveals that after Lario’s k-th move, before Muigi responds, the pile equals:

`k * A - (k - 1) * B`, where `A = max(a_i)` and `B = max(b_j)`.

We only need to check whether this expression ever reaches `t` for some `k ≤ 100`. Because it is linear in k, its maximum occurs at one of the endpoints depending on the sign of `A - B`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(100 × nm) or worse | O(1) | Too slow and unnecessary |
| Optimal extremal reduction | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the entire interaction to two values: Lario’s strongest possible gain `A` and Muigi’s strongest possible loss `B`.

1. Compute `A = max(a_i)` and `B = max(b_j)`.

These represent the only moves that matter under optimal play because any weaker move is strictly dominated.
2. Consider the state after Lario’s first move. The pile is `A`.

If this already reaches `t`, Lario wins immediately since victory is checked right after his move.
3. Otherwise, consider the general k-th Lario move. After Lario moves and before Muigi responds, the pile is:

`f(k) = k*A - (k-1)*B = k(A - B) + B`.
4. Observe how this function behaves in k.

If `A ≥ B`, the function increases with k, so the best chance is at `k = 100`.

If `A < B`, the function decreases with k, so the best chance is at `k = 1`.
5. Evaluate the best reachable peak:

If `A ≥ B`, check `100*(A - B) + B ≥ t`.

If `A < B`, check `A ≥ t`.
6. If either condition holds, choose “Lario”, otherwise choose “Muigi”.

### Why it works

The process between Lario’s moves is fully linear and memoryless. Each full cycle contributes a fixed net change of `A - B`, while Muigi’s move only shifts the current offset. Because the only check for victory happens immediately after Lario’s turn, the game reduces to maximizing a linear function over a bounded integer interval. A linear function over integers achieves its maximum at an endpoint, so only the first and last meaningful positions need to be checked. This eliminates any possibility of hidden intermediate maxima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, t = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    A = max(a)
    B = max(b)

    # peak after first Lario move
    if A >= t:
        print("Lario")
        return

    if A >= B:
        be
```
