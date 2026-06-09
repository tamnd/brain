---
title: "CF 1750A - Indirect Sort"
description: "We are given a small permutation, meaning every number from 1 to n appears exactly once. The task is to determine whether we can transform this array into sorted order using a very specific operation that involves three indices i < j < k."
date: "2026-06-09T15:04:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1750
codeforces_index: "A"
codeforces_contest_name: "CodeTON Round 3 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 800
weight: 1750
solve_time_s: 121
verified: true
draft: false
---

[CF 1750A - Indirect Sort](https://codeforces.com/problemset/problem/1750/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small permutation, meaning every number from 1 to n appears exactly once. The task is to determine whether we can transform this array into sorted order using a very specific operation that involves three indices i < j < k.

Each operation behaves in one of two ways depending on a comparison between the values at positions i and k. If the value at i is larger than the value at k, we are allowed to increase the value at i by adding a[j] to it. Otherwise, we can swap the elements at positions j and k.

The goal is not to simulate a fixed sorting algorithm but to decide whether it is possible, through repeated use of this operation, to eventually reach the sorted permutation.

The constraints are extremely small, with n at most 10, which suggests that a brute-force state search might seem tempting at first glance. However, the branching factor of operations is large because every triple of indices is a potential move, and values can change, not just positions. Even in such a small n, naive BFS over full states becomes messy because values are no longer bounded permutations after the first type of operation.

A key subtle edge case is that the first operation changes values, breaking the permutation structure. For example, starting from a valid permutation, applying the “addition” step can produce values larger than n, which makes state tracking significantly harder if we try to simulate directly.

Another important scenario is when swaps are seemingly available but are actually blocked by the condition on a[i] and a[k]. For example, if the smallest element is not positioned correctly, it may prevent any useful rearrangement even though swaps exist syntactically.

## Approaches

A brute-force approach would treat each array configuration as a state and explore all possible operations. From a given state, we would try every triple i < j < k, generate either a swap or a value change, and continue searching until we either reach the sorted array or exhaust possibilities.

This is correct in principle because it models the rules exactly. However, the number of states explodes immediately. Even ignoring value growth from additions, there are n! permutations, and each state branches into O(n^3) transitions. Once values change, the state space is no longer even bounded by permutations, making the search fundamentally uncontrolled.

The key observation is that the operation has a very strong structural constraint hidden inside it. The swap operation is only enabled when a[i] ≤ a[k]. This single condition determines whether we can reorder elements. If there exists a position that always satisfies this condition against all other values, it becomes a universal enabler for swaps.

This leads to the crucial insight: the value 1 plays a special role. Since all values are positive and distinct, any comparison with 1 will satisfy a[i] ≤ a[k] whenever a[i] = 1. If we can position 1 at the first index, it can act as a permanent facilitator for swaps among all later positions, effectively allowing arbitrary rearrangement of the suffix.

Once this happens, sorting becomes straightforward because we can simulate adjacent swaps anywhere in the array using the triple operation.

Thus the entire problem collapses into checking whether we already have this “swap-enabling anchor” at the start.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | Exponential | Too slow |
| Anchor Observation | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

### Core idea

We check whether the first element of the array is equal to 1.

### Steps

1. Read the array for the current test case.
2. Check the value at position 1 (0-indexed position 0).
3. If it equals 1, output "Yes".
4. Otherwise, output "No".

The reasoning behind this check is that only when 1 is at the first position can it be used as a fixed helper element in every triple operation. Without this, swap operations are restricted by comparisons involving larger values, preventing full rearrangement.

### Why it works

The operation allows swapping j and k only when there exists an i to the left such that a[i] ≤ a[k]. If the first element is 1, choosing i = 1 guarantees this condition always holds for any k, since 1 is the smallest possible value. This means any pair (j, k) can be swapped freely, so the array can be permuted arbitrarily into sorted order.

If 1 is not at the first position, there is no way to make it act as a universal minimum pivot for swaps, and the restriction on i prevents us from freely reordering elements. The array becomes trapped in a structure where full sorting cannot be guaranteed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if a[0] == 1:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and performs a constant-time check per case. The only subtle point is indexing: we directly inspect the first element since that is the only position that matters for determining whether unrestricted swapping is possible.

No simulation of the operation is needed because the decision reduces entirely to the position of the value 1.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
1 3 2
2 1 3
```

| Array | First element | Decision | Output |
| --- | --- | --- | --- |
| [1,2,3] | 1 | swap-capable anchor exists | Yes |
| [1,3,2] | 1 | full rearrangement possible | Yes |
| [2,1,3] | 2 | no universal anchor | No |

When the first element is 1, we can freely swap any pair in the suffix, so even an unsorted permutation like [1,3,2] can be fixed in one move.

### Example 2

Input:

```
4
5 3 4 7 6 2 1
7 6 5 4 3 2 1
1 2 6 7 4 3 5
2 1 3 4 5
```

| Array | First element | Decision | Output |
| --- | --- | --- | --- |
| [5,3,4,7,6,2,1] | 5 | no anchor | No |
| [7,6,5,4,3,2,1] | 7 | no anchor | No |
| [1,2,6,7,4,3,5] | 1 | full swap freedom | Yes |
| [2,1,3,4,5] | 2 | no anchor | No |

This example highlights that even highly sortable-looking permutations cannot be fixed unless the first element is 1. The third case demonstrates how having 1 at the front unlocks complete control over the array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One constant check per test case |
| Space | O(1) | Only storing input array |

The constraints allow up to 5000 test cases, but each one is handled in constant time, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append("Yes" if a[0] == 1 else "No")
    return "\n".join(out)

# provided samples
assert run("""7
3
1 2 3
3
1 3 2
7
5 3 4 7 6 2 1
7
7 6 5 4 3 2 1
5
2 1 4 5 3
5
2 1 3 4 5
7
1 2 6 7 4 3 5
""") == """Yes
Yes
No
No
No
No
Yes"""

# custom cases
assert run("""3
3
2 3 1
3
1 2 3
4
1 4 3 2
""") == """No
Yes
Yes"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| permutation starting with non-1 | No | anchor requirement is necessary |
| already sorted | Yes | identity case |
| 1 followed by disorder | Yes | swap freedom suffices |

## Edge Cases

If the smallest element is not at the first position, even though it exists somewhere in the array, it cannot serve as a global swap enabler. The condition on i requires i < j < k, so the pivot must always be strictly left of any swap operation. Only when 1 starts at index 1 can it consistently act as that pivot for all other pairs.

For example, in `[2,1,3,4,5]`, the value 1 exists but cannot be used as a universal helper because it is not available to the left of all positions. The algorithm correctly outputs "No", matching the fact that no sequence of operations can fully unlock arbitrary reordering.
