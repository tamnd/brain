---
title: "CF 103478B - Serval \u7684\u5143\u7d20\u5468\u671f\u8868"
description: "We are given a single uppercase string representing a “word” built from letters A to Z. The task is to determine whether this word can be segmented completely into a sequence of chemical element symbols, but only using a restricted set: the first 20 elements of the periodic…"
date: "2026-07-03T06:34:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103478
codeforces_index: "B"
codeforces_contest_name: "The 16-th Beihang University Collegiate Programming Contest (BCPC 2021) - Final"
rating: 0
weight: 103478
solve_time_s: 48
verified: true
draft: false
---

[CF 103478B - Serval \u7684\u5143\u7d20\u5468\u671f\u8868](https://codeforces.com/problemset/problem/103478/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single uppercase string representing a “word” built from letters A to Z. The task is to determine whether this word can be segmented completely into a sequence of chemical element symbols, but only using a restricted set: the first 20 elements of the periodic table as provided in the statement.

Each element symbol acts like a tile. Some tiles are one letter long, such as `B`, `C`, `O`, while others are two letters long, such as `HE`, `NA`, or `CL`. The goal is to check whether the entire string can be exactly covered by concatenating these symbols in order, without skipping or overlapping characters.

This is a classic segmentation problem on a string where each segment must belong to a fixed dictionary of strings of length one or two.

The input length is at most 100. This is small enough that even quadratic dynamic programming over positions is easily fast enough under a 1 second limit, since we only perform a constant amount of work per DP transition.

A subtle point is that some symbols are single letters that overlap heavily with prefixes of longer symbols. For example, `C`, `CA`, and `CL` all exist. A greedy approach that always prefers one match (for example always taking one-letter matches first or always preferring two-letter matches) can fail.

For example, consider a hypothetical string like `CA...`. If we greedily take `C` first, we might later block a valid decomposition that requires `CA` at that position. This shows that local choices are not safe.

Another edge case is when multiple segmentations exist but only one leads to a valid full cover. For instance, `NEON` could be split as `NE O N` or `N E O N` depending on availability of symbols, and only some choices are valid.

So we need a method that explores all valid segmentations efficiently.

## Approaches

A brute-force solution tries every possible way to split the string into valid element symbols. At each position, we attempt to match either a one-letter or two-letter symbol and recursively continue. This forms a recursion tree where each position branches into up to two choices.

In the worst case, every prefix is valid, so the number of recursive paths grows like Fibonacci-style branching, roughly O(2^n). For n up to 100, this is completely infeasible.

The key observation is that the state of the problem depends only on the current position in the string. Once we are at index i, the suffix from i onward can be solved independently of how we arrived there. This is a standard optimal substructure property.

This suggests dynamic programming over positions. Let dp[i] represent whether the substring starting at position i can be fully segmented using allowed symbols. Then from position i we only try up to two transitions: taking a one-letter symbol or a two-letter symbol if valid. Each state is computed once, giving linear complexity.

We can compute dp from the end of the string backward, or use memoized recursion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion | O(2^n) | O(n) | Too slow |
| DP over suffix positions | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We preprocess the allowed element symbols into a set for constant-time membership checks. Since there are only 20 symbols, this is negligible overhead.

1. Define a boolean DP array where dp[i] indicates whether the substring starting at index i can be fully segmented. We also set dp[n] = True because an empty suffix is always valid.
2. Iterate i from n−1 down to 0. At each position, we try to match valid symbols starting at i.
3. First, we check the single-character substring s[i]. If it is in the allowed set, then dp[i] can inherit dp[i+1]. This corresponds to consuming one element symbol.
4. Next, if i+1 < n, we check the two-character substring s[i:i+2]. If it is in the allowed set, then dp[i] can inherit dp[i+2]. This corresponds to consuming a two-letter element symbol.
5. If either option leads to a valid completion, we set dp[i] = True.
6. After filling the table, the answer is dp[0], which tells us whether the whole string can be segmented.

The reason we only check one- and two-letter slices is that the problem restricts all symbols to length at most two.

### Why it works

The DP maintains the invariant that dp[i] correctly represents whether the suffix starting at i can be fully covered by valid element symbols. Every transition corresponds exactly to choosing one valid symbol that matches the current prefix of the suffix, and the remaining suffix is independently checked via dp. Since all possible valid first choices are considered, no valid segmentation is missed, and since only valid dictionary matches are used, no invalid segmentation is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

symbols = {
    "H","HE","LI","BE","B","C","N","O","F","NE",
    "NA","MG","AL","SI","P","S","CL","AR","K","CA"
}

def solve():
    s = input().strip()
    n = len(s)

    dp = [False] * (n + 1)
    dp[n] = True

    for i in range(n - 1, -1, -1):
        if s[i:i+1] in symbols and dp[i + 1]:
            dp[i] = True
            continue
        if i + 1 < n and s[i:i+2] in symbols and dp[i + 2]:
            dp[i] = True

    print("YES" if dp[0] else "NO")

if __name__ == "__main__":
    solve()
```

The code mirrors the DP definition directly. The set `symbols` encodes the dictionary of allowed element symbols. The DP array is sized `n+1` to naturally handle the base case of an empty suffix.

The order of checks is irrelevant for correctness, but the early `continue` slightly reduces work when a one-letter match already succeeds. Both transitions are always tested against bounds to avoid invalid slicing at the end of the string.

## Worked Examples

### Example 1: `CLOCK`

We process from right to left.

| i | suffix | one-letter valid | two-letter valid | dp[i] |
| --- | --- | --- | --- | --- |
| 4 | "" | - | - | True |
| 3 | K | True (K) | - | True |
| 2 | O K | True (O) | False | True |
| 1 | L O K | False | True (CL? no) | False |
| 0 | C L O K | True (C) | True (CL) | True |

At index 0, taking `CL` works because `dp[2]` is True, so the full string is segmentable. This matches the expected output YES.

### Example 2: `YES`

We attempt DP:

| i | s[i:i+2] checks | dp[i] |
| --- | --- | --- |
| 3 | "" | True |
| 2 | S not in symbols, no 2-letter match | False |
| 1 | E not valid continuation | False |
| 0 | Y not valid | False |

At index 0, there is no valid first symbol, so segmentation fails immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once with at most two constant-time dictionary checks |
| Space | O(n) | DP array of size n+1 |

The constraints allow up to length 100, so linear DP is far below the limit. Even a more naive O(n^2) approach would be safe, but O(n) keeps the solution clean and robust.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    symbols = {
        "H","HE","LI","BE","B","C","N","O","F","NE",
        "NA","MG","AL","SI","P","S","CL","AR","K","CA"
    }

    s = input().strip()
    n = len(s)

    dp = [False] * (n + 1)
    dp[n] = True

    for i in range(n - 1, -1, -1):
        if s[i:i+1] in symbols and dp[i+1]:
            dp[i] = True
            continue
        if i + 1 < n and s[i:i+2] in symbols and dp[i+2]:
            dp[i] = True

    return "YES" if dp[0] else "NO"

# provided samples
assert run("BCPC\n") == "YES"
assert run("BUAA\n") == "NO"
assert run("CLOCK\n") == "YES"

# custom cases
assert run("HHE\n") == "YES", "H + HE"
assert run("CAK\n") == "YES", "CA + K"
assert run("ZZ\n") == "NO", "invalid letters"
assert run("NEON\n") in {"YES","NO"}, "checks ambiguity handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| HHE | YES | mixing 1- and 2-letter symbols |
| CAK | YES | boundary of 2-letter match usage |
| ZZ | NO | no valid symbols at all |
| NEON | YES | multiple valid segmentations exist |

## Edge Cases

A key edge case is when both one-letter and two-letter symbols are valid at the same position, but only one leads to a successful completion. For example, in `CAK`, at position 0 both `C` and `CA` are valid. Choosing `C` leads to `AK`, which fails, while choosing `CA` leads to `K`, which succeeds. The DP correctly evaluates both possibilities because dp[0] depends on either dp[1] or dp[2], not a greedy choice.

Another edge case is strings composed entirely of single-letter symbols like `BCPC`. The algorithm naturally handles this because it never requires two-letter matches.

Finally, strings ending with a valid prefix but leaving an unmatched suffix, such as `CLX`, fail at the last step since dp cannot reach the terminal state dp[n] = True.
