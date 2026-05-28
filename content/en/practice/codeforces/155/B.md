---
title: "CF 155B - Combination"
description: "We have a collection of cards. Every card gives two things when played. The first number adds to the score, and the second number adds extra opportunities to play more cards. The game starts with exactly one available move."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 155
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 109 (Div. 2)"
rating: 1100
weight: 155
solve_time_s: 95
verified: true
draft: false
---

[CF 155B - Combination](https://codeforces.com/problemset/problem/155/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of cards. Every card gives two things when played. The first number adds to the score, and the second number adds extra opportunities to play more cards.

The game starts with exactly one available move. Playing a card consumes one move, then immediately adds `b[i]` new moves. A card can only be used once. The game ends when there are no remaining moves or when every card has already been used.

The task is to choose both the subset of cards and the order of playing them so that the total earned score is as large as possible.

The constraints are small enough that sorting is easily affordable. With `n ≤ 1000`, even an `O(n^2)` solution would pass comfortably. Exponential search over all subsets or all permutations is impossible because `2^1000` and `1000!` are astronomically large. The structure of the game must be exploited directly.

The tricky part is that a card with low score can still be extremely valuable if it creates many additional moves. A greedy strategy that always takes the highest score first can fail badly.

Consider this example:

```
3
100 0
1 2
50 0
```

If we greedily pick the largest score first, we play `(100,0)` and the game ends with total `100`.

The optimal sequence is different. We first play `(1,2)`, which increases the number of available moves, then play both remaining cards. The total becomes `1 + 100 + 50 = 151`.

Another easy mistake is assuming every card with positive score should always be taken. Sometimes the game ends before we can reach them.

```
2
10 0
9 0
```

We only have one initial move and neither card creates extra moves. We can play exactly one card, so the answer is `10`, not `19`.

There is also a subtle ordering issue among cards that generate extra moves. Suppose we have:

```
3
5 1
4 1
100 0
```

Playing the two generating cards first lets us eventually take all three cards for `109`. If we play `(100,0)` immediately, the game ends at once.

The core challenge is balancing immediate score against future capacity to keep playing.

## Approaches

A brute-force solution would try every possible order of playing cards and simulate the game. This is correct because the game outcome depends entirely on the chosen sequence. Unfortunately, the number of permutations is `n!`. Even for `n = 15`, this is already too large.

We need to understand what actually matters in a good sequence.

Suppose a card has `b[i] > 0`. Playing it never reduces the total number of future playable cards. We spend one move and gain at least one back. Such cards are valuable because they keep the game alive.

Now suppose a card has `b[i] = 0`. Playing it strictly decreases the remaining move count by one. These cards consume the limited resource.

This observation suggests splitting the cards into two groups.

Cards with `b[i] > 0` are infrastructure cards. They help us continue playing more cards later. Cards with `b[i] = 0` are terminal cards. They should usually be delayed until we have already expanded our available moves as much as possible.

Among the infrastructure cards themselves, we want to prioritize the ones that create more future opportunities. If a card gives many extra moves, delaying it risks running out of moves before using it.

This leads to the greedy strategy:

Sort cards by descending `b[i]`. Then process them in that order while we still have available moves.

Why does this work?

Whenever we have a choice between two unused cards, the one with larger `b[i]` preserves more future flexibility. Taking it earlier can only help because it leaves us with at least as many future moves as any other choice.

Once all profitable expansion cards are handled, we use the remaining moves on the highest scoring terminal cards.

In fact, a single sorting rule already captures this behavior cleanly. Sorting by descending `b[i]` automatically places all expansion cards before terminal cards.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n!)` | `O(n)` | Too slow |
| Optimal Greedy + Sorting | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read all cards and store them as pairs `(a, b)`.
2. Sort the cards in descending order of `b`.

Cards that create more future moves should be used earlier because they keep the game alive longer.
3. Initialize the number of available moves as `1`.

This matches the game rule that we may initially play exactly one card.
4. Iterate through the sorted cards.
5. Before playing a card, check whether we still have at least one available move.

If the move counter is already zero, the game must stop immediately.
6. Play the current card.

Add `a[i]` to the answer.
7. Update the move counter.

Playing the card consumes one move and adds `b[i]` new moves, so:

```
moves = moves - 1 + b[i]
```
8. Continue until all cards are processed or the move counter becomes zero.

### Why it works

The key invariant is that after processing some prefix of the sorted order, no other ordering of those same cards could leave us with more remaining moves.

Suppose two cards are adjacent and their `b` values satisfy `b1 < b2`. If we swap them so that the larger `b` card comes first, the number of remaining moves after playing both cards increases earlier and never becomes worse later. This exchange argument shows that any optimal order can be transformed into one sorted by descending `b` without decreasing the achievable score.

Once the order is fixed this way, taking every playable card is always optimal because scores are non-negative. There is never a reason to skip a card if we still have an available move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cards = []

    for _ in range(n):
        a, b = map(int, input().split())
        cards.append((b, a))

    cards.sort(reverse=True)

    moves = 1
    ans = 0

    for b, a in cards:
        if moves == 0:
            break

        ans += a
        moves = moves - 1 + b

    print(ans)

solve()
```

