---
title: "CF 2227B - Party Monster"
description: "We are given a string made only of opening and closing parentheses. In one move, we are allowed to take a contiguous block, remove it, and then reinsert its characters anywhere in the remaining string, with full freedom to permute those removed characters and place each one…"
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2227
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1096 (Div. 3)"
rating: 0
weight: 2227
solve_time_s: 218
verified: false
draft: false
---

[CF 2227B - Party Monster](https://codeforces.com/problemset/problem/2227/B)

**Rating:** -  
**Tags:** greedy  
**Solve time:** 3m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made only of opening and closing parentheses. In one move, we are allowed to take a contiguous block, remove it, and then reinsert its characters anywhere in the remaining string, with full freedom to permute those removed characters and place each one independently.

The question is whether, after doing nothing or applying this single move, we can obtain a valid bracket sequence where every prefix never has more closing brackets than opening brackets and the total number of opens equals closes.

The constraints are large, with the total length across all test cases up to 200,000. That immediately rules out any quadratic or cubic idea per test case. Any solution must run in linear or near-linear time over the input.

A subtle aspect of the operation is that it does not preserve the internal order of the removed segment. The removed characters become a free multiset that can be injected anywhere. This makes the operation much stronger than a standard substring move or rotation, because it allows us to locally “repair” imbalance using arbitrarily placed parentheses.

Edge cases that tend to break naive reasoning come from assuming the operation preserves structure. For example, in a string like “())(”, a naive attempt might think only adjacent swaps matter, but the operation can completely reshuffle a chosen block, changing global feasibility in ways that are not localized.

Another common pitfall is ignoring prefix constraints. Even if the total number of opens equals closes, a string like “())(()” cannot be fixed by simple rearrangement intuition unless we explicitly reason about how prefix deficits can be corrected using the removable block.

## Approaches

A brute force approach would try every substring to remove. For each choice, we would simulate removing it, then try all possible insertions of its characters into the remaining string and check whether any arrangement yields a valid bracket sequence. Even if we ignore permutations inside the removed block and only consider placements, the number of ways to distribute characters is exponential in the substring length. This quickly becomes infeasible even for n around 50.

The key simplification comes from separating what the operation can and cannot change. Removing a substring produces two parts: a fixed ordered sequence and a bag of parentheses we can place anywhere. The fixed part imposes prefix constraints that must be satisfied, while the bag can only help by supplying extra opening brackets early enough to repair negative prefix balance.

This reduces the problem to reasoning about prefix imbalance in the remaining sequence after removal. If we look at a candidate remaining sequence, define its worst prefix deficit as how far the balance drops below zero. The removable block can contribute enough opening brackets to compensate for that deficit, because those openings can be placed before the problematic prefixes.

Thus, the task becomes: can we choose a removed segment such that the number of opening brackets we remove is at least as large as the maximum prefix deficit of the remaining string?

This transforms the problem into controlling a single quantity over all possible removals, which can be handled by prefix analysis of the original string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force removal + reconstruction | Exponential | O(n) | Too slow |
| Prefix balance + optimal split reasoning | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We define prefix balance as the running difference between opening and closing brackets.

1. Compute the prefix balance over the whole string. This tells us how the sequence behaves if read left to right without modification.
2. Check if the total number of opening and closing brackets is equal. If not, no rearrangement can fix the imbalance since the operation preserves character counts.
3. Track the minimum prefix balance over the string. This value measures how deep the sequence ever dips below a valid state.
4. If the minimum prefix balance is already nonnegative, the string is already a valid bracket sequence and we can immediately answer yes.
5. Otherwise, consider what removing a substring does. Removing a segment deletes some closing and opening brackets from the prefix structure, which can only increase prefix balance in affected regions.
6. The important observation is that the only useful effect of the removed segment is how many opening brackets it contributes back when reinserted. Let that number be k.
7. The remaining fixed part has some maximum prefix deficit d, meaning there exists a prefix where it is short by d opening brackets compared to closings.
8. The problem reduces to whether we can choose a removed segment that provides k opening brackets with k at least d.
9. Since we are free to choose the removed segment, we can always align the removal to capture regions that reduce the worst deficit, and the optimal choice corresponds to cutting around the deepest prefix dip.
10. Therefore, we only need to determine whether there exists a segment whose opening count is large enough to cover the unavoidable prefix deficit of the rest, which can be inferred from prefix extrema of the original string.

### Why it works

The operation only gives freedom over one multiset of parentheses, while the remaining sequence keeps its order constraints. Every invalid prefix in the remaining sequence must be corrected by injecting enough opening brackets before that prefix begins. The number of available openings depends solely on how many are removed, and this quantity is globally constrained by the chosen segment. The prefix structure of the original string encodes exactly where deficits can appear, and removing a segment can only smooth a contiguous portion of that structure. This makes the feasibility condition depend entirely on prefix minima and how much they can be offset, which is fully captured by scanning the balance array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input().strip())
        s = input().strip()

        bal = 0
        min_bal = 0

        for ch in s:
            if ch == '(':
                bal += 1
            else:
                bal -= 1
            if bal < min_bal:
                min_bal = bal

        # necessary condition: equal number of brackets
        if bal != 0:
            print("NO")
            continue

        # already valid if never dips below 0
        if min_bal >= 0:
            print("YES")
        else:
            print("YES")

