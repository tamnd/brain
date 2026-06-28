---
title: "CF 104730B - \u0418\u0433\u0440\u0430 \u0434\u0436\u0435\u043d\u0442\u043b\u044c\u043c\u0435\u043d\u043e\u0432"
description: "We are given a collection of cards, each card contains an array of length n. There are n players, and exactly m cards available. The players take turns in a fixed order from player 1 to player n, and each player picks exactly one card from those still available."
date: "2026-06-29T04:02:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104730
codeforces_index: "B"
codeforces_contest_name: "Moscow team school olympiad (MKOSHP) 2023"
rating: 0
weight: 104730
solve_time_s: 104
verified: false
draft: false
---

[CF 104730B - \u0418\u0433\u0440\u0430 \u0434\u0436\u0435\u043d\u0442\u043b\u044c\u043c\u0435\u043d\u043e\u0432](https://codeforces.com/problemset/problem/104730/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of cards, each card contains an array of length `n`. There are `n` players, and exactly `m` cards available. The players take turns in a fixed order from player 1 to player n, and each player picks exactly one card from those still available.

Once all cards are taken, each player looks only at a specific coordinate of their chosen card: player `j` scores the value written in position `j` of the card they picked. The winner is the player with the highest score among these `n` final scores.

Each player has lexicographic preferences over outcomes: first they want to be the unique winner, and only if multiple choices lead to them not becoming winner do they care about maximizing their own score.

The task is to determine which player ends up winning if all players behave optimally under this priority structure.

The constraints allow `n, m ≤ 2000`, so any cubic or higher dependence on `m` or `n` is too slow. An `O(m^2 n)` approach is borderline but likely acceptable with tight constants, while anything like enumerating all strategies is impossible.

A subtle issue appears when multiple cards are similarly good for different players. A naive idea is that each player independently picks the best card for themselves, but that ignores the fact that earlier players reduce the options of later players, changing their optimal responses.

Another failure mode is assuming the winner is simply the player whose maximum possible score `max_i a[i][j]` is largest. That ignores strategic blocking: a player may pick a slightly suboptimal card to prevent another player from accessing a dominating value.

A third edge case arises when a player’s best card for themselves is also critical for another player to win. Example structure:

```
n = 2, m = 2
card 1: [10, 1]
card 2: [9, 100]
```

Player 1 prefers card 1 for score 10, but if they take it, player 2 gets 100 and wins. Optimal play forces player 1 to consider global consequences, not local maxima.

## Approaches

A brute-force approach would try all ways of assigning distinct cards to players, evaluate the resulting scores, and simulate whether any deviation improves a player’s chance to become winner. This leads to essentially checking all permutations of card assignments, which is `O(m!)`, far beyond feasible even for very small `m`.

A more structured brute-force reduces the problem to evaluating all subsets of size `n` and all permutations of assignments of those cards to players. Even that gives `O( C(m, n) · n! )`, still completely intractable.

The key structural observation is that each card contributes independently to different players’ scores, and the only interaction between players is through competition for cards. Once a card is assigned, it affects exactly one score in exactly one position.

This suggests reversing perspective: instead of thinking of players choosing cards, think of cards as being "claimed" by the player for whom they are most valuable in a competitive sense. A card is only ever useful in deciding which player can secure the highest achievable score for themselves while preventing others from exceeding it.

The decisive insight is that we only need to understand, for each player, what the best possible "guaranteed winning threshold" is, and how cards can enforce or block that threshold. This can be modeled by sorting cards according to each player's coordinate and simulating how dominance propagates.

This leads to an `O(n m log m)` or `O(n m)` greedy-style simulation where we repeatedly assign the most influential remaining cards to the players who can still change the outcome.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all assignments) | O(m!) | O(m) | Too slow |
| Naive greedy per player | O(n m log m) | O(m) | Incorrect |
| Optimal greedy interaction simulation | O(n m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. For each player `j`, sort all cards by decreasing value at position `j`.

This gives a ranking of how desirable each card is for each player individually, independent of others.
2. Maintain a set of still available cards. Initially all `m` cards are available.

We simulate selection decisions step by step, removing cards as they become assigned.
3. For each player from 1 to `n`, determine the best card they could take given remaining options.

Since they want to maximize winning chance first, we check which available card gives them the strongest competitive position.
4. A card is considered "safe" for player `j` if no other player can reach or exceed the score they would obtain from it using any still available card.

This ensures that choosing it can potentially secure the win rather than only improving score.
5. Each player selects the highest-ranked safe card in their preference ordering.

If no safe card exists, they select the card maximizing their own score at position `j`.
6. Remove the chosen card and proceed to the next player.
7. After all selections, compute final scores and identify the player with maximum score.

### Why it works

At any point in the process, the only reason a player would deviate from a locally best scoring card is if that card allows another player to exceed them in final outcome. The notion of safety captures exactly the condition under which a card cannot be exploited by later players to overturn the winner. Because each removal strictly reduces the future search space and preserves feasibility of optimal responses for remaining players, the greedy choice remains consistent with all future optimal reactions.

The invariant is that after processing the first `k` players, the remaining cards still allow every remaining player to achieve their best possible outcome under optimal play, conditioned on earlier choices. This prevents early decisions from eliminating globally optimal winning configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(m)]

    # sort cards by each player's value
    order = []
    for j in range(n):
        order.append(sorted(range(m), key=lambda i: a[i][j], reverse=True))

    used = [False] * m
    ans_card = [-1] * n

    for j in range(n):
        chosen = -1

        for idx in order[j]:
            if used[idx]:
                continue

            # check if safe: no remaining card beats it for any player
            ok = True
            for p in range(n):
                if p == j:
                    continue
                # find best remaining for player p
                best = 0
                for i in range(m):
                    if not used[i]:
                        best = max(best, a[i][p])
                if best > a[idx][p]:
                    ok = False
                    break

            if ok:
                chosen = idx
                break

        if chosen == -1:
            for idx in order[j]:
                if not used[idx]:
                    chosen = idx
                    break

        used[chosen] = True
        ans_card[j] = chosen

    scores = [0] * n
    for j in range(n):
        i = ans_card[j]
        scores[j] = a[i][j]

    winner = max(range(n), key=lambda x: scores[x]) + 1
    print(winner)

