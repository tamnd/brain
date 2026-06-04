---
title: "CF 228B - Two Tables"
description: "We have two binary matrices. A shift (x, y) means that cell (i, j) of the first matrix is compared with cell (i + x, j + y) of the second matrix. For a fixed shift, the overlap factor is the sum of products of overlapping cells."
date: "2026-06-04T08:59:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 1400
weight: 228
solve_time_s: 95
verified: true
draft: false
---

[CF 228B - Two Tables](https://codeforces.com/problemset/problem/228/B)

**Rating:** 1400  
**Tags:** brute force, implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two binary matrices. A shift `(x, y)` means that cell `(i, j)` of the first matrix is compared with cell `(i + x, j + y)` of the second matrix.

For a fixed shift, the overlap factor is the sum of products of overlapping cells. Since all values are either `0` or `1`, a product contributes `1` exactly when both overlapping cells contain `1`.

Another way to view the problem is to look only at the positions containing `1`. For a given shift, the overlap factor is simply the number of pairs of `1` cells, one from each table, that become aligned after applying that shift.

We must find any shift that maximizes this count.

The dimensions of both matrices are at most `50 × 50`. That means each matrix contains at most `2500` cells. A solution that examines every possible shift and every cell pair would perform tens of millions of operations. That is not enormous, but there is a much cleaner observation that leads directly to the intended solution.

The fact that the matrices contain only `0` and `1` is the key structural property. Only positions containing `1` matter. Since each matrix is guaranteed to contain at least one `1`, we can focus entirely on those positions.

A common mistake is to think only about overlapping areas. The optimal shift may place most of one matrix outside the other. For example:

```
A:
1

B:
1
```

Every shift produces overlap factor either `1` or `0`. The shift values themselves are not constrained by the matrix dimensions.

Another easy mistake is to compute shifts in the wrong direction. If a `1` in the first matrix is at `(r1, c1)` and a `1` in the second matrix is at `(r2, c2)`, the shift that aligns them is:

```
x = r2 - r1
y = c2 - c1
```

Reversing the subtraction produces the opposite shift and counts the wrong alignments.

A final subtle case occurs when multiple shifts achieve the same maximum overlap. The statement allows any optimal answer, so we only need to remember one shift with the largest count.

## Approaches

The most direct solution is to try every possible shift. Since the matrices are at most `50 × 50`, the row shift ranges roughly from `-49` to `49`, and the column shift does the same. For each shift, we can scan all cells and count overlapping pairs of ones.

This approach is correct because it literally evaluates the overlap factor for every candidate shift. The problem is efficiency. There are about `100 × 100 = 10,000` possible shifts, and each shift may require scanning up to `2500` cells. The worst-case cost is around 25 million cell checks.

The crucial observation is that only cells containing `1` contribute to the overlap factor.

Suppose a `1` in the first matrix is located at `(ra, ca)` and a `1` in the second matrix is located at `(rb, cb)`. These two cells become aligned under exactly one shift:

```
(rb - ra, cb - ca)
```

If many pairs of ones produce the same shift, then all those pairs become aligned simultaneously under that shift.

This transforms the problem into a counting problem. For every pair consisting of a `1` from the first matrix and a `1` from the second matrix, compute the shift that aligns them and count how many times each shift appears.

The shift with the largest frequency is exactly the shift that creates the maximum number of overlapping pairs of ones.

Since each matrix contains at most `2500` ones, there are at most `2500 × 2500 = 6.25` million pairs. That comfortably fits within the limits in Python.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(na·ma·nb·mb) via all shifts and scans | O(1) | Accepted, but less elegant |
| Optimal | O(A·B) where A and B are counts of ones | O(A·B) in the worst case | Accepted |

## Algorithm Walkthrough

1. Read both matrices.
2. Extract the coordinates of every cell containing `1` in the first matrix.
3. Extract the coordinates of every cell containing `1` in the second matrix.
4. Create a hash map from shift `(x, y)` to its frequency.
5. For every `1` cell `(ra, ca)` in the first matrix and every `1` cell `(rb, cb)` in the second matrix, compute:

```
x = rb - ra
y = cb - ca
```

Increment the frequency of shift `(x, y)`.

This shift is the unique translation that aligns those two cells.
6. Track the shift whose frequency becomes largest.
7. Output that shift.

### Why it works

Consider any fixed shift `(x, y)`.

A pair of `1` cells contributes to the overlap factor under this shift if and only if:

```
rb = ra + x
cb = ca + y
```

Rearranging gives:

```
x = rb - ra
y = cb - ca
```

So every contributing pair corresponds to exactly one occurrence of shift `(x, y)` in our counting process.

Conversely, every pair counted for shift `(x, y)` becomes aligned under that shift and contributes `1` to the overlap factor.

The frequency stored for a shift is therefore exactly equal to its overlap factor. Maximizing the frequency maximizes the overlap factor, which proves correctness.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    na, ma = map(int, input().split())

    ones_a = []
    for i in range(na):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch == '1':
                ones_a.append((i, j))

    nb, mb = map(int, input().split())

    ones_b = []
    for i in range(nb):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch == '1':
                ones_b.append((i, j))

    cnt = defaultdict(int)

    best_shift = (0, 0)
    best_count = -1

    for ra, ca in ones_a:
        for rb, cb in ones_b:
            shift = (rb - ra, cb - ca)
            cnt[shift] += 1

            if cnt[shift] > best_count:
                best_count = cnt[shift]
                best_shift = shift

    print(best_shift[0], best_shift[1])

if __name__ == "__main__":
    solve()
```

The first part of the code extracts all positions containing `1`. Every other cell is irrelevant because a product involving a zero never contributes to the overlap factor.

The nested loop enumerates every pair of `1` cells. For each pair we compute the unique shift that aligns them. The dictionary counts how many pairs vote for each shift.

The moment a shift's count exceeds the current maximum, we store it as the best answer. Since the statement accepts any optimal shift, there is no need for tie-breaking logic.

Using zero-based coordinates instead of one-based coordinates does not affect the computed shifts. Both endpoints of the subtraction are shifted by the same constant, so the difference remains identical.

No overflow issues exist because coordinate differences are at most about `50` in magnitude.

## Worked Examples

### Sample 1

Input:

```
3 2
01
10
00
2 3
001
111
```

Positions of ones:

```
A: (0,1), (1,0)
B: (0,2), (1,0), (1,1), (1,2)
```

| A cell | B cell | Shift |
| --- | --- | --- |
| (0,1) | (0,2) | (0,1) |
| (0,1) | (1,0) | (1,-1) |
| (0,1) | (1,1) | (1,0) |
| (0,1) | (1,2) | (1,1) |
| (1,0) | (0,2) | (-1,2) |
| (1,0) | (1,0) | (0,0) |
| (1,0) | (1,1) | (0,1) |
| (1,0) | (1,2) | (0,2) |

Frequency table:

| Shift | Count |
| --- | --- |
| (0,1) | 2 |
| all others | 1 |

The maximum frequency is `2`, so `(0,1)` is an optimal answer.

This example demonstrates the central idea: the answer emerges directly from counting identical shifts.

### Example 2

```
1 1
1
1 1
1
```

Positions:

```
A: (0,0)
B: (0,0)
```

| A cell | B cell | Shift |
| --- | --- | --- |
| (0,0) | (0,0) | (0,0) |

Frequency table:

| Shift | Count |
| --- | --- |
| (0,0) | 1 |

Output:

```
0 0
```

This shows the smallest possible valid input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A·B) | A and B are the numbers of ones in the two matrices |
| Space | O(A·B) worst case | Distinct shifts stored in the hash map |

In the worst case, both matrices are entirely filled with ones, so `A = B = 2500`. The algorithm performs `6.25 × 10^6` pair evaluations, which fits comfortably within the time limit. The number of distinct shifts is actually bounded by the coordinate ranges, making memory usage very small in practice.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    na, ma = map(int, input().split())

    ones_a = []
    for i in range(na):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch == '1':
                ones_a.append((i, j))

    nb, mb = map(int, input().split())

    ones_b = []
    for i in range(nb):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch == '1':
                ones_b.append((i, j))

    cnt = defaultdict(int)

    best_shift = (0, 0)
    best_count = -1

    for ra, ca in ones_a:
        for rb, cb in ones_b:
            shift = (rb - ra, cb - ca)
            cnt[shift] += 1

            if cnt[shift] > best_count:
                best_count = cnt[shift]
                best_shift = shift

    return f"{best_shift[0]} {best_shift[1]}"

# provided sample
assert run(
"""3 2
01
10
00
2 3
001
111
"""
) == "0 1"

# minimum size
assert run(
"""1 1
1
1 1
1
"""
) == "0 0"

# unique non-zero shift
assert run(
"""2 2
10
00
2 2
00
01
"""
) == "1 1"

# all cells are ones
out = run(
"""2 2
11
11
2 2
11
11
"""
)
assert out == "0 0"

# boundary shift
assert run(
"""1 2
10
2 2
00
01
"""
) == "1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-cell matrices | `0 0` | Minimum valid input |
| One corner aligned to opposite corner | `1 1` | Correct shift direction |
| All cells equal to one | `0 0` | Large overlap count accumulation |
| Edge-to-edge alignment | `1 1` | Boundary coordinate differences |

## Edge Cases

Consider two matrices each containing a single `1`:

```
1 1
1
1 1
1
```

The only pair of ones produces shift `(0,0)`. The frequency of that shift is `1`, so the algorithm returns `(0,0)`. No overlap-area calculations are needed.

Consider a case where the optimal shift moves one matrix mostly outside the other:

```
1 2
10
2 2
00
01
```

The positions of ones are `(0,0)` and `(1,1)`. Their alignment shift is `(1,1)`. The algorithm counts this pair and returns `(1,1)` even though most cells lie outside the overlapping region. This is correct because overlap factor depends only on aligned ones.

Consider multiple optimal answers:

```
1 2
11
1 2
11
```

Both shifts `(0,0)` and several others may receive counts during processing, but `(0,0)` achieves the maximum overlap factor of `2`. If another shift tied for the maximum in a different example, the algorithm would return whichever reached the maximum first. The statement explicitly allows any optimal answer, so this behavior is valid.

Finally, consider the common sign mistake. If a `1` appears at `(0,0)` in the first matrix and `(1,1)` in the second matrix, the aligning shift is:

```
(1 - 0, 1 - 0) = (1,1)
```

Using `(0 - 1, 0 - 1)` would produce `(-1,-1)`, which moves the second matrix in the wrong direction. The algorithm consistently computes `rb - ra` and `cb - ca`, avoiding this error.
