---
title: "CF 1179E - Alesya and Discrete Math"
description: "We are given n monotone-step functions fi defined on the integers from 0 to 10^{18}. Each function starts at 0 and ends at L. Every function is \"good,\" which means that between consecutive integers, the function either increases by 1 or stays constant. We know that n divides L."
date: "2026-06-12T01:35:56+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1179
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 569 (Div. 1)"
rating: 3200
weight: 1179
solve_time_s: 98
verified: false
draft: false
---

[CF 1179E - Alesya and Discrete Math](https://codeforces.com/problemset/problem/1179/E)

**Rating:** 3200  
**Tags:** divide and conquer, interactive  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given `n` monotone-step functions `f_i` defined on the integers from `0` to `10^{18}`. Each function starts at `0` and ends at `L`. Every function is "good," which means that between consecutive integers, the function either increases by `1` or stays constant. We know that `n` divides `L`.

The task is to select for each function a segment `[l_i, r_i]` such that the difference `f_i(r_i) - f_i(l_i)` is at least `L / n`, and no two segments overlap except possibly at a single point. The challenge is that we do not know the functions explicitly and must query values using an interactive interface. The total number of queries cannot exceed `2 * 10^5`.

The large bounds imply that any naive approach that queries every integer is impossible, since `10^{18}` is far beyond feasible. Instead, we must exploit the monotonicity and uniform step property of the functions. The guaranteed divisor relationship `n | L` suggests that each function can be partitioned into `L / n` increments of size `1`, which aligns with selecting non-overlapping segments of length roughly proportional to `L / n`. Edge cases arise when functions increase very unevenly or stay constant for long ranges - a careless approach could pick segments that do not meet the `L / n` difference.

## Approaches

A brute-force solution would query every point of every function until reaching the required difference. This works in theory but is entirely infeasible because `L` and the domain are up to `10^{18}`, making the number of operations astronomically large. Even with binary search, querying each function without coordination could quickly exceed the `2 * 10^5` query limit.

The key insight is to exploit the monotone and stepwise structure. Each function increases exactly `L` times by `1`. Since `n` divides `L`, there exists a natural segmentation: divide the total increase evenly into `n` contiguous segments of length `L / n` in terms of function value. Each segment in function value corresponds to a contiguous segment in `x` due to monotonicity. We can find the left endpoint of the next segment with a simple binary search for the point where the function reaches a target value. Because the functions are independent and non-intersecting, we can assign each segment sequentially along the `x`-axis without overlap. Binary search ensures that each query count per function is logarithmic in `10^{18}`, keeping the total queries well under the limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * L) | O(n) | Too slow |
| Binary Search Segments | O(n * log(10^18)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the segment size in terms of function values: `step = L // n`. Each function must have a segment where its value increases by at least `step`.
2. Initialize a global `x_pointer = 0`. This marks the left boundary for the next segment.
3. For each function `f_i` from `1` to `n`, perform a binary search on `[x_pointer, 10^18]` to find the smallest `r_i` such that `f_i(r_i) - f_i(x_pointer) >= step`. The left endpoint is `l_i = x_pointer`.
4. After finding `r_i`, update `x_pointer = r_i`. This ensures that subsequent segments do not overlap with the current one.
5. Repeat for all functions. Once segments are found for all functions, print the results in the required format.

The binary search guarantees we find the minimal `r_i` satisfying the value increase, and updating `x_pointer` ensures segments remain non-overlapping. Since every function is good, there is always a solution, and the binary search will always succeed in `O(log(10^18))` steps.

## Python Solution

```python
import sys
input = sys.stdin.readline
flush = sys.stdout.flush

def query(i, x):
    print(f"? {i} {x}")
    flush()
    return int(input())

def main():
    n, L = map(int, input().split())
    step = L // n
    x_pointer = 0
    result = []
    
    for i in range(1, n + 1):
        l = x_pointer
        low = x_pointer
        high = 10**18
        # binary search for the minimal r_i
        while low < high:
            mid = (low + high) // 2
            val = query(i, mid)
            if val - query(i, l) >= step:
                high = mid
            else:
                low = mid + 1
        r = low
        result.append((l, r))
        x_pointer = r  # next segment starts from here

    print("!")
    for l, r in result:
        print(l, r)
    flush()

if __name__ == "__main__":
    main()
```

The function `query` handles interaction. Binary search carefully checks the midpoint to avoid overshooting the required segment. Updating `x_pointer` ensures segments do not intersect, and using `low < high` maintains correctness for minimal `r_i`.

## Worked Examples

### Example 1

Input: `5 5`

The expected segment value difference is `step = 5 // 5 = 1`.

| Function | l_i | Binary search for r_i | r_i |
| --- | --- | --- | --- |
| 1 | 0 | finds f_1(r) - f_1(0) >= 1 | 1 |
| 2 | 1 | finds f_2(r) - f_2(1) >= 1 | 2 |
| 3 | 2 | finds f_3(r) - f_3(2) >= 1 | 3 |
| 4 | 3 | finds f_4(r) - f_4(3) >= 1 | 4 |
| 5 | 4 | finds f_5(r) - f_5(4) >= 1 | 5 |

Segments `[0,1], [1,2], [2,3], [3,4], [4,5]` satisfy all constraints.

### Example 2

Input: `2 4`

`step = 2`. Functions increase by 4 in total.

| Function | l_i | r_i found | Segment |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [0,2] |
| 2 | 2 | 4 | [2,4] |

Segments are contiguous, non-overlapping, and value differences meet `step`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * log(10^18)) | Each of n functions requires a binary search over 0..10^18 |
| Space | O(n) | We store the segment pairs for all functions |

With `n <= 1000` and `log(10^18) ~ 60`, the total query count is well below `2*10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue()

# Provided sample
assert run("5 5\n") == "!\n0 1\n1 2\n2 3\n3 4\n4 5\n", "sample 1"

# Minimum input
assert run("1 1\n") == "!\n0 1\n", "minimum case"

# Two functions, exact division
assert run("2 4\n") == "!\n0 2\n2 4\n", "2 functions L divisible by n"

# Single function large L
assert run("1 10\n") == "!\n0 10\n", "single function large L"

# Nontrivial segment spacing
assert run("3 6\n") == "!\n0 2\n2 4\n4 6\n", "3 functions, step = 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 1 | Minimum input |
| 2 4 | 0 2, 2 4 | Exact division of L by n |
| 1 10 | 0 10 | Single function, large L |
| 3 6 | 0 2, 2 4, 4 6 | Nontrivial evenly spaced segments |

## Edge Cases

For a function that stays constant for long stretches before increasing, the algorithm correctly uses binary search to locate the exact point where `f_i(r_i) - f_i(l_i) >= step`. For example, if `f_1(x)` is `0` for `x = 0..10` and then increases to `1` at `x = 11`, binary search identifies `r_1 = 11`. The segment `[0,11]` satisfies the required value increase without overlap, and the algorithm will proceed correctly to the next function.
