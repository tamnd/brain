---
title: "CF 253B - Physics Practical"
description: "We are given a list of measurement results from a physics experiment. Vasya wants to keep as many measurements as possible, but the remaining set must satisfy one condition: the largest remaining value cannot be more than twice the smallest remaining value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 253
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 154 (Div. 2)"
rating: 1400
weight: 253
solve_time_s: 194
verified: true
draft: false
---

[CF 253B - Physics Practical](https://codeforces.com/problemset/problem/253/B)

**Rating:** 1400  
**Tags:** binary search, dp, sortings, two pointers  
**Solve time:** 3m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of measurement results from a physics experiment. Vasya wants to keep as many measurements as possible, but the remaining set must satisfy one condition: the largest remaining value cannot be more than twice the smallest remaining value.

The task is to remove the minimum number of measurements so that the remaining numbers satisfy:

$y \le 2x$

where `x` is the minimum remaining value and `y` is the maximum remaining value.

Another way to think about the problem is this: among all subsets whose maximum value is at most twice the minimum value, find the largest possible subset. Once we know the maximum number of measurements we can keep, the answer is simply:

`removed = n - kept`

The input size reaches `10^5`, which immediately rules out quadratic solutions. Any approach that checks every pair of boundaries independently and scans the whole array again would perform around `10^10` operations in the worst case, far beyond the time limit. We need something around `O(n log n)` or `O(n)` after sorting.

The values themselves are small, at most `5000`, but `n` is large enough that we should still focus on algorithms that scale well with the number of elements.

There are several easy-to-miss edge cases.

Consider an array where all values are already valid:

```
5
2 2 3 4 4
```

The correct answer is `0` because the largest value is `4` and the smallest is `2`, so `4 ≤ 2 * 2`.

A careless implementation might always try to shrink windows unnecessarily and remove elements even though no removals are needed.

Another tricky case is when duplicates appear around the boundary:

```
6
1 2 2 2 4 4
```

The whole array is invalid because `4 > 2 * 1`. But after removing only the `1`, the remaining array becomes valid. The correct answer is `1`.

An incorrect two-pointer implementation may move the left pointer too aggressively and miss the optimal window.

A third important case is the minimum size input:

```
2
1 5000
```

The only valid remaining subsets have size `1`, since `5000 > 2`. The answer is `1`.

This catches implementations that assume at least two elements must remain.

## Approaches

The brute-force idea is straightforward once the array is sorted. Suppose we fix the smallest remaining value at index `i`. Then we can try every possible ending index `j ≥ i` and check whether:

$a_j \le 2a_i$

If the condition holds, then the subarray from `i` to `j` is valid, because sorting guarantees every element between them also lies within the same range.

This works because any optimal solution can always be represented as a contiguous segment in sorted order. If we keep values `3` and `7`, we would never exclude a value `5` sitting between them after sorting.

The brute-force method checks all `O(n^2)` pairs `(i, j)`. With `n = 10^5`, this becomes roughly `10^10` checks, which is far too slow.

The key observation is that once the array is sorted, the valid range for a fixed left endpoint expands monotonically. If a window `[l, r]` is valid, then increasing `r` may eventually break the condition, but decreasing `r` will never hurt.

That monotonic structure is exactly what two pointers are designed for.

We maintain a sliding window `[l, r]` over the sorted array. For every `r`, we move `l` forward only while the condition is violated. At that point, the current window becomes the largest valid segment ending at `r`.

Since each pointer moves only forward, the total work after sorting is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input array and sort it.

Sorting transforms the problem into finding the longest contiguous segment where the largest value is at most twice the smallest.
2. Initialize two pointers.

Let `l = 0`. We will iterate `r` from left to right.
3. For each `r`, expand the right side of the window.

The current window is `[l, r]`.
4. While the window is invalid, move `l` forward.

The window is invalid when:

$a_r > 2a_l$

Since the array is sorted, increasing `l` increases the minimum value of the window, making the condition easier to satisfy.
5. After restoring validity, compute the window size.

The current valid segment length is:

```
r - l + 1
```

Keep track of the maximum valid length seen so far.
6. After processing all positions, print:

```
n - maximum_valid_length
```

This is the minimum number of deletions needed.

### Why it works

After sorting, every valid solution corresponds to a contiguous subarray. If two kept elements satisfy the condition, then every value between them also satisfies it automatically because sorted order preserves the range.

The sliding window maintains the invariant that the current segment `[l, r]` is always valid after the inner loop finishes. For each right endpoint `r`, the algorithm finds the smallest possible `l` that keeps the segment valid, which also gives the largest valid window ending at `r`.

Because every possible optimal segment appears as some window during the scan, the algorithm cannot miss the best answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    l = 0
    best = 0

    for r in range(n):
        while a[r] > 2 * a[l]:
            l += 1

        best = max(best, r - l + 1)

    print(n - best)

solve()
```

The first step sorts the measurements. Without sorting, there is no efficient way to maintain the minimum and maximum values of a candidate segment while preserving contiguity of chosen elements.

The left pointer `l` only moves forward. This matters for efficiency. If it could move backward, the complexity would no longer be linear after sorting.

The condition inside the `while` loop is strict:

```
a[r] > 2 * a[l]
```

Using `>=` here would be wrong because equality is allowed. For example, `[2, 4]` is valid.

The window size is computed as:

```
r - l + 1
```

This is a classic off-by-one detail. Both endpoints are included in the current segment.

The final answer subtracts the largest valid kept segment from the total number of measurements.

## Worked Examples

### Example 1

Input:

```
6
4 5 3 8 3 7
```

After sorting:

```
[3, 3, 4, 5, 7, 8]
```

| r | a[r] | l after adjustment | Window | Window Size | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | [3] | 1 | 1 |
| 1 | 3 | 0 | [3, 3] | 2 | 2 |
| 2 | 4 | 0 | [3, 3, 4] | 3 | 3 |
| 3 | 5 | 0 | [3, 3, 4, 5] | 4 | 4 |
| 4 | 7 | 4 | [7] | 1 | 4 |
| 5 | 8 | 4 | [7, 8] | 2 | 4 |

The largest valid segment has size `4`, so we remove `6 - 4 = 2` measurements.

This trace shows how the left pointer can jump several positions when the ratio condition becomes invalid.

### Example 2

Input:

```
6
1 2 2 2 4 4
```

Sorted array:

```
[1, 2, 2, 2, 4, 4]
```

| r | a[r] | l after adjustment | Window | Window Size | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1] | 1 | 1 |
| 1 | 2 | 0 | [1, 2] | 2 | 2 |
| 2 | 2 | 0 | [1, 2, 2] | 3 | 3 |
| 3 | 2 | 0 | [1, 2, 2, 2] | 4 | 4 |
| 4 | 4 | 1 | [2, 2, 2, 4] | 4 | 4 |
| 5 | 4 | 1 | [2, 2, 2, 4, 4] | 5 | 5 |

The optimal choice removes only the `1`.

This example demonstrates why we should not move the left pointer more than necessary. Once `l` becomes `1`, the window becomes valid again and keeps maximum size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, sliding window is linear |
| Space | O(1) | Only a few variables besides the input array |

The solution easily fits within the limits. Sorting `10^5` integers is fast in Python, and the two-pointer scan touches each element at most twice.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    a.sort()

    l = 0
    best = 0

    for r in range(n):
        while a[r] > 2 * a[l]:
            l += 1

        best = max(best, r - l + 1)

    print(n - best)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("6\n4 5 3 8 3 7\n") == "2\n", "sample 1"

# minimum size
assert run("2\n1 5000\n") == "1\n", "minimum size"

# already valid
assert run("5\n2 2 3 4 4\n") == "0\n", "already valid"

# all equal
assert run("6\n7 7 7 7 7 7\n") == "0\n", "all equal"

# off-by-one boundary
assert run("4\n2 4 4 4\n") == "0\n", "equality allowed"

# single bad small element
assert run("6\n1 2 2 2 4 4\n") == "1\n", "remove smallest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 5000` | `1` | Minimum-size behavior |
| `5 / 2 2 3 4 4` | `0` | Already valid array |
| `6 / 7 7 7 7 7 7` | `0` | Duplicate handling |
| `4 / 2 4 4 4` | `0` | Equality boundary `y = 2x` |
| `6 / 1 2 2 2 4 4` | `1` | Correct left pointer movement |

## Edge Cases

Consider the equality boundary case:

```
4
2 4 4 4
```

After sorting, the array remains the same. When `r` reaches the first `4`, the condition checked is:

```
4 > 2 * 2
```

which becomes:

```
4 > 4
```

This is false, so the window remains valid. The algorithm correctly keeps all elements and outputs `0`.

Now consider the extreme mismatch case:

```
2
1 5000
```

At `r = 1`, the condition becomes:

```
5000 > 2
```

which is true, so `l` advances to `1`. The valid window becomes `[5000]` with size `1`. The algorithm outputs `2 - 1 = 1`.

Finally, consider repeated elements near the boundary:

```
6
1 2 2 2 4 4
```

When `r` reaches the first `4`, the current minimum `1` no longer works because:

```
4 > 2
```

The algorithm advances `l` once, making the minimum value `2`. Now the condition becomes:

```
4 > 4
```

which is false, so the large valid window is preserved. This confirms that the sliding window shrinks only as much as necessary, which is essential for optimality.
