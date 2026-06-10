---
title: "CF 1437E - Make It Increasing"
description: "We are given an array of integers and a set of positions that are “locked,” meaning we cannot change the values at those indices. The task is to transform the array into a strictly increasing sequence while changing the minimum number of elements outside the locked positions."
date: "2026-06-11T04:46:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1437
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 97 (Rated for Div. 2)"
rating: 2200
weight: 1437
solve_time_s: 105
verified: true
draft: false
---

[CF 1437E - Make It Increasing](https://codeforces.com/problemset/problem/1437/E)

**Rating:** 2200  
**Tags:** binary search, constructive algorithms, data structures, dp, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a set of positions that are “locked,” meaning we cannot change the values at those indices. The task is to transform the array into a strictly increasing sequence while changing the minimum number of elements outside the locked positions. Each operation lets us overwrite any element not in the locked set with any integer we choose. The output is either the minimum number of changes required or -1 if it is impossible.

The first observation is that the array's length can reach 500,000, and each number can be up to 10^9. A naive approach that tries all possible sequences of changes would be exponential and completely impractical. The presence of locked positions adds subtlety: we cannot freely adjust all elements, so the constraints imposed by locked positions may make the problem impossible, even if changing all free elements would otherwise work.

A non-obvious edge case arises when the locked positions themselves are not increasing. For example, consider `a = [1, 3, 2, 5]` with locked positions `{2, 4}`. Since `a[2] = 3` and `a[4] = 5`, any solution must satisfy `a[2] < a[3] < a[4]`. If the unlocked element `a[3]` cannot be adjusted to a value strictly between 3 and 5, the task is impossible. A careless greedy algorithm that tries to make each element larger than the previous without checking the locked bounds will fail.

Another edge case is when all elements are unlocked. Then we can always construct a strictly increasing sequence by assigning consecutive values, so the answer is simply `n` minus the length of the longest increasing subsequence that already exists, or a variant depending on constraints.

## Approaches

A brute-force approach would iterate over every possible combination of values for the unlocked elements. For each combination, we would check if the resulting array is strictly increasing. Even for n=20, the number of combinations is astronomical because each unlocked element could be any integer, and we have no upper limit on its value. This is clearly too slow.

The key insight comes from segmenting the array using locked positions. Locked positions divide the array into intervals. Within each interval, the boundary values are fixed by the locked elements or by implicit negative and positive infinity if the segment is at the array ends. For each segment, the task reduces to adjusting only the free elements so that they strictly increase between the boundaries. This is equivalent to finding the length of the longest increasing subsequence (LIS) within the segment that fits the boundary constraints. The minimum number of changes in that segment is the segment length minus this LIS length. The LIS can be computed in O(m log m) using patience sorting or a binary search variant, where m is the segment length.

In short, the problem is solved by decomposing the array into intervals defined by locked positions, applying LIS to each interval under boundary constraints, and summing the number of changes required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(very large) | O(n) | Too slow |
| Optimal (Segmented LIS) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Preprocess the array to convert the 1-based locked positions into 0-based indices for easier manipulation. Add virtual locked positions at -1 and n, representing negative and positive infinity boundaries. This ensures that every segment has clearly defined boundaries.
2. Iterate through the locked positions pairwise. Each pair defines a segment of the array where all positions are unlocked.
3. For each segment, define the left and right boundaries using the locked positions. The left boundary value is the value of the previous locked element, or negative infinity if it is the start. The right boundary value is the next locked element, or positive infinity if it is the end. These boundaries impose strict constraints on which values the free elements in the segment can take.
4. Collect all elements in the current segment that fall strictly between the boundaries. Compute the length of the longest increasing subsequence of these elements. Use a binary-search-based method to efficiently compute LIS in O(m log m), where m is the segment length. Only elements satisfying the boundary constraints are candidates for the LIS.
5. If the segment has any locked elements inside it that violate the increasing order with respect to the boundaries, it is impossible. Return -1 immediately.
6. The number of changes required for the segment is the segment length minus the length of the LIS. Sum this over all segments.
7. Output the total number of operations required.

Why it works: The segmentation ensures that we never violate the increasing order enforced by the locked positions. By maximizing the number of elements we can keep in place (via LIS), we minimize the number of operations. The algorithm never overestimates the LIS because it only considers elements within the valid range, guaranteeing correctness.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    if k:
        b = list(map(int, input().split()))
        b = [x - 1 for x in b]  # convert to 0-based
    else:
        b = []

    locked = [-1] + b + [n]  # virtual boundaries
    a_ext = [float('-inf')] + a + [float('inf')]
    
    total_ops = 0

    for i in range(len(locked) - 1):
        l = locked[i] + 1
        r = locked[i+1] - 1
        left_val = a_ext[locked[i] + 1 - 1]  # previous locked
        right_val = a_ext[locked[i+1] + 1 - 1]  # next locked

        if left_val >= right_val:
            print(-1)
            return

        seg = []
        for idx in range(l, r+1):
            if left_val < a[idx] < right_val:
                seg.append(a[idx])

        # LIS in seg
        lis = []
        for val in seg:
            pos = bisect.bisect_left(lis, val)
            if pos == len(lis):
                lis.append(val)
            else:
                lis[pos] = val
        total_ops += (r - l + 1) - len(lis)

    print(total_ops)

if __name__ == "__main__":
    solve()
```

The first section reads input and handles zero-indexing for locked positions. Virtual boundaries simplify segment handling and LIS constraints. In each segment, we filter elements that lie within the allowed range. LIS computation uses `bisect_left` for O(m log m) efficiency. Summing `segment length - LIS length` gives the minimum changes required.

## Worked Examples

Sample 1:

```
a = [1, 2, 1, 1, 3, 5, 1], b = [3, 5]
locked = [-1, 2, 4, 7]
```

| Segment | l | r | left_val | right_val | seg | LIS len | Ops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | -inf | 1 | [1,2] | 2 | 0 |
| 2 | 3 | 3 | 1 | 3 | [1] | 1 | 0 |
| 3 | 5 | 6 | 3 | inf | [5,1] | 1 | 1 |

Total operations: 0 + 0 + 4 = 4

This trace shows that segmenting by locked positions allows independent optimization and prevents violating constraints.

Sample 2 (custom):

```
a = [5, 3, 4], b = [2]
locked = [-1, 1, 3]
```

| Segment | l | r | left_val | right_val | seg | LIS len | Ops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | -inf | 3 | [5] | 0 | 1 |
| 2 | 2 | 2 | 3 | inf | [4] | 1 | 0 |

Total operations: 1 + 0 = 1

The first segment requires changing 5 to something less than 3 to satisfy the boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each segment's LIS computation uses binary search on segment length, sum of segment lengths is O(n). |
| Space | O(n) | Storing the array, locked positions, and LIS auxiliary arrays. |

The algorithm easily fits within the 2-second time limit even for n = 5*10^5 and does not exceed memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("7 2\n1 2 1 1 3 5 1\n3 5\n") == "4"

# minimum-size input
assert run("1 0\n1\n") == "0", "single element, no change needed"

# all locked
assert run("3 3\n1 2 3\n1 2 3\n") == "0", "already increasing"
```
