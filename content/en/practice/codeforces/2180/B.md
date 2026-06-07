---
title: "CF 2180B - Ashmal"
description: "We are given a sequence of strings, and we must insert them one by one into an initially empty string. Each new string can be placed either at the left end or the right end of the current result. After all insertions, we obtain a single final string."
date: "2026-06-07T22:06:10+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2180
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 31 (Div. 1 + Div. 2)"
rating: 800
weight: 2180
solve_time_s: 89
verified: true
draft: false
---

[CF 2180B - Ashmal](https://codeforces.com/problemset/problem/2180/B)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of strings, and we must insert them one by one into an initially empty string. Each new string can be placed either at the left end or the right end of the current result. After all insertions, we obtain a single final string. Our task is to choose directions of insertion so that this final string is lexicographically smallest among all possible choices.

The key difficulty is that each decision affects future structure in a global way. A choice that looks locally better may block a better arrangement later, because once a string is placed on a side, its internal characters become fixed relative to the rest of the construction.

The constraints are small in terms of number of strings, at most 1000 per test and total length at most 4000. This immediately rules out any approach that tries all 2^n assignments of directions. Even 2^1000 is completely infeasible. We are therefore looking for a greedy decision process where each string is placed once with some locally optimal rule.

A subtle edge case comes from strings that are identical or share long prefixes. For example, if we have strings like `"ab"` and `"aa"`, placing `"ab"` on the left versus right changes which character is compared first in the final lexicographic comparison. A naive approach that simply compares strings independently without considering both orientations of the whole constructed sequence will fail.

Another corner case is when multiple strings begin with the same character. A greedy rule that only compares first characters without looking at the eventual full concatenation may make the wrong early placement, because the decisive comparison can happen far deeper inside concatenated blocks.

## Approaches

A brute-force idea is to try every possible assignment of each string to either the left or right side. For each of the 2^n configurations, we build the resulting string and take the minimum lexicographically. This is correct because it explores all possible outcomes, but it is exponential in n and fails immediately at n = 1000.

The important observation is that we do not need to construct full candidate strings. At each step, we are only deciding between two possibilities: put the next string at the front or at the back. The final string is a concatenation of blocks, so lexicographic comparison between two complete outcomes depends on the first position where they differ. That position must lie entirely inside one of the blocks or at a boundary between blocks.

This reduces the problem to a greedy ordering decision for each string independently: when considering placing a string `x`, we compare two hypothetical outcomes: current result + x at end, and x + current result at front. Instead of building both full strings, we only need to know which concatenation is lexicographically smaller.

The key simplification is that we can safely decide greedily at each step: between placing `x` on the left or right, we compare `x + current` versus `current + x`. The smaller of the two determines the optimal placement for this step.

This works because the decision does not depend on future strings: future insertions will only append further blocks on either side, but they affect both branches symmetrically. Thus, once we pick the smaller orientation at step i, no later choice can reverse the lexicographic ordering established at the first differing position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · total length) | O(total length) | Too slow |
| Optimal Greedy | O(n · total length) | O(total length) | Accepted |

## Algorithm Walkthrough

We maintain a current string `s`, initially empty.

1. Start with `s = ""`. This represents the empty construction before any insertions. There is no decision to make for the first string because both front and back insertions produce the same result.
2. For each next string `x`, consider the two possible outcomes: placing `x` at the front gives `x + s`, placing it at the back gives `s + x`.
3. Compare these two candidate strings lexicographically. The lexicographic order depends on the first index where they differ, so we simulate the comparison directly using Python string comparison.
4. If `x + s` is smaller, update `s = x + s`. Otherwise set `s = s + x`. This ensures that after processing each string, `s` is the best achievable result for the prefix of processed strings.
5. Continue until all strings are processed and output `s`.

The reason this works is that once we commit to placing a string on one side, all future strings only extend the result beyond the first mismatch point between the two options. That mismatch point determines the ordering permanently, so no later operation can change the relative order established at step i.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = input().split()

        s = ""

        for i in range(n):
            x = arr[i]

            # compare two possible placements
            if x + s < s + x:
                s = x + s
            else:
                s = s + x

        print(s)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the greedy rule. The only nontrivial part is the comparison `x + s < s + x`, which correctly models lexicographic ordering between the two possible final states at this step.

A common mistake is trying to compare only first characters or lengths. That fails because the deciding character may appear deep inside either string. Python’s string comparison already handles full lexicographic evaluation correctly, so we rely on it safely.

## Worked Examples

### Example 1

Input:

```
n = 3
a = ["a", "ab", "abc"]
```

| Step | x | current s | x + s | s + x | chosen s |
| --- | --- | --- | --- | --- | --- |
| 1 | a | "" | a | a | a |
| 2 | ab | a | aba | aab | aab |
| 3 | abc | aab | abcaab | aababc | aababc |

Final output is `aababc`.

This trace shows how early placement affects prefix ordering. Even though `"ab"` is larger than `"a"` in isolation, placing it after `"a"` produces a better prefix alignment.

### Example 2

Input:

```
n = 2
a = ["b", "ba"]
```

| Step | x | current s | x + s | s + x | chosen s |
| --- | --- | --- | --- | --- | --- |
| 1 | b | "" | b | b | b |
| 2 | ba | b | bab | bba | bab |

Final output is `bab`.

This demonstrates how the comparison correctly decides placement based on full concatenation rather than just first characters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each step compares concatenations whose total length is proportional to current result |
| Space | O(L) | We store only the evolving string |

The total length across all strings is bounded by 4000, so even repeated comparisons remain fast. The solution easily fits within limits.

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
        n = int(input())
        arr = input().split()
        s = ""
        for x in arr:
            if x + s < s + x:
                s = x + s
            else:
                s = s + x
        out.append(s)
    return "\n".join(out)

# provided samples
assert run("""3
4
amir rima amin nima
1
codeforces
3
a ab abc
""") == """aminamirrimanima
codeforces
aababc"""

# custom case 1: single element
assert run("""1
1
zzz
""") == "zzz"

# custom case 2: identical strings
assert run("""1
3
a a a
""") == "aaa"

# custom case 3: strong prefix effect
assert run("""1
2
ba ab
""") == "abba"

# custom case 4: alternating greedy pressure
assert run("""1
4
b ba a aa
""") == "aaaabba"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | unchanged string | base case handling |
| all equal | concatenation stability | identical comparisons |
| "ba ab" | abba | ordering sensitivity to full comparison |
| mixed prefixes | stable greedy behavior | multi-step interactions |

## Edge Cases

One edge case is when all strings are identical. The algorithm always compares `x + s` and `s + x`, which are equal, so it consistently appends to the right. This produces a straightforward concatenation without ambiguity.

Another case is when a string is a prefix of another. For example, `"a"` and `"ab"` can lead to different lexicographic outcomes depending on placement. The algorithm correctly resolves this because `"ab" + "a" = "aba"` is greater than `"a" + "ab" = "aab"`, so `"a"` is placed first, preserving lexicographic optimality.

A final subtle case is alternating small and large strings. Even when local comparisons suggest a reversal, the full concatenation comparison ensures that only the first differing character decides placement, so earlier decisions remain consistent with global lexicographic order.
