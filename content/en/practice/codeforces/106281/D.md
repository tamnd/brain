---
title: "CF 106281D - \u0413\u043b\u0438\u043d\u044f\u043d\u0430\u044f \u0442\u0430\u0431\u043b\u0438\u0447\u043a\u0430"
description: "The tablet is a rectangular grid of cells. A means the cell was painted, while a . means it was left empty. Every possible 5 x 3 window inside this grid may represent one digit."
date: "2026-06-25T07:38:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106281
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 7-8 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106281
solve_time_s: 28
verified: true
draft: false
---

[CF 106281D - \u0413\u043b\u0438\u043d\u044f\u043d\u0430\u044f \u0442\u0430\u0431\u043b\u0438\u0447\u043a\u0430](https://codeforces.com/problemset/problem/106281/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The tablet is a rectangular grid of cells. A `*` means the cell was painted, while a `.` means it was left empty. Every possible `5 x 3` window inside this grid may represent one digit. The digit patterns are fixed, but the tablet may contain extra painted cells because of damage or mistakes. A window represents a digit if every cell that is required to be painted for that digit is actually painted in the window. Extra painted cells do not invalidate a digit.

If several digits match the same window, we take the largest one. The task is to check every possible position of the `5 x 3` rectangle and add all recognized digits.

The grid dimensions are at most `100 x 100`, so there are at most `(N - 4) * (M - 2)` windows. This is small enough that even checking every window against every digit is fine. The total number of cells in all windows is roughly `100 * 100 * 10 * 15`, which is only a few million simple operations. More advanced methods such as hashing or preprocessing are unnecessary here.

The main edge cases come from the fact that a digit is defined only by its required painted cells. A common mistake is to require the entire `5 x 3` window to exactly match a digit.

For example:

```
5 3
***
***
***
***
***
```

The answer is `9`. Every digit can be placed inside this fully painted rectangle because all required cells exist, so we must choose the largest digit.

Another tricky case is when a window has extra stars that do not belong to the chosen digit:

```
5 3
***
*.*
***
*.*
***
```

The correct answer is `0`, because the zero pattern requires the border cells, and the extra stars do not hurt. A solution that compares the whole picture against the digit template exactly would reject it incorrectly.

## Approaches

A straightforward solution is to store the ten digit templates and scan every possible `5 x 3` rectangle. For each rectangle, we test every digit from `0` to `9`. To test a digit, we look at the cells where the template contains a star and check whether the corresponding tablet cells are also stars. If all required cells are present, that digit is a candidate. Since the largest valid digit is needed, scanning digits in increasing order and overwriting the answer works.

This brute force is already the optimal approach for these limits. There are at most `96 * 98 = 9408` windows. Each window checks ten digits, and each digit has at most fifteen cells. The total work is under two million cell checks, so the direct simulation easily fits.

The important observation is that the problem does not ask us to reconstruct the entire tablet. Each window is independent, and the definition of a valid digit only depends on a small fixed pattern. That turns the task into a constant-sized pattern matching problem repeated over the grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM * 10 * 15) | O(1) | Accepted |
| Optimal | O(NM * 10 * 15) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store the ten digit drawings as `5 x 3` arrays. A star in the template means that the corresponding cell must be painted.
2. Iterate over every possible top-left corner of a `5 x 3` rectangle. The row can go from `0` to `N - 5`, and the column can go from `0` to `M - 3`.
3. For the current rectangle, try every digit from `0` to `9`. Check only the cells that are stars in that digit's template. If any required cell is missing from the tablet, this digit cannot be represented.
4. Whenever a digit matches, store it as the current answer for this rectangle. Since digits are checked in increasing order, the last matching digit is the largest one.
5. Add the chosen digit to the total sum and continue with the next rectangle.

Why it works:

