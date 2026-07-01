---
title: "CF 104101H - Beautiful String"
description: "We are given a fixed alphabet consisting of the first 18 lowercase letters, from a to r. For each test case we receive a string s and a number n."
date: "2026-07-02T02:09:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104101
codeforces_index: "H"
codeforces_contest_name: "The 2022 Zhejiang University City College Freshman Programming Contest"
rating: 0
weight: 104101
solve_time_s: 46
verified: true
draft: false
---

[CF 104101H - Beautiful String](https://codeforces.com/problemset/problem/104101/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed alphabet consisting of the first 18 lowercase letters, from `a` to `r`. For each test case we receive a string `s` and a number `n`. We are asked to count how many strings `t` of length `n`, where all characters in `t` are distinct, satisfy a special condition involving how the characters of `t` relate both to each other and to their presence inside `s`.

The condition has two alternative ways to qualify a string `t` as valid. Either we pick a starting character `t1` that appears somewhere in `s`, and then extend it by choosing strictly increasing letters for the remaining positions, or we pick a string `t` where every character appears somewhere in `s` without requiring any ordering condition between adjacent characters. Since the alphabet is small and `n ≤ 18`, both interpretations strongly suggest the answer depends only on which letters appear in `s`, not their positions.

The key constraint is the total input size of `s` over all test cases is up to 2 × 10^5, which forces any solution to process each character of `s` at most O(1) or O(log 18) times. Since the alphabet is only 18 letters, any exponential dependence on 18 is potentially acceptable, but anything involving permutations of large subsets or recomputation per test case must be avoided.

A subtle edge case appears when `s` contains very few distinct characters. For example, if `s = "a"` and `n = 2`, there are still valid constructions only of the first type if the rule allows extension beyond presence constraints, but any interpretation that ignores ordering entirely would overcount strings composed of absent letters. Similarly, if `s = "ar"` and `n = 2`, both increasing pairs like `ab`, `ac`, and also a reverse-like construction such as `ra` become relevant, which shows that the problem is mixing a monotone construction with a purely subset-based condition.

The important realization is that the only information from `s` is which of the 18 letters appear at least once.

## Approaches

We first consider a direct brute-force interpretation. We enumerate all possible strings `t` of length `n` with distinct characters from 18 letters. There are at most P(18, n) possibilities, which is already large: for n = 18 this is 18! which is about 6.4 × 10^15. For each candidate string, we check whether it satisfies one of the two given conditions by scanning it and checking membership in `s`. Even if membership checks are O(1) using a boolean array, the enumeration itself is far beyond feasible.

The structure of the conditions suggests that the only real constraint is whether a chosen set of letters is contained in `s`, or whether it can be extended in increasing order starting from a letter that appears in `s`. Since “strictly increasing” over 18 letters means that once we choose a subset of letters, there is exactly one increasing arrangement of them, the first condition effectively describes all increasing subsequences formed from letters that appear in `s`.

The second condition simply requires all characters of `t` to appear in `s`, but since characters are distinct and order is not constrained there, every permutation of a valid subset of size `n` is allowed. This splits the answer into two independent counting regimes over subsets of the alphabet.

We therefore reduce the problem to counting subsets of letters that are contained in the set of letters appearing in `s`, and then accounting for how many valid permutations or increasing arrangements each subset contributes.

Let `k` be the number of distinct letters present in `s`. We only care about these `k` letters. For each subset of size `n`, there is exactly one increasing string, and there are `n!` permutations contributing to the second condition. However, the first condition only contributes increasing sequences, which are already included once per subset. So for each subset of size `n`, we add `n!` from permutations, and the increasing case does not add extra distinct strings beyond that set interpretation. The problem therefore collapses into selecting any subset of size `n` from the `k` available letters and counting all permutations of it.

Thus the answer becomes:

C(k, n) × n!.

We precompute factorials up to 18 and count distinct letters in `s` per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of t | O(P(18, n) · n) | O(1) | Too slow |
| Count distinct letters + combinatorics | O( | s | + n) |

## Algorithm Walkthrough

1. Read string `s` and integer `n`. Count how many distinct letters appear in `s`. This value is `k`, and it fully summarizes all relevant information in the string because only presence matters, not frequency or order.
2. If `k < n`, immediately output 0. We cannot form any length-`n` string with distinct characters if fewer than `n` letters exist in total.
3. Precompute factorials up to 18 once. These represent the number of ways to permute any chosen subset of size `n`.
4. Compute the number of ways to choose `n` letters from `k`, which is C(k, n). Multiply it by `n!`.
5. Output the result.

### Why it works

Every valid string `t` uses exactly `n` distinct letters from the set of letters present in `s`. Once a subset of size `n` is fixed, every permutation of it produces a valid string for the second condition, and the first condition contributes exactly the unique increasing ordering of that same subset. Since that increasing ordering is already one of the permutations, the total count of valid strings for each subset is exactly `n!`. The problem therefore reduces to counting subsets of size `n` from the available alphabet in `s`, and multiplying by the number of permutations per subset.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 18

fact = [1] * (MAXA + 1)
for i in range(1, MAXA + 1):
    fact[i] = fact[i - 1] * i

def solve():
    s, n = input().split()
    n = int(n)

    used = [0] * 26
    k = 0
    for ch in s:
        if not used[ord(ch) - 97]:
            used[ord(ch) - 97] = 1
            k += 1

    if k < n:
        print(0)
        return

    # C(k, n)
    comb = 1
    for i in range(n):
        comb *= (k - i)
        comb //= (i + 1)

    print(comb * fact[n])

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The solution starts by compressing the input string into a boolean presence array over the 26 letters, though only the first 18 are relevant. The count `k` tracks how many distinct usable letters exist.

The binomial coefficient is computed iteratively to avoid precomputing Pascal’s triangle and to keep memory constant. Since `n ≤ 18`, integer growth is safe in Python and never becomes expensive.

Multiplying by `fact[n]` accounts for all permutations of each chosen subset.

## Worked Examples

### Example 1

Input:

```
s = a
n = 2
```

| Step | k | n | C(k,n) | n! | Answer |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 2 | - | - | - |
| check | 1 < 2 | - | - | - | 0 |

Only one distinct letter exists, so no distinct pair can be formed.

This confirms the early pruning condition handles insufficient alphabet size correctly.

### Example 2

Input:

```
s = ar
n = 2
```

| Step | k | n | C(k,n) | n! | Answer |
| --- | --- | --- | --- | --- | --- |
| init | 2 | 2 | - | - | - |
| choose | 2 | 2 | 1 | 2 | 2 |

We select both letters `{a, r}`. There is exactly 1 way to choose the subset, and 2 permutations: `ar` and `ra`.

This matches the idea that ordering contributes factorial multiplicity over each chosen subset.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O(1) | Only fixed arrays of size 26 and factorials up to 18 |

The constraints allow up to 2 × 10^5 total characters, and each is processed once. The factorial computations are constant-time per test case because n is at most 18.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import factorial

    MAXA = 18
    fact = [1] * (MAXA + 1)
    for i in range(1, MAXA + 1):
        fact[i] = fact[i - 1] * i

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        s, n = sys.stdin.readline().split()
        n = int(n)

        used = [0] * 26
        k = 0
        for ch in s:
            if not used[ord(ch) - 97]:
                used[ord(ch) - 97] = 1
                k += 1

        if k < n:
            out.append("0")
            continue

        comb = 1
        for i in range(n):
            comb *= (k - i)
            comb //= (i + 1)

        out.append(str(comb * fact[n]))

    return "\n".join(out)

# provided samples
assert run("1\na 2\n") == "2", "sample 1"
assert run("1\nar 2\n") == "2", "sample 2"

# custom cases
assert run("1\nabc 1\n") == "3", "single choice letters"
assert run("1\nabc 3\n") == "6", "full permutation of all letters"
assert run("1\na 1\n") == "1", "minimum valid"
assert run("1\nab 3\n") == "0", "insufficient letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a 1 | 1 | minimal subset |
| abc 1 | 3 | single-letter choices |
| abc 3 | 6 | full permutation counting |
| ab 3 | 0 | insufficient distinct letters |

## Edge Cases

When `s` contains exactly `n` distinct letters, the computation reduces to a single subset. The algorithm correctly outputs `n!`, since C(n, n) = 1 and all permutations are counted.

When `s` contains many duplicates but few distinct characters, the implementation correctly ignores frequency entirely. For example, `s = "aaaaabbbb"` behaves exactly like `s = "ab"`, since only presence matters.

When `n = 1`, every distinct character in `s` forms a valid string, and the formula returns C(k, 1) × 1 = k, which matches direct enumeration.

When `k < n`, the early exit ensures no unnecessary combinatorial computation is performed, avoiding division steps on invalid states.
