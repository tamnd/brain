---
title: "CF 102279A - Amsopoly Simple Version"
description: "The board has (N+1) positions arranged in a circle. Position (0), corresponding to the first position in the statement, belongs to the government and can never cause a payment. The other (N) positions are properties that can be owned. There are three players, Seo, B21, and Lowie."
date: "2026-08-17T10:08:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "A"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 90
verified: true
draft: false
---

[CF 102279A - Amsopoly Simple Version](https://codeforces.com/problemset/problem/102279/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The board has (N+1) positions arranged in a circle. Position (0), corresponding to the first position in the statement, belongs to the government and can never cause a payment. The other (N) positions are properties that can be owned.

There are three players, Seo, B21, and Lowie. Every time a player moves, their displacement is fixed: Seo always moves (V_s), B21 always moves (V_b), and Lowie always moves (V_l). They move in that order repeatedly. When a player reaches an unowned property, they take it. Reaching their own property does nothing, while reaching another player's property immediately creates the event we are looking for.

The task is to find the number of dice rolls that have occurred when the first payment happens. If no payment happens during the allowed (10^9) moves of each player, the required output is (3\cdot10^9).

The bounds make a direct simulation of all (10^9) turns per player impossible. Even a very small constant amount of work per turn would require about three billion iterations. The board size, however, is only (N+1\le100001), which strongly suggests that the relevant behavior should repeat after a number of turns proportional to (N).

The first subtle case is reaching the government position. For example, with `3 1 1 1`, the board has four positions. Seo reaches property 1 on the first roll, B21 reaches the same property on the second roll, so the answer is `2`. A careless implementation that treats the starting position as an ordinary property would incorrectly report a payment.

Another boundary case is a movement equal to (N). For `3 3 3 3`, the board size is four, so every player moves three positions each turn. Seo claims position 3 on roll 1, and B21 reaches it on roll 2. The answer is `2`. Using modulo (N) instead of modulo (N+1) silently gives the wrong board geometry.

The order of moves also matters. For `3 1 2 3`, Seo claims position 1 on roll 1, B21 claims position 2 on roll 2, and Lowie claims position 3 on roll 3. On Seo's second move, he reaches position 2, which B21 already owns, so the answer is `4`. A simulation that processes a whole round before checking ownership would miss the fact that ownership changes immediately after each individual roll.

Finally, a game can repeat forever without a payment. The sample `29 6 10 15` is such a case, and the correct answer is `3000000000`. Stopping merely because every player has revisited some positions is not sufficient unless the repetition of the entire game state has been established.

## Approaches

The straightforward solution is to simulate the game exactly as it happens. Keep the current position of each player and an array storing which player owns each property. Process Seo, then B21, then Lowie, update the current position with modulo (N+1), and immediately inspect the destination. If it is empty, assign its owner. If it belongs to somebody else, return the current number of rolls.

This simulation is completely correct because it follows precisely the state transition described by the game. Its problem is the stopping condition. The statement allows (10^9) moves for each player, so the worst case would require (3\cdot10^9) simulated rolls, which is far beyond the one-second limit.

The key observation is that the board contains exactly (N+1) positions. Consider one player after (N+1) of their own moves. Their total displacement is

[
(N+1)V.
]

That is (V) complete laps around a board of size (N+1), so the player is exactly where they started. More importantly, because the movement amount is fixed, the sequence of positions reached during the next (N+1) moves is identical to the sequence from the previous (N+1) moves. This is the central periodicity observation used by the official editorial.

After (N+1) moves by every player, all three players are back at their initial positions. The order of their moves is also back at the beginning of a round, and every property that could have been claimed during that block has been encountered in exactly the same way in the next block. If no payment happened during these first (3(N+1)) rolls, the next block is an exact repetition, so a payment can never happen later.

Since (N\le100000), (3(N+1)\le300003). We can therefore replace a potentially three-billion-step simulation with at most about three hundred thousand steps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9)) rolls | (O(N)) | Too slow |
| Optimal | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Let `m = N + 1`, because the complete circular board contains the government position plus the (N) properties. Store every position using indices from `0` through `m-1`, where `0` is the government position.
2. Create an ownership array of length `m`. Initially every entry is zero, meaning unowned. The entry at position `0` is never claimed because it belongs to the government.
3. Keep three current positions, initially all equal to zero. Also keep the three fixed movement values (V_s,V_b,V_l).
4. Simulate at most `m` complete rounds. In each round, process the three players in the exact order Seo, B21, Lowie. A player advances by their fixed movement value using modulo `m`.
5. Increment the global roll counter immediately after each movement. This counter represents the number of dice rolls that have actually happened, so if the current destination belongs to another player, returning it gives exactly the requested answer.
6. If the destination is zero, ignore it because the government owns that position. If its owner is zero, assign the current player as its owner. If its owner is already the current player, nothing happens. If its owner is another player, return the current roll count because this is the first payment.
7. If all `3*m` possible rolls are processed without a payment, return `3000000000`. The state after these `m` moves per player is exactly the same as the initial state, so every future block would repeat the same transitions and cannot introduce a payment.

