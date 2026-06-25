---
title: "CF 105909K - UNO\uff01"
description: "We have a circular table with n players. Player i starts with a[i] cards. The game begins with player 1, and the initial direction is clockwise. A sequence of exactly m played cards is given."
date: "2026-06-25T14:08:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105909
codeforces_index: "K"
codeforces_contest_name: "The 9th Hebei Collegiate Programming Contest"
rating: 0
weight: 105909
solve_time_s: 62
verified: true
draft: false
---

[CF 105909K - UNO\uff01](https://codeforces.com/problemset/problem/105909/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular table with `n` players. Player `i` starts with `a[i]` cards. The game begins with player 1, and the initial direction is clockwise.

A sequence of exactly `m` played cards is given. Each character describes the card played on that turn:

`C` is a normal card and has no effect.

`S` skips the next player in the current direction.

`R` reverses the playing direction.

`D` gives the next player two additional cards and also skips that player.

Whenever a player plays a card, their hand size decreases by one. If their hand reaches zero immediately after playing, they leave the game at once and are removed from the circle.

The input guarantees that the play sequence is valid and that at least two players still have cards after the final play. We must output the final number of cards held by every original player.

The interesting part is that players disappear during the simulation. Once someone leaves, future turn order, skips, reverses, and draw-two effects must operate on the remaining circular list of active players.

The limits are up to `2 × 10^5` players and `2 × 10^5` played cards. A simulation that repeatedly scans the circle to find the next active player could degrade to quadratic time. With 200,000 operations, we need every turn to be processed in constant or logarithmic time.

A subtle edge case appears when a player leaves immediately after playing a special card.

For example:

```
3 players
cards = [1, 5, 5]
play = "S"
```

Player 1 plays `S`, their card count becomes zero, and they leave. The skipped player is still player 2, because "next player" is determined from player 1's position before they disappear. A careless implementation that removes player 1 first and then searches for the next player can target the wrong person.

Another tricky case is a reverse card played by a player who leaves.

```
3 players
cards = [1, 5, 5]
play = "R"
```

Player 1 leaves immediately after playing. The direction changes, and the next turn belongs to the player who was on player 1's opposite side in the new direction. If we try to continue from the removed player without preserving its neighbors, the simulation breaks.

A final source of bugs is combining removal with skipping.

```
3 players
cards = [1, 5, 5]
play = "D"
```

Player 1 gives player 2 two cards, player 2 loses its turn, player 1 leaves, and the next turn becomes player 3. The order of these updates matters.

## Approaches

The most direct simulation stores all active players in a circle and, after every card, walks through the players to find who acts next. This is correct because the game rules are local, every turn only affects nearby players in the current direction.

The problem is efficiency. A player may leave the game, which means we need to remove them from the circle. If we represent active players with a normal array or list, removing someone can cost `O(n)`. Doing that up to `m = 2 × 10^5` times leads to roughly `O(nm)` work, far beyond the limit.

The key observation is that the game only needs three operations on the active players:

1. Find the next active player.
2. Find the previous active player.
3. Remove a player from the circle.

These are exactly the operations supported by a circular doubly linked list in `O(1)` time.

We store for every player its current clockwise neighbor and counterclockwise neighbor. Removing a player becomes a standard linked-list splice. After that, all effects can be processed using only neighbor pointers.

Each played card then requires only a constant number of pointer updates and hand-count updates, giving linear total complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every player's card count in an array.
2. Build a circular doubly linked list using two arrays:

`nxt[i]` is the clockwise neighbor of player `i`,

`prv[i]` is the counterclockwise neighbor of player `i`.
3. Let `cur = 1`, because player 1 moves first.
4. Let `dir = 1` represent clockwise and `dir = -1` represent counterclockwise.
5. For each character in the play string:

1. Record the current player's two neighbors before any removal:

`left = prv[cur]`,

`right = nxt[cur]`.
2. If the card is `S` or `D`, determine the affected player:

`target = right` when `dir = 1`,

`target = left` when `dir = -1`.
3. If the card is `D`, add two cards to `target`.
4. Decrease `cards[cur]` by one because the card is played.
5. If `cards[cur]` becomes zero, remove `cur` from the linked list.
6. Handle the card effect.

For `C`, the next player is simply `target`.

For `S` and `D`, the next player is the player after `target` in the current direction.

For `R`, reverse the direction. The next player becomes the neighbor of the current position in the new direction.
6. Continue until all `m` cards have been processed.
7. Output the final card count of every player.

### Why it works

The linked list always represents exactly the players who still have cards. When a player's count reaches zero, they are removed immediately, matching the rules.

For every turn, the algorithm identifies affected players using the current circle and current direction before any future turn is chosen. This matches the game definition of "next player".

The invariant is that before processing each card, `cur` is exactly the player whose turn it is, and the linked list contains exactly the active players in correct circular order. Every update preserves this invariant, so after the final card the stored card counts are the true final hand sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))
s = input().strip()

nxt = [0] * n
prv = [0] * n

for i in range(n):
    nxt[i] = (i + 1) % n
    prv[i] = (i - 1 + n) % n

cur = 0
dirv = 1

