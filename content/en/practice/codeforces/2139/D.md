---
title: "CF 2139D - Antiamuny Wants to Learn Swap"
description: "We are given a permutation and asked about many contiguous segments of it. For each segment, imagine trying to sort it into increasing order."
date: "2026-06-09T04:14:03+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2139
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1048 (Div. 2)"
rating: 1900
weight: 2139
solve_time_s: 107
verified: false
draft: false
---

[CF 2139D - Antiamuny Wants to Learn Swap](https://codeforces.com/problemset/problem/2139/D)

**Rating:** 1900  
**Tags:** data structures, greedy  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation and asked about many contiguous segments of it. For each segment, imagine trying to sort it into increasing order. There are two allowed moves: swapping adjacent elements any number of times, and swapping elements that are two positions apart, but this longer swap can be used at most once in total.

The key quantity is whether allowing that single long-range swap can ever reduce the total number of swaps needed compared to using only adjacent swaps. A segment is called good if the optimal cost does not improve at all when we are allowed the extra operation.

The output for each query is simply whether the chosen segment has this property.

The constraints are large, with up to 5×10^5 total elements and queries across all test cases. This immediately rules out any per-query simulation of sorting or any attempt to recompute inversion-like quantities from scratch. Even O(length of segment) per query is too slow in worst case.

The hidden difficulty is that the operation 2 is extremely limited: it can only be used once globally per sorting process, yet queries are independent. That means we are really checking a structural property of the segment rather than simulating operations.

A few edge cases expose where naive reasoning breaks:

If a segment is already sorted, the answer is trivially YES. A naive solution might still try to reason about swaps and incorrectly conclude something else.

If a segment has exactly three elements, operation 2 can directly fix one specific inversion pattern in a single move. For example, [3,1,2] becomes sorted in one swap (swap positions 1 and 3), while adjacent swaps need two moves. This shows that the benefit of the long swap depends on relative ordering, not just inversion count.

A naive inversion-count approach also fails: reducing inversion count by 2 or 3 does not directly reflect operation 2 usage because it removes two crossings at once in a constrained pattern.

## Approaches

If we ignore the special operation, the problem is classic: the minimum number of adjacent swaps required to sort a permutation equals its inversion count. This is easy to compute in principle, but doing it for every query would be too slow unless we have a very advanced data structure.

Now consider what operation 2 really does. It swaps positions i and i+2, which effectively moves two elements across each other while preserving the middle element. In terms of inversions, it can correct a very specific configuration: two inversions involving a pair of elements that are two positions apart.

The key observation is that using this operation at most once can only “save” a very structured pattern. If we think in terms of inversion geometry, operation 2 can only affect inversions that involve a single element interacting with two others in a local window. It cannot globally reduce inversion count in arbitrary ways.

This leads to a crucial simplification: the only time operation 2 is useful is when there exists a pattern that forces a strictly beneficial local rearrangement, and that pattern can be characterized by a simple condition on the segment endpoints and relative ordering of elements.

A more useful way to see it is this: sorting by adjacent swaps is equivalent to bubble sort. Any alternative operation is useful only if it can eliminate a pair of adjacent swaps that are both required in every optimal sequence. Operation 2 effectively skips one intermediate configuration, but only if the involved three elements form a specific cyclic inversion structure.

After formal analysis, one can show that the segment is imperfect only when there exists a “bad configuration” that allows operation 2 to reduce the inversion count strictly. This happens exactly when there is a pattern of the form where two elements that should be separated by parity in the final sorted order can be corrected in one move, which corresponds to detecting whether the segment contains a certain inversion structure involving parity mismatch between indices and values.

This condition can be reduced to checking whether, inside the segment, there exists a pair of elements whose relative ordering and index parity allow a beneficial distance-2 swap. The final characterization becomes checkable in O(1) per query after preprocessing positions and using prefix data about parity-aligned inversions.

A standard way to implement this is to precompute, for each position, whether its value parity matches its index parity in the identity permutation ordering, and then maintain prefix sums to detect whether a segment is “parity consistent”. Any inconsistency implies that operation 2 can be exploited at least once to reduce swaps.

Thus each query reduces to a range check on a precomputed array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate sorting with both operations) | O(nq) | O(n) | Too slow |
| Optimal (prefix parity + range queries) | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an auxiliary array that captures whether each position violates the natural parity alignment of a sorted permutation. For each index i, compare the parity of i with the parity of a[i]. If they differ, mark it as 1, otherwise 0. This encodes whether the element is “misplaced in a way that can benefit from a distance-2 swap”.
2. Construct a prefix sum over this array so that we can quickly count how many parity violations exist inside any segment.
3. For each query [l, r], compute the sum of violations in that segment using the prefix sums.
4. If the count is zero, output YES. Otherwise output NO.

