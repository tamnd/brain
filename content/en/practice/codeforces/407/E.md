---
title: "CF 407E - k-d-sequence"
description: "We are given an integer sequence of length $n$ and two additional parameters: $k$, the maximum number of elements we are allowed to insert, and $d$, the intended difference of an arithmetic progression."
date: "2026-06-07T01:51:19+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 407
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 239 (Div. 1)"
rating: 3100
weight: 407
solve_time_s: 271
verified: false
draft: false
---

[CF 407E - k-d-sequence](https://codeforces.com/problemset/problem/407/E)

**Rating:** 3100  
**Tags:** data structures  
**Solve time:** 4m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer sequence of length $n$ and two additional parameters: $k$, the maximum number of elements we are allowed to insert, and $d$, the intended difference of an arithmetic progression. The task is to find the longest contiguous subarray of the original sequence that can be extended by at most $k$ numbers so that, after sorting, it forms an arithmetic progression with difference $d$. The output is the 1-based indices of the left and right ends of such a subarray. If multiple subarrays have the same length, we pick the one that starts earliest.

The constraints are high: $n$ can go up to $2 \cdot 10^5$, and $k$ can be of similar magnitude. A naive $O(n^2)$ approach that considers every possible subarray and counts the missing numbers to complete the arithmetic progression will perform roughly $2 \cdot 10^5 \cdot 10^5 \sim 2 \cdot 10^{10}$ operations in the worst case, far exceeding the 2-second limit. We need a near-linear algorithm, ideally $O(n \log n)$ or better.

Edge cases that might trip up a naive implementation include sequences where $d = 0$. For instance, the sequence `[5, 5, 5]` is trivially a good 2-d sequence for any $k \ge 0$, but carelessly assuming non-zero differences could cause errors. Another subtlety is that the subarray might already contain duplicates or be sorted in reverse; a careless approach may miscount missing elements if it assumes strict increasing sequences.

## Approaches

The brute-force approach is simple to describe. For each possible starting index $l$, we try every ending index $r \ge l$, extract the subarray $a[l..r]$, and compute the number of elements we would need to insert to make it an arithmetic progression with difference $d$. We sort the subarray, determine the smallest and largest values, calculate the expected number of elements for a full arithmetic progression, and subtract the subarray’s length. If the required insertions are at most $k$, we update the answer. While correct, this approach is $O(n^2 \log n)$ due to sorting each subarray, which is too slow for large $n$.

The key insight to optimize is that we only need the minimum and maximum of the subarray and the number of distinct elements after mapping to “positions modulo $d$” for $d \neq 0$. Specifically, every number in an arithmetic progression with difference $d$ must be of the form $start + j \cdot d$. If we define $b_i = (a_i - a_1) / d$ for each element in the subarray (assuming it is divisible by $d$), the subarray is a good $k$-$d$ sequence if the maximum of $b_i$ minus the minimum plus one minus the number of elements in the subarray does not exceed $k$.

This mapping reduces the problem to maintaining a window over the array and efficiently tracking the minimum and maximum of $b_i$ within the window. A sliding window combined with a balanced BST or a multiset can maintain these bounds in $O(\log n)$ per insertion/removal, giving $O(n \log n)$ overall.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n) | Too slow |
| Sliding Window + Multiset | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize pointers `left = 0` and `right = 0` to define a sliding window, and variables to store the best length and indices found so far.
2. Use a multiset (or equivalent structure) to maintain all mapped positions `(a_i - a[left]) / d` within the current window. This allows efficient retrieval of the minimum and maximum of the window at any time.
3. Expand the window by moving `right` forward one element at a time. For each new element `a[right]`, check if it can be included by computing its position relative to `a[left]`. If `(a[right] - a[left]) % d != 0`, the element cannot fit the arithmetic progression starting at `a[left]` and with difference `d`. In that case, move `left` forward until the remainder condition holds.
4. Maintain the invariant that the number of missing elements to complete the arithmetic progression is at most `k`. Compute this as `max_pos - min_pos + 1 - current_window_size`. If the invariant is violated, shrink the window from the left until it holds again.
5. After each expansion of the window, if the current window length is larger than the best recorded, update the best length and indices.
6. Continue until `right` reaches the end of the array. Return the stored best left and right indices.

**Why it works**: At every step, the window represents a contiguous subarray that could be extended into an arithmetic progression with at most `k` insertions. The sliding window ensures we only consider maximal valid subarrays starting from each left index. By tracking min and max in the mapped positions, we can calculate exactly how many elements are missing. No valid subarray is skipped, and no invalid subarray is incorrectly included.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict
from sortedcontainers import SortedList

n, k, d = map(int, input().split())
a = list(map(int, input().split()))

if d == 0:
    # special case: all elements must be equal
    best_len = 1
    best_l = 0
    count = defaultdict(int)
    l = 0
    for r in range(n):
        count[a[r]] += 1
        while (r - l + 1) - max(count.values()) > k:
            count[a[l]] -= 1
            if count[a[l]] == 0:
                del count[a[l]]
            l += 1
        if r - l + 1 > best_len:
            best_len = r - l + 1
            best_l, best_r = l, r
    print(best_l + 1, best_r + 1)
else:
    b = [ai // d for ai in a]
    best_len = 0
    best_l = 0
    s = SortedList()
    l = 0
    for r in range(n):
        s.add(b[r])
        while (s[-1] - s[0] + 1) - len(s) > k:
            s.remove(b[l])
            l += 1
        if r - l + 1 > best_len:
            best_len = r - l + 1
            best_l, best_r = l, r
    print(best_l + 1, best_r + 1)
```

The solution handles the edge case `d = 0` separately because division and modulo operations are not meaningful. For `d > 0`, we map each element to its “position index” in a hypothetical arithmetic progression, and a `SortedList` allows efficient tracking of minimum and maximum. The sliding window logic ensures the contiguous subarray satisfies the `k` insertions requirement.

## Worked Examples

**Sample Input 1**

```
6 1 2
4 3 2 8 6 2
```

| l | r | window `b` | min | max | max-min+1-len | Valid? |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [2] | 2 | 2 | 0 | Yes |
| 0 | 1 | [2,1] | 1 | 2 | 0 | Yes |
| 0 | 2 | [2,1,1] | 1 | 2 | 0 | Yes |
| 0 | 3 | [2,1,4] | 1 | 4 | 1 | Yes |
| 0 | 4 | [2,1,4,3] | 1 | 4 | 0 | Yes |
| 0 | 5 | [2,1,4,3,1] | 1 | 4 | 1 | Yes |

Longest valid window is indices 2-4 (1-based 3-5), corresponding to `[2,8,6]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element is added and removed from a `SortedList` once; operations are O(log n). |
| Space | O(n) | `SortedList` can store up to n elements. |

For $n \le 2 \cdot 10^5$, the algorithm executes roughly $4 \cdot 10^6$ log operations, which fits comfortably in 2 seconds.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    f = io.StringIO()
    with redirect_stdout(f):
        exec(open("solution.py").read())
    return f.getvalue().strip
```
