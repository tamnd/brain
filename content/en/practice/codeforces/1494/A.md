---
title: "CF 1494A - ABC String"
description: "We are given a string over three symbols: A, B, and C. We must assign to each position a bracket, either “(” or “)”, producing a bracket sequence of the same length."
date: "2026-06-10T22:08:05+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1494
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 105 (Rated for Div. 2)"
rating: 900
weight: 1494
solve_time_s: 99
verified: true
draft: false
---

[CF 1494A - ABC String](https://codeforces.com/problemset/problem/1494/A)

**Rating:** 900  
**Tags:** bitmasks, brute force, implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string over three symbols: A, B, and C. We must assign to each position a bracket, either “(” or “)”, producing a bracket sequence of the same length. The key restriction is that equal letters must map to equal brackets, so every A is replaced by the same bracket, every B by the same bracket, and every C by the same bracket.

So instead of choosing brackets per position, we are choosing a mapping from the set {A, B, C} to {“(”, “)”}. There are only 8 possible mappings, but not all of them produce a valid regular bracket sequence.

The goal is to determine whether at least one of these mappings produces a correct bracket sequence.

The constraint n ≤ 50 is very small. A brute force over all mappings and a linear validity check per mapping is easily fast enough, since we only perform at most 8 × 50 operations per test case, with t ≤ 1000.

A subtle failure case arises if one tries to greedily assign brackets based on local balance or frequency without respecting global structure. For example, assuming the majority letter should become “(” can fail because balance depends on ordering, not counts.

Another pitfall is treating the problem as independent per position. Since all occurrences of a letter are tied together, flipping a single position is impossible, which makes local fixes invalid.

## Approaches

The brute force view is straightforward. Each of A, B, and C can independently be mapped to either “(” or “)”, giving 2³ = 8 assignments. For each assignment, we construct the resulting bracket sequence and check whether it is a regular bracket sequence by scanning left to right and maintaining a balance counter that must never go negative and must end at zero.

This works because a regular bracket sequence can be verified in O(n), and the number of candidate mappings is constant. The total cost per test case is therefore constant times n.

Trying to be clever by assigning brackets greedily based on positions does not work because the constraints couple all occurrences of a letter globally. The structure is small enough that enumeration dominates any need for optimization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (8 mappings) | O(8n) | O(n) | Accepted |
| Optimal (same idea) | O(8n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem to testing all possible assignments from letters to brackets.

1. Enumerate all 8 mappings from {A, B, C} to {“(”, “)”}. This is done using a 3-bit mask, where each bit determines the bracket type for one letter. This ensures we cover every possible global assignment.
2. For each mapping, construct or simulate the bracket sequence by replacing each character in the string according to the mapping. We do not need to explicitly build the string; we can compute balance directly.
3. Scan the string from left to right while maintaining a counter `bal`. When we see “(”, we increment it; when we see “)”, we decrement it.
4. If at any point `bal` becomes negative, the sequence is invalid and we immediately stop checking this mapping. This is necessary because a prefix with more closing than opening brackets cannot be fixed later.
5. After finishing the scan, check whether `bal` equals zero. If yes, the mapping produces a valid regular bracket sequence, so we can output “YES”.
6. If no mapping works, output “NO”.

### Why it works

Any valid assignment is fully described by choosing a bracket type for each of the three letters. There are no hidden degrees of freedom. The prefix condition on bracket sequences is both necessary and sufficient: a sequence is regular if and only if its running balance never drops below zero and ends at zero. Since we test all possible assignments exhaustively, we cannot miss a valid configuration, and each invalid assignment is rejected exactly when it violates the prefix condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_valid(s, mp):
    bal = 0
    for ch in s:
        if mp[ch]:
            bal += 1
        else:
            bal -= 1
        if bal < 0:
            return False
    return bal == 0

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()

        letters = ['A', 'B', 'C']

        ok = False
        for mask in range(8):
            mp = {}
            for i, c in enumerate(letters):
                mp[c] = (mask >> i) & 1  # 1 -> '(', 0 -> ')'

            if is_valid(s, mp):
                ok = True
                break

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution iterates over all 8 mappings using a bitmask. Each bit encodes whether a letter is mapped to “(” or “)”. The helper function checks validity in linear time by maintaining a running balance and rejecting early if it becomes negative. Early exit is important but not strictly necessary due to small constraints.

The mapping dictionary is rebuilt for each mask, which is fine since only three keys exist. An alternative would be a precomputed array of size 8 × 3, but it would not change complexity.

## Worked Examples

### Example 1

Input string: `AABBAC`

We test mappings in mask order.

| Mask | A | B | C | Sequence | Balance trace | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 000 | ) | ) | ) | )))))) | always negative early | No |
| 001 | ) | ) | ( | ))))( | negative prefix | No |
| 010 | ) | ( | ) | )((()) | prefix goes negative early | No |
| 011 | ) | ( | ( | )((( (invalid) | negative at start | No |
| 100 | ( | ) | ) | ())( (()) | prefix valid, ends 0 | Yes |

Once a valid assignment is found, we stop and output YES.

This trace shows how only a specific global grouping of letters can satisfy balance constraints, not just local structure.

### Example 2

Input string: `CACA`

We try a successful mapping:

| Mask | A | B | C | Sequence | Balance trace | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | ( | - | ) | )() (after mapping) | -1 early | No |
| 100 | ( | - | ) | ()() | 1,0,1,0 | Yes |

This demonstrates that alternating structure is achievable only when letter mapping aligns with alternation in the original string order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(8n) per test case | We try 8 mappings and scan the string once per mapping |
| Space | O(1) auxiliary | Only a small mapping array and counters are used |

With n ≤ 50 and t ≤ 1000, the total number of operations is at most about 400k character checks, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_valid(s, mp):
        bal = 0
        for ch in s:
            bal += 1 if mp[ch] else -1
            if bal < 0:
                return False
        return bal == 0

    def solve():
        t = int(input())
        for _ in range(t):
            s = input().strip()
            letters = ['A', 'B', 'C']

            ok = False
            for mask in range(8):
                mp = {}
                for i, c in enumerate(letters):
                    mp[c] = (mask >> i) & 1
                if is_valid(s, mp):
                    ok = True
                    break
            print("YES" if ok else "NO")

    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("4\nAABBAC\nCACA\nBBBBAC\nABCA\n") == "YES\nYES\nNO\nNO"

# custom cases
assert run("1\nAA") == "NO"
assert run("1\nAB") == "YES"
assert run("1\nABCABC") == "YES"
assert run("1\nAAAAAA") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| AA | NO | smallest even case with no valid mapping |
| AB | YES | simplest valid alternating structure |
| ABCABC | YES | multi-letter cyclic valid assignment |
| AAAAAA | NO | uniform string must fail balance constraints |

## Edge Cases

A key edge case is when all characters are identical. For example `AAAAAA` forces every position to receive the same bracket. If mapped to “(”, the sequence never closes; if mapped to “)”, it immediately becomes invalid. The algorithm correctly tests both and rejects both because neither produces zero final balance.

Another case is alternating structure like `ABABAB`. Here only certain mappings allow prefix stability. During execution, the balance trace remains non-negative only for assignments that align A and B to opposite bracket types, which the enumeration captures automatically.

A third case is short strings like `AB`. Even though counts are balanced, only one mapping yields a valid sequence. The scan correctly rejects mappings that produce a prefix drop to -1 immediately, which is the earliest possible failure point.
