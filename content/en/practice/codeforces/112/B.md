---
title: "CF 112B - Petya and Square"
description: "We have a square board of size 2n × 2n, divided into unit cells. One cell is marked. We want to know whether it is possible to draw a cutting path along grid lines so that the board is split into two congruent parts after rotation, while the cutting path never touches the marked…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 112
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 85 (Div. 2 Only)"
rating: 1200
weight: 112
solve_time_s: 102
verified: true
draft: false
---

[CF 112B - Petya and Square](https://codeforces.com/problemset/problem/112/B)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a square board of size `2n × 2n`, divided into unit cells. One cell is marked. We want to know whether it is possible to draw a cutting path along grid lines so that the board is split into two congruent parts after rotation, while the cutting path never touches the marked cell.

The key detail is that the two resulting pieces must become identical after a rotation. For a square with even side length, the natural rotational symmetry is centered in the middle of the board.

The input gives the side length `2n` and the coordinates `(x, y)` of the marked cell. Rows and columns are 1-indexed. We must print `"YES"` if such a cut exists, otherwise `"NO"`.

The constraints are tiny, the side length is at most 100, so performance is not the challenge here. The difficulty is recognizing the geometric observation hidden in the statement. A brute-force geometric construction would be unnecessary and error-prone.

The non-obvious part is understanding which cells are unavoidable for every valid symmetric cut.

Consider the smallest interesting case:

```
4 2 2
```

The square is `4 × 4`. The central area consists of four cells:

```
(2,2) (2,3)
(3,2) (3,3)
```

If the marked cell is one of these four cells, the answer is `"NO"`.

Why? Any valid cut that splits the square into two rotationally equivalent halves must pass through the exact center of the board. In an even-sized grid, the center lies at the intersection of those four cells, so every possible symmetric dividing path touches that central `2 × 2` block.

A careless solution might check only the exact center point and forget that an even-sized grid has four central cells rather than one.

Another easy mistake is using zero-based reasoning with one-based coordinates. For a `6 × 6` board, the central cells are:

```
(3,3) (3,4)
(4,3) (4,4)
```

not `(2,2)` and `(3,3)`.

For example:

```
6 3 4
```

must produce `"NO"` because `(3,4)` is inside the central block.

But:

```
6 2 4
```

produces `"YES"` because the marked cell is outside that unavoidable region.

## Approaches

A brute-force interpretation would try to explicitly construct every possible cutting line along grid edges, verify that it splits the board into equal rotationally congruent regions, and check whether the path touches the marked cell.

Even for a `100 × 100` board, the number of possible lattice paths is enormous. The search space grows exponentially because at every grid intersection the path may branch in several directions. This approach becomes infeasible almost immediately.

The reason brute force feels natural is that the statement talks about geometric cuts rather than simple arithmetic conditions. But the geometry here is extremely rigid.

The crucial observation is that every valid partition must respect 180-degree rotational symmetry around the center of the square. If the side length is even, the center lies between four cells. Any symmetric dividing path must pass through that central region.

That means the only cells that can never be avoided are the four middle cells:

```
(n,n)
(n,n+1)
(n+1,n)
(n+1,n+1)
```

If the marked cell is one of them, every valid cut intersects it, so the answer is `"NO"`.

For every other cell, a suitable symmetric cut can be drawn that avoids the marked position, so the answer is `"YES"`.

The entire problem reduces to checking whether `(x, y)` belongs to the central `2 × 2` block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the side length `2n` and the cell coordinates `(x, y)`.
2. Compute `n = side_length // 2`.

The four unavoidable central cells are determined entirely by this value.
3. Check whether the marked cell lies inside the central `2 × 2` block.

This happens exactly when:

```
x is either n or n+1
and
y is either n or n+1
```
4. If both conditions hold, print `"NO"`.

Every symmetric cut must pass through this region.
5. Otherwise, print `"YES"`.

Outside the center block, there exists a valid symmetric partition avoiding the marked cell.

### Why it works

A valid cut divides the square into two parts that become identical after rotation. Such symmetry forces the dividing path to pass through the geometric center of the square.

Because the side length is even, the geometric center lies between four cells. Any path through the center necessarily touches the central `2 × 2` block. Those four cells are unavoidable.

Every other cell can be avoided by choosing an appropriate symmetric cut. So the answer is `"NO"` exactly for the four central cells, and `"YES"` everywhere else.

## Python Solution

```python
import sys
input = sys.stdin.readline

side, x, y = map(int, input().split())

n = side // 2

if (x == n or x == n + 1) and (y == n or y == n + 1):
    print("NO")
else:
    print("YES")
```

The implementation follows the mathematical observation directly.

First we compute `n`, which identifies the middle of the board. Since the side length is always even, the center consists of four cells rather than one.

The condition:

```
(x == n or x == n + 1)
```

checks whether the row belongs to the central pair of rows. The same logic applies to columns.

Both conditions must hold simultaneously for the marked cell to be inside the central `2 × 2` block.

A common off-by-one mistake is forgetting that the grid uses one-based indexing. For a `4 × 4` board, the central rows are `2` and `3`, not `1` and `2`.

The solution uses constant time and constant memory.

## Worked Examples

### Example 1

Input:

```
4 1 1
```

| Variable | Value |
| --- | --- |
| side | 4 |
| n | 2 |
| x | 1 |
| y | 1 |

Central cells are:

```
(2,2) (2,3)
(3,2) (3,3)
```

The marked cell `(1,1)` is outside this region, so the answer is:

```
YES
```

This example demonstrates that almost all cells are valid. Only the center block is forbidden.

### Example 2

Input:

```
6 3 4
```

| Variable | Value |
| --- | --- |
| side | 6 |
| n | 3 |
| x | 3 |
| y | 4 |

Central cells are:

```
(3,3) (3,4)
(4,3) (4,4)
```

The marked cell `(3,4)` belongs to the center block, so the answer is:

```
NO
```

This trace confirms the exact boundary of the forbidden region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, but this solution is optimal anyway. It performs a constant amount of work regardless of board size and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    side, x, y = map(int, input().split())

    n = side // 2

    if (x == n or x == n + 1) and (y == n or y == n + 1):
        print("NO")
    else:
        print("YES")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("4 1 1\n") == "YES", "sample 1"

# minimum valid size, central cell
assert run("2 1 1\n") == "NO", "minimum size central cell"

# minimum valid size, another central cell
assert run("2 2 2\n") == "NO", "all cells are central in 2x2"

# outside center block
assert run("6 2 4\n") == "YES", "outside forbidden region"

# exact center boundary
assert run("6 3 4\n") == "NO", "central block detection"

# maximum size edge position
assert run("100 1 100\n") == "YES", "large board edge cell"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | `NO` | Smallest board, every cell is central |
| `2 2 2` | `NO` | Confirms all four cells are forbidden in `2 × 2` |
| `6 2 4` | `YES` | Cell adjacent to center but still valid |
| `6 3 4` | `NO` | Correct identification of central block |
| `100 1 100` | `YES` | Large boundary coordinates |

## Edge Cases

Consider the smallest possible board:

```
2 1 1
```

Here `n = 1`, so the central block is:

```
(1,1) (1,2)
(2,1) (2,2)
```

The marked cell belongs to this block, so the algorithm prints `"NO"`.

This case is easy to mishandle if the implementation assumes there is only one central cell.

Now consider:

```
6 2 3
```

We compute:

```
n = 3
```

The forbidden cells are:

```
(3,3) (3,4)
(4,3) (4,4)
```

The marked cell `(2,3)` is directly above the center block but not inside it. The algorithm correctly prints `"YES"`.

This catches off-by-one mistakes where programmers accidentally expand the forbidden region beyond the true `2 × 2` center.

Finally, consider:

```
100 50 51
```

Here:

```
n = 50
```

The central cells are:

```
(50,50) (50,51)
(51,50) (51,51)
```

The marked cell `(50,51)` lies inside the block, so the algorithm prints `"NO"`.

This verifies that the logic scales correctly to the largest input size without any special handling.
