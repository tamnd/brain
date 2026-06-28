---
title: "CF 104842B - Basketball Plus-Minus"
description: "The game simulates a basketball match where two teams each start with five active players and five substitutes. Over time, two things happen: players are swapped between the court and the bench, and scoring events occur."
date: "2026-06-28T11:31:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104842
codeforces_index: "B"
codeforces_contest_name: "2020-2021 ICPC, Moscow Subregional"
rating: 0
weight: 104842
solve_time_s: 57
verified: true
draft: false
---

[CF 104842B - Basketball Plus-Minus](https://codeforces.com/problemset/problem/104842/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The game simulates a basketball match where two teams each start with five active players and five substitutes. Over time, two things happen: players are swapped between the court and the bench, and scoring events occur. The twist is that scoring does not go to a team total alone, but is distributed to individual players who are currently on the court.

Whenever a team scores a basket worth x points, every player from that team who is currently playing on the court gains x to their personal statistic. At the same time, every player from the opposing team currently on the court loses x. Substitutions do not affect accumulated scores, but they change which players are currently affected by future scoring events.

The task is to process the full sequence of substitutions and scoring events in order and compute, for every player who ever appeared on the court, their final plus-minus value. Output must follow the order in which players first appear in play, not input declaration order.

The constraints are small, with at most 1000 events. This immediately rules out anything more complex than linear or near-linear simulation. Any approach that updates per event over the current five players on each team is easily fast enough since each event touches at most ten players.

A subtle detail is that players may appear in the output order only when they first step onto the court, not when they are listed in the initial roster. Another detail is that substitutions can introduce players not mentioned earlier in events, so the system must dynamically register new names.

Another edge case is repeated appearances: a player can leave and re-enter the court multiple times, but their score is cumulative across all periods they are active.

## Approaches

A direct simulation matches the problem statement exactly. We maintain the current five players for each team in a set, and maintain a dictionary mapping each player name to their accumulated score. We also track whether a player has been seen before in order to fix the output ordering.

For each scoring event, we iterate over the five active players of the scoring team and add x, and iterate over the five active players of the opponent and subtract x. For substitution events, we remove one player from the active set and insert another, without changing scores.

This works because the number of active players is constant and small, so each event costs constant work. With up to 1000 events, total operations remain tiny.

A brute force variant would try to reconstruct the full timeline and recompute contributions per player per event, but that is unnecessary since we already maintain exact state incrementally. There is no need for recomputation or rollback; the system is purely forward additive.

The key observation is that the only state that matters at any time is the current five players per team. Everything else is just accumulated bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate full recomputation per event | O(q * n) | O(n) | Too slow / unnecessary |
| Direct simulation with active sets | O(q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse initial team names and starting lineups, and mark all these players as “known” so we can preserve ordering later. We also initialize their scores to zero.
2. Store the current on-court players for each team in a set or dictionary-like structure. This allows O(1) membership updates during substitutions.
3. Maintain a dictionary `score[player]` to accumulate plus-minus values across the match.
4. Maintain a list `order` that records the first time each player appears in any on-court position. This list will be used for final output ordering.
5. Process each event in chronological order.
6. If the event is a scoring event for team T with value x, iterate over the five players currently on the court for T and add x to each of their scores. Then iterate over the opposing team's five players and subtract x from each of them. This directly reflects how the scoring affects individual statistics.
7. If the event is a substitution, remove the outgoing player from the active set and insert the incoming player. If the incoming player has never appeared before, initialize their score to zero and append them to the output order list.
8. After all events, iterate over the recorded order list and print each player along with their team and signed score.

### Why it works

At any moment in time, a player's contribution to the final statistic depends only on whether they are on the court during each scoring event. The algorithm maintains the exact set of active players at every step, so each scoring update is applied precisely to the correct subset of players. Since substitutions only change membership in this set and never affect past events, processing events sequentially preserves correctness without needing rollback or future knowledge.

## Python Solution

```python
import sys
input = sys.stdin.readline

def fmt(x):
    if x > 0:
        return f"+{x}"
    return str(x)

first_team = input().strip()
first_players = [input().strip() for _ in range(5)]

second_team = input().strip()
second_players = [input().strip() for _ in range(5)]

score = {}
team_of = {}

on = {first_team: set(first_players),
      second_team: set(second_players)}

order = []
seen = set()

def register(p, team):
    if p not in seen:
        seen.add(p)
        order.append(p)
        score[p] = 0
        team_of[p] = team

for p in first_players:
    register(p, first_team)

for p in second_players:
    register(p, second_team)

q = int(input())
for _ in range(q):
    line = input().strip()

    if "scored" in line:
        parts = line.split()
        team = parts[1]
        val = int(parts[-1])

        for p in on[team]:
            score[p] += val
        other = first_team if team == second_team else second_team
        for p in on[other]:
            score[p] -= val

    else:
        parts = line.split()
        team = parts[1]
        y = parts[3]
        z = parts[5]

        on[team].remove(y)
        on[team].add(z)

        register(z, team)

for p in order:
    s = score[p]
    sign = "" if s == 0 else ("+" if s > 0 else "")
    print(f"{p} ({team_of[p]}) {fmt(s)}")
```

The core implementation keeps two active sets, one per team, and updates them directly when substitutions happen. The scoring logic is symmetric: we loop over the scoring team’s five players to add points and over the opposing five to subtract. The `register` function ensures we only add players once to the output order and initialize their metadata exactly when they first appear in play.

One subtle point is parsing event lines. Instead of relying on strict formatting branches, we check for the keyword `"scored"`, since that cleanly separates the two event types. Another subtle point is that players may be introduced via substitution before ever appearing in the initial lineup ordering, so registration must happen both at initialization and during substitutions.

## Worked Examples

We trace a simplified scenario to see how scoring and substitutions interact.

### Example 1

Input:

```
A
p1
p2
p3
p4
p5
B
q1
q2
q3
q4
q5
2
Team A scored 2
Team B replaced q1 with q6
```

We track active sets and scores.

| Step | Event | A on court | B on court | Score change |
| --- | --- | --- | --- | --- |
| 0 | init | p1..p5 | q1..q5 | all 0 |
| 1 | A scores 2 | p1..p5 | q1..q5 | A +2 each, B -2 each |
| 2 | B sub | p1..p5 | q2..q6 | no change |

Final effect is only from step 1, demonstrating that substitutions only affect future scoring.

### Example 2

Input:

```
A
a1
a2
a3
a4
a5
B
b1
b2
b3
b4
b5
3
Team A scored 3
Team A replaced a1 with a6
Team A scored 1
```

| Step | Event | A on court | B on court | Score change |
| --- | --- | --- | --- | --- |
| 0 | init | a1..a5 | b1..b5 | 0 |
| 1 | A scored 3 | a1..a5 | b1..b5 | +3 / -3 |
| 2 | sub | a2..a6 | b1..b5 | 0 |
| 3 | A scored 1 | a2..a6 | b1..b5 | +1 / -1 |

This shows why tracking the current active set is sufficient: the second scoring event uses a different group of players than the first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each event touches at most 10 players (5 per team) |
| Space | O(n) | Stores scores, team mapping, and active sets |

With at most 1000 events, the solution performs only a few thousand operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    first_team = input().strip()
    first_players = [input().strip() for _ in range(5)]

    second_team = input().strip()
    second_players = [input().strip() for _ in range(5)]

    score = {}
    team_of = {}

    on = {first_team: set(first_players),
          second_team: set(second_players)}

    order = []
    seen = set()

    def register(p, team):
        if p not in seen:
            seen.add(p)
            order.append(p)
            score[p] = 0
            team_of[p] = team

    for p in first_players:
        register(p, first_team)
    for p in second_players:
        register(p, second_team)

    q = int(input())
    for _ in range(q):
        line = input().strip()
        if "scored" in line:
            parts = line.split()
            team = parts[1]
            val = int(parts[-1])
            other = first_team if team == second_team else second_team
            for p in on[team]:
                score[p] += val
            for p in on[other]:
                score[p] -= val
        else:
            parts = line.split()
            team = parts[1]
            y = parts[3]
            z = parts[5]
            on[team].remove(y)
            on[team].add(z)
            register(z, team)

    out = []
    for p in order:
        s = score[p]
        if s > 0:
            out.append(f"{p} ({team_of[p]}) +{s}")
        elif s < 0:
            out.append(f"{p} ({team_of[p]}) {s}")
        else:
            out.append(f"{p} ({team_of[p]}) 0")

    return "\n".join(out)

# custom tests

inp = """A
a1
a2
a3
a4
a5
B
b1
b2
b3
b4
b5
1
Team A scored 1
"""
assert "a1 (A) +1" in run(inp)

inp = """A
a1
a2
a3
a4
a5
B
b1
b2
b3
b4
b5
1
Team B scored 2
"""
assert "a1 (A) -2" in run(inp)

inp = """A
a1
a2
a3
a4
a5
B
b1
b2
b3
b4
b5
3
Team A scored 1
Team A replaced a1 with a6
Team A scored 1
"""
out = run(inp)
assert "a6 (A)" in out
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single score | players updated correctly | basic scoring propagation |
| opponent score | negative updates work | symmetry of update |
| substitution + re-entry | new player tracking | dynamic roster correctness |

## Edge Cases

One subtle case is when a player is introduced via substitution and immediately affects ordering. For example, if a new player enters mid-game and later contributes to scoring, they must appear after all initial players in output order. The `register` function ensures this by appending only at first appearance.

Another case is repeated substitutions of the same player. Since we use sets, removing and re-adding is safe and idempotent. Scores are not reset, so returning players continue accumulating from past contributions.

A final case is players who are declared in the initial roster but never appear on court due to immediate substitutions. These still appear in output because they were initially on court, even if they never receive scoring updates.
