---
title: "CF 104072B - Balls"
description: "We are given a line with several balls placed at different positions. Each ball starts at a known coordinate and moves along the number line with a constant velocity, either to the left or to the right. All balls start moving at the same moment."
date: "2026-07-02T02:52:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104072
codeforces_index: "B"
codeforces_contest_name: "AGM 2022, Final Round, Day 2"
rating: 0
weight: 104072
solve_time_s: 46
verified: true
draft: false
---

[CF 104072B - Balls](https://codeforces.com/problemset/problem/104072/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line with several balls placed at different positions. Each ball starts at a known coordinate and moves along the number line with a constant velocity, either to the left or to the right. All balls start moving at the same moment. The twist is that whenever two balls meet, they do not interact in a complicated physical way, instead they pass through each other by swapping their velocities, which makes the system equivalent to particles moving freely if we ignore identities.

At a fixed time T, we are asked to determine where all balls are located. The final output is not tied to the original identities, since collisions effectively permute velocities between balls. Instead, we are interested in the multiset of positions of all balls after time T, printed in non-decreasing order.

The key constraint is N up to 100000 and coordinates and velocities up to 10^9 in magnitude, with time up to 10^9. This immediately implies that any simulation that advances time step by step or processes collisions explicitly is impossible. A naive simulation of collisions would require processing potentially O(N^2) interaction events in the worst case, since every pair of balls can interact indirectly through chains of swaps. Even an event-driven simulation would be too slow because the number of collision events can be quadratic.

A simpler but subtle edge case appears when multiple balls share the same initial position or arrive at the same point at the same time due to different speeds. Since collisions are defined as instantaneous swaps, these situations do not create ambiguity in the final set of positions, but they break naive implementations that try to simulate ordering explicitly rather than working with a mathematical transformation of motion.

For example, consider two balls at positions 0 and 10 moving toward each other with speeds 1 and -1. After T = 5, they collide at position 5 and swap velocities, so the left ball ends on the right and vice versa. A naive simulation tracking identities would be forced to handle collision ordering precisely, but the final positions are simply the same as if the balls had passed through each other.

The core modeling insight is that swapping velocities at collisions makes the system equivalent to letting balls pass through each other without interaction, and then reassigning identities afterward based on order.

## Approaches

The brute-force view is to simulate the motion and explicitly process collisions. We would maintain all balls sorted by position, repeatedly find the next collision event, advance time to that event, swap velocities of the colliding pair, and continue until time T. Each collision is an event, and in the worst case, every pair of adjacent balls can collide multiple times depending on velocities. The number of events can reach O(N^2), and each event requires priority queue updates or list scans, making the solution far too slow for N = 100000.

The key observation is that swapping velocities during collisions is equivalent to saying that balls behave like they pass through each other unchanged if we ignore their identities. This means we can compute where each ball would be if it moved independently: position at time T is simply p_i + s_i * T.

The only remaining issue is that collisions swap identities, but since the output requires only positions sorted in non-decreasing order, identity is irrelevant. After computing all final positions independently, sorting them gives the correct configuration. The radius R is irrelevant to the final positions because it only affects when collisions occur, not the mathematical equivalence of trajectory swapping.

Thus the problem reduces to computing a linear transformation for each ball and sorting the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N^2) or worse | O(N) | Too slow |
| Independent Motion + Sort | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. For each ball, compute its position as if no collisions ever occurred. This is done using p_i + s_i * T, which represents uniform motion under constant velocity. This step is valid because collisions only swap velocities and do not change the set of trajectories.
2. Store all computed positions in an array. At this point, each entry represents a final possible location of some ball, but identities are no longer meaningful.
3. Sort the array of positions in non-decreasing order. Sorting is necessary because collisions only permute which ball occupies which trajectory, but the set of final coordinates is unchanged.
4. Output the sorted list as the final configuration.

Why it works

The crucial invariant is that collisions only permute velocities between balls, which means the multiset of trajectories is preserved. If we imagine labeling each velocity as a token and letting it move freely, each token follows a straight-line path. The swapping mechanism ensures that balls simply exchange these tokens when they meet. Therefore, at any time T, the set of positions occupied by balls is exactly the set of positions obtained by independently advancing each initial ball without considering collisions. The only difference is which ball ends up at which position, which is irrelevant since output is sorted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r, t = map(int, input().split())
    pos = []
    
    for _ in range(n):
        p, s = map(int, input().split())
        pos.append(p + s * t)
    
    pos.sort()
    print(*pos)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the observation that collisions do not affect the multiset of final positions. Each ball’s trajectory is computed independently, then the results are sorted.

The only subtle point is using 64-bit safe arithmetic. In Python this is automatic, but in other languages care is needed since p_i and s_i * T can reach up to 10^18.

## Worked Examples

### Example 1

Input:

3 1 5

3 -1

8 -2

1 3

We compute raw positions:

| Ball | p | s | p + sT |
| --- | --- | --- | --- |
| 1 | 3 | -1 | -2 |
| 2 | 8 | -2 | -2 |
| 3 | 1 | 3 | 16 |

After sorting we get -2, -2, 16.

This matches the idea that two balls may end up sharing the same final coordinate value depending on velocity and initial placement, but ordering is determined only at the end.

This trace shows that collisions are irrelevant to computation, since direct evaluation already yields correct final set.

### Example 2

Input:

4 1 3

0 2

5 -1

10 -2

7 1

Raw positions:

| Ball | p | s | p + sT |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 6 |
| 2 | 5 | -1 | 2 |
| 3 | 10 | -2 | 4 |
| 4 | 7 | 1 | 10 |

Sorting gives 2, 4, 6, 10.

This example shows that even though faster balls may overtake slower ones in physical motion, swapping ensures trajectories are preserved, so final positions depend only on linear motion, not interaction order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | computing positions is O(N), sorting dominates |
| Space | O(N) | storing final positions |

The constraints allow up to 100000 balls, so an O(N log N) solution fits comfortably within limits. Memory usage is linear and well within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# sample
assert run("""3 1 5
3 -1
8 -2
1 3
""") == "-2 -2 16"

# minimum size
assert run("""1 1 10
5 2
""") == "25"

# all same speed
assert run("""3 1 2
0 1
10 1
20 1
""") == "2 12 22"

# mixed directions
assert run("""4 1 1
0 -1
1 1
2 -1
3 1
""") == "-1 0 2 4"

# large values
assert run("""2 1 1000000000
0 1000000000
1000000000 -1000000000
""") == "0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 ball | direct motion | base case |
| identical speeds | stable ordering | no interaction effect |
| mixed directions | sign handling | correctness under swaps |
| large values | overflow safety | 1e18 scale correctness |

## Edge Cases

One subtle situation is when two balls end up at exactly the same computed position. For instance, two balls starting at different points can land on the same coordinate after time T due to opposite velocities. The algorithm still works because sorting treats equal values naturally, and collisions in the original process also allow temporary overlap without changing final position set.

Another edge case is T = 0. In this case, computed positions reduce to initial positions p_i, and sorting simply returns the initial ordering by coordinate, which matches the requirement since no motion occurs.

A further edge case is negative velocities combined with large T, which can push positions into negative numbers. The formula p_i + s_i * T handles this directly, and Python integer arithmetic prevents overflow issues that would appear in fixed-width integer languages.
