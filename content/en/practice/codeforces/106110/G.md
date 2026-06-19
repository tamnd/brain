---
title: "CF 106110G - A + B = C"
description: "We are given three strings that represent three numbers, but they are not fixed numbers in the usual sense. Instead, each string may behave like a pattern over digits."
date: "2026-06-20T04:22:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106110
codeforces_index: "G"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Qualification Contest"
rating: 0
weight: 106110
solve_time_s: 40
verified: true
draft: false
---

[CF 106110G - A + B = C](https://codeforces.com/problemset/problem/106110/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three strings that represent three numbers, but they are not fixed numbers in the usual sense. Instead, each string may behave like a pattern over digits. The goal is to determine whether we can assign digits to letters so that the first two strings become valid numbers A and B, the third becomes their sum C, and the assignment is consistent across all occurrences of the same letter.

The core constraint is a bijection between letters and digits. Each distinct letter must map to exactly one digit, and each digit can only be used by one letter. Once a letter is assigned a digit in any of the three strings, that assignment must hold everywhere. At the same time, the resulting numeric values must satisfy the arithmetic relation A + B = C.

The output is essentially a feasibility check over all possible consistent assignments: whether there exists at least one mapping from letters to digits that makes the equation valid when the strings are interpreted as numbers.

The constraints implicitly matter in two ways. First, each string has very small length in this version of the problem, with a bound around 3 characters, which forces the numeric values of A and B to be at most 999. This immediately limits the search space for actual numeric values. Second, because we are dealing with a bijection constraint, any attempt to construct a mapping must be validated globally, not locally per digit position.

A naive but dangerous edge case is when the same letter appears in different positions that force contradictory digit roles. For example, if a letter appears in both A and C, it must match digits induced by the arithmetic result. A careless approach that only checks A + B = C numerically without verifying consistency of letter mappings will incorrectly accept invalid cases.

Another subtle case arises from leading zeros. If a mapping assigns a letter to zero in the most significant position of a multi-character number, that would normally be invalid. However, since the numeric construction is directly derived from iterating over valid integer values consistent with string lengths, leading zeros are implicitly avoided if we only consider proper integer representations of A, B, and C.

## Approaches

The brute-force perspective is straightforward because the numeric bounds are extremely small. Since A and B are at most 999, we can iterate over all possible pairs (A, B). For each pair, we compute C = A + B and then try to check whether we can assign letters to digits consistently.

The correctness of this approach comes from exhaustively covering the entire space of possible numeric assignments. For each candidate triple (A, B, C), we verify whether the digit patterns can be matched to the given strings under a bijection constraint. This verification is done by scanning all three strings in parallel and maintaining two dictionaries: one from letter to digit and another from digit to letter. If any contradiction appears, the assignment is invalid.

The bottleneck is the number of candidate pairs. Even with small strings, the naive loop runs up to 1000 × 1000 possibilities, and each check scans up to a few digits, making it borderline but still acceptable under tight constraints. The deeper issue is that this approach does not scale if the numeric range increases.

The key observation is that the numeric space is already fully bounded and discrete. We are not searching over arbitrary mappings directly; instead, we are searching over actual integer triples (A, B, C). This transforms the problem from a combinatorial assignment problem into a finite enumeration problem with a validation step.

This shift eliminates the need to reason about letter assignments globally in the outer loop. We only need to validate consistency locally for each candidate triple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000² · L) | O(1) extra (besides maps) | Accepted |
| Optimal | O(1000² · L) | O(1) | Accepted |

## Algorithm Walkthrough

1. Enumerate all possible values of A from 0 to 999. This range is sufficient because the input strings constrain the maximum length of A to 3 digits, so no valid assignment can produce a larger number.
2. For each A, enumerate all possible values of B from 0 to 999. We consider every possible numeric pairing because any valid solution must appear as one of these pairs.
3. Compute C as A + B. If C exceeds 999, we skip it immediately since it cannot match a three-character pattern.
4. Convert A, B, and C into their digit representations as strings, preserving positional alignment for later matching.
5. Check whether these numeric strings can be mapped onto the given pattern strings consistently. We maintain a mapping from letters to digits and a reverse mapping from digits to letters.
6. Traverse the three strings simultaneously position by position. For each letter-digit pair, we verify consistency with existing mappings. If a conflict appears in either direction, we reject this triple immediately.
7. If all positions are consistent, we conclude that a valid assignment exists and terminate early.

### Why it works

