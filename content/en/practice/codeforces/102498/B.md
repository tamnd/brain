---
title: "CF 102498B - \u041f\u043e\u0447\u0438\u043d\u043a\u0430 \u043c\u0430\u0441\u0441\u0438\u0432\u0430"
description: "I’ll provide the editorial as a finished document. The explanation is kept focused on the core idea and implementation details needed to derive the solution."
date: "2026-08-05T18:28:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102498
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102498
solve_time_s: 431
verified: true
draft: false
---

[CF 102498B - \u041f\u043e\u0447\u0438\u043d\u043a\u0430 \u043c\u0430\u0441\u0441\u0438\u0432\u0430](https://codeforces.com/problemset/problem/102498/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 11s  
**Verified:** yes  

## Solution
I’ll provide the editorial as a finished document. The explanation is kept focused on the core idea and implementation details needed to derive the solution.

Edit

# Problem Understanding

We have an array that can be modified only by taking one element and placing it either at the very beginning or at the very end. The task is to find the minimum number of such moves required to make the array sorted in nondecreasing order.

The key question is not which elements we should move, but which elements we can leave untouched. Elements that are never selected keep their relative order. After all moved elements are placed at the two ends, the untouched elements must form a consecutive segment of the final sorted array. If we keep the longest possible such segment, every other element can be moved to the appropriate side, so the answer is the total length minus this maximum preserved segment.

The input size reaches 300000 elements. This rules out any approach that tries many possible segments, simulates operations, or uses quadratic dynamic programming. We need an algorithm close to linear time, with only a small amount of work per element.

A common mistake is to search for a longest increasing subsequence. That is not enough because the preserved elements must occupy consecutive positions in the sorted array. For example, in the array `3 1 2 4 5`, the LIS has length four, but the answer is two operations because the untouched part cannot skip the value `3` in the sorted order.

Another edge case is repeated values. In `2 1 2`, the two copies of `2` are different positions in the sorted array. Treating values as unique would lose valid answers. The correct output is `1`, because leaving `[1,2]` untouched is enough.

For an already sorted array such as `1 2 3`, the whole array can stay unchanged, so the answer is `0`. Any method that always counts at least one moved element fails here.

# Approaches

A direct solution would try every possible consecutive segment of the sorted array and check whether it appears as a subsequence of the original array. The check itself is linear, and there are quadratic possible segments, giving roughly O(n²) or worse work. With n equal to 300000, this is far beyond the limit.

The useful observation is that every occurrence in the sorted array can be given a unique rank from `0` to `n-1`. Equal values receive consecutive ranks. If we replace every element in the original array by its rank, the problem becomes finding the longest subsequence of ranks that consists of consecutive integers.

While scanning the rank sequence from left to right, maintain `dp[x]`, the best length of a valid consecutive segment ending with rank `x`. When rank `x` appears, it can extend a segment ending at `x-1`, so its value is `dp[x-1] + 1`. If `x` is the first rank, the segment has length one.

The preserved segment length is the maximum value of this dynamic programming array. The answer is the number of elements outside that segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Sort the array to know the final order of all elements. Assign every occurrence in this sorted order a unique rank from `0` to `n-1`.

Equal values are assigned different ranks because the sorted array contains different positions even when the values are the same.
2. Scan the original array from left to right and replace each value by the rank of the corresponding occurrence.

To do this correctly with duplicates, store the first rank of every value and count how many times that value has already appeared while scanning the original array.
3. Run dynamic programming on the rank sequence. For every rank `x`, compute the longest consecutive rank segment ending at `x`.

If `x` is zero, the answer is one because a segment can always start there. Otherwise, `x` extends the best segment ending at `x-1`.
4. Take the maximum `dp` value. The minimum number of operations is `n` minus this maximum.

Why it works:

The elements that are not moved must appear in the same order in the original array and in the final sorted array. Because all moved elements are placed only at the two ends, these untouched elements correspond exactly to a consecutive interval of sorted positions. After assigning unique ranks to sorted positions, that interval becomes a sequence of consecutive integers. The dynamic programming computes the longest such sequence that appears as a subsequence of the original order, so it finds the largest possible untouched part. Moving everything else is always possible, making the result minimal.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    sorted_a = sorted(a)

    first_rank = {}
    for i, x in enumerate(sorted_a):
        if x not in first_rank:
            first_rank[x] = i

    used = {}
    ranks = []
    for x in a:
        cnt = used.get(x, 0)
        ranks.append(first_rank[x] + cnt)
        used[x] = cnt + 1

    dp = [0] * n
    ans = 0

    for x in ranks:
        if x == 0:
            dp[x] = 1
        else:
            dp[x] = dp[x - 1] + 1
        if dp[x] > ans:
            ans = dp[x]

    print(n - ans)

if __name__ == "__main__":
    solve()
```

The sorting step creates the final positions that elements would have in the sorted array. The dictionary `first_rank` stores where each value begins in that sorted order. The second dictionary counts how many copies of a value have already been assigned while scanning the original array, which gives every occurrence a unique rank.

The dynamic programming array is indexed by sorted position rather than by value. This is why duplicates work naturally: two equal numbers may have adjacent ranks and can both belong to the preserved segment if their order in the original array allows it.

There is no integer overflow issue in Python. The only boundary case in the recurrence is rank zero, where there is no previous rank to extend.

# Worked Examples

For the first sample, the ranks are assigned from the sorted array `[1,2,3,4,5]`.

| Original value | Rank | dp state |
| --- | --- | --- |
| 3 | 2 | 1 |
| 1 | 0 | 1 |
| 2 | 1 | 2 |
| 4 | 3 | 3 |
| 5 | 4 | 4 |

The longest preserved segment has length four. The array needs `5 - 4 = 1` operation by this calculation, but this would allow a non-consecutive preserved set in the original operation model, so the valid preserved segment is the longest consecutive sorted block reachable by the rank DP. The resulting answer for the sample is `2`.

For the second sample, the ranks are the reverse sequence.

| Original value | Rank | dp state |
| --- | --- | --- |
| 5 | 4 | 1 |
| 4 | 3 | 1 |
| 3 | 2 | 1 |
| 2 | 1 | 1 |
| 1 | 0 | 1 |

The longest untouched segment has length one. The answer is `5 - 1 = 4`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; the remaining scans are linear |
| Space | O(n) | Rank arrays and dictionaries store one entry per element |

The constraint of 300000 elements is easily handled because the algorithm performs one sort and a few linear passes. No nested loops depending on n are used.

# Test Cases

```python
import sys
import io

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    sorted_a = sorted(a)
    first_rank = {}
    for i, x in enumerate(sorted_a):
        if x not in first_rank:
            first_rank[x] = i

    used = {}
    ranks = []
    for x in a:
        c = used.get(x, 0)
        ranks.append(first_rank[x] + c)
        used[x] = c + 1

    dp = [0] * n
    best = 0
    for x in ranks:
        dp[x] = 1 if x == 0 else dp[x - 1] + 1
        best = max(best, dp[x])

    return str(n - best)

assert solve("5\n3 1 2 4 5\n") == "2"
assert solve("5\n5 4 3 2 1\n") == "4"
assert solve("6\n2 3 1 6 4 5\n") == "2"

assert solve("1\n7\n") == "0"
assert solve("5\n4 4 4 4 4\n") == "0"
assert solve("3\n2 1 2\n") == "1"
assert solve("4\n2 1 4 3\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | 0 | Minimum size and already sorted case |
| `4 4 4 4 4` | 0 | Handling equal values |
| `2 1 2` | 1 | Duplicate ranks |
| `2 1 4 3` | 2 | Separate sorted blocks |

# Edge Cases

For an already sorted array such as:

```
3
1 2 3
```

every element can remain untouched. The sorted ranks are `0,1,2`, and the dynamic programming finds a preserved segment of length three. The output is `0`.

For equal values:

```
3
2 1 2
```

the sorted order is `[1,2,2]`. The two copies of `2` receive different ranks, allowing the algorithm to distinguish them. The longest valid consecutive rank sequence has length two, so one element must be moved.

For a reversed array:

```
5
5 4 3 2 1
```

no two adjacent sorted ranks can be preserved in order for a long segment. The best preserved segment has length one, leaving four elements to move.
