---
title: "CF 104669G - No Anime"
description: "We are dealing with two agents on an infinite 2D grid. One agent, Keys, moves every second by exactly one grid step in one of the four cardinal directions. After moving, Keys leaves a permanent “poster” on the cell he just left."
date: "2026-06-29T09:42:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "G"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 89
verified: true
draft: false
---

[CF 104669G - No Anime](https://codeforces.com/problemset/problem/104669/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are dealing with two agents on an infinite 2D grid. One agent, Keys, moves every second by exactly one grid step in one of the four cardinal directions. After moving, Keys leaves a permanent “poster” on the cell he just left.

The second agent, Tortles, moves after Keys each second. In a single second, Tortles may either stay in place or move along a Manhattan path whose total length is exactly 2, which effectively means he can traverse up to two grid edges per second but cannot make a single-step move.

Tortles has two objectives. First, he must eventually visit and clean every cell that Keys has ever visited and left a poster on. Only after all posters are gone does the pursuit matter. Second, he must end up on the same cell as Keys at some point after that cleanup is complete.

The input gives initial coordinates of both agents. We are asked to compute the minimum number of seconds until Tortles can guarantee both cleaning all posters and eventually catching Keys, assuming both play optimally.

The coordinate bounds go up to 10^9, which immediately rules out any simulation of movement over time or grid traversal. Any valid solution must compress the interaction into a closed-form expression depending only on the initial geometry.

A common subtle issue is misinterpreting Tortles’ movement as either Manhattan distance ≤ 2 or exactly 2. The correct interpretation allows staying still or moving along any path whose total Manhattan length is exactly 2, which effectively behaves like “speed 2 in L1 per second”.

Another potential pitfall is overthinking the posters. Keys leaves a full path trace, but Tortles is not required to minimize travel over that entire path independently; optimal play reduces everything to a single pursuit constraint between two moving points.

## Approaches

A brute-force interpretation would simulate both players second by second. Keys chooses a direction, Tortles responds optimally by exploring which two-step path minimizes future cost while also cleaning newly generated posters. This turns into a branching game tree where each state depends on full history of visited cells. Since Keys can move in 4 directions and Tortles can choose among many two-step paths, the number of states grows exponentially with time. Even for small distances, this becomes infeasible beyond a few dozen steps.

The key simplification comes from separating the problem into two interacting motions rather than a growing set of visited constraints. The only thing that matters for feasibility is how fast Tortles can reduce the Manhattan separation while Keys is actively trying to increase it. The poster trail does not introduce additional constraints because every poster lies on Keys’ path, and once Tortles is able to match Keys’ position over time, he will necessarily pass through all intermediate visited cells in a way that is not worse than the final chase constraint.

This reduces the problem to a pursuit game in Manhattan metric where Keys moves with speed 1 per second and Tortles effectively moves with speed 2 per second, but with the important ordering that Keys moves first each round. That ordering slightly weakens Tortles’ advantage but does not change the linear relationship.

The entire problem collapses into tracking how the Manhattan distance evolves under optimal adversarial play.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation of game states | Exponential | Exponential | Too slow |
| Optimal distance analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

Let the initial Manhattan distance between Tortles and Keys be $D = |X_1 - X_2| + |Y_1 - Y_2|$.

1. Compute $D$ from the given coordinates. This represents the initial separation on the grid under optimal alignment of axis-aligned movement.
2. Observe one full second of interaction. Keys moves first, so he can increase the Manhattan distance by at most 1 by moving directly away from Tortles along a grid axis.
3. After Keys moves, Tortles responds with a two-step Manhattan move, which can reduce the distance by at most 2 by moving along a shortest path toward Keys’ new position.
4. Combine the two effects over one second. The distance change per round is at most +1 from Keys and at most −2 from Tortles, giving a net decrease of at least 1 in the best-case scenario for Keys and optimal response from Tortles.
5. Therefore, after $t$ seconds, Tortles can have reduced the initial distance by at most $t$, while Keys may have increased it by at most $t$, and Tortles can reduce by at most $2t$. The constraint for capture becomes $2t \ge D + t$, which simplifies to $t \ge D$.
6. Output $D$, since it is the smallest integer time satisfying the capture condition.

### Why it works

The invariant is that the Manhattan distance between the two agents can increase by at most 1 before Tortles moves and can decrease by at most 2 after Tortles moves. This bounds the net progress per second in a way that depends only on the initial distance, not the specific path Keys takes. Since Keys’ optimal strategy is always to maximize separation and Tortles’ optimal strategy is always to minimize it, the system behaves like a linear differential inequality in discrete time whose tight solution is exactly the initial Manhattan distance.

The poster mechanism does not change this invariant because every posted cell lies on Keys’ trajectory, and once Tortles reaches Keys optimally, he necessarily passes through all intermediate positions in a time-efficient chase path.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        dist = abs(x1 - x2) + abs(y1 - y2)
        out.append(str(dist))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution computes the Manhattan distance for each test case. This directly matches the derived optimal capture time.

The implementation is straightforward, but the key point is that no simulation or state tracking is required. Everything reduces to a single arithmetic expression per test case.

## Worked Examples

### Example 1

Input:

```
1
1 1 1 2
```

Here the distance is $|1-1| + |1-2| = 1$.

| Step | Keys Position | Tortles Position | Distance |
| --- | --- | --- | --- |
| 0 | (1,2) | (1,1) | 1 |

Tortles can move directly upward in one second using a two-step path that effectively closes the gap. This confirms that the answer is 1, matching the formula.

### Example 2

Input:

```
1
1 1 4 5
```

Initial distance is $|1-4| + |1-5| = 7$.

| Step | Keys Position | Tortles Position | Distance |
| --- | --- | --- | --- |
| 0 | (4,5) | (1,1) | 7 |

Over time, Keys can only delay capture by at most matching one unit per second of progress, while Tortles removes up to two units per second. The net effect reduces the problem to exactly 7 seconds of chase time.

This confirms that diagonal or axis-biased movement does not change the linear dependence on Manhattan distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case computes a constant number of arithmetic operations |
| Space | O(1) | Only a few variables are used besides output storage |

The solution is optimal for the constraints since coordinates can be as large as 10^9, making any geometric traversal impossible. The constant-time per test case approach is the only viable method.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod  # dummy import safety

    t = int(sys.stdin.readline())
    res = []
    for _ in range(t):
        x1, y1, x2, y2 = map(int, sys.stdin.readline().split())
        res.append(str(abs(x1 - x2) + abs(y1 - y2)))
    return "\n".join(res)

# provided sample
assert run("1\n1 1 1 2\n") == "1"

# same cell
assert run("1\n5 5 5 5\n") == "0"

# horizontal distance
assert run("1\n1 1 10 1\n") == "9"

# mixed direction
assert run("1\n1 2 4 6\n") == "7"

# large coordinates
assert run("1\n1000000000 1 1 1000000000\n") == "1999999998"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| same cell | 0 | zero distance edge case |
| horizontal line | 9 | axis-aligned movement correctness |
| mixed direction | 7 | general Manhattan geometry |
| large coordinates | 1999999998 | overflow-safe arithmetic |

## Edge Cases

When both players start at the same cell, the Manhattan distance is zero and the answer is trivially zero. The algorithm handles this directly since the absolute difference computation yields 0 immediately.

When movement is purely horizontal or vertical, the distance reduces to a single absolute difference. The formula still applies without modification since the second coordinate contributes zero.

For large coordinate values, such as opposite corners of the allowed range, the subtraction and absolute value operations remain safe in Python due to unbounded integers, and the result directly reflects the full Manhattan span without intermediate overflow risk.
