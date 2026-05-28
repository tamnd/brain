---
title: "CF 71D - Solitaire"
description: "We are given a rectangular board filled with playing cards. The board size is at most $17 times 17$, but the total number of placed cards never exceeds 52 because the deck has only 52 regular cards plus two jokers. A valid 3×3 square must satisfy one of two properties: 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 2200
weight: 71
solve_time_s: 138
verified: true
draft: false
---

[CF 71D - Solitaire](https://codeforces.com/problemset/problem/71/D)

**Rating:** 2200  
**Tags:** brute force, implementation  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular board filled with playing cards. The board size is at most $17 \times 17$, but the total number of placed cards never exceeds 52 because the deck has only 52 regular cards plus two jokers.

A valid 3×3 square must satisfy one of two properties:

1. All 9 cards have the same suit.
2. All 9 cards have pairwise distinct ranks.

Two such squares must exist without overlapping.

The twist comes from jokers. The input may contain `J1` and `J2`, representing two distinct jokers from the deck. Before checking the condition, we may replace each joker with any unused card from the remaining deck. The replacement cards must be distinct and must not already appear on the board.

The task is not only to decide whether a solution exists, but also to print one valid joker replacement and the coordinates of the two 3×3 squares.

The constraints are small enough that brute force over board positions is realistic. The number of possible 3×3 squares is at most:

$$(17 - 2)^2 = 225$$

So even checking all pairs of squares is cheap:

$$225^2 \approx 5 \times 10^4$$

The expensive part is joker replacement. A naive search over all possible card assignments can reach roughly:

$$54^2 \cdot 225^2 \approx 1.5 \times 10^8$$

which is uncomfortable in Python once validation logic is added.

The key observation is that each 3×3 square contains only 9 cells. Whether a square can become valid depends only on those 9 cards, not on the rest of the board. That allows us to preprocess every square independently and record which joker assignments make it valid.

Several edge cases are easy to mishandle.

A joker may lie outside the chosen squares. In that case, its replacement still matters because every card in the deck must remain unique. A careless implementation might assign the same replacement card to both jokers simply because neither joker participates in a square.

For example:

```
3 6
2S 3S 4S 5S 6S 7S
8S 9S TS JS QS KS
AS J1 J2 2H 3H 4H
```

The two jokers are irrelevant to the valid square, but they still must receive distinct unused cards.

Another subtle case is overlap detection. Two 3×3 squares are invalid if they share even one cell.

For example, in a 4×4 board:

```
(1,1) square covers rows 1..3 and cols 1..3
(2,2) square covers rows 2..4 and cols 2..4
```

These overlap in a 2×2 region and cannot be used together.

A common bug is checking only whether top-left corners differ.

The rank condition also requires all 9 ranks to be pairwise distinct. Duplicate ranks immediately invalidate the square, even if suits differ.

Example:

```
2S 3H 4D
5C 6S 7H
8D 2C 9S
```

This is not valid under the rank rule because rank `2` appears twice.

## Approaches

The most direct solution is brute force.

We can enumerate every pair of 3×3 squares, enumerate every possible replacement for each joker, build the final board, and test whether both squares satisfy either condition.

The board contains at most 225 possible squares. There are at most 54 candidate cards for each joker. Testing one square costs constant time because it always contains exactly 9 cells.

That gives a worst-case complexity around:

$$225^2 \cdot 54^2$$

which is already more than 100 million combinations before accounting for validation overhead. Python can struggle with this.

The important structural observation is that squares are independent. A square only cares about the cards inside its own 9 cells. So instead of trying all global joker assignments first, we can preprocess each square and ask:

"Which joker replacements make this particular square valid?"

Since there are at most two jokers, the number of replacement combinations is tiny:

- no jokers: exactly one state
- one joker: at most 52 possible cards
- two jokers: at most $52 \cdot 51$

For each square, we test every legal joker assignment once and store all assignments that make the square valid.

After preprocessing, solving the problem becomes easy:

1. Enumerate pairs of non-overlapping squares.
2. Check whether their valid assignment sets are compatible.
3. Compatibility means both squares agree on the final joker replacement.

This transforms the problem from repeated expensive validation into a lookup problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(S^2 \cdot C^2)$ | $O(1)$ | Too slow |
| Optimal | $O(S \cdot C^2 + S^2 \cdot A)$ | $O(S \cdot A)$ | Accepted |

Here:

- $S \le 225$ is the number of squares
- $C \le 54$ is the number of card assignments
- $A$ is the number of valid assignments per square

In practice, $A$ is small.

## Algorithm Walkthrough

1. Parse the board and collect all used regular cards.

Jokers are excluded because they may later become any unused card.
2. Generate the list of unused cards from the full 52-card deck.

These are the only legal replacements for jokers.
3. Enumerate every 3×3 square on the board.

A square is identified by its top-left corner.
4. For each square, test every possible joker assignment.

If there are no jokers, there is only one assignment.

If there is one joker, try every unused card.

If there are two jokers, try every ordered pair of distinct unused cards.
5. After substituting joker values inside the square, test whether the square is valid.

A square is valid if either:

- all suits are identical
- all ranks are distinct
6. Store every assignment that makes the square valid.

The stored key is the full global joker assignment:

- `()` if no jokers
- `(card,)` if one joker exists
- `(card1, card2)` if both exist
7. Enumerate all pairs of squares.

Skip pairs whose areas overlap.
8. For a non-overlapping pair, check whether there exists a joker assignment present in both squares' valid assignment sets.

Since joker replacements are global, both squares must agree on the same final assignment.
9. As soon as one compatible pair is found, print the required output.
10. If no pair works, print `"No solution."`

### Why it works

Each square is evaluated under every legal joker replacement. The preprocessing step records exactly the assignments under which the square becomes valid.

Later, when combining two squares, requiring a shared assignment guarantees that the same global joker replacement makes both squares valid simultaneously.

Non-overlap is checked explicitly, so the final configuration always satisfies all constraints.

Because every legal assignment and every square pair is examined, no valid solution can be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

RANKS = "23456789TJQKA"
SUITS = "CDHS"

ALL_CARDS = [r + s for r in RANKS for s in SUITS]

def overlap(r1, c1, r2, c2):
    return not (
        r1 + 2 < r2 or
        r2 + 2 < r1 or
        c1 + 2 < c2 or
        c2 + 2 < c1
    )

def valid_square(cells):
    suits = [x[1] for x in cells]
    if len(set(suits)) == 1:
        return True

    ranks = [x[0] for x in cells]
    return len(set(ranks)) == 9

def solve():
    n, m = map(int, input().split())
    board = [input().split() for _ in range(n)]

    jokers = []
    used = set()

    for i in range(n):
        for j in range(m):
            card = board[i][j]
            if card in ("J1", "J2"):
                jokers.append(card)
            else:
                used.add(card)

    unused = [c for c in ALL_CARDS if c not in used]

    joker_count = len(jokers)

    assignments = []

    if joker_count == 0:
        assignments.append(())
    elif joker_count == 1:
        for c in unused:
            assignments.append((c,))
    else:
        for c1 in unused:
            for c2 in unused:
                if c1 != c2:
                    assignments.append((c1, c2))

    square_info = []

    for r in range(n - 2):
        for c in range(m - 2):
            valid_assignments = set()

            for assn in assignments:
                cells = []

                ok = True

                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        card = board[i][j]

                        if card == "J1":
                            if joker_count == 1:
                                card = assn[0]
                            else:
                                card = assn[0]
                        elif card == "J2":
                            card = assn[1]

                        cells.append(card)

                if valid_square(cells):
                    valid_assignments.add(assn)

            square_info.append((r, c, valid_assignments))

    total = len(square_info)

    for i in range(total):
        r1, c1, s1 = square_info[i]

        if not s1:
            continue

        for j in range(i + 1, total):
            r2, c2, s2 = square_info[j]

            if not s2:
                continue

            if overlap(r1, c1, r2, c2):
                continue

            common = s1 & s2

            if common:
                assn = next(iter(common))

                print("Solution exists.")

                if joker_count == 0:
                    print("There are no jokers.")
                elif joker_count == 1:
                    print(f"Replace {jokers[0]} with {assn[0]}.")
                else:
                    print(f"Replace J1 with {assn[0]} and J2 with {assn[1]}.")

                print(f"Put the first square to ({r1 + 1}, {c1 + 1}).")
                print(f"Put the second square to ({r2 + 1}, {c2 + 1}).")
                return

    print("No solution.")

solve()
```

The implementation follows the preprocessing strategy directly.

`valid_square` checks the two allowed patterns. Suit equality is tested first because it is slightly cheaper. Rank uniqueness simply uses a set.

The `assignments` list represents every legal global joker replacement. The ordering matters when both jokers exist because `J1 -> A`, `J2 -> B` differs from `J1 -> B`, `J2 -> A`.

Each square stores a set of valid assignments. Using a set makes intersection testing efficient later.

The overlap test is easy to get wrong. Two 3×3 squares do not overlap only if one lies completely above, below, left, or right of the other. Every other configuration overlaps.

The replacement logic inside square construction intentionally substitutes only joker cells. All normal cards remain unchanged.

The final search simply finds a pair of squares with a non-empty assignment intersection.

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

Possible squares:

| Square | Top-left | Valid |
| --- | --- | --- |
| A | (1,1) | No |
| B | (1,2) | No |
| C | (1,3) | No |
| D | (1,4) | No |
| E | (2,1) | No |
| F | (2,2) | No |
| G | (2,3) | No |
| H | (2,4) | No |

No square satisfies either rule, so no pair can work.

Output:

```
No solution.
```

This example demonstrates that even visually structured regions may fail because rank uniqueness requires all nine ranks to differ exactly.

### Example 2

Input:

```
3 6
2S 3S 4S 5H 6H 7H
5S 6S 7S 8H 9H TH
8S 9S TS J1 QH KH
```

Unused cards include many possibilities.

The left 3×3 square contains:

| 2S | 3S | 4S |
| --- | --- | --- |
| 5S | 6S | 7S |
| 8S | 9S | TS |

All suits are `S`, so the square is valid immediately.

The right 3×3 square contains ranks:

| H | H | H |
| --- | --- | --- |
| H | H | H |
| J1 | H | H |

Replacing `J1` with `AH` makes all ranks distinct:

$$5,6,7,8,9,T,A,Q,K$$

The algorithm records this assignment as valid for the second square and finds a compatible pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(S \cdot C^2 + S^2 \cdot A)$ | preprocess all squares and assignments, then test square pairs |
| Space | $O(S \cdot A)$ | stores valid assignments for each square |

With at most 225 squares and at most a few thousand joker assignments, the solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    RANKS = "23456789TJQKA"
    SUITS = "CDHS"

    ALL_CARDS = [r + s for r in RANKS for s in SUITS]

    def overlap(r1, c1, r2, c2):
        return not (
            r1 + 2 < r2 or
            r2 + 2 < r1 or
            c1 + 2 < c2 or
            c2 + 2 < c1
        )

    def valid_square(cells):
        suits = [x[1] for x in cells]
        if len(set(suits)) == 1:
            return True

        ranks = [x[0] for x in cells]
        return len(set(ranks)) == 9

    input = sys.stdin.readline

    n, m = map(int, input().split())
    board = [input().split() for _ in range(n)]

    jokers = []
    used = set()

    for i in range(n):
        for j in range(m):
            card = board[i][j]
            if card in ("J1", "J2"):
                jokers.append(card)
            else:
                used.add(card)

    unused = [c for c in ALL_CARDS if c not in used]

    joker_count = len(jokers)

    assignments = []

    if joker_count == 0:
        assignments.append(())
    elif joker_count == 1:
        for c in unused:
            assignments.append((c,))
    else:
        for c1 in unused:
            for c2 in unused:
                if c1 != c2:
                    assignments.append((c1, c2))

    square_info = []

    for r in range(n - 2):
        for c in range(m - 2):
            valid_assignments = set()

            for assn in assignments:
                cells = []

                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        card = board[i][j]

                        if card == "J1":
                            card = assn[0]
                        elif card == "J2":
                            card = assn[1]

                        cells.append(card)

                if valid_square(cells):
                    valid_assignments.add(assn)

            square_info.append((r, c, valid_assignments))

    total = len(square_info)

    for i in range(total):
        r1, c1, s1 = square_info[i]

        for j in range(i + 1, total):
            r2, c2, s2 = square_info[j]

            if overlap(r1, c1, r2, c2):
                continue

            if s1 & s2:
                print("Solution exists.")
                return out.getvalue()

    print("No solution.")
    return out.getvalue()

# provided sample
assert run(
"""4 6
2S 3S 4S 7S 8S AS
5H 6H 7H 5S TC AC
8H 9H TH 7C 8C 9C
2D 2C 3C 4C 5C 6C
"""
).strip() == "No solution.", "sample 1"

# minimum board
assert "No solution." in run(
"""3 3
2S 3S 4S
5S 6S 7S
8S 9S TS
"""
), "single square cannot form two non-overlapping squares"

# simple positive case
assert "Solution exists." in run(
"""3 6
2S 3S 4S 2H 3H 4H
5S 6S 7S 5H 6H 7H
8S 9S TS 8H 9H TH
"""
), "two disjoint suit squares"

# overlap trap
assert "No solution." in run(
"""4 4
2S 3S 4S 5S
6S 7S 8S 9S
TS JS QS KS
AH 2H 3H 4H
"""
), "overlapping valid squares are forbidden"

# joker replacement
assert "Solution exists." in run(
"""3 6
2S 3S 4S 5H 6H 7H
5S 6S 7S 8H 9H TH
8S 9S TS J1 QH KH
"""
), "joker creates distinct ranks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3×3 single valid square | No solution | Need two non-overlapping squares |
| Two horizontal suit squares | Solution exists | Basic positive case |
| 4×4 overlapping candidates | No solution | Correct overlap detection |
| One joker repair | Solution exists | Joker substitution logic |

## Edge Cases

Consider the overlap issue again.

Input:

```
4 4
2S 3S 4S 5S
6S 7S 8S 9S
TS JS QS KS
AH 2H 3H 4H
```

The square at `(1,1)` is valid because all suits are spades.

The square at `(2,2)` also looks promising:

```
7S 8S 9S
JS QS KS
2H 3H 4H
```

A buggy implementation might accept both because their top-left coordinates differ.

The algorithm correctly rejects them because rows `2..3` and columns `2..3` overlap.

Another tricky case involves duplicate ranks.

Input:

```
3 3
2S 3H 4D
5C 6S 7H
8D 2C 9S
```

The suits are not uniform.

The ranks are:

```
2 3 4
5 6 7
8 2 9
```

Rank `2` appears twice, so the square is invalid.

The algorithm uses `len(set(ranks)) == 9`, which catches this immediately.

Finally, consider jokers outside the active squares.

Input:

```
3 6
2S 3S 4S 5S 6S 7S
8S 9S TS JS QS KS
AS J1 J2 2H 3H 4H
```

The left square already satisfies the suit condition. The jokers are irrelevant to it.

A careless solution might assign both jokers the same unused card because they are never inspected.

The algorithm generates assignments using ordered distinct pairs only, guaranteeing deck consistency globally.
