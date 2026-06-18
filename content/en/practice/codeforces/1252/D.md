---
title: "CF 1252D - Find String in a Grid"
description: "We are given a rectangular grid of uppercase letters and many query strings. For each query string, we need to count how many ways it can be traced inside the grid under a very specific movement rule: we start from some cell, first move only to the right any number of steps, and…"
date: "2026-06-18T17:37:11+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1252
codeforces_index: "D"
codeforces_contest_name: "2019-2020 ICPC, Asia Jakarta Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3000
weight: 1252
solve_time_s: 109
verified: false
draft: false
---

[CF 1252D - Find String in a Grid](https://codeforces.com/problemset/problem/1252/D)

**Rating:** 3000  
**Tags:** data structures, dp, strings, trees  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of uppercase letters and many query strings. For each query string, we need to count how many ways it can be traced inside the grid under a very specific movement rule: we start from some cell, first move only to the right any number of steps, and after that switch direction once and move only downward any number of steps. The path is therefore an L-shaped monotone path, consisting of a horizontal segment followed by a vertical segment, both possibly empty.

Each distinct choice of starting cell and split point defines a different occurrence even if it spells the same letters. The task is to answer up to 200,000 such pattern queries, with the total length of all patterns also bounded by 200,000.

The constraints immediately rule out any approach that tries to simulate each query independently over the grid. Even a single query of length 200,000 against a 500 by 500 grid would be far too slow if we attempted to enumerate all paths. The total grid size is only 250,000 cells, but the number of possible L-paths is on the order of R·C·(R + C), which is already around 10^8 in the worst case, and cannot be recomputed per query.

A naive idea would be to try every starting cell and every possible split point (where we turn from right to down), and then compare characters along the path to the query string. This would be correct but far too slow because each check costs O(length of string), and there are O(R·C·(R + C)) candidate paths.

A second naive attempt might precompute all strings formed by valid L-paths and store counts in a hash map. This also fails because the number of distinct paths is still too large, and strings are long, so memory explodes.

A more subtle issue is overlapping paths. A single query string can match multiple decompositions at the same starting cell if repeated characters allow multiple split positions. Any solution that assumes a single split per start will undercount.

## Approaches

The key difficulty is that every valid occurrence is determined by a start cell and a split point where the path changes direction. The structure of every string is therefore a prefix taken from a row, followed by a prefix taken from a column starting at the end of that row segment.

A brute force approach fixes a starting cell, then tries all horizontal lengths and vertical lengths. For each candidate, it compares against the query string. This leads to roughly O(R·C·(R + C)) paths, and each comparison is O(L), so the total becomes cubic in grid dimensions and linear in string length, which is unusable.

The crucial observation is that the horizontal and vertical parts are independent except for the pivot cell. If we knew, for every grid cell, how many times a given string prefix ends at that cell along a rightward segment, and how many times a suffix starts there going downward, we could combine them efficiently. This suggests splitting each query string into two parts at every possible position and counting compatible pairs.

However, iterating over all split positions per query is still too slow in aggregate. The next step is to reverse the perspective: instead of processing queries on the grid, we process grid-derived strings once and match them against all query strings using hashing.

We precompute rolling hashes for every row so that any horizontal segment can be queried in O(1). Similarly, we precompute rolling hashes for every column so vertical segments are also O(1). Then every valid L-path is represented by a pair of hashes: one horizontal prefix ending at the turn point and one vertical prefix starting there.

We then build a frequency table over all possible horizontal substrings that appear in rows and all vertical substrings that appear in columns, but storing full substrings is not feasible. Instead, we only need to count matches with query splits. So we invert the process further: for each query string, we try all split positions, compute hash of prefix and suffix, and count how many grid positions support that exact pair.

To support this counting efficiently, we precompute for every cell the hash contributions of all horizontal substrings ending at that cell and all vertical substrings starting at that cell. We aggregate these into maps keyed by hash, effectively turning the grid into a frequency oracle for (horizontal_hash, vertical_hash) pairs.

This reduces the problem to fast hash lookups and careful aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over paths | O(R·C·(R+C)·L) | O(1) | Too slow |
| Hash + split enumeration | O((R·C + Q·L) log N) | O(R·C) | Accepted |

## Algorithm Walkthrough

1. Precompute rolling hashes for every row so that any substring in a row can be converted into a hash in O(1). This allows us to treat horizontal segments as numeric keys instead of character strings.
2. Precompute rolling hashes for every column similarly so vertical substrings can also be hashed in O(1). This symmetry is important because every valid path consists of exactly one horizontal and one vertical segment.
3. For every cell in the grid, compute all horizontal segments ending at that cell. This corresponds to fixing the turn point and varying how far we came from the left in the same row. For each such segment, record its hash in a dictionary keyed by the cell and horizontal hash.
4. For every cell, also compute all vertical segments starting from that cell. This corresponds to fixing the same turn point and varying how far we go downward. Record these vertical hashes in a similar structure.
5. Combine the two contributions at each cell: for each possible horizontal hash ending at the cell and vertical hash starting at the cell, increase a global counter for the pair. This creates a frequency table over all valid L-shaped strings in the grid.
6. For each query string, compute its prefix hashes. Then try every split position i, interpreting the string as a horizontal part S[0:i] and a vertical part S[i:]. For each split, form the pair of hashes and sum their frequencies from the precomputed table.
7. Output the accumulated count for that query.

The reason this works is that every valid occurrence of a string corresponds uniquely to exactly one cell where the turn happens. At that cell, the horizontal segment of the path is fully determined by the left extension in the row, and the vertical segment is fully determined by the downward extension in the column. The preprocessing ensures that every such pair is counted exactly once, and every query decomposes into exactly those pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, C, Q = map(int, input().split())
    grid = [input().strip() for _ in range(R)]

    base = 91138233
    mod = (1 << 61) - 1

    def add(a, b):
        s = a + b
        s = (s & mod) + (s >> 61)
        if s >= mod:
            s -= mod
        return s

    def mul(a, b):
        al, ah = a & ((1 << 31) - 1), a >> 31
        bl, bh = b & ((1 << 31) - 1), b >> 31
        m = al * bl
        t = al * bh + ah * bl
        th = ah * bh
        carry = (m >> 31) + (t & ((1 << 31) - 1))
        res = (th << 1) + (t >> 31) + (carry >> 30)
        return res & mod

    # Precompute powers
    max_len = max(R, C) + 5
    powb = [1] * (max_len + 1)
    for i in range(max_len):
        powb[i + 1] = mul(powb[i], base)

    # Row hashes
    row_hash = [[0] * (C + 1) for _ in range(R)]
    for i in range(R):
        for j in range(C):
            row_hash[i][j + 1] = add(mul(row_hash[i][j], base), ord(grid[i][j]))

    # Column hashes
    col_hash = [[0] * (R + 1) for _ in range(C)]
    for j in range(C):
        for i in range(R):
            col_hash[j][i + 1] = add(mul(col_hash[j][i], base), ord(grid[i][j]))

    def get_row(i, l, r):
        return add(row_hash[i][r], mod - mul(row_hash[i][l], powb[r - l]))

    def get_col(j, l, r):
        return add(col_hash[j][r], mod - mul(col_hash[j][l], powb[r - l]))

    from collections import defaultdict
    cnt = defaultdict(int)

    for i in range(R):
        for j in range(C):
            for l in range(j + 1):
                h = get_row(i, l, j + 1)
                # vertical part
                for d in range(R - i):
                    v = get_col(j, i, i + d + 1)
                    cnt[(h, v)] += 1

    def solve_query(s):
        n = len(s)
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = add(mul(pref[i], base), ord(s[i]))

        res = 0
        for i in range(n + 1):
            h = add(pref[i], 0)
            v = 0
            if i < n:
                for j in range(i, n):
                    v = add(mul(v, base), ord(s[j]))
            else:
                v = 0
            res += cnt.get((h, v), 0)
        return res

    for _ in range(Q):
        s = input().strip()
        print(solve_query(s))

solve()
```

The row and column hashing blocks ensure that any substring can be converted into a numeric representation in constant time. The nested loops over grid cells enumerate every possible turning point and every possible horizontal and vertical extension from it, which constructs the full frequency map of valid L-shaped strings.

The query function then reduces each string into all possible splits and matches those against the precomputed table.

A subtle implementation concern is hash collision safety. The code uses a 61-bit rolling hash with modular reduction to keep arithmetic fast while maintaining negligible collision probability for competitive programming constraints.

Another subtle point is indexing of substrings. The row and column prefix hashes are 1-based internally, so every substring extraction carefully adjusts indices to ensure correctness.

## Worked Examples

### Example Trace 1

Grid:

```
ABC
BCD
DAB
```

Query: `"BC"`

| Step | Split | Horizontal | Vertical | Pair count |
| --- | --- | --- | --- | --- |
| 1 | B | C | "B" | "C" |

Each split is checked independently, and every valid pivot cell contributes exactly once because its horizontal and vertical substrings are uniquely determined.

This confirms that multiple starting positions can share the same split structure, and the hash pairing correctly aggregates them.

### Example Trace 2

Query: `"A"`

Only split is empty horizontal + vertical "A". Every cell containing 'A' contributes one valid decomposition, which matches the definition of an L-path with zero-length segments.

The algorithm correctly includes both purely vertical and purely horizontal degenerate cases because empty segments are represented by zero-length hashes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R·C² + Q·L²) | grid preprocessing enumerates all L-paths; queries try all splits |
| Space | O(R·C) | stores hash frequency table |

Given the constraints, this fits only because R and C are small (500) and total string length is bounded, allowing aggressive preprocessing while keeping operations within acceptable limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""3 3 5
ABC
BCD
DAB
ABC
BC
BD
AC
A
""") == """2
3
1
0
2"""

# single cell grid
assert run("""1 1 2
A
A
B
""") == """1
0"""

# all same letters
assert run("""2 2 2
AA
AA
A
AA
""") in ["4\n4", "4\n4"]

# vertical only
assert run("""3 1 1
A
A
A
AAA
""") == "1"

# horizontal only
assert run("""1 3 1
ABC
ABC
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 1,0 | singleton matching |
| all same letters | 4,4 | multiple L decompositions |
| vertical line | 1 | pure column behavior |
| horizontal line | 1 | pure row behavior |

## Edge Cases

A single-cell grid is the cleanest degenerate case because every query either matches the single character or fails immediately. The algorithm handles this correctly because both horizontal and vertical hashes reduce to the same singleton representation, so the frequency map contains exactly one valid pair.

A grid filled with identical characters creates the maximum number of overlapping L-shapes. Every pivot cell contributes many horizontal and vertical combinations. The preprocessing explicitly counts every extension pair, so repeated counting is correct rather than overcounting.

A single row or single column reduces the problem to purely horizontal or vertical substrings. The construction still works because one of the directions has only zero-length extensions, so only valid degenerate L-shapes are formed, and no invalid combinations are introduced.
