---
title: "CF 102620B - Pirating Parrots"
description: "The problem describes a parrot that is already following a partially written route on a coordinate grid. The route is made of the four movement commands: moving right, left, up, or down. After executing the existing commands, the parrot is at some position."
date: "2026-08-02T07:06:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102620
codeforces_index: "B"
codeforces_contest_name: "mBIT Standard June 2020"
rating: 0
weight: 102620
solve_time_s: 48
verified: true
draft: false
---

[CF 102620B - Pirating Parrots](https://codeforces.com/problemset/problem/102620/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a parrot that is already following a partially written route on a coordinate grid. The route is made of the four movement commands: moving right, left, up, or down. After executing the existing commands, the parrot is at some position. The goal is to find the smallest number of extra commands that must be appended to the end of the route so that the parrot reaches the given destination point.

The input gives the current route, its length, and the final coordinates the parrot needs to reach. The output is only the number of additional moves needed, not the actual sequence of moves.

The constraints make the intended idea much simpler than a search problem. If the route length is at most a few hundred characters, directly simulating the movement takes only linear time. Even if the route length were much larger, a single pass would still be the correct approach because every command affects the final position independently. Any solution that tries to explore possible paths or simulate turns would be unnecessary because the parrot is allowed to choose any commands after the given prefix.

The main edge cases come from handling the final position correctly. A careless implementation can assume that the target is always to the upper right and forget that the remaining distance can require moving left or down. For example, with input:

```
1
R
0 0
```

the parrot ends at `(1, 0)`. The correct output is:

```
1
```

because one left move is enough. An implementation that only adds positive coordinate differences would incorrectly produce zero.

Another case is when the current route already reaches the destination. For example:

```
2
RU
1 1
```

The correct output is:

```
0
```

because no extra commands are needed. Code that always adds at least one move would fail here.

A third common mistake is confusing the current position with the destination coordinates. For:

```
3
DDD
0 -5
```

the current position is `(0, -3)`, so the remaining distance is two moves downward. The correct output is:

```
2
```

A solution that directly compares the target coordinates with the route length or ignores the simulated position would not handle this correctly.

## Approaches

The straightforward approach is to try to solve the problem by thinking about all possible appended command sequences. Since each new move can be one of four directions, a brute-force search of depth `k` would examine `4^k` possibilities for `k` added commands. This is correct because it checks every possible route extension, but it grows exponentially and quickly becomes impossible.

The brute force is unnecessary because the grid has a useful property: the order of moves does not matter when we only care about the final position. The existing commands simply determine how far away the parrot is from the destination. Once we know the horizontal and vertical differences, the shortest path is forced. Every horizontal difference requires exactly one horizontal move, and every vertical difference requires exactly one vertical move.

The observation that the Manhattan distance between two grid points gives the minimum number of axis-aligned moves reduces the entire problem to a single simulation pass followed by a simple calculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^k) | O(k) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the existing route and simulate it from the origin. Increase the x-coordinate for every right move, decrease it for every left move, increase the y-coordinate for every up move, and decrease it for every down move. This gives the exact position after the known part of the route.
2. Compute the horizontal difference between the destination and the current x-coordinate. Compute the vertical difference between the destination and the current y-coordinate. These values describe how far the parrot still needs to travel in each direction.
3. Add the absolute values of the two differences. The result is the minimum number of extra moves because each move can change exactly one coordinate by one unit.

Why it works: the invariant is that after processing any prefix of the given route, the stored coordinates exactly match the parrot's real location after that prefix. After the entire route is processed, the remaining displacement to the destination is known. Any valid continuation must fix every unit of horizontal and vertical difference, requiring at least `abs(dx) + abs(dy)` moves. Moving directly along those differences achieves exactly that many moves, so the value is both a lower bound and achievable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    x, y = map(int, input().split())

    cx = 0
    cy = 0

    for c in s:
        if c == 'R':
            cx += 1
        elif c == 'L':
            cx -= 1
        elif c == 'U':
            cy += 1
        elif c == 'D':
            cy -= 1

    print(abs(x - cx) + abs(y - cy))

