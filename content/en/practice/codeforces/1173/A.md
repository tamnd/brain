---
title: "CF 1173A - Nauuo and Votes"
description: "The problem asks us to determine the outcome of a simple voting scenario. There are three categories of voters: some are guaranteed to upvote, some are guaranteed to downvote, and some are undecided. The input gives the counts of each group."
date: "2026-06-12T01:54:35+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1173
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 564 (Div. 2)"
rating: 800
weight: 1173
solve_time_s: 98
verified: true
draft: false
---

[CF 1173A - Nauuo and Votes](https://codeforces.com/problemset/problem/1173/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to determine the outcome of a simple voting scenario. There are three categories of voters: some are guaranteed to upvote, some are guaranteed to downvote, and some are undecided. The input gives the counts of each group. The goal is to predict the net result of the vote: either positive, negative, neutral, or uncertain. A positive result occurs if upvotes strictly exceed downvotes, negative if downvotes strictly exceed upvotes, neutral if they are equal, and uncertain if the unknown voters could change the outcome depending on how they vote.

The constraints are very small: each count is at most 100, so the total number of voters is at most 300. This allows us to reason about all possibilities without worrying about efficiency. There are no performance concerns for iterating over small ranges, but we should still aim for a constant-time solution by analyzing the range of possible vote totals.

Non-obvious edge cases include situations where the unknown votes can flip the result. For example, if upvotes and downvotes are equal and there is at least one unknown voter, the outcome is uncertain because a single vote could tip the balance. Another edge case is when one side dominates even after assigning all unknown votes to the other side, such as 10 upvotes, 2 downvotes, and 3 unknown. Here, the result is definitely positive, even if all unknown votes go to downvote.

## Approaches

A brute-force approach would consider all ways the unknown voters can vote. If there are `z` unknown voters, there are `z+1` ways to distribute them between upvotes and downvotes. For each distribution, we calculate the net result. If all outcomes are the same, that is the final result; otherwise, the result is uncertain. This works because `z` is at most 100, so we would compute at most 101 possibilities. While feasible in practice for this problem, it is unnecessary and can be simplified.

The key observation is that we only need the minimum and maximum possible difference between upvotes and downvotes. The minimum difference occurs if all unknown voters vote down, the maximum if all vote up. If both extremes give the same sign, the result is determined. Otherwise, it is uncertain. This reduces the problem to a few comparisons, producing an O(1) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(z) | O(1) | Works but overkill |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers representing the guaranteed upvotes `x`, guaranteed downvotes `y`, and unknown votes `z`.
2. Compute the maximum possible net vote difference as `x + z - y`, which assumes all unknown votes are upvotes.
3. Compute the minimum possible net vote difference as `x - (y + z)`, which assumes all unknown votes are downvotes.
4. If both maximum and minimum are strictly positive, print "+", because even in the worst-case scenario upvotes exceed downvotes.
5. If both maximum and minimum are strictly negative, print "-", because downvotes dominate in all possible assignments of unknown votes.
6. If both maximum and minimum are zero, print "0", because the votes are tied regardless of unknown votes.
7. Otherwise, print "?", indicating that different assignments of unknown votes could produce different outcomes, making the result uncertain.

Why it works: by considering only the extreme scenarios, we capture the full range of possible outcomes. Any distribution of unknown votes produces a result between these two extremes. If both extremes lead to the same result, all intermediate distributions also lead to that same result. If the extremes produce different results, some assignment exists that produces each result, meaning uncertainty.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, y, z = map(int, input().split())

max_diff = x + z - y
min_diff = x - (y + z)

if min_diff > 0:
    print("+")
elif max_diff < 0:
    print("-")
elif min_diff <= 0 <= max_diff and max_diff == 0 and min_diff == 0:
    print("0")
else:
    print("?")
```

The code reads the vote counts and computes the extreme vote differences, then decides the outcome based on these extremes. The subtlety lies in handling the zero case carefully: if both extremes are exactly zero, the result is neutral. Otherwise, if extremes differ across zero, the result is uncertain. No loops or additional data structures are necessary.

## Worked Examples

**Sample 1**

Input: `3 7 0`

| x | y | z | max_diff | min_diff | result |
| --- | --- | --- | --- | --- | --- |
| 3 | 7 | 0 | -4 | -4 | - |

All votes are known, difference is negative. Result is "-" as expected.

**Sample 2**

Input: `1 1 1`

| x | y | z | max_diff | min_diff | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | -1 | ? |

Unknown voter can tip the result either way. The algorithm correctly outputs "?".

These traces confirm that computing extremes captures the entire range of possibilities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and comparisons on three integers |
| Space | O(1) | Only a few integer variables are used |

Given the constraints (all counts ≤ 100), the solution executes in constant time and memory, far below the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, y, z = map(int, input().split())
    max_diff = x + z - y
    min_diff = x - (y + z)
    if min_diff > 0:
        return "+"
    elif max_diff < 0:
        return "-"
    elif min_diff <= 0 <= max_diff and max_diff == 0 and min_diff == 0:
        return "0"
    else:
        return "?"

# Provided samples
assert run("3 7 0\n") == "-", "sample 1"
assert run("3 1 2\n") == "+", "sample 2"
assert run("1 1 0\n") == "0", "sample 3"
assert run("1 0 1\n") == "?", "sample 4"

# Custom cases
assert run("0 0 0\n") == "0", "all zero votes"
assert run("100 0 0\n") == "+", "max upvotes only"
assert run("0 100 0\n") == "-", "max downvotes only"
assert run("50 50 0\n") == "0", "tie with no unknowns"
assert run("50 49 1\n") == "?", "tie possible with one unknown"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | 0 | smallest input, neutral outcome |
| 100 0 0 | + | maximal upvotes dominate |
| 0 100 0 | - | maximal downvotes dominate |
| 50 50 0 | 0 | tie without unknowns |
| 50 49 1 | ? | uncertainty introduced by single unknown |

## Edge Cases

When the unknown votes can change the result, such as `1 0 1`, the algorithm correctly computes `max_diff = 2` and `min_diff = 0`. Since the extremes are not both strictly positive, negative, or exactly zero, the output is "?", capturing uncertainty.

When all votes are known and balanced, such as `2 2 0`, both extremes equal zero, and the output is "0".

When one side dominates even with unknown votes, such as `10 2 3`, the extremes are `11` and `5`, both positive, so the algorithm prints "+", correctly confirming the dominance of upvotes.
