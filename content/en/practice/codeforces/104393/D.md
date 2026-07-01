---
title: "CF 104393D - Destroying Asteriods"
description: "We are given a vertical grid with many rows and columns, but almost all cells are empty except for one asteroid in each column. Column $i$ contains exactly one asteroid placed at row $ci$."
date: "2026-07-01T01:21:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104393
codeforces_index: "D"
codeforces_contest_name: "ICPC Masters Mexico LATAM 2023"
rating: 0
weight: 104393
solve_time_s: 77
verified: true
draft: false
---

[CF 104393D - Destroying Asteriods](https://codeforces.com/problemset/problem/104393/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a vertical grid with many rows and columns, but almost all cells are empty except for one asteroid in each column. Column $i$ contains exactly one asteroid placed at row $c_i$. The spaceship starts at position $(0, 0)$, and it can move up and down within its current column. The key action is that at any moment it can fire a beam, and that beam destroys every asteroid that lies on the same row as the spaceship’s current position.

The movement between columns is implicit in the statement: since asteroids are spread across columns but shooting affects an entire row, the actual structure is that each asteroid corresponds to a target point $(i, c_i)$. The ship can reposition vertically to any row costlessly in terms of constraints, but the number of shots is limited to $K$, and each shot is only useful if it is fired on a row containing at least one asteroid that has not already been destroyed.

So the task reduces to choosing at most $K$ row indices such that the total number of columns whose asteroid lies on those rows is maximized.

Each chosen row “covers” all columns whose asteroid height equals that row value, and each column contributes at most once because there is only one asteroid per column.

The constraints are large: $C$ can go up to $10^5$. Any solution that tries all subsets of rows or even all combinations of shooting sequences is infeasible. Even $O(C \log C)$ or $O(C)$ per query is acceptable, but anything quadratic over rows or columns would be too slow.

A subtle edge case comes from repeated heights. If multiple columns share the same $c_i$, one shot on that row clears all of them. A naive approach that treats columns independently instead of aggregating by row would overcount actions and underestimate efficiency.

Another edge case is when $K$ exceeds the number of distinct heights. In that case, every distinct row with at least one asteroid should be chosen, but a naive greedy-by-column approach might still waste shots.

For example, consider:

```
C = 5, K = 5
c = [1, 1, 2, 2, 3]
```

Correct answer is 5, since all asteroids are cleared using 3 shots. A naive approach that fires per column could incorrectly assume more shots are needed or mis-handle duplicates.

## Approaches

A brute-force interpretation would be to think in terms of sequences of shots. Since the spaceship can freely move vertically, each shot is effectively choosing a row, and all asteroids on that row are removed. A naive solution would try all subsets of rows of size at most $K$, compute how many columns are covered, and take the best. This is correct, because order does not matter, only which rows are chosen.

However, the number of possible subsets of rows is exponential in the number of distinct heights. In the worst case, all $c_i$ are distinct, so there are $C$ candidate rows. Trying all $K$-combinations leads to $\binom{C}{K}$, which is infeasible even for small $K$. Even a backtracking solution would explode combinatorially.

The key observation is that rows are independent: choosing a row contributes exactly the number of columns whose asteroid lies there, and there is no interaction between rows except the budget $K$. So the problem becomes: we have a multiset of weights (frequencies of each row height), and we want to pick at most $K$ elements with maximum total sum, where picking a row yields its frequency.

This immediately reduces to sorting frequencies in descending order and taking the top $K$. Each shot should be used on a row that gives the maximum marginal gain, and since gains are fixed and independent, greedy selection is optimal.

We compute a frequency map of all $c_i$, sort the frequencies, and sum the largest $K$ values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over row subsets | $O(2^C)$ | $O(C)$ | Too slow |
| Frequency counting + sorting | $O(C \log C)$ | $O(C)$ | Accepted |

## Algorithm Walkthrough

1. Read the list of asteroid heights and count how many times each height appears.

This step groups all columns that can be destroyed with a single shot, since firing on a row removes all asteroids on that row.
2. Extract all frequencies into an array.

Each frequency represents the benefit of choosing that row once.
3. Sort the frequencies in descending order.

We want to prioritize rows that give the most asteroid removals per shot.
4. Take the first $K$ values from the sorted list and sum them.

If there are fewer than $K$ distinct rows, we take all of them since extra shots cannot improve the result.
5. Output the computed sum.

### Why it works

Each row contributes a fixed value independent of other rows, because each asteroid belongs to exactly one row and is removed the first time that row is chosen. This creates a set of independent rewards, and each shot can select exactly one reward. Since there is no overlap between rewards of different rows, maximizing total destruction reduces to selecting the largest available rewards up to $K$. Any deviation from taking the largest available remaining reward can only replace a larger contribution with a smaller one, which cannot improve the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, C, K = map(int, input().split())
    c = list(map(int, input().split()))

    freq = {}
    for x in c:
        freq[x] = freq.get(x, 0) + 1

    vals = sorted(freq.values(), reverse=True)

    ans = 0
    for i in range(min(K, len(vals))):
        ans += vals[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first compresses the grid structure into a frequency map over rows. This is the crucial simplification that removes any dependency on movement or geometry. The sorting step ensures we always consider the most profitable rows first.

The loop is carefully bounded by both $K$ and the number of distinct rows, which avoids indexing errors when $K$ is large.

## Worked Examples

### Sample 1

Input:

```
3 3 1
2 2 1
```

Frequencies are:

- row 2 → 2 asteroids
- row 1 → 1 asteroid

| Step | Available rows (freq) | Chosen | Remaining K | Total |
| --- | --- | --- | --- | --- |
| start | [2, 1] | - | 1 | 0 |
| 1 | [2, 1] | 2 | 0 | 2 |

Output is 2.

This shows that even though there are multiple columns, a single optimal row choice maximizes coverage.

### Sample 2

Input:

```
2 3 3
2 2 1
```

Frequencies:

- row 2 → 2
- row 1 → 1

| Step | Available rows (freq) | Chosen | Remaining K | Total |
| --- | --- | --- | --- | --- |
| start | [2, 1] | - | 3 | 0 |
| 1 | [2, 1] | 2 | 2 | 2 |
| 2 | [1] | 1 | 1 | 3 |

Output is 3.

This confirms that extra shots beyond the number of useful rows do not change the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(C \log C)$ | Counting frequencies is linear, sorting distinct heights dominates |
| Space | $O(C)$ | Frequency map stores at most one entry per distinct height |

The constraints allow up to $10^5$ values, so a linearithmic solution is well within limits. The memory usage is also linear in the number of distinct asteroid heights, which fits comfortably within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter

    R, C, K = map(int, input().split())
    c = list(map(int, input().split()))

    freq = Counter(c)
    vals = sorted(freq.values(), reverse=True)

    ans = sum(vals[:K])
    return str(ans)

# provided samples
assert run("3 3 1\n2 2 1\n") == "2", "sample 1"
assert run("2 3 3\n2 2 1\n") == "3", "sample 2"
assert run("3 3 2\n1 2 3\n") == "2", "sample 3"

# custom cases
assert run("1 1 1\n1\n") == "1", "single asteroid"
assert run("5 5 10\n1 1 1 1 1\n") == "5", "all same row"
assert run("5 5 2\n1 2 3 4 5\n") == "2", "all distinct, limited shots"
assert run("5 6 3\n1 1 2 2 3 3\n") == "6", "balanced frequencies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single asteroid | 1 | minimal case correctness |
| all same row | 5 | many shots vs one row collapse |
| all distinct, limited shots | 2 | greedy selection over unique rows |
| balanced frequencies | 6 | optimal grouping of equal blocks |

## Edge Cases

A common edge case is when all asteroids lie on the same row. For example:

```
3 3 10
5 5 5
```

The frequency map contains only one entry, 3. The algorithm sorts [3] and takes min(K, 1), producing 3. Any reasoning that tries to “use multiple shots per column” would be incorrect because the model only allows one destruction per row per shot.

Another edge case is when $K = 0$. The frequency list may be non-empty, but the algorithm correctly returns 0 because it never selects any row when slicing by $K$. A naive loop over frequencies without guarding for zero shots could incorrectly accumulate values.

A final subtle case is large diversity:

```
C = 5, K = 2
c = [1, 2, 3, 4, 5]
```

The algorithm sorts all ones and picks two, producing 2. Any approach that attempts to “move the ship” between columns rather than treating rows as independent rewards might incorrectly overcomplicate movement, but movement cost is irrelevant to scoring, so only selection matters.
