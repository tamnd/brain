---
title: "CF 1499A - Domino on Windowsill"
description: "We are given a board of size $2 times n$, where the first $k1$ cells of the top row and $k2$ cells of the bottom row are white, and the rest are black. We are also given a number of white dominoes $w$ and black dominoes $b$."
date: "2026-06-10T21:26:40+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1499
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 106 (Rated for Div. 2)"
rating: 800
weight: 1499
solve_time_s: 270
verified: true
draft: false
---

[CF 1499A - Domino on Windowsill](https://codeforces.com/problemset/problem/1499/A)

**Rating:** 800  
**Tags:** combinatorics, constructive algorithms, math  
**Solve time:** 4m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a board of size $2 \times n$, where the first $k_1$ cells of the top row and $k_2$ cells of the bottom row are white, and the rest are black. We are also given a number of white dominoes $w$ and black dominoes $b$. Each domino is $2 \times 1$ and can be placed either horizontally or vertically, but it must cover cells of the same color. The task is to determine whether it is possible to place all $w + b$ dominoes on the board without overlaps.

The inputs describe multiple test cases. For each test case, $n$ can go up to $1000$ and the number of test cases $t$ can go up to $3000$, so any algorithm must handle up to $3 \cdot 10^6$ board cells in total. This rules out any solution that tries to explicitly simulate all domino placements, because that could easily lead to $O(n^2)$ work per test case.

Non-obvious edge cases appear when one row has zero white or black cells, when dominoes must be placed vertically but one row does not have enough corresponding cells, or when there are odd numbers of single-colored cells that cannot form a domino. For example, a board with $n=1$, $k_1=0$, $k_2=1$, and $w=1$ cannot accommodate a white domino because there is only one white cell. A careless approach that only checks the total number of white cells would incorrectly say placement is possible.

## Approaches

The brute-force approach would attempt to simulate placing dominoes in every valid position. One could try all horizontal placements and then vertical placements, or even try all permutations recursively. This is correct because it enumerates every valid configuration, but it is far too slow. For $n = 1000$, the number of placements grows combinatorially, and with $t = 3000$ test cases, this quickly exceeds practical limits.

The key insight is that we do not need to simulate placements. Each domino covers exactly two cells of the same color. For vertical dominoes, the maximum number we can place is $\min(k_1, k_2)$ for white dominoes and $\min(n - k_1, n - k_2)$ for black dominoes. After using vertical dominoes, the remaining cells in each row can only be paired horizontally within the same row. Thus, the maximum number of dominoes of a color is the sum of vertically-placed dominoes plus half of the remaining single-colored cells. This reduces the problem to simple arithmetic on counts of colored cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * t) | O(n) | Too slow |
| Counting Cells | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $k_1$, $k_2$, $w$, $b$. Here $k_1$ and $k_2$ are the number of white cells in the top and bottom rows, respectively.
2. Compute the maximum number of white dominoes that can be placed. The vertical dominoes are limited by $\min(k_1, k_2)$. The remaining white cells in the top row are $k_1 - \min(k_1, k_2)$, and in the bottom row $k_2 - \min(k_1, k_2)$. Each horizontal domino occupies 2 cells, so the number of horizontal dominoes we can place is $(\text{remaining top} + \text{remaining bottom}) // 2$. Add vertical and horizontal counts to get `max_white`.
3. Compute the maximum number of black dominoes similarly. The number of black cells in the top row is $n - k_1$, and in the bottom row $n - k_2$. The maximum vertical dominoes are $\min(n - k_1, n - k_2)$ and horizontal dominoes are the remaining black cells divided by 2. Sum these for `max_black`.
4. If $w \le max_white$ and $b \le max_black$, print "YES"; otherwise, print "NO". This ensures that the board has enough space for all dominoes without explicitly placing them.

**Why it works**: The algorithm correctly counts the maximum possible dominoes of each color. Vertical dominoes are always optimal to maximize usage, and horizontal dominoes use any leftover single-colored cells. Since dominoes cannot overlap and each domino covers exactly 2 cells, exceeding these maxima is impossible. This arithmetic guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k1, k2 = map(int, input().split())
    w, b = map(int, input().split())
    
    # Maximum white dominoes
    vertical_white = min(k1, k2)
    remaining_white_top = k1 - vertical_white
    remaining_white_bottom = k2 - vertical_white
    horizontal_white = (remaining_white_top + remaining_white_bottom) // 2
    max_white = vertical_white + horizontal_white
    
    # Maximum black dominoes
    black_top = n - k1
    black_bottom = n - k2
    vertical_black = min(black_top, black_bottom)
    remaining_black_top = black_top - vertical_black
    remaining_black_bottom = black_bottom - vertical_black
    horizontal_black = (remaining_black_top + remaining_black_bottom) // 2
    max_black = vertical_black + horizontal_black
    
    if w <= max_white and b <= max_black:
        print("YES")
    else:
        print("NO")
```

The code first reads the number of test cases, then iterates through each. Maximum dominoes for each color are computed separately. Using integer division ensures only full dominoes are counted. The condition `w <= max_white and b <= max_black` is the key decision point. Careful subtraction prevents negative counts and ensures that the division correctly represents pairs of cells.

## Worked Examples

**Example 1**

Input: `1 0 1` with `w=1, b=0`

| Variable | Value |
| --- | --- |
| vertical_white | 0 |
| remaining_white_top | 0 |
| remaining_white_bottom | 1 |
| horizontal_white | 0 |
| max_white | 0 |

Since `w = 1 > max_white = 0`, output is "NO".

**Example 2**

Input: `4 3 1` with `w=2, b=2`

| Variable | Value |
| --- | --- |
| vertical_white | 1 |
| remaining_white_top | 2 |
| remaining_white_bottom | 0 |
| horizontal_white | 1 |
| max_white | 2 |
| black_top | 1 |
| black_bottom | 3 |
| vertical_black | 1 |
| remaining_black_top | 0 |
| remaining_black_bottom | 2 |
| horizontal_black | 1 |
| max_black | 2 |

Both `w <= max_white` and `b <= max_black`, output "YES".

These traces show the algorithm correctly handles uneven rows and both vertical and horizontal domino placement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves simple arithmetic and comparisons |
| Space | O(1) | Only integer variables per test case, no large arrays |

The solution scales linearly with the number of test cases, independent of $n$, making it efficient enough for the constraints $t \le 3000$ and $n \le 1000$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, k1, k2 = map(int, input().split())
        w, b = map(int, input().split())
        vertical_white = min(k1, k2)
        remaining_white_top = k1 - vertical_white
        remaining_white_bottom = k2 - vertical_white
        horizontal_white = (remaining_white_top + remaining_white_bottom) // 2
        max_white = vertical_white + horizontal_white
        black_top = n - k1
        black_bottom = n - k2
        vertical_black = min(black_top, black_bottom)
        remaining_black_top = black_top - vertical_black
        remaining_black_bottom = black_bottom - vertical_black
        horizontal_black = (remaining_black_top + remaining_black_bottom) // 2
        max_black = vertical_black + horizontal_black
        if w <= max_white and b <= max_black:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("5\n1 0 1\n1 0\n1 1 1\n0 0\n3 0 0\n1 3\n4 3 1\n2 2\n5 4 3\n3 1") == "NO\nYES\nNO\nYES\nYES"

# custom cases
assert run("1\n1 0 0\n0 1") == "YES", "single column, only black domino"
assert run("1\n1 1 1\n1 0") == "YES", "single column, only white domino"
assert run("1\n2 1 1\n1 1") == "YES", "two
```
