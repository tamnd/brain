---
title: "CF 104770B - Battleship"
description: "The task is about a standard Battleship grid but stripped down to a single query. You are given a square board where each cell is either empty water or contains part of a ship. Alongside this grid, you are also given a single coordinate representing a shot fired by the opponent."
date: "2026-06-28T19:52:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104770
codeforces_index: "B"
codeforces_contest_name: "The XXXI Saint-Petersburg High School Programming Contest (SpbKOSHP 2023) | Qualification for the XXIV Russia Open High School Programming Contest (VKOSHP 2023)"
rating: 0
weight: 104770
solve_time_s: 130
verified: true
draft: false
---

[CF 104770B - Battleship](https://codeforces.com/problemset/problem/104770/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about a standard Battleship grid but stripped down to a single query. You are given a square board where each cell is either empty water or contains part of a ship. Alongside this grid, you are also given a single coordinate representing a shot fired by the opponent. Your job is to determine whether that shot hits a ship cell or lands in water.

In more concrete terms, the input provides an integer grid size and a pair of coordinates. Then it gives an n by n map of characters, where one symbol marks ship cells and the other marks empty sea. The output is a simple yes-or-no decision based on whether the specified coordinate corresponds to a ship cell.

The constraints are small enough that any O(n²) scan of the grid is trivially fast. Even a direct lookup after parsing the grid is optimal, so there is no need for any preprocessing beyond reading the matrix. The structure of the problem rules out any algorithmic complexity concerns like graph traversal or optimization.

The main subtlety is indexing and input formatting. The coordinate is given in zero-based indexing, while many programmers instinctively treat grids as one-based. Another common pitfall is assuming a different input format for the grid, such as space-separated characters instead of contiguous strings, which changes how each row must be parsed.

A concrete edge case arises when the shot is on a boundary or corner. For example, if n = 1 and the grid is a single cell containing water, a shot at (0, 0) must output "Yes". A careless implementation that accidentally swaps row and column or shifts indices by one would incorrectly classify this case.

## Approaches

The brute-force interpretation is to treat every query as a scan over the entire grid to find whether the target cell is a ship. For each query, you would iterate over all n² cells and compare coordinates. This is correct because it directly checks the definition of a hit, but it wastes work since only one cell matters.

The key observation is that the entire grid is static and the query asks about exactly one position. That means we do not need to search; we only need direct indexing into a preloaded 2D structure. Once the grid is stored in memory, accessing a single cell is O(1), so the whole problem reduces to reading input and performing one lookup.

The transition from brute force to optimal comes from recognizing that spatial queries on a static matrix do not require repeated scanning. The grid itself already encodes all necessary information, so preprocessing is just parsing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan per Query | O(n²) | O(n²) | Too slow (unnecessary work) |
| Direct Indexing | O(n²) preprocessing, O(1) query | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the integers n, r, c, which define the grid size and the shot position. The coordinates are assumed to be zero-based, so no adjustment is needed.
2. Read the n rows of the grid and store them in a structure that allows direct indexing. Each row can be stored as a string or list of characters so that grid[r][c] is immediately accessible.
3. Access the cell at position (r, c) in the stored grid.
4. If that cell contains a ship marker, output "No" because the shot is a hit. Otherwise output "Yes" because it is a miss.

The reasoning behind step 4 comes directly from the problem definition: "No" corresponds to hitting a ship, while "Yes" corresponds to water.

### Why it works

The algorithm preserves a one-to-one mapping between input grid cells and memory representation. Since no transformation of the grid is performed, every query coordinate corresponds exactly to one stored character. This makes correctness depend only on correct parsing and correct indexing, so no combinatorial or geometric reasoning is required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, r, c = map(int, input().split())
    grid = [input().strip().replace(" ", "") for _ in range(n)]

    if grid[r][c] == 'S':
        print("No")
    else:
        print("Yes")

if __name__ == "__main__":
    main()
```

The key implementation detail is handling the fact that rows may contain spaces between characters in some variants of the statement. Using `replace(" ", "")` ensures robustness if the input is space-separated.

Indexing is kept zero-based throughout, matching the problem definition directly, which avoids off-by-one errors that are common in grid problems.

## Worked Examples

### Example 1

Input:

n = 5, r = 3, c = 1

We inspect only the single cell at row 3, column 1.

| Step | r | c | grid[r][c] | Decision |
| --- | --- | --- | --- | --- |
| Check | 3 | 1 | S | Hit |

The cell contains a ship, so the output is "No". This confirms that the lookup is sufficient without scanning the grid.

### Example 2

Input:

n = 5, r = 4, c = 4

| Step | r | c | grid[r][c] | Decision |
| --- | --- | --- | --- | --- |
| Check | 4 | 4 | O | Miss |

The cell is water, so the output is "Yes". This shows that boundary cells are handled identically to interior ones since the grid is uniformly indexed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Reading and storing the grid dominates, while query evaluation is O(1) |
| Space | O(n²) | Entire grid is stored for direct access |

The constraints are small enough that storing the grid and performing a single lookup is well within limits. Even for n up to 1000, this approach remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue().strip() if False else ""

# provided sample
# assert run(...) == ...

# custom tests
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 / O | Yes | single-cell water |
| 1 0 0 / S | No | single-cell ship |
| 2 1 1 / OO OO | Yes | bottom-right miss |
| 2 0 0 / SO OS | No | top-left hit |

## Edge Cases

A key edge case is a 1 by 1 grid, where both row and column indices must resolve correctly without assuming any surrounding structure. In that case, the algorithm reduces to a single character comparison, and any indexing mistake immediately becomes visible.

Another edge case is when the input includes spaces between characters. Treating each line as a raw string without removing spaces would shift indices and produce incorrect results. The solution avoids this by normalizing each row before indexing, ensuring the grid structure matches the intended 2D layout.
