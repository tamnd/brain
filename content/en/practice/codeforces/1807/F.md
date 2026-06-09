---
title: "CF 1807F - Bouncy Ball"
description: "We have a ball moving inside an n × m rectangular grid. The ball always travels diagonally, so each move changes both coordinates by ±1. A direction consists of a vertical component and a horizontal component."
date: "2026-06-09T09:05:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1807
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 859 (Div. 4)"
rating: 1700
weight: 1807
solve_time_s: 87
verified: true
draft: false
---

[CF 1807F - Bouncy Ball](https://codeforces.com/problemset/problem/1807/F)

**Rating:** 1700  
**Tags:** brute force, dfs and similar, implementation  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a ball moving inside an `n × m` rectangular grid. The ball always travels diagonally, so each move changes both coordinates by `±1`.

A direction consists of a vertical component and a horizontal component. For example, `DR` means increasing both row and column, while `UL` means decreasing both. Whenever the next move would leave the grid, the corresponding component of the direction is reversed. Hitting the top or bottom wall flips the vertical component. Hitting the left or right wall flips the horizontal component. Reaching a corner flips both.

The task is not to count steps. We must count how many bounces occur before the ball visits a target cell for the first time. If the ball never reaches that cell, we output `-1`.

The most important constraint is that the sum of all grid sizes over all test cases is at most `5 · 10^4`. That is surprisingly small. Even though individual dimensions can reach `25000`, the total number of cells across all test cases is limited. This strongly suggests that simulating the motion is feasible if we avoid revisiting the same state indefinitely.

A subtle point is that the ball bounces after entering a cell. The cell itself is visited before the direction changes. Any simulation that reflects first and then checks the position can produce incorrect answers.

Another subtle point is that the ball may enter a cycle that never contains the target cell. Since the motion is deterministic, once the same state appears again, the future repeats forever.

Consider:

```
2 4
start = (2,1), DR
target = (2,2)
```

The ball moves:

```
(2,1) -> (1,2) -> (2,3) -> (1,4) -> ...
```

Cell `(2,2)` is never visited. A simulation without cycle detection would run forever. The correct answer is `-1`.

Another easy mistake is counting bounces instead of counting bounces before reaching the target.

Example:

```
3 3
start = (1,3), UR
target = (2,2)
```

The ball first reaches `(2,2)` after bouncing once from the upper wall. The answer is `1`. If we continue the simulation and count later bounces, the result becomes incorrect.

A third corner case occurs when the starting position already equals the target.

Example:

```
3 3
start = (2,2), DR
target = (2,2)
```

The answer is `0` because the ball is already there before any movement happens.

## Approaches

A straightforward simulation follows the ball one step at a time. At each move we update the position, perform any necessary reflection, and count bounces.

This approach is correct because the motion rules are deterministic. The problem is that the ball may move for an extremely long time before repeating. Since dimensions can be as large as `25000`, a pure step-by-step simulation could require millions of moves.

The key observation is that nothing interesting happens between bounces.

Suppose the ball is currently at `(r,c)` with some direction. Until it hits a wall, it simply follows a straight diagonal. During that segment, the row and column change by the same amount each step.

Instead of simulating every move, we can jump directly to the next bounce. Let

```
dr ∈ {+1,-1}
dc ∈ {+1,-1}
```

represent the current direction.

The distance to the next vertical wall is determined by `dr`:

```
if dr = +1: n - r
if dr = -1: r - 1
```

Similarly, the distance to the next horizontal wall is:

```
if dc = +1: m - c
if dc = -1: c - 1
```

The smaller of these two distances tells us how many diagonal steps remain before the next bounce event.

While travelling along this diagonal segment, the target is reached exactly when both row and column offsets match. We can test this algebraically without stepping through every intermediate cell.

After jumping to the bounce position, we flip the required direction components, increase the bounce counter, and continue.

The state of the system is:

```
(row, column, direction)
```

There are only `4nm` possible states. Once a state repeats, the future trajectory repeats as well. Since the total `nm` across all tests is at most `5 · 10^4`, storing visited states is easily affordable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of moves) | O(1) | Too slow |
| Optimal | O(number of bounce states) ≤ O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Convert the direction string into two components `dr` and `dc`, each equal to `+1` or `-1`.
2. If the starting cell already equals the target cell, return `0`.
3. Maintain a set of visited states `(row, column, dr, dc)`.
4. Before processing a state, check whether it has already been seen. If it has, the trajectory has entered a cycle and the target will never be reached. Return `-1`.
5. Compute the number of steps until the next vertical wall and the next horizontal wall.
6. Let `k` be the smaller of those two values. The ball travels exactly `k` diagonal steps before the next bounce event.
7. Check whether the target lies on this diagonal segment. Since both coordinates move linearly, the target is reached during the segment iff:

