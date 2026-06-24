---
title: "CF 105556I - \u68cb\u76d8"
description: "We have an $n times m$ chessboard and a puzzle piece that always covers exactly three cells. The crucial geometric observation is that if we color the board like a standard chessboard, every valid piece placement covers three cells of the same color."
date: "2026-06-25T06:08:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105556
codeforces_index: "I"
codeforces_contest_name: "The 6th FanRuan Cup Southeast University Programming Contest (Winter)"
rating: 0
weight: 105556
solve_time_s: 50
verified: true
draft: false
---

[CF 105556I - \u68cb\u76d8](https://codeforces.com/problemset/problem/105556/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times m$ chessboard and a puzzle piece that always covers exactly three cells.

The crucial geometric observation is that if we color the board like a standard chessboard, every valid piece placement covers three cells of the same color. Once that property is discovered, the original packing problem becomes a counting problem on black and white cells.

Let $B$ be the number of black cells and $W$ be the number of white cells on the board.

Every piece consumes exactly three cells of one color, so no solution can use more than

$$\left\lfloor \frac{B}{3} \right\rfloor +
\left\lfloor \frac{W}{3} \right\rfloor$$

pieces.

The remaining question is whether this upper bound is always achievable. The official hint points toward a constructive argument: after separating cells by color, each color class forms a connected grid graph. A connected graph with $k$ vertices can be split into as many disjoint connected components of size $3$ as possible, leaving fewer than three unused vertices. That means every color class can realize exactly $\lfloor k/3 \rfloor$ pieces. Combining the two colors achieves the upper bound.

The board size is tiny from a computational perspective. Once the formula is known, only a few arithmetic operations are required.

A common mistake is to assume the answer is simply $\lfloor nm/3 \rfloor$. The colors matter.

For example, on a $2 \times 2$ board:

```
B W
W B
```

There are two black cells and two white cells.

$$\left\lfloor \frac{2}{3} \right\rfloor +
\left\lfloor \frac{2}{3} \right\rfloor = 0$$

while

$$\left\lfloor \frac{4}{3} \right\rfloor = 1$$

so treating all cells together gives the wrong result.

Another easy pitfall appears when the numbers of black and white cells differ.

For a $3 \times 3$ board:

$$B = 5,\quad W = 4$$

and

$$\left\lfloor \frac{5}{3} \right\rfloor +
\left\lfloor \frac{4}{3} \right\rfloor
= 1 + 1 = 2.$$

Using only $\lfloor 9/3 \rfloor = 3$ would overestimate the answer.

## Approaches

A brute force approach would try to enumerate piece placements and search for a maximum packing. Even for moderate board sizes this becomes infeasible because the number of possible configurations grows exponentially.

The key observation completely changes the problem.

After coloring the board in a checkerboard pattern, every piece occupies three cells of the same color. That immediately separates the board into two independent resources: black cells and white cells.

If a color class contains $k$ cells, each piece consumes exactly three of them, so at most $\lfloor k/3 \rfloor$ pieces can be formed from that color.

The remaining step is proving that this upper bound is achievable. The connectedness argument from the hint guarantees that a connected set of $k$ cells can always be partitioned into as many connected triples as possible, leaving at most two unused cells. Thus each color contributes exactly $\lfloor k/3 \rfloor$ pieces.

All that remains is computing the numbers of black and white cells:

$$B = \left\lceil \frac{nm}{2} \right\rceil,
\qquad
W = \left\lfloor \frac{nm}{2} \right\rfloor.$$

The answer becomes

$$\left\lfloor \frac{B}{3} \right\rfloor +
\left\lfloor \frac{W}{3} \right\rfloor.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $m$.
2. Compute the total number of cells.

$$S = n \times m$$

1. Compute the number of black cells.

$$B = \frac{S + 1}{2}$$

using integer division.

1. Compute the number of white cells.

$$W = \frac{S}{2}$$

using integer division.

1. Compute

$$\left\lfloor \frac{B}{3} \right\rfloor +
\left\lfloor \frac{W}{3} \right\rfloor.$$

1. Output the result.

### Why it works

Every piece occupies exactly three cells of a single chessboard color. A color class with $k$ cells cannot contribute more than $\lfloor k/3 \rfloor$ pieces because each piece consumes three cells.

The color classes are connected grid graphs. A connected graph with $k$ vertices can be repeatedly separated into connected components of size three, leaving fewer than three vertices unused. Thus each color class can realize exactly $\lfloor k/3 \rfloor$ pieces.

Since black and white cells are independent, the maximum number of pieces is

$$\left\lfloor \frac{B}{3} \right\rfloor +
\left\lfloor \frac{W}{3} \right\rfloor.$$

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

s = n * m
black = (s + 1) // 2
white = s // 2

print(black // 3 + white // 3)
```

The implementation follows the formula directly.

The expression `(s + 1) // 2` computes the larger color class on a checkerboard, which is the black count when the total number of cells is odd.

The expression `s // 2` computes the smaller color class.

Integer division by three gives the number of complete triples available from each color class. Adding those two values produces the answer.

No loops, recursion, or large data structures are needed.

## Worked Examples

### Example 1

Input:

```
2 2
```

Total cells:

$$S = 4$$

| Variable | Value |
| --- | --- |
| S | 4 |
| B | 2 |
| W | 2 |
| B // 3 | 0 |
| W // 3 | 0 |
| Answer | 0 |

The board contains only two cells of each color, so no color has enough cells to form a piece.

### Example 2

Input:

```
3 3
```

| Variable | Value |
| --- | --- |
| S | 9 |
| B | 5 |
| W | 4 |
| B // 3 | 1 |
| W // 3 | 1 |
| Answer | 2 |

The black cells can form one triple, and the white cells can form one triple. One black cell and one white cell remain unused.

This example demonstrates why the answer is not simply $\lfloor 9/3 \rfloor = 3$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations |
| Space | O(1) | Uses constant extra memory |

The solution performs a fixed amount of work regardless of the board size, so it easily satisfies any reasonable contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, sys.stdin.readline().split())
    s = n * m
    black = (s + 1) // 2
    white = s // 2

    return str(black // 3 + white // 3)

# custom cases

assert run("1 1\n") == "0", "minimum board"

assert run("2 2\n") == "0", "not enough cells of either color"

assert run("3 3\n") == "2", "odd-sized board"

assert run("3 4\n") == "4", "equal color counts"

assert run("100000 100000\n") == str(((100000 * 100000 + 1) // 2) // 3 + ((100000 * 100000) // 2) // 3), "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Smallest possible board |
| `2 2` | `0` | Cannot form a triple from either color |
| `3 3` | `2` | Odd number of cells |
| `3 4` | `4` | Equal black and white counts |
| `100000 100000` | Formula value | Large-number arithmetic |

## Edge Cases

Consider the input

```
2 2
```

The board contains two black cells and two white cells.

The algorithm computes

$$B=2,\quad W=2$$

and returns

$$0+0=0.$$

A naive solution using $\lfloor nm/3 \rfloor$ would return $1$, which is impossible because no color class contains three cells.

Now consider

```
3 3
```

The algorithm computes

$$B=5,\quad W=4.$$

The answer becomes

$$\left\lfloor \frac{5}{3} \right\rfloor +
\left\lfloor \frac{4}{3} \right\rfloor
=2.$$

The remaining cells are one black and one white cell, neither of which can participate in another piece. The formula naturally handles this leftover situation.

Finally, for a board with an even number of cells such as

```
3 4
```

we get

$$B=W=6.$$

The answer is

$$6/3 + 6/3 = 4.$$

Both color classes are used completely, showing that the formula also handles the case with no leftovers.
