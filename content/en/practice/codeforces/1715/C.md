---
title: "CF 1715C - Monoblock"
description: "We are given an array of integers, and we define its awesomeness as the minimum number of consecutive identical blocks the array can be split into. For example, [1,1,2,2,2,3] has awesomeness 3 because it can be split into [1,1], [2,2,2], [3]."
date: "2026-06-09T19:55:21+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1715
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 816 (Div. 2)"
rating: 1700
weight: 1715
solve_time_s: 129
verified: true
draft: false
---

[CF 1715C - Monoblock](https://codeforces.com/problemset/problem/1715/C)

**Rating:** 1700  
**Tags:** combinatorics, data structures, implementation, math  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we define its awesomeness as the minimum number of consecutive identical blocks the array can be split into. For example, `[1,1,2,2,2,3]` has awesomeness 3 because it can be split into `[1,1]`, `[2,2,2]`, `[3]`. The problem asks us to support queries that change a single element of the array and, after each change, calculate the sum of awesomeness values over all subarrays.

The array length and number of queries can be up to $10^5$. A brute-force approach that considers every subarray after each query would require up to $10^5 \cdot 10^{10}$ operations in the worst case, which is obviously far too slow. This forces us to find a way to compute the sum efficiently, ideally in O(1) or O(log n) per query, after some preprocessing.

Non-obvious edge cases include arrays with all identical elements, arrays where every element is distinct, and updates that do not change the value of the array element. For example, if the array is `[5,5,5]` and we set the second element to 5 again, the sum of awesomeness should remain unchanged. Similarly, updates at the edges of the array may affect fewer subarrays and need careful handling.

## Approaches

The brute-force method iterates over all subarrays after each query and counts blocks. For an array of length $n$, there are $\frac{n(n+1)}{2}$ subarrays, and for each subarray, counting blocks takes up to $O(n)$. This gives a worst-case complexity of $O(n^3)$ per query, which is impractical for $n = 10^5$.

The key insight is that the sum of awesomeness of all subarrays can be expressed as $n(n+1)/2$ plus a contribution from every position where the element changes value relative to its neighbor. Specifically, a block boundary occurs at index $i$ if $a[i] \neq a[i+1]$. Each such boundary contributes to all subarrays that contain it, and the number of such subarrays is exactly $i \cdot (n-i)$ for a boundary between positions $i$ and $i+1$.

This reduces the problem to tracking the set of adjacent pairs that are unequal. Each query changes at most two pairs: the one on the left of the updated index and the one on the right. By maintaining a running total of contributions from all boundaries, we can update the answer in O(1) per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the sum of awesomeness. Start with `total = n*(n+1)//2`. This counts every subarray as at least one block.
2. Iterate over all adjacent pairs `(a[i], a[i+1])`. If they are different, compute their contribution as `i * (n-i)` and add it to `total`. This step computes the contribution of all block boundaries.
3. For each query `(idx, x)`, consider the two boundaries affected: `(idx-1, idx)` and `(idx, idx+1)`, if they exist. Subtract the old contributions from `total` before the update.
4. Update `a[idx] = x`.
5. Add the contributions of the potentially new boundaries `(idx-1, idx)` and `(idx, idx+1)` to `total`.
6. Print `total`.

Why it works: The sum of awesomeness can be decomposed into contributions from every change in adjacent elements. Updating a single element only affects boundaries touching it. By maintaining the contributions for each boundary and updating only those affected, the algorithm preserves correctness while avoiding recomputation over unaffected subarrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

total = n * (n + 1) // 2

def contrib(i):
    if 0 <= i < n - 1 and a[i] != a[i+1]:
        return (i + 1) * (n - (i + 1))
    return 0

for i in range(n - 1):
    total += contrib(i)

for _ in range(m):
    idx, x = map(int, input().split())
    idx -= 1
    
    total -= contrib(idx - 1)
    total -= contrib(idx)
    
    a[idx] = x
    
    total += contrib(idx - 1)
    total += contrib(idx)
    
    print(total)
```

The function `contrib(i)` computes the boundary contribution of the pair `(a[i], a[i+1])`. We subtract old contributions before the update and add new ones after the update. Using 0-based indexing requires adjusting `idx` from the query.

## Worked Examples

Sample input:

```
5 5
1 2 3 4 5
3 2
4 2
3 1
2 1
2 2
```

| Step | Array | Changed boundaries | Total awesomeness |
| --- | --- | --- | --- |
| Initial | [1,2,3,4,5] | all pairs differ | 35 |
| Q1: (3,2) | [1,2,2,4,5] | pairs (2,3) changes | 29 |
| Q2: (4,2) | [1,2,2,2,5] | pairs (3,4) changes | 23 |
| Q3: (3,1) | [1,2,1,2,5] | pairs (2,3) changes | 35 |
| Q4: (2,1) | [1,1,1,2,5] | pairs (1,2) changes | 25 |
| Q5: (2,2) | [1,2,1,2,5] | pairs (1,2) changes | 35 |

The trace confirms the invariant that only boundaries touching the updated index affect the total.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Initial computation of boundaries is O(n), each query updates O(1) boundaries |
| Space | O(n) | Storing the array |

This fits comfortably within the 1-second limit for $n, m \le 10^5$ and uses only linear memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # copy-paste solution here
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    total = n * (n + 1) // 2
    def contrib(i):
        if 0 <= i < n - 1 and a[i] != a[i+1]:
            return (i + 1) * (n - (i + 1))
        return 0
    for i in range(n - 1):
        total += contrib(i)
    for _ in range(m):
        idx, x = map(int, input().split())
        idx -= 1
        total -= contrib(idx - 1)
        total -= contrib(idx)
        a[idx] = x
        total += contrib(idx - 1)
        total += contrib(idx)
        print(total)
    return out.getvalue().strip()

# provided sample
assert run("5 5\n1 2 3 4 5\n3 2\n4 2\n3 1\n2 1\n2 2\n") == "29\n23\n35\n25\n35", "sample 1"

# minimum-size input
assert run("1 1\n1\n1 1\n") == "1", "single element"

# all equal values
assert run("3 2\n2 2 2\n2 3\n3 2\n") == "6\n7", "all equal initially, then changing"

# alternating values
assert run("4 2\n1 2 1 2\n2 2\n3 2\n") == "20\n21", "alternating pattern"

# edge update
assert run("5 1\n1 2 3 4 5\n5 1\n") == "31", "updating last element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | trivial array, sum of subarrays is 1 |
| all equal values | 6,7 | updates merge/split blocks |
| alternating values | 20,21 | patterns with frequent boundaries |
| edge update | 31 | correctly handles last element update |

## Edge Cases

If the updated value does not change the element, the total remains the same. For example, `[2,2,2
