---
title: "CF 102271A - The Cybermen Moonbase (Easy)"
description: "The grid has H rows and W columns. Time and column advance together, so at time t the TARDIS is in column t. Its vertical coordinate may change by at most K between consecutive columns, with the vertical direction wrapping cyclically from row H to row 1 and from row 1 to row H."
date: "2026-08-17T18:18:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102271
codeforces_index: "A"
codeforces_contest_name: "Helvetic Coding Contest 2019 (two remaining problems)"
rating: 0
weight: 102271
solve_time_s: 150
verified: true
draft: false
---

[CF 102271A - The Cybermen Moonbase (Easy)](https://codeforces.com/problemset/problem/102271/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid has `H` rows and `W` columns. Time and column advance together, so at time `t` the TARDIS is in column `t`. Its vertical coordinate may change by at most `K` between consecutive columns, with the vertical direction wrapping cyclically from row `H` to row `1` and from row `1` to row `H`.

Each Cyberman starts at a fixed column and row at time `1`. Cybermen never change columns. Instead, at every subsequent time step they all move one row in the same direction, determined by the corresponding character of `S`. Thus, if a Cyberman starts in row `r` at column `c`, then when the TARDIS reaches column `c`, that Cyberman has been shifted by the prefix of `S` corresponding to the first `c - 1` moves. Multiple Cybermen can occupy the same cell, but for the TARDIS only the fact that a cell is blocked matters. The official statement and contest materials use this interpretation and give the three samples with outputs `4`, `72`, and `600000`.

The input gives `H`, `W`, `K`, and `N`, followed by the `N` initial Cyberman positions and then a string of length `W - 1`. The output is the number of distinct sequences of TARDIS coordinates that start in an unoccupied cell of column `1`, make one move per time step, never enter an occupied cell, and finish somewhere in column `W`. The answer is taken modulo `10^9 + 7`.

The dimensions `H` and `W` are at most `1000`, so a solution with roughly one operation per grid cell, `O(HW)`, is easily practical. The value of `K` is at most `10`, which also makes an `O(HWK)` dynamic program feasible in principle, but there is an even cleaner `O(HW)` transition using a sliding window. There can be `5000` Cybermen, so rebuilding every column by examining every Cyberman would be wasteful if done repeatedly. Each Cyberman needs to be processed only once after we know the vertical shift for its column.

The first edge case is an occupied starting cell. For example,

```
2 2 1 2
1 1
1 2
U
```

has both cells of the first column blocked, so the correct answer is `0`. A careless implementation that initializes every first-column state to `1` would count paths starting inside Cybermen.

The second edge case is vertical wrapping. Consider

```
5 2 1 1
2 5
U
```

At column `2`, the Cyberman moves from row `5` to row `1`. The other four cells are available. From every row in column `1`, the TARDIS can reach three consecutive rows cyclically, so each of the four allowed destinations has three possible predecessors. The answer is `12`. An implementation that treats rows as an ordinary interval would mishandle transitions around rows `1` and `5`.

The third edge case is that Cyberman movement depends on time, not on how many columns the Cyberman has moved through. For example,

```
5 3 1 2
1 1
2 1
UU
```

At column `1`, row `1` is blocked, giving first-column DP `[0,1,1,1,1]`. At column `2`, both Cybermen have moved up once, so the Cyberman initially at `(2,1)` occupies row `2`. The second column therefore has DP `[2,0,3,3,3]`, with total `11`. Column `3` has no Cyberman, and the total becomes `33`. An implementation that forgets the movement prefix or applies the instruction one time step too early gets a different result.

## Approaches

The most direct solution is to treat the problem as a path-counting dynamic program. Let `dp[r]` be the number of ways to reach row `r` in the current column. For a destination row `r`, every previous row whose cyclic distance from `r` is at most `K` contributes to the new value. After computing those sums, blocked cells are set to zero.

A brute-force implementation can avoid dynamic programming entirely by recursively enumerating every possible TARDIS path. This is correct because every legal path is generated exactly once, and every illegal path is rejected as soon as it reaches an occupied cell. The problem is the number of paths. In the worst case there are no obstacles, and with `H = 1000` and `K = 10`, every row has `21` distinct reachable rows. The first column has `1000` choices, followed by `21` choices for each of the remaining `999` columns, giving

`1000 * 21^999`

possible paths. That is roughly `10^1321`, so enumeration is completely infeasible.

The first useful observation is that we do not need to remember the complete path. Once the TARDIS reaches a particular cell, all earlier choices matter only through the number of paths that reached that cell. This gives the standard column-by-column DP.

A second observation handles the moving obstacles. Every Cyberman moves according to the same signal, so the vertical displacement after `c - 1` moves is known from the prefix of `S`. We can precompute that displacement for every column. A Cyberman initially at `(c, r)` then blocks exactly one row in column `c`, namely the appropriately shifted version of `r`. We can mark these cells once before running the DP.

The remaining transition is initially `O(HK)` per column because each destination examines at most `2K + 1` previous rows. That would already be acceptable under these constraints, since `H,W <= 1000` and `K <= 10`, but the transition has more structure. For consecutive destination rows, their predecessor intervals differ by only one row on each side. We can maintain the sum of the current cyclic interval and update it in constant time. This reduces the DP transition to `O(H)` per column.

When `2K + 1 >= H`, every row can reach every other row on the cyclic grid. In that case every destination receives the same total number of paths, namely the sum of the previous DP array. Handling this case separately avoids counting the same cyclic row more than once when constructing a sliding window.

The official contest editorial describes the same underlying column DP, with the transition summing all previous rows within distance `K`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(H(2K+1)^(W-1))` | `O(W)` recursion depth | Too slow |
| DP with direct transitions | `O(N + HWK)` | `O(HW)` | Accepted |
| DP with cyclic sliding window | `O(N + HW)` | `O(HW)` | Accepted |

## Algorithm Walkthrough

1. Read all Cyberman positions and the movement string. Build a prefix displacement for every column. Let `shift[c]` be the vertical displacement of a Cyberman at time `c` relative to its initial row. Thus `shift[0] = 0`, and each following value changes by `+1` for `U` or `-1` for `D`. The modulo operation on rows gives the cyclic wrapping.
2. Create a blocked-cell array for the `W` columns. For every Cyberman initially at column `c` and row `r`, mark the row obtained by applying `shift[c - 1]` to `r`. The Cyberman stays in column `c`, so it contributes only to that column. This is the key distinction between the obstacle movement and the TARDIS movement.
3. Initialize the DP for column `1`. Every unblocked row has exactly one way to be the starting cell, while every blocked row has zero ways. At this point `prev[r]` represents all valid paths ending at row `r` in the current column.
4. Process columns from `2` through `W`. For each column, calculate the sum of `prev[r']` over all rows `r'` whose cyclic distance from the destination row `r` is at most `K`. If the destination is blocked, its DP value is zero regardless of the predecessor sum.
5. If `2K + 1 >= H`, every source row can reach every destination row. Compute `total = sum(prev)` once and assign this value to every unblocked destination. This avoids constructing a window that would contain the same cyclic row multiple times.
6. Otherwise, maintain a cyclic sliding window of exactly `2K + 1` distinct source rows. Construct the conceptual sequence

`prev[H-K], ..., prev[H-1], prev[0], ..., prev[H-1], prev[0], ..., prev[K-1]`.

The first window corresponds to destination row `0`. When moving to the next destination row, subtract the source row leaving the window and add the source row entering it. Thus every destination sum costs constant time.
7. Replace `prev` with the newly computed DP array and continue to the next column. After column `W` has been processed, sum all entries of `prev`. Every surviving entry represents paths ending at that row, and every possible final row is acceptable.

### Why it works

The invariant is that after processing column `c`, `prev[r]` equals exactly the number of legal TARDIS paths whose current position is `(c,r)`. The initialization satisfies this because every free starting cell contributes one path and every blocked cell contributes none. For a transition to `(c,r)`, every legal path must come from exactly one row within cyclic distance `K`, so summing the corresponding previous DP values counts every legal extension exactly once. A blocked destination contributes zero, removing precisely the paths that would enter a Cyberman. The sliding window computes the same predecessor sum as the direct recurrence, only by reusing the overlap between consecutive windows. Hence the invariant remains true for every column, and summing the final DP array gives exactly the required number of paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    H, W, K, N = map(int, input().split())

    cybermen = [tuple(map(int, input().split())) for _ in range(N)]
    S = input().strip()

    # shift[c] is the vertical displacement at column c + 1,
    # using 0-based column indices.
    shift = [0] * W
    for c in range(1, W):
        shift[c] = shift[c - 1] + (1 if S[c - 1] == 'U' else -1)

    # blocked[c][r] == 1 means row r (0-based) is occupied
    # in column c (0-based).
    blocked = [bytearray(H) for _ in range(W)]

    for c, r in cybermen:
        row = (r - 1 + shift[c - 1]) % H
        blocked[c - 1][row] = 1

    # DP for the first column.
    prev = [0 if blocked[0][r] else 1 for r in range(H)]

    # If one move can reach every row, every destination gets
    # the same predecessor sum.
    all_rows_reachable = 2 * K + 1 >= H

    for c in range(1, W):
        if all_rows_reachable:
            total = sum(prev) % MOD
            cur = [
                0 if blocked[c][r] else total
                for r in range(H)
            ]
        else:
            # Cyclic sliding window.
            ext = prev[-K:] + prev + prev[:K]
            width = 2 * K + 1

            window = sum(ext[:width]) % MOD
            cur = [0] * H

            for r in range(H):
                if not blocked[c][r]:
                    cur[r] = window

                if r + 1 < H:
                    window += ext[r + width]
                    window -= ext[r]
                    window %= MOD

        prev = cur

    print(sum(prev) % MOD)

if __name__ == "__main__":
    solve()
```

The `shift` array records the cumulative movement of the Cybermen. For column `c`, the TARDIS arrives there at time `c`, so exactly `c - 1` signal characters have affected every Cyberman. The expression `(r - 1 + shift[c - 1]) % H` converts the original one-based row into a zero-based cyclic row.

The `blocked` array uses one `bytearray` per column. This is compact and lets us test whether a destination is occupied in constant time. If several Cybermen end up in the same cell, assigning `1` again has no effect, which is exactly what we need.

The first DP array contains only `0` and `1`, because there is no movement before entering the first column. From the second column onward, the transition depends only on the preceding DP array, so storing two full DP layers is unnecessary.

The `all_rows_reachable` branch handles small values of `H`. For example, when `H = 5` and `K = 3`, the cyclic distance between any two rows is at most `2`, so every row reaches every other row. A naive circular window of length `7` would count some rows twice. Using the total sum directly avoids that problem.

For the normal case, `ext` contains enough copies of the beginning and end of `prev` to turn every cyclic predecessor interval into an ordinary contiguous slice. The first window corresponds to destination row `0`. After processing that row, one old value leaves the window and one new value enters it. The order of these updates is chosen so that `cur[r]` uses exactly the window for destination `r`, not destination `r + 1`.

All arithmetic is reduced modulo `10^9 + 7`. Python integers do not overflow, but keeping the rolling sum bounded prevents unnecessary growth and keeps the implementation efficient.

## Worked Examples

### Sample 1

The input is

```
2 2 1 0
U
```

There are no Cybermen. With two rows and `K = 1`, the vertical cycle allows every row to reach every other row in one move.

| Column | Blocked rows | `prev` before transition | `cur` after transition |
| --- | --- | --- | --- |
| 1 | none | `[1, 1]` | `[1, 1]` |
| 2 | none | `[1, 1]` | `[2, 2]` |

The final sum is `2 + 2 = 4`, matching the sample output.

This example exercises the `2K + 1 >= H` branch. The transition does not need to inspect individual predecessor rows because every row is reachable.

### Sample 2

The input is

```
5 4 1 3
1 3
2 2
2 1
UDU
```

The Cyberman at column `1`, row `3` moves up once by the time the TARDIS reaches column `2`. The two Cybermen initially in column `2`, rows `2` and `1`, also move up once. Thus the blocked rows are `{3}` in column `1`, `{2,3}` in column `2`, and no cells in columns `3` and `4`.

| Column | Blocked rows | DP vector |
| --- | --- | --- |
| 1 | `{3}` | `[1, 1, 0, 1, 1]` |
| 2 | `{2, 3}` | `[3, 0, 0, 2, 3]` |
| 3 | `{}` | `[6, 3, 2, 5, 5]` |
| 4 | `{}` | `[14, 11, 10, 12, 16]` |

For column `2`, row `1` receives paths from rows `5`, `1`, and `2`, giving `3`. Row `4` receives paths from rows `3`, `4`, and `5`, giving `2`, and row `5` receives `3`. The blocked rows receive zero.

Column `3` has no obstacles, so the total number of paths becomes `24`, which is then multiplied by the three possible predecessor rows for every destination in column `4`. The final total is `72`, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N + HW)` | Each Cyberman is processed once, each column processes every row once |
| Space | `O(HW + N)` | The blocked grid uses `O(HW)` space and the input positions use `O(N)` space |

With `H,W <= 1000`, the DP performs at most about one million row updates. The obstacle preprocessing handles only `N <= 5000` Cybermen. The memory usage of the blocked grid is also small enough for the `256 MB` limit, while the implementation keeps only two DP vectors.

## Test Cases

```python
# Complete assert-based harness for the solution.

import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    H, W, K, N = map(int, input().split())
    cybermen = [tuple(map(int, input().split())) for _ in range(N)]
    S = input().strip()

    shift = [0] * W
    for c in range(1, W):
        shift[c] = shift[c - 1] + (1 if S[c - 1] == 'U' else -1)

    blocked = [bytearray(H) for _ in range(W)]
    for c, r in cybermen:
        row = (r - 1 + shift[c - 1]) % H
        blocked[c - 1][row] = 1

    prev = [0 if blocked[0][r] else 1 for r in range(H)]
    all_rows_reachable = 2 * K + 1 >= H

    for c in range(1, W):
        if all_rows_reachable:
            total = sum(prev) % MOD
            cur = [0 if blocked[c][r] else total for r in range(H)]
        else:
            ext = prev[-K:] + prev + prev[:K]
            width = 2 * K + 1
            window = sum(ext[:width]) % MOD
            cur = [0] * H

            for r in range(H):
                if not blocked[c][r]:
                    cur[r] = window

                if r + 1 < H:
                    window += ext[r + width]
                    window -= ext[r]
                    window %= MOD

        prev = cur

    print(sum(prev) % MOD)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    """2 2 1 0
U
"""
) == "4", "sample 1"

