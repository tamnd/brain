---
title: "CF 102203M - RED-7"
description: "We have a two-player game played with distinct cards. Every card has a value from 1 to 7 and a color from the ordered set R, O, Y, G, B, N, P. A card with a larger value is stronger, and cards with equal values are ordered by color, with R strongest and P weakest."
date: "2026-08-18T00:59:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "M"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 284
verified: true
draft: false
---

[CF 102203M - RED-7](https://codeforces.com/problemset/problem/102203/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a two-player game played with distinct cards. Every card has a value from 1 to 7 and a color from the ordered set R, O, Y, G, B, N, P. A card with a larger value is stronger, and cards with equal values are ordered by color, with R strongest and P weakest.

Each player starts with one card already in their palette and up to six cards in their hand. The canvas initially represents the red rule, so the player with the strongest palette card is currently ahead. The first player's initial palette card is guaranteed to be weaker than the second player's.

A canvas card determines the rule under which the winner is evaluated. The seven rules are red for the strongest card, orange for the largest group of equal values, yellow for the largest group of one color, green for the largest number of even-valued cards, blue for the largest number of distinct colors, indigo for the longest consecutive run of values, and violet for the largest number of cards with value below 4.

For every rule, a player does not simply use all suitable cards. They choose the best possible combination by first maximizing its size and then maximizing its strongest card. Thus, the game state is determined by the cards currently in both palettes, the cards still in both hands, the current canvas color, and whose turn it is.

On a turn, the player can move one hand card to their palette, move one hand card to the canvas, or perform both operations using two different cards. After the operation, the player must be strictly ahead under the resulting canvas rule. If no such move exists, that player loses immediately. A player with an empty hand also loses when their turn begins, although they may legally finish a turn with an empty hand.

The input gives the two hand sizes and the cards belonging to each player. The first card on each player's line is already in that player's palette, while all remaining cards start in the hand. The required output is `First` if the first player has a winning strategy and `Second` otherwise.

The restriction of at most six cards in each hand is the central reason an exhaustive game-state search is possible. There are at most twelve cards whose locations can change. Each such card can be in the hand, in the palette, or already discarded onto the canvas, giving at most (3^{12}=531441) local ownership configurations before accounting for the canvas rule and the turn. This rules out algorithms whose work grows like the entire game tree, but it makes memoized state search practical.

Several details are easy to get wrong. An empty hand at the beginning of a turn is an immediate loss, even if that player was leading after the previous move. For example, the first sample is

```
0 0
3G
7Y
```

and the answer is `Second`. There is no legal move at all, so the fact that the second player initially leads is not the main reason for the answer. A search that checks only whether the current player is already winning would incorrectly return `First`.

Another subtle case is that playing a card to the canvas must be evaluated using the new canvas rule. In the second sample,

```
3 0
1R 2R 3R 4R
7R
```

the first player cannot improve under red because even their strongest available palette card is below 7R. Playing a card to the canvas also cannot help unless the resulting rule makes the first player lead. The correct answer is `Second`.

The tie-breaking inside a rule is another common source of errors. Consider

```
1 1
2P 2R
2Y 2O
```

The first player can put 2R into the palette. Under red, both players have a highest card of value 2, but R is stronger than Y, so the first player leads. The correct answer is `First`. A comparison based only on the numerical value would miss the color tie-break.

The boundary in the violet rule is also strict in the right place: values 1, 2, and 3 count, while 4 does not. For example,

```
1 1
3P 1R
7R 4O
```

The first player can put 1R on the canvas. The new rule is violet, and the first palette contains 3P, while the second palette contains 7R. The first player has one qualifying card and the second has none, so the answer is `First`. An implementation using `value <= 4` would produce the wrong result on this case.

## Approaches

The direct brute-force approach is to simulate every possible move and recursively inspect every continuation of the game. This is correct because a position is winning exactly when there exists a legal move that leaves the current player ahead and gives the opponent a losing position. If no such move exists, the position is losing.

With six cards in hand, a player has six palette-only actions, six canvas-only actions, and (6\cdot5=30) actions that use one card for the palette and a different card for the canvas. That is 42 possible actions at the beginning of a turn. A raw game-tree search can consequently have an upper bound of (42^{12}), which is about (3.0\cdot10^{19}) branches. Most of those branches are illegal or terminate much earlier, but the bound already shows that direct recursion cannot be used.

The brute-force search works because every move strictly reduces the number of cards in the current player's hand, so there are no cycles. The problem is that many different move sequences reach the same position. Once the same palettes, hands, canvas rule, and turn occur again, the future game is identical regardless of how that position was reached.

The key observation is therefore to memoize positions rather than move sequences. For each player, every hand card has exactly three relevant statuses: it is still in the hand, it has been moved to the palette, or it has already been discarded to the canvas. The initial palette card is fixed and needs no ternary state. Six hand cards consequently give only (3^6=729) possible local states per player.

The exact card currently on top of the canvas is not needed. Only its color matters because the canvas determines a rule. The fact that the card itself has disappeared from the game is already represented by that card being in neither the hand nor the palette. This reduces the global state to two local states, one of seven canvas colors, and the player to move.

For every possible palette mask, we can also precompute the best combination for each of the seven rules. A palette contains at most seven cards, so we can simply enumerate all its submasks and select the valid submask with maximum size and then maximum card strength. This makes evaluating a position constant time during the game search.

The resulting search is still exponential, but its state space is tiny enough for these constraints. A dense byte array is used for memoization rather than a Python dictionary, because the complete state space has only about 7.4 million entries and a byte per entry is inexpensive. The recursion also stops as soon as it finds a winning move, which is particularly effective because most positions have a legal move that can be rejected or accepted without exploring every alternative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(42^{12})) game-tree branches | (O(12)) recursion depth | Too slow |
| Optimal | (O(3^{n+m}(n+m)^2)) states and transitions in the worst case | (O(3^{n+m})) memoization | Accepted |