### Why it works

The invariant is that immediately before every simulated roll, the stored positions and ownership array exactly describe the real game after the same number of rolls. Each movement uses the correct fixed displacement and modulo (N+1), and ownership is updated immediately after the destination is reached. Thus the first time the algorithm sees another player's owner is exactly the first payment in the real game.

If no payment appears during (N+1) moves of each player, all three positions return to zero because each player has moved through an integer number of complete board laps. The same fixed movement values and the same turn order then reproduce the same sequence of destinations. Since the ownership state has also been produced by that same sequence without a conflict, the future game repeats indefinitely. Hence returning `3000000000` is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, vs, vb, vl = map(int, input().split())

    m = n + 1
    moves = (vs, vb, vl)

    # owner[pos] = 0 if the property is unowned,
    # otherwise 1, 2, or 3 for the corresponding player.
    owner = [0] * m

    # All players start at the government position.
    pos = [0, 0, 0]

    rolls = 0

    # After m moves by each player, the whole game state repeats.
    for _ in range(m):
        for player in range(3):
            pos[player] = (pos[player] + moves[player]) % m
            rolls += 1

            p = pos[player]

            # Position 0 belongs to the government.
            if p == 0:
                continue

            if owner[p] == 0:
                owner[p] = player + 1
            elif owner[p] != player + 1:
                print(rolls)
                return

    print(3000000000)

if __name__ == "__main__":
    solve()
