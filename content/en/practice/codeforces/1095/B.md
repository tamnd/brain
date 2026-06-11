---
title: "CF 1095B - Array Stabilization"
description: "We are given a list of numbers representing an array, and we are allowed to remove exactly one element. After removing it, we look at how “spread out” the remaining numbers are, defined as the difference between the largest and smallest remaining value."
date: "2026-06-12T05:51:22+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1095
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 529 (Div. 3)"
rating: 900
weight: 1095
solve_time_s: 84
verified: true
draft: false
---

[CF 1095B - Array Stabilization](https://codeforces.com/problemset/problem/1095/B)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numbers representing an array, and we are allowed to remove exactly one element. After removing it, we look at how “spread out” the remaining numbers are, defined as the difference between the largest and smallest remaining value.

The task is to choose which single element to remove so that this spread becomes as small as possible, and then output that minimum achievable spread.

The key constraint is that the array can be large, up to 100,000 elements. That immediately rules out any approach that tries removing each element and recomputing the minimum and maximum from scratch in linear time per removal, since that would lead to roughly $O(n^2)$ work in the worst case. Instead, we need to compute something about global structure once and reuse it.

A subtle edge case appears when extreme values occur multiple times. For example, if the minimum value appears more than once, removing just one occurrence does not change the minimum. The same applies to the maximum. This matters because the optimal removal often targets one of the extremes, but not always.

Consider the array `[1, 100, 100, 100]`. Removing `1` gives spread `100 - 100 = 0`. Removing `100` gives spread `100 - 1 = 99`. A naive approach that only considers removing the first or last element in sorted order would fail if it does not account for duplicates of extrema correctly.

Another edge case arises when all values are equal. Then any removal still leaves all equal values, and the answer is zero.

## Approaches

The brute-force idea is straightforward: for every index, simulate removing that element, compute the minimum and maximum of the remaining array, and track the smallest resulting difference. Computing min and max after each removal costs $O(n)$, and doing it for all $n$ positions yields $O(n^2)$. With $n = 10^5$, this is far beyond feasible limits.

The structure of the problem makes a more efficient strategy possible. The instability depends only on the minimum and maximum of the remaining elements. When we remove one element, only two things can change the answer: either we remove something that is not an extreme and the min/max stay the same, or we remove one of the extreme values and potentially shift the min or max to the second smallest or second largest element.

This suggests that we only need to know the smallest and second smallest values, and the largest and second largest values. If we remove a middle element, the min and max remain unchanged, so the result is unchanged. If we remove the current minimum, the new minimum becomes the second minimum. If we remove the current maximum, the new maximum becomes the second maximum.

Thus, the optimal answer must come from only two candidates: removing the minimum or removing the maximum. Any other removal cannot improve the range, since it leaves both extrema intact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array once to determine the smallest value, the second smallest value, the largest value, and the second largest value. These four numbers fully describe how the range can change after removing an extreme element.
2. Compute the original range as `max_value - min_value`. This represents the case where we remove a non-extreme element or effectively do not improve anything.
3. Consider removing the minimum element. After removal, the smallest remaining value becomes the second smallest, so the resulting range becomes `max_value - second_min`.
4. Consider removing the maximum element. After removal, the largest remaining value becomes the second largest, so the resulting range becomes `second_max - min_value`.
5. Take the minimum among these three values: original range, removing minimum, and removing maximum. This is the best achievable instability after removing exactly one element.

### Why it works

The array’s instability depends only on its extreme values. Removing a non-extreme element cannot change either endpoint of the range, so it cannot improve the result. Removing an extreme changes only one side of the range, and the next candidate value on that side is uniquely determined by the second smallest or second largest element. Since every valid removal falls into one of these categories, checking these cases exhaustively covers all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

INF = 10**18

min1 = min2 = INF
max1 = max2 = -INF

for x in a:
    # update smallest and second smallest
    if x < min1:
        min2 = min1
        min1 = x
    elif x < min2:
        min2 = x

    # update largest and second largest
    if x > max1:
        max2 = max1
        max1 = x
    elif x > max2:
        max2 = x

original = max1 - min1
remove_min = max1 - min2
remove_max = max2 - min1

print(min(original, remove_min, remove_max))
```

The implementation performs a single pass over the array, maintaining four running values. The update logic carefully preserves both the best and second-best candidates for each extreme, ensuring that when an extreme is hypothetically removed, the correct replacement value is already known.

The final step evaluates the three meaningful configurations. No other removals are explicitly considered because they cannot alter either boundary of the range.

## Worked Examples

### Example 1

Input:

```
4
1 3 3 7
```

We track minima and maxima:

| Step | Value | min1 | min2 | max1 | max2 |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | inf | - | - |
| 2 | 3 | 1 | 3 | 3 | inf |
| 3 | 3 | 1 | 3 | 3 | inf |
| 4 | 7 | 1 | 3 | 7 | 3 |

Now compute:

- original = 7 - 1 = 6
- remove min = 7 - 3 = 4
- remove max = 3 - 1 = 2

Answer is 2.

This trace shows that removing a middle element (3) is irrelevant, while removing the maximum produces the best improvement.

### Example 2

Input:

```
5
5 5 5 5 5
```

| Step | Value | min1 | min2 | max1 | max2 |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | inf | 5 | -inf |
| 2 | 5 | 5 | 5 | 5 | 5 |
| 3 | 5 | 5 | 5 | 5 | 5 |
| 4 | 5 | 5 | 5 | 5 | 5 |
| 5 | 5 | 5 | 5 | 5 | 5 |

Compute:

- original = 0
- remove min = 5 - 5 = 0
- remove max = 5 - 5 = 0

Answer is 0.

This confirms that duplicates of extreme values are handled correctly: removing one occurrence does not change the effective min or max.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute extreme and second extreme values |
| Space | O(1) | Only four auxiliary variables are used |

The linear scan fits comfortably within the 100,000 element limit, and constant memory ensures no overhead beyond input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    INF = 10**18

    min1 = min2 = INF
    max1 = max2 = -INF

    for x in a:
        if x < min1:
            min2 = min1
            min1 = x
        elif x < min2:
            min2 = x

        if x > max1:
            max2 = max1
            max1 = x
        elif x > max2:
            max2 = x

    return str(min(max1 - min1, max1 - min2, max2 - min1))

# provided sample
assert run("4\n1 3 3 7\n") == "2"

# all equal
assert run("5\n5 5 5 5 5\n") == "0"

# remove min best case
assert run("4\n1 100 100 100\n") == "0"

# remove max best case
assert run("4\n1 2 3 4\n") == "2"

# minimal size
assert run("2\n1 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | stability under duplicate extrema |
| skewed with single min | 0 | removing min improves range |
| increasing sequence | 2 | removing max case correctness |
| size 2 | 0 | minimal boundary behavior |

## Edge Cases

One important case is when the minimum or maximum appears multiple times. For input `[1, 1, 5, 10]`, removing one `1` does not change the minimum, so the second minimum is still `1`. The algorithm handles this because `min2` will also be `1`, so `max - min2` correctly reflects no change in range.

Another case is when the best move is not obvious from position but from value repetition. In `[1, 2, 3, 4]`, removing `2` or `3` does nothing to improve the range, while removing `1` or `4` gives a smaller range. The algorithm captures this by only evaluating extreme removals, ensuring that non-extreme removals never need to be explicitly tested.

Finally, for arrays of size two, removing one element leaves a single value, making the instability zero. The formula reduces correctly because either extreme removal leads to comparing identical remaining endpoints.
