---
title: "CF 274B - Zero Tree"
description: "This problem asks whether a matrix returns to its original form after repeatedly applying cyclic row shifts. The matrix has m rows and n columns. Every operation affects all rows simultaneously, but the direction depends on the row index."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 274
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 168 (Div. 1)"
rating: 1800
weight: 274
solve_time_s: 208
verified: true
draft: false
---

[CF 274B - Zero Tree](https://codeforces.com/problemset/problem/274/B)

**Rating:** 1800  
**Tags:** dfs and similar, dp, greedy, trees  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem asks whether a matrix returns to its original form after repeatedly applying cyclic row shifts. The matrix has `m` rows and `n` columns. Every operation affects all rows simultaneously, but the direction depends on the row index.

Rows with even indices, such as `0`, `2`, and `4`, are shifted one position to the left. Rows with odd indices, such as `1`, `3`, and `5`, are shifted one position to the right. These shifts are cyclic, meaning elements that move past one end wrap around to the opposite side.

The operation is repeated exactly `k` times. After all shifts are complete, we must determine whether the resulting matrix is identical to the original matrix.

The constraints are very small. Both dimensions are at most `25`, and `k` is at most `50`. Even a direct simulation would fit comfortably within the limits. Still, the problem becomes cleaner if we recognize the mathematical behavior of cyclic shifts.

The key observation is that shifting a row by `n` positions restores the row to its original state because the row length is `n`. This means only `k % n` actually matters. If the effective shift amount is zero, every row returns immediately. Otherwise, each row must be checked carefully.

Several edge cases are easy to mishandle.

A matrix with only one column always remains unchanged because shifting a single element cyclically does nothing. For example:

```
[[5],
 [7],
 [9]]
```

No matter how many operations are applied, the matrix never changes.

Another tricky case occurs when rows contain repeated patterns. A row may return to its original arrangement even when the shift amount is nonzero. For example:

```
[1, 2, 1, 2]
```

A left shift by `2` produces the same row again.

A final edge case is when all values in a row are equal. Any cyclic shift leaves the row unchanged:

```
[5, 5, 5, 5]
```

A naive implementation that assumes every nonzero shift changes the row would fail here.

## Approaches

The most direct approach is brute-force simulation. We can perform the operation exactly `k` times. During each operation, we shift every even-indexed row left by one and every odd-indexed row right by one. After all operations finish, we compare the final matrix with the original matrix.

This works because the operations are defined explicitly, and simulation exactly follows the problem statement. The issue is that repeated shifting performs unnecessary work. Every row eventually repeats after `n` shifts because cyclic rotations wrap around.

Suppose a row has length `n`. Shifting left by `n` positions produces the same row again. The same is true for right shifts. This means performing `k` individual operations is equivalent to performing a single shift of size:

```
k % n
```

Once we recognize this, we no longer need repeated simulation. For each row, we can directly compute the row after the effective shift and compare it with the original row.

For even-indexed rows, a left shift by `shift` positions transforms:

```
row[i] -> row[(i + shift) % n]
```

For odd-indexed rows, a right shift by `shift` positions transforms:

```
row[i] -> row[(i - shift + n) % n]
```

If every transformed row matches the original row, the answer is `true`. Otherwise, it is `false`.

| Approach | Time Complexity | Space Complexity | Notes |
| --- | --- | --- | --- |
| Brute Force | O(m × n × k) | O(n) | Simulates every operation directly |
| Optimal | O(m × n) | O(1) or O(n) | Uses cyclic shift periodicity |

## Algorithm Walkthrough

1. Compute the number of columns `n` and reduce the shift amount using:

```
shift = k % n
```

A cyclic shift repeats every `n` operations, so larger values of `k` are redundant.
2. Iterate through every row of the matrix.

The row index determines the shift direction.
3. For even-indexed rows, simulate a left cyclic shift logically.

For each column `j`, the value after shifting comes from:

```
row[(j + shift) % n]
```

Compare this directly against the original value at position `j`.
4. For odd-indexed rows, simulate a right cyclic shift logically.

For each column `j`, the shifted value comes from:

```
row[(j - shift + n) % n]
```

Again, compare it directly with the original value at position `j`.
5. If any value differs, return `False` immediately.

One mismatch is enough to prove the matrix changed.
6. If all rows match after checking every element, return `True`.

### Why it works

Cyclic shifts form a repeating cycle of length `n`. Performing `k` shifts is exactly equivalent to performing `k % n` shifts. The algorithm checks the exact element that would appear in every position after the final shift. Since every cell is verified against its original value, the algorithm correctly determines whether the matrix remains unchanged.

## Python Solution

```
from typing import List

class Solution:
    def areSimilar(self, mat: List[List[int]], k: int) -> bool:
        rows = len(mat)
        cols = len(mat[0])

        shift = k % cols

        for row_index in range(rows):
            row = mat[row_index]

            for col in range(cols):
                if row_index % 2 == 0:
                    shifted_value = row[(col + shift) % cols]
                else:
                    shifted_value = row[(col - shift + cols) % cols]

                if shifted_value != row[col]:
                    return False

        return True
```

The implementation starts by computing the effective shift amount using modulo arithmetic. This removes unnecessary repeated rotations.

The outer loop processes each row independently. Since even and odd rows move in opposite directions, the code branches based on the row index parity.

Instead of physically constructing shifted rows, the algorithm computes where each value would come from after shifting. This keeps the implementation simple and avoids extra memory allocations.

The moment a mismatch appears, the function returns `False`. Early termination avoids unnecessary work once the answer is already known.

If all positions match successfully, the matrix remains unchanged after all operations, so the function returns `True`.

## Go Solution

```
func areSimilar(mat [][]int, k int) bool {
    rows := len(mat)
    cols := len(mat[0])

    shift := k % cols

    for r := 0; r < rows; r++ {
        row := mat[r]

        for c := 0; c < cols; c++ {
            var shiftedValue int

            if r%2 == 0 {
                shiftedValue = row[(c+shift)%cols]
            } else {
                shiftedValue = row[(c-shift+cols)%cols]
            }

            if shiftedValue != row[c] {
                return false
            }
        }
    }

    return true
}
```

The Go implementation follows the same logic as the Python version. Since Go arrays are represented using slices, indexing remains straightforward.

One small detail is handling negative indices for right shifts. The expression:

```
(c - shift + cols) % cols
```

ensures the index always remains nonnegative before taking modulo.

Integer overflow is not a concern because all values and dimensions are very small.

## Worked Examples

### Example 1

Input:

```
mat = [
  [1,2,3],
  [4,5,6],
  [7,8,9]
]
k = 4
```

The number of columns is `3`.

Effective shift:

```
shift = 4 % 3 = 1
```

#### Row 0, even-indexed, left shift by 1

| Position | Original | Shifted Source | Shifted Value |
| --- | --- | --- | --- |
| 0 | 1 | row[1] | 2 |
| 1 | 2 | row[2] | 3 |
| 2 | 3 | row[0] | 1 |

The shifted row becomes:

```
[2,3,1]
```

This differs from the original row immediately, so the algorithm returns `False`.

### Example 2

Input:

```
mat = [
  [1,2,1,2],
  [5,5,5,5],
  [6,3,6,3]
]
k = 2
```

Number of columns:

```
4
```

Effective shift:

```
2 % 4 = 2
```

#### Row 0, even-indexed

Original row:

```
[1,2,1,2]
```

Left shift by `2`:

```
[1,2,1,2]
```

The row matches.

#### Row 1, odd-indexed

Original row:

```
[5,5,5,5]
```

Right shift by `2`:

```
[5,5,5,5]
```

Still identical.

#### Row 2, even-indexed

Original row:

```
[6,3,6,3]
```

Left shift by `2`:

```
[6,3,6,3]
```

All rows match, so the algorithm returns `True`.

### Example 3

Input:

```
mat = [
  [2,2],
  [2,2]
]
k = 3
```

Number of columns:

```
2
```

Effective shift:

```
3 % 2 = 1
```

Every row contains identical values, so shifting changes nothing.

The algorithm checks all positions successfully and returns `True`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m × n) | Every cell is checked once |
| Space | O(1) | Only a few variables are used |

