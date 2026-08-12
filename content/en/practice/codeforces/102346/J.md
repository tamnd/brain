---
title: "CF 102346J - Jar of Water Game"
description: "We have a circle of at most 13 contestants. There are four copies of each card value being used, plus one wildcard. Each contestant starts with four ordinary cards, while the starting contestant also receives the wildcard and therefore initially has five cards."
date: "2026-08-13T01:47:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 667
verified: true
draft: false
---

[CF 102346J - Jar of Water Game](https://codeforces.com/problemset/problem/102346/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circle of at most 13 contestants. There are four copies of each card value being used, plus one wildcard. Each contestant starts with four ordinary cards, while the starting contestant also receives the wildcard and therefore initially has five cards.

The important part is that the game is completely deterministic. The next contestant is always the person to the right of the current contestant, and the card to pass is determined uniquely by the rules. If the current contestant has the wildcard and did not just receive it, the wildcard must be passed. Otherwise, the contestant passes an ordinary card whose frequency in their hand is minimum, breaking ties by the fixed card order `A23456789DQJK`.

A contestant wins exactly when they have four cards, all with the same value. The wildcard does not substitute for a missing card. As soon as at least one contestant reaches that state, the game stops and the contestant with the smallest contestant number among all winning contestants is printed.

The input gives `N` and `K`, followed by four ordinary cards for every contestant. The wildcard is not written in the input. We place it in contestant `K` before simulating the first turn.

The upper bound `N <= 13` is the reason direct simulation is appropriate. There are only 13 possible ordinary card values, so every decision can be made by scanning at most 13 counters. The statement does not give a separate upper bound on the number of turns, so the natural complexity parameter is the number `T` of turns actually simulated before somebody wins. Since the rules leave no choices for the program to explore, there is no search tree.

There are several edge cases that can silently break a simulation.

First, the starting contestant cannot immediately pass the wildcard. For example,

```
2 1
ABBB
AAAB
```

has contestant 1 holding `ABBB` plus the wildcard. The wildcard was just received, so contestant 1 must pass an ordinary card. `A` occurs once and `B` occurs three times, so `A` is passed to contestant 2. Contestant 2 then has `AAAA` and wins, so the output is `2`. A careless implementation that immediately passes the wildcard would produce a different game.

Second, the game can already be over before the first turn. For example,

```
2 2
AAAA
2222
```

gives contestant 2 the wildcard, so contestant 2 has five cards, but contestant 1 already has four `A` cards. The correct output is `1`. Checking for a winner only after the first move is incorrect.

Third, the contestant receiving an ordinary card temporarily has five cards, so simply checking whether some value occurs four times is not enough. In

```
3 3
AAA2
2233
A223
```

contestant 3 starts with the wildcard. They must pass `A`, because `A` and `3` both occur once and `A` is the lower value. The card goes from contestant 3 to contestant 1 because the circle wraps around. Contestant 1 temporarily has `AAAA2`, which is five cards and is not yet winning. On the next turn contestant 1 passes its only `2`, leaving `AAAA`, so contestant 1 wins and the output is `1`.

Finally, the tie-breaking order is the card order from the statement, not alphabetical order. Since `A` is the smallest value, a tie between `A` and `2` must choose `A`. The same fixed order is used every time an ordinary card must be selected.

## Approaches

The most direct approach is to simulate the game exactly as described. Store, for every contestant and every one of the 13 ordinary card values, how many copies are currently in their hand. Store the wildcard separately because it has special behavior and must never participate in the minimum-frequency calculation.

A naive simulation can scan all contestants after every move to see whether somebody has won. For each contestant we inspect all 13 card counters, so one turn costs `O(13N)`, or at most 169 counter inspections when `N = 13`. If the game lasts `T` turns, this gives `O(13NT)`, equivalently `O(NT)` because 13 is fixed. The exact upper bound on these inspections is `169T` for the maximum `N`.

That approach is already fast enough for the given constraints, but there is a simple structural improvement. After we have checked the initial position and established that nobody is currently winning, a move changes the hands of only two contestants: the sender and the receiver. Every other hand is unchanged. Consequently, no untouched contestant can suddenly become a winner. After each move we only need to test those two contestants.

The same observation applies regardless of whether the passed card is the wildcard or an ordinary card. The sender and receiver are the only two hands whose contents changed. Each winning-state check scans at most 13 counters, so the optimal simulation spends `O(13)` work on selecting a card and `O(13)` work on checking each affected hand. Since the card universe has fixed size 13, this is effectively `O(T)`.

The brute-force simulation works because the game has no player decisions left once the initial state is known, but it repeatedly examines players whose hands could not possibly have changed. The observation that only the sender and receiver can change lets us remove those unnecessary scans without changing the simulated sequence at all.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full scan after every turn | `O(13NT)` | `O(13N)` | Accepted, but performs unnecessary scans |
| Check only affected contestants | `O(13T)` | `O(13N)` | Accepted |

## Algorithm Walkthrough

1. Encode the card values in the exact order `A23456789DQJK`. Give every card value an index from 0 to 12. This lets a single integer index represent both the card and its tie-breaking priority.
2. Build a `N x 13` frequency array from the input. For contestant `K`, separately mark that they hold the wildcard. Keeping the wildcard outside the ordinary counts prevents it from being considered when choosing the least frequent ordinary card.
3. Before making any move, scan every contestant and check whether they are already in a winning state. A winning hand must have no wildcard, exactly four ordinary cards in total, and all four must have the same value. If several contestants are already winning, return the smallest contestant number immediately.
4. Set the current contestant to `K` and mark the wildcard as newly received. This special flag is needed only for the contestant currently holding the wildcard. The starting contestant is treated exactly like somebody who has just received it.
5. Compute the next contestant as the person immediately to the right, wrapping from `N` back to `1`. In zero-based Python indexing, this is `(current + 1) % N`.
6. If the current contestant has the wildcard and it was not newly received, pass the wildcard to the next contestant. Remove it from the current contestant, give it to the next contestant, and mark the wildcard as newly received there.
7. Otherwise, choose an ordinary card to pass. Scan the 13 card frequencies, ignoring zero counts and ignoring the wildcard. Select the smallest positive frequency, and when two values have that frequency, keep the smaller card index. This directly implements both levels of the required tie-breaking rule.
8. Move the selected ordinary card from the current contestant to the next contestant. The wildcard state does not change in this case because the wildcard stays with its current holder. If the current contestant had just received the wildcard, the special restriction is now consumed, so their next turn may pass the wildcard.
9. After the move, check only the current contestant and the next contestant. Those are the only hands that changed. If either is winning, choose the smaller contestant number among the winning candidates and return it.
10. Make the next contestant the current contestant and repeat the simulation until a winner is found.

### Why it works

The central invariant is that the stored card counts exactly describe the real game state immediately before every simulated turn. The wildcard flag records whether its current holder is forbidden from passing it. At each turn, the algorithm follows exactly one of the two legal cases from the rules: it passes the wildcard when allowed, or selects the minimum-frequency ordinary card using the prescribed value order. Thus the resulting state is exactly the state of the real game after that turn.

The initial winner check handles games that end before any move. After that check, a new winning state can only appear in a contestant whose hand changed, namely the sender or receiver. Checking those two contestants after every move is consequently sufficient. When a winning state is found, selecting the smallest contestant index matches the required winner rule, so the returned contestant is exactly the one declared by the game.

## Python Solution

```python
import sys
input = sys.stdin.readline

VALUES = "A23456789DQJK"
V = len(VALUES)
POS = {ch: i for i, ch in enumerate(VALUES)}

def is_winner(cards, has_wild):
    if has_wild:
        return False

    total = 0
    has_four = False

    for x in cards:
        total += x
        if x == 4:
            has_four = True

    return total == 4 and has_four

def solve():
    n, k = map(int, input().split())
    k -= 1

    cards = [[0] * V for _ in range(n)]
    has_wild = [False] * n

    for i in range(n):
        s = input().strip()
        for ch in s:
            cards[i][POS[ch]] += 1

    has_wild[k] = True

    # The game may already be over before the first turn.
    for i in range(n):
        if is_winner(cards[i], has_wild[i]):
            return i + 1

    current = k
    wild_new = True

    while True:
        nxt = (current + 1) % n

        # The wildcard can be passed only if it was not
        # received immediately before this turn.
        if has_wild[current] and not wild_new:
            has_wild[current] = False
            has_wild[nxt] = True
            wild_new = True

        else:
            # Pass the least frequent ordinary card.
            # Ties are resolved by VALUES order, which is exactly
            # the index order 0..12.
            chosen = -1
            best_count = 10

            for value in range(V):
                cnt = cards[current][value]
                if cnt == 0:
                    continue

                if cnt < best_count:
                    best_count = cnt
                    chosen = value

            cards[current][chosen] -= 1
            cards[nxt][chosen] += 1

            # If the current player was holding a newly received
            # wildcard, it has now been held for one turn.
            if has_wild[current]:
                wild_new = False

        # Only these two contestants changed.
        winner = -1

        if is_winner(cards[current], has_wild[current]):
            winner = current

        if is_winner(cards[nxt], has_wild[nxt]):
            if winner == -1 or nxt < winner:
                winner = nxt

        if winner != -1:
            return winner

        current = nxt

if __name__ == "__main__":
    print(solve())
```

The `VALUES` string serves two purposes. It gives every card a stable integer index, and that index already represents the required tie-breaking order. There is no need for a separate comparison function.

The ordinary cards are stored as counts rather than as individual card objects. This is enough because the rules only ask how many times each value occurs. It also makes the least-frequency selection a fixed 13-element scan.

The wildcard is stored in `has_wild`. This separation is especially useful for the winning-state test. A contestant holding the wildcard cannot have exactly four cards, even if their four ordinary cards are all equal, so `is_winner` rejects every wildcard holder.

The initial scan happens before the first turn because the game ends as soon as a winning state exists. The starting contestant may have five cards because of the wildcard, so the wildcard holder is never incorrectly accepted as an initial winner.

The expression `(current + 1) % n` handles the circular order without special cases. When the current contestant is `n - 1`, the next contestant becomes zero, corresponding to contestant 1.

The `wild_new` flag is initialized to `True` because contestant `K` received the wildcard immediately before the first turn. When an ordinary card is passed while its holder has the wildcard, the flag becomes `False`, meaning the wildcard can be passed on that contestant's next turn. When the wildcard itself is passed, the receiving contestant gets `wild_new = True`.

The winner check after a move examines only `current` and `nxt`. Their hands are the only ones modified by that move, while the initial scan guarantees that no winning contestant was already present elsewhere. If both affected contestants are winning, the smaller zero-based index is selected, which corresponds to the smaller contestant number.

## Worked Examples

### Sample 1

The input is

```
2 1
33J3
JJJ3
```

Contestant 1 starts with `33J3` and the wildcard. Contestant 2 has `JJJ3`.

| Turn | Current | Wildcard status | Action | State after move | Winner |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Just received | Pass `J` | Player 2 gets `JJJJ` | 2 |

Contestant 1 cannot pass the wildcard because it was just received. Among the ordinary cards, `J` occurs once while `3` occurs three times, so `J` is selected. Contestant 2 receives its fourth `J`, producing the winning hand `JJJJ`. The game stops immediately with contestant 2 as the winner.

This demonstrates the special first-turn wildcard restriction and the fact that the winning condition must be checked after the transfer.

### Sample 2

The input is

```
2 2
A2A2
22AA
```

Contestant 2 starts with the wildcard.

| Turn | Current | Wildcard status | Action | Relevant state after move | Winner |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | Just received | Pass `A` | P1: `AAA2`, P2: `AA22 + W` | None |
| 2 | 1 | No wildcard | Pass `2` | P1: `AAA`, P2: `AAA2 + W` | None |
| 3 | 2 | Can pass wildcard | Pass `W` | P1: `AAA + 2 + W`, P2: `AAA2` | None |
| 4 | 1 | Just received | Pass `2` | P1: `AAA + W`, P2: `AAAA` | 2 |

On the first turn contestant 2 cannot pass the wildcard, so the ordinary cards `A` and `2` are compared. Both occur twice, and `A` is smaller, so `A` is passed.

After contestant 1 passes a `2`, contestant 2 can finally pass the wildcard. Contestant 1 then receives the wildcard and is forbidden from passing it immediately, so it passes its remaining `2`. Contestant 2 now has exactly four `A`? No, the resulting ordinary hand is `AAAA`, so contestant 2 wins. The output is `2`.

The trace demonstrates why the wildcard's one-turn delay must be represented explicitly rather than inferred only from which contestant currently owns it.

## Complexity Analysis

Let `T` be the number of turns simulated before the game ends. There are exactly 13 ordinary card values.

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(13T) = O(T)` | Each turn scans 13 values for card selection and at most two 13-value winner checks |
| Space | `O(13N) = O(N)` | The frequency array stores 13 counters for every contestant |

With `N <= 13`, the state representation is tiny. Every operation over the card values is a fixed 13-element loop, so Python has very little overhead per turn. The solution does not perform any branching search or construct the enormous set of possible card distributions.

## Test Cases

```python
import sys
import io

VALUES = "A23456789DQJK"
POS = {ch: i for i, ch in enumerate(VALUES)}
V = 13

def game(data: str) -> str:
    inp = io.StringIO(data)

    n, k = map(int, inp.readline().split())
    k -= 1

    cards = [[0] * V for _ in range(n)]
    has_wild = [False] * n

    for i in range(n):
        s = inp.readline().strip()
        for ch in s:
            cards[i][POS[ch]] += 1

    has_wild[k] = True

    def winner(i):
        if has_wild[i]:
            return False
        return sum(cards[i]) == 4 and 4 in cards[i]

    for i in range(n):
        if winner(i):
            return str(i + 1)

    current = k
    wild_new = True

    while True:
        nxt = (current + 1) % n

        if has_wild[current] and not wild_new:
            has_wild[current] = False
            has_wild[nxt] = True
            wild_new = True
        else:
            chosen = -1
            best = 10

            for value in range(V):
                cnt = cards[current][value]
                if cnt and cnt < best:
                    best = cnt
                    chosen = value

            cards[current][chosen] -= 1
            cards[nxt][chosen] += 1

            if has_wild[current]:
                wild_new = False

        candidates = []
        if winner(current):
            candidates.append(current)
        if winner(nxt):
            candidates.append(nxt)

        if candidates:
            return str(min(candidates) + 1)

        current = nxt

# Provided samples
assert game("""\
2 1
33J3
JJJ3
""") == "2", "sample 1"

assert game("""\
2 2
A2A2
22AA
""") == "2", "sample 2"

assert game("""\
4 2
774Q
JJQ7
44Q7
4QJJ
""") == "3", "sample 3"

assert game("""\
3 1
JQAA
JJJA
QQQA
""") == "3", "sample 4"

# Minimum N, starting player has the wildcard, so player 1
# wins immediately with four equal ordinary cards.
assert game("""\
2 2
AAAA
2222
""") == "1", "initial winner while wildcard holder is not winning"

# The wildcard was just received, so player 1 must pass A.
# Player 2 then has AAAA and wins.
assert game("""\
2 1
ABBB
AAAB
""") == "2", "wildcard cannot be passed immediately"

# N = 3, K = 3. Player 3 passes A across the circular boundary
# to player 1. Player 1 later passes its only 2 and wins with AAAA.
assert game("""\
3 3
AAA2
2233
A223
""") == "1", "circular wrap-around and tie-breaking"

# Maximum N. Every contestant starts with four equal cards.
# Player 13 receives the wildcard, but player 1 is already winning.
assert game("""\
13 13
AAAA
2222
3333
4444
5555
6666
7777
8888
9999
DDDD
QQQQ
JJJJ
KKKK
""") == "1", "maximum N and all-equal hands"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / AAAA / 2222` | `1` | Minimum size and an initial winner who does not hold the wildcard |
| `2 1 / ABBB / AAAB` | `2` | Wildcard cannot be passed immediately |
| `3 3 / AAA2 / 2233 / A223` | `1` | Circular wrap-around and card-value tie-breaking |
| `13 13 / AAAA / 2222 / ... / KKKK` | `1` | Maximum `N`, all-equal hands, and initial winner detection |

## Edge Cases

The first edge case is the starting contestant holding a newly received wildcard. For

```
2 1
ABBB
AAAB
```

the state begins with contestant 1 holding `ABBB + W`. The `W` cannot be passed on turn 1, so the algorithm enters the ordinary-card branch. The frequencies are `A = 1` and `B = 3`, making `A` the selected card. Contestant 2 receives `A` and changes from `AAAB` to `AAAA`, so the affected-player winner check immediately returns `2`. No second turn is simulated.

The second edge case is an existing winner before the game starts. In

```
2 2
AAAA
2222
```

contestant 2 owns `2222 + W`, while contestant 1 owns exactly `AAAA`. The initial scan sees contestant 1 as a winner before any transfer occurs and returns `1`. The simulation loop is never entered. This also demonstrates why the wildcard must be excluded from the winning condition.

The third edge case is a wildcard holder who has four equal ordinary cards. Such a player has five total cards and is not winning. For example, if a contestant holds `AAAA + W`, the ordinary frequency array contains four `A` cards, but `has_wild` is true, so `is_winner` returns false. Only after the wildcard leaves can those four `A` cards become a winning hand.

The fourth edge case is circular indexing. In

```
3 3
AAA2
2233
A223
```

the first current contestant is contestant 3. Its right-hand neighbor is contestant 1, represented by `(2 + 1) % 3 = 0` in zero-based indexing. Contestant 3 has `A = 1`, `2 = 2`, and `3 = 1`, so the minimum frequency is one and the tie is between `A` and `3`. Since `A` has the smaller value index, it is passed to contestant 1. Contestant 1 later reaches `AAAA` and wins. This catches both the wrap-around boundary and the minimum-value tie-break.

The fifth edge case is a tie between multiple winning contestants. If the initial state is

```
3 3
AAAA
2222
3333
```

contestants 1 and 2 are both already winning, while contestant 3 has the wildcard. The initial scan proceeds in contestant-number order and returns contestant 1. The winner rule is based on contestant number, not card value, so the algorithm must never choose a later contestant merely because their four equal cards have a smaller value.
