---
title: "CF 978C - Letters"
description: "We are given several dormitories arranged in a line. Each dormitory contains a known number of rooms, and all rooms across all dormitories are conceptually concatenated into one long sequence."
date: "2026-06-17T01:22:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 1000
weight: 978
solve_time_s: 72
verified: true
draft: false
---

[CF 978C - Letters](https://codeforces.com/problemset/problem/978/C)

**Rating:** 1000  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several dormitories arranged in a line. Each dormitory contains a known number of rooms, and all rooms across all dormitories are conceptually concatenated into one long sequence. The first dormitory contributes its rooms first, followed by the second, and so on, forming a single continuous numbering from 1 up to the total number of rooms.

The task is to answer queries where each query gives a global room index in this combined sequence. For each such index, we need to determine two things: which dormitory contains that room, and what the room’s local index is inside that dormitory.

The input size makes the structure important. Both the number of dormitories and queries can be up to 200,000, and each dormitory may have up to 10¹⁰ rooms. This immediately rules out any approach that tries to simulate the full flattened array or scan linearly for each query. Even scanning dormitories per query leads to 2×10⁵ × 2×10⁵ operations in the worst case, which is far beyond the time limit.

A subtle edge case comes from boundary values of cumulative sums. For example, if dormitories have sizes `[3, 5]`, then global indices 1 to 3 map to dormitory 1, and 4 to 8 map to dormitory 2. A naive mistake is to treat prefix sums as open intervals inconsistently, leading to off-by-one errors such as mapping index 3 incorrectly into the second dormitory if the boundary condition is not handled carefully.

Another edge case is handling queries that land exactly on the last room of a dormitory. For example, if cumulative sums are `[10, 25, 37]`, then query `10` must map to the first dormitory, not the second. This is where strict inequality vs non-strict inequality matters.

## Approaches

A brute-force strategy would process each query independently by walking through dormitories, subtracting room counts until the remaining index fits inside a dormitory. For a single query, this is O(n). Over m queries, this becomes O(nm), which in the worst case reaches 4×10¹⁰ operations and is not feasible.

The structure of the problem suggests a cumulative perspective. If we compute prefix sums of dormitory sizes, each dormitory corresponds to a contiguous interval on the number line. Each query then becomes a point location problem: find the first prefix sum that is greater than or equal to the query value.

This is exactly a binary search over a monotonic array. Since prefix sums are strictly increasing, we can locate the correct dormitory in O(log n) per query. After finding the dormitory index, the local room number is obtained by subtracting the previous prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Prefix Sum + Binary Search | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums of dormitory sizes so that each position represents the last global index of that dormitory. This transforms the problem into searching ranges instead of iterating structures.
2. For each query value `x`, perform a binary search on the prefix sum array to find the smallest index `i` such that `prefix[i] >= x`. This identifies the dormitory containing the room because `x` lies within its cumulative interval.
3. Once the dormitory `i` is found, compute the local room index. If `i` is the first dormitory, the answer is simply `x`. Otherwise, subtract `prefix[i-1]` from `x`.
4. Output `(i + 1, local_index)` because dormitories are 1-indexed.

The key reasoning step is that each dormitory occupies a contiguous segment on the number line, so locating a room is equivalent to locating which segment contains a point.

### Why it works

The prefix sum array partitions the global numbering into disjoint, contiguous intervals where each interval corresponds to exactly one dormitory. Because prefix sums are strictly increasing, each query value falls into exactly one interval. The binary search finds that interval by exploiting monotonicity, and subtracting the previous boundary yields the correct offset inside the interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    prefix = []
    s = 0
    for x in a:
        s += x
        prefix.append(s)

    import bisect

    out = []
    for x in b:
        i = bisect.bisect_left(prefix, x)
        prev = prefix[i - 1] if i > 0 else 0
        out.append(f"{i + 1} {x - prev}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds prefix sums in a single pass. The critical implementation detail is using `bisect_left`, which finds the first prefix sum not less than the query. This correctly handles boundary values: if a query equals a prefix sum exactly, it still maps to the corresponding dormitory rather than the next one.

The subtraction step uses the previous prefix sum carefully, with a conditional for the first dormitory to avoid negative indexing. This is where many incorrect solutions fail by either always subtracting or forgetting the boundary case entirely.

## Worked Examples

We use the sample input.

Input:

```
n=3, m=6
a = [10, 15, 12]
b = [1, 9, 12, 23, 26, 37]
```

Prefix sums are `[10, 25, 37]`.

| query x | binary search result i | prefix[i-1] | dormitory | local index |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 |
| 9 | 0 | 0 | 1 | 9 |
| 12 | 1 | 10 | 2 | 2 |
| 23 | 1 | 10 | 2 | 13 |
| 26 | 2 | 25 | 3 | 1 |
| 37 | 2 | 25 | 3 | 12 |

This trace shows how each query is classified into the correct interval defined by prefix sums. It also demonstrates correct handling of exact boundary values like 10, 25, and 37 implicitly through binary search behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Prefix construction is linear, each query uses binary search over prefix array |
| Space | O(n) | Only prefix sums are stored |

This fits comfortably within constraints since n and m are up to 2×10⁵, and logarithmic search over this range is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    prefix = []
    s = 0
    for x in a:
        s += x
        prefix.append(s)

    import bisect

    out = []
    for x in b:
        i = bisect.bisect_left(prefix, x)
        prev = prefix[i - 1] if i > 0 else 0
        out.append(f"{i + 1} {x - prev}")

    return "\n".join(out)

# provided sample
assert run("""3 6
10 15 12
1 9 12 23 26 37
""") == """1 1
1 9
2 2
2 13
3 1
3 12"""

# minimum input
assert run("""1 3
5
1 3 5
""") == """1 1
1 3
1 5"""

# boundary at exact prefix
assert run("""2 3
4 6
4 5 10
""") == """1 4
2 1
2 6"""

# all equal sizes
assert run("""4 4
2 2 2 2
1 2 3 8
""") == """1 1
1 2
2 1
4 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single dorm | direct mapping | base case correctness |
| exact prefix hits | correct boundary handling | off-by-one safety |
| equal sizes | uniform segmentation | consistent interval logic |

## Edge Cases

One important edge case is when a query equals a prefix sum exactly. For example, if dorm sizes are `[4, 6]`, prefix is `[4, 10]`, and query is `4`. Binary search returns index `0`, and local index becomes `4 - 0 = 4`, correctly mapping to the last room of the first dormitory.

Another edge case is when the query falls into the last dormitory. With prefix `[4, 10]` and query `9`, binary search returns index `1`, prefix before it is `4`, and local index becomes `5`, correctly identifying the second dormitory.

These cases confirm that treating each dormitory as a closed interval on prefix boundaries combined with `bisect_left` yields correct and stable classification.
