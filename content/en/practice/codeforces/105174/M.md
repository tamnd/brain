---
title: "CF 105174M - \u77f3\u5b50\u6e38\u620f"
description: "We are given a game with a pile of stones. Two players alternate turns, Alice moving first. On each turn, the player looks at the current number of stones, say x, and removes stones according to a rule that depends on parity."
date: "2026-06-27T08:18:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105174
codeforces_index: "M"
codeforces_contest_name: "The 22nd Sichuan University Programming Contest"
rating: 0
weight: 105174
solve_time_s: 72
verified: true
draft: false
---

[CF 105174M - \u77f3\u5b50\u6e38\u620f](https://codeforces.com/problemset/problem/105174/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a game with a pile of stones. Two players alternate turns, Alice moving first. On each turn, the player looks at the current number of stones, say x, and removes stones according to a rule that depends on parity.

If x is odd, the player has no choice and must remove exactly one stone, reducing the pile to x−1. If x is even, the player has two choices: remove one stone, or remove exactly half of the stones, moving the game to x−1 or x/2 respectively. A player who faces zero stones at the start of their turn loses immediately because no move is possible.

The task is to determine, for each initial n, whether Alice has a forced win assuming both players play optimally.

The constraints go up to one million test cases and stone counts up to one million. This immediately rules out any per-test simulation of the game. Even a linear scan per test case would be far too slow. Any acceptable solution must rely on either precomputation up to 10^6 or a closed-form characterization of winning states.

A subtle failure case for naive reasoning comes from assuming symmetry between even and odd states or assuming “taking half” is always strong. For example, at n = 2, both moves lead to 1, which is winning for the next player, so 2 is losing. At n = 4, taking half leads to 2 (losing), so 4 becomes winning, even though subtracting one leads to 3 (winning). This shows that even positions require considering both move options simultaneously, not just the larger reduction.

Another pitfall is assuming all odd positions are losing because they only allow a single move. That is false for small values like 1 and 3, where the forced chain leads into losing states for the opponent.

## Approaches

A direct way to solve the game is to treat every integer x as a game state and define whether it is winning or losing. From a state x, we look at all states reachable in one move and mark x as winning if at least one of those reachable states is losing.

This naturally leads to a dynamic programming formulation. Let dp[x] represent whether the current player has a winning strategy with x stones remaining. From the rules, if x is odd, the only transition is to x−1. If x is even, transitions go to x−1 and x/2. This gives a recurrence where dp[x] depends only on smaller indices, so we can compute dp from 0 up to n.

The brute-force DP is straightforward and correct, but its cost is O(n) per test case if recomputed each time, which is impossible for 10^6 queries. Even if computed once, answering queries is O(1), so the real issue is making sure we precompute once up to the maximum n.

The key structural observation is that after a small prefix, the game stabilizes into a simple pattern. Odd states beyond a threshold become consistently losing because their only move leads directly into a winning even state. Even states beyond a threshold become consistently winning because at least one of their two transitions always leads to a losing position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full recomputation per query | O(n) per query | O(1) | Too slow |
| DP precompute up to max n | O(n) total | O(n) | Accepted |

## Algorithm Walkthrough

We build the solution by computing dp values from 0 up to 1e6 once.

1. Initialize dp[0] as losing because no move exists from an empty pile.
2. For each x from 1 to max_n, determine dp[x] from previously computed states.
3. If x is odd, the only move is to x−1, so dp[x] becomes the opposite of dp[x−1]. This directly reflects that the current player wins if and only if the forced move leaves the opponent in a losing position.
4. If x is even, evaluate both options x−1 and x/2. If either leads to a losing state, mark dp[x] as winning. This encodes optimal play, since the player chooses the best available move.
5. After filling dp, answer each query in O(1) by printing whether dp[n] is true.

The reason this works is that dp[x] exactly encodes the definition of winning positions in a finite impartial game: a state is winning if it has at least one move to a losing state, and losing if all moves lead to winning states. Since every transition reduces x, the DP is well-founded and covers all dependencies.

A deeper structural simplification emerges from examining the recurrence: odd states propagate values from x−1, while even states are influenced by both x−1 and x/2. This quickly collapses into a stable pattern after small values, but the DP formulation is the cleanest way to guarantee correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

dp = [False] * (MAXN + 1)
dp[0] = False

for x in range(1, MAXN + 1):
    if x % 2 == 1:
        dp[x] = not dp[x - 1]
    else:
        lose = False
        if not dp[x - 1]:
            lose = True
        if not dp[x // 2]:
            lose = True
        dp[x] = lose

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append("Alice" if dp[n] else "Bob")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DP array is computed once globally, so each test case is answered in constant time. The transition logic follows directly from the move rules: odd states have a single forced transition, while even states check both possible moves and choose whether any leads to a losing position.

A common implementation mistake is recomputing dp inside the query loop, which would immediately time out under 10^6 inputs. Another subtle issue is forgetting that dp[x] should be true if any move is losing, not if all moves are winning.

## Worked Examples

Consider n = 5, 6, 7.

For this trace, we use the rule-based DP decisions.

### Example 1: n = 5

| x | parity | transitions | dp[x−1] | decision |
| --- | --- | --- | --- | --- |
| 5 | odd | 4 | dp[4]=True | dp[5]=False |

At 5, the only move goes to 4, which is already a winning position, so the current player has no way to force a win.

### Example 2: n = 6

| x | parity | x−1 | x/2 | result |
| --- | --- | --- | --- | --- |
| 6 | even | 5 (F) | 3 (T) | dp[6]=True |

At 6, even though moving to 5 is bad, the move to 3 is strong because it puts the opponent in a losing position.

These two examples show how even states can be saved by the halving move, while odd states are strictly determined by the previous position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAXN + t) | DP is computed once up to 10^6, then each query is O(1) |
| Space | O(MAXN) | dp array stores game results for all states |

The preprocessing fits comfortably within limits because 10^6 transitions are simple constant-time checks. Each query is answered in constant time, making the solution efficient even for the maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    import io as sysio

    out = sysio.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old
    return out.getvalue().strip()

# basic samples (illustrative)
assert run("1\n1\n") == "Alice"
assert run("1\n2\n") == "Bob"

# custom cases
assert run("1\n3\n") == "Alice", "small odd win case"
assert run("1\n4\n") == "Alice", "first even where half matters"
assert run("1\n5\n") == "Bob", "first stable losing odd"
assert run("1\n6\n") == "Alice", "even with winning half move"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | Alice | smallest winning position |
| 2 | Bob | smallest losing even |
| 3 | Alice | early odd exception |
| 4 | Alice | first halving advantage |
| 5 | Bob | stabilization of odd losses |
| 6 | Alice | even state using x/2 |

## Edge Cases

For n = 1, the state is immediately winning because the forced move leads to 0, leaving the opponent unable to move.

For n = 2, the state is losing because both possible moves lead to n = 1, which is winning, so there is no escape.

For n = 3, the forced move goes to 2, which is losing, making 3 winning even though it is odd.

For larger odd values such as n = 5, the forced move goes to 4, which is winning, so the position becomes losing. This demonstrates the transition where odd states stop being favorable once their only child becomes stable and winning.

For even values such as n = 4, the halving move goes to 2, which is losing, so 4 becomes winning even though subtracting one leads to a winning state.
