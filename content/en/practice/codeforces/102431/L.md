---
title: "CF 102431L - Spiral Matrix"
description: "We have an (n times m) rectangular grid of booths. Lee may choose any booth as the starting point and any of the four initial directions. After that, every move is either straight ahead or a single right turn followed by one step."
date: "2026-08-08T23:53:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102431
codeforces_index: "L"
codeforces_contest_name: "2019 China Collegiate Programming Contest Final (CCPC-Final 2019)"
rating: 0
weight: 102431
solve_time_s: 138
verified: true
draft: false
---

[CF 102431L - Spiral Matrix](https://codeforces.com/problemset/problem/102431/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times m) rectangular grid of booths. Lee may choose any booth as the starting point and any of the four initial directions. After that, every move is either straight ahead or a single right turn followed by one step. A left turn is never allowed, and a sequence of right turns is allowed only one turn at a time between consecutive visited cells.

The task is to count the distinct orders in which all (nm) cells can be visited exactly once. Two walks are considered different when their sequences of visited cells differ. The answer is required modulo (10^9+7). The official problem has (n,m\le100), up to 100 test cases, with a 1 second time limit and 256 MB memory limit.

The constraints are small enough that a linear or constant-time formula is easily fast enough, but they rule out anything exponential in the number of cells. A (100\times100) grid contains 10,000 cells, so even (O(nm)) per test case is only about 10,000 operations. In contrast, enumerating all possible walks would have an exponential search tree whose depth is 10,000, which is completely infeasible.

The main edge cases come from very thin rectangles. For a (1\times1) grid, there is exactly one visiting order because there is only one booth, so the answer is 1. A formula intended for ordinary rectangles would incorrectly give 0 here. For example,

```
1
1 1
```

produces

```
Case #1: 1
```

For a (1\times2) grid, there are exactly two visiting orders, one starting from either cell. The initial direction does not create extra orders when the first cell is fixed, because the only useful move is toward the other cell. Thus

```
1
1 2
```

produces

```
Case #1: 2
```

A second easy mistake is treating (1\times m) and (n\times1) as ordinary two-dimensional rectangles. For every one-dimensional grid with at least two cells, the answer is 2, not the expression used for both dimensions greater than one. For example, (1\times100) has only the left-to-right and right-to-left visiting orders.

## Approaches

The direct approach is to perform a depth-first search over all possible walks. We choose every possible starting cell and initial direction, mark the cell as visited, and repeatedly try going straight or turning right before moving one cell. Whenever the walk reaches all (nm) cells, we count it.

This search is correct because every legal visiting order corresponds to one branch of the search tree, and every branch is rejected as soon as it leaves the grid or revisits a cell. However, the search can have two choices at almost every step. With (N=nm) cells, a crude upper bound is (O(nm\cdot 2^{N})) work after accounting for the (O(nm)) possible starting states. For a (100\times100) grid, this means an upper bound on the order of (10^4\cdot2^{10000}) operations, which is not remotely usable.

The useful observation is that legal walks in a rectangular grid are extraordinarily constrained. Since Lee can never turn left, the direction of the walk can only stay unchanged or rotate clockwise. Once the walk turns, its new direction is fixed, and another turn can only continue that clockwise progression. A self-avoiding walk that visits every cell therefore cannot wander arbitrarily through the rectangle. To cover the entire rectangle, it has to trace its boundary in a spiral-like manner.

There are only (2(n+m)-4) such visiting orders when both dimensions exceed one. One way to understand the count is to examine where the walk can begin and how the outer boundary forces the rest of the path. Every valid full-grid walk is determined by choosing one of the boundary positions at which this spiral-like traversal starts, with the four corner cases identified appropriately. The resulting number is exactly

[
2(n+m)-4.
]

This characterization is also the standard compact solution for this problem.

The brute-force search works because it explicitly explores every legal path, but fails because the number of partial paths grows exponentially. The structural observation replaces the entire search with a constant-time calculation based only on the two side lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm\cdot2^{nm})) | (O(nm)) | Too slow |
| Optimal | (O(1)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (m), the number of rows and columns. The answer depends only on the dimensions, not on any contents of the cells, because every cell is structurally identical.
2. If (n=m=1), return 1. There is only one cell, so there is exactly one possible visiting order.
3. If exactly one dimension is 1, return 2. A nontrivial one-dimensional grid can only be traversed from one endpoint to the other, giving the two orientations.
4. If both dimensions are greater than 1, compute

[
2(n+m)-4.
]

The subtraction of 4 accounts for the four corners that would otherwise be counted twice when the possible spiral starts are associated with the four sides.
5. Print the result using the required `Case #x: y` format. The largest answer is only (396) for (100\times100), so the modulus never actually becomes relevant under the given constraints, although using integer arithmetic keeps the implementation compatible with the stated output requirement.

**Why it works.** Every legal walk has a direction that never rotates counterclockwise. A full traversal of a rectangle therefore has no freedom to create an arbitrary Hamiltonian path. Its turns are forced into the clockwise spiral structure of the rectangle. For a two-dimensional rectangle, the possible complete spirals are in one-to-one correspondence with the (2(n+m)-4) valid boundary choices. Thin rectangles collapse this structure into a line, where only the two traversal directions remain, and the single-cell case has only one order. These cases exhaust all possible values of (n) and (m).

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())

        if n == 1 and m == 1:
            ans = 1
        elif n == 1 or m == 1:
            ans = 2
        else:
            ans = 2 * (n + m) - 4

        ans %= MOD
        out.append(f"Case #{case}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop follows the test-case structure directly. For each rectangle, the first condition isolates the unique one-cell case before the one-dimensional case is checked.

The expression for a thin rectangle is deliberately separate from the general formula. Substituting (n=1) into (2(n+m)-4) would give (2m-2), which is wrong for every (m>2). The geometry changes completely when there is no second row.

For a genuine two-dimensional rectangle, the answer is computed directly as `2 * (n + m) - 4`. There is no simulation and no grid to allocate. The modulo operation is included because the statement requests the answer modulo (10^9+7), even though the formula itself stays below the modulus for the given bounds.

The code collects all output lines and writes them once. This is simple and avoids repeated output calls across as many as 100 test cases.

## Worked Examples

The statement provides one sample, (2\times2). Since there is no second sample, the second trace uses (2\times3), which exercises the general two-dimensional formula.

### Example 1: (2\times2)

| Step | (n) | (m) | Condition | Answer |
| --- | --- | --- | --- | --- |
| Read dimensions | 2 | 2 | Both dimensions are greater than 1 |  |
| Apply formula | 2 | 2 | (2(n+m)-4) | (2(2+2)-4=4) |
| Output | 2 | 2 | Final result | 4 |

The four visiting orders correspond to the four possible orientations of the (2\times2) traversal. This agrees with the provided sample, whose output is `Case #1: 4`.

### Example 2: (2\times3)

| Step | (n) | (m) | Condition | Answer |
| --- | --- | --- | --- | --- |
| Read dimensions | 2 | 3 | Both dimensions are greater than 1 |  |
| Apply formula | 2 | 3 | (2(n+m)-4) | (2(2+3)-4=6) |
| Output | 2 | 3 | Final result | 6 |

The important part of this trace is that increasing the rectangle from (2\times2) to (2\times3) adds two possible complete traversals. The formula depends only on the perimeter dimensions, not on an explicit simulation of the six cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T)) | Each test case requires a constant number of arithmetic operations. |
| Space | (O(T)) | The output strings for all test cases are stored before being written. The algorithm itself uses (O(1)) extra space per case. |

