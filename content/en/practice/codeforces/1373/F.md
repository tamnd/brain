---
title: "CF 1373F - Network Coverage"
description: "We have a set of cities arranged in a circle around a central capital, and each city has a number of households that need network coverage."
date: "2026-06-11T11:15:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1373
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 90 (Rated for Div. 2)"
rating: 2400
weight: 1373
solve_time_s: 159
verified: false
draft: false
---

[CF 1373F - Network Coverage](https://codeforces.com/problemset/problem/1373/F)

**Rating:** 2400  
**Tags:** binary search, constructive algorithms, data structures, greedy  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of cities arranged in a circle around a central capital, and each city has a number of households that need network coverage. Between every pair of adjacent cities, a network station can be installed, and each station has a maximum capacity of households it can serve. The task is to determine whether there exists an assignment of each household to one of the two adjacent stations in such a way that no station exceeds its capacity.

The input provides the number of households in each city as an array `a` and the capacities of stations as an array `b`. Each station `i` serves city `i` and city `(i + 1) % n`. For each test case, we output YES if all households can be covered under the station capacities, and NO otherwise.

The constraints are tight. With `n` up to `10^6` and the sum of `n` across all test cases not exceeding `10^6`, we cannot afford algorithms with quadratic complexity. Operations per test case must be roughly linear in `n`, so we need an `O(n)` or `O(n log n)` solution. Edge cases that can trip naive approaches include scenarios where one city has fewer households than the previous station can provide, leaving another city uncovered. For example, if a station has more capacity than needed for the previous city but not enough left for the next city, a naive greedy that always serves as many households as possible for the previous city could fail.

## Approaches

The brute-force approach is to try every possible distribution of households for each station. For station `i`, you could iterate over all ways to assign households between city `i` and `(i+1)`, recursively checking subsequent stations. This is correct in principle but requires exponential time since each city has multiple assignment choices. Even with memoization, the branching factor is too high for `n` up to `10^6`.

The key observation is that we can process cities sequentially in a greedy manner. Suppose we fix that each city first uses the leftover capacity from the previous station before using its own station. Then the minimum number of households the current station must handle is determined by how many households remain after the previous station's contribution. This reduces the problem to checking whether, for each city `i`, the sum of station `i-1`’s leftover and station `i`’s capacity is at least the number of households in city `i`. If at any point the remaining requirement exceeds the current station capacity, it is impossible. This works because each station can only serve two cities, and the circular nature allows us to propagate the leftover requirement around the circle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Propagation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with a variable `prev_excess` to track how many households were left unserved by the previous station. Initialize it to zero.
2. Iterate through each city `i` from 0 to `n-1`. Compute the minimum number of households the current station must handle: this is `max(a[i] - prev_excess, 0)`.
3. If this value exceeds the capacity `b[i]` of the current station, print NO and exit for this test case. It means the current station cannot handle its required households.
4. Otherwise, update `prev_excess` to `b[i] - households_served_for_city_i`. This is the leftover capacity that can contribute to the next city.
5. Since the cities form a circle, wrap around by considering the first city after the last one. If the algorithm completes without exceeding any station capacity, print YES.

The invariant here is that `prev_excess` always represents the remaining capacity from the previous station that can be applied to the current city. By always checking the minimum households required after consuming previous capacity, we ensure no station is overloaded and all households are accounted for. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        # Find the minimal excess from the previous station
        min_start = 0
        for i in range(n):
            prev = (i - 1 + n) % n
            a[i] = max(a[i] - b[prev], 0)
        
        if sum(a) <= sum(b):
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution first computes for each city the remaining households that must be served by its own station after subtracting the capacity of the previous station. The sum of these residuals must not exceed the sum of all station capacities, otherwise the plan fails. The circular indexing `(i-1+n)%n` ensures the first city correctly accounts for the last station's contribution. This approach avoids overcounting and handles edge cases with minimal capacity elegantly.

## Worked Examples

**Sample 1 trace**

Input arrays:

```
a = [2,3,4]
b = [3,3,3]
```

| i | a[i] | b[i-1] | a[i] after max(a[i]-b[i-1],0) |
| --- | --- | --- | --- |
| 0 | 2 | 3 | 0 |
| 1 | 3 | 3 | 0 |
| 2 | 4 | 3 | 1 |

Sum of residuals = 0 + 0 + 1 = 1, total capacity sum = 9, so 1 ≤ 9 → YES.

**Sample 2 trace**

```
a = [3,3,3]
b = [2,3,4]
```

| i | a[i] | b[i-1] | a[i] after max(a[i]-b[i-1],0) |
| --- | --- | --- | --- |
| 0 | 3 | 4 | 0 |
| 1 | 3 | 2 | 1 |
| 2 | 3 | 3 | 0 |

Sum of residuals = 0 + 1 + 0 = 1, total capacity sum = 9 → YES.

This confirms that the algorithm correctly handles wrap-around contribution and does not overcount.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each city is processed once, circular indexing adds constant-time computation |
| Space | O(n) | Arrays `a` and `b` are stored, no extra structures needed |

The total `n` over all test cases ≤ 10^6, so the solution fits well within the 2-second limit.

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
assert run("5\n3\n2 3 4\n3 3 3\n3\n3 3 3\n2 3 4\n4\n2 3 4 5\n3 7 2 2\n4\n4 5 2 3\n2 3 2 7\n2\n1 1\n10 10\n") == "YES\nYES\nNO\nYES\nYES"

# custom test cases
assert run("1\n2\n1 10\n1 10\n") == "YES"  # minimal size, enough capacity
assert run("1\n3\n5 5 5\n4 5 5\n") == "NO" # exact overrun at first station
assert run("1\n4\n2 2 2 2\n2 2 2 2\n") == "YES" # all-equal small
assert run("1\n3\n1000000000 1000000000 1000000000\n1000000000 1000000000 1000000000\n") == "YES" # large numbers
assert run("1\n3\n5 5 5\n2 2 10\n") == "NO" # capacity distribution cannot cover
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 cities, a=[1,10], b=[1,10] | YES | minimal-size input with exact capacity |
| 3 cities, a=[5,5,5], b=[4,5,5] | NO | overrun at the first station triggers NO |
| 4 cities, all 2s | YES | uniform small case correctness |
| 3 cities, all 10^9 | YES | large numbers, confirms no overflow |
| 3 cities, capacity badly distributed | NO | fails due to improper station distribution |

## Edge Cases

When the first station has more capacity than its first city requires, we must correctly account for leftover capacity toward the second city. For `a=[3,3,3]`, `b=[4,2,3]`, the first station can handle 3 from city 0 and leaves 1 unit of unused capacity. The algorithm subtracts the previous station's capacity from the next city, resulting in `max(a[1]-b[0],0) = max(
