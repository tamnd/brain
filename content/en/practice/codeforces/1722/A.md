---
title: "CF 1722A - Spell Check"
description: "We are given a short string in each test case and we need to decide whether it can be interpreted as a rearrangement of the name “Timur” under a very specific spelling rule. The rule is not just that the letters match."
date: "2026-06-15T01:24:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1722
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 817 (Div. 4)"
rating: 800
weight: 1722
solve_time_s: 122
verified: true
draft: false
---

[CF 1722A - Spell Check](https://codeforces.com/problemset/problem/1722/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string in each test case and we need to decide whether it can be interpreted as a rearrangement of the name “Timur” under a very specific spelling rule.

The rule is not just that the letters match. The string must use exactly the five letters that appear in “Timur”, with the same multiplicity, and the uppercase structure must also match: the letter T must appear exactly once and must be uppercase, while the remaining letters must be the lowercase letters i, m, u, and r, each appearing exactly once.

So each test case is essentially asking whether the input string is a valid permutation of the multiset {T, i, m, u, r} with a fixed case constraint.

The input size is extremely small, with at most 10 characters per string and up to 1000 test cases. This immediately implies that any solution with even a simple per-test scan or comparison is easily fast enough. There is no need for advanced data structures or preprocessing, since even an O(10) check per test case is trivial.

The main subtlety is case sensitivity and exact matching. A few common mistakes arise here. One is forgetting that uppercase matters, so “timur” should fail even though the letters match. Another is allowing repeated letters, such as “Timuur”, which introduces duplication and breaks the permutation requirement. A third is accepting strings of the correct letters but incorrect length, such as “Timr”, which is missing a character and should be rejected immediately.

## Approaches

A brute-force way to think about the problem is to generate all permutations of the string “Timur” and check whether the input string matches any of them. Since the name has 5 distinct characters, there are 5! = 120 permutations. For each test case we could compare against all 120 candidates. This works, but it is unnecessary overkill and hides the structure of the problem.

The structure becomes clearer if we notice that “valid spelling” is just membership in a fixed set of five strings. Every valid answer must contain exactly one of each required character with fixed casing. Instead of generating permutations, we can directly compare whether the sorted or frequency representation of the input matches the reference pattern.

A simpler view is to treat the correct answer as a multiset with constraints. We check that the length is exactly 5, then verify that each required character appears exactly once with correct case. This reduces the problem to constant-time checks per test case.

The key insight is that we are not searching over arrangements; we are verifying equality against a fixed multiset with case constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(120 · t) | O(1) | Accepted but unnecessary |
| Direct frequency / set check | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Predefine the exact valid structure of the name as a frequency map: one 'T', one 'i', one 'm', one 'u', and one 'r'. This acts as our target signature.
2. For each test case, first check the length of the string. If it is not 5, we can immediately reject it because a valid spelling must use exactly five letters.
3. Build a frequency counter for the characters in the input string. Since the string is tiny, a simple dictionary or direct counting is sufficient.
4. Compare this frequency map against the target. Every required character must appear exactly once, and no extra characters are allowed.
5. If all conditions match, output “YES”; otherwise output “NO”.

The reason this ordering matters is efficiency and correctness clarity. The length check eliminates many invalid cases immediately, and ensures we do not accidentally accept strings with repeated characters that still contain all required letters.

### Why it works

The algorithm relies on the invariant that a valid spelling of the name corresponds exactly to a permutation of a fixed multiset of characters. Two strings are permutations of each other if and only if they share identical character frequencies. Because the case-sensitive requirement is embedded directly into the multiset definition, frequency comparison fully captures all constraints of the problem. No other structural property of the string matters.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = {'T': 1, 'i': 1, 'm': 1, 'u': 1, 'r': 1}

def ok(s: str) -> bool:
    if len(s) != 5:
        return False
    cnt = {}
    for c in s:
        cnt[c] = cnt.get(c, 0) + 1
    return cnt == TARGET

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        print("YES" if ok(s) else "NO")

if __name__ == "__main__":
    solve()
```

The solution first fixes the expected frequency dictionary for the valid name. Each test case is handled independently, and we ignore the provided length `n` except as a consistency check, since the actual string length is directly measured.

The frequency comparison is exact, so any deviation such as wrong casing, missing letters, or repeated characters immediately fails.

A subtle implementation detail is using `strip()` when reading the string. This prevents newline characters from interfering with the comparison, which is a common source of hidden bugs in contest settings.

## Worked Examples

We trace two representative cases from the sample.

### Example 1

Input string: `Timur`

| Step | String | Length check | Frequency map | Result |
| --- | --- | --- | --- | --- |
| 1 | Timur | 5 | T:1 i:1 m:1 u:1 r:1 | YES |

This confirms the ideal case where the string exactly matches the required multiset. Every character appears once and casing is correct.

### Example 2

Input string: `Timr`

| Step | String | Length check | Frequency map | Result |
| --- | --- | --- | --- | --- |
| 1 | Timr | 4 | T:1 i:1 m:1 r:1 | NO |

Here the length check fails immediately. Even though all characters appear correct, the missing 'u' invalidates the permutation requirement.

These two cases illustrate the two essential failure modes: incorrect length and incorrect frequency composition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case processes at most 10 characters, so total work is linear in number of test cases |
| Space | O(1) | Only a fixed-size frequency dictionary is used per test case |

The constraints ensure that even the most direct implementation is easily within limits. The constant bound on string length guarantees that frequency counting is effectively constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    TARGET = {'T': 1, 'i': 1, 'm': 1, 'u': 1, 'r': 1}
    for _ in range(t):
        n = int(sys.stdin.readline())
        s = sys.stdin.readline().strip()
        cnt = {}
        if len(s) != 5:
            output.append("NO")
            continue
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        output.append("YES" if cnt == TARGET else "NO")
    return "\n".join(output) + "\n"

# provided samples
assert run("""10
5
Timur
5
miurT
5
Trumi
5
mriTu
5
timur
4
Timr
6
Timuur
10
codeforces
10
TimurTimur
5
TIMUR
""") == """YES
YES
YES
YES
NO
NO
NO
NO
NO
NO
"""

# custom cases
assert run("""3
5
Timur
5
Turim
5
TiMur
""") == """YES
YES
NO
""", "case sensitivity check"

assert run("""2
5
Tiiur
5
Timurx
""") == """NO
NO
""", "duplicates and invalid char"

assert run("""1
1
T
""") == "NO\n", "minimum size invalid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Valid permutations | YES | correctness on all valid reorderings |
| Case errors | NO | uppercase constraint enforcement |
| Invalid characters / duplicates | NO | strict multiset matching |
| Minimum size | NO | length constraint handling |

## Edge Cases

A common edge case is when all required letters are present but casing is wrong, such as “timur”. The frequency map matches in structure but not in exact keys, since lowercase ‘t’ is not the required uppercase ‘T’. The algorithm correctly rejects this because dictionary equality is case-sensitive.

Another edge case is repeated letters like “Timuur”. The length may still be 5 if another letter is missing elsewhere, but frequency comparison exposes the imbalance immediately. The count for ‘u’ becomes 2, which fails the exact match against the target.

A final edge case is strings containing extra characters such as “Timurx”. Even though the first five letters are valid, the additional character breaks both the length condition and frequency equality. The algorithm rejects it at the length check stage, preventing unnecessary computation.
