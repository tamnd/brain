---
title: "CF 2A - Winner"
description: "The game records a sequence of rounds. In each round, one player either gains or loses some number of points. At the end"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 2"
rating: 1500
weight: 2
solve_time_s: 69
verified: true
draft: false
---
## Solution
## Problem Understanding

The game records a sequence of rounds. In each round, one player either gains or loses some number of points. At the end, the player with the highest total score should win.

The tricky part appears when several players finish with the same highest score. In that situation, the winner is not chosen arbitrarily. Among all players whose final score equals the maximum value, we pick the one who reached that score first during the game.

The input is already given in chronological order, so the order of rounds matters. Each line contains a player's name and the score change for that round. Scores can become negative during the game, and a player can move above and below the final winning score multiple times.

The constraints are small enough that almost any reasonable implementation will pass. There are at most 1000 rounds, so even an $O(n^2)$ solution performs only about one million operations. That easily fits within the time limit. Still, the problem is less about optimization and more about correctly handling the tie-breaking rule.

The most common mistake is to decide the winner only from the final scores. Consider this input:

```
4
alice 5
bob 5
alice -2
bob -2
```

Both players finish with 3 points. Alice reached 3 first, because after her first move she already had 5. Bob reached 3 later. The correct answer is:

```
alice
```

A careless solution that only checks final totals cannot distinguish this case.

Another subtle case happens when a player reaches the target score early but does not finish with the maximum score.

```
5
alice 10
bob 3
alice -8
bob 5
bob 2
```

Final scores are:

```
alice = 2
bob = 10
```

Alice reached 10 first, but she is not eligible because her final score is not the maximum. The winner is:

```
bob
```

A wrong implementation might incorrectly pick the first player who ever touched the maximum score.

There is also an important interaction with negative values:

```
5
alice 2
bob 3
alice 3
bob -1
alice -2
```

Final scores:

```
alice = 3
bob = 2
```

The maximum final score is 3. Alice becomes the winner even though she temporarily had 5 earlier. The rule is based on reaching at least the final maximum score, not necessarily exactly matching it at the end of some round.

## Approaches

A brute-force solution can simulate the entire game and repeatedly recompute every player's score after each round. For every round, we could scan all previous rounds to determine current totals, then try to decide whether someone already qualifies as the winner.

This works because the constraints are tiny. With $n = 1000$, an $O(n^2)$ solution performs roughly one million updates, which is completely acceptable.

The problem with this approach is not performance but clarity. The tie-breaking condition depends on two different notions of score:

First, the final maximum score among all players.

Second, the earliest moment when a player who eventually achieves that maximum reached it during the game.

Trying to compute both at the same time becomes messy.

The cleaner observation is that the problem naturally splits into two passes.

In the first pass, we compute every player's final score. Once this pass ends, we know the maximum final score $mx$.

Now the tie-breaking rule becomes much simpler. We only care about players whose final score equals $mx$. Among those players, we want the first one whose running score became at least $mx$.

That leads to a very direct second pass. We replay the game in chronological order while maintaining running totals. As soon as a player satisfies both conditions:

1. Their final score equals $mx$.
2. Their running score is at least $mx$.

that player must be the answer.

The second condition uses "at least" rather than "equal" because a player may overshoot the target score before ending exactly at it later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all rounds and store them in a list because we need to process the game twice.
2. During the first pass, maintain a dictionary `final_score[name]` that stores each player's total score after all rounds.
3. After processing every round, compute the maximum final score `mx`.
4. Start a second pass through the rounds in chronological order. Maintain another dictionary `current_score[name]` representing scores during gameplay.
5. For each round, update that player's running score.
6. After updating the running score, check two conditions:

1. The player's final score equals `mx`.
2. The player's running score is at least `mx`.
7. The first player satisfying both conditions is the winner. Print their name and stop immediately.

The reason this works is that only players with final score `mx` are eligible to win. The second pass discovers who among them reached the target earliest because the rounds are processed in chronological order.

### Why it works

After the first pass, `mx` is the highest score achieved at the end of the game. Any player with a smaller final score cannot possibly win, regardless of how large their temporary score became earlier.

During the second pass, `current_score[name]` always equals that player's score after the current round. The first eligible player whose running total becomes at least `mx` is exactly the player who first reached the winning threshold during the game.

Since the rounds are processed in order, no later player could have reached the threshold earlier. That guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

rounds = []
final_score = {}

for _ in range(n):
    name, score = input().split()
    score = int(score)

    rounds.append((name, score))

    if name not in final_score:
        final_score[name] = 0

    final_score[name] += score

mx = max(final_score.values())

current_score = {}

for name, score in rounds:
    if name not in current_score:
        current_score[name] = 0

    current_score[name] += score

    if final_score[name] == mx and current_score[name] >= mx:
        print(name)
        break
