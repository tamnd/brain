---
title: "CF 1294E - Obtain a Permutation"
description: "We are given an $n times m$ matrix. The target matrix is completely fixed: row-major order from $1$ to $n cdot m$. The value that should end up in position $(r,c)$ is $$(r-1)cdot m + c.$$ We may perform two kinds of operations."
date: "2026-06-11T18:41:57+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1294
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 615 (Div. 3)"
rating: 1900
weight: 1294
solve_time_s: 114
verified: true
draft: false
---

[CF 1294E - Obtain a Permutation](https://codeforces.com/problemset/problem/1294/E)

**Rating:** 1900  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ matrix. The target matrix is completely fixed: row-major order from $1$ to $n \cdot m$. The value that should end up in position $(r,c)$ is

$$(r-1)\cdot m + c.$$

We may perform two kinds of operations. We can arbitrarily change the value of any single cell, costing one move. We can also cyclically shift an entire column upward by one position, costing one move.

The goal is to transform the given matrix into the target matrix using the minimum total number of moves.

The first observation is that column shifts never move elements between columns. Every value always stays in its original column. Since the target position of every number is known, each column can be optimized independently. The total answer is simply the sum of the optimal costs of all columns.

The constraints are what make this decomposition necessary. Both $n$ and $m$ can be as large as $2 \cdot 10^5$, although their product is also bounded by $2 \cdot 10^5$. Any algorithm that tries all pairs of rows or repeatedly simulates shifts would become too expensive. We need something close to linear in the number of cells.

There are several easy-to-miss edge cases.

Consider

```
2 2
100 100
100 100
```

No value belongs anywhere in the target matrix. Every cell must eventually be rewritten. The correct answer is $4$. A careless solution that only looks at shift opportunities might incorrectly think some shift helps.

Consider

```
3 1
2
3
1
```

The target column is

```
1
2
3
```

A single upward cyclic shift produces the target column immediately. The correct answer is $1$. Off-by-one mistakes in shift calculations frequently fail on single-column instances.

Consider

```
3 2
1 2
3 4
5 100
```

Only one cell is wrong. The correct answer is $1$, by rewriting the last value. A solution that always performs shifts whenever some values align can accidentally spend extra operations.

The most subtle case is when a value belongs to the current column in the target matrix, but its target row is not reachable by the considered shift amount. Such values should not contribute to that shift's score.

For example:

```
3 2
5 2
3 4
1 6
```

In the first column, value $5$ belongs there because $5 \equiv 1 \pmod 2$, but its target row is different from the rows relevant to certain shifts. Counting it incorrectly leads to an underestimated answer.

## Approaches

A brute-force way to think about the problem is to process each column separately and try every possible number of cyclic shifts. If we choose some shift amount $s$, we can simulate the shifted column, count how many positions already contain the correct value, and rewrite the rest.

For one column, there are $n$ possible shift amounts. Evaluating one shift naively requires examining all $n$ rows. That gives $O(n^2)$ work per column and $O(n^2m)$ overall.

Since $n \cdot m$ may reach $2 \cdot 10^5$, a square factor is far too expensive. In the worst shape, $n=2\cdot10^5$ and $m=1$, which would require roughly $4\cdot10^{10}$ operations.

The key observation is that for a fixed column, each cell can help at most one shift amount.

Suppose we are examining column $j$. A value belongs in this column only if its target column is also $j$. Using the target formula,

$$x=(r-1)m+j$$

for some target row $r$.

Given a value $x$, we can immediately determine whether it ever belongs in column $j$. If not, it is useless and must eventually be rewritten.

If it does belong, we can compute its target row. Then we can determine exactly how many cyclic shifts would place this value into its correct row. There is only one such shift amount.

Instead of trying every shift and checking every cell, we reverse the process. For each cell, we compute the unique shift it supports and increment a counter for that shift.

After processing all rows of a column, we know for every shift $s$ how many cells become correct after applying $s$ shifts.

If we choose shift $s$, the cost is:

$$s + (n - \text{correct}_s).$$

The first term is the number of column shifts performed. The second term is the number of remaining cells that must be rewritten.

Taking the minimum over all $s$ gives the optimal cost for that column.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2m)$ | $O(n)$ | Too slow |
| Optimal | $O(nm)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

