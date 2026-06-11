---
title: "CF 1345A - Puzzle Pieces"
description: "We are asked to determine whether a grid of jigsaw pieces can be assembled given a special piece design. Each piece has exactly three tabs and one blank. The pieces can be rotated in any orientation."
date: "2026-06-11T15:02:28+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1345
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 639 (Div. 2)"
rating: 800
weight: 1345
solve_time_s: 108
verified: true
draft: false
---

[CF 1345A - Puzzle Pieces](https://codeforces.com/problemset/problem/1345/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a grid of jigsaw pieces can be assembled given a special piece design. Each piece has exactly three tabs and one blank. The pieces can be rotated in any orientation. A solution exists if we can fill an $n \times m$ grid such that every tab fits into a blank along shared edges.

The input consists of multiple test cases. Each test case provides two integers, $n$ and $m$, specifying the number of rows and columns in the grid. The output should be "YES" if the puzzle can be solved under these conditions and "NO" otherwise.

Given the constraints $1 \le n,m \le 10^5$ and up to $1000$ test cases, we cannot simulate the puzzle or attempt to place each piece individually. Any brute-force algorithm that manipulates each cell would require $O(n \cdot m)$ operations, which could reach $10^{10}$ in the worst case. This exceeds practical time limits, so we need a mathematical or combinatorial approach.

Non-obvious edge cases arise when the grid is very narrow or very small. For example, a $1 \times m$ or $n \times 1$ grid behaves differently than a larger grid because pieces at the edges do not require all sides to match. Specifically, a $1 \times 3$ grid is solvable, whereas a $100000 \times 100000$ grid is not, despite both being rectangular, because the internal constraints cannot be satisfied with only one blank per piece. A careless approach that ignores parity or internal connectivity would incorrectly output "YES" for large square grids.

## Approaches

The brute-force approach is to try to place pieces in all orientations and check each adjacent pair for matching tabs and blanks. This is correct for small grids, but the operation count is $O(n \cdot m)$ per test case. With the maximum limits, this would require $10^{10}$ operations, which is infeasible for the time limit.

The key insight comes from observing the pieces' structure. Each piece has one blank and three tabs. In any grid larger than $2 \times 2$, some pieces will necessarily have more than one neighbor on different sides, creating conflicts. For example, a piece in a square grid with four neighbors would need four blanks to match, but it only has one. Therefore, the only solvable grids are either one-dimensional (a single row or column) or a $2 \times 2$ square where each piece can satisfy all neighbors.

The problem reduces to a simple check: if the grid is a single row or a single column, it is always solvable because each piece needs to match only one neighbor along the row or column. If both dimensions are even and equal to two, a $2 \times 2$ square is solvable. All other configurations are impossible because at least one piece will have more neighbors than blanks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Too slow |
| Mathematical/Observation | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read integers $n$ and $m$.
3. If either $n = 1$ or $m = 1$, print "YES" because a single row or column can always be assembled.
4. Else if $n = 2$ and $m = 2$, print "YES" because the $2 \times 2$ grid allows each piece to match all neighbors.
5. Otherwise, print "NO" because no configuration satisfies the internal tab-to-blank constraints.

The correctness comes from the invariant that each piece has exactly one blank. Any piece with more than one neighbor requires more blanks than available. Only single rows, single columns, and the $2 \times 2$ square respect this invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if n == 1 or m == 1:
        print("YES")
    elif n == 2 and m == 2:
        print("YES")
    else:
        print("NO")
```

The solution reads all test cases efficiently using fast input. The conditional checks directly implement the mathematical observation derived above. Using `or` allows for any one-dimensional grid, and the equality check handles the $2 \times 2$ edge case. All other inputs are rejected in constant time.

## Worked Examples

For input:

```
3
1 3
100000 100000
2 2
```

| Step | n | m | Condition matched | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | n=1 | YES |
| 2 | 100000 | 100000 | none | NO |
| 3 | 2 | 2 | n=2 & m=2 | YES |

The first row demonstrates a single-row grid, which is solvable. The second row is a large square grid, which fails because internal pieces cannot satisfy the tab-blank requirement. The third row is a $2 \times 2$ grid, which works as expected.

Another input:

```
2
1 1
2 3
```

| Step | n | m | Condition matched | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | n=1 | YES |
| 2 | 2 | 3 | none | NO |

The single piece case confirms that trivial grids are accepted. The $2 \times 3$ rectangle fails because internal pieces cannot match more than one neighbor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires only a few constant-time checks. |
| Space | O(1) | No extra storage proportional to n or m is required. |

Given $t \le 1000$ and $n, m \le 10^5$, the solution runs in under $10^3$ operations per test case and fits comfortably within the memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        if n == 1 or m == 1:
            print("YES")
        elif n == 2 and m == 2:
            print("YES")
        else:
            print("NO")
    return out.getvalue().strip()

# Provided samples
assert run("3\n1 3\n100000 100000\n2 2\n") == "YES\nNO\nYES", "sample 1"

# Custom cases
assert run("2\n1 1\n2 3\n") == "YES\nNO", "single piece and rectangle"
assert run("2\n1 100000\n100000 1\n") == "YES\nYES", "extreme single row/column"
assert run("1\n2 2\n") == "YES", "minimum 2x2"
assert run("1\n3 2\n") == "NO", "non-square small rectangle"
assert run("1\n100000 100000\n") == "NO", "maximum size square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | YES | Single piece grid |
| 2 3 | NO | Rectangle where internal pieces cannot match |
| 1 100000 | YES | Single row, maximum width |
| 100000 1 | YES | Single column, maximum height |
| 2 2 | YES | Minimum solvable square |
| 3 2 | NO | Small rectangle, impossible |
| 100000 100000 | NO | Maximum square grid |

## Edge Cases

The smallest grid, $1 \times 1$, is handled by the `n == 1` condition and outputs "YES". For a narrow but long grid like $1 \times 100000$, the algorithm still outputs "YES" because each piece has only one neighbor. The $2 \times 2$ square triggers the second condition. Large squares like $100000 \times 100000$ fail because the invariant of one blank per piece cannot satisfy the internal neighbors. Each edge case is directly matched by one of the conditional checks, guaranteeing correctness.
