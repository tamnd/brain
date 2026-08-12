---
title: "CF 102428H - Hold or Continue?"
description: "At every decision point, Catelyn has a permanent score C and a temporary turn total X. Hoster has permanent score H. Catelyn must choose between banking the current turn total or rolling the die again."
date: "2026-08-12T07:18:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 175
verified: true
draft: false
---

[CF 102428H - Hold or Continue?](https://codeforces.com/problemset/problem/102428/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

At every decision point, Catelyn has a permanent score `C` and a temporary turn total `X`. Hoster has permanent score `H`. Catelyn must choose between banking the current turn total or rolling the die again. The objective is not to maximize the immediate score, but the probability that Catelyn eventually reaches exactly 75 before Hoster does, assuming both players make optimal decisions.

If Catelyn holds, her score becomes `C + X`. If that is exactly 75, she wins immediately. If it is less than 75, Hoster gets the next turn. If Catelyn continues, a roll of 1 immediately passes the turn without changing either permanent score. A roll from 2 through 6 increases `X`. If the new total would make `C + X` exceed 75, that turn is lost instead of being scored.

There are at most 74 relevant permanent scores for a player before reaching 75, and the turn total is also bounded by the distance to 75. The official problem page gives a 5 second time limit and 1024 MB memory limit. These bounds are generous in absolute terms, but the stochastic game has cyclic dependencies between the two players, so a straightforward recursive search is not enough. The small target value of 75 is the key reason a full dynamic program over score pairs is possible.

The first subtle case is an exact hit. For example,

```
1
73 0 2
```

must produce `H`. Holding scores exactly 75 and wins immediately. A careless implementation that treats holding merely as "pass the turn to the opponent" would incorrectly lose this winning transition.

The second subtle case is reaching 74. Consider

```
1
72 0 2
```

If Catelyn holds, her score becomes 74. She can never reach exactly 75 because every non-1 roll adds at least 2, so this decision has zero eventual winning probability. A careless implementation might treat 74 as an ordinary unfinished score and allow a future roll of 1 or some artificial increment to reach 75.

The third subtle case is a roll that busts the turn. If Catelyn has `C = 70` and `X = 4`, a further roll of 2 makes the temporary total 6 and the permanent score would be 76. That outcome scores nothing and passes the turn. It is not a state with score 76, and treating it as one corrupts the recurrence.

The fourth subtle case is the cyclic dependency between the players. Even after all temporary turn states are ordered by decreasing `X`, the value at the beginning of Catelyn's turn depends on the beginning-of-turn value when Hoster is playing. A plain acyclic DP cannot resolve those two values independently.

## Approaches

A direct brute-force approach would expand the entire game tree. At every roll there are six possible outcomes, and after every non-1 outcome there are two choices, hold or continue. The game is not even guaranteed to terminate after a fixed number of rolls, because players can repeatedly roll 1 or bust without changing their scores. If we artificially stop after `D` rolls, the number of roll sequences alone is `6^D`. For `D = 20`, that is about `3.66 × 10^15` leaves, before considering the strategy choices. So exhaustive simulation cannot give an exact solution.

A more structured approach is dynamic programming. Let `dp[c][h][x]` be Catelyn's winning probability when the player whose turn it is has score `c`, the opponent has score `h`, and the current turn total is `x`. Once the probability of the opponent's next turn is known, the value of every temporary total can be calculated from large `x` down to small `x`, because continuing only moves `x` upward.

The difficulty is the state with `x = 0`. Let `A = dp[c][h][0]`. After a hold or a roll of 1, the game switches to the opponent, so we also need `dp[h][c][0]`. This creates a cycle between the two beginning-of-turn states.

The key observation is that the game is zero-sum. Starting from two ordinary, nonterminal score states, exactly one player eventually wins with probability 1, so

`dp[c][h][0] + dp[h][c][0] = 1`.

Thus, instead of guessing two unknown probabilities, we only need to find one value `A`. If we temporarily guess that Catelyn's winning probability at the beginning of the turn is `A`, then Hoster's corresponding probability is `1 - A`. With that value fixed, all of Catelyn's temporary turn states can be computed deterministically from larger turn totals to smaller ones. This gives a function `F(A)`, where `F(A)` is the probability obtained by actually rolling the first die under the optimal decisions.

The true value satisfies

`A = F(A)`.

Because the value obtained from the turn is monotone with respect to the guessed opponent probability, we can find this fixed point by binary search. The small score limit makes this practical. We process score pairs in decreasing order of `c + h`, so whenever a hold moves the current permanent score from `c` to `c + x`, the required beginning-of-turn state has a strictly larger score sum and has already been computed.

This gives a clean progression from the brute force to the final method. The brute force works because every possible future is represented explicitly, but the tree grows exponentially and may not terminate. Dynamic programming removes repeated subtrees, while the fixed-point observation removes the remaining two-state cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(6^D)` for a `D`-roll truncation | `O(D)` with DFS | Too slow and not exact |
| Optimal | `O(75^3 log(1/ε))` | `O(75^2)` | Accepted |

## Algorithm Walkthrough

1. Define `dp[c][h]` as the probability that the player whose turn it is wins when their permanent score is `c` and the opponent's permanent score is `h`, with an empty temporary turn.

The game is symmetric, so for every nonterminal pair we have `dp[c][h] = 1 - dp[h][c]`. Equal scores consequently have value exactly `0.5`.
2. Process all pairs `(c, h)` in decreasing order of `c + h`.

Suppose we are solving a pair with total score `c + h`. If Catelyn holds after accumulating `x > 0`, her new score is `c + x`, so the opponent's beginning-of-turn state has score sum `h + c + x`, which is strictly larger. That state has already been computed.
3. For a fixed guess `A` for `dp[c][h]`, use `1 - A` as the opponent's beginning-of-turn winning probability.

We now know what happens whenever the current turn ends. A roll of 1, or a roll that busts the turn, gives the opponent the next turn, so its value for the current player is `1 - (1 - A) = A` when the opponent's state is represented by its own winning probability. More directly in the implementation, if the opponent's probability of winning is `p`, every immediate turn loss has value `1 - p`.
4. Compute the temporary turn values from the largest possible total down to 2.

Let `v[x]` be the optimal winning probability after the current player has accumulated exactly `x` points in the turn. Holding gives `1 - dp[h][c+x]`, except when `c+x = 75`, where holding wins immediately and has value 1.

Continuing gives the average of six outcomes. The roll of 1 gives `1 - p`. Rolls from 2 through 6 either move to `v[x+d]` when the resulting score does not exceed 75, or give `1 - p` when the turn busts.

Therefore,

`v[x] = max(hold, continue)`.

Since every `continue` transition goes to a larger temporary total, descending `x` makes this recurrence acyclic.
5. After all temporary states have been calculated, evaluate the beginning of the turn.

Catelyn must roll once. The result 1 ends the turn immediately. Each result from 2 through 6 either reaches one of the already computed `v[d]` states or busts. Their average is the value produced by the current guess.
6. Binary-search the beginning-of-turn probability.

Let the current guess be `A`. Compute the resulting probability `F(A)`. If `F(A) > A`, the guess is too small, so move the lower bound upward. Otherwise move the upper bound downward.

Fifty iterations reduce the numerical interval to far below the required `10^-5` separation between the two actions.
7. Store the resulting value for the score pair.

For `c < h`, store the computed value in `dp[c][h]` and its complement in `dp[h][c]`. For `c = h`, store `0.5` directly.
8. After the complete table is available, answer each query by reconstructing the temporary turn values for its `(C, H)` pair.

The hold value is `1` when `C + X = 75`, otherwise it is `1 - dp[H][C+X]`. The continue value is the average over the six possible next rolls, using the precomputed temporary turn values and treating every bust as an immediate turn loss. Output `H` when the hold value is larger, and `C` otherwise.

The invariant behind the computation is that when solving `(c, h)`, every permanent-score state required by a hold has a strictly larger score sum and is already exact. The only unresolved dependency is the opponent's beginning-of-turn probability, and the symmetry relation reduces that dependency to one scalar. Binary search converges to the unique fixed point, so the temporary values computed from it are exactly the optimal values for that score pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_SCORE = 73
TARGET = 75

def solve(data):
    it = iter(data.split())
    q = int(next(it))
    queries = []

    for _ in range(q):
        c = int(next(it))
        h = int(next(it))
        x = int(next(it))
        queries.append((c, h, x))

    # dp[c][h] = probability that the player to move wins
    # with permanent scores c and h and an empty turn.
    #
    # Columns 74 and 75 are useful boundary states:
    # dp[c][74] = 1 for c < 74, because the opponent at 74
    # can never reach exactly 75.
    # dp[c][75] = 0 because the opponent has already won.
    dp = [[0.0] * 76 for _ in range(74)]

    for c in range(74):
        dp[c][74] = 1.0
        dp[c][75] = 0.0

    def turn_value(c, h, opponent_win):
        """
        Compute the optimal value of the current turn when:
          current permanent score = c
          opponent permanent score = h
          opponent's beginning-of-turn win probability = opponent_win

        Returns the beginning-of-turn value for the current player.
        """
        max_x = TARGET - c
        lose_turn = 1.0 - opponent_win

        v = [0.0] * (max_x + 8)
        suffix = [0.0] * (max_x + 9)

        # Reaching exactly 75 means the player can hold and win.
        v[max_x] = 1.0
        suffix[max_x] = 1.0

        row = dp[h]

        for x in range(max_x - 1, 1, -1):
            # Holding scores c + x.
            hold = 1.0 - row[c + x]

            # Continue:
            # roll 1 is always a turn loss.
            # Rolls 2..6 either reach a known state or bust.
            left = x + 2
            right = min(x + 6, max_x)

            if left <= right:
                known = right - left + 1
                future = suffix[left] - suffix[right + 1]
            else:
                known = 0
                future = 0.0

            continue_value = (
                future + (6 - known) * lose_turn
            ) / 6.0

            v[x] = max(hold, continue_value)
            suffix[x] = suffix[x + 1] + v[x]

        # First roll of a new turn.
        left = 2
        right = min(6, max_x)

        if left <= right:
            known = right - left + 1
            future = suffix[left] - suffix[right + 1]
        else:
            known = 0
            future = 0.0

        return (future + (6 - known) * lose_turn) / 6.0

    # Solve score pairs from larger c+h to smaller c+h.
    for total in range(146, -1, -1):
        lo_c = max(0, total - 73)
        hi_c = min(73, total)

        for c in range(lo_c, hi_c + 1):
            h = total - c

            if c > h:
                continue

            if c == h:
                dp[c][h] = 0.5
                continue

            # We solve for A = dp[c][h].
            # The swapped state has value 1-A.
            lo = 0.0
            hi = 1.0

            for _ in range(50):
                mid = (lo + hi) * 0.5

                # If dp[c][h] = mid, then the opponent's
                # beginning-of-turn probability is 1-mid.
                got = turn_value(c, h, 1.0 - mid)

                if got > mid:
                    lo = mid
                else:
                    hi = mid

            a = (lo + hi) * 0.5
            dp[c][h] = a
            dp[h][c] = 1.0 - a

    def turn_states(c, h, opponent_win):
        """
        Same recurrence as turn_value, but keeps all temporary
        turn states because queries need v[X].
        """
        max_x = TARGET - c
        lose_turn = 1.0 - opponent_win

        v = [0.0] * (max_x + 8)
        suffix = [0.0] * (max_x + 9)

        v[max_x] = 1.0
        suffix[max_x] = 1.0

        row = dp[h]

        for x in range(max_x - 1, 1, -1):
            hold = 1.0 - row[c + x]

            left = x + 2
            right = min(x + 6, max_x)

            if left <= right:
                known = right - left + 1
                future = suffix[left] - suffix[right + 1]
            else:
                known = 0
                future = 0.0

            continue_value = (
                future + (6 - known) * lose_turn
            ) / 6.0

            v[x] = max(hold, continue_value)
            suffix[x] = suffix[x + 1] + v[x]

        return v

    answer = []

    for c, h, x in queries:
        opponent_win = dp[h][c]
        v = turn_states(c, h, opponent_win)

        if c + x == TARGET:
            hold = 1.0
        else:
            hold = 1.0 - dp[h][c + x]

        lose_turn = 1.0 - opponent_win

        left = x + 2
        right = min(x + 6, TARGET - c)

        if left <= right:
            known = right - left + 1
            future = sum(v[d] for d in range(left, right + 1))
        else:
            known = 0
            future = 0.0

        continue_value = (
            future + (6 - known) * lose_turn
        ) / 6.0

        answer.append("H" if hold > continue_value else "C")

    return "\n".join(answer)

if __name__ == "__main__":
    data = sys.stdin.buffer.read()
    print(solve(data))
```

The table `dp` stores only beginning-of-turn probabilities. Temporary totals are computed on demand because keeping every `(c, h, x)` value would increase memory without helping the score-pair computation.

The boundary column 75 represents an already completed game, so it has value zero for the player whose turn would otherwise begin. Column 74 is more subtle. If the opponent has 74 points, that opponent cannot ever score exactly 75, so the player with any score below 74 eventually wins with probability 1. These two boundary values prevent special cases from leaking into the main recurrence.

Inside `turn_value`, `max_x = 75 - c` is the largest temporary total that is still legal. The state at exactly `max_x` is worth 1 because holding reaches 75. Larger totals never appear as states, because those outcomes are busts and immediately pass the turn.

The `suffix` array is a small optimization. A continuation from `x` needs the five values for `x+2` through `x+6`. Since the recurrence is processed backwards, all of them are already known. A suffix sum reduces this part from five additions per state to constant time.

The binary search uses 50 iterations, which is much more accurate than the `10^-5` distinction required by the statement. Python integers do not overflow here, and all arithmetic involving probabilities uses double-precision floating point.

The final query evaluation deliberately compares the two action values directly instead of comparing against an arbitrary threshold. This matters because the correct decision depends on both the current turn total and the opponent's optimal response.

## Worked Examples

The supplied sample is

```
15 0 3
35 50 40
15 0 30
```

and the output is

```
C
H
H
```

For the first query, the relevant state is `(C,H,X) = (15,0,3)`. The precomputation has already determined every beginning-of-turn state with a larger score sum than `15`. The algorithm then reconstructs Catelyn's temporary turn values for score pair `(15,0)`.

| State | Meaning | Decision comparison | Result |
| --- | --- | --- | --- |
| `(15, 0, 3)` | Catelyn has 15 permanent points and 3 in the turn | `continue_value > hold` | `C` |
| `(35, 50, 40)` | Holding would make Catelyn's score 75 | `hold = 1` | `H` |
| `(15, 0, 30)` | Large turn total makes the risk of continuing dominant | `hold > continue_value` | `H` |

The second query exercises the exact-target boundary. Catelyn has 35 permanent points and 40 in the current turn, so holding gives exactly 75. No probability calculation can improve on an immediate win, making `H` forced.

For a second trace, consider the custom input

```
2
73 0 2
72 0 3
```

Both queries are exact hits.

| Query | C | H | X | C + X | Hold value | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 73 | 0 | 2 | 75 | 1 | `H` |
| 2 | 72 | 0 | 3 | 75 | 1 | `H` |

The first query also exercises the smallest possible temporary total that can win immediately. The second confirms that the implementation uses `C + X == 75`, rather than an off-by-one condition such as `C + X >= 75`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(75^3 log(1/ε))` | There are `O(75^2)` score pairs, each uses binary search with `O(log(1/ε))` iterations, and each iteration computes `O(75)` temporary states |
| Space | `O(75^2)` | The permanent-score DP table contains only the beginning-of-turn values |

With 50 binary-search iterations, the numerical precision is far tighter than the required `10^-5`. The largest dimension is only 75, so the roughly quadratic number of score pairs and linear temporary-state calculation fit comfortably within the official 5 second and 1024 MB limits.

## Test Cases

```python
import io
import sys

def solve(inp: str) -> str:
    data = inp.encode()
    it = iter(data.split())

    q = int(next(it))
    queries = []

    for _ in range(q):
        c = int(next(it))
        h = int(next(it))
        x = int(next(it))
        queries.append((c, h, x))

    TARGET = 75

    dp = [[0.0] * 76 for _ in range(74)]

    for c in range(74):
        dp[c][74] = 1.0
        dp[c][75] = 0.0

    def turn_value(c, h, opponent_win):
        max_x = TARGET - c
        lose_turn = 1.0 - opponent_win

        v = [0.0] * (max_x + 8)
        suffix = [0.0] * (max_x + 9)

        v[max_x] = 1.0
        suffix[max_x] = 1.0

        row = dp[h]

        for x in range(max_x - 1, 1, -1):
            hold = 1.0 - row[c + x]

            left = x + 2
            right = min(x + 6, max_x)

            if left <= right:
                known = right - left + 1
                future = suffix[left] - suffix[right + 1]
            else:
                known = 0
                future = 0.0

            cont = (future + (6 - known) * lose_turn) / 6.0
            v[x] = max(hold, cont)
            suffix[x] = suffix[x + 1] + v[x]

        left = 2
        right = min(6, max_x)

        if left <= right:
            known = right - left + 1
            future = suffix[left] - suffix[right + 1]
        else:
            known = 0
            future = 0.0

        return (future + (6 - known) * lose_turn) / 6.0

    for total in range(146, -1, -1):
        lo_c = max(0, total - 73)
        hi_c = min(73, total)

        for c in range(lo_c, hi_c + 1):
            h = total - c

            if c > h:
                continue

            if c == h:
                dp[c][h] = 0.5
                continue

            lo = 0.0
            hi = 1.0

            for _ in range(50):
                mid = (lo + hi) * 0.5
                got = turn_value(c, h, 1.0 - mid)

                if got > mid:
                    lo = mid
                else:
                    hi = mid

            a = (lo + hi) * 0.5
            dp[c][h] = a
            dp[h][c] = 1.0 - a

    def turn_states(c, h, opponent_win):
        max_x = TARGET - c
        lose_turn = 1.0 - opponent_win

        v = [0.0] * (max_x + 8)
        suffix = [0.0] * (max_x + 9)

        v[max_x] = 1.0
        suffix[max_x] = 1.0

        row = dp[h]

        for x in range(max_x - 1, 1, -1):
            hold = 1.0 - row[c + x]

            left = x + 2
            right = min(x + 6, max_x)

            if left <= right:
                known = right - left + 1
                future = suffix[left] - suffix[right + 1]
            else:
                known = 0
                future = 0.0

            cont = (future + (6 - known) * lose_turn) / 6.0
            v[x] = max(hold, cont)
            suffix[x] = suffix[x + 1] + v[x]

        return v

    ans = []

    for c, h, x in queries:
        opponent_win = dp[h][c]
        v = turn_states(c, h, opponent_win)

        if c + x == TARGET:
            hold = 1.0
        else:
            hold = 1.0 - dp[h][c + x]

        lose_turn = 1.0 - opponent_win

        left = x + 2
        right = min(x + 6, TARGET - c)

        if left <= right:
            known = right - left + 1
            future = sum(v[d] for d in range(left, right + 1))
        else:
            known = 0
            future = 0.0

        cont = (future + (6 - known) * lose_turn) / 6.0

        ans.append("H" if hold > cont else "C")

    return "\n".join(ans)

def run(inp: str) -> str:
    return solve(inp)

# Provided sample
assert run(
    """3
15 0 3
35 50 40
15 0 30
"""
) == "C\nH\nH", "sample 1"

# Minimum-size input and exact-hit boundary
assert run(
    """1
73 0 2
"""
) == "H", "minimum query, exact 75"

# Off-by-one boundary: 72 + 3 is exactly 75
assert run(
    """2
72 0 3
73 0 2
"""
) == "H\nH", "exact-hit boundaries"

# Equal permanent scores, including the maximum allowed input scores
assert run(
    """2
73 73 2
73 73 2
"""
) == "H\nH", "equal scores and maximum scores"

# Maximum Q
big_input = "1000\n" + "73 73 2\n" * 1000
assert run(big_input) == "\n".join(["H"] * 1000), "maximum Q"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 15 0 3 / 35 50 40 / 15 0 30` | `C H H` | Provided sample and both actions |
| `1 / 73 0 2` | `H` | Minimum query and immediate win |
| `2 / 72 0 3 / 73 0 2` | `H H` | Exact 75 boundary and off-by-one handling |
| `2 / 73 73 2 / 73 73 2` | `H H` | Equal scores and maximum score values |
| 1000 copies of `73 73 2` | 1000 lines of `H` | Maximum number of queries and repeated-state handling |

## Edge Cases

For an immediate exact win, the input

```
1
73 0 2
```

has `C + X = 75`. The query evaluator takes the exact-hit branch and sets the hold value to 1 without consulting another DP state. Continuing cannot improve on probability 1, so the answer is `H`.

For the unreachable score 74, consider the transition from

```
1
72 0 2
```

Holding creates permanent score 74. The corresponding opponent state is `dp[0][74] = 1`, meaning the opponent eventually wins because the player at 74 can never reach exactly 75. The hold value is consequently `1 - 1 = 0`. This boundary is represented explicitly in the DP table, so 74 is never accidentally treated as a valid predecessor of 75.

For a bust, suppose the current state has `C = 70` and `X = 4`. A roll of 6 makes the temporary total 10 and the would-be permanent score 80. The recurrence does not access `v[10]`, because that state is outside the legal range. Instead it contributes the value of losing the current turn, `1 - opponent_win`. The same treatment applies to every roll that exceeds 75.

For equal scores, the state is symmetric. If both players have the same permanent score and it is the beginning of a turn, swapping their identities changes nothing. Each player consequently has winning probability 0.5. The implementation uses this exact symmetry instead of running a binary search for a state that is already known.

For the cyclic dependency, when solving `(c,h)`, the binary search never attempts to recursively solve `(h,c)`. It uses the zero-sum identity `dp[h][c] = 1 - dp[c][h]`, and every other dependency created by holding has a strictly larger score sum. This is what converts the game from a cyclic stochastic process into a sequence of one-dimensional fixed-point computations.
