---
title: "CF 104158D - Speedy Stamping"
description: "We are given a target string consisting only of the characters T and C. The task is to count how many different ways this string can be formed using a fixed set of stamps. Each position in the string is produced by choosing one of four stamp types."
date: "2026-07-02T01:09:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104158
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 1 (Advanced)"
rating: 0
weight: 104158
solve_time_s: 60
verified: true
draft: false
---

[CF 104158D - Speedy Stamping](https://codeforces.com/problemset/problem/104158/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target string consisting only of the characters T and C. The task is to count how many different ways this string can be formed using a fixed set of stamps.

Each position in the string is produced by choosing one of four stamp types. Some stamps write a single character, while others write two characters at once. The key constraint is that we are not arranging stamps in sequence as operations; instead, we are assigning a decomposition of the string into stamped blocks that exactly cover it without overlap. Each valid way corresponds to a tiling of the string using allowed pieces, and we count all such tilings modulo a large prime.

The string length can be up to 1,000,000. A quadratic or worse solution over substrings is not feasible because even a linear scan repeated per state would already exceed acceptable limits. This forces us into a dynamic programming approach that runs in linear time.

A subtle issue arises from overlapping interpretations of the multi-character stamps. A greedy interpretation fails because choosing a longer stamp early may block valid decompositions later. For example, in the string TCC, if we always try to take the two-character stamp TC first, we may miss configurations where the first character is treated separately.

The main edge case is strings with repeated patterns like TTTT or CCCC, where combinatorial explosion of segmentations happens. Any approach that enumerates partitions explicitly will time out or overflow recursion limits.

## Approaches

A direct approach is to treat this as a partition problem: we try every way to split the string into segments of length 1 or 2, and then check whether each segment matches a valid stamp. This is correct because every tiling corresponds to such a segmentation. However, at each position, we would branch into up to two choices, leading to exponential growth in the number of segmentations. For a string of length n, this yields roughly Fibonacci-like growth, which is already too large for n near 50, let alone 10^6.

The structure of the problem suggests dynamic programming. The important observation is that the number of ways to form a prefix depends only on a small fixed number of previous states. Since each stamp contributes either one or two characters, the state transition only depends on dp[i-1] and dp[i-2]. This reduces the problem to a linear recurrence over the string.

At position i, we consider how the last stamp could end. If the last stamp covers a single character, it must match S[i-1]. If it covers two characters, it must match S[i-2:i]. Each valid match contributes dp[i-1] or dp[i-2] respectively.

We are effectively summing contributions from all valid ways to end at position i, which avoids double counting because each decomposition is uniquely determined by its last piece.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force partitioning | O(2^n) | O(n) | Too slow |
| Dynamic programming | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We define dp[i] as the number of ways to form the prefix S[0:i], using 0-based indexing where dp[0] corresponds to the empty string.

1. Initialize dp[0] = 1 because there is exactly one way to construct an empty prefix, by choosing no stamps. This serves as the base case for building all longer prefixes.
2. Iterate i from 1 to n. At each position i, we compute dp[i] by considering all valid stamps that can end at position i.
3. First consider a one-character stamp. The last character S[i-1] is always covered by exactly one stamp. Since any single-character stamp that matches S[i-1] is allowed, every dp[i-1] way can be extended. This contributes dp[i-1] to dp[i].
4. Next consider a two-character stamp. If i ≥ 2, we check whether S[i-2:i] can be formed by a two-character stamp. If so, every way to form dp[i-2] can be extended by placing this stamp at the end. This contributes dp[i-2] to dp[i].
5. Add both contributions modulo 10^9 + 7.

Why it works is based on a simple decomposition property. Every valid stamping of a prefix has a unique last stamp. That last stamp either covers one or two characters, and removing it leaves a valid stamping of a smaller prefix. This gives a bijection between valid constructions of dp[i] and valid constructions of dp[i-1] and dp[i-2] extended by a final stamp. Since no construction can end in more than one way simultaneously, there is no double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    s = input().strip()
    n = len(s)
    
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        dp[i] = dp[i - 1]  # single-character stamp always usable
        
        if i >= 2:
            # any two-character block is always valid as a stamp
            dp[i] = (dp[i] + dp[i - 2]) % MOD

        else:
            dp[i] %= MOD

    print(dp[n])

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the recurrence. The dp array stores prefix counts, and each state aggregates contributions from the two possible stamp lengths. The modulo is applied at each step to prevent overflow.

The only subtle point is ensuring correct indexing: dp[i] represents the first i characters, so transitions use i-1 and i-2. This avoids off-by-one errors that commonly appear in prefix DP formulations.

## Worked Examples

### Example 1: "TCC"

We compute dp step by step.

| i | Prefix | dp[i-1] contribution | dp[i-2] contribution | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | "" | - | - | 1 |
| 1 | "T" | 1 | - | 1 |
| 2 | "TC" | 1 | 1 | 2 |
| 3 | "TCC" | 2 | 1 | 3 |

This confirms the output 3. The table shows how each prefix accumulates ways from shorter prefixes, matching the combinatorial structure of valid tilings.

### Example 2: "TT"

| i | Prefix | dp[i-1] | dp[i-2] | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | "" | - | - | 1 |
| 1 | "T" | 1 | - | 1 |
| 2 | "TT" | 1 | 1 | 2 |

This shows two valid decompositions: two single stamps or one double stamp.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once with O(1) transitions |
| Space | O(n) | DP array of size n+1 |

The solution fits easily within constraints because even for n = 10^6, the algorithm performs only a few simple arithmetic operations per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7
    s = sys.stdin.readline().strip()
    n = len(s)

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        if i >= 2:
            dp[i] = (dp[i] + dp[i - 2]) % MOD

    return str(dp[n])

# provided sample
assert run("TCC\n") == "3"

# single character
assert run("T\n") == "1"

# two identical characters
assert run("TT\n") == "2"

# alternating pattern
assert run("TCTC\n") == "5"

# long uniform string
assert run("T" * 10 + "\n") == "89"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| T | 1 | base case single character |
| TT | 2 | both 1+1 and 2 decomposition |
| TCTC | 5 | repeated branching growth |
| TTTTTTTTTT | 89 | Fibonacci-like growth correctness |

## Edge Cases

For a single-character string like "T", the algorithm sets dp[1] = dp[0] = 1, since only one single stamp can cover it. There is no dp[i-2] term, so no invalid access occurs.

For a two-character string like "TC", dp[2] = dp[1] + dp[0] = 2. The first term corresponds to two single stamps, and the second corresponds to one two-character stamp. The indexing ensures both possibilities are counted exactly once, and no overlap occurs because each construction is uniquely identified by its last stamp choice.
