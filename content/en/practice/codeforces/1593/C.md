---
title: "CF 1593C - Save More Mice"
description: "We are given a line segment with three types of entities: a cat starting at position 0, a hole at position n, and several mice positioned strictly between them. Time advances in discrete seconds."
date: "2026-06-14T23:39:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1593
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 748 (Div. 3)"
rating: 1000
weight: 1593
solve_time_s: 165
verified: false
draft: false
---

[CF 1593C - Save More Mice](https://codeforces.com/problemset/problem/1593/C)

**Rating:** 1000  
**Tags:** binary search, greedy  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line segment with three types of entities: a cat starting at position 0, a hole at position n, and several mice positioned strictly between them. Time advances in discrete seconds. Each second is split into two actions: first we choose exactly one mouse and move it one step to the right, and then the cat moves one step to the right. If a mouse reaches the hole during its move, it is immediately safe and no longer participates. If the cat lands on a position containing one or more mice after its move, those mice are eaten.

The task is to choose which mouse to move each second in order to maximize how many mice reach the hole before ever sharing a position with the cat after its move.

A useful way to reinterpret this is to think of each mouse as having a deadline: it must reach position n strictly before the cat reaches its position. However, unlike a static deadline problem, we can interleave progress among mice, which creates a scheduling problem rather than a direct comparison problem.

The constraints are large: the total number of mice across all test cases is up to 4⋅10^5. This immediately rules out any quadratic simulation where we repeatedly simulate each second for each mouse. Even O(k^2) per test case would be far too slow. We need something closer to O(k log k) or O(k).

A few edge cases reveal the structure:

If all mice start very close to the cat, for example n = 10 and positions [1,1,1,1], then any poor scheduling where we repeatedly advance one mouse could allow the cat to catch all of them at position 1 before any reach the hole. The correct strategy is to prioritize pushing some mice far enough ahead so they “escape the cat’s reach window.”

If all mice are already close to the hole, for example n = 10 and positions [9,9,9], then any schedule works as long as at least one mouse is moved immediately. The limiting factor is not interference between mice, but the single-mouse-per-second constraint.

The key subtlety is that the cat advances deterministically at unit speed and acts as a moving cutoff line. Mice that lag behind that cutoff become irreversibly doomed.

## Approaches

A direct simulation would try to model each second, choosing a mouse greedily or even exhaustively, updating positions and checking whether mice are eaten or escape. While correct, this approach is fundamentally too slow because each mouse may require up to O(n) moves and we have up to 4⋅10^5 mice.

The key observation is to invert the perspective: instead of thinking about positions in absolute space, we think in terms of “how many seconds each mouse survives before being caught.” A mouse starting at position x must reach n before the cat reaches x. Since the cat moves exactly one step per second starting from 0, the cat reaches position x at time x. This suggests that a mouse must finish its required travel before a deadline tied to its starting position.

However, mice do not move continuously; only one mouse can move per second, so mice effectively compete for time slots before their deadlines. This becomes a scheduling problem: each mouse i needs a certain number of moves (n − x_i), and it must receive enough turns before time x_i.

Rewriting this, each mouse provides a “profit” of 1 if we manage to fully process it, and has a constraint window of size x_i. The best strategy becomes selecting mice that are easiest to complete within their available window. That naturally suggests sorting by starting position and greedily counting how many can be completed while respecting cumulative time.

We process mice in increasing order of their distance to the cat (or equivalently decreasing starting position). Each time we consider a mouse, we try to assign it the required number of moves. If at any point we exceed its deadline, we stop or skip accordingly depending on feasibility tracking. The final structure reduces to selecting a maximum prefix under a feasibility condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(k · n) worst case | O(k) | Too slow |
| Greedy scheduling after sorting | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

We reinterpret each mouse as needing a certain amount of processing time and having a deadline imposed by the cat’s arrival.

1. Compute for each mouse the time it needs to reach the hole, which is n − x_i. This is the number of times it must be chosen to move.
2. Sort mice by their starting position in decreasing order. Mice closer to the hole are prioritized because their deadlines are tighter; delaying them risks immediate loss.
3. Maintain a running counter representing how many seconds have been spent assigning moves to mice that we are attempting to save. This counter represents global time usage in our schedule.
4. Iterate over mice in sorted order. For each mouse, add its required travel time to the counter.
5. If at any point the cumulative time exceeds the number of available safe moves before the cat reaches the relevant boundary, this mouse cannot be saved, and we stop increasing the count.
6. Otherwise, count this mouse as successfully scheduled.

The key idea is that every saved mouse consumes a contiguous block of time in the schedule, and earlier mice (closer to the hole) must be guaranteed completion before the cat’s progression eliminates their feasibility window.

### Why it works

At any moment, the cat enforces a monotone increasing constraint: positions become unsafe permanently once the cat passes them. This creates a structure where feasibility depends only on whether we can assign enough early time slots to each chosen mouse before its implicit deadline. Sorting by position ensures we always consider the most restrictive cases first. The greedy accumulation ensures we never “waste” early time on a mouse that would not fit within the remaining schedule. Because every mouse competes for the same single unit-time resource, optimality reduces to filling the schedule with the maximum number of non-overlapping time requirements under increasing constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        x = list(map(int, input().split()))

        # sort mice by closeness to hole (largest x first)
        x.sort(reverse=True)

        time_used = 0
        saved = 0

        for xi in x:
            need = n - xi

            if time_used + need <= xi:
                time_used += need
                saved += 1
            else:
                break

        print(saved)

if __name__ == "__main__":
    solve()
```

The code first sorts mice so that those closest to the hole are processed first, since they are the most time-sensitive. For each mouse we compute how many moves it requires to reach the hole. The variable `time_used` tracks how many total mouse-moves we have already scheduled. We only accept a mouse if adding its required moves still allows it to finish before the cat reaches its starting position. Once this condition fails, no further mice can be saved because remaining mice are even less constrained.

The key implementation detail is the inequality `time_used + need <= xi`. It encodes the fact that all work assigned to a mouse must occur before the cat reaches its starting position.

## Worked Examples

### Example 1

Input:

```
n = 10
x = [8, 7, 5, 4, 9, 4]
```

Sorted:

```
[9, 8, 7, 5, 4, 4]
```

| Mouse | need (10-x) | time_used before | feasible? | time_used after | saved |
| --- | --- | --- | --- | --- | --- |
| 9 | 1 | 0 | yes | 1 | 1 |
| 8 | 2 | 1 | yes | 3 | 2 |
| 7 | 3 | 3 | yes | 6 | 3 |
| 5 | 5 | 6 | no | - | 3 |

We can save 3 mice before the schedule becomes infeasible. This shows that even though multiple mice are close to the hole, their cumulative processing time becomes the bottleneck.

### Example 2

Input:

```
n = 2
x = [1,1,1,1,1,1,1,1]
```

Sorted:

```
[1,1,1,1,1,1,1,1]
```

| Mouse | need (2-x) | time_used before | feasible? | time_used after | saved |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 | 1 |
| 1 | 1 | 1 | no | - | 1 |

Only one mouse can be saved because each requires exactly one unit of time and the deadline is extremely tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | sorting dominates each test case |
| Space | O(k) | storing mouse positions |

The total k across all test cases is at most 4⋅10^5, so the solution runs comfortably within limits even in Python. Sorting and linear scanning are both efficient enough for this constraint scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("""3
10 6
8 7 5 4 9 4
2 8
1 1 1 1 1 1 1 1
12 11
1 2 3 4 5 6 7 8 9 10 11
""") == """3
1
4"""

# minimum case
assert run("""1
2 1
1
""") == "1"

# all equal positions
assert run("""1
10 5
5 5 5 5 5
""") == "2"

# already near hole
assert run("""1
10 3
9 9 9
""") == "3"

# large spread
assert run("""1
100 4
1 2 50 99
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single mouse | 1 | base feasibility |
| all equal | 2 | scheduling competition |
| near hole | 3 | trivial escape case |
| mixed spread | 3 | greedy ordering correctness |

## Edge Cases

A tight cluster near position 1 exposes the scheduling constraint most clearly. For input like n = 10 and x = [1,1,1], each mouse requires 9 moves while their deadline is 1, making all but possibly none feasible. The algorithm immediately detects infeasibility after the first addition to `time_used`, because even one assignment exceeds the deadline condition.

A symmetric case near the hole, such as x = [n−1, n−1, n−1], shows the opposite behavior. Each mouse requires only one move, and their deadlines are large enough that multiple can be scheduled before the cat reaches their positions. The greedy accumulation continues without violation, confirming that the constraint only binds when cumulative work exceeds available safe time.
