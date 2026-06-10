---
title: "CF 1426B - Symmetric Matrix"
description: "We are asked to determine whether it is possible to tile an (m times m) square using (2 times 2) tiles so that the resulting square is symmetric with respect to its main diagonal. Each tile has fixed numbers in its four cells, and rotations are not allowed."
date: "2026-06-11T05:47:31+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1426
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 674 (Div. 3)"
rating: 900
weight: 1426
solve_time_s: 224
verified: true
draft: false
---

[CF 1426B - Symmetric Matrix](https://codeforces.com/problemset/problem/1426/B)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 3m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether it is possible to tile an \(m \times m\) square using \(2 \times 2\) tiles so that the resulting square is symmetric with respect to its main diagonal. Each tile has fixed numbers in its four cells, and rotations are not allowed. We have an infinite number of each tile type. Symmetry here means that for every pair of positions \((i, j)\) and \((j, i)\), the values must match.

The input gives us \(t\) test cases. Each test case specifies the number of tile types \(n\) and the square size \(m\), followed by the definitions of the tiles in order. Each tile is given in two lines, representing the top and bottom rows. The output for each test case is simply "YES" if the square can be tiled symmetrically, and "NO" otherwise.

Looking at the constraints, \(n\) and \(m\) are both at most 100, and there are at most 100 test cases. This immediately suggests that any solution with time complexity \(O(n \cdot m)\) per test case is feasible. The main subtlety is that the symmetry requirement combined with tiling means that not all tile combinations are valid. In particular, since tiles cannot be rotated, only tiles where the left and right diagonal cells can align with their mirrored positions will be useful for constructing the symmetric square.

Edge cases that a naive approach might miss include when \(m\) is odd. If \(m\) is odd, a symmetric tiling with \(2 \times 2\) tiles is impossible because the center row and column would require a single-cell width that cannot be covered by a \(2 \times 2\) tile. Another subtlety is that we do not need to use all tiles; we only need to find one suitable tile whose off-diagonal cells can pair with themselves or another tile to preserve symmetry.

## Approaches

A brute-force approach would try to place every tile in every position in the \(m \times m\) grid and check for symmetry. For an \(m \times m\) square, there are roughly \((m/2)^2\) placements of \(2 \times 2\) tiles. With \(n\) tiles, this leads to \(O(n \cdot (m/2)^2)\) operations, which is feasible in this problem's constraints, but constructing the entire matrix and checking symmetry is unnecessary. The insight is that we do not need to simulate the entire grid. The only thing that matters is:

1. \(m\) must be even.
2. There must exist at least one tile where the top-right value equals the bottom-left value. This ensures that the tiles can meet along the diagonal and preserve symmetry.

This observation reduces the problem to checking the parity of \(m\) and scanning the tiles for a matching pair of diagonal-adjacent cells. If \(m\) is odd, no symmetric tiling is possible. If \(m\) is even, we simply need to find at least one tile with the off-diagonal symmetry property.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force (simulate tiling) | O(n * m²) | O(m²) | Accepted but unnecessary |
| Optimal (parity + tile check) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases \(t\). Iterate through each test case.
2. For each test case, read the number of tile types \(n\) and the desired square size \(m\).
3. Initialize a flag `found` as False. This flag will indicate whether a suitable tile exists.
4. For each tile, read the four integers \(a, b, c, d\) representing the top-left, top-right, bottom-left, and bottom-right numbers respectively.
5. Check if \(b = c\). This condition ensures that the tile can contribute to a symmetric tiling along the diagonal.
6. If any tile satisfies this condition, set `found` to True.
7. After scanning all tiles, if `m` is odd, output "NO" because a \(2 \times 2\) tiling cannot cover an odd-dimension square symmetrically.
8. If `m` is even and `found` is True, output "YES"; otherwise output "NO".

Why it works: the symmetry of the matrix reduces the problem to ensuring that the tiles' off-diagonal cells can meet along the diagonal, and the square size must be divisible by 2 to accommodate full \(2 \times 2\) tiles. This invariant guarantees correctness without constructing the entire matrix.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    found = False
    for _ in range(n):
        a, b = map(int, input().split())
        c, d = map(int, input().split())
        if b == c:
            found = True
    if m % 2 != 0:
        print("NO")
    else:
        print("YES" if found else "NO")
```

The solution reads input efficiently using `sys.stdin.readline`. We keep a simple flag to detect a suitable tile. The check `m % 2 != 0` immediately handles the impossible odd-length squares. We do not store tiles unnecessarily, keeping space usage minimal.

## Worked Examples

### Sample 1

Input:  

```
3 4
1 2
5 6
5 7
7 4
8 9
9 8
```

Processing:

| Tile | a | b | c | d | b==c |
|---|---|---|---|---|---|
| 1 | 1 | 2 | 5 | 6 | False |
| 2 | 5 | 7 | 7 | 4 | True |
| 3 | 8 | 9 | 9 | 8 | True |

`m = 4` (even), at least one tile has `b == c`, so output "YES".

### Odd size example

Input:  

```
1 3
1 2
2 1
```

`m = 3` (odd), output "NO" immediately, regardless of tile contents.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(t * n) | We check each tile once per test case |
| Space | O(1) | Only a single boolean flag is needed |

The solution easily fits within the 1-second limit for up to 100 test cases and 100 tiles per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        found = False
        for _ in range(n):
            a, b = map(int, input().split())
            c, d = map(int, input().split())
            if b == c:
                found = True
        if m % 2 != 0:
            print("NO")
        else:
            print("YES" if found else "NO")
    return output.getvalue().strip()

# provided samples
assert run("6\n3 4\n1 2\n5 6\n5 7\n7 4\n8 9\n9 8\n2 5\n1 1\n1 1\n2 2\n2 2\n1 100\n10 10\n10 10\n1 2\n4 5\n8 4\n2 2\n1 1\n1 1\n1 2\n3 4\n1 2\n1 1\n1 1") == "YES\nNO\nYES\nNO\nYES\nYES", "sample 1"

# custom cases
assert run("1\n1 2\n1 2\n2 3") == "YES", "single tile matching"
assert run("1\n1 2\n1 2\n3 4") == "NO", "single tile non-matching"
assert run("1\n2 3\n1 2\n2 1\n3 4\n4 3") == "NO", "odd square size"
assert run("1\n2 4\n1 2\n2 1\n3 4\n4 3") == "YES", "even square size, multiple tiles"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1 2\n1 2\n2 3 | YES | Single tile with `b==c` works |
| 1 2\n1 2\n3 4 | NO | Single tile without `b==c` fails |
| 2 3\n1 2\n2 1\n3 4\n4 3 | NO | Odd `m` cannot be tiled |
| 2 4\n1 2\n2 1\n3 4\n4 3 | YES | Even `m` with matching tile succeeds |

## Edge Cases

An important edge case occurs when the square size \(m\) is odd. For example, with input:

```
1
1 3
1 2
2 1
```

The algorithm first checks `m % 2 !=
