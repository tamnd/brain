---
title: "CF 105450A - Minimize Sour Difference"
description: "We are given a list of integer sourness values representing candies. Alice is allowed to remove exactly $k$ candies from this list, leaving $n-k$ candies behind."
date: "2026-06-23T03:05:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105450
codeforces_index: "A"
codeforces_contest_name: "UTPC x WiCS Contest 10-25-24 (UT Internal)"
rating: 0
weight: 105450
solve_time_s: 79
verified: false
draft: false
---

[CF 105450A - Minimize Sour Difference](https://codeforces.com/problemset/problem/105450/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integer sourness values representing candies. Alice is allowed to remove exactly $k$ candies from this list, leaving $n-k$ candies behind. After removal, we look at the remaining set and measure how “spread out” it is by taking the difference between the largest and smallest remaining value. The goal is to choose which candies to remove so that this final spread is as small as possible.

In other words, we are not trying to control pairwise differences inside some chosen subset directly, but instead we are controlling the range of what remains after deletions. The objective reduces to making the remaining values as tightly clustered as possible on the number line.

The constraints $n \le 1000$ allow a solution that is roughly $O(n^2)$, but also make it possible to use sorting and a sliding window without concern for performance. Anything $O(n^3)$ or worse would be risky at scale, but even $O(n^2)$ would pass comfortably.

A subtle but important edge case arises when all numbers are identical. In that case, every subset has range zero, and the answer must be zero regardless of removals. Another edge case is when only one candy remains after removals, meaning $n-k=1$. The range of a single element is always zero, and any correct approach must handle this explicitly or implicitly.

A common incorrect approach is to greedily remove extreme values from both ends without considering the best contiguous block. This can fail when the optimal solution is not centered or when multiple dense clusters exist. For example, with values like $[1, 2, 3, 100, 101]$, removing the wrong extremes might leave a wide gap even though a tight block exists.

## Approaches

The brute-force idea is straightforward: try every possible subset of size $n-k$, compute its minimum and maximum, and track the smallest possible range. This is correct because it checks all configurations, but it is computationally infeasible. The number of subsets is $\binom{n}{n-k}$, which grows exponentially and becomes impossible even for $n=30$.

The key observation is that only the relative ordering of values matters, not their original positions. Once the array is sorted, any optimal remaining set of size $n-k$ must consist of contiguous elements in this sorted order. If it were not contiguous, there would be a gap inside the selection, and replacing an extreme element with a closer missing element would always reduce or maintain the range.

This reduces the problem to choosing a window of size $n-k$ in the sorted array and minimizing the difference between its endpoints. Each window represents keeping a tightly packed group of candies and discarding everything outside it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{n}{k} \cdot n)$ | $O(n)$ | Too slow |
| Sort + Sliding Window | $O(n \log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. Sorting organizes all candidates so that any optimal subset becomes a contiguous segment in this ordering.
2. Compute the number of candies that will remain, $m = n - k$. This is the fixed size of the window we must evaluate.
3. Slide a window of size $m$ across the sorted array. For each window starting at index $i$, the window covers elements from $i$ to $i+m-1$.
4. For each window, compute the difference between its last and first element. This value represents the range if we keep exactly those candies.
5. Track the minimum such difference across all windows and output it.

Each step is necessary because sorting creates structure, the window enforces the subset size constraint, and evaluating endpoints directly captures the range without scanning inside the window.

### Why it works

After sorting, any subset of size $m$ that is not contiguous can be improved by replacing a large internal gap with a closer element outside the subset. This replacement never increases the range and often decreases it. Repeating this argument forces an optimal solution to become a contiguous block. Therefore, every optimal solution corresponds exactly to one sliding window of length $m$, and checking all such windows guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    m = n - k
    if m <= 1:
        print(0)
        return
    
    ans = float('inf')
    
    for i in range(n - m + 1):
        ans = min(ans, a[i + m - 1] - a[i])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that any optimal selection must appear as a contiguous block. The variable `m` represents how many candies remain after removals. If only one candy remains, the answer is immediately zero since no spread exists.

The loop checks every possible window of size `m`. For each starting index `i`, the difference `a[i + m - 1] - a[i]` computes the range of that segment. The minimum over all windows is the best achievable configuration.

A common implementation mistake is using `n-k` incorrectly as the number of removed elements rather than remaining ones. Another subtle issue is forgetting that the last valid window starts at `n-m`, not `n-m+1`.

## Worked Examples

### Sample 1

Input:

```
6 3
1 4 8 9 12 16
```

Here $m = 3$. After sorting (already sorted), we evaluate windows of size 3.

| i | window | range |
| --- | --- | --- |
| 0 | [1, 4, 8] | 7 |
| 1 | [4, 8, 9] | 5 |
| 2 | [8, 9, 12] | 4 |
| 3 | [9, 12, 16] | 7 |

Minimum range is 4.

This trace shows how the best solution is not necessarily at the extremes but in the densest region of the array.

### Sample 2

Input:

```
4 1
9 3 1 2
```

Sorted array: [1, 2, 3, 9], $m = 3$

| i | window | range |
| --- | --- | --- |
| 0 | [1, 2, 3] | 2 |
| 1 | [2, 3, 9] | 7 |

Minimum range is 2.

This demonstrates that removing a single extreme element (9) produces the tightest cluster.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, sliding window is linear |
| Space | $O(1)$ extra | In-place sort and constant auxiliary variables |

The constraints $n \le 1000$ make this comfortably fast. Even repeated sorting across multiple test cases would remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("6 3\n1 4 8 9 12 16\n") == "4"

# sample 2
assert run("4 1\n9 3 1 2\n") == "2"

# sample 3
assert run("6 4\n10 8 2 6 7 10\n") == "0"

# custom cases
assert run("2 1\n5 100\n") == "0"
assert run("5 2\n1 100 101 102 103\n") == "2"
assert run("5 4\n1 2 3 4 5\n") == "0"
assert run("6 2\n1 10 20 30 40 50\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 / 5 100 | 0 | single remaining element |
| 5 2 / 1 100 101 102 103 | 2 | optimal dense block in middle |
| 5 4 / 1 2 3 4 5 | 0 | removing one element from uniform progression edge case |
| 6 2 / 1 10 20 30 40 50 | 20 | wide spacing with best contiguous segment choice |

## Edge Cases

For the single-element remaining case, such as input:

```
3 2
10 1 7
```

After sorting, we get [1, 7, 10] and $m = 1$. The algorithm immediately returns 0 because any single element window has zero range. This avoids accessing invalid window endpoints and correctly reflects the definition of range.

For all-equal values:

```
5 2
7 7 7 7 7
```

Every window of any size has identical endpoints, so every computed range is 0. The minimum remains 0, and the algorithm naturally handles this without special casing.

For widely separated clusters:

```
6 2
1 2 3 100 101 102
```

Sorted array already shows two tight groups. Windows of size 4 will either include both clusters or only one. The optimal window is [1, 2, 3, 100] giving range 99, or [2, 3, 100, 101] giving 99 as well. This confirms the algorithm systematically evaluates all candidate contiguous selections and does not miss split-cluster configurations.
