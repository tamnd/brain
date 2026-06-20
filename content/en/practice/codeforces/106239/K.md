---
title: "CF 106239K - \u7ebf\u6bb5\u8986\u76d6"
description: "We are given a sorted list of distinct points on a number line. The task is to cover all these points using at most $k$ segments, where a segment can be any interval $[a,b]$ and its cost is its geometric length $ A useful way to reframe the problem is to think of grouping points."
date: "2026-06-20T09:06:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106239
codeforces_index: "K"
codeforces_contest_name: "2025\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66\u65b0\u751f\u8d5b(\u51b3\u8d5b)"
rating: 0
weight: 106239
solve_time_s: 46
verified: true
draft: false
---

[CF 106239K - \u7ebf\u6bb5\u8986\u76d6](https://codeforces.com/problemset/problem/106239/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted list of distinct points on a number line. The task is to cover all these points using at most $k$ segments, where a segment can be any interval $[a,b]$ and its cost is its geometric length $|a-b|$. A segment covers a point if the point lies between its endpoints. The goal is to minimize the total length of all chosen segments, and we must report the optimal value for every $k$ from 1 to $n$.

A useful way to reframe the problem is to think of grouping points. If we decide to cover a consecutive group of points $x_l, x_{l+1}, \dots, x_r$ with one segment, the cheapest possible segment is exactly $[x_l, x_r]$, and its cost is $x_r - x_l$. Any optimal solution will always use segments that cover contiguous blocks of the sorted array, because any segment spanning non-contiguous points can be shortened without losing coverage.

The constraints allow up to $2 \times 10^5$ points, which immediately rules out any solution that tries all partitions or uses $O(n^2)$ dynamic programming transitions directly. We need something closer to linear or $O(n \log n)$, and we also need answers for all $k$, which suggests building a global structure once rather than recomputing per $k$.

A subtle point appears when thinking about $k=1$. The only segment must cover all points, so the answer is $x_n - x_1$. For larger $k$, we are effectively allowed to split the array into multiple segments, paying only for the spans inside each segment.

A naive approach might try all ways to split the array into $k$ groups for each $k$, but that leads to combinatorial explosion. Even computing a single $k$-partition optimally with DP costs $O(n^2 k)$ or $O(n^2)$, which is too large.

## Approaches

The key observation is that splitting a segment reduces cost in a very structured way. If we cover all points with one segment, the cost is $x_n - x_1$. Suppose we insert a split between $x_i$ and $x_{i+1}$. Instead of one segment $[x_1, x_n]$, we now use two segments $[x_1, x_i]$ and $[x_{i+1}, x_n]$. The new cost becomes

$$(x_i - x_1) + (x_n - x_{i+1})$$

compared to

$$x_n - x_1.$$

The difference is

$$(x_n - x_1) - [(x_i - x_1) + (x_n - x_{i+1})] = x_{i+1} - x_i.$$

This means every possible split between adjacent points has a “saving” equal to the gap between them. A split removes that gap from the total cost because the segment no longer spans across it.

So the problem becomes equivalent to this: we start with cost $x_n - x_1$, and we are allowed to insert up to $k-1$ splits. Each split at position $i$ gives a gain of $x_{i+1} - x_i$. To minimize total cost, we want to maximize the sum of chosen gains, which is achieved by picking the largest gaps.

Thus, for each $k$, the optimal strategy is to choose the $k-1$ largest adjacent gaps and subtract their sum from $x_n - x_1$.

This reduces the problem to sorting gaps once and computing prefix sums, after which each answer is a simple subtraction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over partitions | $O(n^2)$ or worse | $O(n)$ | Too slow |
| Sort gaps + prefix sums | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute all adjacent differences $d_i = x_{i+1} - x_i$ for $i = 1$ to $n-1$.

These represent the savings obtained if we decide to split between those two points, since a split removes that gap from being covered by a single segment.
2. Sort the array $d$ in descending order.

We want to prioritize the largest savings first because each split is independent and contributes additively to the total improvement.
3. Build a prefix sum array over the sorted gaps, where `pref[i]` is the sum of the largest $i$ gaps.

This allows us to answer any $k$ efficiently without recomputing sums.
4. Initialize the base cost as $x_n - x_1$, which corresponds to covering everything with a single segment.
5. For each $k$ from 1 to $n$, output:

$$(x_n - x_1) - \text{pref}[k-1]$$

because using $k$ segments means inserting exactly $k-1$ splits.

Why it works

Every valid segmentation corresponds to choosing a subset of gaps where cuts are placed. Each cut removes exactly one adjacent gap from being included in a spanning segment. Since gaps are independent and do not interact, the total improvement is additive. The optimal solution is therefore obtained by selecting the largest $k-1$ improvements, which is exactly what sorting guarantees. No alternative structure can yield a larger reduction because any rearrangement of cuts does not change the multiset of chosen gaps, only which ones are included.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
x = list(map(int, input().split()))

if n == 1:
    print(0)
    sys.exit()

gaps = [x[i+1] - x[i] for i in range(n - 1)]
gaps.sort(reverse=True)

pref = [0] * (n)
for i, v in enumerate(gaps, start=1):
    pref[i] = pref[i - 1] + v

base = x[-1] - x[0]

ans = []
for k in range(1, n + 1):
    ans.append(str(base - pref[k - 1]))

print(" ".join(ans))
```

The implementation directly mirrors the transformation from segment partitioning to selecting gaps. The only care needed is indexing: there are $n-1$ gaps but answers require $k-1$ of them, so prefix array is built with length $n$ to safely include the zero case.

The base cost is computed once, and every query is a constant-time subtraction.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

Gaps are $[1, 1]$, sorted as $[1, 1]$, prefix sums $[0, 1, 2]$. Base cost is $3 - 1 = 2$.

| k | chosen gaps | sum | answer |
| --- | --- | --- | --- |
| 1 | none | 0 | 2 |
| 2 | 1 gap | 1 | 1 |
| 3 | 2 gaps | 2 | 0 |

Output:

```
2 1 0
```

This shows that each additional segment removes one boundary gap, gradually reducing total cost to zero when every point is isolated.

### Example 2

Input:

```
4
1 3 6 10
```

Gaps are $[2, 3, 4]$, sorted $[4, 3, 2]$, prefix sums $[0, 4, 7, 9]$. Base cost is $9$.

| k | chosen gaps | sum | answer |
| --- | --- | --- | --- |
| 1 | none | 0 | 9 |
| 2 | 4 | 4 | 5 |
| 3 | 4,3 | 7 | 2 |
| 4 | 4,3,2 | 9 | 0 |

This trace highlights that optimal segmentation always cuts at the largest separations first, producing the most balanced cost reduction per additional segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the $n-1$ gaps dominates the runtime |
| Space | $O(n)$ | Storage for gaps and prefix sums |

The solution comfortably fits the constraints since $n \le 2 \times 10^5$, and sorting plus linear prefix computation is well within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input().strip())
    x = list(map(int, input().split()))

    if n == 1:
        return "0"

    gaps = [x[i+1] - x[i] for i in range(n - 1)]
    gaps.sort(reverse=True)

    pref = [0] * (n)
    for i, v in enumerate(gaps, start=1):
        pref[i] = pref[i - 1] + v

    base = x[-1] - x[0]

    ans = []
    for k in range(1, n + 1):
        ans.append(str(base - pref[k - 1]))

    return " ".join(ans)

# provided samples
assert run("3\n1 2 3\n") == "2 1 0"

# minimum size
assert run("1\n100\n") == "0"

# simple spaced points
assert run("2\n1 10\n") == "9 0"

# all equal gaps
assert run("5\n1 2 3 4 5\n") == "4 3 2 1 0"

# large uneven gaps
assert run("4\n1 2 100 101\n") == "100 1 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | base case handling |
| two distant points | 9 0 | single gap behavior |
| uniform spacing | 4 3 2 1 0 | consistent greedy reduction |
| mixed large gap | 100 1 0 0 | correctness of sorting gaps |

## Edge Cases

For a single point, the algorithm produces no gaps and directly outputs zero, since base cost is zero and no splits are needed.

For example input:

```
1
42
```

The gap list is empty, prefix sums are all zero, and every $k$ returns zero. The algorithm never attempts to access invalid indices because the prefix array is sized to $n$, and $k-1$ ranges safely from 0 to 0.

For closely packed points such as:

```
3
10 11 12
```

gaps are $[1,1]$, and the algorithm selects them in order. For $k=2$, one gap is removed, reducing cost from 2 to 1, matching the interpretation that a single cut removes exactly one unit of span.

For highly unbalanced spacing such as:

```
3
1 2 100
```

gaps are $[1, 98]$. The optimal strategy for $k=2$ selects the large gap first, removing 98 from the total span, leaving only 1, which matches splitting at the dominant separation.
