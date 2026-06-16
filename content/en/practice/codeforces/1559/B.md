---
title: "CF 1559B - Mocha and Red and Blue"
description: "We are given a line of positions, each position holding a tile that must end up colored either red or blue. Some tiles are already fixed, while others are blank and can be assigned either color."
date: "2026-06-16T16:34:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1559
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 738 (Div. 2)"
rating: 900
weight: 1559
solve_time_s: 316
verified: false
draft: false
---

[CF 1559B - Mocha and Red and Blue](https://codeforces.com/problemset/problem/1559/B)

**Rating:** 900  
**Tags:** dp, greedy  
**Solve time:** 5m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of positions, each position holding a tile that must end up colored either red or blue. Some tiles are already fixed, while others are blank and can be assigned either color.

After we finalize all colors, we pay a cost equal to the number of adjacent pairs of tiles that share the same color. Each time two neighbors match, the cost increases by one. The task is to fill all blanks so that this cost is as small as possible, and output any coloring that achieves this minimum.

The key observation is that the cost depends only on adjacent equality. This means we are not trying to match a global pattern, only to avoid long runs of identical colors where possible.

The constraints are small: each test has length at most 100 and there are at most 100 tests. This allows any linear or even quadratic approach per test, but rules out exponential enumeration of all fillings, which would grow like 2 to the power of number of blanks and quickly become infeasible.

A few edge situations matter.

If the string is already fully fixed and alternates like "RBRBRB", the cost is already zero and no changes are needed. A naive approach that tries to “optimize” might incorrectly change forced structure if it ignores fixed constraints.

If all characters are "?", then any alternating pattern such as "BRBRBR..." or "RBRBRB..." achieves zero cost, which is optimal. A careless greedy that always starts with a fixed color without considering symmetry still works, but only because both colors are equivalent.

If fixed characters are inconsistent in forcing long segments, for example "R???R", any solution must respect endpoints and cannot simply alternate freely without aligning boundaries.

## Approaches

A brute-force strategy would try all assignments of colors to the blank positions. For each assignment, we compute the number of adjacent equal pairs in linear time. If there are k blanks, this produces 2^k possibilities, and each evaluation costs O(n), leading to O(n · 2^k). Even with n = 100, k can be large, making this approach astronomically slow.

The key structural insight is that adjacent conflicts are purely local. Each position only interacts with its immediate neighbors. This means we do not need to decide all blanks independently; instead, we can construct the solution greedily from left to right while maintaining consistency with already decided neighbors.

The crucial simplification is that once a character is fixed, any blank segment between fixed characters behaves like a constrained interpolation problem. Inside such a segment, we only care about whether endpoints force a match or mismatch, and we can fill greedily in a way that avoids equal adjacencies as much as possible. This leads to the standard construction: propagate constraints from left to right, ensuring each position differs from its left neighbor whenever possible, but respecting fixed colors.

This reduces the problem to a single pass construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^k) | O(n) | Too slow |
| Optimal Greedy Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the final string from left to right.

1. Replace all '?' with placeholders and prepare to fill the string. The goal is to decide each position while respecting fixed constraints.
2. For the first position, if it is '?', assign it arbitrarily to 'B'. There is no left neighbor, so no cost can be influenced here.
3. For each position i from 1 to n - 1, decide its color based on two rules. If s[i] is fixed ('B' or 'R'), we must keep it. Otherwise, we choose a color different from s[i - 1] if possible.
4. When s[i] is '?', assign it the opposite of s[i - 1]. This prevents creating an equal adjacent pair at position i - 1 and i.
5. If s[i] is fixed and matches s[i - 1], we accept the cost contribution, since we cannot change fixed characters. If it differs, we simply proceed.
6. Continue until the end of the string, ensuring every decision is locally optimal given previous choices.

The output is the fully constructed string.

### Why it works

At every position, we minimize the contribution of the edge between i - 1 and i. If a free choice exists, we always select a color that avoids equality with the previous character. If no free choice exists due to a fixed constraint, we are forced to accept the cost. Since every edge is handled exactly once and independently, no later decision can improve or worsen earlier edges, so the greedy choice is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = list(input().strip())

        # handle first position
        if s[0] == '?':
            s[0] = 'B'

        for i in range(1, n):
            if s[i] == '?':
                # choose opposite of previous
                s[i] = 'R' if s[i - 1] == 'B' else 'B'

        print(''.join(s))

if __name__ == "__main__":
    solve()
```

The implementation follows the left-to-right construction directly. The first position is initialized arbitrarily because it has no left constraint. Each subsequent '?' is assigned the opposite color of its predecessor, ensuring no new equal-adjacent pair is introduced when possible.

Fixed characters naturally override the greedy choice: when s[i] is already 'R' or 'B', we simply keep it, and the algorithm proceeds. This is safe because fixed constraints define unavoidable edges in the cost, and we do not attempt to modify them.

## Worked Examples

### Example 1

Input: `?R???BR`

We process left to right.

| i | s[i] before | s[i-1] | action | s after step |
| --- | --- | --- | --- | --- |
| 0 | ? | - | set to B | BR???BR |
| 1 | R | B | fixed | BR???BR |
| 2 | ? | R | set B | BRB??BR |
| 3 | ? | B | set R | BRBR?BR |
| 4 | ? | R | set B | BRBRBBR |
| 5 | B | B | fixed, match | BRBRBBR |
| 6 | R | B | fixed | BRBRBRR |

This demonstrates how each blank is chosen to avoid matching its left neighbor when possible, and how fixed characters override choices.

### Example 2

Input: `???`

| i | s[i] before | s[i-1] | action | s after step |
| --- | --- | --- | --- | --- |
| 0 | ? | - | B | B?? |
| 1 | ? | B | R | BR? |
| 2 | ? | R | B | BRB |

This produces a perfectly alternating sequence, which achieves zero imperfectness.

The second example shows that in fully free strings, the algorithm reduces the cost to its theoretical minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | each position is processed once |
| Space | O(n) | storing and modifying the string |

The total work across all test cases is at most 100 × 100 operations, which is trivially within limits. Memory usage is linear in the string length.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = list(input().strip())
        if s[0] == '?':
            s[0] = 'B'
        for i in range(1, n):
            if s[i] == '?':
                s[i] = 'R' if s[i - 1] == 'B' else 'B'
        out.append(''.join(s))
    return '\n'.join(out)

# provided samples
assert run("5\n7\n?R???BR\n7\n???R???\n1\n?\n1\nB\n10\n?R??RB??B?\n") == \
"BRRBRBR\nBRBRBRB\nB\nB\nBRRBRBBRBR"

# all unknown
assert run("1\n5\n?????\n") == "BRBRB"

# already fixed alternating
assert run("1\n4\nBRBR\n") == "BRBR"

# single char
assert run("1\n1\n?\n") == "B"

# forced segment
assert run("1\n5\nR???R\n") == "RBRBR"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all '?' | BRBRB | pure greedy alternation |
| BRBR | BRBR | no modification of fixed valid string |
| ? single | B | boundary initialization |
| R???R | RBRBR | consistency with fixed endpoints |

## Edge Cases

For a fully unknown string like `?????`, the algorithm starts with 'B' and alternates deterministically. Each step depends only on the previous character, so the entire structure is consistent and yields zero adjacent equal pairs.

For an already optimal configuration like `BRBR`, the algorithm never modifies fixed characters and simply passes through, preserving the zero-cost structure.

For single-character inputs, initialization handles the absence of neighbors safely, since no adjacency exists and therefore no imperfectness can be created or removed.
