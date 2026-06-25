---
title: "CF 106188B - MLG 360 No Scope"
description: "We have a player standing at a coordinate (ex, ey) on a grid. The player is facing one of the eight compass directions and fires a bullet after a full rotation. The rotation does not change the final direction, so the bullet simply travels forever in the original direction."
date: "2026-06-25T10:46:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106188
codeforces_index: "B"
codeforces_contest_name: "UTPC x WiCS Contest 11-12-2025"
rating: 0
weight: 106188
solve_time_s: 37
verified: true
draft: false
---

[CF 106188B - MLG 360 No Scope](https://codeforces.com/problemset/problem/106188/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a player standing at a coordinate `(ex, ey)` on a grid. The player is facing one of the eight compass directions and fires a bullet after a full rotation. The rotation does not change the final direction, so the bullet simply travels forever in the original direction. Among all given enemy positions, we need to find the first enemy the bullet reaches. If the bullet path never contains an enemy, we print `-1`.

The input gives the number of enemies, the player's location, the facing direction, and the coordinates of every enemy. The output is the coordinates of the enemy closest to the player along that ray.

The coordinates are bounded by `100000`, and the number of enemies can also reach `100000`. A solution that checks every grid position in the bullet path can perform up to about `100000` checks per direction, which is unnecessary. Since there can be `100000` enemies, we want an algorithm that processes each enemy a constant number of times, giving an `O(n)` solution. Sorting is also possible, but a linear scan is enough because the number of possible directions is tiny.

The tricky cases come from confusing "same line" with "in the bullet path". For example, if the player is at `(1,1)` facing `NORTHEAST`, an enemy at `(3,3)` is hit and the answer is:

```
3 3
```

A careless solution that only checks the diagonal equation but forgets the direction might incorrectly accept `(0,0)` in a version of the problem where negative coordinates are allowed, because it is on the same diagonal but behind the player.

Another edge case is multiple enemies on the same ray. For input:

```
2 1 1
EAST
3 1
5 1
```

the correct output is:

```
3 1
```

The first enemy blocks the second one. Checking only whether any enemy lies in the direction and keeping the last one found can return the wrong target.

A final common mistake is handling the player's own tile. For example:

```
1 1 1
NORTH
1 1
```

The answer is:

```
1 1
```

The enemy is on the starting position and is the first entity encountered. A solution that only searches strictly forward from the next tile would miss it.

## Approaches

The straightforward approach is to simulate the bullet path. Starting from the player's position, move one tile at a time in the chosen direction and check whether there is an enemy at every visited coordinate. If we store enemies in a set, this can be implemented easily and is correct because the first coordinate encountered on the path is exactly the first enemy hit.

The problem is the amount of empty space the bullet may travel through. The coordinate range reaches `100000`, so a single simulation can require around `100000` steps. Repeating this over large inputs is still manageable in some cases, but it wastes work because most visited cells do not contain enemies. The grid is huge while the enemy count is only `100000`.

The key observation is that we only care about enemy coordinates. Every direction has a simple mathematical condition. For example, moving north means the enemy must have the same `x` coordinate and a `y` value not smaller than the player's. Moving northeast means the difference between `x` and `y` must match the player's difference. The ray condition tells us which enemies are candidates, and the distance from the player tells us which candidate is reached first.

During one scan over all enemies, we check whether the enemy lies on the ray. If it does, we compare its distance with the best candidate found so far. Because the ray only goes in one direction, the closest candidate is exactly the first one hit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max_coordinate) | O(n) | Too slow conceptually because it scans empty cells |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the player's position, direction, and all enemy positions. Convert the direction into a movement vector `(dx, dy)`. For example, north becomes `(0, 1)` and southwest becomes `(-1, -1)`. This lets every direction use the same logic.
2. For each enemy, compute the difference from the player:

`(tx, ty) = (enemy_x - ex, enemy_y - ey)`

The enemy can only be hit if it is somewhere along the vector `(dx, dy)`.
3. Check whether the enemy is on the same ray. A point `(tx, ty)` lies on the ray when there is some nonnegative distance `k` such that:

`tx = k * dx` and `ty = k * dy`

The signs must match the direction, and the ratio between coordinates must match. Because the movement vectors contain only `0`, `1`, or `-1`, this can be simplified into checking the line condition and direction.
4. If the enemy is valid, compute how far away it is. The squared distance is enough because we only compare values. The candidate with the smallest distance is the one hit first.
5. After all enemies are processed, print the stored answer. If no candidate was found, print `-1`.

