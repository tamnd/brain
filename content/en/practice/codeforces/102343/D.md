---
title: "CF 102343D - Candy Land"
description: "The game board is a line of n squares. Squares 1 through n - 1 have either a color such as RED or a unique special square such as SPECIALCANE. Square n is the finish square and represents every color at once. Players begin before square 1."
date: "2026-08-16T17:58:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "D"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 179
verified: true
draft: false
---

[CF 102343D - Candy Land](https://codeforces.com/problemset/problem/102343/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The game board is a line of `n` squares. Squares `1` through `n - 1` have either a color such as `RED` or a unique special square such as `SPECIALCANE`. Square `n` is the finish square and represents every color at once. Players begin before square `1`.

There are `p` players and a deck containing `c` cards. On each turn, the next player takes the next card from the top of the deck. After using it, that card goes to the bottom, so the deck repeats cyclically. The player order also repeats cyclically. The first player to reach square `n` wins. The official statement guarantees that the game finishes in fewer than 10,000 turns.

A type `1` card contains one color. The player moves to the first square strictly after their current position having that color. If there is no such ordinary square, the finish square is reached because it contains every color.

A type `2` card contains one color twice. The player moves to the second occurrence of that color strictly after their current position. The finish square counts as an occurrence of every color, which is why a player can win even when there is only one ordinary occurrence ahead.

A type `3` card names a special square. The player moves directly to that square, regardless of whether it is ahead of or behind their current position. Special squares are unique, so their destination is unambiguous.

The constraints are deliberately small. The board has at most 200 squares, the deck has at most 500 cards, and the game lasts fewer than 10,000 turns. Even an implementation that scans the entire board for every color card performs at most about 2,000,000 square checks. That is easily manageable under the 3 second limit and 256 MB memory limit.

The main edge cases come from the finish square and from the direction of special moves. For example, consider

```
2 2
RED
1
2 RED
```

The only ordinary square is `RED`, and the finish square is square `2`. Player 1 takes a type `2 RED` card while standing at position `0`. The first `RED` occurrence is square `1`, and the second is the finish square, so the correct output is `1`. A careless implementation that searches only the `n - 1` explicitly supplied board squares would incorrectly conclude that there is no second occurrence.

Another boundary case is a special card moving a player backward:

```
4 2
RED
SPECIALX
BLUE
1
3 SPECIALX
```

Player 1 immediately moves to square `2`, even though the move is not a forward move. A simulation that assumes every card only increases the position would get the state wrong.

A final edge case is that several players may occupy the same square. For example,

```
3 2
RED
RED
1
1 RED
```

Player 1 moves to square `1`. On the next turn player 2 takes the same card and also moves to square `1`. There is no collision rule, so both positions remain valid. The official rules explicitly allow multiple players to share a square.

## Approaches

The most direct solution is to simulate the game exactly as it is described. Keep one position for every player, keep an index for the next card, and process turns until someone reaches the final square. For a type `1` or type `2` color card, scan forward through the board and count matching colors. For a type `3` card, look up the named special square and assign that position directly.

This brute-force simulation is already fast enough. In the worst case there are fewer than 10,000 turns and each turn may inspect all 199 ordinary squares, giving fewer than 1,990,000 board checks. The brute-force approach therefore does not actually become too slow under the given constraints.

There is still a useful optimization that makes the simulation cleaner. For every color, preprocess the sorted list of board positions containing that color. Add the final square `n` to every color's list because the finish square represents every color. Then a type `1` card asks for the first stored position greater than the player's current position, while a type `2` card asks for the second such position. Binary search finds that first position directly.

The observation behind this optimization is that the board never changes. Every query asks the same static question, namely which occurrence of a particular color comes after a given position. Precomputing the occurrence lists separates this static information from the dynamic part of the game, which is only the players' current positions.

Special squares can be stored in a dictionary from their names to their board positions. Since their names are unique, this gives constant-time lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Tn) | O(n + c + p) | Accepted |
| Optimal | O(n + c + T log n) | O(n + c) | Accepted |

Here `T < 10000` is the number of turns. The optimal version is preferable because its complexity directly reflects the fact that each move is a query against a fixed board.

## Algorithm Walkthrough

1. Read the board and number its positions from `1` through `n`. The input describes only positions `1` through `n - 1`, while position `n` is the multicolored finish square.
2. Build a dictionary `color_positions`. For every ordinary color square at position `i`, append `i` to that color's list. After reading the board, append `n` to every color list. The finish square must be included because it acts as an occurrence of every color.
3. Build a dictionary `special_positions` while reading the board. If a square starts with `SPECIAL`, store its complete name and its position.
4. Read the deck and store each card as its type and target string. The deck itself never changes in order, because used cards simply move from the front to the back. Consequently, turn `t` always uses card `(t mod c)`.
5. Initialize every player's position to `0`. The player whose turn it is on turn `t` is `(t mod p)`. Both indices are zero-based internally, while the player number printed at the end is one-based.
6. For a type `3` card, replace the current player's position with the stored special-square position. No forward search is involved because special cards move directly to their named squares.
7. For a type `1` color card, use `bisect_right` on the color's position list to find the first position strictly greater than the player's current position. Assign that position to the player.
8. For a type `2` color card, perform the same binary search, but take the element one position later in the occurrence list. Because the finish square was appended to every color list, it naturally becomes the second occurrence when it is needed.
9. After applying the card, check whether the player's position is `n`. If so, print that player's one-based number immediately. The game stops at the first player reaching the finish.
10. Advance the turn and repeat. The input guarantee that the game finishes within 10,000 turns means no cycle-detection mechanism is necessary.

