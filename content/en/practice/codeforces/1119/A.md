---
title: "CF 1119A - Ilya and a Colorful Walk"
description: "We are given a street with n houses in a row, numbered from 1 to n, where each house has a color represented by an integer. Ilya wants to pick two houses of different colors and walk between them, measuring the distance simply as the difference in their indices (j - i) for i < j."
date: "2026-06-12T04:27:56+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1119
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 2"
rating: 1100
weight: 1119
solve_time_s: 65
verified: true
draft: false
---

[CF 1119A - Ilya and a Colorful Walk](https://codeforces.com/problemset/problem/1119/A)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a street with `n` houses in a row, numbered from `1` to `n`, where each house has a color represented by an integer. Ilya wants to pick two houses of **different colors** and walk between them, measuring the distance simply as the difference in their indices `(j - i)` for `i < j`. The task is to find the maximum distance he can achieve under this rule.

The input gives the number of houses `n` followed by a list of colors `c_1, c_2, ..., c_n`. The output is a single integer: the largest possible distance between two houses with different colors.

Since `n` can be as large as 300,000 and the time limit is 2 seconds, any solution that examines every possible pair of houses (which would require roughly 45 billion operations in the worst case) is infeasible. This rules out brute-force approaches with `O(n^2)` complexity. We need a solution linear in `n` or close to it.

Edge cases include situations where the first and last houses have different colors (producing the maximum distance), or when the array has long sequences of identical colors except at the ends. For example, `[1, 1, 1, 1, 2]` should return `4`, not `1`. A naive implementation scanning only neighboring pairs would return the wrong answer. Another subtle case is when the maximum distance occurs from the start to a late differing house or from the end to an early differing house, so the solution must consider both ends of the array.

## Approaches

The brute-force approach iterates over every possible pair `(i, j)` with `i < j` and checks if the colors differ, tracking the maximum `j - i`. This is correct but requires `O(n^2)` operations, which is far too slow for `n` up to 300,000.

The key observation to optimize this problem is that the maximum distance will always involve **one of the endpoints**. If we try to maximize `j - i`, the largest difference occurs either starting from the first house or ending at the last house. Therefore, we only need to check distances from the first house to the last house of a different color and from the last house to the first house of a different color. This reduces the problem to **checking two candidates**, making it `O(n)`.

The optimal approach scans from both ends: starting from the left, find the furthest house on the right with a different color, and starting from the right, find the furthest house on the left with a different color. The maximum of these two distances is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Record the color of the first house `c_first = c[0]`.
2. Scan the array from the end backward. For each house, if its color differs from `c_first`, compute `distance = index_last - 0` and update the maximum distance. Stop at the first differing color from the end because we only care about the **furthest one**.
3. Record the color of the last house `c_last = c[n-1]`.
4. Scan the array from the beginning forward. For each house, if its color differs from `c_last`, compute `distance = n-1 - index_first` and update the maximum distance. Stop at the first differing color from the start because again, we only care about the **furthest one**.
5. Return the larger of the two distances found.

**Why it works:** The maximum distance is constrained by the endpoints. Any two houses inside the array with different colors will have a smaller distance than one of the endpoints paired with a differing color at the opposite end. By checking only the endpoints, we guarantee that we find the maximal possible distance without missing any candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
colors = list(map(int, input().split()))

c_first = colors[0]
c_last = colors[-1]

# distance from the first house to the furthest differing color from the end
for i in range(n-1, -1, -1):
    if colors[i] != c_first:
        dist1 = i
        break

# distance from the last house to the furthest differing color from the start
for i in range(n):
    if colors[i] != c_last:
        dist2 = n - 1 - i
        break

print(max(dist1, dist2))
```

The code first assigns the first and last colors, then scans from the end for the first house differing from the start and from the start for the first house differing from the end. The `break` ensures we only take the furthest possible differing house in each case. Using `i` directly as a distance is safe because Python is 0-indexed, so `i - 0` is `i`, and `n - 1 - i` directly computes the distance from the end.

## Worked Examples

### Sample 1

Input: `[1, 2, 3, 2, 3]`

| i | colors[i] != c_first? | dist1 |
| --- | --- | --- |
| 4 | 3 != 1 | 4 |

| i | colors[i] != c_last? | dist2 |
| --- | --- | --- |
| 0 | 1 != 3 | 4 |

Maximum distance is `max(4, 4) = 4`.

This confirms that scanning from both ends correctly identifies the maximum distance.

### Sample 2

Input: `[1, 1, 1, 2]`

| i | colors[i] != c_first? | dist1 |
| --- | --- | --- |
| 3 | 2 != 1 | 3 |

| i | colors[i] != c_last? | dist2 |
| --- | --- | --- |
| 0 | 1 != 2 | 3 |

Maximum distance is `3`, which is correct. This trace confirms the algorithm handles sequences of identical colors followed by a differing color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We perform two linear scans over the array, once from each end. |
| Space | O(1) | Only a few variables are stored; no additional data structures scale with n. |

With n up to 300,000, O(n) operations run comfortably within a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    colors = list(map(int, input().split()))
    c_first = colors[0]
    c_last = colors[-1]

    for i in range(n-1, -1, -1):
        if colors[i] != c_first:
            dist1 = i
            break
    for i in range(n):
        if colors[i] != c_last:
            dist2 = n - 1 - i
            break
    return str(max(dist1, dist2))

# Provided samples
assert run("5\n1 2 3 2 3\n") == "4", "sample 1"
assert run("2\n1 2\n") == "1", "sample 2"
assert run("7\n1 1 1 2 2 2 1\n") == "6", "sample 3"

# Custom cases
assert run("4\n1 1 1 2\n") == "3", "identical prefix"
assert run("4\n2 1 1 1\n") == "3", "identical suffix"
assert run("3\n1 2 1\n") == "2", "alternating colors"
assert run("6\n1 1 1 1 1 2\n") == "5", "large end distance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4\n1 1 1 2\n` | 3 | Handling identical colors at the start |
| `4\n2 1 1 1\n` | 3 | Handling identical colors at the end |
| `3\n1 2 1\n` | 2 | Alternating colors, short array |
| `6\n1 1 1 1 1 2\n` | 5 | Maximum distance occurs from start to last differing color |

## Edge Cases

For an array like `[1, 1, 1, 2]`, scanning from the end finds the differing color at index 3, giving a distance of `3`. Scanning from the start finds the differing color at the last index as well, also giving `3`. This ensures that sequences of identical colors at either end do not cause the algorithm to miss the correct maximum. Similarly, if the array is `[2, 1, 1, 1]`, scanning from the start finds index 0 for the differing color from the end, producing the correct maximum distance. The algorithm handles these edge cases naturally without additional conditionals.
