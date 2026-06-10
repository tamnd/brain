---
title: "CF 1487A - Arena"
description: "We are given a collection of heroes, each with an initial strength or level. They fight pairwise, and whenever two heroes with different levels meet, the stronger one wins and grows stronger. If their levels are equal, the fight is a draw and nobody gains anything."
date: "2026-06-10T22:58:38+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1487
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 104 (Rated for Div. 2)"
rating: 800
weight: 1487
solve_time_s: 130
verified: true
draft: false
---

[CF 1487A - Arena](https://codeforces.com/problemset/problem/1487/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of heroes, each with an initial strength or level. They fight pairwise, and whenever two heroes with different levels meet, the stronger one wins and grows stronger. If their levels are equal, the fight is a draw and nobody gains anything. We are asked to find how many heroes have a chance to become the ultimate champion if we can choose the order of fights arbitrarily. In other words, a hero is a possible winner if there exists a sequence of fights in which this hero ends up winning an astronomically large number of duels.

The input provides the number of heroes and their initial levels. The output is the count of heroes that could potentially win under some sequence of fights. With $n$ up to $100$ and levels capped at $100$, we can afford to consider each hero individually and reason about relative levels. Brute-force simulation of all possible sequences is impractical because the number of sequences grows explosively.

A subtle edge case is when all heroes have equal levels. In that scenario, every fight is a draw, so no hero can accumulate wins. For example, with levels `[5, 5]`, the answer is `0`. Another edge case occurs when there is only one hero strictly stronger than the others; only that hero can win. For `[3, 2, 2]`, the strongest hero alone is a possible winner. Naive approaches might incorrectly count heroes with the second-highest level as winners because they could win small fights, but in reality they can never surpass the strongest hero in a sequence optimized for the eventual winner.

## Approaches

A brute-force approach would attempt to simulate all sequences of fights. For each hero, we could try every possible pair of duels and track wins. This is correct in principle, but the number of fights required is astronomically large (`100^500`), so any actual simulation is impossible. The operation count would explode even for `n = 100`, making it infeasible.

The key observation is that a hero can only be a possible winner if their level is not strictly smaller than the smallest level of any potential rival that can eventually surpass them. Concretely, the minimum-level hero can never block a stronger hero from winning, and a hero with level one less than the maximum cannot prevent the maximum-level hero from eventually winning. Therefore, we only need to consider the hero with the minimum level. A hero is a possible winner if their level is greater than or equal to the minimum level in the array.

This insight reduces the problem to finding the smallest level and counting heroes whose level is greater than `min_level`. If all heroes are tied at the minimum level, no one can win, which matches the edge case discussed above.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(???) | O(n) | Infeasible due to huge number of fights |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, process the following steps.
2. Read `n`, the number of heroes, and the array of their levels `a`.
3. Determine the minimum level among all heroes. This level represents the “weakest” possible hero that can participate in a winning sequence.
4. Count all heroes whose level is strictly greater than this minimum. These heroes are candidates because they can always dominate the minimum-level heroes until the very end.
5. Print the count for the current test case.

Why it works: A hero cannot become a possible winner if there exists a strictly stronger hero, because eventually that hero will always surpass them in wins. Conversely, any hero whose level is above the minimum can, in some sequence of fights, eliminate or stay ahead of weaker heroes and accumulate the required wins. This reduces the problem to a simple comparison with the minimum level.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    min_level = min(a)
    count = sum(1 for x in a if x > min_level)
    print(count)
```

The solution first reads the number of test cases. For each test case, it reads the hero levels and computes the minimum. We then count heroes strictly stronger than the minimum. Using a generator expression avoids unnecessary intermediate lists. This ensures O(n) processing per test case, which is efficient given the constraints.

## Worked Examples

### Example 1

Input: `[3, 2, 2]`

| Hero | Level | Level > min_level? |
| --- | --- | --- |
| 1 | 3 | Yes |
| 2 | 2 | No |
| 3 | 2 | No |

The minimum level is `2`. Only the hero with level `3` exceeds this minimum, so there is 1 possible winner.

### Example 2

Input: `[5, 5]`

| Hero | Level | Level > min_level? |
| --- | --- | --- |
| 1 | 5 | No |
| 2 | 5 | No |

All heroes have the same level. The minimum is `5` and no hero is strictly stronger, so the count is `0`.

### Example 3

Input: `[1, 3, 3, 7]`

| Hero | Level | Level > min_level? |
| --- | --- | --- |
| 1 | 1 | No |
| 2 | 3 | Yes |
| 3 | 3 | Yes |
| 4 | 7 | Yes |

Minimum is `1`. Three heroes are strictly stronger, so the answer is `3`.

These traces confirm the algorithm correctly counts heroes who are strictly stronger than the weakest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case scans n elements twice (min and count). Maximum t = 500, n = 100 → 50,000 operations. |
| Space | O(n) | We store levels in an array for each test case. |

The solution fits comfortably within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        min_level = min(a)
        count = sum(1 for x in a if x > min_level)
        print(count)
    return output.getvalue().strip()

# provided samples
assert run("3\n3\n3 2 2\n2\n5 5\n4\n1 3 3 7\n") == "1\n0\n3", "sample 1"

# custom cases
assert run("1\n2\n1 100\n") == "1", "one very strong, one weak"
assert run("1\n5\n10 10 10 10 10\n") == "0", "all equal levels"
assert run("1\n4\n1 2 3 4\n") == "3", "all different levels"
assert run("1\n3\n2 2 3\n") == "1", "single winner above duplicates"
assert run("1\n2\n100 1\n") == "1", "max and min boundary values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n1 100` | `1` | One strong hero dominates weak hero |
| `5\n10 10 10 10 10` | `0` | All equal, no winner |
| `4\n1 2 3 4` | `3` | Multiple heroes stronger than min |
| `3\n2 2 3` | `1` | Only strongest among duplicates wins |
| `2\n100 1` | `1` | Boundary value handling |

## Edge Cases

If all heroes have the same level, the minimum equals all levels, and no hero is strictly stronger. The algorithm correctly returns `0`. For heroes with one exceptionally strong hero and several weak heroes, the algorithm counts only the strong hero as a possible winner. For small arrays (`n = 2`), the algorithm handles both equal and unequal values correctly. The implementation also works for the maximum allowed levels (`100`) and maximum number of heroes (`100`) without overflow or inefficiency.