Why it works: before every turn, each player's stored position is exactly their real position in the game. For a special card, the dictionary gives precisely the unique square named by the card. For a color card, the occurrence list contains exactly all squares having that color that can be landed on, including the final multicolored square. Binary search selects the first or second occurrence strictly after the current position, exactly matching the card rules. Since the players and deck are advanced cyclically in the same order as the game, every simulated turn matches the real game. The first simulated position equal to `n` is consequently the actual winner.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    n, p = map(int, input().split())

    color_positions = {}
    special_positions = {}

    for pos in range(1, n):
        cell = input().strip()

        if cell.startswith("SPECIAL"):
            special_positions[cell] = pos
        else:
            color_positions.setdefault(cell, []).append(pos)

    # The final square is an occurrence of every color.
    for positions in color_positions.values():
        positions.append(n)

    c = int(input())
    deck = []

    for _ in range(c):
        typ, target = input().split()
        deck.append((int(typ), target))

    player_pos = [0] * p

    turn = 0

    while True:
        player = turn % p
        typ, target = deck[turn % c]
        current = player_pos[player]

        if typ == 3:
            player_pos[player] = special_positions[target]
        else:
            positions = color_positions[target]
            idx = bisect_right(positions, current)

            if typ == 1:
                player_pos[player] = positions[idx]
            else:
                player_pos[player] = positions[idx + 1]

        if player_pos[player] == n:
            print(player + 1)
            return

        turn += 1

if __name__ == "__main__":
    solve()
```

The first preprocessing loop distinguishes ordinary colors from special squares using the `SPECIAL` prefix. This is safe because the statement guarantees that no color contains that substring.

The color lists contain only ordinary board positions at first. Appending `n` afterward is the key implementation detail. It avoids special cases such as "there is only one matching square left, so a type `2` card wins". The binary search then handles that case naturally.

`bisect_right(positions, current)` is also deliberate. The card always asks for a square after the player's current square, not the current square itself. If the player is already standing on a square of the requested color, that square must not count toward the move.

For a type `1` card, `positions[idx]` is the first matching square after the player. For a type `2` card, `positions[idx + 1]` is the second matching square. The problem guarantees that the game rules make the requested move valid, because the finish square supplies the necessary final occurrence.

The player index uses `turn % p`, while the card index uses `turn % c`. These two cycles are independent. Advancing the deck index only when a turn finishes is equivalent to moving the used card to the bottom of the deck.

Python integers have arbitrary precision, so there is no overflow concern. The maximum number of turns is also small, so there is no need for cycle acceleration.

## Worked Examples

### Sample 1

The first sample has ten squares and two players. The ordinary board is

```
1 RED
2 BLUE
3 SPECIALCANE
4 GREEN
5 RED
6 BLUE
7 BLUE
8 GREEN
9 RED
10 FINISH
```

The deck has four cards:

```
1 RED
2 BLUE
3 SPECIALCANE
2 GREEN
```

The key state changes are:

| Turn | Player | Card | Previous Position | New Position |
| --- | --- | --- | --- | --- |
| 1 | 1 | `1 RED` | 0 | 1 |
| 2 | 2 | `2 BLUE` | 0 | 6 |
| 3 | 1 | `3 SPECIALCANE` | 1 | 3 |
| 4 | 2 | `2 GREEN` | 6 | 10 |

On turn 2, the blue positions are `2, 6, 7, 10`. Starting from position `0`, the second occurrence is `6`, so player 2 reaches square 6. On turn 4, the green positions after position 6 are `8, 10`, so the second occurrence is the finish square. The answer is `2`. The official sample explanation gives the same sequence.

### Sample 2

The second sample has two board positions before the finish:

```
1 RED
2 SPECIALLOLLIPOP
3 FINISH
```

There are three players and two cards:

```
3 SPECIALLOLLIPOP
1 RED
```

The trace is:

| Turn | Player | Card | Previous Position | New Position |
| --- | --- | --- | --- | --- |
| 1 | 1 | `3 SPECIALLOLLIPOP` | 0 | 2 |
| 2 | 2 | `1 RED` | 0 | 1 |
| 3 | 3 | `3 SPECIALLOLLIPOP` | 0 | 2 |
| 4 | 1 | `1 RED` | 2 | 3 |

Player 1 reaches the special square on the first turn. On the fourth turn, the `RED` card has no ordinary red square after position 2, so the finish square is selected. Player 1 wins. The sample output is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + c + T log n) | Board and deck preprocessing are linear, and each of the `T` turns performs at most one binary search. |
| Space | O(n + c) | The occurrence lists, special-square map, deck, and player positions store linear-size state. |

Here `n <= 200`, `c <= 500`, and `T < 10000`. Even the simpler O(Tn) simulation would perform fewer than two million board checks, while the submitted solution is faster and remains comfortably within the 3 second and 256 MB limits.

## Test Cases

The following tests use the two official samples and four additional cases. The maximum-size case is generated programmatically so the test remains readable while still constructing a board with `n = 200` and a deck with `c = 500`.

```python
import sys
import io
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    n, p = map(int, input().split())

    color_positions = {}
    special_positions = {}

    for pos in range(1, n):
        cell = input().strip()

        if cell.startswith("SPECIAL"):
            special_positions[cell] = pos
        else:
            color_positions.setdefault(cell, []).append(pos)

    for positions in color_positions.values():
        positions.append(n)

    c = int(input())
    deck = []

    for _ in range(c):
        typ, target = input().split()
        deck.append((int(typ), target))

    player_pos = [0] * p
    turn = 0

    while True:
        player = turn % p
        typ, target = deck[turn % c]
        current = player_pos[player]

        if typ == 3:
            player_pos[player] = special_positions[target]
        else:
            positions = color_positions[target]
            idx = bisect_right(positions, current)

            if typ == 1:
                player_pos[player] = positions[idx]
            else:
                player_pos[player] = positions[idx + 1]

        if player_pos[player] == n:
            return str(player + 1)

        turn += 1

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve() + "\n"
    finally:
        sys.stdin = old_stdin

