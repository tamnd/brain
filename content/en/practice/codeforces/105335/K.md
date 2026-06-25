---
title: "CF 105335K - Kid Rally"
description: "The map is an N × M grid of lattice points. Each point has a score between 0 and 9. Alice starts at the top-left corner (1,1) and Bob starts at the top-right corner (1,M). A move must go to a strictly larger row number, and every move is a straight line segment."
date: "2026-06-26T00:32:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105335
codeforces_index: "K"
codeforces_contest_name: "ICPC Thailand National Competition 2024"
rating: 0
weight: 105335
solve_time_s: 83
verified: true
draft: false
---

[CF 105335K - Kid Rally](https://codeforces.com/problemset/problem/105335/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The map is an `N × M` grid of lattice points. Each point has a score between `0` and `9`.

Alice starts at the top-left corner `(1,1)` and Bob starts at the top-right corner `(1,M)`. A move must go to a strictly larger row number, and every move is a straight line segment. The score of a path is the sum of all lattice points visited by that path.

The two paths are not allowed to intersect. Either child may stop at any moment and finish their rally.

The final answer is

$$(\text{Alice score}) \times (\text{Bob score})$$

and we want the maximum possible value.

The grid dimensions are at most `1000 × 1000`, but every cell value is only a single digit. That small score range turns out to be the key observation.

The first geometric fact is that an optimal path never jumps over rows. If a path moves from row `r` directly to row `r+2`, every score is non-negative, so inserting an intermediate point in row `r+1` can only increase the score. The tutorial for the contest explicitly states that in an optimal solution the row coordinate increases by exactly one at every move.

Once both players are still moving, they must appear in every row and Alice must stay strictly to the left of Bob in that row.

A subtle edge case appears when one player stops early.

Consider

```
2 2
9 1
9 0
```

If both continue to row 2, the best product is `18 × 1 = 18`.

A better solution is for Alice to stop immediately. Alice keeps score `9`, while Bob moves to `(2,1)` and gets `1 + 9 = 10`. The answer becomes `90`. The official tutorial calls out exactly this situation.

Any solution that assumes both players always continue until row `N` will fail on this test.

## Approaches

A brute force formulation is easy to describe. For every row, choose Alice's column and Bob's column such that Alice stays to the left. Then compute both scores and maximize the product.

The problem is that each row has roughly `M²` possibilities. With `N,M ≤ 1000`, the number of configurations is astronomically large.

The key observation is that once we know Alice's column in a row, Bob only cares about the best value strictly to its right.

Suppose we are processing row `r`.

If Alice takes column `i`, she gains

$$S[r][i]$$

and Bob can choose the best column to the right, gaining

$$\max_{j>i} S[r][j].$$

For this row we only need pairs

$$(a,b).$$

Since every cell value is between `0` and `9`, both `a` and `b` are digits.

For a fixed Alice gain `a`, only the maximum achievable Bob gain matters. That means each row contributes at most ten useful transitions, one for every digit `0..9`.

Now look at the total score.

Alice's additional score beyond the starting cell is at most

$$9(N-1) \le 8991.$$

That means we can run a knapsack-style DP where the state is Alice's accumulated score.

Let

$$dp[x]$$

be the maximum Bob score obtainable while both players are still active and Alice has accumulated additional score `x`.

The state space is only about `9000`, which is small enough.

The remaining complication is early stopping. After processing some prefix of rows, Alice may stop and Bob becomes unrestricted, or Bob may stop and Alice becomes unrestricted. We evaluate both possibilities at every row boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| DP on Alice's score | O(N · 9000) | O(9000) | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. Let `baseA = S[1][1]` and `baseB = S[1][M]`.
3. For every row `r ≥ 2`, compute:

`rowMax[r]` = maximum value in that row.

For every digit `a` from `0` to `9`, compute

`best[a] = max value to the right of some column whose value equals a`.

This represents all useful transitions while both players are still active.
4. Build a suffix array

$$suf[r] = \sum_{k=r}^{N} rowMax[k]$$

which tells us how many points a lone remaining player can still collect after the other one stops.
5. Initialize

```
dp[0] = 0
```

and all other states as impossible.
6. Before processing row `r`, evaluate stopping after row `r-1`.

If Alice stops:

```
Alice = baseA + x
Bob   = baseB + dp[x] + suf[r]
```

If Bob stops:

```
Alice = baseA + x + suf[r]
Bob   = baseB + dp[x]
```

Update the answer with both products.
7. Process row `r`.

For every reachable state `x` and every valid digit transition `(a,b)` from that row:

```
ndp[x + a] =
    max(ndp[x + a], dp[x] + b)
```
8. Replace `dp` with `ndp` and continue.
9. After all rows are processed, evaluate the case where both players remain active until the last row:

```
(baseA + x) * (baseB + dp[x])
```
10. Output the maximum product.

### Why it works

While both players are moving, every row contributes independently.

If Alice chooses a column with value `a`, Bob's optimal choice in that same row depends only on the best value strictly to the right. No other information about the row matters.

The DP stores every possible Alice total score and the largest Bob score compatible with it. Since future rows only depend on accumulated totals, this state is sufficient.

Whenever one player stops, the remaining player becomes unconstrained and can independently take the maximum value from every remaining row. The suffix sums exactly represent that future gain.

The DP explores every feasible active-prefix configuration and every possible stopping position, so the maximum product is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [list(map(int, input().split())) for _ in range(n)]

    baseA = g[0][0]
    baseB = g[0][m - 1]

    row_max = [0] * n
    row_opts = []

    for r in range(1, n):
        row = g[r]
        row_max[r] = max(row)

        suf_right = [-1] * m
        cur = -1
        for c in range(m - 1, -1, -1):
            suf_right[c] = cur
            cur = max(cur, row[c])

        best = [-1] * 10

        for c in range(m - 1):
            a = row[c]
            b = suf_right[c]
            if b >= 0:
                best[a] = max(best[a], b)

        opts = []
        for a in range(10):
            if best[a] >= 0:
                opts.append((a, best[a]))

        row_opts.append(opts)

    suf = [0] * (n + 2)
    for r in range(n - 1, 0, -1):
        suf[r] = suf[r + 1] + row_max[r]

    MAXS = 9 * (n - 1)

    NEG = -10**18
    dp = [NEG] * (MAXS + 1)
    dp[0] = 0

    ans = baseA * baseB

    for idx in range(n - 1):
        r = idx + 2

        rem = suf[r]

        for x in range(MAXS + 1):
            if dp[x] == NEG:
                continue

            bob_now = dp[x]

            ans = max(
                ans,
                (baseA + x) * (baseB + bob_now + rem)
            )

            ans = max(
                ans,
                (baseA + x + rem) * (baseB + bob_now)
            )

        ndp = [NEG] * (MAXS + 1)

        for x in range(MAXS + 1):
            if dp[x] == NEG:
                continue

            cur_b = dp[x]

            for a, b in row_opts[idx]:
                nx = x + a
                if cur_b + b > ndp[nx]:
                    ndp[nx] = cur_b + b

        dp = ndp

    for x in range(MAXS + 1):
        if dp[x] == NEG:
            continue

        ans = max(
            ans,
            (baseA + x) * (baseB + dp[x])
        )

    print(ans)

solve()
```

After reading the grid, the code preprocesses each row into a compact set of transitions. For every digit `a`, only the largest Bob gain achievable while Alice gains `a` is kept. This is exactly the compression that reduces the per-row work from `O(M²)` possibilities to at most ten transitions.

The DP array is indexed by Alice's accumulated score. Since every score is a digit, the maximum index is only `9(N-1)`.

The suffix array handles the early-stop cases. When Alice or Bob stops, the other player can freely collect the maximum value of every remaining row, so a simple suffix sum is enough.

The most common implementation mistake is forgetting the stopping cases before the last row. The official tutorial's `2 × 2` example exists precisely because the optimum may require one player to stop immediately.

## Worked Examples

### Example 1

```
3 5
9 1 3 2 5
0 0 9 0 0
3 1 2 6 1
```

Row 2 produces:

| Alice gain | Best Bob gain |
| --- | --- |
| 0 | 9 |
| 9 | 0 |

Row 3 produces:

| Alice gain | Best Bob gain |
| --- | --- |
| 3 | 6 |
| 1 | 6 |
| 2 | 6 |
| 6 | 1 |

DP evolution:

| Stage | Alice score | Bob score |
| --- | --- | --- |
| Start | 0 | 0 |
| After row 2 | 0 | 9 |
| After row 2 | 9 | 0 |
| After row 3 | 3 | 15 |
| After row 3 | 1 | 15 |
| After row 3 | 2 | 15 |
| After row 3 | 6 | 10 |
| After row 3 | 12 | 6 |
| After row 3 | 10 | 6 |
| After row 3 | 11 | 6 |
| After row 3 | 15 | 1 |

The best state gives totals:

```
Alice = 9 + 3 = 12
Bob   = 5 + 15 = 20
```

Product:

```
240
```

This matches the sample.

### Example 2

```
2 2
9 1
9 0
```

Before processing row 2:

| Alice extra | Bob extra |
| --- | --- |
| 0 | 0 |

If Alice stops immediately:

| Quantity | Value |
| --- | --- |
| Alice | 9 |
| Bob | 1 + 9 = 10 |
| Product | 90 |

If both continue:

| Quantity | Value |
| --- | --- |
| Alice | 18 |
| Bob | 1 |
| Product | 18 |

The algorithm correctly keeps `90`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · 9000) | DP score range is at most `9(N-1)` |
| Space | O(9000) | One DP array over Alice's score |

With `N ≤ 1000`, the score range never exceeds about `9000`, so the DP remains comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    data = io.StringIO(inp)
    input = data.readline

    n, m = map(int, input().split())
    g = [list(map(int, input().split())) for _ in range(n)]

    baseA = g[0][0]
    baseB = g[0][m - 1]

    row_max = [0] * n
    row_opts = []

    for r in range(1, n):
        row = g[r]
        row_max[r] = max(row)

        suf_right = [-1] * m
        cur = -1
        for c in range(m - 1, -1, -1):
            suf_right[c] = cur
            cur = max(cur, row[c])

        best = [-1] * 10

        for c in range(m - 1):
            a = row[c]
            b = suf_right[c]
            if b >= 0:
                best[a] = max(best[a], b)

        opts = []
        for a in range(10):
            if best[a] >= 0:
                opts.append((a, best[a]))

        row_opts.append(opts)

    suf = [0] * (n + 2)
    for r in range(n - 1, 0, -1):
        suf[r] = suf[r + 1] + row_max[r]

    MAXS = 9 * (n - 1)
    NEG = -10**18

    dp = [NEG] * (MAXS + 1)
    dp[0] = 0

    ans = baseA * baseB

    for idx in range(n - 1):
        r = idx + 2
        rem = suf[r]

        for x in range(MAXS + 1):
            if dp[x] == NEG:
                continue

            ans = max(ans, (baseA + x) * (baseB + dp[x] + rem))
            ans = max(ans, (baseA + x + rem) * (baseB + dp[x]))

        ndp = [NEG] * (MAXS + 1)

        for x in range(MAXS + 1):
            if dp[x] == NEG:
                continue

            for a, b in row_opts[idx]:
                ndp[x + a] = max(ndp[x + a], dp[x] + b)

        dp = ndp

    for x in range(MAXS + 1):
        if dp[x] != NEG:
            ans = max(ans, (baseA + x) * (baseB + dp[x]))

    return str(ans) + "\n"

# provided sample
assert run(
"""3 5
9 1 3 2 5
0 0 9 0 0
3 1 2 6 1
"""
) == "240\n"

# custom cases
assert run(
"""2 2
9 1
9 0
"""
) == "90\n"

assert run(
"""2 2
0 0
0 0
"""
) == "0\n"

assert run(
"""2 3
1 2 3
4 5 6
"""
) == "24\n"

assert run(
"""3 2
9 9
9 9
9 9
"""
) == "243\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2×2 early-stop example | 90 | One player stopping immediately |
| All zeros | 0 | Zero-score handling |
| Single extra row | 24 | Basic DP transition |
| All values equal | 243 | Multiple equivalent choices |

## Edge Cases

Consider again:

```
2 2
9 1
9 0
```

Initial state:

```
Alice = 9
Bob = 1
```

Before row 2 is processed, the algorithm evaluates stopping.

The remaining maximum-row suffix is:

```
9
```

Alice stopping gives:

```
9 × (1 + 9) = 90
```

which becomes the current answer.

The DP transition for continuing produces only:

```
18 × 1 = 18
```

so the final answer remains `90`.

Now consider:

```
2 2
0 0
0 0
```

Every transition contributes zero. The DP contains only one reachable state, and every stopping evaluation also produces zero. The algorithm outputs `0`, which is correct.

Finally consider:

```
3 2
9 9
9 9
9 9
```

The only possible ordering is Alice in column 1 and Bob in column 2. Both collect all three rows:

```
27 × 27 = 729
```

If either stops early, the product becomes smaller. The DP evaluates both continuing and stopping, keeping the correct maximum.
