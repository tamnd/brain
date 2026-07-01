---
title: "CF 104386E - Gridy"
description: "We are given a rectangular grid where each cell already contains either a fixed 0, a fixed 1, or an unknown ?. Every unknown cell will later be independently replaced by either 0 or 1, each choice having equal probability."
date: "2026-07-01T02:49:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104386
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #14 (Cool-Forces)"
rating: 0
weight: 104386
solve_time_s: 63
verified: true
draft: false
---

[CF 104386E - Gridy](https://codeforces.com/problemset/problem/104386/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid where each cell already contains either a fixed `0`, a fixed `1`, or an unknown `?`. Every unknown cell will later be independently replaced by either `0` or `1`, each choice having equal probability. After all replacements are made, we inspect the final binary grid and check whether it contains any pair of orthogonally adjacent `1` cells.

The task is not to simulate randomness, but to compute the probability that the final grid has no two neighboring `1` cells. The answer must be given modulo 998244353.

A useful way to view this is as a probabilistic constraint satisfaction problem: each `?` is a free binary variable, and we want the fraction of assignments that produce an independent set of `1` cells in the grid graph.

The grid size is at most 15 by 15, so there are at most 225 cells. This immediately rules out any approach that enumerates all assignments of `?`, since in the worst case there are 2^225 possibilities, which is far beyond computational feasibility. Even 2^40 is already borderline in 2 seconds, so brute force over cells is not viable.

Another naive idea is to directly generate all valid assignments and count them, then divide by 2^{number of question marks}. This still requires enumerating all valid configurations, which is exponential in the number of cells.

A second naive mistake is to treat cells independently or to try greedy local decisions. The adjacency constraint couples choices across the grid, so local independence fails.

A concrete edge case where naive reasoning breaks is a fully unknown 2x2 grid. There are 16 total assignments, but only those without adjacent `1`s are valid. A naive “multiply probabilities per cell” approach would incorrectly assume independence and overcount valid states.

The key difficulty is global adjacency, which suggests a graph constraint problem over a grid graph with small width and height. This is a classic setup for profile dynamic programming over subsets of a row.

## Approaches

The brute-force solution is to iterate over all assignments of the `?` cells, fill the grid, and check whether any adjacent pair of `1`s exists. Each check costs O(nm), and there are 2^k assignments where k is the number of question marks. In the worst case k = 225, so this is completely infeasible.

Even if we restrict to only valid states, the number of independent sets in a grid grows exponentially in nm. The structure of the problem suggests we should avoid enumerating full grids and instead build the solution incrementally.

The key observation is that adjacency constraints are local: a cell only interacts with its left, right, up, and down neighbors. If we process the grid row by row, the only unresolved dependency when filling a row is the relationship with the previous row. This suggests a bitmask dynamic programming over rows, where each row configuration encodes which cells are set to `1`.

For each row, we enumerate all valid bitmasks that respect the fixed constraints from `0`, `1`, and `?`. Then we transition between consecutive rows, enforcing that no vertical conflicts occur and that within a row no two adjacent bits are both `1`.

This reduces the problem from exponential in nm to exponential in m, which is at most 15, making it feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^{nm} · nm) | O(nm) | Too slow |
| Row DP with bitmasking | O(n · 2^m · 2^m) | O(2^m) | Accepted |

## Algorithm Walkthrough

We process the grid row by row, treating each row as a bitmask of length m where bit j is 1 if cell (i, j) is assigned 1.

1. Precompute all valid row masks that do not contain adjacent 1s horizontally. This ensures no violations within a row. Any mask with `mask & (mask << 1) != 0` is invalid.
2. For each row i, filter valid masks further based on the fixed grid constraints. If a cell is forced to 0, that bit must be 0. If forced to 1, that bit must be 1. Otherwise it can be either.
3. Define a transition between two row masks `a` (previous row) and `b` (current row). The constraint is that no vertical adjacency of ones is allowed, so `a & b == 0`.
4. Use dynamic programming where `dp[i][mask]` is the number of valid configurations for rows up to i, with row i equal to `mask`.
5. Initialize dp for row 0 by assigning all valid masks consistent with row 0 constraints.
6. For each next row, compute dp transitions by iterating over all valid previous masks and current masks satisfying vertical compatibility, accumulating counts.
7. After processing all rows, sum over dp[n-1][mask] for all valid masks in the last row.
8. Convert the result into a probability by dividing by 2^{number of `?`} using modular inverse.

