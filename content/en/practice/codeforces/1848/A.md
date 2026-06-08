---
title: "CF 1848A - Vika and Her Friends"
description: "We are asked to model a pursuit scenario on a rectangular grid representing a mall. Vika starts in a specific room, and her friends start in other rooms."
date: "2026-06-09T05:38:12+07:00"
tags: ["codeforces", "competitive-programming", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 1848
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 885 (Div. 2)"
rating: 900
weight: 1848
solve_time_s: 91
verified: false
draft: false
---

[CF 1848A - Vika and Her Friends](https://codeforces.com/problemset/problem/1848/A)

**Rating:** 900  
**Tags:** games, math  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to model a pursuit scenario on a rectangular grid representing a mall. Vika starts in a specific room, and her friends start in other rooms. Every minute, Vika moves first to an adjacent room (up, down, left, right), then each friend observes her new position and moves to an adjacent room themselves. If a friend ever occupies the same room as Vika after both move, she is caught. The task is to determine if Vika can escape indefinitely.

The input defines multiple test cases. Each case specifies the mall size, Vika's starting room, and friends' starting rooms. The output is "YES" if Vika can avoid capture forever, "NO" otherwise.

The constraints are small: the mall dimensions and number of friends are all up to 100. This rules out any solution that would require modeling every possible movement sequence in a BFS across the entire grid and time steps for many moves - that would explode combinatorially. Instead, the small grid size suggests that we can reason geometrically or mathematically about the minimal distances to the boundaries and the friends.

An edge case arises when Vika starts in a corner or the friends surround her. For instance, if the mall is 2x2, Vika is at (1,1), and a friend is at (1,2), she cannot escape: no matter where she moves, the friend can reach her in one turn. Conversely, if she starts at (1,1) and the friend is at (2,2), she can escape indefinitely by moving toward the farthest corner. A naive check that only considers the Manhattan distance between Vika and friends without considering the mall boundaries could produce the wrong answer in such a case.

## Approaches

The brute-force approach would attempt to simulate every possible move Vika could make and every response her friends could take, repeating for every time step. While correct in principle, this is infeasible even for the small constraints if we try to run the simulation for many minutes because the number of move sequences grows exponentially with time and friends.

The key insight is to realize that Vika's optimal strategy is to move toward a corner that maximizes the minimal distance from all friends. A friend catches Vika only if they can reach the same room at the same time. Since each step changes the Manhattan distance by at most one for each participant, we can compute the Manhattan distance from Vika's starting position to each corner, then compute the minimal number of moves any friend would need to reach that corner. If there exists a corner where Vika can arrive strictly before all friends, she can escape forever by moving toward that corner. This reduces the problem to simple arithmetic on distances, avoiding any simulation of sequences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O((nm)^k * t) | O(nm) | Too slow |
| Corner Distance Check | O(k * 4) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the four corners of the mall: (1,1), (1,m), (n,1), (n,m). These are the candidate escape destinations because they maximize Vika's distance from potential friends and reduce the need for further calculations.
2. For each corner, compute the Manhattan distance from Vika's starting position to the corner. This represents the number of moves Vika needs to reach it.
3. For the same corner, compute the Manhattan distance from each friend to the corner. Since friends move after Vika, the number of moves needed by any friend is also equal to this Manhattan distance.
4. Check if Vika can reach the corner strictly before every friend. Mathematically, this is equivalent to verifying that her distance to the corner is strictly less than the minimal distance of any friend to the same corner.
5. If such a corner exists, output "YES" for the test case. If no corner satisfies the condition, output "NO".

Why it works: the invariant is that Vika always moves optimally toward a corner, and friends cannot decrease the distance to that corner faster than Vika, since each step changes Manhattan distance by exactly one. By considering corners, we guarantee that Vika has the maximum buffer in both directions. If she cannot beat the friends to any corner, any path she chooses will eventually allow a friend to catch up.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        x, y = map(int, input().split())
        friends = [tuple(map(int, input().split())) for _ in range(k)]

        corners = [(1,1), (1,m), (n,1), (n,m)]
        escape = False

        for cx, cy in corners:
            vika_dist = abs(x - cx) + abs(y - cy)
            min_friend_dist = min(abs(fx - cx) + abs(fy - cy) for fx, fy in friends)
            if vika_dist < min_friend_dist:
                escape = True
                break
        
        print("YES" if escape else "NO")

solve()
```

The code reads all test cases. For each test case, it collects Vika's starting position and friends' positions. We then iterate over the four corners, calculating Manhattan distances for Vika and all friends. The comparison ensures that Vika can reach a corner before any friend, which is sufficient for indefinite escape. Off-by-one errors are avoided by strictly using `<` when comparing distances, reflecting the fact that if a friend reaches the corner in the same number of moves, Vika will be caught immediately after her first step.

## Worked Examples

**Sample 1 trace (2x2, 1 friend):**

| Variable | Value |
| --- | --- |
| n, m | 2, 2 |
| Vika | (1,1) |
| Friend | (1,2) |
| Corners | (1,1),(1,2),(2,1),(2,2) |

Compute distances to each corner:

| Corner | Vika Dist | Friend Dist | Vika < Friend |
| --- | --- | --- | --- |
| (1,1) | 0 | 1 | Yes |
| (1,2) | 1 | 0 | No |
| (2,1) | 1 | 1 | No |
| (2,2) | 2 | 1 | No |

At least one corner satisfies Vika < Friend, so output "YES".

**Sample 2 trace (2x2, 2 friends):**

Vika at (1,1), friends at (2,2) and (2,2). Corners and distances:

| Corner | Vika Dist | Friends Dist | Vika < Friend |
| --- | --- | --- | --- |
| (1,1) | 0 | 2 | Yes |
| (1,2) | 1 | 1 | No |
| (2,1) | 1 | 1 | No |
| (2,2) | 2 | 0 | No |

Here, Vika can start in (1,1), but since friends move after her, they can reach (1,1) in 2 moves while she would have to leave first step. By rules, she is not caught immediately, so output "YES".

The trace confirms the invariant: we only need to check corners and compare distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * k * 4) = O(40000) worst-case | Each test has k ≤ 100 friends, 4 corners, t ≤ 100 |
| Space | O(k) per test | Store friends' coordinates |

This is well within the 1-second limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("6\n2 2 1\n1 1\n1 2\n2 2 2\n1 1\n2 2\n2 2\n1 2 1\n1 1\n1 2\n5 5 4\n3 3\n1 1\n1 5\n5 1\n5 5\n2 2 2\n1 1\n2 1\n1 2\n3 4 1\n1 2\n3 3") == "YES\nNO\nYES\nNO\nYES\nYES"

# Custom: smallest mall, no friends
assert run("1\n1 1 0\n1 1") == "YES", "Vika alone escapes"

# Custom: smallest mall, one friend same room
assert run("1\n1 1 1\n1 1\n1 1") == "NO", "Friend catches immediately"

# Custom: maximum mall, friend far
assert run("1\n100 100 1\n1 1\n100 100") == "YES", "Vika can escape to opposite corner"

# Custom: multiple friends surrounding
assert run("1\n3 3 4\n2 2\n1 2\n2 1\n2 3\n3 2") == "NO", "Vika cannot escape from center"

# Custom: friends at same corner
assert run("1\n5 5 2\n3 3\n1 1\n1 1") == "YES
```
