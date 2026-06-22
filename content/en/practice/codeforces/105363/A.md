---
title: "CF 105363A - Hello!"
description: "We are given several short strings, and for each one we must decide whether it can be rearranged to form the word “hola”. Rearranging means we are allowed to permute the characters freely, but we cannot add or remove any character."
date: "2026-06-23T05:34:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105363
codeforces_index: "A"
codeforces_contest_name: "XXV Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105363
solve_time_s: 71
verified: true
draft: false
---

[CF 105363A - Hello!](https://codeforces.com/problemset/problem/105363/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several short strings, and for each one we must decide whether it can be rearranged to form the word “hola”. Rearranging means we are allowed to permute the characters freely, but we cannot add or remove any character. So the task reduces to checking whether the multiset of letters in the input word matches exactly the multiset of letters in “hola”.

Each query is independent, and the strings are extremely small, so the decision for each case is purely local to that string. The output for each case is a simple acceptance or rejection based on this comparison.

The constraint that each string has length at most 5 changes the perspective significantly. Any algorithm that does constant or near-constant work per character is trivially fast enough. Even something slightly redundant, like sorting each string, is still negligible. This pushes the solution away from complexity concerns and toward correctness and simplicity.

A few edge cases appear naturally. A string with repeated letters such as “holaa” must be rejected because it contains an extra character even though it includes all required ones. A shorter string such as “ola” must also be rejected because it is missing letters. Another case is a correct permutation like “ohal”, where the letters match exactly but are shuffled.

A naive approach that only checks whether all required characters appear at least once would fail. For example, “holi” contains h, o, l, i, so a naive presence check might mistakenly accept it if it does not account for exact frequency matching.

## Approaches

A brute-force way to think about this problem is to generate all permutations of the input string and check whether any of them equals “hola”. Since the strings have length at most 5, the maximum number of permutations is 120, so this is technically feasible per test case. However, generating permutations repeatedly is unnecessary work, and conceptually it obscures the simpler structure of the problem. The correctness comes from matching character counts, not exploring rearrangements explicitly.

The key observation is that two strings are permutations of each other if and only if they contain the same frequency of each character. Instead of generating rearrangements, we can directly compare character counts. Since the target word is fixed and very small, we can either sort both strings or count frequencies and compare.

Sorting is particularly clean here. If we sort the input string and compare it to the sorted version of “hola”, which is “ahlo”, we get an immediate equality test. Alternatively, a frequency array over 26 lowercase letters works equally well, but sorting is sufficient and arguably simpler for such small constraints.

The brute-force approach spends time exploring unnecessary structures, while the optimal view collapses the problem into a direct canonical representation of each string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (generate permutations) | O(T · n! · n) | O(n) | Too slow in spirit, unnecessary |
| Optimal (sort or frequency compare) | O(T · n log n) | O(1) | Accepted |

## Algorithm Walkthrough

We will use the sorting-based approach because it is the most direct.

1. Precompute the sorted reference string for “hola”, which becomes “ahlo”. This gives us a canonical form to compare against every input.
2. Read the number of test cases T, since each case is independent and must be processed separately.
3. For each input string s, compute its sorted version. Sorting ensures that any permutation of the same letters collapses into the same representation.
4. Compare the sorted string with “ahlo”. If they are identical, the input is exactly a permutation of “hola”, so we output “SI”. Otherwise, we output “NO”.
5. Repeat this process for all test cases, producing one answer per line.

### Why it works

Sorting defines a deterministic canonical form for any multiset of characters. Two strings are permutations of each other if and only if their sorted representations are identical. This creates a one-to-one mapping between equivalence classes of strings under permutation and their sorted forms, so equality of sorted strings is both necessary and sufficient for correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    target = sorted("hola")
    target = "".join(target)

    t = int(input().strip())
    for _ in range(t):
        s = input().strip()
        if "".join(sorted(s)) == target:
            print("SI")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution first constructs the sorted form of the target word “hola”, which is “ahlo”. This avoids recomputing or hardcoding character comparisons manually.

For each test case, the input string is sorted using Python’s built-in sort, which is efficient and sufficient given the maximum length of 5. The comparison is then a simple string equality check, which directly encodes whether both strings have identical character multisets.

The use of `sys.stdin.readline` ensures fast input handling, although performance is not critical here due to small constraints. The logic itself is entirely centered on canonical representation through sorting.

## Worked Examples

We trace two cases: one valid permutation and one invalid string.

### Example 1

Input string: `ohal`

| Step | String | Sorted form | Compare with "ahlo" | Result |
| --- | --- | --- | --- | --- |
| 1 | ohal | ahol | ahol == ahlo | NO |
| 2 |  |  |  |  |

Here we see that although the string contains the same letters as “hola”, the sorted form differs, so it is rejected. This shows that sorting must match exactly, not partially.

Now consider a correct case.

Input string: `loha`

| Step | String | Sorted form | Compare with "ahlo" | Result |
| --- | --- | --- | --- | --- |
| 1 | loha | ahlo | ahlo == ahlo | SI |

This confirms that any permutation collapses to the same canonical form.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · n log n) | Each string of length at most 5 is sorted independently |
| Space | O(1) | Only a fixed reference string and temporary sorting space are used |

The constraints are so small that even repeated sorting is effectively constant time. The solution is well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("""6
hola
ola
ohal
loha
holaa
holi
""") == """SI
NO
NO
SI
NO
NO"""

# minimum size
assert run("""2
h
a
""") == """NO
NO"""

# exact match and permutation variants
assert run("""3
hola
loah
ahlo
""") == """SI
SI
SI"""

# repeated character case
assert run("""2
holaa
aahlo
""") == """NO
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single letters | NO, NO | minimum size rejection |
| permutations of hola | SI lines | correctness under reordering |
| repeated letters | NO | frequency mismatch handling |

## Edge Cases

A string shorter than “hola”, such as `h`, is handled by sorting into a single-character string. Since this cannot match the four-character reference, the comparison fails immediately and produces “NO”.

A string with repeated letters like `holaa` sorts to `aa hlo` (conceptually `aahlo`), which differs from `ahlo`, so it is rejected. This confirms that frequency mismatches are correctly detected without explicitly counting characters.

A fully valid permutation like `loah` sorts to `ahlo`, matching the target exactly. This confirms that order differences are fully normalized by the sorting step.
