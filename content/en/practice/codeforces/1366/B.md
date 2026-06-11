---
title: "CF 1366B - Shuffle"
description: "We are given an array of size $n$ initialized with all zeros except for a single one at position $x$. The array is 1-indexed. We then have $m$ operations, each defined by a range $[li, ri]$. In each operation, we can swap any two elements within that range."
date: "2026-06-11T12:02:43+07:00"
tags: ["codeforces", "competitive-programming", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1366
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 89 (Rated for Div. 2)"
rating: 1300
weight: 1366
solve_time_s: 110
verified: true
draft: false
---

[CF 1366B - Shuffle](https://codeforces.com/problemset/problem/1366/B)

**Rating:** 1300  
**Tags:** math, two pointers  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of size $n$ initialized with all zeros except for a single one at position $x$. The array is 1-indexed. We then have $m$ operations, each defined by a range $[l_i, r_i]$. In each operation, we can swap any two elements within that range. The task is to determine, after applying these operations in any order we choose, how many positions in the array could possibly contain the 1.

Although the array size $n$ can be very large, up to $10^9$, the number of operations $m$ is small, at most 100. This suggests that we cannot represent the array explicitly. Instead, we must reason about ranges and the movement of the 1 through these ranges.

An important subtlety is that multiple swaps in overlapping ranges can effectively propagate the 1 to any position that is connected by the union of the ranges. For example, if the initial 1 is at position 4, and the first operation covers [1, 6], then the 1 can reach all positions from 1 to 6 immediately. If a later operation covers [2, 3], it does not extend the reach further, but if another operation covers [5, 7], then the reachable positions extend to [1, 7].

Non-obvious edge cases include: the 1 starting at the boundary (position 1 or $n$), operations that are singletons ([3,3]), and operations that do not overlap with any current reachable positions. A naive solution that attempts to simulate all possible swaps will fail because $n$ is too large. For instance, with $n = 10^9$, storing the array or iterating through it is infeasible.

## Approaches

A brute-force approach would simulate the swaps directly by maintaining the array. For each operation, we would attempt all pairs of swaps within the range, checking if the 1 moves. Even if we only track the position of the 1, trying every swap in every range quickly becomes intractable. For $m = 100$ operations with ranges up to size $n$, this approach is impossible because of the huge size of the array.

The key insight is to track the **contiguous range of positions where the 1 can appear** rather than the array itself. Initially, the range is just [x, x]. For each operation, if its range overlaps the current range of the 1, we can merge them: the 1 can now appear anywhere in the union of the current range and the operation's range. Otherwise, the operation does not affect the 1's possible positions. After processing all operations, the answer is simply the length of the final range.

This observation reduces the problem to simple interval union tracking, which is efficient because $m$ is small and $n$ does not need to be represented explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n) | O(n) | Too slow |
| Optimal (interval tracking) | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `left` and `right` to `x`. These variables represent the current inclusive range where the 1 can appear.
2. Iterate over each operation defined by `[l_i, r_i]`.
3. If the operation's range `[l_i, r_i]` overlaps the current range `[left, right]` (i.e., `l_i <= right` and `r_i >= left`), update the range to include the operation: `left = min(left, l_i)` and `right = max(right, r_i)`.
4. After processing all operations, the number of indices where the 1 can end up is `right - left + 1`.
5. Repeat for all test cases.

Why it works: The invariant is that `left` and `right` always encompass all positions reachable by the 1 through the operations considered so far. Whenever an operation overlaps this range, the reachable range expands to include it. No operation outside the current range can affect the 1, so ignoring non-overlapping operations is correct. The final range length is exactly the count of possible positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x, m = map(int, input().split())
    left = right = x
    for _ in range(m):
        l, r = map(int, input().split())
        if l <= right and r >= left:
            left = min(left, l)
            right = max(right, r)
    print(right - left + 1)
```

The solution reads the number of test cases and iterates over them. For each test case, it initializes the reachable range to `[x, x]`. Each operation is checked for overlap, and the range is updated accordingly. Finally, the length of the range is printed. The code uses inclusive indexing and handles single-element ranges correctly because the range computation `right - left + 1` works for `left = right`.

## Worked Examples

**Example 1:**

Input:

```
6 4 3
1 6
2 3
5 5
```

| Step | Operation | left | right |
| --- | --- | --- | --- |
| Init | - | 4 | 4 |
| 1 | [1,6] | 1 | 6 |
| 2 | [2,3] | 1 | 6 |
| 3 | [5,5] | 1 | 6 |

Output: `6`

The 1 can reach all positions from 1 to 6.

**Example 2:**

Input:

```
4 1 2
2 4
1 2
```

| Step | Operation | left | right |
| --- | --- | --- | --- |
| Init | - | 1 | 1 |
| 1 | [2,4] | 1 | 1 |
| 2 | [1,2] | 1 | 2 |

Output: `2`

The 1 can reach positions 1 and 2 only; the first operation does not extend the range because it does not overlap the initial position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * m) | Each operation is processed once per test case, with $m \le 100$ |
| Space | O(1) | Only two integers are tracked per test case, regardless of $n$ |

Given $m \le 100$ and $t \le 100$, the total operations are at most 10,000, well within 1 second. Memory is negligible since we do not store the array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, x, m = map(int, input().split())
        left = right = x
        for _ in range(m):
            l, r = map(int, input().split())
            if l <= right and r >= left:
                left = min(left, l)
                right = max(right, r)
        print(right - left + 1)
    return output.getvalue().strip()

# Provided samples
assert run("3\n6 4 3\n1 6\n2 3\n5 5\n4 1 2\n2 4\n1 2\n3 3 2\n2 3\n1 2") == "6\n2\n3", "sample"

# Custom test cases
assert run("1\n1 1 1\n1 1") == "1", "single element array"
assert run("1\n10 5 2\n1 4\n7 10") == "1", "operations do not connect"
assert run("1\n10 5 3\n3 6\n5 8\n1 2") == "6", "overlapping ranges expand reach"
assert run("1\n5 3 0") == "1", "no operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 1 1 | 1 | Single-element array |
| 10 5 2 / 1 4 / 7 10 | 1 | Operations do not overlap initial 1 |
| 10 5 3 / 3 6 / 5 8 / 1 2 | 6 | Overlapping operations expand reachable range |
| 5 3 0 | 1 | No operations, 1 cannot move |

## Edge Cases

If the 1 starts at the first or last index, and operations cover ranges including the boundary, the algorithm correctly merges ranges. For example, with `n = 5, x = 5, m = 1` and operation `[4,5]`, the initial range `[5,5]` merges with `[4,5]` to `[4,5]`. The output is `2`, which is correct. Single-element operations `[3,3]` that do not overlap the current range leave the range unchanged, correctly producing the output 1.