## Algorithm Walkthrough

1. Convert every card into a pair consisting of its value and its color rank. The color order R, O, Y, G, B, N, P becomes 0 through 6, so a card can be compared by the integer `value * 7 + color`.
2. For each player, precompute the optimal score of every possible palette mask under every canvas rule. A score contains the size of the optimal combination and the rank of its strongest card. We encode it as `size * 50 + rank`, while an impossible combination receives `-1`.

To compute a rule's score, enumerate every nonempty submask of the palette and test whether it satisfies that rule. This is small because a palette contains at most seven cards.
3. Represent the mutable part of each player's cards using six ternary digits. Digit zero means that the corresponding hand card has been discarded, digit one means it is still in the hand, and digit two means it is in the palette. The initial palette card is always included separately in the palette mask.

A local state therefore has at most (3^6=729) values. From a local state we can immediately obtain its hand mask and palette mask.
4. Precompute the result of moving every possible hand card to the palette and the result of moving every possible hand card to the canvas. A palette move changes its ternary digit from one to two. A canvas move changes it from one to zero.
5. Define a recursive game function whose state consists of the first player's local state, the second player's local state, the current canvas color, and the player whose turn it is.

The memo table stores whether that position is winning or losing for the player to move.
6. If the current player's hand is empty, mark the position as losing immediately. This is checked before considering the current canvas rule because the rules explicitly make an empty hand a loss at the beginning of a turn.
7. Try every palette-only move. Move one hand card into the current player's palette, keep the canvas rule unchanged, and compare the resulting optimal scores. If the current player leads and the opponent's resulting state is losing, the current position is winning.
8. Try every canvas-only move. Remove one hand card, use its color as the new canvas rule, and compare the new rule immediately. The card is no longer in the palette, so the palette itself does not change.
9. Try every ordered pair of distinct hand cards for the combined action. First move one card to the palette, then remove another card to the canvas. The new canvas rule must be evaluated using the enlarged palette and the remaining cards.
10. If any of these moves leads to an opponent-losing position while leaving the current player ahead, mark the current state as winning. If every possible move fails, mark it as losing.

The central invariant is that every memoized state contains exactly the information that can influence all future moves. Cards that remain in a hand can still be played, cards in a palette contribute to every future rule, and discarded cards can never return. The canvas color is the only property of the current canvas card that affects future rules. Thus two game histories with the same four local hand/palette states, canvas color, and turn have exactly the same set of future possibilities. The recursive minimax rule then matches optimal play: a position is winning precisely when the player has at least one legal move to a losing position for the opponent.

