---
title: "CF 345F - Superstitions Inspection"
description: "The input describes a collection of countries, where each country is followed by a list of superstition names observed in that country. Each superstition is written as a line starting with an asterisk, and names may contain multiple words separated by irregular spacing."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "F"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 2700
weight: 345
solve_time_s: 113
verified: false
draft: false
---

[CF 345F - Superstitions Inspection](https://codeforces.com/problemset/problem/345/F)

**Rating:** 2700  
**Tags:** *special  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

The input describes a collection of countries, where each country is followed by a list of superstition names observed in that country. Each superstition is written as a line starting with an asterisk, and names may contain multiple words separated by irregular spacing. Countries appear as standalone lines without the asterisk prefix.

The task is to determine which superstition names appear in the largest number of distinct countries. Two superstition names should be considered identical even if their capitalization differs or if they contain inconsistent spacing between words. After identifying the maximum frequency, we must output all superstition names that achieve this maximum, sorted lexicographically by their normalized form.

The main difficulty is not counting itself, but correctly parsing and normalizing names. A superstition like "Friday the 13th", "friday   THE 13TH", and "FRIDAY the 13th" must all collapse into the same canonical representation. Similarly, country boundaries matter because occurrences are counted per country, not per line or per raw entry.

The constraints are extremely small in terms of input size, at most 50 lines of up to 50 characters each. This immediately rules out any concern about asymptotic efficiency beyond simple linear parsing. Even a quadratic or cubic grouping strategy would be acceptable, but clean linear hashing solutions are more appropriate.

The subtle failure modes come entirely from string normalization and grouping logic.

One common mistake is counting repeated occurrences within a single country multiple times. The statement explicitly says entries are unique within each country, but robust solutions should still guard against accidental duplication introduced by normalization. For example, if a country had:

```
* Black cat
* black   CAT
```

both must be treated as the same superstition, but still only contribute a single country occurrence.

Another pitfall is failing to correctly split country boundaries. Country names appear without a prefix, but they may consist of multiple words. A naive parser that assumes every non-asterisk line is a country header works here because format is consistent, but trimming and state management must be precise.

Finally, spacing normalization is tricky: multiple spaces between words should be treated as a single separator, and leading or trailing spaces should be ignored entirely.

## Approaches

A brute-force interpretation would proceed by storing every occurrence of every superstition per country, then for each superstition recomputing how many distinct countries contain it. This could be done by maintaining a mapping from superstition to a list of countries and deduplicating later. Given the input is tiny, even nested loops over all countries and all superstition lists would pass, but it is conceptually wasteful and error-prone.

The key observation is that we never need raw lists after parsing. We only need a mapping from each normalized superstition name to the set of countries in which it appears. This reduces the problem to a straightforward frequency count over sets.

The main technical insight is normalization. Each superstition must be converted into a canonical form by lowercasing all words and collapsing multiple spaces. Once this is done, identical superstition names become identical keys in a dictionary. Then, instead of counting occurrences, we accumulate a set of countries per superstition.

At the end, we compute the maximum size among these sets and output all keys reaching that size in sorted order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute per superstition) | O(N²) | O(N) | Accepted |
| Optimal (hash map + sets) | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read input line by line while tracking the current country name. Any line not starting with `*` is treated as a new country header. We normalize the country name in a stable way (lowercase and trimmed spacing) so it can be used as a dictionary key.
2. For each superstition line, remove the leading `*`, then normalize the remainder. Normalization means splitting by whitespace and joining words with single spaces after converting to lowercase. This guarantees that all spacing and capitalization variations collapse into a single representation.
3. Maintain a dictionary `occ`, where each superstition maps to a set of countries. When we encounter a superstition in a country, we insert the current country into that set. Using a set automatically ensures multiple mentions within the same country do not inflate counts.
4. After processing all lines, compute the maximum size among all country sets stored in `occ`.
5. Collect all superstition names whose set size equals this maximum value.
6. Sort these superstition names lexicographically and output them one per line.

The correctness hinges on the fact that every superstition-country relationship is recorded exactly once in a set, so frequency becomes the cardinality of that set.

### Why it works