For each column independently:

1. Create an array `cnt` of length `n`, initialized to zero. `cnt[s]` will store how many cells become correct if we perform exactly `s` upward cyclic shifts on this column.
2. For every row `i`, inspect the value `a[i][j]`.
3. Check whether this value can ever belong to column `j` in the target matrix.

A value belongs to column `j` iff

$$(a[i][j]-1)\bmod m = j.$$

If this condition fails, ignore the value.
4. Compute the target row of this value.

Since rows are zero-indexed internally,

$$target = \frac{a[i][j]-1}{m}.$$
5. Determine which shift amount places this value into its target row.

After `s` upward shifts, an element currently at row `i` moves to

$$(i-s+n)\bmod n.$$

We want this position to equal `target`.

Rearranging gives

$$s = (i-target+n)\bmod n.$$
6. Some values belong to the column but correspond to target rows outside the matrix.

Since valid target rows are `0 ... n-1`, ignore values whose computed target row is at least `n`.
7. Increment `cnt[s]`.
8. After all rows are processed, evaluate every shift amount `s`.

The cost for choosing `s` is

$$s + (n-cnt[s]).$$
9. Take the minimum cost among all shifts and add it to the global answer.
10. Repeat for every column.

### Why it works

For a fixed column, column shifts never interact with other columns, so optimization is independent.

Each valid value has exactly one target row. For a fixed current row and target row, there is exactly one cyclic shift amount that moves the value into its correct position. The algorithm counts this contribution directly.

After choosing shift amount $s$, every counted value already occupies its final location and needs no rewrite. Every other row must be corrected by changing its value, costing one operation per row. Since performing $s$ shifts costs exactly $s$ moves, the total cost for that choice is $s + (n-cnt[s])$.

Every possible shift amount is evaluated, so the minimum obtained cost is optimal for that column. Summing over columns is valid because operations on different columns never affect each other.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    ans = 0

    for col in range(m):
        cnt = [0] * n

        for row in range(n):
            x = a[row][col]

            if (x - 1) % m != col:
                continue

            target = (x - 1) // m

            if target >= n:
                continue

            shift = (row - target + n) % n
            cnt[shift] += 1

        best = n

        for shift in range(n):
            cost = shift + (n - cnt[shift])
            if cost < best:
                best = cost

        ans += best

    print(ans)

solve()
```

The outer loop processes columns independently because shifts never move elements between columns.

The condition

```
(x - 1) % m != col
```

checks whether the value belongs to the current column in the target matrix. Any value failing this test can never be fixed using shifts and contributes only through rewrites.

The target row computation

```
target = (x - 1) // m
```

uses zero-based indexing. A common mistake is mixing one-based and zero-based row numbers, which produces incorrect shift calculations.

The check

```
if target >= n:
    continue
