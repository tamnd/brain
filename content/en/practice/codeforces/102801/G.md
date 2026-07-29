---
title: "CF 102801G - Halli Galli"
description: "Halli Galli is a simulation problem about several players revealing fruit cards one by one. The players act cyclically, so after the last player takes a turn, the first player starts again."
date: "2026-07-30T06:02:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "G"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 266
verified: true
draft: false
---

[CF 102801G - Halli Galli](https://codeforces.com/problemset/problem/102801/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 26s  
**Verified:** yes  

## Solution
# Problem Understanding

Halli Galli is a simulation problem about several players revealing fruit cards one by one. The players act cyclically, so after the last player takes a turn, the first player starts again. Each player keeps only their latest revealed card because a new card covers the previous one.

After every revealed card, we inspect all visible cards. For each fruit type among Apple, Banana, Grape, and Pear, we count how many fruits of that type are currently visible. If exactly five fruits of a type are present, the bell is pushed once for that type. The answer is the total number of bell pushes over all turns. The original statement defines up to 100 test cases, with at most 100 turns per case and at most 6 players.

The small limits are a clue that this is mainly an implementation and simulation problem. Even checking every fruit count from scratch after every turn is cheap. There are only four fruit types, so the direct simulation needs only a constant amount of work per turn. A solution with unnecessary large structures or complicated preprocessing is solving a harder problem than the one given.

The main source of mistakes is handling the replacement rule correctly. A player does not add cards forever. Their old card disappears when they reveal a new one.

For example:

```
1
2 1
A 5
A 5
```

The correct output is:

```
2
```

After the first turn, the visible cards contain five apples, so the bell rings once. After the second turn, the old card is replaced by the new apple card, not added on top of it. There are still five apples, so the bell rings once again. A careless implementation that keeps every played card would count ten apples and produce an incorrect result.

Another edge case is when several fruit types reach five at the same time.

```
1
3 3
A 5
B 5
G 5
```

The correct output is:

```
3
```

Each fruit type independently contributes one bell push. Checking only whether any fruit reaches five instead of counting all matching types loses these extra pushes.

A final boundary case appears when a player has no previous card.

```
1
1 6
P 1
```

The correct output is:

```
0
```

The first turn must only add the new card. There is nothing to remove from that player's position.

## Approaches

The brute-force approach is to store all currently visible cards, simulate every turn, and after each turn scan every player's card to rebuild the four fruit totals. This is correct because the game state is completely described by the cards currently visible. With at most six players and four fruit types, even this direct method is fast enough here.

The same idea can be viewed more generally. The visible state changes only at the position of the player whose turn it is. When that player reveals a card, one old card may disappear and one new card appears. Recomputing everything after every move is unnecessary because most of the state stays unchanged.

The key observation is that we only need the total number of each fruit currently visible. When a player changes cards, we can subtract the fruits from the old card and add the fruits from the new card. The fruit totals always represent the current board state, so after every turn we only need four comparisons to decide how many times the bell rings.

The brute-force works because the number of players is tiny, but the incremental update approach matches the structure of the game directly. It reduces the work from repeatedly scanning all players to updating one card and checking four counters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NK) | O(K) | Accepted with given limits |
| Optimal | O(N) | O(K) | Accepted |

## Algorithm Walkthrough

1. Store the current card of every player. Initially, every player has no card.
2. Keep four counters representing the number of visible fruits of each type. These counters are the complete information needed to decide whether the bell rings.
3. For every turn, determine which player is acting by using the turn index modulo the number of players.
4. If that player already has a card, remove its fruit amount from the corresponding fruit counter. The old card is no longer visible after the player reveals a new one.
5. Read the new card, store it as the player's current card, and add its fruit amount to the matching fruit counter.
6. Check the four fruit counters. Every counter equal to five adds one to the answer because every fruit type is counted independently.
7. After processing all turns, output the accumulated bell pushes.

Why it works:

