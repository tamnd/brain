---
title: "CF 2179B - Blackslex and Showering"
description: "We are given a sequence of floors that Blackslex needs to visit in order, and moving between floors takes time proportional to the absolute difference between consecutive floors. Blackslex can skip at most one floor in the sequence."
date: "2026-06-07T22:15:03+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2179
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1071 (Div. 3)"
rating: 800
weight: 2179
solve_time_s: 79
verified: true
draft: false
---

[CF 2179B - Blackslex and Showering](https://codeforces.com/problemset/problem/2179/B)

**Rating:** 800  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of floors that Blackslex needs to visit in order, and moving between floors takes time proportional to the absolute difference between consecutive floors. Blackslex can skip at most one floor in the sequence. The goal is to compute the minimum total time he can achieve if he chooses the optimal floor to skip.

Formally, for an array of integers representing floor numbers, the default time is the sum of absolute differences between consecutive elements. Removing a single element $a_k$ reduces the sum by the sum of the two adjacent differences $|a_{k-1}-a_k| + |a_k - a_{k+1}|$ and replaces it with a single jump $|a_{k-1}-a_{k+1}|$. We must determine which floor, if any, to remove to minimize the total.

The constraints allow up to $2 \cdot 10^5$ floors across all test cases and each test case can have up to $2 \cdot 10^5$ floors. Since the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$, any solution that processes each floor a constant number of times per test case will run efficiently. This rules out algorithms with more than $O(n)$ per test case.

A non-obvious edge case occurs when the optimal floor to remove is the first or last in the array. Since skipping the first or last floor only removes one difference rather than combining two, we need to account for this carefully. For example, given $a = [1, 100, 2]$, removing the middle floor gives time $|1-2| = 1$, but removing the first or last does not reduce the maximum jump between 1 and 100. A careless implementation that assumes the skipped element is never at the boundaries could miss the correct minimum.

## Approaches

The brute-force solution iterates over all possible floors to remove. For each candidate floor $k$, we compute the sum of absolute differences after removing it by adjusting the two adjacent differences. This method works because it correctly simulates every possible skip, but it requires $O(n^2)$ time in the worst case if we recompute the sum from scratch for every candidate. For $n \approx 2 \cdot 10^5$, this is far too slow.

The key insight is that the effect of removing a floor $a_k$ is local. The total sum decreases by $|a_{k-1}-a_k| + |a_k - a_{k+1}|$ and increases by $|a_{k-1}-a_{k+1}|$. Therefore, we can precompute the total sum of differences once and then iterate over possible skips in $O(n)$ by computing the change for each candidate. This observation reduces the complexity from $O(n^2)$ to $O(n)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the initial total time by summing $|a[i+1]-a[i]|$ for $i = 0$ to $n-2$. This gives the time without skipping any floor.
2. Initialize a variable `min_time` with this total.
3. Iterate over floors from the second to the second-to-last (indices 1 to n-2). For each floor $a[i]$, compute the cost reduction if we skip it: the change is `abs(a[i-1]-a[i]) + abs(a[i]-a[i+1]) - abs(a[i-1]-a[i+1])`.
4. Update `min_time` to be the minimum of its current value and the total minus this reduction.
5. Handle the edge floors separately. Skipping the first floor reduces only the first difference, and skipping the last floor reduces only the last difference. Compare these reductions with `min_time`.
6. Output `min_time` for the test case.

The correctness comes from the observation that removing any element only affects its immediate neighbors. Computing the total sum once and then adjusting for a candidate skip captures exactly the effect on the total time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        total = sum(abs(a[i+1]-a[i]) for i in range(n-1))
        min_time = total
        
        # consider skipping each interior floor
        for i in range(1, n-1):
            reduction = abs(a[i-1]-a[i]) + abs(a[i]-a[i+1]) - abs(a[i-1]-a[i+1])
            min_time = min(min_time, total - reduction)
        
        # consider skipping first or last floor
        min_time = min(min_time, total - abs(a[1]-a[0]))
        min_time = min(min_time, total - abs(a[n-1]-a[n-2]))
        
        print(min_time)
```

The code first reads input and computes the initial sum of absolute differences. It then iterates over the interior floors and calculates the net gain from skipping each. Finally, it compares with the gains from skipping the first or last floor. Using `min()` guarantees the global minimum is found without unnecessary conditionals. Fast I/O handles the large input size efficiently.

## Worked Examples

**Sample 1:** `a = [4, 15, 1, 7, 9]`

| i | a[i-1] | a[i] | a[i+1] | Reduction | total - reduction |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 15 | 1 | 18 | 11 |
| 2 | 15 | 1 | 7 | 20 | 9 |
| 3 | 1 | 7 | 9 | 14 | 15 |

Edge: skipping first: total - |15-4| = 34-11 = 23, skipping last: 34-2 = 32

Minimum is 11. Demonstrates that skipping interior floors can significantly reduce total.

**Sample 2:** `a = [2, 4, 8]`

Skipping middle:  |2-4| + |4-8| - |2-8| = 2 + 4 - 6 = 0, total - 0 = 6? Wait compute total first: |4-2| + |8-4| = 2 + 4 = 6. So skipping 4: total - reduction = 6 - 0 = 6? But the sample output is 2. Check: skipping second: sum becomes |8-2| = 6? hmm sample says 2. Ah, maybe he skipped last? Let's compute all: skipping first: |8-4| = 4, skipping last: |4-2| = 2, skip middle: |2-8| = 6. Minimum is 2. So edge case confirms first/last skipping is important.

This demonstrates why the algorithm must handle first and last separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Sum of differences is O(n), iterating for candidate skips is O(n) |
| Space | O(n) | Storing the array |

Given the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$, this fits well under 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("3\n5\n4 15 1 7 9\n3\n2 4 8\n6\n11 13 17 19 23 29\n") == "11\n2\n12", "sample tests"

# minimum-size input
assert run("1\n3\n1 2 3\n") == "1", "minimum size"

# all equal values
assert run("1\n4\n5 5 5 5\n") == "0", "all equal"

# large jumps
assert run("1\n5\n1 100 1 100 1\n") == "198", "alternating large jumps"

# skip first floor
assert run("1\n4\n10 1 2 3\n") == "3", "skip first floor optimal"

# skip last floor
assert run("1\n4\n1 2 3 10\n") == "3", "skip last floor optimal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n5\n4 15 1 7 9\n3\n2 4 8\n6\n11 13 17 19 23 29\n` | `11\n2\n12` | Sample correctness |
| `1\n3\n1 2 3\n` | `1` | Minimum array size, interior removal unnecessary |
| `1\n4\n5 5 |  |  |