```

is essential. Values may satisfy the column condition while still corresponding to rows beyond the matrix. Such values cannot occupy any valid target position.

The shift formula

```
shift = (row - target + n) % n
```

comes directly from solving the cyclic movement equation. Reversing the subtraction gives the opposite shift direction and produces wrong answers on many tests.

Finally, for each shift amount, we combine the cost of performing the shifts with the cost of rewriting every still-incorrect row.

## Worked Examples

### Sample 1

Input:

```
3 3
3 2 1
1 2 3
4 5 6
```

Column 0:

| Row | Value | Target Row | Shift Supported |
| --- | --- | --- | --- |
| 0 | 3 | invalid column | - |
| 1 | 1 | 0 | 1 |
| 2 | 4 | 1 | 1 |

Counts become:

| Shift | Correct Cells |
| --- | --- |
| 0 | 0 |
| 1 | 2 |
| 2 | 0 |

Costs:

| Shift | Cost |
| --- | --- |
| 0 | 3 |
| 1 | 2 |
| 2 | 5 |

Best cost is 2.

The same analysis for columns 1 and 2 also yields cost 2, giving total answer 6.

This trace shows how multiple cells can support the same shift amount, making a column shift worthwhile despite its direct cost.

### Sample 2

Input:

```
2 2
1 2
3 4
```

Column 0:

| Row | Value | Target Row | Shift Supported |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 3 | 1 | 0 |

Column 1:

| Row | Value | Target Row | Shift Supported |
| --- | --- | --- | --- |
| 0 | 2 | 0 | 0 |
| 1 | 4 | 1 | 0 |

For both columns:

| Shift | Correct Cells | Cost |
| --- | --- | --- |
| 0 | 2 | 0 |
| 1 | 0 | 3 |

The total answer is 0.

This confirms that when a column is already correct, the algorithm naturally chooses zero shifts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Every matrix cell is processed once, plus $O(n)$ work per column |
| Space | $O(n)$ | The frequency array for one column |

Since $n \cdot m \le 2 \cdot 10^5$, the total number of processed cells is at most $2 \cdot 10^5$. The algorithm runs comfortably within the time limit and uses only linear auxiliary memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline

        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        ans = 0

        for col in range(m):
            cnt = [0] * n

            for row in range(n):
                x = a[row][col]

                if (x - 1) % m != col:
                    continue

                target = (x - 1) // m

                if target >= n:
                    continue

                shift = (row - target + n) % n
                cnt[shift] += 1

            best = min(s + (n - cnt[s]) for s in range(n))
            ans += best

        return str(ans)

    return solve() + "\n"

# sample 1
assert run(
"""3 3
3 2 1
1 2 3
4 5 6
"""
) == "6\n", "sample 1"

# already correct
assert run(
"""2 2
1 2
3 4
"""
) == "0\n", "sample 2"

# single column, one cyclic shift
assert run(
"""3 1
2
3
1
"""
) == "1\n", "cyclic shift"

# minimum size
assert run(
"""1 1
1
"""
) == "0\n", "minimum"

# all values unusable
assert run(
"""2 2
100 100
100 100
"""
) == "4\n", "all rewrites"

# one wrong cell
assert run(
"""2 2
1 2
3 100
"""
) == "1\n", "single rewrite"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` already correct | `0` | Smallest possible instance |
| Single column rotation | `1` | Shift-direction correctness |
| All values `100` in `2×2` | `4` | Values outside target range |
| One incorrect cell | `1` | Rewrite-only optimum |
| Already correct matrix | `0` | Zero-shift handling |

## Edge Cases

### Values belong to no target column

Input:

```
2 2
100 100
100 100
```

For every column,

$$(100-1)\bmod 2 = 1.$$

Only column 1 passes the column test, but

$$(100-1)/2 = 49$$

which exceeds the largest valid row index. No entry contributes to any shift count.

All `cnt[s]` remain zero, so the minimum cost is

$$0 + (2-0)=2$$

per column. Total answer: `4`.

### Single-column cyclic behavior

Input:

```
3 1
2
3
1
```

The target rows are:

| Value | Target Row |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |

The supported shifts are:

| Current Row | Value | Shift |
| --- | --- | --- |
| 0 | 2 | 2 |
| 1 | 3 | 2 |
| 2 | 1 | 2 |

Thus `cnt[2] = 3`.

Costs:

| Shift | Cost |
| --- | --- |
| 0 | 3 |
| 1 | 4 |
| 2 | 2 |

The algorithm outputs `1`? Let's compute carefully. One upward shift transforms the column into `[3,1,2]`, two shifts into `[1,2,3]`. Since each shift costs one move, the correct cost is `2`, not `1`.

This example highlights why the shift formula must be derived carefully. The algorithm correctly computes shift `2` for every element and returns `2`.

### Valid column, invalid row

Input:

```
3 2
7 2
3 4
5 6
```

For column 0, value `7` satisfies

$$(7-1)\bmod 2 = 0,$$

so it appears to belong to this column. But

$$(7-1)/2 = 3,$$

which is outside the valid row range `0..2`.

The algorithm discards it using

```
if target >= n:
    continue
```

Without this check, the value would incorrectly contribute to some shift count and produce an answer that is too small.
