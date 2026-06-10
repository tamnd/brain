---
title: "CF 1583C - Omkar and Determination"
description: "We are given a rectangular board where each cell is either blocked by an X or empty. From an empty cell we may move only upward or leftward. A cell is called exitable if some sequence of such moves lets us leave the grid. The question is not to simulate those moves."
date: "2026-06-10T09:47:33+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1583
codeforces_index: "C"
codeforces_contest_name: "Technocup 2022 - Elimination Round 1"
rating: 1700
weight: 1583
solve_time_s: 136
verified: true
draft: false
---

[CF 1583C - Omkar and Determination](https://codeforces.com/problemset/problem/1583/C)

**Rating:** 1700  
**Tags:** data structures, dp  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular board where each cell is either blocked by an `X` or empty. From an empty cell we may move only upward or leftward. A cell is called exitable if some sequence of such moves lets us leave the grid. The question is not to simulate those moves. Instead, for many intervals of columns, we must decide whether the pattern of exitable cells uniquely determines the original placement of blocked cells inside that column range.

Each query takes a contiguous set of columns and asks whether two different obstacle configurations could produce exactly the same exitability pattern. If no ambiguity exists, we answer `YES`. Otherwise we answer `NO`.

The product `n × m` is at most `10^6`, so processing the whole grid once is affordable. The number of queries reaches `2·10^5`, which rules out any solution that scans a whole subgrid for every query. Even a linear scan over the width of the interval would lead to roughly `2·10^11` operations in the worst case. Query processing must be constant or logarithmic time.

The tricky part is understanding what kind of local pattern creates ambiguity.

Consider

```
.X
X.
```

The lower-left cell and upper-right cell are both blocked. These two obstacles form a corner that prevents information from propagating. The same exitability pattern would appear if the bottom-right cell were blocked as well. A careless solution that only counts blocked cells would miss this.

Another subtle case is a single column.

```
X
.
X
```

Every query whose left and right endpoints are the same must return `YES`, because there is no pair of adjacent columns that can create ambiguity.

A third edge case appears when several bad positions exist, but all of them lie outside the query interval.

```
..X.
.X..
....
```

Suppose the only problematic boundary is between columns 2 and 3. Query `[1,2]` should still return `YES`. A global answer for the whole grid is not enough, because different column ranges behave differently.

## Approaches

A brute-force solution would examine every query independently. For a column interval `[l,r]`, we could inspect the corresponding subgrid and determine whether any ambiguous structure exists inside it. This approach is correct because it directly checks the queried region, but in the worst case each query touches nearly `10^6` cells. With `2·10^5` queries, the total work becomes around `2·10^11` operations, which is far beyond the limit.

The key observation is that ambiguity arises from only one type of local configuration. Suppose cell `(i,j)` and cell `(i-1,j+1)` are both blocked. Then these two obstacles form a diagonal corner:

```
. X
X .
```

Once such a pattern exists across two neighboring columns, the exact arrangement of some cells becomes impossible to reconstruct from exitability information alone.

This means that every problematic structure can be represented by the boundary between two adjacent columns. For each column `j`, we only need to know whether some row contains both `(i,j)` and `(i-1,j+1)` blocked. If so, the boundary between columns `j` and `j+1` is bad.

A query `[l,r]` is invalid exactly when at least one bad boundary lies between those columns. That converts the problem into a range existence query over a one-dimensional array, which is easily handled using prefix maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(qnm) | O(1) | Too slow |
| Optimal | O(nm + q) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the grid and create an array `bad` of length `m+1`, initially filled with zeroes.
2. For every cell `(i,j)` with `i ≥ 1` and `j ≥ 1`, check whether both `(i,j-1)` and `(i-1,j)` contain `X`.

These two cells form the diagonal pattern

```
. X
X .
```

whose existence creates ambiguity.
3. If such a pair exists, mark column boundary `j` as bad by setting `bad[j]=1`.

The value `j` represents the boundary between columns `j` and `j+1` in one-based indexing.
4. Build a prefix sum array `pref`.

`pref[j]` stores the number of bad boundaries among positions `1…j`.
5. For each query `[l,r]`, compute

```
pref[r-1] - pref[l-1]
```

This quantity counts bad boundaries lying strictly inside the interval.
6. If the count equals zero, output `YES`. Otherwise output `NO`.

### Why it works

Every loss of information comes from a diagonal pair of blocked cells occupying opposite corners of a `2×2` square. Such a pair prevents us from distinguishing between several obstacle configurations that produce the same exitability pattern.

A query interval is determinable precisely when none of its neighboring column pairs contains such a diagonal conflict. Since every bad configuration is localized to a single boundary between adjacent columns, storing all bad boundaries and answering range queries over them captures exactly the condition required. No bad boundary inside the interval means no ambiguity is possible, while the presence of even one bad boundary already creates multiple valid grids.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

bad = [0] * (m + 1)

for i in range(1, n):
    for j in range(1, m):
        if grid[i][j - 1] == 'X' and grid[i - 1][j] == 'X':
            bad[j] = 1

pref = [0] * (m + 1)
for j in range(1, m + 1):
    pref[j] = pref[j - 1] + bad[j]

q = int(input())
ans = []

for _ in range(q):
    l, r = map(int, input().split())
    if pref[r - 1] - pref[l - 1] == 0:
        ans.append("YES")
    else:
        ans.append("NO")

sys.stdout.write("\n".join(ans))
```

The nested loop scans every `2×2` square indirectly. Whenever the upper-right and lower-left cells are both blocked, the boundary between those columns becomes problematic.

The array `bad` uses one-based boundary numbering. Position `j` corresponds to the border between columns `j` and `j+1`. This indexing is easy to get wrong. The query `[l,r]` contains boundaries `l,l+1,…,r-1`, which explains the expression `pref[r-1]-pref[l-1]`.

Integer overflow is not an issue because all counts are at most `m≤10^6`.

## Worked Examples

### Example 1

Input:

```
4 5
..XXX
...X.
...X.
...X.
```

The detected bad boundaries are:

| Row | Column pair producing conflict | Boundary marked |
| --- | --- | --- |
| 1 | none | - |
| 2 | none | - |
| 3 | columns 4 and 5 | 4 |
| 4 | columns 4 and 5 | 4 |

Thus

| Boundary | bad | Prefix |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |
| 4 | 1 | 1 |
| 5 | 0 | 1 |

For query `[1,3]`:

| l | r | pref[r-1] | pref[l-1] | Difference | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 0 | 0 | YES |

For query `[1,5]`:

| l | r | pref[r-1] | pref[l-1] | Difference | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 0 | 1 | NO |

This example shows that a single bad boundary affects every interval containing it.

### Example 2

Grid:

```
3 3
...
...
...
```

No conflicts exist.

| Boundary | bad | Prefix |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |

For any query the difference of prefix sums is zero, so every answer is `YES`.

This example confirms that an entirely empty grid is always uniquely determined.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm + q) | One pass over the grid and constant work per query |
| Space | O(m) | Arrays `bad` and `pref` |

Since `nm≤10^6`, the preprocessing phase performs about one million operations. Answering `2·10^5` queries in constant time easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    bad = [0] * (m + 1)

    for i in range(1, n):
        for j in range(1, m):
            if grid[i][j - 1] == 'X' and grid[i - 1][j] == 'X':
                bad[j] = 1

    pref = [0] * (m + 1)
    for j in range(1, m + 1):
        pref[j] = pref[j - 1] + bad[j]

    q = int(input())
    ans = []

    for _ in range(q):
        l, r = map(int, input().split())
        ans.append("YES" if pref[r - 1] - pref[l - 1] == 0 else "NO")

    return "\n".join(ans)

# provided sample
assert run("""4 5
..XXX
...X.
...X.
...X.
5
1 3
3 3
4 5
5 5
1 5
""") == """YES
YES
NO
YES
NO"""

# minimum size
assert run("""1 1
.
1
1 1
""") == "YES"

# all blocked
assert run("""2 2
XX
XX
1
1 2
""") == "YES"

# one bad boundary
assert run("""2 2
.X
X.
1
1 2
""") == "NO"

# boundary exclusion
assert run("""3 4
..X.
.X..
....
2
1 2
2 4
""") == """YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | YES | Minimum dimensions |
| All cells blocked | YES | Absence of diagonal conflicts |
| `.X / X.` | NO | Single bad boundary |
| Mixed 3×4 example | YES, NO | Correct interval boundaries |

## Edge Cases

A single-column query contains no neighboring column pairs.

```
3 1
X
.
X
1
1 1
```

The `bad` array remains zero because there are no boundaries at all. The query computes `pref[0]-pref[0]=0`, so the answer is `YES`.

Consider the diagonal conflict

```
2 2
.X
X.
1
1 2
```

During preprocessing, at `(1,1)` we find that the lower-left and upper-right cells are both `X`, so `bad[1]=1`. The query evaluates `pref[1]-pref[0]=1`, producing `NO`.

Finally, suppose the conflict lies outside the queried interval:

```
3 4
..X.
.X..
....
2
1 2
2 4
```

Only boundary 2 is marked bad. For `[1,2]`, the difference is `pref[1]-pref[0]=0`, so the answer is `YES`. For `[2,4]`, the difference becomes `pref[3]-pref[1]=1`, producing `NO`. The algorithm isolates each interval correctly instead of using a single global decision.
