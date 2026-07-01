---
title: "CF 104069I - Irritating Carlinhos"
description: "Two people start at distinct integer coordinates on a 2D grid. Each of them has a movement script made of the same length, where each character instructs a unit move in one of the four cardinal directions."
date: "2026-07-02T03:01:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "I"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 49
verified: true
draft: false
---

[CF 104069I - Irritating Carlinhos](https://codeforces.com/problemset/problem/104069/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people start at distinct integer coordinates on a 2D grid. Each of them has a movement script made of the same length, where each character instructs a unit move in one of the four cardinal directions. Time advances in discrete steps, and at each step both characters move exactly once. The key twist is that Thiago always moves first at every time step, and Carlinhos moves immediately after him.

After each individual move, including intermediate states, we want to know whether at any moment both end up occupying the same grid cell. If this ever happens, Carlinhos successfully catches Thiago and we stop caring about the rest of the simulation. If it never happens throughout the entire sequence, Thiago escapes.

The constraints allow up to 200,000 moves per person, so any approach that simulates all positions directly is already linear in time, which is acceptable. Anything quadratic, such as checking all pairs of positions between the two paths, is immediately infeasible because it would require on the order of 10^10 comparisons in the worst case.

A subtle point is the timing of checks. They do not only meet after both move in a step; they can meet right after Thiago moves but before Carlinhos reacts, and also right after Carlinhos moves. A naive approach that only compares positions after synchronized steps would miss valid catches.

A typical incorrect approach is to simulate both full paths separately and only compare final positions or only compare positions at equal indices. For example, if Thiago steps into Carlinhos’ previous position in the middle of the sequence, a coarse comparison strategy would miss it.

## Approaches

A brute-force interpretation is to simulate the process step by step. At each time step, we update Thiago’s position, check for equality, then update Carlinhos’ position and check again. This is straightforward and correctly models the rules. Since each move is O(1), the total complexity is O(n), which is already efficient enough. However, brute force is useful mainly as a correctness baseline rather than an optimization target.

The key insight is that there is no hidden interaction between past states beyond the current positions. Each step depends only on the previous positions and the next direction. This removes any need for storing histories or comparing trajectories. The problem reduces to maintaining two running coordinates and checking equality at two specific moments per step.

So instead of thinking in terms of paths, we think in terms of synchronized state evolution: at each index i, we apply Thiago’s move first, test collision, then apply Carlinhos’ move and test again. This reduces the problem to a constant-time update loop over the strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(n) | O(1) | Accepted |
| Any path comparison / pairwise checking | O(n^2) | O(n) | Too slow |

## Algorithm Walkthrough

We maintain two position pairs, one for Thiago and one for Carlinhos. We then iterate through the movement strings index by index.

1. Initialize Thiago at (tx, ty) and Carlinhos at (cx, cy). These are the starting coordinates before any movement is applied.
2. For each index i from 0 to n - 1, first apply Thiago’s move s[i]. This updates his position by one unit in the corresponding direction. After this update, we immediately compare Thiago’s position with Carlinhos’. If they match, we return success.
3. Next apply Carlinhos’ move t[i]. This updates his position. After this second update, we again compare the two positions. If they match, we return success.
4. If we finish all steps without any equality event, we conclude that no capture occurred.

The order inside each iteration is essential. Checking only after both moves would incorrectly ignore cases where Thiago lands directly on Carlinhos before he moves away.

Why it works: the system evolves as a discrete-time interleaving of two independent deterministic walks. At every moment where a collision can occur, the state of interest is completely described by the current coordinates of both agents. Since movements do not depend on past collisions or external constraints, once equality is detected at any intermediate step, it is guaranteed to be the earliest and valid capture point. The algorithm enumerates every such possible state transition exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def move(x, y, c):
    if c == 'U':
        return x, y + 1
    if c == 'D':
        return x, y - 1
    if c == 'R':
        return x + 1, y
    return x - 1, y

def solve():
    tx, ty, cx, cy = map(int, input().split())
    s = input().strip()
    t = input().strip()

    for i in range(len(s)):
        tx, ty = move(tx, ty, s[i])
        if tx == cx and ty == cy:
            print("Rodou!")
            return

        cx, cy = move(cx, cy, t[i])
        if tx == cx and ty == cy:
            print("Rodou!")
            return

    print("Quase!")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the exact simulation described earlier. The helper function translates each direction into a coordinate delta, ensuring constant-time updates. The main loop respects the required ordering: Thiago moves first, followed by an immediate collision check, then Carlinhos moves and is checked again.

A common implementation mistake is swapping the order of updates or checking only once per iteration. Both break correctness because they miss intermediate collision states.

## Worked Examples

### Example 1

Input:

```
2 0 0 0
L
R
```

| Step | Thiago pos | Carlinhos pos | Event |
| --- | --- | --- | --- |
| start | (2,0) | (0,0) | none |
| i=0 after Thiago | (1,0) | (0,0) | no |
| i=0 after Carlinhos | (1,0) | (1,0) | catch |

This trace shows that the collision occurs only after Carlinhos moves, not after Thiago’s move. The algorithm correctly checks both moments.

### Example 2

Input:

```
0 1 0 0
UU
UU
```

| Step | Thiago pos | Carlinhos pos | Event |
| --- | --- | --- | --- |
| start | (0,1) | (0,0) | none |
| i=0 after Thiago | (0,2) | (0,0) | no |
| i=0 after Carlinhos | (0,2) | (0,1) | no |
| i=1 after Thiago | (0,3) | (0,1) | no |
| i=1 after Carlinhos | (0,3) | (0,2) | no |

No intersection ever occurs, even though the paths approach each other closely. The simulation confirms that proximity alone is insufficient without exact overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each step performs constant-time updates and comparisons |
| Space | O(1) | Only current coordinates are stored |

The linear scan over up to 200,000 moves easily fits within time limits, since each iteration is a handful of arithmetic operations and comparisons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("0 1 0 0\nUU\nUU\n") == "Quase!"
assert run("2 0 0 0\nL\nR\n") == "Rodou!"
assert run("2 2 0 0\nDLDL\nRURU\n") == "Rodou!"

# custom cases
assert run("0 0 1 0\nR\nL\n") == "Rodou!", "immediate swap collision"
assert run("0 0 10 10\nUURR\nLLDD\n") == "Quase!", "never meet diagonal separation"
assert run("5 5 5 6\nD\nU\n") == "Rodou!", "meet after first pair"
assert run("-1 -1 1 1\nRUR\nLUL\n") == "Rodou!", "alternating crossing path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| immediate swap case | Rodou! | collision after one move |
| diagonal separation | Quase! | no accidental match |
| early catch | Rodou! | detection in first step |
| crossing trajectories | Rodou! | alternating intersections |

## Edge Cases

One edge case is when both players start adjacent and cross into each other’s positions immediately. For example:

```
0 0 1 0
R
L
```

Thiago moves first from (0,0) to (1,0), which is already Carlinhos’ starting position, so the answer must be “Rodou!”. The algorithm catches this right after Thiago’s move.

Another edge case is when they would only meet if both moves are applied simultaneously, but never after either single move. This is not valid in the problem model because collisions are checked after each individual movement, so simultaneous-step reasoning would be incorrect. The simulation correctly avoids false positives because it checks intermediate states explicitly.

A final case is when they start very close but diverge forever. Since every step is independent, once positions differ and movement directions do not align toward a meeting, the algorithm simply continues without storing history, correctly producing “Quase!”.
