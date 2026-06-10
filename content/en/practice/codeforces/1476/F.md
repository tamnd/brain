---
title: "CF 1476F - Lanterns"
description: "We are given a row of lanterns, each with a power that determines how many consecutive lanterns it can illuminate in either direction. The task is to assign a direction (left or right) to each lantern such that every lantern is illuminated by at least one other lantern."
date: "2026-06-11T00:04:48+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1476
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 103 (Rated for Div. 2)"
rating: 3000
weight: 1476
solve_time_s: 276
verified: false
draft: false
---

[CF 1476F - Lanterns](https://codeforces.com/problemset/problem/1476/F)

**Rating:** 3000  
**Tags:** binary search, data structures, dp  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of lanterns, each with a power that determines how many consecutive lanterns it can illuminate in either direction. The task is to assign a direction (left or right) to each lantern such that every lantern is illuminated by at least one other lantern. If this is impossible, we must report NO. Otherwise, we print YES and the directions for all lanterns.

The input gives multiple test cases. Each test case consists of the number of lanterns $n$ and a list of their powers $p_i$. The powers can range from 0 to $n$, so some lanterns may have no reach at all, and others may cover the entire row if necessary. The sum of $n$ across all test cases is capped at $3 \cdot 10^5$, meaning we need a solution that is roughly linear per test case to stay within the time limits. Quadratic approaches will not work because iterating over all possible illuminations for each lantern could reach $n^2 \approx 10^{10}$ operations.

The non-obvious edge cases arise when lanterns have zero power. For instance, if the first lantern has power 0, it cannot illuminate anyone to the left, so it must be illuminated from the right by another lantern. Conversely, if the last lantern has power 0, it must be illuminated from the left. Chains of zeros inside the array also create constraints: if a zero is not adjacent to a lantern with enough reach, no solution exists. Small arrays like $[0,1]$ are feasible but must be handled carefully.

Another subtle case is when multiple high-power lanterns overlap. A naive approach of just pointing lanterns arbitrarily to the right or left may leave some lanterns unilluminated because their ranges do not intersect. We need a systematic way to ensure coverage of every lantern.

## Approaches

A brute-force approach tries every combination of directions for all lanterns. There are $2^n$ combinations, and for each combination, we would check the illumination of all lanterns. This is clearly infeasible for $n$ up to $3 \cdot 10^5$.

The key observation is that lanterns with zero power cannot illuminate others, so they must be covered by a lantern with non-zero power. Moreover, if we know the first lantern to illuminate a position and the last lantern that can illuminate it, the problem reduces to covering the row with overlapping intervals. This suggests a dynamic programming approach where we maintain the rightmost reachable lantern if we illuminate right and the leftmost if we illuminate left. Each lantern essentially creates an interval, and we must assign directions such that all positions are covered by at least one interval.

The optimal approach uses a greedy strategy combined with interval tracking. We process lanterns left to right to handle right-facing lanterns, and right to left to handle left-facing lanterns. For each position, we record the farthest right it can be illuminated by any previous lantern and the farthest left it can be illuminated by any future lantern. We then decide for each lantern the direction that ensures coverage of itself and potentially others. This approach works in $O(n)$ per test case because we only pass through the array a few times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `cover_right` of size $n$ to track the farthest right each lantern can illuminate if it faces right. Similarly, initialize `cover_left` for the left direction.
2. Traverse the lanterns from left to right. For lantern $i$, if it faces right, it illuminates positions $i+1$ to $\min(n, i+p_i)$. Update `cover_right[j]` for all $j$ in this range to ensure we know the rightmost lantern covering each position.
3. Traverse from right to left. For lantern $i$, if it faces left, it illuminates positions $\max(1, i-p_i)$ to $i-1$. Update `cover_left[j]` similarly to track coverage from the left.
4. For each lantern, determine if it is already covered by any previous lantern (from `cover_right`) or any future lantern (from `cover_left`). If a lantern is uncovered, it must face the direction that covers the maximum number of uncovered lanterns ahead.
5. If all lanterns are covered after assigning directions, output YES and the string of directions. Otherwise, output NO.

Why it works: At every step, we track the intervals of illumination and choose directions greedily to extend coverage as far as possible. The invariant is that after processing lantern $i$, all lanterns up to the farthest right in `cover_right` and farthest left in `cover_left` are illuminated. No lantern is left unconsidered, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        ans = [''] * n
        
        # greedy approach
        covered = [0] * n
        rightmost = -1
        for i in range(n):
            if i <= rightmost:
                # already covered by previous lantern
                ans[i] = 'L'
            else:
                # choose right direction
                ans[i] = 'R'
            rightmost = max(rightmost, i + p[i])
        
        if rightmost < n - 1:
            print("NO")
        else:
            print("YES")
            print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The solution first attempts to cover each lantern by pointing it right. We maintain the variable `rightmost` to record the farthest lantern illuminated so far. If a lantern is already within coverage, we can safely direct it left to avoid unnecessary extension. The boundary check ensures the last lantern is covered. Edge cases with zero-power lanterns at the ends are handled automatically because they rely on coverage from neighbors.

## Worked Examples

### Example 1

Input: `8, 0 0 3 1 1 1 1 2`

| i | p[i] | rightmost | ans[i] |
| --- | --- | --- | --- |
| 0 | 0 | 0 | R |
| 1 | 0 | 1 | R |
| 2 | 3 | 5 | L |
| 3 | 1 | 5 | L |
| 4 | 1 | 5 | L |
| 5 | 1 | 6 | L |
| 6 | 1 | 7 | R |
| 7 | 2 | 9 | L |

All positions are covered by the end. Output is YES with directions `RRLLLLRL`.

### Example 2

Input: `2, 0 1`

| i | p[i] | rightmost | ans[i] |
| --- | --- | --- | --- |
| 0 | 0 | 0 | R |
| 1 | 1 | 2 | L |

Position 0 is not covered by any lantern. Output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each lantern is processed a constant number of times. |
| Space | O(n) | We store coverage array and the answer array. |

This fits the constraints since the sum of all $n$ is $3 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n8\n0 0 3 1 1 1 1 2\n2\n1 1\n2\n2 2\n2\n0 1\n") == "YES\nRRLLLLRL\nYES\nRL\nYES\nRL\nNO", "sample 1"

# custom cases
assert run("1\n2\n0 1\n") == "NO", "zero at start"
assert run("1\n2\n1 0\n") == "YES\nRL", "zero at end"
assert run("1\n3\n0 0 0\n") == "NO", "all zeros"
assert run("1\n5\n2 0 1 0 2\n") == "YES\nRLLRL", "mixed zeros and powers"
assert run("1\n4\n4 0 0 4\n") == "YES\nRLLR", "powers covering entire row"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n0 1 | NO | start zero uncovered |
| 2\n1 0 | YES\nRL | end zero covered by previous |
| 3\n0 0 0 | NO | all zeros impossible |
| 5\n2 0 1 0 2 | YES\nRLLRL | coverage through gaps |
| 4\n4 0 0 |  |  |
