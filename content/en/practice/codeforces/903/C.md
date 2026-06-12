---
title: "CF 903C - Boxes Packing"
description: "We are given n cubic boxes, each with a side length specified by an array a. Mishka wants to nest these boxes inside each other according to strict rules: a box can go into another box only if it is strictly smaller and the larger box does not already contain another box."
date: "2026-06-12T22:54:11+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 903
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 34 (Rated for Div. 2)"
rating: 1200
weight: 903
solve_time_s: 315
verified: true
draft: false
---

[CF 903C - Boxes Packing](https://codeforces.com/problemset/problem/903/C)

**Rating:** 1200  
**Tags:** greedy  
**Solve time:** 5m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given *n* cubic boxes, each with a side length specified by an array *a*. Mishka wants to nest these boxes inside each other according to strict rules: a box can go into another box only if it is strictly smaller and the larger box does not already contain another box. The goal is to minimize the number of visible boxes, which are boxes not contained in any other box. Essentially, we want to create chains of nested boxes where the length of each chain is as long as possible, so that as many boxes as possible are hidden inside others.

The input constraint allows *n* up to 5000. This rules out brute-force approaches that try all permutations or all pairwise nestings in an exhaustive manner, because *n!* or even *n²* operations could approach 25 million or higher, which is too slow in Python for worst-case inputs if the algorithm is not simple and tight. Each box size can be up to 10⁹, which means we cannot rely on frequency arrays with indices corresponding to size, but counting duplicates is feasible. 

The tricky edge cases involve boxes of equal size. For example, consider `3 3 3`. No box can go inside another because nesting requires strictly smaller size. The correct minimum number of visible boxes is 3. A naive approach that ignores duplicates might try to nest them incorrectly and undercount the visible boxes. Another subtle scenario is when one size occurs many times, e.g., `1 2 2 2 3`. We must ensure that no more boxes of the same size are nested than allowed, which is equivalent to treating boxes of the same size as independent and counting the maximum frequency of any size.

## Approaches

A brute-force method would attempt to simulate all possible nesting configurations. We could try sorting the boxes and then iteratively attempting to place each box into any larger box that is currently empty. While this would eventually produce a correct answer, it requires checking each pair repeatedly, potentially O(n²), and managing which boxes are free to contain others, which becomes messy and inefficient. For 5000 boxes, this could lead to roughly 25 million operations and is close to the time limit in Python, especially with frequent list manipulations.

The key observation is that the boxes only differ in size, and nesting constraints are entirely determined by size comparisons. This reduces the problem to counting how many boxes of each size exist. Each visible box must be at least as frequent as the maximum occurrence of any size, because we cannot nest identical boxes. If a size occurs five times and larger sizes occur fewer times, we need at least five visible boxes to accommodate all of them without violating the strict nesting rule. Sorting and counting frequencies allow us to identify this maximum count efficiently. Therefore, the problem reduces to computing the frequency of each box size and taking the largest count. This insight transforms a potentially messy simulation into a clean, O(n log n) algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of boxes, *n*, and the array of box sizes, *a*. This sets up the input for processing.
2. Sort the array *a*. Sorting ensures that all equal-sized boxes are contiguous and makes counting frequencies straightforward.
3. Initialize a counter variable to track the frequency of the current size and a variable `max_count` to store the largest frequency seen.
4. Iterate through the sorted array. For each box, check if it is the same as the previous one. If it is, increment the counter. If it is different, reset the counter to 1.
5. After updating the counter for each box, update `max_count` if the current counter exceeds it. This guarantees that `max_count` always holds the frequency of the most common size.
6. After processing all boxes, output `max_count` as the minimum number of visible boxes. This is correct because the maximum frequency dictates the number of boxes that cannot be nested into each other due to the strict size requirement.

Why it works: The invariant is that for any size that occurs *k* times, at least *k* boxes must remain visible, because no two identical boxes can nest. Sorting ensures that we see all identical boxes consecutively, and tracking the maximum frequency guarantees that the output is never smaller than the necessary minimum. No configuration can reduce the visible count below this maximum frequency, so the solution is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
a.sort()

max_count = 0
current_count = 0
prev = None

for size in a:
    if size == prev:
        current_count += 1
    else:
        current_count = 1
        prev = size
    if current_count > max_count:
        max_count = current_count

print(max_count)
```

The solution starts by sorting the boxes so that identical sizes are adjacent. We initialize `current_count` to count consecutive identical boxes. Each time we encounter a new size, we reset `current_count` to 1. `max_count` tracks the largest frequency. Sorting is critical because it allows us to scan the array in one pass without missing duplicates. Forgetting to reset the counter when a new size is encountered would lead to an overcount. Using a separate variable `prev` is safer than relying on index arithmetic, which can cause off-by-one errors.

## Worked Examples

**Sample Input 1**

```
3
1 2 3
```

| size | prev | current_count | max_count |
|------|------|---------------|-----------|
| 1    | None | 1             | 1         |
| 2    | 1    | 1             | 1         |
| 3    | 2    | 1             | 1         |

The largest frequency is 1, so only one visible box is required. Boxes can nest completely into one chain: 1 inside 2 inside 3.

**Sample Input 2**

```
5
2 2 3 3 3
```

| size | prev | current_count | max_count |
|------|------|---------------|-----------|
| 2    | None | 1             | 1         |
| 2    | 2    | 2             | 2         |
| 3    | 2    | 1             | 2         |
| 3    | 3    | 2             | 2         |
| 3    | 3    | 3             | 3         |

The maximum frequency is 3, so at least three visible boxes are required. The first chain can nest a 2 into a 3, leaving three visible boxes of size 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n log n) | Sorting dominates the complexity, the subsequent scan is O(n) |
| Space | O(n) | Storing the array of sizes and a few counters |

For n up to 5000, O(n log n) corresponds to roughly 65,000 operations, which is well within the 1-second time limit. Memory usage is minimal, fitting comfortably within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    max_count = 0
    current_count = 0
    prev = None

    for size in a:
        if size == prev:
            current_count += 1
        else:
            current_count = 1
            prev = size
        if current_count > max_count:
            max_count = current_count
    return str(max_count)

# provided samples
assert run("3\n1 2 3\n") == "1", "sample 1"
assert run("5\n2 2 3 3 3\n") == "3", "sample 2"

# custom cases
assert run("1\n7\n") == "1", "single box"
assert run("4\n5 5 5 5\n") == "4", "all equal boxes"
assert run("6\n1 2 2 1 5 3\n") == "2", "duplicates mixed"
assert run("5\n10 20 10 20 10\n") == "3", "high-low-high pattern"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1\n7 | 1 | Single box edge case |
| 4\n5 5 5 5 | 4 | All boxes equal, no nesting possible |
| 6\n1 2 2 1 5 3 | 2 | Duplicates require tracking frequency |
| 5\n10 20 10 20 10 | 3 | Ensures correct maximum frequency handling |

## Edge Cases

For input `3 3 3`, the algorithm sorts the array as `[3, 3, 3]`. It counts the frequency of 3 as 3. Since no box can nest into another of the same size, all three boxes remain visible. The output is correctly 3.

For a single box input `1`, the array `[1]` results in `max_count = 1`, which is correct. For a sequence with alternating sizes, the algorithm correctly resets the counter at each size change and tracks the maximum frequency,