At any point in processing, the structure `occ[s]` represents exactly the set of countries in which superstition `s` has appeared so far. Since each country contributes at most one membership to this set, the final size of the set is exactly the number of distinct countries containing that superstition. Normalization ensures that all equivalent textual variants map to the same key, so no split identities occur. Therefore selecting maximum set size correctly identifies the most widespread superstition(s).

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize_name(s: str) -> str:
    return " ".join(s.strip().lower().split())

def solve():
    occ = {}
    current_country = None

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue

        if not line.startswith("*"):
            current_country = normalize_name(line)
            continue

        superstition = normalize_name(line[1:])
        if superstition not in occ:
            occ[superstition] = set()
        occ[superstition].add(current_country)

    max_count = 0
    for s in occ:
        max_count = max(max_count, len(occ[s]))

    result = [s for s in occ if len(occ[s]) == max_count]
    result.sort()

    print("\n".join(result))

if __name__ == "__main__":
    solve()
```

The solution relies on a simple state machine: we switch between reading country headers and superstition entries. The normalization function is critical because it guarantees both case-insensitivity and whitespace collapse in one step.

A subtle detail is that we never assume superstition uniqueness per country explicitly. Even though the statement guarantees it, storing into a set makes the solution robust and simplifies reasoning.

## Worked Examples

### Example 1

Input:

```
Ukraine
* Friday the   13th
* black   cat
USA
* friday   THE 13th
* Black Cat
```

| Step | Country | Superstition | Normalized | Occ State |
| --- | --- | --- | --- | --- |
| 1 | ukraine | friday the 13th | friday the 13th | {ukraine} |
| 2 | ukraine | black cat | black cat | {ukraine} |
| 3 | usa | friday the 13th | friday the 13th | {ukraine, usa} |
| 4 | usa | black cat | black cat | {ukraine, usa} |

Both superstition sets end with size 2, so both are output in sorted order.

This demonstrates that normalization merges variants correctly and that sets prevent double counting within a country.

### Example 2

Input:

```
A
* lucky coin
* lucky coin
B
* Lucky   Coin
C
* unlucky cat
```

| Step | Country | Superstition | Normalized | Occ State |
| --- | --- | --- | --- | --- |
| 1 | a | lucky coin | lucky coin | {a} |
| 2 | a | lucky coin | lucky coin | {a} |
| 3 | b | lucky coin | lucky coin | {a, b} |
| 4 | c | unlucky cat | unlucky cat | {c} |

The repeated entry in country A does not change the set. The maximum frequency is 2 for "lucky coin".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · L) | Each line is parsed once, and normalization is linear in line length |
| Space | O(K) | Each distinct superstition stores a set of countries |

Given at most 50 lines of length 50, the solution is trivially within limits. Even with heavy overhead from Python sets and dictionaries, performance is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout

# provided sample
assert capture("""Ukraine
* Friday the   13th
* black   cat
* knock the   wood
USA
* wishing well
* friday   the   13th
Holland
France
* Wishing Well""") == "friday the 13th\nwishing well"

# all same superstition across countries
assert capture("""A
* bad luck
B
* Bad   Luck
C
* BAD LUCK""") == "bad luck"

# single country only
assert capture("""A
* one two
* three four""") == "one two\nthree four"

# tie case
assert capture("""A
* x
B
* y""") == "x\ny"

# repeated entries in same country
assert capture("""A
* repeat
* repeat
B
* repeat""") == "repeat"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| normalization variants | merged output | case and spacing collapse |
| single country | all listed | no cross-country requirement |
| tie case | both sorted | correct tie handling |
| duplicates in one country | single count | set deduplication |

## Edge Cases

One edge case is multiple occurrences of the same superstition within a single country after normalization. For example:

```
A
* Black Cat
* black   cat
B
* black cat
```

The algorithm processes country A and inserts "black cat" once into its set. The second insertion is ignored by the set, so the final set is `{A, B}`. The output count remains correct at 2.

Another edge case is inconsistent spacing in country names themselves. Since country names are normalized before use as dictionary keys, "United  States" and "United States" would collapse to the same identifier if they appeared, ensuring correctness even under noisy formatting.

A final edge case is an input where a country has no superstition entries. The parser correctly updates `current_country` but performs no insertions until a starred line appears, so no invalid state is introduced and the structure remains consistent.
