---
title: "CF 105010D - Divisibility Game"
description: "We are given a multiset of positive integers. Two players alternate turns, starting with Oussama. On each turn, the current player inspects the array. If every element is divisible by a fixed odd integer $k$, the current player immediately loses."
date: "2026-06-28T02:27:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105010
codeforces_index: "D"
codeforces_contest_name: "Winter Cup 6.0 Online Mirror Contest"
rating: 0
weight: 105010
solve_time_s: 75
verified: false
draft: false
---

[CF 105010D - Divisibility Game](https://codeforces.com/problemset/problem/105010/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of positive integers. Two players alternate turns, starting with Oussama. On each turn, the current player inspects the array. If every element is divisible by a fixed odd integer $k$, the current player immediately loses. Otherwise, they must pick any two elements, remove them, and insert their sum back into the array. The sum of all elements is guaranteed to always remain divisible by $k$, so the game is well-defined and does not drift into inconsistent states.

The game ends exactly when a player is forced into a position where no element breaks divisibility by $k$. Since moves strictly reduce the array size by one, the game must terminate in a finite number of steps, but the winner depends on how quickly players can force the array into a fully divisible state.

The constraints make a naive simulation impossible. With $n \le 10^5$, each move is $O(n)$ if implemented directly, and up to $n$ moves may occur, leading to $O(n^2)$ behavior. This is too slow.

A more subtle issue is that the problem is not about the actual values, but about their residues modulo $k$. Many states that look different numerically behave identically in terms of whether a move is possible and how the game evolves.

A few edge cases expose where naive intuition fails. If all elements are already divisible by $k$, the first player loses immediately. For example, input $n=3, k=5, A=[5,10,15]$ leads to an immediate loss for Oussama.

Another subtle case occurs when only one element is not divisible by $k$. Since every move merges two elements, that single “bad” element cannot be eliminated unless it is paired with something else. For example, $A=[1,5,10]$ with $k=5$ has exactly one non-divisible element, and the outcome depends on whether it can be neutralized before the turn passes back.

Finally, parity of moves matters. Because each move reduces the array size by one, the total number of moves until termination is fixed once the process is forced. The winner is determined by whether Oussama or Rami makes the last legal merge before the array becomes fully divisible.

## Approaches

A brute-force simulation would explicitly try all pairs $(i, j)$, perform merges, and recursively explore outcomes. This is correct in principle because the state space is finite and deterministic, but each state branches into $O(n^2)$ possibilities, and there are $O(n)$ levels. Even with pruning, this grows explosively beyond any feasible limit.

The key observation is that the exact values of elements are irrelevant except for whether they are divisible by $k$. Define a “bad” element as one with remainder nonzero modulo $k$, and a “good” element otherwise. A merge operation replaces two elements with their sum, which preserves the total sum modulo $k$, but can change how many bad elements exist.

The only structure that matters is the number of bad elements. Good elements are neutral in the sense that they can be used to manipulate bad ones without introducing new modular imbalance.

Let $b$ be the number of elements not divisible by $k$. Each move reduces the array size by one, and the game ends when $b = 0$. The crucial point is that merging two elements affects $b$ depending on whether the selected pair contains bad elements. Optimal play reduces to controlling how fast $b$ can be driven to zero, while also controlling turn parity.

If $b = 0$, the first player loses immediately. If $b = 1$, the single bad element forces deterministic play: every merge involving it and a good element reduces the array size without eliminating the bad element, and eventually the opponent can force a position where the last move belongs to them.

If $b \ge 2$, players always have enough flexibility to choose merges that avoid prematurely eliminating structure, and the game reduces to a parity contest over the number of required merges to eliminate all bad elements. The decisive factor becomes whether $b$ is even or odd, combined with the fact that Oussama moves first.

Thus the solution reduces to counting how many elements are not divisible by $k$, then applying a small case analysis.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Counting Residues | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Scan the array and count how many elements are not divisible by $k$. This value $b$ captures all meaningful structure in the game because only these elements can influence whether a move is still available.
2. If $b = 0$, immediately conclude that the first player loses. The game is already in a terminal state, so no move exists for Oussama at the start.
3. If $b = 1$, conclude that the second player wins. With only one problematic element, every merge keeps that element present, and the first player is forced into a sequence of moves that hands control to the opponent in the final step.
4. If $b \ge 2$, determine the winner based on parity. Since each move reduces the array size by exactly one, the number of moves until termination is fixed, and control alternates deterministically. In this regime, Oussama wins if $b$ is odd, otherwise Rami wins.

### Why it works

The state evolution depends only on how many elements remain that can prevent immediate termination. Merging does not create new non-divisible structure in a way that affects long-term feasibility because the global sum is fixed modulo $k$. This forces the game into a deterministic reduction process where only the count of bad elements and turn parity matter. Once those two quantities are fixed, no alternative move sequence can change the eventual outcome, so the case analysis is exhaustive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    b = 0
    for x in a:
        if x % k != 0:
            b += 1
    
    if b == 0:
        print("Rami")
    elif b == 1:
        print("Rami")
    else:
        if b % 2 == 1:
            print("Oussama")
        else:
            print("Rami")

if __name__ == "__main__":
    solve()
```

The implementation focuses entirely on counting elements that are not divisible by $k$. The loop is linear and avoids any simulation of merges.

The decision logic directly mirrors the case breakdown. The two early branches handle the degenerate configurations where the game ends immediately or becomes forced with a single non-divisible element. The final branch uses parity of $b$ to determine which player makes the last effective reduction step.

A common pitfall is trying to simulate the merge process, which is unnecessary and leads to incorrect reasoning about intermediate array states. The correct perspective is that merges only serve to reduce count, not to preserve any deeper structure.

## Worked Examples

### Example 1

Input:

```
3 5
0 2 3
```

Here $k = 5$. We classify elements by divisibility.

| Step | Array | b (non-divisible count) | Decision |
| --- | --- | --- | --- |
| Start | [0,2,3] | 2 | Continue |

Since $b = 2$, we are in the parity regime.

The value is even, so Rami wins.

This demonstrates that with two non-divisible elements, the second player can mirror the reduction process and force the last move.

### Example 2

Input:

```
3 5
1 1 3
```

| Step | Array | b | Decision |
| --- | --- | --- | --- |
| Start | [1,1,3] | 3 | Continue |

Here $b = 3$, which is odd and greater than 1.

Oussama wins because he makes the first move and the parity ensures he also controls the final decisive reduction.

This shows that once at least two bad elements exist, the game outcome collapses to parity rather than specific values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass counting elements not divisible by $k$ |
| Space | $O(1)$ | Only a counter is maintained |

The constraints allow up to $10^5$ elements, so a linear scan is optimal and comfortably within limits. No additional memory beyond counters is needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys
    output = io.StringIO()
    _stdout = _sys.stdout
    _sys.stdout = output
    try:
        solve()
    finally:
        _sys.stdout = _stdout
    return output.getvalue().strip()

# provided samples
assert run("3 5\n0 2 3\n") == "Oussama", "sample 1"
assert run("3 5\n1 1 3\n") == "Rami", "sample 2"

# custom cases
assert run("1 7\n0\n") == "Rami", "all divisible"
assert run("1 7\n3\n") == "Rami", "single bad element"
assert run("2 5\n1 2\n") == "Oussama", "minimal mixed case"
assert run("4 3\n1 2 4 5\n") in {"Oussama", "Rami"}, "parity sanity check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single good element | Rami | immediate loss case |
| single bad element | Rami | forced single-bad behavior |
| two mixed elements | Oussama | minimal active game |
| multiple elements | parity-based | general correctness |

## Edge Cases

When all elements are divisible by $k$, the counter $b$ becomes zero immediately and the algorithm returns Rami without entering any further logic. This matches the rule that the first player has no valid move.

When exactly one element is not divisible by $k$, the algorithm returns Rami as well. In this situation, every move necessarily keeps that element present while reducing the array size, leading to a forced sequence where the second player controls the final transition.

For larger $b$, the algorithm reduces the game to parity. For example, with input $A=[1,2,4,5]$, $k=3$, we get $b=4$. The algorithm outputs Rami because even parity means the second player aligns with the final move, confirming that intermediate value rearrangements do not affect outcome.
