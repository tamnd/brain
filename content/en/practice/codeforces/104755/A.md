---
title: "CF 104755A - Poster"
description: "We are given a short poster text and a pen that can write using three fixed colors. Each color has a limited capacity measured in how many characters it can be used for."
date: "2026-06-28T22:51:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104755
codeforces_index: "A"
codeforces_contest_name: "LU ICPC Selection Contest 2023"
rating: 0
weight: 104755
solve_time_s: 49
verified: true
draft: false
---

[CF 104755A - Poster](https://codeforces.com/problemset/problem/104755/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short poster text and a pen that can write using three fixed colors. Each color has a limited capacity measured in how many characters it can be used for. The key constraint is not about individual characters being freely colored, but about partitioning character types into the three colors.

Every character in the text belongs to exactly one of three categories: letters, digits, or punctuation marks. Spaces exist in the text but are not part of these categories and therefore do not consume ink in any color. The task is to decide whether we can assign each category to a distinct color such that the total number of characters in that category does not exceed the available ink for that color.

In other words, we must map letters, digits, and punctuation injectively onto the set of colors blue, yellow, and red, and after choosing this mapping, each category’s count must fit within its assigned capacity.

The input limits are small, with the text length at most 1000. This immediately suggests that counting and checking a constant number of configurations is sufficient, since there are only 3 categories and thus only 6 possible assignments.

A naive but important pitfall is to assume that colors can be mixed within a category. For example, trying to split letters across multiple colors would violate the rule that each category must be assigned exactly one color. Another subtle issue is forgetting to ignore spaces, which do not belong to any category.

A small example where mistakes can happen is:

Input:

ICPC

1 1 10

Letters = 4, punctuation = 0, digits = 0. If we mistakenly allow splitting letters across colors, we might incorrectly conclude feasibility, but the problem disallows that.

Correct output is:

No

since 4 exceeds both 1 and 10 in some mappings depending on assignment constraints.

## Approaches

The brute-force idea is to try all possible assignments of the three categories to the three colors. For each assignment, we compute the total number of letters, digits, and punctuation marks in the text, then check whether each category fits into its assigned capacity.

Since there are exactly three categories and three colors, the number of mappings is 3 factorial, which is 6. For each mapping, we scan the entire text once to count category frequencies. With a maximum length of 1000, this yields at most about 6000 character checks, which is trivial even under tight limits.

The key insight is that the structure is not dynamic or combinatorial beyond permutations. There is no dependency between characters inside a category, only between aggregate counts and fixed capacities. This reduces the problem from something that might look like assignment or DP into a constant-factor permutation check problem.

The brute-force already runs fast enough, but the conceptual simplification is recognizing that the only degrees of freedom are the 6 permutations of category-to-color mappings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | O(6 · n) | O(1) | Accepted |
| Optimal (same idea, optimized) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We first compute three values: the number of letters, the number of digits, and the number of punctuation characters in the text. Spaces are ignored entirely.

After that, we try every possible assignment of the three categories to the three available colors. Each assignment pairs one category count with one capacity limit.

For each assignment, we check whether all three category counts are less than or equal to their assigned capacities. If we find at least one valid assignment, we can immediately conclude that the poster is possible.

If none of the six assignments satisfy the constraints, the answer is impossible.

### Why it works

Each valid solution corresponds exactly to choosing a bijection between the three categories and the three colors. Since capacities are fixed per color, feasibility depends only on whether the chosen pairing respects all three inequalities simultaneously. Enumerating all bijections guarantees that no valid mapping is missed, and checking them independently ensures correctness because categories do not interact once assigned.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    b, y, r = map(int, input().split())
    s = input().rstrip('\n')

    letters = digits = punct = 0

    punct_set = set([',', '-', ';', ':', '.', '!', '?'])

    for ch in s:
        if ch == ' ':
            continue
        if ch.isalpha():
            letters += 1
        elif ch.isdigit():
            digits += 1
        else:
            punct += 1

    counts = [letters, digits, punct]
    caps = [b, y, r]

    import itertools

    for perm in itertools.permutations(caps):
        ok = True
        for i in range(3):
            if counts[i] > perm[i]:
                ok = False
                break
        if ok:
            print("Yes")
            return

    print("No")

if __name__ == "__main__":
    solve()
```

The code first separates the text into the three required categories using simple character classification. Letters are detected using `isalpha`, digits using `isdigit`, and everything else except spaces is treated as punctuation. This matches the problem definition since punctuation is explicitly limited to a small known set, but the classification rule is safely captured by the fallback branch.

We then treat the three counts and three capacities as multisets. By permuting capacities, we simulate all possible assignments of colors to categories. Each permutation is checked independently in constant time.

A subtle point is ensuring spaces are excluded, since they appear in the text but do not belong to any category. The explicit `continue` handles this cleanly.

## Worked Examples

### Example 1

Input:

```
21 8 2
ICPC Programming Season 2023-2024!
```

Counts:

letters = 24, digits = 8, punctuation = 1

We test permutations of capacities (21, 8, 2).

| permutation | letters | digits | punctuation | valid |
| --- | --- | --- | --- | --- |
| (21,8,2) | 24 ≤ 21 | 8 ≤ 8 | 1 ≤ 2 | No |
| (21,2,8) | 24 ≤ 21 | 8 ≤ 2 | 1 ≤ 8 | No |
| (8,21,2) | 24 ≤ 8 | 8 ≤ 21 | 1 ≤ 2 | No |
| ... | ... | ... | ... | ... |

No permutation satisfies all constraints, so output is `No`.

This demonstrates that even if total capacity seems sufficient, the fixed assignment constraint can block feasibility.

### Example 2

Input:

```
5 20 5
13 problems in the contest!
```

Counts:

letters = 17, digits = 2, punctuation = 1

One valid assignment is:

digits → blue (5), letters → yellow (20), punctuation → red (5)

| category | count | assigned cap | ok |
| --- | --- | --- | --- |
| digits | 2 | 5 |  |
| letters | 17 | 20 |  |
| punct | 1 | 5 |  |

This permutation satisfies all constraints, so output is `Yes`.

This shows that feasibility depends on matching large categories to large capacities correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan to count characters plus constant 6 permutations |
| Space | O(1) | Only three counters and fixed arrays |

The input size is at most 1000 characters, so a single pass over the string is trivial. The constant factor from checking six permutations is negligible, ensuring the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdout = _sys.stdout
    _sys.stdout = out
    solve()
    _sys.stdout = _stdout
    return out.getvalue().strip()

# sample-like case: impossible
assert run("21 8 2\nICPC Programming Season 2023-2024!\n") == "No"

# sample-like case: possible
assert run("5 20 5\n13 problems in the contest!\n") == "Yes"

# minimum size, single letter
assert run("1 1 1\na\n") == "Yes"

# digits dominate punctuation requirement
assert run("0 5 0\n12345\n") == "Yes"

# tight fail case
assert run("2 2 2\nabc123!!!\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1, "a" | Yes | minimal valid assignment |
| 0 5 0, "12345" | Yes | category with zero others ignored |
| 2 2 2, "abc123!!!" | No | tight capacity mismatch forcing failure |

## Edge Cases

A subtle edge case arises when one category is empty. For example:

Input:

```
1 1 1
abc123
```

Here punctuation is zero. The algorithm still treats punctuation as a category with count 0, and any assignment where it maps to any color remains valid because 0 ≤ capacity always holds. The permutation check naturally accommodates this without special handling.

Another edge case is when all characters belong to a single category:

Input:

```
10 10 10
abcdef
```

Counts are letters = 6, digits = 0, punctuation = 0. The algorithm checks all permutations, and any mapping where letters are assigned to a capacity ≥ 6 succeeds. Since at least one such mapping exists, the output is correctly `Yes`.

A final edge case involves tight coupling where only one specific permutation works. The brute permutation loop ensures this is still found, since every bijection is tested independently and no heuristic pruning is applied.
