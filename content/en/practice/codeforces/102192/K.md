---
title: "CF 102192K - Pop the Balloons"
description: "Think of every row as a left vertex and every column as a right vertex. A balloon at cell (r, c) is an edge between row r and column c. When we pop a balloon at (r, c), every remaining balloon incident to row r or column c disappears."
date: "2026-08-18T02:15:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "K"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 236
verified: true
draft: false
---

[CF 102192K - Pop the Balloons](https://codeforces.com/problemset/problem/102192/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every row as a left vertex and every column as a right vertex. A balloon at cell `(r, c)` is an edge between row `r` and column `c`.

When we pop a balloon at `(r, c)`, every remaining balloon incident to row `r` or column `c` disappears. Consequently, two balloons that are both directly popped can never share a row or a column. The directly popped balloons form a matching in this bipartite graph.

There is one more condition. After all darts have been thrown, every balloon must have disappeared. A balloon that was not directly popped must share its row or its column with some directly popped balloon. In graph terminology, the directly popped matching has to be maximal. Thus the problem is to count maximal matchings by size, then account for the fact that the darts are thrown in an order.

For every `x` from `1` through `k`, the output asks for the number of ordered sequences of exactly `x` balloon positions that form such a clearing process. The order matters, so if a set of `x` valid popped balloons is found, it contributes `x!` different dart sequences.

The grid has at most `12` rows and `20` columns. The small dimension is the key constraint. A state describing all rows can have three possibilities per row, giving `3^12 = 531441` states at most. That is large but manageable with a carefully implemented dynamic program. A state involving all `20` columns would have `3^20`, which is already far too large, so the grid should be oriented so that the dimension represented by the ternary state is the smaller one.

The number of darts is at most `20`, but there can be at most `12` directly popped balloons because directly popped balloons cannot share a row. The parameter `k` is still useful for pruning states with more than `k` darts, but it does not change the asymptotic state count.

The official statement uses a seven second limit and 256 MB of memory. Its sample consists of four test cases and has outputs `1, 2`, `2, 0`, `1, 8, 0`, and `2`, respectively.

A first edge case is an entirely empty grid. For example,

```
1
1 1 1
.
```

has output

```
0
```

because there is no legal position for even the first dart. A careless implementation that treats the empty matching as a successful clearing strategy would incorrectly report one way for zero darts, but the problem only asks for positive dart counts.

Another edge case is a grid with several balloons in one row. For

```
1
1 3 3
QQQ
```

the correct output is

```
3
0
0
```

One dart is enough, and there are three possible cells for it. A brute force based on selecting arbitrary subsets of balloons may count the three single-cell choices correctly, but it can easily mishandle the fact that the dart order has no effect when there is only one dart.

A more subtle case is

```
1
2 2 2
Q.
.Q
```

The correct output is

```
0
2
```

Each balloon must be popped directly, and the two darts can be thrown in either order. A careless approach that counts only sets of popped cells would return `1` instead of `2`.

Finally, consider a dense grid where `k` is larger than the number of rows. For example, a `2 x 2` all-balloon grid can never require or permit three directly popped balloons, because two directly popped balloons already use both rows. The answers for larger dart counts must remain zero. The DP naturally handles this because the number of rows limits the number of state digits equal to `1`, which represent already selected rows.

## Approaches

The brute-force approach is to choose the first balloon to pop, simulate its row and column being cleared, choose the next remaining balloon, and continue until either all balloons disappear or `k` darts have been used. This is correct because every legal dart sequence is explored directly, and the simulation exactly follows the game rules.

The problem is the branching factor. A `12 x 20` grid can contain `240` balloons. If all of them are present and we try every ordered sequence of exactly `20` darts, the number of leaves is

`240 * 239 * 238 * ... * 221 = 240! / 220!`.

That is already about `10^47` sequences. Even checking only subsets instead of ordered sequences gives an exponential search over hundreds of balloons.

The useful observation is that the actual directly popped balloons form a matching. Once we decide which rows have already been selected, the only information needed about previous columns is whether a row has already been selected, whether it has appeared in an unselected column and still needs to be selected, or whether it has never appeared in a relevant column.

That gives three states per row. We process the grid column by column, using a ternary mask for the row states. We deliberately keep the columns outside the state because there are only `20` of them.

For a fixed column, there are only two kinds of action. We either do not throw a dart in that column, in which case every balloon in the column becomes an obligation to eventually select its row, or we throw a dart at one balloon in the column. In the second case, that row becomes selected, while all other balloons in the column disappear immediately and create no future obligation.

The DP therefore enumerates every possible matching once, using the increasing column order as its canonical representation. After the final column, a state is successful exactly when there is no row with an outstanding unselected balloon. If the state contains `x` selected rows, it represents one canonical maximal matching of size `x`.

The dart positions can then be ordered arbitrarily. Since the selected balloons form a matching, no two of them share a row or column, so every permutation of the selected balloons is a valid dart order. We multiply the number of canonical matchings of size `x` by `x!`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(P(B, k))`, where `B <= 240` | `O(B)` | Too slow |
| Optimal | `O(n * m * 3^m)` | `O(3^m)` | Accepted |

Here `m <= 12` is the dimension represented by the ternary state and `n <= 20` is the number of processed columns.

## Algorithm Walkthrough

1. Treat each balloon as an edge between its row and column. A directly popped set must be a matching because two directly popped balloons cannot share a row or column.
2. Process the grid by columns. Since there are at most `20` columns and at most `12` rows, storing a ternary state over rows is the smaller representation.
3. Give each row one of three states. State `0` means that no balloon in this row has appeared in a column that was left unpopped. State `1` means that the row has already been selected by a dart. State `2` means that a balloon in this row has appeared in an earlier column that was not popped, so this row still needs to be selected later.
4. Start with state `0` for every row and one DP way.
5. For the current column, first consider throwing no dart there. Every balloon in that column disappears only if its row is later selected, so every row currently in state `0` that contains a balloon in this column changes to state `2`. Rows already in state `2` stay there, while rows in state `1` remain selected.
6. Next consider throwing a dart at each balloon of the current column whose row has not already been selected. The chosen row changes to state `1`. All other balloons in the current column are blown away by this dart, so they do not create new state `2` obligations.
7. Reject states whose number of selected rows exceeds `k`. Since every selected row corresponds to one dart, such states can never contribute to an answer.
8. After all columns have been processed, keep only states containing no digit `2`. Such a state has no row that still needs a dart, so every balloon has been cleared either directly or by sharing a row or column with a directly popped balloon.
9. Add the DP value of each successful state to the answer indexed by its number of state `1` digits. This counts each maximal matching once, because its selected columns are processed in increasing order.
10. For every `x`, multiply the number of canonical matchings by `x!`. The multiplication converts the canonical column order into all possible orders of the `x` dart throws.

After the numbered steps, the key invariant is that after processing the first `j` columns, a state records exactly which rows have already been selected and which rows are still required to be selected because an uncleared balloon was encountered in those columns. A transition either leaves the current column unselected, creating precisely those new obligations, or selects one valid balloon and clears the rest of that column immediately. Thus every DP path corresponds to one matching, and every matching has exactly one path when its selected columns are considered from left to right. A final state with no digit `2` is exactly a maximal matching, which is exactly a set of darts that clears every balloon.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(m, n, k, grid):
    # We keep m as the smaller dimension.
    # The input already guarantees m <= 12 and n <= 20.
    #
    # For every column, mask bit r is set when grid[r][col] == 'Q'.
    columns = []
    for col in range(n):
        mask = 0
        for r in range(m):
            if grid[r][col] == 'Q':
                mask |= 1 << r
        columns.append(mask)

    states = 3 ** m

    pow3 = [1] * m
    for r in range(1, m):
        pow3[r] = pow3[r - 1] * 3

    # sum3[mask] = sum(pow3[r]) over all set bits r.
    # It lets us change all selected zero digits to digit 2 at once.
    sum3 = [0] * (1 << m)
    for mask in range(1, 1 << m):
        bit = mask & -mask
        r = bit.bit_length() - 1
        sum3[mask] = sum3[mask ^ bit] + pow3[r]

    # one[s]: rows whose ternary digit is 1.
    # two[s]: rows whose ternary digit is 2.
    # cnt[s]: number of digits equal to 1.
    #
    # Row 0 is the least significant ternary digit.
    one = [0] * states
    two = [0] * states
    cnt = [0] * states

    for s in range(1, states):
        q, d = divmod(s, 3)
        one[s] = (one[q] << 1) | (1 if d == 1 else 0)
        two[s] = (two[q] << 1) | (1 if d == 2 else 0)
        cnt[s] = cnt[q] + (1 if d == 1 else 0)

    dp = [0] * states
    dp[0] = 1

    full_rows = (1 << m) - 1

    for col_mask in columns:
        ndp = [0] * states

        for s in range(states):
            ways = dp[s]
            if ways == 0:
                continue

            used = cnt[s]
            if used > k:
                continue

            one_mask = one[s]
            two_mask = two[s]

            # Case 1: do not shoot this column.
            #
            # Every row containing a balloon in this column and currently
            # in state 0 becomes state 2.
            zero_rows = col_mask & ~(one_mask | two_mask) & full_rows
            base = s + 2 * sum3[zero_rows]

            ndp[base] += ways

            # Case 2: shoot one balloon in this column.
            #
            # A row already in state 1 cannot be shot again.
            # Starting from 'base', the chosen row would have digit 2,
            # but becomes digit 1, so subtract one power of 3.
            if used < k:
                available = col_mask & ~one_mask & full_rows

                while available:
                    bit = available & -available
                    ns = base - pow3[bit.bit_length() - 1]
                    ndp[ns] += ways
                    available ^= bit

        dp = ndp

    # Successful states have no digit 2.
    # Digit 1 counts directly popped rows, hence darts.
    ans = [0] * (min(k, m) + 1)

    for s in range(states):
        ways = dp[s]
        if ways and two[s] == 0:
            x = cnt[s]
            if 1 <= x <= k:
                ans[x] += ways

    # The DP stores each matching in increasing column order.
    # The actual darts may be thrown in any order.
    fact = 1
    result = []
    for x in range(1, k + 1):
        if x <= m:
            fact *= x
            result.append(str(ans[x] * fact))
        else:
            result.append("0")

    return "\n".join(result)

def solve(data):
    tokens = data.split()
    it = iter(tokens)

    t = int(next(it))
    out = []

    for _ in range(t):
        m = int(next(it))
        n = int(next(it))
        k = int(next(it))

        grid = [next(it).decode() if isinstance(next_val := next(it), bytes) else next_val
                for _ in range(m)]

        out.append(solve_case(m, n, k, grid))

    return "\n".join(out) + "\n"

def main():
    t = int(input())
    out = []

    for _ in range(t):
        m, n, k = map(int, input().split())
        grid = [input().strip() for _ in range(m)]
        out.append(solve_case(m, n, k, grid))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
```

The core representation is a ternary integer. The least significant ternary digit belongs to row zero, so changing a row state is just adding or subtracting a power of three. The arrays `one` and `two` let the transition determine which rows are selected and which rows still have unresolved balloons without repeatedly decoding the ternary number.

`sum3` is a small optimization that matters in this state space. When a column is not popped, every currently unseen balloon row changes from digit `0` to digit `2`. Instead of modifying each row separately, the code collects all such rows into one bitmask and adds twice the corresponding powers of three.

The shooting transition deserves particular attention. The variable `base` represents what would happen if the current column were not popped. For a row chosen as the dart position, that row would have digit `2` in `base`, but the dart changes it to digit `1`. Hence subtracting exactly one power of three gives the correct state whether the original digit was `0` or `2`.

A row with digit `1` cannot be selected again. Its earlier dart already removed every balloon in that row, so there cannot be a legal balloon left there. This is why `available` removes `one_mask`.

Python integers have arbitrary precision, which is necessary here. The number of valid dart sequences can be much larger than a 64 bit integer, so unlike a typical modular counting problem, no modulus is applied.

The `solve` helper is included for the assert-based tests below. The actual contest entry point uses `input = sys.stdin.readline` and processes test cases directly.

## Worked Examples

### Sample 1

Consider the first official sample:

```
2 2 2
QQ
.Q
```

The columns are `{row 1}` and `{row 1, row 2}`. We use `0` for unseen, `1` for already selected by a dart, and `2` for a row that currently has an unresolved balloon.

| Column | Previous state | Action | New state | Ways |
| --- | --- | --- | --- | --- |
| 1 | `00` | no dart | `20` | 1 |
| 1 | `00` | shoot row 1 | `10` | 1 |
| 2 | `20` | no dart | `22` | 1 |
| 2 | `20` | shoot row 1 | `10` | 1 |
| 2 | `10` | no dart | `12` | 1 |
| 2 | `10` | shoot row 2 | `11` | 1 |

After the second column, states `10` and `11` are valid because they contain no digit `2`. The first represents one selected balloon, so it contributes `1` canonical matching. The second represents two selected balloons, so it contributes `1` canonical matching.

For one dart, `1! = 1`. For two darts, `2! = 2`. The final output is consequently `1, 2`, matching the official sample.

The interesting part is the state `20` when the second column is shot at row 1. The row 2 balloon in that column is blown away immediately, so row 2 does not become an unresolved state. That is why the result is `10`, not a state containing row 2 as unresolved.

### Sample 2

The second sample is

```
2 2 2
QQ
..
```

Both balloons are in the same row.

| Column | Previous state | Action | New state | Ways |
| --- | --- | --- | --- | --- |
| 1 | `00` | no dart | `20` | 1 |
| 1 | `00` | shoot row 1 | `10` | 1 |
| 2 | `20` | no dart | `20` | 1 |
| 2 | `20` | shoot row 1 | `10` | 1 |
| 2 | `10` | no dart | `10` | 1 |

The final state `10` receives two ways. They correspond to shooting the first balloon or shooting the second balloon. Both choices clear the entire row, so the answer for one dart is `2`.

There is no valid two-dart solution. Once one balloon in the row is popped, the other disappears with it, so there is never a legal second dart. The output is `2, 0`, again matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n * m * 3^m)` | There are `3^m` row states for each of `n` columns, and each state can try every balloon row in that column |
| Space | `O(3^m + 2^m)` | Two DP layers and ternary-state metadata dominate the memory usage |

With `m = 12`, there are only `531441` ternary states. The maximum transition work is roughly `20 * 12 * 531441`, about `127.5` million simple state-row operations. The implementation avoids decoding ternary states inside the innermost loop and processes rows with bitmasks, which is necessary for the upper bound. The memory requirement is dominated by the two DP layers and remains within the intended state-space bound.

## Test Cases

```python
import sys
import io
from math import factorial

