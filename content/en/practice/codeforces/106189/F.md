---
title: "CF 106189F - Classic Tetris: Scoring"
description: "We are given the scoring log of a Tetris player. Each log entry tells us that the player cleared exactly 1, 2, 3, or 4 lines at once, represented by the strings single, double, triple, and tetris. The player starts at level 18."
date: "2026-06-25T06:48:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "F"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 39
verified: true
draft: false
---

[CF 106189F - Classic Tetris: Scoring](https://codeforces.com/problemset/problem/106189/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the scoring log of a Tetris player. Each log entry tells us that the player cleared exactly 1, 2, 3, or 4 lines at once, represented by the strings `single`, `double`, `triple`, and `tetris`.

The player starts at level 18. The score awarded for a clear depends on the current level.

At level 18:

- single = 760 points
- double = 1900 points
- triple = 5700 points
- tetris = 22800 points

The level increases when the total number of cleared lines reaches certain thresholds.

The first transition is special. The player remains at level 18 until at least 130 total cleared lines have been accumulated. Once the total reaches 130 or more, the player moves to level 19.

After that, every additional 10 cleared lines increase the level by one. Reaching 140 lines gives level 20, reaching 150 lines gives level 21, and so on.

Each level above 18 increases the scoring values by:

- +40 for a single
- +100 for a double
- +300 for a triple
- +1200 for a tetris

The task is to process the log, compute the final score, and output both the score and the final level.

The number of actions can be as large as $10^5$. This immediately rules out any simulation that repeatedly iterates through line counts or level ranges for every action. We need a solution whose work is proportional to the number of log entries. An $O(N)$ scan is easily fast enough.

A subtle detail is that the level used for scoring an action is the level before the newly cleared lines from that action are added. If a move clears enough lines to cross a threshold, that move still scores using the previous level, and only future moves use the higher level.

Consider this example:

```
129 cleared lines so far
next action = single
```

The single must still be scored as a level-18 single. After the action, the total becomes 130 and the player advances to level 19.

A common mistake is to update the line count first, compute the new level, and then score the action. That would incorrectly award level-19 points for the move that actually triggered the transition.

Another edge case is a large clear crossing several thresholds at once.

```
128 lines
next action = tetris
```

The player jumps from 128 to 132 total lines. The action is still scored at level 18. The level becomes 19 only afterward.

## Approaches

A straightforward simulation processes the actions one by one.

For every action, determine the current level from the number of lines already cleared, look up the score for that action at that level, add the corresponding number of cleared lines, and continue.

Even a brute-force version is already efficient because there are only $10^5$ actions. The only potential inefficiency would be repeatedly recomputing the level by iterating through thresholds. If we scanned thresholds every time, the cost would grow unnecessarily.

The key observation is that the level depends only on the number of lines cleared before the current action. There is a direct formula.

If fewer than 130 lines have been cleared, the level is 18.

Otherwise:

$$\text{level} = 19 + \left\lfloor \frac{\text{lines}-130}{10} \right\rfloor$$

Once we can compute the current level in constant time, every action is processed in constant time as well.

For scoring, let

$$d = \text{level} - 18$$

Then the score values become:

$$760 + 40d$$

for a single,

$$1900 + 100d$$

for a double,

$$5700 + 300d$$

for a triple,

$$22800 + 1200d$$

for a tetris.

The entire problem reduces to a single pass over the log.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force threshold simulation | O(N) | O(1) | Accepted |
| Optimal direct-level computation | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `lines = 0` and `score = 0`.
2. For each scoring action, determine the current level from the number of lines already cleared.

If `lines < 130`, the level is 18. Otherwise use:

$$19 + (lines - 130) // 10$$
3. Compute `d = level - 18`.

This tells us how many level increases have occurred since the starting level.
4. Award points for the current action using the current level.

The action must be scored before adding its newly cleared lines.
5. Add the corresponding number of cleared lines:

`single -> 1`

`double -> 2`

`triple -> 3`

`tetris -> 4`
6. Continue until all log entries are processed.
7. After processing the entire log, compute the final level from the final total number of cleared lines using the same formula.
8. Output the final score and final level.

### Why it works

At every moment, the game level is determined solely by the number of lines cleared before the current action. The scoring rules depend on that level and not on the line count after the action.

The algorithm maintains exactly this invariant. Before processing each log entry, `lines` stores the number of previously cleared lines. The current level is computed from that value, the action is scored accordingly, and only then are the newly cleared lines added.

Because every action is scored using the same level that the real game would use, and because the level transitions are computed directly from the official thresholds, the accumulated score and final level are correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_level(lines):
    if lines < 130:
        return 18
    return 19 + (lines - 130) // 10

def solve():
    n = int(input())

    score = 0
    lines = 0

    for _ in range(n):
        action = input().strip()

        level = get_level(lines)
        d = level - 18

        if action == "single":
            score += 760 + 40 * d
            lines += 1
        elif action == "double":
            score += 1900 + 100 * d
            lines += 2
        elif action == "triple":
            score += 5700 + 300 * d
            lines += 3
        else:  # tetris
            score += 22800 + 1200 * d
            lines += 4

    final_level = get_level(lines)
    print(score, final_level)

solve()
```

The function `get_level` encodes the level-transition rules directly. Keeping this logic in one place avoids inconsistencies between scoring and final-level computation.

The critical implementation detail is the order of operations. The current level is computed before updating the line count. This matches the game's behavior when a move crosses a threshold.

The score values are expressed through the base level-18 values plus a level-dependent increment. This avoids storing a large table and mirrors the rule described in the statement.

Python integers automatically handle large values, so there is no overflow concern even if every action is a tetris.

## Worked Examples

### Example 1

Input:

```
4
single
double
triple
tetris
```

| Action | Lines Before | Level | Points Gained | Lines After | Total Score |
| --- | --- | --- | --- | --- | --- |
| single | 0 | 18 | 760 | 1 | 760 |
| double | 1 | 18 | 1900 | 3 | 2660 |
| triple | 3 | 18 | 5700 | 6 | 8360 |
| tetris | 6 | 18 | 22800 | 10 | 31160 |

Final level = 18.

Output:

```
31160 18
```

This trace shows that no threshold is crossed, so every action uses the starting level.

### Example 2

Constructed example:

```
2
tetris
tetris
```

Assume the player already had 128 cleared lines before these two actions. We focus on the threshold crossing behavior.

| Action | Lines Before | Level | Points Gained | Lines After |
| --- | --- | --- | --- | --- |
| tetris | 128 | 18 | 22800 | 132 |
| tetris | 132 | 19 | 24000 | 136 |

The first tetris crosses 130 lines but is still scored at level 18. Only the next action receives level-19 scoring.

This confirms the key invariant used by the algorithm.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each log entry is processed once |
| Space | O(1) | Only a few counters are stored |

With at most $10^5$ actions, a single linear scan easily fits within the time limit. Memory usage remains constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    def input():
        return input_data.readline()

    n = int(input())

    def get_level(lines):
        if lines < 130:
            return 18
        return 19 + (lines - 130) // 10

    score = 0
    lines = 0

    for _ in range(n):
        action = input().strip()

        level = get_level(lines)
        d = level - 18

        if action == "single":
            score += 760 + 40 * d
            lines += 1
        elif action == "double":
            score += 1900 + 100 * d
            lines += 2
        elif action == "triple":
            score += 5700 + 300 * d
            lines += 3
        else:
            score += 22800 + 1200 * d
            lines += 4

    output_data.write(f"{score} {get_level(lines)}")
    return output_data.getvalue()

# provided samples
assert run("4\nsingle\ndouble\ntriple\ntetris\n") == "31160 18"
assert run("2\nsingle\nsingle\n") == "1520 18"

# minimum input
assert run("1\nsingle\n") == "760 18"

# exact first threshold
assert run("130\n" + "single\n" * 130) == "98800 19"

# threshold crossed by last action
assert run("33\n" + "tetris\n" * 33) == "752400 19"

# all equal values
assert run("3\ntetris\ntetris\ntetris\n") == "68400 18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One single | 760 18 | Minimum size |
| 130 singles | 98800 19 | Exact transition to level 19 |
| 33 tetrises | 752400 19 | Crossing threshold via a multi-line clear |
| Three tetrises | 68400 18 | Repeated identical actions |

## Edge Cases

Consider the threshold-crossing case:

```
33
tetris
tetris
...
tetris
```

After 32 tetrises, the player has cleared 128 lines and remains at level 18. The 33rd tetris is scored using level 18, giving 22800 points. Only after adding the four cleared lines does the total become 132, which promotes the player to level 19.

A solution that updates the line count before scoring would incorrectly award 24000 points for that final tetris.

Now consider the exact threshold:

```
130
single
single
...
single
```

The 130th single is scored while the player still has 129 cleared lines, so it uses level 18 scoring. After the line is added, the total becomes exactly 130 and the final level becomes 19. The algorithm computes the level before updating `lines`, so it handles this boundary correctly.

Finally, consider a game that never reaches 130 lines:

```
2
single
double
```

The total line count is only 3. Every action is scored at level 18 and the final level remains 18. The formula correctly stays in the special pre-transition range for all computations.
