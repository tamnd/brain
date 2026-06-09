---
title: "CF 1907A - Rook"
description: "The task is to list all legal moves of a rook from a given square on an empty chessboard. A rook moves horizontally along its row or vertically along its column, stopping only at the edges of the board."
date: "2026-06-08T20:36:35+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1907
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 913 (Div. 3)"
rating: 800
weight: 1907
solve_time_s: 116
verified: false
draft: false
---

[CF 1907A - Rook](https://codeforces.com/problemset/problem/1907/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to list all legal moves of a rook from a given square on an empty chessboard. A rook moves horizontally along its row or vertically along its column, stopping only at the edges of the board. Each test case gives a square in standard chess notation, like "d5", where the first character is the column from 'a' to 'h' and the second is the row from '1' to '8'. The output should list all squares the rook can reach from that starting point, in any order.

The input constraint is small: at most 64 test cases and the board size is fixed at 8x8. This means even a solution that naively enumerates all moves for every test case runs in constant time per test case, because a rook can only have up to 14 possible moves (7 along its row, 7 along its column) and there are only 64 squares. The only edge case occurs when the rook is on the edge or corner of the board. For example, if the rook is at "a1", its legal moves are "a2" through "a8" vertically and "b1" through "h1" horizontally. A careless approach might accidentally include the starting square in the output, which would be incorrect.

## Approaches

The most straightforward approach is to simulate the rook's movement. For the row containing the rook, iterate through all columns 'a' to 'h', skipping the rook's current column, and output each square. For the column containing the rook, iterate through all rows '1' to '8', skipping the rook's current row, and output each square. This approach is correct because it directly implements the rook's movement rules. It is also efficient, because each test case involves at most 14 operations, so even with 64 test cases, the total operations are negligible.

There is no asymptotically faster solution because the output itself can be up to 14 squares per test case. Any solution must at least print all legal moves, so the naive simulation is already optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test case | O(1) | Accepted |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the position string like "d5".
3. Extract the column character and row digit from the string. Convert the column to an integer index if convenient, or keep it as a character.
4. Iterate over all column letters from 'a' to 'h'. For each column, if it is not equal to the rook's current column, output the square formed by that column and the rook's current row.
5. Iterate over all row digits from '1' to '8'. For each row, if it is not equal to the rook's current row, output the square formed by the rook's current column and that row.
6. Move to the next test case.

Why it works: The algorithm iterates exactly over all squares in the rook's row and column, skipping the square it currently occupies. Since the board is empty, every such square is reachable and no square is omitted or repeated. The constraints guarantee that the loops always stay within 'a'-'h' and '1'-'8', so boundary conditions are inherently handled.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    pos = input().strip()
    col, row = pos[0], pos[1]

    for c in 'abcdefgh':
        if c != col:
            print(c + row)
    for r in '12345678':
        if r != row:
            print(col + r)
```

The first section reads the number of test cases. For each test case, we parse the column and row from the input string. The next two loops enumerate all possible horizontal moves along the row and vertical moves along the column, skipping the starting square itself. Using characters directly avoids conversion mistakes between indices and letters. This also ensures all moves are printed in standard chess notation.

## Worked Examples

Sample 1:

Input: "d5"

| Variable | Value during row loop | Output |
| --- | --- | --- |
| c | 'a' | 'a5' |
| c | 'b' | 'b5' |
| c | 'c' | 'c5' |
| c | 'd' | skipped |
| c | 'e' | 'e5' |
| c | 'f' | 'f5' |
| c | 'g' | 'g5' |
| c | 'h' | 'h5' |

| Variable | Value during column loop | Output |
| --- | --- | --- |
| r | '1' | 'd1' |
| r | '2' | 'd2' |
| r | '3' | 'd3' |
| r | '4' | 'd4' |
| r | '5' | skipped |
| r | '6' | 'd6' |
| r | '7' | 'd7' |
| r | '8' | 'd8' |

The trace confirms that the algorithm produces exactly 14 squares excluding the starting square, covering all possible rook moves.

Another example:

Input: "a1"

Row loop outputs 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'

Column loop outputs 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'

All legal moves are produced, showing that edge positions are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case has at most 14 iterations to enumerate squares. |
| Space | O(1) | No extra memory proportional to input size is used. |

Given up to 64 test cases, the total operations are under 1000, far below the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        pos = input().strip()
        col, row = pos[0], pos[1]
        for c in 'abcdefgh':
            if c != col:
                print(c + row)
        for r in '12345678':
            if r != row:
                print(col + r)
    return output.getvalue().strip()

# Provided sample
assert run("1\nd5\n") == '\n'.join([
    'a5','b5','c5','e5','f5','g5','h5',
    'd1','d2','d3','d4','d6','d7','d8'
]), "sample 1"

# Custom: corner
assert run("1\na1\n") == '\n'.join([
    'b1','c1','d1','e1','f1','g1','h1',
    'a2','a3','a4','a5','a6','a7','a8'
]), "corner"

# Custom: opposite corner
assert run("1\nh8\n") == '\n'.join([
    'a8','b8','c8','d8','e8','f8','g8',
    'h1','h2','h3','h4','h5','h6','h7'
]), "opposite corner"

# Custom: center position
assert run("1\ne4\n") == '\n'.join([
    'a4','b4','c4','d4','f4','g4','h4',
    'e1','e2','e3','e5','e6','e7','e8'
]), "center"

# Custom: multiple test cases
assert run("2\nd5\na1\n") == '\n'.join([
    'a5','b5','c5','e5','f5','g5','h5',
    'd1','d2','d3','d4','d6','d7','d8',
    'b1','c1','d1','e1','f1','g1','h1',
    'a2','a3','a4','a5','a6','a7','a8'
]), "multiple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "a1" | b1-c1-d1-e1-f1-g1-h1, a2-a8 | Rook at corner |
| "h8" | a8-g8-f8-... h1-h7 | Opposite corner |
| "e4" | a4-d4-f4-h4, e1-e3, e5-e8 | Center of board |
| "d5\na1" | Combined outputs | Multiple test cases |

## Edge Cases

For a rook on "a1", row loop generates 'b1' through 'h1', skipping 'a1'. Column loop generates 'a2' through 'a8', skipping 'a1'. This covers the top-left corner correctly with no off-by-one errors. A rook on "h8" similarly produces all legal moves without exceeding board boundaries. The algorithm inherently handles the maximum and
