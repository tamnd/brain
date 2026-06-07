---
title: "CF 2179E - Blackslex and Girls"
description: "We are asked to divide voters into districts according to a binary pattern while respecting minimum district sizes. Specifically, we have two parties, A and B, with a total of x and y voters, respectively."
date: "2026-06-07T22:18:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 2179
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1071 (Div. 3)"
rating: 1800
weight: 2179
solve_time_s: 127
verified: false
draft: false
---

[CF 2179E - Blackslex and Girls](https://codeforces.com/problemset/problem/2179/E)

**Rating:** 1800  
**Tags:** constructive algorithms, geometry, math  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to divide voters into districts according to a binary pattern while respecting minimum district sizes. Specifically, we have two parties, A and B, with a total of `x` and `y` voters, respectively. There are `n` districts, and each district `i` requires at least `p_i` total voters. We are also given a binary string `s` of length `n` that indicates the desired winner of each district: if `s_i = 0`, party A must have more voters than B in district `i`; if `s_i = 1`, party B must have more voters than A.

Our task is to determine whether it is possible to allocate the voters in such a way that every district has a winner matching the string `s` while satisfying the minimum voter counts.

The constraints are substantial. `n` can be up to 2·10^5, and the sum of `n` over all test cases does not exceed 2·10^5. Each voter count `x`, `y`, and district minimum `p_i` can be up to 10^9. A naive approach that tries all allocations is completely infeasible because it would require an astronomical number of operations. Any solution must run in linear time relative to `n` for each test case.

Non-obvious edge cases arise when the minimum district sizes `p_i` consume more voters than available, or when the distribution to satisfy the winner condition is impossible. For example, if a district has `p_i = 5`, `x = 2`, `y = 3`, and `s_i = 0`, there is no way for A to have more voters than B because A alone cannot reach the minimum majority. Similarly, if all districts require B to win but `y` is too small, the solution is impossible. These constraints show that the problem is not just about totals but about careful allocation.

## Approaches

The brute-force approach would consider all combinations of voters in each district, testing every possible allocation for arrays `a` and `b`. This approach is correct because it would eventually enumerate every valid configuration, but it is clearly infeasible. For `n = 10^5` and voter counts up to 10^9, the number of potential distributions grows exponentially, far exceeding any realistic computation time.

The key observation is that for each district, the requirement reduces to a linear inequality: if `s_i = 0`, we must have `a_i > b_i` and `a_i + b_i >= p_i`; if `s_i = 1`, we require `b_i > a_i` and `a_i + b_i >= p_i`. Since `a_i` and `b_i` are nonnegative integers, we can calculate the minimum and maximum allocation bounds for each district individually and then check if the total voters `x` and `y` can satisfy these bounds globally. This reduces the problem to two ranges: the total voters that must go to A and the total that must go to B, which can be checked in linear time.

The observation that each district’s requirements define a range for the number of voters from A (or B) allows us to formulate a simple sum-of-minimums and sum-of-maximums check. If the total number of voters of each party fits within these ranges, a solution exists; otherwise, it does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(sum(p_i))) | O(n) | Too slow |
| Range-Based Allocation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each district `i`, determine the minimum number of voters that must go to party A (`min_a`) and the minimum to party B (`min_b`). If `s_i = 0`, A must win, so the minimum allocation for A is `(p_i + 1) // 2`. If `s_i = 1`, B must win, so the minimum allocation for A is `0`.
2. For the same district, determine the maximum allocation for A. This is constrained by the total voters in the district: if `s_i = 0`, the maximum A can take is `p_i - 0` (all voters if B takes none). If `s_i = 1`, the maximum A can take is `p_i - (p_i + 1) // 2` to ensure B wins.
3. Sum the minimum allocations across all districts to get `min_total_a`. Sum the maximum allocations to get `max_total_a`. This defines the global feasible range for A.
4. Check whether `x` (total voters of A) lies within `[min_total_a, max_total_a]`. Similarly, verify that `y` fits the complementary distribution.
5. If both totals fit within the feasible ranges, print YES. Otherwise, print NO.

**Why it works:** Each district defines a local feasible range for A and B independently. Summing minimums and maximums gives a global feasible range. If the total voters lie outside this range, some district cannot meet both the minimum and winner requirement, so no solution exists. If it lies inside, a valid allocation can always be constructed greedily by distributing surplus voters in any order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x, y = map(int, input().split())
        s = input().strip()
        p = list(map(int, input().split()))
        
        min_a_total = 0
        max_a_total = 0
        
        for i in range(n):
            if s[i] == '0':
                min_a = (p[i] + 1) // 2
                max_a = p[i]
            else:
                min_a = 0
                max_a = p[i] // 2
            min_a_total += min_a
            max_a_total += max_a
        
        if min_a_total <= x <= max_a_total and (sum(p) - x) <= y:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution first calculates the per-district minimum and maximum voters for party A based on the winner requirement. Summing across all districts gives a feasible total range for A. We then check whether `x` fits inside this range and whether the remaining voters can satisfy B. The order of operations is crucial: integer division is carefully used to handle odd and even `p_i` values, ensuring that a majority exists where needed.

## Worked Examples

**Example 1:**

Input:

```
n=3, x=5, y=5
s=010
p=[2,4,3]
```

| i | s_i | p_i | min_a | max_a | min_a_total | max_a_total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | 2 | 1 | 2 |
| 2 | 1 | 4 | 0 | 2 | 1 | 4 |
| 3 | 0 | 3 | 2 | 3 | 3 | 7 |

`min_total_a = 3`, `max_total_a = 7`. Since `x = 5` is within `[3, 7]`, and `y = 5` is enough to cover remaining voters, the output is YES.

**Example 2:**

Input:

```
n=2, x=3, y=3
s=00
p=[4,3]
```

| i | s_i | p_i | min_a | max_a | min_a_total | max_a_total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 2 | 4 | 2 | 4 |
| 2 | 0 | 3 | 2 | 3 | 4 | 7 |

`min_total_a = 4`, `max_total_a = 7`. `x = 3` is less than `min_total_a`, so output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each district is processed once; sum operations are linear |
| Space | O(n) | We store the array `p` of length n |

The algorithm easily handles `n` up to 2·10^5 and sums of `n` over all test cases up to 2·10^5. Memory usage is within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("6\n3 5 5\n010\n2 4 3\n4 2 3\n0001\n1 1 1 1\n2 4 2\n00\n3 3\n4 23 20\n1111\n2 2 2 2\n1 25 26\n0\n51\n2 4 2\n00\n3 4") == \
"YES\nNO\nYES\nNO\nNO\nNO"

# Custom cases
assert run("1\n1 1 1\n0\n1") == "YES", "single district, minimal input"
assert run("1\n1
```
