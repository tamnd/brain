---
title: "CF 104677C - Darcy Parties"
description: "We are given a group of people, each holding some number of cake slices. If the cake had been divided perfectly, every person would have received exactly the same number of slices, because the total number of slices is guaranteed to be divisible by the number of people."
date: "2026-06-29T09:11:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104677
codeforces_index: "C"
codeforces_contest_name: "Sugar Sweet \u2764\ufe0f"
rating: 0
weight: 104677
solve_time_s: 62
verified: true
draft: false
---

[CF 104677C - Darcy Parties](https://codeforces.com/problemset/problem/104677/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of people, each holding some number of cake slices. If the cake had been divided perfectly, every person would have received exactly the same number of slices, because the total number of slices is guaranteed to be divisible by the number of people.

The task is to determine how many people do not match this ideal equal share. In other words, we compute the average number of slices per person and count how many individuals differ from that value.

The input is a small integer array, and the output is a single integer: the number of positions where the value is not equal to the average.

Since both the number of people and slice counts are at most 10, the input size is extremely small. This removes any need for advanced data structures or optimizations beyond a single pass through the array.

A subtle edge case arises when all values are already equal. In that case, the answer should be zero. Another corner case is when only one person exists, since the “average” is trivially their value, so again the answer is zero.

A naive mistake would be to recompute or simulate redistribution operations instead of directly comparing to the computed average. That would be unnecessary and could introduce rounding or integer division errors if not handled carefully.

## Approaches

The brute-force interpretation would be to try redistributing slices until everyone becomes equal, then count how many people changed during that process. One could simulate transfers between pairs until equilibrium is reached. However, even though the constraints are tiny here, that approach is fundamentally unnecessary and obscures the structure of the problem.

The key observation is that the final correct value for every person is fixed and uniquely determined: it is simply the total sum divided by N. There is no need to simulate any distribution process. Once this target value is known, the problem reduces to a direct comparison against each element of the array.

This transforms the problem from a process simulation into a simple aggregation and counting task. The brute-force idea works conceptually because redistribution eventually leads to uniformity, but it fails as a method because it introduces extra state changes that are irrelevant to the final question.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k·N²) or worse | O(N) | Too slow / unnecessary |
| Direct Comparison | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

### Steps

1. Read the number of people N and the list of slice counts.
2. Compute the total sum of all slices. This represents the full cake distributed across all participants.
3. Compute the target number of slices per person as total sum divided by N. This is guaranteed to be an integer due to the problem condition.
4. Initialize a counter to zero.
5. Iterate over each person's slice count.
6. For each person, compare their value with the target value.
7. If the values differ, increment the counter.
8. Output the final counter value.

Each comparison directly answers whether that person deviates from the fair distribution, so no intermediate transformation is required.

### Why it works

The sum constraint ensures that there exists a unique integer value that represents the fair share. Since fairness is defined purely by equality to this derived constant, every incorrect case is exactly one element not equal to that constant. The algorithm relies on the invariant that the target value is globally correct and independent of ordering or local relationships between elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    target = sum(a) // n
    ans = 0
    
    for x in a:
        if x != target:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is a direct translation of the algorithm. The most important detail is computing the target using integer division after summing all elements. Since the problem guarantees divisibility, there is no need for floating-point handling or rounding.

The loop simply counts mismatches. No sorting or extra storage is needed.

## Worked Examples

### Example 1

Input:

```
5
1 3 2 2 2
```

First compute the sum: 1 + 3 + 2 + 2 + 2 = 10.

Target per person is 10 / 5 = 2.

Now compare each value:

| Index | Value | Target | Match? | Counter |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | No | 1 |
| 2 | 3 | 2 | No | 2 |
| 3 | 2 | 2 | Yes | 2 |
| 4 | 2 | 2 | Yes | 2 |
| 5 | 2 | 2 | Yes | 2 |

Final answer is 2.

This confirms that the algorithm correctly identifies only the elements deviating from the global average.

### Example 2

Input:

```
4
4 4 4 4
```

Sum is 16, target is 4.

| Index | Value | Target | Match? | Counter |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | Yes | 0 |
| 2 | 4 | 4 | Yes | 0 |
| 3 | 4 | 4 | Yes | 0 |
| 4 | 4 | 4 | Yes | 0 |

Final answer is 0.

This shows the algorithm correctly handles the fully balanced configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass to compute sum and one pass to count mismatches |
| Space | O(1) | Only a few integer variables are used |

Given N ≤ 10, this is far below any practical limit. Even for much larger constraints, the solution scales linearly and remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))
    target = sum(a) // n
    ans = sum(1 for x in a if x != target)
    return str(ans)

# provided sample
assert run("5\n1 3 2 2 2\n") == "2"

# all equal
assert run("3\n2 2 2\n") == "0"

# single element
assert run("1\n7\n") == "0"

# two elements mismatch
assert run("2\n1 3\n") == "2"

# mixed case
assert run("4\n0 2 2 2\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1 3 2 2 2 | 2 | basic mixed distribution |
| 3 2 2 2 | 0 | already balanced |
| 1 7 | 0 | single-element edge case |
| 2 1 3 | 2 | both wrong relative to mean |
| 4 0 2 2 2 | 1 | sparse deviation case |

## Edge Cases

For a single person input like `1\n5`, the algorithm computes sum 5, target 5, and finds no mismatches, producing 0. This confirms that the definition of fairness degenerates correctly when N = 1.

For an already uniform array like `3\n2 2 2`, the computed target is 2, and every comparison succeeds, so the counter remains zero throughout. This verifies that the algorithm does not incorrectly flag equal configurations due to redundant checks or integer division issues.