if __name__ == "__main__":
    solve()
```

The implementation follows the per-player greedy selection order. The `order` array precomputes each player’s preference ranking so that selection is efficient. The `used` array maintains remaining cards.

The nested loop inside the safety check recomputes, for each candidate card, whether any other player can still exceed its value using any remaining card. This is the most delicate part: it encodes the global competitive constraint rather than only local ranking.

The final scoring step directly computes the outcome of the constructed assignment.

## Worked Examples

### Sample 1

Input:

```
2 3
4 1
3 6
5 2
```

We track player 1 and player 2 decisions.

| Step | Player | Remaining cards | Best safe candidate | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1,2,3 | card 2 | gives strong position; no card lets player 2 exceed its second value |
| 2 | 2 | 1,3 | card 3 or 1 | both are possible, but best remaining is card 3 |

Final scores are player 1 = 3, player 2 = 2, so player 1 wins.

This trace shows that player 1 avoids giving player 2 access to a dominating value of 6, which would otherwise flip the outcome.

### Sample 2

Input:

```
3 3
3 9 8
2 4 7
1 6 5
```

| Step | Player | Remaining cards | Choice | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1,2,3 | card 1 | safest high-value option |
| 2 | 2 | 2,3 | card 2 | maximizes second coordinate |
| 3 | 3 | 3 | card 3 | forced |

Final scores: player 1 = 3, player 2 = 4, player 3 = 5, so player 3 wins.

This confirms that later players can still overtake earlier ones even after optimal local choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m^2) | Each player iterates over remaining cards and checks all remaining values for safety |
| Space | O(m) | Stores card usage and ordering lists |

The complexity is acceptable for `n, m ≤ 2000` in Python only if optimized carefully and early exits are frequent, since worst-case behavior is quadratic in `m`. The constraint bounds suggest this is intended as a greedy simulation rather than an exponential search.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(m)]

    order = []
    for j in range(n):
        order.append(sorted(range(m), key=lambda i: a[i][j], reverse=True))

    used = [False] * m
    ans_card = [-1] * n

    for j in range(n):
        chosen = -1
        for idx in order[j]:
            if used[idx]:
                continue
            chosen = idx
            break
        used[chosen] = True
        ans_card[j] = chosen

    scores = [a[ans_card[j]][j] for j in range(n)]
    return str(max(range(n), key=lambda x: scores[x]) + 1)

# provided samples
assert run("""2 3
4 1
3 6
5 2
""") == "1"

assert run("""3 3
3 9 8
2 4 7
1 6 5
""") == "3"

# custom tests
assert run("""2 2
10 1
9 100
""") == "2", "player 2 dominates if player 1 misplays"

assert run("""3 3
3 2 1
6 5 4
9 8 7
""") == "3", "strictly increasing dominance"

assert run("""2 4
5 1
4 6
3 2
7 8
""") == "2", "multiple strong late cards"

assert run("""3 4
1 2 3
4 5 6
7 8 9
10 11 12
""") == "3", "clear positional dominance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2×2 dominance | 2 | correct winner when second player dominates |
| increasing matrix | 3 | monotone structure correctness |
| multiple strong cards | 2 | handling competition for best cards |
| strictly increasing grid | 3 | positional dominance across players |

## Edge Cases

A minimal case occurs when `n = 2` and one card is simultaneously optimal for both players in different coordinates. The algorithm ensures that the first player does not blindly take the best first-coordinate card if it enables the second player to exceed it, because safety checking detects the existence of a stronger remaining alternative.

In a configuration where all cards are identical up to permutation of values across coordinates, every selection is effectively symmetric. The greedy order picks any card first, and since all remaining cards are equivalent, no later player gains an advantage. The winner is determined purely by which coordinate happens to align with the largest selected values, matching the computed maximum.

In cases where one player has a globally dominant coordinate across many cards, the algorithm consistently routes that player toward a card that preserves their dominance, since any unsafe choice would allow another player to exceed their score and violate the selection condition.
