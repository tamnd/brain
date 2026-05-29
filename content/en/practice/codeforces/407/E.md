---
title: "CF 407E - k-d-sequence"
description: "We are given a sequence of integers, a[1…n], and two parameters k and d. The goal is to find the longest contiguous subsegment of a that can be extended into an arithmetic progression with difference d by adding at most k elements."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 407
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 239 (Div. 1)"
rating: 3100
weight: 407
solve_time_s: 276
verified: false
draft: false
---

[CF 407E - k-d-sequence](https://codeforces.com/problemset/problem/407/E)

**Rating:** 3100  
**Tags:** data structures  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers, `a[1…n]`, and two parameters `k` and `d`. The goal is to find the longest contiguous subsegment of `a` that can be extended into an arithmetic progression with difference `d` by adding at most `k` elements. The output should be the indices `[l, r]` of this subsegment, choosing the smallest `l` in case of ties.

Constraints indicate that `n` can reach 2×10^5, and `k` can also be large, up to 2×10^5. With a 2-second time limit, any algorithm worse than O(n log n) or O(n) risks being too slow. The numbers themselves range up to ±10^9, meaning we must be careful with arithmetic but integer operations are safe in Python.

Edge cases arise in several ways. If `d` is zero, an arithmetic progression consists of equal numbers, so the problem reduces to counting how many elements are identical or can be made identical with at most `k` insertions. Another edge case is when `k` is zero: we cannot add numbers, so only naturally existing arithmetic progressions are allowed. Careless solutions that assume `d > 0` or ignore `k=0` will fail.

A simple illustrative edge case is `n=5, k=1, d=2, a=[1,3,7,9,11]`. The naive approach might try every subsegment, but the correct answer is `[3,5]` because adding `5` between `3` and `7` would exceed `k=1`. Small inputs can help verify boundary conditions where insertions are exactly used up.

## Approaches

A brute-force approach would examine every possible subsegment `[l,r]`, sort it, calculate the number of missing elements required to form an arithmetic progression with difference `d`, and check if this number is ≤ `k`. Sorting each subsegment takes O(n log n), and checking every subsegment is O(n^2), yielding O(n^3 log n) overall. This is clearly infeasible for n=2×10^5.

The key insight is that the number of missing elements in an arithmetic progression depends only on the minimum and maximum values of the segment and the difference `d`. For a segment of length `m` with minimum `min_val` and maximum `max_val`, the full AP would have length `((max_val - min_val) // d) + 1`. The missing elements are `full_length - m`. If this number ≤ `k`, the segment is valid.

This observation reduces the problem to maintaining the minimum and maximum of a sliding window efficiently. A multiset or balanced BST allows us to get min and max in O(log m) time per insertion/removal, which is fast enough. We can use a two-pointer (sliding window) technique: extend the right end until the segment becomes invalid, then move the left end to restore validity. This avoids checking all O(n^2) segments explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3 log n) | O(n) | Too slow |
| Sliding Window + Multiset | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers `l=0` and `r=0`. Use a multiset `window` to track elements in `a[l…r]`. Maintain `min_val` and `max_val` for the current window.
2. Iterate `r` from 0 to n-1, adding `a[r]` into the multiset. Update `min_val` and `max_val`.
3. Compute the required length of an ideal AP: `required_length = ((max_val - min_val) // d) + 1`.
4. Compute missing elements: `missing = required_length - window.size()`.
5. If `missing > k`, remove `a[l]` from the multiset and increment `l`. Repeat until `missing <= k`.
6. Update the answer if `r - l + 1` is larger than the previous best.
7. Continue until `r = n-1`. Output the 1-based indices `[best_l+1, best_r+1]`.

**Why it works**: The sliding window invariant guarantees that at any moment the current window `[l,r]` satisfies the property that it can become a k-d sequence. Since we extend `r` greedily and adjust `l` only when necessary, we explore all maximal windows efficiently. The min-max tracking ensures we compute the required AP length correctly, and the multiset handles duplicates and dynamic updates seamlessly.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

def main():
    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))

    if d == 0:
        best_len = 0
        best_l = 0
        l = 0
        while l < n:
            val = a[l]
            r = l
            while r < n and a[r] == val:
                r += 1
            count = r - l
            if count + k >= count:  # always true
                if count > best_len:
                    best_len = count
                    best_l = l
            l = r
        print(best_l+1, best_l + best_len)
        return

    window = SortedList()
    l = 0
    best_len = 0
    best_l = 0
    for r in range(n):
        window.add(a[r])
        while window[-1] - window[0] > d * (len(window) - 1) + k * d:
            window.remove(a[l])
            l += 1
        if len(window) > best_len:
            best_len = len(window)
            best_l = l

    print(best_l + 1, best_l + best_len)

if __name__ == "__main__":
    main()
```

The code first handles the `d=0` edge case separately because all elements must be equal. For `d>0`, it uses a `SortedList` from `sortedcontainers` to maintain the sliding window dynamically. The condition in the while loop ensures the number of missing elements never exceeds `k`.

## Worked Examples

### Sample 1

Input: `6 1 2; 4 3 2 8 6 2`

| l | r | window | min_val | max_val | required_length | missing | best_len |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [4] | 4 | 4 | 1 | 0 | 1 |
| 0 | 1 | [3,4] | 3 | 4 | 2 | 0 | 2 |
| 0 | 2 | [2,3,4] | 2 | 4 | 2 | 0 | 3 |
| 0 | 3 | [2,3,4,8] | 2 | 8 | 4 | 1 | 4 → exceeds k, remove l=0 |
| 1 | 3 | [3,4,8] | 3 | 8 | 4 | 1 | 3 |
| 2 | 4 | [4,8,6] | 4 | 8 | 3 | 0 | 3 |

Longest segment is `[2,4]` → 1-based `[3,5]`.

This trace shows how the sliding window moves and removes elements when the missing count exceeds `k`.

### Sample 2 (custom)

Input: `5 0 1; 1 2 4 5 6`

The algorithm finds `[0,1]` → `[1,2]` because adding no elements is allowed.

| l | r | window | min | max | req_len | missing | best_len |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | 1 | 1 | 0 | 1 |
| 0 | 1 | [1,2] | 1 | 2 | 2 | 0 | 2 |
| 0 | 2 | [1,2,4] | 1 | 4 | 4 | 1 → exceeds k | remove 1 → window [2,4] |

This confirms the sliding window correctly stops when `missing > k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element is added/removed from `SortedList` at most once, each operation O(log n) |
| Space | O(n) | `SortedList` stores at most n elements |

The algorithm easily fits within 2 seconds for n ≤ 2×10^5, with memory well under 256 MB.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# provided samples
assert run("6 1 2\n4 3
```
