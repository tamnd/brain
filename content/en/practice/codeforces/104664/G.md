---
title: "CF 104664G - Spaghetti Game"
description: "We are looking at a two-player game played on a single integer value, the spaghetti pile. The pile starts at zero. Two players act alternately for a fixed number of turns: Lario plays first, and both players get exactly 100 moves each."
date: "2026-06-29T10:06:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104664
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 2 (Beginner)"
rating: 0
weight: 104664
solve_time_s: 95
verified: false
draft: false
---

[CF 104664G - Spaghetti Game](https://codeforces.com/problemset/problem/104664/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are looking at a two-player game played on a single integer value, the spaghetti pile. The pile starts at zero. Two players act alternately for a fixed number of turns: Lario plays first, and both players get exactly 100 moves each. On Lario’s turn he may either add some fixed amount chosen from a list of values or do nothing. On Muigi’s turn he may either subtract some fixed amount chosen from his own list or do nothing. Every move is chosen freely from the allowed options for that player.

Lario’s objective is simple: at any moment during the process, if the pile ever reaches at least a threshold value t, he immediately wins. If 100 rounds complete without the pile ever reaching t, Muigi wins.

The twist is that we are not just simulating the game. We are allowed to choose which player to control, and then both players behave optimally: the controlled player tries to win, while the opponent tries to prevent that outcome.

The constraints are small: at most 100 move types per player, and at most 100 rounds. Even though this suggests a brute force game search might be possible, the interaction pattern and the independence of moves strongly hint that the structure is much simpler than a general state-space game.

A subtle edge case is that both players can skip turns. This matters only if all available moves are harmful, but since skipping is equivalent to adding or subtracting zero, it never creates a fundamentally new state. Another edge case is that the pile can become negative without restriction. A naive solution might try to bound the pile tightly around t, but that is unsafe because Muigi can push it arbitrarily low and then Lario may need multiple moves to recover.

A second hidden pitfall is assuming move ordering matters. One might think interleaving optimal choices changes the outcome, but both players have fixed numbers of turns, and each move is independent of previous choices except through the current sum, which makes the process additive.

## Approaches

A direct brute-force approach would treat this as a two-player game over states defined by current pile value, number of moves already used by each player, and whose turn it is. From a state, we branch over all possible choices of moves. Each branch continues until either Lario reaches t or all 100 rounds finish.

The problem with this approach is the size of the state space. The pile value can range from strongly negative to strongly positive. Each move changes it by up to 100, and there are 200 moves total, so the range can easily reach about [-20000, 20000]. Combining this with 100-by-100 move counters produces a state space far too large for any dynamic programming approach in one second.

The key observation is that the game is purely additive. Each Lario move contributes a fixed positive increment chosen from a set, and each Muigi move contributes a fixed non-positive decrement chosen from another set. There is no dependency between which particular move was chosen earlier and which moves are available later, and no constraints like limited resources or state changes beyond the sum.

This collapses the game into a deterministic optimization problem. Over 100 moves, Lario wants to maximize total gain, while Muigi wants to maximize total loss. Because each move is independent, both players will simply pick the best available option every time they act, or skip if all options are worse than zero.

So the entire game reduces to comparing two constants: the best single gain Lario can produce and the best single loss Muigi can produce.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game DP | O(100 · 100 · range) | O(100 · 100 · range) | Too slow |
| Greedy Extremes | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the maximum value among Lario’s bundle sizes, call it A. This represents the strongest possible single move Lario can repeatedly choose, since nothing prevents reuse.
2. Compute the maximum value among Muigi’s bundle sizes, call it B. This is the strongest possible single subtraction Muigi can repeatedly apply.
3. Observe that each player has exactly 100 turns, so if both play optimally, Lario contributes 100 · A total increase.
4. Similarly, Muigi contributes 100 · B total decrease.
5. The final pile value under optimal play is therefore 100 · A − 100 · B.
6. If this final value is at least t, choose Lario as the controlled player; otherwise choose Muigi.

### Why it works

The important invariant is that each player’s move sequence is independent and unconstrained across turns. The only interaction between players is through the scalar pile value, and each player’s optimal action on any turn is identical regardless of history: Lario always prefers the largest available addition, and Muigi always prefers the largest available subtraction.

Because the number of moves is fixed and neither player can affect the other’s available action set, any deviation from the maximum choice strictly reduces the controlling player’s final achievable extremum. This turns the game into a linear sum optimization with fixed multiplicity, eliminating any strategic branching.

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

    if 100 * (A - B) >= t:
        print("Lario")
    else:
        print("Muigi")

    sys.stdout.flush()

if __name__ == "__main__":
    solve()
```

The implementation reduces the entire interactive game to computing two maxima. The only subtlety is remembering that both players act 100 times, so the contribution is scaled by 100.

A common mistake is trying to simulate the interaction step by step or alternating moves. That is unnecessary because no move depends on the opponent’s last choice except through the scalar sum, and optimal behavior never changes across turns.

## Worked Examples

### Example 1

Input:

```
n=3, m=3, t=20
a = [3, 6, 15]
b = [2, 8, 15]
```

Here A = 15 and B = 15.

| Step | A | B | Expression | Value |
| --- | --- | --- | --- | --- |
| Compute maxima | 15 | 15 | - | - |
| Total effect | - | - | 100·15 − 100·15 | 0 |

Since 0 < 20, Muigi wins.

This shows a balanced case where both players have equally strong moves, so neither can push the pile upward overall.

### Example 2

Input:

```
n=2, m=2, t=50
a = [10, 1]
b = [3, 2]
```

A = 10, B = 3.

| Step | A | B | Expression | Value |
| --- | --- | --- | --- | --- |
| Compute maxima | 10 | 3 | - | - |
| Total effect | - | - | 100·10 − 100·3 | 700 |

Since 700 ≥ 50, Lario wins.

This demonstrates how repeated dominance in per-turn best moves overwhelms the threshold regardless of intermediate play.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | We scan both arrays once to compute maxima |
| Space | O(1) | Only a constant number of variables are stored |

The constraints are small enough that even a linear scan is trivial, but the main point is conceptual simplification rather than optimization. The solution eliminates the need to simulate 200 interactive turns entirely.

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

# sample
assert run("""3 3 20
3 6 15
2 8 15
""") == "Muigi"

# Lario clearly wins
assert run("""2 2 10
10 1
1 1
""") == "Lario"

# Muigi strongly dominates
assert run("""2 2 100
1 2
50 40
""") == "Muigi"

# equal zero-effect threshold case
assert run("""1 1 1
5
5
""") == "Muigi"

# minimal case
assert run("""1 1 1
1
1
""") == "Muigi"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal strengths | Muigi | balanced case |
| Lario strong | Lario | positive dominance |
| Muigi strong | Muigi | negative dominance |
| minimal tie | Muigi | threshold boundary |

## Edge Cases

One subtle case is when both players have identical maximum values. For example:

```
n=1, m=1, t=1
a = [5]
b = [5]
```

Here A = B = 5, so the net effect is zero. The pile never grows, so Lario cannot reach t unless t is 0 or negative. The algorithm correctly outputs Muigi.

Another case is when Lario has only weak moves and Muigi has none:

```
a = [1, 2], b = [0]
```

A = 2 and B = 0, so Lario gains 200 total. Even if Muigi always skips, he cannot stop growth. The formula correctly captures that skipping is just a zero move and does not alter optimality.

Finally, if t is extremely large relative to all moves, even the best-case accumulation fails. The computation still correctly scales by 100 moves, ensuring no undercounting of total potential growth.
