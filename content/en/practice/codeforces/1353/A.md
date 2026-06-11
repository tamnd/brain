---
title: "CF 1353A - Most Unstable Array"
description: "We are given an array length n and a required total sum m. The task is to assign non-negative integers to an array of length n so that the sum of all elements equals m."
date: "2026-06-11T14:01:03+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1353
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 642 (Div. 3)"
rating: 800
weight: 1353
solve_time_s: 106
verified: true
draft: false
---

[CF 1353A - Most Unstable Array](https://codeforces.com/problemset/problem/1353/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array length `n` and a required total sum `m`. The task is to assign non-negative integers to an array of length `n` so that the sum of all elements equals `m`. Among all such arrays, we want the one that makes the total “adjacent jump” as large as possible, where each jump is the absolute difference between neighboring elements.

The expression being maximized measures how much the array oscillates when read left to right. A flat array produces zero, while alternating between large and small values creates large contributions from every transition.

The constraints are extremely large: both `n` and `m` can be up to `10^9`, and there can be up to `10^4` test cases. This immediately rules out constructing arrays explicitly or simulating anything proportional to `n`. Any solution must reduce each test case to constant time arithmetic.

A naive attempt would try to distribute `m` across the array in different patterns and compute the resulting sum of differences. Even if we only tried to simulate one candidate array per test case, building or iterating over `n` elements is impossible.

A subtle edge case appears when `n = 1`. There are no adjacent pairs, so the answer is always zero regardless of `m`. Another corner is when `n = 2`, where the answer becomes simply `|a1 - a2|` under the constraint `a1 + a2 = m`, which is maximized by pushing all mass into one side.

## Approaches

The brute-force viewpoint is to try all possible arrays of length `n` with sum `m`, compute their adjacent differences, and track the maximum. Even if we restrict ourselves to integer compositions of `m`, the number of possibilities grows exponentially with `m` and combinatorially with `n`. This is completely infeasible even for small inputs.

The key structural observation is that every unit of value placed in the array can only contribute to differences when it is moved between positions that are not symmetric. To maximize adjacent differences, we want the array to alternate between high and low values as much as possible. However, we are constrained by total mass `m`, so we cannot freely assign large alternating values everywhere.

The optimal construction turns out to be extremely simple: we place all non-zero mass in two extreme patterns depending on `n`. When `n = 1`, there is no adjacent pair. When `n = 2`, we place `m` entirely on one side. When `n ≥ 3`, we can achieve a full “zig-zag” pattern where values alternate between zero and non-zero, and every unit of mass contributes twice to the total difference except for boundary limitations. This leads to the closed form result that the maximum value is `2 * m` when `n ≥ 3`, and `m` when `n = 2`.

The reason this works is that each unit placed in an interior position can be counted twice in transitions, once when entering and once when leaving, and the alternating structure ensures no wasted mass in flat segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each test case to a direct formula based only on `n` and `m`.

1. If `n == 1`, return `0`. There are no adjacent elements, so no differences exist.
2. If `n == 2`, return `m`. The best we can do is split `m` into `(m, 0)` or `(0, m)`, giving difference `m`.
3. If `n >= 3`, return `2 * m`. We can construct an alternating pattern such as `[0, m, 0, 0, 0, ...]` rearranged into a zig-zag where all movement of mass contributes twice across transitions.

The key reason step 3 works is that with at least three positions, we can always separate the mass so that it is surrounded by zeros, allowing it to be “entered” and “exited” in adjacent transitions.

### Why it works

The value of the objective depends only on changes between consecutive positions. Each positive unit placed in the array can contribute at most twice to the sum of absolute differences, once when it is approached from a zero (or lower value) and once when it leaves back to zero (or lower value). With at least three slots, we can always arrange zeros around all mass in a way that avoids interference between contributions, making `2m` achievable and maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        if n == 1:
            print(0)
        elif n == 2:
            print(m)
        else:
            print(2 * m)

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and applies a direct case distinction. The implementation relies on the fact that the answer depends only on `n` and `m`, so no array construction is required.

The only subtlety is ensuring that multiplication by 2 is done in Python integers, which safely handle values up to `2 * 10^9` within the constraints.

## Worked Examples

We trace the logic for selected inputs.

### Example 1

Input:

`n = 2, m = 2`

| Step | n | m | Decision | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | n == 2 | 2 |

Here the array `[2, 0]` achieves value `|2 - 0| = 2`, which matches the output.

This confirms that with two elements, all mass must be placed at one endpoint.

### Example 2

Input:

`n = 5, m = 5`

| Step | n | m | Decision | Output |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | n ≥ 3 | 10 |

A construction like `[0, 5, 0, 0, 0]` rearranged into a zig-zag interpretation yields maximum alternation. Each unit contributes twice across transitions, producing `2 * 5 = 10`.

This shows how increasing available positions allows full exploitation of oscillation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with constant arithmetic |
| Space | O(1) | No auxiliary storage proportional to input size |

The constraints allow up to `10^4` test cases, so a constant-time solution per test case is necessary. This solution meets that requirement easily.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        if n == 1:
            output.append("0")
        elif n == 2:
            output.append(str(m))
        else:
            output.append(str(2 * m))
    return "\n".join(output)

# provided samples
assert run("""5
1 100
2 2
5 5
2 1000000000
1000000000 1000000000
""") == """0
2
10
1000000000
2000000000"""

# minimum size
assert run("1\n1 0\n") == "0"

# small alternating case
assert run("1\n3 1\n") == "2"

# large single element
assert run("1\n1 1000000000\n") == "0"

# large two element
assert run("1\n2 1000000000\n") == "1000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `0` | single element edge case |
| `3 1` | `2` | minimum oscillation case |
| `1 1000000000` | `0` | large n=1 stability |
| `2 1000000000` | `1000000000` | boundary for n=2 |

## Edge Cases

For `n = 1`, the algorithm returns `0` immediately. With input `n = 1, m = 100`, there are no adjacent pairs, so the computed value is structurally zero regardless of distribution. The condition `n == 1` directly enforces this.

For `n = 2`, the algorithm returns `m`. If we take `n = 2, m = 7`, the only way to split the sum is `(7, 0)` or `(3, 4)` or any partition. The best case is always placing all mass on one side, producing difference `7`. The branch `n == 2` captures this exact behavior.

For `n ≥ 3`, consider `n = 3, m = 4`. The algorithm returns `8`. A valid construction is `[0, 4, 0]`, producing `|0-4| + |4-0| = 8`. This shows that the doubling effect is achievable even in the smallest case where it applies.
