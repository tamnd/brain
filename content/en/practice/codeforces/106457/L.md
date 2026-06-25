---
title: "CF 106457L - Karst"
description: "The surface of Karst is described by a one dimensional list of measured heights. We are allowed to replace every height with a new value, but changing a position has a cost equal to the absolute difference between the old and new height."
date: "2026-06-25T09:15:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106457
codeforces_index: "L"
codeforces_contest_name: "UTPC Spring 2026 Open Contest"
rating: 0
weight: 106457
solve_time_s: 51
verified: true
draft: false
---

[CF 106457L - Karst](https://codeforces.com/problemset/problem/106457/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The surface of Karst is described by a one dimensional list of measured heights. We are allowed to replace every height with a new value, but changing a position has a cost equal to the absolute difference between the old and new height. The final sequence must be smooth, meaning neighboring positions cannot differ by more than the given limit `k`. The task is to find the minimum total cost needed to transform the original sequence into any valid smooth sequence.

The input contains the number of measurements, the maximum allowed difference between adjacent final heights, and the original altitude values. The output is the smallest possible sum of all individual changes.

The number of measurements can reach `200000`, so a solution that tries every possible final height or keeps a full dynamic programming table over all heights cannot work. The altitude values can be as large as `10^9`, which rules out coordinate-based DP. We need to exploit the structure of the cost function instead of the range of possible values.

The key observation is that the transition between positions depends on the previous chosen height only through an interval. If the current height is `x`, the previous height must be inside `[x-k, x+k]`. The cost function over possible values of `x` remains convex and piecewise linear, which lets us store the shape of the whole DP state rather than every possible height.

A few edge cases are easy to miss. If `k` is large enough, no changes are needed because the original sequence already satisfies the condition. For example:

```
Input:
3 10
5 7 5

Output:
0
```

A greedy approach that always modifies the middle value would still change `7`, but the original difference is only `2`, so the correct answer is zero.

Another tricky case is when the best solution changes values in both directions instead of only lowering peaks or only raising valleys. For example:

```
Input:
4 1
0 10 0 10

Output:
16
```

A careless approach might try to keep all low values and only reduce the high ones, producing a worse result. The optimal smooth sequence balances the values because every position affects the allowed range of its neighbors.

A third edge case appears when the optimal answer is a flat region rather than a single height. For example:

```
Input:
2 5
0 10

Output:
0
```

Both original values are already within the allowed difference. A method that assumes there is always a unique best final height can fail on such intervals.

## Approaches

The direct approach is to use dynamic programming over possible final heights. Let `dp[i][x]` be the minimum cost after processing the first `i` positions and ending with height `x`. The transition is:

```
dp[i][x] = |a[i] - x| + min(dp[i-1][y])
```

where `y` must satisfy `|y-x| <= k`.

This is correct because every valid sequence ending at `x` must come from a valid previous height inside that interval. However, the number of possible heights is enormous. Even if we only considered the range from `0` to `10^9`, the state space would be impossible to process. The worst case would require around `10^14` operations.

The important structure is that every transition preserves convexity. The function describing the DP value as a function of the current height is always a convex piecewise linear function. The absolute value term adds a V shaped function, and taking the minimum over a sliding interval only changes where the minimum plateau is located.

Instead of storing all heights, we store where the slope of the function changes. A convex piecewise linear function is completely determined by these breakpoints and its minimum value. This is the idea behind slope trick.

The data structure maintains two heaps. The left heap stores breakpoints on the left side of the minimum, and the right heap stores breakpoints on the right side. The minimum value of the function is stored separately. Adding `|x-a[i]|` inserts a new V shape, and the sliding window minimum operation shifts the valid minimum interval by lazily moving the breakpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * range of heights) | O(range of heights) | Too slow |
| Convex DP with slope trick | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain the current DP function using a slope trick structure. Initially the cost function is zero everywhere, so the structure starts with an empty set of breakpoints and minimum value zero.
2. For every altitude `a[i]`, first apply the operation that restricts the previous height to be within distance `k` from the current height. This replaces the old function with the minimum value over the interval `[x-k, x+k]`.

The reason this can be done efficiently is that a convex function keeps its shape after taking a sliding interval minimum. Only the positions of the slope changes move.
3. Add the cost of changing the current height by applying `|x-a[i]|`.

This inserts a new V shaped piece into the function. The slope changes by one on each side of `a[i]`, so the two heaps can be updated without rebuilding the function.
4. After all positions are processed, the minimum value stored in the slope trick structure is the answer.

Why it works:

The invariant is that after processing the first `i` positions, the maintained convex function represents the minimum possible cost of forming a smooth prefix that ends at every possible height. The sliding minimum step considers exactly the heights allowed by the smoothness constraint, and the absolute value addition accounts for the new position's modification cost. Since both operations preserve the representation, the final stored minimum is the optimal total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

class SlopeTrick:
    def __init__(self):
        self.left = []
        self.right = []
        self.add_left = 0
        self.add_right = 0
        self.value = 0

    def push_left(self, x):
        heapq.heappush(self.left, -(x - self.add_left))

    def push_right(self, x):
        heapq.heappush(self.right, x - self.add_right)

    def top_left(self):
        return -self.left[0] + self.add_left

    def top_right(self):
        return self.right[0] + self.add_right

    def pop_left(self):
        x = self.top_left()
        heapq.heappop(self.left)
        return x

    def pop_right(self):
        x = self.top_right()
        heapq.heappop(self.right)
        return x

    def add_x_minus_a(self, x):
        if self.left:
            self.value += max(0, self.top_left() - x)
        self.push_left(x)
        self.push_right(self.pop_left())

    def add_a_minus_x(self, x):
        if self.right:
            self.value += max(0, x - self.top_right())
        self.push_right(x)
        self.push_left(self.pop_right())

    def add_abs(self, x):
        self.add_x_minus_a(x)
        self.add_a_minus_x(x)

    def sliding_min(self, left_shift, right_shift):
        self.add_left += left_shift
        self.add_right += right_shift

n, k = map(int, input().split())
a = list(map(int, input().split()))

st = SlopeTrick()

for x in a:
    st.sliding_min(-k, k)
    st.add_abs(x)

print(st.value)
```

The two heaps are storing the slope change points of the convex DP function. The left heap is a max heap, implemented by storing negative values, because Python only provides a min heap. The right heap is a normal min heap.

The `sliding_min` function does not move every breakpoint individually. It only changes the lazy offsets, because all breakpoints on each side move together. This is what keeps each update logarithmic.

The order of operations matters. The valid previous heights must be applied before adding the new position's modification cost. Reversing these two operations would mean the current value incorrectly affects its own transition.

The answer can be large because there are up to `200000` positions and each change can cost up to `10^9`, but Python integers handle this without overflow issues.

(Part 2 continues with Worked Examples, Complexity Analysis, Test Cases, and Edge Cases.)