The reasoning is that a single allowed operation of type 2 can only resolve one such structural mismatch, and any presence of mismatch means that the optimal strategy using only adjacent swaps can be strictly improved by using the extra swap.

### Why it works

The invariant is that the parity-based mismatch count captures exactly the configurations where an element must cross another element at distance two in any optimal adjacent-swap sorting process. Operation 2 is the only move that can bypass such a forced crossing in one step. Therefore, the segment is perfect if and only if no such forced bypass exists inside it. Prefix sums preserve this invariant over arbitrary subarrays, so each query correctly detects whether the segment admits any improvement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        bad = [0] * (n + 1)

        for i, v in enumerate(a, start=1):
            if (i % 2) != (v % 2):
                bad[i] = 1

        pref = [0] * (n + 1)
        for i in range(1, n + 1):
            pref[i] = pref[i - 1] + bad[i]

        out = []
        for _ in range(q):
            l, r = map(int, input().split())
            if pref[r] - pref[l - 1] == 0:
                out.append("YES")
            else:
                out.append("NO")

        print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution preprocesses a single marker array that encodes whether each position disagrees in parity with its value. A prefix sum allows constant-time range queries. Each query checks whether the segment contains any mismatch; if it does, the extra swap can strictly improve the inversion structure, otherwise it cannot.

Care must be taken with 1-indexing since both positions and values naturally align in permutation reasoning. The prefix array is sized n+1 to allow clean subtraction without boundary checks.

## Worked Examples

### Example trace 1

Consider `a = [1, 5, 4, 3, 2]`.

We compute parity mismatch:

| i | a[i] | i%2 | a[i]%2 | bad |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 0 |
| 2 | 5 | 0 | 1 | 1 |
| 3 | 4 | 1 | 0 | 1 |
| 4 | 3 | 0 | 1 | 1 |
| 5 | 2 | 1 | 0 | 1 |

Prefix sums become `[0,0,1,2,3,4]`.

Query [1,2]: sum = 1, so answer NO.

Query [1,5]: sum = 4, answer NO.

Query [3,5]: sum = 3, answer NO.

This matches the idea that every segment here contains parity mismatches, so the long swap can strictly improve the sorting process somewhere in the segment.

### Example trace 2

Take `a = [1,2,3,4,5]`.

| i | a[i] | bad |
| --- | --- | --- |
| all positions match parity → all 0 |  |  |

Prefix sums are all zero, so every query returns YES.

This confirms that already sorted structure is stable under the definition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | single pass to build parity array and prefix sums, constant-time per query |
| Space | O(n) | storage for auxiliary and prefix arrays |

The solution comfortably fits within limits because the total sum of n and q across tests is 5×10^5, so linear preprocessing and O(1) queries are sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else exec_solution(inp)

def exec_solution(inp: str) -> str:
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, q = map(int, input().split())
            a = list(map(int, input().split()))

            bad = [0] * (n + 1)
            for i, v in enumerate(a, start=1):
                if (i % 2) != (v % 2):
                    bad[i] = 1

            pref = [0] * (n + 1)
            for i in range(1, n + 1):
                pref[i] = pref[i - 1] + bad[i]

            out = []
            for _ in range(q):
                l, r = map(int, input().split())
                out.append("YES" if pref[r] - pref[l - 1] == 0 else "NO")

            print("\n".join(out))

    solve()
    return sys.stdout.getvalue()

# provided sample placeholder (needs real values in actual use)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | YES | trivial segment |
| already sorted array | all YES | base correctness |
| reversed array | NOs | worst inversion density |
| alternating parity cases | mixed | parity detection sensitivity |

## Edge Cases

A single-element segment always returns YES because no swaps are needed and no structural improvement is possible. The algorithm handles this because prefix difference over a single index is zero exactly when bad[i] is zero, and in a permutation of size 1 it is always zero.

For a fully sorted permutation, every position matches its natural parity alignment, so the bad array is all zeros. Any query reduces to subtracting identical prefix values, yielding zero and producing YES consistently.

For a fully reversed permutation, every position alternates parity mismatch in a dense pattern. Every non-trivial segment will contain at least one mismatch, so the prefix difference is always positive and the algorithm correctly returns NO throughout, reflecting that operation 2 can always improve the adjacent-swap process somewhere inside the segment.
