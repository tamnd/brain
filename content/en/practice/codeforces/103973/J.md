---
title: "CF 103973J - Two Kings"
description: "We are given two kings on an infinite chessboard. One king belongs to Walk Alone (white) and the other to Salix Leaf (black). They alternate moves starting with white, and each king moves like a standard chess king, meaning it can step to any of the eight neighboring squares."
date: "2026-07-02T06:22:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103973
codeforces_index: "J"
codeforces_contest_name: "2022 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103973
solve_time_s: 50
verified: true
draft: false
---

[CF 103973J - Two Kings](https://codeforces.com/problemset/problem/103973/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two kings on an infinite chessboard. One king belongs to Walk Alone (white) and the other to Salix Leaf (black). They alternate moves starting with white, and each king moves like a standard chess king, meaning it can step to any of the eight neighboring squares.

There is an extra restriction: a king is not allowed to move into any square that is adjacent to the other king. In practice, this means the two kings must always remain at a Chebyshev distance strictly greater than 1 after every move.

White’s objective is not to capture or reach a specific square, but to eventually reach some position with arbitrarily large x-coordinate, formally a cell of the form (10^100, y). Since the board is infinite, this is equivalent to asking whether white can keep increasing its x-coordinate indefinitely without ever being blocked. Black’s objective is to prevent this from ever becoming possible.

Each test case gives the initial coordinates of both kings. We must determine whether white has a forced strategy to eventually escape to the right forever, assuming both players play optimally.

The constraints allow up to 100,000 test cases with coordinates up to 10^9 in absolute value. This immediately rules out any simulation of the game. Even a single game can last arbitrarily many moves, and each move depends on global strategy rather than local greed, so any solution must reduce the problem to a constant-time geometric condition per test case.

A subtle point is that movement is constrained by proximity. Even if black is far away in Euclidean terms, it may still be able to interfere if it can align itself in front of white before white advances too far. Another important edge case is when black starts ahead in the x direction but is significantly offset in y. Intuition might suggest black always wins when it is ahead, but this is not true because vertical separation can prevent black from forming an effective blocking line.

## Approaches

A brute-force interpretation of the game would simulate all legal moves of both kings and run a minimax search over the infinite game tree. Each state consists of two positions on an infinite grid, and from each state both players have up to eight possible moves, with additional legality constraints due to adjacency restrictions. Even with memoization, the state space is unbounded because coordinates are not bounded and kings can drift arbitrarily far. This makes brute-force fundamentally impossible.

The key observation is that the only thing that matters is relative geometry between the two kings. White’s objective depends only on whether black can ever permanently prevent increases in the x-coordinate. Since both kings move at the same speed and have identical movement capabilities, black can only control white if it can consistently maintain a “blocking position” in front of white along the x-axis.

This turns the problem into understanding whether black can reach and maintain a position aligned with white in time. The decisive factor becomes whether black can reduce the horizontal gap while also compensating for vertical separation. If black is too far vertically relative to the horizontal distance, it cannot simultaneously close the gap and align itself in front of white before white slips past.

This leads to a simple geometric condition on the initial configuration: compare horizontal distance with vertical offset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Simulation | O(infinite) | O(state space) | Too slow |
| Geometric Reduction | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Extract coordinates and compute relative position

For each test case, we take white at (x1, y1) and black at (x2, y2). We compute dx = x2 - x1 and dy = y2 - y1. This transforms the problem into analyzing whether black is initially to the right and how far it is vertically displaced.

The sign of dx immediately determines whether black is already behind white. If black starts behind or at the same x-coordinate, it cannot establish a permanent barrier in front, since white can always keep moving rightward first.

### 2. Handle the case where black is not ahead

If dx <= 0, white is already at least as far right as black. Since white moves first and only cares about increasing x, black cannot form a blocking wall ahead of white. White wins immediately in this scenario.

### 3. When black is ahead, compare vertical offset to horizontal advantage

If dx > 0, black is initially in front. Now the only question is whether black can align itself vertically with white quickly enough to block progress.

We compare |dy| with dx. The value dx represents how many steps black is ahead horizontally, which is also the number of moves available before white can potentially bypass its x-position. During that time, black must also correct vertical separation of |dy| to align itself in front of white.

If |dy| < dx, black has enough time to adjust vertically and still remain in front of white, allowing it to form an effective barrier.

If |dy| >= dx, black cannot both close the vertical gap and maintain its horizontal lead in time, so white can always find a path to slip past and continue increasing x indefinitely.

### 4. Decide the winner

If black is ahead and |dy| < dx, output Salix Leaf. Otherwise output Walk Alone.

### Why it works

The key invariant is that blocking white requires black to eventually occupy a position on or ahead of white’s x-frontier while also staying adjacent enough in y to prevent bypassing. Because both kings move one step per turn, horizontal progress acts as a strict time budget for black to fix vertical misalignment. If that budget is insufficient, white can always maintain forward progress in x by exploiting remaining horizontal slack.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        dx = x2 - x1
        dy = y2 - y1

        if dx <= 0:
            print("Walk Alone")
        else:
            if abs(dy) < dx:
                print("Salix Leaf")
            else:
                print("Walk Alone")

if __name__ == "__main__":
    solve()
```

The solution reads each test case and reduces it to two differences. The first decision point checks whether black is already ahead in the x-direction. If not, white trivially wins because black cannot establish a forward barrier.

When black is ahead, the only relevant comparison is between horizontal lead and vertical separation. The strict inequality `abs(dy) < dx` is crucial: equality is not sufficient for black because in the borderline case, white can always maintain just enough horizontal progress to prevent full alignment, breaking the blocking strategy.

All operations are constant time per test case, so the solution easily handles 100,000 inputs.

## Worked Examples

### Example 1

Input:

(0, -1) and (2, 1)

| dx | dy | Condition | Winner |
| --- | --- | --- | --- |
| 2 | 2 | 2 < 2 is false | Walk Alone |

Here black is ahead, but its vertical offset is too large relative to its horizontal advantage. It cannot align fast enough before white keeps advancing, so white escapes.

### Example 2

Input:

(-2, 3) and (2, 3)

| dx | dy | Condition | Winner |
| --- | --- | --- | --- |
| 4 | 0 | 0 < 4 is true | Salix Leaf |

Black is directly aligned horizontally with white and far enough ahead. It can immediately establish a blocking position and maintain it, preventing white from ever gaining a clear path to the right.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires only constant-time arithmetic |
| Space | O(1) | No auxiliary structures beyond input variables |

The constraints allow up to 10^5 test cases, and the solution performs only a few integer operations per case, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        x1, y1, x2, y2 = map(int, input().split())
        dx = x2 - x1
        dy = y2 - y1
        if dx <= 0:
            print("Walk Alone")
        else:
            print("Salix Leaf" if abs(dy) < dx else "Walk Alone")

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("3\n0 -1 2 1\n-2 3 2 3\n2 0 -1 0") == "Walk Alone\nSalix Leaf\nWalk Alone"

# black ahead but diagonal too large
assert run("1\n0 0 3 3") == "Walk Alone"

# black directly ahead aligned
assert run("1\n0 0 3 0") == "Salix Leaf"

# white already ahead
assert run("1\n5 0 2 0") == "Walk Alone"

# equality boundary case
assert run("1\n0 0 2 2") == "Walk Alone"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample set | mixed | correctness on given cases |
| (0,0)-(3,3) | Walk Alone | diagonal equality boundary |
| (0,0)-(3,0) | Salix Leaf | clean blocking case |
| white ahead | Walk Alone | dx <= 0 case |
| equal dx=dy | Walk Alone | strict inequality behavior |

## Edge Cases

When black starts ahead but exactly matches the vertical offset in magnitude, such as (0,0) and (2,2), the algorithm classifies it as white win because abs(dy) is not strictly less than dx. In this situation, black’s ability to correct vertical misalignment is just tight enough that it cannot simultaneously maintain a forward blocking position, allowing white to keep progressing in x.

When black is behind in x, such as white at (2,0) and black at (-1,0), dx is negative and the algorithm immediately returns Walk Alone. Even though black might move toward white, it cannot ever become a persistent forward blocker since white always retains initiative in the x-direction.
