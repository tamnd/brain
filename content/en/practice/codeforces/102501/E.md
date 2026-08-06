---
title: "CF 102501E - Pixels"
description: "We have a rectangular binary grid. A cell is either black or white, and we need to choose a set of cells whose switches are pressed. Pressing one switch toggles that cell and its four orthogonal neighbours."
date: "2026-08-06T18:55:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 60
verified: true
draft: false
---

[CF 102501E - Pixels](https://codeforces.com/problemset/problem/102501/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular binary grid. A cell is either black or white, and we need to choose a set of cells whose switches are pressed. Pressing one switch toggles that cell and its four orthogonal neighbours. The task is to output one valid set of pressed switches or prove that no such set exists.

The input gives the desired final state of every cell. The output is another grid of the same size, where `P` means that the corresponding switch is pressed and `A` means it is not pressed.

The total number of cells is at most 100000. A general Gaussian elimination over all cells would require a matrix with 100000 variables, which is far beyond what can be handled. The solution needs to exploit the rectangular structure instead of treating every cell as an unrelated variable. The important observation is that the smaller side of the rectangle is at most about 316 when the area is bounded by 100000, so a linear system on the smaller dimension is feasible.

There are several small cases where a careless solution fails. For a single row, pressing a cell affects only its neighbours in that row, so the vertical reasoning used for larger grids must still work. For example:

```
1 2
B W
```

The two cells always change together when either switch is pressed, so the answer is `IMPOSSIBLE`.

A second trap is forgetting that the first or last row has fewer neighbours. For example:

```
2 1
B
B
```

Pressing the top switch toggles both cells, so pressing the top cell produces the required result. A solution that assumes every cell has four neighbours would build the wrong equations.

## Approaches

A direct approach is to view every cell as a variable and build a linear system over GF(2). Each variable says whether a switch is pressed. Each equation describes whether a final cell should be black or white. This is correct because toggling is equivalent to addition modulo two. However, the matrix would contain up to 100000 variables, making ordinary elimination too slow. The worst case would need roughly 10 15 bit operations.

The grid structure gives a better route. If we decide which switches are pressed in one row, all following rows can be forced. This is the classic chasing technique used in Lights Out problems. The only unknown part becomes the first row. Since we can transpose the grid, the number of columns can always be made the smaller dimension. The first row then contains at most 316 variables.

The remaining problem is a small linear system. We simulate the chase once with each possible basis vector of the first row to learn how every first-row variable affects the final row. Then Gaussian elimination finds the required first row presses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2 min(K,L) ) | O(KL) | Too slow |
| Optimal | O(KL⋅min(K,L)) | O(KL) | Accepted |

## Algorithm Walkthrough

1. If the number of rows is larger than the number of columns, transpose the grid. This keeps the first row small, which is the only part that will be solved by Gaussian elimination.
2. Represent every row as a bit mask. The target grid is converted into a binary matrix where `1` means black.
3. Define a chase function. Given the first row of presses, every next row is determined because row `i` must be fixed by choosing row `i + 1`. The formula is:

x i+1 ​ =d i ​ ⊕T(x i ​ )⊕x i−1 ​

where T toggles a row together with its left and right neighbours.

1. Run the chase with an empty first row. The remaining difference in the last row becomes the constant part of the final equation.
2. Run the chase once for every single bit in the first row. The resulting last-row differences form the columns of a linear system.
3. Solve the linear system with Gaussian elimination over GF(2). If a contradiction appears, the picture cannot be created.
4. Use the solved first row, run the chase one final time, and output the presses. If the grid was transposed, transpose the answer back.

The invariant behind the chase is that after processing row `i`, all rows above it are already correct and will never change again. Every possible solution must have some first row of presses, and the chase generates exactly the solution determined by that first row. The final linear system checks which first row makes the last row correct, so a found solution is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def toggle_row(x, m):
    return x ^ ((x << 1) & ((1 << m) - 1)) ^ (x >> 1)

def chase(first, target, n, m):
    press = [0] * n
    press[0] = first
    for i in range(n - 1):
        cur = target[i] ^ press[i - 1] if i else target[i]
        press[i + 1] = cur ^ toggle_row(press[i], m)
    return press

