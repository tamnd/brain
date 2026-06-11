---
title: "CF 1302C - Segment tree or Fenwick?"
description: "We are asked to maintain an array of integers that starts with all zeros and answer a series of queries. Each query is either an assignment, setting a specific element to a value, or a range sum query, asking for the sum of a contiguous subarray."
date: "2026-06-11T18:10:10+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1302
codeforces_index: "C"
codeforces_contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
weight: 1302
solve_time_s: 106
verified: true
draft: false
---

[CF 1302C - Segment tree or Fenwick?](https://codeforces.com/problemset/problem/1302/C)

**Rating:** -  
**Tags:** data structures  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain an array of integers that starts with all zeros and answer a series of queries. Each query is either an assignment, setting a specific element to a value, or a range sum query, asking for the sum of a contiguous subarray. There are multiple independent test cases, each with its own array and queries. The output is simply the results of the sum queries, in order.

The constraints are tight: the array length and the number of queries per test case can each reach up to $10^5$, and the total across all test cases can reach $10^6$. This rules out naive approaches that scan ranges for every sum query. A naive solution would take $O(n)$ per sum query, resulting in up to $10^{11}$ operations in the worst case, which is far beyond any reasonable time limit.

A subtle edge case arises when a query asks for the sum of the entire array before any updates. In that scenario, a careless implementation that assumes values are initialized might try to read uninitialized memory or miscalculate, but the correct sum is zero. Another edge case is repeated updates to the same position, which must overwrite previous values rather than accumulate.

## Approaches

The brute-force method is straightforward. We maintain the array explicitly and process each query in the obvious way. Assignments are done in $O(1)$ time, but sum queries require iterating from the left index to the right index, which is $O(n)$ in the worst case. With $q$ queries, the overall complexity can reach $O(nq)$, which is far too slow for large inputs.

The key insight to improve performance is that we only need to support point updates and range sum queries. This exactly matches the capabilities of a Fenwick Tree (Binary Indexed Tree) or a Segment Tree. Both data structures allow point updates in $O(\log n)$ and range sum queries in $O(\log n)$. Fenwick Tree is simpler to implement and slightly faster in practice for this type of query.

The crucial observation is that the array values are only replaced, not incremented. For a Fenwick Tree, we can store the current values in a separate array to compute the difference on each assignment, and then propagate that difference into the tree. This allows each query to be processed in $O(\log n)$, which keeps total operations under $10^7$ for the problem's constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Fenwick Tree | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays per test case: the main array to store current values and a Fenwick Tree array for efficient prefix sums. This sets up a structure that can process both assignments and range queries efficiently.
2. For a type 1 query, `1 x y`, compute the difference between the new value `y` and the current value at position `x`. Update the main array at position `x` with the new value. Then propagate this difference through the Fenwick Tree. Propagating the difference ensures that future range sum queries reflect the updated value without recomputing sums from scratch.
3. For a type 2 query, `2 l r`, compute the prefix sum up to `r` in the Fenwick Tree and subtract the prefix sum up to `l-1`. This gives the sum of the subarray `[l, r]`. Output this value.
4. Repeat the above steps for each query and for each test case independently.

Why it works: The Fenwick Tree maintains the invariant that each node stores a partial sum of the array. When we update a value, the difference is propagated to all relevant nodes, ensuring that any prefix sum query returns the correct total. Range sum queries are then just the difference of two prefix sums, which is mathematically equivalent to the direct sum of elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add(bit, i, delta):
    n = len(bit)
    while i < n:
        bit[i] += delta
        i += i & -i

def prefix_sum(bit, i):
    result = 0
    while i > 0:
        result += bit[i]
        i -= i & -i
    return result

def main():
    T = int(input())
    for _ in range(T):
        n, q = map(int, input().split())
        arr = [0] * (n + 1)
        bit = [0] * (n + 1)
        for _ in range(q):
            query = input().split()
            if query[0] == '1':
                x, y = int(query[1]), int(query[2])
                delta = y - arr[x]
                arr[x] = y
                add(bit, x, delta)
            else:
                l, r = int(query[1]), int(query[2])
                result = prefix_sum(bit, r) - prefix_sum(bit, l - 1)
                print(result)

if __name__ == "__main__":
    main()
```

The solution first defines helper functions to update the Fenwick Tree and compute prefix sums. The `add` function propagates the delta through all relevant nodes. `prefix_sum` walks backward through the tree to sum the relevant values. In the main loop, we read each test case, initialize the array and tree, and process each query according to its type. The key subtlety is computing the difference `delta` for assignments to maintain correctness.

## Worked Examples

**Sample 1**

| Step | Query | arr | BIT | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 1 6 | [0,0,0,0,0,0,0] | [0,0,0,0,0,0,0] | 0 |
| 2 | 1 3 2 | [0,0,2,0,0,0,0] | [0,0,2,2,0,0,0] |  |
| 3 | 2 2 4 | [0,0,2,0,0,0,0] | [0,0,2,2,0,0,0] | 2 |
| 4 | 1 6 3 | [0,0,2,0,0,0,3] | [0,0,2,2,0,0,3] |  |
| 5 | 2 1 6 | [0,0,2,0,0,0,3] | [0,0,2,2,0,0,3] | 5 |

This demonstrates that the algorithm correctly updates values and computes sums over arbitrary ranges.

**Sample 2**

| Step | Query | arr | BIT | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 3 7 | [0,0,7,0,0,0] | [0,0,7,7,0,0] |  |
| 2 | 1 1 4 | [0,4,7,0,0,0] | [0,4,7,11,0,0] |  |
| 3 | 2 1 5 | [0,4,7,0,0,0] | [0,4,7,11,0,0] | 11 |

Here we see that multiple updates accumulate correctly in the Fenwick Tree, and the range sum calculation uses the difference of prefix sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) log n) | Each query requires O(log n) for update or sum; initializing arrays is O(n) per test case. |
| Space | O(n) | We store the array and the Fenwick Tree per test case. |

Given that the sum of `n` and `q` across all test cases is at most $10^6$, the total operations are below $2 \cdot 10^6 \cdot \log 10^5 \approx 2 \cdot 10^6 \cdot 17$, which fits comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Provided samples
assert run("2\n6 5\n2 1 6\n1 3 2\n2 2 4\n1 6 3\n2 1 6\n5 3\n1 3 7\n1 1 4\n2 1 5\n") == "0\n2\n5\n11", "sample 1"

# Minimum-size input
assert run("1\n1 2\n2 1 1\n1 1 5\n") == "0", "min size"

# Maximum-size input: all zeros, sum query entire array
n = 100000
q = 1
inp = f"1\n{n} {q}\n2 1 {n}\n"
assert run(inp) == "0", "max size, all zeros"

# Repeated updates
assert run("1\n3 5\n1 1 5\n1 1 10\n2 1 1\n
```