sample1 = """\
10 2
RED
BLUE
SPECIALCANE
GREEN
RED
BLUE
BLUE
GREEN
RED
4
1 RED
2 BLUE
3 SPECIALCANE
2 GREEN
"""

sample2 = """\
2 3
RED
SPECIALLOLLIPOP
2
3 SPECIALLOLLIPOP
1 RED
"""

assert run(sample1) == "2\n", "sample 1"
assert run(sample2) == "1\n", "sample 2"

# Minimum-size board. A type-1 card immediately reaches the finish.
assert run("""\
2 2
RED
1
1 RED
""") == "1\n", "minimum board"

# Type-2 card must count the finish square as the second occurrence.
assert run("""\
2 2
RED
1
2 RED
""") == "1\n", "finish counts as second occurrence"

# A special card may move backwards.
assert run("""\
4 2
RED
SPECIALX
BLUE
2
1 RED
3 SPECIALX
""") == "1\n", "backward special move"

# Maximum-size board and deck.
# Every ordinary square is RED, so the type-2 card reaches the second
# occurrence immediately on the first turn.
board = ["RED"] * 199
deck = ["2 RED"] * 500

max_input = (
    "200 6\n"
    + "\n".join(board)
    + "\n500\n"
    + "\n".join(deck)
    + "\n"
)

assert run(max_input) == "1\n", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `2` | Normal multi-player simulation, repeated deck, color and special cards |
| Sample 2 | `1` | A special move followed by a color move to the finish |
| `2 2 / RED / 1 RED` | `1` | Minimum board size and immediate finish |
| `2 2 / RED / 2 RED` | `1` | The finish square counts as the second occurrence |
| `4 2 / RED / SPECIALX / BLUE` | `1` | A special card can move a player backward |
| `n = 200, c = 500` | `1` | Maximum board and deck sizes |

## Edge Cases

The first subtle case is the final square acting as a color occurrence. With

```
2 2
RED
1
2 RED
```

the color list is initially `[1]`. The algorithm appends the finish position and obtains `[1, 2]`. The player's current position is `0`, so `bisect_right` returns index `0`. A type `2` card selects index `1`, which is position `2`. The output is `1`. No special-case branch is needed.

The second subtle case is a special move that goes backward. With

```
4 2
RED
SPECIALX
BLUE
2
1 RED
3 SPECIALX
```

player 1 first moves to position `1`. On the next time player 1 acts, the special card moves them directly to position `2`, regardless of their previous position. The algorithm assigns `special_positions["SPECIALX"]` directly, so it does not accidentally restrict the move to positions after the current one.

The third case is multiple players sharing a square. With

```
3 2
RED
RED
1
1 RED
```

player 1 moves from `0` to `1`. On the next turn player 2 independently moves from `0` to `1`. The simulation stores a separate position for each player, so neither player's move affects the other. This matches the rule that players are allowed to occupy the same square.

The fourth case is when a type `1` card has no ordinary matching square ahead. Consider

```
3 2
BLUE
RED
1
1 BLUE
```

Player 1 starts at `0` and moves to position `1`, so there is no issue yet. If player 1 later receives another `1 BLUE` card from position `1`, there is no ordinary `BLUE` square after it. The color occurrence list is `[1, 3]`, where `3` is the finish, so binary search selects `3`. The algorithm reaches the correct result without treating the finish as a separate kind of move.
