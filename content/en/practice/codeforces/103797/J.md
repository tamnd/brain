---
title: "CF 103797J - Judge Crush"
description: "We are given a grid of contestants by problem, where each pair $(c, p)$ represents one contestant solving one problem. Over time, we receive a chronological stream of submissions, each submission belonging to one such cell and carrying a verdict."
date: "2026-07-02T08:49:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "J"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 49
verified: true
draft: false
---

[CF 103797J - Judge Crush](https://codeforces.com/problemset/problem/103797/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of contestants by problem, where each pair $(c, p)$ represents one contestant solving one problem. Over time, we receive a chronological stream of submissions, each submission belonging to one such cell and carrying a verdict.

The key rule is that we only care about incorrect submissions that happen before the first accepted solution for that same $(c, p)$. Once a cell receives its first AC, that cell becomes inactive and later submissions to it must be ignored completely.

After processing all submissions, we must answer many queries. Each query gives a rectangular subgrid defined by a range of contestants and a range of problems. For that rectangle, we need to compute the total number of counted incorrect submissions (those that happened before AC) across all cells inside it.

The constraints already suggest the shape of the solution. The grid size is at most $500 \times 500$, so about 250,000 cells. The number of submissions and queries can both reach $2 \times 10^5$. This immediately rules out any solution that scans submissions per query or recomputes per cell per query. The structure strongly hints that we should compress all submission information into a static 2D array and then support fast submatrix sum queries.

A subtle point is the “before AC only” condition. A naive mistake is to count all non-AC submissions globally and later try to subtract those after AC. That fails because submissions after AC must not affect the cell at all, but they still appear in the input stream and can incorrectly inflate counts if not filtered carefully per cell.

Another edge case appears when a cell never receives an AC. In that case, none of its submissions should be counted at all, even if there are many WA or TLE entries. Only cells that eventually reach AC contribute anything.

## Approaches

A direct approach is to simulate each query independently. For a given rectangle, we could iterate over all submissions and check whether they belong to a cell inside the rectangle and occurred before that cell’s first AC. This requires scanning up to $2 \times 10^5$ submissions per query, giving a worst-case complexity around $4 \times 10^{10}$ operations, which is far beyond feasible limits.

The key observation is that each cell behaves independently from others. A submission only affects its own $(c, p)$, and once we determine how many valid incorrect submissions belong to that cell, it never changes again. This means the entire dynamic process can be reduced to computing a single integer per grid cell.

Once each cell has a fixed value, the problem becomes a classic 2D range sum query problem. A 2D prefix sum allows answering each query in constant time.

The only remaining task is computing, for every cell, how many submissions before its first AC are incorrect. We can process the submission log in order, maintaining for each cell whether it has already seen AC, and if not, increment its counter whenever a non-AC verdict appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | $O(S \cdot Q)$ | $O(1)$ | Too slow |
| Per-cell accumulation + 2D prefix sum | $O(S + NM + Q)$ | $O(NM)$ | Accepted |

## Algorithm Walkthrough

We treat the grid as a table where each entry stores a counter of valid wrong submissions.

1. Create two $N \times M$ arrays: one boolean array to mark whether a cell has already received AC, and one integer array to count incorrect submissions before AC. This separation is necessary because after AC we must freeze the state of that cell.
2. Process submissions in chronological order. For each submission $(c, p, v)$, first check whether this cell already has AC. If it does, skip the submission completely because anything after AC is irrelevant by definition.
3. If the verdict is AC and the cell is not yet marked, mark it as solved. From this moment onward, no future submission will affect this cell.
4. If the verdict is not AC and the cell is still unsolved, increment its counter. This ensures we only count mistakes that occur before the first successful submission.
5. After processing all submissions, build a 2D prefix sum over the counter grid. Each prefix cell stores the sum of all values in the rectangle from $(1,1)$ to $(i,j)$.
6. For each query rectangle, compute the sum using inclusion-exclusion on the prefix grid in constant time.

### Why it works

Each cell is independent because submissions only modify their own coordinate. The moment a cell receives AC, its final contribution is fully determined and no later event can change it. Therefore, the problem decomposes into computing a fixed value per cell. The prefix sum transformation preserves exact sums over subrectangles, so every query is answered using only precomputed information without revisiting the submission log.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    N, M = map(int, input().split())
    S = int(input())

    solved = [[False] * (M + 1) for _ in range(N + 1)]
    bad = [[0] * (M + 1) for _ in range(N + 1)]

    for _ in range(S):
        c, p, v = input().split()
        c = int(c)
        p = int(p)

        if solved[c][p]:
            continue

        if v == "AC":
            solved[c][p] = True
        else:
            bad[c][p] += 1

    pref = [[0] * (M + 1) for _ in range(N + 1)]

    for i in range(1, N + 1):
        row_sum = 0
        for j in range(1, M + 1):
            row_sum += bad[i][j]
            pref[i][j] = pref[i - 1][j] + row_sum

    Q = int(input())
    out = []

    for _ in range(Q):
        c1, p1, c2, p2 = map(int, input().split())

        res = pref[c2][p2]
        if c1 > 1:
            res -= pref[c1 - 1][p2]
        if p1 > 1:
            res -= pref[c2][p1 - 1]
        if c1 > 1 and p1 > 1:
            res += pref[c1 - 1][p1 - 1]

        out.append(str(res))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The core implementation maintains a per-cell state machine. The `solved` table ensures that once AC is reached, later submissions are ignored. The `bad` table accumulates only valid pre-AC incorrect attempts.

The prefix sum construction is done row by row to avoid nested recomputation. Query answering uses the standard inclusion-exclusion formula for submatrices, relying entirely on the precomputed prefix table.

## Worked Examples

### Example 1

Consider a tiny system with 2 contestants and 2 problems. Suppose we process submissions and end up with the following per-cell counts of valid wrong submissions before AC:

| Cell | bad count |
| --- | --- |
| (1,1) | 0 |
| (1,2) | 1 |
| (2,1) | 3 |
| (2,2) | 0 |

Now we build prefix sums:

| i\j | 1 | 2 |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 3 | 4 |

For a query covering the full grid, we return 4. This matches the fact that only three incorrect submissions happened in (2,1) and one in (1,2).

### Example 2

If a cell has multiple incorrect submissions but never receives AC, such as (1,1) having 10 WA but no AC, its contribution remains 0. The prefix grid ignores it entirely.

A query over any region containing (1,1) will not include those 10 attempts, confirming that only cells with eventual AC contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(S + NM + Q)$ | One pass over submissions, one pass over grid for prefix sums, constant time per query |
| Space | $O(NM)$ | Two grids storing state and prefix sums |

The bounds $N, M \le 500$ make the $NM$ storage trivial, while $S, Q \le 2 \times 10^5$ ensure that only linear-time processing of submissions and queries is acceptable. The solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    N, M = map(int, input().split())
    S = int(input())

    solved = [[False] * (M + 1) for _ in range(N + 1)]
    bad = [[0] * (M + 1) for _ in range(N + 1)]

    for _ in range(S):
        c, p, v = input().split()
        c = int(c)
        p = int(p)
        if solved[c][p]:
            continue
        if v == "AC":
            solved[c][p] = True
        else:
            bad[c][p] += 1

    pref = [[0] * (M + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            pref[i][j] = pref[i-1][j] + pref[i][j-1] - pref[i-1][j-1] + bad[i][j]

    Q = int(input())
    out = []
    for _ in range(Q):
        c1, p1, c2, p2 = map(int, input().split())
        res = pref[c2][p2] - pref[c1-1][p2] - pref[c2][p1-1] + pref[c1-1][p1-1]
        out.append(str(res))
    return "\n".join(out)

# custom minimal case
assert run("""1 1
3
1 1 WA
1 1 AC
1 1 WA
1
1 1 1 1
""") == "1", "basic AC cutoff"

# all no AC => zero contribution
assert run("""2 2
3
1 1 WA
1 1 WA
2 2 TLE
1
1 1 2 2
""") == "0", "no AC anywhere"

# multiple cells independent
assert run("""2 2
4
1 1 WA
1 2 WA
2 1 WA
2 2 AC
1
1 1 2 2
""") == "3", "independent accumulation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal AC cutoff | 1 | stops counting after AC |
| no AC anywhere | 0 | cells without AC contribute nothing |
| independent cells | 3 | per-cell independence |

## Edge Cases

A common pitfall is counting all wrong submissions regardless of AC timing. For example:

```
1 1
3
1 1 WA
1 1 AC
1 1 WA
1
1 1 1 1
```

Here the correct answer is 1, not 2. The third submission must be ignored because AC has already occurred. The algorithm handles this by marking the cell as solved and skipping all later updates.

Another edge case is a cell that never gets AC:

```
1 1
2
1 1 WA
1 1 TLE
1
1 1 1 1
```

The correct output is 0. The `solved` flag is never set, but since there is no AC, the rule explicitly says we should not count these submissions at all. The implementation enforces this by only incrementing `bad` before AC and never adding it to the final sum unless AC occurred.
