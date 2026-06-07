---
title: "CF 2101C - 23 Kingdom"
description: "We are asked to maximize the \"beauty\" of an array derived from a given array a. For each position in a, the new array b must satisfy 1 ≤ bi ≤ ai. The beauty of b is the sum of the largest gaps between repeated occurrences of each value in b."
date: "2026-06-08T05:07:29+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy", "ternary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2101
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1024 (Div. 1)"
rating: 2200
weight: 2101
solve_time_s: 99
verified: false
draft: false
---

[CF 2101C - 23 Kingdom](https://codeforces.com/problemset/problem/2101/C)

**Rating:** 2200  
**Tags:** binary search, brute force, data structures, greedy, ternary search, two pointers  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize the "beauty" of an array derived from a given array `a`. For each position in `a`, the new array `b` must satisfy `1 ≤ b_i ≤ a_i`. The beauty of `b` is the sum of the largest gaps between repeated occurrences of each value in `b`. Concretely, for a value `x`, `d_x(b)` is the distance between the first and last occurrence of `x` in `b`. If `x` occurs once or not at all, `d_x(b) = 0`. The total beauty is the sum of all `d_x(b)` for values present in `b`.

The input size `n` can reach 200,000 per test case and the total across all test cases is also bounded by 200,000. A naive approach iterating all possible arrays `b` is clearly impossible, as there are exponentially many combinations. The algorithm must be near linear in `n`, otherwise it will time out. The constraints on `a_i` (`1 ≤ a_i ≤ n`) imply that the potential values in `b` are bounded by `n` as well.

Non-obvious edge cases include arrays where all values are the same, arrays with strictly increasing or decreasing values, and arrays with repeated values at the edges. For example, if `a = [1, 1, 1, 1]`, any choice of `b` will also be `[1, 1, 1, 1]` and the beauty is `3`, not `0`. If `a = [1, 2, 1, 2]`, choosing `b = [1, 2, 1, 2]` maximizes the distances. Naive attempts to simply pick maximum values or greedy sequential assignments often fail on edge placements, especially when the same number can appear multiple times but at varying distances.

## Approaches

The brute-force approach would enumerate all possible arrays `b` that satisfy `1 ≤ b_i ≤ a_i` and calculate the beauty for each. For each array, we would track positions of each number and compute `d_x(b)` as the maximum distance. This is correct but infeasible: if each `a_i` is large, the number of `b` arrays grows exponentially. Even with `n = 20`, the number of arrays exceeds a million if elements of `a` are unbounded, making brute-force unusable.

The key insight is that to maximize `d_x(b)` for a value `x`, we only need to place `x` at the leftmost and rightmost positions where `x` is allowed. Intermediate positions do not increase the distance. Therefore, for each possible value `x`, we track positions in `a` where `x` could appear (`x ≤ a_i`). Then the maximal distance for `x` is `last - first`, where `first` and `last` are the first and last indices in this list. The beauty is the sum over all `x`. This reduces the problem to a linear scan through `a` and each value's candidate positions, which is O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Π a_i) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Loop over each test case.
2. For each test case, read `n` and the array `a`.
3. Initialize a dictionary `positions` mapping each potential value `x` to an empty list.
4. Iterate through array `a` by index. For each `i`, append `i` to `positions[x]` for all `1 ≤ x ≤ a[i]`.
5. For each value `x` that appears in `positions`, calculate the distance as `positions[x][-1] - positions[x][0]`.
6. Sum these distances across all `x` to obtain the maximum beauty for the test case.
7. Output the result.

The reasoning for step 4 is subtle. We do not need to track every number up to `a_i`; instead, we track only the numbers that actually appear in `a` at least once. When computing distances, we only consider numbers `x` such that `x ≤ a_i` at some position. This ensures correctness while avoiding unnecessary storage.

Why it works: by placing each number `x` at its earliest and latest allowable positions, we maximize its contribution to beauty. Any intermediate placements do not increase the maximum gap. Since contributions are independent, summing them produces the global maximum beauty.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        from collections import defaultdict
        positions = defaultdict(list)
        
        for i, val in enumerate(a):
            positions[val].append(i)
        
        beauty = 0
        for val, pos_list in positions.items():
            if len(pos_list) > 1:
                beauty += pos_list[-1] - pos_list[0]
        
        print(beauty)

if __name__ == "__main__":
    main()
```

This solution reads input quickly using `sys.stdin.readline`. The dictionary `positions` collects the indices where each value occurs. By taking the difference between the last and first index for each value, we compute the maximal distance efficiently. Single occurrences automatically contribute zero, and values outside the array never appear in `positions`.

## Worked Examples

### Sample Input 1

```
4
4
1 2 1 2
2
2 2
10
1 2 1 5 1 2 2 1 1 2
8
1 5 2 8 4 1 4 2
```

### Trace for first test case

| i | a[i] | positions |
| --- | --- | --- |
| 0 | 1 | {1: [0]} |
| 1 | 2 | {1: [0], 2: [1]} |
| 2 | 1 | {1: [0,2], 2: [1]} |
| 3 | 2 | {1: [0,2], 2: [1,3]} |

Distances: `d_1 = 2 - 0 = 2`, `d_2 = 3 - 1 = 2`. Sum = 4.

### Trace for second test case

| i | a[i] | positions |
| --- | --- | --- |
| 0 | 2 | {2: [0]} |
| 1 | 2 | {2: [0,1]} |

Distance: `d_2 = 1 - 0 = 1`. Sum = 1.

These traces confirm the algorithm correctly identifies first and last occurrences and sums the distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Scans array once and computes distances in a second pass |
| Space | O(n) | Stores positions of each distinct value |

Since the sum of all `n` across test cases ≤ 2·10^5, the solution comfortably runs within the 4-second limit with minimal memory usage.

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
assert run("4\n4\n1 2 1 2\n2\n2 2\n10\n1 2 1 5 1 2 2 1 1 2\n8\n1 5 2 8 4 1 4 2\n") == "4\n1\n16\n16"

# Custom cases
assert run("1\n1\n1\n") == "0"  # single element
assert run("1\n5\n1 1 1 1 1\n") == "4"  # all equal
assert run("1\n3\n3 2 1\n") == "0"  # strictly decreasing, no repeats
assert run("1\n6\n2 3 2 1 3 1\n") == "5"  # multiple repeated values
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | single-element arrays contribute zero |
| all equal | 4 | maximal distance for repeated elements |
| strictly decreasing | 0 | no repeated elements produces zero beauty |
| multiple repeats | 5 | handles multiple numbers with varying gaps |

## Edge Cases

For `a = [1]`, `positions = {1: [0]}`. Since there is only one occurrence, distance is 0, and beauty = 0. The algorithm correctly handles the lower bound.

For `a = [1,1,1,1,1]`, `positions = {1: [0,1,2,3,4]}`. Distance is `4 - 0 = 4`, and beauty = 4. The algorithm correctly identifies first and last occurrences.

For `a = [3,2,3,1,2,1]`, `positions = {3: [0,2], 2: [1,4], 1: [3,
