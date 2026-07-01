---
title: "CF 104454N - Just another array problem"
description: "We are given a sequence that starts out already sorted in non-decreasing order. After that, the sequence is not modified by insertions or deletions, but it can be cyclically rotated many times, either to the left or to the right."
date: "2026-06-30T14:30:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104454
codeforces_index: "N"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2021"
rating: 0
weight: 104454
solve_time_s: 71
verified: true
draft: false
---

[CF 104454N - Just another array problem](https://codeforces.com/problemset/problem/104454/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence that starts out already sorted in non-decreasing order. After that, the sequence is not modified by insertions or deletions, but it can be cyclically rotated many times, either to the left or to the right.

Alongside these rotations, we are asked queries of two kinds. One kind performs a rotation by some offset, effectively shifting the array in a circle. The other kind asks whether a value exists in the current rotated array, and if it does, we must report the position of its first occurrence in the current layout, otherwise we output -1.

The important observation hidden in the statement is that rotations do not change the multiset of values or their relative order in the original sorted array. Only the starting point of indexing changes. So the structure is always a sorted array viewed through a moving circular window.

The constraints are large, with up to 200,000 elements and up to 300,000 queries. This immediately rules out any approach that physically rotates the array for each shift, since a single rotation would cost O(N), leading to O(NQ) in the worst case, which is far beyond limits. Even scanning the array for each query would be too slow.

A subtle issue arises with indexing after multiple rotations. If we simulate shifts incorrectly, we can easily lose track of where index 1 currently is, causing wrong answers for duplicate values or boundary wrapping. Another tricky case is repeated values, where the “first occurrence” depends on the current rotated start, not the original ordering.

For example, consider `a = [1,1,2]`. After a right shift by 1, the array becomes `[2,1,1]`. A query for `1` should return index 2, not 3, because the first 1 in the rotated view is at position 2. Any solution that only remembers original positions of values without adjusting for rotation will misreport.

## Approaches

The brute-force idea is straightforward. We maintain the array explicitly. Each shift operation performs an actual cyclic rotation, either using slicing or deque operations. Each query scans the entire array to find the first occurrence of the target value.

This is correct because it literally simulates the process described. However, each rotation costs O(N), and each query costs O(N). With up to 300,000 operations, this leads to about 10^10 operations in the worst case, which is infeasible.

The key observation is that the array is static up to rotation. We never change relative order, only the starting index. This means we do not need to move elements at all. We only need to maintain a logical offset that tells us which index is currently considered position 1. Once we fix this offset, every query becomes a simple index translation problem.

To support fast membership queries, we exploit that the array is sorted, so binary search works on the original array. The only complication is translating a found index in the original array into its rotated position.

We combine two ideas: a running offset for rotation, and binary search for locating values. This reduces each query to O(log N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate array) | O(NQ) | O(N) | Too slow |
| Optimal (offset + binary search) | O(Q log N) | O(N) | Accepted |

## Algorithm Walkthrough

We treat the array as fixed in memory and maintain a variable `shift` that represents how many positions the array has been rotated to the right relative to its original configuration.

1. Initialize `shift = 0`. This means index alignment is unchanged from the original array.
2. For a shift operation `s k`, we normalize it modulo `N` and update the shift. A right shift by `k` increases the offset, while a left shift decreases it. We store everything modulo `N` so the shift stays within range. This step avoids physically rotating the array.
3. For a query `? x`, we first perform a binary search on the original sorted array to find the first occurrence index `i` of value `x`. If not found, we immediately output `-1`.
4. Once we have index `i` in the original array, we convert it to its current position in the rotated array using the shift. The original index `i` moves forward by `shift`, so its new position is `(i + shift) mod N`, converted to 1-based indexing.
5. We output this computed position.

The key idea is that every element keeps its identity and relative order, so the only thing that changes is how we interpret indices.

### Why it works

At any point, the array is equivalent to taking the original sorted array and cutting it at some position `shift`, then swapping the two parts. This is a rigid cyclic transformation, so relative order of all elements is preserved. Therefore, the k-th occurrence of any value in the original array remains the k-th occurrence in the rotated structure, only its index shifts uniformly. The shift variable fully captures this transformation, so mapping indices through it preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())

    shift = 0

    def first_occurrence(x):
        lo, hi = 0, n - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] >= x:
                hi = mid - 1
            else:
                lo = mid + 1
        if lo < n and a[lo] == x:
            return lo
        return -1

    for _ in range(q):
        parts = input().split()
        if parts[0] == 's':
            k = int(parts[1])
            k %= n
            shift = (shift + k) % n
        else:
            x = int(parts[1])
            i = first_occurrence(x)
            if i == -1:
                print(-1)
            else:
                pos = (i + shift) % n + 1
                print(pos)