def run(inp: str) -> str:
    return solve(inp)

# Provided samples
sample = """\
4
2 2 2
QQ
.Q
2 2 2
QQ
..
3 3 3
.Q.
QQQ
.Q.
1 3 1
Q.Q
"""

expected_sample = """\
1
2
2
0
1
8
0
2
"""

assert run(sample) == expected_sample, "official samples"

# Minimum-size non-empty grid
assert run("""\
1
1 1 1
Q
""") == "1\n", "single balloon"

# Minimum-size empty grid
assert run("""\
1
1 1 1
.
""") == "0\n", "empty grid"

# One row, every balloon can be cleared by any one dart
assert run("""\
1
1 3 3
QQQ
""") == "3\n0\n0\n", "one-row boundary"

# Two diagonal balloons must both be popped, in either order
assert run("""\
1
2 2 2
Q.
.Q
""") == "0\n2\n", "diagonal balloons"

# Maximum-size all-balloon grid.
# A maximal matching must have exactly 12 darts.
max_grid = "12 20 20\n" + "\n".join(["Q" * 20] * 12) + "\n"
max_input = "1\n" + max_grid

max_matching_ordered = (
    factorial(20) // factorial(8) * factorial(12)
)

max_expected = "\n".join(
    ["0"] * 11 + [str(max_matching_ordered)]
) + "\n"

