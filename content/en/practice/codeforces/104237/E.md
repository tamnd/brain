---
title: "CF 104237E - Tree Counting"
description: "We are given a line of blocks, each block having a certain number of trees. A series of walks is also given, where each walk covers a contiguous segment of blocks from one endpoint to another, inclusive."
date: "2026-07-01T23:20:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104237
codeforces_index: "E"
codeforces_contest_name: "Harker Programming Invitational 2023 Novice"
rating: 0
weight: 104237
solve_time_s: 70
verified: true
draft: false
---

[CF 104237E - Tree Counting](https://codeforces.com/problemset/problem/104237/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of blocks, each block having a certain number of trees. A series of walks is also given, where each walk covers a contiguous segment of blocks from one endpoint to another, inclusive. For every walk, Clare passes all trees located on every block within that interval, and the task is to compute the total number of trees she passes across all walks combined.

A direct reading of the problem suggests we repeatedly need to compute the sum of values over many subarrays of a fixed array. The array length is at most 200, while the number of queries can reach 10,000. Each value is small, but the accumulation over many ranges is what matters.

The constraints immediately suggest that recomputing each segment sum from scratch is borderline but potentially acceptable. However, doing 10,000 queries each scanning up to 200 elements results in about 2 million operations, which is already near the upper edge of what is comfortable in Python under a 1 second limit. Any additional overhead or multiple test cases would make this risky. A cleaner solution should avoid repeated traversal.

A subtle point is that each walk endpoint can be given in any order. A walk from block 5 to block 2 is the same as from 2 to 5. Any solution that assumes A_i is always less than or equal to B_i will fail.

Another common mistake is forgetting inclusivity. Since both endpoints are included, a segment like 1 to 1 still contributes the value of that single block, not zero.

Edge cases appear when the walk range collapses to a single block or when all trees are concentrated at one position. For example, if we have N = 1, T = [7], and a single query (1, 1), the correct answer is 7. A careless implementation using half-open intervals or incorrect slicing would produce 0.

## Approaches

The most direct approach is to process each walk independently by iterating over all blocks in its range and summing the trees. This is straightforward: for each query, we normalize the endpoints so that we always iterate from the smaller index to the larger one, then accumulate the values in that interval.

This approach is correct because it directly follows the definition of the problem without transformation. However, its cost scales linearly with the size of each query interval. In the worst case, each query spans almost the entire array, leading to roughly M × N operations, which is about 2 × 10^6 operations in the worst case here. That is still barely feasible, but it is unnecessarily tight and does repeated work.

The key observation is that the underlying array is static. Every query asks for a sum over a range of a fixed array, and there are many such queries. This structure is exactly what prefix sums are designed for. By precomputing cumulative sums once, each query can be answered in constant time by subtracting two prefix values. The entire cost of repeated range summation collapses into a single preprocessing step.

The brute-force method works because the data is small, but it fails in terms of efficiency margin and scalability. The prefix sum transformation replaces repeated traversal with reuse of previously computed partial results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(MN) | O(1) | Too slow under tight constraints |
| Prefix Sum | O(N + M) | O(N) | Accepted |

## Algorithm Walkthrough

We transform the array into a structure that allows constant-time range queries.

1. Read the array of trees and build a prefix sum array where each position stores the total number of trees from the start up to that index. This allows any prefix segment sum to be retrieved instantly rather than recomputed.
2. For each query, read the endpoints A and B. Since the direction of the walk does not matter, reorder them so that the smaller index comes first. This ensures we always work with a valid increasing interval.
3. Compute the sum of trees in that interval using the prefix array. The sum from L to R is obtained by subtracting the prefix value before L from the prefix value at R. This works because prefix sums accumulate all contributions up to a point, and subtraction removes everything before the interval.
4. Add the computed value to a running total, since the problem asks for the sum over all walks combined rather than per-query output.
5. After processing all queries, output the accumulated total.

### Why it works

The prefix sum array encodes the invariant that each position stores the total contribution of all elements before it. Any range sum can be expressed as the difference of two such cumulative values because all overlapping contributions cancel out except those strictly inside the interval. Since each query is reduced to a constant-time arithmetic operation over precomputed values, no recomputation or overlap ambiguity occurs, and every block contributes exactly once per query that includes it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    t = list(map(int, input().split()))
    
    prefix = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + t[i - 1]
    
    total = 0
    for _ in range(m):
        a, b = map(int, input().split())
        if a > b:
            a, b = b, a
        total += prefix[b] - prefix[a - 1]
    
    print(total)

if __name__ == "__main__":
    solve()
```

The solution first constructs a prefix sum array where index i represents the total number of trees from block 1 through block i. This is done in a single linear pass over the input array.

Each query is then handled independently. The only subtle implementation detail is the normalization of endpoints, ensuring the left boundary is not greater than the right boundary. The subtraction `prefix[b] - prefix[a - 1]` correctly captures the sum of the inclusive interval without needing loops or slicing.

A common pitfall is forgetting that prefix indexing requires an offset, since prefix[0] represents an empty sum. This is why we access `a - 1` safely even when a is 1, because prefix[0] is defined as 0.

## Worked Examples

Consider the sample input.

Input:

```
4 2
2 1 6 1
1 2
2 4
```

Prefix construction and query evaluation proceed as follows.

| Step | A | B | Normalized (L, R) | prefix[L-1] | prefix[R] | Range Sum | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Query 1 | 1 | 2 | (1, 2) | 0 | 3 | 3 | 3 |
| Query 2 | 2 | 4 | (2, 4) | 2 | 10 | 8 | 11 |

The first query sums the first two blocks, yielding 2 + 1 = 3. The second query sums blocks 2 through 4, yielding 1 + 6 + 1 = 8. The total is 11.

Now consider a second input designed to test single-block and reversed intervals.

Input:

```
5 3
3 0 4 2 1
5 2
1 1
3 3
```

| Step | A | B | Normalized (L, R) | prefix[L-1] | prefix[R] | Range Sum | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Query 1 | 5 | 2 | (2, 5) | 3 | 10 | 7 | 7 |
| Query 2 | 1 | 1 | (1, 1) | 0 | 3 | 3 | 10 |
| Query 3 | 3 | 3 | (3, 3) | 4 | 7 | 4 | 14 |

This trace shows that reversed intervals are handled correctly and that single-element intervals still contribute their value properly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | One pass builds prefix sums, and each query is answered in constant time |
| Space | O(N) | Only the prefix array is stored in addition to input |

The constraints allow up to 200 elements and 10,000 queries. The solution performs a single linear preprocessing step and then constant-time work per query, which is comfortably within limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp)).strip()

def solve_output(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    t = list(map(int, input().split()))
    prefix = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + t[i - 1]
    total = 0
    for _ in range(m):
        a, b = map(int, input().split())
        if a > b:
            a, b = b, a
        total += prefix[b] - prefix[a - 1]
    return str(total)

# provided sample
assert solve_output("4 2\n2 1 6 1\n1 2\n2 4\n") == "11"

# single element range
assert solve_output("1 1\n7\n1 1\n") == "7"

# reversed interval
assert solve_output("3 1\n1 2 3\n3 1\n") == "6"

# all equal values
assert solve_output("5 2\n2 2 2 2 2\n1 5\n2 4\n") == "18"

# full coverage repeated
assert solve_output("4 3\n1 1 1 1\n1 4\n1 4\n1 4\n") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single block | 7 | minimal boundary case |
| reversed range | 6 | order independence |
| uniform array | 18 | consistent accumulation |
| repeated full range | 12 | repeated prefix usage |

## Edge Cases

A single-block input tests whether the implementation correctly handles prefix indexing at zero. With input `1 1 / 7 / 1 1`, the prefix array becomes `[0, 7]`, and the query evaluates as `prefix[1] - prefix[0]`, yielding 7.

A reversed query such as `3 1` verifies that normalization is applied. Without swapping, a naive loop or slice would treat the range incorrectly or produce an empty segment. After swapping, the interval becomes valid and the prefix subtraction produces the full sum.

Uniform arrays stress repeated accumulation consistency. Since every block has the same value, every range sum is proportional to its length, and prefix subtraction preserves this exactly across multiple queries.
