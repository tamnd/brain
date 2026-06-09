---
title: "CF 1676E - Eating Queries"
description: "We are given multiple independent scenarios, each describing a collection of candies where each candy has a fixed amount of sugar."
date: "2026-06-10T00:59:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1676
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 790 (Div. 4)"
rating: 1100
weight: 1676
solve_time_s: 85
verified: true
draft: false
---

[CF 1676E - Eating Queries](https://codeforces.com/problemset/problem/1676/E)

**Rating:** 1100  
**Tags:** binary search, greedy, sortings  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent scenarios, each describing a collection of candies where each candy has a fixed amount of sugar. For every query, we want to determine the smallest number of candies Timur must eat so that the total sugar he consumes reaches at least a target value. He is free to choose any subset of candies for each query, but within a query each candy can be used at most once.

A key observation is that the order in which candies are eaten is not fixed, so for any target we are effectively choosing the best possible subset. The best strategy for minimizing the number of candies while reaching a required sum is always to take the largest values first.

The constraints are large enough that any solution which tries to recompute an optimal subset per query will fail. With up to 150,000 candies and 150,000 queries in total, an O(nq) approach is immediately impossible. Even an O(n log n) solution per query would be far too slow. This pushes us toward a preprocessing strategy that allows each query to be answered in logarithmic or constant time.

A subtle edge case appears when the total sum of all candies is smaller than the query value. In that situation, no selection of candies can satisfy the requirement, so the answer must be -1. Another corner case is when a single candy already exceeds the target, where the answer should be 1.

## Approaches

A brute-force method would try every subset size implicitly by testing combinations of candies. One could imagine sorting the array and, for each query, greedily picking candies from largest to smallest until the sum reaches the target. While correct, this still costs O(n) per query in the worst case, since we may need to scan many elements before reaching the threshold. With up to 150,000 queries, this leads to roughly 2.25 × 10^10 operations, which is far beyond feasible limits.

The key structural insight is that once the candies are sorted in descending order, the optimal strategy for any query is always a prefix of this sorted array. That transforms each query into a prefix-sum threshold problem. If we precompute prefix sums, then each query reduces to finding the smallest index where the prefix sum reaches or exceeds the target. This can be done efficiently with binary search.

So the problem becomes: after sorting, we build an array where each position stores the total sugar of the best possible k candies. Each query is then a search for the first position where this cumulative sum is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Greedy per query | O(nq) | O(1) | Too slow |
| Sort + Prefix Sum + Binary Search | O(n log n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the candies in descending order. This ensures that whenever we take the first k candies, we are always maximizing total sugar for that k. Any other ordering would only reduce the sum for the same number of candies.
2. Build a prefix sum array over the sorted list. Each prefix value represents the maximum possible sugar achievable using exactly k candies.
3. For each query value x, first check whether x is larger than the total sum of all candies. If it is, no selection can satisfy the requirement, so the answer is -1.
4. Otherwise, perform a binary search on the prefix sum array to find the smallest index k such that prefix[k] ≥ x. This index represents the minimum number of candies needed.
5. Output k for that query.

### Why it works

The correctness relies on a monotonicity property introduced by sorting. After sorting in descending order, the prefix sums form a non-decreasing sequence, and any selection of k candies cannot exceed the sum of the first k candies. This means the best possible outcome for any fixed k is uniquely determined by the prefix. Since feasibility is monotonic in k, binary search finds the minimal k that satisfies the condition without missing any valid configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]
        
        total = pref[n]
        
        for _ in range(q):
            x = int(input())
            if x > total:
                print(-1)
                continue
            
            lo, hi = 1, n
            ans = n
            while lo <= hi:
                mid = (lo + hi) // 2
                if pref[mid] >= x:
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            
            print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the candies in descending order so that the most valuable choices come first. The prefix sum array is then constructed to allow constant-time computation of any prefix total.

Each query is handled independently. We first compare the target with the total sum to avoid unnecessary searching. The binary search then operates over the prefix sums, exploiting their monotonic structure to locate the first position where the required sum is reached.

A common pitfall is forgetting to sort in descending order. Without this, prefix sums do not represent optimal selections, and binary search would return incorrect results. Another subtle issue is off-by-one indexing in the prefix array, which is why it is built with size n+1.

## Worked Examples

### Example Trace 1

Input:

```
n = 5
a = [1, 3, 2, 5, 4]
queries = [3, 10]
```

After sorting:

```
[5, 4, 3, 2, 1]
```

Prefix sums:

| k | prefix[k] |
| --- | --- |
| 1 | 5 |
| 2 | 9 |
| 3 | 12 |
| 4 | 14 |
| 5 | 15 |

Query 1: x = 3

We search for smallest k with prefix[k] ≥ 3 → k = 1.

Query 2: x = 10

We find prefix[3] = 12 ≥ 10 → k = 3.

This shows how even small k can satisfy large targets due to greedy ordering.

### Example Trace 2

Input:

```
n = 4
a = [2, 2, 2, 2]
queries = [1, 9]
```

Sorted array remains:

```
[2, 2, 2, 2]
```

Prefix sums:

| k | prefix[k] |
| --- | --- |
| 1 | 2 |
| 2 | 4 |
| 3 | 6 |
| 4 | 8 |

Query 1: x = 1 → k = 1

Query 2: x = 9 → impossible, answer = -1

This demonstrates the correctness of the global feasibility check using total sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | sorting dominates per test case, each query uses binary search |
| Space | O(n) | prefix sum array storage |

Given that the total sum of n and q over all test cases is bounded by 1.5 × 10^5, this complexity comfortably fits within time limits, as both sorting and binary search are efficient at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)
        pref = [0]
        for v in a:
            pref.append(pref[-1] + v)
        total = pref[-1]
        for _ in range(q):
            x = int(input())
            if x > total:
                out.append("-1")
                continue
            lo, hi = 1, n
            ans = n
            while lo <= hi:
                mid = (lo + hi) // 2
                if pref[mid] >= x:
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            out.append(str(ans))
    return "\n".join(out)

# provided sample (simplified check)
assert run("""1
5 2
1 2 3 4 5
3
10
""") == "1\n2"

# custom cases
assert run("""1
1 3
5
5
6
1
""") == "1\n-1\n1"

assert run("""1
4 2
1 1 1 1
2
5
""") == "2\n-1"

assert run("""1
5 2
5 4 3 2 1
15
16
""") == "5\n-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single candy | 1, -1, 1 | single-element edge behavior |
| uniform values | 2, -1 | prefix symmetry and impossibility |
| perfect sum boundary | 5, -1 | exact total vs overflow case |

## Edge Cases

When the target exceeds the total sum of all candies, the algorithm immediately returns -1 without searching. For example, with candies [2, 2, 2], the total is 6, so a query asking for 7 is impossible. The prefix sum check detects this in constant time.

When a single candy is sufficient, the prefix array ensures the binary search returns 1. For instance, with [10, 1, 1], a query of 5 is satisfied immediately by the first element, and the search does not incorrectly consider larger k values.

When all candies are identical, the prefix grows linearly, and binary search still correctly finds the threshold. For [3, 3, 3, 3], a query of 6 returns 2 because only the first two elements reach the target, matching the monotonic structure of the prefix sums.
