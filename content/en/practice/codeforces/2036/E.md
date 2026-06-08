---
title: "CF 2036E - Reverse the Rivers"
description: "We are given a world with n countries, each divided into k regions, where each region has an initial water value a[i][j]. The sages have built channels so that water in a region flows downstream through countries in the same region index."
date: "2026-06-08T10:21:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2036
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 984 (Div. 3)"
rating: 1600
weight: 2036
solve_time_s: 124
verified: true
draft: false
---

[CF 2036E - Reverse the Rivers](https://codeforces.com/problemset/problem/2036/E)

**Rating:** 1600  
**Tags:** binary search, constructive algorithms, data structures, greedy  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a world with `n` countries, each divided into `k` regions, where each region has an initial water value `a[i][j]`. The sages have built channels so that water in a region flows downstream through countries in the same region index. After this redistribution, the water value of region `j` in country `i` becomes the cumulative bitwise OR of all values in that region from country 1 to `i`. Formally, `b[i][j] = a[1][j] | a[2][j] | ... | a[i][j]`.

Queries are collections of requirements for regions. Each requirement specifies a region, a comparison operator (`<` or `>`), and a threshold. We are asked to find the earliest country (smallest index) that satisfies all requirements in the query, or `-1` if no country fits.

The constraints tell us `n*k <= 10^5` and the total number of query requirements across all queries is also at most `10^5`. This means we cannot afford a naive approach that checks every country against every requirement per query, as the worst case would be `O(n*q*k)` operations which could reach `10^10`. We need to preprocess the cumulative OR values and leverage fast lookups for each query.

A subtle edge case arises when multiple requirements on the same region contradict each other, for example, `r > 5` and `r < 3` in the same query. Careless code could select a country that satisfies one but not both requirements. Another edge case is when the cumulative OR reaches its maximum value early, making later comparisons trivial.

## Approaches

The brute-force solution would calculate the cumulative OR for every country and region. For each query, we would iterate over all countries, check each requirement, and stop at the first country that satisfies all. This works because it correctly simulates the problem rules, but it fails at scale. With `n = 10^5`, `k = 10^5`, and queries up to `10^5`, the total operations could easily exceed `10^10`.

The key insight is that the cumulative OR array `b` is monotone non-decreasing per bit: once a bit becomes 1, it stays 1 for all subsequent countries. This allows us to precompute for each region the earliest country where `b[i][j]` crosses a threshold. For `<` requirements, we can track the last country where the value is strictly less than the threshold. For `>` requirements, we track the first country exceeding the threshold. By storing these indices, each query reduces to computing the maximum of the "first exceeding" indices for `>` constraints and the minimum of the "last below" indices for `<` constraints. If the maximum index is less than or equal to the minimum index, the answer exists; otherwise, it does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n_k + q_n*k) | O(n*k) | Too slow |
| Optimal | O(n*k + total_requirements) | O(n*k) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `b` of size `n x k` to store cumulative OR values. For each region `j`, set `b[0][j] = a[0][j]`.
2. For each country `i` from 1 to `n-1` and each region `j`, compute `b[i][j] = b[i-1][j] | a[i][j]`. This precomputes the water distribution.
3. For each query, initialize two pointers `l = 1` and `r = n` representing the feasible country range.
4. Iterate over the requirements of the query. For a requirement `(region, operator, value)`:

- If the operator is `>`, perform a binary search on `b[:,region]` to find the first country index `idx` where `b[idx][region] > value`. Update `l = max(l, idx+1)`.
- If the operator is `<`, perform a binary search to find the first country index `idx` where `b[idx][region] >= value`. Update `r = min(r, idx)`.
5. After processing all requirements, if `l <= r`, output `l` as the smallest suitable country index. Otherwise, output `-1`.

Why it works: the precomputed cumulative OR arrays are non-decreasing per region, so binary search correctly identifies the threshold crossing points. By intersecting the feasible intervals across all requirements, we ensure the selected country satisfies every constraint.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n, k, q = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

# compute cumulative OR for each region
b = [a[0][:]]
for i in range(1, n):
    b.append([b[i-1][j] | a[i][j] for j in range(k)])

# transpose for easier access per region
b_cols = list(zip(*b))

for _ in range(q):
    m = int(input())
    l, r = 0, n-1  # 0-based indexing
    requirements = []
    for _ in range(m):
        r_idx, op, c = input().split()
        r_idx = int(r_idx)-1
        c = int(c)
        requirements.append((r_idx, op, c))
    
    for r_idx, op, c in requirements:
        col = b_cols[r_idx]
        if op == '>':
            idx = bisect.bisect_right(col, c)
            l = max(l, idx)
        else:  # '<'
            idx = bisect.bisect_left(col, c)
            r = min(r, idx-1)
    if l <= r:
        print(l+1)
    else:
        print(-1)
```

This code first computes cumulative ORs in `b` and then transposes it into `b_cols` for column-wise access. We use Python's `bisect` to find threshold crossings efficiently. `l` and `r` represent the feasible range of countries; after processing all requirements, we check if a valid country exists.

## Worked Examples

**Sample Input 1**

```
3 4 4
1 3 5 9
4 6 5 3
2 1 2 7
3
1 > 4
2 < 8
1 < 6
2
1 < 8
2 > 8
1
3 > 5
2
4 > 8
1 < 8
```

| Country | Region 1 | Region 2 | Region 3 | Region 4 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 5 | 9 |
| 2 | 5 | 7 | 5 | 11 |
| 3 | 7 | 7 | 7 | 15 |

Query 1 requirements: `(1 > 4)`, `(2 < 8)`, `(1 < 6)`

Binary search yields feasible country index 1 (0-based) → output `2`.

Query 2: `(1 < 8)`, `(2 > 8)`

No country satisfies both → output `-1`.

Query 3: `(3 > 5)`

First country satisfying → country 3 → output `3`.

Query 4: `(4 > 8)`, `(1 < 8)`

First country satisfying → country 1 → output `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*k + total_requirements * log n) | Precompute cumulative ORs takes `n*k`. Each requirement binary search is O(log n). Total requirements <= 1e5. |
| Space | O(n*k) | Store cumulative OR arrays. |

This fits within the 2s time limit given the constraints, as `n*k <= 1e5` and total requirements `<= 1e5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    exec(open("solution.py").read(), globals())
    return output.getvalue().strip()

# Provided sample
assert run("""3 4 4
1 3 5 9
4 6 5 3
2 1 2 7
3
1 > 4
2 < 8
1 < 6
2
1 < 8
2 > 8
1
3 > 5
2
4 > 8
1 < 8""") == "2\n-1\n3\n1"

# Custom case: all equal values
assert run("""2 2 1
5 5
5 5
2
1 > 4
2 < 6""") == "1"

# Custom case: no suitable country
assert run("""2 2 1
1 2
3 4
2
1 > 10
2 < 1""") == "-1"

# Custom case: minimum input
assert run("""1 1 1
1
1
1 > 0""") == "1"

# Custom case: multiple options, pick smallest
```