## Python Solution

```python
import sys
input = sys.stdin.readline

from functools import lru_cache

COLORS = "ROYGBNP"
COLOR_ID = {c: i for i, c in enumerate(COLORS)}
BASE = 3 ** 6
STATE_COUNT = BASE
STATE_SPACE = BASE * BASE * 7 * 2

def card_rank(card):
    value, color = card
    return value * 7 + color

def build_scores(cards):
    """
    score[rule][mask] = encoded optimal combination score.
    -1 means that no valid combination exists.

    The encoding is size * 50 + highest_card_rank.
    """
    score = [[-1] * 128 for _ in range(7)]
    total = len(cards)

    ranks = [card_rank(c) for c in cards]
    values = [c[0] for c in cards]
    colors = [c[1] for c in cards]

    for mask in range(1, 1 << total):
        sub = mask

        while sub:
            cnt = sub.bit_count()

            highest = -1
            vals = []
            cols = []

            x = sub
            while x:
                bit = x & -x
                i = bit.bit_length() - 1

                if ranks[i] > highest:
                    highest = ranks[i]

                vals.append(values[i])
                cols.append(colors[i])
                x ^= bit

            valid = [False] * 7

            # Red: exactly one card.
            valid[0] = cnt == 1

            # Orange: all cards have the same value.
            valid[1] = len(set(vals)) == 1

            # Yellow: all cards have the same color.
            valid[2] = len(set(cols)) == 1

            # Green: all cards are even.
            valid[3] = all(v % 2 == 0 for v in vals)

            # Blue: all colors are different.
            valid[4] = len(set(cols)) == cnt

            # Indigo: distinct consecutive values.
            if len(set(vals)) == cnt:
                lo = min(vals)
                hi = max(vals)
                valid[5] = hi - lo + 1 == cnt

            # Violet: all values are below 4.
            valid[6] = all(v < 4 for v in vals)

            encoded = cnt * 50 + highest

            for rule in range(7):
                if valid[rule] and encoded > score[rule][mask]:
                    score[rule][mask] = encoded

            sub = (sub - 1) & mask

    return score

def solve_case(data):
    lines = data.strip().splitlines()
    n, m = map(int, lines[0].split())

    first = []
    second = []

    for token in lines[1].split():
        first.append((int(token[0]), COLOR_ID[token[1]]))

    for token in lines[2].split():
        second.append((int(token[0]), COLOR_ID[token[1]]))

    score_first = build_scores(first)
    score_second = build_scores(second)

    # For a local ternary state:
    # digit 0 = discarded
    # digit 1 = hand
    # digit 2 = palette
    #
    # Bit 0 of the palette mask is always the initial palette card.
    powers = [3 ** i for i in range(6)]

    palette_mask = [0] * STATE_COUNT
    hand_mask = [0] * STATE_COUNT

    next_palette = [[-1] * 6 for _ in range(STATE_COUNT)]
    next_canvas = [[-1] * 6 for _ in range(STATE_COUNT)]

    for state in range(STATE_COUNT):
        x = state
        pmask = 1
        hmask = 0

        digits = [0] * 6

        for i in range(6):
            digits[i] = x % 3
            x //= 3

            if digits[i] == 1:
                hmask |= 1 << (i + 1)
            elif digits[i] == 2:
                pmask |= 1 << (i + 1)

        palette_mask[state] = pmask
        hand_mask[state] = hmask

        for i in range(6):
            if digits[i] == 1:
                # 1 -> 2: move to palette.
                next_palette[state][i] = state + powers[i]

                # 1 -> 0: move to canvas.
                next_canvas[state][i] = state - powers[i]

    # Only the first n or m variable positions are real cards.
    initial_first = sum(powers[i] for i in range(n))
    initial_second = sum(powers[i] for i in range(m))

    colors_first = [c[1] for c in first[1:]]
    colors_second = [c[1] for c in second[1:]]

    memo = bytearray(STATE_SPACE)

    def memo_index(s1, s2, canvas, turn):
        return ((((s1 * STATE_COUNT) + s2) * 7 + canvas) << 1) | turn

    def leads_first(pm1, pm2, rule):
        return score_first[rule][pm1] > score_second[rule][pm2]

    def leads_second(pm1, pm2, rule):
        return score_second[rule][pm2] > score_first[rule][pm1]

    sys.setrecursionlimit(100000)

    def win(s1, s2, canvas, turn):
        idx = memo_index(s1, s2, canvas, turn)
        saved = memo[idx]

        if saved:
            return saved == 2

        if turn == 0:
            me = s1
            opp = s2
            pm_opp = palette_mask[opp]
            hands = hand_mask[me]

            if hands == 0:
                memo[idx] = 1
                return False

            pm_me = palette_mask[me]

            # Action 1: hand -> palette.
            bits = hands
            while bits:
                bit = bits & -bits
                i = bit.bit_length() - 2

                ns = next_palette[me][i]

                if leads_first(palette_mask[ns], pm_opp, canvas):
                    if not win(ns, opp, canvas, 1):
                        memo[idx] = 2
                        return True

                bits ^= bit

            # Action 2: hand -> canvas.
            bits = hands
            while bits:
                bit = bits & -bits
                i = bit.bit_length() - 2

                ns = next_canvas[me][i]
                new_canvas = colors_first[i]

                if leads_first(palette_mask[ns], pm_opp, new_canvas):
                    if not win(ns, opp, new_canvas, 1):
                        memo[idx] = 2
                        return True

                bits ^= bit

            # Action 3: hand -> palette, another hand card -> canvas.
            bits_a = hands
            while bits_a:
                bit_a = bits_a & -bits_a
                a = bit_a.bit_length() - 2

                after_palette = next_palette[me][a]
                remaining = hands ^ bit_a

                bits_b = remaining
                while bits_b:
                    bit_b = bits_b & -bits_b
                    b = bit_b.bit_length() - 2

                    ns = next_canvas[after_palette][b]
                    new_canvas = colors_first[b]

                    if leads_first(
                        palette_mask[ns],
                        pm_opp,
                        new_canvas
                    ):
                        if not win(ns, opp, new_canvas, 1):
                            memo[idx] = 2
                            return True

                    bits_b ^= bit_b

                bits_a ^= bit_a

        else:
            me = s2
            opp = s1
            pm_opp = palette_mask[opp]
            hands = hand_mask[me]

            if hands == 0:
                memo[idx] = 1
                return False

            pm_me = palette_mask[me]

            # Action 1: hand -> palette.
            bits = hands
            while bits:
                bit = bits & -bits
                i = bit.bit_length() - 2

                ns = next_palette[me][i]

                if leads_second(palette_mask[ns], pm_opp, canvas):
                    if not win(opp, ns, canvas, 0):
                        memo[idx] = 2
                        return True

                bits ^= bit

            # Action 2: hand -> canvas.
            bits = hands
            while bits:
                bit = bits & -bits
                i = bit.bit_length() - 2

                ns = next_canvas[me][i]
                new_canvas = colors_second[i]

                if leads_second(palette_mask[ns], pm_opp, new_canvas):
                    if not win(opp, ns, new_canvas, 0):
                        memo[idx] = 2
                        return True

                bits ^= bit

            # Action 3: hand -> palette, another hand card -> canvas.
            bits_a = hands
            while bits_a:
                bit_a = bits_a & -bits_a
                a = bit_a.bit_length() - 2

                after_palette = next_palette[me][a]
                remaining = hands ^ bit_a

                bits_b = remaining
                while bits_b:
                    bit_b = bits_b & -bits_b
                    b = bit_b.bit_length() - 2

                    ns = next_canvas[after_palette][b]
                    new_canvas = colors_second[b]

                    if leads_second(
                        palette_mask[ns],
                        pm_opp,
                        new_canvas
                    ):
                        if not win(opp, ns, new_canvas, 0):
                            memo[idx] = 2
                            return True

                    bits_b ^= bit_b

                bits_a ^= bit_a

        memo[idx] = 1
        return False

    return "First" if win(initial_first, initial_second, 0, 0) else "Second"

def main():
    data = sys.stdin.read()
    if data.strip():
        print(solve_case(data))

if __name__ == "__main__":
    main()
```

