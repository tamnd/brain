---
title: "CF 106068A - Correct Brackets"
description: "We are given a string made only of opening and closing parentheses. The only allowed operation is to take a closing parenthesis from some position and reinsert it anywhere to its left. Opening parentheses are fixed in place."
date: "2026-06-21T09:21:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106068
codeforces_index: "A"
codeforces_contest_name: "2025 Aleppo and Idlib Private Universities Collegiate Programming Contest (APUCPC 2025)"
rating: 0
weight: 106068
solve_time_s: 49
verified: true
draft: false
---

[CF 106068A - Correct Brackets](https://codeforces.com/problemset/problem/106068/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of opening and closing parentheses. The only allowed operation is to take a closing parenthesis from some position and reinsert it anywhere to its left. Opening parentheses are fixed in place.

The goal is to determine whether, after any number of such moves, we can transform the sequence into a well-formed bracket sequence, meaning it can represent a valid arithmetic expression if we insert `+` and `1` between characters.

The important consequence of the allowed operation is that closing brackets are fully reorderable as long as they do not move to the right. In other words, all `')'` characters can be permuted arbitrarily, but only in a way that they shift leftward relative to their original positions. Opening brackets cannot be moved.

The input size goes up to 200,000 characters. Any quadratic or even near-quadratic approach over substrings or repeated simulations is too slow. A linear scan or linear scan with constant extra state is necessary.

A subtle edge case appears when the string starts with many closing brackets. For example, `"))(("` cannot be fixed because no operation can move a closing bracket past an opening bracket to the right, and prefix validity is fundamentally broken at the start. Another edge case is when the number of closing brackets is insufficiently “distributable” to match opens in prefix order even though counts match globally.

## Approaches

A brute-force interpretation would simulate all possible ways of moving closing brackets. Each operation selects a `')'` and inserts it earlier, so in theory we could try to generate all permutations of closing brackets under the constraint that they cannot move right. This leads to a state space that is exponential in the number of closing brackets. Even attempting greedy local fixes would still require repeated scans and updates, leading to quadratic behavior in the worst case.

The key observation is that the operation removes any positional restriction on closing brackets except that they cannot cross to the right. This effectively means we are allowed to rearrange all `')'` characters freely among themselves, as long as the multiset of positions they occupy respects that they stay somewhere not to the right of their original occurrences. Since we are only asked whether a correct bracket sequence can be formed, the only real question is whether we can assign enough closing brackets early enough to satisfy prefix balance.

A correct bracket sequence condition reduces to the classic prefix rule: every prefix must have at least as many `'('` as `')'`, and total counts must match.

Since we can effectively “shift” closing brackets left, the only obstruction comes from prefixes that contain too many closing brackets compared to openings available anywhere to supply them early. The structure collapses into checking whether the sequence can be rearranged into a valid Dyck word given that we cannot move `'('`.

This leads to a greedy check: simulate reading the string, track available openings, and ensure we never need more closings than can be supplied from the total remaining suffix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rearrangements | Exponential | O(n) | Too slow |
| Greedy prefix feasibility check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We convert the problem into a feasibility check on prefix balances under constrained movement of closing brackets.

1. Count total number of `'('` and `')'`. If they are not equal, return "No". A correct bracket sequence requires equal numbers, and no operation changes counts.
2. Iterate through the string from left to right while maintaining how many opening brackets we have seen so far. This represents how many unmatched `'('` are potentially available to support future closing brackets.
3. Maintain a counter for how many closing brackets we have already "fixed" into valid positions. Instead of thinking about actual movement, we treat this as ensuring that at every prefix, the number of required closing brackets does not exceed what could be supplied.
4. At each position, compute the minimum number of unmatched opens we must preserve to keep future validity. If at any point we would be forced into a situation where a prefix has more required `')'` than available `'('`, we conclude impossibility.
5. Since closing brackets can be shifted left, any deficit in a prefix cannot be repaired if there are not enough openings in total suffix positions to compensate. The greedy scan ensures we never overcommit openings too early.

### Why it works

The invariant is that after processing a prefix, the number of available `'('` is exactly the number of opens seen minus the number of closings we have logically matched so far. Because we can only move `')'` left, any valid construction must respect that no prefix ever demands more closings than there exist opens in the entire string up to that point. If a prefix violates this, no rearrangement can fix it, since we cannot introduce new `'('` earlier or move them rightward.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)
    
    open_cnt = s.count('(')
    close_cnt = n - open_cnt
    
    if open_cnt != close_cnt:
        print("No")
        return
    
    balance = 0
    for ch in s:
        if ch == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    solve()
