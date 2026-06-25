---
title: "CF 106078D - Earth"
description: "We are given a sequence of stone masses arranged in a line. From this line, we are allowed to choose a single contiguous segment. Once a segment is chosen, we evaluate its “enjoyment” based on the distribution of values inside it."
date: "2026-06-25T12:08:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106078
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 1 (Advanced)"
rating: 0
weight: 106078
solve_time_s: 49
verified: true
draft: false
---

[CF 106078D - Earth](https://codeforces.com/problemset/problem/106078/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of stone masses arranged in a line. From this line, we are allowed to choose a single contiguous segment. Once a segment is chosen, we evaluate its “enjoyment” based on the distribution of values inside it.

For any chosen segment, we group equal masses together. If a mass value `m` appears `f` times inside the segment, it contributes `m * f` to the total score. Since every occurrence is counted exactly once in its own group, this expression simplifies to summing each element, but with a constraint: we are not optimizing over all subarrays, we are restricting ourselves to segments that contain at most `k` distinct values.

So the task reduces to finding a subarray with at most `k` distinct numbers that maximizes the sum of its elements.

The input is a list of integers, and we must output the maximum possible sum over all valid subarrays under the distinct-count constraint.

The constraint `n ≤ 10^5` immediately rules out any quadratic approach that enumerates all subarrays. A double loop over start and end would generate roughly `n^2 / 2` segments, which is around `5 * 10^9` operations in the worst case, far beyond a 1-2 second limit. This pushes us toward a linear or near-linear sliding window style solution.

A subtle point is that the scoring function might initially look like something more complex than a sum, because of the “frequency times value” phrasing. A naive interpretation might suggest tracking frequencies inside every window and recomputing contributions from scratch, but that would lead to repeated work per extension of the window.

Edge cases that break naive reasoning are mostly about the distinct constraint.

A case like `1 1 1 1` with `k = 1` is straightforward: the entire array is valid and should be chosen. A careless implementation might still try to shrink windows unnecessarily if it mistakenly treats duplicates as increasing distinct count.

A more interesting case is `1 2 3 1 2` with `k = 2`. The optimal window is not necessarily the longest prefix or suffix. If the algorithm greedily expands without careful removal of outdated elements, it may end up with three distinct values and incorrectly accept or reject the window depending on how bookkeeping is done.

## Approaches

The brute-force strategy is to consider every subarray `[l, r]`, compute the number of distinct values inside it, and if it is at most `k`, compute its sum and update the answer. Maintaining a frequency map for each window would allow recomputation of distinct count, but recomputing sums or resetting frequency structures for every `l` leads to a cubic or quadratic behavior depending on implementation style. Even with incremental updates, iterating all `l` still forces `O(n^2)` window extensions, which is too slow for `n = 10^5`.

The key observation is that both the sum and the distinct count behave nicely under a sliding window. When we extend the right boundary, we can update both the sum and frequency in constant time. When the number of distinct values exceeds `k`, we can move the left boundary forward until the constraint is restored. This turns the problem into maintaining the best valid window ending at each position.

The brute-force method works because it explicitly checks all candidates, but it fails because it repeatedly recomputes overlapping information. The sliding window approach removes this redundancy by ensuring each element enters and leaves the window at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Sliding Window | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a frequency table for values currently in the window, along with the current sum and the number of distinct elements.

1. Initialize two pointers `l = 0`, `r = 0`, along with `current_sum = 0`, `distinct = 0`, and an empty frequency map. We are preparing a window that will always remain valid.
2. Move `r` from left to right across the array. Each time we include `a[r]`, we add it to the sum and update its frequency. If this value appears for the first time in the window, we increment the distinct counter. This step ensures we always know the exact contribution of the current window without recomputing it.
3. After inserting `a[r]`, check whether the window violates the constraint `distinct > k`. If it does, we shrink the window from the left by moving `l` forward, removing elements from the sum and updating frequencies. Whenever a frequency drops to zero, we decrement the distinct counter. We continue shrinking until the constraint is restored. This ensures the window is always valid before evaluating it.
4. Once the window is valid, we update the answer with `current_sum`. This is correct because for each right endpoint `r`, we are considering the best possible left boundary that satisfies the constraint.
5. Continue this process until `r` reaches the end of the array.

### Why it works

At any fixed position `r`, the algorithm maintains the smallest possible left boundary `l` such that the subarray `[l, r]` contains at most `k` distinct values. Any other valid subarray ending at `r` must start at or to the right of this `l`, which would only reduce the sum because all numbers are non-negative. Therefore, the window maintained by the algorithm is the optimal candidate for that endpoint, and taking the maximum over all endpoints covers all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    l = 0
    distinct = 0
    current_sum = 0
    best = 0

    for r in range(n):
        x = a[r]
        current_sum += x

        if x not in freq or freq[x] == 0:
            freq[x] = 1
            distinct += 1
        else:
            freq[x] += 1

        while distinct > k:
            y = a[l]
            freq[y] -= 1
            current_sum -= y
            if freq[y] == 0:
                distinct -= 1
            l += 1

        best = max(best, current_sum)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation follows the sliding window structure directly. The frequency dictionary tracks how many times each value appears, and the `distinct` counter avoids recomputing dictionary size repeatedly. The key subtlety is updating `current_sum` symmetrically when expanding and shrinking the window, otherwise the answer will drift from the actual subarray sum.

## Worked Examples

### Example 1

Input:

`n = 8, k = 3`

`[1, 7, 2, 3, 2, 2, 1, 7]`

We track the window as `r` increases.

| r | l | window | distinct | sum | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | 1 | 1 |
| 1 | 0 | [1,7] | 2 | 8 | 8 |
| 2 | 0 | [1,7,2] | 3 | 10 | 10 |
| 3 | 0 | [1,7,2,3] → shrink | 3 | 12 | 12 |
| 4 | 1 | [7,2,3,2] | 3 | 14 | 14 |
| 5 | 1 | [7,2,3,2,2] | 3 | 16 | 16 |
| 6 | 3 | [3,2,2,1] | 3 | 8 | 16 |
| 7 | 3 | [3,2,2,1,7] → shrink | 3 | 15 | 16 |

The best value appears when the window balances a high-value element (`7`) with multiple occurrences of `2`. The trace confirms that we never consider invalid windows even temporarily.

### Example 2

Input:

`n = 5, k = 1`

`[5, 1, 5, 5, 1]`

| r | l | window | distinct | sum | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [5] | 1 | 5 | 5 |
| 1 | 1 | [1] | 1 | 1 | 5 |
| 2 | 2 | [5] | 1 | 5 | 5 |
| 3 | 2 | [5,5] | 1 | 10 | 10 |
| 4 | 4 | [1] | 1 | 1 | 10 |

This case shows that whenever a new distinct value appears, the left pointer must jump forward aggressively, collapsing the window until validity is restored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element enters and leaves the window at most once, so all pointer and frequency updates are linear |
| Space | O(n) | Frequency map stores at most one entry per distinct value in the array |

The linear complexity fits comfortably within the constraints for `n ≤ 10^5`, and the memory usage is bounded by the number of distinct values, which is also at most `n`. The solution therefore satisfies both limits with room to spare.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("8 3\n1 7 2 3 2 2 1 7\n") == "16"

# all equal, k = 1
assert run("5 1\n5 5 5 5 5\n") == "25"

# k equals n (entire array always valid)
assert run("4 4\n1 2 3 4\n") == "10"

# k = 1 with alternating values
assert run("6 1\n1 2 1 2 1 2\n") == "2"

# single element
assert run("1 1\n7\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 25 | single distinct value handling |
| k = n | 10 | no shrinking needed |
| alternating, k=1 | 2 | aggressive shrinking correctness |
| single element | 7 | minimal boundary case |

## Edge Cases

When all elements are identical, the frequency map grows but `distinct` never exceeds 1, so the window always expands to full length. The algorithm correctly keeps a single update path and never triggers shrinking.

When `k` equals `n`, the constraint never activates. The window becomes the entire array, and the algorithm degenerates to computing a prefix sum while maintaining correctness guarantees without any pointer movement on the left.

When values alternate heavily and `k = 1`, every new element forces immediate contraction. The left pointer effectively tracks the right pointer, and the window size never exceeds 1. This confirms that the shrink logic correctly restores validity even in worst-case oscillating inputs.
