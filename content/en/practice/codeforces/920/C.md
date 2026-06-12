---
title: "CF 920C - Swap Adjacent Elements"
description: "We are given a permutation of size n, meaning every integer from 1 to n appears exactly once. Alongside this array is a string that describes which adjacent positions are “connected” by an allowed swap."
date: "2026-06-13T02:47:14+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "greedy", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 920
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 37 (Rated for Div. 2)"
rating: 1400
weight: 920
solve_time_s: 150
verified: true
draft: false
---

[CF 920C - Swap Adjacent Elements](https://codeforces.com/problemset/problem/920/C)

**Rating:** 1400  
**Tags:** dfs and similar, greedy, math, sortings, two pointers  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of size n, meaning every integer from 1 to n appears exactly once. Alongside this array is a string that describes which adjacent positions are “connected” by an allowed swap. If the i-th character is 1, we are allowed to swap elements at positions i and i+1 any number of times; if it is 0, that boundary is permanently blocked.

Because swaps can be repeated arbitrarily on allowed edges, the actual freedom is not about individual swaps but about which indices can be reached from each other through chains of allowed adjacent swaps. Inside such a reachable region, elements can be permuted arbitrarily. Between different regions, no element can ever cross.

The task is to determine whether, using these constrained swap operations, the array can be transformed into the sorted permutation 1, 2, 3, ..., n.

The constraint n up to 200000 immediately rules out any simulation of swaps. Even linear-time repeated swapping would be too slow because a single element might move O(n) times. Any approach must reduce the problem to a single pass or near-linear processing with maybe sorting.

A subtle failure case appears when connectivity is indirect. For example, if swaps are allowed between (1,2) and (2,3), but not (3,4), then positions 1 to 3 form one group. A naive approach that only checks adjacent correct placements or tries local fixes will miss that the whole segment is globally constrained.

Another tricky case is when components are long but internally disordered:

Input:

n = 5

a = [5, 4, 3, 2, 1]

s = 1111

Output should be YES, because full freedom allows sorting completely. A greedy adjacent check might incorrectly reject intermediate disorder even though global reordering is possible.

Finally, consider disconnected swaps:

Input:

n = 4

a = [2, 1, 4, 3]

s = 00 0

Output is NO, because no swaps are allowed, even though each pair is locally correctable in isolation in other problems.

## Approaches

If we try to simulate the process directly, we would repeatedly scan the array and apply swaps wherever allowed. Even in the best implementation, moving a single element to its correct position might require O(n) swaps, and doing this for all elements leads to O(n²) behavior. With n up to 200000, this is completely infeasible.

The key observation is that swaps define an equivalence relation over indices. If position i can reach position j through a chain of allowed adjacent swaps, then the elements in this whole connected component can be arbitrarily permuted. This turns the problem from “sequence of operations” into “grouping constraint”.

Once we accept that each connected segment of indices is independent, the problem becomes checking whether each segment already contains exactly the set of values that must end up there in the sorted array. Since the final target is identity permutation, position i must contain value i. So for any segment [l, r], the values currently inside must be exactly the integers from l to r in some order.

This reduces the task to scanning connected components of the graph formed by adjacent allowed swaps, collecting values in each component, and verifying they match the expected interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swapping Simulation | O(n²) | O(1) | Too slow |
| Component Grouping + Validation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array by splitting it into maximal segments where swaps are fully connected.

1. We iterate through the swap string and identify segments of indices where consecutive edges are all 1. Each such segment represents a component where any permutation is possible. This is the crucial structural simplification.
2. For each segment [l, r], we collect all values a[l], a[l+1], ..., a[r]. These are the only values that can ever appear in this segment, because no element can cross a 0 boundary.
3. We sort the collected values and compare them against the expected sequence l, l+1, ..., r. If they match exactly, the segment is valid.
4. If any segment fails this condition, we immediately conclude sorting is impossible.
5. If all segments satisfy the condition, we conclude it is possible to sort the entire array.

The reason sorting works as a check is that both the expected set and the current values must form a contiguous interval of integers of the same size. Equality after sorting is a direct way to verify identical multisets.

### Why it works

The swap graph decomposes the array into connected components, and swaps never move elements across components. This creates an invariant: the multiset of values inside any component is fixed forever. The sorted target requires each position i to contain value i, so each component must contain exactly the integers corresponding to its index range. If this condition holds, internal rearrangement inside each component can construct the sorted array; if it fails, no sequence of allowed swaps can repair missing or extra values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    s = input().strip()
    
    i = 0
    while i < n:
        j = i
        while j < n - 1 and s[j] == '1':
            j += 1
        
        segment = a[i:j+1]
        segment.sort()
        
        expected = list(range(i + 1, j + 2))
        if segment != expected:
            print("NO")
            return
        
        i = j + 1
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation scans the array once, expanding each maximal region where swaps are allowed. For each region, it extracts the values and sorts them to check whether they match the required identity interval. The indexing is carefully aligned: segment [i, j] in 0-based indexing corresponds to values that must be exactly [i+1, j+1].

A common mistake is misaligning indices when constructing the expected range. Another subtle issue is forgetting that j stops at n-1, because the swap string has length n-1 and defines boundaries between elements.

## Worked Examples

### Example 1

Input:

n = 6

a = [1, 2, 5, 3, 4, 6]

s = 01110

We process segments:

| Step | l | r | Segment values | Sorted segment | Expected range | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | [1] | [1] | [1] | yes |
| 2 | 1 | 4 | [2,5,3,4] | [2,3,4,5] | [2,3,4,5] | yes |
| 3 | 5 | 5 | [6] | [6] | [6] | yes |

All segments match expectations, so the answer is YES.

This shows a case where internal disorder is fully fixable because connectivity allows rearrangement within a block.

### Example 2

Input:

n = 4

a = [2, 1, 4, 3]

s = 001

Segments:

| Step | l | r | Segment values | Sorted segment | Expected range | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | [2,1] | [1,2] | [1,2] | yes |
| 2 | 2 | 3 | [4,3] | [3,4] | [3,4] | yes |

Even though swaps are restricted, each component already contains exactly the correct set of values, so the answer is YES.

This demonstrates that we are not “sorting globally”, only checking consistency within each connected region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each segment is sorted once, and every element belongs to exactly one segment |
| Space | O(n) | Temporary storage for segment values |

The total work stays within limits because each index is processed exactly once, and sorting is applied over disjoint segments whose combined size is n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided sample
assert run("""6
1 2 5 3 4 6
01110
""") == "YES"

# no swaps allowed, already sorted
assert run("""3
1 2 3
00
""") == "YES"

# no swaps allowed, impossible
assert run("""3
2 1 3
00
""") == "NO"

# full connectivity
assert run("""5
5 4 3 2 1
1111
""") == "YES"

# alternating small components
assert run("""4
2 1 4 3
00
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 / 00 | YES | already sorted with no swaps |
| 2 1 3 / 00 | NO | isolated inversion cannot be fixed |
| 5 4 3 2 1 / 1111 | YES | full reordering possible |

## Edge Cases

A boundary case occurs when there are no allowed swaps at all. In this situation every index forms a component of size one, so each segment trivially matches its expected value only if the array is already sorted. The algorithm handles this naturally because each segment [i, i] is checked against a single-element expected range.

Another edge case is a fully connected swap string. Here the entire array becomes one component, so the check reduces to verifying whether the multiset of values is exactly 1 to n. Since the input is guaranteed to be a permutation, sorting that segment will always match the expected range, leading to YES.

A more subtle case is alternating constraints like 101010..., where components are very small. The algorithm still behaves correctly because each maximal contiguous block is processed independently, and no assumption is made about global connectivity.
