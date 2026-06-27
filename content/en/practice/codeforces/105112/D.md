---
title: "CF 105112D - Date Picker"
description: "We are given a weekly calendar encoded as a 7 by 24 grid. Each row corresponds to a day and each column corresponds to an hour. A cell is either free or blocked. Free means you are available at that day and hour, blocked means you are busy."
date: "2026-06-27T19:57:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105112
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC Northwestern European Regional Programming Contest (NWERC 2023)"
rating: 0
weight: 105112
solve_time_s: 67
verified: true
draft: false
---

[CF 105112D - Date Picker](https://codeforces.com/problemset/problem/105112/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weekly calendar encoded as a 7 by 24 grid. Each row corresponds to a day and each column corresponds to an hour. A cell is either free or blocked. Free means you are available at that day and hour, blocked means you are busy.

A “date picker” process then happens in two independent steps. First, you must choose at least $d$ days out of the 7. Second, you must choose at least $h$ hours out of the 24. After these choices are made, a meeting time is sampled uniformly from the Cartesian product of the chosen days and chosen hours. Every pair $(day, hour)$ in the selected sets is equally likely.

The probability we care about is the probability that the sampled slot is free in the original calendar. We are allowed to choose the sets of days and hours optimally to maximize this probability.

The output is this maximum achievable probability.

The key subtlety is that the randomness is over pairs, not over days or hours separately. Once we pick a set of days and hours, every combination is equally likely, so the quality of a choice is determined by how many free cells lie inside the induced submatrix, normalized by its area.

The grid is extremely small: only 7 by 24. This immediately rules out anything exponential in both dimensions. A naive approach that tries all subsets of days and hours would involve $2^7 \cdot 2^{24}$, which is far too large. Even more targeted enumeration of both sides is too slow if done independently.

A few edge cases are easy to mis-handle:

If all cells are blocked, the answer must be 0 regardless of choices. A greedy approach that tries to maximize rows or columns independently may still produce a nonzero ratio if it incorrectly normalizes.

If $d = 7$ and $h = 24$, the choice is forced, and the answer is simply the fraction of free cells in the whole grid.

If $d = 1$ or $h = 1$, the problem reduces to choosing a single row or column set, and naive reasoning about “independent optimization per dimension” can fail because adding more rows or columns increases both numerator and denominator in a coupled way.

## Approaches

A brute-force strategy would try every subset of days and every subset of hours. For each pair of subsets, we compute how many free cells lie inside the induced submatrix and divide by its size. This is correct because it exactly matches the probability definition. The issue is scale: there are $2^7 = 128$ row subsets and $2^{24} \approx 16$ million column subsets, which leads to billions of evaluations even before counting the cost of computing sums inside each submatrix.

The structure becomes manageable once we separate the roles of rows and columns. The grid is small in rows, so we can enumerate all row subsets efficiently. For any fixed set of rows, the problem collapses into choosing a good subset of columns.

Fix a row subset $S$. For each column $j$, we can compute how many free cells appear in that column among the chosen rows. Call this value $c[j]$. Now the problem is purely one-dimensional: we must choose at least $h$ columns, and each chosen column contributes independently $c[j]$ to the numerator. The resulting probability for a column set $T$ is

$$\frac{\sum_{j \in T} c[j]}{|S| \cdot |T|}.$$

For fixed $S$, the denominator in rows is constant, so the inner problem becomes maximizing the average value of chosen columns, subject to selecting at least $h$ of them.

This is a classic structure: once column contributions are known, the best subset of a given size is always the top-k columns by $c[j]$. The only remaining question is which size $k \ge h$ is optimal.

Thus, for each row subset, we sort the 24 column scores, compute prefix sums, and evaluate the best ratio over all $k \ge h$.

This reduces the problem to trying all row subsets and solving a small sorted optimization problem per subset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over rows and columns | $O(2^7 \cdot 2^{24} \cdot 7 \cdot 24)$ | $O(1)$ | Too slow |
| Enumerate row subsets + greedy columns | $O(2^7 \cdot 24 \log 24)$ | $O(24)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Enumerate every subset of the 7 rows using a bitmask. Each subset represents a possible choice of days. This is feasible because there are only 128 subsets, and any optimal solution must correspond to one of these subsets.
2. For each row subset $S$, build an array $c[0..23]$ where $c[j]$ counts how many chosen rows have a free cell in column $j$. This compresses the 2D structure into a 1D scoring system over hours.
3. If the number of selected rows is less than $d$, skip this subset. Even though the problem allows “at least $d$” days, using fewer than $d$ is invalid and must be discarded.
4. Sort the column scores $c[j]$ in descending order. This ordering ensures that for any fixed number of columns $k$, the optimal choice is always the first $k$, since all contributions are independent and additive.
5. Compute prefix sums over the sorted array so that the sum of the best $k$ columns can be retrieved in constant time.
6. For each $k$ from $h$ to 24, compute the value

$$\frac{\text{prefix}[k]}{k \cdot |S|}$$

and track the maximum over all $k$. The division by $|S|$ reflects that each chosen day multiplies the number of candidate meeting slots.
7. Take the maximum over all row subsets.

### Why it works

For a fixed row subset, every column contributes independently to the total number of free pairs. Because the probability depends only on the sum of selected column contributions divided by the product of selected set sizes, the optimal structure for columns must be a prefix of the sorted contributions. Any deviation, such as replacing a higher-value column with a lower-value one, strictly decreases the numerator without changing the denominator. This guarantees that restricting attention to sorted prefixes loses no optimal solutions, and enumerating row subsets ensures all possible row combinations are considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    grid = [input().strip() for _ in range(7)]
    d, h = map(int, input().split())

    best = 0.0

    for mask in range(1 << 7):
        rows = [i for i in range(7) if mask & (1 << i)]
        r = len(rows)
        if r < d:
            continue

        col = [0] * 24
        for i in rows:
            row = grid[i]
            for j in range(24):
                if row[j] == '.':
                    col[j] += 1

        col.sort(reverse=True)

        pref = [0] * 25
        for i in range(24):
            pref[i + 1] = pref[i] + col[i]

        for k in range(h, 25):
            val = pref[k] / (k * r)
            if val > best:
                best = val

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the decomposition into row subsets and column scoring. The row mask enumerates all possible day selections. For each selection, the column aggregation step builds independent hour scores.

Sorting the 24 column values is safe because it converts the combinatorial column choice into a monotone decision problem where optimal sets are always prefixes. The prefix array allows constant-time evaluation of any candidate size $k$.

The final division by $k \cdot r$ is done per candidate, ensuring we respect the probability definition exactly rather than maximizing raw counts.

## Worked Examples

### Sample 1

We consider one representative row subset that could be optimal after evaluation. Suppose a subset selects $r = 2$ rows. After scanning those rows, we obtain column scores such as:

| Step | Column scores (unsorted) | Sorted | Prefix sum |
| --- | --- | --- | --- |
| After aggregation | [2, 1, 0, 2, ...] | 2,2,1,0,... | 0,2,4,5,... |

For each $k \ge h = 5$, we compute the ratio $\text{prefix}[k]/(2k)$. The best among all row subsets turns out to be 0.8, matching the sample output.

This trace shows how the solution does not fix a single number of columns but instead tries all valid sizes while maintaining optimal prefix structure.

### Sample 2

For a different grid, suppose a row subset of size $r = 3$ produces more balanced column scores:

| Step | Column scores (unsorted) | Sorted | Prefix sum |
| --- | --- | --- | --- |
| After aggregation | [3,2,2,1,...] | 3,2,2,1,... | 0,3,5,7,8,... |

We evaluate $k \ge 8$. For each $k$, the ratio varies slightly, and the best occurs at a specific $k$ where adding more columns starts reducing average quality.

This demonstrates why “always take exactly h columns” is incorrect: increasing the number of columns can either improve or degrade the ratio depending on the tail of the distribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^7 \cdot 24 \log 24)$ | enumerate all row subsets, compute 24 column sums, sort per subset |
| Space | $O(24)$ | only column counters and prefix arrays are stored |

