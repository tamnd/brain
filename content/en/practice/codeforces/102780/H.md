---
title: "CF 102780H - Men's showdown"
description: "We have a pile containing N crayons. Two players alternate turns, and on each turn a player removes exactly 1, 5, or 13 crayons. The player who takes the last remaining crayon wins immediately."
date: "2026-07-27T20:14:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "H"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 60
verified: true
draft: false
---

[CF 102780H - Men's showdown](https://codeforces.com/problemset/problem/102780/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a pile containing N crayons. Two players alternate turns, and on each turn a player removes exactly 1, 5, or 13 crayons. The player who takes the last remaining crayon wins immediately. Both players know the current pile size and always choose moves that maximize their chance of winning. The task is to determine whether the first or second player has a winning strategy.

The input contains a single integer N, the initial number of crayons. The output is the number of the player who can force a win, where player 1 moves first and player 2 moves second.

The upper bound of N is 10000. This is small enough that a linear dynamic programming solution is easily possible. A solution that tries every possible game sequence would grow exponentially because each position can branch into up to three next positions. Even a quadratic approach is unnecessary because every pile size only depends on a few smaller pile sizes.

The tricky cases come from positions close to the end of the game. For example, when there is only one crayon:

```
1
```

The correct output is:

```
1
```

A player can remove the only crayon and win. A careless solution that only checks whether a player can take 5 or 13 crayons could incorrectly mark this as losing.

Another boundary case is:

```
2
```

The correct output is:

```
2
```

The first player must remove one crayon, leaving one for the opponent. The second player then takes the final crayon. A naive pattern based only on the move sizes might miss that small losing states are determined by previous states.

## Approaches

The direct approach is to simulate every possible game. For a given number of crayons, we can recursively try taking 1, 5, or 13 crayons and see whether any choice leads to a losing position for the opponent. This is correct because every possible move is considered, and a player wins exactly when they can move to a state where the other player cannot force a victory.

The problem with this method is the number of repeated states. For example, while analyzing a pile of size 10000, many different sequences of moves eventually reach the same smaller pile sizes. Without storing results, the recursion explores the same positions again and again. The number of possible move sequences is roughly exponential, making it far too slow.

The key observation is that only the current number of crayons matters. The history of moves has no effect on future possibilities. This means every pile size is a separate game state, and we only need to know whether that state is winning or losing.

We define a state as winning if the current player can make one move that leaves the opponent in a losing state. Otherwise, the state is losing. Starting from the smallest piles, we can compute all states up to N. This converts the recursive search into a simple dynamic programming process.

The brute-force method works because it explores every possible future, but it fails when the same pile sizes are reached through many different paths. The observation that game states depend only on the remaining number of crayons lets us solve every state once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^N) | O(N) recursion depth | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Create an array where the value at index i represents whether a pile containing i crayons is winning for the player whose turn it is. A true value means the current player can force a win, while a false value means every move eventually loses.
2. Set the state for zero crayons as losing. A player who starts their turn with no crayons cannot make a move, so this state is the base case.
3. For every pile size from 1 to N, check the three possible moves: removing 1, 5, or 13 crayons. If a move is possible and leaves a losing state for the opponent, mark the current state as winning.

The reason this works is that a player only needs one successful move. If they can leave the opponent with a losing position, optimal play guarantees that the opponent cannot avoid defeat.

1. After calculating the state for N crayons, output player 1 if the state is winning and player 2 otherwise.

Why it works:

The dynamic programming invariant is that after processing a pile size i, the stored value exactly describes the outcome of the game when i crayons remain. The base case is correct because zero crayons means the previous player already won. For every other state, the algorithm checks all legal moves. If any move reaches a losing state, the current player wins by choosing it. If no such move exists, every possible move gives the opponent a winning position, so the current state is losing. Since all smaller states are already known when a state is calculated, every decision is based on correct information.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    
    win = [False] * (n + 1)
    
    moves = [1, 5, 13]
    
    for i in range(1, n + 1):
        for move in moves:
            if i >= move and not win[i - move]:
                win[i] = True
                break
    
    print(1 if win[n] else 2)

if __name__ == "__main__":
    solve()
```

The array `win` stores the game result for every pile size from zero to N. It starts with all values set to losing because a state only becomes winning after finding a valid move that reaches a losing state.

The loop processes states in increasing order. When calculating `win[i]`, every state `win[i - move]` already has a final value because the remaining pile after a move is always smaller than i.

The `break` statement stops checking moves once a winning move is found. There is no need to search further because one winning option is enough. The boundary check `i >= move` prevents accessing invalid negative indices.

Python integers are large enough for this problem, and the maximum array size is only 10001 elements, so memory usage is minimal.

## Worked Examples

Consider the input:

```
1
```

The trace is:

| Current pile size | Move checked | Previous state | win value |
| --- | --- | --- | --- |
| 1 | Remove 1 | win[0] = False | True |

The only move removes the last crayon and leaves the opponent with zero crayons. Since the opponent has no winning move, player 1 wins.

Now consider:

```
2
```

The trace is:

| Current pile size | Move checked | Previous state | win value |
| --- | --- | --- | --- |
| 1 | Remove 1 | win[0] = False | True |
| 2 | Remove 1 | win[1] = True | False |

For a pile of size two, removing one crayon gives the opponent a winning state. Removing five or thirteen crayons is impossible. Every move loses, so player 2 wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each pile size checks only three possible moves. |
| Space | O(N) | The array stores one boolean result per pile size. |

With N limited to 10000, the algorithm performs only a few tens of thousands of operations and easily fits within the given limits.

## Test Cases

```python
import sys
import io

def solve_input(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline())
    win = [False] * (n + 1)
    
    for i in range(1, n + 1):
        for move in (1, 5, 13):
            if i >= move and not win[i - move]:
                win[i] = True
                break
    
    ans = "1" if win[n] else "2"
    
    sys.stdin = old_stdin
    return ans

assert solve_input("1\n") == "1", "minimum case"
assert solve_input("2\n") == "2", "first losing position"
assert solve_input("5\n") == "1", "direct move of size five"
assert solve_input("13\n") == "1", "direct move of size thirteen"
assert solve_input("10000\n") in ("1", "2"), "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | The smallest possible pile can be taken immediately. |
| 2 | 2 | A losing state caused by giving the opponent the last move. |
| 5 | 1 | A winning state using a larger allowed move. |
| 13 | 1 | Correct handling of the largest move size. |
| 10000 | 1 or 2 | The solution handles the maximum constraint. |

## Edge Cases

For the one-crayon case:

```
1
```

The algorithm begins with `win[0] = False`. While processing `i = 1`, removing one crayon reaches `win[0]`, which is losing for the next player. The current state becomes winning, so the output is player 1.

For the two-crayon case:

```
2
```

The first player can only remove one crayon. This leaves one crayon, and `win[1]` is already known to be true. Since the only move gives the opponent a winning state, `win[2]` remains false and the output is player 2.

For a pile exactly matching one available move:

```
13
```

The state calculation eventually reaches `i = 13`. Removing thirteen crayons reaches `win[0]`, so the state is winning. The algorithm does not require special handling for the move sizes because they are naturally included in the transition checks.

For the maximum input:

```
10000
```

The algorithm still performs only 10000 state calculations, each with three possible transitions. The same invariant applies throughout the entire range, so the final result is computed without recursion depth issues or excessive computation.

```

```

You can adjust the editorial's depth, add game theory terminology, or make it closer to a Codeforces contest editorial style if needed.