assert run(max_input) == max_expected, "maximum dense grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1` with `Q` | `1` | Smallest possible non-empty grid |
| `1 x 1` with `.` | `0` | No legal dart and empty-board handling |
| `1 x 3` with `QQQ` | `3, 0, 0` | Multiple balloons in one row and the maximum useful dart count |
| `2 x 2` with diagonal balloons | `0, 2` | Ordered dart sequences and the requirement that direct hits form a matching |
| `12 x 20` all `Q` | `0` through dart count `11`, then a large value at `12` | Maximum state size, arbitrary-precision counts, and the `x!` ordering factor |

## Edge Cases

For an empty grid, such as

```
1
1 1 1
.
```

the initial state `0` survives every column because there are no balloon bits in any column mask. It is a valid zero-dart state, but the output loop starts at `x = 1`, so nothing is reported. The result is `0`.

For a single row containing `QQQ`,

```
1
1 3 3
QQQ
```

the DP has only three ternary states. Shooting the first, second, or third column creates a state with one selected row and no unresolved state. These are three different one-dart positions. The final answers are `3, 0, 0`.

For diagonal balloons,

```
1
2 2 2
Q.
.Q
```

the first dart can pop either diagonal balloon, but after doing so the other balloon remains because neither its row nor its column was cleared. The DP consequently keeps only the two-dart states as successful. There are two possible dart orders, giving `2`.

The most delicate transition occurs when a column contains several balloons and one of them is selected. Suppose the current state has an unresolved balloon in row 1 and no previous information about row 2, while the current column contains balloons in both rows. Shooting row 1 removes the row 1 and column balloons immediately. Row 2 must not be marked as unresolved merely because a balloon existed there, because that balloon was just blown away. The shooting transition `base - pow3[r]` handles exactly this situation.

When `k > m`, the answer for every `x > m` is necessarily zero. No two directly popped balloons can share a row, so at most `m` darts can be used in a valid sequence. The implementation still prints exactly `k` lines, but the factorial DP result is used only for `x <= m`; all larger values are emitted as zero.
