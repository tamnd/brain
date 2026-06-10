---
title: "CF 1490G - Old Floppy Drive "
description: "We have a circular array of integers, representing a disk in an old floppy drive. Each integer can be positive or negative."
date: "2026-06-10T22:42:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 1490
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 702 (Div. 3)"
rating: 1900
weight: 1490
solve_time_s: 164
verified: true
draft: false
---

[CF 1490G - Old Floppy Drive ](https://codeforces.com/problemset/problem/1490/G)

**Rating:** 1900  
**Tags:** binary search, data structures, math  
**Solve time:** 2m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular array of integers, representing a disk in an old floppy drive. Each integer can be positive or negative. When the drive receives a number $x$, it starts at the first element and sums the elements in order, looping around as needed, until the cumulative sum reaches at least $x$. The time counted is the number of elements visited. For multiple queries, we need to determine how long the drive will take to reach or exceed each query value. If the sum of the entire array is non-positive, it is possible that some $x$ values are unreachable, in which case the drive would run indefinitely and we return $-1$.

The inputs can be large: the array size $n$ and number of queries $m$ can each be up to $2 \cdot 10^5$, and the total sum across all test cases does not exceed $2 \cdot 10^5$. This means that an $O(n \cdot m)$ brute-force approach is infeasible. We need a solution that preprocesses the array and answers each query efficiently, ideally in $O(\log n)$ time per query after some linear preprocessing.

Edge cases include arrays with all negative numbers, where some queries can never be satisfied, or arrays with a mix of positive and negative numbers where the maximum prefix sum is less than the query. For instance, if $a = [-2, -1]$ and $x = 1$, no amount of rotations will reach $x$, so the answer must be $-1$. Another subtle case occurs when the query is smaller than the first element; the drive may stop immediately, even at time $0$.

## Approaches

The brute-force method simulates the disk rotation for each query individually. It keeps a running sum starting from the first element, adds the next element each second, and wraps around at the end of the array. It stops when the sum reaches the query. This approach works correctly but performs $O(n \cdot m)$ operations in the worst case. With $n$ and $m$ up to $2 \cdot 10^5$, this would be up to $4 \cdot 10^{10}$ operations, far exceeding the time limit.

The key observation is that the disk is circular. The cumulative sum of one full rotation is a constant, $S = \sum a_i$. If $S \le 0$, the sum cannot increase indefinitely, and some queries will never be reached. If $S > 0$, after one full rotation, the cumulative sum increases by $S$, so we can compute how many full rotations are needed before reaching the query. Within one rotation, we only need the maximum prefix sums to find how far we need to go.

We can preprocess an array of prefix sums, storing the maximum sum reached at each index. Then, for each query, we check if it can be satisfied within the first rotation. If not, and the total sum $S > 0$, we compute the minimum number of full rotations needed using integer division, and finally use binary search on the prefix sums of a single rotation to determine the additional steps required. This reduces the query complexity to $O(\log n)$ after $O(n)$ preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Optimal | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix sums of the array $a$, and for each position $i$, store the maximum sum reached up to that position. Let this array be `max_prefix`.
2. Compute the total sum of the array, `total_sum = sum(a)`.
3. For each query $x`:

1. If `max_prefix[-1] >= x`, the answer is within the first rotation. Use binary search on `max_prefix` to find the earliest index where the prefix sum is at least $x$. The time is this index.
2. If `total_sum <= 0` and `max_prefix[-1] < x`, the query is impossible. Return `-1`.
3. Otherwise, compute how many full rotations `k` are needed so that `total_sum * k + max_prefix[-1] >= x`. This can be computed using integer division: `k = max(0, (x - max_prefix[-1] + total_sum - 1) // total_sum)`.
4. Compute the remaining sum `x' = x - total_sum * k`. Use binary search on `max_prefix` to find the earliest index where the prefix sum is at least `x'`. The total time is `k * n + index`.
4. Return the times for all queries.

Why it works: the maximum prefix sum in one rotation determines how far we need to go in that rotation. Each full rotation increases the cumulative sum by `total_sum`. By computing the number of full rotations needed and combining it with the prefix sum within a single rotation, we find the earliest time to reach the query. The invariants are that prefix sums are non-decreasing, and total_sum captures the net increase per full rotation.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left

for _ in range(int(input())):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    x = list(map(int, input().split()))

    prefix = []
    curr = 0
    max_prefix = []
    for num in a:
        curr += num
        prefix.append(curr)
        max_prefix.append(curr if not max_prefix else max(max_prefix[-1], curr))
    
    total_sum = curr

    for q in x:
        if max_prefix[-1] >= q:
            idx = bisect_left(max_prefix, q)
            print(idx, end=' ')
        elif total_sum <= 0:
            print(-1, end=' ')
        else:
            k = (q - max_prefix[-1] + total_sum - 1) // total_sum
            remaining = q - k * total_sum
            idx = bisect_left(max_prefix, remaining)
            print(k * n + idx, end=' ')
    print()
```

The code first builds the prefix sums and the maximum prefix sums for efficient querying. `bisect_left` finds the earliest index where a prefix sum reaches the desired value. Full rotations are accounted for with integer division, and edge cases for non-increasing arrays are handled explicitly.

## Worked Examples

Sample Input 1:

```
3
3 3
1 -3 4
1 5 2
2 2
-2 0
1 2
2 2
0 1
1 2
```

Trace for the first test case:

| Query x | max_prefix | total_sum | rotations k | remaining x' | index | total time |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,1,4] | 2 | 0 | 1 | 0 | 0 |
| 5 | [1,1,4] | 2 | 2 | 1 | 0 | 6 |
| 2 | [1,1,4] | 2 | 1 | 0 | 2 | 2 |

This shows the algorithm correctly finds times using rotations and prefix sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | Prefix sums built in O(n), each query answered with binary search O(log n) |
| Space | O(n) | Storing prefix sums and max_prefix |

The solution fits comfortably within the constraints of $n, m \le 2\cdot 10^5$ and 2s time limit.

## Test Cases

```python
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    for _ in range(int(input())):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        x = list(map(int, input().split()))

        prefix = []
        curr = 0
        max_prefix = []
        for num in a:
            curr += num
            prefix.append(curr)
            max_prefix.append(curr if not max_prefix else max(max_prefix[-1], curr))

        total_sum = curr

        res = []
        for q in x:
            if max_prefix[-1] >= q:
                idx = bisect_left(max_prefix, q)
                res.append(str(idx))
            elif total_sum <= 0:
                res.append(str(-1))
            else:
                k = (q - max_prefix[-1] + total_sum - 1) // total_sum
                remaining = q - k * total_sum
                idx = bisect_left(max_prefix, remaining)
                res.append(str(k * n + idx))
        output.write(' '.join(res)+'\n')
    return output.getvalue().strip()

# Provided sample
assert run("3\n3 3\n1 -3 4\n1 5 2\n2 2\n-2 0\n1 2\n2 2\n0 1\n1 2\n") == "0 6 2\n-1 -1\n1 3"

# Custom cases
assert run("1\n1 2\n5\n2 6\n") == "0 1", "Single element array"
assert run("1\n3 2
```