The invariant is that after every processed turn, the four fruit counters exactly match the fruits shown on all players' current cards. Initially both are empty. When a player changes cards, removing the old card and adding the new card updates the counters to the new visible state. Since the bell condition depends only on these four totals, checking them after every update gives exactly the number of pushes required by the rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    index = {'A': 0, 'B': 1, 'G': 2, 'P': 3}

    for _ in range(t):
        n, k = map(int, input().split())

        cards = [None] * k
        counts = [0] * 4
        total = 0

        for turn in range(n):
            ch, x = input().split()
            x = int(x)

            player = turn % k

            if cards[player] is not None:
                old_ch, old_x = cards[player]
                counts[index[old_ch]] -= old_x

            cards[player] = (ch, x)
            counts[index[ch]] += x

            for value in counts:
                if value == 5:
                    total += 1

        ans.append(str(total))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `cards` array stores the latest card for each player. Its index is the player number, so finding the card to remove before an update takes constant time.

The `counts` array contains the current visible amount of each fruit. The mapping from fruit character to array index avoids repeated condition checks and keeps every update constant time.

The order of operations matters. The previous card must be removed before the new card is added because the new card replaces the old one. Checking the bell condition happens only after both operations, because the game judges the complete visible state after the turn finishes.

There is no risk of integer overflow in Python because the maximum number of turns is small. The answer is at most four bell pushes per turn, so it remains tiny.

## Worked Examples

For the sample:

```
1
5 3
A 5
B 2
B 3
G 1
P 5
```

The simulation is:

| Turn | Player | New Card | Fruit Counts A,B,G,P | Bell Pushes This Turn | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | A 5 | 5,0,0,0 | 1 | 1 |
| 2 | 1 | B 2 | 5,2,0,0 | 1 | 2 |
| 3 | 2 | B 3 | 5,5,0,0 | 2 | 4 |
| 4 | 0 | G 1 | 0,5,1,0 | 1 | 5 |
| 5 | 1 | P 5 | 0,3,1,5 | 1 | 6 |

The fourth turn demonstrates why replacement is necessary. Player 0's five apples disappear when the grape card is revealed.

A second example:

```
1
4 2
A 3
A 2
B 5
A 5
```

| Turn | Player | New Card | Fruit Counts A,B,G,P | Bell Pushes This Turn | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | A 3 | 3,0,0,0 | 0 | 0 |
| 2 | 1 | A 2 | 5,0,0,0 | 1 | 1 |
| 3 | 0 | B 5 | 2,5,0,0 | 1 | 2 |
| 4 | 1 | A 5 | 7,0,0,0 | 0 | 2 |

This trace confirms that the counters describe only visible cards. The first apple card is removed on turn three, and the second player's apple card is replaced on turn four.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each turn performs a constant number of updates and checks four fruit counters. |
| Space | O(K) | We store one current card for each player. |

The largest input contains 100 test cases with 100 turns each, so the total number of simulated turns is small. The constant-time update strategy easily fits within the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

# provided sample
assert run("""1
5 3
A 5
B 2
B 3
G 1
P 5
""") == "6\n", "sample 1"

# minimum size
assert run("""1
1 1
A 5
""") == "1\n", "single card"

# no bell
assert run("""1
3 2
A 1
B 1
G 1
""") == "0\n", "no fruit reaches five"

# replacement case
assert run("""1
2 1
A 5
A 5
""") == "2\n", "replacement instead of accumulation"

# multiple fruits at once
assert run("""1
3 3
A 5
B 5
G 5
""") == "3\n", "multiple simultaneous pushes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One player with one card | 1 | Minimum-size input handling |
| Small cards with totals below five | 0 | Avoiding false positives |
| Same player revealing two cards of five apples | 2 | Correct replacement logic |
| Three fruit types reaching five | 3 | Counting every valid fruit type |

## Edge Cases

The replacement case is handled because the algorithm stores exactly one card per player. For:

```
1
2 1
A 5
A 5
```

the first turn adds five apples and the answer becomes one. The second turn removes the old five apples, adds the new five apples, and adds one more bell push. The final answer is two.

The multiple-fruit case is handled by checking all four counters instead of stopping after finding one match. For:

```
1
3 3
A 5
B 5
G 5
```

the counters become five for apples, bananas, and grapes. Each counter contributes separately, giving an answer of three.

The first-card case is handled by checking whether the player already owns a card before removing anything. For:

```
1
1 6
P 1
```

the player has no previous card, so the algorithm only adds one pear and correctly reports zero bell pushes.