The algorithm performs a constant amount of work per matrix cell. Since the matrix contains at most `25 × 25 = 625` elements, the solution easily fits within the limits.

## Test Cases

```
from typing import List

class Solution:
    def areSimilar(self, mat: List[List[int]], k: int) -> bool:
        rows = len(mat)
        cols = len(mat[0])

        shift = k % cols

        for row_index in range(rows):
            row = mat[row_index]

            for col in range(cols):
                if row_index % 2 == 0:
                    shifted_value = row[(col + shift) % cols]
                else:
                    shifted_value = row[(col - shift + cols) % cols]

                if shifted_value != row[col]:
                    return False

        return True

sol = Solution()

assert sol.areSimilar(
    [[1,2,3],[4,5,6],[7,8,9]],
    4
) == False  # provided example 1

assert sol.areSimilar(
    [[1,2,1,2],[5,5,5,5],[6,3,6,3]],
    2
) == True  # provided example 2

assert sol.areSimilar(
    [[2,2],[2,2]],
    3
) == True  # provided example 3

assert sol.areSimilar(
    [[1]],
    100
) == True  # single cell matrix

assert sol.areSimilar(
    [[1,2,3,4]],
    4
) == True  # full cycle returns original

assert sol.areSimilar(
    [[1,2,3,4]],
    1
) == False  # nontrivial left shift

assert sol.areSimilar(
    [[5,5,5],[1,2,3]],
    3
) == True  # shift equal to row length

assert sol.areSimilar(
    [[1,2,1,2]],
    2
) == True  # repeating pattern survives shift

assert sol.areSimilar(
    [[1],[2],[3]],
    50
) == True  # single-column matrix always unchanged
```

