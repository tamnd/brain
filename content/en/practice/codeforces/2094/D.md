---
title: "CF 2094D - Tung Tung Sahur"
description: "We are given a recorded sequence of intended drum hits, where each character is either a left hit or a right hit. Each intended hit does not produce a fixed sound length."
date: "2026-06-08T05:34:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2094
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1017 (Div. 4)"
rating: 1100
weight: 2094
solve_time_s: 66
verified: true
draft: false
---

[CF 2094D - Tung Tung Sahur](https://codeforces.com/problemset/problem/2094/D)

**Rating:** 1100  
**Tags:** greedy, strings, two pointers  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a recorded sequence of intended drum hits, where each character is either a left hit or a right hit. Each intended hit does not produce a fixed sound length. Instead, a single hit may be heard as either one character or two identical characters in the final recorded sound.

So each character in the original sequence expands independently into a short block: a left hit becomes either one “L” or two “L”s, and a right hit becomes either one “R” or two “R”s. After all expansions, the resulting string is concatenated into the observed sound string.

The task is to decide whether a given observed string can be produced from the intended sequence under these rules.

The constraints are large enough that any quadratic or backtracking approach over all expansions is infeasible. The total length across all test cases is up to 200000, so the solution must process each character in linear time overall.

A naive pitfall appears when trying to match character by character without respecting grouping. For example, if p = "LR" and s = "LLRL", a greedy per-character check might accept partial matches too early and fail to detect that the second group cannot align cleanly.

Another common failure case is over-consuming characters in s for a single character in p. For instance, if p has a single 'L', consuming three consecutive 'L's in s is impossible, but a careless pointer implementation might not detect the boundary between groups.

The key difficulty is that we must respect grouping: each character in p corresponds to a contiguous block in s of length 1 or 2, and blocks cannot merge across different characters.

## Approaches

A brute-force idea would be to treat each character in p and branch into two choices: expand it as one character or two characters, then simulate the resulting string and compare with s. This creates an exponential number of possibilities, up to 2^{|p|}, which is impossible even for moderate input sizes.

The structure of the problem suggests a greedy matching strategy instead of enumeration. Since each character in p produces a contiguous block of identical characters in s, we can scan both strings from left to right and match groups.

The key observation is that both p and s can be compressed into runs of equal characters. Each run in p must correspond to a run in s of the same character, and the run length in s must be between the run length in p and twice that run length, since each character expands independently to length 1 or 2.

Thus, the problem reduces to comparing run lengths in order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Run-length greedy matching | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compress both strings p and s into sequences of runs, where each run is a pair (character, length). This is necessary because expansions preserve adjacency, so only run boundaries matter.
2. If the number of runs in p and s differ, immediately return NO. Each hit produces exactly one run, so mismatch in structure cannot be fixed by expansion.
3. Iterate over corresponding runs in p and s in order.
4. For each pair of runs, check that the characters match. If they differ, return NO immediately since expansion never changes characters.
5. Let the run length in p be x and in s be y. Since each character in p becomes either 1 or 2 characters, the total expansion of a run of x identical hits must satisfy x ≤ y ≤ 2x.
6. If any run violates this inequality, return NO.
7. If all runs satisfy the condition, return YES.

### Why it works

Each character in p expands independently but preserves order, so the final string is exactly a concatenation of blocks corresponding one-to-one with p’s runs. Within each run, each original character contributes either 1 or 2 identical characters, meaning the run length can only vary within a fixed interval without affecting neighboring runs. Since runs cannot merge or split across different characters, validating each run independently is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compress(s):
    runs = []
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        runs.append((s[i], j - i))
        i = j
    return runs

t = int(input())
for _ in range(t):
    p = input().strip()
    s = input().strip()

    rp = compress(p)
    rs = compress(s)

    if len(rp) != len(rs):
        print("NO")
        continue

    ok = True
    for (cp, lp), (cs, ls) in zip(rp, rs):
        if cp != cs:
            ok = False
            break
        if ls < lp or ls > 2 * lp:
            ok = False
            break

    print("YES" if ok else "NO")
```

The compression step ensures we only compare meaningful structure instead of individual characters. Each run is stored as a character and its frequency.

The main loop then enforces the structural constraints: same run pattern and valid expansion bounds. The check `ls < lp or ls > 2 * lp` directly encodes the allowed behavior of each hit expanding independently.

## Worked Examples

### Example 1

Input:

p = "LR", s = "LLRR"

| Step | p run | s run | Check |
| --- | --- | --- | --- |
| 1 | L:1 | L:2 | 1 ≤ 2 ≤ 2  |
| 2 | R:1 | R:2 | 1 ≤ 2 ≤ 2  |

All runs match, so output is YES.

This demonstrates the case where every hit expands maximally.

### Example 2

Input:

p = "LRLR", s = "LRLR"

| Step | p run | s run | Check |
| --- | --- | --- | --- |
| 1 | L:1 | L:1 |  |
| 2 | R:1 | R:1 |  |
| 3 | L:1 | L:1 |  |
| 4 | R:1 | R:1 |  |

All runs satisfy constraints, so YES.

This shows minimal expansion where every hit is single-length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited once during compression and once during comparison |
| Space | O(n) | Run storage in worst case when no compression is possible |

The total input size is bounded by 2×10^5 across all test cases, so a linear solution comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def compress(s):
        runs = []
        i = 0
        n = len(s)
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append((s[i], j - i))
            i = j
        return runs

    t = int(input())
    out = []
    for _ in range(t):
        p = input().strip()
        s = input().strip()

        rp = compress(p)
        rs = compress(s)

        if len(rp) != len(rs):
            out.append("YES" if False else "NO")
            continue

        ok = True
        for (cp, lp), (cs, ls) in zip(rp, rs):
            if cp != cs or ls < lp or ls > 2 * lp:
                ok = False
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
R
RR
LRLR
LRLR
LR
LLLR
LLLLLRL
LLLLRRLL
LLRLRLRRL
LLLRLRRLLRRRL
""") == """YES
YES
NO
NO
YES"""

# custom cases
assert run("""3
L
LL
R
RRR
LR
LRRR
""") == """YES
NO
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| L vs LL | YES | maximum expansion of single run |
| R vs RRR | NO | invalid expansion exceeding 2× |
| LR vs LRRR | NO | mismatched run structure |

## Edge Cases

One edge case is when s has extra repetition inside a run that still looks locally valid but globally breaks alignment. For example, p = "LR" and s = "LLLR". The compression yields p runs [(L,1),(R,1)] and s runs [(L,3),(R,1)]. The first run fails the constraint because 3 > 2 × 1, so the answer is NO. The algorithm catches this immediately during the run comparison.

Another edge case is when s has fewer runs than p due to merging across boundaries being impossible under the rules. For example, p = "LRL" and s = "LLRR". Compression gives p as three runs but s as two runs, so the algorithm rejects immediately. This ensures we never incorrectly allow cross-character merging.