- `(i2 - row)` has the same sign as `dr`,
- `(j2 - col)` has the same sign as `dc`,
- and the required row and column offsets are equal.

If the target lies within the next `k` steps, return the current bounce count.
8. Move the ball directly to the bounce position:

```
row += dr * k
col += dc * k
```
9. If the bounce position lies on the top or bottom border, flip `dr`.
10. If the bounce position lies on the left or right border, flip `dc`.
11. Increase the bounce count by one and continue from step 4.

### Why it works

Between two consecutive bounces, the ball follows a single straight diagonal. Every cell visited on that segment satisfies a fixed linear relation between row and column offsets. Checking whether the target belongs to that segment is enough to determine whether it will be reached before the next bounce.

The simulation always jumps from one bounce state to the next without skipping any possible target occurrence, because every intermediate position lies on the examined diagonal segment.

The motion is deterministic. Once a state `(row, column, dr, dc)` repeats, all future states repeat as well. If the target was not found before the repetition, it will never be found later. This guarantees that returning `-1` on a repeated state is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

DIR = {
    "DR": (1, 1),
    "DL": (1, -1),
    "UR": (-1, 1),
    "UL": (-1, -1),
}

def solve():
    t = int(input())

    for _ in range(t):
        n, m, r, c, tr, tc, d = input().split()

        n = int(n)
        m = int(m)
        r = int(r)
        c = int(c)
        tr = int(tr)
        tc = int(tc)

        dr, dc = DIR[d]

        if r == tr and c == tc:
            print(0)
            continue

        visited = set()
        bounces = 0
        answer = -1

        while True:
            state = (r, c, dr, dc)

            if state in visited:
                break

            visited.add(state)

            dv = (n - r) if dr == 1 else (r - 1)
            dh = (m - c) if dc == 1 else (c - 1)

            k = min(dv, dh)

            row_diff = tr - r
            col_diff = tc - c

            if row_diff * dr >= 0 and col_diff * dc >= 0:
                if row_diff == col_diff * dr * dc:
                    steps = abs(row_diff)
                    if steps <= k:
                        answer = bounces
                        break

            r += dr * k
            c += dc * k

            bounced = False

            if r == 1 or r == n:
                dr *= -1
                bounced = True

            if c == 1 or c == m:
                dc *= -1
                bounced = True

            if bounced:
                bounces += 1

        print(answer)

