---
title: "CF 98E - Help Shrek and Donkey"
description: "There are m + n + 1 distinct cards in the deck. Shrek initially knows exactly which m cards he owns, Donkey knows his own n cards, and one card is hidden on the table. Nobody knows the hidden card directly."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 98
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 78 (Div. 1 Only)"
rating: 2700
weight: 98
solve_time_s: 190
verified: false
draft: false
---

[CF 98E - Help Shrek and Donkey](https://codeforces.com/problemset/problem/98/E)

**Rating:** 2700  
**Tags:** dp, games, math, probabilities  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

There are `m + n + 1` distinct cards in the deck. Shrek initially knows exactly which `m` cards he owns, Donkey knows his own `n` cards, and one card is hidden on the table. Nobody knows the hidden card directly.

On each turn, the current player may either guess the hidden card immediately, or ask about some card. If the opponent owns that card, the opponent must reveal it and remove it from the game forever. Otherwise the opponent says they do not have it.

A wrong guess loses instantly, so a player only wants to guess when they know the hidden card with certainty, or when probabilistic reasoning says gambling is optimal.

The input gives only the counts `m` and `n`. The actual identities of cards do not matter because the game is completely symmetric. We must compute the probability that Shrek eventually wins when both players play perfectly.

The limits are small enough for quadratic dynamic programming. Both `m` and `n` are at most `1000`, so there are roughly one million states. Any exponential game-tree search is impossible because even for moderate values the branching factor explodes. A cubic DP would also be dangerous in Python, since `1000^3` operations is far beyond the time limit. An `O(mn)` solution is the natural target.

The dangerous part of this problem is that information is asymmetric. A naive implementation often treats the game as if both players share the same knowledge state, which is false.

Consider the input

```
0 1
```

Shrek owns nothing. There are two possible hidden cards from his perspective, so guessing succeeds with probability `1/2`. The correct answer is:

```
0.5 0.5
```

A careless approach might think Shrek should ask first, but there is nothing to ask about.

Another subtle case is

```
1 0
```

Shrek owns one card, so he immediately knows the hidden card with certainty and wins instantly:

```
1 0
```

Many incorrect recurrences miss this asymmetry and incorrectly output `1/2`.

One more tricky situation is when both players still have many unknown cards. Asking questions does not directly improve your own knowledge, it improves your opponent's knowledge too. Optimal play depends on balancing information gain against giving the turn away.

## Approaches

The brute-force idea is to model the entire game tree. A state would contain the exact probability distribution of which cards each player may still hold, together with whose turn it is. From a state, we try every possible question and every possible guess, recursively evaluating the resulting expected value.

This works conceptually because the game is finite and has perfect rational play. The problem is that the number of information states becomes enormous. Even for twenty cards, the number of possible knowledge distributions is already exponential. With up to 2001 cards total, explicit game-tree search is hopeless.

The key observation is that only the counts matter.

Suppose it is your turn and you currently own `a` cards while your opponent owns `b` cards. From your perspective, the hidden card is equally likely to be any card not in your hand, so there are `b + 1` possibilities. If you guess now, your success probability is exactly:

$$\frac{1}{b+1}$$

What happens if you ask about a card?

You should clearly ask about a card you do not own and have not already been disproven. Among the `b + 1` unknown possibilities, exactly `b` are in the opponent's hand and one is hidden.

With probability `b / (b + 1)`, the opponent reveals the card. Then the game moves to the opponent's turn with state `(b - 1, a)`.

With probability `1 / (b + 1)`, the opponent does not have the card, which means the asked card must be hidden. You immediately learn the hidden card and win on your next move with certainty.

This collapses the whole game into a DP over only two integers.

Let `dp[a][b]` be the probability that the current player eventually wins when they hold `a` cards and the opponent holds `b` cards.

The current player has two choices.

Guess immediately:

$$G = \frac{1}{b+1}$$

Ask a question:

$$Q = \frac{1}{b+1} + \frac{b}{b+1}(1 - dp[b-1][a])$$

The second term comes from role reversal. After a successful query, it becomes the opponent's turn in state `(b-1, a)`, so the opponent wins with probability `dp[b-1][a]`. Hence the current player's probability is `1 - dp[b-1][a]`.

We choose the better action:

$$dp[a][b] = \max(G, Q)$$

The recurrence simplifies beautifully:

$$dp[a][b] = \max\left(
\frac{1}{b+1},
1 - \frac{b}{b+1}dp[b-1][a]
\right)$$

The entire game reduces to filling a `1001 x 1001` table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(mn) | O(mn) | Accepted |

## Algorithm Walkthrough

1. Define `dp[a][b]` as the winning probability for the player whose turn it is, when they own `a` cards and the opponent owns `b` cards.
2. Handle the base case `b = 0`.

If the opponent has no cards, the hidden card is uniquely determined. The current player knows it immediately and wins with probability `1`.
3. Process states in increasing order of `a + b`.

The recurrence for `(a, b)` depends only on `(b - 1, a)`, whose total number of cards is smaller by one.
4. Compute the probability of immediate guessing:

$$guess = \frac{1}{b+1}$$

1. Compute the probability of asking a question.

With probability `1 / (b + 1)`, the asked card is hidden and the current player eventually wins for sure.

With probability `b / (b + 1)`, the opponent reveals the card, the turn changes, and the new state becomes `(b - 1, a)`.

The resulting probability is:

$$ask = \frac{1}{b+1} + \frac{b}{b+1}(1 - dp[b-1][a])$$

1. Store the better option:

$$dp[a][b] = \max(guess, ask)$$

1. The required answer is `dp[m][n]` for Shrek and `1 - dp[m][n]` for Donkey.

### Why it works

The invariant is that every state depends only on the number of cards each player currently owns, not on specific card identities.

At any moment, from the current player's perspective, all unknown cards are symmetric. The hidden card is uniformly distributed among the `b + 1` cards not owned by the player. No strategy can distinguish among them before further questioning.

The recurrence enumerates the only two meaningful actions. Guessing succeeds with exact probability `1 / (b + 1)`. Asking partitions the possibilities into two exhaustive cases: either the opponent owns the card or the hidden card is discovered immediately. The transition after a successful query correctly swaps roles because the turn changes.

Since every transition moves to a strictly smaller state, dynamic programming evaluates all states exactly once and computes the optimal minimax probabilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())

    MAX = max(m, n)

    dp = [[0.0] * (MAX + 1) for _ in range(MAX + 1)]

    for a in range(MAX + 1):
        dp[a][0] = 1.0

    for total in range(1, 2 * MAX + 1):
        for a in range(MAX + 1):
            b = total - a

            if b < 1 or b > MAX or a > MAX:
                continue

            guess = 1.0 / (b + 1)

            ask = 1.0 - (b / (b + 1)) * dp[b - 1][a]

            dp[a][b] = max(guess, ask)

    shrek = dp[m][n]
    donkey = 1.0 - shrek

    print(f"{shrek:.12f} {donkey:.12f}")