```

The solution first checks global feasibility via counts, since any valid bracket sequence must have equal numbers of opening and closing parentheses. Then it performs a standard prefix balance scan. The key idea is that despite the allowed operation, we still cannot fix a prefix where closings exceed openings because no operation can create earlier openings or move openings to the right. The prefix simulation captures exactly this obstruction.

A subtle point is that we do not simulate the allowed reinsertions explicitly. That operation only affects the relative order of closing brackets, but it does not change the fundamental prefix constraint imposed by openings, so the classic validity check remains sufficient.

## Worked Examples

### Example 1: `((()))`

| i | char | balance |
| --- | --- | --- |
| 1 | ( | 1 |
| 2 | ( | 2 |
| 3 | ( | 3 |
| 4 | ) | 2 |
| 5 | ) | 1 |
| 6 | ) | 0 |

This shows a fully valid prefix evolution where balance never drops below zero and ends at zero. It confirms that no rearrangement is needed when the sequence is already correct.

### Example 2: `())(()`

| i | char | balance |
| --- | --- | --- |
| 1 | ( | 1 |
| 2 | ) | 0 |
| 3 | ) | -1 (fail) |

At position 3 the prefix becomes invalid because a closing bracket appears when no unmatched opening exists. Even though later opens exist, they cannot be moved left, so the prefix violation is permanent.

This demonstrates that the algorithm correctly rejects cases where early structure is unsalvageable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the string with constant work per character |
| Space | O(1) | Only counters are maintained |

The constraints allow up to 200,000 characters, so a linear scan is comfortably within limits, and no auxiliary structures proportional to input size are needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        s = sys.stdin.readline().strip()
        n = len(s)
        
        if s.count('(') != n - s.count('('):
            return "No"
        
        bal = 0
        for c in s:
            if c == '(':
                bal += 1
            else:
                bal -= 1
            if bal < 0:
                return "No"
        return "Yes"
    
    return solve()

# provided sample
assert run("((()))\n") == "Yes"

# minimum size
assert run("()\n") == "Yes"

# impossible due to prefix
assert run("())\n") == "No"

# all closing
assert run("))))((\n") == "No"

# already balanced but tricky order
assert run("()()()\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | Yes | Minimum valid case |
| `())` | No | Early prefix failure |
| `))))((` | No | Global imbalance + ordering constraint |
| `()()()` | Yes | Multiple independent valid segments |

## Edge Cases

A critical edge case is when the string is globally balanced but has an early prefix violation, such as `")(()"`. The algorithm processes it as follows: at the first character, balance becomes `-1`, triggering immediate rejection. This matches the fact that no allowed operation can move an opening bracket before position 1, so the prefix cannot be repaired.

Another case is `"()())("`, where total counts are equal but a prefix still breaks at the fifth character. The scan reaches balance `-1` at that point, and the algorithm rejects. Even though there is an extra opening later, it cannot be moved left enough to fix the deficit at the prefix boundary.

A final edge case is already correct sequences like `"((()))"`. The balance never drops below zero, and the algorithm accepts without needing to consider the reordering operation, reflecting that the operation is only relevant when rearrangement might be needed but does not expand the class of feasible prefix-valid strings.