```

The first part converts the input into a board size of `n + 1`. This is the most important indexing choice in the implementation. The government position is represented by zero, while the (N) properties occupy positions `1` through `n`.

The `owner` array stores the current owner of every property. There is no need to store anything special for the government position because the `p == 0` check skips it before the ownership array is consulted.

The outer loop runs exactly `m` times. During each iteration, every player gets one turn, so the simulation covers exactly (N+1) turns for each player, or (3(N+1)) rolls in total.

The inner loop uses `player` values `0`, `1`, and `2`, corresponding to Seo, B21, and Lowie. The owner stored in the array is `player + 1`, which lets zero remain the special value for an unowned property.

The position update uses `(pos[player] + moves[player]) % m`. The modulo must be `N+1`, not `N`, because there are (N+1) positions on the circular board.

The roll counter is incremented before checking the destination. If a payment occurs on that move, the requested answer includes the roll that caused the payment, so the current value of `rolls` is exactly the answer.

Python integers have arbitrary precision, so the required sentinel value `3000000000` needs no special integer type. The actual simulation performs at most `300003` rolls, so both time and memory usage are comfortably within the limits.

## Worked Examples

### Sample 1

For `7 3 4 5`, the board has `8` positions, numbered `0` through `7`. The players move by 3, 4, and 5 respectively.

| Roll | Player | Position | Owner after move | Result |
| --- | --- | --- | --- | --- |
| 1 | Seo | 3 | 3 = Seo | Claims 3 |
| 2 | B21 | 4 | 4 = B21 | Claims 4 |
| 3 | Lowie | 5 | 5 = Lowie | Claims 5 |
| 4 | Seo | 6 | 6 = Seo | Claims 6 |
| 5 | B21 | 0 | unchanged | Government |
| 6 | Lowie | 2 | 2 = Lowie | Claims 2 |
| 7 | Seo | 1 | 1 = Seo | Claims 1 |
| 8 | B21 | 4 | unchanged | Own property |
| 9 | Lowie | 7 | 7 = Lowie | Claims 7 |
| 10 | Seo | 4 | 4 = B21 | Payment |

The tenth roll is Seo's fourth move. He reaches position 4, which B21 claimed on roll 2, so the answer is `10`. This also demonstrates why ownership must be checked after every individual roll rather than after an entire three-player round.

### Sample 2

For `29 6 10 15`, the board has `30` positions. Each player returns to position zero after 30 of their own moves because their total displacement is a multiple of 30.

| Player | Movement | Positions reached modulo 30 |
| --- | --- | --- |
| Seo | 6 | 6, 12, 18, 24, 0, ... |
| B21 | 10 | 10, 20, 0, 10, 20, ... |
| Lowie | 15 | 15, 0, 15, 0, ... |

The nonzero positions visited by these three sequences are disjoint. Consequently, none of the players ever reaches a property owned by another player. After 30 moves by each player, all three return to zero and the ownership pattern repeats, so no later block can create a payment.

The algorithm therefore completes all `3 * 30 = 90` simulated rolls and outputs `3000000000`. The simulation does not need to represent the billion allowed turns because the 30-move cycle has already proved that the game will repeat forever.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | At most (3(N+1)) player moves are simulated. |
| Space | (O(N)) | The ownership array contains (N+1) entries. |

With (N\le100000), the algorithm performs at most `300003` rolls. Each roll uses only a constant amount of work, so the total running time is easily suitable for the one-second limit. The ownership array uses linear memory, with only about one hundred thousand entries.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n, vs, vb, vl = map(int, sys.stdin.readline().split())

        m = n + 1
        moves = (vs, vb, vl)
        owner = [0] * m
        pos = [0, 0, 0]
        rolls = 0

        for _ in range(m):
            for player in range(3):
                pos[player] = (pos[player] + moves[player]) % m
                rolls += 1

                p = pos[player]

                if p == 0:
                    continue

                if owner[p] == 0:
                    owner[p] = player + 1
                elif owner[p] != player + 1:
                    print(rolls)
                    return sys.stdout.getvalue().strip()

        print(3000000000)
        return sys.stdout.getvalue().strip()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1.
assert solve_data("7 3 4 5\n") == "10", "sample 1"

# Provided sample 2.
assert solve_data("29 6 10 15\n") == "3000000000", "sample 2"

# Minimum N, equal movements. Seo claims position 1,
# then B21 immediately reaches it.
assert solve_data("3 1 1 1\n") == "2", "minimum size and equal values"

# Minimum N, movement equal to N.
# The board has 4 positions, so all players first reach position 3.
assert solve_data("3 3 3 3\n") == "2", "boundary movement N"

# The collision happens only after the first three rolls.
assert solve_data("3 1 2 3\n") == "4", "turn-order and off-by-one case"

# Maximum N with maximum movement. The same property is reached
# by Seo and B21 on their first moves.
assert solve_data("100000 100000 100000 100000\n") == "2", "maximum N"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 3 4 5` | `10` | Provided sample and immediate per-roll ownership checks |
| `29 6 10 15` | `3000000000` | Periodicity and the no-payment case |
| `3 1 1 1` | `2` | Minimum board size and equal movements |
| `3 3 3 3` | `2` | Correct modulo (N+1) and maximum movement |
| `3 1 2 3` | `4` | Exact player order and roll counting |
| `100000 100000 100000 100000` | `2` | Maximum (N) and maximum movement values |

## Edge Cases

For `3 1 1 1`, the board size is four. Seo moves from position 0 to position 1 and claims it. B21 then moves from position 0 to position 1 and finds Seo's ownership, so the second roll is the first payment. The algorithm returns `2`, while correctly treating position zero as the government position.

For `3 3 3 3`, the modulo base is four rather than three. Seo moves from zero to position three and claims it. B21 also moves to position three and immediately pays Seo, producing `2`. This case catches implementations that mistakenly use `n` as the circular board length.

For `3 1 2 3`, the first three rolls produce three distinct properties: Seo owns position 1, B21 owns position 2, and Lowie owns position 3. Seo's second move reaches position 2, so the payment happens on roll 4. The ownership array is updated after every move, which preserves the exact chronological order required by the game.

For `29 6 10 15`, all three players repeatedly visit only positions that are not visited by the others. After 30 moves by each player, all positions and ownership transitions enter the same cycle again. The algorithm detects no payment in those `90` rolls and returns `3000000000`, rather than trying to simulate the remaining billion turns per player.
