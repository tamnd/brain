---
title: "CF 102860C - Game"
description: "Edit The game consists of independent rounds. At the start of every round, the score becomes n. Each generator value represents one move: Petya tries to subtract that value from the current score, but only successful subtractions are applied."
date: "2026-07-25T14:19:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102860
codeforces_index: "C"
codeforces_contest_name: "2020-2021 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 20)"
rating: 0
weight: 102860
solve_time_s: 36
verified: true
draft: false
---

[CF 102860C - Game](https://codeforces.com/problemset/problem/102860/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
Edit

# Problem Understanding

The game consists of independent rounds. At the start of every round, the score becomes `n`. Each generator value represents one move: Petya tries to subtract that value from the current score, but only successful subtractions are applied. When the score reaches exactly zero, the current round is completed and the next move, if it exists, starts from a fresh score of `n`.

The input gives the number of moves, the initial score of a round, and the whole sequence of generator outputs. The task is to replay these moves and determine how many rounds were fully completed and what score remained after the final recorded move. If the final move finishes a round, there is no new round started afterwards, so the final score is zero.

The limits are small enough for direct simulation. There are at most `100000` moves, so an algorithm that processes each move once performs only about `100000` operations. Any approach that tries to build all possible round divisions or repeatedly scans the sequence would add unnecessary work, but linear time is easily within the limit.

The main edge cases come from correctly handling failed subtractions and the exact moment a round ends. For example, with input

```
1 5
7
```

the output is

```
0
5
```

because `7` cannot be subtracted from `5`, so the score stays unchanged. A careless solution that always subtracts the generator value would produce an invalid negative score.

Another case is

```
1 5
5
```

with output

```
1
0
```

because the only move completes the round. A common mistake is to reset the score to `5` immediately after reaching zero, which would incorrectly report the final score as the starting score of a new round.

A third boundary case is

```
3 5
2 2 2
```

with output

```
0
1
```

The moves change the score as `5 -> 3 -> 1 -> 1`, because the last subtraction is impossible. A solution that counts every generator value as progress toward a completed round would overcount.

## Approaches

The most direct solution is to simulate the game exactly. We keep the current score and the number of completed rounds. For every generator value, we check whether subtracting it keeps the score non-negative. If it does, we apply the subtraction. When the score becomes zero, one full round has finished, so we increase the answer and prepare the score for the next move.

The brute force interpretation is actually the same as the optimal method here. There is no hidden need for a faster mathematical shortcut because the game state changes only after each move, and the number of moves is limited. A hypothetical approach that tries every possible partition of the sequence into rounds would explore an enormous number of possibilities, but simulation avoids that completely by following the only valid order of events.

The observation that unlocks the solution is that the generator sequence is already the complete history of the game. There are no choices to make. The next state depends only on the current score and the next generator value, so one pass over the sequence is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Accepted |
| Optimal | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the current score to `n` and the completed round counter to zero. The score represents Petya's state before processing the first recorded move.
2. Process each generator value in the order it appears. If the value is not larger than the current score, subtract it from the score. Otherwise, ignore it because the rules do not allow the score to become negative.
3. After every successful subtraction, check whether the score became zero. If it did, increase the completed round counter and restore the score to `n` for future moves. The restoration represents the beginning of the next round, but it does not affect the final answer if the current move was the last one because the required final score in that situation is zero.
4. After all moves are processed, print the number of completed rounds and the current score. If the last move ended a round, the restoration step should not happen after the final move, so the final score remains zero.

The implementation needs one small adjustment for the last step. We can restore the score immediately when a round ends because after the loop we only need the score at the moment the game stopped. To preserve that information, the code checks whether the current move is the final move before resetting.

Why it works: During the simulation, the stored score is always the exact score Petya has after all processed moves. A move is applied precisely when the game rules allow it, and a completed round is counted exactly when the score reaches zero. Since every recorded move is processed once and in the original order, the final stored state matches the real game state.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())
    a = list(map(int, input().split()))

    score = n
    rounds = 0

    for i, x in enumerate(a):
        if x <= score:
            score -= x

        if score == 0:
            rounds += 1
            if i != k - 1:
                score = n

    print(rounds)
    print(score)