def solve_system(cols, rhs, n):
    rows = []
    for i in range(n):
        mask = 0
        for j in range(n):
            if (cols[j] >> i) & 1:
                mask |= 1 << j
        if (rhs >> i) & 1:
            mask |= 1 << n
        rows.append(mask)

    pivot = 0
    where = [-1] * n
    for col in range(n):
        found = -1
        for r in range(pivot, n):
            if (rows[r] >> col) & 1:
                found = r
                break
        if found == -1:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        where[col] = pivot
        for r in range(n):
            if r != pivot and ((rows[r] >> col) & 1):
                rows[r] ^= rows[pivot]
        pivot += 1

    for r in range(n):
        if rows[r] == (1 << n):
            return None

    ans = 0
    for i in range(n):
        if where[i] != -1 and ((rows[where[i]] >> n) & 1):
            ans |= 1 << i
    return ans

def main():
    k, l = map(int, input().split())
    a = [[1 if x == 'B' else 0 for x in input().split()] for _ in range(k)]

    transposed = False
    if k < l:
        a = [list(x) for x in zip(*a)]
        k, l = l, k
        transposed = True

    target = []
    for row in a:
        mask = 0
        for j, x in enumerate(row):
            if x:
                mask |= 1 << j
        target.append(mask)

    base = chase(0, target, k, l)
    rhs = target[-1] ^ (base[-2] if k > 1 else 0) ^ toggle_row(base[-1], l)

    cols = []
    for i in range(l):
        cur = chase(1 << i, target, k, l)
        cols.append(toggle_row(cur[-1], l) ^ (cur[-2] if k > 1 else 0) ^ rhs)

    first = solve_system(cols, rhs, l)
    if first is None:
        print("IMPOSSIBLE")
        return

    ans = chase(first, target, k, l)
    out = [['P' if (ans[i] >> j) & 1 else 'A' for j in range(l)] for i in range(k)]

    if transposed:
        out = [list(x) for x in zip(*out)]

    print('\n'.join(' '.join(row) for row in out))

if __name__ == "__main__":
    main()
```

The implementation stores every row as an integer bit mask. This makes the horizontal neighbour operation a few bit operations instead of iterating over cells. The chase function follows the same invariant described above: once a row is passed, it is fixed permanently.

The Gaussian elimination uses integers as bitsets. The extra highest bit in each row stores the right-hand side, so XORing rows performs elimination over GF(2). The transpose step is essential because it keeps the number of variables in the final system small.

## Worked Examples

For the first sample:

| Step | First row choice | Last row requirement | Result |
| --- | --- | --- | --- |
| Initial | no presses chosen | Two cells must become different | Impossible |
| Elimination | no consistent assignment exists | Contradiction found | `IMPOSSIBLE` |

The contradiction appears because both cells are always toggled together, so the target state cannot be separated.

For a small valid example:

```
2 1
B
B
```

| Step | Current row presses | Next row presses | State |
| --- | --- | --- | --- |
| Start | `0` | `1` | Top row is fixed |
| Finish | `1` | none | Both cells become black |

The chase correctly chooses the only switch that can create the required pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(KL⋅min(K,L)) | Each possible first-row bit requires one chase, and the chase touches every cell |
| Space | O(KL) | The grid and answer are stored |

Because the smaller side of the grid is at most 316, the multiplication factor stays small even when the number of cells reaches 100000.

## Test Cases

```python
# The submitted program is read from stdin, so these examples are intended
# to be run manually with the solution above.

cases = [
    (
        "1 2\nB W\n",
        "IMPOSSIBLE"
    ),
    (
        "1 1\nB\n",
        "P"
    ),
    (
        "2 1\nB\nB\n",
        "P\nA"
    ),
    (
        "1 3\nB B B\n",
        "A P A"
    )
]

for inp, expected in cases:
    print("Input:")
    print(inp)
    print("Expected contains:")
    print(expected)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / B W` | `IMPOSSIBLE` | Unsatisfiable one-row case |
| `1 1 / B` | Any single press | Smallest possible grid |
| `2 1 / B B` | One vertical press | Boundary handling |
| `1 3 / B B B` | Middle press | Horizontal neighbour logic |

## Edge Cases

The unsolvable two-cell row is handled because the generated linear system has no valid first-row assignment. The elimination phase detects the contradiction instead of producing an invalid press pattern.

Single-row and single-column grids are handled because the same recurrence still applies. The missing neighbours simply contribute zero in the bit operations.

Transposition avoids a hidden performance issue. A grid with dimensions `1 x 100000` would otherwise create a linear system with 100000 variables. After transposition, it becomes `100000 x 1`, and the system has only one variable.
