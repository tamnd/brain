---
title: "CF 104619L - Location, Location, Location"
description: "We are given a set of points on a 2D grid, each representing a location such as a house or apartment. We must choose a new point $(x, y)$ where a charging station will be built."
date: "2026-06-29T17:28:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104619
codeforces_index: "L"
codeforces_contest_name: "2023 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 104619
solve_time_s: 61
verified: true
draft: false
---

[CF 104619L - Location, Location, Location](https://codeforces.com/problemset/problem/104619/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on a 2D grid, each representing a location such as a house or apartment. We must choose a new point $(x, y)$ where a charging station will be built. The quality of a candidate location is measured by the sum of Manhattan distances from it to every given point. The Manhattan distance between two points is the horizontal distance plus the vertical distance.

The task is to find a location that minimizes this total distance. If multiple locations achieve the same minimum sum, we must pick the one with the smallest $x$. If there is still a tie, we pick the smallest $y$.

The input size goes up to $n = 100000$, and coordinates are bounded within $[-100000, 100000]$. This immediately rules out any approach that evaluates all candidate positions in the grid or computes distances from every possible point. A brute force over candidate locations would be far too large since even the coordinate range alone gives $200001^2$ possibilities, which is infeasible.

A second naive idea is to test all input points as potential facility locations. That reduces candidates to $n$, but each evaluation still costs $O(n)$, leading to $O(n^2)$ total work. With $n = 10^5$, this becomes $10^{10}$ distance computations, which is too slow.

A subtle edge case arises when multiple points share the same optimal median structure. For example, if all points lie on a vertical line $x = 0$, then any point with $x = 0$ and median $y$ values is optimal. A careless implementation that computes medians independently but does not enforce tie-breaking consistently may return different valid coordinates, but the problem requires deterministic selection.

## Approaches

The key observation is that Manhattan distance separates into independent contributions from $x$ and $y$:

$$|x - x_i| + |y - y_i| = |x - x_i| + |y - y_i|$$

So the total cost becomes:

$$\sum |x - x_i| + \sum |y - y_i|$$

This decomposition is crucial because it means we can optimize $x$ and $y$ independently.

We first consider the 1D version: choose a value $x$ minimizing $\sum |x - x_i|$. A well-known property of absolute deviation is that any median of the multiset minimizes this sum. Intuitively, moving the chosen point left or right increases distance to at least as many points as it decreases.

Thus, the optimal $x$ is the median of the $x_i$ values, and similarly the optimal $y$ is the median of the $y_i$ values.

The brute-force approach would evaluate every candidate $x$ and $y$, recomputing sums each time, costing $O(n)$ per evaluation. That leads to $O(n^2)$ complexity overall. The median insight collapses the entire search space to a single deterministic computation using sorting.

Tie-breaking requires care. When $n$ is even, there are multiple medians. The rule “minimize $x$, then minimize $y$” translates into choosing the lower median index (the left middle element in sorted order), because it produces the smallest valid coordinate among optimal solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal (median) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We treat $x$ and $y$ independently because the cost function splits cleanly.

1. Read all points and store their $x$ and $y$ coordinates separately. This separation is necessary because we will sort each dimension independently.
2. Sort the list of all $x$-coordinates. Sorting is required because the median is defined with respect to order statistics, not raw values.
3. Select the median $x$-coordinate. If $n$ is odd, this is the middle element. If $n$ is even, we choose the lower middle index to satisfy the requirement of minimizing $x$ among all optimal solutions.
4. Repeat the same process for the $y$-coordinates, extracting the median $y$.
5. Output $(x, y)$ as the final answer.

### Why it works

The correctness relies on the property that for any multiset of real numbers, the function $f(t) = \sum |t - a_i|$ is minimized at any median of the set. If we move $t$ to the left of the median, more points lie to the right than left, increasing total distance; if we move right, the opposite happens. Since the objective splits into independent sums over $x$ and $y$, choosing optimal medians for each coordinate simultaneously minimizes the full 2D Manhattan objective. The tie-breaking rule is satisfied by selecting the lower median index, ensuring lexicographically minimal coordinates among all optimal solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    xs = []
    ys = []
    
    for _ in range(n):
        x, y = map(int, input().split())
        xs.append(x)
        ys.append(y)
    
    xs.sort()
    ys.sort()
    
    # lower median for tie-breaking
    x_ans = xs[(n - 1) // 2]
    y_ans = ys[(n - 1) // 2]
    
    print(x_ans, y_ans)

if __name__ == "__main__":
    solve()
```

The solution splits input into two arrays so that sorting can be applied independently. Sorting each array ensures we can directly access the median in constant time after preprocessing. The index $(n - 1) // 2$ is chosen specifically to enforce the tie-breaking rule, ensuring that when multiple optimal medians exist, we select the smallest feasible coordinate.

A common implementation mistake is using `n // 2` blindly without considering even-sized cases and lexicographic constraints. Using `(n - 1) // 2` avoids that issue by always selecting the left median.

## Worked Examples

### Example 1

Input:

```
3
0 2
2 3
1 0
```

Sorted $x$: [0, 1, 2]

Sorted $y$: [0, 2, 3]

| Step | xs | ys | chosen x | chosen y |
| --- | --- | --- | --- | --- |
| sorted | [0,1,2] | [0,2,3] | - | - |
| median | - | - | 1 | 2 |

The median elements are $x = 1$, $y = 2$. This point minimizes total Manhattan distance.

This confirms the property that the middle element balances distances on both sides.

### Example 2

Input:

```
2
0 0
2 2
```

Sorted $x$: [0, 2]

Sorted $y$: [0, 2]

| Step | xs | ys | chosen x | chosen y |
| --- | --- | --- | --- | --- |
| sorted | [0,2] | [0,2] | - | - |
| median rule | - | - | 0 | 0 |

Here both medians are not unique. The rule selects the lower median, giving $(0, 0)$, which is optimal and satisfies tie-breaking.

This demonstrates how even-sized inputs require consistent median selection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting x and y arrays dominates |
| Space | $O(n)$ | storing coordinate arrays |

The constraints allow up to $10^5$ points, and sorting twice at this scale is well within limits. The algorithm uses linear extra memory, which is acceptable under the 2048 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import deque

    input = _sys.stdin.readline

    n = int(input())
    xs = []
    ys = []
    for _ in range(n):
        x, y = map(int, input().split())
        xs.append(x)
        ys.append(y)

    xs.sort()
    ys.sort()
    return f"{xs[(n-1)//2]} {ys[(n-1)//2]}"

# provided sample 1
assert run("""3
0 2
2 3
1 0
""") == "1 2"

# provided sample 2
assert run("""2
0 0
2 2
""") == "0 0"

# all same point
assert run("""3
5 5
5 5
5 5
""") == "5 5"

# vertical line
assert run("""4
0 1
0 2
0 3
0 4
""") == "0 2"

# horizontal line
assert run("""4
1 0
2 0
3 0
4 0
""") == "2 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal points | same point | stability and trivial median |
| vertical line | (0, median y) | independence of x and y |
| horizontal line | (median x, 0) | symmetric behavior |

## Edge Cases

A key edge case is even $n$, where multiple medians exist and tie-breaking matters.

Consider:

```
2
0 0
2 2
```

Sorted $x = [0, 2]$, sorted $y = [0, 2]$. The algorithm picks index $(2 - 1) // 2 = 0$, giving $x = 0$, $y = 0$. If we instead picked the upper median, we would get $(2, 2)$, which has the same total cost but violates the requirement to minimize $x$, then $y$. The lower median selection enforces the correct lexicographically smallest optimal point.

Another case is when all points are identical:

```
3
7 7
7 7
7 7
```

Both sorted arrays are constant, so any median index yields 7. The algorithm returns $(7, 7)$ consistently, matching the only feasible optimal solution.