| Test | Why |
| --- | --- |
| `[[1,2,3],[4,5,6],[7,8,9]], k=4` | Verifies normal mismatch case |
| `[[1,2,1,2],[5,5,5,5],[6,3,6,3]], k=2` | Verifies repeating patterns |
| `[[2,2],[2,2]], k=3` | Verifies all-equal values |
| `[[1]], k=100` | Tests smallest possible matrix |
| `[[1,2,3,4]], k=4` | Tests full-cycle rotation |
| `[[1,2,3,4]], k=1` | Tests nontrivial shift |
| `[[5,5,5],[1,2,3]], k=3` | Tests modulo reduction |
| `[[1,2,1,2]], k=2` | Tests periodic row structure |
| `[[1],[2],[3]], k=50` | Tests single-column behavior |

## Edge Cases

A single-column matrix is a subtle special case because cyclic shifts do nothing when there is only one element. A careless implementation might still attempt index manipulation and accidentally introduce errors. For example:

```
[[1],
 [2],
 [3]]
```

Any value of `k` produces the same matrix. The implementation handles this naturally because:

```
shift = k % 1 = 0
```

Every lookup maps back to the same index.

Rows with repeated periodic patterns are another important case. Consider:

```
[1,2,1,2]
```

A left shift by `2` restores the original row exactly. An incorrect implementation might assume any nonzero shift changes the row. The algorithm instead compares the actual shifted positions element by element, so it correctly recognizes the equality.

Rows containing identical values can also expose logical mistakes. For example:

```
[5,5,5,5]
```

Every cyclic rotation is identical to the original row. Since the implementation computes shifted values directly and compares contents rather than shift counts, it correctly returns `True`.

Finally, large values of `k` could lead to unnecessary repeated simulation. For example:

```
k = 10^9
```

Even though the problem constraints are small, the optimal solution avoids this inefficiency completely by reducing the shift using modulo arithmetic:

```
k % cols
```

This guarantees only the effective rotation amount matters.
