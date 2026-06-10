---
title: "CF 1467B - Hills And Valleys"
description: "We are given a sequence of integers and need to identify \"hills\" and \"valleys\" in it. A hill occurs at position j if the number there is strictly greater than both neighbors, while a valley occurs if it is strictly smaller than both neighbors."
date: "2026-06-11T01:38:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1467
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 695 (Div. 2)"
rating: 1700
weight: 1467
solve_time_s: 103
verified: true
draft: false
---

[CF 1467B - Hills And Valleys](https://codeforces.com/problemset/problem/1467/B)

**Rating:** 1700  
**Tags:** brute force, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and need to identify "hills" and "valleys" in it. A hill occurs at position `j` if the number there is strictly greater than both neighbors, while a valley occurs if it is strictly smaller than both neighbors. The sum of hills and valleys in a sequence is called the intimidation value. We are allowed to change exactly one number in the sequence to any integer, or leave the sequence unchanged, and we want the minimum possible intimidation value after this single change.

The input consists of multiple test cases. Each test case provides the length of the sequence and the sequence itself. The output is one number per test case: the minimal intimidation value achievable.

The constraints are such that the total length of all sequences across all test cases does not exceed 300,000. Since each test case can be as large as 300,000 elements, an $O(n^2)$ approach will be too slow. We need a solution that is linear or near-linear in the size of each sequence.

Edge cases arise when sequences have very few elements, such as three elements, where only the middle element can be a hill or a valley, or sequences where all numbers are equal, which have zero hills and valleys. Careless implementations might try to adjust elements without checking boundaries or might count hills and valleys incorrectly if adjacent changes are ignored.

## Approaches

The brute-force approach iterates over every possible position in the sequence, tries changing it to every possible integer, recalculates the entire intimidation value, and keeps the minimum. This approach is correct in principle but completely impractical. If we attempt to test all values up to $10^9$ for each element, the number of operations explodes, far exceeding feasible limits.

The key insight for optimization comes from the observation that changing a number only affects hills and valleys in its immediate neighborhood - specifically, the index itself and its two adjacent indices. Therefore, we do not need to recalculate the entire sequence each time; we only need to consider the local contribution of hills and valleys around the changed element.

We can precompute the initial hills and valleys for the whole sequence. Then for each candidate position `i` (except the first and last element), we consider three options: changing it to match the left neighbor, to match the right neighbor, or leaving it unchanged. For each option, we compute the change in the local hills and valleys (at indices `i-1`, `i`, and `i+1`). We take the option that reduces the total intimidation value the most. Repeating this for each position and keeping track of the minimum results in a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * value_range) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and the array `a`.
2. Define a helper function `is_hill_or_valley(i)` that returns `1` if `a[i]` is a hill or valley and `0` otherwise. This checks if `a[i] > a[i-1]` and `a[i] > a[i+1]` or `a[i] < a[i-1]` and `a[i] < a[i+1]`.
3. Precompute the initial total intimidation value by summing `is_hill_or_valley(i)` for all `2 ≤ i ≤ n-1`.
4. Initialize `best_reduction` to zero. This will store the maximum decrease in intimidation value we can achieve with one change.
5. Iterate over indices `i` from 1 to `n-2` (0-based indexing, ignoring first and last elements):

1. Compute the current sum of hills and valleys at positions `i-1`, `i`, and `i+1`.
2. Try changing `a[i]` to `a[i-1]`. Compute the new sum at positions `i-1`, `i`, and `i+1`. Compute the reduction: old sum minus new sum. Update `best_reduction` if this is larger.
3. Repeat by changing `a[i]` to `a[i+1]`.
6. The minimal intimidation value is `initial_total - best_reduction`. Print it for the test case.

Why it works: Changing a number only affects its immediate neighbors. By evaluating all relevant local modifications and taking the one that reduces the local sum the most, we guarantee that we find the optimal single-change reduction. No global recalculation is necessary beyond these local neighborhoods.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_hill_or_valley(a, i):
    return (a[i] > a[i-1] and a[i] > a[i+1]) or (a[i] < a[i-1] and a[i] < a[i+1])

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n < 3:
            print(0)
            continue
        hills_valleys = [0] * n
        total = 0
        for i in range(1, n-1):
            if is_hill_or_valley(a, i):
                hills_valleys[i] = 1
                total += 1
        best_reduction = 0
        for i in range(1, n-1):
            original = [hills_valleys[j] for j in range(max(0,i-1), min(n,i+2))]
            current_sum = sum(original)
            for new_val in [a[i-1], a[i+1]]:
                old = a[i]
                a[i] = new_val
                new = [1 if 1 <= j <= n-2 and is_hill_or_valley(a, j) else 0 for j in range(max(0,i-1), min(n,i+2))]
                reduction = current_sum - sum(new)
                best_reduction = max(best_reduction, reduction)
                a[i] = old
        print(total - best_reduction)

if __name__ == "__main__":
    solve()
```

The code precomputes hills and valleys in `hills_valleys`. The nested loop over `i` tests changing `a[i]` to the values of its neighbors. Using slices ensures we only recalculate the local effect for `i-1`, `i`, `i+1`. Restoring `a[i]` after each attempt avoids side effects across iterations. Special handling of `n < 3` avoids index errors.

## Worked Examples

### Sample 1

Input: `[1, 5, 3]`

Initial hills/valleys: index 1 is a hill (5 > 1, 5 > 3), total = 1.

Changing `5` to `1` or `3` removes the hill.

Reduction = 1, final minimal intimidation value = 0.

| i | a[i] change | local old sum | local new sum | reduction | best_reduction |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 | 1 |
| 1 | 3 | 1 | 0 | 1 | 1 |

### Sample 2

Input: `[2, 2, 2, 2, 2]`

All elements equal, no hills or valleys, total = 0.

Any change cannot improve the total further. Output = 0.

| i | a[i] change | local old sum | local new sum | reduction | best_reduction |
| --- | --- | --- | --- | --- | --- |
| 1..3 | 2 (neighbor) | 0 | 0 | 0 | 0 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each index is checked at most twice, with constant-time neighborhood calculations |
| Space | O(n) | Storing hills and valleys for each index |

The linear time per test case ensures that with the sum of `n` over all test cases ≤ 300,000, the solution runs comfortably within 1 second. Memory usage is linear, fitting within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n1 5 3\n5\n2 2 2 2 2\n6\n1 6 2 5 2 10\n5\n1 6 2 5 1\n") == "0\n0\n1\n0"

# Minimum size input
assert run("1\n1\n100\n") == "0", "single element"

# Two elements, no hills or valleys
assert run("1\n2\n3 3\n") == "0", "two elements"

# Maximum-size input, all equal
assert run(f"1\n300000\n{' '.join(['1']*300000)}\n") == "0", "all equal large"

# Peaks at boundaries
assert run("1\n5\n10 1 10 1 10\n") == "1", "alternating peaks"

# Random peaks
assert run("1
```
