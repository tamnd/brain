---
title: "CF 104180H - Not-so Beautiful Painting"
description: "We are given a very large rectangular canvas, conceptually a grid with coordinates up to $10^9 times 10^9$. On this canvas, Bob has already painted several axis-aligned rectangles."
date: "2026-07-02T00:44:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104180
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 2 (Beginner)"
rating: 0
weight: 104180
solve_time_s: 63
verified: true
draft: false
---

[CF 104180H - Not-so Beautiful Painting](https://codeforces.com/problemset/problem/104180/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large rectangular canvas, conceptually a grid with coordinates up to $10^9 \times 10^9$. On this canvas, Bob has already painted several axis-aligned rectangles. These rectangles do not overlap with each other, so each painted cell belongs to at most one rectangle.

After the painting is finished, a set of vertical columns is washed away by rain. Each washed column removes every painted cell whose column index matches one of the given values. The task is to compute how many painted cells remain after deleting all painted cells that lie in those washed columns.

The input consists of non-overlapping rectangles described by their bottom-left and top-right corners, and a list of column indices that are destroyed. The output is the total remaining painted area after removing all painted cells in those columns.

The constraints allow up to $2 \cdot 10^5$ rectangles and $2 \cdot 10^5$ washed columns, while coordinates can be as large as $10^9$. This immediately rules out any grid-based simulation. Even storing per-cell or per-column information explicitly is impossible. Any valid solution must reduce the problem to operations on intervals or aggregated counts, ideally in $O((N + M) \log N)$ or $O(N + M)$.

A subtle point is that rectangles are disjoint. This removes the need for coordinate compression across overlapping shapes, and guarantees that the contribution of each rectangle can be computed independently and safely summed.

Edge cases arise from how columns interact with rectangles:

A rectangle of zero width in practice can occur if $c_1 = c_2$, meaning a single column strip. If that column is washed, the entire rectangle disappears.

Example:

Input:

```
1 1
3 1 3 5
3
```

Output:

```
0
```

A naive per-cell interpretation might still count it incorrectly if it assumes positive width without considering degenerate rectangles.

Another edge case is when no washed columns intersect any rectangle. The answer should equal the total sum of rectangle areas.

Example:

```
1 2
1 1 3 3
10
20
```

Output:

```
9
```

Finally, if many rectangles overlap the same column range but are disjoint in space, we must avoid double counting, which is guaranteed by the problem statement but easy to accidentally reintroduce if processing is done per column without care.

## Approaches

A direct approach would expand every rectangle into unit cells and subtract washed columns. This is immediately infeasible. A single rectangle can cover up to $10^{18}$ cells in the worst case, and even iterating over columns per rectangle would degrade to $O(N \cdot \text{width})$.

A better first observation is that washing affects only columns, not rows. Inside a given rectangle, every column contributes exactly its height to the total painted area. So each rectangle can be seen as a contribution of its vertical height applied uniformly across its column interval $[c_1, c_2]$. The problem becomes: for each rectangle, compute how many of its columns are not in the removed set, and multiply by its height.

The remaining difficulty is that the set of removed columns is large and arbitrary. Checking membership per column is too slow. Instead, we sort the removed columns and use binary search or a pointer sweep to count intersections between a rectangle interval and the deleted set.

Since rectangles do not overlap, we can process each independently. For each rectangle, we count how many deleted columns lie in its horizontal range using binary search on a sorted array. Subtracting this from total width gives surviving columns.

This reduces the problem to sorting the $M$ columns and answering $N$ range-count queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (cell/column simulation) | $O(N \cdot W)$ | $O(W)$ | Too slow |
| Optimal (sort + binary search per rectangle) | $O((N+M)\log M)$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

We convert the problem into counting how many “good” columns remain inside each rectangle.

1. Read all washed column indices and sort them. Sorting is necessary so we can efficiently count how many lie in any interval using binary search. Without sorting, each query would require scanning all columns.
2. Initialize the final answer to zero. We will accumulate contributions from each rectangle independently since they do not overlap.
3. For each rectangle, compute its vertical height as $r_2 - r_1 + 1$. This represents how much each valid column contributes in that rectangle.
4. Determine the total number of columns in the rectangle’s horizontal span, which is $c_2 - c_1 + 1$.
5. Use binary search to count how many washed columns lie in $[c_1, c_2]$. This is done by finding the first index $\ge c_1$ and the first index $> c_2$, and subtracting the two positions.
6. Subtract washed columns from total columns to obtain surviving columns inside the rectangle.
7. Multiply surviving columns by rectangle height and add to the answer.

Each rectangle is handled independently, so we never risk double counting or interference between regions.

### Why it works

The key structural property is that rectangles do not overlap, which makes area additive. Each rectangle contributes a rectangular block of cells, and washing acts independently on columns, removing entire vertical slices uniformly across all rectangles. This means the survival of a cell depends only on its column index, not on which rectangle it belongs to. As a result, each rectangle can be evaluated by projecting the global set of removed columns onto its interval and scaling by height. The binary search step exactly computes this projection size.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    rects = []
    for _ in range(n):
        r1, c1, r2, c2 = map(int, input().split())
        rects.append((r1, c1, r2, c2))
    
    washed = [int(input()) for _ in range(m)]
    washed.sort()
    
    import bisect
    
    ans = 0
    
    for r1, c1, r2, c2 in rects:
        height = r2 - r1 + 1
        total_cols = c2 - c1 + 1
        
        left = bisect.bisect_left(washed, c1)
        right = bisect.bisect_right(washed, c2)
        
        bad_cols = right - left
        good_cols = total_cols - bad_cols
        
        if good_cols > 0:
            ans += good_cols * height
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting all washed columns so that we can query ranges efficiently. For each rectangle, we compute its geometric contribution in terms of height and width. The bisect operations isolate exactly how many washed columns fall into the rectangle’s horizontal interval. Subtracting these gives the number of surviving columns, and multiplying by height converts column count into area.

A common mistake is forgetting that each column contributes the full height, not just a single cell. Another is miscomputing the interval boundaries, especially since both endpoints are inclusive. Using `bisect_left` and `bisect_right` correctly ensures inclusive range counting without manual off-by-one adjustments.

## Worked Examples

### Sample 1

Input:

```
4 3
3 1 5 4
1 5 4 6
1 2 1 3
5 5 5 5
2
4
5
```

Sorted washed columns: [2, 4, 5]

We process each rectangle:

| Rectangle | Height | Column Range | Total cols | Bad cols | Good cols | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| (3,1,5,4) | 3 | [1,4] | 4 | 2 (2,4) | 2 | 6 |
| (1,5,4,6) | 4 | [5,6] | 2 | 1 (5) | 1 | 4 |
| (1,2,1,3) | 1 | [2,3] | 2 | 1 (2) | 1 | 1 |
| (5,5,5,5) | 1 | [5,5] | 1 | 1 (5) | 0 | 0 |

Final answer is 11.

This trace shows how each rectangle is treated independently and how washed columns are only relevant through intersection counts.

### Sample 2

Input:

```
3 3
1 5 3 7
1 8 2 8
4 6 5 8
1
3
10
```

Sorted washed columns: [1, 3, 10]

| Rectangle | Height | Column Range | Total cols | Bad cols | Good cols | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| (1,5,3,7) | 3 | [5,7] | 3 | 0 | 3 | 9 |
| (1,8,2,8) | 2 | [8,8] | 1 | 0 | 1 | 2 |
| (4,6,5,8) | 2 | [6,8] | 3 | 0 | 3 | 6 |

Total is 17.

This example confirms that washed columns outside all rectangle ranges do not affect the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N + M)\log M)$ | Sorting washed columns dominates $O(M \log M)$, and each rectangle query uses two binary searches |
| Space | $O(M)$ | Storage for sorted list of washed columns |