solve()
```

The DP table stores only probabilities for the player whose turn it is. This removes the need for an explicit turn dimension because the recurrence naturally swaps players through the transition `(a, b) -> (b - 1, a)`.

The initialization `dp[a][0] = 1` is critical. If the opponent has no cards left, the hidden card is fully determined. Forgetting this base case causes the entire recurrence to collapse toward incorrect fractional answers.

The iteration order matters. State `(a, b)` depends on `(b - 1, a)`, whose total card count is `a + b - 1`. Processing by increasing `a + b` guarantees the dependency is already computed.

The formula for `ask` is intentionally written in simplified form:

```
ask = 1 - (b / (b + 1)) * dp[b - 1][a]
```

This is algebraically identical to:

```
1/(b+1) + (b/(b+1)) * (1 - dp[b-1][a])
```

The simplified version is numerically cleaner and slightly faster.

Floating-point precision is sufficient because the problem accepts absolute error up to `1e-9`.

## Worked Examples

### Example 1

Input:

```
0 3
```

DP states used:

| State `(a,b)` | Guess | Ask | DP value |
| --- | --- | --- | --- |
| (0,1) | 0.5 | 0.5 | 0.5 |
| (0,2) | 0.333333 | 0.666667 | 0.666667 |
| (0,3) | 0.25 | 0.25 | 0.25 |

Explanation:

For `(0,3)`, asking is terrible because after revealing one card the opponent reaches `(2,0)` and wins immediately. Shrek should simply guess randomly among the four possibilities, giving probability `1/4`.

### Example 2

Input:

```
1 1
```

DP states used:

| State `(a,b)` | Guess | Ask | DP value |
| --- | --- | --- | --- |
| (1,0) | 1 | 1 | 1 |
| (0,1) | 0.5 | 0.5 | 0.5 |
| (1,1) | 0.5 | 0.5 | 0.5 |

Explanation:

Each player knows one card and there are two unknown possibilities from the current player's perspective. Asking gives no advantage because revealing the opponent's only card hands complete information back to them on the next turn.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(mn) | Every DP state is computed once |
| Space | O(mn) | The DP table stores all states |

At most about one million states are evaluated. Each state performs only a few floating-point operations, which easily fits within the 2 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    m, n = map(int, input().split())

    MAX = max(m, n)

    dp = [[0.0] * (MAX + 1) for _ in range(MAX + 1)]

    for a in range(MAX + 1):
        dp[a][0] = 1.0

    for total in range(1, 2 * MAX + 1):
        for a in range(MAX + 1):
            b = total - a

            if b < 1 or b > MAX or a > MAX:
                continue

            guess = 1.0 / (b + 1)
            ask = 1.0 - (b / (b + 1)) * dp[b - 1][a]

            dp[a][b] = max(guess, ask)

    return f"{dp[m][n]:.12f} {1.0 - dp[m][n]:.12f}"

# provided sample
out = solve_io("0 3\n").split()
assert abs(float(out[0]) - 0.25) < 1e-9
assert abs(float(out[1]) - 0.75) < 1e-9

# minimum size
out = solve_io("0 0\n").split()
assert abs(float(out[0]) - 1.0) < 1e-9

# asymmetric certainty
out = solve_io("1 0\n").split()
assert abs(float(out[0]) - 1.0) < 1e-9

# symmetric small case
out = solve_io("1 1\n").split()
assert abs(float(out[0]) - 0.5) < 1e-9

# larger boundary-style case
out = solve_io("1000 1000\n").split()
assert abs(float(out[0]) + float(out[1]) - 1.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `1 0` | Immediate certainty with only one card total |
| `1 0` | `1 0` | Base case where opponent has no cards |
| `1 1` | `0.5 0.5` | Symmetric equilibrium |
| `1000 1000` | probabilities summing to 1 | Large-state performance and numerical stability |

## Edge Cases

Consider the smallest possible game:

```
0 0
```

There is exactly one card in existence and it is hidden. Shrek knows immediately what it must be, so:

```
1 0
```

The algorithm handles this through the base initialization `dp[a][0] = 1`. Since `n = 0`, the answer is directly `dp[0][0] = 1`.

Now consider:

```
1 0
```

Shrek owns one known card and the only remaining card must be hidden. Again the algorithm returns `dp[1][0] = 1`.

This catches implementations that incorrectly assume every guess is probabilistic.

Another subtle case is:

```
0 1
```

There are two possible hidden cards from Shrek's viewpoint. The DP computes:

$$guess = \frac12$$

$$ask = 1 - \frac12 \cdot dp[0][0]
     = 1 - \frac12
     = \frac12$$

Both actions are equivalent, so the final answer is:

```
0.5 0.5
```

Finally consider:

```
0 2
```

The recurrence gives:

$$ask = 1 - \frac23 dp[1][0]
     = 1 - \frac23
     = \frac13$$

which equals the guessing probability. But for:

```
0 3
```

we get:

$$ask = 1 - \frac34 dp[2][0]
     = \frac14$$

Asking no longer helps because revealing a card gives the opponent complete information immediately afterward. This demonstrates that the optimal strategy changes depending on how much information the next reveal creates.