The total work is extremely small: at most 128 iterations, each handling 24 values. Sorting dominates but is trivial at this scale. This easily fits within time limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else solve_and_capture(inp)

def solve_and_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)

    grid = [input().strip() for _ in range(7)]
    d, h = map(int, input().split())

    best = 0.0

    for mask in range(1 << 7):
        rows = [i for i in range(7) if mask & (1 << i)]
        r = len(rows)
        if r < d:
            continue

        col = [0] * 24
        for i in rows:
            for j in range(24):
                if grid[i][j] == '.':
                    col[j] += 1

        col.sort(reverse=True)

        pref = [0] * 25
        for i in range(24):
            pref[i + 1] = pref[i] + col[i]

        for k in range(h, 25):
            best = max(best, pref[k] / (k * r))

    sys.stdin = backup
    return f"{best:.12f}".rstrip('0').rstrip('.')

# provided samples
assert abs(float(run("""\
xxxxxx..xx..xxxxxxxxxxxx
xxxxxxxxxxxxx....xxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxx..xx..xxxxxxxxxxxx
xxxxxxxxxxxxx...x..xxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
2 5
""")) - 0.8) < 1e-6

assert abs(float(run("""\
xxxxxxxxx.....x...xxxxxx
xxxxxxxx..x...x...xxxxxx
xxxxxxxx......x...x.xxxx
xxxxxxxx...xxxxxxxxxxxxx
xxxxxxxx...xxxxxxxxxxxxx
xxxxxxxx...xxxxxxxx.xxxx
......xxxxxxxxxxxxxxxxxx
3 8
""")) - 0.958333333333333) < 1e-6

# custom cases
assert abs(float(run("""\
........................

........................

........................

........................

........................

........................

........................

1 1
""")) - 1.0) < 1e-6

assert abs(float(run("""\
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxx
7 24
""")) - 0.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all dots, minimal choice | 1.0 | fully free grid edge case |
| all blocked, full selection | 0.0 | zero probability stability |

## Edge Cases

When the grid contains no free cells, every row subset produces zero column scores, so every candidate ratio evaluates to zero. The algorithm still behaves correctly because all prefixes remain zero and the maximum stays at zero.

When all cells are free, every column score equals the number of selected rows, so sorting does not change values. Any choice yields probability 1, and the algorithm naturally returns 1 because every ratio becomes $r / (k \cdot r) = 1/k$ times $k$, simplifying to 1.

When $d = 7$, only the full row mask is considered. The algorithm reduces to column optimization over the entire grid, which matches the direct interpretation of the problem.

When $h = 24$, only the full set of columns is considered. The solution degenerates into selecting the best row subset by average density, which is still correctly handled because the column loop only evaluates $k = 24$.
