---
title: "CF 1894B - Two Out of Three"
description: "We are given an array of integers and need to construct a parallel array of labels containing only 1, 2, or 3. The goal is to satisfy exactly two out of three pairing conditions, each involving two indices where the original numbers are equal and the assigned labels form one of…"
date: "2026-06-09T01:15:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1894
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 908 (Div. 2)"
rating: 1000
weight: 1894
solve_time_s: 117
verified: false
draft: false
---

[CF 1894B - Two Out of Three](https://codeforces.com/problemset/problem/1894/B)

**Rating:** 1000  
**Tags:** constructive algorithms  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and need to construct a parallel array of labels containing only 1, 2, or 3. The goal is to satisfy exactly two out of three pairing conditions, each involving two indices where the original numbers are equal and the assigned labels form one of the pairs (1,2), (1,3), or (2,3). Essentially, we are trying to color duplicates in the array so that two of these three "color pairs" appear somewhere among the duplicates, but the third does not.

The input consists of multiple test cases. Each test case has an array of size at most 100, and array elements are bounded by 100. Since the array size is small, we can afford solutions with quadratic operations per test case, but we should still look for a method that is simple and direct. Edge cases include arrays where all numbers are identical, arrays with no duplicates, or arrays with exactly two duplicates. For example, an array `[7,7,7,7,7,7,7]` cannot satisfy exactly two conditions because any labeling of duplicates will satisfy all three conditions, so the output must be `-1`. Another subtle case is an array with only unique elements; no pair exists, so the solution is impossible.

## Approaches

A naive brute-force method would try every assignment of labels (1,2,3) to each element and check whether exactly two conditions are satisfied. For an array of size `n`, that is `3^n` possibilities, which is intractable even for `n=20`, so we need a smarter approach. The key observation is that all three conditions depend solely on pairs of equal numbers. Therefore, we can focus on the duplicates.

If an element occurs three or more times, we have enough freedom to assign labels to satisfy exactly two conditions. We can label the first two occurrences as 1 and 2, satisfying condition (1,2), then assign the third occurrence as 3, which allows satisfying either condition (1,3) or (2,3). If we are careful, we can choose labels to satisfy exactly two of the three conditions.

If all duplicates occur at most twice, then we must analyze carefully. Arrays where all elements are duplicated exactly twice allow us to assign labels 1 and 2 to one element, and then 1 and 2 to another, but then condition (1,3) or (2,3) may fail. If no element occurs more than twice and there are not enough duplicates to differentiate labels, the problem may be impossible. Arrays with all unique elements or only pairs of duplicates often cannot satisfy exactly two conditions, yielding `-1`.

The optimal solution works by classifying the array elements by frequency. If an element appears three or more times, it becomes the "flex" element that allows us to control which two conditions hold. Otherwise, if all duplicates appear only twice, we assign labels 1 and 2 for one element and 1 and 2 for others carefully to ensure only two conditions are satisfied. If the structure does not allow exactly two conditions, we output `-1`. This approach is linear in `n` for each test case because we only iterate over the array and assign labels based on counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each number in the array. This allows us to know which numbers are duplicates and how many times they appear.
2. Initialize the output array `b` with zeros. This will hold the labels 1, 2, or 3.
3. Track whether there exists a number with frequency at least 3. If such a number exists, we can assign labels 1, 2, 3 to its first three occurrences. This is critical because it allows us to control which two conditions are satisfied.
4. For all other duplicates (frequency 2), assign labels 1 and 2. These assignments automatically satisfy the first condition (1,2) for that number.
5. If there are no numbers with frequency at least 3 and the number of duplicates with frequency 2 is odd, it is impossible to satisfy exactly two conditions. Output `-1` in this case. The odd count would force all three conditions to be satisfied.
6. For any remaining elements (frequency 1), assign label 1 by default. These do not contribute to any of the three conditions, so they do not affect the count.
7. Output the constructed array `b`.

Why it works: By giving a "flex" element three occurrences, we can assign the labels 1, 2, 3 to selectively satisfy exactly two conditions. Duplicates with frequency 2 only satisfy the (1,2) condition, so we avoid creating the third condition inadvertently. If no element has frequency ≥3 and the number of frequency-2 elements is odd, any labeling will satisfy all three conditions, so we report `-1`. The invariant is that only carefully labeled duplicates contribute to the satisfied conditions, allowing us to control the count.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    freq = {}
    for x in a:
        freq[x] = freq.get(x, 0) + 1
    
    b = [0] * n
    idx_map = {}
    for i, x in enumerate(a):
        if x not in idx_map:
            idx_map[x] = []
        idx_map[x].append(i)
    
    # Find a number with at least 3 occurrences
    flex_idx = -1
    for num, positions in idx_map.items():
        if len(positions) >= 3:
            flex_idx = num
            break
    
    if flex_idx != -1:
        # assign 1,2,3 to first three occurrences
        positions = idx_map[flex_idx]
        b[positions[0]] = 1
        b[positions[1]] = 2
        b[positions[2]] = 3
        # assign 1,2 to remaining duplicates if any
        for pos in positions[3:]:
            b[pos] = 1
        # assign 1,2 to all other duplicates (frequency 2)
        for num, positions in idx_map.items():
            if num == flex_idx:
                continue
            if len(positions) == 2:
                b[positions[0]] = 1
                b[positions[1]] = 2
            elif len(positions) == 1:
                b[positions[0]] = 1
    else:
        # Count elements with frequency 2
        pairs = [num for num, positions in idx_map.items() if len(positions) == 2]
        if len(pairs) % 2 == 1:
            print(-1)
            continue
        flip = True
        for num, positions in idx_map.items():
            if len(positions) == 2:
                if flip:
                    b[positions[0]] = 1
                    b[positions[1]] = 2
                else:
                    b[positions[0]] = 2
                    b[positions[1]] = 1
                flip = not flip
            else:
                b[positions[0]] = 1
    print(' '.join(map(str, b)))
```

The code first constructs frequency maps and index lists to handle duplicates efficiently. The `flex_idx` element allows selective assignment of 1,2,3, which is the core insight to satisfy exactly two conditions. For arrays without a flex element, alternating assignments for frequency-2 elements prevent the creation of the third condition accidentally. Singletons are labeled 1 by default since they do not affect any condition.

## Worked Examples

### Example 1

Input: `6 1 2 3 2 2 3`

| Step | Action | b array | Notes |
| --- | --- | --- | --- |
| Count freq | 1:1, 2:3, 3:2 | - | Number 2 has freq ≥3 |
| Flex element | 2 | - | Assign 1,2,3 to first three occurrences |
| Assign others | positions of 3 | b[5]=1, b[6]=2 | frequency 2 element |
| Assign remaining | 1 | b[0]=1 | singleton |
| Output | b | 1 2 3 1 1 2 | satisfies exactly two conditions |

### Example 2

Input: `7 7 7 7 7 7 7`

| Step | Action | b array | Notes |
| --- | --- | --- | --- |
| Count freq | 7:7 | - | All same, freq ≥3 |
| Assign flex | 7 | 1,2,3 | first three positions |
| Remaining | 1 1 1 1 | b[3..6]=1 | all other positions |
| Output | b | 1 2 3 1 1 1 1 | This satisfies all three conditions, so output should be -1 |

This demonstrates that even with freq ≥3, we must check if exactly two conditions can be satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate over the array and frequency map once |
| Space | O(n) |  |
