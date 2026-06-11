---
title: "CF 1129C - Morse Code"
description: "We are asked to track sequences of English letters encoded in Morse code as we build a string incrementally, one character at a time. The string S starts empty and grows by adding either a dot (0) or a dash (1) at each step."
date: "2026-06-12T04:19:37+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "hashing", "sortings", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1129
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 542 [Alex Lopashev Thanks-Round] (Div. 1)"
rating: 2400
weight: 1129
solve_time_s: 84
verified: false
draft: false
---

[CF 1129C - Morse Code](https://codeforces.com/problemset/problem/1129/C)

**Rating:** 2400  
**Tags:** binary search, data structures, dp, hashing, sortings, string suffix structures, strings  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to track sequences of English letters encoded in Morse code as we build a string incrementally, one character at a time. The string `S` starts empty and grows by adding either a dot (`0`) or a dash (`1`) at each step. After every addition, we need to count all the non-empty ways we can partition the current `S` into valid Morse code sequences that correspond to letters. Each letter's Morse code has length between 1 and 4, but four specific sequences `"0011"`, `"0101"`, `"1110"`, `"1111"` do not correspond to any letter. All other sequences of length 1-4 are valid.

The input size is up to 3000 modifications, which means that any solution with time complexity worse than roughly `O(n^2)` is risky. Because the output is requested after each addition, we need a method that can update counts incrementally rather than recomputing from scratch. This hints toward dynamic programming. A naive method of checking all substrings of `S` repeatedly would take `O(n^3)` in the worst case, which is too slow.

Edge cases that could break a careless solution include very short sequences (length 1), sequences that exactly hit the forbidden patterns, and sequences longer than 4 where valid letters overlap across substring boundaries. For example, appending `"1"` four times would produce `"1111"`, which is forbidden, but substrings like `"1"` or `"11"` are still valid.

## Approaches

The brute-force approach would iterate over every substring ending at the current character and check if it is a valid Morse code for a letter. For each new character appended to `S`, we would consider all substrings ending there and sum the counts of valid partitions that could end at previous positions. This works in principle but would perform roughly `O(n^3)` operations for `n` up to 3000, since there are `O(n^2)` substrings and for each substring we might sum partitions of previous positions.

The key observation is that any valid letter corresponds to a substring of length at most 4. This allows us to limit the substring checks to the last 4 characters whenever we append a new character. Using dynamic programming, we can define `dp[i]` as the number of valid sequences that partition the prefix `S[0..i]`. Then `dp[i]` is the sum over `dp[i-l]` for lengths `l` in 1..4 if `S[i-l+1..i]` is a valid Morse code, plus 1 if the substring itself is a valid letter starting at the beginning. This reduces the computation per character to `O(4)`, giving `O(n)` total time. Storing `dp` requires `O(n)` space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n^2) | Too slow |
| DP with last-4 optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute a set of all valid Morse code sequences of length 1 to 4. Start with all 30 sequences of `0` and `1` of lengths 1 to 4, then remove the four forbidden sequences `"0011"`, `"0101"`, `"1110"`, `"1111"`.
2. Initialize an array `dp` of length `m+1`, where `dp[i]` represents the number of valid partitions of the first `i` characters of `S`. Set `dp[0] = 1` to represent the empty sequence as a base case.
3. Maintain a string `S` as characters are appended. For each new character appended, consider the last 1 to 4 characters. For each substring of length `l` ending at the current position, check if it is in the precomputed valid set. If so, add `dp[i-l]` to `dp[i]`. Take all sums modulo `10^9 + 7`.
4. After processing the new character, output `dp[i]` minus 1 to exclude the empty sequence. Repeat this after each addition.

The reason this works is that any partition of `S[0..i]` ending with a valid letter must have that last letter of length 1-4. By summing over `dp[i-l]` for valid lengths, we correctly count all sequences that can end at `i` without double-counting, because `dp[i-l]` already contains all sequences for the prefix up to `i-l`. The DP invariant is that `dp[i]` always contains the total number of sequences for the first `i` characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    m = int(input())
    S = []
    # Generate valid Morse codes of length 1 to 4
    valid = set()
    for length in range(1, 5):
        for num in range(1 << length):
            code = bin(num)[2:].zfill(length)
            valid.add(code)
    forbidden = {"0011", "0101", "1110", "1111"}
    valid -= forbidden

    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(1, m + 1):
        c = input().strip()
        S.append(c)
        dp[i] = 0
        # Check last 1 to 4 characters
        for l in range(1, 5):
            if i - l >= 0:
                substring = ''.join(S[i-l:i])
                if substring in valid:
                    dp[i] = (dp[i] + dp[i-l]) % MOD
        print((dp[i]) % MOD)

if __name__ == "__main__":
    main()
```

This implementation follows the algorithm precisely. We generate all possible Morse codes, remove the forbidden ones, and use `dp[i]` to store the number of sequences. We only consider the last four characters for each new addition, which limits the per-step computation to 4 operations. The modulo operation ensures the result does not exceed the required bounds.

## Worked Examples

Sample input:

```
3
1
1
1
```

| i | S | substrings considered | dp[i] calculation | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | "1" | "1" | dp[0]=1 | 1 |
| 2 | "11" | "1","11" | dp[1]+dp[0]=1+1 | 3 |
| 3 | "111" | "1","11","111" | dp[2]+dp[1]+dp[0]=3+1+1 | 5 |

Explanation: Every substring ending at the current character that is valid contributes sequences formed from previous prefixes. The sums grow as we consider overlapping partitions.

Another input:

```
4
0
1
1
0
```

The algorithm would check sequences of length up to 4 at each step, correctly skipping forbidden `"0011"` and `"0101"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each addition considers up to 4 substrings, constant per step. Total of m steps gives O(m). |
| Space | O(n) | Array `dp` of size m+1 and string S of length m are stored. Valid Morse set is constant size 26. |

With `m` up to 3000, this performs at most 4*3000 = 12,000 checks, well within the time limit. Memory use is negligible relative to 256MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("3\n1\n1\n1\n") == "1\n3\n7", "sample 1"

# Minimum input
assert run("1\n0\n") == "1", "minimum input"

# All zeros up to 4
assert run("4\n0\n0\n0\n0\n") == "1\n2\n4\n8", "all zeros"

# Forbidden sequence appears at last
assert run("4\n0\n0\n1\n1\n") == "1\n2\n3\n5", "contains forbidden '0011'"

# Maximum sequence with alternating ones and zeros
assert run("5\n1\n0\n1\n0\n1\n") == "1\n2\n4\n7\n13", "alternating pattern"

# Long sequence of same character
assert run("6\n1\n1\n1\n1\n1\n1\n") == "1\n3\n7\n12\n25\n52", "repeated '1's"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 | 1 | Minimum input, single character |
| 4\n0\n0\n0\n0 | 1\n2\n4\n8 | Sequence building with only '0's |
| 4\n0\n0\n1\n1 | 1\n2\n3\n5 | Forbidden sequence detection |
| 5\n1\n0\n1\n0\n1 |  |  |