if __name__ == "__main__":
    main()
```

The solution keeps the array unchanged and only maintains a rotation offset. The binary search finds the first occurrence in the original sorted array, which is valid because sorting is preserved under rotation. The final step adjusts the index using modular arithmetic. The only subtlety is ensuring the modulo operation handles negative shifts correctly, which is why shifts are normalized before being applied.

## Worked Examples

### Sample 1

Initial array: `[1,2,3,4,5,6,7]`

We track `shift` and process each operation.

| Step | Operation | shift | Found index (original) | Computed position | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | ? 9 | 0 | - | - | -1 |
| 2 | s 2 | 2 | - | - | - |
| 3 | ? 4 | 2 | 3 | (3+2)%7+1 = 6 | 6 |
| 4 | s -2 | 0 | - | - | - |
| 5 | ? 3 | 0 | 2 | 2 | 3 |
| 6 | s -5 | 2 | - | - | - |
| 7 | ? 6 | 2 | 5 | (5+2)%7+1 = 1 | 1 |

This trace shows how the same original index maps to different positions purely through the shift variable.

### Sample 2

Initial array: `[1,1,2,2,3,3,4]`

| Step | Operation | shift | First occurrence index | Computed position | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | ? 9 | 0 | - | - | -1 |
| 2 | s 2 | 2 | - | - | - |
| 3 | ? 4 | 2 | 6 | (6+2)%7+1 = 2 | 2 |
| 4 | s -1 | 1 | - | - | - |
| 5 | ? 2 | 1 | 2 | (2+1)%7+1 = 4 | 4 |
| 6 | s -5 | 3 | - | - | - |
| 7 | ? 1 | 3 | 0 | (0+3)%7+1 = 4 | 4 |

This example highlights duplicates. The binary search always returns the first occurrence in the original array, which remains valid after rotation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q log N) | Each query uses O(log N) binary search; shifts are O(1) |
| Space | O(N) | Store the original array only |

The complexity comfortably fits within limits since the total number of operations is at most a few hundred thousand, and each query only performs logarithmic work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import *
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    q = int(sys.stdin.readline())

    shift = 0

    def first_occurrence(x):
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] >= x:
                hi = mid - 1
            else:
                lo = mid + 1
        if lo < n and a[lo] == x:
            return lo
        return -1

    out = []
    for _ in range(q):
        parts = sys.stdin.readline().split()
        if parts[0] == 's':
            k = int(parts[1]) % n
            shift = (shift + k) % n
        else:
            x = int(parts[1])
            i = first_occurrence(x)
            out.append(str(-1 if i == -1 else (i + shift) % n + 1))

    return "\n".join(out) + ("\n" if out else "")

# provided samples
assert run("""7
1 2 3 4 5 6 7
7
? 9
s 2
? 4
s -2
? 3
s -5
? 6
""") == """-1
6
3
1
"""

assert run("""7
1 1 2 2 3 3 4
7
? 9
s 2
? 4
s -1
? 2
s -5
? 1
""") == """-1
2
4
4
"""

# custom cases
assert run("""1
5
3
? 5
s 1
? 5
""") == """1
1
"""

assert run("""3
1 2 3
4
s 1
s 1
s -2
? 2
""") == """2
"""

assert run("""5
1 2 2 2 3
2
? 2
? 4
""") == """2
-1
"""

assert run("""6
1 2 3 4 5 6
1
s 5
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1, 1 | shift correctness at boundary |
| full rotations | 2 | wrap-around consistency |
| missing value | -1 | failed search handling |
| no queries | empty | trivial edge handling |

## Edge Cases

One edge case is when the array has size 1. Any shift operation should have no visible effect, since all rotations are identical. The algorithm handles this because shift is always taken modulo N, and modulo 1 is always 0, so the position mapping remains stable.

Another case is repeated values. Since we always return the first occurrence in the original array, we rely on binary search returning the leftmost match. After rotation, even though duplicates move as a block, their internal ordering is preserved, so the mapped index remains valid.

A final edge case is large negative shifts. These are normalized using modulo arithmetic before being applied. This prevents the shift value from drifting outside the array range and ensures consistent mapping even after many alternating left and right operations.
