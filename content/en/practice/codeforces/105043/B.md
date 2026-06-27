---
title: "CF 105043B - \u0414\u0432\u043e\u0438\u0447\u043d\u044b\u0439 \u043f\u0430\u0443\u043a \u043f\u043b\u0435\u0442\u0451\u0442 \u043f\u0430\u0443\u0442\u0438\u043d\u0443"
description: "We are given a sequence of pillar heights laid out in a straight line. Each position has a height, and we also have a threshold value x. The task is to find a contiguous segment of these pillars such that every pillar inside the segment has height at most x."
date: "2026-06-28T01:31:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105043
codeforces_index: "B"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u041d\u0422\u041e: \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u043e\u043d\u043d\u0430\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u044c. \u0421\u0435\u043a\u0446\u0438\u044f - \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430"
rating: 0
weight: 105043
solve_time_s: 77
verified: false
draft: false
---

[CF 105043B - \u0414\u0432\u043e\u0438\u0447\u043d\u044b\u0439 \u043f\u0430\u0443\u043a \u043f\u043b\u0435\u0442\u0451\u0442 \u043f\u0430\u0443\u0442\u0438\u043d\u0443](https://codeforces.com/problemset/problem/105043/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of pillar heights laid out in a straight line. Each position has a height, and we also have a threshold value `x`. The task is to find a contiguous segment of these pillars such that every pillar inside the segment has height at most `x`. Among all such valid segments, we want the maximum possible length.

In simpler terms, imagine walking along the array and only being allowed to stay on positions where the height does not exceed `x`. Whenever you hit a pillar that is too tall, you must stop that segment and start a new one after it. The answer is the longest uninterrupted stretch of “allowed” positions.

The input size can be very large, up to 700,000 elements. That immediately rules out any solution that checks all subsegments explicitly. A quadratic approach would involve considering all start positions and expanding to the right, which in the worst case performs on the order of $n^2$ checks, far too slow for this constraint. The solution must therefore process the array in linear time.

A subtle edge case appears when all elements are greater than `x`. In that case, no valid segment exists, and the answer is zero. Another corner case is when all elements are valid, in which case the answer is simply `n`.

A naive mistake often comes from treating the problem as “count elements ≤ x” globally, instead of respecting contiguity. For example, if the array is `[1, 100, 2, 3]` with `x = 50`, the valid elements are 1, 2, 3, but they do not form one segment. The correct answer is 2, not 3.

## Approaches

The brute-force idea is straightforward: for every starting index, extend a window to the right while all elements remain ≤ x, and compute its length. This correctly finds all valid segments, but in the worst case where all elements are ≤ x, each starting index scans to the end, producing roughly $n + (n-1) + \dots + 1$ operations, which is quadratic.

The key observation is that validity depends only on whether each individual element is ≤ x, and the condition for a segment is purely local. We do not need to maintain complex structure or recompute anything across segments. Instead, the array splits naturally into maximal contiguous blocks of “good” values. Each time we encounter an element greater than `x`, it breaks the structure completely, resetting the current segment length to zero.

This reduces the problem to a single linear scan where we track the length of the current valid run and maintain the maximum over all runs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Single Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining two values: the length of the current valid segment and the best answer seen so far.

1. Initialize `cur = 0` and `best = 0`. The variable `cur` tracks the current streak of valid elements, while `best` stores the maximum streak found so far.
2. Iterate through each height in the array. For each element, check whether it is ≤ x. This determines whether it can extend the current valid segment.
3. If the element is ≤ x, increment `cur` by 1 because the valid segment continues without interruption. This reflects that the current position extends the current run.
4. If the element is greater than x, reset `cur` to 0. This is necessary because the validity condition requires all elements in the segment to satisfy the constraint, and this element breaks continuity completely.
5. After updating `cur`, update `best = max(best, cur)` to record the longest valid segment seen up to this point.
6. After processing the entire array, output `best`.

### Why it works

At any position, `cur` exactly represents the length of the current contiguous suffix ending at that position where all values are ≤ x. Every time we reset, we are cutting the array exactly at invalid elements, which are the only possible breakpoints for valid segments. Since every valid segment must lie entirely between two invalid elements (or boundaries), every candidate segment is fully captured as some value of `cur`, ensuring no valid segment is missed and no invalid segment is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    cur = 0
    best = 0

    for v in a:
        if v <= x:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation reads the input in one pass and maintains only constant extra state. The key detail is that the reset happens immediately when encountering a value greater than `x`, ensuring that no invalid element contaminates a segment. The maximum update is done after extending the current run, which ensures the final value of each run is captured correctly.

## Worked Examples

### Example 1

Input:

```
5 4
1 5 2 3 6
```

We track the scan step by step.

| i | value | ≤ x? | cur | best |
| --- | --- | --- | --- | --- |
| 1 | 1 | yes | 1 | 1 |
| 2 | 5 | no | 0 | 1 |
| 3 | 2 | yes | 1 | 1 |
| 4 | 3 | yes | 2 | 2 |
| 5 | 6 | no | 0 | 2 |

The longest valid contiguous segment appears between indices 3 and 4, giving length 2.

This confirms that resets correctly split the array into independent segments and that we never merge across invalid boundaries.

### Example 2

Input:

```
5 4
1 4 3 2 1
```

| i | value | ≤ x? | cur | best |
| --- | --- | --- | --- | --- |
| 1 | 1 | yes | 1 | 1 |
| 2 | 4 | yes | 2 | 2 |
| 3 | 3 | yes | 3 | 3 |
| 4 | 2 | yes | 4 | 4 |
| 5 | 1 | yes | 5 | 5 |

All elements satisfy the condition, so the entire array forms one valid segment.

This shows the algorithm naturally handles the “no breaks” case without any special logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant work |
| Space | O(1) | Only two integer variables are maintained |

The linear scan is necessary because of the large constraint on `n`, and it fits easily within typical time limits even for the maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case: mixed breaks
assert run("5 4\n1 5 2 3 6\n") == "2"

# all valid
assert run("5 4\n1 4 3 2 1\n") == "5"

# all invalid
assert run("4 10\n20 30 40 50\n") == "0"

# single element valid
assert run("1 5\n3\n") == "1"

# single element invalid
assert run("1 5\n10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed breaks | 2 | reset logic correctness |
| all valid | 5 | full-array streak |
| all invalid | 0 | empty valid segment |
| single valid | 1 | minimum positive case |
| single invalid | 0 | minimum zero case |

## Edge Cases

A fully invalid array such as `5 3 / 10 11 12 13 14` demonstrates the reset mechanism repeatedly triggering. The algorithm never increments `cur`, so it remains zero throughout, and `best` stays zero, correctly capturing that no valid segment exists.

A fully valid array such as `5 10 / 1 2 3 4 5` never triggers a reset. The variable `cur` accumulates to `n`, and `best` is updated at every step, ending at `5`. This shows that the algorithm does not require segment boundaries to be explicitly detected, since continuity is naturally handled by accumulation.

A mixed case like `6 4 / 1 2 10 3 4 5` shows a single break splitting the array into two candidate segments `[1,2]` and `[3,4,5]`. The algorithm correctly evaluates both via independent runs of `cur`, and `best` captures the maximum among them, which is `3`.