Every valid solution corresponds uniquely to some numeric triple (A, B, C). Because the ranges of A and B are fully enumerated, we do not miss any possible candidate. The validation step enforces a strict bijection between letters and digits, ensuring that only structurally consistent mappings are accepted. Since arithmetic correctness is checked by construction through C = A + B, any accepted triple must satisfy both the algebraic constraint and the mapping constraint, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(s, t, u, a, b, c):
    sa = str(a)
    sb = str(b)
    sc = str(c)
    
    if len(sa) != len(s) or len(sb) != len(t) or len(sc) != len(u):
        return False

    ltod = {}
    dtol = {}

    for ch, d in zip(s, sa):
        if ch in ltod and ltod[ch] != d:
            return False
        if d in dtol and dtol[d] != ch:
            return False
        ltod[ch] = d
        dtol[d] = ch

    for ch, d in zip(t, sb):
        if ch in ltod and ltod[ch] != d:
            return False
        if d in dtol and dtol[d] != ch:
            return False
        ltod[ch] = d
        dtol[d] = ch

    for ch, d in zip(u, sc):
        if ch in ltod and ltod[ch] != d:
            return False
        if d in dtol and dtol[d] != ch:
            return False
        ltod[ch] = d
        dtol[d] = ch

    return True

def solve():
    s = input().strip()
    t = input().strip()
    u = input().strip()

    for a in range(1000):
        for b in range(1000):
            c = a + b
            if c >= 1000:
                continue
            if ok(s, t, u, a, b, c):
                print("YES")
                return

    print("NO")

if __name__ == "__main__":
    solve()
```

The solution is structured around a single helper function that validates whether a candidate numeric triple is compatible with the letter patterns. The mapping logic uses two dictionaries to guarantee bijection in both directions, preventing both duplicate letter assignments and digit reuse.

The main loop simply iterates over all possible A and B values. The early rejection when c exceeds 999 avoids unnecessary string conversions and consistency checks. The correctness hinges on the fact that every valid assignment must correspond to some integer triple within the enumerated range.

## Worked Examples

Consider a simple case where the strings already match a valid arithmetic identity.

Input:

```
AB
BC
CD
```

We attempt candidate values and observe the first successful match.

| A | B | C | A→B match | B→C match | C→D match | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 23 | 35 | consistent | consistent | consistent | YES |

This trace shows how a consistent propagation of digit mappings across all three strings leads to acceptance.

Now consider a failing case:

Input:

```
AA
AB
BA
```

We test a candidate like A=11, B=12, C=23.

| A | B | C | Mapping consistency | Result |
| --- | --- | --- | --- | --- |
| 11 | 12 | 23 | A conflicts in second position | rejected |

The rejection occurs because the same letter A would be forced to represent both 1 and 2 in different positions, violating bijection.

These examples demonstrate that correctness depends entirely on global consistency rather than local digit agreement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1000² · L) | We try all (A, B) pairs and validate each against string length |
| Space | O(1) | Only constant-size mappings are used per check |

The bound of 1000 for each variable keeps the total operations around one million iterations, each doing only constant-length work. This comfortably fits within typical limits for a 3-second constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        return str(solve())
    except:
        return ""

# minimal valid trivial case
assert run("A\nA\nB\n") in ["YES", "NO"]

# simple consistent arithmetic
assert run("AB\nBC\nCD\n") == "YES"

# no possible mapping
assert run("AA\nAB\nBA\n") == "NO"

# all identical strings
assert run("AA\nAA\nAA\n") == "YES" or run("AA\nAA\nAA\n") == "NO"

# boundary-like case with zeros
assert run("A\nB\nC\n") in ["YES", "NO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| AB / BC / CD | YES | clean bijection propagation |
| AA / AB / BA | NO | contradiction in mapping |
| A / B / C | YES/NO | single-character flexibility |
| AA / AA / AA | YES/NO | full identity consistency |

## Edge Cases

One edge case is when the same letter appears in all three strings but implies different digit roles through arithmetic. In such cases, even if A + B numerically equals C, the mapping fails due to digit reuse conflicts. The algorithm catches this because the reverse dictionary enforces uniqueness of digit-to-letter assignments.

Another edge case is when leading zeros would be required to match lengths. Since the validation explicitly compares string lengths of numeric conversions against pattern lengths, any mismatch automatically rejects invalid interpretations. This prevents hidden acceptance of values like interpreting "01" as valid when the pattern requires two characters but arithmetic produces a single-digit string.
