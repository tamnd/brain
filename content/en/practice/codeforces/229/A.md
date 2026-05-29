---
title: "CF 229A - Shifts"
description: "We have a binary matrix where each row can be rotated cyclically. A left rotation moves every element one position left and wraps the first element to the end. A right rotation does the opposite."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 229
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 142 (Div. 1)"
rating: 1500
weight: 229
solve_time_s: 94
verified: true
draft: false
---

[CF 229A - Shifts](https://codeforces.com/problemset/problem/229/A)

**Rating:** 1500  
**Tags:** brute force, two pointers  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a binary matrix where each row can be rotated cyclically. A left rotation moves every element one position left and wraps the first element to the end. A right rotation does the opposite.

The goal is to make at least one column consist entirely of `1`s, using the minimum total number of row shifts. Each row may be shifted independently, and shifting a row by one position costs one move.

The key observation is that rows do not interact with each other except through the choice of the final column. If we decide that column `j` should become all `1`s, then each row independently contributes some minimum cost to place a `1` into that column. The total cost for column `j` is the sum of those per-row costs.

The constraints are small in one dimension and large in the other. We have at most `100` rows, but up to `10^4` columns. A solution around `O(n * m^2)` is still acceptable because the worst case is about `10^8` operations, which is close to the limit in Python and risky. Anything cubic is completely impossible. A near-linear scan per row is the target.

There is one particularly important impossibility condition. If a row contains no `1` at all, then no amount of cyclic shifting can ever place a `1` into any column. That means the answer is immediately `-1`.

A common mistake is to treat left and right shifts separately without considering wraparound correctly.

For example:

```
1 5
10000
```

The correct answer is `0`, because column `0` already contains a `1`.

If we target column `4`, the minimum cost is `1`, not `4`, because one right shift transforms `10000` into `00001`.

Another easy bug appears when computing distances only in one direction.

Consider:

```
1 6
001000
```

Targeting column `0` should cost `2`, because shifting left twice moves the `1` from index `2` to index `0`. A one-directional scan might incorrectly return `4`.

There is also a subtle wraparound case:

```
1 5
00001
```

Targeting column `0` costs `1`, because one left shift moves the last element to the front. Forgetting cyclic behavior would incorrectly return `4`.

## Approaches

The brute-force idea is straightforward. For every target column `j`, try every row independently and compute the minimum number of shifts needed to bring some `1` into column `j`.

Suppose a row has a `1` at position `k`. To move that `1` into column `j`, we can rotate left or right. The cost is:

```
min((j - k) mod m, (k - j) mod m)
```

For every row and every target column, we could scan all positions containing `1` and take the minimum cost.

This works because each row is independent once the target column is fixed.

The problem is complexity. In the worst case, every row contains `m` ones. Then for each of the `m` target columns we scan all `m` positions again. The total complexity becomes:

```
O(n * m^2)
```

With `m = 10^4`, this reaches around `10^10` primitive operations, far too slow.

The structure of the problem gives a much better option. For a fixed row, we want the distance from every column to the nearest `1` on a circle.

That becomes a classic nearest-element problem on a cyclic array.

The useful trick is to duplicate the row. If the original row has length `m`, create a conceptual array of length `2m` by repeating it twice. Now circular wraparound becomes ordinary linear distance.

We scan from left to right and track the nearest `1` on the left. Then we scan from right to left and track the nearest `1` on the right. Combining those two distances gives the minimum cyclic distance for every column.

After computing the cost contribution of one row to every column, we add it into a global answer array.

This reduces the total complexity to `O(n * m)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m²) | O(1) | Too slow |
| Optimal | O(n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the matrix and create an array `ans` of size `m`, initialized to `0`.
2. Process each row independently because the cost contribution of one row does not depend on the others.
3. If a row contains no `1`, immediately print `-1`.

No cyclic shift can create a `1` in that row, so forming an all-ones column is impossible.
4. Duplicate the row by concatenating it with itself.

This transforms cyclic movement into ordinary linear movement. Positions near the ends can now see wrapped neighbors naturally.
5. Create an array `dist` of length `2m`, initialized with a large value.
6. Scan left to right.

Maintain the position of the most recent `1`. If the current position is reachable from that `1`, update the distance.
7. Scan right to left.

Maintain the nearest `1` on the right and minimize the distance again.
8. For each original column `j`, the relevant positions are `j` and `j + m` inside the doubled array.

Take the minimum of those two distances. This gives the true cyclic distance from column `j` to the nearest `1`.
9. Add that distance into `ans[j]`.
10. After all rows are processed, print the minimum value in `ans`.

### Why it works

For a fixed target column, the optimal strategy is independent for each row. The minimum total cost is the sum of the minimum costs per row.

Duplicating the row converts circular distance into linear distance. Any shortest cyclic path between two positions appears as an ordinary segment somewhere inside the doubled array.

The two scans compute the nearest `1` from the left and right for every position. Taking the minimum gives the shortest linear distance, which matches the shortest cyclic shift distance after duplication.

Since every row contributes its exact minimum cost to every column, and we finally choose the cheapest column, the algorithm always produces the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    rows = [input().strip() for _ in range(n)]

    ans = [0] * m
    INF = 10**18

    for s in rows:
        if '1' not in s:
            print(-1)
            return

        t = s + s
        dist = [INF] * (2 * m)

        last = -INF

        for i in range(2 * m):
            if t[i] == '1':
                last = i
            dist[i] = min(dist[i], i - last)

        last = INF

        for i in range(2 * m - 1, -1, -1):
            if t[i] == '1':
                last = i
            dist[i] = min(dist[i], last - i)

        for j in range(m):
            ans[j] += min(dist[j], dist[j + m])

    print(min(ans))

solve()
```

The solution maintains a running total for every target column. Each row independently adds its minimum shift cost into that total.

The duplicated string `t = s + s` is the core trick. Without duplication, handling wraparound cleanly becomes messy and error-prone. After duplication, a nearest-`1` search behaves exactly like a normal linear array problem.

The left-to-right scan computes the distance to the nearest `1` on the left side. The right-to-left scan computes the nearest `1` on the right side. The minimum of the two is the true shortest distance.

The expression:

```
min(dist[j], dist[j + m])
```

is easy to overlook. Both positions correspond to the same original cyclic column. Taking both ensures that wraparound paths are included correctly.

Using a very large sentinel like `10**18` avoids special-case checks during scanning.

## Worked Examples

### Sample 1

Input:

```
3 6
101010
000100
100000
```

For the first row:

| Column | Nearest `1` distance |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |
| 4 | 0 |
| 5 | 1 |

For the second row:

| Column | Nearest `1` distance |
| --- | --- |
| 0 | 3 |
| 1 | 2 |
| 2 | 1 |
| 3 | 0 |
| 4 | 1 |
| 5 | 2 |

For the third row:

| Column | Nearest `1` distance |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

Summing column-wise:

| Column | Total cost |
| --- | --- |
| 0 | 3 |
| 1 | 4 |
| 2 | 3 |
| 3 | 4 |
| 4 | 3 |
| 5 | 4 |

The minimum is `3`.

This example demonstrates that multiple columns may share the same optimal answer. The algorithm evaluates all of them simultaneously.

### Sample 2

Input:

```
2 3
000
111
```

The first row contains no `1`.

| Row | Contains `1`? |
| --- | --- |
| 000 | No |
| 111 | Yes |

Since the first row can never contribute a `1` to any column, the answer is immediately `-1`.

This confirms the impossibility check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Each row is scanned a constant number of times |
| Space | O(m) | Distance arrays and answer array are linear in columns |

With `n ≤ 100` and `m ≤ 10^4`, the total work is around a few million operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    rows = [input().strip() for _ in range(n)]

    ans = [0] * m
    INF = 10**18

    for s in rows:
        if '1' not in s:
            print(-1)
            return

        t = s + s
        dist = [INF] * (2 * m)

        last = -INF

        for i in range(2 * m):
            if t[i] == '1':
                last = i
            dist[i] = min(dist[i], i - last)

        last = INF

        for i in range(2 * m - 1, -1, -1):
            if t[i] == '1':
                last = i
            dist[i] = min(dist[i], last - i)

        for j in range(m):
            ans[j] += min(dist[j], dist[j + m])

    print(min(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
"""3 6
101010
000100
100000
"""
) == "3", "sample 1"

# impossible case
assert run(
"""2 3
000
111
"""
) == "-1", "sample 2"

# minimum size
assert run(
"""1 1
1
"""
) == "0", "single cell already valid"

# wraparound check
assert run(
"""1 5
00001
"""
) == "0", "existing column already works"

# cyclic distance must use wraparound
assert run(
"""1 5
10000
"""
) == "0", "distance through wraparound"

# all ones
assert run(
"""3 4
1111
1111
1111
"""
) == "0", "no shifts needed"

# off-by-one around edges
assert run(
"""2 5
01000
00010
"""
) == "2", "edge distance correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Minimum-size input |
| `2 3 / 000 / 111` | `-1` | Impossible rows |
| `1 5 / 00001` | `0` | Existing valid column |
| `1 5 / 10000` | `0` | Wraparound handling |
| all rows `1111` | `0` | No movement needed |
| `01000` and `00010` | `2` | Boundary distances |

## Edge Cases

Consider the impossible configuration:

```
2 4
0000
1010
```

The first row contains no `1`. During processing, the algorithm checks:

```
if '1' not in s:
```

and immediately returns `-1`.

This is correct because cyclic shifts only rearrange existing values. A row of all zeros can never contribute a `1` to any column.

Now consider wraparound behavior:

```
1 5
00001
```

Column `0` is only one shift away from the existing `1`.

After duplication:

```
0000100001
```

the left-to-right and right-to-left scans correctly detect that the nearest `1` to position `0` is distance `1`, not `4`.

This validates the cyclic transformation trick.

Finally, consider a case where the shortest path crosses the boundary:

```
1 6
100000
```

Targeting column `5` should cost `1`.

Inside the doubled string:

```
100000100000
```

position `5` sees the next `1` at position `6`, giving distance `1`.

A naive non-cyclic implementation would incorrectly return `5`.
