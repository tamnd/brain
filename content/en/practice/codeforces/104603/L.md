---
title: "CF 104603L - Game series"
description: "The task describes a two-match football series between two teams, Archimedians F.C. and Pithgoreans F.C. Each match produces a score for both teams, and the winner of the series is decided by summing goals across both matches."
date: "2026-06-30T02:56:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104603
codeforces_index: "L"
codeforces_contest_name: "2023 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 104603
solve_time_s: 45
verified: true
draft: false
---

[CF 104603L - Game series](https://codeforces.com/problemset/problem/104603/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a two-match football series between two teams, Archimedians F.C. and Pithgoreans F.C. Each match produces a score for both teams, and the winner of the series is decided by summing goals across both matches. If one team has a strictly higher total number of goals, that team wins the series. If both teams end with exactly the same total score, the series is not resolved and instead goes to a third tiebreaker match, which is not part of the input.

The input consists of two pairs of integers. The first pair represents the goals scored by Archimedians and Pithgoreans in the first match. The second pair represents the same information for the second match. The output is a single character indicating the outcome of the series after summing both matches.

Although the problem is extremely small in terms of constraints, the reasoning still benefits from being explicit about aggregation and comparison. Each score is bounded between 0 and 31, which ensures that the total per team is at most 62. This guarantees there are no overflow concerns in any standard integer type and also confirms that a direct computation approach is sufficient without optimizations.

The only subtle edge case is when the totals are equal. For example, if the inputs are `3 1` and `1 3`, both teams end with 4 goals. In this case, the correct output is `D`, meaning a deciding match is required. A naive mistake would be to compare match-by-match winners instead of total goals, which would incorrectly suggest a draw or even a winner based on per-game outcomes.

Another potential pitfall is forgetting to aggregate both matches before comparing. For instance, in `3 0` and `0 3`, each team wins one match individually, but the correct logic still leads to a draw because total goals are equal.

## Approaches

A brute-force interpretation might try to reason about each match separately, deciding a winner per game and then attempting to combine outcomes. This approach is flawed because the series rule depends only on total goals, not match victories. Even if implemented correctly, it introduces unnecessary logic to track per-game results when a simple sum is sufficient.

The correct and optimal approach is to aggregate goals for both teams across the two matches and then compare the totals directly. This works because the series definition reduces the entire problem to a single scalar comparison per team. The structure of the problem eliminates any interaction between matches beyond addition.

The brute-force idea would still run in constant time, but with more complicated state handling. The optimal solution simplifies everything to two additions and one comparison, reducing both cognitive and implementation complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Match-by-match reasoning | O(1) | O(1) | Unnecessary complexity |
| Total sum comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers representing the two match results. The first two correspond to Archimedians and Pithgoreans in the first match, and the next two correspond to the second match.
2. Compute the total goals for Archimedians by summing their scores from both matches. This directly represents their full contribution across the series.
3. Compute the total goals for Pithgoreans in the same way, ensuring symmetry in how both teams are evaluated.
4. Compare the two totals. If Archimedians’ total is greater, the series result is determined immediately as a win for Archimedians.
5. If Pithgoreans’ total is greater, they are declared the winner.
6. If neither total is greater, the totals must be equal, which implies the series is undecided and requires a tiebreaker match.

The correctness comes from the fact that the problem definition reduces all match-level outcomes into a single aggregate score comparison. Once totals are computed, no additional structure from the individual games can affect the decision.

## Python Solution

```python
import sys
input = sys.stdin.readline

a1, p1 = map(int, input().split())
a2, p2 = map(int, input().split())

a_total = a1 + a2
p_total = p1 + p2

if a_total > p_total:
    print("A")
elif p_total > a_total:
    print("P")
else:
    print("D")
```

The solution reads two lines and immediately aggregates the scores for both teams. The decision logic is then a direct comparison of the two totals. There is no need for loops or additional data structures since the input size is fixed.

A common implementation mistake would be to compare `(a1 > p1) + (a2 > p2)` instead of total goals. That would incorrectly treat match wins as equivalent to goals, which is not what the problem defines.

## Worked Examples

First sample input:

Input:

3 1

1 1

We compute totals step by step.

| Step | Archimedians | Pithgoreans |
| --- | --- | --- |
| Match 1 | 3 | 1 |
| Match 2 | 1 | 1 |
| Total | 4 | 2 |

Archimedians have a higher total, so the output is `A`.

Second sample input:

Input:

4 3

1 3

| Step | Archimedians | Pithgoreans |
| --- | --- | --- |
| Match 1 | 4 | 3 |
| Match 2 | 1 | 3 |
| Total | 5 | 6 |

Pithgoreans have the higher total, so the output is `P`.

Third sample input:

Input:

2 4

2 0

| Step | Archimedians | Pithgoreans |
| --- | --- | --- |
| Match 1 | 2 | 4 |
| Match 2 | 2 | 0 |
| Total | 4 | 4 |

Totals are equal, so the result is `D`.

These traces confirm that only total aggregation matters, and match-level outcomes are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The input size is fixed to two matches, so the algorithm runs in constant time regardless of constraints. This is well within any reasonable time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import Popen, PIPE
    # simulate by executing the solution directly
    a1, p1 = map(int, sys.stdin.readline().split())
    a2, p2 = map(int, sys.stdin.readline().split())
    a_total = a1 + a2
    p_total = p1 + p2
    if a_total > p_total:
        return "A"
    elif p_total > a_total:
        return "P"
    else:
        return "D"

# provided samples
assert run("3 1\n1 1\n") == "A"
assert run("4 3\n1 3\n") == "P"
assert run("2 4\n2 0\n") == "D"

# custom cases
assert run("0 0\n0 0\n") == "D"
assert run("31 0\n0 31\n") == "D"
assert run("31 0\n0 0\n") == "A"
assert run("0 31\n0 0\n") == "P"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 / 0 0 | D | both teams completely equal |
| 31 0 / 0 31 | D | maximum values but balanced totals |
| 31 0 / 0 0 | A | extreme unbalanced win for Archimedians |
| 0 31 / 0 0 | P | symmetric extreme win for Pithgoreans |

## Edge Cases

The equality scenario is the only structurally important edge case. For input `0 0` and `0 0`, both totals are zero. The algorithm computes `a_total = 0` and `p_total = 0`, reaches the equality branch, and outputs `D`, which matches the requirement for a tiebreaker.

Another boundary case is when one team scores maximally in one match and zero in the other, such as `31 0` and `0 31`. The totals again equalize at 31, leading to output `D`. This confirms that match distribution does not matter, only cumulative scoring.

A third case is a fully dominant performance like `31 0` and `0 0`. Here Archimedians total 31 while Pithgoreans total 0, producing output `A`. The symmetric case behaves identically for Pithgoreans. These confirm that the algorithm correctly handles extreme inputs without overflow or ordering issues.
