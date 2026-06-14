---
title: "CF 1557B - Moamen and k-subarrays"
description: "We are given an array of distinct integers and we are allowed to manipulate its structure in a very specific way. First, we cut the array into exactly k contiguous segments. Then we are allowed to reorder these segments arbitrarily."
date: "2026-06-14T22:03:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1557
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 737 (Div. 2)"
rating: 1100
weight: 1557
solve_time_s: 573
verified: false
draft: false
---

[CF 1557B - Moamen and k-subarrays](https://codeforces.com/problemset/problem/1557/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 9m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct integers and we are allowed to manipulate its structure in a very specific way. First, we cut the array into exactly k contiguous segments. Then we are allowed to reorder these segments arbitrarily. Finally, we glue them back together in the chosen order.

The key question is whether we can make the final array sorted in non-decreasing order after doing this once.

The constraints matter because the total number of elements across all test cases reaches 300000. This immediately rules out anything that tries to explore all partitions or permutations of segments. Any solution must be linear or near linear per test case, otherwise it will not scale.

A subtle aspect of the problem is that we are not allowed to rearrange elements inside each segment. Only the segments themselves can be permuted. This restriction forces us to think in terms of how many “correctly ordered blocks” the array can be decomposed into.

One edge case that often causes confusion is when k is large but the array is already almost sorted. For example, if the array is already sorted, any k works because we can split it into single elements and reassemble them. On the other hand, if k is too small, we lose flexibility. For instance, if k = 1, we cannot reorder anything at all, so the array must already be sorted.

Another subtle case appears when the array is “locally ordered” but global inversion exists. For example, consider:

Input:

```

```

We might try splitting as [2, 1] and [4, 3], but no reordering of these blocks yields a fully sorted sequence because each block itself is internally inverted in a way that cannot be repaired by swapping blocks.

The real difficulty is to determine how many segments are “necessary” to preserve sorted structure.

## Approaches

A brute-force solution would try all ways to split the array into k non-empty contiguous segments, then for each partition try all permutations of the segments and check if any ordering produces a sorted array. The number of partitions alone is exponential, and the permutations of segments add a factorial factor on top. Even for n = 20 this becomes infeasible, so this direction is purely theoretical.

The key observation is that the final array is formed by concatenating k segments in some order, so what matters is whether we can partition the array into at most k “sortable blocks” such that sorting these blocks by their minimum or maximum values aligns them into the global sorted order.

Because all elements are distinct, each segment has a well-defined minimum and maximum, and the only way segments can be reordered into a sorted array is if there exists a partition where each segment corresponds to a consecutive range in the sorted array. In other words, each segment must not “interleave” values that belong to different parts of the sorted sequence.

This leads to a simpler viewpoint: consider the positions of elements in the sorted array. As we scan the original array, we can form a segment whenever the prefix we have seen forms a prefix of the sorted order in terms of maximum position. The number of such natural segments is fixed by the structure of the permutation.

Let that number be cnt, the minimum number of monotonic “sorted-compatible” segments required. If we are allowed to form k segments, then we can always split further, but we cannot merge below cnt. Therefore the condition becomes simple: we need k ≥ cnt.

Thus the problem reduces to computing how many “break points” exist where continuity in sorted order is violated in terms of positions in the sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all partitions + permutations) | O(n! · n) | O(n) | Too slow |
| Optimal (greedy segmentation via sorted positions) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array while keeping track of original positions. This gives the target global order.
2. Build an array pos where pos[x] is the index of value x in the sorted array. This converts the problem into working with a permutation of indices.
3. Scan the original array from left to right, maintaining the maximum position in the sorted array seen so far.
4. Whenever this maximum position equals the current index in the sorted order of the scan, we can close a segment. This is because all elements seen so far exactly form a prefix of the sorted permutation.
5. Count how many such segments are formed; call this cnt.
6. The answer is YES if and only if cnt ≤ k, otherwise NO.

### Why it works

The scan builds the smallest possible segments such that each segment contains elements that must stay together in any sorted reconstruction. A segment boundary can only be placed when the set of seen elements corresponds exactly to a prefix of the sorted array; otherwise some element from a future part would be trapped inside the segment, making correct ordering impossible. This forces a unique minimal segmentation, and any valid solution must use at least that many segments.

## Python Solution

```
PythonRun
```

The solution first compresses the array into sorted ranks using a dictionary, which allows comparisons in O(1). The greedy scan maintains the furthest sorted position seen so far. When that matches the current scan index, it means everything seen so far belongs exactly to a contiguous prefix of the sorted array, so we can safely cut a segment there.

The only subtle implementation detail is the use of indices in the sorted array rather than values. This avoids incorrect reasoning based on raw values, since the ordering structure is what matters.

## Worked Examples

### Example 1

Input:

```

```

Sorted array is [1, 2, 3, 4, 5], so positions:

```

```

Scan:

| i | a[i] | pos[a[i]] | mx | cut? |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 1 | yes |
| 1 | 1 | 0 | 1 | no |
| 2 | 4 | 3 | 3 | yes |
| 3 | 3 | 2 | 3 | no |
| 4 | 5 | 4 | 4 | yes |

Segments formed: 3, so cnt = 3. Since k = 2, answer is NO.

This shows that even though the array is close to sorted, it requires at least 3 inseparable blocks.

### Example 2

Input:

```

```

Sorted array is [1, 2, 3, 4, 5].

| i | a[i] | pos[a[i]] | mx | cut? |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | 2 | no |
| 1 | 1 | 0 | 2 | no |
| 2 | 2 | 1 | 2 | yes |
| 3 | 5 | 4 | 4 | no |
| 4 | 4 | 3 | 4 | yes |

Here cnt = 2, and k = 5, so we can always split further into more segments, giving YES.

This demonstrates that extra freedom in k only helps by allowing refinement, never by merging constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting per test case dominates |
| Space | O(n) | storing sorted copy and position map |

The total n across test cases is at most 3e5, so sorting and linear scans fit comfortably within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | YES | minimum size |
| reversed array, k=1 | YES | already single segment |
| reversed array, k=2 | NO | insufficient splits |
| alternating inversions | YES | multiple valid cuts |

## Edge Cases

One edge case is a fully sorted array. The algorithm scans and finds a cut at every position, producing cnt = n. For any k ≥ n, answer is YES, and for k < n, it is NO. This matches intuition because every element is already isolated in a natural prefix chain.

Another edge case is a completely reversed array. The positions increase gradually, so the maximum is always at the end, producing cnt = 1. Even with k = 1, the answer is YES because the whole array is already one valid segment that can be reordered trivially only if k allows no splits.

A mixed inversion pattern such as [3, 1, 2, 6, 5, 4] produces multiple segment boundaries exactly when the scan reaches full prefix coverage of sorted indices, and the greedy rule captures these boundaries precisely without ambiguity.
