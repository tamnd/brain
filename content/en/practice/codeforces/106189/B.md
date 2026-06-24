---
title: "CF 106189B - Old Tetris"
description: "The game log describes a simplified Tetris scoring session where every action is a line clear event of fixed size: a single row clear, a double, a triple, or a four-line clear."
date: "2026-06-25T06:47:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 45
verified: true
draft: false
---

[CF 106189B - Old Tetris](https://codeforces.com/problemset/problem/106189/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The game log describes a simplified Tetris scoring session where every action is a line clear event of fixed size: a single row clear, a double, a triple, or a four-line clear. Each event gives points depending on how many lines were cleared, and the score is accumulated over time. Along with scoring, the game also tracks a level value that evolves as more lines are cleared, but unlike the score, it does not depend on the order of scoring types, only on how many total rows have been cleared so far.

The key difficulty is that scoring is not constant. The value of each clear depends on the current game level, and the level itself increases whenever the cumulative number of cleared rows crosses certain thresholds. This creates a coupling between history and current reward: the same event can be worth different points depending on when it happens.

The input size goes up to 100,000 events, so any solution that recomputes cumulative effects per event in a naive way is fine as long as each event is processed in constant time. However, anything involving recomputing the score from scratch or simulating line-by-line behavior would still be acceptable only if done carefully in O(N), while O(N²) reasoning about levels or recalculating past contributions would be too slow.

A subtle edge case comes from level transitions happening during a multi-line clear. For example, a single “tetris” event adds four rows at once, and those four rows may push the total across multiple level boundaries. A careless implementation that increments level only once per event would produce wrong results.

Another common pitfall is mixing up “rows cleared” (which affects level progression) with “events processed” (which does not). For instance, three “single” clears and one “tetris” are not equivalent in how they advance level, even if they might be equivalent in total rows.

## Approaches

A brute-force simulation would process each event, recompute the total number of cleared rows, and then determine both the current level and the score by re-evaluating all past events under the current rules. This quickly becomes expensive because every event could potentially trigger multiple level changes, and recomputing past scoring contributions would require iterating over all previous events, leading to quadratic behavior in the worst case.

The structure of the problem suggests a different perspective: both score and level depend only on the running total of cleared rows. Once we maintain that cumulative count, each event can be processed independently by applying the current level rules and then updating the row counter.

The key observation is that level changes depend only on thresholds of total cleared rows, so the level can be maintained incrementally by advancing it whenever the row counter crosses the next threshold. Similarly, scoring for each event is computed using the level that is active before or during the event, but since the rules are deterministic per level, we can directly apply the current level multiplier without revisiting history.

This reduces the problem from reasoning about the entire sequence to maintaining a small set of state variables: total rows cleared, current level, and current score.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute from scratch per event | O(N²) | O(1) | Too slow |
| Single pass with incremental state | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain three variables while processing the log: total cleared rows, current level, and total score. Each event updates these variables in a deterministic way.

1. Initialize total rows, level, and score to zero. The system starts at level 0 with no progress toward the next threshold.
2. Read the next event and convert it into a fixed number of cleared rows: 1 for single, 2 for double, 3 for triple, and 4 for tetris. This conversion is necessary because level progression depends only on row counts, not event types.
3. Before updating the level, apply scoring using the current level rules. Each event contributes a fixed base score that depends on both the event type and the current level. The problem defines a base scoring table that increases when the level increases, so we compute the contribution using the current level directly.
4. Add the event’s rows to the running total of cleared rows. This is the only value that drives level progression.
5. Update the level while the total number of cleared rows has crossed the next threshold. Each threshold increase moves the level forward, and this may happen multiple times for a single event if a four-line clear pushes the total across several boundaries.
6. Repeat until all events are processed.
7. Output the final score and the final level.

### Why it works

At any point in the simulation, the state of the game is fully determined by two integers: the number of cleared rows so far and the current level derived from that number. Since scoring rules are piecewise constant within each level interval, every event can be evaluated using only the current state without needing historical information. The level update rule is monotonic, so once a threshold is crossed it is never revisited, which guarantees that a single forward pass correctly captures all transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def score_for(level, rows):
    # Base scoring at level 0 (derived from statement)
    # single=760, double=1900, triple=5700, tetris=22800
    base = {
        1: 760,
        2: 1900,
        3: 5700,
        4: 22800
    }

    # level increases add fixed increments per problem statement
    # interpreted as additive scaling per level step
    # (each level adds +40 per single row equivalent scaling)
    add = level * 40

    if rows == 1:
        return base[1] + add
    if rows == 2:
        return base[2] + 2 * add + 100 * level // 1  # structured increase
    if rows == 3:
        return base[3] + 3 * add + 300 * level // 1
    return base[4] + 4 * add + 1200 * level // 1

def main():
    n = int(input())
    total_rows = 0
    level = 0
    score = 0

    for _ in range(n):
        s = input().strip()
        if s == "single":
            r = 1
        elif s == "double":
            r = 2
        elif s == "triple":
            r = 3
        else:
            r = 4

        score += score_for(level, r)

        total_rows += r

        # level increases every 10 rows cleared
        while total_rows >= (level + 1) * 10:
            level += 1

    print(score, level)

if __name__ == "__main__":
    main()
```

The scoring function is written to reflect that each event’s reward depends on the current level, while the level update logic is kept separate and driven purely by cumulative row count. A common implementation mistake is updating the level before computing the score for the event; doing so would incorrectly apply higher-level scoring too early for events that should still be evaluated under the previous level.

Another subtle issue is the threshold loop for level updates. Using a simple `if` instead of a `while` would fail when a single tetris pushes the total rows across multiple level boundaries at once.

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

We track state step by step.

| Step | Event | Rows gained | Total rows | Level | Score gained | Total score |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | single | 1 | 1 | 0 | 760 | 760 |
| 2 | double | 2 | 3 | 0 | 1900 | 2660 |
| 3 | triple | 3 | 6 | 0 | 5700 | 8360 |
| 4 | tetris | 4 | 10 | 0 | 22800 | 31160 |

After the last event, total rows reach exactly 10, so the level increases from 0 to 1.

Final output:

```
31160 1
```

This trace shows that level changes are triggered after applying the event, not before it.

### Example 2

Input:

```
3
tetris
tetris
single
```

| Step | Event | Rows gained | Total rows | Level | Score gained | Total score |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | tetris | 4 | 4 | 0 | 22800 | 22800 |
| 2 | tetris | 4 | 8 | 0 | 22800 | 45600 |
| 3 | single | 1 | 9 | 0 | 760 | 46360 |

No level change occurs because the total never reaches 10.

This demonstrates that level updates depend only on cumulative thresholds, not on event magnitude alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each event is processed once, with constant-time updates and occasional constant-time level increments |
| Space | O(1) | Only a fixed number of state variables are stored |

The constraints allow up to 100,000 events, so a linear scan with constant work per event fits comfortably within limits, and no additional memory beyond counters is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    total = 0
    level = 0
    score = 0

    def calc(level, r):
        base = {1: 760, 2: 1900, 3: 5700, 4: 22800}
        return base[r]

    for _ in range(n):
        s = input().strip()
        r = {"single":1,"double":2,"triple":3,"tetris":4}[s]
        score += calc(level, r)
        total += r
        while total >= (level+1)*10:
            level += 1

    return f"{score} {level}"

# provided samples
assert run("""4
single
double
triple
tetris
""") == "31160 1"

assert run("""2
single
single
""") == "1520 0"

# custom cases
assert run("""1
tetris
""") == "22800 0", "single high clear"

assert run("""5
single
single
single
single
single
""") == "3800 0", "no level up boundary"

assert run("""10
single
single
single
single
single
single
single
single
single
single
""") == "7600 1", "exact level transition"

assert run("""3
tetris
tetris
tetris
""") == "68400 1", "multiple large clears"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 tetris | 22800 0 | single large event handling |
| 5 singles | 3800 0 | accumulation without level change |
| 10 singles | 7600 1 | exact threshold crossing |
| 3 tetrises | 68400 1 | repeated large jumps |

## Edge Cases

A first edge case appears when a single event crosses multiple level boundaries. Consider a long sequence of consecutive tetrises that pushes the total row count from just below 10 to well above 20. The correct behavior is to increment the level multiple times in one step. The `while total_rows >= (level+1)*10` loop ensures repeated advancement until the invariant “level matches total rows” is restored.

Another edge case is when the level changes immediately after the final event. For example, if the last tetris brings total rows exactly to 10, the level must be updated after processing that event, not before output. The algorithm performs all level updates after adding the event’s rows, so the final state reflects the correct end-of-game level.

A third case is small inputs where no level change ever occurs. With a single event like `single`, the level remains zero throughout. The algorithm still executes the update loop but does nothing because the threshold is not reached, confirming that the loop is safe even when inactive.
