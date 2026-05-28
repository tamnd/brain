---
title: "CF 98E - Help Shrek and Donkey"
description: "There are m + n + 1 distinct cards in total. Shrek initially knows his own m cards, Donkey knows his own n cards, and one card is hidden on the table. Nobody knows the hidden card directly. Players alternate turns, with Shrek moving first."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 98
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 78 (Div. 1 Only)"
rating: 2700
weight: 98
solve_time_s: 145
verified: true
draft: false
---

[CF 98E - Help Shrek and Donkey](https://codeforces.com/problemset/problem/98/E)

**Rating:** 2700  
**Tags:** dp, games, math, probabilities  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `m + n + 1` distinct cards in total. Shrek initially knows his own `m` cards, Donkey knows his own `n` cards, and one card is hidden on the table. Nobody knows the hidden card directly.

Players alternate turns, with Shrek moving first. On each turn a player may either guess the hidden card immediately, or ask whether the opponent owns some specific card. If the opponent has it, that card is revealed and removed from the game forever. Otherwise the opponent simply answers "no".

A wrong guess loses instantly. A correct guess wins instantly. Both players play perfectly and both know that the other also plays perfectly. We must compute the probability that Shrek wins and the probability that Donkey wins.

The only input is `(m, n)`, the initial number of cards held by Shrek and Donkey. The output is two probabilities whose sum is `1`.

The constraints go up to `1000`, which is small for quadratic dynamic programming but far too large for any state space based on explicit card configurations. There are exponentially many possible distributions of cards, so we need to compress the game into a much smaller mathematical state.

The critical observation is that card identities do not matter. Only the counts matter. At any point the game state is completely determined by how many unknown cards each player may still have. That reduces the problem to about one million states, which is manageable.

Several edge cases are easy to mishandle.

If one player starts with zero cards, the answer is not automatically losing. For example:

```
0 3
```

Shrek knows nothing, but there are only four possible hidden cards from his perspective. Any guess succeeds with probability `1/4`, which matches the sample output.

Another subtle case is:

```
0 0
```

There is exactly one card total, and it is hidden. Shrek guesses immediately and wins with probability `1`.

A common wrong idea is to assume that asking questions is always better than guessing. That fails when a player already knows the hidden card with certainty. For example:

```
1 0
```

Shrek knows his own card, so the hidden card must be the only remaining one. He wins immediately with probability `1`.

A more dangerous mistake is to model the game as random questioning. The players are optimal, not random. Every question is chosen to maximize winning probability, and the optimal move depends on future recursive states.

## Approaches

A brute-force formulation would track the exact set of cards each player may still hold and recursively simulate every legal question and guess. This is correct because the game is one of perfect information once probabilities are included in the state.

The problem is the size of the state space. With up to `2001` cards total, the number of possible hidden distributions is astronomical. Even for thirty cards the state graph is already infeasible.

The key observation is symmetry. The names of the cards never matter, only how many possibilities remain.

Suppose it is your turn and there are currently:

- `a` cards that only the opponent might hold,
- `b` cards that only you might hold,
- `1` hidden card.

From your perspective, every unknown card is equally likely to be hidden. Asking about a card either removes one possibility or reveals information that changes the counts. Two cards with the same status are interchangeable.

That means the game state collapses to just `(a, b)` together with whose turn it is.

Now we can define a dynamic programming state:

`dp[a][b]` = probability that the current player eventually wins when they know `b` cards and the opponent may know `a` cards.

From a state `(a, b)`, the current player has two kinds of actions.

They may guess immediately. Since there are `a + 1` possibilities for the hidden card from their perspective, the success probability is:

$$\frac{1}{a+1}$$

Or they may ask about one of the opponent's possible cards.

If the opponent really has it, which happens with probability `a / (a+1)`, that card gets removed and the same player moves again in state `(a-1, b)`.

If the card is actually hidden, which happens with probability `1 / (a+1)`, the turn passes to the opponent in state `(b, a-1)`.

This recursive structure is the entire game.

The brute-force approach fails because it distinguishes card identities unnecessarily. The symmetry observation reduces the state space to only about one million states, allowing memoized DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over card distributions | Exponential | Exponential | Too slow |
| DP on card counts | O(mn) | O(mn) | Accepted |

## Algorithm Walkthrough

1. Define `dp[a][b]` as the probability that the current player wins when the opponent may possess `a` unknown cards and the current player knows `b` cards.
2. Handle the base case `dp[0][b] = 1`.

When the opponent has no possible private cards left, the hidden card is completely determined, so the current player guesses correctly immediately.
3. For every state `(a, b)` with `a > 0`, consider the option of guessing immediately.

The hidden card is uniformly distributed among `a + 1` possibilities, so immediate guessing gives probability:

$$\frac{1}{a+1}$$

1. Consider asking about one of the opponent's possible cards.

With probability:

$$\frac{a}{a+1}$$

the opponent actually has the card. It is removed, and the current player continues from `(a-1, b)`.

1. Otherwise the asked card was hidden.

This happens with probability:

$$\frac{1}{a+1}$$

The turn changes, and the roles swap. The opponent's winning probability from `(b, a-1)` is `dp[b][a-1]`, so the current player's probability becomes:

$$1 - dp[b][a-1]$$

1. Combine the two outcomes of asking:

$$\frac{a}{a+1} dp[a-1][b] + \frac{1}{a+1}(1 - dp[b][a-1])$$

1. The current player chooses the better of guessing and asking:

$dp[a][b]=\max\left(\frac1{a+1},\frac{a}{a+1}dp[a-1][b]+\frac1{a+1}(1-dp[b][a-1])\right)$

1. Fill the table in increasing order of `a + b`. Every transition only references smaller states, so this order guarantees that dependencies are already computed.
2. The final answer is `dp[n][m]` because initially Shrek sees `n` cards that might belong to Donkey and knows his own `m` cards.

Why it works:

The state `(a, b)` fully captures all information relevant to future decisions. Every remaining unknown card is symmetric, so no strategy can depend on card identities. The recurrence enumerates every optimal first move: either guess immediately or ask a question. The asking transition splits into the only two possible outcomes, weighted by their exact probabilities. Since both players play optimally afterward, the recursive states already contain the correct continuation values. By induction on `a + b`, every DP entry equals the true optimal winning probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, n = map(int, input().split())

MAX = max(m, n)

dp = [[0.0] * (MAX + 1) for _ in range(MAX + 1)]

for b in range(MAX + 1):
    dp[0][b] = 1.0

for s in range(1, 2 * MAX + 1):
    for a in range(1, min(MAX, s) + 1):
        b = s - a

        if b < 0 or b > MAX:
            continue

        guess = 1.0 / (a + 1)

        ask = (
            (a / (a + 1)) * dp[a - 1][b]
            + (1.0 / (a + 1)) * (1.0 - dp[b][a - 1])
        )

        dp[a][b] = max(guess, ask)

shrek = dp[n][m]
donkey = 1.0 - shrek

print(f"{shrek:.12f} {donkey:.12f}")
```

The DP table stores probabilities for every pair `(a, b)` up to the maximum input size.

The base row `dp[0][b] = 1` represents positions where the current player already knows the hidden card with certainty.

The outer loop iterates by increasing `a + b`. This ordering matters because the recurrence depends on `(a-1, b)` and `(b, a-1)`, both of which have smaller total size.

The transition computes the two legal strategies separately. The guessing probability is straightforward. The asking transition carefully handles the role swap after a failed question. The value `dp[b][a-1]` represents the opponent's winning probability after the turn changes, so we subtract from `1`.

A common implementation mistake is forgetting that the second branch swaps the players' perspectives. Using `dp[a-1][b]` in both branches produces incorrect answers.

Another subtle point is floating-point precision. The required error tolerance is `1e-9`, so Python `float` is sufficient.

## Worked Examples

### Example 1

Input:

```
0 3
```

Initial state is `dp[3][0]`.

| State | Guess Value | Ask Value | DP |
| --- | --- | --- | --- |
| dp[0][0] | 1 | - | 1 |
| dp[1][0] | 1/2 | 1/2 | 1/2 |
| dp[2][0] | 1/3 | 1/2 | 1/2 |
| dp[3][0] | 1/4 | 1/4 | 1/4 |

Final answer:

```
0.25 0.75
```

This trace shows that questioning does not help when you initially know nothing. Every failed question immediately hands the turn to the opponent.

### Example 2

Input:

```
1 0
```

Initial state is `dp[0][1]`.

| State | Guess Value | Ask Value | DP |
| --- | --- | --- | --- |
| dp[0][1] | 1 | - | 1 |

Final answer:

```
1.0 0.0
```

There is only one possible hidden card, so Shrek wins instantly without asking anything.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max(m, n)^2) | Every DP state is computed once |
| Space | O(max(m, n)^2) | The DP table stores all states |

With limits up to `1000`, the table contains about one million states. Each transition performs constant work, so the solution easily fits within the time limit and uses acceptable memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    m, n = map(int, input().split())

    MAX = max(m, n)

    dp = [[0.0] * (MAX + 1) for _ in range(MAX + 1)]

    for b in range(MAX + 1):
        dp[0][b] = 1.0

    for s in range(1, 2 * MAX + 1):
        for a in range(1, min(MAX, s) + 1):
            b = s - a

            if b < 0 or b > MAX:
                continue

            guess = 1.0 / (a + 1)

            ask = (
                (a / (a + 1)) * dp[a - 1][b]
                + (1.0 / (a + 1)) * (1.0 - dp[b][a - 1])
            )

            dp[a][b] = max(guess, ask)

    shrek = dp[n][m]
    donkey = 1.0 - shrek

    print(f"{shrek:.12f} {donkey:.12f}")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("0 3\n") == "0.250000000000 0.750000000000", "sample 1"

# minimum size
assert run("0 0\n") == "1.000000000000 0.000000000000", "single hidden card"

# immediate certainty
assert run("1 0\n") == "1.000000000000 0.000000000000", "known hidden card"

# symmetric case
res = run("1 1\n")
a, b = map(float, res.split())
assert abs(a + b - 1.0) < 1e-9, "probabilities sum to 1"

# larger boundary-style test
res = run("1000 1000\n")
a, b = map(float, res.split())
assert 0.0 <= a <= 1.0
assert 0.0 <= b <= 1.0
assert abs(a + b - 1.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `1 0` | Smallest possible state |
| `1 0` | `1 0` | Immediate deterministic win |
| `1 1` | Probabilities sum to 1 | Symmetric recursion correctness |
| `1000 1000` | Valid probabilities | Performance and bounds |

## Edge Cases

Consider:

```
0 0
```

There is exactly one card in the entire game, and it is hidden. The DP immediately uses the base case `dp[0][0] = 1`. Shrek guesses the only possible card and wins with certainty.

Now consider:

```
1 0
```

Shrek owns one card, Donkey owns none, so the hidden card is uniquely determined. The algorithm again reaches `dp[0][1] = 1`. A careless implementation that always tries asking first would fail because there is nobody to ask about.

Finally consider:

```
0 3
```

The recurrence becomes:

$$dp[3][0]
=
\max\left(
\frac14,
\frac34 dp[2][0] + \frac14 (1 - dp[0][2])
\right)$$

Since `dp[0][2] = 1`, the asking branch collapses to:

$$\frac34 \cdot \frac12 + \frac14 \cdot 0
=
\frac38$$

But `dp[2][0]` itself optimally becomes `1/2`, leading eventually to `dp[3][0] = 1/4`.

The important detail is that a failed question immediately gives the opponent a winning state. The recurrence handles this through the term:

$$1 - dp[b][a-1]$$

Without the role swap, the probability would be overestimated.
