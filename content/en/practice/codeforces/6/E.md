---
title: "CF 6E - Exposition"
description: "We are given a sequence of books by Berlbury, each with a known height, arranged chronologically. The library wants to organize an exposition by selecting consecutive books such that the difference between the tallest and shortest book in the selection does not exceed a given…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dsu", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 6
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 6 (Div. 2 Only)"
rating: 1900
weight: 6
solve_time_s: 58
verified: true
draft: false
---
[CF 6E - Exposition](https://codeforces.com/problemset/problem/6/E)

**Rating:** 1900  
**Tags:** binary search, data structures, dsu, trees, two pointers  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of books by Berlbury, each with a known height, arranged chronologically. The library wants to organize an exposition by selecting consecutive books such that the difference between the tallest and shortest book in the selection does not exceed a given limit, `k`. Our task is twofold: first, to maximize the number of books in such a selection, and second, to enumerate all consecutive intervals that achieve this maximum count while satisfying the height constraint.

The input provides `n`, the number of books, `k`, the maximum allowed height difference, and an array `h` of book heights. The output should first give the maximum number of books `a` and the number of valid periods `b`, followed by `b` lines of 1-based indices indicating the start and end of each period.

With `n` up to 10^5 and a 2-second time limit, any naive approach that checks all possible subarrays would be too slow. A brute-force examination of all possible intervals would require O(n^2) operations, which can reach 10^10 comparisons in the worst case. This is far beyond feasible, so we must find a more efficient method.

An important edge case arises when `k` is zero, meaning only consecutive books of exactly equal height can be selected. Another is when all books are strictly increasing or decreasing in height, which can cause the first or last book to be excluded in all maximal intervals if care is not taken. A careless approach may miss intervals at the boundaries or miscount the maximum length.

## Approaches

The brute-force approach iterates over every possible starting index `i` and for each, extends the interval to the right until the height difference exceeds `k`. For each interval, we track the length and compare it to the current maximum. This method is correct because it considers every consecutive subsequence, but it requires O(n^2) comparisons in the worst case. With `n = 10^5`, this results in 10^10 operations, which is far too slow for a 2-second time limit.

The key observation that unlocks an efficient solution is that we are only interested in consecutive subarrays where we need to maintain the minimum and maximum values efficiently. This structure allows us to use a two-pointer technique combined with a data structure capable of retrieving the min and max in O(1) for a sliding window. Specifically, using two deques to track indices of minimum and maximum heights lets us expand the right boundary while keeping the interval valid. When the interval becomes invalid, we move the left pointer forward, maintaining the invariant that the interval between the two pointers always satisfies the height difference constraint. This reduces the complexity to O(n), since each element is pushed and popped from the deques at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Two Pointers + Deques | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two deques: one for tracking maximum heights (`max_deque`) and one for minimum heights (`min_deque`). Initialize two pointers, `l = 0` and `r = 0`, representing the current interval `[l, r]`. Initialize variables to store the current maximum length `max_len` and a list `intervals` for valid intervals.
2. Expand the right pointer `r` one book at a time. For each new book `h[r]`, remove indices from the back of `max_deque` while `h[r]` is greater than the heights they represent. This ensures `max_deque[0]` always points to the maximum in the interval. Similarly, remove indices from the back of `min_deque` while `h[r]` is smaller than the heights they represent.
3. After adding `r` to both deques, check if the current interval `[l, r]` violates the height difference constraint: `h[max_deque[0]] - h[min_deque[0]] > k`. If it does, increment `l` to shrink the interval until the difference is at most `k`. Remove indices from the front of the deques that are now outside the interval.
4. When the interval `[l, r]` is valid, compare its length to `max_len`. If it exceeds `max_len`, update `max_len` and reset the `intervals` list with the current interval. If it equals `max_len`, append the current interval.
5. Increment `r` until the end of the array. After the loop, output `max_len`, the number of intervals, and each interval in 1-based indexing.

**Why it works**: The algorithm maintains the invariant that `[l, r]` is always the maximal consecutive interval ending at `r` with a valid height difference. Using deques ensures min and max are always tracked efficiently, so the length of each maximal interval is calculated correctly without missing any valid subsequence.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

n, k = map(int, input().split())
h = list(map(int, input().split()))

l = 0
max_len = 0
intervals = []

min_deque = deque()
max_deque = deque()

for r in range(n):
    while max_deque and h[r] > h[max_deque[-1]]:
        max_deque.pop()
    max_deque.append(r)
    
    while min_deque and h[r] < h[min_deque[-1]]:
        min_deque.pop()
    min_deque.append(r)
    
    while h[max_deque[0]] - h[min_deque[0]] > k:
        l += 1
        if max_deque[0] < l:
            max_deque.popleft()
        if min_deque[0] < l:
            min_deque.popleft()
    
    curr_len = r - l + 1
    if curr_len > max_len:
        max_len = curr_len
        intervals = [(l + 1, r + 1)]
    elif curr_len == max_len:
        intervals.append((l + 1, r + 1))

print(max_len, len(intervals))
for a, b in intervals:
    print(a, b)
```

The deques ensure that each operation on them is O(1) amortized. Boundary conditions are carefully handled by checking indices against `l` when the left pointer moves. 1-based indexing is applied when storing intervals.

## Worked Examples

Sample input 1:

```
3 3
14 12 10
```

Trace of key variables:

| r | l | max_deque | min_deque | curr_len | max_len | intervals |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0] | [0] | 1 | 1 | [(1,1)] |
| 1 | 0 | [0] | [1] | 2 | 2 | [(1,2)] |
| 2 | 1 | [1,2] | [2] | 2 | 2 | [(1,2),(2,3)] |

This demonstrates that the two-pointer and deque method correctly tracks all maximal intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each book is added and removed from each deque at most once. Two-pointer traversal is linear. |
| Space | O(n) | The two deques can each store up to `n` indices in the worst case. |

With n up to 10^5, O(n) operations easily fit in the 2-second limit, and the memory usage is well below 64 MB.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio
    f = sysio.StringIO()
    with redirect_stdout(f):
        exec(open('solution.py').read())
    return f.getvalue().strip()

# Provided sample
assert run("3 3\n14 12 10\n") == "2 2\n1 2\n2 3", "sample 1"

# Minimum size
assert run("1 0\n5\n") == "1 1\n1 1", "single book"

# All equal values
assert run("4 0\n7 7 7 7\n") == "4 1\n1 4", "all equal"

# Maximum k
assert run("5 1000000\n1 1000 500 999 1001\n") == "5 1\n1 5", "huge k allows all"

# Boundary condition
assert run("5 2\n1 2 3 4 5\n") == "3 3\n1 3\n2 4\n3 5", "sliding windows correct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 book | 1 1\n1 1 | Minimal input handled correctly |
| 4 books equal | 4 1\n1 4 | k=0 with all equal heights |
| Max k | 5 1\n1 5 | Large k includes all |
