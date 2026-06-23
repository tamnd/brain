---
title: "CF 105336K - \u53d6\u6c99\u5b50\u6e38\u620f"
description: "There is a pile of $n$ stones and two players who alternate turns, with Alice moving first. On each move a player removes some positive number of stones from the pile. The size of a move is restricted in two ways."
date: "2026-06-23T15:26:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105336
codeforces_index: "K"
codeforces_contest_name: "The 2024 CCPC Online Contest"
rating: 0
weight: 105336
solve_time_s: 66
verified: true
draft: false
---

[CF 105336K - \u53d6\u6c99\u5b50\u6e38\u620f](https://codeforces.com/problemset/problem/105336/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a pile of $n$ stones and two players who alternate turns, with Alice moving first. On each move a player removes some positive number of stones from the pile. The size of a move is restricted in two ways. It cannot exceed $k$, and it must be compatible with all previous moves in the sense that it has to divide every previously chosen move. On the very first move there is no divisibility restriction, so Alice only needs to choose a number between $1$ and $k$ and not exceeding the remaining stones.

The game ends when a player removes the last stones, and that player wins. Both players play optimally.

The input gives multiple independent games. Each test case specifies $n$ and $k$, and we must determine whether Alice has a forced win.

The constraints reach up to $10^9$ for both $n$ and $k$, with up to $10^4$ test cases, so any solution must be constant time per test case. Anything involving simulation of the game tree or iterating over possible moves is immediately infeasible.

A subtle edge case appears when $k = 1$. In that situation, every move is forced to be exactly 1 whenever legal, and the divisibility condition becomes irrelevant but still valid. Another delicate point is that after the first move, the divisibility constraint starts restricting moves heavily, but it does not eliminate the move “1” whenever $k \ge 1$, which completely changes the structure of the remaining game.

For example, if $n = 5, k = 1$, Alice is forced to take 1, and the game becomes a simple alternating removal of 1 stone. If $n = 4, k = 3$, Alice has multiple first moves, but after that the structure collapses into a highly constrained process. A naive assumption that the game depends only on gcd dynamics without noticing the constant availability of move 1 would lead to incorrect conclusions.

## Approaches

A direct simulation tries to model the game state as remaining stones together with the gcd of all previous moves. Each turn enumerates all valid divisors of that gcd that do not exceed $k$, and are not larger than the remaining pile. This correctly captures the rules, but the branching factor is still too large in principle, and the game tree grows quickly even though $n$ is large. The main issue is not just performance, but also that reasoning about optimal play over varying gcd states becomes complex.

The key simplification comes from observing that after the first move, the divisibility restriction does not meaningfully reduce choices in most cases, because the number 1 always remains valid. Since 1 divides every integer and is always within the limit $k$, the game after the first move degenerates into a forced subtraction process where both players can always take 1 until the pile is exhausted.

This turns the entire game into a first-move choice followed by a deterministic parity game. Alice’s decision reduces to choosing the first move $a_1$, after which the remaining game is a pure take-one game on $n - a_1$ stones starting from Bob.

Brute force tries all first moves and then simulates the remaining game. The optimized solution compresses the second phase into a parity check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation of game states | Exponential | O(1) | Too slow |
| First-move + parity reduction | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Handle the trivial winning move

If $n \le k$, Alice can take all stones in her first move because there is no divisibility restriction initially. She wins immediately.

### 2. Reduce the game after the first move

Assume Alice takes $a_1$, where $1 \le a_1 \le k$ and $a_1 \le n$. After this move, the remaining pile is $r = n - a_1$, and all future moves must divide $a_1$.

The crucial observation is that the value 1 is always a valid move because it divides every integer and always satisfies $1 \le k$.

### 3. Collapse the game to a take-one process

From this point on, both players can always take exactly 1 stone. Any other allowed moves do not affect optimal play because they are never necessary to maintain legality, and taking 1 is always available.

Thus the remainder of the game becomes a simple alternating process where each player removes 1 stone.

### 4. Determine the winner of the remaining game

In a take-one game, the player who faces an odd number of stones always wins under optimal play. Bob moves first in the remaining game, so Bob wins iff $r$ is odd.

Alice wants Bob to face an even number of stones, so she wants

$$n - a_1 \equiv 0 \pmod 2$$

which is equivalent to choosing $a_1$ with the same parity as $n$.

### 5. Check feasibility of choosing such a move

Alice can pick any $a_1 \le k$. So:

- If $n$ is odd, she needs an odd $a_1$, and 1 is always available, so she wins.
- If $n$ is even, she needs an even $a_1$. This is possible only if $k \ge 2$, since the smallest even move is 2.

### Why it works

The invariant is that after the first move, the set of legal moves always includes 1, and 1 is sufficient to simulate optimal play in the remaining game. The rest of the move set cannot improve either player’s outcome because any deviation from repeatedly taking 1 does not change parity-based inevitability of the terminal state. The game therefore reduces to controlling the parity of the remaining pile after the first move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())

        if n <= k:
            out.append("Alice")
            continue

        if n % 2 == 1:
            out.append("Alice")
        else:
            if k >= 2:
                out.append("Alice")
            else:
                out.append("Bob")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the reduction. The first condition handles immediate termination when Alice can take everything. The second branch encodes the parity condition derived from the forced “take 1” phase. No simulation of divisors or gcd states is required, since the move 1 dominates all future possibilities.

