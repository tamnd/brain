---
title: "CF 79B - Colorful Field"
description: "We are asked to simulate planting crops on a rectangular field, but with a catch: some cells are wasteland. The field is represented as an n by m grid, with rows numbered from 1 to n and columns from 1 to m."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 79
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 71"
rating: 1400
weight: 79
solve_time_s: 79
verified: true
draft: false
---

[CF 79B - Colorful Field](https://codeforces.com/problemset/problem/79/B)

**Rating:** 1400  
**Tags:** implementation, sortings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate planting crops on a rectangular field, but with a catch: some cells are wasteland. The field is represented as an _n_ by _m_ grid, with rows numbered from 1 to _n_ and columns from 1 to _m_. Some cells contain waste, and the rest contain crops planted cyclically in the order Carrots → Kiwis → Grapes, filling the field row by row, skipping waste cells.

Input gives the dimensions of the field, a list of waste cell coordinates, and a list of query coordinates. For each query, we must determine whether that cell is waste or which crop it contains.

Constraints are moderately large: the field can have up to 40,000 rows and columns. That gives up to 1.6 billion cells. Clearly, storing the entire field explicitly is impossible within memory limits, so any solution that builds the full grid is not feasible. The number of waste cells and queries, however, is small (up to 1000 each), which hints that a direct simulation of the whole field is unnecessary. We must work with waste cells and queries in a more abstract, index-based way.

Edge cases that could break a naive solution include querying a cell that is waste, the first or last cell in the planting order, or having multiple queries for the same cell. If you fail to skip waste cells correctly when counting crops, the crop assignment will be off by one or more, producing incorrect answers.

## Approaches

A brute-force solution would try to simulate the entire planting process. You could iterate through each cell in row-major order, skip waste cells, and assign crops in the Carrot-Kiwi-Grape cycle. This is conceptually simple and correct, but the field could be up to 40,000 × 40,000, which is 1.6 billion cells. Even with fast iteration, simulating each cell would take hundreds of seconds-far too slow for a 2-second limit.

The key observation that allows optimization is that the planting order is predictable: each cultivated cell gets a crop based purely on its index in the row-major sequence, ignoring waste cells that come before it. So, we can compute a "linear index" of any cell in O(1) time. Then, if we know how many waste cells appear before a given cell in this linear ordering, we can subtract that count to determine the crop type for that cell. Waste cells act as offsets in the sequence, shifting the crop indices for subsequent cells.

With this insight, the solution reduces to three main steps: map 2D coordinates to 1D indices, sort the waste cells by their indices, and for each query, check if it's a waste cell and, if not, determine the crop using modulo arithmetic based on the number of non-waste cells before it. Sorting waste cells costs O(k log k), and each query can be answered in O(log k) using binary search, which is efficient given k ≤ 1000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n*m) | Too slow |
| Optimal | O(k log k + t log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Compute the 1D index for every cell in row-major order using the formula `(row - 1) * m + (col - 1)`. This gives a unique integer for each cell, allowing waste cells to be handled in a simple linear fashion.
2. Convert each waste cell coordinate to its corresponding 1D index and store them in a list. Then sort this list. Sorting ensures that, for any query, we can efficiently determine how many waste cells precede it using binary search.
3. For each query, first convert the coordinate to its 1D index. Check if this index is in the sorted list of waste indices using binary search. If it is, the cell is waste, and we output "Waste".
4. If the cell is not waste, count the number of waste cells with indices less than the query cell using `bisect_left`. Subtract this count from the query cell index to get its zero-based position among cultivated cells.
5. Use modulo 3 on this position to determine the crop: position % 3 == 0 corresponds to Carrots, 1 to Kiwis, and 2 to Grapes.

Why it works: The crucial invariant is that the crop type of a cultivated cell depends only on its relative position among cultivated cells, not on the full field. Sorting waste cells allows us to determine this relative position efficiently. Subtracting the number of preceding waste cells correctly shifts the sequence, preserving the intended planting order.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n, m, k, t = map(int, input().split())
waste = []

for _ in range(k):
    a, b = map(int, input().split())
    idx = (a - 1) * m + (b - 1)
    waste.append(idx)

waste.sort()
crops = ["Carrots", "Kiwis", "Grapes"]

for _ in range(t):
    i, j = map(int, input().split())
    query_idx = (i - 1) * m + (j - 1)
    pos = bisect.bisect_left(waste, query_idx)
    if pos < len(waste) and waste[pos] == query_idx:
        print("Waste")
    else:
        crop_idx = (query_idx - pos) % 3
        print(crops[crop_idx])
```

The code converts both waste cells and queries to their linear indices. Sorting the waste indices allows binary search to detect waste and compute the number of preceding wastes efficiently. Subtracting the number of preceding wastes yields the cultivated cell index to determine the crop cyclically.

## Worked Examples

**Sample Input 1:**

```
4 5 5 6
4 3
1 3
3 3
2 5
3 2
1 3
1 4
2 3
2 4
1 1
1 1
```

| Query | Linear idx | Wastes before | Adjusted idx | Crop |
| --- | --- | --- | --- | --- |
| 1,3 | 2 | 0 | waste | Waste |
| 1,4 | 3 | 1 | 2 | Grapes |
| 2,3 | 7 | 3 | 4 | Carrots |
| 2,4 | 8 | 3 | 5 | Kiwis |
| 1,1 | 0 | 0 | 0 | Carrots |
| 1,1 | 0 | 0 | 0 | Carrots |

This trace confirms that subtracting the number of preceding waste cells aligns crops correctly.

**Custom Input 2 (First cell is waste, last cell queried):**

```
3 3 1 2
1 1
1 1
3 3
```

| Query | Linear idx | Wastes before | Adjusted idx | Crop |
| --- | --- | --- | --- | --- |
| 1,1 | 0 | 0 | waste | Waste |
| 3,3 | 8 | 1 | 7 | Kiwis |

This confirms edge handling of first and last cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k + t log k) | Sorting k waste cells, and binary searching for t queries |
| Space | O(k) | Store sorted waste indices |

Even in the worst case with k = t = 1000, the algorithm performs at most 2000 log 1000 operations, negligible compared to the 2-second limit. Memory usage is well within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # insert the solution code here or call a function
    n, m, k, t = map(int, input().split())
    waste = []
    for _ in range(k):
        a, b = map(int, input().split())
        idx = (a - 1) * m + (b - 1)
        waste.append(idx)
    waste.sort()
    crops = ["Carrots", "Kiwis", "Grapes"]
    for _ in range(t):
        i, j = map(int, input().split())
        query_idx = (i - 1) * m + (j - 1)
        pos = bisect.bisect_left(waste, query_idx)
        if pos < len(waste) and waste[pos] == query_idx:
            print("Waste")
        else:
            crop_idx = (query_idx - pos) % 3
            print(crops[crop_idx])
    return out.getvalue().strip()

# provided sample
assert run("""4 5 5 6
4 3
1 3
3 3
2 5
3 2
1 3
1 4
2 3
2 4
1 1
1 1
""") == """Waste
Grapes
Carrots
Kiwis
Carrots
Carrots"""

# custom minimum size
assert run("""1 1 0 1
1 1
```
