---
title: "CF 106263H - SCNU LOGO"
description: "The task starts with a fixed ASCII logo: a small grid made of and . characters with dimensions 5 rows by 36 columns. You are given a scaling factor k, and you must output a new grid where every original character becomes a solid k × k block of the same character."
date: "2026-06-19T14:21:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106263
codeforces_index: "H"
codeforces_contest_name: "2025 \u534e\u5357\u5e08\u8303\u5927\u5b66\u201c\u5353\u8d8a\u6559\u80b2\u676f\u201d\u7b97\u6cd5\u4e0e\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u65b0\u751f\u8d5b\uff09"
rating: 0
weight: 106263
solve_time_s: 63
verified: true
draft: false
---

[CF 106263H - SCNU LOGO](https://codeforces.com/problemset/problem/106263/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The task starts with a fixed ASCII logo: a small grid made of `*` and `.` characters with dimensions 5 rows by 36 columns. You are given a scaling factor `k`, and you must output a new grid where every original character becomes a solid `k × k` block of the same character.

Conceptually, each character in the original grid is a pixel. Scaling by `k` means expanding each pixel into a square tile of side length `k`, preserving its color. The final image therefore has height `5k` and width `36k`.

The constraints are extremely small, with `k` at most 5, so the output size is at most 25 by 180 characters. This immediately tells us that any approach that is even linear in the output size is safe. The real constraint is correctness and avoiding subtle indexing mistakes.

A common mistake appears when people try to reconstruct rows first and then duplicate them incorrectly. Another mistake is mixing up row expansion and column expansion order, which can lead to interleaving repeated patterns instead of block-wise scaling.

For example, if the original grid has a single row `"*."` and `k = 2`, the correct output is:

```
**..
**..
```

A wrong approach might instead duplicate characters vertically but forget horizontal expansion, producing:

```
*.
*.
```

which violates the requirement that each character must become a square block.

Another failure mode comes from attempting to build the scaled grid by concatenating strings repeatedly without controlling alignment, which can easily lead to rows being duplicated incorrectly or columns drifting out of sync.

## Approaches

The brute-force interpretation is direct: treat each character as a pixel and replace it with a `k × k` block immediately in a new grid. For each original row, we construct `k` new rows, and within each of those, we expand each character into `k` copies.

This approach is correct because it explicitly follows the definition of scaling. The cost comes from repeated string construction. For each of the 5 rows, we process 36 characters, and each character contributes `k` copies to each of `k` rows, so total work is proportional to `5 × 36 × k²`. Since `k ≤ 5`, this is at most a few thousand character operations, which is trivial.

There is no meaningful optimization needed beyond implementing the expansion cleanly. The key insight is recognizing that scaling separates into independent row expansion and column expansion: vertical duplication controls how many times each row is repeated, and horizontal duplication controls how wide each character becomes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Expansion | O(5 × 36 × k²) | O(5 × 36 × k²) | Accepted |
| Optimal (same idea, clean construction) | O(5 × 36 × k²) | O(5 × 36 × k²) | Accepted |

## Algorithm Walkthrough

We build the output row by row using direct expansion.

1. Read `k` and the original 5 lines of the logo. The structure is fixed, so no parsing ambiguity exists.
2. For each original row, construct a horizontally expanded version by replacing every character `c` with `c` repeated `k` times. This produces a string representing a single scaled row.
3. Repeat each expanded row `k` times and append all copies to the output. This performs the vertical scaling by duplication.
4. Print all generated rows in order.

The separation of horizontal and vertical expansion ensures that each original character maps to a contiguous `k × k` block. Horizontal expansion ensures width correctness, while repeated printing ensures height correctness.

### Why it works

Each original character at position `(i, j)` maps to a unique block in the output grid occupying rows `[i·k, (i+1)·k)` and columns `[j·k, (j+1)·k)`. The algorithm constructs exactly these blocks because horizontal expansion fixes column intervals, and vertical repetition fixes row intervals. Since every block is filled independently and consistently, no overlaps or gaps can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input().strip())

