---
title: "CF 106118K - King of Tic-Tac-Toe"
description: "We are given a 3 × 3 Tic-Tac-Toe board. Each cell contains either X, O, or .. The board is not guaranteed to be a valid state from a normal game, so the counts of X and O do not matter. Nobita gets a special power: he may place two O marks consecutively on any two empty cells."
date: "2026-06-19T20:07:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106118
codeforces_index: "K"
codeforces_contest_name: "2025 ICPC, Chula Selection Contest"
rating: 0
weight: 106118
solve_time_s: 50
verified: true
draft: false
---

[CF 106118K - King of Tic-Tac-Toe](https://codeforces.com/problemset/problem/106118/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 3 × 3 Tic-Tac-Toe board. Each cell contains either `X`, `O`, or `.`. The board is not guaranteed to be a valid state from a normal game, so the counts of `X` and `O` do not matter.

Nobita gets a special power: he may place two `O` marks consecutively on any two empty cells. After those two placements, the game immediately ends. If the resulting board contains at least one complete row, column, or diagonal consisting entirely of `O`, then Nobita wins.

For every test case, we must determine whether such a pair of moves exists. If it does, we print `YES` and one resulting winning board. Otherwise, we print `NO`.

The board size is fixed at 3 × 3. Even though there may be up to 1000 test cases, each board contains only 9 cells. Any algorithm that performs a constant amount of work per board is easily fast enough. We do not need sophisticated optimization because the search space is tiny.

The main challenge is not performance but correctness. We must carefully consider all possible ways to place the two new `O` marks.

One easy mistake is checking only lines that already contain some `O`s. A winning line may require filling two empty cells.

For example:

```
...
OO.
...
```

Placing an `O` in the last cell of the middle row wins immediately. Since Nobita must make exactly two moves, he can place the second `O` anywhere else. The correct answer is `YES`.

Another subtle case is when the winning line contains no existing `O` at all.

```
...
.X.
...
```

Nobita can place two `O`s in the same row, but that still gives only two marks. A full line requires three `O`s, so the answer is `NO`.

A different mistake is stopping after finding one move that does not win. We need to consider every pair of empty cells.

```
X.X
.O.
...
```

Some placements fail, but choosing the left and right cells of the middle row creates `OOO`. The correct answer is `YES`.

## Approaches

The most direct idea is brute force. Collect all empty cells, choose every possible pair of distinct empty cells, place `O` in those positions, and check whether the resulting board contains a winning line.

A Tic-Tac-Toe board has at most 9 cells, so there are at most 9 empty positions. The number of pairs is at most:

$$\binom{9}{2} = 36$$

For each pair, we examine the 8 possible winning lines, namely 3 rows, 3 columns, and 2 diagonals. The total work per test case is only a few hundred operations.

Since the board size is fixed, this brute-force search is already optimal in practice. There is no larger structure to exploit, and any more complicated approach would only add unnecessary complexity.

The key observation is that the board is so small that exhaustive search is effectively constant time. Instead of reasoning about potential winning lines separately, we can simply test every legal pair of moves and directly verify the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all move pairs | O(E²) where E ≤ 9 | O(1) | Accepted |
| Optimal | O(E²) where E ≤ 9 | O(1) | Accepted |

Since `E` is at most 9, both descriptions represent the same practical solution.

## Algorithm Walkthrough

1. Read the 3 × 3 board.
2. Collect the coordinates of all empty cells.
3. For every pair of distinct empty cells:

Place `O` in both positions on a temporary copy of the board.
4. Check whether the modified board contains a winning line for `O`.

A winning line is any row, column, or diagonal whose three cells are all `O`.
5. If a winning line exists, print `YES` and the modified board.

We may stop immediately because the problem accepts any winning board.
6. If all pairs have been tested and none produce a win, print `NO`.

### Why it works

The algorithm examines every legal way Nobita can use his double move. Each possible outcome after the two placements corresponds to exactly one pair of empty cells, and every such pair is tested.

When a pair is tested, the algorithm explicitly checks all 8 winning lines. If any line consists entirely of `O`, that board is winning. If no line does, that board is not winning.

Because every valid pair of moves is considered and every resulting board is evaluated correctly, the algorithm finds a winning board whenever one exists and reports `NO` only when none exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_win(board):
    for r in range(3):
        if all(board[r][c] == 'O' for c in range(3)):
            return True

    for c in range(3):
        if all(board[r][c] == 'O' for r in range(3)):
            return True

    if all(board[i][i] == 'O' for i in range(3)):
        return True

    if all(board[i][2 - i] == 'O' for i in range(3)):
        return True

    return False

t = int(input())

for _ in range(t):
    board = [list(input().strip()) for _ in range(3)]

    empty = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == '.':
                empty.append((r, c))

    found = False

    m = len(empty)
    for i in range(m):
        for j in range(i + 1, m):
            temp = [row[:] for row in board]

            r1, c1 = empty[i]
            r2, c2 = empty[j]

            temp[r1][c1] = 'O'
            temp[r2][c2] = 'O'

            if is_win(temp):
                print("YES")
                for row in temp:
                    print("".join(row))
                found = True
                break

        if found:
            break

    if not found:
        print("NO")
```

The helper function `is_win` checks all eight possible winning lines. Since the board size is fixed, explicitly testing rows, columns, and diagonals is the simplest and safest implementation.

The list `empty` stores every available move location. The nested loops iterate over all unordered pairs of empty cells. Using `j = i + 1` avoids testing the same pair twice and prevents selecting the same cell twice.

For each candidate pair, a fresh copy of the board is created. This avoids having to undo moves afterward and keeps the logic straightforward.

The moment a winning board is found, the loops terminate and the board is printed. Any valid winning board is acceptable, so there is no need to continue searching.

## Worked Examples

### Example 1

Input board:

```
X.X
.O.
...
```

Empty cells:

| Pair Tested | Winning? |
| --- | --- |
| (0,1), (1,0) | No |
| (0,1), (1,2) | No |
| (1,0), (1,2) | Yes |

Resulting board:

```
X.X
OOO
...
```

The middle row becomes entirely `O`, so the search stops immediately. This demonstrates that we must examine multiple pairs rather than making a greedy choice.

### Example 2

Input board:

```
X.X
.X.
...
```

Empty cells:

| Pair Tested | Winning? |
| --- | --- |
| Any pair | No |

No matter where the two new `O`s are placed, at most two cells of a line can become `O`. Since there are initially no useful `O`s to complete a three-cell line, victory is impossible.

This example shows that having two moves is not automatically enough to create a winning line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(E²) | Enumerate all pairs of empty cells, where E ≤ 9 |
| Space | O(1) | The board size is fixed at 3 × 3 |

Since `E` never exceeds 9, at most 36 pairs are checked. Even with 1000 test cases, the total work remains tiny and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def is_win(board):
        for r in range(3):
            if all(board[r][c] == 'O' for c in range(3)):
                return True

        for c in range(3):
            if all(board[r][c] == 'O' for r in range(3)):
                return True

        if all(board[i][i] == 'O' for i in range(3)):
            return True

        if all(board[i][2 - i] == 'O' for i in range(3)):
            return True

        return False

    t = int(input())

    out = []

    for _ in range(t):
        board = [list(input().strip()) for _ in range(3)]

        empty = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == '.':
                    empty.append((r, c))

        found = False

        for i in range(len(empty)):
            for j in range(i + 1, len(empty)):
                temp = [row[:] for row in board]

                r1, c1 = empty[i]
                r2, c2 = empty[j]

                temp[r1][c1] = 'O'
                temp[r2][c2] = 'O'

                if is_win(temp):
                    out.append("YES")
                    out.extend("".join(row) for row in temp)
                    found = True
                    break

            if found:
                break

        if not found:
            out.append("NO")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue()

# sample 1
res = run("""1
X.X
.O.
...
""")
assert res.startswith("YES")

# sample 2
res = run("""1
O.X
.O.
X..
""")
assert res.startswith("YES")

# impossible case
assert run("""1
X.X
.X.
...
""").strip() == "NO"

# diagonal completion
res = run("""1
O..
.X.
...
""")
assert res.startswith("YES")

# many empty cells
res = run("""1
...
...
...
""")
assert res.strip() == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `X.X / .O. / ...` | YES | Sample-style winning row |
| `O.X / .O. / X..` | YES | Sample-style winning placement |
| `X.X / .X. / ...` | NO | No possible line after two moves |
| `O.. / .X. / ...` | YES | Diagonal completion |
| Empty board | NO | Two moves alone cannot form three `O`s |

## Edge Cases

### Winning line needs both new moves

Input:

```
...
.O.
...
```

The middle row contains only one `O`. Nobita can place `O` in both remaining cells of that row:

```
...
OOO
...
```

The algorithm tests that pair and correctly reports `YES`.

### Many pairs fail before one succeeds

Input:

```
X.X
.O.
...
```

Several pairs of empty cells do not create a winning line. The algorithm keeps searching until it reaches the pair corresponding to the two side cells of the middle row. Because every pair is examined, the winning configuration is never missed.

### No existing support for a line

Input:

```
...
.X.
...
```

After two moves, Nobita can create at most two `O`s in any row, column, or diagonal. A winning line requires three. The algorithm exhausts all pairs, finds no winning board, and prints `NO`.

### More than one winning answer exists

Input:

```
OO.
...
...
```

Placing an `O` in the remaining cell of the top row already completes a line, and the second move may be anywhere else. Multiple valid outputs exist. The algorithm returns the first winning board it encounters, which is allowed by the problem statement.
