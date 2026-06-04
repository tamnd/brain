---
title: "CF 234B - Reading"
description: "We are asked to help Vasya pick the best hours to read a textbook on a train ride. The train trip lasts for n hours, and each hour has a given light level between 0 and 100. Vasya wants to read for exactly k hours."
date: "2026-06-04T10:06:45+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 234
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 145 (Div. 2, ACM-ICPC Rules)"
rating: 1000
weight: 234
solve_time_s: 104
verified: true
draft: false
---

[CF 234B - Reading](https://codeforces.com/problemset/problem/234/B)

**Rating:** 1000  
**Tags:** sortings  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help Vasya pick the best hours to read a textbook on a train ride. The train trip lasts for _n_ hours, and each hour has a given light level between 0 and 100. Vasya wants to read for exactly _k_ hours. His goal is to choose _k_ hours such that the darkest of the selected hours is as bright as possible. In other words, if he reads during hours with light levels 20, 30, and 40, the minimum among these, 20, should be maximized across all possible sets of _k_ hours.

The input gives the number of hours _n_, the number of reading hours _k_, and the light levels for all hours. The output should first report the maximum achievable minimum light level, followed by the indices of the hours Vasya should pick. Multiple optimal solutions can exist.

The constraints are moderate: _n_ can be up to 1000. This means that an $O(n \log n)$ or $O(n^2)$ approach is feasible, but anything exponential like $O(n^k)$ would be too slow. Since light levels are between 0 and 100, we might exploit this small range, but a simpler approach is to focus on the hour selection rather than value frequencies.

Edge cases include when all hours have the same light, when the number of reading hours _k_ equals _n_, or when the maximum and minimum light values are equal. A careless approach might try to select consecutive hours or fail to handle the correct indexing, leading to wrong answers.

## Approaches

A naive approach would consider every combination of _k_ hours out of _n_, compute the minimum light for each combination, and choose the one with the highest minimum. This is correct but infeasible: the number of combinations is $\binom{n}{k}$, which grows extremely fast (for _n_ = 1000 and _k_ = 500 it is astronomically large).

The key insight is that we do not need to examine all combinations. Since we only care about maximizing the minimum light among chosen hours, the optimal set must include the _k_ brightest hours. By sorting the hours by their light level and picking the _k_ largest, we guarantee the largest possible minimum. The minimum light among these chosen hours is simply the smallest value in the selected subset, which will be the $k$-th largest in the full array. After selecting these hours, we output their original indices.

This approach reduces the problem to a sorting and selection task. Sorting takes $O(n \log n)$ time, and selecting the top _k_ and retrieving indices takes $O(n)$. This is efficient for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose k × k) | O(k) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values: _n_ and _k_, followed by the list of light levels.
2. Pair each light level with its original 1-based index. This preserves the hour positions after sorting.
3. Sort the list of pairs in descending order of light levels. This ensures that the first _k_ elements are the hours with the highest light levels.
4. Take the first _k_ pairs from the sorted list. These are the optimal hours for reading.
5. Extract the minimum light level among the chosen hours, which is the last element in the top _k_ subset because the list is sorted in descending order.
6. Collect the indices of the selected hours from the pairs and output them in any order.

Why it works: Sorting the hours by light guarantees that any set containing a smaller light level would not yield a better minimum. By taking the top _k_ values, we ensure that the smallest in this subset is as large as possible. Indices are preserved by storing them alongside the light levels.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
lights = list(map(int, input().split()))

# Pair light levels with their original indices
hours = [(lights[i], i+1) for i in range(n)]

# Sort descending by light level
hours.sort(reverse=True, key=lambda x: x[0])

# Take top k hours
selected = hours[:k]

# Minimum light among chosen hours
min_light = min(l[0] for l in selected)

# Extract indices
indices = [l[1] for l in selected]

print(min_light)
print(" ".join(map(str, indices)))
```

This solution reads the data, pairs light levels with hour indices to retain positions, sorts the pairs in descending order of light, and picks the top _k_. The minimum light is extracted using Python’s built-in `min`, though it could also be the last element of the sorted top _k_ list. Indices are printed in any order.

## Worked Examples

Sample 1:

Input: `5 3\n20 10 30 40 10`

| Step | hours (sorted) | selected | min_light | indices |
| --- | --- | --- | --- | --- |
| Initial | [(20,1),(10,2),(30,3),(40,4),(10,5)] | - | - | - |
| After sorting | [(40,4),(30,3),(20,1),(10,2),(10,5)] | [(40,4),(30,3),(20,1)] | 20 | [4,3,1] |

Output:

```
20
4 3 1
```

This confirms the selection of hours 4,3,1 with minimum light 20.

Custom case 2:

Input: `4 4\n50 50 50 50`

| Step | hours (sorted) | selected | min_light | indices |
| --- | --- | --- | --- | --- |
| Initial | [(50,1),(50,2),(50,3),(50,4)] | - | - | - |
| After sorting | [(50,1),(50,2),(50,3),(50,4)] | all | 50 | [1,2,3,4] |

Output:

```
50
1 2 3 4
```

All hours are equally bright, so any subset of size _k_ gives the same minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the list dominates the runtime |
| Space | O(n) | Storing pairs of light levels and indices |

Given n ≤ 1000, this fits well within the 1-second time limit and the memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    lights = list(map(int, input().split()))
    hours = [(lights[i], i+1) for i in range(n)]
    hours.sort(reverse=True, key=lambda x: x[0])
    selected = hours[:k]
    min_light = min(l[0] for l in selected)
    indices = [l[1] for l in selected]
    return f"{min_light}\n{' '.join(map(str, indices))}"

# Provided sample
assert run("5 3\n20 10 30 40 10\n") == "20\n4 3 1"

# Minimum-size input
assert run("1 1\n0\n") == "0\n1"

# Maximum-size input (all 100)
assert run("1000 1000\n" + " ".join(["100"]*1000) + "\n") == "100\n" + " ".join(str(i) for i in range(1,1001))

# All-equal values, k<n
assert run("5 2\n10 10 10 10 10\n") == "10\n1 2"

# Mixed values, k<n
assert run("6 3\n5 1 9 2 8 3\n") == "5\n3 5 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n0` | `0\n1` | Handles smallest input |
| `1000 1000\n100...` | `100\n1..1000` | Handles maximum-size input |
| `5 2\n10 10 10 10 10` | `10\n1 2` | All values equal, k<n |
| `6 3\n5 1 9 2 8 3` | `5\n3 5 1` | General mixed values, non-consecutive |

## Edge Cases

When _k_ equals _n_, the algorithm naturally selects all hours. For input `4 4\n50 50 50 50`, the algorithm sorts the hours but the top _k_ includes every hour. The minimum light is 50, and indices `[1,2,3,4]` are returned correctly. No off-by-one errors occur because indices are stored as 1-based from the beginning.

When all light levels are identical, any subset of size _k_ is valid. The algorithm still chooses the first _k_ hours after sorting, which is acceptable according to the problem statement. For input `5 3\n10 10 10 10 10`, the algorithm outputs `[1,2,
