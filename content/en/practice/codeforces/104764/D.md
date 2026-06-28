---
title: "CF 104764D - Jelly Swarm"
description: "We are given a set of distinct points on a number line, each representing the position of a jellyfish friend. From these, we must choose exactly $K$ jellyfish and measure how spread out they are."
date: "2026-06-28T20:10:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 75
verified: false
draft: false
---

[CF 104764D - Jelly Swarm](https://codeforces.com/problemset/problem/104764/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct points on a number line, each representing the position of a jellyfish friend. From these, we must choose exactly $K$ jellyfish and measure how spread out they are. The spread of a chosen group is defined as the maximum distance between any two selected positions, which in one dimension is simply the difference between the largest and smallest chosen coordinates.

Among all possible subsets of size $K$, we want the one whose span is as small as possible, and we must output that minimum achievable span.

The constraints go up to $N = 2 \cdot 10^5$, so any solution that tries all subsets of size $K$ is immediately impossible. A naive combinational approach would require checking $\binom{N}{K}$ groups, which grows far beyond any feasible limit. Even checking all windows after sorting but recomputing distances inefficiently would still be fine computationally, so the key is recognizing that the structure of optimal solutions is simple enough to avoid combinatorial search.

A subtle edge case appears when $K = 1$. In that case, any single jellyfish forms a group whose maximum distance is zero, since there is no pair of distinct points. Another edge case arises when points are already tightly clustered versus widely separated; a greedy-looking selection without sorting can easily pick non-consecutive points and overestimate the span.

## Approaches

A brute-force strategy would enumerate all subsets of size $K$, compute the minimum and maximum element in each subset, and track the smallest difference. This is correct because it directly follows the definition of the objective. However, the number of subsets is exponential in $N$, and even if we assume computing each subset span is $O(K)$, the total work becomes astronomically large for $N = 2 \cdot 10^5$.

The key observation is that the order of points on the line completely determines the structure of an optimal subset. If we sort all positions, any optimal group of $K$ points will always correspond to a contiguous block in this sorted order. If a chosen set had a gap, replacing an interior-outside swap with a closer point reduces or preserves the span, so non-contiguous selections are never optimal.

This reduces the task to a sliding window problem over a sorted array: we only need to examine all consecutive segments of length $K$, compute their endpoint differences, and take the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{N}{K} \cdot K)$ | $O(K)$ | Too slow |
| Sorting + Sliding Window | $O(N \log N)$ | $O(1)$ extra (excluding sort) | Accepted |

## Algorithm Walkthrough

### 1. Sort all positions

We begin by sorting the array of coordinates. This places all jellyfish in increasing order along the line, making any group’s span computable as a simple difference between endpoints.

### 2. Initialize answer with infinity

We track the best (smallest) span seen so far. Initially, this is set to a very large value since we have not evaluated any group.

### 3. Slide a window of size $K$

For every index $i$ from $0$ to $N-K$, consider the group formed by positions $a[i], a[i+1], \dots, a[i+K-1]$. This represents a valid candidate group of $K$ jellyfish.

### 4. Compute span of each window

For each window, compute $a[i+K-1] - a[i]$, which directly gives the maximum distance within that group since the array is sorted.

### 5. Update the answer

We keep the minimum of all computed spans. The smallest among these is the optimal answer.

### Why it works

Once the array is sorted, any subset of $K$ elements has a well-defined minimum and maximum determined by their positions. If a subset skips an interior point while taking a farther one, replacing the farther point with the skipped closer point can only reduce the span or leave it unchanged. This implies that optimal subsets must consist of consecutive elements in sorted order. Therefore, checking all windows of length $K$ exhausts all meaningful candidates without missing any optimal configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = float('inf')
    
    for i in range(n - k + 1):
        ans = min(ans, a[i + k - 1] - a[i])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by reading $N$, $K$, and the list of positions. Sorting is essential because it transforms the geometric problem into a linear scan problem where spans become differences of endpoints.

The loop over all windows of size $K$ is safe because every candidate group of $K$ points can be mapped to a contiguous segment in sorted order without increasing its span. The subtraction $a[i + k - 1] - a[i]$ correctly captures the maximum pairwise distance inside that window.

The implementation avoids recomputing min/max inside each window, which would be unnecessary overhead, since sorted order guarantees endpoint sufficiency.

## Worked Examples

### Sample 1

Input:

```
5 3
8 6 15 5 1
```

Sorted array: `[1, 5, 6, 8, 15]`

| i | Window | Span |
| --- | --- | --- |
| 0 | [1, 5, 6] | 6 - 1 = 5 |
| 1 | [5, 6, 8] | 8 - 5 = 3 |
| 2 | [6, 8, 15] | 15 - 6 = 9 |

Minimum span is 3.

This shows that even though far points exist, the optimal group comes from a tight consecutive cluster.

### Sample 2

Input:

```
7 4
1 2 4 5 6 7 9
```

Sorted array is already given.

| i | Window | Span |
| --- | --- | --- |
| 0 | [1, 2, 4, 5] | 5 - 1 = 4 |
| 1 | [2, 4, 5, 6] | 6 - 2 = 4 |
| 2 | [4, 5, 6, 7] | 7 - 4 = 3 |
| 3 | [5, 6, 7, 9] | 9 - 5 = 4 |

Minimum span is 3.

This demonstrates that the best group is not necessarily anchored at one side, but emerges from wherever density is highest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting dominates, followed by linear scan over windows |
| Space | $O(1)$ extra | Only sorting and a few variables are used |

The constraints allow up to $2 \cdot 10^5$ elements, so $O(N \log N)$ sorting easily fits within time limits, and the linear scan is negligible in comparison.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# provided samples
assert run("5 3\n8 6 15 5 1\n") == "3\n", "sample 1"
assert run("7 4\n1 2 4 5 6 7 9\n") == "3\n", "sample 2"

# custom cases
assert run("1 1\n10\n") == "0\n", "single element"
assert run("5 5\n1 100 1000 10000 100000\n") == "99999\n", "all elements chosen"
assert run("6 2\n1 2 3 100 101 102\n") == "1\n", "tight pair exists"
assert run("4 2\n10 1 20 30\n") == "9\n", "boundary pair check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | K = 1 base case |
| all elements chosen | large span | K = N correctness |
| clustered + outliers | 1 | local optimal window |
| mixed spacing | 9 | correct min window selection |

## Edge Cases

When $K = 1$, the algorithm still works naturally. After sorting, each window is a single element, and the span computed is $a[i] - a[i] = 0$. The minimum remains zero, matching the definition that a single point has no internal distance.

When all points are far apart, such as `1 100 1000 10000` with $K = 2$, the algorithm checks every adjacent pair in sorted order. Even though the optimal pair is not necessarily the first two points in input order, sorting ensures we evaluate `1-100`, `100-1000`, and so on, and pick the smallest difference correctly.

When the optimal cluster is in the middle of the array, the sliding window naturally captures it. For example `1 2 3 100 101` with $K = 3$, the window `[1,2,3]` gives span 2, `[2,3,100]` gives 98, and `[3,100,101]` gives 98. The algorithm correctly identifies the dense region rather than being biased toward endpoints.
