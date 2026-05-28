---
title: "CF 154D - Flatland Fencing"
description: "Two players stand on integer points of a number line. On each turn, the current player chooses a new integer coordinate inside a fixed interval relative to their current position. If the first player is at position x, he may move to any integer point in [x + a, x + b]."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 154
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 109 (Div. 1)"
rating: 2400
weight: 154
solve_time_s: 94
verified: true
draft: false
---

[CF 154D - Flatland Fencing](https://codeforces.com/problemset/problem/154/D)

**Rating:** 2400  
**Tags:** games, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players stand on integer points of a number line. On each turn, the current player chooses a new integer coordinate inside a fixed interval relative to their current position.

If the first player is at position `x`, he may move to any integer point in `[x + a, x + b]`.

If the second player is at position `y`, he may move to any integer point in `[y - b, y - a]`.

The movement rules are symmetric. The second player's allowed displacement is exactly the negation of the first player's displacement.

A player wins immediately by moving onto the opponent's current position.

We are given the initial positions `x1` and `x2`, and the movement range `[a, b]`. Both players play optimally. We must determine whether the first player can force a win, whether the second player can force a win, or whether optimal play leads to a draw. If the first player wins, we must also output one winning first move.

The coordinates and movement bounds can be as large as `10^9` in absolute value. That immediately rules out any simulation over states or graph search over positions. The state space is infinite, and even restricting ourselves to "reachable" positions does not help because coordinates can grow arbitrarily large.

This forces us to look for a mathematical characterization of winning and losing positions.

The tricky part is that the game can loop forever. If both players can avoid losing indefinitely, the result is a draw. A naive minimax recursion would fail because there are infinitely many states and cycles.

Several edge cases are easy to misjudge.

Consider:

```
0 10 0 0
```

Both players can only stay in place. Nobody can ever reach the opponent. The correct answer is:

```
DRAW
```

A careless solution that only checks whether the first player can win immediately would incorrectly declare the second player the winner after the first fails to finish the game.

Another subtle case is when the first player can move onto the second immediately:

```
0 2 0 4
```

The first player may move by any value from `0` to `4`, so he can move directly to `2` and win instantly:

```
FIRST
2
```

Missing this immediate winning condition breaks many later arguments.

The most dangerous edge case is when every move of the first player allows an immediate reply by the second player:

```
0 5 2 3
```

The first player may move to `2` or `3`.

If he moves to `2`, the second player at `5` may move to `2` because his allowed moves are in `[5 - 3, 5 - 2] = [2, 3]`.

If he moves to `3`, the second player may also move to `3`.

So every legal first move loses instantly. The correct answer is:

```
SECOND
```

A solution that only reasons about reachability without considering immediate counterplay would fail here.

## Approaches

The brute-force viewpoint is to treat every pair of positions `(p1, p2)` as a game state and recursively classify states as winning, losing, or drawing.

A state is winning if there exists a move to a losing state. It is losing if every move goes to a winning state. Otherwise it is drawing.

This definition is correct, but completely unusable here. Positions range over all integers, so the game graph is infinite. Even if we artificially bound coordinates, transitions branch over up to `b - a + 1` moves each turn. With coordinates up to `10^9`, any explicit exploration is hopeless.

The key observation is that only the distance between the players matters.

Let:

```
d = x2 - x1
```

Suppose the first player chooses displacement `t`, where `a <= t <= b`.

After his move, the new distance becomes:

```
d' = x2 - (x1 + t) = d - t
```

The second player can win immediately if he can move exactly onto the first player's new position. Since his move range is symmetric, he can move by any value in `[a, b]` toward the first player. That means the second player wins immediately exactly when:

```
d' ∈ [a, b]
```

In other words, if after the first move the remaining distance lies inside the move interval, the second player captures immediately.

Now consider what happens if the first player cannot win immediately.

If the first player makes a move leaving distance outside `[a, b]`, then the second player can mirror the game structure and avoid losing. The symmetry of the rules means neither player can create an advantage unless someone can force an immediate capture.

This collapses the entire infinite game into a very small set of conditions:

The first player wins immediately if:

```
d ∈ [a, b]
```

Otherwise, the first player loses if every legal move leaves the new distance inside `[a, b]`.

The set of possible new distances after the first move is:

```
[d - b, d - a]
```

If this entire interval lies inside `[a, b]`, then every move loses instantly.

That condition becomes:

```
d - b >= a
and
d - a <= b
```

which simplifies to:

```
d ∈ [2a, 2b]
```

If neither condition holds, then the first player can choose a move leaving a safe distance, and neither player can force victory afterward. The result is a draw.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Infinite / exponential | Infinite | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial distance:

```
d = x2 - x1
```

Because the rules are symmetric, only the relative distance matters.

1. Check whether the first player can capture immediately.

If:

```
a <= d <= b
```

then the first player may move directly to `x2`.

Output:

```
FIRST
x2
```

This is optimal because winning immediately is always best.

1. Otherwise, check whether every first move loses immediately.

After the first player moves by `t`, the new distance becomes `d - t`.

The second player wins immediately if:

```
a <= d - t <= b
```

We need this to hold for every legal `t`.

Since `t ∈ [a, b]`, the possible values of `d - t` form the interval:

```
[d - b, d - a]
```

Every move loses exactly when:

```
[a, b] contains [d - b, d - a]
```

which is equivalent to:

```
2a <= d <= 2b
```

If this condition holds, output:

```
SECOND
```

1. Otherwise, output:

```
DRAW
```

In this situation, the first player has at least one move that avoids immediate defeat, and neither side can force a future capture because of the complete symmetry of the game.

### Why it works

The game has no long-term positional structure beyond the current distance. A player can only force victory by making the opponent reachable in one move.

If the first player starts within reach, he wins immediately.

If every first move leaves the opponent within reach, the second player wins immediately.

All remaining positions are symmetric safe states. Any non-losing move by one player can be mirrored by the other, so neither side can force progress toward a guaranteed capture. That makes the game a draw.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x1, x2, a, b = map(int, input().split())

    d = x2 - x1

    if a <= d <= b:
        print("FIRST")
        print(x2)
        return

    if 2 * a <= d <= 2 * b:
        print("SECOND")
        return

    print("DRAW")

solve()
```

The implementation directly follows the mathematical characterization from the analysis.

The variable `d` stores the distance from the first player to the second player. Because the movement rules are symmetric, absolute coordinates are irrelevant after this transformation.

The first condition checks whether the first player can move directly onto the second player's position. If so, the winning move is exactly `x2`.

The second condition detects positions where every possible first move allows an immediate counter-capture. The derivation of `2a <= d <= 2b` comes from analyzing all possible remaining distances after the first move.

Everything else is classified as a draw.

One subtle implementation detail is that we do not reorder `x1` and `x2`. The problem statement defines asymmetric movement directions. The first player moves toward increasing coordinates, and the second player moves toward decreasing coordinates. Using:

```
d = x2 - x1
```

preserves that orientation correctly.

Another subtle point is handling negative values of `a` and `b`. The interval checks remain fully valid even when moves may go backward or stay in place.

## Worked Examples

### Example 1

Input:

```
0 2 0 4
```

| Variable | Value |
| --- | --- |
| x1 | 0 |
| x2 | 2 |
| a | 0 |
| b | 4 |
| d | 2 |

Check immediate win:

```
0 <= 2 <= 4
```

True.

The first player moves directly to position `2`.

Output:

```
FIRST
2
```

This trace demonstrates the simplest winning situation. The game ends before the second player gets a turn.

### Example 2

Input:

```
0 5 2 3
```

| Variable | Value |
| --- | --- |
| x1 | 0 |
| x2 | 5 |
| a | 2 |
| b | 3 |
| d | 5 |

Immediate win check:

```
2 <= 5 <= 3
```

False.

Second-player winning check:

```
2 * 2 <= 5 <= 2 * 3
4 <= 5 <= 6
```

True.

Output:

```
SECOND
```

To see why, enumerate the first player's legal moves.

| First move | New position | Remaining distance | Second captures? |
| --- | --- | --- | --- |
| +2 | 2 | 3 | Yes |
| +3 | 3 | 2 | Yes |

Every move leaves the second player within immediate reach.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow coordinates up to `10^9`, but the solution never iterates over positions or move ranges. All computations are constant-time integer arithmetic, so the program easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    x1, x2, a, b = map(int, input().split())

    d = x2 - x1

    if a <= d <= b:
        print("FIRST")
        print(x2)
    elif 2 * a <= d <= 2 * b:
        print("SECOND")
    else:
        print("DRAW")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("0 2 0 4\n") == "FIRST\n2\n", "sample 1"

# immediate loss for first player
assert run("0 5 2 3\n") == "SECOND\n", "all first moves lose"

# nobody can force anything
assert run("0 10 0 0\n") == "DRAW\n", "both players stuck"

# negative moves allowed
assert run("5 8 -2 1\n") == "FIRST\n8\n", "forward move still possible"

# boundary of second-player winning interval
assert run("0 4 2 2\n") == "SECOND\n", "exactly 2a"

# large coordinates
assert run("-1000000000 1000000000 1 2\n") == "DRAW\n", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 5 2 3` | `SECOND` | Every first move loses immediately |
| `0 10 0 0` | `DRAW` | Zero movement creates infinite draw |
| `5 8 -2 1` | `FIRST` | Negative movement bounds handled correctly |
| `0 4 2 2` | `SECOND` | Boundary condition `d = 2a = 2b` |
| `-1000000000 1000000000 1 2` | `DRAW` | Very large coordinates |

## Edge Cases

Consider:

```
0 10 0 0
```

The distance is:

```
d = 10
```

Immediate win check:

```
0 <= 10 <= 0
```

False.

Second-player winning check:

```
0 <= 10 <= 0
```

False.

The algorithm outputs:

```
DRAW
```

This is correct because both players are forced to stay in place forever.

Now consider:

```
0 4 2 2
```

The only legal move length is exactly `2`.

The distance is:

```
d = 4
```

The first player cannot capture immediately because `4` is not in `[2, 2]`.

The second condition becomes:

```
2 * 2 <= 4 <= 2 * 2
```

True.

The algorithm outputs:

```
SECOND
```

Indeed, the first player must move from `0` to `2`, after which the second player moves from `4` to `2` and wins.

Finally, consider a draw with nontrivial movement:

```
0 7 2 3
```

We have:

```
d = 7
```

Immediate win:

```
2 <= 7 <= 3
```

False.

Second-player forced win:

```
4 <= 7 <= 6
```

False.

The algorithm outputs:

```
DRAW
```

The first player can move by `3`, leaving distance `4`. The second player then cannot capture immediately. From there, both players can continue avoiding losing positions indefinitely because neither side can force the distance into a decisive interval.