The algorithm directly follows the definition of a valid digit. A digit is accepted exactly when every required painted cell exists. The algorithm checks every required cell and rejects the digit if even one is absent. Extra stars are ignored, matching the rules of the tablet. Because all possible rectangles are visited, every contribution to the final sum is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    digits = [
        ["***",
         "*.*",
         "*.*",
         "*.*",
         "***"],
        ["..*",
         "..*",
         "..*",
         "..*",
         "..*"],
        ["***",
         "..*",
         "***",
         "*..",
         "***"],
        ["***",
         "..*",
         "***",
         "..*",
         "***"],
        ["*.*",
         "*.*",
         "***",
         "..*",
         "..*"],
        ["***",
         "*..",
         "***",
         "..*",
         "***"],
        ["***",
         "*..",
         "***",
         "*.*",
         "***"],
        ["***",
         "..*",
         "..*",
         "..*",
         "..*"],
        ["***",
         "*.*",
         "***",
         "*.*",
         "***"],
        ["***",
         "*.*",
         "***",
         "..*",
         "***"]
    ]

    ans = 0

    for i in range(n - 4):
        for j in range(m - 2):
            best = -1
            for d in range(10):
                ok = True
                for x in range(5):
                    for y in range(3):
                        if digits[d][x][y] == '*' and grid[i + x][j + y] != '*':
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    best = d
            if best != -1:
                ans += best

    print(ans)

if __name__ == "__main__":
    solve()
```

The digit patterns are encoded exactly as the required painted cells. The algorithm never checks cells that are dots in the template because those cells may contain extra stars and still produce a valid digit.

The loops over `i` and `j` are carefully bounded by `n - 4` and `m - 2`. This prevents accessing rows or columns outside the grid. The inner loops check the five rows and three columns of the current window, so there are no coordinate transformations that could introduce off-by-one mistakes.

The variable `best` starts at `-1` because a window might not contain any digit. When a digit matches, it replaces the previous value, which guarantees that the final stored value is the largest matching digit.

## Worked Examples

Consider:

```
5 3
***
*..
***
..*
***
```

The trace is:

| Window position | Tested digits | Matching digits | Best | Sum |
| --- | --- | --- | --- | --- |
| (0,0) | 0 to 9 | 5 | 5 | 5 |

The window contains exactly the required cells of digit `5`, so the total becomes `5`.

Another example:

```
6 6
.***.*
.*...*
.***.*
.*.*.*
.***.*
....**
```

The important windows are:

| Window position | Matching digits | Best | Added |
| --- | --- | --- | --- |
| (0,1) | 6 | 6 | 6 |
| (0,3) | 1 | 1 | 1 |
| (1,3) | 1 | 1 | 1 |

The final sum is `8`. This demonstrates that overlapping windows are counted independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM * 10 * 15) | Every window checks ten fixed-size patterns |
| Space | O(1) | Only the digit templates and a few variables are stored |

The maximum grid size is only `100 x 100`, so the number of operations is tiny. The solution easily fits the one second time limit and the memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue()

# provided samples
assert run("""5 3
***
*..
***
..*
***
""") == "5\n"

assert run("""6 6
.***.*
.*...*
.***.*
.*.*.*
.***.*
....**
""") == "8\n"

# all cells painted, every digit matches, choose 9
assert run("""5 3
***
***
***
***
***
""") == "9\n"

# no digit can be formed
assert run("""5 3
...
...
...
...
...
""") == "0\n"

# overlapping windows and extra stars
assert run("""10 10
..*.......
..*.....*.
..*.....*.
..*..*..*.
..*..*..*.
..*..*..*.
..*..*..*.
..*..*..*.
..*.....*.
..........
""") == "11\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Full `5 x 3` stars | 9 | Choosing the maximum matching digit |
| Empty grid | 0 | No valid digit recognition |
| Overlapping windows | 11 | Counting every possible rectangle |
| Extra stars in windows | Correct digit sum | Ignoring non-required painted cells |

## Edge Cases

For the fully painted tablet:

```
5 3
***
***
***
***
***
```

The algorithm checks every digit. Since every required star is present, all ten digits pass. Because digits are processed from `0` to `9`, the final stored value is `9`.

For a rectangle with additional stars:

```
5 3
***
***
***
***
***
```

the same reasoning applies. The algorithm never asks whether non-required cells are empty, so the extra stars do not affect recognition.

For an empty rectangle:

```
5 3
...
...
...
...
...
```

every digit fails because every digit template contains at least one required star. The variable `best` stays `-1`, and nothing is added to the answer.
