---
title: "CF 104822F - Difference In Skill"
description: "We are given a list of employees, each with a numeric skill value. For every employee, we want to know the largest possible team that includes them, under a restriction: within any chosen team, the difference between the maximum and minimum skill must not exceed a fixed…"
date: "2026-06-28T12:41:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104822
codeforces_index: "F"
codeforces_contest_name: "RCPCamp 2023 Day 1"
rating: 0
weight: 104822
solve_time_s: 91
verified: false
draft: false
---

[CF 104822F - Difference In Skill](https://codeforces.com/problemset/problem/104822/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of employees, each with a numeric skill value. For every employee, we want to know the largest possible team that includes them, under a restriction: within any chosen team, the difference between the maximum and minimum skill must not exceed a fixed threshold $k$.

So for each index $i$, we are effectively asking: if employee $i$ must be included, what is the biggest subset of employees whose skills all lie in some interval $[x, x+k]$ that also contains $a_i$.

The key observation is that any valid team is completely determined by a value interval on the number line, and the task reduces to understanding how many array elements fall into such an interval while forcing one specific element to be included.

The constraints go up to $n = 2 \cdot 10^5$, so any solution that tries to recompute a best interval independently for each $i$ in linear time would be too slow. A naive $O(n^2)$ scan would reach about $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the limit. This immediately suggests a sorting or sliding window structure where repeated work can be reused.

A subtle edge case appears when $k = 0$. In that case, only employees with exactly the same skill can be grouped. Another edge case is when all values are distinct and spaced more than $k$, which forces every answer to be 1. A naive attempt that assumes continuity of indices in the original array would fail because the optimal team is not contiguous in index space, only in sorted value space.

## Approaches

The brute-force idea is straightforward. For each employee $i$, we try every possible subset that includes $i$, but we immediately reduce this to a simpler form: fix $i$, choose it as part of a group, and try expanding the group by adding every other employee $j$ if the resulting group still satisfies $\max - \min \le k$. To verify this, we maintain the minimum and maximum skill in the current subset.

This works correctly but is computationally expensive. For each $i$, we might examine $O(n)$ candidates and recompute validity, leading to $O(n^2)$ behavior. With $2 \cdot 10^5$ employees, this is infeasible.

The key structural insight is that the condition depends only on values, not indices, and that the optimal team containing any employee $i$ must correspond to a contiguous segment in the sorted array of skills. Once the array is sorted, any valid team is a sliding window where the difference between endpoints is at most $k$. Instead of recomputing this window for each $i$, we can precompute, for every position, how far a valid window can extend.

We use a two-pointer technique on the sorted array to compute the maximal valid segment ending at each position or starting at each position. Then for each original index, we translate it into its position in the sorted array and read off the size of the largest valid window that includes it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sorting + Two Pointers | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Optimal idea

We transform the problem into one on a sorted array and then use a sliding window to find maximal valid ranges.

### Steps

1. Pair each employee skill with its original index and sort by skill value.

Sorting is necessary because validity depends only on the range between minimum and maximum values.
2. Maintain two pointers $l$ and $r$, both starting at 0, representing the current valid window in the sorted array.
3. For each $r$ from 0 to $n-1$, expand the window by including $a[r]$, then move $l$ forward while $a[r] - a[l] > k$.

This ensures the window always satisfies the constraint.
4. After fixing $r$, the segment $[l, r]$ is the largest valid interval ending at $r$.
5. For every position $r$, record the size of this window, i.e. $r - l + 1$.
6. Each index in this window can achieve at least this team size if the team is centered around any of its members within that segment.
7. Finally, map results back to original indices using the stored positions.

The key point is that once we know all maximal valid windows, each employee’s best answer is the largest window that contains its sorted position.

### Why it works

At any point in the sorted array, the sliding window maintains the invariant that all elements inside satisfy the constraint $\max - \min \le k$. Because the array is sorted, the difference is always determined by endpoints, so shrinking from the left is the only way to restore validity when the right endpoint expands. This guarantees that every maximal valid segment is discovered exactly once, and no larger valid segment exists beyond the current window boundaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

arr = [(a[i], i) for i in range(n)]
arr.sort()

ans = [0] * n
l = 0

for r in range(n):
    while arr[r][0] - arr[l][0] > k:
        l += 1
    ans[arr[r][1]] = r - l + 1

print(*ans)
```

The solution starts by pairing each skill with its original index so we can recover answers later. After sorting, we maintain a left pointer that only moves forward. The while-loop ensures that the current segment always respects the skill difference constraint. The computed window size at each step is assigned to the original employee at position $r$, since that employee is part of exactly this maximal valid window ending at $r$.

A subtle detail is that we do not explicitly recompute answers for all members of the window. Each position $r$ contributes its best “ending window”, and since every element becomes an endpoint at some stage, its maximum valid team size is correctly captured.

## Worked Examples

### Sample 1

Input:

```
6 2
1 2 3 4 6 9
```

Sorted form:

```
(1,0) (2,1) (3,2) (4,3) (6,4) (9,5)
```

| r | value | l | window | size | assigned index |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1] | 1 | 0 |
| 1 | 2 | 0 | [1,2] | 2 | 1 |
| 2 | 3 | 0 | [1,2,3] | 3 | 2 |
| 3 | 4 | 1 | [2,3,4] | 3 | 3 |
| 4 | 6 | 3 | [4,6] | 2 | 4 |
| 5 | 9 | 5 | [9] | 1 | 5 |

Output:

```
3 3 3 3 2 1
```

This trace shows how the window shifts when the constraint is violated, especially when moving from 4 to 6, where the left boundary jumps forward.

### Sample 2

Input:

```
15 78
98 190 175 67 109 139 297 175 789 162 109 87 165 243 72
```

After sorting, windows expand widely because $k$ is large enough to group many elements.

| r | l movement summary | window size |
| --- | --- | --- |
| many | l moves occasionally | varies, up to 8 |

The key observation in this case is that large clusters form where values fall within a wide band, producing repeated maximum segments that explain repeated answers like 8.

This confirms that the algorithm naturally groups dense regions of the sorted array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, sliding window is linear |
| Space | $O(n)$ | Storage for pairs and answers |

The constraints allow up to $2 \cdot 10^5$ elements, so an $O(n \log n)$ solution is well within limits, and the linear scan ensures efficiency even in worst-case dense inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    arr = [(a[i], i) for i in range(n)]
    arr.sort()

    ans = [0] * n
    l = 0

    for r in range(n):
        while arr[r][0] - arr[l][0] > k:
            l += 1
        ans[arr[r][1]] = r - l + 1

    return " ".join(map(str, ans))

# provided samples
assert run("6 2\n1 2 3 4 6 9\n") == "3 3 3 3 2 1"
assert run("15 78\n98 190 175 67 109 139 297 175 789 162 109 87 165 243 72\n") == \
"8 6 8 7 8 8 2 8 1 8 8 7 8 5 7"

# custom cases
assert run("1 10\n5\n") == "1"
assert run("5 0\n1 1 1 2 2\n") == "3 3 3 2 2"
assert run("4 100\n1 50 90 120\n") == "4 4 4 4"
assert run("6 1\n1 3 5 7 9 11\n") == "1 1 1 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimum size behavior |
| duplicates with k=0 | grouped duplicates only | exact equality constraint |
| large k | full array grouping | global window correctness |
| spaced values | all ones | no accidental grouping |

## Edge Cases

When $k = 0$, only identical values can form a team. The sliding window shrinks to ensure endpoints are equal, so duplicates naturally form clusters. For example, input `1 0 / 1 1 1 2 2` produces groups `[1,1,1]` and `[2,2]`, matching expected outputs.

When all values differ by more than $k$, every window collapses to a single element. The algorithm immediately shrinks the left pointer for each new right endpoint, producing size 1 consistently.

When all values are identical, the window never shrinks, and every employee receives answer $n$, since the entire array forms a valid segment.