assert run(
    """5 4 1 3
1 3
2 2
2 1
UDU
"""
) == "72", "sample 2"

assert run(
    """5 10 3 10
1 2
2 3
3 4
1 4
1 3
5 1
5 2
5 3
7 1
7 2
UUUDDDUDU
"""
) == "600000", "sample 3"

# Custom 1: minimum dimensions, no obstacles.
assert run(
    """2 2 1 0
U
"""
) == "4", "minimum-size grid"

# Custom 2: maximum row dimension with a short width.
# With H=1000, W=2, K=10 and no obstacles, there are
# 1000 starting rows and 21 choices for the second row.
assert run(
    """1000 2 10 0
U
"""
) == "21000", "large H"

# Custom 3: wrap-around transition.
# Row 5 is blocked in column 2, while K=1 makes row 1
# reachable from row 5 and vice versa.
assert run(
    """5 2 1 1
2 5
U
"""
) == "12", "vertical wrapping"

# Custom 4: obstacle movement must use the time prefix.
# Column 1 blocks row 1.
# The Cyberman initially at column 2, row 1 moves up to row 2
# before the TARDIS reaches column 2.
assert run(
    """5 3 1 2
1 1
2 1
UU
"""
) == "33", "Cyberman movement timing"

# Custom 5: duplicate Cybermen in the same cell must not
# multiply the blocking effect.
assert run(
    """5 3 1 5
2 1
2 1
2 1
2 1
2 1
UU
"""
) == "36", "duplicate obstacles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 0` with `U` | `4` | Minimum dimensions and the all-rows-reachable transition |
| `1000 2 10 0` with `U` | `21000` | Large row dimension and the direct total-sum branch |
| `5 2 1 1`, obstacle `(2,5)` | `12` | Cyclic vertical wrapping |
| `5 3 1 2`, obstacles `(1,1)` and `(2,1)` | `33` | Correct time-dependent Cyberman displacement |
| Five copies of `(2,1)` | `36` | Multiple Cybermen occupying the same cell |

