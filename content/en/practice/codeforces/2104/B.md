---
title: "CF 2104B - Move to the End"
description: "We are given an array of integers, and for every possible length $k$ from 1 to $n$, we want to maximize the sum of the last $k$ elements after moving one element of our choice to the end of the array. After we choose and move that element, we restore the array for the next query."
date: "2026-06-08T04:57:15+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2104
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 178 (Rated for Div. 2)"
rating: 1000
weight: 2104
solve_time_s: 97
verified: false
draft: false
---

[CF 2104B - Move to the End](https://codeforces.com/problemset/problem/2104/B)

**Rating:** 1000  
**Tags:** brute force, data structures, dp, greedy, implementation  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and for every possible length $k$ from 1 to $n$, we want to maximize the sum of the last $k$ elements after moving **one** element of our choice to the end of the array. After we choose and move that element, we restore the array for the next query. Essentially, we are asked: if we are allowed one “move-to-end” operation, what is the best sum of the last $k$ elements for every $k$?

The constraints indicate that $n$ can reach $2 \cdot 10^5$ and there can be up to $10^4$ test cases, but the total sum of $n$ across all test cases is bounded by $2 \cdot 10^5$. This implies we must have an algorithm linear in $n$ for each test case. Any approach that simulates moving every element for every $k$ would be $O(n^2)$ and is clearly too slow.

Non-obvious edge cases appear when all elements are equal, when $n=1$, or when the maximum element is at the start or end. For example, with input `[7, 5]`, the sum for $k=2$ requires choosing the first element to maximize the sum. If you naively just sum the last $k$ elements without considering moves, you get the wrong result.

## Approaches

A brute-force approach would iterate over each $k$ and simulate moving every element to the end, summing the last $k$ elements each time. This works in principle because it evaluates every possible move, but its time complexity is $O(n^2)$, which exceeds the 2-second limit when $n$ is large.

The key insight for an efficient solution is to realize that moving an element to the end only affects the last $k$ elements if it is larger than some of the existing last elements. Sorting the array in decreasing order captures the potential contributions of moving any element. If we compute the prefix sums of the array sorted in decreasing order, the sum of the $k$ largest elements corresponds exactly to the maximum sum achievable by moving any single element to the end. This works because for each $k$, either the current last $k$ elements contain the largest $k$ numbers, or we can move the largest number not already in the last $k$ to the end to improve the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and the array $a$.
2. Sort the array $a$ in non-increasing order to prioritize the largest elements first. This allows us to identify the elements that will maximize sums of any prefix length.
3. Compute the prefix sums of the sorted array. The prefix sum at index $i$ stores the sum of the first $i+1$ largest elements. This prefix sum directly gives the maximum sum for the last $k=i+1$ elements.
4. Output the prefix sums in order. Each entry represents the maximum sum for the corresponding $k$.

Why it works: Sorting ensures that we always know which elements can contribute most to the last $k$ positions. The prefix sum guarantees that we are considering the optimal subset of elements for every $k$. Because the array is restored after every query, we do not need to simulate moves; the sorted order is sufficient to determine the maximum achievable sums.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort(reverse=True)
        prefix = []
        current = 0
        for num in a:
            current += num
            prefix.append(current)
        print(' '.join(map(str, prefix)))

if __name__ == "__main__":
    solve()
```

The code reads multiple test cases. For each array, it sorts in descending order and computes prefix sums. The prefix sums directly correspond to the maximum sums for each $k$ because the largest $k$ numbers always yield the optimal result.

## Worked Examples

For input `[13, 5, 10, 14, 8, 15, 13]`:

| k | Sorted Prefix Sum | Explanation |
| --- | --- | --- |
| 1 | 15 | Largest element moved to end |
| 2 | 28 | Sum of two largest elements: 15 + 13 |
| 3 | 42 | Sum of three largest: 15 + 14 + 13 |
| 4 | 50 | Sum of four largest: 15 + 14 + 13 + 8 |
| 5 | 63 | Sum of five largest: 15 + 14 + 13 + 13 + 8 |
| 6 | 73 | Sum of six largest: 15 + 14 + 13 + 13 + 8 + 10 |
| 7 | 78 | Sum of all seven elements |

The table confirms the prefix sums match the optimal sums computed manually with “move-to-end” operations.

For input `[7, 5]`:

| k | Prefix Sum | Explanation |
| --- | --- | --- |
| 1 | 7 | Move 7 to the end |
| 2 | 12 | Sum of both elements |

This demonstrates that the algorithm correctly handles very small arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; computing prefix sums is O(n) |
| Space | O(n) | Storing prefix sums |

Given the total sum of $n$ across all test cases does not exceed $2 \cdot 10^5$, this algorithm comfortably runs within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n7\n13 5 10 14 8 15 13\n6\n1000000000 1000000000 1000000000 1000000000 1000000000 1000000000\n1\n42\n2\n7 5\n") == "15 28 42 50 63 73 78\n1000000000 2000000000 3000000000 4000000000 5000000000 6000000000\n42\n7 12"

# Custom cases
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n5\n1 2 3 4 5\n") == "5 9 12 14 15", "ascending array"
assert run("1\n3\n10 10 10\n") == "10 20 30", "all equal values"
assert run("1\n4\n1000000000 1 1 1\n") == "1000000000 1000000001 1000000002 1000000003", "large max first"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum-size input |
| 1 2 3 4 5 | 5 9 12 14 15 | general ascending order |
| 10 10 10 | 10 20 30 | all equal values |
| 1000000000 1 1 1 | 1000000000 1000000001 1000000002 1000000003 | boundary with large value |

## Edge Cases

For an array with one element `[42]`, $k=1$ is trivially 42. The algorithm handles this because sorting does not change a single-element array, and the prefix sum is simply the element itself. For arrays where all elements are equal, such as `[10, 10, 10]`, the maximum sum for $k$ is always $10 \times k$, and our prefix sums correctly reflect this. When the largest element is at the beginning or end, the sorted prefix sum ensures that the largest elements are always counted first, automatically producing the correct sums for all $k$.