The implementation stores cards as `(b, a)` instead of `(a, b)` because Python sorts tuples lexicographically. This makes descending sort automatically prioritize larger `b`.

The variable `moves` represents how many additional cards may still be played. Every iteration first checks whether the game has already ended. Forgetting this condition causes incorrect extra plays after the move counter reaches zero.

The update formula is the heart of the simulation:

```
moves = moves - 1 + b
```

The subtraction must happen because the current card consumes one playable opportunity. A common mistake is writing `moves += b`, which incorrectly allows free plays.

The solution never skips a playable card because all scores are non-negative. Once a card is reachable, taking it cannot reduce the total score.

## Worked Examples

### Sample 1

Input:

```
2
1 0
2 0
```

After sorting by descending `b`:

| Step | Card `(a,b)` | Moves Before | Score Before | Moves After | Score After |
| --- | --- | --- | --- | --- | --- |
| 1 | `(2,0)` | 1 | 0 | 0 | 2 |

The game stops immediately because no moves remain.

The trace shows why only one card can be played. Since neither card generates extra moves, the initial single move is the entire resource budget.

### Custom Example

Input:

```
4
100 0
1 3
50 0
40 0
```

Sorted order:

```
(1,3), (100,0), (50,0), (40,0)
```

Simulation:

| Step | Card `(a,b)` | Moves Before | Score Before | Moves After | Score After |
| --- | --- | --- | --- | --- | --- |
| 1 | `(1,3)` | 1 | 0 | 3 | 1 |
| 2 | `(100,0)` | 3 | 1 | 2 | 101 |
| 3 | `(50,0)` | 2 | 101 | 1 | 151 |
| 4 | `(40,0)` | 1 | 151 | 0 | 191 |

The first card has tiny score, but it unlocks enough moves to collect every other card. This demonstrates why maximizing immediate score is the wrong greedy criterion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates the running time |
| Space | `O(n)` | The card array stores all input cards |

With `n ≤ 1000`, this solution is easily fast enough. Sorting one thousand elements is negligible within a 2 second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    cards = []

    for _ in range(n):
        a, b = map(int, input().split())
        cards.append((b, a))

    cards.sort(reverse=True)

    moves = 1
    ans = 0

    for b, a in cards:
        if moves == 0:
            break

        ans += a
        moves = moves - 1 + b

    return str(ans)

# provided sample
assert solve_io(
"""2
1 0
2 0
"""
) == "2"

# minimum size
assert solve_io(
"""1
7 0
"""
) == "7"

# expansion card unlocks everything
assert solve_io(
"""4
100 0
1 3
50 0
40 0
"""
) == "191"

# all cards self-sustaining
assert solve_io(
"""3
5 1
6 1
7 1
"""
) == "18"

# greedy by score would fail
assert solve_io(
"""3
100 0
1 2
50 0
"""
) == "151"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single card with `b=0` | `7` | Minimum input size |
| One expansion card plus terminals | `191` | Extra moves must be used first |
| All `b=1` | `18` | Infinite continuation until cards run out |
| High score but no expansion | `151` | Greedy by score is incorrect |

## Edge Cases

Consider the case where every card has `b = 0`.

```
3
5 0
8 0
2 0
```

After sorting, the order becomes `(8,0), (5,0), (2,0)`.

We start with one move. Playing `(8,0)` reduces the move counter to zero immediately, so the answer becomes `8`.

The algorithm correctly realizes that only one card can ever be played.

Now consider a case where a low scoring card creates many extra moves.

```
3
100 0
1 2
50 0
```

The sorted order starts with `(1,2)` because its `b` value is largest.

After playing it, the move count becomes `2`, allowing both remaining cards to be collected. The final score becomes `151`.

A naive strategy based only on score would incorrectly stop at `100`.

Finally, consider cards with `b = 1`.

```
4
3 1
4 1
5 1
6 1
```

Each played card exactly replenishes the consumed move. The move counter never decreases until cards run out.

The simulation evolves like this:

```
1 -> 1 -> 1 -> 1 -> 1
```

All cards are played successfully, and the total score becomes `18`.

This confirms that the update formula handles self-sustaining cards correctly.
