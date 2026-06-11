---
title: "CF 1174B - Ehab Is an Odd Person"
description: "We are given a sequence of numbers, and we are allowed to reorder it, but with a restriction on how swaps work. A swap is only legal if we pick two positions whose values have opposite parity, meaning one is odd and the other is even."
date: "2026-06-12T01:51:31+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1174
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 563 (Div. 2)"
rating: 1200
weight: 1174
solve_time_s: 93
verified: true
draft: false
---

[CF 1174B - Ehab Is an Odd Person](https://codeforces.com/problemset/problem/1174/B)

**Rating:** 1200  
**Tags:** sortings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers, and we are allowed to reorder it, but with a restriction on how swaps work. A swap is only legal if we pick two positions whose values have opposite parity, meaning one is odd and the other is even. If both are even or both are odd, we cannot swap them directly.

The task is to determine the lexicographically smallest array reachable using any number of such allowed swaps. Lexicographic order means we compare arrays from left to right and prefer the first position where they differ.

The key implication of the operation is that parity groups behave differently: elements can move freely only across parity boundaries, not within the same parity group. This immediately suggests that full arbitrary permutation is not possible, only constrained rearrangement.

The constraint of n up to 100,000 implies we need at least O(n log n) or O(n) solution. Any approach involving repeated simulation of swaps or BFS-style exploration of configurations is infeasible because the state space is exponential in n.

A subtle but important edge case arises when all elements have the same parity. If all numbers are even or all are odd, then no valid swap exists because every pair sums to an even number. In this case, the array is already fixed and cannot be changed.

Another edge case is when there is a mixture of parities but a naive greedy attempt tries to sort the entire array. For example, input `[3, 2, 1]` might tempt sorting to `[1, 2, 3]`, but feasibility depends on parity interactions, not pure ordering.

## Approaches

A brute-force approach would simulate all valid swaps and try to reach all reachable permutations, then pick the smallest lexicographically. From a state perspective, each configuration has up to O(n²) possible swaps, and there are n! permutations in total, making this completely infeasible.

The crucial observation is that a swap is allowed exactly when the two elements have different parity. This means any odd element can swap with any even element, and vice versa. Over repeated swaps, this implies that all odds can effectively permute with all evens through intermediaries, but elements of the same parity never directly constrain each other’s ordering except through global mixing.

We can reinterpret the process: we are allowed to arbitrarily reorder the multiset of all numbers, except that parity interactions ensure that the relative ordering of parity groups in the final arrangement is constrained only by how elements are interleaved.

The key simplification is that we can treat all elements as belonging to two pools: odds and evens. Within each pool, relative ordering is completely free because we can use elements of the opposite parity as intermediaries to effectively simulate swaps between same-parity elements. This is a standard transitivity argument: odd-even swaps allow us to "bubble" elements through the other group.

Thus both odd and even groups can be independently sorted, and then merged greedily by placing the smallest available element at each position, since we can always choose from either group without violating constraints.

However, the true constraint is simpler: because any odd can swap with any even, the multiset is fully permutable. This means the only restriction is that we cannot distinguish parity classes structurally, so the optimal arrangement is simply the globally sorted array.

A naive misconception would be to think parity groups are locked internally, but in fact the swap graph is connected as long as both parities exist.

So the correct logic splits into cases:

If both odd and even exist, we can achieve any permutation, so we sort the whole array.

If only one parity exists, no swaps are possible, so we output the original array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swaps | O(n!) | O(n!) | Too slow |
| Parity Simulation | O(n²) | O(n) | Too slow |
| Sorting with parity check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the array and count how many elements are odd and how many are even. This determines whether any swap is possible at all, since swaps require opposite parity values.
2. If either the odd count or even count is zero, return the array unchanged. No valid swap exists, so no rearrangement is possible.
3. Otherwise, sort the entire array in non-decreasing order. The justification is that the swap graph is connected when both parities exist, meaning any permutation can be constructed.
4. Output the sorted array as the lexicographically smallest arrangement.

### Why it works

The allowed operation defines a graph on array positions where edges connect elements of different parity. When both parities are present, this graph is connected through alternating parity swaps, allowing any element to be moved to any position via intermediate swaps. This implies full permutation reachability. Since all permutations are reachable, the lexicographically smallest reachable arrangement is simply the globally sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    odd = sum(x % 2 for x in a)
    even = n - odd
    
    if odd == 0 or even == 0:
        print(*a)
    else:
        a.sort()
        print(*a)

if __name__ == "__main__":
    main()
```

The code first reads the array and counts parity distribution. That check is crucial because it determines whether swaps can actually change the configuration. If no cross-parity pair exists, sorting would be invalid since it assumes mobility that does not exist.

When both parities exist, we sort the entire array. This relies on the fact that the swap operation effectively makes the permutation group fully reachable.

A subtle point is that we do not need to explicitly simulate swaps or construct intermediate states. The connectivity argument guarantees existence of a sequence of valid swaps transforming any permutation into any other.

## Worked Examples

### Example 1

Input:

```
3
4 1 7
```

Since there are both even (4) and odd (1, 7), sorting is allowed.

| Step | Array state | Odd count | Even count |
| --- | --- | --- | --- |
| Initial | [4, 1, 7] | 2 | 1 |
| Sort | [1, 4, 7] | 2 | 1 |

This confirms that with mixed parity, the smallest lexicographic arrangement is achieved by sorting.

### Example 2

Input:

```
4
2 6 8 10
```

All numbers are even, so no swap is allowed.

| Step | Array state | Action |
| --- | --- | --- |
| Initial | [2, 6, 8, 10] | No swaps possible |

Output remains unchanged.

This demonstrates the frozen-state behavior when the swap condition is never satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates when both parities exist |
| Space | O(n) | Storage for the array |

The constraints allow up to 100,000 elements, so an O(n log n) solution is comfortably within limits. The parity check is O(n) and negligible compared to sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    odd = sum(x % 2 for x in a)
    if odd == 0 or odd == n:
        return " ".join(map(str, a))
    a.sort()
    return " ".join(map(str, a))

# provided sample
assert run("3\n4 1 7\n") == "1 4 7", "sample 1"

# all even
assert run("4\n2 6 8 10\n") == "2 6 8 10", "all even"

# all odd
assert run("3\n5 1 7\n") == "5 1 7", "all odd"

# already sorted
assert run("5\n1 2 3 4 5\n") == "1 2 3 4 5", "already sorted"

# reverse order
assert run("5\n5 4 3 2 1\n") == "1 2 3 4 5", "mixed parity sortable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all even | unchanged | no swaps possible |
| all odd | unchanged | no swaps possible |
| already sorted | same array | identity case |
| reverse order | sorted array | full reordering |

## Edge Cases

When all elements share the same parity, the algorithm correctly detects that no operation can ever be applied. For input `[2, 6, 8]`, the odd count is zero, so we directly return `[2, 6, 8]`. Any attempt to sort here would be invalid because there is no legal swap to justify changing positions.

When both parities exist, even if elements are heavily interleaved, such as `[100, 1, 99, 2]`, the algorithm sorts to `[1, 2, 99, 100]`. The connectivity argument ensures that every required transposition can be decomposed into valid odd-even swaps, so the sorted result is always reachable.
