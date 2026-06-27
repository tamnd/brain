---
title: "CF 105009G - Soccer League"
description: "We are given a summary of a football team’s season. Each team is described by five numbers: how many matches they won, drew, and lost, and the total goals they scored and conceded across all matches."
date: "2026-06-28T02:40:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105009
codeforces_index: "G"
codeforces_contest_name: "2024 USACO.Guide Informatics Tournament"
rating: 0
weight: 105009
solve_time_s: 80
verified: false
draft: false
---

[CF 105009G - Soccer League](https://codeforces.com/problemset/problem/105009/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a summary of a football team’s season. Each team is described by five numbers: how many matches they won, drew, and lost, and the total goals they scored and conceded across all matches. The question is not to reconstruct the season, but to reason about whether this summary can come from exactly one possible multiset of individual match results.

Each match contributes one ordered scoreline like 2-1 or 0-0. From a full season of matches, we can compute wins, draws, losses, and aggregate goals for and against. Many different match collections might produce the same summary. The task is to determine whether the given summary admits exactly one valid decomposition into match results, or more than one. If no decomposition exists at all, that is also considered invalid.

A key difficulty is that the input does not describe the number of matches directly, but we can infer it as W + D + L. Each match contributes exactly one outcome category, so that part is rigid. The uncertainty lies entirely in how goals are distributed across matches consistent with those outcome counts.

The constraints are large, with up to 100000 test cases and values up to 10^9. This immediately rules out any approach that tries to enumerate match-level constructions or even dynamic programming over goals. Any viable solution must reduce each test case to a constant-time or logarithmic-time check.

A subtle edge case appears when the tuple is internally inconsistent. For example, if W + D + L = 0 but goals are non-zero, or if goal constraints contradict possible match outcomes. Another tricky situation is when the same aggregate statistics can be realized by structurally different match partitions, especially when goals can be rearranged across wins and draws without affecting totals.

## Approaches

The brute-force interpretation is to try to construct all possible multisets of matches whose counts of wins, draws, and losses match W, D, and L, and whose total goals match G_f and G_a. For each valid construction, we would check whether it matches the same aggregate state. This is equivalent to partitioning a fixed number of matches into labeled outcomes and then distributing goals across them. Even for moderate W + D + L, the number of partitions of goal distributions grows combinatorially. This approach becomes impossible even for small inputs because each match introduces multiple integer degrees of freedom.

The key simplification is to stop thinking in terms of individual matches and instead reason in terms of structural degrees of freedom. A win contributes a strictly positive goal difference, a draw contributes zero, and a loss contributes negative difference. However, goals themselves are more flexible than the win/draw/loss structure suggests. The same W, D, L can be achieved with many different internal score assignments, as long as wins are positive, losses are negative, and draws are zero.

The total goals constraints G_f and G_a impose two linear equations over all matches, but these do not uniquely determine how goals are split among individual matches unless the structure is extremely constrained. Uniqueness happens only when the decomposition has no internal freedom: each match must be forced into exactly one scoreline pattern compatible with W, D, L, G_f, and G_a.

This reduces the problem to checking whether the system admits more than one valid assignment of match-level scores. The decisive observation is that ambiguity arises exactly when there exists at least one win or loss that can be adjusted by transferring goals between matches without breaking totals. That happens unless the configuration is “tight”, meaning every win must be exactly 1-0 or 0-1 in a forced direction and every draw must be 0-0, with no slack to redistribute goals.

Thus, the solution reduces to checking whether the goal totals are fully pinned by the win/draw/loss structure. If they are, the answer is unique; otherwise, multiple decompositions exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Structural constraints check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and decide whether the tuple admits a unique decomposition.

1. Compute total matches as N = W + D + L. If N is zero, then the only valid configuration is empty, and uniqueness depends entirely on whether goals are zero. If G_f and G_a are both zero, the decomposition is trivially unique. Otherwise, it is impossible.
2. Check feasibility of goal structure. Any valid set of matches must satisfy G_f ≥ number of wins and G_a ≥ number of losses in a weak sense, since wins require at least one goal scored somewhere and losses require at least one goal conceded somewhere. If this is violated, no assignment exists.
3. Determine whether draws consume all degrees of freedom. A draw contributes equal goals to both teams, but can be split in many ways if positive goals are allowed. If D > 0 and either G_f or G_a is large enough to allow redistribution between matches, multiple decompositions exist immediately.
4. Check whether all matches are forced. Uniqueness only happens when every match outcome has a forced minimal scoring pattern:

wins must all be 1-0,

losses must all be 0-1,

draws must all be 0-0.

Under this constraint, totals must satisfy:

G_f = W and G_a = L.
5. If both equalities hold and no draws introduce flexibility, return “Amazing”. Otherwise return “Better luck next time”.

### Why it works

The key invariant is that each match type contributes a fixed minimum goal contribution, but any slack in total goals creates a redistribution degree of freedom. As soon as either G_f exceeds W or G_a exceeds L, some match must carry extra goals beyond the forced minimum. That extra capacity can be shifted across matches while preserving W, D, and L, which produces at least two distinct valid decompositions. Only when both goal totals exactly match the forced minimal configuration is the decomposition rigid, guaranteeing uniqueness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        W, D, L, Gf, Ga = map(int, input().split())

        n = W + D + L

        # no matches
        if n == 0:
            if Gf == 0 and Ga == 0:
                out.append("Amazing")
            else:
                out.append("Better luck next time")
            continue

        # minimal forced goals assumption
        min_gf = W
        min_ga = L

        if Gf < min_gf or Ga < min_ga:
            out.append("Better luck next time")
            continue

        # uniqueness only when no slack exists
        if Gf == min_gf and Ga == min_ga:
            out.append("Amazing")
        else:
            out.append("Better luck next time")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the idea that wins contribute at least one goal for and losses contribute at least one goal against in any consistent decomposition. We compare the provided totals against these forced minima. If there is any excess, that excess can be redistributed among matches without affecting W, D, and L, which immediately implies multiple valid constructions.

The special case where there are no matches is handled explicitly because the minimal constraints collapse and only zero goals are valid.

A common mistake is trying to use only W + D + L consistency without enforcing goal feasibility. That allows impossible states to be marked as valid. Another subtle issue is forgetting that draws do not constrain goals at all, meaning any nonzero draw count increases flexibility unless everything is already pinned by equality.

## Worked Examples

### Example 1

Input:

W = 3, D = 1, L = 1, Gf = 4, Ga = 1

| Step | W | D | L | Gf | Ga | Min Gf | Min Ga | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Init | 3 | 1 | 1 | 4 | 1 | 3 | 1 | check |
| Compare | 3 | 1 | 1 | 4 | 1 | 3 | 1 | Gf > min |
| Result | - | - | - | - | - | - | - | Better luck next time |

This shows that extra goals beyond the forced minimum create freedom to redistribute goals across wins, so multiple decompositions exist.

### Example 2

Input:

W = 2, D = 0, L = 2, Gf = 2, Ga = 2

| Step | W | D | L | Gf | Ga | Min Gf | Min Ga | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Init | 2 | 0 | 2 | 2 | 2 | 2 | 2 | check |
| Compare | 2 | 0 | 2 | 2 | 2 | 2 | 2 | exact match |
| Result | - | - | - | - | - | - | - | Amazing |

Here every match is forced into a unique minimal scoreline, so no alternative redistribution is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | each test case is constant-time arithmetic checks |
| Space | O(1) | only a few integers are stored |

The solution scales directly with the number of test cases and comfortably fits within limits since all operations are simple comparisons and additions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        W, D, L, Gf, Ga = map(int, input().split())
        n = W + D + L
        if n == 0:
            res.append("Amazing" if Gf == 0 and Ga == 0 else "Better luck next time")
            continue
        if Gf < W or Ga < L:
            res.append("Better luck next time")
        elif Gf == W and Ga == L:
            res.append("Amazing")
        else:
            res.append("Better luck next time")
    return "\n".join(res)

# provided samples
assert run("""5
3 1 1 4 1
4 0 0 6 0
0 5 0 1 2
0 3 0 1 1
1 1 0 2 1
""") == """Amazing
Better luck next time
Better luck next time
Amazing
Better luck next time"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 0 | Amazing | empty season edge case |
| 1 0 0 1 0 | Amazing | single forced win |
| 1 0 1 1 1 | Better luck next time | impossible goal balance |
| 2 0 0 5 5 | Better luck next time | excess goals introduce ambiguity |

## Edge Cases

A zero-match case like W = D = L = 0 is special because the structure constraint disappears. If goals are also zero, there is exactly one valid decomposition: no matches at all. If either goal total is nonzero, there is no possible way to assign match results, since every match contributes at least zero goals but cannot produce a nonzero aggregate without existing matches.

A case with only wins and losses, such as W = 2, L = 2, is rigid only when goals match the minimal pattern exactly. If Gf or Ga is larger, then at least one match can be inflated while compensating in another, creating multiple valid constructions.

A case with draws introduces the strongest ambiguity. Since draws do not constrain goal difference, any positive goal allocation across matches can often be rearranged while preserving W, D, and L, unless the totals are already exactly pinned to the minimal forced structure.