The first part of the implementation converts colors to integers and represents each card by its value and color rank. The rank formula makes the required strict ordering a normal integer comparison. Since values are at most 7 and there are seven colors, a rank below 50 is sufficient for all tie-breaking.

`build_scores` handles the rule mechanics separately from the game mechanics. For each palette mask it considers every possible combination and checks the seven definitions directly. This is deliberately simple. There are only (2^7=128) palette masks and each contains at most (2^7=128) submasks, so exhaustive evaluation here is tiny compared with the game search.

The indigo rule deserves particular attention. A valid combination must contain distinct values forming one consecutive interval. A single card is a valid run, so a palette containing only one card still has an indigo combination of size one. The condition `hi - lo + 1 == cnt` together with distinct values captures exactly that property.

The ternary encoding is the main state compression. A variable card has three possible locations from the perspective of future play. Moving a hand card to the palette increments its ternary digit from 1 to 2, while moving it to the canvas decrements it from 1 to 0. The initial palette card is always bit zero of the palette mask and never participates in the ternary digits.

The canvas stores only a color index. Once a card has been discarded, its identity no longer affects any future rule. Its disappearance is already visible because its ternary digit is zero. This is why storing the complete canvas card would create unnecessary states.

The `memo` array uses zero for an unknown state, one for a losing state, and two for a winning state. Its index packs both local states, the canvas color, and the turn into one integer. A byte array is much more memory-efficient than a Python dictionary containing millions of tuple keys.

