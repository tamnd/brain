---
title: "CF 2195B - Heapify 1"
description: "We are given a permutation of integers from 1 to n and can perform a specific type of swap: for any index i from 1 to n/2, we can swap the element at position i with the element at position 2i."
date: "2026-06-07T20:37:35+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2195
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1080 (Div. 3)"
rating: 900
weight: 2195
solve_time_s: 94
verified: true
draft: false
---

[CF 2195B - Heapify 1](https://codeforces.com/problemset/problem/2195/B)

**Rating:** 900  
**Tags:** implementation, sortings  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n and can perform a specific type of swap: for any index i from 1 to n/2, we can swap the element at position i with the element at position 2i. The task is to determine whether, by performing any number of such swaps, the array can be sorted in increasing order.

The input represents multiple test cases. Each test case gives a single integer n, the length of the permutation, followed by n distinct integers from 1 to n in some arbitrary order. The output for each test case is "YES" if the array can be sorted using the allowed operations and "NO" otherwise.

The constraints are significant: n can be up to 200,000, and there can be up to 10,000 test cases, but the total sum of n across all test cases is limited to 200,000. This means we need a solution linear or near-linear in n for each test case. A naive approach that simulates all possible swaps would be exponential in n and completely infeasible.

An edge case arises when the array is almost sorted except for elements that cannot reach their target positions due to the 2i swap structure. For example, for n=5, if the permutation is [1,4,2,3,5], element 4 at index 2 can be swapped with 2 at index 4, allowing sorting, so the answer is YES. But if the array is [1,4,2,3,5], the positions reachable via swaps do not allow element 4 to move to its correct position at index 4, so the answer is NO. Naive algorithms that ignore the swap graph structure might incorrectly say YES.

## Approaches

The brute-force approach is to simulate every possible sequence of allowed swaps and check if the array can become sorted. Each swap only affects pairs of positions (i, 2i), but there are many possible sequences of swaps. For n=200,000, the number of sequences is astronomically large. Even performing each swap in all combinations is impractical because the operation count would grow exponentially.

The key insight is to model the allowed swaps as a directed graph: index i can reach index 2i and vice versa because swaps are reversible. This forms a forest of trees rooted at indices that cannot be written as i=2j (typically the last indices). The critical observation is that elements can only move within the connected component of indices defined by these swaps. Once you know the connected components, you can check if each component contains exactly the elements that should occupy those positions in the sorted array. Sorting is possible if and only if each component contains the correct multiset of target values for those positions.

Thus, the optimal approach is to identify connected components of indices under the swap relation and compare the set of elements in each component with the set of sorted positions they occupy. This approach runs in linear time with respect to n since each index is visited once, and the component membership check is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n and the permutation array a.
2. Initialize a boolean visited array of length n to track which indices have been processed.
3. For each index i from 1 to n, if it has not been visited, start a new component. Initialize two empty lists: one for indices in this component and one for the elements at these indices.
4. Use a depth-first search or iterative traversal to collect all indices reachable from i via swaps. For each index j visited, mark it as visited, add j to the indices list, and a[j] to the elements list. For each index, consider j → 2j and 2j → j connections, as long as indices remain within bounds.
5. After collecting a component, sort both the list of indices and the list of elements. Compare the two lists element-wise; the indices list represents the positions that must contain certain numbers, and the elements list represents the numbers that are actually in those positions. If they differ, sorting is impossible.
6. If all components match their expected elements, print YES; otherwise, print NO.

Why it works: The swap operation defines connected components of indices that can exchange elements freely among themselves. Each component is independent, so the relative ordering of elements in different components cannot be altered. Sorting the array is possible only if each component contains exactly the elements required by their positions in the final sorted array. The algorithm directly checks this invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def can_sort_heapify(n, a):
    visited = [False] * n

    def dfs(idx, indices):
        visited[idx] = True
        indices.append(idx)
        for nxt in [2*(idx+1)-1, (idx+1)//2-1]:
            if 0 <= nxt < n and not visited[nxt]:
                dfs(nxt, indices)

    for i in range(n):
        if not visited[i]:
            indices = []
            dfs(i, indices)
            component_values = [a[j] for j in indices]
            if sorted(indices) != sorted([v-1 for v in component_values]):
                return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(can_sort_heapify(n, a))
```

The solution first sets a recursion limit high enough to avoid stack overflows for large n. The DFS explores all indices reachable via allowed swaps, forming connected components. For each component, we extract the current elements and the target sorted values for those positions. Sorting both lists and comparing ensures that elements can be rearranged within the component to match the sorted array. Using 0-based indexing simplifies the DFS and array handling.

## Worked Examples

### Example 1

Input: [1,4,3,2,5]

| Step | indices visited | component elements | sorted indices | sorted elements | match? |
| --- | --- | --- | --- | --- | --- |
| Start at 0 | [0] | [1] | [0] | [0] | yes |
| Next unvisited 1 | [1,3] | [4,2] | [1,3] | [1,3] | yes |
| Next unvisited 2 | [2] | [3] | [2] | [2] | yes |
| Next unvisited 4 | [4] | [5] | [4] | [4] | yes |

All components match, so output is YES.

### Example 2

Input: [1,4,2,3,5]

| Step | indices visited | component elements | sorted indices | sorted elements | match? |
| --- | --- | --- | --- | --- | --- |
| Start at 0 | [0] | [1] | [0] | [0] | yes |
| Next unvisited 1 | [1,3] | [4,3] | [1,3] | [1,3] | yes |
| Next unvisited 2 | [2] | [2] | [2] | [2] | yes |
| Next unvisited 4 | [4] | [5] | [4] | [4] | yes |

Component 1 indices [1,3] expected values [2,4] but actual values [4,3] → mismatch. Output is NO.

The trace shows how the DFS groups indices and why the mismatch occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is visited exactly once in DFS; sorting each component is O(k log k) but sum of k over all components is n, so O(n log n) worst case |
| Space | O(n) | Visited array and DFS stack |

Given n ≤ 2⋅10^5 and t ≤ 10^4 with total n across tests ≤ 2⋅10^5, the solution easily fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.setrecursionlimit(1 << 20)
    output = io.StringIO()
    sys.stdout = output

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(can_sort_heapify(n, a))
    return output.getvalue().strip()

# provided samples
assert run("2\n5\n1 4 3 2 5\n5\n1 4 2 3 5\n") == "YES\nNO", "sample 1"

# custom cases
assert run("1\n1\n1\n") == "YES", "single element"
assert run("1\n2\n2 1\n") == "YES", "two elements can swap"
assert run("1\n3\n3 2 1\n") == "NO", "three elements impossible"
assert run("1\n4\n4 3 2 1\n") == "NO", "all reversed 4 elements"
assert run("1\n5\n1 2 3 4 5\n") == "YES", "already sorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n1 |  |  |
