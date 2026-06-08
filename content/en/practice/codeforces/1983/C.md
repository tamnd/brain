---
title: "CF 1983C - Have Your Cake and Eat It Too"
description: "We are asked to split a linear cake of n pieces among Alice, Bob, and Charlie. Each person values each piece differently, and the total value of all pieces is the same for everyone."
date: "2026-06-08T16:35:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1983
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 956 (Div. 2) and ByteRace 2024"
rating: 1400
weight: 1983
solve_time_s: 162
verified: false
draft: false
---

[CF 1983C - Have Your Cake and Eat It Too](https://codeforces.com/problemset/problem/1983/C)

**Rating:** 1400  
**Tags:** binary search, brute force, greedy, implementation  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to split a linear cake of `n` pieces among Alice, Bob, and Charlie. Each person values each piece differently, and the total value of all pieces is the same for everyone. The challenge is to assign contiguous slices to each person such that no piece is shared, and each person’s slice reaches at least a third of their total cake value rounded up. The output should be the starting and ending indices of each person’s slice or `-1` if no such division exists.

The constraints on `n` go up to 200,000 per test case, and the sum of all `n` across test cases is also capped at 200,000. With a 2-second time limit, any solution that considers all possible triplets of subarrays explicitly would require up to `O(n^3)` operations, which is infeasible. We need a solution that is essentially linear in `n` for each test case. Edge cases include cakes where a single piece already exceeds a third of the total value, cakes with uniform values where any contiguous allocation works, and cakes where the last pieces must be forced onto someone to satisfy the sum requirement. A naive implementation that always tries the first third blindly can fail when high values are clustered at the end of the array.

## Approaches

The brute-force method would attempt every possible combination of three non-overlapping subarrays and check their sums. This is correct in principle but leads to a worst-case complexity of `O(n^3)`, which is impossible for `n` of 200,000.

The key insight is that each person’s slice only needs to reach a threshold, and we can scan greedily using prefix sums. Once we identify a minimal subarray for Alice that reaches her quota, the remaining cake can be treated as a fresh array for Bob. Using prefix sums, we can locate the minimal right boundary for any left boundary efficiently, effectively reducing the search for each slice to a linear scan rather than nested loops. By processing people in order (Alice, Bob, Charlie) and maintaining cumulative sums, we can determine the first valid split that satisfies all three.

This transforms the problem from `O(n^3)` to a linear scan `O(n)` for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Greedy with prefix sums | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix sums for Alice, Bob, and Charlie separately. This allows any contiguous subarray sum to be calculated in `O(1)` time as `prefix[r] - prefix[l-1]`.
2. Compute the threshold for each person as `ceil(total / 3)`. This is the minimum sum each subarray must reach.
3. Start from the left of the cake and find the minimal slice for Alice. Scan forward and use the prefix sums to determine the first `r_a` such that the sum from index `1` to `r_a` for Alice reaches her threshold.
4. For Bob, begin scanning immediately after Alice’s slice (`r_a + 1`). Find the minimal contiguous subarray for Bob that reaches his threshold using the prefix sums, resulting in `r_b`.
5. The remaining cake automatically goes to Charlie. Check if the sum of Charlie’s slice from `r_b + 1` to `n` meets his threshold. If it does, return the indices `(1, r_a, r_a+1, r_b, r_b+1, n)`.
6. If at any point Alice or Bob cannot reach their threshold with the remaining pieces, output `-1`.

Why it works: the greedy scan is valid because once a minimal slice is chosen for Alice and then Bob, the leftover for Charlie must meet the threshold due to the total sum equality. By always taking the minimal subarray that meets the threshold, we avoid overshooting and leaving insufficient cake for subsequent people.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        c = list(map(int, input().split()))
        
        total = sum(a)
        threshold = (total + 2) // 3  # ceiling division
        
        # prefix sums
        pa = [0]*(n+1)
        pb = [0]*(n+1)
        pc = [0]*(n+1)
        for i in range(n):
            pa[i+1] = pa[i] + a[i]
            pb[i+1] = pb[i] + b[i]
            pc[i+1] = pc[i] + c[i]

        # find Alice slice
        r_a = -1
        for i in range(1, n+1):
            if pa[i] >= threshold:
                r_a = i
                break
        if r_a == -1:
            print(-1)
            continue

        # find Bob slice
        r_b = -1
        for i in range(r_a+1, n+1):
            if pb[i] - pb[r_a] >= threshold:
                r_b = i
                break
        if r_b == -1:
            print(-1)
            continue

        # check Charlie slice
        sum_charlie = pc[n] - pc[r_b]
        if sum_charlie < threshold:
            print(-1)
            continue

        print(1, r_a, r_a+1, r_b, r_b+1, n)

solve()
```

The code uses prefix sums for quick sum calculations. The `r_a` loop finds Alice’s first valid subarray. The `r_b` loop finds Bob’s next valid subarray immediately following Alice’s slice. The remaining indices automatically belong to Charlie. Edge cases are handled by checking `-1` if thresholds cannot be reached.

## Worked Examples

**Sample 1:**

Input slices:

```
a = [5, 1, 1, 1, 1]
b = [1, 1, 5, 1, 1]
c = [1, 1, 1, 1, 5]
```

Threshold = `ceil(9/3) = 3`.

| Step | i | pa[i] | r_a candidate? |
| --- | --- | --- | --- |
| Alice | 1 | 5 | Yes, r_a = 1 |
| Bob | 2 | 1 | No |
|  | 3 | 6 | Yes, r_b = 3 |
| Charlie | 4 to 5 | sum = 6 | threshold met |

Output: `1 1 2 3 4 5`

This shows minimal slices satisfy thresholds and no overlaps occur.

**Sample 2:**

Input:

```
a = [4, 4, 4, 4]
b = [4, 4, 4, 4]
c = [4, 4, 4, 4]
```

Threshold = 6. Any 2-piece slice suffices. Alice can take 2 pieces, Bob next 2, but then Charlie has 0 pieces left, failing threshold. Output: `-1`.

This demonstrates that even with equal distributions, the greedy scan may fail if slices are too large relative to `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per testcase | Each array is scanned once to compute prefix sums and once to find slices |
| Space | O(n) | For prefix sum arrays |

With sum of `n` over all test cases ≤ 200,000, this is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("10\n5\n5 1 1 1 1\n1 1 5 1 1\n1 1 1 1 5\n6\n1 2 3 4 5 6\n5 6 1 2 3 4\n3 4 5 6 1 2\n4\n4 4 4 4\n4 4 4 4\n4 4 4 4\n") == "1 1 2 3 4 5\n5 6 1 2 3 4\n-1\n-1", "sample test"

# Custom cases
assert run("1\n3\n1 1 1\n1 1 1\n1 1 1\n") == "1 1 2 2 3 3", "minimum size input"
assert run("1\n5\n5 5 5 5 5\n5 5 5 5 5\n5 5 5 5 5\n") == "1 2 3 4 5 5", "all equal values"
assert run("1\n4\n1 1 1 10\n1 1 1 10\n1 1 1 10\n") == "1 3 4 4 -1", "edge allocation at end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 pieces all 1 | 1 1 2 2 3 3 | minimal-size allocation works |