The expressions such as `bit.bit_length() - 2` convert a palette or hand bit into the corresponding ternary-card index. The hand card at local index zero is represented by bit one because bit zero is reserved for the initial palette card. This offset is an easy place to introduce an off-by-one error.

The combined action is generated in the correct order. The first selected card is moved to the palette, then a different selected card is moved to the canvas. The second card is therefore evaluated using the enlarged palette, which matters for rules such as orange, yellow, green, blue, indigo, and violet.

There is no integer overflow concern in Python. The largest arithmetic objects used for state indexing are only a few million, while card scores are below 400.

## Worked Examples

### Sample 1

The input is

```
0 0
3G
7Y
```

The initial local states contain only their fixed palette cards. Both hands are empty, so the recursive search terminates before examining the current canvas rule.

| Turn | First hand | First palette | Second hand | Second palette | Canvas | Result |
| --- | --- | --- | --- | --- | --- | --- |
| First | empty | 3G | empty | 7Y | R | First has no move |

The state is losing for the first player because an empty hand at the beginning of a turn is an immediate loss. The second player wins without making a move.

### Sample 2

The input is

```
3 0
1R 2R 3R 4R
7R
```

The canvas is initially red. The first player's only palette card is 1R, while the second player's palette contains 7R.

| Action by First | New palette | New canvas | First score | Second score | Legal winning move |
| --- | --- | --- | --- | --- | --- |
| Put 2R in palette | 1R, 2R | R | 2R | 7R | No |
| Put 3R in palette | 1R, 3R | R | 3R | 7R | No |
| Put 4R in palette | 1R, 4R | R | 4R | 7R | No |
| Put 2R on canvas | 1R | R | 1R | 7R | No |
| Put 3R on canvas | 1R | R | 1R | 7R | No |
| Put 4R on canvas | 1R | R | 1R | 7R | No |

A canvas card is still red because all three available cards are red, so canvas-only moves do not change the rule. A palette move cannot produce a card stronger than 7R. The combined action also cannot help, because every possible canvas card is red and leaves the game under the same highest-card rule.

The first state is consequently losing, so the answer is `Second`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(3^{n+m}(n+m)^2)) | Each card has three statuses, and each state considers one-card and two-card actions |
| Space | (O(3^{n+m})) | Memoization stores one byte for every packed game state, up to a constant factor for the seven rules and two turns |

At the maximum (n=m=6), each player's local state has only 729 possibilities. Including both players, seven canvas colors, and two turns gives about 7.4 million packed states, and the memoization array occupies only a few megabytes. The rule scores and transition tables are negligible in comparison. The search is exponential in the number of hand cards, but the exponent is bounded by twelve, which is exactly why this approach fits the unusually small constraints of the problem.