if __name__ == "__main__":
    solve()
```

The first part of the code reads the route information and initializes the parrot's position at the origin. The simulation loop follows the same transitions described in the algorithm walkthrough, so the coordinates always represent the actual position after the processed prefix.

The final expression uses absolute differences because the parrot may need to correct its position in either direction. There is no need to construct the commands themselves, because only their minimum count is requested.

The implementation does not use any arrays or extra data structures. It also avoids unnecessary string operations by scanning the route once. Python integers do not have overflow issues for these coordinate calculations.

## Worked Examples

Consider the input:

```
6
UUDLRR
5 3
```

The trace is:

| Move processed | Current x | Current y |
| --- | --- | --- |
| Start | 0 | 0 |
| U | 0 | 1 |
| U | 0 | 2 |
| D | 0 | 1 |
| L | -1 | 1 |
| R | 0 | 1 |
| R | 1 | 1 |

The final position is `(1, 1)`. The target is `(5, 3)`, so the remaining displacement is four steps right and two steps up. The answer is:

```
6
```

This example shows that the algorithm only needs the final displacement, not the exact history of the path.

For a second example:

```
3
DDD
0 -5
```

The trace is:

| Move processed | Current x | Current y |
| --- | --- | --- |
| Start | 0 | 0 |
| D | 0 | -1 |
| D | 0 | -2 |
| D | 0 | -3 |

The target is two units below the current position. The answer is:

```
2
```

This confirms that negative coordinates are handled naturally by the absolute difference calculation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The route is scanned exactly once. |
| Space | O(1) | Only the current coordinates are stored. |

The algorithm performs a constant amount of work per movement command, so it easily fits within typical competitive programming limits even for very large routes.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    x, y = map(int, input().split())

    cx = 0
    cy = 0

    for c in s:
        if c == 'R':
            cx += 1
        elif c == 'L':
            cx -= 1
        elif c == 'U':
            cy += 1
        else:
            cy -= 1

    ans = abs(x - cx) + abs(y - cy)

    sys.stdin = old_stdin
    return str(ans)

assert solve_data("6\nUUDLRR\n5 3\n") == "6", "sample 1"
assert solve_data("3\nDDD\n0 -5\n") == "2", "sample 2"

assert solve_data("1\nR\n0 0\n") == "1", "opposite horizontal direction"
assert solve_data("2\nRU\n1 1\n") == "0", "already at destination"
assert solve_data("5\nLLLLL\n3 2\n") == "8", "large correction after negative movement"
assert solve_data("4\nUUUU\n0 100\n") == "96", "vertical boundary movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\nR\n0 0` | `1` | Handles moving back in the opposite direction. |
| `2\nRU\n1 1` | `0` | Handles the case where no extra moves are needed. |
| `5\nLLLLL\n3 2` | `8` | Checks negative current coordinates. |
| `4\nUUUU\n0 100` | `96` | Checks large remaining distance. |

## Edge Cases

For the case where the destination requires moving in the opposite direction from the current route, the algorithm works because it never assumes a direction. In:

```
1
R
0 0
```

the simulation gives `(1, 0)`. The differences are `-1` horizontally and `0` vertically, so the answer becomes `abs(-1) + abs(0) = 1`.

When the route already reaches the target, the remaining displacement is `(0, 0)`. For:

```
2
RU
1 1
```

the simulation ends at `(1, 1)`, making the answer `0`. The algorithm does not add unnecessary moves.

For paths that create negative coordinates, the simulation still follows the same rules. In:

```
3
DDD
0 -5
```

the parrot reaches `(0, -3)`. The remaining vertical distance is `-2`, and the absolute value gives the correct answer of `2`. The sign of the coordinate only determines direction, not the number of moves required.
