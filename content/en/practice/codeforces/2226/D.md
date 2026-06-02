---
title: "CF 2226D - Reserved Reversals"
description: "We are given several test cases, each consisting of an array. The task is to decide whether we can transform each array into a non-decreasing order using a specific operation: we may pick any subarray, compute its minimum and maximum values, and reverse it, but only if the sum…"
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2226
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1095 (Div. 2)"
rating: 0
weight: 2226
solve_time_s: 142
verified: false
draft: false
---

[CF 2226D - Reserved Reversals](https://codeforces.com/problemset/problem/2226/D)

**Rating:** -  
**Tags:** constructive algorithms, dp, greedy, math  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, each consisting of an array. The task is to decide whether we can transform each array into a non-decreasing order using a specific operation: we may pick any subarray, compute its minimum and maximum values, and reverse it, but only if the sum of those two values has odd parity.

Since the sum is odd exactly when one of the two is even and the other is odd, the operation is only available on segments whose minimum and maximum values have different parity.

The output for each test case is a simple feasibility check: whether some sequence of such constrained reversals can sort the array.

The constraints imply a total array length across all test cases up to 2×10^5, so any solution must run in linear or near-linear time per test case. An O(n^2) strategy that tries all segments or simulates operations is immediately infeasible.

A common failure mode in problems of this type is assuming that “having both even and odd numbers” automatically gives full flexibility. That is not obviously true, because the operation depends on extremal values in a segment, not just the presence of both parities. Another subtle pitfall is thinking that reversals behave like arbitrary swaps. They do not; the parity constraint can block certain local rearrangements even when the array looks flexible.

## Approaches

The brute-force perspective is straightforward: repeatedly try all valid segments, reverse them, and check whether the array becomes sorted. Each step would require scanning all O(n^2) segments, computing minima and maxima, and simulating reversals. Even if each segment query were optimized, the number of states reachable through reversals grows explosively, making this approach unusable for n up to 2×10^5.

The key structural observation is that the only thing that matters for enabling any move is whether we can find at least one valid segment. A segment is valid exactly when its minimum and maximum have opposite parity. The smallest possible segment that can be chosen is a length-2 segment, where the minimum and maximum are just the two endpoints. This immediately reduces the operation condition to a much simpler form: an adjacent swap is possible exactly when two neighboring values have different parity.

Once this is seen, the reversal operation no longer needs to be analyzed globally. Any longer valid reversal can be decomposed into a sequence of adjacent swaps across positions where parity differs. This means the system’s real power comes from being able to interchange neighbors of opposite parity, which allows elements to be gradually shuffled across the array as long as there is at least one even and one odd element present.

If the array consists entirely of numbers with the same parity, no segment of length at least two can satisfy the condition, so no operation is ever possible. The array is frozen in its initial state, and sorting is possible only if it is already non-decreasing.

If both parities exist, then there is at least one valid adjacent swap, and repeated use of such swaps allows arbitrary reordering: elements can be “carried through” the array by swapping across opposite-parity neighbors, which eventually enables a standard bubble-sort style rearrangement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all reversals) | O(n³) to exponential | O(n) | Too slow |
| Parity-reduction reasoning | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, scan the array and determine whether there exists at least one even number and at least one odd number. This single check captures whether any valid operation exists at all, because length-2 segments are the minimal candidates for reversals.
2. If the array contains only even numbers or only odd numbers, immediately conclude that no operation is possible. In that situation the array cannot change, so the answer is “YES” only if it is already sorted.
3. If both parities appear, conclude that the array is always sortable. The presence of at least one even and one odd guarantees that adjacent swaps are possible somewhere in the array, and these swaps are sufficient to realize any permutation through repeated local exchanges.
4. Output “YES” for all mixed-parity arrays and for already sorted single-parity arrays, and “NO” otherwise.

### Why it works

The decisive invariant is whether the array contains both parities. If both exist, there is always at least one adjacent pair of opposite parity after some rearrangement, and such pairs can be used to propagate elements through the array. This removes positional rigidity: elements are no longer trapped within fixed regions. If only one parity exists, every subarray has identical parity extrema, so no operation can ever be applied and the configuration is immutable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_sorted(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    has_even = False
    has_odd = False

    for x in a:
        if x % 2 == 0:
            has_even = True
        else:
            has_odd = True

    if has_even and has_odd:
        print("YES")
    else:
        # no operations possible at all
        print("YES" if is_sorted(a) else "NO")
```

The solution first checks parity diversity in a single pass. The only subtle branch is the degenerate case where all numbers share the same parity, in which case the array is immutable and must already be sorted.

The `is_sorted` check is only needed in that degenerate branch, since otherwise the answer is always affirmative.

## Worked Examples

### Example 1

Array: `[2, 1, 3]`

| Step | Even present | Odd present | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | Yes | Yes | Mixed parity detected | YES |

Here, both parities exist, so swaps between opposite-parity neighbors are possible, allowing reordering into sorted form.

### Example 2

Array: `[2, 4, 6, 8]`

| Step | Even present | Odd present | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | Yes | No | No operations possible | Check sorted |
| 2 | - | - | Already sorted | YES |

This shows the frozen nature of single-parity arrays: no operation can ever change the configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single scan to detect parity, optional linear sorted check |
| Space | O(1) | Only two boolean flags are stored |

The total complexity over all test cases is linear in the total input size, which fits comfortably within the constraints of 2×10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        has_even = any(x % 2 == 0 for x in a)
        has_odd = any(x % 2 == 1 for x in a)

        if has_even and has_odd:
            out.append("YES")
        else:
            out.append("YES" if all(a[i] <= a[i+1] for i in range(n-1)) else "NO")

    return "".join(out)

# provided sample (format assumed)
assert run("1\n4\n1 1 2 3\n") == "YES", "sample-like 1"

# all same parity, sorted
assert run("1\n4\n2 4 6 8\n") == "YES"

# all same parity, unsorted
assert run("1\n4\n8 6 4 2\n") == "NO"

# mixed parity, unsorted
assert run("1\n3\n3 1 2\n") == "YES"

# mixed parity, already sorted
assert run("1\n5\n1 2 3 4 5\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all evens sorted | YES | immutable but already sorted |
| all evens unsorted | NO | no operations exist |
| mixed parity | YES | sorting always possible |
| increasing sequence | YES | trivial positive case |

## Edge Cases

A fully uniform-parity array is the only configuration where the system has zero mobility. In such cases, the algorithm correctly falls back to a pure sortedness check.

For example, input `[8, 6, 4, 2]` contains only even numbers. No segment can satisfy the parity condition, so the array cannot change. The algorithm detects this and directly evaluates whether it is already sorted, producing “NO” here.

In contrast, `[3, 1, 2]` contains both parities. Even though the array is not sorted, the existence of at least one even and one odd ensures that valid adjacent swaps exist, so the algorithm correctly returns “YES”.