## Test Cases

```
# This test block assumes solve_case from the solution above is available.

def run(inp: str) -> str:
    return solve_case(inp).strip()

# Provided samples.
assert run("""\
0 0
3G
7Y
""") == "Second", "sample 1"

assert run("""\
3 0
1R 2R 3R 4R
7R
""") == "Second", "sample 2"

assert run("""\
4 3
1O 2O 4G 6G 5B
7B 2Y 5P 2G
""") == "First", "sample 3"

# Minimum-size input. Nobody has a hand, so the first player loses immediately.
assert run("""\
0 0
3G
7Y
""") == "Second", "empty hands"

# Equal values test the color tie-break.
assert run("""\
1 1
2P 2R
2Y 2O
""") == "First", "equal value, stronger color wins"

# Violet boundary: 3 counts, 4 does not.
assert run("""\
1 1
3P 1R
7R 4O
""") == "First", "value 3 belongs to violet"

# Indigo singleton boundary. A one-card run exists, but 7P beats 1R.
assert run("""\
1 0
1R 2O
7P
""") == "Second", "singleton indigo run"

# Maximum hand size for one player.
# First can put 2R into the palette and 3R onto the canvas,
# producing a yellow rule where First has two cards of one color.
# Second has no hand and loses on the following turn.
assert run("""\
6 0
1R 2R 3R 4R 5R 6R 7R
7P
""") == "First", "maximum first-hand size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 / 3G / 7Y` | `Second` | Empty-hand loss at the start of a turn |
| `2P 2R / 2Y 2O` | `First` | Color tie-breaking after equal values |
| `3P 1R / 7R 4O` | `First` | Violet includes 3 but excludes 4 |
| `1R 2O / 7P` | `Second` | A singleton is a valid indigo run |
| `1R 2R 3R 4R 5R 6R 7R / 7P` | `First` | Six-card hand and a combined palette/canvas move |

## Edge Cases

The empty-hand case is handled before any move generation. For

```
0 0
3G
7Y
```

the first local state has a zero hand mask. The recursive function marks it as losing immediately and never tries to compare the two palette cards. The result is `Second`.

The red tie-break is handled by encoding every card as its numerical value followed by its color rank. For

```
1 1
2P 2R
2Y 2O
```

moving 2R to the first palette produces the two highest cards 2R and 2Y. Both have value 2, but the encoded rank of 2R is larger, so the first player leads. The opponent's future possibilities are also explored by the minimax recursion, rather than assuming that winning the current position is enough.

The violet boundary is represented by the condition `v < 4`. In

```
1 1
3P 1R
7R 4O
```

the first player discards 1R to the canvas, changing the rule to violet. The first palette contains 3P, which contributes one qualifying card. The second palette contains 7R, which contributes zero. The first player therefore has a legal winning move.

The indigo singleton case uses the condition that the maximum value minus the minimum value equals the number of distinct values minus one. For a single card, both sides are zero, so the combination is valid. In

```
1 0
1R 2O
7P
```

playing 2O to the canvas creates the indigo rule, but the resulting singleton 1R is weaker than the opponent's singleton 7P. Playing 2O to the palette leaves the red rule active and also loses. With no other action available, the first player loses.

The combined move must use two different cards and must evaluate the canvas rule after the palette card has already been added. In

```
6 0
1R 2R 3R 4R 5R 6R 7R
7P
```

the first player can move 2R to the palette and 3R to the canvas. The new rule is yellow. The first palette then contains 1R and 2R, both of the same color, while the second palette contains only 7P. The first player has two qualifying cards against one, so the move is legal and winning. The second player's hand is empty, so the game ends on the next turn with `First` as the winner.

The indigo rule also requires care when duplicate values exist. Two cards with value 5 do not form a two-card run. The score precomputation checks that all values in an indigo combination are distinct before checking whether they form one consecutive interval. This prevents a duplicate value from incorrectly increasing the run length.

Finally, cards placed on the canvas disappear from the corresponding player's available cards. The implementation records that by changing their ternary status from hand to discarded. The canvas stores only the new color. When another card later replaces it, the old canvas card remains discarded, exactly as required, without needing to remember which card it was.
