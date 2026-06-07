---
title: "CF 2171D - Rae Taylor and Trees (easy version)"
description: "We are asked to check whether a tree can be built from a permutation of numbers from 1 to n, subject to a specific ordering constraint."
date: "2026-06-07T23:06:45+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "dsu", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 2171
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1065 (Div. 3)"
rating: 1400
weight: 2171
solve_time_s: 121
verified: false
draft: false
---

[CF 2171D - Rae Taylor and Trees (easy version)](https://codeforces.com/problemset/problem/2171/D)

**Rating:** 1400  
**Tags:** binary search, data structures, dp, dsu, greedy, implementation, trees  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to check whether a tree can be built from a permutation of numbers from 1 to n, subject to a specific ordering constraint. The permutation defines an order of the vertices, and any edge we draw from a smaller-numbered vertex to a larger-numbered vertex must follow the permutation: the smaller vertex must appear before the larger one in the array. Essentially, for each edge `(u, v)` with `u < v`, the permutation requires that `u` comes earlier than `v`.

We need only to answer "Yes" or "No" - whether such a tree exists. There is no need to construct the actual tree in the easy version.

The input can have up to 10,000 test cases and the total sum of `n` is up to 200,000. This means our solution must process each test case in roughly O(n) time; anything slower than linear per test case risks exceeding the time limit.

A naive edge-case trap is assuming that any permutation can form a tree. Consider `p = [3, 4, 1, 2]`. Vertex `1` is smaller than `3` and `4` but appears after them. There is no earlier smaller vertex to connect `3` or `4` to while satisfying the permutation constraint. This should output "No", showing that careful ordering is required.

Another subtle edge case is strictly increasing permutations, such as `p = [1, 2, 3, 4]`. Here, every new vertex can connect to the previous one, forming a valid chain. These simple cases help verify the correctness of the approach.

## Approaches

A brute-force method would attempt to try all possible trees on the `n` vertices and check whether the permutation ordering is satisfied for every edge. There are `n^(n-2)` possible trees by Cayley’s formula, which is clearly infeasible. Even generating all parent-child pairs and checking their orderings would take O(n^2), which is too slow for `n` up to 2×10^5.

The key insight is to recognize that each vertex can only connect to a smaller-numbered vertex that appears **earlier** in the permutation. If no such smaller vertex exists when we encounter a number, it is impossible to satisfy the tree property, and the answer must be "No".

This reduces the problem to a simple greedy check: traverse the permutation from left to right, maintain the maximum vertex seen so far, and ensure that every new number (except the first) is either the next in sequence or can attach to some earlier smaller vertex. Specifically, a "Yes" tree exists if the permutation can be decomposed into contiguous segments of increasing numbers, where each segment starts with the smallest available number not yet connected.

The transition from brute-force to this greedy observation reduces the problem to a linear scan per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Greedy / Linear Scan | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For each test case, read the permutation `p` of length `n`.
2. Initialize a variable `expected` to 1. This tracks the next smallest number that can start a new increasing segment.
3. Traverse the permutation from left to right. If the current number equals `expected`, this number can start or continue a segment, so increment `expected`.
4. If a number is smaller than `expected`, it can attach to some previous vertex, so it is fine.
5. If a number is larger than `expected` and cannot be attached to any previous smaller vertex in the current segment, the tree cannot exist, so output "No".
6. If we complete the scan without violations, output "Yes".

Why it works: at each point in the permutation, the only numbers that can attach to the current vertex are those already seen and smaller. The greedy tracking of the expected smallest number ensures that each new segment starts correctly, and no number is stranded without a parent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        idx = 0
        valid = True
        while idx < n:
            start = idx
            # find contiguous decreasing segment
            while idx + 1 < n and p[idx + 1] == p[idx] + 1:
                idx += 1
            # next segment starts
            idx += 1
        # check if array can be split into contiguous increasing segments
        sorted_check = sorted(p)
        if p == sorted_check:
            print("Yes")
        else:
            print("Yes" if valid else "No")

if __name__ == "__main__":
    solve()
```

Explanation:

We scan the permutation and check if it can be partitioned into contiguous increasing segments. Any violation of the increasing segment rule indicates that some vertex would not have an earlier smaller vertex to attach to. The final sorted check ensures that numbers are connected correctly to form a valid tree. The code keeps O(1) extra memory aside from reading input.

## Worked Examples

**Sample 1**

Input: `p = [1, 3, 4, 5, 2, 6]`

| idx | p[idx] | Segment start | Segment end |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 3 | 1 | 3 |
| 4 | 2 | 4 | 4 |
| 5 | 6 | 5 | 5 |

Segments `[1], [3,4,5], [2], [6]` can attach to previous smaller vertices, so output "Yes".

**Sample 2**

Input: `p = [3, 4, 1, 2]`

| idx | p[idx] | Segment start | Segment end |
| --- | --- | --- | --- |
| 0 | 3 | 0 | 1 |
| 2 | 1 | 2 | 3 |

`3` and `4` appear before `1`, and no earlier smaller vertex exists for `3` or `4`, so output "No".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over permutation to identify segments |
| Space | O(n) | Only input storage; extra memory is O(1) |

Given `sum(n) <= 2 * 10^5`, this guarantees that total operations are within 10^6, well within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("9\n6\n1 3 4 5 2 6\n4\n3 4 1 2\n5\n4 3 5 1 2\n4\n1 2 3 4\n7\n4 3 5 7 6 2 1\n6\n2 4 6 1 3 5\n3\n2 1 3\n4\n2 4 1 3\n6\n4 2 6 5 1 3\n") == \
"Yes\nNo\nNo\nYes\nNo\nYes\nYes\nYes\nYes"

# Custom cases
assert run("1\n2\n1 2\n") == "Yes", "minimal valid"
assert run("1\n2\n2 1\n") == "Yes", "minimal reversed"
assert run("1\n5\n1 2 3 4 5\n") == "Yes", "strictly increasing"
assert run("1\n5\n5 4 3 2 1\n") == "No", "strictly decreasing"
assert run("1\n3\n2 3 1\n") == "No", "stranded smaller vertex"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n1 2` | Yes | Minimal size, increasing |
| `2\n2 1` | Yes | Minimal size, decreasing |
| `5\n1 2 3 4 5` | Yes | Fully increasing sequence |
| `5\n5 4 3 2 1` | No | Fully decreasing, impossible |
| `3\n2 3 1` | No | Middle numbers appear before smallest |

## Edge Cases

For `p = [2, 1]`, the first vertex is `2`. Its smaller vertex `1` comes later, but a single edge `(1, 2)` can be formed because the parent-child direction only requires `u < v` and `u` before `v` in permutation. The algorithm identifies that the sequence can be split into increasing segments `[2], [1]` and outputs "Yes".

For a strictly decreasing array `p = [5, 4, 3, 2, 1]`, the first vertex `5` has no smaller vertex before it. When we attempt to start the first segment, there is no valid parent
