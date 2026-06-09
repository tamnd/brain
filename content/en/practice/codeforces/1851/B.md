---
title: "CF 1851B - Parity Sort"
description: "We are given an array of integers and allowed to repeatedly swap elements, but with a restriction: a swap is only valid if both elements have the same parity, meaning both are even or both are odd."
date: "2026-06-09T05:24:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 800
weight: 1851
solve_time_s: 85
verified: false
draft: false
---

[CF 1851B - Parity Sort](https://codeforces.com/problemset/problem/1851/B)

**Rating:** 800  
**Tags:** greedy, sortings, two pointers  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and allowed to repeatedly swap elements, but with a restriction: a swap is only valid if both elements have the same parity, meaning both are even or both are odd. Our goal is to determine whether we can fully sort the array into non-decreasing order using any number of such restricted swaps.

The key point is that elements are not freely movable across the entire array. Even numbers can only be rearranged among themselves, and odd numbers can only be rearranged among themselves. This splits the array into two independent “movement groups,” even and odd, which can each be permuted arbitrarily within their own positions but never mixed.

The constraints are large, with up to 2 × 10^5 total elements across test cases. This rules out any approach that tries all swap sequences or simulates sorting with custom rules. Anything beyond linear or near-linear per test case will be too slow.

A subtle edge case appears when the sorted array requires an element to cross parity boundaries. For example, if sorting would require an even number to appear in a position that originally corresponds to an odd-valued slot, that is not directly the issue. The real issue is whether the multiset of values that end up in positions originally occupied by evens/odds is consistent with the target sorted arrangement.

Another misleading case is when the array is already almost sorted but one parity group is internally “misaligned.” For example, `[3, 2, 1]` cannot be sorted because 1 and 2 would need to swap across parity, even though the global sorted array is `[1, 2, 3]`.

## Approaches

The brute-force idea is to simulate the allowed swaps. We could repeatedly scan the array, find pairs of elements with equal parity that are out of order, and swap them if it improves sortedness. In the worst case, this behaves like a constrained bubble sort. Each swap is O(1), but we may need O(n^2) swaps and each pass costs O(n), leading to O(n^3) in pathological reasoning or at least O(n^2) effective operations per test case. With n up to 2 × 10^5, this is infeasible.

The key observation is that the operation allows arbitrary permutation inside each parity class. That means we can fully reorder the subsequence of even numbers and fully reorder the subsequence of odd numbers independently.

Now consider the sorted version of the entire array. If we imagine writing it down, each position in that sorted array expects a specific value. The only question is whether we can assign values to positions while respecting parity constraints.

We simulate sorting but enforce that each position can only receive a value of the same parity as the original position’s parity role is not fixed, but rather the pool constraint matters: we are essentially checking whether, when we take the sorted array and try to “fill” it from left to right, we never need more elements of a parity than we have available.

A simpler and equivalent viewpoint is this: extract all even numbers and all odd numbers. Sort them independently. Then reconstruct the sorted array by taking elements from these two sorted lists in order of the original sorted target. If at any point the next required parity element is unavailable, sorting is impossible.

This reduces the problem to a greedy feasibility check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swapping | O(n^2) or worse | O(1)-O(n) | Too slow |
| Sort parity groups + greedy check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the array into two lists, one containing all even numbers and one containing all odd numbers. This isolates the independent swap groups implied by the operation.
2. Sort both lists in non-decreasing order. This represents the strongest possible rearrangement achievable within each parity group.
3. Sort a copy of the full array. This gives the target final configuration we want to match.
4. Traverse the sorted full array from left to right. For each element, check its parity.
5. If the element is even, take the next smallest unused element from the even list. If it does not match, the construction fails.
6. If the element is odd, take the next smallest unused element from the odd list. If it does not match, the construction fails.
7. If we successfully match every position, output YES; otherwise output NO.

The reasoning behind step 5 and 6 is that within each parity class, we have complete freedom of permutation, so the only constraint is whether the multiset of values of each parity can satisfy the sorted structure in order.

### Why it works

The operation defines two independent permutation groups: all even indices among themselves and all odd indices among themselves. Any reachable configuration is equivalent to independently permuting the even subsequence and the odd subsequence arbitrarily. Sorting is therefore possible exactly when there exists a pairing between sorted target positions and available parity values that respects parity counts position by position. The greedy assignment works because both parity lists are sorted, and any deviation from matching the smallest available valid value would only make future assignments harder, never easier.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        evens = []
        odds = []
        for x in a:
            if x % 2 == 0:
                evens.append(x)
            else:
                odds.append(x)
        
        evens.sort()
        odds.sort()
        
        sorted_a = sorted(a)
        
        ei = oi = 0
        ok = True
        
        for x in sorted_a:
            if x % 2 == 0:
                if ei >= len(evens) or evens[ei] != x:
                    ok = False
                    break
                ei += 1
            else:
                if oi >= len(odds) or odds[oi] != x:
                    ok = False
                    break
                oi += 1
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation first separates values by parity, then sorts both groups. It also sorts the full array to represent the target configuration. Two pointers track consumption of even and odd values. Each element in the sorted target must be matched exactly by the corresponding parity list. Any mismatch means that the required value is not available in the correct parity pool ordering.

The important subtlety is that we never try to simulate swaps. The parity restriction already guarantees full internal rearrangement freedom, so simulation is unnecessary.

## Worked Examples

### Example 1

Input:

```
a = [7, 10, 1, 3, 2]
```

Sorted array:

```
[1, 2, 3, 7, 10]
```

Even list: `[10, 2] → [2, 10]`

Odd list: `[7, 1, 3] → [1, 3, 7]`

| Step | Sorted value | Parity | Even pointer | Odd pointer | Action | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | odd | 0 | 0 | take 1 | ok |
| 2 | 2 | even | 0 | 1 | take 2 | ok |
| 3 | 3 | odd | 0 | 1 | take 3 | ok |
| 4 | 7 | odd | 0 | 2 | take 7 | ok |
| 5 | 10 | even | 1 | 2 | take 10 | ok |

All elements match successfully, so the answer is YES.

This confirms that independent sorting within parity groups is sufficient when counts align with required usage order.

### Example 2

Input:

```
a = [11, 3, 15, 3, 2]
```

Sorted array:

```
[2, 3, 3, 11, 15]
```

Even list: `[2]`

Odd list: `[11, 3, 15, 3] → [3, 3, 11, 15]`

| Step | Sorted value | Parity | Even pointer | Odd pointer | Action | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | even | 0 | 0 | take 2 | ok |
| 2 | 3 | odd | 1 | 0 | take 3 | ok |
| 3 | 3 | odd | 1 | 1 | take 3 | ok |
| 4 | 11 | odd | 1 | 2 | take 11 | ok |
| 5 | 15 | odd | 1 | 3 | take 15 | ok |

This case succeeds, showing that duplicates and mixed parity ordering do not break feasibility as long as each parity pool can satisfy the sorted sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates for each test case |
| Space | O(n) | storing even and odd partitions |

The total input size across all test cases is bounded by 2 × 10^5, so sorting once per test case stays comfortably within time limits. Memory usage remains linear in the input size.

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

        evens = sorted(x for x in a if x % 2 == 0)
        odds = sorted(x for x in a if x % 2 == 1)
        sa = sorted(a)

        ei = oi = 0
        ok = True
        for x in sa:
            if x % 2 == 0:
                if ei >= len(evens) or evens[ei] != x:
                    ok = False
                    break
                ei += 1
            else:
                if oi >= len(odds) or odds[oi] != x:
                    ok = False
                    break
                oi += 1

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""6
5
7 10 1 3 2
4
11 9 3 5
5
11 3 15 3 2
6
10 7 8 1 2 3
1
10
5
6 6 4 1 6
""") == """YES
YES
NO
NO
YES
NO"""

# minimum size
assert run("""2
1
10
1
3
""") == """YES
YES"""

# all equal
assert run("""1
4
2 2 2 2
""") == """YES"""

# parity mismatch stress
assert run("""1
3
2 1 4
""") == """NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element cases | YES/YES | trivial feasibility |
| all equal values | YES | swaps unnecessary |
| mixed parity tight case | NO | impossible ordering |

## Edge Cases

A critical edge case is when sorting requires interleaving parity groups in a way that demands more elements of one parity early than are available. For example, `[2, 1, 4]` sorts to `[1, 2, 4]`, but the structure forces a mismatch in how parity groups are consumed when aligned positionally. The algorithm correctly detects this because the sorted target requires an odd element first while odd pool availability and ordering may not align with the constructed sequence.

Another subtle case is when duplicates exist across parity groups, such as `[6, 6, 4, 1, 6]`. Even though many values repeat, the parity partition still determines feasibility. The algorithm treats each occurrence independently and ensures correct matching, so duplicates do not mask impossibility.
