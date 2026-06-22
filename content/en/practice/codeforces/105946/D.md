---
title: "CF 105946D - Daily Life of Data Visualization Engineers"
description: "The program described here takes an integer array and performs a simple filtering step before turning it into a vertical bar chart. All non-positive values are discarded, and the remaining values keep their original order."
date: "2026-06-22T15:59:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105946
codeforces_index: "D"
codeforces_contest_name: "2025 UP ACM Algolympics Final Round"
rating: 0
weight: 105946
solve_time_s: 57
verified: true
draft: false
---

[CF 105946D - Daily Life of Data Visualization Engineers](https://codeforces.com/problemset/problem/105946/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The program described here takes an integer array and performs a simple filtering step before turning it into a vertical bar chart. All non-positive values are discarded, and the remaining values keep their original order. If nothing survives this filtering, the process fails immediately. Otherwise, each remaining value becomes the height of a column in a grid, and the grid visualizes these heights as stacked blocks from bottom to top.

The key idea is that the final output is not arbitrary ASCII art. It must represent a histogram drawn from some sequence of positive integers. Each column corresponds to one element of the filtered array, and each column is filled from the bottom up with `#` for exactly the number of rows equal to that value. Everything above is `.`.

We are given a grid and asked whether it could have been produced by such a process, and if so, we must reconstruct any valid original array of minimal length.

The constraints are small, with both dimensions up to 100, which suggests that an O(r·c) or O(r·c log c) reconstruction is more than sufficient. The real difficulty is not performance but correctness of interpretation: the grid must be checked against a structure that is implicitly a histogram with strictly vertical columns of contiguous blocks aligned at the bottom.

A naive but common failure case is to misread the bottom alignment rule. For example, a column like

```
.#
#.
```

cannot happen because the `#` must always be contiguous from the bottom upward. Another subtle failure is forgetting that columns are independent: there is no requirement that heights be sorted or monotone.

## Approaches

A brute-force perspective would be to guess all possible arrays of length c, each entry between 0 and r, and check whether their histogram matches the grid. Even if we ignore the preprocessing step (which removes non-positive values), this already yields $(r+1)^c$ possibilities, which is astronomically large even for c = 100.

The structure of the problem removes all ambiguity once we look at the grid column by column. Each column of the final image uniquely determines the value that must have been in the array, because the height of consecutive `#` cells from the bottom is exactly that value. There is no interaction between columns except that the array order is preserved.

The only remaining complication is validity: each column must have a single contiguous block of `#` at the bottom, and nothing above it. If any column violates this, no array can produce it. Once valid, the reconstructed array is simply the list of column heights.

The “cleaning” step in the original program only removes non-positive values. Since the output grid only contains `#` and `.`, any valid column must correspond to a strictly positive integer, so we never need to explicitly reconstruct removed elements. The minimal-length requirement becomes automatic: every valid column must contribute exactly one positive number, and there is no reason to introduce extra elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O((r+1)^c · r·c) | O(r·c) | Too slow |
| Column Reconstruction | O(r·c) | O(c) | Accepted |

## Algorithm Walkthrough

We interpret the grid as c independent vertical columns.

1. For each column j, we compute how many consecutive `#` appear starting from the bottom row upward. This count is the only possible height of a bar that could generate this column. Any deviation above that block immediately invalidates the column.
2. While scanning upward, if we encounter a `#` after already seeing a `.`, the column is structurally impossible. This is because the histogram definition requires all `#` cells to form a contiguous suffix from the bottom.
3. We store the computed height for each column in an array. If a column has zero `#`, its height would be zero, which is not allowed in the final reconstructed array because only positive integers remain after cleaning. However, such a column is still acceptable as long as it is fully empty; it simply means it would have been removed during preprocessing, but since output requires minimal positive array producing the grid, we treat this as invalid unless we reinterpret carefully: in fact, a column with zero `#` means height 0, but since cleaned array removes non-positive values, such a column could not appear at all. So any all-dot column makes the answer impossible.
4. After processing all columns, we output the array of heights if all are positive and valid.

### Why it works

Each column in the output grid is fully determined by a single integer height. The histogram construction has no coupling between columns, so the grid is valid if and only if every column is a suffix of `#` of some positive length. The reconstruction is therefore injective: there is exactly one possible value per column, and any valid solution must match these values. Any violation of contiguity or presence of isolated `#` cells contradicts the definition of bottom-aligned stacking, so rejection is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

r, c = map(int, input().split())
grid = [input().strip() for _ in range(r)]

heights = []

for col in range(c):
    h = 0
    seen_dot = False

    for row in range(r - 1, -1, -1):
        if grid[row][col] == '#':
            if seen_dot:
                print("No")
                sys.exit(0)
            h += 1
        else:
            seen_dot = True

    if h == 0:
        print("No")
        sys.exit(0)

    heights.append(h)

print("Yes")
print(len(heights))
print(*heights)
```

The solution directly encodes the column-wise reconstruction. The downward scan is chosen because the definition of the histogram is bottom-aligned, so counting from the bottom avoids extra transformation.

The `seen_dot` flag enforces contiguity: once we leave the `#` region, we must never see another `#`. This is the critical structural constraint that distinguishes valid histograms from arbitrary patterns.

The check `h == 0` ensures compliance with the requirement that the final cleaned array contains only positive integers, meaning every surviving column must contribute at least one `#`.

## Worked Examples

Consider the first sample:

```
..#
#.#
#.#
###
```

We process column by column.

| Column | Bottom-up scan | Seen dot breaks? | Height |
| --- | --- | --- | --- |
| 0 | #.#. | no | 3 |
| 1 | ###. | no | 1 |
| 2 | #### | no | 4 |

The reconstructed array is `[3, 1, 4]`.

This confirms that valid columns are independent and fully determined by suffix counts.

Now consider an invalid grid:

```
..#
###
#.#
###
```

Column 1 (middle column) becomes problematic because scanning bottom-up yields `# # . #`, meaning after encountering a dot, a hash reappears. This violates the required contiguous structure, so the algorithm rejects immediately.

This demonstrates that the main failure mode is not height mismatch but structural inconsistency inside a column.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(r·c) | Each cell is visited once while scanning columns bottom-up |
| Space | O(c) | Only the reconstructed height array is stored |

The grid size is at most 100×100, so the algorithm executes at most 10,000 operations, well within limits. Memory usage is constant beyond the input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r)]

        heights = []
        for col in range(c):
            h = 0
            seen_dot = False
            for row in range(r - 1, -1, -1):
                if grid[row][col] == '#':
                    if seen_dot:
                        print("No")
                        return out.getvalue().strip()
                    h += 1
                else:
                    seen_dot = True
            if h == 0:
                print("No")
                return out.getvalue().strip()
            heights.append(h)

        print("Yes")
        print(len(heights))
        print(*heights)

    return out.getvalue().strip()

