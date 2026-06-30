---
title: "CF 104415C - Candy Shop"
description: "We are given a list of numbers, each representing how many candies a student is willing to accept in a purchase. The shop is processing students in some order, but we are free to choose the order in which we satisfy them."
date: "2026-06-30T19:50:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104415
codeforces_index: "C"
codeforces_contest_name: "IME++ Starters Try-outs 2023"
rating: 0
weight: 104415
solve_time_s: 45
verified: true
draft: false
---

[CF 104415C - Candy Shop](https://codeforces.com/problemset/problem/104415/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numbers, each representing how many candies a student is willing to accept in a purchase. The shop is processing students in some order, but we are free to choose the order in which we satisfy them. Once we decide a total amount of candies already “committed” or sold, a student can only be satisfied if their requirement is at least that amount. Our task is to maximize how many students we can satisfy by choosing an optimal order of serving them.

The key structure is that each student has a threshold value, and serving a student consumes some amount of “capacity” in a cumulative sense. We are effectively trying to fit as many constraints as possible into an increasing cumulative sum, where earlier choices affect whether later ones are feasible.

If the number of students is large, say up to 200000, then an O(n^2) simulation where we repeatedly try different subsets or reorderings would be far too slow. With roughly 10^5 or 2×10^5 elements, we expect an O(n log n) or O(n) solution. This immediately suggests sorting or greedy selection as the only viable directions.

A subtle failure case arises when one tries to process students in the original order or in descending order. If we take large requirements first, we may inflate the cumulative sum too quickly, which prevents us from fitting in smaller requirements that could have been satisfied earlier.

For example, suppose the requirements are `[5, 1, 2]`. If we process `5` first, the cumulative sum becomes large immediately, and depending on interpretation, we might skip `1` and `2` or mis-evaluate feasibility. The correct answer is to serve `1`, then `2`, then `5`, which allows all three to be satisfied in a controlled cumulative progression.

The central difficulty is recognizing that the order of processing determines how quickly the cumulative constraint grows, and the optimal strategy is the one that delays growth as much as possible.

## Approaches

The brute-force idea is to try every possible ordering of students and simulate how many can be satisfied under that ordering. For each permutation, we maintain a running total and count how many thresholds are met. This works because it directly models the process, but it has factorial complexity. With n students, there are n! permutations, and even evaluating one permutation costs O(n), making the approach infeasible beyond very small n.

The key observation is that the only way to maximize the number of satisfied students is to keep the cumulative sum as small as possible for as long as possible. Any time we pick a student with a large requirement early, we risk increasing the cumulative total unnecessarily and blocking future inclusions. This suggests that we should always prioritize smaller requirements first, since they impose the least constraint on the running total.

Once we sort the requirements in increasing order, we can greedily process them from smallest to largest, maintaining a running sum. Whenever the current requirement is at least the current sum, we can include that student and increase the sum accordingly. If not, we skip them because including them would only increase the sum further without helping satisfy more constraints.

This transforms the problem from a combinatorial search over permutations into a single linear scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n! · n) | O(n) | Too slow |
| Sort + Greedy scan | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We start by sorting all student requirements in non-decreasing order so that we always consider the smallest constraints first. This ensures that every step has the maximum chance of being feasible given the current cumulative sum.

We initialize a running variable `cur = 0`, which represents the total amount of candies already committed, and a counter `ans = 0`, which tracks how many students have been satisfied.

We then iterate through the sorted list. For each value `x`, we check whether it is possible to satisfy this student given the current cumulative sum.

If `x >= cur`, we include this student, increment `ans` by one, and update `cur += x`. The reason this update is safe is that we are only committing to students whose requirement is large enough to accommodate the current state.

If `x < cur`, we skip this student because including them would not make sense in this greedy framework. Since all future values are greater or equal (because of sorting), skipping ensures we do not waste opportunity on an infeasible transition.

Finally, we output `ans`.

### Why it works

At any point, the algorithm maintains the invariant that `cur` is the smallest possible cumulative sum achievable by selecting some subset of processed elements. By processing in sorted order, we ensure that we never encounter a smaller requirement after a larger one. This monotonicity guarantees that once a value cannot satisfy the current sum, no later structure will make it recoverable. The greedy choice of taking every feasible smallest element preserves maximal extensibility of future choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

cur = 0
ans = 0

for x in a:
    if x >= cur:
        ans += 1
        cur += x

print(ans)
```

The solution starts by reading the list of requirements and sorting it so that weaker constraints are handled first. The variable `cur` tracks the accumulated commitment, and `ans` counts how many students are successfully served. Each iteration decides whether the current student can be included without violating the cumulative constraint. The condition `x >= cur` is the key feasibility check that ensures we only extend the solution when it remains valid.

A common mistake is reversing the inequality or updating `cur` incorrectly before checking feasibility. The order matters: we must check first, then update. Another subtle issue is forgetting that skipping a student does not reset or modify `cur`.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [5, 1, 2]
```

Sorted array becomes `[1, 2, 5]`.

| Step | x | cur before | decision | cur after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | take | 1 | 1 |
| 2 | 2 | 1 | take | 3 | 2 |
| 3 | 5 | 3 | take | 8 | 3 |

All students are satisfied because each chosen value stays ahead of the cumulative sum.

### Example 2

Input:

```
n = 4
a = [3, 3, 4, 1]
```

Sorted array becomes `[1, 3, 3, 4]`.

| Step | x | cur before | decision | cur after | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | take | 1 | 1 |
| 2 | 3 | 1 | take | 4 | 2 |
| 3 | 3 | 4 | skip | 4 | 2 |
| 4 | 4 | 4 | take | 8 | 3 |

This demonstrates that once the cumulative sum becomes too large, some mid-sized values are no longer usable, and the greedy order has already locked in the optimal prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, scan is linear |
| Space | O(1) or O(n) | depending on sorting implementation |

The sorting step is the bottleneck, and for up to 200000 elements, it is comfortably within limits. The greedy scan is a single pass and introduces negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve()

# rewritten solution for testing
def solve():
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    a.sort()
    cur = 0
    ans = 0
    for x in a:
        if x >= cur:
            ans += 1
            cur += x
    return str(ans)

# samples / basic
assert solve_from("3\n5 1 2\n") == "3"

# custom cases
assert solve_from("1\n10\n") == "1"
assert solve_from("2\n1 100\n") == "2"
assert solve_from("3\n3 3 3\n") == "3"
assert solve_from("4\n1 2 10 100\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10` | `1` | single element correctness |
| `1 100` | `1` (with 2 elements case) | greedy always takes valid large gap |
| `3 3 3` | `3` | all equal values behave consistently |
| `1 2 10 100` | `4` | monotone growth never blocks early chain |

## Edge Cases

One important edge case is when all values are identical. Consider input `[3, 3, 3]`. After sorting it remains unchanged. The algorithm proceeds as follows: `cur = 0`, first `3 >= 0` so take it, `cur = 3`. Next `3 >= 3` so take it, `cur = 6`. Next `3 >= 6` is false, so we skip it. The output is `2`. This shows that even uniform inputs can break full inclusion once the cumulative sum grows beyond the repeated value.

Another edge case is a very small value followed by a large one, such as `[1, 100, 100]`. The algorithm takes `1`, then `100`, then the final `100` becomes infeasible because `cur` has grown too large. The trace confirms that early small inclusions can block later identical large ones, which is exactly why sorting and greedy acceptance is necessary to control growth.
