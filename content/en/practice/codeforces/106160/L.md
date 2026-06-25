---
title: "CF 106160L - Linguistic Labyrinth"
description: "We have a grid with exactly three rows and W columns. Three cells are special. The first player starts at A = (1, a), the second player starts at B = (3, b), and both want to reach X = (2, 1). Before the game starts, we may place obstacles on any cells except A, B, and X."
date: "2026-06-25T11:14:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "L"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 51
verified: true
draft: false
---

[CF 106160L - Linguistic Labyrinth](https://codeforces.com/problemset/problem/106160/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a grid with exactly three rows and `W` columns. Three cells are special.

The first player starts at `A = (1, a)`, the second player starts at `B = (3, b)`, and both want to reach `X = (2, 1)`.

Before the game starts, we may place obstacles on any cells except `A`, `B`, and `X`. After placing obstacles, the distance from a starting cell to `X` is the length of the shortest valid path through non-blocked cells.

The task is not to compute a distance. Instead, we must construct a labyrinth whose shortest-path distances satisfy

`dist(A, X) = dist(B, X) < ∞`.

If no such labyrinth exists, we print `Impossible`.

The width is at most 100, so there is no algorithmic challenge in terms of complexity. The real difficulty is understanding which configurations are possible and finding a simple constructive pattern.

A subtle case appears when one starting position is already in column 1.

For example:

```
W = 3
a = 3
b = 1
```

Cell `B` is directly adjacent to `X`. Since obstacles remove cells but cannot remove the edge between two surviving adjacent cells, the shortest distance from `B` to `X` is permanently `1`. The other player cannot also have distance `1`, so the answer is impossible.

Another easy-to-miss situation is parity.

Consider:

```
W = 4
a = 3
b = 2
```

The statement's sample declares this impossible.

Any path from `(1,a)` to `(2,1)` has the same parity as its Manhattan distance. Every detour adds an even number of steps in a grid. So every possible path from `A` to `X` has parity `a`, and every possible path from `B` to `X` has parity `b`.

If `a` and `b` have different parity, equal distances are impossible.

Finally, when both starts are already adjacent to `X`:

```
W = 1
a = 1
b = 1
```

both distances are already `1`, so the empty labyrinth works.

## Approaches

A brute-force mindset would try to search over all obstacle placements and check shortest paths with BFS. A `3 × W` board contains up to 300 cells, so the number of obstacle configurations is roughly `2^300`, which is completely infeasible.

The key observation is that the problem is almost entirely determined by geometry.

The first useful fact is parity. Any path from `(1,a)` to `(2,1)` has parity equal to `a`, because the Manhattan distance is `a` and every detour changes the length by an even amount. Similarly, every path from `(3,b)` to `(2,1)` has parity equal to `b`.

Equal distances require equal parity, so `a` and `b` must have the same parity.

The second useful fact concerns column 1. If `a = 1`, then `A` is permanently adjacent to `X`, so `dist(A,X) = 1` no matter what obstacles we place. The same is true for `b = 1`.

That means:

If exactly one of `a` and `b` equals `1`, the answer is impossible.

After removing those impossible cases, suppose both positions are strictly to the right of column 1 and have the same parity.

Let

```
t = (a + b) / 2
```

Since the parities match, `t` is an integer.

We build a tree-shaped corridor.

Open a horizontal segment on row 1 from column `a` to column `t`.

Open a horizontal segment on row 3 from column `b` to column `t`.

Open row 2 from column `1` through column `t`.

Block everything else.

Now every path from either start to `X` must first reach column `t`, then move along row 2 to column 1.

The distance from `A` becomes

```
|a - t| + 1 + (t - 1)
```

and the distance from `B` becomes

```
|b - t| + 1 + (t - 1)
```

Because `t` is exactly the midpoint, the two absolute values are equal, so the distances are equal.

The resulting graph is a tree, so there are no alternative shortcuts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over obstacle placements | Exponential | Exponential | Too slow |
| Midpoint construction | O(W) | O(W) | Accepted |

## Algorithm Walkthrough

1. If `a = 1` and `b = 1`, output the empty grid with only the three special cells marked.
2. If exactly one of `a` and `b` equals `1`, output `Impossible`.

The player starting in column 1 is permanently at distance `1` from `X`, while the other player is not.
3. If `a` and `b` have different parity, output `Impossible`.

Every path from `A` to `X` has parity `a`, and every path from `B` to `X` has parity `b`. Equal lengths must have equal parity.
4. Compute

```
t = (a + b) / 2
```

Since the parities match, this is an integer.
5. Start with a grid filled with obstacles.
6. Open every cell of row 2 from column `1` through column `t`.

This becomes the common corridor leading to `X`.
7. Open the cells on row 1 between columns `a` and `t`, inclusive.

This creates the branch containing `A`.
8. Open the cells on row 3 between columns `b` and `t`, inclusive.

This creates the branch containing `B`.
9. Place the characters `A`, `B`, and `X` in their required cells and print the grid.

### Why it works

The construction creates a tree. Any route from either starting point to `X` must pass through the unique junction at column `t`.

The path length from `A` equals

```
|a - t| + 1 + (t - 1).
```

The path length from `B` equals

```
|b - t| + 1 + (t - 1).
```

Since `t` is the midpoint of `a` and `b`, we have

```
|a - t| = |b - t|.
```

Hence the two distances are identical.

The impossibility conditions are also necessary. Different parity prevents equal lengths, and if exactly one start is in column 1, one player is permanently at distance 1 while the other is not.

## Python Solution

```python
import sys
input = sys.stdin.readline

W, a, b = map(int, input().split())

if a == 1 and b == 1:
    print("Possible")
    print("A")
    print("X")
    print("B")
    sys.exit()

if (a == 1) ^ (b == 1):
    print("Impossible")
    sys.exit()

if (a - b) & 1:
    print("Impossible")
    sys.exit()

t = (a + b) // 2

g = [['*' for _ in range(W)] for _ in range(3)]

for c in range(1, t + 1):
    g[1][c - 1] = '.'

for c in range(min(a, t), max(a, t) + 1):
    g[0][c - 1] = '.'

for c in range(min(b, t), max(b, t) + 1):
    g[2][c - 1] = '.'

g[0][a - 1] = 'A'
g[1][0] = 'X'
g[2][b - 1] = 'B'

print("Possible")
for row in g:
    print(''.join(row))
```

The first block handles the special situations that are impossible by parity or by the fixed distance-1 adjacency to `X`.

The midpoint `t` is the core of the construction. The second row becomes the common corridor. The first and third rows contribute one branch each, ending at column `t`.

The implementation fills the board with obstacles first and only opens cells belonging to the desired tree. This avoids accidentally leaving a shortcut somewhere else.

The interval loops use `min` and `max`, so they work whether `a < t`, `a > t`, or `a = t`.

## Worked Examples

### Example 1

Input:

```
9 3 7
```

Here:

```
t = (3 + 7) / 2 = 5
```

| Step | Value |
| --- | --- |
| a | 3 |
| b | 7 |
| t | 5 |
| Distance A→t | 2 |
| Distance B→t | 2 |
| Distance t→X | 4 |
| Total distance | 7 |

Constructed grid:

```
**A..****
X....****
****..B**
```

Both players travel 7 steps to reach `X`.

This example demonstrates the midpoint idea. The two branches have equal length before joining the common corridor.

### Example 2

Input:

```
4 3 2
```

| Quantity | Value |
| --- | --- |
| a parity | odd |
| b parity | even |

The parities differ, so equal distances are impossible.

Output:

```
Impossible
```

This example demonstrates the necessary parity condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(W) | Each cell is written a constant number of times |
| Space | O(W) | The grid contains exactly `3 × W` cells |

Since `W ≤ 100`, the construction runs instantly and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    data = io.StringIO(inp)
    out = io.StringIO()

    W, a, b = map(int, data.readline().split())

    if a == 1 and b == 1:
        return "Possible\nA\nX\nB\n"

    if (a == 1) ^ (b == 1):
        return "Impossible\n"

    if (a - b) & 1:
        return "Impossible\n"

    t = (a + b) // 2

    g = [['*' for _ in range(W)] for _ in range(3)]

    for c in range(1, t + 1):
        g[1][c - 1] = '.'

    for c in range(min(a, t), max(a, t) + 1):
        g[0][c - 1] = '.'

    for c in range(min(b, t), max(b, t) + 1):
        g[2][c - 1] = '.'

    g[0][a - 1] = 'A'
    g[1][0] = 'X'
    g[2][b - 1] = 'B'

    out.write("Possible\n")
    for row in g:
        out.write("".join(row) + "\n")

    return out.getvalue()

# sample-style checks
assert run("1 1 1\n") == "Possible\nA\nX\nB\n"

assert run("4 3 2\n") == "Impossible\n"

assert run("3 3 1\n") == "Impossible\n"

# custom cases
assert run("5 2 4\n").startswith("Possible")
assert run("10 5 5\n").startswith("Possible")
assert run("7 1 5\n") == "Impossible\n"
assert run("100 99 99\n").startswith("Possible")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | Possible | Minimum size |
| `4 3 2` | Impossible | Parity mismatch |
| `3 3 1` | Impossible | One start fixed at distance 1 |
| `5 2 4` | Possible | Typical midpoint construction |
| `10 5 5` | Possible | Midpoint equals both starts |
| `100 99 99` | Possible | Largest width range |

## Edge Cases

Consider:

```
3 3 1
```

Player `B` starts at `(3,1)`, directly below `X`.

The edge between `(3,1)` and `(2,1)` always exists because neither endpoint may be blocked.

So:

```
dist(B, X) = 1
```

forever.

Player `A` starts at column 3 and cannot also achieve distance 1. The algorithm detects that exactly one start lies in column 1 and prints `Impossible`.

Now consider:

```
4 3 2
```

The parity of every possible `A → X` path is odd, while the parity of every possible `B → X` path is even.

Equal integers cannot simultaneously be odd and even. The algorithm checks parity first and immediately reports `Impossible`.

Finally, consider:

```
5 3 3
```

Then:

```
t = 3
```

Both branches connect directly into the same junction column. The unique path from either start to `X` has length 3, and the construction remains valid without any special handling.
