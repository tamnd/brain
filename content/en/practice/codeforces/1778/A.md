---
title: "CF 1778A - Flip Flop Sum"
description: "We are given an array consisting only of 1s and -1s. The task is to perform exactly one operation: select two consecutive elements and flip their signs. After doing this, we want to maximize the sum of all array elements."
date: "2026-06-09T11:36:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1778
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 848 (Div. 2)"
rating: 800
weight: 1778
solve_time_s: 201
verified: false
draft: false
---

[CF 1778A - Flip Flop Sum](https://codeforces.com/problemset/problem/1778/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 3m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array consisting only of `1`s and `-1`s. The task is to perform exactly one operation: select two consecutive elements and flip their signs. After doing this, we want to maximize the sum of all array elements. The input gives multiple test cases, each with its array, and the output should be the maximum achievable sum for each case.

The constraints indicate that the array can be quite long, up to 100,000 elements per test case, and the total across all test cases is also limited to 100,000. This tells us that any algorithm with complexity worse than linear in `n` per test case will be too slow.

Edge cases arise when the array has all `1`s or all `-1`s. For instance, if the array is `[1,1,1,1]`, flipping any two elements will decrease the sum, so the optimal move is to minimize the damage. Conversely, if the array is `[-1,-1]`, flipping them increases the sum from `-2` to `2`. Another subtle case occurs when the array contains a mix but has a consecutive pair of `-1`s or `1`s at the ends; choosing the right pair can produce the largest improvement or prevent a decrease.

## Approaches

A brute-force approach would iterate over every index `i` from `1` to `n-1`, flip `a[i]` and `a[i+1]`, calculate the sum, and keep track of the maximum. This is correct because it tests all possibilities, but it requires O(n) operations per test case, which is acceptable in this problem but unnecessary. The naive approach works here due to small total input size but can be simplified with a greedy observation.

The key insight is that flipping a pair of consecutive numbers changes the sum as follows. If the pair is `[x, y]`, flipping both gives `-x - y`. The change in sum is `(-x - y) - (x + y) = -2*(x + y)`. To maximize the sum, we want `x + y` to be as small as possible because `-2*(x + y)` will then be the largest increase. The smallest possible sum of two elements is `-2`, which occurs when both are `-1`. Conversely, the largest sum is `2` (both `1`s), which decreases the sum if flipped. Therefore, the optimal strategy is to check if there exists a pair of `-1, -1`; if so, flipping that pair increases the sum by 4. If no such pair exists, flipping a pair of `1,1` or `1,-1` decreases the sum by 4 or 0.

Given the small number of possibilities for pairs (`-1,-1`, `1,1`, `1,-1`, `-1,1`), we can greedily check the array for these patterns and apply the corresponding change.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Flip Every Pair | O(n) per test case | O(1) | Accepted but can be simplified |
| Greedy Based on Pair Sum | O(n) per test case | O(1) | Accepted and simpler |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the length of the array `n` and the array `a`.
3. Compute the initial sum of the array. This is the baseline before any flips.
4. Iterate through the array from the first element to the second-to-last element. For each index `i`, compute the sum of `a[i] + a[i+1]`.
5. If this sum is `-2` (both `-1`s), then flipping this pair increases the total sum by 4. Record that this is the best possible increase and break the loop because no other pair can give a larger increase.
6. If there are no `-1,-1` pairs, check for `1,1` pairs; flipping them decreases the sum by 4. If there are only `1,-1` or `-1,1` pairs, flipping them changes the sum by 0.
7. Add the best achievable increase or decrease to the initial sum and output the result.

Why it works: The operation affects only two consecutive elements. The sum change depends only on these two elements. By examining the four possible pairs and selecting the one that maximizes the increase (or minimizes decrease), we guarantee the optimal sum. Since the array contains only `1` and `-1`, these are the only four configurations, so the greedy choice is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = sum(a)
        best_change = -float('inf')
        for i in range(n-1):
            pair_sum = a[i] + a[i+1]
            change = -2 * pair_sum
            if change > best_change:
                best_change = change
            if best_change == 4:  # maximum possible, can't do better
                break
        print(total + best_change)

if __name__ == "__main__":
    solve()
```

The solution computes the sum once, iterates through consecutive pairs, calculates the potential change if flipped, and keeps the largest possible improvement. It short-circuits once a pair of `-1,-1` is found because this gives the maximal increase.

## Worked Examples

For input:

```
5
-1 1 1 -1 -1
```

| Index i | a[i] | a[i+1] | pair_sum | change | best_change |
| --- | --- | --- | --- | --- | --- |
| 0 | -1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 2 | -4 | 0 |
| 2 | 1 | -1 | 0 | 0 | 0 |
| 3 | -1 | -1 | -2 | 4 | 4 |

Initial sum = -1 + 1 + 1 -1 -1 = -1. Max sum = -1 + 4 = 3.

For input:

```
1 1
```

Only pair sum = 2, change = -4. Initial sum = 2. Max sum = 2 - 4 = -2.

This confirms the algorithm selects the optimal pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Iterate through n-1 consecutive pairs |
| Space | O(n) | Store array a |

With the total sum of n over all test cases ≤ 10^5, this solution runs well under time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n5\n-1 1 1 -1 -1\n5\n1 1 -1 -1 -1\n2\n1 1\n4\n1 -1 -1 1\n") == "3\n3\n-2\n4"

# custom cases
assert run("1\n2\n-1 -1\n") == "2", "flip -1 -1 to increase sum"
assert run("1\n3\n1 1 1\n") == "-1", "flip 1 1 to decrease sum minimally"
assert run("1\n4\n1 -1 1 -1\n") == "0", "flip any 1 -1 pair keeps sum same"
assert run("1\n5\n-1 -1 -1 -1 -1\n") == "1", "flip first -1 -1 gives maximum increase"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n-1 -1 | 2 | minimal array, flip increases sum |
| 3\n1 1 1 | -1 | consecutive 1s, must flip to minimize loss |
| 4\n1 -1 1 -1 | 0 | flipping mixed pairs, sum unchanged |
| 5\n-1 -1 -1 -1 -1 | 1 | multiple -1s, pick optimal pair for maximal sum |

## Edge Cases

For a two-element array `[1,1]`, the only operation is flipping these two elements. The initial sum is 2, flipping changes sum to -2. The algorithm computes `pair_sum = 2`, `change = -4`, and correctly updates the total sum to -2. For `[ -1, -1 ]`, flipping increases sum from -2 to 2. Arrays with alternating signs like `[1, -1, 1, -1]` always produce `change = 0`, so the total sum remains unchanged. The solution correctly handles all such edge cases because it examines each consecutive pair and chooses the one maximizing the net change.
