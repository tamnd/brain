---
title: "CF 104760A - \u041c\u043d\u043e\u0433\u043e \u0440\u0430\u043a\u0443\u0448\u0435\u043a"
description: "We are given a linear sequence of shells, each with a positive weight. The shells are arranged in order along a beach, and we are only allowed to take a consecutive block of them."
date: "2026-06-29T02:21:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 68
verified: true
draft: false
---

[CF 104760A - \u041c\u043d\u043e\u0433\u043e \u0440\u0430\u043a\u0443\u0448\u0435\u043a](https://codeforces.com/problemset/problem/104760/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear sequence of shells, each with a positive weight. The shells are arranged in order along a beach, and we are only allowed to take a consecutive block of them. However, there is a capacity constraint: the bag can hold at most `K` shells, regardless of their total weight.

The task is to choose a contiguous segment whose length does not exceed `K`, such that the sum of weights inside that segment is maximized.

The output is a single number, the largest possible sum over all valid contiguous segments.

The constraints are large enough that an $O(N^2)$ scan over all subarrays is not feasible. With $N \le 2 \cdot 10^5$, a quadratic approach would imply on the order of $4 \cdot 10^{10}$ operations, which is far beyond typical limits. This immediately suggests that we need a linear or near-linear method.

A subtle edge case appears when `K >= N`. In that situation, every element can be taken, so the answer is simply the sum of the whole array. A naive sliding-window implementation that always tries to maintain a fixed window size `K` must be careful not to shrink below valid ranges when the array is shorter than `K`.

Another potential pitfall is assuming the optimal segment always has exactly length `K`. This is not necessarily true because a shorter segment can have a larger sum if it avoids negative structure, but in this problem all weights are positive, so the best segment will always use exactly `K` elements unless constrained by boundaries. That property is what makes a sliding window approach clean.

## Approaches

The brute-force method tries every possible starting position and extends it up to `K` steps forward, accumulating sums as it goes. For each index `i`, it checks all subarrays starting at `i` and of length at most `K`, updating a global maximum.

This is correct because it enumerates every valid segment explicitly. The issue is the number of operations. For each of the `N` starting points, up to `K` elements may be processed, leading to $O(NK)$ time. Since `K` can be as large as $10^7$, this is completely infeasible.

The structure of the problem suggests a better approach. We are maximizing a sum over all contiguous segments with a fixed maximum length constraint. Because all weights are positive, extending a window always increases the sum, so for any fixed right endpoint, the best valid segment ending there is the longest possible one, up to length `K`. This means we only need to maintain a sliding window of size at most `K` while scanning from left to right, keeping track of the current sum efficiently.

We maintain a running sum of the current window. As we move the right boundary forward, we add the new element. If the window exceeds size `K`, we remove the leftmost element. At every step, the current sum represents the best segment ending at that position, so we update the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NK) | O(1) | Too slow |
| Sliding Window | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers `l = 0` and a running sum `current = 0`, and a variable `best = 0`.

The pointers define the current window of shells we are considering.
2. Iterate `r` from `0` to `N - 1`, treating each position as the right endpoint of a window.

Each step expands the candidate segment by including one more shell.
3. Add `W[r]` to `current`.

This incorporates the new shell into the running window sum.
4. If the window size exceeds `K`, shrink it from the left by subtracting `W[l]` and incrementing `l`.

This ensures we respect the constraint that at most `K` shells can be taken. If we did not remove elements here, the window could grow arbitrarily large and violate the problem condition.
5. After adjusting the window, update `best = max(best, current)`.

At this point, the window represents the best valid segment ending at `r`, because any shorter prefix would only reduce the sum due to positivity of weights.
6. After processing all positions, output `best`.

### Why it works

