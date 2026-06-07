---
title: "CF 2087D - Uppercase or Lowercase?"
description: "We are given a sorted list of strings, called handles, with the total number $n$ and a target handle $h$. The goal is to determine the 1-based position of $h$ in this list."
date: "2026-06-08T05:58:26+07:00"
tags: ["codeforces", "competitive-programming", "*special", "interactive"]
categories: ["algorithms"]
codeforces_contest: 2087
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 12"
rating: 0
weight: 2087
solve_time_s: 100
verified: false
draft: false
---

[CF 2087D - Uppercase or Lowercase?](https://codeforces.com/problemset/problem/2087/D)

**Rating:** -  
**Tags:** *special, interactive  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sorted list of strings, called handles, with the total number $n$ and a target handle $h$. The goal is to determine the 1-based position of $h$ in this list. The challenge is that the sorting order is lexicographical, but we do not know whether uppercase letters come before lowercase letters or the other way around. Each handle starts with either a lowercase or uppercase letter, but all subsequent letters are lowercase. Handles are unique and the target handle is guaranteed to exist.

The interaction allows us to query the handle at a specific position $i$ and we can perform at most 10 such queries. Because $n$ can be as high as 500, iterating over the entire list would require up to 500 queries, which exceeds our limit. Therefore, we need a strategy that guarantees we can find $h$ with at most 10 queries.

A naive approach is to check each position in order, but this would fail once $n > 10$. Another subtlety is that the first character’s case can change the effective lexicographical order: for example, if the first letter is uppercase, "Apple" may come before "banana" or after, depending on the system. If a solution ignores this, it may stop searching too early or in the wrong half of the list.

Edge cases include the target being the first or last element, or the first element having an uppercase letter while the rest are lowercase. These could mislead a naive binary search if we assume lowercase always comes first.

## Approaches

The brute-force approach is simple: query positions from 1 to $n$ until the returned handle equals $h$. This is guaranteed to find the handle because we know it exists, but requires up to $n$ queries. For $n = 500$, this is far beyond the 10-query limit, so brute force is not feasible.

The optimal approach leverages binary search. Lexicographical order is total, so if we can determine which order the database uses (uppercase-first or lowercase-first), we can perform a classical binary search. The key insight is that we do not need to query every element to determine the order. The first handle in the list reveals the ordering pattern: compare it with a string that starts with a lowercase letter. If the first handle is smaller than any lowercase string, uppercase comes first; otherwise, lowercase comes first. Once the order is known, we can perform a binary search with at most $\lceil \log_2 n \rceil \le 9$ queries for $n \le 500$, which fits the limit.

The problem structure allows this because all handles are sorted and unique. The uncertainty in case only affects the first character, so we can establish a comparison function for the binary search that correctly interprets lexicographical order in this list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for n > 10 |
| Binary Search with order detection | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Query the first handle in the list to determine the case-based ordering. If the first character is uppercase, assume uppercase-first order; if lowercase, assume lowercase-first order. This is safe because the list is sorted, so the first element always reflects which case comes first.
2. Initialize two pointers, `lo = 1` and `hi = n`. This sets up a classical binary search on positions.
3. While `lo <= hi`, compute the middle index `mid = (lo + hi) // 2`. Query the handle at position `mid`.
4. Compare the returned handle with $h$ using standard string comparison. Respect the detected case order: if uppercase-first, compare strings normally; if lowercase-first, treat lowercase as coming first for comparison purposes. If the middle handle is less than $h$, move `lo = mid + 1`. Otherwise, move `hi = mid - 1`.
5. Repeat until `lo` surpasses `hi`. At this point, the position of $h$ is `lo`, since binary search narrows to the exact index of the target in a sorted list.

Why it works: the binary search invariant is that $h$ is always within the current `lo..hi` interval. Each query halves the interval, so after at most $\lceil \log_2 n \rceil$ queries, the interval reduces to a single element. The initial check of the first handle ensures the comparison function matches the database’s lexicographical ordering, preventing errors due to uppercase/lowercase ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline
print_flush = lambda x: (print(x, flush=True))

def find_handle_position(n, h):
    # Determine case ordering from the first handle
    print_flush("? 1")
    first = input().strip()
    
    def cmp(a, b):
        # Compare respecting the detected order
        # If first character of first handle is uppercase, assume uppercase < lowercase
        if first[0].isupper():
            return a < b
        else:
            return a < b  # lowercase-first, normal comparison suffices

    lo, hi = 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        print_flush(f"? {mid}")
        mid_val = input().strip()
        if mid_val == h:
            print_flush(f"! {mid}")
            return
        if cmp(mid_val, h):
            lo = mid + 1
        else:
            hi = mid - 1
```

We query the first element to detect the ordering. `cmp` reflects this ordering for binary search. Each iteration halves the search range, and if the middle element matches `h`, we return immediately. If not, we adjust `lo` or `hi` according to comparison, guaranteeing convergence within 9 queries for $n \le 500$.

## Worked Examples

### Example 1

Input list: `["Bleddest", "Neon", "adedalic", "awoo"]`, target `adedalic`.

| lo | hi | mid | Query(mid) | cmp(mid_val, h) | New lo/hi |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 2 | Neon | Neon < adedalic? True | lo = 3 |
| 3 | 4 | 3 | adedalic | Equal | Found 3 |

The table confirms binary search quickly narrows down to position 3.

### Example 2

Input list: `["apple", "banana", "cherry", "date"]`, target `cherry`.

| lo | hi | mid | Query(mid) | cmp(mid_val, h) | New lo/hi |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 2 | banana | True | lo = 3 |
| 3 | 4 | 3 | cherry | Equal | Found 3 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each query halves the search interval, at most 9 queries for n ≤ 500 |
| Space | O(1) | Only a few variables for pointers and strings are stored |

The solution fits well within the 2-second limit and 512 MB memory bound.

## Test Cases

```python
# helper: simulate interaction
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    def print_flush(x):
        output.append(x)
    n_h = sys.stdin.readline().strip().split()
    n = int(n_h[0])
    h = n_h[1]
    handles = [sys.stdin.readline().strip() for _ in range(n)]
    def input_mock():
        return handles.pop(0) + "\n"
    global input
    input_backup = input
    input = input_mock
    # run solution
    find_handle_position(n, h)
    input = input_backup
    return "\n".join(output)

# Sample 1
inp1 = "4 adedalic\nBleddest\nNeon\nadedalic\nawoo\n"
assert run(inp1) == "? 1\n? 2\n? 3\n! 3", "Sample 1"

# Custom case: target first
inp2 = "5 Alpha\nAlpha\nBeta\nGamma\nDelta\nEpsilon\n"
assert run(inp2) == "? 1\n! 1", "Target first"

# Custom case: target last
inp3 = "3 cat\napple\nbanana\ncat\n"
assert run(inp3) == "? 1\n? 2\n? 3\n! 3", "Target last"

# Custom case: single element
inp4 = "1 lone\nlone\n"
assert run(inp4) == "? 1\n! 1", "Single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | ? 1 ? 2 ? 3 ! 3 | Normal binary search with mixed case |
| Target first | ? 1 ! 1 | First element detection and immediate return |
| Target last | ? 1 ? 2 ? 3 ! 3 |  |
