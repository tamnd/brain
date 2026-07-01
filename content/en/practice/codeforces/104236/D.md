---
title: "CF 104236D - J IDs"
description: "We are given a rectangular grid, and two players are placed on two different cells. The grid has no obstacles, so movement is always possible in the four cardinal directions."
date: "2026-07-01T23:26:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104236
codeforces_index: "D"
codeforces_contest_name: "Harker Programming Invitational 2023 Advanced"
rating: 0
weight: 104236
solve_time_s: 82
verified: true
draft: false
---

[CF 104236D - J IDs](https://codeforces.com/problemset/problem/104236/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid, and two players are placed on two different cells. The grid has no obstacles, so movement is always possible in the four cardinal directions. The players take turns moving one step at a time, and on each move a player must move to an adjacent cell. The game ends immediately when a player moves onto the cell currently occupied by the other player, and that moving player wins.

The key aspect is that both players play optimally, and the only objective is to force a win or avoid losing, depending on whose turn it is. We are asked to determine the winner given the initial positions and which player moves first.

The constraints allow the grid to be as large as 2000 by 2000, which means any solution that tries to simulate all possible states of the game graph is too slow. A naive state search would treat each pair of positions as a state, giving up to about 4 billion states in the worst case, which is far beyond feasible limits in both time and memory. This immediately suggests that the solution must collapse the state space into a much simpler invariant, most likely based on distances.

A subtle edge case arises when the players are very close. For example, if they are adjacent, the first player can win immediately. Another edge case is when they are separated by a path of length 2, where turn order determines whether the first player reaches the opponent or gets intercepted first. These cases hint that parity of distance and turn order will matter more than the exact path structure.

## Approaches

A brute-force approach would model the game as a state graph where each state consists of the positions of both players and whose turn it is. From each state, we would try all four moves for the active player and recursively evaluate whether it leads to a win. This is a typical minimax game on a huge implicit graph. While conceptually correct, the number of states is on the order of $R^2 C^2$, since each player independently occupies a cell, and each transition branches in up to four directions. Even with memoization, the number of reachable configurations remains far too large for a 1 second limit.

The key observation is that both players are symmetric in movement power and are trying to minimize the Manhattan distance between them. On an empty grid, the shortest path between two cells is exactly their Manhattan distance. If both players play optimally, they will always move along some shortest path toward each other, because any deviation only delays the meeting and worsens their position.

This reduces the game to a single quantity: the Manhattan distance between the players. Each move reduces this distance by exactly 1, because the moving player can always step closer to the opponent. The game ends when the distance reaches 0 on a player's turn, meaning that player has just stepped into the opponent's cell.

So instead of tracking positions, we only track how many moves are needed to eliminate the distance, and which player gets the final move. This converts a complex game state problem into a parity problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Graph | Exponential | Exponential | Too slow |
| Manhattan Distance + Parity | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the Manhattan distance between the two players using the formula $D = |r_s - r_c| + |c_s - c_c|$. This represents the minimum number of moves required for one player to reach the other in an empty grid.
2. Observe that every move by either player reduces this distance by exactly 1 under optimal play. This is because each player always moves closer to the opponent, and there are no obstacles forcing detours.
3. Conclude that the game ends exactly on move number $D$, since after $D$ total moves the distance becomes zero and the last mover has stepped onto the opponent’s cell.
4. Determine which player makes move number $D$. If the first player is Sam, then Sam moves on turns 1, 3, 5, and so on. If Clyde moves first, then Clyde occupies the odd turns instead.
5. Compare the parity of $D$ with the identity of the first mover. If $D$ is odd, the first mover makes the final move; if $D$ is even, the second mover makes it.

### Why it works

The invariant is that optimal play forces both players to always reduce the Manhattan distance by exactly one per move. There is no benefit in delaying or taking longer paths because the opponent can mirror optimal movement. This turns the game into a deterministic countdown from $D$ to zero, where the only remaining degree of freedom is which player gets the last decrement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, C = map(int, input().split())
    rs, cs, rc, cc = map(int, input().split())
    first = input().strip()

    dist = abs(rs - rc) + abs(cs - cc)

    if first == 'S':
        # Sam moves on odd turns
        if dist % 2 == 1:
            print("S")
        else:
            print("C")
    else:
        # Clyde moves on odd turns
        if dist % 2 == 1:
            print("C")
        else:
            print("S")

if __name__ == "__main__":
    solve()
```

The implementation reduces the entire grid game into computing a single Manhattan distance and checking parity. The only subtle part is correctly aligning parity with the identity of the first mover. A common mistake is to assume the first player always corresponds to the same parity without adjusting for whether it is Sam or Clyde. The code explicitly branches on the starting character to maintain that alignment.

## Worked Examples

### Example 1

Input:

```
7 8
1 3 5 4
C
```

Manhattan distance is $|1-5| + |3-4| = 4 + 1 = 5$.

| Step | Move | Remaining Distance | Player |
| --- | --- | --- | --- |
| 1 | C | 4 | C |
| 2 | S | 3 | S |
| 3 | C | 2 | C |
| 4 | S | 1 | S |
| 5 | C | 0 | C wins |

C moves first and also moves on all odd turns. Since the distance is 5, the 5th move is made by C, so C wins.

### Example 2

Input:

```
3 3
1 1 3 3
S
```

Distance is $|1-3| + |1-3| = 4$.

| Step | Move | Remaining Distance | Player |
| --- | --- | --- | --- |
| 1 | S | 3 | S |
| 2 | C | 2 | C |
| 3 | S | 1 | S |
| 4 | C | 0 | C wins |

Since distance is even and Sam moves first, Clyde gets the last move.

These traces show that the entire game reduces cleanly into a countdown where only parity determines the winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and input parsing are performed |
| Space | O(1) | No additional data structures beyond variables |

The solution easily fits within constraints since it performs constant work regardless of grid size, even when $R$ and $C$ are at their maximum values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""7 8
1 3 5 4
C
""") == "C"

# adjacent cells, immediate win
assert run("""2 2
1 1 1 2
S
""") == "S"

# symmetric center
assert run("""3 3
1 1 3 3
S
""") == "C"

# even distance, second player advantage
assert run("""4 4
1 1 2 2
C
""") == "S"

# large grid
assert run("""2000 2000
1 1 2000 2000
S
""") == "S"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Adjacent cells | S | immediate winning move handling |
| 3x3 diagonal | C | even distance parity |
| 4x4 close positions | S | correct role swap when C starts |
| max distance grid | S | performance and parity stability |

## Edge Cases

When the players start adjacent, the Manhattan distance is 1. The first player always wins immediately because they can move directly onto the opponent’s cell. The algorithm computes $D = 1$, and since 1 is odd, it assigns the win to the first mover, matching the actual gameplay.

When the distance is even, such as a 2-step separation, the second mover effectively gets the final move. For instance, if Sam starts and the distance is 2, Sam moves first reducing it to 1, then Clyde reduces it to 0 and wins. The parity rule correctly captures this without simulating turns.

When Clyde starts instead, the parity interpretation flips roles but the same invariant holds. The computation does not depend on grid size or shape, only on Manhattan distance and turn order alignment.
