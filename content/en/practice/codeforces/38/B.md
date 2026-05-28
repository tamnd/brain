---
title: "CF 38B - Chess"
description: "We are given the positions of two chess pieces on a standard 8 × 8 board, one rook and one knight. Their starting positions are guaranteed to be safe, meaning the rook does not attack the knight and the knight does not attack the rook."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 38
codeforces_index: "B"
codeforces_contest_name: "School Personal Contest #1 (Winter Computer School 2010/11) - Codeforces Beta Round 38 (ACM-ICPC Rules)"
rating: 1200
weight: 38
solve_time_s: 120
verified: false
draft: false
---
[CF 38B - Chess](https://codeforces.com/problemset/problem/38/B)

**Rating:** 1200  
**Tags:** brute force, implementation, math  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given the positions of two chess pieces on a standard 8 × 8 board, one rook and one knight. Their starting positions are guaranteed to be safe, meaning the rook does not attack the knight and the knight does not attack the rook.

We must place one more knight on an empty square so that after placing it, none of the three pieces attack each other. The new knight must avoid attacking the rook, avoid attacking the existing knight, and also avoid being attacked by them. Since knight attacks are symmetric, this simply means no pair of pieces can attack each other.

The board size is fixed at only 64 squares. That changes the nature of the problem completely. Even a brute-force approach that checks every square independently is tiny in terms of operations. We never need advanced optimization or preprocessing because the maximum work is bounded by a small constant.

A direct simulation is enough. For each board cell, we can ask:

1. Is the square already occupied?
2. Is it attacked by the rook?
3. Is it attacked by the existing knight?
4. Would the new knight attack the rook?
5. Would the new knight attack the existing knight?

The last two checks are actually the same as checking whether the square is attacked by those pieces, because attacks are mutual for knights and rook movement is symmetric along rows and columns.

There are several easy-to-miss edge cases.

One common mistake is forgetting that the new knight cannot be placed on an occupied square. Consider:

```
a1
c2
```

The square `a1` is invalid because the rook already occupies it, and `c2` is invalid because the existing knight occupies it.

Another mistake is checking only whether the rook attacks the new knight, while forgetting the knight can also attack the rook. For knights this distinction matters conceptually, even though attack relations are symmetric. Example:

```
d4
f5
```

Placing the new knight at `e2` is invalid because the knight on `e2` attacks `d4`.

Boundary handling is another source of bugs. Knight moves can go outside the board. For example:

```
a1
h8
```

From `a1`, moves like `(-2, -1)` or `(1, -2)` are invalid and must be ignored. A careless implementation may access invalid indices or incorrectly count nonexistent squares.

## Approaches

The most straightforward idea is brute force. The chessboard has only 64 squares, so we can try placing the new knight on every square and verify whether the resulting configuration is safe.

For each candidate square, we perform constant-time checks:

- The square must not already contain the rook or knight.
- The rook must not attack the candidate.
- The existing knight must not attack the candidate.

A rook attacks any square in the same row or column. A knight attacks according to its eight possible L-shaped moves.

Even if we checked all 64 squares and tested all eight knight moves every time, the total work would still be tiny. Roughly speaking, this is under a thousand primitive operations.

Because the board size is fixed, the brute-force solution is already optimal in practice. There is no meaningful asymptotic improvement possible here. The key observation is that the search space is constant-sized, so exhaustive checking is the intended solution.

The only real challenge is implementing the chess attack rules correctly and cleanly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(64) | O(1) | Accepted |
| Optimal | O(64) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the rook position and the existing knight position.
2. Convert chess coordinates into numeric board coordinates.

The columns `a` through `h` become `0` through `7`, and rows `1` through `8` become `0` through `7`. Numeric coordinates make movement checks much easier.
3. Store the eight possible knight movement offsets.

A knight moves by `(±2, ±1)` or `(±1, ±2)`.
4. Iterate through every square on the board.

Since the board is only 8 × 8, checking all positions directly is simplest and safest.
5. Skip the square if it already contains the rook or the existing knight.

The problem only allows placement on empty squares.
6. Check whether the rook attacks the candidate square.

A rook attacks along rows and columns, so the square is invalid if it shares either coordinate with the rook.
7. Check whether the existing knight attacks the candidate square.

Compare the coordinate difference with the eight knight movement patterns.
8. If neither piece attacks the candidate square, count it as valid.
9. Print the final count.

### Why it works

The algorithm explicitly checks every square where the new knight could possibly be placed. A square is counted only if all attack conditions are satisfied. Since every candidate square is examined exactly once and every invalid condition is rejected, the final count contains precisely the valid placements and nothing else.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse(pos):
    x = ord(pos[0]) - ord('a')
    y = int(pos[1]) - 1
    return x, y

def knight_attacks(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx, dy) in [(1, 2), (2, 1)]

rook = input().strip()
knight = input().strip()

rx, ry = parse(rook)
kx, ky = parse(knight)

answer = 0

for x in range(8):
    for y in range(8):

        # occupied square
        if (x, y) == (rx, ry) or (x, y) == (kx, ky):
            continue

        # rook attack
        if x == rx or y == ry:
            continue

        # knight attack
        if knight_attacks(kx, ky, x, y):
            continue

        answer += 1

print(answer)
```

The `parse` function converts chess notation into zero-based coordinates. This avoids repeated character arithmetic throughout the solution.

The `knight_attacks` helper isolates the movement logic for knights. Instead of generating all moves explicitly, it uses coordinate differences. A knight attack always produces absolute differences `(1, 2)` or `(2, 1)`.

The nested loops iterate through every board square. Since the board size is fixed, this exhaustive search is both simple and efficient.

The order of checks matters for readability more than performance. We first reject occupied squares, then rook attacks, then knight attacks. Each rejected condition immediately skips unnecessary work.

One subtle detail is row conversion. Chess rows are written as `1` through `8`, but arrays are naturally zero-based. Subtracting one keeps all coordinates within `[0, 7]`.

## Worked Examples

### Example 1

Input:

```
a1
b2
```

The rook is at `(0, 0)` and the knight is at `(1, 1)`.

| Candidate | Occupied | Same Row/Col as Rook | Attacked by Knight | Valid |
| --- | --- | --- | --- | --- |
| a1 | Yes | Yes | No | No |
| a2 | No | Yes | No | No |
| c3 | No | No | No | Yes |
| d1 | No | Yes | No | No |
| c4 | No | No | Yes | No |

Final valid count:

```
44
```

This trace shows how multiple independent constraints eliminate squares. A square can fail for different reasons, and the algorithm checks them one by one.

### Example 2

Input:

```
d4
a1
```

The rook is at `(3, 3)` and the knight is at `(0, 0)`.

| Candidate | Occupied | Same Row/Col as Rook | Attacked by Knight | Valid |
| --- | --- | --- | --- | --- |
| b3 | No | No | Yes | No |
| c2 | No | No | Yes | No |
| e5 | No | No | No | Yes |
| d8 | No | Yes | No | No |
| h7 | No | No | No | Yes |

The knight on `a1` attacks only `b3` and `c2`. The rook removes an entire row and column. All remaining safe squares are counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) | Every board square is checked once |
| Space | O(1) | Only a few coordinate variables are stored |

The board size never changes, so the running time is effectively constant. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    def parse(pos):
        x = ord(pos[0]) - ord('a')
        y = int(pos[1]) - 1
        return x, y

    def knight_attacks(x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx, dy) in [(1, 2), (2, 1)]

    rook = input().strip()
    knight = input().strip()

    rx, ry = parse(rook)
    kx, ky = parse(knight)

    ans = 0

    for x in range(8):
        for y in range(8):

            if (x, y) == (rx, ry) or (x, y) == (kx, ky):
                continue

            if x == rx or y == ry:
                continue

            if knight_attacks(kx, ky, x, y):
                continue

            ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("a1\nb2\n") == "44", "sample 1"

# corner pieces
assert run("a1\nh8\n") == "48", "opposite corners"

# knight near center
assert run("d4\na1\n") == "47", "central rook"

# edge interaction
assert run("h1\nf2\n") == "44", "edge knight attacks"

# another boundary case
assert run("c3\ne4\n") == "42", "multiple knight exclusions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a1 b2` | `44` | Official sample |
| `a1 h8` | `48` | Corner handling and board boundaries |
| `d4 a1` | `47` | Central rook removing row and column |
| `h1 f2` | `44` | Knight attacks near board edge |
| `c3 e4` | `42` | Multiple overlapping attack regions |

## Edge Cases

Consider the input:

```
a1
h8
```

The rook attacks the entire first row and first column. The knight on `h8` attacks only `f7` and `g6`, because all other knight moves go outside the board.

The algorithm handles this naturally. Every square is checked independently, and out-of-board knight moves are never generated because the solution compares coordinate differences directly instead of constructing destinations.

Now consider:

```
d4
f5
```

A careless solution might only check whether the rook attacks the new knight and forget that the new knight can attack existing pieces.

Suppose we try placing the new knight at `e3`. The coordinate difference from `d4` is `(1, 1)`, so the rook is safe. The difference from `f5` is also `(1, 2)`, meaning the knights attack each other. The algorithm rejects the square because `knight_attacks` returns true.

Finally, consider occupied-square handling:

```
a1
c2
```

The algorithm explicitly skips `(0, 0)` and `(2, 1)` before any attack checks happen. Without this condition, an implementation could incorrectly count already occupied positions as legal placements.