Why it works: every enemy that can be hit must satisfy the ray equation, so the algorithm never ignores a possible target. Among all valid targets, the bullet reaches the one with the smallest distance first because the bullet travels continuously outward from the player. Keeping the minimum distance maintains the invariant that the stored answer is always the closest valid enemy seen so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, ex, ey = map(int, input().split())
    direction = input().strip()

    enemies = []
    for _ in range(n):
        x, y = map(int, input().split())
        enemies.append((x, y))

    moves = {
        "NORTH": (0, 1),
        "NORTHEAST": (1, 1),
        "EAST": (1, 0),
        "SOUTHEAST": (1, -1),
        "SOUTH": (0, -1),
        "SOUTHWEST": (-1, -1),
        "WEST": (-1, 0),
        "NORTHWEST": (-1, 1),
    }

    dx, dy = moves[direction]

    best_dist = float("inf")
    ans = None

    for x, y in enemies:
        tx = x - ex
        ty = y - ey

        if dx == 0:
            if tx != 0:
                continue
            if ty * dy < 0:
                continue
        elif dy == 0:
            if ty != 0:
                continue
            if tx * dx < 0:
                continue
        else:
            if tx * dy != ty * dx:
                continue
            if tx * dx < 0 or ty * dy < 0:
                continue

        dist = tx * tx + ty * ty
        if dist < best_dist:
            best_dist = dist
            ans = (x, y)

    if ans is None:
        print(-1)
    else:
        print(ans[0], ans[1])

if __name__ == "__main__":
    solve()
```

The direction dictionary maps each possible facing direction to a vector. This avoids writing separate logic for eight cases and makes the geometric check uniform.

The loop only examines enemy locations. The variables `tx` and `ty` represent the enemy's position relative to the player, which makes checking the ray much simpler than working with absolute coordinates.

For vertical directions, only the `x` coordinate must match. For horizontal directions, only the `y` coordinate must match. For diagonal directions, the relative coordinates must have the same ratio, which becomes the equality `tx * dy == ty * dx`.

The distance comparison uses squared distance because square roots are unnecessary. Comparing `a^2` and `b^2` gives the same ordering as comparing `a` and `b`. The coordinates are small enough that Python integers easily handle the multiplication.

## Worked Examples

For the first sample:

```
1 1 1
NORTHEAST
3 3
```

The state changes as follows:

| Enemy | Relative position | On ray | Distance | Current answer |
| --- | --- | --- | --- | --- |
| (3,3) | (2,2) | Yes | 8 | (3,3) |

The enemy has the same diagonal direction as the bullet, so it becomes the first target.

For the second example:

```
2 1 1
NORTHEAST
3 4
4 3
```

| Enemy | Relative position | On ray | Distance | Current answer |
| --- | --- | --- | --- | --- |
| (3,4) | (2,3) | No | ignored | none |
| (4,3) | (3,2) | No | ignored | none |

Neither enemy is on the diagonal `y = x` extending from the player, so the result is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every enemy is checked once with constant time arithmetic |
| Space | O(1) | Only the current best answer and a few variables are stored |

The solution fits the constraints because `100000` enemies require only `100000` iterations. The arithmetic operations inside each iteration are constant time.

## Test Cases

```python
import sys
import io

def solve(data):
    input = io.StringIO(data).readline

    n, ex, ey = map(int, input().split())
    direction = input().strip()

    moves = {
        "NORTH": (0, 1),
        "NORTHEAST": (1, 1),
        "EAST": (1, 0),
        "SOUTHEAST": (1, -1),
        "SOUTH": (0, -1),
        "SOUTHWEST": (-1, -1),
        "WEST": (-1, 0),
        "NORTHWEST": (-1, 1),
    }

    dx, dy = moves[direction]

    best = float("inf")
    ans = None

    for _ in range(n):
        x, y = map(int, input().split())
        tx, ty = x - ex, y - ey

        if dx == 0:
            if tx != 0 or ty * dy < 0:
                continue
        elif dy == 0:
            if ty != 0 or tx * dx < 0:
                continue
        else:
            if tx * dy != ty * dx or tx * dx < 0 or ty * dy < 0:
                continue

        dist = tx * tx + ty * ty
        if dist < best:
            best = dist
            ans = (x, y)

    if ans is None:
        return "-1"
    return f"{ans[0]} {ans[1]}"

# samples
assert solve("""1 1 1
NORTHEAST
3 3
""") == "3 3"

assert solve("""2 1 1
NORTHEAST
3 4
4 3
""") == "-1"

# custom cases
assert solve("""1 1 1
NORTH
1 1
""") == "1 1"

assert solve("""3 5 5
EAST
10 5
7 5
8 6
""") == "7 5"

assert solve("""4 10 10
SOUTHWEST
8 8
5 5
9 9
1 2
""") == "9 9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / NORTH / 1 1` | `1 1` | Starting position handling |
| `3 5 5 / EAST / 10 5, 7 5, 8 6` | `7 5` | Choosing the nearest enemy on a ray |
| `4 10 10 / SOUTHWEST / 8 8, 5 5, 9 9, 1 2` | `9 9` | Diagonal direction and ignoring unrelated points |

## Edge Cases

For the case where the enemy is behind the player, the ray direction check prevents a false match. If the player is at `(1,1)` facing `NORTHEAST`, an enemy at `(0,0)` would satisfy the diagonal equation but has a negative movement distance, so it is rejected.

For multiple enemies on the same line, the minimum distance comparison keeps the closest one. With:

```
2 1 1
EAST
3 1
5 1
```

the first enemy has distance `4`, while the second has distance `16`. The algorithm stores `(3,1)` and never replaces it with the farther enemy.

For a direction with zero movement in one coordinate, the special checks avoid division style logic. Facing north means all valid enemies must have the same `x`, and only enemies with `y >= ey` can be reached. This handles vertical and horizontal rays without any corner cases from comparing ratios.
