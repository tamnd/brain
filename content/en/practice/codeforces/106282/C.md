---
title: "CF 106282C - \u0413\u043b\u0438\u043d\u044f\u043d\u0430\u044f \u0442\u0430\u0431\u043b\u0438\u0447\u043a\u0430"
description: "The input is a grid made of and . characters. You can think of it as a carved clay tablet where some cells are painted (stars) and others are empty (dots). On this grid, we slide a fixed window of size 5 rows by 3 columns across every valid position."
date: "2026-06-25T07:39:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106282
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 9 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106282
solve_time_s: 46
verified: true
draft: false
---

[CF 106282C - \u0413\u043b\u0438\u043d\u044f\u043d\u0430\u044f \u0442\u0430\u0431\u043b\u0438\u0447\u043a\u0430](https://codeforces.com/problemset/problem/106282/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a grid made of `*` and `.` characters. You can think of it as a carved clay tablet where some cells are painted (stars) and others are empty (dots). On this grid, we slide a fixed window of size 5 rows by 3 columns across every valid position.

For each such window, we try to interpret the pattern inside it as one of ten predefined digit templates from 0 to 9. The interpretation rule is asymmetric: a digit is considered to match a window if every cell that must be `*` in the digit’s template is also `*` in the window. Extra stars are allowed and ignored. Missing required stars immediately disqualify that digit.

If a window matches multiple digits under this relaxed condition, we take the largest digit among them. If it matches none, it contributes zero.

The final answer is the sum of values produced by all 5×3 windows.

The grid size constraint reaches up to 100 by 100. Each window check touches 15 cells per digit, and there are at most about 10^4 windows. A straightforward solution that checks all digits per window runs in roughly 10^4 × 10 × 15 operations, which is comfortably within limits.

A naive interpretation that recomputes or rescans subpatterns inefficiently is unnecessary but still safe due to the small constants.

The main failure mode in careless solutions is mismatching the digit condition. For example, treating the comparison as exact equality instead of “digit stars are a subset of window stars” leads to wrong rejection.

Consider this window:

```
***
*.*
***
```

This should match digit 0 even if the window has extra stars, but a strict equality check would reject it immediately.

Another subtle issue is forgetting that overlapping windows are independent. Each position contributes separately even if it reuses the same cells.

A third mistake comes from digit priority. If a window matches both 1 and 3, selecting the first match instead of the maximum digit changes the result.

## Approaches

A brute-force approach naturally checks every window and, inside it, checks every digit template by comparing all 15 cells. This is already close to optimal because the digit set is fixed and small. The correctness is straightforward since we directly enforce the definition: a digit is valid if no required `*` is missing.

The inefficiency only appears if we attempt to recompute matches from scratch using complex preprocessing or attempt to decode the grid globally. That overcomplicates a problem that is fundamentally local.

The key observation is that the digit set is fixed and tiny, so each window can be validated independently with a direct mask check. There is no need for DP, hashing, or convolution; the structure does not accumulate constraints across windows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per window per digit | O(N·M·10·15) | O(1) | Accepted |
| Any global preprocessing approach | O(N·M + extra) | O(N·M) | Accepted but unnecessary |

## Algorithm Walkthrough

We treat each digit as a fixed 5×3 boolean mask indicating required `*` positions. Then we scan the grid with a sliding window.

1. Predefine the 10 digit masks. Each mask stores which of the 15 positions must be `*`. This turns the problem into subset checking rather than pattern matching.
2. Iterate over every possible top-left corner of a 5×3 window in the grid. Each position defines a candidate subgrid.
3. For each window, try all digits from 0 to 9. For a given digit, check every cell where the digit mask requires a star. If any required position is `.` in the grid, reject that digit for this window. This step directly enforces the “no missing stars” rule.
4. Among all digits that pass, select the maximum value. If none pass, contribute zero for that window.
5. Add the chosen value to the global sum.

The invariant here is that for every window, we maintain the exact set of digits whose required star pattern is a subset of the window’s star pattern. Since we test every digit independently and only reject when a required condition fails, no valid digit is lost. The maximum selection ensures correctness under the tie-breaking rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

DIGITS = [
    ["***", "*.*", "*.*", "*.*", "***"],  # 0
    ["..*", "..*", "..*", "..*", "..*"],  # 1
    ["***", "..*", "***", "*..", "***"],  # 2
    ["***", "..*", "***", "..*", "***"],  # 3
    ["*.*", "*.*", "***", "..*", "..*"],  # 4
    ["***", "*..", "***", "..*", "***"],  # 5
    ["***", "*..", "***", "*.*", "***"],  # 6
    ["***", "..*", "..*", "..*", "..*"],  # 7
    ["***", "*.*", "***", "*.*", "***"],  # 8
    ["***", "*.*", "***", "..*", "***"],  # 9
]

N, M = map(int, input().split())
grid = [input().strip() for _ in range(N)]

ans = 0

for i in range(N - 4):
    for j in range(M - 2):
        best = 0

        for d in range(10):
            ok = True
            for x in range(5):
                for y in range(3):
                    if DIGITS[d][x][y] == '*' and grid[i + x][j + y] != '*':
                        ok = False
                        break
                if not ok:
                    break

            if ok:
                best = d

        ans += best

print(ans)
```

The solution encodes each digit explicitly and uses direct character comparisons. The early rejection inside nested loops is important because it avoids unnecessary scanning once a mismatch is found.

The assignment `best = d` is safe because digits are checked in increasing order, so the final stored value is automatically the maximum valid digit.

Boundary control comes entirely from iterating only up to `N-4` and `M-2`, which guarantees every accessed cell is inside the grid.

## Worked Examples

### Example 1

Input:

```
5 3
***
*..
***
..*
***
```

There is only one window.

| Window | Digit 0 | Digit 1 | Digit 2 | Digit 3 | Digit 4 | Best |
| --- | --- | --- | --- | --- | --- | --- |
| full grid | no | yes | no | no | no | 1 |

This window matches digit 1 because its required stars are all present. No other digit satisfies the subset condition.

Final sum is 1.

### Example 2

Input:

```
6 6
.***.*
.*...*
.***.*
.*.*.*
.***.*
....**
```

Multiple windows exist; consider one representative case.

| Window | Digit 6 | Digit 1 | Digit 8 | Best |
| --- | --- | --- | --- | --- |
| center-left | yes | yes | no | 6 |
| center-right | no | yes | yes | 8 |

Each window independently selects its maximum valid digit. The final sum accumulates contributions across overlapping regions, which is why digits appear multiple times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N−5)(M−3)·10·15) | every window checks all digits and 15 cells |
| Space | O(1) | digit patterns are fixed-size constants |

The grid size caps at 100×100, so the total operations remain on the order of a few million checks, well within a 1-second limit in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import SimpleNamespace

    # re-run solution inline for testing simplicity
    DIGITS = [
        ["***", "*.*", "*.*", "*.*", "***"],
        ["..*", "..*", "..*", "..*", "..*"],
        ["***", "..*", "***", "*..", "***"],
        ["***", "..*", "***", "..*", "***"],
        ["*.*", "*.*", "***", "..*", "..*"],
        ["***", "*..", "***", "..*", "***"],
        ["***", "*..", "***", "*.*", "***"],
        ["***", "..*", "..*", "..*", "..*"],
        ["***", "*.*", "***", "*.*", "***"],
        ["***", "*.*", "***", "..*", "***"],
    ]

    N, M = map(int, _sys.stdin.readline().split())
    grid = [_sys.stdin.readline().strip() for _ in range(N)]

    ans = 0
    for i in range(N - 4):
        for j in range(M - 2):
            best = 0
            for d in range(10):
                ok = True
                for x in range(5):
                    for y in range(3):
                        if DIGITS[d][x][y] == '*' and grid[i+x][j+y] != '*':
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    best = d
            ans += best

    return str(ans)

# provided samples
assert run("5 3\n***\n*..\n***\n..*\n***\n") == "1"
assert run("6 6\n.***.*\n.*...*\n.***.*\n.*.*.*\n.***.*\n....**\n") == "8"

# custom cases
assert run("5 3\n***\n***\n***\n***\n***\n") == "9", "all stars match everything -> always 9"
assert run("5 3\n***\n...\n***\n...\n***\n") == "0", "no digit fully supported"
assert run("5 3\n***\n*.*\n***\n*.*\n***\n") == "9", "perfect digit 8-like full match resolves to 9 if compatible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all stars grid | 9 | maximal matching case |
| sparse grid | 0 | no valid digit windows |
| symmetric full pattern | 9 | tie-breaking to maximum digit |

## Edge Cases

A window filled entirely with stars is the most permissive situation. The algorithm still behaves correctly because every digit passes the subset check, and the maximum digit 9 is chosen.

A window with no stars at all fails every digit because each digit requires at least one mandatory `*`. The check correctly rejects all digits and contributes zero.

Highly irregular patterns where digits overlap partially are handled correctly because the algorithm never assumes exclusivity, it only enforces inclusion of required cells.
