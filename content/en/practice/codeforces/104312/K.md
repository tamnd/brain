---
title: "CF 104312K - Monster-Slayer"
description: "We are given a line of monsters, each with a power value, positive or negative. Saitama can choose any consecutive segment of these monsters and defeat exactly that group."
date: "2026-07-01T19:55:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "K"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 69
verified: true
draft: false
---

[CF 104312K - Monster-Slayer](https://codeforces.com/problemset/problem/104312/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of monsters, each with a power value, positive or negative. Saitama can choose any consecutive segment of these monsters and defeat exactly that group. The strength of a chosen segment is the sum of all values inside it, and the task is to find the maximum possible segment sum over all contiguous segments.

The input is a single array of length up to 100,000, and each value can be as small as negative one billion or as large as one billion. The output is a single integer, the best possible sum from any contiguous subarray.

The constraint on n immediately rules out any solution that tries all subarrays explicitly. A double loop over all (i, j) pairs already leads to roughly 10^10 operations in the worst case, which is far beyond what can pass in one second. This pushes us toward a linear or near-linear solution.

A subtle edge case appears when all numbers are negative. For example, for input `[-5, -2, -8]`, the correct answer is `-2`, coming from choosing a single element. A naive implementation that initializes the answer as zero or assumes we can “skip everything” would incorrectly return zero, even though zero is not a valid subarray sum unless explicitly allowed by an empty subarray, which this problem does not permit.

Another edge case is a single-element array, where the answer must be that element itself, even if negative. This stresses correct initialization.

## Approaches

The brute-force approach is straightforward: consider every possible subarray, compute its sum, and track the maximum. For each starting index i, we extend to every j ≥ i and accumulate sums incrementally. This is correct because it directly evaluates every valid contiguous segment. However, the number of segments is n(n+1)/2, and each sum update is O(1) if we reuse prefix accumulation, still giving O(n^2) total work. With n up to 10^5, this becomes infeasible.

The key observation is that when scanning from left to right, at each position we only care about whether extending the previous segment is beneficial or whether starting fresh at the current position is better. If the running sum becomes negative, keeping it only reduces the contribution of any future extension, so it is optimal to restart from the current element. This turns the global optimization problem into a local decision at each index, which is exactly what allows a linear scan.

This reduces the problem to maintaining a running best prefix ending at each position and tracking the global maximum of these values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal (Kadane’s algorithm) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining two values: the best subarray sum ending at the current position, and the best overall answer seen so far.

1. Initialize the running sum to the first element of the array. This ensures we correctly handle the case where all numbers are negative, since we are forced to pick at least one element.
2. Initialize the global best answer to the same value, since the best subarray at the start can only be that single element.
3. Iterate through the array starting from the second element.
4. At each element p[i], decide whether to extend the previous subarray or start fresh at i. Extending means adding p[i] to the running sum, while restarting means discarding it and setting the running sum to p[i].
5. The decision is made by comparing p[i] with running_sum + p[i]. If the previous sum is negative, restarting is better; otherwise, extending is beneficial.
6. After updating the running sum, update the global answer if the running sum is larger.
7. After finishing the iteration, the global answer is the maximum subarray sum.

Why it works: at every index i, the algorithm maintains the best possible subarray that must end at i. Any subarray ending at i either comes from extending a valid subarray ending at i−1 or starts at i itself. If the previous contribution is negative, it can only reduce future sums, so discarding it cannot worsen any optimal future choice. This local optimality guarantees that the global maximum is encountered among all endpoints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    current = arr[0]
    best = arr[0]
    
    for i in range(1, n):
        current = max(arr[i], current + arr[i])
        best = max(best, current)
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution reads the array once and maintains two running variables. The key line is the transition `current = max(arr[i], current + arr[i])`, which encodes the decision of restarting or extending. The variable `best` tracks the best subarray sum seen so far, regardless of where it ends.

Care must be taken in initialization. Setting both `current` and `best` to the first element ensures correctness even when all numbers are negative, avoiding accidental initialization to zero.

## Worked Examples

### Example 1

Input:

```
9
-2 10 -3 5 -2 1 2 6 -1
```

| i | arr[i] | current before | choice | current after | best |
| --- | --- | --- | --- | --- | --- |
| 0 | -2 | - | start | -2 | -2 |
| 1 | 10 | -2 | extend | 8 vs 10 | 10 |
| 2 | -3 | 10 | extend | 7 vs -3 | 10 |
| 3 | 5 | 7 | extend | 12 vs 5 | 12 |
| 4 | -2 | 12 | extend | 10 vs -2 | 12 |
| 5 | 1 | 10 | extend | 11 vs 1 | 12 |
| 6 | 2 | 11 | extend | 13 vs 2 | 13 |
| 7 | 6 | 13 | extend | 19 vs 6 | 19 |
| 8 | -1 | 19 | extend | 18 vs -1 | 19 |

This trace shows how partial negative contributions are absorbed only when they still improve the running sum, and how the best answer is only updated when a new peak is reached.

### Example 2

Input:

```
5
-5 -2 -8 -1 -3
```

| i | arr[i] | current before | choice | current after | best |
| --- | --- | --- | --- | --- | --- |
| 0 | -5 | - | start | -5 | -5 |
| 1 | -2 | -5 | restart | -2 | -2 |
| 2 | -8 | -2 | restart | -8 | -2 |
| 3 | -1 | -8 | restart | -1 | -1 |
| 4 | -3 | -1 | extend? | -4 vs -3 | -1 |

This demonstrates the important behavior when all numbers are negative: the algorithm continuously restarts, effectively selecting the least negative single element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once with constant-time updates |
| Space | O(1) | Only two integer variables are maintained |

The linear scan fits comfortably within the constraints for n up to 100,000. Memory usage remains constant regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    data = sys.stdin.read().strip().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))

    current = arr[0]
    best = arr[0]

    for i in range(1, n):
        current = max(arr[i], current + arr[i])
        best = max(best, current)

    return str(best)

# provided sample
assert run("""9
-2 10 -3 5 -2 1 2 6 -1""") == "19"

# single element
assert run("""1
-7""") == "-7"

# all negative
assert run("""5
-5 -2 -8 -1 -3""") == "-1"

# all positive
assert run("""4
1 2 3 4""") == "10"

# mixed with large peak
assert run("""6
-1 -2 100 -3 -4 50""") == "100"

# alternating
assert run("""6
1 -1 1 -1 1 -1""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 -7 | -7 | single element handling |
| -5 -2 -8 -1 -3 | -1 | all-negative selection |
| 1 2 3 4 | 10 | monotonic increasing case |
| -1 -2 100 -3 -4 50 | 100 | isolated peak dominance |
| 1 -1 1 -1 1 -1 | 1 | alternating restart behavior |

## Edge Cases

For a single-element input like `[-7]`, the algorithm initializes `current` and `best` to `-7`, so it directly outputs `-7` without entering the loop. This avoids any incorrect assumption that an empty subarray could be chosen.

For an all-negative array like `[-5, -2, -8, -1]`, the algorithm repeatedly restarts at each position because extending always worsens the sum. The running best updates to `-2` at index 1 and never drops afterward, producing the correct least-negative element as the answer.