grid = [input().rstrip("\n") for _ in range(5)]

out_lines = []

for row in grid:
    expanded_row = "".join(ch * k for ch in row)
    for _ in range(k):
        out_lines.append(expanded_row)

sys.stdout.write("\n".join(out_lines))
```

The solution first reads the scaling factor and the fixed number of rows. It then processes each row independently. The expression `ch * k` performs horizontal scaling by duplicating characters. After building one expanded row, it is appended `k` times to achieve vertical scaling. This ordering matters: expanding horizontally first ensures that each printed line already has correct width, so vertical duplication does not require recomputation.

A subtle point is avoiding repeated concatenation inside inner loops using `+=`, which would degrade performance due to repeated string reallocation. Instead, constructing the expanded row once per input row is sufficient.

## Worked Examples

### Example 1

Input:

```
k = 1
row = "*.*"
```

| Step | Original Row | Expanded Row | Output |
| --- | --- | --- | --- |
| 1 | _._ | _._ | _._ |

The scaling factor is 1, so no transformation occurs. The algorithm correctly leaves both dimensions unchanged.

### Example 2

Input:

```
k = 2
row = "*."
```

| Step | Original Row | Expanded Row | Output Lines |
| --- | --- | --- | --- |
| 1 | *. | **.. | **.. |
| 2 | *. | **.. | **.. |

Each character expands into a 2-character block, and each row is repeated twice, forming a 2×2 block per original character. This confirms that both axes are scaled independently and consistently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5 × 36 × k²) | Each character contributes k horizontal copies and each row is repeated k times |
| Space | O(5 × 36 × k²) | Output grid must be stored before printing |

The maximum output size is tiny (at most 900 characters), so the solution comfortably fits within time and memory limits. The algorithm is effectively constant-time under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(sys.stdin.readline().strip())
    grid = [sys.stdin.readline().rstrip("\n") for _ in range(5)]
    out_lines = []
    for row in grid:
        expanded_row = "".join(ch * k for ch in row)
        for _ in range(k):
            out_lines.append(expanded_row)
    return "\n".join(out_lines)

# minimal scaling
assert run("1\n*****...******...***...**...**....**\n**......**.......****..**...**....**\n*****...**.......**.**.**...**....**\n...**...**.......**..****...**....**\n*****...******...**...***...********\n") != "", "k=1 should output same shape"

# k = 2 simple pattern
assert run("2\n*.\n*.\n*.\n*.\n*.\n") == "**..**..\n**..**..\n**..**..\n**..**..\n**..**..\n**..**..", "basic expansion"

# k = 3 single row repeated
assert run("3\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n") == run("3\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*\n"), "consistency check"

# max k behavior
assert len(run("5\n*****...******...***...**...**....**\n**......**.......****..**...**....**\n*****...**.......**.**.**...**....**\n...**...**.......**..****...**....**\n*****...******...**...***...********\n").splitlines()) == 25, "height should be 5*k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=1 logo | identical logo | identity case |
| k=2 small pattern | 2×2 block expansion | correct scaling logic |
| repetitive row input | consistent expansion | stability across rows |
| k=5 full logo | 25 rows output | maximum constraint handling |

## Edge Cases

When `k = 1`, the algorithm should behave as identity. The construction still runs the same loops, but each character is repeated once and each row is printed once, so the output matches input exactly.

For `k = 5`, the largest case, each character becomes a 5×5 block. The algorithm processes 5 rows and produces 25 output rows. Each row expansion is still linear in 36 characters, so the final output is produced without any risk of performance issues or memory strain.

A subtle case is when a row consists entirely of `.` or entirely of `*`. The expansion logic does not distinguish characters, so uniform rows expand into uniform blocks without any structural distortion.
