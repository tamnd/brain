---
title: "CF 333D - Characteristics of Rectangles"
description: "We are given a grid of integers. From this grid we may cut away some rows from the top and bottom, and some columns from the left and right. After cropping, the remaining part must still be a rectangle with at least two rows and two columns."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 333
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 194 (Div. 1)"
rating: 2100
weight: 333
solve_time_s: 132
verified: false
draft: false
---

[CF 333D - Characteristics of Rectangles](https://codeforces.com/problemset/problem/333/D)

**Rating:** 2100  
**Tags:** binary search, bitmasks, brute force, implementation, sortings  
**Solve time:** 2m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of integers. From this grid we may cut away some rows from the top and bottom, and some columns from the left and right. After cropping, the remaining part must still be a rectangle with at least two rows and two columns.

For any chosen rectangle, its value is defined as the minimum among its four corner cells. We want the largest possible value over all valid cropped rectangles.

Another way to phrase the goal is this: choose two different rows and two different columns so that the minimum of the four intersection cells is as large as possible.

If we pick rows `r1 < r2` and columns `c1 < c2`, the rectangle value is

$$\min(a[r1][c1], a[r1][c2], a[r2][c1], a[r2][c2])$$

and we want to maximize this quantity.

The constraints are large enough to rule out direct brute force. Both dimensions can reach 1000, so there may be one million cells. Enumerating every possible rectangle already costs roughly

$$\binom{1000}{2}^2 \approx 2.5 \times 10^{11}$$

which is far beyond what fits into 3 seconds.

A useful observation is that the answer itself is a value from the matrix. That often suggests binary search on the answer. If we can quickly test whether there exists a rectangle whose four corners are all at least some threshold `x`, then we can binary search the maximum feasible `x`.

Several edge cases are easy to mishandle.

Consider this matrix:

```
2 2
5 1
1 5
```

The answer is `1`, not `5`. A careless approach might look only for large numbers independently, but all four corners must simultaneously satisfy the threshold.

Another subtle case is when a row contains many valid columns, but no second row shares two of them.

```
3 4
5 5 1 1
5 1 5 1
1 5 5 1
```

For threshold `5`, every row has two cells equal to `5`, but no pair of rows shares two common valid columns. The correct answer is `1`.

A minimum-size grid also matters:

```
2 2
7 8
9 10
```

No cropping is possible. The answer is simply the minimum corner value of the whole matrix, which is `7`.

## Approaches

The brute-force solution is conceptually simple. We choose every pair of rows and every pair of columns, compute the minimum of the four corner values, and keep the best answer.

There are about

$$\binom{n}{2} \cdot \binom{m}{2}$$

rectangles. With `n = m = 1000`, this becomes roughly `2.5 × 10^11` checks. Even though each check is constant time, the total work is completely infeasible.

The key observation is that for a fixed threshold `x`, the problem becomes boolean:

Can we find two rows and two columns such that all four corresponding cells are at least `x`?

If we convert the matrix into a binary matrix where

```
b[i][j] = 1 if a[i][j] >= x
```

then we only need to know whether there exists a `2 × 2` all-ones submatrix.

This changes the structure of the problem dramatically.

Suppose we process rows one by one. For each row, we look at all columns whose value is at least `x`. If some pair of columns `(c1, c2)` already appeared together in a previous row, then we have found two rows sharing two valid columns. Those four cells form a valid rectangle.

The monotonic property makes binary search possible. If threshold `x` works, then every smaller threshold also works. If `x` fails, every larger threshold fails as well.

The remaining challenge is implementing the feasibility test efficiently.

For each row, we collect all valid columns. Then we enumerate all pairs among them. There are at most

$$\binom{1000}{2} = 499500$$

possible column pairs overall, which is manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) | O(1) | Too slow |
| Optimal | O(nm log V + nm² / 64) practical, O(nm² log V) worst-case | O(m²) | Accepted |

Here `V` is the range of matrix values.

## Algorithm Walkthrough

1. Binary search the answer value.

The answer is between `0` and `10^9`, because every cell lies in this range. We binary search the largest threshold `x` for which a valid rectangle exists.
2. For a fixed threshold `x`, determine which cells are usable.

A cell is usable if its value is at least `x`. We only care about these cells because every corner must satisfy the threshold.
3. Process rows independently.

For each row, gather all column indices where the cell value is at least `x`.
4. Enumerate every pair of valid columns in the row.

If the current row contains valid columns `[c1, c2, c3]`, then the pairs are `(c1,c2)`, `(c1,c3)`, `(c2,c3)`.

Each pair means: this row can serve as one side of a rectangle whose corners all satisfy the threshold.
5. Store previously seen column pairs.

Use a boolean table or set to remember which column pairs have already appeared in earlier
