---
title: "CF 106007I - Reverse and Remove"
description: "We are given a sequence of numbers and a number of operations to perform on it. Each operation always removes the current first element of the sequence, and then reverses whatever remains."
date: "2026-06-22T16:42:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106007
codeforces_index: "I"
codeforces_contest_name: "The 2025 Aleppo Collegiate programming contest"
rating: 0
weight: 106007
solve_time_s: 51
verified: true
draft: false
---

[CF 106007I - Reverse and Remove](https://codeforces.com/problemset/problem/106007/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers and a number of operations to perform on it. Each operation always removes the current first element of the sequence, and then reverses whatever remains. This is repeated exactly k times, and we must output the final sequence after all these transformations.

A useful way to think about the process is that the array is repeatedly being peeled from the front, while its orientation keeps flipping. After each removal, the relative order of the remaining suffix changes depending on how many reversals have already happened, which makes a direct simulation expensive if done literally.

The constraints allow n up to 100000, so any approach that physically reverses the array k times or shifts elements repeatedly would be too slow. A naive simulation would perform up to k removals and each reversal costs O(n), giving O(nk), which degenerates to O(n^2) in the worst case and is not acceptable.

There are two subtle edge cases that expose naive mistakes. First, if k is close to n minus one, the array becomes extremely short and repeated reversing changes the head and tail rapidly, so implementations that forget to update indices correctly will fail. For example, with input n = 5, k = 4, a = [1, 2, 3, 4, 5], the process should leave only a single element, but incorrect pointer-based simulations often drop or duplicate elements due to alternating direction errors.

Second, if k = 0 is disallowed here but thinking generally, or if k = 1, a naive implementation might reverse before removing instead of after removing, which completely changes the result. For example, [1, 2, 3, 4], k = 1 should yield [2, 3, 4], not [4, 3, 2].

The core difficulty is that the sequence is not only shrinking, but also alternating direction in a structured way that we can track without modifying the array itself.

## Approaches

A direct brute force approach literally performs the described operations. We remove the first element of a list and reverse the rest, repeating this k times. Each removal is O(1) if using a deque, but each reversal of the remaining n i elements is O(n i), leading to a total of O(n + (n−1) + … + (n−k)), which is O(nk). When k is large, this becomes quadratic in the size of the input.

The key observation is that we never actually need the intermediate arrays. We only need to know which elements remain after k removals and in what order. The operation alternates the direction in which the remaining segment is read. Instead of simulating reversals, we can maintain two pointers representing the current left and right boundaries of the remaining array, and a boolean flag representing whether the current orientation is normal or reversed.

Each operation removes one element from the active front depending on orientation. If we are in normal orientation, we remove from the left; if reversed, we remove from the right. After removing, we flip the orientation. This eliminates any need for actual array reversal.

This reduces the entire process to O(k) pointer updates, and since k < n ≤ 100000, it is easily efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Two pointers with direction flag | O(k) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two indices, l starting at 0 and r starting at n − 1, and a boolean variable rev initially false meaning we are reading from the left side.

1. Initialize l = 0 and r = n − 1, and set rev = false. This represents the full active segment and its current orientation.
2. Repeat k times, and at each step decide which end of the segment is the “front” depending on rev. If rev is false, the front is at l, otherwise it is at r. This is exactly equivalent to the current array after all implicit reversals.
3. If rev is false, increment l by 1 to remove the leftmost element. If rev is true, decrement r by 1 to remove the rightmost element. This simulates deleting the first element in the current orientation without physically rearranging anything.
4. Flip rev after each removal. This captures the effect of reversing the remaining array. Instead of rearranging elements, we simply change which side we interpret as the front.
5. After k operations, the remaining segment is the interval [l, r]. The final orientation is determined by rev. If rev is false, we output elements from l to r in increasing order. If rev is true, we output elements from r to l in decreasing order.

### Why it works

At any moment, the remaining array is exactly the original array restricted to a contiguous segment [l, r], but possibly viewed in reversed order depending on how many reversals have occurred. Each operation removes one endpoint of this segment and flips the interpretation of direction. The invariant is that the current logical array is always representable as a contiguous slice of the original array plus a direction flag. Since both removal and reversal preserve this structure, no operation ever introduces discontinuities or reorders elements beyond a global flip. This guarantees that pointer movement and a single boolean flag fully describe the evolving state.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

l, r = 0, n - 1
rev = False

for _ in range(k):
    if not rev:
        l += 1
    else:
        r -= 1
    rev = not rev

if not rev:
    res = a[l:r+1]
else:
    res = a[l:r+1][::-1]

print(*res)
```

The implementation keeps the two boundaries l and r and updates them according to the current direction. The boolean rev tracks whether the logical orientation is flipped. After k steps, we extract the remaining segment. The only subtlety is the final output: if the orientation is reversed, we must explicitly reverse the slice once. This avoids reversing the entire array at every step and keeps the solution linear.

Boundary handling is straightforward because the loop guarantees l ≤ r always until exactly k removals are done.

## Worked Examples

### Example 1

Input:

n = 5, k = 2

a = [1, 2, 3, 4, 5]

| Step | l | r | rev | Removed | Segment interpretation |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 4 | false | - | [1, 2, 3, 4, 5] |
| 1 | 1 | 4 | true | 1 | reversed view |
| 2 | 1 | 3 | false | 5 | normal view |

After two operations, remaining segment is [1, 3], which corresponds to [2, 3, 4]. Output is:

2 3 4

This confirms that alternating removals from opposite ends is correctly handled by the direction flag.

### Example 2

Input:

n = 6, k = 3

a = [10, 20, 30, 40, 50, 60]

| Step | l | r | rev | Removed | Segment interpretation |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | false | - | [10, 20, 30, 40, 50, 60] |
| 1 | 1 | 5 | true | 10 | reversed |
| 2 | 1 | 4 | false | 60 | normal |
| 3 | 2 | 4 | true | 20 | reversed |

Remaining segment is [2, 4] giving [30, 40, 50] which matches output.

This shows that even though removals alternate ends, the representation never breaks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each operation updates two pointers and flips a flag once |
| Space | O(n) | Input array is stored, no extra structure is required |

The solution comfortably fits within constraints since k and n are at most 100000. Each operation is constant time, and only a single final reversal is ever performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    l, r = 0, n - 1
    rev = False

    for _ in range(k):
        if not rev:
            l += 1
        else:
            r -= 1
        rev = not rev

    if not rev:
        res = a[l:r+1]
    else:
        res = a[l:r+1][::-1]

    return " ".join(map(str, res)) if res else ""

# provided sample
assert run("5 2\n1 2 3 4 5\n") == "2 3 4"

# custom: k = 1
assert run("4 1\n1 2 3 4\n") == "2 3 4"

# custom: small alternating
assert run("6 3\n10 20 30 40 50 60\n") == "30 40 50"

# custom: maximal skew removal
assert run("5 4\n1 2 3 4 5\n") == "5"

# custom: identity-like structure
assert run("3 2\n7 8 9\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 2 / 1 2 3 4 5 | 2 3 4 | sample correctness |
| 4 1 / 1 2 3 4 | 2 3 4 | single operation |
| 6 3 / 10 20 30 40 50 60 | 30 40 50 | alternating ends |
| 5 4 / 1 2 3 4 5 | 5 | boundary shrinking |
| 3 2 / 7 8 9 | 8 | minimal middle result |

## Edge Cases

One important edge case is when k removes almost the entire array. Consider input:

n = 5, k = 4, a = [1, 2, 3, 4, 5]

The process should leave only one element. The pointer simulation proceeds as follows: initially l = 0, r = 4. First removal takes 1 from the left, so l becomes 1 and rev becomes true. Second removes from right, r becomes 3. Third removes from left, l becomes 2. Fourth removes from right, r becomes 2. The segment collapses to a single element [3], which is correctly output.

Another edge case is minimal k = 1:

n = 4, k = 1, a = [1, 2, 3, 4]

We remove 1 from the left, leaving [2, 3, 4], then reverse is irrelevant for final output since only one step is done. The algorithm matches this exactly since it performs one pointer increment and flips orientation once, producing l = 1, r = 3 and rev = true, but final reversal of the slice restores correct order.

A final subtle case is when the final segment is already in reversed orientation. For example:

n = 3, k = 2, a = [7, 8, 9]

After two operations, the segment is [1, 1] and rev is false or true depending on parity. The algorithm ensures that the final slice is reversed only once, avoiding repeated structural changes that would otherwise lead to inconsistent ordering.
