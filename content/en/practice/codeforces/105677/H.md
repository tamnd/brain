---
title: "CF 105677H - The king of SWERC"
description: "We are given a sequence of names representing votes in an election. Each line corresponds to one vote for a candidate, and each candidate is identified by a single uppercase string. The task is to determine which candidate received strictly more votes than every other candidate."
date: "2026-06-22T05:07:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105677
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC Southwestern European Regional Contest (SWERC 2024)"
rating: 0
weight: 105677
solve_time_s: 43
verified: true
draft: false
---

[CF 105677H - The king of SWERC](https://codeforces.com/problemset/problem/105677/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of names representing votes in an election. Each line corresponds to one vote for a candidate, and each candidate is identified by a single uppercase string. The task is to determine which candidate received strictly more votes than every other candidate.

The important structural detail is that the input guarantees a unique winner. This removes the need to reason about ties or secondary rules. We only need to identify the name with the highest frequency.

The constraints are small, with at most 500 votes and each name having length at most 20. This immediately suggests that even straightforward counting strategies will work comfortably. A solution that is linear in the number of votes, or even quadratic in the worst case, would still be acceptable. However, since the input size is tiny, the cleanest approach is to use a frequency map.

A subtle edge case that often trips naive implementations is forgetting that names repeat in arbitrary order and may not be grouped. For example, an input like

JON

JOFFREY

TYWIN

JON

requires aggregating counts across non-adjacent positions. Any approach that only checks consecutive duplicates would fail here. Another potential pitfall is assuming lexicographic order plays any role, but it is irrelevant because voting frequency is the only deciding factor.

## Approaches

The brute-force idea is to treat each name as a candidate and scan the entire list to count how many times it appears. For every vote, we recompute its total frequency by iterating over all votes again. This is correct because it directly evaluates the definition of “most frequent”, but it performs redundant work. If there are N votes, we perform O(N) counting work for each of the N entries, leading to O(N²) operations.

Given N ≤ 500, this is still numerically small, but it is structurally inefficient and unnecessary. The key observation is that frequency counting does not need repeated scans. We only need to aggregate counts once. A hash map or dictionary allows us to accumulate frequencies in a single pass, updating counts as we read each vote. After that, we simply find the maximum.

This reduces repeated work into a single linear traversal followed by another linear scan over the distinct names.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Accepted but redundant |
| Frequency Map | O(N) | O(K) | Accepted |

Here K is the number of distinct names.

## Algorithm Walkthrough

1. Initialize an empty dictionary to store vote counts keyed by candidate name. This structure represents accumulated knowledge about the election as we process votes sequentially.
2. Read each vote one by one. For each name, increment its count in the dictionary. If the name is not yet present, initialize its count to 1. This step ensures that every vote is accounted for exactly once.
3. Maintain variables to track the current best candidate and their vote count. As we update counts, we can either recompute the maximum at the end or update it incrementally. The simplest and least error-prone approach is to compute it after building the frequency table.
4. After processing all votes, iterate over the dictionary entries and select the name with the maximum frequency. Because the problem guarantees a unique winner, we do not need tie-breaking logic.

### Why it works

At any point during processing, the dictionary stores the exact number of occurrences of each name seen so far. Since every vote is processed exactly once and only increments a single counter, no information is lost or double counted. After all votes are processed, the frequency table is an exact representation of the dataset. Selecting the maximum value over this table is therefore equivalent to selecting the most frequent name in the original input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    
    freq = {}
    
    for _ in range(n):
        name = input().strip()
        freq[name] = freq.get(name, 0) + 1
    
    best_name = ""
    best_count = -1
    
    for name, cnt in freq.items():
        if cnt > best_count:
            best_count = cnt
            best_name = name
    
    print(best_name)

if __name__ == "__main__":
    solve()
```

The solution uses a dictionary keyed by strings to accumulate counts. Each input line is stripped to remove newline characters. The `.get()` method avoids explicit existence checks. After reading all votes, we perform a final scan over dictionary entries to find the maximum.

A subtle implementation detail is initializing `best_count` to -1, ensuring that even a single vote correctly updates the answer.

## Worked Examples

### Example 1

Input:

```
1
RAMSES
```

| Step | Vote | Frequency Map | Best Candidate |
| --- | --- | --- | --- |
| 1 | RAMSES | {RAMSES: 1} | RAMSES |

The single vote immediately determines the winner since there are no competing candidates.

This confirms that the algorithm handles the minimum input size correctly without requiring special casing.

### Example 2

Input:

```
4
JON
JOFFREY
TYWIN
JON
```

| Step | Vote | Frequency Map | Best Candidate |
| --- | --- | --- | --- |
| 1 | JON | {JON: 1} | JON |
| 2 | JOFFREY | {JON: 1, JOFFREY: 1} | JON (tie, first seen) |
| 3 | TYWIN | {JON: 1, JOFFREY: 1, TYWIN: 1} | JON |
| 4 | JON | {JON: 2, JOFFREY: 1, TYWIN: 1} | JON |

After all updates, JON has the highest frequency.

This example shows that repeated non-consecutive votes are correctly aggregated, and that ties during intermediate steps do not affect correctness since final selection happens after full processing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass to build frequencies and one pass over distinct names |
| Space | O(K) | Storage for counts of K unique names |

The constraints allow up to 500 votes, so even the overhead of dictionary operations is negligible. The solution is comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    
    input = _sys.stdin.readline
    
    n = int(input().strip())
    freq = {}
    
    for _ in range(n):
        name = input().strip()
        freq[name] = freq.get(name, 0) + 1
    
    best_name = ""
    best_count = -1
    
    for name, cnt in freq.items():
        if cnt > best_count:
            best_count = cnt
            best_name = name
    
    return best_name + "\n"

# provided samples
assert run("1\nRAMSES\n") == "RAMSES\n"
assert run("4\nJON\nJOFFREY\nTYWIN\nJON\n") == "JON\n"

# custom cases
assert run("3\nA\nB\nA\n") == "A\n"
assert run("5\nZ\nZ\nZ\nY\nX\n") == "Z\n"
assert run("2\nALICE\nBOB\nALICE\n") == "ALICE\n"
assert run("1\nKING\n") == "KING\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 KING | KING | Minimum size input |
| A B A | A | Basic repetition handling |
| Z Z Z Y X | Z | Dominant frequency case |
| ALICE BOB ALICE | ALICE | Non-adjacent duplicates |

## Edge Cases

A key edge case is when the winner appears in separated positions rather than being grouped. For example, in the input

```
3
A
B
A
```

the dictionary evolves as `{A: 1}`, `{A: 1, B: 1}`, `{A: 2, B: 1}`. The final maximum correctly identifies A, even though it is not contiguous. Any approach relying on adjacency would incorrectly treat this as two unrelated A segments.

Another edge case is the smallest possible input:

```
1
KING
```

The frequency table becomes `{KING: 1}` immediately. The maximum selection step simply returns KING, showing that no special logic is required for degenerate cases.

Finally, a case where all names are identical, such as

```
4
A
A
A
A
```

produces a single dictionary entry `{A: 4}`. The algorithm naturally handles this without ambiguity, and the maximum remains consistent throughout all steps.
