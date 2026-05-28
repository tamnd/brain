---
title: "CF 152B - Steps"
description: "We have a rectangular grid with n rows and m columns. Vasya starts at position (xc, yc). Then he processes k movement vectors one by one. For a vector (dx, dy), he repeatedly moves: He keeps moving in that direction until the next move would leave the grid."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 152
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 108 (Div. 2)"
rating: 1300
weight: 152
solve_time_s: 102
verified: true
draft: false
---

[CF 152B - Steps](https://codeforces.com/problemset/problem/152/B)

**Rating:** 1300  
**Tags:** binary search, implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular grid with `n` rows and `m` columns. Vasya starts at position `(xc, yc)`. Then he processes `k` movement vectors one by one.

For a vector `(dx, dy)`, he repeatedly moves:

```
(x, y) -> (x + dx, y + dy)
```

He keeps moving in that direction until the next move would leave the grid. After finishing one vector, he starts the next vector from his current position.

The task is to compute the total number of valid moves across all vectors.

The grid dimensions can be as large as `10^9`, which immediately rules out any simulation over cells of the grid itself. A single vector can also move Vasya up to roughly `10^9` times, so step-by-step simulation is impossible. Even though `k` is only `10^4`, the total number of performed moves may be enormous.

The core observation is that for each vector we do not actually need to simulate the movement. We only need to determine how many times the vector can be applied before one coordinate leaves the valid range.

Several edge cases are easy to mishandle.

Suppose the movement is purely vertical.

Input:

```
5 5
3 3
1
-2 0
```

The correct answer is:

```
1
```

After one move Vasya reaches `(1, 3)`. Another move would reach `(-1, 3)`, outside the grid. A careless solution that divides by both `dx` and `dy` without handling zeros separately will crash or produce garbage.

Negative directions are another common source of mistakes.

Input:

```
5 5
4 4
1
-1 -2
```

The correct answer is:

```
1
```

After one move Vasya reaches `(3, 2)`. Another move would reach `(2, 0)`, which is invalid because column `0` does not exist. If the formulas assume all directions are positive, the computed step count becomes incorrect.

There is also the case where no move is possible at all.

Input:

```
3 3
1 1
1
-1 0
```

The correct answer is:

```
0
```

The first move already leaves the board. Some implementations accidentally produce a negative number of steps and add it to the answer.

Finally, the answer itself can become very large. With dimensions up to `10^9` and up to `10^4` vectors, the total number of moves may exceed 32-bit integer range. Python handles this automatically, but C++ solutions must use `long long`.

## Approaches

The most direct solution is to simulate every move literally. For each vector `(dx, dy)`, we repeatedly check whether `(x + dx, y + dy)` remains inside the board. If it does, we move there and increment the answer.

This brute-force approach is correct because it exactly follows the rules of the game. The problem is the running time. A single vector might produce nearly `10^9` moves. With `10^4` vectors, the total work could reach around `10^13` operations, far beyond what fits in 2 seconds.

The key observation is that the movement along one vector is completely predictable. If Vasya is at `(x, y)` and uses vector `(dx, dy)`, after `t` moves he will be at:

```
(x + t * dx, y + t * dy)
```

We need the largest nonnegative integer `t` such that both coordinates stay inside the grid.

That means:

```
1 <= x + t * dx <= n
1 <= y + t * dy <= m
```

Each coordinate independently imposes an upper limit on `t`. The maximum valid number of steps is simply the minimum of those limits.

For example, if `dx > 0`, then:

```
x + t * dx <= n
t <= (n - x) / dx
```

If `dx < 0`, then:

```
x + t * dx >= 1
t <= (x - 1) / (-dx)
```

We do the same for `dy`, then take the minimum allowed value.

This reduces each vector from potentially billions of simulated moves to a constant amount of arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total steps) | O(1) | Too slow |
| Optimal | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the grid dimensions `n` and `m`.
2. Read the starting position `(x, y)`.
3. Initialize `answer = 0`.
4. Process each vector `(dx, dy)` independently.
5. Compute how many moves are allowed by the row coordinate.

If `dx > 0`, the limiting boundary is the bottom edge:

```
(n - x) // dx
```

If `dx < 0`, the limiting boundary is the top edge:

```
(x - 1) // (-dx)
```

If `dx == 0`, movement never changes the row, so the row coordinate imposes no restriction.
6. Compute how many moves are allowed by the column coordinate using the same logic.
7. The actual number of moves for this vector is the minimum restriction from both coordinates.

Both coordinates must remain valid simultaneously, so the tighter limit controls the movement.
8. Add this value to `answer`.
9. Update the current position:

```
x += steps * dx
y += steps * dy
```
10. After all vectors are processed, print `answer`.

### Why it works

For a fixed vector `(dx, dy)`, every move changes the position by the same amount. After `t` moves, the position is exactly:

```
(x + t * dx, y + t * dy)
```

The algorithm computes the largest `t` for which both coordinates remain inside the valid ranges. Any larger value would violate at least one boundary, so more moves are impossible. Any smaller value is obviously valid.

Because each vector is processed exactly according to these maximum valid moves, the algorithm reproduces the game's rules perfectly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
x, y = map(int, input().split())