The constraints allow up to $2 \cdot 10^5$ elements, and logarithmic queries over this range comfortably fit within time limits. The solution avoids any dependence on coordinate size, relying only on sorted event processing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    rects = []
    for _ in range(n):
        rects.append(tuple(map(int, input().split())))
    washed = [int(input()) for _ in range(m)]
    washed.sort()
    import bisect

    ans = 0
    for r1, c1, r2, c2 in rects:
        h = r2 - r1 + 1
        total = c2 - c1 + 1
        l = bisect.bisect_left(washed, c1)
        r = bisect.bisect_right(washed, c2)
        good = total - (r - l)
        ans += good * h
    return str(ans)

# provided samples
assert run("""4 3
3 1 5 4
1 5 4 6
1 2 1 3
5 5 5 5
2
4
5
""") == "11"

assert run("""3 3
1 5 3 7
1 8 2 8
4 6 5 8
1
3
10
""") == "17"

# minimum-size: single cell unaffected
assert run("""1 1
1 1 1 1
2
""") == "1"

# fully washed single rectangle column
assert run("""1 1
1 5 2 5
5
""") == "0"

# all columns safe
assert run("""2 0
1 1 2 2
3 3 4 4
""") == "8"

# boundary overlap check
assert run("""1 3
1 1 3 3
1
2
3
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell safe | 1 | minimal case |
| single column removed | 0 | full wipe of thin rectangle |
| no washed columns | full area | identity behavior |
| full overlap wash | 0 | boundary inclusion correctness |

## Edge Cases

A key edge case is a rectangle that degenerates into a single column. For example:

Input:

```
1 1
2 7 5 7
7
```

The rectangle has height 4 and width 1. The washed column exactly matches it. The binary search finds one bad column inside $[7,7]$, making good columns zero, and the contribution becomes zero. This confirms correctness for width-one intervals.

Another edge case occurs when washed columns lie completely outside all rectangles:

Input:

```
1 2
1 1 3 3
10
20
```

The binary searches return zero bad columns for the rectangle interval $[1,3]$, so the full area is preserved. The algorithm naturally handles this without special casing.

A final subtle case is multiple rectangles with disjoint horizontal intervals but shared washed columns. Since each rectangle independently queries the same sorted array, there is no interference or double counting, and each contribution is computed strictly within its own bounds.
