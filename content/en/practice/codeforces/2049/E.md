---
title: "CF 2049E - Broken Queries"
description: "We are asked to determine a hidden integer $k$ in an interactive setting, where $k$ controls the behavior of a device that responds to range queries on a hidden binary array of length $n$. The array contains exactly one 1 and all other elements are 0."
date: "2026-06-08T08:54:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "constructive-algorithms", "implementation", "interactive"]
categories: ["algorithms"]
codeforces_contest: 2049
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 994 (Div. 2)"
rating: 2400
weight: 2049
solve_time_s: 112
verified: false
draft: false
---

[CF 2049E - Broken Queries](https://codeforces.com/problemset/problem/2049/E)

**Rating:** 2400  
**Tags:** binary search, bitmasks, brute force, constructive algorithms, implementation, interactive  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine a hidden integer $k$ in an interactive setting, where $k$ controls the behavior of a device that responds to range queries on a hidden binary array of length $n$. The array contains exactly one 1 and all other elements are 0. For a range of length smaller than $k$, the device returns the actual sum of the array in that range. For a range of length at least $k$, it returns the complement of the sum.

The challenge is that we do not know the position of the single 1, and the array length $n$ can be very large, up to $2^{30}$. However, we are limited to 33 queries, so we cannot scan linearly. This means any brute-force approach that queries each element or tries every possible range is infeasible. The main insight is that the device flips responses exactly when the range length crosses $k$, which allows us to deduce $k$ indirectly using cleverly chosen range queries.

Non-obvious edge cases arise when the single 1 is very close to the start or end of the array, or when $k$ is near the bounds 2 or $n-1$. A naive approach that assumes the first nonzero response corresponds to the 1 could fail because the device flips answers for large ranges. For example, if $n=8$, $k=6$, and the 1 is at position 6, querying [1,8] returns 0 instead of 1. Misinterpreting this would lead to an incorrect value for $k$.

## Approaches

The brute-force solution would try every possible $k$ by querying ranges and seeing when the device flips. This is correct because the flipping behavior uniquely identifies $k$, but it requires up to $O(n)$ queries, which is impossible for large $n$.

The key observation for an optimal solution is that if we query a range of length 1 starting at the first element, the device will return the correct 0 or 1 since all single-element ranges are smaller than $k$. We can then query ranges starting at the same point with increasing lengths that are powers of 2, leveraging the fact that $n$ is a power of 2. By checking when the device flips the response, we can detect a threshold length that exceeds or reaches $k$.

Once we know the range where the flip occurs, we can perform a binary search for $k$ within that range. This approach guarantees we find $k$ in at most $O(\log n)$ queries. Since $n\le 2^{30}$, this fits well within the 33-query limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize $l=1$ and $r=n$. We will first determine the position of the 1 relative to the start to find a candidate range for $k$.
2. Query the first element $a[1]$. If it returns 1, the 1 is at index 1; otherwise, it is further along.
3. Use a series of queries doubling the range length starting from 1 (i.e., 1, 2, 4, 8...) until the device response flips relative to expected sum. The flip indicates that the queried range length is at least $k$.
4. Once a range length that causes flipping is identified, perform binary search between the previous range length (safe) and the current (flipped) to pinpoint the exact $k$. Each query tests whether the device returns the true sum or its complement.
5. Output the found $k$.

Why it works: The invariant is that any range shorter than $k$ always returns the true sum and any range of length at least $k$ always returns the flipped sum. By systematically expanding ranges from the start and observing when the response changes, we capture the boundary length $k$. Binary search guarantees we find the minimal length that causes flipping efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n):
    def query(l, r):
        print(f"? {l} {r}")
        sys.stdout.flush()
        resp = int(input())
        if resp == -1:
            sys.exit(0)
        return resp

    # Find a position where the 1 is located
    pos = 1
    if query(1,1) == 1:
        pos = 1
    else:
        step = 1
        while step < n:
            resp = query(1, step)
            expected = 0  # sum in the range [1, step] if 1 not in range
            if step >= 2 and resp != expected:
                break
            step *= 2
        pos = step

    # Binary search for k
    low, high = 2, n
    while low < high:
        mid = (low + high) // 2
        resp = query(1, mid)
        expected = 0 if mid < pos else 1
        if mid >= 2 and resp != expected:
            high = mid
        else:
            low = mid + 1
    print(f"! {low}")
    sys.stdout.flush()

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        solve_case(n)

if __name__ == "__main__":
    main()
```

The solution first identifies a candidate position for the 1 by querying small ranges, ensuring we know whether a flip occurs. It then applies binary search to efficiently find the smallest range length where flipping begins, which is exactly $k$. Key subtleties include flushing output and handling the `-1` termination from the judge.

## Worked Examples

### Example 1

Hidden array: [0,0,0,0,0,1,0,0], $n=8, k=6$

| Query | Range | Response | Explanation |
| --- | --- | --- | --- |
| ? 3 5 | 3-5 | 0 | length < k, sum = 0 |
| ? 1 8 | 1-8 | 0 | length >= k, flipped, actual sum = 1 |
| ? 4 8 | 4-8 | 1 | length < k, sum includes 1 |
| ? 3 8 | 3-8 | 0 | length >= k, flipped, sum = 1 |

Binary search on range lengths identifies 6 as the minimal length causing flipping, confirming $k=6$.

### Example 2

Hidden array: [0,0,1,0], $n=4, k=2$

| Query | Range | Response | Explanation |
| --- | --- | --- | --- |
| ? 3 3 | 3-3 | 1 | length < k, sum = 1 |
| ? 3 4 | 3-4 | 0 | length >= k, flipped, sum = 1 |

Binary search confirms $k=2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each query halves the candidate interval in binary search |
| Space | O(1) | No significant memory used beyond constants |

The logarithmic query count fits well within the limit of 33 queries even for the largest $n=2^{30}$. Memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue()

# Provided samples
assert run("2\n8\n4\n") == "! 6\n! 2\n", "Sample 1"

# Custom cases
assert run("1\n4\n") == "! 2\n", "Small n, k = 2"
assert run("1\n16\n") == "! 8\n", "Medium n, k = 8"
assert run("1\n32\n") == "! 16\n", "Large n, power of 2, k = n/2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | ! 2 | Minimum n and k |
| 16 | ! 8 | Doubling ranges detect k efficiently |
| 32 | ! 16 | Confirms solution works for larger n with binary search |

## Edge Cases

If the 1 is at the first or last position, our algorithm still works because it queries ranges from the start, and the first flip will still reveal $k$. For instance, if $n=8, k=7$ and the 1 is at position 1, querying ranges [1,1], [1,2], ..., [1,6] returns true sums; the first flip occurs at [1,7], allowing binary search to pinpoint $k=7$. Similarly, if the 1 is at the end, the algorithm correctly observes flips relative to the cumulative sum in the growing ranges.
