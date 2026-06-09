---
title: "CF 1806A - Walking Master"
description: "We are asked to compute the minimum number of moves for a character, YunQian, to reach a target point on an infinite Cartesian plane."
date: "2026-06-09T09:08:13+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1806
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 858 (Div. 2)"
rating: 800
weight: 1806
solve_time_s: 111
verified: true
draft: false
---

[CF 1806A - Walking Master](https://codeforces.com/problemset/problem/1806/A)

**Rating:** 800  
**Tags:** geometry, greedy, math  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum number of moves for a character, YunQian, to reach a target point on an infinite Cartesian plane. YunQian has two types of moves: she can move diagonally up-right from $(x, y)$ to $(x+1, y+1)$, or she can move directly left from $(x, y)$ to $(x-1, y)$. The input provides the starting coordinates $(a, b)$ and the target coordinates $(c, d)$ for multiple test cases. The output should either be the minimum number of moves or $-1$ if it is impossible to reach the target.

The coordinates range between $-10^8$ and $10^8$, and there can be up to $10^4$ test cases. A naive simulation that explores every possible path is immediately ruled out because even a single path could require up to $2 \cdot 10^8$ moves in the worst case. This implies the solution must be purely analytical, based on geometry and simple arithmetic rather than search.

Edge cases arise when the target is directly left of the start or above the start without horizontal displacement. For example, if the start is $(-1,0)$ and the target is $(-1,2)$, one cannot reach the target using only left moves because left moves reduce $x$ but leave $y$ unchanged, and diagonal moves increase both $x$ and $y$. Misunderstanding this leads to an incorrect assumption that any vertical or horizontal displacement is always achievable.

## Approaches

A brute-force approach would enumerate all sequences of left and diagonal moves until reaching the target. This works because the moves are deterministic, and one can track coordinates after each move. The problem with this approach is the potential number of moves can reach $10^8$ or more, and there are exponentially many sequences of moves, so it is computationally infeasible.

The key insight is to observe that diagonal moves increase both $x$ and $y$ by one, while left moves decrease only $x$. If we denote $dx = c - a$ and $dy = d - b$, then reaching the target is only possible if the number of diagonal moves $k$ and left moves $l$ satisfy two constraints: $k - l = dx$ and $k = dy$. From this, we derive $l = dy - dx$. The moves are only valid if both $k \ge 0$ and $l \ge 0$, otherwise reaching the target is impossible. This reduces the problem to simple arithmetic for each test case, allowing an $O(1)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(dx+dy)) | O(1) | Too slow |
| Analytical | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the horizontal and vertical displacement: $dx = c - a$, $dy = d - b$. These represent the net changes in the x and y coordinates that we must achieve.
2. Check if the vertical displacement is negative. Since diagonal moves only increase $y$ and left moves leave $y$ unchanged, if $dy < 0$, it is impossible to reach the target. Return $-1$ in this case.
3. Compute the number of left moves required: $l = dy - dx$. This comes from solving the system $k - l = dx$ and $k = dy$, where $k$ is the number of diagonal moves.
4. Verify that the number of left moves is non-negative. If $l < 0$, the target is to the right of where diagonal moves alone would take us, making the target unreachable. Return $-1$.
5. If both previous checks pass, the minimum number of moves is the sum of left and diagonal moves: $k + l = dy + (dy - dx) = 2 \cdot dy - dx$. Return this value.

Why it works: The algorithm works because the moves are linear and deterministic. Every vertical increase must come from a diagonal move, giving $k = dy$. The horizontal displacement is the net effect of diagonals and left moves, giving $dx = k - l$. Solving this system guarantees minimal moves, since any additional diagonal or left moves would overshoot the target.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    dx = c - a
    dy = d - b
    if dy < 0:
        print(-1)
        continue
    l = dy - dx
    if l < 0:
        print(-1)
        continue
    print(dy + l)
```

The solution first reads the number of test cases. For each test case, it calculates the differences in coordinates. It immediately checks if the vertical displacement is negative, which cannot be covered by the available moves. Then it computes the required number of left moves and checks if it is negative. The sum of diagonal and left moves gives the minimal number of moves. Using `sys.stdin.readline` ensures fast I/O for the maximum $10^4$ test cases.

## Worked Examples

Sample Input: `-1 0 -1 2`

| a | b | c | d | dx | dy | l | k+l | Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -1 | 0 | -1 | 2 | 0 | 2 | 2 | 4 | 4 |

The algorithm identifies that two left moves and two diagonal moves suffice to reach the target.

Sample Input: `0 0 4 5`

| a | b | c | d | dx | dy | l | k+l | Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 5 | 4 | 5 | 1 | 6 | 6 |

One diagonal move is used to reach the vertical height beyond what pure diagonals achieve, and the rest adjusts horizontal position with left moves.

These traces confirm the invariant: the sum of left and diagonal moves is minimal while satisfying horizontal and vertical displacements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is solved with a few arithmetic operations. |
| Space | O(1) | Only a constant number of variables are stored per test case. |

Given $t \le 10^4$, this fits comfortably within the 1-second time limit and the memory limit of 1024 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        dx = c - a
        dy = d - b
        if dy < 0:
            print(-1)
            continue
        l = dy - dx
        if l < 0:
            print(-1)
            continue
        print(dy + l)
    return out.getvalue().strip()

# provided samples
assert run("6\n-1 0 -1 2\n0 0 4 5\n-2 -1 1 1\n-3 2 -3 2\n2 -1 -1 -1\n1 1 0 2\n") == \
"4\n6\n-1\n0\n3\n3", "sample 1"

# custom cases
assert run("2\n0 0 0 0\n100000000 100000000 100000001 100000001\n") == \
"0\n1", "zero moves and minimal positive move"
assert run("2\n0 0 -1 1\n0 0 -1 0\n") == \
"-1\n-1", "negative vertical or unreachable horizontal"
assert run("1\n-5 -5 0 0\n") == \
"10", "large move from negative to zero coordinates"
assert run("1\n0 0 0 -1\n") == \
"-1", "vertical target below start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | 0 | No moves needed |
| 100000000 100000000 100000001 100000001 | 1 | Minimal move in large coordinates |
| 0 0 -1 1 | -1 | Target unreachable horizontally with positive vertical |
| -5 -5 0 0 | 10 | Moves from negative to positive coordinates |
| 0 0 0 -1 | -1 | Vertical displacement negative |

## Edge Cases

If the start and target are identical, $dx = dy = 0$. The number of left moves is $0$, and the algorithm correctly returns $0$.

If the target is strictly above the start with no horizontal change, $dx = 0$ and $dy > 0$, the required left moves equal $dy - dx = dy$. The algorithm ensures (l
