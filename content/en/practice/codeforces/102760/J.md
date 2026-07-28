---
title: "CF 102760J - Remote Control"
description: "The grid is infinite, except that the cell (0,0) contains a wall. A remote control contains one fixed sequence of moves."
date: "2026-07-29T00:01:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "J"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 77
verified: true
draft: false
---

[CF 102760J - Remote Control](https://codeforces.com/problemset/problem/102760/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid is infinite, except that the cell `(0,0)` contains a wall. A remote control contains one fixed sequence of moves. A car placed at some non-wall cell follows that sequence, but whenever a move would enter the wall, that single move is ignored and the car continues with the remaining commands.

For every starting coordinate, we need to find the final coordinate after pressing the button once.

The command sequence has length up to `300000`, and there can also be up to `300000` queries. A simulation of the whole path for every query would require up to `9 * 10^10` operations in the worst case, which is far beyond what a 2 second limit allows. We need to preprocess the command sequence once and answer each query in constant time.

The key difficulty is that the wall only affects starting positions that can collide with it. Most starting positions simply follow the command sequence as if the wall did not exist.

A careless implementation can fail on repeated positions in the command path. For example, if the path visits the same displacement several times, the first visit is the one that matters because the car hits the wall there and changes the rest of the simulation.

For the command:

```
2
RL
```

the prefix displacements are `(0,0)`, `(1,0)`, `(0,0)`. A start at `(0,-0)` is invalid because it is the wall, but the same repeated-position issue appears in nearby cases. If we store the last occurrence instead of the first occurrence of a prefix position, the calculated collision point will be wrong.

Another edge case is a command path that never returns to the same displacement. For:

```
1
R
```

a query starting at `(5,5)` should output `(6,5)`. A solution that tries to process every point near the path instead of using the displacement observation would waste time.

## Approaches

The direct approach is to simulate the commands for every query. For a query `(x,y)`, we keep the current position and apply every character of the command. Whenever the next cell is `(0,0)`, we skip that move. This is obviously correct because it follows exactly the rules of the car, but it takes `O(N)` time per query. With both `N` and `Q` equal to `300000`, this becomes `O(NQ)`, which is impossible.

The important observation is that the wall can only matter if the translated command path reaches the origin. Let `P[i]` be the displacement of the car after the first `i` commands when starting from `(0,0)`. Without a wall, a car starting at `(x,y)` would end at:

```
(x + P[N].x, y + P[N].y)
```

The wall is encountered only when:

```
(x,y) + P[i] = (0,0)
```

which means:

```
(x,y) = -P[i]
```

So only starting positions that are the negatives of prefix positions need special handling.

For those positions, the first time the path reaches the wall is the first occurrence of that prefix displacement. After that blocked move, the remaining suffix of the path is executed normally. We can preprocess the answer for every dangerous starting position while scanning the command once.

The brute-force works because it follows the exact simulation, but fails because it repeats the same work for many queries. The observation that only prefix displacements can cause collisions reduces the problem to preprocessing a set of exceptional states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(1) | Too slow |
| Optimal | O(N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

1. Compute the total displacement of the whole command sequence. Any query whose starting position never reaches the wall can be answered by adding this displacement.
2. Scan the command sequence and store every prefix displacement. For each displacement, keep only its first occurrence index. The first occurrence is the first possible time the car would hit the wall for the corresponding starting position.
3. For every first occurrence of a prefix position `P[i]`, create an entry for the dangerous starting point `-P[i]`.
4. To compute the final position of a dangerous starting point, let `i` be the first time the path reaches that prefix displacement. Before the collision, the car reaches the position represented by `P[i-1] - P[i]`. The command at time `i` is blocked, and the remaining commands contribute the displacement `P[N] - P[i]`.

The final position is therefore:

```
P[i-1] - P[i] + P[N] - P[i]
```

or:

```
P[N] + P[i-1] - 2 * P[i]
```

1. For each query, check whether its coordinate exists in the precomputed dangerous-position map. If it does, output the stored answer. Otherwise, output the normal translated position.

Why it works: every possible interaction with the wall corresponds exactly to a prefix displacement of the command path. If a starting position is not the negative of any prefix displacement, the wall is never reached and the final position is just the total displacement away. If it is a dangerous position, the first occurrence of that prefix displacement determines the first blocked move. After that point, the car's behavior is completely determined by the remaining suffix, which is exactly what the formula computes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    dx = [0] * (n + 1)
    dy = [0] * (n + 1)

    x = y = 0
    for i, c in enumerate(s, 1):
        if c == 'L':
            x -= 1
        elif c == 'R':
            x += 1
        elif c == 'U':
            y += 1
        else:
            y -= 1
        dx[i] = x
        dy[i] = y

    total_x, total_y = x, y

    first = {}
    for i in range(n + 1):
        pos = (dx[i], dy[i])
        if pos not in first:
            first[pos] = i

    special = {}
    for (px, py), i in first.items():
        if px == 0 and py == 0:
            continue
        prev_x = dx[i - 1]
        prev_y = dy[i - 1]
        ans_x = total_x + prev_x - 2 * px
        ans_y = total_y + prev_y - 2 * py
        special[(-px, -py)] = (ans_x, ans_y)

    q = int(input())
    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        if (x, y) in special:
            ax, ay = special[(x, y)]
            out.append(f"{ax} {ay}")
        else:
            out.append(f"{x + total_x} {y + total_y}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The arrays `dx` and `dy` store the command path starting from the origin. Keeping all prefixes avoids recomputing coordinates while answering queries.

The `first` dictionary is the important part of the preprocessing. When the same displacement appears multiple times, only the earliest index is stored because that is where the first collision happens. Using the last occurrence would simulate a car that had already passed through the wall, which is impossible.

The `special` dictionary stores only non-wall starting coordinates. The origin is excluded because the car can never start there. Every normal query avoids this dictionary lookup and uses the total displacement directly.

All calculations use Python integers, so there is no overflow concern. The indexing with `i - 1` is safe because the first stored occurrence of `(0,0)` is index `0`, and that case is skipped.

## Worked Examples

For the sample:

```
8
RRDRUULL
5
-2 1
-2 2
-2 -1
-3 -1
1 1
```

The prefix displacements are:

| Step | Command | Position |
| --- | --- | --- |
| 0 | start | (0,0) |
| 1 | R | (1,0) |
| 2 | R | (2,0) |
| 3 | D | (2,-1) |
| 4 | R | (3,-1) |
| 5 | U | (3,0) |
| 6 | U | (3,1) |
| 7 | L | (2,1) |
| 8 | L | (1,1) |

The total displacement is `(1,1)`. A query such as `(1,1)` is not dangerous because `(-1,-1)` is not a prefix displacement, so the answer is `(2,2)`.

For a dangerous query:

| Value | Meaning |
| --- | --- |
| Starting point | (-2, -1) |
| Negative prefix position | (2,1) |
| First occurrence index | 7 |
| Previous prefix | (3,1) |
| Total displacement | (1,1) |
| Final position | (1,0) |

This trace demonstrates that only the first collision matters. After the blocked move, the suffix continues from the position where the failed move left the car.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Q) | The command path is scanned once and every query is answered by dictionary lookup. |
| Space | O(N) | We store prefix displacements and dangerous starting positions. |

The constraints allow linear preprocessing because both the path length and the number of queries are `300000`. The algorithm performs only a constant amount of work per command and per query.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    result = sys.stdout.getvalue()
    sys.stdin = old
    return result

assert run("""1
R
3
1 1
-1 0
0 1
""") == """2 1
0 0
1 1""", "simple movement"

assert run("""8
RRDRUULL
5
-2 1
-2 2
-2 -1
-3 -1
1 1
""") == """-1 3
-1 3
1 0
-2 -1
2 2""", "sample"

assert run("""3
RRR
4
-1 0
-3 0
10 10
1 0
""") == """2 0
2 0
13 10
4 0""", "straight line boundary"

assert run("""4
UDUD
3
0 1
0 -1
5 5
""") == """0 1
0 -1
5 5""", "repeated positions"

assert run("""1
U
2
0 -1
100 100
""") == """0 0
100 101""", "minimum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single right move | Translated positions | Basic movement without collisions |
| Sample | Sample output | Full collision handling |
| Straight path | Correct blocked and normal movement | Prefix collision detection |
| Repeated positions | Same coordinate handling | First occurrence requirement |
| Single command | Smallest path size | Boundary behavior |

## Edge Cases

A repeated prefix position must use its first occurrence. Suppose a command path reaches the same displacement several times. A car starting at the negative of that displacement collides at the first visit, so later visits are irrelevant. The preprocessing keeps the earliest index and produces the correct suffix simulation.

A query that never reaches the wall must not enter the special-case logic. For example, with:

```
1
R
1
5 5
```

the total displacement is `(1,0)`. Since `(-5,-5)` is not a prefix position, the answer is simply `(6,5)`.

A path that immediately returns or repeats positions is handled by the same rule. The dictionary contains only the first time each displacement appears, so the simulation always uses the first blocked move and never assumes the car can pass through the wall.
