---
title: "CF 1873A - Short Sort"
description: "We are given three distinct cards labeled a, b, and c, arranged in some order. Our goal is to determine whether, using at most one swap of two cards, we can transform the row into the ordered sequence abc."
date: "2026-06-08T23:12:44+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1873
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 898 (Div. 4)"
rating: 800
weight: 1873
solve_time_s: 79
verified: true
draft: false
---

[CF 1873A - Short Sort](https://codeforces.com/problemset/problem/1873/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three distinct cards labeled `a`, `b`, and `c`, arranged in some order. Our goal is to determine whether, using at most one swap of two cards, we can transform the row into the ordered sequence `abc`. Each test case consists of a string of length three containing exactly these three letters in some permutation. The output for each case is "YES" if the ordered sequence can be obtained and "NO" otherwise.

Because there are only three elements, the total number of permutations is six. This means we can reason about the problem exhaustively, but we should also understand the exact conditions under which a single swap is sufficient. A swap either fixes one misplaced pair or is unnecessary if the sequence is already `abc`. The constraints are tiny: with up to six test cases, each involving only three letters, any reasonable approach will run in negligible time. Edge cases include the sequence already being sorted (`abc`), sequences that are impossible to fix with one swap (`bca` or `cab`), and sequences that are one swap away (`acb`, `bac`, `cba`).

A naive implementation might incorrectly assume that swapping any two letters is always sufficient. For instance, `bca` cannot become `abc` with a single swap. Checking only the count of misplaced letters would lead to false positives here. The algorithm must consider the positions of each character relative to the target `abc`.

## Approaches

A brute-force approach would explicitly try all possible pairs of positions to swap and then check if the result matches `abc`. With three letters, there are three possible swaps: positions 0 and 1, positions 0 and 2, and positions 1 and 2. After each swap, we compare the string to `abc`. If any swap yields the target, we print "YES"; otherwise, "NO". This is correct because we cover all possible single-swap operations, and it runs in constant time given the fixed input size. The drawback is that this approach does not scale to larger arrays, but here it is acceptable.

The key observation to simplify further is that a permutation of three letters is at most one swap away from `abc` if and only if it is either already `abc` or it has the first and last letters swapped (`acb`, `bac`, `cba`). Sequences `bca` and `cab` require two swaps and cannot be fixed in one operation. By checking the string against these patterns, we can decide the answer in a single comparison, which is effectively O(1) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all swaps) | O(1) | O(1) | Accepted |
| Pattern Check (check against solvable permutations) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the three-character string representing the card sequence.
3. Check if the string is exactly `abc`. If so, print "YES" and continue.
4. Otherwise, check if the string matches one of the three permutations that can become `abc` with one swap: `acb`, `bac`, `cba`. If it does, print "YES".
5. If none of these conditions are met, print "NO". These are the sequences `bca` and `cab`, which require two swaps.
6. Repeat steps 2-5 for all test cases.

Why it works: For a three-element permutation, any string either already matches the target, can be fixed by swapping exactly two elements, or requires more than one swap. The three patterns we check cover all cases that are solvable with one swap, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    if s == "abc" or s in {"acb", "bac", "cba"}:
        print("YES")
    else:
        print("NO")
```

The code first reads the number of test cases. For each test case, we read the string, strip any whitespace, and compare it to the target `abc`. If the string matches `abc` or is one swap away (`acb`, `bac`, `cba`), we print "YES". Otherwise, we print "NO". Using a set for the one-swap patterns allows for efficient membership checking.

## Worked Examples

Consider the input string `acb`.

| Step | s | Check | Output |
| --- | --- | --- | --- |
| 1 | "acb" | s == "abc"? No | - |
| 2 | "acb" | s in {"acb", "bac", "cba"}? Yes | YES |

We detect that `acb` can become `abc` by swapping the last two characters.

Consider `bca`:

| Step | s | Check | Output |
| --- | --- | --- | --- |
| 1 | "bca" | s == "abc"? No | - |
| 2 | "bca" | s in {"acb", "bac", "cba"}? No | NO |

`bca` requires two swaps, so the algorithm correctly outputs "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves a constant number of string comparisons, and t ≤ 6. |
| Space | O(1) | Only the input string and a small set of patterns are stored. |

The solution fits well within the problem constraints. Each operation is trivial, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        s = input().strip()
        if s == "abc" or s in {"acb", "bac", "cba"}:
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("6\nabc\nacb\nbac\nbca\ncab\ncba\n") == "YES\nYES\nYES\nNO\nNO\nYES", "sample 1"

# custom cases
assert run("2\nabc\nbca\n") == "YES\nNO", "already sorted and impossible"
assert run("1\ncba\n") == "YES", "reverse order solvable by one swap"
assert run("1\ncab\n") == "NO", "cannot solve in one swap"
assert run("3\nacb\nbac\nabc\n") == "YES\nYES\nYES", "all one-swap or sorted cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| abc | YES | Already sorted sequence |
| bca | NO | Requires two swaps, impossible |
| cba | YES | Reverse order, solvable with one swap |
| cab | NO | One-swap solution not possible |
| acb, bac, abc | YES | Confirms detection of one-swap patterns |

## Edge Cases

The algorithm handles the edge case of an already sorted sequence `abc` by explicitly checking for equality first. For `bca` and `cab`, the algorithm correctly identifies that no single swap can fix the sequence, outputting "NO". For `cba`, which is reversed, the algorithm detects it as a one-swap case, outputting "YES". The decision to use a set for one-swap permutations ensures that all solvable permutations are captured without missing any valid configuration.