k = int(input())

answer = 0

INF = 10**30

for _ in range(k):
    dx, dy = map(int, input().split())

    steps_x = INF
    steps_y = INF

    if dx > 0:
        steps_x = (n - x) // dx
    elif dx < 0:
        steps_x = (x - 1) // (-dx)

    if dy > 0:
        steps_y = (m - y) // dy
    elif dy < 0:
        steps_y = (y - 1) // (-dy)

    steps = min(steps_x, steps_y)

    answer += steps

    x += steps * dx
    y += steps * dy

print(answer)
```

The implementation follows the mathematical derivation directly.

For each vector we independently compute the maximum valid movement along rows and columns. The value `INF` represents "unlimited" movement for coordinates that never change. For example, if `dx == 0`, the row coordinate never leaves the grid, so only the column constraint matters.

The formulas differ depending on the sign of the direction. When moving downward with positive `dx`, the bottom boundary `n` becomes the limiting factor. When moving upward with negative `dx`, the top boundary `1` becomes the limiting factor.

The update step:

```
x += steps * dx
y += steps * dy
```

is important. The next vector starts from the final position after the current vector finishes.

Python integers automatically handle very large answers safely. In languages with fixed-width integers, the answer must use 64-bit storage.

## Worked Examples

### Sample 1

Input:

```
4 5
1 1
3
1 1
1 1
0 -2
```

| Vector | Current Position | steps_x | steps_y | Chosen Steps | New Position | Total Answer |
| --- | --- | --- | --- | --- | --- | --- |
| (1, 1) | (1, 1) | 3 | 4 | 3 | (4, 4) | 3 |
| (1, 1) | (4, 4) | 0 | 1 | 0 | (4, 4) | 3 |
| (0, -2) | (4, 4) | INF | 1 | 1 | (4, 2) | 4 |

The first vector moves diagonally until the row boundary blocks further movement. The second vector cannot move at all because the next row would be `5`. The last vector only changes columns, so only the column limit matters.

### Sample 2

Input:

```
3 3
1 2
1
-1 0
```

| Vector | Current Position | steps_x | steps_y | Chosen Steps | New Position | Total Answer |
| --- | --- | --- | --- | --- | --- | --- |
| (-1, 0) | (1, 2) | 0 | INF | 0 | (1, 2) | 0 |

The row restriction immediately becomes zero because moving upward from row `1` leaves the grid. The algorithm correctly handles the case where no movement is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each vector requires constant-time arithmetic |
| Space | O(1) | Only a few variables are stored |

With at most `10^4` vectors, this solution performs only a few arithmetic operations per vector. The runtime easily fits within the time limit, and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    x, y = map(int, input().split())

    k = int(input())

    ans = 0
    INF = 10**30

    for _ in range(k):
        dx, dy = map(int, input().split())

        sx = INF
        sy = INF

        if dx > 0:
            sx = (n - x) // dx
        elif dx < 0:
            sx = (x - 1) // (-dx)

        if dy > 0:
            sy = (m - y) // dy
        elif dy < 0:
            sy = (y - 1) // (-dy)

        steps = min(sx, sy)

        ans += steps

        x += steps * dx
        y += steps * dy

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup

    return out.getvalue().strip()

# provided sample
assert run(
"""4 5
1 1
3
1 1
1 1
0 -2
"""
) == "4", "sample 1"

# no movement possible
assert run(
"""3 3
1 1
1
-1 0
"""
) == "0", "blocked immediately"

# pure horizontal movement
assert run(
"""5 10
3 2
1
0 3
"""
) == "2", "horizontal only"

# negative diagonal movement
assert run(
"""5 5
4 4
1
-1 -2
"""
) == "1", "negative direction"

# huge values
assert run(
"""1000000000 1000000000
1 1
1
1 1
"""
) == "999999999", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3x3`, move `(-1,0)` from `(1,1)` | `0` | Immediate boundary collision |
| Horizontal-only movement | `2` | Correct handling of `dx = 0` |
| Negative diagonal movement | `1` | Correct formulas for negative directions |
| Maximum coordinates | `999999999` | Large arithmetic and 64-bit safety |

## Edge Cases

Consider movement where one coordinate never changes.

Input:

```
5 10
3 2
1
0 3
```

The algorithm sets `steps_x = INF` because `dx = 0`. For the column movement:

```
(10 - 2) // 3 = 2
```

So the final answer is `2`. The moves are:

```
(3,2) -> (3,5) -> (3,8)
```

Another move would reach column `11`, outside the grid.

Now consider negative movement.

Input:

```
5 5
4 4
1
-1 -2
```

For rows:

```
(4 - 1) // 1 = 3
```

For columns:

```
(4 - 1) // 2 = 1
```

The minimum is `1`, so only one move is possible. After moving to `(3,2)`, another move would attempt `(2,0)`, which is invalid.

Finally, consider a completely blocked move.

Input:

```
3 3
1 1
1
-1 0
```

For rows:

```
(1 - 1) // 1 = 0
```

For columns, movement is unrestricted because `dy = 0`.

The minimum becomes `0`, so the algorithm performs no movement and leaves the answer unchanged.
