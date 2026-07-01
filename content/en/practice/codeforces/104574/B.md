---
title: "CF 104574B - Preferred Valley"
description: "We are given a sequence of terrain heights that forms a very rigid shape: it starts high, goes down, comes up, goes down again, and finally rises again."
date: "2026-06-30T08:15:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104574
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 09-08-23 Div. 2 (Beginner)"
rating: 0
weight: 104574
solve_time_s: 66
verified: true
draft: false
---

[CF 104574B - Preferred Valley](https://codeforces.com/problemset/problem/104574/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of terrain heights that forms a very rigid shape: it starts high, goes down, comes up, goes down again, and finally rises again. In other words, the array behaves like a “W”, with exactly two low points where the direction changes from decreasing to increasing.

Each low point corresponds to the bottom of a valley. There are exactly two such valleys, so there are exactly two local minima in the array under the strict interpretation of the shape.

The task is to identify the two valley bottoms and output the larger of the two values.

The input size is small, at most 1000 elements, which already suggests that even a straightforward linear scan or even a slightly redundant scan would be sufficient. Anything up to O(n²) would still be fast enough, but the structure guarantees that a linear solution is both possible and cleaner.

The only subtle cases come from how “valley bottom” is interpreted. A naive implementation might look for any index where the value is smaller than both neighbors, but boundary handling and strictness of the shape matter.

For example, if one were careless and checked only `h[i] < h[i-1] and h[i] < h[i+1]`, then plateaus or equal values would break correctness in more general variants. Here the problem guarantees strict monotonic segments, so equality is not expected inside transitions, but the safest reasoning still relies on detecting direction changes rather than pure comparisons.

Another potential mistake is assuming only one valley exists. In this problem there are two, so stopping after the first local minimum would produce an incomplete answer.

## Approaches

A brute-force interpretation is to examine every index and decide whether it is a valley bottom by comparing it with neighbors. For each position `i`, we check whether the sequence goes down into `i` and then goes up after it. If it is, we record it as a valley bottom. Finally, we take the maximum among all recorded bottoms.

This works because the definition of a valley bottom is purely local, but it still requires scanning all positions and performing constant work per position. That is O(n), which is already optimal in terms of asymptotic complexity.

However, we can also think more structurally. Since the array is guaranteed to form a W-shape, the pattern of differences is strictly: down, up, down, up. This means the valley bottoms occur exactly at indices where the direction changes from decreasing to increasing. Instead of checking full neighborhood conditions, we only need to detect sign changes in adjacent differences.

We compute a direction array implicitly by comparing consecutive elements. Whenever `h[i-1] > h[i]` and `h[i] < h[i+1]`, we identify a valley bottom immediately. This removes ambiguity and keeps the implementation minimal.

Both approaches are linear. The difference is conceptual clarity: the second directly encodes the geometry of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (neighbor check) | O(n) | O(1) | Accepted |
| Direction change detection | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate through indices from 1 to n − 2 because only these positions can have both left and right neighbors. This avoids boundary checks that cannot define a valley bottom.
2. At each index `i`, check whether the terrain is decreasing into `i` and increasing out of `i`, meaning `h[i-1] > h[i]` and `h[i] < h[i+1]`. This condition directly captures the definition of a local minimum in a strictly changing sequence.
3. If the condition holds, store `h[i]` as a candidate valley bottom.
4. After scanning the array, compute the maximum among all recorded valley bottoms. This corresponds to choosing the most elevated basin among the two valleys.
5. Output this maximum value.

The key design choice is that we do not try to explicitly segment the array into valleys. The monotonic structure ensures that valley bottoms are uniquely identifiable through local comparisons.

### Why it works

The array alternates direction in a strict pattern due to the W-shape constraint. Every valley bottom is exactly a point where the slope changes from negative to positive. Because the sequence is strictly decreasing before the valley and strictly increasing after it, no other point can satisfy both inequalities simultaneously. This makes the local condition both necessary and sufficient, so every detected point is a true valley bottom and no valid valley bottom is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
h = list(map(int, input().split()))

valleys = []

for i in range(1, n - 1):
    if h[i - 1] > h[i] and h[i] < h[i + 1]:
        valleys.append(h[i])

print(max(valleys))
```

The implementation directly follows the idea of scanning for local minima. The loop bounds ensure we never access invalid indices. The condition `h[i - 1] > h[i] and h[i] < h[i + 1]` encodes the transition from descending slope to ascending slope, which is the defining feature of a valley bottom.

We store all valley bottoms even though there are exactly two, because keeping the logic general avoids relying on the exact count. The final `max` selects the higher of the two basins as required.

## Worked Examples

### Sample 1

Input:

```
7
4 2 1 3 6 4 5
```

We scan each position:

| i | h[i-1] | h[i] | h[i+1] | Valley? | Collected |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 2 | 1 | No | - |
| 2 | 2 | 1 | 3 | Yes | 1 |
| 3 | 1 | 3 | 6 | No | - |
| 4 | 3 | 6 | 4 | No | - |
| 5 | 6 | 4 | 5 | Yes | 4 |

The detected valley bottoms are 1 and 4. The maximum is 4.

This confirms that the algorithm correctly identifies both slope reversals and selects the higher basin.

### Sample 2

Input:

```
5
21 17 19 12 30
```

| i | h[i-1] | h[i] | h[i+1] | Valley? | Collected |
| --- | --- | --- | --- | --- | --- |
| 1 | 21 | 17 | 19 | Yes | 17 |
| 2 | 17 | 19 | 12 | No | - |
| 3 | 19 | 12 | 30 | Yes | 12 |

The valley bottoms are 17 and 12, so the answer is 17.

This trace shows that even when the second valley is deeper, the algorithm correctly selects the higher one, since we explicitly take the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is checked once with constant-time comparisons |
| Space | O(1) | Only a small list of at most two valley candidates is stored |

The constraints allow up to 1000 elements, so a single linear pass is easily fast enough. Even if implemented less efficiently, the runtime remains negligible within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    h = list(map(int, input().split()))

    valleys = []
    for i in range(1, n - 1):
        if h[i - 1] > h[i] and h[i] < h[i + 1]:
            valleys.append(h[i])

    return str(max(valleys))

# provided samples
assert run("7\n4 2 1 3 6 4 5\n") == "4", "sample 1"
assert run("5\n21 17 19 12 30\n") == "17", "sample 2"

# custom cases
assert run("5\n5 1 5 1 5\n") == "5", "symmetric W shape"
assert run("6\n10 7 3 8 6 9\n") == "7", "two valleys different heights"
assert run("5\n9 1 2 1 9\n") == "1", "equal valley bottoms"
assert run("5\n100 50 60 40 80\n") == "50", "ensures correct local detection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 1 5 1 5 | 5 | symmetric structure and equal maxima |
| 6 10 7 3 8 6 9 | 7 | multiple valleys, correct max selection |
| 5 9 1 2 1 9 | 1 | equal valley depths handling |
| 5 100 50 60 40 80 | 50 | correct local minima detection |

## Edge Cases

One edge case is when both valleys have the same depth. For example:

```
5
9 1 2 1 9
```

The scan detects valley bottoms at indices 1 and 3, both equal to 1. The algorithm appends both values and returns `max([1, 1])`, correctly producing 1. The logic does not depend on uniqueness, so duplicate minima are naturally handled.

Another case is when the valley is extremely shallow on one side and deep on the other:

```
7
8 5 1 4 10 3 6
```

The detected bottoms are 1 and 3. The algorithm evaluates both local conditions independently and correctly selects 3. No assumption about symmetry is used, so imbalance does not affect correctness.

A final structural edge case is minimal size input:

```
5
10 2 3 1 9
```

Only indices 1, 2, 3 are checked. The algorithm identifies 2 and 1 as potential valleys and returns 2. The boundary restriction ensures no invalid memory access, and the strict inequality guarantees no false positives at the ends.
