---
title: "CF 105346D - Nightmare on 24th"
description: "We are given a row of buildings indexed from left to right, where each building contains a certain number of students. Freddy always starts from the first building and can only move forward in order."
date: "2026-06-23T15:33:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105346
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 2 (Beginner)"
rating: 0
weight: 105346
solve_time_s: 87
verified: false
draft: false
---

[CF 105346D - Nightmare on 24th](https://codeforces.com/problemset/problem/105346/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of buildings indexed from left to right, where each building contains a certain number of students. Freddy always starts from the first building and can only move forward in order. For each query value, we want to know the smallest prefix of buildings whose total number of students is at least that query value. If even after visiting all buildings the total is still smaller than the query, the answer is impossible.

This is fundamentally a prefix accumulation problem. Each query asks for the first position where the prefix sum reaches or exceeds a threshold.

The constraints allow up to 100,000 buildings and 100,000 queries. A direct simulation per query would scan from the start each time, leading to 10^10 operations in the worst case, which is too slow in Python. This immediately rules out any solution that recomputes sums repeatedly.

Edge cases arise when building values include zeros. A naive pointer approach that assumes progress is always made per building can fail if many consecutive buildings contribute nothing. For example, if all a_i are zero and q_j is positive, the correct answer is -1, and any method relying on incremental progress must explicitly check reachability against total sum.

Another subtle case is when q_j is zero. The correct answer is always 1, since zero students require visiting no meaningful amount of buildings, but the first building is still the minimal prefix.

## Approaches

The brute-force method processes each query independently. For a given q, we start from the first building and accumulate student counts until we reach or exceed q. This is correct because it directly follows the problem definition. However, in the worst case, each query may require scanning all n buildings. With m queries, this becomes O(nm), which is up to 10^10 operations.

The key observation is that all queries operate on the same static prefix structure. Once we compute prefix sums of the array, every query reduces to a search problem: find the smallest index i such that prefix[i] ≥ q. Since prefix sums are non-decreasing, we can use binary search for each query. This reduces each query to O(log n), bringing the total to O((n + m) log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Prefix + Binary Search | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Compute prefix sums over the building array, where prefix[i] stores the total number of students from building 1 to i. This transforms the problem into range reachability instead of repeated summation.
2. For each query q, check whether q is greater than the total sum prefix[n]. If it is, output -1 immediately since even visiting all buildings is insufficient.
3. If q is zero, output 1, since the smallest valid prefix is the first building. This handles the degenerate case where no accumulation is required.
4. Otherwise, perform a binary search on the prefix array to find the smallest index i such that prefix[i] ≥ q. This works because prefix sums are monotonically non-decreasing.
5. Output i for each query.

### Why it works

The prefix sum array encodes cumulative reachability: prefix[i] represents exactly what can be achieved by stopping at building i. Since values never decrease as we move right, the condition prefix[i] ≥ q defines a contiguous region of valid answers. Binary search exploits this monotonic structure to locate the first valid index. The algorithm cannot miss a valid answer because once prefix[i] exceeds q, all later indices also satisfy it, ensuring correctness of the first-found boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = list(map(int, input().split()))

    prefix = [0] * n
    prefix[0] = a[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + a[i]

    total = prefix[-1]
    out = []

    for x in q:
        if x == 0:
            out.append("1")
            continue
        if x > total:
            out.append("-1")
            continue

        lo, hi = 0, n - 1
        ans = n - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if prefix[mid] >= x:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        out.append(str(ans + 1))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution starts by building a prefix sum array so that every query becomes a search over cumulative totals rather than repeated summation. The binary search is implemented manually to avoid overhead and to explicitly control the first position where the prefix constraint is satisfied. The conversion `ans + 1` is required because the array is zero-indexed internally but the problem uses one-indexed building positions.

The special handling for `x == 0` prevents unnecessary binary search and ensures correctness for a boundary condition where the first prefix is always valid.

## Worked Examples

### Example 1

Input:

```
n = 7, m = 5
a = [10, 8, 2, 4, 4, 8, 9]
q = [10, 15, 25, 41, 100]
```

Prefix array:

| i | prefix[i] |
| --- | --- |
| 1 | 10 |
| 2 | 18 |
| 3 | 20 |
| 4 | 24 |
| 5 | 28 |
| 6 | 36 |
| 7 | 45 |

| Query | Binary search steps | Answer index | Output |
| --- | --- | --- | --- |
| 10 | hits at i=1 | 1 | 1 |
| 15 | first ≥15 is i=2 | 2 | 2 |
| 25 | first ≥25 is i=5 | 5 | 5 |
| 41 | first ≥41 is i=7 | 7 | 7 |
| 100 | total < 100 | none | -1 |

This confirms that the binary search correctly finds the leftmost prefix meeting the threshold and correctly rejects unreachable queries.

### Example 2

Input:

```
n = 5, m = 3
a = [0, 0, 5, 0, 10]
q = [1, 5, 15]
```

Prefix array:

| i | prefix[i] |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 5 |
| 4 | 5 |
| 5 | 15 |

| Query | Search behavior | Answer index | Output |
| --- | --- | --- | --- |
| 1 | skips zeros, lands at 3 | 3 | 3 |
| 5 | first reach at 3 | 3 | 3 |
| 15 | exact last element | 5 | 5 |

This example demonstrates correctness in the presence of zero-valued buildings, where progress is not guaranteed at every step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | prefix build is O(n), each query binary search is O(log n) |
| Space | O(n) | prefix array stores cumulative sums |

The constraints allow up to 2 × 10^5 total operations in logarithmic form, which fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = list(map(int, input().split()))

    prefix = [0] * n
    prefix[0] = a[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + a[i]

    total = prefix[-1]
    res = []

    for x in q:
        if x == 0:
            res.append("1")
            continue
        if x > total:
            res.append("-1")
            continue

        lo, hi = 0, n - 1
        ans = n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if prefix[mid] >= x:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        res.append(str(ans + 1))

    return "\n".join(res)

# provided sample
assert run("""7 5
10 8 2 4 4 8 9
10 15 25 41 100
""") == """1
2
5
7
-1"""

# all zeros
assert run("""5 3
0 0 0 0 0
0 1 5
""") == """1
-1
-1"""

# single building
assert run("""1 2
5
3 5
""") == """-1
1"""

# increasing prefix boundary
assert run("""4 3
1 2 3 4
1 10 11
""") == """1
4
-1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | 1, -1, -1 | unreachable sums and zero handling |
| single building | -1, 1 | minimal edge size correctness |
| increasing prefix | 1, 4, -1 | boundary search correctness |

## Edge Cases

One important edge case is when all building values are zero. In this situation, the prefix array never increases, so any positive query must immediately return -1. The algorithm handles this because the binary search condition prefix[mid] ≥ x is never satisfied, and the total sum check rejects the query early.

Another edge case is when the first building already satisfies the query. For example, a = [100, ...], q = 50. The prefix array starts at a large value, so binary search correctly returns index 0, which translates to output 1. The correctness depends on searching for the leftmost valid index, not just any valid index.
