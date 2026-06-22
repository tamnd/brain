---
title: "CF 105345D - Nightmare on 24th"
description: "We are given a line of buildings, each containing some number of students. Freddy always starts from the first building and moves strictly to the right. As he visits buildings in order, he accumulates the number of students he has seen so far."
date: "2026-06-23T05:48:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105345
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 1 (Advanced)"
rating: 0
weight: 105345
solve_time_s: 75
verified: false
draft: false
---

[CF 105345D - Nightmare on 24th](https://codeforces.com/problemset/problem/105345/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of buildings, each containing some number of students. Freddy always starts from the first building and moves strictly to the right. As he visits buildings in order, he accumulates the number of students he has seen so far.

For each query value, we are asked a simple logistics question: how far must Freddy go from the start so that the total number of students he has encountered is at least that query value. If even after visiting all buildings the total is still smaller than the query, the answer is impossible.

The key object is the prefix accumulation of the array. Every query is asking for the smallest prefix length whose sum reaches or exceeds a target.

The constraints push us toward linear or near-linear preprocessing. With up to 100000 buildings and 100000 queries, any solution that recomputes sums per query will fail. A double loop would lead to 10^10 operations in the worst case, which is far beyond a 1 second limit.

A subtle edge case appears when queries ask for zero students. In that case, the answer should be zero buildings, since Freddy already satisfies the requirement before entering any building. Another case is when buildings contain zeros, which can create long stretches where the prefix sum does not change. A naive “stop when sum increases” approach would break here because progress is not tied to visiting new buildings.

## Approaches

A direct approach processes each query independently. For a given target q, we simulate walking from the first building and keep adding student counts until the sum reaches q. This is correct because it follows the exact movement rule. However, each query can require scanning almost all buildings. With m queries, this becomes O(nm), which is too slow when both n and m are large.

The structure of the problem is monotone. As we move right, prefix sums never decrease. This monotonicity means that once we precompute prefix sums, each query becomes a search problem over a sorted (non-decreasing) array. Instead of re-simulating every query, we can answer each one by locating the first prefix sum that reaches the required threshold.

This reduces the task to binary searching over the prefix sum array. Each query is answered in logarithmic time, after a single linear preprocessing pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Prefix Sum + Binary Search | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums of the building array. The value at position i represents the total number of students from building 1 to building i. This transforms the problem into a monotonic array where each step never decreases.
2. For each query value q, check whether it exceeds the last prefix sum. If it does, there is no prefix that can satisfy the requirement, so the answer is -1. This avoids unnecessary searching.
3. If q is zero, return 0 immediately since no buildings are needed to reach zero students.
4. Otherwise, perform a binary search on the prefix sum array to find the smallest index i such that prefix[i] is greater than or equal to q. This works because the prefix array is sorted non-decreasing.
5. Output i + 1 if using zero-based indexing internally, since the answer is defined in terms of number of buildings visited.

### Why it works

The correctness comes from the monotonicity of prefix sums. Once a prefix sum reaches a certain value, all later prefixes are at least as large. This ensures that the set of valid answers forms a contiguous suffix of indices. Binary search exploits exactly this structure by repeatedly halving the search space while preserving the invariant that any valid answer must lie to the right of all positions with insufficient sum and to the left of all positions already confirmed sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
import bisect

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = list(map(int, input().split()))
    
    pref = []
    s = 0
    for x in a:
        s += x
        pref.append(s)
    
    total = pref[-1] if pref else 0
    
    out = []
    for x in q:
        if x == 0:
            out.append("0")
            continue
        if x > total:
            out.append("-1")
            continue
        idx = bisect.bisect_left(pref, x)
        out.append(str(idx + 1))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation begins by constructing the prefix sum array in a single pass over the buildings. This guarantees O(n) preprocessing.

Each query is handled independently. The edge case x == 0 is explicitly returned as 0 before any search, matching the definition that no buildings are needed.

The key operation is `bisect_left`, which finds the first position where the prefix sum is at least the query value. Adding 1 converts the zero-based index into a count of buildings.

The total sum check prevents unnecessary binary searches when the query exceeds all reachable students.

## Worked Examples

### Example 1

Input:

```
n = 7, a = [10, 8, 2, 4, 4, 8, 9]
queries = [10, 15, 25, 41, 100]
```

Prefix sums:

| i | a[i] | prefix |
| --- | --- | --- |
| 1 | 10 | 10 |
| 2 | 8 | 18 |
| 3 | 2 | 20 |
| 4 | 4 | 24 |
| 5 | 4 | 28 |
| 6 | 8 | 36 |
| 7 | 9 | 45 |

Query traces:

| q | binary search target | result index | answer |
| --- | --- | --- | --- |
| 10 | first ≥ 10 | 0 | 1 |
| 15 | first ≥ 15 | 1 | 2 |
| 25 | first ≥ 25 | 4 | 5 |
| 41 | first ≥ 41 | 6 | 7 |
| 100 | exceeds total | none | -1 |

This example shows how the prefix sum acts as a monotone lookup table. Each query corresponds to jumping directly to the first prefix that crosses the threshold.

### Example 2

Input:

```
a = [0, 0, 5, 0, 3]
queries = [0, 1, 5, 8]
```

Prefix sums:

| i | prefix |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 5 |
| 4 | 5 |
| 5 | 8 |

Query behavior:

| q | reasoning | answer |
| --- | --- | --- |
| 0 | empty prefix is valid | 0 |
| 1 | first prefix ≥ 1 is 3rd | 3 |
| 5 | first prefix ≥ 5 is 3rd | 3 |
| 8 | full array needed | 5 |

This highlights how zeros do not break correctness. Even though progress stalls early, prefix sums remain monotone and binary search still finds the correct boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | One pass builds prefix sums, each query uses binary search |
| Space | O(n) | Prefix array stores one value per building |

The constraints allow up to 200000 total elements across input arrays, and logarithmic per-query behavior comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import bisect

    def solve():
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        q = list(map(int, input().split()))
        
        pref = []
        s = 0
        for x in a:
            s += x
            pref.append(s)
        
        total = pref[-1] if pref else 0
        
        out = []
        for x in q:
            if x == 0:
                out.append("0")
            elif x > total:
                out.append("-1")
            else:
                idx = bisect.bisect_left(pref, x)
                out.append(str(idx + 1))
        
        return "\n".join(out)

    return solve()

# provided sample
assert run("""7 5
10 8 2 4 4 8 9
10 15 25 41 100
""") == """1
2
5
7
-1"""

# minimum size
assert run("""1 3
5
0 5 6
""") == """0
1
-1"""

# all zeros
assert run("""5 3
0 0 0 0 0
0 1 10
""") == """0
-1
-1"""

# increasing simple
assert run("""4 4
1 2 3 4
1 3 6 10
""") == """1
2
3
4"""

# boundary exact match
assert run("""3 2
2 2 2
6 7
""") == """3
-1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | direct boundary behavior | smallest input correctness |
| all zeros | stagnation handling | prefix not increasing |
| simple increasing | clean monotone case | binary search correctness |
| exact boundary | equality handling | lower_bound behavior |

## Edge Cases

A zero-query case like input `[5, 2, 3]` with query `0` immediately returns `0` because the prefix sum condition is already satisfied before visiting any building. The algorithm handles this before constructing a search, so no indexing is performed.

An all-zero array such as `[0, 0, 0]` produces prefix sums `[0, 0, 0]`. For a query like `1`, binary search returns the first index, but since the total sum is still zero, the pre-check `x > total` correctly outputs `-1`. This avoids misinterpreting repeated zeros as progress.

A query equal to the total sum, for example array `[3, 1, 2]` and query `6`, lands exactly at the last prefix. Binary search returns the final index, and the answer is the full length, since no earlier prefix reaches the total.
