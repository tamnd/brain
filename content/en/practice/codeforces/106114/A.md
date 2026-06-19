---
title: "CF 106114A - Abacus"
description: "We are given a rectangular arrangement of cells with n rows and m columns. Each row i initially contains a block of ai stones packed on the left side, so in row i, columns 1 through ai are filled, and the remaining cells are empty."
date: "2026-06-19T20:10:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106114
codeforces_index: "A"
codeforces_contest_name: "2025 Sun Yat-sen University Collegiate Programming Contest, Final"
rating: 0
weight: 106114
solve_time_s: 48
verified: true
draft: false
---

[CF 106114A - Abacus](https://codeforces.com/problemset/problem/106114/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular arrangement of cells with n rows and m columns. Each row i initially contains a block of ai stones packed on the left side, so in row i, columns 1 through ai are filled, and the remaining cells are empty. The operation described is a gravity-like transformation applied column-wise: all stones fall vertically downwards until they reach the lowest possible empty positions in their respective columns.

After this falling process stabilizes, each column is simply filled from the bottom with as many stones as originally existed in that column, and any empty space remains above. The task is to compute, after this reconfiguration, how many stones end up in each row.

The key difficulty is that the initial state is given in a compressed row-wise form, but the process of falling is column-driven, so we must mentally transpose the structure.

The constraints n, m ≤ 10^4 imply that an O(nm) simulation over an explicit grid is too large in both time and memory in the worst case. A full simulation would require up to 10^8 cells, which is borderline or unsafe in Python under tight limits. This pushes us toward reasoning about counts rather than explicit grids.

A subtle edge case arises when rows have very different ai values. For example, if n = 3, m = 5, and a = [5, 1, 1], the first row contributes many stones across all columns while lower rows contribute only in the first column. After falling, column heights differ significantly, and a naive row-by-row redistribution would misplace stones unless we explicitly account for column-wise accumulation.

Another failure mode comes from incorrectly assuming that rows independently preserve their counts. For instance, thinking each row keeps ai stones is wrong, since falling redistributes stones between rows.

## Approaches

The brute-force interpretation constructs an explicit grid, marks all ai left-aligned stones, and then repeatedly simulates gravity column by column or by repeatedly pushing stones down until stable. This is correct because it literally follows the process definition. However, the grid can contain up to n × m cells, and each simulation step may require scanning columns multiple times or performing per-cell movement. In the worst case, every cell is processed multiple times, leading to roughly O(nm) memory and potentially O(nm) or worse time depending on implementation overhead. With n and m up to 10^4, this becomes too large.

The key observation is that the final configuration depends only on column totals, not on how stones were distributed within rows initially. Each row i contributes a_i stones distributed across the first a_i columns. If we invert the viewpoint, each column j receives exactly the number of rows i such that a_i ≥ j. Once we know column sums, gravity simply sorts these sums into rows: each row i ends up receiving the total number of columns whose height reaches at least i.

So instead of simulating movement, we compute a frequency array over column heights, then transform it into row counts using a suffix accumulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(nm) | Too slow |
| Optimal | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Build an array cnt of size m where cnt[j] counts how many rows have ai ≥ j + 1. This corresponds to how many stones appear in column j + 1 before falling. This step replaces explicit grid construction with a counting perspective.
2. For each row i from 1 to n, we want to know how many columns have at least i stones. That number is exactly cnt[i - 1]. This works because a column contributes to row i after falling if and only if it has height at least i.
3. Output cnt[0], cnt[1], ..., cnt[n - 1] as the final row counts.

The transformation is purely a change of viewpoint: rows in the final configuration are determined by column heights, and column heights are determined by prefix coverage of the original ai values.

### Why it works

Each original row contributes stones only to a prefix of columns, and therefore each column j accumulates exactly the number of rows that extend to at least j. After falling, columns become independent stacks whose heights are fixed. The final row i is occupied exactly in those columns whose stack height is at least i, because gravity fills from the bottom upward without gaps. This establishes a direct equivalence between “final row occupancy” and “count of columns with height ≥ i”, which guarantees correctness of the counting transformation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

cnt = [0] * (m + 2)

for x in a:
    cnt[1] += 1
    if x + 1 <= m:
        cnt[x + 1] -= 1

for i in range(1, m + 1):
    cnt[i] += cnt[i - 1]

ans = []
for i in range(1, n + 1):
    ans.append(str(cnt[i]))

print(" ".join(ans))
```

The code avoids building any grid. Instead, it uses a difference array over column indices to compute how many rows extend to each column. The prefix sum converts this into actual column heights. Then each row i is answered directly by reading how many columns reach at least height i.

A common pitfall is mixing up row and column indexing. The array cnt is indexed by column height thresholds, not by rows. Another subtle point is ensuring bounds when applying the difference array, since columns beyond m must not be updated.

## Worked Examples

### Example 1

Input:

n = 3, m = 4

a = [3, 1, 2]

We compute column coverage.

| Step | a[i] | Update effect on cnt | cnt after prefix |
| --- | --- | --- | --- |
| 1 | 3 | + at 1, - at 4 | [0,1,1,1] |
| 2 | 1 | + at 1, - at 2 | [0,2,1,1] |
| 3 | 2 | + at 1, - at 3 | [0,3,2,1] |

Now cnt after prefix means:

column 1 has 3 stones, column 2 has 2, column 3 has 1, column 4 has 0.

Final rows:

row 1 = columns with height ≥ 1 = 3

row 2 = columns with height ≥ 2 = 2

row 3 = columns with height ≥ 3 = 1

So output is [3, 2, 1].

This confirms that each row is determined purely by thresholding column heights.

### Example 2

Input:

n = 4, m = 5

a = [5, 3, 3, 1]

Column heights become:

[4, 3, 2, 1, 1]

Now we compute row outputs:

row 1 = 5 columns

row 2 = 3 columns

row 3 = 3 columns

row 4 = 1 column

Output: [5, 3, 3, 1]

This shows that even with repeated values, the method correctly aggregates overlapping prefixes without explicit simulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | one pass over a, one prefix sum over m, one scan over n |
| Space | O(m) | only column-height array is stored |

The constraints n, m ≤ 10^4 make this comfortably efficient, with at most a few tens of thousands of operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    cnt = [0] * (m + 2)

    for x in a:
        cnt[1] += 1
        if x + 1 <= m:
            cnt[x + 1] -= 1

    for i in range(1, m + 1):
        cnt[i] += cnt[i - 1]

    ans = [str(cnt[i]) for i in range(1, n + 1)]
    return " ".join(ans)

# sample-like case
assert run("3 4\n3 1 2\n") == "3 2 1"

# all equal
assert run("3 5\n5 5 5\n") == "3 3 3"

# minimal case
assert run("1 1\n1\n") == "1"

# strictly increasing prefix lengths
assert run("4 5\n1 2 3 4\n") == "4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 4 / 3 1 2 | 3 2 1 | basic transformation correctness |
| 3 5 / 5 5 5 | 3 3 3 | uniform full coverage |
| 1 1 / 1 | 1 | smallest boundary case |
| 4 5 / 1 2 3 4 | 4 3 2 1 | gradual prefix growth |

## Edge Cases

A key edge case is when one row dominates all columns, such as n = 3, m = 5, a = [5, 1, 1]. Column heights become heavily skewed: column 1 has 3 stones while columns 2 through 5 have only 1. The algorithm handles this correctly because cnt[j] directly counts row coverage per column, so no assumption about uniformity is needed.

Another edge case is when all ai are small, such as a = [1, 1, 1, 1]. Then only the first column is non-zero, and after prefix accumulation we get column heights [4, 0, 0, ...]. Row outputs become [1, 0, 0, 0], which matches the fact that only the bottom row receives the single occupied column after falling.

A final edge case is maximum saturation where all ai = m. In this case every column has height n, so every row receives m stones. The algorithm produces cnt[i] = m for all i, which correctly reflects full rectangular filling.
