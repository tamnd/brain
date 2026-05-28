---
title: "CF 25A - IQ test"
description: "We are given a sequence of n natural numbers, where n is at least 3 and at most 100, and each number is at most 100. Amo"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 25
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 25 (Div. 2 Only)"
rating: 1300
weight: 25
solve_time_s: 67
verified: true
draft: false
---

[CF 25A - IQ test](https://codeforces.com/problemset/problem/25/A)

**Rating:** 1300  
**Tags:** brute force  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of `n` natural numbers, where `n` is at least 3 and at most 100, and each number is at most 100. Among these numbers, all except one share the same parity - either even or odd - and exactly one number differs. Our task is to identify the position of this “odd-one-out” number in the sequence, counting positions starting from 1.

The problem is small in scale. With `n` limited to 100, we can afford algorithms that examine each number directly without worrying about efficiency. The primary difficulty lies not in raw computation but in correctly identifying which number breaks the pattern of parity.

A subtle edge case occurs when the first few numbers do not clearly establish the majority parity. For example, if the sequence is `3 2 7`, we cannot immediately conclude the majority parity by just looking at the first two numbers - careful inspection is needed to ensure we pick the single number that truly differs.

## Approaches

The most straightforward approach is brute force: for each number, count how many numbers are even and how many are odd, then pick the one that has a different parity from the majority. This method works because we are guaranteed that exactly one number is different. For `n` up to 100, this requires at most a few hundred operations - trivial for modern processors - so performance is not a concern.

The key insight that allows a cleaner solution is that we do not need to examine the whole sequence to determine the majority parity. Looking at the first three numbers is sufficient. If at least two of these numbers share the same parity, that parity is the majority. Once we know the majority parity, we can scan the sequence once to find the number that differs. This reduces unnecessary checks and makes the logic straightforward and robust.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of elements `n` and the sequence of numbers. We need the numbers in a list so we can index them.
2. Compute the parity of the first three numbers by taking each modulo 2. These three parities determine the majority parity in the sequence because at least two of them must match.
3. Identify the majority parity. If two or more of the first three numbers are even, the majority is even; otherwise, the majority is odd.
4. Iterate over the full sequence of numbers. For each number, compute its parity and compare it with the majority parity.
5. As soon as we find a number whose parity does not match the majority, output its position (1-based index) and terminate. This is guaranteed to be the unique number with different parity.

Why it works: The invariant is that exactly one number differs from the rest. By determining the majority parity from the first three numbers, we guarantee that scanning the rest of the sequence will correctly identify the outlier without ambiguity. Since the input guarantee ensures a single different parity, we never risk a false positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))

# determine majority parity from the first three numbers
first_three = nums[:3]
parities = [x % 2 for x in first_three]
majority_parity = 0 if parities.count(0) > 1 else 1

# find the index of the number with different parity
for i, num in enumerate(nums):
    if num % 2 != majority_parity:
        print(i + 1)
        break
```

The code first slices the first three elements to establish the majority parity. Counting zeros in `parities` checks how many are even. The loop then directly searches for a number that violates the majority parity. We add 1 to the index to convert from 0-based Python indexing to the 1-based indexing required by the problem.

## Worked Examples

**Example 1:**

Input: `5 2 4 7 8 10`

| Step | Variable | Value |
| --- | --- | --- |
| Read input | n | 5 |
| Read input | nums | [2, 4, 7, 8, 10] |
| First three parities | parities | [0, 0, 1] |
| Majority parity | majority_parity | 0 (even) |
| Iteration | i=2, num=7 | 7 % 2 = 1 ≠ 0 → output 3 |

The table shows the algorithm correctly identifies 7 as the number differing in parity.

**Example 2:**

Input: `4 1 1 2 1`

| Step | Variable | Value |
| --- | --- | --- |
| Read input | n | 4 |
| Read input | nums | [1, 1, 2, 1] |
| First three parities | parities | [1, 1, 0] |
| Majority parity | majority_parity | 1 (odd) |
| Iteration | i=2, num=2 | 2 % 2 = 0 ≠ 1 → output 3 |

Here, the edge case where the outlier appears as the third number demonstrates that majority parity detection works with just the first three elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the first three elements to determine the majority, then iterate the full array once. Maximum n = 100, so this is trivial. |
| Space | O(n) | We store the sequence of numbers in a list; additional variables are negligible. |

The algorithm easily fits within the 2-second limit and 256 MB memory cap, even at the largest `n = 100`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n = int(input())
    nums = list(map(int, input().split()))
    first_three = nums[:3]
    parities = [x % 2 for x in first_three]
    majority_parity = 0 if parities.count(0) > 1 else 1
    for i, num in enumerate(nums):
        if num % 2 != majority_parity:
            print(i + 1)
            break
    return output.getvalue().strip()

# provided samples
assert run("5\n2 4 7 8 10\n") == "3", "sample 1"

# custom cases
assert run("3\n2 3 4\n") == "2", "edge: middle number differs"
assert run("3\n1 2 3\n") == "2", "edge: middle number differs, smallest n"
assert run("5\n1 1 1 1 2\n") == "5", "outlier at end"
assert run("4\n2 2 1 2\n") == "3", "outlier in the middle"
assert run("100\n" + " ".join(["2"]*99 + ["3"]) + "\n") == "100", "maximum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 3 4 | 2 | Outlier in middle, small n |
| 3 1 2 3 | 2 | Smallest possible sequence, middle differs |
| 5 1 1 1 1 2 | 5 | Outlier at the end |
| 4 2 2 1 2 | 3 | Outlier in the middle |
| 100 2 2 ... 3 | 100 | Maximum n, last number differs |

## Edge Cases

If the outlier is the first element, e.g., `3 2 4 6`, the first three parities are `[1, 0, 0]`, majority is even, iteration finds the first element differs and outputs `1`.

If the outlier is last, the iteration continues to the end, correctly outputs `n`.

If the outlier is in the middle, e.g., `1 1 2 1`, majority parity is determined correctly from the first three numbers, and scanning the sequence finds the third element differs.

All these edge cases confirm that using the first three elements to determine majority parity is sufficient, and the scanning loop always identifies the single number that violates the majority.

This completes a full, careful editorial suitable for a competitive programmer who wants to understand the problem deeply and re-derive the solution on similar parity-based outlier problems.