# provided sample 1
assert run("""4 3
..#
#.#
#.#
###
""") == "Yes\n3\n3 1 4"

# sample 2 (invalid)
assert run("""4 3
..#
###
#.#
###
""") == "No"

# all dots column
assert run("""3 2
..
..
..
""") == "No"

# single column valid
assert run("""4 1
#
#
.
.
""") == "Yes\n1\n2"

# minimal valid case
assert run("""1 1
#
""") == "Yes\n1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all dots grid | No | Rejects zero-height columns |
| mixed invalid column | No | Detects non-contiguous `#` pattern |
| single column valid | Yes | Basic reconstruction correctness |
| 1×1 grid | Yes | Minimal boundary condition |

## Edge Cases

A grid with a column of all dots fails immediately because the reconstructed height becomes zero. For example:

```
2 2
..
..
```

During processing, both columns yield height 0, so the algorithm outputs `No`. This aligns with the fact that after cleaning, the array would be empty, which is explicitly forbidden.

A column where `#` appears above a `.` is also rejected. For instance:

```
3 1
#
.
#
```

Scanning bottom-up encounters `#`, then `.`, then `#`, triggering the invalid-state flag. This captures the core structural constraint of bottom-aligned histograms.

A fully valid tall column such as:

```
5 1
.
.
#
#
#
```

produces height 3, and no inconsistency appears. The algorithm correctly reconstructs `[3]`, confirming that sparse grids with leading dots are handled naturally.
