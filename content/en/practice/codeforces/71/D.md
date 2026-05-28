---
title: "CF 71D - Solitaire"
description: "We are given a rectangular board filled with playing cards. Every normal card is unique because the deck is standard: 13 ranks times 4 suits. Two special cards, J1 and J2, are jokers. A solved configuration must contain two different 3×3 subgrids that do not overlap."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 2200
weight: 71
solve_time_s: 131
verified: true
draft: false
---

[CF 71D - Solitaire](https://codeforces.com/problemset/problem/71/D)

**Rating:** 2200  
**Tags:** brute force, implementation  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular board filled with playing cards. Every normal card is unique because the deck is standard: 13 ranks times 4 suits. Two special cards, `J1` and `J2`, are jokers.

A solved configuration must contain two different 3×3 subgrids that do not overlap. Each chosen square must satisfy at least one of these conditions:

1. All 9 cards inside the square have the same suit.
2. All 9 cards inside the square have pairwise different ranks.

Jokers cannot remain on the board. Before checking the condition, we may replace every joker with any unused card from the remaining deck. Each replacement card must be distinct and must not already appear on the board.

The task is not only to decide whether such a configuration exists, but also to print one valid replacement assignment and the coordinates of the two 3×3 squares.

The constraints completely shape the solution. The board dimensions are at most 17×17, but the product `n * m` never exceeds 52 because at most 52 non-joker cards exist in the deck. That means the number of possible 3×3 squares is small:

$$(n-2)(m-2) \le 15 \cdot 15 = 225$$

This is tiny. We can afford to examine every possible square and every pair of squares. The only expensive part is joker replacement, but there are at most two jokers, so even brute force over possible replacement cards is manageable.

A subtle detail is that a square may satisfy both properties simultaneously. For example, nine cards of suit `S` can also have nine distinct ranks. The implementation should treat such a square as valid immediately.

Another easy mistake is forgetting that the two squares must not overlap by cells. Sharing even one cell is forbidden. Consider this example:

```
3 5
2S 3S 4S 5S 6S
7S 8S 9S TS JS
QS KS AS 2H 3H
```

The left 3×3 and right 3×3 both satisfy the same-suit condition, but they overlap in a 3×1 strip. The correct answer is still `No solution.`

Joker replacement also creates pitfalls. Suppose we have:

```
3 3
J1 2S 3S
4S 5S 6S
7S 8S 9S
```

A careless implementation might replace `J1` with `2H`, since only one cell is missing for nine distinct ranks. But the square already contains rank `2`, so the distinct-rank condition fails. The correct replacement is something like `AS`, which preserves same-suit.

The final subtlety is deck consistency. Replacement cards must come from cards not already used on the board. If `AS` already exists somewhere outside the target square, we cannot use another `AS` for a joker.

## Approaches

The most direct brute-force solution is to try every possible joker replacement and then test every pair of 3×3 squares.

There are at most two jokers. A full deck has 52 normal cards, so the number of replacement assignments is at most:

$$52 \cdot 51 = 2652$$

For each assignment, we enumerate every 3×3 square. There are at most 225 of them. Checking one square costs constant time because it always contains exactly 9 cards.

After collecting all valid squares, we test every pair for non-overlap. That is at most:

$$225^2 = 50625$$

So the total work is comfortably below a few hundred million primitive operations, even in Python.

The brute-force succeeds because the search space is naturally tiny. The constraints never allow large boards or many jokers.

The key observation is that we do not need any complicated pruning or dynamic programming. The problem looks combinatorial because of the card deck, but the actual branching factor is bounded by the two jokers. Once replacements are fixed, the rest becomes pure enumeration.

A tempting but unnecessary optimization is to reason locally about only squares containing jokers. That complicates the implementation because a replacement may affect multiple candidate squares at once. Since the total number of assignments is already tiny, full recomputation is simpler and safer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all placements and square pairs | O(52² · S²) | O(S) | Accepted |
| Optimized local reasoning | More complicated | More complicated | Unnecessary |

Here `S = (n-2)(m-2)` is the number of 3×3 squares.

## Algorithm Walkthrough

1. Parse the board and collect all used non-joker cards.

We need this so joker replacements only use cards still available in the deck.
2. Generate the full 52-card deck.

The ranks are `23456789TJQKA` and the suits are `CDHS`.
3. Build the list of available replacement cards.

Every card not already present on the board can be assigned to a joker.
4. Generate every valid joker replacement assignment.

If there are no jokers, there is exactly one assignment.

If there is one joker, try every available card.

If there are two jokers, try every ordered pair of distinct available cards.

The order matters because `J1` and `J2` are distinct positions.
5. For each assignment, create the completed board.

Replace joker cells with the chosen cards.
6. Enumerate every possible 3×3 square.

The upper-left corner ranges from `(0,0)` to `(n-3,m-3)`.
7. Check whether a square is valid.

Extract its 9 cards.

The square is valid if either:

- all suits are identical, or
- all ranks are distinct.
8. Store every valid square.

We only need its upper-left coordinates.
9. Try every pair of valid squares.

Two squares are compatible if their cell sets do not intersect.
10. As soon as a non-overlapping pair is found, print the assignment and coordinates.

Any valid answer is acceptable.
11. If all assignments fail, print `No solution.`

### Why it works

The algorithm explicitly examines every legal completed board because every joker replacement assignment is tried. For each completed board, it explicitly checks every possible 3×3 square and every possible pair of squares. A solution exists if and only if at least one examined pair satisfies both validity and non-overlap conditions. Since no configuration is skipped, the algorithm cannot miss a valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

RANKS = "23456789TJQKA"
SUITS = "CDHS"

FULL_DECK = [r + s for r in RANKS for s in SUITS]

def valid_square(board, r, c):
    suits = set()
    ranks = set()

    for i in range(r, r + 3):
        for j in range(c, c + 3):
            card = board[i][j]
            ranks.add(card[0])
            suits.add(card[1])

    return len(suits) == 1 or len(ranks) == 9

def overlap(r1, c1, r2, c2):
    cells1 = set()
    cells2 = set()

    for i in range(r1, r1 + 3):
        for j in range(c1, c1 + 3):
            cells1.add((i, j))

    for i in range(r2, r2 + 3):
        for j in range(c2, c2 + 3):
            cells2.add((i, j))

    return not cells1.isdisjoint(cells2)

def solve():
    n, m = map(int, input().split())

    board = []
    jokers = []
    used = set()

    for i in range(n):
        row = input().split()
        board.append(row)

        for j, card in enumerate(row):
            if card in ("J1", "J2"):
                jokers.append((card, i, j))
            else:
                used.add(card)

    available = [card for card in FULL_DECK if card not in used]

    assignments = []

    if len(jokers) == 0:
        assignments.append({})
    elif len(jokers) == 1:
        name, _, _ = jokers[0]
        for card in available:
            assignments.append({name: card})
    else:
        for i in range(len(available)):
            for j in range(len(available)):
                if i == j:
                    continue
                assignments.append({
                    "J1": available[i],
                    "J2": available[j]
                })

    for assign in assignments:
        cur = [row[:] for row in board]

        for name, r, c in jokers:
            cur[r][c] = assign[name]

        good = []

        for r in range(n - 2):
            for c in range(m - 2):
                if valid_square(cur, r, c):
                    good.append((r, c))

        for i in range(len(good)):
            for j in range(i + 1, len(good)):
                r1, c1 = good[i]
                r2, c2 = good[j]

                if not overlap(r1, c1, r2, c2):
                    print("Solution exists.")

                    if len(jokers) == 0:
                        print("There are no jokers.")
                    elif len(jokers) == 1:
                        print(f"Replace {jokers[0][0]} with {assign[jokers[0][0]]}.")
                    else:
                        print(
                            f"Replace J1 with {assign['J1']} and J2 with {assign['J2']}."
                        )

                    print(f"Put the first square to ({r1 + 1}, {c1 + 1}).")
                    print(f"Put the second square to ({r2 + 1}, {c2 + 1}).")
                    return

    print("No solution.")

solve()
```

The solution follows the brute-force structure directly because the constraints are small enough to allow exhaustive search.

The `valid_square` function checks the two allowed properties independently. The square is accepted if either all suits are equal or all ranks are distinct. Using sets makes this clean: one suit means `len(suits) == 1`, while nine distinct ranks means `len(ranks) == 9`.

The overlap check is implemented with explicit cell sets. Since each square always contains only 9 cells, this stays constant time and avoids tricky rectangle arithmetic mistakes.

The assignment generation is careful about deck legality. Replacement cards come only from `available`, which excludes every non-joker card already present on the board. When there are two jokers, the code forbids using the same replacement card twice.

A subtle implementation detail is copying the board correctly:

```
cur = [row[:] for row in board]
```

Using `board[:]` alone would create a shallow copy and mutate the original rows.

The coordinates printed in the output are 1-indexed, so the code adds 1 before printing.

## Worked Examples

### Example 1

Input:

```
4 6
2S 3S 4S 7S 8S AS
5H 6H 7H 5S TC AC
8H 9H TH 7C 8C 9C
2D 2C 3C 4C 5C 6C
```

Possible 3×3 squares:

| Top-left | Valid? | Reason |
| --- | --- | --- |
| (1,1) | No | Mixed suits, repeated ranks |
| (1,2) | No | Mixed suits, repeated ranks |
| (1,3) | No | Mixed suits, repeated ranks |
| (1,4) | No | Mixed suits, repeated ranks |
| (2,1) | No | Mixed suits, repeated ranks |
| (2,2) | No | Mixed suits, repeated ranks |
| (2,3) | No | Mixed suits, repeated ranks |
| (2,4) | No | Mixed suits, repeated ranks |

No valid square exists at all, so forming two non-overlapping valid squares is impossible.

The trace demonstrates that the algorithm does not assume every dense suit region is valid. The distinct-rank condition is global over all 9 cards.

### Example 2

Input:

```
6 6
2S 3S 4S 2H 3H 4H
5S 6S 7S 5H 6H 7H
8S 9S TS 8H 9H TH
2D 3D 4D 2C 3C 4C
5D 6D 7D 5C 6C 7C
8D 9D TD 8C 9C TC
```

Valid squares:

| Top-left | Valid? | Reason |
| --- | --- | --- |
| (1,1) | Yes | All suits are S |
| (1,4) | Yes | All suits are H |
| (4,1) | Yes | All suits are D |
| (4,4) | Yes | All suits are C |

The algorithm immediately finds two non-overlapping squares, for example `(1,1)` and `(1,4)`.

This trace confirms the overlap logic. Even though four valid squares exist, the algorithm still checks that chosen pairs do not share cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(52² · S²) | At most 2652 joker assignments and at most 225 squares |
| Space | O(S) | Stores all valid squares |

Here `S = (n-2)(m-2)`.

The worst-case operation count easily fits within the 2-second limit because every component is bounded by small constants. Memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    RANKS = "23456789TJQKA"
    SUITS = "CDHS"
    FULL_DECK = [r + s for r in RANKS for s in SUITS]

    input = sys.stdin.readline

    def valid_square(board, r, c):
        suits = set()
        ranks = set()

        for i in range(r, r + 3):
            for j in range(c, c + 3):
                card = board[i][j]
                suits.add(card[1])
                ranks.add(card[0])

        return len(suits) == 1 or len(ranks) == 9

    def overlap(r1, c1, r2, c2):
        s1 = set()
        s2 = set()

        for i in range(r1, r1 + 3):
            for j in range(c1, c1 + 3):
                s1.add((i, j))

        for i in range(r2, r2 + 3):
            for j in range(c2, c2 + 3):
                s2.add((i, j))

        return not s1.isdisjoint(s2)

    n, m = map(int, input().split())

    board = []
    jokers = []
    used = set()

    for i in range(n):
        row = input().split()
        board.append(row)

        for j, card in enumerate(row):
            if card in ("J1", "J2"):
                jokers.append((card, i, j))
            else:
                used.add(card)

    available = [x for x in FULL_DECK if x not in used]

    assignments = []

    if len(jokers) == 0:
        assignments.append({})
    elif len(jokers) == 1:
        for c in available:
            assignments.append({jokers[0][0]: c})
    else:
        for a in available:
            for b in available:
                if a != b:
                    assignments.append({"J1": a, "J2": b})

    out = []

    for assign in assignments:
        cur = [r[:] for r in board]

        for name, r, c in jokers:
            cur[r][c] = assign[name]

        good = []

        for r in range(n - 2):
            for c in range(m - 2):
                if valid_square(cur, r, c):
                    good.append((r, c))

        for i in range(len(good)):
            for j in range(i + 1, len(good)):
                if not overlap(*good[i], *good[j]):
                    out.append("Solution exists.")
                    return "\n".join(out)

    return "No solution."

# provided sample
assert run(
"""4 6
2S 3S 4S 7S 8S AS
5H 6H 7H 5S TC AC
8H 9H TH 7C 8C 9C
2D 2C 3C 4C 5C 6C
"""
) == "No solution.", "sample 1"

# simple valid case
assert run(
"""6 6
2S 3S 4S 2H 3H 4H
5S 6S 7S 5H 6H 7H
8S 9S TS 8H 9H TH
2D 3D 4D 2C 3C 4C
5D 6D 7D 5C 6C 7C
8D 9D TD 8C 9C TC
"""
).startswith("Solution exists."), "two obvious suit squares"

# one joker needed
assert run(
"""3 6
J1 3S 4S 2H 3H 4H
5S 6S 7S 5H 6H 7H
8S 9S TS 8H 9H TH
"""
).startswith("Solution exists."), "joker replacement"

# overlapping-only valid squares
assert run(
"""3 5
2S 3S 4S 5S 6S
7S 8S 9S TS JS
QS KS AS 2H 3H
"""
) == "No solution.", "overlap detection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | No solution. | No valid squares exist |
| 6×6 four-suit blocks | Solution exists. | Basic successful detection |
| One joker board | Solution exists. | Joker replacement correctness |
| 3×5 overlapping squares | No solution. | Non-overlap condition |

## Edge Cases

Consider the overlap-only configuration:

```
3 5
2S 3S 4S 5S 6S
7S 8S 9S TS JS
QS KS AS 2H 3H
```

The algorithm finds two valid squares:

- top-left `(1,1)`
- top-left `(1,2)`

Both are all-spade squares. During pair checking, the overlap function builds the two 9-cell sets and detects shared cells. Since every pair overlaps, the final answer becomes `No solution.`

Now consider a joker case:

```
3 3
J1 2S 3S
4S 5S 6S
7S 8S 9S
```

The available deck excludes every card already present. The algorithm tries all remaining cards for `J1`.

When trying `AS`, the square becomes entirely spades, so it is valid.

When trying `2H`, the ranks become:

```
2 2 3 4 5 6 7 8 9
```

There are only 8 distinct ranks, so the distinct-rank condition fails. The algorithm rejects this assignment automatically because the set size is not 9.

Finally, consider the smallest possible board:

```
3 3
2S 3S 4S
5S 6S 7S
8S 9S TS
```

Only one 3×3 square exists. Even though it is valid, there cannot be two non-overlapping squares. The algorithm stores exactly one valid square, so the pair loop never finds a solution and correctly prints `No solution.`
