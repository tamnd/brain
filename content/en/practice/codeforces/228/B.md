---
title: "CF 228B - Two Tables"
description: "We have two binary grids. A shift (x, y) means that cell (i, j) in the first grid is compared with cell (i + x, j + y) in the second grid. The score of a shift is the number of positions where both cells exist and both contain 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 1400
weight: 228
solve_time_s: 139
verified: true
draft: false
---

[CF 228B - Two Tables](https://codeforces.com/problemset/problem/228/B)

**Rating:** 1400  
**Tags:** brute force, implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two binary grids. A shift `(x, y)` means that cell `(i, j)` in the first grid is compared with cell `(i + x, j + y)` in the second grid. The score of a shift is the number of positions where both cells exist and both contain `1`.

The task is to find any shift that maximizes this overlap count.

The dimensions are at most `50 × 50`, so each table contains at most `2500` cells. That immediately rules out anything extremely heavy, but it also means we can afford quadratic or cubic work over the number of `1` cells.

The key detail is that the shift itself can be very large in absolute value according to the output format, but the useful shifts are actually limited. A shift only matters if at least one `1` from the first table can land on a `1` from the second table. Since coordinates stay within the table sizes, every relevant shift comes from aligning one specific `1` with another specific `1`.

A common mistake is to think only overlapping rectangles matter. Negative shifts are completely valid. For example:

```
1 1
1
1 1
1
```

The best answer is not unique. `(0, 0)` works, but so do many irrelevant shifts with overlap `0`. A careless implementation that only iterates non-negative shifts could miss valid optimal answers in more complicated cases.

Another subtle case appears when the overlap region is empty. Consider:

```
1 1
1
1 1
1
```

Shift `(100, 100)` produces overlap `0` because no cells intersect. The statement explicitly defines this score as `0`, not undefined. A buggy implementation might accidentally access out-of-bounds indices or count garbage values.

There is also an indexing trap in the formula. Suppose:

```
2 2
10
00
2 2
00
01
```

The correct shift is `(1, 1)` because the `1` from the first table at `(0, 0)` aligns with the `1` from the second table at `(1, 1)`. Reversing the subtraction and using `(ax - bx, ay - by)` instead of `(bx - ax, by - ay)` gives the opposite direction and produces the wrong answer.

## Approaches

The direct brute force is easy to describe. We try every possible shift `(x, y)`. For each shift, we iterate over every cell in the first table, compute the corresponding position in the second table, check bounds, and count how many pairs contain two `1`s.

This works because the overlap definition is explicit. If we examine every shift and evaluate its score exactly, the maximum is guaranteed to be found.

The problem is the number of shifts. Rows can move roughly from `-50` to `50`, and the same for columns, so there are about `100 × 100 = 10000` candidate shifts. For each one, scanning all `2500` cells gives around `25 million` operations. In Python this is still actually acceptable, but it is heavier than necessary and easy to implement incorrectly with all the boundary checks.

The useful observation is that only cells containing `1` matter. A pair of zeroes never contributes to the score. If a shift aligns a `1` from the first table with a `1` from the second table, then that pair contributes exactly one vote for that shift.

Suppose a `1` in the first table is at `(ra, ca)` and a `1` in the second table is at `(rb, cb)`. To align them, the shift must be:

$$x = rb - ra,\quad y = cb - ca$$

Every pair of `1` cells determines exactly one shift. If many pairs produce the same shift, that shift creates many overlapping `1`s.

So instead of iterating over shifts and checking cells, we iterate over pairs of `1`s and count how many times each shift appears.

The largest table has at most `2500` ones, so in the absolute worst case we process:

$$2500 \times 2500 = 6.25 \text{ million}$$

pairs. Each pair only performs a subtraction and a hashmap increment, which is fast enough in Python.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((na + nb)(ma + mb)na ma) | O(1) | Accepted but clumsy |
| Optimal | O(A × B) | O(A × B) in worst case | Accepted |

Here `A` and `B` are the numbers of `1`s in the two tables.

## Algorithm Walkthrough

1. Read both tables.
2. Store the coordinates of every cell containing `1` in the first table.

We ignore zeroes because they never contribute to the overlap score.
3. Store the coordinates of every cell containing `1` in the second table.
4. Create a dictionary `cnt` where the key is a shift `(x, y)` and the value is how many pairs of `1`s generate that shift.
5. For every `1` cell `(ra, ca)` in the first table and every `1` cell `(rb, cb)` in the second table, compute:

$$x = rb - ra,\quad y = cb - ca$$

Then increment `cnt[(x, y)]`.

This works because applying that shift moves `(ra, ca)` exactly onto `(rb, cb)`.
6. Track the shift with the largest count while processing pairs.
7. Output any shift with maximum frequency.

### Why it works

Every overlapping pair of `1`s contributes exactly one valid alignment shift. If two different pairs of cells require the same shift, then applying that shift makes both pairs overlap simultaneously.

So the overlap score for a shift is exactly the number of pairs of `1` cells producing that shift. Counting frequencies of shifts is therefore equivalent to computing overlap scores directly.

Since the algorithm checks every possible pair of `1`s, no valid overlap can be missed.

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
        for j in range(ma):
            if row[j] == '1':
                ones_a.append((i, j))

    nb, mb = map(int, input().split())

    ones_b = []

    for i in range(nb):
        row = input().strip()
        for j in range(mb):
            if row[j] == '1':
                ones_b.append((i, j))

    cnt = defaultdict(int)

    best_shift = (0, 0)
    best_value = -1

    for ra, ca in ones_a:
        for rb, cb in ones_b:
            shift = (rb - ra, cb - ca)

            cnt[shift] += 1

            if cnt[shift] > best_value:
                best_value = cnt[shift]
                best_shift = shift

    print(best_shift[0], best_shift[1])

solve()
```

The first part extracts only the coordinates containing `1`. This is the central optimization. Cells containing `0` are irrelevant because multiplying by zero contributes nothing to the overlap sum.

The nested loop enumerates every possible pair of `1`s. The subtraction order matters. We want the shift that moves the first table's cell onto the second table's cell, so the correct formula is:

```
(rb - ra, cb - ca)
```

Reversing it produces the opposite direction.

The dictionary stores how many pairs agree on the same shift. Whenever a shift count increases beyond the current best, we update the answer immediately. There is no need for a second pass through the hashmap.

The implementation uses zero-based indices internally. This is completely fine because only coordinate differences matter. Converting to one-based indexing would produce the same shifts after subtraction.

## Worked Examples

### Example 1

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

The `1` cells are:

First table:

`(0,1), (1,0)`

Second table:

`(0,2), (1,0), (1,1), (1,2)`

| A cell | B cell | Shift | Count after update |
| --- | --- | --- | --- |
| (0,1) | (0,2) | (0,1) | 1 |
| (0,1) | (1,0) | (1,-1) | 1 |
| (0,1) | (1,1) | (1,0) | 1 |
| (0,1) | (1,2) | (1,1) | 1 |
| (1,0) | (0,2) | (-1,2) | 1 |
| (1,0) | (1,0) | (0,0) | 1 |
| (1,0) | (1,1) | (0,1) | 2 |
| (1,0) | (1,2) | (0,2) | 1 |

Shift `(0,1)` appears twice, more than any other shift.

Output:

```
0 1
```

This trace shows the key invariant. Every matching pair contributes one vote to exactly one shift, and the optimal shift is simply the most frequent one.

### Example 2

Input:

```
2 2
10
00
2 2
00
01
```

The `1` cells are:

First table:

`(0,0)`

Second table:

`(1,1)`

| A cell | B cell | Shift | Count |
| --- | --- | --- | --- |
| (0,0) | (1,1) | (1,1) | 1 |

The only possible alignment is `(1,1)`.

Output:

```
1 1
```

This example checks the direction of subtraction. Using `(ra - rb, ca - cb)` would incorrectly produce `(-1,-1)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A × B) | Every pair of `1` cells is processed once |
| Space | O(A × B) worst case | The hashmap may store many distinct shifts |

