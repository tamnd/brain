---
title: "CF 1197A - DIY Wooden Ladder"
description: "We are given a collection of wooden planks of various lengths, and we want to assemble the tallest possible ladder where the ladder has steps and a base."
date: "2026-06-12T00:08:08+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1197
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 69 (Rated for Div. 2)"
rating: 900
weight: 1197
solve_time_s: 275
verified: false
draft: false
---

[CF 1197A - DIY Wooden Ladder](https://codeforces.com/problemset/problem/1197/A)

**Rating:** 900  
**Tags:** greedy, math, sortings  
**Solve time:** 4m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of wooden planks of various lengths, and we want to assemble the tallest possible ladder where the ladder has steps and a base. A $k$-step ladder consists of $k+2$ planks: two for the base, each of length at least $k+1$, and $k$ planks for the steps, each of length at least 1. We cannot cut the planks, so each plank must be used as-is. The task is to determine the maximum number of steps $k$ we can build using some subset of the planks.

The input gives multiple queries. Each query provides the number of planks $n$ and an array of their lengths. The output is the largest integer $k$ for each query, or 0 if no ladder can be formed.

Given that $n$ can be as large as $10^5$ per query and the total $n$ across all queries does not exceed $10^5$, we need an algorithm that is linear or near-linear in $n$, because anything quadratic would perform up to $10^{10}$ operations in the worst case and be too slow. This rules out naive combinatorial checking of every subset of planks.

Edge cases arise when the planks are too short to form a base. For example, if we have lengths `[1, 1, 1]`, the longest base possible requires two planks of length at least 2 (since $k \ge 1$), which is impossible. A careless approach that ignores the base requirement might return $k=1$, which is incorrect. Another edge case is when all planks are very long - the algorithm must still respect that $k$ cannot exceed $n-2$ since at least two planks are reserved for the base.

## Approaches

A brute-force approach would try all possible $k$ values from 1 up to $n-2$, checking for each $k$ if there exist two planks of length at least $k+1$ for the base and at least $k$ remaining planks for the steps. Sorting all possible combinations or iterating subsets is infeasible because it could require $O(2^n)$ operations, far exceeding our time budget.

The key observation is that we do not need to check all subsets explicitly. Once we sort the planks, the largest two planks can serve as the base, and the remaining planks are candidates for steps. If we choose the largest planks for the base, the maximum $k$ is limited by the smaller of two quantities: the number of remaining planks (`n-2`) and the length of the shorter base plank minus 1 (because the base plank must be at least $k+1$). This yields the formula:

```
k = min(n-2, min(base1, base2)-1)
```

where `base1` and `base2` are the two largest planks after sorting. This is optimal because any larger $k$ would violate either the step count or base length constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal (sort and take two largest) | O(n log n) | O(1) additional | Accepted |

## Algorithm Walkthrough

1. For each query, read the number of planks $n$ and the array of lengths.
2. Sort the array in non-decreasing order. Sorting allows us to quickly identify the two longest planks to serve as the base.
3. Assign `base1` and `base2` to the last two elements in the sorted array. `base1` is the largest, `base2` the second largest.
4. Compute the candidate maximum step count `k_candidate` as `min(base2 - 1, n - 2)`. `base2 - 1` ensures the base plank length requirement, and `n - 2` ensures we have enough planks for the steps.
5. If `k_candidate` is less than 1, output 0; otherwise output `k_candidate`.

Why it works: By always selecting the two largest planks as the base, we maximize the potential height of the ladder. Any smaller planks cannot allow a larger $k$ because the base requirement is stricter than the step requirement. The formula `min(base2 - 1, n - 2)` respects both constraints simultaneously. Sorting guarantees we correctly identify the two largest planks efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        if n < 2:
            print(0)
            continue
        a.sort()
        base1, base2 = a[-1], a[-2]
        k = min(base2 - 1, n - 2)
        print(max(k, 0))

if __name__ == "__main__":
    solve()
```

The solution first reads all inputs efficiently using `sys.stdin.readline`. Sorting ensures we can pick the two longest planks. `base2 - 1` gives the maximum number of steps the base can support, and `n - 2` gives the maximum number of steps available from remaining planks. Using `max(k, 0)` handles the edge case where a ladder cannot be formed.

## Worked Examples

### Sample 1

Input: `[1, 3, 1, 3]`

Sorted: `[1, 1, 3, 3]`

`base1=3`, `base2=3`

`k = min(3-1, 4-2) = min(2, 2) = 2`

Output: 2

This demonstrates that both the base and step constraints are correctly enforced.

### Sample 2

Input: `[3, 3, 2]`

Sorted: `[2, 3, 3]`

`base1=3`, `base2=3`

`k = min(3-1, 3-2) = min(2, 1) = 1`

Output: 1

Here the number of planks limits the ladder more than the base length, showing that both constraints must be considered simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per query | Sorting dominates; scanning the last two elements is O(1) |
| Space | O(n) | Storing the plank array for sorting |

Given $n \le 10^5$ total, the worst-case operations are around $10^5 \log 10^5$, which fits within 2 seconds comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n4\n1 3 1 3\n3\n3 3 2\n5\n2 3 3 4 2\n3\n1 1 2\n") == "2\n1\n2\n0", "samples"

# Custom cases
assert run("2\n2\n1 1\n3\n100 100 100\n") == "0\n1", "minimum and equal long planks"
assert run("1\n5\n1 2 3 4 5\n") == "3", "medium range plank lengths"
assert run("1\n3\n1 2 2\n") == "1", "base length constraint tighter than steps"
assert run("1\n6\n10 10 1 1 1 1\n") == "4", "large base planks, plenty of steps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n2\n1 1\n3\n100 100 100\n` | `0\n1` | handles minimum planks and all-equal large planks |
| `1\n5\n1 2 3 4 5\n` | `3` | confirms correct computation when step count limits k |
| `1\n3\n1 2 2\n` | `1` | ensures base length is respected over step count |
| `1\n6\n10 10 1 1 1 1\n` | `4` | tests scenario with abundant steps but large base planks |

## Edge Cases

When only two planks are available and both are too short to form even a 1-step ladder, the algorithm correctly returns 0. For input `[1, 1]`, sorting yields `[1, 1]`, `base2 - 1 = 0`, `n-2=0`, and `max(k, 0)=0`.

When planks are extremely long, like `[100000, 100000, 100000]`, sorting yields `[100000, 100000, 100000]`, `base2 - 1=99999`, `n-2=1`, so `k = min(99999, 1)=1`. This shows the step count constraint can limit the ladder, even if the base planks are enormous.
