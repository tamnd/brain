---
title: "CF 2121F - Yamakasi"
description: "We are given an integer array and, for each test case, two target values: a required subarray sum s and a required maximum value x. The task is to count how many contiguous subarrays have total sum exactly equal to s and whose largest element is exactly x."
date: "2026-06-08T03:50:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2121
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1032 (Div. 3)"
rating: 1800
weight: 2121
solve_time_s: 181
verified: true
draft: false
---

[CF 2121F - Yamakasi](https://codeforces.com/problemset/problem/2121/F)

**Rating:** 1800  
**Tags:** binary search, brute force, data structures, greedy, two pointers  
**Solve time:** 3m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer array and, for each test case, two target values: a required subarray sum `s` and a required maximum value `x`. The task is to count how many contiguous subarrays have total sum exactly equal to `s` and whose largest element is exactly `x`.

A useful way to think about this is that every subarray contributes two independent constraints. The sum condition depends on all elements together, while the maximum condition depends only on the largest element inside the segment. A valid segment must satisfy both simultaneously.

The constraints force us into linear or near-linear behavior. The total length across all test cases is at most `2 · 10^5`, so any solution that is worse than O(n log n) per test case risks timing out. A quadratic scan over all subarrays is immediately infeasible since it would inspect up to about 10^10 segments in the worst case.

A few edge situations matter and can break naive logic.

One issue is when `x` does not appear in a segment but all elements are smaller. Such segments may satisfy the sum condition but must be excluded because their maximum is strictly less than `x`. For example, if `x = 5` and a segment is `[1, 2, 3]`, its sum might match `s`, but it is invalid.

Another subtle case occurs when elements exceed `x`. Any subarray containing an element greater than `x` must be completely excluded, because its maximum automatically violates the requirement. For instance, if `x = 3`, then a segment containing `4` is always invalid regardless of its sum.

Finally, there is a nontrivial interaction between sum counting and maximum restriction: sum counting is easy with prefix sums, but maximum restriction splits the array into independent regions, which must be handled carefully.

## Approaches

A direct brute-force approach tries all subarrays `[l, r]`, computes their sum and maximum, and counts those matching both conditions. Sum can be computed in O(1) using prefix sums, but maximum still costs O(n) per segment unless preprocessed. Even with preprocessing, enumerating all O(n^2) segments leads to quadratic time, which is far too slow for n up to 2 · 10^5.

The key observation is that the maximum constraint is the real structure driver. Instead of checking “max equals x” directly, we can split the problem:

A subarray has maximum exactly `x` if and only if:

1. Every element is at most `x`, and
2. It contains at least one element equal to `x`.

This suggests splitting the array into maximal blocks separated by elements greater than `x`. Inside each block, all elements are ≤ x, so the only remaining condition for validity is “contains at least one x”.

Now the problem becomes: within each block, count subarrays with sum `s` that include at least one occurrence of `x`.

We handle this using a standard decomposition trick: count all subarrays with sum `s` inside the block, then subtract those that contain no `x`. Subarrays containing no `x` live entirely inside smaller segments formed by splitting the block at every position where `a[i] == x`.

So each block splits into segments of elements strictly `< x`. For each such segment, we count subarrays with sum `s` using prefix sums and a hashmap frequency count.

This reduces the global problem into two passes of prefix-sum counting over linear segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

### 1. Split array by elements greater than x

We scan the array and break it into contiguous segments where all values are ≤ x. Any segment containing a value > x cannot contribute any valid subarray crossing that value, so it acts as a hard boundary.

This ensures we only work inside regions where maximum could potentially be x.

### 2. Inside each valid segment, separate positions equal to x

Within a segment, we identify indices where `a[i] == x`. These positions will enforce the “must contain x” requirement.

We conceptually divide the segment into smaller subsegments where all values are strictly less than x.

### 3. Count all subarrays with sum s inside the segment

We compute the number of subarrays with sum `s` using prefix sums. We maintain a hashmap `freq[prefix_sum]` and for each position compute how many previous prefix sums equal `current_sum - s`.

This gives total subarrays with sum `s`, regardless of whether they contain x.

### 4. Subtract subarrays that do not contain x

A subarray without x must lie entirely inside one of the “< x only” segments created by cutting at every occurrence of x.

So we iterate over these smaller segments and again count subarrays with sum `s` using the same prefix-sum method, summing over all such segments.

### 5. Combine results

For each valid segment:

result += (count of all sum-s subarrays) − (count of sum-s subarrays without x)

### Why it works

The algorithm relies on partitioning the search space into disjoint classes. Every subarray in a region where all elements ≤ x is either missing x entirely or contains at least one x. These two categories are disjoint and cover all possibilities. The prefix-sum method correctly counts subarrays by converting the sum constraint into frequency matching on prefix differences. Because each segment is processed independently, no subarray is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def count_sum(arr, target):
    freq = defaultdict(int)
    freq[0] = 1
    cur = 0
    res = 0
    for v in arr:
        cur += v
        res += freq[cur - target]
        freq[cur] += 1
    return res

def solve():
    t = int(input())
    for _ in range(t):
        n, s, x = map(int, input().split())
        a = list(map(int, input().split()))

        ans = 0
        i = 0

        while i < n:
            if a[i] > x:
                i += 1
                continue

            j = i
            while j < n and a[j] <= x:
                j += 1

            segment = a[i:j]

            total = count_sum(segment, s)

            # subtract subarrays that contain no x
            bad = 0
            k = 0
            while k < len(segment):
                if segment[k] == x:
                    k += 1
                    continue
                l = k
                tmp = []
                while k < len(segment) and segment[k] != x:
                    tmp.append(segment[k])
                    k += 1
                bad += count_sum(tmp, s)

            ans += total - bad
            i = j

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first isolates valid regions where the maximum constraint can be satisfied. It then counts all subarrays with the required sum using a prefix frequency map. After that, it removes those subarrays that never include `x` by recomputing the same counting process on subsegments separated by occurrences of `x`.

A subtle detail is that we never explicitly check the maximum inside counting functions. The maximum constraint is enforced structurally by segmentation rather than computed directly, which avoids any O(n) maximum queries per subarray.

## Worked Examples

Consider a simplified trace:

Input:

```
1
5 3 2
1 2 -1 2 1
```

We process the single segment since all values are ≤ 2.

| Step | Segment | Current action | Notes |
| --- | --- | --- | --- |
| 1 | [1,2,-1,2,1] | total sum-s subarrays | all valid candidates ignoring max |
| 2 | split at x=2 | [1], [2], [-1], [2], [1] | isolate x-free regions |
| 3 | count bad | subarrays without 2 | only within [1], [-1], [1] |
| 4 | answer | total - bad | keeps only subarrays containing 2 |

This shows that the subtraction correctly enforces “must include x”.

Now consider a case with a blocking value:

```
1
5 0 2
2 1 5 1 2
```

| Step | Segment | Action | Notes |
| --- | --- | --- | --- |
| 1 | split by >2 | [2,1], [1,2] | 5 breaks segment |
| 2 | process [2,1] | prefix sums | valid region |
| 3 | process [1,2] | prefix sums | independent region |

This confirms that elements greater than `x` correctly separate independent computations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element participates in a constant number of prefix-sum scans across segmentation |
| Space | O(n) | Hashmaps for prefix frequencies within segments |

The total array length over all test cases is bounded by 2 · 10^5, so linear processing per element easily fits within the time limit. The use of prefix hash maps ensures constant amortized operations per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# NOTE: placeholder since full solution function not wrapped
# These are structural tests rather than executable asserts

# edge: single element equal to x and s
# edge: all elements > x
# edge: negative numbers with valid sum
# edge: multiple blocks split by > x
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element match | 1 | minimal case |
| all > x | 0 | full rejection |
| negative sums | correct count | prefix-sum correctness |
| multiple blocks | combined answer | segmentation correctness |

## Edge Cases

A key edge case is when every element is greater than `x`. In this situation, the algorithm immediately skips all segments since no valid block is formed. For example:

Input:

```
1
4 5 2
3 4 5 6
```

The scan finds no segment where `a[i] <= 2`, so the answer remains 0. This is correct because no subarray can have maximum exactly 2.

Another edge case occurs when `x` appears multiple times but sum-valid subarrays never include it. In that case, `total - bad` becomes zero naturally because all valid-sum segments lie in x-free regions.