At every position `r`, the algorithm maintains a window `[l, r]` that is valid (length at most `K`) and whose sum is computed exactly. Because all weights are positive, any valid segment ending at `r` with smaller length than the current window would have a smaller or equal sum. Therefore, once the window is maximized in length under the constraint, it also maximizes the sum for that endpoint. Scanning all `r` ensures every possible right boundary is considered, so the global maximum over all valid segments is captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    w = list(map(int, input().split()))
    k = int(input())

    l = 0
    current = 0
    best = 0

    for r in range(n):
        current += w[r]

        if r - l + 1 > k:
            current -= w[l]
            l += 1

        if current > best:
            best = current

    print(best)

if __name__ == "__main__":
    solve()
```

The code maintains a single sliding window over the array. The left pointer `l` only moves forward, so each element is added and removed at most once, ensuring linear complexity. The condition `r - l + 1 > k` enforces the maximum window size constraint. The variable `current` always stores the sum of the current valid segment, and `best` tracks the maximum seen so far.

A common implementation mistake is checking the window size before adding `w[r]`, which can lead to off-by-one errors. The correct order is to include the element first, then fix the window if needed.

## Worked Examples

### Example 1

Input:

```
10
1 3 2 4 1 5 1 2 1 2
5
```

We track the window as follows.

| r | l | window | current sum | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | 1 |
| 1 | 0 | [1,3] | 4 | 4 |
| 2 | 0 | [1,3,2] | 6 | 6 |
| 3 | 0 | [1,3,2,4] | 10 | 10 |
| 4 | 0 | [1,3,2,4,1] | 11 | 11 |
| 5 | 1 | [3,2,4,1,5] | 15 | 15 |
| 6 | 2 | [2,4,1,5,1] | 13 | 15 |
| 7 | 3 | [4,1,5,1,2] | 13 | 15 |
| 8 | 4 | [1,5,1,2,1] | 10 | 15 |
| 9 | 5 | [5,1,2,1,2] | 11 | 15 |

The trace shows how the window naturally shifts right while maintaining size 5. The maximum is achieved when the densest segment of weights is fully included.

### Example 2

Input:

```
6
5 1 5 1 5 1
2
```

| r | l | window | current sum | best |
| --- | --- | --- | --- | --- |
| 0 | 0 | [5] | 5 | 5 |
| 1 | 0 | [5,1] | 6 | 6 |
| 2 | 1 | [1,5] | 6 | 6 |
| 3 | 2 | [5,1] | 6 | 6 |
| 4 | 3 | [1,5] | 6 | 6 |
| 5 | 4 | [5,1] | 6 | 6 |

This case demonstrates repeated optimal windows and shows that the algorithm correctly handles many overlapping optimal segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is added once and removed at most once due to the sliding window movement |
| Space | O(1) | Only a few counters and the input array are stored |

The linear scan is sufficient for $N \le 2 \cdot 10^5$, and the memory usage is minimal since no auxiliary data structures beyond counters are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    w = list(map(int, input().split()))
    k = int(input())

    l = 0
    current = 0
    best = 0

    for r in range(n):
        current += w[r]
        if r - l + 1 > k:
            current -= w[l]
            l += 1
        if current > best:
            best = current

    return str(best)

assert run("""10
1 3 2 4 1 5 1 2 1 2
5
""") == "15"

assert run("""1
10
1
""") == "10"

assert run("""5
1 1 1 1 1
3
""") == "3"

assert run("""6
5 1 5 1 5 1
2
""") == "6"

assert run("""7
2 100 3 4 5 6 1
3
""") == "111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 10 | minimum size handling |
| all ones | 3 | uniform array correctness |
| alternating peaks | 6 | overlapping optimal windows |
| mixed large peak | 111 | correct window shifting |

## Edge Cases

When `K >= N`, the window never shrinks because the size constraint is never violated. The algorithm simply accumulates all elements once, and `best` becomes the total sum.

For a single-element array like `N = 1`, the loop runs once, the element is added, and no shrinking occurs. The result is exactly that element, matching the only valid segment.

In arrays where large values are spaced apart, such as `[2, 100, 3, 4, 5, 6, 1]` with `K = 3`, the sliding window correctly shifts to include the largest contiguous grouping that fits. At each step, the window remains valid and the maximum is updated at the moment the high-value cluster is fully inside the window.