## Worked Examples

### Example 1: $n = 5, k = 3$

Alice cannot finish the game immediately, so she chooses a first move. The optimal decision is based on parity.

| Step | Player | Move | Remaining $n$ |
| --- | --- | --- | --- |
| 1 | Alice | 1 | 4 |
| 2 | Bob | 1 | 3 |
| 3 | Alice | 1 | 2 |
| 4 | Bob | 1 | 1 |
| 5 | Alice | 1 | 0 |

Alice wins because she chooses a move leaving an even number of stones, and Bob is forced into losing parity.

This demonstrates that once the first move is fixed, the rest of the game is a forced alternating chain.

### Example 2: $n = 6, k = 1$

Alice has no choice for the first move.

| Step | Player | Move | Remaining $n$ |
| --- | --- | --- | --- |
| 1 | Alice | 1 | 5 |
| 2 | Bob | 1 | 4 |
| 3 | Alice | 1 | 3 |
| 4 | Bob | 1 | 2 |
| 5 | Alice | 1 | 1 |
| 6 | Bob | 1 | 0 |

Bob wins because the remaining pile after Alice’s forced move is odd.

This shows why even $n$ becomes losing when $k = 1$, since Alice cannot adjust parity with her first move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case is resolved by a constant number of arithmetic checks |
| Space | O(1) | Only a few variables are used per test case |

The solution easily fits within the limits since even $10^4$ cases require only simple integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        if n <= k:
            res.append("Alice")
        elif n % 2 == 1:
            res.append("Alice")
        elif k >= 2:
            res.append("Alice")
        else:
            res.append("Bob")
    return "\n".join(res)

# provided samples
assert run("3\n2 3\n4 3\n5 1\n") == "Alice\nAlice\nAlice"

# custom cases
assert run("1\n1 1\n") == "Alice", "minimum win"
assert run("1\n2 1\n") == "Bob", "even n, k=1 loss"
assert run("1\n10 1\n") == "Bob", "forced parity loss"
assert run("1\n10 5\n") == "Alice", "k>=2 allows parity fix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | Alice | immediate win when n ≤ k |
| 2 1 | Bob | forced loss under k = 1, even n |
| 10 1 | Bob | parity chain loses for even n |
| 10 5 | Alice | ability to choose even first move |

## Edge Cases

### Case: $n \le k$

Input:

```
n = 7, k = 10
```

Alice immediately takes all 7 stones and wins. The algorithm captures this directly in the first condition, preventing any unnecessary reasoning about parity or future moves.

### Case: $k = 1$

Input:

```
n = 6, k = 1
```

Alice is forced to take 1, leaving 5 stones. The remaining game is a strict alternation of taking 1. The algorithm classifies this as a losing position for Alice because $n$ is even and she cannot adjust parity.

### Case: large $k$, even $n$

Input:

```
n = 10, k = 100
```

Alice chooses an even first move such as 2, leaving 8 stones. The remainder becomes a losing parity for Bob, so Alice wins. The condition $k \ge 2$ correctly captures this flexibility.

### Case: large $n$, small $k$

Input:

```
n = 999999999, k = 1
```

Alice must take 1, and the parity of the remaining pile determines the winner. Since $n$ is odd, Alice wins even though $k$ is minimal, showing that parity dominates when move freedom disappears.
