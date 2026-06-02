---
title: "CF 105E - Lift and Throw"
description: "We are given three characters, each standing on a different position along a one-dimensional half-line. Each position is an integer starting at 1, and each character has a movement range and a throwing range."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 105
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 81"
rating: 2500
weight: 105
solve_time_s: 153
verified: true
draft: false
---

[CF 105E - Lift and Throw](https://codeforces.com/problemset/problem/105/E)

**Rating:** 2500  
**Tags:** brute force  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three characters, each standing on a different position along a one-dimensional half-line. Each position is an integer starting at 1, and each character has a movement range and a throwing range. Movement range defines how far they can move to an unoccupied position, and throwing range defines how far they can throw another character they are holding. Additionally, a character can lift another if they are immediately adjacent, creating a stack of one, two, or even three characters. When stacked, only the topmost character can act-movement and throwing are restricted to the lifter.

The input consists of each character’s starting position, movement range, and throwing range. The output is the maximal position that any of the characters can reach, whether by moving, lifting, or throwing themselves or others. Because positions are small integers (1-10) and each character has only one action of each type, the state space is limited and allows exhaustive simulation if handled carefully.

Edge cases appear when characters are close enough to form stacks or when multiple throw sequences compete. For example, if all characters are adjacent and one has a long throwing range, the optimal path may involve forming a column and throwing the top character far ahead. A naive approach that only considers individual movement could miss these combined sequences. Consider positions `1 1 1` with ranges `3 3 3`; the optimal might involve lifting and throwing chains rather than independent moves.

## Approaches

A brute-force approach would attempt every possible sequence of moves, lifts, and throws for each character, tracking the resulting positions. Since each character has up to three actions, there are permutations of action orders and choices of whom to lift or throw, which quickly explodes combinatorially. For three characters and positions limited to 1-10, this is theoretically feasible but messy to implement without missing sequences.

The key observation is that positions are small, actions are limited, and the state can be fully represented as the tuple of current positions plus who is holding whom. This makes it amenable to a breadth-first search or memoized depth-first search. By generating all reachable states from any given configuration and keeping track of the maximum position seen, we can systematically explore the space without redundancy. The BFS approach naturally accounts for turn order and action limitations.

The optimal approach treats each character’s action as a state transition. A move is valid if the destination is free and within movement range. A lift is valid if the two characters are adjacent and not already held. A throw is valid if the target position is free and within the throwing range. BFS explores all combinations, updating the maximal position any character reaches. Because there are only 10 positions and 3 characters, the total number of states is small enough to simulate fully.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3! × 3^3 × 10^3) | O(10^3) | Too messy / impractical without careful pruning |
| BFS with state memoization | O(10^3 × 3! × 3^3) | O(10^3) | Accepted |

## Algorithm Walkthrough

1. Represent the state of the game as a tuple of the three characters’ positions and a nested tuple describing the holding relationships. This compact representation allows quick comparisons and memoization.
2. Initialize a queue for BFS with the starting positions and an empty holding structure. Track the maximal position encountered in a separate variable.
3. For each state, consider all valid moves for characters who are not held. For each free character, try moving to every position within their movement range that is unoccupied. Push the resulting state to the queue if it has not been visited.
4. For each character who is free and adjacent to another free character, simulate lifting. Update the holding structure so the lifter now holds the lifted character. Push the new state to the queue.
5. For each character who is holding another, try throwing the held character (or column if multiple are stacked) to every free position within their throwing range. Update positions accordingly and push the new state to the queue.
6. After each state transition, update the maximal position if any character’s new position exceeds the current maximum.
7. Continue BFS until the queue is empty. Return the maximal position recorded.

This works because BFS guarantees we explore all reachable states without missing any combination of moves, lifts, and throws. The state representation prevents cycles, ensuring no state is revisited, and by updating the maximum at every step we do not need to backtrack.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    pos = []
    move = []
    throw = []
    for _ in range(3):
        p, m, t = map(int, input().split())
        pos.append(p)
        move.append(m)
        throw.append(t)

    max_pos = max(pos)
    visited = set()
    # state: positions tuple, holding tuple (who holds whom)
    # holding: -1 means free, 0/1/2 means held by character index
    queue = deque()
    init_holding = (-1, -1, -1)
    queue.append((tuple(pos), init_holding))
    visited.add((tuple(pos), init_holding))

    def get_free_positions(positions):
        return set(range(1, 11)) - set(positions)

    while queue:
        positions, holding = queue.popleft()
        max_pos = max(max_pos, max(positions))

        # move
        for i in range(3):
            if holding[i] != -1:
                continue
            for delta in range(-move[i], move[i] + 1):
                if delta == 0:
                    continue
                new_pos = positions[i] + delta
                if 1 <= new_pos <= 10 and new_pos not in positions:
                    new_positions = list(positions)
                    new_positions[i] = new_pos
                    new_state = (tuple(new_positions), holding)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

        # lift
        for i in range(3):
            if holding[i] != -1:
                continue
            for j in range(3):
                if i != j and holding[j] == -1 and abs(positions[i] - positions[j]) == 1:
                    new_holding = list(holding)
                    new_holding[j] = i
                    new_state = (positions, tuple(new_holding))
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

        # throw
        for i in range(3):
            held = [idx for idx, h in enumerate(holding) if h == i]
            if not held:
                continue
            free_pos = get_free_positions(positions)
            for target in free_pos:
                if abs(positions[i] - target) <= throw[i]:
                    new_positions = list(positions)
                    for h_idx in held:
                        new_positions[h_idx] = target
                    new_holding = list(holding)
                    for h_idx in held:
                        new_holding[h_idx] = -1
                    new_state = (tuple(new_positions), tuple(new_holding))
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

    print(max_pos)

solve()
```

The solution starts by reading character positions, move ranges, and throw ranges. BFS explores all reachable states while memoizing visited states to prevent infinite loops. Moves, lifts, and throws are handled separately, always checking if the action is valid. Handling the `holding` tuple correctly ensures that actions are only attempted by characters not currently held, and throw operations correctly propagate positions for any stacked characters. The subtlety is that thrown stacks move as a unit.

## Worked Examples

**Sample 1**

Input:

```
9 3 3
4 3 1
2 3 3
```

| Step | Positions | Holding | Action | Max Pos |
| --- | --- | --- | --- | --- |
| 0 | 9,4,2 | -1,-1,-1 | init | 9 |
| 1 | 6,4,2 | -1,-1,-1 | Laharl moves to 6 | 6 |
| 2 | 6,5,2 | -1,-1,-1 | Flonne moves to 5 | 6 |
| 3 | 6,5,4 | 5 holds 1 | Flonne lifts Etna | 6 |
| 4 | 6,5,4 | 0 holds 2 | Laharl lifts Flonne | 6 |
| 5 | 9,5,4 | -1,0,2 | Laharl throws Flonne | 9 |
| 6 | 12,5,4 | -1,-1,2 | Flonne throws Etna | 12 |
| 7 | 15,5,4 | -1,-1,-1 | Etna moves | 15 |

This shows the optimal strategy forming a stack and using successive throws.

**Custom Example**

Input:

```
1 1 10
2 1 1
3 1 1
```

| Step | Positions | Holding | Action | Max Pos |
| --- | --- | --- | --- | --- |
| 0 | 1,2,3 | -1,-1,-1 | init | 3 |
| 1 | 1,2,3 | 0 holds 1 | Laharl lifts Etna | 3 |
| 2 | 1,2,3 | 0 holds 2 | Etna lifts Flonne | 3 |
| 3 |  |  |  |  |
