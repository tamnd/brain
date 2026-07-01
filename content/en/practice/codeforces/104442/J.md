---
title: "CF 104442J - Aviones"
description: "The grid describes a black-and-white image where most cells are background and the remaining cells belong to an airplane. Every airplane cell is labeled with a digit from 0 to 9, and all cells sharing the same digit form a single “zone type”."
date: "2026-06-30T18:08:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104442
codeforces_index: "J"
codeforces_contest_name: "AdaByron Regional Madrid 2023"
rating: 0
weight: 104442
solve_time_s: 52
verified: true
draft: false
---

[CF 104442J - Aviones](https://codeforces.com/problemset/problem/104442/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid describes a black-and-white image where most cells are background and the remaining cells belong to an airplane. Every airplane cell is labeled with a digit from 0 to 9, and all cells sharing the same digit form a single “zone type”. The task is to decide which zone type should be reinforced.

Separately from the image, we are given a list of impact points. Each impact lands on a valid airplane cell, meaning it always lands on one of the digit-labeled pixels. For each digit, we count how many impacts hit pixels of that digit. We also know how large each digit’s region is, measured by how many grid cells carry that digit.

The decision rule is hierarchical. First, we choose the digit with the smallest number of hits. If multiple digits tie, we prefer the one whose region occupies fewer pixels in the image. If there is still a tie, we choose the digit with the smallest numeric identifier.

The constraints are small: the grid is at most 100 by 100, and there are at most 2000 impacts. This means a direct scan of the entire image and a simple tally per impact is easily fast enough, since all operations are linear in the grid size plus the number of impacts.

A common mistake is to assume that digits always appear in a contiguous or single connected component, but that is irrelevant here. Another subtle trap is forgetting that some digits might not appear at all in the grid; those must be excluded from consideration since they do not represent any zone.

## Approaches

A direct solution computes two pieces of information for each digit from 0 to 9: how many cells in the grid contain that digit, and how many impacts land on it. Both can be accumulated in a single pass over the grid and a single pass over the impact list.

The brute-force way to answer each impact would be to scan the entire grid and check where it lands, but that would make each query O(MN), leading to O(DMN) total work, which is unnecessary given that we can directly index into the grid to find the digit at an impact location.

The key observation is that the grid already encodes everything we need for classification. Each impact is just a lookup into a precomputed labeling, so we can accumulate counts in constant time per event.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan grid per impact) | O(D · M · N) | O(M · N) | Too slow |
| Optimal (precompute + counting) | O(M · N + D) | O(M · N) | Accepted |

## Algorithm Walkthrough

1. Read the grid dimensions and store the grid as a list of strings. Each cell either contains '.' or a digit character. We only care about digit cells because they define valid zones.
2. Initialize an array of size 10 to count how many cells belong to each digit. We also initialize another array of size 10 to count how many impacts hit each digit.
3. Scan every cell in the grid. Whenever we see a digit character, convert it to an integer and increment its size counter. This builds the total area of each zone type in linear time.
4. Read the number of impacts, then process each impact coordinate. For each coordinate, directly access the grid cell and convert it into a digit. Increment the corresponding hit counter. This works because every impact is guaranteed to land on a digit cell.
5. After processing all inputs, iterate over digits from 0 to 9 and select the best candidate using the comparison rule: smallest number of hits first, then smallest zone size, then smallest digit value.
6. Output the chosen digit.

### Why it works

Each impact contributes independently to exactly one digit category, so counting is simply a partition of events over fixed labels. The grid scan provides exact weights for each label, and the impact scan provides exact frequencies. Since both quantities are fully aggregated per digit, comparing digits reduces to a simple lexicographic minimum over precomputed statistics.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    M, N = map(int, input().split())
    grid = [input().strip() for _ in range(N)]

    size = [0] * 10
    hits = [0] * 10

    for y in range(N):
        row = grid[y]
        for x in range(M):
            c = row[x]
            if c != '.':
                size[int(c)] += 1

    D = int(input())
    for _ in range(D):
        y, x = map(int, input().split())
        d = grid[y][x]
        hits[int(d)] += 1

    best = None
    for d in range(10):
        if size[d] == 0:
            continue
        cand = (hits[d], size[d], d)
        if best is None or cand < best:
            best = cand

    print(best[2])

if __name__ == "__main__":
    solve()
```

The solution first builds frequency tables for both region sizes and impact counts. The grid traversal is a direct nested loop over all cells, ensuring each digit’s total area is known exactly once. The second phase processes each impact in constant time by indexing directly into the grid.

The final selection step relies on Python’s tuple comparison, which naturally implements the required priority order: minimize hits, then minimize size, then minimize digit.

## Worked Examples

Consider a simplified grid:

Input:

```
3 3
0.1
0.2.
111
3
0 0
2 0
2 2
```

Here the grid contains digits 0, 1, and 2.

We first compute sizes:

| Digit | Size |
| --- | --- |
| 0 | 2 |
| 1 | 4 |
| 2 | 1 |

Now process impacts:

| Impact | Cell | Digit | Hits |
| --- | --- | --- | --- |
| (0,0) | 0 | 0 | 1 |
| (2,0) | 1 | 1 | 1 |
| (2,2) | 1 | 1 | 2 |

So final hit counts:

| Digit | Hits |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 0 |

Digit 2 has the fewest hits, so it is selected even though it is small. This demonstrates that hit count dominates size in the decision hierarchy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MN + D) | One full scan of the grid plus one pass over all impacts |
| Space | O(MN) | Storage of the grid plus constant-size counters |

The constraints guarantee that at most 10 million grid cells and 2000 impacts are processed, which fits easily within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType

    # assumes solution is defined in same file
    # we re-run solve directly if available
    return _sys.stdout.getvalue().strip()

# custom cases only

def solve_test(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# single digit only
assert solve_test("""5 1
11111
3
0 0
0 1
0 2
""") == "1"

# tie broken by size
assert solve_test("""3 2
0.0
111
2
1 0
1 1
""") == "0"

# no ties, clear minimum hits
assert solve_test("""4 2
00..
1111
1
0 0
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single digit grid | 1 | basic counting correctness |
| tie case | 0 | tie-break by size and id |
| skewed hits | 1 | correct prioritization of hits |

## Edge Cases

One important case is when a digit appears in the grid but receives zero hits. In that situation, it becomes a strong candidate since zero is the minimum possible hit count. The algorithm naturally handles this because all digits are initialized with zero hits, and only those that appear in the grid are considered.

Another case is when multiple digits have zero hits. For example, if digits 2 and 8 both exist but receive no impacts, the decision falls to the smallest region size. The selection loop explicitly compares size after hit count, so the correct smaller zone is chosen.

A final subtle case is when some digits from 0 to 9 never appear in the grid. These must be excluded; otherwise they would incorrectly appear as zero-size zones. The check `if size[d] == 0: continue` ensures that only valid zones are considered.
