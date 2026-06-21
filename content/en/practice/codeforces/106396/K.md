---
title: "CF 106396K - \u5171\u6b7b"
description: "We are given a list of integers and a threshold value $k$. From this list, we are interested in how “close” any two elements can get under the XOR operation."
date: "2026-06-21T09:59:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106396
codeforces_index: "K"
codeforces_contest_name: "Tiangong University 2025 ICPC Team Selection Contest II (Online Mirror)"
rating: 0
weight: 106396
solve_time_s: 41
verified: true
draft: false
---

[CF 106396K - \u5171\u6b7b](https://codeforces.com/problemset/problem/106396/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and a threshold value $k$. From this list, we are interested in how “close” any two elements can get under the XOR operation. Concretely, we look at all pairs of numbers in the array, compute their bitwise XOR, and focus on the smallest XOR value achievable between any pair.

The task is to determine whether this minimum pairwise XOR is at most $k$. If there exists at least one pair whose XOR is small enough, the answer is affirmative, otherwise it is negative.

From a computational standpoint, the array size can be large enough that checking every pair directly would be infeasible. A full pairwise comparison requires $O(n^2)$ operations, which becomes too slow when $n$ grows to typical Codeforces limits like $10^5$.

A subtle case arises when all numbers are identical. In that situation, every XOR is zero, so the answer is always “Yes” regardless of $k$. Another important situation is when values are widely spaced in binary representation. Even if numbers are numerically close, their XOR may still be large due to differing high bits, so ordering by value alone is not obviously sufficient without justification.

## Approaches

The brute-force idea is straightforward: compute XOR for every pair $(i, j)$, track the minimum, and compare it with $k$. This works because it directly evaluates the definition of the problem. However, the number of pairs is $n(n-1)/2$, which reaches around $5 \times 10^9$ operations when $n = 10^5$, far beyond feasible limits.

The key observation is that we do not actually need to compare all pairs. The structure of XOR over integers implies that if two numbers are close in sorted order, they are the most likely candidates to produce the smallest XOR. The reason is that XOR is dominated by the highest bit where two numbers differ. If two numbers are far apart in sorted order, their most significant differing bit is likely high, making their XOR large. Conversely, adjacent elements in sorted order minimize the first position where they differ, which tends to minimize the XOR value.

This reduces the problem to sorting the array and checking XOR only between consecutive elements. The minimum XOR over all pairs must appear among at least one adjacent pair in sorted order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sort + Adjacent Check | $O(n \log n)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the array size $n$ and threshold $k$, followed by the array values.
2. Sort the array in non-decreasing order. This organizes values so that numerically close elements become neighbors.
3. Initialize a variable `ans` to a large number, representing the best XOR found so far.
4. Iterate through the sorted array from index 1 to $n-1$, computing XOR between each pair of consecutive elements.
5. Update `ans` with the minimum of its current value and the computed XOR.
6. After processing all adjacent pairs, compare `ans` with $k$.
7. Output “Yes” if `ans <= k`, otherwise output “No”.

### Why it works

Sorting aligns elements so that any pair with potentially small XOR is forced to appear next to each other. The crucial property is that XOR is determined by the highest differing bit, and any non-adjacent pair must differ at a position at least as significant as some adjacent boundary in the sorted order. Thus, the minimum XOR over all pairs cannot be missed when restricting attention to neighbors in sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = 1 << 60
    
    for i in range(1, n):
        ans = min(ans, a[i - 1] ^ a[i])
    
    print("Yes" if ans <= k else "No")

if __name__ == "__main__":
    solve()
```

The solution begins by reading input efficiently. Sorting is performed once, after which only local adjacency comparisons are needed. The XOR computation uses constant-time bit operations. The sentinel value for `ans` is chosen large enough to avoid accidental overflow in comparisons.

A common mistake is attempting to compare only neighboring values in the original unsorted array, which fails because ordering by input position has no relation to XOR structure. Sorting is essential.

## Worked Examples

### Example 1

Input:

```
4 3
1 5 2 8
```

Sorted array: `[1, 2, 5, 8]`

| i | Pair | XOR | ans |
| --- | --- | --- | --- |
| 1 | 1 ^ 2 | 3 | 3 |
| 2 | 2 ^ 5 | 7 | 3 |
| 3 | 5 ^ 8 | 13 | 3 |

Final `ans = 3`, and since $3 \le 3$, output is `Yes`.

This demonstrates how the optimal pair may come from early adjacent elements after sorting, even if original positions were unrelated.

### Example 2

Input:

```
3 1
10 14 20
```

Sorted array: `[10, 14, 20]`

| i | Pair | XOR | ans |
| --- | --- | --- | --- |
| 1 | 10 ^ 14 | 4 | 4 |
| 2 | 14 ^ 20 | 26 | 4 |

Final `ans = 4`, and since $4 > 1$, output is `No`.

This shows that even relatively close values can produce large XOR due to high-bit differences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear scan follows |
| Space | $O(1)$ extra | In-place sorting aside from input storage |

The approach is efficient for typical constraints up to $10^5$, since sorting and a single pass are well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = 1 << 60
    for i in range(1, n):
        ans = min(ans, a[i - 1] ^ a[i])
    
    return "Yes" if ans <= k else "No"

# provided sample-like cases
assert run("4 3\n1 5 2 8\n") == "Yes"
assert run("3 1\n10 14 20\n") == "No"

# minimum size
assert run("2 0\n7 7\n") == "Yes"

# boundary: just above threshold
assert run("2 3\n1 4\n") == "No"

# all equal
assert run("5 0\n9 9 9 9 9\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 identical values | Yes | XOR = 0 edge case |
| small pair just above k | No | threshold boundary |
| all equal array | Yes | degenerate minimum case |

## Edge Cases

For an input like:

```
2 5
100 103
```

After sorting, the only pair is `(100, 103)` with XOR `7`. The algorithm computes this directly, stores it as `ans`, and correctly returns `No` since $7 > 5$. This confirms that even in minimal-size inputs, the logic degenerates correctly to direct pair evaluation without special handling.
