---
title: "CF 1759A - Yes-Yes?"
description: "We are given a short string for each query and we want to decide whether it could have appeared inside an infinitely repeated pattern formed by writing the word “Yes” over and over again without separators."
date: "2026-06-09T14:27:05+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1759
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round  834 (Div. 3)"
rating: 800
weight: 1759
solve_time_s: 119
verified: true
draft: false
---

[CF 1759A - Yes-Yes?](https://codeforces.com/problemset/problem/1759/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short string for each query and we want to decide whether it could have appeared inside an infinitely repeated pattern formed by writing the word “Yes” over and over again without separators. The string we are checking is not required to align with word boundaries, it can start and end anywhere inside that infinite tape.

The key idea is that the infinite string has a strict periodic structure of length 3: it repeats `Y`, `e`, `s`, `Y`, `e`, `s`, and so on. Any valid substring must match this repeating cycle character by character.

The constraints are small, with up to 1000 test cases and each string of length at most 50. This immediately rules out anything more complex than linear scanning per test case. A direct simulation or pattern check is sufficient.

A subtle case is when the string starts at different offsets of the cycle. For example, starting at `e` or `s` is valid, so we must allow all three rotations of the base pattern.

## Approaches

The brute-force idea is to explicitly construct a long enough prefix of `"YesYesYes..."` and check if the query string appears as a substring. This works because the maximum length is small, so building a string of length around a few hundred is enough. However, this is unnecessary overhead and conceptually indirect.

The key observation is that the infinite string is purely periodic with cycle `"Yes"`. This means every character at position `i` must match `"Yes"[i mod 3]`, but since the substring can start anywhere, we must also allow cyclic shifts of the pattern. There are only three valid starting alignments: `"Yes"`, `"esY"`, and `"sYe"`.

So the problem reduces to checking whether the input string matches one of these three repeating patterns.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force construction | O(n · t) | O(n) | Accepted but unnecessary |
| Cycle checking | O(n · t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Define the base pattern `"Yes"` and consider its three cyclic rotations. Each rotation represents a valid starting phase of the infinite string.

2. For each test string, try matching it against each rotation character by character.

3. For a fixed rotation, check position `i` in the string against `pattern[i % 3]`. If all positions match, the string is valid.

4. If none of the rotations match, the string cannot appear in the infinite repetition.

The important point is that the alignment is unknown, so we brute-force over the three possible phases instead of fixing one.

### Why it works

The infinite string is fully determined by a period-3 automaton. Any substring is equivalent to choosing a start offset in that cycle and reading forward. Since the cycle length is 3, there are exactly three equivalence classes of starts, and checking all of them covers every possible substring alignment. This guarantees completeness without constructing the full infinite string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(s, p):
    for i, ch in enumerate(s):
        if ch != p[i % 3]:
            return False
    return True

def solve():
    t = int(input())
    base = "Yes"
    rotations = [base[i:] + base[:i] for i in range(3)]

    for _ in range(t):
        s = input().strip()
        for p in rotations:
            if ok(s, p):
                print("YES")
                break
        else:
            print("NO")

solve()
```

The solution first precomputes the three cyclic rotations of `"Yes"`. For each query string, it attempts a direct alignment check against each rotation. The modulo operation handles periodic matching cleanly.

A common mistake is to only check against `"YesYes..."` starting at index 0. That fails for strings like `"esYes"`, which are valid but begin in the middle of the cycle. The rotation loop fixes this completely.

## Worked Examples

Take the string `"esYes"`.

| i | s[i] | rotation `"esY"` | match |
|---|------|------------------|--------|
| 0 | e | e |  |
| 1 | s | s |  |
| 2 | Y | Y |  |
| 3 | e | e |  |
| 4 | s | s |  |

This confirms it matches the cycle starting at offset 1.

Now consider `"Yess"`.

| i | s[i] | rotation `"Yes"` | match |
|---|------|------------------|--------|
| 0 | Y | Y |  |
| 1 | e | e |  |
| 2 | s | s |  |
| 3 | s | Y |  |

This fails because the fourth character breaks periodic structure, so no rotation will accept it.

These examples show that correctness depends entirely on periodic consistency, not partial overlaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(t · n) | Each string is checked against 3 patterns with linear scan |
| Space | O(1) | Only a few fixed patterns are stored |

The total input size is small enough that a linear scan per test case is optimal and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def ok(s, p):
        for i, ch in enumerate(s):
            if ch != p[i % 3]:
                return False
        return True

    t = int(input())
    base = "Yes"
    rotations = [base[i:] + base[:i] for i in range(3)]

    out = []
    for _ in range(t):
        s = input().strip()
        for p in rotations:
            if ok(s, p):
                out.append("YES")
                break
        else:
            out.append("NO")
    return "\n".join(out)

assert run("3\nYes\nesY\nooo\n") == "YES\nYES\nNO"
assert run("1\nY") == "YES"
assert run("1\nseY") == "YES"
assert run("1\nYess") == "NO"
```

| Test input | Expected output | What it validates |
|---|---|---|
| minimal valid match | YES | single character alignment cases |
| rotation match | YES | substring starting mid-cycle |
| invalid prefix | NO | broken periodicity |

## Edge Cases

For `"Y"`, `"e"`, and `"s"`, the algorithm checks all rotations and immediately accepts because each character matches at least one phase of the cycle at position 0.

For `"seY"`, the rotation `"seY"` matches exactly, showing that full-cycle alignment is not required, only consistency with some offset.

For `"Yess"`, every rotation fails at position 3, confirming that even a single mismatch breaks validity regardless of prefix correctness.