With at most 100 test cases and dimensions no larger than 100, this is far below the available 1 second and 256 MB limits. The implementation does not allocate a (100\times100) grid, perform a search, or maintain any per-cell state.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m = map(int, input().split())

        if n == 1 and m == 1:
            ans = 1
        elif n == 1 or m == 1:
            ans = 2
        else:
            ans = 2 * (n + m) - 4

        ans %= 10**9 + 7
        out.append(f"Case #{case}: {ans}")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    "1\n2 2\n"
) == "Case #1: 4", "provided sample"

# Minimum-size input
assert run(
    "1\n1 1\n"
) == "Case #1: 1", "single cell"

# One-dimensional boundary case
assert run(
    "1\n1 2\n"
) == "Case #1: 2", "one row"

# Transposed one-dimensional case
assert run(
    "1\n5 1\n"
) == "Case #1: 2", "one column"

# Small two-dimensional rectangle
assert run(
    "1\n2 3\n"
) == "Case #1: 6", "2 by 3 rectangle"

# Equal maximum dimensions
assert run(
    "1\n100 100\n"
) == "Case #1: 396", "maximum equal dimensions"

# Multiple test cases together
assert run(
    "4\n1 1\n1 100\n100 1\n3 4\n"
) == (
    "Case #1: 1\n"
    "Case #2: 2\n"
    "Case #3: 2\n"
    "Case #4: 10"
), "mixed boundary cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Unique single-cell traversal |
| `1 2` | `2` | Smallest nontrivial one-row grid |
| `5 1` | `2` | One-column case and symmetry |
| `2 3` | `6` | General two-dimensional formula |
| `100 100` | `396` | Maximum dimensions and equal sides |
| `1 1`, `1 100`, `100 1`, `3 4` | `1, 2, 2, 10` | Multiple cases and boundary handling |

## Edge Cases

For a (1\times1) grid, the algorithm immediately takes the first branch. There is no movement at all, so the only visiting sequence consists of the single cell. The exact input

```
1
1 1
```

produces `Case #1: 1`. This catches implementations that blindly apply the two-dimensional formula and obtain zero.

For a (1\times100) grid, the second branch applies because one dimension is one. Lee cannot create a two-dimensional spiral because there is no second row. He can only visit the cells from left to right or from right to left, so the answer is exactly 2:

```
1
1 100
```

produces

```
Case #1: 2
```

The same reasoning applies after transposing the grid. For (100\times1), the answer is also 2. This symmetry is useful for catching code that treats rows and columns differently even though the geometry is unchanged by rotation.

For the smallest genuine rectangle, (2\times2), the general branch gives

[
2(2+2)-4=4.
]

Thus

```
1
2 2
```

produces

```
Case #1: 4
```

which is the official sample.

Finally, for the maximum (100\times100) grid, the same constant-time formula gives

[
2(100+100)-4=396.
]

The algorithm does not become slower as the grid grows because it never constructs or traverses the grid. This is exactly the structural advantage over the brute-force search.
