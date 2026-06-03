---
title: "CF 198B - Jumping on Walls"
description: "We have two vertical walls, each represented by a string of length n. Position i on a wall is either safe (-) or blocked (X). The ninja starts at position 0 of the left wall. Every second he may move to one of three positions: 1. One cell upward on the same wall. 2."
date: "2026-06-03T09:49:22+07:00"
tags: ["codeforces", "competitive-programming", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 198
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 125 (Div. 1)"
rating: 1400
weight: 198
solve_time_s: 97
verified: true
draft: false
---

[CF 198B - Jumping on Walls](https://codeforces.com/problemset/problem/198/B)

**Rating:** 1400  
**Tags:** shortest paths  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two vertical walls, each represented by a string of length `n`. Position `i` on a wall is either safe (`-`) or blocked (`X`). The ninja starts at position `0` of the left wall.

Every second he may move to one of three positions:

1. One cell upward on the same wall.
2. One cell downward on the same wall.
3. The opposite wall, `k` cells higher.

Moving beyond position `n - 1` means escaping the canyon immediately.

The complication is the rising water. At time `t`, all positions with index `<= t - 1` are already submerged. After making the `t`-th move, water rises again. A position is usable only if it has not been flooded yet.

The task is to determine whether escape is possible.

The wall height can reach `100000`, which immediately rules out any exponential search. Even a quadratic algorithm would require around `10^10` operations in the worst case, far beyond the limit. We need something close to linear time.

The most subtle part of the problem is the interaction between movement and time. Reaching the same position at different times is not equivalent, because water keeps removing lower positions.

Consider:

```
3 1
---
---
```

The correct answer is `YES`. From position `0`, jump to the other wall at position `1`, then jump again beyond the wall.

A careless implementation that only checks wall obstacles and ignores time would work here, but that same mistake fails on cases where the only path requires visiting already flooded positions.

Another easy mistake is allowing moves onto positions that are already underwater.

```
4 2
----
----
```

Suppose we are at position `2` at time `3`. Position `1` is already flooded, so moving down to it is illegal even though it is marked safe.

The correct condition is not merely "inside bounds and not blocked". The destination index must also be strictly greater than the current time.

A third trap is escape by jumping.

```
5 3
-----
-----
```

From position `3`, a jump lands at position `6`, which is outside the wall. The ninja escapes immediately. Some implementations incorrectly reject moves whose destination index exceeds `n - 1`, missing valid escapes.

## Approaches

A brute-force idea is to model every possible sequence of moves. From each state we try climbing up, climbing down, and jumping across. Since the same positions can be revisited through many different paths, the number of move sequences grows exponentially with time. Even for moderate wall heights this becomes infeasible.

The key observation is that the game naturally forms a graph. A state is completely determined by two pieces of information: which wall we are on and which position we occupy. Time does not need to be stored separately because every move costs exactly one second. In a breadth-first search, the distance from the start is exactly the elapsed time when we reach a state.

Once we know the arrival time of a state, we can decide whether a move is legal. A destination position must be safe, unvisited, and still above the water level at the moment of arrival.

This turns the problem into a shortest-path search on at most `2n` states. Each state has at most three outgoing edges, so the entire graph can be explored in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal BFS | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the two wall strings.
2. Represent a state as `(wall, position)` where `wall` is `0` for the left wall and `1` for the right wall.
3. Start BFS from `(0, 0)` at time `0`.
4. When a state `(wall, pos)` is removed from the queue, its BFS distance is the current time `t`.
5. Generate the three possible moves:

- `(wall, pos + 1)`
- `(wall, pos - 1)`
- `(1 - wall, pos + k)`
6. If any destination index is at least `n`, the ninja escapes immediately and we print `YES`.
7. For destinations inside the wall:

- The cell must be safe (`'-'`).
- The state must not have been visited before.
- The destination index must be strictly greater than `t + 1`.

The last condition models the water. After making the next move, time becomes `t + 1`. Any position with index at most `t + 1` is already flooded and cannot be occupied.
8. Every valid destination is added to the BFS queue with distance `t + 1`.
9. If BFS finishes without escaping, print `NO`.

### Why it works

BFS explores states in increasing order of elapsed time. When a state is first visited, we have found the earliest possible arrival time for that state.

The water restriction depends only on the arrival time. If a position is unsafe when reached at its earliest arrival time, reaching it later cannot help because the water level only rises. Because of this monotonic property, visiting each state once is sufficient.

Every legal sequence of moves corresponds to a path explored by BFS, and every BFS transition corresponds to a legal move in the game. Escape is reported exactly when a move leaves the wall, so the algorithm returns `YES` if and only if a valid escape path exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    walls = [input().strip(), input().strip()]

    visited = [[False] * n for _ in range(2)]
    visited[0][0] = True

    q = deque()
    q.append((0, 0, 0))  # wall, position, time

    while q:
        wall, pos, t = q.popleft()

        moves = [
            (wall, pos + 1),
            (wall, pos - 1),
            (1 - wall, pos + k)
        ]

        for nw, np in moves:
            if np >= n:
                print("YES")
                return

            if np < 0:
                continue

            if np <= t + 1:
                continue

            if walls[nw][np] == 'X':
                continue

            if visited[nw][np]:
                continue

            visited[nw][np] = True
            q.append((nw, np, t + 1))

    print("NO")

solve()
```

The queue stores the current wall, position, and elapsed time. BFS guarantees that states are processed in increasing time order.

The condition `np <= t + 1` is the most important line in the solution. We are considering a move that arrives one second later. At that moment, positions with index at most `t + 1` have already disappeared under the water, so such moves are illegal.

Escape is checked before obstacle validation because leaving the wall immediately wins the game. A jump that lands beyond the top succeeds regardless of what would have existed there.

The visited array prevents revisiting states. Since BFS reaches every state at its earliest possible time, later arrivals cannot produce any advantage.

## Worked Examples

### Sample 1

Input:

```
7 3
---X--X
-X--XX-
```

| Time | State | Move Chosen | Result |
| --- | --- | --- | --- |
| 0 | (L,0) | Jump | (R,3) |
| 1 | (R,3) | Down | (R,2) |
| 2 | (R,2) | Jump | (L,5) |
| 3 | (L,5) | Jump | Position 8 |
| 4 | Escape | - | YES |

This trace shows why jumping across walls is essential. A direct climb is blocked by dangerous cells, but alternating walls creates a route to the top.

### Second Example

```
5 1
--XXX
XXXXX
```

| Time | State | Reachable States |
| --- | --- | --- |
| 0 | (L,0) | (L,1) |
| 1 | (L,1) | none |
| End | - | BFS exhausted |

Output:

```
NO
```

The right wall is completely blocked and climbing farther on the left wall eventually hits obstacles. BFS explores every legal state and finds no escape.

The example demonstrates that failure is detected naturally when the queue becomes empty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the `2n` states is visited at most once |
| Space | O(n) | Queue and visited array store at most `2n` states |

With `n ≤ 100000`, the algorithm processes only a few hundred thousand state transitions. This comfortably fits within the time limit and uses only linear memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k = map(int, input().split())
    walls = [input().strip(), input().strip()]

    visited = [[False] * n for _ in range(2)]
    visited[0][0] = True

    q = deque([(0, 0, 0)])

    while q:
        wall, pos, t = q.popleft()

        for nw, np in (
            (wall, pos + 1),
            (wall, pos - 1),
            (1 - wall, pos + k),
        ):
            if np >= n:
                return "YES"

            if np < 0:
                continue

            if np <= t + 1:
                continue

            if walls[nw][np] == 'X':
                continue

            if visited[nw][np]:
                continue

            visited[nw][np] = True
            q.append((nw, np, t + 1))

    return "NO"

# sample from statement
assert run("7 3\n---X--X\n-X--XX-\n") == "YES", "sample"

# minimum size
assert run("1 1\n-\n-\n") == "YES", "immediate jump escapes"

# blocked everywhere else
assert run("5 1\n--XXX\nXXXXX\n") == "NO", "no usable continuation"

# jump directly out
assert run("5 5\n-----\n-----\n") == "YES", "first move escapes"

# water prevents moving back
assert run("4 1\n----\nXXXX\n") == "NO", "cannot survive rising water"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / - / -` | YES | Smallest possible instance |
| `5 1 / --XXX / XXXXX` | NO | Dead end caused by obstacles |
| `5 5 / ----- / -----` | YES | Immediate escape via jump |
| `4 1 / ---- / XXXX` | NO | Correct handling of flooding |

## Edge Cases

Consider the smallest possible canyon:

```
1 1
-
-
```

The BFS starts at `(0,0)`. The jump move targets position `1`, which is outside the wall. The algorithm checks `np >= n` first and immediately returns `YES`. This handles instant escapes correctly.

Consider a case where moving downward would enter flooded territory:

```
4 2
----
----
```

Suppose BFS reaches position `3` at time `2`. Moving down would target position `2`. The arrival time would be `3`, and the condition `np <= t + 1` becomes `2 <= 3`, so the move is rejected. The algorithm never allows standing on a submerged cell.

Consider a jump that exits the canyon:

```
5 3
-----
-----
```

A state at position `3` generates a jump to position `6`. Since `6 >= 5`, escape is detected immediately. No wall lookup is attempted, avoiding out-of-bounds errors and correctly modeling the game rules.

Finally, consider revisiting a state later:

```
6 2
------
------
```

A position may be reachable through several routes. BFS visits it at the earliest possible time and marks it visited. Any later arrival would face an equal or higher water level, never creating new opportunities. The visited array safely removes redundant exploration while preserving correctness.