```

The solution follows the two-pass structure directly.

The first loop stores every round and computes final totals. Keeping the rounds in a list is necessary because the second pass must replay the game in chronological order.

The dictionary `final_score` maps each player to their score after all rounds. Once the first pass finishes, `mx` becomes the winning final score.

The second loop reconstructs the game step by step. The dictionary `current_score` tracks scores during gameplay rather than final totals.

The order of operations matters. We first update the running score, then check whether the player qualifies. Checking before updating would shift every score by one round and produce incorrect answers.

The condition:

```
current_score[name] >= mx
```

is subtle but essential. Suppose the winning score is 5 and a player temporarily reaches 7 before ending at 5 later. They still count as having reached the target earlier.

Breaking immediately after finding the first valid player is correct because the rounds are processed chronologically.

## Worked Examples

### Example 1

Input:

```
3
mike 3
andrew 5
mike 2
```

First pass:

| Round | Player | Delta | Final Scores |
| --- | --- | --- | --- |
| 1 | mike | +3 | mike = 3 |
| 2 | andrew | +5 | mike = 3, andrew = 5 |
| 3 | mike | +2 | mike = 5, andrew = 5 |

The maximum final score is 5.

Second pass:

| Round | Player | Running Score | Eligible? |
| --- | --- | --- | --- |
| 1 | mike | 3 | No |
| 2 | andrew | 5 | Yes |

Output:

```
andrew
```

This trace shows why the second pass works. Both players finish with 5, but Andrew reaches 5 earlier in the game.

### Example 2

Input:

```
5
alice 10
bob 3
alice -8
bob 5
bob 2
```

First pass:

| Round | Player | Delta | Final Scores |
| --- | --- | --- | --- |
| 1 | alice | +10 | alice = 10 |
| 2 | bob | +3 | alice = 10, bob = 3 |
| 3 | alice | -8 | alice = 2, bob = 3 |
| 4 | bob | +5 | alice = 2, bob = 8 |
| 5 | bob | +2 | alice = 2, bob = 10 |

The maximum final score is 10.

Second pass:

| Round | Player | Running Score | Eligible? |
| --- | --- | --- | --- |
| 1 | alice | 10 | No, final score is only 2 |
| 2 | bob | 3 | No |
| 3 | alice | 2 | No |
| 4 | bob | 8 | No |
| 5 | bob | 10 | Yes |

Output:

```
bob
```

This example demonstrates the most important edge case. Reaching the maximum score during the game is not enough. The player must also finish with that maximum score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each round is processed twice |
| Space | O(n) | Dictionaries and stored rounds use linear space |

With at most 1000 rounds, the solution is comfortably within the limits. Even much slower approaches would pass, but the linear solution is cleaner and matches the structure of the problem naturally.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    rounds = []
    final_score = {}

    for _ in range(n):
        name, score = input().split()
        score = int(score)

        rounds.append((name, score))

        final_score[name] = final_score.get(name, 0) + score

    mx = max(final_score.values())

    current_score = {}

    for name, score in rounds:
        current_score[name] = current_score.get(name, 0) + score

        if final_score[name] == mx and current_score[name] >= mx:
            print(name)
            return

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run(
"""3
mike 3
andrew 5
mike 2
"""
) == "andrew", "sample 1"

# minimum input size
assert run(
"""1
alice 10
"""
) == "alice", "single round"

# tie resolved by earliest reach
assert run(
"""4
alice 5
bob 5
alice -2
bob -2
"""
) == "alice", "earliest reach wins"

# temporary high score should not matter
assert run(
"""5
alice 10
bob 3
alice -8
bob 5
bob 2
"""
) == "bob", "must finish with maximum"

# negative values and multiple crossings
assert run(
"""6
a 2
b 3
a 3
b 2
a -2
b -1
"""
) == "b", "running totals handled correctly"

# all players equal final score
assert run(
"""6
x 1
y 2
x 1
y 0
x 0
y 0
"""
) == "y", "first to reach maximum among tied players"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single round game | alice | Minimum input size |
| Tie with equal finals | alice | Earliest reach rule |
| Temporary high score | bob | Final score eligibility |
| Negative score transitions | b | Correct handling of decreases |
| Equal final totals | y | Chronological tie-breaking |

## Edge Cases

Consider the case where two players finish with the same score, but one reached it earlier:

```
4
alice 5
bob 5
alice -2
bob -2
```

Final scores are:

```
alice = 3
bob = 3
```

The maximum final score is 3.

During the second pass:

```
alice reaches 5 after round 1
bob reaches 5 after round 2
```

Both running scores are already at least 3 when they first appear, but Alice appears earlier chronologically. The algorithm immediately prints `alice`.

Now consider a player who temporarily leads but does not finish first:

```
5
alice 10
bob 3
alice -8
bob 5
bob 2
```

The maximum final score is 10. During replay, Alice reaches 10 first, but her final score is only 2. The condition:

```
final_score[name] == mx
```

rejects her correctly. Bob eventually reaches 10 and wins.

Finally, consider repeated crossings of the target score:

```
6
a 2
b 3
a 3
b 2
a -2
b -1
```

Final scores:

```
a = 3
b = 4
```

The winning final score is 4.

Replay:

```
a: 2
b: 3
a: 5
b: 5
```

When `b` reaches 5, the running score is at least 4 and the final score equals 4, so `b` wins immediately. The algorithm does not care that `a` exceeded 4 earlier because `a` did not finish with the winning total.
