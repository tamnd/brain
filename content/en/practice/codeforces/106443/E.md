---
title: "CF 106443E - Evaluation"
description: "The task is a direct format conversion problem on a fixed-size grid that represents a chessboard. The input is an 8 by 8 character matrix, where each cell is either a chess piece or an empty square."
date: "2026-06-21T16:24:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106443
codeforces_index: "E"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2026"
rating: 0
weight: 106443
solve_time_s: 62
verified: true
draft: false
---

[CF 106443E - Evaluation](https://codeforces.com/problemset/problem/106443/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is a direct format conversion problem on a fixed-size grid that represents a chessboard. The input is an 8 by 8 character matrix, where each cell is either a chess piece or an empty square. Pieces are encoded using standard chess symbols, uppercase for white pieces and lowercase for black pieces, while empty squares are represented by dots.

The required output is a single string in Forsyth-Edwards Notation (FEN). FEN compresses each row of the board from top to bottom, replacing consecutive empty squares with their count, and keeping piece characters unchanged. Rows are separated by slashes.

The structure of the input already matches the spatial layout of a FEN board, so the problem reduces to row-wise compression with a simple run-length encoding rule applied only to dots.

The constraints are minimal because the board size is fixed at 8 by 8. This means any solution, even one with nested loops over the entire grid, runs in constant time. There is no need for asymptotic optimization. The only real requirement is correctness in handling consecutive empty squares and row separators.

The most common mistakes come from subtle formatting issues. A frequent bug is forgetting to flush a pending count of dots at the end of a row. For example, consider the row

```
........
```

The correct output is `8`, but a naive implementation that only emits counts when encountering a non-dot character would incorrectly produce an empty string unless it explicitly handles the end-of-row flush.

Another edge case is mixing digits and characters. For example,

```
r.bk...r
```

must become `r1bk3r`. A buggy approach might append the digit directly without considering that multiple dot segments must be aggregated independently.

Finally, row separation must be exact. Missing a slash between rows or adding a trailing slash at the end produces invalid FEN.

## Approaches

A brute-force interpretation would attempt to process each cell and emit output immediately for every character. One could append dots as-is and later try to post-process the string to compress runs of dots. This would involve scanning the entire intermediate string again to compute run lengths, which is unnecessary and error-prone.

The inefficiency in that approach is not time complexity in the asymptotic sense, since the board is constant size, but structural complexity: multiple passes and extra storage increase the chance of incorrect grouping across row boundaries.

The key observation is that each row is independent, and dot compression is purely local within a row. This means we can process each row in a single linear scan, maintaining a counter for consecutive dots. When a non-dot character is encountered, we flush the counter if it is nonzero, then emit the character. At the end of the row, we flush any remaining counter and append the row result.

This reduces the problem to a single pass per row with constant additional state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with post-processing | O(64) | O(64) | Accepted but unnecessary |
| Single-pass row compression | O(64) | O(64) | Accepted |

## Algorithm Walkthrough

1. Read all 8 rows of the board exactly as strings of length 8. Each row corresponds to one rank in the FEN output order, so no reversal is required. This preserves the top-to-bottom ordering required by the notation.
2. Initialize an empty list to accumulate encoded rows. Using a list avoids repeated string concatenation cost, even though the input size is small.
3. For each row, initialize a counter for consecutive dots and an empty string builder for the encoded version of that row.
4. Scan characters from left to right. If the current character is a dot, increment the dot counter. This defers output until we know the full length of the empty segment.
5. If the current character is not a dot, first check whether the dot counter is nonzero. If it is, append its numeric value to the row string and reset the counter. Then append the piece character itself.
6. After finishing the scan of a row, perform a final flush of the dot counter if it is nonzero. This ensures trailing empty segments are not lost.
7. Append the encoded row to the list of rows.
8. Join all encoded rows using slashes to form the final FEN string.

### Why it works

Each row is decomposed into maximal contiguous segments of either dots or pieces. The algorithm replaces each maximal dot segment with its length and leaves all other characters unchanged. Since segmentation is done strictly left to right without overlap, every square contributes exactly once to exactly one segment. The independence of rows guarantees no interaction between segments across row boundaries, so local correctness per row implies global correctness of the full FEN string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def encode_row(row: str) -> str:
    res = []
    cnt = 0

    for ch in row:
        if ch == '.':
            cnt += 1
        else:
            if cnt:
                res.append(str(cnt))
                cnt = 0
            res.append(ch)

    if cnt:
        res.append(str(cnt))

    return ''.join(res)

def main():
    rows = [input().strip() for _ in range(8)]
    encoded = [encode_row(r) for r in rows]
    print('/'.join(encoded))

if __name__ == "__main__":
    main()
```

The solution isolates row encoding into a helper function, which makes the dot compression logic reusable and easier to reason about. The critical implementation detail is the final flush of the dot counter after each row scan; without it, trailing empty squares would never be emitted.

Using a list for `res` avoids quadratic behavior from repeated string concatenation, even though the scale is fixed here. Joining at the end produces the final compact representation.

## Worked Examples

### Example 1

Input:

```
rnbqkbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBQKBNR
```

Processing each row:

| Row | Dot runs | Encoded |
| --- | --- | --- |
| rnbqkbnr | none | rnbqkbnr |
| pppppppp | none | pppppppp |
| ........ | 8 | 8 |
| ........ | 8 | 8 |
| ........ | 8 | 8 |
| ........ | 8 | 8 |
| PPPPPPPP | none | PPPPPPPP |
| RNBQKBNR | none | RNBQKBNR |

Final output:

```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
```

This trace shows correct compression of full empty rows and confirms that row boundaries are preserved.

### Example 2

Input:

```
r.bk...r
........
```

| Row | Dot runs | Encoded |
| --- | --- | --- |
| r.bk...r | 1, 3 | r1bk3r |
| ........ | 8 | 8 |

Final output:

```
r1bk3r/8
```

This example verifies that multiple separated empty segments are handled independently and that trailing segments are flushed correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) | Each of the 8 rows of length 8 is scanned once |
| Space | O(1) | Only constant extra storage beyond output buffers |

The computation is strictly bounded by a fixed 8 by 8 grid, so it runs instantly within the given limits. Memory usage is constant aside from the output string itself.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    def encode_row(row: str) -> str:
        res = []
        cnt = 0
        for ch in row:
            if ch == '.':
                cnt += 1
            else:
                if cnt:
                    res.append(str(cnt))
                    cnt = 0
                res.append(ch)
        if cnt:
            res.append(str(cnt))
        return ''.join(res)

    rows = [input().strip() for _ in range(8)]
    print('/'.join(encode_row(r) for r in rows))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample 1
assert run("""rnbqkbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBQKBNR
""") == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

# provided sample 2
assert run("""r.bk...r
........
........
........
........
........
........
........
""") == "r1bk3r/8/8/8/8/8/8/8"

# single piece
assert run("""........
........
........
...K....
........
........
........
........
""") == "8/8/8/3K4/8/8/8/8"

# alternating pattern
assert run("""r.r.r.r.
........
........
........
........
........
........
........
""") == "r1r1r1r1/8/8/8/8/8/8/8"

# full pieces
assert run("""RNBQKBNR
RNBQKBNR
RNBQKBNR
RNBQKBNR
RNBQKBNR
RNBQKBNR
RNBQKBNR
RNBQKBNR
""") == "RNBQKBNR/RNBQKBNR/RNBQKBNR/RNBQKBNR/RNBQKBNR/RNBQKBNR/RNBQKBNR/RNBQKBNR"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| full empty board row | 8/... | full-run compression |
| mixed dots and pieces | r1bk3r | multiple segments |
| single piece in center | 3K4 | boundary counting correctness |
| alternating pattern | r1r1r1r1 | repeated flush logic |
| full pieces board | unchanged rows | identity preservation |

## Edge Cases

A fully empty row like `........` tests whether the implementation correctly flushes the dot counter at end-of-row. The algorithm accumulates eight dots, then appends `8` when the row ends, ensuring no loss of state.

A row with multiple separated empty regions such as `r.bk...r` verifies that the counter resets correctly between segments. The scan produces `r`, then flushes `1`, then `bk`, then flushes `3`, and finally `r`, producing `r1bk3r`.

A row composed entirely of pieces ensures that the dot counter remains zero throughout, so no accidental digits are inserted.
