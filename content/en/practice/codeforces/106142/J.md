---
title: "CF 106142J - \u0420\u0430\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0438"
description: "We are given a very large rectangular grid with n rows and m columns. Some cells are blocked by stones, and all remaining cells are free."
date: "2026-06-21T09:35:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106142
codeforces_index: "J"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 25, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 106142
solve_time_s: 62
verified: true
draft: false
---

[CF 106142J - \u0420\u0430\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0438](https://codeforces.com/problemset/problem/106142/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large rectangular grid with `n` rows and `m` columns. Some cells are blocked by stones, and all remaining cells are free. The task is to count how many distinct placements of a `2 × 2` square exist such that all four cells of the square lie inside the grid and none of them contain a stone.

A placement of the `2 × 2` square is fully determined by its top-left cell. If the top-left corner is `(i, j)`, then the square covers `(i, j)`, `(i, j+1)`, `(i+1, j)`, `(i+1, j+1)`. Therefore valid placements correspond exactly to top-left corners in the range `1 ≤ i ≤ n-1` and `1 ≤ j ≤ m-1` such that all four covered cells are free.

The constraints are extreme for the grid size, with `n` and `m` up to one billion. This makes any approach that iterates over the grid impossible. The number of blocked cells is at most 200,000, which is small enough to iterate over directly. This imbalance is the central structural hint: the solution must depend only on the blocked cells, not on the grid dimensions.

A naive attempt would enumerate all `(n-1)(m-1)` possible `2 × 2` placements and check whether each is valid. This is infeasible because the grid can contain up to `10^18` candidate positions.

A second naive idea is to iterate over each blocked cell and mark all affected `2 × 2` squares. This is closer to correct, but care is needed because multiple stones can invalidate the same square, so duplicates must be handled properly.

Edge cases that commonly break incorrect solutions include grids with no stones, grids where stones lie on the border (affecting fewer squares), and cases where multiple stones contribute to the same invalid `2 × 2` region. For example, if two stones lie inside the same `2 × 2` area, that square must still be counted only once as invalid.

## Approaches

The direct counting approach starts from the observation that every valid placement corresponds to a top-left corner of a `2 × 2` block. Without any stones, the answer is simply `(n - 1) × (m - 1)`.

Introducing stones only removes some of these placements. A placement becomes invalid if at least one of its four cells contains a stone. Instead of checking all placements, we invert the perspective: start from all possible placements and subtract those that are blocked.

The key difficulty is avoiding double counting. Each stone affects up to four possible top-left corners of a `2 × 2` square that includes it. If we collect all such affected positions and treat them as invalid placements, duplicates naturally arise when multiple stones influence the same square. This suggests using a set to store all invalid top-left corners.

The final answer is the total number of placements minus the number of distinct invalid placements collected from all stones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all squares | O(nm) | O(1) | Too slow |
| Enumerate affected squares from stones | O(k) average | O(k) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of possible `2 × 2` placements in an empty grid as `(n - 1) × (m - 1)`. This represents all top-left corners that could potentially host a square.
2. Maintain a set that will store all top-left corners of `2 × 2` squares that are invalid due to at least one stone.
3. For each stone located at `(x, y)`, determine which `2 × 2` squares it can belong to. A stone can be in a square whose top-left corner is one of `(x, y)`, `(x-1, y)`, `(x, y-1)`, `(x-1, y-1)` provided those coordinates lie within the valid top-left corner bounds.
4. For each such candidate top-left corner `(i, j)`, check whether `1 ≤ i ≤ n-1` and `1 ≤ j ≤ m-1`. If it is valid, insert `(i, j)` into the set of invalid placements.
5. After processing all stones, subtract the size of the invalid set from the total number of placements.

The reason this works is that every invalid `2 × 2` square must contain at least one stone, and therefore must be discovered when processing that stone. Conversely, every square is added at most once in the set regardless of how many stones it contains, because sets eliminate duplicates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    total = (n - 1) * (m - 1)
    
    bad = set()
    
    for _ in range(k):
        x, y = map(int, input().split())
        
        # possible top-left corners of 2x2 blocks containing (x, y)
        candidates = [
            (x, y),
            (x - 1, y),
            (x, y - 1),
            (x - 1, y - 1)
        ]
        
        for i, j in candidates:
            if 1 <= i <= n - 1 and 1 <= j <= m - 1:
                bad.add((i, j))
    
    print(total - len(bad))

if __name__ == "__main__":
    solve()
```

The solution relies on computing the full count first, then removing invalid configurations. The candidate generation step is the critical part: each stone influences only constant many potential placements, so the total work is linear in `k`. The set ensures that overlapping influence from multiple stones does not lead to over-subtraction.

## Worked Examples

### Example 1

Input:

```
3 3 2
1 3
3 3
```

Total possible `2 × 2` placements are `(2 × 2) = 4`.

We process stone `(1, 3)` first.

| Stone | Candidate top-left corners | Valid corners added to bad set |
| --- | --- | --- |
| (1,3) | (1,3), (0,3), (1,2), (0,2) | (1,2) |
| (3,3) | (3,3), (2,3), (3,2), (2,2) | (2,2) |

Now `bad = {(1,2), (2,2)}`.

The answer becomes `4 - 2 = 2`.

This trace shows that each invalid square is captured exactly once even though multiple stones might contribute candidates in general.

### Example 2

Input:

```
3 5 3
2 4
2 2
2 3
```

Total placements are `(2 × 4) = 8`.

All stones lie on row 2 in consecutive columns, which heavily contaminates all `2 × 2` squares crossing that row.

After processing all candidates, every possible top-left corner ends up in the invalid set.

Final result is `0`, matching the fact that every possible `2 × 2` square includes at least one of the blocked cells.

This example demonstrates that the algorithm naturally handles dense clusters of stones without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each stone generates at most four candidate squares, each inserted into a hash set in average constant time |
| Space | O(k) | The set stores at most four entries per stone, but duplicates are merged |

The constraints allow up to 200,000 stones, so both time and memory usage remain comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    total = (n - 1) * (m - 1)
    bad = set()

    for _ in range(k):
        x, y = map(int, input().split())
        for i, j in [(x, y), (x-1, y), (x, y-1), (x-1, y-1)]:
            if 1 <= i <= n - 1 and 1 <= j <= m - 1:
                bad.add((i, j))

    return str(total - len(bad))

assert run("3 3 2\n1 3\n3 3\n") == "2", "sample 1"
assert run("3 5 3\n2 4\n2 2\n2 3\n") == "0", "sample 2"

assert run("2 2 0\n") == "1", "minimum grid no stones"
assert run("2 2 1\n1 1\n") == "0", "single square fully blocked"
assert run("1000000000 1000000000 0\n") == str((10**9-1)*(10**9-1)), "max grid empty"
assert run("3 3 4\n1 1\n1 2\n2 1\n2 2\n") == "0", "all cells of one square blocked"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 0 | 1 | smallest grid with one placement |
| 2 2 1, (1,1) | 0 | single stone destroys only square |
| 10^9 grid, 0 stones | (n-1)(m-1) | large empty grid correctness |
| full 2x2 blocked | 0 | full coverage of one square |

## Edge Cases

A grid with no stones is handled directly by the formula `(n - 1) × (m - 1)` because the set of invalid squares remains empty. The algorithm produces no candidate insertions, so the subtraction does nothing.

A stone on the boundary such as `(1, m)` only contributes to valid top-left corners if they remain inside bounds. The candidate generation naturally filters out invalid coordinates like `(0, m)` or `(1, m)` when `m` exceeds limits for a top-left corner.

When multiple stones lie within the same `2 × 2` region, all of them attempt to insert the same top-left corner into the set. The set ensures that this square is only counted once in the invalid set, preventing over-subtraction.

A fully blocked `2 × 2` region is correctly handled because every stone inside it generates the same top-left candidate, ensuring the square is included in the invalid set exactly once.
