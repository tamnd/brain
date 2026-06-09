---
title: "CF 1927A - Make it White"
description: "We are given a small horizontal strip of cells, each of which can be black or white. Our goal is to make every cell white by repainting a single contiguous segment. The repainting operation turns every black cell in that segment white, and leaves white cells unchanged."
date: "2026-06-08T18:52:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1927
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 923 (Div. 3)"
rating: 800
weight: 1927
solve_time_s: 100
verified: true
draft: false
---

[CF 1927A - Make it White](https://codeforces.com/problemset/problem/1927/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small horizontal strip of cells, each of which can be black or white. Our goal is to make every cell white by repainting a single contiguous segment. The repainting operation turns every black cell in that segment white, and leaves white cells unchanged. The challenge is to determine the minimum length of the segment that guarantees the entire strip becomes white. The input specifies multiple test cases, each giving the number of cells and the initial colors as a string of 'B' and 'W'. The output is a single integer for each test case representing the minimal segment length required.

The constraints are very small: the number of cells in any strip is at most 10, and there can be up to 10,000 test cases. The small strip length allows us to consider solutions that examine all possible contiguous segments without performance concerns. Edge cases arise when black cells are at the boundaries or clustered at the extremes. For example, if a single black cell is at the leftmost or rightmost position, the minimal segment must cover it; if black cells are scattered, the minimal segment must span from the first to the last black cell.

A careless implementation might simply count the number of black cells or assume the first black cell from the left determines the segment length, which can fail when black cells are separated by whites. For instance, in the strip "BWWB", the correct segment spans from the first to the last black cell, length 4, not just 1 or 2.

## Approaches

The brute-force approach would enumerate every possible contiguous segment and check whether painting that segment turns all cells white. Since the maximum strip length is 10, this involves at most 55 segments per test case (sum of 1 to n), which is perfectly acceptable. Each check is linear in n, so this yields about 550 operations per test case, and up to roughly 5.5 million operations across 10,000 test cases, which is fast enough. This method is correct because it explicitly considers all possible segments, but it is unnecessarily heavy for such a simple problem.

The optimal approach exploits the observation that only the leftmost and rightmost black cells matter. Any segment shorter than the distance between the first and last black cells cannot cover all black cells. Thus, the minimal segment must start at or before the leftmost black and end at or after the rightmost black. The optimal length is the index of the last black minus the index of the first black plus one. This greedy insight reduces the problem to a single pass to find the first and last black cells, giving an O(n) solution per test case, which is extremely fast given n ≤ 10.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted due to small n |
| Greedy (first-last black) | O(n) | O(1) | Accepted, optimal |

## Algorithm Walkthrough

1. For each test case, read the number of cells n and the string s representing the colors.
2. Initialize two variables, `left` and `right`, to track the indices of the leftmost and rightmost black cells. Start `left` at n and `right` at -1 to guarantee they will be overwritten.
3. Loop through the string from left to right. When a black cell is found at index i, update `left` to `min(left, i)` and `right` to `max(right, i)`.
4. After the loop, `left` holds the index of the first black cell, and `right` holds the index of the last black cell. The minimal segment that covers all black cells has length `right - left + 1`.
5. Output the calculated length for the test case.

This algorithm works because any segment shorter than the distance between the first and last black cell leaves at least one black uncovered. Covering exactly from the first to the last black cell ensures all black cells are included and avoids unnecessary repainting of already white cells outside the segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        left = n
        right = -1
        for i, c in enumerate(s):
            if c == 'B':
                left = min(left, i)
                right = max(right, i)
        print(right - left + 1)
```

The solution reads the number of test cases and then iterates over each strip. The leftmost and rightmost black cells are identified by a single pass over the string. The minimal segment length is calculated by subtracting the indices and adding one. Using `strip()` ensures that any trailing newline from `input()` does not interfere with indexing.

## Worked Examples

**Example 1:** "WBBWBW"

| Index | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| Cell | W | B | B | W | B | W |
| left | 1 | 1 | 1 | 1 | 1 | 1 |
| right | 1 | 2 | 2 | 2 | 4 | 4 |

The first black is at index 1, the last black at index 4, so minimal segment length = 4 - 1 + 1 = 4.

**Example 2:** "BWWB"

| Index | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Cell | B | W | W | B |
| left | 0 | 0 | 0 | 0 |
| right | 0 | 0 | 0 | 3 |

Segment length = 3 - 0 + 1 = 4.

These traces confirm the greedy approach correctly identifies the span covering all black cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·t) | Each strip of length n is scanned once, for t test cases. With n ≤ 10, this is efficient. |
| Space | O(1) | Only a few variables per test case are needed; no additional data structures. |

Given the constraints, this solution executes comfortably within the 2-second limit even for 10,000 test cases.

## Test Cases

```python
# helper function
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("8\n6\nWBBWBW\n1\nB\n2\nWB\n3\nBBW\n4\nBWWB\n6\nBWBWWB\n6\nWWBBWB\n9\nWBWBWWWBW\n") == "4\n1\n1\n2\n4\n6\n4\n7", "sample 1"

# custom cases
assert run("2\n3\nBBB\n4\nWWBB") == "3\n2", "all blacks, trailing blacks"
assert run("1\n5\nBWWWB") == "5", "blacks at both ends"
assert run("1\n6\nWWBWWW") == "1", "single black in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "BBB" | 3 | All blacks must be painted |
| "WWBB" | 2 | Trailing blacks correctly counted |
| "BWWWB" | 5 | Blacks at both ends require full segment |
| "WWBWWW" | 1 | Single black handled |

## Edge Cases

A critical edge case occurs when the black cells are separated by whites. For example, "BWWB" has blacks at indices 0 and 3. A naive approach counting only the number of black cells would incorrectly suggest a segment of length 2. The algorithm correctly computes the minimal segment as 3 - 0 + 1 = 4. Another edge case is a single black cell in the strip, e.g., "WBBW". The algorithm computes `left = right = 2`, producing segment length 1, which is correct. This approach correctly handles all positions and spacings of black cells.
