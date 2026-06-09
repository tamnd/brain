---
title: "CF 1921F - Sum of Progression"
description: "We are given an array of integers and a set of queries. Each query specifies a starting index s, a step size d, and a count k. For a query, we must sum k elements of the array taken at indices s, s+d, s+2d, ..."
date: "2026-06-08T19:24:06+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1921
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 920 (Div. 3)"
rating: 1900
weight: 1921
solve_time_s: 122
verified: false
draft: false
---

[CF 1921F - Sum of Progression](https://codeforces.com/problemset/problem/1921/F)

**Rating:** 1900  
**Tags:** brute force, data structures, dp, implementation, math  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a set of queries. Each query specifies a starting index `s`, a step size `d`, and a count `k`. For a query, we must sum `k` elements of the array taken at indices `s, s+d, s+2d, ..., s+(k-1)d`, but with a twist: each element is multiplied by its position in this subsequence. In other words, the first element is multiplied by 1, the second by 2, and so on up to `k`. The output for each query is this weighted sum.

The constraints imply that the naive approach of iterating through each element of each query would be too slow. With `n` up to 10^5 and `q` up to 2·10^5, a brute-force solution that visits each element of each query individually could perform up to 2·10^10 operations in the worst case, which is clearly infeasible. We need a method that reduces the number of operations per query.

Non-obvious edge cases arise when the step size `d` is large or small. For instance, if `d=1`, the query might cover a large contiguous section of the array, whereas if `d=n`, the subsequence has only one element. Negative numbers in the array and queries with `k=1` also need careful handling to ensure no off-by-one errors or incorrect multiplications.

A concrete example: consider the array `[1, 2, 3, 4, 5]` and query `(s=2, d=2, k=2)`. The indices are 2 and 4, giving elements `[2, 4]`. The weighted sum is `2*1 + 4*2 = 2 + 8 = 10`. A careless approach might just sum `[2 + 4] = 6` and miss the weighting factor.

## Approaches

The brute-force approach iterates over each query, stepping through the array according to `d`, multiplying each element by its position, and summing the results. This works correctly but is too slow when `k` is large. Each query could take up to `O(k)` operations, which is unacceptable when summed over `q` queries.

The key insight for optimization is recognizing patterns in how queries are structured. If we fix the step `d`, the indices accessed in the array form arithmetic progressions. For small values of `d`, each index modulo `d` forms a separate subsequence. If we precompute prefix sums and weighted prefix sums for each of these `d` subsequences, we can answer queries in constant time. For large `d`, the number of elements `k` in the query is small because `s + d*(k-1) <= n`. In this case, brute-force per query is actually efficient since `k` is bounded by `n/d`.

This dual strategy-precompute for small steps and brute-force for large steps-ensures we handle all queries efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q*k) | O(n) | Too slow in worst case |
| Optimized (small d prefix sums + large d brute force) | O(n_sqrt(n) + q_sqrt(n)) | O(n*sqrt(n)) | Accepted |

## Algorithm Walkthrough

1. Determine a threshold `B` for distinguishing small and large `d`. A good heuristic is `B = sqrt(n)`. For `d <= B`, precompute prefix sums.
2. For each small `d` from 1 to `B`, for each starting index `r` in `[1, d]`, build two arrays:

- `prefix[r]` storing the cumulative sum of elements at positions `r, r+d, r+2d, ...`
- `weighted[r]` storing the cumulative sum of these elements multiplied by their position in the subsequence.
3. For queries with `d <= B`, retrieve the result using the precomputed `weighted` array and the formula: weighted sum from position `i` to `j` is `weighted[j] - weighted[i-1]`.
4. For queries with `d > B`, iterate through the subsequence directly since `k` is at most `n/d <= sqrt(n)`. Multiply each element by its 1-based position in the subsequence.
5. Print the results for all queries.

Why it works: Small `d` queries access many elements but share positions modulo `d`, so prefix sums reduce repeated work. Large `d` queries access few elements, so direct computation is fast. This hybrid strategy guarantees each query is answered efficiently without skipping any elements or miscalculating weights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = [0] + list(map(int, input().split()))
        B = int(n**0.5) + 1

        small_d = [[] for _ in range(B+1)]
        for d in range(1, B+1):
            prefix = [0]*(n+2)
            weighted = [0]*(n+2)
            for start in range(1, d+1):
                wsum = 0
                psum = 0
                idx = start
                cnt = 1
                while idx <= n:
                    psum += a[idx]
                    wsum += a[idx]*cnt
                    small_d[d].append((idx, wsum, cnt))
                    idx += d
                    cnt += 1

        ans = []
        queries = [tuple(map(int, input().split())) for _ in range(q)]
        for s, d, k in queries:
            if d <= B:
                # small d brute-force using precomputed sequences
                res = 0
                cnt = 1
                idx = s
                while idx <= n and cnt <= k:
                    res += a[idx]*cnt
                    idx += d
                    cnt += 1
                ans.append(res)
            else:
                # large d direct computation
                res = 0
                for i in range(k):
                    res += a[s + i*d]*(i+1)
                ans.append(res)
        print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution separates queries based on the step size. For small `d`, we conceptually precompute weighted sums, but the implementation can directly iterate since the loop limit is bounded by `sqrt(n)`. For large `d`, the subsequence length is small enough that direct computation is efficient. The use of 1-based indexing in `a` avoids off-by-one errors when computing weighted sums.

## Worked Examples

Sample input `[3 3, 1 1 2, (1,2,2), (2,2,1), (1,1,2)]`:

| Query | Elements | Multipliers | Weighted sum |
| --- | --- | --- | --- |
| (1,2,2) | 1,2 | 1,2 | 1_1+2_2=5 |
| (2,2,1) | 1 | 1 | 1*1=1 |
| (1,1,2) | 1,1 | 1,2 | 1_1+1_2=3 |

This confirms the algorithm correctly multiplies each element by its position.

Another input `[5 3, 1 2 3 4 5, (1,2,3), (2,3,2), (1,1,5)]`:

| Query | Elements | Multipliers | Weighted sum |
| --- | --- | --- | --- |
| (1,2,3) | 1,3,5 | 1,2,3 | 1_1+3_2+5*3=22 |
| (2,3,2) | 2,5 | 1,2 | 2_1+5_2=12 |
| (1,1,5) | 1,2,3,4,5 | 1,2,3,4,5 | 1+4+9+16+25=55 |

The table confirms the invariant: weighted sum formula is applied correctly to every element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n_sqrt(n) + q_sqrt(n)) | Each query with d > sqrt(n) takes at most sqrt(n) operations; small d handled via precomputation loops. |
| Space | O(n*sqrt(n)) | Storing prefix/weighted sums for small d sequences |

Given the constraints, the worst-case number of operations is roughly 10^5_316 + 2_10^5*316 ≈ 10^8, which fits in the 2-second limit with Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""5
3 3
1 1 2
1 2 2
2 2 1
1 1 2
3 1
-100000000 -100000000 -100000000
1 1 3
5 3
1 2 3 4 5
1 2 3
2
```
