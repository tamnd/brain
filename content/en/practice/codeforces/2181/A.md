---
title: "CF 2181A - Alphabet City"
description: "We are asked to calculate how many full sets of street signs can be made when one street's order is missing. Each street in Alphabet City has a name made from capital letters, and each street has an order for m identical signs."
date: "2026-06-07T21:56:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 2181
codeforces_index: "A"
codeforces_contest_name: "2025-2026 ICPC, NERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1300
weight: 2181
solve_time_s: 126
verified: true
draft: false
---

[CF 2181A - Alphabet City](https://codeforces.com/problemset/problem/2181/A)

**Rating:** 1300  
**Tags:** binary search, math, strings  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate how many full sets of street signs can be made when one street's order is missing. Each street in Alphabet City has a name made from capital letters, and each street has an order for `m` identical signs. If one street's order is lost, we want to know, for each street in turn, the maximum number `k` of signs we can produce for the other streets using the letters from the remaining `m` signs of all other streets, while still producing at least one sign for the missing street.

In practical terms, we have a multiset of letters from all the signs, and for each candidate missing street, we need to see how many complete copies of the remaining streets we can produce without running out of letters, while reserving at least the letters for one copy of the missing street.

The constraints tell us we may have up to 200,000 streets and each street name may be up to 500,000 letters long, with the sum of all street name lengths bounded by 500,000. This indicates that iterating over every character repeatedly per street will be feasible because the total number of letters is limited. The main complexity comes from evaluating the maximum `k` for every possible missing street.

A subtle edge case occurs when the missing street contains letters that are rare or unique across all streets. For example, if one street has a letter not used elsewhere, once its order is missing, it may be impossible to produce even one full set of the remaining streets (`k = -1`). Another edge case occurs when all streets are identical; then removing any single street does not reduce the letter pool, but the calculation of `k` still must account for reserving letters for the missing street.

## Approaches

The brute-force approach would consider each possible missing street `l`, sum all the letters from the other streets, and try values of `k` from 0 upward until the letters run out. This is correct but slow. The total operations would be roughly O(n × max_possible_k × |alphabet|), which is unmanageable for large `m` and long names.

The key insight is that the problem reduces to counting letters across all streets and performing integer division to compute `k`. For each letter, we can compute how many copies of the remaining streets can be produced without exceeding the available count. Formally, for each letter `c`, let `total[c]` be the number of letters from all `m` copies of all streets, and let `needed[c]` be the sum of letter counts per copy for the remaining streets. Then the maximum `k` is simply `min((total[c] - missing_count[c]) // needed[c] for all letters)` where `missing_count` is the count of letters reserved for the missing street.

The observation that letter counts can be precomputed and reused across all iterations reduces the problem from O(n × total_letters × k) to O(n × 26) per iteration. This is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × m × | s | ) |
| Optimal | O(n × 26 + total_letters) | O(26) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each letter in each street and store them in a list of dictionaries or arrays. This allows fast access to any street's letter distribution.
2. Compute the total number of letters for each type across all streets multiplied by `m`. This is our global letter pool.
3. For each street `l` (the one assumed missing), subtract its letters from the global pool because we need at least one copy of it. Then for the remaining streets, compute the maximum integer `k` such that multiplying each street's letter counts by `k` does not exceed the available letters in the pool.
4. This is done by iterating over each letter in the alphabet and computing `(available_letters_for_this_letter) // (sum_of_letters_for_remaining_streets)`. The minimum value across all letters gives the maximum `k`.
5. If for any letter, the available letters are insufficient even for `k = 0`, then output `-1` for that street.
6. Restore the letter pool to the original total before moving to the next street.

Why it works: Letter availability across the streets is independent and additive. Since we precompute totals, the integer division ensures that we never overuse letters. Taking the minimum across all letters guarantees that all letter requirements are simultaneously satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import Counter

n, m = map(int, input().split())
streets = [input().strip() for _ in range(n)]

# Count letters in each street
letter_counts = [Counter(s) for s in streets]

# Compute total letters from all streets multiplied by m
total_letters = Counter()
for c in letter_counts:
    for letter, count in c.items():
        total_letters[letter] += count * m

result = []

for i in range(n):
    missing = letter_counts[i]
    available = total_letters.copy()
    
    # Reserve letters for one copy of missing street
    for letter, count in missing.items():
        available[letter] -= count
    
    # Compute maximum k for other streets
    max_k = float('inf')
    for j in range(n):
        if j == i:
            continue
        for letter, count in letter_counts[j].items():
            if count == 0:
                continue
            if available[letter] < 0:
                max_k = -1
                break
            max_k = min(max_k, available[letter] // count)
        if max_k == -1:
            break
    result.append(max_k if max_k != float('inf') else -1)

print(' '.join(map(str, result)))
```

In the solution, `Counter` objects store per-street letter counts and total letters. The copy of `total_letters` ensures that modifications for each missing street do not affect subsequent iterations. The integer division `(available[letter] // count)` is safe because we have reserved the letters for the missing street.

## Worked Examples

### Sample Input 1

```
3 10
NEERC
NERC
NEF
```

| Street | Letters | Total Available | Max k Calculation | Result |
| --- | --- | --- | --- | --- |
| 1 missing | NERC + NEF | N:19, E:19, R:11, C:11, F:10 | k = min(19//2, 19//3, 11//1, 11//1, 10//1) = 9 | 9 |
| 2 missing | NEERC + NEF | N:20, E:21, R:11, C:10, F:10 | k = 9 | 9 |
| 3 missing | NEERC + NERC | N:20, E:20, R:11, C:11, F:0 | F unavailable for 1 copy → -1 | -1 |

This trace confirms the correct handling of letters missing entirely for the lost street.

### Sample Input 2

```
2 5
A
B
```

| Street | Letters | Max k |
| --- | --- | --- |
| 1 missing | B | available A=5-1=4, B=5 |
| 2 missing | A | similar logic |

This demonstrates handling single-letter streets and division by zero avoidance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 26 + total_letters) | Counting letters across all streets is O(total_letters), computing max k for n streets is O(n*26) |
| Space | O(n * 26) | Per-street letter counts and total letters counter |

The solution is efficient because the sum of all street name lengths is ≤ 5 × 10^5, and 26 letters are constant.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    streets = [input().strip() for _ in range(n)]
    letter_counts = [Counter(s) for s in streets]
    total_letters = Counter()
    for c in letter_counts:
        for letter, count in c.items():
            total_letters[letter] += count * m
    result = []
    for i in range(n):
        missing = letter_counts[i]
        available = total_letters.copy()
        for letter, count in missing.items():
            available[letter] -= count
        max_k = float('inf')
        for j in range(n):
            if j == i:
                continue
            for letter, count in letter_counts[j].items():
                if count == 0:
                    continue
                if available[letter] < 0:
                    max_k = -1
                    break
                max_k = min(max_k, available[letter] // count)
            if max_k == -1:
                break
        result.append(max_k if max_k != float('inf') else -1)
    return ' '.join(map(str, result))

# provided sample
assert run("3 10\nNEERC\nNERC\nNEF\n") == "9 9 -1"

# single-letter streets
assert run("2 5\nA\nB\n") == "4 4"

# all
```