for ch in s:
    left = prv[cur]
    right = nxt[cur]

    target = right if dirv == 1 else left

    if ch == 'D':
        a[target] += 2

    a[cur] -= 1

    dead = (a[cur] == 0)

    if dead:
        l = prv[cur]
        r = nxt[cur]
        nxt[l] = r
        prv[r] = l

    if ch == 'C':
        cur = target

    elif ch == 'S' or ch == 'D':
        if dirv == 1:
            cur = nxt[target]
        else:
            cur = prv[target]

    else:  # 'R'
        dirv *= -1

        if dirv == 1:
            cur = right
        else:
            cur = left

for x in a:
    print(x)
```

The arrays `nxt` and `prv` form a circular doubly linked list over the active players. Removing a player requires only reconnecting its two neighbors, which is constant time.

The variable `target` is computed before any removal. This is essential because skip and draw-two refer to the next player relative to the player who just acted, not relative to the circle after later updates.

For reverse cards, we store `left` and `right` before removal. If the current player leaves, we still know which player should act next after the direction change.

The card counts never exceed roughly `2 × 10^5 + 2m`, which easily fits inside Python integers.

## Worked Examples

### Example 1

Input:

```
3 6
3 2 3
SRDCCD
```

Trace:

| Turn | Current | Card | Direction | Cards After Turn |
| --- | --- | --- | --- | --- |
| 1 | 1 | S | CW | [2,2,3] |
| 2 | 3 | R | CCW | [2,2,2] |
| 3 | 2 | D | CCW | [4,1,2] |
| 4 | 3 | C | CCW | [4,1,1] |
| 5 | 2 | C | CCW | [4,0,1] |
| 6 | 1 | D | CCW | [3,0,3] |

Output:

```
3
0
3
```

This example demonstrates all three special mechanics: skipping, reversing, and giving extra cards.

### Example 2

Input:

```
4 3
1 2 2 2
RSC
```

Trace:

| Turn | Current | Card | Direction After Turn | Active Players |
| --- | --- | --- | --- | --- |
| 1 | 1 | R | CCW | 2,3,4 |
| 2 | 4 | S | CCW | 2,3 |
| 3 | 2 | C | CCW | 2,3 |

Final counts:

| Player | Cards |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |

This example exercises the case where a player leaves immediately after playing a reverse card.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Building the linked list is O(n), each played card is processed in O(1) |
| Space | O(n) | Card counts and linked-list arrays |

The limits allow up to 200,000 players and 200,000 played cards. A linear simulation easily fits within the time limit and uses only a few arrays of size `n`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    s = input().strip()

    nxt = [0] * n
    prv = [0] * n

    for i in range(n):
        nxt[i] = (i + 1) % n
        prv[i] = (i - 1 + n) % n

    cur = 0
    dirv = 1

    for ch in s:
        left = prv[cur]
        right = nxt[cur]

        target = right if dirv == 1 else left

        if ch == 'D':
            a[target] += 2

        a[cur] -= 1

        if a[cur] == 0:
            l = prv[cur]
            r = nxt[cur]
            nxt[l] = r
            prv[r] = l

        if ch == 'C':
            cur = target
        elif ch in "SD":
            cur = nxt[target] if dirv == 1 else prv[target]
        else:
            dirv *= -1
            cur = right if dirv == 1 else left

    return "\n".join(map(str, a)) + "\n"

# sample
assert run("3 6\n3 2 3\nSRDCCD\n") == "3\n0\n3\n"

# minimum style case
assert run("2 2\n1 2\nCC\n") == "0\n1\n"

# reverse with elimination
assert run("3 1\n1 5 5\nR\n") == "0\n5\n5\n"

# draw-two with elimination
assert run("3 1\n1 5 5\nD\n") == "0\n7\n5\n"

# all normal cards
assert run("4 4\n3 3 3 3\nCCCC\n") == "2\n2\n2\n2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 2 / CC` | `0 1` | Smallest active circle |
| `3 1 / 1 5 5 / R` | `0 5 5` | Reverse while current player leaves |
| `3 1 / 1 5 5 / D` | `0 7 5` | Draw-two and skip with elimination |
| `4 4 / 3 3 3 3 / CCCC` | `2 2 2 2` | Pure turn rotation |

## Edge Cases

Consider:

```
3 1
1 5 5
S
```

Player 1 plays a skip card and immediately reaches zero cards. The skipped player is still player 2, because player 2 was the next active player at the moment the card was played. The algorithm computes `target` before removal, so the correct player is skipped. Final counts become:

```
0
5
5
```

Now consider:

```
3 1
1 5 5
R
```

Player 1 leaves after playing reverse. The direction changes from clockwise to counterclockwise. The next player must be the former left neighbor of player 1. The algorithm stores `left` and `right` before removal, so it can correctly choose the next turn even after player 1 disappears.

Finally:

```
3 1
1 5 5
D
```

Player 1 gives player 2 two cards, skips player 2, then leaves. Player 3 becomes the next player. Because the algorithm applies the draw-two effect before removal and computes the skipped player directly from the current position, the result is exactly:

```
0
7
5
```

These cases are where most incorrect simulations fail, and they are handled naturally by the linked-list representation.
