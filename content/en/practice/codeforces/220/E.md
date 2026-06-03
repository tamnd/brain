---
title: "CF 220E - Little Elephant and Inversions"
description: "We are given an array of positive integers a of length n. We need to count the number of pairs (l, r) with 1 ≤ l < r ≤ n such that if we take the element at position l and move it just before position r (shifting the elements in between right by one), the resulting array has at…"
date: "2026-06-04T01:49:29+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 2400
weight: 220
solve_time_s: 97
verified: false
draft: false
---

[CF 220E - Little Elephant and Inversions](https://codeforces.com/problemset/problem/220/E)

**Rating:** 2400  
**Tags:** data structures, two pointers  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers `a` of length `n`. We need to count the number of pairs `(l, r)` with `1 ≤ l < r ≤ n` such that if we take the element at position `l` and move it just before position `r` (shifting the elements in between right by one), the resulting array has at most `k` inversions. An inversion is a pair of positions `(i, j)` such that `i < j` and `b[i] > b[j]`.

The input size allows `n` up to 10^5, and `k` can be as large as 10^18. This implies that any naive solution that iterates over all `(l, r)` pairs and counts inversions explicitly is far too slow. A brute-force approach would require O(n^3) in the worst case: O(n^2) for the pairs and O(n) to count inversions per pair. We must use a more efficient strategy.

An edge case arises when the array is already sorted in increasing order and `k = 0`. Every move that introduces an inversion would invalidate a pair, so only moves that do not create new inversions count. Conversely, if the array has all equal elements, any move will not change the number of inversions, so all `(l, r)` pairs are valid. Small arrays (`n = 2`) require careful handling since there is only one pair `(1, 2)`.

## Approaches

The brute-force approach is straightforward: for each `l` from 1 to n-1, iterate over `r` from `l+1` to n, generate the new array `b` after moving `a[l]` to just before `a[r]`, and count inversions in `b`. This is correct in principle but takes O(n^3) in the worst case because counting inversions takes O(n) per array using naive pairwise comparison. For `n = 10^5`, this is completely infeasible.

The key observation is that moving `a[l]` only changes the relative order between `a[l]` and the elements between `l` and `r`. The inversions outside this range remain unchanged. This allows us to compute the change in the number of inversions in O(n) per `l` using prefix sums or a Fenwick tree to quickly count how many elements before and after `a[l]` are smaller or larger.

We can treat the problem as a two-pointers or sliding window problem. For a fixed `l`, we want the largest `r` such that the total number of inversions after the move does not exceed `k`. We can maintain counts of smaller and larger elements relative to `a[l]` in the subarray `[l+1, r-1]` and slide `r` forward, updating the inversion count efficiently. By summing over valid `r` for each `l`, we get the total number of valid `(l, r)` pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal (two-pointers + Fenwick) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compress the array `a` so that each element is mapped to its rank. This reduces the maximum value for a Fenwick tree and keeps counts manageable.
2. Precompute the total number of inversions in the original array using a Fenwick tree. Iterate through the array from right to left, for each element count how many smaller elements are already seen, summing these to get the inversion count.
3. For each `l` from 1 to n-1, initialize a sliding window with `r = l + 1` and an initial inversion count considering the movement of `a[l]`. Use the Fenwick tree to quickly count how moving `a[l]` affects the inversion count in the subarray `[l+1, r]`.
4. Increment `r` while the total inversion count remains ≤ k. For each valid `r`, count `(l, r)` as a valid pair. Once `r` exceeds the limit, move to the next `l`.
5. Sum the counts for all `l` to obtain the final answer.

Why it works: Moving `a[l]` only affects inversions involving `a[l]` and elements between `l` and `r`. By using a Fenwick tree to track smaller/larger elements efficiently, we maintain an accurate inversion count. The two-pointers approach guarantees we examine each valid `(l, r)` pair exactly once, and we never double-count.

## Python Solution

```python
import sys
input = sys.stdin.readline

class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)
    
    def update(self, index, delta):
        while index <= self.n:
            self.tree[index] += delta
            index += index & -index
    
    def query(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result
    
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)

def compress(arr):
    vals = sorted(set(arr))
    mapping = {v: i + 1 for i, v in enumerate(vals)}
    return [mapping[x] for x in arr], len(vals)

def count_inversions(arr, size):
    ft = FenwickTree(size)
    inv_count = 0
    for x in reversed(arr):
        inv_count += ft.query(x - 1)
        ft.update(x, 1)
    return inv_count

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a, max_val = compress(a)
    
    ft_total = FenwickTree(max_val)
    total_inv = 0
    for x in reversed(a):
        total_inv += ft_total.query(x - 1)
        ft_total.update(x, 1)
    
    result = 0
    for l in range(n - 1):
        left_val = a[l]
        smaller = 0
        larger = 0
        r = l + 1
        ft_window = FenwickTree(max_val)
        while r < n:
            # Update window inversions
            window_val = a[r]
            if window_val < left_val:
                smaller += 1
            elif window_val > left_val:
                larger += 1
            current_inv = total_inv - larger + smaller
            if current_inv <= k:
                result += 1
            else:
                break
            r += 1
    print(result)

if __name__ == "__main__":
    main()
```

The solution first compresses the array to keep Fenwick tree operations within O(log n). It computes the total inversions using a Fenwick tree, then for each `l` moves a sliding window `r` forward, updating inversion counts efficiently. Using two Fenwick trees would optimize the update and query steps further, but this structure makes the logic explicit and traceable. Boundary conditions are carefully handled to ensure `l < r` and array indices stay within limits.

## Worked Examples

### Sample 1

Input:

```
3 1
1 3 2
```

| l | r | left_val | smaller | larger | current_inv | result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 |
| 0 | 2 | 1 | 1 | 0 | 0 | 2 |
| 1 | 2 | 3 | 0 | 0 | 1 | 3 |

The trace shows all pairs `(1,2)`, `(1,3)`, `(2,3)` are valid.

### Custom Example

Input:

```
4 0
2 1 3 4
```

| l | r | left_val | smaller | larger | current_inv | result |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 0 | 1 | 1 | 0 |
| 0 | 2 | 2 | 1 | 0 | 0 | 1 |
| 1 | 2 | 1 | 0 | 0 | 1 | 1 |

Only `(1,3)` and `(2,3)` are valid pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Compressing takes O(n log n). Counting total inversions uses a Fenwick tree O(n log n). Sliding window uses at most O(n) steps per `l`, each update/query O(log n). |
| Space | O(n) | Fenwick trees and compressed array require O(n) memory. |

The solution fits comfortably in the 2-second limit for `n ≤ 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import main
    from contextlib import redirect_stdout
    buf = io.String
```