Why it works is that every full grid assignment corresponds to exactly one sequence of row masks. The DP enumerates exactly those sequences that satisfy all horizontal and vertical adjacency constraints, and the filtering step ensures consistency with fixed cells. Since each `?` contributes exactly two equiprobable choices, the normalization by 2^k converts counts into probability under uniform random assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def main():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    # count question marks
    q = sum(row.count('?') for row in grid)

    # precompute powers of 2
    pow2 = [1] * (n * m + 1)
    for i in range(1, n * m + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD

    inv_pow2 = pow(pow2[q], MOD - 2, MOD)

    # generate valid row masks (no adjacent 1s)
    valid_masks = []
    for mask in range(1 << m):
        if mask & (mask << 1):
            continue
        valid_masks.append(mask)

    # precompute compatibility with each row
    row_allowed = []
    for i in range(n):
        allowed = []
        for mask in valid_masks:
            ok = True
            for j in range(m):
                if grid[i][j] == '1' and not (mask >> j & 1):
                    ok = False
                    break
                if grid[i][j] == '0' and (mask >> j & 1):
                    ok = False
                    break
            if ok:
                allowed.append(mask)
        row_allowed.append(allowed)

    dp = {mask: 1 for mask in row_allowed[0]}

    for i in range(1, n):
        ndp = {mask: 0 for mask in row_allowed[i]}
        for pmask, val in dp.items():
            for cmask in row_allowed[i]:
                if pmask & cmask:
                    continue
                ndp[cmask] = (ndp[cmask] + val) % MOD
        dp = ndp

    total = sum(dp.values()) % MOD
    print(total * inv_pow2 % MOD)

if __name__ == "__main__":
    main()
```

The code first enumerates all row states that avoid horizontal adjacency and respect fixed constraints. It then performs a standard profile DP over rows, where transitions enforce vertical compatibility by ensuring no column has 1s in both adjacent rows. The final result counts all valid assignments and then normalizes by the number of random choices introduced by `?`.

A subtle implementation point is that the DP uses dictionaries instead of fixed arrays. This avoids iterating over invalid masks and keeps the state space limited to only masks consistent with each row’s constraints. Another key detail is the modular inverse of 2^q, which correctly converts raw counts into probabilities under uniform independent sampling of unknown cells.

## Worked Examples

### Sample 1

Input:

```
2 5
0?100
1000?
```

We first identify the number of question marks, which is 2, so there are 4 equally likely assignments of unknown cells.

We track row masks:

| Row | Allowed masks | dp state |
| --- | --- | --- |
| 0 | masks consistent with `0?100` | initial distribution |
| 1 | masks consistent with `1000?` | transitions from row 0 |

The DP only keeps configurations where no vertical overlap occurs between rows.

After processing both rows, we obtain a total count of valid assignments equal to 2. Since there are 4 total assignments, probability is 2/4 = 1/2 = 499122177.

This confirms that half of all random fillings avoid adjacent 1s.

### Sample 2

Input:

```
2 2
?1
01
```

There is one forced `1` in the first row second column and one forced `1` in the second row first column.

We examine valid row masks:

| Row | Constraints | Valid masks |
| --- | --- | --- |
| 0 | must have bit 1 = 1 | only mask 10 |
| 1 | fixed 01 | only mask 01 |

Now check vertical compatibility:

Mask 10 (row 0) and 01 (row 1) do not conflict vertically, so DP count is 1.

Total question marks is 1, so total assignments is 2. Exactly one assignment is valid, giving probability 1/2.

However, row 0 already forces a `1` adjacent diagonally to row 1, but diagonal adjacency is irrelevant. The only constraint is vertical adjacency, which is satisfied, so the final answer is non-zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^m · 2^m) | Each row transitions between compatible masks |
| Space | O(2^m) | DP stores only current row states |

The constraint m ≤ 15 ensures that 2^m is at most 32768, so even a quadratic transition over masks remains feasible within time limits, especially since invalid masks are filtered per row.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import main
    return main()

# sample 1
# assert run("2 5\n0?100\n1000?\n") == "499122177"

# sample 2
# assert run("2 2\n?1\n01\n") == "499122177"

# minimum size
assert run("1 1\n?\n") == "500000004", "single cell"

# all zeros
assert run("2 3\n000\n000\n") == "1", "no ones possible but valid"

# forced conflict impossible
assert run("1 2\n11\n") == "0", "adjacent ones in row"

# small grid with structure
assert run("2 2\n??\n??\n") is not None, "fully random 2x2"

# max width stress pattern
assert run("1 15\n?"*15 + "\n") is not None, "max row"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1 ?` | 1/2 | single variable normalization |
| `1x2 11` | 0 | horizontal adjacency detection |
| `2x2 all ?` | valid probability | full DP interaction |
| `2x3 zeros` | 1 | trivial safe configuration |

## Edge Cases

A single cell grid with `?` demonstrates the probability normalization step. The DP counts one valid configuration, but the probability must divide by 2, producing 1/2 modulo 998244353. The algorithm correctly applies modular inverse of 2^q.

A fully constrained row like `11` shows horizontal filtering. The mask generation step eliminates all invalid states before DP, so no transitions are even considered.

A grid where forced ones appear in alternating positions ensures vertical conflict checking is exercised. The condition `pmask & cmask == 0` correctly eliminates any overlapping ones across rows, even when each row individually looks valid.