`A` and `B` are the counts of `1`s in the two tables. Since each table contains at most `2500` cells, the worst-case running time is about `6.25 million` pair operations, which easily fits within the limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    na, ma = map(int, input().split())

    ones_a = []

    for i in range(na):
        row = input().strip()
        for j in range(ma):
            if row[j] == '1':
                ones_a.append((i, j))

    nb, mb = map(int, input().split())

    ones_b = []

    for i in range(nb):
        row = input().strip()
        for j in range(mb):
            if row[j] == '1':
                ones_b.append((i, j))

    cnt = defaultdict(int)

    best_shift = (0, 0)
    best_value = -1

    for ra, ca in ones_a:
        for rb, cb in ones_b:
            shift = (rb - ra, cb - ca)

            cnt[shift] += 1

            if cnt[shift] > best_value:
                best_value = cnt[shift]
                best_shift = shift

    print(best_shift[0], best_shift[1])

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

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
) == "0 1", "sample 1"

# minimum size
assert run(
"""1 1
1
1 1
1
"""
) == "0 0", "minimum case"

# negative shift
assert run(
"""2 2
00
01
2 2
10
00
"""
) == "-1 -1", "negative shift"

# exact overlap
assert run(
"""2 2
11
11
2 2
11
11
"""
) == "0 0", "perfect overlap"

# off-by-one direction check
assert run(
"""2 2
10
00
2 2
00
01
"""
) == "1 1", "direction correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-cell tables | `0 0` | Minimum valid input |
| Bottom-right to top-left alignment | `-1 -1` | Negative shifts |
| Two identical full tables | `0 0` | Maximum overlap |
| One isolated pair | `1 1` | Correct subtraction direction |

## Edge Cases

Consider the negative-shift case:

```
2 2
00
01
2 2
10
00
```

The first table has a `1` at `(1,1)`. The second table has a `1` at `(0,0)`.

The algorithm computes:

```
x = 0 - 1 = -1
y = 0 - 1 = -1
```

The hashmap records shift `(-1,-1)` with frequency `1`, which becomes the answer. This confirms that the algorithm naturally handles upward and leftward movement without any special cases.

Now consider a case where many shifts exist but only one gives multiple overlaps:

```
2 2
11
00
2 2
11
00
```

The pairs generate:

```
(0,0), (0,1), (0,-1), (0,0)
```

Shift `(0,0)` appears twice because both `1`s align simultaneously. The algorithm correctly prefers frequency over merely finding any valid overlap.

Finally, consider the subtraction-direction trap:

```
2 2
10
00
2 2
00
01
```

Coordinates:

```
A: (0,0)
B: (1,1)
```

The algorithm stores:

```
(1 - 0, 1 - 0) = (1,1)
```

Applying shift `(1,1)` indeed moves the first table's `1` onto the second table's `1`. This confirms the coordinate transformation is oriented correctly.
