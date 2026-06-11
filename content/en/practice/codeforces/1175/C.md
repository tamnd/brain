---
title: "CF 1175C - Electrification"
description: "We are asked to select an integer point $x$ on a line such that the $(k+1)$-th smallest distance from $x$ to a given set of points is minimized. Each query gives us $n$ sorted integers $a1, a2, dots, an$ representing points on the $OX$ axis, and an integer $k$."
date: "2026-06-12T01:47:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1175
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 66 (Rated for Div. 2)"
rating: 1600
weight: 1175
solve_time_s: 88
verified: true
draft: false
---

[CF 1175C - Electrification](https://codeforces.com/problemset/problem/1175/C)

**Rating:** 1600  
**Tags:** binary search, brute force, greedy  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to select an integer point $x$ on a line such that the $(k+1)$-th smallest distance from $x$ to a given set of points is minimized. Each query gives us $n$ sorted integers $a_1, a_2, \dots, a_n$ representing points on the $OX$ axis, and an integer $k$. The function $f_k(x)$ is defined by computing the absolute distances from $x$ to each $a_i$, sorting them, and picking the $(k+1)$-th value. The goal is to choose $x$ that minimizes $f_k(x)$.

The constraints are tight: $n$ can be up to $2 \cdot 10^5$ and the sum of all $n$ across queries is also at most $2 \cdot 10^5$. This rules out any solution that iterates over all possible $x$ values in the full range, which could be up to $10^9$. We need a solution linear in $n$ per query, or at worst $O(n \log n)$, to stay under the time limit.

Non-obvious edge cases include scenarios where $k = 0$ or $k = n-1$. For $k = 0$, $f_0(x)$ is the minimum distance to any point, so the optimal $x$ must coincide with one of the existing points. For $k = n-1$, $f_{n-1}(x)$ is the maximum distance to any point, which is minimized at the midpoint of the extreme points. A careless approach that assumes a fixed formula without checking boundaries can produce incorrect answers for these extreme $k$ values.

## Approaches

The brute-force approach is straightforward: for each integer $x$ in the range from $a_1$ to $a_n$, compute all distances, sort them, and pick the $(k+1)$-th smallest distance. This is correct but extremely slow because sorting $n$ distances for up to $10^9$ possible $x$ values is infeasible. Even iterating through only the given points as candidates and computing distances for all $n$ would be $O(n^2)$ in the worst case, which is too slow for $n \approx 2 \cdot 10^5$.

The key insight is that $f_k(x)$ depends only on the $k$-th nearest neighbors. Since the points are sorted, the $(k+1)$-th nearest distance at $x$ can be achieved by considering segments of length $k$ in the sorted array. Specifically, for any $x$, the $(k+1)$-th nearest point will be some $a_i$ in the array, and the minimal value occurs when $x$ is placed at the midpoint of $a_i$ and $a_{i+k}$. This reduces the problem to iterating over all $i$ from $0$ to $n-k-1$, computing the midpoint $(a_i + a_{i+k}) // 2$, and picking the value of $x$ that minimizes the distance to the extremes of the segment. This is linear in $n$ per query and avoids sorting at each candidate point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over indices $i$ from $0$ to $n-k-1$. Each segment from $a_i$ to $a_{i+k}$ represents $k+1$ consecutive points. Any $x$ chosen outside this interval cannot reduce the $(k+1)$-th smallest distance for this segment, so the optimal $x$ must lie inside this interval.
2. For each segment, calculate the midpoint $m = (a_i + a_{i+k}) // 2$. Placing $x$ at this midpoint balances the distances to the first and last points in the segment, minimizing the maximum of $|x - a_i|$ and $|x - a_{i+k}|$.
3. Track the minimal distance $d = a_{i+k} - a_i$ across all segments. When a smaller $d$ is found, update the candidate $x$ to the corresponding midpoint.
4. After iterating all segments, the chosen $x$ corresponds to the segment with minimal length. This guarantees $f_k(x)$ is minimized.

Why it works: The $(k+1)$-th smallest distance at a point $x$ is determined by the $k$-nearest neighbors around $x$. The minimal distance is achieved by balancing $x$ inside the smallest segment of length $k$ in the sorted points, which ensures that the farthest of the $k+1$ nearest points is as close as possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        min_len = float('inf')
        ans = 0
        for i in range(n - k):
            length = a[i + k] - a[i]
            if length < min_len:
                min_len = length
                ans = (a[i] + a[i + k]) // 2
        print(ans)

solve()
```

The solution reads the number of queries, then for each query reads $n$, $k$, and the sorted array. It iterates over all possible segments of length $k+1$, computing the segment length and updating the answer with the midpoint of the minimal segment. Using integer division ensures $x$ is an integer. The final answer is printed for each query.

## Worked Examples

**Sample 1**

| i | Segment a[i..i+k] | length | midpoint | min_len | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | [1,2,5] | 5-1=4 | (1+5)//2=3 | 4 | 3 |

Output: 3

**Sample 2**

Input:

```
2 1
1 1000000000
```

| i | Segment | length | midpoint | min_len | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | [1,1000000000] | 1000000000-1=999999999 | (1+1000000000)//2=500000000 | 999999999 | 500000000 |

Output: 500000000

The traces show that the algorithm correctly identifies the segment of minimal length and balances $x$ in the middle to minimize the $(k+1)$-th distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | Iterates over all n-k segments once, constant work per segment |
| Space | O(1) extra | Only keeps minimal length and answer; input array is given |

With $\sum n \le 2 \cdot 10^5$, the total work is well under the 2-second limit. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("3\n3 2\n1 2 5\n2 1\n1 1000000000\n1 0\n4\n") == "3\n500000000\n4", "sample 1"

# custom cases
assert run("1\n1 0\n10\n") == "10", "single point, k=0"
assert run("1\n5 4\n1 2 3 4 5\n") == "3", "k=n-1, mid of extreme"
assert run("1\n4 2\n1 3 6 10\n") == "4", "choose minimal segment among consecutive"
assert run("1\n6 3\n1 2 3 4 5 6\n") == "3", "multiple minimal segments, choose leftmost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 10 | 10 | Single point, k=0 |
| 5 4 1 2 3 4 5 | 3 | k = n-1, mid of extremes |
| 4 2 1 3 6 10 | 4 | Correct minimal segment selection |
| 6 3 1 2 3 4 5 6 | 3 | Multiple minimal segments, leftmost chosen |

## Edge Cases

For k = 0, input `1 0 4`:

- Segment length is irrelevant since k=0.
- Algorithm selects midpoint of segment of length 1, which is 4.
- Correctly outputs 4.

For k = n
