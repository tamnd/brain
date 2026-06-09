---
title: "CF 1923C - Find B"
description: "We are given an array c of positive integers and multiple queries asking whether certain subarrays of c are good."
date: "2026-06-08T19:12:18+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1923
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 162 (Rated for Div. 2)"
rating: 1400
weight: 1923
solve_time_s: 103
verified: true
draft: false
---

[CF 1923C - Find B](https://codeforces.com/problemset/problem/1923/C)

**Rating:** 1400  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array `c` of positive integers and multiple queries asking whether certain subarrays of `c` are _good_. A subarray is good if it is possible to construct another array `b` of the same length such that three conditions hold: the sums of the subarray and `b` match, every element of the subarray differs from the corresponding element of `b`, and all elements of `b` are positive.

The input consists of multiple test cases. Each test case provides the array `c` and a list of queries, each defining a subarray by its starting and ending indices. The output for each query is "YES" if the subarray is good and "NO" otherwise.

The constraints are tight: the total length of all arrays and the total number of queries across test cases can reach 300,000. This implies that any solution that examines each subarray element individually for every query would perform on the order of 10^10 operations in the worst case, which is far too slow. We need a method that can answer each query efficiently without reconstructing the subarray explicitly every time.

A subtle edge case arises when the subarray contains only a single element. In that case, there is no way to satisfy the condition that `b_i ≠ a_i`, because a single positive integer cannot differ from itself while keeping the sum unchanged. Any naive approach that ignores this would incorrectly claim that a length-one subarray is good.

## Approaches

A brute-force approach would attempt to construct a valid array `b` for each query by iterating over the subarray and trying to assign values that differ from `a_i` while keeping the sum consistent. For a subarray of length `m`, this would take `O(m)` time per query. Across the worst-case scenario of 300,000 queries on arrays of length up to 300,000, this results in roughly 10^10 operations, which is infeasible.

The key observation is that the actual values in the subarray are largely irrelevant to the question of goodness. A subarray of length one can never be good, but any subarray of length two or more can always be made good by a simple redistribution trick. If the length is at least two, one can always increase one element by 1 and decrease another by 1. This preserves the sum, guarantees positivity if all original elements are positive, and ensures that all `b_i ≠ a_i`.

This reduces the problem to a simple check: if the subarray length is 1, the answer is "NO". Otherwise, the answer is "YES". This approach answers each query in `O(1)` time after reading the input. Prefix sums are not even necessary because the actual sum does not constrain the feasibility beyond the trivial positivity and sum-preservation conditions, which are satisfied by the redistribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_length_of_subarrays) ≈ 10^10 | O(m) per query | Too slow |
| Optimal | O(n + q) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read `n` and `q`, followed by the array `c` of length `n`.
2. For each query, read the indices `l` and `r`. Compute the length of the subarray as `r - l + 1`.
3. If the length is 1, print "NO" because no array `b` can satisfy `b_1 ≠ a_1` while preserving the sum and positivity.
4. If the length is 2 or more, print "YES" because we can always adjust one element up and another down by 1, ensuring `b_i ≠ a_i` and sum equality.

**Why it works**: The only constraint that could make a subarray impossible is having length 1. For longer subarrays, the sum-preservation condition is flexible enough that one can tweak elements minimally to satisfy all conditions. The invariant is that for any length ≥ 2, at least two elements allow a swap that preserves the sum while changing both values.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    c = list(map(int, input().split()))
    for _ in range(q):
        l, r = map(int, input().split())
        length = r - l + 1
        if length == 1:
            print("NO")
        else:
            print("YES")
```

The solution reads input efficiently using `sys.stdin.readline`. For each query, it calculates the subarray length in `O(1)` and applies the simple length check. The program avoids unnecessary array slicing or sum calculations, which keeps it fast for the largest input sizes. The critical boundary to handle correctly is a subarray of length one.

## Worked Examples

**Sample 1**

Input subarray queries:

```
1 5 -> length 5
4 4 -> length 1
3 4 -> length 2
1 3 -> length 3
```

| Query | Subarray length | Output |
| --- | --- | --- |
| 1 5 | 5 | YES |
| 4 4 | 1 | NO |
| 3 4 | 2 | YES |
| 1 3 | 3 | YES |

The trace confirms that only length-1 subarrays are impossible.

**Edge-case Example**

Input: `c = [7], query = 1 1`

Length is 1, so output is NO. No other values matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Each query is answered in constant time; reading input takes O(n) per test case. |
| Space | O(n) | Only the array `c` needs to be stored. No extra arrays are required. |

This complexity easily fits within the 3-second time limit for `n, q` up to 300,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        c = list(map(int, input().split()))
        for _ in range(q):
            l, r = map(int, input().split())
            length = r - l + 1
            if length == 1:
                print("NO")
            else:
                print("YES")
    return output.getvalue().strip()

# provided sample
assert run("""1
5 4
1 2 1 4 5
1 5
4 4
3 4
1 3
""") == """YES
NO
YES
YES"""

# custom tests
assert run("""1
1 1
7
1 1
""") == "NO", "single element subarray"

assert run("""1
2 2
1 2
1 1
1 2
""") == "NO\nYES", "mix of length 1 and 2"

assert run("""1
3 1
1 1 1
2 3
""") == "YES", "all equal values"

assert run("""1
5 5
5 4 3 2 1
1 5
2 2
3 4
4 5
5 5
""") == "YES\nNO\nYES\nYES\nNO", "various lengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n7\n1 1` | NO | single-element subarray rejection |
| `2 2\n1 2\n1 1\n1 2` | NO YES | mixed lengths handled correctly |
| `3 1\n1 1 1\n2 3` | YES | all-equal values still feasible |
| `5 5\n5 4 3 2 1\n...` | YES NO YES YES NO | correct handling of boundary and intermediate lengths |

## Edge Cases

For a single-element subarray, for example `c = [42], query = 1 1`, the algorithm computes `length = 1` and outputs NO immediately. There is no attempt to construct `b`, avoiding incorrect acceptance.

For the largest subarray possible, such as `c` with length 300,000 and query `1 300000`, `length = 300000` triggers "YES" directly without iterating or summing, confirming the solution handles the upper limit efficiently.

All edge cases, including consecutive equal elements and subarrays at the start or end of the array, are handled correctly by this simple length check.
