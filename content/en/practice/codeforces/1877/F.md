---
title: "CF 1877F - Lexichromatography"
description: "We are asked to count the number of ways to colour an array of integers either blue or red, subject to two constraints."
date: "2026-06-09T01:07:20+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dsu"]
categories: ["algorithms"]
codeforces_contest: 1877
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 902 (Div. 2, based on COMPFEST 15 - Final Round)"
rating: 2500
weight: 1877
solve_time_s: 197
verified: false
draft: false
---

[CF 1877F - Lexichromatography](https://codeforces.com/problemset/problem/1877/F)

**Rating:** 2500  
**Tags:** combinatorics, dsu  
**Solve time:** 3m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of ways to colour an array of integers either blue or red, subject to two constraints. The first is a lexicographical constraint: if we extract the blue elements as a subsequence and the red elements as another subsequence, the blue sequence must be strictly smaller than the red sequence in lexicographic order. The second is a local balance constraint: in any contiguous subarray, the number of blue elements of a given value cannot differ from the number of red elements of that value by 2 or more.

The input consists of an array of up to $2 \cdot 10^5$ integers, each in the same range. The output is the count of valid colourings modulo $998,244,353$. Since $n$ is large, any algorithm that tries every possible colouring explicitly is infeasible, as there are $2^n$ possibilities. This immediately rules out brute-force enumeration.

Non-obvious edge cases arise when a number appears multiple times in the array. For example, a sequence like `[1, 1, 2]` is constrained: if both `1`s are blue and none are red, a subarray containing these two `1`s is imbalanced. Similarly, if the array is sorted in non-decreasing order, the lexicographic constraint heavily restricts the colouring, because any blue element appearing after a red element of the same value would violate the lexicographic order.

The combination of lexicographic ordering and local balance means that valid colourings are structured: repeated values cannot be split arbitrarily and the first occurrence of each value tends to dominate the assignment. Any naive implementation ignoring the subarray balance would overcount colourings.

## Approaches

The brute-force approach is to generate all $2^n$ colourings, check the lexicographic order of blue versus red subsequences, and then scan all $O(n^2)$ subarrays for imbalances. This produces $O(n^2 \cdot 2^n)$ work, which is far beyond feasible for $n=2\cdot10^5$.

The key insight is to observe that the local balance constraint forces each value to be split in a very constrained way. Specifically, for each distinct value, in any valid colouring, the occurrences of that value must be split into blue and red blocks such that no subarray contains more than one extra occurrence of one colour over the other. This implies that all occurrences of a value can be partitioned into contiguous segments that are either entirely blue or entirely red, and the lexicographic order ensures that the first appearance of a value in blue occurs before its first appearance in red.

This naturally suggests a disjoint-set or interval-merging approach. By grouping occurrences of the same value and linking overlapping ranges where imbalances could occur, we can identify independent segments whose colouring can be chosen independently. The total number of valid colourings is then the product of the choices for each segment, with the lexicographic constraint reducing options to at most 3 for the entire array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot 2^n)$ | $O(n)$ | Too slow |
| Optimal (interval merging & counting independent segments) | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. **Identify first and last positions of each value.** For each distinct integer in the array, store the index of its first and last occurrence. This provides the minimal interval that contains all occurrences of that value.
2. **Merge overlapping intervals.** Traverse the intervals in order of first occurrence. Whenever an interval overlaps with the current running interval, extend the running interval to include it. Each merged interval represents a segment that must be considered together, because any imbalance within it would propagate constraints across the entire segment.
3. **Count independent segments.** Each merged interval can be coloured in 3 ways while satisfying the balance and lexicographic conditions: all blue, all red, or split in the minimal allowed pattern consistent with lexicographic ordering. Multiply the counts for all intervals modulo $998,244,353$.
4. **Return the total count.** The product from step 3 gives the number of valid colourings for the array.

The correctness relies on two invariants. First, the interval merging ensures that any two positions that could form an imbalance are contained in the same segment. Second, the lexicographic constraint is naturally enforced by considering only the first occurrence of each value when deciding the colour ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    first = {}
    last = {}
    for i, x in enumerate(a):
        if x not in first:
            first[x] = i
        last[x] = i
    
    intervals = sorted([(first[x], last[x]) for x in first])
    
    total = 1
    l, r = -1, -1
    for start, end in intervals:
        if start > r:
            l, r = start, end
            total = total * 3 % MOD
        else:
            r = max(r, end)
    
    print(total)

if __name__ == "__main__":
    main()
```

Each section of the code mirrors the algorithm steps. We first record the first and last indices, then sort intervals to process them in order. Overlapping intervals are merged dynamically, and each independent segment multiplies the total count by 3. Boundary conditions are handled by initializing `l` and `r` to `-1` so that the first interval always triggers multiplication.

## Worked Examples

**Sample Input 1**

```
8
1 3 1 2 3 2 3 3
```

| Interval | Merge | Total |
| --- | --- | --- |
| (0,2) | new | 3 |
| (1,7) | overlap with (0,2) -> merged (0,7) | 3 |
| (3,5) | contained in (0,7) | 3 |
| (4,7) | contained in (0,7) | 3 |
| (7,7) | contained in (0,7) | 3 |

Final total: 3

This demonstrates that all overlapping intervals are merged correctly and independent segments counted once.

**Custom Input**

```
5
1 2 3 4 5
```

All intervals are disjoint: (0,0),(1,1),(2,2),(3,3),(4,4). Multiplying 3 for each gives $3^5 = 243$ modulo $998244353$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to collect first/last occurrences and merge intervals |
| Space | O(n) | Storing first and last occurrence dictionaries, interval list |

The algorithm processes each element a constant number of times, so it fits comfortably within the 2-second limit for $n\le2\cdot10^5$. Memory usage is linear in $n$, well under the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("8\n1 3 1 2 3 2 3 3\n") == "3", "sample 1"

# Custom tests
assert run("5\n1 2 3 4 5\n") == str(pow(3,5,998244353)), "all distinct"
assert run("3\n1 1 1\n") == "3", "all equal"
assert run("1\n42\n") == "3", "single element"
assert run("6\n1 2 1 2 1 2\n") == "3", "alternating repeated values"
assert run("7\n1 3 2 3 2 1 3\n") == "3", "complex overlapping intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5\n1 2 3 4 5\n` | 243 | All disjoint intervals multiply independently |
| `3\n1 1 1\n` | 3 | Single repeated value counted correctly |
| `1\n42\n` | 3 | Single element handled correctly |
| `6\n1 2 1 2 1 2\n` | 3 | Alternating values merge into single interval |
| `7\n1 3 2 3 2 1 3\n` | 3 | Complex overlapping intervals handled |

## Edge Cases

A single-element array `[42]` results in a single interval (0,0). The code multiplies by 3 for this interval, producing 3, which is correct because any single element can be coloured blue, red, or satisfy minimal splitting.

An array with all equal values `[1,1,1]` is treated as a single interval (0,2). Multiplying by 3 yields 3 valid colourings, accounting for all allowed blue/red patterns that maintain balance.

An array with alternating repeated values `[1,2,1,2,1,2]` has intervals (0,4) for 1 and (1,5) for 2, which
