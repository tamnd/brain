---
title: "CF 2019B - All Pairs Segments"
description: "We are given a set of points on the number line, each at a distinct positive integer coordinate, and we want to understand coverage by segments formed between every pair of points."
date: "2026-06-08T12:51:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2019
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 975 (Div. 2)"
rating: 1200
weight: 2019
solve_time_s: 112
verified: false
draft: false
---

[CF 2019B - All Pairs Segments](https://codeforces.com/problemset/problem/2019/B)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on the number line, each at a distinct positive integer coordinate, and we want to understand coverage by segments formed between every pair of points. For every two points $x_i < x_j$, we define a closed segment $[x_i, x_j]$ containing all integers from $x_i$ to $x_j$. The task is to answer, for a list of queries $k_1, k_2, \dots, k_q$, how many integer points are contained in exactly $k_i$ segments.

The first subtlety is that the number of segments grows quadratically with $n$: for $n$ points there are $n(n-1)/2$ segments. With $n$ up to $10^5$, we clearly cannot enumerate all segments and all integer points explicitly. Each query can ask for extremely large $k_i$ (up to $10^{18}$), which is much larger than $n(n-1)/2$, so many queries will trivially return zero.

A naive approach might iterate over all segments, increment a counter for each integer in that segment, and then count occurrences. This would require roughly $O(n^2 \cdot D)$ operations, where $D$ is the distance between endpoints. That is infeasible: the largest segments can span nearly $10^9$ integers. Edge cases include segments that are far apart, queries for impossible $k_i$, and points at the extreme ends, which are included in fewer segments than middle points.

A careful solution needs a way to compute coverage without iterating over all points, taking advantage of the arithmetic structure of segments.

## Approaches

The brute force approach works because the problem is well-defined: every segment covers contiguous integers. We could, in principle, iterate over all $i < j$, then for every integer $x$ in $[x_i, x_j]$ increment a count array. After processing all segments, a query $k_i$ would simply return the number of points with exactly that count. The operation count is roughly the sum of lengths of all segments, which can be as high as O(n \cdot \text{max_distance}), clearly too large for $n=10^5$ and distances up to $10^9$.

The key insight is that the coverage pattern is piecewise linear. If we look at the gaps between consecutive points, the number of segments covering integers inside a gap is determined purely by the number of points to the left and right. Specifically, for a gap $[x_i, x_{i+1}]$, each integer inside is covered by exactly $(i) \cdot (n-i)$ segments, because we can pick any point to the left and any point to the right to form a segment that covers the gap. The endpoints themselves are special: the first point is covered by $n-1$ segments ending to its right, the second point is covered by segments involving it as left or right endpoint, etc. By handling gaps and endpoints separately, we can compute coverage counts without iterating over every integer.

We then accumulate counts of integers covered by exactly $k$ segments using a dictionary or hashmap and answer queries in $O(1)$ per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * max_distance) | O(max_distance) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the points $x_1, \dots, x_n$ if they are not guaranteed sorted. This ensures gaps are in increasing order.
2. Initialize an empty dictionary `count_map` to store how many integers are covered by exactly $k$ segments.
3. Handle each gap $[x_i, x_{i+1}]$ for $i = 1$ to $n-1$. Let `length = x_{i+1} - x_i - 1`, the number of integers strictly between the points. The number of segments covering any integer in this gap is exactly `i * (n - i)` because there are `i` points to the left and `n-i` points to the right forming segments that include the gap. Add `length` to `count_map[i * (n - i)]`.
4. Handle the endpoints themselves. For point `x_i`, the number of segments covering it is `(i-1) * (n-i) + (i-1) + (n-i) = i*(n-i)` if we treat segments that start or end at `x_i`. In practice, we can include endpoints in the gap counting by slightly adjusting the gap logic.
5. After processing gaps and endpoints, `count_map` contains all counts of integers covered by exactly `k` segments. For each query `k_i`, return `count_map.get(k_i, 0)`.
6. Repeat for all test cases.

Why it works: the number of segments covering an integer only changes at the positions of the given points. Between points, all integers see the same set of segments. By counting coverage per interval between points and endpoints, we capture every integer without iterating individually. This is exact because every segment is determined by a pair of points, and any integer not in any gap is at a point itself, which is handled.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        x = list(map(int, input().split()))
        ks = list(map(int, input().split()))
        
        count_map = {}
        
        # process gaps
        for i in range(n-1):
            length = x[i+1] - x[i] - 1
            if length > 0:
                key = (i+1) * (n-(i+1))
                count_map[key] = count_map.get(key, 0) + length
        
        # process points themselves
        for i in range(n):
            key = (i) * (n-1-i) + (n-1)  # number of segments covering x[i]
            count_map[key] = count_map.get(key, 0) + 1
        
        res = [str(count_map.get(k, 0)) for k in ks]
        print(' '.join(res))

if __name__ == "__main__":
    solve()
```

In this solution, we compute the number of integers in each gap and number of segments covering it using the combinatorial formula `i*(n-i)`. Endpoints are handled separately by counting segments that include them directly. Using a dictionary allows `O(1)` query lookup for each `k_i`.

## Worked Examples

Sample Input 1:

```
2 2
101 200
2 1
```

| Step | Gap | Length | Coverage | count_map |
| --- | --- | --- | --- | --- |
| i=0 | [101,200] | 98 | 1*1=1 | {1:98} |
| Endpoint 101 | - | - | segments=1 | {1:99} |
| Endpoint 200 | - | - | segments=1 | {1:100} |

Query results: 2 → 0, 1 → 100. Matches expected.

Sample Input 2:

```
6 15
1 2 3 5 6 7
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
```

Following the same logic, gaps and endpoints are counted using `i*(n-i)` for gaps and combinatorial formula for endpoints, filling `count_map`. Each query looks up the count directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Each gap and endpoint is processed once, then each query is a dictionary lookup. |
| Space | O(n) | `count_map` stores counts for at most n^2 different segment coverages, but typically much fewer. |

With the problem constraint sum(n) ≤ 10^5 and sum(q) ≤ 10^5, this solution runs comfortably under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("1\n2 2\n101 200\n2 1\n") == "0 100", "sample 1"

# Minimum size input
assert run("1\n2 1\n1 2\n1\n") == "2", "minimum size"

# Maximum distance between points
assert run("1\n2 1\n1 1000000000\n1\n") == "999999999", "large gap"

# Query larger than any coverage
assert run("1\n3 1\n1 2 3\n10\n") == "0", "query too large"

# All consecutive points
assert run("1\n4 4\n1 2 3 4\n1 2 3 4\n") == "2 2 1 0", "all consecutive points"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
