---
title: "CF 148D - Bag of mice"
description: "We have a bag containing white and black mice. The princess moves first, then the dragon, then the princess again, and so on. Whoever draws a white mouse immediately wins. If someone draws a black mouse, the game continues. There is one extra rule during the dragon’s turn."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 148
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 105 (Div. 2)"
rating: 1800
weight: 148
solve_time_s: 115
verified: true
draft: false
---

[CF 148D - Bag of mice](https://codeforces.com/problemset/problem/148/D)

**Rating:** 1800  
**Tags:** dp, games, math, probabilities  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a bag containing white and black mice. The princess moves first, then the dragon, then the princess again, and so on. Whoever draws a white mouse immediately wins. If someone draws a black mouse, the game continues.

There is one extra rule during the dragon’s turn. After the dragon draws a mouse, another random mouse jumps out of the bag because the remaining mice panic. The jumped mouse does not count as being drawn by anyone, so it cannot directly decide the winner.

The input gives the initial number of white mice `w` and black mice `b`. We must compute the probability that the princess eventually wins if every random choice is uniform.

The constraints allow up to 1000 white mice and 1000 black mice. A brute-force simulation over all possible game sequences explodes exponentially because every move branches into several future states. Even a recursive search without memoization would revisit the same `(w, b)` states many times. With only about one million distinct states, dynamic programming is feasible, but anything exponential is not.

The most dangerous part of this problem is correctly modeling the order of events during the dragon’s turn. A careless implementation often merges multiple probabilistic steps into one and accidentally counts impossible transitions.

Consider the input:

```
1 1
```

The princess draws first. She wins immediately with probability `1/2`. If she draws the black mouse instead, the dragon gets the only remaining white mouse and wins. The correct answer is:

```
0.5
```

A wrong recurrence that ignores turn order may incorrectly produce `1`.

Another subtle case is:

```
0 5
```

There are no white mice at all, so the princess can never win. The answer must be:

```
0
```

Some recursive solutions accidentally divide by zero here because they try to compute probabilities involving white mice that do not exist.

A third tricky case is:

```
2 0
```

The princess immediately draws a white mouse with probability `1`, so the answer is:

```
1
```

Transitions involving the dragon should never be evaluated in this state because the game already ends on the princess’s first move.

## Approaches

The brute-force approach is to recursively simulate every possible sequence of draws and jumps. From a state `(w, b)`, we branch on whether the princess draws white or black, then branch again on the dragon’s draw, then again on the mouse that jumps away.

This recursive process is mathematically correct because every game outcome corresponds to exactly one path in the recursion tree. The problem is the number of paths. In the worst case, each turn creates multiple branches, and the game length can be up to 2000 events. The number of states visited without memoization becomes enormous, far beyond what fits in 2 seconds.

The key observation is that the future only depends on how many white and black mice remain. The exact history does not matter. If two different sequences lead to the same `(w, b)` configuration at the princess’s turn, the probability of eventual victory from that point onward is identical.

That makes this a classic dynamic programming problem on states.

Define `dp[w][b]` as the probability that the princess wins when it is her turn and the bag currently contains `w` white mice and `b` black mice.

From this state, there are only a few possibilities.

If the princess draws a white mouse immediately, she wins.

If she draws a black mouse, the dragon moves next. For the princess to survive the dragon’s turn, the dragon must also draw a black mouse. After that, one additional mouse jumps away. Depending on whether the jumped mouse is white or black, we transition to another smaller state.

Every transition strictly decreases the total number of mice, so we can compute states bottom-up.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential recursion tree | Too slow |
| Optimal Dynamic Programming | O(w × b) | O(w × b) | Accepted |

## Algorithm Walkthrough

1. Define `dp[i][j]` as the probability that the princess wins when it is her turn with `i` white mice and `j` black mice remaining.
2. Initialize the base cases.

If there are no white mice, the princess cannot ever win:

```
dp[0][j] = 0
```

If there are no black mice, the princess certainly draws white immediately:

```
dp[i][0] = 1
```
3. Iterate over all states `(i, j)` with `i >= 1` and `j >= 1`.
4. Compute the probability that the princess instantly wins on her own draw.

She picks uniformly among all mice, so:

```
win_now = i / (i + j)
```
5. Compute the probability that the princess first draws a black mouse.

```
princess_black = j / (i + j)
```
6. After the princess removes one black mouse, the dragon acts on a bag containing `i` white and `j - 1` black mice.

For the princess to still have a chance, the dragon must draw a black mouse. If the dragon draws white, the dragon immediately wins.

The probability of the dragon drawing black is:

```
dragon_black = (j - 1) / (i + j - 1)
```
7. After the dragon draws black, another mouse jumps out.

At that moment, the bag contains `i` white and `j - 2` black mice.

There are two possibilities.

If a white mouse jumps out:

```
probability = i / (i + j - 2)
next state = dp[i - 1][j - 2]
```

If a black mouse jumps out:

```
probability = (j - 2) / (i + j - 2)
next state = dp[i][j - 3]
```
8. Add all valid transitions together.

The full recurrence becomes:

```
dp[i][j] =
    i / (i + j)
    +
    (j / (i + j))
    × ((j - 1) / (i + j - 1))
    × (
        (i / (i + j - 2)) × dp[i - 1][j - 2]
        +
        ((j - 2) / (i + j - 2)) × dp[i][j - 3]
      )
```

1. Carefully check bounds before accessing states like `j - 2` or `j - 3`.

### Why it works

The recurrence exhaustively partitions all possible outcomes from a state `(i, j)`.

Either the princess wins immediately by drawing white, or she draws black. In the second case, the only surviving paths are the ones where the dragon also draws black. After that, the jumped mouse determines the next reduced state.

Every transition probability is multiplied by the probability of reaching that transition, and all disjoint possibilities are summed. Since every move strictly decreases the number of mice, the DP eventually reaches base states where the answer is already known.

## Python Solution

```python
import sys
input = sys.stdin.readline

w, b = map(int, input().split())

dp = [[0.0] * (b + 1) for _ in range(w + 1)]

for i in range(1, w + 1):
    dp[i][0] = 1.0

for i in range(1, w + 1):
    for j in range(1, b + 1):
        total = i + j

        # Princess draws white immediately
        ans = i / total

        # Princess draws black
        if j >= 1:
            princess_black = j / total

            # Dragon draws black
            if j >= 2:
                dragon_black = (j - 1) / (total - 1)

                survive_prob = princess_black * dragon_black

                remaining = total - 2

                # A white mouse jumps out
                if i >= 1:
                    ans += (
                        survive_prob
                        * (i / remaining)
                        * dp[i - 1][j - 2]
                    )

                # A black mouse jumps out
                if j >= 3:
                    ans += (
                        survive_prob
                        * ((j - 2) / remaining)
                        * dp[i][j - 3]
                    )

        dp[i][j] = ans

print("{:.9f}".format(dp[w][b]))
```

The DP table stores probabilities for every reachable state. Since every transition reduces the total number of mice, smaller states are already computed before larger ones need them.

The first base case sets `dp[i][0] = 1` because if only white mice remain, the princess wins instantly on her turn.

The recurrence directly mirrors the game process. The most delicate part is the dragon’s turn. After the princess removes a black mouse, the denominator changes because the bag size decreased. After the dragon removes another black mouse, the denominator changes again before the panic jump occurs.

Many wrong solutions accidentally reuse the same denominator for all stages. That produces incorrect probabilities because the bag size changes after every event.

Another subtle implementation detail is checking bounds before accessing `dp[i][j - 3]` or `dp[i - 1][j - 2]`. These states only exist when enough black mice remain.

Floating-point precision is sufficient because the problem only requires an error below `1e-9`.

## Worked Examples

### Example 1

Input:

```
1 3
```

DP transition trace:

| Step | Event | Probability | Next State |
| --- | --- | --- | --- |
| 1 | Princess draws white | 1/4 | Win |
| 2 | Princess draws black | 3/4 | Continue |
| 3 | Dragon draws black | 2/3 | Continue |
| 4 | White mouse jumps out | 1/2 | dp[0][1] = 0 |
| 5 | Black mouse jumps out | 1/2 | dp[1][0] = 1 |

Now compute:

```
dp[1][3]
= 1/4 + (3/4)*(2/3)*((1/2)*0 + (1/2)*1)
= 1/4 + 1/4
= 1/2
```

This example shows why the jumped mouse matters. If the white mouse jumps away, the princess loses all future chances.

### Example 2

Input:

```
2 1
```

DP transition trace:

| Step | Event | Probability | Next State |
| --- | --- | --- | --- |
| 1 | Princess draws white | 2/3 | Win |
| 2 | Princess draws black | 1/3 | Continue |
| 3 | Dragon draws white | 1 | Dragon wins |

Computation:

```
dp[2][1] = 2/3
```

This case demonstrates that sometimes the recursion stops immediately after the dragon’s draw because the dragon can directly win by drawing white.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(w × b) | Each DP state is computed once with constant work |
| Space | O(w × b) | The DP table stores one value per state |

The maximum table size is roughly `1001 × 1001`, which is about one million states. Each state performs only a few arithmetic operations, so the solution easily fits within the time limit and memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    w, b = map(int, input().split())

    dp = [[0.0] * (b + 1) for _ in range(w + 1)]

    for i in range(1, w + 1):
        dp[i][0] = 1.0

    for i in range(1, w + 1):
        for j in range(1, b + 1):
            total = i + j

            ans = i / total

            if j >= 2:
                survive = (j / total) * ((j - 1) / (total - 1))
                remaining = total - 2

                ans += survive * (i / remaining) * dp[i - 1][j - 2]

                if j >= 3:
                    ans += survive * ((j - 2) / remaining) * dp[i][j - 3]

            dp[i][j] = ans

    print("{:.9f}".format(dp[w][b]))

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
assert run("1 3\n") == "0.500000000", "sample 1"

# minimum size, no white mice
assert run("0 5\n") == "0.000000000", "no possible win"

# only white mice
assert run("5 0\n") == "1.000000000", "immediate win"

# small mixed case
assert abs(float(run("1 1\n")) - 0.5) < 1e-9, "balanced small case"

# another small case
assert abs(float(run("2 1\n")) - (2/3)) < 1e-9, "dragon immediately wins after black"

# larger boundary-style case
res = float(run("1000 1000\n"))
assert 0.0 <= res <= 1.0, "probability range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 5` | `0.000000000` | No white mice exist |
| `5 0` | `1.000000000` | Princess instantly wins |
| `1 1` | `0.500000000` | Smallest meaningful mixed state |
| `2 1` | `0.666666667` | Dragon can immediately win |
| `1000 1000` | Valid probability | Maximum constraints |

## Edge Cases

Consider the input:

```
0 5
```

The DP immediately uses the base case:

```
dp[0][5] = 0
```

There is no transition to evaluate because no white mouse exists in the bag. The princess cannot possibly win.

Now consider:

```
2 0
```

The algorithm sets:

```
dp[2][0] = 1
```

The dragon’s turn is never considered because the princess always draws white on her first move.

Finally, consider:

```
1 2
```

The princess wins immediately with probability `1/3`.

If she draws black first, the dragon draws from one white and one black mouse. The dragon survives only if he also draws black, probability `1/2`. Then the only remaining mouse is white and jumps away, leaving no white mice for the princess.

The recurrence computes:

```
dp[1][2]
= 1/3 + (2/3)*(1/2)*dp[0][0]
= 1/3
```

This case checks the subtle situation where the panic jump removes the final white mouse.
