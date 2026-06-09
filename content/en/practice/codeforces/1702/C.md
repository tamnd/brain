---
title: "CF 1702C - Train and Queries"
description: "We are given a train route along stations with very large indices, from 1 to $10^9$. The train travels in the exact order of a list $u1, u2, dots, un$ and can revisit stations multiple times."
date: "2026-06-09T21:41:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1702
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 805 (Div. 3)"
rating: 1100
weight: 1702
solve_time_s: 157
verified: true
draft: false
---

[CF 1702C - Train and Queries](https://codeforces.com/problemset/problem/1702/C)

**Rating:** 1100  
**Tags:** data structures, greedy  
**Solve time:** 2m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a train route along stations with very large indices, from 1 to $10^9$. The train travels in the exact order of a list $u_1, u_2, \dots, u_n$ and can revisit stations multiple times. For each query consisting of two stations $a_j$ and $b_j$, we need to determine whether the train can carry a passenger from $a_j$ to $b_j$ along the forward direction of the route.

The challenge comes from the large range of station indices combined with potentially many queries. The constraints allow up to $2 \cdot 10^5$ stations and queries per test case, and the sum across all test cases is similarly bounded. This rules out any algorithm that iterates over the route for each query, because that could reach $2 \cdot 10^5 \times 2 \cdot 10^5 = 4 \cdot 10^{10}$ operations, far too large for a 3-second limit.

A subtlety arises with repeated stations. If $u = [1, 2, 1]$ and the query is from 2 to 1, a naive “first occurrence to last occurrence” approach might fail if it ignores the fact that 1 occurs both before and after 2. The correct solution must account for first appearances of the start station and last appearances of the end station to respect the forward direction.

Another edge case is when the start or end station is not on the route. If $a_j$ or $b_j$ does not appear in the route, the answer is automatically NO.

## Approaches

The brute-force method is simple: for each query, scan through the train route from left to right to see if you can reach $b_j$ after encountering $a_j$. This works because the route is explicitly defined, but it fails for large inputs. For the worst-case scenario of $n = k = 2 \cdot 10^5$, this requires up to $O(n \cdot k) = 4 \cdot 10^{10}$ operations, which is infeasible.

The optimal approach uses a precomputation insight. For each station index in the route, we store the first time it appears and the last time it appears. Then, for a query from $a_j$ to $b_j$, the answer is YES if the first occurrence of $a_j$ is before the last occurrence of $b_j$. This works because the train only moves forward; the first opportunity to board $a_j$ must come before the last chance to reach $b_j$.

This reduces each query to $O(1)$ lookups, and constructing the first/last occurrence dictionaries is $O(n)$. Thus, the total complexity per test case becomes $O(n + k)$, which fits comfortably within the time limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(1) | Too slow |
| Optimal | O(n + k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and $k$, the route length and number of queries.
2. Read the train route $u$. Initialize two dictionaries: `first_occurrence` and `last_occurrence`. Iterate through $u$ with index $i$. For each station $x = u[i]$, if $x$ is not yet in `first_occurrence`, set it to $i$. Always update `last_occurrence[x] = i\`.
3. For each query $a_j, b_j$, check if both stations exist in the route. If either is missing, print NO. Otherwise, compare indices: if `first_occurrence[a_j] <= last_occurrence[b_j]`, print YES; otherwise, print NO.

Why it works: the algorithm maintains the invariant that `first_occurrence[x]` is the earliest point where you can board station $x$ and `last_occurrence[y]` is the latest point you can exit at station $y$. If the first opportunity to board $a_j$ comes after the last opportunity to reach $b_j$, the train cannot carry a passenger from $a_j$ to $b_j$ in the forward direction. Otherwise, it can.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    input()  # blank line
    n, k = map(int, input().split())
    u = list(map(int, input().split()))
    
    first_occurrence = {}
    last_occurrence = {}
    
    for i, station in enumerate(u):
        if station not in first_occurrence:
            first_occurrence[station] = i
        last_occurrence[station] = i
    
    for _ in range(k):
        a, b = map(int, input().split())
        if a not in first_occurrence or b not in last_occurrence:
            print("NO")
        elif first_occurrence[a] <= last_occurrence[b]:
            print("YES")
        else:
            print("NO")
```

The solution first precomputes the first and last occurrences for each station. This avoids scanning the route repeatedly for each query. Checking existence in the dictionaries also handles the case where a station does not appear in the route.

## Worked Examples

**Test Case 1:**

Route: `[3, 7, 1, 5, 1, 4]`

Queries: `(3, 5), (1, 7), (3, 10)`

| Station | First | Last |
| --- | --- | --- |
| 3 | 0 | 0 |
| 7 | 1 | 1 |
| 1 | 2 | 4 |
| 5 | 3 | 3 |
| 4 | 5 | 5 |

Query 1: `3 -> 5` → first_occ[3] = 0, last_occ[5] = 3 → YES

Query 2: `1 -> 7` → first_occ[1] = 2, last_occ[7] = 1 → NO

Query 3: `3 -> 10` → 10 not in route → NO

**Test Case 2:**

Route: `[1, 2, 1]`

Queries: `(2, 1), (1, 2), (4, 5)`

| Station | First | Last |
| --- | --- | --- |
| 1 | 0 | 2 |
| 2 | 1 | 1 |

Query 1: `2 -> 1` → first_occ[2] = 1, last_occ[1] = 2 → YES

Query 2: `1 -> 2` → first_occ[1] = 0, last_occ[2] = 1 → YES

Query 3: `4 -> 5` → 4 missing → NO

This shows that repeated stations are handled correctly and that queries with missing stations are rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) per test case | Building first/last occurrence maps takes O(n), answering k queries is O(k) |
| Space | O(n) | We store first and last occurrence for each unique station in the route |

Given that the sum of n and k over all test cases does not exceed $2 \cdot 10^5$, the solution easily runs under 3 seconds with low memory overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read(), globals())
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided sample
assert run("3\n\n6 3\n3 7 1 5 1 4\n3 5\n1 7\n3 10\n\n3 3\n1 2 1\n2 1\n1 2\n4 5\n\n7 5\n2 1 1 1 2 4 4\n1 3\n1 4\n2 1\n4 1\n1 2") == \
"""YES
NO
NO
YES
YES
NO
NO
YES
YES
NO
YES"""

# Minimum size input
assert run("1\n\n1 1\n1\n1 1") == "YES"

# All equal stations
assert run("1\n\n4 2\n2 2 2 2\n2 2\n2 3") == "YES\nNO"

# Maximum k with repeated first/last
assert run("1\n\n5 3\n1 2 3 2 1\n1 3\n2 2\n3 1") == "YES\nYES\nNO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n\n1 1\n1\n1 1` | YES | Minimum input edge case |
| `1\n\n4 2\n2 2 2 2\n2 2\n2 |  |  |
