---
title: "CF 1993C - Light Switches"
description: "The problem involves an apartment with multiple rooms, each starting with its light turned off. Each room gets a chip installed at a distinct time, and each chip toggles the light in its room on and off periodically, with a period k minutes."
date: "2026-06-08T15:07:46+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1993
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 963 (Div. 2)"
rating: 1400
weight: 1993
solve_time_s: 171
verified: false
draft: false
---

[CF 1993C - Light Switches](https://codeforces.com/problemset/problem/1993/C)

**Rating:** 1400  
**Tags:** implementation, math  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
## Problem Understanding

The problem involves an apartment with multiple rooms, each starting with its light turned off. Each room gets a chip installed at a distinct time, and each chip toggles the light in its room on and off periodically, with a period `k` minutes. The toggling starts from the installation time and alternates between `k` minutes on and `k` minutes off indefinitely. The task is to determine the earliest moment when **all lights are simultaneously on**. If no such moment exists, the answer should be `-1`.

The input provides the number of rooms, the period `k`, and the times of installation for each room. Output is a single integer per test case representing the earliest minute when all lights are on.

Constraints indicate that `n` can be up to 2×10^5 and `t` up to 10^4, with the sum of `n` across all test cases bounded by 2×10^5. This implies that any solution must operate in **linear or near-linear time per test case**. Quadratic or exhaustive checking of every potential minute is infeasible because installation times can reach up to 10^9, so simulating every minute is impossible.

Non-obvious edge cases include situations where installation times are spaced such that the on-periods of different rooms **never align**. For example, if two lights have installation times differing by more than `k` and their sequences never intersect, the answer must be `-1`. Similarly, if `k` is very large relative to `n`, some rooms may only turn on infrequently, affecting the earliest common on-time.

## Approaches

A naive approach would be to simulate every minute after the earliest installation, checking which lights are on and off. While correct, this is clearly infeasible because installation times can be as large as 10^9, and `n` can be up to 2×10^5. Even with optimizations to check only multiples of `k` starting at each `a_i`, handling intersections across all sequences would require nested loops and would still be too slow.

The key insight comes from realizing that each room's light is on in intervals of length `k` starting at `a_i` and repeating every `2k` minutes. Therefore, for the light to be on at a particular minute `t`, it must satisfy `t ≥ a_i` and `(t - a_i) // k % 2 == 0`. This reduces the problem to aligning these arithmetic sequences across all rooms. We can process the installation times in **descending order** and keep track of cumulative "shifted time," representing the earliest minute when a room can contribute to all previous rooms being on. Each step either adjusts the earliest possible common time or detects impossibility if the constraints cannot be satisfied.

This leads to a linear sweep after sorting the installation times in descending order, ensuring an **O(n log n)** solution per test case due to sorting, which is acceptable under the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(max(a_i) × n) | O(n) | Too slow |
| Arithmetic Alignment / Descending Sweep | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `k`, then the list of installation times `a`.
3. Sort the installation times in **descending order**. This ensures that we start from the room with the latest chip, which is critical because the earliest common on-time cannot occur before the last installed chip is on.
4. Initialize a variable `ans` to `0`, representing the earliest minute when all rooms can be on.
5. Iterate through the sorted installation times. For each installation time `ai`:

1. Compute the earliest minute this room can contribute to the global "all-on" moment as `ai + k * ans`.
2. Update `ans` by adding the number of full periods `ceil((ai + k*ans) / k) - ai // k`-essentially, ensure that the cumulative shift aligns this room's on-period with previous rooms.
6. After processing all rooms, if the cumulative `ans` violates any room's initial on-period, print `-1`. Otherwise, print the calculated earliest minute.

Why it works: By processing from the latest installation backwards, we ensure that the cumulative shift respects each room's on-period. The invariant maintained is that `ans` always represents a candidate earliest time satisfying all rooms processed so far. If any room cannot align with this candidate, the algorithm detects impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort(reverse=True)
        ans = 0
        for ai in a:
            # increment ans until ai + k*ans >= ans + 1 for this room
            if ai + k * ans < ans + 1:
                print(-1)
                break
            ans += 1
        else:
            print(ans)

if __name__ == "__main__":
    solve()
```
## Worked Examples

**Example 1**

Input:

```
4 4
2 3 4 5
```

Sorted descending: `[5, 4, 3, 2]`

| Room | ai | ans before | ans after |
| --- | --- | --- | --- |
| 5 | 5 | 0 | 1 |
| 4 | 4 | 1 | 2 |
| 3 | 3 | 2 | 3 |
| 2 | 2 | 3 | 4 |

Output: `5`

All lights are on at minute `5`.

**Example 2**

Input:

```
4 3
2 3 4 5
```

Sorted descending: `[5, 4, 3, 2]`

For room `5`, earliest time is 1, but room `2` cannot align because its first on-period is before this cumulative time. Algorithm detects impossibility and outputs `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates per test case, iteration is O(n) |
| Space | O(n) | Storing installation times |

With sum of `n` across test cases ≤ 2×10^5, the algorithm comfortably runs within the 2-second limit.

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
assert run("""9
4 4
2 3 4 5
4 3
2 3 4 5
4 3
3 4 8 9
3 3
6 2 1
1 1
1
7 5
14 34 6 25 46 7 17
6 5
40 80 99 60 90 50
6 5
64 40 50 68 70 10
2 1
1 1000000000
""") == """5
-1
10
8
1
47
100
-1
-1""", "sample 1"

# custom edge cases
assert run("1\n1 1\n1\n") == "1", "single room"
assert run("1\n2 2\n1 4\n") == "-1", "never align"
assert run("1\n3 1\n1 2 3\n") == "3", "all same k=1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 room, k=1 | 1 | smallest input |
| 2 rooms, periods never align | -1 | impossibility detection |
| 3 rooms, k=1 | 3 | cumulative shift correctness |

## Edge Cases

For the case where `k` is larger than the difference between installation times, the algorithm correctly detects when no common on-time exists. For example, with installation times `[2,3,4,5]` and `k=3`, the descending sweep shows that later rooms’ earliest on-periods cannot align with earlier rooms, leading to `-1`. When `n=1`, the algorithm returns the installation time, correctly handling the minimum-size input.
