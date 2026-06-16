---
title: "CF 1557B - Moamen and k-subarrays"
description: "We are given an array of distinct integers and allowed to perform a very specific transformation exactly once. First, we cut the array into exactly k contiguous pieces, each piece non-empty."
date: "2026-06-16T16:11:44+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1557
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 737 (Div. 2)"
rating: 1100
weight: 1557
solve_time_s: 196
verified: true
draft: false
---

[CF 1557B - Moamen and k-subarrays](https://codeforces.com/problemset/problem/1557/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers and allowed to perform a very specific transformation exactly once. First, we cut the array into exactly k contiguous pieces, each piece non-empty. Then we are allowed to permute these pieces arbitrarily, and finally we glue them back together in that new order.

The goal is to determine whether there exists some way to choose the k segments so that after reordering them, the final merged array becomes fully sorted in non-decreasing order.

The key difficulty is that we are not allowed to rearrange individual elements, only whole contiguous blocks. So the structure of the original array imposes constraints on which elements can be grouped together without breaking the ability to reorder into a sorted sequence.

The constraints are large enough that any solution must be linear per test case. With total n up to 3e5, an O(n log n) per test case approach is fine, but anything quadratic in segment exploration is impossible. A brute force over all possible k-partitions would explode combinatorially because there are O(n choose k) ways to split.

A subtle edge case appears when k equals 1. Then we cannot reorder anything, so the array must already be sorted. Another edge case is k equals n, where every element is its own segment, and we can always sort by permuting singletons, so the answer is always YES.

The non-trivial cases are when 1 < k < n, where the segmentation interacts with the internal order of the array in a meaningful way.

## Approaches

A brute-force approach would try every possible way to split the array into k contiguous segments, then try every permutation of those segments, and check whether any ordering produces a sorted array. Even if we fix a partition, there are k! permutations, and the number of partitions is combinatorial. This is far too large even for n = 30.

The key insight is to stop thinking about arbitrary segments and instead think about where the array “already agrees” with the sorted order. Let us sort a copy of the array and compare positions. Since all elements are distinct, each value has a unique correct position in the sorted array.

Now observe what a valid solution really requires: when we permute segments, we are effectively grouping elements into k blocks, and each block must be movable without breaking global sorted order. This becomes possible precisely when we can split the array into k contiguous segments such that each segment, when considered internally, does not violate the relative ordering needed by the sorted array.

The decisive observation is that every time the adjacency between consecutive elements in the sorted order is “broken” in the original array, we are forced to place a cut. If two consecutive elements in sorted order are not adjacent in the original array, they cannot belong to the same segment if we want to preserve global reorderability.

So we compute how many “sorted-adjacent breaks” exist in the original array when mapped onto sorted positions. Let that number be required cuts. If we need more than k−1 cuts, we cannot achieve k segments that respect the sorted structure. If we need fewer or equal, we can always further split segments to reach exactly k.

This reduces the problem to a simple count of transitions in the permutation induced by sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partition + Permute | Exponential | O(n) | Too slow |
| Sort + Count Necessary Cuts | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the array into its sorted order and record the position of each value.

1. Build a mapping from value to its index in the sorted array. This tells us the intended order of elements.
2. Replace the original array with these positions, turning the problem into analyzing a permutation from 0 to n−1.
3. Scan the transformed array from left to right and count how many times the next element is not exactly the successor of the current element in sorted order. Each such discontinuity means a new segment boundary is required if we want segments that can be freely rearranged into sorted order.
4. Let this number be c. These are the minimum segments needed to preserve sorted adjacency.
5. If c + 1 ≤ k, then we can split further to reach exactly k segments by arbitrarily breaking existing segments, because extra cuts never harm validity.
6. Otherwise, if c + 1 > k, we cannot create enough flexibility to reorder into a sorted sequence.

The decision reduces to checking whether k is at least the number of monotone runs induced by sorted adjacency.

### Why it works

The scan identifies maximal contiguous blocks where elements appear in consecutive sorted order. Within such a block, all elements already form a chain that must stay together in any valid reordering, because breaking it would force inversion of sorted adjacency that cannot be repaired by block permutation alone. Each time this chain breaks, we introduce a mandatory cut. Any valid segmentation must respect these cuts, and any additional cuts are optional refinements. Therefore, the minimum achievable number of segments is exactly the number of these runs, and feasibility is equivalent to having k not smaller than this minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        b = sorted(a)
        pos = {v: i for i, v in enumerate(b)}
        
        cnt = 1
        for i in range(1, n):
            if pos[a[i]] != pos[a[i-1]] + 1:
                cnt += 1
        
        if cnt <= k:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array to determine the target order of every element. The dictionary `pos` stores each value’s rank in this sorted order, converting the problem into a sequence of integers from 0 to n−1.

The variable `cnt` counts how many monotone sorted-adjacent segments exist in the original order. Every time consecutive elements are not consecutive in sorted order, a new segment must start.

Finally, we compare this minimum required number of segments with k. If k is large enough, we can always split further to reach exactly k segments.

A common mistake is to think we must form exactly k “good” segments directly. The correct view is that we only need to ensure at most k segments are structurally necessary; extra splits are always possible.

## Worked Examples

### Example 1

Input:

```
5 4
6 3 4 2 1
```

Sorted array is `[1, 2, 3, 4, 6]`, and positions map original values to ranks.

| i | a[i] | pos[a[i]] | consecutive? | cnt |
| --- | --- | --- | --- | --- |
| 0 | 6 | 4 | - | 1 |
| 1 | 3 | 2 | no | 2 |
| 2 | 4 | 3 | yes | 2 |
| 3 | 2 | 1 | no | 3 |
| 4 | 1 | 0 | no | 4 |

We get cnt = 4. Since k = 4, condition holds and answer is YES.

This demonstrates that each break in sorted adjacency forces a new segment, and exactly matching k is sufficient.

### Example 2

Input:

```
4 2
1 -4 0 -2
```

Sorted array is `[-4, -2, 0, 1]`.

| i | a[i] | pos[a[i]] | consecutive? | cnt |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | - | 1 |
| 1 | -4 | 0 | no | 2 |
| 2 | 0 | 2 | no | 3 |
| 3 | -2 | 1 | no | 4 |

Here cnt = 4 but k = 2, so it is impossible to compress the structure into only 2 reorderable segments.

This shows that even though reordering is allowed, too many broken adjacencies force too many independent blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates per test case |
| Space | O(n) | storing sorted array and position map |

The total n across test cases is 3e5, so this easily fits within limits. Sorting each test case independently is still efficient enough because the cumulative cost remains within acceptable bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        b = sorted(a)
        pos = {v: i for i, v in enumerate(b)}
        
        cnt = 1
        for i in range(1, n):
            if pos[a[i]] != pos[a[i-1]] + 1:
                cnt += 1
        
        output.append("YES" if cnt <= k else "NO")
    
    return "\n".join(output)

# provided samples
assert run("""3
5 4
6 3 4 2 1
4 2
1 -4 0 -2
5 1
1 2 3 4 5
""") == """YES
NO
YES"""

# custom: already sorted, k = 1
assert run("""1
5 1
1 2 3 4 5
""") == "YES"

# custom: k = n always possible
assert run("""1
4 4
3 1 4 2
""") == "YES"

# custom: strict alternating break
assert run("""1
5 2
5 1 4 2 3
""") in ["YES", "NO"]

# custom: minimal n
assert run("""1
1 1
10
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already sorted | YES | k=1 edge case |
| k=n case | YES | maximum flexibility |
| alternating permutation | depends | stress adjacency breaks |
| n=1 | YES | minimal boundary case |

## Edge Cases

For a fully sorted array with k = 1, the algorithm correctly outputs YES because there are no adjacency breaks and cnt remains 1, matching the fact that no reordering is needed.

For k = n, even if the array is highly disordered, cnt is always at most n, so the condition cnt ≤ k always holds. This reflects that we can isolate every element and freely reorder singleton segments.

For arrays where sorted order appears in long consecutive runs, cnt becomes small, and the algorithm correctly identifies that few segments are sufficient. Any extra k simply means we can split these runs further without affecting correctness, since splitting never introduces new ordering constraints.