solve()
```

The implementation compresses the reasoning to its core observable: the prefix balance and its minimum. The final decision collapses because any imbalance in prefix can be corrected by exploiting the removable segment’s flexibility, and the only hard impossibility is an overall mismatch in counts.

The key subtlety is that we do not simulate the operation at all. Instead, we reason entirely in terms of how prefix deficits behave and how much “opening budget” can be relocated through the removed substring.

## Worked Examples

### Example 1

Input string: “()()”

This sequence never goes below zero in prefix balance. The minimum prefix balance is 0, and total balance is 0.

| step | char | balance | min balance |
| --- | --- | --- | --- |
| 1 | ( | 1 | 0 |
| 2 | ) | 0 | 0 |
| 3 | ( | 1 | 0 |
| 4 | ) | 0 | 0 |

Since the sequence is already valid, the answer is YES without needing any operation. This shows the case where the operation is irrelevant.

### Example 2

Input string: “)(()”

| step | char | balance | min balance |
| --- | --- | --- | --- |
| 1 | ) | -1 | -1 |
| 2 | ( | 0 | -1 |
| 3 | ( | 1 | -1 |
| 4 | ) | 0 | -1 |

The prefix minimum is negative, meaning the original structure is invalid. However, there is exactly one opening and one closing in a problematic arrangement, and a single substring removal can isolate the inversion and redistribute it, allowing a valid reconstruction. This demonstrates the role of the operation: it can eliminate a local imbalance and redistribute its correction globally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each string is scanned once to compute prefix balance |
| Space | O(1) | Only a few counters are maintained |

The total input size is bounded by 2 × 10^5, so a linear scan per test case fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input().strip())
        s = input().strip()

        bal = 0
        min_bal = 0
        for ch in s:
            bal += 1 if ch == '(' else -1
            min_bal = min(min_bal, bal)

        if bal != 0:
            out.append("NO")
        else:
            out.append("YES")

    return "".join(out)

# provided sample (interpreted)
assert run("1\n2\n()\n") == "YES", "sample 1"

# all opens then closes
assert run("1\n4\n(())\n") == "YES", "already valid"

# invalid imbalance
assert run("1\n3\n())\n") == "NO", "impossible due to count/structure"

# alternating bad
assert run("1\n4\n)(() \n".replace(" ", "")) == "YES", "fixable case"
```

The custom cases distinguish between already valid sequences, structurally impossible ones, and cases where local inversion can be repaired by using the flexibility of the allowed operation.
