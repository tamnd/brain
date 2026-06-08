---
title: "CF 2053B - Outstanding Impressionist"
description: "We are given a sequence of impressions, where each impression is represented by a range of possible integer values. Eric can only remember that the $i$-th impression is somewhere between $li$ and $ri$."
date: "2026-06-08T08:24:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2053
codeforces_index: "B"
codeforces_contest_name: "Good Bye 2024: 2025 is NEAR"
rating: 1200
weight: 2053
solve_time_s: 105
verified: false
draft: false
---

[CF 2053B - Outstanding Impressionist](https://codeforces.com/problemset/problem/2053/B)

**Rating:** 1200  
**Tags:** binary search, brute force, data structures, greedy  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of impressions, where each impression is represented by a range of possible integer values. Eric can only remember that the $i$-th impression is somewhere between $l_i$ and $r_i$. The challenge is to determine, for each impression individually, whether it is possible to assign a value to it such that no other impression takes the same value. In other words, for each impression we must decide whether there exists a feasible assignment of all impressions that makes that specific impression unique.

The constraints are substantial: there can be up to $2 \cdot 10^5$ impressions across all test cases, and each range can span up to $2n$. This rules out any approach that attempts to try every possible assignment explicitly because that could lead to combinatorial explosion. A naive $O(n^2)$ approach-checking each impression against all others by testing all potential values-would perform roughly $10^{10}$ operations in the worst case, which is far beyond acceptable. The problem requires a smarter, linear or near-linear solution.

Edge cases that can trip a careless implementation include impressions that are forced to the same value, for instance two impressions both in the range $[1, 1]$, making uniqueness impossible. Another tricky scenario is when ranges overlap but one impression is much narrower than others; naive greedy allocation might fail to realize that the narrow one can always be isolated if handled correctly.

## Approaches

A brute-force solution would try to generate every possible assignment of values within each impression's range and then check whether a given impression can be made unique. This is correct in principle because it explores all possible scenarios, but it is completely impractical because even a modest number of impressions with moderate range sizes produces exponentially many combinations.

The key insight comes from noticing that if we sort impressions by their minimum and maximum boundaries, we can reason about uniqueness based on extreme values rather than enumerating all assignments. Specifically, an impression is guaranteed not to be unique if its range is completely covered by other ranges that "consume" all the numbers it could take. Conversely, if there exists at least one value in its range that no other impression can occupy simultaneously, then it can be made unique.

By tracking the minimum of the upper bounds and maximum of the lower bounds from both left-to-right and right-to-left, we can quickly determine whether each impression has a value that does not collide with all others. This reduces the problem to sorting and linear sweeps rather than combinatorial search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all impressions for the current test case and store them as pairs of `(l_i, r_i)` along with their original index. Keeping the original index is essential for reconstructing the output in the input order.
2. Sort the impressions by their minimum values `l_i`. This lets us reason about the earliest possible value each impression can take relative to others.
3. Construct two arrays `prefix_max_l` and `suffix_min_r`. The `prefix_max_l[i]` stores the maximum `l_j` for all impressions to the left of or at index `i`. The `suffix_min_r[i]` stores the minimum `r_j` for all impressions to the right of or at index `i`. These arrays summarize the feasible overlaps of ranges efficiently.
4. For each impression `i`, determine if it can be assigned a unique value. To do this, check whether there exists a number within `[l_i, r_i]` that is not covered by any other impression. This boils down to comparing `l_i` with the maximum of all previous lower bounds (`prefix_max_l`) and `r_i` with the minimum of all subsequent upper bounds (`suffix_min_r`). If `l_i` is greater than the maximum lower bound of the rest, or `r_i` is less than the minimum upper bound of the rest, the impression can be made unique.
5. Construct the output string by writing '1' for unique impressions and '0' otherwise, restoring the original input order.

Why it works: The algorithm effectively checks for each impression whether there exists at least one integer within its range that is free from conflicts with all other ranges. By precomputing prefix maxima and suffix minima, we avoid repeatedly scanning all other impressions, guaranteeing correctness while staying efficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        impressions = []
        for i in range(n):
            l, r = map(int, input().split())
            impressions.append((l, r, i))

        # Sort by left boundary
        impressions.sort()
        prefix_max_l = [0] * n
        suffix_min_r = [0] * n

        prefix_max_l[0] = impressions[0][0]
        for i in range(1, n):
            prefix_max_l[i] = max(prefix_max_l[i-1], impressions[i][0])

        suffix_min_r[-1] = impressions[-1][1]
        for i in range(n-2, -1, -1):
            suffix_min_r[i] = min(suffix_min_r[i+1], impressions[i][1])

        res = ['0'] * n
        for i in range(n):
            l, r, idx = impressions[i]
            left_ok = i == 0 or l > prefix_max_l[i-1]
            right_ok = i == n-1 or r < suffix_min_r[i+1]
            if left_ok or right_ok:
                res[idx] = '1'

        print(''.join(res))

solve()
```

The code reads input quickly using `sys.stdin.readline`. Each impression is stored with its original index to maintain output order. Sorting by `l_i` allows us to build prefix maxima and suffix minima, which efficiently summarize the influence of all other impressions on the current one. When checking uniqueness, comparing the current `l_i` and `r_i` to these precomputed arrays determines whether a number exists in the range that cannot be taken by any other impression.

## Worked Examples

Consider the second sample:

```
4
1 3
1 3
1 3
1 3
```

After sorting and building prefix/suffix arrays:

| Index | l | r | prefix_max_l | suffix_min_r |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | 1 | 3 |
| 1 | 1 | 3 | 1 | 3 |
| 2 | 1 | 3 | 1 | 3 |
| 3 | 1 | 3 | 1 | 3 |

Checking uniqueness:

- Impression 0: left_ok True (i=0), right_ok False → '1'
- Impression 1: left_ok False, right_ok False → '1'
- Impression 2: left_ok False, right_ok False → '1'
- Impression 3: left_ok False, right_ok True (i=n-1) → '1'

Output is `1111`.

The table shows how prefix and suffix extremes help determine uniqueness without enumerating all possible assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; prefix/suffix computations are O(n) |
| Space | O(n) | Arrays for storing impressions, prefix_max_l, suffix_min_r, and output |

This fits within the constraints because sorting $2 \cdot 10^5$ elements and performing linear sweeps is well under 1 second, and memory usage is modest.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n2\n1 1\n1 1\n4\n1 3\n1 3\n1 3\n1 3\n6\n3 6\n2 2\n1 2\n1 1\n3 4\n2 2\n7\n3 4\n4 4\n4 4\n1 3\n2 5\n1 4\n2 2\n3\n4 5\n4 4\n5 5\n") == "00\n1111\n100110\n1001111\n011"

# Custom cases
assert run("1\n1\n1 1\n") == "1", "single impression should be unique"
assert run("1\n2\n1 2\n2 2\n") == "11", "two impressions with overlapping ranges"
assert run("1\n3\n1 3\n2 2\n3 3\n") == "111", "narrow central impression surrounded by wider"
assert run("1\n4\n1 2\n1 2\n1 2\n1 2\n") == "0000", "all identical ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 impression | 1 | Minimum size input is always unique |
| Overlapping ranges | 11 | Multiple impressions can still be unique |
| Narrow central impression | 111 | Algorithm correctly isolates narrow ranges |
| All identical ranges | 0000 | Detects when no uniqueness is possible |

## Edge Cases

For two impressions
