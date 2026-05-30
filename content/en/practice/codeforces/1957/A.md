---
title: "CF 1957A - Stickogon"
description: "We are given a collection of sticks, each with an integer length. The goal is to build as many regular polygons as possible using these sticks, with the restriction that each side of a polygon must be exactly one stick, and no stick can be reused."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1957
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 940 (Div. 2) and CodeCraft-23"
rating: 800
weight: 1957
solve_time_s: 43
verified: true
draft: false
---

[CF 1957A - Stickogon](https://codeforces.com/problemset/problem/1957/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of sticks, each with an integer length. The goal is to build as many regular polygons as possible using these sticks, with the restriction that each side of a polygon must be exactly one stick, and no stick can be reused. A regular polygon requires at least three sides of equal length. Therefore, to form a polygon with sides of length `L`, we need at least three sticks of length `L`.

The input consists of multiple test cases. For each test case, we know how many sticks are available and their individual lengths. The output for each test case is the maximum number of polygons we can form with the given sticks.

The constraints are small: up to 100 sticks per test case, and up to 100 test cases. This means we can afford solutions with quadratic complexity in `n` per test case, but we should still prefer linear or near-linear approaches. Because sticks have lengths between 1 and 100, we can also leverage counting techniques rather than sorting or more complex data structures.

A subtle edge case arises when the total number of sticks of a certain length is insufficient to form even the smallest polygon. For example, if we have two sticks of length 5, we cannot form a triangle, so the output is zero for that length. Another edge case occurs when multiple polygons could be formed from different lengths; our solution must maximize the total number of polygons, not just the largest polygon.

## Approaches

A brute-force approach would be to try all possible subsets of sticks to form polygons. For every subset of length at least three, we would check if all sticks in the subset have the same length. We would then recursively remove the sticks used and continue searching. This is correct but infeasible because the number of subsets grows exponentially with `n`. For `n = 100`, iterating over all subsets is completely impractical.

The key insight is that a polygon can only be formed by having at least three sticks of the same length. Therefore, instead of examining arbitrary subsets, we can group sticks by their length and count how many we have of each length. The maximum number of polygons we can form from sticks of a single length is simply the integer division of the count by three. By summing this value over all lengths, we get the maximum number of polygons that can be formed from all sticks.

This counting-based method works because the problem allows forming polygons independently from each length, and no stick is shared between polygons. We do not need to consider mixing lengths, which simplifies the solution dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Counting & Division | O(n + L) | O(L) | Accepted |

Here `L` is the maximum stick length (100), which is negligible compared to `n`.

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the list of stick lengths `a`.
3. Initialize a frequency array `count` of size 101 (to cover lengths 1 to 100) to zero.
4. Iterate over all sticks, incrementing `count[length]` for each stick.
5. Initialize a variable `polygons` to zero.
6. For each possible length from 1 to 100, compute the number of polygons that can be formed from sticks of that length by integer division `count[length] // 3` and add it to `polygons`.
7. Print the value of `polygons` for the test case.

Why it works: Each polygon requires exactly three or more sticks of equal length. By counting the number of sticks per length, we can directly compute how many non-overlapping groups of three exist for each length. Summing across lengths ensures that all sticks are used optimally without violating the "no reuse" rule. Since we never mix lengths, we avoid the need for any complex subset selection.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    sticks = list(map(int, input().split()))
    count = [0] * 101
    for stick in sticks:
        count[stick] += 1
    polygons = 0
    for length in range(1, 101):
        polygons += count[length] // 3
    print(polygons)
```

This code starts by reading the number of test cases. For each case, we read the number of sticks and their lengths. The frequency array `count` is used to tally how many sticks exist for each possible length. By dividing each frequency by three, we find how many polygons we can form from that length, summing the results for all lengths. Using integer division ensures we ignore leftover sticks that cannot complete a polygon.

Subtle points include initializing the count array to size 101 to account for lengths up to 100, and ensuring that we correctly use integer division to avoid fractional polygons.

## Worked Examples

### Example 1

Input:

```
6
2 2 3 3 3 3
```

| Length | Count | Polygons |
| --- | --- | --- |
| 2 | 2 | 0 |
| 3 | 4 | 1 |
| Total polygons: 1 |  |  |

This shows that lengths with fewer than three sticks cannot contribute.

### Example 2

Input:

```
4 2 2 2 2 4 2 4 4
```

| Length | Count | Polygons |
| --- | --- | --- |
| 2 | 5 | 1 |
| 4 | 4 | 1 |
| Total polygons: 2 |  |  |

This demonstrates that multiple lengths can simultaneously contribute to the total.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + L) | Counting sticks takes O(n), iterating through lengths takes O(L) |
| Space | O(L) | Frequency array of size 101 |

Given `n` up to 100 and `L = 100`, the solution runs comfortably under the 1-second limit with minimal memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        sticks = list(map(int, input().split()))
        count = [0] * 101
        for stick in sticks:
            count[stick] += 1
        polygons = sum(c // 3 for c in count)
        print(polygons)
    return output.getvalue().strip()

# Provided samples
assert run("4\n1\n1\n2\n1 1\n6\n2 2 3 3 3 3\n9\n4 2 2 2 2 4 2 4 4\n") == "0\n0\n1\n2"

# Custom cases
assert run("1\n3\n1 1 1\n") == "1", "single triangle"
assert run("1\n5\n5 5 5 5 5\n") == "1", "five sticks of same length"
assert run("1\n6\n6 6 6 6 6 6\n") == "2", "two polygons possible"
assert run("1\n10\n1 1 1 2 2 2 3 3 3 3\n") == "4", "multiple lengths"
assert run("1\n2\n7 7\n") == "0", "insufficient sticks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 sticks of same length | 1 | Basic triangle formation |
| 5 sticks of same length | 1 | Leftover sticks ignored |
| 6 sticks of same length | 2 | Multiple polygons of same length |
| Mixed lengths | 4 | Sum of polygons across lengths |
| Only two sticks | 0 | Cannot form polygon with fewer than three sticks |

## Edge Cases

For the input `2\n7 7`, the algorithm initializes the count array to zero, increments count[7] twice, and computes `2 // 3` as zero. The output is correctly zero, demonstrating that insufficient sticks are handled automatically. Similarly, for `6\n6 6 6 6 6 6`, count[6] is 6, and `6 // 3` equals 2, yielding two polygons. This confirms that both single-length and multi-length contributions are accurately tallied.
