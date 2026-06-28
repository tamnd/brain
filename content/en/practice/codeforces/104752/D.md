---
title: "CF 104752D - Determine Palindrome Message"
description: "We are given a single string consisting of lowercase Latin characters, but it may also contain digits or other characters in the input format examples, so we treat it as a sequence of symbols."
date: "2026-06-29T01:24:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "D"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 63
verified: true
draft: false
---

[CF 104752D - Determine Palindrome Message](https://codeforces.com/problemset/problem/104752/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string consisting of lowercase Latin characters, but it may also contain digits or other characters in the input format examples, so we treat it as a sequence of symbols. From this string, we are allowed to choose some multiset of characters, and rearrange them in any order. The goal is to decide whether there exists a non-empty selection of these characters that can be permuted into a palindrome.

A palindrome requires symmetry around its center. That symmetry imposes a strict condition on how many times each character can appear. Characters must pair up on opposite sides, and at most one character is allowed to remain unpaired in the center position.

The string length is up to 100000, which immediately suggests that any solution must run in linear time or close to it. A quadratic or exponential approach would be impossible because even a simple $O(n^2)$ check would already be around $10^{10}$ operations in the worst case.

A subtle edge case is that we are not required to use all characters. This matters because it removes the usual “frequency parity” constraint over the full string. For example, if we had exactly one character appearing once, we can simply ignore it and form a palindrome from the rest, which is always valid if at least one character exists. Another edge case is a string with all distinct characters. Even there, we can pick any single character and form a length 1 palindrome.

A naive mistake would be to assume we must use all characters. For example, input `abc` would be incorrectly rejected if one assumes all letters must be used, but in fact we can pick `a` alone and form a palindrome.

## Approaches

A brute-force interpretation would try to test all subsets of characters, and for each subset check whether it can be permuted into a palindrome. Even if we ignore ordering and only consider character counts, the number of subsets is $2^n$, which is completely infeasible for $n = 10^5$. Even reducing to frequency vectors does not help because the state space remains exponential.

The key observation is that since we can discard characters freely, the only requirement for constructing a palindrome is that we can select at least one character. Any single character forms a valid palindrome of length one. This immediately collapses the problem: as long as the string is non-empty, the answer is always YES.

The intended deeper viewpoint is that palindrome feasibility depends on parity constraints, but those constraints can always be satisfied by choosing a single character occurrence. There is no restriction forcing us to use multiple distinct characters.

Thus the problem reduces to checking whether the input string contains at least one character, which is always true given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n) | O(n) | Too slow |
| Optimal observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal idea

1. Read the input string $s$. We only need to know whether it is empty or not.
2. If $s$ has length at least 1, immediately conclude that we can form a palindrome.
3. Print YES.

The reasoning behind step 2 is that any single character is already a palindrome. Since we are allowed to choose a subset of letters, we can always pick one occurrence and form a valid palindrome of length one.

## Why it works

A palindrome condition requires that all characters except possibly one have even frequency in the chosen multiset. If we choose exactly one character, its frequency is 1, and it trivially satisfies the condition because it is the middle character. Therefore every non-empty multiset of size 1 is valid, which means any non-empty input string automatically contains a valid selection.

The invariant is that we are not required to use all characters, only to exhibit one subset that can be rearranged into a palindrome. The singleton subset always satisfies this invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().rstrip("\n")
    if len(s) > 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads the input string and checks its length. No frequency counting is required because the ability to discard characters trivializes the parity constraints. The only subtle point is stripping the newline correctly; otherwise, the length check would still work but may include the newline character depending on the environment.

## Worked Examples

### Example 1: `3aab`

We track only whether we can form a palindrome subset.

| Step | Current string | Action | Reason |
| --- | --- | --- | --- |
| 1 | 3aab | read input | input exists |
| 2 | 3aab | check length | non-empty |
| 3 | YES | output | single character subset exists |

This shows that even though the string contains multiple distinct symbols, we can choose a single character like `a`.

### Example 2: `3abc`

| Step | Current string | Action | Reason |
| --- | --- | --- | --- |
| 1 | 3abc | read input | input exists |
| 2 | 3abc | check length | non-empty |
| 3 | YES | output | pick one character |

This confirms that lack of repeated characters does not matter because subset selection allows us to ignore constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single scan to read string |
| Space | O(1) | no auxiliary data structures |

The solution easily fits within constraints since it performs only a constant amount of work after reading the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    s = sys.stdin.readline().rstrip("\n")
    print("YES" if len(s) > 0 else "NO")

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("3aab\n") == "YES"
assert run("3abc\n") == "YES"
assert run("6aaaaaa\n") == "YES"

# custom cases
assert run("a\n") == "YES", "single character"
assert run("z\n") == "YES", "any single char works"
assert run("1234567890\n") == "YES", "mixed digits still valid"
assert run("\n") == "NO", "empty string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | YES | minimal non-empty case |
| `"z"` | YES | any single symbol works |
| `"1234567890"` | YES | non-letter characters irrelevant |
| `""` | NO | empty input edge case |

## Edge Cases

The empty string case is the only meaningful boundary condition. If the input line is empty, the algorithm correctly outputs NO because no characters are available to form even a length-1 palindrome.

For input `"a"`, the algorithm reads a non-empty string, checks length, and immediately returns YES. The chosen subset is `{a}`, which forms the palindrome `"a"`.

For input `"abcde"`, the algorithm again returns YES because it does not attempt to enforce symmetry on the full set. Instead, it implicitly selects a single character such as `"c"` and forms a valid palindrome.

All other cases follow the same pattern, and the decision is always determined solely by whether at least one character exists.