if __name__ == "__main__":
    solve()
```

The variables `score` and `rounds` directly represent the two quantities requested in the output. The loop follows the generator history from left to right, matching the game order.

The subtraction condition uses `x <= score` instead of checking after subtraction because Python integers allow negative values, but the game itself does not. This prevents an invalid intermediate state.

The reset condition checks whether the current move is the final move. If a round ends earlier, the next recorded move belongs to a new round and must start from `n`. If the final move ends a round, no new round begins, so the answer must keep the score at zero.

There are no indexing tricks or large integer concerns. The values fit easily in Python's integer type, and the algorithm only stores the input sequence and a few variables.

## Worked Examples

For the sample input

```
4 3
1 2 4 1
```

the trace is:

| Move | Generator value | Score before move | Score after move | Completed rounds |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | 0 |
| 2 | 2 | 2 | 0 | 1 |
| 3 | 4 | 3 | 3 | 1 |
| 4 | 1 | 3 | 2 | 1 |

The second move finishes the first round. The third move starts with a fresh score of three, and the remaining moves leave the final score at two. This demonstrates the reset behavior between rounds.

For the input

```
5 4
3 1 5 4 2
```

the trace is:

| Move | Generator value | Score before move | Score after move | Completed rounds |
| --- | --- | --- | --- | --- |
| 1 | 3 | 4 | 1 | 0 |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 5 | 4 | 4 | 1 |
| 4 | 4 | 4 | 0 | 2 |
| 5 | 2 | 4 | 2 | 2 |

The trace shows two completed rounds and a remaining score of two. It also checks the case where a later move finishes a round and another move continues the game.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each generator value is processed exactly once. |
| Space | O(k) | The implementation stores the input array. |

The time complexity is linear in the number of moves, which is suitable for `k` up to `100000`. The memory usage is also well below the limit. The array storage could be removed with a streaming parser, but it is unnecessary for these constraints.

## Test Cases

```python
import sys
import io

def solve(data):
    input = io.StringIO(data).readline
    k, n = map(int, input().split())
    a = list(map(int, input().split()))

    score = n
    rounds = 0

    for i, x in enumerate(a):
        if x <= score:
            score -= x
        if score == 0:
            rounds += 1
            if i != k - 1:
                score = n

    return f"{rounds}\n{score}\n"

assert solve("4 3\n1 2 4 1\n") == "1\n2\n", "sample 1"
assert solve("1 5\n5\n") == "1\n0\n", "single completed round"
assert solve("1 5\n7\n") == "0\n5\n", "failed subtraction"
assert solve("3 5\n2 2 2\n") == "0\n1\n", "ignored final move"
assert solve("5 4\n3 1 5 4 2\n") == "2\n2\n", "multiple rounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 3 / 1 2 4 1` | `1 / 2` | Provided sample behavior |
| `1 5 / 5` | `1 / 0` | Final move ends a round |
| `1 5 / 7` | `0 / 5` | Invalid subtraction is ignored |
| `3 5 / 2 2 2` | `0 / 1` | Boundary after failed subtraction |
| `5 4 / 3 1 5 4 2` | `2 / 2` | Several completed rounds |

## Edge Cases

For the case

```
1 5
7
```

the algorithm starts with score five. The only generator value is larger than the score, so no subtraction happens. The score never reaches zero, the round counter remains zero, and the final score is five.

For the case

```
1 5
5
```

the subtraction succeeds and changes the score from five to zero. The algorithm counts one completed round. Since this is the final move, it does not reset the score, leaving the required final score as zero.

For the case

```
3 5
2 2 2
```

the first move changes the score to three and the second changes it to one. The third move cannot be applied because two is larger than one, so the score remains one. The algorithm never counts a round because zero is never reached.

For the case

```
5 4
3 1 5 4 2
```

the first two moves complete a round. The third move begins with score four, fails, and keeps the score unchanged. The fourth move completes the second round. The final move starts from four and leaves two. The algorithm handles both the middle reset and the final non-zero score correctly.