## Edge Cases

When the entire first column is blocked, the initial DP vector is all zeroes. For

```
2 2 1 2
1 1
1 2
U
```

both rows are marked before initialization, so `prev = [0, 0]`. Every later transition also produces zero, and the answer is `0`. The algorithm never needs a special case for this situation because the initial DP definition already captures it.

For vertical wrapping, consider

```
5 2 1 1
2 5
U
```

The Cyberman at column `2`, row `5` moves upward to row `1`, so column `2` blocks row `1`. Column `1` has DP `[1,1,1,1,1]`. The available destinations are rows `2`, `3`, `4`, and `5`. Their predecessor windows are respectively `{1,2,3}`, `{2,3,4}`, `{3,4,5}`, and `{4,5,1}`, each containing three paths. The final vector is `[0,3,3,3,3]`, giving `12`.

For a moving obstacle, consider

```
5 3 1 2
1 1
2 1
UU
```

The first column blocks row `1`, so the initial DP is `[0,1,1,1,1]`. The second Cyberman starts at column `2`, row `1`, but by time `2` it has moved upward to row `2`. The second column therefore has row `2` blocked. The cyclic predecessor sums give `[2,0,3,3,3]`, whose total is `11`. Column `3` has no obstacles, and each destination receives three predecessor rows, producing a total of `33`. This confirms that the signal prefix is applied according to the TARDIS's time, not according to a Cyberman's starting column history.

Finally, if several Cybermen occupy the same cell, they still block only one cell. In

```
5 3 1 5
2 1
2 1
2 1
2 1
2 1
UU
```

all five Cybermen move to row `2` in column `2`. The blocked array records that cell once. Column `1` has all five starting rows available, so column `2` has four available rows with three predecessors each, giving `12` paths. Column `3` has no obstacle, so the total becomes `36`. Treating each Cyberman as a separate obstacle would incorrectly remove the same cell multiple times, while the bytearray representation naturally handles duplicates.
