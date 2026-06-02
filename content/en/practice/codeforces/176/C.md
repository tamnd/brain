---
title: "CF 176C - Playing with Superglue"
description: "We have two chips on an $n times m$ grid. On each turn, the first player moves exactly one non-glued chip by one square in the four-neighbor grid. After that, the second player permanently glues one currently empty square. A chip is allowed to move onto a glued square."
date: "2026-06-02T17:16:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 2000
weight: 176
solve_time_s: 215
verified: false
draft: false
---

[CF 176C - Playing with Superglue](https://codeforces.com/problemset/problem/176/C)

**Rating:** 2000  
**Tags:** combinatorics, constructive algorithms  
**Solve time:** 3m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We have two chips on an $n \times m$ grid. On each turn, the first player moves exactly one non-glued chip by one square in the four-neighbor grid. After that, the second player permanently glues one currently empty square.

A chip is allowed to move onto a glued square. The moment it does so, that chip becomes permanently stuck. The first player wins immediately when the two chips occupy the same square. The second player wins if both chips become unable to move before they ever meet.

The board dimensions can be as large as $100 \times 100$, but that turns out to be misleading. The winning condition depends only on the relative displacement of the two chips, not on the total number of cells. The state space of the full game is enormous because glue placement accumulates over time, so any attempt to model the entire game tree is hopeless.

A naive implementation might try to represent all glued cells and run a minimax search. Even on a $10 \times 10$ board there are already $100$ possible glue locations on the first move, then $99$ on the next move, and so on. The branching factor explodes immediately.

The tricky part is that the board size itself is mostly irrelevant. Two chips very far apart give the second player enough time to build barriers and force both chips to become trapped. Two chips close together can usually meet before the glue becomes decisive.

One easy mistake is to look only at Manhattan distance. For example:

```
10 10 1 1 5 5
```

Here the displacement is $(4,4)$. The Manhattan distance is only $8$, but the correct answer is `Second`. A strategy based only on distance would incorrectly predict a win for the first player.

Another subtle case is:

```
10 10 1 1 4 5
```

The displacement is $(3,4)$. This is also a losing configuration for the first player even though many nearby positions are winning.

A final trap is assuming that every position inside a $5 \times 5$ neighborhood is winning. The pairs $(3,4)$ and $(4,4)$ are special exceptions.

## Approaches

The brute-force idea is straightforward. Represent the entire board, track which cells are glued, generate every legal move for the first player and every glue placement for the second player, then run minimax.

This is correct because it explores the complete game tree. The problem is that the number of reachable positions grows astronomically. After only a handful of turns there are already millions of distinct glue configurations. No search-based solution can survive within the limits.

The key observation is that optimal play depends only on the relative position of the two chips. After analyzing the game, one finds a remarkably small set of losing configurations.

Let

$$dx = |x_1 - x_2|,\qquad dy = |y_1 - y_2|$$

and reorder them so that $dx \le dy$.

The complete solution is:

If $dy > 4$, the second player wins.

If $(dx,dy) = (4,4)$, the second player wins.

If $(dx,dy) = (3,4)$, the second player wins.

Every other position is winning for the first player. This characterization was the intended solution of the problem.

Once this pattern is known, the game reduces to a few integer comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the board dimensions and the coordinates of the two chips.
2. Compute the absolute coordinate differences:

$$dx = |x_1 - x_2|$$

$$dy = |y_1 - y_2|$$

Only the relative displacement matters.
3. Reorder the values so that $dx \le dy$.

This lets us treat symmetric positions identically.
4. If $dy > 4$, output `"Second"`.

Positions separated by more than four cells in one direction are losing for the first player.
5. If $(dx,dy) = (4,4)$, output `"Second"`.
6. If $(dx,dy) = (3,4)$, output `"Second"`.
7. In every remaining case, output `"First"`.

### Why it works

The game has a complete classification in terms of the relative displacement between the chips. After normalizing so that $dx \le dy$, every position outside the $5 \times 5$ neighborhood is losing for the first player because the second player can always create enough glued cells before the chips can meet. Inside that neighborhood, exhaustive game analysis leaves only two losing configurations, $(3,4)$ and $(4,4)$. Every other normalized displacement admits a forcing strategy for the first player.

Because the algorithm implements exactly this characterization, its answer is correct for every legal input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, x1, y1, x2, y2 = map(int, input().split())

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    if dx > dy:
        dx, dy = dy, dx

    if dy > 4:
        print("Second")
    elif (dx, dy) == (4, 4):
        print("Second")
    elif (dx, dy) == (3, 4):
        print("Second")
    else:
        print("First")

if __name__ == "__main__":
    solve()
```

The first section computes the relative displacement between the chips. The actual coordinates and even the board dimensions cease to matter after this step.

The swap guarantees that equivalent positions such as $(1,4)$ and $(4,1)$ are represented by the same pair. Forgetting this normalization would misclassify symmetric positions.

The remaining logic directly implements the winning-position characterization. The order of checks is not important, but testing `dy > 4` first makes the structure slightly clearer.

No overflow issues exist because every value is at most $100$.

## Worked Examples

### Example 1

Input:

```
1 6 1 2 1 6
```

| Variable | Value |
| --- | --- |
| dx | 0 |
| dy | 4 |
| Normalized pair | (0, 4) |
| Losing pattern? | No |
| Answer | First |

The position lies inside the winning region and is not one of the two exceptional losing states.

### Example 2

Input:

```
10 10 1 1 10 10
```

| Variable | Value |
| --- | --- |
| dx | 9 |
| dy | 9 |
| Normalized pair | (9, 9) |
| dy > 4 ? | Yes |
| Answer | Second |

The chips start too far apart. The second player has enough time to control the board before a meeting becomes possible.

This example demonstrates the most important invariant of the solution: once the larger coordinate difference exceeds four, the exact geometry no longer matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons |
| Space | O(1) | Constant extra memory |

The board can contain up to $10{,}000$ cells, but the algorithm never examines individual cells. It performs a fixed amount of work regardless of board size, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n, m, x1, y1, x2, y2 = map(int, input().split())

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    if dx > dy:
        dx, dy = dy, dx

    if dy > 4 or (dx, dy) == (4, 4) or (dx, dy) == (3, 4):
        print("Second")
    else:
        print("First")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("1 6 1 2 1 6\n") == "First", "sample 1"
assert run("6 5 4 3 2 1\n") == "First", "sample 2"
assert run("10 10 1 1 10 10\n") == "Second", "sample 3"

# custom cases
assert run("1 2 1 1 1 2\n") == "First", "minimum board"
assert run("10 10 1 1 5 5\n") == "Second", "(4,4) losing state"
assert run("10 10 1 1 4 5\n") == "Second", "(3,4) losing state"
assert run("100 100 1 1 1 5\n") == "First", "boundary dy=4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 1 1 1 2` | `First` | Smallest legal board |
| `10 10 1 1 5 5` | `Second` | Special losing state (4,4) |
| `10 10 1 1 4 5` | `Second` | Special losing state (3,4) |
| `100 100 1 1 1 5` | `First` | Boundary case where dy equals 4 |

## Edge Cases

Consider:

```
10 10 1 1 5 5
```

We obtain $dx = 4$, $dy = 4$. The algorithm reaches the explicit $(4,4)$ check and outputs `Second`. A solution based only on the rule "all positions with differences at most four are winning" would fail here.

Now consider:

```
10 10 1 1 4 5
```

The normalized displacement is $(3,4)$. This is the other exceptional losing state. The dedicated check correctly returns `Second`.

Finally:

```
100 100 1 1 1 6
```

The normalized displacement is $(0,5)$. Since $dy > 4$, the algorithm immediately outputs `Second`. This confirms that the large-distance rule takes precedence over all smaller local patterns. The answer is determined without considering the actual board dimensions.