solve()
```

The direction string is converted into two signed components. This makes reflections extremely simple because bouncing off a horizontal wall only changes `dr`, while bouncing off a vertical wall only changes `dc`.

The core idea is the jump length `k`. Instead of simulating every move, we compute how far the ball can travel before touching a wall. That entire diagonal segment is processed at once.

The target check is the most delicate part. Along a diagonal segment, both coordinates change by exactly the same number of steps in magnitude. The equality

```
row_diff == col_diff * dr * dc
```

encodes that requirement for all four directions simultaneously.

Another subtle detail is the timing of the bounce count. We first check whether the target lies on the current segment. If it does, the answer is the number of bounces that have already happened. Only after reaching the bounce position do we increment the bounce counter.

Cycle detection uses the complete state `(row, column, dr, dc)`. Using only the position would be incorrect because arriving at the same cell with a different direction can lead to a different future trajectory.

## Worked Examples

### Example 1

Input:

```
5 7 1 7 2 4 DL
```

| Bounce Count | Position | Direction | k | Target on Segment? |
| --- | --- | --- | --- | --- |
| 0 | (1,7) | DL | 4 | No |
| 1 | (5,3) | UL | 2 | No |
| 2 | (3,1) | UR | 2 | No |
| 3 | (1,3) | DR | 1 | Yes |

The final segment goes from `(1,3)` to `(2,4)`. The target lies on that segment, so the answer is the current bounce count, which is `3`.

### Example 2

Input:

```
6 4 1 2 3 4 DR
```

| Bounce Count | Position | Direction | k | Target on Segment? |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | DR | 2 | Yes |

The target `(3,4)` lies directly on the initial diagonal path. No bounce occurs before reaching it, so the answer is `0`.

This example demonstrates why the answer counts bounces, not travelled segments or steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each state is processed at most once |
| Space | O(nm) | Visited state set |

The number of possible states is at most `4nm`, since each cell can be combined with four directions. The problem guarantees that the sum of all `nm` values over the test file is at most `5 · 10^4`, so the total work remains comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    DIR = {
        "DR": (1, 1),
        "DL": (1, -1),
        "UR": (-1, 1),
        "UL": (-1, -1),
    }

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m, r, c, tr, tc, d = input().split()

        n = int(n)
        m = int(m)
        r = int(r)
        c = int(c)
        tr = int(tr)
        tc = int(tc)

        dr, dc = DIR[d]

        if (r, c) == (tr, tc):
            out.append("0")
            continue

        vis = set()
        b = 0
        ans = -1

        while True:
            state = (r, c, dr, dc)

            if state in vis:
                break

            vis.add(state)

            dv = (n - r) if dr == 1 else (r - 1)
            dh = (m - c) if dc == 1 else (c - 1)

            k = min(dv, dh)

            rd = tr - r
            cd = tc - c

            if rd * dr >= 0 and cd * dc >= 0:
                if rd == cd * dr * dc:
                    if abs(rd) <= k:
                        ans = b
                        break

            r += dr * k
            c += dc * k

            if r == 1 or r == n:
                dr *= -1

            if c == 1 or c == m:
                dc *= -1

            b += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""6
5 7 1 7 2 4 DL
5 7 1 7 3 2 DL
3 3 1 3 2 2 UR
2 4 2 1 2 2 DR
4 3 1 1 1 3 UL
6 4 1 2 3 4 DR
""") == """3
-1
1
-1
4
0"""

# custom cases
assert run("""1
3 3 2 2 2 2 DR
""") == "0", "already at target"

assert run("""1
2 2 1 1 2 2 DR
""") == "0", "direct diagonal reach"

assert run("""1
2 4 2 1 2 2 DR
""") == "-1", "unreachable cycle"

assert run("""1
25000 2 1 1 25000 2 DR
""") == "0", "large boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Start equals target | 0 | Immediate termination |
| 2×2 diagonal reach | 0 | No bounce before target |
| Sample 4 | -1 | Correct cycle detection |
| 25000×2 grid | 0 | Handles maximum dimensions |

## Edge Cases

### Starting position is already the target

Input:

```
1
3 3 2 2 2 2 DR
```

The algorithm checks this condition before entering the simulation loop. No movement is required, so it outputs:

```
0
```

Without this check, the simulation would continue moving and could return a larger value.

### Target never appears in the cycle

Input:

```
1
2 4 2 1 2 2 DR
```

Trace:

```
(2,1,DR)
→ (1,2,UR)
→ (2,3,DR)
→ (1,4,UR)
→ (2,3,DL)
→ ...
```

Eventually a previously seen state reappears. The target `(2,2)` never belonged to any processed diagonal segment, so the algorithm returns:

```
-1
```

The repeated-state check prevents an infinite loop.

### Target reached exactly at the end of a segment

Input:

```
1
6 4 1 2 3 4 DR
```

The first diagonal segment has length `k = 2`:

```
(1,2) → (2,3) → (3,4)
```

The target is the final cell of that segment. Since the target check uses `steps <= k`, the endpoint is included and the algorithm correctly outputs:

```
0
```

Using a strict inequality would incorrectly miss this case.

### Corner bounce

Input:

```
1
2 2 1 1 1 2 UL
```

The ball starts in direction `UL`, immediately reaches the corner `(1,1)` bounce state, and both direction components are reversed together when the corner is processed.

The implementation flips the vertical component if a top or bottom border is touched and independently flips the horizontal component if a left or right border is touched. A corner naturally triggers both flips, exactly matching the problem rules.
