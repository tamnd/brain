---
title: "CF 103577C - Corona"
description: "Each test case gives a genome string, and we must assign a numerical score that comes from all of its contiguous substrings. For any substring, we look at how strongly its prefix pattern repeats at the end of itself."
date: "2026-07-03T03:31:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103577
codeforces_index: "C"
codeforces_contest_name: "2021 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 103577
solve_time_s: 148
verified: true
draft: false
---

[CF 103577C - Corona](https://codeforces.com/problemset/problem/103577/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a genome string, and we must assign a numerical score that comes from all of its contiguous substrings. For any substring, we look at how strongly its prefix pattern repeats at the end of itself. More precisely, for a substring, we take the longest proper prefix that also appears as a suffix of the same substring, and we measure its length. That length is called the level of the substring. The task is to sum this level over every possible substring of the given string.

The input consists of up to 50 strings, each of length at most 5000. This immediately rules out any approach that treats each substring independently with a linear scan. There are O(n^2) substrings per string, so even O(n) work per substring leads to about 1.25 × 10^11 operations in the worst case, which is far beyond feasibility.

A subtle issue is that the level is defined using proper prefix and suffix, so the whole substring itself is not allowed even if it matches trivially. For example, for "aaaa", the substring "aa" has level 1, but "a" has level 0. Another point that often causes mistakes is overlapping structure: different substrings share large portions of computation, so recomputing prefix-suffix structure from scratch for each substring is wasteful.

Edge cases arise when the string has no repetition, such as "abcde", where every substring has level 0, and when the string is highly repetitive, such as "aaaaa", where every substring has a large border structure. A naive solution that forgets to exclude the full substring as a valid border would overcount in cases like "aaa", where "aaa" should contribute 2, not 3.

## Approaches

The brute force approach examines every substring and computes its level independently. For a substring s[l..r], we can run a prefix-suffix computation over that substring, such as KMP prefix-function, to find its longest border. Computing this costs O(r-l+1), and since there are O(n^2) substrings, the total complexity becomes O(n^3). With n up to 5000, this is already too slow, and repeated over up to 50 test cases it becomes completely infeasible.

The key observation is that the level of a substring depends only on prefix-function behavior inside that substring, and prefix-function can be computed incrementally in linear time for any fixed starting position. If we fix a left endpoint i, then for the suffix s[i:], we can compute its prefix-function once in O(n). Every prefix of this suffix corresponds exactly to a substring starting at i. The prefix-function value at position j gives the level of substring s[i..i+j]. This removes repeated recomputation and reduces the total work to O(n^2) per string.

The transition from brute force to optimal is essentially moving from recomputing structure per substring to reusing the automaton-like transitions of KMP across all substrings sharing the same start.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Prefix-function per start | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We process each string independently.

1. Fix a starting index i from 0 to n − 1. We will treat s[i:] as a fresh string.
2. Build the prefix-function array pi for this suffix using standard KMP logic.

At position j in this suffix, pi[j] represents the length of the longest proper prefix of s[i..i+j] that is also its suffix.
3. For every j, add pi[j] to the answer. This directly accumulates the level of substring s[i..i+j].
4. Repeat for all starting positions i, summing contributions.

The important detail is that pi is recomputed for each suffix, not for the whole string once. This is necessary because prefix relationships are relative to the start of the substring.

### Why it works

For a fixed i, the prefix-function computation simulates matching prefixes of s[i:] against its own suffixes. At each position j, the computed pi[j] is exactly the longest border of the substring s[i..i+j] because the prefix-function is defined to track the longest proper prefix that is also a suffix of the prefix ending at j. Since every substring is uniquely represented as a prefix of some suffix, summing all pi[j] over all i,j covers every substring exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(s: str) -> int:
    n = len(s)
    total = 0

    for i in range(n):
        pi = [0] * (n - i)
        for j in range(1, n - i):
            k = pi[j - 1]
            while k > 0 and s[i + j] != s[i + k]:
                k = pi[k - 1]
            if s[i + j] == s[i + k]:
                k += 1
            pi[j] = k
            total += k

    return total

def main():
    data = sys.stdin.read().strip().split()
    out = []
    for s in data:
        out.append(str(solve_one(s)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The outer loop fixes the substring start, and the inner loop builds the prefix-function incrementally. The variable k plays the role of the current border length candidate, exactly as in KMP. Each mismatch fallback follows the failure links encoded in pi.

A common implementation pitfall is forgetting to offset indices by i when comparing characters. Another is accidentally using a single global prefix-function, which would mix unrelated substrings and produce incorrect borders.

## Worked Examples

Consider the string "aaa".

For i = 0:

| j | substring | pi[j] |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | aa | 1 |
| 2 | aaa | 2 |

Contribution is 3.

For i = 1:

| j | substring | pi[j] |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | aa | 1 |

Contribution is 1.

For i = 2:

| j | substring | pi[j] |
| --- | --- | --- |
| 0 | a | 0 |

Contribution is 0.

Total is 4.

Now consider "ababa".

For i = 0:

| j | substring | pi[j] |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | ab | 0 |
| 2 | aba | 1 |
| 3 | abab | 2 |
| 4 | ababa | 3 |

Sum is 6.

For i = 1 ("baba") the contributions are 0,0,1,2 giving 3. For i = 2 ("aba") we get 0,0,1 giving 1. Remaining starts contribute 0. Total is 10.

These traces show that each substring is treated exactly once as a prefix of a suffix starting at its left endpoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per string | Each suffix builds a linear prefix-function, and there are n suffixes |
| Space | O(n) | Only one prefix-function array is stored at a time |

With n ≤ 5000 and at most 50 strings, this fits comfortably within time limits, since the total number of operations is on the order of 1.25 × 10^8 in the worst case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve_one(s: str) -> int:
        n = len(s)
        total = 0
        for i in range(n):
            pi = [0] * (n - i)
            for j in range(1, n - i):
                k = pi[j - 1]
                while k > 0 and s[i + j] != s[i + k]:
                    k = pi[k - 1]
                if s[i + j] == s[i + k]:
                    k += 1
                pi[j] = k
                total += k
        return total

    out = []
    for s in sys.stdin.read().split():
        out.append(str(solve_one(s)))
    return "\n".join(out)

# provided-like samples
assert run("a") == "0"
assert run("aa") == "1"
assert run("aaa") == "4"

# custom cases
assert run("abc") == "0", "no repetition"
assert run("aaaa") == str(10), "high repetition"
assert run("ababa") == "10", "overlapping borders"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "abc" | 0 | no border structure anywhere |
| "aaaa" | 10 | strong repetition and cumulative borders |
| "ababa" | 10 | overlapping prefix-suffix chains |

## Edge Cases

For a string like "abcde", every mismatch happens immediately in the prefix-function, so every pi[j] stays zero. The algorithm correctly accumulates zero for all substrings because no suffix shares a non-trivial prefix structure.

For a uniform string like "aaaaa", the prefix-function grows linearly for every suffix. For each starting position i, the contribution is triangular, and the algorithm accumulates these contributions without recomputation. The prefix-function construction ensures that at position j we always count the longest valid border strictly shorter than the substring, never the full substring itself.

For highly overlapping patterns like "ababa", repeated fallback through pi[k-1] correctly captures nested borders such as "a", "aba", and "ababa". Each fallback step preserves the invariant that k is always a valid border length of the current prefix, so no invalid border lengths are ever added.
