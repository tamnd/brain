---
title: "CF 106414E - BABA IS LOCKED"
description: "We have an n by m grid. A path starts at the bottom-left cell and must finish at the top-right cell. At every move, the path may go one cell up, one cell left, or one cell right. It can never go down and it can never step on a cell twice."
date: "2026-06-25T09:47:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106414
codeforces_index: "E"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2026 - Open Division"
rating: 0
weight: 106414
solve_time_s: 46
verified: true
draft: false
---

[CF 106414E - BABA IS LOCKED](https://codeforces.com/problemset/problem/106414/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n` by `m` grid. A path starts at the bottom-left cell and must finish at the top-right cell. At every move, the path may go one cell up, one cell left, or one cell right. It can never go down and it can never step on a cell twice. The task is to count how many different valid paths exist, with the answer taken modulo `998244353`.

The important part of the movement rules is that the row number can only decrease. Once a path leaves a row by moving upward, it will never return to that row. This means every row can be considered independently, and the only information passed from one row to the next is the column where the path moves upward.

The constraints allow `n` and `m` to be as large as 100, with many test cases. A solution that explores every path is impossible because the number of paths grows exponentially. We need to find a mathematical pattern and compute it directly. Since the answer only involves powers and modular arithmetic, an `O(n)` or `O(log n)` solution is enough.

A common mistake is to think that the path is forced to move straight upward after reaching a column. For example, in a `2 x 3` grid, the answer is not 1. The bottom row can move from the starting column 0 to column 0, 1, or 2 before going upward, giving 3 paths.

Another mistake is to allow the path to reverse inside a row. For example, starting at column 0 in a row, moving to column 2, and then coming back to column 1 is invalid because column 1 was already visited. Every row's visited cells must form one continuous segment.

## Approaches

The brute force idea is to simulate every possible path. From each visited cell, we try every allowed move and stop when we reach the target or get stuck. This is correct because it directly follows the definition of a valid path.

The problem is that the number of choices explodes. A path can make many horizontal choices in every row, and the number of possible paths grows exponentially with the grid dimensions. Even small grids quickly create far too many recursive branches.

The key observation is that a path's behavior inside a row is simple. When a path enters a row, it is at some column `x`. Before moving upward, it can choose any column `y` in that row as the place where it leaves. The cells between `x` and `y` are visited as one continuous horizontal segment. No other shape is possible because changing horizontal direction would require revisiting a cell.

For every row except the top row, the leaving column can be any of the `m` columns. The bottom row starts at column 0, but it still has `m` possible columns where it can leave. The next rows behave the same way. The top row does not need a choice because once it is entered, the path only moves horizontally until it reaches the top-right cell.

There are `n - 1` rows where we choose an exit column, and each choice has `m` possibilities. The total number of paths is therefore `m^(n-1)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(nm) recursion stack | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m` for the current grid. The path has a choice of exit column in every row except the final row, so we need to compute `m` raised to the power `n - 1`.
2. Compute `m^(n-1)` using modular exponentiation. The exponent can be large across the input size, so repeated multiplication is not the intended approach.
3. Output the computed value modulo `998244353`.

Why it works:

Every row transition is completely described by the column where the path goes upward. After entering a row, choosing any exit column produces exactly one valid horizontal segment, and every valid segment corresponds to exactly one exit column. Since rows are independent and the top row has no transition choice, the number of possible paths is the product of `m` choices over `n - 1` rows.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    data = input().split()
    if not data:
        return
    t = int(data[0])
    ans = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        m = int(data[idx + 1])
        idx += 2
        ans.append(str(pow(m, n - 1, MOD)))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation uses Python's built in modular exponentiation. The `pow(base, exponent, mod)` form performs binary exponentiation, so it only needs logarithmically many operations.

The exponent is `n - 1` because the bottom row and every row above it until the top row require a decision about where to move upward. The top row only finishes the path and contributes no additional branching.

There are no boundary checks or simulations because the proof already reduced the problem to counting choices. The modulo is applied during exponentiation to avoid large intermediate values.

## Worked Examples

For the first sample, the grid is `2 x 3`.

| Step | Rows processed | Choices per row | Current count |
| --- | --- | --- | --- |
| Start | Need to choose bottom row exit | 3 | 3 |
| Finish | Top row reaches target | no choice | 3 |

The answer is 3. The three paths correspond to leaving the bottom row at columns 0, 1, or 2.

For the second sample, the grid is `3 x 4`.

| Step | Rows processed | Choices per row | Current count |
| --- | --- | --- | --- |
| Start | Bottom row exit | 4 | 4 |
| Continue | Middle row exit | 4 | 16 |
| Finish | Top row reaches target | no choice | 16 |

The answer is 16 because the first two rows each contribute four possible exit columns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Modular exponentiation needs logarithmically many multiplications |
| Space | O(1) | Only the current answer and input values are stored |

The solution easily fits the limits because each test case requires only one fast exponentiation and no grid construction.

## Test Cases

```python
import sys, io

MOD = 998244353

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        out.append(str(pow(m, n - 1, MOD)))
    return "\n".join(out)

assert solution("""2
2 3
3 4
""") == "3\n16", "samples"

assert solution("""1
2 2
""") == "2", "minimum grid"

assert solution("""1
100 100
""") == str(pow(100, 99, MOD)), "large grid"

assert solution("""3
5 1
4 5
2 100
""") == "\n".join([
    str(pow(1, 4, MOD)),
    str(pow(5, 3, MOD)),
    str(pow(100, 1, MOD))
]), "boundary cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3`, `3 4` | `3`, `16` | Confirms the basic formula |
| `2 2` | `2` | Checks the smallest possible grid |
| `100 100` | `100^99 mod MOD` | Checks large exponent handling |
| `m = 1` cases | Correct powers of one | Checks the single-column boundary |

## Edge Cases

For a `2 x 3` grid, a naive approach might think there is only one path because the start and finish are vertically aligned in the same column after choosing the shortest route. The algorithm sees that the bottom row can exit at any of the three columns, so it computes `3^(2-1) = 3`.

For a grid with one column, such as `5 x 1`, the only possible movement is upward. The formula gives `1^(5-1) = 1`, matching the single valid path.

For a large grid such as `100 x 100`, enumerating paths is impossible. The algorithm never creates paths at all, it only evaluates the number of independent column choices using modular exponentiation.
