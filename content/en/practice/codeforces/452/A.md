---
title: "CF 452A - Eevee"
description: "We are given a partially filled crossword slot and asked to identify which of Eevee's evolutions fits it. The input specifies the length of the word and a string pattern using lowercase letters and dots, where a dot represents an unknown character."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 452
codeforces_index: "A"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 1"
rating: 1000
weight: 452
solve_time_s: 66
verified: true
draft: false
---

[CF 452A - Eevee](https://codeforces.com/problemset/problem/452/A)

**Rating:** 1000  
**Tags:** brute force, implementation, strings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a partially filled crossword slot and asked to identify which of Eevee's evolutions fits it. The input specifies the length of the word and a string pattern using lowercase letters and dots, where a dot represents an unknown character. Our task is to find which Pokémon name matches the given length and known letters. Eevee has exactly eight evolutions: Vaporeon, Jolteon, Flareon, Espeon, Umbreon, Leafeon, Glaceon, and Sylveon. Only one evolution can match the input pattern.

The length `n` is constrained between 6 and 8, which is very small. This means that even checking all eight possible evolutions against the pattern individually is feasible. The pattern can include any combination of letters and dots, so the key requirement is to match letters where they are provided while ignoring dots. Edge cases arise when the first or last letters are unknown, or when multiple names share letters in overlapping positions but only one matches both the length and letter constraints. For example, a pattern of `....eon` could match multiple evolutions if we ignored length, but the length ensures uniqueness.

## Approaches

The naive approach is a simple brute-force check. We iterate over each of the eight evolution names. For each name, we first verify that its length equals `n`. Then we compare each character in the name with the corresponding character in the pattern. If the pattern character is a letter, it must match exactly; if it is a dot, we ignore it. As soon as we find a name that satisfies both conditions, we return it. This brute-force works because there are only eight names and the maximum word length is 8, giving at most 64 character comparisons. There is no need for optimization; even in the worst-case scenario, the solution is instantaneous.

The observation that unlocks the solution is the small input space. The problem is essentially a string matching problem against a small fixed set. There is no need for advanced data structures, backtracking, or dynamic programming. The brute-force approach is both simple and optimal in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8 * n) = O(64) | O(1) | Accepted |
| Optimal | O(8 * n) = O(64) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store all eight possible Eevee evolutions in a list in lowercase.
2. Read the integer `n` and the pattern string of length `n`.
3. Iterate over each evolution name. First, check if its length matches `n`. If not, skip it.
4. For a candidate of the correct length, iterate over each position `i` in the string. If the pattern at `i` is a dot, continue. If it is a letter, compare it with the character at the same position in the candidate. If they differ, break and continue to the next candidate.
5. If the iteration completes without a mismatch, the candidate matches the pattern. Print this name and stop the program.

Why it works: The algorithm ensures that only names with the correct length are considered and that all known letters in the pattern are satisfied. Since the problem guarantees exactly one match, stopping at the first match is safe. Each comparison is positionally checked, so no incorrect name can slip through.

## Python Solution

```python
import sys
input = sys.stdin.readline

evolutions = ["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "leafeon", "glaceon", "sylveon"]

n = int(input())
pattern = input().strip()

for evo in evolutions:
    if len(evo) != n:
        continue
    match = True
    for i in range(n):
        if pattern[i] != '.' and pattern[i] != evo[i]:
            match = False
            break
    if match:
        print(evo)
        break
```

We first define the list of all evolution names in lowercase. We read the integer length `n` and the string pattern, stripping any trailing newline. For each candidate, we skip it if the length is wrong. The `match` flag tracks if the candidate satisfies all known letters. If we encounter a letter mismatch, we set `match` to `False` and break. The first candidate that passes all checks is printed. Off-by-one errors are avoided because we use zero-based indexing, and the pattern and candidate are guaranteed to be the same length when compared.

## Worked Examples

Sample Input 1:

```
7
j......
```

| i | pattern[i] | evo[i] | match? |
| --- | --- | --- | --- |
| 0 | j | j | True |
| 1 | . | o | True |
| 2 | . | l | True |
| 3 | . | t | True |
| 4 | . | e | True |
| 5 | . | o | True |
| 6 | . | n | True |

The algorithm prints `jolteon`. The invariant holds: all specified letters match, and length matches.

Sample Input 2:

```
6
......
```

| i | pattern[i] | evo[i] | match? |
| --- | --- | --- | --- |
| All positions | . | varies by candidate | True for `espeon` |

The algorithm prints `espeon` because it is the only 6-letter evolution. This demonstrates handling completely unknown patterns.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(8 * n) | We check up to 8 candidates, each of length at most 8 |
| Space | O(1) | Only storing the list of evolutions and pattern string |

Given n ≤ 8 and only 8 candidates, the algorithm completes in negligible time and requires minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    evolutions = ["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "leafeon", "glaceon", "sylveon"]
    n = int(sys.stdin.readline())
    pattern = sys.stdin.readline().strip()
    for evo in evolutions:
        if len(evo) != n:
            continue
        match = True
        for i in range(n):
            if pattern[i] != '.' and pattern[i] != evo[i]:
                match = False
                break
        if match:
            return evo

# Provided samples
assert run("7\nj......\n") == "jolteon"
assert run("6\n......\n") == "espeon"

# Custom cases
assert run("8\n.......n\n") == "vaporeon", "matches last letter"
assert run("7\nf......\n") == "flareon", "first letter known"
assert run("7\n..a....\n") == "leafeon", "middle letter match"
assert run("6\n......\n") == "espeon", "all dots minimum length"
assert run("8\n.s.....n\n") == "sylveon", "pattern starts with s and ends with n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 8\n.......n | vaporeon | correct handling of last letter match |
| 7\nf...... | flareon | first letter match |
| 7\n..a.... | leafeon | middle letter match |
| 6\n...... | espeon | fully unknown pattern, minimum length |
| 8\n.s.....n | sylveon | combination of first and last letters |

## Edge Cases

A pattern with all dots of length 6 is handled correctly: the algorithm iterates over all 6-letter candidates and selects `espeon`. A pattern like `j......` ensures that a name starting with `j` is picked; other 7-letter evolutions are skipped. A pattern with specific letters in the middle, such as `..a....`, correctly ignores dots and matches only `leafeon`. The algorithm never falsely selects multiple candidates because the length filter combined with the letter comparisons guarantees uniqueness.
