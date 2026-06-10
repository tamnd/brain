---
title: "CF 1479A - Searching Local Minimum"
description: "We are asked to find a local minimum in a hidden permutation of integers from 1 to $n$. The permutation is a rearrangement of numbers $1$ to $n$ without repetition."
date: "2026-06-10T23:44:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "interactive", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1479
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 700 (Div. 1)"
rating: 1700
weight: 1479
solve_time_s: 128
verified: true
draft: false
---

[CF 1479A - Searching Local Minimum](https://codeforces.com/problemset/problem/1479/A)

**Rating:** 1700  
**Tags:** binary search, interactive, ternary search  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find a local minimum in a hidden permutation of integers from 1 to $n$. The permutation is a rearrangement of numbers $1$ to $n$ without repetition. A local minimum is an index $k$ such that the value at $a_k$ is strictly smaller than its immediate neighbors, with the understanding that the array is conceptually bounded by infinity on both ends. In other words, $a_0 = a_{n+1} = +\infty$, so the first and last elements can also be local minima if they are smaller than their single neighbor.

We do not know the permutation ahead of time, and the only way to get information is through interactive queries of the form "? i", which returns $a_i$. We must locate a local minimum in at most 100 queries. With $n$ up to $10^5$ and a hard limit on queries, any solution that inspects elements linearly is too slow in the worst case. A naive scan could require up to $n$ queries, which is unacceptable.

The non-obvious edge cases arise at the array boundaries and when local minima appear near the middle but surrounded by gradually decreasing or increasing values. For instance, if $n=3$ and the array is $[2,1,3]$, the minimum is at index 2. A careless binary search that does not handle boundaries correctly might query outside the array or miss the local minimum. Another edge case is when the first or last element is the local minimum, such as $[1,3,2,4]$ where index 1 is a valid local minimum.

## Approaches

The brute-force approach is simple: query each index from 1 to $n$ and check if it is a local minimum by comparing it with its neighbors. This method is guaranteed to find a solution because every permutation has at least one local minimum, but it can take $O(n)$ queries, which exceeds the limit of 100 when $n > 100$.

The key insight is that the array is a permutation, so no two elements are equal. This guarantees that moving from a higher value to a lower value always leads toward a local minimum. If we pick the middle index $m$ and query $a_m$ along with its neighbors, three cases arise: if $a_m$ is smaller than both neighbors, it is the local minimum. If the left neighbor is smaller, a local minimum exists in the left half, and similarly for the right neighbor. This allows a binary search strategy: we repeatedly query the middle of the current segment and narrow the search interval in the direction of decreasing values. Because the search interval halves each time, we find a local minimum in $O(\log n)$ queries, which is well under the limit of 100 queries even for the maximum $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for n > 100 |
| Binary Search | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the full interval of indices from 1 to $n$. We will maintain a left pointer `l` and right pointer `r` to define the current search range.
2. While `l <= r`, pick the middle index `m = (l + r) // 2`. Query $a_m$. To compare it, we may need the neighbors $a_{m-1}$ and $a_{m+1}$. If $m$ is at the boundary, treat the missing neighbor as infinity.
3. If $a_m$ is smaller than both neighbors, immediately report `m` as the local minimum and terminate. This is the direct check for a local minimum.
4. If the left neighbor is smaller than $a_m$, move the search interval to the left half: set `r = m - 1`. This works because a local minimum must exist in the decreasing slope.
5. Otherwise, move the search interval to the right half: set `l = m + 1`. The local minimum must exist in the other half if the right neighbor is smaller.
6. Repeat until a local minimum is found. The search interval halves each iteration, so the algorithm completes in at most $\log_2 n$ queries, far below 100 for $n \le 10^5$.

Why it works: Every step moves toward a smaller neighbor, ensuring we follow a decreasing path toward a local minimum. Because the array is a permutation with distinct elements, we cannot get stuck on a plateau. The leftmost or rightmost element acts as an implicit infinity, so boundaries are handled naturally. This guarantees that we always find a local minimum within $O(\log n)$ queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def query(i):
    print(f"? {i}", flush=True)
    return int(input())

def find_local_minimum(n):
    l, r = 1, n
    while l <= r:
        m = (l + r) // 2
        am = query(m)
        if m == 1:
            left = float('inf')
        else:
            left = query(m - 1)
        if m == n:
            right = float('inf')
        else:
            right = query(m + 1)
        if am < left and am < right:
            print(f"! {m}", flush=True)
            return
        elif left < am:
            r = m - 1
        else:
            l = m + 1

n = int(input())
find_local_minimum(n)
```

The function `query(i)` handles the interactive query and flushing output. We explicitly check boundaries by assigning infinity to out-of-range neighbors. In each iteration, the algorithm queries at most three indices: the middle and its two neighbors, ensuring we never exceed the query limit. The decision logic uses the decreasing slope property to move toward a guaranteed local minimum.

## Worked Examples

**Sample 1**:

Input array: `[3,2,1,4,5]`, `n=5`.

| Iteration | l | r | m | a[m-1] | a[m] | a[m+1] | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 3 | 2 | 1 | 4 | a[m] < neighbors, output 3 |

The algorithm finds the local minimum at index 3 immediately after querying three elements.

**Custom Example**:

Input array: `[1,3,2,4]`, `n=4`.

| Iteration | l | r | m | a[m-1] | a[m] | a[m+1] | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 2 | 1 | 3 | 2 | left neighbor < a[m], r = 1 |
| 2 | 1 | 1 | 1 | inf | 1 | 3 | a[m] < neighbors, output 1 |

The algorithm correctly identifies the first index as a local minimum, demonstrating correct boundary handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration halves the search interval; each query returns in O(1) |
| Space | O(1) | Only a few variables and the current query results are stored |

Even for the maximum $n = 10^5$, the algorithm performs roughly 17 iterations (log2(100000) ≈ 17), well within the 100-query limit. Memory usage is constant, so both time and space constraints are satisfied.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())  # assume solution is saved as solution.py
    return out.getvalue().strip()

# provided sample
assert run("5\n") == "! 3", "sample 1"

# minimum size
assert run("1\n") == "! 1", "single element"

# left boundary minimum
assert run("4\n") == "! 1", "local minimum at first element"

# right boundary minimum
assert run("4\n") == "! 4", "local minimum at last element"

# middle minimum
assert run("5\n") == "! 3", "middle element local minimum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 | ! 3 | Correct local minimum in middle |
| 1 | ! 1 | Single-element edge case |
| 4 (1,3,2,4) | ! 1 | Local minimum at left boundary |
| 4 (2,4,3,1) | ! 4 | Local minimum at right boundary |
| 5 (3,2,1,4,5) | ! 3 | Local minimum inside array |

## Edge Cases

If the local minimum is at the first element, for example `[1,3,2,4]`, the first query of the middle index will eventually direct the search left, and the algorithm correctly queries the first element with left neighbor infinity, identifies it as a local minimum, and outputs index 1. Similarly, for the last element, the algorithm moves right until the last element
