---
title: "CF 1245C - Constanze's Machine"
description: "We receive a string that is claimed to be produced by a slightly broken writing machine. The machine normally prints each spoken letter as itself, but two special letters behave differently: if the user says w, the machine writes uu, and if the user says m, it writes nn."
date: "2026-06-15T21:34:46+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1245
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 597 (Div. 2)"
rating: 1400
weight: 1245
solve_time_s: 126
verified: true
draft: false
---

[CF 1245C - Constanze's Machine](https://codeforces.com/problemset/problem/1245/C)

**Rating:** 1400  
**Tags:** dp  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We receive a string that is claimed to be produced by a slightly broken writing machine. The machine normally prints each spoken letter as itself, but two special letters behave differently: if the user says `w`, the machine writes `uu`, and if the user says `m`, it writes `nn`. All other letters are printed unchanged.

We are given a final written string and asked to count how many original spoken strings could have produced it under these rules.

Rephrased, we are trying to decompose the given string into segments, where every `u` might come from either a real `u` or from a hidden `w`, and every `n` might come from either a real `n` or from a hidden `m`. The task is to count all valid decompositions.

The input length can be up to 100,000. Any solution that tries to enumerate all interpretations or do exponential branching will immediately fail because even a small run of repeated characters like `uuuuuu...` would explode into exponential combinations. This forces a linear or near-linear dynamic programming approach.

A subtle edge case is that invalid characters inside a run break all possibilities. For example, if the string contains a character other than `u`, `n`, `w`, or `m`, it is still fine because those letters are fixed, but if the interpretation forces splitting incorrectly, some segments might become impossible. More concretely, consider `"amanda"`. The letter `m` in the original language always produces `"nn"`, so a single standalone `m` in the output can never exist. Any occurrence of `m` in the output string immediately kills all valid interpretations, because no source letter produces a single `m`.

Another important case is short runs. For instance `"u"` has exactly one interpretation, but `"uu"` has two: either `u u` or `w`. For `"uuu"` we already need a recurrence, because overlapping placements of `w` create dependencies.

## Approaches

A brute-force interpretation tries to treat every position as either coming from a normal letter or part of a merged transformation. This quickly becomes a backtracking problem where every run of identical characters `u` or `n` doubles decisions at each step. For a run of length `k`, the number of segmentations corresponds to Fibonacci-like growth, but naive enumeration would still explicitly branch, leading to exponential complexity.

The key observation is that only two letters introduce ambiguity, and both ambiguities are local: `w → uu` and `m → nn`. This means ambiguity only appears in consecutive runs of `u` or `n`. Everything else is fixed one-to-one.

So the string can be processed linearly, compressing it into maximal consecutive runs. For any run of `u` of length `k`, we count how many ways we can split it into pieces of size 1 or 2, since each piece corresponds to either a literal `u` or a hidden `w`. The same applies to runs of `n`.

This is exactly a Fibonacci DP over each run length, multiplied across independent segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal DP (run + Fibonacci) | O(n) | O(n) or O(1) | Accepted |

## Algorithm Walkthrough

We process the string and compress it into consecutive blocks of identical characters.

1. Scan the string from left to right and identify maximal runs of identical characters. Each run is processed independently because no transformation crosses a different character boundary.
2. If we encounter a character `m` or `w` in the final string, we immediately return 0. This is because neither `m` nor `w` can appear as a single printed character in the output; they are always expanded into two-character sequences.
3. For each run of `u` with length `k`, compute the number of ways to partition it into segments of size 1 or 2. A size-1 segment corresponds to a literal `u`, and a size-2 segment corresponds to a hidden `w`.
4. For each run of `n` with length `k`, compute the same type of partition count, since `n` can come either from `n` or from `m`.
5. Multiply the contribution of each run into a global answer modulo $10^9+7$.
6. Use a Fibonacci-style DP where `dp[i]` represents the number of ways to cover a run of length `i`. The transition is `dp[i] = dp[i-1] + dp[i-2]`, because the last segment is either size 1 or size 2.

### Why it works

Each valid interpretation corresponds uniquely to a tiling of every maximal `u` or `n` segment into tiles of length 1 or 2. These tilings are independent across segments because different characters cannot overlap in interpretation. The recurrence exactly counts all binary choices of splitting or merging adjacent characters, and no configuration is counted twice because every tiling corresponds to exactly one decomposition into `u` and `w` (or `n` and `m`).

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

s = input().strip()

# invalid characters that cannot appear in output
# since m and w are always expanded, they never appear alone
for ch in s:
    if ch == 'm' or ch == 'w':
        print(0)
        sys.exit(0)

n = len(s)

# precompute fibonacci up to n
dp = [0] * (n + 1)
dp[0] = 1
if n >= 1:
    dp[1] = 1

for i in range(2, n + 1):
    dp[i] = (dp[i - 1] + dp[i - 2]) % MOD

ans = 1

i = 0
while i < n:
    j = i
    while j < n and s[j] == s[i]:
        j += 1
    length = j - i

    if s[i] == 'u' or s[i] == 'n':
        ans = (ans * dp[length]) % MOD

    i = j

print(ans)
```

The code first rejects impossible cases involving `m` or `w`. It then precomputes Fibonacci numbers because every run of length `k` reduces to a tiling count `dp[k]`. The string is scanned once to extract runs, and each run contributes multiplicatively to the answer.

A common implementation pitfall is forgetting that runs are independent. Another is mixing up which characters are valid singletons. Only `u` and `n` are ambiguous; everything else contributes exactly one way.

## Worked Examples

### Example 1: `ouuokarinn`

We split into runs:

| Segment | Character | Length | Ways |
| --- | --- | --- | --- |
| o | o | 1 | 1 |
| uu | u | 2 | 2 |
| o | o | 1 | 1 |
| k | k | 1 | 1 |
| a | a | 1 | 1 |
| r | r | 1 | 1 |
| i | i | 1 | 1 |
| nn | n | 2 | 2 |

Multiplying: $2 \times 2 = 4$.

This shows how ambiguity only comes from consecutive `u` and `n`, and each contributes independently.

### Example 2: `banana`

Runs:

| Segment | Character | Length | Ways |
| --- | --- | --- | --- |
| b | b | 1 | 1 |
| a | a | 1 | 1 |
| n | n | 1 | 1 |
| a | a | 1 | 1 |
| n | n | 1 | 1 |
| a | a | 1 | 1 |

All segments contribute 1, so result is 1.

This confirms that isolated `n` is valid and has no ambiguity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute DP and one pass to scan runs |
| Space | O(n) | Fibonacci table up to n |

The constraints allow linear time comfortably, and the memory usage stays small even at maximum input size.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve():
    s = input().strip()
    for ch in s:
        if ch == 'm' or ch == 'w':
            print(0)
            return

    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = (dp[i-1] + dp[i-2]) % MOD

    ans = 1
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        length = j - i
        if s[i] in ('u', 'n'):
            ans = (ans * dp[length]) % MOD
        i = j

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("ouuokarinn\n") == "4"

# custom cases
assert run("banana\n") == "1"
assert run("u\n") == "1"
assert run("uu\n") == "2"
assert run("m\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| u | 1 | single ambiguity base case |
| uu | 2 | split vs merge choice |
| m | 0 | invalid output character |
| banana | 1 | no ambiguity chain |

## Edge Cases

A single `m` or `w` in the input immediately forces the answer to zero because no valid original string can produce a standalone `m` or `w`. The algorithm handles this by early termination before any DP work.

A long run of `u` such as `"uuuuuu"` tests whether the Fibonacci preprocessing correctly scales up splitting combinations. The DP ensures each additional character only increases complexity linearly.

Mixed strings like `"uunnnnuu"` test independence of runs. Each block is handled separately, and the multiplication step ensures cross-block combinations are counted correctly without interaction.
